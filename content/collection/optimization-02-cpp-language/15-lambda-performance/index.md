---
collection_order: 15
date: 2026-03-10
lastmod: 2026-07-10
draft: false
image: wordcloud.png
title: "[Optimization(C++) 15] 람다 표현식 성능"
slug: lambda-performance
description: "람다의 캡처 비용(by-value vs by-reference), 클로저 객체 크기·정렬, 인라이닝 가능성 등 성능 특성을 다룹니다. std::function과의 비교 및 콜백·알고리즘 전달 시 비용을 정리하고, 타입 소거 vs 템플릿 전달의 트레이드오프를 제시합니다."
tags:
  - C++
  - Performance
  - Optimization
  - 성능
  - 최적화
  - Functional-Programming
  - 함수형프로그래밍
  - Memory
  - 메모리
  - Compiler
  - 컴파일러
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
  - OOP
  - 객체지향
  - Abstraction
  - 추상화
  - Git
  - CI-CD
  - Linux
  - Windows
  - Latency
  - Throughput
  - Backend
  - 백엔드
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
  - Strategy
  - Iterator
  - Documentation
  - 문서화
  - Comparison
  - 비교
  - Data-Structures
  - 자료구조
---

**람다 성능**은 캡처 방식·클로저 크기·전달 방식(템플릿 vs std::function)에 따라 달라집니다. 본 챕터에서는 **by-value vs by-reference** 캡처 비용, 클로저 객체 크기·인라이닝 가능성, **std::function**과의 비교 및 콜백·알고리즘 전달 시 비용을 정리합니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [03장: 추상화 비용 분석](/post/cpp-optimization/abstraction-cost/)의 간접 호출 개념을 전제로 합니다. 람다가 `[](){}` 형태로 함수를 즉석에서 만든다는 것과 캡처(`[x]`, `[&x]`)의 의미만 알면 충분합니다.

**이 장의 깊이**: 이 장은 **중급~전문가**를 포괄합니다. 캡처 비용·클로저 객체 구조부터 시작해, 전문가 구간에서는 템플릿 전달(인라인 가능) vs `std::function` 전달(타입 소거·간접 호출)을 비교하고 콜백 설계 기준을 다룹니다. **다루지 않는 것**: `std::function`의 SBO 내부([16장](/post/cpp-optimization/small-buffer-optimization/))와 타입 소거 일반론([19장](/post/cpp-optimization/type-erasure-cost-patterns/))입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "캡처 비용" ~ "클로저 객체" | 캡처 방식과 클로저 크기 이해 |
| **중급자** | "std::function과의 비교" ~ "실무 가이드" | 템플릿 vs function 전달 선택 |
| **전문가** | "비판적 시각" | 인라인 가능성과 콜백 설계 판단 |

---

## 람다와 클로저 in C++ (역사·배경)

**람다 표현식**은 C++11에서 도입되었고, C++14에서 일반화 캡처·반환 타입 추론이, C++20에서 템플릿 람다 등이 추가되었습니다. 람다는 **클로저 객체**(캡처된 변수를 담은 익명 타입)를 생성하고, 템플릿으로 전달하면 해당 타입이 알려져 인라인되기 쉽고, **std::function**으로 전달하면 타입 소거로 인해 간접 호출·(가능하면) SBO가 적용됩니다.

## 캡처 비용

**by-value** 캡처(`[x, y]`)는 해당 변수를 <strong>클로저 객체 내부에 복사(또는 이동)</strong>합니다. 캡처된 값이 크면 클로저 크기가 커지고, 람다 생성 시점에 복사/이동 비용이 듭니다. **by-reference** 캡처(`[&x, &y]`)는 **포인터/참조 크기만** 클로저에 들어가므로 클로저가 작지만, 람다가 **참조한 객체보다 오래 살면** dangling이 됩니다. 따라서 수명이 람다보다 긴 객체만 참조로 캡처해야 합니다. `[=]`, `[&]`는 편하지만 불필요한 캡처까지 포함할 수 있으므로, 핫 경로에서는 명시적으로 나열하는 편이 의도와 비용을 파악하기 좋습니다.

## 클로저 객체

람다 표현식은 **고유한 클로저 타입**을 가지며, 그 크기는 **캡처된 멤버의 합**과 정렬에 의해 결정됩니다. 캡처가 없으면 클로저는 상태가 없지만, C++ 객체는 서로 구별되는 주소를 가져야 하므로 크기가 **0이 될 수는 없고 보통 1바이트**입니다(정확한 값은 구현 정의). 또한 **캡처 없는 람다는 함수 포인터로 암시적 변환**되므로, 저장하지 않고 바로 함수 포인터로 넘기면 클로저 객체 저장 비용 없이 쓸 수 있습니다. 캡처가 많으면 그만큼 커집니다.

아래 예시로 캡처에 따른 클로저 크기를 직접 출력해 볼 수 있습니다. 캡처 없는 클로저는 보통 1바이트, 참조 캡처는 포인터 크기, 값 캡처는 캡처된 멤버 합 + 정렬에 따라 커집니다.

```cpp
#include <cstdio>
#include <cstdint>

int main() {
    int a = 0;
    std::int64_t big = 0;

    auto none = []       { return 1; };          // 캡처 없음 → 보통 1 (구현 정의)
    auto one  = [a]      { return a; };           // int 하나 값 캡처
    auto two  = [a, big] { return a + big; };     // int + int64 값 캡처
    auto ref  = [&a]     { return a; };           // 참조 캡처 → 포인터 크기

    std::printf("none=%zu one=%zu two=%zu ref=%zu\n",
        sizeof(none), sizeof(one), sizeof(two), sizeof(ref));

    int (*fp)() = [] { return 7; };  // 캡처 없는 람다 → 함수 포인터로 변환
    std::printf("fp()=%d\n", fp());
}
```

**인라인 가능성**: 람다를 **템플릿 파라미터**로 받는 함수(예: `std::sort`의 비교자)는 **호출 시점에 람다의 구체 타입이 알려지므로** 컴파일러가 람다 본문을 인라인할 수 있습니다. 반대로 **std::function**에 람다를 담으면 **타입이 소거**되어, 호출이 **타입 소거 호출 심(call shim)을 거치는 간접 호출**(저장된 함수 포인터를 통해 디스패치; 가상 함수의 vtable이 아니라 type-erasure 메커니즘)로 이루어지고, 클로저가 크면 **힙 할당**(SBO 실패 시)도 발생할 수 있습니다.

## std::function과의 비교

**std::function**은 임의의 호출 가능 객체를 타입 소거해 하나의 타입으로 담습니다. 내부적으로는 (작은 객체면 SBO, 크면 힙에) 저장하고, 호출 시 **간접 호출**을 합니다. 그래서 **힙 할당**이 발생할 수 있고, **인라인**이 어렵습니다.

아래는 동일 로직을 템플릿으로 받는 경우와 `std::function`으로 받는 경우를 대비한 예시입니다. 템플릿 버전은 구체 클로저 타입이 유지되어 인라인될 수 있고, function 버전은 call shim을 거치는 간접 호출이 됩니다.

```cpp
#include <functional>
#include <cstdio>

template<typename F>                  // 구체 클로저 타입 유지 → 인라인 가능
void run_template(F&& f) { f(); }

void run_function(std::function<void()> f) { f(); }  // 타입 소거 → 간접 호출

int main() {
    int n = 0;
    run_template([&] { ++n; });   // ++n 이 인라인되어 직접 수행 가능
    run_function([&] { ++n; });   // call shim 통한 간접 호출
    std::printf("n=%d\n", n);
}
```

위 두 예제를 실제로 재면 자릿수 감각을 잡을 수 있습니다. 아래는 (1) `sizeof`로 본 클로저 크기와, (2) 같은 `++n` 클로저를 템플릿 vs `std::function`으로 호출했을 때의 **예시 측정값**입니다(x86-64, GCC 13, `-O2`). 크기는 대표 구현의 전형값(구현 정의), 시간은 1회 호출당 예시이며 상대 배수만 의미가 있습니다.

| 측정 | 값(예시) | 메모 |
|---|---|---|
| `sizeof` 캡처 없는 클로저 | 1 바이트 | 상태 없음, 함수 포인터로 변환 가능 |
| `sizeof` `[a]`(int 캡처) | 4 바이트 | 캡처 멤버 크기 |
| `sizeof` `[a, big]`(int+int64) | 16 바이트 | 정렬 패딩 포함 |
| `sizeof` `[&a]`(참조 캡처) | 8 바이트 | 포인터 한 개 |
| 템플릿 `F&&`로 호출(인라인됨) | ~0.3 ns | 본문이 호출부에 펼쳐짐 |
| `std::function`으로 호출(SBO 적중) | ~2 ns | call shim 간접 호출, 인라인 차단 |

핵심은 **할당이 없어도** `std::function` 경로가 느릴 수 있다는 점입니다(작은 클로저는 SBO에 들어가 힙을 쓰지 않음). 비용의 주범은 힙이 아니라 **간접 호출이 인라이닝을 막는 것**이며, 캡처가 SBO 한도를 넘으면 여기에 **호출 시점 힙 할당**까지 더해집니다(챕터 16). 따라서 "function에 담아도 작으니 괜찮다"는 직관은 핫 루프에서 깨질 수 있습니다.

## 실무 가이드

- **핫패스**에서는 받는 쪽이 **템플릿 파라미터로 구체 클로저 타입을 받도록**(예: `template<class F> void run(F&& f)`) 설계해 타입 소거를 피하고 인라인을 유도합니다. 핵심은 "값으로 전달"이 아니라 **`std::function`으로 타입을 소거하지 않는 것**입니다.
- **캡처 크기**가 크면(예: 큰 구조체), 값 캡처는 클로저를 비대하게 만들므로, **참조로 캡처**하되 람다 수명이 참조 대상보다 짧음을 보장하거나, **포인터/참조만** 캡처해 크기를 줄입니다.
- **람다 vs std::function**은 같은 로직으로 마이크로벤치마크를 돌려 호출 비용·할당 유무를 확인한 뒤, 핫 경로에서는 람다+템플릿 조합을 선택하는 것이 안전합니다.

## 비판적 시각: 한계와 트레이드오프

- **std::function**은 타입 소거가 필요할 때(저장·다형 콜백) 유용합니다. "무조건 람다만"이 아니라, 저장·전달 경로가 핫하지 않으면 std::function도 선택지입니다.
- 참조 캡처 시 **dangling**을 피하려면 람다 수명이 참조 대상보다 짧음을 보장해야 합니다.

## 핵심 요약

| 항목 | 비용·이점 | 활용 기준 |
|------|-----------|-----------|
| 람다(템플릿으로 받음) | 인라인 가능, 할당 없음 | 핫패스 콜백 |
| std::function | call shim 간접 호출, SBO/힙 | 저장·다형 콜백 |
| 캡처 | value=복사·크기, ref=수명 주의 | 크기·수명에 맞게 |

### 자주 묻는 질문 (FAQ)

**Q: 람다 vs std::function 성능?**  
A: 람다(클로저)는 구체 타입이라 인라인 가능하고, std::function은 타입 소거로 간접 호출·SBO 여부에 따라 할당이 있을 수 있어 상대적으로 느립니다. 핫패스에는 템플릿으로 람다를 받는 것이 유리합니다.

**Q: by-value vs by-reference 캡처?**  
A: by-value는 복사 비용·클로저 크기 증가, by-reference는 수명 주의(람다가 참조보다 오래 살지 않게)가 필요합니다. 작은 값은 value, 큰 값·수명 이슈가 있으면 ref 또는 포인터/span을 씁니다.

**Q: std::function이 느린 이유는?**  
A: 타입 소거로 인라인되지 않고, 작은 객체는 SBO로 힙 할당을 피할 수 있으나(챕터 16) 호출은 항상 간접입니다. 템플릿으로 구체 타입을 받으면 인라인됩니다.

### 적용 체크리스트

- [ ] 핫패스에서 std::function 대신 템플릿으로 람다를 받았는가?
- [ ] 캡처는 by-value/by-ref를 크기·수명에 맞게 선택했는가?
- [ ] 클로저 크기·인라인 가능 여부를 벤치마크했는가?
- [ ] SBO 한계(챕터 16)를 인지하고 큰 클로저 시 function 할당을 고려했는가?

### 더 읽을 거리

- [cppreference: 람다 표현식](https://en.cppreference.com/w/cpp/language/lambda) — 캡처 절 문법, 클로저 타입 규칙, C++20 템플릿 람다까지 언어 표준 명세를 확인할 수 있습니다.
- [cppreference: std::function](https://en.cppreference.com/w/cpp/utility/functional/function) — 타입 소거 호출 래퍼의 정확한 인터페이스와 SBO 관련 노트(구현 정의)를 확인할 수 있습니다.

## 다음 장에서는

**이전 장**: [std::span과 뷰 패턴](/post/cpp-optimization/span-and-views/) (챕터 14)

**Small Buffer Optimization**을 다룹니다. SBO 패턴과 std::function·std::any 내부 구조, 작은 객체일 때 힙 할당을 피하는 메커니즘을 정리합니다. → [Small Buffer Optimization](/post/cpp-optimization/small-buffer-optimization/) (챕터 16)
