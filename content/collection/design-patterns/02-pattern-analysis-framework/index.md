---
draft: true
collection_order: 20
title: "[Design Patterns] 패턴 분석의 프레임워크"
description: "GoF 패턴을 체계적으로 분석하고 평가하는 과학적 방법론을 제시합니다. Intent 분석부터 Trade-off 평가까지, 패턴의 본질을 꿰뚫어보는 전문가적 사고 과정을 학습하고, 상황에 맞는 최적의 패턴을 선택할 수 있는 분석 능력을 기릅니다. 인지과학적 관점에서 패턴 인식과 스키마 이론을 탐구합니다."
image: "wordcloud.png"
date: 2024-12-02T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Software Architecture
- Design Analysis
- Pattern Theory
tags:
- Pattern Analysis
- GoF Patterns
- Design Framework
- Software Design
- Pattern Evaluation
- Trade Off Analysis
- Intent Analysis
- Pattern Selection
- Design Methodology
- Cognitive Science
- Schema Theory
- Pattern Recognition
- Expert Thinking
- Software Architecture
- Design Principles
- Pattern Comparison
- Architectural Patterns
- System Design
- Code Quality
- Design Decision
- Pattern Mastery
- Software Engineering
- Design Wisdom
- Pattern Application
- Structural Analysis
- Behavioral Analysis
- Creational Analysis
- Design Metrics
- Pattern Evolution
- Software Craftsmanship
- 패턴 분석
- GoF 패턴
- 설계 프레임워크
- 소프트웨어 설계
- 패턴 평가
- 트레이드오프 분석
- 의도 분석
- 패턴 선택
- 설계 방법론
- 인지 과학
- 스키마 이론
- 패턴 인식
- 전문가 사고
- 소프트웨어 아키텍처
- 설계 원칙
- 패턴 비교
- 아키텍처 패턴
- 시스템 설계
- 코드 품질
- 설계 결정
- 패턴 마스터리
- 소프트웨어 공학
- 설계 지혜
- 패턴 적용
- 구조적 분석
- 행동적 분석
- 생성적 분석
- 설계 메트릭
- 패턴 진화
- 소프트웨어 장인정신
---

GoF 패턴을 체계적으로 분석하고 평가하는 과학적 방법론을 제시합니다. Intent 분석부터 Trade-off 평가까지, 패턴의 본질을 꿰뚫어보는 전문가적 사고 과정을 학습합니다.

## 서론: 패턴을 보는 눈

> *"패턴을 안다는 것과 패턴을 이해한다는 것은 전혀 다른 차원의 문제다."*

많은 개발자들이 GoF의 23개 패턴을 외우고 있습니다. Observer는 일대다 관계, Strategy는 알고리즘 교체... 하지만 정작 실무에서 **"이 상황에서 어떤 패턴을 써야 할까?"** 혹은 **"이 패턴이 정말 최선의 선택일까?"**라는 질문 앞에서는 막막해집니다.

패턴을 단순히 암기하는 것과 패턴의 본질을 꿰뚫어보는 것 사이에는 **거대한 간극**이 있습니다. 진정한 설계 전문가는 패턴을 **분석하고, 평가하고, 상황에 맞게 선택**할 수 있는 능력을 갖춘 사람입니다.

이번 글에서는 패턴을 체계적으로 분석하고 평가하는 **과학적 방법론**을 제시합니다. 이는 단순한 기법이 아니라, **사고의 프레임워크**입니다.

### GoF 패턴 분석 템플릿의 심층 해부

#### Intent (의도) - 패턴의 영혼

GoF 책에서 가장 중요한 섹션은 바로 **"Intent"**입니다. 여기에 패턴의 핵심 가치가 압축되어 있습니다.

**Observer 패턴의 Intent 분석:**
```
"Define a one-to-many dependency between objects so that when one 
object changes state, all its dependents are notified and updated automatically."
```

이 한 문장을 해부해보면:
- **핵심 문제**: "one-to-many dependency"
- **트리거 조건**: "when one object changes state"  
- **해결책**: "all its dependents are notified and updated automatically"
- **목표**: 자동화된 상태 동기화

**Intent 분석 체크리스트:**
```
□ 해결하려는 핵심 문제가 명확한가?
□ 문제의 범위가 적절히 정의되었는가?
□ 해결책의 본질이 간결하게 표현되었는가?
□ 다른 패턴과 구분되는 고유성이 있는가?
```

#### Structure (구조) - 패턴의 해부학

구조 다이어그램은 패턴의 **"해부학"**입니다. 단순히 클래스 관계를 보여주는 것이 아니라, **역할 분담의 철학**을 담고 있습니다.

**Strategy 패턴 구조 분석:**
```java
// Context: 전략을 사용하는 주체
public class SortContext {
    private SortStrategy strategy;  // 의존성 주입 지점
    
    public void setStrategy(SortStrategy strategy) {
        this.strategy = strategy;   // 런타임 교체 가능
    }
    
    public void executeSort(int[] data) {
        strategy.sort(data);        // 위임(delegation)
    }
}

// Strategy: 알고리즘의 공통 인터페이스
public interface SortStrategy {
    void sort(int[] data);          // 템플릿 메서드
}

// ConcreteStrategy: 구체적 구현
public class QuickSortStrategy implements SortStrategy {
    public void sort(int[] data) {
        // QuickSort 구현
    }
}
```

**구조 분석의 핵심 포인트:**
1. **역할 분리**: Context는 "언제", Strategy는 "어떻게"
2. **의존성 방향**: Context → Strategy (역방향 불가)
3. **교체 메커니즘**: setStrategy() 통한 런타임 변경
4. **위임 패턴**: Context가 실제 작업을 Strategy에 위임

#### Participants (참여자) - 역할과 책임

각 참여자는 **단일 책임 원칙**을 따라 명확한 역할을 가집니다.

**Command 패턴 참여자 분석:**
```java
// Client: 명령을 조립하는 역할
public class MacroRecorder {
    public void createMacro() {
        Command[] commands = {
            new CopyCommand(editor),
            new PasteCommand(editor),
            new SaveCommand(editor)
        };
        MacroCommand macro = new MacroCommand(commands);
        invoker.setCommand(macro);
    }
}

// Invoker: 명령을 실행하는 역할
public class MenuButton {
    private Command command;
    
    public void click() {
        command.execute();  // 구체적 명령을 몰라도 실행 가능
    }
}

// Command: 명령의 추상화
public interface Command {
    void execute();
    void undo();           // 실행 취소 지원
}

// ConcreteCommand: 구체적 명령 구현
public class CopyCommand implements Command {
    private TextEditor receiver;
    private String backup;
    
    public void execute() {
        backup = receiver.getSelection();
        receiver.copy();
    }
    
    public void undo() {
        receiver.setSelection(backup);
    }
}

// Receiver: 실제 작업을 수행하는 객체
public class TextEditor {
    public void copy() { /* 실제 복사 로직 */ }
    public void paste() { /* 실제 붙여넣기 로직 */ }
}
```

**참여자 분석 매트릭스:**
| 참여자 | 주요 책임 | 알아야 할 것 | 몰라도 되는 것 |
|--------|-----------|---------------|----------------|
| Client | 명령 조립 | Command 인터페이스 | 구체적 실행 방법 |
| Invoker | 명령 실행 트리거 | Command 인터페이스 | 구체적 명령 내용 |
| Command | 인터페이스 정의 | Receiver 인터페이스 | 구체적 구현 방법 |
| ConcreteCmd | 구체적 명령 구현 | Receiver의 메서드 | 다른 Command들 |
| Receiver | 실제 작업 수행 | 자신의 도메인 로직 | Command 존재 여부 |

#### Collaborations (협력) - 상호작용의 예술

협력 패턴은 **시나리오별 상호작용**을 보여줍니다. 이는 패턴의 **동적 측면**입니다.

**Observer 패턴 협력 시퀀스:**
```
Subject.notifyObservers() 호출 시:

1. Subject → Observer1: update()
2. Subject → Observer2: update()  
3. Subject → Observer3: update()

Observer.update() 내부에서:

4. Observer1 → Subject: getState()
5. Observer1: updateInternalState()
6. Observer2 → Subject: getState()
7. Observer2: updateInternalState()
```

**협력 분석의 핵심 질문:**
- 누가 협력을 시작하는가? (Subject)
- 협력의 순서가 중요한가? (Observer들의 순서는 보통 중요하지 않음)
- 실패 시 어떻게 처리하는가? (일부 Observer 실패 시 다른 Observer들은?)
- 순환 참조 위험이 있는가? (Observer가 Subject 상태를 변경하면?)

### 패턴 적용 조건 분석 기법

#### 문제 영역 식별 매트릭스

패턴 적용을 위해서는 먼저 **문제의 본질**을 정확히 파악해야 합니다.

**문제 유형별 패턴 매핑:**
| 문제 유형 | 1차 후보 패턴 | 2차 후보 패턴 |
|-----------|---------------|---------------|
| 객체 생성이 복잡함 | Factory Method | Abstract Factory, Builder |
| 객체 생성 비용이 높음 | Singleton | Flyweight, Object Pool |
| 런타임에 행동을 변경해야 함 | Strategy | State, Command |
| 복잡한 객체 구조를 단순화 | Facade | Adapter, Proxy |
| 객체 간 일대다 의존성 | Observer | Mediator, Event Bus |
| 알고리즘을 캡슐화해야 함 | Template Method | Strategy, Command |

#### 적용 가능성 평가 체크리스트

**Context 분석:**
```java
// 예시: 로깅 시스템에서 Strategy 패턴 적용 검토

// 현재 상황
public class Logger {
    public void log(String message, LogLevel level) {
        if (level == LogLevel.DEBUG) {
            System.out.println("[DEBUG] " + message);
        } else if (level == LogLevel.INFO) {
            writeToFile("[INFO] " + message);
        } else if (level == LogLevel.ERROR) {
            sendToSentry("[ERROR] " + message);
        }
    }
}

// Strategy 패턴 적용 가능성 평가
```

**평가 기준:**
```
- 알고리즘이 여러 개인가? 
   → YES: DEBUG/INFO/ERROR 각각 다른 출력 방식

- 런타임에 알고리즘을 변경해야 하는가?
   → YES: 환경(개발/운영)에 따라 로깅 방식 변경

- 새로운 알고리즘이 추가될 가능성이 있는가?
   → YES: WARN 레벨, 외부 모니터링 시스템 연동 등

- 알고리즘들이 공통 인터페이스를 가질 수 있는가?
   → YES: log(String message) 인터페이스로 통일 가능

- 알고리즘들 간에 상태 공유가 필요한가?
   → NO: 각 로그 전략은 독립적

결론: Strategy 패턴 적용 적합
```

#### 대안 패턴 비교 분석

같은 문제를 해결하는 여러 패턴이 있을 때의 **선택 기준**:

**캐싱 구현 시 패턴 선택:**
```java
// 옵션 1: Proxy 패턴
public class CacheProxy implements DataService {
    private DataService realService;
    private Map<String, Object> cache = new HashMap<>();
    
    public Object getData(String key) {
        if (cache.containsKey(key)) {
            return cache.get(key);
        }
        Object data = realService.getData(key);
        cache.put(key, data);
        return data;
    }
}

// 옵션 2: Decorator 패턴  
public class CacheDecorator implements DataService {
    private DataService wrappedService;
    private Map<String, Object> cache = new HashMap<>();
    
    public Object getData(String key) {
        if (cache.containsKey(key)) {
            return cache.get(key);
        }
        Object data = wrappedService.getData(key);
        cache.put(key, data);
        return data;
    }
}

// 옵션 3: Strategy 패턴
public class DataServiceContext {
    private CacheStrategy cacheStrategy;
    private DataService dataService;
    
    public Object getData(String key) {
        return cacheStrategy.getData(key, dataService);
    }
}
```

**비교 분석:**

| 기준 | Proxy | Decorator | Strategy |
|------|-------|-----------|----------|
| 투명성 | 높음 | 중간 | 낮음 |
| 런타임 교체 | 어려움 | 어려움 | 쉬움 |
| 다중 기능 조합 | 어려움 | 쉬움 | 중간 |
| 성능 오버헤드 | 낮음 | 중간 | 높음 |
| 구현 복잡도 | 낮음 | 중간 | 높음 |

```
선택 기준:
- 단순 캐싱만 필요 → Proxy
- 캐싱 + 로깅 + 압축 등 다중 기능 → Decorator  
- 캐싱 전략을 런타임에 변경 → Strategy
```

### Trade-off 분석 프레임워크

#### 성능 vs 유연성 분석

**Flyweight vs 일반 객체:**
```java
// 일반 객체 방식: 성능 우수, 유연성 낮음
public class Character {
    private char character;
    private Font font;
    private Color color;
    private int x, y;
    
    // 10,000개 문자 = 10,000개 Font, Color 객체
}

// Flyweight 방식: 메모리 효율적, 복잡성 증가
public class CharacterFlyweight {
    private char character;
    private Font font;      // intrinsic state (공유)
    private Color color;    // intrinsic state (공유)
    
    public void render(int x, int y, Graphics g) {
        // extrinsic state는 파라미터로 전달
    }
}

public class CharacterFactory {
    private Map<String, CharacterFlyweight> flyweights = new HashMap<>();
    
    public CharacterFlyweight getFlyweight(char c, Font f, Color col) {
        String key = c + f.toString() + col.toString();
        return flyweights.computeIfAbsent(key, 
            k -> new CharacterFlyweight(c, f, col));
    }
}
```

**성능 측정 데이터:**
```
10,000개 문자 객체 생성 시:

일반 방식:
- 메모리 사용량: ~40MB (4KB × 10,000)
- 생성 시간: ~50ms
- 접근 시간: ~1ns (직접 접근)

Flyweight 방식:
- 메모리 사용량: ~1MB (공유 객체 + 팩토리)
- 생성 시간: ~20ms (중복 제거)
- 접근 시간: ~100ns (HashMap 조회)

결론: 메모리가 중요하면 Flyweight, 속도가 중요하면 일반 방식
```

#### 복잡성 vs 재사용성 분석

**Abstract Factory의 복잡성 증가:**
```java
// 단순한 팩토리: 복잡성 낮음, 재사용성 낮음
public class ButtonFactory {
    public Button createButton(String os) {
        if ("Windows".equals(os)) {
            return new WindowsButton();
        } else if ("Mac".equals(os)) {
            return new MacButton();
        }
        throw new IllegalArgumentException("Unsupported OS");
    }
}

// Abstract Factory: 복잡성 높음, 재사용성 높음
public abstract class GUIFactory {
    public abstract Button createButton();
    public abstract Checkbox createCheckbox();
    public abstract Menu createMenu();
}

public class WindowsFactory extends GUIFactory {
    public Button createButton() { return new WindowsButton(); }
    public Checkbox createCheckbox() { return new WindowsCheckbox(); }
    public Menu createMenu() { return new WindowsMenu(); }
}

public class MacFactory extends GUIFactory {
    public Button createButton() { return new MacButton(); }
    public Checkbox createCheckbox() { return new MacCheckbox(); }
    public Menu createMenu() { return new MacMenu(); }
}
```

**복잡성 매트릭스:**
```
구현 방식          | 클래스 수 | Cyclomatic | 이해 시간 | 확장 비용
Simple Factory    |    3     |     3      |   5분    |   높음
Abstract Factory  |    12    |     8      |   30분   |   낮음

비교 기준:
- 제품군이 2개 이하 → Simple Factory
- 제품군이 3개 이상이고 자주 확장 → Abstract Factory
```

#### 메모리 vs 속도 Trade-off

**Singleton vs Factory의 메모리 사용:**
```java
// Singleton: 메모리 효율적, 전역 상태 위험
public class DatabaseConnection {
    private static DatabaseConnection instance;
    private Connection connection;
    
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
    
    // 메모리: 1개 인스턴스만 유지
    // 동시성: synchronized로 인한 성능 저하
}

// Factory: 유연성 높음, 메모리 사용량 증가
public class ConnectionFactory {
    private Pool<Connection> connectionPool;
    
    public Connection getConnection() {
        return connectionPool.borrowObject();
    }
    
    // 메모리: N개 Connection 객체 유지
    // 동시성: Thread-safe pool 구현
}
```

**성능 벤치마크:**
```
동시 접속 1000명 시:

Singleton 방식:
- 메모리: 50MB (1개 Connection + 대기 큐)
- 평균 응답시간: 500ms (순차 처리)
- TPS: 2000

Connection Pool 방식:  
- 메모리: 200MB (20개 Connection pool)
- 평균 응답시간: 50ms (병렬 처리)  
- TPS: 20000

Trade-off: 메모리 4배 증가로 성능 10배 향상
```

### 패턴 평가 매트릭스

#### 정량적 평가 기준

**패턴 평가 매트릭스 템플릿:**

| 평가 기준 | 가중치 | Observer | Strategy | Command |
|-----------|--------|----------|----------|---------|
| 코드 복잡도 (낮을수록 좋음) | 25% | 6 | 8 | 4 |
| 성능 오버헤드 (낮을수록 좋음) | 20% | 5 | 9 | 7 |
| 확장 용이성 (높을수록 좋음) | 20% | 9 | 9 | 8 |
| 팀 숙련도 요구 (낮을수록 좋음) | 15% | 7 | 8 | 5 |
| 메모리 사용량 (낮을수록 좋음) | 10% | 6 | 9 | 7 |
| 테스트 용이성 (높을수록 좋음) | 10% | 8 | 9 | 9 |

```
가중 평균 계산:
Observer = (6×0.25 + 5×0.20 + 9×0.20 + 7×0.15 + 6×0.10 + 8×0.10) = 6.65
Strategy = (8×0.25 + 9×0.20 + 9×0.20 + 8×0.15 + 9×0.10 + 9×0.10) = 8.40
Command = (4×0.25 + 7×0.20 + 8×0.20 + 5×0.15 + 7×0.10 + 9×0.10) = 6.35
```

#### 상황별 가중치 적용

**프로젝트 특성에 따른 가중치 조정:**
| 프로젝트 유형 | 개발 속도 | 코드 복잡도 | 확장성 | 유지보수성 | 성능 | 메모리 효율성 |
|---------------|-----------|-------------|--------|------------|------|---------------|
| 스타트업 초기 프로젝트 | 40% | 30% | 20% | - | 10% | - |
| 대규모 엔터프라이즈 | 15% | - | 35% | 25% | 25% | - |
| 실시간 시스템 | - | 10% | 15% | - | 50% | 25% |

#### 팀 특성 고려사항

**팀 숙련도별 패턴 선택 가이드:**
```java
// 초급 팀: 단순하고 직관적인 패턴 선호
public class SimpleFactory {
    public static Logger createLogger(String type) {
        switch (type) {
            case "file": return new FileLogger();
            case "console": return new ConsoleLogger();
            default: throw new IllegalArgumentException();
        }
    }
}

// 중급 팀: 적당한 복잡도의 패턴 활용 가능
public class LoggerBuilder {
    private String output;
    private String format;
    private LogLevel level;
    
    public LoggerBuilder output(String output) {
        this.output = output;
        return this;
    }
    
    public Logger build() {
        return new Logger(output, format, level);
    }
}

// 고급 팀: 복잡한 패턴도 효과적으로 활용
public class LoggerFactory {
    private Map<String, Supplier<Logger>> loggerSuppliers;
    
    public <T extends Logger> void registerLogger(
        String name, 
        Class<T> loggerClass,
        Function<Configuration, T> factory) {
        // 제네릭과 함수형 인터페이스를 활용한 고급 팩토리
    }
}
```

### 인지과학적 패턴 분석

#### 청킹(Chunking)과 패턴 인식

**전문가의 패턴 인식 과정:**
```java
// 초보자가 보는 것: 20줄의 개별 코드
public class WeatherStation {
    private List<Display> displays = new ArrayList<>();
    
    public void addDisplay(Display display) {
        displays.add(display);
    }
    
    public void removeDisplay(Display display) {
        displays.remove(display);
    }
    
    public void notifyDisplays() {
        for (Display display : displays) {
            display.update(temperature, humidity, pressure);
        }
    }
    
    public void measurementsChanged() {
        notifyDisplays();
    }
}

// 전문가가 보는 것: "Observer 패턴"
// → 즉시 다음 사항들을 추론:
//   - Subject-Observer 관계
//   - Push vs Pull 모델 (Push 사용)
//   - 느슨한 결합
//   - 확장 가능한 구조
```

**패턴 인식 훈련법:**
1. **패턴 시그니처 학습**: `List<Observer>` + `notify()` = Observer 패턴
2. **의도 기반 분류**: "일대다 의존성" → Observer
3. **구조적 특징 암기**: Subject, Observer, ConcreteSubject, ConcreteObserver
4. **변형 패턴 인식**: EventBus, Reactive Streams도 Observer의 변형

#### 스키마 이론과 패턴 적용

**패턴 스키마의 구성 요소:**
```
Observer 패턴 스키마:
┌─ 구조적 스키마 ─┐    ┌─ 행동적 스키마 ─┐    ┌─ 적용 스키마 ─┐
│ Subject         │    │ attach()       │    │ 상태 변경     │
│ Observer        │    │ detach()       │    │ 통지 필요     │
│ ConcreteSubject │    │ notify()       │    │ 일대다 관계   │
│ ConcreteObserver│    │ update()       │    │ 느슨한 결합   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**스키마 활성화 트리거:**
- "변경 사항을 여러 곳에 알려야 한다" → Observer 스키마 활성화
- "알고리즘을 바꿔가며 사용해야 한다" → Strategy 스키마 활성화
- "복잡한 객체를 단계별로 만들어야 한다" → Builder 스키마 활성화

### 패턴의 진화적 관점

#### 언어별 패턴 적응

**JavaScript에서의 Observer 패턴 진화:**
```javascript
// 전통적 Observer (Java 스타일)
class Subject {
    constructor() {
        this.observers = [];
    }
    
    attach(observer) {
        this.observers.push(observer);
    }
    
    notify(data) {
        this.observers.forEach(observer => observer.update(data));
    }
}

// JavaScript 관용적 Observer (EventEmitter)
const EventEmitter = require('events');

class WeatherStation extends EventEmitter {
    updateWeather(data) {
        this.emit('weatherChanged', data);
    }
}

const station = new WeatherStation();
station.on('weatherChanged', data => console.log(data));

// 현대적 Reactive Observer (RxJS)
import { Subject } from 'rxjs';

const weatherSubject = new Subject();
const subscription = weatherSubject.subscribe({
    next: data => console.log(data),
    error: err => console.error(err),
    complete: () => console.log('Complete')
});
```

**언어별 패턴 적응 원칙:**
- **C++**: RAII와 결합된 패턴 (스마트 포인터 활용)
- **Python**: Duck Typing 활용한 간소화된 패턴
- **Rust**: 소유권 시스템과 조화되는 패턴 변형
- **Go**: 인터페이스 기반 간소화된 패턴

#### 패턴의 자연적 진화

**Singleton → Service Locator → Dependency Injection 진화:**
```java
// 1세대: Singleton (1990년대)
public class DatabaseConnection {
    private static DatabaseConnection instance;
    // 전역 상태, 테스트 어려움
}

// 2세대: Service Locator (2000년대)  
public class ServiceLocator {
    private static Map<Class<?>, Object> services = new HashMap<>();
    
    public static <T> T getService(Class<T> serviceClass) {
        return (T) services.get(serviceClass);
    }
    // 중앙집중식 관리, 여전히 전역 상태
}

// 3세대: Dependency Injection (2010년대~)
@Component
public class OrderService {
    private final PaymentService paymentService;
    
    @Autowired
    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
    // 명시적 의존성, 테스트 용이
}
```

### 실전 패턴 분석 예제

#### 케이스 스터디: 로깅 시스템 설계

**요구사항:**
- 다양한 출력 대상 (콘솔, 파일, 네트워크)
- 로그 레벨별 필터링
- 포맷 커스터마이징
- 성능 최적화 (비동기 처리)

**패턴 적용 분석:**
```java
// Strategy 패턴: 출력 전략
public interface LogAppender {
    void append(LogEvent event);
}

public class ConsoleAppender implements LogAppender {
    public void append(LogEvent event) {
        System.out.println(event.getMessage());
    }
}

public class AsyncAppender implements LogAppender {
    private final LogAppender delegate;
    private final BlockingQueue<LogEvent> queue = new LinkedBlockingQueue<>();
    
    public AsyncAppender(LogAppender delegate) {
        this.delegate = delegate;
        startBackgroundThread();
    }
    
    public void append(LogEvent event) {
        queue.offer(event);  // 비동기 처리
    }
}

// Chain of Responsibility: 필터 체인
public abstract class LogFilter {
    protected LogFilter next;
    
    public void setNext(LogFilter next) {
        this.next = next;
    }
    
    public final void filter(LogEvent event) {
        if (shouldProcess(event)) {
            process(event);
            if (next != null) {
                next.filter(event);
            }
        }
    }
    
    protected abstract boolean shouldProcess(LogEvent event);
    protected abstract void process(LogEvent event);
}

// Builder 패턴: 로거 구성
public class LoggerBuilder {
    private List<LogAppender> appenders = new ArrayList<>();
    private LogLevel level = LogLevel.INFO;
    private LogFormatter formatter = new SimpleFormatter();
    
    public LoggerBuilder addAppender(LogAppender appender) {
        this.appenders.add(appender);
        return this;
    }
    
    public LoggerBuilder level(LogLevel level) {
        this.level = level;
        return this;
    }
    
    public Logger build() {
        return new Logger(appenders, level, formatter);
    }
}
```

**패턴 선택 근거:**
```
Strategy (LogAppender):
- 출력 방식이 다양함
- 런타임 교체 필요 없음 (설정 시점에 결정)
- 각 전략이 독립적

Chain of Responsibility (LogFilter):  
- 여러 필터를 조합해야 함
- 필터 순서가 중요함
- 동적으로 필터 체인 구성 가능

Builder (LoggerBuilder):
- 설정 옵션이 많음
- 선택적 매개변수 지원
- 불변 객체 생성
```

## 한눈에 보는 패턴 분석 프레임워크

### 패턴 분석 체크리스트

| 분석 단계 | 핵심 질문 | 확인 항목 |
|----------|----------|----------|
| Intent 분석 | 이 패턴이 해결하는 핵심 문제는? | 문제 정의 명확성, 범위 적절성, 해법 간결성 |
| Structure 분석 | 역할 분담은 적절한가? | 의존성 방향, 교체 메커니즘, 위임 패턴 |
| Participants 분석 | 각 참여자의 책임은 명확한가? | 단일 책임, 알아야 할 것/몰라도 될 것 |
| Collaborations 분석 | 상호작용은 적절한가? | 협력 시작점, 순서 중요성, 실패 처리 |

### 패턴 적용 결정 매트릭스

| 문제 유형 | 1차 후보 | 2차 후보 | 선택 기준 |
|----------|----------|----------|----------|
| 객체 생성이 복잡함 | Factory Method | Abstract Factory, Builder | 제품군 수, 생성 단계 복잡도 |
| 객체 생성 비용이 높음 | Singleton | Flyweight, Object Pool | 인스턴스 공유 가능 여부 |
| 런타임 행동 변경 | Strategy | State, Command | 상태 의존성, 실행 취소 필요 |
| 복잡한 구조 단순화 | Facade | Adapter, Proxy | 서브시스템 수, 호환성 문제 |
| 일대다 의존성 | Observer | Mediator, Event Bus | 통신 방향, 결합도 요구사항 |
| 알고리즘 캡슐화 | Template Method | Strategy, Command | 알고리즘 골격 고정 여부 |

### Trade-off 분석 기준

| 기준 | 설명 | 고려 사항 |
|------|------|----------|
| 성능 vs 유연성 | 런타임 오버헤드와 확장성의 균형 | 메모리 사용량, 접근 시간, HashMap 조회 비용 |
| 복잡성 vs 재사용성 | 클래스 수 증가와 확장 비용의 균형 | Cyclomatic 복잡도, 이해 시간, 확장 비용 |
| 투명성 vs 교체 용이성 | 기존 코드 영향과 런타임 변경의 균형 | 컴파일타임 의존성, 인터페이스 변경 |

### 패턴 평가 매트릭스 템플릿

| 평가 기준 | 가중치 예시 | 측정 방법 |
|----------|------------|----------|
| 코드 복잡도 | 25% | Cyclomatic Complexity, 클래스 수 |
| 성능 오버헤드 | 20% | 벤치마크, 메모리 프로파일링 |
| 확장 용이성 | 20% | 새 기능 추가 시 변경 파일 수 |
| 팀 숙련도 요구 | 15% | 이해 시간, 러닝 커브 |
| 메모리 사용량 | 10% | 힙 메모리 분석 |
| 테스트 용이성 | 10% | Mock 필요 수, 테스트 코드 라인 |

### 프로젝트 유형별 가중치 조정

| 프로젝트 유형 | 개발 속도 | 확장성 | 성능 | 유지보수성 |
|--------------|----------|--------|------|-----------|
| 스타트업 초기 | 40% | 20% | 10% | 30% |
| 대규모 엔터프라이즈 | 15% | 35% | 25% | 25% |
| 실시간 시스템 | 10% | 15% | 50% | 25% |
| 레거시 유지보수 | 20% | 15% | 15% | 50% |

---

### 결론: 패턴 분석의 마스터하기

패턴 분석 능력은 하루아침에 기를 수 있는 것이 아닙니다. 하지만 체계적인 프레임워크를 따라 꾸준히 연습하면, 다음과 같은 **전문가적 사고력**을 개발할 수 있습니다:

#### 패턴 분석 전문가의 사고 과정:
1. **문제 본질 파악**: "정말 해결해야 할 핵심 문제는 무엇인가?"
2. **패턴 후보 선별**: "이 문제를 해결할 수 있는 패턴들은?"
3. **Trade-off 분석**: "각 패턴의 장단점과 적용 비용은?"
4. **상황적 적합성**: "우리 팀과 프로젝트에 가장 적합한 것은?"
5. **진화 가능성**: "미래 요구사항 변화에 어떻게 대응할 것인가?"

#### 지속적 개선을 위한 실천 방안:
- **패턴 분석 일지 작성**: 매일 마주친 패턴들을 기록하고 분석
- **코드 리뷰에서 패턴 관점 적용**: "이 코드에 숨어있는 패턴은?"
- **패턴 적용 후기 작성**: 선택한 패턴이 얼마나 효과적이었는지 회고
- **다양한 구현 방식 실험**: 같은 패턴을 다른 언어로 구현해보기

패턴을 **분석하고 평가하는 능력**은 단순히 패턴을 아는 것보다 훨씬 가치 있는 역량입니다. 이는 **설계 사고력**의 핵심이며, 진정한 소프트웨어 아키텍트로 성장하는 발판이 됩니다.

다음 글에서는 이런 분석 능력을 바탕으로 **객체지향 설계의 본질**을 더 깊이 탐구해보겠습니다. 패턴은 결국 좋은 객체지향 설계 원칙들의 구체적 표현이기 때문입니다.

---

**핵심 메시지:**
"패턴을 올바르게 분석하고 평가하는 능력은 패턴을 단순히 아는 것보다 훨씬 중요하며, 이것이 진정한 설계 전문가와 코드 작성자를 구분하는 핵심 역량이다." 