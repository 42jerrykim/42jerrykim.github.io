---
title: "[Redux] 28. Redux와 TypeScript - 타입 안전한 상태 관리"
description: "05편의 TypeScript 기초를 Redux에 적용해 RootState·AppDispatch 타입을 추출하고, 타입 지정된 useSelector/useDispatch 훅, createSlice의 PayloadAction, createAsyncThunk의 rejectValue 타입까지 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 28
draft: false
slug: redux-typescript
image: "wordcloud.png"
tags:
  - Redux
  - TypeScript
  - Redux-Toolkit
  - React
  - JavaScript
  - Type-Safety(타입안전성)
  - Frontend(프론트엔드)
  - Web(웹)
  - Best-Practices
  - Code-Quality(코드품질)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Advanced
  - Deep-Dive
  - RootState타입
  - AppDispatch타입
  - PayloadAction
  - 타입지정훅
  - ReturnType유틸리티
  - Interface(인터페이스)
  - API(Application Programming Interface)
  - Error-Handling(에러처리)
  - rejectValue타이핑
  - withTypes헬퍼
---

# 28. Redux와 TypeScript - 타입 안전한 상태 관리

05편에서 인터페이스·제네릭·구분 유니온 같은 TypeScript 기초를 다뤘습니다. 이 편은 그 지식을 Redux 코드에 실제로 적용해, 상태와 액션에 타입 안전성을 부여하는 표준 패턴을 다룹니다.

## 학습 목표

- `RootState`, `AppDispatch` 타입을 Store로부터 자동 추출할 수 있다.
- 타입 지정된 `useAppSelector`/`useAppDispatch` 훅을 만들어 컴포넌트 전체에서 재사용할 수 있다.
- `createSlice`의 리듀서에서 `PayloadAction<T>`로 액션 페이로드 타입을 명시할 수 있다.

## RootState와 AppDispatch: Store로부터 타입을 추출한다

Redux TypeScript 프로젝트에서 반복적으로 등장하는 첫 단계는, 상태와 dispatch의 타입을 **Store 자체로부터 추출**하는 것입니다. 이는 05편에서 배운 `typeof`와 유틸리티 타입을 그대로 응용한 것입니다.

```typescript
// app/store.ts
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "../features/counter/counterSlice";
import todosReducer from "../features/todos/todosSlice";

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    todos: todosReducer,
  },
});

// 05편의 typeof + ReturnType으로, store.getState()의 반환 타입을 그대로 RootState로 추출
export type RootState = ReturnType<typeof store.getState>;
// store.dispatch 함수 자체의 타입을 추출 — thunk 지원 여부까지 포함된 정확한 타입
export type AppDispatch = typeof store.dispatch;
```

이렇게 하면 리듀서 구조가 바뀔 때마다 `RootState`를 손으로 다시 작성할 필요가 없습니다. `configureStore`의 `reducer` 객체가 변경되면 `RootState`도 자동으로 그 변경을 반영합니다.

## 타입 지정된 useSelector/useDispatch 훅

12편에서 쓴 `useSelector`, `useDispatch`는 기본적으로 상태 타입을 모릅니다(`state`가 `any`로 추론됩니다). 매번 `useSelector((state: RootState) => ...)`처럼 타입을 명시하는 대신, **타입이 미리 적용된 커스텀 훅**을 한 번만 만들어 재사용합니다.

```typescript
// app/hooks.ts
import { useDispatch, useSelector, TypedUseSelectorHook } from "react-redux";
import type { RootState, AppDispatch } from "./store";

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

```typescript
// features/counter/Counter.tsx
import { useAppSelector, useAppDispatch } from "../../app/hooks";
import { incremented } from "./counterSlice";

function Counter() {
  const count = useAppSelector((state) => state.counter.count); // state가 RootState로 자동 추론됨
  const dispatch = useAppDispatch();

  return <button onClick={() => dispatch(incremented())}>{count}</button>;
}
```

`state.counter.count`를 입력하는 순간 에디터가 `state.counter`가 어떤 필드를 가지는지 자동완성으로 제안합니다. 오타(`state.coutner`)가 있으면 컴파일 타임에 바로 에러가 발생합니다. 26편의 `app/` 폴더가 바로 이 `hooks.ts`와 `store.ts`를 담는 위치입니다.

React-Redux 최신 버전은 `TypedUseSelectorHook` 대신 더 짧게 쓸 수 있는 `.withTypes()` 헬퍼도 제공합니다.

```typescript
// app/hooks.ts — .withTypes()를 쓴 대안 (React-Redux 9+)
import { useDispatch, useSelector } from "react-redux";
import type { RootState, AppDispatch } from "./store";

export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();
```

두 방식은 결과적으로 동일한 타입 안전성을 제공하며, `TypedUseSelectorHook`은 여전히 널리 쓰이는 기존 관용구이고 `.withTypes()`는 더 최근에 추가된 축약형입니다. 어느 쪽을 쓰든 팀 안에서 일관되게만 사용하면 됩니다.

## createSlice와 PayloadAction

17편에서 만든 `reducers` 함수에 타입을 붙일 때는, RTK가 제공하는 `PayloadAction<T>` 제네릭 타입을 씁니다.

```typescript
// features/counter/counterSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface CounterState {
  count: number;
}

const initialState: CounterState = { count: 0 };

const counterSlice = createSlice({
  name: "counter",
  initialState,
  reducers: {
    incremented: (state) => {
      state.count += 1; // state는 CounterState로 자동 추론됨(initialState의 타입을 따름)
    },
    incrementedBy: (state, action: PayloadAction<number>) => { // payload가 number임을 명시
      state.count += action.payload; // action.payload는 number로 타입 체크됨
    },
  },
});

export const { incremented, incrementedBy } = counterSlice.actions;
export default counterSlice.reducer;
```

`PayloadAction<number>`는 05편에서 배운 제네릭을 응용한 타입으로, `{ type: string; payload: number }` 형태를 나타냅니다. `incrementedBy(state, action: PayloadAction<number>)`라고 선언하면, `incrementedBy("5")`처럼 문자열을 전달하려는 실수를 컴파일 타임에 막을 수 있습니다.

## 페이로드가 객체일 때

```typescript
interface Todo {
  id: string;
  text: string;
  done: boolean;
}

interface TodosState {
  items: Todo[];
  status: "idle" | "loading" | "succeeded" | "failed"; // 05편의 리터럴 유니온 타입
}

const todosSlice = createSlice({
  name: "todos",
  initialState: { items: [], status: "idle" } as TodosState,
  reducers: {
    todoAdded: {
      reducer: (state, action: PayloadAction<Todo>) => {
        state.items.push(action.payload);
      },
      prepare: (text: string) => ({
        payload: { id: crypto.randomUUID(), text, done: false } as Todo,
      }),
    },
    todoToggled: (state, action: PayloadAction<string>) => { // id(string)를 페이로드로 받음
      const todo = state.items.find((t) => t.id === action.payload);
      if (todo) todo.done = !todo.done;
    },
  },
});
```

`status: "idle" | "loading" | "succeeded" | "failed"`는 05편에서 다룬 리터럴 유니온 타입입니다. 19편에서 문자열로만 관리했던 이 필드가, TypeScript 환경에서는 오타(`"loadng"`)를 컴파일 타임에 잡아주는 안전장치가 됩니다.

## createAsyncThunk의 타입 지정

19편의 `createAsyncThunk`도 제네릭으로 반환 타입과 인자 타입을 지정할 수 있습니다.

```typescript
import { createAsyncThunk } from "@reduxjs/toolkit";

export const fetchTodos = createAsyncThunk<Todo[]>( // 반환 타입(fulfilled의 payload 타입)을 명시
  "todos/fetchTodos",
  async () => {
    const response = await fetch("/api/todos");
    return (await response.json()) as Todo[];
  }
);

// extraReducers에서도 action.payload가 자동으로 Todo[]로 추론된다
extraReducers: (builder) => {
  builder.addCase(fetchTodos.fulfilled, (state, action) => {
    state.items = action.payload; // action.payload: Todo[] — 별도 타입 단언 불필요
  });
},
```

19편에서 `rejectWithValue`로 반환한 값은 `action.payload`에 담긴다고 배웠습니다. 이 값에도 타입을 붙이려면 `createAsyncThunk`의 **세 번째 제네릭 인자**(`{ rejectValue: T }`)를 지정합니다.

```typescript
interface ApiError {
  code: string;
  message: string;
}

// <성공 시 payload 타입, thunk 인자 타입, { rejectValue: 실패 시 payload 타입 }>
export const fetchTodoById = createAsyncThunk<Todo, string, { rejectValue: ApiError }>(
  "todos/fetchTodoById",
  async (todoId, { rejectWithValue }) => {
    const response = await fetch(`/api/todos/${todoId}`);
    if (!response.ok) {
      const errorBody: ApiError = await response.json();
      return rejectWithValue(errorBody); // ApiError 타입으로 체크됨
    }
    return (await response.json()) as Todo;
  }
);

extraReducers: (builder) => {
  builder.addCase(fetchTodoById.rejected, (state, action) => {
    state.error = action.payload?.message; // action.payload: ApiError | undefined 로 정확히 추론됨
  });
},
```

이 세 번째 제네릭을 생략하면 `action.payload`는 `unknown`으로 추론되어, 실패 응답의 구조를 활용하는 코드에서 타입 체크의 이점을 잃게 됩니다.

## RTK Query의 타입 지정

24편의 `createApi`도 `builder.query<반환타입, 인자타입>` 형태로 제네릭을 받습니다.

```typescript
export const postsApi = createApi({
  reducerPath: "postsApi",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  endpoints: (builder) => ({
    getPosts: builder.query<Post[], void>({ // <반환 타입, 인자 타입>
      query: () => "/posts",
    }),
    getPostById: builder.query<Post, string>({ // 인자로 postId(string)를 받고 Post를 반환
      query: (postId) => `/posts/${postId}`,
    }),
  }),
});
```

`useGetPostByIdQuery("abc")`처럼 호출하면 인자 타입이 `string`인지 체크되고, `data` 필드는 자동으로 `Post | undefined`로 추론됩니다.

## 실무 체크리스트

- `RootState`/`AppDispatch`를 Store로부터 `ReturnType`/`typeof`로 추출해 손으로 중복 정의하지 않았는가?
- 컴포넌트 전체에서 `useSelector`/`useDispatch` 대신 타입이 지정된 `useAppSelector`/`useAppDispatch`를 사용하고 있는가?
- `reducers`의 각 함수에서 `action.payload`의 타입을 `PayloadAction<T>`로 명시했는가?
- `createAsyncThunk`가 구조화된 에러 응답을 반환한다면, 세 번째 제네릭(`{ rejectValue: T }`)으로 실패 시 `action.payload`의 타입도 명시했는가?

## 연습 과제

### 기초(★☆☆)
- 15편의 `counterSlice`를 TypeScript로 변환하고, `RootState`/`AppDispatch`를 추출하는 `store.ts`를 작성해보세요.

### 중급(★★☆)
- `todosSlice`의 `Todo` 인터페이스를 정의하고, `todoAdded`의 `prepare` 콜백에 정확한 타입을 붙여보세요.

### 고급(★★★)
- 25편의 `postsApi`를 TypeScript로 옮기고, `getPosts`/`getPostById`/`addPost` 각각에 정확한 `<반환타입, 인자타입>` 제네릭을 지정해보세요.
- `fetchTodoById`에 `{ rejectValue: ApiError }`를 지정한 뒤, 세 번째 제네릭을 일부러 빼보고 `action.payload`의 추론 타입이 `ApiError | undefined`에서 `unknown`으로 어떻게 바뀌는지 비교해보세요.

## 요약

- `RootState`와 `AppDispatch`는 Store로부터 `ReturnType`/`typeof`로 자동 추출해, 구조 변경 시 타입이 자동으로 따라오게 한다.
- `useAppSelector`/`useAppDispatch` 커스텀 훅(`TypedUseSelectorHook` 또는 `.withTypes()`)으로 매 컴포넌트에서 타입을 반복 명시하는 것을 피한다.
- `PayloadAction<T>`와 `createApi`의 제네릭으로 액션 페이로드와 API 응답 모두에 타입 안전성을 확보하고, `createAsyncThunk`의 세 번째 제네릭(`rejectValue`)으로 실패 응답까지 타입을 붙인다.

## 참고 문헌 및 출처(추천)

- Redux Toolkit 공식 문서, "Usage With TypeScript"
- Redux 공식 문서, "Redux Essentials, TypeScript Quick Start"
- React-Redux 공식 문서, "Static Typing"

---

## 다음 글

- 다음: [29. Redux 성능 최적화와 디버깅 심화](../redux-performance-debugging/)
