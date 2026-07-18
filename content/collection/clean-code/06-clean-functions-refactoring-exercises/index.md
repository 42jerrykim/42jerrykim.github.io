---
draft: false
collection_order: 6
slug: clean-functions-refactoring-exercises
title: "[Clean Code] 06. 함수 리팩토링 실습"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "80줄짜리 긴 주문 처리 함수를 파싱·검증·계산·저장 네 단계로 분해하는 실습을 통해 05장의 함수 설계 원칙을 직접 적용하고, 분해 전후의 테스트 용이성 차이와 분해를 어디서 멈춰야 하는지 판단 기준을 함께 살펴본다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Refactoring(리팩토링)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Testing(테스트)
- Java
- Debugging(디버깅)
- Implementation(구현)
- Modularity
- Pitfalls(함정)
- Error-Handling(에러처리)
- Coupling(결합도)
- Cohesion(응집도)
- Code-Review(코드리뷰)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- OOP(객체지향)
- Design-Pattern(디자인패턴)
- SOLID
- Abstraction(추상화)
- TDD(Test-Driven Development)
---

## 이 장을 읽기 전에

이 장은 [05장: 함수는 작게, 한 가지만](/post/clean-code/clean-functions-single-responsibility-principle/)에서 다룬 원칙(작은 함수, 추상화 수준 통일, 인수 최소화)을 실제 코드에 적용하는 실습이다. 05장을 먼저 읽었다는 전제로 진행하며, 클래스 수준의 책임 분리는 [18~19장](/post/clean-code/clean-classes-solid-principles-oop/)에서 다룬다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 실습 1 전체 | 긴 함수를 단계별로 나누는 절차를 따라 하며 익힌다 |
| 실무자 | 실습 2, "판단 기준" | 분해된 함수 각각을 어떻게 독립적으로 테스트할지 설계한다 |

## 실습 1: 긴 함수 분해

아래 함수는 문자열로 들어온 주문 데이터를 파싱하고, 재고를 확인하고, 할인과 세금을 계산하고, 재고를 차감하는 일을 모두 한 함수 안에서 처리한다.

```java
// 실습 대상: 파싱, 검증, 계산, 재고 차감이 뒤섞인 함수
public String processOrder(String orderData) {
    String[] parts = orderData.split(",");
    String customerId = parts[0];
    String productId = parts[1];
    int quantity = Integer.parseInt(parts[2]);

    if (customerId == null || customerId.trim().isEmpty()) {
        return "Error: Invalid customer ID";
    }

    int availableStock = getStock(productId);
    if (availableStock < quantity) {
        return "Error: Insufficient stock";
    }

    double unitPrice = getProductPrice(productId);
    double totalPrice = unitPrice * quantity;
    double taxAmount = totalPrice * 0.1;
    double finalPrice = totalPrice + taxAmount;

    updateStock(productId, quantity);
    String orderId = generateOrderId();
    saveOrder(orderId, customerId, productId, quantity, finalPrice);

    return "Order processed. ID: " + orderId + ", Total: $" + String.format("%.2f", finalPrice);
}
```

이 함수를 분해하기 전에, 먼저 이 함수 안에 몇 개의 "TO 문단"이 숨어 있는지 세어본다. "주문 데이터를 파싱하려면", "재고를 검증하려면", "최종 가격을 계산하려면", "주문을 저장하려면" — 최소 네 개의 서로 다른 문단이 한 함수에 뭉쳐 있다는 것이 드러난다. 이 네 문단이 바로 분해의 단위가 된다.

```java
// 리팩토링 결과: 흐름만 남기고 세부는 하위 함수로 위임
public String processOrder(String orderData) {
    try {
        OrderRequest request = parseOrderData(orderData);
        validateOrder(request);
        double finalPrice = calculateFinalPrice(request);
        String orderId = saveOrder(request, finalPrice);
        return formatSuccessMessage(orderId, finalPrice);
    } catch (OrderProcessingException e) {
        return "Error: " + e.getMessage();
    }
}

private OrderRequest parseOrderData(String orderData) {
    String[] parts = orderData.split(",");
    return new OrderRequest(parts[0], parts[1], Integer.parseInt(parts[2]));
}

private void validateOrder(OrderRequest request) {
    if (request.getCustomerId() == null || request.getCustomerId().isEmpty()) {
        throw new OrderProcessingException("Invalid customer ID");
    }
    if (getStock(request.getProductId()) < request.getQuantity()) {
        throw new OrderProcessingException("Insufficient stock");
    }
}

private double calculateFinalPrice(OrderRequest request) {
    double totalPrice = getProductPrice(request.getProductId()) * request.getQuantity();
    return totalPrice * 1.1; // 세금 10% 포함
}
```

`processOrder`만 읽으면 "파싱하고, 검증하고, 계산하고, 저장하고, 메시지를 만든다"는 다섯 단계가 그대로 눈에 들어온다. 이는 05장에서 다룬 "TO 문단"을 그대로 코드로 옮긴 것과 같다.

## 실습 2: 분해가 테스트 용이성에 미치는 영향

분해되기 전 `processOrder`를 테스트하려면 문자열 파싱, 재고 조회, 가격 계산, 저장 로직을 모두 포함하는 통합 시나리오를 준비해야 했다. 분해된 이후에는 `calculateFinalPrice`만 따로 호출해 "수량 3개, 단가 1000원일 때 세금 포함 최종가가 3300원인가"를 독립적으로 검증할 수 있다. 이는 함수를 작게 만드는 것이 단순히 미관의 문제가 아니라, 각 단계를 독립적으로 검증 가능하게 만드는 실질적 이점이라는 것을 보여준다. 테스트 코드 자체를 깨끗하게 유지하는 원칙은 [16장](/post/clean-code/unit-testing-tdd-test-driven-development/)에서 별도로 다룬다.

아래 체크리스트로 분해 결과를 점검할 수 있다. 각 함수가 하나의 문단으로 설명되는가, 함수 하나를 이해하기 위해 다른 함수 두 개 이상을 동시에 열어봐야 하는가, 새로운 할인 정책이 추가된다면 몇 개의 함수를 고쳐야 하는가 — 마지막 질문에 "하나만 고치면 된다(`calculateFinalPrice`)"고 답할 수 있다면 분해가 책임을 제대로 나눈 것이다.

## 판단 기준: 언제 분해를 멈춰야 하는가

`parseOrderData`를 다시 "고객 ID 파싱"과 "상품 ID·수량 파싱"으로 더 쪼갤 수도 있다. 하지만 이 지점에서는 멈추는 것이 합리적이다 — 이유는 이 세 값이 개념적으로 "주문 데이터 파싱"이라는 하나의 단위를 이루고, 더 쪼개도 별도로 재사용되거나 독립적으로 테스트할 필요가 없기 때문이다. 05장에서 다룬 판단 기준을 그대로 적용하면, "이 함수를 호출하는 다른 맥락이 존재하는가", "이 하위 단계를 독립적으로 검증할 필요가 있는가"에 "아니오"로 답할 수 있다면 그 지점이 적절한 분해의 끝이다.

## 다음 장에서는

[07장: 주석은 실패를 의미한다](/post/clean-code/code-comments-documentation-best-practices/)에서는 코드가 스스로 의도를 표현하지 못할 때 우리가 흔히 의존하는 주석의 함정을 다룬다.

## 평가 기준

- [ ] 긴 함수에서 "TO 문단" 단위를 식별해 분해 지점을 찾을 수 있다.
- [ ] 분해된 함수 각각을 독립적으로 테스트할 수 있음을 코드로 보일 수 있다.
- [ ] 분해를 어느 지점에서 멈춰야 하는지 재사용성·테스트 필요성 기준으로 판단할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 3장.
- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.). Addison-Wesley. "Extract Function".
