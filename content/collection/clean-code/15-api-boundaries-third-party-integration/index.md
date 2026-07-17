---
draft: false
collection_order: 15
slug: api-boundaries-third-party-integration
title: "[Clean Code] 15장. 경계 — 외부 라이브러리 사용법"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "외부 라이브러리 제공자와 사용자의 상반된 요구가 만드는 긴장을 짚고, 학습 테스트로 경계를 검증하는 방법과 어댑터 패턴으로 서드파티 API를 감싸 변경에 대비하는 전략을 판단 기준과 과잉 설계 비판까지 함께 다룬다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Design-Pattern(디자인패턴)
- Adapter
- Testing(테스트)
- Code-Quality(코드품질)
- Best-Practices
- Maintainability
- Coupling(결합도)
- Interface(인터페이스)
- Encapsulation(캡슐화)
- Java
- Implementation(구현)
- Pitfalls(함정)
- Error-Handling(에러처리)
- API(Application Programming Interface)
- Open-Source(오픈소스)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Refactoring(리팩토링)
- Readability
- Software-Architecture(소프트웨어아키텍처)
- Documentation(문서화)
- Code-Review(코드리뷰)
---

## 이 장을 읽기 전에

이 장은 [13~14장](/post/clean-code/error-handling-exceptions-best-practices/)에서 다룬 예외 어댑터 개념을 확장해, 외부 라이브러리 전체를 감싸는 경계 설계로 넓힌다. 최소 하나의 서드파티 라이브러리(로깅, HTTP 클라이언트 등)를 사용해 본 경험이 있으면 예제를 이해하기 쉽다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "외부 코드 사용의 긴장"부터 "학습 테스트"까지 | 외부 라이브러리를 그대로 노출하면 왜 위험한지 이해한다 |
| 실무자 | "판단 기준", "비판적 시각" | 어댑터를 도입할 가치가 있는 경계와 과잉 설계가 되는 경계를 구분한다 |

## 외부 코드 사용의 긴장

라이브러리나 프레임워크 제공자는 최대한 많은 사용 사례를 지원하려고 인터페이스를 범용적으로 설계한다. 반면 사용자는 자신의 특정 요구에 집중된 좁고 명확한 인터페이스를 원한다. 이 긴장은 특히 `Map`, `List` 같은 범용 컬렉션 타입을 애플리케이션 코드 전반에 그대로 노출할 때 잘 드러난다.

```java
// Bad: Map을 그대로 여기저기 전달한다
Map<String, Sensor> sensors = new HashMap<>();
Sensor s = sensors.get(sensorId);

// 이 Map을 인수로 받는 모든 함수는 clear(), remove() 같은
// Map의 모든 공개 메서드에 대한 접근 권한도 함께 받는다
```

`Map<String, Sensor>`를 그대로 전달하면, 이 값을 받는 모든 코드가 `sensors.clear()`를 호출해 전체 센서 목록을 지워버릴 수 있는 권한까지 함께 갖게 된다. 이는 애초에 그 코드가 필요로 하지 않는 권한이다. 이 문제는 필요한 동작만 제공하는 전용 클래스로 감싸면 해결된다.

```java
// Good: 필요한 동작만 제공하는 클래스로 감싼다
public class Sensors {
    private final Map<String, Sensor> sensors = new HashMap<>();

    public Sensor getById(String id) {
        return sensors.get(id);
    }
    // clear(), remove() 등은 외부에 노출하지 않는다
}
```

`Sensors` 클래스는 `Map`의 범용 인터페이스 중 이 애플리케이션이 실제로 필요로 하는 부분(`getById`)만 노출한다. `Map`의 구현이 `HashMap`에서 다른 자료구조로 바뀌더라도, 이 변경은 `Sensors` 클래스 내부에 갇히고 나머지 코드베이스는 영향을 받지 않는다.

## 경계를 살피고 익히기: 학습 테스트

새로운 서드파티 라이브러리를 도입할 때, 공식 문서만 읽고 바로 애플리케이션 코드에 통합하면 라이브러리의 실제 동작을 오해한 채로 코드를 작성하기 쉽다. **학습 테스트(Learning Tests)**는 라이브러리의 API를 우리 애플리케이션 코드가 아니라 별도의 테스트 코드에서 먼저 호출해 보며, 그 라이브러리가 우리가 기대하는 대로 동작하는지 검증하는 기법이다.

```java
// 학습 테스트: 로깅 라이브러리가 기대한 대로 동작하는지 애플리케이션 코드와 분리해 검증한다
@Test
void loggerAddsAppenderAndRotatesFileAtConfiguredSize() {
    Logger logger = LoggerFactory.getLogger("test");
    RollingFileAppender appender = new RollingFileAppender();
    appender.setMaximumFileSize("1KB");
    logger.addAppender(appender);

    for (int i = 0; i < 1000; i++) {
        logger.info("로그 메시지 " + i);
    }

    assertTrue(rotatedFilesExist());
}
```

이 테스트는 프로덕션 코드의 일부가 아니라, "이 라이브러리 버전에서 이 API가 문서대로 동작하는가"를 확인하는 안전망이다. 라이브러리를 업그레이드할 때 이 학습 테스트를 다시 실행하면, 새 버전에서 동작이 바뀌었는지 애플리케이션 코드를 건드리기 전에 즉시 알 수 있다. 이는 [16장](/post/clean-code/unit-testing-tdd-test-driven-development/)에서 다룰 테스트 스위트의 회귀 안전망 역할과 같은 원리를 경계 지점에 적용한 것이다.

## 아직 존재하지 않는 코드 사용하기

때로는 아직 구현되지 않았거나, 다른 팀이 개발 중이라 인터페이스가 확정되지 않은 외부 시스템과 통합해야 할 때가 있다. 이 경우 우리 쪽에서 원하는 인터페이스를 먼저 정의하고, 실제 구현이 준비되기 전까지는 이 인터페이스를 구현하는 임시 어댑터를 사용해 개발을 계속 진행할 수 있다.

```java
// 우리 쪽에서 필요를 기준으로 인터페이스를 먼저 정의한다
public interface TransmitterAdapter {
    void transmit(double frequency, byte[] data);
}

// 실제 하드웨어 API가 확정되기 전까지 사용할 임시 구현
public class FakeTransmitterAdapter implements TransmitterAdapter {
    public void transmit(double frequency, byte[] data) {
        System.out.println("전송 시뮬레이션: " + frequency + "Hz");
    }
}
```

나중에 실제 하드웨어 API가 확정되면, `TransmitterAdapter`를 구현하는 새 클래스 하나만 추가하면 되고 이 인터페이스를 사용하는 나머지 코드는 전혀 바뀌지 않는다. 이 접근은 GoF의 **어댑터 패턴(Adapter Pattern)**을 경계 관리에 적용한 것이며, 외부 시스템의 불확실성을 우리 코드베이스 안으로 끌어들이지 않고 인터페이스 뒤에 격리한다.

## 흔한 오개념

**"신뢰할 수 있는 유명 라이브러리는 감쌀 필요가 없다"**는 오해가 흔하다. 문제는 라이브러리의 신뢰도가 아니라, 그 라이브러리의 API가 우리 애플리케이션의 어휘와 일치하지 않는다는 점이다. 아무리 잘 만들어진 라이브러리라도, 그 API를 코드베이스 전역에 그대로 노출하면 나중에 라이브러리를 교체하거나 버전을 올릴 때 변경이 애플리케이션 코드 곳곳으로 퍼진다.

**"학습 테스트는 프로덕션 코드가 아니므로 시간 낭비다"**는 오해도 있다. 실제로는 학습 테스트에 들이는 시간이, 라이브러리 오해로 인해 프로덕션에서 발생하는 버그를 디버깅하는 시간보다 훨씬 적다. 또한 학습 테스트는 라이브러리 업그레이드 시 회귀를 즉시 감지하는 무료 안전망 역할도 겸한다.

## 판단 기준: 언제 감싸고 언제 그대로 쓸 것인가

모든 외부 의존성을 무조건 감쌀 필요는 없다. 판단 기준은 "이 라이브러리가 코드베이스 전역의 여러 곳에서 호출되는가"와 "이 라이브러리를 교체하거나 모킹해야 할 가능성이 있는가"이다. 두 질문 중 하나라도 "그렇다"면 어댑터로 감싸는 비용을 들일 가치가 있다. 반대로 특정 유틸리티 함수 하나를 애플리케이션의 한 지점에서만 호출한다면, 그 지점을 감싸는 별도 클래스를 만드는 것은 오히려 불필요한 간접 계층만 늘리는 과잉 설계가 될 수 있다.

## 비판적 시각

경계를 감싸는 전략에는 실질적인 비용이 따른다. 모든 외부 라이브러리 호출을 어댑터 뒤에 숨기면, 코드베이스에 "진짜 로직"과 "어댑터로의 위임"이라는 두 종류의 간접 계층이 늘어나고, 신입 개발자는 실제 동작을 확인하기 위해 여러 파일을 오가야 한다. YAGNI(You Aren't Gonna Need It) 원칙을 지지하는 개발자들은, 아직 라이브러리를 교체할 계획이 구체적으로 없다면 미리 어댑터를 만드는 것이 실현되지 않을 유연성에 선제적으로 비용을 지불하는 것이라고 비판한다. 실무적인 절충안은, 처음부터 모든 것을 감싸기보다 실제로 두 번째 구현체가 필요해지거나(테스트용 페이크, 대체 벤더) 두 번 이상 같은 라이브러리 호출부를 수정하게 됐을 때 그 시점에 어댑터를 도입하는 것이다.

## 다음 장에서는

[16장: TDD 법칙과 F.I.R.S.T 원칙](/post/clean-code/unit-testing-tdd-test-driven-development/)에서는 학습 테스트에서 다룬 "먼저 테스트로 검증한다"는 접근을 테스트 주도 개발 전체로 확장한다.

## 평가 기준

- [ ] 범용 컬렉션 타입을 그대로 노출하는 것의 위험성을 설명하고 전용 클래스로 감쌀 수 있다.
- [ ] 학습 테스트를 작성해 서드파티 라이브러리의 동작을 애플리케이션 코드와 독립적으로 검증할 수 있다.
- [ ] 아직 확정되지 않은 외부 API를 어댑터 인터페이스로 먼저 정의하고 개발을 진행할 수 있다.
- [ ] 어댑터 도입 여부를 "재사용 범위"와 "교체 가능성" 기준으로 판단할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 8장.
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley. "Adapter".
