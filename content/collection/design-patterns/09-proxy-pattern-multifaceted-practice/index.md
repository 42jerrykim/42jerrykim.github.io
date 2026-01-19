---
draft: true
collection_order: 91
title: "[Design Patterns] 프록시 패턴 실습 - 다면적 제어와 최적화"
description: "Proxy 패턴의 다양한 형태를 실제 프로젝트에 적용하는 실습입니다. Virtual Proxy, Protection Proxy, Remote Proxy, Smart Proxy 등을 구현하며 접근 제어, 지연 로딩, 캐싱, 원격 호출 등의 고급 기법을 마스터하고 성능 최적화와 보안 강화 방법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-09T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Structural Patterns
- Access Control
- Practice
- Performance Optimization
tags:
- Proxy Pattern Practice
- Virtual Proxy
- Protection Proxy
- Remote Proxy
- Smart Proxy
- Access Control
- Lazy Loading
- Caching
- Performance Optimization
- Security
- Remote Method Invocation
- AOP Implementation
- Structural Patterns
- Design Patterns
- GoF Patterns
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Software Architecture
- 프록시 패턴 실습
- 가상 프록시
- 보호 프록시
- 원격 프록시
- 스마트 프록시
- 접근 제어
- 지연 로딩
- 캐싱
- 성능 최적화
- 보안
- 원격 메서드 호출
- AOP 구현
- 구조 패턴
- 디자인 패턴
- GoF 패턴
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 소프트웨어 아키텍처
---

이 실습에서는 Virtual, Protection, Remote, Caching 등 다양한 Proxy 유형을 직접 구현하며 성능 최적화 기법을 익힙니다.

## 실습 목표
- 다양한 Proxy 유형 구현 (가상, 보호, 원격, 캐싱)
- 지연 로딩과 성능 최적화 기법
- AOP 스타일 횡단 관심사 처리
- 동적 프록시와 리플렉션 활용

## 실습 1: 이미지 로딩 Virtual Proxy

### 요구사항
대용량 이미지의 지연 로딩 시스템

### 코드 템플릿

```java
// TODO 1: Subject 인터페이스 정의
public interface Image {
    void display();
    int getWidth();
    int getHeight();
    long getFileSize();
    String getFilename();
}

// TODO 2: RealSubject 구현
public class RealImage implements Image {
    private final String filename;
    private byte[] imageData;
    private int width, height;
    private boolean loaded = false;
    
    public RealImage(String filename) {
        this.filename = filename;
        // TODO: 실제 로딩은 하지 않음
    }
    
    private void loadImageIfNeeded() {
        if (!loaded) {
            // TODO: 실제 이미지 로딩 (시간이 오래 걸리는 작업 시뮬레이션)
            System.out.println("Loading image: " + filename);
            try {
                Thread.sleep(2000); // 로딩 시간 시뮬레이션
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            loaded = true;
        }
    }
    
    // TODO: 이미지 관련 메서드들 구현
}

// TODO 3: Virtual Proxy 구현
public class ImageProxy implements Image {
    private final String filename;
    private RealImage realImage;
    private ImageMetadata metadata; // 빠르게 접근 가능한 메타데이터
    
    public ImageProxy(String filename) {
        this.filename = filename;
        this.metadata = loadMetadata(filename); // 빠른 메타데이터 로딩
    }
    
    private ImageMetadata loadMetadata(String filename) {
        // TODO: 빠른 메타데이터 로딩 (파일 헤더만 읽기)
        return new ImageMetadata(filename);
    }
    
    private RealImage getRealImage() {
        if (realImage == null) {
            realImage = new RealImage(filename);
        }
        return realImage;
    }
    
    // TODO: 메타데이터는 즉시 반환, 실제 데이터가 필요할 때만 로딩
}

// TODO 4: 캐싱 기능 추가
public class CachingImageProxy implements Image {
    private static final Map<String, RealImage> cache = new LRUCache<>(100);
    private final String filename;
    
    // TODO: LRU 캐시를 활용한 이미지 캐싱
}
```

## 실습 2: 보안 Protection Proxy

### 요구사항
사용자 권한에 따른 파일 접근 제어

### 코드 템플릿

```java
// TODO 1: 파일 서비스 인터페이스
public interface FileService {
    String readFile(String filename);
    void writeFile(String filename, String content);
    void deleteFile(String filename);
    List<String> listFiles(String directory);
}

// TODO 2: 실제 파일 서비스
public class RealFileService implements FileService {
    // TODO: 실제 파일 시스템 접근 구현
}

// TODO 3: 보안 프록시
public class SecurityFileProxy implements FileService {
    private final FileService fileService;
    private final AccessController accessController;
    
    public SecurityFileProxy(FileService fileService, AccessController accessController) {
        this.fileService = fileService;
        this.accessController = accessController;
    }
    
    @Override
    public String readFile(String filename) {
        User currentUser = getCurrentUser();
        if (!accessController.canRead(currentUser, filename)) {
            throw new SecurityException("Access denied: " + filename);
        }
        
        // TODO: 접근 로그 기록
        logAccess(currentUser, "READ", filename);
        return fileService.readFile(filename);
    }
    
    // TODO: 나머지 메서드들에도 보안 검사 적용
}

// TODO 4: 접근 제어자
public class AccessController {
    private final Map<String, Set<Permission>> userPermissions;
    private final Map<String, FilePermission> filePermissions;
    
    public boolean canRead(User user, String filename) {
        // TODO: 사용자 권한과 파일 권한 검사
        return false;
    }
    
    public boolean canWrite(User user, String filename) {
        // TODO: 쓰기 권한 검사
        return false;
    }
    
    public boolean canDelete(User user, String filename) {
        // TODO: 삭제 권한 검사
        return false;
    }
}
```

## 실습 3: 원격 서비스 Remote Proxy

### 요구사항
원격 서버의 서비스를 로컬에서 사용하는 것처럼 처리

### 코드 템플릿

```java
// TODO 1: 서비스 인터페이스
public interface UserService {
    User getUserById(Long id);
    List<User> searchUsers(String keyword);
    User createUser(CreateUserRequest request);
    void updateUser(Long id, UpdateUserRequest request);
}

// TODO 2: 로컬 구현 (테스트용)
public class LocalUserService implements UserService {
    // TODO: 로컬 메모리 기반 구현
}

// TODO 3: 원격 프록시
public class RemoteUserServiceProxy implements UserService {
    private final String serverUrl;
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public RemoteUserServiceProxy(String serverUrl) {
        this.serverUrl = serverUrl;
        this.httpClient = HttpClient.newHttpClient();
        this.objectMapper = new ObjectMapper();
    }
    
    @Override
    public User getUserById(Long id) {
        try {
            // TODO: HTTP GET 요청으로 원격 서버 호출
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(serverUrl + "/users/" + id))
                .GET()
                .build();
            
            HttpResponse<String> response = httpClient.send(request, 
                HttpResponse.BodyHandlers.ofString());
            
            // TODO: 응답을 User 객체로 변환
            return objectMapper.readValue(response.body(), User.class);
        } catch (Exception e) {
            throw new RuntimeException("Remote call failed", e);
        }
    }
    
    // TODO: 나머지 메서드들도 원격 호출로 구현
}

// TODO 4: 회로 차단기 기능 추가
public class CircuitBreakerProxy implements UserService {
    private final UserService delegate;
    private final CircuitBreaker circuitBreaker;
    
    // TODO: 원격 서비스 장애 시 회로 차단기 동작
}
```

## 실습 4: 동적 프록시 구현

### 코드 템플릿

```java
// TODO 1: 범용 프록시 핸들러
public class LoggingInvocationHandler implements InvocationHandler {
    private final Object target;
    private final Logger logger;
    
    public LoggingInvocationHandler(Object target) {
        this.target = target;
        this.logger = LoggerFactory.getLogger(target.getClass());
    }
    
    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        // TODO: 메서드 호출 전후 로깅
        long startTime = System.currentTimeMillis();
        
        try {
            Object result = method.invoke(target, args);
            // TODO: 성공 로그
            return result;
        } catch (Exception e) {
            // TODO: 에러 로그
            throw e;
        } finally {
            long endTime = System.currentTimeMillis();
            // TODO: 실행 시간 로그
        }
    }
}

// TODO 2: 프록시 팩토리
public class ProxyFactory {
    @SuppressWarnings("unchecked")
    public static <T> T createLoggingProxy(T target, Class<T> interfaceClass) {
        return (T) Proxy.newProxyInstance(
            interfaceClass.getClassLoader(),
            new Class[]{interfaceClass},
            new LoggingInvocationHandler(target)
        );
    }
    
    public static <T> T createCachingProxy(T target, Class<T> interfaceClass) {
        // TODO: 캐싱 프록시 생성
        return null;
    }
    
    public static <T> T createRetryProxy(T target, Class<T> interfaceClass, 
                                       int maxRetries) {
        // TODO: 재시도 프록시 생성
        return null;
    }
}

// TODO 3: 어노테이션 기반 프록시
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Cacheable {
    int ttlSeconds() default 300;
    String keyPrefix() default "";
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Retry {
    int maxAttempts() default 3;
    long delayMs() default 1000;
}

// TODO 4: AOP 스타일 프록시 처리기
public class AnnotationProxyHandler implements InvocationHandler {
    private final Object target;
    private final Map<String, Object> cache = new ConcurrentHashMap<>();
    
    // TODO: 어노테이션 기반 횡단 관심사 처리
}
```

## 체크리스트

### 기본 Proxy 유형
- [ ] Virtual Proxy (지연 로딩)
- [ ] Protection Proxy (접근 제어)  
- [ ] Remote Proxy (원격 접근)
- [ ] Caching Proxy (결과 캐싱)

### 고급 기능
- [ ] 동적 프록시 구현
- [ ] 어노테이션 기반 AOP
- [ ] 회로 차단기 패턴
- [ ] 성능 모니터링

### 최적화 및 확장
- [ ] LRU 캐시 구현
- [ ] 비동기 프록시
- [ ] 프록시 체이닝
- [ ] 메트릭 수집

## 추가 도전

1. **Smart Proxy**: 참조 카운팅과 자동 정리
2. **Copy-on-Write Proxy**: 쓰기 시점 복사
3. **Adaptive Proxy**: 상황에 따른 전략 변경
4. **Distributed Proxy**: 분산 환경 투명 접근

## 실무 적용

### Proxy 활용 사례
- ORM 지연 로딩 (Hibernate)
- Spring AOP 프록시
- HTTP 클라이언트 래핑
- 데이터베이스 커넥션 풀
- 보안 검사 계층
- 성능 모니터링

### 성능 고려사항
- 프록시 생성 비용
- 메서드 호출 오버헤드
- 메모리 사용량 증가
- 캐시 효율성

---

**핵심 포인트**: Proxy 패턴은 다양한 형태로 진화하여 현대 소프트웨어의 핵심 인프라가 되었습니다. 지연 로딩, 보안, 캐싱, 모니터링 등 횡단 관심사를 우아하게 처리하는 강력한 도구입니다. 