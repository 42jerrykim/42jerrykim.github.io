---
draft: true
collection_order: 450
image: "wordcloud.png"
description: "패키지 구조의 네 가지 접근법을 다룹니다. 계층별, 기능별, 포트와 어댑터, 컴포넌트별 패키지 구성과 각각의 장단점, 그리고 컴파일러 기반 강제 방법을 설명합니다."
title: "[Clean Architecture] 45. 빠진 장: 패키지 구조"
date: 2026-01-18
categories: CleanArchitecture
tags: [Clean Architecture, 클린 아키텍처, Package Structure, 패키지 구조, Package by Layer, 계층별 패키지, Package by Feature, 기능별 패키지, Ports and Adapters, 포트와 어댑터, Package by Component, 컴포넌트별 패키지, Compiler, 컴파일러, Enforcement, 강제, Access Modifier, 접근 제한자, Public, Private, Internal, Module, 모듈, Visibility, 가시성, Software Architecture, 소프트웨어 아키텍처, Java, Kotlin, C#, Namespace, 네임스페이스, Import, 임포트, Simon Brown, 사이먼 브라운, Organization, 구성, Directory, 디렉토리, Encapsulation, 캡슐화, Dependency, 의존성]
---

마틴의 책에는 **빠져 있는** 중요한 주제가 있다: **패키지 구조**. 이 장은 사이먼 브라운(Simon Brown)이 기고했다.

## 네 가지 패키지 구성법

### 1. 계층별 패키지 (Package by Layer)

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

**문제**: 기능 추가 시 여러 패키지 수정

### 2. 기능별 패키지 (Package by Feature)

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

**장점**: 기능 단위로 응집
**문제**: 계층 구분이 불명확

### 3. 포트와 어댑터 (Ports and Adapters)

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

**장점**: Clean Architecture 구현
**문제**: 복잡성 증가

### 4. 컴포넌트별 패키지

```
com.myapp.orders/
├── internal/
│   ├── OrderServiceImpl
│   └── JpaOrderRepository
└── OrderComponent (public facade)
```

**장점**: 캡슐화 강화

## 컴파일러 강제

패키지 구조만으로는 **부족**하다. 개발자가 규칙을 어길 수 있다.

### 접근 제한자 활용

```java
// Java - package-private 활용
class OrderServiceImpl { }  // default: 패키지 외부에서 접근 불가
public interface OrderService { }  // public: 외부 공개
```

### 모듈 시스템

```java
// Java 9+ 모듈
module com.myapp.orders {
    exports com.myapp.orders.api;  // 공개할 것만 export
    // internal 패키지는 숨겨짐
}
```

## 핵심

> "좋은 아키텍처는 **컴파일러가 강제**해야 한다. 패키지 구조와 접근 제한자를 활용하여 의존성 규칙을 코드 수준에서 강제하라."

---

## Clean Architecture 커리큘럼을 마치며

지금까지 소프트웨어 아키텍처의 역사부터 Clean Architecture의 모든 원칙까지 살펴보았다. 핵심은 단 하나:

> **"의존성은 안쪽으로, 세부사항에서 정책으로."**

이 원칙을 이해하고 적용하면, 유지보수하기 쉽고, 테스트하기 쉽고, 확장하기 쉬운 소프트웨어를 만들 수 있다.
