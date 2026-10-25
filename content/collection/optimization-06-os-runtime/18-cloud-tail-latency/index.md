---
collection_order: 18
date: 2026-07-13
lastmod: 2026-10-24
draft: false
image: wordcloud.png
title: "[OS 06] 클라우드 환경 꼬리 지연"
slug: cloud-noisy-neighbor-cpu-steal-time
description: "퍼블릭 클라우드의 Noisy Neighbor 현상과 CPU Steal Time의 발생 원리를 mpstat %steal 지표로 분석하고, 인스턴스 타입 선택·전용 호스트·Sole-Tenant 노드·모니터링으로 꼬리 지연을 방어하는 실무 전략을 정리합니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - OS(운영체제)
  - Linux(리눅스)
  - CPU(Central Processing Unit)
  - Cloud(클라우드)
  - Kubernetes
  - Latency
  - Monitoring(모니터링)
  - Observability
  - Best-Practices
  - System-Design
  - Production
  - Reliability
  - Scalability(확장성)
  - Hardware(하드웨어)
  - Deep-Dive
  - Advanced
  - Comparison(비교)
  - Pitfalls(함정)
  - Edge-Cases(엣지케이스)
  - Guide(가이드)
  - Reference(참고)
  - Noisy-Neighbor
  - CPU-Steal-Time
  - Dedicated-Host
  - Sole-Tenancy
  - Nitro-System
  - Hypervisor
  - Multi-Tenancy
---

**클라우드 환경 꼬리 지연**이란 퍼블릭 클라우드의 공유 물리 하드웨어 위에서 다른 테넌트(입주자)의 워크로드가 내 인스턴스의 CPU·캐시·메모리 대역폭·I/O 자원을 잠식해, 평균 지연은 그대로인데 p99·p999 같은 꼬리 지연만 튀는 현상을 말합니다. 코드와 컴파일 플래그를 아무리 다듬어도, 내 vCPU가 물리 코어를 실제로 배정받지 못하고 하이퍼바이저 대기열에서 기다리는 시간(**CPU Steal Time**)이 늘어나면 그 위의 모든 최적화가 잡음에 묻힙니다. 이 장은 이 트랙에서 다룬 스케줄링·affinity·컨테이너 자원 제어가 "내 프로세스 안"의 문제였다면, 그 경계를 넘어 "내가 통제할 수 없는 이웃"이 만드는 지연을 어떻게 관측하고 방어하는지를 다룹니다.

## 이 장을 읽기 전에

이 장은 트랙 인트로인 [Introduction: OS·런타임 Low-latency 운영환경](/post/os-optimization/getting-started-os-runtime-performance-tuning/)에서 정리한 "운영환경이 지연 분포를 결정한다"는 관점과, [03장: CPU Pinning/Affinity 전략](/post/os-optimization/cpu-pinning-affinity-strategy/)·[04장: NUMA CPU Affinity·스레드 배치](/post/os-optimization/numa-cpu-affinity-thread-placement/)에서 다룬 "코어를 명시적으로 통제한다"는 개념을 전제로 합니다. 정밀한 지연 측정 방법은 [06장: 정밀 시간 측정](/post/os-optimization/precise-time-measurement-rdtsc-clock-gettime/)에서 다룬 `clock_gettime`·RDTSC를 그대로 사용합니다. **이 장의 깊이**는 **심화**입니다. CPU Steal Time의 측정 원리, Noisy Neighbor가 발생하는 구조, 인스턴스 타입·전용 호스트 선택 전략을 다루되, 통계적으로 엄밀한 SLA 산정이나 특정 클라우드 벤더의 과금 세부사항은 다루지 않습니다. **다루지 않는 것**: Kubernetes 노드 내부의 CFS quota·isolcpus·Intel RDT 조합은 [11장: 컨테이너/가상화 성능 고려사항](/post/os-optimization/container-virtualization-performance-considerations/)에서, cgroups v2 컨트롤러 세부 메커니즘은 [13장: cgroups v2 리소스 제어](/post/os-optimization/cgroups-v2-resource-control-performance/)에서 이미 다뤘으므로 여기서는 반복하지 않고 링크로 위임합니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **중급자** | 도입 ~ "CPU Steal Time이 보여주는 것" | steal time이 무엇을 측정하고 무엇을 측정하지 않는지 이해 |
| **심화 학습자** | "Noisy Neighbor가 발생하는 구조" ~ "흔한 오개념" | 오버커밋·버스터블 크레딧·SMT 경합의 메커니즘 파악 |
| **전문가** | "방어 전략" ~ "비판적 시각" | 인스턴스·격리 옵션 선택과 전용 호스트의 한계를 판단 |

---

## Noisy Neighbor와 CPU Steal Time의 등장 배경

**Noisy Neighbor**라는 용어 자체는 특정 발명가나 발표 논문이 있는 개념이라기보다, 멀티테넌트 인프라가 상용화되면서 운영자들 사이에서 자연스럽게 굳어진 표현입니다. 하드웨어 하나를 여러 고객에게 나눠 파는 모델은 메인프레임의 타임셰어링 시절부터 있었지만, 이것이 지연시간 문제로 본격적으로 불거진 것은 2006년 전후 Amazon EC2 같은 퍼블릭 클라우드가 등장하면서부터입니다. 서로 신뢰 관계가 없는 여러 회사의 VM이 같은 물리 서버 위에서 동시에 실행되기 시작하자, 한 테넌트의 부하 급증이 물리적으로 인접한 다른 테넌트의 성능을 갉아먹는 현상이 운영 이슈로 떠올랐습니다.

이 현상을 게스트 OS 관점에서 정량화한 지표가 **CPU Steal Time**입니다. Xen 같은 반가상화(paravirtualization) 하이퍼바이저는 게스트 커널이 "내 vCPU가 실행 가능한 상태인데도 하이퍼바이저가 다른 손님을 서비스하느라 나를 스케줄링하지 않은 시간"을 스스로 알 수 있도록 커널에 훅을 심었습니다. 리눅스는 `/proc/stat`의 CPU 통계 줄에 **steal** 필드를 두어 이 시간을 노출하며, 하이퍼바이저가 이 값을 채웁니다. `mpstat`·`top`·`vmstat` 같은 표준 도구의 `%st`(steal) 컬럼은 모두 이 필드를 읽어 표시하는 것이며, [Linux man-pages 프로젝트의 mpstat(1) 문서](https://man7.org/linux/man-pages/man1/mpstat.1.html)는 이를 "가상 CPU가 하이퍼바이저가 다른 가상 프로세서를 서비스하는 동안 비자발적으로 대기한 시간의 비율"로 정의합니다.

## CPU Steal Time이 보여주는 것: 하이퍼바이저 스케줄링의 그림자

Steal time을 정확히 이해하려면 하이퍼바이저가 무엇을 스케줄링하는지부터 봐야 합니다. 물리 코어(pCPU) 하나 위에 여러 테넌트의 vCPU가 시분할로 얹히는 오버커밋(overcommit) 환경에서, 호스트 스케줄러는 각 vCPU에게 타임슬라이스를 순서대로 배정합니다. 내 vCPU가 실행 대기열(run queue)에서 실행 가능한 상태로 남아 있는데도 다른 테넌트의 vCPU가 슬라이스를 쓰는 중이라면, 그 대기 시간이 게스트 커널 입장에서는 steal time으로 누적됩니다. 즉 steal time은 "내가 유휴(idle)해서 안 쓴 시간"이 아니라 "쓰고 싶었는데 못 쓴 시간"이라는 점이 핵심이며, 이 구분이 idle time과 steal time을 나누는 이유입니다.

이 값이 실제로 어떻게 계산되는지는 `/proc/stat`을 직접 읽어보면 가장 분명해집니다. 아래 프로그램은 `mpstat`이 내부적으로 하는 일과 동일하게, 두 시점 사이의 누적 CPU 시간 델타에서 steal 비율을 계산합니다.

```c
#include <stdio.h>
#include <unistd.h>

// /proc/stat 첫 줄 형식: cpu user nice system idle iowait irq softirq steal ...
typedef struct {
  unsigned long long user, nice, system, idle, iowait, irq, softirq, steal;
} CpuTimes;

static int read_cpu_times(CpuTimes *t) {
  FILE *f = fopen("/proc/stat", "r");
  if (!f) return -1;
  int n = fscanf(f, "cpu %llu %llu %llu %llu %llu %llu %llu %llu",
                 &t->user, &t->nice, &t->system, &t->idle,
                 &t->iowait, &t->irq, &t->softirq, &t->steal);
  fclose(f);
  return (n == 8) ? 0 : -1;
}

static unsigned long long total(const CpuTimes *t) {
  return t->user + t->nice + t->system + t->idle + t->iowait + t->irq + t->softirq + t->steal;
}

int main(void) {
  CpuTimes prev, cur;
  if (read_cpu_times(&prev) != 0) { fprintf(stderr, "read failed\n"); return 1; }
  for (;;) {
    sleep(1);
    if (read_cpu_times(&cur) != 0) break;
    unsigned long long dt = total(&cur) - total(&prev);
    unsigned long long dsteal = cur.steal - prev.steal;
    double pct = dt ? (100.0 * (double)dsteal / (double)dt) : 0.0;
    printf("steal: %.2f%%\n", pct);
    prev = cur;
  }
  return 0;
}
```

`gcc -O2 -o steal_monitor steal_monitor.c`(Linux x86-64/ARM64 공통, 커널 버전 무관하게 `/proc/stat`에 steal 필드가 있으면 동작)로 빌드해 실행하면 1초 간격으로 steal 비율이 출력됩니다. 팀마다 기준은 다르지만, steal time이 낮은 한 자릿수 percent를 넘어 지속적으로 관측되면 인스턴스 배치나 타입을 재검토하는 경험적 관행이 널리 쓰입니다. 다만 컨테이너 안에서 이 프로그램을 돌리면 namespace가 `/proc/stat`을 완전히 격리하지 않는 경우가 많아 호스트 전체의 steal 값이 보일 수 있다는 점은 주의해야 합니다 — 컨테이너 스코프의 CPU 자원 통제는 [11장](/post/os-optimization/container-virtualization-performance-considerations/)에서 다룬 cgroup 계정 방식과는 별개의 문제입니다.

## Noisy Neighbor가 발생하는 구조: 오버커밋과 버스터블 크레딧

CPU steal time이 관측되는 근본 원인은 클라우드 사업자가 물리 코어 수보다 많은 vCPU를 판매하는 **오버커밋**에 있습니다. 오버커밋 자체는 나쁜 설계가 아닙니다 — 대부분의 워크로드가 항상 CPU를 100% 쓰지 않는다는 통계적 사실 위에서 비용 효율을 높이는 정상적인 자원 관리 기법입니다. 문제는 오버커밋 비율이 클수록, 그리고 같은 물리 호스트에 배치된 이웃 테넌트의 부하 패턴이 예측 불가능할수록, 내 vCPU가 대기열에서 기다리는 시간의 분산이 커진다는 데 있습니다.

이 구조가 가장 두드러지는 것이 **버스터블(burstable) 인스턴스 계열**(AWS T 시리즈, Azure B 시리즈 등)입니다. 이 계열은 평상시 낮은 기준 성능만 보장하고, CPU 크레딧을 적립해 두었다가 순간적인 버스트에 그 크레딧을 소모하는 방식으로 가격을 낮춥니다. 크레딧이 소진되면 성능이 기준선으로 강제로 떨어지는데, 이 강제 저하와 이웃 테넌트로 인한 steal time 증가가 동시에 나타나면 어느 쪽이 원인인지 게스트 지표만으로는 구분하기 어렵습니다. 반대로 "고정 성능(fixed performance)" 인스턴스는 일반적으로 이런 변동성이 작다고 알려져 있지만, 오버커밋 정책은 사업자가 공개하지 않는 부분이 많아 직접 측정해야 합니다. 물리 코어 하나를 SMT(Simultaneous Multi-Threading)로 둘로 쪼갠 논리 코어를 서로 다른 워크로드가 나눠 쓰는 구성에서는, steal time에 잡히지 않는 또 다른 경합도 남습니다 — 같은 물리 코어를 공유하는 형제(sibling) 논리 코어가 L1/L2 캐시와 실행 유닛을 두고 경쟁하기 때문입니다. 이 경합은 스케줄링 대기가 아니라 명령어 처리량 저하로 나타나므로 `%steal`에는 반영되지 않습니다.

이 관계를 하나의 그림으로 정리하면 다음과 같습니다. 호스트 하이퍼바이저 스케줄러가 물리 코어 하나를 여러 테넌트의 vCPU에 시분할로 배정하는 동안, 대기 중인 테넌트의 게스트 커널에는 그 대기 시간이 steal time으로 누적됩니다.

```mermaid
flowchart TD
  tenantA["Tenant A vCPU</br>(내 워크로드)"]
  tenantB["Tenant B vCPU</br>(이웃 워크로드)"]
  hostScheduler["호스트 하이퍼바이저 스케줄러"]
  physicalCore["물리 코어 pCPU"]
  tenantA --> hostScheduler
  tenantB --> hostScheduler
  hostScheduler -- "타임슬라이스 배정" --> physicalCore
  hostScheduler -- "대기 중</br>(steal 누적)" --> tenantA
  physicalCore -- "슬라이스 종료" --> hostScheduler
```

## 재현과 관찰: 로컬에서 경합 만들어보기

실제 하이퍼바이저 수준의 steal time은 다른 고객의 워크로드에 의존하므로 재현할 수 없습니다. 다만 같은 게스트 안에서 이웃 부하가 반복 작업의 완료 시간 분포에 미치는 영향은 관찰할 수 있습니다. 아래 스크립트는 논리 코어 하나를 측정 대상으로 삼아, 이웃 부하가 없을 때와 다른 코어에 있을 때와 같은 코어에 있을 때를 나란히 비교합니다.

```bash
#!/usr/bin/env bash
# 환경: Linux x86-64, stress-ng (apt install stress-ng), coreutils, 코어 2개 이상
# 목적: 측정 코어(TARGET_CPU)의 고정 작업 완료 시간을 RUNS번 재서 이웃 부하의 영향을 비교한다.
# 한계: 하이퍼바이저의 vCPU 오버커밋은 만들 수 없다. 같은 게스트 안에서
#       (a) 다른 코어의 부하, (b) 같은 코어를 공유하는 부하만 비교한다.
set -euo pipefail
NCPU=$(nproc)
if [ "$NCPU" -lt 2 ]; then echo "코어 2개 이상 필요" >&2; exit 1; fi
TARGET_CPU=0
RUNS=100

measure() {  # 측정 코어에서 고정 작업을 RUNS번 수행하고 걸린 ns를 한 줄씩 출력
  for _ in $(seq 1 "$RUNS"); do
    start=$(date +%s%N)
    taskset -c "$TARGET_CPU" bash -c 'for i in $(seq 1 200000); do :; done'
    echo $(( $(date +%s%N) - start ))
  done
}

summarize() {  # 입력(ns)의 p50, p99, max를 출력
  sort -n | awk '{a[NR]=$1} END {i=int((NR-1)*0.99)+1; if (i>NR) i=NR; print "p50=" a[int(NR*0.5)+1] " p99=" a[i] " max=" a[NR] " (ns, n=" NR ")"}'
}

echo "=== 이웃 부하 없음 ==="
measure | summarize

echo "=== 다른 코어에 부하 ==="
stress-ng --taskset "1-$((NCPU-1))" --cpu $((NCPU-1)) --timeout 600s &
STRESS_PID=$!
sleep 1
measure | summarize
kill "$STRESS_PID" 2>/dev/null || true
wait || true

echo "=== 같은 코어에 부하(코어 공유) ==="
stress-ng --taskset "$TARGET_CPU" --cpu 1 --timeout 600s &
STRESS_PID=$!
sleep 1
measure | summarize
kill "$STRESS_PID" 2>/dev/null || true
wait || true
```

이 스크립트는 하이퍼바이저의 vCPU 오버커밋과 steal time을 만들지 못합니다. 대신 같은 게스트 안에서 이웃 부하의 두 가지 영향을 분리해 보여 줍니다. 두 번째 측정은 다른 코어의 부하가 SMT 형제 코어, 공유 캐시, 주파수 같은 간접 경로로 주는 영향을, 세 번째 측정은 하나의 코어를 두 작업이 시분할하면서 생기는 대기 효과를 보여 줍니다. 세 번째 상황이 오버커밋된 vCPU가 겪는 대기와 구조적으로 닮았지만 같은 현상은 아닙니다. 결과값은 하드웨어와 부하에 따라 달라지므로 이 글에는 싣지 않으며, 100회 측정에서 p50 대비 p99가 얼마나 벌어지는지를 세 경우에서 비교해 보시기 바랍니다. 나노초 단위로 더 정밀하게 측정하려면 `date +%s%N` 대신 [06장에서 다룬 `clock_gettime(CLOCK_MONOTONIC)`](/post/os-optimization/precise-time-measurement-rdtsc-clock-gettime/) 기반 계측으로 바꾸는 것이 좋습니다.

## 흔한 오개념

<strong>"steal time이 0%면 내 성능 문제는 100% 내 코드 탓이다"</strong>는 절반만 맞습니다. steal time은 하이퍼바이저 스케줄러가 vCPU를 대기시킨 시간만 잡을 뿐, SMT 형제 코어의 캐시·실행 유닛 경합이나 같은 소켓의 다른 테넌트가 유발하는 L3 캐시·메모리 대역폭 경합은 반영하지 않습니다. steal이 0이어도 명령어당 사이클 수(IPC)가 이유 없이 튄다면 이런 "steal에 안 잡히는" 경합을 의심해야 합니다.

<strong>"전용 호스트(Dedicated Host)나 격리 인스턴스를 쓰면 steal time이 완전히 사라진다"</strong>도 과장입니다. 다른 고객과의 경합은 제거되지만, 같은 호스트 위에 내 조직의 다른 VM 여러 개를 올려 두면 그들끼리 경합할 수 있고, [GCP의 sole-tenant 노드는 CPU 오버커밋 설정을 제공](https://docs.cloud.google.com/compute/docs/nodes/sole-tenant-nodes)하므로 설정에 따라 "내 워크로드끼리의" 오버커밋이 여전히 발생할 수 있습니다. 전용 호스트는 **테넌트 간** 경합을 없애는 것이지, 오버커밋이라는 메커니즘 자체를 없애는 것이 아닙니다.

<strong>"steal time 수치는 어느 클라우드에서나 똑같이 신뢰할 수 있다"</strong>는 것도 조심해야 합니다. steal time 계정 방식은 하이퍼바이저 구현에 종속적입니다. [AWS Nitro System](https://aws.amazon.com/ec2/nitro/)처럼 네트워크·스토리지 컨트롤러를 전용 하드웨어 카드로 오프로드하는 구조와 그렇지 않은 구조는 하이퍼바이저가 맡는 일의 범위가 다릅니다. 즉 "이 클라우드는 항상 steal이 낮다/높다"를 다른 클라우드와 절대값으로 직접 비교하는 것은 하이퍼바이저 아키텍처 차이를 무시하는 것입니다.

## 방어 전략: 인스턴스 선택과 전용 호스트

Noisy Neighbor를 완전히 제거할 수는 없지만, 테넌트 간 경합의 **범위**를 좁히는 선택지는 주요 클라우드마다 마련되어 있습니다. 어느 선택지를 쓸지는 격리 강도와 비용·운영 복잡도의 트레이드오프 문제입니다.

| 옵션 | 격리 수준 | 대표 제공사 | 비용·운영 특성 |
|------|---------|-----------|--------------|
| 범용 온디맨드 인스턴스 | 낮음(멀티테넌트 공유) | 각 사업자의 기본 계열 | 비용이 낮은 편이며 사업자가 공개하는 오버커밋 정책은 제한적 |
| 고정 성능·컴퓨팅 최적화 계열 | 중간 | 각 사업자의 고성능 계열 | 일반적으로 변동성이 작다고 알려져 있으나 직접 측정이 필요 |
| [AWS Dedicated Instance/Host](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html) | 높음(물리 서버 단위 전용) | AWS | Host는 소켓·코어 가시성 제공, per-host 과금 |
| [Azure 격리(Isolated) VM 크기](https://learn.microsoft.com/en-us/azure/virtual-machines/isolation) | 높음(물리 서버 단위 전용) | Azure | 비격리 대비 약 10% 프리미엄, 하드웨어 세대에 수명 종속 |
| [GCP Sole-Tenant 노드](https://docs.cloud.google.com/compute/docs/nodes/sole-tenant-nodes) | 높음(물리 서버 단위 전용) | GCP | 자체 CPU 오버커밋 설정 가능, 노드 단위 과금 |

전용 호스트·격리 인스턴스를 도입하기 전에는 앞서의 `steal_monitor`를 배포 환경에 상시 배치해 애플리케이션의 p99 지연 시계열과 나란히 두고, steal time 스파이크와 지연 스파이크가 같은 시각에 겹치는지 확인해야 합니다. 이후의 단계는 아래 판단 기준 표의 첫 행을 따릅니다. 컨테이너·Kubernetes 위에서 이 경합을 완화하는 노드 내부 수단(Static CPU Manager Policy, isolcpus, Intel RDT)은 [11장](/post/os-optimization/container-virtualization-performance-considerations/)에서 다뤘으므로, 그 위에 노드 풀 자체를 전용 호스트로 올릴지 말지가 이 장에서 추가되는 결정입니다.

## 판단 기준

| 상황 | 권장 | 비권장 |
|------|------|--------|
| p99 지연이 간헐적으로 튀고 steal time과 시간대가 겹침 | 인스턴스 타입 변경(고정 성능 계열) 우선 검토 후 전용 호스트 검토 | steal time 확인 없이 애플리케이션 코드만 반복 프로파일링 |
| 규제·컴플라이언스로 물리적 테넌트 분리가 요구됨 | Dedicated Host/Isolated VM/Sole-tenant 노드 | 소프트웨어 격리(cgroup)만으로 대체 시도 |
| 상시 부하가 낮고 가끔 버스트하는 워크로드 | 버스터블 계열 + 크레딧 소진 모니터링 | 버스터블 계열에 상시 높은 부하를 걸어 크레딧 고갈 방치 |
| steal은 낮은데 IPC·지연이 불안정 | SMT 형제 경합·LLC 경합 의심, 코어 배치 재검토([03장](/post/os-optimization/cpu-pinning-affinity-strategy/)) | steal time만 보고 "이웃 문제 아님"으로 단정 |
| 멀티테넌트 K8s 노드 풀 운영 | 신뢰 경계에 따라 노드 풀 분리 + 필요 시 전용 호스트 위에 노드 배치 | 신뢰 불가 배치 워크로드와 지연 민감 워크로드를 같은 노드 풀에 무제한 혼재 |

## 비판적 시각: 한계와 트레이드오프

전용 호스트·격리 인스턴스가 만능 해법은 아닙니다. 비용 프리미엄이 뒤따르고(표의 Azure 격리 VM 예시처럼), Dedicated Host는 소켓·코어 단위로 통째로 구매해야 하므로 활용률이 낮은 워크로드에는 오히려 비효율적입니다. 더 근본적인 한계는 앞의 오개념에서 본 대로 steal time이 CPU 스케줄링 대기라는 한 가지 차원만 보여준다는 점이므로, steal time이 정상이라는 이유만으로 이웃 문제가 없다고 결론짓지 않아야 합니다.

또한 Noisy Neighbor로 인한 꼬리 지연 저하가 계약상 보상 대상인지는 사업자별 SLA 문서를 직접 확인해야 하며, 방어는 기본적으로 이용자의 운영 책임으로 두고 설계하는 것이 안전합니다. 마지막으로, 로컬에서 재현하는 경합 실험은 실제 이웃 테넌트의 부하 패턴을 통제할 수 없다는 근본적 한계가 있습니다 — 이 장에서 다룬 재현 스크립트는 메커니즘을 이해하고 모니터링 코드를 검증하는 용도로는 유효하지만, 특정 클라우드·특정 시점의 실제 steal time 수준을 예측하는 도구는 아닙니다.

## 마무리

- CPU Steal Time이 하이퍼바이저 스케줄링 대기를 측정하는 지표이며, `/proc/stat`의 steal 필드에서 계산되는 원리를 설명할 수 있다.
- 오버커밋·버스터블 크레딧·SMT 형제 경합이 각각 어떻게 Noisy Neighbor를 만드는지 구분할 수 있다.
- steal time이 낮아도 캐시·메모리 대역폭·네트워크 경합은 별도로 존재할 수 있다는 점을 설명할 수 있다.
- 인스턴스 타입 변경과 전용 호스트/격리 인스턴스/sole-tenant 노드 중 상황에 맞는 방어 전략을 선택할 수 있다.
- 전용 호스트가 테넌트 간 경합만 제거할 뿐 오버커밋 메커니즘 자체를 없애지 않는다는 한계를 판단할 수 있다.

이 장으로 [OS·런타임 Low-latency 운영환경 트랙](/post/os-optimization/getting-started-os-runtime-performance-tuning/)의 18개 챕터가 마무리됩니다. 파일·블록 I/O 경로의 병목이 남아 있다면 **Tr.09 I/O 최적화**로, 패킷·프로토콜 경로가 문제라면 **Tr.10 네트워크 최적화**로 이어 가고, 이 트랙 전체를 다른 11개 트랙과 함께 어떤 순서로 읽을지는 [Low-latency 최적화 시리즈 개요](/post/low-latency-optimization-series/getting-started-low-latency-optimization-series-overview/)에서 확인할 수 있습니다. 클라우드·컨테이너 경계의 보안·성능 트레이드오프를 더 깊이 보고 싶다면 이미 게시된 [17장: eBPF·커널 경계와 성능 안전](/post/os-optimization/ebpf-xdp-kernel-boundary-performance-safety-expert/)이 이어서 읽기 좋은 주제입니다.
