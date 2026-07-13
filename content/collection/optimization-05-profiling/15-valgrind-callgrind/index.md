---
collection_order: 15
date: 2026-07-12
lastmod: 2026-07-12
draft: false
image: wordcloud.png
title: "[Profiling 05] Valgrind·Callgrind: 캐시 시뮬레이션과 호출 그래프"
slug: valgrind-callgrind-cache-simulation
description: "Valgrind 계열 도구(memcheck·cachegrind·callgrind·massif)의 동적 바이너리 계측과 캐시 시뮬레이션 원리, 도구별 오버헤드, KCachegrind 시각화를 다루고 시뮬레이션 수치와 하드웨어 실측의 차이를 판단하는 기준을 정리합니다."
tags:
  - Performance(성능)
  - Optimization(최적화)
  - Profiling(프로파일링)
  - Benchmark
  - Latency
  - C++
  - C
  - Memory(메모리)
  - CPU(Central Processing Unit)
  - Cache
  - Compiler(컴파일러)
  - OS(운영체제)
  - Linux(리눅스)
  - Debugging(디버깅)
  - Testing(테스트)
  - Hardware(하드웨어)
  - Implementation(구현)
  - Best-Practices
  - Comparison(비교)
  - Pitfalls(함정)
  - Troubleshooting(트러블슈팅)
  - Workflow(워크플로우)
  - Guide(가이드)
  - Tutorial(튜토리얼)
  - Deep-Dive
  - Reference(참고)
  - 실습
  - Valgrind
  - Callgrind
  - Cachegrind
  - Memcheck
  - Massif
  - KCachegrind
  - Call-Graph
  - Cache-Simulation
---

**Valgrind는 프로그램의 기계어를 실행 시점에 가로채 중간 표현으로 번역하고, 그 위에 계측 코드를 삽입해 다시 실행하는 동적 바이너리 계측(DBI, Dynamic Binary Instrumentation) 프레임워크**입니다. 이 장에서는 Valgrind 계열 도구 중 성능 분석에 쓰이는 cachegrind(캐시·분기 시뮬레이션)와 callgrind(호출 그래프·명령어 수 프로파일링)를 중심으로, memcheck·massif가 성능 작업에서 맡는 보조 역할까지 함께 다룹니다. [샘플링 프로파일러](/post/profiling-analysis/sampling-profiling-perf-vtune/)가 "실제 하드웨어에서 시간이 어디에 쓰였는가"를 통계적으로 추정한다면, Valgrind 계열은 "이 코드가 몇 개의 명령어를 실행했고 어떤 메모리 접근 패턴을 보였는가"를 **결정론적으로 셉니다**. 실행할 때마다 수치가 흔들리는 µs 단위 측정의 세계에서, 매번 같은 숫자가 나오는 도구는 그 자체로 귀중한 기준선이 됩니다. 다만 그 숫자는 시뮬레이션의 산물이지 실측이 아니므로, 이 장의 후반부에서 "시뮬레이션 수치를 언제 믿고 언제 의심할지"를 명확한 기준으로 정리합니다.

## 이 장을 읽기 전에

**선행 챕터**: [샘플링 프로파일링: perf·VTune 원리](/post/profiling-analysis/sampling-profiling-perf-vtune/)를 먼저 읽으면 "샘플링 vs 시뮬레이션"의 대비가 선명해집니다. 캐시 계층(L1/L2/LL)과 캐시 미스가 왜 비싼지에 대한 기본 감각은 [Tr.01의 STL 컨테이너 비용](/post/cpp-optimization/stl-container-cost/) 수준이면 충분합니다.

**이 장의 깊이**: 난이도는 **기초**입니다. 도구 설치·실행·출력 해석까지를 손에 익히는 것이 목표이며, VEX 중간 표현의 내부 구조나 시뮬레이터 구현 세부까지는 내려가지 않습니다.

**다루지 않는 것**: 하드웨어 카운터로 캐시 미스를 실측하는 방법은 [08장 하드웨어 성능 카운터](/post/profiling-analysis/hardware-performance-counters/)에, perf 명령 자체의 고급 활용은 [07장 Linux perf 고급](/post/profiling-analysis/linux-perf-advanced/)에 위임합니다. 힙 할당 프로파일링(massif·DHAT의 심화 활용)은 [20장 메모리 프로파일링: 힙 분석](/post/profiling-analysis/memory-profiling-heap-analysis/)에서 본격적으로 다룹니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "역사" ~ "Cachegrind" | DBI·시뮬레이션 원리와 도구 가족 구분, cachegrind 실행·해석 |
| **중급자** | "Callgrind" ~ "KCachegrind" | 포함/배타 비용 구분, 선택적 계측으로 오버헤드 관리, 시각화 |
| **전문가** | "시뮬레이션 vs 실측" ~ "비판적 시각" | 시뮬레이션 수치의 신뢰 범위를 정의하고 실측과 역할 분담 |

## Valgrind의 역사: memcheck에서 도구 프레임워크로

Valgrind는 Julian Seward가 개발해 2002년 7월 1.0 버전을 공개한 오픈소스 프로젝트로, 이름은 북유럽 신화에서 발할라(Valhalla)의 정문을 가리키는 단어에서 왔습니다. 초기에는 메모리 오류 검출기(지금의 memcheck)가 사실상 전부였지만, 곧 "바이너리를 번역해 계측 코드를 끼워 넣는 코어"와 "그 위에서 무엇을 셀지 정의하는 도구 플러그인"을 분리한 프레임워크로 재설계되었습니다. 이 구조 덕분에 Nicholas Nethercote의 cachegrind, Josef Weidendorfer의 callgrind(원래 별도 프로젝트 'Calltree'로 시작해 3.2.0부터 본체에 합류), 힙 프로파일러 massif 같은 도구가 같은 코어 위에 얹혔습니다. 프레임워크의 설계 철학은 Nethercote와 Seward가 PLDI 2007에서 발표한 논문 "Valgrind: A Framework for Heavyweight Dynamic Binary Instrumentation"에 정리되어 있습니다.

프로젝트는 2026년 현재도 활발히 유지되고 있습니다. 2025년 10월의 3.26.0 릴리스는 라이선스를 GPLv3로 올리고 90건의 버그를 수정했으며, 이 글을 쓰는 2026년 7월 시점의 최신 안정판은 2026년 5월 20일 나온 3.27.1입니다. 성능 분석 관점에서 기억할 최근 변화는 하나입니다. **Valgrind 3.22(2023년 10월)부터 cachegrind의 기본값이 `--cache-sim=no`로 바뀌었습니다.** 캐시 시뮬레이션 모델이 2002년경 AMD Athlon 수준의 근사여서 현대 CPU의 동작을 반영한다고 보기 어렵다는 이유였고, 이제 기본 실행에서는 명령어 실행 수(Ir)만 셉니다. 캐시·분기 시뮬레이션이 필요하면 명시적으로 켜야 합니다.

## 핵심 원리: 동적 바이너리 계측과 시뮬레이션

Valgrind의 동작을 한 문장으로 줄이면 "프로그램을 CPU가 직접 실행하게 두지 않고, Valgrind가 만든 가상 CPU 위에서 실행한다"입니다. 코어는 원본 바이너리의 기계어 블록을 VEX라는 아키텍처 중립적 중간 표현(IR)으로 디스어셈블하고, 활성화된 도구 플러그인이 이 IR에 계측 코드를 삽입하면, 코어가 다시 호스트 기계어로 컴파일(JIT)해 실행합니다. 소스 코드도, 재컴파일도, 특별한 링크도 필요 없습니다. 디버그 심볼(`-g`)만 있으면 결과를 소스 라인 단위로 되돌려 붙일 수 있습니다.

```mermaid
flowchart LR
  exeBin["원본 바이너리</br>(x86-64 기계어)"] --> vexIr["VEX IR로 번역"]
  vexIr --> toolInstr["도구 플러그인이 계측 삽입</br>(예: 모든 메모리 접근 후킹)"]
  toolInstr --> jitGen["호스트 코드로 재컴파일 후 실행"]
  jitGen --> simState["시뮬레이터 상태 갱신</br>(I1/D1/LL 캐시, 분기 예측기)"]
  simState --> outFile["cachegrind.out.pid</br>callgrind.out.pid"]
```

이 방식의 결정적 성질이 두 가지 있습니다. 첫째, **모든 명령어·모든 메모리 접근을 빠짐없이 관찰**하므로 결과가 샘플링처럼 통계적 추정이 아니라 전수 조사입니다. 같은 입력이면(주소 공간 배치 무작위화 등 비결정 요소를 제외하면) 실행할 때마다 거의 같은 수치가 나옵니다. 둘째, 그 대가로 **오버헤드가 큽니다**. 모든 명령어가 번역·계측을 거치므로 [Valgrind 공식 도구 소개](https://valgrind.org/info/tools.html) 기준 memcheck는 원본 대비 약 10~30배, cachegrind는 약 20~100배, massif는 약 20배 느려집니다. callgrind는 cachegrind를 확장한 도구라 비슷한 자릿수의 오버헤드를 가지며, 커뮤니티에 보고된 실측 사례는 대략 20~50배 범위에 걸쳐 있습니다(워크로드·플랫폼에 따라 편차가 큽니다). [공식 매뉴얼](https://valgrind.org/docs/manual/cl-manual.html)이 못 박아 두는 지점은 두 곳뿐입니다 — 계측을 끈 상태(`--instr-atstart=no`)는 Valgrind 최소 오버헤드인 약 4배가 상한이고, 여기에 캐시·분기 시뮬레이션을 추가하면 다시 약 2배가 더해집니다. 이 오버헤드 때문에 Valgrind 계열은 프로덕션이 아니라 **개발 머신에서의 오프라인 분석 도구**입니다. 프로덕션에서 낮은 오버헤드로 상시 관찰하는 방법은 [11장 지속적 프로파일링](/post/profiling-analysis/continuous-profiling-production/)과 [16장 BPF 기반 동적 프로파일링](/post/profiling-analysis/bpf-based-profiling-bpftrace-bcc/)의 몫입니다.

성능 분석 관점에서 도구 가족을 정리하면 다음과 같습니다.

| 도구 | 측정 대상 | 대략적 오버헤드 | 성능 작업에서의 역할 |
|------|----------|----------------|--------------------|
| memcheck | 메모리 오류·누수 | 10~30배 | 최적화 전 정합성 확보, 누수로 인한 할당 압력 진단 |
| cachegrind | 명령어 수(Ir), 캐시·분기 시뮬레이션 | 20~100배 | 코드 변경 전후의 결정론적 비용 비교 |
| callgrind | 호출 그래프 + 명령어 수(+선택적 캐시 시뮬레이션) | 대략 20~50배(+시뮬레이션 시 추가 증가) | 어떤 호출 경로가 비용을 만드는지 구조적 분석 |
| massif | 힙 사용량 스냅샷 | 약 20배 | 힙 성장 곡선 파악([20장](/post/profiling-analysis/memory-profiling-heap-analysis/)에서 심화) |
| DHAT | 할당 블록의 수명·접근 밀도 | — | 짧게 살고 자주 할당되는 블록 탐지 |

오버헤드 수치는 워크로드와 옵션에 따라 크게 달라지므로 절대값보다는 자릿수 감각으로 받아들이는 것이 안전합니다.

## Cachegrind: 캐시·분기 시뮬레이션

cachegrind는 프로그램의 모든 명령어 인출과 데이터 접근을 가로채, 소프트웨어로 구현된 캐시 모델에 흘려 넣습니다. 모델은 1차 명령어 캐시(I1)·1차 데이터 캐시(D1)와 통합 최종 캐시(LL, Last-Level)의 3개로 구성되며, [공식 매뉴얼](https://valgrind.org/docs/manual/cg-manual.html)이 밝히듯 2002년경 AMD Athlon 하드웨어를 근사한 것입니다. 기본 실행은 앞서 말한 대로 Ir(실행 명령어 수)만 세고, `--cache-sim=yes`를 줘야 D1mr(1차 데이터 캐시 읽기 미스)·DLmr(최종 캐시 읽기 미스) 같은 캐시 이벤트가, `--branch-sim=yes`를 줘야 분기 예측 실패 이벤트가 나옵니다.

동작을 눈으로 확인하기 위해 캐시 접근 패턴만 다르고 계산량은 같은 두 함수를 준비합니다. 행 우선(row-major) 순회는 연속 메모리를 읽고, 열 우선(column-major) 순회는 매 접근마다 4KiB(N=1024, int 4바이트)씩 건너뛰므로 캐시 라인 재사용이 거의 없습니다.

```cpp
// demo.cpp — g++ -O1 -g demo.cpp -o demo  (-g는 소스 라인 매핑에 필수)
#include <cstdio>
#include <vector>

constexpr int N = 1024;

long long sum_row_major(const std::vector<int>& m) {
  long long s = 0;
  for (int i = 0; i < N; ++i)
    for (int j = 0; j < N; ++j) s += m[i * N + j];
  return s;
}

long long sum_col_major(const std::vector<int>& m) {
  long long s = 0;
  for (int j = 0; j < N; ++j)
    for (int i = 0; i < N; ++i) s += m[i * N + j];
  return s;
}

int main() {
  std::vector<int> m(static_cast<size_t>(N) * N, 1);
  std::printf("%lld %lld\n", sum_row_major(m), sum_col_major(m));
}
```

`-O1`을 쓴 이유는 두 가지입니다. `-O0`은 프레임 접근이 지배해 캐시 효과가 묻히고, `-O2` 이상은 컴파일러가 순회 순서를 바꾸거나 벡터화해 비교 자체를 무너뜨릴 수 있습니다. 최적화 수준이 측정 대상을 바꿔버리는 문제는 [01장 Microbenchmark 설계 원칙](/post/profiling-analysis/microbenchmark-design-principles/)에서 다룬 것과 동일한 함정입니다.

```bash
valgrind --tool=cachegrind --cache-sim=yes ./demo
cg_annotate cachegrind.out.$(pgrep -n demo 2>/dev/null || echo '<pid>')  # 실제로는 출력된 파일명을 그대로 사용
```

실행이 끝나면 `cachegrind.out.<pid>` 파일이 생기고, `cg_annotate`가 이를 함수·소스 라인 단위로 요약합니다. 아래는 예시 출력의 핵심 부분입니다(수치는 컴파일러·라이브러리 버전에 따라 다르며, 여기서는 해석 방법을 보이기 위한 전형적 형태입니다).

```text
--------------------------------------------------------------------------------
Ir          Dr         D1mr       DLmr       function
--------------------------------------------------------------------------------
5,246,483   1,048,576  1,048,412  1,048,201  sum_col_major(std::vector<int> const&)
5,246,483   1,048,576     65,613     65,540  sum_row_major(std::vector<int> const&)
```

해석은 이렇습니다. 두 함수의 Ir(실행 명령어 수)과 Dr(데이터 읽기 수)은 사실상 같습니다 — 같은 일을 하니까요. 그러나 D1mr(1차 데이터 캐시 읽기 미스)은 약 16배 차이가 납니다. 행 우선은 64바이트 캐시 라인 하나로 int 16개를 처리해 접근 16회당 미스 1회(1,048,576/16 ≈ 65,536)인 반면, 열 우선은 거의 모든 접근이 미스입니다. "실행 시간이 다르다"가 아니라 "**미스 횟수가 왜, 정확히 몇 배 다른지**"를 결정론적 수치로 보여주는 것이 cachegrind의 방식입니다. 같은 진단을 실제 하드웨어에서 하려면 [08장의 하드웨어 카운터](/post/profiling-analysis/hardware-performance-counters/)로 `cache-misses` 이벤트를 세면 되고, 두 결과를 비교하는 것이 좋은 훈련이 됩니다.

## Callgrind: 호출 그래프와 포함 비용

cachegrind가 "어느 라인이 비싼가"를 보여준다면, callgrind는 여기에 **누가 그 라인을 호출했는가**라는 구조를 더합니다. callgrind는 함수 호출·반환을 추적해 호출 그래프를 만들고, 각 함수의 비용을 배타 비용(self cost, 함수 자신이 직접 실행한 명령어)과 포함 비용(inclusive cost, 호출한 하위 함수까지 합친 비용)으로 나눠 기록합니다. 핫패스 분석에서 중요한 것은 대개 포함 비용입니다. "malloc이 배타 비용 상위"라는 정보만으로는 아무것도 고칠 수 없고, "어떤 경로가 malloc을 1초에 수십만 번 호출하는가"를 호출 그래프에서 찾아야 하기 때문입니다. 이 비용 전파(propagation) 개념은 [05장 Flame Graph 분석](/post/profiling-analysis/flame-graph-analysis/)의 스택 병합과 같은 문제를 다른 각도에서 푸는 것입니다.

```bash
valgrind --tool=callgrind --dump-instr=yes --collect-jumps=yes ./demo
callgrind_annotate callgrind.out.<pid>            # 함수별 요약
callgrind_annotate --tree=both callgrind.out.<pid> # 호출자/피호출자 트리 포함
```

`--dump-instr=yes`는 명령어(어셈블리) 단위 비용을, `--collect-jumps=yes`는 조건 분기의 실행/도약 횟수를 함께 기록해 이후 KCachegrind에서 어셈블리 뷰와 점프 시각화를 쓸 수 있게 합니다. 예시 출력은 다음과 같은 형태입니다.

```text
--------------------------------------------------------------------------------
Ir                      file:function
--------------------------------------------------------------------------------
5,246,483 (39.7%)  demo.cpp:sum_col_major(std::vector<int> const&)
5,246,483 (39.7%)  demo.cpp:sum_row_major(std::vector<int> const&)
1,048,576 ( 7.9%)  demo.cpp:main
```

여기서 main의 Ir이 낮게 보이는 것이 배타 비용의 함정입니다. main의 포함 비용은 사실상 100%이지만(두 함수를 모두 호출하므로), 배타 비용만 보면 초기화 루프 정도만 잡힙니다. `--tree=both`나 KCachegrind의 호출 그래프 뷰로 포함 비용을 함께 봐야 "어디를 고치면 전체가 줄어드는가"를 판단할 수 있습니다.

실전에서 callgrind의 오버헤드를 관리하는 핵심은 **선택적 계측**입니다. 초기화가 긴 서버 프로그램이라면 시작부터 전부 계측할 이유가 없습니다.

```bash
# 계측을 끈 채 시작(최소 오버헤드 ~4배), 원하는 시점에 켠다
valgrind --tool=callgrind --instr-atstart=no ./server &
callgrind_control -i on     # 관심 구간 진입 시 계측 시작
callgrind_control -d        # 현재까지의 프로파일 덤프
callgrind_control -i off    # 계측 중단
```

`--toggle-collect=<함수명>`을 쓰면 특정 함수에 들어갈 때만 수집을 켜고 나올 때 끄는 방식으로 핫패스만 격리할 수도 있습니다. 계측 자체를 끄면 오버헤드가 Valgrind 최소 수준(약 4배)까지 내려가므로, 긴 실행에서 관심 구간만 정밀하게 뜨는 워크플로우가 가능합니다.

## KCachegrind로 시각화하기

`callgrind_annotate`의 텍스트 출력은 함수 수가 수백 개를 넘으면 읽기 어려워집니다. [KCachegrind](https://kcachegrind.github.io/html/Home.html)는 callgrind 출력 파일을 읽어 호출 그래프(GraphViz `dot` 필요), 호출 관계 맵(treemap), 소스·어셈블리 주석 뷰(`objdump` 필요)를 제공하는 GUI 도구로, callgrind의 원저자인 Josef Weidendorfer가 함께 만들었습니다. KDE 의존성이 부담스러운 환경(macOS·Windows 포함)에서는 순수 Qt 버전인 QCachegrind를 쓰면 됩니다.

```bash
sudo apt install kcachegrind graphviz   # Debian/Ubuntu 계열
kcachegrind callgrind.out.<pid>
```

KCachegrind를 열면 왼쪽에 함수 목록(배타/포함 비용 정렬), 오른쪽에 선택 함수의 호출자·피호출자·호출 그래프·소스 주석 탭이 나옵니다. 실무에서 유용한 읽기 순서는 다음과 같습니다. 먼저 포함 비용(Incl.) 기준으로 정렬해 상위 함수에서 시작하고, 호출 그래프를 따라 내려가면서 "포함 비용이 크게 갈라지는 지점"을 찾습니다. 그 지점의 소스 주석 뷰에서 라인별 Ir(과 켜져 있다면 D1mr)을 확인하면, 텍스트 리포트로는 몇 시간 걸릴 탐색이 몇 분으로 줄어듭니다. 재귀·상호 호출이 만드는 사이클을 자동 감지해 묶어주는 기능도 텍스트 도구에는 없는 강점입니다. 다양한 프로파일러 출력 포맷을 이 화면 문법으로 읽는 일반론은 [19장 프로파일러 출력 해석 실전](/post/profiling-analysis/profiler-output-interpretation-practice/)에서 이어집니다.

## 시뮬레이션 vs 실측: 무엇을 믿을 것인가

이 장에서 가장 중요한 절입니다. cachegrind의 캐시 모델에 대해 공식 매뉴얼은 시뮬레이션이 다음과 같다고 명시합니다.

> "…are basic and unlikely to reflect the behaviour of a modern machine." — [Valgrind 공식 매뉴얼, Cachegrind 장](https://valgrind.org/docs/manual/cg-manual.html) (캐시·분기 시뮬레이션 기본값을 끈 이유에 대한 설명)

현대 CPU에는 시뮬레이터가 모델링하지 않는 것이 많습니다. 하드웨어 프리페처는 순차 접근 패턴을 감지해 미스를 선제 흡수하고, 비순차(out-of-order) 실행은 미스 지연을 다른 명령어 실행으로 가리며, 캐시 교체 정책도 순수 LRU가 아닙니다. TLB, 메모리 컨트롤러 큐잉, 하이퍼스레딩 간섭, 주파수 스케일링도 모두 시뮬레이션 밖입니다. 따라서 **cachegrind의 미스 수를 실제 하드웨어 카운터 값과 일치시키려는 시도는 실패할 수밖에 없고, 애초에 그 용도가 아닙니다**. 또한 Valgrind는 멀티스레드 프로그램을 한 번에 한 스레드씩 직렬화해 실행하므로, 락 경합·false sharing 같은 동시성 성능 문제는 아예 관찰 대상이 아닙니다.

그렇다면 무엇에 씁니까? 시뮬레이션의 강점은 정확도가 아니라 **결정론과 전수성**입니다. 실측(perf, VTune)은 실제 기계의 진실을 말하지만 실행마다 수 % 흔들리고, 짧은 함수는 샘플이 부족합니다. 시뮬레이션은 현실의 근사일 뿐이지만 같은 입력에 대해 거의 완전히 재현 가능하고, 아무리 짧은 코드라도 명령어 하나 단위까지 셉니다. 그래서 "리팩토링 전후로 실행 명령어 수가 0.3% 줄었는가" 같은 미세한 회귀 검증에는 실측보다 시뮬레이션이 오히려 신뢰할 만한 신호를 줍니다. 실제로 여러 오픈소스 프로젝트가 CI에서 cachegrind의 Ir 수를 성능 회귀 지표로 쓰는 이유가 이것입니다. 정리하면 역할 분담은 이렇습니다.

| 질문 | 적합한 도구 |
|------|------------|
| 실제 지연 시간이 어디서 발생하는가 | perf·VTune 실측 ([03장](/post/profiling-analysis/sampling-profiling-perf-vtune/)) |
| 실제 캐시 미스가 몇 번 일어났는가 | 하드웨어 카운터 ([08장](/post/profiling-analysis/hardware-performance-counters/)) |
| 이 변경으로 명령어 수·접근 패턴이 어떻게 변했는가 | cachegrind·callgrind (이 장) |
| 어떤 호출 경로가 비용을 만드는가 | callgrind + KCachegrind (이 장) |
| 노이즈 없는 결정론적 회귀 신호가 필요한가 | cachegrind Ir 비교 (이 장) |

## 흔한 오개념 교정

**오개념 1: "cachegrind의 미스 수치는 실제 캐시 미스 횟수다."** 아닙니다. 2002년경 하드웨어를 근사한 소프트웨어 모델의 출력이며, 프리페처·비순차 실행·현대적 교체 정책이 반영되지 않아 실측과 수치도, 때로는 경향도 다를 수 있습니다. cachegrind 수치는 "접근 패턴의 구조적 비교"(예: 순회 순서 A vs B)에 쓰고, 절대값 검증은 하드웨어 카운터로 합니다. 이 구분 때문에 3.22부터 캐시 시뮬레이션이 기본값에서 빠졌다는 사실 자체가 좋은 경고문입니다.

**오개념 2: "Ir이 크면 그만큼 느리다."** Ir은 실행 명령어 수이지 시간이 아닙니다. 명령어마다 지연이 다르고(나눗셈 vs 덧셈), 캐시 미스 하나가 명령어 수백 개 분량의 시간을 먹을 수 있으며, 비순차 실행이 상당 부분을 겹쳐 실행합니다. Ir이 10% 줄어도 실측 시간은 그대로일 수 있고 그 반대도 가능합니다. Ir은 "일의 양"의 결정론적 대리 지표로 유용하지만, 최종 판정은 항상 벽시계 시간·지연 분포 실측으로 해야 합니다.

**오개념 3: "Valgrind는 오버헤드가 커서 성능 분석에는 못 쓴다."** 오버헤드가 결과를 왜곡하는 것은 시간 기반 측정일 때의 이야기입니다. cachegrind·callgrind가 세는 것은 시간이 아니라 명령어 수와 시뮬레이션 이벤트이므로, 실행이 50배 느려져도 세어진 숫자 자체는 왜곡되지 않습니다. 못 쓰는 곳은 명확합니다 — 프로덕션 상시 프로파일링, 타이밍 의존 동작(타임아웃·경쟁 조건), 멀티스레드 경합 분석. 그 영역은 [16장 BPF](/post/profiling-analysis/bpf-based-profiling-bpftrace-bcc/)와 [17장 분산 트레이싱](/post/profiling-analysis/distributed-tracing-microsecond-overhead/)의 도구가 맡습니다.

## 판단 기준: 언제 Valgrind 계열을 꺼낼 것인가

- [ ] **호출 구조를 모른다** → callgrind + KCachegrind. 낯선 코드베이스의 비용 구조를 파악하는 첫 도구로 탁월합니다.
- [ ] **결정론적 전후 비교가 필요하다** → cachegrind Ir 비교. 노이즈가 심한 CI 환경에서 실측 벤치마크가 흔들릴 때 특히 유효합니다.
- [ ] **접근 패턴의 구조적 차이를 보이고 싶다** → `--cache-sim=yes`. 순회 순서·자료구조 배치 비교처럼 "몇 배" 수준의 차이를 볼 때만 씁니다.
- [ ] **하드웨어 카운터가 없는 환경이다**(일부 VM·컨테이너, 권한 제한) → 시뮬레이션이 유일한 캐시 분석 수단일 수 있습니다.
- [ ] **실제 지연·꼬리 지연을 판정해야 한다** → 피하십시오. 실측([03장](/post/profiling-analysis/sampling-profiling-perf-vtune/)·[09장](/post/profiling-analysis/tail-latency-analysis/))으로 갑니다.
- [ ] **멀티스레드 경합·타이밍 버그를 보고 있다** → 피하십시오. 스레드 직렬화 때문에 현상 자체가 사라집니다.
- [ ] **프로덕션이다** → 피하십시오. 10배 이상의 슬로다운은 상시 운영에 허용되지 않습니다.

## 비판적 시각: 한계와 트레이드오프

첫째, 캐시 모델의 노후화는 구조적 문제입니다. 시뮬레이터를 현대 CPU 수준으로 정교화하려면 마이크로아키텍처별 모델이 필요한데, 벤더가 세부를 공개하지 않는 데다 유지 비용이 막대해 현실적으로 개선이 어렵습니다. 프로젝트가 기본값을 끄는 쪽을 선택한 것은 정직한 결정이지만, 뒤집어 말하면 "캐시 시뮬레이션"이라는 이 장 제목의 절반은 이제 보조 기능이라는 뜻이기도 합니다.

둘째, 오버헤드는 관찰 대상 자체를 바꿉니다. 50배 느려진 프로그램은 네트워크 타임아웃에 걸리고, 타이머 기반 로직이 다르게 동작하며, 다른 프로세스와의 상호작용 타이밍이 완전히 달라집니다. "계측된 실행에서 관찰한 호출 구조가 실제 실행의 구조와 같다"는 가정은 CPU 바운드 코드에서는 대체로 성립하지만, I/O·타이머가 얽힌 코드에서는 검증 없이 믿을 수 없습니다.

셋째, 플랫폼 제약이 있습니다. Valgrind는 Linux를 중심으로 한 Unix 계열 도구이며 Windows 네이티브를 지원하지 않습니다(Windows에서는 [14장 ETW](/post/profiling-analysis/windows-etw-performance-analysis/)가 그 자리를 대신합니다). 또한 JIT 언어 런타임이나 특이한 시스템 콜을 쓰는 프로그램에서 호환성 문제가 생길 수 있습니다. 마지막으로, 결정론이라는 장점도 절대적이지 않습니다. ASLR, 힙 주소에 의존하는 해시 순서, 스레드 스케줄 의존 로직이 있으면 시뮬레이션 수치도 실행 간 흔들릴 수 있으므로, 회귀 게이트로 쓸 때는 허용 오차를 두고 운영해야 합니다.

## 마무리: 이 장의 평가 기준

- [ ] Valgrind의 DBI 구조(VEX 번역 → 도구 계측 → 재컴파일 실행)와 도구 플러그인 가족(memcheck·cachegrind·callgrind·massif)의 역할을 구분해 설명할 수 있다.
- [ ] cachegrind를 `--cache-sim=yes`로 실행하고 `cg_annotate` 출력에서 Ir·D1mr을 읽어 접근 패턴 차이를 진단할 수 있다.
- [ ] callgrind의 배타 비용과 포함 비용을 구분하고, `--instr-atstart=no`·`callgrind_control`로 관심 구간만 계측할 수 있다.
- [ ] KCachegrind에서 포함 비용 정렬 → 호출 그래프 → 소스 주석 순서로 병목 후보를 좁힐 수 있다.
- [ ] 시뮬레이션 수치(결정론적 명령어 수)와 실측(perf·하드웨어 카운터)의 역할 분담을 상황별로 판단할 수 있다.

**이전 장**: [Windows ETW 성능 분석](/post/profiling-analysis/windows-etw-performance-analysis/) — Windows 진영에서 커널 수준 이벤트로 같은 질문에 답하는 방법을 다뤘습니다.

**다음 장에서는** [BPF 기반 동적 프로파일링](/post/profiling-analysis/bpf-based-profiling-bpftrace-bcc/)을 다룹니다. Valgrind가 "개발 머신에서 느리지만 전수로" 보는 도구라면, bpftrace·BCC는 커널 안에서 검증된 프로그램을 실행해 "프로덕션에서 낮은 오버헤드로" 관찰하는 정반대 극단의 도구입니다. 두 접근의 대비를 통해 오버헤드-정밀도-운영 환경이라는 3축 트레이드오프가 완성됩니다.
