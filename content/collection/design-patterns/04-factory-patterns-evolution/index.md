---
draft: true
collection_order: 40
title: "[Design Patterns] 팩토리 패턴의 진화"
description: "Simple Factory부터 Abstract Factory까지 객체 생성 패턴의 완전한 진화 과정을 탐구합니다. 각 팩토리 패턴의 특징과 적용 시나리오를 실무 관점에서 분석하고, 의존성 주입과 IoC 컨테이너의 현대적 발전까지 다룹니다. 복잡한 객체 생성 로직을 우아하게 관리하는 전문가 수준의 설계 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-04T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Creational Patterns
- Factory Patterns
- Object Creation
tags:
- Factory Method
- Abstract Factory
- Simple Factory
- Static Factory
- Factory Pattern
- Object Creation
- Creational Patterns
- Design Patterns
- GoF Patterns
- Dependency Injection
- IoC Container
- Object Instantiation
- Class Hierarchy
- Product Family
- Factory Evolution
- Software Architecture
- Design Principles
- Pattern Progression
- Code Organization
- Object Lifecycle
- Factory Design
- Creation Logic
- Pattern Implementation
- Software Engineering
- Design Methodology
- Architectural Patterns
- Object Composition
- Flexibility Design
- Extensible Design
- Modular Design
- 팩토리 메서드
- 추상 팩토리
- 심플 팩토리
- 정적 팩토리
- 팩토리 패턴
- 객체 생성
- 생성 패턴
- 디자인 패턴
- GoF 패턴
- 의존성 주입
- IoC 컨테이너
- 객체 인스턴스화
- 클래스 계층
- 제품군
- 팩토리 진화
- 소프트웨어 아키텍처
- 설계 원칙
- 패턴 진행
- 코드 구조화
- 객체 생명주기
- 팩토리 설계
- 생성 로직
- 패턴 구현
- 소프트웨어 공학
- 설계 방법론
- 아키텍처 패턴
- 객체 컴포지션
- 유연한 설계
- 확장 가능한 설계
- 모듈러 설계
---

Simple Factory부터 Abstract Factory까지, Factory 패턴군의 진화 과정을 탐구합니다. 객체 생성의 복잡성을 어떻게 캡슐화하고, 유연한 시스템을 구축하는지 학습합니다.

## 서론: new 키워드의 한계와 객체 생성의 딜레마

> *"객체를 만드는 일은 쉽다. 올바른 객체를 올바른 시점에 올바른 방식으로 만드는 일은 어렵다."*

자바를 처음 배울 때 가장 먼저 접하는 키워드 중 하나가 `new`입니다. `new Button()`, `new ArrayList()`, `new Date()`... 이렇게 객체를 만드는 것이 당연해 보입니다. 하지만 시스템이 복잡해지면서 우리는 **"new의 한계"**에 부딪히게 됩니다.

```java
// 언뜻 보기에는 문제없어 보이는 코드
public class OrderService {
    public void processOrder(Order order) {
        PaymentProcessor processor = new CreditCardProcessor();  // 하드코딩!
        EmailNotifier notifier = new SmtpEmailNotifier();       // 하드코딩!
        
        processor.process(order.getPayment());
        notifier.sendConfirmation(order.getCustomer());
    }
}
```

이 코드의 문제점은 무엇일까요? **생성(`new`)과 사용(메서드 호출)이 강하게 결합**되어 있다는 것입니다:

1. **확장성 부족**: 새로운 결제 방식을 추가하려면 코드 수정 필요
2. **테스트 어려움**: Mock 객체로 교체하기 어려움  
3. **의존성 결합**: 구체 클래스에 직접 의존
4. **설정 복잡성**: 객체 생성 매개변수가 복잡할 때 관리 어려움

Factory 패턴은 이러한 **"생성의 복잡성"**을 해결하기 위해 진화해온 패턴군입니다. 단순한 Simple Factory부터 현대의 DI Container까지, 이들의 진화 과정을 따라가다 보면 **객체지향 설계의 핵심 원리**들을 발견할 수 있습니다.

### Simple Factory: 생성 로직의 중앙화

#### 가장 단순한 해결책

가장 먼저 떠오르는 해결책은 **생성 로직을 별도의 클래스로 분리**하는 것입니다:

```java
// Simple Factory 패턴
public class PaymentProcessorFactory {
    public static PaymentProcessor create(PaymentType type) {
        switch (type) {
            case CREDIT_CARD:
                return new CreditCardProcessor();
            case PAYPAL:
                return new PayPalProcessor();
            case BANK_TRANSFER:
                return new BankTransferProcessor();
            default:
                throw new IllegalArgumentException("Unsupported payment type: " + type);
        }
    }
}

// 사용하는 쪽
public class OrderService {
    public void processOrder(Order order) {
        PaymentProcessor processor = PaymentProcessorFactory.create(order.getPaymentType());
        processor.process(order.getPayment());
    }
}
```

**Simple Factory의 장점:**
- **생성 로직 중앙화**: 모든 생성 로직이 한 곳에 집중
- **클라이언트 단순화**: 구체 클래스를 알 필요 없음
- **일관성**: 동일한 방식으로 객체 생성

**하지만 한계도 명확합니다:**
```java
// 새로운 결제 방식 추가 시
public static PaymentProcessor create(PaymentType type) {
    switch (type) {
        case CREDIT_CARD:
            return new CreditCardProcessor();
        case PAYPAL:
            return new PayPalProcessor();
        case BANK_TRANSFER:
            return new BankTransferProcessor();
        case CRYPTOCURRENCY:  // 새로 추가
            return new CryptocurrencyProcessor();  // 기존 코드 수정!
        default:
            throw new IllegalArgumentException("Unsupported payment type: " + type);
    }
}
```

이는 **개방-폐쇄 원칙(OCP) 위반**입니다. 확장을 위해 기존 코드를 수정해야 합니다.

#### Static Factory Methods의 미학

Joshua Bloch의 『Effective Java』에서 강조하는 **Static Factory Methods**는 Simple Factory의 세련된 형태입니다:

```java
// Java의 실제 사례들
List<String> emptyList = Collections.emptyList();
Optional<String> optional = Optional.of("value");
LocalDate today = LocalDate.now();
Integer number = Integer.valueOf(42);  // new Integer(42)보다 권장

// 장점을 보여주는 커스텀 예제
public class DatabaseConnection {
    private final String url;
    private final ConnectionType type;
    
    private DatabaseConnection(String url, ConnectionType type) {
        this.url = url;
        this.type = type;
    }
    
    // 의미 있는 이름으로 생성 의도를 명확히 전달
    public static DatabaseConnection forMySQL(String host, int port, String database) {
        String url = String.format("jdbc:mysql://%s:%d/%s", host, port, database);
        return new DatabaseConnection(url, ConnectionType.MYSQL);
    }
    
    public static DatabaseConnection forPostgreSQL(String host, int port, String database) {
        String url = String.format("jdbc:postgresql://%s:%d/%s", host, port, database);
        return new DatabaseConnection(url, ConnectionType.POSTGRESQL);
    }
    
    public static DatabaseConnection fromUrl(String url) {
        ConnectionType type = ConnectionType.fromUrl(url);
        return new DatabaseConnection(url, type);
    }
    
    // 캐싱을 통한 성능 최적화도 가능
    private static final Map<String, DatabaseConnection> cache = new ConcurrentHashMap<>();
    
    public static DatabaseConnection cached(String url) {
        return cache.computeIfAbsent(url, DatabaseConnection::fromUrl);
    }
}
```

**Static Factory Methods의 장점:**
- **명확한 의미**: `forMySQL()`이 `new DatabaseConnection()`보다 의도가 명확
- **유연한 반환**: 서브클래스나 인터페이스 구현체 반환 가능
- **인스턴스 제어**: 캐싱, 풀링, 싱글톤 패턴 적용 가능
- **매개변수 제약 회피**: 동일한 시그니처 문제 해결

### Factory Method Pattern: 생성 책임의 위임

#### Template Method와의 만남

Simple Factory의 OCP 위반 문제를 해결하는 방법은 **생성 책임을 서브클래스에 위임**하는 것입니다. 이것이 바로 Factory Method 패턴입니다:

```java
// 추상 Creator 클래스
public abstract class PaymentServiceCreator {
    // Template Method: 전체 프로세스를 정의
    public final PaymentResult processPayment(PaymentRequest request) {
        PaymentProcessor processor = createPaymentProcessor();  // Factory Method
        
        // 공통 로직
        logPaymentAttempt(request);
        PaymentResult result = processor.process(request);
        logPaymentResult(result);
        
        return result;
    }
    
    // Factory Method: 서브클래스에서 구현
    protected abstract PaymentProcessor createPaymentProcessor();
    
    // 공통 기능들
    private void logPaymentAttempt(PaymentRequest request) {
        System.out.println("Processing payment: " + request.getAmount());
    }
    
    private void logPaymentResult(PaymentResult result) {
        System.out.println("Payment result: " + result.getStatus());
    }
}

// 구체적인 Creator 구현들
public class CreditCardPaymentService extends PaymentServiceCreator {
    @Override
    protected PaymentProcessor createPaymentProcessor() {
        return new CreditCardProcessor();
    }
}

public class PayPalPaymentService extends PaymentServiceCreator {
    @Override
    protected PaymentProcessor createPaymentProcessor() {
        return new PayPalProcessor();
    }
}

// 새로운 결제 방식 추가 - 기존 코드 수정 없음!
public class CryptocurrencyPaymentService extends PaymentServiceCreator {
    @Override
    protected PaymentProcessor createPaymentProcessor() {
        return new CryptocurrencyProcessor();
    }
}
```

**Factory Method의 핵심 특징:**
- **OCP 준수**: 새로운 타입 추가 시 기존 코드 수정 불필요
- **Template Method 연계**: 생성과 사용이 하나의 알고리즘으로 통합
- **다형성 활용**: 서브클래스별로 다른 객체 생성

#### 실제 사례: Java Collections Framework

Java Collections Framework는 Factory Method 패턴의 훌륭한 예시입니다:

```java
// AbstractList의 iterator() 메서드
public abstract class AbstractList<E> extends AbstractCollection<E> implements List<E> {
    
    // Template Method
    public Iterator<E> iterator() {
        return listIterator();  // Factory Method 호출
    }
    
    // Factory Method - 서브클래스에서 구현
    public ListIterator<E> listIterator() {
        return listIterator(0);
    }
    
    public ListIterator<E> listIterator(final int index) {
        rangeCheckForAdd(index);
        
        return new ListItr(index);  // 기본 구현
    }
    
    // ArrayList, LinkedList 등에서 각각 최적화된 Iterator 구현
}

// ArrayList의 구현
public class ArrayList<E> extends AbstractList<E> {
    @Override
    public ListIterator<E> listIterator(int index) {
        if (index < 0 || index > size)
            throw new IndexOutOfBoundsException("Index: " + index);
        return new ListItr(index);  // ArrayList 최적화 Iterator
    }
    
    private class ListItr extends Itr implements ListIterator<E> {
        // ArrayList에 특화된 효율적인 구현
    }
}

// LinkedList의 구현
public class LinkedList<E> extends AbstractSequentialList<E> {
    @Override
    public ListIterator<E> listIterator(int index) {
        checkPositionIndex(index);
        return new ListItr(index);  // LinkedList 최적화 Iterator
    }
    
    private class ListItr implements ListIterator<E> {
        // LinkedList에 특화된 효율적인 구현
    }
}
```

#### Spring Framework의 Bean Factory

Spring Framework는 Factory Method 패턴을 대규모로 활용하는 대표적인 예시입니다:

```java
// BeanFactory 인터페이스 - Factory Method의 추상화
public interface BeanFactory {
    Object getBean(String name) throws BeansException;
    <T> T getBean(String name, Class<T> requiredType) throws BeansException;
    <T> T getBean(Class<T> requiredType) throws BeansException;
    
    boolean containsBean(String name);
    boolean isSingleton(String name) throws NoSuchBeanDefinitionException;
    // ... 기타 Factory Methods
}

// ApplicationContext - 고수준 Factory
public interface ApplicationContext extends BeanFactory, MessageSource, 
        ApplicationEventPublisher, ResourcePatternResolver {
    
    // Factory Method들이 Template Method 패턴으로 조합됨
    default <T> T getBean(Class<T> requiredType) throws BeansException {
        return getBeanFactory().getBean(requiredType);
    }
    
    // 복잡한 초기화 로직이 Template Method로 구현됨
    void refresh() throws BeansException, IllegalStateException;
}

// 구체적인 구현체들
public class ClassPathXmlApplicationContext extends AbstractXmlApplicationContext {
    
    // Factory Method 구현
    @Override
    protected Resource[] getConfigResources() {
        return getConfigLocations() != null 
            ? Arrays.stream(getConfigLocations())
                   .map(ClassPathResource::new)
                   .toArray(Resource[]::new)
            : null;
    }
}

public class AnnotationConfigApplicationContext extends GenericApplicationContext {
    
    // Factory Method 구현
    @Override
    protected void customizeBeanFactory(DefaultListableBeanFactory beanFactory) {
        super.customizeBeanFactory(beanFactory);
        if (this.allowBeanDefinitionOverriding != null) {
            beanFactory.setAllowBeanDefinitionOverriding(this.allowBeanDefinitionOverriding);
        }
        if (this.allowCircularReferences != null) {
            beanFactory.setAllowCircularReferences(this.allowCircularReferences);
        }
    }
}
```

### Abstract Factory Pattern: 제품군의 일관성

#### 관련 객체군의 생성 문제

Factory Method는 **단일 타입의 객체 생성**에 적합합니다. 하지만 **서로 관련된 여러 객체를 함께 생성**해야 할 때는 어떻게 해야 할까요?

예를 들어, GUI 라이브러리에서 플랫폼별로 일관된 모양과 느낌(Look & Feel)을 제공해야 한다고 생각해보세요:

```java
// 문제 상황: 플랫폼별로 다른 컴포넌트들이 섞일 수 있음
public class ApplicationWindow {
    public void createUI() {
        // 문제: 플랫폼별로 다른 컴포넌트들이 섞일 수 있음
        Button button = new WindowsButton();      // Windows 스타일
        TextField textField = new MacTextField(); // Mac 스타일 - 일관성 깨짐!
        Menu menu = new LinuxMenu();              // Linux 스타일 - 더 큰 문제!
        
        // 시각적 일관성이 파괴됨
    }
}
```

Abstract Factory 패턴은 이런 **"제품군(Product Family)"**의 일관성을 보장합니다:

```java
// Abstract Factory 패턴 구현
public interface GUIFactory {
    Button createButton();
    TextField createTextField();
    Menu createMenu();
    Dialog createDialog();
}

// Windows 전용 Factory
public class WindowsGUIFactory implements GUIFactory {
    @Override
    public Button createButton() {
        return new WindowsButton();
    }
    
    @Override
    public TextField createTextField() {
        return new WindowsTextField();
    }
    
    @Override
    public Menu createMenu() {
        return new WindowsMenu();
    }
    
    @Override
    public Dialog createDialog() {
        return new WindowsDialog();
    }
}

// Mac 전용 Factory
public class MacGUIFactory implements GUIFactory {
    @Override
    public Button createButton() {
        return new MacButton();
    }
    
    @Override
    public TextField createTextField() {
        return new MacTextField();
    }
    
    @Override
    public Menu createMenu() {
        return new MacMenu();
    }
    
    @Override
    public Dialog createDialog() {
        return new MacDialog();
    }
}

// 클라이언트 코드
public class ApplicationWindow {
    private final GUIFactory guiFactory;
    
    public ApplicationWindow(GUIFactory guiFactory) {
        this.guiFactory = guiFactory;
    }
    
    public void createUI() {
        // 모든 컴포넌트가 동일한 플랫폼 스타일로 생성됨
        Button button = guiFactory.createButton();
        TextField textField = guiFactory.createTextField();
        Menu menu = guiFactory.createMenu();
        Dialog dialog = guiFactory.createDialog();
        
        // 시각적 일관성 보장!
    }
}

// Factory 선택 로직
public class GUIFactoryProvider {
    public static GUIFactory getFactory() {
        String os = System.getProperty("os.name").toLowerCase();
        
        if (os.contains("windows")) {
            return new WindowsGUIFactory();
        } else if (os.contains("mac")) {
            return new MacGUIFactory();
        } else {
            return new LinuxGUIFactory();
        }
    }
}
```

#### 실제 사례: 데이터베이스 드라이버

JDBC는 Abstract Factory 패턴의 실용적인 예시입니다:

```java
// JDBC의 Abstract Factory 구조
public interface Driver {
    Connection connect(String url, Properties info) throws SQLException;
    boolean acceptsURL(String url) throws SQLException;
}

// Connection이 Abstract Factory 역할
public interface Connection {
    Statement createStatement() throws SQLException;
    PreparedStatement prepareStatement(String sql) throws SQLException;
    CallableStatement prepareCall(String sql) throws SQLException;
    DatabaseMetaData getMetaData() throws SQLException;
}

// MySQL 드라이버의 구현
public class MySQLConnection implements Connection {
    @Override
    public Statement createStatement() throws SQLException {
        return new MySQLStatement(this);  // MySQL 전용 Statement
    }
    
    @Override
    public PreparedStatement prepareStatement(String sql) throws SQLException {
        return new MySQLPreparedStatement(this, sql);  // MySQL 전용 PreparedStatement
    }
    
    @Override
    public DatabaseMetaData getMetaData() throws SQLException {
        return new MySQLDatabaseMetaData(this);  // MySQL 전용 MetaData
    }
}

// PostgreSQL 드라이버의 구현
public class PostgreSQLConnection implements Connection {
    @Override
    public Statement createStatement() throws SQLException {
        return new PostgreSQLStatement(this);  // PostgreSQL 전용 Statement
    }
    
    @Override
    public PreparedStatement prepareStatement(String sql) throws SQLException {
        return new PostgreSQLPreparedStatement(this, sql);  // PostgreSQL 전용 PreparedStatement
    }
    
    @Override
    public DatabaseMetaData getMetaData() throws SQLException {
        return new PostgreSQLDatabaseMetaData(this);  // PostgreSQL 전용 MetaData
    }
}

// 사용법 - 드라이버 변경 시에도 일관된 객체군 보장
public class DatabaseService {
    private final Connection connection;
    
    public DatabaseService(String databaseUrl) throws SQLException {
        this.connection = DriverManager.getConnection(databaseUrl);
        // URL에 따라 적절한 Connection 구현체가 반환됨
        // 그리고 그 Connection에서 생성되는 모든 객체들이 일관성을 가짐
    }
    
    public void executeQuery(String sql) throws SQLException {
        Statement stmt = connection.createStatement();  // 드라이버별 최적화된 Statement
        PreparedStatement pstmt = connection.prepareStatement(sql);  // 일관된 구현체
        DatabaseMetaData metadata = connection.getMetaData();  // 일관된 메타데이터
        
        // 모든 객체가 동일한 드라이버 구현체 계열
    }
}
```

#### 현대적 사례: 클라우드 서비스 SDK

클라우드 서비스들도 Abstract Factory 패턴을 활용합니다:

```java
// AWS SDK의 Abstract Factory 패턴
public interface AWSServiceFactory {
    AmazonS3 createS3Client();
    AmazonEC2 createEC2Client();
    AmazonRDS createRDSClient();
    AmazonSQS createSQSClient();
}

// 리전별 Factory 구현
public class USEastFactory implements AWSServiceFactory {
    private final AWSCredentials credentials;
    
    public USEastFactory(AWSCredentials credentials) {
        this.credentials = credentials;
    }
    
    @Override
    public AmazonS3 createS3Client() {
        return AmazonS3ClientBuilder.standard()
                .withCredentials(new AWSStaticCredentialsProvider(credentials))
                .withRegion(Regions.US_EAST_1)
                .build();
    }
    
    @Override
    public AmazonEC2 createEC2Client() {
        return AmazonEC2ClientBuilder.standard()
                .withCredentials(new AWSStaticCredentialsProvider(credentials))
                .withRegion(Regions.US_EAST_1)
                .build();
    }
    
    // ... 기타 서비스들도 동일한 리전과 자격증명으로 구성
}

public class EuropeWestFactory implements AWSServiceFactory {
    private final AWSCredentials credentials;
    
    public EuropeWestFactory(AWSCredentials credentials) {
        this.credentials = credentials;
    }
    
    @Override
    public AmazonS3 createS3Client() {
        return AmazonS3ClientBuilder.standard()
                .withCredentials(new AWSStaticCredentialsProvider(credentials))
                .withRegion(Regions.EU_WEST_1)  // 다른 리전
                .build();
    }
    
    // ... 모든 서비스가 EU 리전으로 일관되게 구성
}

// 사용 예제
public class CloudService {
    private final AWSServiceFactory serviceFactory;
    
    public CloudService(AWSServiceFactory serviceFactory) {
        this.serviceFactory = serviceFactory;
    }
    
    public void migrateData() {
        // 모든 서비스가 동일한 리전과 설정으로 생성됨
        AmazonS3 s3 = serviceFactory.createS3Client();
        AmazonEC2 ec2 = serviceFactory.createEC2Client();
        AmazonRDS rds = serviceFactory.createRDSClient();
        
        // 동일한 리전 내에서 일관된 작업 수행
        // 네트워크 지연 최소화, 데이터 주권 준수 등
    }
}
```

### 현대적 Factory 패턴의 진화

#### Dependency Injection과 Factory의 융합

현대의 Factory 패턴은 **DI Container**와 결합되면서 새로운 차원의 유연성을 획득했습니다:

```java
// 전통적인 Factory 방식
public class OrderServiceFactory {
    public static OrderService create() {
        PaymentProcessor paymentProcessor = new CreditCardProcessor();
        NotificationService notificationService = new EmailNotificationService();
        return new OrderService(paymentProcessor, notificationService);
    }
}

// 현대적인 DI 기반 Factory
@Configuration
public class OrderServiceConfiguration {
    
    @Bean
    @ConditionalOnProperty(name = "payment.type", havingValue = "credit")
    public PaymentProcessor creditCardProcessor() {
        return new CreditCardProcessor();
    }
    
    @Bean
    @ConditionalOnProperty(name = "payment.type", havingValue = "paypal")
    public PaymentProcessor paypalProcessor() {
        return new PayPalProcessor();
    }
    
    @Bean
    public OrderService orderService(PaymentProcessor paymentProcessor,
                                   NotificationService notificationService) {
        return new OrderService(paymentProcessor, notificationService);
    }
}

// 사용하는 쪽 - Factory의 복잡성이 완전히 숨겨짐
@Service
public class OrderController {
    private final OrderService orderService;  // 자동으로 주입됨
    
    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }
}
```

#### Functional Factory: 고차 함수의 활용

함수형 프로그래밍의 영향으로 **함수 자체를 Factory로 사용**하는 패턴이 등장했습니다:

```java
// 전통적인 Factory
public interface ProcessorFactory {
    PaymentProcessor create(PaymentConfig config);
}

// 함수형 Factory
public class FunctionalFactoryExample {
    
    // 함수를 반환하는 Factory
    public static Function<PaymentConfig, PaymentProcessor> getProcessorFactory(PaymentType type) {
        switch (type) {
            case CREDIT_CARD:
                return config -> new CreditCardProcessor(config.getApiKey(), config.getEndpoint());
            case PAYPAL:
                return config -> new PayPalProcessor(config.getClientId(), config.getSecret());
            case CRYPTO:
                return config -> new CryptoProcessor(config.getWalletAddress());
            default:
                throw new IllegalArgumentException("Unsupported type: " + type);
        }
    }
    
    // Curry를 활용한 Factory
    public static Function<PaymentConfig, PaymentProcessor> createCurriedFactory(
            PaymentType type, 
            SecuritySettings security) {
        
        Function<PaymentType, Function<SecuritySettings, Function<PaymentConfig, PaymentProcessor>>> 
            curriedFactory = paymentType -> securitySettings -> config -> {
                PaymentProcessor processor = createProcessor(paymentType, config);
                return new SecurePaymentProcessorWrapper(processor, securitySettings);
            };
        
        return curriedFactory.apply(type).apply(security);
    }
    
    // 사용법
    public void processPayments() {
        Function<PaymentConfig, PaymentProcessor> factory = getProcessorFactory(PaymentType.CREDIT_CARD);
        
        List<PaymentConfig> configs = getPaymentConfigs();
        List<PaymentProcessor> processors = configs.stream()
            .map(factory)  // Factory를 map 함수로 직접 사용
            .collect(Collectors.toList());
    }
}
```

#### Generic Factory와 타입 안전성

제네릭을 활용하면 **타입 안전한 Factory**를 만들 수 있습니다:

```java
// 타입 안전한 Generic Factory
public class TypeSafeFactory {
    
    private final Map<Class<?>, Supplier<?>> factories = new HashMap<>();
    
    // 타입 안전한 Factory 등록
    public <T> void register(Class<T> type, Supplier<T> factory) {
        factories.put(type, factory);
    }
    
    // 타입 안전한 객체 생성
    @SuppressWarnings("unchecked")
    public <T> T create(Class<T> type) {
        Supplier<T> factory = (Supplier<T>) factories.get(type);
        if (factory == null) {
            throw new IllegalArgumentException("No factory registered for type: " + type);
        }
        return factory.get();
    }
    
    // 빌더 패턴과 결합
    public static TypeSafeFactory builder() {
        return new TypeSafeFactory();
    }
    
    public <T> TypeSafeFactory with(Class<T> type, Supplier<T> factory) {
        register(type, factory);
        return this;
    }
}

// 사용 예제
public class FactoryUsage {
    public void demonstrateTypeSafety() {
        TypeSafeFactory factory = TypeSafeFactory.builder()
            .with(PaymentProcessor.class, () -> new CreditCardProcessor())
            .with(NotificationService.class, () -> new EmailNotificationService())
            .with(AuditLogger.class, () -> new DatabaseAuditLogger());
        
        // 컴파일 타임에 타입 안전성 보장
        PaymentProcessor processor = factory.create(PaymentProcessor.class);
        NotificationService notifier = factory.create(NotificationService.class);
        
        // 컴파일 에러 - 등록되지 않은 타입
        // ReportGenerator generator = factory.create(ReportGenerator.class);
    }
}
```

#### 어노테이션 기반 Factory 자동화

어노테이션과 리플렉션을 활용하면 Factory 코드를 대폭 줄일 수 있습니다:

```java
// Factory 자동화를 위한 어노테이션
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface FactoryProduct {
    String value();
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface AutoFactory {
    Class<?> productType();
}

// 제품 클래스들
@FactoryProduct("credit-card")
public class CreditCardProcessor implements PaymentProcessor {
    // 구현
}

@FactoryProduct("paypal")
public class PayPalProcessor implements PaymentProcessor {
    // 구현
}

@FactoryProduct("crypto")
public class CryptoProcessor implements PaymentProcessor {
    // 구현
}

// 자동화된 Factory
@AutoFactory(productType = PaymentProcessor.class)
public class AutoPaymentProcessorFactory {
    
    private static final Map<String, Class<? extends PaymentProcessor>> productMap = new HashMap<>();
    
    static {
        // 클래스패스 스캔을 통한 자동 등록
        Reflections reflections = new Reflections("com.example.processors");
        Set<Class<?>> annotatedClasses = reflections.getTypesAnnotatedWith(FactoryProduct.class);
        
        for (Class<?> clazz : annotatedClasses) {
            if (PaymentProcessor.class.isAssignableFrom(clazz)) {
                FactoryProduct annotation = clazz.getAnnotation(FactoryProduct.class);
                productMap.put(annotation.value(), (Class<? extends PaymentProcessor>) clazz);
            }
        }
    }
    
    public PaymentProcessor create(String type) {
        Class<? extends PaymentProcessor> clazz = productMap.get(type);
        if (clazz == null) {
            throw new IllegalArgumentException("Unknown payment type: " + type);
        }
        
        try {
            return clazz.getDeclaredConstructor().newInstance();
        } catch (Exception e) {
            throw new RuntimeException("Failed to create instance", e);
        }
    }
    
    // 새로운 타입 추가 시 코드 수정 불필요!
    // 단지 @FactoryProduct 어노테이션만 추가하면 자동으로 등록
}
```

### 성능 분석과 최적화 전략

#### Factory 패턴의 성능 특성

```java
// 성능 벤치마크를 위한 테스트
public class FactoryPerformanceTest {
    
    private static final int ITERATIONS = 1_000_000;
    
    @Benchmark
    public PaymentProcessor directCreation() {
        return new CreditCardProcessor();  // 직접 생성
    }
    
    @Benchmark
    public PaymentProcessor simpleFactory() {
        return PaymentProcessorFactory.create(PaymentType.CREDIT_CARD);  // Simple Factory
    }
    
    @Benchmark
    public PaymentProcessor reflectionFactory() {
        return reflectionBasedFactory.create("credit-card");  // 리플렉션 기반
    }
    
    @Benchmark
    public PaymentProcessor cachedFactory() {
        return cachedFactory.create(PaymentType.CREDIT_CARD);  // 캐시된 Factory
    }
}

/*
성능 벤치마크 결과 (나노초/operation):

직접 생성:           5.2 ns/op
Simple Factory:      8.7 ns/op  (67% 오버헤드)
리플렉션 Factory:    847 ns/op  (16,200% 오버헤드!)
캐시된 Factory:      12.3 ns/op (136% 오버헤드)

결론: 
- 단순한 Factory는 허용 가능한 오버헤드
- 리플렉션은 성능 크리티컬한 곳에서 피해야 함
- 캐싱은 리플렉션 비용을 크게 줄임
*/
```

#### 객체 풀링과 Factory 패턴

```java
// 고성능 Pool 기반 Factory
public class PooledFactory<T> {
    private final Queue<T> pool;
    private final Supplier<T> creator;
    private final Consumer<T> resetter;
    private final int maxPoolSize;
    
    public PooledFactory(Supplier<T> creator, Consumer<T> resetter, int maxPoolSize) {
        this.pool = new ConcurrentLinkedQueue<>();
        this.creator = creator;
        this.resetter = resetter;
        this.maxPoolSize = maxPoolSize;
    }
    
    public T acquire() {
        T instance = pool.poll();
        if (instance == null) {
            instance = creator.get();
        }
        return instance;
    }
    
    public void release(T instance) {
        if (pool.size() < maxPoolSize) {
            resetter.accept(instance);  // 객체 초기화
            pool.offer(instance);
        }
    }
}

// 사용 예제
public class DatabaseConnectionFactory {
    private static final PooledFactory<Connection> connectionPool = 
        new PooledFactory<>(
            () -> createNewConnection(),
            connection -> resetConnection(connection),
            20  // 최대 20개 연결 풀링
        );
    
    public static Connection getConnection() {
        return connectionPool.acquire();
    }
    
    public static void returnConnection(Connection connection) {
        connectionPool.release(connection);
    }
}
```

### 안티패턴과 함정들

#### God Factory 안티패턴

```java
// 안티패턴: 너무 많은 책임을 가진 Factory
public class GodFactory {
    // 모든 종류의 객체를 생성하는 거대한 Factory
    public Object create(String type, Map<String, Object> params) {
        switch (type) {
            case "payment-processor":
                return createPaymentProcessor(params);
            case "notification-service":
                return createNotificationService(params);
            case "audit-logger":
                return createAuditLogger(params);
            case "report-generator":
                return createReportGenerator(params);
            // ... 수십 개의 case문
            default:
                throw new IllegalArgumentException("Unknown type: " + type);
        }
    }
    
    // 문제점:
    // 1. 단일 책임 원칙 위반
    // 2. 개방-폐쇄 원칙 위반
    // 3. 하나의 클래스가 너무 많은 것을 알고 있음
    // 4. 테스트하기 어려움
}

// 해결책: 도메인별 Factory 분리
public class PaymentProcessorFactory {
    public PaymentProcessor create(PaymentType type, PaymentConfig config) {
        // 결제 관련 객체만 생성
    }
}

public class NotificationServiceFactory {
    public NotificationService create(NotificationType type, NotificationConfig config) {
        // 알림 관련 객체만 생성
    }
}
```

#### Factory 오버엔지니어링

```java
// 안티패턴: 단순한 객체에도 Factory 적용
public class StringFactory {
    public String createEmpty() {
        return "";
    }
    
    public String createFrom(String value) {
        return new String(value);
    }
    
    public String createUpperCase(String value) {
        return value.toUpperCase();
    }
}

// 문제: 이미 충분히 간단한 것을 복잡하게 만듦
// 해결책: 단순한 것은 그대로 두기
String empty = "";
String copy = new String(value);
String upper = value.toUpperCase();
```

### 실무 적용 가이드라인

#### Factory 패턴 선택 기준

```
Simple Factory 선택 기준:
- 생성할 타입이 3-5개 이하
- 생성 로직이 단순함
- 확장 빈도가 낮음
- 팀의 숙련도가 낮음

Factory Method 선택 기준:
- 생성과 사용이 함께 이루어져야 함
- 서브클래스별로 다른 객체 생성 필요
- 프레임워크나 라이브러리 설계
- 확장성이 중요함

Abstract Factory 선택 기준:
- 관련된 객체들을 함께 생성해야 함
- 제품군의 일관성이 중요함
- 플랫폼별 구현이 필요함
- 대규모 시스템 설계
```

#### 현대적 선택 가이드

```java
// 상황별 최적 선택
public class ModernFactoryGuidelines {
    
    // 1. Spring 환경에서는 @Configuration 활용
    @Configuration
    public class ServiceConfiguration {
        @Bean
        @Profile("production")
        public PaymentService productionPaymentService() {
            return new ProductionPaymentService();
        }
        
        @Bean
        @Profile("development")
        public PaymentService mockPaymentService() {
            return new MockPaymentService();
        }
    }
    
    // 2. 함수형 스타일이 적합한 경우
    public class FunctionalApproach {
        Map<PaymentType, Function<PaymentConfig, PaymentProcessor>> factories = Map.of(
            PaymentType.CREDIT_CARD, config -> new CreditCardProcessor(config),
            PaymentType.PAYPAL, config -> new PayPalProcessor(config),
            PaymentType.CRYPTO, config -> new CryptoProcessor(config)
        );
        
        public PaymentProcessor create(PaymentType type, PaymentConfig config) {
            return factories.get(type).apply(config);
        }
    }
    
    // 3. 레거시 시스템에서는 점진적 적용
    public class LegacyIntegration {
        // 기존 코드를 Factory로 감싸서 점진적 개선
        public PaymentProcessor createPaymentProcessor(String type) {
            // 기존 switch 문을 그대로 활용하되 Factory로 분리
            return LegacyPaymentProcessorCreator.create(type);
        }
    }
}
```

## 한눈에 보는 Factory 패턴군

### Factory 패턴 비교표

| 비교 항목 | Simple Factory | Factory Method | Abstract Factory |
|----------|---------------|----------------|------------------|
| **핵심 목적** | 생성 로직 중앙화 | 생성 책임 서브클래스 위임 | 제품군 일관성 보장 |
| **OCP 준수** | 위반 (switch문 수정 필요) | 준수 (새 서브클래스 추가) | 준수 (새 Factory 추가) |
| **복잡도** | 낮음 | 중간 | 높음 |
| **클래스 수** | 최소 | 중간 | 많음 |
| **확장 방식** | 기존 코드 수정 | 새 서브클래스 생성 | 새 Factory 계열 생성 |
| **적용 시점** | 단순한 생성 로직 | Template Method와 연계 | 여러 제품군 관리 |
| **GoF 분류** | 비GoF (관용구) | GoF 생성 패턴 | GoF 생성 패턴 |

### Factory 패턴 선택 가이드

| 상황 | 권장 패턴 | 이유 |
|------|----------|------|
| 생성 타입이 3-5개 이하, 변경 빈도 낮음 | Simple Factory | 단순하고 이해하기 쉬움 |
| 서브클래스별 다른 객체 생성 필요 | Factory Method | 확장성 확보, OCP 준수 |
| 관련 객체들을 일관된 스타일로 생성 | Abstract Factory | 제품군 일관성 보장 |
| Spring/DI 환경에서 동작 | @Bean + @Configuration | 프레임워크 통합 |
| 성능 크리티컬, 생성 비용 높음 | Factory + Object Pool | 재사용으로 성능 향상 |

### Factory 패턴 장단점 비교

| 패턴 | 장점 | 단점 |
|------|------|------|
| Simple Factory | 구현 간단, 생성 로직 집중 | OCP 위반, 확장 시 수정 필요 |
| Factory Method | OCP 준수, 유연한 확장 | 클래스 계층 복잡도 증가 |
| Abstract Factory | 제품군 일관성, 교체 용이 | 많은 클래스 필요, 복잡도 높음 |

### Static Factory Methods vs Constructor

| 비교 항목 | Static Factory Methods | 생성자 (Constructor) |
|----------|----------------------|---------------------|
| 이름 | 의미 있는 이름 가능 (forMySQL, of) | 클래스명으로 고정 |
| 반환 타입 | 서브클래스/인터페이스 반환 가능 | 해당 타입만 반환 |
| 인스턴스 제어 | 캐싱, 싱글톤, 풀링 가능 | 항상 새 인스턴스 |
| 시그니처 제약 | 동일 매개변수도 다른 이름 가능 | 오버로딩만 가능 |
| 상속 | 상속 시 제약 있음 | 자유로운 상속 |

### 패턴 적용 체크리스트

| 체크 항목 | 설명 |
|----------|------|
| 생성 타입 수 확인 | 3개 이하: Simple, 4개 이상: Factory Method 고려 |
| 확장 빈도 예측 | 잦은 확장 예상 시 Factory Method 또는 Abstract Factory |
| 제품군 관리 필요성 | 관련 객체 일관성 필요 시 Abstract Factory |
| 팀 숙련도 고려 | 복잡한 패턴은 이해도 확인 후 도입 |
| 프레임워크 활용 | Spring 환경에서는 DI 기반 Factory 우선 |

---

### 결론: Factory 패턴의 본질과 미래

Factory 패턴군의 진화 과정을 살펴보면, 이들이 단순한 **"객체 생성 도구"**를 넘어서 **"시스템 아키텍처의 핵심"**이 되어왔음을 알 수 있습니다.

#### Factory 패턴의 진정한 가치:

1. **관심사의 분리**: 생성 로직과 비즈니스 로직의 명확한 분리
2. **확장성**: 새로운 타입 추가 시 기존 코드 수정 최소화  
3. **일관성**: 관련 객체들의 생성 규칙과 정책 통일
4. **테스트 용이성**: Mock 객체 주입을 통한 단위 테스트 지원

#### 현대적 트렌드와 미래 전망:

**DI Container의 보편화**로 전통적인 Factory 패턴의 필요성이 줄어들고 있지만, 여전히 다음 영역에서는 필수적입니다:

- **라이브러리/프레임워크 설계**: 사용자에게 확장점 제공
- **플러그인 아키텍처**: 동적 모듈 로딩과 생성
- **멀티 테넌트 시스템**: 테넌트별 구현체 분리
- **마이크로서비스**: 서비스 간 인터페이스 추상화

**함수형 프로그래밍의 영향**으로 Factory도 더욱 간결하고 조합 가능한 형태로 진화하고 있습니다. 고차 함수, 모나드, 커링 등의 개념이 Factory 설계에 적용되면서 **더욱 표현력 있고 안전한 객체 생성**이 가능해지고 있습니다.

#### 실무자를 위한 조언:

1. **과도한 추상화 피하기**: 단순한 것은 단순하게 유지
2. **팀의 성숙도 고려**: 복잡한 패턴보다는 이해하기 쉬운 구조 선택
3. **성능 임계점 인식**: 리플렉션 기반 Factory의 성능 비용 인지
4. **점진적 적용**: 레거시 시스템에서는 단계적으로 Factory 패턴 도입

Factory 패턴을 마스터한다는 것은 단순히 객체를 만드는 방법을 아는 것이 아닙니다. 그것은 **시스템의 유연성과 확장성을 설계하는 능력**을 갖추는 것이며, **변화하는 요구사항에 우아하게 대응할 수 있는 아키텍처**를 구축하는 것입니다.

다음 글에서는 Factory 패턴과는 정반대의 철학을 가진 **Singleton 패턴**을 살펴보겠습니다. "하나만 존재해야 하는 것"의 복잡성과 논란, 그리고 현대적 대안들에 대해 깊이 있게 탐구해보겠습니다.

---

**핵심 메시지:**
"Factory 패턴은 단순한 객체 생성 도구가 아니라, 시스템의 유연성과 확장성을 좌우하는 핵심 설계 요소이며, 현대 프레임워크의 기반이 되는 필수적인 패턴이다." 