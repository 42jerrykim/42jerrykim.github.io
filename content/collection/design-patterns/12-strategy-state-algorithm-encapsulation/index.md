---
draft: true
collection_order: 120
title: "[Design Patterns] 전략과 상태: 알고리즘 캡슐화의 미학"
description: "동적으로 알고리즘을 교체하는 Strategy 패턴과 상태에 따라 행동을 변경하는 State 패턴의 고급 활용법을 탐구합니다. 알고리즘 캡슐화, 상태 기계 설계, 함수형 프로그래밍과의 연계 등을 통해 유연하고 확장 가능한 시스템을 설계하는 전문가 수준의 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-12T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Behavioral Patterns
- Algorithm Design
- State Management
tags:
- Design-Pattern
- GoF
- Functional-Programming
- SOLID
- 디자인패턴
---

Strategy와 State 패턴의 철학적 차이를 탐구합니다. 알고리즘 교체와 상태 기반 행동 변화를 통해 유연한 시스템을 설계하는 방법을 학습합니다.

## 서론: 행동의 캡슐화 vs 상태의 진화

> *"Strategy 패턴은 '어떻게 할 것인가'를 캡슐화하고, State 패턴은 '언제 무엇을 할 것인가'를 캡슐화한다."*

현대 소프트웨어 개발에서 **Strategy**와 **State** 패턴은 매우 자주 혼동되는 패턴들입니다. 두 패턴 모두 **컴포지션을 통한 다형성**을 활용하고, **UML 다이어그램조차 거의 동일**합니다. 하지만 이들의 **철학적 차이**는 명확합니다.

**Strategy 패턴**은 **"알고리즘의 캡슐화"**에 초점을 맞춥니다. 런타임에 알고리즘을 교체할 수 있는 유연성을 제공하며, "어떻게 할 것인가(How)"의 문제를 해결합니다.

**State 패턴**은 **"상태 기반 행동 변화"**에 초점을 맞춥니다. 객체의 내부 상태에 따라 행동이 자동으로 변하며, "언제 무엇을 할 것인가(When & What)"의 문제를 해결합니다.

## Strategy 패턴 - 알고리즘의 캡슐화

### Strategy 패턴의 핵심 철학

Strategy 패턴은 **"알고리즘 패밀리를 정의하고, 각각을 캡슐화하여 상호 교체 가능하게 만드는"** 패턴입니다. 이는 **개방-폐쇄 원칙**의 완벽한 구현체입니다.

```java
// Strategy 패턴 없이 구현한다면?
class BadPriceCalculator {
    public double calculatePrice(double basePrice, String customerType) {
        switch (customerType) {
            case "REGULAR":
                return basePrice;
            case "MEMBER":
                return basePrice * 0.9;
            case "VIP":
                return basePrice * 0.8;
            case "EMPLOYEE":
                return basePrice * 0.7;
            default:
                throw new IllegalArgumentException("Unknown customer type");
        }
    }
}
```

### Strategy 패턴으로 우아하게 해결

```java
// Strategy 패턴으로 우아하게 해결
interface PaymentStrategy {
    PaymentResult processPayment(double amount, PaymentContext context);
    String getPaymentType();
    boolean isAvailable(PaymentContext context);
}

class CreditCardStrategy implements PaymentStrategy {
    private final String cardNumber;
    private final String cvv;
    private final String expiryDate;
    private final CardProcessor cardProcessor;
    
    public CreditCardStrategy(String cardNumber, String cvv, String expiryDate) {
        this.cardNumber = maskCardNumber(cardNumber);
        this.cvv = cvv;
        this.expiryDate = expiryDate;
        this.cardProcessor = new CardProcessor();
    }
    
    @Override
    public PaymentResult processPayment(double amount, PaymentContext context) {
        try {
            // 카드 유효성 검증
            if (!validateCard()) {
                return PaymentResult.failed("Invalid card information");
            }
            
            // 한도 확인
            if (!checkCreditLimit(amount)) {
                return PaymentResult.failed("Credit limit exceeded");
            }
            
            // 실제 결제 처리
            String transactionId = cardProcessor.processTransaction(cardNumber, amount);
            
            return PaymentResult.success(transactionId, amount, "Credit Card Payment Completed");
            
        } catch (PaymentException e) {
            return PaymentResult.failed("Payment processing failed: " + e.getMessage());
        }
    }
    
    @Override
    public String getPaymentType() {
        return "Credit Card";
    }
    
    @Override
    public boolean isAvailable(PaymentContext context) {
        return validateCard() && context.getAmount() <= 10000.0; // 1만달러 한도
    }
    
    private boolean validateCard() {
        return cardNumber != null && cvv != null && !isExpired();
    }
    
    private boolean isExpired() {
        // 만료일 확인 로직
        return false;
    }
    
    private boolean checkCreditLimit(double amount) {
        // 신용한도 확인 로직
        return true;
    }
    
    private String maskCardNumber(String cardNumber) {
        return cardNumber.replaceAll("\\d(?=\\d{4})", "*");
    }
}

class PayPalStrategy implements PaymentStrategy {
    private final String email;
    private final String apiKey;
    private final PayPalClient paypalClient;
    
    public PayPalStrategy(String email, String apiKey) {
        this.email = email;
        this.apiKey = apiKey;
        this.paypalClient = new PayPalClient(apiKey);
    }
    
    @Override
    public PaymentResult processPayment(double amount, PaymentContext context) {
        try {
            // PayPal 계정 잔액 확인
            if (!checkAccountBalance(amount)) {
                return PaymentResult.failed("Insufficient PayPal balance");
            }
            
            // PayPal API 호출
            PayPalTransaction transaction = paypalClient.createPayment(email, amount);
            
            return PaymentResult.success(
                transaction.getId(), 
                amount, 
                "PayPal Payment Completed"
            );
            
        } catch (PayPalException e) {
            return PaymentResult.failed("PayPal processing failed: " + e.getMessage());
        }
    }
    
    @Override
    public String getPaymentType() {
        return "PayPal";
    }
    
    @Override
    public boolean isAvailable(PaymentContext context) {
        return paypalClient.isAccountValid(email);
    }
    
    private boolean checkAccountBalance(double amount) {
        return paypalClient.getBalance(email) >= amount;
    }
}

class CryptocurrencyStrategy implements PaymentStrategy {
    private final String walletAddress;
    private final String privateKey;
    private final BlockchainClient blockchainClient;
    
    public CryptocurrencyStrategy(String walletAddress, String privateKey) {
        this.walletAddress = walletAddress;
        this.privateKey = privateKey;
        this.blockchainClient = new BlockchainClient();
    }
    
    @Override
    public PaymentResult processPayment(double amount, PaymentContext context) {
        try {
            // USD를 암호화폐로 변환
            double cryptoAmount = convertToCrypto(amount);
            
            // 지갑 잔액 확인
            if (!hasEnoughBalance(cryptoAmount)) {
                return PaymentResult.failed("Insufficient cryptocurrency balance");
            }
            
            // 블록체인 트랜잭션 생성
            String txHash = blockchainClient.sendTransaction(
                walletAddress, context.getRecipientAddress(), cryptoAmount
            );
            
            return PaymentResult.success(txHash, amount, "Cryptocurrency Payment Completed");
            
        } catch (BlockchainException e) {
            return PaymentResult.failed("Blockchain transaction failed: " + e.getMessage());
        }
    }
    
    @Override
    public String getPaymentType() {
        return "Cryptocurrency";
    }
    
    @Override
    public boolean isAvailable(PaymentContext context) {
        return blockchainClient.isNetworkAvailable() && 
               context.getRecipientAddress() != null;
    }
    
    private double convertToCrypto(double usdAmount) {
        return blockchainClient.convertUSDToCrypto(usdAmount);
    }
    
    private boolean hasEnoughBalance(double cryptoAmount) {
        return blockchainClient.getBalance(walletAddress) >= cryptoAmount;
    }
}

// Context 클래스
class PaymentProcessor {
    private PaymentStrategy paymentStrategy;
    private final List<PaymentStrategy> availableStrategies;
    private final PaymentLogger logger;
    
    public PaymentProcessor() {
        this.availableStrategies = new ArrayList<>();
        this.logger = new PaymentLogger();
    }
    
    public void addPaymentStrategy(PaymentStrategy strategy) {
        availableStrategies.add(strategy);
    }
    
    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.paymentStrategy = strategy;
    }
    
    public PaymentResult processPayment(double amount, PaymentContext context) {
        if (paymentStrategy == null) {
            return selectOptimalStrategy(amount, context);
        }
        
        if (!paymentStrategy.isAvailable(context)) {
            return PaymentResult.failed("Selected payment method is not available");
        }
        
        logger.logPaymentAttempt(paymentStrategy.getPaymentType(), amount);
        PaymentResult result = paymentStrategy.processPayment(amount, context);
        logger.logPaymentResult(result);
        
        return result;
    }
    
    private PaymentResult selectOptimalStrategy(double amount, PaymentContext context) {
        for (PaymentStrategy strategy : availableStrategies) {
            if (strategy.isAvailable(context)) {
                setPaymentStrategy(strategy);
                return processPayment(amount, context);
            }
        }
        return PaymentResult.failed("No available payment methods");
    }
    
    public List<String> getAvailablePaymentMethods(PaymentContext context) {
        return availableStrategies.stream()
            .filter(strategy -> strategy.isAvailable(context))
            .map(PaymentStrategy::getPaymentType)
            .collect(Collectors.toList());
    }
}

// 결과 클래스들
class PaymentResult {
    private final boolean success;
    private final String transactionId;
    private final double amount;
    private final String message;
    private final LocalDateTime timestamp;
    
    private PaymentResult(boolean success, String transactionId, double amount, String message) {
        this.success = success;
        this.transactionId = transactionId;
        this.amount = amount;
        this.message = message;
        this.timestamp = LocalDateTime.now();
    }
    
    public static PaymentResult success(String transactionId, double amount, String message) {
        return new PaymentResult(true, transactionId, amount, message);
    }
    
    public static PaymentResult failed(String message) {
        return new PaymentResult(false, null, 0.0, message);
    }
    
    // getters...
}

class PaymentContext {
    private final double amount;
    private final String currency;
    private final String recipientAddress;
    private final Map<String, Object> additionalData;
    
    public PaymentContext(double amount, String currency, String recipientAddress) {
        this.amount = amount;
        this.currency = currency;
        this.recipientAddress = recipientAddress;
        this.additionalData = new HashMap<>();
    }
    
    // getters and setters...
}
```

### 함수형 프로그래밍에서의 Strategy 패턴

Java 8 이후, Strategy 패턴은 함수형 인터페이스와 람다 표현식으로 더욱 간결하게 구현할 수 있습니다:

```java
// 함수형 Strategy 패턴
@FunctionalInterface
interface DiscountStrategy {
    double applyDiscount(double price);
}

class FunctionalPriceCalculator {
    // 전략들을 정적 메서드로 정의
    public static final DiscountStrategy NO_DISCOUNT = price -> price;
    public static final DiscountStrategy MEMBER_DISCOUNT = price -> price * 0.9;
    public static final DiscountStrategy VIP_DISCOUNT = price -> price * 0.8;
    public static final DiscountStrategy SEASONAL_DISCOUNT = price -> price * 0.85;
    
    // 복합 할인 전략
    public static DiscountStrategy combined(DiscountStrategy... strategies) {
        return price -> Arrays.stream(strategies)
            .reduce(price, (p, strategy) -> strategy.applyDiscount(p), (p1, p2) -> p2);
    }
    
    // 조건부 할인 전략
    public static DiscountStrategy conditional(Predicate<Double> condition, 
                                             DiscountStrategy strategy) {
        return price -> condition.test(price) ? strategy.applyDiscount(price) : price;
    }
    
    public double calculatePrice(double basePrice, DiscountStrategy strategy) {
        return strategy.applyDiscount(basePrice);
    }
}

// 사용 예시
FunctionalPriceCalculator calculator = new FunctionalPriceCalculator();

// 기본 사용
double memberPrice = calculator.calculatePrice(100.0, MEMBER_DISCOUNT);

// 람다로 인라인 전략
double customPrice = calculator.calculatePrice(100.0, price -> price * 0.75);

// 복합 전략
DiscountStrategy blackFriday = combined(MEMBER_DISCOUNT, SEASONAL_DISCOUNT);
double specialPrice = calculator.calculatePrice(200.0, blackFriday);

// 조건부 전략
DiscountStrategy bulkDiscount = conditional(
    price -> price > 500, 
    price -> price * 0.95
);
```

## State 패턴 - 상태 기반 행동 변화

### State 패턴의 핵심 철학

State 패턴은 **"객체의 내부 상태가 변할 때 객체의 행동이 바뀌도록 허용하는"** 패턴입니다. 마치 객체의 클래스가 바뀌는 것처럼 보입니다.

```java
// State 패턴 없이 구현한다면?
class BadVendingMachine {
    private enum State { IDLE, MONEY_INSERTED, PRODUCT_SELECTED, DISPENSING }
    private State currentState = State.IDLE;
    private double balance = 0.0;
    
    public void insertMoney(double amount) {
        // 😱 상태마다 다른 조건문 필요
        if (currentState == State.IDLE) {
            balance += amount;
            currentState = State.MONEY_INSERTED;
        } else if (currentState == State.MONEY_INSERTED) {
            balance += amount;
        } else {
            System.out.println("Cannot insert money in current state");
        }
    }
    
    public void selectProduct(String code) {
        if (currentState == State.MONEY_INSERTED) {
            // 복잡한 조건 로직
            currentState = State.PRODUCT_SELECTED;
        } else {
            System.out.println("Invalid state for product selection");
        }
    }
    
    // 더 많은 메서드들... 각각 복잡한 조건문 포함
}
```

### State 패턴으로 우아하게 해결

```java
// State 패턴으로 우아하게 해결
interface VendingMachineState {
    void insertMoney(VendingMachine machine, double amount);
    void selectProduct(VendingMachine machine, String productCode);
    void dispenseProduct(VendingMachine machine);
    void returnMoney(VendingMachine machine);
    String getStateName();
}

class IdleState implements VendingMachineState {
    private static final IdleState INSTANCE = new IdleState();
    
    public static IdleState getInstance() {
        return INSTANCE;
    }
    
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        machine.addMoney(amount);
        System.out.printf("💰 Money inserted: $%.2f\n", amount);
        machine.setState(MoneyInsertedState.getInstance());
    }
    
    @Override
    public void selectProduct(VendingMachine machine, String productCode) {
        System.out.println("[Error] Please insert money first!");
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("[Error] Please insert money and select product first!");
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        System.out.println("[Error] No money to return!");
    }
    
    @Override
    public String getStateName() {
        return "Idle";
    }
}

class MoneyInsertedState implements VendingMachineState {
    private static final MoneyInsertedState INSTANCE = new MoneyInsertedState();
    
    public static MoneyInsertedState getInstance() {
        return INSTANCE;
    }
    
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        machine.addMoney(amount);
        System.out.printf("💰 Additional money inserted: $%.2f (Total: $%.2f)\n", 
                         amount, machine.getCurrentBalance());
    }
    
    @Override
    public void selectProduct(VendingMachine machine, String productCode) {
        Product product = machine.getProduct(productCode);
        if (product == null) {
            System.out.println("[Error] Invalid product code!");
            return;
        }
        
        if (machine.getCurrentBalance() >= product.getPrice()) {
            machine.setSelectedProduct(product);
            System.out.printf("[OK] Product selected: %s ($%.2f)\n", 
                             product.getName(), product.getPrice());
            machine.setState(ProductSelectedState.getInstance());
        } else {
            System.out.printf("[Error] Insufficient funds! Need $%.2f more\n", 
                             product.getPrice() - machine.getCurrentBalance());
        }
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("[Error] Please select a product first!");
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        double balance = machine.getCurrentBalance();
        machine.resetBalance();
        System.out.printf("💵 Returned $%.2f\n", balance);
        machine.setState(IdleState.getInstance());
    }
    
    @Override
    public String getStateName() {
        return "Money Inserted";
    }
}

class ProductSelectedState implements VendingMachineState {
    private static final ProductSelectedState INSTANCE = new ProductSelectedState();
    
    public static ProductSelectedState getInstance() {
        return INSTANCE;
    }
    
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        machine.addMoney(amount);
        System.out.printf("💰 Additional money inserted: $%.2f\n", amount);
    }
    
    @Override
    public void selectProduct(VendingMachine machine, String productCode) {
        System.out.println("[Warning] Product already selected. Press dispense or return money.");
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        Product product = machine.getSelectedProduct();
        double change = machine.getCurrentBalance() - product.getPrice();
        
        machine.setState(DispensingState.getInstance());
        
        System.out.printf("🥤 Dispensing: %s\n", product.getName());
        
        if (change > 0) {
            System.out.printf("💵 Change returned: $%.2f\n", change);
        }
        
        machine.resetBalance();
        machine.setSelectedProduct(null);
        machine.setState(IdleState.getInstance());
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        double balance = machine.getCurrentBalance();
        machine.resetBalance();
        machine.setSelectedProduct(null);
        System.out.printf("💵 Transaction cancelled. Returned $%.2f\n", balance);
        machine.setState(IdleState.getInstance());
    }
    
    @Override
    public String getStateName() {
        return "Product Selected";
    }
}

class DispensingState implements VendingMachineState {
    private static final DispensingState INSTANCE = new DispensingState();
    
    public static DispensingState getInstance() {
        return INSTANCE;
    }
    
    @Override
    public void insertMoney(VendingMachine machine, double amount) {
        System.out.println("⏳ Please wait, dispensing in progress...");
    }
    
    @Override
    public void selectProduct(VendingMachine machine, String productCode) {
        System.out.println("⏳ Please wait, dispensing in progress...");
    }
    
    @Override
    public void dispenseProduct(VendingMachine machine) {
        System.out.println("⏳ Already dispensing...");
    }
    
    @Override
    public void returnMoney(VendingMachine machine) {
        System.out.println("⏳ Cannot return money while dispensing...");
    }
    
    @Override
    public String getStateName() {
        return "Dispensing";
    }
}

// Context 클래스
class VendingMachine {
    private VendingMachineState currentState;
    private double currentBalance;
    private Product selectedProduct;
    private final Map<String, Product> products;
    private final List<StateTransitionListener> listeners;
    
    public VendingMachine() {
        this.currentState = IdleState.getInstance();
        this.currentBalance = 0.0;
        this.products = new HashMap<>();
        this.listeners = new ArrayList<>();
        initializeProducts();
    }
    
    private void initializeProducts() {
        products.put("A1", new Product("A1", "Coca Cola", 1.50));
        products.put("B1", new Product("B1", "Pepsi", 1.50));
        products.put("C1", new Product("C1", "Water", 1.00));
        products.put("D1", new Product("D1", "Juice", 2.00));
    }
    
    // 상태 전이와 함께 이벤트 발생
    public void setState(VendingMachineState newState) {
        VendingMachineState oldState = this.currentState;
        this.currentState = newState;
        
        System.out.printf("🔄 State: %s → %s\n", 
                         oldState.getStateName(), newState.getStateName());
        
        // 상태 전이 이벤트 통지
        notifyStateTransition(oldState, newState);
    }
    
    private void notifyStateTransition(VendingMachineState from, VendingMachineState to) {
        for (StateTransitionListener listener : listeners) {
            listener.onStateTransition(from.getStateName(), to.getStateName());
        }
    }
    
    public void addStateTransitionListener(StateTransitionListener listener) {
        listeners.add(listener);
    }
    
    // 상태에 위임하는 메서드들
    public void insertMoney(double amount) {
        currentState.insertMoney(this, amount);
    }
    
    public void selectProduct(String productCode) {
        currentState.selectProduct(this, productCode);
    }
    
    public void dispenseProduct() {
        currentState.dispenseProduct(this);
    }
    
    public void returnMoney() {
        currentState.returnMoney(this);
    }
    
    // 내부 상태 관리 메서드들
    public void addMoney(double amount) {
        this.currentBalance += amount;
    }
    
    public double getCurrentBalance() {
        return currentBalance;
    }
    
    public void resetBalance() {
        this.currentBalance = 0.0;
    }
    
    public Product getProduct(String code) {
        return products.get(code);
    }
    
    public void setSelectedProduct(Product product) {
        this.selectedProduct = product;
    }
    
    public Product getSelectedProduct() {
        return selectedProduct;
    }
    
    public String getCurrentStateName() {
        return currentState.getStateName();
    }
}

// 상태 전이 이벤트 리스너
interface StateTransitionListener {
    void onStateTransition(String fromState, String toState);
}

class Product {
    private final String code;
    private final String name;
    private final double price;
    
    public Product(String code, String name, double price) {
        this.code = code;
        this.name = name;
        this.price = price;
    }
    
    // getters...
    public String getCode() { return code; }
    public String getName() { return name; }
    public double getPrice() { return price; }
}
```

## Strategy vs State - 구조적 유사성과 본질적 차이

### 패턴 비교 매트릭스

| **특성** | **Strategy Pattern** | **State Pattern** |
|----------|---------------------|-------------------|
| **핵심 목적** | 알고리즘 캡슐화 | 상태 기반 행동 변화 |
| **Context 역할** | 전략 선택과 위임 | 상태 전이와 행동 위임 |
| **객체 생명주기** | 필요에 따라 생성/교체 | 상태 전이에 따라 변경 |
| **상호 작용** | Context → Strategy | State ↔ Context |
| **전이 책임** | Context가 결정 | State가 주도할 수 있음 |
| **복잡성** | 상대적으로 단순 | 상태 전이 로직으로 복잡 |
| **사용 시점** | 런타임 알고리즘 선택 | 객체 상태 변화 시 |

### 실제 비교 예시

```java
// Strategy 패턴 예시: 정렬 알고리즘 선택
class SortingContext {
    private SortingStrategy strategy;
    
    public void setStrategy(SortingStrategy strategy) {
        this.strategy = strategy; // Context가 전략을 선택
    }
    
    public void sort(int[] array) {
        strategy.sort(array); // 전략에 위임
    }
}

// State 패턴 예시: TCP 연결 상태
class TCPConnection {
    private TCPState currentState;
    
    public void open() {
        currentState.open(this); // 상태가 전이를 결정할 수 있음
    }
    
    public void setState(TCPState state) {
        this.currentState = state; // 상태가 Context를 변경
    }
}
```

### 언제 어떤 패턴을 선택할 것인가?

**Strategy 패턴을 선택하세요:**
- 런타임에 알고리즘을 변경해야 할 때
- 조건문이 많은 알고리즘 선택 로직이 있을 때
- 알고리즘 패밀리를 캡슐화하고 싶을 때
- 클라이언트가 사용할 알고리즘을 선택해야 할 때

**State 패턴을 선택하세요:**
- 객체의 행동이 상태에 따라 달라질 때
- 상태 전이 로직이 복잡할 때
- 상태 전이 규칙이 명확할 때
- 상태 머신을 구현해야 할 때

## 한눈에 보는 Strategy & State 패턴

### Strategy vs State 핵심 비교

| 비교 항목 | Strategy 패턴 | State 패턴 |
|----------|--------------|-----------|
| **핵심 목적** | 알고리즘 캡슐화 및 교체 | 상태별 행동 캡슐화 |
| **변화 주체** | 클라이언트가 선택 | 객체 내부에서 전이 |
| **교체 시점** | 클라이언트 결정 (외부) | 상태 로직에 따라 (내부) |
| **캡슐화 대상** | "어떻게(How)" | "언제(When)" |
| **상태 인식** | Context가 전략 몰라도 됨 | Context가 상태 알 필요 없음 |
| **전이 책임** | 없음 (선택만) | State 또는 Context |

### 구조적 유사점과 차이점

| 측면 | Strategy | State |
|------|----------|-------|
| UML 구조 | 거의 동일 | 거의 동일 |
| 공통 인터페이스 | Strategy 인터페이스 | State 인터페이스 |
| Context 역할 | 전략 사용 | 현재 상태 유지 |
| 구체 클래스 | 알고리즘 구현 | 상태별 행동 구현 |
| 핵심 차이 | **의도(Intent)** | **의도(Intent)** |

### 선택 가이드

| 상황 | 권장 패턴 | 이유 |
|------|----------|------|
| 정렬 알고리즘 교체 | Strategy | 클라이언트가 알고리즘 선택 |
| 할인 정책 적용 | Strategy | 조건에 따른 계산 방식 변경 |
| 주문 상태 관리 | State | 상태 전이에 따른 행동 변화 |
| 게임 캐릭터 상태 | State | 상태별 다른 행동 패턴 |
| 결제 처리 방식 | Strategy | 결제 수단별 처리 로직 |
| TCP 연결 상태 | State | 연결 상태에 따른 행동 |

### if-else 제거 효과 비교

| 문제 코드 | Strategy 해결 | State 해결 |
|----------|--------------|-----------|
| if(type == A) doA() | strategy.execute() | state.handle() |
| switch(algorithm) | strategy.process() | - |
| switch(state) | - | state.action() |
| 조건 추가 시 | 새 Strategy 클래스 | 새 State 클래스 |

### 장단점 비교

| 패턴 | 장점 | 단점 |
|------|------|------|
| Strategy | 알고리즘 독립적 변경, OCP 준수, 테스트 용이 | 클래스 수 증가, 클라이언트가 전략 알아야 함 |
| State | 상태 로직 분리, 전이 로직 명확, OCP 준수 | 상태 수에 비례한 클래스, 상태 공유 어려움 |

### 현대적 구현 방식

| 구현 방식 | Strategy 예시 | State 예시 |
|----------|--------------|-----------|
| 전통적 OOP | interface + 구현 클래스들 | interface + 상태 클래스들 |
| 함수형 (Java 8+) | `Function<T, R>` | 가능하나 복잡 |
| Enum 활용 | `enum Strategy` | `enum State` |
| 람다 + Map | `Map<String, Strategy>` | 제한적 |

### 적용 체크리스트

| Strategy 체크 항목 | State 체크 항목 |
|------------------|----------------|
| 여러 알고리즘이 존재하는가? | 객체가 여러 상태를 가지는가? |
| 클라이언트가 알고리즘을 선택하는가? | 상태에 따라 행동이 달라지는가? |
| 런타임에 알고리즘 교체 필요? | 상태 전이 로직이 명확한가? |
| 조건문으로 알고리즘 분기 중? | switch/if로 상태 분기 중? |

---

## 결론: 캡슐화의 두 얼굴

Strategy와 State 패턴은 **"캡슐화"**라는 공통 목표를 가지지만, 서로 다른 관점에서 접근합니다:

- **Strategy**: "어떻게(How)" - 알고리즘의 캡슐화
- **State**: "언제(When)" - 상태별 행동의 캡슐화

### 현대적 활용:

```
Strategy Pattern → Modern Evolution:
- Java 8+ Functional Interfaces
- Spring Strategy Pattern (Multiple implementations)
- Payment Processing Systems
- Algorithm Libraries (Apache Commons)

State Pattern → Modern Evolution:
- Spring State Machine
- Akka Actor Model States
- Reactive State Management
- Finite State Machines in Microservices
```

### 실무 가이드라인:

```
Strategy 패턴 적용 시점:
- 동일한 목적의 다양한 알고리즘이 존재할 때
- 런타임에 알고리즘 선택이 필요할 때
- 조건문으로 인한 복잡성을 줄이고 싶을 때

State 패턴 적용 시점:
- 객체의 상태가 명확히 구분될 때
- 상태에 따른 행동 변화가 복잡할 때
- 상태 전이 규칙이 명확할 때

주의사항:
- 과도한 추상화 방지
- 성능 오버헤드 고려
- 메모리 사용량 모니터링
- 상태/전략 객체의 생명주기 관리
```

두 패턴 모두 **개방-폐쇄 원칙**을 실현하고 **코드의 유연성**을 높이는 강력한 도구입니다. 핵심은 **"무엇을 캡슐화하려는가?"**를 명확히 하는 것입니다.

다음 글에서는 **Command와 Chain of Responsibility 패턴**을 탐구하겠습니다. 요청의 캡슐화와 처리 체인을 통해 더욱 유연한 시스템 설계 방법을 살펴보겠습니다.

---

**핵심 메시지:**
"Strategy는 '어떻게 할 것인가'의 다양성을, State는 '언제 무엇을 할 것인가'의 변화를 캡슐화한다. 구조는 비슷하지만 철학이 다른 이 두 패턴을 올바르게 구분하는 것이 설계의 핵심이다." 