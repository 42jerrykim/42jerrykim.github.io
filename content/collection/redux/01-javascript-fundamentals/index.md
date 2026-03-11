---
draft: true
title: "[Redux] 01. JavaScript 핵심 개념 - 변수, 함수, 객체"
date: 2025-10-14
lastmod: 2025-10-14
description: "JavaScript 입문자를 위한 핵심 개념 완벽 가이드. var, let, const 변수 선언부터 화살표 함수, 객체와 배열 조작까지 Redux 학습을 위한 필수 JavaScript 기초를 단계별로 마스터합니다."
slug: javascript-fundamentals
tags:
  - JavaScript
  - TypeScript
  - React
  - Frontend
  - 프론트엔드
  - Web
  - 웹
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - Functional-Programming
  - 함수형프로그래밍
  - Data-Structures
  - 자료구조
  - Array
  - 배열
  - Refactoring
  - 리팩토링
  - Testing
  - 테스트
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - Beginner
  - Reference
  - 참고
  - Readability
  - Maintainability
  - Modularity
  - Interface
  - 인터페이스
  - Encapsulation
  - 캡슐화
  - Documentation
  - 문서화
  - Error-Handling
  - 에러처리
  - Pitfalls
  - 함정
  - Edge-Cases
  - 엣지케이스
  - Debugging
  - 디버깅
  - Performance
  - 성능
  - Type-Safety
  - Git
  - IDE
  - VSCode
  - How-To
  - Tips
  - Technology
  - 기술
  - Education
  - 교육
  - 실습
  - Case-Study
  - Comparison
  - 비교
  - JSON
  - HTTP
  - API
  - Async
  - 비동기
  - State
  - Observer
  - Event-Driven
  - Caching
  - 캐싱
  - Scalability
  - 확장성
  - Deep-Dive
  - Workflow
  - 워크플로우
series: ["Redux 완전 정복"]
series_order: 1
---

이 장에서는 **Redux 코드를 읽고 작성하는 데 꼭 필요한 JavaScript 기초**만 골라 다룹니다. Redux의 Action, Reducer, state는 모두 JavaScript의 **변수·함수·객체·배열**로 이루어져 있기 때문에, 이 기초가 없으면 "코드는 보이는데 무슨 뜻인지 모르겠다"는 상태가 됩니다. 01장을 마치면 02(ES6+ 문법)와 06(Redux란 무엇인가)으로 넘어갈 준비가 됩니다.

## 이 글을 읽은 후 달성해야 할 목표 (평가 기준)

이 챕터를 마치면 다음을 할 수 있어야 합니다:

- **var**, **let**, **const**의 차이(스코프, 재선언, 호이스팅)를 설명하고 상황에 맞게 선택할 수 있다.
- 일반 함수와 화살표 함수의 차이(특히 **this** 바인딩)를 설명하고, Redux Action Creator 등에서 적절히 선택할 수 있다.
- 객체와 배열을 생성·조작하고, **불변성**을 유지하며 수정하는 패턴을 코드로 작성할 수 있다.
- Redux에서 자주 쓰는 JavaScript 패턴(상수 Action Type, 화살표 함수 반환 객체, 스프레드)을 설명할 수 있다.

## 왜 이것을 배워야 할까요?

Redux를 배우기 전에 JavaScript 기초가 탄탄해야 하는 이유:

1. **Redux는 순수 JavaScript입니다**: Redux의 Action, Reducer는 모두 JavaScript 함수와 객체입니다
2. **불변성 관리**: 객체와 배열을 다루는 방법을 알아야 Redux의 불변성 원칙을 이해할 수 있습니다
3. **함수형 프로그래밍**: Redux는 함수형 프로그래밍 패러다임을 따릅니다

## 변수 선언 - var, let, const

이 절에서는 **var, let, const**의 차이를 이해하고, Redux 코드에서 왜 **const**와 **let**만 쓰는지** 알 수 있도록 정리합니다. 변수 선언 방식에 따라 스코프(범위)와 재할당 가능 여부가 달라지므로, 먼저 세 가지를 구분하는 것이 중요합니다.

### var의 문제점

**var**는 예전 JavaScript의 유일한 변수 선언 키워드였지만, 블록 스코프가 없고 재선언·호이스팅 때문에 실수가 나오기 쉽습니다. 아래 코드는 **함수 스코프**, **재선언**, **호이스팅**이 각각 어떤 동작을 하는지 보여 줍니다. Redux 예제에서는 var를 쓰지 않고 let/const만 쓰는 것이 권장됩니다.

```javascript
// var는 함수 스코프를 가집니다
function varExample() {
    if (true) {
        var x = 10;
    }
    console.log(x); // 10 - 블록 밖에서도 접근 가능! (문제)
}

// var는 재선언이 가능합니다
var name = "Alice";
var name = "Bob"; // 에러 없이 덮어써짐 (문제)

// var는 호이스팅됩니다
console.log(y); // undefined (에러가 아님!)
var y = 5;
```

**문제점**: 블록 스코프가 아닌 함수 스코프라서 블록 안에서 선언한 변수가 밖에서도 보이고, 재선언이 허용되어 같은 이름을 실수로 두 번 선언해도 에러가 나지 않으며, 호이스팅 때문에 선언 전에 사용해도 undefined가 나와 디버깅이 어렵습니다. 그래서 현대적인 Redux/React 코드에서는 var 대신 **let**과 **const**만 사용합니다.

### let - 재할당 가능한 변수

**let**은 블록 스코프를 가지며, 같은 블록 안에서 재선언할 수 없습니다. 반면 **재할당**(값을 바꾸는 것)은 가능하므로, 루프 카운터나 조건에 따라 바뀌어야 하는 변수에 씁니다. 아래 예는 블록 안에서만 유효한 let 변수와, 블록 밖에서는 참조할 수 없음을 보여 줍니다.

```javascript
// let은 블록 스코프를 가집니다
function letExample() {
    if (true) {
        let x = 10;
        console.log(x); // 10
    }
    // console.log(x); // ReferenceError: x is not defined
}

// let은 재선언이 불가능합니다
let name = "Alice";
// let name = "Bob"; // SyntaxError

// 하지만 재할당은 가능합니다
let count = 0;
count = 1; // OK
count = 2; // OK
```

**사용 시기**: 값이 변경될 수 있는 변수. 블록 밖에서 let으로 선언한 변수를 참조하면 ReferenceError가 나오므로, Redux에서 반복문이나 조건문 안의 임시 변수는 let으로 두면 스코프가 명확해집니다.

### const - 재할당 불가능한 상수

**const**는 한 번 할당한 값을 다시 할당할 수 없게 만듭니다. 객체나 배열을 const로 선언해도 **그 안의 속성이나 요소는 수정 가능**하므로, "참조는 고정하고 내용만 바꾸는" Redux state 패턴과 잘 맞습니다. 아래는 const의 초기화 의무, 재할당 불가, 그리고 객체·배열의 내용 수정은 허용됨을 보여 줍니다.

```javascript
// const는 반드시 초기화해야 합니다
// const x; // SyntaxError

const PI = 3.14159;
// PI = 3.14; // TypeError: Assignment to constant variable

// 객체의 경우 참조는 변경 불가, 내용은 변경 가능
const person = { name: "Alice" };
person.name = "Bob"; // OK (객체 내용 변경)
// person = {}; // Error (새로운 객체 할당 불가)

// 배열도 마찬가지
const numbers = [1, 2, 3];
numbers.push(4); // OK
// numbers = []; // Error
```

객체·배열은 **참조만 바꾸지 않으면** const로 선언한 뒤 속성·요소를 수정해도 됩니다. 다만 Redux에서는 "기존 객체를 수정하지 않고 새 객체를 반환"하는 불변성 규칙을 지키므로, 실전에서는 스프레드 등으로 새 객체/배열을 만들어 할당하는 방식을 씁니다.

**Redux에서의 활용**: Action Type 상수나 초기 state처럼 **다시 바꿀 일이 없는 값**은 const로 두는 것이 Redux 코드에서의 관례입니다. 아래처럼 상수와 초기 상태를 const로 선언합니다.

```javascript
// Redux에서는 대부분 const를 사용합니다
const INCREMENT = 'INCREMENT';  // Action Type
const initialState = { count: 0 };  // 초기 상태
```

### 변수 선언 가이드라인

```javascript
// ❌ 나쁜 예 - var 사용
var userId = 123;

// ✅ 좋은 예 - const 우선, 필요시 let
const userId = 123;
let counter = 0;

// Redux 스타일
const ADD_TODO = 'ADD_TODO';
const todos = [];
```

실무에서는 이 가이드라인대로 const를 기본으로 두면 스코프와 재할당 여부가 코드만 봐도 분명해져 Redux 코드 리뷰나 디버깅에 유리합니다.

**원칙**: 
1. 기본적으로 `const` 사용
2. 재할당이 필요하면 `let` 사용
3. `var`는 사용하지 않기

이 가이드라인을 지키면 스코프와 재할당 여부가 코드만 봐도 분명해져서, Redux 코드 리뷰나 디버깅 시 유리합니다.

### 변수 선언 한눈에 보기

| 선언 | 스코프 | 재선언 | 재할당 | Redux에서 활용 |
|------|--------|--------|--------|----------------|
| **var** | 함수 스코프 | 가능 | 가능 | 사용 지양 (예측 어려움) |
| **let** | 블록 스코프 | 불가 | 가능 | 반복문·재할당 필요 시 |
| **const** | 블록 스코프 | 불가 | 불가 | Action Type, 초기 상태, 대부분의 식별자 |

## 함수 정의

변수 다음으로 **함수**를 정리합니다. Redux의 reducer, action creator, selector는 모두 함수이므로, **일반 함수와 화살표 함수의 차이**, 특히 **this 바인딩**을 알아 두어야 합니다. 이 절에서는 함수 선언문·함수 표현식·화살표 함수를 비교하고, Redux 코드에서 자주 쓰는 형태를 짚습니다.

### 함수 선언문 (Function Declaration)

**함수 선언문**은 `function` 키워드와 이름으로 정의하며, 호이스팅되어 선언 전에도 호출할 수 있습니다. 아래 예는 선언문으로 정의한 함수를 호출하는 기본 형태입니다. Redux만 보면 선언문보다 **화살표 함수**를 더 자주 쓰지만, 재귀나 메서드처럼 이름이 필요할 때는 선언문도 씁니다.

```javascript
// 전통적인 함수 선언
function add(a, b) {
    return a + b;
}

console.log(add(2, 3)); // 5

// 호이스팅됨 - 선언 전에 호출 가능
greet("Alice"); // "Hello, Alice"

function greet(name) {
    return `Hello, ${name}`;
}
```

함수 선언문은 스크립트나 함수 스코프 전체로 호이스팅되므로, 코드 순서상 아래에 정의해도 위에서 호출할 수 있습니다. 단, Redux reducer나 action creator는 보통 **화살표 함수**로 짧게 쓰는 패턴이 많습니다.

### 함수 표현식 (Function Expression)

**함수 표현식**은 변수에 함수를 할당하는 형태입니다. **호이스팅되지 않아** 선언 전에는 호출할 수 없고, 화살표 함수나 콜백을 변수에 넣을 때와 같은 방식입니다. 아래는 표현식으로 함수를 만든 뒤, 그 변수를 통해 호출하는 예입니다.

```javascript
// 함수를 변수에 할당
const subtract = function(a, b) {
    return a - b;
};

console.log(subtract(5, 3)); // 2

// 호이스팅 안 됨
// multiply(2, 3); // TypeError: multiply is not a function

const multiply = function(a, b) {
    return a * b;
};
```

표현식은 "함수도 값이다"를 보여 주며, Redux에서 `const increment = () => ({ type: 'INCREMENT' })`처럼 action creator를 만드는 방식과 같은 패턴입니다.

### 화살표 함수 (Arrow Function) ⭐

Redux 코드에서 **가장 많이 쓰는 형태**가 화살표 함수입니다. `function` 키워드 없이 `=>`로 정의하고, 인자가 하나일 때 괄호 생략, 본문이 return 한 줄이면 중괄호·return 생략이 가능합니다. 아래는 다양한 화살표 함수 문법과, Redux 스타일의 action creator 예시입니다.

```javascript
// 기본 형태
const divide = (a, b) => {
    return a / b;
};

// 한 줄일 때 중괄호와 return 생략 가능
const square = x => x * x;

// 매개변수가 없을 때
const getRandom = () => Math.random();

// 매개변수가 여러 개일 때
const sum = (a, b, c) => a + b + c;

// 객체 리터럴 반환 시 괄호로 감싸기
const createPerson = (name, age) => ({ name, age });

console.log(createPerson("Alice", 25)); 
// { name: "Alice", age: 25 }
```

### this 바인딩 차이 ⚠️

```javascript
// 일반 함수: this는 호출 방식에 따라 결정
const obj1 = {
    name: "Object 1",
    greet: function() {
        console.log(this.name);
    }
};
obj1.greet(); // "Object 1"

// 화살표 함수: this는 상위 스코프의 this를 사용
const obj2 = {
    name: "Object 2",
    greet: () => {
        console.log(this.name); // undefined (전역 this)
    }
};
obj2.greet(); // undefined

// Redux에서의 활용
const actionCreator = (payload) => ({
    type: 'ADD_TODO',
    payload
});
```

**Redux에서 화살표 함수를 선호하는 이유**:
- 간결한 문법
- this 바인딩 문제 없음
- 암묵적 반환으로 Action 객체 생성이 쉬움

## 객체 (Object)

Redux의 **state**는 대부분 **객체** 또는 객체가 중첩된 형태입니다. 이 절에서는 객체 생성·속성 접근·수정·삭제와, Redux에서 state를 다룰 때 자주 쓰는 패턴을 정리합니다. "불변성"은 다음 배열 절에서 스프레드와 함께 다루지만, 객체도 "기존 객체를 수정하지 않고 새 객체를 반환"하는 Redux 원칙을 따릅니다.

### 객체 생성과 접근

객체는 **키-값 쌍**의 집합이며, 리터럴 `{}`로 만들고 점(`.`) 또는 대괄호(`['key']`)로 접근합니다. 아래는 객체 생성, 속성 읽기, 그리고 Redux state에서 자주 보는 중첩 접근 방식을 보여 줍니다.

```javascript
// 객체 리터럴
const user = {
    name: "Alice",
    age: 25,
    email: "alice@example.com"
};

// 점 표기법
console.log(user.name); // "Alice"

// 대괄호 표기법
console.log(user["email"]); // "alice@example.com"

// 동적 속성 접근
const key = "age";
console.log(user[key]); // 25
```

### 객체 속성 추가/수정/삭제

```javascript
const person = { name: "Bob" };

// 추가
person.age = 30;
person["city"] = "Seoul";

// 수정
person.name = "Robert";

// 삭제
delete person.city;

console.log(person); // { name: "Robert", age: 30 }
```

### 객체 메서드

```javascript
const calculator = {
    value: 0,
    add: function(n) {
        this.value += n;
        return this;
    },
    subtract: function(n) {
        this.value -= n;
        return this;
    },
    // ES6 단축 메서드
    multiply(n) {
        this.value *= n;
        return this;
    }
};

// 메서드 체이닝
calculator.add(10).subtract(3).multiply(2);
console.log(calculator.value); // 14
```

### Redux State 예제

```javascript
// Redux의 State는 보통 객체입니다
const reduxState = {
    user: {
        id: 1,
        name: "Alice",
        isLoggedIn: true
    },
    todos: [
        { id: 1, text: "Learn Redux", completed: false },
        { id: 2, text: "Build App", completed: false }
    ],
    filters: {
        status: "all",
        search: ""
    }
};

// State 접근
console.log(reduxState.user.name); // "Alice"
console.log(reduxState.todos[0].text); // "Learn Redux"
```

## 배열 (Array)

Redux에서 **목록 형태의 state**(예: todo 목록, 댓글 목록)는 **배열**로 다룹니다. 이 절에서는 배열 생성·접근·자주 쓰는 메서드와, **불변성을 지키며** 배열을 수정하는 방법(스프레드, map, filter 등)을 다룹니다. Redux reducer에서는 원본 배열을 바꾸지 않고 새 배열을 반환하는 것이 핵심입니다.

### 배열 생성과 접근

배열은 `[]` 리터럴이나 `Array` 생성자로 만들고, 인덱스로 요소에 접근합니다. 아래는 배열 생성, 인덱스 접근, length, 그리고 Redux에서 자주 쓰는 순회의 기본 형태입니다.

```javascript
// 배열 리터럴
const fruits = ["apple", "banana", "orange"];

// 인덱스로 접근 (0부터 시작)
console.log(fruits[0]); // "apple"
console.log(fruits[2]); // "orange"

// 배열 길이
console.log(fruits.length); // 3

// 마지막 요소 접근
console.log(fruits[fruits.length - 1]); // "orange"
```

### 배열 기본 메서드

```javascript
const numbers = [1, 2, 3];

// push - 끝에 추가 (원본 변경 ⚠️)
numbers.push(4);
console.log(numbers); // [1, 2, 3, 4]

// pop - 끝에서 제거 (원본 변경 ⚠️)
const last = numbers.pop();
console.log(last); // 4
console.log(numbers); // [1, 2, 3]

// unshift - 앞에 추가 (원본 변경 ⚠️)
numbers.unshift(0);
console.log(numbers); // [0, 1, 2, 3]

// shift - 앞에서 제거 (원본 변경 ⚠️)
const first = numbers.shift();
console.log(first); // 0
console.log(numbers); // [1, 2, 3]
```

### 불변성을 지키는 방법 (Redux 중요! ⭐)

Redux에서는 **기존 배열을 수정하지 않고 새 배열을 만들어 반환**해야 합니다. `push`, `splice`처럼 원본을 바꾸는 메서드 대신 **스프레드(`...`)**, **map**, **filter**, **slice**를 사용합니다. 아래 첫 번째 예는 스프레드로 새 배열을 만드는 패턴이고, 두 번째는 map/filter로 항목 추가·삭제·수정을 불변하게 하는 패턴입니다.

```javascript
const original = [1, 2, 3];

// ❌ 나쁜 예 - 원본 수정
original.push(4); // 원본이 변경됨

// ✅ 좋은 예 - 새 배열 생성
const added = [...original, 4]; // [1, 2, 3, 4]
const removed = original.filter(n => n !== 2); // [1, 3]
const updated = original.map(n => n * 2); // [2, 4, 6]

console.log(original); // [1, 2, 3, 4] - 이미 변경됨 😢
```

위에서 본 스프레드·filter·map을 reducer 안에서 쓰려면, "추가·삭제·수정"을 각각 **순수 함수**로 두는 패턴이 유용합니다. 아래는 그 패턴을 Redux 스타일로 정리한 것입니다. reducer에서는 이렇게 새 배열을 반환하면 됩니다.

**Redux 스타일 (불변성 유지)**:
```javascript
// 추가
const addItem = (arr, item) => [...arr, item];

// 삭제
const removeItem = (arr, index) => [
    ...arr.slice(0, index),
    ...arr.slice(index + 1)
];

// 수정
const updateItem = (arr, index, newValue) => [
    ...arr.slice(0, index),
    newValue,
    ...arr.slice(index + 1)
];

// 또는 map 사용
const updateItemWithMap = (arr, index, newValue) =>
    arr.map((item, i) => i === index ? newValue : item);
```

### Redux Todo 예제

```javascript
// Redux에서 Todo 추가
const todos = [
    { id: 1, text: "Learn JS", completed: false }
];

// 새로운 Todo 추가 (불변성 유지)
const newTodos = [
    ...todos,
    { id: 2, text: "Learn Redux", completed: false }
];

// Todo 완료 처리 (불변성 유지)
const completedTodos = todos.map(todo =>
    todo.id === 1
        ? { ...todo, completed: true }
        : todo
);
```

## 실습 문제 🏋️‍♂️

### 문제 1: 변수 선언
```javascript
// TODO: const와 let을 적절히 사용하여 작성하세요
// 1. 사용자 이름 (변경 불가)
// 2. 나이 (변경 가능)
// 3. 취미 배열 (내용 추가 가능, 재할당 불가)

// 답안:
const userName = "Alice";
let userAge = 25;
const hobbies = ["reading", "coding"];
hobbies.push("gaming"); // OK
// hobbies = []; // Error
```

### 문제 2: 화살표 함수
```javascript
// TODO: 다음 함수를 화살표 함수로 변환하세요

// 기존 함수
function double(x) {
    return x * 2;
}

function greet(name) {
    return `Hello, ${name}!`;
}

function createUser(name, age) {
    return { name: name, age: age };
}

// 답안:
const double = x => x * 2;
const greet = name => `Hello, ${name}!`;
const createUser = (name, age) => ({ name, age });
```

### 문제 3: 객체 조작
```javascript
// TODO: Redux State에서 사용자 정보 업데이트
const state = {
    user: { name: "Alice", age: 25 },
    isLoggedIn: false
};

// 1. 로그인 상태를 true로 변경 (불변성 유지)
// 2. 사용자 나이를 26으로 변경 (불변성 유지)

// 답안:
const newState1 = {
    ...state,
    isLoggedIn: true
};

const newState2 = {
    ...state,
    user: {
        ...state.user,
        age: 26
    }
};
```

### 문제 4: 배열 조작 (Redux 스타일)
```javascript
// TODO: 불변성을 유지하며 배열 조작
const todos = [
    { id: 1, text: "Learn JS", completed: false },
    { id: 2, text: "Learn React", completed: false }
];

// 1. id가 3인 새 todo 추가
// 2. id가 1인 todo의 completed를 true로 변경
// 3. id가 2인 todo 삭제

// 답안:
// 1. 추가
const addedTodos = [
    ...todos,
    { id: 3, text: "Learn Redux", completed: false }
];

// 2. 수정
const updatedTodos = todos.map(todo =>
    todo.id === 1
        ? { ...todo, completed: true }
        : todo
);

// 3. 삭제
const filteredTodos = todos.filter(todo => todo.id !== 2);
```

## 흔한 실수와 해결법 ⚠️

### 실수 1: var 사용
```javascript
// ❌ 나쁜 예
var count = 0;

// ✅ 좋은 예
const count = 0; // 또는 let count = 0;
```

### 실수 2: 원본 배열 수정
```javascript
// ❌ 나쁜 예
const state = { items: [1, 2, 3] };
state.items.push(4); // 원본 수정!

// ✅ 좋은 예
const newState = {
    ...state,
    items: [...state.items, 4]
};
```

### 실수 3: 객체 참조 공유
```javascript
// ❌ 나쁜 예
const user = { name: "Alice" };
const newUser = user;
newUser.name = "Bob";
console.log(user.name); // "Bob" - 원본도 변경됨!

// ✅ 좋은 예
const user = { name: "Alice" };
const newUser = { ...user, name: "Bob" };
console.log(user.name); // "Alice" - 원본 유지
```

### 실수 4: this 바인딩 혼동
```javascript
// ❌ 문제 발생
const obj = {
    value: 10,
    getValue: () => this.value // undefined
};

// ✅ 해결
const obj = {
    value: 10,
    getValue: function() { return this.value; }
    // 또는
    getValue() { return this.value; }
};
```

### 한계와 비판적 시각

- **var**는 레거시 코드에서만 만나게 되므로, 새 코드에서는 **let**/**const**만 사용하는 것이 좋습니다. 화살표 함수는 **this**가 없어 메서드나 생성자로 쓰기 부적합하므로, 객체 메서드는 일반 함수 또는 단축 메서드로 정의해야 합니다. **불변성** 유지는 Redux에서 필수이지만, 깊은 중첩 객체는 스프레드만으로는 불편하므로 08장에서 다루는 Immer 등 도구를 고려할 수 있습니다.

## 체크리스트 ✅

학습을 완료했다면 다음을 확인하세요:

- [ ] var, let, const의 차이를 설명할 수 있다
- [ ] 화살표 함수를 작성할 수 있다
- [ ] 화살표 함수와 일반 함수의 차이(this)를 안다
- [ ] 객체를 생성하고 속성에 접근할 수 있다
- [ ] 배열을 생성하고 기본 메서드를 사용할 수 있다
- [ ] 불변성을 유지하며 객체/배열을 수정할 수 있다
- [ ] 스프레드 연산자(...)를 사용할 수 있다
- [ ] 실습 문제를 모두 해결했다

## 다음 단계 🚀

축하합니다! JavaScript 핵심 개념을 익혔습니다.

**다음 챕터 예고**: [02. ES6+ 필수 문법 - 구조 분해, 스프레드, 템플릿 리터럴](../02-es6-essential-syntax/)에서는 Redux 코드를 더 간결하게 만들어주는 현대적인 JavaScript 문법을 배웁니다.

### 추가 학습 자료

- [MDN - JavaScript 기초](https://developer.mozilla.org/ko/docs/Learn/JavaScript/First_steps)
- [JavaScript.info - 기본](https://ko.javascript.info/first-steps)
- [ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/)

---

**핵심 요약**: Redux를 잘 사용하려면 JavaScript 기초가 중요합니다. 특히 **불변성**과 **화살표 함수**는 Redux의 핵심 개념이니 확실히 이해하고 넘어가세요! 💪

