---
collection_order: 7
title: "[Design Pattern] Bridge - 브릿지 패턴"
description: "Bridge 패턴은 구현부와 추상부를 분리하여 독립적으로 확장 가능하게 하는 구조적 패턴입니다. 다양한 구현체와 추상을 조합해 복잡한 기능 변경을 쉽게 처리합니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Bridge
  - 브릿지
  - Structural Pattern
  - 구조 패턴
  - GoF
  - Gang of Four
  - Abstraction
  - 추상화
  - Implementation
  - 구현
  - Decoupling
  - 분리
  - Separation of Concerns
  - 관심사 분리
  - Refined Abstraction
  - 정제된 추상화
  - Concrete Implementation
  - 구체적 구현
  - Composition over Inheritance
  - 상속보다 합성
  - Flexibility
  - 유연성
  - Extensibility
  - 확장성
  - Platform Independence
  - 플랫폼 독립성
  - Driver
  - 드라이버
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
  - Runtime Binding
  - 런타임 바인딩
  - Interface
  - 인터페이스
  - Delegation
  - 위임
  - Cross Platform
  - 크로스 플랫폼
---

브릿지 패턴(Bridge Pattern)은 추상화(Abstraction)와 구현(Implementation)을 분리하여 각각 독립적으로 변형할 수 있게 하는 구조적 디자인 패턴이다. 이 패턴은 상속 대신 합성을 사용하여 두 차원의 변화를 독립적으로 관리할 수 있게 해주며, 런타임에 구현을 교체할 수 있는 유연성을 제공한다.

## 개요

**브릿지 패턴의 정의**

브릿지 패턴은 하나의 추상적 개념에 대해 여러 구현이 가능할 때, 추상화 계층과 구현 계층을 분리하여 별도의 클래스 계층으로 발전시키는 패턴이다. 이 두 계층은 "브릿지"를 통해 연결되어, 서로 독립적으로 확장될 수 있다.

**패턴의 필요성 및 사용 사례**

브릿지 패턴은 다음과 같은 상황에서 유용하다:

- **다차원 확장**: 추상화와 구현 두 방향으로 확장이 필요할 때
- **플랫폼 독립성**: 동일한 추상화를 다양한 플랫폼에서 사용해야 할 때
- **구현 교체**: 런타임에 구현을 동적으로 변경해야 할 때
- **클래스 폭발 방지**: 상속으로 인한 서브클래스 급증을 방지하고 싶을 때

**클래스 폭발 문제 예시**

상속만 사용할 경우:
```
Shape
├── Circle
│   ├── RedCircle
│   ├── BlueCircle
│   └── GreenCircle
├── Square
│   ├── RedSquare
│   ├── BlueSquare
│   └── GreenSquare
└── ...
```

브릿지 패턴 사용 시:
```
Shape (추상화)        Color (구현)
├── Circle            ├── Red
├── Square            ├── Blue
└── ...               └── Green
```

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 추상화와 구현의 독립적 확장 | 복잡성 증가 (클래스 수 증가) |
| 런타임 구현 교체 가능 | 단일 차원 변화에는 과도한 설계 |
| 클래스 폭발 문제 해결 | 초기 설계 비용 증가 |
| 플랫폼 독립적 코드 작성 가능 | 이해하기 어려울 수 있음 |

## 브릿지 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│          Abstraction                │
├─────────────────────────────────────┤
│ - implementor: Implementor          │
├─────────────────────────────────────┤
│ + operation()                       │
│   └── implementor.operationImpl()   │
└─────────────────────────────────────┘
              │
              │ has-a (bridge)
              ▼
┌─────────────────────────────────────┐
│       <<interface>>                 │
│        Implementor                  │
├─────────────────────────────────────┤
│ + operationImpl()                   │
└─────────────────────────────────────┘
              △
              │
     ┌────────┴────────┐
     │                 │
┌─────────────┐  ┌─────────────┐
│ ConcreteA   │  │ ConcreteB   │
├─────────────┤  ├─────────────┤
│+operationIm │  │+operationIm │
└─────────────┘  └─────────────┘
```

**1. Abstraction (추상화)**
- 고수준의 제어 로직 정의
- Implementor에 대한 참조 유지
- 클라이언트가 사용하는 인터페이스

**2. RefinedAbstraction (정제된 추상화)**
- Abstraction을 확장한 변형
- 추가적인 고수준 기능 제공

**3. Implementor (구현자)**
- 구현 클래스들의 인터페이스 정의
- Abstraction과 다른 인터페이스를 가질 수 있음

**4. ConcreteImplementor (구체적 구현자)**
- Implementor 인터페이스의 구체적 구현
- 플랫폼별 또는 특정 방식의 구현

## 구현 예제

### Python 예제 - 리모컨과 디바이스

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod

# Implementor - 디바이스 인터페이스
class Device(ABC):
    @abstractmethod
    def is_enabled(self) -> bool:
        pass
    
    @abstractmethod
    def enable(self) -> None:
        pass
    
    @abstractmethod
    def disable(self) -> None:
        pass
    
    @abstractmethod
    def get_volume(self) -> int:
        pass
    
    @abstractmethod
    def set_volume(self, volume: int) -> None:
        pass
    
    @abstractmethod
    def get_channel(self) -> int:
        pass
    
    @abstractmethod
    def set_channel(self, channel: int) -> None:
        pass

# ConcreteImplementor - TV
class TV(Device):
    def __init__(self):
        self._on = False
        self._volume = 30
        self._channel = 1
    
    def is_enabled(self) -> bool:
        return self._on
    
    def enable(self) -> None:
        self._on = True
        print("TV: 전원 켜짐")
    
    def disable(self) -> None:
        self._on = False
        print("TV: 전원 꺼짐")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, volume: int) -> None:
        self._volume = max(0, min(100, volume))
        print(f"TV: 볼륨 {self._volume}")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int) -> None:
        self._channel = channel
        print(f"TV: 채널 {self._channel}")

# ConcreteImplementor - Radio
class Radio(Device):
    def __init__(self):
        self._on = False
        self._volume = 20
        self._channel = 87  # FM 주파수
    
    def is_enabled(self) -> bool:
        return self._on
    
    def enable(self) -> None:
        self._on = True
        print("Radio: 전원 켜짐")
    
    def disable(self) -> None:
        self._on = False
        print("Radio: 전원 꺼짐")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, volume: int) -> None:
        self._volume = max(0, min(100, volume))
        print(f"Radio: 볼륨 {self._volume}")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int) -> None:
        self._channel = channel
        print(f"Radio: FM {self._channel}")

# Abstraction - 기본 리모컨
class RemoteControl:
    def __init__(self, device: Device):
        self._device = device
    
    def toggle_power(self) -> None:
        if self._device.is_enabled():
            self._device.disable()
        else:
            self._device.enable()
    
    def volume_up(self) -> None:
        self._device.set_volume(self._device.get_volume() + 10)
    
    def volume_down(self) -> None:
        self._device.set_volume(self._device.get_volume() - 10)
    
    def channel_up(self) -> None:
        self._device.set_channel(self._device.get_channel() + 1)
    
    def channel_down(self) -> None:
        self._device.set_channel(self._device.get_channel() - 1)

# RefinedAbstraction - 고급 리모컨
class AdvancedRemoteControl(RemoteControl):
    def mute(self) -> None:
        self._device.set_volume(0)
        print("음소거 활성화")
    
    def set_channel_direct(self, channel: int) -> None:
        self._device.set_channel(channel)
        print(f"채널 {channel}로 직접 이동")

# 사용 예제
if __name__ == "__main__":
    print("=== TV with Basic Remote ===")
    tv = TV()
    tv_remote = RemoteControl(tv)
    tv_remote.toggle_power()
    tv_remote.volume_up()
    tv_remote.channel_up()
    
    print("\n=== Radio with Advanced Remote ===")
    radio = Radio()
    radio_remote = AdvancedRemoteControl(radio)
    radio_remote.toggle_power()
    radio_remote.set_channel_direct(91)
    radio_remote.mute()
    
    print("\n=== TV with Advanced Remote ===")
    tv_advanced = AdvancedRemoteControl(tv)
    tv_advanced.set_channel_direct(5)
    tv_advanced.mute()
```

### Java 예제 - 도형과 색상

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

// Implementor - 색상 인터페이스
interface Color {
    String fill();
    String getColorName();
}

// ConcreteImplementor - Red
class Red implements Color {
    @Override
    public String fill() {
        return "빨간색으로 채우기";
    }
    
    @Override
    public String getColorName() {
        return "빨간색";
    }
}

// ConcreteImplementor - Blue
class Blue implements Color {
    @Override
    public String fill() {
        return "파란색으로 채우기";
    }
    
    @Override
    public String getColorName() {
        return "파란색";
    }
}

// ConcreteImplementor - Green
class Green implements Color {
    @Override
    public String fill() {
        return "초록색으로 채우기";
    }
    
    @Override
    public String getColorName() {
        return "초록색";
    }
}

// Abstraction - 도형
abstract class Shape {
    protected Color color;  // Bridge
    
    public Shape(Color color) {
        this.color = color;
    }
    
    abstract void draw();
    abstract String getName();
}

// RefinedAbstraction - Circle
class Circle extends Shape {
    private int radius;
    
    public Circle(int radius, Color color) {
        super(color);
        this.radius = radius;
    }
    
    @Override
    void draw() {
        System.out.println("원 그리기 (반지름: " + radius + ")");
        System.out.println("  " + color.fill());
    }
    
    @Override
    String getName() {
        return color.getColorName() + " 원";
    }
}

// RefinedAbstraction - Rectangle
class Rectangle extends Shape {
    private int width;
    private int height;
    
    public Rectangle(int width, int height, Color color) {
        super(color);
        this.width = width;
        this.height = height;
    }
    
    @Override
    void draw() {
        System.out.println("사각형 그리기 (" + width + " x " + height + ")");
        System.out.println("  " + color.fill());
    }
    
    @Override
    String getName() {
        return color.getColorName() + " 사각형";
    }
}

// RefinedAbstraction - Triangle
class Triangle extends Shape {
    public Triangle(Color color) {
        super(color);
    }
    
    @Override
    void draw() {
        System.out.println("삼각형 그리기");
        System.out.println("  " + color.fill());
    }
    
    @Override
    String getName() {
        return color.getColorName() + " 삼각형";
    }
}

// 사용 예제
public class BridgeDemo {
    public static void main(String[] args) {
        // 다양한 도형과 색상 조합
        Shape[] shapes = {
            new Circle(10, new Red()),
            new Circle(5, new Blue()),
            new Rectangle(4, 6, new Green()),
            new Triangle(new Red())
        };
        
        System.out.println("=== 도형 그리기 ===\n");
        for (Shape shape : shapes) {
            System.out.println(shape.getName() + ":");
            shape.draw();
            System.out.println();
        }
    }
}
```

### C# 예제 - 메시지와 발송 방법

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;

// Implementor - 메시지 발송 인터페이스
public interface IMessageSender
{
    void Send(string title, string body);
    string GetSenderType();
}

// ConcreteImplementor - Email
public class EmailSender : IMessageSender
{
    private readonly string _smtpServer;
    
    public EmailSender(string smtpServer)
    {
        _smtpServer = smtpServer;
    }
    
    public void Send(string title, string body)
    {
        Console.WriteLine($"[EMAIL via {_smtpServer}]");
        Console.WriteLine($"제목: {title}");
        Console.WriteLine($"내용: {body}");
    }
    
    public string GetSenderType() => "이메일";
}

// ConcreteImplementor - SMS
public class SmsSender : IMessageSender
{
    private readonly string _phoneNumber;
    
    public SmsSender(string phoneNumber)
    {
        _phoneNumber = phoneNumber;
    }
    
    public void Send(string title, string body)
    {
        Console.WriteLine($"[SMS to {_phoneNumber}]");
        Console.WriteLine($"{title}: {body}");
    }
    
    public string GetSenderType() => "SMS";
}

// ConcreteImplementor - Push Notification
public class PushSender : IMessageSender
{
    private readonly string _appId;
    
    public PushSender(string appId)
    {
        _appId = appId;
    }
    
    public void Send(string title, string body)
    {
        Console.WriteLine($"[PUSH via App: {_appId}]");
        Console.WriteLine($"📱 {title}");
        Console.WriteLine($"   {body}");
    }
    
    public string GetSenderType() => "푸시 알림";
}

// Abstraction - 메시지
public abstract class Message
{
    protected IMessageSender Sender;  // Bridge
    
    public Message(IMessageSender sender)
    {
        Sender = sender;
    }
    
    public abstract void Send();
}

// RefinedAbstraction - 일반 메시지
public class TextMessage : Message
{
    private readonly string _content;
    
    public TextMessage(IMessageSender sender, string content) : base(sender)
    {
        _content = content;
    }
    
    public override void Send()
    {
        Sender.Send("일반 메시지", _content);
    }
}

// RefinedAbstraction - 긴급 메시지
public class UrgentMessage : Message
{
    private readonly string _content;
    
    public UrgentMessage(IMessageSender sender, string content) : base(sender)
    {
        _content = content;
    }
    
    public override void Send()
    {
        string urgentTitle = "🚨 [긴급] 🚨";
        string urgentContent = $"*** 긴급 ***\n{_content}\n*** 즉시 확인 요망 ***";
        Sender.Send(urgentTitle, urgentContent);
    }
}

// RefinedAbstraction - 예약 메시지
public class ScheduledMessage : Message
{
    private readonly string _content;
    private readonly DateTime _scheduledTime;
    
    public ScheduledMessage(IMessageSender sender, string content, DateTime scheduledTime) 
        : base(sender)
    {
        _content = content;
        _scheduledTime = scheduledTime;
    }
    
    public override void Send()
    {
        Console.WriteLine($"[예약됨: {_scheduledTime:yyyy-MM-dd HH:mm}]");
        Sender.Send("예약 메시지", _content);
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        // 발송 방법들
        var emailSender = new EmailSender("smtp.example.com");
        var smsSender = new SmsSender("010-1234-5678");
        var pushSender = new PushSender("com.myapp");
        
        Console.WriteLine("=== 이메일로 긴급 메시지 ===");
        var urgentEmail = new UrgentMessage(emailSender, "서버가 다운되었습니다!");
        urgentEmail.Send();
        
        Console.WriteLine("\n=== SMS로 일반 메시지 ===");
        var textSms = new TextMessage(smsSender, "회의가 30분 후에 시작됩니다.");
        textSms.Send();
        
        Console.WriteLine("\n=== 푸시로 예약 메시지 ===");
        var scheduledPush = new ScheduledMessage(
            pushSender, 
            "오늘의 할인 이벤트를 확인하세요!", 
            DateTime.Now.AddHours(2)
        );
        scheduledPush.Send();
        
        Console.WriteLine("\n=== 푸시로 긴급 메시지 ===");
        var urgentPush = new UrgentMessage(pushSender, "결제가 완료되었습니다.");
        urgentPush.Send();
    }
}
```

## 실제 사용 사례

### 1. JDBC Driver
Java의 JDBC는 브릿지 패턴의 대표적 예이다. `DriverManager`(Abstraction)가 다양한 데이터베이스 드라이버(Implementation)를 연결한다.

### 2. GUI 프레임워크
Java AWT/Swing에서 `Window` 추상화는 다양한 OS 플랫폼의 네이티브 윈도우 구현과 분리되어 있다.

### 3. 크로스 플랫폼 앱
React Native, Flutter 등은 추상적인 UI 컴포넌트가 플랫폼별 네이티브 구현에 위임하는 브릿지 구조를 사용한다.

### 4. 로깅 프레임워크
SLF4J는 추상 로깅 API를 제공하고, 다양한 로깅 구현(Logback, Log4j 등)에 연결할 수 있다.

## 관련 패턴

| 패턴 | 브릿지와의 관계 |
|------|---------------|
| **Adapter** | Adapter는 기존 인터페이스를 변환, Bridge는 설계 초기부터 분리 |
| **Abstract Factory** | 브릿지의 구현 객체를 생성하는 데 사용될 수 있음 |
| **Strategy** | 둘 다 합성을 사용하지만, Strategy는 알고리즘 교체에 초점 |

## FAQ

**Q1: 브릿지 패턴과 어댑터 패턴의 차이점은 무엇인가요?**

어댑터 패턴은 이미 존재하는 두 인터페이스 사이의 호환성 문제를 해결하는 반면, 브릿지 패턴은 설계 초기부터 추상화와 구현을 분리하여 독립적으로 발전시키기 위해 사용됩니다.

**Q2: 언제 브릿지 패턴을 사용해야 하나요?**

두 개 이상의 독립적인 차원으로 클래스가 확장될 때, 또는 런타임에 구현을 전환해야 할 때 사용합니다. 단일 차원 변화에는 불필요하게 복잡할 수 있습니다.

**Q3: 브릿지 패턴에서 Abstraction과 Implementation의 인터페이스가 동일해야 하나요?**

아닙니다. 오히려 다른 경우가 많습니다. Abstraction은 고수준 기능을, Implementation은 저수준 기본 연산을 정의합니다.

**Q4: 브릿지 패턴을 사용하면 성능에 영향이 있나요?**

추가적인 간접 호출이 있지만, 대부분의 경우 무시할 수 있는 수준입니다. 설계의 유연성으로 인한 이점이 더 큽니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- JDBC API 문서