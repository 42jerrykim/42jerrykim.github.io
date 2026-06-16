---
collection_order: 10
date: 2026-03-10
lastmod: 2026-06-01
draft: true
title: "[Optimization(C++) 10] 코루틴 성능"
slug: coroutine-performance
description: "C++20 코루틴의 성능 특성과 오버헤드를 다룹니다. 코루틴 프레임 할당·저장/복원 비용, 컴파일러 최적화 한계를 정리하고, Low-latency 경로에서의 사용 기준을 제시하며, generator·task 패턴별 비용과 대안을 비교합니다."
tags:
  - C++
  - Performance
  - Optimization
  - 성능
  - 최적화
  - Async
  - 비동기
  - Concurrency
  - 동시성
  - Memory
  - 메모리
  - Compiler
  - 컴파일러
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Profiling
  - 프로파일링
  - Benchmark
  - Time-Complexity
  - 시간복잡도
  - Latency
  - Throughput
  - Testing
  - 테스트
  - Debugging
  - 디버깅
  - Refactoring
  - 리팩토링
  - Readability
  - Maintainability
  - Modularity
  - Git
  - CI-CD
  - Linux
  - Windows
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
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Type-Safety
  - Software-Architecture
  - 소프트웨어아키텍처
  - Documentation
  - 문서화
  - OS
  - 운영체제
  - Thread
  - Process
---

본 챕터에서는 C++20 코루틴의 성능 특성과 오버헤드를 다룹니다. **왜 Low-latency에서 이슈인가**: 코루틴은 suspend/resume마다 상태 저장·복원과 (기본적으로) 프레임 힙 할당이 필요하므로, µs 단위 핫패스에서는 이 오버헤드가 허용 한도를 넘을 수 있습니다. 네트워크/IO 대기처럼 suspend 시간이 긴 비동기 흐름에는 적합하지만, "짧은 연산만 하고 곧 반환"하는 경로에는 부적합할 수 있습니다.

## 이 장을 읽기 전에

**완전한 초보자?** 이 장은 [06장: 객체 수명 최적화](/post/cpp-optimization/object-lifetime/)의 할당 비용 개념을 전제로 합니다. `co_await`·`co_yield`·`co_return`이 함수의 실행을 중단·재개한다는 큰 그림만 알면 충분합니다.

**이 장의 깊이**: 이 장은 **심화~전문가**를 포괄합니다. 코루틴이 프레임으로 변환되는 메커니즘부터 시작해, 전문가 구간에서는 프레임 힙 할당·suspend/resume 비용을 따지고 µs 핫패스에서 쓸지/피할지, custom allocator·HALO(힙 할당 제거) 가능성을 판단하는 기준을 다룹니다. **다루지 않는 것**: 비동기 IO·이벤트 루프 설계(Tr.11 IO/네트워크 트랙)와 스레드 스케줄링(Tr.04 동시성 트랙)입니다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| **초보자** | "C++20 코루틴 메커니즘" | 코루틴이 프레임으로 바뀌는 큰 그림 이해 |
| **중급자** | "코루틴 프레임 할당" ~ "suspend / resume 비용" | 코루틴 오버헤드의 출처 파악 |
| **전문가** | "Low-latency 경로에서의 사용 기준" ~ "비판적 시각" | µs 경로에서 쓸지/피할지 판단 |

---

## C++20 코루틴 도입 (역사·배경)

C++20에서 **코루틴**이 표준에 포함되었습니다. 코루틴 TS를 거쳐 표준화되면서, `co_await`·`co_yield`·`co_return`과 promise_type·awaitable 인터페이스가 정의되었습니다. 컴파일러는 코루틴을 **프레임**(상태 블록)으로 변환하고, 대부분의 구현체는 이 프레임을 **힙에 할당**합니다. 따라서 "한 번 호출할 때마다 할당"이 발생할 수 있어, Low-latency에서는 custom allocator나 스택/버퍼 기반 프레임이 필요할 수 있습니다.

> "The coroutine frame is allocated on the heap by default. Implementations may provide overloads of operator new that allow placement of the frame elsewhere." — C++20 Standard (coroutines). 사용자 할당자로 힙 할당을 제거할 수 있습니다.

## C++20 코루틴 메커니즘

C++20 코루틴은 **일시 정지(suspend)**와 **재개(resume)**가 가능한 함수입니다. 컴파일러는 코루틴을 **프레임(coroutine frame)**이라는 상태 블록으로 변환합니다. 이 프레임에는 지역 변수, 중단 지점(재개 시 어디서 실행할지), promise 객체 등이 들어갑니다. **promise_type**은 코루틴의 반환값·예외·최종 정리 등을 제어하고, **awaitable**은 `co_await` 지점에서 "지금 멈출지, 바로 진행할지"와 재개 시 동작을 정의합니다. suspend 시 제어가 호출자로 돌아가고, resume 시 저장된 상태에서 이어서 실행됩니다.

```mermaid
flowchart LR
  subgraph call [호출]
    A["코루틴 진입"]
    B["프레임 할당"]
    C["실행"]
  end
  subgraph susp [suspend]
    D["상태 저장"]
    E["호출자로 제어 반환"]
  end
  subgraph res [resume]
    F["상태 복원"]
    G["이어서 실행"]
  end
  A --> B --> C
  C -->|"co_await"| D --> E
  E --> F --> G --> C
```

**컴파일 가능한 최소 generator**: `co_yield`로 값을 내보낼 때마다 suspend되고, 호출자가 `resume()`으로 다시 진행시킵니다. `promise_type`과 `std::coroutine_handle`로 직접 generator를 구성하면 코루틴의 실제 동작을 확인할 수 있습니다.

```cpp
#include <coroutine>
#include <cstdio>

template <typename T>
struct Generator {
  struct promise_type {
    T current{};
    Generator get_return_object() {
      return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
    }
    std::suspend_always initial_suspend() noexcept { return {}; }
    std::suspend_always final_suspend() noexcept { return {}; }
    std::suspend_always yield_value(T v) noexcept { current = v; return {}; }
    void return_void() {}
    void unhandled_exception() { std::terminate(); }
  };

  std::coroutine_handle<promise_type> h;
  explicit Generator(std::coroutine_handle<promise_type> handle) : h(handle) {}
  ~Generator() { if (h) h.destroy(); }
  Generator(Generator&& o) noexcept : h(o.h) { o.h = {}; }

  bool next() { h.resume(); return !h.done(); }   // 다음 co_yield까지 진행
  T value() const { return h.promise().current; }
};

Generator<int> iota(int n) {
  for (int i = 0; i < n; ++i)
    co_yield i;                 // 매 반복마다 suspend
}

int main() {
  auto g = iota(3);
  while (g.next())
    std::printf("%d\n", g.value());   // 0, 1, 2
}
```

## 코루틴 프레임 할당

기본적으로 코루틴 프레임은 **힙에 할당**됩니다(표준은 `operator new`를 사용할 수 있다고만 하고, 구현체가 그렇게 하는 경우가 많습니다). 따라서 코루틴을 한 번 호출할 때마다 할당이 발생할 수 있고, µs 단위 경로에서는 이 할당 비용과 캐시 효과가 부담이 될 수 있습니다.

**사용자 제공 할당자**를 쓰거나 **미리 할당된 버퍼**를 넘기면, 프레임을 그 버퍼에 올려 힙 할당을 제거할 수 있습니다. C++20에서는 promise의 `operator new`/`operator delete` 오버로드와 연계해 custom allocator를 주입하는 패턴이 사용됩니다. 이렇게 하면 할당 비용은 줄지만, 버퍼 수명 관리와 스레드 안전성은 설계자가 책임져야 합니다.

## suspend / resume 비용

suspend 지점을 넘어 살아남아야 하는 **로컬 상태**가 코루틴 프레임에 저장되고, resume 시 다시 사용됩니다. "모든 레지스터를 통째로 저장한다"기보다, 컴파일러가 **각 suspend 지점에서 살아 있는 값만** 프레임에 스필(spill)하고 resume 함수를 별도 경로로 아웃라인하는 방식이며, 정확한 코드 생성은 **컴파일러·최적화 수준에 따라 다릅니다**. 이 저장/복원과 **상태 머신 분기** 비용이 매 suspend/resume마다 듭니다. 코루틴이 인라인되지 않으면 이 경로가 여러 번 오가므로, 매우 짧은 연산만 하고 suspend하는 패턴은 상대적으로 오버헤드가 눈에 띕니다.

**네트워크/IO 대기**처럼 suspend된 시간이 긴 경우에는, suspend/resume 비용은 대기 시간에 비해 무시할 수 있을 수 있습니다. 반대로 **연산만 하고 곧바로 반환**하는 코루틴은 suspend/resume이 곧바로 오버헤드로 나타나므로, Low-latency 핫패스에는 맞지 않을 수 있습니다.

## Low-latency 경로에서의 사용 기준

**µs 단위 핫패스**에서는 코루틴의 프레임 할당과 suspend/resume 비용이 허용 한도를 넘을 수 있으므로, 코루틴 대신 **동기 코드**, **콜백**, **상태 기계**를 쓰는 편이 나을 수 있습니다. **std::async**는 별도 스레드/풀과 연계되므로 지연과 스케줄링 비용이 있고, 단순 "한 번 비동기로 실행"에는 과할 수 있습니다.

**언제 코루틴을 쓸지**: 비동기 IO·이벤트 루프·지연이 큰 작업을 하나의 제어 흐름으로 쓰기 좋을 때, 그리고 할당·suspend 비용이 그 이득에 비해 작을 때 사용합니다. **언제 피할지**: 지연이 매우 짧고 호출 빈도가 높은 경로, 또는 할당을 피하기 어려운 구조일 때는 동기 경로나 콜백/상태 기계를 선택하는 것이 안전합니다.

## 평가 기준 (학습 성과 목표)

- C++20 코루틴의 **프레임**·**suspend/resume** 동작과 **promise_type**·**awaitable** 역할을 설명할 수 있다.
- 프레임 **힙 할당**과 **사용자 할당자/버퍼**로 할당을 제거하는 방법을 구분할 수 있다.
- µs 단위 핫패스에서는 코루틴 대신 **동기·콜백·상태 기계**를 선택하고, 비동기 IO·긴 지연 시에만 코루틴을 고려할 수 있다.

## 판단 기준 (언제 쓸고 언제 피할지)

| 상황 | 권장 | 비권장 |
|------|------|--------|
| 비동기 IO·이벤트 루프·긴 지연 | 코루틴(할당·suspend 비용 감수) | µs 핫패스에 코루틴 |
| µs 단위·고빈도 호출 | 동기 코드, 콜백, 상태 기계 | 코루틴 |
| 프레임 할당 제거 | 사용자 할당자·미리 할당 버퍼 | 기본 힙 할당 유지 |

**적용 체크리스트**: (1) 핫패스 지연·호출 빈도 평가. (2) 코루틴 사용 시 프레임 할당·suspend 비용 벤치마크. (3) 필요 시 동기/콜백/상태 기계로 대체.

## 비판적 시각: 한계와 트레이드오프

- 코루틴은 **가독성·제어 흐름** 측면에서 비동기 코드를 단순하게 쓸 수 있게 한다. "무조건 피하기"가 아니라, 지연·빈도가 허용할 때만 사용하고 비용을 측정하는 것이 합리적이다.
- **할당 제거**를 위해 사용자 할당자·버퍼를 쓰면 수명·스레드 안전성 책임이 설계자에게 있으므로, 문서화와 테스트가 필요하다.

## 핵심 요약

| 항목 | 요약 |
|------|------|
| 프레임 | 상태·지역변수·재개 지점 저장, 기본 힙 할당 |
| suspend/resume | 살아 있는 값만 스필·분기 비용; 짧은 연산만 하면 오버헤드 상대적 큼 |
| Low-latency | µs 경로는 동기·콜백·상태 기계; 코루틴은 긴 지연·비동기 IO에 |

### 용어 정리

| 용어 | 설명 |
|------|------|
| **coroutine frame** | 코루틴의 상태·지역 변수·재개 지점을 담는 블록; 기본적으로 힙 할당 |
| **promise_type** | 코루틴 반환값·예외·최종 정리 제어 |
| **awaitable** | co_await 시 suspend/resume 동작 정의 |

### 벤치마크 결과 해석 가이드

| 관찰 | 해석·다음 단계 |
|------|----------------|
| 코루틴 경로가 동기 코드보다 느림 | 프레임 할당·suspend/resume 비용; µs 경로면 동기/콜백/상태 기계 고려 |
| 사용자 할당자 도입 후 지연 감소 | 힙 할당 제거 효과; 버퍼 수명·스레드 안전성 문서화 |
| suspend 빈도가 높을수록 오버헤드 증가 | 짧은 연산만 하고 suspend하는 패턴은 비권장 |

### 자주 묻는 질문 (FAQ)

**Q: 코루틴은 항상 힙 할당하나요?**  
A: 기본적으로 구현체가 힙에 할당하는 경우가 많습니다. 사용자 제공 할당자·미리 할당된 버퍼로 제거할 수 있습니다.

**Q: µs 단위 경로에 코루틴을 써도 되나요?**  
A: 권장하지 않습니다. 동기 코드·콜백·상태 기계가 적합합니다. 코루틴은 비동기 IO·긴 지연 시에 고려합니다.

**Q: suspend/resume 비용은 얼마나 되나요?**  
A: 구현체·플랫폼에 따라 다릅니다. 격리 벤치마크로 측정하고, 네트워크 대기 등 긴 지연에서는 상대적으로 무시할 수 있습니다.

### 적용 체크리스트 (실무용)

- [ ] 핫패스 지연·호출 빈도 평가 후 코루틴 사용 여부 결정했는가?
- [ ] 코루틴 사용 시 프레임 할당·suspend 비용 벤치마크했는가?
- [ ] 필요 시 동기/콜백/상태 기계 대안을 검토했는가?
- [ ] 사용자 할당자·버퍼 사용 시 수명·스레드 안전성 문서화했는가?

### 진단 도구 요약

| 목적 | 도구·방법 |
|------|-----------|
| 프레임 할당 비용 | 격리 벤치마크, 사용자 할당자 전후 비교 |
| suspend/resume 비용 | suspend 횟수·빈도별 지연 측정 |
| 대안 비교 | 동기·콜백·상태 기계와 동일 시나리오 벤치마크 |

### 자주 하는 실수

- **µs 핫패스에 코루틴 도입**: 지연·빈도가 허용할 때만 사용하고, 동기/콜백/상태 기계를 우선 검토합니다.
- **프레임 할당 무시**: 기본 힙 할당 비용을 벤치마크하고, 필요 시 사용자 할당자·버퍼로 제거합니다.
- **suspend 빈도 과다**: 짧은 연산만 하고 suspend하면 오버헤드가 상대적으로 커지므로, suspend 구간을 줄이거나 대안을 고려합니다.

### 리팩토링 시 주의

동기 코드를 코루틴으로 바꿀 때: (1) 지연·호출 빈도가 코루틴에 맞는지 평가, (2) 프레임 할당·suspend 비용 벤치마크, (3) 회귀 없을 때만 도입. 사용자 할당자 도입 시 버퍼 수명·스레드 안전성을 명확히 하고 테스트를 추가합니다.

### 추가 읽기 및 관련 챕터

- **챕터 09 (Modern C++)**: Ranges·Concepts(런타임 비용 없음)와 대비.
- **챕터 11 (예외 처리 심화)**: 예외·noexcept와 성능.
- **챕터 12 (인라이닝)**: 인라인 여부가 코루틴 경로에도 영향.

---

## 다음 장에서는

**이전 장**: [Modern C++ 기능](/post/cpp-optimization/modern-cpp-features/) (챕터 09)

**예외 처리 심화**를 다룹니다. zero-cost exception의 실제 동작, noexcept 전략, 예외 사양이 인라이닝·코드 생성에 미치는 영향을 마이크로벤치마크로 검증합니다. → [예외 처리 심화](/post/cpp-optimization/exception-deep-dive/) (챕터 11)
