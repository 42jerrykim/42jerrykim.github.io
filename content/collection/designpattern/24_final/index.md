---
collection_order: 24
title: "[Design Pattern] 디자인 패턴 총정리 및 실전 적용"
description: "디자인 패턴의 개념과 등장 배경, 객체지향 설계 원리를 정리합니다. 실무에서 패턴을 적용하는 이유와 역사, 실제 소프트웨어 개발에서 패턴의 역할을 다룹니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - GoF
  - Gang of Four
  - Software Design
  - 소프트웨어 설계
  - Creational Pattern
  - 생성 패턴
  - Structural Pattern
  - 구조 패턴
  - Behavioral Pattern
  - 행위 패턴
  - Object Oriented
  - 객체지향
  - OOP
  - 객체지향 프로그래밍
  - SOLID
  - Clean Code
  - 클린 코드
  - Refactoring
  - 리팩토링
  - Best Practices
  - 모범 사례
  - Code Quality
  - 코드 품질
  - Maintainability
  - 유지보수성
  - Extensibility
  - 확장성
  - Code Reusability
  - 코드 재사용성
  - Software Architecture
  - 소프트웨어 아키텍처
  - Software Engineering
  - 소프트웨어 공학
  - Programming
  - 프로그래밍
  - Development
  - 개발
  - Java
  - C++
  - Python
  - C#
  - Pattern Summary
  - 패턴 요약
  - Pattern Selection
  - 패턴 선택
  - Anti Pattern
  - 안티 패턴
---

이 글에서는 지금까지 학습한 GoF의 23가지 디자인 패턴을 총정리하고, 각 패턴을 언제 어떻게 선택해야 하는지, 그리고 실무에서 패턴을 효과적으로 적용하는 방법을 다룬다.

## 디자인 패턴의 가치

한때 소프트웨어 개발에서 모든 논의의 핵심은 디자인 패턴(Design Pattern)이었다. 개발자들은 밤을 세워가며 객체(Object), 응집도(Cohesion), 결합도(Coupling)에 대해 진지한 토론을 벌이기도 했다. 객체지향(Object-oriented)을 공부하는 개발자라면 반드시 넘어야 할 산이 디자인 패턴이었다.

최근에는 프레임워크와 라이브러리가 많은 패턴을 내재화하여, 직접 패턴을 구현할 기회가 줄었다. 하지만 패턴을 이해하는 것은 여전히 중요하다. 왜냐하면:

- **코드 이해력 향상**: 프레임워크 내부 구조를 이해할 수 있다
- **설계 역량 강화**: 확장 가능하고 유지보수하기 쉬운 코드를 작성할 수 있다
- **커뮤니케이션 효율화**: 팀원들과 공통 어휘로 소통할 수 있다
- **문제 해결 도구**: 반복되는 설계 문제에 검증된 해결책을 적용할 수 있다

## GoF 23가지 패턴 요약

### 생성 패턴 (Creational Patterns)

객체 생성 메커니즘을 다루며, 상황에 적합한 방식으로 객체를 생성한다.

| 패턴 | 목적 | 사용 시기 |
|------|------|----------|
| **Abstract Factory** | 관련 객체 군을 생성 | 제품군을 일관되게 생성해야 할 때 |
| **Builder** | 복잡한 객체를 단계별로 생성 | 생성자 매개변수가 많을 때 |
| **Factory Method** | 서브클래스가 생성할 객체 결정 | 객체 생성을 서브클래스에 위임할 때 |
| **Prototype** | 기존 객체를 복제하여 생성 | 복잡한 객체를 복제해야 할 때 |
| **Singleton** | 인스턴스가 하나만 존재하도록 보장 | 전역 접근점이 필요할 때 |

### 구조 패턴 (Structural Patterns)

클래스와 객체를 조합하여 더 큰 구조를 만든다.

| 패턴 | 목적 | 사용 시기 |
|------|------|----------|
| **Adapter** | 호환되지 않는 인터페이스를 변환 | 레거시 코드나 서드파티 통합 시 |
| **Bridge** | 추상화와 구현을 분리 | 두 차원으로 확장이 필요할 때 |
| **Composite** | 트리 구조로 부분-전체 계층 표현 | 개별/복합 객체를 동일하게 다룰 때 |
| **Decorator** | 동적으로 기능 추가 | 상속 없이 기능을 확장할 때 |
| **Facade** | 복잡한 서브시스템에 단순한 인터페이스 제공 | 복잡성을 숨기고 싶을 때 |
| **Flyweight** | 공유를 통해 대량의 객체를 효율적으로 관리 | 유사한 객체가 많을 때 |
| **Proxy** | 다른 객체에 대한 접근을 제어 | 지연 로딩, 접근 제어, 캐싱 시 |

### 행위 패턴 (Behavioral Patterns)

객체 간의 책임 분배와 알고리즘을 다룬다.

| 패턴 | 목적 | 사용 시기 |
|------|------|----------|
| **Chain of Responsibility** | 요청을 처리할 핸들러 체인 | 미들웨어, 필터 구현 시 |
| **Command** | 요청을 객체로 캡슐화 | Undo/Redo, 큐잉 필요 시 |
| **Interpreter** | 문법 규칙을 클래스로 표현 | DSL, 간단한 언어 해석 시 |
| **Iterator** | 컬렉션 요소를 순차 접근 | 다양한 컬렉션 순회 시 |
| **Mediator** | 객체 간 상호작용을 캡슐화 | 복잡한 객체 관계 단순화 시 |
| **Memento** | 객체 상태를 저장하고 복원 | 스냅샷, 롤백 기능 구현 시 |
| **Observer** | 상태 변화를 관찰자에게 통지 | 이벤트 시스템, 데이터 바인딩 시 |
| **State** | 상태에 따라 행동 변경 | 상태 기계 구현 시 |
| **Strategy** | 알고리즘을 캡슐화하여 교체 가능하게 | 알고리즘을 동적으로 선택할 때 |
| **Template Method** | 알고리즘 골격 정의, 일부 단계 서브클래스에 위임 | 공통 알고리즘 구조 공유 시 |
| **Visitor** | 객체 구조에 새 연산 추가 | 연산이 자주 추가되는 경우 |

## 패턴 선택 가이드

### 문제 유형별 패턴 선택

```
생성 문제
├── 복잡한 객체 생성? → Builder
├── 객체 군 생성? → Abstract Factory
├── 런타임에 타입 결정? → Factory Method
├── 객체 복제 필요? → Prototype
└── 단일 인스턴스? → Singleton

구조 문제
├── 인터페이스 불일치? → Adapter
├── 추상화/구현 분리? → Bridge
├── 트리 구조? → Composite
├── 동적 기능 추가? → Decorator
├── 복잡성 숨김? → Facade
├── 대량의 유사 객체? → Flyweight
└── 접근 제어/지연 로딩? → Proxy

행위 문제
├── 요청 처리 체인? → Chain of Responsibility
├── Undo/Redo? → Command + Memento
├── 간단한 언어 해석? → Interpreter
├── 컬렉션 순회? → Iterator
├── 복잡한 객체 관계? → Mediator
├── 상태 저장/복원? → Memento
├── 상태 변화 통지? → Observer
├── 상태에 따른 행동? → State
├── 알고리즘 교체? → Strategy
├── 알고리즘 골격 공유? → Template Method
└── 새 연산 추가? → Visitor
```

### 유사 패턴 비교

**Strategy vs State**
- Strategy: 클라이언트가 전략 선택, 알고리즘 교체에 초점
- State: 내부에서 상태 전이, 상태에 따른 행동 변화에 초점

**Decorator vs Proxy**
- Decorator: 기능 추가, 여러 겹 래핑 가능
- Proxy: 접근 제어, 단일 래핑

**Facade vs Adapter**
- Facade: 복잡성 숨김, 새 인터페이스 제공
- Adapter: 인터페이스 변환, 호환성 제공

**Factory Method vs Abstract Factory**
- Factory Method: 하나의 제품 생성
- Abstract Factory: 관련된 제품 군 생성

## 패턴 적용 시 주의사항

### 안티패턴 피하기

1. **과도한 패턴 사용 (Pattern Overuse)**
   - 단순한 문제에 복잡한 패턴 적용은 오히려 해로움
   - "망치를 들면 모든 것이 못으로 보인다" 경계

2. **패턴 강제 적용 (Pattern Force-fitting)**
   - 문제에 맞는 패턴을 선택해야 함
   - 패턴을 위한 패턴 적용 금지

3. **패턴 맹목적 추종 (Pattern Cargo Cult)**
   - 패턴의 의도와 맥락을 이해해야 함
   - 코드 복사-붙여넣기 지양

### 효과적인 패턴 적용

1. **YAGNI 원칙**: 실제로 필요할 때 적용
2. **점진적 적용**: 리팩토링을 통해 점진적으로 도입
3. **팀 합의**: 팀원들이 패턴을 이해하고 있는지 확인
4. **문서화**: 왜 해당 패턴을 선택했는지 기록

## 현대 개발에서의 패턴

### 프레임워크에 내장된 패턴

- **Spring**: DI(Factory), AOP(Proxy, Decorator), MVC(Observer, Strategy)
- **React**: 컴포넌트(Composite), Hooks(Strategy), Context(Observer)
- **Django**: MTV(MVC 변형), ORM(Active Record, Data Mapper)

### 함수형 프로그래밍과 패턴

많은 GoF 패턴이 함수형 프로그래밍에서 간단히 구현됨:
- **Strategy**: 고차 함수로 대체
- **Command**: 함수를 값으로 전달
- **Iterator**: 제너레이터, 스트림

### 마이크로서비스 아키텍처

새로운 패턴의 등장:
- API Gateway (Facade의 분산 버전)
- Service Mesh (Proxy의 확장)
- Event Sourcing (Command + Memento)
- CQRS (Command와 Query 분리)

## 결론

디자인 패턴은 소프트웨어 설계의 도구 상자다. 모든 도구를 한 번에 사용할 필요는 없지만, 각 도구의 용도와 사용법을 알고 있어야 적절한 상황에서 꺼내 쓸 수 있다.

패턴을 공부할 때 가장 중요한 것은:
1. **의도(Intent)** 이해: 왜 이 패턴이 필요한가?
2. **적용 상황(Applicability)** 파악: 언제 사용해야 하는가?
3. **결과(Consequences)** 인식: 어떤 트레이드오프가 있는가?

패턴은 목적이 아니라 수단이다. 좋은 코드를 작성하기 위해 패턴을 활용하되, 패턴 자체가 목표가 되지 않도록 주의하자.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- Refactoring Guru (https://refactoring.guru)
- Martin Fowler의 Patterns of Enterprise Application Architecture

