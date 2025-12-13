---
draft: true
---
# 13장. 클라우드 네이티브 아키텍처

## 학습 목표
- 12 Factor App 원칙을 이해하고 적용한다
- 컨테이너 아키텍처 패턴을 습득한다
- 서비스 메시 아키텍처의 개념을 파악한다
- 클라우드 보안 아키텍처를 학습한다

---

## Factor App 원칙

### Factor App이란?

12 Factor App은 **클라우드 네이티브 애플리케이션 개발을 위한 방법론**으로, 확장 가능하고 유지보수 가능한 SaaS 애플리케이션 구축 원칙입니다.

### 핵심 원칙 구현 예제

```java
// 1. 코드베이스 (Codebase) - 하나의 코드베이스, 여러 배포
// Git 저장소 하나에서 dev, staging, production 환경으로 배포

// 2. 종속성 (Dependencies) - 명시적 선언과 격리
// Maven/Gradle을 통한 명시적 의존성 관리
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web:2.7.0'
    implementation 'org.springframework.boot:spring-boot-starter-data-jpa:2.7.0'
}

// 3. 설정 (Config) - 환경에 설정 저장
@Configuration
public class DatabaseConfig {
    
    @Value("${DATABASE_URL}")
    private String databaseUrl;
    
    @Value("${DATABASE_USERNAME}")
    private String username;
    
    @Value("${DATABASE_PASSWORD}")
    private String password;
    
    @Bean
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(databaseUrl);
        config.setUsername(username);
        config.setPassword(password);
        return new HikariDataSource(config);
    }
}

// 4. 백엔드 서비스 (Backing Services) - 연결된 자원으로 취급
@Service
public class OrderService {
    
    // 데이터베이스를 연결된 자원으로 취급
    private final OrderRepository orderRepository;
    
    // 외부 API를 연결된 자원으로 취급
    private final PaymentGatewayClient paymentGateway;
    
    // 메시지 큐를 연결된 자원으로 취급  
    private final MessageQueue messageQueue;
    
    public OrderService(OrderRepository orderRepository,
                       PaymentGatewayClient paymentGateway,
                       MessageQueue messageQueue) {
        this.orderRepository = orderRepository;
        this.paymentGateway = paymentGateway;
        this.messageQueue = messageQueue;
    }
}

// 5. 빌드, 릴리스, 실행 (Build, Release, Run) - 단계 엄격히 분리
// Dockerfile
FROM openjdk:11-jre-slim
COPY target/app.jar app.jar
ENTRYPOINT ["java", "-jar", "/app.jar"]

# Jenkins Pipeline
pipeline {
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Release') {
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
                sh 'docker push myapp:${BUILD_NUMBER}'
            }
        }
        stage('Run') {
            steps {
                sh 'kubectl set image deployment/myapp myapp=myapp:${BUILD_NUMBER}'
            }
        }
    }
}

// 6. 프로세스 (Processes) - 무상태 프로세스로 실행
@RestController
public class OrderController {
    
    private final OrderService orderService;
    
    // 상태를 인스턴스 변수에 저장하지 않음
    @PostMapping("/orders")
    public ResponseEntity<Order> createOrder(@RequestBody CreateOrderRequest request) {
        // 모든 상태는 데이터베이스나 외부 스토어에 저장
        Order order = orderService.createOrder(request);
        return ResponseEntity.ok(order);
    }
}

// 7. 포트 바인딩 (Port Binding) - 포트 바인딩으로 서비스 공개
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// application.yml
server:
  port: ${PORT:8080}

// 8. 동시성 (Concurrency) - 프로세스 모델로 확장
@Configuration
@EnableAsync
public class AsyncConfig {
    
    @Bean
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(50);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.initialize();
        return executor;
    }
}

// 9. 폐기 가능 (Disposability) - 빠른 시작과 우아한 종료
@Component
public class GracefulShutdown implements ApplicationListener<ContextClosedEvent> {
    
    @Override
    public void onApplicationEvent(ContextClosedEvent event) {
        // 진행 중인 요청 완료 대기
        log.info("애플리케이션이 종료됩니다. 진행 중인 작업을 완료하는 중...");
        
        // 리소스 정리
        cleanupResources();
    }
    
    private void cleanupResources() {
        // 커넥션 풀 종료, 파일 핸들 해제 등
    }
}

// 10. 개발/프로덕션 동등성 (Dev/Prod Parity) - 개발, 스테이징, 프로덕션 환경을 최대한 비슷하게
// Docker Compose로 로컬 환경 구성
version: '3.8'
services:
  app:
    build: .
    environment:
      - DATABASE_URL=jdbc:postgresql://db:5432/myapp
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=myapp

// 11. 로그 (Logs) - 로그를 이벤트 스트림으로 취급
@Component
public class StructuredLogging {
    
    private final Logger logger = LoggerFactory.getLogger(StructuredLogging.class);
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    public void logOrderCreated(String orderId, String customerId) {
        try {
            Map<String, Object> logEvent = Map.of(
                "event", "order_created",
                "order_id", orderId,
                "customer_id", customerId,
                "timestamp", Instant.now().toString()
            );
            
            // 구조화된 로그를 stdout으로 출력
            logger.info(objectMapper.writeValueAsString(logEvent));
        } catch (Exception e) {
            logger.error("로그 작성 실패", e);
        }
    }
}

// 12. 관리 프로세스 (Admin Processes) - 일회성 관리 작업을 일회성 프로세스로 실행
@Component
public class DataMigrationCommand implements CommandLineRunner {
    
    private final DataMigrationService migrationService;
    
    @Override
    public void run(String... args) throws Exception {
        if (args.length > 0 && "migrate".equals(args[0])) {
            migrationService.migrate();
        }
    }
}
```

---

## 컨테이너 아키텍처 패턴

### 컨테이너 설계 패턴

```java
// 사이드카 패턴 (Sidecar Pattern)
// 메인 애플리케이션과 함께 배포되는 보조 컨테이너

// 메인 애플리케이션
@RestController
public class UserController {
    
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable String id) {
        User user = userService.findById(id);
        return ResponseEntity.ok(user);
    }
}

// Kubernetes Deployment with Sidecar
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  template:
    spec:
      containers:
      - name: user-service
        image: user-service:latest
        ports:
        - containerPort: 8080
      - name: logging-sidecar
        image: fluentd:latest
        volumeMounts:
        - name: log-volume
          mountPath: /var/log
      volumes:
      - name: log-volume
        emptyDir: {}

// 앰배서더 패턴 (Ambassador Pattern)
@Component
public class DatabaseAmbassador {
    
    private final List<DataSource> dataSources;
    private final LoadBalancer loadBalancer;
    
    public Connection getConnection() {
        DataSource selectedDataSource = loadBalancer.select(dataSources);
        return selectedDataSource.getConnection();
    }
}

// 어댑터 패턴 (Adapter Pattern)
@Component
public class LegacySystemAdapter {
    
    private final LegacyClient legacyClient;
    
    public ModernResponse adaptLegacyCall(ModernRequest request) {
        LegacyRequest legacyRequest = convertToLegacyFormat(request);
        LegacyResponse legacyResponse = legacyClient.call(legacyRequest);
        return convertToModernFormat(legacyResponse);
    }
}
```

### 멀티 스테이지 빌드

```dockerfile
# 멀티 스테이지 Dockerfile
# Stage 1: Build
FROM maven:3.8-openjdk-11 AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM openjdk:11-jre-slim
WORKDIR /app
COPY --from=builder /app/target/app.jar app.jar

# 보안을 위한 non-root 사용자 생성
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup
USER appuser

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

---

## 서비스 메시 아키텍처

### 서비스 메시란?

서비스 메시는 **마이크로서비스 간의 통신을 처리하는 인프라 계층**으로, 트래픽 관리, 보안, 관찰 가능성을 제공합니다.

### Istio 서비스 메시 구현

```yaml
# Virtual Service - 트래픽 라우팅
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
  - user-service
  http:
  - match:
    - headers:
        version:
          exact: v2
    route:
    - destination:
        host: user-service
        subset: v2
  - route:
    - destination:
        host: user-service
        subset: v1

# Destination Rule - 로드 밸런싱
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: user-service
spec:
  host: user-service
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2

# Service Entry - 외부 서비스 접근
apiVersion: networking.istio.io/v1beta1
kind: ServiceEntry
metadata:
  name: external-payment-service
spec:
  hosts:
  - payment-api.example.com
  ports:
  - number: 443
    name: https
    protocol: HTTPS
  location: MESH_EXTERNAL
  resolution: DNS
```

### Circuit Breaker with Istio

```java
// 애플리케이션 코드
@Service
public class PaymentService {
    
    private final PaymentClient paymentClient;
    
    public PaymentResult processPayment(PaymentRequest request) {
        try {
            return paymentClient.processPayment(request);
        } catch (Exception e) {
            // Istio가 Circuit Breaker를 처리하므로 
            // 애플리케이션 코드는 단순하게 유지
            throw new PaymentProcessingException("결제 처리 실패", e);
        }
    }
}
```

```yaml
# Istio Destination Rule with Circuit Breaker
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: payment-service
spec:
  host: payment-service
  trafficPolicy:
    outlierDetection:
      consecutiveErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
    connectionPool:
      tcp:
        maxConnections: 10
      http:
        http1MaxPendingRequests: 10
        maxRequestsPerConnection: 2
```

---

## 클라우드 보안 아키텍처

### Zero Trust 아키텍처

```java
// JWT 기반 인증
@RestController
public class SecureController {
    
    @PreAuthorize("hasRole('USER')")
    @GetMapping("/secure/data")
    public ResponseEntity<SecureData> getSecureData(
            @AuthenticationPrincipal JwtAuthenticationToken token) {
        
        String userId = token.getToken().getClaimAsString("sub");
        
        // 세밀한 권한 검사
        if (!hasAccessToResource(userId, "secure-data")) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }
        
        SecureData data = secureDataService.getData(userId);
        return ResponseEntity.ok(data);
    }
    
    private boolean hasAccessToResource(String userId, String resource) {
        // 실시간 권한 검증
        return authorizationService.checkAccess(userId, resource);
    }
}

// Security Configuration
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtDecoder(jwtDecoder()))
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            );
        
        return http.build();
    }
}
```

### Secrets 관리

```java
// Kubernetes Secrets 사용
@Configuration
public class SecretsConfig {
    
    @Value("${spring.datasource.password}")
    private String databasePassword;
    
    @Bean
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl("jdbc:postgresql://db:5432/myapp");
        config.setUsername("app_user");
        config.setPassword(databasePassword); // Kubernetes Secret에서 주입
        return new HikariDataSource(config);
    }
}
```

```yaml
# Kubernetes Secret
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  password: <base64-encoded-password>

# Deployment with Secret
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        env:
        - name: SPRING_DATASOURCE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
```

### 네트워크 보안

```yaml
# Network Policy - 네트워크 수준 보안
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-netpol
spec:
  podSelector:
    matchLabels:
      app: web
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

---

## 핵심 요약

### 클라우드 네이티브 아키텍처 구성 요소

| **구성 요소** | **목적** | **주요 기술** | **고려사항** |
|-------------|---------|-------------|------------|
| **12 Factor App** | 클라우드 적합성 | 환경 변수, 무상태 | 원칙 준수 |
| **컨테이너** | 일관된 실행 환경 | Docker, Kubernetes | 보안, 리소스 관리 |
| **서비스 메시** | 서비스 간 통신 | Istio, Linkerd | 복잡성 관리 |
| **Zero Trust** | 보안 모델 | JWT, mTLS | 성능 영향 |

### 구현 가이드라인
1. **12 Factor App 원칙 준수**
2. **컨테이너 최적화 및 보안**
3. **서비스 메시를 통한 트래픽 관리**
4. **Zero Trust 보안 모델 적용**

---

## 생각해보기

1. 기존 애플리케이션을 12 Factor App으로 마이그레이션하는 전략은?
2. 서비스 메시 도입 시 성능 오버헤드를 어떻게 관리할 것인가?
3. 클라우드 네이티브 환경에서의 데이터 보안 전략은?

---

## 추가 학습 자료

### 도서
- "Cloud Native Patterns" - Cornelia Davis
- "Kubernetes in Action" - Marko Lukša

### 온라인 자료
- 12factor.net 공식 사이트
- Istio 공식 문서
- CNCF Landscape 