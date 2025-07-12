---
draft: true
---
# 10장: 클래스

## 강의 목표
- 클래스 설계의 기본 원칙과 체계 이해
- 단일 책임 원칙(SRP)과 응집도 개념 습득
- 변경에 유연한 클래스 구조 설계 능력 개발

## 내용 구성 전략

### 10.1 클래스 체계
**접근 방법**:
- 자바 관례에 따른 클래스 내부 구성 순서
- 캡슐화와 정보 은닉의 중요성

**주요 내용**:
- 클래스 정의는 변수 목록으로 시작한다
- 정적 공개 상수가 있다면 맨 먼저 나온다
- 다음으로 정적 비공개 변수가 나오며, 이어서 비공개 인스턴스 변수가 나온다
- 공개 변수가 필요한 경우는 거의 없다
- 변수 목록 다음에는 공개 함수가 나온다
- 비공개 함수는 자신을 호출하는 공개 함수 직후에 넣는다

**클래스 체계 예시**:
```java
public class SuperDashboard extends JFrame implements MetaDataUser {
    // 1. 정적 공개 상수
    public static final String COMPONENT_SIZING_ERROR = "Cannot size component";
    
    // 2. 정적 비공개 변수
    private static final String TAG = "SuperDashboard";
    
    // 3. 비공개 인스턴스 변수
    private boolean useSSL;
    private String userName;
    private String password;
    
    // 4. 공개 함수
    public SuperDashboard() {
        initialize();
    }
    
    public void setUserName(String userName) {
        this.userName = userName;
    }
    
    public String getUserName() {
        return userName;
    }
    
    public void processLogin() {
        if (isValidUser()) {
            performLogin();
        }
    }
    
    // 5. 비공개 함수 (호출하는 공개 함수 직후)
    private void initialize() {
        // 초기화 로직
    }
    
    private boolean isValidUser() {
        // 유효성 검증 로직
        return userName != null && password != null;
    }
    
    private void performLogin() {
        // 로그인 수행 로직
    }
}
```

#### 10.1.1 캡슐화
**접근 방법**:
- 변수와 유틸리티 함수의 공개 여부 결정
- 테스트를 위한 접근성과 캡슐화의 균형

**주요 내용**:
- 변수와 유틸리티 함수는 가능한 한 공개하지 않는 편이 낫지만 반드시 숨겨야 한다는 법칙도 없다
- 때로는 변수나 유틸리티 함수를 protected로 선언해 테스트 코드에 접근을 허용하기도 한다
- 하지만 그 전에 비공개 상태를 유지할 온갖 방법을 강구한다
- 캡슐화를 풀어주는 결정은 언제나 최후의 수단이다

### 10.2 클래스는 작아야 한다!
**접근 방법**:
- 클래스 크기의 척도와 기준
- 함수와 클래스에서의 "작음"의 의미 차이

**주요 내용**:
- 클래스를 만들 때 첫 번째 규칙은 크기다. 클래스는 작아야 한다
- 두 번째 규칙도 크기다. 더 작아야 한다
- 함수는 물리적인 행 수로 크기를 측정했다. 클래스는 다른 척도를 사용한다
- 클래스가 맡은 **책임**을 센다

**크기 측정 예시**:
```java
// Bad: 너무 많은 책임을 가진 클래스 (70개 이상의 공개 메서드)
public class SuperDashboard extends JFrame implements MetaDataUser {
    public Component getLastFocusedComponent()
    public void setLastFocused(Component lastFocused)
    public int getMajorVersionNumber()
    public int getMinorVersionNumber()
    public int getBuildNumber()
    public void addVersionListener(VersionListener listener)
    public void removeVersionListener(VersionListener listener)
    public void fireVersionListeners(MetaData metadata)
    public void addPropertyChangeListener(PropertyChangeListener listener)
    public void removePropertyChangeListener(PropertyChangeListener listener)
    public void firePropertyChangeListeners(String propertyName, Object oldValue, Object newValue)
    // ... 60개 이상의 메서드가 더 있음
}

// Good: 단일 책임으로 분리된 클래스들
public class Version {
    public int getMajorVersionNumber()
    public int getMinorVersionNumber() 
    public int getBuildNumber()
}

public class VersionNotifier {
    public void addVersionListener(VersionListener listener)
    public void removeVersionListener(VersionListener listener)
    public void fireVersionListeners(MetaData metadata)
}

public class PropertyChangeNotifier {
    public void addPropertyChangeListener(PropertyChangeListener listener)
    public void removePropertyChangeListener(PropertyChangeListener listener)
    public void firePropertyChangeListeners(String propertyName, Object oldValue, Object newValue)
}
```

#### 10.2.1 단일 책임 원칙
**접근 방법**:
- SRP(Single Responsibility Principle)의 개념과 적용
- 변경할 이유가 하나여야 한다는 원칙

**주요 내용**:
- 단일 책임 원칙(SRP)은 클래스나 모듈을 변경할 이유가 하나, 단 하나뿐이어야 한다는 원칙이다
- 책임, 즉 변경할 이유를 파악하려 애쓰다 보면 코드를 추상화하기도 쉬워진다
- 더 좋은 추상화가 더 쉽게 떠오른다

**SRP 위반 예시**:
```java
// Bad: SRP 위반 - 여러 책임을 가짐
public class Employee {
    // 직원 정보 관리 책임
    private String name;
    private String address;
    private String phoneNumber;
    
    // 급여 계산 책임
    public Money calculatePay() {
        // 급여 계산 로직
        return new Money(salary);
    }
    
    // 데이터베이스 저장 책임
    public void save() {
        // 데이터베이스에 저장
    }
    
    // 보고서 생성 책임
    public String generateReport() {
        return "Employee Report: " + name;
    }
}

// Good: SRP 준수 - 각각 하나의 책임만 가짐
public class Employee {
    private String name;
    private String address;
    private String phoneNumber;
    
    // 접근자 메서드들만
    public String getName() { return name; }
    public String getAddress() { return address; }
    public String getPhoneNumber() { return phoneNumber; }
}

public class PayCalculator {
    public Money calculatePay(Employee employee) {
        // 급여 계산 로직
        return new Money(employee.getSalary());
    }
}

public class EmployeeRepository {
    public void save(Employee employee) {
        // 데이터베이스에 저장
    }
}

public class EmployeeReporter {
    public String generateReport(Employee employee) {
        return "Employee Report: " + employee.getName();
    }
}
```

**SRP를 지키지 않을 때의 문제점**:
1. 급여 계산 로직이 변경되면 Employee 클래스가 변경됨
2. 데이터베이스 스키마가 변경되면 Employee 클래스가 변경됨
3. 보고서 형식이 변경되면 Employee 클래스가 변경됨

#### 10.2.2 응집도
**접근 방법**:
- 클래스 응집도의 개념과 측정 방법
- 높은 응집도를 가진 클래스의 특징

**주요 내용**:
- 클래스는 인스턴스 변수 수가 작아야 한다
- 각 클래스 메서드는 클래스 인스턴스 변수를 하나 이상 사용해야 한다
- 일반적으로 메서드가 변수를 더 많이 사용할수록 메서드와 클래스는 응집도가 더 높다
- 응집도가 높다는 것은 클래스에 속한 메서드와 변수가 서로 의존하며 논리적인 단위로 뭉쳐진다는 의미다

**응집도 예시**:
```java
// Good: 높은 응집도
public class Stack {
    private int topOfStack = 0;
    private List<Integer> elements = new LinkedList<Integer>();
    
    public int size() { 
        return topOfStack; // topOfStack 사용
    }
    
    public void push(int element) { 
        topOfStack++; // topOfStack 사용
        elements.add(element); // elements 사용
    }
    
    public int pop() throws PoppedWhenEmpty { 
        if (topOfStack == 0) // topOfStack 사용
            throw new PoppedWhenEmpty();
        int element = elements.get(--topOfStack); // topOfStack, elements 사용
        elements.remove(topOfStack); // topOfStack, elements 사용
        return element;
    }
}

// Bad: 낮은 응집도
public class LowCohesion {
    private String name;
    private int age;
    private List<String> hobbies;
    private DatabaseConnection db;
    private Logger logger;
    
    public void setName(String name) {
        this.name = name; // name만 사용
    }
    
    public void setAge(int age) {
        this.age = age; // age만 사용
    }
    
    public void logMessage(String message) {
        logger.log(message); // logger만 사용
    }
    
    public void saveToDatabase() {
        db.save(this); // db만 사용
    }
}
```

#### 10.2.3 응집도를 유지하면 작은 클래스 여럿이 나온다
**접근 방법**:
- 큰 함수를 작은 함수 여럿으로 쪼개는 과정
- 변수 승격과 클래스 분리 과정

**주요 내용**:
- 큰 함수를 작은 함수 여럿으로 쪼개다 보면 종종 작은 클래스 여럿으로 쪼갤 기회가 생긴다
- 그러면 프로그램에 점점 더 체계가 잡히고 구조가 투명해진다

**리팩토링 과정 예시**:
```java
// Before: 긴 함수와 많은 지역 변수
public class LargeClass {
    public void largeMethod() {
        // 100줄 이상의 코드
        String data1, data2, data3;
        int count1, count2, count3;
        
        // data1, count1을 사용하는 로직
        // ...
        
        // data2, count2를 사용하는 로직
        // ...
        
        // data3, count3을 사용하는 로직
        // ...
    }
}

// After: 작은 클래스들로 분리
public class DataProcessor1 {
    private String data;
    private int count;
    
    public DataProcessor1(String data) {
        this.data = data;
        this.count = 0;
    }
    
    public void process() {
        // data와 count를 사용하는 로직
    }
}

public class DataProcessor2 {
    private String data;
    private int count;
    
    public DataProcessor2(String data) {
        this.data = data;
        this.count = 0;
    }
    
    public void process() {
        // data와 count를 사용하는 로직
    }
}

public class DataProcessor3 {
    private String data;
    private int count;
    
    public DataProcessor3(String data) {
        this.data = data;
        this.count = 0;
    }
    
    public void process() {
        // data와 count를 사용하는 로직
    }
}
```

### 10.3 변경하기 쉬운 클래스
**접근 방법**:
- OCP(Open-Closed Principle) 적용
- 새 기능 추가 시 기존 코드 변경 최소화

**주요 내용**:
- 깨끗한 시스템은 클래스를 체계적으로 정리해 변경에 수반하는 위험을 낮춘다
- 새 기능을 수정하거나 기존 기능을 변경할 때 건드릴 코드가 최소인 시스템 구조가 바람직하다
- 이상적인 시스템이라면 새 기능을 추가할 때 시스템을 확장할 뿐 기존 코드를 변경하지는 않는다

**변경하기 어려운 클래스 예시**:
```java
// Bad: 새로운 SQL 문 유형이 추가될 때마다 클래스 수정 필요
public class Sql {
    public Sql(String table, Column[] columns)
    public String create()
    public String insert(Object[] fields)
    public String selectAll()
    public String findByKey(String keyColumn, String keyValue)
    public String select(Column column, String pattern)
    public String select(Criteria criteria)
    public String preparedInsert()
    private String columnList(Column[] columns)
    private String valuesList(Object[] fields, final Column[] columns)
    private String selectWithCriteria(String criteria)
    private String placeholderList(Column[] columns)
}
```

**변경하기 쉬운 클래스 예시**:
```java
// Good: OCP 준수 - 확장에는 열려있고 변경에는 닫혀있음
abstract public class Sql {
    public Sql(String table, Column[] columns) 
    abstract public String generate();
}

public class CreateSql extends Sql {
    public CreateSql(String table, Column[] columns) 
    @Override public String generate()
}

public class SelectSql extends Sql {
    public SelectSql(String table, Column[] columns) 
    @Override public String generate()
}

public class InsertSql extends Sql {
    public InsertSql(String table, Column[] columns, Object[] fields) 
    @Override public String generate()
    private String valuesList(Object[] fields, final Column[] columns)
}

public class SelectWithCriteriaSql extends Sql { 
    public SelectWithCriteriaSql(String table, Column[] columns, Criteria criteria) 
    @Override public String generate()
}

public class SelectWithMatchSql extends Sql { 
    public SelectWithMatchSql(String table, Column[] columns, Column column, String pattern) 
    @Override public String generate()
}

public class FindByKeySql extends Sql { 
    public FindByKeySql(String table, Column[] columns, String keyColumn, String keyValue) 
    @Override public String generate()
}

public class PreparedInsertSql extends Sql {
    public PreparedInsertSql(String table, Column[] columns) 
    @Override public String generate() {
        return String.format("INSERT INTO %s (%s) VALUES (%s)", 
            table, columnList(columns), placeholderList(columns));
    }
    private String placeholderList(Column[] columns)
}
```

#### 10.3.1 변경으로부터 격리
**접근 방법**:
- 의존성 역전 원칙(DIP) 적용
- 인터페이스와 추상 클래스를 통한 격리

**주요 내용**:
- 상세한 구현에 의존하는 클라이언트 클래스는 구현이 바뀌면 위험에 빠진다
- 그래서 우리는 인터페이스와 추상 클래스를 사용해 구현이 미치는 영향을 격리한다
- 상세한 구현에 의존하는 코드는 테스트가 어렵다

**DIP 적용 예시**:
```java
// Bad: 구체적인 구현에 의존
public class Portfolio {
    private TokyoStockExchange exchange;
    
    public Portfolio(TokyoStockExchange exchange) {
        this.exchange = exchange;
    }
    
    public Money value() {
        Money money = Money.zero();
        for (String symbol : portfolio) {
            money = money.add(exchange.currentPrice(symbol));
        }
        return money;
    }
}

// Good: 추상화에 의존
public interface StockExchange {
    Money currentPrice(String symbol);
}

public class Portfolio {
    private StockExchange exchange;
    
    public Portfolio(StockExchange exchange) {
        this.exchange = exchange;
    }
    
    public Money value() {
        Money money = Money.zero();
        for (String symbol : portfolio) {
            money = money.add(exchange.currentPrice(symbol));
        }
        return money;
    }
}

public class TokyoStockExchange implements StockExchange {
    public Money currentPrice(String symbol) {
        // 실제 도쿄 증권 거래소에서 가격을 가져오는 로직
    }
}

// 테스트를 위한 목 객체
public class MockStockExchange implements StockExchange {
    private Map<String, Money> prices = new HashMap<>();
    
    public void setPrice(String symbol, Money price) {
        prices.put(symbol, price);
    }
    
    public Money currentPrice(String symbol) {
        return prices.get(symbol);
    }
}

// 테스트 코드
@Test
public void testPortfolioValue() {
    MockStockExchange exchange = new MockStockExchange();
    exchange.setPrice("AAPL", Money.dollars(100));
    exchange.setPrice("GOOGL", Money.dollars(200));
    
    Portfolio portfolio = new Portfolio(exchange);
    portfolio.add("AAPL");
    portfolio.add("GOOGL");
    
    assertEquals(Money.dollars(300), portfolio.value());
}
```

## 강의 진행 방식
1. **도입 (10분)**: 복잡한 클래스 경험 사례 공유
2. **이론 (25분)**: SRP, 응집도, OCP, DIP 원칙 설명
3. **실습 (40분)**: 큰 클래스를 작은 클래스들로 리팩토링
4. **코드 리뷰 (15분)**: 클래스 설계 품질 검토

## 실습 과제
1. **클래스 분해**: God Class를 SRP를 준수하는 작은 클래스들로 분해
2. **인터페이스 추출**: 변경하기 어려운 클래스에 인터페이스 적용
3. **응집도 개선**: 낮은 응집도의 클래스를 높은 응집도로 리팩토링

## 평가 기준
- SRP 적용 능력 (30%)
- 응집도 이해 및 개선 능력 (35%)
- 변경에 유연한 설계 능력 (35%)

## 클래스 설계 체크리스트
- [ ] 클래스가 하나의 책임만 가지는가? (SRP)
- [ ] 클래스의 크기가 적절한가?
- [ ] 인스턴스 변수 수가 작은가?
- [ ] 메서드들이 인스턴스 변수를 적절히 사용하는가? (응집도)
- [ ] 새로운 기능 추가 시 기존 코드 변경이 최소화되는가? (OCP)
- [ ] 구체적인 구현이 아닌 추상화에 의존하는가? (DIP)
- [ ] 클래스가 테스트하기 쉬운가?
- [ ] 캡슐화가 적절히 유지되는가?

## SOLID 원칙 요약
1. **SRP (Single Responsibility Principle)**: 클래스를 변경할 이유는 하나뿐이어야 한다
2. **OCP (Open-Closed Principle)**: 확장에는 열려 있고 변경에는 닫혀 있어야 한다
3. **LSP (Liskov Substitution Principle)**: 상위 타입의 객체를 하위 타입으로 바꿔도 프로그램이 정상 작동해야 한다
4. **ISP (Interface Segregation Principle)**: 클라이언트는 자신이 사용하지 않는 메서드에 의존하지 않아야 한다
5. **DIP (Dependency Inversion Principle)**: 상위 모듈은 하위 모듈에 의존하면 안 된다

## 추가 자료
- Robert C. Martin의 "Clean Architecture"
- Gang of Four "Design Patterns"
- Refactoring.Guru의 디자인 패턴 설명
- SOLID 원칙에 대한 심화 학습 자료 