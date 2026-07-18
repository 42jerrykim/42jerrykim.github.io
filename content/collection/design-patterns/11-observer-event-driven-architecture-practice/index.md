---
draft: true
collection_order: 111
title: "[Design Patterns] 11. 옵저버: 이벤트 드리븐 아키텍처의 핵심 — 실습"
slug: "observer-event-driven-architecture-practice"
description: "Observer 패턴을 활용해 주식 시세 모니터링과 온도 센서 알림 시스템, MVC 아키텍처를 직접 구현합니다. WeakReference와 비동기 처리를 적용해 느슨한 결합과 성능을 동시에 확보하는 방법을 실습합니다."
image: "wordcloud.png"
date: 2024-12-11T11:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Behavioral Patterns
- Event Driven Architecture
- Practice
- Reactive Systems
tags:
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Behavioral-Pattern
- Observer
- Event-Driven
- Software-Architecture(소프트웨어아키텍처)
- Tutorial(튜토리얼)
- Implementation(구현)
- Performance(성능)
- Optimization(최적화)
- Async(비동기)
- Concurrency(동시성)
- Java
- OOP(객체지향)
- Interface(인터페이스)
- Coupling(결합도)
- Best-Practices
- Guide(가이드)
- Case-Study
- Advanced
- Memory(메모리)
- Benchmark
- Profiling(프로파일링)
- System-Design
- Reliability
- Scalability(확장성)
- Refactoring(리팩토링)
- Code-Quality(코드품질)
---

이 실습에서는 Observer 패턴을 활용하여 주식 시세 모니터링, 센서 알림 시스템 등 이벤트 주도 아키텍처를 구현합니다.

## 실습 목표

1. 주식 시세 모니터링 시스템 구현
2. 온도 센서 알림 시스템 구현
3. 성능 최적화 실습

## 과제 1: 주식 시세 모니터링

> *"한 객체의 상태가 변했을 때, 그 객체에 의존하는 다른 객체들에게 자동으로 알려주고 업데이트되도록 하는 일대다 의존성을 정의한다."* — GoF, 《Design Patterns》(1994), Observer 패턴 Intent

이 과제는 Observer 패턴의 가장 단순한 형태(Subject/Observer 인터페이스 분리)를 주식 시세라는 익숙한 도메인에 적용해보는 것이 목적이다. 화면 표시, 임계값 알림, 로그 기록처럼 성격이 다른 구독자들이 동일한 가격 변경 이벤트에 반응해야 할 때, `Stock`이 구독자의 구체 타입을 몰라도 통지할 수 있어야 한다는 점이 핵심이다.

### 기본 구조

아래는 `Stock`의 attach/detach/notifyObservers와 `StockLogger` 옵저버까지 포함한 완성 참조 구현이다. `StockDisplay`, `StockAlert`는 이 구조를 참고해 직접 구현한다.

```java
// Subject 인터페이스
public interface StockSubject {
    void attach(StockObserver observer);
    void detach(StockObserver observer);
    void notifyObservers();
}

// Observer 인터페이스
public interface StockObserver {
    void update(String symbol, double price, double change);
}

// 참조 구현: Subject 역할을 하는 구체 주식 클래스
public class Stock implements StockSubject {
    private final String symbol;
    private double price;
    private double change;
    private final List<StockObserver> observers = new ArrayList<>();

    public Stock(String symbol, double initialPrice) {
        this.symbol = symbol;
        this.price = initialPrice;
    }

    @Override
    public void attach(StockObserver observer) {
        observers.add(observer);
    }

    @Override
    public void detach(StockObserver observer) {
        observers.remove(observer);
    }

    @Override
    public void notifyObservers() {
        // 통지 도중 attach/detach가 호출될 수 있으므로 방어적으로 복사한다
        for (StockObserver observer : new ArrayList<>(observers)) {
            observer.update(symbol, price, change);
        }
    }

    public void setPrice(double newPrice) {
        this.change = newPrice - this.price;
        this.price = newPrice;
        notifyObservers();
    }
}

// 참조 구현: 로그만 남기는 가장 단순한 Observer
public class StockLogger implements StockObserver {
    @Override
    public void update(String symbol, double price, double change) {
        System.out.printf("[LOG] %s: $%.2f (%+.2f)%n", symbol, price, change);
    }
}
```

### 구현 과제
- StockDisplay, StockAlert 옵저버 구현 (위 StockLogger를 참고)
- 여러 주식 동시 모니터링 기능

## 과제 2: 온도 센서 알림

이 과제는 단순 통지가 아니라 조건부 통지(임계값을 넘었을 때만 반응)를 Observer 구조 위에 얹는 감각을 익히는 것이 목적이다. `TemperatureSensor`는 값이 바뀌었다는 사실만 알리고, 임계값 판단과 알림 채널 선택은 각 Observer가 책임진다는 역할 분리에 주목한다.

### 기본 구조
```java
public class TemperatureSensor {
    private double temperature;
    private List<TemperatureObserver> observers = new ArrayList<>();
    
    public void setTemperature(double temperature) {
        this.temperature = temperature;
        notifyObservers();
    }
    
    // TODO: Observer 관리 메서드 구현
}

public interface TemperatureObserver {
    void onTemperatureChanged(double temperature);
}
```

### 구현 과제
- 임계값 기반 알림 시스템
- 다양한 알림 채널 (이메일, SMS, 로그)
- 알림 빈도 제한 기능

## 과제 3: 성능 최적화

이 과제는 Observer 패턴을 실서비스에 적용할 때 마주치는 두 가지 문제 — 등록 해제를 잊어 발생하는 메모리 누수, 동기 통지로 인한 호출 스레드 블로킹 — 을 완화하는 기법을 다룬다.

**WeakReference를 언제 쓸 것인가**: WeakReference는 detach() 호출을 잊어도 GC가 알아서 정리해준다는 장점이 있지만, 정리 시점이 GC 타이밍에 좌우되어 예측 불가능하고 notifyObservers()마다 죽은 참조를 순회하며 걸러내는 오버헤드가 붙는다. Subject를 attach한 코드가 자신의 생명주기를 명확히 통제할 수 있다면(예: 화면이 닫힐 때 확실히 detach를 호출할 수 있는 UI 컴포넌트) 명시적 해제가 더 예측 가능하고 저렴하다. 반대로 Subject가 전역 싱글턴이나 장수명 캐시처럼 Observer보다 훨씬 오래 살아남고 호출자가 detach를 안정적으로 보장하기 어려운 구조라면, WeakReference로 누수를 방지하는 편이 안전하다.

| 선택 기준 | WeakReference | 명시적 해제(detach) |
|----------|---------------|---------------------|
| Observer 생명주기 통제 | 호출자가 통제하기 어려움 | 호출자가 명확히 통제 가능 |
| Subject 수명 | Observer보다 훨씬 김(싱글턴, 캐시) | Observer와 비슷하거나 짧음 |
| 정리 시점 | GC 타이밍에 의존, 예측 불가 | detach 호출 즉시, 예측 가능 |
| 런타임 오버헤드 | notifyObservers마다 죽은 참조 스캔 | 없음 |
| 실수 시 위험 | 없음(자동 회수) | detach 누락 시 누수 |
| 적합한 상황 | 전역 캐시, 이벤트 버스 | UI 컴포넌트, 명확한 스코프 객체 |

### WeakReference Observer
```java
public class WeakReferenceSubject {
    private List<WeakReference<Observer>> observers = new ArrayList<>();
    
    public void attach(Observer observer) {
        observers.add(new WeakReference<>(observer));
    }
    
    public void notifyObservers() {
        Iterator<WeakReference<Observer>> iterator = observers.iterator();
        while (iterator.hasNext()) {
            WeakReference<Observer> ref = iterator.next();
            Observer observer = ref.get();
            
            if (observer == null) {
                iterator.remove(); // GC된 Observer 제거
            } else {
                observer.update(this);
            }
        }
    }
}
```

### 비동기 Observer

통지 자체는 즉시 반환하고, 실제 처리는 별도 스레드로 넘겨 호출 스레드(대개 Subject가 setPrice 등을 호출한 스레드)를 블로킹하지 않는다. `processUpdate`는 여기서 실제로 무거운 작업(가격 이력 집계, 알림 발송 등)을 수행하는 자리이며, 비동기 실행 중 발생한 예외가 조용히 삼켜지지 않도록 명시적으로 잡아 로깅해야 한다.

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

// 위 StockObserver 인터페이스(update(symbol, price, change))를 그대로 구현한다
public class AsyncObserver implements StockObserver {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();

    @Override
    public void update(String symbol, double price, double change) {
        executor.submit(() -> {
            try {
                processUpdate(symbol, price, change);
            } catch (Exception e) {
                // 비동기 작업의 예외는 호출 스레드로 전파되지 않으므로 반드시 여기서 처리한다
                System.err.println("AsyncObserver failed to process update: " + e.getMessage());
            }
        });
    }

    private void processUpdate(String symbol, double price, double change) {
        // 실제 처리 로직: 가격 변동을 별도 로그 저장소에 비동기로 기록
        System.out.printf("[Async] %s price change recorded: $%.2f (%+.2f)%n",
            symbol, price, change);
    }
}
```

## 완성도 체크리스트

### 기본 구현
- [ ] Subject/Observer 인터페이스 구현 — `Stock`이 구체 Observer 타입을 몰라도 `StockObserver` 인터페이스만으로 통지할 수 있는지 확인
- [ ] 다양한 Observer 구현체 작성 — Display/Alert/Logger처럼 반응 방식이 다른 Observer가 동일한 인터페이스로 등록되는지 확인
- [ ] 동적 Observer 추가/제거 기능 — 실행 중에 attach/detach를 호출해도 다른 Observer의 통지가 깨지지 않는지 확인
- [ ] 예외 처리 (Observer 실패 시) — 하나의 Observer에서 예외가 발생해도 나머지 Observer가 정상 통지받는지 확인

### 고급 기능
- [ ] WeakReference 기반 메모리 누수 방지 — detach를 호출하지 않은 Observer가 GC 이후 목록에서 자동으로 사라지는지 확인
- [ ] 비동기 알림 처리 — 통지가 호출 스레드를 블로킹하지 않고 별도 스레드에서 처리되는지 확인
- [ ] 알림 필터링 및 우선순위 — 조건에 맞지 않는 이벤트는 걸러지고, 우선순위가 높은 Observer가 먼저 통지받는지 확인
- [ ] 성능 모니터링 및 최적화 — Observer 수 증가에 따른 통지 시간을 실측했는지 확인

### 테스트
- [ ] 다수 Observer 성능 테스트 — 수천 개 Observer 등록 시에도 통지 시간이 선형적으로 증가하는지 확인
- [ ] 메모리 누수 시나리오 테스트 — detach 없이 Observer를 반복 생성해도 힙 사용량이 계속 늘지 않는지 확인
- [ ] 동시성 테스트 — 여러 스레드가 동시에 attach/detach/notify를 호출해도 예외나 데이터 손상이 없는지 확인

## 추가 도전 과제

1. EventBus 패턴으로 확장
2. Reactive Streams 연계
3. 분산 Observer 시스템
4. 패턴 조합 (Observer + Strategy + Command)

## 실무 적용 예시

### MVC 아키텍처
```java
// Model이 Subject 역할
public class UserModel extends Observable {
    private String username;
    
    public void setUsername(String username) {
        this.username = username;
        setChanged();
        notifyObservers(username);
    }
}

// View가 Observer 역할
public class UserView implements Observer {
    @Override
    public void update(Observable o, Object arg) {
        if (o instanceof UserModel) {
            updateDisplay((String) arg);
        }
    }
}
```

### Spring Events
```java
@Component
public class OrderService {
    @Autowired
    private ApplicationEventPublisher eventPublisher;
    
    public void processOrder(Order order) {
        // 주문 처리 로직
        eventPublisher.publishEvent(new OrderCreatedEvent(order));
    }
}

@EventListener
@Component
public class EmailService {
    public void handleOrderCreated(OrderCreatedEvent event) {
        sendConfirmationEmail(event.getOrder());
    }
}
```

---

**실습 팁**
- Observer 패턴의 메모리 누수 위험성 항상 고려
- 비동기 처리 시 스레드 안전성 확보
- 대량 Observer 등록 시 성능 영향 측정
- 실제 GUI 프레임워크나 이벤트 시스템 분석 