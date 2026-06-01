---
collection_order: 9
date: 2026-03-10
lastmod: 2026-06-01
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

## Zero-cost exception 모델 (역사·배경과 실제)

"Zero-cost exception"은 **예외가 발생하지 않는 정상 경로**에서는 추가 비용을 거의 들이지 않겠다는 설계 목표입니다. 많은 Unix·Linux 플랫폼이 채택한 **Itanium C++ ABI**에서는 예외가 throw되지 않을 때 별도 분기나 테이블 조회를 하지 않고, 예외가 발생했을 때만 **unwinding** 정보와 **landing pad**를 사용해 스택을 되감고 catch 블록을 찾습니다. Windows에서는 **SEH(Structured Exception Handling)**와 연동된 방식으로 비슷한 "정상 경로 비용 없음" 모델을 따릅니다. 따라서 비용이 **예외 경로에만 집중**되며, 정상 경로에서는 예외 메커니즘이 거의 비용을 부과하지 않습니다.

> "In the zero-cost model, the runtime does not need to do anything when no exception is thrown. The cost is paid when an exception is thrown." — Itanium C++ ABI, Exception Handling. noexcept는 "이 함수는 예외를 던지지 않는다"는 계약으로, 이동 선택·인라이닝에 영향을 줄 수 있습니다.

## 예외 발생 경로 비용

예외가 throw되면 런타임은 **스택을 되감으며** 각 프레임의 소멸자를 호출하고, **catch**가 나올 때까지 **landing pad**를 찾습니다. catch 블록이 여러 개이면 **타입 매칭**으로 어떤 catch가 이 예외를 받을지 결정합니다. 이 과정은 예외 타입·스택 깊이·프레임 수에 비례해 비용이 들므로, "예외는 예외적인 상황"에만 쓰는 것이 성능과 설계 모두에 좋습니다.

**예외 vs 에러 코드 / std::expected**: 예외는 정상 경로에는 비용이 거의 없지만 실패 경로는 비쌉니다. 에러 코드나 expected는 정상·실패 모두 같은 코드 경로로 처리되어 비용이 예측 가능합니다. 아래는 같은 파싱 로직을 두 방식으로 구현한 비교입니다. `std::from_chars`는 예외를 던지지 않으므로, expected 버전은 실패에도 unwinding이 없습니다.

```cpp
#include <expected>      // C++23
#include <charconv>
#include <string_view>
#include <stdexcept>
#include <system_error>

// expected 기반: 정상·실패 모두 같은 분기로 처리되어 비용이 예측 가능
std::expected<int, std::errc> parse(std::string_view s) {
  int value{};
  auto [ptr, ec] = std::from_chars(s.data(), s.data() + s.size(), value);
  if (ec != std::errc{})
    return std::unexpected(ec);
  return value;
}

// 예외 기반: 정상 경로는 zero-cost지만 실패 경로는 throw/unwinding 비용
int parse_or_throw(std::string_view s) {
  int value{};
  auto [ptr, ec] = std::from_chars(s.data(), s.data() + s.size(), value);
  if (ec != std::errc{})
    throw std::invalid_argument("invalid integer");
  return value;
}
```

실패가 자주 나오는 경로나, 실패 시에도 낮은 지연이 중요하면 expected·에러 코드를 쓰는 편이 낫습니다. 실패가 정말 드문 예외 상황이면 예외가 정상 경로를 더 깔끔하게 유지합니다.

## noexcept의 의미와 최적화

함수에 **noexcept**를 붙이면 "이 함수는 예외를 던지지 않는다"는 계약이 됩니다. 표준 라이브러리에서는 **이동 연산**이 noexcept일 때만 이동을 선택하고, 그렇지 않으면 복사를 선택하는 경우가 있습니다. 대표적으로 `std::vector` 재할당 시, 이동 생성자가 noexcept가 아니면 강한 예외 보장을 위해 **복사**를 선택합니다. **std::move_if_noexcept**는 "이동이 noexcept이면 이동, 아니면 복사"를 선택하는 유틸리티로, 이런 최적화를 일관되게 적용할 때 쓰입니다.

**소멸자**와 **이동 생성자·이동 대입 연산자**는 가능하면 **noexcept**로 두는 것이 좋습니다. 소멸자는 예외를 던지면 스택 언와인딩 중 추가 문제를 일으킬 수 있고, 이동이 noexcept여야 컨테이너가 이동을 안전하게 사용할 수 있기 때문입니다.

```cpp
#include <vector>

struct Widget {
  Widget(Widget&& other) noexcept { /* 이동 */ }
  Widget& operator=(Widget&& other) noexcept { return *this; }
  ~Widget() noexcept {}
};

// 이동 연산자가 noexcept이므로 vector 재할당 시 복사 대신 이동을 선택한다.
// noexcept를 떼면 같은 재할당에서 요소가 복사된다(강한 예외 보장 때문).
std::vector<Widget> v;
```

## 예외 사양이 인라이닝·코드 생성에 미치는 영향

noexcept 함수는 "예외를 전파하지 않는다"는 정보를 컴파일러에 주므로, **언와인딩 경로**를 생성하지 않아도 되고, **인라이닝**이나 **코드 배치**를 더 공격적으로 할 수 있는 여지가 생깁니다. 마이크로벤치마크에서는 "동일한 함수를 noexcept 있음/없음"으로 비교해 호출 비용이 미세하게 나뉘는지 확인할 수 있습니다. 효과는 플랫폼·컴파일러에 따라 다릅니다.

**실무 권장**: 실패 경로가 없거나, 실패 시 빠르게 종료해도 되는 **핫패스**에서는 해당 함수를 **noexcept**로 선언하는 것이 좋습니다. 예외를 던질 수 있는 경로가 있다면 noexcept를 붙이면 안 되며(위반 시 `std::terminate`), 대신 해당 경로는 에러 코드나 expected로 처리하는 설계를 고려합니다.

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
- **noexcept**는 계약이므로, 위반 시 `std::terminate`가 호출된다. 예외를 던질 수 있는 경로가 있으면 붙이지 않는다.

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
| **move_if_noexcept** | 이동이 noexcept이면 이동, 아니면 복사를 선택하는 유틸리티 |

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

### 자주 하는 실수

- **예외를 던질 수 있는 함수에 noexcept**: 위반 시 `std::terminate`; 예외 경로가 있으면 붙이지 않습니다.
- **이동 연산자에 noexcept 누락**: 컨테이너 재할당 시 복사가 선택될 수 있어 성능 손실.
- **실패가 빈번한 경로에 예외만 사용**: expected로 전환해 실패 경로 비용을 예측 가능하게 합니다.

### 리팩토링 시 주의

noexcept 추가 시 계약이 되므로, 해당 함수와 그 안에서 호출하는 함수가 예외를 던지지 않음을 보장해야 합니다. expected 도입 시 에러 타입 E를 가볍게 두고, 호출 체인 전체를 에러 코드/expected로 통일하는 것이 좋습니다.

### 추가 읽기 및 관련 챕터

- **챕터 08 (코루틴)**: 비동기·런타임 오버헤드.
- **챕터 10 (인라이닝)**: noexcept가 인라이닝에 미치는 영향.
- **챕터 11 (variant/optional/expected)**: expected 상세.

---

## 다음 장에서는

**이전 장**: [코루틴 성능](/post/cpp-optimization/coroutine-performance/) (챕터 08)

**인라이닝 유도 기법**을 다룹니다. inline·__forceinline 활용과 인라이닝을 유도하는 코드 패턴, 실패 원인 진단(Tr.02 컴파일러 트랙 연계)을 정리합니다. → [인라이닝 유도 기법](/post/cpp-optimization/inlining-techniques/) (챕터 10)
