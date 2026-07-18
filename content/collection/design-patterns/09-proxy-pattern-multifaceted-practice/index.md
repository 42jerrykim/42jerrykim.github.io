---
draft: true
collection_order: 91
title: "[Design Patterns] 프록시 패턴 실습 - 다면적 제어와 최적화"
slug: "proxy-pattern-multifaceted-practice"
description: "Proxy 패턴의 다양한 형태를 실제 프로젝트에 적용하는 실습입니다. Virtual Proxy, Protection Proxy, Remote Proxy, Smart Proxy 등을 구현하며 접근 제어, 지연 로딩, 캐싱, 원격 호출 등의 고급 기법을 마스터하고 성능 최적화와 보안 강화 방법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-09T11:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Structural Patterns
- Access Control
- Practice
- Performance Optimization
tags:
- Caching(캐싱)
- Performance(성능)
- Security(보안)
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Tutorial(튜토리얼)
- Implementation(구현)
- Software-Architecture(소프트웨어아키텍처)
- Structural-Pattern
- Proxy
- Interface(인터페이스)
- OOP(객체지향)
- Optimization(최적화)
- Best-Practices
- Code-Quality(코드품질)
- Maintainability
- Testing(테스트)
- Guide(가이드)
- Case-Study
- Advanced
- Java
- Authentication(인증)
- Memory(메모리)
- SOLID
- Clean-Architecture(클린아키텍처)
- System-Design
---

이 실습에서는 Virtual, Protection, Remote, Caching 등 다양한 Proxy 유형을 직접 구현하며 성능 최적화 기법을 익힙니다.

네 가지 Proxy 유형은 겉보기엔 모두 "대상 객체를 감싸는 클래스"라는 같은 모양이지만, 각각 해결하는 문제가 다릅니다. Virtual Proxy는 "생성 비용이 큰 객체를 언제 만들 것인가", Protection Proxy는 "누가 접근할 수 있는가", Remote Proxy는 "물리적으로 떨어진 객체를 어떻게 로컬처럼 다룰 것인가"라는 서로 다른 질문에 답합니다. 이 차이 때문에 실무에서 "Proxy를 쓸까"보다 "어떤 문제 때문에 Proxy 유형을 쓸까"를 먼저 판단하는 것이 중요하며, 아래 실습들은 이 네 가지 문제 상황을 각각 별도로 다룹니다.

GoF는 Proxy를 **"다른 객체에 대한 접근을 제어하기 위해 그 객체를 대리하는 자리표시자를 제공하는"** 패턴으로 정의한다(Gamma, Helm, Johnson, Vlissides, *Design Patterns*, 1994). 아래 네 실습은 이 정의에서 "접근을 제어"하는 방식(생성 시점 제어, 권한 제어, 위치 제어, 반복 호출 제어)이 유형마다 어떻게 달라지는지를 코드로 확인합니다.

## 실습 목표
- 실습 1에서 `ImageProxy`가 `getWidth()` 같은 메타데이터 조회 시점과 `display()` 같은 실제 데이터 조회 시점을 구분해, 후자에서만 `RealImage`가 생성됨을 로그로 확인할 수 있다.
- 실습 2에서 권한이 없는 `User`로 `SecurityFileProxy.writeFile()`을 호출했을 때 `SecurityException`이 발생하고 `RealFileService`의 상태가 변경되지 않음을 테스트로 검증할 수 있다.
- 실습 3에서 `RemoteUserServiceProxy`와 `LocalUserService`를 동일한 `UserService` 타입으로 다루면서, 호출부 코드를 전혀 수정하지 않고 두 구현을 교체할 수 있음을 보일 수 있다.
- 실습 4에서 `LoggingInvocationHandler` 하나로 서로 다른 두 인터페이스에 대한 프록시를 생성해, 정적 Proxy 클래스를 인터페이스 수만큼 만들지 않아도 됨을 확인할 수 있다.

## 실습 1: 이미지 로딩 Virtual Proxy

### 왜 Virtual Proxy인가

수백 장의 대용량 이미지를 목록에 나열할 때, 화면에 보이지도 않는 이미지까지 전부 디스크에서 읽어 메모리에 올리면 초기 로딩이 매우 느려집니다. `ImageProxy`는 파일명과 메타데이터만 먼저 들고 있다가, `display()`처럼 실제 픽셀 데이터가 필요한 시점에만 `RealImage`를 생성합니다. 클라이언트는 `Image` 인터페이스만 보고 있으므로 지금 다루는 것이 프록시인지 실제 이미지인지 신경 쓸 필요가 없습니다.

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

### 왜 Protection Proxy인가

파일 읽기/쓰기/삭제마다 권한 검사 코드를 `RealFileService` 내부에 심으면, 서비스 로직과 보안 로직이 뒤섞여 둘 다 테스트하기 어려워집니다. `SecurityFileProxy`는 실제 파일 접근 로직은 `RealFileService`에 그대로 두고, 그 앞단에서 `AccessController`로 권한을 검증한 뒤에만 위임합니다. 권한 정책이 바뀌어도 `RealFileService`는 전혀 건드릴 필요가 없습니다.

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
    private final Map<String, String> storage = new ConcurrentHashMap<>();

    @Override
    public String readFile(String filename) {
        String content = storage.get(filename);
        if (content == null) {
            throw new NoSuchElementException("File not found: " + filename);
        }
        return content;
    }

    @Override
    public void writeFile(String filename, String content) {
        storage.put(filename, content);
    }

    @Override
    public void deleteFile(String filename) {
        storage.remove(filename);
    }

    @Override
    public List<String> listFiles(String directory) {
        List<String> result = new ArrayList<>();
        for (String name : storage.keySet()) {
            if (name.startsWith(directory)) {
                result.add(name);
            }
        }
        return result;
    }
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
        
        logAccess(currentUser, "READ", filename);
        return fileService.readFile(filename);
    }

    @Override
    public void writeFile(String filename, String content) {
        User currentUser = getCurrentUser();
        if (!accessController.canWrite(currentUser, filename)) {
            throw new SecurityException("Access denied: " + filename);
        }
        logAccess(currentUser, "WRITE", filename);
        fileService.writeFile(filename, content);
    }

    @Override
    public void deleteFile(String filename) {
        User currentUser = getCurrentUser();
        if (!accessController.canDelete(currentUser, filename)) {
            throw new SecurityException("Access denied: " + filename);
        }
        logAccess(currentUser, "DELETE", filename);
        fileService.deleteFile(filename);
    }

    @Override
    public List<String> listFiles(String directory) {
        // 목록 조회는 읽기 권한과 동일한 기준으로 검사한다
        User currentUser = getCurrentUser();
        if (!accessController.canRead(currentUser, directory)) {
            throw new SecurityException("Access denied: " + directory);
        }
        return fileService.listFiles(directory);
    }

    private User getCurrentUser() {
        // TODO: 실제로는 인증 컨텍스트(SecurityContext 등)에서 조회
        return CurrentUserHolder.get();
    }

    private void logAccess(User user, String action, String filename) {
        System.out.println("[AUDIT] " + user.getName() + " " + action + " " + filename);
    }
}

// TODO 4: 접근 제어자
public class AccessController {
    private final Map<String, Set<Permission>> userPermissions;
    private final Map<String, FilePermission> filePermissions;

    public AccessController(Map<String, Set<Permission>> userPermissions,
                             Map<String, FilePermission> filePermissions) {
        this.userPermissions = userPermissions;
        this.filePermissions = filePermissions;
    }
    
    public boolean canRead(User user, String filename) {
        return hasPermission(user, Permission.READ);
    }
    
    public boolean canWrite(User user, String filename) {
        return hasPermission(user, Permission.WRITE);
    }
    
    public boolean canDelete(User user, String filename) {
        return hasPermission(user, Permission.DELETE);
    }

    private boolean hasPermission(User user, Permission permission) {
        // TODO: filePermissions까지 함께 반영하는 세밀한 검사로 확장 가능
        Set<Permission> permissions = userPermissions.get(user.getName());
        return permissions != null && permissions.contains(permission);
    }
}

// TODO 5: 최소 지원 타입 (실습 편의를 위한 뼈대)
public enum Permission {
    READ, WRITE, DELETE
}

public class FilePermission {
    private final String filename;
    private final Set<Permission> allowed;

    public FilePermission(String filename, Set<Permission> allowed) {
        this.filename = filename;
        this.allowed = allowed;
    }

    public boolean allows(Permission permission) {
        return allowed.contains(permission);
    }
}

public class User {
    private final String name;

    public User(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}

// 실습 편의용 최소 홀더 (실제 서비스에서는 인증 프레임워크의 SecurityContext 등으로 대체)
public class CurrentUserHolder {
    private static final ThreadLocal<User> CURRENT = ThreadLocal.withInitial(() -> new User("guest"));

    public static User get() {
        return CURRENT.get();
    }
}
```

## 실습 3: 원격 서비스 Remote Proxy

### 왜 Remote Proxy인가

클라이언트 코드가 "이 호출이 네트워크를 타는지"를 매번 의식해야 한다면, HTTP 요청 구성·직렬화·예외 처리 코드가 비즈니스 로직 곳곳에 흩어집니다. `RemoteUserServiceProxy`는 `UserService` 인터페이스 뒤에서 HTTP 통신을 캡슐화하여, 클라이언트가 `LocalUserService`를 쓰든 원격 프록시를 쓰든 동일한 코드로 호출할 수 있게 합니다.

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

### 왜 동적 프록시인가

로깅, 캐싱, 재시도 같은 부가 기능을 인터페이스마다 별도의 정적 Proxy 클래스로 만들면 대상 인터페이스 수만큼 클래스가 늘어납니다. `LoggingInvocationHandler`처럼 `InvocationHandler`를 구현하면, `Proxy.newProxyInstance()`가 런타임에 임의의 인터페이스에 대한 프록시 인스턴스를 만들어주므로 하나의 핸들러로 여러 인터페이스에 동일한 횡단 관심사를 적용할 수 있습니다.

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
- [ ] Virtual Proxy (지연 로딩) — `RealImage` 생성 시점을 `display()` 호출까지 미뤄야 대용량 이미지 목록의 초기 로딩 비용을 없앨 수 있다.
- [ ] Protection Proxy (접근 제어) — 권한 검사를 `SecurityFileProxy`에 모아두지 않으면 `RealFileService` 내부 곳곳에 보안 로직이 흩어져 테스트하기 어려워진다.
- [ ] Remote Proxy (원격 접근) — HTTP 통신 세부사항을 `RemoteUserServiceProxy` 뒤에 숨겨야 클라이언트 코드가 로컬/원격 구현을 동일하게 다룰 수 있다.
- [ ] Caching Proxy (결과 캐싱) — 동일 이미지를 반복 요청할 때마다 디스크를 다시 읽으면 `Virtual Proxy`의 지연 로딩 이득이 캐싱 없이는 매번 소모된다.

### 고급 기능
- [ ] 동적 프록시 구현 — `LoggingInvocationHandler` 하나로 여러 인터페이스를 처리해야 인터페이스 수만큼 정적 Proxy 클래스를 만드는 비용을 피할 수 있다.
- [ ] 어노테이션 기반 AOP — `@Cacheable`, `@Retry` 같은 선언적 표시가 없으면 캐싱·재시도 로직을 메서드마다 수동으로 반복 작성해야 한다.
- [ ] 회로 차단기 패턴 — 원격 서비스가 장애 상태일 때도 계속 호출을 시도하면 장애가 클라이언트 전체로 전파되므로 `CircuitBreakerProxy`로 차단해야 한다.
- [ ] 성능 모니터링 — 프록시 계층에서 실행 시간을 기록해야 어떤 호출이 오버헤드의 주된 원인인지 코드 수정 없이 파악할 수 있다.

### 최적화 및 확장
- [ ] LRU 캐시 구현 — 캐시 크기를 제한하지 않으면 `CachingImageProxy`가 메모리를 무한정 소비할 수 있어 오래된 항목을 밀어낼 정책이 필요하다.
- [ ] 비동기 프록시 — 호출 스레드를 블로킹하면 원격 호출 지연이 그대로 클라이언트 응답 시간에 더해지므로 비동기 처리로 분리할 필요가 있다.
- [ ] 프록시 체이닝 — 캐싱과 보안 검사를 동시에 적용하려면 여러 Proxy를 겹쳐 감싸야 하며, 이때 감싸는 순서가 동작 순서를 결정한다.
- [ ] 메트릭 수집 — 프록시 계층에서 호출 횟수와 실패율을 집계해야 어떤 유형의 오버헤드가 실제로 문제인지 데이터로 판단할 수 있다.

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

## 선택 기준과 오버헤드 트레이드오프

네 가지 Proxy 유형 중 무엇을 선택할지는 "무엇을 지연시키거나 통제하고 싶은가"로 결정됩니다. 객체 생성 비용 자체가 문제라면 Virtual Proxy, 호출 주체의 권한이 문제라면 Protection Proxy, 물리적 위치가 문제라면 Remote Proxy, 동일 연산의 반복 호출이 문제라면 Caching Proxy가 대상입니다. 여러 문제가 겹치면(예: 원격 호출 결과를 캐싱하고 싶다) 프록시를 체이닝해서 조합할 수 있지만, 체이닝이 길어질수록 각 계층이 어디서 예외를 던지는지 추적하기 어려워지므로 실무에서는 꼭 필요한 조합만 남기는 것이 안전합니다.

오버헤드 트레이드오프도 유형마다 다릅니다. `ImageProxy`의 지연 로딩은 최초 접근 시점의 지연을 감수하는 대신 불필요한 로딩을 통째로 없애므로 대체로 이득이 명확합니다. 반면 `SecurityFileProxy`의 권한 검사나 `LoggingInvocationHandler`의 리플렉션 기반 호출은 모든 호출마다 고정 비용이 붙습니다. I/O가 지배적인 작업(파일, 네트워크, DB)에서는 이 고정 비용이 상대적으로 무시할 수준이지만, 초당 수백만 번 호출되는 순수 연산 경로에 동적 프록시를 무분별하게 씌우면 그 오버헤드가 누적되어 눈에 띄는 성능 저하로 이어질 수 있으므로, 적용 전에 대상 경로의 호출 빈도를 먼저 확인해야 합니다.

---

**핵심 포인트**: Proxy 패턴은 다양한 형태로 진화하여 현대 소프트웨어의 핵심 인프라가 되었습니다. 지연 로딩, 보안, 캐싱, 모니터링 등 횡단 관심사를 우아하게 처리하는 강력한 도구입니다. 