---
title: "[Cpp] = default와 {} 생성자는 다르다: GCC 15·16에서 4.5배 느려진 사례"
description: "span() = default와 span() {}는 같아 보이지만 triviality와 값 초기화가 다르다. Lemire가 보고한 GCC 15·16의 약 4.5배 차이(7.75–8.04 ns vs 1.73 ns)를 의미론부터 정리한다."
date: 2026-11-05T00:30:00+09:00
lastmod: 2026-11-05
draft: false
categories:
  - Cpp
  - Optimization
tags:
  - C++
  - Compiler(컴파일러)
  - Optimization(최적화)
  - Performance(성능)
  - Benchmark
  - Benchmark(벤치마크)
  - Assembly
  - Assembly(어셈블리)
  - Memory(메모리)
  - Latency
  - Throughput
  - CPU
  - Case-Study
  - Deep-Dive
  - Best-Practices
  - Testing(테스트)
  - Profiling(프로파일링)
  - Software-Engineering(소프트웨어공학)
  - Init(초기화)
  - Daniel-Lemire
  - GCC
  - Clang
  - Constructor(생성자)
  - Trivial-Type
  - Value-Initialization
  - Code-Generation
  - Performance-Regression
  - Compiler-Optimization
  - Open-Source(오픈소스)
  - Cpp-Performance
image: "wordcloud.png"
---

C++에서 "아무것도 하지 않는 기본 생성자"를 쓰는 방법은 두 가지다. `span() = default;`와 `span() {}`. 대부분의 코드베이스에서는 취향 문제로 취급되지만, Daniel Lemire는 2026년 11월 2일 블로그에서 이 둘이 GCC 15와 16에서 약 4.5배의 성능 차이를 만든 사례를 공개했다. 이 글은 그 측정치를 인용하고, 왜 두 선언이 의미론적으로 다른지를 먼저 정리한다.

## 두 선언은 타입의 성질을 바꾼다

핵심은 **첫 선언에 `= default`를 쓰면 생성자가 user-provided가 아니다**라는 점이다. 이 경우 멤버가 모두 trivial이면 타입은 **trivially default constructible**을 유지한다. 반면 `{}`로 본문을 직접 쓰면 비어 있어도 user-provided 생성자가 되어 타입은 trivial이 아니다.

```cpp
#include <cstddef>
#include <type_traits>

struct span_default {
    const char* start;
    std::size_t length;
    span_default() = default;
    span_default(const char* s, std::size_t n) : start(s), length(n) {}
};

struct span_braces {
    const char* start;
    std::size_t length;
    span_braces() {}
    span_braces(const char* s, std::size_t n) : start(s), length(n) {}
};

static_assert(std::is_trivially_default_constructible_v<span_default>);
static_assert(!std::is_trivially_default_constructible_v<span_braces>);
```

위 코드는 이 글을 위해 만든 최소 예시이며 Lemire의 벤치마크 코드가 아니다. 두 타입의 차이는 컴파일 타임에 검사된다. 이 차이가 코드젠에 영향을 줄 수 있다는 점이 이 사례의 요점이다.

## 값 초기화에서 갈리는 동작

초기화 문법에 따라 결과가 달라진다. Lemire의 정리를 표로 옮기면 다음과 같다.

| 선언 | `span s;` | `span s{};` |
|---|---|---|
| `span() = default;` | 멤버 미초기화 | 패딩 포함 객체 전체를 0으로 채움(생성자는 실행되지 않음) |
| `span() {}` | 빈 생성자 호출(컴파일러가 제거 가능), 멤버 미초기화 | 빈 생성자 호출, 0으로 채우지 않음 |

`= default` 쪽의 `span s{};`는 값 초기화(value-initialization) 규칙에 따라 제로 초기화가 먼저 일어난다. `{}` 쪽은 생성자가 user-provided이므로 제로 초기화 단계가 없다. 따라서 멤버 이니셜라이저 `s()`나 `T{}`처럼 값 초기화가 끼는 코드 경로에서는 컴파일러가 해야 할 일이 달라진다.

```cpp
span_default a{};
// a.start == nullptr, a.length == 0 이 보장된다.

span_braces b{};
// 생성자가 아무것도 쓰지 않으므로 b.start, b.length를 읽으면 불확정 값이다.
```

## 측정 결과

Lemire의 측정 조건은 Intel Xeon Gold 6548N(Emerald Rapids) 한 코어, `-O2 -march=x86-64`, 1억 개의 span, 5회 실행 중 최고 기록이다. 그는 `span`을 `box` 타입으로 감싸고, 값 초기화된 box 또는 span을 담은 box를 대입하는 루프를 돌렸다.

| 컴파일러 | `span() = default` | `span() {}` |
|---|---|---|
| GCC 14.3 | 1.73 ns/span | 1.74 ns/span |
| GCC 15.2 | 7.75 ns/span | 1.73 ns/span |
| GCC 16.2 | 8.04 ns/span | 1.73 ns/span |
| clang 21 | 1.75 ns/span | 1.74 ns/span |

GCC 15.2와 16.2에서만 `= default` 버전이 약 4.5배 느리다(7.75÷1.73≈4.5, 8.04÷1.73≈4.6). GCC 14.3과 clang 21에서는 차이가 없다. 즉 이 현상은 언어 규칙이 만든 필연이 아니라 특정 컴파일러 버전의 코드젠 선택이다.

## 어셈블리에서 보이는 차이

Lemire가 GCC 16의 출력을 비교한 설명에 따르면, `{}` 버전은 세 필드를 `consume`이 읽는 메모리에 곧바로 쓴다. `= default` 버전은 시작 포인터와 길이를 스택의 임시 객체를 거치게 한 뒤 16바이트를 복사해 오는 경로가 생긴다. 불필요한 임시 객체 한 번의 왕복이 비용 차이를 설명하는 그림으로 보인다. 다만 원문은 GCC 내부의 근본 원인까지는 밝히지 않으며, 이 글도 추측하지 않는다.

## 이 사례에서 가져갈 것

- **일반 규칙으로 읽지 않는다.** "`{}`가 더 빠르다"가 아니라 "특정 타입·컴파일러 범위에서 `{}` 선택이 4.5배 회귀를 피했다"는 관측이다. clang 21과 GCC 14.3에서는 두 선언이 동일하다.
- **trivial 여부는 의도된 설계 선택이다.** `= default`로 trivial 타입을 유지하면 `memcpy` 가능성이나 제로 초기화 같은 이점이 생기므로, 성능 이유 하나로 `{}`로 바꾸기 전에 그 이점을 잃는지 확인해야 한다.
- **컴파일러 업그레이드 때 마이크로벤치마크를 돌린다.** 작은 값 타입이 핫 루프에 있다면 GCC 14에서 15로 올릴 때 같은 소스가 4배 이상 느려질 수 있다. 업그레이드 CI에 해당 루프의 벤치마크를 넣어 두면 이런 회귀를 일찍 잡는다.
- **측정 주체의 한계를 기억한다.** 위 수치는 한 대의 머신, 한 벤치마크, 5회 중 최고 기록이다. 다른 CPU나 다른 호출 패턴에서 같은 배율이 나온다는 보장은 없다.

## 참고 및 출처

- Daniel Lemire, "In C++, = default and {} are not the same constructor" (2026-11-02): <https://lemire.me/blog/2026/11/02/default-and-braces-are-not-the-same-constructor/>
