---
collection_order: 23
title: "[Design Pattern] Visitor - 방문자 패턴"
description: "Visitor 패턴은 객체 구조와 오퍼레이션을 분리하여 새로운 기능 추가를 쉽게 합니다. 복잡한 객체 구조에서도 기능의 유연한 확장과 유지보수가 가능합니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Visitor
  - 방문자
  - Behavioral Pattern
  - 행위 패턴
  - GoF
  - Gang of Four
  - Double Dispatch
  - 이중 디스패치
  - Element
  - 요소
  - Concrete Visitor
  - 구체 방문자
  - Concrete Element
  - 구체 요소
  - Object Structure
  - 객체 구조
  - Accept
  - Visit
  - Separation of Concerns
  - 관심사 분리
  - Open Closed Principle
  - 개방 폐쇄 원칙
  - Polymorphism
  - 다형성
  - Traversal
  - 순회
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
  - AST
  - Abstract Syntax Tree
  - Compiler
  - 컴파일러
  - Document
  - 문서
---

방문자 패턴(Visitor Pattern)은 객체 구조의 요소들에 수행할 연산을 별도의 방문자 객체로 분리하는 행위 디자인 패턴이다. 이 패턴을 사용하면 기존 객체 구조를 변경하지 않고 새로운 연산을 추가할 수 있다.

## 개요

**방문자 패턴의 정의**

방문자 패턴은 데이터 구조와 처리를 분리하여, 구조 내의 요소들에 대한 새로운 연산을 요소 클래스의 수정 없이 추가할 수 있게 한다. 이는 더블 디스패치(Double Dispatch) 기법을 사용하여 구현된다.

**더블 디스패치 (Double Dispatch)**

일반적인 메서드 호출(싱글 디스패치)은 호출 객체의 타입만으로 메서드를 결정한다. 더블 디스패치는 호출 객체와 매개변수 객체 모두의 타입에 따라 메서드를 결정한다.

**패턴의 필요성 및 사용 사례**

방문자 패턴은 다음과 같은 상황에서 유용하다:

- **컴파일러**: AST(추상 구문 트리) 순회 및 처리
- **문서 처리**: 다양한 형식으로 내보내기 (PDF, HTML, Text)
- **UI 렌더링**: 다양한 렌더러로 그리기
- **파일 시스템**: 파일 크기 계산, 검색, 변환
- **세금 계산**: 다양한 상품에 대한 세금 계산

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 관련 연산을 한 곳에 모음 | 새 요소 추가 시 모든 Visitor 수정 |
| 새 연산 추가 용이 | 요소의 캡슐화 위반 가능 |
| 복잡한 객체 구조 순회 통합 | 복잡한 구조 |
| 단일 책임 원칙 준수 | 이해하기 어려울 수 있음 |

## 방문자 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│          <<interface>>              │
│            Visitor                  │
├─────────────────────────────────────┤
│ + visitElementA(ElementA)           │
│ + visitElementB(ElementB)           │
└─────────────────────────────────────┘
              △
              │
    ┌─────────┴─────────┐
    │                   │
┌──────────────┐  ┌──────────────┐
│ ConcreteVis1 │  │ ConcreteVis2 │
└──────────────┘  └──────────────┘

┌─────────────────────────────────────┐
│          <<interface>>              │
│            Element                  │
├─────────────────────────────────────┤
│ + accept(Visitor)                   │
└─────────────────────────────────────┘
              △
              │
    ┌─────────┴─────────┐
    │                   │
┌──────────────┐  ┌──────────────┐
│   ElementA   │  │   ElementB   │
├──────────────┤  ├──────────────┤
│ +accept(v)   │  │ +accept(v)   │
│  v.visitA()  │  │  v.visitB()  │
└──────────────┘  └──────────────┘
```

**1. Visitor (방문자)**
- 각 요소 타입에 대한 visit 메서드 정의

**2. ConcreteVisitor (구체적 방문자)**
- 실제 연산 구현

**3. Element (요소)**
- accept 메서드 정의

**4. ConcreteElement (구체적 요소)**
- accept에서 적절한 visit 메서드 호출

## 구현 예제

### Python 예제 - 도형 면적/둘레 계산

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import List
import math

# Visitor 인터페이스
class ShapeVisitor(ABC):
    @abstractmethod
    def visit_circle(self, circle: 'Circle') -> float:
        pass
    
    @abstractmethod
    def visit_rectangle(self, rectangle: 'Rectangle') -> float:
        pass
    
    @abstractmethod
    def visit_triangle(self, triangle: 'Triangle') -> float:
        pass

# Element 인터페이스
class Shape(ABC):
    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> float:
        pass

# ConcreteElement - 원
class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def accept(self, visitor: ShapeVisitor) -> float:
        return visitor.visit_circle(self)

# ConcreteElement - 사각형
class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def accept(self, visitor: ShapeVisitor) -> float:
        return visitor.visit_rectangle(self)

# ConcreteElement - 삼각형
class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c
    
    def accept(self, visitor: ShapeVisitor) -> float:
        return visitor.visit_triangle(self)

# ConcreteVisitor - 면적 계산
class AreaCalculator(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> float:
        return math.pi * circle.radius ** 2
    
    def visit_rectangle(self, rectangle: Rectangle) -> float:
        return rectangle.width * rectangle.height
    
    def visit_triangle(self, triangle: Triangle) -> float:
        # 헤론의 공식
        s = (triangle.a + triangle.b + triangle.c) / 2
        return math.sqrt(s * (s - triangle.a) * (s - triangle.b) * (s - triangle.c))

# ConcreteVisitor - 둘레 계산
class PerimeterCalculator(ShapeVisitor):
    def visit_circle(self, circle: Circle) -> float:
        return 2 * math.pi * circle.radius
    
    def visit_rectangle(self, rectangle: Rectangle) -> float:
        return 2 * (rectangle.width + rectangle.height)
    
    def visit_triangle(self, triangle: Triangle) -> float:
        return triangle.a + triangle.b + triangle.c

# 사용 예제
if __name__ == "__main__":
    shapes: List[Shape] = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4, 5)
    ]
    
    area_calc = AreaCalculator()
    perimeter_calc = PerimeterCalculator()
    
    print("=== 도형 계산 (Visitor 패턴) ===\n")
    
    for shape in shapes:
        shape_name = shape.__class__.__name__
        area = shape.accept(area_calc)
        perimeter = shape.accept(perimeter_calc)
        print(f"{shape_name}:")
        print(f"  면적: {area:.2f}")
        print(f"  둘레: {perimeter:.2f}\n")
```

### Java 예제 - 문서 내보내기

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// Element 인터페이스
interface DocumentElement {
    void accept(DocumentVisitor visitor);
}

// ConcreteElement - 제목
class Heading implements DocumentElement {
    private String text;
    private int level;
    
    public Heading(String text, int level) {
        this.text = text;
        this.level = level;
    }
    
    public String getText() { return text; }
    public int getLevel() { return level; }
    
    @Override
    public void accept(DocumentVisitor visitor) {
        visitor.visitHeading(this);
    }
}

// ConcreteElement - 문단
class Paragraph implements DocumentElement {
    private String text;
    
    public Paragraph(String text) {
        this.text = text;
    }
    
    public String getText() { return text; }
    
    @Override
    public void accept(DocumentVisitor visitor) {
        visitor.visitParagraph(this);
    }
}

// ConcreteElement - 이미지
class Image implements DocumentElement {
    private String url;
    private String alt;
    
    public Image(String url, String alt) {
        this.url = url;
        this.alt = alt;
    }
    
    public String getUrl() { return url; }
    public String getAlt() { return alt; }
    
    @Override
    public void accept(DocumentVisitor visitor) {
        visitor.visitImage(this);
    }
}

// Visitor 인터페이스
interface DocumentVisitor {
    void visitHeading(Heading heading);
    void visitParagraph(Paragraph paragraph);
    void visitImage(Image image);
    String getResult();
}

// ConcreteVisitor - HTML 내보내기
class HtmlExporter implements DocumentVisitor {
    private StringBuilder sb = new StringBuilder();
    
    @Override
    public void visitHeading(Heading heading) {
        sb.append(String.format("<h%d>%s</h%d>\n", 
            heading.getLevel(), heading.getText(), heading.getLevel()));
    }
    
    @Override
    public void visitParagraph(Paragraph paragraph) {
        sb.append(String.format("<p>%s</p>\n", paragraph.getText()));
    }
    
    @Override
    public void visitImage(Image image) {
        sb.append(String.format("<img src=\"%s\" alt=\"%s\" />\n", 
            image.getUrl(), image.getAlt()));
    }
    
    @Override
    public String getResult() {
        return "<html>\n<body>\n" + sb.toString() + "</body>\n</html>";
    }
}

// ConcreteVisitor - Markdown 내보내기
class MarkdownExporter implements DocumentVisitor {
    private StringBuilder sb = new StringBuilder();
    
    @Override
    public void visitHeading(Heading heading) {
        sb.append("#".repeat(heading.getLevel()))
          .append(" ")
          .append(heading.getText())
          .append("\n\n");
    }
    
    @Override
    public void visitParagraph(Paragraph paragraph) {
        sb.append(paragraph.getText()).append("\n\n");
    }
    
    @Override
    public void visitImage(Image image) {
        sb.append(String.format("![%s](%s)\n\n", image.getAlt(), image.getUrl()));
    }
    
    @Override
    public String getResult() {
        return sb.toString();
    }
}

// 사용 예제
public class VisitorDemo {
    public static void main(String[] args) {
        List<DocumentElement> document = Arrays.asList(
            new Heading("방문자 패턴", 1),
            new Paragraph("방문자 패턴은 객체 구조와 연산을 분리합니다."),
            new Image("diagram.png", "패턴 다이어그램"),
            new Heading("장점", 2),
            new Paragraph("새 연산 추가가 쉽습니다.")
        );
        
        System.out.println("=== HTML 출력 ===");
        DocumentVisitor htmlExporter = new HtmlExporter();
        for (DocumentElement elem : document) {
            elem.accept(htmlExporter);
        }
        System.out.println(htmlExporter.getResult());
        
        System.out.println("=== Markdown 출력 ===");
        DocumentVisitor mdExporter = new MarkdownExporter();
        for (DocumentElement elem : document) {
            elem.accept(mdExporter);
        }
        System.out.println(mdExporter.getResult());
    }
}
```

## 실제 사용 사례

### 1. 컴파일러 AST 처리
TypeChecker, CodeGenerator 등 다양한 Visitor

### 2. DOM 순회
Node.accept(Visitor) 패턴

### 3. Java Annotation Processing
ElementVisitor 인터페이스

## 관련 패턴

| 패턴 | 방문자와의 관계 |
|------|---------------|
| **Composite** | Composite 구조 순회에 Visitor 사용 |
| **Iterator** | 복잡한 구조 순회 시 함께 사용 |
| **Interpreter** | AST 처리에 Visitor 사용 |

## FAQ

**Q1: 새 요소 타입을 추가하면 어떻게 되나요?**

모든 Visitor에 새 visit 메서드를 추가해야 합니다. 이것이 Visitor 패턴의 주요 단점입니다.

**Q2: 언제 Visitor 패턴을 사용해야 하나요?**

요소 클래스가 안정적이고 새 연산이 자주 추가될 때 유용합니다.

## 참고 자료

- GoF의 "Design Patterns"
- ANTLR 문서