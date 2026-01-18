---
collection_order: 22
title: "[Design Pattern] Strategy - 전략 패턴"
description: "Strategy 패턴은 알고리즘을 캡슐화하여 동적으로 교체할 수 있게 합니다. 실행 중에 다양한 전략을 유연하게 변경하여 확장성과 유지보수성을 크게 향상시킵니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Strategy
  - 전략
  - Behavioral Pattern
  - 행위 패턴
  - GoF
  - Gang of Four
  - Algorithm
  - 알고리즘
  - Encapsulation
  - 캡슐화
  - Context
  - 컨텍스트
  - Concrete Strategy
  - 구체 전략
  - Runtime
  - 런타임
  - Polymorphism
  - 다형성
  - Composition
  - 합성
  - Open Closed Principle
  - 개방 폐쇄 원칙
  - Dependency Injection
  - 의존성 주입
  - Interchangeable
  - 교체 가능
  - Sorting
  - 정렬
  - Payment
  - 결제
  - Code Reusability
  - 코드 재사용성
  - Maintainability
  - 유지보수성
  - Software Design
  - 소프트웨어 설계
  - OOP
  - 객체지향 프로그래밍
  - Java
  - C++
  - Python
  - C#
  - Comparator
  - Validator
  - 검증기
  - Compression
  - 압축
---

전략 패턴(Strategy Pattern)은 알고리즘 군을 정의하고 각각을 캡슐화하여 상호 교환 가능하게 만드는 행위 디자인 패턴이다. 이 패턴을 사용하면 알고리즘을 사용하는 클라이언트와 독립적으로 알고리즘을 변경할 수 있으며, 런타임에 동적으로 알고리즘을 교체할 수 있다.

## 개요

**전략 패턴의 정의**

전략 패턴은 특정 기능을 수행하는 알고리즘을 별도의 클래스로 분리하고, 이들을 교환 가능하게 만드는 패턴이다. 조건문으로 가득한 코드 대신, 각 알고리즘을 독립적인 전략 객체로 캡슐화하여 유연성과 재사용성을 높인다.

**패턴의 필요성 및 사용 사례**

전략 패턴은 다음과 같은 상황에서 유용하다:

- **알고리즘 선택**: 정렬, 검색, 암호화 등 다양한 알고리즘 중 선택
- **결제 시스템**: 신용카드, PayPal, 암호화폐 등 결제 방식 선택
- **압축/인코딩**: 다양한 압축 또는 인코딩 방식 지원
- **경로 탐색**: 최단 경로, 최소 비용 등 다양한 경로 알고리즘
- **검증 로직**: 다양한 유효성 검사 규칙 적용
- **가격 정책**: 할인, 멤버십 등 다양한 가격 계산 방식

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 알고리즘을 런타임에 교체 가능 | 전략이 적으면 과도한 설계 |
| 조건문 제거로 코드 간결화 | 클라이언트가 전략들을 알아야 함 |
| 개방-폐쇄 원칙 준수 | 전략마다 별도 클래스 필요 |
| 알고리즘 독립적 테스트 가능 | 람다/함수형 프로그래밍으로 대체 가능한 경우 많음 |

## 전략 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│            Context                  │
├─────────────────────────────────────┤
│ - strategy: Strategy                │
├─────────────────────────────────────┤
│ + setStrategy(Strategy)             │
│ + executeStrategy()                 │
│   └── strategy.execute()            │
└─────────────────────────────────────┘
              │
              │ has-a
              ▼
┌─────────────────────────────────────┐
│       <<interface>>                 │
│          Strategy                   │
├─────────────────────────────────────┤
│ + execute()                         │
└─────────────────────────────────────┘
              △
              │
     ┌────────┼────────┐
     │        │        │
┌─────────┐ ┌─────────┐ ┌─────────┐
│ StratA  │ │ StratB  │ │ StratC  │
├─────────┤ ├─────────┤ ├─────────┤
│+execute │ │+execute │ │+execute │
└─────────┘ └─────────┘ └─────────┘
```

**1. Strategy (전략)**
- 모든 전략에 대한 공통 인터페이스 정의
- Context가 전략을 실행하기 위해 사용하는 메서드 선언

**2. ConcreteStrategy (구체적 전략)**
- Strategy 인터페이스의 구체적 구현
- 특정 알고리즘을 캡슐화

**3. Context (컨텍스트)**
- Strategy 객체에 대한 참조를 유지
- 전략을 설정하고 실행하는 메서드 제공
- 알고리즘 선택을 클라이언트에 위임

## 구현 예제

### Python 예제 - 결제 시스템

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import Optional

# Strategy 인터페이스
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass
    
    @abstractmethod
    def get_payment_method(self) -> str:
        pass

# ConcreteStrategy - 신용카드 결제
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str, expiry: str):
        self._card_number = card_number
        self._cvv = cvv
        self._expiry = expiry
    
    def pay(self, amount: float) -> bool:
        masked_card = f"****-****-****-{self._card_number[-4:]}"
        print(f"  💳 신용카드 결제: {masked_card}")
        print(f"     금액: ₩{amount:,.0f}")
        print(f"     결제 승인됨")
        return True
    
    def get_payment_method(self) -> str:
        return "신용카드"

# ConcreteStrategy - PayPal 결제
class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self._email = email
    
    def pay(self, amount: float) -> bool:
        print(f"  📧 PayPal 결제: {self._email}")
        print(f"     금액: ₩{amount:,.0f}")
        print(f"     결제 승인됨")
        return True
    
    def get_payment_method(self) -> str:
        return "PayPal"

# ConcreteStrategy - 암호화폐 결제
class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet_address: str, crypto_type: str = "BTC"):
        self._wallet_address = wallet_address
        self._crypto_type = crypto_type
    
    def pay(self, amount: float) -> bool:
        # 환율 적용 (예시)
        crypto_amount = amount / 50000000  # 가상의 BTC 환율
        print(f"  🪙 {self._crypto_type} 결제")
        print(f"     지갑: {self._wallet_address[:10]}...")
        print(f"     금액: ₩{amount:,.0f} ({crypto_amount:.6f} {self._crypto_type})")
        print(f"     블록체인 트랜잭션 전송 중...")
        return True
    
    def get_payment_method(self) -> str:
        return f"암호화폐({self._crypto_type})"

# ConcreteStrategy - 계좌이체
class BankTransferPayment(PaymentStrategy):
    def __init__(self, bank_name: str, account_number: str):
        self._bank_name = bank_name
        self._account_number = account_number
    
    def pay(self, amount: float) -> bool:
        masked_account = f"***-***-{self._account_number[-4:]}"
        print(f"  🏦 계좌이체: {self._bank_name} {masked_account}")
        print(f"     금액: ₩{amount:,.0f}")
        print(f"     이체 완료")
        return True
    
    def get_payment_method(self) -> str:
        return "계좌이체"

# Context - 쇼핑 카트
class ShoppingCart:
    def __init__(self):
        self._items = []
        self._payment_strategy: Optional[PaymentStrategy] = None
    
    def add_item(self, name: str, price: float, quantity: int = 1):
        self._items.append({"name": name, "price": price, "quantity": quantity})
    
    def get_total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self._items)
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        self._payment_strategy = strategy
        print(f"\n결제 방식 설정: {strategy.get_payment_method()}")
    
    def checkout(self) -> bool:
        if not self._payment_strategy:
            print("결제 방식을 선택해주세요!")
            return False
        
        print("\n" + "="*50)
        print("주문 내역:")
        for item in self._items:
            subtotal = item["price"] * item["quantity"]
            print(f"  - {item['name']} x {item['quantity']}: ₩{subtotal:,.0f}")
        
        total = self.get_total()
        print(f"\n총 금액: ₩{total:,.0f}")
        print("="*50)
        
        print(f"\n{self._payment_strategy.get_payment_method()}로 결제 진행:")
        return self._payment_strategy.pay(total)

# 사용 예제
if __name__ == "__main__":
    # 장바구니 생성 및 상품 추가
    cart = ShoppingCart()
    cart.add_item("노트북", 1500000)
    cart.add_item("마우스", 50000)
    cart.add_item("키보드", 100000, 2)
    
    # 신용카드로 결제
    card_payment = CreditCardPayment("1234567890123456", "123", "12/25")
    cart.set_payment_strategy(card_payment)
    cart.checkout()
    
    print("\n" + "="*60 + "\n")
    
    # 같은 장바구니, 다른 결제 방식
    paypal_payment = PayPalPayment("user@example.com")
    cart.set_payment_strategy(paypal_payment)
    cart.checkout()
    
    print("\n" + "="*60 + "\n")
    
    # 암호화폐로 결제
    crypto_payment = CryptoPayment("1A2b3C4d5E6f7G8h9I0j", "ETH")
    cart.set_payment_strategy(crypto_payment)
    cart.checkout()
```

### Java 예제 - 정렬 전략

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// Strategy 인터페이스
interface SortStrategy<T extends Comparable<T>> {
    void sort(List<T> list);
    String getName();
}

// ConcreteStrategy - 버블 정렬
class BubbleSort<T extends Comparable<T>> implements SortStrategy<T> {
    @Override
    public void sort(List<T> list) {
        int n = list.size();
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (list.get(j).compareTo(list.get(j + 1)) > 0) {
                    T temp = list.get(j);
                    list.set(j, list.get(j + 1));
                    list.set(j + 1, temp);
                }
            }
        }
    }
    
    @Override
    public String getName() {
        return "버블 정렬 O(n²)";
    }
}

// ConcreteStrategy - 퀵 정렬
class QuickSort<T extends Comparable<T>> implements SortStrategy<T> {
    @Override
    public void sort(List<T> list) {
        quickSort(list, 0, list.size() - 1);
    }
    
    private void quickSort(List<T> list, int low, int high) {
        if (low < high) {
            int pi = partition(list, low, high);
            quickSort(list, low, pi - 1);
            quickSort(list, pi + 1, high);
        }
    }
    
    private int partition(List<T> list, int low, int high) {
        T pivot = list.get(high);
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (list.get(j).compareTo(pivot) < 0) {
                i++;
                T temp = list.get(i);
                list.set(i, list.get(j));
                list.set(j, temp);
            }
        }
        
        T temp = list.get(i + 1);
        list.set(i + 1, list.get(high));
        list.set(high, temp);
        
        return i + 1;
    }
    
    @Override
    public String getName() {
        return "퀵 정렬 O(n log n)";
    }
}

// ConcreteStrategy - 병합 정렬
class MergeSort<T extends Comparable<T>> implements SortStrategy<T> {
    @Override
    public void sort(List<T> list) {
        if (list.size() > 1) {
            List<T> sorted = mergeSort(list);
            for (int i = 0; i < sorted.size(); i++) {
                list.set(i, sorted.get(i));
            }
        }
    }
    
    private List<T> mergeSort(List<T> list) {
        if (list.size() <= 1) return list;
        
        int mid = list.size() / 2;
        List<T> left = mergeSort(new ArrayList<>(list.subList(0, mid)));
        List<T> right = mergeSort(new ArrayList<>(list.subList(mid, list.size())));
        
        return merge(left, right);
    }
    
    private List<T> merge(List<T> left, List<T> right) {
        List<T> result = new ArrayList<>();
        int i = 0, j = 0;
        
        while (i < left.size() && j < right.size()) {
            if (left.get(i).compareTo(right.get(j)) <= 0) {
                result.add(left.get(i++));
            } else {
                result.add(right.get(j++));
            }
        }
        
        while (i < left.size()) result.add(left.get(i++));
        while (j < right.size()) result.add(right.get(j++));
        
        return result;
    }
    
    @Override
    public String getName() {
        return "병합 정렬 O(n log n)";
    }
}

// Context - 정렬기
class Sorter<T extends Comparable<T>> {
    private SortStrategy<T> strategy;
    
    public void setStrategy(SortStrategy<T> strategy) {
        this.strategy = strategy;
    }
    
    public void sort(List<T> list) {
        if (strategy == null) {
            System.out.println("정렬 전략을 선택해주세요!");
            return;
        }
        
        System.out.println("\n" + strategy.getName() + " 실행");
        System.out.println("정렬 전: " + list);
        
        long startTime = System.nanoTime();
        strategy.sort(list);
        long endTime = System.nanoTime();
        
        System.out.println("정렬 후: " + list);
        System.out.printf("소요 시간: %.3f ms%n", (endTime - startTime) / 1_000_000.0);
    }
}

// 사용 예제
public class StrategyDemo {
    public static void main(String[] args) {
        Sorter<Integer> sorter = new Sorter<>();
        
        // 데이터 준비
        List<Integer> data1 = new ArrayList<>(Arrays.asList(64, 34, 25, 12, 22, 11, 90));
        List<Integer> data2 = new ArrayList<>(Arrays.asList(64, 34, 25, 12, 22, 11, 90));
        List<Integer> data3 = new ArrayList<>(Arrays.asList(64, 34, 25, 12, 22, 11, 90));
        
        // 버블 정렬
        sorter.setStrategy(new BubbleSort<>());
        sorter.sort(data1);
        
        // 퀵 정렬
        sorter.setStrategy(new QuickSort<>());
        sorter.sort(data2);
        
        // 병합 정렬
        sorter.setStrategy(new MergeSort<>());
        sorter.sort(data3);
    }
}
```

### C# 예제 - 할인 전략

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;

// Strategy 인터페이스
public interface IDiscountStrategy
{
    decimal CalculateDiscount(decimal originalPrice);
    string GetDescription();
}

// ConcreteStrategy - 정가 (할인 없음)
public class NoDiscount : IDiscountStrategy
{
    public decimal CalculateDiscount(decimal originalPrice)
    {
        return originalPrice;
    }
    
    public string GetDescription() => "정가 (할인 없음)";
}

// ConcreteStrategy - 퍼센트 할인
public class PercentageDiscount : IDiscountStrategy
{
    private readonly decimal _percentage;
    
    public PercentageDiscount(decimal percentage)
    {
        _percentage = percentage;
    }
    
    public decimal CalculateDiscount(decimal originalPrice)
    {
        return originalPrice * (1 - _percentage / 100);
    }
    
    public string GetDescription() => $"{_percentage}% 할인";
}

// ConcreteStrategy - 정액 할인
public class FixedAmountDiscount : IDiscountStrategy
{
    private readonly decimal _amount;
    
    public FixedAmountDiscount(decimal amount)
    {
        _amount = amount;
    }
    
    public decimal CalculateDiscount(decimal originalPrice)
    {
        return Math.Max(0, originalPrice - _amount);
    }
    
    public string GetDescription() => $"₩{_amount:N0} 할인";
}

// ConcreteStrategy - 멤버십 등급 할인
public class MembershipDiscount : IDiscountStrategy
{
    private readonly string _tier;
    private readonly decimal _discountRate;
    
    public MembershipDiscount(string tier)
    {
        _tier = tier;
        _discountRate = tier switch
        {
            "Bronze" => 5,
            "Silver" => 10,
            "Gold" => 15,
            "Platinum" => 20,
            "Diamond" => 25,
            _ => 0
        };
    }
    
    public decimal CalculateDiscount(decimal originalPrice)
    {
        return originalPrice * (1 - _discountRate / 100);
    }
    
    public string GetDescription() => $"{_tier} 회원 {_discountRate}% 할인";
}

// ConcreteStrategy - 시즌 세일
public class SeasonalDiscount : IDiscountStrategy
{
    private readonly string _season;
    private readonly decimal _discountRate;
    
    public SeasonalDiscount(string season)
    {
        _season = season;
        _discountRate = season switch
        {
            "BlackFriday" => 50,
            "Christmas" => 30,
            "Summer" => 20,
            "NewYear" => 25,
            _ => 10
        };
    }
    
    public decimal CalculateDiscount(decimal originalPrice)
    {
        return originalPrice * (1 - _discountRate / 100);
    }
    
    public string GetDescription() => $"{_season} 세일 {_discountRate}% 할인";
}

// Context - 주문
public class Order
{
    private IDiscountStrategy _discountStrategy;
    public string ProductName { get; set; }
    public decimal OriginalPrice { get; set; }
    
    public Order(string productName, decimal originalPrice)
    {
        ProductName = productName;
        OriginalPrice = originalPrice;
        _discountStrategy = new NoDiscount(); // 기본값
    }
    
    public void SetDiscountStrategy(IDiscountStrategy strategy)
    {
        _discountStrategy = strategy;
    }
    
    public decimal GetFinalPrice()
    {
        return _discountStrategy.CalculateDiscount(OriginalPrice);
    }
    
    public void PrintReceipt()
    {
        decimal finalPrice = GetFinalPrice();
        decimal savedAmount = OriginalPrice - finalPrice;
        
        Console.WriteLine("═══════════════════════════════════════");
        Console.WriteLine($"상품: {ProductName}");
        Console.WriteLine($"정가: ₩{OriginalPrice:N0}");
        Console.WriteLine($"적용 할인: {_discountStrategy.GetDescription()}");
        Console.WriteLine("───────────────────────────────────────");
        Console.WriteLine($"결제 금액: ₩{finalPrice:N0}");
        if (savedAmount > 0)
        {
            Console.WriteLine($"절약 금액: ₩{savedAmount:N0} ({savedAmount / OriginalPrice * 100:F1}%)");
        }
        Console.WriteLine("═══════════════════════════════════════\n");
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        var order = new Order("노트북 프로 15인치", 2000000m);
        
        Console.WriteLine("=== 다양한 할인 전략 적용 ===\n");
        
        // 정가
        order.SetDiscountStrategy(new NoDiscount());
        order.PrintReceipt();
        
        // 10% 할인
        order.SetDiscountStrategy(new PercentageDiscount(10));
        order.PrintReceipt();
        
        // 정액 30만원 할인
        order.SetDiscountStrategy(new FixedAmountDiscount(300000));
        order.PrintReceipt();
        
        // Gold 회원 할인
        order.SetDiscountStrategy(new MembershipDiscount("Gold"));
        order.PrintReceipt();
        
        // 블랙프라이데이 세일
        order.SetDiscountStrategy(new SeasonalDiscount("BlackFriday"));
        order.PrintReceipt();
    }
}
```

## 실제 사용 사례

### 1. Java Comparator
```java
Collections.sort(list, Comparator.comparing(User::getName));
Collections.sort(list, Comparator.comparing(User::getAge).reversed());
```

### 2. Python sorted()의 key 함수
```python
sorted(items, key=lambda x: x.price)
sorted(items, key=lambda x: x.name)
```

### 3. 압축 라이브러리
```python
# 다양한 압축 알고리즘 선택
compress(data, strategy=GzipStrategy())
compress(data, strategy=ZipStrategy())
```

### 4. 인증 방식
```java
// OAuth, JWT, Basic Auth 등
authService.setStrategy(new JWTStrategy());
authService.authenticate(credentials);
```

## 관련 패턴

| 패턴 | 전략과의 관계 |
|------|-------------|
| **State** | 둘 다 위임 사용, State는 상태 변화에 초점 |
| **Template Method** | 상속 vs 합성 방식의 차이 |
| **Command** | Command는 요청 캡슐화, Strategy는 알고리즘 캡슐화 |
| **Bridge** | 둘 다 합성 사용, Bridge는 구현과 추상화 분리 |

## FAQ

**Q1: 전략 패턴과 상태 패턴의 차이점은 무엇인가요?**

전략 패턴에서 클라이언트가 전략을 선택하고, 상태 패턴에서는 Context 내부에서 상태가 전이됩니다. 전략은 알고리즘 선택에 초점을, 상태는 객체의 상태 변화에 초점을 맞춥니다.

**Q2: 람다/함수형 프로그래밍으로 대체할 수 있나요?**

간단한 전략은 람다로 대체 가능합니다. 하지만 전략이 복잡하거나 상태를 가진다면 클래스로 구현하는 것이 좋습니다.

**Q3: 전략 객체는 어떻게 생성하나요?**

팩토리 패턴과 함께 사용하거나, DI 컨테이너를 통해 주입받을 수 있습니다. 설정 파일이나 환경 변수를 통해 동적으로 선택할 수도 있습니다.

**Q4: 전략이 Context의 데이터에 접근해야 한다면?**

전략 메서드의 매개변수로 필요한 데이터를 전달하거나, Context 자체를 전달할 수 있습니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- Java Comparator 문서