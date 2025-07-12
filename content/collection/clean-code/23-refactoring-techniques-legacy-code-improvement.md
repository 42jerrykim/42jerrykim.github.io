---
draft: true
---
# 14장: 리팩토링 실습

## 강의 목표
- 점진적 개선을 통한 리팩토링 기법 습득
- 실제 코드 예제를 통한 리팩토링 과정 체험
- 지속적인 코드 개선의 중요성과 방법론 이해
- 대규모 리팩토링 프로젝트 관리 능력 개발

## 내용 구성 전략

### 14.1 점진적 개선
**접근 방법**:
- 큰 변화를 작은 단계로 나누는 전략
- 각 단계에서 테스트를 통한 검증
- 기능 유지와 코드 개선의 균형

**주요 내용**:
- 프로그램을 망치는 가장 좋은 방법 중 하나는 개선이라는 이름 아래 구조를 크게 뒤바꾸는 행위다
- 그래서 TDD(Test Driven Development)라는 기법을 사용한다
- TDD는 언제 어느 때라도 시스템이 돌아가야 한다는 원칙을 따른다
- 변경을 가한 후에도 시스템이 변경 전과 똑같이 돌아가야 한다

**점진적 개선의 원칙**:
```java
// 리팩토링 전략: 한 번에 하나씩 변경
// 1단계: 기존 코드 이해
// 2단계: 테스트 코드 작성
// 3단계: 작은 변경 수행
// 4단계: 테스트 실행
// 5단계: 다음 변경으로 진행
```

### 14.2 Args 구현 사례
**접근 방법**:
- 명령행 인수 파싱 프로그램의 진화 과정
- 기능 추가에 따른 코드 복잡도 증가 문제
- 체계적인 리팩토링을 통한 해결

**초기 구현 - 문제가 있는 코드**:
```java
// Bad: 기능이 추가될수록 복잡해지는 Args 클래스
public class Args {
    private Map<Character, ArgumentMarshaler> marshalers;
    private Set<Character> argsFound;
    private ListIterator<String> currentArgument;
    
    public Args(String schema, String[] args) throws ArgsException {
        marshalers = new HashMap<Character, ArgumentMarshaler>();
        argsFound = new HashSet<Character>();
        
        parseSchema(schema);
        parseArgumentStrings(Arrays.asList(args));
    }
    
    // 100여 줄의 복잡한 메서드들...
    private void parseSchema(String schema) throws ArgsException {
        for (String element : schema.split(","))
            if (element.length() > 0)
                parseSchemaElement(element.trim());
    }
    
    private void parseSchemaElement(String element) throws ArgsException {
        char elementId = element.charAt(0);
        String elementTail = element.substring(1);
        validateSchemaElementId(elementId);
        
        if (elementTail.length() == 0)
            marshalers.put(elementId, new BooleanArgumentMarshaler());
        else if (elementTail.equals("*"))
            marshalers.put(elementId, new StringArgumentMarshaler());
        else if (elementTail.equals("#"))
            marshalers.put(elementId, new IntegerArgumentMarshaler());
        else if (elementTail.equals("##"))
            marshalers.put(elementId, new DoubleArgumentMarshaler());
        else if (elementTail.equals("[*]"))
            marshalers.put(elementId, new StringArrayArgumentMarshaler());
        else
            throw new ArgsException(INVALID_ARGUMENT_FORMAT, elementId, elementTail);
    }
    
    // 더 많은 복잡한 메서드들...
}
```

**리팩토링된 구현 - 개선된 코드**:
```java
// Good: 책임이 분리된 깔끔한 Args 클래스
public class Args {
    private Map<Character, ArgumentMarshaler> marshalers;
    private Set<Character> argsFound;
    private ListIterator<String> currentArgument;
    
    public Args(String schema, String[] args) throws ArgsException {
        marshalers = new HashMap<Character, ArgumentMarshaler>();
        argsFound = new HashSet<Character>();
        
        parseSchema(schema);
        parseArgumentStrings(Arrays.asList(args));
    }
    
    private void parseSchema(String schema) throws ArgsException {
        for (String element : schema.split(","))
            if (element.length() > 0)
                parseSchemaElement(element.trim());
    }
    
    private void parseSchemaElement(String element) throws ArgsException {
        char elementId = element.charAt(0);
        String elementTail = element.substring(1);
        validateSchemaElementId(elementId);
        
        ArgumentMarshaler marshaler = marshalerForElement(elementTail);
        marshalers.put(elementId, marshaler);
    }
    
    private ArgumentMarshaler marshalerForElement(String elementTail) throws ArgsException {
        if (elementTail.length() == 0)
            return new BooleanArgumentMarshaler();
        else if (elementTail.equals("*"))
            return new StringArgumentMarshaler();
        else if (elementTail.equals("#"))
            return new IntegerArgumentMarshaler();
        else if (elementTail.equals("##"))
            return new DoubleArgumentMarshaler();
        else if (elementTail.equals("[*]"))
            return new StringArrayArgumentMarshaler();
        else
            throw new ArgsException(INVALID_ARGUMENT_FORMAT, 
                                  elementTail.charAt(0), elementTail);
    }
    
    // 각 타입별 Marshaler 클래스로 책임 분리
}

// ArgumentMarshaler 인터페이스
public interface ArgumentMarshaler {
    void set(Iterator<String> currentArgument) throws ArgsException;
}

// 구체적인 Marshaler 구현체들
public class BooleanArgumentMarshaler implements ArgumentMarshaler {
    private boolean booleanValue = false;
    
    public void set(Iterator<String> currentArgument) throws ArgsException {
        booleanValue = true;
    }
    
    public static boolean getValue(ArgumentMarshaler am) {
        if (am != null && am instanceof BooleanArgumentMarshaler)
            return ((BooleanArgumentMarshaler) am).booleanValue;
        else
            return false;
    }
}

public class StringArgumentMarshaler implements ArgumentMarshaler {
    private String stringValue = "";
    
    public void set(Iterator<String> currentArgument) throws ArgsException {
        try {
            stringValue = currentArgument.next();
        } catch (NoSuchElementException e) {
            throw new ArgsException(MISSING_STRING);
        }
    }
    
    public static String getValue(ArgumentMarshaler am) {
        if (am != null && am instanceof StringArgumentMarshaler)
            return ((StringArgumentMarshaler) am).stringValue;
        else
            return "";
    }
}
```

### 14.3 리팩토링 과정 단계별 분석
**접근 방법**:
- 각 리팩토링 단계의 목적과 결과
- 변경 시 발생할 수 있는 위험 요소
- 안전한 리팩토링을 위한 전략

**1단계: 기존 시스템 이해**
```java
// 현재 상태 파악
// - 어떤 기능을 수행하는가?
// - 어떤 구조로 되어 있는가?
// - 어떤 부분이 복잡한가?
// - 테스트 커버리지는 어떤가?

public class AnalysisExample {
    // 복잡도 측정
    private void calculateComplexity() {
        // 사이클로매틱 복잡도
        // 메서드 길이
        // 클래스 응집도
        // 결합도 분석
    }
}
```

**2단계: 안전망 구축 (테스트 코드)**
```java
// 기존 동작을 보장하는 테스트 작성
@Test
public void testSimpleFlags() throws Exception {
    Args args = new Args("x,y", new String[]{"-x", "-y"});
    assertTrue(args.getBoolean('x'));
    assertTrue(args.getBoolean('y'));
}

@Test
public void testStringArgument() throws Exception {
    Args args = new Args("x*", new String[]{"-x", "hello"});
    assertEquals("hello", args.getString('x'));
}

@Test
public void testIntegerArgument() throws Exception {
    Args args = new Args("x#", new String[]{"-x", "42"});
    assertEquals(42, args.getInt('x'));
}
```

**3단계: 작은 변경들의 연속**
```java
// 변경 전: 하나의 큰 메서드
public void parseArgumentStrings(List<String> argsList) throws ArgsException {
    for (currentArgument = argsList.listIterator(); currentArgument.hasNext();) {
        String argString = currentArgument.next();
        if (argString.startsWith("-")) {
            parseArgumentCharacters(argString.substring(1));
        } else {
            currentArgument.previous();
            break;
        }
    }
}

// 변경 후: 여러 개의 작은 메서드들
public void parseArgumentStrings(List<String> argsList) throws ArgsException {
    for (currentArgument = argsList.listIterator(); currentArgument.hasNext();) {
        String argString = currentArgument.next();
        if (argString.startsWith("-")) {
            parseArgumentCharacters(argString.substring(1));
        } else {
            handleNonFlagArgument();
            break;
        }
    }
}

private void handleNonFlagArgument() {
    currentArgument.previous();
}

private void parseArgumentCharacters(String argChars) throws ArgsException {
    for (int i = 0; i < argChars.length(); i++)
        parseArgumentCharacter(argChars.charAt(i));
}

private void parseArgumentCharacter(char argChar) throws ArgsException {
    ArgumentMarshaler m = marshalers.get(argChar);
    argsFound.add(argChar);
    if (m == null) {
        throw new ArgsException(UNEXPECTED_ARGUMENT, argChar, null);
    } else {
        m.set(currentArgument);
    }
}
```

### 14.4 리팩토링 원칙과 패턴
**접근 방법**:
- 검증된 리팩토링 기법들
- 각 상황에 적합한 패턴 선택
- 코드 냄새 제거 기법

**주요 리팩토링 패턴**:
```java
// 1. Extract Method (메서드 추출)
// Before
public void printOwing() {
    printBanner();
    
    // print details
    System.out.println("name: " + name);
    System.out.println("amount: " + getOutstanding());
}

// After
public void printOwing() {
    printBanner();
    printDetails(getOutstanding());
}

private void printDetails(double outstanding) {
    System.out.println("name: " + name);
    System.out.println("amount: " + outstanding);
}

// 2. Move Method (메서드 이동)
// Before: 잘못된 클래스에 있는 메서드
public class Account {
    private AccountType type;
    private int daysOverdrawn;
    
    double overdraftCharge() {
        if (type.isPremium()) {
            double result = 10;
            if (daysOverdrawn > 7) result += (daysOverdrawn - 7) * 0.85;
            return result;
        } else {
            return daysOverdrawn * 1.75;
        }
    }
}

// After: 적절한 클래스로 이동
public class Account {
    private AccountType type;
    private int daysOverdrawn;
    
    double overdraftCharge() {
        return type.overdraftCharge(daysOverdrawn);
    }
}

public class AccountType {
    double overdraftCharge(int daysOverdrawn) {
        if (isPremium()) {
            double result = 10;
            if (daysOverdrawn > 7) result += (daysOverdrawn - 7) * 0.85;
            return result;
        } else {
            return daysOverdrawn * 1.75;
        }
    }
}

// 3. Replace Conditional with Polymorphism (조건부를 다형성으로)
// Before
public class Bird {
    public double getSpeed() {
        switch (type) {
            case EUROPEAN:
                return getBaseSpeed();
            case AFRICAN:
                return getBaseSpeed() - getLoadFactor() * numberOfCoconuts;
            case NORWEGIAN_BLUE:
                return (nailed) ? 0 : getBaseSpeed(voltage);
        }
        throw new RuntimeException("Should be unreachable");
    }
}

// After
public abstract class Bird {
    public abstract double getSpeed();
}

public class European extends Bird {
    public double getSpeed() {
        return getBaseSpeed();
    }
}

public class African extends Bird {
    public double getSpeed() {
        return getBaseSpeed() - getLoadFactor() * numberOfCoconuts;
    }
}
```

### 14.5 대규모 리팩토링 전략
**접근 방법**:
- 레거시 시스템의 점진적 개선
- 아키텍처 수준의 리팩토링
- 팀 단위 리팩토링 관리

**주요 내용**:
- 큰 리팩토링은 여러 명이 달려들면 실패할 확률이 높다
- 대신 팀 전체가 합의하에 조금씩 바꿔야 한다
- 모든 변경을 리뷰하고 승인하는 과정이 필요하다

**Strangler Fig 패턴 예시**:
```java
// 기존 레거시 시스템
public class LegacyOrderService {
    public void processOrder(Order order) {
        // 복잡한 레거시 로직
        validateOrderLegacy(order);
        calculatePriceLegacy(order);
        persistOrderLegacy(order);
        sendNotificationLegacy(order);
    }
}

// 새로운 시스템으로 점진적 이관
public class OrderService {
    private LegacyOrderService legacyService;
    private NewOrderValidator validator;
    private NewPriceCalculator calculator;
    
    public void processOrder(Order order) {
        // 단계적으로 새 시스템으로 교체
        if (useNewValidation(order)) {
            validator.validate(order);
        } else {
            legacyService.validateOrderLegacy(order);
        }
        
        if (useNewPricing(order)) {
            calculator.calculatePrice(order);
        } else {
            legacyService.calculatePriceLegacy(order);
        }
        
        // 아직 레거시 사용
        legacyService.persistOrderLegacy(order);
        legacyService.sendNotificationLegacy(order);
    }
    
    private boolean useNewValidation(Order order) {
        // 점진적 롤아웃 로직
        return order.getCustomerType().equals("PREMIUM");
    }
}
```

### 14.6 리팩토링 후 결과 검증
**접근 방법**:
- 성능 측정과 비교
- 코드 품질 지표 개선 확인
- 유지보수성 향상 검증

**측정 지표**:
```java
// 코드 품질 지표 측정
public class CodeQualityMetrics {
    // 1. 사이클로매틱 복잡도
    public int calculateCyclomaticComplexity(Method method) {
        // 분기점 개수 + 1
        return countDecisionPoints(method) + 1;
    }
    
    // 2. 응집도 (LCOM - Lack of Cohesion of Methods)
    public double calculateCohesion(Class clazz) {
        // 메서드 간 공유 인스턴스 변수 비율
        return calculateSharedVariableRatio(clazz);
    }
    
    // 3. 결합도
    public int calculateCoupling(Class clazz) {
        // 다른 클래스와의 의존성 개수
        return countDependencies(clazz);
    }
    
    // 4. 테스트 커버리지
    public double calculateTestCoverage(Package pkg) {
        return (double) coveredLines / totalLines * 100;
    }
}
```

### 14.7 지속적인 리팩토링
**접근 방법**:
- 일상적인 개발 과정에 리팩토링 통합
- 코드 리뷰 과정에서의 리팩토링
- 자동화된 리팩토링 도구 활용

**주요 내용**:
- 리팩토링은 한 번에 끝나는 작업이 아니다
- 보이스카우트 규칙: "캠프장은 처음 왔을 때보다 더 깨끗하게 해놓고 떠나라"
- 코드를 체크인하기 전에 코드가 처음보다 깨끗한지 확인하라

**지속적 리팩토링 체크리스트**:
```java
// 매일 해야 할 리팩토링 활동
public class DailyRefactoringChecklist {
    // 1. 메서드명이 의도를 명확히 드러내는가?
    public void checkMethodNames() {
        // process() -> processPayment()
        // handle() -> handleUserRegistration()
    }
    
    // 2. 매직 넘버를 상수로 교체했는가?
    public void replaceHardcodedValues() {
        // Bad: if (age > 18)
        // Good: if (age > LEGAL_AGE)
        final int LEGAL_AGE = 18;
    }
    
    // 3. 중복 코드를 제거했는가?
    public void removeDuplication() {
        // 동일한 로직이 3번 이상 반복되면 추출
    }
    
    // 4. 긴 메서드를 분할했는가?
    public void splitLongMethods() {
        // 20줄 이상 메서드는 분할 고려
    }
}
```

## 강의 진행 방식
1. **도입 (15분)**: Args 프로그램 초기 버전 소개 및 문제점 분석
2. **이론 (20분)**: 점진적 개선 원칙과 리팩토링 전략 설명
3. **실습 (45분)**: 실제 코드를 단계별로 리팩토링
4. **토론 (10분)**: 리팩토링 경험 공유 및 베스트 프랙티스 논의

## 실습 과제
1. **레거시 코드 리팩토링**: 제공된 복잡한 코드를 단계별로 개선
2. **리팩토링 계획 수립**: 기존 프로젝트의 리팩토링 로드맵 작성
3. **코드 품질 측정**: 리팩토링 전후의 품질 지표 비교 분석

## 평가 기준
- 점진적 개선 과정의 이해도 (25%)
- 적절한 리팩토링 기법 적용 (35%)
- 테스트를 통한 안전성 확보 (25%)
- 코드 품질 개선 결과 (15%)

## 리팩토링 체크리스트
**계획 단계**:
- [ ] 리팩토링 목표가 명확한가?
- [ ] 충분한 테스트 커버리지를 확보했는가?
- [ ] 변경 범위가 적절히 제한되어 있는가?
- [ ] 팀원들과 리팩토링 계획을 공유했는가?

**실행 단계**:
- [ ] 한 번에 하나의 변경만 수행하고 있는가?
- [ ] 각 단계마다 테스트를 실행하고 있는가?
- [ ] 기능 변경과 구조 변경을 분리하고 있는가?
- [ ] 변경 사항을 버전 관리 시스템에 자주 커밋하고 있는가?

**검증 단계**:
- [ ] 모든 테스트가 통과하는가?
- [ ] 성능이 저하되지 않았는가?
- [ ] 코드 품질 지표가 개선되었는가?
- [ ] 다른 팀원이 변경 사항을 이해할 수 있는가?

## 결론
깨끗한 코드를 만들려면 먼저 더러운 코드를 만든 뒤에 정리해야 한다. 이것이 현실이다. 대다수 신참 프로그래머는 이 충고를 충실히 따르지만, 코드를 정리하는 능력은 부족하다. 그런데 코드를 정리하는 능력은 깨끗한 코드를 작성하는 데 필수적이다.

**핵심 원칙**:
1. **점진적 개선**: 큰 변화를 작은 단계로 나누어 진행
2. **테스트 우선**: 모든 변경은 테스트로 검증
3. **지속적 적용**: 일상적인 개발 과정에 리팩토링 통합
4. **팀 차원 접근**: 개인이 아닌 팀 단위의 코드 품질 관리

코드는 한 번 작성되지만 열 번 읽힌다. 그러므로 읽기 쉬운 코드를 만드는 일이 중요하다. 처음부터 완벽한 코드를 작성할 수는 없다. 하지만 지속적인 개선을 통해 깨끗하고 유지보수하기 쉬운 코드로 발전시킬 수 있다.

## 추가 자료
- Martin Fowler, "Refactoring: Improving the Design of Existing Code"
- Robert C. Martin, "Clean Code" - Chapter 14: Successive Refinement
- Joshua Kerievsky, "Refactoring to Patterns"
- 정적 분석 도구: SonarQube, PMD, Checkstyle
- IDE 리팩토링 도구 활용법
- 자동화된 리팩토링과 안전한 변경 관리 