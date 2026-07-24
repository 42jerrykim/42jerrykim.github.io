---
image: "wordcloud.png"
slug: closures-and-scope
collection_order: 98
draft: false
title: "[Computer Terms] 클로저와 스코프 (Closure, Scope)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "클로저는 함수가 자신이 정의된 렉시컬 환경의 변수를 기억해 반환 후에도 접근하는 원리입니다. 렉시컬 스코프와 동적 스코프의 차이를 JavaScript 카운터 예시로 다루고, 클로저의 메모리 누수 위험과 언제 피해야 하는지도 정리합니다."
tags:
- Technology(기술)
- Education(교육)
- Programming-Language(프로그래밍언어)
- Closure(클로저)
- Scope(스코프)
- JavaScript
- Python
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
- Clean-Code(클린코드)
- Data-Structures(자료구조)
- Refactoring(리팩토링)
- Design-Pattern(디자인패턴)
---

## 이 장을 읽기 전에

[가비지 컬렉션](/post/computerterms/garbage-collection/)에서 다룬 "더 이상 참조되지 않는 메모리만 회수된다"는 원리를 안다고 가정한다. 이 챕터에서 다루는 클로저가 바로 함수가 반환된 뒤에도 특정 변수를 계속 참조해 회수를 막는 대표적인 사례다.

## 스코프: 변수를 어디서 찾을 수 있는가

**스코프(Scope)**는 어떤 변수 이름이 코드의 어느 범위에서 유효한지를 정하는 규칙이다. 스코프를 결정하는 방식에는 크게 두 가지가 있다. **렉시컬 스코프(Lexical Scope, 정적 스코프)**는 변수가 코드 상에서 **정의된 위치**를 기준으로 유효 범위를 정한다 — 함수가 어디서 호출되든 상관없이, 그 함수가 소스 코드에서 어디에 쓰여 있었는지만으로 어떤 변수에 접근할 수 있는지가 정해진다. **동적 스코프(Dynamic Scope)**는 반대로 함수가 **호출된 시점의 호출 스택**을 기준으로 변수를 찾는다. JavaScript, Python, Java를 포함한 대부분의 현대 언어는 렉시컬 스코프를 쓰고, 동적 스코프는 초기 Lisp 방언이나 Bash 셸 변수 일부에서 볼 수 있다.

```python
x = "전역"

def outer():
    x = "outer의 지역"
    def inner():
        print(x)  # 렉시컬 스코프: inner가 "정의된 위치" 기준으로 outer의 x를 찾는다
    inner()

outer()  # "outer의 지역" 출력 - inner가 호출된 위치와 무관하게 정의 위치가 기준
```

동적 스코프였다면 `inner`가 어디서 호출되었는지(호출 스택에 어떤 `x`가 있었는지)에 따라 다른 값을 참조했겠지만, 렉시컬 스코프에서는 `inner`가 소스 코드에서 `outer` 안에 정의되어 있다는 사실만으로 항상 `outer`의 `x`를 가리킨다는 것이 정해진다.

## 클로저: 정의된 환경을 기억하는 함수

**클로저(Closure)**는 함수가 자신이 정의될 당시의 렉시컬 환경(그 시점에 유효했던 변수들)을 함께 "포획(capture)"해서, 그 함수가 정의된 스코프를 벗어나 다른 곳에서 호출되거나 심지어 바깥 함수가 이미 반환된 뒤에도 그 변수에 계속 접근할 수 있게 하는 함수를 말한다. 이는 렉시컬 스코프가 있기에 가능한 현상이다 — 함수가 어디서 정의되었는지만 알면 되므로, 정의 시점의 환경을 그대로 함수에 붙여 들고 다닐 수 있다.

```javascript
function makeCounter() {
    let count = 0;                 // makeCounter가 반환된 뒤에도 클로저가 이 변수를 붙잡는다
    return function () {
        count += 1;
        return count;
    };
}

const counter1 = makeCounter();
console.log(counter1());  // 1
console.log(counter1());  // 2  - count가 호출 사이에도 유지됨

const counter2 = makeCounter();
console.log(counter2());  // 1  - counter1과 별개의 독립된 count를 포획
```

`makeCounter` 함수의 실행이 끝나면 보통 지역 변수 `count`는 스택에서 사라져야 하지만, 반환된 익명 함수가 `count`를 참조하는 클로저이기 때문에 [가비지 컬렉션](/post/computerterms/garbage-collection/)이 이 변수를 회수하지 않는다 — `counter1`이라는 변수가 그 클로저를 참조하는 한, 클로저가 참조하는 `count`도 도달 가능(reachable) 상태로 유지된다. `counter1`과 `counter2`는 각각 `makeCounter`를 호출할 때마다 새로 만들어진 독립된 `count`를 포획하므로 서로 영향을 주지 않는다.

## 비교: 렉시컬 스코프 vs 동적 스코프

| 특성 | 렉시컬 스코프 | 동적 스코프 |
|---|---|---|
| 변수 결정 기준 | 코드상 정의 위치 | 호출 시점의 호출 스택 |
| 클로저 지원 | 자연스럽게 지원 | 일반적으로 지원하지 않음 |
| 코드 읽기만으로 예측 | 가능(정적으로 분석 가능) | 어려움(실행 흐름을 알아야 함) |
| 대표 사례 | JavaScript, Python, Java | 초기 Lisp, Bash 지역 변수 일부 |

## 흔한 오개념

**"클로저는 특별한 문법이다"** — 클로저는 별도의 키워드나 문법이 아니라, 렉시컬 스코프를 쓰는 언어에서 함수를 값으로 다룰 수 있으면(다른 함수의 반환값이 되거나 변수에 저장될 수 있으면) 자연스럽게 발생하는 현상이다. 함수 안에 함수를 정의하고 바깥 변수를 참조하도록 반환하기만 하면 이미 클로저다.

**"클로저가 포획한 변수는 값이 복사된다"** — 클로저는 변수의 **값**이 아니라 변수 자체(참조)를 포획한다. 반복문 안에서 클로저를 여러 개 만들 때 이 차이 때문에 흔한 버그가 생긴다. 예를 들어 JavaScript에서 `var i`로 선언한 반복 변수를 여러 클로저가 포획하면 모든 클로저가 같은 `i`를 공유해 반복이 끝난 뒤의 최종값을 함께 보게 되지만, 반복마다 새 스코프를 만드는 `let i`를 쓰면 클로저마다 독립된 `i`를 포획한다.

## 언제 클로저를 쓰고, 언제 피해야 하는가

클로저는 상태를 캡슐화하거나(위 카운터 예시처럼 `count`를 외부에서 직접 건드릴 수 없게 숨김), 콜백에 호출 당시의 컨텍스트를 함께 실어 보내거나, 반복되는 설정값을 미리 고정한 함수를 만드는 모듈 패턴에서 특히 유용하다. 하지만 대가도 있다. 첫째, 클로저가 큰 객체(대용량 배열, DOM 노드)를 포획한 채 오래 살아 있으면, [가비지 컬렉션](/post/computerterms/garbage-collection/)이 그 객체를 계속 "도달 가능"한 상태로 취급해 회수하지 못한다 — 특히 이벤트 리스너에 등록된 클로저를 해제하지 않으면 이 문제가 브라우저 탭이 오래 열려 있을수록 누적되는 메모리 누수로 이어진다. 둘째, 클로저를 여러 겹으로 중첩하면 어떤 변수가 어느 스코프에서 왔는지 추적하기 어려워져 가독성이 떨어진다. 따라서 클로저가 포획하는 변수의 수명이 짧고 크기가 작다면 적극적으로 쓰되, 큰 데이터를 오래 포획해야 하는 상황이라면 명시적으로 참조를 해제하는 시점(예: 이벤트 리스너 제거)을 함께 설계해야 한다.

## 다른 개념과의 연결

클로저가 [가비지 컬렉션](/post/computerterms/garbage-collection/)의 회수 시점에 영향을 준다는 점에서 두 챕터는 직접 이어진다. 다음 챕터에서는 클로저와 불변성을 함께 활용해 부작용 없는 함수를 조합하는 함수형 프로그래밍 패러다임을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 렉시컬 스코프와 동적 스코프가 변수를 찾는 기준의 차이를 설명할 수 있다. 클로저가 함수 반환 이후에도 특정 변수를 계속 참조하는 원리를 렉시컬 스코프와 연결해 설명할 수 있다. 반복문 안에서 클로저를 만들 때 변수 공유로 인해 생기는 버그를 예로 들어 설명할 수 있다.

## 참고 자료

> Abelson, H., & Sussman, G. J. (1996). *Structure and Interpretation of Computer Programs* (2nd ed.), Section 1.1.8: Procedures as Black-Box Abstractions. MIT Press.

- [MDN: Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures) — JavaScript 클로저의 동작 원리와 흔한 함정
- [Python Documentation: Nested Scopes](https://docs.python.org/3/reference/executionmodel.html#resolution-of-names) — Python의 렉시컬 스코프 규칙(LEGB)
