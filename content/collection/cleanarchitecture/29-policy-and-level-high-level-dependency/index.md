---
draft: true
collection_order: 290
image: "wordcloud.png"
description: "정책의 수준(Level)과 의존성 방향의 관계를 다룹니다. 고수준 정책과 저수준 정책을 입출력으로부터의 거리를 기준으로 구분하고, 암호화 프로그램 예제로 의존성이 고수준을 향해야 하는 이유를 아주 자세히 설명합니다."
title: "[Clean Architecture] 29. 정책과 수준"
slug: policy-and-level-high-level-dependency
date: 2026-01-18
categories: CleanArchitecture
tags:
  - Clean-Architecture(클린아키텍처)
  - Security(보안)
  - Dependency-Injection(의존성주입)
  - Software-Architecture(소프트웨어아키텍처)
  - IO(Input/Output)
  - Shortest-Path(최단경로)
  - Interface(인터페이스)
  - Abstraction(추상화)
  - Code-Quality(코드품질)
  - Design-Pattern(디자인패턴)
  - Coupling(결합도)
  - Cohesion(응집도)
  - Modularity
  - History(역사)
  - Best-Practices
  - Maintainability
  - Refactoring(리팩토링)
  - Case-Study
  - Deep-Dive
  - Technology(기술)
  - Testing(테스트)
  - OOP(객체지향)
  - Polymorphism(다형성)
  - System-Design
  - Documentation(문서화)
  - Readability
  - TDD(Test-Driven Development)
---

소프트웨어 시스템은 여러 **정책(Policy)**의 집합이다. 정책들은 서로 다른 **수준(Level)**에 존재하며, 의존성은 수준의 방향으로 흘러야 한다.

## 정책(Policy)이란?

정책은 시스템의 **행동을 기술**하는 것이다.

```mermaid
flowchart LR
    subgraph Policies [정책의 예]
        P1[입력을 읽는 방법]
        P2[데이터를 변환하는 방법]
        P3[출력을 쓰는 방법]
    end
```

### 정책의 예시

| 정책 유형 | 예시 |
|----------|------|
| 입력 정책 | 키보드 읽기, 파일 읽기, HTTP 요청 수신 |
| 변환 정책 | 암호화, 포맷 변환, 비즈니스 규칙 적용 |
| 출력 정책 | 화면 출력, 파일 저장, HTTP 응답 전송 |

```java
// 다양한 정책의 예
// 입력 정책
interface InputReader {
    String read();
}

// 변환 정책 (비즈니스 규칙)
interface Transformer {
    String transform(String input);
}

// 출력 정책
interface OutputWriter {
    void write(String output);
}
```

## 수준(Level)이란?

**입력과 출력으로부터의 거리**가 수준을 결정한다.

```mermaid
flowchart LR
    INPUT[입력 장치<br/>저수준]
    LOW1[입력 처리<br/>저수준]
    MID[비즈니스 로직<br/>중간]
    HIGH[핵심 규칙<br/>고수준]
    MID2[출력 처리<br/>중간]
    LOW2[출력 장치<br/>저수준]
    OUTPUT[화면/파일<br/>저수준]
    
    INPUT --> LOW1 --> MID --> HIGH
    HIGH --> MID2 --> LOW2 --> OUTPUT
```

### 수준의 정의

| 수준 | 특징 | 예시 |
|------|------|------|
| **고수준** | 입출력에서 멀리 떨어짐 | 핵심 비즈니스 규칙 |
| **중간 수준** | 변환과 처리 | 유스케이스 |
| **저수준** | 입출력에 가까움 | UI, DB, 외부 API |

### 왜 거리가 중요한가?

> "입력과 출력에 가까울수록 **변경 가능성이 높다**. 멀수록 **안정적**이다."

```mermaid
flowchart TB
    subgraph ChangeFrequency [변경 빈도]
        UI[UI - 자주 변경]
        UC[유스케이스 - 가끔 변경]
        BR[비즈니스 규칙 - 드물게 변경]
    end
    
    UI -->|더 안정| UC -->|더 안정| BR
```

## 의존성 방향

의존성은 **수준이 낮은 곳에서 수준이 높은 곳**으로 흘러야 한다.

```mermaid
flowchart TB
    subgraph Good [올바른 의존성 방향]
        direction TB
        L1[저수준: Console Reader]
        L2[저수준: Console Writer]
        H[고수준: Encrypter]
        
        L1 --> H
        L2 --> H
    end
```

### 잘못된 의존성

```mermaid
flowchart TB
    subgraph Bad [잘못된 의존성 방향]
        direction TB
        H2[고수준: Encrypter]
        L3[저수준: Console Reader]
        L4[저수준: Console Writer]
        
        H2 --> L3
        H2 --> L4
    end
```

고수준 정책이 저수준 정책을 **모르게** 해야 한다.

## 예시: 암호화 프로그램

마틴은 간단한 암호화 프로그램을 예로 들어 설명한다.

### 요구사항

- 문자를 읽어서
- 암호화하고
- 암호화된 문자를 출력

### 잘못된 설계

```java
// 고수준이 저수준에 의존 - 나쁜 설계
public class Encrypter {
    private ConsoleReader reader;   // 저수준에 의존!
    private ConsoleWriter writer;   // 저수준에 의존!
    
    public void encrypt() {
        char c = reader.readChar();
        char encrypted = doEncrypt(c);
        writer.writeChar(encrypted);
    }
    
    private char doEncrypt(char c) {
        // 암호화 로직 (고수준)
        return (char)(c + 1);
    }
}
```

### 올바른 설계

```java
// 고수준: 비즈니스 규칙 (인터페이스만 알고 있음)
public interface Encrypt {
    char encrypt(char c);
}

public class CaesarCipher implements Encrypt {
    private final int shift;
    
    public char encrypt(char c) {
        return (char)(c + shift);
    }
}

// 저수준: 입출력 인터페이스
public interface CharReader {
    char readChar();
}

public interface CharWriter {
    void writeChar(char c);
}

// 저수준 구현: 고수준 인터페이스에 의존
public class ConsoleReader implements CharReader {
    public char readChar() {
        return (char) System.in.read();
    }
}

public class ConsoleWriter implements CharWriter {
    public void writeChar(char c) {
        System.out.print(c);
    }
}
```

### 조립 (의존성 주입)

```java
// Main에서 조립
public class Main {
    public static void main(String[] args) {
        CharReader reader = new ConsoleReader();
        CharWriter writer = new ConsoleWriter();
        Encrypt encrypt = new CaesarCipher(3);
        
        // 고수준 모듈에 저수준 구현 주입
        EncryptionService service = new EncryptionService(
            reader, writer, encrypt
        );
        service.run();
    }
}

// 고수준 서비스: 인터페이스만 의존
public class EncryptionService {
    private final CharReader reader;
    private final CharWriter writer;
    private final Encrypt encrypt;
    
    public void run() {
        char c;
        while ((c = reader.readChar()) != EOF) {
            writer.writeChar(encrypt.encrypt(c));
        }
    }
}
```

## 수준과 변경

```mermaid
flowchart TB
    subgraph Levels [수준별 변경 특성]
        HIGH[고수준<br/>비즈니스 규칙<br/>변경 적음]
        MID[중간 수준<br/>유스케이스<br/>가끔 변경]
        LOW[저수준<br/>입출력<br/>자주 변경]
    end
    
    LOW -->|의존| MID
    MID -->|의존| HIGH
```

| 수준 | 변경 빈도 | 변경 이유 |
|------|----------|----------|
| 고수준 | 드물게 | 비즈니스 요구사항 변경 |
| 중간 수준 | 가끔 | 새로운 기능 추가 |
| 저수준 | 자주 | 기술 변경, UI 개선 |

### 왜 고수준으로 의존해야 하는가?

```java
// 저수준이 변경되어도 고수준은 영향 없음

// 콘솔 → 파일로 변경
public class FileReader implements CharReader {
    public char readChar() {
        return fileInputStream.read();
    }
}

// 암호화 로직(고수준)은 그대로!
public class CaesarCipher implements Encrypt {
    public char encrypt(char c) {
        return (char)(c + shift);
    }
}
```

## 아키텍처에 적용

```mermaid
flowchart TB
    subgraph Architecture [클린 아키텍처의 수준]
        ENT[Entities<br/>가장 고수준]
        UC[Use Cases<br/>고수준]
        CTRL[Controllers<br/>중간]
        GW[Gateways<br/>저수준]
        DB[(DB)<br/>가장 저수준]
    end
    
    DB --> GW --> CTRL --> UC --> ENT
```

## 흔한 오해

"고수준"을 "추상 클래스나 인터페이스"와 같은 말로, "저수준"을 "구체 클래스"와 같은 말로 오해하기 쉽다. 그러나 이 장이 정의하는 수준은 추상화 정도가 아니라 **입출력으로부터의 거리**다. 암호화 예제에서 `Encrypt` 인터페이스와 `CaesarCipher` 구현 모두 고수준에 속한다 — 암호화 알고리즘이 무엇이든 입출력 장치와 무관하게 성립하는 규칙이기 때문이다. 반면 `CharReader`·`CharWriter`는 인터페이스임에도 저수준이다. 입출력 장치에 직접 닿아 있어 자주 바뀔 수 있기 때문이다. 즉 추상화(인터페이스 vs 구현)와 수준(고수준 vs 저수준)은 서로 다른 축이며, 둘 다 같은 방향(안정적인 쪽)으로 의존성이 향해야 한다는 점에서만 만난다.

## 학습 목표

이 장을 읽은 후 다음을 스스로 점검한다.

- 수준(Level)이 "입출력으로부터의 거리"로 정의된다는 것을, 추상화 정도와 구분해 설명할 수 있는가?
- 암호화 예제에서 왜 `Encrypt`는 고수준이고 `CharReader`는 저수준인지 설명할 수 있는가?
- 저수준 구현(콘솔 → 파일)이 바뀌어도 고수준 로직이 영향받지 않는 이유를 코드로 설명할 수 있는가?
- Clean Architecture의 동심원(Entities → Use Cases → Controllers → Gateways)이 왜 수준의 순서와 일치하는지 설명할 수 있는가?

## 판단 기준

새 클래스나 모듈을 어느 수준에 배치할지 판단할 때 다음을 확인한다.

- 이 코드가 입출력 장치(파일, 네트워크, DB, UI)의 구체적인 형태가 바뀌면 함께 바뀌는가? 그렇다면 저수준이다.
- 이 코드가 특정 기술과 무관하게, 비즈니스 요구사항이 바뀔 때만 바뀌는가? 그렇다면 고수준이다.
- 지금 의존성 화살표가 저수준에서 고수준으로 향하는가, 아니면 고수준 코드에 저수준 클래스 이름이 직접 등장하는가?

## 참고 자료

- Robert C. Martin, 『Clean Architecture』, 2017, 19장 — 정책과 수준, 암호화 예제의 원 출처.

## 핵심 요약

| 원칙 | 설명 |
|------|------|
| 수준의 정의 | 입출력으로부터의 거리 |
| 의존성 방향 | 저수준 → 고수준 |
| 고수준의 특징 | 안정적, 변경 적음 |
| 저수준의 특징 | 불안정, 변경 많음 |

마틴은 수준이 높을수록 변경이 적고, 수준이 낮을수록 변경이 많다고 말한다. 따라서 의존성은 고수준을 향해야 한다(Martin, 『Clean Architecture』, 2017, 19장).

```mermaid
flowchart LR
    CHANGE[변경] --> LOW[저수준]
    LOW -->|의존| HIGH[고수준]
    HIGH -.->|영향 없음| CHANGE
```

안정적인 고수준 정책이 불안정한 저수준 정책을 모르게 하면, **저수준의 변경이 고수준에 영향을 주지 않는다**.
