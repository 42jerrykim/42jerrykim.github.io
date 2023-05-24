---
title: "Abstract Factory"
last_modified_at: 2023-01-12
date: 2022-01-01
header:
  teaser: /plantuml/abstract_factory.svg
---

추상 팩토리 패턴은 여러개의 개별적인 팩토리를 캡슐화하는 방법을 제공한다. 각각의 팩토리는 구현 클래스(Concrete Class) 없이 공통의 기능을 가지고 있어야 한다. 보통의 경우에는 클라이언트 프로그램에서 추상 팩토리에 대한 구현체(Concrete Implementation)를 생성하고 팩토리의 제너릭 인터페이스를 사용하여 구현체를 사용한다. 클라이언트는 결과물(Product)의 제너릭 인터페이스(Generic Interfaces)만 사용하기 때문에 팩토리 내부에서 어떤 객체(Concrete Objects)가 반환되는지 모른다. 팩토리에서 객체를 생성하는 메소드를 인터페이스로 노출하기 때문에 추상 팩토리 패턴은 객체가 어떻게 구현되어 있는지와 객체를 사용하는 일반적인 방법을 분리 할 수 있다. 그리고 추상 팩토리 패턴은 객체 합성(Object Composition)에 의존한다.

# 개요

|![](/plantuml/abstract_factory.svg)|
|:---:|
|클래스 다이어그램|

추상 팩토리 패턴은 잘 알려진 23개의 패턴중에서 아래와 같은 상황에서 사용할 수 있는 패턴이다.

* 어플리케이션과 객체를 어떤식으로 생성하는지 독립적으로 처리해야 할때
* 클래스와 객체를 생성할때 필요한것들과 분리 시키고 싶을때
* 관련되거나 의존하는 객체를 한번에 생성하고 싶을때

클래스 내부에서 객체를 직접 생성하는것은 유연성을 가지기 어렵다. 이유는 클래스와 특정 객체에 대한 코드를 작성하고 나면 클래스를 바꾸지 않고서는 객체를 생성하는 부분을 수정할 수 없기 때문이다. 또한 다른 객체를 사용해야 하는 추가적인 요구사항을 수용하기 어렵게 만든다. 그리고 실제 객체를 Mock 객체로 대체 할 수 없기 때문에 클래스만 테스트하기 어렵다. 

추상 팩토리 패턴은 아래와 같은 문제점을 해결하는데 도움이 된다.

* 객체를 생성하는 인터페이스를 정의하고 구현하는것을 분리된 팩토리에서 처리하는것으로 객체 생성을 캡슐화한다.
* 객체를 직접 생성하는 대신에 팩토리에서 생성할 수 있도록 객체 생성을 위임한다.

# 정의

추상 팩토리 패턴은 객체에 대한 구현 클래스 없이, 관련되거나 의존성이 있는 객체들을 생성하는 인터페이스다.

# 사용법

# 구조

# 예시

```csharp
using System;

namespace RefactoringGuru.DesignPatterns.AbstractFactory.Conceptual
{
    // The Abstract Factory interface declares a set of methods that return
    // different abstract products. These products are called a family and are
    // related by a high-level theme or concept. Products of one family are
    // usually able to collaborate among themselves. A family of products may
    // have several variants, but the products of one variant are incompatible
    // with products of another.
    public interface IAbstractFactory
    {
        IAbstractProductA CreateProductA();

        IAbstractProductB CreateProductB();
    }

    // Concrete Factories produce a family of products that belong to a single
    // variant. The factory guarantees that resulting products are compatible.
    // Note that signatures of the Concrete Factory's methods return an abstract
    // product, while inside the method a concrete product is instantiated.
    class ConcreteFactory1 : IAbstractFactory
    {
        public IAbstractProductA CreateProductA()
        {
            return new ConcreteProductA1();
        }

        public IAbstractProductB CreateProductB()
        {
            return new ConcreteProductB1();
        }
    }

    // Each Concrete Factory has a corresponding product variant.
    class ConcreteFactory2 : IAbstractFactory
    {
        public IAbstractProductA CreateProductA()
        {
            return new ConcreteProductA2();
        }

        public IAbstractProductB CreateProductB()
        {
            return new ConcreteProductB2();
        }
    }

    // Each distinct product of a product family should have a base interface.
    // All variants of the product must implement this interface.
    public interface IAbstractProductA
    {
        string UsefulFunctionA();
    }

    // Concrete Products are created by corresponding Concrete Factories.
    class ConcreteProductA1 : IAbstractProductA
    {
        public string UsefulFunctionA()
        {
            return "The result of the product A1.";
        }
    }

    class ConcreteProductA2 : IAbstractProductA
    {
        public string UsefulFunctionA()
        {
            return "The result of the product A2.";
        }
    }

    // Here's the the base interface of another product. All products can
    // interact with each other, but proper interaction is possible only between
    // products of the same concrete variant.
    public interface IAbstractProductB
    {
        // Product B is able to do its own thing...
        string UsefulFunctionB();

        // ...but it also can collaborate with the ProductA.
        //
        // The Abstract Factory makes sure that all products it creates are of
        // the same variant and thus, compatible.
        string AnotherUsefulFunctionB(IAbstractProductA collaborator);
    }

    // Concrete Products are created by corresponding Concrete Factories.
    class ConcreteProductB1 : IAbstractProductB
    {
        public string UsefulFunctionB()
        {
            return "The result of the product B1.";
        }

        // The variant, Product B1, is only able to work correctly with the
        // variant, Product A1. Nevertheless, it accepts any instance of
        // AbstractProductA as an argument.
        public string AnotherUsefulFunctionB(IAbstractProductA collaborator)
        {
            var result = collaborator.UsefulFunctionA();

            return $"The result of the B1 collaborating with the ({result})";
        }
    }

    class ConcreteProductB2 : IAbstractProductB
    {
        public string UsefulFunctionB()
        {
            return "The result of the product B2.";
        }

       // The variant, Product B2, is only able to work correctly with the
       // variant, Product A2. Nevertheless, it accepts any instance of
       // AbstractProductA as an argument.
        public string AnotherUsefulFunctionB(IAbstractProductA collaborator)
        {
            var result = collaborator.UsefulFunctionA();

            return $"The result of the B2 collaborating with the ({result})";
        }
    }

    // The client code works with factories and products only through abstract
    // types: AbstractFactory and AbstractProduct. This lets you pass any
    // factory or product subclass to the client code without breaking it.
    class Client
    {
        public void Main()
        {
            // The client code can work with any concrete factory class.
            Console.WriteLine("Client: Testing client code with the first factory type...");
            ClientMethod(new ConcreteFactory1());
            Console.WriteLine();

            Console.WriteLine("Client: Testing the same client code with the second factory type...");
            ClientMethod(new ConcreteFactory2());
        }

        public void ClientMethod(IAbstractFactory factory)
        {
            var productA = factory.CreateProductA();
            var productB = factory.CreateProductB();

            Console.WriteLine(productB.UsefulFunctionB());
            Console.WriteLine(productB.AnotherUsefulFunctionB(productA));
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            new Client().Main();
        }
    }
}
```
# 구체적인 구현클래스가 없는 팩토리 예시

아래의 코드에서 WinFactory는 IButton을 반환하는 메소드만 가지고 있기 때문에 구현 클래스(Concrete Classes)가 없다고 말할 수 있다.

```csharp
interface IButton
{
    void Paint();
}

interface IGUIFactory
{
    IButton CreateButton();
}

class WinFactory : IGUIFactory
{
    public IButton CreateButton()
    {
        return new WinButton();
    }
}
```

# 영문 단어 번역 사전

|영문|한글|
|:---|:---|
|Concrete Implementation|구현체|
|Concrete Objects|구현 객체|
|Concrete Classes|구현 클래스|
|Object Composition|객체 합성 (Composition 의 경우 구성으로 번역할지, 합성으로 번역할지 애매하다.)|

# 참고

* [https://en.wikipedia.org/wiki/Abstract_factory_pattern](https://en.wikipedia.org/wiki/Abstract_factory_pattern)
* [객체지향 프로그래밍(OOP) – 2 : Composition and Inheritance](https://actruce.com/copy-object-oriented-programming-2/)
