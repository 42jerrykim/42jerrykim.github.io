---
draft: true
collection_order: 170
title: "[Design Patterns] 패턴의 조합과 상호작용: 설계의 협주곡"
description: "여러 디자인 패턴들이 어떻게 조화롭게 결합되어 강력한 시스템을 구축하는지 탐구합니다. 패턴 간 시너지 효과, 복합 패턴 시나리오, 패턴 충돌 해결책 등을 통해 실제 프로젝트에서 패턴들을 효과적으로 조합하는 전문가 수준의 아키텍처 설계 능력을 기릅니다."
image: "wordcloud.png"
date: 2024-12-17T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Pattern Integration
- System Architecture
- Advanced Design
tags:
- Design-Pattern
- GoF
- Software-Architecture
- Best-Practices
- SOLID
- 디자인패턴
- 소프트웨어아키텍처
---

여러 패턴의 조합과 상호작용을 통해 시너지 효과를 내는 방법을 탐구합니다. 실제 시스템에서 패턴들이 어떻게 협력하는지 학습합니다.

## 서론: 패턴들의 아름다운 협주곡

> *"단일 패턴은 솔로 연주와 같다. 진정한 아름다움은 여러 패턴이 조화롭게 어우러질 때 드러난다."*

현실의 소프트웨어 시스템에서 **단일 패턴만으로 모든 문제를 해결하는 경우는 거의 없습니다**. 복잡한 비즈니스 요구사항과 기술적 제약사항을 만족시키기 위해서는 **여러 패턴의 조합**이 필요합니다.

하지만 패턴 조합은 **양날의 검**입니다. 올바르게 조합하면 각 패턴의 장점이 시너지를 내어 **1+1=3**의 효과를 얻을 수 있습니다. 반대로 잘못 조합하면 복잡성만 증가하고 **안티패턴**이 될 수 있습니다.

이 글에서는 **패턴 조합의 예술**을 탐구합니다:
- **자연스러운 패턴 조합** - 서로 보완하는 패턴들
- **복합 패턴 시나리오** - 실제 시스템에서의 활용
- **아키텍처 패턴과의 연계** - 더 큰 그림에서의 역할
- **패턴 충돌과 해결책** - 조합 시 주의사항

## 자연스러운 패턴 조합들

### Factory + Singleton - 객체 생성의 완벽한 조합

**Factory 패턴**과 **Singleton 패턴**은 객체 생성 영역에서 완벽한 조합을 이룹니다:

```java
// Factory + Singleton 조합의 우아함
public class DatabaseConnectionFactory {
    private static volatile DatabaseConnectionFactory instance;
    private final Map<String, DataSource> dataSources;
    private final ConnectionPoolManager poolManager;
    
    private DatabaseConnectionFactory() {
        this.dataSources = new ConcurrentHashMap<>();
        this.poolManager = new ConnectionPoolManager();
        initializeDataSources();
    }
    
    // Singleton 보장
    public static DatabaseConnectionFactory getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnectionFactory.class) {
                if (instance == null) {
                    instance = new DatabaseConnectionFactory();
                }
            }
        }
        return instance;
    }
    
    // Factory Method 패턴
    public Connection createConnection(DatabaseType type) {
        DataSource dataSource = dataSources.get(type.getName());
        if (dataSource == null) {
            throw new IllegalArgumentException("Unsupported database type: " + type);
        }
        
        try {
            Connection connection = dataSource.getConnection();
            return new MonitoredConnection(connection, poolManager);
        } catch (SQLException e) {
            throw new RuntimeException("Failed to create connection", e);
        }
    }
    
    // Abstract Factory 패턴 (타입별 특화 팩토리)
    public DatabaseOperations createOperations(DatabaseType type) {
        switch (type) {
            case MYSQL:
                return new MySQLOperations(createConnection(type));
            case POSTGRESQL:
                return new PostgreSQLOperations(createConnection(type));
            case ORACLE:
                return new OracleOperations(createConnection(type));
            default:
                throw new IllegalArgumentException("Unsupported database type: " + type);
        }
    }
    
    private void initializeDataSources() {
        // 데이터소스 초기화 로직
        dataSources.put("mysql", createMySQLDataSource());
        dataSources.put("postgresql", createPostgreSQLDataSource());
        dataSources.put("oracle", createOracleDataSource());
    }
}

// 사용 예시
public class DatabaseService {
    private final DatabaseConnectionFactory factory;
    
    public DatabaseService() {
        // Singleton 팩토리 사용
        this.factory = DatabaseConnectionFactory.getInstance();
    }
    
    public void performDatabaseOperation(DatabaseType type) {
        // Factory로 적절한 연결과 연산 객체 생성
        DatabaseOperations ops = factory.createOperations(type);
        ops.executeQuery("SELECT * FROM users");
    }
}
```

### Observer + Command - 이벤트와 액션의 완벽한 분리

**Observer 패턴**으로 이벤트를 감지하고 **Command 패턴**으로 액션을 실행하는 조합:

```java
// Observer + Command 조합
public class EventDrivenOrderSystem {
    private final List<OrderEventObserver> observers;
    private final CommandQueue commandQueue;
    private final CommandProcessor processor;
    
    public EventDrivenOrderSystem() {
        this.observers = new CopyOnWriteArrayList<>();
        this.commandQueue = new LinkedBlockingQueue<>();
        this.processor = new CommandProcessor(commandQueue);
        setupObservers();
    }
    
    private void setupObservers() {
        // 각 Observer가 특정 Command를 생성하도록 설계
        addObserver(new InventoryObserver());
        addObserver(new PaymentObserver());
        addObserver(new NotificationObserver());
        addObserver(new AuditObserver());
    }
    
    public void addObserver(OrderEventObserver observer) {
        observers.add(observer);
    }
    
    public void processOrder(Order order) {
        // 주문 처리 이벤트 발생
        OrderEvent event = new OrderEvent(OrderEventType.ORDER_PLACED, order);
        notifyObservers(event);
    }
    
    private void notifyObservers(OrderEvent event) {
        for (OrderEventObserver observer : observers) {
            try {
                // Observer가 Command 생성
                List<Command> commands = observer.handleEvent(event);
                
                // 생성된 Command들을 큐에 추가
                for (Command command : commands) {
                    commandQueue.offer(command);
                }
            } catch (Exception e) {
                System.err.println("Observer failed: " + e.getMessage());
            }
        }
    }
}

// Observer 구현체
class InventoryObserver implements OrderEventObserver {
    private final InventoryService inventoryService;
    
    public InventoryObserver() {
        this.inventoryService = new InventoryService();
    }
    
    @Override
    public List<Command> handleEvent(OrderEvent event) {
        List<Command> commands = new ArrayList<>();
        
        if (event.getType() == OrderEventType.ORDER_PLACED) {
            Order order = event.getOrder();
            
            // 재고 차감 Command 생성
            for (OrderItem item : order.getItems()) {
                commands.add(new DeductInventoryCommand(
                    inventoryService, 
                    item.getProductId(), 
                    item.getQuantity()
                ));
            }
            
            // 재고 부족 시 알림 Command 생성
            commands.add(new CheckLowStockCommand(inventoryService, order));
        }
        
        return commands;
    }
}

// Command 구현체
class DeductInventoryCommand implements Command {
    private final InventoryService inventoryService;
    private final String productId;
    private final int quantity;
    private int deductedQuantity = 0;
    
    public DeductInventoryCommand(InventoryService service, String productId, int quantity) {
        this.inventoryService = service;
        this.productId = productId;
        this.quantity = quantity;
    }
    
    @Override
    public void execute() {
        deductedQuantity = inventoryService.deductStock(productId, quantity);
        System.out.println("Deducted " + deductedQuantity + " units of " + productId);
    }
    
    @Override
    public void undo() {
        if (deductedQuantity > 0) {
            inventoryService.addStock(productId, deductedQuantity);
            System.out.println("Restored " + deductedQuantity + " units of " + productId);
        }
    }
}
```

### Decorator + Strategy - 기능 확장과 알고리즘 선택의 조합

**Decorator 패턴**으로 기능을 확장하고 **Strategy 패턴**으로 알고리즘을 선택:

```java
// Decorator + Strategy 조합
// 기본 서비스 인터페이스
interface PaymentService {
    PaymentResult processPayment(PaymentRequest request);
}

// 기본 구현
class BasicPaymentService implements PaymentService {
    private PaymentStrategy strategy;
    
    public BasicPaymentService(PaymentStrategy strategy) {
        this.strategy = strategy;
    }
    
    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        return strategy.process(request);
    }
    
    public void setStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }
}

// Decorator 기본 클래스
abstract class PaymentServiceDecorator implements PaymentService {
    protected final PaymentService decoratedService;
    
    public PaymentServiceDecorator(PaymentService service) {
        this.decoratedService = service;
    }
    
    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        return decoratedService.processPayment(request);
    }
}

// 로깅 Decorator
class LoggingPaymentDecorator extends PaymentServiceDecorator {
    private final Logger logger;
    
    public LoggingPaymentDecorator(PaymentService service) {
        super(service);
        this.logger = LoggerFactory.getLogger(LoggingPaymentDecorator.class);
    }
    
    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        logger.info("Processing payment: {} for amount: {}", 
                   request.getPaymentMethod(), request.getAmount());
        
        long startTime = System.currentTimeMillis();
        PaymentResult result = super.processPayment(request);
        long endTime = System.currentTimeMillis();
        
        logger.info("Payment processed in {}ms. Result: {}", 
                   endTime - startTime, result.isSuccess() ? "SUCCESS" : "FAILED");
        
        return result;
    }
}

// 캐싱 Decorator
class CachingPaymentDecorator extends PaymentServiceDecorator {
    private final Map<String, PaymentResult> cache;
    private final Duration cacheTimeout;
    
    public CachingPaymentDecorator(PaymentService service, Duration cacheTimeout) {
        super(service);
        this.cache = new ConcurrentHashMap<>();
        this.cacheTimeout = cacheTimeout;
    }
    
    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        String cacheKey = generateCacheKey(request);
        
        // 캐시 확인 (중복 결제 방지)
        PaymentResult cachedResult = cache.get(cacheKey);
        if (cachedResult != null && !isCacheExpired(cachedResult)) {
            return PaymentResult.duplicate(cachedResult);
        }
        
        PaymentResult result = super.processPayment(request);
        
        // 성공한 결제만 캐시
        if (result.isSuccess()) {
            cache.put(cacheKey, result);
        }
        
        return result;
    }
    
    private String generateCacheKey(PaymentRequest request) {
        return request.getCustomerId() + "_" + 
               request.getAmount() + "_" + 
               request.getCurrency() + "_" + 
               request.getTimestamp().truncatedTo(ChronoUnit.MINUTES);
    }
}

// 재시도 Decorator
class RetryPaymentDecorator extends PaymentServiceDecorator {
    private final int maxRetries;
    private final Duration retryDelay;
    
    public RetryPaymentDecorator(PaymentService service, int maxRetries, Duration retryDelay) {
        super(service);
        this.maxRetries = maxRetries;
        this.retryDelay = retryDelay;
    }
    
    @Override
    public PaymentResult processPayment(PaymentRequest request) {
        for (int attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                PaymentResult result = super.processPayment(request);
                
                if (result.isSuccess() || !result.isRetryable()) {
                    return result;
                }
                
                if (attempt < maxRetries) {
                    System.out.println("Payment attempt " + attempt + " failed. Retrying in " + 
                                     retryDelay.toMillis() + "ms");
                    Thread.sleep(retryDelay.toMillis());
                }
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return PaymentResult.failed("Payment interrupted");
            } catch (Exception e) {
                if (attempt == maxRetries) {
                    return PaymentResult.failed("Payment failed after " + maxRetries + " attempts");
                }
            }
        }
        
        return PaymentResult.failed("Payment failed after " + maxRetries + " attempts");
    }
}

// 사용 예시 - 패턴들의 아름다운 조합
public class PaymentSystemDemo {
    public static void main(String[] args) {
        // Strategy 패턴으로 결제 방식 선택
        PaymentStrategy creditCardStrategy = new CreditCardStrategy();
        PaymentService basicService = new BasicPaymentService(creditCardStrategy);
        
        // Decorator 패턴으로 기능 확장 (체인 형태로)
        PaymentService enhancedService = new LoggingPaymentDecorator(
            new CachingPaymentDecorator(
                new RetryPaymentDecorator(basicService, 3, Duration.ofSeconds(1)),
                Duration.ofMinutes(5)
            )
        );
        
        // 사용
        PaymentRequest request = new PaymentRequest("customer123", 100.0, "USD");
        PaymentResult result = enhancedService.processPayment(request);
        
        System.out.println("Payment result: " + result);
    }
}
```

## 복합 패턴 시나리오 - E-Commerce 시스템

실제 E-Commerce 시스템에서 여러 패턴이 어떻게 조합되는지 살펴보겠습니다:

```java
// 복합 패턴이 적용된 E-Commerce 시스템
public class ECommerceSystem {
    
    // 1. Factory + Singleton + Builder 조합
    public static class ServiceFactory {
        private static volatile ServiceFactory instance;
        private final Map<Class<?>, Object> services;
        
        private ServiceFactory() {
            this.services = new ConcurrentHashMap<>();
            initializeServices();
        }
        
        public static ServiceFactory getInstance() {
            if (instance == null) {
                synchronized (ServiceFactory.class) {
                    if (instance == null) {
                        instance = new ServiceFactory();
                    }
                }
            }
            return instance;
        }
        
        @SuppressWarnings("unchecked")
        public <T> T getService(Class<T> serviceClass) {
            return (T) services.get(serviceClass);
        }
        
        private void initializeServices() {
            // Builder 패턴으로 복잡한 서비스 구성
            UserService userService = new UserServiceBuilder()
                .withRepository(createUserRepository())
                .withValidator(createUserValidator())
                .withNotificationService(createNotificationService())
                .withAuditService(createAuditService())
                .build();
                
            OrderService orderService = new OrderServiceBuilder()
                .withRepository(createOrderRepository())
                .withInventoryService(createInventoryService())
                .withPaymentService(createPaymentService())
                .withShippingService(createShippingService())
                .build();
                
            services.put(UserService.class, userService);
            services.put(OrderService.class, orderService);
        }
    }
    
    // 2. Observer + Command + Strategy 조합
    public static class OrderProcessingSystem {
        private final List<OrderObserver> observers;
        private final CommandProcessor commandProcessor;
        private final OrderValidationStrategy validationStrategy;
        
        public OrderProcessingSystem() {
            this.observers = new ArrayList<>();
            this.commandProcessor = new CommandProcessor();
            this.validationStrategy = new CompositeValidationStrategy();
            setupObservers();
        }
        
        private void setupObservers() {
            observers.add(new InventoryUpdateObserver());
            observers.add(new PaymentProcessingObserver());
            observers.add(new EmailNotificationObserver());
            observers.add(new AuditLogObserver());
            observers.add(new AnalyticsObserver());
        }
        
        public OrderResult processOrder(Order order) {
            try {
                // Strategy 패턴으로 주문 검증
                ValidationResult validation = validationStrategy.validate(order);
                if (!validation.isValid()) {
                    return OrderResult.validationFailed(validation.getErrors());
                }
                
                // Observer 패턴으로 이벤트 발생
                OrderEvent event = new OrderEvent(ORDER_SUBMITTED, order);
                List<Command> commands = notifyObserversAndCollectCommands(event);
                
                // Command 패턴으로 비즈니스 로직 실행
                ExecutionResult executionResult = commandProcessor.executeAll(commands);
                
                if (executionResult.isSuccess()) {
                    notifyObservers(new OrderEvent(ORDER_COMPLETED, order));
                    return OrderResult.success(order);
                } else {
                    // 실패 시 보상 트랜잭션
                    commandProcessor.undoAll(executionResult.getExecutedCommands());
                    notifyObservers(new OrderEvent(ORDER_FAILED, order));
                    return OrderResult.failed(executionResult.getError());
                }
                
            } catch (Exception e) {
                return OrderResult.error("Order processing failed: " + e.getMessage());
            }
        }
        
        private List<Command> notifyObserversAndCollectCommands(OrderEvent event) {
            List<Command> allCommands = new ArrayList<>();
            
            for (OrderObserver observer : observers) {
                try {
                    List<Command> commands = observer.handleEvent(event);
                    allCommands.addAll(commands);
                } catch (Exception e) {
                    System.err.println("Observer failed: " + e.getMessage());
                }
            }
            
            return allCommands;
        }
    }
    
    // 3. State + Template Method + Visitor 조합
    public static abstract class OrderWorkflow {
        protected Order order;
        protected OrderState currentState;
        private final List<OrderStateListener> stateListeners;
        
        public OrderWorkflow(Order order) {
            this.order = order;
            this.currentState = new PendingState();
            this.stateListeners = new ArrayList<>();
        }
        
        // Template Method: 워크플로우 실행 골격
        public final WorkflowResult executeWorkflow() {
            try {
                onWorkflowStarted();
                
                while (!currentState.isTerminal()) {
                    OrderState previousState = currentState;
                    currentState = processCurrentState();
                    
                    if (currentState != previousState) {
                        onStateTransition(previousState, currentState);
                        notifyStateListeners(previousState, currentState);
                    }
                }
                
                WorkflowResult result = createFinalResult();
                onWorkflowCompleted(result);
                
                return result;
                
            } catch (Exception e) {
                return handleWorkflowError(e);
            }
        }
        
        // Visitor 패턴으로 상태별 작업 처리
        public void acceptVisitor(OrderStateVisitor visitor) {
            currentState.accept(visitor);
        }
        
        // Hook 메서드들
        protected void onWorkflowStarted() {
            System.out.println("Workflow started for order: " + order.getId());
        }
        
        protected void onStateTransition(OrderState from, OrderState to) {
            System.out.println("State transition: " + from.getName() + " -> " + to.getName());
        }
        
        protected void onWorkflowCompleted(WorkflowResult result) {
            System.out.println("Workflow completed: " + result.getStatus());
        }
        
        // Abstract 메서드들
        protected abstract OrderState processCurrentState();
        protected abstract WorkflowResult createFinalResult();
        protected abstract WorkflowResult handleWorkflowError(Exception e);
        
        public void addStateListener(OrderStateListener listener) {
            stateListeners.add(listener);
        }
        
        private void notifyStateListeners(OrderState from, OrderState to) {
            for (OrderStateListener listener : stateListeners) {
                listener.onStateChanged(order, from, to);
            }
        }
    }
    
    // 4. Decorator + Composite + Facade 조합
    public static class OrderValidationService {
        private final ValidationComponent rootValidator;
        
        public OrderValidationService() {
            this.rootValidator = buildValidationTree();
        }
        
        private ValidationComponent buildValidationTree() {
            // Composite 패턴으로 검증 트리 구성
            CompositeValidator rootValidator = new CompositeValidator("Root Validator");
            
            // 기본 검증
            CompositeValidator basicValidation = new CompositeValidator("Basic Validation");
            basicValidation.add(new OrderFormatValidator());
            basicValidation.add(new CustomerValidator());
            basicValidation.add(new ProductValidator());
            
            // 비즈니스 검증
            CompositeValidator businessValidation = new CompositeValidator("Business Validation");
            businessValidation.add(new InventoryValidator());
            businessValidation.add(new PricingValidator());
            businessValidation.add(new PromotionValidator());
            
            // 보안 검증
            CompositeValidator securityValidation = new CompositeValidator("Security Validation");
            securityValidation.add(new FraudDetectionValidator());
            securityValidation.add(new RateLimitValidator());
            
            rootValidator.add(basicValidation);
            rootValidator.add(businessValidation);
            rootValidator.add(securityValidation);
            
            // Decorator 패턴으로 기능 확장
            ValidationComponent decoratedValidator = new LoggingValidationDecorator(
                new PerformanceValidationDecorator(
                    new CachingValidationDecorator(rootValidator)
                )
            );
            
            return decoratedValidator;
        }
        
        // Facade 패턴으로 간단한 인터페이스 제공
        public ValidationResult validateOrder(Order order) {
            return rootValidator.validate(order);
        }
        
        public ValidationReport getDetailedValidationReport(Order order) {
            DetailedValidationVisitor visitor = new DetailedValidationVisitor();
            rootValidator.accept(visitor);
            return visitor.getReport();
        }
    }
}
```

## 아키텍처 패턴과의 연계

### MVC 아키텍처에서의 패턴 조합

```java
// MVC + 디자인 패턴 조합
// Model Layer - Repository + Factory + Observer
@Component
public class UserModel {
    private final UserRepository repository;
    private final UserFactory factory;
    private final List<ModelObserver> observers;
    
    public UserModel(UserRepository repository, UserFactory factory) {
        this.repository = repository;
        this.factory = factory;
        this.observers = new CopyOnWriteArrayList<>();
    }
    
    public User createUser(UserCreateRequest request) {
        // Factory로 User 생성
        User user = factory.createUser(request);
        
        // Repository로 저장
        User savedUser = repository.save(user);
        
        // Observer들에게 알림
        notifyObservers(new ModelEvent(ModelEventType.USER_CREATED, savedUser));
        
        return savedUser;
    }
    
    public void addObserver(ModelObserver observer) {
        observers.add(observer);
    }
    
    private void notifyObservers(ModelEvent event) {
        observers.forEach(observer -> observer.onModelChanged(event));
    }
}

// View Layer - Composite + Decorator + Template Method
public abstract class BaseView {
    protected final List<ViewComponent> components;
    private final List<ViewDecorator> decorators;
    
    public BaseView() {
        this.components = new ArrayList<>();
        this.decorators = new ArrayList<>();
    }
    
    // Template Method for rendering
    public final String render() {
        StringBuilder html = new StringBuilder();
        
        html.append(renderHeader());
        html.append(renderContent());
        html.append(renderFooter());
        
        // Apply decorators
        String result = html.toString();
        for (ViewDecorator decorator : decorators) {
            result = decorator.decorate(result);
        }
        
        return result;
    }
    
    protected abstract String renderHeader();
    protected abstract String renderContent();
    protected abstract String renderFooter();
    
    // Composite pattern for components
    public void addComponent(ViewComponent component) {
        components.add(component);
    }
    
    // Decorator pattern for view enhancement
    public void addDecorator(ViewDecorator decorator) {
        decorators.add(decorator);
    }
}

// Controller Layer - Command + Chain of Responsibility + Strategy
@RestController
public class UserController {
    private final RequestHandlerChain handlerChain;
    private final CommandProcessor commandProcessor;
    private final ResponseStrategy responseStrategy;
    
    public UserController() {
        this.handlerChain = buildHandlerChain();
        this.commandProcessor = new CommandProcessor();
        this.responseStrategy = new JSONResponseStrategy();
    }
    
    @PostMapping("/users")
    public ResponseEntity<?> createUser(@RequestBody UserCreateRequest request) {
        try {
            // Chain of Responsibility로 요청 전처리
            ProcessingContext context = new ProcessingContext(request);
            handlerChain.handle(context);
            
            if (context.hasErrors()) {
                return responseStrategy.createErrorResponse(context.getErrors());
            }
            
            // Command 패턴으로 비즈니스 로직 실행
            CreateUserCommand command = new CreateUserCommand(
                context.getValidatedRequest(),
                userService
            );
            
            CommandResult result = commandProcessor.execute(command);
            
            // Strategy 패턴으로 응답 생성
            return responseStrategy.createSuccessResponse(result.getData());
            
        } catch (Exception e) {
            return responseStrategy.createErrorResponse("Internal server error");
        }
    }
    
    private RequestHandlerChain buildHandlerChain() {
        AuthenticationHandler authHandler = new AuthenticationHandler();
        ValidationHandler validationHandler = new ValidationHandler();
        RateLimitHandler rateLimitHandler = new RateLimitHandler();
        AuditHandler auditHandler = new AuditHandler();
        
        authHandler.setNext(validationHandler);
        validationHandler.setNext(rateLimitHandler);
        rateLimitHandler.setNext(auditHandler);
        
        return new RequestHandlerChain(authHandler);
    }
}
```

### 마이크로서비스 아키텍처에서의 패턴 활용

```java
// 마이크로서비스 + 패턴 조합
// API Gateway - Proxy + Decorator + Chain of Responsibility
public class ApiGateway {
    private final ServiceDiscovery serviceDiscovery;
    private final LoadBalancer loadBalancer;
    private final RequestFilterChain filterChain;
    
    public ApiGateway() {
        this.serviceDiscovery = new ConsulServiceDiscovery();
        this.loadBalancer = new RoundRobinLoadBalancer();
        this.filterChain = buildFilterChain();
    }
    
    public CompletableFuture<Response> routeRequest(Request request) {
        // Chain of Responsibility로 필터 적용
        FilterContext context = new FilterContext(request);
        filterChain.filter(context);
        
        if (context.isBlocked()) {
            return CompletableFuture.completedFuture(
                Response.blocked(context.getBlockReason())
            );
        }
        
        // Service Discovery로 서비스 인스턴스 찾기
        String serviceName = extractServiceName(request.getPath());
        List<ServiceInstance> instances = serviceDiscovery.getInstances(serviceName);
        
        if (instances.isEmpty()) {
            return CompletableFuture.completedFuture(
                Response.serviceUnavailable("Service not available: " + serviceName)
            );
        }
        
        // Load Balancer로 인스턴스 선택
        ServiceInstance instance = loadBalancer.choose(instances);
        
        // Proxy 패턴으로 실제 서비스 호출
        ServiceProxy proxy = createServiceProxy(instance);
        return proxy.forwardRequest(context.getProcessedRequest());
    }
    
    private RequestFilterChain buildFilterChain() {
        AuthenticationFilter authFilter = new AuthenticationFilter();
        RateLimitFilter rateLimitFilter = new RateLimitFilter();
        LoggingFilter loggingFilter = new LoggingFilter();
        CompressionFilter compressionFilter = new CompressionFilter();
        
        return RequestFilterChain.builder()
            .addFilter(authFilter)
            .addFilter(rateLimitFilter)
            .addFilter(loggingFilter)
            .addFilter(compressionFilter)
            .build();
    }
    
    private ServiceProxy createServiceProxy(ServiceInstance instance) {
        // Decorator 패턴으로 프록시 기능 확장
        ServiceProxy baseProxy = new HttpServiceProxy(instance);
        
        return new CircuitBreakerProxy(
            new RetryProxy(
                new TimeoutProxy(baseProxy, Duration.ofSeconds(30)),
                3, Duration.ofMillis(500)
            ),
            new CircuitBreakerConfig()
        );
    }
}
```

## 패턴 충돌과 해결 방법

### 책임 중복 문제

여러 패턴을 조합할 때 **책임이 중복**되는 경우가 있습니다:

```java
// 문제: Singleton + Factory에서 책임 중복
public class BadUserServiceFactory {
    private static BadUserServiceFactory instance;
    private UserService userService; // Singleton 책임
    
    private BadUserServiceFactory() {
        this.userService = createUserService(); // Factory 책임
    }
    
    public static BadUserServiceFactory getInstance() {
        // Singleton 관리 책임
        if (instance == null) {
            synchronized (BadUserServiceFactory.class) {
                if (instance == null) {
                    instance = new BadUserServiceFactory();
                }
            }
        }
        return instance;
    }
    
    public UserService getUserService() {
        return userService; // 단순 반환? Factory 역할 모호
    }
    
    // 😱 문제점:
    // 1. Singleton 관리와 Factory 역할이 혼재
    // 2. 생성 로직과 인스턴스 관리가 분리되지 않음
    // 3. 테스트하기 어려움
}

// 해결: 책임 분리
public class ServiceRegistry {
    // Singleton 책임만 담당
    private static volatile ServiceRegistry instance;
    private final Map<Class<?>, Object> services;
    private final ServiceFactory serviceFactory; // Factory에게 생성 위임
    
    private ServiceRegistry() {
        this.services = new ConcurrentHashMap<>();
        this.serviceFactory = new ServiceFactory(); // Factory 책임 분리
    }
    
    public static ServiceRegistry getInstance() {
        if (instance == null) {
            synchronized (ServiceRegistry.class) {
                if (instance == null) {
                    instance = new ServiceRegistry();
                }
            }
        }
        return instance;
    }
    
    @SuppressWarnings("unchecked")
    public <T> T getService(Class<T> serviceClass) {
        return (T) services.computeIfAbsent(serviceClass, clazz -> {
            return serviceFactory.createService(clazz); // Factory에게 생성 위임
        });
    }
}

// 별도의 Factory 클래스
public class ServiceFactory {
    // Factory 책임만 담당
    public <T> T createService(Class<T> serviceClass) {
        if (serviceClass == UserService.class) {
            return serviceClass.cast(createUserService());
        } else if (serviceClass == OrderService.class) {
            return serviceClass.cast(createOrderService());
        }
        throw new IllegalArgumentException("Unknown service: " + serviceClass);
    }
    
    private UserService createUserService() {
        return new UserServiceBuilder()
            .withRepository(createUserRepository())
            .withValidator(createUserValidator())
            .build();
    }
    
    private OrderService createOrderService() {
        return new OrderServiceBuilder()
            .withRepository(createOrderRepository())
            .withPaymentService(createPaymentService())
            .build();
    }
}
```

### 복잡성 증가와 해결책

패턴 조합으로 인한 **과도한 복잡성**을 관리하는 방법:

```java
// Facade 패턴으로 복잡성 숨기기
public class ECommerceFacade {
    // 복잡한 서브시스템들을 내부에 숨김
    private final UserService userService;
    private final OrderService orderService;
    private final PaymentService paymentService;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;
    
    public ECommerceFacade() {
        // 복잡한 초기화 로직을 숨김
        ServiceRegistry registry = ServiceRegistry.getInstance();
        this.userService = registry.getService(UserService.class);
        this.orderService = registry.getService(OrderService.class);
        this.paymentService = createEnhancedPaymentService();
        this.inventoryService = registry.getService(InventoryService.class);
        this.notificationService = registry.getService(NotificationService.class);
    }
    
    // 복잡한 비즈니스 프로세스를 단순한 인터페이스로 제공
    public OrderResult placeOrder(PlaceOrderRequest request) {
        try {
            // 1. 사용자 검증
            User user = userService.getUser(request.getUserId());
            if (user == null) {
                return OrderResult.userNotFound();
            }
            
            // 2. 재고 확인
            boolean inventoryAvailable = inventoryService.checkAvailability(request.getItems());
            if (!inventoryAvailable) {
                return OrderResult.inventoryUnavailable();
            }
            
            // 3. 주문 생성
            Order order = orderService.createOrder(request);
            
            // 4. 결제 처리
            PaymentResult paymentResult = paymentService.processPayment(
                order.getPaymentInfo()
            );
            if (!paymentResult.isSuccess()) {
                orderService.cancelOrder(order.getId());
                return OrderResult.paymentFailed(paymentResult.getError());
            }
            
            // 5. 재고 차감
            inventoryService.deductInventory(request.getItems());
            
            // 6. 알림 발송
            notificationService.sendOrderConfirmation(user, order);
            
            return OrderResult.success(order);
            
        } catch (Exception e) {
            // 복잡한 에러 처리 로직도 숨김
            return handleOrderError(e, request);
        }
    }
    
    // 클라이언트는 복잡한 서브시스템을 알 필요 없음
    public UserProfile getUserProfile(String userId) {
        User user = userService.getUser(userId);
        List<Order> recentOrders = orderService.getRecentOrders(userId, 5);
        
        return UserProfile.builder()
            .user(user)
            .recentOrders(recentOrders)
            .build();
    }
    
    private PaymentService createEnhancedPaymentService() {
        // 내부적으로는 복잡한 패턴 조합 사용
        PaymentService basicService = new BasicPaymentService(new CreditCardStrategy());
        
        return new LoggingPaymentDecorator(
            new RetryPaymentDecorator(
                new SecurityPaymentDecorator(basicService),
                3, Duration.ofSeconds(1)
            )
        );
    }
    
    private OrderResult handleOrderError(Exception e, PlaceOrderRequest request) {
        // 복잡한 에러 처리 및 보상 트랜잭션 로직
        return OrderResult.error("Order processing failed: " + e.getMessage());
    }
}
```

## 한눈에 보는 패턴 조합

### 자주 사용되는 패턴 조합 매트릭스

| 기본 패턴 | 조합 패턴 | 시너지 효과 | 사용 예 |
|----------|----------|-----------|--------|
| Factory Method | Strategy | 전략 객체 생성 캡슐화 | 결제 처리 시스템 |
| Factory Method | Singleton | 유일 인스턴스 + 생성 추상화 | 로거, 커넥션 풀 |
| Abstract Factory | Singleton | 팩토리 자체를 싱글톤으로 | GUI 테마 팩토리 |
| Strategy | Template Method | 알고리즘 골격 + 세부 전략 | 데이터 처리 파이프라인 |
| Observer | Mediator | 중재자가 이벤트 조정 | GUI 컴포넌트 연동 |
| Composite | Iterator | 트리 구조 순회 | 파일 시스템 탐색 |
| Decorator | Strategy | 장식 방식 전략화 | 동적 기능 조합 |
| Command | Memento | 명령 Undo/Redo | 텍스트 에디터 |
| Proxy | Decorator | 접근 제어 + 기능 추가 | 캐싱 + 로깅 |

### 패턴 조합 레벨별 가이드

| 레벨 | 조합 방식 | 복잡도 | 권장 상황 |
|------|----------|--------|----------|
| 1단계 | 단일 패턴 | 낮음 | 명확한 단일 문제 |
| 2단계 | 2개 조합 | 중간 | 연관된 두 문제 |
| 3단계 | 3개 조합 | 높음 | 복합 요구사항 |
| 4단계+ | 아키텍처 수준 | 매우 높음 | 프레임워크 설계 |

### 패턴 시너지 점수표

| 조합 | 시너지 점수 | 설명 |
|------|-----------|------|
| Factory + Strategy | ★★★★★ | 완벽한 생성-행동 분리 |
| Observer + Mediator | ★★★★☆ | 효과적인 통신 패턴 |
| Composite + Visitor | ★★★★☆ | 구조 + 연산 분리 |
| Decorator + Factory | ★★★★☆ | 동적 기능 + 생성 추상화 |
| Command + Memento | ★★★★★ | Undo/Redo 완벽 지원 |
| State + Strategy | ★★★☆☆ | 주의 필요 (유사성 혼동) |

### 패턴 충돌/회피 조합

| 조합 | 문제점 | 대안 |
|------|-------|------|
| Singleton + Prototype | 복제 시 단일성 위반 | Factory Method |
| Strategy + State 혼용 | 의도 혼란 | 명확한 구분 사용 |
| Observer 중첩 | 순환 통지 위험 | Mediator로 조정 |
| Decorator 과다 | 체인 복잡성 | Composite 고려 |

### 프레임워크별 패턴 조합 활용

| 프레임워크 | 핵심 패턴 조합 | 효과 |
|-----------|--------------|------|
| Spring MVC | Front Controller + Strategy + Factory | 요청 처리 유연성 |
| Hibernate | Proxy + Unit of Work + Identity Map | 영속성 투명성 |
| React | Composite + Observer + State | UI 컴포넌트 모델 |
| Redux | Command + Observer + Singleton | 상태 관리 |

### 조합 적용 체크리스트

| 체크 항목 | 설명 |
|----------|------|
| 각 패턴이 독립적으로 필요한가? | 불필요한 복잡성 방지 |
| 조합 시 시너지가 있는가? | 1+1 > 2 효과 확인 |
| 팀이 이해할 수 있는 수준인가? | 유지보수성 고려 |
| 테스트가 용이한가? | 조합으로 인한 복잡성 확인 |
| 점진적 도입 가능한가? | 단계적 적용 계획 |

---

## 결론: 패턴 조합의 예술

패턴 조합은 **소프트웨어 설계의 예술**입니다. 올바른 조합은 다음을 가능하게 합니다:

### 성공적인 패턴 조합의 원칙

1. **단일 책임 유지**: 각 패턴이 명확한 책임을 가져야 합니다
2. **점진적 적용**: 한 번에 모든 패턴을 적용하지 말고 점진적으로 추가합니다
3. **복잡성 관리**: Facade 패턴으로 복잡성을 숨기고 단순한 인터페이스를 제공합니다
4. **테스트 가능성**: 패턴 조합이 테스트를 어렵게 만들어서는 안 됩니다
5. **문서화**: 복잡한 패턴 조합은 반드시 문서화해야 합니다

### 조합 시 주의사항

- **과도한 엔지니어링** 피하기
- **성능 영향** 고려하기
- **팀의 이해도** 확인하기
- **유지보수성** 검토하기

> *"패턴은 문제를 해결하는 도구입니다. 패턴 자체가 목적이 되어서는 안 됩니다. 조합의 복잡성이 얻는 이익보다 클 때는 과감히 단순화해야 합니다."*

패턴 조합의 진정한 가치는 **복잡한 문제를 우아하게 해결**하는 데 있습니다. 각 패턴의 장점을 살리면서도 전체적인 조화를 이루는 것이 바로 **설계의 예술**입니다. 