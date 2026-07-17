---
title: "[Redux] 03. 배열과 객체 다루기 - map, filter, reduce"
description: "Redux의 selector와 리듀서는 map/filter/reduce 같은 고차 함수로 상태를 조회·변환합니다. 원본을 바꾸지 않는 배열·객체 메서드와 바꾸는 메서드를 명확히 구분해 불변성을 지키는 습관을 코드로 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 3
draft: false
slug: array-object-manipulation
image: "wordcloud.png"
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
  - Functional-Programming(함수형프로그래밍)
  - Readability
  - How-To
  - Guide(가이드)
  - Documentation(문서화)
  - Reference(참고)
  - Immutability
  - Performance(성능)
  - Edge-Cases(엣지케이스)
  - 고차함수
  - 맵필터리듀스
  - 순수함수
  - 불변성
  - 배열변경메서드
  - selector패턴
  - 함수합성
---

# 03. 배열과 객체 다루기 - map, filter, reduce

Redux의 리듀서와 selector는 대부분 배열을 "조회하고 변환"하는 작업입니다. `map`, `filter`, `reduce` 세 가지 고차 함수만 능숙하게 다뤄도 Redux 코드의 상당 부분을 읽고 쓸 수 있습니다.

## 학습 목표

- `map`, `filter`, `reduce`의 동작과 반환값을 정확히 설명할 수 있다.
- 원본을 바꾸는 배열 메서드와 바꾸지 않는 메서드를 구분해 리듀서에서 안전한 쪽만 쓸 수 있다.
- 세 함수를 조합해 상태에서 파생 데이터를 계산할 수 있다.

## map: 각 요소를 변환한 새 배열을 만든다

`map()`은 배열의 각 요소에 함수를 적용해 **같은 길이의 새 배열**을 반환합니다.

```javascript
const todos = [
  { id: 1, text: "학습", done: false },
  { id: 2, text: "복습", done: false },
];

// id가 1인 항목만 done: true로 바꾼 새 배열
const updated = todos.map((todo) =>
  todo.id === 1 ? { ...todo, done: true } : todo
);

console.log(todos[0].done);   // false — 원본은 그대로
console.log(updated[0].done); // true — 새 배열의 해당 항목만 변경됨
```

**핵심은 조건에 해당하지 않는 항목도 새 객체로 만들 필요는 없다는 것**입니다. 위 예제에서 `id`가 1이 아닌 항목은 원래 객체를 그대로 반환합니다(불필요한 새 객체 생성을 피해 리렌더 최적화에도 도움이 됩니다. 13편에서 다룹니다).

## filter: 조건을 만족하는 요소만 남긴다

`filter()`는 조건 함수가 `true`를 반환하는 요소만 모아 **새 배열**을 반환합니다.

```javascript
const activeTodos = todos.filter((todo) => !todo.done);
console.log(activeTodos.length); // 2 (아직 done: true인 항목이 없다면)
```

`filter()`로 특정 항목을 "삭제"하는 것도 흔한 패턴입니다. 원본 배열에서 해당 id를 제외한 새 배열을 만드는 방식이, 배열 메서드 `splice()`로 원본을 직접 자르는 것보다 Redux에서 안전합니다.

```javascript
const removeTodo = (state, idToRemove) => state.filter((todo) => todo.id !== idToRemove);
```

## reduce: 배열을 하나의 값으로 접는다

`reduce()`는 배열의 모든 요소를 순회하며 **누적값(accumulator)**을 만들어 갑니다. 이름 그대로 Redux의 "Reducer"라는 개념과 정확히 같은 발상입니다.

```javascript
const prices = [1000, 2000, 1500];

const total = prices.reduce((sum, price) => sum + price, 0);
console.log(total); // 4500
```

`reduce()`의 두 번째 인자(`0`)는 **초기 누적값**입니다. 이 초기값이 바로 Redux 리듀서의 `initialState`와 같은 역할을 합니다. 실제로 Redux의 `combineReducers`는 여러 리듀서를 실행하며 전체 상태 객체를 "누적"해 나가는데, 이는 `reduce()`의 발상을 상태 관리에 그대로 적용한 것입니다.

```javascript
// reduce로 배열을 객체(맵)로 변환 — Redux selector에서 자주 쓰는 패턴
const todosById = todos.reduce((acc, todo) => {
  acc[todo.id] = todo;
  return acc;
}, {});

console.log(todosById[1]); // { id: 1, text: "학습", done: false }
```

이 "배열 → id 기반 객체" 변환은 27편(정규화)에서 대규모 데이터를 다루는 핵심 기법으로 다시 등장합니다.

## 세 함수 조합하기

실무에서는 `map`/`filter`/`reduce`를 체이닝해 복잡한 파생 데이터를 계산합니다.

```javascript
const orders = [
  { id: 1, status: "confirmed", total: 10000 },
  { id: 2, status: "cancelled", total: 5000 },
  { id: 3, status: "confirmed", total: 20000 },
];

// 확정된 주문의 총액 합계
const confirmedTotal = orders
  .filter((order) => order.status === "confirmed")
  .map((order) => order.total)
  .reduce((sum, total) => sum + total, 0);

console.log(confirmedTotal); // 30000
```

이런 체이닝은 14편(Selector 패턴)에서 `useSelector`와 함께 쓰이며, 컴포넌트가 필요로 하는 파생 데이터를 상태로부터 계산하는 표준적인 방식이 됩니다.

## 객체 순회와 변환: Object.keys/values/entries

Redux 상태에서 배열 못지않게 자주 마주치는 형태가, 방금 `reduce()`로 만든 `todosById`처럼 **id를 키로 쓰는 객체**입니다. 이런 객체는 배열이 아니므로 `map`/`filter`를 바로 쓸 수 없습니다. JavaScript는 객체를 배열로 변환하는 세 가지 메서드로 이 문제를 해결합니다.

```javascript
Object.keys(todosById);   // ["1", "2"] — 키만 담은 배열
Object.values(todosById); // [{...}, {...}] — 값만 담은 배열
Object.entries(todosById); // [["1", {...}], ["2", {...}]] — [키, 값] 쌍의 배열
```

`Object.values()`로 객체를 배열로 바꾸고 나면, 앞서 배운 map/filter/reduce를 그대로 이어 쓸 수 있습니다. 예를 들어 완료된 todo 개수를 세려면 `Object.values(todosById).filter((todo) => todo.done).length`처럼 씁니다. 27편(정규화)에서 `state.entities`(id 기반 객체)로부터 목록을 뽑아낼 때 바로 이 패턴을 다시 사용합니다.

## 객체를 불변하게 업데이트하기: Object.assign과 스프레드

배열에 `push`/`splice`(변경)와 `concat`/`filter`(새 배열 반환)가 있듯, 객체에도 원본을 직접 바꾸는 방식과 새 객체를 반환하는 방식이 있습니다. 리듀서 안에서는 항상 새 객체를 반환하는 쪽을 씁니다.

```javascript
const todo = { id: 1, text: "학습", done: false };

// 나쁜 예: 원본 객체를 직접 변경
todo.done = true;

// 좋은 예 1: Object.assign의 첫 인자로 빈 객체를 넘겨 새 객체를 만든다
const updated1 = Object.assign({}, todo, { done: true });

// 좋은 예 2: 스프레드 연산자(02편)로 새 객체 생성 — 실무에서 더 널리 쓰인다
const updated2 = { ...todo, done: true };
```

`Object.assign({}, todo, { done: true })`은 빈 객체 `{}`에 `todo`의 속성을 먼저 복사하고, 그 위에 `{ done: true }`를 덮어씁니다. 첫 인자를 빈 객체가 아니라 `todo` 자체로 쓰면(`Object.assign(todo, { done: true })`) 원본을 직접 변경해버리는 흔한 실수가 됩니다. 02편에서 배운 스프레드 연산자가 같은 일을 더 짧고 안전하게 하므로, 실무에서는 스프레드를 더 많이 씁니다.

## 원본을 바꾸는 메서드는 리듀서에서 쓰지 않는다

JavaScript 배열 메서드 중 일부는 **원본을 직접 변경(mutate)**합니다. Redux 리듀서 안에서는 이런 메서드를 쓰면 안 됩니다.

| 원본을 바꾸는 메서드(리듀서에서 금지) | 새 배열/값을 반환하는 메서드(리듀서에서 사용) |
|---|---|
| `push()`, `pop()` | `concat()`, `[...arr, item]` |
| `splice()` | `slice()`, `filter()` |
| `sort()`, `reverse()` (원본 정렬) | `[...arr].sort()` (복사본 정렬) |
| 인덱스 직접 대입(`arr[0] = x`) | `map()`으로 새 배열 생성 |
| 객체 속성 직접 대입(`obj.x = y`) | `{ ...obj, x: y }` 또는 `Object.assign({}, obj, { x: y })` |

`sort()`와 `reverse()`는 특히 자주 놓치는 함정입니다. 정렬 자체는 새 배열을 반환하는 것처럼 보이지만, 실제로는 **원본 배열을 제자리에서 정렬한 뒤 그 원본을 반환**합니다.

```javascript
const numbers = [3, 1, 2];
const sorted = numbers.sort();
console.log(numbers === sorted); // true — 같은 배열! 원본이 정렬되어 버렸다

// 안전한 방법: 복사본을 만든 뒤 정렬
const safelySorted = [...numbers].sort();
```

## 실무 체크리스트

- `map`/`filter`로 새 배열을 만들 때, 조건에 해당하지 않는 항목까지 불필요하게 새 객체로 만들고 있지 않은가?
- `reduce`의 초기값 타입(배열/객체/숫자)이 최종적으로 원하는 결과 타입과 일치하는가?
- 리듀서 코드에 `push`, `splice`, `sort()`(원본 정렬), 객체 속성 직접 대입(`obj.x = y`) 같은 변경이 섞여 있지 않은가?

## 연습 과제

### 기초(★☆☆)
- `orders` 배열에서 `status`가 `"cancelled"`인 주문만 골라내는 `filter` 코드를 작성해보세요.

### 중급(★★☆)
- `todos` 배열을 `reduce`로 `{ done: [...], active: [...] }` 형태의 객체로 분류해보세요.
- `todosById` 객체에서 `Object.values()`와 `filter()`를 조합해 완료되지 않은 todo 개수를 구해보세요.

### 고급(★★★)
- `map`, `filter`, `reduce`를 체이닝해 "완료되지 않은 할 일 중 텍스트 길이가 5자 이상인 항목의 개수"를 계산하는 코드를 작성해보세요.

## 요약

- `map`은 변환, `filter`는 선별, `reduce`는 누적이라는 각자의 역할이 있고 조합해서 복잡한 파생 데이터를 계산한다.
- `reduce`의 발상(초기값 + 누적 함수)은 Redux 리듀서 개념과 본질적으로 같다.
- `Object.keys/values/entries`로 id 기반 객체를 배열로 바꾸면 map/filter/reduce를 그대로 이어 쓸 수 있고, 객체 업데이트는 스프레드나 `Object.assign({}, obj, patch)`로 새 객체를 반환해야 한다.
- 리듀서 안에서는 원본을 바꾸는 배열 메서드(`push`, `splice`, `sort()`)를 절대 쓰지 않는다.

## 참고 문헌 및 출처(추천)

- MDN Web Docs, "Array.prototype.reduce()" — reduce의 정확한 동작과 초기값 규칙
- MDN Web Docs, "Array.prototype.sort()" — sort가 원본을 변경한다는 명세
- Redux 공식 문서, "Immutable Update Patterns" — 배열/객체 불변 업데이트 패턴 목록

---

## 다음 글

- 다음: [04. 비동기 JavaScript - Promise와 async/await](../asynchronous-javascript/)
