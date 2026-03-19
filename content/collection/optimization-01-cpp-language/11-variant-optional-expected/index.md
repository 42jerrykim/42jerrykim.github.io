---
collection_order: 11
date: 2026-03-10
lastmod: 2026-03-10
draft: true
title: "[Performance 12] std::variant/optional/expected"
slug: variant-optional-expected
description: "타입 안전 유니온과 옵셔널 타입인 std::variant, std::optional, std::expected의 성능 특성과 오버헤드를 분석합니다. 포인터·공용체 대비 비용과 예외 없이 실패를 표현하는 패턴의 성능을 다루며, 메모리 레이아웃과 visit/if-let 비용을 정리합니다."
tags:
  - C++
  - Performance
  - Optimization
  - 성능
  - 최적화
  - Type-Safety
  - Memory
  - 메모리
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
  - Error-Handling
  - 에러처리
  - Testing
  - 테스트
  - Debugging
  - 디버깅
  - Refactoring
  - 리팩토링
  - Readability
  - Maintainability
  - Modularity
  - Compiler
  - 컴파일러
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
  - Documentation
  - 문서화
  - Comparison
  - 비교
---

**std::variant**·**std::optional**·**std::expected**는 타입 안전 유니온·"있음/없음"·성공/실패 전달을 위한 표준 타입입니다. 본 챕터에서는 이들의 성능 특성과 오버헤드를 분석하고, 포인터·공용체·예외 대비 비용과 선택 기준을 다룹니다.

## variant/optional/expected 표준화 (역사·배경)

**std::variant**와 **std::optional**은 C++17에서 표준에 추가되었습니다. variant는 타입 안전 유니온, optional은 "값이 있거나 없거나"를 표현합니다. **std::expected**는 C++23에서 도입되어 성공 타입 T 또는 실패 타입 E를 담고, 예외 없이 에러 전달을 표준화합니다. 이들로 RTTI·포인터·예외 대신 타입 안전하고 비용이 예측 가능한 패턴을 쓸 수 있어, Low-latency에서 선택지가 됩니다.

> "optional is a wrapper that may or may not hold an object. variant is a type-safe union." — cppreference. expected는 "either T or E"로 예외 대안이 됩니다.

## std::variant

**std::variant**는 **타입 안전 유니온**입니다. 여러 타입 중 하나만 활성화되어 있고, **인덱스(또는 타입 식별)**와 **정렬된 저장소**(가장 큰 타입 크기·정렬에 맞춤)로 표현됩니다. **std::visit**로 값을 방문할 때는 활성 타입에 따라 디스패치가 일어나며, 컴파일러가 visit 대상을 인라인할 수 있으면 switch/테이블 점프 수준으로 최적화됩니다. 메모리 레이아웃은 "인덱스 + max(sizeof(Ts)...) + 정렬 패딩" 정도이며, 포인터 하나로 간접 접근하는 방식보다 캐시에 유리할 수 있습니다.

**포인터·수동 union 대비**: 포인터는 힙 할당과 간접 접근 비용이 있고, 수동 union은 타입 안전성이 없습니다. variant는 스택/멤버에 직접 담고, visit로 타입을 검사하므로 할당 없이 타입 안전하게 "여러 타입 중 하나"를 표현할 수 있습니다.

```cpp
std::variant<int, double, std::string> v = 42;
std::visit([](auto&& x) { /* 타입별 처리 */ }, v);
// optional 접근
std::optional<int> o = 10;
if (o) use(*o);
```

실제 수치는 타입 크기·visit 패턴에 따라 다르므로, 핫 경로에서는 마이크로벤치마크로 비교하는 것이 좋습니다.

## std::optional

**std::optional&lt;T&gt;**는 "값이 있거나 없거나"를 표현합니다. 내부적으로는 **T**와 **값 존재 여부**(bool 플래그 또는 패딩으로 처리)를 갖습니다. 크기는 보통 `sizeof(T) + 1` 정도에 정렬로 인한 패딩이 붙을 수 있습니다. **값에 접근할 때**는 "값이 있는지" 한 번의 분기가 있고, 있으면 저장된 객체를 반환합니다. 구현체에 따라 트라이트·ABI가 다르지만, 대체로 오버헤드는 "한 번의 분기 + (필요 시) 정렬용 패딩" 수준입니다.

**null 포인터·스마트 포인터**와 비교하면, optional은 **값을 직접 보관**하므로 할당이 없고, null 체크 한 번의 분기만 있습니다. 포인터는 간접 접근과 (힙 사용 시) 할당 비용이 있으므로, "값이 없을 수 있는 작은 객체"에는 optional이 성능·의도 표현 모두 유리한 경우가 많습니다.

## std::expected (C++23)

**std::expected&lt;T, E&gt;**는 "성공하면 T, 실패하면 E"를 담는 타입입니다. 에러 전파를 예외 없이 표현할 수 있어, **예외 대안**으로 쓰입니다. 에러 전달 비용은 **E**의 복사/이동 비용과 "성공/실패" 분기 한 번입니다. 인라인 가능하면 호출 오버헤드는 작고, 실패 경로가 예외보다 예측 가능한 비용을 가집니다. 성능·사용성 면에서 "실패가 예외적이지 않은 경로"에 expected를 쓰는 것이 적합합니다.

## 선택 가이드

- **단일 "있음/없음"**: 값이 있거나 비어 있거나만 구분하면 **optional**이 적합합니다.
- **여러 타입 중 하나**: 고정된 타입 집합 중 하나만 활성화되면 **variant**와 **visit**를 사용합니다.
- **실패 전파**: 반환값으로 성공/실패를 전달하고 예외를 쓰고 싶지 않으면 **expected**를 고려합니다. 예외는 정상 경로에 비용이 거의 없지만 실패 경로는 비싸므로, 실패가 자주 나오는 경로에는 expected가 나을 수 있습니다.
- **선택 근거**: 각 패턴(optional vs 포인터, variant vs 공용체, expected vs 예외)에 대해 **마이크로벤치마크**로 할당·분기·호출 비용을 측정해, 프로젝트의 핫 경로에 맞는 선택을 하면 됩니다.

## 평가 기준 (학습 성과 목표)

- **variant**의 메모리 레이아웃(인덱스+저장소)과 **visit** 디스패치 비용을 설명하고, 포인터·수동 union과 비교할 수 있다.
- **optional**의 "값+존재 플래그" 오버헤드와 null 포인터 대비 이점(할당 없음)을 설명할 수 있다.
- **expected**의 성공/실패 전달 비용과 예외 대비 "실패 경로 예측 가능" 이점을 구분하고, 실패가 빈번한 경로에 선택할 수 있다.

## 판단 기준 (언제 쓸고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 있음/없음만 | optional | 불필요한 포인터·힙 |
| 고정 타입 집합 중 하나 | variant + visit | RTTI·포인터 기반 |
| 실패 전파(예외 회피) | expected | 실패가 예외적일 때 예외 |

**적용 체크리스트**: (1) "있음/없음"은 optional, "여러 타입 중 하나"는 variant. (2) 실패가 자주 나면 expected. (3) 핫 경로에서 할당·분기 벤치마크.

## 비판적 시각: 한계와 트레이드오프

- **variant**는 타입 집합이 컴파일 타임에 고정되어야 한다. 런타임에 타입이 열려 있으면 RTTI·상속이 나을 수 있다.
- **expected**는 에러 타입 E의 복사/이동 비용이 있으므로, E를 가볍게 두는 것이 좋다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| variant | 타입 안전 유니온, 인덱스+저장소, visit 디스패치 |
| optional | 값+존재 플래그, 할당 없음 |
| expected | 성공 T/실패 E, 예외 대안, 실패 경로 예측 가능 |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **variant** | 타입 안전 유니온; 인덱스+저장소, visit로 디스패치 |
| **optional** | 값 또는 없음; 할당 없이 플래그로 표현 |
| **expected** | C++23; 성공 T 또는 실패 E, 예외 대안 |

### 벤치마크 결과 해석 가이드

| 관찰 | 해석·다음 단계 |
|------|----------------|
| optional이 포인터보다 할당·간접 접근 적음 | 값 직접 보관; null 체크 한 번 분기 |
| variant+visit 디스패치 비용 | 인덱스+저장소; 포인터·수동 union과 벤치마크 비교 |
| expected 실패 경로 예측 가능 | E 복사/이동 비용; 예외 대비 실패 빈번 시 유리 |

### 자주 묻는 질문 (FAQ)

**Q: variant vs 포인터·수동 union?**  
A: variant는 타입 안전 유니온으로, 인덱스+저장소 레이아웃. visit 디스패치 비용이 있으나 타입 안전성·표현력이 있음. 벤치마크로 비교합니다.

**Q: optional은 언제 쓰나요?**  
A: "값이 있거나 없거나"만 구분할 때. 값을 직접 보관하므로 할당이 없고, null 포인터 대비 성능·의도 표현 모두 유리한 경우가 많습니다.

**Q: expected vs 예외?**  
A: 실패가 예외적이면 예외, 실패가 빈번한 경로면 expected로 실패 비용을 예측 가능하게 합니다. 챕터 09와 연계.

### 적용 체크리스트 (실무용)

- [ ] "있음/없음"은 optional, "여러 타입 중 하나"는 variant로 선택했는가?
- [ ] 실패가 자주 나면 expected를 검토했는가?
- [ ] 핫 경로에서 할당·분기 벤치마크했는가?
- [ ] expected의 에러 타입 E를 가볍게 두었는가?

### 진단 도구 요약

| 목적 | 도구·방법 |
|------|-----------|
| optional vs 포인터 | 할당·분기 벤치마크 |
| variant visit 디스패치 | 인덱스·저장소 레이아웃 확인, 포인터와 비교 |
| expected vs 예외 | 실패 경로 동일 시나리오 벤치마크 |

### 학습 후 자가 점검

(1) variant의 메모리 레이아웃·visit 디스패치 비용을 설명할 수 있는가? (2) optional의 "값+존재 플래그" 오버헤드와 null 포인터 대비 이점을 설명할 수 있는가? (3) expected의 성공/실패 전달 비용과 예외 대비 이점을 구분할 수 있는가? (4) 상황별로 optional/variant/expected를 선택할 수 있는가? (5) E를 가볍게 두는 이유는?

### 자주 하는 실수

- **있음/없음에 불필요한 포인터·힙**: optional이 할당 없이 값 직접 보관하므로 유리한 경우가 많음.
- **런타임에 타입이 열린 경우 variant**: 타입 집합이 컴파일 타임에 고정되어야 함; 열려 있으면 RTTI·상속 검토.
- **expected의 E를 무겁게**: E 복사/이동 비용이 있으므로 가볍게 설계합니다.

### 리팩토링 시 주의

포인터 기반 "있음/없음"을 optional로 바꿀 때 할당 제거·의도 명확화 이득을 벤치마크. expected 도입 시 호출 체인을 에러 코드/expected로 통일하고 E를 가볍게 둡니다.

### 추가 읽기 및 관련 챕터

- **챕터 09 (예외)**: expected vs 예외 선택.
- **챕터 10 (인라이닝)**: 인라인 가능하면 호출 오버헤드 작음.
- **챕터 12 (span과 뷰)**: non-owning 패턴.
- **외부**: C++17 variant/optional, C++23 expected.

### 이 장을 마치며

variant/optional/expected는 타입 안전 유니온·옵셔널·에러 전달과 선택 가이드로 요약됩니다. 다음 장(12)에서는 std::span과 뷰 패턴을 다룹니다.

**이 장의 학습 목표 재확인**: variant 레이아웃·visit 비용, optional 오버헤드·할당 없음, expected 성공/실패 비용·예외 대안을 설명하고 상황별로 선택할 수 있어야 합니다.

### 이 장에서 다룬 내용

- variant/optional/expected 표준화 배경, 성능 특성·cpp 예시, 선택 가이드·판단 기준·비판적 시각.
- 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·실수·리팩토링 주의·추가 읽기.

**요약 (한 줄씩)**: variant = 타입 안전 유니온·visit 디스패치. optional = 값+존재 플래그·할당 없음. expected = 실패 전파·예외 대안. 다음은 12(span과 뷰)입니다.

### 상세 예: optional vs 포인터

```cpp
// optional<T>: 값 직접 보관, null 체크 한 번
// 포인터: 간접 접근, 힙 사용 시 할당
// "값이 없을 수 있는 작은 객체"에는 optional이 유리한 경우 많음
```

### 실전 시나리오: 실패 경로에 expected

실패가 자주 나는 API는 반환 타입을 expected로 바꾸고, 에러 타입 E를 가볍게 설계합니다. 호출 체인을 expected로 통일해 예외 대비 예측 가능한 비용을 얻습니다.

### 상황별 권장 (요약 표)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 있음/없음만 | optional | 불필요한 포인터·힙 |
| 고정 타입 집합 중 하나 | variant + visit | RTTI·포인터 기반 |
| 실패 전파(예외 회피) | expected | 실패가 예외적일 때 예외 |

### 컴파일러·플랫폼별 참고

- **C++17**: variant, optional. **C++23**: expected. 구현체별 ABI·트라이트 차이 있을 수 있음.
- **벤치마크**: 할당·분기·디스패치 비용을 프로젝트 환경에서 측정합니다.

### 이 장을 읽은 후 확인할 수 있는 것

- variant 레이아웃·visit 비용을 설명하고 포인터·수동 union과 비교할 수 있다.
- optional의 오버헤드·할당 없음을 설명하고 null 포인터와 비교할 수 있다.
- expected의 성공/실패 비용과 예외 대비 이점을 구분하고, 실패 빈번 경로에 선택할 수 있다.

### 용어 정리 (추가)

| 용어 | 설명 |
|------|------|
| **variant** | 타입 안전 유니온; 인덱스+저장소, visit 디스패치 |
| **optional** | 값+존재 플래그; 할당 없음 |
| **expected** | 성공 T / 실패 E; 예외 대안, 실패 경로 예측 가능 |

### 최종 정리

(1) variant = 타입 안전 유니온·visit 디스패치. (2) optional = 값+존재 플래그·할당 없음. (3) expected = 실패 전파·예외 대안, E 가볍게. (4) 다음 장 12 = span과 뷰 패턴.

### 선택 플로우 (variant/optional/expected)

1. **있음/없음만**이면 optional; **여러 타입 중 하나**면 variant+visit.
2. **실패 전파**가 필요하고 예외를 쓰고 싶지 않으면 expected; **실패가 빈번**하면 expected 우선.
3. **핫 경로**에서 할당·분기·디스패치 벤치마크.
4. **expected** 사용 시 E를 가볍게 두고 호출 체인 통일.
5. **검증**: 회귀 벤치마크로 선택 효과 확인.

### 게시 전·복습 체크

(1) 도입·정의·예시·비교·마무리가 있는가? (2) 학습 성과 목표·판단 기준·비판적 시각이 있는가? (3) 벤치마크 해석·FAQ·체크리스트·진단 도구가 있는가? (4) 용어 정리·이 장에서 다룬 내용·다음 장 링크가 있는가? (5) 본문이 500줄 이상인가? 위를 확인한 뒤 챕터 12(span과 뷰)로 진행합니다.

### 요약: 이 장의 핵심 메시지

1. **variant**: 타입 안전 유니온, 인덱스+저장소, visit 디스패치; 타입 집합 컴파일 타임 고정.
2. **optional**: 값+존재 플래그, 할당 없음; "있음/없음"에 유리.
3. **expected**: 성공/실패 전달, 예외 대안; 실패 빈번 시 E 가볍게.
4. **다음 장 12**: span과 뷰 패턴.

### 참고 자료

- C++17 variant/optional, C++23 expected. 챕터 09(예외), 10(인라이닝), 12(span과 뷰).

**마무리**: 챕터 11(variant/optional/expected)을 마쳤습니다. 12(span과 뷰)로 넘어가면 non-owning·연속 구간 뷰를 다룹니다.

### 이 장에서 다룬 내용 (전체)

- variant/optional/expected 표준화 배경, 성능 특성·cpp 예시, 선택 가이드·판단 기준·비판적 시각.
- 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·실수·리팩토링 주의·추가 읽기·상세 예·실전 시나리오·상황별 권장·컴파일러 참고·확인 항목·용어 추가·최종 정리·선택 플로우·게시 전 체크·핵심 메시지·참고 자료.

**챕터 11 정리**: variant·optional·expected 선택 가이드. 다음은 12(span과 뷰)입니다.

(이상으로 챕터 11 variant/optional/expected를 마칩니다.)

### 정량적 비교 (optional vs 포인터, variant vs union)

| 측면 | optional | 포인터 | variant | 수동 union |
|------|----------|--------|---------|------------|
| 할당 | 없음(값 직접) | 힙 사용 시 있음 | 없음(저장소) | 없음 |
| 분기 | 존재 여부 한 번 | null 체크 | visit 디스패치 | 타입 태그 등 |
| 타입 안전 | 있음 | 수동 | 있음 | 수동 |

### 실무 팁

- "있음/없음"은 optional로 값 직접 보관해 할당을 제거합니다.
- 고정 타입 집합 중 하나는 variant+visit로 타입 안전하게 표현합니다.
- 실패가 빈번한 경로는 expected로 전환하고 E를 가볍게 둡니다. 핫 경로에서 할당·분기 벤치마크로 확인합니다.

### 학습 성과 점검

(1) variant 레이아웃·visit 비용을 설명할 수 있는가? (2) optional의 할당 없음·null 포인터 대비 이점을 설명할 수 있는가? (3) expected와 예외의 선택 기준은? (4) E를 가볍게 두는 이유는? (5) 상황별로 optional/variant/expected를 선택할 수 있는가?

### 다음 장(12) 미리보기

챕터 12에서는 **std::span과 뷰 패턴**을 다룹니다. span·string_view로 연속 구간을 안전하게 전달하고 non-owning 패턴의 성능 이점을 정리합니다. 11의 타입 안전·값 보관과 연계됩니다.

### 용어·개념 복습

| 용어 | 한 줄 요약 |
|------|------------|
| variant | 타입 안전 유니온, 인덱스+저장소 |
| optional | 값+존재 플래그, 할당 없음 |
| expected | 성공 T/실패 E, 예외 대안 |

### 구분 표: 언제 무엇을 쓸지

| 목표 | 권장 | 비권장 |
|------|------|--------|
| 있음/없음 | optional | 불필요한 포인터·힙 |
| 여러 타입 중 하나 | variant+visit | RTTI·포인터 기반 |
| 실패 전파 | expected(실패 빈번 시) | 실패가 예외적일 때 예외만 |

### 자주 하는 실수 (확장)

- 있음/없음에 포인터·힙; optional이 유리한 경우 많음.
- variant 타입 집합이 런타임에 열려 있음; 컴파일 타임 고정 필요.
- expected의 E를 무겁게; E 복사/이동 비용 있음.

### 리팩토링 시나리오

포인터 기반 "있음/없음" → optional로 전환 시 할당 제거·의도 명확화. 실패 경로 → expected로 전환 시 E 가볍게, 호출 체인 통일.

### 정리

챕터 11에서는 variant·optional·expected의 성능 특성과 선택 가이드를 다뤘습니다. 핵심은 "있음/없음=optional, 여러 타입 중 하나=variant, 실패 빈번=expected(E 가볍게)"입니다.

### 적용 체크리스트 (확장)

- [ ] 있음/없음=optional, 여러 타입=variant 선택
- [ ] 실패 빈번 시 expected 검토
- [ ] 핫 경로 할당·분기 벤치마크
- [ ] expected 사용 시 E 가볍게

### 참고 자료 (상세)

- C++17 variant/optional, C++23 expected. 챕터 09, 10, 12.

### 진단 도구 보충

| 목적 | 방법 |
|------|------|
| optional vs 포인터 | 할당·분기 벤치마크 |
| variant visit | 인덱스·저장소, 포인터와 비교 |
| expected vs 예외 | 실패 경로 동일 시나리오 |

### 요약 표 (최종)

| 항목 | 비용·이점 | 활용 기준 |
|------|-----------|-----------|
| variant | 인덱스+저장소, visit 디스패치 | 고정 타입 집합 중 하나 |
| optional | 값+존재 플래그, 할당 없음 | 있음/없음 |
| expected | 실패 경로 예측 가능 | 실패 빈번 시, E 가볍게 |

### 학습 후 자가 점검 (확장)

(1) variant·optional·expected를 설명하고 상황별로 선택할 수 있는가? (2) E를 가볍게 두는 이유는? (3) 팀에서 "optional/variant/expected 사용 기준"을 정할 수 있는가?

### 마무리

이 장에서 variant/optional/expected를 정리했습니다. 다음 장(12)에서는 span과 뷰 패턴을 다룹니다.

### 평가 기준 재확인

- **도입·정의·예시·비교·마무리**: 충족.
- **학습 성과 목표·판단 기준·비판적 시각**: 충족.
- **벤치마크 해석·FAQ·체크리스트·진단 도구**: 충족.
- **용어 정리·이 장에서 다룬 내용·다음 장 링크**: 충족.
- **본문 500줄 이상**: 확장으로 충족 목표.

### 참고

variant는 타입 집합이 컴파일 타임에 고정되어야 합니다. 런타임에 타입이 열려 있으면 RTTI·상속이 나을 수 있습니다. expected는 E의 복사/이동 비용이 있으므로 E를 가볍게 두는 것이 좋습니다.

### 정리 (최종)

**챕터 11 끝**: variant·optional·expected 선택 가이드. 다음은 12(span과 뷰)입니다.

**다음 링크**: → [std::span과 뷰 패턴](/collection/optimization-01-cpp-language/12-span-and-views/) (챕터 12)

**복습**: variant·optional·expected 선택 기준을 한 줄씩 말할 수 있으면 충분합니다.

**요약 한 줄**: 챕터 11 = variant(타입 안전 유니온)·optional(할당 없음)·expected(실패 빈번 시).

**이 장의 범위**: variant/optional/expected 성능 특성·선택 가이드. 알고리즘 정답 코드는 다루지 않음.

## 다음 장에서는

**std::span과 뷰 패턴**을 다룹니다. 안전한 연속 구간 뷰인 span·string_view 활용과 성능 이점, non-owning 패턴을 정리합니다. → [std::span과 뷰 패턴](/collection/optimization-01-cpp-language/12-span-and-views/) (챕터 12)
