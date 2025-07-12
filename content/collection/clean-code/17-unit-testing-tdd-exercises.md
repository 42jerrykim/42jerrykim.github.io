---
draft: true
---
# Chapter 9: 단위 테스트 - 실습 과제

## 실습 개요
이 실습은 TDD(Test-Driven Development) 방식으로 개발하고, 깨끗한 테스트 코드를 작성하며, F.I.R.S.T 원칙을 적용하는 것을 목표로 합니다.

## 실습 1: TDD 실습 - 계산기 구현 (50분)

### 목표
Red-Green-Refactor 사이클로 간단한 계산기를 구현합니다.

### TDD 사이클
1. **Red**: 실패하는 테스트 작성
2. **Green**: 테스트를 통과하는 최소한의 코드 작성  
3. **Refactor**: 코드를 개선하되 테스트는 계속 통과

### 구현 요구사항

다음 기능을 가진 계산기를 TDD로 구현하세요:

1. **기본 산술 연산**: 덧셈, 뺄셈, 곱셈, 나눗셈
2. **메모리 기능**: 값 저장, 불러오기, 초기화
3. **연산 히스토리**: 최근 10개 연산 기록
4. **예외 처리**: 0으로 나누기, 잘못된 입력 등

### TDD 실습 과정

#### 1단계: 첫 번째 테스트 작성 (Red)

```java
// CalculatorTest.java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {
    
    private Calculator calculator;
    
    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }
    
    @Test
    void shouldReturnZeroWhenCreated() {
        // Given - calculator is created in setUp
        
        // When
        double result = calculator.getCurrentValue();
        
        // Then
        assertEquals(0.0, result);
    }
}
```

**컴파일 실패** → Calculator 클래스 생성 필요

#### 2단계: 테스트를 통과하는 최소 코드 (Green)

```java
// Calculator.java
public class Calculator {
    private double currentValue = 0.0;
    
    public double getCurrentValue() {
        return currentValue;
    }
}
```

**테스트 통과** ✅

#### 3단계: 더 많은 테스트 추가 (Red)

```java
@Test
void shouldAddTwoNumbers() {
    // Given
    calculator.add(5.0);
    
    // When
    calculator.add(3.0);
    
    // Then
    assertEquals(8.0, calculator.getCurrentValue());
}

@Test
void shouldSubtractNumbers() {
    // Given
    calculator.add(10.0);
    
    // When
    calculator.subtract(4.0);
    
    // Then
    assertEquals(6.0, calculator.getCurrentValue());
}
```

#### 4단계: 테스트를 통과하는 코드 구현 (Green)

```java
public class Calculator {
    private double currentValue = 0.0;
    
    public double getCurrentValue() {
        return currentValue;
    }
    
    public void add(double value) {
        currentValue += value;
    }
    
    public void subtract(double value) {
        currentValue -= value;
    }
}
```

#### 5단계: 더 복잡한 기능 추가

```java
// 메모리 기능 테스트
@Test
void shouldStoreValueInMemory() {
    // Given
    calculator.add(42.0);
    
    // When
    calculator.storeInMemory();
    calculator.clear();
    
    // Then
    assertEquals(0.0, calculator.getCurrentValue());
    assertEquals(42.0, calculator.recallFromMemory());
}

// 히스토리 기능 테스트
@Test
void shouldKeepHistoryOfOperations() {
    // Given
    calculator.add(5.0);
    calculator.multiply(2.0);
    calculator.subtract(3.0);
    
    // When
    List<String> history = calculator.getHistory();
    
    // Then
    assertEquals(3, history.size());
    assertTrue(history.contains("ADD 5.0"));
    assertTrue(history.contains("MULTIPLY 2.0"));
    assertTrue(history.contains("SUBTRACT 3.0"));
}

// 예외 처리 테스트
@Test
void shouldThrowExceptionWhenDividingByZero() {
    // Given & When & Then
    assertThrows(ArithmeticException.class, () -> {
        calculator.divide(0.0);
    });
}
```

#### 6단계: 완전한 Calculator 구현

```java
import java.util.ArrayList;
import java.util.List;

public class Calculator {
    private double currentValue = 0.0;
    private double memoryValue = 0.0;
    private final List<String> history = new ArrayList<>();
    private static final int MAX_HISTORY_SIZE = 10;
    
    public double getCurrentValue() {
        return currentValue;
    }
    
    public void add(double value) {
        currentValue += value;
        addToHistory("ADD " + value);
    }
    
    public void subtract(double value) {
        currentValue -= value;
        addToHistory("SUBTRACT " + value);
    }
    
    public void multiply(double value) {
        currentValue *= value;
        addToHistory("MULTIPLY " + value);
    }
    
    public void divide(double value) {
        if (value == 0.0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        currentValue /= value;
        addToHistory("DIVIDE " + value);
    }
    
    public void clear() {
        currentValue = 0.0;
        addToHistory("CLEAR");
    }
    
    public void storeInMemory() {
        memoryValue = currentValue;
        addToHistory("STORE_MEMORY");
    }
    
    public double recallFromMemory() {
        return memoryValue;
    }
    
    public void clearMemory() {
        memoryValue = 0.0;
        addToHistory("CLEAR_MEMORY");
    }
    
    public List<String> getHistory() {
        return new ArrayList<>(history);
    }
    
    public void clearHistory() {
        history.clear();
    }
    
    private void addToHistory(String operation) {
        if (history.size() >= MAX_HISTORY_SIZE) {
            history.remove(0);
        }
        history.add(operation);
    }
}
```

#### 7단계: 리팩토링 (Refactor)

```java
// 개선된 Calculator - 연산을 별도 클래스로 분리
public class Calculator {
    private double currentValue = 0.0;
    private final MemoryStorage memory = new MemoryStorage();
    private final OperationHistory history = new OperationHistory();
    
    public double getCurrentValue() {
        return currentValue;
    }
    
    public Calculator add(double value) {
        currentValue += value;
        history.record(Operation.ADD, value);
        return this;
    }
    
    public Calculator subtract(double value) {
        currentValue -= value;
        history.record(Operation.SUBTRACT, value);
        return this;
    }
    
    public Calculator multiply(double value) {
        currentValue *= value;
        history.record(Operation.MULTIPLY, value);
        return this;
    }
    
    public Calculator divide(double value) {
        if (value == 0.0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        currentValue /= value;
        history.record(Operation.DIVIDE, value);
        return this;
    }
    
    public Calculator clear() {
        currentValue = 0.0;
        history.record(Operation.CLEAR, 0.0);
        return this;
    }
    
    // 메모리 관련 메서드들
    public Calculator storeInMemory() {
        memory.store(currentValue);
        history.record(Operation.STORE_MEMORY, currentValue);
        return this;
    }
    
    public double recallFromMemory() {
        return memory.recall();
    }
    
    // 히스토리 관련 메서드들
    public List<OperationRecord> getHistory() {
        return history.getRecords();
    }
    
    public Calculator clearHistory() {
        history.clear();
        return this;
    }
}

// 보조 클래스들
class MemoryStorage {
    private double value = 0.0;
    
    void store(double value) {
        this.value = value;
    }
    
    double recall() {
        return value;
    }
    
    void clear() {
        value = 0.0;
    }
}

class OperationHistory {
    private final List<OperationRecord> records = new ArrayList<>();
    private static final int MAX_SIZE = 10;
    
    void record(Operation operation, double value) {
        if (records.size() >= MAX_SIZE) {
            records.remove(0);
        }
        records.add(new OperationRecord(operation, value, LocalDateTime.now()));
    }
    
    List<OperationRecord> getRecords() {
        return new ArrayList<>(records);
    }
    
    void clear() {
        records.clear();
    }
}

record OperationRecord(Operation operation, double value, LocalDateTime timestamp) {}

enum Operation {
    ADD, SUBTRACT, MULTIPLY, DIVIDE, CLEAR, STORE_MEMORY, CLEAR_MEMORY
}
```

### TDD 체크리스트
```markdown
## TDD 실습 체크리스트

### Red 단계
- [ ] 실패하는 테스트 작성
- [ ] 컴파일 오류도 실패로 간주
- [ ] 한 번에 하나의 실패하는 테스트만

### Green 단계  
- [ ] 테스트를 통과하는 최소한의 코드
- [ ] 중복 코드나 하드코딩 허용
- [ ] 빠르게 테스트 통과시키기

### Refactor 단계
- [ ] 코드 품질 개선
- [ ] 중복 제거
- [ ] 테스트는 계속 통과해야 함

### 전체 과정
- [ ] 짧은 사이클 유지 (5-10분)
- [ ] 모든 테스트 항상 통과
- [ ] 점진적 기능 추가
```

## 실습 2: 테스트 리팩토링 (30분)

### 목표
지저분한 테스트 코드를 깨끗하게 개선합니다.

### 개선 대상 테스트

```java
// Bad: 지저분한 테스트 코드
public class UserServiceTest {
    
    @Test
    public void test1() {
        UserService userService = new UserService();
        UserRepository userRepository = new UserRepository();
        EmailService emailService = new EmailService();
        userService.setUserRepository(userRepository);
        userService.setEmailService(emailService);
        
        User user = new User();
        user.setName("John Doe");
        user.setEmail("john@example.com");
        user.setAge(25);
        user.setPassword("password123");
        
        User result = userService.createUser(user);
        
        Assert.assertEquals("John Doe", result.getName());
        Assert.assertEquals("john@example.com", result.getEmail());
        Assert.assertEquals(25, result.getAge());
        Assert.assertNotNull(result.getId());
        Assert.assertTrue(result.isActive());
    }
    
    @Test
    public void test2() {
        UserService userService = new UserService();
        UserRepository userRepository = new UserRepository();
        EmailService emailService = new EmailService();
        userService.setUserRepository(userRepository);
        userService.setEmailService(emailService);
        
        User user = new User();
        user.setName("");
        user.setEmail("john@example.com");
        user.setAge(25);
        
        try {
            userService.createUser(user);
            Assert.fail("Should have thrown exception");
        } catch (IllegalArgumentException e) {
            Assert.assertEquals("Name cannot be empty", e.getMessage());
        }
    }
    
    @Test
    public void test3() {
        UserService userService = new UserService();
        UserRepository userRepository = new UserRepository();
        EmailService emailService = new EmailService();
        userService.setUserRepository(userRepository);
        userService.setEmailService(emailService);
        
        User user1 = new User();
        user1.setName("John");
        user1.setEmail("john@example.com");
        user1.setAge(25);
        
        User user2 = new User();
        user2.setName("Jane");
        user2.setEmail("john@example.com"); // 동일한 이메일
        user2.setAge(30);
        
        userService.createUser(user1);
        
        try {
            userService.createUser(user2);
            Assert.fail("Should have thrown exception");
        } catch (IllegalArgumentException e) {
            Assert.assertEquals("Email already exists", e.getMessage());
        }
    }
}
```

### 개선 과제

다음 원칙을 적용하여 테스트를 개선하세요:

1. **명확한 테스트 이름**: 테스트의 의도가 드러나는 이름
2. **Given-When-Then 구조**: 명확한 테스트 구조
3. **테스트 데이터 빌더**: 테스트 데이터 생성 개선
4. **중복 제거**: 공통 설정 추출

### 개선 결과 템플릿

```java
// Good: 깨끗한 테스트 코드
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private EmailService emailService;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    @DisplayName("유효한 사용자 정보로 사용자를 생성하면 성공한다")
    void shouldCreateUserSuccessfully_WhenValidUserDataProvided() {
        // Given
        User inputUser = createValidUser()
            .withName("John Doe")
            .withEmail("john@example.com")
            .withAge(25)
            .build();
        
        User savedUser = createValidUser()
            .withId(1L)
            .withName("John Doe")
            .withEmail("john@example.com")
            .withAge(25)
            .withActive(true)
            .build();
        
        when(userRepository.existsByEmail("john@example.com")).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        
        // When
        User result = userService.createUser(inputUser);
        
        // Then
        assertThat(result)
            .extracting("id", "name", "email", "age", "active")
            .containsExactly(1L, "John Doe", "john@example.com", 25, true);
        
        verify(emailService).sendWelcomeEmail(result);
    }
    
    @Test
    @DisplayName("이름이 비어있으면 사용자 생성에 실패한다")
    void shouldFailToCreateUser_WhenNameIsEmpty() {
        // Given
        User userWithEmptyName = createValidUser()
            .withName("")
            .build();
        
        // When & Then
        assertThatThrownBy(() -> userService.createUser(userWithEmptyName))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessage("Name cannot be empty");
        
        verifyNoInteractions(userRepository, emailService);
    }
    
    @Test
    @DisplayName("이미 존재하는 이메일로 사용자 생성 시 실패한다")
    void shouldFailToCreateUser_WhenEmailAlreadyExists() {
        // Given
        String duplicateEmail = "existing@example.com";
        User userWithDuplicateEmail = createValidUser()
            .withEmail(duplicateEmail)
            .build();
        
        when(userRepository.existsByEmail(duplicateEmail)).thenReturn(true);
        
        // When & Then
        assertThatThrownBy(() -> userService.createUser(userWithDuplicateEmail))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessage("Email already exists");
        
        verify(userRepository, never()).save(any());
        verifyNoInteractions(emailService);
    }
    
    @Nested
    @DisplayName("사용자 나이 검증")
    class UserAgeValidation {
        
        @ParameterizedTest
        @DisplayName("유효하지 않은 나이로 사용자 생성 시 실패한다")
        @ValueSource(ints = {-1, 0, 17, 151})
        void shouldFailToCreateUser_WhenAgeIsInvalid(int invalidAge) {
            // Given
            User userWithInvalidAge = createValidUser()
                .withAge(invalidAge)
                .build();
            
            // When & Then
            assertThatThrownBy(() -> userService.createUser(userWithInvalidAge))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("Age must be between 18 and 150");
        }
        
        @ParameterizedTest
        @DisplayName("유효한 나이로 사용자 생성 시 성공한다")
        @ValueSource(ints = {18, 25, 65, 150})
        void shouldCreateUserSuccessfully_WhenAgeIsValid(int validAge) {
            // Given
            User userWithValidAge = createValidUser()
                .withAge(validAge)
                .build();
            
            when(userRepository.existsByEmail(any())).thenReturn(false);
            when(userRepository.save(any())).thenReturn(userWithValidAge);
            
            // When
            User result = userService.createUser(userWithValidAge);
            
            // Then
            assertThat(result.getAge()).isEqualTo(validAge);
        }
    }
    
    // 테스트 데이터 빌더
    private UserTestDataBuilder createValidUser() {
        return new UserTestDataBuilder();
    }
    
    private static class UserTestDataBuilder {
        private Long id;
        private String name = "Default Name";
        private String email = "default@example.com";
        private int age = 25;
        private String password = "password123";
        private boolean active = true;
        
        UserTestDataBuilder withId(Long id) {
            this.id = id;
            return this;
        }
        
        UserTestDataBuilder withName(String name) {
            this.name = name;
            return this;
        }
        
        UserTestDataBuilder withEmail(String email) {
            this.email = email;
            return this;
        }
        
        UserTestDataBuilder withAge(int age) {
            this.age = age;
            return this;
        }
        
        UserTestDataBuilder withPassword(String password) {
            this.password = password;
            return this;
        }
        
        UserTestDataBuilder withActive(boolean active) {
            this.active = active;
            return this;
        }
        
        User build() {
            User user = new User();
            user.setId(id);
            user.setName(name);
            user.setEmail(email);
            user.setAge(age);
            user.setPassword(password);
            user.setActive(active);
            return user;
        }
    }
}
```

### 테스트 리팩토링 체크리스트
```markdown
## 테스트 리팩토링 체크리스트

### 테스트 이름
- [ ] 테스트의 의도가 명확히 드러남
- [ ] should_When_Then 패턴 사용
- [ ] 비즈니스 용어 사용

### 테스트 구조
- [ ] Given-When-Then 구조 명확
- [ ] 하나의 테스트는 하나의 개념만
- [ ] 적절한 단언문 사용

### 테스트 데이터
- [ ] 테스트 빌더 패턴 사용
- [ ] 의미 있는 테스트 데이터
- [ ] 중복 데이터 제거

### 가독성
- [ ] 주석 없이도 이해 가능
- [ ] 간결하고 명확한 표현
- [ ] 일관된 코딩 스타일
```

## 실습 3: F.I.R.S.T 원칙 적용 (30분)

### 목표
기존 테스트를 F.I.R.S.T 원칙에 맞게 수정합니다.

### F.I.R.S.T 원칙 복습

- **Fast**: 빠르게 실행
- **Independent**: 독립적
- **Repeatable**: 반복 가능
- **Self-Validating**: 자가 검증
- **Timely**: 시기 적절

### 개선 대상 테스트

```java
// Bad: F.I.R.S.T 원칙을 위반하는 테스트들
public class OrderServiceTest {
    
    private static OrderService orderService;
    private static DatabaseConnection dbConnection;
    private static Order testOrder;
    
    @BeforeAll
    static void setUpClass() {
        // 실제 데이터베이스 연결 (느림)
        dbConnection = new DatabaseConnection("localhost:5432/testdb");
        orderService = new OrderService(dbConnection);
        
        // 공유 테스트 데이터 (독립적이지 않음)
        testOrder = new Order();
        testOrder.setId(1L);
        testOrder.setCustomerId(100L);
        testOrder.setAmount(new BigDecimal("99.99"));
    }
    
    @Test
    void testOrderCreation() {
        // 이전 테스트의 결과에 의존 (독립적이지 않음)
        testOrder.setStatus(OrderStatus.PENDING);
        Order result = orderService.createOrder(testOrder);
        
        // 수동으로 결과 확인 필요 (자가 검증 아님)
        System.out.println("Created order ID: " + result.getId());
        System.out.println("Order status: " + result.getStatus());
        
        // 외부 서비스 호출로 인한 불안정성 (반복 가능하지 않음)
        boolean emailSent = orderService.sendConfirmationEmail(result);
        System.out.println("Email sent: " + emailSent);
    }
    
    @Test
    void testOrderCancellation() {
        // 이전 테스트에서 생성된 주문에 의존
        testOrder.setStatus(OrderStatus.CONFIRMED);
        
        boolean cancelled = orderService.cancelOrder(testOrder.getId());
        
        if (cancelled) {
            System.out.println("Order cancelled successfully");
        } else {
            System.out.println("Failed to cancel order");
        }
        
        // 실제 외부 결제 시스템 호출 (느리고 불안정)
        RefundResult refund = orderService.processRefund(testOrder.getId());
        System.out.println("Refund status: " + refund.getStatus());
    }
    
    @Test  
    void testOrderValidation() {
        // 현재 날짜에 의존하는 테스트 (반복 가능하지 않음)
        LocalDate today = LocalDate.now();
        testOrder.setOrderDate(today);
        
        boolean isValid = orderService.validateOrder(testOrder);
        
        // 수동 검증
        if (isValid) {
            System.out.println("Order is valid");
        } else {
            System.out.println("Order is invalid");
        }
    }
}
```

### 개선 과제

F.I.R.S.T 원칙을 적용하여 테스트를 개선하세요:

### 개선 결과 템플릿

```java
// Good: F.I.R.S.T 원칙을 준수하는 테스트
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    
    @Mock
    private OrderRepository orderRepository;
    
    @Mock
    private EmailService emailService;
    
    @Mock
    private PaymentService paymentService;
    
    @Mock
    private Clock clock;
    
    @InjectMocks
    private OrderService orderService;
    
    // Fast: 빠른 실행을 위한 모킹 사용
    // Independent: 각 테스트마다 새로운 객체 생성
    @Test
    @DisplayName("유효한 주문 데이터로 주문 생성 시 성공한다")
    void shouldCreateOrder_WhenValidOrderDataProvided() {
        // Given - Independent: 테스트마다 독립적인 데이터
        Order inputOrder = OrderTestData.createValidOrder()
            .withCustomerId(100L)
            .withAmount(new BigDecimal("99.99"))
            .build();
        
        Order savedOrder = OrderTestData.createValidOrder()
            .withId(1L)
            .withCustomerId(100L)
            .withAmount(new BigDecimal("99.99"))
            .withStatus(OrderStatus.PENDING)
            .build();
        
        when(orderRepository.save(any(Order.class))).thenReturn(savedOrder);
        when(emailService.sendConfirmationEmail(any())).thenReturn(true);
        
        // When
        Order result = orderService.createOrder(inputOrder);
        
        // Then - Self-Validating: 자동 검증
        assertThat(result)
            .extracting("id", "customerId", "amount", "status")
            .containsExactly(1L, 100L, new BigDecimal("99.99"), OrderStatus.PENDING);
        
        verify(emailService).sendConfirmationEmail(result);
    }
    
    // Repeatable: 시간에 의존하지 않는 테스트
    @Test
    @DisplayName("주문 취소 시 환불이 정상 처리된다")
    void shouldProcessRefund_WhenOrderIsCancelled() {
        // Given - Repeatable: 고정된 시간 사용
        LocalDateTime fixedTime = LocalDateTime.of(2023, 12, 15, 10, 0);
        when(clock.instant()).thenReturn(fixedTime.toInstant(ZoneOffset.UTC));
        when(clock.getZone()).thenReturn(ZoneOffset.UTC);
        
        Order existingOrder = OrderTestData.createValidOrder()
            .withId(1L)
            .withStatus(OrderStatus.CONFIRMED)
            .withOrderDate(fixedTime.minusHours(1))
            .build();
        
        RefundResult successfulRefund = new RefundResult(
            RefundStatus.SUCCESS, 
            "Refund processed successfully"
        );
        
        when(orderRepository.findById(1L)).thenReturn(Optional.of(existingOrder));
        when(paymentService.processRefund(any())).thenReturn(successfulRefund);
        when(orderRepository.save(any())).thenReturn(existingOrder);
        
        // When
        boolean result = orderService.cancelOrder(1L);
        
        // Then - Self-Validating
        assertThat(result).isTrue();
        
        verify(paymentService).processRefund(argThat(refundRequest -> 
            refundRequest.getOrderId().equals(1L) &&
            refundRequest.getAmount().equals(existingOrder.getAmount())
        ));
        
        verify(orderRepository).save(argThat(order ->
            order.getStatus() == OrderStatus.CANCELLED
        ));
    }
    
    // Fast & Independent: 빠르고 독립적인 검증 테스트
    @ParameterizedTest
    @DisplayName("주문 유효성 검사 시나리오별 테스트")
    @MethodSource("orderValidationTestCases")
    void shouldValidateOrder_BasedOnOrderData(Order order, boolean expectedValid, String description) {
        // Given - Fast: 외부 의존성 없이 빠른 실행
        // (실제 시간이나 외부 서비스 호출 없음)
        
        // When
        boolean result = orderService.validateOrder(order);
        
        // Then - Self-Validating: 명확한 자동 검증
        assertThat(result)
            .as(description)
            .isEqualTo(expectedValid);
    }
    
    private static Stream<Arguments> orderValidationTestCases() {
        return Stream.of(
            Arguments.of(
                OrderTestData.createValidOrder().build(),
                true,
                "유효한 주문은 검증을 통과해야 함"
            ),
            Arguments.of(
                OrderTestData.createValidOrder().withCustomerId(null).build(),
                false,
                "고객 ID가 없는 주문은 검증 실패해야 함"
            ),
            Arguments.of(
                OrderTestData.createValidOrder().withAmount(BigDecimal.ZERO).build(),
                false,
                "금액이 0인 주문은 검증 실패해야 함"
            ),
            Arguments.of(
                OrderTestData.createValidOrder().withAmount(new BigDecimal("-10")).build(),
                false,
                "음수 금액인 주문은 검증 실패해야 함"
            )
        );
    }
    
    // Timely: 프로덕션 코드와 함께 작성되는 테스트 예시
    @Test
    @DisplayName("주문 금액 할인 적용 시 정확한 최종 금액이 계산된다")
    void shouldCalculateCorrectFinalAmount_WhenDiscountApplied() {
        // Given
        Order order = OrderTestData.createValidOrder()
            .withAmount(new BigDecimal("100.00"))
            .build();
        
        Discount discount = new Discount(DiscountType.PERCENTAGE, new BigDecimal("10"));
        
        // When
        BigDecimal finalAmount = orderService.calculateFinalAmount(order, discount);
        
        // Then
        assertThat(finalAmount)
            .isEqualTo(new BigDecimal("90.00"));
    }
}

// 테스트 데이터 빌더 - Independent & Repeatable 지원
class OrderTestData {
    public static OrderBuilder createValidOrder() {
        return new OrderBuilder();
    }
    
    public static class OrderBuilder {
        private Long id;
        private Long customerId = 100L;
        private BigDecimal amount = new BigDecimal("99.99");
        private OrderStatus status = OrderStatus.PENDING;
        private LocalDateTime orderDate = LocalDateTime.of(2023, 12, 15, 10, 0);
        
        public OrderBuilder withId(Long id) {
            this.id = id;
            return this;
        }
        
        public OrderBuilder withCustomerId(Long customerId) {
            this.customerId = customerId;
            return this;
        }
        
        public OrderBuilder withAmount(BigDecimal amount) {
            this.amount = amount;
            return this;
        }
        
        public OrderBuilder withStatus(OrderStatus status) {
            this.status = status;
            return this;
        }
        
        public OrderBuilder withOrderDate(LocalDateTime orderDate) {
            this.orderDate = orderDate;
            return this;
        }
        
        public Order build() {
            Order order = new Order();
            order.setId(id);
            order.setCustomerId(customerId);
            order.setAmount(amount);
            order.setStatus(status);
            order.setOrderDate(orderDate);
            return order;
        }
    }
}
```

### F.I.R.S.T 원칙 체크리스트
```markdown
## F.I.R.S.T 원칙 적용 체크리스트

### Fast (빠름)
- [ ] 외부 의존성 모킹 사용
- [ ] 실제 데이터베이스/네트워크 호출 제거
- [ ] 복잡한 계산이나 긴 대기 시간 제거
- [ ] 테스트 실행 시간 1초 이내

### Independent (독립적)
- [ ] 테스트 간 실행 순서 무관
- [ ] 각 테스트마다 새로운 테스트 데이터
- [ ] 공유 상태 제거
- [ ] @BeforeEach로 초기화

### Repeatable (반복 가능)
- [ ] 환경에 관계없이 동일한 결과
- [ ] 시간, 랜덤값 등 고정
- [ ] 외부 서비스 모킹
- [ ] 네트워크 상태 무관

### Self-Validating (자가 검증)
- [ ] 자동으로 성공/실패 판단
- [ ] 수동 확인 불필요
- [ ] 명확한 assertion 사용
- [ ] System.out.println 제거

### Timely (시기 적절)
- [ ] 프로덕션 코드 작성 전/중 테스트 작성
- [ ] TDD 사이클 준수
- [ ] 코드 변경과 동시에 테스트 업데이트
```

## 평가 기준

### 실습 1: TDD 실습 (50점)
- Red-Green-Refactor 사이클 준수 (20점)
- 테스트 코드 품질 (15점)
- 점진적 기능 개발 (10점)
- 최종 코드 품질 (5점)

### 실습 2: 테스트 리팩토링 (25점)
- 테스트 가독성 개선 (10점)
- Given-When-Then 구조 적용 (8점)
- 중복 제거 및 구조 개선 (7점)

### 실습 3: F.I.R.S.T 원칙 적용 (25점)
- 각 원칙별 적용 정확성 (20점)
- 전체적인 테스트 품질 향상 (5점)

## 제출 형식
- 파일명: `09_unit-testing-tdd_실습_[이름].md`
- 제출 기한: 다음 강의 시작 전
- 포함 내용: 
  - TDD로 구현한 계산기 코드
  - 리팩토링된 테스트 코드
  - F.I.R.S.T 원칙 적용 결과

## 추가 자료
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)
- [AssertJ Assertions Guide](https://assertj.github.io/doc/)
- TDD 관련 서적: "Test Driven Development" by Kent Beck
- 테스트 더블 패턴 가이드 