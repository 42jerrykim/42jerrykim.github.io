---
title: "[Redux] 22. Redux Thunk - 가장 간단한 비동기 처리"
description: "21편의 미들웨어 구조 위에서 redux-thunk가 정확히 무엇을 하는지 직접 구현해봅니다. thunk 함수가 action 대신 dispatch되는 원리와, getState로 조건부 dispatch를 하는 패턴을 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 22
draft: false
slug: redux-thunk
tags:
  - Redux
  - Redux-Thunk
  - JavaScript
  - Asynchronous(비동기)
  - Frontend(프론트엔드)
  - Web(웹)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Intermediate
  - Deep-Dive
  - Implementation(구현)
  - thunk함수
  - getState활용
  - 조건부dispatch
  - thunk미들웨어직접구현
  - 액션함수구분
  - Error-Handling(에러처리)
  - Concurrency(동시성)
  - API(Application Programming Interface)
  - Composition(합성)
---

# 22. Redux Thunk - 가장 간단한 비동기 처리

21편에서 미들웨어가 `store => next => action => {}` 구조를 가진다는 것을 배웠습니다. 이 편은 그 구조 위에서 `redux-thunk`가 정확히 어떤 한 가지 일을 하는지 직접 구현해보며 확인합니다.

## 학습 목표

- `redux-thunk` 미들웨어를 처음부터 직접 구현할 수 있다.
- thunk 함수(action 대신 dispatch되는 함수)가 무엇이고 왜 유효한지 설명할 수 있다.
- `getState`를 활용해 현재 상태에 따라 조건부로 dispatch를 결정하는 thunk를 작성할 수 있다.

## Thunk 미들웨어를 직접 구현하기

`redux-thunk`가 하는 일은 사실 단 하나입니다. **"dispatch된 액션이 함수라면, 그 함수를 대신 실행해준다."**

```javascript
// redux-thunk의 핵심 로직 — 실제 라이브러리도 본질적으로 이와 동일하다
const thunkMiddleware = (store) => (next) => (action) => {
  if (typeof action === "function") {
    // action이 함수라면, (dispatch, getState)를 인자로 그 함수를 호출한다
    return action(store.dispatch, store.getState);
  }
  return next(action); // 함수가 아닌 일반 객체 액션은 그대로 통과시킨다
};
```

이것이 전부입니다. 07편에서 배운 `dispatch(action)`은 원래 **일반 객체**만 받도록 되어 있었는데, thunk 미들웨어가 "액션이 함수인 경우"라는 새로운 경로를 추가해준 것입니다.

## Thunk 함수란 무엇인가

**Thunk**는 "나중에 실행할 계산을 감싼 함수"를 뜻하는 일반적인 프로그래밍 용어입니다. Redux 맥락에서 thunk는 `(dispatch, getState) => { ... }` 형태의 함수를 말합니다.

```javascript
// 가장 단순한 thunk: 지연 후 dispatch
function incrementLater() {
  return (dispatch, getState) => { // 이 함수 자체가 "액션"으로 dispatch된다
    setTimeout(() => {
      dispatch({ type: "counter/incremented" }); // 지연 후 실제 액션을 dispatch
    }, 1000);
  };
}

store.dispatch(incrementLater()); // thunkMiddleware가 이 함수를 감지해 대신 실행
```

`store.dispatch(incrementLater())`를 호출하면, `incrementLater()`가 반환한 함수가 `thunkMiddleware`에 도달합니다. `typeof action === "function"`이 참이므로, 21편의 `next(action)` 대신 **그 함수 자체를 호출**합니다. 이 함수 안에서 원하는 시점에 `dispatch`를 호출해 실제 액션을 발생시킬 수 있습니다.

## 09편의 fetchTodos를 thunk로 이해하기

09편과 19편에서 이미 사용했던 비동기 액션 패턴이 사실 thunk였습니다. 이제 그 구조를 명확히 짚어봅니다.

```javascript
function fetchTodos() {
  return async (dispatch, getState) => { // 이 async 함수가 thunk다
    dispatch({ type: "todos/loadStarted" });
    try {
      const response = await fetch("/api/todos"); // 04편: async/await
      const todos = await response.json();
      dispatch({ type: "todos/loadSucceeded", payload: todos });
    } catch (error) {
      dispatch({ type: "todos/loadFailed", payload: error.message });
    }
  };
}
```

`fetchTodos()`는 액션 객체가 아니라 **함수를 반환하는 함수**입니다. `dispatch(fetchTodos())`를 호출하면, thunk 미들웨어가 이 내부 함수를 감지해 `(dispatch, getState)`를 인자로 실행해줍니다. 함수 내부에서는 `await`로 비동기 흐름을 자유롭게 제어하면서, 원하는 시점마다 `dispatch`로 동기 액션을 발생시킵니다.

## getState로 조건부 dispatch하기

Thunk의 두 번째 인자 `getState`는 **dispatch 시점의 최신 상태**를 읽을 수 있게 해줍니다. 이를 활용하면 "이미 로딩 중이면 중복 요청을 막는다" 같은 로직을 구현할 수 있습니다.

```javascript
function fetchTodosIfNeeded() {
  return (dispatch, getState) => {
    const { status } = getState().todos; // 19편에서 만든 status 필드 활용
    if (status === "loading" || status === "succeeded") {
      return; // 이미 불러왔거나 불러오는 중이면 아무것도 하지 않는다
    }
    return dispatch(fetchTodos()); // 필요할 때만 실제 fetchTodos thunk를 실행
  };
}
```

컴포넌트가 마운트될 때마다 `fetchTodosIfNeeded()`를 호출해도, 이미 데이터를 가져온 상태라면 중복 네트워크 요청이 발생하지 않습니다. 이 패턴은 `getState`가 리듀서 밖(미들웨어)에서도 상태에 접근할 수 있다는 것을 보여주는 대표적인 예입니다.

## 여러 액션을 조합하는 thunk

Thunk는 여러 개의 dispatch를 원하는 순서와 조건으로 조합할 수 있습니다.

```javascript
function checkoutCart() {
  return async (dispatch, getState) => {
    const { items } = getState().cart;
    if (items.length === 0) {
      dispatch({ type: "cart/checkoutRejected", payload: "장바구니가 비어 있습니다" });
      return;
    }

    dispatch({ type: "cart/checkoutStarted" });
    try {
      const order = await fetch("/api/orders", {
        method: "POST",
        body: JSON.stringify({ items }),
      }).then((res) => res.json());

      dispatch({ type: "cart/checkoutSucceeded", payload: order });
      dispatch({ type: "cart/cleared" }); // 성공 후 장바구니 비우기까지 하나의 thunk 안에서 처리
    } catch (error) {
      dispatch({ type: "cart/checkoutFailed", payload: error.message });
    }
  };
}
```

이처럼 "검증 → 시작 알림 → API 호출 → 성공 시 후속 액션 두 개" 같은 여러 단계를 하나의 thunk 함수 안에 자연스럽게 표현할 수 있습니다.

## Thunk의 한계

Thunk는 간단하지만, 다음과 같은 상황에서는 코드가 복잡해지기 쉽습니다.

- **여러 비동기 작업의 취소**: 사용자가 검색어를 빠르게 여러 번 입력할 때, 이전 요청을 취소하고 마지막 요청만 반영하는 로직은 thunk 안에서 직접 `AbortController` 등을 관리해야 한다.
- **복잡한 순서 제어**: "A가 끝난 뒤 B와 C를 동시에 실행하고, 그중 하나라도 실패하면 D를 실행" 같은 흐름은 `async/await`만으로 표현하면 코드가 빠르게 복잡해진다.

이런 경우를 위한 대안이 23편의 **Redux Saga**입니다. Saga는 제너레이터 함수로 이런 복잡한 흐름을 더 선언적으로 표현합니다. 다만 대부분의 실무 프로젝트에서는 thunk만으로 충분하며, Saga는 팀이 복잡한 사이드 이펙트 요구사항을 명확히 가지고 있을 때 선택하는 것이 일반적입니다.

## 실무 체크리스트

- Thunk 안에서 `dispatch`를 호출하는 순서가 실제로 의도한 상태 전이 순서와 일치하는가?
- 중복 요청을 막아야 하는 thunk에 `getState`로 현재 상태를 확인하는 가드를 추가했는가?
- thunk가 지나치게 복잡한 순서 제어를 담당하고 있다면, Saga 같은 대안이 더 적합하지 않은지 검토했는가?

## 연습 과제

### 기초(★☆☆)
- `thunkMiddleware`를 직접 작성하고 `applyMiddleware`로 등록해, `dispatch(function() {...})` 형태의 액션이 정상적으로 실행되는지 확인해보세요.

### 중급(★★☆)
- `fetchTodosIfNeeded()`를 작성해, 같은 컴포넌트가 두 번 마운트되어도 네트워크 요청이 한 번만 발생하는지 확인해보세요.

### 고급(★★★)
- `checkoutCart()` thunk에 "이미 체크아웃이 진행 중이면 중복 실행을 막는" 가드를 `getState`로 추가해보세요.

## 요약

- `redux-thunk`는 "dispatch된 값이 함수면 그 함수를 대신 실행한다"는 단 하나의 규칙을 가진 미들웨어다.
- Thunk 함수는 `(dispatch, getState)`를 받아, 그 안에서 자유롭게 비동기 로직과 조건부 dispatch를 조합할 수 있다.
- 복잡한 순서 제어나 요청 취소가 필요한 경우에는 23편의 Saga가 대안이 될 수 있다.

## 참고 문헌 및 출처(추천)

- Redux Thunk 공식 문서(GitHub), "redux-thunk"
- Redux 공식 문서, "Writing Tests, Async Action Creators"

---

## 다음 글

- 다음: [23. Redux Saga - 강력한 사이드 이펙트 관리](../redux-saga/)
