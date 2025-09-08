---
image: "tmp_wordcloud.png"
categories: CSharp
date: "2024-08-14T00:00:00Z"
header: null
tags:
- CSharp
- interface
- AbstractClass
- object-oriented programming
- inheritance
- polymorphism
- encapsulation
- SoftwareDesign
- coding
- ProgrammingConcepts
- SoftwareDevelopment
- C# programming
- OOPPrinciples
- MethodOverriding
- MethodImplementation
- ClassDesign
- SoftwareArchitecture
- DesignPatterns
- ProgrammingLanguages
- CodeQuality
- SoftwareEngineering
- debugging
- CodeMaintenance
- SoftwareTesting
- ApplicationDevelopment
- PerformanceOptimization
- DataAbstraction
- CodeReusability
- SoftwareLifecycle
- DevelopmentMethodologies
- AgileDevelopment
- VersionControl
- CodeDocumentation
- BestPractices
- CleanCode
- refactoring
- SoftwareTools
- IDE
- VisualStudio
- .NET framework
- ProgrammingTutorials
- learning C#
- CodingChallenges
- TechBlogs
- DeveloperCommunity
- ProgrammingResources
- OnlineCourses
- SoftwareProjects
teaser: /assets/images/undefined/teaser.jpg
title: '[C#] C# 인터페이스와 추상클래스의 차이점'
---

C#에서 인터페이스와 추상 클래스는 객체 지향 프로그래밍의 중요한 개념으로, 이 둘은 비슷한 점이 많지만 여러 가지 차이점이 존재한다. 인터페이스는 클래스가 따라야 할 행동의 청사진을 제공하며, 모든 멤버가 추상 메서드와 상수로만 이루어져 있다. 반면, 추상 클래스는 일반 메서드와 필드를 가질 수 있으며, 인스턴스를 생성할 수 없는 특성을 지닌다. 인터페이스는 다중 상속을 지원하여 여러 클래스가 동일한 인터페이스를 구현할 수 있도록 하며, 이는 코드의 유연성과 재사용성을 높이는 데 기여한다. 추상 클래스는 공통적인 기능을 가진 클래스의 기본 구현을 제공할 수 있어, 상속받는 클래스에서 기본적인 동작을 재정의할 수 있는 장점을 가진다. 이러한 특성 덕분에 개발자는 요구 사항에 따라 적절한 구조를 선택하여 소프트웨어를 설계할 수 있다. 인터페이스와 추상 클래스의 차이를 이해하는 것은 C# 프로그래밍에서 매우 중요하며, 이를 통해 더 나은 코드 품질과 유지 보수성을 확보할 수 있다.


|![]()|
|:---:|
||


<!--
##### Outline #####
-->

<!--
---
## C# 인터페이스와 추상 클래스의 차이점
**서론**
**C#에서의 추상화 개념**
**인터페이스와 추상 클래스의 정의**
**인터페이스와 추상 클래스의 필요성**

## 인터페이스의 특징
**인터페이스의 기본 구조**
**인터페이스의 접근 제한자**
**인터페이스의 메서드와 프로퍼티**
**인터페이스의 다중 상속**

## 추상 클래스의 특징
**추상 클래스의 기본 구조**
**추상 클래스의 접근 제한자**
**추상 클래스의 메서드와 필드**
**추상 클래스의 상속 규칙**

## 인터페이스와 추상 클래스의 비교
**구현 방식의 차이**
**상속의 차이**
**성능 차이**
**사용 사례의 차이**

## Practical Examples
**인터페이스 사용 예제**
**추상 클래스 사용 예제**
**인터페이스와 추상 클래스의 혼합 사용 예제**
**실제 프로젝트에서의 활용 사례**

## Frequently Asked Questions
**인터페이스와 추상 클래스 중 어떤 것을 선택해야 할까?**
**인터페이스는 왜 다중 상속이 가능한가?**
**추상 클래스는 왜 인스턴스화할 수 없는가?**
**인터페이스의 기본 구현 메서드는 무엇인가?**

## Related Technologies
**C#의 객체 지향 프로그래밍**
**다형성과 상속**
**SOLID 원칙**
**디자인 패턴에서의 인터페이스와 추상 클래스 활용**

## 결론
**주요 포인트 요약**
**인터페이스와 추상 클래스의 중요성**
**C#에서의 추상화 개념의 활용**
**향후 학습 방향 제안**

---
-->

<!--
---
## C# 인터페이스와 추상 클래스의 차이점
**서론**
**C#에서의 추상화 개념**
**인터페이스와 추상 클래스의 정의**
**인터페이스와 추상 클래스의 필요성**
-->

## C# 인터페이스와 추상 클래스의 차이점

**서론**  

C#은 객체 지향 프로그래밍 언어로, 코드의 재사용성과 유지보수성을 높이기 위해 다양한 추상화 개념을 제공한다. 그 중에서도 인터페이스와 추상 클래스는 매우 중요한 역할을 한다. 이 글에서는 C#에서 인터페이스와 추상 클래스의 차이점과 각각의 특징에 대해 자세히 살펴보겠다.

**C#에서의 추상화 개념**  

추상화는 복잡한 시스템을 단순화하여 이해하기 쉽게 만드는 과정이다. C#에서는 클래스와 객체를 통해 추상화를 구현할 수 있으며, 인터페이스와 추상 클래스는 이러한 추상화를 더욱 효과적으로 수행할 수 있도록 돕는다. 인터페이스는 특정 기능을 정의하고, 이를 구현하는 클래스가 해당 기능을 제공하도록 강제하는 반면, 추상 클래스는 공통된 속성과 메서드를 정의하여 상속받는 클래스가 이를 재사용할 수 있도록 한다.

**인터페이스와 추상 클래스의 정의**  

인터페이스는 메서드, 프로퍼티, 이벤트 등을 정의하는 계약으로, 이를 구현하는 클래스는 반드시 해당 메서드들을 구현해야 한다. 반면, 추상 클래스는 하나 이상의 추상 메서드를 포함할 수 있으며, 이를 상속받는 클래스는 추상 메서드를 구현해야 한다. 추상 클래스는 일반 메서드와 필드를 가질 수 있는 반면, 인터페이스는 기본적으로 메서드의 시그니처만을 정의한다.

**인터페이스와 추상 클래스의 필요성**  

인터페이스와 추상 클래스는 코드의 유연성과 확장성을 높이는 데 중요한 역할을 한다. 인터페이스를 사용하면 다양한 클래스가 동일한 메서드를 구현할 수 있어 다형성을 제공하며, 추상 클래스를 사용하면 공통된 기능을 재사용할 수 있어 코드의 중복을 줄일 수 있다. 이러한 특성 덕분에 대규모 프로젝트에서의 유지보수성과 협업이 용이해진다.

--- 

이와 같은 방식으로 나머지 목차에 대해서도 작성할 수 있다. 각 섹션에 대해 더 깊이 있는 설명과 예제를 추가하여 독자가 이해할 수 있도록 돕는 것이 중요하다.

<!--
## 인터페이스의 특징
**인터페이스의 기본 구조**
**인터페이스의 접근 제한자**
**인터페이스의 메서드와 프로퍼티**
**인터페이스의 다중 상속**
-->

## 인터페이스의 특징

**인터페이스의 기본 구조**  

인터페이스는 C#에서 객체 지향 프로그래밍의 중요한 개념 중 하나이다. 인터페이스는 클래스가 구현해야 하는 메서드, 프로퍼티, 이벤트 등을 정의하는 계약을 제공한다. 인터페이스는 다음과 같은 기본 구조를 가진다.

```csharp
public interface IExample
{
    void MethodA();
    int PropertyB { get; set; }
}
```

위의 예제에서 `IExample`이라는 인터페이스는 `MethodA`라는 메서드와 `PropertyB`라는 프로퍼티를 정의하고 있다. 이 인터페이스를 구현하는 클래스는 이 두 가지를 반드시 구현해야 한다.

**인터페이스의 접근 제한자**  

인터페이스의 멤버는 기본적으로 public 접근 제한자를 가진다. 즉, 인터페이스 내의 모든 메서드와 프로퍼티는 외부에서 접근할 수 있다. 그러나 인터페이스 자체는 private이나 protected 접근 제한자를 가질 수 없다. 이는 인터페이스가 다른 클래스와의 상호작용을 위해 설계되었기 때문이다.

**인터페이스의 메서드와 프로퍼티**  

인터페이스는 메서드와 프로퍼티를 정의할 수 있으며, 이들은 구현 클래스에서 반드시 구현해야 한다. 메서드는 반환형과 매개변수를 정의할 수 있으며, 프로퍼티는 getter와 setter를 통해 값을 읽고 쓸 수 있다. 다음은 인터페이스의 메서드와 프로퍼티를 정의하는 예제이다.

```csharp
public interface IAnimal
{
    void Speak();
    string Name { get; set; }
}
```

위의 예제에서 `IAnimal` 인터페이스는 `Speak` 메서드와 `Name` 프로퍼티를 정의하고 있다. 이를 구현하는 클래스는 이 두 가지를 반드시 구현해야 한다.

**인터페이스의 다중 상속**  

C#에서는 클래스가 다중 상속을 지원하지 않지만, 인터페이스는 다중 상속을 지원한다. 즉, 하나의 클래스가 여러 개의 인터페이스를 구현할 수 있다. 이는 코드의 재사용성을 높이고, 다양한 기능을 조합할 수 있는 유연성을 제공한다. 다음은 다중 상속을 사용하는 예제이다.

```csharp
public interface IFlyable
{
    void Fly();
}

public interface ISwimmable
{
    void Swim();
}

public class Duck : IFlyable, ISwimmable
{
    public void Fly()
    {
        Console.WriteLine("Duck is flying.");
    }

    public void Swim()
    {
        Console.WriteLine("Duck is swimming.");
    }
}
```

위의 예제에서 `Duck` 클래스는 `IFlyable`과 `ISwimmable` 두 개의 인터페이스를 구현하고 있다. 이를 통해 `Duck` 클래스는 비행과 수영 기능을 모두 가질 수 있다.

<!--
## 추상 클래스의 특징
**추상 클래스의 기본 구조**
**추상 클래스의 접근 제한자**
**추상 클래스의 메서드와 필드**
**추상 클래스의 상속 규칙**
-->

## 추상 클래스의 특징

**추상 클래스의 기본 구조**  

추상 클래스는 C#에서 객체 지향 프로그래밍의 중요한 개념 중 하나이다. 추상 클래스는 인스턴스화할 수 없는 클래스이며, 다른 클래스가 상속받아 사용할 수 있는 기본 구조를 제공한다. 추상 클래스는 일반 클래스와 마찬가지로 필드, 메서드, 프로퍼티를 가질 수 있지만, 최소한 하나 이상의 추상 메서드를 포함해야 한다. 추상 메서드는 구현이 없는 메서드로, 이를 상속받는 클래스에서 반드시 구현해야 한다.  

**추상 클래스의 접근 제한자**  

추상 클래스의 접근 제한자는 클래스의 접근성을 정의하는 중요한 요소이다. C#에서는 `public`, `protected`, `internal`, `private`와 같은 접근 제한자를 사용할 수 있다. 일반적으로 추상 클래스는 `protected` 또는 `public`으로 선언하여, 상속받는 클래스가 접근할 수 있도록 하는 것이 일반적이다. `protected`로 선언된 멤버는 해당 클래스와 그 클래스를 상속받은 클래스에서만 접근할 수 있다.  

**추상 클래스의 메서드와 필드**  

추상 클래스는 일반 클래스와 마찬가지로 필드와 메서드를 가질 수 있다. 필드는 클래스의 상태를 나타내며, 메서드는 클래스의 동작을 정의한다. 추상 클래스 내에서 정의된 메서드는 일반 메서드와 추상 메서드로 나뉜다. 일반 메서드는 구현을 포함하고, 추상 메서드는 구현이 없는 메서드이다. 이를 통해 추상 클래스는 기본적인 동작을 정의하고, 상속받는 클래스에서 구체적인 동작을 구현할 수 있도록 한다.  

**추상 클래스의 상속 규칙**  

추상 클래스는 다른 클래스에 의해 상속될 수 있으며, 이를 통해 코드의 재사용성을 높일 수 있다. C#에서는 단일 상속만 지원하므로, 한 클래스는 하나의 추상 클래스만 상속받을 수 있다. 그러나 추상 클래스는 여러 개의 인터페이스를 구현할 수 있다. 상속받는 클래스는 추상 클래스에서 정의된 추상 메서드를 반드시 구현해야 하며, 이를 통해 구체적인 동작을 정의할 수 있다.  

---  

이와 같은 방식으로 추상 클래스의 특징을 이해하고 활용하면, C#에서 객체 지향 프로그래밍의 강력한 기능을 최대한 활용할 수 있다. 추상 클래스는 코드의 구조를 명확히 하고, 유지보수성을 높이는 데 큰 도움이 된다.

<!--
## 인터페이스와 추상 클래스의 비교
**구현 방식의 차이**
**상속의 차이**
**성능 차이**
**사용 사례의 차이**
-->

## 인터페이스와 추상 클래스의 비교

**구현 방식의 차이**  

인터페이스와 추상 클래스는 모두 추상화의 개념을 제공하지만, 구현 방식에서 큰 차이를 보인다. 인터페이스는 메서드의 시그니처만 정의하고, 실제 구현은 이를 구현하는 클래스에서 제공해야 한다. 반면, 추상 클래스는 일부 메서드에 대한 기본 구현을 제공할 수 있으며, 이를 상속받는 클래스는 필요에 따라 해당 메서드를 오버라이드할 수 있다. 이러한 차이는 코드의 재사용성과 유지보수성에 영향을 미친다.

**상속의 차이**  

인터페이스는 다중 상속을 지원하는 반면, 추상 클래스는 단일 상속만 가능하다. 즉, 하나의 클래스는 여러 개의 인터페이스를 구현할 수 있지만, 하나의 추상 클래스만 상속받을 수 있다. 이로 인해 인터페이스는 다양한 기능을 조합하여 사용할 수 있는 유연성을 제공한다. 반면, 추상 클래스는 상속 구조가 명확하여 코드의 가독성을 높이는 데 기여할 수 있다.

**성능 차이**  

성능 측면에서 인터페이스는 메서드 호출 시 약간의 오버헤드가 발생할 수 있다. 이는 인터페이스 메서드가 가상 메서드로 처리되기 때문인데, 이로 인해 메서드 호출 시 추가적인 작업이 필요하다. 반면, 추상 클래스는 일반적으로 더 나은 성능을 제공할 수 있다. 그러나 이러한 성능 차이는 대부분의 경우 미미하며, 실제 애플리케이션에서는 코드의 구조와 유지보수성을 고려하는 것이 더 중요하다.

**사용 사례의 차이**  

인터페이스는 주로 서로 다른 클래스 간의 계약을 정의할 때 사용된다. 예를 들어, 다양한 형태의 데이터 저장소를 구현할 때, 각 저장소가 공통적으로 가져야 할 메서드를 인터페이스로 정의할 수 있다. 반면, 추상 클래스는 공통된 기능을 가진 클래스의 기본 구조를 정의할 때 유용하다. 예를 들어, 여러 종류의 동물 클래스를 만들 때, 공통된 속성과 메서드를 추상 클래스로 정의하고, 각 동물 클래스에서 이를 상속받아 구체적인 구현을 제공할 수 있다. 

이러한 차이점들은 개발자가 특정 상황에 맞는 적절한 선택을 할 수 있도록 도와준다. 인터페이스와 추상 클래스는 각각의 장단점이 있으며, 이를 잘 이해하고 활용하는 것이 중요하다.

<!--
## Practical Examples
**인터페이스 사용 예제**
**추상 클래스 사용 예제**
**인터페이스와 추상 클래스의 혼합 사용 예제**
**실제 프로젝트에서의 활용 사례**
-->

## Practical Examples

**인터페이스 사용 예제**  

인터페이스는 C#에서 객체 간의 계약을 정의하는 데 사용된다. 예를 들어, `IAnimal`이라는 인터페이스를 정의하고, 이 인터페이스를 구현하는 여러 동물 클래스를 만들어 보자. 

```csharp
public interface IAnimal
{
    void Speak();
}

public class Dog : IAnimal
{
    public void Speak()
    {
        Console.WriteLine("Woof!");
    }
}

public class Cat : IAnimal
{
    public void Speak()
    {
        Console.WriteLine("Meow!");
    }
}
```

위의 코드에서 `IAnimal` 인터페이스는 `Speak` 메서드를 정의하고, `Dog`와 `Cat` 클래스는 이 인터페이스를 구현하여 각자의 소리를 출력한다. 

**추상 클래스 사용 예제**  

추상 클래스는 공통된 기능을 가진 여러 클래스의 기본 클래스로 사용된다. 예를 들어, `Animal`이라는 추상 클래스를 정의하고, 이를 상속받는 `Dog`와 `Cat` 클래스를 만들어 보자.

```csharp
public abstract class Animal
{
    public abstract void Speak();
}

public class Dog : Animal
{
    public override void Speak()
    {
        Console.WriteLine("Woof!");
    }
}

public class Cat : Animal
{
    public override void Speak()
    {
        Console.WriteLine("Meow!");
    }
}
```

위의 코드에서 `Animal` 클래스는 추상 메서드 `Speak`를 정의하고, `Dog`와 `Cat` 클래스는 이를 구현하여 각자의 소리를 출력한다. 

**인터페이스와 추상 클래스의 혼합 사용 예제**  

인터페이스와 추상 클래스를 혼합하여 사용할 수도 있다. 예를 들어, `IAnimal` 인터페이스와 `Animal` 추상 클래스를 함께 사용하는 경우를 살펴보자.

```csharp
public interface IAnimal
{
    void Speak();
}

public abstract class Animal : IAnimal
{
    public abstract void Speak();
}

public class Dog : Animal
{
    public override void Speak()
    {
        Console.WriteLine("Woof!");
    }
}

public class Cat : Animal
{
    public override void Speak()
    {
        Console.WriteLine("Meow!");
    }
}
```

위의 코드에서 `Animal` 클래스는 `IAnimal` 인터페이스를 구현하고, `Dog`와 `Cat` 클래스는 `Animal` 클래스를 상속받아 `Speak` 메서드를 구현한다. 

**실제 프로젝트에서의 활용 사례**  

실제 프로젝트에서는 인터페이스와 추상 클래스를 적절히 활용하여 코드의 재사용성과 유지보수성을 높일 수 있다. 예를 들어, 게임 개발에서 다양한 캐릭터를 구현할 때, `ICharacter` 인터페이스를 정의하고, `Character`라는 추상 클래스를 만들어 공통된 기능을 구현할 수 있다. 

```csharp
public interface ICharacter
{
    void Attack();
}

public abstract class Character : ICharacter
{
    public abstract void Attack();
}

public class Warrior : Character
{
    public override void Attack()
    {
        Console.WriteLine("Warrior attacks with a sword!");
    }
}

public class Mage : Character
{
    public override void Attack()
    {
        Console.WriteLine("Mage casts a fireball!");
    }
}
```

이와 같이 인터페이스와 추상 클래스를 활용하면, 다양한 캐릭터의 행동을 일관되게 정의하고, 새로운 캐릭터를 추가할 때도 기존 코드를 수정하지 않고 쉽게 확장할 수 있다. 

이러한 예제들은 C#에서 인터페이스와 추상 클래스의 사용법을 이해하는 데 큰 도움이 된다.

<!--
## Frequently Asked Questions
**인터페이스와 추상 클래스 중 어떤 것을 선택해야 할까?**
**인터페이스는 왜 다중 상속이 가능한가?**
**추상 클래스는 왜 인스턴스화할 수 없는가?**
**인터페이스의 기본 구현 메서드는 무엇인가?**
-->

## Frequently Asked Questions

**인터페이스와 추상 클래스 중 어떤 것을 선택해야 할까?**  

인터페이스와 추상 클래스는 각각의 용도와 상황에 따라 선택해야 한다. 인터페이스는 여러 클래스에서 공통적으로 구현해야 하는 메서드의 집합을 정의할 때 유용하다. 반면, 추상 클래스는 기본적인 구현을 제공하면서도 일부 메서드는 자식 클래스에서 구현하도록 강제할 때 사용된다. 따라서, 다중 상속이 필요한 경우에는 인터페이스를, 기본 구현이 필요한 경우에는 추상 클래스를 선택하는 것이 좋다.

**인터페이스는 왜 다중 상속이 가능한가?**  

인터페이스는 다중 상속이 가능하다. 이는 인터페이스가 메서드의 구현을 포함하지 않기 때문이다. 인터페이스는 단순히 메서드의 시그니처만을 정의하므로, 여러 인터페이스를 구현하는 것이 가능하다. 반면, 클래스는 상태(필드)를 가질 수 있기 때문에 다중 상속을 허용하지 않는다. 이러한 이유로 인터페이스는 다중 상속을 지원하여 유연한 설계를 가능하게 한다.

**추상 클래스는 왜 인스턴스화할 수 없는가?**  

추상 클래스는 인스턴스화할 수 없다. 이는 추상 클래스가 완전한 구현을 제공하지 않기 때문이다. 추상 클래스는 최소한 하나 이상의 추상 메서드를 포함하고 있으며, 이러한 메서드는 자식 클래스에서 반드시 구현해야 한다. 따라서, 추상 클래스는 기본적인 틀을 제공하는 역할을 하며, 직접적으로 객체를 생성할 수는 없다.

**인터페이스의 기본 구현 메서드는 무엇인가?**  

C# 8.0부터 인터페이스는 기본 구현을 제공할 수 있는 기능이 추가되었다. 이를 통해 인터페이스 내에서 메서드의 기본 구현을 정의할 수 있으며, 이를 구현하는 클래스는 필요에 따라 해당 메서드를 오버라이드할 수 있다. 기본 구현 메서드는 인터페이스의 유연성을 높이고, 기존 인터페이스에 새로운 기능을 추가할 때 호환성을 유지하는 데 도움을 준다.

<!--
## Related Technologies
**C#의 객체 지향 프로그래밍**
**다형성과 상속**
**SOLID 원칙**
**디자인 패턴에서의 인터페이스와 추상 클래스 활용**
-->

## Related Technologies

**C#의 객체 지향 프로그래밍**  

C#은 객체 지향 프로그래밍(OOP) 언어로, 객체와 클래스의 개념을 기반으로 설계되었다. 객체 지향 프로그래밍은 코드의 재사용성과 유지보수성을 높이는 데 큰 도움을 준다. C#에서는 클래스와 객체를 통해 데이터와 기능을 묶어 관리할 수 있으며, 이를 통해 복잡한 시스템을 보다 쉽게 설계하고 구현할 수 있다. 객체 지향 프로그래밍의 주요 특징으로는 캡슐화, 상속, 다형성이 있다. 이러한 특징들은 C#의 인터페이스와 추상 클래스의 사용에 큰 영향을 미친다.

**다형성과 상속**  

다형성은 동일한 인터페이스를 통해 서로 다른 객체를 다룰 수 있는 능력을 의미한다. C#에서는 다형성을 통해 코드의 유연성을 높일 수 있으며, 이는 인터페이스와 추상 클래스의 중요한 특징 중 하나이다. 상속은 기존 클래스의 속성과 메서드를 새로운 클래스에서 재사용할 수 있게 해준다. C#에서는 추상 클래스를 통해 상속을 구현할 수 있으며, 이를 통해 코드의 중복을 줄이고, 유지보수를 용이하게 할 수 있다.

**SOLID 원칙**  

SOLID 원칙은 객체 지향 프로그래밍에서의 설계 원칙으로, 소프트웨어의 유지보수성과 확장성을 높이는 데 도움을 준다. SOLID는 다음과 같은 다섯 가지 원칙으로 구성된다: 

1. **단일 책임 원칙(SRP)**: 클래스는 하나의 책임만 가져야 한다.
2. **개방-폐쇄 원칙(OCP)**: 클래스는 확장에는 열려 있어야 하고, 수정에는 닫혀 있어야 한다.
3. **리스코프 치환 원칙(LSP)**: 자식 클래스는 부모 클래스를 대체할 수 있어야 한다.
4. **인터페이스 분리 원칙(ISP)**: 클라이언트는 자신이 사용하지 않는 인터페이스에 의존하지 않아야 한다.
5. **의존성 역전 원칙(DIP)**: 고수준 모듈은 저수준 모듈에 의존해서는 안 된다.

이 원칙들은 C#에서 인터페이스와 추상 클래스를 설계하고 구현하는 데 중요한 가이드라인이 된다.

**디자인 패턴에서의 인터페이스와 추상 클래스 활용**  

디자인 패턴은 소프트웨어 설계에서 자주 발생하는 문제를 해결하기 위한 일반적인 솔루션이다. C#에서는 인터페이스와 추상 클래스를 활용하여 다양한 디자인 패턴을 구현할 수 있다. 예를 들어, 전략 패턴에서는 인터페이스를 사용하여 알고리즘을 캡슐화하고, 팩토리 패턴에서는 추상 클래스를 사용하여 객체 생성의 책임을 분리할 수 있다. 이러한 패턴들은 코드의 재사용성을 높이고, 시스템의 유연성을 증가시키는 데 기여한다. 

이와 같이 C#의 인터페이스와 추상 클래스는 객체 지향 프로그래밍의 핵심 개념과 밀접하게 연관되어 있으며, 다양한 기술과 원칙을 통해 소프트웨어 개발의 품질을 높이는 데 중요한 역할을 한다.

<!--
## 결론
**주요 포인트 요약**
**인터페이스와 추상 클래스의 중요성**
**C#에서의 추상화 개념의 활용**
**향후 학습 방향 제안**
-->

## 결론

**주요 포인트 요약**  

C#에서 인터페이스와 추상 클래스는 객체 지향 프로그래밍의 중요한 개념이다. 이 두 가지는 코드의 재사용성과 유지보수성을 높이는 데 기여한다. 인터페이스는 다중 상속을 지원하며, 클래스가 특정 기능을 구현하도록 강제하는 역할을 한다. 반면, 추상 클래스는 공통된 기능을 제공하면서도 인스턴스화할 수 없는 특성을 가진다. 이 두 가지를 적절히 활용하면 더 나은 소프트웨어 설계를 할 수 있다.

**인터페이스와 추상 클래스의 중요성**  

인터페이스와 추상 클래스는 소프트웨어 개발에서 중요한 역할을 한다. 이들은 코드의 유연성을 높이고, 다양한 구현체를 통해 다형성을 제공한다. 인터페이스는 여러 클래스가 동일한 메서드를 구현하도록 강제함으로써 일관성을 유지하게 해준다. 추상 클래스는 공통된 기능을 제공하여 코드 중복을 줄이는 데 도움을 준다. 이러한 특성 덕분에 개발자는 더 효율적이고 관리하기 쉬운 코드를 작성할 수 있다.

**C#에서의 추상화 개념의 활용**  

C#에서 추상화는 복잡한 시스템을 단순화하는 데 중요한 역할을 한다. 인터페이스와 추상 클래스를 통해 개발자는 시스템의 세부 사항을 숨기고, 사용자에게 필요한 기능만을 제공할 수 있다. 이는 코드의 가독성을 높이고, 유지보수를 용이하게 한다. 또한, 추상화는 시스템의 변경에 대한 유연성을 제공하여, 새로운 기능을 추가하거나 기존 기능을 수정할 때 발생할 수 있는 문제를 최소화한다.

**향후 학습 방향 제안**  

C#의 인터페이스와 추상 클래스에 대한 이해를 바탕으로, 더 나아가 SOLID 원칙과 디자인 패턴을 학습하는 것이 좋다. SOLID 원칙은 객체 지향 설계의 기본 원칙으로, 코드의 품질을 높이는 데 기여한다. 또한, 디자인 패턴을 통해 다양한 문제를 해결하는 방법을 배우고, 실제 프로젝트에서의 적용 사례를 통해 실력을 쌓는 것이 중요하다. 이러한 학습을 통해 개발자는 더 나은 소프트웨어를 설계하고 구현할 수 있는 능력을 갖추게 될 것이다.

<!--
##### Reference #####
-->

## Reference


* [https://holjjack.tistory.com/41](https://holjjack.tistory.com/41)
* [https://paparoni-story.tistory.com/120](https://paparoni-story.tistory.com/120)
* [https://imcoding-official.tistory.com/46](https://imcoding-official.tistory.com/46)
* [https://velog.io/@ssu_hyun/이것이-C이다-8.-인터페이스와-추상-클래스](https://velog.io/@ssu_hyun/이것이-C이다-8.-인터페이스와-추상-클래스)
* [https://daekyoulibrary.tistory.com/entry/C-인터페이스와-클래스의-사이-추상-클래스Abstract-Class](https://daekyoulibrary.tistory.com/entry/C-인터페이스와-클래스의-사이-추상-클래스Abstract-Class)
* [https://narakit.tistory.com/237](https://narakit.tistory.com/237)
* [https://ifhead.tistory.com/entry/C-Abstract%EC%B6%94%EC%83%81Virtual%EA%B0%80%EC%83%81Interface%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4-%EC%B0%A8%EC%9D%B4](https://ifhead.tistory.com/entry/C-Abstract%EC%B6%94%EC%83%81Virtual%EA%B0%80%EC%83%81Interface%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4-%EC%B0%A8%EC%9D%B4)


<!--
![https://blog.kakaocdn.net/dn/dvBma9/btqAowX7Zfo/F9qkvgWA8rQKwNXAZCkgFk/img.png](https://blog.kakaocdn.net/dn/dvBma9/btqAowX7Zfo/F9qkvgWA8rQKwNXAZCkgFk/img.png)

###  C# 인터페이스와 추상클래스의 차이점

|  **Interface** |  **Abstract Class**  
---|---|---  
**접근 지정자** |  \- 함수에 대한 접근 지정자를 가질수 없습니다.   
\- 기본적으로 public 입니다.  |  \- 함수에 대한 접근 지정자를 가질 수 있습니다.   
**구현** |  \- 구현이 아닌 서명만 가질 수 있습니다.  |  \- 구현을 제공할 수 있습니다.   
**속도** |  \- 인터페이스가 상대적으로 느립니다.  |  \- 추상 클래스가 빠릅니다.   
**인스턴스화** |  \- 인터페이스는 추상적이며 인스턴스화 할 수 없습니다.  |  \- 추상클래스는 인스턴스화 할 수 없습니다.   
**필드** |  \- 인터페이스는 필드를 가질 수 없습니다.  |  \- 추상클래스는 필드와 상수를 정의 할 수 있습니다.   
**메소드** |  \- 인터페이스에는 추상메소드만 있습니다.  |  \- 추상클래스에는 비추상메소드가 있을 수 있습니다.   
  
  * C#에서 클래스는 하나 이상의 인터페이스를 상속합니다. 그러나 클래스는 하나의 추상클래스만 상속 할 수 있습니다. 
  * C#에서 인터페이스는 생성자를 선언할 수 없습니다. 추상 클래스는 생성자를 선언할 수 있습니다. 
  * C#에서 인터페이스는 클래스의 외부 능력을 정의하는 데 사용됩니다. 추상 클래스는 클래스의 실제 ID를 정의하는 데 사용되며 객체 또는 동일한 유형으로 사용됩니다. 
  * C#에서 다양한 구현이 메소드 서명 만 공유하는 경우 인터페이스가 사용됩니다. 다양한 구현이 동일한 종류이고 동일한 동작 또는 상태를 사용하는 경우 추상 클래스가 사용됩니다. 
  * C#에서 새 메소드가 인터페이스에 추가 된 경우 모든 인터페이스가 구현 된 위치를 추적하고 해당 메소드의 구현도 추가해야합니다. 추상 클래스에서 새 메소드가 추가 된 경우 기본 구현을 추가 할 수있는 옵션이 있으므로 모든 기존 코드가 올바르게 작동합니다. 

* * *

###  정리

  
C#은 데이터 추상화에 사용되었습니다. 여러 클래스가 인터페이스를 구현해야하는 경우 인터페이스가 추상 클래스보다 낫습니다.  인터페이스
멤버는 정적일 수 없으며,  추상 클래스의 유일한 완전한 멤버는 정적 일 수 있습니다.

  
C#은 다중 상속을 지원하지 않으며 인터페이스는 주로 다중 상속을 구현하는 데 사용됩니다.

클래스는 하나 이상의 인터페이스를 구현할 수 있으며 하나의 추상 클래스에서만 상속합니다.

인터페이스는 주로 메서드 나 기능을 구현할 필요가없는 경우에만 사용됩니다.

추상 클래스는 최소한의 기본구현을 필요할때 사용됩니다.

C# 인터페이스와 추상클래스는 요구 사항에 따라 응용 프로그램을 개발하는 데 많이 사용되는 객체 지향 프로그래밍 개념입니다. 그것은 더
편안하고 비즈니스 요구 사항에 맞는 기술 리드에 의해 순수하게 선택됩니다.

C# 인터페이스와 추상 클래스는 모두 사용하기 쉽고 모든 프로그래밍 언어에서 쉽게 배울 수 있습니다.


-->

<!--






-->

<!--
객체지향 프로그래밍의 '꽃'인 인터페이스와 추상 클래스에 대해서 공부했습니다.

배우기에 앞서서는 인터페이스와 추상 클래스가 많이 비슷하기도 하고 다른 점이 뭐가 있을까에 대해서 궁금했었는데 빠르게 알아봅시다!

####  **# 인터페이스 선언**

C#의 인터페이스는 다음과 같이 생겼습니다.

    
    
    interface flyable
    {
        void fly();
    }

인터페이스에서는 **메서드** , **이벤트** , **인덱서** , **프로퍼티** 만을 가질 수 있고, 클래스의 선언과 비슷하지만 언뜻
보면 구현부가 없고 함수의 정의 부분만 있습니다.

인터페이스에서는 접근 제한 한정자를 사용할 수 없으며, 모든 것들이 public으로 선언됩니다.

클래스와는 다르게 인스턴스화를 만들 수 도 없고요.

다만, 인터페이스를 상속한 클래스에서는 인스턴스를 만드는 것이 가능합니다.

상속받은 클래스에서는 인터페이스에서 선언된 모든 메서드 및 프로퍼티를 구현해줘야하고, 이 메서드들은 public 한정자로 수식해야 합니다.

더 나아가면 인터페이스는 분명 인스턴스화를 하지 못하지만 그것을 상속받은 클래스에서는 인스턴스를 만들 수 있고 그것을 인터페이스가 참조할 수
있습니다.

이러한 것이 가능한 이유는 파생 클래스도 기반 클래스와 같은 형식으로 간주된다는 것에서부터 시작됩니다. 인터페이스를 상속받은 클래스의
관계에서도 동일합니다.

####  **# 인터페이스는 왜 쓰는 것일까?**

저도 항상 인터페이스하면 고개를 끄덕끄덕했지만 정작 왜 사용하는지에 대해서 의문이 많았습니다.

인터페이스를 한 마디로 정의하면  **약속** 이라고 합니다.

인터페이스를 가지고 있는 클래스들은 인터페이스에서 정의한 모든 것들을 구현해야 한다는 약속을 가지고 있기 때문입니다.

또, 어떤 프로그램을 사용할 때 사용자의 입맛에 따라 결정을 해야한다고 할 때 인터페이스는 아주 훌륭한 해결책이 되기도 합니다.

인터페이스를 상속받는 객체는 인터페이스의 역할을 가지고 있기 때문에 인터페이스 명만 봐도 이 클래스가 어떤 지원을 하는지 대략적으로 알 수
도 있습니다.

아래에는 어떤 모니터에서 사용자로부터 입력받은 온도를 기록한다고 했을 때, logger가 어떻게 이 메시지를 기록할지 정해주는 방법입니다.

    
    
    using System;
    using System.IO;
    
    namespace Interface
    {
        interface ILogger // 인터페이스!
        {
            void WriteLog(string message);
        }
    
        // 나는 Console에 로그를 저장하겠다.
        class ConsoleLogger : ILogger
        {
            public void WriteLog(string message)
            {
                Console.WriteLine($"{DateTime.Now.ToLocalTime()}, {message}");
            }
        }
    
        // 나는 파일에 로그를 저장하겠다.
        class FileLogger : ILogger
        {
            private StreamWriter writer;
    
            public FileLogger(string path)
            {
                writer = File.CreateText(path);
                writer.AutoFlush = true;
            }
    
            public void WriteLog(string message)
            {
                writer.WriteLine($"{DateTime.Now.ToLocalTime()}, {message}");
            }
        }
    
        class ClimateMonitor
        {
            private ILogger logger; // 어떤 로거를 사용할 지
            public ClimateMonitor(ILogger logger)
            {
                this.logger = logger;
            }
            public void start()
            {
                while(true)
                {
                    Console.WriteLine("온도를 입력 : ");
                    string temperature = Console.ReadLine();
                    if (temperature == "") break;
    
                    // 등록된 로거에 message를 넘겨준다.
                    logger.WriteLog($"현재 온도 : {temperature}");
                }
            }
        }
    
        class Program
        {
            static void Main()
            {
                ClimateMonitor monitor = new ClimateMonitor(new FileLogger("MyLog.txt"));
    
                monitor.start();
            }
        }
    }

ClimateMonitor는 현재 온도를 기록하려고 하는데 기록하는 방법은 많습니다. 콘솔에 출력하거나 혹은 파일에 저장하거나 등등. 그럴
때 이러한 것을 프로그래머가 입맛에 따라 결정할 수 있게 내부 변수로 인터페이스를 가질 수 있도록 선언하고, 생성자를 통해 어떤 로거를
사용할지 결정한 후 그 로거를 실행하는 방법입니다.

중요한 것은 ConsoleLogger와 FileLogger는 모두 ILogger로부터 상속받았기 때문에 ILogger가 두 클래스를 참조할
수 있습니다.

어떤가요. 느낌이왔나요?

게임으로 비유하면, 같은 두손검이라도 '쟈드'와 '그륜힐'은 외형과 성능이 다릅니다. 그런데 캐릭터에 착용하면 똑같은 두손검입니다. 따라서
어떤 두손검을 사용할지 캐릭터 내부 변수로 ISward 라는 것을 만들고 캐릭터를 생성할 때 어떤 검을 끼워줄지 매핑하면 됩니다.

####  **# 인터페이스도 상속할 수 있다?**

인터페이스는 클래스는 물론 구조체도 인터페이스를 상속할 수 있습니다.

그런데 문제점이 발생합니다.

기존에 상속받아서 사용하고 있었는데 인터페이스 내부를 수정하려고 한다면? 펑;;;;

왜냐하면 인터페이스를 상속받은 것들은 모두 그 안에 있는 것을 구현해줘야 하기 때문입니다.

따라서 기존의 소스 코드에 영향을 주지 않고도 새로운 기능을 추가하기 위해서는 인터페이스를 상속하는 인터페이스를 이용하는 것이 좋다고
합니다. (프로젝트가 작으면 문제없지만, 방대하다면 어느 세월에 고칠까요? 게다가 고친다고 해도 사이드 이펙트는??? => 야근)

또 상속하려는 인터페이스가 소스 코드가 아닌 어셈블리만으로 제공되는 경우 우리가 내부 인터페이스를 수정할 수 없는 경우도 있습니다.

기존에 ILogger를 상속받는 IFormattableLogger는 다음과 같이 작성됩니다.

    
    
    interface IFormattableLogger : ILogger
    {
        void WriteLog(string format, params object[] args);
    }

매개변수로 기존 메시지와, 어떤 인자를 받을지 모르므로 모든 객체의 최상 부모인 object 형식으로 받고 있습니다.

직접 확인해봅시다!

    
    
    using System;
    
    namespace DerivedInterface
    {
        // 기존에 있던 인터페이스 입니다.
        interface ILogger
        {
            void WriteLog(string message);
        }
    
        // 추가 기능이 생겼습니다. (다양한 인자를 받고 싶어요!)
        interface IFormattableLogger : ILogger
        {
            void WriteLog(string format, params Object[] arges);
        }
    
        class ConsoleLogger : IFormattableLogger
        {
            public void WriteLog(string message)
            {
                Console.WriteLine($"{DateTime.Now.ToLocalTime()}, {message}");
            }
    
            public void WriteLog(string format, params Object[] args)
            {
                // 지정된 형식에 따라 개체의 값을 문자열로 변환합니다.
                String message = String.Format(format, args);
                Console.WriteLine($"{DateTime.Now.ToLocalTime()}, {message}");
            }
        }
    
        class Program
        {
            static void Main()
            {
                IFormattableLogger logger = new ConsoleLogger();
                logger.WriteLog("C# is good language");
                logger.WriteLog("{0} + {1} + {2} = {3}", 1, 2, 3, 6);
            }
        }
    }

####  **# 인터페이스는 다중 상속이 가능해?**

C#에서는 여러 클래스를 한꺼번에 상속할 수 없습니다.

어떤 클래스가 A로부터 상속받고, B로부터 상속받았는데 신기하게도 A에도 charge()가 있고, B에도 charge()라는 메서드가
있습니다. 그래서 어떤 charge()를 사용할지 모호하기 때문에 이것을 **죽음의 다이아몬드** 라고 합니다.

컴퓨터 세계에서는 모호한 프로그램을 재앙이라고 합니다. 문법의 사소한 한 톨이라도 틀리면 용납하지 않으니까요.

그런데 신기하게도 _**인터페이스는 다중 상속을 지원** _ 합니다.

이것도 쓸 수 있고 저것도 쓸 수 있습니다. 이게 가능한 이유는 인터페이스의 경우 외형만 물려주기 때문에 속이 어떨지 몰라도 겉모습만큼은
확실하게 같아야 합니다. 따라서 죽음의 다이아몬드 문제도 생기지 않습니다.

다중 상속의 인터페이스 확인해봅시다!

    
    
    using System;
    
    namespace MultiInterfaceInheritance
    {
        interface IRunable
        {
            void Run(); // 나를 받으면 달릴 수 있어
        }
    
        interface IFlyable
        {
            void Fly(); // 나를 받으면 날 수 있어
        }
    
        class FlyingOrc : IRunable, IFlyable
        {
            public void Run()
            {
                Console.WriteLine("난 오크 뛴다!");
            }
            public void Fly()
            {
                Console.WriteLine("난 오크 날기도 한다!");
            }
        }
    
        class Program
        {
            static void Main()
            {
                FlyingOrc orc = new FlyingOrc();
                orc.Run();
                orc.Fly();
    
                IRunable runnable = orc as IRunable;
                runnable.Run();
    
                IFlyable flyable = orc as IFlyable;
                flyable.Fly();
            }
        }
    }

오크는 뛰기와 날기라는 인터페이스를 모두 가지고 있기 때문에 둘 다 사용할 수 있습니다. 즉 다중 인터페이스 상속이 가능하게 되었습니다.
무서운 오크죠.

####  **# 인터페이스의 기본 구현 메서드**

기존까지 알고 있었던 인터페이스는 구현부를 만들 수 없었습니다. 그런데? 가능하게 할 수 있습니다.

가능하게 하기 전에 왜 필요할 지부터 보겠습니다.

초기 버전을 설계할 때는 이렇게 사용하도록 인터페이스를 정의하고 서비스해왔는데 다시 보니까 이 기능이 빠져있었던 것입니다. 그래서 개발자는
그 인터페이슬 수정하려고 했으나 아차!.. 그것을 상속받아 사용하는 개체가 +99개인 겁니다.. 어떻게 하면 안전하게 추가할 수 있을까요?

여기서 등장한 것이 바로 **기본 구현 메서드** 입니다.

인터페이스를 수정했지만 다른 기존 코드에는 아무런 영향을 받지 않습니다.

게다가 인터페이스의 기본 구현 메서드는 인터페이스 참조로 업 캐스팅 했을 때만 사용할 수 있기 때문에 프로그래머가 파생 클래스에서
인터페이스에 추가된 메서드를 엉뚱하게 호출할 일도 없습니다.

살펴봅시다.

    
    
    using System;
    
    namespace DefaultImplemetation
    {
        interface ILogger
        {
            void WriteLog(string message);
            void WriteError(string error)
            {
                WriteLog(error); // 구현부가 있네요!
            }
        }
    
        class ConsoleLogger : ILogger
        {
            public void WriteLog(string message)
            {
                Console.WriteLine($"{message}");
            }
        }
    
        class Program
        {
            static void Main()
            {
                ILogger logger = new ConsoleLogger();
                // 업캐스팅일 때 다 사용할 수 있습니다!
                logger.WriteLog("System Up");
                logger.WriteError("Error!!");
    
                // 프로그래머가 엉뚱한 호출을 사용을 못하게 막습니다.
                ConsoleLogger clogger = new ConsoleLogger();
                clogger.WriteLog("System Up");
                //clogger.WriteError("난 왜 안돼?");
            }
        }
    }

####  **# 추상 클래스는 인터페이스와 클래스 사이**

추상 클래스는 인터페이스와 다르게 '구현'을 할 수 있습니다.

그렇지만 클래스와는 다르게 인스턴스화 및 인스턴스를 가질 수 없습니다.

=> 구현을 할 수 있지만 인스턴스를 만들지 못합니다.

인터페이스는 모든 메서드가 public이지만 클래스는 default가 private입니다.

추상 클래스는 추상 메서드를 가질 수 있습니다. 이것 때문에 인터페이스와도 유사합니다.

추상 메서드는 구현을 못하지만 파생 클래스에서는 반드시 구현하도록 강제가 됩니다. (인터페이스와 유사)

추상 클래스를 이용한 프로그램을 살펴봅시다.

    
    
    using System;
    
    namespace AbstractClass
    {
        abstract class AbstractBase
        {
            protected void PrivateMethodA()
            {
                Console.WriteLine("AbstractBase.PrivateMethodA()");
            }
    
            public void PublicMethodA()
            {
                Console.WriteLine("PublicMethodA()");
            }
    
            // 추상 메서드
            public abstract void AbstractMethodA();
        }
    
        class Derived : AbstractBase
        {
            // 구현하기!
            public override void AbstractMethodA()
            {
                Console.WriteLine("Derived.AbstractMethodA()");
                // 상속받았기 때문에 사용할 수 있습니다.
                PrivateMethodA();
            }
        }
    
        class Program
        {
            static void Main()
            {
                AbstractBase obj = new Derived();
                obj.AbstractMethodA();
                // 상속받았기 때문에 사용할 수 있습니다.
                obj.PublicMethodA();
            }
        }
    }

추상 클래스는 일반 클래스가 가질 수 있는 구현 + 추상 메서드를 가지고 있습니다. (인터페이스 역할)

추상 메서드는 추상 클래스를 사용하는 프로그래머가 그 기능을 정의하도록 강제하는 장치이기 때문에 혹여나 실수를 하더라도 컴파일러가 이를
상기시켜줄 수 있습니다. 그래서 추상 클래스를 사용합니다.

길고 길었지만,

\- 인터페이스를 왜 사용하는지?

\- 인터페이스와 클래스의 차이

\- 인터페이스와 추상 클래스의 차이

에 대해서 배웠습니다.


-->

<!--






-->

<!--
##  소개

안녕하세요 아임코딩입니다.

이번에는 C#에서 사용하는 추상화에 대해서 알아보겠습니다.

##  유튜브 링크

[ https://youtu.be/tZoe_tdgMEY ](https://youtu.be/tZoe_tdgMEY)

VIDEO

##  추상화

  * 추상이란 사물이나 표상(表象)을 어떤 성질·공통성·본질에 착안하여 그것을 추출(抽出)하여 파악하는 것 
  * 결국 어떤 공통적인 성질이나 본질을 추출하여 파악하는 것이 추상화의 핵심입니다. 
  * 추상화의 핵심은 구체적인 사물을 추상적으로 표현하는 것입니다. 객체 지향 프로그래밍에서는 추상화를 통해 클래스를 정의하고, 인스턴스를 생성하여 사용합니다. 

##  C#에서 추상화

  * 클래스 : 현실에 있는 다양한 사물들을 공통성, 본질을 추출하여 데이터와 메서드로 만들어서 제공합니다. 
  * 추상 클래스 : 클래스들에서 공통적으로 사용되는 변수나 메서드를 추출하여 추상 클래스를 만들 수 있습니다. 추상 클래스는 객체를 만들 수 없고, 상속을 하는 역할로만 사용합니다. 추상 클래스에는 추상 메서드를 선언하는데 정의하지는 않고 추상 메서드의 정의는 자식 클래스에서 진행합니다. 
  * 인터페이스 : 인터페이스는 추상 클래스와 비슷하지만, 모든 멤버가 추상 메서드와 상수로만 이루어져 있습니다. 인터페이스를 구현하는 클래스는 인터페이스에서 정의한 모든 메서드를 반드시 구현해야 합니다. 인터페이스는 다중 상속을 지원하며, 클래스의 계층 구조를 유연하게 설계할 수 있도록 도와줍니다. 
  * 클래스 : class 키워드를 사용합니다. 
  * 추상 클래스 : abstract 키워드를 사용합니다. 
  * 인터페이스 : interface 키워드를 사용합니다. 

##  클래스

클래스는 일상에 있는 사물들의 특성을 추출하여 데이터 필드와 메서드로 나타낸 것으로 실제 사물들을 추상화한 결과라고 할 수 있습니다.

클래스에 대한 자세한 내용은 이전에 발행한 클래스에 대한 글을 참조해주시기 바랍니다.

[ 2023.05.05 - [프로그래밍/C#] - [C#] 클래스 ](https://imcoding-
official.tistory.com/entry/C-%ED%81%B4%EB%9E%98%EC%8A%A4)

[ [C#] 클래스  안녕하세요 아임코딩입니다. 이번에는 C#의 핵심이라고 할 수 있는 클래스에 대해서 알아보겠습니다. 객체 지향
프로그래밍에서 가장 중요한 개념 중 하나가 클래스입니다. 클래스는 데이터와  imcoding-official.tistory.com
](https://imcoding-official.tistory.com/entry/C-%ED%81%B4%EB%9E%98%EC%8A%A4)

##  추상 클래스

C#에서는 추상 클래스를 제공합니다. 추상 클래스는 클래스들의 공통점을 모아서 상속할 부모 클래스를 만들 때 주로 사용합니다. 추상
클래스에는 추상 메서드와 일반 메서드가 함께 존재할 수 있습니다.

추상 클래스는 다음과 같은 형식을 가집니다.

    
    
    abstract class [클래스 이름]
    {
    	//필드
        //메서드
    }

C# 코드 상에서 추상 클래스를 구현해보고 상속받아 사용해보겠습니다.

###  추상 클래스 부모 클래스

    
    
        abstract class Parent       //추상 클래스
        {
            public string name = "tom";
    
            public abstract void printName();   //추상 메서드
            
            public void nomalMethod()   //추상 클래스의 일반 메서드
            {
                Console.WriteLine("Parent 클래스의 일반 메서드입니다.");
            }
        }

abstract 키워드로 추상 클래스를 만들 수 있습니다.

추상 클래스는 일반 클래스와 유사하게 필드, 메서드를 갖지만 차이점은

추상 메서드를 가진다는 점입니다.

추상 메서드는 반드시 자식 클래스에서 재정의 해야합니다.

추상 메서드를 자식 클래스에서는 override 키워드를 사용해서 추상 메서드를 재정의합니다.

###  추상 클래스 자식 클래스

Parent 클래스를 상속받는 Child 클래스의 예입니다.

    
    
        class Child : Parent
        {
            public override void printName()
            {
                Console.WriteLine(name);
            }
        }

Child 클래스는 Parent 클래스의

private string name = "tom;

public abstract void printName();

public void nomalMethod()

세 가지 모두를 상속받습니다.

하지만 printName() 메서드는 추상 메서드이기 때문에 반드시 자식 클래스에서 재정의 해줘야 합니다.

그래서 Child 클래스에서 override 키워드를 이용하여 printName() 메서드를 재정의 해줬습니다.

###  추상 클래스 프로그램 전체 코드

이제 프로그램의 전체 코드를 살펴보겠습니다.

    
    
    using System;
    namespace CSTistory
    {
        abstract class Parent       //추상 클래스
        {
            public string name = "tom";
    
            public abstract void printName();   //추상 메서드
            
            public void nomalMethod()   //추상 클래스의 일반 메서드
            {
                Console.WriteLine("Parent 클래스의 일반 메서드입니다.");
            }
        }
    
        class Child : Parent
        {
            public override void printName()    //부모 클래스의 추상 메서드 재정의
            {
                Console.WriteLine(name);
            }
        }
    
        internal class Program
        {
            static void Main(string[] args)
            {
                Child child = new Child();
    
                child.printName();      //자식 클래스에서 재정의한 추상 메서드 호출
                child.nomalMethod();    //부모 클래스의 일반 메서드 호출
            }
        }
    }

![https://blog.kakaocdn.net/dn/dgwtNZ/btsd4F2hDRO/k91YSGYwSAFZe4U92CTFjK/img.png](https://blog.kakaocdn.net/dn/dgwtNZ/btsd4F2hDRO/k91YSGYwSAFZe4U92CTFjK/img.png)

Main 함수에서

Child 클래스의 객체를 생성하고

child.printName() 에서 자식 클래스에서 재정의한 추상 메서드를 호출합니다.

child.nomalMethod() 에서 부모 클래스의 일반 메서드를 호출합니다.

따라서 결과는 두 메서드가 실행한 결과인

"tom"

"Parent 클래스의 일반 메서드입니다."

가 출력되는 것입니다.

##  인터페이스

인터페이스는 추상 메서드만 모아놓은 것이라고 생각하면 쉽다.

필드와 일반 메서드를 가지지 않는 추상 클래스라고 생각해도 괜찮다.

다른 말로 하면 추상 메서드만 가지고 있는 추상 클래스라고 생각해도 된다.

인터페이스에서 선언한 함수는 abstract 키워드를 사용할 필요가 없다.

인터페이스에서 상속받은 함수는 재정의할 때 override 키워드를 사용할 필요가 없다.

###  인터페이스 형식

인터페이스는 다음과 같은 형식으로 선언한다.

    
    
    [접근제한자] interface [인터페이스 이름]
    {
    	//메서드 선언
    }

관례적으로 인터페이스의 이름에는 I 접두사를 붙여준다.

인터페이스를 간단하게 구현해보면 다음과 같다.

인터페이스 내에 추상 메서드를 선언할 때는 abstract 키워드가 필요없다.

    
    
        public interface IMyInterface
        {
            public void myPrint();
        }

###  인터페이스 상속

인터페이스를 상속받은 클래스의 예는 아래와 같다.

    
    
        public class MyClass : IMyInterface
        {
            public void myPrint()
            {
                Console.WriteLine("인터페이스를 통해 상속받은 메서드를 재정의한 함수입니다.");
            }
        }

인터페이스에서 상속받은 메서드를 재정의할 때는 override 키워드를 사용할 필요가 없다.

###  인터페이스 전체 프로그램 코드

위에서 구현한 인터페이스와

인터페이스를 상속받는 클래스의 객체를 만들고

자식 클래스에서 재정의한 함수를 호출하는 프로그램을 확인해보겠습니다.

    
    
    using System;
    namespace CSTistory
    {
        public interface IMyInterface   //인터페이스
        {
            public void myPrint();      //메서드 선언
        }
    
        public class MyClass : IMyInterface //인터페이스 상속
        {
            public void myPrint()       //인터페이스 추상 메서드 구현
            {
                Console.WriteLine("인터페이스를 통해 상속받은 메서드를 재정의한 함수입니다.");
            }
        }
    
        internal class Program
        {
            static void Main(string[] args)
            {
                MyClass myClass = new MyClass();    //MyClass 클래스 객체 생성
    
                myClass.myPrint();                  //재정의한 함수 호출
            }
        }
    }

![https://blog.kakaocdn.net/dn/ZJ3yr/btsdZyReMFj/O8hCCIupxcYYBotTkTB6s0/img.png](https://blog.kakaocdn.net/dn/ZJ3yr/btsdZyReMFj/O8hCCIupxcYYBotTkTB6s0/img.png)

Main 함수에서

MyClass 클래스의 myClass 객체를 생성하고

인터페이스에서 상속받아 재정의한 함수인 myPrint() 함수를 호출합니다.

따라서 결과는 다음과 같이 나오는 것을 확인할 수 있습니다.

이상으로 C#에서 구현할 수 있는 추상화에 대해서 알아봤습니다.


-->

<!--






-->

<!--
#  Key point

#  8.1 인터페이스(Interface)

  * 클래스의 청사진 
    * 클래스가 해야하는 행동을 결정   
= 클래스가 어떤 메소드를 가질지 결정

  * 선언 : ` interface ` 키워드 이용   
![https://velog.velcdn.com/images/ssu_hyun/post/71063c69-057f-476b-805d-597f4e246ba9/image.png](https://velog.velcdn.com/images/ssu_hyun/post/71063c69-057f-476b-805d-597f4e246ba9/image.png)

  * 대개 ` I ` 로 시작하는 이름으로 명명 
  * 메소드 **구현** , 필드 X 
  * 메소드, 이벤트, 인덱서, 프로퍼티만을 가질 수 있다. 
  * 접근 제한 한정자를 사용할 수 없고 모든 것이 ` public ` 으로 선언됨 
  * 인스턴스를 가질 수는 없지만, 인터페이스를 상속받는 클래스의 인스턴스를 만드는 것은 가능하다. 참조를 만들어 여기에 파생 클래스의 객체 위치를 담는 것 
  * **파생 클래스는 기반 클래스와 같은 형식으로 간주한다  
= ConsoleLogger의 객체는 ILogger의 객체로 취급할 수 있다. **

> 예제 프로그램

    
    
       
       interface ILogger
       {
           void WriteLog(string message);
       }
       
       
       class ConsoleLogger : ILogger  
       {
           public void WriteLog(string message)  
           {
               Console.WriteLine(
                        "{0} {1}",
                        DateTime.Now.ToLocalTime(), message);
            }
        }
        
        
        ILogger logger = new ConsoleLogger();
        logger.WriteLog("Hello, World!");

#  8.2 인터페이스는 약속이다

  * 인터페이스는 클래스가 따라야 하는 약속 
    * 인터페이스의 파생 클래스는 인터페이스에 선언된 **① 모든 메소드(및 프로퍼티)를 구현** 해줘야 하며 이 메소드들은 **②` public ` 한정자 ** 로 수식해야 한다. 
  * 상속을 통한 connect 역할 
    * 어떤 클래스든 인터페이스를 위의 약속을 지켜 상속받아 구현하면 인터페이스 즉 기반클래스(부모 클래스)의 역할을 할 수 있다. 
    * **` 기반 클래스(부모) ≒ 파생 클래스(자식) ` ** 이 성립되는 것 

> 예제 프로그램 - ` 콘솔에 로그 출력 `
    
    
    using System;
    using System.IO;
    
    namespace Interface
    {
    	
       interface ILogger
       {
           void WriteLog(string message);
       }
    
       
       class ConsoleLogger : ILogger
       {
           public void WriteLog(string message) 
           {
               Console.WriteLine(
                        "{0} {1}",
                        DateTime.Now.ToLocalTime(), message);
           }
       }
    
       class ClimateMonitor
       {
           private ILogger logger;  
           public ClimateMonitor(ILogger logger)  
           {
               this.logger = logger;
           }
    
           public void start()
           {
               while (true)
               {
                   Console.Write("온도를 입력해주세요. : ");
                   string temperature = Console.ReadLine();  
                   if (temperature == "")
                       break;
    
                   logger.WriteLog("현재 온도 : " + temperature);
               }
           }
       }
    
       class MainApp
       {
           static void Main(string[] args)
           {
               
               ClimateMonitor monitor = new ClimateMonitor(new ConsoleLogger());
               monitor.start();
           }
       }
    } 

![https://velog.velcdn.com/images/ssu_hyun/post/272023d2-efad-4178-8e76-209192340c12/image.png](https://velog.velcdn.com/images/ssu_hyun/post/272023d2-efad-4178-8e76-209192340c12/image.png)

> 예제 프로그램 - ` 텍스트파일에 로그 출력 `
    
    
    using System;
    using System.IO;
    
     
     namespace Interface
    {
        interface ILogger
        {
            void WriteLog(string message);
        }
    
        
        class ConsoleLogger : ILogger
        {
            public void WriteLog(string message)
            {
                Console.WriteLine(
                         "{0} {1}",
                         DateTime.Now.ToLocalTime(), message);
            }
        }
    
        
        class FileLogger : ILogger
        {
            private StreamWriter writer;
    
            public FileLogger(string path)
            {
                writer = File.CreateText(path);
                writer.AutoFlush = true;
            }
    
            public void WriteLog(string message)
            {
                 writer.WriteLine("{0} {1}", DateTime.Now.ToShortTimeString(), message);
            }
        }
    
        class ClimateMonitor
        {
            private ILogger logger;  
            public ClimateMonitor(ILogger logger)  
            {
                this.logger = logger;
            }
    
            public void start()
            {
                while (true)
                {
                    Console.Write("온도를 입력해주세요. : ");
                    string temperature = Console.ReadLine();  
                    if (temperature == "")
                        break;
    
                    logger.WriteLog("현재 온도 : " + temperature);
                }
            }
        }
    
        class MainApp
        {
            static void Main(string[] args)
            {
                
                ClimateMonitor monitor = new ClimateMonitor(new FileLogger("MyLog.txt"));
                monitor.start();
            }
        }
    }

![https://velog.velcdn.com/images/ssu_hyun/post/836ccfce-2456-4a98-9945-25f42dd8da85/image.png](https://velog.velcdn.com/images/ssu_hyun/post/836ccfce-2456-4a98-9945-25f42dd8da85/image.png)

  * cmd에서 ` txt파일 ` 한글깨짐 없이 여는 법 
    * ` type ` 명령어 통해 파일 읽기 ![https://velog.velcdn.com/images/ssu_hyun/post/6582ada4-cc49-4e7d-8d72-76762e4d7434/image.png](https://velog.velcdn.com/images/ssu_hyun/post/6582ada4-cc49-4e7d-8d72-76762e4d7434/image.png)
    * chcp( **CH** ange **C** ode **P** ages) : **cmd 상의 언어를 바꾸는 명령어**
    * 한글코드인 ` 949 ` 에서 한글이 깨지는 문제가 발생하므로 유니코드 ` 65001 ` 설정   
_*유니코드 : 모든 언어를 표시할 수 있는 코드_
![https://velog.velcdn.com/images/ssu_hyun/post/5bfd6e65-b25c-4940-9a8b-7fb22322e801/image.png](https://velog.velcdn.com/images/ssu_hyun/post/5bfd6e65-b25c-4940-9a8b-7fb22322e801/image.png)
![https://velog.velcdn.com/images/ssu_hyun/post/36c95058-212a-47d6-8cf0-134d0656c161/image.png](https://velog.velcdn.com/images/ssu_hyun/post/36c95058-212a-47d6-8cf0-134d0656c161/image.png)

> 예제 프로그램 - ` 상속을 통한 class connect 역할 `
    
    
    using System;
    using System.IO;
    
    namespace Interface
    {
        interface ILogger
        {
            void WriteLog(string message);
        }
    
    
        
    
    
        
        class ConsoleLogger : ILogger
        {
            public void WriteLog(string message)
            {
                Console.WriteLine(
                         "{0} {1}",
                         DateTime.Now.ToLocalTime(), message);
            }
        }
    
        
        class FileLogger : ILogger
        {
            private StreamWriter writer;
    
            public FileLogger(string path)
            {
                writer = File.CreateText(path);
                writer.AutoFlush = true;
            }
    
            public void WriteLog(string message)
            {
                 writer.WriteLine("{0} {1}", DateTime.Now.ToShortTimeString(), message);
            }
        }
    
        class ClimateMonitor
        {
            private ILogger logger; 
            public ClimateMonitor(ILogger logger)  
            {
                this.logger = logger;
            }
    
            public void start()
            {
                while (true)
                {
                    Console.Write("온도를 입력해주세요. : ");
                    string temperature = Console.ReadLine();  
                    if (temperature == "")
                        break;
    
                    logger.WriteLog("현재 온도 : " + temperature);
                }
            }
        }
    
        class MainApp
        {
            static void Main(string[] args)
            {
                
    
                ClimateMonitor monitor = new ClimateMonitor(new FileLogger("MyLog.txt"));
    
                monitor.start();
            }
        }
    }

![https://velog.velcdn.com/images/ssu_hyun/post/8c7c8705-848f-4588-af57-fca898a9521b/image.png](https://velog.velcdn.com/images/ssu_hyun/post/8c7c8705-848f-4588-af57-fca898a9521b/image.png)

> _[비타민 퀴즈]  
>  ClimateMonitor의 logger가 ConsoleLogger의 객체를 가리킬 경우 실행 결과 _
>  
>  
>     ClimateMonitor monitor = new ClimateMonitor(new ConsoleLogger());
>
>
> ![https://velog.velcdn.com/images/ssu_hyun/post/45c0ccc8-0c7d-486a-b3ff-39f056c9e59c/image.png](https://velog.velcdn.com/images/ssu_hyun/post/45c0ccc8-0c7d-486a-b3ff-39f056c9e59c/image.png)

#  8.3 인터페이스를 상속하는 인터페이스

> 예제 프로그램
    
    
    using System;
    
    namespace DerivedInterface
    {	
    	
        interface ILogger
        {
            void WriteLog(string message);
        }
    	
        
        interface IFormattableLogger : ILogger
        {
            void WriteLog(string format, params Object[] args);
        }
    	
        
        class ConsoleLogger2 : IFormattableLogger
        {
            public void WriteLog(string message)
            {
                Console.WriteLine(
                    $"{DateTime.Now.ToLocalTime()}, {message}");
            }
    
            public void WriteLog(string format, params Object[] args)
            {
                String message = String.Format(format, args);
                Console.WriteLine(
                    $"{DateTime.Now.ToLocalTime()}, {message}");
            }
        }
    	
        
        class MainApp
        {
            static void Main(string[] args)
            {
                IFormattableLogger logger = new ConsoleLogger2();
                logger.WriteLog("The world is not flat.");
                logger.WriteLog("{0} + {1} = {2}", 1, 1, 2);
            }
        }
    }

![https://velog.velcdn.com/images/ssu_hyun/post/bc16ccac-094c-41a2-8f59-55c0055070ac/image.png](https://velog.velcdn.com/images/ssu_hyun/post/bc16ccac-094c-41a2-8f59-55c0055070ac/image.png)

#  8.4 여러 개의 인터페이스, 한꺼번에 상속하기

  * 클래스는 프로그램의 모호성을 초래하는 "죽음의 다이아몬드"문제로 인해 **C#에서는 클래스의 다중 상속을 허용하지 않는다.**
  * **인터페이스의 다중 상속은 허용** (내용이 아닌 외형을 물려줌)   

> 예제 프로그램
    
    
    using System;
    
    namespace MultiInterfaceInheritance
    {
    	
        interface IRunnable
        {
            void Run();
        }
    
    	
        interface IFlyable
        {
            void Fly();
        }
    
    	
        class FlyingCar : IRunnable, IFlyable
        {
            public void Run()
            {
                Console.WriteLine("Run! Run!");
            }
    
            public void Fly()
            {
                Console.WriteLine("Fly! Fly!");
            }
        }
    
        class MainApp
        {
            static void Main(string[] args)
            {
                FlyingCar car = new FlyingCar();
                car.Run();
                car.Fly();
    
                IRunnable runnable = car as IRunnable;  
                runnable.Run();
    
                IFlyable flyable = car as IFlyable;  
                flyable.Fly();
            }
        }
    }

![https://velog.velcdn.com/images/ssu_hyun/post/dc25cb1f-1dad-4bf9-b46b-54430f5cc58b/image.png](https://velog.velcdn.com/images/ssu_hyun/post/dc25cb1f-1dad-4bf9-b46b-54430f5cc58b/image.png)

> _그래도 여러 클래스로부터 구현을 물려받고 싶다면?_
>
>   * 포함(Containment)기법  
>  : 클래스 안에 물려받고 싶은 기능을 가진 클래스들을 필드로 선언해 넣는 것
>

>  
>  
>     MyVehicle()
>     {
>         Car car = new Car();
>         Plane plane = new Plane();  
>         public void Fly() { plane.Ride(); }
>         public void Run() { car.Ride(); }
>     }

#  8.5 인터페이스의 기본 구현 메소드

> 예제 프로그램
    
    
    using System;
    
    namespace DefaultImplementation
    {
    	
        interface ILogger
        {
            void WriteLog(string message);
    
            void WriteError(string error) 
            {
                WriteLog($"Error: {error}");  
            }    
        }
    	
        
        class ConsoleLogger : ILogger
        {
            public void WriteLog(string message)
            {
                Console.WriteLine(
                    $"{DateTime.Now.ToLocalTime()}, {message}");
            }
        }
    	
        
        class MainApp
        {
            static void Main(string[] args)
            {
                ILogger logger = new ConsoleLogger();
                logger.WriteLog("System Up"); 
                logger.WriteError("System Fail");  
    
                ConsoleLogger clogger = new ConsoleLogger();
                clogger.WriteLog("System Up"); 
                
                
            }
        }
    }

  * 인터페이스에 선언된 기본 구현 인터페이스는 파생 클래스의 참조로 호출할 수 없다.   
![https://velog.velcdn.com/images/ssu_hyun/post/ae941023-123f-413f-a7dc-7a5e1b4603e8/image.png](https://velog.velcdn.com/images/ssu_hyun/post/ae941023-123f-413f-a7dc-7a5e1b4603e8/image.png)

#  8.6 추상 클래스 : 인터페이스와 클래스 사이

  * 메소드의 구현 가질 수 있음(=클래스) 

    * 추상 메소드(Abstract Method) : 추상 클래스에서 구현을 가지지 않는 메소드 
    * 추상 클래스의 파생 클래스는 **① 추상 메소드를 반드시 구현** 해야하며 (인터페이스 역할) **② public, protected, internal, protected internal 한정자 중 하나로 수식** 될 것 강조 
  * 객체 생성 불가(=인터페이스) 

  * 인터페이스를 제공하되 기본적인 구현을 함께 제공하고 싶을 경우 사용 

    * 파생 클래스가 구현해야할 **메소드 정의 강제와 기본적인 구현** 모두 하고 싶을 때 
  * 추상 클래스는 또 다른 추상 클래스를 상속할 수 있다. 

    * 이 경우 자식 추상 클래스는 부모 추상 클래스의 추상 메소드를 구현하지 않아도 된다. 
  * 사용 목적 : 내가 만든 추상 클래스를 이용할 때 이에 대한 규칙/약속 강제 

  * 선언 
    
        abstract class 클래스이름
    {
        
    }
    
    
    
    abstract class AbstractBase  
    {
        public abstract void SomeMethod();  
    }
    
    class Derived : AbstractBase
    {
        public override void SomeMethod()
        {
            
        }
    }

> 예제 프로그램
    
    
    using System;
    
    namespace AbstractClass
    {
        abstract class AbstractBase  
        {
            protected void PrivateMethodA()
            {
                Console.WriteLine("AbstractBase.PrivateMethodA()");
            }
    
            public void PublicMethodA()
            {
                Console.WriteLine("AbstractBase.PublicMethodA()");
            }
    
            public abstract void AbstractMethodA();  
        }
    
    	
        class Derived : AbstractBase
        {
        	
            public override void AbstractMethodA()
            {
                Console.WriteLine("Derived.AbstractMethodA()");
                PrivateMethodA();
            }
        }
    
        class MainApp
        {
            static void Main(string[] args)
            {
                AbstractBase obj = new Derived();
                obj.AbstractMethodA();
                obj.PublicMethodA();
            }
        }
    }

![https://velog.velcdn.com/images/ssu_hyun/post/5f5e8519-f019-48f4-8ac6-7aefdcc4e2ed/image.png](https://velog.velcdn.com/images/ssu_hyun/post/5f5e8519-f019-48f4-8ac6-7aefdcc4e2ed/image.png)

#  연습 문제

  1. 인터페이스와 클래스가 다른 점은 무엇입니까?   
: 인터페이스는 클래스와 달리 내부에 **메서드(함수)와 프로퍼티, 인덱서만 선언 가능** 하며, new 키워드를 통해 **인스턴스화 할 수
없다** . 또한 **접근 지정자가 기본적으로` public ` 으로 설정 ** 되어 있다. 따라서 해당 인터페이스를 상속받는 클래스를
만들어, 업 캐스팅 형식의 참조를 통해 인터페이스를 활용해야 한다.

인터페이스는 하나의 약속이다. 인터페이스를 상속받는 모든 파생 클래스들은 인터페이스에 선언되어 있는 함수를 무조건 정의해야 한다. 따라서
어떤 프로그래머가 해당 클래스가 어떤 인터페이스를 상속받고 있는지만 알고 있어도, 해당 클래스가 어떤 기능을 하는지 유추할 수 있다.

  2. 인터페이스와 추상 클래스가 다른 점은 무엇입니까?   
: 추상클래스는 인터페이스와 기본적으로 역할(함수의 정의를 강요)은 비슷하지만, 인터페이스와 달리 데이터(변수)를 선언할 수 있다. 또한
필요에 의해 함수를 정의해도 괜찮다. 추상 클래스에는 해당 클래스에서만 사용 가능한 추상 메서드라는 것이 존재하는데, 이는 인터페이스의
메서드와 같은 역할을 한다. 하지만 모든 추상 클래스 내의 메소드와 데이터는 private으로 설정되어 있기 때문에, 추상 메서드의 접근
지정자를 public으로 설정하는 것을 추천한다.


-->

<!--






-->

<!--
##  **ì¶”ìƒ� í�´ë�˜ìŠ¤ (Absract Class)**

####  **êµ¬í˜„ë¶€ë¥¼ ê°€ì§ˆ ìˆ˜ ì�ˆì§€ë§Œ, ì�¸ìŠ¤í„´ìŠ¤ëŠ” ìƒ�ì„±í• ìˆ˜
ì—†ë‹¤.**

ì¶”ìƒ� í�´ë�˜ìŠ¤ëŠ” _**êµ¬í˜„ë¶€** ë¥¼ ê°€ì§ˆ ìˆ˜ ì�ˆë‹¤. _ êµ¬í˜„ë¶€ë¥¼
ê°€ì§ˆ ìˆ˜ëŠ” ì�ˆì§€ë§Œ,  í�´ë�˜ìŠ¤ì™€ ë‹¬ë¦¬ ì�¸ìŠ¤í„´ìŠ¤ ìƒ�ì„±ì�€ í• ìˆ˜
ì—†ë‹¤.

í•˜ì§€ë§Œ  **ì¶”ìƒ� í�´ë�˜ìŠ¤ë¥¼ ìƒ�ì†� ë°›ì�€ í�´ë�˜ìŠ¤ì�˜ ì�¸ìŠ¤í„´ìŠ¤** ëŠ”
ìƒ�ì„± ê°€ëŠ¥  í•˜ë©°,  **ì—…ìº�ìŠ¤íŒ…** ë˜�í•œ ê°€ëŠ¥  í•˜ë‹¤.

ì¶”ìƒ� í�´ë�˜ìŠ¤ ì„ ì–¸ì�€ ë‹¤ì�Œê³¼ ê°™ì�´  **absract** í‚¤ì›Œë“œë¥¼
ì‚¬ìš©í•˜ì—¬ ì„ ì–¸í•œë‹¤.

    
    
    abstract class í�´ë�˜ìŠ¤ì�´ë¦„
    {
        // í�´ë�˜ìŠ¤ì™€ ë�™ì�¼í•˜ê²Œ êµ¬í˜„
    }

ì ‘ê·¼ì„± ì¸¡ë©´ì—�ì„œ ë³¸ë‹¤ë©´, **í�´ë�˜ìŠ¤ì™€ ë�” ê°€ê¹�ë‹¤.**

ì�¸í„°í�˜ì�´ìŠ¤ëŠ” ëª¨ë“ ë©”ì†Œë“œê°€ **public** ìœ¼ë¡œ ì„ ì–¸ë�˜ëŠ” ë°˜ë©´,
í�´ë�˜ìŠ¤ëŠ” í•œì •ì��ë¥¼ ëª…ì‹œí•˜ì§€ ì•Šìœ¼ë©´ ëª¨ë“ ë©”ì†Œë“œê°€
**private** ìœ¼ë¡œ ì„ ì–¸ë�œë‹¤.

####  **ì¶”ìƒ� ë©”ì†Œë“œ(Abstract Method)ë¥¼ ê°€ì§ˆ ìˆ˜ ì�ˆë‹¤.**

    
    
    abstract class AbstractClass
    {
        public abstract void AbstractMethod();    // ì¶”ìƒ� ë©”ì†Œë“œ
    }
    
    
    class DerivedClass : AbstractClass
    {
        public override void AbstractMethod()     // ì¶”ìƒ� ë©”ì†Œë“œ êµ¬í˜„ ê°•ì œ
        {
            ...
        }
    }

ì¶”ìƒ� ë©”ì†Œë“œëŠ” ì¶”ìƒ� í�´ë�˜ìŠ¤ê°€ **ì�¸í„°í�˜ì�´ìŠ¤ì�˜ ì—­í•** ì�„ í•
ìˆ˜ ì�ˆê²Œ í•´ì£¼ëŠ” ì�¥ì¹˜ì�´ë‹¤.

êµ¬í˜„ì�„ ê°–ì§€ëŠ” ëª»í•˜ì§€ë§Œ, ì��ì‹� í�´ë�˜ìŠ¤ì—�ì„œ ë°˜ë“œì‹œ
êµ¬í˜„í•˜ë�„ë¡� ê°•ì œ  í•œë‹¤.

ì��ì‹� í�´ë�˜ìŠ¤ë“¤ì�€ ë°˜ë“œì‹œ ì�´ ì¶”ìƒ� ë©”ì†Œë“œë“¤ì�„ ê°€ì§€ê³
êµ¬í˜„í•´ë†¨ì�„ ê±°ë�¼ëŠ” ì�¼ì¢…ì�˜ ì•½ì†�ì�¸ ì…ˆì�´ë‹¤.

####  **ì¶”ìƒ� ë©”ì†Œë“œì�˜ ê¸°ë³¸ ì ‘ê·¼ì„±ì�€ ë¬´ì—‡ì�¼ê¹Œ?**

    
    
    abstract class AbstractClass
    {
        abstract void AbstractMethod();   // public? private?

**ì¶”ìƒ� í�´ë�˜ìŠ¤** ë‚˜ **í�´ë�˜ìŠ¤** ëŠ” ê·¸ ì•ˆì—�ì„œ ì„ ì–¸ë�˜ëŠ” ëª¨ë“
**í•„ë“œ** , **ë©”ì†Œë“œ** , **í”„ë¡œí�¼í‹°** , **ì�´ë²¤íŠ¸** ëª¨ë‘� ì ‘ê·¼
í•œì •ì��ë¥¼ ëª…ì‹œí•˜ì§€ ì•Šìœ¼ë©´  **private** ìœ¼ë¡œ ê°„ì£¼í•œë‹¤.
ì—¬ê¸°ì—� ì¶”ìƒ� ë©”ì†Œë“œ ë˜�í•œ ì˜ˆì™¸ê°€ ë� ìˆ˜ëŠ” ì—†ë‹¤.

í•˜ì§€ë§Œ **ì•½ì†�** ì—­í• ì�„ í•˜ëŠ” ì¶”ìƒ� ë©”ì†Œë“œê°€  private  ì�´ë�¼ëŠ”
ê²ƒì�´ ë§�ì�´ ì•ˆ ë�œë‹¤.

ê·¸ë�˜ì„œ  C# ì»´íŒŒì�¼ëŸ¬ëŠ” ì¶”ìƒ� ë©”ì†Œë“œê°€ ë°˜ë“œì‹œ **public** ,
**protected** , **internal** , **protected internal** í•œì •ì�� ì¤‘ í•˜ë‚˜ë¡œ
ìˆ˜ì‹�ë� ê²ƒì�„ ê°•ìš”í•œë‹¤.

####  **ì¶”ìƒ� í�´ë�˜ìŠ¤ê°€ ë˜� ë‹¤ë¥¸ ì¶”ìƒ� í�´ë�˜ìŠ¤ë¥¼ ìƒ�ì†�í•˜ëŠ”
ê²½ìš°**

ì¶”ìƒ� í�´ë�˜ìŠ¤ëŠ” ë˜� ë‹¤ë¥¸ ì¶”ìƒ� í�´ë�˜ìŠ¤ë¥¼ ìƒ�ì†�í• ìˆ˜ ì�ˆìœ¼ë©°, ì�´
ê²½ìš° ì��ì‹� ì¶”ìƒ� í�´ë�˜ìŠ¤ëŠ” ë¶€ëª¨ ì¶”ìƒ� í�´ë�˜ìŠ¤ì�˜ ì¶”ìƒ�
ë©”ì†Œë“œë¥¼ êµ¬í˜„í•˜ì§€ ì•Šì•„ë�„ ë�œë‹¤. ì¶”ìƒ� ë©”ì†Œë“œëŠ”
ì�¸ìŠ¤í„´ìŠ¤ë¥¼ ìƒ�ì„±í• í�´ë�˜ìŠ¤ì—�ì„œ êµ¬í˜„í•˜ë©´ ë�˜ê¸° ë•Œë¬¸ì�´ë‹¤.

###  **"ê·¸ë�˜ì„œ, ì¶”ìƒ� í�´ë�˜ìŠ¤ëŠ” ì™œ ì‚¬ìš©í•˜ëŠ”ê±´ë�°?"**

ì¶”ìƒ� í�´ë�˜ìŠ¤ë¥¼ ì‚¬ìš©í•˜ì§€ ì•Šìœ¼ë©´ ì–´ë–¤ ì�¼ì�´ ë°œìƒ�í• ê¹Œ? ë§Œì•½
íŒ€ë�¼ë¦¬ ì�¼ì�„ í•˜ëŠ”ë�°, ë‹¤ì�Œê³¼ ê°™ì�€ ë§�ì�„ ë“¤ì—ˆë‹¤ê³ ìƒ�ê°�
í•´ë³´ì��.

> **"ì�´ í�´ë�˜ìŠ¤ëŠ” ì§�ì ‘ ì�¸ìŠ¤í„´ìŠ¤í™”í•˜ì§€ ë§�ê³ ì��ì‹� í�´ë�˜ìŠ¤ë¥¼
> ë§Œë“¤ì–´ ì‚¬ìš©í•˜ì„¸ìš”.  
>  Method1()ê³¼ Method2()ëŠ” ê¼­ ì˜¤ë²„ë�¼ì�´ë”© í•´ì•¼ í•©ë‹ˆë‹¤." **  
>  
>

í”„ë¡œê·¸ë�˜ë¨¸ë�„ ì‚¬ë�Œì�´ê¸° ë•Œë¬¸ì—� ì•„ë¬´ë¦¬ ì�´ëŸ° ì¢‹ì�€ ë©”ë‰´ì–¼ì�´
ì�ˆë‹¤ê³ í•˜ë�”ë�¼ë�„, ì�¼ì�´ ë§�ë‹¤ë³´ë©´ ê¹Œë¨¹ì�„ ìˆ˜ë�„ ì�ˆë‹¤.

**ì¶”ìƒ� í�´ë�˜ìŠ¤ë¥¼ ì‚¬ìš©í•˜ë©´ ì�´ëŸ° ë¬¸ì œê°€ ë°œìƒ�í• ì�¼ì�´
ì—†ì–´ì§„ë‹¤.**

ì»´íŒŒì�¼ëŸ¬ê°€ ì˜¤ë²„ë�¼ì�´ë”©ì�„ ê°•ì œí•˜ë�„ë¡� ìš”êµ¬í•˜ê³ , ì•ˆ í•˜ë©´
ì»´íŒŒì�¼ ì˜¤ë¥˜ë¥¼ ë°œìƒ�ì‹œí‚¤ê¸° ë•Œë¬¸ì�´ë‹¤.

ì�´ê²ƒì�´ ì¶”ìƒ� í�´ë�˜ìŠ¤ë¥¼ ì‚¬ìš©í•˜ëŠ” ì�´ìœ ë‹¤.

  * ì�´ ê¸€ì�€ < **ì�´ê²ƒì�´ C#ì�´ë‹¤** > ì±…ì�„ ë°”íƒ•ìœ¼ë¡œ ê³µë¶€í•œ ê¸€ì�…ë‹ˆë‹¤. 


-->

<!--






-->

<!--
**인터페이스 interface**

OOP에서 객체들의 공통적인 행동에 대한 명세를 규정하고 이를 상속(구현)하는 클래스는 인터페이스를 구현하도록 한다.

    
    
    public interface INetwork
    {
        public void Send();
    }

INetwork라는 인터페이스는 Send()라는 함수적 기능만 있을 뿐이다. INetwork를 구현하는 구현체는 이제 Send() 함수
기능을 가지는 클래스라고 할 수 있다.

    
    
    public partial class IPv4Network : INetwork
    {
        public void Send()
        {
            Console.WriteLine($"{nameof(IPv4Network)}");
        }
    }
    
    public partial class IPv6Network : INetwork
    {
        public void Send()
        {
            Console.WriteLine($"{nameof(IPv6Network)}");
        }
    }

이를 구현한 다양한 구현체 클래스를 작성할 수 있다.

    
    
    var ipv4 = new IPv4Network();
    var ipv6 = new IPv6Network();
    
    ipv4.Send(); // "IPv4Network"
    ipv6.Send(); // "IPv6Network"

구현체의 함수를 호출하면 var가 실제로 해석된 클래스의 Send() 메서드를 찾아서 호출하게 된다. **이 과정은 정적으로 이루어지며 이미
해당 클래스가 INetwork를 직접 구현한 경우 컴파일 에러 없이 수행된다.**

    
    
    public partial class IPv4PrivateNetwork : IPv4Network
    {
        public new void Send()
        {
            Console.WriteLine($"{nameof(IPv4PrivateNetwork)}");
        }
    }

만약 구현체를 상속하여 인터페이스로 정의된 함수를 새로 정의하고 싶다면 인터페이스의 메서드는 가상 함수가 아니므로 new 키워드로 상위
클래스의 메서드를 숨김으로써 재정의해야한다.

    
    
    var ipv4p = new IPv4PrivateNetwork();
    ipv4p.Send(); // "Ipv4PrivateNetwork"
    
    var ipv4p_c = ipv4p as IPv4Network;
    ipv4p_c.Send(); // "Ipv4Network"
    
    var ivp4p_i = ipv4p as INetwork;
    ivp4p_i.Send(); // "Ipv4Network"

인터페이스가 추상 클래스와 다른 점은 여기서 볼 수 있는데, _ IPv4PrivateNetwork  _ 타입의  **ipv4p** 인스턴스
는  **정적으로 해석되어 항상 캐스팅된 타입의 메서드를 호출한다.** 이는 인터페이스를 구현한 구현체의 Send() 그리고 new 타입으로
새로 정의된 Send() 모두 정적으로 각각 IPv4Network와 IPv4PrivateNetwork 클래스 타입에 정의되어 있기 때문이다.  
  
**추상 클래스 Abstract**

추상 클래스 뿐만 아니라 하나의 가상 함수를 포함하는 모든 클래스를 가리킨다. 가상 함수를 가지는 객체 타입은 C++의 가상 함수 테이블
처럼 동적으로 객체 타입을 확인하여 override된 메서드를 호출한다.

    
    
    public abstract class EndPoint
    {
        public abstract void Configure();
    }
    
    public partial class IPv4Network : EndPoint
    {
        public override void Configure()
        {
            Console.WriteLine("Configuration Ipv4 ...");
        }
    }
    
    public partial class IPv4PrivateNetwork : IPv4Network
    {
        public override void Configure()
        {
            Console.WriteLine("Configuration Ipv4 as Private ...");
        }
    }

C# partial 기능을 이용하여 EndPoint 라는 추상 클래스를 상속하는 것으로 명세를 추가해본다.

각각 IPv4Network와 IPv4PrivateNetwork는 Configure()라는 메서드를 자신의 기반 클래스의 Configure()
메서드를 override 한다.

    
    
    var ipv4p = new IPv4PrivateNetwork();
    ipv4p.Send(); // "Ipv4PrivateNetwork"
    
    var ipv4p_c = ipv4p as IPv4Network;
    ipv4p_c.Send(); // "Ipv4Network"
    
    var ivp4p_i = ipv4p as INetwork;
    ivp4p_i.Send(); // "Ipv4Network"
    
    ipv4p.Configure(); // "Configuration Ipv4 as Private ..."
    ipv4p_c.Configure(); // "Configuration Ipv4 as Private ..."
    //ivp4p_i.Configure(); // "Configuration Ipv4 as Private ..."

이제 **Ipv4p** 인스턴스는 _IPv4PrivateNetwork_ 의 인스턴스로써 Configure()를 호출하면  **동적으로 객체
타입을 확인** 하여 override된 메서드를 호출하게 된다.

_마지막 메서드는 iv4p_i가 같은 인스턴스를 지칭하지만 INetwork 인터페이스로 해석되기 때문에 해당 메서드 정의가 없으므로 컴파일
에러가 발생한다._

    
    
    public interface INetwork
    {
        public void Send();
    
        public abstract void Configure();
    }

이렇게 사용하는 경우는 거의 없지만 C#은 고급 언어으로써 모든 메서드, 속성 마다 접근자와 virtual/abstract와 같은 상속
특성을 추가 할 수 있다.

    
    
    ipv4p.Configure(); // "Configuration Ipv4 as Private ..."
    ipv4p_c.Configure(); // "Configuration Ipv4 as Private ..."
    ivp4p_i.Configure(); // "Configuration Ipv4 as Private ..."

마지막 문장은 이제 오류없이 컴파일된다.  
  
**결론**

**인터페이스의 메서드는 정적으로 해석된 타입의 메서드를 호출하게 되며 보통 인터페이스를 직접 구현한 메서드를 가리킨다.** 인터페이스의
메서드를 상속된 클래스에서 재정의하려면 new를 사용해야한다. new를 사용했더하더라도 상속된 클래스의 인스턴스가 인터페이스로 캐스팅되어
메서드를 호출하면 정적으로 확인된 기반 클래스가 직접 구현한 인터페이스 메서드를 호출하게 된다.

**추상/가상 메서드는 항상 동적으로 타입을 확인하여 실제 타입에서 override된 메서드를 호출한다.** 인스턴스는  C#  가상 함수
테이블을 자신의 메모리에 가지고 있다.

  
_**용법** _

\- 인터페이스

인터페이스의 경우 상속보다는 여러 객체의 공통적인 기능을 묶는 기능을 정의한다. 인터페이스 구현체가 구현하는 경우외에 구현체를 상속하는
클래스에서 인터페이스 메서드를 재정의하는 경우는 인터페이스에 추상 함수로 정의하거나 new로 숨겨야하는 지 혹은 인터페이스가 아니라 추상
클래스로 정의해야 할 지 고려해야한다.

\- 추상/가상 함수

여러 계층의 클래스에 대한 정의를 해야하고 파생 클래스에서 override한 경우 기반 클래스의 기존 기능이 필요하여 base.Call()를
사용해야하거나 혹은 반드시 동적으로 타입에 따라 결정되어야하는 메서드인 경우 추상/가상 함수로 정의하도록 한다.


-->

<!--






-->

<!--
##  Virtual

  * virtual은  재정의(override)가 선택사항이다. 
  * virtual 키워드가 포함된 클래스는 인스턴스화가 가능하다. 
  * 상속할 때 어떻게 할 것인지의 문제와 결부되어 있으므로 상속을 염두에 둔 클래스에 적용한다. 
  * 일반 메소드는 new를 통해 재정의할 수 있지만 부모 클래스를 기반으로 자식을 인스턴스화하면 부모 메소드가 나온다. 
  * 일반 메소드와 달리 override를 통해 재정의하면 부모 클래스를 기반으로 자식을 인스턴스화하더라도 제대로 자식 메소드가 나온다. 

**버추얼 메소드와 일반 메소드의 상속 차이**

    
    
    // Online C# Editor for free
    // Write, Edit and Run your C# code using C# Online Compiler
    
    using System;
    
    public class HelloWorld
    {
        class A {
            public A(){}
            
            public void NormalMethod(){
                Console.WriteLine (" 부모의 보통 메소드");
            }
            
            public virtual void VirtualMethod(){
                Console.WriteLine (" 부모의 버추얼 메소드");
            }
        }
        
        class B : A {
            public B(){}
            
            new public void NormalMethod(){
                Console.WriteLine (" 자식의 재정의한 보통 메소드");
            }
            
            public override void VirtualMethod(){
                Console.WriteLine (" 자식의 오버라이드한 버추얼 메소드");
            }
        }
        
        
        public static void Main(string[] args)
        {
            Console.WriteLine("B b");
            B bb = new B();
            bb.NormalMethod();
            bb.VirtualMethod();
            
            // ---------------
            
            Console.WriteLine("A a");
            A a = new A();
            a.NormalMethod();
            a.VirtualMethod();
            
            // ---------------
            
            Console.WriteLine("A <- b");
            A abb = bb;
            abb.NormalMethod();
            abb.VirtualMethod();
            
            // ---------------
            
            Console.WriteLine("A b");
            A ab = new B();
            ab.NormalMethod();
            ab.VirtualMethod();
            
            // 에러 : An explicit conversion exists (are you missing a cast?)
            // B ba = new A();
            // ba.NormalMethod();
            // ba.VirtualMethod();
        }
    }

![https://blog.kakaocdn.net/dn/bpnPpn/btrLgaPU4Mz/PuHAQY2OGmQAV8GDFdtEP0/img.png](https://blog.kakaocdn.net/dn/bpnPpn/btrLgaPU4Mz/PuHAQY2OGmQAV8GDFdtEP0/img.png)
결과 화면

##  Abstract

  * abstract는 자식 클래스에서 반드시 재정의해야 한다. 
  * 필드 혹은 메소드에 abstract를 사용하려면 클래스도 abstract여야 한다. 
  * abstract 클래스라고 해서 구성요소까지 모두 abstract여야만 하는 것은 아니다. 
  * abstract 클래스는 인스턴스화할 수 없다. 

##  interface

  * abstract와 달리  interface는 다중 상속  이 가능하다. 
  * abstract가 아닌 필드는 정의할 수 없다. 
  * 정의만 있고 구현 내용이 없다. 
  * 접근 제한자를 사용할 수 없으며 모든 필드는 public이 적용된다. 
  * interface는 상속의 개념이 아니라 기능을 탑재하는 개념이다. Has-A not Is-A. 


-->

<!--






-->

