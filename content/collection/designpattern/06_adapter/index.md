---
collection_order: 6
title: "[Design Pattern] Adapter - 어댑터 패턴"
description: "Adapter 패턴은 호환되지 않는 인터페이스를 가진 클래스들을 함께 동작하게 하는 구조적 패턴입니다. 기존 코드 수정 없이 인터페이스를 변환하여 재사용성을 높입니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Adapter
  - 어댑터
  - Structural Pattern
  - 구조 패턴
  - GoF
  - Gang of Four
  - Wrapper
  - 래퍼
  - Interface Conversion
  - 인터페이스 변환
  - Compatibility
  - 호환성
  - Legacy Code
  - 레거시 코드
  - Class Adapter
  - 클래스 어댑터
  - Object Adapter
  - 객체 어댑터
  - Target Interface
  - 타겟 인터페이스
  - Adaptee
  - 적응자
  - Integration
  - 통합
  - Third Party Library
  - 서드파티 라이브러리
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
  - Composition
  - 합성
  - Inheritance
  - 상속
  - Delegation
  - 위임
  - API Adapter
  - Plug Adapter
  - 플러그 어댑터
---

어댑터 패턴(Adapter Pattern)은 호환되지 않는 인터페이스를 가진 클래스들이 함께 동작할 수 있도록 중간에서 인터페이스를 변환해주는 구조적 디자인 패턴이다. 마치 해외여행 시 사용하는 전원 어댑터처럼, 서로 다른 인터페이스 사이에서 다리 역할을 수행한다. 이 패턴을 사용하면 기존 코드를 수정하지 않고도 새로운 인터페이스와 호환되도록 만들 수 있어, 레거시 시스템 통합이나 서드파티 라이브러리 활용 시 매우 유용하다.

## 개요

**어댑터 패턴의 정의**

어댑터 패턴은 클라이언트가 기대하는 인터페이스(Target)와 실제로 제공되는 인터페이스(Adaptee) 사이의 불일치를 해결하는 패턴이다. 어댑터는 Adaptee의 인터페이스를 Target 인터페이스로 변환하여, 클라이언트가 Adaptee를 직접 사용하지 않고도 그 기능을 활용할 수 있게 한다.

**패턴의 필요성 및 사용 사례**

어댑터 패턴은 다음과 같은 상황에서 필요하다:

- **레거시 시스템 통합**: 기존 시스템의 인터페이스가 새로운 시스템과 호환되지 않을 때
- **서드파티 라이브러리 활용**: 외부 라이브러리의 인터페이스가 애플리케이션의 인터페이스와 맞지 않을 때
- **인터페이스 표준화**: 여러 클래스가 각기 다른 인터페이스를 가지고 있지만, 동일한 방식으로 사용하고 싶을 때
- **테스트 용이성**: 테스트하기 어려운 외부 의존성을 어댑터로 감싸서 목(Mock) 객체로 대체할 때

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 기존 코드 수정 없이 새로운 인터페이스 지원 | 추가적인 클래스로 인한 복잡성 증가 |
| 단일 책임 원칙 준수 (인터페이스 변환 로직 분리) | 과도한 사용 시 코드 가독성 저하 |
| 개방-폐쇄 원칙 준수 (확장에 열려있음) | 때로는 Adaptee 전체를 수정하는 것이 더 간단할 수 있음 |
| 코드 재사용성 향상 | 양방향 어댑터 구현 시 복잡해질 수 있음 |

## 어댑터 패턴의 구성 요소

어댑터 패턴은 다음과 같은 참여자들로 구성된다:

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Client    │──────▶│   Target    │       │   Adaptee   │
└─────────────┘       └─────────────┘       └─────────────┘
                            △                      │
                            │                      │
                      ┌─────────────┐              │
                      │   Adapter   │──────────────┘
                      └─────────────┘
```

**1. Target (타겟)**
- 클라이언트가 사용하고자 하는 인터페이스를 정의한다.
- 클라이언트는 이 인터페이스를 통해 객체와 상호작용한다.

**2. Adaptee (적응 대상)**
- 이미 존재하는 클래스로, 호환되지 않는 인터페이스를 가지고 있다.
- 어댑터를 통해 Target 인터페이스와 호환되도록 변환된다.

**3. Adapter (어댑터)**
- Target 인터페이스를 구현하고, 내부적으로 Adaptee 인스턴스를 참조한다.
- Target의 메서드 호출을 Adaptee의 메서드 호출로 변환한다.

**4. Client (클라이언트)**
- Target 인터페이스를 사용하여 객체와 상호작용한다.
- Adapter를 통해 간접적으로 Adaptee의 기능을 사용한다.

## 어댑터 패턴의 종류

### 객체 어댑터 (Object Adapter)

객체 어댑터는 **합성(Composition)**을 사용하여 Adaptee 객체를 내부에 포함하고, Target 인터페이스를 구현한다. 이 방식은 더 유연하며, 런타임에 Adaptee를 교체할 수 있다.

```
┌─────────────────────────────────────┐
│           <<interface>>             │
│              Target                 │
├─────────────────────────────────────┤
│ + request()                         │
└─────────────────────────────────────┘
                 △
                 │ implements
┌─────────────────────────────────────┐
│            Adapter                  │
├─────────────────────────────────────┤
│ - adaptee: Adaptee                  │
├─────────────────────────────────────┤
│ + request()                         │
│   └── adaptee.specificRequest()     │
└─────────────────────────────────────┘
                 │
                 │ has-a
                 ▼
┌─────────────────────────────────────┐
│            Adaptee                  │
├─────────────────────────────────────┤
│ + specificRequest()                 │
└─────────────────────────────────────┘
```

### 클래스 어댑터 (Class Adapter)

클래스 어댑터는 **다중 상속**을 사용하여 Target과 Adaptee를 모두 상속받는다. 이 방식은 다중 상속을 지원하는 언어(예: C++)에서만 사용 가능하다.

```
┌─────────────────┐     ┌─────────────────┐
│     Target      │     │     Adaptee     │
├─────────────────┤     ├─────────────────┤
│ + request()     │     │ + specificReq() │
└─────────────────┘     └─────────────────┘
         △                      △
         │                      │
         └──────────┬───────────┘
                    │ extends
           ┌─────────────────┐
           │     Adapter     │
           ├─────────────────┤
           │ + request()     │
           │   └── this.     │
           │   specificReq() │
           └─────────────────┘
```

## 구현 예제

### Python 예제

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod

# Target 인터페이스
class MediaPlayer(ABC):
    """클라이언트가 기대하는 인터페이스"""
    
    @abstractmethod
    def play(self, filename: str) -> None:
        pass

# Adaptee - 호환되지 않는 기존 클래스
class AdvancedMediaPlayer:
    """다양한 포맷을 지원하는 고급 미디어 플레이어"""
    
    def play_vlc(self, filename: str) -> None:
        print(f"Playing VLC file: {filename}")
    
    def play_mp4(self, filename: str) -> None:
        print(f"Playing MP4 file: {filename}")

# Adapter - 객체 어댑터 방식
class MediaAdapter(MediaPlayer):
    """AdvancedMediaPlayer를 MediaPlayer 인터페이스에 맞게 변환"""
    
    def __init__(self, audio_type: str):
        self.advanced_player = AdvancedMediaPlayer()
        self.audio_type = audio_type
    
    def play(self, filename: str) -> None:
        if self.audio_type == "vlc":
            self.advanced_player.play_vlc(filename)
        elif self.audio_type == "mp4":
            self.advanced_player.play_mp4(filename)

# 클라이언트 코드
class AudioPlayer(MediaPlayer):
    """오디오 플레이어 - 클라이언트"""
    
    def play(self, filename: str) -> None:
        # 파일 확장자 추출
        file_extension = filename.split('.')[-1].lower()
        
        if file_extension == "mp3":
            print(f"Playing MP3 file: {filename}")
        elif file_extension in ["vlc", "mp4"]:
            # 어댑터를 통해 재생
            adapter = MediaAdapter(file_extension)
            adapter.play(filename)
        else:
            print(f"Unsupported format: {file_extension}")

# 사용 예제
if __name__ == "__main__":
    player = AudioPlayer()
    
    player.play("song.mp3")      # Playing MP3 file: song.mp3
    player.play("movie.mp4")     # Playing MP4 file: movie.mp4
    player.play("video.vlc")     # Playing VLC file: video.vlc
    player.play("doc.pdf")       # Unsupported format: pdf
```

### Java 예제

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

// Target 인터페이스
interface Duck {
    void quack();
    void fly();
}

// 구체적인 Target 구현
class MallardDuck implements Duck {
    @Override
    public void quack() {
        System.out.println("Quack!");
    }
    
    @Override
    public void fly() {
        System.out.println("I'm flying!");
    }
}

// Adaptee - 호환되지 않는 인터페이스
interface Turkey {
    void gobble();
    void fly();
}

class WildTurkey implements Turkey {
    @Override
    public void gobble() {
        System.out.println("Gobble gobble!");
    }
    
    @Override
    public void fly() {
        System.out.println("I'm flying a short distance!");
    }
}

// Adapter - Turkey를 Duck처럼 사용할 수 있게 변환
class TurkeyAdapter implements Duck {
    private Turkey turkey;
    
    public TurkeyAdapter(Turkey turkey) {
        this.turkey = turkey;
    }
    
    @Override
    public void quack() {
        // Turkey의 gobble을 Duck의 quack으로 변환
        turkey.gobble();
    }
    
    @Override
    public void fly() {
        // Turkey는 짧게 날므로 5번 날아서 Duck처럼 보이게 함
        for (int i = 0; i < 5; i++) {
            turkey.fly();
        }
    }
}

// 클라이언트 코드
public class AdapterDemo {
    public static void testDuck(Duck duck) {
        duck.quack();
        duck.fly();
    }
    
    public static void main(String[] args) {
        // 일반 오리 테스트
        Duck mallardDuck = new MallardDuck();
        System.out.println("=== MallardDuck ===");
        testDuck(mallardDuck);
        
        // 칠면조를 어댑터로 감싸서 오리처럼 사용
        Turkey wildTurkey = new WildTurkey();
        Duck turkeyAdapter = new TurkeyAdapter(wildTurkey);
        System.out.println("\n=== TurkeyAdapter ===");
        testDuck(turkeyAdapter);
    }
}
```

### C# 예제

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;

// Target 인터페이스
public interface ITarget
{
    string GetRequest();
}

// Adaptee - 호환되지 않는 기존 클래스
public class Adaptee
{
    public string GetSpecificRequest()
    {
        return "Specific request from Adaptee";
    }
}

// Adapter - 객체 어댑터
public class Adapter : ITarget
{
    private readonly Adaptee _adaptee;

    public Adapter(Adaptee adaptee)
    {
        _adaptee = adaptee;
    }

    public string GetRequest()
    {
        // Adaptee의 메서드를 호출하고 결과를 변환
        return $"Adapter: (TRANSLATED) {_adaptee.GetSpecificRequest()}";
    }
}

// 실제 사용 예제: XML에서 JSON으로 변환하는 어댑터
public interface IJsonDataProvider
{
    string GetJsonData();
}

public class XmlDataProvider
{
    public string GetXmlData()
    {
        return "<data><name>John</name><age>30</age></data>";
    }
}

public class XmlToJsonAdapter : IJsonDataProvider
{
    private readonly XmlDataProvider _xmlProvider;

    public XmlToJsonAdapter(XmlDataProvider xmlProvider)
    {
        _xmlProvider = xmlProvider;
    }

    public string GetJsonData()
    {
        string xmlData = _xmlProvider.GetXmlData();
        // 실제로는 XML 파싱 후 JSON 변환 로직이 필요
        // 여기서는 간단히 시뮬레이션
        return "{ \"name\": \"John\", \"age\": 30 }";
    }
}

// 클라이언트 코드
public class Program
{
    public static void Main(string[] args)
    {
        // 기본 어댑터 예제
        Adaptee adaptee = new Adaptee();
        ITarget target = new Adapter(adaptee);
        Console.WriteLine(target.GetRequest());

        // XML to JSON 어댑터 예제
        XmlDataProvider xmlProvider = new XmlDataProvider();
        IJsonDataProvider jsonAdapter = new XmlToJsonAdapter(xmlProvider);
        
        Console.WriteLine($"Original XML: {xmlProvider.GetXmlData()}");
        Console.WriteLine($"Converted JSON: {jsonAdapter.GetJsonData()}");
    }
}
```

## 실제 사용 사례

### 1. Java의 InputStreamReader

Java에서 `InputStreamReader`는 바이트 스트림(`InputStream`)을 문자 스트림(`Reader`)으로 변환하는 어댑터이다.

```java
// InputStream(Adaptee)을 Reader(Target)로 변환
InputStream inputStream = new FileInputStream("file.txt");
Reader reader = new InputStreamReader(inputStream, "UTF-8");
BufferedReader bufferedReader = new BufferedReader(reader);
```

### 2. Arrays.asList()

배열을 List 인터페이스로 변환하는 어댑터 역할을 한다.

```java
String[] array = {"a", "b", "c"};
List<String> list = Arrays.asList(array);  // 배열을 List로 어댑팅
```

### 3. Spring Framework의 HandlerAdapter

Spring MVC에서 다양한 형태의 핸들러를 동일한 방식으로 처리할 수 있게 해주는 어댑터이다.

### 4. 레거시 시스템 통합

```python
# 레거시 결제 시스템
class LegacyPaymentSystem:
    def process_payment_legacy(self, amount, currency, account):
        return f"Legacy: Processing {amount} {currency} from {account}"

# 새로운 결제 인터페이스
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, payment_info: dict) -> str:
        pass

# 어댑터
class LegacyPaymentAdapter(PaymentProcessor):
    def __init__(self, legacy_system: LegacyPaymentSystem):
        self.legacy = legacy_system
    
    def pay(self, payment_info: dict) -> str:
        return self.legacy.process_payment_legacy(
            payment_info['amount'],
            payment_info['currency'],
            payment_info['account']
        )
```

## 관련 패턴

| 패턴 | 어댑터와의 관계 |
|------|----------------|
| **Bridge** | 구조는 비슷하지만, Bridge는 설계 단계에서 추상화와 구현을 분리하고, Adapter는 기존 클래스를 호환시키기 위해 사용 |
| **Decorator** | 둘 다 래퍼 역할을 하지만, Decorator는 기능을 추가하고, Adapter는 인터페이스를 변환 |
| **Proxy** | 둘 다 다른 객체를 감싸지만, Proxy는 동일한 인터페이스를 유지하면서 접근을 제어 |
| **Facade** | Adapter는 하나의 인터페이스를 변환하고, Facade는 여러 인터페이스를 단순화 |

## FAQ

**Q1: 객체 어댑터와 클래스 어댑터 중 어떤 것을 선택해야 하나요?**

대부분의 경우 객체 어댑터를 권장합니다. 객체 어댑터는 합성을 사용하므로 더 유연하고, 대부분의 언어에서 지원됩니다. 클래스 어댑터는 다중 상속이 필요하며, Adaptee의 서브클래스도 함께 어댑팅할 수 없습니다.

**Q2: 어댑터 패턴과 데코레이터 패턴의 차이점은 무엇인가요?**

어댑터 패턴은 인터페이스를 변환하여 호환성을 제공하는 것이 목적이고, 데코레이터 패턴은 동일한 인터페이스를 유지하면서 기능을 추가하는 것이 목적입니다.

**Q3: 양방향 어댑터란 무엇인가요?**

양방향 어댑터는 두 인터페이스를 모두 구현하여 양쪽 클라이언트 모두에서 사용할 수 있는 어댑터입니다. 구현이 복잡해질 수 있으므로 신중하게 사용해야 합니다.

**Q4: 어댑터를 사용하면 성능에 영향이 있나요?**

어댑터는 추가적인 간접 호출을 발생시키므로 약간의 오버헤드가 있을 수 있습니다. 그러나 대부분의 경우 이 오버헤드는 무시할 수 있을 정도로 작습니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- Refactoring Guru - Adapter Pattern