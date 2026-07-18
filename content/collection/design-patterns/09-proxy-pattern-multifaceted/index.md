---
draft: true
collection_order: 90
title: "[Design Patterns] 프록시 패턴의 다면성"
description: "대리자 역할을 수행하는 Proxy 패턴의 다양한 형태와 활용법을 심도 있게 분석합니다. Virtual, Protection, Remote, Cache Proxy의 특징과 적용 시나리오를 탐구하고, 현대 시스템에서의 프록시 활용(AOP, 지연 로딩, 보안)까지 다룹니다."
image: "wordcloud.png"
date: 2024-12-09T10:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Structural Patterns
- Proxy Patterns
- System Design
tags:
- Design-Pattern(디자인패턴)
- Performance(성능)
- GoF(Gang of Four)
- Memory(메모리)
- Structural-Pattern
- Proxy
- Caching(캐싱)
- Security(보안)
- Interface(인터페이스)
- OOP(객체지향)
- Coupling(결합도)
- Abstraction(추상화)
- Encapsulation(캡슐화)
- SOLID
- Software-Architecture(소프트웨어아키텍처)
- Clean-Architecture(클린아키텍처)
- Optimization(최적화)
- Implementation(구현)
- Best-Practices
- Code-Quality(코드품질)
- Maintainability
- Deep-Dive
- Advanced
- Java
- Authentication(인증)
- System-Design
---

Proxy 패턴의 다양한 형태와 활용법을 탐구합니다. 지연 로딩, 접근 제어, 원격 투명성 등 대리자의 강력한 능력을 학습합니다.

## 서론: 투명한 대리자의 예술

> *"진정한 대리자는 자신의 존재를 드러내지 않는다. 클라이언트는 실제 객체와 대화하고 있다고 믿지만, 그 뒤에서는 보이지 않는 손이 모든 것을 조율하고 있다."*

**Proxy 패턴**은 **"다른 객체에 대한 대리자 또는 자리표시자"**를 제공하는 패턴입니다. 마치 비서가 CEO를 대신해 업무를 처리하듯, Proxy는 실제 객체 대신 클라이언트의 요청을 받아 처리합니다.

하지만 단순한 대리자가 아닙니다. Proxy는 다음과 같은 **강력한 능력**들을 가지고 있습니다:

### 지연 로딩 (Lazy Loading)
- 비용이 큰 객체를 실제 필요한 시점까지 생성 지연
- 메모리 효율성과 초기 로딩 시간 단축

### 원격 투명성 (Remote Transparency)
- 네트워크 너머의 객체를 마치 로컬 객체처럼 사용
- 분산 시스템의 복잡성을 클라이언트로부터 숨김

### 접근 제어 (Access Control)
- 보안과 권한 검증을 투명하게 처리
- 감사 로깅과 모니터링 기능 제공

### 성능 최적화 (Performance Enhancement)
- 캐싱, 풀링, 배치 처리 등을 통한 성능 향상
- 리소스 사용 최적화

```java
// 현실적인 문제 상황
public class DocumentViewer {
    public void openDocument(String filename) {
        // 문제점들:
        // 1. 큰 파일은 로딩이 오래 걸림 (지연 로딩 필요)
        // 2. 원격 서버의 파일도 있음 (네트워크 투명성 필요)
        // 3. 민감한 문서는 권한 확인 필요 (보안 제어 필요)
        // 4. 자주 쓰는 문서는 캐싱하고 싶음 (성능 최적화 필요)
        
        Document doc = new RealDocument(filename);
        if (doc.isLarge()) {
            // 로딩이 오래 걸림... 😞
        }
        if (doc.isRemote()) {
            // 네트워크 에러 처리... 😰
        }
        if (doc.isConfidential()) {
            // 권한 확인... 🔐
        }
        doc.display();
    }
}
```

이런 복잡한 요구사항들을 어떻게 우아하게 해결할 수 있을까요?

## Virtual Proxy

### 패턴의 동기와 철학

Virtual Proxy는 **"비용이 큰 객체의 생성을 실제 필요한 시점까지 지연"**시키는 패턴입니다. 큰 이미지 파일, 무거운 데이터베이스 연결, 복잡한 계산 결과 등을 다룰 때 특히 유용합니다.

GoF는 원저에서 Proxy를 **"다른 객체에 대한 접근을 제어하기 위해 그 객체를 대리하는 자리표시자를 제공하는"** 패턴으로 정의하며, Virtual Proxy를 "필요할 때에만 생성해야 하는, 생성 비용이 큰 객체를 표현하는" 대리자로 소개한다(Gamma, Helm, Johnson, Vlissides, *Design Patterns*, 1994).

- 비용이 큰 객체의 지연 생성
- 이미지 로딩, 데이터베이스 연결 등
- 메모리 최적화와 성능 향상

```java
   // Subject 인터페이스
   interface Image {
       void display();
       String getInfo();
   }
   
   // RealSubject - 실제 이미지
   class RealImage implements Image {
       private String filename;
       private byte[] imageData;
       
       public RealImage(String filename) {
           this.filename = filename;
           loadFromDisk(); // 비용이 큰 작업
       }
       
       private void loadFromDisk() {
           System.out.println("Loading image: " + filename);
           // 실제로는 디스크에서 이미지 로딩
           try {
               Thread.sleep(1000); // 로딩 시뮬레이션
               imageData = new byte[1024 * 1024]; // 1MB 이미지
           } catch (InterruptedException e) {
               Thread.currentThread().interrupt();
           }
       }
       
       @Override
       public void display() {
           System.out.println("Displaying image: " + filename);
       }
       
       @Override
       public String getInfo() {
           return "Real image: " + filename + " (Size: " + imageData.length + " bytes)";
       }
   }
   
   // Virtual Proxy
   class ImageProxy implements Image {
       private String filename;
       private RealImage realImage;
       
       public ImageProxy(String filename) {
           this.filename = filename;
       }
       
       @Override
       public void display() {
           if (realImage == null) {
               realImage = new RealImage(filename); // 지연 로딩
           }
           realImage.display();
       }
       
       @Override
       public String getInfo() {
           if (realImage == null) {
               return "Proxy image: " + filename + " (Not loaded yet)";
           }
           return realImage.getInfo();
       }
   }
   ```
   
## Remote Proxy

네트워크 너머의 객체를 마치 로컬 객체처럼 다루게 해주는 형태입니다.

- 네트워크를 통한 원격 객체 접근
- RPC, REST API, gRPC 등
- 네트워크 투명성 제공

```java
   // 원격 서비스 인터페이스
   interface BankService {
       BigDecimal getBalance(String accountId);
       boolean transfer(String fromAccount, String toAccount, BigDecimal amount);
   }
   
   // 실제 원격 서비스 (서버에 위치)
   class RealBankService implements BankService {
       @Override
       public BigDecimal getBalance(String accountId) {
           // 실제 데이터베이스 조회
           return new BigDecimal("1000.00");
       }
       
       @Override
       public boolean transfer(String fromAccount, String toAccount, BigDecimal amount) {
           // 실제 송금 처리
           return true;
       }
   }
   
   // Remote Proxy (클라이언트에 위치)
   class BankServiceProxy implements BankService {
       private String serverUrl;
       private HttpClient httpClient;
       
       public BankServiceProxy(String serverUrl) {
           this.serverUrl = serverUrl;
           this.httpClient = HttpClient.newHttpClient();
       }
       
       @Override
       public BigDecimal getBalance(String accountId) {
           try {
               HttpRequest request = HttpRequest.newBuilder()
                   .uri(URI.create(serverUrl + "/balance/" + accountId))
                   .GET()
                   .build();
               
               HttpResponse<String> response = httpClient.send(request, 
                   HttpResponse.BodyHandlers.ofString());
               
               return new BigDecimal(response.body());
           } catch (Exception e) {
               throw new RuntimeException("Remote call failed", e);
           }
       }
       
       @Override
       public boolean transfer(String fromAccount, String toAccount, BigDecimal amount) {
           // HTTP POST 요청으로 송금 요청
           try {
               String jsonBody = String.format(
                   "{\"from\":\"%s\",\"to\":\"%s\",\"amount\":%s}",
                   fromAccount, toAccount, amount
               );
               
               HttpRequest request = HttpRequest.newBuilder()
                   .uri(URI.create(serverUrl + "/transfer"))
                   .header("Content-Type", "application/json")
                   .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                   .build();
               
               HttpResponse<String> response = httpClient.send(request,
                   HttpResponse.BodyHandlers.ofString());
               
               return response.statusCode() == 200;
           } catch (Exception e) {
               throw new RuntimeException("Remote transfer failed", e);
           }
       }
   }
   ```
   
## Protection Proxy

접근 권한을 검증한 뒤에만 실제 객체로 요청을 전달하는 형태입니다.

- 접근 권한 제어와 보안
- 인증, 인가, 감사 로깅
- 민감한 리소스 보호

```java
   // 민감한 정보를 다루는 서비스
   interface SecureDocument {
       String getContent();
       void updateContent(String content);
       void delete();
   }
   
   class ConfidentialDocument implements SecureDocument {
       private String content;
       private String filename;
       
       public ConfidentialDocument(String filename, String content) {
           this.filename = filename;
           this.content = content;
       }
       
       @Override
       public String getContent() {
           return content;
       }
       
       @Override
       public void updateContent(String content) {
           this.content = content;
           System.out.println("Document updated: " + filename);
       }
       
       @Override
       public void delete() {
           System.out.println("Document deleted: " + filename);
       }
   }
   
   // Protection Proxy
   class SecureDocumentProxy implements SecureDocument {
       private ConfidentialDocument realDocument;
       private User currentUser;
       private AuditLogger auditLogger;
       
       public SecureDocumentProxy(ConfidentialDocument document, User user) {
           this.realDocument = document;
           this.currentUser = user;
           this.auditLogger = new AuditLogger();
       }
       
       @Override
       public String getContent() {
           if (!hasReadPermission()) {
               throw new SecurityException("Read access denied");
           }
           auditLogger.log("Document accessed by: " + currentUser.getName());
           return realDocument.getContent();
       }
       
       @Override
       public void updateContent(String content) {
           if (!hasWritePermission()) {
               throw new SecurityException("Write access denied");
           }
           auditLogger.log("Document modified by: " + currentUser.getName());
           realDocument.updateContent(content);
       }
       
       @Override
       public void delete() {
           if (!hasDeletePermission()) {
               throw new SecurityException("Delete access denied");
           }
           auditLogger.log("Document deleted by: " + currentUser.getName());
           realDocument.delete();
       }
       
       private boolean hasReadPermission() {
           return currentUser.hasRole("READER") || 
                  currentUser.hasRole("WRITER") || 
                  currentUser.hasRole("ADMIN");
       }
       
       private boolean hasWritePermission() {
           return currentUser.hasRole("WRITER") || 
                  currentUser.hasRole("ADMIN");
       }
       
       private boolean hasDeletePermission() {
           return currentUser.hasRole("ADMIN");
       }
   }
   ```

## 현대 프레임워크에서의 Proxy 활용

- Spring AOP와 Dynamic Proxy
- JPA의 Lazy Loading
- ORM의 Entity Proxy
- CDN과 Reverse Proxy

### Spring AOP Dynamic Proxy 예시

```java
   @Service
   @Transactional
   public class UserService {
       @Autowired
       private UserRepository userRepository;
       
       @Cacheable("users")
       @LogExecutionTime
       public User findById(Long id) {
           return userRepository.findById(id);
       }
   }
   
   // Spring이 생성하는 동적 프록시 (의사코드)
   class UserService$Proxy implements UserService {
       private UserService target;
       private TransactionManager txManager;
       private CacheManager cacheManager;
       private Logger logger;
       
       @Override
       public User findById(Long id) {
           // 1. 캐시 확인
           User cached = cacheManager.get("users", id);
           if (cached != null) return cached;
           
           // 2. 트랜잭션 시작
           TransactionStatus tx = txManager.getTransaction();
           
           // 3. 실행 시간 측정 시작
           long startTime = System.currentTimeMillis();
           
           try {
               // 4. 실제 메서드 호출
               User result = target.findById(id);
               
               // 5. 결과 캐싱
               cacheManager.put("users", id, result);
               
               // 6. 트랜잭션 커밋
               txManager.commit(tx);
               
               return result;
           } catch (Exception e) {
               // 7. 트랜잭션 롤백
               txManager.rollback(tx);
               throw e;
           } finally {
               // 8. 실행 시간 로깅
               long executionTime = System.currentTimeMillis() - startTime;
               logger.info("Method execution time: {}ms", executionTime);
           }
       }
   }
   ```

## 구현 기법과 최적화

- Dynamic Proxy vs Static Proxy
- Reflection 기반 구현
- Bytecode 조작 (CGLIB, ASM)
- 성능 최적화 전략

### Dynamic Proxy 구현

```java
   // JDK Dynamic Proxy 사용
   public class ProxyFactory {
       public static <T> T createProxy(T target, Class<T> interfaceType) {
           return (T) Proxy.newProxyInstance(
               interfaceType.getClassLoader(),
               new Class[]{interfaceType},
               new InvocationHandler() {
                   @Override
                   public Object invoke(Object proxy, Method method, Object[] args) 
                           throws Throwable {
                       // Before advice
                       System.out.println("Before: " + method.getName());
                       long startTime = System.nanoTime();
                       
                       try {
                           // 실제 메서드 호출
                           Object result = method.invoke(target, args);
                           
                           // After advice
                           long endTime = System.nanoTime();
                           System.out.println("After: " + method.getName() + 
                               " (" + (endTime - startTime) + "ns)");
                           
                           return result;
                       } catch (InvocationTargetException e) {
                           // Exception advice
                           System.out.println("Exception in: " + method.getName());
                           throw e.getCause();
                       }
                   }
               }
           );
       }
   }
   ```

### Proxy와 다른 패턴의 관계

Proxy는 구조적으로 Decorator, Adapter와 자주 혼동되지만 목적이 다릅니다. Decorator는 대상과 동일한 인터페이스를 유지하면서 새로운 책임을 동적으로 "추가"하는 것이 목적이라 여러 겹으로 체이닝되는 경우가 흔한 반면, Proxy는 대상에 대한 "접근 자체를 제어"하는 것이 목적이라 보통 대상 하나당 하나의 계층으로 존재합니다(뒤의 "Proxy vs Decorator vs Adapter 비교" 표 참고). Adapter는 서로 다른 인터페이스를 호환되게 "변환"하는 것이 목적이므로 원본과 다른 인터페이스를 노출할 수 있지만, Proxy와 Decorator는 원본과 동일한 인터페이스를 유지한다는 점에서 Adapter와 구분됩니다. Facade는 여러 서브시스템을 하나의 단순한 인터페이스로 묶는다는 점에서 목적 자체는 Proxy와 다르지만, 단일 진입점 뒤로 복잡성을 감춘다는 점에서는 넓은 의미의 대리자 역할을 공유합니다. 실무에서는 이 패턴들이 조합되어 쓰이는 경우도 흔합니다. 예를 들어 Spring AOP의 프록시는 트랜잭션·보안 제어라는 Proxy 본연의 역할을 수행하면서도, 인터셉터 체인을 통해 로깅 같은 부가 기능을 덧붙이는 Decorator적 동작을 함께 보여줍니다.

### 깊이 있는 분석 포인트

1. **네트워크와 분산 시스템 관점:**
   - 네트워크 지연과 장애 처리
   - 로드 밸런싱과 장애 복구
   - 캐싱과 CDN 전략

2. **성능 최적화 관점:**
   - Reflection 오버헤드 최소화
   - Bytecode 생성과 클래스 로딩
   - 메모리 사용량과 가비지 컬렉션

3. **보안과 감사 관점:**
   - 인증과 인가 메커니즘
   - 감사 로깅과 모니터링
   - 취약점과 보안 고려사항

### 실제 사례 분석

1. **Hibernate Lazy Loading**
   ```java
   @Entity
   public class User {
       @Id
       private Long id;
       
       @OneToMany(fetch = FetchType.LAZY, mappedBy = "user")
       private List<Order> orders; // Proxy 객체로 지연 로딩
   }
   
   // Hibernate가 생성하는 프록시
   class User$HibernateProxy extends User {
       private boolean initialized = false;
       private SessionImplementor session;
       
       @Override
       public List<Order> getOrders() {
           if (!initialized) {
               // 실제 데이터베이스 조회
               List<Order> realOrders = session.createQuery(
                   "SELECT o FROM Order o WHERE o.user.id = :userId")
                   .setParameter("userId", getId())
                   .getResultList();
               super.setOrders(realOrders);
               initialized = true;
           }
           return super.getOrders();
       }
   }
   ```

2. **CDN과 Reverse Proxy**
   ```nginx
   # Nginx 설정 예시
   server {
       listen 80;
       server_name example.com;
       
       # 정적 자원은 CDN으로 프록시
       location ~* \.(jpg|jpeg|png|gif|css|js)$ {
           proxy_pass http://cdn.example.com;
           proxy_cache_valid 1d;
       }
       
       # API 요청은 백엔드 서버로 프록시
       location /api/ {
           proxy_pass http://backend-servers;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Java RMI와 Remote Proxy**
   ```java
   // RMI 인터페이스
   public interface Calculator extends Remote {
       int add(int a, int b) throws RemoteException;
       int multiply(int a, int b) throws RemoteException;
   }
   
   // RMI 구현체 (서버)
   public class CalculatorImpl extends UnicastRemoteObject 
                                implements Calculator {
       public CalculatorImpl() throws RemoteException {}
       
       @Override
       public int add(int a, int b) throws RemoteException {
           return a + b;
       }
       
       @Override
       public int multiply(int a, int b) throws RemoteException {
           return a * b;
       }
   }
   
   // 클라이언트에서 자동 생성되는 프록시 (Stub)
   // 네트워크 호출을 투명하게 처리
   ```

## 성능 분석과 최적화 전략

### Proxy 오버헤드 분석

```java
// 성능 측정 결과 (나노초/operation)
/*
작업 유형           | 직접 호출 | JDK Proxy | CGLIB  | 오버헤드
단순 메서드         |   1ns    |   15ns   |  12ns  | 1200-1500%
복잡한 메서드       |  100ns   |  115ns   | 112ns  |    12-15%
네트워크 호출       |  50ms    |  50.1ms  | 50.1ms |     0.2%
데이터베이스 조회   |  10ms    |  10.05ms |10.05ms |     0.5%

결론:
- 단순한 메서드: Proxy 오버헤드가 상당함
- 복잡한 작업: 오버헤드가 상대적으로 미미함
- I/O 작업: 오버헤드가 거의 무시할 수준
- 실무에서는 대부분 복잡한 작업이므로 큰 문제 없음

※ 위 수치는 특정 환경에서 관찰될 수 있는 예시 값이며, JVM 워밍업·JIT 최적화·하드웨어에 따라 실제 측정치는 달라질 수 있습니다. 절대값보다 "작업이 가벼울수록 상대적 오버헤드가 커진다"는 경향성에 주목하세요.
*/

// 최적화된 Proxy 구현
public class OptimizedProxyFactory {
    
    // 캐시를 통한 성능 최적화
    private static final Map<Class<?>, Method[]> METHOD_CACHE = new ConcurrentHashMap<>();
    private static final Map<String, Class<?>> PROXY_CLASS_CACHE = new ConcurrentHashMap<>();
    
    public static <T> T createOptimizedProxy(T target, Class<T> interfaceType, 
                                           ProxyInterceptor interceptor) {
        // 1. 프록시 클래스 캐싱
        String cacheKey = interfaceType.getName() + "_" + interceptor.getClass().getName();
        Class<?> proxyClass = PROXY_CLASS_CACHE.computeIfAbsent(cacheKey, k -> 
            Proxy.getProxyClass(interfaceType.getClassLoader(), interfaceType)
        );
        
        // 2. 메서드 정보 캐싱
        Method[] methods = METHOD_CACHE.computeIfAbsent(interfaceType, Class::getDeclaredMethods);
        
        // 3. 최적화된 InvocationHandler
        InvocationHandler handler = new OptimizedInvocationHandler(target, interceptor, methods);
        
        try {
            return (T) proxyClass.getConstructor(InvocationHandler.class).newInstance(handler);
        } catch (Exception e) {
            throw new RuntimeException("Failed to create optimized proxy", e);
        }
    }
    
    private static class OptimizedInvocationHandler implements InvocationHandler {
        private final Object target;
        private final ProxyInterceptor interceptor;
        private final Method[] cachedMethods;
        
        public OptimizedInvocationHandler(Object target, ProxyInterceptor interceptor, Method[] methods) {
            this.target = target;
            this.interceptor = interceptor;
            this.cachedMethods = methods;
        }
        
        @Override
        public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
            // Object 메서드는 별도 처리
            if (method.getDeclaringClass() == Object.class) {
                return method.invoke(target, args);
            }
            
            // 인터셉터 적용
            return interceptor.intercept(target, method, args);
        }
    }
}

// 프록시 인터셉터 인터페이스
@FunctionalInterface
public interface ProxyInterceptor {
    Object intercept(Object target, Method method, Object[] args) throws Throwable;
}
```

### 현대적 Proxy 활용: Reactive Programming

```java
// Reactive Streams와 Proxy 패턴의 조합
public class ReactiveServiceProxy implements UserService {
    private final UserService target;
    private final CircuitBreaker circuitBreaker;
    private final Cache<String, User> cache;
    
    public ReactiveServiceProxy(UserService target) {
        this.target = target;
        this.circuitBreaker = CircuitBreaker.ofDefaults("userService");
        this.cache = Caffeine.newBuilder()
            .maximumSize(1000)
            .expireAfterWrite(Duration.ofMinutes(10))
            .build();
    }
    
    @Override
    public Mono<User> findById(String userId) {
        return Mono.fromSupplier(() -> cache.getIfPresent(userId))
            .switchIfEmpty(
                // 캐시 미스 시 실제 서비스 호출
                Mono.fromSupplier(() -> circuitBreaker.executeSupplier(() -> {
                    User user = target.findById(userId).block();
                    cache.put(userId, user);
                    return user;
                }))
                .subscribeOn(Schedulers.boundedElastic())
                .timeout(Duration.ofSeconds(5))
                .retry(2)
                .onErrorResume(throwable -> {
                    // 폴백 처리
                    return Mono.just(User.defaultUser(userId));
                })
            );
    }
    
    @Override
    public Flux<User> findAll() {
        return Flux.defer(() -> 
            Flux.fromIterable(target.findAll().collectList().block())
        )
        .subscribeOn(Schedulers.boundedElastic())
        .timeout(Duration.ofSeconds(10))
        .onErrorResume(throwable -> 
            Flux.just(User.defaultUser("error"))
        );
    }
}

// Service Mesh와 Proxy 패턴
@Component
public class ServiceMeshProxy implements OrderService {
    private final LoadBalancer loadBalancer;
    private final MetricsCollector metricsCollector;
    private final DistributedTracing tracing;
    
    @Override
    public Order createOrder(OrderRequest request) {
        // 1. 분산 추적 시작
        Span span = tracing.nextSpan().name("create-order");
        
        try (Tracer.SpanInScope ws = tracing.tracer().withSpanInScope(span)) {
            // 2. 로드 밸런싱
            ServiceInstance instance = loadBalancer.choose("order-service");
            
            // 3. 메트릭 수집 시작
            Timer.Sample sample = Timer.start(metricsCollector.registry());
            
            // 4. 실제 서비스 호출
            Order result = invokeService(instance, request);
            
            // 5. 메트릭 기록
            sample.stop(metricsCollector.timer("order.create"));
            
            // 6. 추적 정보 추가
            span.tag("order.id", result.getId());
            span.tag("success", "true");
            
            return result;
            
        } catch (Exception e) {
            span.tag("error", e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
}
```

## 한눈에 보는 Proxy 패턴

### Proxy 유형별 비교표

| Proxy 유형 | 핵심 목적 | 사용 시나리오 | 성능 영향 |
|-----------|----------|-------------|----------|
| Virtual Proxy | 지연 로딩 | 큰 이미지, 무거운 객체 | 초기 로딩 개선 |
| Protection Proxy | 접근 제어 | 권한 검증, 보안 | 약간의 오버헤드 |
| Remote Proxy | 원격 투명성 | 분산 시스템, RMI | 네트워크 지연 |
| Cache Proxy | 성능 최적화 | 자주 접근하는 데이터 | 캐시 히트 시 향상 |
| Smart Proxy | 추가 기능 | 로깅, 카운팅, 잠금 | 기능에 따라 다름 |
| Logging Proxy | 감사 추적 | 호출 기록, 디버깅 | I/O 오버헤드 |

### Proxy vs Decorator vs Adapter 비교

| 비교 항목 | Proxy | Decorator | Adapter |
|----------|-------|-----------|---------|
| 핵심 목적 | 접근 제어 | 기능 추가 | 인터페이스 변환 |
| 인터페이스 | 동일 유지 | 동일 유지 | 변환 |
| 대상 생성 | Proxy가 제어 | 외부에서 전달 | 외부에서 전달 |
| 재귀 구조 | 보통 X | O (체이닝) | X |
| 투명성 | 높음 | 높음 | 중간 |

### 구현 방식별 특성

| 구현 방식 | 장점 | 단점 | 적용 시점 |
|----------|------|------|----------|
| 정적 Proxy | 컴파일타임 안전, 디버깅 용이 | 인터페이스당 클래스 필요 | 대상 명확, 개수 적음 |
| 동적 Proxy (JDK) | 런타임 생성, 유연함 | 인터페이스만 지원 | 인터페이스 기반 설계 |
| CGLIB Proxy | 클래스도 프록시 가능 | final 클래스 불가 | Spring AOP 기본 |
| 바이트코드 조작 | 최고 유연성 | 복잡성, 디버깅 어려움 | 고급 AOP 요구 |

### 성능 오버헤드 가이드

| 작업 유형 | 직접 호출 | Proxy 호출 | 오버헤드 비율 |
|----------|---------|-----------|-------------|
| 단순 getter | 1ns | ~15ns | ~1,200-1,500% |
| 비즈니스 로직 | 1ms | 1.01ms | ~1% |
| 데이터베이스 조회 | 10ms | 10.05ms | ~0.5% |
| 네트워크 I/O | 50ms | 50.1ms | ~0.2% |

※ 위 "Proxy 오버헤드 분석"의 측정 결과와 동일한 시나리오를 기준으로 통일한 예시 수치이며, 실제 값은 환경에 따라 달라질 수 있습니다.

### Proxy 선택 결정 가이드

| 상황 | 권장 Proxy 유형 | 이유 |
|------|---------------|------|
| 대용량 이미지 갤러리 | Virtual Proxy | 필요 시점 로딩 |
| 민감한 데이터 접근 | Protection Proxy | 권한 사전 검증 |
| 마이크로서비스 호출 | Remote Proxy | 네트워크 투명성 |
| 자주 조회하는 설정 | Cache Proxy | 반복 호출 최적화 |
| 호출 추적/디버깅 | Logging Proxy | 감사 로그 생성 |

### Spring AOP Proxy 비교

| 특성 | JDK Dynamic Proxy | CGLIB Proxy |
|------|------------------|-------------|
| 대상 | 인터페이스 기반 | 클래스 기반 |
| 생성 속도 | 빠름 | 느림 (바이트코드 생성) |
| 실행 속도 | 약간 느림 | 빠름 |
| final 메서드 | 지원 | 불가 |
| Spring 기본 | 인터페이스 있을 때 | 인터페이스 없을 때 |

### 적용 체크리스트

| 체크 항목 | 설명 |
|----------|------|
| 실제 객체 접근 제어 필요? | Protection/Virtual Proxy |
| 원격 객체 로컬처럼 사용? | Remote Proxy |
| 비싼 연산 결과 재사용? | Cache Proxy |
| 호출 전후 추가 작업? | Smart/Logging Proxy |
| AOP 적용 고려? | 동적 Proxy + 어노테이션 |

---

## 결론: 투명성과 다면성의 조화

Proxy 패턴을 깊이 탐구한 결과, 이 패턴은 **단순한 대리자 역할을 넘어서 현대 소프트웨어 아키텍처의 핵심 메커니즘**임을 확인했습니다.

### Proxy 패턴의 핵심 가치:

1. **투명성 (Transparency)**: 클라이언트가 복잡성을 의식하지 않는 자연스러운 사용
2. **제어성 (Control)**: 접근, 생성, 성능을 세밀하게 제어
3. **확장성 (Extensibility)**: 기존 코드 변경 없이 새로운 기능 추가
4. **분산 지원 (Distribution)**: 네트워크와 분산 환경의 복잡성 추상화

### 세 가지 핵심 형태의 현대적 의미:

```
전통적 Proxy → 현대적 진화

Virtual Proxy →
- JPA Lazy Loading
- React Suspense
- CDN Cache
- Serverless Cold Start 최적화

Remote Proxy →
- RESTful API Client
- gRPC Stub
- Service Mesh
- Event-driven Architecture

Protection Proxy →
- OAuth2 & JWT
- API Gateway
- Zero Trust Security
- Audit & Compliance
```

### 현대 아키텍처에서의 활용:

**1. 마이크로서비스**: 서비스 간 통신의 투명성과 회복력 제공
**2. 클라우드 네이티브**: 분산 환경의 복잡성 추상화
**3. 리액티브 시스템**: 비동기 처리와 백프레셔 관리
**4. 보안 아키텍처**: 제로 트러스트와 세밀한 접근 제어

주의사항: 단순한 작업에서는 오버헤드를 고려해야 하고, 프록시 체인이 깊어지면 디버깅이 어려워지며, 메모리 누수와 순환 참조 방지, 예외 처리와 에러 전파를 신중히 설계해야 합니다. 각 Proxy 유형을 언제 선택할지는 앞의 "Proxy 선택 결정 가이드" 표를 기준으로 판단하세요.

## 평가 기준

이 글에서 다룬 Proxy 패턴의 적용 여부는 다음 기준으로 판단할 수 있습니다.

- **접근 제어가 핵심 목적인가**: 단순히 기능을 덧붙이고 싶다면 Decorator를, 인터페이스 자체를 바꾸고 싶다면 Adapter를 검토합니다. Proxy는 "동일한 인터페이스를 유지하면서 접근을 제어"할 때만 선택합니다.
- **지연·원격·보안 중 어떤 문제를 푸는가**: Virtual Proxy는 생성 비용, Remote Proxy는 네트워크 투명성, Protection Proxy는 권한 검증이라는 서로 다른 문제를 풉니다. 세 문제 중 어느 것도 해당하지 않으면 Proxy가 과한 설계일 수 있습니다.
- **오버헤드가 감당 가능한가**: "성능 오버헤드 가이드" 표에서 보듯 I/O 중심 작업은 오버헤드가 무시할 수준이지만, 단순 getter처럼 가벼운 호출에 Proxy를 씌우면 상대적 오버헤드가 커집니다.
- **프록시 체인의 디버깅 비용을 감수할 수 있는가**: 프록시가 여러 겹 중첩되면 스택 추적이 어려워지므로, 팀의 디버깅 관례와 도구 지원을 함께 고려해야 합니다.

### 성능과 복잡성의 균형:

Proxy 패턴의 성공적인 적용을 위해서는 **성능 오버헤드와 제공되는 가치 사이의 균형**을 잘 맞춰야 합니다:

- **I/O 중심 작업**: 오버헤드가 미미하므로 적극적 활용
- **CPU 중심 작업**: 오버헤드를 신중히 고려하여 선택적 적용
- **분산 환경**: 네트워크 지연에 비해 프록시 오버헤드는 무시할 수준

Proxy 패턴은 **투명성이라는 강력한 원칙** 하에 복잡한 현실 문제를 우아하게 해결하는 도구입니다. 특히 현대의 분산 시스템, 클라우드 환경, 마이크로서비스 아키텍처에서는 없어서는 안 될 핵심 패턴으로 자리잡고 있습니다.

다음 글에서는 **Bridge와 Flyweight 패턴**을 탐구하겠습니다. 구현과 추상화의 분리, 그리고 메모리 효율성의 극대화를 통해 대규모 시스템을 우아하게 설계하는 방법을 살펴보겠습니다.

---

**핵심 메시지:**
"Proxy 패턴은 단순한 대리자 역할을 넘어서, 현대 분산 시스템과 프레임워크의 핵심 메커니즘이다. 투명성을 유지하면서도 성능, 보안, 확장성을 제공하는 강력한 도구로, 특히 AOP와 ORM, 분산 시스템에서 없어서는 안 될 패턴이다." 