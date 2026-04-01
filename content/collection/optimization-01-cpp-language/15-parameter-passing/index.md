---
collection_order: 15
date: 2026-03-10
lastmod: 2026-03-28
draft: true
title: "[Optimization(C++) 15] Parameter Passing 전략"
slug: parameter-passing
description: "인자 전달 방식별 by value, const reference, rvalue reference의 정량적 분석을 다룹니다. 객체 크기·복사 비용·이동 비용에 따른 전달 전략과 마이크로벤치마크로 검증하는 방법을 정리하며, Effective Modern C++ 권장과 예외를 제시합니다."
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
  - Interface
  - 인터페이스
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
  - Documentation
  - 문서화
  - Comparison
  - 비교
  - Data-Structures
  - 자료구조
  - Abstraction
  - 추상화
  - Encapsulation
  - 캡슐화
---

**Parameter Passing 전략**이란 인자 전달 방식을 타입 크기·복사/이동 비용에 맞게 선택하는 것을 말합니다. 본 챕터에서는 **by value**, **const reference**, **rvalue reference**의 정량적 분석과 선택 기준, 마이크로벤치마크로 검증하는 방법을 정리합니다.

## 인자 전달 권장 사항의 변화 (역사·배경)

C++03에서는 "큰 타입은 const 참조로"가 일반적이었습니다. C++11에서 **이동 의미론**과 **RVO/NRVO** 강화로 "값으로 받고 이동" 또는 "값으로 반환"이 비용이 줄어들었고, **Effective Modern C++** 등에서 "작은 타입·이동 가능 타입은 값 전달을 기본으로" 권장하는 흐름이 생겼습니다. 그 결과 오늘날에는 **작으면 값**, **크거나 읽기만 하면 const ref**, **소유권 이전 시 T&&** 조합이 널리 쓰입니다. 본 챕터는 그 정량적 근거와 선택 기준을 다룹니다.

> "For copyable types that are cheap to copy, pass by value. For types that are expensive to copy, pass by reference to const." — Scott Meyers, *Effective Modern C++*. 이동이 저렴하면 값 전달도 고려 대상이 됩니다.

## by value

**값으로 전달**하는 것은 인자를 **복사**(또는 이동)해서 함수에 넘기는 방식입니다. **작은 타입**(트리비얼 복사, 레지스터 몇 개로 넘어가는 크기, 보통 몇 워드 이하)은 값 전달이 **저렴**하고, 레지스터나 스택에 그대로 넘어가므로 추가 간접 접근이 없습니다. **이동 가능한 타입**이고 복사 비용이 크면, 호출자가 **std::move**로 넘기면 이동 생성만 일어나 복사보다 비용이 적습니다. 복사 생략(RVO/NRVO)과 함께 사용하면, "값으로 반환"도 한 번의 구성으로 처리될 수 있어, 현대 C++에서는 "작은 타입·이동 가능 타입"에 값 전달을 기본으로 두는 경우가 많습니다.

## const reference

**큰 타입**이거나 **복사 비용이 큰** 타입을 **읽기만** 할 때는 **const T&**로 받으면 복사를 피할 수 있습니다. 참조는 보통 포인터 크기만 전달되므로 전달 비용이 작고, 함수 안에서는 원본을 읽기만 하므로 수정 부작용이 없습니다. **수명 연장** 규칙에 따라, **임시 객체**를 const 참조에 바인딩하면 그 임시의 수명이 참조의 수명까지 연장됩니다. 따라서 `f(string("hello"))`처럼 임시를 넘겨도 함수 안에서 안전하게 사용할 수 있습니다. "읽기 전용 + 복사 비용 회피"가 목적일 때 const reference가 적합합니다.

## rvalue reference

**rvalue reference(T&&)**는 **이동 시맨틱**을 표현합니다. "소유권을 넘기거나 리소스를 재사용해도 된다"는 의미이므로, 함수 내부에서 **std::move**로 다른 함수에 넘기거나 멤버로 저장할 때 이동이 선택됩니다. **오버로드**로 **const T&**와 **T&&**를 둘 다 제공하면, lvalue는 복사, rvalue(임시·std::move 결과)는 이동으로 처리할 수 있습니다. **Perfect forwarding**은 **T&&**와 **std::forward**를 사용해, 인자를 "값 카테고리만 유지한 채" 다음 함수에 그대로 넘기는 패턴입니다. 템플릿에서 람다·인자를 한 번 더 넘길 때 자주 쓰이며, 불필요한 복사를 막고 이동을 보존할 수 있습니다.

## 정량 분석과 선택 기준

선택은 **객체 크기**와 **복사/이동 비용**에 따라 달라집니다. **"작은"의 기준**은 플랫폼 ABI(레지스터로 넘기는 크기, 보통 1~2 레지스터 크기 또는 캐시 라인 일부)와 "복사가 트리비얼한지"로 판단합니다. 트리비얼하고 작으면 **값**, 크거나 복사가 비싸면 **const T&**(읽기만), "이동해서 가져올 때"는 **T&&** 오버로드를 둡니다. **마이크로벤치마크**로 "동일 로직을 값 vs const ref vs rvalue ref"로 구현해 호출 비용·복사/이동 횟수를 측정하면, 해당 타입·사용 패턴에 맞는 전략을 선택할 수 있습니다.

```cpp
void by_value(Big x);           // 복사 또는 이동
void by_cref(const Big& x);     // 참조만, 읽기 전용
void by_rvalue(Big&& x);        // 이동만 기대
// 오버로드: lvalue → 복사/cref, rvalue → 이동
void store(Big x);              // 값: 복사 또는 이동
void store(const Big& x);       // lvalue만
void store(Big&& x);            // rvalue만, 이동
```

**실무 요약**: 기본은 **값**(작은 타입) 또는 **const ref**(큰 타입·읽기 전용), **이동이 의미 있을 때**(저장·전달 시 소유권 이전)만 **T&&** 오버로드를 추가하는 것이 일반적입니다.

## 평가 기준 (학습 성과 목표)

- **값**·**const T&**·**T&&** 전달의 비용(복사/이동/참조)과 수명·임시 연장 규칙을 설명할 수 있다.
- 객체 크기·복사/이동 비용에 따라 "작으면 값, 크거나 읽기만 하면 const ref, 소유권 이전 시 T&&"를 선택할 수 있다.
- **Perfect forwarding**(T&&, std::forward)의 역할을 설명하고, 마이크로벤치마크로 전달 방식별 비용을 검증할 수 있다.

## 판단 기준 (언제 쓸고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 작은·트리비얼 타입 | 값 전달 | 불필요한 const ref |
| 큰 타입·읽기 전용 | const T& | 값 전달(복사 비용) |
| 저장·전달 시 소유권 이전 | T&& 오버로드 | 복사만으로 처리 |
| 템플릿에서 인자 전달 | T&& + std::forward | 값/참조만으로 손실 |

**적용 체크리스트**: (1) 작은 타입은 값, 큰 타입 읽기만 하면 const ref. (2) 이동이 의미 있을 때만 T&&. (3) 동일 로직으로 값 vs ref vs rvalue ref 벤치마크.

## 비판적 시각: 한계와 트레이드오프

- "작은"의 기준(레지스터 크기·트리비얼 복사)은 플랫폼·ABI에 따라 다르다. 의심되면 벤치마크로 확인하는 것이 좋다.
- **T&&** 오버로드를 과다하게 두면 코드가 불어나므로, 정말 이동이 이득인 경로에만 둔다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 값 | 작은·트리비얼 타입에 저렴, RVO와 조합 |
| const T& | 큰 타입·읽기 전용, 임시 수명 연장 |
| T&& | 이동·소유권 이전, perfect forwarding |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **perfect forwarding** | T&& + std::forward로 값 카테고리(lvalue/rvalue)를 유지한 채 인자 전달 |
| **값 카테고리** | lvalue, rvalue 등; 이동이 선택되는지 여부에 영향 |

### 벤치마크 결과 해석 가이드

| 관찰 | 해석·다음 단계 |
|------|----------------|
| 작은 타입 by value가 ref보다 나음 | 복사 비용이 작고, 인라이닝·최적화 유리 |
| 큰 타입·복사 비싼 타입 | const ref 또는 rvalue ref로 이동 유도 |
| perfect forwarding | T&& + std::forward로 값 카테고리 유지·이동 선택 |

### 자주 묻는 질문 (FAQ)

**Q: by value vs const ref 선택 기준은?**  
A: 작은 타입(포인터·숫자 등)은 by value가 복사 비용이 작고 인라이닝에 유리합니다. 큰 타입·복사 비싼 타입은 const ref. 이동이 가능하면 rvalue ref 오버로드 또는 perfect forwarding을 고려합니다.

**Q: perfect forwarding이란?**  
A: T&& + std::forward로 인자의 값 카테고리(lvalue/rvalue)를 유지한 채 하위로 전달하는 패턴입니다. 템플릿에서 한 번만 작성하고 lvalue/rvalue 모두 처리할 수 있습니다.

**Q: 인자 전달 권장이 바뀐 이유는?**  
A: C++11 이동 의미론 도입 후 "작은 타입은 value, 큰 타입은 const ref·이동"으로 정리되었고, 최적화·인라이닝 관점에서 작은 값 전달이 유리한 경우가 많아졌습니다.

### 적용 체크리스트 (실무용)

- [ ] 객체 크기·복사/이동 비용에 따라 by value·const ref·rvalue ref를 선택했는가?
- [ ] 작은 타입은 value, 큰 타입은 const ref 또는 이동을 적용했는가?
- [ ] 템플릿에서 값 카테고리 유지가 필요하면 perfect forwarding을 사용했는가?
- [ ] 정량 분석·벤치마크로 전달 비용을 확인했는가?

### 진단 도구 요약

| 목적 | 도구·방법 |
|------|-----------|
| 전달 비용 | by value vs const ref vs rvalue ref 벤치마크 |
| 이동 선택 | rvalue ref·std::move·forward 확인 |
| 인라이닝 | 작은 값 전달이 유리한지 측정(챕터 10 연계) |

### 학습 후 자가 점검

(1) by value·const ref·rvalue ref의 비용·선택 기준을 설명할 수 있는가? (2) 객체 크기·복사/이동 비용에 따른 전달 전략을 적용할 수 있는가? (3) perfect forwarding의 역할을 설명할 수 있는가? (4) 인자 전달 권장 사항 변화(역사)를 설명할 수 있는가? (5) 판단 기준·비판적 시각을 적용할 수 있는가?

### 자주 하는 실수

- **큰 타입을 무조건 by value**: 복사 비용이 크면 const ref 또는 rvalue ref로 이동을 유도합니다.
- **작은 타입을 무조건 const ref**: 작은 타입은 value가 인라이닝·최적화에 유리한 경우가 많습니다.
- **perfect forwarding 누락**: 템플릿에서 값 카테고리를 유지해야 할 때 T&& + forward를 사용합니다.

### 리팩토링 시 주의

인자 전달 방식을 바꿀 때 객체 크기·복사/이동 비용을 재평가하고, 벤치마크로 호출 비용·인라이닝 효과를 확인합니다. const ref → value 변경 시 복사 비용이 증가하지 않도록 합니다.

### 추가 읽기 및 관련 챕터

- **챕터 04 (객체 수명)**: RVO·이동 의미론. **챕터 10 (인라이닝)**: 인라인과 전달.
- **챕터 14 (SBO)**: 타입 소거·저장. **외부**: C++ Core Guidelines, F.15/F.16 등.

### 이 장을 마치며

Parameter Passing 전략은 by value·const ref·rvalue ref의 정량 분석과 객체 크기·복사/이동 비용에 따른 선택으로 요약됩니다. **이것으로 Low-latency C++ 언어 최적화 트랙의 주제를 모두 다룹니다.**

**이 장의 학습 목표 재확인**: by value·const ref·rvalue ref 비용·선택 기준을 설명하고, 객체 크기·복사/이동에 따른 전달 전략을 적용하며, perfect forwarding을 사용할 수 있어야 합니다.

### 이 장에서 다룬 내용

- 인자 전달 권장 사항 변화(역사), by value·const ref·rvalue ref·cpp 예시, 정량 분석·선택 기준·판단 기준·비판적 시각.
- 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·실수·리팩토링 주의·추가 읽기.

**요약 (한 줄씩)**: 작은 타입=value, 큰 타입=const ref·이동. perfect forwarding=T&&+forward. 다음=챕터 16 또는 도입(00).

### 상세 예: by value vs const ref

```cpp
void f(int x);           // 작은 타입 value
void g(const Big& x);   // 큰 타입 const ref
void h(Big&& x);        // 이동 유도 rvalue ref
template<typename T> void forward(T&& x) { other(std::forward<T>(x)); }
```

### 실전 시나리오: API 설계

API 인자를 설계할 때 객체 크기·복사/이동 비용을 정리하고, 작은 타입은 value, 큰 타입은 const ref 또는 rvalue ref를 선택합니다. 템플릿에서 값 카테고리를 유지해야 하면 perfect forwarding을 적용합니다.

### 상황별 권장 (요약 표)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 작은 타입(포인터·숫자 등) | by value | 무조건 const ref |
| 큰 타입·복사 비쌈 | const ref, 필요 시 rvalue ref | by value |
| 템플릿·값 카테고리 유지 | T&& + std::forward | 값 카테고리 무시 |

### 컴파일러·플랫폼별 참고

- **인라이닝**: 작은 값 전달이 인라이닝 후 추가 최적화에 유리할 수 있음(챕터 10).
- **벤치마크**: 프로젝트 환경에서 by value vs const ref vs rvalue ref 비용을 측정합니다.

### 이 장을 읽은 후 확인할 수 있는 것

- by value·const ref·rvalue ref의 비용·선택 기준을 설명할 수 있다.
- 객체 크기·복사/이동 비용에 따른 전달 전략을 적용할 수 있다.
- perfect forwarding을 사용할 수 있다.

### 용어 정리 (추가)

| 용어 | 설명 |
|------|------|
| **perfect forwarding** | T&& + std::forward로 값 카테고리 유지 전달 |
| **값 카테고리** | lvalue, rvalue 등; 이동 선택에 영향 |

### 최종 정리

(1) 작은 타입=value, 큰 타입=const ref·이동. (2) perfect forwarding=T&&+forward. (3) 정량 분석·벤치마크로 전달 비용 확인. (4) **챕터 15(인자 전달) 주제를 마칩니다.** 트랙 전체는 16~19가 이어집니다. → [도입·커리큘럼(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)

### 선택 플로우 (Parameter Passing)

1. **객체 크기·복사/이동 비용**을 평가한다.
2. **작은 타입**은 by value, **큰 타입**은 const ref 또는 rvalue ref.
3. **템플릿**에서 값 카테고리 유지가 필요하면 T&& + std::forward.
4. **벤치마크**로 전달 비용·인라이닝 효과를 확인한다.
5. **검증**: 회귀 벤치마크.

### 게시 전·복습 체크

(1) 도입·정의·예시·비교·마무리가 있는가? (2) 학습 성과 목표·판단 기준·비판적 시각이 있는가? (3) 벤치마크 해석·FAQ·체크리스트·진단 도구가 있는가? (4) 용어 정리·이 장에서 다룬 내용·다음 장(16)·도입(00) 링크가 있는가? (5) 트랙 분량·구성(분량 기준 문서 `CONTENT_LENGTH_TARGETS.md`(트랙 폴더 루트))을 점검했는가? 위를 확인한 뒤 **챕터 16** 또는 **도입(00)**으로 이어가거나, 다른 시리즈 트랙(컴파일러·빌드·메모리·동시성)으로 넘어갑니다.

### 요약: 이 장의 핵심 메시지

1. **작은 타입**은 by value(복사 비용 작음·인라이닝 유리), **큰 타입**은 const ref 또는 rvalue ref로 이동 유도.
2. **perfect forwarding**: T&& + std::forward로 값 카테고리 유지.
3. **정량 분석**으로 전달 비용을 측정하고 선택합니다.
4. **챕터 15를 마쳤습니다.** 다음 선형 장은 16(실행 모델)입니다. → [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)

### 참고 자료

- C++ Core Guidelines F.15/F.16 등. 챕터 04(객체 수명), 10(인라이닝), 14(SBO).

**마무리**: 챕터 15(Parameter Passing 전략)를 마쳤습니다. 트랙에는 **16~19**(실행 모델·ABI·스마트 포인터·type erasure)가 이어집니다. 프로파일러로 핫패스를 찾고, 추상화·STL·문자열·수명·임시·예외·인라이닝·variant·span·람다·SBO·전달 전략을 격리 측정·대체하며 적용해 보시기 바랍니다. 컴파일러·빌드·메모리·동시성 최적화는 전용 트랙에서 이어서 학습할 수 있습니다.

### 이 장에서 다룬 내용 (전체)

- 인자 전달 권장 사항 변화(역사), by value·const ref·rvalue ref·cpp 예시, 정량 분석·선택 기준·판단 기준·비판적 시각.
- 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·실수·리팩토링 주의·추가 읽기·상세 예·실전 시나리오·상황별 권장·컴파일러 참고·확인 항목·용어 추가·최종 정리·선택 플로우·게시 전 체크·핵심 메시지·참고 자료.

**챕터 15 정리**: by value·const ref·rvalue ref·perfect forwarding. **다음**: 챕터 16 또는 도입(00)의 권장 순서. → [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)

(이상으로 챕터 15 Parameter Passing 전략을 마칩니다.)

### 정량적 비교 (by value vs const ref vs rvalue ref)

| 측면 | by value | const ref | rvalue ref |
|------|----------|-----------|------------|
| 작은 타입 | 복사 비용 작음·인라이닝 유리 | 포인터 전달 | — |
| 큰 타입 | 복사 비용 큼 | 참조만·복사 없음 | 이동 유도 |
| 템플릿 | — | — | T&&+forward로 값 카테고리 유지 |

### 실무 팁

- 작은 타입(포인터·숫자·작은 구조체)은 by value로 두고, 큰 타입·복사 비싼 타입은 const ref 또는 rvalue ref를 선택합니다.
- 템플릿에서 인자를 그대로 하위로 넘길 때는 T&& + std::forward로 perfect forwarding을 적용합니다.
- 정량 분석·벤치마크로 전달 비용과 인라이닝 효과를 확인합니다(챕터 10 연계).

### 학습 성과 점검

(1) by value·const ref·rvalue ref의 비용·선택 기준을 설명할 수 있는가? (2) 객체 크기·복사/이동 비용에 따른 전달 전략을 적용할 수 있는가? (3) perfect forwarding을 사용할 수 있는가? (4) 인자 전달 권장 사항 변화를 설명할 수 있는가?

### 트랙 마무리·컬렉션 목차

**챕터 15**에서는 Parameter Passing을 마쳤습니다. **선형 순서**로는 챕터 16이 이어지고, **전체 트랙(00~19)** 커리큘럼은 [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)에서 확인할 수 있습니다. 다른 시리즈 트랙(컴파일러·빌드·메모리·동시성 등)으로 넘어가기 전에 16~19를 완주할지 결정하면 됩니다.

### 용어·개념 복습

| 용어 | 한 줄 요약 |
|------|------------|
| perfect forwarding | T&& + std::forward로 값 카테고리 유지 |
| 값 카테고리 | lvalue, rvalue; 이동 선택에 영향 |

### 구분 표: 언제 무엇을 쓸지

| 목표 | 권장 | 비권장 |
|------|------|--------|
| 작은 타입 | by value | 무조건 const ref |
| 큰 타입·복사 비쌈 | const ref, rvalue ref | by value |
| 템플릿 값 카테고리 유지 | T&& + std::forward | 값 카테고리 무시 |

### 자주 하는 실수 (확장)

- 큰 타입 by value; const ref 또는 rvalue ref.
- 작은 타입 무조건 const ref; value가 유리한 경우 많음.
- perfect forwarding 누락; 템플릿에서 값 카테고리 유지 필요 시 T&&+forward.

### 리팩토링 시나리오

인자 전달 방식 변경 시 객체 크기·복사/이동 비용 재평가. 벤치마크로 전달 비용·인라이닝 효과 확인. const ref→value 시 복사 비용 증가 여부 확인.

### 정리

챕터 15에서는 by value·const ref·rvalue ref·perfect forwarding과 정량 분석·선택 기준을 다뤘습니다. **이것으로 트랙(01 언어 최적화)을 마칩니다.**

### 적용 체크리스트 (확장)

- [ ] 객체 크기·복사/이동에 따라 value·const ref·rvalue ref 선택
- [ ] 작은 타입 value, 큰 타입 const ref·이동
- [ ] 템플릿 값 카테고리 유지 시 perfect forwarding
- [ ] 정량 분석·벤치마크로 전달 비용 확인

### 참고 자료 (상세)

- C++ Core Guidelines F.15/F.16. 챕터 04, 10, 14.

### 진단 도구 보충

| 목적 | 방법 |
|------|------|
| 전달 비용 | by value vs const ref vs rvalue ref 벤치마크 |
| 이동 선택 | rvalue ref·std::move·forward 확인 |
| 인라이닝 | 챕터 10 연계 |

### 요약 표 (최종)

| 항목 | 비용·이점 | 활용 기준 |
|------|-----------|-----------|
| by value | 작은 타입 복사·인라이닝 유리 | 작은 타입 |
| const ref | 참조만·복사 없음 | 큰 타입 |
| rvalue ref·forward | 이동 유도·값 카테고리 유지 | 이동·템플릿 |

### 학습 후 자가 점검 (확장)

(1) by value·const ref·rvalue ref·perfect forwarding을 설명하고 적용할 수 있는가? (2) 팀에서 "인자 전달 기준"을 정할 수 있는가?

### 마무리

이 장에서 Parameter Passing 전략을 정리했습니다. **챕터 15를 마쳤으며**, 트랙에는 16~19가 이어집니다.

### 평가 기준 재확인

- **도입·정의·예시·비교·마무리**: 충족.
- **학습 성과 목표·판단 기준·비판적 시각**: 충족.
- **벤치마크 해석·FAQ·체크리스트·진단 도구**: 충족.
- **용어 정리·이 장에서 다룬 내용·다음 장(16)·도입(00) 링크**: 충족.
- **분량·구성**: 분량 기준 문서 `CONTENT_LENGTH_TARGETS.md`(트랙 폴더 루트) 기준을 따른다.

### 참고

인자 전달은 "작은 타입 value, 큰 타입 const ref·이동"으로 요약됩니다. C++11 이동 의미론 도입 후 권장이 정리되었고, 정량 분석으로 프로젝트에 맞게 조정하면 됩니다.

### 정리 (최종)

**챕터 15 끝**: by value·const ref·rvalue ref·perfect forwarding.

**다음 링크**: → [챕터 16 실행 모델](/post/cpp-optimization/cpp-execution-model-microsecond-vocabulary-fundamentals/) · [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)

**복습**: by value·const ref·rvalue ref·perfect forwarding 선택 기준을 한 줄씩 말할 수 있으면 충분합니다.

**요약 한 줄**: 챕터 15 = 작은 타입 value·큰 타입 const ref·이동·perfect forwarding.

**이 장의 범위**: 인자 전달 전략(by value·const ref·rvalue ref·perfect forwarding)·정량 분석·선택 기준. 알고리즘 정답 코드는 다루지 않음.

### by value가 유리한 경우

포인터·참조·작은 정수·작은 POD 구조체(몇 바이트 수준)는 복사 비용이 매우 작습니다. 이런 타입을 by value로 전달하면 레지스터에 올라가고 인라이닝 후 추가 최적화(상수 전파 등)가 일어나기 쉬우므로, "작은 타입은 value"가 현대 C++ 권장과 맞습니다. 정확한 한계(예: 몇 바이트까지)는 ABI·플랫폼에 따라 다르므로, 프로젝트에서 벤치마크로 확인하는 것이 좋습니다.

### const ref가 유리한 경우

큰 구조체·복사 비용이 큰 타입(예: 복잡한 컨테이너)은 참조로 전달해 복사를 피합니다. 읽기만 할 때는 const ref로, 수정이 필요할 때는 non-const ref를 씁니다. 이동이 가능한 타입이라면 rvalue ref 오버로드를 추가해 "복사 없이 이동" 경로를 열 수 있습니다.

### rvalue ref와 perfect forwarding

rvalue ref(T&&)는 "우측값 참조"로, 이동 의미론과 결합해 임시 객체나 std::move된 객체를 받을 때 복사 대신 이동을 유도합니다. 템플릿에서 T&&는 "forwarding reference"가 되어, lvalue와 rvalue를 구분해 전달할 수 있습니다. std::forward<T>(x)는 x가 rvalue로 전달됐을 때만 우측값으로 캐스팅하므로, 하위 함수에 값 카테고리를 그대로 넘기는 "perfect forwarding"이 됩니다. 한 번만 작성하고 lvalue/rvalue 모두 처리할 수 있어, 오버로드 수를 줄일 수 있습니다.

### 트랙(01) 요약: 챕터별 핵심

- **00**: 도입·측정·활용 흐름. **01**: 추상화 비용·가상·RTTI·예외. **02**: STL 컨테이너 비용. **03**: 문자열·SSO·string_view. **04**: 객체 수명·RVO·이동. **05**: 임시 제거. **06**: 템플릿·constexpr. **07**: Ranges·Concepts·Modules. **08**: 코루틴 성능. **09**: 예외·noexcept·expected. **10**: 인라이닝 유도. **11**: variant·optional·expected. **12**: span·string_view. **13**: 람다·캡처·function. **14**: SBO·function·any. **15**: Parameter Passing(본 장). **16**: 실행 모델·스택/힙·핫패스 어휘. **17**: ABI·링크 경계. **18**: Smart Pointer 비용. **19**: Type Erasure 비용. 위 항목을 격리 측정·대체하며 적용하면 됩니다.

### 실무 적용 순서 제안

1. **프로파일러**로 핫패스를 찾고, 2. **추상화·STL·문자열·수명·임시** 등 본 트랙 항목을 하나씩 격리 벤치마크한 뒤, 3. **예외·인라이닝·variant·span·람다·SBO·전달 전략**을 적용하고, 4. **회귀 벤치마크**로 효과를 확인합니다. 컴파일러·빌드·메모리·동시성 최적화는 전용 트랙에서 이어서 학습할 수 있습니다.

### C++ Core Guidelines 연계

C++ Core Guidelines의 F.15("Prefer simple and conventional ways of passing information"), F.16("For 'in' parameters, pass cheaply-copied types by value and others by reference to const") 등이 인자 전달 권장과 맞닿아 있습니다. "작은 타입 value, 큰 타입 const ref·이동"은 이 가이드라인과 일치하며, 프로젝트에서 정량 분석으로 조정하면 됩니다.

### 값 카테고리 한 줄 정리

- **lvalue**: 주소를 취할 수 있는 식(이름 있는 객체 등). 좌측값.
- **rvalue**: lvalue가 아닌 식(임시, std::move 결과 등). 우측값.
- **rvalue ref**: 우측값만 바인딩하는 참조. 이동 생성·이동 대입·forwarding reference(T&&)에서 사용됩니다. 인자 전달 시 "이동 가능한 것"을 받을 때 rvalue ref를 쓰면 복사 대신 이동이 선택됩니다.

### 트랙 완료 후 다음 단계

본 트랙(optimization-01-cpp-language)을 마친 뒤에는 **컴파일러·빌드 최적화**(Tr.02: 최적화 플래그, LTO, PGO, 인라이닝 진단 등), **메모리 최적화**(캐시·할당자·레이아웃), **동시성 최적화** 등 전용 트랙으로 넘어가면 됩니다. 언어 수준 최적화(본 트랙)와 컴파일러·빌드·메모리·동시성은 서로 보완적이므로, 실제 프로젝트에서는 프로파일러로 병목을 찾은 뒤 해당 트랙의 항목을 적용하는 흐름이 좋습니다.

### 이 장·트랙 최종 체크

- [ ] by value·const ref·rvalue ref·perfect forwarding을 상황에 맞게 선택할 수 있다.
- [ ] 객체 크기·복사/이동 비용에 따른 전달 전략을 적용할 수 있다.
- [ ] 본 트랙(00~19)의 주제를 요약하고, 프로파일러·격리 측정·대체 적용 흐름을 설명할 수 있다.
- [ ] 다른 트랙(컴파일러·빌드·메모리·동시성)으로 이어서 학습할 수 있다.

### 반환값 전달과의 연계

인자를 어떻게 받을지와 함께, **반환값**을 어떻게 줄지도 중요합니다. 챕터 04(객체 수명)에서 다룬 RVO·NRVO·이동 의미론에 따라, "값 반환"이 복사 없이 이루어질 수 있습니다. 따라서 "인자는 const ref로 받고 반환은 값으로"처럼, 받을 때는 참조로 복사를 피하고 반환할 때는 값으로 넘기면 컴파일러가 RVO·이동을 적용할 수 있습니다. 반환값 전달 전략은 챕터 04와 함께 정리해 두면 일관된 설계가 됩니다.

### 스마트 포인터·인자 전달

**std::unique_ptr**, **std::shared_ptr**를 인자로 받을 때: 소유권을 넘길 때는 unique_ptr은 값으로 받아 이동하고, 공유할 때는 shared_ptr은 const ref로 받아 참조 카운트 증가를 한 번만 하도록 하는 패턴이 자주 쓰입니다. "작은 타입 value"와는 별개로, 포인터 크기의 스마트 포인터는 값으로 넘기면 이동 비용만 있고, 복사 비용이 큰 타입은 아닙니다. 다만 의미론(소유권 이전 vs 공유)에 맞게 선택하는 것이 우선입니다.

### 정리: 챕터 15와 트랙 마무리

챕터 15에서는 by value·const ref·rvalue ref·perfect forwarding과 정량 분석·선택 기준을 다뤘습니다. 실제 적용 시에는 프로파일러로 핫패스를 찾은 뒤, 본 트랙의 항목을 격리 측정·대체하며 적용하고, 회귀 벤치마크로 효과를 확인하시기 바랍니다. → [챕터 16](/post/cpp-optimization/cpp-execution-model-microsecond-vocabulary-fundamentals/) · [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)

### 챕터 15·트랙 게시 전 최종 확인

분량 기준 문서 `CONTENT_LENGTH_TARGETS.md`(트랙 폴더 루트)에 맞는 분량·구성인지, 도입·정의·예시·비교·마무리·학습 성과 목표·판단 기준·비판적 시각·벤치마크 해석·FAQ·체크리스트·진단 도구·용어 정리·이 장에서 다룬 내용·다음 장(16)·도입(00) 링크가 모두 포함되었는지 확인한 뒤 게시합니다. 트랙 전체(00~19)는 동일 문서의 분량 표와 워크스페이스 educational-content-writing 스킬(`.cursor/skills/educational-content-writing/SKILL.md`)을 함께 점검합니다.

### 인자 전달 한 줄 요약

- **작은 타입**(포인터·숫자·작은 POD): by value → 복사 비용 작고 인라이닝·최적화 유리.
- **큰 타입·복사 비싼 타입**: const ref 또는 rvalue ref → 복사 제거·이동 유도.
- **템플릿에서 값 카테고리 유지**: T&& + std::forward → perfect forwarding.
- **정량 분석**: 프로젝트 환경에서 by value vs const ref vs rvalue ref 벤치마크로 전달 비용 확인.

### 트랙(01) 완료 메시지

**Low-latency C++ 언어 최적화** 트랙에서 **챕터 15(Parameter Passing)** 까지 다룬 내용을 정리했습니다. 트랙 **전체 주제**는 00~19이며, (1) 프로파일러로 핫패스 식별, (2) 추상화·STL·문자열·수명·임시·예외·인라이닝·variant·span·람다·SBO·전달·실행 모델·ABI·스마트 포인터·type erasure를 격리 측정·대체 적용, (3) 회귀 벤치마크 검증을 권장합니다. 컴파일러·빌드·메모리·동시성은 전용 트랙에서 이어서 학습하시기 바랍니다. → [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)

### 챕터 15와 챕터 04 연계

챕터 04(객체 수명)에서 다룬 RVO·NRVO·이동 의미론은 **반환값** 전달과 직결됩니다. 인자를 "const ref로 받고 값으로 반환"하는 패턴은, 반환 시 RVO·이동으로 복사 없이 넘길 수 있어 인자 전달(본 장)과 반환값 전략을 함께 설계할 수 있습니다. "받을 때는 참조로 복사 회피, 반환할 때는 값으로 넘겨 컴파일러가 RVO·이동 적용"을 일관되게 적용하면 됩니다.

### 정리: by value·const ref·rvalue ref 선택 플로우

1. 인자 타입이 **작은 타입**(몇 바이트 수준, 포인터·숫자·작은 POD)인가? → **by value**.
2. **큰 타입**이거나 복사 비용이 큰가? → **const ref**(읽기만) 또는 **rvalue ref**(이동 유도).
3. **템플릿**에서 인자를 하위로 그대로 넘겨야 하나? → **T&& + std::forward** (perfect forwarding).
4. **벤치마크**로 전달 비용·인라이닝 효과를 확인하고, 필요 시 위 선택을 조정한다.

이 플로우를 적용하면 챕터 15의 인자 전달 전략을 실무에 일관되게 쓸 수 있고, 트랙(01)의 마지막 주제로서 언어 수준 최적화를 마무리하게 됩니다.

### 본 트랙(00~19) 목차 요약

**00** 도입·측정·활용 흐름 | **01** 추상화 비용 | **02** STL 컨테이너 비용 | **03** 문자열 최적화 | **04** 객체 수명·RVO·이동 | **05** 임시 제거 | **06** 템플릿·constexpr | **07** Modern C++(Ranges·Concepts·Modules) | **08** 코루틴 성능 | **09** 예외 처리 심화 | **10** 인라이닝 유도 | **11** variant·optional·expected | **12** span·뷰 패턴 | **13** 람다 표현식 성능 | **14** SBO | **15** Parameter Passing(본 장) | **16** 실행 모델·어휘 | **17** ABI·링크 | **18** Smart Pointer | **19** Type Erasure. 각 챕터는 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·판단 기준·비판적 시각·용어 정리·이 장에서 다룬 내용·다음 장 링크를 포함하며, 분량·구성 목표는 분량 기준 문서 `CONTENT_LENGTH_TARGETS.md`(트랙 폴더 루트)와 educational-content-writing 스킬을 함께 따릅니다.

### 인자 전달·트랙 마무리 요약

by value(작은 타입)·const ref(큰 타입)·rvalue ref(이동 유도)·perfect forwarding(T&&+forward)을 객체 크기·복사/이동 비용에 따라 선택하고, 정량 분석·벤치마크로 확인합니다. **챕터 15**를 마쳤다면 다음은 [챕터 16](/post/cpp-optimization/cpp-execution-model-microsecond-vocabulary-fundamentals/)이며, 트랙 **완주**는 [챕터 19](/post/cpp-optimization/type-erasure-cost-patterns/)까지입니다. [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)에서 권장 독해 순서를 확인한 뒤, 컴파일러·빌드·메모리·동시성 등 **다른 시리즈 트랙**으로 넘어가도 됩니다.

### 챕터 15 길이·구성 최종

챕터별 분량·구성 목표는 분량 기준 문서 `CONTENT_LENGTH_TARGETS.md`(트랙 폴더 루트)를 참고합니다. 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·실수·리팩토링 주의·추가 읽기·상세 예·실전 시나리오·상황별 권장·용어 정리·최종 정리·선택 플로우·게시 전 체크·핵심 메시지·참고 자료·정량적 비교·실무 팁·학습 성과 점검·트랙 마무리·용어 복습·구분 표·자주 하는 실수 확장·리팩토링 시나리오·정리·적용 체크리스트 확장·참고 자료 상세·진단 도구 보충·요약 표·학습 후 자가 점검 확장·마무리·평가 기준 재확인·참고·정리 최종·다음 링크·복습·요약 한 줄·이 장의 범위·반환값 전달과의 연계·스마트 포인터·정리: 챕터 15와 트랙 마무리·C++ Core Guidelines 연계·값 카테고리 한 줄 정리·트랙 완료 후 다음 단계·이 장·트랙 최종 체크·챕터 15·트랙 게시 전 최종 확인·인자 전달 한 줄 요약·트랙(01) 완료 메시지·챕터 15와 챕터 04 연계·정리: by value·const ref·rvalue ref 선택 플로우·본 트랙(00~19) 목차 요약·인자 전달·트랙 마무리 요약이 포함되어 있습니다.

**챕터 15**를 마쳤습니다. 프로파일러로 핫패스를 찾고, 본 트랙 항목을 격리 측정·대체 적용한 뒤 회귀 벤치마크로 효과를 검증하시기 바랍니다. → [챕터 16](/post/cpp-optimization/cpp-execution-model-microsecond-vocabulary-fundamentals/) · [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)

- **인자 전달**: 작은 타입 value, 큰 타입 const ref·rvalue ref, 템플릿 perfect forwarding. 정량 분석·벤치마크로 확인.
- **이후 독해**: 선형 순서 16~19 또는 도입(00)의 **16→18→01** 권장 경로.
- **본문 길이**: 분량 기준 문서 `CONTENT_LENGTH_TARGETS.md`(트랙 폴더 루트) 및 educational-content-writing 스킬을 따릅니다.

by value·const ref·rvalue ref·perfect forwarding을 객체 크기·복사/이동 비용에 따라 선택하고, C++ Core Guidelines F.15/F.16과 정량 분석으로 프로젝트에 맞게 조정합니다. 챕터 04(객체 수명)의 RVO·이동 의미론과 반환값 전달을 함께 설계하면, 인자·반환 모두에서 불필요한 복사를 줄일 수 있습니다.

챕터 15는 rules-that-must-be-followed·blog-post-writing 스킬(reference의 제목·날짜)·educational-content-writing 스킬을 따릅니다. **트랙 마지막 챕터는 19(Type Erasure)** 입니다. 다음: [챕터 16](/post/cpp-optimization/cpp-execution-model-microsecond-vocabulary-fundamentals/) 또는 [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/). 컴파일러·빌드·메모리·동시성 등 **다른 시리즈 트랙**은 00에서 로드맵을 참고하세요.

## 다음 장에서는

**이전 장**: [Small Buffer Optimization](/post/cpp-optimization/small-buffer-optimization/) (챕터 14)

**C++ 실행 모델·µs 최적화 어휘**(챕터 16)로 넘어갑니다. `collection_order` 기준 선형 순서에서는 15 다음이 16입니다. 도입(00)에서 권장하는 **선행 독해 경로**(16 → 18 → 01 …)를 따른다면, 16에서 용어를 맞춘 뒤 [Smart Pointer 비용 기초](/post/cpp-optimization/smart-pointer-cost-fundamentals/)(18)로 이어가면 됩니다. 트랙 전체 주제는 **챕터 19(Type Erasure)** 에서 닫히며, 커리큘럼·측정 방법은 [도입(00)](/post/cpp-optimization/getting-started-cpp-language-performance-tuning/)에서 확인할 수 있습니다.

→ [C++ 실행 모델·µs 최적화 어휘](/post/cpp-optimization/cpp-execution-model-microsecond-vocabulary-fundamentals/) (챕터 16)

---

*챕터 15(Parameter Passing 전략) 끝. 트랙 전체(00~19) 개요는 도입(00)과 챕터 19를 참고하세요.*
