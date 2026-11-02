---
collection_order: 15
date: 2026-03-10
lastmod: 2026-10-21
draft: false
image: wordcloud.png
title: "[Optimization(C++) 15] 람다 표현식 성능"
slug: lambda-performance
description: "람다의 캡처 비용(by-value vs by-reference), 클로저 객체 크기·정렬, 인라이닝 가능성 등 성능 특성을 다룹니다. std::function과의 비교 및 콜백·알고리즘 전달 시 비용을 정리하고, 타입 소거 vs 템플릿 전달의 트레이드오프를 제시합니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Functional-Programming(함수형프로그래밍)
  - Memory(메모리)
  - Compiler(컴파일러)
  - Implementation(구현)
  - Code-Quality(코드품질)
  - Best-Practices
  - Clean-Code(클린코드)
  - Type-Safety
  - Readability
  - Maintainability
  - Modularity
  - Abstraction(추상화)
  - Advanced
  - Deep-Dive
  - 실습
  - Guide(가이드)
  - Reference(참고)
  - Edge-Cases(엣지케이스)
  - Pitfalls(함정)
  - Comparison(비교)
  - Closure(클로저)
  - Assembly(어셈블리)
  - Heap(힙)
  - Lambda
  - std-function
  - Type-Erasure
  - Inlining
  - Callback
  - SBO
---

**람다 성능**은 캡처 방식·클로저 크기·전달 방식(템플릿 vs std::function)에 따라 달라집니다. 본 챕터에서는 **by-value vs by-reference** 캡처 비용, 클로저 객체 크기·인라이닝 가능성, **std::function**과의 비교 및 콜백·알고리즘 전달 시 비용을 정리합니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [03장: 추상화 비용 분석](/post/cpp-optimization/abstraction-cost/)의 간접 호출 개념을 전제로 합니다. 람다가 `[](){}` 형태로 함수를 즉석에서 만든다는 것과 캡처(`[x]`, `[&x]`)의 의미만 알면 충분합니다.

**이 장의 깊이**: 이 장은 **중급–전문가**를 포괄합니다. 캡처 비용·클로저 객체 구조부터 시작해, 전문가 구간에서는 템플릿 전달(인라인 가능) vs `std::function` 전달(타입 소거·간접 호출)을 비교하고 콜백 설계 기준을 다룹니다. **다루지 않는 것**: `std::function`의 SBO 내부([16장](/post/cpp-optimization/small-buffer-optimization/))와 타입 소거 일반론([19장](/post/cpp-optimization/type-erasure-cost-patterns/))입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "캡처 비용" ~ "클로저 객체" | 캡처 방식과 클로저 크기 이해 |
| **중급자** | "std::function과의 비교" ~ "실무 가이드" | 템플릿 vs function 전달 선택 |
| **전문가** | "비판적 시각" | 인라인 가능성과 콜백 설계 판단 |

---

## 람다와 클로저 in C++ (역사·배경)

**람다 표현식**은 C++11에서 도입되었고, C++14에서 초기화 캡처(일반화 캡처)·제네릭 람다와 반환 타입 추론의 확장이, C++20에서 템플릿 람다 등이 추가되었습니다. 람다는 **클로저 객체**(캡처된 변수를 담은 익명 타입)를 생성하고, 템플릿으로 전달하면 해당 타입이 알려져 인라인되기 쉽고, **std::function**으로 전달하면 타입 소거로 인해 간접 호출·(가능하면) SBO가 적용됩니다.

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

**인라인 가능성**: 람다를 **템플릿 파라미터**로 받는 함수(예: `std::sort`의 비교자)는 **호출 시점에 람다의 구체 타입이 알려지므로** 컴파일러가 람다 본문을 인라인할 수 있습니다. 반대로 **std::function**에 람다를 담으면 **타입이 소거**되어, 호출이 **타입 소거된 디스패치 경로를 거치는 간접 호출**로 이루어지고, 클로저가 크면 std::function을 만들 때 **힙 할당**(SBO 실패 시)도 발생할 수 있습니다. 아래에서 실제 어셈블리로 확인합니다.

## std::function과의 비교

**std::function**은 임의의 호출 가능 객체를 타입 소거해 하나의 타입으로 담습니다. 내부적으로는 작은 객체면 객체 안의 버퍼(SBO)에, 크면 힙에 저장하고, 호출은 저장해 둔 디스패치 경로를 거치는 **간접 호출**이 됩니다. 디스패치 방식은 구현마다 다릅니다. libstdc++는 객체 안에 저장한 함수 포인터(호출 심)를 부르고, libc++의 기본 구현은 내부 기반 클래스 `__base`의 가상 함수 `operator()`를 부릅니다. 어느 쪽이든 호출부에서는 실제 클로저 타입이 보이지 않으므로 인라인이 어렵고, 힙 할당이 필요한 경우 그 비용은 **std::function을 생성하거나 복사할 때** 발생합니다.

아래 예제는 같은 로직(`i * k`를 1000번 더하기)을 템플릿으로 받는 함수와 `std::function`으로 받는 함수에 각각 넘깁니다. 두 함수에 `noinline`을 붙여 호출부 인라인을 막고, 함수 본문 안에서 람다 호출이 어떻게 컴파일되는지만 비교합니다.

```cpp
#include <functional>

template<typename F>
__attribute__((noinline)) int run_template(F&& f, int n) {
    int s = 0;
    for (int i = 0; i < n; ++i) s += f(i);   // 구체 클로저 타입 → 인라인 가능
    return s;
}

__attribute__((noinline)) int run_function(const std::function<int(int)>& f, int n) {
    int s = 0;
    for (int i = 0; i < n; ++i) s += f(i);   // 타입 소거 → 매 반복 간접 호출
    return s;
}

int main(int argc, char**) {
    int k = argc;
    return run_template([k](int i) { return i * k; }, 1000)
         + run_function([k](int i) { return i * k; }, 1000);
}
```

GCC 14.2 `-std=c++17 -O2`(x86-64, Compiler Explorer)로 컴파일하면 차이가 극명합니다. 템플릿 버전은 람다 본문이 루프 안으로 펼쳐진 뒤 루프 전체가 닫힌 식(0부터 999까지의 합 499500에 `k`를 곱하기)으로 접혀, 함수 본문이 명령 두 개만 남습니다. `std::function` 버전은 반복마다 "대상이 비어 있는가" 검사와 객체 안에 저장된 포인터를 통한 간접 호출을 수행합니다(발췌).

```text
; run_template (상수 전파된 복제본) — 루프가 사라짐
        imul    eax, edi, 499500
        ret

; run_function — 루프 본문 발췌
.L23:
        cmp     QWORD PTR [rbp+16], 0        ; 빈 std::function인지 검사
        mov     DWORD PTR [rsp+12], ebx
        je      .L26                          ; 비어 있으면 bad_function_call 경로
        mov     rsi, r14
        mov     rdi, rbp
        add     ebx, 1
        call    [QWORD PTR [rbp+24]]          ; 저장된 호출 심을 통한 간접 호출
        add     r12d, eax
        cmp     r13d, ebx
        jne     .L23
```

이 예제의 클로저는 `int` 하나만 캡처하므로 SBO에 들어가 힙 할당이 전혀 없습니다. 그런데도 차이가 이만큼 납니다. 즉 `std::function` 경로의 주된 비용은 힙이 아니라 **간접 호출이 인라이닝과 그 뒤의 최적화(루프 접기, 벡터화)를 막는 것**이며, 캡처가 SBO 한도를 넘으면 여기에 생성·복사 시점의 힙 할당이 더해집니다([16장](/post/cpp-optimization/small-buffer-optimization/)). 다만 이 결과를 "항상 간접"으로 일반화할 수는 없습니다. `std::function`을 만드는 곳과 호출하는 곳이 한 번역 단위 안에서 함께 보이고 인라인되면, 컴파일러가 저장된 대상을 추적해 간접 호출을 없애기도 합니다. 위 예제에서 `noinline`을 붙인 것도 이 효과를 배제하고 경계 너머의 일반적인 경우를 보이기 위해서입니다.

## 흔한 오해

<strong>"캡처 없는 람다는 0바이트다"</strong>는 틀렸습니다. 앞의 클로저 크기 예제처럼 캡처가 없어도 클로저 객체는 고유한 주소를 가져야 하므로 크기가 1 이상입니다. 비용이 0에 가까운 것은 크기 때문이 아니라, 상태가 없어 함수 포인터로 변환되거나 통째로 인라인되기 때문입니다.

<strong>"std::function은 항상 힙을 쓴다"</strong>도 틀렸습니다. 표준은 대상이 함수 포인터나 `std::reference_wrapper`일 때 객체 안에 직접 저장해 동적 할당을 하지 않도록 보장하며, 구현들은 그 밖의 작은 클로저도 내부 버퍼에 담습니다. 위 예제처럼 힙 할당이 없어도 느릴 수 있다는 점이 오히려 더 중요한 사실입니다.

<strong>"참조 캡처는 항상 값 캡처보다 싸다"</strong>도 경우에 따라 다릅니다. 참조 캡처는 클로저 크기를 포인터 하나로 줄이지만, 람다 본문이 그 값을 읽을 때마다 메모리를 거쳐야 하고, 컴파일러가 다른 쓰기와의 별칭(aliasing) 가능성 때문에 값을 레지스터에 묶어 두지 못할 수 있습니다. `int`·`double`처럼 작은 값은 값 캡처가 클로저 크기를 거의 늘리지 않으면서 이런 문제를 피하므로 대개 더 낫습니다.

## 실무 가이드

핫패스에서는 콜백을 받는 쪽이 `template<class F> void run(F&& f)`처럼 **템플릿 파라미터로 구체 클로저 타입을 받도록** 설계합니다. 핵심은 "값으로 전달"이 아니라 `std::function`으로 타입을 소거하지 않는 것이며, 그래야 위 예제처럼 람다 본문이 호출부에 펼쳐지고 후속 최적화가 이어집니다. 반대로 콜백을 멤버에 저장하거나, 서로 다른 람다를 한 컨테이너에 담거나, 헤더에 템플릿을 노출하고 싶지 않은 API 경계라면 `std::function`이 합리적인 선택입니다. 판단 기준은 "그 호출이 얼마나 자주 일어나는가"이며, 이벤트 핸들러 등록처럼 드문 경로라면 `std::function`의 비용은 측정되지 않을 만큼 작습니다.

캡처는 크기와 수명을 함께 보고 고릅니다. 큰 구조체를 값으로 캡처하면 클로저가 커지고 생성 시 복사가 일어나며, `std::function`에 담을 때 SBO 한도를 넘어 힙 할당까지 유발할 수 있습니다. 이때는 참조나 포인터로 캡처해 크기를 줄이되, 람다가 참조 대상보다 오래 살지 않음을 보장해야 합니다. 람다를 비동기 작업이나 다른 스레드로 넘겨 수명이 길어진다면 참조 캡처 대신 `[data = std::move(data)]` 같은 초기화 캡처(C++14)로 소유권을 클로저에 넘기는 것이 안전합니다.

## 비판적 시각: 한계와 트레이드오프

템플릿으로 람다를 받는 설계는 호출 비용을 없애는 대신 다른 비용을 치릅니다. 서로 다른 람다마다 함수가 따로 인스턴스화되므로 코드 크기와 컴파일 시간이 늘고, 구현을 헤더에 노출해야 하며, 콜백 타입이 함수 시그니처에 드러나지 않아 인터페이스를 읽기 어려워집니다. 그래서 "핫 경로는 템플릿, 저장·다형 콜백은 std::function"이라는 이분법이 현실적인 절충입니다.

`std::function` 자체의 한계를 줄이는 표준 대안도 나왔습니다. C++23의 `std::move_only_function`은 복사 불가능한 클로저(예: `unique_ptr`을 캡처한 람다)를 담을 수 있고, `const` 정확성을 시그니처에 반영합니다. 다만 둘 다 타입 소거라는 점은 같아서, 이 장에서 본 간접 호출 비용은 그대로 남습니다.

## 핵심 요약

| 항목 | 비용·이점 | 활용 기준 |
|------|-----------|-----------|
| 람다(템플릿으로 받음) | 인라인 가능, 할당 없음 | 핫패스 콜백 |
| std::function | 간접 호출(구현별 디스패치), SBO/힙 | 저장·다형 콜백 |
| 캡처 | value=복사·크기, ref=수명 주의 | 크기·수명에 맞게 |

## 이 글을 읽은 후 달성해야 할 목표

이 장을 마치면 람다를 "편한 문법"이 아니라 "클로저 타입과 전달 방식에 따라 비용이 갈리는 객체"로 다룰 수 있어야 합니다.

- 캡처 방식에 따른 클로저 크기를 `sizeof`로 확인하고, 값/참조 캡처를 크기·수명·별칭 관점에서 고를 수 있다.
- 템플릿 전달과 `std::function` 전달의 차이를 생성된 어셈블리(인라인·루프 접기 vs 간접 호출)로 설명할 수 있다.
- `std::function`의 힙 할당이 생성·복사 시점에 일어나며, 할당이 없어도 인라인 차단 비용이 남는다는 점을 콜백 설계에 반영할 수 있다.

### 적용 체크리스트

- [ ] 핫패스 콜백을 템플릿 파라미터로 받았는가? — 타입 소거가 없어야 람다 본문이 인라인된다.
- [ ] 수명이 호출을 넘는 람다에서 참조 캡처를 없앴는가? — 비동기·저장 콜백의 참조 캡처는 dangling이 된다.
- [ ] `std::function`에 담는 클로저의 캡처 크기를 확인했는가? — SBO 한도를 넘으면 생성·복사마다 힙 할당이 붙는다.

### 더 읽을 거리

- [cppreference: 람다 표현식](https://en.cppreference.com/w/cpp/language/lambda) — 캡처 절 문법, 클로저 타입 규칙, C++20 템플릿 람다까지 언어 표준 명세를 확인할 수 있습니다.
- [cppreference: std::function 생성자](https://en.cppreference.com/w/cpp/utility/functional/function/function) — 함수 포인터·`reference_wrapper` 대상에 대한 소형 객체 최적화 보장과, 그 밖의 대상은 동적 할당될 수 있다는 노트를 확인할 수 있습니다.

## 다음 장에서는

**이전 장**: [std::span과 뷰 패턴](/post/cpp-optimization/span-and-views/) (챕터 14)

**Small Buffer Optimization**을 다룹니다. SBO 패턴과 std::function·std::any 내부 구조, 작은 객체일 때 힙 할당을 피하는 메커니즘을 정리합니다. → [Small Buffer Optimization](/post/cpp-optimization/small-buffer-optimization/) (챕터 16)
