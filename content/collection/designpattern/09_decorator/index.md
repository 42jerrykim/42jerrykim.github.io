---
collection_order: 9
title: "[Design Pattern] Decorator - 데코레이터 패턴"
description: "Decorator 패턴은 객체에 동적으로 새로운 기능을 추가하는 구조적 패턴입니다. 상속 대신 합성을 활용하여 기존 코드 수정 없이 여러 기능을 유연하게 조합합니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Decorator
  - 데코레이터
  - Structural Pattern
  - 구조 패턴
  - GoF
  - Gang of Four
  - Wrapper
  - 래퍼
  - Dynamic Behavior
  - 동적 행위
  - Composition
  - 합성
  - Open Closed Principle
  - 개방 폐쇄 원칙
  - Single Responsibility
  - 단일 책임
  - Flexible Extension
  - 유연한 확장
  - Concrete Decorator
  - 구체 데코레이터
  - Component
  - 컴포넌트
  - Stream
  - 스트림
  - I/O
  - 입출력
  - BufferedInputStream
  - Coffee Example
  - 커피 예제
  - Code Reusability
  - 코드 재사용성
  - Maintainability
  - 유지보수성
  - Software Design
  - 소프트웨어 설계
  - OOP
  - 객체지향 프로그래밍
  - Java
  - C++
  - Python
  - C#
  - Chaining
  - 체이닝
  - Runtime
  - 런타임
  - Feature Addition
  - 기능 추가
---

데코레이터 패턴(Decorator Pattern)은 객체에 동적으로 새로운 책임을 추가할 수 있게 해주는 구조적 디자인 패턴이다. 상속을 사용하지 않고도 객체의 기능을 확장할 수 있어, 런타임에 유연하게 기능을 조합할 수 있다. 마치 선물 포장처럼 객체를 여러 겹으로 감싸면서 새로운 기능을 덧붙이는 방식으로 동작한다.

## 개요

**데코레이터 패턴의 정의**

데코레이터 패턴은 기존 객체를 새로운 객체로 감싸서 기능을 추가하는 패턴이다. 데코레이터는 원본 객체와 동일한 인터페이스를 구현하므로, 클라이언트 입장에서는 데코레이터로 감싸진 객체와 원본 객체를 동일하게 취급할 수 있다.

**패턴의 필요성 및 사용 사례**

데코레이터 패턴은 다음과 같은 상황에서 유용하다:

- **동적 기능 추가**: 런타임에 객체의 기능을 동적으로 추가하거나 제거해야 할 때
- **기능 조합의 폭발적 증가 방지**: 상속으로 인한 서브클래스 폭발을 피하고 싶을 때
- **단일 책임 원칙 준수**: 각 기능을 별도의 클래스로 분리하고 싶을 때
- **기존 코드 수정 불가**: 기존 클래스를 수정할 수 없지만 기능을 확장해야 할 때

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 상속보다 유연한 기능 확장 | 많은 작은 객체가 생성될 수 있음 |
| 런타임에 동적으로 기능 추가/제거 가능 | 데코레이터 순서에 따라 결과가 달라질 수 있음 |
| 단일 책임 원칙 준수 | 초기 설정 코드가 복잡해질 수 있음 |
| 개방-폐쇄 원칙 준수 | 특정 데코레이터를 제거하기 어려울 수 있음 |

## 데코레이터 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│         <<interface>>               │
│           Component                 │
├─────────────────────────────────────┤
│ + operation()                       │
└─────────────────────────────────────┘
              △
              │
     ┌────────┴────────┐
     │                 │
┌─────────────┐  ┌─────────────────────────────┐
│ Concrete    │  │       Decorator             │
│ Component   │  ├─────────────────────────────┤
├─────────────┤  │ - component: Component      │
│ +operation()│  ├─────────────────────────────┤
└─────────────┘  │ + operation()               │
                 │   └── component.operation() │
                 └─────────────────────────────┘
                               △
                               │
              ┌────────────────┼────────────────┐
              │                │                │
      ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
      │ ConcreteDecA  │ │ ConcreteDecB  │ │ ConcreteDecC  │
      ├───────────────┤ ├───────────────┤ ├───────────────┤
      │ + operation() │ │ + operation() │ │ + operation() │
      │ + addedBehav()│ │ + addedBehav()│ │ + addedBehav()│
      └───────────────┘ └───────────────┘ └───────────────┘
```

**1. Component (컴포넌트)**
- 기본 기능을 정의하는 인터페이스 또는 추상 클래스
- 데코레이터와 구체 컴포넌트가 공통으로 구현하는 인터페이스

**2. ConcreteComponent (구체 컴포넌트)**
- Component 인터페이스를 구현하는 기본 객체
- 데코레이터가 감싸는 대상이 되는 원본 객체

**3. Decorator (데코레이터)**
- Component 인터페이스를 구현하고, Component 객체를 참조
- 기본 동작을 위임하고 추가 기능을 정의

**4. ConcreteDecorator (구체 데코레이터)**
- Decorator를 확장하여 실제 추가 기능을 구현
- 원본 객체의 메서드 호출 전후에 추가 동작 수행

## 구현 예제

### Python 예제 - 커피 주문 시스템

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod

# Component 인터페이스
class Coffee(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

# ConcreteComponent - 기본 커피
class Espresso(Coffee):
    def get_description(self) -> str:
        return "에스프레소"
    
    def get_cost(self) -> float:
        return 2.0

class HouseBlend(Coffee):
    def get_description(self) -> str:
        return "하우스 블렌드"
    
    def get_cost(self) -> float:
        return 1.5

# Decorator 기본 클래스
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        pass

# ConcreteDecorator - 토핑 추가
class Milk(CoffeeDecorator):
    def get_description(self) -> str:
        return f"{self._coffee.get_description()}, 우유"
    
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.3

class Mocha(CoffeeDecorator):
    def get_description(self) -> str:
        return f"{self._coffee.get_description()}, 모카"
    
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.5

class Whip(CoffeeDecorator):
    def get_description(self) -> str:
        return f"{self._coffee.get_description()}, 휘핑크림"
    
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.4

class Shot(CoffeeDecorator):
    def get_description(self) -> str:
        return f"{self._coffee.get_description()}, 샷 추가"
    
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.6

# 사용 예제
if __name__ == "__main__":
    # 기본 에스프레소
    coffee = Espresso()
    print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
    
    # 에스프레소 + 우유 + 모카 + 휘핑크림
    coffee = Espresso()
    coffee = Milk(coffee)
    coffee = Mocha(coffee)
    coffee = Whip(coffee)
    print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
    
    # 하우스 블렌드 + 더블 모카 + 휘핑크림
    coffee = HouseBlend()
    coffee = Mocha(coffee)
    coffee = Mocha(coffee)  # 더블 모카
    coffee = Whip(coffee)
    print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
```

### Java 예제 - I/O 스트림

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.io.*;

// Component 인터페이스
interface DataSource {
    void writeData(String data);
    String readData();
}

// ConcreteComponent
class FileDataSource implements DataSource {
    private String filename;
    
    public FileDataSource(String filename) {
        this.filename = filename;
    }
    
    @Override
    public void writeData(String data) {
        try (FileOutputStream fos = new FileOutputStream(filename)) {
            fos.write(data.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    @Override
    public String readData() {
        try (FileInputStream fis = new FileInputStream(filename)) {
            byte[] buffer = new byte[fis.available()];
            fis.read(buffer);
            return new String(buffer);
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }
}

// Decorator 기본 클래스
abstract class DataSourceDecorator implements DataSource {
    protected DataSource wrappee;
    
    public DataSourceDecorator(DataSource source) {
        this.wrappee = source;
    }
    
    @Override
    public void writeData(String data) {
        wrappee.writeData(data);
    }
    
    @Override
    public String readData() {
        return wrappee.readData();
    }
}

// ConcreteDecorator - 암호화
class EncryptionDecorator extends DataSourceDecorator {
    public EncryptionDecorator(DataSource source) {
        super(source);
    }
    
    @Override
    public void writeData(String data) {
        // 간단한 암호화 (실제로는 더 복잡한 알고리즘 사용)
        String encrypted = encode(data);
        super.writeData(encrypted);
    }
    
    @Override
    public String readData() {
        String data = super.readData();
        return decode(data);
    }
    
    private String encode(String data) {
        StringBuilder result = new StringBuilder();
        for (char c : data.toCharArray()) {
            result.append((char) (c + 1));
        }
        return result.toString();
    }
    
    private String decode(String data) {
        StringBuilder result = new StringBuilder();
        for (char c : data.toCharArray()) {
            result.append((char) (c - 1));
        }
        return result.toString();
    }
}

// ConcreteDecorator - 압축
class CompressionDecorator extends DataSourceDecorator {
    public CompressionDecorator(DataSource source) {
        super(source);
    }
    
    @Override
    public void writeData(String data) {
        String compressed = compress(data);
        super.writeData(compressed);
    }
    
    @Override
    public String readData() {
        String data = super.readData();
        return decompress(data);
    }
    
    private String compress(String data) {
        // 간단한 압축 시뮬레이션
        return "[COMPRESSED]" + data;
    }
    
    private String decompress(String data) {
        return data.replace("[COMPRESSED]", "");
    }
}

// 사용 예제
public class DecoratorDemo {
    public static void main(String[] args) {
        String data = "Hello, Decorator Pattern!";
        
        // 기본 파일 저장
        DataSource source = new FileDataSource("test.txt");
        source.writeData(data);
        
        // 암호화 + 압축 적용
        DataSource encrypted = new CompressionDecorator(
            new EncryptionDecorator(
                new FileDataSource("encrypted.txt")
            )
        );
        encrypted.writeData(data);
        System.out.println("Saved encrypted data");
        System.out.println("Read back: " + encrypted.readData());
    }
}
```

### C# 예제 - 알림 시스템

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;

// Component 인터페이스
public interface INotifier
{
    void Send(string message);
}

// ConcreteComponent
public class BasicNotifier : INotifier
{
    private readonly string _email;

    public BasicNotifier(string email)
    {
        _email = email;
    }

    public void Send(string message)
    {
        Console.WriteLine($"이메일로 '{message}' 전송: {_email}");
    }
}

// Decorator 기본 클래스
public abstract class NotifierDecorator : INotifier
{
    protected INotifier _wrappee;

    public NotifierDecorator(INotifier notifier)
    {
        _wrappee = notifier;
    }

    public virtual void Send(string message)
    {
        _wrappee.Send(message);
    }
}

// ConcreteDecorator - SMS 알림 추가
public class SMSDecorator : NotifierDecorator
{
    private readonly string _phoneNumber;

    public SMSDecorator(INotifier notifier, string phoneNumber) : base(notifier)
    {
        _phoneNumber = phoneNumber;
    }

    public override void Send(string message)
    {
        base.Send(message);
        Console.WriteLine($"SMS로 '{message}' 전송: {_phoneNumber}");
    }
}

// ConcreteDecorator - Slack 알림 추가
public class SlackDecorator : NotifierDecorator
{
    private readonly string _channel;

    public SlackDecorator(INotifier notifier, string channel) : base(notifier)
    {
        _channel = channel;
    }

    public override void Send(string message)
    {
        base.Send(message);
        Console.WriteLine($"Slack 채널 '{_channel}'에 '{message}' 전송");
    }
}

// ConcreteDecorator - 카카오톡 알림 추가
public class KakaoDecorator : NotifierDecorator
{
    private readonly string _kakaoId;

    public KakaoDecorator(INotifier notifier, string kakaoId) : base(notifier)
    {
        _kakaoId = kakaoId;
    }

    public override void Send(string message)
    {
        base.Send(message);
        Console.WriteLine($"카카오톡으로 '{message}' 전송: {_kakaoId}");
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("=== 기본 이메일만 ===");
        INotifier notifier = new BasicNotifier("user@example.com");
        notifier.Send("서버 점검 알림");
        
        Console.WriteLine("\n=== 이메일 + SMS ===");
        notifier = new SMSDecorator(
            new BasicNotifier("user@example.com"),
            "010-1234-5678"
        );
        notifier.Send("긴급 알림");
        
        Console.WriteLine("\n=== 이메일 + SMS + Slack + 카카오톡 ===");
        notifier = new KakaoDecorator(
            new SlackDecorator(
                new SMSDecorator(
                    new BasicNotifier("admin@example.com"),
                    "010-9876-5432"
                ),
                "#alerts"
            ),
            "admin_kakao"
        );
        notifier.Send("시스템 장애 발생!");
    }
}
```

## 실제 사용 사례

### 1. Java I/O 스트림

Java의 I/O 라이브러리는 데코레이터 패턴의 대표적인 예이다.

```java
// 기본 스트림 + 버퍼링 + 데이터 타입 변환
DataInputStream dis = new DataInputStream(
    new BufferedInputStream(
        new FileInputStream("data.bin")
    )
);
```

### 2. Python의 함수 데코레이터

Python에서는 `@` 문법으로 데코레이터를 간편하게 적용할 수 있다.

```python
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_decorator
def say_hello(name):
    print(f"Hello, {name}!")

say_hello("World")
```

### 3. Spring Framework의 트랜잭션

Spring의 `@Transactional`은 데코레이터 패턴과 유사하게 메서드에 트랜잭션 기능을 추가한다.

### 4. GUI 컴포넌트

스크롤바, 테두리 등을 GUI 컴포넌트에 동적으로 추가하는 데 사용된다.

## 관련 패턴

| 패턴 | 데코레이터와의 관계 |
|------|-------------------|
| **Adapter** | 인터페이스를 변환하지만, Decorator는 인터페이스를 유지하면서 기능 추가 |
| **Composite** | 둘 다 재귀적 합성을 사용하지만, Decorator는 하나의 자식만 가짐 |
| **Strategy** | Decorator는 외부에서 객체를 감싸고, Strategy는 내부 알고리즘을 교체 |
| **Proxy** | 둘 다 래퍼이지만, Proxy는 동일 인터페이스로 접근을 제어 |

## FAQ

**Q1: 데코레이터 패턴과 상속의 차이점은 무엇인가요?**

상속은 컴파일 타임에 정적으로 결정되지만, 데코레이터는 런타임에 동적으로 기능을 조합할 수 있습니다. 또한 상속은 서브클래스 폭발 문제를 일으킬 수 있지만, 데코레이터는 조합으로 해결합니다.

**Q2: 데코레이터 적용 순서가 중요한가요?**

네, 순서에 따라 결과가 달라질 수 있습니다. 예를 들어 암호화 후 압축과 압축 후 암호화는 다른 결과를 만들 수 있습니다.

**Q3: 데코레이터 패턴의 단점을 어떻게 극복할 수 있나요?**

팩토리 패턴이나 빌더 패턴과 함께 사용하면 데코레이터 조합의 복잡성을 줄일 수 있습니다. 또한 설정 파일을 통해 데코레이터 조합을 관리할 수 있습니다.

**Q4: 언제 데코레이터 대신 상속을 사용해야 하나요?**

기능 확장이 고정적이고 런타임에 변경할 필요가 없다면 상속이 더 간단할 수 있습니다. 또한 기본 클래스의 구현에 강하게 의존하는 경우 상속이 더 적합할 수 있습니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns - 커피 예제
- Java I/O 라이브러리 공식 문서