---
collection_order: 11
date: 2026-03-10
lastmod: 2026-07-10
draft: false
image: wordcloud.png
title: "[Optimization(C++) 11] 예외 처리 심화"
slug: exception-deep-dive
description: "zero-cost exception의 실제 동작과 noexcept 전략을 다룹니다. 예외 발생 경로와 정상 경로의 비용 차이, 예외 사양이 인라이닝·코드 생성에 미치는 영향을 마이크로벤치마크로 검증하고, 핫패스에서의 사용·회피 기준을 정리합니다."
tags:
  - C++
  - Performance
  - Optimization
  - 성능
  - 최적화
  - Error-Handling
  - 에러처리
  - Compiler
  - 컴파일러
  - Memory
  - 메모리
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Profiling
  - 프로파일링
  - Benchmark
  - Time-Complexity
  - 시간복잡도
  - Testing
  - 테스트
  - Debugging
  - 디버깅
  - Refactoring
  - 리팩토링
  - Type-Safety
  - Readability
  - Maintainability
  - Modularity
  - Edge-Cases
  - 엣지케이스
  - Pitfalls
  - 함정
  - Git
  - CI-CD
  - Linux
  - Windows
  - Latency
  - Throughput
  - Backend
  - 백엔드
  - Embedded
  - 임베디드
  - Advanced
  - Deep-Dive
  - 실습
  - Guide
  - 가이드
  - Reference
  - 참고
  - Case-Study
  - Technology
  - 기술
  - Tutorial
  - 튜토리얼
  - Documentation
  - 문서화
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - Abstraction
  - 추상화
  - Interface
  - 인터페이스
---

**예외 처리 심화**에서는 정상 경로와 예외 경로의 비용 차이를 구분하고, noexcept로 이동·인라이닝을 유도하는 방법을 다룹니다. 본 챕터에서는 zero-cost exception의 실제 동작과 noexcept 전략, 예외 사양이 인라이닝·코드 생성에 미치는 영향을 마이크로벤치마크로 검증합니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [03장: 추상화 비용 분석](/post/cpp-optimization/abstraction-cost/)에서 짚은 "예외의 정량적 비용"을 더 깊이 다룹니다. `try`/`catch`/`throw`의 기본 의미와 `noexcept` 키워드가 "예외를 던지지 않음을 약속"한다는 정도만 알면 충분합니다.

**이 장의 깊이**: 이 장은 **심화~전문가**를 포괄합니다. zero-cost exception 모델의 실제 동작부터 시작해, 전문가 구간에서는 예외 경로 비용, `noexcept`가 이동·인라이닝에 미치는 영향, 예외 사양이 코드 생성에 미치는 영향을 마이크로벤치마크로 검증합니다. **다루지 않는 것**: 에러 표현 대안인 `std::expected`([13장](/post/cpp-optimization/variant-optional-expected/))의 세부와 Windows SEH 내부 구현입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "예외 발생 경로 비용" | 정상 경로 vs 예외 경로 비용 차이 이해 |
| **중급자** | "noexcept의 의미와 최적화" ~ "예외 사양이 인라이닝·코드 생성에 미치는 영향" | noexcept로 이동·인라이닝 유도 |
| **전문가** | "판단 기준" ~ "비판적 시각" | 예외 vs 에러 코드/expected 선택 |

---

## Zero-cost exception 모델 (역사·배경과 실제)

"Zero-cost exception"은 **예외가 발생하지 않는 정상 경로**에서는 추가 비용을 거의 들이지 않겠다는 설계 목표입니다. 많은 Unix·Linux 플랫폼이 채택한 **Itanium C++ ABI**에서는 예외가 throw되지 않을 때 별도 분기나 테이블 조회를 하지 않고, 예외가 발생했을 때만 **unwinding** 정보와 **landing pad**를 사용해 스택을 되감고 catch 블록을 찾습니다. Windows에서는 **SEH(Structured Exception Handling)**와 연동된 방식으로 비슷한 "정상 경로 비용 없음" 모델을 따릅니다. 따라서 비용이 **예외 경로에만 집중**되며, 정상 경로에서는 예외 메커니즘이 거의 비용을 부과하지 않습니다.

> "In the zero-cost model, the runtime does not need to do anything when no exception is thrown. The cost is paid when an exception is thrown." — [Itanium C++ ABI: Exception Handling](https://itanium-cxx-abi.github.io/cxx-abi/abi-eh.html). noexcept는 "이 함수는 예외를 던지지 않는다"는 계약으로, 이동 선택·인라이닝에 영향을 줄 수 있습니다.

## 예외 발생 경로 비용

예외가 throw되면 런타임은 **스택을 되감으며** 각 프레임의 소멸자를 호출하고, **catch**가 나올 때까지 **landing pad**를 찾습니다. catch 블록이 여러 개이면 **타입 매칭**으로 어떤 catch가 이 예외를 받을지 결정합니다. 이 과정은 예외 타입·스택 깊이·프레임 수에 비례해 비용이 들므로, "예외는 예외적인 상황"에만 쓰는 것이 성능과 설계 모두에 좋습니다.

**예외 vs 에러 코드 / std::expected**: 예외는 정상 경로에는 비용이 거의 없지만 실패 경로는 비쌉니다. 에러 코드나 expected는 정상·실패 모두 같은 코드 경로로 처리되어 비용이 예측 가능합니다. 아래는 같은 파싱 로직을 두 방식으로 구현한 비교입니다. `std::from_chars`는 예외를 던지지 않으므로, expected 버전은 실패에도 unwinding이 없습니다.

```cpp
#include <expected>      // C++23
#include <charconv>
#include <string_view>
#include <stdexcept>
#include <system_error>

// expected 기반: 정상·실패 모두 같은 분기로 처리되어 비용이 예측 가능
std::expected<int, std::errc> parse(std::string_view s) {
  int value{};
  auto [ptr, ec] = std::from_chars(s.data(), s.data() + s.size(), value);
  if (ec != std::errc{})
    return std::unexpected(ec);
  return value;
}

// 예외 기반: 정상 경로는 zero-cost지만 실패 경로는 throw/unwinding 비용
int parse_or_throw(std::string_view s) {
  int value{};
  auto [ptr, ec] = std::from_chars(s.data(), s.data() + s.size(), value);
  if (ec != std::errc{})
    throw std::invalid_argument("invalid integer");
  return value;
}
```

실패가 자주 나오는 경로나, 실패 시에도 낮은 지연이 중요하면 expected·에러 코드를 쓰는 편이 낫습니다. 실패가 정말 드문 예외 상황이면 예외가 정상 경로를 더 깔끔하게 유지합니다.

**"정상 경로는 거의 공짜, throw 경로는 비싸다"는 주장을 실제로 격리 측정**하면 다음과 같습니다. 아래는 예외를 던지지 않는 정상 호출과, 매번 throw/catch가 일어나는 호출을 같은 틀에서 비교하는 Google Benchmark 코드입니다.

```cpp
#include <benchmark/benchmark.h>
#include <stdexcept>

static int normal_path(int x) { return x + 1; }

static int throwing_path(int x) {
  if (x < 0) throw std::invalid_argument("negative");
  return x + 1;
}

static void BM_NormalPath(benchmark::State& state) {
  int x = 0;
  for (auto _ : state) {
    x = normal_path(x);
    benchmark::DoNotOptimize(x);
  }
}
BENCHMARK(BM_NormalPath);

static void BM_ThrowCatchPath(benchmark::State& state) {
  for (auto _ : state) {
    try {
      throwing_path(-1);
    } catch (const std::invalid_argument&) {
      benchmark::DoNotOptimize(0);
    }
  }
}
BENCHMARK(BM_ThrowCatchPath);

BENCHMARK_MAIN();
```

`g++ -O2 bench.cpp -lbenchmark -lpthread`로 빌드해 실행하면(x86-64, GCC 13, `-O2` 기준 예시 수치), `BM_NormalPath`는 회당 약 0.3ns인 반면 `BM_ThrowCatchPath`는 회당 약 1~2µs로, **약 수천 배** 차이가 납니다. 절대값은 예외 타입·스택 깊이·플랫폼·언와인딩 구현에 따라 크게 달라지지만, "정상 경로 대비 throw 경로가 수천 배 비싸다"는 방향성 자체는 zero-cost 모델의 전형적 특징이며, 이 배율 때문에 예외를 제어 흐름(반복문 대체 등)으로 쓰면 안 되는 이유이기도 합니다.

## noexcept의 의미와 최적화

함수에 **noexcept**를 붙이면 "이 함수는 예외를 던지지 않는다"는 계약이 됩니다. 표준 라이브러리에서는 **이동 연산**이 noexcept일 때만 이동을 선택하고, 그렇지 않으면 복사를 선택하는 경우가 있습니다. 대표적으로 `std::vector` 재할당 시, 이동 생성자가 noexcept가 아니면 강한 예외 보장을 위해 **복사**를 선택합니다. **std::move_if_noexcept**는 "이동이 noexcept이면 이동, 아니면 복사"를 선택하는 유틸리티로, 이런 최적화를 일관되게 적용할 때 쓰입니다.

**소멸자**와 **이동 생성자·이동 대입 연산자**는 가능하면 **noexcept**로 두는 것이 좋습니다. 소멸자는 예외를 던지면 스택 언와인딩 중 추가 문제를 일으킬 수 있고, 이동이 noexcept여야 컨테이너가 이동을 안전하게 사용할 수 있기 때문입니다.

```cpp
#include <vector>

struct Widget {
  Widget(Widget&& other) noexcept { /* 이동 */ }
  Widget& operator=(Widget&& other) noexcept { return *this; }
  ~Widget() noexcept {}
};

// 이동 연산자가 noexcept이므로 vector 재할당 시 복사 대신 이동을 선택한다.
// noexcept를 떼면 같은 재할당에서 요소가 복사된다(강한 예외 보장 때문).
std::vector<Widget> v;
```

## 예외 사양이 인라이닝·코드 생성에 미치는 영향

noexcept 함수는 "예외를 전파하지 않는다"는 정보를 컴파일러에 주므로, **언와인딩 경로**를 생성하지 않아도 되고, **인라이닝**이나 **코드 배치**를 더 공격적으로 할 수 있는 여지가 생깁니다. 마이크로벤치마크에서는 "동일한 함수를 noexcept 있음/없음"으로 비교해 호출 비용이 미세하게 나뉘는지 확인할 수 있습니다. 효과는 플랫폼·컴파일러에 따라 다릅니다.

**실무 권장**: 실패 경로가 없거나, 실패 시 빠르게 종료해도 되는 **핫패스**에서는 해당 함수를 **noexcept**로 선언하는 것이 좋습니다. 예외를 던질 수 있는 경로가 있다면 noexcept를 붙이면 안 되며(위반 시 `std::terminate`), 대신 해당 경로는 에러 코드나 expected로 처리하는 설계를 고려합니다.

## 평가 기준 (학습 성과 목표)

- **zero-cost exception**의 의미(정상 경로 비용 없음, throw 경로는 비쌈)와 Itanium ABI·SEH 맥락을 설명할 수 있다.
- **noexcept**가 이동 선택·인라이닝·코드 생성에 미치는 영향을 설명하고, 소멸자·이동 연산에 noexcept를 적용할 수 있다.
- 예외 vs **에러 코드/expected**의 비용 차이를 구분하고, 실패가 빈번한 경로에서는 expected를 선택할 수 있다.

## 판단 기준 (언제 쓰고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 정상만 있는 핫패스 | noexcept | 예외 전파 가능 경로에 noexcept |
| 이동·컨테이너 활용 | 이동 생성/대입 noexcept | noexcept 없는 이동 |
| 실패가 자주 나는 경로 | expected·에러 코드 | 예외 throw |

### 자주 하는 실수

- **예외를 던질 수 있는 함수에 noexcept**: 위반 시 `std::terminate`; 예외 경로가 있으면 붙이지 않습니다.
- **이동 연산자에 noexcept 누락**: 컨테이너 재할당 시 복사가 선택될 수 있어 성능 손실.
- **실패가 빈번한 경로에 예외만 사용**: expected로 전환해 실패 경로 비용을 예측 가능하게 합니다.

### 리팩토링 시 주의

noexcept 추가 시 계약이 되므로, 해당 함수와 그 안에서 호출하는 함수가 예외를 던지지 않음을 보장해야 합니다. expected 도입 시 에러 타입 E를 가볍게 두고, 호출 체인 전체를 에러 코드/expected로 통일하는 것이 좋습니다.

## 멀티스레드 환경의 숨은 함정: 언와인딩 경합

이 챕터 앞부분에서 다룬 "throw 1회당 비용"은 **단일 스레드**에서 격리 측정한 값입니다. 여러 스레드가 **동시에** 예외를 던지는 상황에서는 전혀 다른 문제가 생깁니다. Itanium ABI 기반 구현(libgcc/libunwind 등)은 언와인딩 테이블 조회 경로의 상당 부분에서 **전역 동기화**(뮤텍스에 준하는 락)를 거치므로, 여러 스레드가 동시에 throw하면 이 락을 두고 경합합니다. 단일 스레드 마이크로벤치마크로는 이 경합이 전혀 드러나지 않습니다.

Thomas Neumann(TUM)은 WG21 논문에서 128코어 AMD EPYC 7713 머신을 이용해 이 경합을 정량적으로 보여줍니다. 실패율(예외가 발생하는 비율)을 고정한 채 스레드 수를 1→128로 늘렸을 때 실행 시간이 어떻게 바뀌는지 측정한 결과는 다음과 같습니다.

> "Threads: 1, 2, 4, 8, 16, 32, 64, 128 / 0.1% failure: 29ms, 29ms, 29ms, 29ms, 30ms, 30ms, 31ms, 105ms / 1.0% failure: 29ms, 30ms, 31ms, 34ms, 58ms, 123ms, 280ms, 1030ms / 10% failure: 36ms, 49ms, 129ms, 306ms, 731ms, 1320ms, 2703ms, 6425ms" — Thomas Neumann (TUM), [P2544R0: "C++ exceptions are becoming more and more problematic"](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2544r0.html) (2022-02-07)

실패율 10%를 고정하고 스레드 수만 1→128로 늘리면 36ms → 6,425ms로 **약 178배** 느려집니다. 코어가 늘어날수록 스레드가 더 많은 일을 병렬로 처리해 시간이 줄어들기를 기대하지만, 실패율이 조금이라도 있으면 오히려 초선형(super-linear)으로 나빠집니다. 실패율 0.1%처럼 아주 낮아도 128코어에서는 105ms로 3배 이상 벌어집니다. Low-latency 서비스가 멀티스레드로 동작하고 예외가 완전히 0은 아닌 실패 경로(파싱 실패, 검증 실패 등)에 쓰인다면, 이 경합이 단일 스레드 벤치마크에서는 보이지 않던 꼬리 지연의 원인이 될 수 있습니다. 멀티스레드 핫패스에서 실패가 드물지 않게 나온다면, 이 챕터에서 다룬 "정상 경로 vs throw 경로"뿐 아니라 "동시 throw 경로"까지 별도로 측정하거나, 애초에 expected·에러 코드로 설계하는 편이 안전합니다.

## 비판적 시각: 한계와 트레이드오프

- **예외**는 오류 전파와 스택 언와인딩을 맞춰 리소스 정리를 안전하게 해준다. "예외 금지"가 아니라, 핫패스와 실패 경로를 분리하고 실패 비용이 문제될 때만 expected로 대체하는 균형이 좋다.
- **noexcept**는 계약이므로, 위반 시 `std::terminate`가 호출된다. 예외를 던질 수 있는 경로가 있으면 붙이지 않는다.
- **멀티스레드 언와인딩 경합**은 단일 스레드 관점의 "zero-cost"를 무너뜨릴 수 있다. 동시성이 높은 서비스에서는 실패율이 낮아도 경합 비용을 별도로 측정해야 한다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| zero-cost | 정상 경로 비용 거의 없음, throw 경로는 언와인딩·landing pad 비용 |
| noexcept | 이동 선택·인라이닝 유리, 소멸·이동에 권장 |
| 실패 경로 | 빈번하면 expected·에러 코드, 예외는 예외 상황에만 |
| 멀티스레드 함정 | 동시 throw는 언와인딩 락 경합으로 초선형 저하(최대 178배, P2544) |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **landing pad** | 예외 발생 시 제어가 넘어가는 지점; catch 블록 진입 |
| **unwinding** | 스택을 되감으며 소멸자 호출·landing pad 탐색 |
| **move_if_noexcept** | 이동이 noexcept이면 이동, 아니면 복사를 선택하는 유틸리티 |

### 자주 묻는 질문 (FAQ)

**Q: zero-cost exception이란?**  
A: 예외를 던지지 않는 정상 경로에서는 비용이 거의 없고, throw 시에만 unwinding 등 비용이 든다는 모델(Itanium ABI·SEH)입니다.

**Q: 모든 함수에 noexcept를 붙여도 되나요?**  
A: 아니요. 예외를 던질 수 있는 경로가 있으면 noexcept를 붙이면 안 되며(위반 시 terminate), 소멸자·이동 연산자 등 실패가 없을 때만 씁니다.

**Q: 예외 vs expected 선택 기준은?**  
A: 실패가 예외적이면 예외, 실패가 빈번한 경로면 expected·에러 코드로 예측 가능한 비용을 선택합니다.

**Q: 멀티스레드 환경에서도 "정상 경로는 공짜"인가요?**  
A: 정상 경로(throw 없음)는 여전히 공짜에 가깝습니다. 문제는 **여러 스레드가 동시에 throw할 때**입니다. 언와인딩 구현의 전역 락 경합으로 실패율이 낮아도 스레드 수가 늘수록 초선형으로 느려질 수 있습니다(P2544). 단일 스레드 벤치마크만으로는 이 비용이 드러나지 않으므로, 멀티스레드 핫패스라면 동시 throw 시나리오를 별도로 측정해야 합니다.

### 적용 체크리스트 (실무용)

- [ ] 소멸자·이동 연산자에 noexcept 적용했는가?
- [ ] 실패 경로가 있으면 예외 대신 expected 검토했는가?
- [ ] noexcept 유무에 따른 인라이닝·이동 선택 벤치마크했는가?
- [ ] 멀티스레드 핫패스라면 동시 throw 시 언와인딩 경합을 별도로 측정했는가?

### 추가 읽기 및 관련 챕터

- **챕터 10 (코루틴)**: 비동기·런타임 오버헤드.
- **챕터 12 (인라이닝)**: noexcept가 인라이닝에 미치는 영향.
- **챕터 13 (variant/optional/expected)**: expected 상세.
- [Itanium C++ ABI: Exception Handling](https://itanium-cxx-abi.github.io/cxx-abi/abi-eh.html) — zero-cost 예외 모델·언와인딩·landing pad 규격을 정의하는 1차 출처.
- [cppreference: noexcept specifier](https://en.cppreference.com/w/cpp/language/noexcept_spec) — noexcept 계약, 위반 시 `std::terminate` 규칙을 다루는 1차 출처.
- [P2544R0: "C++ exceptions are becoming more and more problematic"](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2544r0.html) — Thomas Neumann(TUM, 2022), 멀티스레드 언와인딩 락 경합을 실측 데이터로 보여주는 WG21 논문.

---

## 다음 장에서는

**이전 장**: [코루틴 성능](/post/cpp-optimization/coroutine-performance/) (챕터 10)

**인라이닝 유도 기법**을 다룹니다. inline·__forceinline 활용과 인라이닝을 유도하는 코드 패턴, 실패 원인 진단(Tr.02 컴파일러 트랙 연계)을 정리합니다. → [인라이닝 유도 기법](/post/cpp-optimization/inlining-techniques/) (챕터 12)
