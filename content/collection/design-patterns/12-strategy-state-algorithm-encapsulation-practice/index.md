---
draft: true
collection_order: 121
title: "[Design Patterns] 전략과 상태 패턴 실습 - 알고리즘 캡슐화"
description: "Strategy와 State 패턴을 통해 알고리즘 캡슐화와 상태 전이를 실습합니다. 정렬 알고리즘 선택, 결제 전략, 게임 캐릭터 상태 관리 등을 구현하며 개방-폐쇄 원칙을 실현하고 복잡한 상태 로직을 우아하게 관리하는 설계 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-12T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Behavioral Patterns
- Algorithm Encapsulation
- Practice
- State Management
tags:
- Strategy Pattern Practice
- State Pattern Practice
- Algorithm Encapsulation
- State Transition
- Sorting Algorithms
- Payment Strategy
- Game Character States
- Open Closed Principle
- Context Switching
- State Machine
- Behavioral Patterns
- Design Patterns
- GoF Patterns
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Software Architecture
- Dynamic Behavior
- 전략 패턴 실습
- 상태 패턴 실습
- 알고리즘 캡슐화
- 상태 전이
- 정렬 알고리즘
- 결제 전략
- 게임 캐릭터 상태
- 개방 폐쇄 원칙
- 컨텍스트 전환
- 상태 머신
- 행동 패턴
- 디자인 패턴
- GoF 패턴
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 소프트웨어 아키텍처
- 동적 행동
---

이 실습에서는 Strategy 패턴으로 알고리즘을, State 패턴으로 상태 기반 행동을 캡슐화하는 방법을 직접 구현합니다.

## 실습 목표
- Strategy 패턴으로 알고리즘 캡슐화 구현
- State 패턴으로 상태 기반 행동 변화 구현
- 두 패턴의 차이점과 적용 시나리오 이해
- 함수형 프로그래밍 스타일 Strategy 패턴 구현

## 실습 1: 할인 전략 시스템 (Strategy)

### 요구사항
다양한 할인 정책을 적용하는 쇼핑몰 시스템

### 코드 템플릿

```java
// TODO 1: Strategy 인터페이스 정의
public interface DiscountStrategy {
    double calculateDiscount(Order order);
    String getDiscountDescription();
    boolean isApplicable(Customer customer);
}

// TODO 2: 구체적인 할인 전략들 구현
public class RegularCustomerDiscount implements DiscountStrategy {
    // TODO: 일반 고객 할인 (5%) 구현
}

public class VIPCustomerDiscount implements DiscountStrategy {
    // TODO: VIP 고객 할인 (15%) 구현
}

public class BulkOrderDiscount implements DiscountStrategy {
    // TODO: 대량 주문 할인 (수량별 차등) 구현
}

public class SeasonalDiscount implements DiscountStrategy {
    // TODO: 계절별 할인 (기간 제한) 구현
}

// TODO 3: Context 클래스 구현
public class PriceCalculator {
    private DiscountStrategy discountStrategy;
    
    // TODO: 전략 설정 및 가격 계산 로직
    public double calculateFinalPrice(Order order, Customer customer) {
        // TODO: 적용 가능한 할인 전략을 찾아 최적 할인 적용
        return 0.0;
    }
}

// TODO 4: 함수형 스타일 Strategy 구현
public class FunctionalDiscountCalculator {
    // TODO: Function 인터페이스를 활용한 할인 전략
    private static final Function<Order, Double> NO_DISCOUNT = order -> 0.0;
    private static final Function<Order, Double> MEMBER_DISCOUNT = order -> order.getTotal() * 0.1;
    
    // TODO: 조건부 할인 전략
    public static Function<Order, Double> conditionalDiscount(
        Predicate<Order> condition, 
        Function<Order, Double> discount) {
        // TODO: 조건을 만족할 때만 할인 적용
        return null;
    }
}
```

## 실습 2: 자판기 상태 관리 (State)

### 요구사항
동전 투입, 상품 선택, 배출 과정의 상태 관리

### 코드 템플릿

```java
// TODO 1: State 인터페이스 정의
public interface VendingMachineState {
    void insertCoin(VendingMachine machine, int amount);
    void selectProduct(VendingMachine machine, String productCode);
    void dispenseProduct(VendingMachine machine);
    void returnCoins(VendingMachine machine);
    String getStateName();
}

// TODO 2: 구체적인 상태들 구현
public class IdleState implements VendingMachineState {
    private static final IdleState INSTANCE = new IdleState();
    
    public static IdleState getInstance() {
        return INSTANCE;
    }
    
    // TODO: 각 상태에서의 행동 구현
}

public class HasMoneyState implements VendingMachineState {
    // TODO: 동전 투입 상태에서의 행동
}

public class SoldState implements VendingMachineState {
    // TODO: 상품 판매 상태에서의 행동
}

public class SoldOutState implements VendingMachineState {
    // TODO: 품절 상태에서의 행동
}

// TODO 3: Context 클래스 (자판기)
public class VendingMachine {
    private VendingMachineState currentState;
    private int coinBalance;
    private Map<String, Product> products;
    
    // TODO: 상태 전이 로직과 동작 메서드들 구현
    public void setState(VendingMachineState state) {
        // TODO: 상태 변경 시 로깅
    }
    
    // TODO: 상태에 위임하는 메서드들
    public void insertCoin(int amount) {
        currentState.insertCoin(this, amount);
    }
}
```

## 실습 3: 게임 캐릭터 상태 시스템

### 코드 템플릿

```java
// TODO 1: 캐릭터 상태 구현 (정상, 독, 빙결, 버프 등)
public abstract class CharacterState {
    protected final String stateName;
    protected final int duration;
    protected final GameCharacter character;
    
    // TODO: 상태별 행동 수정 메서드들
    public abstract int modifyDamage(int baseDamage);
    public abstract int modifySpeed(int baseSpeed);
    public abstract void onEnterState();
    public abstract void onExitState();
    public abstract void onUpdate();
}

// TODO 2: 상태 조합 시스템 (여러 상태 동시 적용)
public class StateManager {
    private final List<CharacterState> activeStates;
    
    // TODO: 여러 상태가 동시에 적용될 때의 효과 계산
}
```

## 체크리스트

### Strategy 패턴
- [ ] 알고리즘 가족 캡슐화
- [ ] 런타임 전략 변경 구현
- [ ] 함수형 스타일 전략 구현
- [ ] 조건부 전략 적용

### State 패턴
- [ ] 상태별 행동 변화 구현
- [ ] 상태 전이 로직 구현
- [ ] Singleton 상태 객체 적용
- [ ] 상태 히스토리 관리

### 패턴 비교 분석
- [ ] Strategy vs State 차이점 정리
- [ ] 각 패턴의 적용 시나리오 분석
- [ ] 성능 및 메모리 사용량 비교

## 추가 도전

1. **State Machine Builder**: 상태 기계 생성기 구현
2. **Strategy Composition**: 여러 전략 조합 시스템
3. **Dynamic Strategy Loading**: 런타임 전략 로딩
4. **State Persistence**: 상태 저장/복원 시스템

## 실무 적용

### Strategy 패턴 활용
- 결제 처리 전략
- 데이터 검증 전략
- 로깅 전략
- 캐싱 전략

### State 패턴 활용
- 워크플로우 관리
- 게임 캐릭터 상태
- 주문 처리 상태
- 커넥션 상태 관리

---

**핵심 포인트**: Strategy는 '어떻게 할 것인가'의 다양성을, State는 '언제 무엇을 할 것인가'의 변화를 캡슐화합니다. 구조는 비슷하지만 목적과 사용법이 다른 두 패턴을 명확히 구분하는 것이 중요합니다. 