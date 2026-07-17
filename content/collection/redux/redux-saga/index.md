---
title: "[Redux] 23. Redux Saga - 강력한 사이드 이펙트 관리"
description: "제너레이터 함수와 yield로 사이드 이펙트를 선언적으로 기술하는 Redux Saga를 다룹니다. take·call·put 이펙트와, 22편의 thunk로는 표현이 번거로운 takeLatest 취소 패턴을 코드로 비교합니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 23
draft: false
slug: redux-saga
tags:
  - Redux
  - Redux-Saga
  - JavaScript
  - Asynchronous(비동기)
  - Design-Pattern(디자인패턴)
  - Frontend(프론트엔드)
  - Web(웹)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Intermediate
  - Deep-Dive
  - Implementation(구현)
  - 제너레이터함수
  - yield표현식
  - 이펙트객체
  - takeLatest패턴
  - 요청취소
  - 사가테스트용이성
  - Concurrency(동시성)
  - Testing(테스트)
  - Error-Handling(에러처리)
---

# 23. Redux Saga - 강력한 사이드 이펙트 관리

22편에서 thunk의 한계로 "여러 비동기 작업의 취소"와 "복잡한 순서 제어"를 언급했습니다. 이 편은 **제너레이터 함수**를 기반으로 이런 문제를 더 선언적으로 다루는 Redux Saga를 소개합니다.

## 학습 목표

- 제너레이터 함수와 `yield`가 Saga에서 어떻게 사이드 이펙트를 기술하는지 설명할 수 있다.
- `take`, `call`, `put` 세 가지 기본 이펙트로 간단한 saga를 작성할 수 있다.
- `takeLatest`가 22편의 thunk로는 번거로운 "이전 요청 취소" 문제를 어떻게 해결하는지 설명할 수 있다.

## 제너레이터 함수 복습

Saga를 이해하려면 먼저 JavaScript의 **제너레이터 함수**(`function*`)를 알아야 합니다. 제너레이터는 `yield`를 만날 때마다 실행을 일시 정지하고, 호출자가 재개할 때까지 기다립니다.

```javascript
function* countUpTo3() {
  yield 1;
  yield 2;
  yield 3;
}

const gen = countUpTo3();
console.log(gen.next()); // { value: 1, done: false }
console.log(gen.next()); // { value: 2, done: false }
console.log(gen.next()); // { value: 3, done: false }
console.log(gen.next()); // { value: undefined, done: true }
```

이 "일시 정지하고 값을 내보낸다"는 특성 덕분에, 제너레이터는 **"무엇을 할지" 기술만 하고, 실제 실행은 다른 코드(Saga 미들웨어)에 맡기는** 구조를 만들 수 있습니다.

## Saga의 핵심 아이디어: 이펙트 객체

Saga 함수 안에서 `yield`하는 것은 실제 함수 호출이 아니라, **"이런 일을 해달라"는 순수한 설명(이펙트 객체)**입니다.

```javascript
import { call, put, takeEvery } from "redux-saga/effects";

function fetchTodosApi() {
  return fetch("/api/todos").then((res) => res.json());
}

function* fetchTodosSaga() {
  try {
    yield put({ type: "todos/loadStarted" }); // put: dispatch를 대신 기술한 이펙트
    const todos = yield call(fetchTodosApi);   // call: 함수 호출을 대신 기술한 이펙트
    yield put({ type: "todos/loadSucceeded", payload: todos });
  } catch (error) {
    yield put({ type: "todos/loadFailed", payload: error.message });
  }
}
```

`call(fetchTodosApi)`는 `fetchTodosApi()`를 직접 호출하는 게 아니라, `{ type: "CALL", fn: fetchTodosApi }`와 비슷한 **순수 객체**를 만듭니다. 이 객체를 Saga 미들웨어가 받아서 **실제로 함수를 호출하고, 그 결과를 제너레이터에 돌려줍니다.** 09편의 async/await와 결과적으로 비슷한 일을 하지만, "무엇을 할지"와 "어떻게 실행할지"가 분리되어 있다는 점이 다릅니다.

## call과 put이 순수 객체라는 것의 이점: 테스트 용이성

이 분리 덕분에 saga 함수는 **실제 네트워크 요청 없이도 단위 테스트가 가능**합니다.

```javascript
// fetchTodosSaga의 실행 흐름을 실제 API 호출 없이 검증
const gen = fetchTodosSaga();

let result = gen.next();
console.log(result.value); // put({ type: "todos/loadStarted" }) — 이펙트 객체 그 자체를 검사할 수 있다

result = gen.next(); // call(fetchTodosApi)까지 진행
console.log(result.value.payload.fn === fetchTodosApi); // true — 실제 호출 없이 "무엇을 호출하려 했는지"만 확인

result = gen.next([{ id: 1, text: "우유 사기" }]); // 가짜 응답을 직접 주입
console.log(result.value); // put({ type: "todos/loadSucceeded", payload: [...] })
```

07편에서 리듀서를 순수 함수로 정의했던 것과 비슷한 원리가 여기서도 테스트 용이성으로 이어집니다. `call(fetchTodosApi)`가 실제로 fetch를 실행하지 않고 "무엇을 호출하려는지"에 대한 설명만 담고 있으므로, 그 설명 자체를 mock 없이 검증할 수 있습니다.

## take: 특정 액션을 기다린다

`take`는 특정 액션 타입이 dispatch될 때까지 saga 실행을 멈춥니다.

```javascript
import { take, call, put } from "redux-saga/effects";

function* watchFetchTodos() {
  while (true) {
    yield take("todos/fetchRequested"); // 이 액션이 dispatch될 때까지 대기
    yield call(fetchTodosSaga);          // 대기가 끝나면 실행
  }
}
```

`while (true)` 안에서 `take`를 쓰는 패턴은 "이 액션 타입이 dispatch될 때마다 반복해서 반응한다"는 뜻입니다. 이 패턴이 매우 흔하기 때문에, Saga는 이를 축약한 헬퍼 함수들을 제공합니다.

## takeEvery vs takeLatest: 22편 thunk의 한계 해결

`takeEvery`는 `watchFetchTodos`와 동일하게 매 액션마다 새로운 saga를 실행합니다. 반면 **`takeLatest`는 이전에 실행 중이던 saga를 자동으로 취소하고 최신 것만 남깁니다.**

```javascript
import { takeLatest, call, put } from "redux-saga/effects";

function* searchProductsSaga(action) {
  const results = yield call(searchApi, action.payload.query);
  yield put({ type: "search/succeeded", payload: results });
}

function* watchSearch() {
  yield takeLatest("search/queryChanged", searchProductsSaga); // 이전 검색 요청은 자동 취소됨
}
```

사용자가 검색창에 "리액트"를 빠르게 타이핑하면 `r`, `ri`, `리`, `리액`, `리액트` 순서로 여러 번 `search/queryChanged`가 dispatch될 수 있습니다. `takeLatest`는 새 액션이 들어올 때마다 **이전에 진행 중이던 `searchProductsSaga` 실행을 자동으로 취소**하고 최신 요청만 살려둡니다. 그 결과 느린 응답이 빠른 응답보다 늦게 도착해 화면을 덮어쓰는(오래된 결과가 최신 결과를 잘못 대체하는) 문제가 방지됩니다.

22편에서 이 문제를 thunk로 해결하려면 `AbortController`를 직접 관리하거나, "이 요청이 최신 요청인지" 확인하는 ID 비교 로직을 직접 작성해야 했습니다. `takeLatest`는 이 패턴을 한 줄로 표현합니다.

## Saga 미들웨어 등록

```javascript
import { configureStore } from "@reduxjs/toolkit";
import createSagaMiddleware from "redux-saga";
import rootReducer from "./rootReducer";
import rootSaga from "./rootSaga";

const sagaMiddleware = createSagaMiddleware();

export const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ thunk: false }).concat(sagaMiddleware), // 18편: thunk를 끄고 saga로 대체
  devTools: process.env.NODE_ENV !== "production",
});

sagaMiddleware.run(rootSaga); // Store 생성 후 saga 실행 시작
```

Saga도 결국 21편에서 배운 미들웨어 구조 위에서 동작합니다. `sagaMiddleware`가 dispatch되는 액션을 감시하다가, `take` 이펙트가 기다리는 액션 타입과 일치하면 해당 제너레이터의 다음 단계를 진행시키는 방식입니다.

## Saga를 선택하는 기준

모든 프로젝트에 Saga가 필요한 것은 아닙니다. 다음 상황에서 Saga 도입을 고려합니다.

- 여러 비동기 작업 간의 **복잡한 순서 제어**(A 성공 후 B와 C 동시 실행, 그중 하나 실패 시 D 실행)가 자주 필요하다.
- 검색 자동완성처럼 **이전 요청의 자동 취소**가 핵심 요구사항이다.
- 사이드 이펙트 로직을 **네트워크 없이 순수하게 단위 테스트**해야 하는 요구가 강하다.

단순한 CRUD API 호출이 대부분이라면 22편의 thunk나 24편의 RTK Query만으로 충분한 경우가 많습니다. Saga는 학습 곡선(제너레이터 문법, 이펙트 개념)이 있는 만큼, 실제로 복잡한 사이드 이펙트 요구사항이 있을 때 도입하는 것이 합리적입니다.

## 실무 체크리스트

- 여러 비동기 작업 간 복잡한 순서 제어나 요청 취소가 실제로 필요한 상황인가, 아니면 thunk로 충분한가?
- `takeEvery`와 `takeLatest` 중 상황에 맞는 것을 선택했는가(중복 실행이 허용되는지 여부)?
- Saga 함수를 실제 API 호출 없이 이펙트 객체 검증만으로 테스트하고 있는가?

## 연습 과제

### 기초(★☆☆)
- `fetchTodosSaga`를 작성하고 `watchFetchTodos`로 감싸, `todos/fetchRequested` 액션이 dispatch될 때마다 실행되는지 확인해보세요.

### 중급(★★☆)
- `watchSearch`를 `takeEvery`로 바꿨을 때와 `takeLatest`로 뒀을 때, 빠른 연속 입력에서 화면에 표시되는 검색 결과가 어떻게 달라지는지 관찰해보세요.

### 고급(★★★)
- `fetchTodosSaga`의 제너레이터를 실제 네트워크 호출 없이 `gen.next()`를 수동으로 진행시키며, 각 단계에서 발생하는 이펙트 객체가 예상과 일치하는지 검증하는 테스트를 작성해보세요.

## 요약

- Saga는 제너레이터 함수와 `yield`로 사이드 이펙트를 순수한 이펙트 객체로 기술하고, 미들웨어가 실제 실행을 담당한다.
- 이펙트 객체가 순수 데이터이기 때문에 실제 API 호출 없이도 saga의 실행 흐름을 테스트할 수 있다.
- `takeLatest`는 22편 thunk에서 직접 구현해야 했던 "이전 요청 자동 취소"를 선언적으로 해결한다.

## 참고 문헌 및 출처(추천)

- Redux Saga 공식 문서, "Redux-Saga: An intuitive guide"
- Redux Saga 공식 문서, "Using Saga Helpers"
- MDN Web Docs, "Generator" — 제너레이터 함수 기초

---

## 다음 글

- 다음: [24. RTK Query - 데이터 페칭의 혁명](../rtk-query/)
