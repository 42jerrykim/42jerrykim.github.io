---
title: "[Redux] 19. createAsyncThunk - 비동기 로직 단순화"
description: "09편에서 손으로 만들었던 시작·성공·실패 세 액션과 04편의 async/await를 createAsyncThunk 하나로 대체합니다. extraReducers의 pending/fulfilled/rejected 케이스로 로딩 상태를 관리하는 표준 패턴을 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 19
draft: false
slug: create-async-thunk
tags:
  - Redux
  - Redux-Toolkit
  - JavaScript
  - Asynchronous(비동기)
  - API
  - React
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
  - Implementation(구현)
  - createAsyncThunk문법
  - pending상태
  - fulfilled상태
  - rejected상태
  - 로딩상태관리
  - rejectWithValue
  - Error-Handling(에러처리)
  - Concurrency(동시성)
---

# 19. createAsyncThunk - 비동기 로직 단순화

09편에서 비동기 흐름을 "시작(pending) → 성공(fulfilled) → 실패(rejected)"라는 세 개의 동기 액션으로 손수 나눠 dispatch했습니다. 이 편은 이 반복적인 패턴을 `createAsyncThunk` 하나로 대체합니다.

## 학습 목표

- `createAsyncThunk`가 API 호출 함수 하나로부터 pending/fulfilled/rejected 액션을 자동 생성하는 원리를 설명할 수 있다.
- `extraReducers`에서 이 세 상태를 처리해 로딩 상태를 관리할 수 있다.
- `rejectWithValue`로 에러 정보를 커스터마이징해 전달할 수 있다.

## 09편 패턴 복습: 손으로 만든 비동기 액션 3종

09편에서는 `user` 도메인으로 이 패턴을 봤습니다. 이번 편은 20편의 실습 프로젝트와 이어지도록 `todos` 도메인으로 같은 패턴을 다시 짜봅니다.

```javascript
// 09편과 동일한 패턴을 todos 도메인으로 다시 쓴 순수 Redux 비동기 흐름
const todosLoadStarted = () => ({ type: "todos/loadStarted" });
const todosLoadSucceeded = (todos) => ({ type: "todos/loadSucceeded", payload: todos });
const todosLoadFailed = (error) => ({ type: "todos/loadFailed", payload: error, error: true });

function fetchTodos() {
  return async (dispatch) => {
    dispatch(todosLoadStarted());
    try {
      const response = await fetch("/api/todos"); // 04편: async/await
      const todos = await response.json();
      dispatch(todosLoadSucceeded(todos));
    } catch (error) {
      dispatch(todosLoadFailed(error.message));
    }
  };
}
```

액션 생성자 3개, thunk 함수 1개, 그리고 이 세 액션에 대응하는 리듀서 케이스까지 — API 호출 하나를 다루는 데 상당히 많은 코드가 필요했습니다.

## createAsyncThunk: 하나의 비동기 함수로 액션 3종 생성

```javascript
import { createAsyncThunk } from "@reduxjs/toolkit";

export const fetchTodos = createAsyncThunk(
  "todos/fetchTodos",      // 액션 타입 접두사 — pending/fulfilled/rejected가 이로부터 파생됨
  async () => {
    const response = await fetch("/api/todos"); // 04편의 async/await를 그대로 사용
    return await response.json(); // 이 반환값이 fulfilled 액션의 payload가 된다
  }
);
```

`createAsyncThunk("todos/fetchTodos", asyncFn)`을 호출하면 다음 세 액션 타입이 **자동으로** 만들어집니다.

| 자동 생성되는 액션 타입 | 발생 시점 |
|---|---|
| `todos/fetchTodos/pending` | 위 `todosLoadStarted`에 대응, 호출 시작 시 |
| `todos/fetchTodos/fulfilled` | 위 `todosLoadSucceeded`에 대응, `return`한 값이 `payload` |
| `todos/fetchTodos/rejected` | 위 `todosLoadFailed`에 대응, 예외 발생 시 |

액션 생성자 3개와 `try/catch`를 손으로 쓸 필요 없이, `async` 함수 하나만 작성하면 됩니다.

## extraReducers로 세 상태 처리하기

17편에서 짧게 언급한 `extraReducers`가 바로 이 세 액션을 처리하는 곳입니다. 로딩 상태를 관리하는 표준 패턴은 다음과 같습니다.

```javascript
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

export const fetchTodos = createAsyncThunk("todos/fetchTodos", async () => {
  const response = await fetch("/api/todos");
  return await response.json();
});

const todosSlice = createSlice({
  name: "todos",
  initialState: {
    items: [],
    status: "idle", // 'idle' | 'loading' | 'succeeded' | 'failed'
    error: null,
  },
  reducers: {
    // 17편에서 다룬 동기 액션들(todoAdded 등)은 여기에 그대로 둔다
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTodos.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchTodos.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload; // async 함수가 return한 값
      })
      .addCase(fetchTodos.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message; // 예외 발생 시 자동으로 채워지는 에러 정보
      });
  },
});

export default todosSlice.reducer;
```

`builder.addCase(actionCreator, reducerFn)` 형태로 각 상태 전이를 처리합니다. `fetchTodos.pending`, `fetchTodos.fulfilled`, `fetchTodos.rejected`는 `createAsyncThunk`가 자동으로 붙여준 속성으로, 17편의 `createAction`으로 만든 액션과 마찬가지로 `addCase`의 첫 인자로 쓸 수 있습니다.

## 컴포넌트에서 사용하기

`fetchTodos`를 dispatch하는 쪽은 09편의 thunk를 dispatch하던 방식과 동일합니다.

```jsx
import { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchTodos } from "./todosSlice";

function TodoList() {
  const dispatch = useDispatch();
  const { items, status, error } = useSelector((state) => state.todos);

  useEffect(() => {
    if (status === "idle") {
      dispatch(fetchTodos()); // configureStore(18편)에 기본 포함된 thunk 미들웨어가 처리
    }
  }, [status, dispatch]);

  if (status === "loading") return <p>로딩 중...</p>;
  if (status === "failed") return <p>에러: {error}</p>;

  return (
    <ul>
      {items.map((todo) => <li key={todo.id}>{todo.text}</li>)}
    </ul>
  );
}
```

`status` 필드로 로딩/성공/실패 상태를 명시적으로 구분하는 것이 핵심입니다. 단순히 `items.length === 0`으로 "로딩 중"을 판단하면, "로딩이 끝났지만 결과가 빈 배열인 경우"와 구분할 수 없기 때문입니다.

## rejectWithValue: 에러 정보 커스터마이징

기본적으로 `rejected` 액션의 `action.error.message`는 JS 예외 객체의 메시지를 그대로 담습니다. 서버가 반환하는 구조화된 에러 응답(예: `{ code: "NOT_FOUND", detail: "..." }`)을 그대로 전달하고 싶다면 `rejectWithValue`를 씁니다.

```javascript
export const fetchTodos = createAsyncThunk(
  "todos/fetchTodos",
  async (_, { rejectWithValue }) => {
    const response = await fetch("/api/todos");
    if (!response.ok) {
      const errorBody = await response.json();
      return rejectWithValue(errorBody); // action.payload로 전달됨 (action.error가 아님)
    }
    return await response.json();
  }
);
```

이렇게 `rejectWithValue`로 감싼 값은 리듀서 쪽에서도 짝을 맞춰 읽어야 합니다. `extraReducers`의 `rejected` 케이스에서 `action.payload`를 우선 확인하도록 고칩니다.

```javascript
.addCase(fetchTodos.rejected, (state, action) => {
  state.status = "failed";
  // rejectWithValue를 썼다면 action.payload에, 아니면 action.error.message에 담긴다
  state.error = action.payload ?? action.error.message;
})
```

`rejectWithValue`로 반환한 값은 `action.error`가 아니라 **`action.payload`**에 담긴다는 점이 자주 헷갈리는 부분입니다. 이 구분은 리듀서에서 에러를 처리할 때 어느 필드를 읽어야 하는지 명확히 해줍니다.

## 인자를 받는 thunk

API 호출에 인자가 필요하면 async 함수의 첫 번째 매개변수로 받습니다.

```javascript
export const fetchTodoById = createAsyncThunk(
  "todos/fetchTodoById",
  async (todoId) => { // dispatch(fetchTodoById(3))일 때 todoId === 3
    const response = await fetch(`/api/todos/${todoId}`);
    return await response.json();
  }
);
```

두 번째 매개변수는 `{ dispatch, getState, rejectWithValue, ... }`를 담은 thunkAPI 객체로, 위 `rejectWithValue` 예시에서 이미 사용했습니다.

## 실무 체크리스트

- API 호출을 09편 스타일의 손으로 만든 3-액션 thunk 대신 `createAsyncThunk`로 작성하고 있는가?
- 로딩 상태를 boolean(`isLoading`)이 아니라 `'idle'/'loading'/'succeeded'/'failed'` 같은 명시적 상태로 관리해, "로딩 끝 + 결과 없음"과 "로딩 중"을 구분하고 있는가?
- 서버의 구조화된 에러 응답을 그대로 전달해야 한다면 `rejectWithValue`를 사용하고 있는가?

## 연습 과제

### 기초(★☆☆)
- 09편의 `fetchTodos` thunk를 `createAsyncThunk` 버전으로 다시 작성해보세요.

### 중급(★★☆)
- `status` 필드를 활용해 "로딩 중", "에러 발생", "빈 목록", "정상 목록" 네 가지 UI 상태를 모두 렌더링하는 컴포넌트를 작성해보세요.

### 고급(★★★)
- 서버가 404일 때 `{ code: "NOT_FOUND" }`를 응답한다고 가정하고, `rejectWithValue`로 이 정보를 받아 "해당 항목을 찾을 수 없습니다"라는 전용 메시지를 표시해보세요.

## 요약

- `createAsyncThunk`는 API 호출 함수 하나로부터 pending/fulfilled/rejected 세 액션을 자동 생성한다.
- `extraReducers`의 `addCase`로 이 세 상태를 처리해 로딩 상태를 명시적으로 관리한다.
- `rejectWithValue`로 반환한 값은 `action.error`가 아니라 `action.payload`에 담긴다.

## 참고 문헌 및 출처(추천)

- Redux Toolkit 공식 문서, "createAsyncThunk" API 레퍼런스
- Redux Toolkit 공식 문서, "Redux Essentials, Part 5: Async Logic and Data Fetching"
- Redux Toolkit 공식 문서, "rejectWithValue"

---

## 다음 글

- 다음: [20. 실습: RTK로 앱 리팩터링](../practice-rtk-app/)
