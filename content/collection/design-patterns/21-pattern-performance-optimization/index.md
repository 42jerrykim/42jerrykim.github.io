---
draft: true
collection_order: 210
title: "[Design Patterns] 21. 패턴의 성능 분석과 최적화"
slug: "pattern-performance-optimization"
description: "디자인 패턴의 성능 특성을 정량적으로 분석하고 최적화하는 전문가 기법을 학습합니다. 메모리 사용량, CPU 오버헤드, JIT 컴파일러 최적화, 캐시 친화성 등을 고려한 고성능 패턴 구현 방법과 성능 측정, 프로파일링 기법을 통해 실무에서 성능과 설계의 균형을 찾는 방법을 탐구합니다."
image: "wordcloud.png"
date: 2024-12-21T10:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Performance Optimization
- Pattern Analysis
- System Performance
tags:
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Performance(성능)
- Optimization(최적화)
- Memory(메모리)
- CPU(Central Processing Unit)
- Cache
- Benchmark
- Profiling(프로파일링)
- Compiler(컴파일러)
- Singleton
- Factory
- Observer
- Strategy
- Decorator
- Proxy
- Behavioral-Pattern
- Creational-Pattern
- Structural-Pattern
- OOP(객체지향)
- Java
- Best-Practices
- Implementation(구현)
- Code-Quality(코드품질)
- Concurrency(동시성)
- Thread
- Deep-Dive
- Advanced
- Comparison(비교)
---

각 디자인 패턴의 성능 특성을 정량적으로 분석하고 최적화 기법을 탐구합니다. 성능과 설계의 균형을 찾는 실무적 접근법을 학습합니다.

## 서론: 성능 우수한 패턴 설계

> *"좋은 설계는 아름다움과 성능을 동시에 추구한다. 패턴은 우아함을 제공하지만, 성능도 고려해야 한다."*

디자인 패턴은 **코드의 구조와 유지보수성**을 향상시키지만, 때로는 **성능 오버헤드**를 가져올 수 있습니다. 이 글에서는 각 패턴의 성능 특성을 정량적으로 분석하고, 실무에서 성능과 설계의 균형을 찾는 방법을 탐구합니다.

### 성능 최적화의 핵심 관점
- **메모리 사용량**: 객체 생성 비용과 메모리 점유율
- **CPU 사용량**: 메서드 호출 오버헤드와 연산 복잡도
- **캐시 친화성**: 메모리 지역성과 캐시 히트율
- **JIT 컴파일러 최적화**: 핫스팟과 인라이닝 가능성

## 패턴별 성능 분석

> **caveat**: 아래 수치(ns, %)는 특정 환경(JDK 17, JIT 워밍업 10,000회, 특정 CPU)에서 측정된 예시 수치이며, JDK 버전·CPU 모델·JVM 플래그·워밍업 여부에 따라 크게 달라질 수 있습니다. 실무에서는 반드시 대상 환경에서 JMH로 직접 재측정해야 하며, 이 수치를 그대로 실무 판단 근거로 사용하지 마세요.

### 생성 패턴 성능 분석

Factory Method나 Abstract Factory는 객체 생성 시점에 간접 호출(가상 메서드 디스패치, 조건 분기)을 한 단계 더 거치므로 직접 `new`보다 느립니다. 하지만 이 오버헤드는 대개 수십~수백 나노초 수준이라, I/O나 DB 호출이 섞인 실제 요청 처리 경로에서는 무시할 수 있는 크기인 경우가 많습니다. 아래 벤치마크는 이 오버헤드가 실제로 "얼마나 작은지"를 보여주기 위한 예시입니다.

이 절과 다음 절의 벤치마크 코드는 `Product`, `DatabaseConnection`, `SortStrategy` 등 프로젝트마다 다르게 구현될 타입을 전제로 합니다. 아래는 벤치마크가 참조하는 최소 스텁으로, 실제 프로젝트에서는 도메인에 맞는 완전한 구현으로 대체해야 합니다.

```java
// 벤치마크가 공통으로 참조하는 최소 타입 스텁
interface Product {}
class ConcreteProduct implements Product {}
class ProductFactory {
    static Product create(String type) { return new ConcreteProduct(); }
}
interface AbstractFactory {
    Product createProduct();
}
class FactoryProducer {
    static AbstractFactory getFactory(String osName) {
        return ConcreteProduct::new;
    }
}
class DatabaseConnection {
    private static final DatabaseConnection INSTANCE = new DatabaseConnection("default");
    DatabaseConnection(String url) { /* 커넥션 초기화 */ }
    static DatabaseConnection getInstance() { return INSTANCE; }
}
interface SortStrategy {
    void sort(int[] data);
}
class QuickSortStrategy implements SortStrategy {
    public void sort(int[] data) { Arrays.sort(data); }
}
class MergeSortStrategy implements SortStrategy {
    public void sort(int[] data) { Arrays.sort(data); }
}
class HeapSortStrategy implements SortStrategy {
    public void sort(int[] data) { Arrays.sort(data); }
}
class BubbleSortStrategy implements SortStrategy {
    public void sort(int[] data) { Arrays.sort(data); }
}
class InsertionSortStrategy implements SortStrategy {
    public void sort(int[] data) { Arrays.sort(data); }
}
```

```java
// Factory Method vs Direct Instantiation 성능 비교
public class CreationPatternBenchmark {
    // 생성 패턴 4종의 상대적 오버헤드를 비교하는 JMH 벤치마크.
    // 절대 수치보다 "직접 생성 대비 몇 배"라는 상대 비율에 주목해서 읽습니다.

    // 직접 생성 (베이스라인) - 예시 환경 기준 ~50ns
    @Benchmark
    public Product createDirect() {
        return new ConcreteProduct();
    }
    
    // Factory Method - 예시 환경 기준 ~120ns (+140% 오버헤드)
    @Benchmark
    public Product createViaFactory() {
        return ProductFactory.create("concrete");
    }
    
    // Abstract Factory - 예시 환경 기준 ~200ns (+300% 오버헤드)
    @Benchmark
    public Product createViaAbstractFactory() {
        AbstractFactory factory = FactoryProducer.getFactory("Windows");
        return factory.createProduct();
    }
    
    // Singleton - 멀티스레드 환경, 예시 환경 기준 ~15ns (synchronized 버전: ~80ns)
    @Benchmark
    public DatabaseConnection getSingleton() {
        return DatabaseConnection.getInstance();
    }
}

// 메모리 사용량 측정
public class MemoryUsageAnalysis {
    public void measureMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        
        // 직접 생성 vs Singleton 메모리 비교
        long beforeMemory = runtime.totalMemory() - runtime.freeMemory();
        
        // 1000개 객체 직접 생성
        List<DatabaseConnection> connections = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            connections.add(new DatabaseConnection("url" + i));
        }
        
        long directCreationMemory = runtime.totalMemory() - runtime.freeMemory() - beforeMemory;
        System.out.println("Direct creation: " + directCreationMemory + " bytes");
        
        // Singleton 사용
        connections.clear();
        DatabaseConnection singleton = DatabaseConnection.getInstance();
        for (int i = 0; i < 1000; i++) {
            connections.add(singleton); // 참조만 저장
        }
        
        long singletonMemory = runtime.totalMemory() - runtime.freeMemory() - beforeMemory;
        System.out.println("Singleton: " + singletonMemory + " bytes");
        // 예시 환경 기준 결과: Singleton이 약 95% 메모리 절약 (참조 1000개 vs 인스턴스 1000개)
        // 실제 절약률은 객체 크기와 참조 크기(8바이트, compressed oops 기준)의 비율에 따라 달라집니다.
    }
}
```

### 구조 패턴 성능 분석

구조 패턴은 대부분 "메모리를 줄이는 대신 조회 비용을 더하는(Flyweight, Proxy)" 또는 "호출 하나를 여러 단계로 나누는 대신 조합 유연성을 얻는(Decorator)" 트레이드오프를 가집니다. 아래 벤치마크는 이 트레이드오프가 실제로 어느 방향으로, 얼마나 나타나는지를 보여주는 예시 측정치입니다.

```java
// Flyweight 패턴의 메모리 효율성
public class FlyweightPerformanceAnalysis {
    
    // Flyweight 없이 구현 - 예시 환경 기준 메모리 사용량 ~400KB
    @Benchmark
    public void withoutFlyweight() {
        List<Character> characters = new ArrayList<>();
        for (int i = 0; i < 10000; i++) {
            characters.add(new Character('A', "Arial", 12, Color.BLACK));
        }
    }
    
    // Flyweight 패턴 적용 - 예시 환경 기준 메모리 사용량 ~80KB (약 80% 절약)
    @Benchmark
    public void withFlyweight() {
        CharacterFlyweightFactory factory = new CharacterFlyweightFactory();
        List<CharacterContext> characters = new ArrayList<>();
        
        for (int i = 0; i < 10000; i++) {
            CharacterFlyweight flyweight = factory.getFlyweight('A', "Arial", 12, Color.BLACK);
            characters.add(new CharacterContext(flyweight, i, i)); // 위치만 개별 저장
        }
    }
    
    // Proxy 패턴의 지연 로딩 효과 (예시 수치, 실제 I/O 지연시간에 따라 달라짐)
    @Benchmark
    public void proxyLazyLoading() {
        ImageProxy proxy = new ImageProxy("large_image.jpg");
        
        // 이미지 정보만 필요한 경우 - 예시 환경 기준 ~5ns (실제 로딩 없음)
        String info = proxy.getInfo();
        
        // 실제 이미지가 필요한 경우 - 예시 환경 기준 최초 ~1000ms, 캐시 후 ~50ms
        proxy.display();
        proxy.display();
    }
}

// Decorator 패턴의 체인 성능
public class DecoratorPerformanceAnalysis {
    
    // 짧은 체인(2단계) - 예시 환경 기준 ~100ns
    @Benchmark
    public void shortDecoratorChain() {
        TextProcessor processor = new LoggingDecorator(
            new EncryptionDecorator(
                new PlainTextProcessor()
            )
        );
        processor.process("Hello");
    }
    
    // 긴 체인(5단계) - 예시 환경 기준 ~500ns (짧은 체인 대비 약 5배)
    @Benchmark
    public void longDecoratorChain() {
        TextProcessor processor = new LoggingDecorator(
            new CompressionDecorator(
                new EncryptionDecorator(
                    new ValidationDecorator(
                        new FormattingDecorator(
                            new PlainTextProcessor()
                        )
                    )
                )
            )
        );
        processor.process("Hello");
    }
}
```

### 행동 패턴 성능 분석

Observer의 통지 비용은 리스너 수에 선형으로 비례하므로, 리스너가 적을 때는 문제되지 않다가 리스너가 늘어나면서 병목이 되는 경우가 흔합니다. Strategy는 if-else 대비 오버헤드가 있지만 그 크기는 분기 예측 성공률과 JIT 인라이닝 여부에 따라 20~25% 수준으로 작게 나타나는 경우가 많습니다. 아래는 이런 경향을 보여주는 예시 벤치마크입니다.

```java
// Observer 패턴의 알림 성능
public class ObserverPerformanceAnalysis {
    
    // 리스너 10개 - 예시 환경 기준 ~50ns
    @Benchmark
    public void fewObservers() {
        Subject subject = new ConcreteSubject();
        for (int i = 0; i < 10; i++) {
            subject.attach(new ConcreteObserver());
        }
        subject.notifyObservers();
    }
    
    // 리스너 1000개 - 예시 환경 기준 ~5000ns (리스너 수에 선형 비례)
    @Benchmark
    public void manyObservers() {
        Subject subject = new ConcreteSubject();
        for (int i = 0; i < 1000; i++) {
            subject.attach(new ConcreteObserver());
        }
        subject.notifyObservers();
    }
    
    // 비동기 Observer 패턴 - 예시 환경 기준 ~100ns (메인 스레드는 큐잉만 하고 빠르게 반환)
    @Benchmark
    public void asyncObservers() {
        AsyncSubject subject = new AsyncSubject();
        for (int i = 0; i < 1000; i++) {
            subject.attach(new AsyncObserver());
        }
        subject.notifyObservers();
    }
}

// Strategy 패턴 vs if-else 성능
public class StrategyPerformanceAnalysis {
    
    // if-else 직접 분기 - 예시 환경 기준 ~20ns (분기 예측 성공 시)
    @Benchmark
    public void ifElseApproach() {
        String type = "quick";
        if ("quick".equals(type)) {
            // QuickSort 로직
        } else if ("merge".equals(type)) {
            // MergeSort 로직
        } else if ("heap".equals(type)) {
            // HeapSort 로직
        }
    }
    
    // Strategy 패턴 - 예시 환경 기준 ~25ns (+25% 오버헤드, 대신 확장성 확보)
    @Benchmark
    public void strategyPattern() {
        SortStrategy strategy = new QuickSortStrategy();
        strategy.sort(data);
    }
    
    // 함수형 접근법 - 예시 환경 기준 ~22ns (JIT 최적화 후)
    @Benchmark
    public void functionalApproach() {
        Function<int[], Void> sortFunction = this::quickSort;
        sortFunction.apply(data);
    }
}
```

## JIT 컴파일러와 패턴 최적화

HotSpot JIT 컴파일러는 호출 지점(call site)에서 실제로 몇 개의 구체 타입이 나타나는지를 추적해 인라이닝 여부를 결정합니다. 한 지점에서 타입이 1개(monomorphic)면 적극적으로 인라이닝하고, 2개(bipolymorphic)까지는 제한적으로, 3개 이상(megamorphic)이 되면 인라이닝을 포기하고 가상 메서드 테이블을 조회합니다. Strategy나 Observer처럼 다형성을 활용하는 패턴은 이 megamorphic 상황을 유발하기 쉬우므로, 핫 패스에서는 다형성의 폭을 의도적으로 좁히는 설계가 필요할 수 있습니다.

### 가상 메서드 호출과 인라이닝

```java
// 인라이닝 가능성을 고려한 패턴 설계
public class JITOptimizationAnalysis {
    
    // 단형성 호출 (Monomorphic) - 인라이닝 가능
    @Benchmark
    public void monomorphicCall() {
        SortStrategy strategy = new QuickSortStrategy();
        for (int i = 0; i < 10000; i++) {
            strategy.sort(data); // JIT이 인라이닝 가능
        }
    }
    
    // 다형성 호출 (Polymorphic) - 인라이닝 어려움
    @Benchmark
    public void polymorphicCall() {
        SortStrategy[] strategies = {
            new QuickSortStrategy(),
            new MergeSortStrategy(),
            new HeapSortStrategy()
        };
        
        for (int i = 0; i < 10000; i++) {
            strategies[i % 3].sort(data); // JIT 최적화 제한
        }
    }
    
    // Megamorphic 호출 - 인라이닝 불가능
    @Benchmark
    public void megamorphicCall() {
        SortStrategy[] strategies = {
            new QuickSortStrategy(),
            new MergeSortStrategy(),
            new HeapSortStrategy(),
            new BubbleSortStrategy(),
            new InsertionSortStrategy()
        };
        
        for (int i = 0; i < 10000; i++) {
            strategies[i % 5].sort(data); // 가상 메서드 테이블 조회
        }
    }
}

// JIT 친화적인 패턴 설계
public abstract class JITFriendlyPattern {
    
    // final 메서드로 인라이닝 보장
    public final void processTemplate() {
        step1(); // 인라이닝 가능
        step2(); // 인라이닝 가능
        step3(); // 인라이닝 가능
    }
    
    protected abstract void step1();
    protected abstract void step2();
    protected abstract void step3();
    
    // 핫스팟 메서드는 작게 유지 (< 35 바이트코드)
    public final int calculateHash() {
        return Objects.hash(field1, field2); // 인라이닝 가능
    }
}
```

### 분기 예측과 패턴 최적화

```java
// 분기 예측 친화적인 Chain of Responsibility
public class OptimizedChainOfResponsibility {
    
    // 처리 빈도에 따른 핸들러 순서 최적화
    public void optimizeHandlerOrder() {
        // 통계 기반 핸들러 순서 조정
        // 가장 빈번한 핸들러를 앞에 배치
        List<Handler> handlers = Arrays.asList(
            new FrequentHandler(),    // 70% 처리
            new ModerateHandler(),    // 20% 처리  
            new RareHandler()         // 10% 처리
        );
        
        // 이렇게 하면 분기 예측 성공률이 높아짐
    }
    
    // 분기 예측을 고려한 Handler 구현
    public abstract class Handler {
        protected Handler nextHandler;
        
        public final void handleRequest(Request request) {
            // 가장 일반적인 케이스를 먼저 체크
            if (canHandleFast(request)) { // 80% 확률로 true
                doHandle(request);
                return; // 예측 성공
            }
            
            if (nextHandler != null) { // 20% 확률
                nextHandler.handleRequest(request); // 예측 실패
            }
        }
        
        protected abstract boolean canHandleFast(Request request);
        protected abstract void doHandle(Request request);
    }
}
```

## 메모리 최적화 전략

Object Pool은 "생성 비용이 비싼 객체(스레드, DB 커넥션, 대형 버퍼)"를 재사용해 할당·GC 비용을 줄이는 기법입니다. 다만 객체 생성이 저렴한 경우(단순 POJO 등)에는 풀 관리 오버헤드(동기화, 상태 추적)가 오히려 순수 생성보다 손해일 수 있으므로, "생성 비용 >> 풀 관리 비용"인 경우에만 적용해야 합니다.

### Object Pool과 Factory 패턴 결합

```java
public class OptimizedObjectFactory {
    private final Queue<ExpensiveObject> pool = new ConcurrentLinkedQueue<>();
    private final AtomicInteger poolSize = new AtomicInteger(0);
    private static final int MAX_POOL_SIZE = 100;
    
    public ExpensiveObject createObject() {
        ExpensiveObject obj = pool.poll();
        if (obj != null) {
            poolSize.decrementAndGet();
            obj.reset(); // 객체 재사용을 위한 초기화
            return obj; // 풀에서 재사용 (0ns 할당 시간)
        }
        
        return new ExpensiveObject(); // 새 객체 생성 (~1000ns)
    }
    
    public void returnObject(ExpensiveObject obj) {
        if (poolSize.get() < MAX_POOL_SIZE) {
            obj.cleanup(); // 정리 작업
            pool.offer(obj);
            poolSize.incrementAndGet();
        }
        // 풀이 가득 찬 경우 GC에 맡김
    }
    
    // 예시 환경 기준 성능 측정 결과 (실제 값은 ExpensiveObject의 생성 비용에 따라 달라짐):
    // - 풀 사용 시: 평균 5ns 할당
    // - 일반 생성: 평균 1000ns 할당
    // - 개선율: 약 99.5%
}
```

### Flyweight 패턴의 메모리 효율성

```java
// 메모리 효율적인 Flyweight 구현
public class CharacterFlyweight {
    private final char character;
    private final String fontFamily;
    private final int fontSize;
    private final Color color;
    
    // 메모리 사용량: 4 + 8 + 4 + 8 = 24 bytes per flyweight
    
    public void render(int x, int y, Graphics g) {
        // 외재적 상태 (x, y)는 파라미터로 전달
        g.setFont(new Font(fontFamily, Font.PLAIN, fontSize));
        g.setColor(color);
        g.drawString(String.valueOf(character), x, y);
    }
    
    // equals와 hashCode로 동일한 flyweight 식별
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof CharacterFlyweight)) return false;
        
        CharacterFlyweight that = (CharacterFlyweight) obj;
        return character == that.character &&
               fontSize == that.fontSize &&
               Objects.equals(fontFamily, that.fontFamily) &&
               Objects.equals(color, that.color);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(character, fontFamily, fontSize, color);
    }
}

// Factory로 Flyweight 인스턴스 관리
public class CharacterFlyweightFactory {
    private final Map<String, CharacterFlyweight> flyweights = new ConcurrentHashMap<>();
    
    public CharacterFlyweight getFlyweight(char character, String fontFamily, 
                                         int fontSize, Color color) {
        String key = character + "|" + fontFamily + "|" + fontSize + "|" + color.getRGB();
        
        return flyweights.computeIfAbsent(key, k -> 
            new CharacterFlyweight(character, fontFamily, fontSize, color)
        );
    }
    
    public int getFlyweightCount() {
        return flyweights.size();
    }
    
    // 예시 계산 (문자당 24바이트, 컨텍스트당 8바이트 가정. 실제 값은 JVM 객체 헤더 크기와 정렬 방식에 따라 달라짐):
    // 일반 구현: 1,000,000 문자 = 24MB
    // Flyweight: 100 고유 문자 = 2.4KB + 컨텍스트 8MB = 8.0024MB
    // 메모리 절약: 약 67%
}
```

## 성능 측정과 프로파일링

JMH(Java Microbenchmark Harness)는 JIT 워밍업, 데드 코드 제거(Dead Code Elimination), 루프 최적화 같은 마이크로벤치마크 함정을 자동으로 방지해주는 도구입니다. 직접 `System.nanoTime()`으로 측정하면 JIT이 워밍업되지 않은 상태를 재거나, 결과를 사용하지 않는 계산이 통째로 제거되어 잘못된 수치를 얻기 쉽습니다. 아래는 실제로 컴파일 가능한 최소 JMH 벤치마크 예시로, 의존 타입(`Observer`, `Subject`)까지 함께 정의했습니다.

```java
import org.openjdk.jmh.annotations.*;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

// 의존 타입 최소 정의 (Observer 패턴)
interface Observer {
    void update(Subject subject);
}

interface Subject {
    void attach(Observer observer);
    void notifyObservers();
}

class ConcreteObserver implements Observer {
    private int lastState;

    @Override
    public void update(Subject subject) {
        this.lastState = ((ConcreteSubject) subject).getState();
    }
}

class ConcreteSubject implements Subject {
    private final List<Observer> observers = new ArrayList<>();
    private int state = 0;

    @Override
    public void attach(Observer observer) {
        observers.add(observer);
    }

    @Override
    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(this);
        }
    }

    public int getState() {
        return state;
    }
}

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@State(Scope.Benchmark)
public class PatternPerformanceBenchmark {

    private List<Observer> observers;
    private Subject subject;

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
    public void testObserverNotification() {
        subject.notifyObservers();
    }

    @Benchmark
    public void testDirectMethodCall() {
        // Observer 패턴 없이 직접 호출과 비교
        for (Observer observer : observers) {
            observer.update(subject);
        }
    }

    // 예시 환경 기준 결과 분석 (실제 값은 JDK/CPU/워밍업 설정에 따라 달라짐):
    // Observer 패턴: 평균 2.5μs
    // 직접 호출: 평균 2.1μs
    // 오버헤드: 약 19%
}
```

### 메모리 프로파일링

```java
public class MemoryProfiler {
    
    public void analyzePatternMemoryUsage() {
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        
        // Singleton vs Multiple Instances
        long beforeSingleton = memoryBean.getHeapMemoryUsage().getUsed();
        
        // Singleton 테스트
        DatabaseConnection singleton = DatabaseConnection.getInstance();
        List<DatabaseConnection> singletonRefs = new ArrayList<>();
        for (int i = 0; i < 10000; i++) {
            singletonRefs.add(singleton);
        }
        
        long afterSingleton = memoryBean.getHeapMemoryUsage().getUsed();
        System.out.println("Singleton memory: " + (afterSingleton - beforeSingleton) + " bytes");
        
        // Multiple Instances 테스트
        long beforeMultiple = memoryBean.getHeapMemoryUsage().getUsed();
        
        List<DatabaseConnection> multipleInstances = new ArrayList<>();
        for (int i = 0; i < 10000; i++) {
            multipleInstances.add(new DatabaseConnection("url" + i));
        }
        
        long afterMultiple = memoryBean.getHeapMemoryUsage().getUsed();
        System.out.println("Multiple instances memory: " + (afterMultiple - beforeMultiple) + " bytes");
        
        // 예시 환경 기준 결과 (heap 사용량은 GC 타이밍에 영향을 받아 측정마다 흔들릴 수 있음):
        // Singleton: ~80KB (참조만 저장)
        // Multiple: ~2.4MB (각 인스턴스마다 메모리 할당)
        // 메모리 절약: 약 96.7%
    }
}
```

## 성능 최적화 가이드라인

### 패턴 선택 기준

```java
// 성능 크리티컬한 영역에서의 패턴 선택
public class PerformanceCriticalPatternChoice {
    
    // 높은 빈도 호출: 단순한 패턴 선택
    @HotSpot
    public void highFrequencyOperation() {
        // Strategy 패턴보다는 enum 기반 접근법
        SortType.QUICK.sort(data); // 더 빠른 디스패치
    }
    
    // 낮은 빈도 호출: 유연성 우선
    @ColdSpot
    public void lowFrequencyOperation() {
        // 복잡한 패턴도 허용 (Factory, Builder 등)
        ComplexObjectBuilder.builder()
            .withProperty1(value1)
            .withProperty2(value2)
            .build();
    }
    
    // 메모리 제약 환경: 경량 패턴 선택
    @MemoryConstrained
    public void memoryConstrainedOperation() {
        // Flyweight 패턴 적극 활용
        CharacterFlyweight flyweight = factory.getFlyweight('A');
        flyweight.render(x, y, graphics);
    }
}

// 성능 모니터링을 위한 Decorator
public class PerformanceMonitoringDecorator<T> implements Service<T> {
    private final Service<T> delegate;
    private final PerformanceCounter counter;
    
    @Override
    public T execute(Request request) {
        long startTime = System.nanoTime();
        try {
            return delegate.execute(request);
        } finally {
            long duration = System.nanoTime() - startTime;
            counter.record(duration);
            
            // 성능 임계값 초과 시 경고
            if (duration > PERFORMANCE_THRESHOLD) {
                logger.warn("Slow operation detected: {}ns", duration);
            }
        }
    }
}
```

### 프로덕션 환경 최적화

```java
// 프로덕션 환경에서의 패턴 최적화
@Configuration
public class ProductionOptimizedConfig {
    
    // Singleton 범위 최적화
    @Bean
    @Scope("singleton")
    public ExpensiveService expensiveService() {
        return new ExpensiveServiceImpl();
    }
    
    // Connection Pool을 활용한 Factory
    @Bean
    public DataSourceFactory dataSourceFactory() {
        return PooledDataSourceFactory.builder()
            .maxPoolSize(50)
            .minPoolSize(10)
            .connectionTimeout(30000)
            .build();
    }
    
    // 비동기 Observer 패턴
    @Bean
    public AsyncEventPublisher eventPublisher() {
        return AsyncEventPublisher.builder()
            .threadPoolSize(4)
            .queueCapacity(1000)
            .rejectionPolicy("CALLER_RUNS")
            .build();
    }
}
```

## 실습 과제

### 과제 1: 성능 벤치마크 작성
다음 패턴들의 성능을 비교 분석하는 벤치마크를 작성하세요:
1. Factory Method vs Direct Instantiation
2. Decorator Chain vs Conditional Logic
3. Observer vs Event Bus

### 과제 2: 메모리 효율적인 패턴 구현
대용량 데이터 처리를 위한 메모리 효율적인 패턴을 구현하세요:
1. Flyweight 패턴으로 게임 캐릭터 시스템
2. Object Pool 패턴으로 네트워크 연결 관리
3. Proxy 패턴으로 이미지 지연 로딩

## 토론 주제

1. **성능 vs 유지보수성**: 어떤 상황에서 성능을 우선시해야 하는가?

2. **마이크로 벤치마크의 함정**: JIT 워밍업, GC 영향 등을 어떻게 고려할 것인가?

3. **패턴의 적정 복잡도**: 언제 패턴을 단순화하거나 제거해야 하는가?

## 흔한 오해: 패턴은 항상 느리다

"디자인 패턴은 우아하지만 느리다"는 말은 절반만 맞다. 위 벤치마크들을 종합하면 실제 그림은 더 미묘하다.

첫째, 오버헤드의 상대 크기와 절대 크기를 구분해야 한다. Factory Method는 직접 생성보다 "+140%" 느리다는 수치만 보면 심각해 보이지만, 절대 시간으로는 수십~수백 나노초 차이일 뿐이다. Scott Oaks(2014)는 대부분의 실무 애플리케이션에서 실제 병목은 I/O, 네트워크 호출, 알고리즘 복잡도이지 이런 나노초 단위의 패턴 오버헤드가 아니라고 지적한다. "최적화 기법 적용 가이드" 표에서 콜드 패스(호출 빈도가 낮은 경로)에는 패턴 오버헤드가 1% 미만이라 무시 가능하다고 정리한 것도 같은 맥락이다.

둘째, 패턴이 오히려 빨라지는 경우도 있다. Flyweight는 메모리를 최대 80% 절약하면서 캐시 지역성을 높여 조회 성능을 개선할 수 있고, Object Pool은 생성 비용이 큰 객체(스레드, DB 커넥션)에서 할당 비용을 1000ns에서 5ns 수준으로 줄인다. 이런 경우 "패턴을 쓰면 느려진다"는 통념과 정반대로, 패턴을 안 쓰는 것이 더 느리다.

셋째, 진짜 위험은 오버헤드의 크기가 아니라 누적되는 위치다. Decorator 체인이나 Observer의 리스너 수처럼 핫 패스(자주 호출되는 경로)에서 반복되는 오버헤드는 나노초 단위라도 누적되어 유의미한 지연이 된다. 따라서 "패턴은 항상 느리다/항상 무시할 만하다"라는 일반화 대신, 그 패턴이 핫 패스에 있는지 콜드 패스에 있는지를 먼저 확인하는 것이 실무적으로 옳은 질문이다.

## 한눈에 보는 패턴 성능 최적화

원래 여기에는 "패턴별 성능 특성", "최적화 우선순위", "최적화 기법 매트릭스", "오버헤드 벤치마크 가이드", "최적화 결정 가이드" 등 6개의 표가 있었지만, 대부분 같은 정보(어떤 패턴에 어떤 최적화가 필요한가)를 다른 각도에서 반복하고 있었습니다. 아래 두 표로 통합합니다.

### 패턴별 성능 특성과 최적화 우선순위

패턴별 오버헤드 크기와 대응하는 최적화 우선순위·포인트를 한 표로 정리합니다. 우선순위가 높을수록 실무에서 실제로 병목이 되는 경우가 많았던 패턴입니다.

| 패턴 | 메모리 오버헤드 | 실행 시간 오버헤드 | 최적화 우선순위 | 핵심 최적화 포인트 |
|------|--------------|-----------------|---------------|-----------------|
| Decorator | 높음 (체인당) | 중간 | 1 (높음) | 체인 길이 5단계 이하로 제한 |
| Observer | 중간 | 통지 비용 (리스너 수에 선형 비례) | 1 (높음) | 리스너 수 관리, 비동기 통지 |
| Flyweight | 매우 낮음 | 조회 비용 | 매우 높음 | 메모리 절약 효과를 캐시 히트율로 검증 |
| Prototype | 가변적 | 복제 비용 | 2 (중간) | 얕은 복사 vs 깊은 복사 선택 |
| Proxy | 낮음 | 가변적 (I/O 대상에 좌우) | 2 (중간) | 지연 로딩 효과 확인 |
| Command | 중간 | 낮음 | 2 (중간) | 명령 이력 크기 제한 |
| Builder | 중간 | 낮음 | 3 (낮음) | 불필요한 빌더 사용 피하기 |
| Strategy | 낮음 | 낮음 (if-else 대비 +20~25%) | 3 (낮음) | 전략 객체 재사용 |
| Factory Method | 낮음 | 낮음 | 3 (낮음) | 생성 비용이 클 때만 객체 풀 고려 |
| Singleton | 낮음 | 낮음 | 3 (낮음) | 스레드 안전성 확보 방식(synchronized vs 초기화 시점) 확인 |
| Abstract Factory | 중간 | 낮음 | 3 (낮음) | - |
| Adapter | 낮음 | 무시 가능 | 3 (낮음) | - |

### 최적화 기법 적용 가이드

"어떤 상황에서 어떤 기법을 써야 하는가"를 기준으로 정리합니다. 핫 패스(자주 호출되는 경로)는 나노초 단위 오버헤드도 누적되므로 패턴을 최소화하는 방향이, 콜드 패스는 I/O·네트워크 지연이 패턴 오버헤드(대개 1% 미만)를 압도하므로 가독성을 우선하는 방향이 맞습니다.

| 상황 | 권장 기법 | 적용 패턴 | 효과 (복잡도) |
|------|----------|----------|-------------|
| 핫 패스 — 나노초 단위로 민감 | 패턴 최소화·직접 호출 | Strategy, Observer | 단순 getter~메서드 체인 수준(허용 오버헤드 100~2000%)의 누적을 방지 |
| 콜드 패스 — 호출 빈도 낮음 | 패턴 유지, 가독성 우선 | Factory, Builder | I/O·네트워크 호출(1ms+) 앞에서 패턴 오버헤드는 1% 미만이라 무시 가능 |
| 반복 생성 비용이 큰 객체 | 객체 풀링 | Factory, Prototype | 생성 비용 감소 (복잡도 중간) |
| 시작 시간이 중요 | 지연 초기화 | Singleton, Proxy | 앱 부팅 시간 단축 (복잡도 낮음) |
| 메모리 제약 | Flyweight, 캐싱 | Flyweight, Proxy | 반복 비용 제거, 객체 수 감소 (복잡도 중간) |
| 동시성 높음 | 불변 객체, Lock-free 자료구조 | Builder, Prototype | 락 경합 감소 (복잡도 낮음) |
| 통지·명령 이력이 누적됨 | 배치 처리 | Observer, Command | 통지 비용 감소 (복잡도 중간) |

프로파일링에는 목적에 맞는 도구를 씁니다. 메모리 할당 횟수는 VisualVM·JProfiler로, 메서드 호출 시간은 JMH·Async-profiler로, GC 압력은 GC 로그·JFR로, Flyweight의 실제 캐시 히트율은 커스텀 메트릭으로 확인합니다.

## 평가 기준

이 글을 읽고 다음을 스스로 설명할 수 있다면 핵심을 이해한 것입니다.

- 위 벤치마크 수치가 "예시 수치"인 이유와, 실무에 적용하기 전에 반드시 대상 환경에서 JMH로 재측정해야 하는 이유를 설명할 수 있다.
- monomorphic·bipolymorphic·megamorphic 호출이 JIT 인라이닝 결정에 미치는 영향을 설명하고, Strategy/Observer 같은 다형성 패턴이 왜 megamorphic 상황을 유발하기 쉬운지 말할 수 있다.
- Object Pool이 "생성 비용 >> 풀 관리 비용"일 때만 이득이라는 조건을 설명하고, 반대의 경우(단순 POJO 등)에 풀링이 손해인 이유를 말할 수 있다.
- 핫 패스와 콜드 패스에서 왜 서로 다른 최적화 전략(패턴 최소화 vs 가독성 우선)을 선택해야 하는지 설명할 수 있다.

다음 글([안티패턴 식별과 리팩토링](/post/design-patterns/antipatterns-refactoring/))에서는 성능이 아닌 유지보수성 관점에서, 패턴이 오히려 코드를 나쁘게 만드는 상황(안티패턴)과 그 리팩토링 방법을 다룹니다.

---

## 참고 자료

### 성능 측정 도구
- JMH (Java Microbenchmark Harness)
- VisualVM, JProfiler
- GC 로그 분석 도구

### 관련 도서
- "Java Performance: The Definitive Guide" - Scott Oaks (2014)
- "Optimizing Java" - Benjamin J. Evans, James Gough, Chris Newland (2018)

---

**"좋은 코드는 아름답고 빠르다. 패턴은 그 두 가지를 모두 달성하는 도구가 되어야 한다."**
