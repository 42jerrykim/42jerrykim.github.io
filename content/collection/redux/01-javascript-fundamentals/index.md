---
draft: true
title: "[Redux] 01. JavaScript 핵심 개념 - 변수, 함수, 객체"
date: 2025-10-14
lastmod: 2025-10-14
tags: ["Redux", "JavaScript", "변수", "함수", "객체", "기초", "var", "let", "const", "화살표함수", "Arrow Function", "ES6", "프로그래밍기초", "웹개발", "프론트엔드", "초보자", "입문", "JavaScript Basics", "Variables", "Functions", "Objects", "Fundamentals", "Beginner", "Web Development", "Frontend", "Programming", "Coding", "Software Development", "JS Tutorial", "Learn JavaScript", "JavaScript Guide", "코딩", "개발", "자바스크립트입문", "자바스크립트기초", "변수선언", "함수정의", "객체조작", "배열기초", "데이터타입", "스코프", "호이스팅", "this키워드", "프로토타입", "클로저", "Scope", "Hoisting", "Prototype"]
description: "JavaScript 입문자를 위한 핵심 개념 완벽 가이드. var, let, const 변수 선언부터 화살표 함수, 객체와 배열 조작까지 Redux 학습을 위한 필수 JavaScript 기초를 단계별로 마스터합니다"
series: ["Redux 완전 정복"]
series_order: 1
---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- ✅ var, let, const의 차이점을 이해하고 적절히 사용
- ✅ 일반 함수와 화살표 함수의 차이를 알고 상황에 맞게 선택
- ✅ 객체와 배열을 생성하고 조작하는 방법 숙지
- ✅ Redux에서 사용되는 JavaScript 패턴 이해

## 왜 이것을 배워야 할까요?

Redux를 배우기 전에 JavaScript 기초가 탄탄해야 하는 이유:

1. **Redux는 순수 JavaScript입니다**: Redux의 Action, Reducer는 모두 JavaScript 함수와 객체입니다
2. **불변성 관리**: 객체와 배열을 다루는 방법을 알아야 Redux의 불변성 원칙을 이해할 수 있습니다
3. **함수형 프로그래밍**: Redux는 함수형 프로그래밍 패러다임을 따릅니다

## 1. 변수 선언 - var, let, const

### 1.1 var의 문제점

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

**문제점**:
- 블록 스코프가 아닌 함수 스코프
- 재선언 가능 (실수 유발)
- 호이스팅으로 인한 혼란

### 1.2 let - 재할당 가능한 변수

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

**사용 시기**: 값이 변경될 수 있는 변수

### 1.3 const - 재할당 불가능한 상수

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

**Redux에서의 활용**:
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

**원칙**: 
1. 기본적으로 `const` 사용
2. 재할당이 필요하면 `let` 사용
3. `var`는 사용하지 않기

## 2. 함수 정의

### 2.1 함수 선언문 (Function Declaration)

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

### 2.2 함수 표현식 (Function Expression)

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

### 2.3 화살표 함수 (Arrow Function) ⭐

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

### 2.4 this 바인딩 차이 ⚠️

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

## 3. 객체 (Object)

### 3.1 객체 생성과 접근

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

### 3.2 객체 속성 추가/수정/삭제

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

### 3.3 객체 메서드

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

### 3.4 Redux State 예제

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

## 4. 배열 (Array)

### 4.1 배열 생성과 접근

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

### 4.2 배열 기본 메서드

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

### 4.3 불변성을 지키는 방법 (Redux 중요! ⭐)

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

### 4.4 Redux Todo 예제

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

## 5. 실습 문제 🏋️‍♂️

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

## 6. 흔한 실수와 해결법 ⚠️

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

## 7. 체크리스트 ✅

학습을 완료했다면 다음을 확인하세요:

- [ ] var, let, const의 차이를 설명할 수 있다
- [ ] 화살표 함수를 작성할 수 있다
- [ ] 화살표 함수와 일반 함수의 차이(this)를 안다
- [ ] 객체를 생성하고 속성에 접근할 수 있다
- [ ] 배열을 생성하고 기본 메서드를 사용할 수 있다
- [ ] 불변성을 유지하며 객체/배열을 수정할 수 있다
- [ ] 스프레드 연산자(...)를 사용할 수 있다
- [ ] 실습 문제를 모두 해결했다

## 8. 다음 단계 🚀

축하합니다! JavaScript 핵심 개념을 익혔습니다.

**다음 챕터 예고**: 
`02. ES6+ 필수 문법 - 구조 분해, 스프레드, 템플릿 리터럴`에서는 Redux 코드를 더 간결하게 만들어주는 현대적인 JavaScript 문법을 배웁니다.

### 추가 학습 자료

- [MDN - JavaScript 기초](https://developer.mozilla.org/ko/docs/Learn/JavaScript/First_steps)
- [JavaScript.info - 기본](https://ko.javascript.info/first-steps)
- [ES6 In Depth](https://hacks.mozilla.org/category/es6-in-depth/)

---

**핵심 요약**: Redux를 잘 사용하려면 JavaScript 기초가 중요합니다. 특히 **불변성**과 **화살표 함수**는 Redux의 핵심 개념이니 확실히 이해하고 넘어가세요! 💪

