---
image: "wordcloud.png"
slug: generics-and-polymorphism
collection_order: 100
draft: false
title: "[Computer Terms] 제네릭과 다형성 (Generics, Polymorphism)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "제네릭은 정적 타입 언어에서 타입마다 로직을 중복 작성하지 않도록 타입을 매개변수화합니다. 오버로딩·오버라이딩·제네릭이라는 다형성의 세 형태를 TypeScript 코드로 구분합니다."
tags:
- Technology(기술)
- Education(교육)
- Programming-Language(프로그래밍언어)
- Type-System(타입시스템)
- Polymorphism(다형성)
- TypeScript
- Java
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Software-Engineering(소프트웨어공학)
- Code-Quality(코드품질)
- Debugging(디버깅)
- Design-Pattern(디자인패턴)
- Clean-Code(클린코드)
- Data-Structures(자료구조)
- Refactoring(리팩토링)
---

## 이 장을 읽기 전에

[타입 시스템](/post/computerterms/type-systems/)에서 다룬 정적 타입 언어가 컴파일 시점에 타입 불일치를 잡아낸다는 원리와, [함수형 프로그래밍 패러다임](/post/computerterms/functional-programming-paradigm/)에서 다룬 "같은 로직을 여러 데이터에 재사용"하는 감각을 안다고 가정한다. 이 챕터는 정적 타입 언어에서 그 재사용을 타입 안전하게 하는 방법을 다룬다.

## 정적 타입 언어의 딜레마: 재사용이냐 안전이냐

[타입 시스템](/post/computerterms/type-systems/)에서 다룬 것처럼 정적 타입 언어는 컴파일 시점에 타입 오류를 잡아준다는 장점이 있지만, 그 대가로 "숫자 배열에서 최댓값을 찾는 함수"와 "문자열 배열에서 최댓값을 찾는 함수"를 타입마다 따로 작성해야 하는 것처럼 보인다. 함수 시그니처에 타입을 고정해버리면 재사용성이 크게 떨어진다. **제네릭(Generics)**은 함수나 클래스를 정의할 때 구체적인 타입 대신 `T` 같은 **타입 매개변수(Type Parameter)**를 두어, 실제로 그 함수·클래스를 사용하는 시점에 타입이 채워지도록 하는 기법이다. 이렇게 하면 타입마다 로직을 중복 작성하지 않으면서도, 컴파일러가 여전히 타입을 검사할 수 있다.

```typescript
// 제네릭이 없다면 number용, string용 함수를 각각 만들어야 한다
function firstNumber(arr: number[]): number {
    return arr[0];
}
function firstString(arr: string[]): string {
    return arr[0];
}

// 제네릭: T라는 타입 매개변수를 두어 어떤 타입의 배열에도 재사용
function first<T>(arr: T[]): T {
    return arr[0];
}

const n = first<number>([1, 2, 3]);      // T가 number로 채워짐, n: number
const s = first<string>(["a", "b"]);     // T가 string으로 채워짐, s: string
// first<number>([1, 2, 3]).toUpperCase();  // 컴파일 오류: number에는 toUpperCase가 없음
```

`first` 함수는 단 한 번만 작성되었지만, 호출 시점에 `T`가 `number`로 채워지면 반환값도 `number`로, `string`으로 채워지면 반환값도 `string`으로 컴파일러가 추론한다. 그 덕분에 마지막 줄처럼 `number` 배열에 문자열 전용 메서드를 잘못 호출하려 하면 컴파일 시점에 바로 오류가 난다 — 코드는 한 번만 썼지만 타입 안전성은 그대로 유지된다.

## 다형성의 세 형태: 오버로딩, 오버라이딩, 제네릭

**다형성(Polymorphism)**은 "여러(poly) 형태(morph)"라는 어원 그대로, 하나의 이름이나 인터페이스로 서로 다른 타입에 대해 다르게 동작하는 능력을 가리키는 포괄적 개념이다. 흔히 세 가지 형태로 구분한다. **오버로딩(Overloading)**은 같은 이름의 함수를 매개변수의 타입이나 개수를 다르게 해 여러 버전으로 정의하는 것으로, 어떤 버전이 실행될지는 컴파일 시점에 인자 타입을 보고 정해진다(**정적 다형성**). **오버라이딩(Overriding)**은 상위 클래스가 정의한 메서드를 하위 클래스가 자신에 맞게 다시 정의하는 것으로, 실제로 어떤 버전이 실행될지는 그 객체의 실제 타입에 따라 실행 시점에 정해진다(**동적 다형성**). **제네릭**은 앞서 본 것처럼 타입을 매개변수화해 하나의 코드가 여러 타입에 대해 동작하게 하는 것으로, 오버로딩·오버라이딩과 달리 코드 자체는 하나만 존재한다.

```java
class Shape {
    double area() { return 0; }
}
class Circle extends Shape {
    double radius;
    Circle(double r) { this.radius = r; }
    @Override
    double area() { return Math.PI * radius * radius; }  // 오버라이딩: 실행 시점에 실제 타입 기준으로 결정
}
class Square extends Shape {
    double side;
    Square(double s) { this.side = s; }
    @Override
    double area() { return side * side; }
}

class Calc {
    // 오버로딩: 매개변수 타입이 다른 두 print 버전, 컴파일 시점에 인자 타입으로 결정
    void print(int x) { System.out.println("int: " + x); }
    void print(double x) { System.out.println("double: " + x); }
}
```

`Shape` 타입 변수에 `Circle`이나 `Square` 객체를 담아 `area()`를 호출하면, 실제로 어떤 클래스의 `area()`가 실행될지는 프로그램이 그 줄에 도달하는 순간의 실제 객체 타입을 보고 결정된다 — 이것이 오버라이딩이 "동적" 다형성으로 불리는 이유다. 반면 `Calc`의 `print` 메서드는 어떤 버전이 호출될지가 인자로 `int`를 넘겼는지 `double`을 넘겼는지에 따라 컴파일 시점에 이미 정해진다.

## 비교: 오버로딩 vs 오버라이딩 vs 제네릭

| 특성 | 오버로딩 | 오버라이딩 | 제네릭 |
|---|---|---|---|
| 결정 시점 | 컴파일 시점(정적) | 실행 시점(동적) | 컴파일 시점(정적) |
| 코드 개수 | 시그니처마다 별도 작성 | 클래스마다 별도 작성 | 하나의 코드로 여러 타입 지원 |
| 관계 | 같은 클래스 내 여러 메서드 | 상속 관계(부모-자식) | 타입 매개변수화 |
| 목적 | 인자 형태별 처리 분기 | 하위 클래스별 동작 특화 | 타입 중복 제거 |

## 흔한 오개념

**"제네릭은 다형성의 한 형태일 뿐 서로 무관하다"** — 제네릭과 오버라이딩은 실제로 함께 쓰이는 경우가 많다. 예를 들어 제네릭 컬렉션 클래스(`List<T>`)에 담긴 객체의 메서드를 호출할 때, 그 메서드가 오버라이딩되어 있다면 컴파일 시점에는 `T`로만 알려진 타입이라도 실행 시점에는 실제 객체 타입에 맞는 오버라이딩된 메서드가 호출된다 — 정적 다형성(제네릭)과 동적 다형성(오버라이딩)이 한 코드 안에서 겹쳐 동작하는 것이다.

**"제네릭은 아무 타입이나 다 받는다는 뜻이다"** — `Any` 타입으로 받는 것과 제네릭은 다르다. `Any`는 타입 정보를 버려서 컴파일러가 이후 검사를 포기하지만, 제네릭은 `T`가 무엇이든 호출 시점에 **하나의 구체적인 타입으로 고정**되고 그 타입에 맞는 검사를 계속 수행한다. 앞의 `first<number>([1, 2, 3])` 예시에서 반환값에 문자열 메서드를 호출하면 오류가 나는 것이 이 차이를 보여준다.

## 다른 개념과의 연결

제네릭이 컴파일 시점에 타입을 검사한다는 점은 [타입 시스템](/post/computerterms/type-systems/)에서 다룬 정적 타입 검사의 연장선이며, 함수형 프로그래밍의 `map`/`filter`(예: `map<T, U>`)도 내부적으로 제네릭 타입 시그니처로 정의된다. 다음 챕터에서는 정적 타입 언어가 컴파일 시점에 잡아내지 못하는 또 다른 종류의 메모리 버그를, 가비지 컬렉션과 다른 제3의 접근인 소유권 모델로 원천 차단하는 방법을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 제네릭이 타입 중복 작성 문제를 해결하는 원리를 설명할 수 있다. 오버로딩·오버라이딩·제네릭을 결정 시점(정적/동적)과 코드 개수 기준으로 구분할 수 있다. 제네릭과 `Any` 타입의 차이를 타입 안전성 관점에서 설명할 수 있다.

## 참고 자료

> Cardelli, L., & Wegner, P. (1985). "On Understanding Types, Data Abstraction, and Polymorphism." *ACM Computing Surveys*, 17(4), 471–523.

- [TypeScript Handbook: Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html) — TypeScript 제네릭 함수·클래스·제약 조건의 공식 문서
- [Oracle Java Tutorials: Polymorphism](https://docs.oracle.com/javase/tutorial/java/IandI/polymorphism.html) — Java에서 오버라이딩 기반 동적 다형성이 동작하는 방식
