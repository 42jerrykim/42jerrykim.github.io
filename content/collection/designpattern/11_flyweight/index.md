---
collection_order: 11
title: "[Design Pattern] Flyweight - 플라이웨이트 패턴"
description: "Flyweight 패턴은 대량의 객체를 효율적으로 관리하고 메모리 사용량을 줄이기 위해 객체 공유를 활용합니다. 동일 데이터의 중복을 최소화하여 성능을 최적화합니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Flyweight
  - 플라이웨이트
  - Structural Pattern
  - 구조 패턴
  - GoF
  - Gang of Four
  - Memory Optimization
  - 메모리 최적화
  - Object Sharing
  - 객체 공유
  - Intrinsic State
  - 내재 상태
  - Extrinsic State
  - 외재 상태
  - Object Pool
  - 객체 풀
  - Cache
  - 캐시
  - Performance
  - 성능
  - Immutable
  - 불변
  - Factory
  - 팩토리
  - HashMap
  - 해시맵
  - String Pool
  - 문자열 풀
  - Integer Cache
  - 정수 캐시
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
  - Game Development
  - 게임 개발
  - Graphics
  - 그래픽
  - Text Editor
  - 텍스트 에디터
---

플라이웨이트 패턴(Flyweight Pattern)은 대량의 유사한 객체를 효율적으로 관리하기 위해 객체 공유를 활용하는 구조적 디자인 패턴이다. 이 패턴은 각 객체에 모든 데이터를 유지하는 대신, 여러 객체가 공유할 수 있는 상태(내재 상태)와 객체마다 다른 상태(외재 상태)를 분리하여 메모리 사용량을 크게 줄인다.

## 개요

**플라이웨이트 패턴의 정의**

플라이웨이트 패턴은 많은 수의 유사한 객체를 생성해야 할 때, 공유 가능한 부분을 별도의 객체로 분리하여 재사용함으로써 메모리 효율성을 높이는 패턴이다. "플라이웨이트(경량)"라는 이름처럼, 객체를 가볍게 만드는 것이 목적이다.

**내재 상태와 외재 상태**

- **내재 상태 (Intrinsic State)**: 객체 내부에 저장되며 여러 객체가 공유할 수 있는 불변 데이터
- **외재 상태 (Extrinsic State)**: 객체 외부에서 전달되며 각 상황에 따라 달라지는 데이터

**패턴의 필요성 및 사용 사례**

플라이웨이트 패턴은 다음과 같은 상황에서 유용하다:

- **대량의 유사 객체**: 수천~수백만 개의 유사한 객체가 필요할 때
- **메모리 제약**: 메모리 사용량이 중요한 환경에서
- **공유 가능한 상태**: 객체의 상태 중 상당 부분이 공유 가능할 때
- **객체 정체성 불필요**: 객체의 고유 식별이 필요하지 않을 때

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 메모리 사용량 대폭 감소 | 코드 복잡성 증가 |
| 성능 향상 가능 | 상태 분리 비용 (외재 상태 전달) |
| 객체 생성 비용 절감 | 플라이웨이트가 불변이어야 함 |
| 캐싱 활용 가능 | 모든 상황에 적합하지 않음 |

## 플라이웨이트 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│         FlyweightFactory            │
├─────────────────────────────────────┤
│ - flyweights: Map<key, Flyweight>   │
├─────────────────────────────────────┤
│ + getFlyweight(key): Flyweight      │
└─────────────────────────────────────┘
              │
              │ creates/manages
              ▼
┌─────────────────────────────────────┐
│       <<interface>>                 │
│          Flyweight                  │
├─────────────────────────────────────┤
│ + operation(extrinsicState)         │
└─────────────────────────────────────┘
              △
              │
     ┌────────┴────────┐
     │                 │
┌───────────────┐  ┌───────────────┐
│ Concrete      │  │ Unshared      │
│ Flyweight     │  │ Flyweight     │
├───────────────┤  ├───────────────┤
│ intrinsicState│  │ allState      │
├───────────────┤  ├───────────────┤
│ +operation()  │  │ +operation()  │
└───────────────┘  └───────────────┘
```

**1. Flyweight (플라이웨이트)**
- 공유 가능한 인터페이스 정의
- 내재 상태 저장 및 외재 상태를 매개변수로 받음

**2. ConcreteFlyweight (구체적 플라이웨이트)**
- 내재 상태를 저장하는 공유 가능한 객체
- 반드시 불변(immutable)이어야 함

**3. UnsharedConcreteFlyweight (비공유 플라이웨이트)**
- 공유되지 않는 플라이웨이트 (선택적)
- 모든 상태를 내부에 저장

**4. FlyweightFactory (플라이웨이트 팩토리)**
- 플라이웨이트 객체 생성 및 관리
- 이미 존재하는 플라이웨이트 반환 (캐싱)

## 구현 예제

### Python 예제 - 텍스트 에디터의 문자

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from typing import Dict
import sys

# Flyweight - 문자 스타일 (내재 상태)
class CharacterStyle:
    """공유되는 문자 스타일 (폰트, 크기, 색상)"""
    
    def __init__(self, font: str, size: int, color: str):
        self._font = font
        self._size = size
        self._color = color
    
    def render(self, char: str, x: int, y: int) -> None:
        """문자를 화면에 렌더링 (x, y는 외재 상태)"""
        print(f"'{char}' at ({x}, {y}) - {self._font}, {self._size}pt, {self._color}")
    
    @property
    def font(self) -> str:
        return self._font
    
    @property
    def size(self) -> int:
        return self._size
    
    @property
    def color(self) -> str:
        return self._color

# FlyweightFactory
class StyleFactory:
    """문자 스타일을 생성하고 캐싱하는 팩토리"""
    
    _styles: Dict[str, CharacterStyle] = {}
    
    @classmethod
    def get_style(cls, font: str, size: int, color: str) -> CharacterStyle:
        key = f"{font}_{size}_{color}"
        
        if key not in cls._styles:
            cls._styles[key] = CharacterStyle(font, size, color)
            print(f"Created new style: {key}")
        
        return cls._styles[key]
    
    @classmethod
    def get_style_count(cls) -> int:
        return len(cls._styles)

# 문자 클래스 (외재 상태 포함)
class Character:
    """문서 내의 문자"""
    
    def __init__(self, char: str, style: CharacterStyle, x: int, y: int):
        self._char = char
        self._style = style  # 플라이웨이트 참조
        self._x = x          # 외재 상태
        self._y = y          # 외재 상태
    
    def render(self) -> None:
        self._style.render(self._char, self._x, self._y)

# 문서 클래스
class Document:
    """문서"""
    
    def __init__(self):
        self._characters = []
    
    def add_character(self, char: str, font: str, size: int, color: str, x: int, y: int) -> None:
        style = StyleFactory.get_style(font, size, color)
        self._characters.append(Character(char, style, x, y))
    
    def render(self) -> None:
        for char in self._characters:
            char.render()
    
    def get_character_count(self) -> int:
        return len(self._characters)

# 메모리 사용량 비교
def calculate_memory_without_flyweight(char_count: int) -> int:
    """플라이웨이트 없이 각 문자가 모든 정보를 가질 때"""
    # 문자(1) + 폰트이름(20) + 크기(4) + 색상(10) + x(4) + y(4) = ~43 bytes
    return char_count * 43

def calculate_memory_with_flyweight(char_count: int, style_count: int) -> int:
    """플라이웨이트 사용 시"""
    # 각 스타일: 폰트이름(20) + 크기(4) + 색상(10) = ~34 bytes
    # 각 문자: 문자(1) + 스타일참조(8) + x(4) + y(4) = ~17 bytes
    return (style_count * 34) + (char_count * 17)

# 사용 예제
if __name__ == "__main__":
    doc = Document()
    
    # 문서에 텍스트 추가 (같은 스타일은 공유됨)
    text = "Hello, Flyweight Pattern!"
    x, y = 0, 0
    
    for char in text:
        if char.isupper():
            doc.add_character(char, "Arial Bold", 14, "blue", x, y)
        elif char.islower():
            doc.add_character(char, "Arial", 12, "black", x, y)
        else:
            doc.add_character(char, "Arial", 12, "gray", x, y)
        x += 10
    
    print(f"\n=== 문서 렌더링 ===")
    doc.render()
    
    print(f"\n=== 통계 ===")
    print(f"총 문자 수: {doc.get_character_count()}")
    print(f"생성된 스타일 수: {StyleFactory.get_style_count()}")
    
    print(f"\n=== 메모리 절약 (10,000자 기준) ===")
    char_count = 10000
    without = calculate_memory_without_flyweight(char_count)
    with_fw = calculate_memory_with_flyweight(char_count, StyleFactory.get_style_count())
    saved = without - with_fw
    print(f"플라이웨이트 미사용: {without:,} bytes")
    print(f"플라이웨이트 사용: {with_fw:,} bytes")
    print(f"절약: {saved:,} bytes ({(saved/without)*100:.1f}%)")
```

### Java 예제 - 게임의 나무 (Tree)

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// Flyweight - 나무 타입 (내재 상태)
class TreeType {
    private String name;
    private String color;
    private String texture;
    
    public TreeType(String name, String color, String texture) {
        this.name = name;
        this.color = color;
        this.texture = texture;
    }
    
    public void draw(int x, int y) {
        // 실제로는 텍스처를 사용해 렌더링
        System.out.printf("%s 나무 at (%d, %d) - 색상: %s%n", name, x, y, color);
    }
    
    public String getName() { return name; }
}

// FlyweightFactory - 나무 타입 팩토리
class TreeTypeFactory {
    private static Map<String, TreeType> treeTypes = new HashMap<>();
    
    public static TreeType getTreeType(String name, String color, String texture) {
        String key = name + "_" + color + "_" + texture;
        
        if (!treeTypes.containsKey(key)) {
            treeTypes.put(key, new TreeType(name, color, texture));
            System.out.println("새 TreeType 생성: " + key);
        }
        
        return treeTypes.get(key);
    }
    
    public static int getTypeCount() {
        return treeTypes.size();
    }
}

// 개별 나무 (외재 상태 포함)
class Tree {
    private int x;          // 외재 상태
    private int y;          // 외재 상태
    private TreeType type;  // 플라이웨이트 참조
    
    public Tree(int x, int y, TreeType type) {
        this.x = x;
        this.y = y;
        this.type = type;
    }
    
    public void draw() {
        type.draw(x, y);
    }
}

// 숲 클래스
class Forest {
    private List<Tree> trees = new ArrayList<>();
    
    public void plantTree(int x, int y, String name, String color, String texture) {
        TreeType type = TreeTypeFactory.getTreeType(name, color, texture);
        Tree tree = new Tree(x, y, type);
        trees.add(tree);
    }
    
    public void draw() {
        for (Tree tree : trees) {
            tree.draw();
        }
    }
    
    public int getTreeCount() {
        return trees.size();
    }
}

// 사용 예제
public class FlyweightDemo {
    public static void main(String[] args) {
        Forest forest = new Forest();
        Random random = new Random();
        
        // 대량의 나무 심기
        String[] treeNames = {"소나무", "참나무", "단풍나무"};
        String[] colors = {"녹색", "진녹색", "황록색"};
        String[] textures = {"pine.png", "oak.png", "maple.png"};
        
        System.out.println("=== 나무 심기 ===");
        for (int i = 0; i < 20; i++) {
            int x = random.nextInt(100);
            int y = random.nextInt(100);
            int typeIndex = random.nextInt(3);
            
            forest.plantTree(x, y, 
                treeNames[typeIndex], 
                colors[typeIndex], 
                textures[typeIndex]);
        }
        
        System.out.println("\n=== 숲 렌더링 ===");
        forest.draw();
        
        System.out.println("\n=== 통계 ===");
        System.out.println("총 나무 수: " + forest.getTreeCount());
        System.out.println("나무 타입 수: " + TreeTypeFactory.getTypeCount());
        
        // 메모리 절약 계산
        long withoutFlyweight = forest.getTreeCount() * (8 + 8 + 100); // x, y, 타입 데이터
        long withFlyweight = forest.getTreeCount() * (8 + 8 + 8)  // x, y, 참조
                           + TreeTypeFactory.getTypeCount() * 100; // 타입당 데이터
        
        System.out.println("\n메모리 사용량 (대략적 계산):");
        System.out.println("플라이웨이트 미사용: " + withoutFlyweight + " bytes");
        System.out.println("플라이웨이트 사용: " + withFlyweight + " bytes");
    }
}
```

### C# 예제 - 총알/파티클 시스템

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;
using System.Collections.Generic;

// Flyweight - 총알 타입 (내재 상태)
public class BulletType
{
    public string Name { get; }
    public string Sprite { get; }  // 스프라이트 이미지 경로
    public int Damage { get; }
    public float Speed { get; }
    
    public BulletType(string name, string sprite, int damage, float speed)
    {
        Name = name;
        Sprite = sprite;
        Damage = damage;
        Speed = speed;
        Console.WriteLine($"BulletType 생성: {name}");
    }
    
    public void Render(float x, float y, float direction)
    {
        // 실제로는 스프라이트를 해당 위치에 렌더링
        Console.WriteLine($"  [{Name}] 위치({x:F1}, {y:F1}) 방향:{direction:F0}° 데미지:{Damage}");
    }
}

// FlyweightFactory
public class BulletTypeFactory
{
    private static Dictionary<string, BulletType> _bulletTypes = new Dictionary<string, BulletType>();
    
    public static BulletType GetBulletType(string name, string sprite, int damage, float speed)
    {
        string key = $"{name}_{damage}_{speed}";
        
        if (!_bulletTypes.ContainsKey(key))
        {
            _bulletTypes[key] = new BulletType(name, sprite, damage, speed);
        }
        
        return _bulletTypes[key];
    }
    
    public static int TypeCount => _bulletTypes.Count;
}

// 총알 인스턴스 (외재 상태 포함)
public class Bullet
{
    private float _x;           // 외재 상태
    private float _y;           // 외재 상태
    private float _direction;   // 외재 상태
    private BulletType _type;   // 플라이웨이트 참조
    
    public Bullet(float x, float y, float direction, BulletType type)
    {
        _x = x;
        _y = y;
        _direction = direction;
        _type = type;
    }
    
    public void Update(float deltaTime)
    {
        // 총알 이동
        float radians = _direction * (float)Math.PI / 180f;
        _x += (float)Math.Cos(radians) * _type.Speed * deltaTime;
        _y += (float)Math.Sin(radians) * _type.Speed * deltaTime;
    }
    
    public void Render()
    {
        _type.Render(_x, _y, _direction);
    }
}

// 게임 월드
public class GameWorld
{
    private List<Bullet> _bullets = new List<Bullet>();
    private Random _random = new Random();
    
    public void SpawnBullet(string typeName, float x, float y, float direction)
    {
        BulletType type;
        
        switch (typeName)
        {
            case "기본":
                type = BulletTypeFactory.GetBulletType("기본", "bullet_basic.png", 10, 100f);
                break;
            case "화염":
                type = BulletTypeFactory.GetBulletType("화염", "bullet_fire.png", 25, 80f);
                break;
            case "얼음":
                type = BulletTypeFactory.GetBulletType("얼음", "bullet_ice.png", 15, 90f);
                break;
            default:
                type = BulletTypeFactory.GetBulletType("기본", "bullet_basic.png", 10, 100f);
                break;
        }
        
        _bullets.Add(new Bullet(x, y, direction, type));
    }
    
    public void Update(float deltaTime)
    {
        foreach (var bullet in _bullets)
        {
            bullet.Update(deltaTime);
        }
    }
    
    public void Render()
    {
        Console.WriteLine("\n=== 게임 월드 렌더링 ===");
        foreach (var bullet in _bullets)
        {
            bullet.Render();
        }
    }
    
    public int BulletCount => _bullets.Count;
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        GameWorld world = new GameWorld();
        Random random = new Random();
        
        Console.WriteLine("=== 총알 생성 ===\n");
        
        // 대량의 총알 생성
        string[] bulletTypes = { "기본", "화염", "얼음", "기본", "화염" };
        
        for (int i = 0; i < 15; i++)
        {
            string type = bulletTypes[random.Next(bulletTypes.Length)];
            float x = (float)random.NextDouble() * 100;
            float y = (float)random.NextDouble() * 100;
            float dir = (float)random.NextDouble() * 360;
            
            world.SpawnBullet(type, x, y, dir);
        }
        
        world.Render();
        
        Console.WriteLine("\n=== 통계 ===");
        Console.WriteLine($"총 총알 수: {world.BulletCount}");
        Console.WriteLine($"총알 타입 수: {BulletTypeFactory.TypeCount}");
        
        // 메모리 절약 분석
        int bulletCount = world.BulletCount;
        int typeCount = BulletTypeFactory.TypeCount;
        
        // 플라이웨이트 미사용: 각 총알이 모든 데이터 보유
        long withoutFlyweight = bulletCount * (4 + 4 + 4 + 100 + 4 + 4); // x, y, dir, sprite경로, damage, speed
        
        // 플라이웨이트 사용: 타입 공유
        long withFlyweight = bulletCount * (4 + 4 + 4 + 8) + typeCount * (100 + 4 + 4);
        
        Console.WriteLine($"\n메모리 사용량 비교 (추정):");
        Console.WriteLine($"플라이웨이트 미사용: {withoutFlyweight:N0} bytes");
        Console.WriteLine($"플라이웨이트 사용: {withFlyweight:N0} bytes");
        Console.WriteLine($"절약: {withoutFlyweight - withFlyweight:N0} bytes ({(1 - (double)withFlyweight / withoutFlyweight) * 100:F1}%)");
    }
}
```

## 실제 사용 사례

### 1. Java String Pool
```java
// 문자열 리터럴은 String Pool에서 공유됨
String s1 = "Hello";
String s2 = "Hello";
System.out.println(s1 == s2);  // true - 같은 객체
```

### 2. Java Integer Cache
```java
// -128 ~ 127 범위의 Integer는 캐싱됨
Integer i1 = 100;
Integer i2 = 100;
System.out.println(i1 == i2);  // true - 같은 객체
```

### 3. 게임 개발
파티클 시스템, 총알, NPC 등 대량의 유사한 객체를 효율적으로 관리

### 4. 텍스트 에디터
문자별 포맷팅 정보를 공유하여 메모리 절약

## 관련 패턴

| 패턴 | 플라이웨이트와의 관계 |
|------|---------------------|
| **Composite** | Composite의 Leaf 노드를 플라이웨이트로 구현 |
| **Factory** | 플라이웨이트 객체 생성과 캐싱 관리에 사용 |
| **Singleton** | 플라이웨이트 팩토리가 싱글턴일 수 있음 |
| **State/Strategy** | 상태/전략 객체를 플라이웨이트로 공유 가능 |

## FAQ

**Q1: 플라이웨이트 객체는 왜 불변이어야 하나요?**

여러 클라이언트가 동시에 같은 플라이웨이트를 참조하므로, 한 곳에서 상태를 변경하면 모든 참조에 영향을 미칩니다. 불변 객체로 만들어 이런 부작용을 방지합니다.

**Q2: 플라이웨이트 패턴을 사용하면 항상 메모리가 절약되나요?**

아닙니다. 객체 수가 적거나 공유 가능한 상태가 적으면 오히려 팩토리 관리 비용이 더 클 수 있습니다. 대량의 유사 객체가 있을 때만 효과적입니다.

**Q3: 외재 상태를 매번 전달하는 것이 비효율적이지 않나요?**

상황에 따라 다릅니다. 메모리 절약이 연산 비용보다 중요한 경우에 플라이웨이트가 적합합니다. 외재 상태 전달 비용을 최소화하도록 설계해야 합니다.

**Q4: 스레드 안전성은 어떻게 보장하나요?**

플라이웨이트가 불변이면 본질적으로 스레드 안전합니다. 팩토리의 캐시 접근은 동기화가 필요할 수 있습니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Java String Pool 문서
- Game Programming Patterns (Robert Nystrom)