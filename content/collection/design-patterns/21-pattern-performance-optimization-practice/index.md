---
draft: true
collection_order: 211
title: "[Design Patterns] 패턴 성능 최적화 실습 - 효율적인 설계와 구현"
description: "디자인 패턴의 성능 특성을 분석하고 최적화하는 실습입니다. 객체 풀링, 지연 로딩, 캐싱, 플라이웨이트 등의 최적화 기법을 적용하여 패턴의 장점은 유지하면서 성능 오버헤드를 최소화하는 고급 구현 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-21T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Performance Optimization
- Pattern Implementation
- Practice
- Efficiency
tags:
- Performance Optimization Practice
- Object Pooling
- Lazy Loading
- Caching Strategies
- Memory Management
- Flyweight Optimization
- Benchmarking
- Profiling
- JVM Performance
- GC Optimization
- Pattern Efficiency
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Software Architecture
- Performance Tuning
- 성능 최적화 실습
- 객체 풀링
- 지연 로딩
- 캐싱 전략
- 메모리 관리
- 플라이웨이트 최적화
- 벤치마킹
- 프로파일링
- JVM 성능
- GC 최적화
- 패턴 효율성
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 소프트웨어 아키텍처
- 성능 튜닝
---

이 실습에서는 성능 벤치마크 작성, 메모리 효율적인 패턴 구현, JIT 최적화 분석을 직접 수행합니다.

## 실습 목표

1. 성능 벤치마크 작성 및 측정
2. 메모리 효율적인 패턴 구현
3. JIT 최적화와 패턴의 상관관계 분석

## 과제 1: 성능 벤치마크 작성

### Factory Method vs Direct Instantiation
```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@State(Scope.Benchmark)
public class CreationPatternBenchmark {
    
    @Benchmark
    public Object directInstantiation() {
        return new ConcreteProduct();
    }
    
    @Benchmark
    public Object factoryMethod() {
        return ProductFactory.createProduct("concrete");
    }
    
    @Benchmark
    public Object abstractFactory() {
        AbstractFactory factory = new ConcreteFactory();
        return factory.createProduct();
    }
}

// TODO: 다음 팩토리들을 구현하세요
class ProductFactory {
    public static Product createProduct(String type) {
        // TODO: 구현
        return null;
    }
}

abstract class AbstractFactory {
    abstract Product createProduct();
}

class ConcreteFactory extends AbstractFactory {
    @Override
    Product createProduct() {
        // TODO: 구현
        return null;
    }
}
```

### Decorator Chain vs Conditional Logic
```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS) 
public class DecoratorBenchmark {
    
    private String data = "test data";
    
    @Benchmark
    public String conditionalApproach() {
        String result = data;
        if (needsCompression()) {
            result = compress(result);
        }
        if (needsEncryption()) {
            result = encrypt(result);
        }
        if (needsLogging()) {
            log(result);
        }
        return result;
    }
    
    @Benchmark
    public String decoratorPattern() {
        DataProcessor processor = new LoggingDecorator(
            new EncryptionDecorator(
                new CompressionDecorator(
                    new BaseDataProcessor()
                )
            )
        );
        return processor.process(data);
    }
}

// TODO: Decorator 패턴 구현
interface DataProcessor {
    String process(String data);
}

class BaseDataProcessor implements DataProcessor {
    @Override
    public String process(String data) {
        return data;
    }
}

abstract class DataProcessorDecorator implements DataProcessor {
    protected DataProcessor processor;
    
    public DataProcessorDecorator(DataProcessor processor) {
        this.processor = processor;
    }
}

// TODO: 구체적인 Decorator들 구현
class CompressionDecorator extends DataProcessorDecorator {
    // TODO: 구현
}
```

### Observer vs Direct Call
```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
public class ObserverBenchmark {
    
    private Subject subject;
    private List<Observer> observers;
    
    @Setup
    public void setup() {
        subject = new ConcreteSubject();
        observers = new ArrayList<>();
        
        for (int i = 0; i < 1000; i++) {
            Observer observer = new ConcreteObserver();
            observers.add(observer);
            subject.attach(observer);
        }
    }
    
    @Benchmark
    public void observerPattern() {
        subject.notifyObservers();
    }
    
    @Benchmark
    public void directCall() {
        for (Observer observer : observers) {
            observer.update(subject);
        }
    }
}
```

## 과제 2: 메모리 효율적인 패턴 구현

### Flyweight 패턴으로 게임 캐릭터 시스템
```java
// 게임 캐릭터 Flyweight
public class CharacterType {
    private final String name;
    private final Sprite sprite;
    private final int health;
    private final int damage;
    
    public CharacterType(String name, Sprite sprite, int health, int damage) {
        this.name = name;
        this.sprite = sprite;
        this.health = health;
        this.damage = damage;
    }
    
    public void render(Graphics g, int x, int y, int level) {
        // TODO: 렌더링 로직 구현
        // 외재적 상태(x, y, level)를 사용하여 렌더링
    }
    
    public int getEffectiveDamage(int level) {
        // TODO: 레벨에 따른 데미지 계산
        return damage + (level * 2);
    }
}

// Factory
public class CharacterTypeFactory {
    private static final Map<String, CharacterType> characterTypes = new HashMap<>();
    
    public static CharacterType getCharacterType(String typeName) {
        // TODO: 캐시된 CharacterType 반환 또는 새로 생성
        return characterTypes.computeIfAbsent(typeName, name -> {
            // TODO: 캐릭터 타입별 기본 속성 설정
            return createCharacterType(name);
        });
    }
    
    private static CharacterType createCharacterType(String name) {
        // TODO: 구현
        return null;
    }
}

// 게임 캐릭터 (Context)
public class GameCharacter {
    private final CharacterType type;
    private int x, y;           // 외재적 상태
    private int level;          // 외재적 상태
    private int currentHealth;  // 외재적 상태
    
    public GameCharacter(String typeName, int x, int y) {
        this.type = CharacterTypeFactory.getCharacterType(typeName);
        this.x = x;
        this.y = y;
        this.level = 1;
        // TODO: 초기 체력 설정
    }
    
    public void render(Graphics g) {
        type.render(g, x, y, level);
    }
}
```

### Object Pool 패턴으로 네트워크 연결 관리
```java
public class ConnectionPool {
    private final Queue<Connection> availableConnections;
    private final Set<Connection> usedConnections;
    private final int maxSize;
    private final AtomicInteger currentSize;
    
    public ConnectionPool(int maxSize) {
        this.maxSize = maxSize;
        this.availableConnections = new ConcurrentLinkedQueue<>();
        this.usedConnections = ConcurrentHashMap.newKeySet();
        this.currentSize = new AtomicInteger(0);
    }
    
    public Connection getConnection() {
        // TODO: 연결 풀에서 연결 가져오기
        // 1. 사용 가능한 연결이 있으면 반환
        // 2. 없으면 새로 생성 (최대 크기 제한)
        // 3. 최대 크기 초과 시 대기 또는 예외
        return null;
    }
    
    public void returnConnection(Connection connection) {
        // TODO: 연결을 풀로 반환
        // 1. 사용 중 목록에서 제거
        // 2. 연결 상태 검증
        // 3. 정상이면 사용 가능 목록에 추가
    }
    
    // 성능 모니터링
    public ConnectionPoolStats getStats() {
        return new ConnectionPoolStats(
            availableConnections.size(),
            usedConnections.size(),
            maxSize
        );
    }
}

// 성능 측정
@Test
public void benchmarkConnectionPool() {
    ConnectionPool pool = new ConnectionPool(10);
    
    // 풀 사용 시
    long startTime = System.nanoTime();
    for (int i = 0; i < 10000; i++) {
        Connection conn = pool.getConnection();
        // 작업 수행
        doWork(conn);
        pool.returnConnection(conn);
    }
    long poolTime = System.nanoTime() - startTime;
    
    // 매번 새로 생성 시
    startTime = System.nanoTime();
    for (int i = 0; i < 10000; i++) {
        Connection conn = new Connection();
        doWork(conn);
        conn.close();
    }
    long directTime = System.nanoTime() - startTime;
    
    System.out.printf("Pool: %d ns, Direct: %d ns, Improvement: %.2f%%\n",
                      poolTime, directTime, 
                      ((double)(directTime - poolTime) / directTime) * 100);
}
```

### Proxy 패턴으로 이미지 지연 로딩
```java
public interface Image {
    void display();
    int getWidth();
    int getHeight();
}

public class RealImage implements Image {
    private final String filename;
    private BufferedImage image;
    
    public RealImage(String filename) {
        this.filename = filename;
        loadImage(); // 즉시 로딩
    }
    
    private void loadImage() {
        // TODO: 실제 이미지 파일 로딩 (시간 소요)
        try {
            Thread.sleep(100); // 로딩 시간 시뮬레이션
            // image = ImageIO.read(new File(filename));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    @Override
    public void display() {
        System.out.println("Displaying " + filename);
    }
}

public class ImageProxy implements Image {
    private final String filename;
    private RealImage realImage;
    private final int width, height; // 메타데이터만 미리 로딩
    
    public ImageProxy(String filename) {
        this.filename = filename;
        // TODO: 메타데이터만 로딩 (빠름)
        this.width = loadWidth(filename);
        this.height = loadHeight(filename);
    }
    
    @Override
    public void display() {
        if (realImage == null) {
            realImage = new RealImage(filename); // 지연 로딩
        }
        realImage.display();
    }
    
    @Override
    public int getWidth() {
        return width; // 즉시 반환 (실제 이미지 로딩 불필요)
    }
    
    @Override
    public int getHeight() {
        return height; // 즉시 반환
    }
}

// 성능 테스트
@Test
public void benchmarkImageProxy() {
    String[] filenames = {"img1.jpg", "img2.jpg", "img3.jpg"};
    
    // Proxy 사용 시
    long startTime = System.nanoTime();
    List<Image> proxyImages = new ArrayList<>();
    for (String filename : filenames) {
        proxyImages.add(new ImageProxy(filename));
    }
    // 크기 정보 조회 (실제 이미지 로딩 없음)
    for (Image image : proxyImages) {
        int size = image.getWidth() * image.getHeight();
    }
    long proxyTime = System.nanoTime() - startTime;
    
    // 직접 로딩 시
    startTime = System.nanoTime();
    List<Image> realImages = new ArrayList<>();
    for (String filename : filenames) {
        realImages.add(new RealImage(filename));
    }
    for (Image image : realImages) {
        int size = image.getWidth() * image.getHeight();
    }
    long realTime = System.nanoTime() - startTime;
    
    System.out.printf("Proxy: %d ns, Real: %d ns\n", proxyTime, realTime);
}
```

## 과제 3: JIT 최적화 분석

### 단형성 vs 다형성 호출 성능
```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
public class JITOptimizationBenchmark {
    
    private SortStrategy quickSort = new QuickSortStrategy();
    private SortStrategy[] strategies = {
        new QuickSortStrategy(),
        new MergeSortStrategy(),
        new HeapSortStrategy()
    };
    private int[] data = generateRandomArray(1000);
    
    @Benchmark
    public void monomorphicCall() {
        // 단형성 호출 - JIT이 인라이닝 가능
        for (int i = 0; i < 1000; i++) {
            quickSort.sort(data.clone());
        }
    }
    
    @Benchmark
    public void polymorphicCall() {
        // 다형성 호출 - JIT 최적화 제한적
        for (int i = 0; i < 1000; i++) {
            strategies[i % 3].sort(data.clone());
        }
    }
    
    @Benchmark
    public void megamorphicCall() {
        // Megamorphic 호출 - 가상 메서드 테이블 조회
        SortStrategy[] manyStrategies = {
            new QuickSortStrategy(),
            new MergeSortStrategy(), 
            new HeapSortStrategy(),
            new BubbleSortStrategy(),
            new InsertionSortStrategy()
        };
        
        for (int i = 0; i < 1000; i++) {
            manyStrategies[i % 5].sort(data.clone());
        }
    }
}

// TODO: Strategy 구현체들
interface SortStrategy {
    void sort(int[] array);
}

class QuickSortStrategy implements SortStrategy {
    @Override
    public void sort(int[] array) {
        // TODO: 퀵소트 구현
        Arrays.sort(array); // 임시 구현
    }
}
```

### 메서드 크기와 인라이닝
```java
public class InliningAnalysis {
    
    // 작은 메서드 - 인라이닝 가능
    public final int smallMethod(int a, int b) {
        return a + b;
    }
    
    // 큰 메서드 - 인라이닝 불가능
    public final int largeMethod(int a, int b) {
        int result = a + b;
        for (int i = 0; i < 100; i++) {
            result += i * a;
            result -= i * b;
            if (result > 1000) {
                result = result % 1000;
            }
        }
        return result;
    }
    
    @Benchmark
    public void benchmarkSmallMethod() {
        int sum = 0;
        for (int i = 0; i < 100000; i++) {
            sum += smallMethod(i, i + 1);
        }
    }
    
    @Benchmark
    public void benchmarkLargeMethod() {
        int sum = 0;
        for (int i = 0; i < 100000; i++) {
            sum += largeMethod(i, i + 1);
        }
    }
}
```

## 완성도 체크리스트

### 벤치마크 작성
- [ ] JMH를 사용한 마이크로 벤치마크
- [ ] 워밍업 단계 고려
- [ ] 통계적으로 유의미한 결과
- [ ] 메모리 사용량 측정

### 메모리 최적화
- [ ] Object Pool 구현 및 성능 측정
- [ ] Flyweight 패턴 메모리 절약 확인
- [ ] Lazy Loading 효과 측정
- [ ] GC 압박 분석

### JIT 최적화
- [ ] 단형성/다형성 호출 성능 차이 측정  
- [ ] 메서드 인라이닝 효과 분석
- [ ] 분기 예측 최적화 적용
- [ ] 핫스팟 식별

## 추가 도전 과제

1. **프로파일링 도구 활용**
   - JProfiler, VisualVM으로 성능 병목점 식별
   - 메모리 덤프 분석

2. **GC 튜닝과 패턴**
   - 세대별 GC와 객체 생명주기 분석
   - 패턴이 GC에 미치는 영향

3. **CPU 캐시 최적화**
   - 메모리 지역성 고려한 패턴 설계
   - False Sharing 회피

4. **병렬 처리 최적화**
   - Thread-safe 패턴 구현
   - Lock-free 자료구조 활용

---

**실습 팁**
- 측정 전 충분한 워밍업 수행
- 여러 번 측정하여 평균값 사용
- 실제 운영 환경에 가까운 조건에서 테스트
- 마이크로 벤치마크의 한계 인식하고 매크로 벤치마크 병행 