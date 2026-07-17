---
draft: true
collection_order: 17
slug: unit-testing-tdd-exercises
title: "[Clean Code] 17장. 단위 테스트 리팩토링 실습"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "간단한 계산기를 Red-Green-Refactor 사이클로 직접 구현하고, 실제 DB에 의존하는 F.I.R.S.T 원칙 위반 테스트 코드를 정리하며 16장에서 배운 테스트 설계 원칙을 실제 코드로 손에 익히는 실습이다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- TDD(Test-Driven Development)
- Testing(테스트)
- Refactoring(리팩토링)
- Code-Quality(코드품질)
- Best-Practices
- Maintainability
- Java
- Debugging(디버깅)
- Implementation(구현)
- Pitfalls(함정)
- Edge-Cases(엣지케이스)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Code-Review(코드리뷰)
- Readability
- Design-Pattern(디자인패턴)
- Error-Handling(에러처리)
- CI-CD(Continuous Integration/Continuous Deployment)
- Productivity(생산성)
- Interface(인터페이스)
- Dependency-Injection(의존성주입)
- Database(데이터베이스)
---

## 이 장을 읽기 전에

이 장은 [16장: TDD 법칙과 F.I.R.S.T 원칙](/post/clean-code/unit-testing-tdd-test-driven-development/)에서 다룬 Red-Green-Refactor 사이클과 F.I.R.S.T 원칙을 직접 적용하는 실습이다. 16장을 먼저 읽었다는 전제로 진행한다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 실습 1 전체 | Red-Green-Refactor 사이클을 처음부터 끝까지 직접 따라간다 |
| 실무자 | 실습 2, "판단 기준" | F.I.R.S.T 위반 테스트를 식별하고 원인별로 고치는 방법을 익힌다 |

## 실습 1: TDD로 계산기 구현하기

간단한 계산기의 덧셈 기능을 TDD로 구현하는 과정을 처음부터 따라가 본다. 첫 단계는 아직 존재하지 않는 `Calculator` 클래스를 사용하는 실패하는 테스트를 작성하는 것이다.

```java
// Red: Calculator 클래스가 아직 없으므로 컴파일조차 되지 않는다
@Test
void addsTwoNumbers() {
    Calculator calculator = new Calculator();
    assertEquals(5, calculator.add(2, 3));
}
```

이 테스트를 컴파일되게 만드는 최소한의 코드만 작성한다. TDD의 두 번째 법칙("컴파일은 성공하되 실행이 실패하는 정도로만 작성")에 따라, 아직 로직을 채우지 않는다.

```java
// Green으로 가는 중간 단계: 컴파일은 되지만 항상 실패하는 최소 구현
class Calculator {
    int add(int a, int b) { return 0; }
}
```

이제 테스트를 실제로 통과시키는 최소한의 로직을 채운다.

```java
// Green: 테스트를 통과시키는 실제 구현
class Calculator {
    int add(int a, int b) { return a + b; }
}
```

이 상태에서 뺄셈 기능을 추가하려면, 다시 실패하는 테스트를 먼저 작성하는 것으로 사이클을 반복한다.

```java
@Test
void subtractsTwoNumbers() {
    Calculator calculator = new Calculator();
    assertEquals(1, calculator.subtract(3, 2));
}
```

이 사이클을 나눗셈까지 반복하면, 자연스럽게 "0으로 나누면 어떻게 되는가"라는 경계 조건도 테스트로 먼저 다루게 된다.

```java
@Test
void divisionByZeroThrowsException() {
    Calculator calculator = new Calculator();
    assertThrows(ArithmeticException.class, () -> calculator.divide(10, 0));
}
```

경계 조건을 테스트로 먼저 명시하면, 구현 단계에서 이 경우를 빠뜨릴 가능성이 줄어든다. 이는 TDD가 커버리지 수치보다 "설계 시점에 경계 조건을 미리 생각하게 만든다"는 부수 효과를 실제로 보여주는 사례다.

## 실습 2: F.I.R.S.T 위반 테스트 정리

아래 테스트는 실제 데이터베이스에 연결하고, 이전 테스트가 만든 데이터에 의존한다.

```java
// 실습 대상: F.I.R.S.T 원칙을 위반하는 테스트
@Test
void test1_createUser() {
    Connection conn = DriverManager.getConnection("jdbc:mysql://prod-db/test");
    Statement stmt = conn.createStatement();
    stmt.execute("INSERT INTO users (name) VALUES ('test-user')");
}

@Test
void test2_findUser() {
    // test1이 먼저 실행되어 'test-user'가 존재한다고 가정한다
    Connection conn = DriverManager.getConnection("jdbc:mysql://prod-db/test");
    ResultSet rs = conn.createStatement().executeQuery(
        "SELECT * FROM users WHERE name = 'test-user'");
    assertTrue(rs.next());
}
```

이 두 테스트는 최소 세 가지 F.I.R.S.T 위반을 동시에 보인다. 실제 데이터베이스에 연결하므로 **Fast**를 위반해 실행이 느리고, `test2`가 `test1`의 실행 순서와 부수 효과에 의존하므로 **Independent**를 위반하며, 실제 프로덕션 DB 상태에 따라 결과가 달라질 수 있어 **Repeatable**도 위반한다. 인메모리 테스트 더블로 교체하면 세 문제가 동시에 해소된다.

```java
// 리팩토링 결과: 인메모리 저장소로 대체해 독립적이고 빠르며 반복 가능하게 만든다
@Test
void createdUserCanBeFound() {
    InMemoryUserRepository repository = new InMemoryUserRepository();
    UserService service = new UserService(repository);

    service.createUser("test-user");

    assertTrue(repository.findByName("test-user").isPresent());
}
```

이제 이 테스트는 다른 테스트의 실행 여부나 순서와 무관하게, 어떤 환경에서 몇 번을 실행해도 동일한 결과를 낸다. 실제 데이터베이스와의 통합이 정말로 검증돼야 한다면, 이런 검증은 별도의 통합 테스트 계층으로 분리하고 단위 테스트와는 실행 빈도·속도 기준을 다르게 가져가는 것이 실무에서 흔한 절충안이다.

## 판단 기준: 테스트가 F.I.R.S.T를 위반하는지 빠르게 진단하기

새 테스트를 작성한 뒤 "이 테스트를 실행 순서를 바꿔도, 다른 테스트와 함께 병렬로 실행해도, 네트워크가 끊긴 환경에서도 같은 결과가 나오는가"를 자문한다. 하나라도 "아니오"라면 그 테스트는 외부 상태나 다른 테스트에 암묵적으로 의존하고 있다는 신호이며, 테스트 더블(스텁, 페이크)로 그 의존성을 대체할 필요가 있다.

## 다음 장에서는

[18장: 클래스는 작아야 한다](/post/clean-code/clean-classes-solid-principles-oop/)에서는 함수와 테스트를 넘어 클래스 전체의 설계 원칙(SRP, SOLID)을 다룬다.

## 평가 기준

- [ ] Red-Green-Refactor 사이클을 실제 기능 구현에 처음부터 끝까지 적용할 수 있다.
- [ ] 경계 조건(0으로 나누기 등)을 구현 전에 테스트로 먼저 명시할 수 있다.
- [ ] F.I.R.S.T 원칙을 위반하는 테스트를 진단하고 테스트 더블로 리팩토링할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 9장.
- Beck, K. (2002). *Test-Driven Development: By Example*. Addison-Wesley.
