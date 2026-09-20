---
collection_order: 7
date: 2026-03-10
lastmod: 2026-07-10
draft: false
image: wordcloud.png
title: "[Optimization(C++) 07] 임시 객체 제거"
slug: temporary-removal
description: "임시 객체 생성이 발생하는 패턴을 진단하고, 연산자 오버로딩·암시적 변환·연속 연산 등에서 임시를 제거하는 패턴을 다룹니다. 컴파일러 출력과 프로파일링으로 임시 비용을 확인하는 방법을 정리하며, 실무 적용 시 주의점과 대안을 제시합니다."
tags:
  - C++
  - Performance(성능)
  - Optimization(최적화)
  - Memory(메모리)
  - Compiler(컴파일러)
  - Profiling(프로파일링)
  - Benchmark
  - Implementation(구현)
  - Code-Quality(코드품질)
  - Best-Practices
  - Clean-Code(클린코드)
  - OOP(객체지향)
  - Time-Complexity(시간복잡도)
  - Space-Complexity(공간복잡도)
  - Testing(테스트)
  - Debugging(디버깅)
  - Refactoring(리팩토링)
  - Type-Safety
  - Readability
  - Maintainability
  - Modularity
  - Git
  - CI-CD
  - Linux
  - Windows
  - Latency
  - Throughput
  - Backend(백엔드)
  - Embedded(임베디드)
  - Advanced
  - Deep-Dive
  - 실습
  - Guide(가이드)
  - Reference(참고)
  - Case-Study
  - Technology(기술)
  - Tutorial(튜토리얼)
  - Edge-Cases(엣지케이스)
  - Pitfalls(함정)
  - Data-Structures(자료구조)
  - Documentation(문서화)
  - Software-Architecture(소프트웨어아키텍처)
  - Encapsulation(캡슐화)
  - Comparison(비교)
---

**임시 객체 제거**란 연산·전달 과정에서 불필요한 임시 생성과 복사/이동을 없애는 것을 말합니다. 본 챕터에서는 연산자 오버로딩·암시적 변환·연속 연산에서 임시가 생기는 패턴을 진단하고, 참조 전달·explicit·in-place 연산(+=) 등으로 제거하는 기법과 컴파일러·프로파일링으로 비용을 확인하는 방법을 정리합니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [06장: 객체 수명 최적화](/post/cpp-optimization/object-lifetime/)에서 다룬 복사·이동·RVO를 전제로 합니다. 식 `a + b + d`가 중간 결과(임시 객체)를 만든다는 점만 떠올릴 수 있으면 충분합니다.

**이 장의 깊이**: 이 장은 **중급–전문가**를 포괄합니다. 임시 객체가 생기는 패턴과 진단법부터 시작해, 전문가 구간에서는 `c = a + b + d`와 in-place `+=`를 생성자 카운터로 비교하고 in-place 연산으로 임시를 제거하는 기준을 다룹니다. **다루지 않는 것**: 컨테이너 자체의 할당 비용([04장](/post/cpp-optimization/stl-container-cost/))과 문자열 임시([05장](/post/cpp-optimization/string-optimization/))의 세부, 그리고 컴파일 타임에 연산 트리를 하나의 루프로 합성하는 expression template(템플릿 메타프로그래밍 영역)입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "임시 객체 생성 패턴" ~ "진단 방법" | 임시 객체가 어디서 생기는지 식별 |
| **중급자** | "제거 패턴" ~ "계측 예제: `c = a + b + d` vs in-place `+=`" | 임시 제거 효과를 직접 계측 |
| **전문가** | "판단 기준" ~ "비판적 시각" | 임시 제거가 이득인 경우/과잉인 경우 판단 |

---

## 임시 객체와 표준 (배경)

C++ 표준은 **temporary materialization** 등으로 "임시가 언제 생성되는지"를 정의합니다. 연산자 오버로딩으로 반환값을 받을 때, 암시적 변환으로 인자를 맞출 때, 값 반환 시(RVO가 없을 때) 임시가 생길 수 있습니다. 컴파일러는 **copy elision**으로 일부 임시를 제거하지만, 사용자 코드가 `operator+` 체이닝·암시적 변환을 유발하면 임시가 남을 수 있어, Low-latency 경로에서는 패턴을 인지하고 제거하는 것이 중요합니다.

[cppreference: Implicit conversions - Temporary materialization](https://en.cppreference.com/w/cpp/language/implicit_conversion#Temporary_materialization) 문서에 따르면, 임의의 완전한 타입 `T`의 prvalue는 필요한 시점에 xvalue로 변환되며, 이 변환이 새 임시 객체를 만들어내는 과정을 **temporary materialization**이라 부릅니다. 즉 연산 결과·변환 결과가 값으로 "쓰이기 위해" 구체적인 객체로 만들어지는 순간에 임시가 생성됩니다.

## 임시 객체 생성 패턴

**연산자 오버로딩**: `a + b`처럼 이항 `operator+`를 쓰면 결과를 담을 **임시 객체**가 생성됩니다. `Matrix c = a + b + d`처럼 체이닝하면 각 `+`마다 임시가 하나씩 생깁니다. 반면 `a += b; a += d;`처럼 `operator+=`를 쓰면 기존 객체 하나만 수정하므로 임시가 필요 없습니다.

```cpp
// 임시 여러 개: a+b 임시, (a+b)+d 임시
Matrix c = a + b + d;

// 임시 없음: in-place
Matrix c = a;
c += b;
c += d;
```

**암시적 변환**: 인자 하나만 받는 생성자(또는 변환 연산자)가 있으면, 컴파일러가 다른 타입을 그 타입으로 자동 변환할 때 **임시**를 만듭니다. 변환이 의도치 않았거나 비용이 크면 `explicit`로 막는 것이 좋습니다.

```cpp
struct Big { Big(int); };
void f(const Big&);
f(42);  // Big 임시 생성 후 const Big&로 전달

struct ExplicitBig { explicit ExplicitBig(int); };
// f(42);  // 오류: explicit이면 암시적 임시 생성 안 됨
```

**함수 인자·반환값**: 인자를 **값**으로 받으면 호출 시 복사(또는 이동)가 일어나고, 반환도 값이면 임시가 생길 수 있습니다(RVO/NRVO로 제거되는 경우 제외). 인자를 읽기만 할 때는 `const T&`나 `T&&`로 받아 임시 생성을 줄일 수 있습니다.

## 진단 방법

임시 생성 여부는 추측이 아니라 확인의 대상입니다. 가장 근본적인 방법은 **컴파일러 출력**을 직접 보는 것으로, GCC/Clang에서 `-fdump-tree-*`로 중간 표현을 덤프하거나 `-S`로 어셈블리를 생성한 뒤 생성자·소멸자 심볼이 몇 번 호출되는지 세면 임시 생성 횟수를 정확히 파악할 수 있습니다. 코드 규모가 커서 어셈블리를 눈으로 추적하기 어려울 때는 **프로파일링**으로 전환합니다. 메모리 할당 프로파일러로 특정 타입의 할당 횟수를 관찰하거나, CPU 프로파일러에서 해당 타입의 생성자·소멸자가 전체 실행 시간에서 차지하는 비중을 확인하면 됩니다. 마지막으로 가장 실용적인 방법은 **로깅·카운터**입니다. 생성자·복사 생성자·이동 생성자 각각에 정적 카운터를 넣어 단위 테스트나 벤치마크를 실행할 때 호출 횟수를 기록하면, 아래 계측 예제처럼 임시 제거 전후로 횟수가 실제로 줄어드는지 눈으로 검증할 수 있습니다. 세 방법은 상호 배타적이지 않으며, 어셈블리로 존재를 확인하고 카운터로 회귀를 방지하는 식으로 함께 쓰는 것이 일반적입니다.

## 제거 패턴

임시를 제거하는 기법은 "임시가 왜 생겼는가"에 따라 대응이 달라집니다. 함수가 인자를 값으로 받아 호출마다 복사를 유발한다면, 읽기만 할 때는 **참조로 전달**해 `const T&`를, 소유권을 넘기거나 수정할 때는 `T&&`를 씁니다. `void f(const T&)`는 호출자가 임시를 넘겨도 그 임시의 수명이 함수 종료까지 연장되므로 "읽기 전용" API에 특히 적합합니다. 같은 연산을 반복 수행한다면 **연산 결합**으로 대응합니다 — 중간 결과를 한 번 변수에 담아 재사용하면 같은 연산을 반복할 때마다 임시가 다시 생성되는 낭비를 막을 수 있으므로, 루프 안이 아니라 루프 밖에서 한 번만 만들고 재사용합니다. 의도하지 않은 타입 변환이 임시를 유발한다면 **explicit**를 둡니다. 단일 인자 생성자나 변환 연산자에 `explicit`를 붙이면 암시적 변환으로 인한 임시 생성 자체가 컴파일 시점에 차단됩니다. 마지막으로 연산자를 직접 설계하는 입장이라면 **연산자 설계** 원칙을 따릅니다. 반복 덧셈처럼 누적되는 연산에는 `operator+=`를 제공하고, 사용자 편의를 위한 `a + b`는 `T tmp = a; tmp += b; return tmp;`처럼 구현해 한 번의 명시적 복사만 발생하도록 설계합니다.

## 계측 예제: `c = a + b + d` vs in-place `+=`

연산 카운터를 가진 `Matrix` 타입으로 임시 생성 횟수를 직접 셉니다. 체이닝 `a + b + d`는 임시 두 개를 만들지만, in-place `+=`는 추가 임시가 없습니다. 아래는 그대로 컴파일·실행할 수 있습니다(`-std=c++17 -O2`).

```cpp
#include <iostream>
#include <vector>

struct Matrix {
  static int ctor, copy, tmp;     // tmp: operator+가 만든 임시 수
  std::vector<double> a;

  explicit Matrix(size_t n = 16) : a(n * n, 0.0) { ++ctor; }
  Matrix(const Matrix& o) : a(o.a) { ++copy; }

  Matrix& operator+=(const Matrix& o) {
    for (size_t i = 0; i < a.size(); ++i) a[i] += o.a[i];
    return *this;                 // in-place: 새 객체 없음
  }
  friend Matrix operator+(const Matrix& x, const Matrix& y) {
    Matrix r = x;                 // 복사 1회
    r += y;
    ++tmp;                        // operator+가 반환하는 임시를 계측
    return r;                     // NRVO로 호출 측에 직접 구성
  }
};
int Matrix::ctor = 0, Matrix::copy = 0, Matrix::tmp = 0;

static void reset() { Matrix::ctor = Matrix::copy = Matrix::tmp = 0; }
static void report(const char* tag) {
  std::cout << tag << ": ctor=" << Matrix::ctor
            << " copy=" << Matrix::copy
            << " tmp(op+)=" << Matrix::tmp << '\n';
}

int main() {
  Matrix a, b, d;                 // ctor=3

  reset();
  Matrix c1 = a + b + d;          // op+ 두 번 → 임시 2, 복사 2
  report("chain a+b+d");          // copy=2 tmp(op+)=2

  reset();
  Matrix c2 = a;                  // copy=1
  c2 += b;                        // in-place
  c2 += d;                        // in-place
  report("in-place +=");          // copy=1 tmp(op+)=0
}
```

`a + b + d`는 `operator+`를 두 번 호출하며 매번 복사로 임시를 만들지만, `+=` 버전은 시작 복사 한 번 외에 추가 임시가 없습니다. 핫패스의 반복 연산에서는 이 차이가 누적됩니다. (측정값은 컴파일러·플래그에 따라 다를 수 있음)

## 평가 기준 (학습 성과 목표)

- 연산자 오버로딩(`operator+` vs `operator+=`), 암시적 변환, 값 전달·반환에서 **임시가 생기는 조건**을 설명할 수 있다.
- **참조 전달**(const T&, T&&), **explicit**, **연산 결합·+=**로 임시를 제거할 수 있다.
- 컴파일러 덤프·어셈블리·카운터로 생성자 호출 횟수를 확인하고, 제거 전/후 벤치마크로 검증할 수 있다.

## 판단 기준 (언제 쓰고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 읽기 전용 인자 | `const T&` / string_view | 값 전달로 임시 유발 |
| 반복 연산(루프 내) | `+=`, in-place, 루프 밖 한 번 생성 | 매번 `operator+` |
| 단일 인자 생성자 | `explicit` (의도한 변환만) | 암시적 임시 유발 |
| 연산자 설계 | `+=` 제공, `+`는 `tmp+=` 반환 | `+`만 제공해 임시 다수 |

### 자주 하는 실수

- **값으로 받는 인자 유지**: 읽기만 하는 인자는 `const T&` 또는 string_view로 바꿔 임시와 복사를 줄입니다.
- **`operator+`만 제공**: 반복 연산 시 임시가 누적되므로 `+=`를 제공하고 반복 연산에서는 `+=` 사용을 가이드합니다.
- **암시적 변환 허용**: 의도하지 않은 변환으로 임시가 생기면 `explicit`로 막습니다.
- **참조 전달 후 수명 오류**: `const T&`로 받은 임시는 함수 종료까지 유지되지만, 포인터/참조를 저장하면 댕글링이 됩니다. 저장이 필요하면 복사하거나 소유 타입을 씁니다.

### 리팩토링 시 주의

인자를 참조로 바꾸면 호출처에서 임시가 사라지지만, 참조의 수명을 호출자가 보장해야 합니다. 예: `void f(T x)`를 `void f(const T& x)`로 바꿀 때, f 내부에서 포인터/참조를 저장하지 않는지 확인하고 테스트·벤치마크로 회귀를 검증합니다.

## 비판적 시각: 한계와 트레이드오프

- **참조 전달**: 라이프타임을 호출자가 관리해야 하므로 API 계약을 명확히 한다. 임시를 받아도 수명이 함수 종료까지 연장되는 `const T&`는 읽기 전용 API에 적합하다.
- **operator+ 제거**: 사용자 편의를 위해 `a + b`를 제공하되, 내부는 `T tmp = a; tmp += b; return tmp;`로 한 번의 복사만 두고, 반복 연산은 `+=` 사용을 권장하는 식으로 균형을 잡는다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 임시 원인 | `operator+`, 암시적 변환, 값 전달·반환, 연속 연산 |
| 제거 | `const T&`/`T&&`, explicit, `+=`·in-place, reserve |
| 진단 | 어셈블리·덤프·카운터·프로파일러로 호출 횟수 확인 |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **temporary materialization** | prvalue가 glvalue로 사용되기 위해 구체화될 때 임시 생성 |
| **explicit** | 단일 인자 생성자·변환 연산자에 붙여 암시적 변환 차단 |
| **in-place** | 새 객체를 만들지 않고 기존 객체를 수정하는 연산(예: `+=`) |

### 자주 묻는 질문 (FAQ)

**Q: 모든 단일 인자 생성자에 explicit를 붙여야 하나요?**  
A: 변환이 의도된 경우(예: 단위 래퍼)만 명시적 변환을 허용하고, 나머지는 explicit로 암시적 임시 생성을 막는 것이 좋습니다. API 설계에 따라 선택합니다.

**Q: operator+를 제거해야 하나요?**  
A: 아니요. operator+는 사용자 편의를 위해 유지하되, 내부는 `T tmp = a; tmp += b; return tmp;`로 한 번의 복사만 두고, 반복 연산은 `+=` 사용을 권장합니다.

**Q: 참조 전달만 하면 임시가 사라지나요?**  
A: `const T&`는 호출자가 임시를 넘겨도 수명이 함수 종료까지 연장되므로, "읽기 전용" 인자에서는 임시 생성이 한 번만 일어나고 복사 비용을 줄일 수 있습니다. `T&&`는 이동을 유도할 때 사용합니다.

### 적용 체크리스트 (실무용)

- [ ] 읽기 전용 인자를 `const T&`/string_view로 받았는가?
- [ ] 반복 연산에서 `+=` 또는 in-place·루프 밖 한 번 생성을 사용했는가?
- [ ] 단일 인자 생성자에 explicit를 붙였는가?
- [ ] 연산자 설계에서 `+=`를 제공하고 `+`는 `tmp+=` 반환으로 했는가?
- [ ] 컴파일러 덤프·어셈블리·카운터로 생성자 호출 횟수를 확인했는가?
- [ ] 제거 전/후 벤치마크로 회귀 검증했는가?

### 더 읽을 거리

- [cppreference: Implicit conversions - Temporary materialization](https://en.cppreference.com/w/cpp/language/implicit_conversion#Temporary_materialization) — prvalue가 xvalue로 변환되며 임시 객체가 구체화되는 규칙을 정의하는 참조 문서
- [cppreference: Value categories](https://en.cppreference.com/w/cpp/language/value_category) — prvalue/xvalue/lvalue와 결과 객체(result object) 개념을 정의하는 참조 문서

## 다음 장에서는

**이전 장**: [객체 수명 최적화](/post/cpp-optimization/object-lifetime/) (챕터 06)

**템플릿/constexpr**를 다룹니다. constexpr·consteval로 컴파일 타임 계산을 하고, 템플릿으로 비용을 제어·인라이닝을 유도하는 패턴을 정리합니다. 05의 "임시 제거"(런타임 경로)와 06의 "컴파일 타임으로 옮기기"를 함께 적용하면 런타임 생성·복사를 더 줄일 수 있습니다.

→ [템플릿/constexpr](/post/cpp-optimization/templates-constexpr/) (챕터 08)
