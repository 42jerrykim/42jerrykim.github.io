---
collection_order: 61
draft: true
title: "[Design Patterns] 빌더와 프로토타입 패턴 실습 - 복잡한 객체 생성 마스터"
description: "Builder와 Prototype 패턴을 실제 프로젝트에 적용하는 종합 실습입니다. HTTP 클라이언트 Builder, 게임 캐릭터 Prototype, 설정 객체 관리 등을 통해 복잡한 객체 생성과 복제 전략을 마스터하고, 불변 객체와 성능 최적화 기법까지 학습합니다."
date: 2024-12-06T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Creational Patterns
- Object Construction
- Practice
- Pattern Implementation
tags:
- Builder Pattern Practice
- Prototype Pattern Practice
- Object Construction
- Fluent Interface
- Method Chaining
- Complex Objects
- Object Cloning
- Deep Copy
- Shallow Copy
- Immutable Objects
- HTTP Client Builder
- Game Character Creation
- Configuration Objects
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Creational Patterns
- Design Patterns
- GoF Patterns
- Object Assembly
- Data Transfer Objects
- API Design
- 빌더 패턴 실습
- 프로토타입 패턴 실습
- 객체 구성
- 플루언트 인터페이스
- 메서드 체이닝
- 복잡한 객체
- 객체 복제
- 깊은 복사
- 얕은 복사
- 불변 객체
- HTTP 클라이언트 빌더
- 게임 캐릭터 생성
- 설정 객체
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 생성 패턴
- 디자인 패턴
- GoF 패턴
- 객체 조립
- 데이터 전송 객체
- API 설계
---

# Builder & Prototype 패턴 실습 - 복잡한 객체 생성 마스터

## 🎯 **실습 목표**
- Builder 패턴의 다양한 구현 방식 학습
- Prototype 패턴의 깊은 복사와 얕은 복사 이해
- 불변 객체와 Builder 패턴 조합
- 성능 최적화된 객체 생성 전략

## 📋 **실습 1: HTTP 클라이언트 Builder**

### **요구사항**
복잡한 HTTP 요청 설정을 간편하게 생성할 수 있는 Builder 구현

### **💻 코드 템플릿**

```java
public class HttpRequest {
    private final String url;
    private final String method;
    private final Map<String, String> headers;
    private final String body;
    private final int timeout;
    
    // TODO 1: private 생성자 구현
    
    // TODO 2: Builder 내부 클래스 구현
    public static class Builder {
        // TODO: 필수 필드와 선택적 필드 구분
        // TODO: 체이닝 메서드들 구현
        // TODO: 검증 로직 포함한 build() 메서드
    }
    
    // TODO 3: 정적 팩토리 메서드
    public static Builder builder() {
        return new Builder();
    }
}

// TODO 4: 테스트 코드
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
        
        // TODO: 검증 로직
    }
}
```

## 📋 **실습 2: 게임 캐릭터 Prototype**

### **요구사항**
게임 캐릭터의 효율적인 복제 시스템 구현

### **💻 코드 템플릿**

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

## 📋 **실습 3: 설정 객체 Builder + Prototype**

### **💻 코드 템플릿**

```java
public class ServerConfig implements Cloneable {
    // TODO 1: 불변 필드들과 Builder 패턴 조합
    // TODO 2: 환경별 설정 복제 (dev, staging, prod)
    // TODO 3: 설정 변경 시 새 인스턴스 생성하는 with* 메서드들
}
```

## ✅ **체크리스트**

### **Builder 패턴**
- [ ] 필수/선택적 매개변수 구분
- [ ] 메서드 체이닝 구현
- [ ] 검증 로직 포함
- [ ] 불변 객체 생성

### **Prototype 패턴**
- [ ] 깊은 복사 정확히 구현
- [ ] 성능 최적화 (필요한 부분만 복사)
- [ ] 복사 생성자 구현
- [ ] 프로토타입 팩토리 구현

### **통합 구현**
- [ ] Builder + Prototype 조합
- [ ] 함수형 스타일 변형 메서드
- [ ] 성능 테스트 완료

## 🔍 **추가 도전**

1. **Type-Safe Builder**: 컴파일 타임 검증
2. **Lens 패턴**: 함수형 객체 변형
3. **Copy-on-Write**: 지연 복사 최적화
4. **Fluent Interface**: 자연어에 가까운 API

## 🚀 **실무 적용**

### **Builder 패턴 활용**
- DTO/VO 객체 생성
- 설정 객체 관리
- 테스트 데이터 빌더

### **Prototype 패턴 활용**
- 객체 풀 관리
- 설정 템플릿 시스템
- 성능 크리티컬한 객체 생성

---

💡 **핵심 포인트**: Builder는 복잡한 객체 생성을, Prototype은 효율적인 객체 복제를 담당합니다. 두 패턴의 조합으로 강력한 객체 생성 전략을 구축할 수 있습니다. 