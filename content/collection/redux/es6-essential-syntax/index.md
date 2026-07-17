---
title: "[Redux] 02. ES6+ 필수 문법 - 구조 분해, 스프레드, 템플릿 리터럴"
description: "Redux 리듀서 코드의 대부분은 구조 분해와 스프레드 연산자로 이루어져 있습니다. 원본을 바꾸지 않고 새 객체·배열을 만드는 이 두 문법을 정확히 익히면 08편의 불변성 원칙이 훨씬 쉬워집니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 2
draft: false
slug: es6-essential-syntax
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
  - How-To
  - Guide(가이드)
  - Documentation(문서화)
  - Reference(참고)
  - Software-Architecture(소프트웨어아키텍처)
  - Clean-Code(클린코드)
  - Immutability
  - 구조분해할당
  - 스프레드연산자
  - 나머지매개변수
  - 템플릿리터럴
  - 얕은복사
  - 불변성
  - 리듀서문법
  - Implementation(구현)
---

# 02. ES6+ 필수 문법 - 구조 분해, 스프레드, 템플릿 리터럴

이 편에서 다루는 세 가지 문법(구조 분해, 스프레드, 템플릿 리터럴)은 Redux 리듀서 코드 어디에나 등장합니다. "원본은 그대로 두고 새 값을 만든다"는 08편의 불변성 원칙을 실제 코드로 표현하는 도구가 바로 이것입니다.

## 학습 목표

- 구조 분해 할당으로 객체·배열에서 필요한 값만 꺼낼 수 있다.
- 스프레드 연산자로 원본을 바꾸지 않고 새 객체·배열을 만들 수 있다.
- 템플릿 리터럴로 가독성 좋은 문자열을 조합할 수 있다.

## 구조 분해 할당: 필요한 값만 꺼낸다

**구조 분해 할당(Destructuring Assignment)**은 객체나 배열에서 필요한 값만 변수로 꺼내는 문법입니다.

```javascript
const user = { id: 1, name: "Kim", role: "admin" };

// 기존 방식
const id = user.id;
const name = user.name;

// 구조 분해
const { id: userId, name: userName, role = "guest" } = user;
console.log(userId, userName, role); // 1 "Kim" "admin"
```

`role = "guest"`처럼 **기본값**을 지정하면, 해당 속성이 없을 때만 기본값이 사용됩니다. 배열에서도 순서 기반으로 구조 분해할 수 있습니다.

```javascript
const [first, second, ...rest] = [10, 20, 30, 40];
console.log(first, second, rest); // 10 20 [30, 40]
```

React 컴포넌트에서 `useSelector`, `useDispatch`의 반환값이나 props를 다룰 때 구조 분해를 거의 항상 사용하게 됩니다(12편에서 다룹니다).

## 스프레드 연산자: 원본을 바꾸지 않고 복사·병합한다

**스프레드 연산자(`...`)**는 객체나 배열의 내용을 펼쳐서 새로운 객체·배열에 담습니다.

```javascript
const original = { count: 0, step: 1 };

// 원본을 바꾸지 않고 count만 변경한 새 객체 생성
const updated = { ...original, count: original.count + 1 };

console.log(original); // { count: 0, step: 1 } — 원본 그대로
console.log(updated);  // { count: 1, step: 1 } — 새 객체
```

이 패턴 `{ ...state, someField: newValue }`가 Redux 리듀서의 가장 흔한 형태입니다. 배열에도 동일하게 적용됩니다.

```javascript
const todos = [{ id: 1, text: "학습", done: false }];

// 새 항목을 추가한 새 배열
const withNewTodo = [...todos, { id: 2, text: "복습", done: false }];

// 특정 항목만 업데이트한 새 배열
const withToggled = todos.map((todo) =>
  todo.id === 1 ? { ...todo, done: true } : todo
);
```

**주의**: 스프레드는 **얕은 복사(shallow copy)**입니다. 중첩된 객체까지 복사하지 않습니다.

```javascript
const state = { user: { name: "Kim" }, count: 0 };
const copied = { ...state };

copied.user.name = "Lee";
console.log(state.user.name); // "Lee" — 중첩 객체는 참조를 공유하므로 원본도 바뀜!
```

중첩된 값을 안전하게 바꾸려면 중첩 단계마다 스프레드를 적용해야 합니다.

```javascript
const safeCopy = { ...state, user: { ...state.user, name: "Lee" } };
```

이 "얕은 복사의 함정"은 08편(불변성)에서 다시 자세히 다룹니다.

## 나머지 매개변수: 가변 인자를 배열로 받는다

**나머지 매개변수(Rest Parameter)**는 함수가 임의 개수의 인자를 배열로 받게 해줍니다. 구조 분해의 `...rest`와 문법은 같지만 위치가 다릅니다.

```javascript
function createAction(type, ...payloadArgs) {
  return { type, payload: payloadArgs };
}

console.log(createAction("cart/add", "apple", 2));
// { type: "cart/add", payload: ["apple", 2] }
```

## 템플릿 리터럴: 문자열을 조합한다

**템플릿 리터럴**은 백틱(`` ` ``)으로 감싸고 `${}` 안에 표현식을 넣어 문자열을 조합합니다.

```javascript
const domain = "cart";
const event = "itemAdded";

// 기존 방식
const actionType1 = domain + "/" + event;

// 템플릿 리터럴
const actionType2 = `${domain}/${event}`;

console.log(actionType1 === actionType2); // true
```

Redux 액션 타입을 `"cart/itemAdded"`처럼 `도메인/이벤트` 형식으로 짓는 관례가 많은데, 템플릿 리터럴을 쓰면 오타 없이 일관되게 조합할 수 있습니다.

## 흔한 실수

- **스프레드가 깊은 복사라고 착각하는 실수**: 중첩 객체는 참조가 공유되므로, 중첩된 부분을 바꾸려면 중첩 단계마다 스프레드해야 합니다.
- **배열 스프레드 순서를 잘못 배치해 값이 덮어써지는 실수**: `{ ...defaults, ...overrides }`처럼 **나중에 오는 값이 우선**한다는 규칙을 기억해야 합니다.
- **구조 분해에서 기본값을 `null`에는 적용하지 못한다는 것을 모르는 실수**: 기본값은 값이 `undefined`일 때만 적용되고, `null`일 때는 적용되지 않습니다.

## 실무 체크리스트

- 객체를 업데이트할 때 `{ ...state, field: value }` 패턴을 일관되게 쓰고 있는가?
- 중첩된 객체를 업데이트할 때 중첩 단계마다 스프레드를 적용했는가?
- 스프레드로 여러 출처를 병합할 때 우선순위(나중에 오는 값이 이긴다)를 의도한 대로 배치했는가?

## 연습 과제

### 기초(★☆☆)
- `{ id: 1, name: "Kim", email: "kim@test.com" }`에서 구조 분해로 `name`만 꺼내고, 나머지 속성은 `rest`라는 이름으로 한 번에 묶어보세요.

### 중급(★★☆)
- `{ user: { profile: { age: 20 } } }` 형태의 중첩 객체에서, `age`만 21로 바꾼 새 객체를 스프레드로 만들어보세요(원본은 그대로 유지).

### 고급(★★★)
- 여러 부분 상태 객체(`{ ...defaults }`, `{ ...userPrefs }`, `{ ...sessionOverrides }`)를 순서대로 병합해 최종 설정 객체를 만들고, 어떤 값이 최종적으로 우선하는지 규칙을 코드 주석으로 설명해보세요.

## 요약

- 구조 분해로 객체·배열에서 필요한 값만 명확하게 꺼낸다.
- 스프레드는 원본을 바꾸지 않고 새 객체·배열을 만들지만, 얕은 복사이므로 중첩 구조는 단계마다 펼쳐야 한다.
- 템플릿 리터럴로 문자열을 안전하고 읽기 쉽게 조합한다.

## 참고 문헌 및 출처(추천)

- MDN Web Docs, "Spread syntax (...)" — 스프레드 연산자의 정확한 동작 범위
- MDN Web Docs, "Destructuring assignment" — 구조 분해의 전체 문법
- ECMAScript 2015 (ES6) Language Specification — 스프레드·구조 분해 표준 정의

---

## 다음 글

- 다음: [03. 배열과 객체 다루기 - map, filter, reduce](../array-object-manipulation/)
