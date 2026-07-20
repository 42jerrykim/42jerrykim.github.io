---
collection_order: 12
date: 2026-07-13
lastmod: 2026-07-13
draft: false
image: wordcloud.png
title: "[OS 06] IRQ 최적화"
slug: irq-interrupt-optimization
description: "인터럽트 처리의 top half/bottom half 구조, softirq·NAPI·threaded IRQ 메커니즘을 설명하고, IRQ affinity·irqbalance·managed_irq로 저지연 워크로드의 격리 코어에서 인터럽트를 배제하는 실전 전략을 정리합니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - OS(운영체제)
  - Linux(리눅스)
  - Kernel
  - CPU(Central Processing Unit)
  - Memory(메모리)
  - Concurrency(동시성)
  - C
  - C++
  - Networking(네트워킹)
  - IO(Input/Output)
  - Benchmark
  - Latency
  - Throughput
  - Profiling(프로파일링)
  - Best-Practices
  - System-Design
  - Advanced
  - Deep-Dive
  - Hardware(하드웨어)
  - Edge-Cases(엣지케이스)
  - Pitfalls(함정)
  - Guide(가이드)
  - Reference(참고)
  - IRQ
  - Top-Half
  - Bottom-Half
  - Softirq
  - Threaded-IRQ
  - NAPI
  - irqbalance
  - IRQ-Affinity
  - managed_irq
  - isolcpus
---

**IRQ 최적화**란 하드웨어 인터럽트가 CPU 코어를 선점하는 시점·빈도·대상 코어를 통제해, 저지연 워크로드가 예측 가능한 실행 시간을 확보하도록 만드는 일련의 기법을 말한다. [CPU Pinning/Affinity 전략](/post/os-optimization/cpu-pinning-affinity-strategy/)(3장)에서 스레드를 특정 코어에 고정해도, 그 코어에 네트워크 카드나 디스크 컨트롤러의 인터럽트가 계속 떨어진다면 고정의 의미는 절반만 남는다. 인터럽트는 스케줄러의 개입 없이 CPU를 즉시 가로채는 하드웨어 이벤트이므로, 아무리 스레드를 잘 배치해도 인터럽트 핸들러가 몇 마이크로초씩 코어를 뺏어가면 꼬리 지연(tail latency)에 스파이크가 남는다. 이 장은 인터럽트가 top half와 bottom half로 나뉘어 처리되는 구조를 먼저 설명하고, `smp_affinity`로 인터럽트를 특정 코어에 묶는 방법과 irqbalance가 그 배치를 자동으로 흔드는 이유, 그리고 격리 코어에서 인터럽트를 최대한 배제하는 실전 절차를 정리한다.

## 이 장을 읽기 전에

**선행 장**: [CPU Pinning/Affinity 전략](/post/os-optimization/cpu-pinning-affinity-strategy/)(3장)에서 `isolcpus`·`nohz_full`·`cpuset`으로 코어를 격리하는 방법을, [Context Switch 비용 분석과 회피](/post/os-optimization/context-switch-cost-avoidance/)(1장)에서 스케줄러가 개입하는 비용의 구조를 다뤘다. 이 장은 그 위에서 "스케줄러가 아니라 하드웨어 인터럽트 자체가 코어를 뺏는 경우"를 다룬다.

**전제 지식**: 논리 CPU와 코어의 구분, `taskset`/`sched_setaffinity`로 스레드를 코어에 고정하는 절차, `isolcpus`가 스케줄러 도메인에서 코어를 빼는 방식만 알면 충분하다.

**이 장의 깊이**: **심화**. top half/bottom half의 내부 동작, softirq·threaded IRQ의 커널 구현 원리, `/proc/irq/N/smp_affinity`·`managed_irq`로 인터럽트를 특정 코어에서 배제하는 절차, 그리고 irqbalance와 수동 설정이 충돌하는 지점까지 다룬다.

**다루지 않는 것**: NAPI를 활용한 네트워크 패킷 처리 파이프라인 심화와 XDP의 조기 처리 경로는 [09장: XDP/eBPF 개요](/post/os-optimization/xdp-ebpf-overview-fundamentals/)와 아직 집필되지 않은 Tr.10(네트워크 최적화)의 몫이며, io_uring이 NAPI busy-poll을 등록하는 구체적 API는 [08장: io_uring 개요](/post/os-optimization/io-uring-overview-fundamentals/)에서 다룬다. `cpuset` cgroup의 계층 구조와 리소스 제어 자체는 [13장: cgroups v2 리소스 제어](/post/os-optimization/cgroups-v2-resource-control-performance/)로, 컨테이너 환경에서 호스트 IRQ가 게스트에 어떻게(또는 어떻게 안) 보이는지는 [11장: 컨테이너/가상화 성능 고려사항](/post/os-optimization/container-virtualization-performance-considerations/)으로 위임한다. NUMA 노드와 디바이스의 물리적 배치 관계는 [04장: NUMA CPU Affinity·스레드 배치](/post/os-optimization/numa-cpu-affinity-thread-placement/)를 참고한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **중급자** | "인터럽트 처리 구조의 역사와 배경" ~ "Bottom Half의 세 가지 구현" | top half/bottom half가 왜 분리되어 있고 무엇을 나눠 맡는지 이해 |
| **심화 학습자** | "IRQ Affinity" ~ "irqbalance와 저지연 격리 전략" | smp_affinity·managed_irq·irqbalance를 조합해 격리 코어에서 인터럽트를 배제하는 절차 습득 |
| **전문가** | "판단 기준" ~ "비판적 시각" | managed_irq의 best-effort 한계와 완전한 격리가 불가능한 상황을 판단 |

---

## 인터럽트 처리 구조의 역사와 배경

인터럽트를 즉시 처리할 부분과 나중으로 미룰 부분으로 나누는 아이디어 자체는 유닉스 계열 커널의 오래된 설계 원칙이다. 하드웨어가 인터럽트를 걸면 CPU는 인터럽트가 비활성화된 상태로 최소한의 확인 작업만 수행하고, 나머지 무거운 처리는 인터럽트가 다시 켜진 뒤로 미루는 구조가 다양한 이름(top half/bottom half, hardirq/softirq)으로 반복해서 채택되어 왔다. 리눅스에서 이 분리를 구체화한 두 축은 각기 다른 시기에 다른 문제를 풀기 위해 등장했다. **softirq**(그리고 그 위에 얹힌 tasklet)는 초기 리눅스 SMP 지원 시절부터 존재해 왔고, 하드웨어 인터럽트 컨텍스트를 최소화하면서도 여러 CPU가 동시에 후속 처리를 나눠 맡을 수 있게 했다. <strong>NAPI(New API)</strong>는 2001년 Jamal Hadi Salim, Robert Olsson, Alexey Kuznetsov가 발표한 ["Beyond Softnet"](https://www.usenix.org/legacy/publications/library/proceedings/als01/full_papers/jamal/jamal.pdf) 논문에서 제안된 네트워크 수신 경로 개선안으로, 트래픽이 몰릴 때 패킷마다 인터럽트를 걸어 CPU를 마비시키는 대신 인터럽트를 잠시 끄고 폴링으로 전환해 처리량을 지키는 절충안을 표준화했다. **threaded IRQ**는 이보다 늦게, Thomas Gleixner가 PREEMPT_RT 패치 세트에서 오래 유지해 오던 기법을 2009년 **Linux 2.6.30**에 `request_threaded_irq()` API로 메인라인에 병합하면서 일반 커널의 정식 기능이 되었다([LWN: Moving interrupts to threads](https://lwn.net/Articles/302043/)). 이 세 가지는 "인터럽트 컨텍스트에서 얼마나 오래 머물 것인가"라는 같은 질문에 대한 서로 다른 시대의 답이며, 오늘날 커널은 세 메커니즘을 상황에 따라 함께 쓴다.

## Top Half와 Bottom Half: 인터럽트 처리의 두 층

**top half**(하드웨어 인터럽트 핸들러, hardirq)는 인터럽트가 발생한 순간 실행되는 코드로, 인터럽트 컨텍스트에서 돌기 때문에 다른 인터럽트를 막은 채(또는 우선순위가 더 높은 인터럽트만 허용한 채) 실행된다. 이 컨텍스트는 잠들 수 없고(mutex를 잡을 수 없고), 가능한 한 짧아야 한다는 제약이 있다 — 하드웨어에게 "인터럽트를 받았다"는 사실을 확인(acknowledge)하고, 레지스터에서 최소한의 정보(어떤 디바이스인지, DMA가 끝났는지)만 읽어 낸 뒤, 나머지 처리를 뒤로 미루는 요청을 남기고 즉시 반환하는 것이 이상적인 top half다. **bottom half**는 이 미뤄진 처리를 더 관대한 컨텍스트에서 수행하는 부분으로, 인터럽트가 다시 켜진 상태이거나 아예 프로세스 컨텍스트에서 실행되므로 더 오래 걸리는 작업(패킷 파싱, 버퍼 복사, 락 획득)을 안전하게 수행할 수 있다.

```mermaid
flowchart LR
  hw["하드웨어 인터럽트</br>(NIC·디스크·타이머)"] --> topHalf["Top Half</br>(hardirq, IRQ 비활성)"]
  topHalf -->|"ack + 최소 확인"| defer{"후속 처리 필요?"}
  defer -->|"raise_softirq"| softirqQ["Softirq 큐"]
  defer -->|"wake_up_process"| irqThread["Threaded IRQ</br>(커널 스레드)"]
  softirqQ --> bottomHalf["Bottom Half</br>(softirq/NAPI poll, 프로세스 컨텍스트 유사)"]
  irqThread --> bottomHalf
  bottomHalf --> done["패킷/블록 I/O 완료 처리"]
```

이 분리가 필요한 이유는 인터럽트 컨텍스트가 자원을 다루는 방식에 근본적인 제약이 있기 때문이다. hardirq 안에서 슬립하거나 페이지 폴트를 유발하면 커널 전체가 그 코어에서 멈춘 채 데드락에 가까운 상태에 빠질 수 있으므로, top half는 "인터럽트가 왔다"는 사실만 최대한 빨리 인정하고 실제 데이터 처리는 bottom half로 넘겨야 한다. 저지연 워크로드 관점에서 이 구조가 문제가 되는 지점은, top half가 아무리 짧아도 인터럽트 발생 자체가 지연 민감 스레드의 실행을 강제로 끊는다는 사실은 변하지 않는다는 것이다. bottom half를 어디서(어떤 CPU에서, 어떤 컨텍스트에서) 실행할지를 통제하는 것이 이 장 뒷부분의 IRQ affinity 논의로 이어진다.

## Bottom Half의 세 가지 구현: Softirq·Tasklet·Threaded IRQ

리눅스 커널은 bottom half를 구현하는 세 가지 메커니즘을 제공하며, 이들은 서로 대체재라기보다 다른 트레이드오프를 가진 계층이다.

**softirq**는 커널이 부팅 시 정적으로 등록하는 고정된 개수(현재 10종: `HI`, `TIMER`, `NET_TX`, `NET_RX`, `BLOCK`, `IRQ_POLL`, `TASKLET`, `SCHED`, `HRTIMER`, `RCU`)의 지연 실행 슬롯이다. hardirq보다는 관대해 인터럽트가 켜진 채로 실행되지만, 여전히 선점 불가능한 컨텍스트라 같은 CPU의 다른 softirq를 끼어들게 하지 못하고, 잠들 수도 없다. 네트워크 수신(`NET_RX_SOFTIRQ`)과 블록 I/O 완료 처리가 이 경로를 쓰는 대표적인 사용자다. **tasklet**은 softirq 위에 만들어진 상위 계층으로, 커널 모듈이나 드라이버가 런타임에 동적으로 등록할 수 있다는 점이 다르다 — 같은 종류의 softirq(`TASKLET`)를 공유하지만, 같은 tasklet은 여러 CPU에서 동시에 실행되지 않도록 보장된다는 제약이 softirq와 다르다. **threaded IRQ**는 앞서 역사 절에서 다룬 대로 인터럽트 처리를 아예 스케줄 가능한 커널 스레드로 옮긴 것으로, 드라이버가 `request_threaded_irq()`를 호출하면 빠른 확인만 담당하는 primary handler와 실제 처리를 담당하는 스레드 핸들러를 분리해 등록할 수 있다.

```c
// 예시: 드라이버가 threaded IRQ를 등록하는 골격 (리눅스 커널 모듈 코드)
// 이 코드는 사용자 공간 컴파일러가 아니라 커널 소스 트리의 Kbuild로 빌드해야 하며,
// 여기서는 top half/bottom half 분리가 API 수준에서 어떻게 드러나는지만 보여준다.
#include <linux/interrupt.h>

// primary handler: hardirq 컨텍스트, 인터럽트가 이 디바이스의 것인지만 빠르게 확인
static irqreturn_t dev_irq_quick_check(int irq, void *dev_id) {
  if (!device_has_pending_data(dev_id))
    return IRQ_NONE;       // 이 디바이스의 인터럽트가 아님
  return IRQ_WAKE_THREAD;  // 스레드 핸들러를 깨워 처리를 위임
}

// thread handler: 커널 스레드(프로세스 컨텍스트), 잠들거나 락을 잡을 수 있음
static irqreturn_t dev_irq_thread_fn(int irq, void *dev_id) {
  process_device_data(dev_id);  // 오래 걸릴 수 있는 실제 처리
  return IRQ_HANDLED;
}

static int dev_probe_register_irq(struct my_device *dev) {
  return request_threaded_irq(dev->irq, dev_irq_quick_check, dev_irq_thread_fn,
                               IRQF_ONESHOT, "my_device", dev);
}
```

threaded IRQ의 실질적 이점은 커널 스레드가 되는 순간 그 실행이 **일반 스케줄러의 관리 대상**이 된다는 것이다 — 우선순위를 매길 수 있고(`chrt`로 조정 가능), 특정 코어에 고정할 수 있고(스레드이므로 `taskset`/`sched_setaffinity`가 그대로 적용된다), 다른 스레드처럼 선점될 수 있다. 이 성질 때문에 **PREEMPT_RT** 커널은 `IRQF_NO_THREAD`·`IRQF_PERCPU`·`IRQF_ONESHOT` 플래그가 붙은 예외를 빼고 사실상 모든 인터럽트 핸들러를 강제로 스레드화하며, IRQ 스레드는 기본적으로 `SCHED_FIFO` 우선순위 50으로 실행된다. 반대로 일반(비-RT) 커널에서는 `threadirqs` 부팅 파라미터를 명시적으로 켜야 이 강제 스레드화가 적용된다. 이 차이는 왜 PREEMPT_RT 환경에서 IRQ affinity 설정이 "인터럽트 자체"뿐 아니라 "그 인터럽트를 처리하는 커널 스레드"까지 함께 겨냥해야 하는지를 설명한다.

## IRQ Affinity: smp_affinity와 managed_irq

**IRQ affinity**는 특정 인터럽트 소스가 어떤 논리 CPU에서 top half(그리고 연쇄적으로 bottom half의 상당 부분)를 실행할지를 지정하는 설정이다. 이 값은 `/proc/irq/<IRQ번호>/smp_affinity`(16진수 비트마스크)나 커널 3.0부터 지원되는 더 읽기 쉬운 `/proc/irq/<IRQ번호>/smp_affinity_list`(CPU 범위 목록)로 조회·수정한다. 리눅스 커널 문서는 이 파일들이 "주어진 인터럽트 소스에 허용되는 대상 CPU"를 지정하며, 마스크에서 모든 CPU를 끄는 것은 허용되지 않는다고 명시한다([kernel docs: SMP IRQ affinity](https://docs.kernel.org/core-api/irq/irq-affinity.html)). 새로 등록되는(아직 활성화되지 않은) 인터럽트는 `/proc/irq/default_smp_affinity`에 지정된 기본 마스크를 물려받으므로, 저지연 서버라면 이 기본값 자체를 housekeeping 코어로 좁혀 두는 것이 새 디바이스가 격리 코어로 흘러드는 사고를 줄인다.

```bash
# 현재 시스템의 인터럽트 목록과 CPU별 누적 횟수 확인
cat /proc/interrupts

# 예: NIC 큐 하나(IRQ 128)를 housekeeping 코어(0,1)로만 제한
echo 0-1 > /proc/irq/128/smp_affinity_list

# 부팅 이후 새로 등록되는 인터럽트의 기본 허용 범위를 housekeeping 코어로 좁힘
echo 0-1 > /proc/irq/default_smp_affinity
```

`cat /proc/interrupts`의 출력은 각 행이 하나의 인터럽트 소스이고 각 열이 코어별 누적 발생 횟수라는 간단한 ASCII 표 형식이며, 열이 CPU 개수만큼 이어진 뒤 인터럽트 컨트롤러 종류와 디바이스 이름이 붙는다([man7.org: proc_interrupts(5)](https://man7.org/linux/man-pages/man5/proc_interrupts.5.html)). 격리 코어에 인터럽트가 새는지 확인하는 가장 직접적인 방법은 이 파일을 두 시점에서 스냅숏으로 떠 차분(diff)을 보는 것이다.

```bash
#!/usr/bin/env bash
# irq_leak_check.sh — 지정한 격리 코어 열의 인터럽트 카운터가 구간 동안 증가했는지 확인
# 사용: ./irq_leak_check.sh <감시할 CPU 컬럼 번호, 0-base> <측정 구간(초)>
set -euo pipefail
cpu_col=$(( $1 + 2 ))   # /proc/interrupts는 1열이 IRQ 번호, 2열부터 CPU0
duration=$2

before=$(awk -v c="$cpu_col" 'NR>1 {sum+=$c} END{print sum+0}' /proc/interrupts)
sleep "$duration"
after=$(awk -v c="$cpu_col" 'NR>1 {sum+=$c} END{print sum+0}' /proc/interrupts)

echo "CPU$1: ${duration}초간 인터럽트 증가량 = $(( after - before ))"
```

이 스크립트는 CPU 열 하나의 총합만 비교하므로 어떤 IRQ가 새는지까지는 알려주지 못한다 — 특정 IRQ를 의심한다면 `awk 'NR==1 || $1 ~ /^128:/' /proc/interrupts`처럼 해당 행만 반복 관찰하는 편이 원인 추적에 더 유용하다.

`smp_affinity`로 모든 인터럽트가 통제되는 것은 아니다. 멀티 큐 디바이스(다중 NIC 큐, NVMe 큐)의 인터럽트는 블록/네트워크 서브시스템이 큐 개수만큼 자동으로 할당하고 관리하는 **managed interrupt**로 취급되며, 이 경우 `/proc/irq/N/smp_affinity`에 값을 써도 커널이 그 값을 무시하고 자체 판단을 우선한다. 커널 문서는 이런 인터럽트를 격리 코어에서 배제하는 전용 경로로 `isolcpus=` 부팅 파라미터의 **`managed_irq`** 서브 플래그를 제공하며, "관리형 인터럽트가 회피해야 할 CPU 마스크를 지정하는 best-effort 기능"이라고 규정한다. 다만 이 회피는 "자동 할당된 인터럽트 마스크에 회피 대상 바깥의 온라인 CPU가 남아 있을 때만" 적용되고, 요청된 마스크가 격리 코어만으로 이루어져 있다면 회피는 아무 효과가 없다([kernel docs: Affinity managed interrupts](https://docs.kernel.org/core-api/irq/managed_irq.html)). 즉 코어 수가 극단적으로 적어 housekeeping 코어가 부족한 시스템에서는 managed_irq 회피 자체가 무력화될 수 있다는 뜻이며, 이는 뒤에서 다룰 비판적 시각의 핵심 근거이기도 하다.

## irqbalance와 저지연 격리 전략

**irqbalance**는 시스템의 인터럽트를 여러 CPU에 자동으로 분산시켜 특정 코어 하나가 인터럽트 처리로 과부하되는 것을 막는 사용자 공간 데몬이다. 일반적인 범용 서버에서는 이 자동 분산이 바람직하지만, 저지연 워크로드의 격리 코어 관점에서는 정반대의 문제를 일으킨다 — irqbalance는 "인터럽트를 고르게 나눈다"는 목표를 위해 주기적으로 `smp_affinity`를 재계산하고 재기록하므로, 관리자가 수동으로 IRQ를 housekeeping 코어에 고정해도 irqbalance가 그 설정을 되돌려 격리 코어로 다시 흘려보낼 수 있다. 이 충돌을 막는 실전 절차는 세 단계로 요약된다.

첫째, irqbalance 자체를 끄거나(`systemctl stop irqbalance && systemctl disable irqbalance`) 켜 두더라도 특정 CPU를 배분 대상에서 빼도록 설정한다. 두 번째 방법은 `/etc/sysconfig/irqbalance`(또는 배포판에 따라 `/etc/default/irqbalance`)의 `IRQBALANCE_BANNED_CPUS`(16진수 비트마스크) 또는 `IRQBALANCE_BANNED_CPULIST`(CPU 범위) 값을 지정해 격리 코어를 재분배 대상에서 명시적으로 제외하는 것이다. 최신 배포판의 irqbalance는 이 값이 비어 있어도 `isolcpus`로 지정된 코어를 자동으로 감지해 배분 대상에서 제외하는 경우가 많지만, 이 자동 감지에 전적으로 의존하기보다 명시적으로 값을 지정해 검증하는 편이 안전하다.

```bash
# /etc/sysconfig/irqbalance (RHEL 계열) 또는 /etc/default/irqbalance (Debian 계열)
# CPU 2,3을 irqbalance의 재분배 대상에서 제외 (격리 코어로 가정)
IRQBALANCE_BANNED_CPULIST=2-3
```

둘째, 격리 코어에 이미 고정된 인터럽트가 있다면 `--banirq` 옵션이나 설정 파일로 해당 IRQ 번호 자체를 irqbalance의 관리 목록에서 빼, 관리자가 수동으로 써 둔 `smp_affinity` 값을 irqbalance가 건드리지 못하게 한다. 셋째, managed IRQ 디바이스(NVMe, 멀티 큐 NIC)는 앞 절에서 설명한 대로 `smp_affinity` 자체가 커널에 의해 무시될 수 있으므로, 부팅 파라미터에 `isolcpus=domain,managed_irq,nohz_full,<격리코어목록>`처럼 `managed_irq` 서브 플래그를 함께 넣어 커널 수준에서 회피를 시도해야 한다. 이 세 단계를 모두 거쳐도 앞 절에서 언급한 best-effort 한계 때문에 완전한 배제가 보장되지는 않으므로, 배치 후에는 반드시 `irq_leak_check.sh` 같은 도구로 격리 코어의 인터럽트 카운터가 실제로 정체되어 있는지 확인해야 한다.

## 흔한 오개념

<strong>"isolcpus로 코어를 격리하면 그 코어에는 인터럽트도 자동으로 안 온다"</strong>는 정확하지 않다. `isolcpus`(domain 플래그)는 일반 스케줄러의 부하 분산 대상에서 코어를 빼는 것이지, 인터럽트 라우팅을 바꾸는 기능이 아니다. 인터럽트가 격리 코어를 피하게 하려면 `smp_affinity`를 별도로 설정하거나 `managed_irq` 서브 플래그를 함께 지정해야 하며, 이 둘을 빠뜨리면 스케줄러 격리는 성공했는데 인터럽트만 여전히 격리 코어를 때리는 상황이 벌어진다.

<strong>"managed_irq를 켜면 관리형 인터럽트가 격리 코어에서 완전히 빠진다"</strong>도 과장이다. 커널 문서가 명시하듯 이는 best-effort 기능이라 자동 할당 마스크에 격리 코어 바깥의 온라인 CPU가 남아 있을 때만 작동하며, housekeeping 코어가 너무 적거나 없으면 이 회피 자체가 무력화된다. "설정했으니 안전하다"고 가정하지 말고 실측으로 검증해야 한다.

<strong>"irqbalance를 끄기만 하면 인터럽트 배치가 고정된다"</strong>도 절반만 맞다. irqbalance를 멈춰도 새로 핫플러그되는 디바이스나 새 인터럽트는 `default_smp_affinity`를 물려받으므로, 이 기본값이 격리 코어를 포함하고 있다면 irqbalance 없이도 새 인터럽트가 격리 코어로 들어올 수 있다. `default_smp_affinity` 자체를 housekeeping 코어로 좁혀야 이 구멍이 막힌다.

## 판단 기준

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 특정 인터럽트를 특정 코어에 고정 | `/proc/irq/N/smp_affinity_list`로 명시적 지정 | 커널·irqbalance의 기본 배치에 의존 |
| 저지연 격리 코어에서 인터럽트를 최대한 배제 | `isolcpus=domain,managed_irq,nohz_full,...` + irqbalance 배제 + 수동 affinity | isolcpus만 설정하고 인터럽트는 방치 |
| 멀티 큐 NIC/NVMe(managed IRQ) 디바이스 | `managed_irq` 서브 플래그 + housekeeping 코어를 충분히 확보 | smp_affinity로 직접 제어 가능하다고 가정 |
| 범용 서버, 코어별 부하가 들쭉날쭉 | irqbalance 활성 상태 유지 | 이유 없이 irqbalance 전면 비활성화 |
| 인터럽트 처리 로직에서 락 대기·긴 계산이 필요 | threaded IRQ(`request_threaded_irq`)로 분리 | hardirq/softirq 컨텍스트에서 무거운 작업 수행 |
| 격리 설정 후 실제 효과 확인 | `/proc/interrupts` 스냅숏 diff로 정기 검증 | 설정 직후 한 번만 확인하고 방치 |

## 비판적 시각: 한계와 트레이드오프

IRQ affinity와 격리는 **완결된 보장이 아니라 best-effort 완화책**이라는 점을 반복해서 짚어야 한다. `managed_irq`는 커널 문서 스스로가 "회피를 시도한다"고만 표현할 뿐 보장한다고 말하지 않으며, housekeeping 코어가 부족한 소형 시스템(예: 4~8코어 임베디드 어플라이언스)에서는 이 회피가 사실상 작동하지 않을 수 있다. 이런 환경에서는 격리 코어 개수 자체를 줄여서라도 housekeeping 여유를 확보하는 재설계가, 설정 플래그를 아무리 정교하게 조합하는 것보다 나은 선택일 수 있다.

irqbalance를 완전히 꺼 버리는 흔한 처방도 공짜가 아니다. irqbalance는 범용 워크로드에서 코어 간 인터럽트 부하를 자동으로 고르게 만드는 실질적인 이점을 제공하므로, 저지연 격리 코어만 배제하고 나머지 housekeeping 코어에서는 계속 동작하도록 `IRQBALANCE_BANNED_CPULIST`로 범위를 좁히는 편이, 데몬 자체를 끄고 모든 인터럽트를 수동으로 영구히 관리하는 것보다 운영 부담이 작은 경우가 많다. 반대로 인터럽트 패턴이 정적이고 예측 가능한 전용 어플라이언스라면 irqbalance를 아예 배제하고 정적 설정으로 고정하는 편이 재현성 면에서 유리할 수 있다 — 정답은 워크로드의 안정성에 달려 있다.

threaded IRQ로 처리를 스레드화하면 지연 민감 워크로드와 같은 자원(코어, 우선순위 예산)을 두고 IRQ 스레드가 경쟁하게 된다는 점도 트레이드오프다. PREEMPT_RT의 기본 `SCHED_FIFO` 50 우선순위는 일반적인 애플리케이션 스레드보다 높게 설정되어 있어, IRQ 스레드가 저지연 워커보다 먼저 스케줄될 수 있다. 이 우선순위를 낮추면 인터럽트 처리 자체가 지연되어 다른 형태의 지연 스파이크(예: 네트워크 버퍼 드롭)로 이어질 수 있으므로, IRQ 스레드 우선순위 조정은 "인터럽트 지연"과 "애플리케이션 스레드 지연" 사이의 저울질이지 일방적인 개선이 아니다. 마지막으로, 컨테이너·가상화 환경에서는 게스트가 호스트의 실제 IRQ 토폴로지를 보지 못하는 경우가 흔해 이 장의 기법 상당수가 그대로 적용되지 않으며, 이 문제는 [11장](/post/os-optimization/container-virtualization-performance-considerations/)에서 별도로 다룬다.

## 마무리

이 장을 읽은 뒤 다음을 스스로 점검할 수 있어야 한다.

- [ ] top half(hardirq)와 bottom half(softirq/threaded IRQ)가 각각 어떤 컨텍스트 제약을 받는지 설명할 수 있다.
- [ ] softirq·tasklet·threaded IRQ 세 가지 bottom half 구현의 차이(정적/동적 등록, 동시 실행 제약, 스케줄러 관리 여부)를 구분할 수 있다.
- [ ] `/proc/irq/N/smp_affinity`(_list)와 `/proc/irq/default_smp_affinity`의 관계를 설명하고, 격리 코어에서 인터럽트를 배제하도록 설정할 수 있다.
- [ ] managed IRQ(멀티 큐 NIC/NVMe)가 `smp_affinity` 수동 설정을 무시할 수 있고, `managed_irq` 회피도 best-effort라는 한계를 안다.
- [ ] irqbalance가 저지연 격리 코어와 충돌하는 이유와, 전면 비활성화 대신 대상 코어만 배제하는 대안을 판단할 수 있다.
- [ ] `/proc/interrupts` 스냅숏 diff로 격리 설정이 실제로 작동하는지 검증하는 절차를 실행할 수 있다.

**다음 장에서는** 이렇게 IRQ와 스레드를 코어에 배치한 뒤 그 배치를 강제하고 리소스를 제어하는 계층인 **cgroups v2**를 다룬다. `cpuset` 파티션이 이 장에서 다룬 격리 코어 목록을 어떻게 정적 `isolcpus` 부팅 파라미터 없이도 런타임에 재구성 가능하게 만드는지, 그리고 CPU·메모리 대역폭 제어가 지연 분포에 미치는 영향을 이어서 살펴본다.

→ [cgroups v2 리소스 제어](/post/os-optimization/cgroups-v2-resource-control-performance/)
