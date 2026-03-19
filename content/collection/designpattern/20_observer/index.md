---
collection_order: 20
title: "[Design Pattern] Observer - 옵저버 패턴"
description: "Observer 패턴은 객체의 상태 변화가 있을 때 의존 객체들에게 자동으로 알림을 보냅니다. 객체 간 결합도를 낮추고 효율적으로 이벤트를 전달하여 확장성을 높입니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design-Pattern
  - 디자인패턴
  - Observer
  - GoF
  - Implementation
  - Software-Architecture
  - Code-Quality
  - 코드품질
  - 소프트웨어아키텍처
  - OOP
  - 객체지향
  - Java
  - C++
  - Python
  - CSharp
  - Git
  - GitHub
  - 구현
  - Queue
  - Memory
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Refactoring
  - 리팩토링
  - Documentation
  - 문서화
  - Interface
  - 인터페이스
  - Abstraction
  - 추상화
  - SOLID
  - Encapsulation
  - 캡슐화
  - Polymorphism
  - 다형성
  - Composition
  - 합성
  - Dependency-Injection
  - 의존성주입
  - Testing
  - 테스트
  - Performance
  - 성능
  - Education
  - 교육
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
---

옵저버 패턴(Observer Pattern)은 객체 사이에 일대다(one-to-many) 의존 관계를 정의하여, 어떤 객체의 상태가 변할 때 그 객체에 의존하는 모든 객체에게 자동으로 알림을 보내고 갱신하는 행위 디자인 패턴이다. 발행-구독(Pub-Sub) 패턴이라고도 불리며, 이벤트 기반 시스템의 핵심 패턴이다.

## 개요

**옵저버 패턴의 정의**

옵저버 패턴은 주체(Subject)와 관찰자(Observer) 사이의 느슨한 결합을 제공한다. 주체는 자신의 상태가 변경되면 등록된 모든 관찰자에게 알림을 보내고, 관찰자들은 이 알림을 받아 적절한 동작을 수행한다.

**패턴의 필요성 및 사용 사례**

옵저버 패턴은 다음과 같은 상황에서 유용하다:

- **이벤트 시스템**: GUI 이벤트 처리, 사용자 입력 처리
- **데이터 바인딩**: 모델 변경 시 뷰 자동 갱신 (MVC 패턴)
- **실시간 업데이트**: 주식 가격, 날씨 정보, 소셜 미디어 피드
- **분산 시스템**: 메시지 큐, 이벤트 버스
- **느슨한 결합**: 객체 간 직접 의존성을 제거하고 싶을 때

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 느슨한 결합 (Subject와 Observer 독립) | Observer가 많으면 알림 비용 증가 |
| 런타임에 Observer 추가/제거 가능 | 알림 순서가 보장되지 않을 수 있음 |
| 개방-폐쇄 원칙 준수 | 메모리 누수 위험 (구독 해제 누락) |
| 브로드캐스트 통신 지원 | 복잡한 의존성 추적이 어려움 |

## 옵저버 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│           Subject                   │
├─────────────────────────────────────┤
│ - observers: List<Observer>         │
├─────────────────────────────────────┤
│ + attach(Observer)                  │
│ + detach(Observer)                  │
│ + notify()                          │
│   └── for each observer:            │
│       observer.update()             │
└─────────────────────────────────────┘
              │
              │ notifies
              ▼
┌─────────────────────────────────────┐
│       <<interface>>                 │
│          Observer                   │
├─────────────────────────────────────┤
│ + update()                          │
└─────────────────────────────────────┘
              △
              │
     ┌────────┴────────┐
     │                 │
┌───────────────┐  ┌───────────────┐
│ ConcreteObsA  │  │ ConcreteObsB  │
├───────────────┤  ├───────────────┤
│ + update()    │  │ + update()    │
└───────────────┘  └───────────────┘
```

**1. Subject (주체)**
- Observer들의 목록을 관리
- Observer 등록(attach), 해제(detach), 알림(notify) 메서드 제공
- 상태 변경 시 모든 Observer에게 알림

**2. Observer (관찰자)**
- 주체로부터 알림을 받는 인터페이스
- update() 메서드를 통해 상태 변경 통지 수신

**3. ConcreteSubject (구체적 주체)**
- 실제 상태를 보유하고 변경되면 Observer에게 알림
- getState(), setState() 등의 메서드 제공

**4. ConcreteObserver (구체적 관찰자)**
- Subject의 상태 변화에 반응하는 실제 구현
- Subject 참조를 통해 필요한 정보 획득

## 푸시 vs 풀 모델

### 푸시 모델 (Push Model)
Subject가 변경된 데이터를 Observer에게 직접 전달

```python
# Subject가 데이터를 직접 전달
observer.update(temperature, humidity, pressure)
```

### 풀 모델 (Pull Model)
Observer가 필요한 데이터를 Subject로부터 직접 가져옴

```python
# Observer가 필요한 데이터를 요청
def update(self, subject):
    temp = subject.get_temperature()
```

## 구현 예제

### Python 예제 - 날씨 모니터링

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import List

# Observer 인터페이스
class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        pass

# Subject 인터페이스
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass
    
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass
    
    @abstractmethod
    def notify(self) -> None:
        pass

# ConcreteSubject - 날씨 데이터
class WeatherStation(Subject):
    def __init__(self):
        self._observers: List[Observer] = []
        self._temperature: float = 0.0
        self._humidity: float = 0.0
        self._pressure: float = 0.0
    
    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Observer 등록됨: {observer.__class__.__name__}")
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
        print(f"Observer 해제됨: {observer.__class__.__name__}")
    
    def notify(self) -> None:
        print("\n날씨 데이터 업데이트 알림 전송 중...")
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)
    
    def set_measurements(self, temp: float, humidity: float, pressure: float) -> None:
        print(f"\n=== 새로운 측정값: 온도={temp}°C, 습도={humidity}%, 기압={pressure}hPa ===")
        self._temperature = temp
        self._humidity = humidity
        self._pressure = pressure
        self.notify()

# ConcreteObserver - 현재 날씨 표시
class CurrentConditionsDisplay(Observer):
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        print(f"[현재 날씨] 온도: {temperature}°C | 습도: {humidity}%")

# ConcreteObserver - 통계 표시
class StatisticsDisplay(Observer):
    def __init__(self):
        self._temperatures: List[float] = []
    
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        self._temperatures.append(temperature)
        avg = sum(self._temperatures) / len(self._temperatures)
        max_temp = max(self._temperatures)
        min_temp = min(self._temperatures)
        print(f"[통계] 평균: {avg:.1f}°C | 최고: {max_temp}°C | 최저: {min_temp}°C")

# ConcreteObserver - 예보 표시
class ForecastDisplay(Observer):
    def __init__(self):
        self._last_pressure: float = 0.0
    
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        if pressure > self._last_pressure:
            forecast = "맑은 날씨가 예상됩니다"
        elif pressure < self._last_pressure:
            forecast = "비가 올 수 있습니다"
        else:
            forecast = "현재 날씨가 유지될 것입니다"
        
        self._last_pressure = pressure
        print(f"[예보] {forecast}")

# 사용 예제
if __name__ == "__main__":
    # Subject 생성
    weather_station = WeatherStation()
    
    # Observer 생성 및 등록
    current_display = CurrentConditionsDisplay()
    stats_display = StatisticsDisplay()
    forecast_display = ForecastDisplay()
    
    weather_station.attach(current_display)
    weather_station.attach(stats_display)
    weather_station.attach(forecast_display)
    
    # 날씨 데이터 변경 (자동으로 모든 Observer에게 알림)
    weather_station.set_measurements(25.0, 65.0, 1013.0)
    weather_station.set_measurements(27.5, 70.0, 1010.0)
    weather_station.set_measurements(23.0, 80.0, 1015.0)
    
    # Observer 해제
    print()
    weather_station.detach(forecast_display)
    weather_station.set_measurements(22.0, 75.0, 1012.0)
```

### Java 예제 - 뉴스 구독 시스템

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// Observer 인터페이스
interface Subscriber {
    void update(String news, String category);
}

// Subject 인터페이스
interface Publisher {
    void subscribe(Subscriber subscriber);
    void unsubscribe(Subscriber subscriber);
    void notifySubscribers(String news, String category);
}

// ConcreteSubject - 뉴스 에이전시
class NewsAgency implements Publisher {
    private List<Subscriber> subscribers = new ArrayList<>();
    private Map<Subscriber, Set<String>> categoryPreferences = new HashMap<>();
    
    @Override
    public void subscribe(Subscriber subscriber) {
        subscribers.add(subscriber);
        categoryPreferences.put(subscriber, new HashSet<>());
        System.out.println("새 구독자 등록: " + subscriber.getClass().getSimpleName());
    }
    
    public void subscribeToCategory(Subscriber subscriber, String category) {
        if (categoryPreferences.containsKey(subscriber)) {
            categoryPreferences.get(subscriber).add(category);
            System.out.println(subscriber.getClass().getSimpleName() + "이(가) " + category + " 카테고리 구독");
        }
    }
    
    @Override
    public void unsubscribe(Subscriber subscriber) {
        subscribers.remove(subscriber);
        categoryPreferences.remove(subscriber);
    }
    
    @Override
    public void notifySubscribers(String news, String category) {
        System.out.println("\n[뉴스 발행] " + category + ": " + news);
        for (Subscriber subscriber : subscribers) {
            Set<String> prefs = categoryPreferences.get(subscriber);
            if (prefs.isEmpty() || prefs.contains(category)) {
                subscriber.update(news, category);
            }
        }
    }
    
    public void publishNews(String news, String category) {
        notifySubscribers(news, category);
    }
}

// ConcreteObserver - 이메일 구독자
class EmailSubscriber implements Subscriber {
    private String email;
    
    public EmailSubscriber(String email) {
        this.email = email;
    }
    
    @Override
    public void update(String news, String category) {
        System.out.println("  📧 " + email + "로 이메일 발송: [" + category + "] " + news);
    }
}

// ConcreteObserver - 앱 알림 구독자
class AppNotificationSubscriber implements Subscriber {
    private String userId;
    
    public AppNotificationSubscriber(String userId) {
        this.userId = userId;
    }
    
    @Override
    public void update(String news, String category) {
        System.out.println("  📱 " + userId + " 앱 알림: [" + category + "] " + news);
    }
}

// ConcreteObserver - SMS 구독자
class SMSSubscriber implements Subscriber {
    private String phoneNumber;
    
    public SMSSubscriber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }
    
    @Override
    public void update(String news, String category) {
        System.out.println("  💬 " + phoneNumber + "로 SMS: [" + category + "] " + news);
    }
}

// 사용 예제
public class ObserverDemo {
    public static void main(String[] args) {
        NewsAgency newsAgency = new NewsAgency();
        
        // 구독자 생성
        Subscriber emailSub = new EmailSubscriber("user@example.com");
        Subscriber appSub = new AppNotificationSubscriber("user123");
        Subscriber smsSub = new SMSSubscriber("010-1234-5678");
        
        // 기본 구독
        newsAgency.subscribe(emailSub);
        newsAgency.subscribe(appSub);
        newsAgency.subscribe(smsSub);
        
        // 카테고리별 구독 설정
        newsAgency.subscribeToCategory(emailSub, "스포츠");
        newsAgency.subscribeToCategory(emailSub, "경제");
        newsAgency.subscribeToCategory(smsSub, "속보");
        // appSub는 모든 카테고리 수신
        
        // 뉴스 발행
        newsAgency.publishNews("주가 2% 상승", "경제");
        newsAgency.publishNews("월드컵 한국 승리!", "스포츠");
        newsAgency.publishNews("긴급 재난 문자", "속보");
        newsAgency.publishNews("맛집 탐방기", "라이프");
    }
}
```

### C# 예제 - 주식 가격 모니터링

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;
using System.Collections.Generic;

// 주식 정보 클래스
public class StockInfo
{
    public string Symbol { get; set; }
    public decimal Price { get; set; }
    public decimal Change { get; set; }
    public decimal ChangePercent => Price != 0 ? (Change / (Price - Change)) * 100 : 0;
}

// Observer 인터페이스
public interface IStockObserver
{
    void OnStockUpdate(StockInfo stock);
}

// Subject - 주식 시장
public class StockMarket
{
    private Dictionary<string, List<IStockObserver>> _observers = new Dictionary<string, List<IStockObserver>>();
    private Dictionary<string, StockInfo> _stocks = new Dictionary<string, StockInfo>();
    
    public void Subscribe(string symbol, IStockObserver observer)
    {
        if (!_observers.ContainsKey(symbol))
        {
            _observers[symbol] = new List<IStockObserver>();
        }
        
        if (!_observers[symbol].Contains(observer))
        {
            _observers[symbol].Add(observer);
            Console.WriteLine($"{observer.GetType().Name}이(가) {symbol} 구독");
        }
    }
    
    public void Unsubscribe(string symbol, IStockObserver observer)
    {
        if (_observers.ContainsKey(symbol))
        {
            _observers[symbol].Remove(observer);
        }
    }
    
    public void UpdateStock(string symbol, decimal newPrice)
    {
        decimal oldPrice = _stocks.ContainsKey(symbol) ? _stocks[symbol].Price : newPrice;
        
        var stockInfo = new StockInfo
        {
            Symbol = symbol,
            Price = newPrice,
            Change = newPrice - oldPrice
        };
        
        _stocks[symbol] = stockInfo;
        NotifyObservers(symbol, stockInfo);
    }
    
    private void NotifyObservers(string symbol, StockInfo stock)
    {
        if (_observers.ContainsKey(symbol))
        {
            foreach (var observer in _observers[symbol])
            {
                observer.OnStockUpdate(stock);
            }
        }
    }
}

// ConcreteObserver - 콘솔 디스플레이
public class ConsoleDisplay : IStockObserver
{
    public void OnStockUpdate(StockInfo stock)
    {
        string arrow = stock.Change >= 0 ? "▲" : "▼";
        string color = stock.Change >= 0 ? "+" : "";
        Console.WriteLine($"  📊 {stock.Symbol}: ${stock.Price:F2} ({color}{stock.Change:F2}, {color}{stock.ChangePercent:F2}%) {arrow}");
    }
}

// ConcreteObserver - 알림 서비스
public class AlertService : IStockObserver
{
    private decimal _threshold;
    
    public AlertService(decimal threshold)
    {
        _threshold = threshold;
    }
    
    public void OnStockUpdate(StockInfo stock)
    {
        if (Math.Abs(stock.ChangePercent) >= _threshold)
        {
            Console.WriteLine($"  🚨 경보! {stock.Symbol}이(가) {stock.ChangePercent:F2}% 변동!");
        }
    }
}

// ConcreteObserver - 로깅 서비스
public class LoggingService : IStockObserver
{
    public void OnStockUpdate(StockInfo stock)
    {
        Console.WriteLine($"  📝 [LOG {DateTime.Now:HH:mm:ss}] {stock.Symbol}: ${stock.Price} (변동: {stock.Change:+0.00;-0.00})");
    }
}

// ConcreteObserver - 자동 매매 시스템
public class AutoTrader : IStockObserver
{
    private string _targetSymbol;
    private decimal _buyThreshold;
    private decimal _sellThreshold;
    
    public AutoTrader(string symbol, decimal buyThreshold, decimal sellThreshold)
    {
        _targetSymbol = symbol;
        _buyThreshold = buyThreshold;
        _sellThreshold = sellThreshold;
    }
    
    public void OnStockUpdate(StockInfo stock)
    {
        if (stock.Symbol == _targetSymbol)
        {
            if (stock.Price <= _buyThreshold)
            {
                Console.WriteLine($"  🤖 자동매매: {stock.Symbol} 매수 신호! (현재가: ${stock.Price}, 목표가: ${_buyThreshold})");
            }
            else if (stock.Price >= _sellThreshold)
            {
                Console.WriteLine($"  🤖 자동매매: {stock.Symbol} 매도 신호! (현재가: ${stock.Price}, 목표가: ${_sellThreshold})");
            }
        }
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        var market = new StockMarket();
        
        // Observer 생성
        var consoleDisplay = new ConsoleDisplay();
        var alertService = new AlertService(5.0m); // 5% 이상 변동 시 경보
        var loggingService = new LoggingService();
        var autoTrader = new AutoTrader("AAPL", 150m, 180m);
        
        // 구독 설정
        market.Subscribe("AAPL", consoleDisplay);
        market.Subscribe("AAPL", alertService);
        market.Subscribe("AAPL", loggingService);
        market.Subscribe("AAPL", autoTrader);
        
        market.Subscribe("GOOGL", consoleDisplay);
        market.Subscribe("GOOGL", loggingService);
        
        // 주가 업데이트
        Console.WriteLine("\n=== 주식 시장 업데이트 ===");
        
        Console.WriteLine("\n[AAPL 업데이트]");
        market.UpdateStock("AAPL", 165.00m);
        
        Console.WriteLine("\n[GOOGL 업데이트]");
        market.UpdateStock("GOOGL", 140.00m);
        
        Console.WriteLine("\n[AAPL 급등]");
        market.UpdateStock("AAPL", 175.00m); // 약 6% 상승
        
        Console.WriteLine("\n[AAPL 매수 신호]");
        market.UpdateStock("AAPL", 148.00m); // 매수 목표가 이하
    }
}
```

## 실제 사용 사례

### 1. Java Swing/AWT 이벤트 리스너
```java
button.addActionListener(e -> System.out.println("클릭됨"));
```

### 2. JavaScript DOM 이벤트
```javascript
element.addEventListener('click', (e) => console.log('클릭됨'));
```

### 3. Vue.js / React 상태 관리
상태 변경 시 자동으로 UI가 업데이트됨

### 4. RxJS/RxJava
```javascript
observable.subscribe(value => console.log(value));
```

### 5. C# 이벤트
```csharp
public event EventHandler<StockEventArgs> StockChanged;
```

## 관련 패턴

| 패턴 | 옵저버와의 관계 |
|------|---------------|
| **Mediator** | 옵저버는 직접 통신, Mediator는 중재자 통해 통신 |
| **Singleton** | Subject가 싱글턴일 수 있음 |
| **Command** | 알림 시 실행할 작업을 Command로 캡슐화 |

## FAQ

**Q1: 옵저버 패턴과 Pub-Sub 패턴의 차이점은 무엇인가요?**

전통적인 옵저버 패턴에서 Subject는 Observer를 직접 알고 있습니다. Pub-Sub 패턴은 중간에 메시지 브로커가 있어 발행자와 구독자가 서로를 알지 못합니다.

**Q2: 메모리 누수를 어떻게 방지하나요?**

Observer가 더 이상 필요하지 않을 때 반드시 구독을 해제(detach)해야 합니다. 약한 참조(WeakReference)를 사용하거나, Observer의 생명주기에 맞춰 자동 해제되도록 설계할 수 있습니다.

**Q3: 알림 순서가 중요한 경우 어떻게 하나요?**

우선순위 큐를 사용하거나, 체인 형태로 Observer를 연결하여 순서를 보장할 수 있습니다. 또는 순서가 중요한 로직은 별도로 처리합니다.

**Q4: 동기 vs 비동기 알림의 차이는?**

동기 알림은 모든 Observer가 처리를 완료할 때까지 대기하고, 비동기 알림은 별도의 스레드에서 처리됩니다. 비동기 방식은 성능이 좋지만 복잡성이 증가합니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- ReactiveX 공식 문서