---
draft: true
---
# 13장: 동시성

## 강의 목표
- 동시성 프로그래밍의 필요성과 복잡성 이해
- 동시성 관련 미신과 오해 해소
- 안전하고 효율적인 동시성 코드 작성 기법 습득

## 내용 구성 전략

### 동시성이 필요한 이유?
**접근 방법**:
- 동시성의 필요성과 장점 분석
- 성능과 사용자 경험 개선 관점

**주요 내용**:
- 동시성은 결합(coupling)을 없애는 전략이다
- 즉, 무엇(what)과 언제(when)를 분리하는 전략이다
- 스레드가 하나인 프로그램에서 무엇과 언제는 서로 밀접하다
- 무엇과 언제를 분리하면 애플리케이션 구조와 효율이 극적으로 나아진다

**동시성의 장점**:
- **처리량(throughput) 개선**: 동시에 여러 작업을 처리할 수 있다
- **응답 시간(response time) 개선**: 사용자가 기다리는 시간을 줄일 수 있다
- **구조적 개선**: 무엇과 언제의 분리로 더 나은 구조를 만들 수 있다

**실제 예시**:
```java
// 동시성 없는 웹 서버 - 한 번에 하나의 요청만 처리
public class SimpleWebServer {
    public void run() {
        while (true) {
            Socket connection = serverSocket.accept();
            processRequest(connection); // 요청을 순차적으로 처리
        }
    }
    
    private void processRequest(Socket connection) {
        // 요청 처리 (시간이 오래 걸릴 수 있음)
        // 이 동안 다른 요청들은 대기해야 함
    }
}

// 동시성을 사용한 웹 서버 - 여러 요청을 동시에 처리
public class ConcurrentWebServer {
    public void run() {
        while (true) {
            Socket connection = serverSocket.accept();
            // 새로운 스레드에서 요청 처리
            executor.submit(() -> processRequest(connection));
        }
    }
    
    private void processRequest(Socket connection) {
        // 요청 처리 (다른 요청들과 병렬로 실행)
    }
}
```

### 미신과 오해
**접근 방법**:
- 동시성에 대한 잘못된 인식들 교정
- 현실적인 동시성 프로그래밍 인식

**주요 내용**:
동시성과 관련한 일반적인 미신과 오해를 살펴보자:

#### 미신들:
- **"동시성은 항상 성능을 높여준다"** 
  - 사실: 대기 시간이 아주 길어 여러 스레드가 프로세서를 공유할 수 있거나, 여러 프로세서가 동시에 처리할 독립적인 계산이 충분히 많은 경우에만 성능이 높아진다

- **"동시성을 구현해도 설계는 변하지 않는다"**
  - 사실: 단일 스레드 시스템과 다중 스레드 시스템은 설계가 판이하게 다르다

- **"웹 또는 EJB 컨테이너를 사용하면 동시성을 이해할 필요가 없다"**
  - 사실: 실제로는 컨테이너가 어떻게 동작하는지, 어떻게 동시 수정, 데드락 등과 같은 문제를 피할 수 있는지를 알아야만 한다

#### 타당한 생각들:
- **동시성은 다소 부하를 유발한다** - 성능 측면에서 부하가 있고, 코드도 더 복잡하다
- **동시성은 복잡하다** - 간단한 문제라도 동시성은 복잡하다
- **일반적으로 동시성 버그는 재현하기 어렵다** - 그래서 일회성 문제로 여겨 무시하기 쉽다
- **동시성을 구현하려면 흔히 근본적인 설계 전략을 재고해야 한다**

### 난관
**접근 방법**:
- 동시성 프로그래밍에서 직면하는 주요 문제들
- 실제 버그 사례를 통한 이해

**주요 내용**:
동시성을 구현하기 어려운 이유는 다음과 같다:

```java
// 동시성 문제 예시
public class SimpleCounter {
    private int count = 0;
    
    // 문제가 있는 메서드 - 스레드 안전하지 않음
    public void increment() {
        count++; // 이 한 줄은 실제로 여러 단계로 나뉜다:
                 // 1. count 값을 읽는다
                 // 2. count 값을 1 증가시킨다  
                 // 3. 증가된 값을 count에 저장한다
    }
    
    public int getCount() {
        return count;
    }
}

// 두 스레드가 동시에 increment()를 호출하면:
// Thread 1: count 값(0)을 읽는다
// Thread 2: count 값(0)을 읽는다  
// Thread 1: 0 + 1 = 1을 계산한다
// Thread 2: 0 + 1 = 1을 계산한다
// Thread 1: count에 1을 저장한다
// Thread 2: count에 1을 저장한다
// 결과: count = 1 (예상: 2)

// 올바른 구현 - 동기화 사용
public class ThreadSafeCounter {
    private int count = 0;
    
    public synchronized void increment() {
        count++;
    }
    
    public synchronized int getCount() {
        return count;
    }
}

// 또는 AtomicInteger 사용
public class AtomicCounter {
    private final AtomicInteger count = new AtomicInteger(0);
    
    public void increment() {
        count.incrementAndGet();
    }
    
    public int getCount() {
        return count.get();
    }
}
```

### 동시성 방어 원칙
**접근 방법**:
- 동시성 문제를 방지하기 위한 설계 원칙들
- 실용적인 가이드라인 제시

#### 단일 책임 원칙 (SRP)
**주요 내용**:
- **동시성 관련 코드는 다른 코드와 분리하라**
- 동시성 관련 코드는 독자적인 개발, 변경, 조율 주기가 있다
- 동시성 관련 코드에는 독자적인 난관이 있다
- 잘못 구현한 동시성 코드는 별의별 방식으로 실패한다

```java
// Bad: 동시성과 비즈니스 로직이 섞임
public class OrderProcessor {
    private final Object lock = new Object();
    private final List<Order> orders = new ArrayList<>();
    
    public void processOrder(Order order) {
        synchronized(lock) {
            // 동시성 관련 로직과 비즈니스 로직이 섞임
            validateOrder(order);
            calculateTotal(order);
            saveToDatabase(order);
            orders.add(order);
            sendConfirmationEmail(order);
        }
    }
}

// Good: 동시성과 비즈니스 로직 분리
public class OrderProcessor {
    private final OrderService orderService;
    private final ConcurrentOrderQueue orderQueue;
    
    public OrderProcessor(OrderService orderService, ConcurrentOrderQueue orderQueue) {
        this.orderService = orderService;
        this.orderQueue = orderQueue;
    }
    
    public void processOrder(Order order) {
        // 비즈니스 로직은 OrderService에 위임
        Order processedOrder = orderService.process(order);
        
        // 동시성 관련 로직은 ConcurrentOrderQueue에 위임
        orderQueue.add(processedOrder);
    }
}

// 동시성 전담 클래스
public class ConcurrentOrderQueue {
    private final BlockingQueue<Order> orders = new LinkedBlockingQueue<>();
    
    public void add(Order order) {
        try {
            orders.put(order);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public Order take() throws InterruptedException {
        return orders.take();
    }
}

// 순수 비즈니스 로직 클래스
public class OrderService {
    public Order process(Order order) {
        validateOrder(order);
        calculateTotal(order);
        saveToDatabase(order);
        sendConfirmationEmail(order);
        return order;
    }
}
```

#### 따름 정리: 자료 범위를 제한하라
**주요 내용**:
- 객체 하나를 공유하는 코드가 둘 이상이라면 해당 코드는 잠재적으로 간섭받을 가능성이 있다
- **공유 객체를 사용하는 코드 내 임계영역을 synchronized 키워드로 보호하라**
- 이런 임계영역의 수를 줄이는 기술이 중요하다

```java
// Bad: 넓은 범위의 공유 데이터
public class UserService {
    private final Map<String, User> users = new HashMap<>(); // 전역 공유
    
    public synchronized void addUser(User user) {
        users.put(user.getId(), user);
    }
    
    public synchronized User getUser(String id) {
        return users.get(id);
    }
    
    public synchronized void removeUser(String id) {
        users.remove(id);
    }
    
    // 문제: 모든 메서드가 같은 락을 공유함
}

// Good: 범위 제한과 전용 동시성 클래스 사용
public class UserService {
    private final ConcurrentUserRepository repository;
    
    public UserService() {
        this.repository = new ConcurrentUserRepository();
    }
    
    public void addUser(User user) {
        repository.save(user);
    }
    
    public User getUser(String id) {
        return repository.findById(id);
    }
    
    public void removeUser(String id) {
        repository.deleteById(id);
    }
}

// 동시성 전담 클래스
public class ConcurrentUserRepository {
    private final ConcurrentHashMap<String, User> users = new ConcurrentHashMap<>();
    
    public void save(User user) {
        users.put(user.getId(), user);
    }
    
    public User findById(String id) {
        return users.get(id);
    }
    
    public void deleteById(String id) {
        users.remove(id);
    }
}
```

#### 따름 정리: 자료 사본을 사용하라
**주요 내용**:
- 공유 자료를 줄이는 좋은 방법 중 하나는 처음부터 공유하지 않는 것이다
- 객체를 복사해 읽기 전용으로 사용하는 방법이 가능하다
- 복사 비용이 걱정될 수 있지만, 동기화 비용이 복사 비용보다 클 수도 있다

```java
// 자료 사본 활용 예시
public class ConfigurationManager {
    private volatile Configuration currentConfig;
    
    public void updateConfiguration(Configuration newConfig) {
        // 불변 객체를 사용하여 사본 생성
        this.currentConfig = new Configuration(newConfig);
    }
    
    public Configuration getConfiguration() {
        // 현재 설정의 사본을 반환
        return new Configuration(currentConfig);
    }
}

// 불변 Configuration 클래스
public final class Configuration {
    private final Map<String, String> properties;
    
    public Configuration(Map<String, String> properties) {
        this.properties = Collections.unmodifiableMap(new HashMap<>(properties));
    }
    
    public Configuration(Configuration other) {
        this.properties = other.properties; // 불변이므로 안전하게 공유
    }
    
    public String getProperty(String key) {
        return properties.get(key);
    }
}
```

#### 따름 정리: 스레드는 가능한 독립적으로 구현하라
**주요 내용**:
- 다른 스레드와 자료를 공유하지 않는 스레드를 구현하라
- 각 스레드는 클라이언트 요청 하나를 처리한다
- 모든 정보는 비공유 출처에서 가져오며 로컬 변수에 저장한다

```java
// 스레드 독립성 예시
public class RequestProcessor {
    private final ExecutorService executor = Executors.newFixedThreadPool(10);
    
    public void processRequest(HttpRequest request) {
        executor.submit(new RequestHandler(request));
    }
    
    // 각 요청을 독립적으로 처리하는 핸들러
    private static class RequestHandler implements Runnable {
        private final HttpRequest request;
        
        public RequestHandler(HttpRequest request) {
            this.request = request;
        }
        
        @Override
        public void run() {
            try {
                // 로컬 변수만 사용 - 스레드 안전
                String requestData = request.getBody();
                ProcessingResult result = processData(requestData);
                sendResponse(result);
            } catch (Exception e) {
                handleError(e);
            }
        }
        
        private ProcessingResult processData(String data) {
            // 공유 자원 없이 독립적으로 처리
            return new ProcessingResult(data);
        }
        
        private void sendResponse(ProcessingResult result) {
            // 응답 전송
        }
        
        private void handleError(Exception e) {
            // 에러 처리
        }
    }
}
```

### 라이브러리를 이해하라
**접근 방법**:
- Java 동시성 라이브러리의 주요 클래스들
- 각 클래스의 적절한 사용법

**주요 내용**:

#### 스레드 환경에 안전한 컬렉션
```java
// 스레드 안전한 컬렉션 사용
public class SafeCollectionExamples {
    // ConcurrentHashMap - 높은 동시성 성능
    private final Map<String, User> users = new ConcurrentHashMap<>();
    
    // CopyOnWriteArrayList - 읽기가 많고 쓰기가 적을 때
    private final List<String> eventLog = new CopyOnWriteArrayList<>();
    
    // BlockingQueue - 생산자-소비자 패턴
    private final BlockingQueue<Task> taskQueue = new LinkedBlockingQueue<>();
    
    public void addUser(String id, User user) {
        users.put(id, user);
    }
    
    public void logEvent(String event) {
        eventLog.add(event);
    }
    
    public void addTask(Task task) throws InterruptedException {
        taskQueue.put(task);
    }
    
    public Task getNextTask() throws InterruptedException {
        return taskQueue.take();
    }
}
```

#### Executor 프레임워크
```java
// Executor 사용 예시
public class TaskExecutorService {
    private final ExecutorService executor;
    
    public TaskExecutorService() {
        // 다양한 ExecutorService 타입
        this.executor = Executors.newFixedThreadPool(10);
        // this.executor = Executors.newCachedThreadPool();
        // this.executor = Executors.newSingleThreadExecutor();
    }
    
    public Future<String> submitTask(String data) {
        return executor.submit(() -> {
            // 작업 처리
            return processData(data);
        });
    }
    
    public void submitAsyncTask(String data) {
        executor.execute(() -> {
            processDataAsync(data);
        });
    }
    
    private String processData(String data) {
        // 데이터 처리 로직
        return "Processed: " + data;
    }
    
    private void processDataAsync(String data) {
        // 비동기 처리 로직
    }
    
    public void shutdown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

### 실행 모델을 이해하라
**접근 방법**:
- 주요 동시성 실행 모델들
- 각 모델의 장단점과 적용 사례

**주요 내용**:

#### 생산자-소비자 (Producer-Consumer)
```java
public class ProducerConsumerExample {
    private final BlockingQueue<String> queue = new LinkedBlockingQueue<>(10);
    
    // 생산자
    class Producer implements Runnable {
        @Override
        public void run() {
            try {
                for (int i = 0; i < 100; i++) {
                    String item = "Item-" + i;
                    queue.put(item); // 큐가 가득 차면 대기
                    System.out.println("Produced: " + item);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    // 소비자
    class Consumer implements Runnable {
        @Override
        public void run() {
            try {
                while (true) {
                    String item = queue.take(); // 큐가 비어있으면 대기
                    processItem(item);
                    System.out.println("Consumed: " + item);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        private void processItem(String item) {
            // 아이템 처리
        }
    }
}
```

#### 읽기-쓰기 (Readers-Writers)
```java
public class ReadersWritersExample {
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    private final Lock readLock = lock.readLock();
    private final Lock writeLock = lock.writeLock();
    private String data = "Initial Data";
    
    // 읽기 작업 - 여러 스레드가 동시에 수행 가능
    public String readData() {
        readLock.lock();
        try {
            return data;
        } finally {
            readLock.unlock();
        }
    }
    
    // 쓰기 작업 - 독점적으로 수행
    public void writeData(String newData) {
        writeLock.lock();
        try {
            this.data = newData;
        } finally {
            writeLock.unlock();
        }
    }
}
```

#### 철학자들의 저녁식사 (Dining Philosophers)
```java
public class DiningPhilosophers {
    private final int numPhilosophers = 5;
    private final Object[] forks = new Object[numPhilosophers];
    
    public DiningPhilosophers() {
        for (int i = 0; i < numPhilosophers; i++) {
            forks[i] = new Object();
        }
    }
    
    class Philosopher implements Runnable {
        private final int id;
        
        public Philosopher(int id) {
            this.id = id;
        }
        
        @Override
        public void run() {
            try {
                while (true) {
                    think();
                    eat();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        private void eat() throws InterruptedException {
            // 데드락 방지: 작은 번호 포크를 먼저 획득
            Object firstFork = forks[Math.min(id, (id + 1) % numPhilosophers)];
            Object secondFork = forks[Math.max(id, (id + 1) % numPhilosophers)];
            
            synchronized (firstFork) {
                synchronized (secondFork) {
                    System.out.println("Philosopher " + id + " is eating");
                    Thread.sleep(1000); // 식사 시간
                }
            }
        }
        
        private void think() throws InterruptedException {
            System.out.println("Philosopher " + id + " is thinking");
            Thread.sleep(1000); // 사고 시간
        }
    }
}
```

### 동기화하는 메서드 사이에 존재하는 의존성을 이해하라
**접근 방법**:
- 공유 클래스에서 여러 메서드 사용 시의 문제점
- 클라이언트 기반 잠금, 서버 기반 잠금, 어댑터 서버

**주요 내용**:
공유 클래스 하나에 동기화된 메서드가 여럿이라면 구현이 까다로워진다.

```java
// 문제가 있는 코드
public class IntegerIterator implements Iterator<Integer> {
    private Integer nextValue = 0;
    
    public synchronized boolean hasNext() {
        return nextValue < 100000;
    }
    
    public synchronized Integer next() {
        if (nextValue == 100000)
            throw new IteratorPastEndException();
        return ++nextValue;
    }
}

// 사용 코드 - 문제 발생 가능
IntegerIterator iterator = new IntegerIterator();
while (iterator.hasNext()) {
    int nextValue = iterator.next(); // hasNext()와 next() 사이에 다른 스레드가 개입 가능
}

// 해결책 1: 클라이언트 기반 잠금
public class ClientLockingExample {
    private final IntegerIterator iterator = new IntegerIterator();
    private final Object lock = new Object();
    
    public void useIterator() {
        synchronized (lock) {
            while (iterator.hasNext()) {
                int nextValue = iterator.next();
                // 처리
            }
        }
    }
}

// 해결책 2: 서버 기반 잠금
public class ServerBasedIterator implements Iterator<Integer> {
    private Integer nextValue = 0;
    
    public synchronized Integer nextIfAvailable() {
        if (nextValue < 100000) {
            return ++nextValue;
        }
        return null;
    }
}

// 해결책 3: 어댑터 서버
public class ThreadSafeIteratorAdapter {
    private final IntegerIterator iterator;
    
    public ThreadSafeIteratorAdapter(IntegerIterator iterator) {
        this.iterator = iterator;
    }
    
    public synchronized Integer nextIfAvailable() {
        if (iterator.hasNext()) {
            return iterator.next();
        }
        return null;
    }
}
```

### 동기화하는 부분을 작게 만들어라
**접근 방법**:
- 동기화 영역 최소화의 중요성
- 성능과 안전성의 균형

**주요 내용**:
- synchronized 키워드를 사용하면 락을 설정한다
- 같은 락으로 감싼 모든 코드 영역은 한 번에 한 스레드만 실행 가능하다
- 락은 스레드를 지연시키고 부하를 가중시킨다
- 그러므로 synchronized 문을 가능한 작게 만들어라

```java
// Bad: 큰 동기화 영역
public class BadSynchronization {
    private final List<String> items = new ArrayList<>();
    
    public synchronized void processItems() {
        // 긴 전처리 작업 (동기화 불필요)
        String preprocessedData = performLongPreprocessing();
        
        // 실제 공유 자원 접근
        items.add(preprocessedData);
        
        // 긴 후처리 작업 (동기화 불필요)
        performLongPostprocessing(preprocessedData);
    }
    
    private String performLongPreprocessing() {
        // 시간이 오래 걸리는 작업
        return "processed";
    }
    
    private void performLongPostprocessing(String data) {
        // 시간이 오래 걸리는 작업
    }
}

// Good: 작은 동기화 영역
public class GoodSynchronization {
    private final List<String> items = new ArrayList<>();
    
    public void processItems() {
        // 전처리 - 동기화 밖에서 수행
        String preprocessedData = performLongPreprocessing();
        
        // 최소한의 동기화 영역
        synchronized (this) {
            items.add(preprocessedData);
        }
        
        // 후처리 - 동기화 밖에서 수행
        performLongPostprocessing(preprocessedData);
    }
    
    private String performLongPreprocessing() {
        return "processed";
    }
    
    private void performLongPostprocessing(String data) {
        // 후처리 로직
    }
}
```

### 올바른 종료 코드는 구현하기 어렵다
**접근 방법**:
- 동시성 애플리케이션의 깔끔한 종료 방법
- 데드락이나 리소스 누수 방지

**주요 내용**:
영구적으로 돌아가는 시스템을 구현하는 편이 종료 코드를 개발하는 편보다 쉽다.

```java
// 올바른 종료 코드 예시
public class GracefulShutdownExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(10);
    private volatile boolean shutdownRequested = false;
    private final CountDownLatch shutdownLatch = new CountDownLatch(1);
    
    public void start() {
        // 작업 스레드들 시작
        for (int i = 0; i < 10; i++) {
            executor.submit(this::workerLoop);
        }
    }
    
    private void workerLoop() {
        try {
            while (!shutdownRequested) {
                // 작업 수행
                doWork();
                
                // 인터럽트 체크
                if (Thread.currentThread().isInterrupted()) {
                    break;
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            // 정리 작업
            cleanup();
        }
    }
    
    public void shutdown() {
        shutdownRequested = true;
        
        // 실행 중인 태스크 완료 대기
        executor.shutdown();
        
        try {
            // 60초 대기 후 강제 종료
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
                
                // 인터럽트된 태스크 대기
                if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                    System.err.println("Executor did not terminate");
                }
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        } finally {
            shutdownLatch.countDown();
        }
    }
    
    public void awaitShutdown() throws InterruptedException {
        shutdownLatch.await();
    }
    
    private void doWork() throws InterruptedException {
        // 실제 작업
        Thread.sleep(100);
    }
    
    private void cleanup() {
        // 리소스 정리
    }
}
```

### 스레드 코드 테스트하기
**접근 방법**:
- 동시성 코드의 테스트 전략
- 버그 재현과 검증 방법

**주요 내용**:
- 말이 안 되는 실패는 잠정적인 스레드 문제로 취급하라
- 다중 스레드를 고려하지 않은 순차 코드부터 제대로 돌게 만들자
- 다중 스레드를 쓰는 코드 부분을 다양한 환경에 쉽게 끼워 넣을 수 있게 스레드 코드를 구현하라
- 다중 스레드를 쓰는 코드 부분을 상황에 맞춰 조율할 수 있게 작성하라
- 프로세서 수보다 많은 스레드를 돌려보라
- 다른 플랫폼에서 돌려보라
- 코드에 보조 코드(instrument)를 넣어 돌려라. 강제로 실패를 일으키게 해보라

```java
// 동시성 테스트 예시
public class ConcurrencyTest {
    
    @Test
    public void testConcurrentCounter() throws InterruptedException {
        final int numThreads = 10;
        final int incrementsPerThread = 1000;
        final AtomicCounter counter = new AtomicCounter();
        final ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        final CountDownLatch startLatch = new CountDownLatch(1);
        final CountDownLatch endLatch = new CountDownLatch(numThreads);
        
        // 여러 스레드에서 동시에 카운터 증가
        for (int i = 0; i < numThreads; i++) {
            executor.submit(() -> {
                try {
                    startLatch.await(); // 모든 스레드가 동시에 시작
                    for (int j = 0; j < incrementsPerThread; j++) {
                        counter.increment();
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    endLatch.countDown();
                }
            });
        }
        
        startLatch.countDown(); // 모든 스레드 시작
        endLatch.await(); // 모든 스레드 완료 대기
        
        assertEquals(numThreads * incrementsPerThread, counter.getCount());
        
        executor.shutdown();
    }
    
    @Test
    public void testProducerConsumer() throws InterruptedException {
        final BlockingQueue<String> queue = new LinkedBlockingQueue<>(10);
        final int numItems = 100;
        final CountDownLatch producerLatch = new CountDownLatch(1);
        final CountDownLatch consumerLatch = new CountDownLatch(1);
        final AtomicInteger consumedCount = new AtomicInteger(0);
        
        // 생산자 스레드
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < numItems; i++) {
                    queue.put("Item-" + i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                producerLatch.countDown();
            }
        });
        
        // 소비자 스레드
        Thread consumer = new Thread(() -> {
            try {
                while (consumedCount.get() < numItems) {
                    String item = queue.poll(1, TimeUnit.SECONDS);
                    if (item != null) {
                        consumedCount.incrementAndGet();
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                consumerLatch.countDown();
            }
        });
        
        producer.start();
        consumer.start();
        
        producerLatch.await(5, TimeUnit.SECONDS);
        consumerLatch.await(5, TimeUnit.SECONDS);
        
        assertEquals(numItems, consumedCount.get());
    }
}
```

## 강의 진행 방식
1. **도입 (10분)**: 동시성 필요성과 복잡성 논의
2. **이론 (30분)**: 동시성 원칙과 패턴 설명
3. **실습 (35분)**: 동시성 문제 해결 실습
4. **테스트 (15분)**: 동시성 코드 테스트 방법 실습

## 실습 과제
1. **동시성 버그 수정**: 스레드 안전하지 않은 코드를 안전하게 수정
2. **생산자-소비자 구현**: BlockingQueue를 사용한 생산자-소비자 패턴 구현
3. **동시성 테스트**: 멀티스레드 환경에서의 테스트 케이스 작성

## 평가 기준
- 동시성 문제 식별 및 해결 능력 (40%)
- 적절한 동시성 도구 선택 및 사용 (35%)
- 동시성 코드 테스트 능력 (25%)

## 동시성 체크리스트
- [ ] 동시성 관련 코드가 다른 코드와 분리되었는가?
- [ ] 공유 데이터의 범위가 최소화되었는가?
- [ ] 적절한 동시성 컬렉션을 사용했는가?
- [ ] 동기화 영역이 최소한으로 유지되었는가?
- [ ] 데드락 가능성을 고려했는가?
- [ ] 스레드 안전성이 보장되는가?
- [ ] 올바른 종료 코드가 구현되었는가?
- [ ] 동시성 코드에 대한 적절한 테스트가 있는가?

## 추가 자료
- "Java Concurrency in Practice" - Brian Goetz
- "Concurrent Programming in Java" - Doug Lea
- Java 공식 동시성 튜토리얼
- "The Art of Multiprocessor Programming" - Maurice Herlihy
- 동시성 패턴과 베스트 프랙티스 가이드
</rewritten_file> 