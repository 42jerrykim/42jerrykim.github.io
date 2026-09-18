---
title: "[Cpp] 배열의 1%만 서브노멀이어도 인텔에서 45배 느려지는 이유"
description: "Daniel Lemire가 5종 CPU에서 측정한 벤치마크에 따르면 배열 값의 1%만 서브노멀이어도 인텔 곱셈은 최대 50배, 나눗셈은 18배 느려지지만 AMD Zen 5·ARM 계열은 거의 영향이 없다. 원인인 마이크로코드 보조 경로와 FTZ/DAZ 회피법을 정리한다."
date: 2026-09-18
lastmod: 2026-09-18
draft: false
categories:
  - Cpp
  - Optimization
tags:
  - C++
  - Assembly
  - Floating-Point(부동소수점)
  - IEEE-754(부동소수점표준)
  - Numerical-Computing(수치계산)
  - Computer-Architecture(컴퓨터구조)
  - Precision(정밀도)
  - SIMD(단일명령다중데이터)
  - Vectorization(벡터화)
  - Pipelining(파이프라이닝)
  - Bottleneck(병목)
  - Low-Level(로우레벨)
  - Register(레지스터)
  - ISA(명령어집합구조)
  - Optimization(최적화)
  - Performance(성능)
  - Benchmark(벤치마크)
  - Cache(캐시)
  - Compiler(컴파일러)
  - Memory(메모리)
  - Latency(지연시간)
  - Hardware(하드웨어)
  - CPU(중앙처리장치)
  - Subnormal-Number
  - Denormal-Number
  - Microcode-Assist
  - x86
  - Daniel-Lemire
image: "wordcloud.png"
---

0에 아주 가까운 부동소수점 값, 즉 **서브노멀(subnormal, denormal)** 수를 계산에 섞으면 느려진다는 건 게임 프로그래머와 머신러닝 엔지니어 사이에서 오래된 경험칙이다. 그런데 "얼마나" 느려지는지, 그리고 그 느려짐이 CPU를 가리지 않고 똑같이 나타나는지는 별개의 질문이다. 컴퓨터과학자 Daniel Lemire가 2026년 9월 15일 공개한 벤치마크는 이 질문에 구체적인 숫자로 답한다 — 배열 값의 단 1%만 서브노멀이어도 인텔 프로세서에서는 벡터화된 연산 블록 전체가 느려지는 반면, AMD Zen 5와 ARM 계열(AWS Graviton 5, Apple M4 Max)에서는 사실상 아무 일도 일어나지 않는다.

## 서브노멀이 뭐고 왜 생기나

IEEE 754 표준은 부동소수점 수를 부호·지수·가수(mantissa)로 표현한다. 지수가 표현 가능한 최솟값에 도달하면, 표준은 두 가지 선택지 중 하나를 강제로 고른다. 그 아래 값을 전부 0으로 뭉개거나(급격한 언더플로), 가수의 정밀도를 조금씩 깎아가며 0까지 완만하게 줄어들게 하거나(완만한 언더플로, gradual underflow)다. IEEE 754는 후자를 선택했고, 그 결과 지수부가 전부 0이면서 가수부가 0이 아닌 특수한 비트 패턴이 정의됐다 — 이것이 서브노멀이다. 배정밀도(double) 기준 서브노멀은 약 4.9 × 10⁻³²⁴부터 2.2 × 10⁻³⁰⁸ 사이의 극히 작은 값을 표현하며, 신호 처리나 반복 계산에서 값이 0으로 수렴해 가는 과정에 자연스럽게 나타난다.

문제는 이 "가수 정밀도를 깎아가며 표현"하는 비트 패턴이 일반 정규화(normal) 수와 형태가 달라서, CPU의 부동소수점 실행 유닛이 정규화 수를 처리하도록 설계된 고정 파이프라인을 그대로 통과시킬 수 없다는 데 있다. 하드웨어가 이 특수 케이스를 전용 회로로 처리하지 않으면, 훨씬 느린 별도의 경로로 떨어진다.

## 벤치마크 설계: 5개 아키텍처, 5가지 커널

Lemire는 16,384개 double 값으로 이루어진 배열(캐시에 들어가는 크기)에 대해 다섯 가지 커널을 측정했다.

- 각 값에 0.75를 곱하기
- 두 배열을 더하기
- 각 값을 3으로 나누기
- 입력은 정규화 값이지만 출력이 서브노멀이 되도록 아주 작은 상수(2⁻¹⁰³⁰)를 곱하기
- 이전 결과에 의존하는 종속 연쇄(`x *= 0.9999`를 16,384번 반복)

각 커널을 정규화 값(0.5–1.0 범위)만 있는 경우, 서브노멀이 100개 중 1개(1%) 섞인 경우, 전부 서브노멀인 경우로 나눠 측정했다. 컴파일러는 GCC 15와 Apple Clang 17을 `-O3 -march=native`로 썼고, Clang 21로 교차 확인했다. 테스트 CPU는 다음 다섯 종이다.

- Intel Xeon 6975P-C (Granite Rapids, AWS c8i.xlarge)
- Intel Xeon Gold 6548N (Emerald Rapids, 자체 서버)
- AMD EPYC 9R45 (Zen 5, AWS c8a.xlarge)
- AWS Graviton 5 (Arm Neoverse V3, c9g.xlarge)
- Apple M4 Max

## 핵심 수치: 인텔만 유독 느리다

원소당 나노초(ns) 단위로 측정한 결과는 인텔 두 세대와 나머지 세 아키텍처 사이에 분명한 선을 긋는다.

**Intel (Granite Rapids / Emerald Rapids)**

| 커널 | 정규화 | 1% 서브노멀 | 전부 서브노멀 |
|---|---|---|---|
| 곱하기 0.75 (Granite Rapids) | 0.17 | 0.44 | 8.35 |
| 3으로 나누기 (Granite Rapids) | 0.51 | 0.85 | 9.38 |
| 종속 연쇄 (Granite Rapids) | 0.77 | – | 32.69 |
| 곱하기 0.75 (Emerald Rapids) | 0.21 | 0.49 | 9.25 |
| 3으로 나누기 (Emerald Rapids) | 0.57 | 0.94 | 10.40 |
| 종속 연쇄 (Emerald Rapids) | 1.14 | – | 36.51 |

**AMD Zen 5 / ARM 계열**

| 커널 | 정규화 | 1% 서브노멀 | 전부 서브노멀 |
|---|---|---|---|
| 곱하기 0.75 (Zen 5) | 0.07 | 0.10 | 0.08 |
| 3으로 나누기 (Zen 5) | 0.11 | 0.24 | 0.25 |
| 종속 연쇄 (Zen 5) | 0.66 | – | 0.88 |
| 곱하기 0.75 (Graviton 5 / M4 Max) | 0.17 / 0.06 | 0.17 / 0.06 | 0.16 / 0.06 |
| 종속 연쇄 (Graviton 5 / M4 Max) | 0.91 / 0.72 | – | 0.91 / 0.75 |

인텔 계열에서 서브노멀이 낀 곱셈은 정규화 값 대비 약 45–50배, 나눗셈은 약 18배 느려진다. 종속 연쇄는 단계당 약 1ns에서 30ns 이상으로 늘어난다. 정상 곱셈의 지연시간이 4사이클이라면, 서브노멀이 낀 곱셈은 128사이클이다. 입력이 서브노멀이든 출력이 서브노멀이든 페널티는 동일하다 — "정규화 in, subnormal out" 커널(Granite Rapids 기준 0.17ns → 8.58ns)이 이를 보여준다. 유일한 예외는 덧셈·뺄셈으로, 서브노멀이 섞여도 전속력을 유지한다.

AMD Zen 5는 곱셈·덧셈이 입력과 무관하게 전속력으로 돈다. 종속 곱셈 연쇄만 약 30% 느려지고(단계당 0.66ns → 0.88ns), 나눗셈은 약 2배 느려진다. 흥미로운 점은 나눗셈에서 1%만 서브노멀이어도 전부 서브노멀인 경우와 거의 비슷하게 느려진다는 것이다. Graviton 5와 Apple M4 Max는 아예 신경 쓰지 않는다 — 정규화 값과 서브노멀 값의 실행 시간 차이가 측정 오차 수준이다.

## 왜 인텔에서만 이런가: 마이크로코드 보조 경로

Lemire의 벤치마크 자체는 원인을 깊이 파고들지 않지만, Chips and Cheese가 2024년 공개한 인텔 E-코어 분석이 그 배경을 설명한다. 인텔 CPU의 부동소수점 실행 유닛은 정규화 값을 전용 하드웨어 경로로 처리하도록 설계돼 있는데, 서브노멀처럼 표준 파이프라인이 다루지 못하는 예외 케이스가 나타나면 훨씬 느린 마이크로코드 보조(microcode assist) 경로로 넘어간다. 이 분석에 따르면 인텔 Crestmont(E-코어)에서는 서브노멀 결과를 만드는 곱셈 하나가 280사이클 이상 걸렸다. 반면 후속 E-코어인 Skymont는 서브노멀을 전담하는 하드웨어 fast path를 추가해, `-ffast-math` 없이도 이 페널티를 없앴다.

문제는 Lemire가 측정한 Granite Rapids·Emerald Rapids가 이 fast path를 갖춘 Skymont가 아니라 인텔의 P-코어 계열이라는 점이다. 같은 글에 달린 독자 댓글이 지적하듯, 인텔은 이미 자사 E-코어에 서브노멀 하드웨어 처리 기술을 갖고 있으면서도 아직 P-코어 라인업 전체에는 옮기지 못한 상태로 보인다. 벡터화된 코드에서 이 마이크로코드 경로가 치명적인 이유는 SIMD 명령어 하나가 여러 값을 한 번에 처리하기 때문이다. 16개 값 중 단 1개만 서브노멀이어도, 그 SIMD 레인 전체가 마이크로코드 경로로 떨어지면서 나머지 15개의 정규화 값까지 함께 그 속도로 묶인다. 최적화 컴파일러가 아무리 정상 경로를 벡터화해도, 예외적인 입력 하나가 파이프라인 전체를 끌어내리는 셈이다.

## 실전 팁: 회피법과 트레이드오프

인텔 P-코어에서 서브노멀이 성능에 문제가 된다고 판단되면, MXCSR 레지스터의 FTZ(Flush-To-Zero)와 DAZ(Denormals-Are-Zero) 플래그를 켜는 것이 표준적인 회피책이다. FTZ는 연산 결과가 서브노멀이면 0으로 처리하고, DAZ는 입력이 서브노멀이면 0으로 취급한다. GCC·Clang에서는 `-mdaz-ftz`, 인텔 컴파일러에서는 `-ftz` 플래그로 켤 수 있다.

1. **FTZ/DAZ를 켠다**: 지진파 모델링 소프트웨어 DENISE Black Edition의 사례에서는 FTZ를 켠 뒤 실행 시간이 절반 이하로 줄고 병렬 효율이 0.42에서 0.86으로 개선됐다고 보고됐다. 다만 FTZ/DAZ는 IEEE 754 표준과 어긋나는 동작이라, 서브노멀 결과가 실제로 의미 있는 계산(예: 부호가 중요한 나눗셈의 분모)에서는 결과가 달라질 수 있다.
2. **데이터 타입을 바꾼다**: 단정밀도(float)에서 서브노멀이 자주 나온다면 배정밀도(double)로 바꿔 여유를 확보하는 방법이 있다. 반대로 float128 같은 초고정밀 타입으로 도피하는 건 추천되지 않는다 — 그 자체로 연산이 훨씬 느리기 때문이다.
3. **수치적으로 회피한다**: 계산 결과에 작은 상수를 더해 값이 0에 너무 가까워지지 않게 하는 "softening" 기법으로 서브노멀 발생 자체를 막을 수도 있다. 다만 이는 계산의 의미를 바꾸는 것이므로 수치해석적으로 그래도 되는 상황인지 먼저 확인해야 한다.

셋 다 트레이드오프가 있으므로, IEEE 754 완전 준수가 필요한 과학 계산 코드라면 FTZ/DAZ를 기본으로 켜기보다 서브노멀이 실제로 핫패스에서 발생하는지부터 프로파일링으로 확인하는 편이 안전하다.

## 요약

| 아키텍처 | 곱셈(전부 서브노멀) | 나눗셈(전부 서브노멀) | 1% 서브노멀의 영향 |
|---|---|---|---|
| Intel Granite/Emerald Rapids | 정규화 대비 약 45–50배 | 약 18배 | 블록 전체가 느려짐 |
| AMD Zen 5 | 거의 없음(연쇄만 약 1.3배) | 약 2배 | 나눗셈만 영향 |
| AWS Graviton 5 / Apple M4 Max | 측정 오차 수준 | 측정 오차 수준 | 없음 |

정규화 경로만 놓고 보면 최신 CPU들의 부동소수점 처리량은 크게 다르지 않다. 하지만 "드물게 나타나는 예외적인 입력값 하나가 파이프라인 전체를 얼마나 끌어내리는가"라는 축에서는 아키텍처 간 격차가 이렇게 크게 벌어진다. 벡터화나 캐시 지역성처럼 흔히 논의되는 최적화 축과 마찬가지로([관련 글: 벡터화가 빠른 진짜 이유](/post/2026-09-06-vectorization-ilp-mlp-not-simd-width/)), 부동소수점 엣지 케이스 처리 역시 실제 하드웨어를 재는 것 외에는 답이 나오지 않는 영역이다.

## 참고 자료

- Daniel Lemire, "Subnormal floating-point numbers are expensive… on Intel processors" (2026-09-15): <https://lemire.me/blog/2026/09/15/subnormal-floating-point-numbers-are-expensive-on-intel-processors/>
- 벤치마크 소스 코드: <https://github.com/lemire/Code-used-on-Daniel-Lemire-s-blog/tree/master/2026/09/15>
- Chips and Cheese, "FP rounding, subnormals, and Intel's E-cores" (2024-06-15): <https://chipsandcheese.com/i/146379373/fp-rounding>
- Intel, "Set the FTZ and DAZ Flags": <https://www.intel.com/content/www/us/en/docs/dpcpp-cpp-compiler/developer-guide-reference/2023-0/set-the-ftz-and-daz-flags.html>
- POP Centre of Excellence, "Avoiding subnormal floating-point calculations": <https://co-design.pop-coe.eu/best-practices/avoid-subnormals.html>
