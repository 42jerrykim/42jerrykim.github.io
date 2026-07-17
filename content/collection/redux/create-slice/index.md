---
title: "[Redux] 17. createSlice - 간결한 리듀서 작성"
description: "createSlice의 name·initialState·reducers 세 필드가 액션 타입, 액션 생성자, 리듀서를 어떻게 자동 생성하는지 15편의 counterSlice·todosSlice를 실제로 다시 작성하며 확인합니다. extraReducers도 함께 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 17
draft: false
slug: create-slice
image: "wordcloud.png"
tags:
  - Redux
  - Redux-Toolkit
  - JavaScript
  - React
  - Frontend(프론트엔드)
  - Web(웹)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Refactoring(리팩토링)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Intermediate
  - Implementation(구현)
  - API
  - createSlice문법
  - reducers필드
  - extraReducers
  - 액션타입자동생성
  - immer드래프트
  - prepare콜백
  - Type-Safety
  - Error-Handling(에러처리)
  - addMatcher패턴
  - breaking체인지주의
---

# 17. createSlice - 간결한 리듀서 작성

16편에서 `createSlice`가 무엇을 대신해주는지 미리 봤습니다. 이 편은 `createSlice`의 세 필드(`name`, `initialState`, `reducers`)를 하나씩 뜯어보고, 15편에서 순수 Redux로 작성한 `counterSlice`와 `todosSlice`를 실제로 다시 작성합니다.

## 학습 목표

- `createSlice`의 `name`, `initialState`, `reducers` 필드의 역할을 설명할 수 있다.
- `reducers`에 정의한 함수 이름으로부터 액션 타입과 액션 생성자가 어떻게 만들어지는지 설명할 수 있다.
- 페이로드가 여러 값으로 구성될 때 `prepare` 콜백을 사용할 수 있다.

## createSlice의 세 필드

```javascript
import { createSlice } from "@reduxjs/toolkit";

const counterSlice = createSlice({
  name: "counter",        // 이 slice의 이름 — 액션 타입의 접두사가 된다
  initialState: { count: 0 }, // 07편의 초기 상태와 동일한 역할
  reducers: {              // 액션 타입+생성자+리듀서 케이스를 한 번에 정의
    incremented: (state) => {
      state.count += 1;
    },
    decremented: (state) => {
      state.count -= 1;
    },
  },
});
```

- **`name: "counter"`**: `reducers`의 각 키(`incremented`)와 결합해 `"counter/incremented"`라는 액션 타입 문자열을 만든다.
- **`initialState`**: 07편에서 리듀서 함수의 기본 매개변수로 썼던 것과 동일하다.
- **`reducers`**: 각 함수가 07편의 `switch` 문 케이스 하나에 대응한다. 함수 이름이 곧 액션 타입의 나머지 부분이 된다.

**흔한 오개념 하나**: `reducers`의 키(`incremented`)는 단순한 함수 이름이 아니라, `name`과 결합해 **실제로 dispatch되는 액션 타입 문자열의 일부**가 됩니다. 즉 `incremented`를 `handleIncrement`로 리네이밍하면, 액션 타입도 `"counter/incremented"`에서 `"counter/handleIncrement"`로 바뀝니다. DevTools 로그에 남은 과거 기록이나, 이 액션 타입 문자열을 직접 참조하는 다른 코드(예: 다른 slice의 `extraReducers`)가 있다면 이 리네이밍은 **겉보기와 달리 브레이킹 체인지**입니다.

`createSlice`가 반환하는 객체는 `{ name, reducer, actions, caseReducers }`를 갖습니다. 이 중 `slice.reducer`(합쳐진 리듀서 함수)와 `slice.actions`(액션 생성자 모음)를 주로 씁니다.

```javascript
export const { incremented, decremented } = counterSlice.actions;
export const counterReducer = counterSlice.reducer;

// 사용법은 07편과 동일하다
counterReducer({ count: 0 }, incremented()); // { count: 1 }
```

## payload가 있는 액션: action.payload

인자를 받는 액션 생성자는 두 번째 매개변수 `action`으로 페이로드에 접근합니다.

```javascript
const counterSlice = createSlice({
  name: "counter",
  initialState: { count: 0 },
  reducers: {
    incremented: (state) => {
      state.count += 1;
    },
    incrementedBy: (state, action) => {
      state.count += action.payload; // 07편의 action.payload와 동일한 관례
    },
  },
});

export const { incrementedBy } = counterSlice.actions;
incrementedBy(5); // { type: "counter/incrementedBy", payload: 5 } — 자동 생성됨
```

`incrementedBy(5)`를 호출하면 `createSlice`가 자동으로 `{ type: "counter/incrementedBy", payload: 5 }` 형태의 액션 객체를 만들어줍니다. 07편에서 손으로 작성했던 `(amount) => ({ type: "counter/incrementedBy", payload: amount })`와 동일한 결과입니다.

## 15편의 counterSlice를 createSlice로 다시 쓰기

```javascript
// features/counter/counterSlice.js — RTK 버전
import { createSlice } from "@reduxjs/toolkit";

const counterSlice = createSlice({
  name: "counter",
  initialState: { count: 0 },
  reducers: {
    incremented: (state) => {
      state.count += 1;
    },
    decremented: (state) => {
      state.count -= 1;
    },
    incrementedBy: (state, action) => {
      state.count += action.payload;
    },
  },
});

export const { incremented, decremented, incrementedBy } = counterSlice.actions;
export default counterSlice.reducer;
```

15편의 순수 Redux 버전(액션 생성자 3개 + `switch` 문 4케이스, 총 22줄)과 비교하면 이 버전은 14줄입니다. 무엇보다 `"counter/incremented"` 같은 문자열을 어디에도 직접 쓰지 않았다는 점이 핵심입니다.

## 15편의 todosSlice를 createSlice로 다시 쓰기

배열 상태를 다루는 `todosSlice`도 다시 써봅니다. 08편에서 배운 불변 추가/삭제(`[...state, item]`, `filter()`)가 `createSlice` 안에서는 어떻게 바뀌는지 주목하세요.

```javascript
// features/todos/todosSlice.js — RTK 버전
import { createSlice, nanoid } from "@reduxjs/toolkit";

const todosSlice = createSlice({
  name: "todos",
  initialState: [],
  reducers: {
    todoAdded: {
      reducer: (state, action) => {
        state.push(action.payload); // Immer 덕분에 push()를 직접 써도 안전하다
      },
      prepare: (text) => ({
        payload: { id: nanoid(), text, done: false }, // 페이로드 조립 로직을 분리
      }),
    },
    todoToggled: (state, action) => {
      const todo = state.find((t) => t.id === action.payload);
      if (todo) todo.done = !todo.done; // 배열 안 객체를 직접 변경해도 Immer가 불변 업데이트로 변환
    },
    todoRemoved: (state, action) => {
      return state.filter((t) => t.id !== action.payload); // 필터링은 새 배열을 반환하는 편이 자연스럽다
    },
  },
});

export const { todoAdded, todoToggled, todoRemoved } = todosSlice.actions;
export default todosSlice.reducer;
```

15편에서 `[...state, item]`으로 불변 추가를 했던 것이, RTK 버전에서는 `state.push(action.payload)`로 **직접 변경처럼** 보입니다. 이것이 가능한 이유는 `createSlice`의 `reducers` 함수 내부에서 `state`가 실제 상태가 아니라 **Immer의 draft 객체**이기 때문입니다. draft에 가한 변경은 Immer가 추적해, 실제로는 새 불변 상태를 만들어 반환합니다. `todoRemoved`처럼 `return`으로 새 배열을 명시적으로 반환하는 것도 여전히 유효합니다.

## prepare 콜백: 페이로드 조립 로직 분리하기

`todoAdded`에서 쓴 `{ reducer, prepare }` 형태에 주목하세요. 액션 생성자가 받는 인자(`text`)와 실제 페이로드 형태(`{ id, text, done }`)가 다를 때, **`prepare` 콜백**으로 이 변환 로직을 리듀서와 분리합니다.

```javascript
todoAdded: {
  prepare: (text) => ({
    payload: { id: nanoid(), text, done: false }, // 여기서 id를 생성하고 형태를 조립
  }),
  reducer: (state, action) => {
    state.push(action.payload); // 리듀서는 조립된 payload를 그대로 사용
  },
},
```

`nanoid()`는 RTK가 내장 제공하는 고유 ID 생성 함수로, 15편에서 임시로 썼던 `Date.now()`보다 충돌 위험이 낮습니다. `prepare` 없이 `reducer`만 쓸 때는 액션 생성자가 받은 인자가 그대로 `action.payload`가 되지만, `prepare`를 쓰면 인자를 원하는 형태로 가공한 뒤 `payload`(그리고 필요하면 `meta`, `error`)로 반환할 수 있습니다.

## extraReducers: 다른 slice의 액션에 반응하기

가끔 한 slice의 리듀서가 **자신이 정의하지 않은 액션 타입**에 반응해야 할 때가 있습니다. 예를 들어 "전체 초기화" 액션이 여러 slice에 동시에 영향을 줄 때입니다.

```javascript
import { createAction } from "@reduxjs/toolkit";

export const allDataReset = createAction("app/allDataReset"); // 어느 slice에도 속하지 않는 공용 액션

const todosSlice = createSlice({
  name: "todos",
  initialState: [],
  reducers: {
    /* ... */
  },
  extraReducers: (builder) => {
    builder.addCase(allDataReset, () => {
      return []; // todos slice 소유가 아닌 액션에 반응해 초기화
    });
  },
});
```

`extraReducers`는 19편에서 다룰 `createAsyncThunk`가 자동 생성하는 pending/fulfilled/rejected 액션을 처리할 때 가장 자주 쓰입니다. 지금은 "slice 밖에서 정의된 액션에도 반응할 수 있다"는 것만 기억해두면 충분합니다.

`builder`는 `addCase` 외에도 두 가지 메서드를 더 제공합니다. **`addMatcher`**는 정확한 액션 타입이 아니라 **조건 함수**로 여러 액션에 한 번에 반응할 때 씁니다.

```javascript
import { isAnyOf } from "@reduxjs/toolkit";

extraReducers: (builder) => {
  builder.addMatcher(
    isAnyOf(fetchTodos.pending, fetchUser.pending), // 여러 thunk의 pending을 한 번에 매칭
    (state) => {
      state.status = "loading";
    }
  );
},
```

여러 개의 `createAsyncThunk`가 공통으로 "로딩 시작" 처리를 해야 할 때, `addCase`를 각 thunk마다 반복해서 쓰는 대신 `addMatcher` + `isAnyOf`로 한 번에 묶을 수 있습니다. **`addDefaultCase`**는 어떤 `addCase`/`addMatcher`에도 걸리지 않은 액션에 대한 기본 동작을 정의합니다(자주 쓰이지는 않지만, 알아두면 "매칭되지 않은 나머지"를 명시적으로 다룰 수 있습니다).

## 실무 체크리스트

- `reducers`의 함수 이름이 액션 타입의 의미를 명확히 드러내는가(`incremented`가 아니라 `handleClick` 같은 모호한 이름은 피한다)?
- 페이로드를 조립하는 로직이 복잡하다면 `prepare` 콜백으로 분리했는가?
- `extraReducers`가 필요한 경우는 "이 slice 밖에서 정의된 액션에 반응해야 할 때"로 한정하고 있는가?

## 연습 과제

### 기초(★☆☆)
- 15편의 `todosReducer`에서 `todoToggled`, `todoRemoved` 케이스를 `createSlice`의 `reducers`로 옮겨보세요(이미 위 예시에 있지만, 직접 타이핑하며 익혀보세요).

### 중급(★★☆)
- `prepare` 콜백을 사용해, `todoAdded`가 `priority`(`"high"`/`"normal"`/`"low"`) 인자도 받아 페이로드에 포함하도록 확장해보세요.

### 고급(★★★)
- `extraReducers`로 `counterSlice`가 `allDataReset` 액션에 반응해 `count`를 0으로 되돌리도록 구현해보세요.
- 두 개의 서로 다른 `createAsyncThunk`를 만들고, `addMatcher` + `isAnyOf`로 두 thunk의 `pending` 상태를 하나의 매처에서 함께 처리해보세요.

## 요약

- `createSlice`는 `name`+`reducers`의 키를 조합해 액션 타입을, `reducers`의 값으로 리듀서 케이스와 액션 생성자를 자동 생성한다.
- `reducers` 함수 안의 `state`는 Immer draft이므로 직접 변경 스타일과 `return` 스타일 모두 쓸 수 있다.
- 페이로드 조립이 복잡하면 `prepare` 콜백으로, slice 밖 액션에 반응해야 하면 `extraReducers`로 처리한다.

## 참고 문헌 및 출처(추천)

- Redux Toolkit 공식 문서, "createSlice" API 레퍼런스
- Redux Toolkit 공식 문서, "Usage With TypeScript, reducers.prepare"
- Immer 공식 문서, "Update patterns"

---

## 다음 글

- 다음: [18. configureStore - Store 설정 자동화](../configure-store/)
