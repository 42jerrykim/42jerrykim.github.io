---
collection_order: 10
date: 2026-07-13
lastmod: 2026-07-13
draft: false
image: wordcloud.png
title: "[CPU 06] 추측 실행과 보안 영향"
slug: speculative-execution-security-impact
description: "추측 실행이 Spectre·Meltdown 계열 사이드채널로 이어지는 메커니즘을 설명하고, retpoline·IBRS/eIBRS·KPTI 완화 기법의 실측 성능 비용과 VMScape·Branch Privilege Injection 등 2024~2025년 신규 변종의 교훈을 정리합니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - CPU(Central Processing Unit)
  - Cache
  - Memory(메모리)
  - Assembly
  - Compiler(컴파일러)
  - Hardware(하드웨어)
  - Benchmark
  - Latency
  - Throughput
  - Profiling(프로파일링)
  - Security(보안)
  - OS(운영체제)
  - Linux(리눅스)
  - Windows(윈도우)
  - Advanced
  - Deep-Dive
  - Case-Study
  - Technology(기술)
  - Reference(참고)
  - Comparison(비교)
  - Edge-Cases(엣지케이스)
  - Pitfalls(함정)
  - Documentation(문서화)
  - Spectre
  - Meltdown
  - Speculative-Execution
  - Transient-Execution
  - Retpoline
  - KPTI
  - IBRS
  - Side-Channel
  - Branch-Target-Injection
  - VMScape
---

**추측 실행(speculative execution)**이란 CPU가 분기·메모리 접근 결과가 아직 확정되지 않은 시점에, 그 결과를 미리 예측해 뒤따르는 명령어를 미리 실행해 두는 하드웨어 기법입니다. [01장](/post/cpu-optimization/cpu-pipeline-fundamentals/)에서 다룬 파이프라이닝과 [06장](/post/cpu-optimization/out-of-order-execution-performance/)에서 다룬 Out-of-Order 실행 모두 이 추측에 의존해야 파이프라인을 계속 채울 수 있습니다. 문제는 예측이 틀렸을 때 CPU가 레지스터와 메모리 같은 **아키텍처 상태(architectural state)**는 깨끗이 되돌리지만, 캐시 점유·분기 예측기 히스토리 같은 **마이크로아키텍처 상태(microarchitectural state)**는 되돌리지 않는다는 데 있습니다. 2018년 초 공개된 Spectre와 Meltdown은 바로 이 틈을 이용해, 소프트웨어 관점에서는 "실행된 적 없는" 명령어가 남긴 캐시 흔적만으로 임의의 메모리를 읽어낼 수 있음을 보였습니다. 이 장에서는 추측 실행이 어떻게 사이드채널로 이어지는지, Spectre/Meltdown 계열 취약점이 어떤 계보로 진화해 왔는지, 그리고 retpoline·IBRS·KPTI 같은 완화 기법이 지연시간 예산에 실제로 얼마를 청구하는지를 다룹니다.

## 이 장을 읽기 전에

이 장은 [02장: 분기 예측 메커니즘과 비용](/post/cpu-optimization/branch-prediction-mechanisms-cost/)에서 다룬 BTB(Branch Target Buffer)·예측 실패 시 파이프라인 플러시 개념과, [06장: Out-of-Order 실행과 성능](/post/cpu-optimization/out-of-order-execution-performance/)에서 다룬 "실행은 추측적, 폐기(retire)는 순서대로"라는 원칙을 전제로 합니다. 두 장의 핵심만 요약하면, CPU는 아직 확정되지 않은 분기·주소를 추측해 명령을 앞당겨 실행하고, 추측이 틀리면 그 결과를 조용히 버립니다.

**이 장의 깊이**: 이 장은 **심화**입니다. 추측 실행이 왜 사이드채널이 되는지의 원리, Spectre v1/v2·Meltdown의 메커니즘 차이, retpoline·IBRS/eIBRS·STIBP·IBPB·KPTI 같은 완화 기법과 그 성능 비용, 그리고 2024~2025년에 새로 드러난 변종(GhostRace, Indirector, VMScape, Branch Privilege Injection)까지 다룹니다. **다루지 않는 것**: BTB 내부 구조와 일반 분기 예측 비용은 [02장](/post/cpu-optimization/branch-prediction-mechanisms-cost/), ROB·reservation station의 내부 동작은 [06장](/post/cpu-optimization/out-of-order-execution-performance/), 캐시 계층의 지연시간 자체는 [03장](/post/cpu-optimization/cache-hierarchy-l1-l2-l3/), TopDown에서 Bad Speculation을 Frontend/Backend Bound와 구분하는 방법은 [17장](/post/cpu-optimization/frontend-backend-bound-topdown-basics/), Apple Silicon M시리즈의 전반적인 마이크로아키텍처는 [13장](/post/cpu-optimization/apple-silicon-m-series-architecture/)에서 각각 다루므로 이 장에서는 반복하지 않습니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "추측 실행이 보안 문제가 된 배경" ~ "추측 실행이 비밀을 새어나가게 하는 메커니즘" | Spectre/Meltdown이 왜 가능한지 기본 원리 이해 |
| **중급자** | "흔한 오개념" ~ "완화 기법과 성능 비용" | 각 완화 기법이 막는 대상과 실제 비용 이해 |
| **전문가** | "판단 기준" ~ "비판적 시각" | 워크로드·신뢰 경계에 따라 완화 수준을 직접 선택 |

---

## 추측 실행이 보안 문제가 된 배경

2018년 1월 3일, 원래 예정보다 며칠 앞당겨 Spectre와 Meltdown이 공개되었습니다. Google Project Zero의 Jann Horn이 독립적으로 두 취약점 계열을 모두 발견했고, 거의 동시에 Graz 공과대학의 Moritz Lipp 등이 Meltdown을, Paul Kocher가 이끈 다국적 학계·산업 공동 연구팀이 Spectre를 각각 논문으로 정리해 발표했습니다. 두 취약점은 같은 근본 현상(추측 실행이 마이크로아키텍처 흔적을 남긴다)에서 출발하지만 공격 대상이 다릅니다.

> "Meltdown breaks the most fundamental isolation between user applications and the operating system." — Lipp, Schwarz, Gruss 외, "Meltdown"(2018), [meltdownattack.com](https://meltdownattack.com/)

Meltdown은 유저 프로세스와 커널 사이의 경계를, Spectre는 서로 다른 애플리케이션 사이의 경계를 깬다는 점에서 다릅니다.

> "Spectre breaks the isolation between different applications. It allows an attacker to trick error-free programs, which follow best practices, into leaking their secrets." — Kocher 외, "Spectre Attacks"(2018), [meltdownattack.com](https://meltdownattack.com/)

공개 이후 8년 가까이 지난 지금도 이 계열의 취약점은 끊이지 않고 새로 발견되고 있습니다. 아래 표는 커리큘럼과 직결되는 주요 변종만 추린 것으로, 전체 목록이 아니라 "추측 실행이 만드는 문제가 왜 한 번의 패치로 끝나지 않는가"를 보여주는 표본입니다.

| 연도 | 이름 | 공격 대상 |
|------|------|-----------|
| 2018 | Spectre v1/v2, Meltdown | bounds check 우회, 분기 목표 주입, 커널 메모리 유출 |
| 2018 | L1TF(Foreshadow) | 무효 PTE라도 L1 캐시에 남은 데이터를 추측적으로 로드 |
| 2019 | MDS(RIDL/Fallout/ZombieLoad) | 로드/스토어 버퍼 등 내부 버퍼의 잔여 데이터 샘플링 |
| 2022 | Retbleed | 얕은 콜스택에서 retpoline 자체를 우회하는 리턴 예측 |
| 2023 | Zenbleed, Downfall(GDS) | AMD Zen2 레지스터 파일 오염, Intel AVX 계열 gather 샘플링 |
| 2023 | Inception/SRSO | AMD 리턴 예측기에 추측 페이즈 자체를 주입 |
| 2024 | GhostRace | 잠금(lock) 경합 코드 경로에 숨은 Spectre v1 gadget |
| 2024 | Indirector | 간접 분기 예측기(IBP)·BTB를 고정밀 조작해 ASLR 우회 |
| 2025 | SLAP·FLOP | Apple M시리즈의 로드 주소/값 예측기 오남용 |
| 2025 | Branch Privilege Injection | 유저→커널 전환 순간 분기 예측기 갱신의 특권 혼동(CVE-2024-45332) |
| 2025 | VMScape | 게스트가 훈련한 분기 예측기 상태로 호스트 하이퍼바이저 침투(CVE-2025-40300) |

이 목록에서 알 수 있듯 벤더·세대가 바뀌어도 패턴은 반복됩니다 — 예측기를 원하는 방향으로 훈련시키고, 경계를 넘나드는 추측적 접근을 유도하고, 그 결과를 캐시나 다른 마이크로아키텍처 상태에 인코딩한 뒤 타이밍으로 읽어냅니다.

## 추측 실행이 비밀을 새어나가게 하는 메커니즘

핵심 아이디어는 단순합니다. CPU가 추측이 틀렸다는 것을 확인하면 **레지스터 값·메모리 쓰기 같은 아키텍처 상태는 되돌리지만**, 그 추측적 실행이 캐시에 무엇을 적재했는지, 분기 예측기의 히스토리를 어떻게 바꿔놨는지 같은 **부수 효과는 되돌리지 않습니다**. 공격자는 이 부수 효과를 직접 읽을 수 없지만, 캐시 히트와 미스의 접근 시간 차이를 측정하는 **Flush+Reload** 같은 타이밍 사이드채널로 간접적으로 읽어낼 수 있습니다. Spectre v1(bounds check bypass)의 전형적인 형태는 다음과 같은 코드 패턴에서 나타납니다.

```cpp
#include <cstdint>
#include <cstddef>

// 실제 공격 코드가 아니라 Spectre v1 gadget의 "패턴"을 보여주는 예시다.
// array1_size 검사가 있어도, 분기 예측기가 반복 학습을 통해 "범위 안"이라고
// 확신하고 있으면 검사 결과가 확정되기 전에 array1[x]를 추측적으로 읽어
// array2 인덱싱에 써버릴 수 있다.
uint8_t array1[16] = {0};
size_t array1_size = 16;
uint8_t array2[256 * 512];  // 캐시 라인 간격(512바이트)으로 분리한 probe 배열
uint8_t temp = 0;

void victim_function(size_t x) {
  if (x < array1_size) {                  // 예측기가 "참"으로 강하게 학습된 상태
    temp &= array2[array1[x] * 512];      // 검사 확정 전에 이미 실행될 수 있음
  }
}
```

공격자는 먼저 `victim_function`을 유효한 `x`로 반복 호출해 분기 예측기가 "범위 안"을 강하게 기대하도록 훈련시킵니다. 그다음 범위를 벗어난 `x`(예: 커널 메모리나 다른 프로세스의 비밀이 위치한 오프셋)로 호출하면, 예측기는 여전히 "범위 안"이라고 예측해 `array1[x]`의 실제 값(비밀 바이트)을 추측적으로 읽고, 그 값에 512를 곱한 오프셋으로 `array2`를 인덱싱합니다. 몇 사이클 뒤 bounds check가 확정되어 이 경로가 잘못되었음이 드러나면 CPU는 레지스터·`temp` 값을 원래대로 되돌리지만, `array2` 중 `secret * 512` 위치는 이미 캐시에 올라와 있습니다. 공격자는 이후 `array2`의 256개 캐시 라인을 하나씩 접근해 보며 어느 라인이 비정상적으로 빠르게(캐시 히트로) 응답하는지 측정하고, 그 인덱스가 곧 비밀 바이트 값입니다. Meltdown은 이와 다르게 커널 전용 페이지를 유저 모드에서 직접 로드하되, 권한 검사가 파이프라인 뒤쪽에서 비동기로 처리되는 틈을 노려 같은 방식으로 캐시에 값을 새깁니다.

```mermaid
flowchart LR
  train["공격자: 분기 예측기 훈련</br>(정상 입력으로 반복 호출)"] --> mispredict["피해자 코드: 예측기가</br>여전히 잘못 예측"]
  mispredict --> transient["추측적 실행:</br>bounds check 우회, 비밀 로드"]
  transient --> encode["비밀 값을 캐시 인덱스로</br>인코딩(probe 배열 접근)"]
  encode --> squash["예측 실패 확정</br>레지스터/메모리 롤백"]
  squash --> residue["캐시 상태는 롤백 안 됨</br>(마이크로아키텍처 잔여물)"]
  residue --> reload["공격자: Flush+Reload로</br>probe 배열 접근 시간 측정"]
  reload --> leak["가장 빠른 캐시 라인 인덱스</br>= 비밀 바이트 값"]
```

이 다이어그램에서 가장 중요한 지점은 `squash`와 `residue` 사이입니다. 아키텍처 상태 롤백과 마이크로아키텍처 상태 잔존 사이의 이 비대칭이야말로 지난 8년간 나온 거의 모든 변종(Spectre, Meltdown, MDS, Retbleed, Downfall, VMScape)이 공유하는 공통 근본 원인입니다.

## 흔한 오개념

**"패치를 다 적용하면 완전히 안전해진다"**는 틀린 생각입니다. Spectre/Meltdown류 취약점의 근본 원인은 추측 실행이라는 하드웨어 최적화 자체에 있고, 패치는 알려진 특정 gadget 패턴을 막을 뿐입니다. GhostRace(2024)가 잠금 경합 코드라는 전혀 새로운 위치에서 Spectre v1 gadget을 찾아냈고, Branch Privilege Injection(2025)이 유저→커널 전환의 나노초 단위 틈에서 새 경로를 찾아낸 것처럼, 예측기와 특권 전환이 존재하는 한 새로운 변종이 계속 나올 수 있습니다.

**"이건 소프트웨어 버그라 컴파일러·커널만 고치면 근본적으로 해결된다"**도 오해입니다. retpoline·LFENCE 삽입 같은 소프트웨어 완화는 하드웨어의 근본 동작(추측 실행)은 그대로 둔 채 특정 gadget이 악용되는 경로만 차단하는 우회책에 가깝습니다. eIBRS·CET 같은 하드웨어 강화도 특정 클래스의 공격만 저비용으로 막을 뿐, Retbleed가 retpoline을, Inception이 AMD의 하드웨어 완화를 각각 우회했듯 소프트웨어와 하드웨어 어느 쪽도 단독으로 "완전한 해결"을 제공하지 않습니다.

**"Spectre v1은 2018년 취약점이라 이제 레거시고 신경 쓸 필요 없다"**는 생각도 위험합니다. v1(bounds check bypass)은 하드웨어 수정이 사실상 불가능해 지금도 컴파일러 수준의 정적 분석과 수동 코드 검토에 의존하는데, GhostRace가 2024년에 리눅스 커널의 락 프리미티브에서 새 v1 gadget을 발견했다는 사실 자체가 "오래된 취약점 계열"이라는 인식과 "실제로 남아 있는 위험" 사이의 간극을 보여줍니다.

## 완화 기법과 성능 비용

완화 기법은 크게 세 갈래로 나뉩니다. **간접 분기 예측 자체를 막는 계열**(retpoline, IBRS/eIBRS, STIBP, IBPB)은 Spectre v2·BHI 계열을 겨냥하고, **투기적 메모리 접근 자체를 지연시키는 계열**(LFENCE 삽입)은 v1 gadget을 겨냥하며, **권한 경계를 넘는 캐시 접근을 차단하는 계열**(KPTI, L1D 플러시)은 Meltdown·L1TF·MDS 계열을 겨냥합니다. 이 세 갈래는 막는 대상이 다르므로 하나만 적용해서는 안 되고, 위협 모델에 맞춰 조합해야 합니다.

**Retpoline**은 컴파일러가 간접 호출/점프를 "예측된 실행이 무한 루프에 갇히는" 트램폴린 코드로 바꾸는 소프트웨어 기법입니다.

```text
; retpoline 개념도 — 실제 target으로는 ret가 점프하지만
; 예측된(추측) 실행 경로는 아래 루프에 갇혀 아무 것도 읽지 못한다
call setup_target
capture_speculation:
  pause
  lfence
  jmp capture_speculation
setup_target:
  mov [rsp], target_address
  ret                        ; 실제 실행: target_address로 점프
```

**IBRS(Indirect Branch Restricted Speculation)**는 이후 예측을 제한하는 하드웨어 기능이고, 이를 매 커널 진입마다 다시 켜야 했던 초기 버전 대신 부팅 시 한 번만 설정하면 되는 **eIBRS**가 뒤이어 나왔습니다. **STIBP**는 SMT 형제 스레드 사이에 예측기 상태를 격리하고, **IBPB**는 컨텍스트 전환·VMEXIT 시점에 예측기 히스토리를 통째로 비웁니다. 커널이 이 상태를 어떻게 판단했는지는 `/sys/devices/system/cpu/vulnerabilities/` 아래 파일로 직접 확인할 수 있습니다.

```text
$ cat /sys/devices/system/cpu/vulnerabilities/spectre_v2
Mitigation: Enhanced / Automatic IBRS; IBPB: conditional; RSB filling
$ cat /sys/devices/system/cpu/vulnerabilities/meltdown
Mitigation: PTI
```

(정확한 문자열은 커널 버전·마이크로코드·CPU 세대에 따라 달라지므로 대상 시스템에서 직접 확인해야 합니다.)

이 완화 기법들은 공짜가 아닙니다. Meltdown 대응으로 도입된 **KPTI(Kernel Page Table Isolation)**는 유저/커널 페이지 테이블을 분리해 커널 진입·복귀마다 추가 TLB 처리를 요구하며, 2018년 초 syscall이 잦은 워크로드(PostgreSQL, Redis 등)에서는 최대 30%에 가까운 성능 저하가 보고된 바 있습니다 — 이후 PCID(Process-Context Identifier) 지원으로 전체 TLB 플러시를 피할 수 있게 되면서 전형적인 비용은 크게 줄었지만, syscall 빈도가 극단적으로 높은 코드에서는 여전히 체감할 수 있는 수준입니다. Linux 커널 공식 문서는 L1TF 대응으로 VM 진입마다 L1D 캐시를 플러시하는 완화의 비용을 다음과 같이 명시합니다.

> "관련 성능 저하는 VM exit 빈도에 따라 1%에서 50% 사이로 나타난다." — [kernel.org, L1TF 문서](https://www.kernel.org/doc/html/latest/admin-guide/hw-vuln/l1tf.html) 요지 (조건부 플러시 기준, virtio 등 최적화된 구성에서는 영향이 최소화됨)

2025년 VMScape 대응으로 추가된 "VMEXIT 시 IBPB 발행" 완화도 비슷한 패턴을 보였다고 보도되었습니다 — 대부분의 워크로드에서는 1% 안팎으로 미미하지만, I/O가 잦은 가상화 워크로드에서는 51%까지 치솟을 수 있다는 것입니다([comsec.ethz.ch, VMScape 연구](https://comsec.ethz.ch/research/microarch/vmscape-exposing-and-exploiting-incomplete-branch-predictor-isolation-in-cloud-environments/)). 같은 해 공개된 Branch Privilege Injection의 마이크로코드 완화는 이보다 훨씬 가벼워, Alder Lake 기준 2.7% 수준의 오버헤드가 보고되었습니다([ethz.ch 뉴스](https://ethz.ch/en/news-and-events/eth-news/news/2025/05/eth-zurich-researchers-discover-new-security-vulnerability-in-intel-processors.html)). 이 세 수치의 편차 자체가 중요한 교훈입니다 — 완화 비용은 "몇 퍼센트"라는 단일 숫자가 아니라 **VMEXIT·syscall·TLB 미스 빈도 같은 워크로드 특성에 따라 1%와 50%를 오갈 수 있는 분포**이므로, 실제 배포 전에는 대상 워크로드로 직접 측정해야 합니다.

이 격리를 실제 시스템에서 재현해 측정하려면, syscall 하나의 순수 지연시간을 반복 측정하는 벤치마크를 부팅 옵션을 바꿔가며 비교하는 방법이 가장 직접적입니다.

```cpp
#include <benchmark/benchmark.h>
#include <unistd.h>

// spectre_v2=on(기본)과 spectre_v2=off, mitigations=off 커널 부팅 옵션으로
// 각각 재부팅한 뒤 이 벤치마크를 실행해 ns/iter를 비교하면, 완화 기법이
// syscall 경로에 추가하는 순수 오버헤드를 격리해 측정할 수 있다.
static void BM_GetpidSyscall(benchmark::State& state) {
  for (auto _ : state) {
    benchmark::DoNotOptimize(getpid());
  }
}
BENCHMARK(BM_GetpidSyscall);

BENCHMARK_MAIN();
```

`g++ -O2 -std=c++17 bench.cpp -lbenchmark -lpthread`(Linux, GCC 13 기준)로 빌드합니다. 이 벤치마크는 재부팅 권한과 커널 부팅 파라미터 변경 권한이 있는 격리된 테스트 환경에서만 실행해야 하며, 프로덕션 시스템의 완화를 실제로 끄는 근거로 곧바로 쓰면 안 됩니다 — 측정은 "이 워크로드에서 완화 비용이 실제로 얼마인가"를 파악하는 데만 씁니다.

## 판단 기준

| 상황 | 추측 실행 위협이 관련되는 이유 | 실무 대응 |
|------|-------------------------------|-----------|
| 멀티테넌트 클라우드(공유 하이퍼바이저) | 게스트가 예측기를 훈련시켜 호스트·다른 게스트를 침투(VMScape) | IBPB-on-VMEXIT 등 벤더 권장 완화를 전부 적용, I/O 워크로드는 사전 측정 |
| 브라우저·JS 샌드박스처럼 신뢰 안 되는 코드 실행 | 임의 스크립트가 같은 프로세스 내에서 Spectre v1/v2 gadget을 유발 가능 | 사이트 격리(process-per-origin), 컴파일러 스펙터 완화 옵션 활성화 |
| 단일 테넌트 임베디드·전용 어플라이언스 | 신뢰 안 되는 코드가 애초에 실행되지 않음 | 위협 모델 문서화 후 일부 완화(STIBP 등)를 선택적으로 비활성화 검토 |
| SMT(하이퍼스레딩) 활성화, 서로 다른 신뢰 수준 스레드 | 형제 스레드가 예측기 상태를 공유해 정보가 새어 나갈 수 있음 | STIBP 또는 신뢰 안 되는 워크로드만 SMT 비활성화([14장](/post/cpu-optimization/smt-hyperthreading-performance/)) |
| p99 지연시간이 예산의 전부인 단일 테넌트 HFT 서버 | 완화 비용이 곧바로 p99를 밀어 올림 | 위협 모델과 컴플라이언스 요건을 근거로 완화 범위를 팀 차원에서 명시적으로 합의 |

## 비판적 시각: 한계와 트레이드오프

추측 실행 취약점 대응은 "패치 한 번으로 끝나는 버그 수정"이 아니라 **끝나지 않는 두더지 잡기(whack-a-mole)**에 가깝습니다. Retpoline은 Retbleed에, AMD의 하드웨어 완화는 Inception에 각각 우회당했고, Indirector처럼 벤더가 "기존 완화로 충분하다"며 심각도를 낮춰 발표한 사례도 있어 완화가 실제로 얼마나 포괄적인지 외부에서 검증하기 어렵습니다. 근본 원인이 수십 년간 성능 향상의 핵심 동력이었던 추측 실행 자체에 있다 보니, 하드웨어 벤더 입장에서는 "완전히 끄면 안전하지만 성능이 크게 떨어지는" 기능을 쉽게 포기할 수 없다는 구조적 긴장이 계속됩니다.

이 긴장은 저지연 시스템 엔지니어에게 실제 선택의 문제로 다가옵니다. 앞서 본 것처럼 KPTI·IBPB·L1D 플러시 같은 완화는 워크로드에 따라 수십 퍼센트에 달하는 지연시간 비용을 청구할 수 있는데, 신뢰 안 되는 코드가 절대 실행되지 않는 단일 테넌트 전용 서버(예: 폐쇄망의 HFT 매칭 엔진)라면 일부 완화를 의도적으로 비활성화하는 것이 합리적인 선택일 수 있습니다. 다만 이 판단은 개인이 임의로 내릴 일이 아니라, 위협 모델·컴플라이언스 요건·향후 신뢰 경계 변화 가능성을 팀·보안 담당자와 함께 문서화한 뒤 내려야 합니다 — "성능 때문에 껐다"는 결정이 감사·사고 대응 시점에 근거 없는 선택으로 남으면 안 되기 때문입니다.

## 마무리

- [ ] 추측 실행이 아키텍처 상태와 마이크로아키텍처 상태를 다르게 취급한다는 점에서 사이드채널이 발생하는 원리를 설명할 수 있다.
- [ ] Spectre v1/v2와 Meltdown이 각각 어떤 경계를 깨는지 구분할 수 있다.
- [ ] retpoline·IBRS/eIBRS·STIBP·IBPB·KPTI가 각각 어떤 공격 계열을 막는지 설명할 수 있다.
- [ ] 완화 비용이 워크로드(syscall·VMEXIT 빈도)에 따라 크게 달라진다는 것을 알고, 배포 전 직접 측정할 수 있다.
- [ ] 신뢰 경계와 워크로드 특성에 따라 완화 범위를 판단하고 그 근거를 문서화할 수 있다.

**이전 장**: [CPU 하드웨어 카운터 활용](/post/cpu-optimization/cpu-hardware-performance-counters/) (챕터 09)

**다음 장에서는** CPU가 소비 전력과 발열 한도 안에서 클럭 주파수를 동적으로 조절하는 주파수 스케일링을 다룹니다. 추측 실행 완화가 명령어당 비용을 늘린다면, 주파수 스케일링은 같은 명령어를 초당 몇 번 실행할 수 있는지 자체를 바꾸므로, 두 요인을 함께 이해해야 지연시간 예산을 온전히 설명할 수 있습니다.

→ [CPU 주파수 스케일링과 성능](/post/cpu-optimization/cpu-frequency-scaling-performance/) (챕터 11)
