---
title: "[Redux] 18. configureStore - Store 설정 자동화"
description: "07편의 createStore+combineReducers+applyMiddleware 조합을 configureStore 한 번의 호출로 대체합니다. 개발 환경 검사 미들웨어와 DevTools 연결은 물론, preloadedState로 SSR·영속화된 초기 상태를 주입하는 방법까지 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 18
draft: false
slug: configure-store
image: "wordcloud.png"
tags:
  - Redux
  - Redux-Toolkit
  - JavaScript
  - React
  - Frontend(프론트엔드)
  - Web(웹)
  - Software-Architecture(소프트웨어아키텍처)
  - Debugging(디버깅)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Intermediate
  - Implementation(구현)
  - configureStore문법
  - 미들웨어자동구성
  - 상태변경감지미들웨어
  - 직렬화감지미들웨어
  - devtools자동연결
  - 개발환경전용검사
  - Configuration(설정)
  - System-Design
  - preloadedState
  - enhancers확장
---

# 18. configureStore - Store 설정 자동화

07편에서 `createStore`와 `combineReducers`로 Store를 만들었고, 09편에서 미들웨어를 `applyMiddleware`로 연결하는 개념을 다뤘습니다. 이 편은 이 모든 설정을 `configureStore` 하나로 대체하고, RTK가 개발 환경에서 자동으로 켜주는 두 가지 검사 미들웨어를 살펴봅니다.

## 학습 목표

- `configureStore`로 여러 리듀서를 조합하고 DevTools까지 연결하는 Store를 만들 수 있다.
- 개발 환경에서 자동으로 켜지는 상태 변경 감지·직렬화 감지 미들웨어의 역할을 설명할 수 있다.
- `middleware` 옵션으로 기본 미들웨어를 확장하거나 커스터마이징할 수 있다.

## configureStore의 기본 사용법

```javascript
// store.js — RTK 버전
import { configureStore } from "@reduxjs/toolkit";
import counterReducer from "./features/counter/counterSlice";
import todosReducer from "./features/todos/todosSlice";

export const store = configureStore({
  reducer: {
    counter: counterReducer, // combineReducers를 내부적으로 자동 호출
    todos: todosReducer,
  },
});
```

15편의 순수 Redux 버전과 비교해봅시다.

```javascript
// 15편: 순수 Redux 버전
import { createStore, combineReducers } from "redux";
import { counterReducer } from "./features/counter/counterSlice";
import { todosReducer } from "./features/todos/todosSlice";

const rootReducer = combineReducers({ counter: counterReducer, todos: todosReducer });
export const store = createStore(rootReducer);
```

`configureStore`는 `reducer` 옵션에 객체를 전달하면 내부적으로 `combineReducers`를 자동 호출합니다(단일 리듀서 함수를 바로 전달할 수도 있습니다). 겉보기엔 큰 차이가 없어 보이지만, `configureStore`는 여기에 **더 많은 것을 기본으로 켜줍니다.**

## 자동으로 켜지는 것들

`configureStore`는 인자를 최소화해도 다음을 자동으로 설정합니다.

- **Redux DevTools Extension 연결**: 09편에서 다룬 시간 여행 디버깅이 별도 설정 없이 바로 동작한다.
- **`redux-thunk` 미들웨어**: 19편에서 다룰 비동기 로직에 필요한 미들웨어가 기본 포함된다.
- **개발 환경 전용 검사 미들웨어 두 가지**: 아래에서 자세히 다룬다.

```javascript
// 순수 Redux였다면 이 모든 것을 직접 조합해야 했다
import { createStore, combineReducers, applyMiddleware, compose } from "redux";
import thunk from "redux-thunk";

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(
  rootReducer,
  composeEnhancers(applyMiddleware(thunk))
);
```

`configureStore`가 이 조합을 대신해주므로, "DevTools 연결을 깜빡했다"거나 "프로덕션 빌드에 디버깅 코드가 남았다" 같은 실수가 줄어듭니다.

## 검사 미들웨어 1: 상태 변경 감지(Immutability Check)

08편에서 "리듀서 밖에서 상태를 직접 변경하면 안 된다"는 규칙을 배웠습니다. 개발 환경에서 `configureStore`는 **매 액션 이후 상태 트리를 검사해, 직접 변경이 있었는지 자동으로 감지**합니다.

```javascript
// 이 코드가 어딘가에 있다면 (버그: 리듀서 밖에서 상태를 직접 변경)
store.getState().todos.push({ id: 1, text: "잘못된 직접 변경" });

// 개발 환경의 configureStore는 콘솔에 다음과 같은 경고를 출력한다:
// "A state mutation was detected between dispatches, in the path 'todos.0'..."
```

이 검사는 상태 트리 크기에 비례해 비용이 들기 때문에 **프로덕션 빌드에서는 자동으로 꺼집니다.** 즉 개발 중에만 안전망 역할을 하고, 실제 배포 성능에는 영향을 주지 않습니다.

## 검사 미들웨어 2: 직렬화 감지(Serializability Check)

Redux 상태와 액션은 원칙적으로 **직렬화 가능한 값**(객체, 배열, 문자열, 숫자, 불리언, null)만 담아야 합니다. DevTools의 시간 여행 디버깅(09편)이나 상태를 `localStorage`에 저장하는 기능이 함수·클래스 인스턴스·Promise 같은 직렬화 불가능한 값이 섞이면 깨지기 때문입니다.

```javascript
// 나쁜 예: 액션 페이로드에 Date 객체(직렬화 불가능한 값)를 담음
dispatch({ type: "log/added", payload: { createdAt: new Date() } });

// 개발 환경의 configureStore는 다음과 같은 경고를 출력한다:
// "A non-serializable value was detected in the state, in the path `log.createdAt`..."
```

이 경고를 없애려면 `Date` 객체 자체를 상태에 넣지 않고, 직렬화 가능한 형태로 바꿔서 저장하면 됩니다.

```javascript
// 개선: Date 대신 직렬화 가능한 타임스탬프 문자열/숫자를 저장한다
dispatch({ type: "log/added", payload: { createdAt: Date.now() } }); // 숫자
// 또는
dispatch({ type: "log/added", payload: { createdAt: new Date().toISOString() } }); // 문자열
```

이 검사 역시 개발 환경 전용이며, 정말로 직렬화 불가능한 값을 의도적으로 저장해야 하는 드문 경우에는 아래처럼 특정 경로를 예외로 지정할 수 있습니다.

```javascript
import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: { /* ... */ },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ["file/uploadStarted"], // 이 액션 타입만 검사에서 제외
        ignoredPaths: ["upload.fileObject"],     // 이 상태 경로만 검사에서 제외
      },
    }),
});
```

## middleware 옵션으로 미들웨어 확장하기

기본 미들웨어(thunk + 두 검사 미들웨어)에 09편에서 만든 것 같은 커스텀 미들웨어를 추가하려면 `getDefaultMiddleware()`가 반환하는 배열에 이어 붙입니다.

```javascript
import { configureStore } from "@reduxjs/toolkit";
import { loggerMiddleware } from "./middleware/logger"; // 09편에서 만든 커스텀 미들웨어

export const store = configureStore({
  reducer: { /* ... */ },
  middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(loggerMiddleware),
});
```

`getDefaultMiddleware()`가 이미 thunk와 개발용 검사 미들웨어를 포함하고 있으므로, 이 배열을 통째로 교체하지 않고 `.concat()`으로 이어 붙이는 것이 기본값을 잃지 않는 방법입니다.

## preloadedState: Store를 빈 상태가 아닌 값으로 시작하기

실무에서는 Store를 항상 `initialState`(각 slice의 기본값)로만 시작하지 않습니다. 서버에서 미리 렌더링한 데이터를 그대로 이어받거나(SSR hydration), 이전 세션에서 `localStorage`에 저장해둔 상태를 복원해야 할 때는 `preloadedState` 옵션을 씁니다.

```javascript
import { configureStore } from "@reduxjs/toolkit";

// localStorage에 저장해둔 상태를 복원(직렬화된 문자열을 다시 객체로)
const persistedState = JSON.parse(localStorage.getItem("reduxState") ?? "null");

export const store = configureStore({
  reducer: { /* ... */ },
  preloadedState: persistedState ?? undefined, // 저장된 값이 없으면 각 slice의 initialState를 그대로 사용
});
```

`preloadedState`로 넘긴 값은 각 slice의 `initialState`를 **덮어씁니다.** SSR 환경에서는 서버가 이미 계산한 상태를 HTML에 직렬화해 내려보내고, 클라이언트 쪽 `configureStore`가 이를 `preloadedState`로 받아 "서버와 클라이언트가 같은 상태에서 시작하는" 하이드레이션을 구현합니다.

## enhancers: Store 생성 과정 자체를 확장하기

`enhancers` 옵션은 `middleware`보다 더 근본적인 확장 지점으로, **Store 생성 함수(`createStore`) 자체를 감싸는 고차 함수**를 추가합니다. 대부분의 프로젝트는 `configureStore`가 기본 제공하는 DevTools 연결만으로 충분하므로 이 옵션을 직접 쓸 일은 드물지만, 오프라인 지원이나 상태 영속화 같은 라이브러리가 내부적으로 이 지점을 사용합니다.

```javascript
export const store = configureStore({
  reducer: { /* ... */ },
  enhancers: (getDefaultEnhancers) => getDefaultEnhancers().concat(myCustomEnhancer),
});
```

`middleware`가 "액션이 리듀서에 도달하기 전"을 확장하는 지점이라면, `enhancers`는 그보다 바깥쪽인 "Store 자체가 어떻게 만들어지는가"를 확장하는 지점입니다. 이 둘의 관계는 21편에서 미들웨어 구조를 다룰 때 다시 짚습니다.

## 실무 체크리스트

- 새 프로젝트의 Store를 `createStore` + `applyMiddleware` 조합이 아니라 `configureStore`로 만들고 있는가?
- SSR이나 상태 영속화가 필요한 프로젝트라면 `preloadedState`로 초기 상태를 올바르게 주입하고 있는가?
- 개발 환경 콘솔에 상태 변경 감지·직렬화 감지 경고가 뜨면 무시하지 않고 원인을 찾아 고치고 있는가?
- 커스텀 미들웨어를 추가할 때 `getDefaultMiddleware()`를 대체하지 않고 확장하는 방식으로 쓰고 있는가?

## 연습 과제

### 기초(★☆☆)
- 15편의 `store.js`를 `configureStore`로 다시 작성하고, Redux DevTools Extension이 별도 설정 없이 연결되는지 확인해보세요.

### 중급(★★☆)
- 리듀서 안이 아닌 컴포넌트 코드에서 `store.getState().todos.push(...)`처럼 의도적으로 직접 변경을 실행해, 콘솔에 뜨는 경고 메시지를 관찰해보세요.

### 고급(★★★)
- 액션 페이로드에 `File` 객체(직렬화 불가능)를 담아 직렬화 감지 경고를 발생시킨 뒤, `ignoredActions`로 해당 액션 타입만 예외 처리해보세요.
- `localStorage`에 상태를 저장하는 코드와, 새로고침 시 그 값을 `preloadedState`로 복원하는 코드를 작성해 상태가 유지되는지 확인해보세요.

## 요약

- `configureStore`는 `combineReducers`, `applyMiddleware`, DevTools 연결을 한 번의 호출로 자동 설정한다.
- 개발 환경에서는 상태 변경 감지와 직렬화 감지 미들웨어가 기본으로 켜져 흔한 실수를 조기에 발견하게 해준다.
- 커스텀 미들웨어는 `getDefaultMiddleware()`를 대체하지 않고 이어 붙이는 방식으로 추가하고, `preloadedState`로 SSR·영속화된 초기 상태를 주입할 수 있다.

## 참고 문헌 및 출처(추천)

- Redux Toolkit 공식 문서, "configureStore" API 레퍼런스
- Redux Toolkit 공식 문서, "immutableStateInvariantMiddleware"
- Redux Toolkit 공식 문서, "serializableStateInvariantMiddleware"

---

## 다음 글

- 다음: [19. createAsyncThunk - 비동기 로직 단순화](../create-async-thunk/)
