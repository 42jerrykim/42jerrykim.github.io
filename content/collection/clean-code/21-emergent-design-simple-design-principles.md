---
draft: true
---
# 12장: 창발성

## 강의 목표
- 창발적 설계를 통한 깔끔한 코드 구현 방법 이해
- 단순한 설계 규칙 4가지 습득과 적용
- 코드 중복 제거와 표현력 향상 기법 학습

## 내용 구성 전략

### 창발적 설계로 깔끔한 코드를 구현하자
**접근 방법**:
- 창발성(Emergence) 개념의 이해
- 단순한 규칙에서 복잡한 시스템이 나오는 원리

**주요 내용**:
- 단순한 설계 규칙을 따르면 우수한 설계가 '창발'한다
- 켄트 벡이 제시한 단순한 설계 규칙 네 개가 소프트웨어 설계 품질을 크게 높여준다
- 이 규칙들을 따르면 코드 구조와 설계를 파악하기 쉬워진다

**창발성의 정의**:
- 창발성이란 단순한 요소들이 상호작용하여 복잡하고 예상치 못한 특성이나 행동이 나타나는 현상
- 소프트웨어에서는 단순한 설계 원칙들이 상호작용하여 우수한 전체 아키텍처가 나타나는 것

### 단순한 설계 규칙 4가지
**접근 방법**:
- 켄트 벡의 단순한 설계 규칙 소개
- 중요도 순서에 따른 규칙 배열

**주요 내용**:
켄트 벡이 제시한 단순한 설계 규칙은 다음과 같다 (중요도 순):

1. **모든 테스트를 실행한다**
2. **중복을 없앤다**
3. **프로그래머 의도를 표현한다**
4. **클래스와 메서드 수를 최소로 줄인다**

이 규칙들을 따르면 코드의 구조와 설계를 파악하기 쉬워진다.

### 단순한 설계 규칙 1: 모든 테스트를 실행하라
**접근 방법**:
- 테스트 가능한 시스템의 특징
- 테스트가 설계에 미치는 영향

**주요 내용**:
- 설계는 의도한 대로 돌아가는 시스템을 내놓아야 한다
- 문서로는 시스템을 완벽하게 설계했지만, 시스템이 의도한 대로 돌아가는지 검증할 간단한 방법이 없다면, 문서 작성을 위해 투자한 노력에 대한 가치는 인정받기 힘들다
- 테스트를 철저히 거쳐 모든 테스트 케이스를 항상 통과하는 시스템은 '테스트가 가능한 시스템'이다

**테스트가 가능한 시스템의 특징**:
```java
// Bad: 테스트하기 어려운 코드
public class OrderProcessor {
    public void processOrder(Order order) {
        // 직접적인 의존성
        EmailService emailService = new EmailService();
        DatabaseService dbService = new DatabaseService();
        
        // 하드코딩된 로직
        if (order.getTotal() > 1000) {
            emailService.sendEmail(order.getCustomer().getEmail(), 
                "Your order exceeds $1000");
        }
        
        // 현재 시간에 직접 의존
        order.setProcessedDate(new Date());
        
        dbService.save(order);
    }
}

// Good: 테스트 가능한 코드
public class OrderProcessor {
    private final EmailService emailService;
    private final DatabaseService dbService;
    private final Clock clock;
    
    public OrderProcessor(EmailService emailService, 
                         DatabaseService dbService, 
                         Clock clock) {
        this.emailService = emailService;
        this.dbService = dbService;
        this.clock = clock;
    }
    
    public void processOrder(Order order) {
        if (order.getTotal() > 1000) {
            sendHighValueOrderNotification(order);
        }
        
        order.setProcessedDate(clock.getCurrentTime());
        dbService.save(order);
    }
    
    private void sendHighValueOrderNotification(Order order) {
        emailService.sendEmail(order.getCustomer().getEmail(), 
            "Your order exceeds $1000");
    }
}

// 테스트 코드
@Test
public void shouldSendEmailForHighValueOrder() {
    // Given
    EmailService mockEmailService = mock(EmailService.class);
    DatabaseService mockDbService = mock(DatabaseService.class);
    Clock mockClock = mock(Clock.class);
    Date fixedDate = new Date();
    when(mockClock.getCurrentTime()).thenReturn(fixedDate);
    
    OrderProcessor processor = new OrderProcessor(
        mockEmailService, mockDbService, mockClock);
    
    Order highValueOrder = new Order();
    highValueOrder.setTotal(1500);
    Customer customer = new Customer("test@example.com");
    highValueOrder.setCustomer(customer);
    
    // When
    processor.processOrder(highValueOrder);
    
    // Then
    verify(mockEmailService).sendEmail("test@example.com", 
        "Your order exceeds $1000");
    assertEquals(fixedDate, highValueOrder.getProcessedDate());
}
```

**테스트가 설계에 미치는 긍정적 영향**:
- 크기가 작고 목적 하나만 수행하는 클래스가 나온다
- SRP를 준수하는 클래스는 테스트가 훨씬 더 쉽다
- 결합도가 높으면 테스트 작성이 어렵다
- DIP와 같은 원칙을 적용하고 의존성 주입, Mock 객체, 인터페이스를 사용해 테스트 케이스를 작성한다

### 단순한 설계 규칙 2-4: 리팩토링
**접근 방법**:
- 테스트 케이스 작성 후 리팩토링 단계
- 중복 제거, 표현력 향상, 구조 개선

**주요 내용**:
- 테스트 케이스를 모두 작성했다면 이제 코드와 클래스를 정리해도 괜찮다
- 구체적으로는 코드를 점진적으로 리팩토링해 나간다
- 테스트 케이스가 있으니까 코드를 정리하면서 시스템이 깨질까 걱정할 필요가 없다

### 중복을 없애라
**접근 방법**:
- 중복의 다양한 형태 식별
- 중복 제거 기법과 패턴

**주요 내용**:
- 우수한 설계에서 중복은 커다란 적이다
- 중복은 추가 작업, 추가 위험, 불필요한 복잡도를 뜻한다
- 중복은 여러 가지 형태로 나타난다

#### 12.5.1 명백한 중복
**예시**:
```java
// Bad: 명백한 중복
public class VacationPolicy {
    public void accrueUSDivisionVacation() {
        // 미국 직원 휴가 적립 로직
        // 근무 개월 수 계산
        // 휴가 일수 계산
        // 데이터베이스 업데이트
    }
    
    public void accrueEUDivisionVacation() {
        // 유럽 직원 휴가 적립 로직  
        // 근무 개월 수 계산
        // 휴가 일수 계산 (다른 정책)
        // 데이터베이스 업데이트
    }
}

// Good: 중복 제거
public abstract class VacationPolicy {
    public void accrueVacation() {
        int monthsWorked = calculateMonthsWorked();
        int vacationDays = calculateVacationDays(monthsWorked);
        updateDatabase(vacationDays);
    }
    
    protected abstract int calculateVacationDays(int monthsWorked);
    
    private int calculateMonthsWorked() {
        // 공통 로직
    }
    
    private void updateDatabase(int vacationDays) {
        // 공통 로직
    }
}

public class USVacationPolicy extends VacationPolicy {
    @Override
    protected int calculateVacationDays(int monthsWorked) {
        // 미국 휴가 정책에 따른 계산
        return monthsWorked * 2;
    }
}

public class EUVacationPolicy extends VacationPolicy {
    @Override
    protected int calculateVacationDays(int monthsWorked) {
        // 유럽 휴가 정책에 따른 계산
        return monthsWorked * 3;
    }
}
```

#### 12.5.2 더 미묘한 중복
**예시**:
```java
// Bad: 미묘한 중복 (구조적 중복)
public class Line {
    public Line(Point start, Point end) {
        this.start = start;
        this.end = end;
    }
    
    public double getLength() {
        double dx = end.x - start.x;
        double dy = end.y - start.y;
        return Math.sqrt(dx*dx + dy*dy);
    }
}

public class Rectangle {
    private Point topLeft;
    private Point bottomRight;
    
    public double getDiagonalLength() {
        double dx = bottomRight.x - topLeft.x;
        double dy = bottomRight.y - topLeft.y;
        return Math.sqrt(dx*dx + dy*dy);
    }
}

// Good: 중복 제거
public class Point {
    public final double x, y;
    
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }
    
    public double distanceTo(Point other) {
        double dx = other.x - this.x;
        double dy = other.y - this.y;
        return Math.sqrt(dx*dx + dy*dy);
    }
}

public class Line {
    private Point start, end;
    
    public Line(Point start, Point end) {
        this.start = start;
        this.end = end;
    }
    
    public double getLength() {
        return start.distanceTo(end);
    }
}

public class Rectangle {
    private Point topLeft;
    private Point bottomRight;
    
    public double getDiagonalLength() {
        return topLeft.distanceTo(bottomRight);
    }
}
```

#### 12.5.3 Template Method 패턴을 활용한 중복 제거
**예시**:
```java
// Bad: 중복된 고차원 정책
public class HourlyEmployee {
    public Money calculatePay() {
        int straightTime = Math.min(40, timeCard.getHours());
        int overTime = Math.max(0, timeCard.getHours() - 40);
        int straightPay = straightTime * payRate;
        int overtimePay = (int)Math.round(overTime * payRate * 1.5);
        return new Money(straightPay + overtimePay);
    }
}

public class SalariedEmployee {
    public Money calculatePay() {
        return new Money(salary);
    }
}

// Good: Template Method 패턴 적용
public abstract class Employee {
    public Money calculatePay() {
        int regularHours = calculateRegularHours();
        int overtimeHours = calculateOvertimeHours();
        int regularPay = regularHours * getRegularRate();
        int overtimePay = overtimeHours * getOvertimeRate();
        return new Money(regularPay + overtimePay);
    }
    
    protected abstract int getRegularRate();
    protected abstract int getOvertimeRate();
    
    private int calculateRegularHours() {
        return Math.min(40, timeCard.getHours());
    }
    
    private int calculateOvertimeHours() {
        return Math.max(0, timeCard.getHours() - 40);
    }
}

public class HourlyEmployee extends Employee {
    @Override
    protected int getRegularRate() {
        return payRate;
    }
    
    @Override
    protected int getOvertimeRate() {
        return (int)Math.round(payRate * 1.5);
    }
}

public class SalariedEmployee extends Employee {
    @Override
    protected int getRegularRate() {
        return salary / 2080; // 연봉을 시간당으로 환산
    }
    
    @Override
    protected int getOvertimeRate() {
        return 0; // 급여직원은 초과근무수당 없음
    }
}
```

### 표현하라
**접근 방법**:
- 코드의 의도를 명확하게 표현하는 방법
- 가독성과 유지보수성 향상 기법

**주요 내용**:
- 소프트웨어 프로젝트 비용 중 대다수는 장기적인 유지보수에 들어간다
- 시스템이 점차 복잡해지면서 유지보수 개발자가 시스템을 이해하느라 보내는 시간은 늘어만 간다
- 코드는 개발자의 의도를 분명히 표현해야 한다

#### 12.6.1 표현력을 높이는 방법들

**1. 좋은 이름 선택하기**
```java
// Bad: 모호한 이름
public class DtaRcrd102 {
    private Date genymdhms;
    private Date modymdhms;
    private final String pszqint = "102";
}

// Good: 의미있는 이름
public class Customer {
    private Date generationTimestamp;
    private Date modificationTimestamp;
    private final String recordId = "102";
}
```

**2. 함수와 클래스 크기를 작게 유지하기**
```java
// Bad: 큰 함수
public void processOrder(Order order) {
    // 100줄의 복잡한 로직
    // 주문 검증, 재고 확인, 결제 처리, 배송 등
}

// Good: 작은 함수들로 분해
public void processOrder(Order order) {
    validateOrder(order);
    checkInventory(order);
    processPayment(order);
    scheduleShipping(order);
}

private void validateOrder(Order order) { /* ... */ }
private void checkInventory(Order order) { /* ... */ }
private void processPayment(Order order) { /* ... */ }
private void scheduleShipping(Order order) { /* ... */ }
```

**3. 표준 명칭 사용하기**
```java
// Command 패턴 사용 예시
public interface Command {
    void execute();
    void undo();
}

public class DeleteFileCommand implements Command {
    private File file;
    private boolean wasDeleted;
    
    public DeleteFileCommand(File file) {
        this.file = file;
    }
    
    @Override
    public void execute() {
        wasDeleted = file.delete();
    }
    
    @Override
    public void undo() {
        if (wasDeleted) {
            // 파일 복원 로직
        }
    }
}
```

**4. 단위 테스트 케이스를 꼼꼼히 작성하기**
```java
@Test
public void shouldCalculateAreaCorrectlyForRectangle() {
    // Given
    Rectangle rectangle = new Rectangle(5, 3);
    
    // When
    double area = rectangle.calculateArea();
    
    // Then
    assertEquals(15.0, area, 0.001);
}

@Test
public void shouldReturnZeroAreaForNegativeDimensions() {
    // Given
    Rectangle rectangle = new Rectangle(-5, 3);
    
    // When
    double area = rectangle.calculateArea();
    
    // Then
    assertEquals(0.0, area, 0.001);
}
```

### 클래스와 메서드 수를 최소로 줄여라
**접근 방법**:
- 과도한 추상화의 위험성
- 실용적인 접근법의 중요성

**주요 내용**:
- 때로는 무의미하고 독단적인 정책 탓에 클래스 수와 메서드 수가 늘어나기도 한다
- 클래스마다 무조건 인터페이스를 생성하라고 요구하는 구현 표준이 좋은 예다
- 자료 클래스와 동작 클래스는 무조건 분리해야 한다고 주장하는 개발자도 좋은 예다
- 가능한 독단적인 견해는 멀리하고 실용적인 방식을 택한다

**균형잡힌 접근법**:
```java
// Bad: 과도한 추상화
public interface UserDataAccessInterface {
    UserEntity getUserEntityById(Long id);
}

public class UserDataAccessImplementation implements UserDataAccessInterface {
    @Override
    public UserEntity getUserEntityById(Long id) {
        // 구현
    }
}

public interface UserBusinessLogicInterface {
    UserDTO processUserBusinessLogic(Long id);
}

public class UserBusinessLogicImplementation implements UserBusinessLogicInterface {
    // 구현
}

// Good: 실용적인 접근
public class UserRepository {
    public User findById(Long id) {
        // 구현
    }
}

public class UserService {
    private UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public User getUser(Long id) {
        return userRepository.findById(id);
    }
}
```

**우선순위**:
이 규칙은 함수와 클래스 수를 가능한 줄이라고 제안한다. 하지만 이 규칙은 4개 규칙 중 우선순위가 가장 낮다:

1. 테스트 케이스 작성
2. 중복 제거  
3. 의도 표현
4. **클래스와 메서드 수 최소화** ← 가장 낮은 우선순위

### 결론
**접근 방법**:
- 단순한 설계 규칙의 종합적 적용
- 지속적인 개선의 중요성

**주요 내용**:
- 경험을 대신할 단순한 개발 기법이 있을까? 당연히 없다
- 하지만 이 장에서 소개한 기법은 켄트 벡이 수십 년간 쌓은 경험의 정수다
- 이 규칙들을 따르면 우수한 기법과 원칙을 단번에 활용할 수 있다

## 강의 진행 방식
1. **도입 (10분)**: 창발성 개념과 사례 소개
2. **이론 (25분)**: 단순한 설계 규칙 4가지 상세 설명
3. **실습 (40분)**: 중복 제거와 표현력 향상 리팩토링
4. **회고 (15분)**: 설계 개선 과정 공유 및 토론

## 실습 과제
1. **중복 제거**: 제공된 코드에서 다양한 형태의 중복 찾기 및 제거
2. **표현력 향상**: 의도가 불분명한 코드를 명확하게 표현하도록 개선
3. **테스트 주도 리팩토링**: 테스트를 먼저 작성한 후 안전하게 리팩토링

## 평가 기준
- 중복 식별 및 제거 능력 (35%)
- 코드 표현력 향상 능력 (35%)
- 단순한 설계 규칙 종합 적용 (30%)

## 창발적 설계 체크리스트
- [ ] 모든 테스트가 통과하는가?
- [ ] 명백한 중복이 제거되었는가?
- [ ] 구조적/의미적 중복도 제거되었는가?
- [ ] 코드가 의도를 명확히 표현하는가?
- [ ] 클래스와 메서드 이름이 적절한가?
- [ ] 함수와 클래스 크기가 적당한가?
- [ ] 표준 명칭을 적절히 사용했는가?
- [ ] 단위 테스트가 코드를 설명하는가?
- [ ] 과도한 추상화를 피했는가?

## 리팩토링 우선순위
1. **테스트 케이스 확보** (안전망 구축)
2. **중복 제거** (구조 개선)
3. **의도 표현** (가독성 향상)
4. **크기 최소화** (복잡도 감소)

## 추가 자료
- Kent Beck의 "Extreme Programming Explained"
- Martin Fowler의 "Refactoring: Improving the Design of Existing Code"
- "Design Patterns" Gang of Four
- "Effective Java" - Joshua Bloch
- 실제 오픈소스 프로젝트의 리팩토링 사례 