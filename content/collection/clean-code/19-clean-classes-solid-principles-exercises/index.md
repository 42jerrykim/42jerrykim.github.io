---
draft: true
collection_order: 19
slug: clean-classes-solid-principles-exercises
title: "[Clean Code] 19장. SOLID 원칙 리팩토링 실습"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "DB 연결, 검증, 이메일 발송, 캐시 관리를 모두 떠맡은 God Class UserManager를 SRP와 DIP에 따라 네 개의 협력 클래스로 분해하는 실습을 통해 18장의 SOLID 원칙을 실제 코드와 조립 지점 설계에 적용한다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- SOLID
- Refactoring(리팩토링)
- OOP(객체지향)
- Coupling(결합도)
- Cohesion(응집도)
- Code-Quality(코드품질)
- Best-Practices
- Maintainability
- Dependency-Injection(의존성주입)
- Java
- Testing(테스트)
- Implementation(구현)
- Pitfalls(함정)
- Interface(인터페이스)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Code-Review(코드리뷰)
- Readability
- Design-Pattern(디자인패턴)
- Software-Architecture(소프트웨어아키텍처)
- System-Design
- Encapsulation(캡슐화)
---

## 이 장을 읽기 전에

이 장은 [18장: 클래스는 작아야 한다](/post/clean-code/clean-classes-solid-principles-oop/)에서 다룬 SRP, 응집도, DIP를 실제 God Class에 적용하는 실습이다. 18장을 먼저 읽었다는 전제로 진행한다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 실습 1 전체 | 하나의 클래스에 뒤섞인 여러 책임을 식별하고 분리하는 절차를 익힌다 |
| 실무자 | 실습 2, "판단 기준" | 분리된 클래스들을 조립하는 지점(Composition Root)의 위치를 설계한다 |

## 실습 1: God Class 분해

아래 `UserManager`는 DB 연결 초기화, 사용자 검증, 저장, 이메일 발송, 캐시 관리라는 다섯 가지 책임을 한 클래스에 모두 담고 있다.

```java
// 실습 대상: 다섯 가지 책임이 뒤섞인 God Class
public class UserManager {
    private Connection dbConnection;
    private EmailService emailService;
    private Map<String, User> userCache = new HashMap<>();

    public UserManager() {
        this.dbConnection = DriverManager.getConnection("jdbc:mysql://localhost/userdb");
        this.emailService = new EmailService();
    }

    public boolean isValidUser(User user) {
        return user.getEmail() != null && user.getEmail().matches("^[A-Za-z0-9+_.-]+@(.+)$");
    }

    public void saveUser(User user) throws SQLException {
        String sql = "INSERT INTO users (name, email) VALUES (?, ?)";
        PreparedStatement stmt = dbConnection.prepareStatement(sql);
        stmt.setString(1, user.getName());
        stmt.setString(2, user.getEmail());
        stmt.executeUpdate();
    }

    public void sendWelcomeEmail(User user) {
        emailService.send(user.getEmail(), "Welcome!", "Thanks for joining.");
    }

    public User getCachedUser(String email) {
        return userCache.get(email);
    }
}
```

이 클래스를 변경해야 하는 이유는 최소 네 가지다. 이메일 검증 규칙이 바뀌면, 데이터베이스 스키마가 바뀌면, 이메일 발송 방식이 바뀌면, 캐시 전략이 바뀌면 — 모두 이 하나의 클래스를 건드리게 된다. 18장에서 다룬 SRP 기준으로, 이 네 가지 변경 이유 각각을 별도 클래스로 분리한다.

```java
// 리팩토링 결과: 책임별로 분리된 클래스들
public class UserValidator {
    public boolean isValid(User user) {
        return user.getEmail() != null && user.getEmail().matches("^[A-Za-z0-9+_.-]+@(.+)$");
    }
}

public class UserRepository {
    private final Connection dbConnection;
    public UserRepository(Connection dbConnection) { this.dbConnection = dbConnection; }

    public void save(User user) throws SQLException {
        String sql = "INSERT INTO users (name, email) VALUES (?, ?)";
        PreparedStatement stmt = dbConnection.prepareStatement(sql);
        stmt.setString(1, user.getName());
        stmt.setString(2, user.getEmail());
        stmt.executeUpdate();
    }
}

public class UserNotifier {
    private final EmailService emailService;
    public UserNotifier(EmailService emailService) { this.emailService = emailService; }

    public void sendWelcomeEmail(User user) {
        emailService.send(user.getEmail(), "Welcome!", "Thanks for joining.");
    }
}

public class UserCache {
    private final Map<String, User> cache = new HashMap<>();
    public void put(User user) { cache.put(user.getEmail(), user); }
    public User get(String email) { return cache.get(email); }
}
```

분리된 각 클래스는 이제 하나의 이해관계자, 하나의 변경 이유만 갖는다. `UserValidator`는 이메일 검증 규칙이 바뀔 때만, `UserRepository`는 DB 스키마가 바뀔 때만 수정된다.

## 실습 2: 조립 지점 설계 — DIP 적용

책임을 분리한 뒤에는 이 조각들을 다시 조립해 원래의 기능(회원가입 처리)을 완성해야 한다. 이때 각 조각이 서로를 직접 `new`로 생성하게 하면 다시 강한 결합이 생긴다. 대신 상위 계층의 `UserService`가 생성자를 통해 필요한 협력자를 주입받도록 설계한다.

```java
// UserService는 구체적인 구현이 아니라 필요한 협력자를 주입받아 조립한다
public class UserService {
    private final UserValidator validator;
    private final UserRepository repository;
    private final UserNotifier notifier;
    private final UserCache cache;

    public UserService(UserValidator validator, UserRepository repository,
                        UserNotifier notifier, UserCache cache) {
        this.validator = validator;
        this.repository = repository;
        this.notifier = notifier;
        this.cache = cache;
    }

    public void registerUser(User user) throws SQLException {
        if (!validator.isValid(user)) {
            throw new IllegalArgumentException("Invalid user: " + user.getEmail());
        }
        repository.save(user);
        cache.put(user);
        notifier.sendWelcomeEmail(user);
    }
}
```

`UserService`를 테스트할 때는 실제 DB나 이메일 서버 대신 각 협력자의 테스트 더블을 주입하면 된다. 이는 [16~17장](/post/clean-code/unit-testing-tdd-test-driven-development/)에서 다룬 F.I.R.S.T 원칙을 만족하는 테스트를 가능하게 하는 구조이며, 이 조립 방식을 시스템 전체로 확장하는 방법은 [20장](/post/clean-code/system-design-dependency-injection-architecture/)에서 다룬다.

## 판단 기준: 분해가 과도한지 점검하기

리팩토링 후 클래스 개수가 1개에서 5개로 늘었다는 사실 자체는 성공의 척도가 아니다. 점검할 것은 "각 클래스가 정말 서로 다른 이유로 변경되는가"이다. 만약 `UserCache`가 실제로는 `UserRepository`와 항상 함께 수정된다면(캐시 무효화 로직이 저장 로직에 강하게 결합돼 있다면), 두 클래스를 억지로 분리한 것이 오히려 하나의 논리적 단위를 두 파일로 쪼개 추적을 어렵게 만든 것일 수 있다. 이 경우 18장의 "비판적 시각"에서 다룬 과잉 설계 신호로 보고 재통합을 고려해야 한다.

## 다음 장에서는

[20장: 시스템과 의존성 주입](/post/clean-code/system-design-dependency-injection-architecture/)에서는 이 실습에서 손으로 조립한 `UserService`의 협력자 주입을 시스템 전체 규모로 확장하는 방법을 다룬다.

## 평가 기준

- [ ] God Class에서 서로 다른 변경 이유를 식별하고 책임별로 클래스를 분리할 수 있다.
- [ ] 분리된 클래스들을 생성자 주입으로 조립하는 구조를 설계할 수 있다.
- [ ] 분해가 과도한지 "실제로 함께 변경되는가"라는 기준으로 재점검할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 10장.
