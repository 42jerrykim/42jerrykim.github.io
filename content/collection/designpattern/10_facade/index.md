---
collection_order: 10
title: "[Design Pattern] Facade - 퍼사드 패턴"
description: "Facade 패턴은 복잡한 서브시스템에 간단한 인터페이스를 제공하여 클라이언트가 내부 구현에 신경 쓰지 않고 사용할 수 있게 합니다. 결합도를 낮추고 가독성을 높입니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Facade
  - 퍼사드
  - Structural Pattern
  - 구조 패턴
  - GoF
  - Gang of Four
  - Simplified Interface
  - 단순화된 인터페이스
  - Subsystem
  - 서브시스템
  - Encapsulation
  - 캡슐화
  - Loose Coupling
  - 느슨한 결합
  - High Level Interface
  - 고수준 인터페이스
  - API Gateway
  - 게이트웨이
  - Wrapper
  - 래퍼
  - Complexity Hiding
  - 복잡성 숨김
  - Library
  - 라이브러리
  - Framework
  - 프레임워크
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
  - Service Layer
  - 서비스 레이어
  - Controller
  - 컨트롤러
  - Entry Point
  - 진입점
  - Unified Interface
  - 통합 인터페이스
---

퍼사드 패턴(Facade Pattern)은 복잡한 서브시스템에 대한 단순화된 인터페이스를 제공하는 구조적 디자인 패턴이다. 건물의 정면(Facade)처럼, 복잡한 내부 구조를 숨기고 깔끔한 외관만 보여주는 역할을 한다. 클라이언트는 서브시스템의 복잡한 상호작용을 알 필요 없이 퍼사드를 통해 간단하게 기능을 사용할 수 있다.

## 개요

**퍼사드 패턴의 정의**

퍼사드 패턴은 라이브러리, 프레임워크 또는 복잡한 클래스 집합에 대한 단순화된 인터페이스를 제공한다. 서브시스템의 복잡성을 하나의 클래스 뒤로 숨겨서, 클라이언트가 쉽게 사용할 수 있도록 한다.

**패턴의 필요성 및 사용 사례**

퍼사드 패턴은 다음과 같은 상황에서 유용하다:

- **복잡한 서브시스템 단순화**: 많은 클래스와 상호작용이 필요한 작업을 하나의 메서드로 제공
- **레이어 분리**: 시스템을 레이어로 구분하고, 레이어 간 통신을 위한 진입점 제공
- **레거시 코드 래핑**: 복잡하거나 설계가 좋지 않은 레거시 코드에 깔끔한 인터페이스 제공
- **의존성 감소**: 클라이언트와 서브시스템 간의 직접적인 의존성을 줄임

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 서브시스템과 클라이언트 간 결합도 감소 | 퍼사드가 모든 클래스와 결합될 수 있음 (God Object) |
| 복잡한 작업을 간단하게 수행 가능 | 서브시스템의 모든 기능을 제공하지 못할 수 있음 |
| 클라이언트 코드의 가독성 향상 | 추가적인 추상화 레이어로 인한 오버헤드 |
| 서브시스템 변경 시 영향 최소화 | 과도한 단순화로 유연성이 제한될 수 있음 |

## 퍼사드 패턴의 구성 요소

```
┌─────────────────┐
│     Client      │
└────────┬────────┘
         │
         │ uses
         ▼
┌─────────────────────────────────────┐
│            Facade                   │
├─────────────────────────────────────┤
│ + operation()                       │
│   ├── subsystem1.method()           │
│   ├── subsystem2.method()           │
│   └── subsystem3.method()           │
└─────────────────────────────────────┘
         │
         │ delegates to
         ▼
┌─────────────────────────────────────────────────────┐
│                   Subsystem                         │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │ Class A   │  │ Class B   │  │ Class C   │  ...  │
│  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────┘
```

**1. Facade (퍼사드)**
- 서브시스템의 기능을 감싸는 단순화된 인터페이스 제공
- 클라이언트의 요청을 적절한 서브시스템 객체에 위임
- 서브시스템 클래스들의 생명주기를 관리할 수도 있음

**2. Subsystem Classes (서브시스템 클래스들)**
- 실제 기능을 구현하는 클래스들
- 퍼사드의 존재를 모르며, 서로 직접 통신
- 독립적으로도 사용 가능

**3. Client (클라이언트)**
- 퍼사드를 통해 서브시스템의 기능을 사용
- 서브시스템의 복잡한 구조를 알 필요 없음

## 구현 예제

### Python 예제 - 홈 시어터 시스템

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

# 서브시스템 클래스들
class Amplifier:
    def on(self):
        print("앰프 전원 ON")
    
    def off(self):
        print("앰프 전원 OFF")
    
    def set_volume(self, level: int):
        print(f"앰프 볼륨 설정: {level}")
    
    def set_surround_sound(self):
        print("앰프 서라운드 사운드 모드 설정")

class DVDPlayer:
    def on(self):
        print("DVD 플레이어 전원 ON")
    
    def off(self):
        print("DVD 플레이어 전원 OFF")
    
    def play(self, movie: str):
        print(f"DVD 재생: {movie}")
    
    def stop(self):
        print("DVD 정지")
    
    def eject(self):
        print("DVD 꺼냄")

class Projector:
    def on(self):
        print("프로젝터 전원 ON")
    
    def off(self):
        print("프로젝터 전원 OFF")
    
    def wide_screen_mode(self):
        print("프로젝터 와이드스크린 모드")

class TheaterLights:
    def dim(self, level: int):
        print(f"조명 밝기 조절: {level}%")
    
    def on(self):
        print("조명 ON")

class Screen:
    def down(self):
        print("스크린 내림")
    
    def up(self):
        print("스크린 올림")

class PopcornPopper:
    def on(self):
        print("팝콘 기계 ON")
    
    def off(self):
        print("팝콘 기계 OFF")
    
    def pop(self):
        print("팝콘 튀기는 중...")

# Facade 클래스
class HomeTheaterFacade:
    """홈 시어터 시스템을 위한 간단한 인터페이스 제공"""
    
    def __init__(self):
        self.amp = Amplifier()
        self.dvd = DVDPlayer()
        self.projector = Projector()
        self.lights = TheaterLights()
        self.screen = Screen()
        self.popper = PopcornPopper()
    
    def watch_movie(self, movie: str):
        """영화 시청을 위한 모든 준비를 한 번에 수행"""
        print("=== 영화 시청 준비 ===")
        self.popper.on()
        self.popper.pop()
        self.lights.dim(10)
        self.screen.down()
        self.projector.on()
        self.projector.wide_screen_mode()
        self.amp.on()
        self.amp.set_surround_sound()
        self.amp.set_volume(5)
        self.dvd.on()
        self.dvd.play(movie)
        print("=== 영화를 즐기세요! ===\n")
    
    def end_movie(self):
        """영화 종료 후 모든 장비 정리"""
        print("=== 영화 종료 ===")
        self.popper.off()
        self.lights.on()
        self.screen.up()
        self.projector.off()
        self.amp.off()
        self.dvd.stop()
        self.dvd.eject()
        self.dvd.off()
        print("=== 정리 완료 ===")

# 사용 예제
if __name__ == "__main__":
    # 퍼사드 없이 사용하면 복잡함
    # amp.on(); amp.set_surround_sound(); projector.on(); ...
    
    # 퍼사드를 사용하면 간단함
    home_theater = HomeTheaterFacade()
    home_theater.watch_movie("인셉션")
    print()
    home_theater.end_movie()
```

### Java 예제 - 컴퓨터 시작 시스템

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

// 서브시스템 클래스들
class CPU {
    public void freeze() {
        System.out.println("CPU: 프로세스 중단");
    }
    
    public void jump(long position) {
        System.out.println("CPU: 메모리 위치 " + position + "로 점프");
    }
    
    public void execute() {
        System.out.println("CPU: 명령 실행 중...");
    }
}

class Memory {
    public void load(long position, byte[] data) {
        System.out.println("Memory: 위치 " + position + "에 데이터 로드");
    }
}

class HardDrive {
    public byte[] read(long lba, int size) {
        System.out.println("HardDrive: 섹터 " + lba + "에서 " + size + " 바이트 읽기");
        return new byte[size];
    }
}

class GraphicsCard {
    public void initialize() {
        System.out.println("GraphicsCard: 초기화");
    }
    
    public void display(String message) {
        System.out.println("GraphicsCard: '" + message + "' 화면에 표시");
    }
}

class Fan {
    public void start() {
        System.out.println("Fan: 냉각 팬 시작");
    }
    
    public void stop() {
        System.out.println("Fan: 냉각 팬 정지");
    }
}

// Facade 클래스
class ComputerFacade {
    private static final long BOOT_ADDRESS = 0x00000000L;
    private static final long BOOT_SECTOR = 0L;
    private static final int SECTOR_SIZE = 512;
    
    private CPU cpu;
    private Memory memory;
    private HardDrive hardDrive;
    private GraphicsCard graphicsCard;
    private Fan fan;
    
    public ComputerFacade() {
        this.cpu = new CPU();
        this.memory = new Memory();
        this.hardDrive = new HardDrive();
        this.graphicsCard = new GraphicsCard();
        this.fan = new Fan();
    }
    
    public void start() {
        System.out.println("=== 컴퓨터 시작 ===");
        fan.start();
        graphicsCard.initialize();
        cpu.freeze();
        byte[] bootData = hardDrive.read(BOOT_SECTOR, SECTOR_SIZE);
        memory.load(BOOT_ADDRESS, bootData);
        cpu.jump(BOOT_ADDRESS);
        cpu.execute();
        graphicsCard.display("시스템 준비 완료!");
        System.out.println("=== 부팅 완료 ===\n");
    }
    
    public void shutdown() {
        System.out.println("=== 컴퓨터 종료 ===");
        graphicsCard.display("시스템을 종료합니다...");
        cpu.freeze();
        fan.stop();
        System.out.println("=== 종료 완료 ===");
    }
}

// 사용 예제
public class FacadeDemo {
    public static void main(String[] args) {
        ComputerFacade computer = new ComputerFacade();
        
        // 복잡한 부팅 과정을 한 줄로 수행
        computer.start();
        
        // 종료도 간단하게
        computer.shutdown();
    }
}
```

### C# 예제 - 온라인 쇼핑 주문 시스템

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;

// 서브시스템 클래스들
public class InventoryService
{
    public bool CheckStock(string productId, int quantity)
    {
        Console.WriteLine($"재고 확인: {productId} x {quantity}");
        return true; // 재고 있음으로 가정
    }
    
    public void ReserveStock(string productId, int quantity)
    {
        Console.WriteLine($"재고 예약: {productId} x {quantity}");
    }
}

public class PaymentService
{
    public bool ProcessPayment(string cardNumber, decimal amount)
    {
        Console.WriteLine($"결제 처리: {amount:C} (카드: {MaskCardNumber(cardNumber)})");
        return true; // 결제 성공으로 가정
    }
    
    private string MaskCardNumber(string cardNumber)
    {
        return "****-****-****-" + cardNumber.Substring(cardNumber.Length - 4);
    }
}

public class ShippingService
{
    public string CreateShipment(string address, string productId)
    {
        string trackingNumber = Guid.NewGuid().ToString().Substring(0, 8).ToUpper();
        Console.WriteLine($"배송 생성: {productId} -> {address}");
        Console.WriteLine($"운송장 번호: {trackingNumber}");
        return trackingNumber;
    }
}

public class NotificationService
{
    public void SendEmail(string email, string subject, string body)
    {
        Console.WriteLine($"이메일 발송: {email}");
        Console.WriteLine($"제목: {subject}");
    }
    
    public void SendSMS(string phone, string message)
    {
        Console.WriteLine($"SMS 발송: {phone}");
    }
}

public class OrderLoggingService
{
    public void LogOrder(string orderId, string status)
    {
        Console.WriteLine($"[LOG] 주문 {orderId}: {status} - {DateTime.Now}");
    }
}

// Facade 클래스
public class OrderFacade
{
    private readonly InventoryService _inventory;
    private readonly PaymentService _payment;
    private readonly ShippingService _shipping;
    private readonly NotificationService _notification;
    private readonly OrderLoggingService _logging;
    
    public OrderFacade()
    {
        _inventory = new InventoryService();
        _payment = new PaymentService();
        _shipping = new ShippingService();
        _notification = new NotificationService();
        _logging = new OrderLoggingService();
    }
    
    public bool PlaceOrder(
        string productId, 
        int quantity, 
        string cardNumber, 
        decimal amount,
        string shippingAddress,
        string email,
        string phone)
    {
        string orderId = Guid.NewGuid().ToString().Substring(0, 8).ToUpper();
        Console.WriteLine($"\n=== 주문 처리 시작: {orderId} ===\n");
        
        // 1. 재고 확인
        if (!_inventory.CheckStock(productId, quantity))
        {
            _logging.LogOrder(orderId, "재고 부족으로 실패");
            return false;
        }
        
        // 2. 재고 예약
        _inventory.ReserveStock(productId, quantity);
        
        // 3. 결제 처리
        if (!_payment.ProcessPayment(cardNumber, amount))
        {
            _logging.LogOrder(orderId, "결제 실패");
            return false;
        }
        
        // 4. 배송 생성
        string trackingNumber = _shipping.CreateShipment(shippingAddress, productId);
        
        // 5. 알림 발송
        _notification.SendEmail(email, "주문 확인", $"주문이 완료되었습니다. 운송장: {trackingNumber}");
        _notification.SendSMS(phone, $"주문완료! 운송장: {trackingNumber}");
        
        // 6. 로깅
        _logging.LogOrder(orderId, "주문 완료");
        
        Console.WriteLine($"\n=== 주문 처리 완료: {orderId} ===\n");
        return true;
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        OrderFacade orderFacade = new OrderFacade();
        
        // 퍼사드를 사용하면 복잡한 주문 프로세스를 한 번의 호출로 처리
        bool success = orderFacade.PlaceOrder(
            productId: "LAPTOP-001",
            quantity: 1,
            cardNumber: "1234567890123456",
            amount: 1500000m,
            shippingAddress: "서울시 강남구 테헤란로 123",
            email: "customer@example.com",
            phone: "010-1234-5678"
        );
        
        Console.WriteLine(success ? "주문이 성공적으로 처리되었습니다." : "주문 처리에 실패했습니다.");
    }
}
```

## 실제 사용 사례

### 1. SLF4J (Simple Logging Facade for Java)

다양한 로깅 프레임워크(Log4j, Logback 등)에 대한 통합 인터페이스를 제공한다.

```java
// 다양한 로깅 구현체를 동일한 인터페이스로 사용
Logger logger = LoggerFactory.getLogger(MyClass.class);
logger.info("This is a log message");
```

### 2. jQuery

복잡한 DOM 조작과 AJAX 호출을 단순화한 퍼사드를 제공한다.

```javascript
// 복잡한 DOM API 대신 간단한 jQuery 인터페이스
$('#element').fadeIn().css('color', 'red').text('Hello');
```

### 3. 스프링 프레임워크의 JdbcTemplate

JDBC의 복잡한 연결/자원 관리를 숨기고 간단한 인터페이스를 제공한다.

```java
// 복잡한 Connection, Statement, ResultSet 관리를 숨김
List<User> users = jdbcTemplate.query("SELECT * FROM users", rowMapper);
```

### 4. API Gateway

마이크로서비스 아키텍처에서 여러 서비스에 대한 단일 진입점을 제공한다.

## 관련 패턴

| 패턴 | 퍼사드와의 관계 |
|------|----------------|
| **Adapter** | Adapter는 인터페이스를 변환하고, Facade는 복잡성을 숨김 |
| **Mediator** | 둘 다 협력을 중재하지만, Mediator는 양방향, Facade는 단방향 |
| **Singleton** | Facade가 하나만 필요한 경우 싱글턴으로 구현하기도 함 |
| **Abstract Factory** | 서브시스템 객체 생성을 Facade가 팩토리에 위임할 수 있음 |

## FAQ

**Q1: 퍼사드 패턴과 래퍼 클래스의 차이점은 무엇인가요?**

래퍼는 보통 하나의 객체를 감싸지만, 퍼사드는 여러 객체와 상호작용하는 전체 서브시스템에 대한 인터페이스를 제공합니다. 또한 퍼사드는 새로운 기능을 추가하기보다는 기존 기능에 대한 단순화된 접근을 제공합니다.

**Q2: 퍼사드를 사용하면 서브시스템 클래스에 직접 접근할 수 없나요?**

퍼사드는 서브시스템에 대한 직접 접근을 막지 않습니다. 필요하면 클라이언트가 서브시스템 클래스를 직접 사용할 수 있습니다. 퍼사드는 선택적인 단순화된 인터페이스를 제공하는 것이지, 유일한 접근점을 강제하지 않습니다.

**Q3: 퍼사드가 너무 많은 책임을 가지면 어떻게 하나요?**

퍼사드가 God Object가 되는 것을 피하려면, 기능별로 여러 개의 퍼사드로 분리하거나, 서브시스템 자체를 재구성하는 것을 고려해야 합니다.

**Q4: 퍼사드와 서비스 레이어의 차이점은 무엇인가요?**

서비스 레이어는 비즈니스 로직을 캡슐화하는 아키텍처 패턴이고, 퍼사드는 복잡한 인터페이스를 단순화하는 디자인 패턴입니다. 서비스 레이어가 퍼사드 패턴을 사용하여 구현될 수 있습니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- Martin Fowler의 Patterns of Enterprise Application Architecture