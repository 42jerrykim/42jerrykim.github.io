---
draft: false
collection_order: 22
slug: concurrency-multithreading-parallel-programming
title: "[Clean Code] 22. 동시성 결함과 방어 원칙"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "동시성이 무엇(what)과 언제(when)를 분리하는 전략임을 설명하고, 자료 범위 제한·자료 사본 사용 같은 동시성 방어 원칙을 경쟁 조건 예제와 jcstress 검증 절차, 암달의 법칙 기반 판단 기준으로 함께 다룬다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Concurrency(동시성)
- Thread
- Synchronization
- Code-Quality(코드품질)
- Best-Practices
- Maintainability
- Java
- Debugging(디버깅)
- Testing(테스트)
- Implementation(구현)
- Pitfalls(함정)
- Edge-Cases(엣지케이스)
- Performance(성능)
- Async(비동기)
- System-Design
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Readability
- Refactoring(리팩토링)
- SOLID
- Coupling(결합도)
- Code-Review(코드리뷰)
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 장은 [18장](/post/clean-code/clean-classes-solid-principles-oop/)에서 다룬 SRP를 동시성이라는 새로운 차원에 적용한다. 스레드나 비동기 처리를 한 번이라도 다뤄 본 경험이 있으면 이해하기 쉽지만, 필수는 아니다. 이 장의 깊이는 중급이며, 락 프리 자료구조나 메모리 모델의 세부 사항 같은 전문가 수준 주제는 다루지 않는다. 그 내용은 별도의 시스템 프로그래밍 시리즈에서 다룰 범위다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "동시성이 필요한 이유"부터 "동시성 방어 원칙"까지 | 동시성이 왜 필요하고 왜 위험한지 개념적으로 이해한다 |
| 실무자 | "판단 기준", "비판적 시각", 검증 절차 | 실제 동시성 버그를 진단하고 검증 도구로 확인하는 방법을 익힌다 |

## 동시성은 결합을 없애는 전략이다

**동시성(Concurrency)**은 본질적으로 "무엇(what)을 하는가"와 "언제(when) 하는가"를 분리하는 전략이다. 단일 스레드 프로그램에서는 이 둘이 강하게 묶여 있다 — 코드에 적힌 순서가 곧 실행 순서다. 동시성을 도입하면 여러 작업의 실행 순서를 실행 환경(스케줄러)에 맡기게 되고, 그 대가로 처리량과 응답성을 얻는 대신 코드의 예측 가능성을 잃는다. 이 트레이드오프를 이해하지 못한 채 "빠르게 만들고 싶으니 일단 멀티스레드로 만든다"는 접근은 오히려 디버깅하기 매우 어려운 버그를 만든다.

## 흔한 미신과 오개념

**"동시성은 항상 성능을 개선한다"**는 오해가 가장 흔하다. 스레드를 늘리는 것은 CPU 코어 수, 작업의 병렬화 가능 비율, 스레드 간 조율 비용(락 경합, 컨텍스트 스위칭)에 따라 오히려 성능을 떨어뜨릴 수 있다. 특히 작업 대부분이 공유 자원에 대한 락을 기다리는 데 소요된다면, 스레드를 아무리 늘려도 처리량은 늘지 않는다.

**"동시성 문제는 충분히 테스트하면 다 잡아낼 수 있다"**는 오해도 위험하다. 동시성 버그는 특정 스레드 스케줄링 순서에서만 드러나는 **비결정적(non-deterministic)** 성격을 갖는다. 개발 환경에서 수천 번 실행해도 재현되지 않던 경쟁 조건이 프로덕션의 특정 부하 패턴에서만 나타나는 경우가 흔하며, "테스트를 통과했다"는 사실이 "동시성 버그가 없다"는 증명이 되지 못한다.

## 동시성 방어 원칙

동시성 관련 코드는 다른 로직과 뒤섞이지 않도록 분리해야 한다는 것이 첫 번째 방어 원칙이다. 이는 18장에서 다룬 SRP를 동시성에 적용한 것으로, 동시성 코드는 그 자체로 복잡하기 때문에 비즈니스 로직과 섞이면 두 종류의 복잡성이 곱해진다.

두 번째 원칙은 공유 자료의 범위(critical section)를 최대한 좁게 제한하는 것이다. `synchronized` 블록이나 락으로 보호하는 코드 구간이 넓을수록 다른 스레드가 그 자원을 기다리는 시간이 늘어나고, 동시에 그 넓은 구간 안에서 우연한 결합이 생길 위험도 커진다. 세 번째 원칙은 가능하다면 공유 자료의 사본을 사용해 애초에 경쟁 자체를 없애는 것이다 — 여러 스레드가 같은 가변 객체를 공유하는 대신, 각자 불변 사본을 갖고 작업한 뒤 결과만 병합하면 락이 필요 없어진다.

## 경쟁 조건: 깨진 코드에서 검증까지

아래 카운터는 단일 스레드에서는 완벽하게 동작하지만, 여러 스레드가 동시에 `increment()`를 호출하면 값이 조용히 틀어진다.

```java
// 깨진 코드: 자연스러워 보이지만 스레드 안전하지 않다
public class Counter {
    private int count = 0;
    public void increment() {
        count = count + 1; // 읽기-수정-쓰기가 원자적이지 않다
    }
    public int get() { return count; }
}
```

이 코드가 깨지는 이유는 `count = count + 1`이 하나의 명령이 아니라 "읽기 → 더하기 → 쓰기"라는 세 단계로 컴파일되기 때문이다. 두 스레드가 동시에 `count`가 5인 상태를 읽고, 각자 6을 계산해 쓰면, 두 번의 증가가 있었음에도 최종값은 6이 된다 — 이는 자바 언어 명세(Java Language Specification)가 이 세 단계의 원자성을 보장하지 않기 때문에 "우연히 대부분 동작"할 뿐 "항상 정확하다고 보장"되지 않는다.

```java
// 올바른 구현: java.util.concurrent.atomic으로 원자적 연산을 보장한다
import java.util.concurrent.atomic.AtomicInteger;

public class Counter {
    private final AtomicInteger count = new AtomicInteger(0);
    public void increment() {
        count.incrementAndGet(); // CAS(Compare-And-Swap) 기반 원자적 연산
    }
    public int get() { return count.get(); }
}
```

`AtomicInteger`는 CAS(Compare-And-Swap) 명령을 이용해 "읽기-수정-쓰기"를 하드웨어 수준에서 원자적으로 수행하므로, 두 스레드가 동시에 호출해도 두 번의 증가가 모두 정확히 반영된다.

두 버전의 실제 안전성 차이는 OpenJDK의 **jcstress**(Java Concurrency Stress) 도구로 검증할 수 있다. jcstress는 여러 스레드가 동시에 같은 상태를 조작하도록 강제로 스케줄링하며 관찰 가능한 모든 상태 조합을 통계로 수집한다.

```bash
# jcstress로 두 Counter 구현을 스트레스 테스트한다
mvn clean verify
java -jar target/jcstress.jar -t CounterTest -m stress
```

깨진 버전은 반복 실행 시 `count`가 예상보다 작은 값으로 관찰되는 사례가 리포트에 나타나고, `AtomicInteger` 기반 버전은 모든 반복에서 정확한 값만 관찰된다. 다만 "이번 실행에서 문제가 관찰되지 않았다"는 것이 "이 코드가 모든 하드웨어와 JVM 구현에서 항상 안전하다"는 증명은 아니라는 점을 분명히 해야 한다 — 경쟁 조건은 CPU 아키텍처, JIT 최적화 수준, 시스템 부하에 따라 발현 빈도가 크게 달라지므로, 검증 도구가 문제를 찾지 못했다는 것은 "이번 조건에서는 못 찾았다"이지 "안전이 증명됐다"가 아니다.

## 판단 기준: 언제 동시성을 도입할 가치가 있는가

동시성을 도입하기 전에 "이 작업이 실제로 병렬화 가능한 비율이 얼마나 되는가"를 먼저 따져야 한다. 암달의 법칙(Amdahl's Law)이 보여주듯, 작업의 일부만 병렬화 가능하고 나머지가 순차적으로 실행돼야 한다면 스레드를 아무리 늘려도 전체 성능 향상은 그 순차 부분에 의해 상한이 정해진다. I/O 대기가 대부분인 작업(네트워크 호출, 파일 읽기)은 비동기 처리로 큰 이득을 보지만, 이미 CPU를 포화 상태로 쓰는 연산 위주 작업에 스레드를 추가로 투입하는 것은 컨텍스트 스위칭 비용만 늘릴 수 있다.

## 비판적 시각

동시성 코드의 근본적인 어려움은 "정상적으로 보인다"와 "실제로 안전하다"를 구분하기 어렵다는 데 있다. 위에서 다룬 검증 절차도 특정 실행 환경, 특정 하드웨어(x86과 ARM은 메모리 모델의 세부 보장이 다르다)에서 관찰한 결과일 뿐이며, 다른 조건에서는 다르게 동작할 수 있다. 이 근본적 불확실성 때문에 Java Concurrency in Practice(Goetz et al., 2006)를 비롯한 여러 저작은 "가능하다면 직접 락을 다루는 저수준 동시성 코드를 작성하지 말고, 검증된 고수준 동시성 유틸리티(`java.util.concurrent`의 실행자, 동시성 컬렉션, 원자 변수)를 사용하라"고 강조한다. 직접 락을 설계하고 검증하는 비용은 대부분의 애플리케이션 개발에서 감당하기에 너무 크며, 이미 수많은 사례로 검증된 라이브러리 구현을 재사용하는 편이 훨씬 안전하다.

## 다음 장에서는

[23장: 리팩토링과 레거시 코드 개선](/post/clean-code/refactoring-techniques-legacy-code-improvement/)에서는 이 시리즈 전체에서 다룬 원칙들을 실제 레거시 코드에 종합적으로 적용하는 방법을 다룬다.

## 평가 기준

- [ ] 동시성을 "무엇과 언제의 분리"로 설명하고 그 트레이드오프를 논증할 수 있다.
- [ ] 경쟁 조건이 왜 발생하는지 "읽기-수정-쓰기의 비원자성"으로 설명할 수 있다.
- [ ] 동시성 방어 원칙(관심사 분리, critical section 최소화, 자료 사본)을 코드에 적용할 수 있다.
- [ ] 동시성 검증 도구의 "문제 미발견"이 "안전 증명"이 아니라는 한계를 설명할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 13장.
- Goetz, B., Peierls, T., Bloch, J., Bowbeer, J., Holmes, D., & Lea, D. (2006). *Java Concurrency in Practice*. Addison-Wesley.
- [OpenJDK jcstress](https://github.com/openjdk/jcstress)
