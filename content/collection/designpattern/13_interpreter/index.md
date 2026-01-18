---
collection_order: 13
title: "[Design Pattern] Interpreter - 인터프리터 패턴"
description: "Interpreter 패턴은 특정 언어나 문법을 해석하는 과정을 객체로 표현합니다. 간단한 문법 규칙을 객체 조합으로 구축하고 해석 로직을 유연하게 확장할 수 있습니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Interpreter
  - 인터프리터
  - Behavioral Pattern
  - 행위 패턴
  - GoF
  - Gang of Four
  - Grammar
  - 문법
  - Language
  - 언어
  - DSL
  - Domain Specific Language
  - 도메인 특화 언어
  - Parser
  - 파서
  - Expression
  - 표현식
  - Abstract Syntax Tree
  - 추상 구문 트리
  - Terminal Expression
  - 터미널 표현식
  - Nonterminal Expression
  - 비터미널 표현식
  - Context
  - 컨텍스트
  - Regular Expression
  - 정규 표현식
  - SQL Parser
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
  - Compiler
  - 컴파일러
  - Calculator
  - 계산기
  - Rule Engine
  - 규칙 엔진
---

인터프리터 패턴(Interpreter Pattern)은 특정 언어나 문법을 해석하고 실행하는 방법을 정의하는 행위 디자인 패턴이다. 이 패턴을 사용하면 간단한 언어의 문법을 클래스로 표현하고, 문장을 해석하는 인터프리터를 구현할 수 있다.

## 개요

**인터프리터 패턴의 정의**

인터프리터 패턴은 언어의 문법을 클래스 계층으로 표현하고, 추상 구문 트리(AST)를 구성한 후 이를 해석하여 실행한다. 주로 도메인 특화 언어(DSL)나 간단한 스크립트 언어를 구현할 때 사용된다.

**패턴의 필요성 및 사용 사례**

인터프리터 패턴은 다음과 같은 상황에서 유용하다:

- **정규 표현식**: 패턴 매칭
- **수학 표현식**: 계산기
- **SQL 파서**: 쿼리 해석
- **설정 파일**: 간단한 스크립트 언어
- **규칙 엔진**: 비즈니스 규칙 평가
- **템플릿 엔진**: 동적 문서 생성

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 문법 규칙 변경/추가 용이 | 복잡한 문법에 부적합 |
| 문법이 클래스로 명시적 표현 | 클래스 수가 많아짐 |
| 새 표현식 추가 용이 | 성능 이슈 가능 |
| 인터프리터 확장 용이 | 유지보수 어려울 수 있음 |

## 인터프리터 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│          <<interface>>              │
│         AbstractExpression          │
├─────────────────────────────────────┤
│ + interpret(Context): result        │
└─────────────────────────────────────┘
              △
              │
    ┌─────────┴─────────┐
    │                   │
┌──────────────┐  ┌──────────────┐
│ Terminal     │  │ Nonterminal  │
│ Expression   │  │ Expression   │
└──────────────┘  └──────────────┘
```

**1. AbstractExpression (추상 표현식)**
- interpret() 메서드 정의

**2. TerminalExpression (터미널 표현식)**
- 문법의 끝 요소 (변수, 상수 등)

**3. NonterminalExpression (비터미널 표현식)**
- 다른 표현식을 포함하는 복합 표현식 (연산자 등)

**4. Context (컨텍스트)**
- 해석에 필요한 전역 정보 (변수 값 등)

## 구현 예제

### Python 예제 - 수식 계산기

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import Dict

# Context - 변수 저장소
class Context:
    def __init__(self):
        self.variables: Dict[str, float] = {}
    
    def set_variable(self, name: str, value: float):
        self.variables[name] = value
    
    def get_variable(self, name: str) -> float:
        return self.variables.get(name, 0)

# AbstractExpression
class Expression(ABC):
    @abstractmethod
    def interpret(self, context: Context) -> float:
        pass

# TerminalExpression - 숫자
class NumberExpression(Expression):
    def __init__(self, value: float):
        self.value = value
    
    def interpret(self, context: Context) -> float:
        return self.value

# TerminalExpression - 변수
class VariableExpression(Expression):
    def __init__(self, name: str):
        self.name = name
    
    def interpret(self, context: Context) -> float:
        return context.get_variable(self.name)

# NonterminalExpression - 덧셈
class AddExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: Context) -> float:
        return self.left.interpret(context) + self.right.interpret(context)

# NonterminalExpression - 뺄셈
class SubtractExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: Context) -> float:
        return self.left.interpret(context) - self.right.interpret(context)

# NonterminalExpression - 곱셈
class MultiplyExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: Context) -> float:
        return self.left.interpret(context) * self.right.interpret(context)

# NonterminalExpression - 나눗셈
class DivideExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: Context) -> float:
        right_val = self.right.interpret(context)
        if right_val == 0:
            raise ValueError("Division by zero")
        return self.left.interpret(context) / right_val

# 사용 예제
if __name__ == "__main__":
    context = Context()
    context.set_variable("x", 10)
    context.set_variable("y", 5)
    
    # (x + y) * 2 - 10
    expression = SubtractExpression(
        MultiplyExpression(
            AddExpression(
                VariableExpression("x"),
                VariableExpression("y")
            ),
            NumberExpression(2)
        ),
        NumberExpression(10)
    )
    
    print(f"x = {context.get_variable('x')}, y = {context.get_variable('y')}")
    print(f"(x + y) * 2 - 10 = {expression.interpret(context)}")
    
    # x / y + 3
    expression2 = AddExpression(
        DivideExpression(
            VariableExpression("x"),
            VariableExpression("y")
        ),
        NumberExpression(3)
    )
    
    print(f"x / y + 3 = {expression2.interpret(context)}")
```

### Java 예제 - 불리언 표현식

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// Context
class BooleanContext {
    private Map<String, Boolean> variables = new HashMap<>();
    
    public void setVariable(String name, boolean value) {
        variables.put(name, value);
    }
    
    public boolean getVariable(String name) {
        return variables.getOrDefault(name, false);
    }
}

// AbstractExpression
interface BooleanExpression {
    boolean interpret(BooleanContext context);
}

// TerminalExpression - 상수
class ConstantExpression implements BooleanExpression {
    private boolean value;
    
    public ConstantExpression(boolean value) {
        this.value = value;
    }
    
    @Override
    public boolean interpret(BooleanContext context) {
        return value;
    }
}

// TerminalExpression - 변수
class BooleanVariableExpression implements BooleanExpression {
    private String name;
    
    public BooleanVariableExpression(String name) {
        this.name = name;
    }
    
    @Override
    public boolean interpret(BooleanContext context) {
        return context.getVariable(name);
    }
}

// NonterminalExpression - AND
class AndExpression implements BooleanExpression {
    private BooleanExpression left;
    private BooleanExpression right;
    
    public AndExpression(BooleanExpression left, BooleanExpression right) {
        this.left = left;
        this.right = right;
    }
    
    @Override
    public boolean interpret(BooleanContext context) {
        return left.interpret(context) && right.interpret(context);
    }
}

// NonterminalExpression - OR
class OrExpression implements BooleanExpression {
    private BooleanExpression left;
    private BooleanExpression right;
    
    public OrExpression(BooleanExpression left, BooleanExpression right) {
        this.left = left;
        this.right = right;
    }
    
    @Override
    public boolean interpret(BooleanContext context) {
        return left.interpret(context) || right.interpret(context);
    }
}

// NonterminalExpression - NOT
class NotExpression implements BooleanExpression {
    private BooleanExpression expression;
    
    public NotExpression(BooleanExpression expression) {
        this.expression = expression;
    }
    
    @Override
    public boolean interpret(BooleanContext context) {
        return !expression.interpret(context);
    }
}

// 사용 예제
public class InterpreterDemo {
    public static void main(String[] args) {
        BooleanContext context = new BooleanContext();
        context.setVariable("A", true);
        context.setVariable("B", false);
        context.setVariable("C", true);
        
        // (A AND B) OR C
        BooleanExpression expression = new OrExpression(
            new AndExpression(
                new BooleanVariableExpression("A"),
                new BooleanVariableExpression("B")
            ),
            new BooleanVariableExpression("C")
        );
        
        System.out.println("A = true, B = false, C = true");
        System.out.println("(A AND B) OR C = " + expression.interpret(context));
        
        // NOT (A OR B)
        BooleanExpression expression2 = new NotExpression(
            new OrExpression(
                new BooleanVariableExpression("A"),
                new BooleanVariableExpression("B")
            )
        );
        
        System.out.println("NOT (A OR B) = " + expression2.interpret(context));
    }
}
```

## 실제 사용 사례

### 1. 정규 표현식
java.util.regex.Pattern

### 2. SQL 파서
Hibernate HQL, JPQL

### 3. SpEL (Spring Expression Language)
```java
ExpressionParser parser = new SpelExpressionParser();
Expression exp = parser.parseExpression("'Hello'.concat(' World')");
```

## 관련 패턴

| 패턴 | 인터프리터와의 관계 |
|------|------------------|
| **Composite** | AST가 Composite 구조 |
| **Visitor** | AST 순회에 Visitor 사용 |
| **Flyweight** | 터미널 표현식 공유 |

## FAQ

**Q1: 복잡한 언어에도 적합한가요?**

아닙니다. 복잡한 언어는 파서 생성기(ANTLR 등)를 사용하는 것이 좋습니다.

**Q2: 성능 문제는 어떻게 해결하나요?**

캐싱, Flyweight 패턴 사용, 또는 바이트코드로 컴파일하는 방법이 있습니다.

## 참고 자료

- GoF의 "Design Patterns"
- ANTLR Documentation