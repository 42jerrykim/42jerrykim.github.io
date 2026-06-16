---
collection_order: 8
date: 2026-03-10
lastmod: 2026-06-01
draft: false
title: "[Optimization(C++) 08] 템플릿/constexpr"
slug: templates-constexpr
description: "constexpr, consteval을 활용한 컴파일 타임 계산과 템플릿 기반 비용 제어 전략을 다룹니다. 런타임 오버헤드를 컴파일 타임으로 옮기고 인라이닝을 유도하는 패턴을 정리하며, 컴파일 시간·ABI 트레이드오프와 적용 기준을 제시합니다."
tags:
  - C++
  - Performance
  - Optimization
  - 성능
  - 최적화
  - Compiler
  - 컴파일러
  - Memory
  - 메모리
  - CPU
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Type-Safety
  - Profiling
  - 프로파일링
  - Benchmark
  - Time-Complexity
  - 시간복잡도
  - Space-Complexity
  - 공간복잡도
  - Testing
  - 테스트
  - Debugging
  - 디버깅
  - Refactoring
  - 리팩토링
  - Readability
  - Maintainability
  - Modularity
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
  - Edge-Cases
  - 엣지케이스
  - Pitfalls
  - 함정
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - Abstraction
  - 추상화
  - Composition
  - 합성
  - Documentation
  - 문서화
  - Math
  - 수학
---

**템플릿/constexpr**는 런타임 비용을 컴파일 타임으로 옮기고, 템플릿으로 인라이닝·타입별 최적화를 유도하는 수단입니다. 본 챕터에서는 **constexpr**·**consteval**을 활용한 컴파일 타임 계산과 템플릿 기반 비용 제어 전략을 다루고, lookup table·상수 분기 제거·코드 블로트 억제 방법을 정리합니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [03장: 추상화 비용 분석](/post/cpp-optimization/abstraction-cost/)의 "런타임 비용" 관점을 전제로 합니다. 템플릿이 타입별로 코드를 찍어낸다는 점과 `constexpr`가 "컴파일 타임 계산"을 뜻한다는 정도만 알면 충분합니다.

**이 장의 깊이**: 이 장은 **중급~전문가**를 포괄합니다. `constexpr`·`consteval`로 런타임 계산을 컴파일 타임으로 옮기는 것부터 시작해, 전문가 구간에서는 템플릿으로 인라이닝·상수 분기 제거를 유도하면서 코드 블로트를 억제하는 전략을 다룹니다. **다루지 않는 것**: 컴파일러 인라이닝 진단([12장](/post/cpp-optimization/inlining-techniques/))과 빌드 시간·모듈([09장](/post/cpp-optimization/modern-cpp-features/), Tr.02)입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "constexpr 함수·변수" ~ "consteval (C++20)" | 컴파일 타임 계산의 의미와 효과 이해 |
| **중급자** | "템플릿과 비용 제어" ~ "컴파일 타임 계산 전략" | lookup table·상수 분기 제거 적용 |
| **전문가** | "판단 기준" ~ "비판적 시각" | 코드 블로트 대비 이득 판단 |

---

## constexpr와 consteval 도입 (역사·배경)

**constexpr**는 C++11에서 도입되어 "상수 표현식에서 사용 가능한 함수·변수"를 표준화했습니다. C++14에서 제약이 완화되어 여러 문장·루프가 constexpr 함수 안에 올 수 있게 되었고, C++20에서는 **consteval**이 추가되어 "반드시 컴파일 타임에만 평가되는 함수"를 표현할 수 있게 되었습니다. 이로써 lookup table·설정값·분기 제거 등을 컴파일 타임에 처리해 런타임 비용을 줄이는 패턴이 언어로 지원됩니다.

> "A constexpr function is a function that can be used in a constant expression." — cppreference (constexpr). 상수 맥락에서 호출되면 컴파일 타임에 평가되고, 그렇지 않으면 일반 함수처럼 런타임에 실행됩니다.

## constexpr 함수·변수

**constexpr**로 선언된 함수와 변수는 **상수 표현식**에서 사용될 수 있으며, 그런 맥락에서는 **컴파일 타임**에 평가됩니다. 인자가 모두 상수이면 컴파일러가 컴파일 시점에 계산하고, 그렇지 않으면 일반 함수처럼 런타임에 실행됩니다. 즉, constexpr 함수는 **런타임과 컴파일타임 모두**에서 쓸 수 있는 이중 역할을 합니다.

```cpp
constexpr int factorial(int n) {
  return n <= 1 ? 1 : n * factorial(n - 1);
}
constexpr int k = factorial(5);  // 컴파일 타임에 120

// C++20: consteval은 반드시 상수 맥락에서만 호출
consteval int sq(int x) { return x * x; }
constexpr int a = sq(10);  // OK
```

로케일·설정에 의존하지 않는 순수 계산은 constexpr로 옮기면 런타임 부담을 줄일 수 있습니다.

## consteval (C++20)

**consteval** 함수는 **반드시 컴파일 타임에만** 평가됩니다. 상수 표현식이 아닌 맥락에서 호출하면 컴파일 오류가 납니다. "이 함수는 상수 맥락에서만 호출되어야 한다"는 API 계약을 타입 시스템으로 강제할 때 유용합니다.

**constexpr vs consteval**: constexpr는 "상수 맥락이면 컴파일 타임, 아니면 런타임"이고, consteval은 "항상 컴파일 타임"입니다. 호출처가 항상 상수일 때만 기대할 수 있으면 consteval로 제한하면 되고, 런타임 인자도 받아야 하면 constexpr를 씁니다.

## 템플릿과 비용 제어

템플릿은 **인스턴스화**될 때마다 해당 타입/값에 대한 코드가 생성됩니다. 따라서 템플릿 파라미터 조합이 많으면 **코드 크기**와 **컴파일 시간**이 늘어납니다. 반면 템플릿 함수는 대부분 **헤더에 정의**되어 인라인 확장되기 쉬우므로, 호출 오버헤드가 없고 컴파일러 최적화(인라이닝, 상수 전파)에 유리합니다.

**`if constexpr` 타입 디스패치**는 컴파일 타임에 분기를 결정해, 선택되지 않은 경로의 코드를 아예 생성하지 않습니다. 가상 함수나 런타임 분기 없이 타입별 구현을 하나의 함수에 담을 수 있어, 코드 블로트와 런타임 분기를 동시에 줄입니다.

```cpp
#include <string>
#include <type_traits>

template <typename T>
std::string to_text(const T& value) {
  if constexpr (std::is_integral_v<T>) {
    return std::to_string(value);       // 정수 경로만 인스턴스화
  } else if constexpr (std::is_floating_point_v<T>) {
    return std::to_string(value);       // 실수 경로만 인스턴스화
  } else {
    return std::string{value};          // 그 외(예: const char*)
  }
}

// 선택되지 않은 분기는 인스턴스화되지 않으므로 컴파일 오류·코드 생성이 없다.
// to_text(42), to_text(3.14), to_text("hi") 각각 다른 경로만 컴파일된다.
```

비용 제어를 위해 **타입별 특수화**나 **`if constexpr`**로 불필요한 인스턴스(예: 사용하지 않는 타입에 대한 코드)를 줄일 수 있습니다. 공통 인터페이스만 쓰고 나머지는 특수화로 제한하면 코드 블로트를 억제할 수 있습니다.

## 컴파일 타임 계산 전략

인덱스나 키가 제한된 집합이면, constexpr 함수로 **lookup table**을 생성해 `constexpr` 변수로 두면 런타임 계산·할당이 사라집니다. 아래 예는 `constexpr std::array`를 constexpr 함수로 채우고, `static_assert`로 "테이블이 정말 컴파일 타임에 확정되는지" 검증합니다.

```cpp
#include <array>
#include <cstddef>

// 컴파일 타임에 제곱 lookup table을 생성한다.
constexpr std::array<int, 16> make_squares() {
  std::array<int, 16> t{};
  for (std::size_t i = 0; i < t.size(); ++i)
    t[i] = static_cast<int>(i * i);
  return t;
}

constexpr auto kSquares = make_squares();   // 런타임 계산·할당 없음
static_assert(kSquares[4] == 16, "테이블이 컴파일 타임에 채워져야 한다");
static_assert(kSquares[15] == 225);
```

- **상수 파라미터 계산**: 설정·모드가 컴파일 타임 상수로 알려지면, 그에 따른 분기·계수도 constexpr로 계산해 런타임 분기를 제거할 수 있습니다.
- **검증**: `static_assert`나 consteval 함수로 "이 값은 반드시 상수여야 한다"는 조건을 두면, 실수로 런타임 경로로 빠지는 것을 방지할 수 있습니다.

**constexpr의 한계**: constexpr 평가 안에서는 정의되지 않은 동작, `reinterpret_cast`, 그리고 (구버전에서) 동적 할당·`try`/`throw`·가상 호출 등이 금지됩니다. C++20에서 일부 동적 할당·가상 호출이 풀렸고, C++23에서 더 완화되었지만, **허용 범위는 표준 버전과 컴파일러마다 다르므로** "컴파일 타임에 확정"을 기대하는 값은 `static_assert`나 constexpr 변수 초기화로 강제해 두는 것이 안전합니다.

## 평가 기준 (학습 성과 목표)

- **constexpr**와 **consteval**의 차이(상수 맥락에서만 vs 항상 컴파일 타임)를 설명하고, 런타임 분기·테이블 조회 제거에 활용할 수 있다.
- 템플릿 **인스턴스화**와 코드 크기·컴파일 시간 트레이드오프를 설명하고, `if constexpr`·특수화로 불필요한 인스턴스를 줄일 수 있다.
- lookup table·상수 파라미터 계산을 constexpr로 옮기고, `static_assert`/consteval로 상수 요구사항을 검증할 수 있다.

## 판단 기준 (언제 쓸고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 설정·모드가 상수일 때 | constexpr 계산, lookup table | 런타임 분기·테이블 조회 |
| "반드시 상수" API | consteval | constexpr만으로 런타임 호출 허용 |
| 템플릿 코드 블로트 | `if constexpr`, 특수화로 경로 제한 | 모든 조합 인스턴스화 |

**적용 체크리스트**: (1) 핫 경로에서 상수로 고정 가능한 부분은 constexpr로. (2) 컴파일 타임만 허용할 API는 consteval. (3) 템플릿 인스턴스 수가 많으면 타입/경로 제한 검토.

## 비판적 시각: 한계와 트레이드오프

- **컴파일 타임 증가**: constexpr·템플릿이 많으면 컴파일 시간과 오브젝트 크기가 커진다. 핫 경로와 상수로 확정되는 부분만 컴파일 타임으로 옮기는 것이 좋다.
- **consteval**: 런타임 인자도 받아야 하는 함수는 constexpr를 유지하고, "상수만" 받는 보조 함수만 consteval로 두는 식으로 구분한다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| constexpr | 상수 맥락에서 컴파일 타임, 그 외 런타임; 이중 역할 |
| consteval | 항상 컴파일 타임, 상수 API 강제 |
| 템플릿 | 인라인·최적화 유리, 인스턴스 수만큼 코드 증가; `if constexpr`·특수화로 제어 |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **constexpr** | 상수 표현식에서 사용 가능; 상수 맥락이면 컴파일 타임, 아니면 런타임 |
| **consteval** | C++20; 반드시 컴파일 타임에만 평가되는 함수 |
| **상수 맥락** | constexpr 변수 초기화, 템플릿 인자, `static_assert` 등 컴파일 타임에 평가되는 맥락 |

### 벤치마크 결과 해석 가이드

| 관찰 | 해석·다음 단계 |
|------|----------------|
| 런타임 계산이 핫패스에 있음 | constexpr/consteval로 옮길 수 있는지 검토; 컴파일 타임으로 이전 |
| 템플릿 인스턴스가 많아 컴파일 시간 증가 | 명시적 인스턴스화·외부 템플릿·공통 타입으로 묶기 검토 |
| constexpr 함수가 런타임에 호출됨 | 상수 맥락에서 호출하거나 consteval(C++20) 검토 |

### 자주 묻는 질문 (FAQ)

**Q: constexpr와 consteval의 차이는?**  
A: constexpr는 상수 맥락이면 컴파일 타임, 아니면 런타임에 평가될 수 있습니다. consteval(C++20)은 반드시 컴파일 타임에만 평가됩니다.

**Q: 템플릿이 비용을 줄이나요?**  
A: 템플릿은 인라이닝·타입별 최적화를 유도해 런타임 비용을 줄일 수 있지만, 인스턴스 수가 늘면 컴파일 시간·코드 크기가 늘 수 있습니다. 트레이드오프를 측정합니다.

**Q: 컴파일 타임 계산을 얼마나 써야 하나요?**  
A: 핫패스에서 반복되는 상수 계산·테이블 생성 등은 constexpr/consteval로 옮기면 유리합니다. 과도하면 컴파일 시간이 늘어나므로, 프로파일러로 확인한 뒤 적용합니다.

### 적용 체크리스트 (실무용)

- [ ] 핫패스에 상수 계산이 있는지 확인하고 constexpr/consteval로 옮겼는가?
- [ ] 템플릿 인스턴스 수가 과도하지 않은가? (컴파일 시간·코드 크기)
- [ ] 고정 lookup table을 `constexpr std::array`로 컴파일 타임에 생성했는가?
- [ ] `static_assert`로 상수 요구사항을 검증했는가?
- [ ] 변경 후 벤치마크·컴파일 시간으로 회귀 검증했는가?

### 진단 도구 요약

| 목적 | 도구·방법 |
|------|-----------|
| 컴파일 타임 vs 런타임 | constexpr 호출 맥락 확인, 어셈블리에서 상수 폴딩 확인 |
| 템플릿 인스턴스 수 | `-ftime-trace`, 바이너리 크기·심볼 수 |
| 컴파일 시간 | 빌드 시간 측정, 모듈·외부 템플릿 검토 |

### 자주 하는 실수

- **과도한 constexpr**: 모든 함수를 constexpr로 만들면 컴파일 시간이 늘 수 있음. 핫패스·상수 계산에 집중.
- **템플릿 남발**: 인스턴스가 많아지면 컴파일·코드 크기 비용이 큼. 공통 타입·명시적 인스턴스화 검토.
- **런타임 맥락에서만 호출**: constexpr 함수를 상수 맥락에서 호출해야 컴파일 타임에 평가됨. consteval이 필요하면 C++20 사용.

### 리팩토링 시 주의

기존 런타임 계산을 constexpr로 옮길 때, 의존하는 함수·데이터도 constexpr 호환으로 바꿔야 합니다. 점진적으로 옮기고, 테스트·벤치마크로 동작과 성능을 확인합니다.

### 추가 읽기 및 관련 챕터

- **챕터 07 (임시 제거)**: 런타임 임시 제거와 연계.
- **챕터 09 (Modern C++)**: ranges·concepts·modules와 컴파일·런타임 비용.
- **챕터 12 (인라이닝)**: 템플릿·인라이닝 유도.

---

## 다음 장에서는

**이전 장**: [임시 객체 제거](/post/cpp-optimization/temporary-removal/) (챕터 07)

**Modern C++ 기능**을 다룹니다. C++17/20/23의 ranges, concepts, modules 등 성능 관련 기능의 비용·이점과 Low-latency 활용 기준을 정리합니다. → [Modern C++ 기능](/post/cpp-optimization/modern-cpp-features/) (챕터 09)
