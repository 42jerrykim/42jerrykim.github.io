---
draft: true
collection_order: 13
slug: error-handling-exceptions-best-practices
title: "[Clean Code] 13장. 오류 코드 대신 예외를 써라"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "오류 코드가 호출자 코드를 어떻게 오염시키는지 보이고, 예외에 의미 있는 컨텍스트를 담는 방법과 null 반환·전달을 피하는 기법을 다룬다. Optional·Result 타입 같은 현대적 오류 처리도 함께 비교한다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Error-Handling(에러처리)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Java
- Python
- Kotlin
- Debugging(디버깅)
- Refactoring(리팩토링)
- Type-Safety
- Implementation(구현)
- Pitfalls(함정)
- Edge-Cases(엣지케이스)
- Testing(테스트)
- Design-Pattern(디자인패턴)
- Interface(인터페이스)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Code-Review(코드리뷰)
- System-Design
- Software-Architecture(소프트웨어아키텍처)
---

## 이 장을 읽기 전에

이 장은 [05장](/post/clean-code/clean-functions-single-responsibility-principle/)에서 다룬 "명령과 조회 분리", "오류 코드보다 예외" 원칙을 확장한다. 예외를 던지고 잡는(`try`/`catch`) 기본 문법 경험이 필요하다. 외부 라이브러리 예외를 감싸는 방법은 [15장](/post/clean-code/api-boundaries-third-party-integration/)에서 더 다룬다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "오류 코드보다 예외"부터 "예외에 의미 제공"까지 | 오류 코드 대신 예외를 쓰는 구체적 이유를 이해한다 |
| 실무자 | "판단 기준", "비판적 시각" | checked/unchecked 예외, Optional/Result 타입 중 팀 상황에 맞는 전략을 선택한다 |

## 오류 코드가 호출자 코드를 오염시키는 이유

오류를 코드(정수, 열거형 반환값)로 표현하면, 호출자는 함수를 호출한 직후 그 값을 즉시 확인해야 한다. 이 확인을 잊어버리기 쉽고, 여러 오류 코드를 연쇄적으로 확인하다 보면 코드가 깊이 중첩된 **화살촉 구조(arrow code)**가 만들어진다.

```java
// 오류 코드: 호출자가 매번 확인해야 하고, 확인 로직이 중첩된다
if (deletePage(page) == E_OK) {
    if (registry.deleteReference(page.name) == E_OK) {
        if (configKeys.deleteKey(page.name.makeKey()) == E_OK) {
            logger.log("page deleted");
        } else {
            logger.log("configKey not deleted");
        }
    } else {
        logger.log("deleteReference from registry failed");
    }
} else {
    logger.log("delete failed");
}

// 예외: 정상 흐름과 오류 처리가 분리된다
try {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
} catch (Exception e) {
    logger.log(e.getMessage());
}
```

예외를 사용한 버전은 "정상적으로 세 단계를 순서대로 수행한다"는 흐름이 중첩 없이 그대로 드러나고, 오류 처리는 `catch` 블록 하나로 모인다. 이는 05장에서 다룬 "오류 처리도 한 가지 작업이므로 별도 함수로 분리해야 한다"는 원칙과 직결된다.

## Try-Catch-Finally를 먼저 작성하라

예외가 발생할 수 있는 코드를 작성할 때는, 로직을 먼저 채우고 나중에 예외 처리를 끼워 넣기보다 `try` 블록의 범위와 `catch`가 남길 상태를 먼저 정의하는 편이 안전하다. `try` 블록은 트랜잭션과 비슷하다 — `try` 블록 안에서 무엇이 실행되든, `catch` 블록을 나오는 순간 프로그램 상태는 일관성이 있어야 한다. 이 원칙에 따르면, 예외가 발생할 코드를 작성하기 전에 먼저 "이 작업이 실패하면 어떤 예외가 발생하는가"를 검증하는 테스트를 작성하고, 그 예외를 잡는 `try`/`catch` 뼈대를 만든 다음 실제 로직을 채워 넣는 순서가 실수를 줄인다.

## 예외에 의미 있는 컨텍스트를 담아라

예외를 던질 때 스택 트레이스만으로는 "어떤 작업이, 어떤 입력값으로, 왜 실패했는지"를 알기 어렵다. 예외 메시지에는 실패한 연산과 실패 유형을 명시하는 정보를 충분히 담아야 한다.

```java
// 부족한 컨텍스트: 어떤 계좌에서, 왜 실패했는지 알 수 없다
throw new InsufficientFundsException();

// 충분한 컨텍스트: 원인 진단에 필요한 정보가 담겨 있다
throw new InsufficientFundsException(
    String.format("계좌 %s의 잔액이 부족합니다. 요청 금액: %s, 현재 잔액: %s",
        accountId, requestedAmount, currentBalance));
```

또한 예외 클래스는 호출자가 실제로 신경 쓰는 방식으로 분류해야 한다. 외부 라이브러리가 던지는 예외 타입이 제각각이라면, 이를 하나의 예외 타입으로 감싸는 **어댑터**를 만들어 호출자가 하나의 `catch` 블록으로 처리할 수 있게 하는 편이 낫다. 이 패턴은 [15장](/post/clean-code/api-boundaries-third-party-integration/)에서 외부 라이브러리 경계를 다룰 때 더 자세히 살펴본다.

## null을 반환하지도, 전달하지도 마라

`null`을 반환하는 함수는 호출자에게 "이 값이 없을 수도 있다"는 책임을 암묵적으로 떠넘긴다. 호출자가 `null` 확인을 빠뜨리면 `NullPointerException`이 코드베이스 어디서든 터질 수 있고, 그 원인을 역추적하기 어렵다.

```java
// Bad: null을 반환해 호출자가 확인을 빠뜨릴 여지를 남긴다
public Employee getEmployee(String id) {
    Employee employee = repository.find(id);
    return employee; // 찾지 못하면 null
}

// Good: Optional로 "값이 없을 수 있다"는 사실을 타입 시스템에 드러낸다
public Optional<Employee> getEmployee(String id) {
    return repository.find(id);
}
```

`Optional<Employee>`를 반환하면, 호출자는 컴파일러의 도움을 받아 "값이 없을 수 있다"는 사실을 무시할 수 없다. `orElseThrow()`, `orElse(defaultValue)`, `map()` 같은 메서드로 명시적으로 처리 경로를 선택해야 한다. 마찬가지로 함수에 `null`을 인수로 전달하는 것도 피해야 한다 — 함수 내부에서 `null` 검사를 빠뜨리면 실행 중 예외가 발생하고, 검사를 추가하면 모든 호출부에 방어 코드가 늘어난다.

## 흔한 오개념

**"예외는 항상 checked(확인) 예외로 선언해야 안전하다"**는 오해가 있다. Java의 checked 예외는 컴파일러가 처리를 강제한다는 장점이 있지만, 호출 스택 깊숙한 곳에서 발생한 예외를 상위 함수들이 각자의 시그니처에 `throws` 절로 계속 전파해야 하는 부담을 만든다. 이는 캡슐화를 해친다 — 하위 모듈의 구현이 바뀌어 새로운 예외 타입이 추가되면, 그 예외를 전혀 신경 쓰지 않던 상위 함수의 시그니처까지 연쇄적으로 고쳐야 한다.

**"오류 처리를 예외로 통일하면 성능이 나빠진다"**는 오해도 있다. 현대 JVM·CLR 등에서 예외의 실질적 비용은 "예외를 던지는 시점"에 집중되며, 정상 흐름에서 `try` 블록에 진입하는 것 자체의 오버헤드는 미미하다. 성능이 문제가 되는 경우는 예외를 정상적인 제어 흐름(예: 반복문 종료 조건)으로 남용할 때이지, 진짜 예외적인 상황에 예외를 쓰는 것 자체가 아니다.

## 판단 기준: Checked vs Unchecked, Optional vs 예외

호출자가 그 오류를 받아 즉시 유의미하게 대응할 수 있고, 그 오류가 자주 발생할 것으로 예상되는 경우(예: 파일이 존재하지 않음, 네트워크 타임아웃)는 checked 예외나 명시적 반환 타입(Optional, Result)으로 표현해 호출자가 처리를 놓치지 않게 강제하는 편이 유리하다. 반대로 프로그래밍 오류(잘못된 인수, 널 포인터)처럼 호출자가 그 자리에서 복구할 수 없고 애초에 발생해서는 안 되는 상황은 unchecked 예외로 표현해, 모든 호출부에 불필요한 `throws` 전파를 강제하지 않는 편이 코드를 더 깔끔하게 유지한다. "값이 없을 수 있다"는 것 자체가 정상적인 결과의 일부라면(검색 결과 없음) `Optional`을, "실패 이유가 여러 가지이고 호출자가 이유별로 다르게 대응해야 한다"면 예외 또는 `Result` 타입을 선택하는 것이 실무적으로 유용한 기준이다.

## 비판적 시각

Java의 checked 예외는 오랫동안 논쟁의 대상이었다. Bruce Eckel을 비롯한 여러 개발자는 checked 예외가 대규모 코드베이스에서 예외 전파를 강제해 오히려 API 설계의 유연성을 해친다고 비판했고, 이런 비판은 이후 언어 설계에도 영향을 미쳐 C#과 Kotlin은 처음부터 checked 예외를 채택하지 않았다. 한편 Rust와 Go는 예외 자체를 던지고 잡는 매커니즘 대신, 함수의 반환 타입에 성공/실패를 명시하는 `Result<T, E>`나 다중 반환값(`value, err`) 방식을 표준으로 삼았다 — 이는 "오류 처리를 함수 시그니처에서 숨기지 않는다"는 점에서 Java의 checked 예외와 목적은 비슷하지만, 예외 전파의 암묵성 문제 없이 타입 시스템으로 강제한다는 차이가 있다. 이 흐름은 Java·Kotlin 생태계에서 `Optional`, `Either`, `Result` 같은 타입을 예외 대신 사용하려는 움직임과도 맞닿아 있으며, "예외를 쓸 것인가 명시적 반환 타입을 쓸 것인가"는 여전히 활발히 논의되는 설계 선택이다.

## 다음 장에서는

[14장: 오류 처리 리팩토링 실습](/post/clean-code/error-handling-exceptions-exercises/)에서는 오류 코드로 뒤덮인 코드를 예외 기반으로 리팩토링해 본다.

## 평가 기준

- [ ] 오류 코드 반환이 왜 화살촉 코드를 만드는지 설명하고 예외로 대체할 수 있다.
- [ ] 예외 메시지에 진단에 필요한 컨텍스트를 포함시킬 수 있다.
- [ ] null 반환/전달의 위험성을 설명하고 Optional로 대체할 수 있다.
- [ ] checked/unchecked 예외, Optional/Result 타입 중 상황에 맞는 선택을 할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 7장.
- [Oracle Java Tutorials — Exceptions](https://docs.oracle.com/javase/tutorial/essential/exceptions/index.html)
- [The Rust Programming Language — Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html)
