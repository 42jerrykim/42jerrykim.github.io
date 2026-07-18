---
draft: true
collection_order: 61
title: "[Design Patterns] 06. 빌더와 프로토타입 패턴의 깊이 있는 이해 — 실습"
slug: "builder-prototype-deep-understanding-practice"
description: "Builder와 Prototype 패턴을 실제 프로젝트에 적용하는 종합 실습입니다. HTTP 클라이언트 Builder, 게임 캐릭터 Prototype, 설정 객체 관리 등을 통해 복잡한 객체 생성과 복제 전략을 마스터하고, 불변 객체와 성능 최적화 기법까지 학습합니다."
image: "wordcloud.png"
date: 2024-12-06T11:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Creational Patterns
- Object Construction
- Practice
- Pattern Implementation
tags:
- Tutorial(튜토리얼)
- Implementation(구현)
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Creational-Pattern
- Builder
- Software-Architecture(소프트웨어아키텍처)
- OOP(객체지향)
- Composition(합성)
- Encapsulation(캡슐화)
- Polymorphism(다형성)
- Abstraction(추상화)
- Interface(인터페이스)
- Clean-Code(클린코드)
- Best-Practices
- Code-Quality(코드품질)
- Maintainability
- Readability
- Type-Safety
- Performance(성능)
- Optimization(최적화)
- Testing(테스트)
- Guide(가이드)
- Case-Study
- Advanced
- Java
- SOLID
- Refactoring(리팩토링)
---

이 실습에서는 Builder와 Prototype 패턴을 활용하여 복잡한 객체 생성 문제를 해결하는 다양한 기법을 직접 구현합니다.

## 실습 목표
- Builder 패턴의 다양한 구현 방식 학습
- Prototype 패턴의 깊은 복사와 얕은 복사 이해
- 불변 객체와 Builder 패턴 조합
- 성능 최적화된 객체 생성 전략

## 실습 1: HTTP 클라이언트 Builder

이론 편의 "Constructor Hell" 예시(url, method, headers, body, timeout 등 여러 매개변수를 가진 생성자)를 실제로 Builder로 리팩터링하는 실습입니다. url과 method는 요청마다 반드시 있어야 하는 필수 필드이고, headers·body·timeout은 없어도 요청이 성립하는 선택 필드라는 점에 주목해 필수/선택을 구분하는 Builder를 설계합니다. 필수 필드는 생성자가 아니라 `build()` 시점에 검증하는 이유는, 필드가 하나만 있을 때는 생성자 검증도 무방하지만 필수 필드가 2개 이상이 되는 순간 "어떤 순서로 넘겨야 컴파일이 되는가"라는 문제가 다시 생기기 때문입니다. 또한 `headers` 필드는 `Map`을 그대로 반환하면 외부에서 내부 상태를 변경할 수 있으므로, `build()` 시점에 `Collections.unmodifiableMap`으로 방어적 복사를 해야 한다는 점도 함께 확인합니다.

### 요구사항
복잡한 HTTP 요청 설정을 간편하게 생성할 수 있는 Builder 구현

### 기준 답안

```java
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

public final class HttpRequest {
    private final String url;
    private final String method;
    private final Map<String, String> headers;
    private final String body;
    private final int timeout;

    private HttpRequest(Builder builder) {
        this.url = builder.url;
        this.method = builder.method;
        this.headers = Collections.unmodifiableMap(new LinkedHashMap<>(builder.headers));
        this.body = builder.body;
        this.timeout = builder.timeout;
    }

    public String getUrl() { return url; }
    public String getMethod() { return method; }
    public Map<String, String> getHeaders() { return headers; }
    public String getBody() { return body; }
    public int getTimeout() { return timeout; }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        // 필수 필드 - build() 시점에 null 검증
        private String url;
        private String method;

        // 선택 필드 - 기본값 지정
        private final Map<String, String> headers = new LinkedHashMap<>();
        private String body = "";
        private int timeout = 3000;

        public Builder url(String url) {
            this.url = url;
            return this;
        }

        public Builder method(String method) {
            this.method = method;
            return this;
        }

        public Builder header(String key, String value) {
            this.headers.put(key, value);
            return this;
        }

        public Builder body(String body) {
            this.body = body;
            return this;
        }

        public Builder timeout(int timeoutMillis) {
            if (timeoutMillis <= 0) {
                throw new IllegalArgumentException("timeout must be positive: " + timeoutMillis);
            }
            this.timeout = timeoutMillis;
            return this;
        }

        public HttpRequest build() {
            if (url == null || url.isEmpty()) {
                throw new IllegalStateException("url is required");
            }
            if (method == null || method.isEmpty()) {
                throw new IllegalStateException("method is required");
            }
            return new HttpRequest(this);
        }
    }
}

// 테스트 코드
public class HttpRequestTest {
    @Test
    public void testBuilder() {
        HttpRequest request = HttpRequest.builder()
            .url("https://api.example.com")
            .method("POST")
            .header("Content-Type", "application/json")
            .body("{\"name\":\"test\"}")
            .timeout(5000)
            .build();

        assertEquals("https://api.example.com", request.getUrl());
        assertEquals("POST", request.getMethod());
        assertEquals("application/json", request.getHeaders().get("Content-Type"));
        assertEquals(5000, request.getTimeout());
    }

    @Test
    public void testMissingUrlThrows() {
        assertThrows(IllegalStateException.class, () ->
            HttpRequest.builder().method("GET").build()
        );
    }
}
```

## 실습 2: 게임 캐릭터 Prototype

게임 캐릭터는 `Stats`, `List<Item>`, `Equipment` 같은 참조 타입 필드를 여러 개 갖고 있어, `clone()`을 얕은 복사로 구현하면 원본과 복제본이 인벤토리를 공유하는 버그가 생깁니다. 이 실습에서는 각 참조 필드를 개별적으로 깊은 복사하는 `clone()`과, 동일한 목적을 생성자로 표현하는 복사 생성자 두 가지 방식을 비교합니다. 아래 코드 템플릿의 TODO 4개는 각각 다른 목적을 가집니다. TODO 1(`clone()`)은 `Cloneable` 계약을 따르는 표준 복제 경로이고, TODO 2(복사 생성자)는 `CloneNotSupportedException` 없이 같은 결과를 얻는 대안입니다. TODO 3(`toBuilder()`)은 복제 후 일부 필드만 바꾸고 싶을 때 Builder의 유연한 검증·조합 능력을 빌려오는 역할이며, TODO 4(`CharacterPrototypeFactory`)는 클래스별 기본 프로토타입을 미리 등록해두고 이름만 바꿔 대량 생성하는 실무 시나리오(이론 편의 "100명의 Warrior 생성" 예시)를 그대로 구현하는 것입니다. 구현 시 `stats`, `inventory`, `equipment` 세 필드 모두 얕은 복사로 남겨두지 않았는지 각각 확인하세요.

### 요구사항
게임 캐릭터의 효율적인 복제 시스템 구현

### 코드 템플릿

```java
public class GameCharacter implements Cloneable {
    private String name;
    private int level;
    private Stats stats;
    private List<Item> inventory;
    private Equipment equipment;
    
    // TODO 1: 깊은 복사 구현
    @Override
    public GameCharacter clone() throws CloneNotSupportedException {
        // TODO: 참조 타입 필드들의 깊은 복사 구현
        return null;
    }
    
    // TODO 2: 복사 생성자 구현
    public GameCharacter(GameCharacter other) {
        // TODO: 다른 방식의 복사 구현
    }
    
    // TODO 3: 빌더와 결합
    public Builder toBuilder() {
        // TODO: 기존 객체를 바탕으로 Builder 생성
        return null;
    }
}

// TODO 4: 캐릭터 프로토타입 팩토리
public class CharacterPrototypeFactory {
    private final Map<String, GameCharacter> prototypes = new HashMap<>();
    
    // TODO: 프로토타입 등록 및 생성 메서드 구현
}
```

## 실습 3: 설정 객체 Builder + Prototype

dev/staging/prod처럼 대부분의 필드는 같고 일부만 다른 설정 객체를 만들 때, 매번 Builder로 처음부터 값을 채우면 공통 필드가 중복됩니다. 이 실습에서는 하나의 기본 설정을 Prototype으로 복제한 뒤 Builder의 `with*` 메서드로 환경별 차이만 덮어써, 두 패턴을 조합하는 방법을 익힙니다. TODO 1(불변 필드 + Builder)은 실습 1에서 만든 패턴을 재사용하되 `equals`/`hashCode`까지 갖춘 완전한 값 객체로 만드는 것이 목표이고, TODO 2(환경별 설정 복제)는 `baseConfig.clone()` 후 `dbUrl`, `logLevel` 같은 환경 종속 필드만 바꾸는 흐름을 구현합니다. TODO 3(`with*` 메서드)은 복제 후 필드 변경을 매번 `clone()` 직접 호출 없이 하나의 메서드 호출로 끝내기 위한 것으로, 실습 2의 `toBuilder()`와 같은 목적을 더 가벼운 방식으로 달성합니다.

### 코드 템플릿

```java
public class ServerConfig implements Cloneable {
    // TODO 1: 불변 필드들과 Builder 패턴 조합
    // TODO 2: 환경별 설정 복제 (dev, staging, prod)
    // TODO 3: 설정 변경 시 새 인스턴스 생성하는 with* 메서드들
}
```

## 체크리스트

### Builder 패턴
- [ ] 필수/선택적 매개변수 구분
- [ ] 메서드 체이닝 구현
- [ ] 검증 로직 포함
- [ ] 불변 객체 생성

### Prototype 패턴
- [ ] 깊은 복사 정확히 구현
- [ ] 성능 최적화 (필요한 부분만 복사)
- [ ] 복사 생성자 구현
- [ ] 프로토타입 팩토리 구현

### 통합 구현
- [ ] Builder + Prototype 조합
- [ ] 함수형 스타일 변형 메서드
- [ ] 성능 테스트 완료

## 추가 도전

1. **Type-Safe Builder**: 컴파일 타임 검증
2. **Lens 패턴**: 함수형 객체 변형
3. **Copy-on-Write**: 지연 복사 최적화
4. **Fluent Interface**: 자연어에 가까운 API

## 실무 적용

### Builder 패턴 활용
- DTO/VO 객체 생성 — 선택 필드가 많은 요청/응답 객체에서 생성자 오버로딩 대신 이름 있는 메서드로 값을 채워 가독성을 높인다 (실습 1의 `HttpRequest.Builder` 참고)
- 설정 객체 관리 — 대부분 필드에 합리적인 기본값을 두고 필요한 값만 덮어써 환경별 설정 코드 중복을 줄인다 (실습 3의 `ServerConfig` 참고)
- 테스트 데이터 빌더 — 테스트마다 관심 있는 필드만 지정하고 나머지는 기본값을 쓰는 픽스처를 만들어 테스트 코드의 의도를 드러낸다 (예: `aUser().withName("test").build()`)

### Prototype 패턴 활용
- 객체 풀 관리 — 매번 새로 생성하는 대신 미리 만든 프로토타입을 복제해 재사용, 초기화 비용을 반복 지불하지 않는다 (실습 2의 `CharacterPrototypeFactory` 참고)
- 설정 템플릿 시스템 — dev/staging/prod처럼 공통 필드가 많은 설정을 기본 템플릿 하나로 유지하고 필요한 부분만 복제 후 수정한다 (실습 3 참고)
- 성능 크리티컬한 객체 생성 — DB 조회나 복잡한 계산이 들어간 초기화를 한 번만 수행하고 이후에는 `clone()`으로 대체해 초기화 비용을 없앤다 (이론 편의 JMH 벤치마크 참고)

### 과용하면 안 되는 경우
- 필드가 2~3개뿐인 단순 DTO — 일반 생성자나 정적 팩토리 메서드로 충분하며 Builder는 코드량만 늘린다
- 참조 필드가 없어 얕은 복사와 깊은 복사의 차이가 없는 불변 객체 — Prototype 없이 생성자 재사용으로 충분하다
- 생성 빈도가 낮고 초기화 비용도 낮은 객체 — Prototype의 복제 이득보다 별도 clone 로직 유지 비용이 더 크다

---

### 평가 기준

**이 실습을 마친 후 스스로 확인해야 할 목표:**
- [ ] 실습 1의 `HttpRequest.Builder`에서 필수 필드 누락 시 `build()`가 `IllegalStateException`을 던지는지 테스트로 확인했다
- [ ] 실습 2의 `clone()`에서 `stats`, `inventory`, `equipment` 세 필드 모두 깊은 복사를 구현하고, 복제본 수정이 원본에 영향을 주지 않는지 검증했다
- [ ] 실습 3에서 환경별 `ServerConfig`를 만들 때 공통 필드를 중복 입력하지 않고 Prototype + `with*` 조합으로 구현했다
- [ ] Builder/Prototype 각각을 언제 쓰고 언제 과용인지("과용하면 안 되는 경우" 참고) 스스로 설명할 수 있다

**핵심 포인트**: Builder는 복잡한 객체 생성을, Prototype은 효율적인 객체 복제를 담당합니다. 두 패턴의 조합으로 강력한 객체 생성 전략을 구축할 수 있습니다. 