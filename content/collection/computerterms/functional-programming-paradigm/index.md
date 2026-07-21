---
image: "wordcloud.png"
slug: functional-programming-paradigm
collection_order: 99
draft: false
title: "[Computer Terms] 함수형 프로그래밍 패러다임 (Functional Programming)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "함수형 프로그래밍은 순수 함수와 불변성을 핵심 원칙으로 삼는 패러다임입니다. 명령형 반복문과 함수형 map/filter/reduce를 같은 문제로 비교해 차이를 설명합니다."
tags:
- Technology(기술)
- Education(교육)
- Programming-Language(프로그래밍언어)
- Functional-Programming(함수형프로그래밍)
- Immutability(불변성)
- Python
- JavaScript
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
- Refactoring(리팩토링)
- Concurrency(동시성)
---

## 이 장을 읽기 전에

[클로저와 스코프](/post/computerterms/closures-and-scope/)에서 다룬 "함수를 값으로 다루고 다른 함수에 전달하거나 반환할 수 있다"는 개념을 안다고 가정한다. 이 챕터는 그런 함수들을 어떤 원칙으로 조합해 프로그램을 만드는지, 즉 함수형 프로그래밍이라는 패러다임 자체를 다룬다.

## 순수 함수: 같은 입력에는 항상 같은 출력

함수형 프로그래밍의 핵심은 **순수 함수(Pure Function)**다. 순수 함수는 두 가지 성질을 만족한다. 첫째, 같은 입력이 주어지면 언제 호출하든 항상 같은 출력을 반환한다. 둘째, 함수 바깥의 상태를 변경하거나(전역 변수 수정, 파일 쓰기, 화면 출력 등) 바깥 상태에 의존하지 않는다 — 이를 **부작용(Side Effect)이 없다**고 표현한다. 반대로 현재 시각을 반환하는 함수나, 호출할 때마다 외부 변수를 증가시키는 함수는 순수하지 않다. 순수 함수는 입력과 출력의 관계만으로 동작이 완전히 설명되므로, 호출 순서나 몇 번 호출되었는지와 무관하게 항상 같은 결과를 예측할 수 있어 테스트하기 쉽고, 여러 곳에서 동시에 호출해도 서로 간섭하지 않는다.

## 불변성: 값을 바꾸지 않고 새로 만든다

**불변성(Immutability)**은 한번 만들어진 데이터를 변경하지 않고, 변경이 필요하면 원본은 그대로 둔 채 변경된 내용을 반영한 **새 데이터를 만들어 반환**하는 원칙이다. 이는 순수 함수와 밀접하게 연결된다 — 함수가 인자로 받은 자료구조를 직접 수정해버리면 그 자체가 부작용이 되어 순수성이 깨지기 때문이다. Python의 리스트(`list`)나 JavaScript의 배열(`Array`)은 기본적으로 가변(mutable)이지만, 함수형 스타일에서는 이런 가변 자료구조라도 원본을 건드리지 않고 새 리스트를 만들어 반환하는 방식으로 다룬다.

```python
# 명령형: 반복문 + 가변 변수로 짝수의 제곱을 누적
def squares_of_evens_imperative(numbers):
    result = []
    for n in numbers:
        if n % 2 == 0:
            result.append(n * n)   # result라는 가변 상태를 계속 수정
    return result

# 함수형: filter로 걸러내고 map으로 변환 - 원본 리스트를 건드리지 않음
def squares_of_evens_functional(numbers):
    return list(map(lambda n: n * n, filter(lambda n: n % 2 == 0, numbers)))

numbers = [1, 2, 3, 4, 5, 6]
print(squares_of_evens_imperative(numbers))  # [4, 16, 36]
print(squares_of_evens_functional(numbers))  # [4, 16, 36]
print(numbers)  # [1, 2, 3, 4, 5, 6] - 원본은 두 방식 모두 그대로
```

두 함수는 같은 결과를 내지만 접근 방식이 다르다. 명령형 버전은 "어떻게(How) 계산할지"를 한 단계씩 지시한다 — 빈 리스트를 만들고, 반복하면서, 조건에 맞으면 추가하라는 절차를 명령형으로 나열한다. 함수형 버전은 "무엇을(What) 원하는지"를 선언한다 — filter로 짝수만 걸러내고 map으로 제곱하라는 두 변환의 조합으로 결과를 표현하며, 중간 과정에서 어떤 가변 변수도 등장하지 않는다.

```javascript
// JavaScript의 reduce: 누적값을 매번 새로 계산해 반환(원본 배열은 불변)
const numbers = [1, 2, 3, 4, 5];
const sum = numbers.reduce((acc, n) => acc + n, 0);
console.log(sum);        // 15
console.log(numbers);    // [1, 2, 3, 4, 5] - reduce는 원본을 수정하지 않는다
```

`reduce`는 누적값(`acc`)을 매 단계 새로운 값으로 계산해 다음 단계로 넘길 뿐, 원본 배열이나 이전 누적값을 직접 수정하지 않는다는 점에서 반복문으로 변수를 계속 덮어쓰는 명령형 누적과 대비된다.

## 비교: 명령형 vs 함수형

| 특성 | 명령형(Imperative) | 함수형(Functional) |
|---|---|---|
| 표현 방식 | 어떻게(How) 계산할지 절차를 지시 | 무엇을(What) 원하는지 변환의 조합으로 선언 |
| 상태 변경 | 반복문 안에서 변수를 계속 갱신 | 새 값을 만들어 반환, 원본 불변 |
| 대표 도구 | `for`/`while` 반복문 | `map`/`filter`/`reduce` |
| 동시 실행 안전성 | 공유 변수 접근 시 주의 필요 | 순수 함수는 상태 공유가 없어 안전 |

## 흔한 오개념

**"함수형 프로그래밍은 특정 언어(Haskell 등)에서만 쓸 수 있다"** — 순수 함수와 불변성은 언어 기능이 아니라 **작성 스타일**에 가깝다. Python, JavaScript, Java(스트림 API) 모두 `map`/`filter`/`reduce`에 해당하는 도구를 제공하며, 반복문 대신 이런 함수로 로직을 작성하면 명령형 언어에서도 함수형 스타일로 코드를 짤 수 있다. Haskell 같은 언어는 그 스타일을 문법 차원에서 강제하거나 장려할 뿐이다.

**"함수형 코드는 항상 더 빠르다/느리다"** — 불변성은 매번 새 자료구조를 만들 수 있어 원본을 직접 수정하는 것보다 메모리 할당이 늘어날 수 있지만, 그 대가로 [가비지 컬렉션](/post/computerterms/garbage-collection/)이 관리하는 동시성 안전성과 예측 가능성을 얻는다. 성능은 언어 구현(예: 불변 자료구조 전용 최적화 여부)에 따라 크게 달라지므로, "함수형이라 무조건 느리다"거나 "무조건 빠르다"는 단정은 근거가 없다.

## 다른 개념과의 연결

함수형 프로그래밍의 불변성 원칙은 [클로저와 스코프](/post/computerterms/closures-and-scope/)에서 다룬, 클로저가 변수를 참조 형태로 포획하는 특성과 함께 쓰이면 "포획한 변수를 다시 수정하지 않는" 안전한 클로저 사용으로 이어진다. 다음 챕터에서는 정적 타입 언어에서 같은 로직을 타입마다 중복 작성하지 않기 위한 제네릭과, 함수형 프로그래밍에서도 자주 쓰이는 다형성을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 순수 함수의 두 조건(같은 입력에 같은 출력, 부작용 없음)을 설명할 수 있다. 불변성이 왜 순수 함수와 함께 요구되는지 설명할 수 있다. 같은 문제를 명령형 반복문과 함수형 map/filter/reduce로 각각 구현했을 때의 차이를 코드로 비교할 수 있다.

## 참고 자료

> Hughes, J. (1989). "Why Functional Programming Matters." *The Computer Journal*, 32(2), 98–107.

- [Python Documentation: Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html) — Python에서 map/filter/reduce와 순수 함수를 활용하는 공식 가이드
- [MDN: Array.prototype.reduce()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce) — JavaScript reduce의 동작 방식과 예제
