---
draft: true
---
# 5장. 품질 속성과 아키텍처

## 학습 목표
- 아키텍처 품질 속성의 개념과 중요성을 이해한다
- 성능, 확장성, 가용성, 보안성, 유지보수성의 구체적 요구사항을 파악한다
- 품질 속성 간의 트레이드오프 관계를 분석한다
- 아키텍처 결정이 품질 속성에 미치는 영향을 평가한다

---

## 성능 (Performance)

### 성능의 핵심 메트릭

#### 응답 시간 (Response Time)
- **정의**: 요청부터 응답까지의 시간
- **측정 방법**: 평균, 최대, 백분위수(P95, P99)
- **목표 설정**: 사용자 경험 기반 임계값

#### 처리량 (Throughput)
- **정의**: 단위 시간당 처리 가능한 요청 수
- **측정 단위**: TPS(Transactions Per Second), RPS(Requests Per Second)
- **확장 전략**: 수평/수직 확장을 통한 처리량 증대

### 성능 최적화 전략

#### 캐싱 전략
```java
// Redis를 활용한 캐싱 구현
@Service
public class ProductService {
    
    @Autowired
    private ProductRepository productRepository;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    @Cacheable(value = "products", key = "#productId")
    public Product getProduct(String productId) {
        // 캐시 미스 시 데이터베이스에서 조회
        return productRepository.findById(productId)
            .orElseThrow(() -> new ProductNotFoundException("상품을 찾을 수 없습니다"));
    }
    
    @CacheEvict(value = "products", key = "#product.id")
    public Product updateProduct(Product product) {
        return productRepository.save(product);
    }
}
```

#### 비동기 처리
```java
// 비동기 처리를 통한 성능 개선
@Service
public class OrderService {
    
    @Async
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // 주문 생성 후 비동기로 처리
        CompletableFuture.allOf(
            CompletableFuture.runAsync(() -> sendOrderConfirmationEmail(event)),
            CompletableFuture.runAsync(() -> updateInventory(event)),
            CompletableFuture.runAsync(() -> notifyWarehouse(event))
        ).join();
    }
    
    private void sendOrderConfirmationEmail(OrderCreatedEvent event) {
        // 이메일 발송 로직
        emailService.sendOrderConfirmation(event.getCustomerId(), event.getOrderId());
    }
}
```

---

## 확장성 (Scalability)

### 확장 방식

#### 수직 확장 (Scale Up)
- **정의**: 하드웨어 성능 향상 (CPU, 메모리 증가)
- **장점**: 구현이 단순, 데이터 일관성 유지 용이
- **단점**: 물리적 한계 존재, 비용 증가

#### 수평 확장 (Scale Out)
- **정의**: 서버 인스턴스 수 증가
- **장점**: 이론적으로 무한 확장 가능, 비용 효율적
- **단점**: 복잡성 증가, 데이터 일관성 관리 어려움

### 확장성 설계 원칙

#### 무상태 설계 (Stateless Design)
```java
// 무상태 REST API 설계
@RestController
public class UserController {
    
    @GetMapping("/api/users/{userId}")
    public ResponseEntity<User> getUser(@PathVariable String userId, 
                                       HttpServletRequest request) {
        // JWT에서 인증 정보 추출 (세션 상태 없음)
        String token = extractTokenFromHeader(request);
        Claims claims = jwtService.parseToken(token);
        
        // 상태 정보를 외부 저장소에서 조회
        User user = userService.findById(userId);
        return ResponseEntity.ok(user);
    }
}
```

#### 데이터베이스 샤딩
```java
// 샤딩 전략 구현
@Component
public class UserShardingStrategy {
    
    public String determineShardKey(String userId) {
        // 사용자 ID 기반 해시 샤딩
        int hash = userId.hashCode();
        int shardIndex = Math.abs(hash) % 4; // 4개 샤드
        return "shard_" + shardIndex;
    }
    
    public DataSource getDataSource(String shardKey) {
        return shardDataSources.get(shardKey);
    }
}
```

---

## 가용성 (Availability)

### 가용성 메트릭

#### 업타임 목표
- **99.9%**: 연간 8.76시간 다운타임 허용
- **99.99%**: 연간 52.56분 다운타임 허용  
- **99.999%**: 연간 5.26분 다운타임 허용

### 고가용성 설계 패턴

#### Circuit Breaker 패턴
```java
// Hystrix를 활용한 Circuit Breaker 구현
@Service
public class PaymentService {
    
    @HystrixCommand(
        fallbackMethod = "fallbackPayment",
        commandProperties = {
            @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "20"),
            @HystrixProperty(name = "circuitBreaker.errorThresholdPercentage", value = "50"),
            @HystrixProperty(name = "circuitBreaker.sleepWindowInMilliseconds", value = "5000")
        }
    )
    public PaymentResult processPayment(String orderId, BigDecimal amount) {
        // 외부 결제 서비스 호출
        return externalPaymentClient.processPayment(orderId, amount);
    }
    
    public PaymentResult fallbackPayment(String orderId, BigDecimal amount) {
        // 장애 상황에서의 대체 처리
        return PaymentResult.pending("결제 서비스 일시 중단, 나중에 다시 시도됩니다");
    }
}
```

#### 장애 격리 (Bulkhead Pattern)
```java
// 스레드 풀 격리를 통한 장애 격리
@Configuration
public class ThreadPoolConfig {
    
    @Bean("orderProcessingExecutor")
    public Executor orderProcessingExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("OrderProcessing-");
        return executor;
    }
    
    @Bean("paymentProcessingExecutor")  
    public Executor paymentProcessingExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(3);
        executor.setMaxPoolSize(6);
        executor.setQueueCapacity(50);
        executor.setThreadNamePrefix("PaymentProcessing-");
        return executor;
    }
}
```

---

## 보안성 (Security)

### 보안 원칙

#### 기밀성 (Confidentiality)
- **데이터 암호화**: 전송 중(TLS) 및 저장 시(AES) 암호화
- **접근 제어**: 역할 기반 접근 제어(RBAC)
- **토큰 기반 인증**: JWT, OAuth 2.0 활용

#### 무결성 (Integrity)
- **디지털 서명**: 데이터 변조 방지
- **체크섬**: 데이터 전송 오류 검증
- **감사 로그**: 모든 변경 사항 추적

### 보안 구현 예제

#### JWT 기반 인증
```java
// JWT 토큰 생성 및 검증
@Service
public class JwtService {
    
    private final String SECRET_KEY = "mySecretKey";
    private final long EXPIRATION_TIME = 86400000; // 24시간
    
    public String generateToken(String username, List<String> roles) {
        return Jwts.builder()
            .setSubject(username)
            .claim("roles", roles)
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
            .signWith(SignatureAlgorithm.HS512, SECRET_KEY)
            .compact();
    }
    
    public Claims parseToken(String token) {
        return Jwts.parser()
            .setSigningKey(SECRET_KEY)
            .parseClaimsJws(token)
            .getBody();
    }
    
    public boolean isTokenExpired(String token) {
        Claims claims = parseToken(token);
        return claims.getExpiration().before(new Date());
    }
}
```

#### 입력 검증 및 SQL 인젝션 방지
```java
// 안전한 데이터베이스 접근
@Repository
public class UserRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    // PreparedStatement 사용으로 SQL 인젝션 방지
    public List<User> findUsersByRole(String role) {
        String query = "SELECT u FROM User u WHERE u.role = :role";
        return entityManager.createQuery(query, User.class)
            .setParameter("role", role)
            .getResultList();
    }
    
    // 입력 검증
    public User createUser(CreateUserRequest request) {
        // 입력 검증
        if (!isValidEmail(request.getEmail())) {
            throw new InvalidInputException("올바르지 않은 이메일 형식입니다");
        }
        
        if (!isStrongPassword(request.getPassword())) {
            throw new InvalidInputException("비밀번호는 8자 이상, 특수문자 포함해야 합니다");
        }
        
        // 비밀번호 해싱
        String hashedPassword = BCrypt.hashpw(request.getPassword(), BCrypt.gensalt());
        
        User user = new User(request.getUsername(), request.getEmail(), hashedPassword);
        return entityManager.merge(user);
    }
}
```

---

## 유지보수성 (Maintainability)

### 유지보수성 특성

#### 수정 용이성 (Modifiability)
- **모듈화**: 기능별 독립적인 모듈 구성
- **느슨한 결합**: 모듈 간 의존성 최소화
- **높은 응집도**: 관련 기능들의 집중화

#### 테스트 용이성 (Testability)
- **의존성 주입**: 테스트 더블 활용
- **단위 테스트**: 개별 컴포넌트 테스트
- **통합 테스트**: 시스템 간 상호작용 테스트

### 유지보수성 향상 기법

#### SOLID 원칙 적용
```java
// 단일 책임 원칙 (SRP) 적용
public class EmailService {
    public void sendEmail(String to, String subject, String body) {
        // 이메일 발송만 담당
    }
}

public class EmailNotificationService {
    private EmailService emailService;
    
    public void sendOrderConfirmation(Order order) {
        String subject = "주문 확인: " + order.getId();
        String body = createOrderConfirmationBody(order);
        emailService.sendEmail(order.getCustomerEmail(), subject, body);
    }
}

// 의존성 역전 원칙 (DIP) 적용
public interface PaymentProcessor {
    PaymentResult process(PaymentRequest request);
}

public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public PaymentResult process(PaymentRequest request) {
        // 신용카드 결제 처리
        return new PaymentResult(true, "결제 완료");
    }
}

public class PaymentService {
    private PaymentProcessor paymentProcessor;
    
    public PaymentService(PaymentProcessor paymentProcessor) {
        this.paymentProcessor = paymentProcessor;
    }
    
    public PaymentResult processPayment(PaymentRequest request) {
        return paymentProcessor.process(request);
    }
}
```

#### 자동화된 테스트
```java
// 단위 테스트 예제
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    
    @Mock
    private OrderRepository orderRepository;
    
    @Mock
    private PaymentService paymentService;
    
    @InjectMocks
    private OrderService orderService;
    
    @Test
    void 주문_생성_성공() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest("customer1", "product1", 2);
        when(paymentService.processPayment(any())).thenReturn(PaymentResult.success());
        
        // When
        Order result = orderService.createOrder(request);
        
        // Then
        assertThat(result.getStatus()).isEqualTo(OrderStatus.CONFIRMED);
        verify(orderRepository).save(any(Order.class));
    }
    
    @Test
    void 결제_실패시_주문_실패() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest("customer1", "product1", 2);
        when(paymentService.processPayment(any())).thenReturn(PaymentResult.failure("결제 실패"));
        
        // When & Then
        assertThatThrownBy(() -> orderService.createOrder(request))
            .isInstanceOf(PaymentFailedException.class);
    }
}
```

---

## 품질 속성 트레이드오프 분석

### 주요 트레이드오프 관계

| **품질 속성 A** | **품질 속성 B** | **트레이드오프 관계** | **해결 방안** |
|---------------|---------------|-------------------|-------------|
| **성능** | **보안** | 암호화로 인한 성능 저하 | 하드웨어 가속, 효율적 알고리즘 |
| **가용성** | **일관성** | CAP 정리에 따른 선택 | Eventually Consistent 모델 |
| **확장성** | **단순성** | 분산으로 인한 복잡성 증가 | 점진적 확장, 자동화 도구 |
| **보안** | **사용성** | 보안 강화로 인한 복잡성 | UX 최적화, SSO 도입 |

### 품질 속성 우선순위 결정 프레임워크

1. **비즈니스 요구사항 분석**: 핵심 비즈니스 목표 식별
2. **사용자 시나리오 매핑**: 주요 사용 사례별 품질 요구사항
3. **비용-효과 분석**: 품질 개선 비용 대비 비즈니스 가치
4. **위험 평가**: 품질 저하 시 비즈니스 영향도 평가

---

## 생각해보기

1. 현재 시스템에서 가장 중요한 품질 속성은 무엇이며, 그 이유는?
2. 성능과 보안 사이의 트레이드오프를 어떻게 균형있게 해결할 수 있을까?
3. 확장성을 위해 포기할 수 있는 다른 품질 속성은 무엇인가?

---

## 추가 학습 자료

### 도서
- "Software Architecture in Practice" - SEI 시리즈
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Release It!" - Michael Nygard

### 온라인 자료
- High Scalability 웹사이트
- AWS Well-Architected Framework
- Google Cloud Architecture Center 