---
collection_order: 12
title: "[Design Pattern] Proxy - 프록시 패턴"
description: "Proxy 패턴은 객체에 대한 접근을 제어하기 위해 대리자 객체를 제공합니다. 프록시를 통해 접근 제어, 로깅, 지연 로딩 등 부가 기능을 손쉽게 추가할 수 있습니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Proxy
  - 프록시
  - Structural Pattern
  - 구조 패턴
  - GoF
  - Gang of Four
  - Surrogate
  - 대리자
  - Access Control
  - 접근 제어
  - Lazy Loading
  - 지연 로딩
  - Virtual Proxy
  - 가상 프록시
  - Remote Proxy
  - 원격 프록시
  - Protection Proxy
  - 보호 프록시
  - Caching Proxy
  - 캐싱 프록시
  - Logging
  - 로깅
  - Security
  - 보안
  - Smart Reference
  - 스마트 참조
  - Placeholder
  - 플레이스홀더
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
  - Dynamic Proxy
  - 동적 프록시
  - AOP
  - 관점 지향 프로그래밍
  - Spring Proxy
  - JDK Proxy
---

프록시 패턴(Proxy Pattern)은 다른 객체에 대한 접근을 제어하기 위해 대리자(Surrogate) 또는 플레이스홀더 역할을 하는 객체를 제공하는 구조적 디자인 패턴이다. 실제 객체를 직접 참조하는 대신 프록시 객체를 통해 간접적으로 접근함으로써, 접근 제어, 지연 로딩, 로깅, 캐싱 등 다양한 부가 기능을 추가할 수 있다.

## 개요

**프록시 패턴의 정의**

프록시 패턴은 실제 객체(Real Subject)와 동일한 인터페이스를 구현하는 프록시 객체를 통해 실제 객체에 대한 접근을 제어한다. 클라이언트는 프록시와 실제 객체의 차이를 인식하지 못하며, 프록시가 요청을 가로채어 전처리, 후처리 또는 완전히 다른 동작을 수행할 수 있다.

**패턴의 필요성 및 사용 사례**

프록시 패턴은 다음과 같은 상황에서 유용하다:

- **지연 로딩 (Virtual Proxy)**: 무거운 객체의 생성을 실제로 필요할 때까지 지연
- **접근 제어 (Protection Proxy)**: 권한에 따라 객체 접근을 제한
- **원격 객체 접근 (Remote Proxy)**: 원격 서버의 객체를 로컬 객체처럼 사용
- **캐싱 (Caching Proxy)**: 비용이 큰 연산 결과를 캐싱
- **로깅/감사 (Logging Proxy)**: 객체 접근 이력을 기록
- **스마트 참조 (Smart Reference)**: 참조 횟수 추적 등 추가 기능 제공

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 실제 객체 수정 없이 기능 추가 가능 | 응답 지연이 발생할 수 있음 |
| 클라이언트가 객체 존재 여부를 모르게 관리 | 코드 복잡성 증가 |
| 객체 생명주기 관리 가능 | 프록시 추가로 인한 오버헤드 |
| 개방-폐쇄 원칙 준수 | 동적 프록시 사용 시 디버깅이 어려울 수 있음 |

## 프록시 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│         <<interface>>               │
│            Subject                  │
├─────────────────────────────────────┤
│ + request()                         │
└─────────────────────────────────────┘
              △
              │
     ┌────────┴────────┐
     │                 │
┌─────────────┐  ┌─────────────────────────────┐
│ RealSubject │  │          Proxy              │
├─────────────┤  ├─────────────────────────────┤
│ + request() │  │ - realSubject: RealSubject  │
└─────────────┘  ├─────────────────────────────┤
      △          │ + request()                 │
      │          │   ├── // 전처리              │
      └──────────│   ├── realSubject.request() │
                 │   └── // 후처리              │
                 └─────────────────────────────┘
```

**1. Subject (주체)**
- 실제 객체와 프록시가 구현하는 공통 인터페이스
- 클라이언트가 사용하는 인터페이스 정의

**2. RealSubject (실제 주체)**
- 실제 비즈니스 로직을 포함하는 객체
- 프록시가 대신할 원본 객체

**3. Proxy (프록시)**
- RealSubject에 대한 참조를 유지
- Subject 인터페이스를 구현하여 RealSubject 대신 사용됨
- 접근 제어, 캐싱, 지연 로딩 등의 추가 기능 수행

## 프록시의 종류

### 1. 가상 프록시 (Virtual Proxy)
생성 비용이 큰 객체의 생성을 지연시킨다.

### 2. 보호 프록시 (Protection Proxy)
접근 권한에 따라 객체 접근을 제어한다.

### 3. 원격 프록시 (Remote Proxy)
원격 서버의 객체에 대한 로컬 대리자 역할을 한다.

### 4. 캐싱 프록시 (Caching Proxy)
비용이 많이 드는 연산의 결과를 캐싱한다.

### 5. 로깅 프록시 (Logging Proxy)
요청에 대한 로그를 기록한다.

## 구현 예제

### Python 예제 - 이미지 로딩 (가상 프록시)

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
import time

# Subject 인터페이스
class Image(ABC):
    @abstractmethod
    def display(self) -> None:
        pass
    
    @abstractmethod
    def get_filename(self) -> str:
        pass

# RealSubject - 실제 이미지 클래스
class RealImage(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._load_from_disk()
    
    def _load_from_disk(self) -> None:
        """디스크에서 이미지를 로드하는 무거운 작업"""
        print(f"Loading image from disk: {self._filename}")
        time.sleep(2)  # 로딩 시간 시뮬레이션
        print(f"Image loaded: {self._filename}")
    
    def display(self) -> None:
        print(f"Displaying image: {self._filename}")
    
    def get_filename(self) -> str:
        return self._filename

# Proxy - 가상 프록시
class ImageProxy(Image):
    def __init__(self, filename: str):
        self._filename = filename
        self._real_image = None  # 지연 로딩
    
    def display(self) -> None:
        """실제로 display가 호출될 때 이미지를 로드"""
        if self._real_image is None:
            self._real_image = RealImage(self._filename)
        self._real_image.display()
    
    def get_filename(self) -> str:
        return self._filename

# 사용 예제
if __name__ == "__main__":
    print("=== 프록시 없이 직접 사용 ===")
    image1 = RealImage("photo1.jpg")  # 즉시 로딩
    print()
    
    print("=== 프록시 사용 ===")
    image2 = ImageProxy("photo2.jpg")  # 로딩 안됨
    print(f"이미지 객체 생성됨: {image2.get_filename()}")
    print("아직 이미지가 로드되지 않았습니다.")
    print()
    
    print("=== 실제 표시 요청 시 ===")
    image2.display()  # 이때 로딩
    print()
    
    print("=== 두 번째 표시 (이미 로드됨) ===")
    image2.display()  # 재로딩 없이 표시
```

### Java 예제 - 접근 제어 (보호 프록시)

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// Subject 인터페이스
interface Document {
    void display();
    void edit(String content);
    String getContent();
}

// RealSubject - 실제 문서
class RealDocument implements Document {
    private String filename;
    private String content;
    
    public RealDocument(String filename) {
        this.filename = filename;
        loadDocument();
    }
    
    private void loadDocument() {
        System.out.println("Loading document: " + filename);
        this.content = "Original content of " + filename;
    }
    
    @Override
    public void display() {
        System.out.println("Document: " + filename);
        System.out.println("Content: " + content);
    }
    
    @Override
    public void edit(String newContent) {
        this.content = newContent;
        System.out.println("Document edited successfully");
    }
    
    @Override
    public String getContent() {
        return content;
    }
}

// 사용자 권한 열거형
enum AccessLevel {
    READ_ONLY,
    READ_WRITE,
    ADMIN
}

// 사용자 클래스
class User {
    private String name;
    private AccessLevel accessLevel;
    
    public User(String name, AccessLevel accessLevel) {
        this.name = name;
        this.accessLevel = accessLevel;
    }
    
    public String getName() { return name; }
    public AccessLevel getAccessLevel() { return accessLevel; }
}

// Proxy - 보호 프록시
class DocumentProxy implements Document {
    private RealDocument realDocument;
    private String filename;
    private User currentUser;
    
    public DocumentProxy(String filename, User user) {
        this.filename = filename;
        this.currentUser = user;
    }
    
    @Override
    public void display() {
        // 읽기는 모든 사용자 허용
        if (realDocument == null) {
            realDocument = new RealDocument(filename);
        }
        System.out.println("[" + currentUser.getName() + "] accessing document...");
        realDocument.display();
    }
    
    @Override
    public void edit(String content) {
        // 쓰기는 READ_WRITE 이상만 허용
        if (currentUser.getAccessLevel() == AccessLevel.READ_ONLY) {
            System.out.println("Access Denied: " + currentUser.getName() + 
                " doesn't have write permission");
            return;
        }
        
        if (realDocument == null) {
            realDocument = new RealDocument(filename);
        }
        System.out.println("[" + currentUser.getName() + "] editing document...");
        realDocument.edit(content);
    }
    
    @Override
    public String getContent() {
        if (realDocument == null) {
            realDocument = new RealDocument(filename);
        }
        return realDocument.getContent();
    }
}

// 사용 예제
public class ProxyDemo {
    public static void main(String[] args) {
        User admin = new User("Admin", AccessLevel.ADMIN);
        User editor = new User("Editor", AccessLevel.READ_WRITE);
        User viewer = new User("Viewer", AccessLevel.READ_ONLY);
        
        System.out.println("=== Admin User ===");
        Document doc1 = new DocumentProxy("report.txt", admin);
        doc1.display();
        doc1.edit("Admin edited content");
        System.out.println();
        
        System.out.println("=== Editor User ===");
        Document doc2 = new DocumentProxy("report.txt", editor);
        doc2.edit("Editor edited content");
        System.out.println();
        
        System.out.println("=== Viewer User ===");
        Document doc3 = new DocumentProxy("report.txt", viewer);
        doc3.display();
        doc3.edit("Viewer trying to edit");  // 거부됨
    }
}
```

### C# 예제 - 캐싱 프록시

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;
using System.Collections.Generic;
using System.Threading;

// Subject 인터페이스
public interface IWeatherService
{
    WeatherData GetWeather(string city);
}

// 날씨 데이터 클래스
public class WeatherData
{
    public string City { get; set; }
    public double Temperature { get; set; }
    public string Condition { get; set; }
    public DateTime Timestamp { get; set; }
    
    public override string ToString()
    {
        return $"{City}: {Temperature}°C, {Condition} (조회: {Timestamp:HH:mm:ss})";
    }
}

// RealSubject - 실제 날씨 서비스 (외부 API 호출 시뮬레이션)
public class RealWeatherService : IWeatherService
{
    public WeatherData GetWeather(string city)
    {
        Console.WriteLine($"[RealWeatherService] {city}의 날씨 정보를 외부 API에서 가져오는 중...");
        Thread.Sleep(2000); // API 호출 시간 시뮬레이션
        
        // 시뮬레이션 데이터 반환
        Random random = new Random();
        return new WeatherData
        {
            City = city,
            Temperature = Math.Round(random.NextDouble() * 30, 1),
            Condition = new[] { "맑음", "흐림", "비", "눈" }[random.Next(4)],
            Timestamp = DateTime.Now
        };
    }
}

// Proxy - 캐싱 프록시
public class CachingWeatherProxy : IWeatherService
{
    private readonly IWeatherService _realService;
    private readonly Dictionary<string, WeatherData> _cache;
    private readonly TimeSpan _cacheExpiration;
    
    public CachingWeatherProxy(TimeSpan cacheExpiration)
    {
        _realService = new RealWeatherService();
        _cache = new Dictionary<string, WeatherData>();
        _cacheExpiration = cacheExpiration;
    }
    
    public WeatherData GetWeather(string city)
    {
        // 캐시 확인
        if (_cache.TryGetValue(city, out WeatherData cachedData))
        {
            // 캐시 만료 확인
            if (DateTime.Now - cachedData.Timestamp < _cacheExpiration)
            {
                Console.WriteLine($"[CachingProxy] 캐시에서 {city} 날씨 정보 반환");
                return cachedData;
            }
            else
            {
                Console.WriteLine($"[CachingProxy] {city} 캐시 만료, 새로 조회");
                _cache.Remove(city);
            }
        }
        else
        {
            Console.WriteLine($"[CachingProxy] {city} 캐시 없음, 새로 조회");
        }
        
        // 실제 서비스 호출
        WeatherData weatherData = _realService.GetWeather(city);
        
        // 캐시에 저장
        _cache[city] = weatherData;
        Console.WriteLine($"[CachingProxy] {city} 날씨 정보 캐시됨");
        
        return weatherData;
    }
}

// 로깅 프록시 (데코레이터 패턴과 결합 가능)
public class LoggingWeatherProxy : IWeatherService
{
    private readonly IWeatherService _wrappedService;
    
    public LoggingWeatherProxy(IWeatherService service)
    {
        _wrappedService = service;
    }
    
    public WeatherData GetWeather(string city)
    {
        Console.WriteLine($"[LOG {DateTime.Now:HH:mm:ss}] GetWeather 호출: {city}");
        
        var startTime = DateTime.Now;
        var result = _wrappedService.GetWeather(city);
        var elapsed = DateTime.Now - startTime;
        
        Console.WriteLine($"[LOG {DateTime.Now:HH:mm:ss}] GetWeather 완료: {elapsed.TotalMilliseconds}ms");
        
        return result;
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        // 캐싱 프록시 생성 (5초 캐시)
        IWeatherService weatherService = new CachingWeatherProxy(TimeSpan.FromSeconds(5));
        
        // 로깅 프록시로 감싸기
        weatherService = new LoggingWeatherProxy(weatherService);
        
        Console.WriteLine("=== 첫 번째 조회 (캐시 없음) ===");
        Console.WriteLine(weatherService.GetWeather("서울"));
        Console.WriteLine();
        
        Console.WriteLine("=== 두 번째 조회 (캐시 히트) ===");
        Console.WriteLine(weatherService.GetWeather("서울"));
        Console.WriteLine();
        
        Console.WriteLine("=== 다른 도시 조회 ===");
        Console.WriteLine(weatherService.GetWeather("부산"));
        Console.WriteLine();
        
        Console.WriteLine("=== 5초 대기 후 재조회 (캐시 만료) ===");
        Thread.Sleep(5500);
        Console.WriteLine(weatherService.GetWeather("서울"));
    }
}
```

## 실제 사용 사례

### 1. Java의 동적 프록시 (java.lang.reflect.Proxy)

```java
// 런타임에 프록시 생성
MyInterface proxy = (MyInterface) Proxy.newProxyInstance(
    MyInterface.class.getClassLoader(),
    new Class<?>[] { MyInterface.class },
    new MyInvocationHandler(realObject)
);
```

### 2. Spring AOP

Spring은 프록시 패턴을 사용하여 트랜잭션, 보안, 로깅 등의 횡단 관심사를 처리한다.

```java
@Transactional  // 프록시가 트랜잭션 처리
public void saveData(Data data) {
    repository.save(data);
}
```

### 3. Hibernate의 Lazy Loading

연관된 엔티티를 실제로 접근할 때까지 로딩을 지연한다.

```java
@OneToMany(fetch = FetchType.LAZY)  // 프록시로 지연 로딩
private List<Order> orders;
```

### 4. JavaScript의 Proxy 객체

```javascript
const handler = {
    get: function(obj, prop) {
        console.log(`Accessing property: ${prop}`);
        return obj[prop];
    }
};
const proxy = new Proxy(target, handler);
```

## 관련 패턴

| 패턴 | 프록시와의 관계 |
|------|---------------|
| **Decorator** | 둘 다 래퍼이지만, Decorator는 기능 추가, Proxy는 접근 제어가 주 목적 |
| **Adapter** | Adapter는 인터페이스 변환, Proxy는 동일 인터페이스 유지 |
| **Facade** | Facade는 복잡성 숨김, Proxy는 접근 제어와 부가 기능 |

## FAQ

**Q1: 프록시 패턴과 데코레이터 패턴의 차이점은 무엇인가요?**

프록시는 객체에 대한 접근을 제어하고, 데코레이터는 객체에 새로운 기능을 추가합니다. 프록시는 객체의 생명주기를 관리할 수 있지만, 데코레이터는 이미 존재하는 객체에 기능을 더합니다.

**Q2: 언제 동적 프록시를 사용해야 하나요?**

컴파일 타임에 프록시할 클래스를 알 수 없거나, 많은 인터페이스에 대해 유사한 프록시 로직을 적용해야 할 때 동적 프록시가 유용합니다.

**Q3: 프록시가 성능에 미치는 영향은 어떤가요?**

프록시는 추가적인 간접 호출 오버헤드가 있지만, 캐싱 프록시나 가상 프록시의 경우 오히려 성능을 향상시킬 수 있습니다.

**Q4: 스마트 참조 프록시란 무엇인가요?**

실제 객체에 대한 참조 횟수를 추적하거나, 참조 시 추가 작업(락 획득, 영속성 저장 등)을 수행하는 프록시입니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Spring Framework AOP 문서
- Java Reflection API 문서