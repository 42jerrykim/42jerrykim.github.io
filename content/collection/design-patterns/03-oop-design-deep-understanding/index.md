---
collection_order: 30
draft: true
title: "[Design Patterns] 객체지향 설계의 깊이 있는 이해"
description: "객체지향 프로그래밍의 근본 원리와 설계 철학을 심도 있게 탐구합니다. SOLID 원칙, 캡슐화, 상속, 다형성의 본질을 이해하고, 실제 코드에서 이러한 개념들이 어떻게 패턴으로 구현되는지 학습합니다. 좋은 객체지향 설계와 나쁜 설계를 구분하는 안목을 기르고, 설계 품질을 향상시키는 실무 기법을 익힙니다."
date: 2024-12-03T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Object Oriented Programming
- Software Design
- Design Principles
tags:
- Object Oriented Design
- OOP Principles
- SOLID Principles
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
- Design Patterns
- Code Quality
- Software Architecture
- Class Design
- Interface Design
- Composition
- Aggregation
- Dependency Injection
- Inversion Of Control
- Single Responsibility
- Open Closed Principle
- Liskov Substitution
- Interface Segregation
- Dependency Inversion
- Design By Contract
- Domain Modeling
- Object Modeling
- Software Engineering
- Clean Code
- Refactoring
- Code Smells
- Design Quality
- Architectural Design
- 객체 지향 설계
- OOP 원칙
- SOLID 원칙
- 캡슐화
- 상속
- 다형성
- 추상화
- 디자인 패턴
- 코드 품질
- 소프트웨어 아키텍처
- 클래스 설계
- 인터페이스 설계
- 컴포지션
- 집합
- 의존성 주입
- 제어 역전
- 단일 책임
- 개방 폐쇄 원칙
- 리스코프 치환
- 인터페이스 분리
- 의존성 역전
- 계약에 의한 설계
- 도메인 모델링
- 객체 모델링
- 소프트웨어 공학
- 클린 코드
- 리팩토링
- 코드 스멜
- 설계 품질
- 아키텍처 설계
---

# 객체지향 설계의 심층 이해

## **서론: 객체지향, 그 오해와 진실**

> *"객체지향은 현실 세계를 모델링하는 것이다."*

이는 아마도 객체지향에 대한 **가장 큰 오해** 중 하나일 것입니다. 자동차 클래스에 `start()`, `stop()` 메서드를 만들고, 강아지 클래스에 `bark()` 메서드를 만드는 것이 객체지향이라고 생각한다면, 당신은 객체지향의 **겉모습**만 보고 있는 것입니다.

진정한 객체지향은 **현실 세계 모델링이 아니라**, **복잡성을 다루는 강력한 사고 방식**입니다. 그리고 이 사고 방식의 핵심은 **"책임의 분배"**와 **"협력의 설계"**에 있습니다.

많은 개발자들이 클래스와 객체를 만들 줄 알지만, 정작 **"왜 이렇게 설계해야 하는가?"**에 대한 답을 갖지 못합니다. 상속을 남용하고, 캡슐화를 getter/setter로 오해하며, 다형성을 단순한 메서드 오버라이딩 정도로 인식합니다.

이번 글에서는 객체지향의 **진정한 본질**을 탐구하고, 이것이 어떻게 디자인 패턴의 철학적 기반이 되는지 살펴보겠습니다.

### **1. 캡슐화: 정보 은닉을 넘어선 책임의 캡슐화**

#### **1.1 잘못된 캡슐화의 이해**

대부분의 개발자들이 생각하는 캡슐화는 이런 것입니다:

```java
// 잘못된 캡슐화 예시
public class User {
    private String name;
    private int age;
    private String email;
    
    // getter/setter 메서드들
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}

// 사용하는 곳에서
User user = new User();
user.setName("김개발");
user.setAge(30);
user.setEmail("kim@example.com");

if (user.getAge() >= 18) {
    // 성인 인증 로직
    sendWelcomeEmail(user.getEmail());
}
```

이것은 캡슐화가 아니라 **"캡슐화의 위장"**입니다. 실제로는 모든 내부 상태가 외부에 노출되어 있고, 객체의 책임은 외부 코드가 대신 수행하고 있습니다.

#### **1.2 진정한 캡슐화: 책임과 지식의 은닉**

진정한 캡슐화는 **"객체가 무엇을 알고 있는가"**와 **"객체가 무엇을 할 수 있는가"**를 하나로 묶는 것입니다:

```java
// 올바른 캡슐화 예시
public class User {
    private String name;
    private LocalDate birthDate;
    private Email email;
    private UserStatus status;
    
    public User(String name, LocalDate birthDate, String email) {
        this.name = validateName(name);
        this.birthDate = validateBirthDate(birthDate);
        this.email = new Email(email);  // Email 객체가 유효성 검증 담당
        this.status = UserStatus.PENDING;
    }
    
    public boolean isAdult() {
        return Period.between(birthDate, LocalDate.now()).getYears() >= 18;
    }
    
    public void activate() {
        if (!isAdult()) {
            throw new IllegalStateException("미성년자는 활성화할 수 없습니다");
        }
        this.status = UserStatus.ACTIVE;
        publishEvent(new UserActivatedEvent(this));
    }
    
    public void sendWelcomeMessage() {
        if (status != UserStatus.ACTIVE) {
            throw new IllegalStateException("활성화된 사용자만 환영 메시지를 받을 수 있습니다");
        }
        email.send(createWelcomeMessage());
    }
    
    // private 메서드들로 내부 로직 은닉
    private String validateName(String name) { /* 검증 로직 */ }
    private LocalDate validateBirthDate(LocalDate date) { /* 검증 로직 */ }
    private WelcomeMessage createWelcomeMessage() { /* 메시지 생성 로직 */ }
}

// 사용하는 곳에서
User user = new User("김개발", LocalDate.of(1990, 1, 1), "kim@example.com");
user.activate();
user.sendWelcomeMessage();
```

**핵심 차이점:**
- **지식의 은닉**: 나이 계산 로직, 활성화 조건 등이 User 내부에 은닉
- **행동의 캡슐화**: `activate()`, `sendWelcomeMessage()` 등 의미 있는 행동 제공
- **불변식 보장**: 객체의 상태가 항상 유효한 상태로 유지됨

#### **1.3 Tell, Don't Ask 원칙**

**잘못된 접근 (Ask):**
```java
// 외부에서 객체의 상태를 묻고 판단
if (user.getStatus() == UserStatus.ACTIVE && user.getAge() >= 18) {
    emailService.sendPromotionEmail(user.getEmail());
}
```

**올바른 접근 (Tell):**
```java
// 객체에게 행동을 지시
user.sendPromotionEmailIfEligible(promotionContent);

// User 클래스 내부
public void sendPromotionEmailIfEligible(PromotionContent content) {
    if (canReceivePromotion()) {
        email.send(createPromotionMessage(content));
    }
}

private boolean canReceivePromotion() {
    return status == UserStatus.ACTIVE && isAdult();
}
```

### **2. 상속 vs 컴포지션: 설계 철학의 근본적 차이**

#### **2.1 상속의 매력과 함정**

상속은 강력하지만 위험한 도구입니다. **"is-a"** 관계를 모델링하는 데 적합해 보이지만, 실제로는 많은 함정이 있습니다.

**취약한 기반 클래스 문제:**
```java
// 기반 클래스
public class HashSet<E> {
    private int addCount = 0;
    
    public boolean add(E e) {
        addCount++;
        return super.add(e);
    }
    
    public boolean addAll(Collection<? extends E> c) {
        addCount += c.size();
        return super.addAll(c);  // 내부적으로 add()를 호출함!
    }
    
    public int getAddCount() {
        return addCount;
    }
}

// 파생 클래스 사용
InstrumentedHashSet<String> set = new InstrumentedHashSet<>();
set.addAll(Arrays.asList("A", "B", "C"));
System.out.println(set.getAddCount());  // 예상: 3, 실제: 6!
```

**문제의 원인:**
- `addAll()`이 내부적으로 `add()`를 호출
- 파생 클래스에서 `add()`를 오버라이드했으므로 중복 카운팅
- 기반 클래스의 **내부 구현 변경**이 파생 클래스를 **예측 불가능하게 만듦**

#### **2.2 컴포지션을 통한 안전한 설계**

```java
// 컴포지션 기반 설계
public class InstrumentedSet<E> implements Set<E> {
    private final Set<E> set;
    private int addCount = 0;
    
    public InstrumentedSet(Set<E> set) {
        this.set = set;
    }
    
    @Override
    public boolean add(E e) {
        addCount++;
        return set.add(e);
    }
    
    @Override
    public boolean addAll(Collection<? extends E> c) {
        addCount += c.size();
        return set.addAll(c);
    }
    
    public int getAddCount() {
        return addCount;
    }
    
    // 나머지 Set 메서드들은 단순히 위임 (Forwarding)
    @Override public int size() { return set.size(); }
    @Override public boolean isEmpty() { return set.isEmpty(); }
    // ... 기타 메서드들
}

// 사용
Set<String> hashSet = new HashSet<>();
InstrumentedSet<String> instrumentedSet = new InstrumentedSet<>(hashSet);
instrumentedSet.addAll(Arrays.asList("A", "B", "C"));
System.out.println(instrumentedSet.getAddCount());  // 정확히 3
```

**컴포지션의 장점:**
- **안전성**: 내부 구현 변경에 영향받지 않음
- **유연성**: 런타임에 다른 Set 구현체로 교체 가능
- **명확성**: 어떤 메서드가 어떤 동작을 하는지 명확함

#### **2.3 위임(Delegation) vs 전략(Strategy)**

**위임 패턴:**
```java
public class SortedList<E> {
    private final List<E> list;
    private final Comparator<E> comparator;
    
    public SortedList(Comparator<E> comparator) {
        this.list = new ArrayList<>();
        this.comparator = comparator;
    }
    
    public void add(E element) {
        list.add(element);
        Collections.sort(list, comparator);  // 정렬 책임을 Collections에 위임
    }
    
    // 나머지 메서드들은 list에 위임
    public E get(int index) { return list.get(index); }
    public int size() { return list.size(); }
}
```

**전략 패턴:**
```java
public interface SortStrategy<E> {
    void sort(List<E> list, Comparator<E> comparator);
}

public class QuickSortStrategy<E> implements SortStrategy<E> {
    public void sort(List<E> list, Comparator<E> comparator) {
        // QuickSort 구현
    }
}

public class SortedList<E> {
    private final List<E> list;
    private final Comparator<E> comparator;
    private final SortStrategy<E> sortStrategy;
    
    public SortedList(Comparator<E> comparator, SortStrategy<E> strategy) {
        this.list = new ArrayList<>();
        this.comparator = comparator;
        this.sortStrategy = strategy;
    }
    
    public void add(E element) {
        list.add(element);
        sortStrategy.sort(list, comparator);  // 정렬 전략에 위임
    }
}
```

**차이점:**
- **위임**: 특정 작업을 다른 객체에 맡김 (고정적)
- **전략**: 알고리즘을 교체 가능하게 만듦 (동적)

### **3. 다형성: 유연성의 핵심 동력**

#### **3.1 다형성의 진정한 의미**

다형성은 단순히 메서드 오버라이딩이 아닙니다. 그것은 **"같은 인터페이스, 다른 구현"**을 통해 **코드의 유연성과 확장성**을 제공하는 메커니즘입니다.

**컴파일타임 다형성 vs 런타임 다형성:**
```java
// 컴파일타임 다형성 (메서드 오버로딩)
public class Calculator {
    public int add(int a, int b) { return a + b; }
    public double add(double a, double b) { return a + b; }
    public String add(String a, String b) { return a + b; }
}

// 런타임 다형성 (메서드 오버라이딩)
public interface PaymentProcessor {
    PaymentResult process(PaymentRequest request);
}

public class CreditCardProcessor implements PaymentProcessor {
    public PaymentResult process(PaymentRequest request) {
        // 신용카드 결제 로직
        return new PaymentResult(SUCCESS, "Credit card payment processed");
    }
}

public class PayPalProcessor implements PaymentProcessor {
    public PaymentResult process(PaymentRequest request) {
        // PayPal 결제 로직
        return new PaymentResult(SUCCESS, "PayPal payment processed");
    }
}

// 다형성의 활용
public class OrderService {
    private final PaymentProcessor processor;
    
    public OrderService(PaymentProcessor processor) {
        this.processor = processor;  // 어떤 구현체든 받아들임
    }
    
    public void processOrder(Order order) {
        PaymentRequest request = createPaymentRequest(order);
        PaymentResult result = processor.process(request);  // 다형적 호출
        
        if (result.isSuccess()) {
            completeOrder(order);
        }
    }
}
```

#### **3.2 리스코프 치환 원칙(LSP)의 깊은 의미**

LSP는 단순히 "파생 클래스는 기반 클래스를 대체할 수 있어야 한다"는 것이 아닙니다. 그것은 **"행동적 호환성"**을 보장하는 원칙입니다.

**LSP 위반 사례:**
```java
// 잘못된 설계
public class Rectangle {
    protected int width, height;
    
    public void setWidth(int width) { this.width = width; }
    public void setHeight(int height) { this.height = height; }
    public int getArea() { return width * height; }
}

public class Square extends Rectangle {
    @Override
    public void setWidth(int width) {
        this.width = width;
        this.height = width;  // 정사각형이므로 높이도 같이 변경
    }
    
    @Override
    public void setHeight(int height) {
        this.width = height;   // 정사각형이므로 너비도 같이 변경
        this.height = height;
    }
}

// 문제가 되는 코드
public void testRectangle(Rectangle rect) {
    rect.setWidth(5);
    rect.setHeight(4);
    assert rect.getArea() == 20;  // Square일 경우 실패!
}
```

**LSP를 준수하는 설계:**
```java
// 올바른 설계
public abstract class Shape {
    public abstract int getArea();
    public abstract void resize(double factor);
}

public class Rectangle extends Shape {
    private int width, height;
    
    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }
    
    @Override
    public int getArea() { return width * height; }
    
    @Override
    public void resize(double factor) {
        this.width = (int)(width * factor);
        this.height = (int)(height * factor);
    }
    
    // 불변성을 유지하는 메서드들
    public Rectangle withWidth(int newWidth) {
        return new Rectangle(newWidth, this.height);
    }
    
    public Rectangle withHeight(int newHeight) {
        return new Rectangle(this.width, newHeight);
    }
}

public class Square extends Shape {
    private int side;
    
    public Square(int side) {
        this.side = side;
    }
    
    @Override
    public int getArea() { return side * side; }
    
    @Override
    public void resize(double factor) {
        this.side = (int)(side * factor);
    }
    
    public Square withSide(int newSide) {
        return new Square(newSide);
    }
}
```

#### **3.3 인터페이스 분리 원칙(ISP)과 설계 유연성**

**ISP 위반 사례:**
```java
// 잘못된 설계: 비대한 인터페이스
public interface Worker {
    void work();
    void eat();
    void sleep();
    void attendMeeting();
    void writeReport();
    void operateMachine();
}

// 문제: 로봇은 eat(), sleep()을 구현할 수 없음
public class Robot implements Worker {
    public void work() { /* 작업 수행 */ }
    public void eat() { throw new UnsupportedOperationException(); }
    public void sleep() { throw new UnsupportedOperationException(); }
    public void attendMeeting() { throw new UnsupportedOperationException(); }
    public void writeReport() { /* 보고서 작성 */ }
    public void operateMachine() { /* 기계 조작 */ }
}
```

**ISP를 준수하는 설계:**
```java
// 올바른 설계: 역할별 인터페이스 분리
public interface Workable {
    void work();
}

public interface Eatable {
    void eat();
}

public interface Sleepable {
    void sleep();
}

public interface MeetingAttendable {
    void attendMeeting();
}

public interface ReportWritable {
    void writeReport();
}

public interface MachineOperable {
    void operateMachine();
}

// 필요한 인터페이스만 구현
public class Human implements Workable, Eatable, Sleepable, MeetingAttendable, ReportWritable {
    public void work() { /* 작업 수행 */ }
    public void eat() { /* 식사 */ }
    public void sleep() { /* 수면 */ }
    public void attendMeeting() { /* 회의 참석 */ }
    public void writeReport() { /* 보고서 작성 */ }
}

public class Robot implements Workable, ReportWritable, MachineOperable {
    public void work() { /* 작업 수행 */ }
    public void writeReport() { /* 보고서 작성 */ }
    public void operateMachine() { /* 기계 조작 */ }
}

// 클라이언트 코드는 필요한 인터페이스만 의존
public class WorkManager {
    private final List<Workable> workers;
    
    public void assignWork() {
        for (Workable worker : workers) {
            worker.work();  // 다형성 활용
        }
    }
}
```

### **4. 의존성과 결합도: 설계의 미묘한 예술**

#### **4.1 의존성의 다양한 형태**

의존성은 단순히 "A가 B를 사용한다"가 아닙니다. 여러 층위의 의존성이 있습니다:

**컴파일타임 의존성 vs 런타임 의존성:**
```java
// 컴파일타임 의존성: 소스 코드 수준의 의존성
public class OrderService {
    private PaymentProcessor processor;  // PaymentProcessor 인터페이스에 의존
    
    public OrderService(PaymentProcessor processor) {
        this.processor = processor;
    }
    
    public void processOrder(Order order) {
        processor.process(createPaymentRequest(order));
    }
}

// 런타임 의존성: 실행 시점의 실제 객체 의존성
PaymentProcessor creditCardProcessor = new CreditCardProcessor();
OrderService orderService = new OrderService(creditCardProcessor);
// 런타임에는 CreditCardProcessor 객체에 실제로 의존
```

**의존성 역전 원칙(DIP)의 실제 적용:**
```java
// 잘못된 설계: 고수준 모듈이 저수준 모듈에 의존
public class OrderService {
    private MySQLOrderRepository repository;  // 구체 클래스에 의존
    private EmailNotificationService emailService;  // 구체 클래스에 의존
    
    public OrderService() {
        this.repository = new MySQLOrderRepository();  // 직접 생성
        this.emailService = new EmailNotificationService();  // 직접 생성
    }
    
    public void processOrder(Order order) {
        repository.save(order);
        emailService.sendConfirmation(order);
    }
}

// 올바른 설계: 추상화에 의존
public class OrderService {
    private final OrderRepository repository;  // 인터페이스에 의존
    private final NotificationService notificationService;  // 인터페이스에 의존
    
    public OrderService(OrderRepository repository, NotificationService notificationService) {
        this.repository = repository;
        this.notificationService = notificationService;
    }
    
    public void processOrder(Order order) {
        repository.save(order);
        notificationService.sendConfirmation(order);
    }
}

// 의존성 주입을 통한 구성
public class OrderServiceFactory {
    public static OrderService create() {
        OrderRepository repository = new MySQLOrderRepository();
        NotificationService notificationService = new EmailNotificationService();
        return new OrderService(repository, notificationService);
    }
}
```

#### **4.2 결합도의 스펙트럼**

결합도는 단순히 "높다/낮다"가 아니라 **여러 단계**가 있습니다:

**1. Content Coupling (내용 결합) - 최악**
```java
// A가 B의 내부 데이터를 직접 수정
public class BadExample {
    public void manipulateUser(User user) {
        user.status = "ACTIVE";  // private 필드에 직접 접근 (reflection 등)
        user.validateInternalState();  // private 메서드 호출
    }
}
```

**2. Common Coupling (공통 결합) - 매우 나쁨**
```java
// 전역 변수를 통한 결합
public class GlobalState {
    public static String currentUser;
    public static boolean isDebugMode;
}

public class ServiceA {
    public void doSomething() {
        if (GlobalState.isDebugMode) {
            System.out.println("ServiceA: " + GlobalState.currentUser);
        }
    }
}
```

**3. Control Coupling (제어 결합) - 나쁨**
```java
// 제어 정보를 전달하여 상대방의 동작을 제어
public class ControlCouplingExample {
    public void processData(Data data, boolean useNewAlgorithm) {
        if (useNewAlgorithm) {
            // 새로운 알고리즘
        } else {
            // 기존 알고리즘
        }
    }
}
```

**4. Data Coupling (데이터 결합) - 좋음**
```java
// 필요한 데이터만 매개변수로 전달
public class DataCouplingExample {
    public PaymentResult processPayment(PaymentRequest request) {
        // request에 필요한 데이터만 포함
        return new PaymentResult(/* 결과 데이터 */);
    }
}
```

**5. Message Coupling (메시지 결합) - 최선**
```java
// 메시지를 통한 느슨한 결합
public class MessageCouplingExample {
    private final EventPublisher eventPublisher;
    
    public void processOrder(Order order) {
        // 작업 수행
        eventPublisher.publish(new OrderProcessedEvent(order.getId()));
        // 누가 이 이벤트를 처리할지 모르고 관심도 없음
    }
}
```

###️ **5. SOLID 원칙: 객체지향 설계의 통합 이론**

#### **5.1 SRP: 단일 책임 원칙의 깊은 이해**

SRP는 "클래스는 하나의 책임만 가져야 한다"가 아닙니다. 정확히는 **"클래스가 변경되는 이유는 오직 하나여야 한다"**입니다.

**SRP 위반 사례:**
```java
// 잘못된 설계: 여러 책임이 섞임
public class Employee {
    private String name;
    private BigDecimal salary;
    private String department;
    
    // 책임 1: 급여 계산
    public BigDecimal calculatePay() {
        // 복잡한 급여 계산 로직
        // HR 부서의 정책 변경에 영향받음
    }
    
    // 책임 2: 데이터 저장
    public void save() {
        // 데이터베이스 저장 로직
        // DBA의 스키마 변경에 영향받음
    }
    
    // 책임 3: 보고서 생성
    public String generateReport() {
        // 보고서 포맷 생성
        // 회계팀의 보고서 양식 변경에 영향받음
    }
}
```

**SRP를 준수하는 설계:**
```java
// 올바른 설계: 책임 분리
public class Employee {
    private final String name;
    private final BigDecimal salary;
    private final String department;
    
    // 생성자와 기본적인 getter들만
    public Employee(String name, BigDecimal salary, String department) {
        this.name = name;
        this.salary = salary;
        this.department = department;
    }
    
    // 불변 객체로 설계
    public String getName() { return name; }
    public BigDecimal getSalary() { return salary; }
    public String getDepartment() { return department; }
}

// 각각의 책임을 별도 클래스로 분리
public class PayCalculator {
    public BigDecimal calculatePay(Employee employee) {
        // 급여 계산 로직만 담당
    }
}

public class EmployeeRepository {
    public void save(Employee employee) {
        // 데이터 저장 로직만 담당
    }
}

public class EmployeeReportGenerator {
    public String generateReport(Employee employee) {
        // 보고서 생성 로직만 담당
    }
}
```

#### **5.2 OCP: 개방-폐쇄 원칙의 실제 적용**

OCP는 **"확장에는 열려있고, 수정에는 닫혀있어야 한다"**는 원칙입니다. 이는 **Strategy 패턴**과 **Template Method 패턴**의 이론적 기반입니다.

**OCP 위반 사례:**
```java
// 잘못된 설계: 새로운 도형 추가 시마다 기존 코드 수정 필요
public class AreaCalculator {
    public double calculateArea(Object shape) {
        if (shape instanceof Rectangle) {
            Rectangle rectangle = (Rectangle) shape;
            return rectangle.getWidth() * rectangle.getHeight();
        } else if (shape instanceof Circle) {
            Circle circle = (Circle) shape;
            return Math.PI * circle.getRadius() * circle.getRadius();
        } else if (shape instanceof Triangle) {  // 새로운 도형 추가 시 수정
            Triangle triangle = (Triangle) shape;
            return 0.5 * triangle.getBase() * triangle.getHeight();
        }
        throw new IllegalArgumentException("Unknown shape");
    }
}
```

**OCP를 준수하는 설계:**
```java
// 올바른 설계: 새로운 도형 추가 시 기존 코드 수정 불필요
public abstract class Shape {
    public abstract double calculateArea();
}

public class Rectangle extends Shape {
    private final double width, height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    @Override
    public double calculateArea() {
        return width * height;
    }
}

public class Circle extends Shape {
    private final double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}

// 새로운 도형 추가 시 기존 코드 수정 없음
public class Triangle extends Shape {
    private final double base, height;
    
    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }
    
    @Override
    public double calculateArea() {
        return 0.5 * base * height;
    }
}

public class AreaCalculator {
    public double calculateTotalArea(List<Shape> shapes) {
        return shapes.stream()
                    .mapToDouble(Shape::calculateArea)
                    .sum();
    }
}
```

#### **5.3 SOLID 원칙들의 시너지**

SOLID 원칙들은 **독립적이지 않습니다**. 서로 상호작용하면서 **강력한 설계 철학**을 형성합니다:

```java
// SOLID 원칙이 모두 적용된 종합 예제
// SRP: 각 클래스는 단일 책임
// OCP: 새로운 알림 방식 추가 시 기존 코드 수정 없음
// LSP: 모든 NotificationSender 구현체는 치환 가능
// ISP: 클라이언트가 사용하지 않는 메서드에 의존하지 않음
// DIP: 고수준 모듈이 저수준 모듈에 의존하지 않음

// 추상화 (DIP, ISP)
public interface NotificationSender {
    void send(String recipient, String message);
}

public interface NotificationFormatter {
    String format(String message, NotificationMetadata metadata);
}

// 구체 구현들 (SRP, LSP)
public class EmailNotificationSender implements NotificationSender {
    @Override
    public void send(String recipient, String message) {
        // 이메일 발송 로직
    }
}

public class SMSNotificationSender implements NotificationSender {
    @Override
    public void send(String recipient, String message) {
        // SMS 발송 로직
    }
}

public class HTMLNotificationFormatter implements NotificationFormatter {
    @Override
    public String format(String message, NotificationMetadata metadata) {
        return "<html><body>" + message + "</body></html>";
    }
}

// 고수준 모듈 (OCP, DIP)
public class NotificationService {
    private final NotificationSender sender;
    private final NotificationFormatter formatter;
    
    public NotificationService(NotificationSender sender, NotificationFormatter formatter) {
        this.sender = sender;
        this.formatter = formatter;
    }
    
    public void sendNotification(String recipient, String message, NotificationMetadata metadata) {
        String formattedMessage = formatter.format(message, metadata);
        sender.send(recipient, formattedMessage);
    }
}

// 새로운 알림 방식 추가 (OCP)
public class SlackNotificationSender implements NotificationSender {
    @Override
    public void send(String recipient, String message) {
        // Slack 메시지 발송 로직
    }
}

// 사용 (DIP)
public class NotificationServiceFactory {
    public static NotificationService createEmailService() {
        return new NotificationService(
            new EmailNotificationSender(),
            new HTMLNotificationFormatter()
        );
    }
    
    public static NotificationService createSMSService() {
        return new NotificationService(
            new SMSNotificationSender(),
            new PlainTextNotificationFormatter()
        );
    }
}
```

### **6. 현대적 관점에서 본 객체지향**

#### **6.1 함수형 프로그래밍과의 융합**

현대의 객체지향은 **순수하지 않습니다**. 함수형 프로그래밍의 좋은 아이디어들을 적극적으로 받아들이고 있습니다:

```java
// 전통적인 객체지향 (가변 상태)
public class TraditionalOrderProcessor {
    private List<Order> processedOrders = new ArrayList<>();
    
    public void processOrders(List<Order> orders) {
        for (Order order : orders) {
            if (order.isValid()) {
                order.setStatus(OrderStatus.PROCESSED);
                processedOrders.add(order);
            }
        }
    }
}

// 함수형 아이디어를 접목한 객체지향 (불변성 + 함수 조합)
public class ModernOrderProcessor {
    public List<Order> processOrders(List<Order> orders) {
        return orders.stream()
            .filter(Order::isValid)
            .map(this::processOrder)
            .collect(Collectors.toList());
    }
    
    private Order processOrder(Order order) {
        return order.withStatus(OrderStatus.PROCESSED);  // 불변 객체 반환
    }
}

// 불변 객체 설계
public class Order {
    private final String id;
    private final OrderStatus status;
    private final List<OrderItem> items;
    
    public Order(String id, OrderStatus status, List<OrderItem> items) {
        this.id = id;
        this.status = status;
        this.items = List.copyOf(items);  // 방어적 복사
    }
    
    public Order withStatus(OrderStatus newStatus) {
        return new Order(this.id, newStatus, this.items);
    }
    
    public boolean isValid() {
        return !items.isEmpty() && items.stream().allMatch(OrderItem::isValid);
    }
}
```

#### **6.2 DDD(Domain-Driven Design)와의 연결**

DDD는 객체지향 설계에 **비즈니스 도메인의 복잡성**을 다루는 방법론을 제공합니다:

```java
// DDD 스타일의 객체지향 설계
public class BankAccount {  // Aggregate Root
    private final AccountId accountId;
    private final CustomerId customerId;
    private Money balance;
    private final List<Transaction> transactions;
    
    public BankAccount(AccountId accountId, CustomerId customerId, Money initialDeposit) {
        if (initialDeposit.isNegative()) {
            throw new IllegalArgumentException("초기 입금액은 양수여야 합니다");
        }
        
        this.accountId = accountId;
        this.customerId = customerId;
        this.balance = initialDeposit;
        this.transactions = new ArrayList<>();
        
        // 도메인 이벤트 발생
        DomainEvents.raise(new AccountOpenedEvent(accountId, customerId, initialDeposit));
    }
    
    public void withdraw(Money amount) {
        if (amount.isNegative()) {
            throw new IllegalArgumentException("출금액은 양수여야 합니다");
        }
        
        if (balance.isLessThan(amount)) {
            throw new InsufficientBalanceException("잔액이 부족합니다");
        }
        
        this.balance = balance.subtract(amount);
        this.transactions.add(new Transaction(TransactionType.WITHDRAWAL, amount));
        
        DomainEvents.raise(new MoneyWithdrawnEvent(accountId, amount, balance));
    }
    
    public void deposit(Money amount) {
        if (amount.isNegative()) {
            throw new IllegalArgumentException("입금액은 양수여야 합니다");
        }
        
        this.balance = balance.add(amount);
        this.transactions.add(new Transaction(TransactionType.DEPOSIT, amount));
        
        DomainEvents.raise(new MoneyDepositedEvent(accountId, amount, balance));
    }
    
    // 도메인 로직이 객체 내부에 캡슐화됨
    public boolean canWithdraw(Money amount) {
        return balance.isGreaterThanOrEqual(amount);
    }
}

// Value Object
public class Money {
    private final BigDecimal amount;
    private final Currency currency;
    
    public Money(BigDecimal amount, Currency currency) {
        if (amount == null || currency == null) {
            throw new IllegalArgumentException("금액과 통화는 null일 수 없습니다");
        }
        this.amount = amount;
        this.currency = currency;
    }
    
    public Money add(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("다른 통화는 더할 수 없습니다");
        }
        return new Money(amount.add(other.amount), currency);
    }
    
    public boolean isGreaterThanOrEqual(Money other) {
        return amount.compareTo(other.amount) >= 0;
    }
    
    // 불변 객체로 설계
    @Override
    public boolean equals(Object obj) { /* equals 구현 */ }
    @Override
    public int hashCode() { /* hashCode 구현 */ }
}
```

### **결론: 객체지향 설계의 본질**

객체지향은 **"현실 세계 모델링"**이 아닙니다. 그것은 **복잡한 소프트웨어 시스템을 다루기 위한 강력한 사고 도구**입니다.

#### **객체지향의 진정한 가치:**

1. **책임의 명확한 분배**: 각 객체는 명확한 책임을 가지고, 그 책임을 완전히 수행합니다.

2. **변경에 대한 유연한 대응**: 추상화와 다형성을 통해 요구사항 변경에 유연하게 대응할 수 있습니다.

3. **복잡성의 효과적 관리**: 캡슐화를 통해 복잡성을 국소화하고, 인터페이스를 통해 단순화합니다.

4. **재사용성과 확장성**: 잘 설계된 객체지향 코드는 재사용과 확장이 용이합니다.

#### **디자인 패턴과의 연결:**

디자인 패턴은 이러한 객체지향 원칙들의 **구체적 적용 사례**입니다:

- **Strategy 패턴**: OCP와 DIP의 구현체
- **Observer 패턴**: 느슨한 결합과 메시지 기반 통신
- **Factory 패턴**: DIP와 객체 생성 책임의 분리
- **Decorator 패턴**: OCP와 컴포지션의 활용

객체지향을 이해한다는 것은 단순히 클래스와 상속을 아는 것이 아닙니다. 그것은 **"어떻게 책임을 분배하고, 어떻게 협력하게 할 것인가"**에 대한 깊은 통찰을 갖는 것입니다.

다음 글에서는 이러한 객체지향 원칙들이 어떻게 **Factory 패턴군**으로 구현되는지 살펴보겠습니다. 객체 생성이라는 책임을 어떻게 분리하고 관리할지에 대한 여정이 시작됩니다.

---

**💡 핵심 메시지:**
"객체지향은 단순한 프로그래밍 기법이 아니라 복잡한 문제를 다룰 수 있는 강력한 사고 방식이며, 디자인 패턴은 이러한 사고 방식이 구체화된 형태이다." 