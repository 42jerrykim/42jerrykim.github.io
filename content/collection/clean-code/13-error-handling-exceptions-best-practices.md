---
draft: true
---
# 7장: 오류 처리

## 강의 목표
- 깨끗한 오류 처리 기법 습득
- 예외와 오류 코드의 적절한 사용법 이해
- 안정적이고 유지보수 가능한 오류 처리 구조 설계 능력 개발

## 내용 구성 전략

### 오류 코드보다 예외를 사용하라
**접근 방법**:
- 오류 코드와 예외 처리 방식의 차이점 분석
- 코드 가독성과 유지보수성 관점에서의 비교

**주요 내용**:
- 오류 코드를 사용하면 호출자 코드가 복잡해진다
- 함수를 호출한 즉시 오류를 확인해야 하기 때문에 이 단계를 잊어버리기 쉽다
- 예외를 던지면 호출자 코드가 더 깔끔해진다
- 논리가 오류 처리 코드와 뒤섞이지 않는다

**비교 예시**:
```java
// Bad: 오류 코드 사용
public class DeviceController {
    public void sendShutDown() {
        DeviceHandle handle = getHandle(DEV1);
        // 디바이스 상태를 점검한다.
        if (handle != DeviceHandle.INVALID) {
            // 레코드 필드에 디바이스 상태를 저장한다.
            retrieveDeviceRecord(handle);
            // 디바이스가 일시정지 상태가 아니라면 종료한다.
            if (record.getStatus() != DEVICE_SUSPENDED) {
                pauseDevice(handle);
                clearDeviceWorkQueue(handle);
                closeDevice(handle);
            } else {
                logger.log("Device suspended. Unable to shut down");
            }
        } else {
            logger.log("Invalid handle for: " + DEV1.toString());
        }
    }
}

// Good: 예외 사용
public class DeviceController {
    public void sendShutDown() {
        try {
            tryToShutDown();
        } catch (DeviceShutDownError e) {
            logger.log(e);
        }
    }
    
    private void tryToShutDown() throws DeviceShutDownError {
        DeviceHandle handle = getHandle(DEV1);
        DeviceRecord record = retrieveDeviceRecord(handle);
        
        pauseDevice(handle);
        clearDeviceWorkQueue(handle);
        closeDevice(handle);
    }
    
    private DeviceHandle getHandle(DeviceID id) {
        // ...
        throw new DeviceShutDownError("Invalid handle for: " + id.toString());
    }
}
```

### Try-Catch-Finally 문부터 작성하라
**접근 방법**:
- TDD 관점에서의 예외 처리 구현
- 예외 안전성을 고려한 코드 작성

**주요 내용**:
- try 블록은 트랜잭션과 비슷하다
- try 블록에서 무슨 일이 생기든지 catch 블록은 프로그램 상태를 일관성 있게 유지해야 한다
- 예외가 발생할 코드를 짤 때는 try-catch-finally 문으로 시작하는 편이 낫다

**TDD 예시**:
```java
// 1단계: 실패하는 테스트 작성
@Test(expected = StorageException.class)
public void retrieveSectionShouldThrowOnInvalidFileName() {
    sectionStore.retrieveSection("invalid - file");
}

// 2단계: 예외를 던지는 코드 작성
public List<RecordedGrip> retrieveSection(String sectionName) {
    try {
        FileInputStream stream = new FileInputStream(sectionName);
    } catch (Exception e) {
        throw new StorageException("retrieval error", e);
    }
    return new ArrayList<RecordedGrip>();
}

// 3단계: 테스트를 통과하도록 코드 개선
public List<RecordedGrip> retrieveSection(String sectionName) {
    try {
        FileInputStream stream = new FileInputStream(sectionName);
        stream.close();
    } catch (FileNotFoundException e) {
        throw new StorageException("retrieval error", e);
    }
    return new ArrayList<RecordedGrip>();
}
```

### 미확인(unchecked) 예외를 사용하라
**접근 방법**:
- Checked vs Unchecked 예외의 장단점 분석
- 현대적 언어들의 예외 처리 경향

**주요 내용**:
- 확인된 예외는 OCP(Open Closed Principle)를 위반한다
- 메서드에서 확인된 예외를 던졌는데 catch 블록이 세 단계 위에 있다면 그 사이 메서드 모두가 선언부에 해당 예외를 정의해야 한다
- 이는 캡슐화를 깨뜨린다
- 아주 중요한 라이브러리를 작성한다면 모든 예외를 잡아야 한다
- 하지만 일반적인 애플리케이션은 의존성이라는 비용이 이익보다 크다

### 예외에 의미를 제공하라
**접근 방법**:
- 예외 메시지의 중요성과 작성 방법
- 디버깅을 위한 충분한 정보 제공

**주요 내용**:
- 예외를 던질 때는 전후 상황을 충분히 덧붙인다
- 오류 메시지에 정보를 담아 예외와 함께 던진다
- 실패한 연산 이름과 실패 유형도 언급한다
- 애플리케이션이 로깅 기능을 사용한다면 catch 블록에서 오류를 기록하도록 충분한 정보를 넘겨준다

**개선 예시**:
```java
// Bad: 의미 없는 예외
throw new Exception("Error occurred");

// Good: 의미 있는 예외
throw new InsufficientFundsException(
    "Account " + accountId + " has insufficient funds. " +
    "Current balance: " + currentBalance + 
    ", Requested amount: " + requestedAmount
);
```

### 호출자를 고려해 예외 클래스를 정의하라
**접근 방법**:
- 예외 분류의 다양한 방법
- 호출하는 라이브러리 API를 감싸는 기법

**주요 내용**:
- 오류를 분류하는 방법은 수없이 많다
- 오류를 정의할 때 프로그래머에게 가장 중요한 관심사는 **오류를 잡아내는 방법**이다
- 외부 API를 감싸면 외부 라이브러리와 프로그램 사이의 의존성이 크게 줄어든다

**Wrapper 패턴 예시**:
```java
// Bad: 외부 라이브러리 예외를 그대로 사용
ACMEPort port = new ACMEPort(12);

try {
    port.open();
} catch (DeviceResponseException e) {
    reportPortError(e);
    logger.log("Device response exception", e);
} catch (ATM1212UnlockedException e) {
    reportPortError(e);
    logger.log("Unlock exception", e);
} catch (GMXError e) {
    reportPortError(e);
    logger.log("Device response exception");
} finally {
    // ...
}

// Good: Wrapper 클래스를 사용해 예외 단순화
LocalPort port = new LocalPort(12);
try {
    port.open();
} catch (PortDeviceFailure e) {
    reportError(e);
    logger.log(e.getMessage(), e);
} finally {
    // ...
}

public class LocalPort {
    private ACMEPort innerPort;
    
    public LocalPort(int portNumber) {
        innerPort = new ACMEPort(portNumber);
    }
    
    public void open() {
        try {
            innerPort.open();
        } catch (DeviceResponseException e) {
            throw new PortDeviceFailure(e);
        } catch (ATM1212UnlockedException e) {
            throw new PortDeviceFailure(e);
        } catch (GMXError e) {
            throw new PortDeviceFailure(e);
        }
    }
    // ...
}
```

### 정상 흐름을 정의하라
**접근 방법**:
- Special Case Pattern 적용
- 예외 상황을 정상 흐름으로 처리하는 기법

**주요 내용**:
- 때로는 중단이 적합하지 않은 때도 있다
- 예외적인 상황을 캡슐화해서 처리하면 클라이언트 코드가 예외적인 상황을 처리할 필요가 없어진다

**Special Case Pattern 예시**:
```java
// Bad: 예외로 제어 흐름 처리
try {
    MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
    m_total += expenses.getTotal();
} catch (MealExpensesNotFound e) {
    m_total += getMealPerDiem();
}

// Good: Special Case Pattern 적용
MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
m_total += expenses.getTotal();

public class PerDiemMealExpenses implements MealExpenses {
    public int getTotal() {
        // 기본값을 반환한다.
        return getMealPerDiem();
    }
}
```

### null을 반환하지 마라
**접근 방법**:
- null 반환의 문제점과 대안 제시
- Optional 패턴 등 현대적 해결책

**주요 내용**:
- null을 반환하는 코드는 일거리를 늘릴 뿐만 아니라 호출자에게 문제를 떠넘긴다
- 메서드에서 null을 반환하고픈 유혹이 든다면 그 대신 예외를 던지거나 특수 사례 객체를 반환한다
- 사용하려는 외부 API가 null을 반환한다면 감싸기 메서드를 구현해 예외를 던지거나 특수 사례 객체를 반환하는 방식을 고려한다

**개선 예시**:
```java
// Bad: null 반환
public List<Employee> getEmployees() {
    if (.. there are no employees ..) {
        return null;
    }
    // 직원들을 반환
}

// 호출자가 null 체크를 해야 함
List<Employee> employees = getEmployees();
if (employees != null) {
    for (Employee e : employees) {
        totalPay += e.getPay();
    }
}

// Good: 빈 리스트 반환
public List<Employee> getEmployees() {
    if (.. there are no employees ..) {
        return Collections.emptyList();
    }
    // 직원들을 반환
}

// 호출자가 null 체크를 할 필요 없음
List<Employee> employees = getEmployees();
for (Employee e : employees) {
    totalPay += e.getPay();
}
```

### null을 전달하지 마라
**접근 방법**:
- 메서드 인수로 null을 전달하는 것의 위험성
- null 방어 코드의 문제점

**주요 내용**:
- 메서드에서 null을 반환하는 방식도 나쁘지만 메서드로 null을 전달하는 방식은 더 나쁘다
- 정상적인 인수로 null을 기대하는 API가 아니라면 메서드로 null을 전달하는 코드는 최대한 피한다
- 인수로 null이 넘어오면 코드에 문제가 있다는 말이다

**null 전달 문제 예시**:
```java
// Bad: null 전달 가능성
public class MetricsCalculator {
    public double xProjection(Point p1, Point p2) {
        return (p2.x – p1.x) * 1.5;
    }
}

// 호출: calculator.xProjection(null, new Point(12, 13));
// 결과: NullPointerException

// Better: null 체크 추가
public double xProjection(Point p1, Point p2) {
    if (p1 == null || p2 == null) {
        throw new InvalidArgumentException("Invalid argument for MetricsCalculator.xProjection");
    }
    return (p2.x – p1.x) * 1.5;
}

// Best: 애초에 null을 전달하지 못하도록 설계
// 파라미터 검증, 불변 객체 사용, Optional 활용 등
```

### 결론
**접근 방법**:
- 깨끗한 코드에서 오류 처리의 역할
- 견고한 소프트웨어 개발을 위한 원칙

**주요 내용**:
- 깨끗한 코드는 읽기도 좋아야 하지만 안정성도 높아야 한다
- 이 둘은 상충하는 목표가 아니다
- 오류 처리를 프로그램 논리와 분리해 독자적인 사안으로 고려하면 튼튼하고 깨끗한 코드를 작성할 수 있다

## 강의 진행 방식
1. **도입 (10분)**: 나쁜 오류 처리 경험 사례 공유
2. **이론 (25분)**: 예외 처리 원칙과 패턴 설명
3. **실습 (40분)**: 오류 코드를 예외 처리로 리팩토링
4. **토론 (15분)**: 프로젝트별 오류 처리 전략 수립

## 실습 과제
1. **오류 처리 리팩토링**: 오류 코드 기반 코드를 예외 처리로 변환
2. **예외 클래스 설계**: 프로젝트에 적합한 예외 계층 구조 설계
3. **Wrapper 클래스 구현**: 외부 라이브러리 예외를 감싸는 클래스 작성

## 평가 기준
- 예외 처리 원칙 이해도 (30%)
- 적절한 예외 설계 능력 (35%)
- null 처리 개선 능력 (35%)

## 오류 처리 체크리스트
- [ ] 오류 코드 대신 예외를 사용하는가?
- [ ] Try-Catch-Finally 구조가 명확한가?
- [ ] 미확인 예외를 적절히 활용하는가?
- [ ] 예외 메시지가 충분한 정보를 제공하는가?
- [ ] 외부 API 예외를 적절히 감쌌는가?
- [ ] null 반환을 피하고 있는가?
- [ ] null 전달을 방지하고 있는가?
- [ ] 오류 처리 코드가 비즈니스 로직을 가리지 않는가?

## 추가 자료
- "Effective Java" - 예외 처리 관련 아이템들
- "Clean Architecture" - 경계에서의 오류 처리
- Java Optional, Rust Result 타입 등 현대적 오류 처리 방법
- 함수형 프로그래밍의 Either/Try 모나드 