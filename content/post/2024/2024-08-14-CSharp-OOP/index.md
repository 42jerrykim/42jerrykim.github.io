---
image: "tmp_wordcloud.png"
categories: CSharp
date: "2024-08-14T00:00:00Z"
header: null

tags:
- CSharp
- ObjectOrientedProgramming
- OOP
- Programming
- SoftwareDevelopment
- Inheritance
- Polymorphism
- Encapsulation
- Abstraction
- Classes
- Methods
- Properties
- CodeReuse
- SoftwareDesign
- VisualStudio
- Unity
- GameDevelopment
- CSharpBasics
- ProgrammingConcepts
- SoftwareEngineering
- CodeMaintenance
- Debugging
- SoftwareArchitecture
- DesignPatterns
- ObjectModels
- DataHiding
- MethodOverriding
- MethodOverloading
- Interfaces
- Constructors
- Transactions
- BankAccount
- InterestEarningAccount
- LineOfCreditAccount
- GiftCardAccount
- CodeExamples
- ProgrammingTutorial
- SoftwareTesting
- CodeQuality
- BestPractices
- DevelopmentTools
- CodeStructure
- SoftwareLifecycle
- AgileDevelopment
- VersionControl
- GitHub
- CodeCollaboration
- SoftwareDocumentation
- LearningCSharp
teaser: /assets/images/undefined/teaser.jpg
title: '[C#] 객체 지향 프로그래밍(C#)'
aliases: /csharp/CSharp-OOP/
---

C#은 객체 지향 프로그래밍 언어로, 소프트웨어 개발에 있어 강력한 도구이다. 객체 지향 프로그래밍(OOP)의 네 가지 기본 원칙인 추상화, 캡슐화, 상속, 다형성을 통해 개발자는 코드의 재사용성과 유지보수성을 높일 수 있다. 이 문서에서는 C#을 사용하여 OOP의 개념을 실습하는 방법을 다룬다. 특히, `BankAccount` 클래스를 기반으로 다양한 계좌 유형을 생성하고, 각 계좌의 특성에 맞는 기능을 추가하는 과정을 통해 상속과 다형성을 활용하는 방법을 설명한다. 또한, C#의 클래스와 메서드를 정의하고, 객체를 생성하여 상호작용하는 방법을 배운다. 이 과정에서 코드의 구조화와 조직화의 중요성을 강조하며, OOP의 원칙이 실제 소프트웨어 개발에 어떻게 적용되는지를 보여준다. C#의 객체 지향 프로그래밍을 통해 복잡한 시스템을 효과적으로 설계하고 구현할 수 있는 방법을 익히게 될 것이다.




<!--
##### Outline #####
-->

<!--
---
## 객체 지향 프로그래밍(C#)
**소개**  
**C#의 객체 지향 프로그래밍 개념**  
**객체 지향 프로그래밍의 중요성**  
**이 문서의 내용 개요**  

## 객체 지향 프로그래밍의 기본 원칙
**추상화**  
**캡슐화**  
**상속**  
**다형성**  

## C#에서의 객체 지향 프로그래밍
**C#의 클래스와 객체**  
**C#의 접근 제한자**  
**C#의 인터페이스**  
**C#의 예외 처리**  

## C#을 이용한 객체 지향 프로그래밍 실습
**클래스 정의하기**  
**객체 생성하기**  
**상속과 다형성 활용하기**  
**인터페이스 사용하기**  

## 실용적인 예제
**은행 계좌 클래스 구현**  
**이자 소득 계좌 클래스**  
**신용 한도 계좌 클래스**  
**선불 선물 카드 계좌 클래스**  

## 자주 묻는 질문(FAQ)
**객체 지향 프로그래밍이란 무엇인가요?**  
**C#에서의 상속은 어떻게 작동하나요?**  
**다형성을 어떻게 활용할 수 있나요?**  
**캡슐화의 장점은 무엇인가요?**  

## 관련 기술
**C#과 .NET 프레임워크**  
**Unity와 C#의 관계**  
**Java와 C#의 객체 지향 프로그래밍 비교**  
**Python과 C#의 객체 지향 프로그래밍 비교**  

## 결론
**객체 지향 프로그래밍의 중요성 요약**  
**C#에서의 객체 지향 프로그래밍의 장점**  
**향후 학습 방향 제안**  
**마무리**  

---
-->

<!--
---
## 객체 지향 프로그래밍(C#)
**소개**  
**C#의 객체 지향 프로그래밍 개념**  
**객체 지향 프로그래밍의 중요성**  
**이 문서의 내용 개요**  
-->

## 객체 지향 프로그래밍(C#)

**소개**  

객체 지향 프로그래밍(Object-Oriented Programming, OOP)은 소프트웨어 개발에서 객체를 중심으로 설계하는 프로그래밍 패러다임이다. C#은 마이크로소프트에서 개발한 프로그래밍 언어로, 객체 지향 프로그래밍을 지원하는 강력한 기능을 제공한다. 이 문서에서는 C#에서의 객체 지향 프로그래밍의 기본 개념과 원칙, 그리고 실습 예제를 통해 이해를 돕고자 한다.

**C#의 객체 지향 프로그래밍 개념**  

C#에서 객체 지향 프로그래밍은 클래스와 객체를 기반으로 한다. 클래스는 객체의 설계도 역할을 하며, 객체는 클래스의 인스턴스이다. C#은 클래스, 상속, 다형성, 캡슐화와 같은 개념을 통해 개발자가 복잡한 소프트웨어를 보다 쉽게 관리하고 유지보수할 수 있도록 돕는다.

**객체 지향 프로그래밍의 중요성**  

객체 지향 프로그래밍은 코드의 재사용성을 높이고, 유지보수를 용이하게 하며, 코드의 가독성을 향상시키는 데 기여한다. 또한, 현실 세계의 객체를 모델링하여 소프트웨어를 설계할 수 있게 해주므로, 개발자들이 문제를 보다 직관적으로 이해하고 해결할 수 있도록 돕는다.

**이 문서의 내용 개요**  

이 문서에서는 객체 지향 프로그래밍의 기본 원칙과 C#에서의 구현 방법, 실습 예제, 자주 묻는 질문, 관련 기술, 그리고 결론을 다룰 예정이다. 각 섹션은 객체 지향 프로그래밍의 다양한 측면을 깊이 있게 탐구하며, 독자가 C#을 통해 객체 지향 프로그래밍을 이해하고 활용할 수 있도록 안내할 것이다.

<!--
## 객체 지향 프로그래밍의 기본 원칙
**추상화**  
**캡슐화**  
**상속**  
**다형성**  
-->

## 객체 지향 프로그래밍의 기본 원칙

**추상화**  

추상화는 복잡한 시스템을 단순화하는 과정이다. 이는 객체의 중요한 특성만을 강조하고 불필요한 세부 사항은 숨기는 방법이다. 예를 들어, 자동차라는 객체를 생각해보면, 우리는 자동차의 속도, 연료, 엔진 상태와 같은 중요한 속성만을 고려하고, 엔진 내부의 복잡한 기계적 구조는 신경 쓰지 않는다. C#에서는 추상 클래스를 사용하여 추상화를 구현할 수 있다. 추상 클래스는 인스턴스를 생성할 수 없지만, 자식 클래스에서 상속받아 사용할 수 있는 기본 구조를 제공한다.

**캡슐화**  

캡슐화는 객체의 상태를 보호하고, 객체의 내부 구현을 외부에서 접근하지 못하도록 하는 원칙이다. 이를 통해 객체의 데이터가 무분별하게 변경되는 것을 방지할 수 있다. C#에서는 접근 제한자를 사용하여 캡슐화를 구현한다. 예를 들어, `private` 접근 제한자를 사용하면 해당 클래스 내부에서만 접근할 수 있는 변수를 정의할 수 있다. 이렇게 하면 객체의 상태를 안전하게 유지할 수 있다.

**상속**  

상속은 기존 클래스의 속성과 메서드를 새로운 클래스가 물려받는 기능이다. 이를 통해 코드의 재사용성을 높이고, 계층 구조를 형성할 수 있다. C#에서는 `:` 기호를 사용하여 상속을 구현한다. 예를 들어, `Animal`이라는 기본 클래스가 있을 때, `Dog`라는 클래스는 `Animal` 클래스를 상속받아 `bark()` 메서드를 추가할 수 있다. 이렇게 하면 `Dog` 클래스는 `Animal` 클래스의 모든 속성과 메서드를 사용할 수 있다.

**다형성**  

다형성은 동일한 인터페이스를 통해 서로 다른 객체가 다르게 동작할 수 있는 능력이다. 이는 메서드 오버로딩과 메서드 오버라이딩을 통해 구현된다. C#에서는 기본 클래스에서 정의된 메서드를 자식 클래스에서 재정의하여 다형성을 활용할 수 있다. 예를 들어, `Shape`라는 기본 클래스가 있을 때, `Circle`과 `Square` 클래스는 `Shape` 클래스를 상속받아 `Draw()` 메서드를 각각 다르게 구현할 수 있다. 이렇게 하면 동일한 메서드 호출이지만, 객체의 종류에 따라 다른 동작을 수행하게 된다. 

이러한 기본 원칙들은 객체 지향 프로그래밍의 핵심 개념으로, C#을 포함한 많은 프로그래밍 언어에서 널리 사용된다. 이 원칙들을 이해하고 활용하는 것은 효과적인 소프트웨어 개발에 필수적이다.

<!--
## C#에서의 객체 지향 프로그래밍
**C#의 클래스와 객체**  
**C#의 접근 제한자**  
**C#의 인터페이스**  
**C#의 예외 처리**  
-->

## C#에서의 객체 지향 프로그래밍

**C#의 클래스와 객체**  

C#에서 클래스는 객체 지향 프로그래밍의 기본 단위이다. 클래스는 속성과 메서드를 포함할 수 있으며, 이를 통해 객체를 생성할 수 있다. 객체는 클래스의 인스턴스이며, 클래스에서 정의한 속성과 메서드를 사용할 수 있다. 예를 들어, `Car`라는 클래스를 정의하고, 이 클래스를 기반으로 `myCar`라는 객체를 생성할 수 있다. 

```csharp
public class Car
{
    public string Color { get; set; }
    public string Model { get; set; }

    public void Drive()
    {
        Console.WriteLine("The car is driving.");
    }
}

// 객체 생성
Car myCar = new Car();
myCar.Color = "Red";
myCar.Model = "Toyota";
myCar.Drive();
```

**C#의 접근 제한자**  

C#에서는 접근 제한자를 사용하여 클래스의 멤버에 대한 접근을 제어할 수 있다. 주요 접근 제한자는 `public`, `private`, `protected`, `internal`이 있다. `public`은 모든 클래스에서 접근할 수 있으며, `private`는 해당 클래스 내에서만 접근할 수 있다. `protected`는 상속받은 클래스에서 접근할 수 있고, `internal`은 같은 어셈블리 내에서 접근할 수 있다.

```csharp
public class Person
{
    private string name; // private 접근 제한자

    public void SetName(string name)
    {
        this.name = name; // public 메서드를 통해 접근
    }

    public string GetName()
    {
        return name;
    }
}
```

**C#의 인터페이스**  

인터페이스는 클래스가 구현해야 하는 메서드의 집합을 정의한다. 인터페이스는 다중 상속을 지원하며, 여러 클래스에서 동일한 인터페이스를 구현할 수 있다. 인터페이스는 `interface` 키워드를 사용하여 정의하며, 메서드의 구현은 포함하지 않는다.

```csharp
public interface IDriveable
{
    void Drive();
}

public class Car : IDriveable
{
    public void Drive()
    {
        Console.WriteLine("The car is driving.");
    }
}
```

**C#의 예외 처리**  

C#에서는 예외 처리를 위해 `try`, `catch`, `finally` 블록을 사용한다. `try` 블록 내에서 예외가 발생할 수 있는 코드를 작성하고, `catch` 블록에서 예외를 처리한다. `finally` 블록은 예외 발생 여부와 관계없이 항상 실행되는 코드를 포함한다.

```csharp
try
{
    int[] numbers = { 1, 2, 3 };
    Console.WriteLine(numbers[5]); // 예외 발생
}
catch (IndexOutOfRangeException ex)
{
    Console.WriteLine("Index was out of range: " + ex.Message);
}
finally
{
    Console.WriteLine("This block always executes.");
}
```

이와 같이 C#에서의 객체 지향 프로그래밍은 클래스와 객체, 접근 제한자, 인터페이스, 예외 처리 등을 통해 강력한 구조를 제공한다. 이러한 개념들은 소프트웨어 개발에서 코드의 재사용성과 유지보수성을 높이는 데 중요한 역할을 한다.

<!--
## C#을 이용한 객체 지향 프로그래밍 실습
**클래스 정의하기**  
**객체 생성하기**  
**상속과 다형성 활용하기**  
**인터페이스 사용하기**  
-->

## C#을 이용한 객체 지향 프로그래밍 실습

**클래스 정의하기**  

C#에서 클래스는 객체를 생성하기 위한 청사진 역할을 한다. 클래스는 속성과 메서드를 포함할 수 있으며, 이를 통해 객체의 상태와 행동을 정의할 수 있다. 클래스는 `class` 키워드를 사용하여 정의하며, 다음은 간단한 클래스 정의의 예이다.

```csharp
public class Car
{
    public string Model { get; set; }
    public int Year { get; set; }

    public void Drive()
    {
        Console.WriteLine($"{Model} is driving.");
    }
}
```

위의 예제에서 `Car` 클래스는 `Model`과 `Year`라는 두 개의 속성을 가지고 있으며, `Drive`라는 메서드를 통해 자동차가 주행하는 행동을 정의하고 있다.

**객체 생성하기**  

클래스를 정의한 후, 해당 클래스를 기반으로 객체를 생성할 수 있다. 객체는 클래스의 인스턴스이며, 클래스에서 정의한 속성과 메서드를 사용할 수 있다. 객체를 생성하는 방법은 다음과 같다.

```csharp
Car myCar = new Car();
myCar.Model = "Tesla Model S";
myCar.Year = 2022;
myCar.Drive();
```

위의 코드에서 `myCar`라는 객체를 생성하고, `Model`과 `Year` 속성을 설정한 후, `Drive` 메서드를 호출하여 자동차가 주행하는 메시지를 출력한다.

**상속과 다형성 활용하기**  

상속은 기존 클래스의 속성과 메서드를 새로운 클래스에서 재사용할 수 있게 해주는 기능이다. C#에서는 `:` 기호를 사용하여 상속을 구현할 수 있다. 다음은 상속을 활용한 예제이다.

```csharp
public class ElectricCar : Car
{
    public int BatteryLife { get; set; }

    public void Charge()
    {
        Console.WriteLine($"{Model} is charging.");
    }
}
```

위의 예제에서 `ElectricCar` 클래스는 `Car` 클래스를 상속받아 `BatteryLife` 속성과 `Charge` 메서드를 추가하였다. 이를 통해 전기차의 특성을 정의할 수 있다.

다형성은 동일한 메서드가 서로 다른 클래스에서 다르게 동작할 수 있게 해주는 개념이다. 이를 통해 코드의 유연성을 높일 수 있다. 다음은 다형성을 활용한 예제이다.

```csharp
public void TestDrive(Car car)
{
    car.Drive();
}

Car myCar = new Car();
ElectricCar myElectricCar = new ElectricCar();

TestDrive(myCar);
TestDrive(myElectricCar);
```

위의 코드에서 `TestDrive` 메서드는 `Car` 타입의 매개변수를 받아 해당 객체의 `Drive` 메서드를 호출한다. `myCar`와 `myElectricCar` 모두 `Car` 타입으로 처리되지만, 각각의 클래스에서 정의된 `Drive` 메서드가 호출된다.

**인터페이스 사용하기**  

인터페이스는 클래스가 구현해야 하는 메서드의 집합을 정의하는 계약이다. 인터페이스는 `interface` 키워드를 사용하여 정의하며, 클래스는 해당 인터페이스를 구현하여 메서드를 제공해야 한다. 다음은 인터페이스의 예제이다.

```csharp
public interface IDriveable
{
    void Drive();
}

public class Bicycle : IDriveable
{
    public void Drive()
    {
        Console.WriteLine("Bicycle is pedaling.");
    }
}
```

위의 예제에서 `IDriveable` 인터페이스는 `Drive` 메서드를 정의하고 있으며, `Bicycle` 클래스는 이를 구현하여 자전거의 주행 행동을 정의하고 있다. 인터페이스를 사용하면 서로 다른 클래스들이 동일한 메서드를 구현할 수 있어 코드의 일관성을 유지할 수 있다.

이와 같이 C#을 이용한 객체 지향 프로그래밍 실습을 통해 클래스, 객체, 상속, 다형성, 인터페이스의 개념을 이해하고 활용할 수 있다. 이러한 개념들은 소프트웨어 개발에서 코드의 재사용성과 유지보수성을 높이는 데 중요한 역할을 한다.

<!--
## 실용적인 예제
**은행 계좌 클래스 구현**  
**이자 소득 계좌 클래스**  
**신용 한도 계좌 클래스**  
**선불 선물 카드 계좌 클래스**  
-->

## 실용적인 예제

**은행 계좌 클래스 구현**  

은행 계좌 클래스를 구현하는 것은 객체 지향 프로그래밍의 기본 개념을 이해하는 데 매우 유용하다. 이 클래스는 계좌의 속성과 기능을 정의한다. 예를 들어, 계좌 번호, 계좌 소유자, 잔액 등의 속성을 가질 수 있다. 또한, 입금, 출금, 잔액 조회와 같은 메서드를 포함할 수 있다. 아래는 C#으로 은행 계좌 클래스를 구현한 예제 코드이다.

```csharp
public class BankAccount
{
    public string AccountNumber { get; set; }
    public string AccountHolder { get; set; }
    private decimal balance;

    public BankAccount(string accountNumber, string accountHolder)
    {
        AccountNumber = accountNumber;
        AccountHolder = accountHolder;
        balance = 0;
    }

    public void Deposit(decimal amount)
    {
        if (amount > 0)
        {
            balance += amount;
            Console.WriteLine($"{amount}원이 입금되었습니다. 현재 잔액: {balance}원");
        }
        else
        {
            Console.WriteLine("입금 금액은 0보다 커야 합니다.");
        }
    }

    public void Withdraw(decimal amount)
    {
        if (amount > 0 && amount <= balance)
        {
            balance -= amount;
            Console.WriteLine($"{amount}원이 출금되었습니다. 현재 잔액: {balance}원");
        }
        else
        {
            Console.WriteLine("출금 금액이 유효하지 않습니다.");
        }
    }

    public decimal GetBalance()
    {
        return balance;
    }
}
```

**이자 소득 계좌 클래스**  

이자 소득 계좌 클래스는 기본 은행 계좌 클래스를 상속받아 이자 계산 기능을 추가한 것이다. 이 클래스는 이자율을 속성으로 가지고 있으며, 이자를 계산하는 메서드를 포함한다. 아래는 이자 소득 계좌 클래스를 구현한 예제 코드이다.

```csharp
public class SavingsAccount : BankAccount
{
    public decimal InterestRate { get; set; }

    public SavingsAccount(string accountNumber, string accountHolder, decimal interestRate)
        : base(accountNumber, accountHolder)
    {
        InterestRate = interestRate;
    }

    public void AddInterest()
    {
        decimal interest = GetBalance() * InterestRate;
        Deposit(interest);
        Console.WriteLine($"이자가 추가되었습니다: {interest}원");
    }
}
```

**신용 한도 계좌 클래스**  

신용 한도 계좌 클래스는 기본 은행 계좌 클래스를 상속받아 신용 한도를 추가한 것이다. 이 클래스는 신용 한도를 속성으로 가지고 있으며, 출금 시 신용 한도를 초과하지 않도록 하는 기능을 포함한다. 아래는 신용 한도 계좌 클래스를 구현한 예제 코드이다.

```csharp
public class CreditAccount : BankAccount
{
    public decimal CreditLimit { get; set; }

    public CreditAccount(string accountNumber, string accountHolder, decimal creditLimit)
        : base(accountNumber, accountHolder)
    {
        CreditLimit = creditLimit;
    }

    public new void Withdraw(decimal amount)
    {
        if (amount > 0 && (GetBalance() + CreditLimit) >= amount)
        {
            base.Withdraw(amount);
        }
        else
        {
            Console.WriteLine("신용 한도를 초과할 수 없습니다.");
        }
    }
}
```

**선불 선물 카드 계좌 클래스**  

선불 선물 카드 계좌 클래스는 특정 금액이 충전된 카드 계좌를 나타낸다. 이 클래스는 잔액이 0이 될 때까지 출금할 수 있는 기능을 포함한다. 아래는 선불 선물 카드 계좌 클래스를 구현한 예제 코드이다.

```csharp
public class GiftCardAccount : BankAccount
{
    public GiftCardAccount(string accountNumber, string accountHolder, decimal initialBalance)
        : base(accountNumber, accountHolder)
    {
        Deposit(initialBalance);
    }
}
```

이와 같이 다양한 계좌 클래스를 구현함으로써 객체 지향 프로그래밍의 원칙을 실제로 적용할 수 있다. 각 클래스는 서로 다른 기능을 가지며, 상속과 다형성을 통해 코드의 재사용성을 높일 수 있다.

<!--
## 자주 묻는 질문(FAQ)
**객체 지향 프로그래밍이란 무엇인가요?**  
**C#에서의 상속은 어떻게 작동하나요?**  
**다형성을 어떻게 활용할 수 있나요?**  
**캡슐화의 장점은 무엇인가요?**  
-->

## 자주 묻는 질문(FAQ)

**객체 지향 프로그래밍이란 무엇인가요?**  

객체 지향 프로그래밍(Object-Oriented Programming, OOP)은 소프트웨어 설계 패러다임 중 하나로, 프로그램을 객체(object)라는 단위로 구성하는 방법이다. 객체는 데이터와 그 데이터를 처리하는 메서드를 포함하고 있으며, 이를 통해 코드의 재사용성과 유지보수성을 높일 수 있다. OOP는 주로 클래스(class)와 객체(object)를 기반으로 하며, 추상화, 캡슐화, 상속, 다형성의 네 가지 기본 원칙을 따른다. 이러한 원칙들은 프로그램의 구조를 명확하게 하고, 복잡한 문제를 더 쉽게 해결할 수 있도록 돕는다.

**C#에서의 상속은 어떻게 작동하나요?**  

C#에서 상속은 한 클래스가 다른 클래스의 속성과 메서드를 물려받는 기능이다. 이를 통해 코드의 재사용성을 높이고, 계층적인 관계를 형성할 수 있다. 상속을 통해 자식 클래스는 부모 클래스의 모든 기능을 사용할 수 있으며, 필요에 따라 부모 클래스의 메서드를 오버라이드(override)하여 자신만의 기능을 추가할 수 있다. C#에서는 단일 상속만 지원하지만, 인터페이스를 통해 다중 상속의 효과를 얻을 수 있다. 상속을 활용하면 코드의 중복을 줄이고, 유지보수를 용이하게 할 수 있다.

**다형성을 어떻게 활용할 수 있나요?**  

다형성(Polymorphism)은 동일한 인터페이스를 통해 서로 다른 객체를 처리할 수 있는 능력을 의미한다. C#에서는 메서드 오버로딩(method overloading)과 메서드 오버라이딩(method overriding)을 통해 다형성을 구현할 수 있다. 메서드 오버로딩은 같은 이름의 메서드를 매개변수의 타입이나 개수에 따라 다르게 정의하는 것이고, 메서드 오버라이딩은 부모 클래스의 메서드를 자식 클래스에서 재정의하는 것이다. 다형성을 활용하면 코드의 유연성을 높이고, 다양한 객체를 일관된 방식으로 처리할 수 있다.

**캡슐화의 장점은 무엇인가요?**  

캡슐화(Encapsulation)는 객체의 상태(데이터)를 외부에서 직접 접근하지 못하도록 숨기고, 대신 공개된 메서드를 통해 접근하도록 하는 원칙이다. C#에서는 접근 제한자(access modifier)를 사용하여 캡슐화를 구현할 수 있다. 캡슐화의 주요 장점은 데이터의 무결성을 보호하고, 객체의 내부 구현을 변경하더라도 외부에 미치는 영향을 최소화할 수 있다는 것이다. 또한, 캡슐화를 통해 객체의 사용 방법을 명확히 하고, 코드의 가독성을 높일 수 있다.

<!--
## 관련 기술
**C#과 .NET 프레임워크**  
**Unity와 C#의 관계**  
**Java와 C#의 객체 지향 프로그래밍 비교**  
**Python과 C#의 객체 지향 프로그래밍 비교**  
-->

## 관련 기술

**C#과 .NET 프레임워크**  

C#은 마이크로소프트에서 개발한 프로그래밍 언어로, .NET 프레임워크와 함께 사용된다. .NET 프레임워크는 다양한 프로그래밍 언어를 지원하며, C#은 그 중 하나로, 강력한 객체 지향 프로그래밍 기능을 제공한다. .NET 프레임워크는 다양한 라이브러리와 API를 제공하여 개발자가 복잡한 애플리케이션을 쉽게 구축할 수 있도록 돕는다. C#과 .NET 프레임워크의 결합은 웹 애플리케이션, 데스크톱 애플리케이션, 모바일 애플리케이션 등 다양한 플랫폼에서의 개발을 가능하게 한다. 

**Unity와 C#의 관계**  

Unity는 게임 개발을 위한 강력한 엔진으로, C#을 주요 스크립팅 언어로 사용한다. Unity에서 C#을 사용하면 게임의 로직, 물리 엔진, 사용자 인터페이스 등을 구현할 수 있다. C#의 객체 지향 프로그래밍 특성 덕분에 Unity에서 복잡한 게임 구조를 쉽게 관리할 수 있으며, 재사용 가능한 코드 작성이 가능하다. Unity와 C#의 조합은 게임 개발자들에게 매우 인기가 있으며, 많은 게임이 이 두 기술을 기반으로 개발되고 있다.

**Java와 C#의 객체 지향 프로그래밍 비교**  

Java와 C#은 모두 객체 지향 프로그래밍 언어로, 많은 유사점을 가지고 있다. 두 언어 모두 클래스와 객체, 상속, 다형성 등의 개념을 지원하며, 강력한 타입 시스템을 제공한다. 그러나 두 언어는 몇 가지 차이점도 존재한다. 예를 들어, C#은 프로퍼티와 이벤트를 지원하여 더 간결한 코드 작성을 가능하게 하며, Java는 플랫폼 독립성을 강조하여 JVM에서 실행된다. 이러한 차이점은 개발자가 선택할 때 고려해야 할 중요한 요소가 된다.

**Python과 C#의 객체 지향 프로그래밍 비교**  

Python과 C#은 각각의 장점과 단점을 가진 객체 지향 프로그래밍 언어이다. Python은 동적 타이핑을 지원하여 코드 작성이 간편하고, 문법이 간결하여 배우기 쉽다. 반면, C#은 정적 타이핑을 지원하여 컴파일 시 오류를 미리 발견할 수 있는 장점이 있다. 또한, C#은 강력한 IDE 지원과 .NET 생태계의 다양한 라이브러리를 활용할 수 있어 대규모 애플리케이션 개발에 유리하다. 두 언어는 각각의 용도에 따라 적합한 선택이 될 수 있다. 

--- 

이와 같이 C#과 관련된 다양한 기술들을 살펴보았다. 각 기술은 객체 지향 프로그래밍의 원칙을 바탕으로 하여 개발자에게 유용한 도구와 환경을 제공한다. C#을 배우고 활용하는 과정에서 이러한 기술들을 이해하고 활용하는 것이 중요하다.

<!--
## 결론
**객체 지향 프로그래밍의 중요성 요약**  
**C#에서의 객체 지향 프로그래밍의 장점**  
**향후 학습 방향 제안**  
**마무리**  
-->

## 결론

**객체 지향 프로그래밍의 중요성 요약**  

객체 지향 프로그래밍(OOP)은 소프트웨어 개발에서 매우 중요한 개념이다. OOP는 코드의 재사용성을 높이고, 유지보수를 용이하게 하며, 복잡한 시스템을 더 쉽게 관리할 수 있도록 돕는다. 이러한 특성 덕분에 OOP는 대규모 소프트웨어 프로젝트에서 널리 사용되고 있다. OOP의 기본 원칙인 추상화, 캡슐화, 상속, 다형성은 개발자들이 더 효율적으로 코드를 작성하고, 문제를 해결할 수 있도록 해준다. 

**C#에서의 객체 지향 프로그래밍의 장점**  

C#은 객체 지향 프로그래밍을 지원하는 강력한 언어로, 다양한 기능을 제공한다. C#의 클래스와 객체는 개발자가 복잡한 문제를 해결하는 데 필요한 구조를 제공하며, 접근 제한자는 데이터 보호를 가능하게 한다. 또한, C#의 인터페이스는 다형성을 구현하는 데 유용하며, 예외 처리는 프로그램의 안정성을 높인다. 이러한 장점 덕분에 C#은 게임 개발, 웹 애플리케이션, 데스크톱 애플리케이션 등 다양한 분야에서 널리 사용되고 있다.

**향후 학습 방향 제안**  

객체 지향 프로그래밍을 더 깊이 이해하기 위해서는 다양한 프로젝트를 통해 실습하는 것이 중요하다. C#의 다양한 라이브러리와 프레임워크를 활용하여 실제 애플리케이션을 개발해보는 것이 좋다. 또한, 다른 프로그래밍 언어와의 비교를 통해 OOP의 개념을 더욱 확고히 할 수 있다. 예를 들어, Java나 Python과 같은 언어에서의 OOP 구현 방식을 살펴보는 것도 유익하다. 

**마무리**  

객체 지향 프로그래밍은 현대 소프트웨어 개발의 핵심 개념 중 하나이다. C#을 통해 OOP의 원리를 배우고, 이를 실제 프로젝트에 적용함으로써 개발자로서의 역량을 키울 수 있다. 앞으로도 지속적인 학습과 실습을 통해 OOP의 깊이를 더해 나가길 바란다.

<!--
##### Reference #####
-->

## Reference


* [https://learn.microsoft.com/ko-kr/dotnet/csharp/fundamentals/tutorials/oop](https://learn.microsoft.com/ko-kr/dotnet/csharp/fundamentals/tutorials/oop)
* [https://nybot-house.tistory.com/105](https://nybot-house.tistory.com/105)
* [https://koco-pot.co.kr/c-%EC%96%B8%EC%96%B4%EC%9D%98-%EA%B0%9D%EC%B2%B4-%EC%A7%80%ED%96%A5-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EA%B0%9C%EB%85%90%EA%B3%BC-%EC%8B%A4%EC%8A%B5-%EB%B0%A9%EB%B2%95/](https://koco-pot.co.kr/c-%EC%96%B8%EC%96%B4%EC%9D%98-%EA%B0%9D%EC%B2%B4-%EC%A7%80%ED%96%A5-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EA%B0%9C%EB%85%90%EA%B3%BC-%EC%8B%A4%EC%8A%B5-%EB%B0%A9%EB%B2%95/)
* [https://nybot-house.tistory.com/104](https://nybot-house.tistory.com/104)
* [https://geukggom.tistory.com/100](https://geukggom.tistory.com/100)


<!--
#  객체 지향 프로그래밍(C#)

##  이 문서의 내용

C#은 객체 지향 프로그래밍 언어입니다. 객체 지향 프로그래밍의 네 가지 기본 원칙은 다음과 같습니다.

  * 추상화 - 관련 특성 및 엔터티의 상호 작용을 클래스로 모델링하여 시스템의 추상적 표현을 정의합니다. 
  * 캡슐화 - 객체의 내부 상태와 기능을 숨기고 public 함수 세트를 통해서만 객체에 액세스할 수 있습니다. 
  * 상속 - 기존 추상화를 기반으로 새 추상화를 만들 수 있습니다. 
  * 다형성 - 여러 추상화에서 다양한 방법으로 상속된 속성 또는 메서드를 구현할 수 있습니다. 

앞의 [ 클래스 소개 ](classes) 자습서에서 추상화와 캡슐화를 살펴봤습니다. ` BankAccount ` 클래스는 은행 계좌 개념에
대한 추상화를 제공했습니다. ` BankAccount ` 클래스를 사용한 코드에 영향을 주지 않고 해당 구현을 수정할 수 있습니다. `
BankAccount ` 및 ` Transaction ` 클래스는 코드에서 이러한 개념을 설명하는 데 필요한 구성 요소의 캡슐화를
제공합니다.

이 자습서에서는 상속과 다형성을 활용하도록 이 애플리케이션을 확장해 새 기능을 추가합니다. 또한 ` BankAccount ` 클래스에 기능을
추가하여 앞의 자습서에서 배운 추상화 및 캡슐화 방법을 활용합니다.

##  다른 유형의 계좌 만들기

이 프로그램을 빌드한 후 기능 추가를 요청 받습니다. 이 프로그램은 은행 계좌 유형이 하나뿐인 상황에서는 잘 작동합니다. 시간이 지나면서
요구 사항이 바뀌고 관련된 다음과 같은 계정 유형이 요청됩니다.

  * 매월말에 이자가 붙는 이자 소득 계좌. 
  * 잔고가 음수일 수 있지만 잔고가 있는 경우 매달 이자 비용이 발생하는 신용 한도. 
  * 1회 예치로 시작하고 지불만 가능한 선불 선물 카드 계좌. 이 계좌는 매월초에 한 번 잔고를 다시 채울 수 있습니다. 

이 모든 다양한 계좌는 이전 자습서에서 정의한 ` BankAccount ` 클래스와 비슷합니다. 해당 코드를 복사하고 클래스 이름을 바꾸고
수정할 수도 있습니다. 이 방법은 단기적으로는 효과가 있지만 시간이 지남에 따라 작업이 늘어납니다. 모든 변경 내용은 영향을 받는 모든
클래스에 복사됩니다.

대신 이전 자습서에서 만든 ` BankAccount ` 클래스에서 메서드와 데이터를 상속하는 새 은행 계좌 유형을 만들 수 있습니다. 이러한
새 클래스는 각 유형에 필요한 특정 동작으로 ` BankAccount ` 클래스를 확장할 수 있습니다.

    
    
    public class InterestEarningAccount : BankAccount
    {
    }
    
    public class LineOfCreditAccount : BankAccount
    {
    }
    
    public class GiftCardAccount : BankAccount
    {
    }
    

이러한 각 클래스는 공유 기본 클래스인 ` BankAccount ` 클래스에서 공유 동작을 상속합니다. 파생 클래스 각각에 새롭고 다양한
기능의 구현을 작성합니다. 이러한 파생 클래스에는 이미 ` BankAccount ` 클래스에 정의된 동작이 모두 있습니다.

각각의 새 클래스는 서로 다른 소스 파일에 만드는 것이 좋습니다. [ Visual Studio
](https://visualstudio.com) 에서 프로젝트를 마우스 오른쪽 단추로 클릭하고 클래스 추가를 선택하여 새 파일에 새
클래스를 추가할 수 있습니다. [ Visual Studio Code ](https://code.visualstudio.com) 에서는 파일을
선택한 다음 새로 만들기를 선택하여 새 원본 파일을 만듭니다. 어느 도구에서나 클래스와 일치하도록 파일 이름을 지정합니다.
_InterestEarningAccount.cs_ , _LineOfCreditAccount.cs_ , _GiftCardAccount.cs_
.

위의 샘플에 나온 것처럼 클래스를 만들면 파생 클래스가 컴파일되지 않는 것을 확인할 수 있습니다. 생성자는 객체를 초기화합니다. 파생 클래스
생성자는 파생 클래스를 초기화하고 파생 클래스에 포함된 기본 클래스 객체를 초기화하는 방법에 대한 지침을 제공해야 합니다. 적절한 초기화는
일반적으로 추가 코드 없이 발생합니다. ` BankAccount ` 클래스는 다음 서명을 사용하여 하나의 공용 생성자를 선언합니다.

    
    
    public BankAccount(string name, decimal initialBalance)
    

컴파일러는 사용자가 직접 생성자를 정의할 때 기본 생성자를 생성하지 않습니다. 즉, 각 파생 클래스가 이 생성자를 명시적으로 호출해야
합니다. 기본 클래스 생성자에 인수를 전달할 수 있는 생성자를 선언합니다. 다음 코드는 ` InterestEarningAccount ` 의
생성자를 보여 줍니다.

    
    
    public InterestEarningAccount(string name, decimal initialBalance) : base(name, initialBalance)
    {
    }
    

이 새로운 생성자의 매개 변수는 기본 클래스 생성자의 매개 변수 형식 및 이름과 일치합니다. ` : base() ` 구문을 사용하여 기본
클래스 생성자에 대한 호출을 나타낼 수 있습니다. 일부 클래스는 여러 생성자를 정의하며, 이 구문을 사용하면 호출하는 기본 클래스 생성자를
선택할 수 있습니다. 생성자를 업데이트한 후 각 파생 클래스의 코드를 개발할 수 있습니다. 새 클래스에 대한 요구 사항은 다음과 같이 지정할
수 있습니다.

  * 이자 소득 계좌: 
    * 월말 잔고의 2%에 해당하는 예금을 얻게 됩니다. 
  * 신용 한도: 
    * 음수의 잔고일 수 있지만 절대값은 대출 한도보다 클 수 없습니다. 
    * 월말 잔고가 0이 아닌 경우 매달 이자 비용이 발생합니다. 
    * 대출 한도를 초과하는 인출 때마다 수수료가 발생합니다. 
  * 선물 카드 계좌: 
    * 매월 한 번 말일에 지정된 금액으로 계좌를 다시 채울 수 있습니다. 

이러한 계좌 유형 세 가지 모두 월말에 발생하는 작업이 있음을 볼 수 있습니다. 하지만 계좌 유형마다 수행하는 작업은 다릅니다. 다형성을
사용하여 이 코드를 구현합니다. ` BankAccount ` 클래스에서 단일 ` virtual ` 메서드를 만듭니다.

    
    
    public virtual void PerformMonthEndTransactions() { }
    

앞의 코드는 ` virtual ` 키워드를 사용하여 파생 클래스가 다른 구현을 제공할 수 있는 기본 클래스에서 메서드를 선언하는 방법을 보여
줍니다. ` virtual ` 메서드는 파생 클래스가 다시 구현하도록 선택할 수 있는 메서드입니다. 파생 클래스는 ` override `
키워드를 사용하여 새 구현을 정의합니다. 일반적으로 이것을 “기본 클래스 구현 재정의”라고 합니다. ` virtual ` 키워드는 파생
클래스가 동작을 재정의할 수 있도록 지정합니다. 파생 클래스가 동작을 재정의해야 하는 ` abstract ` 메서드를 선언할 수도 있습니다.
기본 클래스는 ` abstract ` 메서드의 구현을 제공하지 않습니다. 다음으로 만든 새로운 두 클래스의 구현을 정의해야 합니다. `
InterestEarningAccount ` 로 시작합니다.

    
    
    public override void PerformMonthEndTransactions()
    {
        if (Balance > 500m)
        {
            decimal interest = Balance * 0.02m;
            MakeDeposit(interest, DateTime.Now, "apply monthly interest");
        }
    }
    

` LineOfCreditAccount ` 에 다음 코드를 추가합니다. 이 코드는 계좌에서 인출되는 양수의 이자 비용을 계산하기 위해 잔고를
무효화합니다.

    
    
    public override void PerformMonthEndTransactions()
    {
        if (Balance < 0)
        {
            // Negate the balance to get a positive interest charge:
            decimal interest = -Balance * 0.07m;
            MakeWithdrawal(interest, DateTime.Now, "Charge monthly interest");
        }
    }
    

` GiftCardAccount ` 클래스가 해당 월말 기능을 구현하려면 두 가지 변경이 필요합니다. 먼저 매월 더할 선택적 금액을
포함하도록 생성자를 수정합니다.

    
    
    private readonly decimal _monthlyDeposit = 0m;
    
    public GiftCardAccount(string name, decimal initialBalance, decimal monthlyDeposit = 0) : base(name, initialBalance)
        => _monthlyDeposit = monthlyDeposit;
    

생성자는 ` monthlyDeposit ` 값의 기본값을 제공하므로 호출자는 월별 예치금이 없는 ` 0 ` 을 생략할 수 있습니다. 다음으로
생성자에서 0이 아닌 값으로 설정된 경우 월별 예치금을 추가하도록 ` PerformMonthEndTransactions ` 메서드를
재정의합니다.

    
    
    public override void PerformMonthEndTransactions()
    {
        if (_monthlyDeposit != 0)
        {
            MakeDeposit(_monthlyDeposit, DateTime.Now, "Add monthly deposit");
        }
    }
    

재정의는 생성자에서 설정된 월별 예치금을 적용합니다. ` Main ` 메서드에 다음 코드를 추가하여 ` GiftCardAccount ` 및
` InterestEarningAccount ` 에 대한 이러한 변경을 테스트합니다.

    
    
    var giftCard = new GiftCardAccount("gift card", 100, 50);
    giftCard.MakeWithdrawal(20, DateTime.Now, "get expensive coffee");
    giftCard.MakeWithdrawal(50, DateTime.Now, "buy groceries");
    giftCard.PerformMonthEndTransactions();
    // can make additional deposits:
    giftCard.MakeDeposit(27.50m, DateTime.Now, "add some additional spending money");
    Console.WriteLine(giftCard.GetAccountHistory());
    
    var savings = new InterestEarningAccount("savings account", 10000);
    savings.MakeDeposit(750, DateTime.Now, "save some money");
    savings.MakeDeposit(1250, DateTime.Now, "Add more savings");
    savings.MakeWithdrawal(250, DateTime.Now, "Needed to pay monthly bills");
    savings.PerformMonthEndTransactions();
    Console.WriteLine(savings.GetAccountHistory());
    

결과를 확인합니다. 이제 ` LineOfCreditAccount ` 에 대한 유사한 테스트 코드 집합을 추가합니다.

    
    
    var lineOfCredit = new LineOfCreditAccount("line of credit", 0);
    // How much is too much to borrow?
    lineOfCredit.MakeWithdrawal(1000m, DateTime.Now, "Take out monthly advance");
    lineOfCredit.MakeDeposit(50m, DateTime.Now, "Pay back small amount");
    lineOfCredit.MakeWithdrawal(5000m, DateTime.Now, "Emergency funds for repairs");
    lineOfCredit.MakeDeposit(150m, DateTime.Now, "Partial restoration on repairs");
    lineOfCredit.PerformMonthEndTransactions();
    Console.WriteLine(lineOfCredit.GetAccountHistory());
    

앞의 코드를 추가하고 프로그램을 실행하면 다음과 같은 오류가 표시됩니다.

    
    
    Unhandled exception. System.ArgumentOutOfRangeException: Amount of deposit must be positive (Parameter 'amount')
       at OOProgramming.BankAccount.MakeDeposit(Decimal amount, DateTime date, String note) in BankAccount.cs:line 42
       at OOProgramming.BankAccount..ctor(String name, Decimal initialBalance) in BankAccount.cs:line 31
       at OOProgramming.LineOfCreditAccount..ctor(String name, Decimal initialBalance) in LineOfCreditAccount.cs:line 9
       at OOProgramming.Program.Main(String[] args) in Program.cs:line 29
    

참고

실제 출력에는 프로젝트와 함께 폴더의 전체 경로가 포함됩니다. 간단히 하기 위해 폴더 이름이 생략되었습니다. 또한 코드 형식에 따라 줄
번호가 약간 다를 수 있습니다.

` BankAccount ` 는 초기 잔고가 0보다 커야 한다고 가정하기 때문에 이 코드는 실패합니다. ` BankAccount ` 클래스에
베이킹된 또 다른 가정은 잔고는 음수가 될 수 없다는 것입니다. 대신 계좌 잔고를 초과하는 인출은 거부됩니다. 두 가지 가정 모두 변경해야
합니다. 신용 한도 계좌는 0에서 시작하며, 일반적으로 음수의 잔고를 갖습니다. 또한 고객이 너무 많은 비용을 빌리는 경우 수수료가
발생합니다. 트랜잭션은 허용되지만 비용이 더 많이 듭니다. 첫 번째 규칙은 최소 잔고를 지정하는 ` BankAccount ` 생성자에 선택적
인수를 추가하여 구현할 수 있습니다. 기본값은 ` 0 ` 입니다. 두 번째 규칙에는 파생 클래스가 기본 알고리즘을 수정할 수 있도록 하는
메커니즘이 필요합니다. 어떤 면에서 기본 클래스는 초과 인출이 있을 때 수행해야 하는 작업을 파생 형식에게 ‘물어봅니다’. 기본 동작은
예외를 throw하여 트랜잭션을 거부하는 것입니다.

선택적 ` minimumBalance ` 매개 변수를 포함하는 두 번째 생성자를 추가하여 시작해 보겠습니다. 이 새 생성자는 기존 생성자가
수행하는 모든 작업을 수행합니다. 또한 최소 잔고 속성을 설정합니다. 기존 생성자의 본문을 복사할 수 있지만 나중에 두 위치가 변경될 수
있습니다. 대신 생성자 연결을 사용하여 한 생성자가 다른 생성자를 호출하도록 할 수 있습니다. 다음 코드는 두 개의 생성자와 새 추가 필드를
보여 줍니다.

    
    
    private readonly decimal _minimumBalance;
    
    public BankAccount(string name, decimal initialBalance) : this(name, initialBalance, 0) { }
    
    public BankAccount(string name, decimal initialBalance, decimal minimumBalance)
    {
        Number = s_accountNumberSeed.ToString();
        s_accountNumberSeed++;
    
        Owner = name;
        _minimumBalance = minimumBalance;
        if (initialBalance > 0)
            MakeDeposit(initialBalance, DateTime.Now, "Initial balance");
    }
    

앞의 코드는 두 가지 새로운 방법을 보여 줍니다. 첫째, ` minimumBalance ` 필드는 ` readonly ` 로 표시됩니다.
즉, 객체가 생성된 후에는 값을 변경할 수 없습니다. ` BankAccount ` 가 만들어지면 ` minimumBalance ` 를 변경할
수 없습니다. 둘째, 두 매개 변수를 취하는 생성자는 ` : this(name, initialBalance, 0) { } ` 를 구현으로
사용합니다. ` : this() ` 식은 매개 변수가 세 개인 다른 생성자를 호출합니다. 이 방법을 사용하면 클라이언트 코드가 여러 생성자
중 하나를 선택할 수 있더라도 객체 초기화에 단일 구현을 사용할 수 있습니다.

이 구현은 초기 잔고가 ` 0 ` 보다 큰 경우에만 ` MakeDeposit ` 을 호출합니다. 그러면 예치금은 양수여야 한다는 규칙이
유지되지만 신용 계정이 ` 0 ` 의 잔고로 열립니다.

이제 ` BankAccount ` 클래스에 최소 잔고에 대한 읽기 전용 필드가 있으므로 마지막 변경은 ` MakeWithdrawal `
메서드에서 하드 코드를 ` 0 ` 에서 ` minimumBalance ` 로 변경하는 것입니다.

    
    
    if (Balance - amount < _minimumBalance)
    

` BankAccount ` 클래스를 확장한 후 다음 코드에 나온 것처럼 새 기본 생성자를 호출하도록 ` LineOfCreditAccount
` 생성자를 수정할 수 있습니다.

    
    
    public LineOfCreditAccount(string name, decimal initialBalance, decimal creditLimit) : base(name, initialBalance, -creditLimit)
    {
    }
    

` LineOfCreditAccount ` 생성자는 ` minimumBalance ` 매개 변수의 의미와 일치하도록 ` creditLimit
` 매개 변수의 부호를 변경할 수 있습니다.

##  다른 초과 인출 규칙

추가할 마지막 기능을 사용하면 ` LineOfCreditAccount ` 는 트랜잭션을 거부하는 대신 대출 한도 초과에 대해 수수료를 청구할
수 있습니다.

한 가지 방법은 필요한 동작을 구현하는 가상 함수를 정의하는 것입니다. ` BankAccount ` 클래스는 ` MakeWithdrawal
` 메서드를 두 개의 메서드로 리팩터링합니다. 새 메서드는 인출로 잔고가 최솟값보다 낮아지면 지정된 작업을 수행합니다. 기존 `
MakeWithdrawal ` 메서드에는 다음과 같은 코드가 있습니다.

    
    
    public void MakeWithdrawal(decimal amount, DateTime date, string note)
    {
        if (amount <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(amount), "Amount of withdrawal must be positive");
        }
        if (Balance - amount < _minimumBalance)
        {
            throw new InvalidOperationException("Not sufficient funds for this withdrawal");
        }
        var withdrawal = new Transaction(-amount, date, note);
        _allTransactions.Add(withdrawal);
    }
    

다음 코드로 바꿉니다.

    
    
    public void MakeWithdrawal(decimal amount, DateTime date, string note)
    {
        if (amount <= 0)
        {
            throw new ArgumentOutOfRangeException(nameof(amount), "Amount of withdrawal must be positive");
        }
        Transaction? overdraftTransaction = CheckWithdrawalLimit(Balance - amount < _minimumBalance);
        Transaction? withdrawal = new(-amount, date, note);
        _allTransactions.Add(withdrawal);
        if (overdraftTransaction != null)
            _allTransactions.Add(overdraftTransaction);
    }
    
    protected virtual Transaction? CheckWithdrawalLimit(bool isOverdrawn)
    {
        if (isOverdrawn)
        {
            throw new InvalidOperationException("Not sufficient funds for this withdrawal");
        }
        else
        {
            return default;
        }
    }
    

추가된 메서드는 ` protected ` 로, 파생 클래스에서만 호출할 수 있음을 뜻합니다. 이렇게 선언하면 다른 클라이언트가 메서드를
호출할 수 없습니다. 또한 파생 클래스가 동작을 변경할 수 있도록 ` virtual ` 입니다. 반환 형식은 ` Transaction? `
입니다. ` ? ` 주석은 메서드가 ` null ` 을 반환할 수 있음을 나타냅니다. 인출 한도를 초과할 때 수수료를 청구하기 위해 `
LineOfCreditAccount ` 에 다음 구현을 추가합니다.

    
    
    protected override Transaction? CheckWithdrawalLimit(bool isOverdrawn) =>
        isOverdrawn
        ? new Transaction(-20, DateTime.Now, "Apply overdraft fee")
        : default;
    

재정의는 계좌에서 초과 인출할 때 수수료 트랜잭션을 반환합니다. 인출이 한도를 초과하지 않으면 메서드는 ` null ` 트랜잭션을
반환합니다. 이는 수수료가 없음을 나타냅니다. ` Program ` 클래스의 ` Main ` 메서드에 다음 코드를 추가하여 이러한 변경
내용을 테스트합니다.

    
    
    var lineOfCredit = new LineOfCreditAccount("line of credit", 0, 2000);
    // How much is too much to borrow?
    lineOfCredit.MakeWithdrawal(1000m, DateTime.Now, "Take out monthly advance");
    lineOfCredit.MakeDeposit(50m, DateTime.Now, "Pay back small amount");
    lineOfCredit.MakeWithdrawal(5000m, DateTime.Now, "Emergency funds for repairs");
    lineOfCredit.MakeDeposit(150m, DateTime.Now, "Partial restoration on repairs");
    lineOfCredit.PerformMonthEndTransactions();
    Console.WriteLine(lineOfCredit.GetAccountHistory());
    

프로그램을 실행하고 결과를 확인합니다.

##  요약

잘 알 수 없는 경우 [ GitHub 리포지토리
](https://github.com/dotnet/docs/tree/main/docs/csharp/fundamentals/tutorials/snippets/object-
oriented-programming) 에서 이 자습서의 소스를 확인할 수 있습니다.

이 자습서에서 객체 지향 프로그래밍에 사용되는 다양한 방법을 살펴봤습니다.

  * 각 계좌 유형의 클래스를 정의할 때 추상화를 사용했습니다. 이러한 클래스는 해당 계좌 유형의 동작을 설명합니다. 
  * 각 클래스에서 많은 세부 정보를 ` private ` 으로 유지하는 경우 캡슐화를 사용했습니다. 
  * ` BankAccount ` 클래스에서 이미 만든 구현을 활용하여 코드를 저장하는 경우 상속을 사용했습니다. 
  * 파생 클래스가 해당 계좌 유형의 특정 동작을 만들기 위해 재정의할 수 있는 ` virtual ` 메서드를 만들 때 다형성을 사용했습니다. 


-->

<!--






-->

<!--
이전 포스팅에서 OOP란 무엇인지, 왜 사용해야 하는지, 그리고 OOP의 핵심개념들에는 무엇이 있는지 알아 보았다.

[ https://nybot-house.tistory.com/104 ](https://nybot-house.tistory.com/104)

[ [C# Basics] 객체지향 OOP란 무엇인가? - 핵심 4개념과 개론  이전 포스팅에서 한번 다루었던 OOP에 대해 다시 한번 그
중요성을 느꼈기에 한번 더 다뤄 보고자 한다. 이전 글: https://nybot-house.tistory.com/53 1. OOP 란? -
객체 지향 프로그래밍 소개 C++의 OOP란, 객체  nybot-house.tistory.com  ](https://nybot-
house.tistory.com/104)

이번 포스팅에서는 OOP(Object Oriented Programming)의 핵심 개념 중 하나인 캡슐화와 은닉성에 대해 자세히 알아
보자.

###  캡슐화(은닉성)란?

캡슐화는 객체의 세부 구현 내용을 숨기고(은닉성), 사용자에게는 필요한 인터페이스만을 제공하는 것을 말한다. 이를 통해 객체의 내부 구현이
외부에 노출되지 않게 하여 객체의 데이터와 메서드를 보호하고(보안), 사용상의 실수를 줄이며, 코드의 재사용성과 유지보수성을 높일 수 있다.

###  C# Unity 예시: Player Class

Unity 게임 개발에서 C#을 사용하여 캡슐화와 은닉성을 어떻게 구현할 수 있는지 예시를 통해 자세히 살펴보자.  
밑의 코드는 게임 플레이어의 체력을 관리하는 간단힌 'Player' 클래스이다.

    
    
    public class Player
    {
        // 캡슐화를 위해 체력(health)을 private 변수로 선언합니다.
        private int health;
    
        // 생성자에서 플레이어의 초기 체력을 설정합니다.
        public Player(int initialHealth)
        {
            health = initialHealth;
        }
    
        // 체력을 안전하게 조정할 수 있는 public 메서드를 제공합니다.
        public void TakeDamage(int damage)
        {
            if (damage < 0)
            {
                throw new ArgumentException("Damage cannot be negative");
            }
    
            health -= damage;
    
            // 체력이 0 이하가 되면 플레이어가 사망했다고 가정합니다.
            if (health <= 0)
            {
                Die();
            }
        }
    
        // 체력을 안전하게 회복시킬 수 있는 public 메서드를 제공합니다.
        public void Heal(int amount)
        {
            if (amount < 0)
            {
                throw new ArgumentException("Heal amount cannot be negative");
            }
    
            health += amount;
        }
    
        // 플레이어의 현재 체력을 확인할 수 있는 public 메서드를 제공합니다.
        public int GetHealth()
        {
            return health;
        }
    
        // 사망 처리를 위한 private 메서드입니다.
        private void Die()
        {
            Debug.Log("Player Died");
            // 사망 처리 로직...
        }
    }

위의 예시에서 _health 변수는 private으로 선언_ 되어 클래스 외부에서 직접 접근할 수 없다.  
이는 health 변수의 값이 클래스 내부의 메서드를 통해서만 변경될 수 있도록 하여, _health 의 값이 의도치 않게 외부에서 변경되는
것을 방지_ 한다. (다른 클래스나 메서드에서 부르려고 해도 외부에서는 결코 부를 수 없다.)

또한, 'TakeDamage' 메서드는 플레이어가 피해를 받을 때 'health'값을 감소시키고, 플레이어의 체력이 0이하가 되면
'Die'메서드를 호출한다. 'Heal' 메서드는 플레이어의 체력을 회복시킨다. ' _Die'메서드는 private으로 선언되어 클래스
외부에서 직접 호출할 수 없으며, 오직 클래스 내부에서만 호출될 수 있다_ .

###  private 이 아닐 경우 발생할 수 있는 문제

private 으로 변수와 메서드를 숨기지 않을 경우, 별 문제가 발생하지 않을 거라고 생각할 수도 있다. 하지만 이럴 경우, 클래스의 내부
구현이 외부로 노출되어 예기치 않은 방식으로 변경될 수가 있다. 이는 코드의 안정성을 해칠 수 있게 만들고, 유지보수를 어렵게 만든다.

예를 들어 'health'변수를 'public'으로 선언했다고 가정해 보자.

    
    
    public class Player
    {
        public int health; // 외부에서 직접 접근 가능
    
        public void TakeDamage(int damage)
        {
            health -= damage;
            if (health <= 0)
            {
                Die();
            }
        }
    
        private void Die()
        {
            Debug.Log("Player Died");
        }
    }

이 경우, 'health'변수는 외부에서 직접 접근이 가능해져, 클래스 외부의 다른 코드에서 다음과 같이 'health'값을 부적절하게
변경할 수 있다.

    
    
    Player player = new Player();
    player.health = -100; // health를 직접 조작하여 예상치 못한 값으로 설정

이렇게 'health'값이 직접 조작되면, 'TakeDamage'메서드를 통한 정상적인 흐름을 벗어나, 'health'값이 음수가 되거나,
'Die'메서드가 적절한 시점에 호출되지 않는 등의 문제가 발생할 수 있다. 이는 버그와 예측 불가능한 동작을 초래할 수 있다. 당신은 안
그럴 거라고? 천만에! 복잡한 상호작용의 총 집합체인 게임을 개발하다 보면 어떤 일이든 발생할 수 있다는 것을 명심해야 한다.

따라서 변수와 메서드를 'private'으로 설정하고, 필요한 경우에만 제한된 인터페이스(ex: 'TakeDamage' 메서드)를 통해
접근을 허용하는 것이 좋다. 이를 통해 클래스의 책임과 인터페이스가 명확해지며, 코드의 안정성과 유지보수성이 향상된다.

###  Unity의 [SerializeField] 속성

Unity에서는 [SerializeField] 속성을 사용하여 private 필드를 인스펙터에서 편집할 수 있게 만들 수 있다. 이는 캡슐화
원칙을 유지하면서도, Unity의 시각적 편집 환경에서 직접적으로 개발자가 값을 조정할 수 있게 해준다. [SerializeField]
속성은 해당 필드를 private으로 유지하면서도 Unity 에디터에 노출시켜, 에디터 내에서 값을 수정할 수 있도록 한다. 이는 게임 개발
과정에서 굉장한 편의성을 제공하는 동시에 코드의 안정성과 캡슐화 원칙을 해치지 않는다.

    
    
    using UnityEngine;
    
    public class Player : MonoBehaviour
    {
        [SerializeField]
        private int health; // Unity 에디터에서 접근 가능하지만 코드에서는 private
    
        public void TakeDamage(int damage)
        {
            health -= damage;
            if (health <= 0)
            {
                Die();
            }
        }
    
        private void Die()
        {
            Debug.Log("Player Died");
        }
    }

![https://blog.kakaocdn.net/dn/bFL0qB/btsGzGeNpoR/a9QKqLXjhkjSJt1Q9mI3qK/img.png](https://blog.kakaocdn.net/dn/bFL0qB/btsGzGeNpoR/a9QKqLXjhkjSJt1Q9mI3qK/img.png)
SerializeField를 붙여주어 선언해 주면 변수를 에디터 인스펙터에서 직접 수치를 가시화하고 빠르고 쉽게 조작할 수 있다

###  결론

위의 예시처럼 캡슐화를 통해 은닉함으로써 클래스의 내부 구현을 숨기고, 객체의 데이터를 보호하며, 사용자에게는 클래스를 사용하는 데 필요한
인터페이스만을 노출시키게 된다. 이렇게 함으로써 코드의 안정성과 유지보수성이 향상되며, 클래스 사용자는 클래스 내부 구현에 대해 신경 쓰지
않고도 기능을 이용할 수 있게 된다.


-->

<!--






-->

<!--
##  소개

C# 언어는 객체 지향 프로그래밍 기반으로 만들어졌습니다. C#을 사용하면 객체지향 프로그래밍 개념과 실습 방법을 배울 수 있습니다. 이번
포스팅에서는 C# 언어의 객체 지향 프로그래밍 개념과 실습 방법에 대해 알아보겠습니다. 객체 지향 프로그래밍에 대해 기본적인 이해가 되어
있다면 C# 언어를 사용하여 객체 지향 프로그래밍 실습을 하는 방법에 대해 알아보겠습니다. 또한 객체 지향 프로그래밍이 무엇인지에 대해
알아보고 C# 언어에서 사용되는 주요 객체 지향 프로그래밍 개념에 대해 살펴보겠습니다.

![C# 언어의 객체 지향 프로그래밍 개념과 실습 방법

-씨샵샵](https://koco-pot.co.kr/wp-content/uploads/sites/62/2023/05/n_5984_1.png)   
(위 사진은 내용과 무관함 [ Pexels 제공 사진 ](https://www.pexels.com) )

##  상세설명

###  1\. C# 객체 지향 개념

C#에서 객체 지향 프로그래밍(Object-Oriented Programming, OOP)은 소프트웨어를 만들기 위한 강력한 기술로, 코드의
재사용과 변경을 간편하게 하기 위해 사용됩니다. C#에서 OOP는 클래스, 객체, 상속, 인터페이스, 접근 한정자, 예외 처리 등과 같은
기능을 제공합니다. OOP의 개념을 이해하고 사용하는 것은 C# 프로그래밍의 기본이며, 이를 통해 적은 시간 내에 복잡한 프로그램을 빠르고
안정적으로 만들 수 있습니다.

###  2\. 객체 지향 프로그래밍 이해하기

C#은 객체 지향 프로그래밍(OOP, Object Oriented Programming)의 개념을 반영하여 최신 언어로 개발되었다. OOP는
프로그램을 작성하는 방법론 중 하나로, 코드를 객체들로 나누어 각각의 객체에 책임과 역할을 부여하는 방식이다. 객체는 비슷한 특성이나 기능을
가진 데이터들을 의미하며, 객체들의 상호작용에 의해 프로그램이 작동하게 된다.

C#에서 객체 지향 프로그래밍을 사용하려면 객체를 만들고 관리하는 방법을 이해할 필요가 있다. 객체는 클래스로 만들어지고, 클래스는 변수,
메소드 등의 요소로 구성된다. 생성한 객체는 객체 변수로 저장하고, 이 변수는 객체의 메소드를 호출하여 객체의 속성을 변경하거나 객체의
기능을 실행할 수 있다. 객체 지향 프로그래밍을 이해하고 사용하려면 이러한 개념들을 먼저 이해해야 한다.

###  3\. C#에서 객체 지향 프로그래밍 실습

C#은 객체 지향 프로그래밍의 기본 개념을 이해하고 이를 실습하는데 탁월한 언어입니다. 이 글에서 C#에서 객체 지향 프로그래밍을 실습하는
방법을 소개하겠습니다.

첫째, 객체 지향 프로그래밍을 실습하기 위해서는 객체를 생성하고 속성과 메소드를 정의하는 클래스를 작성해야 합니다. C#에서는 클래스를 통해
객체를 생성하고 속성과 메소드를 선언할 수 있습니다.

둘째, 객체 지향 프로그래밍은 다형성과 상속을 통해 더 나은 프로그램을 작성할 수 있습니다. C#에서는 매개 변수를 사용하여 상속과 다형성을
사용할 수 있습니다.

셋째, 객체 지향 프로그래밍에서는 인터페이스를 사용하여 여러 클래스의 기능을 쉽게 관리할 수 있습니다. C#에서는 인터페이스를 사용하여 여러
클래스의 기능을 쉽게 관리할 수 있습니다.

따라서 C#에서 객체 지향 프로그래밍을 실습하기 위해서는 클래스를 작성하고 상속과 다형성, 인터페이스를 사용하여 프로그램을 개발해야 합니다.
이러한 방법을 알고 있으면 C#에서 객체 지향 프로그래밍을 사용하여 더 나은 프로그램을 만들 수 있습니다.

###  4\. 객체 지향 개념 실습 방법

C# 언어를 사용한 객체 지향 프로그래밍의 실습 방법은 여러 가지가 있습니다. 먼저 클래스를 정의해야합니다. 클래스는 객체의 구조를 정의하는
데 사용되며 객체의 상태 및 행동을 정의하는 데 사용됩니다. 그 다음 객체를 생성하고 서로 다른 객체 사이의 관계를 정의해야합니다. 객체
지향 프로그래밍은 다형성과 상속을 통해 재사용할 수 있는 코드를 작성하는 것을 목표로합니다. 또한 메소드를 정의하고 인스턴스 변수를 사용하여
객체 사이의 메시지를 전달하는 것도 중요합니다. 마지막으로 객체가 상호 작용하면서 목표를 달성하기 위해 코드를 디버깅하고 테스트하는 것이
필요합니다.

###  5\. 객체 지향 프로그래밍 실행 시 반드시 알아야 할 것

C# 언어는 객체 지향 프로그래밍을 위해 만들어졌습니다. 객체 지향 프로그래밍 실행 시 가장 중요한 것은 설계도를 먼저 작성하고, 그 다음
단계로 실행 과정에 들어가는 것입니다. 설계도를 작성하기 위해서는 클래스, 속성, 메소드의 구분 없이 적절한 설계를 해야 합니다. 또한,
실행을 위해서는 적절한 인스턴스를 만들고, 그 인스턴스를 사용하는 과정이 필요합니다. 그리고 객체 지향 프로그래밍에서는 상속, 오버로딩,
오버라이딩 등의 개념을 적용하는 것도 매우 중요합니다. 따라서 이러한 개념을 제대로 이해하고, 적절한 설계를 하고, 인스턴스를 사용하고,
객체 지향 프로그래밍의 각 개념들을 잘 사용하는 것이 객체 지향 프로그래밍 실행 시 반드시 알아야 할 것입니다.

![C# 언어의 객체 지향 프로그래밍 개념과 실습 방법

2-씨샵샵](https://koco-pot.co.kr/wp-
content/uploads/sites/62/2023/05/n_5984_2.png)  
(위 사진은 내용과 무관함 [ Pexels 제공 사진 ](https://www.pexels.com) )

##  종합

C#은 객체 지향 프로그래밍(OOP)을 지원하는 강력한 언어입니다. OOP는 객체 중심의 접근 방법으로 프로그래밍을 하는 것입니다. 클래스,
인터페이스, 메소드, 상속 등 C#에서 제공하는 OOP 기능을 사용해 프로그램을 개발할 수 있습니다. C#을 이용해 객체 지향 프로그래밍을
하려면, 클래스의 생성과 사용법, 인터페이스 제공하는 기능, 메소드의 사용법, 상속의 활용법 등의 개념을 이해해야 합니다. 또한 디버깅과
다양한 객체 지향 기능을 이해하고 실습할 수 있는 방법도 필요합니다. 이런 내용들을 배우는 것은 어렵지만, 실습을 통해 더 나은 객체 지향
프로그래밍을 할 수 있게 됩니다.

####  함께 보면 좋은 영상

![객체 지향 프로그래밍이란?](https://i.ytimg.com/vi/dy9yQIx38u8/hqdefault.jpg)

객체 지향 프로그래밍이란?

VIDEO


-->

<!--






-->

<!--
이전 포스팅에서 한번 다루었던 OOP에 대해 다시 한번 그 중요성을 느꼈기에 한번 더 다뤄 보고자 한다.

**이전 글:** [ https://nybot-house.tistory.com/53 ](https://nybot-
house.tistory.com/53)

[ 1\. OOP 란? - 객체 지향 프로그래밍 소개  C++의 OOP란, 객체Object 가 중심이 되서 프로그래밍하는 패러다임. C++
는 여러가지 패러다임을 제공해 주는 멀티 패러다임 언어이다. 1) procedural 2) functional 3) OOP - (
Object-Oriented Programming ) 4) generic 를  nybot-house.tistory.com
](https://nybot-house.tistory.com/53)

게임 개발을 하는 데 있어 객체 지향 프로그래밍, 즉 OOP (Object Oriented Programming)의 중요성은 다시 말할 필요
없이 핵심이고 중요하다. 필자 또한 처음 입사했을 때 OOP에 맞게 코딩하지 않아 굉장히 많은 지적을 받았던 기억이 있다. OOP는 필자가
게임 개발을 할 때 가장 먼저 고려하는 요소이고, 이미 프로그램을 다 짠 후에도 OOP에 맞게 코드를 짰는지 다시 한번 더 고민하는 시간을
갖고는 한다. 그렇다면 OOP란 무엇이며, 어떤 역할을 할까?

OOP는 프로그램 패러다임 중에 하나로, 데이터와 그 데이터를 처리하는 함수들을 하나의 '객체'로 묶어서 생각하는 방식이다. 복잡하고 상호
작용이 많은 시스템을 설계하는 게임 개발에서  OOP를 고려하지 않고 게임을 개발한다면  수없이 많은 스파게티 코딩이 생길 것이고, 확장성,
유지 보수 등에 엄청난 시간을 쏟게 될 것이다.

###  ** OOP의 핵심 개념들  **

OOP는 주로 다음 네 가지 원칙에 기반한다.

  1. **캡슐화-은닉성 (Encapsulation)**   
: 데이터(속성)과 그 데이터를 다루는 함수(메서드)를 객체 내부에 포함시켜, 객체의 세부 구현 내용이 외부에 드러나지 않도록 하는 것이다.
이는 코드의 재사용성을 높이고, 변경에 따른 위협을 줄인다.

  2. **상속성(Inheritance)**   
: 한 클래스(부모 클래스)의 속성과 메서드를 다른 클래스(자식 클래스)가 물려 받을 수 있게 함으로써, 공통된 코드를 재사용할 수 있게
한다.

  3. **다형성 (Polymorphism)**   
: 같은 이름의 메서드가 다른 클래스에서 다양한 방식으로 실행될 수 있음을 의미한다. 이를 통해 코드의 유연성과 확장성이 증가한다.

  4. **추상화 (Abstraction)**   
: 복잡한 실제 세계를 간단한 모델로 표현하는 것으로, 필요한 정보만을 추출하여 객체의 특성을 단순화한

###  **oop가 게임 개발, 특히 Unity에서 중요한 이유**

  1. 구조화와 조직화   
: OOP를 사용하면 코드를 논리적이고 체계적으로 조직할 수 있어, 프로젝트의 복잡성을 관리하기 쉽다. 게임 개발은 다양한 객체(캐릭터,
아이템, 환경 등)을 다루기 때문에 이러한 조직화는 필수적이다.

  2. 재사용성과 확장성   
: OOP의 상속성과 캡슐화는 코드 재사용을 용이하게 한다. 이는 개발 시간을 단축하고, 프로젝트의 확장성을 높여준다.

  3. 유지 보수의 용이성   
: OOP의 추상화와 캡슐화는 코드 변경 시 영향을 받는 범위를 최소화하며, 이는 유지 보수를 용이하게 한다.

  4. 협업   
: 게임 개발은 협업의 연속이다. 99퍼센트의 개발자들은 혼자 게임 개발을 할 수 없다. OOP는 각 개발자가 시스템의 특정 부분(객체)에
집중할 수 있게 하여, 대규모 프로젝트에서의 협업을 원활하게 한다

###  **결론**

Unity 게임 엔진은 이러한 OOP 원칙을 근간으로 설계되었으며, Unity에서 스크립팅을 할 때 객체 지향 언어인 C#을 사용하게 된다.
따라서 OOP에 대한 이해는 Unity 게임 개발에서 매우 중요하며, 효율적인 게임 설계와 개발을 위한 필수적인 기술이다.

이제 다음 포스팅들에서 OOP의 4 핵심 개념에 대해 구체적으로 알아 보시면 되겠다.

**상속성:** [ https://nybot-house.tistory.com/58 ](https://nybot-
house.tistory.com/58)

[ 1\. Inheritance 상속이란? _ C++  1\. Inheritance 상속 : C++에서 상속이란, 기존에 정의되어 있는
클래스의 모든 멤버 변수와 멤버 함수를 물려받아 새로운 클래스를 작성하는 것을 말한다. 이 때, 기존에 정의되어 있던 클래스를 기
nybot-house.tistory.com  ](https://nybot-house.tistory.com/58)

**캡슐화/은닉성:** [ https://nybot-house.tistory.com/105 ](https://nybot-
house.tistory.com/105)

[ [C# Basics] 은닉성 (캡슐화) - OOP 의 핵심 개념(객체 지향 프로그래밍)  이전 포스팅에서 OOP란 무엇인지, 왜 사용해야
하는지, 그리고 OOP의 핵심개념들에는 무엇이 있는지 알아 보았다. https://nybot-house.tistory.com/104 [C#
Basics] 객체지향 OOP란 무엇인가? - 핵심 4개념과 개  nybot-house.tistory.com  ](https://nybot-
house.tistory.com/105)


-->

<!--






-->

<!--
![https://blog.kakaocdn.net/dn/cS7s9h/btracYY1SBu/ElaKP56NxFd2DUjOtjGukk/img.png](https://blog.kakaocdn.net/dn/cS7s9h/btracYY1SBu/ElaKP56NxFd2DUjOtjGukk/img.png)

* * *

##  **객체 지향 프로그래밍이란?**

**객체 지향 프로그래밍(Object-Oriented Programming)** 은 **객체(Object)를 중심** 으로 프로그램을 설계,
개발해 나가는 것을 말합니다. 객체 지향 프로그래밍의 가장 큰 특징은 **클래스** 를 이용해 _함수(처리 부분), 변수(데이터 부분)를
하나로 묶어 객체(인스턴스)로 만들어 사용_ 한다는 점입니다.

C#은 여러 언어의 장점을 결합한 객체지향 언어입니다. 언어의 사용을 단순화하여 숫자를 객체와 같이 처리하게 하고, Collection에
저장할 수 있게 해줍니다. 또한, 박싱/언박싱의 개념을 가지고 있어 숫자를 객체로, 객체를 다시 숫자로 변경할 수 있게 해줍니다. 객체로
사용할 필요가 없는 숫자는 단순 값으로 처리되어 효율적인 사용이 가능합니다.

이 포스팅에서는 객체 지향 언어의 _장단점_ 과 객체 지향 언어의 _4가지 특징_ 에 대해 다뤄보겠습니다.

* * *

####

###  **1\. 객체 지향 언어와 절차 지향 언어의 비교**

|  **객체 지향 언어** |  **절차 지향 언어**  
---|---|---  
장점  |  \- 코드의 재사용성이 용이   
\- 개발이 간단  
\- 유지보수가 쉬움  
\- 대규모 프로젝트에 적합  |  \- 처리속도가 빠름   
\- 컴퓨터의 처리구조와 비슷해 실행속도가 빠름  
단점  |  \- 처리속도가 느림   
\- 객체에 따른 용량 증가  
\- 설계 단계에서 시간이 많이 소요  |  \- 유지보수가 어려움   
\- 대규모 프로젝트에 부적합  
\- 프로젝트 분석이 어려움  
  
####  *** 객체 지향 프로그래밍의 5가지 설계 원칙**

1\. 단일 책임 원칙 : 클래스는 단 하나의 목적을 가져야 하며, 클래스를 변경하는 이유는 단 하나의 이유여야 한다.

2\. 클래스는 확장에는 열려 있고, 변경에는 닫혀 있어야 한다.

3\. 리스코프 치환 원칙 : 상위 타입의 객체를 하위 타입으로 바꾸어도 프로그램은 일관되게 동작해야 한다.

4\. 인터페이스 분리 원칙 : 클라이언트는 이용하지 않는 메서드에 의존하지 않도록 인터페이스를 분리해야 한다.

5\. 의존 역전 법칙 : 클라이언트는 추상화(인터페이스)에 의존해야 하며, 구체화(구현된 클래스)에 의존해선 안 된다.

* * *

###  **2\. 객체 지향 프로그래밍의 4가지 특징**

객체 지향에는 4가지 특징이 있습니다.

1) 캡슐화

2) 추상화

3) 상속

4) 다형성

####  **1) 캡슐화**

캡슐화는 연관있는 변수와 메소드를 묶어주는 작업을 말하며, 클래스의 접근을 제한하는 것과 관계가 있습니다. 접근 지정자(private,
protected, public)를 통해 외부로부터의 접근을 제한하고, 객체 내에서만 접근이 가능하도록(정보 은닉) 해줍니다.

* 접근지정자 [ https://geukggom.tistory.com/83 ](https://geukggom.tistory.com/83)

[ [C# 기초] #03 : 변수 - 접근지정자(public, private, protected)  유니티 기초 글 링크 모음 :
geukggom.tistory.com/1 [Unity] 공부글 모음 1) 변수 - 데이터형식(Data Type)과 형변환 :
geukggom.tistory.com/20 - 값 형식 / 참조 형식 : https://geukggom.tistory.com/44 - L..
geukggom.tistory.com  ](https://geukggom.tistory.com/83)

클래스의 변수와 함수가 모두 public으로 만들어질 경우, 클래스의 고유의 객체 특성을 잃어버릴 수 있기 때문에 꼭 필요한 데이터 외에는
private(내부에서만 접근 가능)로 설정해야 합니다. 접근지정자에 대한 자세한 설명은 위 포스팅에서 좀 더 자세히 다루기 때문에
넘어가도록 하겠습니다.

####  **2) 추상화**

객체 지향에서 추상화란 객체에서 필요한 공통된 부분을 추출하는 것을 의미합니다.

![https://blog.kakaocdn.net/dn/bAQtjS/btracJ2dsEq/bZNKofKy2DUhHPXGLvoCh0/img.png](https://blog.kakaocdn.net/dn/bAQtjS/btracJ2dsEq/bZNKofKy2DUhHPXGLvoCh0/img.png)

이렇게 Cat, Dog라는 각각의 class가 있습니다.

각각의 클래스는 공통점을 가지는데, 이는 둘 다 Animal이라는 공통적인 속성을 가지고 있기 때문입니다. 따라서 아래와 같이
Animal이라는 추상적인 class로 둘의 공통된 부분을 묶을 수 있습니다.

![https://blog.kakaocdn.net/dn/cz9ykE/btracJVwkAQ/zBahwwyBOlkpW5fkghgzKK/img.png](https://blog.kakaocdn.net/dn/cz9ykE/btracJVwkAQ/zBahwwyBOlkpW5fkghgzKK/img.png)

다음, 상속에서 계속 설명이 이어집니다.

####  **3) 상속**

상속은 부모 클래스로부터 공 _통된 변수와 함수, 인터페이스를 그대로 물려받는 것_ 을 말합니다.

상속은 비슷한 객체들의 부모 클래스와 인터페이스를 정의하여 공통화 한 다음 상속받아 객체를 좀 더 다루기 쉽게 합니다. 추상화에서 각
클래스의 공통된 부분을 묶었다면, 부모 class를 상속받아 거기에 포함된 데이터를 그대로 사용할 수 있습니다.

![https://blog.kakaocdn.net/dn/b2eInh/btradI9HNon/uZ8Hv9P6KjLEuFKYCNbMoK/img.png](https://blog.kakaocdn.net/dn/b2eInh/btradI9HNon/uZ8Hv9P6KjLEuFKYCNbMoK/img.png)

####  **4) 다형성**

다형성은 같은 종류의 클래스가 하나의 메시지에 대해 서로 다른 행동을 하는 것을 말합니다.

위의 예시에 이어서 설명하자면, Cat, Dog는 Animal이라는 공통적인 class를 상속받았지만, 각자의 고유한 특징(Say()함수)을
가집니다. 이렇듯 다형성을 통해 변경이 필요한 부분을 변경하여 사용할 수 있습니다.

다형성은 오버라이딩, 오버로딩 형태로 제공됩니다.

![https://blog.kakaocdn.net/dn/GdD2k/btq99mtgENq/ueuoMjFRy9NZFYsVuBbN8k/img.png](https://blog.kakaocdn.net/dn/GdD2k/btq99mtgENq/ueuoMjFRy9NZFYsVuBbN8k/img.png)


-->

<!--






-->

