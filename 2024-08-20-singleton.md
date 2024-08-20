---
title: "[DesignPattern] 싱글턴 패턴"
categories: designpattern
tags:
- Singleton
- DesignPattern
- CreationalPattern
- ObjectOriented
- SoftwareDesign
- GlobalAccess
- ThreadSafety
- LazyInitialization
- EagerInitialization
- DoubleCheckedLocking
- EnumSingleton
- Java
- C++
- Kotlin
- ThreadSafety
- RaceCondition
- DependencyInjection
- UnitTesting
- AntiPattern
- MemoryManagement
- SharedResource
- Initialization
- StaticMethod
- PrivateConstructor
- InstanceVariable
- Synchronization
- HolderPattern
- Reflection
- Serialization
- GlobalState
- Coupling
- OpenClosedPrinciple
- SingleResponsibilityPrinciple
- DesignPrinciples
- SoftwareEngineering
- CodeQuality
- Refactoring
- Performance
- ObjectCreation
- ClassDiagram
- UML
- SoftwareArchitecture
- DesignPatterns
- Programming
- Development
- BestPractices
- CleanCode
- SoftwareDevelopment
header:
teaser: /assets/images/undefined/teaser.jpg
---

싱글턴 패턴은 객체 지향 소프트웨어 개발에서 자주 사용되는 디자인 패턴 중 하나로, 특정 클래스의 인스턴스가 오직 하나만 존재하도록 보장하는 패턴이다. 이 패턴은 전역적으로 접근할 수 있는 인스턴스를 제공하여, 여러 객체가 동일한 인스턴스를 공유할 수 있도록 한다. 싱글턴 패턴은 주로 데이터베이스 연결, 로그 기록, 설정 관리 등과 같이 애플리케이션 전역에서 단일 인스턴스가 필요한 경우에 유용하게 사용된다. 그러나 싱글턴 패턴은 여러 가지 문제점을 동반할 수 있다. 예를 들어, 멀티 스레드 환경에서 인스턴스가 여러 번 생성되는 경합 조건이 발생할 수 있으며, 이는 프로그램의 안정성을 저해할 수 있다. 또한, 싱글턴 패턴은 테스트하기 어려운 구조를 만들어, 의존성 주입과 같은 다른 디자인 원칙을 위반할 수 있다. 따라서 싱글턴 패턴을 사용할 때는 이러한 장단점을 충분히 고려해야 하며, 필요에 따라 대체 디자인 패턴을 검토하는 것이 좋다.

|![](/plantuml/singleton.svg)|
|:---:|
|클래스 다이어그램|

## 싱글턴 패턴 개요

**싱글턴 패턴의 정의**  
싱글턴 패턴은 특정 클래스의 인스턴스가 오직 하나만 존재하도록 보장하는 디자인 패턴이다. 이 패턴은 전역적으로 접근할 수 있는 인스턴스를 제공하여, 애플리케이션 내에서 자원 관리와 데이터 공유를 용이하게 한다.

**싱글턴 패턴의 필요성**  
애플리케이션에서 특정 자원이나 서비스가 단 하나의 인스턴스만 필요할 때 싱글턴 패턴이 유용하다. 예를 들어, 데이터베이스 연결이나 설정 파일 관리와 같은 경우, 여러 인스턴스가 생성되면 자원 낭비와 데이터 불일치가 발생할 수 있다.

**싱글턴 패턴의 역사**  
싱글턴 패턴은 1970년대에 처음 등장하였으며, 이후 다양한 프로그래밍 언어와 환경에서 널리 사용되기 시작했다. 이 패턴은 객체 지향 프로그래밍의 발전과 함께 더욱 중요해졌다.

**싱글턴 패턴의 사용 사례**  
싱글턴 패턴은 다양한 분야에서 사용된다. 예를 들어, 로깅 시스템, 프린터 관리, 설정 관리 등에서 이 패턴을 통해 자원 관리와 데이터 일관성을 유지할 수 있다.

## 싱글턴 패턴의 의도

**클래스 인스턴스의 유일성 보장**  

싱글턴 패턴의 가장 중요한 의도는 특정 클래스의 인스턴스가 오직 하나만 존재하도록 보장하는 것이다. 이는 애플리케이션 내에서 해당 클래스의 인스턴스가 여러 개 생성되는 것을 방지하여, 데이터의 일관성을 유지하고 자원 낭비를 줄이는 데 기여한다. 예를 들어, 데이터베이스 연결을 관리하는 클래스가 여러 개의 인스턴스를 생성하게 되면, 각 인스턴스가 서로 다른 연결을 유지하게 되어 데이터의 충돌이나 불일치가 발생할 수 있다. 따라서 싱글턴 패턴을 통해 이러한 문제를 예방할 수 있다.

**전역 접근 지점 제공**  

싱글턴 패턴은 전역적으로 접근 가능한 인스턴스를 제공한다. 이는 애플리케이션의 어느 곳에서든 해당 인스턴스에 접근할 수 있도록 하여, 코드의 일관성을 높이고 유지보수를 용이하게 한다. 예를 들어, 로깅 시스템을 싱글턴으로 구현하면, 애플리케이션의 모든 모듈에서 동일한 로깅 인스턴스를 사용하게 되어 로그의 통합 관리가 가능해진다. 이러한 전역 접근은 코드의 가독성을 높이고, 개발자가 인스턴스를 관리하는 데 드는 노력을 줄여준다.

**자원 관리의 용이성**  

싱글턴 패턴은 자원 관리의 용이성을 제공한다. 특정 자원, 예를 들어 데이터베이스 연결이나 파일 핸들러와 같은 경우, 여러 인스턴스가 생성되면 자원 낭비가 발생할 수 있다. 싱글턴 패턴을 사용하면 이러한 자원을 중앙에서 관리할 수 있어, 자원의 효율적인 사용이 가능해진다. 또한, 자원의 초기화와 해제를 한 곳에서 관리할 수 있어, 코드의 복잡성을 줄이고 오류 발생 가능성을 낮출 수 있다. 

이러한 이유로 싱글턴 패턴은 다양한 상황에서 유용하게 사용될 수 있으며, 특히 자원 관리가 중요한 애플리케이션에서 그 효과를 극대화할 수 있다.

## 싱글턴 패턴의 문제점

1. **단일 책임 원칙 위반**  

싱글턴 패턴은 클래스가 단 하나의 인스턴스만을 가지도록 강제하는 디자인 패턴이다. 그러나 이로 인해 클래스가 여러 가지 책임을 지게 되는 경우가 많다. 예를 들어, 싱글턴 클래스가 데이터베이스 연결을 관리하면서 동시에 애플리케이션의 상태를 유지하는 역할을 수행할 수 있다. 이러한 경우, 클래스는 단일 책임 원칙(SRP)을 위반하게 되며, 이는 유지보수와 확장성을 저해할 수 있다. 

1. **테스트의 어려움**  

싱글턴 패턴은 테스트를 어렵게 만드는 요소 중 하나이다. 테스트 환경에서는 종종 클래스의 인스턴스를 교체하거나 모의 객체(mock object)를 사용해야 하는데, 싱글턴 패턴은 이러한 작업을 어렵게 만든다. 싱글턴 인스턴스는 애플리케이션의 생명 주기 동안 지속되기 때문에, 테스트가 끝난 후에도 상태가 남아있을 수 있다. 이로 인해 테스트 간의 독립성이 깨질 수 있으며, 이는 테스트의 신뢰성을 떨어뜨린다.

1. **멀티 스레드 환경에서의 문제**  

멀티 스레드 환경에서 싱글턴 패턴을 사용할 경우, 동기화 문제로 인해 여러 스레드가 동시에 인스턴스를 생성할 위험이 있다. 이로 인해 애플리케이션의 상태가 예기치 않게 변할 수 있으며, 이는 데이터 손실이나 충돌을 초래할 수 있다. 따라서 멀티 스레드 환경에서 안전하게 싱글턴을 구현하기 위해서는 추가적인 동기화 메커니즘이 필요하다.

1. **의존성 증가**  

싱글턴 패턴을 사용하면 클래스 간의 의존성이 증가할 수 있다. 싱글턴 인스턴스에 의존하는 클래스가 많아질수록, 해당 인스턴스의 변경이 다른 클래스에 미치는 영향이 커진다. 이는 코드의 결합도를 높이고, 결과적으로 시스템의 복잡성을 증가시킬 수 있다. 따라서 싱글턴 패턴을 사용할 때는 이러한 의존성을 신중하게 관리해야 한다. 

이와 같이 싱글턴 패턴은 여러 가지 문제점을 내포하고 있다. 이러한 문제점을 인식하고 적절한 대안을 마련하는 것이 중요하다.

싱글턴 패턴의 문제점을 해결하는 방법에는 여러 가지가 있다. 각 문제에 대한 해결 방법을 설명하고, 그에 맞는 C# 예제 코드를 제공하겠다.

## 싱글턴 패턴의 해결책

**1. 단일 책임 원칙 위반 해결**

- **문제:** 싱글턴 클래스가 여러 책임을 가지게 되어 단일 책임 원칙(SRP)을 위반한다.  
- **해결 방법:** 책임을 분리하여 각 클래스가 하나의 책임만 가지도록 설계한다. 예를 들어, 데이터베이스 연결을 관리하는 클래스와 애플리케이션 상태를 관리하는 클래스를 분리할 수 있다.

**예제 코드**
```csharp
public class DatabaseConnectionManager
{
    private static DatabaseConnectionManager _instance;
    private static readonly object _lock = new object();

    private DatabaseConnectionManager() 
    {
        // Initialize connection
    }

    public static DatabaseConnectionManager Instance
    {
        get
        {
            lock (_lock)
            {
                if (_instance == null)
                {
                    _instance = new DatabaseConnectionManager();
                }
                return _instance;
            }
        }
    }

    public void Connect()
    {
        // Connection logic
    }
}

public class ApplicationStateManager
{
    private static ApplicationStateManager _instance;
    private static readonly object _lock = new object();

    private ApplicationStateManager() 
    {
        // Initialize state
    }

    public static ApplicationStateManager Instance
    {
        get
        {
            lock (_lock)
            {
                if (_instance == null)
                {
                    _instance = new ApplicationStateManager();
                }
                return _instance;
            }
        }
    }

    public string GetState()
    {
        // Return current state
        return "State";
    }
}
```
이 코드에서는 `DatabaseConnectionManager`와 `ApplicationStateManager` 클래스를 분리하여 각각 데이터베이스 연결 관리와 애플리케이션 상태 관리를 담당하게 했다.

**2. 테스트의 어려움 해결**

- **문제:** 싱글턴 패턴은 테스트 시 객체를 교체하거나 모의 객체를 사용하는 것을 어렵게 만든다.  
- **해결 방법:** 싱글턴 패턴을 사용하더라도 테스트 가능한 구조를 만들기 위해 의존성 주입(Dependency Injection, DI)을 사용할 수 있다.

**예제 코드:**
```csharp
public interface IDatabaseConnectionManager
{
    void Connect();
}

public class DatabaseConnectionManager : IDatabaseConnectionManager
{
    private static DatabaseConnectionManager _instance;
    private static readonly object _lock = new object();

    private DatabaseConnectionManager() { }

    public static DatabaseConnectionManager Instance
    {
        get
        {
            lock (_lock)
            {
                if (_instance == null)
                {
                    _instance = new DatabaseConnectionManager();
                }
                return _instance;
            }
        }
    }

    public void Connect()
    {
        // Connection logic
    }
}

public class Application
{
    private readonly IDatabaseConnectionManager _dbConnectionManager;

    public Application(IDatabaseConnectionManager dbConnectionManager)
    {
        _dbConnectionManager = dbConnectionManager;
    }

    public void Run()
    {
        _dbConnectionManager.Connect();
        // Application logic
    }
}

// 테스트 시 모의 객체를 사용할 수 있음
public class MockDatabaseConnectionManager : IDatabaseConnectionManager
{
    public void Connect()
    {
        // Mock connection logic
    }
}
```
위 코드에서는 `IDatabaseConnectionManager` 인터페이스를 사용하여 실제 `DatabaseConnectionManager` 대신 모의 객체인 `MockDatabaseConnectionManager`를 주입할 수 있도록 했다. 이를 통해 테스트 간의 독립성을 유지할 수 있다.

**3. 멀티 스레드 환경에서의 문제 해결**

- **문제:** 멀티 스레드 환경에서 싱글턴 인스턴스가 여러 번 생성될 수 있는 문제가 발생할 수 있다.  
- **해결 방법:** 싱글턴 인스턴스를 안전하게 생성하기 위해 이중 잠금(Double-Check Locking)이나 정적 초기화자를 사용할 수 있다.

**예제 코드:**
```csharp
public class SafeSingleton
{
    private static SafeSingleton _instance;
    private static readonly object _lock = new object();

    private SafeSingleton() { }

    public static SafeSingleton Instance
    {
        get
        {
            if (_instance == null)
            {
                lock (_lock)
                {
                    if (_instance == null)
                    {
                        _instance = new SafeSingleton();
                    }
                }
            }
            return _instance;
        }
    }
}
```
또는 정적 초기화자를 사용하는 방법도 있다.

```csharp
public class StaticSingleton
{
    private static readonly StaticSingleton _instance = new StaticSingleton();

    static StaticSingleton() { }

    private StaticSingleton() { }

    public static StaticSingleton Instance
    {
        get { return _instance; }
    }
}
```
정적 초기화자를 사용하면 멀티 스레드 환경에서 안전하게 싱글턴을 생성할 수 있다.

**4. 의존성 증가 해결**

- **문제:** 싱글턴 패턴을 사용하면 클래스 간 의존성이 증가하여 결합도가 높아질 수 있다.  
- **해결 방법:** 싱글턴 패턴 대신 의존성 주입(DI)을 활용하여 의존성을 명시적으로 관리하고, 테스트 가능성과 확장성을 개선할 수 있다.

**예제 코드:**
```csharp
public class Service
{
    private readonly IDatabaseConnectionManager _dbConnectionManager;

    public Service(IDatabaseConnectionManager dbConnectionManager)
    {
        _dbConnectionManager = dbConnectionManager;
    }

    public void PerformOperation()
    {
        _dbConnectionManager.Connect();
        // Service logic
    }
}
```
여기서 `Service` 클래스는 `IDatabaseConnectionManager`에 대한 의존성을 주입받아 사용하므로, `Service` 클래스와 데이터베이스 연결 관리 간의 결합도가 낮아진다. 이는 코드의 유지보수성과 확장성을 높인다.

이와 같이, 싱글턴 패턴의 문제점을 해결하기 위해 책임 분리, 의존성 주입, 멀티 스레드 안전성 보장, 그리고 의존성 관리 등의 다양한 방법을 활용할 수 있다. 이러한 접근 방식은 코드의 품질을 높이고, 유지보수와 테스트를 용이하게 만드는 데 도움을 줄 수 있다.

## 싱글턴 패턴의 구현 방법

**Eager Initialization**  

`Eager Initialization`은 싱글톤 인스턴스를 프로그램 시작 시점에 미리 생성하는 방법이다. 이 방식은 가장 간단하고 직관적인 싱글톤 구현 방법 중 하나로, 인스턴스가 필요해지기 전에 미리 생성되므로 초기화 시점에서의 성능이 중요한 애플리케이션에서 적합할 수 있다.

다음은 C#에서 `Eager Initialization`을 사용하여 싱글톤을 구현하는 예제이다:

```csharp
using System;

public class Singleton
{
    // 싱글톤 인스턴스를 클래스 로드 시점에 미리 생성합니다.
    private static readonly Singleton instance = new Singleton();

    // 외부에서는 이 생성자를 사용할 수 없습니다.
    private Singleton()
    {
        // 초기화 코드 작성 (필요한 경우)
        Console.WriteLine("싱글톤 인스턴스 생성됨.");
    }

    // 유일한 싱글톤 인스턴스를 반환합니다.
    public static Singleton Instance
    {
        get
        {
            return instance;
        }
    }

    // 싱글톤 클래스의 메서드 예시
    public void DoSomething()
    {
        Console.WriteLine("싱글톤의 메서드 호출");
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        // Singleton 인스턴스 사용
        Singleton.Instance.DoSomething(); // "싱글톤 인스턴스 생성됨." 과 "싱글톤의 메서드 호출" 출력

        // 동일한 인스턴스 확인
        Singleton anotherInstance = Singleton.Instance;
        Console.WriteLine(object.ReferenceEquals(Singleton.Instance, anotherInstance)); // "True" 출력
    }
}
```

**코드 설명**

1. **Static 변수로 싱글톤 인스턴스 생성**:
   - `static readonly` 키워드를 사용하여 `Singleton` 클래스 로드 시점에 싱글톤 인스턴스를 미리 생성한다. 이 인스턴스는 프로그램이 종료될 때까지 유지된다.

2. **생성자(private)**:
   - `private` 생성자는 외부에서 이 클래스를 인스턴스화할 수 없도록 막아준다. 이를 통해 클래스 외부에서 `new Singleton()`을 호출할 수 없게 된다.

3. **Instance 프로퍼티**:
   - `Instance` 프로퍼티는 이미 생성된 싱글톤 인스턴스를 반환한다. 이때 `Instance`를 호출할 때마다 새로운 객체가 생성되는 것이 아니라, 미리 생성된 동일한 인스턴스를 반환한다.

4. **메인 메서드**:
   - `Program` 클래스의 `Main` 메서드에서 `Singleton.Instance`를 통해 싱글톤 인스턴스를 호출하고, 메서드를 실행한다. 또한 동일한 인스턴스인지 확인하기 위해 `ReferenceEquals`를 사용해 참조를 비교한다.

**장점**

- **간단함**: 코드가 매우 간단하고 직관적이다. 복잡한 동기화나 추가적인 코드 없이도 싱글톤 패턴을 쉽게 구현할 수 있다.
- **스레드 안전성**: 클래스 로드 시점에서 인스턴스가 생성되므로, 멀티스레드 환경에서도 안전하게 사용할 수 있다.
- **예측 가능성**: 인스턴스가 프로그램 시작 시점에 생성되므로, 언제 인스턴스가 생성되는지 명확하게 예측할 수 있다.

**단점**

- **리소스 낭비 가능성**: 인스턴스가 필요하지 않은 경우에도 프로그램 시작 시점에 생성되므로, 불필요한 리소스를 소비할 수 있다. 이는 특히 인스턴스 생성 비용이 크거나, 애플리케이션이 가벼운 경우 문제가 될 수 있다.
- **지연 초기화 불가능**: 인스턴스를 지연 초기화해야 하는 경우, 즉 인스턴스가 필요한 시점에 생성되어야 하는 경우에는 적합하지 않다.

`Eager Initialization`은 간단하고 효과적인 싱글톤 구현 방법이지만, 인스턴스가 반드시 필요하지 않거나 리소스가 중요한 경우에는 `Lazy Initialization` 같은 다른 패턴을 고려하는 것이 좋다.

**Lazy Initialization**  

Lazy Initialization을 사용하여 싱글턴 패턴을 구현하면, 싱글턴 인스턴스가 실제로 필요할 때까지 생성되지 않도록 할 수 있다. 이는 자원을 효율적으로 사용할 수 있게 하며, 초기화 비용이 높은 객체를 지연 생성하는 데 유용하다. C#에서는 `Lazy<T>` 클래스를 사용하여 이를 간단하게 구현할 수 있다.

아래는 Lazy Initialization을 사용한 싱글턴 패턴의 구현 예제이다.

```csharp
public class LazySingleton
{
    // Lazy<T>를 사용하여 싱글턴 인스턴스를 지연 초기화
    private static readonly Lazy<LazySingleton> _instance = new Lazy<LazySingleton>(() => new LazySingleton());

    // 생성자는 private로 설정하여 외부에서 인스턴스를 생성하지 못하게 함
    private LazySingleton()
    {
        // 필요한 초기화 작업을 여기서 수행
    }

    // 싱글턴 인스턴스를 반환하는 정적 프로퍼티
    public static LazySingleton Instance
    {
        get
        {
            return _instance.Value; // .Value를 호출할 때 인스턴스가 초기화됨
        }
    }

    // 예시 메서드
    public void DoSomething()
    {
        Console.WriteLine("Lazy Singleton Instance is working.");
    }
}
```

**이 코드의 동작 방식**

1. **`Lazy<LazySingleton>` 사용:** `Lazy<LazySingleton>`는 `LazySingleton` 인스턴스를 지연 초기화하는 데 사용된다. `Lazy<T>`는 쓰레드 안전성을 기본적으로 제공하므로 멀티 스레드 환경에서도 안전하게 사용할 수 있다.

2. **지연 초기화:** `_instance.Value`가 처음 호출될 때 `LazySingleton` 인스턴스가 생성된다. 그 전까지는 인스턴스가 생성되지 않으므로 자원을 절약할 수 있다.

3. **Thread Safety:** `Lazy<T>`는 기본적으로 쓰레드 안전성을 제공하므로, 멀티 스레드 환경에서도 별도의 동기화 코드를 추가할 필요 없이 안전하게 인스턴스를 생성할 수 있다.

**사용 예제**

```csharp
class Program
{
    static void Main(string[] args)
    {
        // 인스턴스가 처음으로 사용될 때 초기화됨
        LazySingleton.Instance.DoSomething();

        // 동일한 인스턴스를 재사용
        LazySingleton.Instance.DoSomething();
    }
}
```

이 예제에서 `LazySingleton.Instance`가 처음 호출될 때 `LazySingleton`의 인스턴스가 생성되고, 이후로는 동일한 인스턴스가 반환된다. 이렇게 하면 인스턴스 초기화가 지연되며, 필요한 경우에만 인스턴스가 생성되므로 자원을 효율적으로 사용할 수 있다.

**장점**

1. **자원 효율성**
   - Lazy Initialization을 사용하면 객체가 실제로 필요할 때까지 인스턴스를 생성하지 않으므로, 초기화가 불필요한 상황에서 자원을 절약할 수 있다. 특히, 객체의 생성 비용이 높거나 프로그램이 종료될 때까지 인스턴스가 필요하지 않을 가능성이 있는 경우에 매우 유리하다.

2. **멀티 스레드 안전성**
   - C#의 `Lazy<T>` 클래스는 기본적으로 멀티 스레드 환경에서 안전하게 동작하도록 설계되어 있다. 별도의 동기화 코드 없이도 여러 스레드에서 동시에 싱글턴 인스턴스에 접근할 수 있으며, 인스턴스가 중복 생성되는 문제를 방지할 수 있다.

3. **초기화 시점 제어**
   - Lazy Initialization을 사용하면 싱글턴 인스턴스의 초기화 시점을 정확하게 제어할 수 있다. 이로 인해 애플리케이션의 시작 시점에 불필요한 초기화를 방지하고, 필요할 때만 초기화를 수행하여 애플리케이션의 성능을 최적화할 수 있다.

4. **간결한 코드**
   - C#에서 `Lazy<T>`를 사용하면 복잡한 동기화 코드 없이도 쉽게 지연 초기화를 구현할 수 있다. 이는 코드의 간결성과 가독성을 높이는 데 도움이 된다.

**단점**

1. **지연 초기화로 인한 지연**
   - 인스턴스가 필요할 때까지 초기화를 지연하기 때문에, 초기 접근 시 인스턴스 생성으로 인한 지연이 발생할 수 있다. 이로 인해, 인스턴스가 사용되기 전까지 성능이 저하될 수 있다. 특히, 인스턴스가 처음으로 사용되는 시점에서 성능이 중요한 경우에는 문제가 될 수 있다.

2. **메모리 누수 가능성**
   - Lazy Initialization으로 인해 인스턴스가 나중에 생성되므로, 인스턴스가 더 오랫동안 메모리에 남아 있을 가능성이 있다. 이는 메모리 누수의 원인이 될 수 있으며, 메모리 관리가 중요한 애플리케이션에서는 문제가 될 수 있다.

3. **복잡성 증가 가능성**
   - Lazy Initialization을 도입함으로써 코드의 복잡성이 약간 증가할 수 있다. 특히, 다양한 초기화 방식이 혼재된 대규모 시스템에서는 어느 부분에서 지연 초기화를 사용할지 판단하는 것이 어려울 수 있다. 이는 유지보수성과 이해도를 낮출 수 있다.

4. **의도하지 않은 초기화 순서**
   - 경우에 따라 Lazy Initialization으로 인해 예상치 못한 시점에 객체가 초기화될 수 있다. 예를 들어, 객체가 사용되기 전까지 초기화되지 않는다는 특성 때문에, 프로그램의 특정 순서나 상태에서 문제가 발생할 수 있다. 이는 시스템의 복잡성을 증가시키고, 디버깅을 어렵게 만들 수 있다.

Lazy Initialization을 사용한 싱글턴 패턴은 자원 효율성과 멀티 스레드 안전성 측면에서 매우 유용한 방법이다. 특히, 초기화 비용이 높은 객체나 멀티 스레드 환경에서 안전한 싱글턴 패턴이 필요할 때 큰 장점을 제공한다. 그러나 초기화 지연으로 인한 성능 문제, 메모리 관리, 코드 복잡성 등의 단점도 존재하므로, 애플리케이션의 요구사항과 환경에 맞게 신중하게 선택해야 한다.

**Double-Checked Locking**  

`Double-Checked Locking`은 멀티스레드 환경에서 성능을 최적화하면서도 스레드 안전하게 싱글톤 인스턴스를 생성하기 위해 자주 사용되는 패턴이다. 이 패턴은 처음 인스턴스가 생성될 때만 락을 사용하고, 이후에는 락 없이 인스턴스에 접근할 수 있도록 한다.

C#에서 `Double-Checked Locking`을 사용하여 싱글톤을 구현하는 예제는 다음과 같다:

```csharp
using System;

public class Singleton
{
    private static Singleton instance = null;
    private static readonly object lockObject = new object();

    // 외부에서는 이 생성자를 사용할 수 없습니다.
    private Singleton()
    {
        // 초기화 코드 작성 (필요한 경우)
        Console.WriteLine("싱글톤 인스턴스 생성됨.");
    }

    public static Singleton Instance
    {
        get
        {
            // 인스턴스가 이미 생성되었는지 확인합니다 (첫 번째 체크).
            if (instance == null)
            {
                lock (lockObject) // 다른 스레드가 접근하지 못하도록 락을 겁니다.
                {
                    // 인스턴스가 생성되지 않은 경우 다시 한 번 체크합니다 (두 번째 체크).
                    if (instance == null)
                    {
                        instance = new Singleton();
                    }
                }
            }
            return instance;
        }
    }

    // 싱글톤 클래스의 메서드 예시
    public void DoSomething()
    {
        Console.WriteLine("싱글톤의 메서드 호출");
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        // Singleton 인스턴스 사용
        Singleton.Instance.DoSomething(); // "싱글톤 인스턴스 생성됨." 과 "싱글톤의 메서드 호출" 출력

        // 동일한 인스턴스 확인
        Singleton anotherInstance = Singleton.Instance;
        Console.WriteLine(object.ReferenceEquals(Singleton.Instance, anotherInstance)); // "True" 출력
    }
}
```

**코드 설명**

1. **Static 변수와 Lock 객체**:
   - `instance` 변수는 `null`로 초기화되며, 실제로 필요할 때 초기화된다.
   - `lockObject`는 스레드 간의 동기화를 위해 사용되는 객체로, `lock` 문을 사용할 때 이 객체를 통해 락을 건다.

2. **Instance 프로퍼티**:
   - 첫 번째 `if (instance == null)` 체크는 인스턴스가 이미 생성된 경우 불필요한 락을 피하기 위해 존재한다. 이로 인해 성능이 최적화된다.
   - 인스턴스가 `null`인 경우에만 `lock`을 걸고, 다시 한 번 `instance`를 체크한다. 이렇게 이중 체크를 통해 멀티스레드 환경에서도 안전하게 인스턴스를 생성할 수 있다.

3. **메인 메서드**:
   - `Program` 클래스의 `Main` 메서드에서 `Singleton.Instance`를 통해 싱글톤 인스턴스를 호출하고, 메서드를 실행한다. 또한 동일한 인스턴스인지 확인하기 위해 `ReferenceEquals`를 사용해 참조를 비교한다.

**장점**

- **성능 최적화**: 인스턴스가 이미 생성된 경우, 불필요한 락을 걸지 않으므로 성능이 최적화된다.
- **스레드 안전성**: 멀티스레드 환경에서도 안전하게 싱글톤 인스턴스를 생성할 수 있다.

**단점**

- **복잡성 증가**: 코드가 단순한 싱글톤 구현 방식보다 복잡하다. 이는 가독성을 떨어뜨릴 수 있다.
- **메모리 장벽 문제**: 이 패턴은 C#에서는 잘 작동하지만, 다른 언어에서는 메모리 장벽 문제로 인해 완벽하게 안전하지 않을 수 있다. 다행히 C#에서는 CLR이 메모리 장벽을 관리하기 때문에 문제가 발생하지 않는다.

이 방법은 `Lazy<T>`나 `Initialization-on-demand Holder` 패턴을 사용할 수 없는 경우에 유용할 수 있으며, 특히 성능 최적화가 중요한 경우에 적합하다. C#에서는 `Lazy<T>`를 사용하는 것이 더 간단하고 직관적인 방법일 수 있지만, `Double-Checked Locking`을 이해하고 있는 것이 좋다.

**Initialization-on-demand Holder Pattern**  

`Initialization-on-demand Holder Idiom`은 지연 초기화를 통해 싱글톤을 안전하게 생성하는 패턴 중 하나이다. 이 패턴은 클래스 로딩 시점의 특성을 이용해, 객체를 필요할 때만 초기화하여 성능과 스레드 안전성을 동시에 보장한다.

C#에서 `Initialization-on-demand Holder Idiom` 패턴을 사용하여 싱글톤을 구현하는 예제는 다음과 같다.

```csharp
using System;

public class Singleton
{
    // 내부 정적 클래스는 Singleton 클래스가 처음 사용될 때 로드됩니다.
    private class SingletonHolder
    {
        // 정적 생성자에서 Singleton 인스턴스를 초기화합니다.
        internal static readonly Singleton instance = new Singleton();
    }

    // 외부에서는 이 생성자를 사용할 수 없습니다.
    private Singleton()
    {
        // 초기화 코드 작성 (필요한 경우)
        Console.WriteLine("싱글톤 인스턴스 생성됨.");
    }

    // 유일한 싱글톤 인스턴스를 반환합니다.
    public static Singleton Instance
    {
        get
        {
            return SingletonHolder.instance;
        }
    }

    // 싱글톤 클래스의 메서드 예시
    public void DoSomething()
    {
        Console.WriteLine("싱글톤의 메서드 호출");
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        // Singleton 인스턴스 사용
        Singleton.Instance.DoSomething(); // "싱글톤 인스턴스 생성됨." 과 "싱글톤의 메서드 호출" 출력

        // 동일한 인스턴스 확인
        Singleton anotherInstance = Singleton.Instance;
        Console.WriteLine(object.ReferenceEquals(Singleton.Instance, anotherInstance)); // "True" 출력
    }
}
```

**코드 설명**

1. **Singleton Class**:
   - `Singleton` 클래스의 생성자는 `private`으로 설정하여 외부에서 인스턴스를 생성하지 못하도록 했다.
   - 내부 정적 클래스 `SingletonHolder`는 `Singleton` 클래스가 처음 사용될 때 로드된다. 이 내부 클래스는 정적 생성자를 통해 싱글톤 인스턴스를 초기화한다.

2. **SingletonHolder Class**:
   - `SingletonHolder` 클래스는 `Singleton` 클래스가 처음 사용될 때(예: `Instance` 프로퍼티가 처음으로 호출될 때) 로드된다.
   - C#에서는 클래스 로더가 클래스의 정적 필드를 초기화할 때 스레드 안전성을 보장하므로, 이 방법은 멀티스레드 환경에서도 안전하다.

3. **Instance Property**:
   - `Instance` 프로퍼티는 `SingletonHolder` 클래스의 `instance` 필드를 반환한다. 이때 `Singleton` 인스턴스는 클래스가 처음 호출되는 시점에만 초기화된다.

4. **Main Method**:
   - `Program` 클래스의 `Main` 메서드에서는 `Singleton.Instance`를 통해 싱글톤 인스턴스를 호출하고, 메서드를 실행한다. 또한, 동일한 인스턴스를 반환하는지 확인하기 위해 `ReferenceEquals`를 사용해 참조를 비교한다.

**장점**

- **지연 초기화**: 필요할 때까지 객체가 생성되지 않으므로 자원을 효율적으로 사용할 수 있다.
- **스레드 안전성**: 클래스 초기화 시점에서 스레드 안전성을 보장한다.
- **단순함**: 코드가 간결하며, 싱글톤 패턴의 의도를 명확하게 드러낸다.


**단점**

`Initialization-on-demand Holder Idiom`은 C#에서 싱글톤 패턴을 구현하는 데 있어 여러 장점이 있지만, 몇 가지 단점도 존재할 수 있다. 이러한 단점은 특정 상황에서 문제를 일으킬 수 있으므로 고려해야 한다.

1. **지연 초기화로 인한 지연된 예외 처리**:
   - 싱글톤 인스턴스가 처음 접근되는 시점에서 초기화되기 때문에, 초기화 중 발생하는 예외가 프로그램의 시작 시점이 아닌, 처음으로 인스턴스를 요청할 때 발생할 수 있다. 이로 인해 예외가 예상치 못한 시점에 발생하여 디버깅이 어려워질 수 있다.

2. **복잡한 초기화 로직**:
   - 싱글톤 인스턴스의 초기화 과정이 복잡하거나, 의존성이 많은 경우에는 이러한 초기화 로직이 내부 정적 클래스에서 처리되기 어려울 수 있다. 초기화가 복잡하면 코드 가독성이 떨어지고, 관리가 어려워질 수 있다.

3. **의도하지 않은 초기화 순서**:
   - 클래스가 의도치 않게 로드되거나 초기화되는 경우가 발생할 수 있다. 예를 들어, `Instance` 프로퍼티가 아니라 다른 정적 멤버나 메서드가 먼저 호출되는 경우, 싱글톤 인스턴스가 예상보다 늦게 초기화되거나 다른 순서로 초기화될 수 있다. 이는 초기화 순서에 민감한 프로그램에서는 문제를 일으킬 수 있다.

4. **사용자의 클래스 설계 의도에 혼란**:
   - 내부 클래스를 사용하여 싱글톤을 구현하는 방식은 일반적인 싱글톤 패턴 구현 방식보다 덜 직관적일 수 있다. 특히, 이 패턴에 익숙하지 않은 개발자에게는 코드가 왜 이렇게 작성되었는지 이해하는 데 시간이 걸릴 수 있다. 이는 코드 유지보수성에 부정적인 영향을 미칠 수 있다.

5. **직렬화에 대한 고려 필요**:
   - 만약 싱글톤 인스턴스를 직렬화해야 하는 경우, 이 패턴을 사용할 때 추가적인 처리(예: `ISerializable` 인터페이스 구현과 `readResolve` 메서드의 사용)를 해야 할 수 있다. 직렬화와 역직렬화 과정에서 싱글톤이 깨질 위험이 있다.

6. **일부 상황에서 불필요한 복잡성**:
   - 이 패턴은 간단한 싱글톤을 구현할 때 불필요하게 복잡할 수 있다. 만약 싱글톤 초기화가 매우 간단하고 지연 초기화가 필요하지 않다면, 이 패턴은 단순한 `Lazy<T>`를 사용하는 것보다 복잡해질 수 있다.

이러한 단점들은 특정 상황에서 문제를 일으킬 수 있으므로, 싱글톤 패턴을 적용할 때는 항상 패턴의 장단점을 고려하여 선택하는 것이 중요하다. 프로그램의 요구사항과 상황에 맞게 가장 적합한 방법을 사용하는 것이 바람직하다.


이 패턴은 특히 싱글톤 인스턴스가 무겁고, 애플리케이션 전반에서 적절한 시점에 생성되어야 할 때 유용하다. C#의 정적 클래스 초기화 메커니즘을 활용하여 손쉽게 싱글톤 패턴을 구현할 수 있는 좋은 방법 중 하나이다.

**Enum을 이용한 싱글턴**  

C#에서 싱글톤 패턴을 구현하는 데 있어서 `enum`을 사용하는 것은 약간 특이한 접근 방법이다. 하지만 가능하다. 일반적으로, 싱글톤 패턴은 클래스 자체가 하나의 인스턴스만을 가지도록 보장하는 패턴이다. `enum`은 C#에서 상수 값들을 그룹화하는 데 주로 사용되지만, 각 열거형 값은 사실상 클래스의 정적 인스턴스와 비슷한 역할을 할 수 있다.

다음은 `enum`을 사용하여 싱글톤 패턴을 구현하는 예제이다.

```csharp
using System;

public enum Singleton
{
    Instance;

    private int someValue;

    // 생성자처럼 동작하는 정적 초기화 블록
    static Singleton()
    {
        Instance.someValue = 42; // 예제 값 초기화
    }

    public void DoSomething()
    {
        Console.WriteLine("싱글톤의 메서드 호출: " + someValue);
    }

    public int GetValue()
    {
        return someValue;
    }

    public void SetValue(int newValue)
    {
        someValue = newValue;
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        Singleton.Instance.DoSomething(); // "싱글톤의 메서드 호출: 42" 출력

        Singleton.Instance.SetValue(100);
        Console.WriteLine(Singleton.Instance.GetValue()); // "100" 출력
    }
}
```

**코드 설명**

1. **Singleton Enum**:
   - `enum Singleton`을 정의하고, 하나의 열거형 값 `Instance`를 선언했다. 이 `Instance`는 이 열거형의 유일한 값이며, 이것이 곧 싱글톤 인스턴스로 작동한다.
   - C#에서 `enum`은 기본적으로 `System.Enum`을 상속받고, `sealed` 클래스로 작동한다. 그래서 `enum` 자체는 상속되거나 확장될 수 없다. 이는 싱글톤 패턴의 특성과 잘 맞는다.

2. **정적 초기화 블록**:
   - `enum` 내부에서 정적 초기화 블록을 사용해 초기화 작업을 수행할 수 있다. 여기서는 `someValue`라는 필드를 초기화했다.
   
3. **싱글톤 기능**:
   - `DoSomething`, `GetValue`, `SetValue`와 같은 메서드를 통해 싱글톤 인스턴스의 동작을 정의했다. 이러한 메서드는 언제나 `Singleton.Instance`를 통해 접근 가능하다.

4. **메인 메서드**:
   - `Program` 클래스의 `Main` 메서드에서 `Singleton.Instance`를 사용해 메서드를 호출하고, 값을 설정하고 가져오는 등의 작업을 수행했다.

**장점과 단점**

- **장점**: 
  - `enum`을 사용하면 싱글톤 인스턴스가 자동으로 초기화되며, 멀티스레딩 환경에서도 안전하다.
  
- **단점**: 
  - `enum`은 본래 싱글톤 패턴을 구현하기 위한 것이 아니므로, 이런 방법은 직관적이지 않으며 일반적인 싱글톤 패턴보다 가독성이 떨어질 수 있다.

이 방식은 싱글톤 패턴의 변형된 구현 방법 중 하나로, 일반적인 방식으로는 많이 사용되지 않으나, C#의 다양한 기능을 활용해 독특한 방식으로 싱글톤을 구현할 수 있다는 점에서 흥미롭다.

## 실제 상황 적용

**프린터 관리자 예시**  
프린터 관리자는 여러 사용자가 동시에 프린터를 사용할 수 있도록 관리하는 시스템이다. 이 시스템에서 싱글턴 패턴을 적용하면, 모든 사용자가 동일한 프린터 인스턴스를 공유하게 된다. 이를 통해 프린터의 상태를 중앙에서 관리할 수 있으며, 자원 낭비를 줄일 수 있다.

```csharp
public class PrinterManager
{
    private static PrinterManager instance;

    private PrinterManager() { }

    public static PrinterManager Instance
    {
        get
        {
            if (instance == null)
            {
                instance = new PrinterManager();
            }
            return instance;
        }
    }

    public void Print(string document)
    {
        // 인쇄 로직
    }
}

```

**데이터베이스 연결 예시**  
데이터베이스 연결을 관리하는 클래스에서도 싱글턴 패턴을 활용할 수 있다. 데이터베이스 연결은 자원 소모가 크기 때문에, 여러 개의 인스턴스를 생성하는 것은 비효율적이다.

```csharp
public class DatabaseConnection
{
    private static DatabaseConnection instance;

    private DatabaseConnection() { }

    public static DatabaseConnection Instance
    {
        get
        {
            if (instance == null)
            {
                instance = new DatabaseConnection();
            }
            return instance;
        }
    }

    public void Query(string sql)
    {
        // 쿼리 실행 로직
    }
}

```

**로깅 시스템 예시**  
로깅 시스템에서도 싱글턴 패턴이 유용하게 사용된다. 애플리케이션의 여러 부분에서 로그를 기록할 때, 동일한 로깅 인스턴스를 사용하면 로그의 일관성을 유지할 수 있다.

```csharp
public class Logger
{
    private static Logger instance;

    private Logger() { }

    public static Logger Instance
    {
        get
        {
            if (instance == null)
            {
                instance = new Logger();
            }
            return instance;
        }
    }

    public void Log(string message)
    {
        // 로그 기록 로직
    }
}

```

## 싱글턴 패턴의 장단점

**장점**

1. **메모리 절약**  
   싱글턴 패턴을 사용하면 클래스의 인스턴스가 오직 하나만 생성되므로, 메모리 사용을 최적화할 수 있다.

2. **데이터 공유 용이**  
   하나의 인스턴스를 모든 클라이언트가 공유하게 되므로, 동일한 데이터나 설정을 여러 부분에서 사용해야 할 때 유리하다.

3. **전역 접근 가능**  
   싱글턴 객체는 애플리케이션 어디에서나 접근할 수 있는 전역적인 접근점을 제공한다. 이는 코드의 다른 부분에서 해당 객체를 재사용할 수 있게 해주며, 필요한 기능이나 데이터를 쉽게 호출할 수 있도록 한다.

**단점**

1. **단일 책임 원칙 위반**  
   싱글턴 패턴은 클래스가 여러 가지 책임을 지게 되어 단일 책임 원칙(SRP)을 위반할 수 있으며, 이는 유지보수와 확장성을 저해할 수 있다.

2. **테스트의 어려움**  
   싱글턴 인스턴스는 전역적으로 사용되기 때문에, 테스트가 끝난 후에도 상태가 남아있을 수 있어 테스트 간의 독립성이 깨질 수 있다.

3. **멀티 스레드 환경에서의 문제**  
   멀티 스레드 환경에서 싱글턴 패턴을 사용할 경우, 동기화 문제로 인해 여러 스레드가 동시에 인스턴스를 생성할 위험이 있다.

4. **의존성 증가**  
   싱글턴 패턴을 사용하면 클래스 간의 의존성이 증가할 수 있어, 코드의 결합도를 높이고 시스템의 복잡성을 증가시킬 수 있다.

## 관련 기술

**전역 변수와의 비교**  
전역 변수는 프로그램의 모든 부분에서 접근할 수 있는 변수이다. 이는 간편하게 데이터를 공유할 수 있는 장점이 있지만, 전역 변수의 사용은 코드의 가독성을 떨어뜨리고, 예기치 않은 부작용을 초래할 수 있다. 반면, 싱글턴 패턴은 클래스의 인스턴스를 하나만 생성하여 전역적으로 접근할 수 있도록 하여, 전역 변수의 단점을 보완한다.

**팩토리 패턴과의 관계**  
팩토리 패턴은 객체 생성의 책임을 별도의 팩토리 클래스에 위임하는 디자인 패턴이다. 싱글턴 패턴과 팩토리 패턴은 객체 생성과 관련이 있지만, 그 목적은 다르다. 싱글턴 패턴은 인스턴스의 유일성을 보장하는 데 중점을 두고 있으며, 팩토리 패턴은 다양한 객체를 생성하는 데 중점을 둔다. 두 패턴은 함께 사용될 수 있으며, 팩토리 메서드에서 싱글턴 인스턴스를 반환하도록 구현할 수 있다.

**플라이웨이트 패턴과의 관계**  
플라이웨이트 패턴은 메모리 사용을 최적화하기 위해 공유 가능한 객체를 재사용하는 디자인 패턴이다. 싱글턴 패턴과 플라이웨이트 패턴은 모두 객체의 수를 제한하는 데 중점을 두지만, 그 접근 방식은 다르다. 싱글턴 패턴은 특정 클래스의 인스턴스를 하나만 생성하는 반면, 플라이웨이트 패턴은 동일한 객체를 여러 번 재사용하여 메모리 사용을 줄인다.

## 자주 묻는 질문

**싱글턴 패턴은 언제 사용해야 하나요?**  
싱글턴 패턴은 특정 클래스의 인스턴스가 오직 하나만 존재해야 할 때 사용해야 한다. 예를 들어, 애플리케이션에서 데이터베이스 연결을 관리하는 클래스나, 설정 정보를 관리하는 클래스와 같이 전역적으로 접근해야 하는 자원에 적합하다.

**싱글턴 패턴의 단점은 무엇인가요?**  
싱글턴 패턴의 주요 단점은 단일 책임 원칙(SRP)을 위반할 수 있다는 점이다. 또한, 테스트가 어려워지는 문제도 있다. 마지막으로, 멀티 스레드 환경에서의 안전성 문제도 고려해야 한다.

**멀티 스레드 환경에서 싱글턴을 안전하게 구현하는 방법은?**  
멀티 스레드 환경에서 싱글턴을 안전하게 구현하기 위해서는 'Double-Checked Locking' 패턴을 사용하는 방법이 있다. 또 다른 방법으로는 'Initialization-on-demand Holder Pattern'을 사용할 수 있다.

**싱글턴 패턴을 테스트하는 방법은?**  
싱글턴 패턴을 테스트하는 방법으로는 인스턴스를 여러 번 호출하여 항상 동일한 인스턴스가 반환되는지를 확인하는 방법이 있다. 또한, 테스트 프레임워크를 사용하여 의존성을 주입하고, 싱글턴 인스턴스를 모킹(mocking)하여 테스트할 수도 있다.

## 결론

**싱글턴 패턴의 요약**  
싱글턴 패턴은 객체 지향 프로그래밍에서 특정 클래스의 인스턴스가 오직 하나만 존재하도록 보장하는 디자인 패턴이다. 이 패턴은 전역 접근 지점을 제공하며, 자원 관리의 용이성을 높인다.

**싱글턴 패턴의 적절한 사용법**  
싱글턴 패턴은 특정 자원이나 서비스가 애플리케이션 전역에서 단 하나만 존재해야 할 때 유용하다. 예를 들어, 데이터베이스 연결, 로깅 시스템, 설정 관리 등에서 사용될 수 있다.

**미래의 디자인 패턴에 대한 전망**  
디자인 패턴은 소프트웨어 개발의 복잡성을 줄이고, 코드의 재사용성을 높이는 데 기여한다. 싱글턴 패턴은 여전히 유용하지만, 현대의 소프트웨어 아키텍처에서는 더 많은 유연성과 테스트 용이성을 제공하는 패턴들이 주목받고 있다. 앞으로도 다양한 디자인 패턴이 발전하고, 새로운 요구사항에 맞춰 진화할 것으로 예상된다.

## Reference

* [refactoring.guru - 싱글턴 패턴](https://refactoring.guru/ko/design-patterns/singleton)
* [gmlwjd9405 블로그 - 싱글턴 패턴](https://gmlwjd9405.github.io/2018/07/06/singleton-pattern.html)
* [velog - 싱글턴 패턴](https://velog.io/@wlsrhkd4023/Design-Pattern-%EC%8B%B1%EA%B8%80%ED%86%A4-%ED%8C%A8%ED%84%B4Singleton-Pattern-rzs6f6vd)
* [위키백과 - 싱글턴 패턴](https://en.wikipedia.org/wiki/Singleton_pattern)
* [HexaBrain 블로그 - 싱글턴 패턴](https://blog.hexabrain.net/394)


<!--
#  싱글턴 패턴

다음 이름으로도 불립니다:  Singleton

##  의도

**싱글턴** 은 클래스에 인스턴스가 하나만 있도록 하면서 이 인스턴스에 대한 전역 접근​(액세스) 지점을 제공하는 생성 디자인 패턴입니다.

![싱글턴
패턴](https://refactoring.guru/images/patterns/content/singleton/singleton.png?id=108a0b9b5ea5c4426e0afa4504491d6f)

##  __ 문제

싱글턴 패턴은 한 번에 두 가지의 문제를 동시에 해결함으로써 _ 단  일  책  임  원  칙  _ 을 위반합니다.

  1. **클래스에 인스턴스가 하나만 있도록 합니다** . 사람들은 클래스에 있는 인스턴스 수를 제어하려는 가장 일반적인 이유는 일부 공유 리소스​(예: 데이터베이스 또는 파일)​에 대한 접근을 제어하기 위함입니다. 

예를 들어 객체를 생성했지만 잠시 후 새 객체를 생성하기로 했다고 가정해 봅시다. 그러면 새 객체를 생성하는 대신 이미 만든 객체를 받게
됩니다.

물론 생성자 호출은 특성상 **반드시** 새 객체를 반환해야 하므로 위 행동은 일반 생성자로 구현할 수 없습니다.

![객체에 대한 전역
접근](https://refactoring.guru/images/patterns/content/singleton/singleton-
comic-1-ko.png?id=b0a209b736f252f5457f0e1fde6e19ac)

클라이언트들은 항상 같은 객체와 작업하고 있다는 사실을 인식조차 못 할 수 있습니다.

  2. **해당 인스턴스에 대한 전역 접근 지점을 제공합니다** . 필수 객체들을 저장하기 위해 전역 변수들을 정의했다고 가정해 봅시다. 이 변수들을 사용하면 매우 편리할지는 몰라도, 모든 코드가 잠재적으로 해당 변수의 내용을 덮어쓸 수 있고 그로 인해 앱에 오류가 발생해 충돌할 수 있으므로 그리 안전한 방법은 아닙니다. 

전역 변수와 마찬가지로 싱글턴 패턴을 사용하면 프로그램의 모든 곳에서부터 일부 객체에 접근할 수 있습니다. 그러나 이 패턴은 다른 코드가
해당 인스턴스를 덮어쓰지 못하도록 보호하기도 합니다.

이 문제에는 또 다른 측면이 있습니다. 당신은 첫 번째 문제를 해결하는 코드가 프로그램 전체에 흩어져 있는 것을 원하지 않을 것입니다. 특히
코드의 나머지 부분이 이미 첫 번째 문제를 해결하는 코드에 의존하고 있다면, 이 코드를 한 클래스 내에 두는 것이 훨씬 좋습니다.

최근에는 싱글턴 패턴이 워낙 대중화되어 패턴이 나열된 문제 중 한 가지만 해결하더라도 그것을 _ 싱  글  턴  _ 이라고 부를 수
있습니다.

##  __ 해결책

싱글턴의 모든 구현은 공통적으로 다음의 두 단계를 갖습니다.

  * 다른 객체들이 싱글턴 클래스와 함께 ` new ` 연산자를 사용하지 못하도록 디폴트 생성자를 비공개로 설정하세요. 
  * 생성자 역할을 하는 정적 생성 메서드를 만드세요. 내부적으로 이 메서드는 객체를 만들기 위하여 비공개 생성자를 호출한 후 객체를 정적 필드에 저장합니다. 이 메서드에 대한 그다음 호출들은 모두 캐시된 객체를 반환합니다. 

당신의 코드가 싱글턴 클래스에 접근할 수 있는 경우, 이 코드는 싱글턴의 정적 메서드를 호출할 수 있습니다. 따라서 해당 메서드가 호출될
때마다 항상 같은 객체가 반환됩니다.

##  __ 실제상황 적용

정부는 싱글턴 패턴의 훌륭한 예입니다. 국가는 하나의 공식 정부만 가질 수 있습니다. 그리고 'X의 정부'라는 명칭은 정부를 구성하는
개인들의 신원과 관계없이 정부 책임자들의 그룹을 식별하는 글로벌 접근 지점입니다.

##  __ 구조

  1. **싱글턴** 클래스는 정적 메서드 ` get­Instance ` 를 선언합니다. 이 메서드는 자체 클래스의 같은 인스턴스를 반환합니다. 

싱글턴의 생성자는 항상 클라이언트 코드에서부터 숨겨져야 합니다. ` get­Instance ` 메서드를 호출하는 것이 Singleton
객체를 가져올 수 있는 유일한 방법이어야 합니다.

##  __ 의사코드

이 예에서 데이터베이스의 연결 클래스는 **싱글턴** 의 역할을 합니다. 이 클래스에는 공개된 생성자가 없으므로 해당 클래스의 객체를
가져오는 유일한 방법은 ` get­Instance ` 메서드를 호출하는 것입니다. 이 메서드는 처음 생성된 객체를 캐시 한 후 모든 후속
호출들에서 해당 객체를 반환합니다.

    
    
    // 데이터베이스 클래스는 클라이언트들이 프로그램 전체에서 데이터베이스 연결의 같은
    // 인스턴스에 접근할 수 있도록 해주는 `getInstance`(인스턴스 가져오기) 메서드를
    // 정의합니다.
    class Database is
        // 싱글턴 인스턴스를 저장하기 위한 필드는 정적으로 선언되어야 합니다.
        private static field instance: Database
    
        // 싱글턴의 생성자는 `new` 연산자를 사용한 직접 생성 호출들을 방지하기 위해
        // 항상 비공개여야 합니다.
        private constructor Database() is
            // 데이터베이스 서버에 대한 실제 연결과 같은 일부 초기화 코드.
    
        // 싱글턴 인스턴스로의 접근을 제어하는 정적 메서드.
        public static method getInstance() is
            if (Database.instance == null) then
                acquireThreadLock() and then
                    // 이 스레드가 잠금 해제를 기다리는 동안 인스턴스가 다른
                    // 스레드에 의해 초기화되지 않았는지 확인하세요.
                    if (Database.instance == null) then
                        Database.instance = new Database()
            return Database.instance
    
        // 마지막으로 모든 싱글턴은 해당 로직의 인스턴스에서 실행할 수 있는 비즈니스
        // 로직을 정의해야 합니다.
        public method query(sql) is
            // 예를 들어 앱의 모든 데이터베이스 쿼리들은 이 메서드를 거칩니다. 따라서
            // 여기에 스로틀링 또는 캐싱 논리를 배치할 수 있습니다.
            // …
    
    class Application is
        method main() is
            Database foo = Database.getInstance()
            foo.query("SELECT ...")
            // …
            Database bar = Database.getInstance()
            bar.query("SELECT ...")
            // 변수 `bar`는 변수 `foo`와 같은 객체를 포함할 것입니다.
    

##  __ 적용

__ 싱글턴 패턴은 당신 프로그램의 클래스에 모든 클라이언트가 사용할 수 있는 단일 인스턴스만 있어야 할 때 사용하세요. 예를 들자면
프로그램의 다른 부분들에서 공유되는 단일 데이터베이스 객체처럼 말입니다.

__ 싱글턴 패턴은 특별 생성 메서드를 제외하고는 클래스의 객체들을 생성할 수 있는 모든 다른 수단들을 비활성화합니다. 이 메서드는 새
객체를 생성하거나 객체가 이미 생성되었으면 기존 객체를 반환합니다.

__ 싱글턴 패턴은 전역 변수들을 더 엄격하게 제어해야 할 때 사용하세요.

__ 전역 변수들과 달리 싱글턴 패턴은 클래스의 인스턴스가 하나만 있도록 보장해 줍니다. 캐시 된 인스턴스는 싱글턴 클래스 자체를 제외하고는
그 어떤 것과도 대체될 수 없습니다.

참고로 이 제한은 언제든 조정할 수 있고 원하는 수만큼의 싱글턴 인스턴스 생성을 허용할 수 있습니다. 그러기 위해서 변경해야 하는 코드의
유일한 부분은 ` get­Instance ` 메서드의 본문입니다.

##  __ 구현방법

  1. 싱글턴 인스턴스의 저장을 위해 클래스에 비공개 정적 필드를 추가하세요. 

  2. 싱글턴 인스턴스를 가져오기 위한 공개된 정적 생성 메서드를 선언하세요. 

  3. 정적 메서드 내에서 '지연된 초기화'를 구현하세요. 그러면 이것은 첫 번째 호출에서 새 객체를 만든 후 그 객체를 정적 필드에 넣을 것입니다. 이 메서드는 모든 후속 호출들에서 항상 해당 인스턴스를 반환해야 합니다. 

  4. 클래스의 생성자를 비공개로 만드세요. 그러면 클래스의 정적 메서드는 여전히 생성자를 호출할 수 있지만 다른 객체들은 호출할 수 없을 것입니다. 

  5. 클라이언트 코드를 살펴보며 싱글턴의 생성자에 대한 모든 직접 호출들을 싱글턴의 정적 생성 메서드에 대한 호출로 바꾸세요. 

##  __ 장단점

  * __ 클래스가 하나의 인스턴트만 갖는다는 것을 확신할 수 있습니다. 
  * __ 이 인스턴스에 대한 전역 접근 지점을 얻습니다. 
  * __ 싱글턴 객체는 처음 요청될 때만 초기화됩니다. 

  * __ _ 단  일  책  임  원  칙  _ 을 위반합니다. 이 패턴은 한 번에 두 가지의 문제를 동시에 해결합니다. 
  * __ 또 싱글턴 패턴은 잘못된 디자인​(예를 들어 프로그램의 컴포넌트들이 서로에 대해 너무 많이 알고 있는 경우)​을 가릴 수 있습니다. 
  * __ 그리고 이 패턴은 다중 스레드 환경에서 여러 스레드가 싱글턴 객체를 여러 번 생성하지 않도록 특별한 처리가 필요합니다. 
  * __ 싱글턴의 클라이언트 코드를 유닛 테스트하기 어려울 수 있습니다. 그 이유는 많은 테스트 프레임워크들이 모의 객체들을 생성할 때 상속에 의존하기 때문입니다. 싱글턴 클래스의 생성자는 비공개이고 대부분 언어에서 정적 메서드를 오버라이딩하는 것이 불가능하므로 싱글턴의 한계를 극복할 수 있는 창의적인 방법을 생각해야 합니다. 아니면 그냥 테스트를 작성하지 말거나 싱글턴 패턴을 사용하지 않으면 됩니다. 

##  __ 다른 패턴과의 관계

  * 대부분의 경우 하나의 퍼사드 객체만 있어도 충분하므로 [ 퍼사드 ](/ko/design-patterns/facade) 패턴의 클래스는 종종 [ 싱글턴 ](/ko/design-patterns/singleton) 으로 변환될 수 있습니다. 

  * 만약 객체들의 공유된 상태들을 단 하나의 플라이웨이트 객체로 줄일 수 있다면 [ 플라이웨이트 ](/ko/design-patterns/flyweight) 는 [ 싱글턴 ](/ko/design-patterns/singleton) 과 유사해질 수 있습니다. 그러나 이 패턴들에는 두 가지 근본적인 차이점이 있습니다: 

    1. 싱글턴은 인스턴스가 하나만 있어야 합니다. 반면에 _ 플  라  이  웨  이  트  _ 클래스는 여러 고유한 상태를 가진 여러 인스턴스를 포함할 수 있습니다. 
    2. _ 싱  글  턴  _ 객체는 변할 수 있습니다 (mutable). 플라이웨이트 객체들은 변할 수 없습니다 (immutable). 
  * [ 추상 팩토리들 ](/ko/design-patterns/abstract-factory) , [ 빌더들 ](/ko/design-patterns/builder) 및 [ 프로토타입들 ](/ko/design-patterns/prototype) 은 모두 [ 싱글턴 ](/ko/design-patterns/singleton) 으로 구현할 수 있습니다. 


-->

<!--






-->

<!--
##  Goal

>   * 싱글턴 패턴의 개념을 이해한다.
>   * 예시를 통해 싱글턴 패턴을 이해한다.
>

##  싱글턴 패턴이란

  * 전역 변수를 사용하지 않고 **객체를 하나만 생성** 하도록 하며, 생성된 객체를 **어디에서든지 참조할 수 있도록** 하는 패턴 
    * ‘생성(Creational) 패턴’의 하나 ( _아래 참고_ ) 
  * ![](https://gmlwjd9405.github.io/images/design-pattern-singleton/singleton-example.png)
  * 역할이 수행하는 작업 
    * Singleton 
      * 하나의 인스턴스만을 생성하는 책임이 있으며 getInstance 메서드를 통해 모든 클라이언트에게 동일한 인스턴스를 반환하는 작업을 수행한다. 

참고

  * 생성(Creational) 패턴 
    * 객체 생성에 관련된 패턴 
    * 객체의 생성과 조합을 캡슐화해 특정 객체가 생성되거나 변경되어도 프로그램 구조에 영향을 크게 받지 않도록 유연성을 제공한다. 

##  예시

###  프린터 관리자 만들기

###  문제점

**다중 스레드에서** Printer 클래스를 이용할 때 인스턴스가 1개 이상 생성되는 경우가 발생할 수 있다.

  * **경합 조건(Race Condition)** 을 발생시키는 경우 
    1. Printer 인스턴스가 아직 생성되지 않았을 때 스게드 1이 getPrinter 메서드의 if문을 실행해 이미 인스턴스가 생성되었는지 확인한다. 현재 printer 변수는 null인 상태다. 
    2. 만약 스레드 1이 생성자를 호출해 인스턴스를 만들기 전 스레드 2가 if문을 실행해 printer 변수가 null인지 확인한다. 현재 printer 변수는 null이므로 인스턴스를 생성하는 생성자를 호출하는 코드를 실행하게 된다. 
    3. 스레드 1도 스레드 2와 마찬가지로 인스턴스를 생성하는 코드를 실행하게 되면 결과적으로 Printer 클래스의 인스턴스가 2개 생성된다. 
  * 경합 조건이란? 
    * 메모리와 같은 동일한 자원을 2개 이상의 스레드가 이용하려고 경합하는 현상 
  * 스레드 스케줄링을 고의로 변경하여 경합 조건을 만들어보자. 
    
        public class Printer {
        // 외부에 제공할 자기 자신의 인스턴스
        private static Printer printer = null;
        private Printer() { }
        // 자기 자신의 인스턴스를 외부에 제공
        public static Printer getPrinter(){
          // 조건 검사 구문 (문제의 원인!)
          if (printer == null) {
            try {
              // 스레드 스케줄링 변경(스레드 실행 1ms동안 정지)
              Thread.sleep(1);
            } catch (InterruptedException e) { }
    
            // Printer 인스턴스 생성
            printer = new Printer();
          }
          return printer;
        }
        public void print(String str) {
          System.out.println(str);
        }
    }
    
    
        public class UserThread extends Thread{
      public UserThread(String name) { super(name); }
      public void run() {
        Printer printer = printer.getPrinter();
        printer.print(Thread.currentThread().getName() + " print using " + printer.toString());
      }
    }
    public class Client {
      private static final int THREAD_NUM = 5;
      public static void main(String[] args) {
        UserThread[] user = new UserThread[THREAD_NUM];
        for (int i = 0; i < THREAD_NUM; i++) {
          // UserThread 인스턴스 생성
          user[i] = new UserThread((i+1));
          user[i].start();
        }
      }
    }
    

###  해결책

프린터 관리자(Lazy Initialization)는 사실 **다중 스레드 애플리케이션이 아닌 경우에는 아무런 문제가 되지 않는다.**

  * 다중 스레드 애플리케이션에서 발생하는 문제를 해결하는 방법 
    1. 정적 변수에 인스턴스를 만들어 바로 초기화하는 방법 (Eager Initialization) 
    2. 인스턴스를 만드는 메서드에 동기화하는 방법 (Thread-Safe Initialization) 

  1. 정적 변수에 인스턴스를 만들어 바로 초기화하는 방법 
    
        public class Printer {
       // static 변수에 외부에 제공할 자기 자신의 인스턴스를 만들어 초기화
       private static Printer printer = new Printer();
       private Printer() { }
       // 자기 자신의 인스턴스를 외부에 제공
       public static Printer getPrinter(){
         return printer;
       }
       public void print(String str) {
         System.out.println(str);
       }
    }
    

     * static 변수 
       * 객체가 생성되기 전 클래스가 메모리에 로딩될 때 만들어져 초기화가 한 번만 실행된다. 
       * 프로그램 시작~종료까지 없어지지 않고 메모리에 계속 상주하며 클래스에서 생성된 모든 객체에서 참조할 수 있다. 
  2. 인스턴스를 만드는 메서드에 동기화하는 방법 
    
        public class Printer {
       // 외부에 제공할 자기 자신의 인스턴스
       private static Printer printer = null;
       private int counter = 0;
       private Printer() { }
       // 인스턴스를 만드는 메서드 동기화 (임계 구역)
       public synchronized static Printer getPrinter(){
         if (printer == null) {
           printer = new Printer(); // Printer 인스턴스 생성
         }
         return printer;
       }
       public void print(String str) {
         // 오직 하나의 스레드만 접근을 허용함 (임계 구역)
         // 성능을 위해 필요한 부분만을 임계 구역으로 설정한다.
         synchronized(this) {
           counter++;
           System.out.println(str + counter);
         }
       }
    }
    

     * 인스턴스를 만드는 메서드를 **임계 구역으로 변경**
       * 다중 스레드 환경에서 동시에 여러 스레드가 getPrinter 메서드를 소유하는 객체에 접근하는 것을 방지한다. 
     * 공유 변수에 접근하는 부분을 **임계 구역으로 변경**
       * 여러 개의 스레드가 하나뿐인 counter 변수 값에 동시에 접근해 갱신하는 것을 방지한다. 
     * getInstance()에 Lock을 하는 방식이라 속도가 느리다. 

##  정적 클래스

정적 메서드로만 이루어진 정적 클래스를 사용하면 싱글턴과 동일한 효과를 얻을 수 있다.

    
    
    public class Printer {
          private static int counter = 0;
          // 메서드 동기화 (임계 구역)
          public synchronized static void print(String str) {
            counter++;
            System.out.println(str + counter);
          }
    }
    
    
    
    public class UserThread extends Thread{
        // 스레드 생성
        public UserThread(String name) { super(name); }
        // 현재 스레드 이름 출력
        public void run() {
          Printer.print(Thread.currentThread().getName());
        }
    }
    public class Client {
        private static final int THREAD_NUM = 5;
        public static void main(String[] args) {
          UserThread[] user = new UserThread[THREAD_NUM];
          for (int i = 0; i < THREAD_NUM; i++) {
            // UserThread 인스턴스 생성
            user[i] = new UserThread((i+1));
            user[i].start();
          }
        }
    }
    

  * 차이점 
    * 정적 클래스를 이용하면 객체를 전혀 생성하지 않고 메서드를 사용한다. 
    * 정적 메서드를 사용하므로 일반적으로 실행할 때 바인딩되는(컴파일 타임에 바인딩되는) 인스턴스 메서드를 사용하는 것보다 성능 면에서 우수하다. 
  * 정적 클래스를 사용할 수 없는 경우 
    * 인터페이스를 구현해야 하는 경우, 정적 메서드는 인터페이스에서 사용할 수 없다. 
  * 인터페이스를 사용하는 주된 이유? 
    * 대체 구현이 필요한 경우 
    * 예를 들어 Mock 객체를 사용해 단위 테스트를 수행하는 경우 

##  Enum 클래스

    
    
    public enum SingletonTest {
    	INSTANCE;
      
    	public static SingletonTest getInstance() {		
    		return INSTANCE;
    	}
    }
    

  * Thread-safety와 Serialization이 보장된다. 
  * Reflection을 통한 공격에도 안전하다. 
  * 따라서 Enum을 이용해서 Singleton을 구현하는 것이 가장 좋은 방법이다. 

#  관련된 Post

#  References

>


-->

<!--






-->

<!--
##  싱글톤 패턴

이번글에서는 디자인 패턴 중 하나인 싱글톤 패턴에 대해서 알아봅니다.

싱글톤 패턴은 객체 지향 소프트웨어에서 반복되는 문제를 해결하기 위해 잘 설명해진 [ GoF 디자인 패턴
](https://en.wikipedia.org/wiki/Design_Patterns) 중 하나입니다. 싱글톤 패턴은 클래스의 인스턴스화를
**단일 인스턴스** 로 제한하는 패턴입니다.

##  싱글톤 패턴의 특징

  * 오직 하나의 객체 인스턴스를 가진다 
  * 인스턴스에 접근하기 위한 쉬운 방법을 제공한다 
  * 인스턴스화를 컨트롤한다 (ex.클래스 생성자를 숨김) 

####  싱글톤 패턴의 장점

싱글톤 패턴을 사용하여 인스턴스를 한 개로만 가져가면 아래와 같은 이점이 있습니다.

  * **메모리 비용 절감** : 객체를 생성할 때 마다 메모리를 할당 받는데 한번의 최초 한번의 new를 통해 객체를 생성한다면 고정된 메모리 영역의 사용으로 메모리 비용을 절감할 수 있다 
  * **데이터 공유** : 싱글톤 인스턴스는 전역으로 사용되는 인스턴스이기 때문에 다른 클래스의 인스턴스들과 데이터를 공유할 수 있다 

####  싱글톤 패턴의 단점

싱글톤 패턴만의 장점도 분명하지만 반대로 안티패턴이라고 불릴만큼 단점도 많이 있습니다.

  * **테스트하기 어려움** : 많은 데이터를 공유할 수록 다른 클래스들 간의 결합도(Coupling)이 높아지고 개방-폐쇄원칙(OCP)을 위배하면서 테스트하기가 어려워짐 
  * **멀티 스레드 처리** : 멀티 스레드 환경에서 여러 인스턴스가 생성되는 것을 방지하기 위한 동기화 처리를 위해 syncronized 키워드를 사용해야하고 이는 많은 양의 코드를 작성을 요구함 
  * **SOLID 원칙 위반(SRP, DIP, OCP)** : 싱글톤은 Primary Function과 하나의 인스턴스만 생성 두 가지 책임이 있기 때문에 SRP를 위반하고 의존관계상 클라이언트가 구현체에 의존하면서 DIP를 위반하고 자연스럽게 OCP도 위반할 가능성이 높다. 

##  구현 코드

####  Java

    
    
    public class Coin {
    
        private static final int ADD_MORE_COIN = 10;
        private int coin;
        private static Coin instance = new Coin(); // eagerly loads the singleton
    
        private Coin() {
            // private to prevent anyone else from instantiating
        }
    
        public static Coin getInstance() {
            return instance;
        }
    
        public int getCoin() {
            return coin;
        }
    
        public void addMoreCoin() {
            coin += ADD_MORE_COIN;
        }
    
        public void deductCoin() {
            coin--;
        }
    }
    

####  Kotlin

    
    
    object Coin {
        private var coin: Int = 0
    
        fun getCoin():Int {
            return coin
        }
    
        fun addCoin() {
            coin += 10
        }
    
        fun deductCoin() {
            coin--
        }
    }

###  멀티스레드 환경에서 싱글톤 생성

####  지연 초기화(Lazy initialization)

멀티 스레드에서 하나의 싱글톤 객체에 접근할 때 경쟁 상태(Race Condition)이 발생하여 여러개의 인스턴스가 생성될 수 있어
자바에서는 synchronized로 감싸서 지연 초기화를 더블체킹과함께 스레드 세이프하게 생성해야한다.

    
    
    public class Singleton {
    
        private static volatile Singleton instance = null;
    
        private Singleton() {}
    
        public static Singleton getInstance() {
            if (instance == null) {
                synchronized(Singleton.class) {
                    if (instance == null) {
                        instance = new Singleton();
                    }
                }
            }
    
            return instance;
        }
    }

###  완벽한 싱글톤을 만들기 위해

앞서 제시한 싱글톤을 생성한 방법은 두가지 문제점이 있다

  1. 직렬화와 역직렬화 
  2. 리플렉션   
싱글톤 클래스를 직렬화와 역직렬화 할 때 인스턴스가 새로 생성되어 싱글톤의 단일 인스턴스를 위반한다. 그리고 리플렉션을 이용하여 런타임에
싱글톤 private 생성자에 접근하여 새로운 인스턴스를 생성할 수 있다. 이 두가지 문제는 Enum을 통해 해결할 수 있다

    
    
    enum EnumSingleton {
        INSTANCE;
        String name;
        
        public String getName() {
            return name;
        }
        public void setName(String name) {
            this.name = name;
        }
    }
    // EnumSingleton singleton = EnumSingleton.INSTANCE;

Enum은 직렬화와 역직렬화가 가능하기 때문에 별도의 ` Serializable ` 을 구현하지 않아도 되고 리플렉션을 시도하려고 하면 `
NoSuchMethodException ` 이 발생하기 때문에 외부에서 싱글톤 인스턴스를 생성하는 것은 불가능하므로 완벽한 싱글톤 형태라고
불린다.

##  결론

싱글톤은 이점이 있는 패턴이지만 앱 전역의 상태 관리를 하는데 있어서 안티패턴으로 간주된다. 이로 인해 싱글톤에 대한 잠재적인 종속성이
도입되어 실제 코드를 분석하기 위한 어려움과 크고 리팩토링에 대한 비용도 증가한다. 그리고 SOLID 원칙중 SRP, DIP, OCP를 위반
할 수 있고 이로인해 테스트하기 어렵다.

###  참고


-->

<!--






-->

<!--
Design pattern in object-oriented software development

[
![](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Singleton_UML_class_diagram.svg/220px-
Singleton_UML_class_diagram.svg.png)
](/wiki/File:Singleton_UML_class_diagram.svg) A [ class diagram
](/wiki/Class_diagram "Class diagram") exemplifying the singleton pattern.

In [ software engineering ](/wiki/Software_engineering "Software engineering")
, the **singleton pattern** is a [ software design pattern
](/wiki/Software_design_pattern "Software design pattern") that restricts the
[ instantiation ](/wiki/Instantiation_\(computer_science\) "Instantiation
\(computer science\)") of a [ class ](/wiki/Class_\(computer_programming\)
"Class \(computer programming\)") to a singular instance. One of the well-
known [ "Gang of Four" design patterns ](/wiki/Design_Patterns "Design
Patterns") , which describes how to solve recurring problems in [ object-
oriented software ](/wiki/Object-oriented_programming "Object-oriented
programming") ,  [  1  ]  the pattern is useful when exactly one object is
needed to coordinate actions across a system.

More specifically, the singleton pattern allows objects to:  [  2  ]

  * Ensure they only have one instance 
  * Provide easy access to that instance 
  * Control their instantiation (for example, hiding the [ constructors ](/wiki/Constructor_\(object-oriented_programming\) "Constructor \(object-oriented programming\)") of a [ class ](/wiki/Class_\(computer_programming\) "Class \(computer programming\)") ) 

The term comes from the [ mathematical concept of a singleton
](/wiki/Singleton_\(mathematics\) "Singleton \(mathematics\)") .

Singletons are often preferred to [ global variables ](/wiki/Global_variables
"Global variables") because they do not pollute the global [ namespace
](/wiki/Namespace "Namespace") (or their containing namespace). Additionally,
they permit [ lazy ](/wiki/Lazy_evaluation "Lazy evaluation") allocation and
initialization, whereas global variables in many languages will always consume
resources.  [  1  ]  [  3  ]

The singleton pattern can also be used as a basis for other design patterns,
such as the [ abstract factory ](/wiki/Abstract_factory_pattern "Abstract
factory pattern") , [ factory method ](/wiki/Factory_method_pattern "Factory
method pattern") , [ builder ](/wiki/Builder_pattern "Builder pattern") and [
prototype ](/wiki/Prototype_pattern "Prototype pattern") patterns. [ Facade
](/wiki/Facade_pattern "Facade pattern") objects are also often singletons
because only one facade object is required.

[ Logging ](/wiki/Log_file "Log file") is a common real-world use case for
singletons, because all objects that wish to log messages require a uniform
point of access and conceptually write to a single source.  [  4  ]

Implementations of the singleton pattern ensure that only one instance of the
singleton class ever exists and typically provide [ global access
](/wiki/Global_scope "Global scope") to that instance.

Typically, this is accomplished by:

The instance is usually stored as a private [ static variable
](/wiki/Static_variable "Static variable") ; the instance is created when the
variable is initialized, at some point before when the static method is first
called.

This C++11 implementation is based on the pre C++98 implementation in the book
[ _[ citation needed  ](/wiki/Wikipedia:Citation_needed "Wikipedia:Citation
needed") _ ]  .

    
    
    #include <iostream>
    
    class Singleton {
    public:
      // defines an class operation that lets clients access its unique instance.
      static Singleton& get() {
        // may be responsible for creating its own unique instance.
        if (nullptr == instance) instance = new Singleton;
        return *instance;
      }
      Singleton(const Singleton&) = delete; // rule of three
      Singleton& operator=(const Singleton&) = delete;
      static void destruct() {
        delete instance;
        instance = nullptr;
      }
      // existing interface goes here
      int getValue() {
        return value;
      }
      void setValue(int value_) {
        value = value_;
      }
    private:
      Singleton() = default; // no public constructor
      ~Singleton() = default; // no public destructor
      static Singleton* instance; // declaration class variable
      int value;
    };
    
    Singleton* Singleton::instance = nullptr; // definition class variable
    
    int main() {
      Singleton::get().setValue(42);
      std::cout << "value=" << Singleton::get().getValue() << '\n';
      Singleton::destruct();
    }
    

The program output is

This is an implementation of the Meyers singleton  [  5  ]  in C++11. The
Meyers singleton has no destruct method. The program output is the same as
above.

    
    
    #include <iostream>
    
    class Singleton {
    public:
      static Singleton& get() {
        static Singleton instance;
        return instance;
      }
      int getValue() {
        return value;
      }
      void setValue(int value_) {
        value = value_;
      }
    private:
      Singleton() = default;
      ~Singleton() = default;
      int value;
    };
    
    int main() {
      Singleton::get().setValue(42);
      std::cout << "value=" << Singleton::get().getValue() << '\n';
    }
    

###  Lazy initialization

[  [ edit  ](/w/index.php?title=Singleton_pattern&action=edit&section=3 "Edit
section: Lazy initialization") ]

A singleton implementation may use [ lazy initialization
](/wiki/Lazy_initialization "Lazy initialization") in which the instance is
created when the static method is first invoked. In [ multithreaded
](/wiki/Multithreading_\(software\) "Multithreading \(software\)") programs,
this can cause [ race conditions ](/wiki/Race_condition "Race condition") that
result in the creation of multiple instances. The following [ Java 5+
](/wiki/Java_version_history#Java_5 "Java version history") example  [  6  ]
is a [ thread-safe ](/wiki/Thread_safety "Thread safety") implementation,
using lazy initialization with [ double-checked locking ](/wiki/Double-
checked_locking "Double-checked locking") .

    
    
    public class Singleton {
    
        private static volatile Singleton instance = null;
    
        private Singleton() {}
    
        public static Singleton getInstance() {
            if (instance == null) {
                synchronized(Singleton.class) {
                    if (instance == null) {
                        instance = new Singleton();
                    }
                }
            }
            return instance;
        }
    }
    

Some consider the singleton to be an [ anti-pattern ](/wiki/Anti-pattern
"Anti-pattern") that introduces [ global state ](/wiki/Global_variables
"Global variables") into an application, often unnecessarily. This introduces
a potential dependency on the singleton by other objects, requiring analysis
of implementation details to determine whether a dependency actually exists.
[  7  ]  This increased [ coupling ](/wiki/Coupling_\(computer_programming\)
"Coupling \(computer programming\)") can introduce difficulties with [ unit
testing ](/wiki/Unit_testing "Unit testing") .  [  8  ]  In turn, this places
restrictions on any abstraction that uses the singleton, such as preventing [
concurrent ](/wiki/Concurrency_\(computer_science\) "Concurrency \(computer
science\)") use of multiple instances.  [  8  ]  [  9  ]  [  10  ]

Singletons also violate the [ single-responsibility principle ](/wiki/Single-
responsibility_principle "Single-responsibility principle") because they are
responsible for enforcing their own uniqueness along with performing their
normal functions.  [  8  ]

  1. ^  _**a** _ _**b** _ Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (1994).  [ _Design Patterns: Elements of Reusable Object-Oriented Software_ ](https://archive.org/details/designpatternsel00gamm/page/127) . Addison Wesley. pp. [ 127ff ](https://archive.org/details/designpatternsel00gamm/page/127) . [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 0-201-63361-2  ](/wiki/Special:BookSources/0-201-63361-2 "Special:BookSources/0-201-63361-2") .  ` {{ [ cite book ](/wiki/Template:Cite_book "Template:Cite book") }} ` : CS1 maint: multiple names: authors list ( [ link ](/wiki/Category:CS1_maint:_multiple_names:_authors_list "Category:CS1 maint: multiple names: authors list") ) 
  2. ** ^  ** [ "The Singleton design pattern - Problem, Solution, and Applicability" ](http://w3sdesign.com/?gr=c05&ugr=proble) . _w3sDesign.com_ . Retrieved  2017-08-16  . 
  3. ** ^  ** Soni, Devin (31 July 2019). [ "What Is a Singleton?" ](https://betterprogramming.pub/what-is-a-singleton-2dc38ca08e92) . _BetterProgramming_ . Retrieved  28 August  2021  . 
  4. ** ^  ** Rainsberger, J.B. (1 July 2001). [ "Use your singletons wisely" ](https://web.archive.org/web/20210224180356/https://www.ibm.com/developerworks/library/co-single/) . IBM. Archived from [ the original ](https://www.ibm.com/developerworks/library/co-single/) on 24 February 2021  . Retrieved  28 August  2021  . 
  5. ** ^  ** Scott Meyers (1997). _More Effective C++_ . Addison Wesley. pp. 146 ff. [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 0-201-63371-X  ](/wiki/Special:BookSources/0-201-63371-X "Special:BookSources/0-201-63371-X") . 
  6. ** ^  ** Eric Freeman, Elisabeth Freeman, Kathy Sierra, and Bert Bates (October 2004). [ "5: One of a Kind Objects: The Singleton Pattern" ](https://books.google.com/books?id=GGpXN9SMELMC&pg=PA182) . _Head First Design Patterns_ (First ed.). O'Reilly Media, Inc. p. 182. [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 978-0-596-00712-6  ](/wiki/Special:BookSources/978-0-596-00712-6 "Special:BookSources/978-0-596-00712-6") .  ` {{ [ cite book ](/wiki/Template:Cite_book "Template:Cite book") }} ` : CS1 maint: multiple names: authors list ( [ link ](/wiki/Category:CS1_maint:_multiple_names:_authors_list "Category:CS1 maint: multiple names: authors list") ) 
  7. ** ^  ** [ "Why Singletons Are Controversial" ](https://web.archive.org/web/20210506162753/https://code.google.com/archive/p/google-singleton-detector/wikis/WhySingletonsAreControversial.wiki) . _Google Code Archive_ . Archived from [ the original ](https://code.google.com/archive/p/google-singleton-detector/wikis/WhySingletonsAreControversial.wiki) on 6 May 2021  . Retrieved  28 August  2021  . 
  8. ^  _**a** _ _**b** _ _**c** _ Button, Brian (25 May 2004). [ "Why Singletons are Evil" ](https://web.archive.org/web/20210715184717/https://docs.microsoft.com/en-us/archive/blogs/scottdensmore/why-singletons-are-evil) . _Being Scott Densmore_ . Microsoft. Archived from [ the original ](https://docs.microsoft.com/en-us/archive/blogs/scottdensmore/why-singletons-are-evil) on 15 July 2021  . Retrieved  28 August  2021  . 
  9. ** ^  ** Steve Yegge. [ Singletons considered stupid ](http://steve.yegge.googlepages.com/singleton-considered-stupid) , September 2004 
  10. ** ^  ** Hevery, Miško, " [ Global State and Singletons ](http://googletesting.blogspot.com/2008/11/clean-code-talks-global-state-and.html) ", _Clean Code Talks_ , 21 November 2008. 


-->

<!--






-->

<!--
##  정의

싱글턴(singleton)은 오직 하나의 객체만을 생성할 수 있는 클래스를 말합니다. 따라서 싱글턴 패턴을 사용하면 쉽게 객체의 유일성을
보장할 수 있습니다. 또한 일반적으로 싱글턴 객체에 대한 참조를 public static 필드나 public static 메서드로 노출하므로
어디에서나 싱글턴 객체에 접근할 수 있습니다.

![](https://blog.kakaocdn.net/dn/ctQPjZ/btrBx1auqlI/O2INmcM9wkYtz8BjI1gRG0/img.png)

##  구현

###  public static final 필드

객체가 오직 하나만을 보장하려면 어떻게 해야 할까요? 바로 정적(static) 필드를 사용하는 것입니다. 정적 필드를 사용하면 모든 객체가
공유하는 필드를 만들 수 있으며, 한 번만 생성되고 별도의 메모리 공간에 저장된다는 특징이 있습니다.

    
    
    public class Singleton {
    	public static Singleton INSTANCE = new Singleton();
    	...
    }

하지만 이것으론 부족합니다. 외부에서 자유롭게 접근할 수 있기 때문에 이 필드에 다른 객체가 할당되거나, 이미 할당했는데 싱글턴 내부에서
다시 객체를 할당하는 실수가 없도록 final로 선언해야 합니다. 그리고 외부에서 생성자를 통해 객체를 생성할 수 없도록 생성자의 접근
범위를 private로 제한해야 합니다.

    
    
    public class Singleton {
    	public static final Singleton INSTANCE = new Singleton();
    
    	private Singleton() { }
    
    	...
    }
    
    // 혹은 ...
    public class Singleton {
    	private static final Singleton INSTANCE = new Singleton();
    
    	private Singleton() { }
    
    	public static Singleton getInstance() {
    		return INSTANCE;
    	}
    
    	...
    }

이러면 외부에서 아래와 같이 정적 필드로 접근할 수 있습니다.

    
    
    // 생성자의 접근 범위가 private이기 때문에 생성자로는 객체를 생성할 수 없다.
    // Singleton obj = new Singleton(); (X)
    
    // INSTANCE는 final로 선언되었기 때문에 외부에서 다시 지정하는 것은 불가능하다.
    // Singleton.INSTANCE = null; (X)
    
    // 외부에서 정적 필드로 다음과 같이 접근할 수 있다.
    Singleton.INSTANCE.service();
    
    // 혹은...
    Singleton obj = Singleton.getInstance();
    obj.service();

###  지연 초기화(lazy initialization)

혹은 아래와 같은 방법으로도 초기화할 수 있습니다. 아래 예시에서는 Singleton.getInstance() 메서드 호출 시점에 정적
필드가 아직 초기화되지 않았으면 객체를 생성하고, 그 후에는 전에 생성한 객체의 참조(reference)를 그대로 반환합니다.

    
    
    public class Singleton {  
        private static Singleton instance;  
      
        private Singleton() { }  
      
        public static Singleton getInstance() {  
            if (instance == null) {  
                instance = new Singleton();  
            }  
            return instance;  
        }  
    }

덧붙이자면, 사실은 여기에서 지연 초기화로 분류되지 않은 다른 방법들도 따지고 보면 지연 초기화처럼 동작합니다.

####  스레드 안전(thread safe)

여기서 주의할 점은 멀티 스레드 환경에서 위와 같은 초기화 방법을 사용할 경우 스레드 안전하지 않다는 문제가 있습니다. 두 개 이상의
스레드가 Singleton.getInstance()를 동시에 호출한다면 어떻게 될까요?

![](https://blog.kakaocdn.net/dn/ctaRyz/btrBu6DAbjp/b0oRHAkXCxeHkusTz4HQe1/img.png)

싱글턴 패턴으로 객체가 유일함을 보장하려고 했으나 위와 같이 스레드가 서로 다른 객체의 참조를 가지는 상황이 벌어질 수 있습니다. 따라서 한
번에 하나의 스레드만 접근할 수 있도록 다음과 같이 동기화를 해주어야 합니다.

    
    
    public class Singleton {  
        private static Singleton instance;  
      
        private Singleton() { }  
      
        public static synchronized Singleton getInstance() {  
            if (instance == null) {  
                instance = new Singleton();  
            }  
            return instance;  
        }  
    }

하지만 이 방법은 정적 필드가 초기화된 후 싱글턴 객체를 얻으려고 할 때 불필요하게 동기화가 일어나므로 성능이 걱정된다면 다음의 방법을
사용할 수 있습니다.

####  더블 체크 락킹(Double-Checked Locking)

여기서 객체가 올바르게 생성된 이후에는 별다른 수정 작업 없이 참조를 반환하는 작업만 있으므로 동기화 범위를 다음과 같이 줄일 수 있습니다.

    
    
    public class Singleton {  
        private static Singleton instance; // (1)
      
        private Singleton() { }  
    
    	// 코드가 다소 장황하지만 동기화 오버헤드를 피할 수 있으므로 성능 이점이 있다.
    	public static Singleton getInstance() {
    		if (instance == null) {
    			// 동기화 블록은 한번에 하나의 스레드만 접근할 수 있다.
    			synchronized (Singleton.class) {
    				if (instance == null) {
    					instance = new Singleton();
    				}
    			}
    		}
    		return instance;
    	}
    
    	...
    }

코드만 보면 정상적으로 동작할 것 같지만 멀티 스레드 환경에서는 직관을 벗어나는 동작을 보일 수 있습니다. 컴파일러가 최적화라는 명목으로
연산의 순서를 변경(reordering)할 수 있기 때문입니다. 프로그래머는 이를 단일 스레드 환경에서는 알아차릴 수 없지만 멀티 스레드
환경으로 오면 이야기가 달라집니다. 문제는 다음과 같습니다.

    
    
    if (instance == null) { // (1)
    	synchronized (Singleton.class) { // (2)
    		if (instance == null) { // (3)
    			instance = new Singleton(); // (4)
    		} // (5)
    	} // (6)
    } // (7)
    return instance; // (8)

한 스레드가 4번에서 싱글턴 객체를 위한 메모리 공간을 할당하고 참조를 instance에 저장한 후에 싱글턴 객체의 생성자에서 내부 상태
초기화가 이루어지고 있다고 해봅시다. 이렇게 초기화하고 있는 도중에 1번으로 다른 스레드가 들어와서 null이 아님을 확인하고 초기화 중인
객체 참조를 그대로 반환할 수도 있습니다. 따라서 외부에서는 올바르게 초기화되지 않은 객체의 상태를 관찰할 수 있습니다. 이를 보고 문득
'객체의 초기화가 완전히 끝난 다음에야 그 객체에 대한 참조가 instance에 저장되는 게 아닌가?'라고 생각할 수 있지만 실제론 동기화
블록 내부에서 컴파일러로 인해 재배열이 일어나므로 다르게 동작할 수도 있습니다. 그렇게 연산 순서가 뒤바뀌더라도 (단일 스레드에서는)
프로그래머가 관찰할 수 있는 결과는 바뀌지 않기 때문입니다. 하지만 멀티 스레드 환경에서는 위의 코드가 동시에 실행될 수 있으므로 이런
최적화는 적절하지 않습니다. 이를 방지하려면 어떻게 해야 할까요?

    
    
    public class Singleton {  
        private static volatile Singleton instance; // (1)
    
    	...
    }

바로 위와 같이 instance 필드를 volatile로 선언하는 것입니다. 이 키워드를 사용하여 instance 필드에 값을 쓸 때 이러한
재배열이 일어나지 않도록 컴파일러에게 지시할 수 있습니다(물론 volatile은 그 이상의 일을 합니다). 따라서 최종적으로는 아래와 같이
쓸 수 있습니다.

    
    
    public class Singleton {  
        private static volatile Singleton instance;
      
        private Singleton() { }  
    
    	public static Singleton getInstance() {
    		if (instance == null) {
    			synchronized (Singleton.class) {
    				if (instance == null) {
    					instance = new Singleton();
    				}
    			}
    		}
    		return instance;
    	}
    
    	...
    }

####  요청 시 초기화 홀더 패턴(Initialization-on-demand holder pattern)

이 방법은 홀더 클래스를 사용해서 지연 초기화를 구현합니다. 더블 체크 락킹보다 더 단순하며 안전하기까지 합니다.

    
    
    public class Singleton {  
    
        private Singleton() { }
        
        private static final class Holder {  
            private static final Singleton INSTANCE = new Singleton();  
        }  
        
        public static Singleton getInstance() {  
            return Holder.INSTANCE;  
        }
    
    	...
    }

어떻게 이런 방법을 사용할 수 있을까요? Holder.INSTANCE는 결국엔 즉시 초기화를 장황하게 사용하는 방법이 아닐까요? 물론
아닙니다. 이를 이해하려면 초기화가 언제 일어나는지 알고 있어야 하는데, 아래 내용은 [ JLS 12.4.1
](https://docs.oracle.com/javase/specs/jls/se9/html/jls-12.html#jls-12.4.1) 에서
확인할 수 있는 내용입니다.

> 클래스나 인터페이스 타입 T는 다음 중 하나가 처음 일어나기 직전에 초기화됩니다.  
>  
>  \- T는 클래스이며 T의 인스턴스가 생성된다.  
>  \- T에 선언된 정적 메서드가 호출된다.  
>  \- T에 선언된 정적 필드가 할당된다.  
>  (추가: 예를 들어서 외부에서 공개된 정적 필드에 값을 할당하는 등이 있다.)  
>  \- T에 선언된 정적 필드가 사용되며 이때 이 필드는 상수 변수가 아니다.  
>  (JLS 4.12.4: 상수 변수는 상수 표현식으로 초기화된 기본 타입이나 String 타입의 final 변수를 말한다.)

따라서 Holder 클래스에 선언된 정적 필드인 INSTANCE가 사용될 때 Holder 클래스의 초기화가 일어납니다. 즉, 위의 예시에서는
런타임에 Singleton.getInstance()를 호출하여 Holder.INSTANCE을 사용하기 전에 클래스로더를 통해 Holder
클래스의 초기화가 일어나게 됩니다. 그와 동시에 Holder 클래스의 초기화 단계에서 정적 필드 INSTANCE의 초기화가 단 한 번만
일어납니다.

굳이 중첩 클래스를 사용할 필요는 없지 않을까요?

맞습니다. JLS에서 위와 같은 내용을 보장하므로 Singleton 클래스의 초기화는 Singleton 클래스의 '정적 메서드' 혹은 '상수
변수가 아닌 정적 필드'를 사용하는 게 아닌 이상은 이루어지지 않을 것입니다. 따라서 아래와 같이 작성해도 지연 초기화처럼 동작합니다.
대부분의 경우 싱글턴에는 공개된 정적 메서드가 getInstance() 하나뿐이므로 그렇게 생각하는 것이 자연스럽습니다.

    
    
    public class Singleton {
    	private static final Singleton INSTANCE = new Singleton();
    
        private Singleton() { }
        
        public static Singleton getInstance() {  
            return INSTANCE;  
        }
    
    	...
    }

만약에 getInstance() 이외의 공개된 정적 메서드가 있다면 Holder 중첩 클래스를 만드는 게 적절하지만 그런 사례를 좀처럼
떠올려 볼 수가 없네요.

###  열거형을 사용하는 방법

이번 방법은 바로 조슈아 블로치(Joshua Bloch)가 이펙티브 자바에서 소개한 열거형을 사용하는 방법입니다. 지금까지 소개한 방법 중에
가장 간결하고 완벽한 방법이며 이 방법을 통해 리플렉션 API를 통해 인스턴스를 만드려는 시도를 손쉽게 무력화할 수 있습니다. 거기에다가
추가적인 노력 없이 직렬화할 수도 있습니다. Enum을 [ 공식 문서
](https://docs.oracle.com/javase/specs/jls/se9/html/jls-8.html#jls-8.9) 에서
살펴보면 다음과 같은 내용을 확인할 수 있습니다.

> 열거형에는 열거형 상수를 통해 정의된 인스턴스 이외의 인스턴스는 없습니다. 열거형을 명시적으로 인스턴스화하려고 시도하면 컴파일 타임
> 에러가 발생합니다. 컴파일 타임 에러 외에도 아래 세 가지 메커니즘이 열거형 상수를 통해 정의된 인스턴스 이외의 열거형 인스턴스가
> 존재하지 않음을 보장합니다.  
>  
>  \- Enum의 final clone() 메서드를 통해 열거 상수를 복제할 수 없음을 보장한다.  
>  (추가: 복제하려고 하면 CloneNotSupportedException 예외를 던진다.)  
>  \- 직렬화 메커니즘을 통한 특수 처리로 역직렬화의 결과로 중복 인스턴스가 생성되지 않음을 보장한다.  
>  \- 리플렉션을 통해 열거형을 인스턴스화하는 것은 금지된다.

조금은 코드가 어색해보일 수 있지만 여태껏 소개한 방법 중에 가장 완벽한 방법입니다. 열거형에서도 이미 봤겠지만 열거형은 다른 클래스를
상속받을 수 없으므로, 클래스 상속이 필요하다면 이 방법은 사용할 수 없으니 참고합시다.

    
    
    public enum Singleton {
    	INSTANCE;
    
    	...
    }

위를 좀 더 익숙한 코드로 바꾸면 실은 아래와 같습니다.

    
    
    // 이 코드는 동작하지 않으니 참고만 하자.
    final class Singleton extends Enum<Singleton> {
    	public static final INSTANCE = new Singleton();
    	...
    }

##  문제점

싱글턴 패턴은 보통 객체의 유일성이 아니라 전역 접근, 즉 어디에서나 접근할 수 있다는 점을 과도하게 오용할 때 문제가 됩니다. 주로 이
패턴은 아래와 같은 문제점을 지니고 있습니다.

####  테스트하기가 어렵다

정적 필드는 한번 할당되면 보통은 프로그램이 종료되기 전까지 계속 살아있게 됩니다. 각 테스트는 독립적, 즉 다른 테스트에 영향을 미치지
않아야 하는데 한 테스트에서 싱글턴 객체가 만들어지면 그 이후의 다른 테스트에서도 이를 확인할 수 있습니다. 또한 일반적으로 인터페이스가
아닌 클래스를 통해 구현되는 싱글턴은 목(mock)으로 대체할 수 없으므로 단위 테스트를 매우 까다롭게 만듭니다. 이를 해결하기 위해서 주로
의존관계 주입(dependency injection, 이하 DI)을 사용할 수 있으며 이때는 보통 DI 프레임워크가 싱글턴 객체의 생성을
제어합니다.

####  데이터 경쟁이 일어나기 쉽다

이는 굳이 싱글턴 패턴이 아니더라도 멀티 스레드 환경에서 공유할 수 있는 상태(쉽게 말해서 필드)를 가지고 있으면 항상 조심해야 하는
내용입니다. 싱글턴이 상태를 가지고 있다면 상황이 더 복잡해지며, 멀티 스레드 환경에서는 공유 변수 접근 시 적절하게 동기화가 이루어지지
않았다면 경쟁 상태(race condition)가 문제가 될 수 있으므로 주의해야 합니다.

####  변경에 취약해진다

어디에서나 접근할 수 있으므로 싱글턴의 구조나 동작에 변경이 일어나면 싱글턴에 의존하고 있는 클래스에서도 역시 문제가 발생합니다. 이렇게
긴밀하게 연결된 관계는 테스트가 어렵다는 문제점으로도 이어집니다.

##  참고


-->

<!--






-->

