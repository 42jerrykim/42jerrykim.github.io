---
title: "[Redux] 01. JavaScript 핵심 개념 - 변수, 함수, 객체"
description: "Redux의 Action과 Reducer는 결국 JavaScript의 객체와 함수일 뿐입니다. var/let/const의 스코프 차이, 함수 선언 방식, 객체·배열 기본 조작을 Redux 코드를 읽는 데 필요한 만큼 정리합니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 1
draft: false
slug: javascript-fundamentals
tags:
  - JavaScript
  - Frontend(프론트엔드)
  - Web(웹)
  - Beginner
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Data-Structures(자료구조)
  - Readability
  - Debugging(디버깅)
  - How-To
  - Guide(가이드)
  - Documentation(문서화)
  - Reference(참고)
  - Software-Architecture(소프트웨어아키텍처)
  - Type-Safety
  - Error-Handling(에러처리)
  - 변수스코프
  - 함수선언
  - 화살표함수
  - 객체리터럴
  - 클로저
  - 호이스팅
  - 원시타입
---

# 01. JavaScript 핵심 개념 - 변수, 함수, 객체

Redux의 Action은 `{ type: "order/placed", payload: {...} }` 같은 평범한 객체이고, Reducer는 `(state, action) => newState` 형태의 평범한 함수입니다. 이 시리즈를 시작하기 전에, Redux 코드를 읽고 쓰는 데 필요한 JavaScript 기초를 정리합니다. 이미 익숙하다면 이 장은 빠르게 훑고 02편으로 넘어가도 좋습니다.

## 학습 목표

- `var`/`let`/`const`의 스코프·재선언 차이를 설명하고 상황에 맞게 선택할 수 있다.
- 함수 선언식·함수 표현식·화살표 함수의 차이(특히 `this` 바인딩)를 구분할 수 있다.
- 객체·배열을 다루는 기본 문법으로 Redux의 상태 형태를 읽고 쓸 수 있다.

## 변수 선언: var는 왜 피해야 하는가

`var`는 **함수 스코프**를 가지고, `let`/`const`는 **블록 스코프**를 가집니다. 이 차이가 실무 버그의 흔한 원인입니다.

```javascript
function demonstrateScope() {
  if (true) {
    var functionScoped = "I leak outside the block";
    let blockScoped = "I stay inside the block";
  }
  console.log(functionScoped); // "I leak outside the block" — 블록을 넘어 접근 가능
  console.log(typeof blockScoped); // "undefined" — blockScoped는 여기서 보이지 않음
}
```

`var`는 또한 **호이스팅**(선언이 스코프 최상단으로 끌어올려짐) 시 `undefined`로 초기화되어, 선언 전에 참조해도 에러 없이 `undefined`를 반환합니다. 반면 `let`/`const`는 선언 전 구간(Temporal Dead Zone)에서 참조하면 `ReferenceError`가 발생해 실수를 더 빨리 발견하게 해줍니다. 이런 이유로 **`const`를 기본으로, 재할당이 필요할 때만 `let`을 쓰고, `var`는 쓰지 않는 것**이 현대 JavaScript의 관례입니다.

```javascript
const MAX_RETRY = 3; // 재할당하지 않을 값
let retryCount = 0;  // 반복문에서 값이 바뀜

while (retryCount < MAX_RETRY) {
  retryCount += 1;
}
```

`const`는 **재할당을 막을 뿐, 값 자체를 불변으로 만들지 않습니다.** 객체나 배열을 `const`로 선언해도 내부 속성은 바꿀 수 있습니다.

```javascript
const state = { count: 0 };
state.count = 1; // 허용됨 — 재할당(state = {...})이 아니라 속성 변경이기 때문
```

이 구분은 08편(불변성)에서 Redux가 상태를 다루는 방식을 이해하는 데 중요한 기초가 됩니다.

## 함수 정의: 세 가지 방식과 this의 차이

JavaScript에는 함수를 정의하는 방식이 세 가지 있고, 가장 중요한 차이는 `this`가 무엇을 가리키는가입니다.

```javascript
// 1. 함수 선언식: 호이스팅되어 선언 전에도 호출 가능
function add(a, b) {
  return a + b;
}

// 2. 함수 표현식: 변수에 할당된 시점부터 호출 가능
const subtract = function (a, b) {
  return a - b;
};

// 3. 화살표 함수: this를 자신만의 것으로 바인딩하지 않고, 정의된 위치의 this를 그대로 사용
const multiply = (a, b) => a * b;
```

화살표 함수가 `this`를 새로 만들지 않는다는 점은 콜백 함수에서 특히 중요합니다.

```javascript
class Counter {
  constructor() {
    this.count = 0;
  }

  // 화살표 함수: this가 항상 Counter 인스턴스를 가리킴
  increment = () => {
    this.count += 1;
  };
}
```

일반 함수로 `increment`를 정의했다면, 이 메서드를 이벤트 핸들러로 전달했을 때 `this`가 `Counter` 인스턴스가 아니라 호출한 쪽의 컨텍스트로 바뀌어버리는 흔한 버그가 생깁니다. Redux 자체는 클래스보다 순수 함수를 많이 쓰지만, React 컴포넌트에서 이벤트 핸들러를 작성할 때 이 차이를 알아둬야 합니다.

## 객체와 배열: Redux 상태의 기본 형태

Redux의 상태(state)는 대부분 객체와 배열의 조합입니다.

```javascript
const initialState = {
  user: { id: 1, name: "Kim" },
  todos: [
    { id: 1, text: "Redux 배우기", done: false },
    { id: 2, text: "React-Redux 연동하기", done: false },
  ],
};

// 속성 접근
console.log(initialState.user.name); // "Kim"
console.log(initialState.todos[0].text); // "Redux 배우기"

// 배열에 새 항목 추가 (원본을 바꾸지 않는 방식은 08편에서 다룸)
const newTodos = initialState.todos.concat({ id: 3, text: "테스트 작성", done: false });
console.log(newTodos.length); // 3
console.log(initialState.todos.length); // 2 — 원본은 그대로
```

`concat()`이 원본 배열을 바꾸지 않고 새 배열을 반환한다는 점을 눈여겨보세요. `push()`는 원본을 직접 바꾸므로 Redux 리듀서 안에서는 쓰지 않습니다. 이 원칙은 08편에서 자세히 다룹니다.

## 흔한 실수

- **`var`로 반복문 변수를 선언하고 클로저에서 예상과 다른 값을 얻는 실수**: `var`는 블록 스코프가 없어 모든 반복이 같은 변수를 공유합니다. `let`을 쓰면 반복마다 새 바인딩이 생겨 의도한 대로 동작합니다.
- **객체를 `const`로 선언했으니 안전하다고 착각하는 실수**: 앞서 봤듯 `const`는 재할당만 막을 뿐, 속성 변경은 막지 않습니다.
- **일반 함수로 콜백을 작성해 `this`가 예상과 다르게 바뀌는 실수**: 클래스 메서드를 콜백으로 넘길 때는 화살표 함수나 `.bind(this)`가 필요합니다.

## 실무 체크리스트

- 재할당이 필요 없는 변수는 `const`, 필요한 경우만 `let`을 쓰고 있는가?
- 콜백 함수에서 `this`가 예상한 컨텍스트를 가리키는지 확인했는가?
- 배열을 변경할 때 원본을 직접 바꾸는 메서드(`push`, `splice` 등)와 새 배열을 반환하는 메서드(`concat`, `map` 등)를 구분해서 쓰고 있는가?

## 연습 과제

### 기초(★☆☆)
- `var`와 `let`으로 각각 반복문을 작성하고, `setTimeout` 콜백 안에서 반복 변수 값이 어떻게 다르게 출력되는지 확인해보세요.

### 중급(★★☆)
- 위 `initialState` 객체에서 `todos` 배열의 두 번째 항목의 `done`을 `true`로 바꾼 **새 객체**(원본은 그대로 두고)를 만들어보세요.

### 고급(★★★)
- 화살표 함수와 일반 함수로 각각 클래스 메서드를 정의하고, 이벤트 핸들러로 전달했을 때 `this`가 어떻게 달라지는지 콘솔로 확인해보세요.

## 요약

- `const`를 기본으로 쓰고, 재할당이 필요할 때만 `let`을 쓴다. `var`는 쓰지 않는다.
- 화살표 함수는 자신만의 `this`를 만들지 않고, 정의된 위치의 `this`를 그대로 사용한다.
- Redux의 상태는 객체와 배열의 조합이며, 원본을 바꾸지 않는 메서드(`concat`, `map`)에 익숙해져야 한다.

## 참고 문헌 및 출처(추천)

- MDN Web Docs, "let" — 블록 스코프와 Temporal Dead Zone
- MDN Web Docs, "Arrow function expressions" — 화살표 함수의 `this` 바인딩 규칙
- Kyle Simpson, 『You Don't Know JS: Scope & Closures』(2014) — 스코프와 클로저의 심화 원리

---

## 다음 글

- 다음: [02. ES6+ 필수 문법 - 구조 분해, 스프레드, 템플릿 리터럴](../es6-essential-syntax/)
