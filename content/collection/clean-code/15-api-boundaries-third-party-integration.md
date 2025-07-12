---
draft: true
---
# 8장: 경계

## 강의 목표
- 외부 코드와 내부 코드 사이의 경계 관리 방법 습득
- 서드파티 라이브러리 활용 시 안전한 통합 기법 학습
- 학습 테스트와 어댑터 패턴을 통한 경계 관리 능력 개발

## 내용 구성 전략

### 8.1 외부 코드 사용하기
**접근 방법**:
- 인터페이스 제공자와 인터페이스 사용자의 서로 다른 관점 분석
- Map과 같은 범용 인터페이스의 사용 방법

**주요 내용**:
- 패키지 제공자나 프레임워크 제공자는 적용성을 최대한 넓히려 애쓴다
- 사용자는 자신의 요구에 집중하는 인터페이스를 바란다
- 이런 긴장으로 인해 시스템 경계에서 문제가 생길 소지가 많다

**Map 사용 예시**:
```java
// Bad: Map을 그대로 사용
Map sensors = new HashMap();
Sensor s = (Sensor)sensors.get(sensorId);

// Better: 제네릭 사용
Map<String, Sensor> sensors = new HashMap<Sensor>();
Sensor s = sensors.get(sensorId);

// Best: Map을 감싸는 클래스 생성
public class Sensors {
    private Map sensors = new HashMap();
    
    public Sensor getById(String id) {
        return (Sensor) sensors.get(id);
    }
    
    // 이하 Sensor와 관련된 비즈니스 규칙이 들어간다.
}
```

### 8.2 경계 살피고 익히기
**접근 방법**:
- 서드파티 코드를 사용하기 전의 학습 과정
- 실험을 통한 이해와 검증

**주요 내용**:
- 서드파티 패키지 테스트가 우리 책임은 아니다
- 하지만 우리 자신을 위해 우리가 사용할 코드를 테스트하는 편이 바람직하다
- 곧바로 우리쪽 코드를 작성해 외부 코드를 호출하는 대신 먼저 간단한 테스트 케이스를 작성해 외부 코드를 익힌다

**학습 접근법**:
1. 문서를 읽으며 사용법을 결정한다
2. 우리쪽 코드를 작성해 라이브러리가 예상대로 동작하는지 확인한다
3. 라이브러리를 이해한다. 다음 기능을 구현한다. 다시 문제에 부딪힌다

### 8.3 log4j 익히기
**접근 방법**:
- 실제 라이브러리(log4j)를 학습하는 과정을 단계별로 설명
- 학습 테스트의 실제 적용 사례

**주요 내용**:
- 로깅 기능을 직접 구현하는 대신 아파치의 log4j 패키지 사용 결정
- 패키지를 다운받아 소개 페이지를 연다

**학습 테스트 과정**:
```java
// 1단계: 첫 번째 테스트 케이스
@Test
public void testLogCreate() {
    Logger logger = Logger.getLogger("MyLogger");
    logger.info("hello");
}

// 실행 결과: log4j:WARN No appenders could be found for logger (MyLogger).

// 2단계: Appender 추가
@Test  
public void testLogAddAppender() {
    Logger logger = Logger.getLogger("MyLogger");
    ConsoleAppender appender = new ConsoleAppender();
    logger.addAppender(appender);
    logger.info("hello");
}

// 실행 결과: hello

// 3단계: PatternLayout 추가
@Test
public void testLogAddAppender() {
    Logger logger = Logger.getLogger("MyLogger");
    logger.removeAllAppenders();
    logger.addAppender(new ConsoleAppender(
        new PatternLayout("%p %t %m%n"),
        ConsoleAppender.SYSTEM_OUT));
    logger.info("hello");
}

// 실행 결과: INFO main hello
```

**최종 LogTest 클래스**:
```java
public class LogTest {
    private Logger logger;
    
    @Before
    public void initialize() {
        logger = Logger.getLogger("logger");
        logger.removeAllAppenders();
        Logger.getRootLogger().removeAllAppenders();
    }
    
    @Test
    public void basicLogger() {
        BasicConfigurator.configure();
        logger.info("basicLogger");
    }
    
    @Test
    public void addAppenderWithStream() {
        logger.addAppender(new ConsoleAppender(
            new PatternLayout("%p %t %m%n"), 
            ConsoleAppender.SYSTEM_OUT));
        logger.info("addAppenderWithStream");
    }
    
    @Test
    public void addAppenderWithoutStream() {
        logger.addAppender(new ConsoleAppender(
            new PatternLayout("%p %t %m%n")));
        logger.info("addAppenderWithoutStream");
    }
}
```

### 8.4 학습 테스트는 공짜 이상이다
**접근 방법**:
- 학습 테스트의 투자 대비 효과 분석
- 패키지 업그레이드 시의 이점

**주요 내용**:
- 학습 테스트에 드는 비용은 없다. 어차피 API를 배워야 하기 때문이다
- 오히려 필요한 지식만 확보하는 손쉬운 방법이다
- 학습 테스트는 패키지가 예상대로 도는지 검증한다
- 패키지 작성자에게는 코드를 변경할 이유가 생긴다. 그들은 사용자가 코드를 사용하는 방식에 신경 쓸 이유가 없다
- 학습 테스트를 이용한 학습이 필요하다. 그렇지 않으면 낡은 버전을 필요 이상으로 오랫동안 사용하려는 유혹에 빠지기 쉽다

**학습 테스트의 장점**:
1. **공짜**: 어차피 API를 배워야 한다
2. **투자**: 패키지의 새 버전이 나온다면 학습 테스트를 돌려서 차이가 있는지 확인한다
3. **신뢰**: 패키지 작성자에게 코드를 변경할 이유가 생긴다

### 8.5 아직 존재하지 않는 코드를 사용하기
**접근 방법**:
- 개발 중인 시스템에서 아직 구현되지 않은 부분을 다루는 방법
- 어댑터 패턴을 통한 경계 관리

**주요 내용**:
- 경계와 관련해 또 다른 유형은 아는 코드와 모르는 코드를 분리하는 경계다
- 때로는 우리 지식이 경계를 너머 미치지 못하는 코드 영역도 있다
- 때로는 (적어도 지금은) 알려고 해도 알 수가 없다. 때로는 더 이상 내다보지 않기로 결정한다

**실제 사례 - 송신기 시스템**:
```java
// 문제: Transmitter API가 아직 설계되지 않은 상황

// 해결책 1: 우리가 바라는 인터페이스를 정의
public interface Transmitter {
    public void transmit(SomeType frequency, OtherType stream);
}

// 해결책 2: FakeTransmitter 구현으로 테스트
public class FakeTransmitter implements Transmitter {
    public void transmit(SomeType frequency, OtherType stream) {
        // 실제 구현이 나올 때까지 임시 구현
    }
}

// 해결책 3: 실제 API가 나오면 어댑터 구현
public class TransmitterAdapter implements Transmitter {
    private RealTransmitterAPI api;
    
    public TransmitterAdapter(RealTransmitterAPI api) {
        this.api = api;
    }
    
    public void transmit(SomeType frequency, OtherType stream) {
        // RealTransmitterAPI를 우리 인터페이스에 맞게 변환
        api.doTransmission(convertFrequency(frequency), convertStream(stream));
    }
}
```

### 8.6 깨끗한 경계
**접근 방법**:
- 경계 관리의 핵심 원칙
- 변경에 대한 대응력 향상

**주요 내용**:
- 소프트웨어 설계가 우수하다면 변경하는데 많은 투자와 재작업이 필요하지 않다
- 통제가 불가능한 외부 패키지에 의존하는 대신 통제가 가능한 우리 코드에 의존하는 편이 훨씬 좋다
- 외부 패키지를 호출하는 코드를 가능한 줄여 경계를 관리하자
- Map에서 봤듯이, 새로운 클래스로 경계를 감싸거나 ADAPTER 패턴을 사용해 우리가 원하는 인터페이스를 패키지가 제공하는 인터페이스로 변환하자

**경계 관리 전략**:
1. **패키지를 감싸거나 어댑터를 사용해 우리가 원하는 인터페이스를 패키지가 제공하는 인터페이스로 변환**
2. **어느 방법이든 코드 가독성이 높아지며, 경계 인터페이스를 사용하는 일관성도 높아지며, 외부 패키지가 변했을 때 변경할 코드도 줄어든다**

**어댑터 패턴 구현**:
```java
// 외부 라이브러리 인터페이스
public class ExternalLibrary {
    public void complexMethod(String param1, int param2, boolean param3) {
        // 복잡한 외부 라이브러리 로직
    }
}

// 우리가 원하는 간단한 인터페이스
public interface SimpleInterface {
    void doWork(WorkData data);
}

// 어댑터 클래스
public class ExternalLibraryAdapter implements SimpleInterface {
    private ExternalLibrary externalLib;
    
    public ExternalLibraryAdapter() {
        this.externalLib = new ExternalLibrary();
    }
    
    @Override
    public void doWork(WorkData data) {
        // 우리 데이터를 외부 라이브러리 형식으로 변환
        String param1 = data.getName();
        int param2 = data.getCount();
        boolean param3 = data.isEnabled();
        
        externalLib.complexMethod(param1, param2, param3);
    }
}

// 클라이언트 코드
public class BusinessLogic {
    private SimpleInterface worker;
    
    public BusinessLogic(SimpleInterface worker) {
        this.worker = worker;
    }
    
    public void processWork(WorkData data) {
        // 비즈니스 로직에 집중할 수 있음
        validateData(data);
        worker.doWork(data);
        logResult(data);
    }
}
```

## 강의 진행 방식
1. **도입 (10분)**: 서드파티 라이브러리 통합 경험 공유
2. **이론 (25분)**: 경계 관리 원칙과 패턴 설명
3. **실습 (40분)**: 실제 라이브러리를 사용한 학습 테스트 작성
4. **토론 (15분)**: 프로젝트에서의 경계 관리 전략 수립

## 실습 과제
1. **학습 테스트 작성**: 새로운 라이브러리에 대한 학습 테스트 케이스 작성
2. **어댑터 패턴 구현**: 외부 API를 감싸는 어댑터 클래스 구현
3. **경계 인터페이스 설계**: 아직 구현되지 않은 모듈에 대한 인터페이스 설계

## 평가 기준
- 학습 테스트 작성 능력 (35%)
- 어댑터 패턴 구현 능력 (35%)
- 경계 관리 전략 수립 능력 (30%)

## 경계 관리 체크리스트
- [ ] 외부 코드를 직접 사용하지 않고 감쌌는가?
- [ ] 학습 테스트를 작성했는가?
- [ ] 인터페이스가 우리 요구사항에 맞게 설계되었는가?
- [ ] 외부 라이브러리 변경에 대한 영향도가 최소화되었는가?
- [ ] 비즈니스 로직이 외부 의존성으로부터 분리되었는가?
- [ ] 어댑터나 파사드 패턴이 적절히 사용되었는가?
- [ ] 경계에서의 데이터 변환이 명확하게 처리되었는가?

## 경계 관리 패턴
### 1. 어댑터 패턴 (Adapter Pattern)
- **사용 시기**: 외부 인터페이스가 우리 요구사항과 맞지 않을 때
- **장점**: 외부 라이브러리 변경에 대한 보호
- **단점**: 추가적인 추상화 레이어

### 2. 파사드 패턴 (Facade Pattern)  
- **사용 시기**: 복잡한 외부 시스템을 단순하게 사용하고 싶을 때
- **장점**: 사용법 단순화, 의존성 감소
- **단점**: 기능 제한 가능성

### 3. 래퍼 패턴 (Wrapper Pattern)
- **사용 시기**: 외부 코드의 사용법을 제한하고 싶을 때
- **장점**: 안전성 향상, 일관된 사용법
- **단점**: 성능 오버헤드

## 추가 자료
- Gang of Four "Design Patterns" - Adapter, Facade 패턴
- "Patterns of Enterprise Application Architecture" - Gateway 패턴
- Hexagonal Architecture (Ports and Adapters)
- 마이크로서비스에서의 Anti-Corruption Layer 패턴 