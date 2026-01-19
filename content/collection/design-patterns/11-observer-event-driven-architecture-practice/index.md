---
draft: true
collection_order: 111
title: "[Design Patterns] 옵저버 패턴 실습 - 이벤트 주도 아키텍처"
description: "Observer 패턴을 활용한 이벤트 주도 아키텍처를 실습합니다. 주식 시세 모니터링, 온도 센서 알림, MVC 아키텍처 등을 구현하며 느슨한 결합과 반응형 시스템 설계를 마스터하고, WeakReference와 비동기 처리를 통한 성능 최적화 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-11T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Behavioral Patterns
- Event Driven Architecture
- Practice
- Reactive Systems
tags:
- Observer Pattern Practice
- Event Driven Architecture
- Publish Subscribe
- Stock Monitoring
- Temperature Sensor
- MVC Architecture
- WeakReference
- Async Processing
- Performance Optimization
- Reactive Systems
- Loose Coupling
- Behavioral Patterns
- Design Patterns
- GoF Patterns
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Software Architecture
- Event Handling
- 옵저버 패턴 실습
- 이벤트 주도 아키텍처
- 발행 구독
- 주식 모니터링
- 온도 센서
- MVC 아키텍처
- 약한 참조
- 비동기 처리
- 성능 최적화
- 반응형 시스템
- 느슨한 결합
- 행동 패턴
- 디자인 패턴
- GoF 패턴
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 소프트웨어 아키텍처
- 이벤트 처리
---

이 실습에서는 Observer 패턴을 활용하여 주식 시세 모니터링, 센서 알림 시스템 등 이벤트 주도 아키텍처를 구현합니다.

## 실습 목표

1. 주식 시세 모니터링 시스템 구현
2. 온도 센서 알림 시스템 구현
3. 성능 최적화 실습

## 과제 1: 주식 시세 모니터링

### 기본 구조
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

// 구체적인 주식 클래스
public class Stock implements StockSubject {
    private String symbol;
    private double price;
    private double change;
    private List<StockObserver> observers = new ArrayList<>();
    
    // TODO: 구현
}
```

### 구현 과제
- ConcreteStock 클래스 완성
- StockDisplay, StockAlert, StockLogger 옵저버 구현
- 여러 주식 동시 모니터링 기능

## 과제 2: 온도 센서 알림

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

### WeakReference Observer
```java
public class WeakReferenceSubject {
    private List<WeakReference<Observer>> observers = new ArrayList<>();
    
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
```java
public class AsyncObserver implements Observer {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    
    @Override
    public void update(Subject subject) {
        executor.submit(() -> {
            // 비동기 처리 로직
            processUpdate(subject);
        });
    }
}
```

## 완성도 체크리스트

### 기본 구현
- [ ] Subject/Observer 인터페이스 구현
- [ ] 다양한 Observer 구현체 작성
- [ ] 동적 Observer 추가/제거 기능
- [ ] 예외 처리 (Observer 실패 시)

### 고급 기능
- [ ] WeakReference 기반 메모리 누수 방지
- [ ] 비동기 알림 처리
- [ ] 알림 필터링 및 우선순위
- [ ] 성능 모니터링 및 최적화

### 테스트
- [ ] 다수 Observer 성능 테스트
- [ ] 메모리 누수 시나리오 테스트
- [ ] 동시성 테스트

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