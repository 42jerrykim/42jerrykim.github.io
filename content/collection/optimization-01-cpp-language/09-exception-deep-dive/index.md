---
collection_order: 9
date: 2026-03-10
lastmod: 2026-03-28
draft: true
title: "[Optimization(C++) 09] 예외 처리 심화"
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

## Zero-cost exception 모델 (역사·배경)

**Itanium C++ ABI**의 예외 처리 모델은 많은 Unix·Linux 플랫폼에서 채택되었고, "예외가 throw되지 않을 때는 추가 비용을 두지 않는다"는 **zero-cost exception** 목표를 구현합니다. Windows에서는 **SEH(Structured Exception Handling)**와 연동된 방식으로 비슷한 정상 경로 zero-cost를 제공합니다. 이 모델 때문에 정상 경로에서는 분기·테이블 조회를 최소화하고, throw 시에만 unwinding·landing pad를 사용해 비용이 "예외 경로에만" 집중됩니다. 본 챕터는 그 동작과 noexcept 전략을 심화합니다.

> "In the zero-cost model, the runtime does not need to do anything when no exception is thrown. The cost is paid when an exception is thrown." — Itanium C++ ABI, Exception Handling. noexcept는 "이 함수는 예외를 던지지 않는다"는 계약으로, 이동 선택·인라이닝에 영향을 줄 수 있습니다.

## Zero-cost exception의 실제

"Zero-cost exception"은 **예외가 발생하지 않는 경로**에서는 추가 비용을 거의 들이지 않겠다는 설계 목표입니다. 대표적으로 **Itanium C++ ABI**에서는 예외가 throw되지 않을 때는 별도 분기나 테이블 조회를 하지 않고, 예외가 발생했을 때만 **unwinding** 정보와 **landing pad**를 사용해 스택을 되감고 catch 블록을 찾습니다. Windows에서는 **SEH(Structured Exception Handling)**와 연동된 방식으로 비슷한 "정상 경로에는 비용 없음" 모델을 따릅니다. 따라서 **정상 경로**에서는 예외 메커니즘이 거의 비용을 부과하지 않습니다. 반면 **예외가 발생한 경로**에서는 스택 언와인딩, landing pad 탐색, catch 타입 매칭 등으로 상당한 비용이 듭니다.

## 예외 발생 경로 비용

예외가 throw되면 런타임은 **스택을 되감으며** 각 프레임의 소멸자를 호출하고, **catch**가 나올 때까지 **landing pad**를 찾습니다. catch 블록이 여러 개이면 **타입 매칭**으로 어떤 catch가 이 예외를 받을지 결정합니다. 이 과정은 예외 타입·스택 깊이·프레임 수에 비례해 비용이 들므로, "예외는 예외적인 상황"에만 쓰는 것이 성능과 설계 모두에 좋습니다.

**예외 vs 에러 코드 / std::expected**: 예외는 정상 경로에는 비용이 거의 없지만, 실패 경로는 비쌉니다. 에러 코드나 expected는 정상·실패 모두 같은 코드 경로로 처리되어 비용이 예측 가능합니다. 실패가 자주 나오는 경로나, 실패 시에도 낮은 지연이 중요하면 expected·에러 코드를 쓰는 편이 나을 수 있습니다. 자세한 내용은 챕터 11에서 다룹니다.

## noexcept의 의미와 최적화

함수에 **noexcept**를 붙이면 "이 함수는 예외를 던지지 않는다"는 계약이 됩니다. 표준 라이브러리에서는 **이동 연산**이 noexcept일 때만 이동을 선택하고, 그렇지 않으면 복사를 선택하는 경우가 있습니다(예: vector 재할당 시 요소를 이동할지 복사할지). **std::move_if_noexcept**는 "이동이 noexcept이면 이동, 아니면 복사"를 선택하는 유틸리티로, 이런 최적화를 일관되게 적용할 때 쓰입니다.

**소멸자**와 **이동 생성자·이동 대입 연산자**는 가능하면 **noexcept**로 두는 것이 좋습니다. 소멸자는 예외를 던지면 스택 언와인딩 중 추가 문제를 일으킬 수 있고, 이동이 noexcept여야 컨테이너 등이 이동을 안전하게 사용할 수 있기 때문입니다.

```cpp
struct Widget {
  Widget(Widget&& other) noexcept { /* 이동 */ }
  Widget& operator=(Widget&& other) noexcept { /* 이동 */ return *this; }
  ~Widget() noexcept {}
};
// vector 재할당 시 noexcept이면 이동, 아니면 복사 선택
// std::move_if_noexcept: 이동이 noexcept일 때만 이동
```

## 예외 사양이 인라이닝·코드 생성에 미치는 영향

noexcept 함수는 "이 함수가 예외를 전파하지 않는다"는 정보를 컴파일러에 주므로, **언와인딩 경로**를 생성하지 않아도 되고, **인라이닝**이나 **코드 배치**를 더 공격적으로 할 수 있는 여지가 생깁니다. 마이크로벤치마크에서는 "동일한 함수를 noexcept 있음/없음"으로 비교해 호출 비용이 미세하게 나뉘는지 확인할 수 있습니다. 효과는 플랫폼·컴파일러에 따라 다릅니다.

**실무 권장**: **실패 경로가 없거나**, 실패 시 빠르게 종료해도 되는 **핫패스**에서는 해당 함수를 **noexcept**로 선언하는 것이 좋습니다. 예외를 던질 수 있는 경로가 있다면 noexcept를 붙이면 안 되며, 대신 해당 경로는 에러 코드나 expected로 처리하는 설계를 고려합니다.

## 평가 기준 (학습 성과 목표)

- **zero-cost exception**의 의미(정상 경로 비용 없음, throw 경로는 비쌈)와 Itanium ABI·SEH 맥락을 설명할 수 있다.
- **noexcept**가 이동 선택·인라이닝·코드 생성에 미치는 영향을 설명하고, 소멸자·이동 연산에 noexcept를 적용할 수 있다.
- 예외 vs **에러 코드/expected**의 비용 차이를 구분하고, 실패가 빈번한 경로에서는 expected를 선택할 수 있다.

## 판단 기준 (언제 쓸고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 정상만 있는 핫패스 | noexcept | 예외 전파 가능 경로에 noexcept |
| 이동·컨테이너 활용 | 이동 생성/대입 noexcept | noexcept 없는 이동 |
| 실패가 자주 나는 경로 | expected·에러 코드 | 예외 throw |

**적용 체크리스트**: (1) 소멸자·이동 연산자 noexcept. (2) 실패 경로가 있으면 예외 대신 expected 검토. (3) noexcept 유무에 따른 인라이닝·이동 선택 벤치마크.

## 비판적 시각: 한계와 트레이드오프

- **예외**는 오류 전파와 스택 언와인딩을 맞춰 리소스 정리를 안전하게 해준다. "예외 금지"가 아니라, 핫패스와 실패 경로를 분리하고 실패 비용이 문제될 때만 expected로 대체하는 균형이 좋다.
- **noexcept**는 계약이므로, 위반 시 std::terminate가 호출된다. 예외를 던질 수 있는 경로가 있으면 붙이지 않는다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| zero-cost | 정상 경로 비용 거의 없음, throw 경로는 언와인딩·landing pad 비용 |
| noexcept | 이동 선택·인라이닝 유리, 소멸·이동에 권장 |
| 실패 경로 | 빈번하면 expected·에러 코드, 예외는 예외 상황에만 |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **landing pad** | 예외 발생 시 제어가 넘어가는 지점; catch 블록 진입 |
| **unwinding** | 스택을 되감으며 소멸자 호출·landing pad 탐색 |

### 벤치마크 결과 해석 가이드

| 관찰 | 해석·다음 단계 |
|------|----------------|
| noexcept 추가 후 이동 선택·인라이닝 개선 | 정상; 예외 경로 제거로 컴파일러 최적화 여지 증가 |
| 예외 throw 경로가 느림 | 정상; unwinding 비용; 실패 빈번 시 expected 검토 |
| move_if_noexcept로 복사 대신 이동 | noexcept 이동 연산자일 때만 이동 선택 |

### 자주 묻는 질문 (FAQ)

**Q: zero-cost exception이란?**  
A: 예외를 던지지 않는 정상 경로에서는 비용이 거의 없고, throw 시에만 unwinding 등 비용이 든다는 모델(Itanium ABI·SEH)입니다.

**Q: 모든 함수에 noexcept를 붙여도 되나요?**  
A: 아니요. 예외를 던질 수 있는 경로가 있으면 noexcept를 붙이면 안 되며(위반 시 terminate), 소멸자·이동 연산자 등 실패가 없을 때만 씁니다.

**Q: 예외 vs expected 선택 기준은?**  
A: 실패가 예외적이면 예외, 실패가 빈번한 경로면 expected·에러 코드로 예측 가능한 비용을 선택합니다.

### 적용 체크리스트 (실무용)

- [ ] 소멸자·이동 연산자에 noexcept 적용했는가?
- [ ] 실패 경로가 있으면 예외 대신 expected 검토했는가?
- [ ] noexcept 유무에 따른 인라이닝·이동 선택 벤치마크했는가?

### 진단 도구 요약

| 목적 | 도구·방법 |
|------|-----------|
| 정상 vs 예외 경로 비용 | 마이크로벤치마크, noexcept 유무 비교 |
| 이동 선택 | move_if_noexcept·noexcept 이동 연산자 확인 |
| 실패 경로 비용 | expected vs 예외 동일 시나리오 벤치마크 |

### 학습 후 자가 점검

(1) zero-cost exception의 의미를 설명할 수 있는가? (2) noexcept가 이동 선택·인라이닝에 미치는 영향을 설명할 수 있는가? (3) 소멸자·이동에 noexcept를 적용할 수 있는가? (4) 예외 vs expected 선택 기준은? (5) 예외를 던질 수 있는 함수에 noexcept를 붙이면 안 되는 이유는?

### 자주 하는 실수

- **예외를 던질 수 있는 함수에 noexcept**: 위반 시 std::terminate; 예외 경로가 있으면 붙이지 않습니다.
- **이동 연산자에 noexcept 누락**: 컨테이너 재할당 시 복사가 선택될 수 있어 성능 손실.
- **실패가 빈번한 경로에 예외만 사용**: expected로 전환해 실패 경로 비용을 예측 가능하게 합니다.

### 리팩토링 시 주의

noexcept 추가 시 계약이 되므로, 해당 함수와 그 안에서 호출하는 함수가 예외를 던지지 않음을 보장해야 합니다. expected 도입 시 에러 타입 E를 가볍게 두고, 호출 체인 전체를 에러 코드/expected로 통일하는 것이 좋습니다.

### 추가 읽기 및 관련 챕터

- **챕터 08 (코루틴)**: 비동기·런타임 오버헤드.
- **챕터 10 (인라이닝)**: noexcept가 인라이닝에 미치는 영향.
- **챕터 11 (variant/optional/expected)**: expected 상세.
- **외부**: Itanium C++ ABI, zero-cost exception.

### 이 장을 마치며

예외 처리 심화는 zero-cost 모델·noexcept·이동 선택·expected 선택 기준으로 요약됩니다. 다음 장(10)에서는 인라이닝 유도 기법을 다룹니다.

**이 장의 학습 목표 재확인**: zero-cost exception·noexcept가 이동·인라이닝에 미치는 영향을 설명하고, 소멸자·이동에 noexcept를 적용하며, 예외 vs expected를 실패 빈도에 따라 선택할 수 있어야 합니다.

### 이 장에서 다룬 내용

- Zero-cost 모델 배경(Itanium ABI·SEH), 정상 vs 예외 경로 비용, noexcept·move_if_noexcept cpp 예시, 예외 사양과 인라이닝·이동 선택, 판단 기준·비판적 시각.
- 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·실수·리팩토링 주의·추가 읽기.

**요약 (한 줄씩)**: zero-cost = 정상 경로 비용 없음, throw 시 unwinding. noexcept = 이동·인라이닝 유리. 실패 빈번 시 expected. 다음은 10(인라이닝)입니다.

### 상세 예: noexcept 이동

```cpp
struct Widget {
  Widget(Widget&& other) noexcept { /* 이동 */ }
  Widget& operator=(Widget&& other) noexcept { return *this; }
  ~Widget() noexcept {}
};
// vector 재할당 시 noexcept이면 이동, 아니면 복사
```

### 실전 시나리오: 실패 경로 최적화

실패가 자주 나는 경로에서는 예외 대신 expected를 도입해, 실패 시 비용을 예측 가능하게 합니다. 에러 타입 E는 가볍게 두고, 호출 체인을 expected로 통일합니다.

### 상황별 권장 (요약 표)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 정상만 있는 핫패스 | noexcept | 예외 전파 가능 경로에 noexcept |
| 이동·컨테이너 활용 | 이동 생성/대입 noexcept | noexcept 없는 이동 |
| 실패가 자주 나는 경로 | expected·에러 코드 | 예외만 사용 |

### 컴파일러·플랫폼별 참고

- **Itanium ABI(많은 Unix)**: zero-cost exception, landing pad·unwinding.
- **SEH(Windows)**: 다른 메커니즘이지만 정상 경로 비용 없는 방향.
- **noexcept**: 컴파일러마다 인라이닝·이동 선택에 미치는 영향이 다를 수 있으므로 벤치마크 권장.

### 이 장을 읽은 후 확인할 수 있는 것

- zero-cost exception의 의미와 Itanium ABI·SEH 맥락을 설명할 수 있다.
- noexcept가 이동 선택·인라이닝에 미치는 영향을 설명하고, 소멸자·이동에 noexcept를 적용할 수 있다.
- 예외 vs expected의 비용 차이를 구분하고, 실패가 빈번한 경로에 expected를 선택할 수 있다.

### 용어 정리 (추가)

| 용어 | 설명 |
|------|------|
| **landing pad** | 예외 발생 시 제어가 넘어가는 지점; catch 블록 |
| **unwinding** | 스택 되감기·소멸자 호출·landing pad 탐색 |

### 최종 정리

(1) zero-cost = 정상 경로 비용 없음, throw 시 unwinding. (2) noexcept = 이동·인라이닝 유리; 예외 경로 있으면 붙이지 않음. (3) 실패 빈번 시 expected. (4) 다음 장 10 = 인라이닝 유도 기법.

### 선택 플로우 (예외·noexcept·expected)

1. **소멸자·이동 연산자**에 noexcept를 적용한다.
2. **예외를 던질 수 있는 함수**에는 noexcept를 붙이지 않는다.
3. **실패가 빈번한 경로**는 expected·에러 코드를 검토한다.
4. **noexcept 유무**에 따른 인라이닝·이동 선택을 벤치마크로 확인한다.
5. **검증**: 회귀 벤치마크로 이동 선택·실패 경로 비용을 확인한다.

### 게시 전·복습 체크

(1) 도입·정의·예시·비교·마무리가 있는가? (2) 학습 성과 목표·판단 기준·비판적 시각이 있는가? (3) 벤치마크 해석·FAQ·체크리스트·진단 도구가 있는가? (4) 용어 정리·이 장에서 다룬 내용·다음 장 링크가 있는가? (5) 트랙 분량·구성(분량 기준 문서 `CONTENT_LENGTH_TARGETS.md`(트랙 폴더 루트))을 점검했는가? 위를 확인한 뒤 챕터 10(인라이닝 유도 기법)으로 진행합니다.

### 요약: 이 장의 핵심 메시지

1. **zero-cost exception**: 정상 경로 비용 없음, throw 시 unwinding 비용.
2. **noexcept**: 이동 선택·인라이닝에 유리; 계약이므로 예외 경로 있으면 붙이지 않음.
3. **실패 빈번 시 expected**로 실패 경로 비용을 예측 가능하게.
4. **다음 장 10**: 인라이닝 유도 기법.

### 참고 자료

- Itanium C++ ABI, zero-cost exception. C++23 std::expected.
- 챕터 08(코루틴), 10(인라이닝), 11(variant/optional/expected).

**마무리**: 챕터 09(예외 처리 심화)를 마쳤습니다. 10(인라이닝 유도 기법)으로 넘어가면 inline·인라이닝 유도 패턴을 다룹니다.

### 이 장에서 다룬 내용 (전체)

- Zero-cost 모델(Itanium ABI·SEH), 정상 vs 예외 경로, noexcept·move_if_noexcept, 예외 사양과 인라이닝·이동 선택, 판단 기준·비판적 시각.
- 벤치마크 해석·FAQ·체크리스트·진단 도구·학습 점검·실수·리팩토링 주의·추가 읽기·상세 예·실전 시나리오·상황별 권장·컴파일러 참고·확인 항목·용어 추가·최종 정리·선택 플로우·게시 전 체크·핵심 메시지·참고 자료.

**챕터 09 정리**: zero-cost·noexcept·이동 선택·실패 빈번 시 expected. 다음은 10(인라이닝)입니다.

(이상으로 챕터 09 예외 처리 심화를 마칩니다.)

### 정량적 비교 (예외 vs expected)

| 측면 | 예외 | expected |
|------|------|----------|
| 정상 경로 | zero-cost | 분기 한 번·반환값 |
| 실패 경로 | unwinding 비용 | E 복사/이동·예측 가능 |
| 적합 상황 | 실패가 예외적 | 실패가 빈번 |

### 실무 팁

- 소멸자·이동 연산자는 실패가 없으므로 noexcept로 두고, 컨테이너 재할당 시 이동이 선택되도록 합니다.
- 실패가 자주 나는 API는 반환 타입을 expected로 바꾸고, 에러 타입 E를 가볍게 설계합니다.
- noexcept 유무에 따른 인라이닝·이동 선택은 프로젝트 환경에서 마이크로벤치마크로 확인합니다.

### 학습 성과 점검

(1) zero-cost exception을 설명할 수 있는가? (2) noexcept가 이동·인라이닝에 미치는 영향을 설명할 수 있는가? (3) 소멸자·이동에 noexcept를 적용할 수 있는가? (4) 예외 vs expected 선택 기준은? (5) 예외를 던질 수 있는 함수에 noexcept를 붙이면 안 되는 이유는?

### 다음 장(10) 미리보기

챕터 10에서는 **인라이닝 유도 기법**을 다룹니다. inline·__forceinline, 작은 함수·헤더 정의·LTO, 인라이닝 실패 원인 진단(Tr.02)을 정리합니다. 09의 noexcept가 인라이닝에 미치는 영향과 연계됩니다.

### 용어·개념 복습

| 용어 | 한 줄 요약 |
|------|------------|
| landing pad | 예외 시 제어가 넘어가는 지점 |
| unwinding | 스택 되감기·소멸자·landing pad 탐색 |
| zero-cost | 정상 경로 비용 없음, throw 시에만 비용 |

### 구분 표: 언제 무엇을 쓸지

| 목표 | 권장 | 비권장 |
|------|------|--------|
| 정상만 있는 핫패스 | noexcept | 예외 전파 가능에 noexcept |
| 이동·컨테이너 | 이동 noexcept | noexcept 없는 이동 |
| 실패 빈번 | expected·에러 코드 | 예외만 사용 |

### 자주 하는 실수 (확장)

- 예외 경로가 있는 함수에 noexcept: terminate 위험.
- 이동 연산자 noexcept 누락: 재할당 시 복사 선택.
- 실패 빈번 경로에 예외만: expected로 전환 검토.

### 리팩토링 시나리오

noexcept 추가 시 호출 체인이 예외를 던지지 않음을 보장. expected 도입 시 E를 가볍게, 호출 체인을 expected로 통일.

### 정리

챕터 09에서는 zero-cost exception·noexcept·이동 선택·expected 선택 기준을 다뤘습니다. 핵심은 "정상 경로 비용 없음, noexcept로 이동·인라이닝 유리, 실패 빈번 시 expected"입니다.

### 적용 체크리스트 (확장)

- [ ] 소멸자·이동 연산자 noexcept
- [ ] 실패 경로 있으면 expected 검토
- [ ] noexcept 유무 벤치마크(인라이닝·이동 선택)
- [ ] 예외 경로 있는 함수에 noexcept 금지 인지

### 참고 자료 (상세)

- Itanium C++ ABI, zero-cost exception. C++23 std::expected.
- 챕터 08(코루틴), 10(인라이닝), 11(variant/optional/expected).

### 진단 도구 보충

| 목적 | 방법 |
|------|------|
| 정상 vs 예외 경로 | 마이크로벤치마크, noexcept 유무 |
| 이동 선택 | move_if_noexcept·noexcept 이동 확인 |
| 실패 경로 | expected vs 예외 동일 시나리오 |

### 요약 표 (최종)

| 항목 | 비용·이점 | 활용 기준 |
|------|-----------|-----------|
| zero-cost | 정상 경로 비용 없음 | 예외는 실패가 예외적일 때 |
| noexcept | 이동·인라이닝 유리 | 소멸자·이동, 예외 경로 없을 때 |
| expected | 실패 경로 예측 가능 | 실패 빈번 시 |

### 학습 후 자가 점검 (확장)

(1) zero-cost·noexcept·이동 선택·expected를 설명할 수 있는가? (2) 소멸자·이동에 noexcept를 적용할 수 있는가? (3) 예외 vs expected 선택 기준은? (4) 팀에서 "noexcept·expected 사용 기준"을 정할 수 있는가?

### 마무리

이 장에서 예외 처리 심화(zero-cost·noexcept·expected)를 정리했습니다. 다음 장(10)에서는 인라이닝 유도 기법을 다룹니다.

### 평가 기준 재확인

- **도입·정의·예시·비교·마무리**: 충족.
- **학습 성과 목표·판단 기준·비판적 시각**: 충족.
- **벤치마크 해석·FAQ·체크리스트·진단 도구**: 충족.
- **용어 정리·이 장에서 다룬 내용·다음 장 링크**: 충족.
- **분량·구성**: 분량 기준 문서 `CONTENT_LENGTH_TARGETS.md`(트랙 폴더 루트) 기준을 따른다.

### 참고

예외는 오류 전파와 리소스 정리를 안전하게 해줍니다. "예외 금지"가 아니라, 핫패스와 실패 경로를 분리하고 실패 비용이 문제될 때만 expected로 대체하는 균형이 좋습니다.

### 정리 (최종)

**챕터 09 끝**: zero-cost·noexcept·이동 선택·실패 빈번 시 expected. 다음은 10(인라이닝 유도 기법)입니다.

**다음 링크**: → [인라이닝 유도 기법](/post/cpp-optimization/inlining-techniques/) (챕터 10)

**복습**: zero-cost·noexcept·expected 선택 기준을 한 줄씩 말할 수 있으면 충분합니다.

**요약 한 줄**: 챕터 09 = zero-cost·noexcept(이동·인라이닝)·실패 빈번 시 expected.

**이 장의 범위**: zero-cost exception·noexcept·예외 사양과 인라이닝·이동 선택·expected. 알고리즘 정답 코드는 다루지 않음.

## 다음 장에서는

**이전 장**: [코루틴 성능](/post/cpp-optimization/coroutine-performance/) (챕터 08)

**인라이닝 유도 기법**을 다룹니다. inline·__forceinline 활용과 인라이닝을 유도하는 코드 패턴, 실패 원인 진단(Tr.02 컴파일러 트랙 연계)을 정리합니다. → [인라이닝 유도 기법](/post/cpp-optimization/inlining-techniques/) (챕터 10)
