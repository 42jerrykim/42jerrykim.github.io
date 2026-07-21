---
draft: false
collection_order: 20
slug: system-design-dependency-injection-architecture
title: "[Clean Code] 20. 시스템과 의존성 주입"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "객체를 만드는 과정(제작)과 그 객체를 사용하는 로직(사용)을 분리해야 하는 이유를 설명하고, Composition Root와 의존성 주입 컨테이너를 이용한 시스템 조립 전략을 서비스 로케이터 안티패턴 비판과 함께 다룬다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Dependency-Injection(의존성주입)
- Software-Architecture(소프트웨어아키텍처)
- System-Design
- Design-Pattern(디자인패턴)
- Code-Quality(코드품질)
- Best-Practices
- Maintainability
- Coupling(결합도)
- SOLID
- Java
- Testing(테스트)
- Implementation(구현)
- Pitfalls(함정)
- Interface(인터페이스)
- Microservices(마이크로서비스)
- Backend(백엔드)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Readability
- Encapsulation(캡슐화)
- Abstraction(추상화)
- OOP(객체지향)
- Performance(성능)
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 장은 [18–19장](/post/clean-code/clean-classes-solid-principles-oop/)에서 다룬 DIP와 생성자 주입을 애플리케이션 하나가 아니라 시스템 전체 규모로 확장한다. 여러 클래스가 협력하는 애플리케이션을 구성해 본 경험이 있으면 이해하기 쉽다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "제작과 사용의 분리"부터 "Composition Root"까지 | 객체 생성 로직이 비즈니스 로직에 섞이면 왜 문제인지 이해한다 |
| 실무자 | "판단 기준", "비판적 시각" | DI 컨테이너 도입 여부를 프로젝트 규모에 맞게 판단한다 |

## 제작과 사용의 분리

모든 프로그램은 두 가지 서로 다른 관심사로 나뉜다. 객체를 만들고 의존성을 서로 연결하는 **제작(construction)**, 그리고 그렇게 조립된 객체를 이용해 실제 요구사항을 처리하는 <strong>사용(use)</strong>이다. 이 두 관심사를 뒤섞으면, 비즈니스 로직 한가운데에 `new` 호출과 설정값 읽기 코드가 흩어져 시스템을 이해하기 어렵게 만든다.

```java
// Bad: 사용 로직 안에 제작 로직이 뒤섞여 있다
public class OrderProcessor {
    public void process(Order order) {
        PaymentGateway gateway = new StripePaymentGateway(loadApiKeyFromConfig());
        InventoryService inventory = new DatabaseInventoryService(new MySqlConnection());
        // ... 실제 주문 처리 로직
        gateway.charge(order.getTotal());
        inventory.reserve(order.getItems());
    }
}
```

`OrderProcessor`는 주문을 처리하는 것이 본연의 책임인데, 결제 게이트웨이 구현체를 어떻게 만들지, DB 연결을 어떻게 초기화할지까지 알아야 한다. 이는 18장에서 다룬 SRP를 시스템 수준에서 위반하는 것과 같다 — 결제 수단이 바뀌거나 DB 드라이버가 바뀔 때마다 주문 처리 로직과 무관한 이유로 이 클래스를 고쳐야 한다.

## Composition Root: 제작을 한곳으로 모으기

제작과 사용을 분리하는 실무적인 방법은, 애플리케이션 전체에서 객체를 조립하는 지점을 **단 하나의 위치**로 모으는 것이다. 이 지점을 흔히 **Composition Root**라 부르며, 대개 `main` 함수나 애플리케이션의 진입점 근처에 위치한다.

```java
// main()에 해당하는 Composition Root: 모든 제작 로직이 여기에 모인다
public class Application {
    public static void main(String[] args) {
        PaymentGateway gateway = new StripePaymentGateway(loadApiKeyFromConfig());
        InventoryService inventory = new DatabaseInventoryService(new MySqlConnection());

        OrderProcessor processor = new OrderProcessor(gateway, inventory);
        processor.run();
    }
}

// 사용 로직만 남은 OrderProcessor: 협력자를 생성자로 주입받는다
public class OrderProcessor {
    private final PaymentGateway gateway;
    private final InventoryService inventory;

    public OrderProcessor(PaymentGateway gateway, InventoryService inventory) {
        this.gateway = gateway;
        this.inventory = inventory;
    }

    public void process(Order order) {
        gateway.charge(order.getTotal());
        inventory.reserve(order.getItems());
    }
}
```

이 구조에서 `OrderProcessor`는 `PaymentGateway`와 `InventoryService`가 인터페이스라는 사실만 알고, 그 구현이 Stripe인지 다른 PG사인지, MySQL인지 다른 DB인지 전혀 몰라도 된다. 결제 수단을 바꾸는 변경은 Composition Root 한 곳만 수정하면 되고, `OrderProcessor`의 로직은 전혀 건드리지 않는다. 이 원리는 [19장](/post/clean-code/clean-classes-solid-principles-exercises/) 실습에서 `UserService`를 조립했던 방식을 시스템 전체 진입점으로 확장한 것이다.

## DI 컨테이너와 관심사 확장

객체 그래프가 작을 때는 위 예제처럼 생성자 호출을 손으로 나열하는 **Pure DI**로 충분하다. 하지만 협력자 수가 수십, 수백 개로 늘어나면 이 나열 작업 자체가 부담이 된다. 이때 Spring, Guice 같은 **DI 컨테이너**는 클래스에 붙은 애너테이션이나 설정 파일을 읽어 의존성 그래프를 자동으로 조립해준다. DI 컨테이너를 쓰더라도 원칙은 동일하다 — 컨테이너의 설정 자체가 Composition Root 역할을 하며, 비즈니스 로직 클래스들은 여전히 컨테이너의 존재를 몰라야 한다.

로깅, 트랜잭션 관리, 보안 검사처럼 여러 모듈에 공통으로 걸쳐 있는 관심사를 <strong>횡단 관심사(Cross-Cutting Concern)</strong>라 부른다. 이런 관심사를 각 클래스에 직접 코드로 흩뿌리면, 트랜잭션 정책 하나가 바뀔 때마다 수십 개의 클래스를 찾아 고쳐야 한다. <strong>관점 지향 프로그래밍(Aspect-Oriented Programming, AOP)</strong>은 이런 횡단 관심사를 별도의 선언(애너테이션, 프록시 설정)으로 분리해, 비즈니스 로직 코드에서 완전히 걷어내는 접근이다.

```java
// 트랜잭션 관심사가 애너테이션으로 분리되어 비즈니스 로직과 섞이지 않는다
public class OrderService {
    @Transactional
    public void placeOrder(Order order) {
        repository.save(order);
        inventory.reserve(order.getItems());
    }
}
```

## 흔한 오개념

<strong>"DI 프레임워크를 도입하면 자동으로 좋은 설계가 된다"</strong>는 오해가 흔하다. 실제로는 프레임워크가 의존성을 자동으로 연결해줄 뿐, 어떤 클래스가 어떤 협력자에 의존해야 하는지에 대한 설계 판단(18장의 SRP, DIP)은 여전히 사람이 해야 한다. DI 컨테이너 위에서도 God Class는 얼마든지 만들어질 수 있다.

<strong>"모든 의존성은 인터페이스 뒤에 숨겨야 한다"</strong>는 오해도 있다. 15장에서 다룬 판단 기준과 마찬가지로, 실제로 교체되거나 모킹될 필요가 없는 안정적인 값 객체(예: `Money`, `DateRange`)까지 인터페이스로 감싸는 것은 불필요한 간접 계층만 늘린다.

## 판단 기준: Pure DI vs DI 컨테이너

객체 그래프가 작고(수 개–십여 개 클래스) 팀 규모가 작다면, 프레임워크 없이 Composition Root에서 생성자를 직접 호출하는 Pure DI로 충분하며, 이는 컴파일 타임에 오류를 잡을 수 있고 디버깅도 단순하다는 장점이 있다. 반대로 마이크로서비스 하나가 수십 개의 서비스·리포지토리·어댑터로 구성되고, 트랜잭션·보안 같은 횡단 관심사가 여러 계층에 반복적으로 필요하다면 DI 컨테이너와 AOP의 이점이 도입 비용을 상회한다.

## 비판적 시각

DI 컨테이너, 특히 리플렉션 기반 프레임워크는 "이 객체가 어디서 어떻게 생성됐는가"를 코드를 읽는 것만으로 추적하기 어렵게 만든다는 비판을 꾸준히 받아왔다. 스택 트레이스에 프레임워크 내부 클래스가 잔뜩 섞여 나오거나, 설정 오류가 런타임에야 발견되는 문제는 Pure DI에서는 애초에 생기지 않는 종류의 디버깅 비용이다. 이런 이유로 Mark Seemann을 비롯한 일부 DI 전문가들은 "DI 컨테이너는 필수가 아니라 선택적 편의 도구"이며, 소규모–중간 규모 프로젝트에서는 Pure DI가 오히려 더 명확하다고 주장한다. 또한 DI 컨테이너를 잘못 사용해 객체가 필요한 시점에 컨테이너에서 직접 조회하는 방식(**서비스 로케이터, Service Locator**)으로 흘러가면, 이는 의존성을 생성자로 명시하지 않고 숨기는 안티패턴이 되어 오히려 DIP가 해결하려던 문제(숨겨진 결합)를 재생산한다는 점도 널리 지적된다.

## 다음 장에서는

[21장: 창발적 설계 네 가지 규칙](/post/clean-code/emergent-design-simple-design-principles/)에서는 이 시리즈에서 다룬 여러 원칙을 관통하는 "단순한 설계"라는 상위 기준을 다룬다.

## 평가 기준

- [ ] 제작과 사용을 분리해야 하는 이유를 SRP와 연결해 설명할 수 있다.
- [ ] Composition Root 패턴으로 객체 그래프 조립을 한 곳에 모을 수 있다.
- [ ] Pure DI와 DI 컨테이너 중 프로젝트 규모에 맞는 선택을 할 수 있다.
- [ ] 서비스 로케이터가 왜 DIP를 오히려 훼손하는 안티패턴인지 설명할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 11장.
- Fowler, M. *Inversion of Control Containers and the Dependency Injection pattern*. [https://martinfowler.com/articles/injection.html](https://martinfowler.com/articles/injection.html)
- Seemann, M., & Deursen, S. (2019). *Dependency Injection Principles, Practices, and Patterns*. Manning.
