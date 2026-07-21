---
collection_order: 6
date: 2026-03-10
lastmod: 2026-07-10
draft: false
image: wordcloud.png
title: "[Optimization(C++) 06] 객체 수명 최적화"
slug: object-lifetime
description: "Copy Elision, RVO/NRVO, 이동 의미론을 심화하여 객체 수명·복사/이동 비용을 제어하는 방법을 다룹니다. 반환값 최적화와 move semantics가 성능에 미치는 영향을 마이크로벤치마크로 검증하고, 언제 이동을 쓸지·회피할지 판단 기준을 제시합니다."
tags:
  - C++
  - Performance
  - Optimization
  - 성능
  - 최적화
  - Memory
  - 메모리
  - Compiler
  - 컴파일러
  - OOP
  - 객체지향
  - Data-Structures
  - 자료구조
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
  - Space-Complexity
  - 공간복잡도
  - Type-Safety
  - Readability
  - Maintainability
  - Modularity
  - Refactoring
  - 리팩토링
  - Testing
  - 테스트
  - Debugging
  - 디버깅
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
  - Composition
  - 합성
  - Documentation
  - 문서화
---

**객체 수명 최적화**란 반환·전달 시 불필요한 복사와 임시 생성을 줄여 생성/이동 비용을 제어하는 것을 말합니다. 본 챕터에서는 **Copy Elision**, **RVO/NRVO**, **이동 의미론**을 심화하여 반환값 최적화와 move semantics가 성능에 미치는 영향을 마이크로벤치마크로 검증하는 방법을 다룹니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [03장: 추상화 비용 분석](/post/cpp-optimization/abstraction-cost/)의 측정 흐름을 전제로 합니다. 복사 생성자·이동 생성자가 무엇인지, 함수가 객체를 값으로 반환한다는 것이 무슨 뜻인지 정도만 알면 충분합니다.

**이 장의 깊이**: 이 장은 **중급–전문가**를 포괄합니다. Copy Elision·RVO/NRVO의 동작부터 시작해, 전문가 구간에서는 생성자 카운터로 복사·이동·생략을 실제로 계측하고 이동 의미론을 핫패스에 적용하는 기준을 다룹니다. **다루지 않는 것**: 임시 객체 제거 패턴(이어지는 [07장](/post/cpp-optimization/temporary-removal/))과 인자 전달 전략([17장](/post/cpp-optimization/parameter-passing/))입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "Copy Elision" ~ "RVO / NRVO" | 반환값 최적화가 복사를 없애는 원리 이해 |
| **중급자** | "이동 의미론 심화" ~ "계측 예제: RVO vs 이동 vs 복사 (생성자 카운터)" | 복사·이동·생략을 직접 계측 |
| **전문가** | "판단 기준" ~ "비판적 시각" | 이동/RVO 보장 조건과 적용 판단 |

---

## 반환값 최적화와 이동 의미론 (역사·배경)

**RVO/NRVO**는 C++98 시대부터 컴파일러가 적용해 오던 최적화였고, C++11에서 **이동 의미론**(rvalue reference, `std::move`)이 도입되면서 "복사 대신 이동"이 표준화되었습니다. C++17에서는 **mandatory copy elision**으로 prvalue 반환 시 복사/이동을 생략하는 것이 언어 규칙이 되었고, 이로써 반환값으로 큰 객체를 넘길 때의 비용을 이론적으로 제거할 수 있게 되었습니다.

> "When a prvalue of class type X is used to initialize an object of the same type X, the copy/move construction may be omitted to construct the result object directly." — [cppreference: Copy elision](https://en.cppreference.com/w/cpp/language/copy_elision) 문서 (ISO C++ 표준 기반). C++17부터 일부 경우 elision이 "선택"이 아니라 "필수"입니다.

## Copy Elision

C++17부터 <strong>prvalue(순수 우측값)</strong>는 "임시를 물리적으로 만들지 않고 곧바로 최종 목적지에 초기화한다"는 의미론을 갖습니다. 함수가 prvalue를 반환할 때, 컴파일러는 **반드시** 그 반환값을 호출 측의 객체에 직접 구성하며, 이때 "복사/이동"은 개념적으로만 존재하고 실제로는 한 번의 구성만 일어납니다. 이를 **강제 copy elision**이라고 합니다.

## RVO / NRVO

<strong>RVO(Return Value Optimization)</strong>는 함수가 임시 객체를 반환할 때(예: `return T(a, b);`) 그 임시를 호출자의 메모리 위치에 직접 만드는 최적화입니다. <strong>NRVO(Named Return Value Optimization)</strong>는 함수 내부에 **이름 있는** 로컬 객체를 두고 그걸 반환할 때(예: `T result; ... return result;`) 그 로컬 객체를 호출자의 반환값 위치에 직접 구성하는 최적화입니다.

NRVO는 **분기**가 있거나 **여러 return 문**이 서로 다른 로컬 객체를 가리키면 적용되지 않을 수 있습니다. 반환 경로를 단순하게 유지하고, 가능하면 단일 `return result;` 형태로 두는 것이 NRVO 확률을 높입니다.

```cpp
// 적용 잘 됨: 단일 return, 같은 타입 prvalue 또는 named object
Widget make()       { return Widget{}; }        // RVO
Widget make_named() { Widget w; return w; }      // NRVO

// 적용 제한될 수 있음: 분기로 서로 다른 객체 반환
Widget make(bool flag) { Widget w1, w2; return flag ? w1 : w2; }  // NRVO 어려움
```

## 이동 의미론 심화

이동(move)은 **리소스를 복사하지 않고 "훔쳐 오는"** 동작입니다. `void f(T&& t)`에 `std::move(x)`나 임시를 넘기면 이동 생성/대입이 사용되고, 함수가 값으로 반환할 때 로컬 변수는 컴파일러가 rvalue로 처리해 이동을 선택할 수 있습니다(또는 RVO/NRVO로 아예 제거).

표준에 따르면 이동된 **후**의 객체는 **valid but unspecified** 상태입니다. 소멸자 호출과 대입은 안전하지만, 그 외 사용은 구현/계약에 의존합니다. 복사 제거가 불가능할 때의 우선순위는 보통 **RVO/NRVO → 이동 → 복사**입니다.

과거에는 "값 반환 시 `std::move`로 감싸서 반환해야 한다"는 말이 있었지만, `return std::move(local);`을 쓰면 "이동될 대상"이 되어 일부 컴파일러에서 **NRVO가 깨집니다**. 따라서 그냥 **`return local;`**으로 두고, RVO/NRVO와 이동을 컴파일러에게 맡기는 것이 올바른 관례입니다.

## 계측 예제: RVO vs 이동 vs 복사 (생성자 카운터)

`Widget`에 정적 카운터를 두면 RVO/NRVO·이동·복사 중 무엇이 일어났는지 호출 횟수로 직접 확인할 수 있습니다. 아래는 그대로 컴파일·실행할 수 있습니다(`-std=c++17 -O2`).

```cpp
#include <iostream>
#include <utility>
#include <vector>

struct Widget {
  static int ctor, copy, move;
  std::vector<int> data;

  Widget() : data(1000) { ++ctor; }
  Widget(const Widget& o) : data(o.data) { ++copy; }
  Widget(Widget&& o) noexcept : data(std::move(o.data)) { ++move; }
  Widget& operator=(const Widget&) = default;
  Widget& operator=(Widget&&) noexcept = default;
};
int Widget::ctor = 0, Widget::copy = 0, Widget::move = 0;

Widget make_rvo()   { return Widget{}; }          // RVO: 추가 ctor 0
Widget make_nrvo()  { Widget w; return w; }       // NRVO: 추가 ctor 0
Widget make_moved() { Widget w; return std::move(w); } // NRVO 깨짐 → 이동 1회

static void reset() { Widget::ctor = Widget::copy = Widget::move = 0; }
static void report(const char* tag) {
  std::cout << tag << ": ctor=" << Widget::ctor
            << " copy=" << Widget::copy
            << " move=" << Widget::move << '\n';
}

int main() {
  reset(); Widget a = make_rvo();   report("RVO");   // ctor=1 copy=0 move=0
  reset(); Widget b = make_nrvo();  report("NRVO");  // ctor=1 copy=0 move=0
  reset(); Widget c = make_moved(); report("moved"); // ctor=1 copy=0 move=1

  reset();
  Widget src;                 // ctor=1
  Widget cp = src;            // 복사 경로: copy=1
  Widget mv = std::move(src); // 이동 경로: move=1
  report("copy/move");        // ctor=1 copy=1 move=1
}
```

`RVO`/`NRVO`는 생성자 1회(기본 생성)만 일어나고 복사·이동이 0인 반면, `make_moved`는 NRVO가 깨져 이동이 1회 추가됩니다. 이것이 `return std::move(local)`을 피해야 하는 이유입니다. (측정값은 컴파일러·플래그에 따라 다를 수 있으나, C++17에서 RVO 경로의 추가 생성자 0회는 보장됩니다.)

## 평가 기준 (학습 성과 목표)

- **Copy Elision**(C++17 강제), **RVO**, **NRVO**의 조건과 "반환 위치에 직접 구성" 의미를 설명할 수 있다.
- 이동 의미론(리소스 훔치기, valid but unspecified)과 반환 시 선택 순서(RVO/NRVO → 이동 → 복사)를 구분할 수 있다.
- `return std::move(local)`이 NRVO를 깨는 이유를 설명하고, 값 반환 시 `return local`만 쓰는 관례를 적용할 수 있다.
- 복사/이동/RVO 세 가지 형태로 생성자 카운터·벤치마크를 나누어 호출 횟수와 실행 시간을 검증할 수 있다.

## 판단 기준 (언제 쓰고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 함수가 값 반환 | 값 반환 `T f()` + 단일 return | `return std::move(local)` |
| 호출자가 반환값 받기 | `T result = f();` (RVO 활용) | 불필요한 참조·포인터 반환 |
| 이동 가능한 타입 | 이동 생성자/대입 `noexcept` | 이동 후 사용 전제로 남기기 |
| 복잡한 반환 경로 | 단일 return으로 단순화 | 여러 return·분기 유지 |

### 자주 하는 실수

- **`return std::move(local)` 사용**: NRVO를 깨뜨림. `return local`만 사용.
- **참조로 반환**: 로컬 객체를 `const T&`로 반환하면 댕글링 참조(미정의 동작). 값 반환으로 바꾸고 RVO를 활용한다.
- **여러 return 경로**: 각 경로에서 다른 로컬을 반환하면 NRVO가 적용되지 않을 수 있으므로, 단일 return으로 정리할 수 있는지 검토한다.
- **이동 후 재사용**: valid but unspecified이므로 소멸·대입 외에는 문서화된 계약이 없으면 재사용하지 않는다.

### 리팩토링 시 주의

참조나 포인터로 반환하던 API를 값 반환으로 바꾸면, 호출자가 `T result = f();`로 받아 RVO를 활용할 수 있습니다. 단, 기존에 `const T&` 등으로 받던 코드는 수정이 필요할 수 있으므로, 호출처를 함께 점검하고 벤치마크로 회귀를 확인합니다.

## 비판적 시각: 한계와 트레이드오프

- **NRVO**: 분기·여러 return 대상이 있으면 적용되지 않을 수 있다. 복잡한 경로는 이동에 의존하게 되며, 이동이 저렴한 타입이면 여전히 수용 가능하다.
- **이동 후 객체**: "valid but unspecified"이므로, 이동 후 재사용 계약을 문서화하고 소멸·대입만 허용하는 것이 안전하다.
- **이동 불가 타입**: 복사만 가능한 타입은 값 반환 시 복사가 선택될 수 있어, 반환 횟수가 많은 경로에서는 out 인자를 고려할 수 있다. 다만 RVO가 적용되면 복사가 생략되므로 먼저 반환 경로를 단순화한다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| Copy Elision | prvalue는 최종 목적지에 직접 구성, 복사/이동 개념적만 존재 |
| RVO/NRVO | 반환 시 호출자 위치에 직접 구성, `return local` 유지 |
| 이동 | 리소스 훔치기, RVO 불가 시 이동이 다음 선택 |
| 금기 | `return std::move(local)` → NRVO 깨짐 |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **RVO** | Return Value Optimization; 임시 반환 시 호출자 위치에 직접 구성 |
| **NRVO** | Named RVO; 이름 있는 로컬 객체 반환 시 같은 최적화 |
| **prvalue** | 순수 우측값; C++17에서 반환 시 mandatory copy elision 대상 |
| **valid but unspecified** | 이동된 후 객체 상태; 소멸·대입은 가능, 그 외는 계약에 따름 |

### 자주 묻는 질문 (FAQ)

**Q: `return std::move(local)`이 왜 나쁜가요?**  
A: NRVO는 "반환할 로컬 객체를 호출자 측에 직접 구성"하는데, std::move를 쓰면 "이동할 대상"이 되어 NRVO 후보에서 빠질 수 있습니다. `return local`만 쓰세요.

**Q: 값 반환은 항상 비용이 없나요?**  
A: RVO/NRVO가 적용되면 반환 위치에 직접 구성되어 추가 복사/이동이 없습니다. 적용이 안 되면 이동(또는 복사)이 선택됩니다. 이동이 저렴한 타입이면 값 반환이 권장됩니다.

**Q: 이동 후 객체를 재사용해도 되나요?**  
A: 표준상 "valid but unspecified"이므로, 소멸·대입만 보장됩니다. 일반적으로 이동 후에는 그 객체를 다시 쓰지 않는 것이 안전합니다.

**Q: 이동 생성자에 noexcept를 왜 붙이나요?**  
A: `std::vector` 같은 컨테이너는 재할당 시 이동 생성자가 noexcept일 때만 이동을 선택합니다. noexcept가 아니면 강한 예외 보장을 위해 복사로 폴백할 수 있습니다.

### 적용 체크리스트 (실무용)

- [ ] 반환 경로를 단일 `return result`로 단순화했는가?
- [ ] `return std::move(local)`을 제거하고 `return local`로 했는가?
- [ ] 이동 생성자/대입에 noexcept를 붙였는가?
- [ ] 호출자가 `T result = f();` 형태로 받아 RVO를 활용하는가?
- [ ] 생성자/이동 카운터 또는 어셈블리로 호출 횟수를 검증했는가?
- [ ] 변경 후 벤치마크로 회귀 검증했는가?

### 더 읽을 거리

- [cppreference: Copy elision](https://en.cppreference.com/w/cpp/language/copy_elision) — RVO/NRVO와 C++17 mandatory copy elision의 정확한 적용 조건을 정리한 표준 라이브러리 참조 문서

## 다음 장에서는

**이전 장**: [문자열 최적화](/post/cpp-optimization/string-optimization/) (챕터 05)

**임시 객체 제거**를 다룹니다. 연산자 오버로딩·암시적 변환·연속 연산에서 임시가 생기는 패턴을 진단하고, 참조 전달·explicit·+= 등으로 제거하는 방법을 정리합니다. 04에서 다룬 "값 반환"과 05의 "참조 전달"을 함께 쓰면 인자·반환 경로 모두에서 불필요한 복사를 줄일 수 있습니다.

→ [임시 객체 제거](/post/cpp-optimization/temporary-removal/) (챕터 07)
