---
draft: true
collection_order: 450
image: "wordcloud.png"
description: "패키지 구조의 네 가지 접근법을 다룹니다. 계층별, 기능별, 포트와 어댑터, 컴포넌트별 패키지 구성과 각각의 장단점, 그리고 접근 제한자로 의존성 규칙을 컴파일러가 강제하게 만드는 컴파일 가능한 Java 예제를 설명합니다."
title: "[Clean Architecture] 45. 빠진 장: 패키지 구조"
slug: missing-chapter-package-structure
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean-Architecture(클린아키텍처)
  - Software-Architecture(소프트웨어아키텍처)
  - Java
  - Encapsulation(캡슐화)
  - Cohesion(응집도)
  - Interface(인터페이스)
  - Refactoring(리팩토링)
  - History(역사)
  - Case-Study
  - Package-by-Layer
  - Package-by-Feature
  - Ports-and-Adapters
  - Package-by-Component
  - Access-Modifier
  - Compiler-Enforcement
  - Module-System
  - Factory
  - Repository-Pattern
  - Use-Case
  - Package-Visibility
  - Directory-Structure
  - Hexagonal-Architecture
  - Simon-Brown
  - JPMS
  - Encapsulation-Enforcement
---

[44장: 사례 연구](/post/clean-architecture/case-study-video-sales-system/)에서 액터·유스케이스·엔터티·컴포넌트를 설계했지만, 그 설계를 실제 소스 코드의 **디렉터리 구조**로 어떻게 옮길지는 다루지 않았다. 마틴의 책에는 이 질문에 대한 답이 **빠져 있는데**, 2판(2023년 서문에서 마틴이 직접 언급)에 사이먼 브라운(Simon Brown, 『Software Architecture for Developers』 저자)이 "빠진 장(The Missing Chapter)"을 기고해 이 공백을 메웠다(Martin, 『Clean Architecture』, 2017, 34장).

패키지 구조가 왜 별도로 다룰 만한 문제인지부터 짚어야 한다. 아무리 유스케이스·엔터티·경계를 잘 설계해도, 그 설계가 실제 폴더와 클래스 가시성으로 반영되지 않으면 다른 개발자가 실수로(혹은 마감에 쫓겨) 경계를 넘나드는 `import`를 추가하는 것을 막을 방법이 없다. 설계 문서는 코드 리뷰에서나 참고될 뿐, 컴파일 시점에는 아무 힘이 없다.

## 네 가지 패키지 구성법

브라운은 실무에서 흔히 쓰이는 패키지 구성법 네 가지를 비교하며, 각각이 아키텍처를 얼마나 "강제"하는지를 기준으로 평가한다.

### 1. 계층별 패키지 (Package by Layer)

가장 흔한 방식은 기술적 역할(컨트롤러, 서비스, 저장소)을 기준으로 최상위 패키지를 나누는 것이다.

```
com.myapp/
├── controllers/
│   └── OrderController
├── services/
│   └── OrderService
├── repositories/
│   └── OrderRepository
└── models/
    └── Order
```

이 구조의 근본적인 문제는 **기능 하나를 추가하려면 거의 항상 패키지 네 개를 동시에 수정해야 한다**는 점이다. "주문 취소" 기능 하나를 넣으려 해도 `controllers`·`services`·`repositories`·`models`를 모두 열어야 하므로, 계층별 패키지는 "이 기능이 어디 있는지"보다 "이 계층에 뭐가 있는지"를 기준으로 코드를 조직한다. 게다가 `OrderService`가 `public`이면 다른 서비스나 컨트롤러가 얼마든지 그 내부 구현에 직접 접근할 수 있어, 계층 간 경계가 관례로만 존재하고 컴파일러는 이를 전혀 강제하지 않는다.

### 2. 기능별 패키지 (Package by Feature)

기능(도메인 개념) 단위로 패키지를 나누면 계층별 패키지의 첫 번째 문제는 해결된다.

```
com.myapp/
├── orders/
│   ├── OrderController
│   ├── OrderService
│   ├── OrderRepository
│   └── Order
└── payments/
    ├── PaymentController
    └── ...
```

이제 "주문" 관련 코드는 모두 `orders` 패키지 하나에 모여 있어, 기능 하나를 바꿀 때 여러 패키지를 오갈 필요가 없다. 응집도(cohesion) 측면에서는 계층별 패키지보다 명백히 낫다. 그러나 대가가 있다 — 같은 패키지 안에서는 컨트롤러가 리포지토리를, 리포지토리가 컨트롤러를 직접 참조해도 컴파일러가 막지 않는다. 계층 구분이 사라진 것이 아니라, 그 구분을 지킬지 말지가 온전히 개발자의 규율에 맡겨진 것이다.

### 3. 포트와 어댑터 (Ports and Adapters)

헥사고날 아키텍처로도 불리는 이 방식은 도메인을 중심에 두고, 그 도메인이 외부와 통신하는 지점(포트)과 실제 구현(어댑터)을 명시적으로 분리한다.

```
com.myapp/
├── domain/
│   ├── Order
│   └── OrderService
├── application/
│   └── OrderUseCase
└── infrastructure/
    ├── OrderController
    └── JpaOrderRepository
```

이 구조는 지금까지 이 시리즈에서 다뤄온 Clean Architecture의 계층(엔터티→유스케이스→인터페이스 어댑터→프레임워크)을 패키지 이름으로 직접 반영한다는 점에서 가장 원칙에 충실하다. `domain`이 `infrastructure`를 참조하지 않는 한, 의존성 규칙이 패키지 구조에서도 시각적으로 드러난다. 문제는 복잡성이다 — 작은 애플리케이션에서도 `domain`·`application`·`infrastructure` 세 계층을 항상 유지해야 하므로, 기능 하나 추가에 필요한 파일 수와 탐색 깊이가 계층별·기능별 패키지보다 늘어난다.

### 4. 컴포넌트별 패키지 (Package by Component)

브라운이 최종적으로 제안하는 방식은 앞의 세 방식과는 다른 축에서 접근한다 — 계층이나 기능이 아니라 **완결된 비즈니스 역량(컴포넌트)** 단위로 패키지를 나누고, 그 패키지 안의 구현 세부사항은 `public` 파사드 하나만 남기고 모두 package-private으로 숨긴다.

```
com.myapp.orders/
├── internal/
│   ├── OrderServiceImpl
│   └── JpaOrderRepository
└── OrderComponent (public facade)
```

이 방식의 핵심은 단순히 "패키지를 이렇게 나누자"는 관례가 아니라, 자바의 **접근 제한자를 이용해 그 관례를 컴파일러 수준에서 강제한다**는 데 있다. `internal` 패키지의 클래스들을 package-private으로 선언하면, `com.myapp.orders` 패키지 바깥의 어떤 코드도 `OrderServiceImpl`이나 `JpaOrderRepository`를 직접 `import`할 수 없다 — 아예 컴파일이 되지 않는다. 앞의 세 방식이 "이렇게 구성하기를 권장한다"에 그쳤다면, 컴포넌트별 패키지는 "이렇게 구성하지 않으면 빌드가 깨진다"로 강제 수준을 한 단계 끌어올린다.

다음 표는 네 가지 방식을 강제력(컴파일러가 위반을 막아주는 정도) 기준으로 비교한 것이다.

| 방식 | 응집 기준 | 계층 경계 강제 | 컴파일러 강제 |
|------|----------|--------------|-------------|
| 계층별 패키지 | 기술적 역할 | 약함(관례) | 없음 |
| 기능별 패키지 | 도메인 개념 | 없음 | 없음 |
| 포트와 어댑터 | Clean Architecture 계층 | 강함(관례) | 없음(패키지만으로는) |
| 컴포넌트별 패키지 | 비즈니스 역량 | 강함 | **있음**(접근 제한자) |

## 컴파일러 강제

패키지 구조만으로는 **부족**하다. 아무리 "이 패키지는 외부에서 쓰면 안 된다"고 문서에 적어도, 개발자가 실수로(혹은 급해서) `import`를 추가하면 컴파일은 아무 문제 없이 통과한다. 브라운이 강조하는 지점은 정확히 여기다 — 규칙을 사람이 지키게 하지 말고, **컴파일러가 지키게 만들라**는 것이다.

### 접근 제한자 활용

가장 직접적인 방법은 자바의 default(package-private) 접근 제한자를 이용하는 것이다. 아래 예제는 `OrderService` 인터페이스만 `public`으로 공개하고, 실제 구현체(`OrderServiceImpl`)는 같은 패키지 밖에서 접근할 수 없도록 감춘다. 팩토리(`OrderServiceFactory`)만이 구현체를 생성해 인터페이스 타입으로 반환하므로, 외부 패키지는 구현이 무엇인지 전혀 알 필요가 없다.

```java
import java.util.HashMap;
import java.util.Map;

// 외부에 공개되는 계약 — 이것만 다른 패키지에서 볼 수 있다
interface OrderRecord {
    String getId();
    int getTotal();
}

// package-private 구현 — 같은 패키지 밖에서는 이 클래스 이름조차 참조할 수 없다
class OrderServiceImpl implements OrderService {
    private final Map<String, OrderRecord> store = new HashMap<>();

    @Override
    public void save(OrderRecord order) {
        store.put(order.getId(), order);
    }

    @Override
    public OrderRecord findById(String id) {
        return store.get(id);
    }
}

// 외부에 공개되는 서비스 계약
interface OrderService {
    void save(OrderRecord order);
    OrderRecord findById(String id);
}

// public 팩토리만이 구현체 생성을 담당 — 외부는 이 메서드만 호출한다
public class OrderServiceFactory {
    public static OrderService create() {
        return new OrderServiceImpl();
    }
}
```

이 예제를 같은 패키지 안에서 컴파일하면 아무 문제가 없다. 그러나 다른 패키지에서 `new OrderServiceImpl()`을 시도하면 `OrderServiceImpl has private access`류의 컴파일 오류가 발생한다 — 코드 리뷰가 아니라 **빌드 자체가 위반을 막는다**. 이것이 "포트와 어댑터"와 "컴포넌트별 패키지"의 결정적 차이다. 전자는 관례로 계층을 나누고, 후자는 그 관례를 컴파일러에게 위임한다.

### 모듈 시스템

패키지 하나를 넘어 여러 패키지로 이루어진 컴포넌트를 캡슐화하려면, Java 9부터 도입된 모듈 시스템(JPMS)의 `exports` 선언을 사용할 수 있다. 아래는 개념을 보여주는 `module-info.java` 예시다(모듈 시스템은 별도의 컴파일 단위이므로 이 시리즈의 다른 예제처럼 단일 파일로 컴파일 검증하지는 않는다).

```
module com.myapp.orders {
    exports com.myapp.orders.api;  // 공개할 것만 export
    // com.myapp.orders.internal 패키지는 명시적으로 export하지 않으므로
    // 모듈 바깥에서는 그 존재조차 참조할 수 없다
}
```

접근 제한자가 "같은 패키지 안에서는 서로 다 보인다"는 한계를 갖는 반면, 모듈 시스템은 여러 패키지로 구성된 컴포넌트 전체의 경계를 선언할 수 있다는 점에서 더 강력하다. 다만 실무에서는 접근 제한자만으로도 대부분의 캡슐화 목적을 달성할 수 있어, 모듈 시스템은 라이브러리 배포처럼 더 엄격한 경계가 필요한 경우에 주로 쓰인다.

## 흔한 오해

"컴포넌트별 패키지가 컴파일러로 강제되니 항상 최선"이라고 오해하기 쉽다. 실제로는 트레이드오프다 — 포트와 어댑터는 계층(도메인/애플리케이션/인프라)이라는 축을 엄격하게 지키는 대신 컴파일러의 도움을 받지 못하고, 컴포넌트별 패키지는 컴파일러의 도움을 받는 대신 계층 축이 아니라 컴포넌트 축으로 나뉘어 "이 코드가 도메인 로직인지 인프라 코드인지"가 패키지 구조만으로는 한눈에 안 보일 수 있다. 브라운도 이 둘을 "서로 다른 장점을 가진 건전한 전략"으로 병렬 제시하지, 후자가 전자의 상위 호환이라고 말하지 않는다.

또 다른 오해는 "패키지 구조를 한 번 잘 정하면 끝"이라고 믿는 것이다. 계층별 패키지로 시작한 프로젝트가 커지면서 기능별로, 다시 컴포넌트별로 리팩터링되는 것은 흔한 일이다. 이 장의 요지는 "처음부터 컴포넌트별 패키지를 써라"가 아니라, **프로젝트 규모와 팀이 감당할 수 있는 복잡성에 맞춰 강제 수준을 선택하고, 필요해지면 컴파일러의 도움을 받는 방향으로 리팩터링하라**는 것이다.

## 학습 목표

이 장을 읽은 후 다음을 스스로 점검한다.

- 계층별 패키지에서 기능 하나를 추가할 때 왜 여러 패키지를 동시에 수정해야 하는지 설명할 수 있는가?
- "패키지 구조로 계층을 나누는 것"과 "접근 제한자로 계층을 강제하는 것"의 차이를 코드로 보여줄 수 있는가?
- 포트와 어댑터와 컴포넌트별 패키지가 각각 어떤 축(계층 vs 컴포넌트)을 기준으로 나뉘는지 설명할 수 있는가?
- 프로젝트 규모에 따라 어떤 패키지 구성법을 선택할지 판단 기준을 제시할 수 있는가?

## 판단 기준

새 프로젝트나 리팩터링에서 패키지 구조를 정할 때 다음을 확인한다.

- 기능 하나를 추가·수정할 때 서로 다른 최상위 패키지 여러 개를 열어야 하는가? 그렇다면 계층별 패키지의 문제를 겪고 있는 것이다.
- 같은 패키지 안의 구현 클래스를 다른 패키지에서 실수로 `import`한 적이 있는가? 있다면 package-private 접근 제한자로 강제할 후보다.
- 팀이 계층(도메인/애플리케이션/인프라) 구분을 엄격히 지킬 규율이 있는가, 아니면 컴파일러의 강제가 필요한가? 후자라면 컴포넌트별 패키지를 고려한다.

## 참고 자료

- Robert C. Martin, 『Clean Architecture』(2017), 34장 "The Missing Chapter"(Simon Brown 기고) — 네 가지 패키지 구성법과 컴파일러 강제 원칙의 원출처.
- [serodriguez68/clean-architecture — Chapter 34: Package Organization Strategies](https://github.com/serodriguez68/clean-architecture/blob/master/part-6-details.md) — 인용문 대조에 사용한 책 요약본.

## 핵심 요약

| 방식 | 응집 기준 | 컴파일러 강제 |
|------|----------|-------------|
| 계층별 패키지 | 기술적 역할 | 없음 |
| 기능별 패키지 | 도메인 개념 | 없음 |
| 포트와 어댑터 | Clean Architecture 계층 | 없음 |
| 컴포넌트별 패키지 | 비즈니스 역량 | 있음(접근 제한자) |

> "The best approach to enforce this architectural principle is via the compiler."
> — Simon Brown, 『Clean Architecture』(2017), 34장 "The Missing Chapter"

---

## Clean Architecture 커리큘럼을 마치며

지금까지 소프트웨어 아키텍처의 역사부터 Clean Architecture의 모든 원칙까지 살펴보았다. 핵심은 단 하나:

> **"의존성은 안쪽으로, 세부사항에서 정책으로."**

이 원칙을 이해하고 적용하면, 유지보수하기 쉽고, 테스트하기 쉽고, 확장하기 쉬운 소프트웨어를 만들 수 있다.
