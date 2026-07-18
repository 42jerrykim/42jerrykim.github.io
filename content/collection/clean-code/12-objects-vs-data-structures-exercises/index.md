---
draft: false
collection_order: 12
slug: objects-vs-data-structures-exercises
title: "[Clean Code] 12. 디미터 법칙 리팩토링 실습"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "정수 타입 코드로 도형 종류를 분기하는 절차적 계산기 코드를 다형성 객체로 변환하고, 여러 단계를 파고드는 기차 충돌 코드를 디미터 법칙에 따라 정리하는 두 가지 리팩토링 실습을 변경 시나리오 검증과 함께 진행한다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- OOP(객체지향)
- Refactoring(리팩토링)
- Encapsulation(캡슐화)
- Design-Pattern(디자인패턴)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Coupling(결합도)
- Java
- Implementation(구현)
- Pitfalls(함정)
- Polymorphism(다형성)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Code-Review(코드리뷰)
- Testing(테스트)
- Interface(인터페이스)
- Abstraction(추상화)
- SOLID
- Software-Architecture(소프트웨어아키텍처)
- Composition(합성)
---

## 이 장을 읽기 전에

이 장은 [11장: 객체와 자료구조의 비대칭](/post/clean-code/objects-vs-data-structures-design-patterns/)에서 다룬 개념(자료 추상화, 디미터 법칙, 기차 충돌)을 실제 코드에 적용하는 실습이다. 11장을 먼저 읽었다는 전제로 진행한다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 실습 1 전체 | 타입 코드 분기를 다형성으로 바꾸는 절차를 따라 한다 |
| 실무자 | 실습 2, "판단 기준" | 리팩토링이 실제로 변경 비용을 낮췄는지 시나리오로 검증한다 |

## 실습 1: 타입 코드를 다형성으로 변환

아래 코드는 정수 타입 코드(`SQUARE`, `RECTANGLE`, `CIRCLE`)로 도형을 구분하고, 넓이 계산 함수 안에서 이 타입 코드를 분기한다.

```java
// 실습 대상: 타입 코드로 분기하는 절차적 코드
public class GeometryCalculator {
    public static final int SQUARE = 1;
    public static final int RECTANGLE = 2;
    public static final int CIRCLE = 3;

    public double calculateArea(int shapeType, double... params) {
        switch (shapeType) {
            case SQUARE:    return params[0] * params[0];
            case RECTANGLE: return params[0] * params[1];
            case CIRCLE:    return Math.PI * params[0] * params[0];
            default: throw new IllegalArgumentException("Unknown shape type");
        }
    }
}
```

이 코드의 문제는 11장에서 다룬 표 그대로다. 새 도형(`Triangle`)을 추가하려면 `calculateArea`뿐 아니라, 만약 `calculatePerimeter` 같은 함수가 더 있었다면 그 함수들도 모두 찾아 분기를 추가해야 한다. 게다가 `params[0]`, `params[1]`이라는 위치 기반 인수는 어떤 도형이 몇 개의 인수를 요구하는지 타입 시스템으로 보장하지 못한다.

```java
// 리팩토링 결과: 각 도형이 자신의 넓이 계산 책임을 가진다
public interface Shape {
    double calculateArea();
}

public class Square implements Shape {
    private final double side;
    public Square(double side) { this.side = side; }
    public double calculateArea() { return side * side; }
}

public class Rectangle implements Shape {
    private final double width, height;
    public Rectangle(double width, double height) { this.width = width; this.height = height; }
    public double calculateArea() { return width * height; }
}

public class Circle implements Shape {
    private final double radius;
    public Circle(double radius) { this.radius = radius; }
    public double calculateArea() { return Math.PI * radius * radius; }
}
```

이제 새 도형을 추가하려면 `Shape`를 구현하는 클래스 하나만 작성하면 되고, 기존 `Square`, `Rectangle`, `Circle`은 전혀 건드릴 필요가 없다. 대신 이 설계는 11장에서 짚은 트레이드오프대로, 만약 나중에 "모든 도형의 둘레를 출력하는 새 리포트 기능"처럼 새로운 연산이 자주 추가되는 시스템이라면 오히려 모든 클래스를 순회하며 고쳐야 하는 비용이 생긴다는 점도 함께 기억해야 한다.

## 실습 2: 기차 충돌 코드 정리

다음 코드는 주문 시스템에서 배송지의 우편번호를 가져오는 과정을 보여준다.

```java
// 실습 대상: 여러 단계를 파고드는 기차 충돌
String zipCode = order.getCustomer().getAddress().getShippingAddress().getZipCode();
```

이 한 줄은 `order`가 `Customer`를 갖고, `Customer`가 `Address`를 갖고, `Address`가 다시 `ShippingAddress`를 갖는다는 네 단계의 내부 구조를 호출자에게 그대로 노출한다. `Customer`의 주소 저장 방식이 바뀌면(예: `Address`와 `ShippingAddress`를 하나로 합치는 리팩토링) 이 코드를 사용하는 모든 곳이 함께 깨진다. 디미터 법칙에 따라 `Order`가 필요한 동작을 직접 제공하도록 고친다.

```java
// 리팩토링 결과: order 자신에게 필요한 동작을 직접 요청한다
public class Order {
    public String getShippingZipCode() {
        return customer.getAddress().getShippingAddress().getZipCode();
    }
}

// 호출부는 내부 구조를 몰라도 된다
String zipCode = order.getShippingZipCode();
```

`getShippingZipCode()` 내부에서는 여전히 여러 단계를 거치지만, 이는 `Order` 클래스 하나의 책임 안에 갇혀 있다. `Customer`나 `Address`의 내부 구조가 바뀌어도, 그 변경은 `Order` 클래스 안에서만 수정하면 되고 외부 호출자는 영향을 받지 않는다.

## 판단 기준: 리팩토링이 실제로 결합도를 낮췄는지 검증하기

리팩토링 후에는 "배송지 저장 방식이 바뀐다면 몇 개의 파일을 고쳐야 하는가"라는 질문으로 결과를 검증한다. 리팩토링 전에는 `order.getCustomer().getAddress()...` 패턴이 코드베이스 여러 곳에 흩어져 있었다면, 그 모든 위치를 찾아 고쳐야 한다. 리팩토링 후에는 `Order.getShippingZipCode()` 내부 한 곳만 고치면 된다. 이 질문에 "한 곳만 고치면 된다"고 답할 수 있어야 디미터 법칙 적용이 실질적인 효과를 낸 것이다. 단순히 문법적으로 메서드 호출을 한 단계 감쌌다고 해서 항상 결합도가 낮아지는 것은 아니라는 점에 주의한다 — 만약 `getShippingZipCode()`가 여전히 `Customer`, `Address`의 구체적인 타입을 매개변수로 노출한다면, 겉보기만 정리됐을 뿐 실질적인 결합도는 그대로일 수 있다.

## 다음 장에서는

[13장: 오류 코드 대신 예외를 써라](/post/clean-code/error-handling-exceptions-best-practices/)에서는 자료구조와 객체를 넘어, 실패를 다루는 방식을 살펴본다.

## 평가 기준

- [ ] 타입 코드 분기를 다형성 클래스 계층으로 변환할 수 있다.
- [ ] 기차 충돌 코드를 식별하고 디미터 법칙에 따라 캡슐화할 수 있다.
- [ ] 리팩토링이 실제로 결합도를 낮췄는지 "변경 시나리오"로 검증할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 6장.
- Lieberherr, K., & Holland, I. (1989). "Assuring Good Style for Object-Oriented Programs." *IEEE Software*, 6(5), 38–48.
