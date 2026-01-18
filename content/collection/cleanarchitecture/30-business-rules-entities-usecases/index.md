---
collection_order: 300
image: "wordcloud.png"
description: "업무 규칙의 두 가지 유형인 엔터티와 유스케이스를 다룹니다. 핵심 업무 규칙과 애플리케이션 특화 규칙의 차이, 그리고 요청/응답 모델의 설계 방법을 설명합니다."
title: "[Clean Architecture] 30. 업무 규칙: 엔티티와 유스케이스"
date: 2026-01-18
categories: CleanArchitecture
tags: [Clean Architecture, 클린 아키텍처, Business Rules, 비즈니스 규칙, Entity, 엔터티, Use Case, 유스케이스, Critical Business Rules, 핵심 업무 규칙, Application Business Rules, 애플리케이션 업무 규칙, Domain, 도메인, Request Model, 요청 모델, Response Model, 응답 모델, DTO, Data Transfer Object, Input Port, 입력 포트, Output Port, 출력 포트, Interactor, 인터랙터, Enterprise, 기업, Application, 애플리케이션, Software Architecture, 소프트웨어 아키텍처, Domain Model, 도메인 모델, Data, 데이터, Behavior, 행동, Loan, 대출, Interest, 이자, Customer, 고객, Object Oriented, 객체 지향, Independence, 독립성]
---

업무 규칙은 시스템에서 가장 **핵심적인 부분**이다. 마틴은 업무 규칙을 두 가지로 구분한다: **엔터티**(핵심 업무 규칙)와 **유스케이스**(애플리케이션 업무 규칙).

## 핵심 업무 규칙 (Critical Business Rules)

컴퓨터가 없어도 **존재하는** 규칙이다.

### 예시: 대출

- 대출에는 이자가 붙는다
- 이자는 원금, 이율, 기간으로 계산된다
- 이 규칙은 **컴퓨터 이전에도 존재**했다

### 핵심 업무 데이터 (Critical Business Data)

규칙이 필요로 하는 데이터:
- 원금 (Principal)
- 이율 (Interest Rate)
- 기간 (Term)

## 엔터티 (Entity)

핵심 업무 규칙 + 핵심 업무 데이터 = **엔터티**

```java
public class Loan {
    private Money principal;
    private double interestRate;
    private int termInMonths;
    
    // 핵심 업무 규칙
    public Money calculateInterest() {
        return principal.multiply(interestRate)
                       .multiply(termInMonths / 12.0);
    }
    
    public Money calculateMonthlyPayment() {
        // 핵심 업무 규칙
    }
}
```

특성:
- **순수한 비즈니스 개념**
- UI, DB, 프레임워크와 **무관**
- **가장 변하지 않는** 부분

## 유스케이스 (Use Case)

**애플리케이션 특화** 업무 규칙이다.

```java
public class ApplyForLoanUseCase {
    private final CustomerRepository customers;
    private final LoanRepository loans;
    private final CreditService creditService;
    
    public ApplyForLoanResponse execute(ApplyForLoanRequest request) {
        // 1. 고객 조회
        Customer customer = customers.findById(request.getCustomerId());
        
        // 2. 신용 확인 (애플리케이션 규칙)
        CreditScore score = creditService.check(customer);
        if (score.isBelowMinimum()) {
            return ApplyForLoanResponse.rejected("신용 부족");
        }
        
        // 3. 대출 생성 (엔터티 사용)
        Loan loan = new Loan(
            request.getPrincipal(),
            determineRate(score),
            request.getTerm()
        );
        
        // 4. 저장
        loans.save(loan);
        
        return ApplyForLoanResponse.approved(loan.getId());
    }
}
```

### 요청/응답 모델

유스케이스의 **입력과 출력**은 단순한 데이터 구조:

```java
// 요청 모델
public class ApplyForLoanRequest {
    private String customerId;
    private Money principal;
    private int term;
}

// 응답 모델
public class ApplyForLoanResponse {
    private String status;
    private String loanId;
    private String message;
}
```

**주의**: 엔터티를 요청/응답에 직접 사용하지 마라!

## 엔터티 vs 유스케이스

| 항목 | 엔터티 | 유스케이스 |
|------|--------|-----------|
| 범위 | 기업 전체 | 특정 애플리케이션 |
| 변경 이유 | 비즈니스 규칙 변경 | 애플리케이션 요구 변경 |
| 의존성 | 없음 | 엔터티에 의존 |
| 예시 | Loan.calculateInterest() | ApplyForLoan |

## 핵심

> "엔터티는 기업의 핵심이다. 유스케이스는 엔터티를 사용하여 애플리케이션의 목적을 달성한다."
