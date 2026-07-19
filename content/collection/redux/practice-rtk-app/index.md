---
title: "[Redux] 20. 실습: RTK로 앱 리팩터링"
description: "15편의 순수 Redux Counter/Todo 앱을 createSlice·configureStore·createAsyncThunk로 완전히 다시 작성합니다. 코드량 비교와 함께 Phase 4를 마무리하는 종합 실습입니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 20
draft: false
slug: practice-rtk-app
image: "wordcloud.png"
tags:
  - Redux
  - Redux-Toolkit
  - React
  - JavaScript
  - Frontend(프론트엔드)
  - Web(웹)
  - Case-Study
  - 실습
  - Refactoring(리팩토링)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Intermediate
  - Implementation(구현)
  - Deep-Dive
  - rtk종합실습
  - 순수redux대비코드량
  - 비동기thunk통합
  - 슬라이스리팩터링
  - Migration(마이그레이션)
  - Productivity(생산성)
---

# 20. 실습: RTK로 앱 리팩터링

Phase 4의 마지막 편입니다. 15편에서 순수 Redux로 만든 Counter/Todo 앱을 16~19편에서 배운 `createSlice`·`configureStore`·`createAsyncThunk`로 완전히 다시 작성하고, 코드량이 실제로 얼마나 줄었는지 비교합니다.

## 학습 목표

- 순수 Redux 프로젝트 전체를 Redux Toolkit으로 리팩터링할 수 있다.
- `createAsyncThunk`로 서버에서 초기 Todo 목록을 불러오는 기능을 추가할 수 있다.
- 리팩터링 전후 코드를 비교해 RTK가 줄여주는 보일러플레이트의 종류를 구체적으로 설명할 수 있다.

## 리팩터링 대상: 15편의 프로젝트 구조

```
src/
  store.js
  features/
    counter/
      counterSlice.js
      counterSelectors.js
      Counter.jsx
    todos/
      todosSlice.js
      todosSelectors.js
      TodoList.jsx
  App.jsx
```

구조 자체는 그대로 유지합니다. 26편(프로젝트 구조)에서 다룰 "기능 단위 폴더 구조"는 순수 Redux든 RTK든 동일하게 적용되는 원칙이기 때문입니다. 바뀌는 것은 각 파일 **내부**의 구현입니다.

## counterSlice.js 리팩터링

```javascript
// features/counter/counterSlice.js — 17편의 createSlice 적용
import { createSlice } from "@reduxjs/toolkit";

const counterSlice = createSlice({
  name: "counter",
  initialState: { count: 0 },
  reducers: {
    incremented: (state) => { state.count += 1; },
    decremented: (state) => { state.count -= 1; },
  },
});

export const { incremented, decremented } = counterSlice.actions;
export const selectCount = (state) => state.counter.count; // 14편: selector는 그대로 유지
export default counterSlice.reducer;
```

`Counter.jsx`는 **한 줄도 바꿀 필요가 없습니다.** `useSelector(selectCount)`와 `dispatch(incremented())`는 액션이 `createSlice`에서 왔든 손으로 만들었든 동일하게 동작하기 때문입니다. 이것이 Redux의 계층 분리(UI는 액션의 출처를 몰라도 된다)가 주는 실질적 이점입니다.

## todosSlice.js 리팩터링: 동기 로직 + 비동기 로직 통합

15편에서는 Todo를 로컬에서만 추가했지만, 이번에는 19편의 `createAsyncThunk`로 **서버에서 초기 목록을 불러오는 기능**을 추가합니다.

```javascript
// features/todos/todosSlice.js — 17편(createSlice) + 19편(createAsyncThunk) 통합
import { createSlice, createAsyncThunk, nanoid } from "@reduxjs/toolkit";

export const fetchTodos = createAsyncThunk("todos/fetchTodos", async () => {
  const response = await fetch("/api/todos");
  return await response.json();
});

const todosSlice = createSlice({
  name: "todos",
  initialState: {
    items: [],
    status: "idle", // 19편: 'idle' | 'loading' | 'succeeded' | 'failed'
    error: null,
  },
  reducers: {
    todoAdded: {
      reducer: (state, action) => {
        state.items.push(action.payload);
      },
      prepare: (text) => ({ payload: { id: nanoid(), text, done: false } }),
    },
    todoToggled: (state, action) => {
      const todo = state.items.find((t) => t.id === action.payload);
      if (todo) todo.done = !todo.done;
    },
    todoRemoved: (state, action) => {
      state.items = state.items.filter((t) => t.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTodos.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchTodos.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(fetchTodos.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      });
  },
});

export const { todoAdded, todoToggled, todoRemoved } = todosSlice.actions;
export default todosSlice.reducer;
```

동기 액션(`todoAdded` 등)과 비동기 액션(`fetchTodos`)이 **같은 slice 파일 안에서** 자연스럽게 공존합니다. 09편에서는 이 둘을 다른 방식(리듀서 케이스 vs 별도의 thunk 파일)으로 다뤄야 했지만, RTK에서는 `reducers`와 `extraReducers`로 통합된 위치에서 관리합니다.

## todosSelectors.js: 상태 구조 변경 반영

`status` 필드가 추가되면서 상태 구조가 `state.todos`(배열)에서 `state.todos.items`(객체 안의 배열)로 바뀌었습니다. Selector 파일만 수정하면 이 변화가 다른 파일에 전파되지 않습니다.

```javascript
// features/todos/todosSelectors.js
import { createSelector } from "@reduxjs/toolkit";

export const selectAllTodos = (state) => state.todos.items; // 상태 구조 변경 지점을 여기 한 곳으로 흡수
export const selectTodosStatus = (state) => state.todos.status;
export const selectTodosError = (state) => state.todos.error;

export const selectCompletedCount = createSelector(
  [selectAllTodos],
  (todos) => todos.filter((todo) => todo.done).length
);
```

15편에서 강조했던 "상태 구조가 바뀌어도 selector 파일 한 곳만 고치면 된다"는 이점이 여기서 그대로 증명됩니다. `TodoList.jsx`는 `selectAllTodos`를 그대로 호출하므로 내부 구조 변경을 알 필요가 없습니다.

## store.js 리팩터링

```javascript
// store.js — 18편의 configureStore 적용
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./features/counter/counterSlice";
import todosReducer from "./features/todos/todosSlice";

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    todos: todosReducer,
  },
});
```

`combineReducers`, DevTools 연결, thunk 미들웨어 설정이 모두 사라지고 `reducer` 객체 하나만 남았습니다.

## TodoList.jsx: 로딩 상태 반영

컴포넌트는 19편에서 다룬 `status` 기반 조건 렌더링만 추가하면 됩니다.

```jsx
// features/todos/TodoList.jsx
import { useEffect, useCallback } from "react";
import { useSelector, useDispatch } from "react-redux";
import { selectAllTodos, selectTodosStatus, selectCompletedCount } from "./todosSelectors";
import { fetchTodos, todoAdded, todoToggled, todoRemoved } from "./todosSlice";

export function TodoList() {
  const todos = useSelector(selectAllTodos);
  const status = useSelector(selectTodosStatus);
  const completedCount = useSelector(selectCompletedCount);
  const dispatch = useDispatch();

  useEffect(() => {
    if (status === "idle") dispatch(fetchTodos()); // 19편: 최초 마운트 시 서버에서 불러오기
  }, [status, dispatch]);

  const handleToggle = useCallback((id) => dispatch(todoToggled(id)), [dispatch]); // 13편: 콜백 안정화

  if (status === "loading") return <p>불러오는 중...</p>;

  return (
    <div>
      <p>완료: {completedCount} / {todos.length}</p>
      <ul>
        {todos.map((todo) => (
          <li key={todo.id} onClick={() => handleToggle(todo.id)}>
            {todo.text}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## 코드량 비교

| 파일 | 15편(순수 Redux) | 20편(RTK) |
|---|---|---|
| `counterSlice.js` | 액션 생성자 3개 + switch 4케이스 (약 20줄) | `createSlice` 호출 1개 (약 12줄) |
| `todosSlice.js` (+비동기 포함) | 액션 생성자 3개 + switch 4케이스 + 별도 thunk 파일 (약 40줄, 2개 파일) | `createSlice` + `createAsyncThunk` (약 30줄, 1개 파일) |
| `store.js` | `combineReducers` + DevTools 연결 코드 (약 10줄) | `configureStore` 호출 1개 (약 6줄) |

단순 라인 수보다 중요한 것은 **줄어든 종류**입니다. 액션 타입 문자열 중복, 수동 불변 업데이트, 별도의 thunk 파일 분리, DevTools 연결 코드가 모두 사라졌습니다. 반면 리듀서의 **로직 자체**(어떤 액션이 상태를 어떻게 바꾸는가)는 15편과 20편이 본질적으로 동일합니다. RTK는 로직을 대신 짜주는 도구가 아니라, 그 로직을 표현하는 데 필요한 **의례적인 코드**를 없애주는 도구입니다.

## 실무 체크리스트

- slice 파일 안에서 동기 액션(`reducers`)과 비동기 액션(`extraReducers` + `createAsyncThunk`)이 자연스럽게 공존하고 있는가?
- 상태 구조가 바뀌었을 때 selector 파일만 수정하고 컴포넌트는 그대로 유지되는가?
- RTK로 리팩터링한 뒤에도 리듀서의 핵심 로직(어떤 액션이 상태를 어떻게 바꾸는가)이 리팩터링 전과 동일한지 확인했는가?

## 연습 과제

### 기초(★☆☆)
- 15편의 원본 코드와 이 편의 RTK 코드를 나란히 놓고, 실제로 줄어든 줄 수를 세어보세요.

### 중급(★★☆)
- `todoRemoved`를 `createAsyncThunk` 기반의 `deleteTodoOnServer`로 바꿔, 서버에 DELETE 요청을 보낸 뒤 성공하면 목록에서 제거하도록 구현해보세요.

### 고급(★★★)
- `fetchTodos`가 실패했을 때 "재시도" 버튼을 눌러 `status`를 `'idle'`로 되돌리고 다시 `fetchTodos()`를 dispatch하는 재시도 UX를 구현해보세요.

## 요약

- RTK 리팩터링은 리듀서의 로직을 바꾸는 것이 아니라, 그 로직을 표현하는 보일러플레이트를 줄이는 작업이다.
- 동기·비동기 로직이 하나의 slice 파일 안에서 `reducers`/`extraReducers`로 통합 관리된다.
- Selector 계층 덕분에 상태 구조 변경(배열 → `{ items, status, error }`)이 컴포넌트에 전파되지 않는다.

## 참고 문헌 및 출처(추천)

- Redux Toolkit 공식 문서, "Redux Essentials, Part 5: Async Logic and Data Fetching"
- Redux Toolkit 공식 문서, "Migrating to Modern Redux"

---

## 다음 글

- 다음: [21. Redux 미들웨어의 이해](../redux-middleware/)
