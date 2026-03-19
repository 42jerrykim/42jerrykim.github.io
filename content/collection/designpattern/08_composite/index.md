---
collection_order: 8
title: "[Design Pattern] Composite - 컴포지트 패턴"
description: "Composite 패턴은 객체들을 트리 구조로 구성하여 부분-전체 계층을 표현합니다. 단일 객체와 복합 객체를 동일하게 다루어 재귀적 처리를 단순화하는 구조 패턴입니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design-Pattern
  - 디자인패턴
  - GoF
  - Software-Architecture
  - 재귀
  - Code-Quality
  - 코드품질
  - 소프트웨어아키텍처
  - OOP
  - 객체지향
  - Java
  - C++
  - Python
  - CSharp
  - Iterator
  - Git
  - GitHub
  - Implementation
  - 구현
  - Tree
  - Recursion
  - Windows
  - File-System
  - Linux
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Refactoring
  - 리팩토링
  - Documentation
  - 문서화
  - Interface
  - 인터페이스
  - Abstraction
  - 추상화
  - SOLID
  - Encapsulation
  - 캡슐화
  - Polymorphism
  - 다형성
  - Composition
  - 합성
  - Dependency-Injection
  - 의존성주입
  - Testing
  - 테스트
  - Performance
  - 성능
  - Education
  - 교육
---

컴포지트 패턴(Composite Pattern)은 객체들을 트리 구조로 구성하여 부분-전체 계층을 표현하는 구조적 디자인 패턴이다. 이 패턴을 사용하면 클라이언트가 단일 객체(Leaf)와 복합 객체(Composite)를 동일하게 다룰 수 있어, 재귀적 구조를 단순하고 일관되게 처리할 수 있다.

## 개요

**컴포지트 패턴의 정의**

컴포지트 패턴은 개별 객체와 복합 객체를 같은 타입으로 취급하여, 동일한 인터페이스를 통해 다룰 수 있게 한다. 트리 구조로 이루어진 계층적 데이터를 처리할 때 특히 유용하며, 클라이언트는 전체 구조를 신경 쓰지 않고 동일한 방식으로 모든 요소를 처리할 수 있다.

**패턴의 필요성 및 사용 사례**

컴포지트 패턴은 다음과 같은 상황에서 유용하다:

- **파일 시스템**: 파일과 폴더를 동일하게 취급
- **GUI 컴포넌트**: 버튼, 패널, 윈도우 등을 계층적으로 구성
- **조직 구조**: 직원과 부서를 트리 형태로 표현
- **메뉴 시스템**: 메뉴 항목과 서브메뉴를 동일하게 처리
- **그래픽 편집기**: 기본 도형과 그룹화된 도형을 동일하게 다룸

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 단일/복합 객체를 동일하게 처리 | 지나치게 일반적인 설계가 될 수 있음 |
| 새로운 종류의 컴포넌트 추가 용이 | 컴포넌트 타입 제한이 어려움 |
| 재귀적 구조 처리 단순화 | 공통 인터페이스 설계가 어려울 수 있음 |
| 클라이언트 코드 단순화 | Leaf에서 불필요한 메서드 구현 필요 |

## 컴포지트 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│         <<interface>>               │
│           Component                 │
├─────────────────────────────────────┤
│ + operation()                       │
│ + add(Component)                    │
│ + remove(Component)                 │
│ + getChild(int)                     │
└─────────────────────────────────────┘
              △
              │
     ┌────────┴────────┐
     │                 │
┌─────────────┐  ┌─────────────────────────────┐
│    Leaf     │  │        Composite            │
├─────────────┤  ├─────────────────────────────┤
│ +operation()│  │ - children: List<Component> │
└─────────────┘  ├─────────────────────────────┤
                 │ + operation()               │
                 │   └── for child in children │
                 │       child.operation()     │
                 │ + add(Component)            │
                 │ + remove(Component)         │
                 │ + getChild(int)             │
                 └─────────────────────────────┘
```

**1. Component (컴포넌트)**
- 모든 객체(Leaf와 Composite)의 공통 인터페이스 정의
- 기본 동작과 자식 관리 메서드 선언
- 필요에 따라 기본 구현 제공

**2. Leaf (리프)**
- 더 이상 자식이 없는 말단 객체
- Component 인터페이스의 실제 동작 구현
- 자식 관리 메서드는 보통 빈 구현이거나 예외 발생

**3. Composite (컴포지트)**
- 자식 컴포넌트를 포함하는 복합 객체
- 자식 추가/제거/조회 메서드 구현
- operation()에서 자식들의 operation()을 재귀적으로 호출

## 구현 예제

### Python 예제 - 파일 시스템

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import List

# Component 추상 클래스
class FileSystemComponent(ABC):
    def __init__(self, name: str):
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name
    
    @abstractmethod
    def get_size(self) -> int:
        """파일/폴더의 크기를 반환"""
        pass
    
    @abstractmethod
    def display(self, indent: int = 0) -> None:
        """구조를 출력"""
        pass
    
    # 자식 관리 메서드 (기본 구현)
    def add(self, component: 'FileSystemComponent') -> None:
        raise NotImplementedError("Cannot add to a file")
    
    def remove(self, component: 'FileSystemComponent') -> None:
        raise NotImplementedError("Cannot remove from a file")
    
    def get_child(self, index: int) -> 'FileSystemComponent':
        raise NotImplementedError("Cannot get child from a file")

# Leaf - 파일
class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size
    
    def get_size(self) -> int:
        return self._size
    
    def display(self, indent: int = 0) -> None:
        print("  " * indent + f"📄 {self._name} ({self._size} bytes)")

# Composite - 폴더
class Folder(FileSystemComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[FileSystemComponent] = []
    
    def get_size(self) -> int:
        """폴더 내 모든 파일의 크기 합계"""
        total = 0
        for child in self._children:
            total += child.get_size()
        return total
    
    def display(self, indent: int = 0) -> None:
        print("  " * indent + f"📁 {self._name}/ ({self.get_size()} bytes)")
        for child in self._children:
            child.display(indent + 1)
    
    def add(self, component: FileSystemComponent) -> None:
        self._children.append(component)
    
    def remove(self, component: FileSystemComponent) -> None:
        self._children.remove(component)
    
    def get_child(self, index: int) -> FileSystemComponent:
        return self._children[index]
    
    @property
    def children(self) -> List[FileSystemComponent]:
        return self._children.copy()

# 사용 예제
if __name__ == "__main__":
    # 파일 시스템 구조 생성
    root = Folder("root")
    
    # 문서 폴더
    documents = Folder("documents")
    documents.add(File("resume.docx", 25000))
    documents.add(File("report.pdf", 150000))
    
    # 사진 폴더
    photos = Folder("photos")
    photos.add(File("vacation.jpg", 3500000))
    photos.add(File("family.png", 2800000))
    
    # 하위 폴더
    screenshots = Folder("screenshots")
    screenshots.add(File("screen1.png", 500000))
    screenshots.add(File("screen2.png", 450000))
    photos.add(screenshots)
    
    # 루트에 추가
    root.add(documents)
    root.add(photos)
    root.add(File("readme.txt", 1500))
    
    # 전체 구조 출력
    print("=== 파일 시스템 구조 ===")
    root.display()
    
    print(f"\n총 크기: {root.get_size():,} bytes")
```

### Java 예제 - 조직 구조

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.ArrayList;
import java.util.List;

// Component 인터페이스
interface OrganizationComponent {
    String getName();
    double getSalary();
    void display(int indent);
}

// Leaf - 직원
class Employee implements OrganizationComponent {
    private String name;
    private String position;
    private double salary;
    
    public Employee(String name, String position, double salary) {
        this.name = name;
        this.position = position;
        this.salary = salary;
    }
    
    @Override
    public String getName() {
        return name;
    }
    
    @Override
    public double getSalary() {
        return salary;
    }
    
    @Override
    public void display(int indent) {
        String indentStr = "  ".repeat(indent);
        System.out.println(indentStr + "👤 " + name + " (" + position + ") - $" + salary);
    }
}

// Composite - 부서
class Department implements OrganizationComponent {
    private String name;
    private List<OrganizationComponent> members = new ArrayList<>();
    
    public Department(String name) {
        this.name = name;
    }
    
    @Override
    public String getName() {
        return name;
    }
    
    @Override
    public double getSalary() {
        return members.stream()
                     .mapToDouble(OrganizationComponent::getSalary)
                     .sum();
    }
    
    @Override
    public void display(int indent) {
        String indentStr = "  ".repeat(indent);
        System.out.println(indentStr + "🏢 " + name + " (총 급여: $" + getSalary() + ")");
        for (OrganizationComponent member : members) {
            member.display(indent + 1);
        }
    }
    
    public void add(OrganizationComponent component) {
        members.add(component);
    }
    
    public void remove(OrganizationComponent component) {
        members.remove(component);
    }
    
    public OrganizationComponent getChild(int index) {
        return members.get(index);
    }
}

// 사용 예제
public class CompositeDemo {
    public static void main(String[] args) {
        // 회사 구조 생성
        Department company = new Department("ABC Corp");
        
        // 개발 부서
        Department development = new Department("Development");
        development.add(new Employee("김철수", "Tech Lead", 120000));
        development.add(new Employee("이영희", "Senior Developer", 95000));
        development.add(new Employee("박지민", "Junior Developer", 65000));
        
        // QA 팀 (개발 부서 하위)
        Department qa = new Department("QA Team");
        qa.add(new Employee("최민수", "QA Lead", 85000));
        qa.add(new Employee("정수연", "QA Engineer", 70000));
        development.add(qa);
        
        // 마케팅 부서
        Department marketing = new Department("Marketing");
        marketing.add(new Employee("한지영", "Marketing Manager", 90000));
        marketing.add(new Employee("오세훈", "Marketing Specialist", 60000));
        
        // 회사에 부서 추가
        company.add(development);
        company.add(marketing);
        company.add(new Employee("강대표", "CEO", 200000));
        
        // 전체 조직 구조 출력
        System.out.println("=== 조직 구조 ===");
        company.display(0);
        
        System.out.println("\n총 급여 지출: $" + company.getSalary());
    }
}
```

### C# 예제 - 메뉴 시스템

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;
using System.Collections.Generic;

// Component 추상 클래스
public abstract class MenuComponent
{
    public string Name { get; protected set; }
    public string Description { get; protected set; }
    
    public abstract void Display(int indent = 0);
    public abstract decimal GetTotalPrice();
    
    // 기본 구현 (Leaf에서는 예외)
    public virtual void Add(MenuComponent component)
    {
        throw new NotSupportedException("Cannot add to a menu item");
    }
    
    public virtual void Remove(MenuComponent component)
    {
        throw new NotSupportedException("Cannot remove from a menu item");
    }
}

// Leaf - 메뉴 항목
public class MenuItem : MenuComponent
{
    public decimal Price { get; private set; }
    public bool IsVegetarian { get; private set; }
    
    public MenuItem(string name, string description, decimal price, bool isVegetarian)
    {
        Name = name;
        Description = description;
        Price = price;
        IsVegetarian = isVegetarian;
    }
    
    public override void Display(int indent = 0)
    {
        string indentStr = new string(' ', indent * 2);
        string veg = IsVegetarian ? " 🌱" : "";
        Console.WriteLine($"{indentStr}• {Name}{veg} - {Price:C}");
        Console.WriteLine($"{indentStr}  {Description}");
    }
    
    public override decimal GetTotalPrice()
    {
        return Price;
    }
}

// Composite - 메뉴 (서브메뉴 포함 가능)
public class Menu : MenuComponent
{
    private List<MenuComponent> _items = new List<MenuComponent>();
    
    public Menu(string name, string description)
    {
        Name = name;
        Description = description;
    }
    
    public override void Add(MenuComponent component)
    {
        _items.Add(component);
    }
    
    public override void Remove(MenuComponent component)
    {
        _items.Remove(component);
    }
    
    public override void Display(int indent = 0)
    {
        string indentStr = new string(' ', indent * 2);
        Console.WriteLine($"{indentStr}📋 {Name}");
        Console.WriteLine($"{indentStr}   {Description}");
        Console.WriteLine($"{indentStr}   " + new string('-', 30));
        
        foreach (var item in _items)
        {
            item.Display(indent + 1);
        }
    }
    
    public override decimal GetTotalPrice()
    {
        decimal total = 0;
        foreach (var item in _items)
        {
            total += item.GetTotalPrice();
        }
        return total;
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        // 전체 메뉴
        Menu allMenus = new Menu("전체 메뉴", "오늘의 모든 메뉴");
        
        // 아침 메뉴
        Menu breakfastMenu = new Menu("아침 메뉴", "아침 7시 - 11시");
        breakfastMenu.Add(new MenuItem("팬케이크", "메이플 시럽과 함께", 8000, true));
        breakfastMenu.Add(new MenuItem("와플", "생크림과 과일 토핑", 9000, true));
        breakfastMenu.Add(new MenuItem("에그 베네딕트", "수란과 홀란다이즈 소스", 12000, false));
        
        // 점심 메뉴
        Menu lunchMenu = new Menu("점심 메뉴", "오전 11시 - 오후 3시");
        lunchMenu.Add(new MenuItem("샐러드", "신선한 야채와 드레싱", 10000, true));
        lunchMenu.Add(new MenuItem("파스타", "크림 파스타", 13000, false));
        lunchMenu.Add(new MenuItem("스테이크", "안심 스테이크", 25000, false));
        
        // 음료 서브메뉴 (점심 메뉴 하위)
        Menu beverageMenu = new Menu("음료", "함께 주문하세요");
        beverageMenu.Add(new MenuItem("아메리카노", "깊은 풍미의 커피", 4500, true));
        beverageMenu.Add(new MenuItem("카페라떼", "부드러운 우유 커피", 5000, true));
        beverageMenu.Add(new MenuItem("오렌지 주스", "100% 착즙 주스", 6000, true));
        lunchMenu.Add(beverageMenu);
        
        // 전체 메뉴에 추가
        allMenus.Add(breakfastMenu);
        allMenus.Add(lunchMenu);
        
        // 메뉴 출력
        Console.WriteLine("=== 레스토랑 메뉴 ===\n");
        allMenus.Display();
        
        Console.WriteLine($"\n전체 메뉴 합계: {allMenus.GetTotalPrice():C}");
    }
}
```

## 실제 사용 사례

### 1. Java Swing/AWT
```java
// JPanel은 Composite, JButton은 Leaf
JPanel panel = new JPanel();
panel.add(new JButton("OK"));
panel.add(new JButton("Cancel"));
```

### 2. DOM (Document Object Model)
```javascript
// div는 Composite, span은 Leaf
const div = document.createElement('div');
div.appendChild(document.createElement('span'));
```

### 3. React 컴포넌트
```jsx
// Container는 Composite, Button은 Leaf
<Container>
  <Button>Click me</Button>
  <Container>
    <Text>Hello</Text>
  </Container>
</Container>
```

### 4. 파일 시스템 API
운영체제의 파일 시스템이 파일과 디렉토리를 동일하게 다루는 전형적인 예이다.

## 관련 패턴

| 패턴 | 컴포지트와의 관계 |
|------|-----------------|
| **Decorator** | 둘 다 재귀적 합성 사용, Decorator는 기능 추가에 초점 |
| **Iterator** | 컴포지트 구조를 순회할 때 사용 |
| **Visitor** | 컴포지트 구조의 요소들에 연산을 적용할 때 사용 |
| **Flyweight** | 공유 가능한 Leaf 노드를 플라이웨이트로 구현 |

## FAQ

**Q1: Leaf에서 자식 관리 메서드를 어떻게 처리해야 하나요?**

두 가지 접근 방식이 있습니다. 1) 예외를 발생시키거나, 2) 빈 구현을 제공합니다. 투명성(Transparency)을 위해서는 Component에 모든 메서드를 두고, 안전성(Safety)을 위해서는 Composite에만 자식 관리 메서드를 둡니다.

**Q2: 순환 참조 문제는 어떻게 방지하나요?**

add() 메서드에서 순환 참조를 검사하거나, 부모 참조를 유지하여 이미 조상에 있는 컴포넌트는 추가할 수 없도록 해야 합니다.

**Q3: 컴포지트 패턴에서 자식 순서가 중요한가요?**

애플리케이션에 따라 다릅니다. GUI 컴포넌트에서는 순서가 렌더링 순서에 영향을 미치지만, 파일 시스템에서는 보통 중요하지 않습니다.

**Q4: 특정 타입의 컴포넌트만 추가하도록 제한할 수 있나요?**

타입 검사를 통해 가능하지만, 이는 컴포지트 패턴의 균일성 원칙에 어긋납니다. 필요하다면 별도의 패턴이나 제약 조건을 추가해야 합니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- Java Swing API 문서