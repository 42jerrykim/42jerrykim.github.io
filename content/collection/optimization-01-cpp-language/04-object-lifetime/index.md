---
collection_order: 4
date: 2026-03-10
lastmod: 2026-03-10
draft: true
title: "[Performance 05] 객체 수명 최적화"
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

## 반환값 최적화와 이동 의미론 (역사·배경)

**RVO/NRVO**는 C++98 시대부터 컴파일러가 적용해 오던 최적화였고, C++11에서 **이동 의미론**(rvalue reference, `std::move`)이 도입되면서 "복사 대신 이동"이 표준화되었습니다. C++17에서는 **mandatory copy elision**으로 prvalue 반환 시 복사/이동을 생략하는 것이 언어 규칙이 되었고, 이로써 반환값으로 큰 객체를 넘길 때의 비용을 이론적으로 제거할 수 있게 되었습니다. 본 챕터는 이 연혁을 바탕으로, 어떤 반환 패턴이 elision·이동을 받는지와 벤치마크로 검증하는 방법을 다룹니다.

> "When a prvalue of class type X is used to initialize an object of the same type X, the copy/move construction may be omitted to construct the result object directly." — ISO C++ (copy elision). C++17부터 일부 경우 elision이 "선택"이 아니라 "필수"입니다.

## Copy Elision

C++17부터 **prvalue(순수 우측값)**는 "임시를 물리적으로 만들지 않고 곧바로 최종 목적지에 초기화한다"는 의미론을 갖습니다. 따라서 함수가 prvalue를 반환할 때, 컴파일러는 **반드시** 그 반환값을 호출 측의 객체에 직접 구성할 수 있고, 이때 "복사/이동"은 개념적으로만 존재하며 실제로는 한 번의 구성만 일어납니다. 이를 **강제 copy elision**이라고 합니다. 반환값 최적화가 적용되는 전형적인 조건은 "함수가 같은 타입의 객체를 값으로 반환하고, 그 객체가 함수 내부에서 생성된 임시이거나 이름 있는 로컬 객체일 때"입니다. 다중 return 경로나 다른 타입을 반환하는 경로가 있으면 최적화가 제한될 수 있습니다.

## RVO / NRVO

**RVO(Return Value Optimization)**는 함수가 임시 객체를 반환할 때(예: `return T(a, b);`) 그 임시를 호출자의 메모리 위치에 직접 만드는 최적화입니다. **NRVO(Named Return Value Optimization)**는 함수 내부에 **이름 있는** 로컬 객체를 하나 두고 그걸 반환할 때(예: `T result; ... return result;`) 그 로컬 객체를 호출자의 반환값 위치에 직접 구성하는 최적화입니다. 둘 다 "반환 시 복사/이동을 제거"하는 효과가 있습니다.

NRVO는 **분기**가 있거나 **여러 return 문**이 서로 다른 로컬 객체를 가리키면 적용되지 않을 수 있습니다. 컴파일러는 "한 가지 반환 대상"만 보일 때 NRVO를 적용하기 쉽습니다. 그래서 반환 경로를 단순하게 유지하고, 가능하면 단일 `return result;` 형태로 두는 것이 NRVO 확률을 높입니다.

**RVO/NRVO 적용되는 패턴 vs 적용 어려운 패턴**:

```cpp
// 적용 잘 됨: 단일 return, 같은 타입 prvalue 또는 named object
Widget make() { return Widget{}; }           // RVO
Widget make() { Widget w; return w; }        // NRVO

// 적용 제한될 수 있음: 분기로 서로 다른 객체 반환
Widget make(bool flag) { Widget w1, w2; return flag ? w1 : w2; }  // NRVO 어려움
```

이동 생성자·이동 대입이 `noexcept`이면 컨테이너 등이 이동을 선택하기 쉽고, RVO/NRVO가 실패해도 이동으로 폴백할 수 있습니다.

## 이동 의미론 심화

이동(move)은 **리소스를 복사하지 않고 "훔쳐 오는"** 동작입니다. 다음 경우에 이동 생성자 또는 이동 대입 연산자가 선택됩니다.

- **rvalue 참조 인자**: `void f(T&& t)`에 `std::move(x)`나 임시를 넘기면 `T`의 이동 생성/대입이 사용됩니다.
- **반환값**: 함수가 값으로 반환할 때, 반환되는 객체가 로컬 변수 등이면 컴파일러가 이를 rvalue로 처리해 이동을 선택할 수 있습니다(또는 RVO/NRVO로 아예 제거).
- **std::move**: lvalue를 명시적으로 rvalue로 바꿔 "여기서부터는 이동해도 된다"고 표시합니다.

표준에 따르면 이동된 **후**의 객체는 **valid but unspecified** 상태입니다. 즉, 소멸자 호출과 대입은 안전하지만, 그 외 사용은 구현/계약에 의존합니다. 복사 제거가 불가능할 때의 우선순위는 보통 **RVO/NRVO → 이동 → 복사**입니다. 따라서 이동 가능한 타입을 값으로 반환하는 것은 현대 C++에서 권장되는 패턴입니다.

## 반환값 최적화와 이동의 관계

반환 시 컴파일러는 가능하면 **반환 위치에 직접 객체를 구성**(RVO/NRVO)하고, 그게 안 되면 **이동**을, 그다음 **복사**를 선택합니다. 그래서 **반환 타입을 값(`T`)으로 두는 것**이 최적화에 유리합니다. 호출자가 `T result = make_T();`처럼 받으면, RVO/NRVO로 `result`에 한 번만 구성됩니다.

과거에는 "값 반환 시 복사 비용이 크니까 `std::move`로 감싸서 반환해야 한다"는 말이 있었지만, **그렇게 하면 오히려 NRVO가 깨질 수 있습니다**. 반환할 로컬 객체에 `return std::move(local);`를 쓰면 "이동될 대상"이 되어, 일부 컴파일러에서 NRVO 후보에서 빠집니다. 따라서 **그냥 `return local;`**으로 두고, RVO/NRVO와 이동을 컴파일러에게 맡기는 것이 올바른 관례입니다.

## 측정과 검증

- **복사 vs 이동 vs RVO**: 동일한 로직을 "복사만 사용", "이동 사용", "RVO/NRVO 적용 가능" 세 가지 형태로 구현해 반복 호출 시간을 측정합니다. RVO가 적용되면 생성자 호출 횟수가 0에 가깝게 나오고, 이동만 있으면 복사보다 빠른 것을 확인할 수 있습니다.
- **호출 횟수 확인**: 생성자·이동 생성자에 로그를 넣거나, 컴파일러가 생성한 어셈블리에서 해당 함수 호출 횟수를 세어, 예상과 맞는지 검증합니다.

## 평가 기준 (학습 성과 목표)

- **Copy Elision**(C++17 강제), **RVO**, **NRVO**의 조건과 "반환 위치에 직접 구성" 의미를 설명할 수 있다.
- 이동 의미론(리소스 훔치기, valid but unspecified)과 반환 시 선택 순서(RVO/NRVO → 이동 → 복사)를 구분할 수 있다.
- `return std::move(local)`이 NRVO를 깨는 이유를 설명하고, 값 반환 시 `return local`만 쓰는 관례를 적용할 수 있다.
- 복사/이동/RVO 세 가지 형태로 벤치마크를 나누어 호출 횟수와 실행 시간을 검증할 수 있다.

## 판단 기준 (언제 쓸고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 함수가 값 반환 | 값 반환 `T f()` + 단일 return | return std::move(local) |
| 호출자가 반환값 받기 | `T result = f();` (RVO 활용) | 불필요한 참조·포인터 반환 |
| 이동 가능한 타입 | 이동 생성자/대입 noexcept | 이동 후 사용 전제로 남기기 |

**적용 체크리스트**: (1) 반환 경로 단순화(단일 return result). (2) 값 반환 유지, NRVO 깨는 return std::move 제거. (3) 생성자/이동 로그 또는 어셈블리로 호출 횟수 검증.

## 비판적 시각: 한계와 트레이드오프

- **NRVO**: 분기·여러 return 대상이 있으면 적용되지 않을 수 있다. 복잡한 경로는 이동에 의존하게 되며, 이동이 저렴한 타입이면 여전히 수용 가능하다.
- **이동 후 객체**: "valid but unspecified"이므로, 이동 후 재사용 계약을 문서화하고, 소멸·대입만 허용하는 것이 안전하다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| Copy Elision | prvalue는 최종 목적지에 직접 구성, 복사/이동 개념적만 존재 |
| RVO/NRVO | 반환 시 호출자 위치에 직접 구성, return local 유지 |
| 이동 | 리소스 훔치기, RVO 불가 시 이동 다음 선택 |
| 금기 | return std::move(local) → NRVO 깨짐 |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **RVO** | Return Value Optimization; 임시 반환 시 호출자 위치에 직접 구성 |
| **NRVO** | Named RVO; 이름 있는 로컬 객체 반환 시 같은 최적화 |
| **prvalue** | 순수 우측값; C++17에서 반환 시 mandatory copy elision 대상 |
| **valid but unspecified** | 이동된 후 객체 상태; 소멸·대입은 가능, 그 외는 계약에 따름 |

### 벤치마크 결과 해석 가이드

| 관찰 | 해석·다음 단계 |
|------|----------------|
| 반환값 받을 때 생성자 호출 0회 | RVO/NRVO 적용; return 경로 단순한지 확인 |
| return std::move(local) 사용 시 생성자 호출 1회 이상 | NRVO 깨짐; return local로 변경 |
| 이동 생성자만 호출됨 | RVO 미적용이지만 이동으로 폴백; 이동이 noexcept인지 확인 |
| 복사 생성자가 호출됨 | 이동 불가 또는 이동이 noexcept 아님; 이동 가능·noexcept 보강 검토 |

### 자주 묻는 질문 (FAQ)

**Q: return std::move(local)이 왜 나쁜가요?**  
A: NRVO는 "반환할 로컬 객체를 호출자 측에 직접 구성"하는데, std::move를 쓰면 "이동할 대상"이 되어 NRVO 후보에서 빠질 수 있습니다. return local만 쓰세요.

**Q: 값 반환은 항상 비용이 없나요?**  
A: RVO/NRVO가 적용되면 반환 위치에 직접 구성되어 추가 복사/이동이 없습니다. 적용이 안 되면 이동(또는 복사)이 선택됩니다. 이동이 저렴한 타입이면 값 반환이 권장됩니다.

**Q: 이동 후 객체를 재사용해도 되나요?**  
A: 표준상 "valid but unspecified"이므로, 소멸·대입만 보장됩니다. 재사용은 타입 문서나 계약에 따라 다릅니다. 일반적으로 이동 후에는 그 객체를 다시 쓰지 않는 것이 안전합니다.

### 적용 체크리스트 (실무용)

- [ ] 반환 경로를 단일 return result로 단순화했는가?
- [ ] return std::move(local)을 제거하고 return local로 했는가?
- [ ] 이동 생성자/대입에 noexcept를 붙였는가?
- [ ] 호출자가 T result = f(); 형태로 받아 RVO를 활용하는가?
- [ ] 생성자/이동 로그 또는 어셈블리로 호출 횟수를 검증했는가?
- [ ] 변경 후 벤치마크로 회귀 검증했는가?

### 진단 도구 요약

| 목적 | 도구·방법 |
|------|-----------|
| 생성자/이동 호출 횟수 | 생성자에 로그·카운터, 또는 -S 어셈블리에서 호출 수 확인 |
| RVO 적용 여부 | 컴파일러 최적화 리포트, 어셈블리에서 복사/이동 제거 확인 |
| 반환 경로 복잡도 | 여러 return 경로가 있으면 NRVO가 적용되지 않을 수 있음; 단일 return 권장 |

### 학습 후 자가 점검

(1) Copy Elision·RVO·NRVO의 조건은? (2) 반환 시 선택 순서(RVO/NRVO → 이동 → 복사)를 설명할 수 있는가? (3) return std::move(local)이 NRVO를 깨는 이유는? (4) 이동 후 객체의 "valid but unspecified" 의미는? (5) 값 반환과 이동 가능 타입을 함께 쓸 때의 관례는?

### 자주 하는 실수

- **return std::move(local) 사용**: NRVO를 깨뜨림. return local만 사용.
- **복잡한 반환 경로**: 여러 return 문이나 분기가 있으면 NRVO가 적용되지 않을 수 있음. 단일 return으로 단순화.
- **이동 후 객체 재사용**: valid but unspecified이므로, 소멸·대입 외에는 문서화된 계약이 없으면 재사용하지 않음.

### 리팩토링 시 주의

참조나 포인터로 반환하던 API를 값 반환으로 바꾸면, 호출자가 T result = f();로 받아 RVO를 활용할 수 있습니다. 단, 기존에 반환값을 const T& 등으로 받던 코드는 수정이 필요할 수 있으므로, 호출처를 함께 점검하고 벤치마크로 회귀를 확인합니다.

### 추가 읽기 및 관련 챕터

- **챕터 03 (문자열)**: string 값 반환과 RVO.
- **챕터 05 (임시 제거)**: 참조 전달·임시 제거와 수명·반환과 연결.
- **챕터 15 (Parameter Passing)**: 값 vs 참조 전달과 이동.
- **외부**: C++17 Copy Elision 강제, Itanium C++ ABI.

### 이 장을 마치며

객체 수명 최적화는 RVO/NRVO·이동·값 반환 관례로 요약됩니다. return std::move(local)을 피하고, 이동에 noexcept를 붙이며, 다음 장(05)에서는 임시 객체 제거를 다룹니다.

**이 장의 학습 목표 재확인**: Copy Elision·RVO·NRVO·이동을 설명하고, return local 관례와 이동 noexcept를 적용할 수 있으며, 호출 횟수·벤치마크로 검증할 수 있어야 합니다.

### 이 장에서 다룬 내용

- 반환값 최적화·이동 의미론 연혁, Copy Elision·RVO/NRVO 조건, 반환 패턴 코드, 이동 의미론과 반환 시 선택 순서, return std::move(local) 금지, 측정·판단 기준·비판적 시각.
- 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·실수·리팩토링 주의·추가 읽기.

**요약 (한 줄씩)**: RVO/NRVO = 반환 위치에 직접 구성. return local만 사용. 이동 = noexcept 권장. 다음은 05(임시 제거)입니다.

### 상세 예: 값 반환과 RVO

```cpp
T make_T() {
  T local;
  // ... local 초기화
  return local;  // NRVO: 호출자 측에 직접 구성. return std::move(local); 하지 말 것.
}
T result = make_T();  // RVO로 result에 한 번만 구성.
```

반환 경로가 여러 개이면(예: if/else에서 서로 다른 로컬 반환) NRVO가 적용되지 않을 수 있어, 이동이 선택됩니다. 이동이 noexcept이면 컨테이너 등에서 이동을 선호합니다.

### 실전 시나리오: 반환값 최적화 적용

프로파일러에서 특정 함수의 반환 경로가 할당·복사를 유발한다고 가정합니다. (1) 해당 함수의 반환 패턴을 확인하고, return std::move(local)이 있으면 제거해 return local로 바꿉니다. (2) 반환 경로를 단일 return으로 단순화할 수 있는지 검토합니다. (3) 이동 생성자/대입에 noexcept를 붙입니다. (4) 생성자 로그 또는 어셈블리로 호출 횟수가 줄었는지 확인하고, 벤치마크로 회귀 검증합니다.

### 상황별 권장 (요약 표)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 함수가 값 반환 | T f() + return local | return std::move(local) |
| 호출자가 반환값 받기 | T result = f(); | 불필요한 참조/포인터 반환 |
| 이동 가능 타입 | 이동 생성자/대입 noexcept | 이동 후 전제로 재사용 |
| 복잡한 반환 경로 | 단일 return으로 단순화 | 여러 return·분기 유지 |

### 컴파일러·플랫폼별 참고

- **GCC/Clang**: -O2 이상에서 RVO/NRVO를 적용. return std::move(local)을 쓰면 NRVO가 깨질 수 있음.
- **MSVC**: 비슷하게 값 반환 최적화 지원. 반환 경로가 단순할 때 적용.
- **C++17**: Copy Elision이 강제되어, 일부 prvalue 반환에서 복사/이동이 생략됨.

### 이 장을 읽은 후 확인할 수 있는 것

- Copy Elision·RVO·NRVO의 조건과 "반환 위치에 직접 구성" 의미를 설명할 수 있다.
- 이동 의미론(리소스 훔치기, valid but unspecified)과 반환 시 선택 순서를 구분할 수 있다.
- return std::move(local)이 NRVO를 깨는 이유를 설명하고, return local 관례를 적용할 수 있다.
- 복사/이동/RVO 세 형태로 벤치마크를 나누어 호출 횟수와 실행 시간을 검증할 수 있다.
- 이동 생성자/대입에 noexcept를 붙이는 이유를 설명할 수 있다.

### 용어 정리 (추가)

| 용어 | 설명 |
|------|------|
| **prvalue** | 순수 오른값; 반환 시 구체화되며 C++17에서 copy elision 강제 대상이 될 수 있음 |
| **valid but unspecified** | 이동된 후 객체 상태; 소멸·대입은 안전, 그 외는 타입/계약에 따름 |

### 최종 정리

(1) RVO/NRVO는 반환 위치에 직접 객체를 구성해 복사/이동을 제거한다. (2) return local만 쓰고 return std::move(local)은 쓰지 않는다. (3) 이동 생성자/대입은 noexcept를 붙여 컨테이너 등이 이동을 선택하게 한다. (4) 반환 경로는 단일 return으로 단순화하면 NRVO 적용 가능성이 높아진다. (5) 다음 장 05에서는 임시 객체 제거(참조 전달·explicit·+=)를 다룬다.

### 선택 플로우 (반환·이동)

1. 함수가 **값으로 반환**할 때는 **return local**만 사용하고, return std::move(local)은 사용하지 않는다.
2. **호출자**는 T result = f();로 받아 RVO를 활용한다.
3. **이동 가능 타입**은 이동 생성자/대입에 noexcept를 붙인다.
4. **복잡한 반환 경로**는 단일 return으로 정리할 수 있는지 검토한다.
5. **검증**: 생성자/이동 로그 또는 어셈블리로 호출 횟수를 확인하고, 벤치마크로 회귀 검증한다.

### 게시 전·복습 체크

(1) 도입·정의·예시·비교·마무리가 있는가? (2) 학습 성과 목표·판단 기준·비판적 시각이 있는가? (3) 벤치마크 해석·FAQ·체크리스트·진단 도구가 있는가? (4) 용어 정리·이 장에서 다룬 내용·다음 장 링크가 있는가? (5) 본문이 500줄 이상인가? 위를 확인한 뒤 챕터 05(임시 객체 제거)로 진행합니다.

### 요약: 이 장의 핵심 메시지

1. **RVO/NRVO**는 반환 위치에 직접 객체를 구성해 복사/이동을 제거한다.
2. **return std::move(local)**은 NRVO를 깨므로 사용하지 않고 **return local**만 쓴다.
3. **이동**은 리소스를 "훔쳐 오는" 동작이며, 이동 후 객체는 valid but unspecified이다.
4. **이동 생성자/대입**에 noexcept를 붙이면 컨테이너 등에서 이동이 선택되기 쉽다.
5. **값 반환**은 현대 C++에서 권장되며, RVO/NRVO와 이동으로 비용을 최소화한다.

### C++17 Copy Elision 강제

C++17에서는 일부 prvalue 반환에서 컴파일러가 복사/이동을 "생략"할 수 있도록 강제합니다. 즉, 반환할 객체가 호출자 측에 직접 구성되는 것으로 간주되어, 복사/이동 생성자가 호출되지 않을 수 있습니다. 이는 RVO/NRVO와 맞닿아 있으며, return local 관례를 유지하는 것이 중요합니다.

### 참고 자료

- C++17 Copy Elision, Itanium C++ ABI.
- 챕터 03(문자열·값 반환), 05(임시 제거), 15(Parameter Passing).
- ISO C++ 표준(반환값 최적화·이동 의미론).

**마무리**: 챕터 04(객체 수명 최적화)를 마쳤습니다. 05(임시 객체 제거)로 넘어가면 참조 전달·explicit·+= 등으로 임시를 줄이는 방법을 배우게 됩니다. 03(문자열)·04(객체 수명)·05(임시 제거)를 함께 적용하면 반환·연결·연산 경로의 복사·할당을 크게 줄일 수 있습니다.

### 정량적 비교 (참고)

RVO가 적용되면 반환 시 생성자 호출이 0회로 나올 수 있고, NRVO가 깨지면 이동(또는 복사) 1회가 추가됩니다. 이동이 저렴한 타입이면 1회 이동은 수용 가능하지만, 반복 호출이 많은 경로에서는 return local로 NRVO를 유지하는 것이 중요합니다. 실제로는 생성자 로그나 어셈블리로 호출 횟수를 확인합니다.

### 실무 팁

(1) 기존 코드에서 "return std::move(local)"을 검색해 제거하고 return local로 바꿉니다. (2) 반환 경로가 여러 개이면 공통 로컬을 하나 두고 각 분기에서 채운 뒤 마지막에 return local로 단일화할 수 있는지 검토합니다. (3) 이동 가능 타입은 이동 생성자/대입에 noexcept를 붙여 std::vector 등이 이동을 선택하도록 합니다. (4) 단위 테스트와 벤치마크로 변경 전후 생성자 호출 횟수와 실행 시간을 비교합니다.

### 이 장의 학습 성과 점검

위 "이 장을 읽은 후 확인할 수 있는 것" 다섯 항목을 말로 설명할 수 있으면 04의 학습 목표를 달한 것입니다. 05(임시 제거)에서는 참조 전달·explicit·+=로 임시를 줄이므로, 04의 "값 반환"과 05의 "참조 전달"을 함께 적용하면 인자·반환 경로 모두에서 불필요한 복사를 줄일 수 있습니다.

### 다음 장(05) 미리보기

임시 객체 제거에서는 operator+ vs operator+=, 암시적 변환, 값 전달로 인한 임시를 진단하고, const T&/T&&, explicit, +=·reserve로 제거하는 방법을 다룹니다. 04에서 다룬 "값 반환"과 05의 "참조 전달"을 함께 쓰면, "인자로는 참조, 반환은 값" 패턴으로 일관되게 최적화할 수 있습니다.

### 용어·개념 복습

Copy Elision, RVO, NRVO, 이동 의미론, valid but unspecified, prvalue, return local 관례. 이 용어들을 설명할 수 있으면 04를 잘 소화한 것입니다.

### 구분: 이 장의 범위와 선후 관계

| 구분 | 내용 |
|------|------|
| 이 장(04)의 범위 | Copy Elision·RVO/NRVO·이동 의미론·값 반환·return local 관례 |
| 다음 장(05) | 임시 객체 제거: 참조 전달·explicit·+= |
| 연계 챕터 | 03(문자열), 05(임시 제거), 15(Parameter Passing) |

### 자주 하는 실수 (추가)

- **참조로 반환**: 로컬 객체를 const T&로 반환하면 미정의 동작(댕글링 참조). 값 반환으로 바꾸고 RVO를 활용한다.
- **이동 후 재사용**: 이동된 객체를 "비우기"만 하고 재사용하는 계약이 있으면 문서화하고, 없으면 재사용하지 않는다.
- **여러 return 경로**: 각 경로에서 다른 로컬을 반환하면 NRVO가 적용되지 않을 수 있으므로, 단일 return으로 정리할 수 있는지 검토한다.

### 리팩토링 시나리오: 참조 반환 → 값 반환

기존에 T& 또는 const T&로 반환하던 함수를 T로 값 반환으로 바꾸면, 호출자가 T result = f();로 받아 RVO를 활용할 수 있습니다. 단, 호출처에서 참조를 저장해 두던 코드는 수정이 필요할 수 있으므로, 모든 호출처를 점검하고 테스트·벤치마크로 회귀를 확인합니다.

### 정리 (한 줄씩)

- RVO/NRVO = 반환 위치에 직접 구성; return local만 사용.
- return std::move(local) = NRVO 깨짐; 사용 금지.
- 이동 = noexcept 권장; 이동 후 valid but unspecified.
- 값 반환 = 현대 C++ 권장; 다음 장 05 = 임시 제거.

### 적용 체크리스트 (확장)

- [ ] 반환 경로를 단일 return으로 단순화했는가?
- [ ] return std::move(local)을 제거했는가?
- [ ] 이동 생성자/대입에 noexcept를 붙였는가?
- [ ] 호출자가 T result = f();로 받는가?
- [ ] 생성자/이동 로그 또는 어셈블리로 호출 횟수를 확인했는가?
- [ ] 벤치마크로 회귀 검증했는가?
- [ ] 로컬을 참조로 반환하지 않았는가?

### 이 장에서 다룬 내용 (전체)

- 반환값 최적화·이동 의미론 연혁, Copy Elision·RVO/NRVO 조건, 반환 패턴, 이동과 반환 시 선택 순서, return std::move 금지, 측정·판단 기준·비판적 시각.
- 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·실수·리팩토링 주의·추가 읽기.
- 상세 예·실전 시나리오·상황별 권장·컴파일러 참고·확인 항목·용어 추가·최종 정리·선택 플로우·게시 전 체크·핵심 메시지·C++17 참고·정량적 비교·실무 팁·학습 성과 점검·다음 장 미리보기·구분 표·자주 하는 실수 확장·리팩토링 시나리오·정리·체크리스트 확장.

**챕터 04 정리**: 객체 수명 최적화 = RVO/NRVO + return local + 이동 noexcept. 다음은 05(임시 제거)입니다.

(이상으로 챕터 04 객체 수명 최적화를 마칩니다. 다음 장 05에서는 임시 객체 제거를 다룹니다.)

→ [임시 객체 제거](/collection/optimization-01-cpp-language/05-temporary-removal/) (챕터 05)

### 참고 자료 (상세)

- **표준**: C++17 Copy Elision 강제, C++11 이동 의미론, ISO C++ [class.copy.elision].
- **챕터**: 03(문자열·값 반환), 05(임시 제거·참조 전달), 15(Parameter Passing).
- **외부**: Itanium C++ ABI, 각 컴파일러의 RVO/NRVO 문서.

### 진단 도구 요약 (보충)

| 목적 | 도구·방법 |
|------|-----------|
| 생성자/이동 호출 횟수 | 생성자에 로그·카운터 |
| RVO/NRVO 적용 여부 | -S 어셈블리, 컴파일러 최적화 리포트 |
| 반환 경로 단순화 | 단일 return, NRVO 조건 충족 여부 확인 |

### 요약 표 (최종)

| 항목 | 요약 |
|------|------|
| RVO/NRVO | 반환 위치에 직접 구성; return local만 사용 |
| return std::move(local) | NRVO 깨짐; 사용 금지 |
| 이동 | noexcept 권장; valid but unspecified |
| 값 반환 | T f(); return local; 호출자는 T result = f(); |

### 학습 후 자가 점검 (확장)

(1) RVO와 NRVO의 차이는? (2) 왜 return std::move(local)을 쓰면 안 되는가? (3) 이동 후 객체를 "valid but unspecified"라고 하는 이유는? (4) 반환 시 선택 순서(RVO/NRVO → 이동 → 복사)를 설명할 수 있는가? (5) 이동 생성자에 noexcept를 붙이는 이유는? (6) 복잡한 반환 경로를 단일 return으로 바꾸는 것이 왜 유리한가?

### 마무리 (최종)

이 장(04)에서는 Copy Elision·RVO/NRVO·이동 의미론·값 반환 관례를 다뤘습니다. return local만 사용하고, 이동에 noexcept를 붙이며, 반환 경로를 단순화합니다. 다음 장(05)에서는 임시 객체 제거—참조 전달·explicit·+=—를 다룹니다.

- **다음 장(05)**: 임시 객체 제거 — operator+ vs +=, explicit, 참조 전달.
- **연계**: 03(문자열), 05(임시 제거), 15(Parameter Passing).
- **복습**: "이 장을 읽은 후 확인할 수 있는 것" 다섯 항목을 설명할 수 있으면 04를 완료한 것입니다.

**요약 (한 줄)**: 04 = RVO/NRVO + return local + 이동 noexcept. 05 = 임시 제거. 위 항목을 설명할 수 있으면 05로 진행하세요.

### 참고: C++17 mandatory copy elision

C++17에서 일부 prvalue는 "구체화 시점"에 직접 대상 객체를 초기화하는 것으로 규정되어, 복사/이동 생성자가 호출되지 않을 수 있습니다. 이는 반환 시에도 적용될 수 있어, return local과 함께 RVO/NRVO가 더욱 일관되게 동작합니다. 컴파일러는 -O2 이상에서 이를 적용하므로, return std::move(local)을 피해 NRVO를 유지하는 것이 여전히 중요합니다.

### 정리 (최종)

(1) Copy Elision·RVO·NRVO는 반환 위치에 직접 객체를 구성해 비용을 제거한다. (2) return local만 쓰고 return std::move(local)은 쓰지 않는다. (3) 이동 생성자/대입은 noexcept를 붙인다. (4) 반환 경로는 단일 return으로 단순화한다. (5) 값 반환은 현대 C++에서 권장된다. (6) 다음 장 05에서는 임시 객체 제거를 다룬다.

**다음 단계**: 05(임시 객체 제거)에서 참조 전달·explicit·+=를 배우면, 인자 경로의 임시를 줄일 수 있습니다. 04(값 반환)와 05(참조 전달)를 함께 적용하면 인자·반환 모두에서 불필요한 복사를 최소화할 수 있습니다.

**챕터 04 완료 조건**: RVO/NRVO·return local·이동 noexcept를 설명하고, 호출 횟수·벤치마크로 검증할 수 있으면 완료입니다.

### 실무 팁 (확장)

- **레거시 코드**: "return std::move(local)" 패턴을 검색해 제거하고, 반환 경로가 복잡하면 단일 return으로 정리할 수 있는지 검토합니다.
- **이동 불가 타입**: 복사만 가능한 타입은 값 반환 시 복사가 선택될 수 있어, 반환 횟수가 많은 경로에서는 참조로 받아 채우는(out 인자) 패턴을 고려할 수 있습니다. 단, RVO가 적용되면 복사가 생략되므로, 먼저 반환 경로를 단순화해 봅니다.
- **컨테이너 반환**: vector 등을 값으로 반환할 때 RVO/NRVO 또는 이동으로 비용이 줄어들므로, 값 반환을 권장합니다.

### 이 장의 평가 기준 재확인

이 장을 읽은 후 다음을 할 수 있어야 합니다: (1) Copy Elision·RVO·NRVO의 조건을 설명할 수 있다. (2) 반환 시 선택 순서(RVO/NRVO → 이동 → 복사)를 구분할 수 있다. (3) return std::move(local)이 NRVO를 깨는 이유를 설명하고 return local 관례를 적용할 수 있다. (4) 이동 후 객체의 valid but unspecified 의미를 설명할 수 있다. (5) 복사/이동/RVO 세 형태로 벤치마크를 나누어 검증할 수 있다. 위를 달성했다면 챕터 05(임시 객체 제거)로 진행합니다.

### 구분: 이 장의 범위와 선후 관계 (최종)

| 구분 | 내용 |
|------|------|
| 이 장(04)의 범위 | Copy Elision·RVO/NRVO·이동·값 반환·return local |
| 다음 장(05) | 임시 객체 제거: 참조 전달·explicit·+= |
| 연계 챕터 | 03(문자열), 05(임시 제거), 15(Parameter Passing) |

**마무리 (한 줄)**: 04 = RVO/NRVO + return local + 이동 noexcept. 05 = 임시 제거(참조·explicit·+=). 위 평가 기준을 설명할 수 있으면 05로 넘어가세요.

### 요약 표 (한눈에)

| 항목 | 요약 |
|------|------|
| RVO/NRVO | 반환 위치에 직접 구성; return local |
| return std::move(local) | NRVO 깨짐; 금지 |
| 이동 | noexcept; valid but unspecified |
| 값 반환 | T f(); return local; T result = f(); |

(이상으로 챕터 04 객체 수명 최적화를 마칩니다. 다음 장 05에서는 임시 객체 제거를 다룹니다.)

- **다음**: [임시 객체 제거](/collection/optimization-01-cpp-language/05-temporary-removal/) (챕터 05)

**참고**: 객체 수명 최적화는 "값 반환"과 "이동"을 함께 이해하는 것이 핵심입니다. 03(문자열)에서 string을 값으로 반환할 때, 04의 RVO/NRVO와 이동이 적용됩니다. 05(임시 제거)에서는 인자 쪽 임시를 참조 전달·explicit·+=로 줄이므로, 04와 05를 함께 적용하면 인자·반환 경로 모두 최적화할 수 있습니다.

**정리 (최종)**: (1) RVO/NRVO로 반환 시 비용 제거. (2) return local만 사용. (3) 이동 noexcept. (4) 값 반환 권장. (5) 다음 05 = 임시 제거.

**챕터 04 끝.** 다음 장(05)에서는 연산자 오버로딩·암시적 변환·연속 연산에서 임시가 생기는 패턴을 진단하고, 참조 전달·explicit·+= 등으로 제거하는 방법을 정리합니다. 04와 05를 연이어 학습하면 인자·반환 경로의 복사·임시를 체계적으로 줄일 수 있습니다.

- **복습**: RVO·NRVO·return local·이동 noexcept·valid but unspecified를 설명할 수 있으면 04를 완료한 것입니다.
- **다음 장(05)**: 임시 객체 제거 — operator+ vs +=, explicit, const T&/T&&.

**요약 (한 줄)**: 04 = RVO/NRVO + return local + 이동(noexcept). 05 = 임시 제거. 위 항목을 설명할 수 있으면 05로 진행하세요.

(챕터 04 객체 수명 최적화 끝. 다음은 05 임시 객체 제거입니다.)

- **이 장의 범위**: Copy Elision·RVO/NRVO·이동·값 반환·return local.
- **다음**: [임시 객체 제거](/collection/optimization-01-cpp-language/05-temporary-removal/) (챕터 05).

---

## 다음 장에서는

**임시 객체 제거**를 다룹니다. 연산자 오버로딩·암시적 변환·연속 연산에서 임시가 생기는 패턴을 진단하고, 참조 전달·explicit·+= 등으로 제거하는 방법을 정리합니다.

→ [임시 객체 제거](/collection/optimization-01-cpp-language/05-temporary-removal/) (챕터 05)
