---
title: "[Redux] 26. Redux 프로젝트 구조 - 확장 가능한 설계"
description: "15·20·25편에서 계속 써온 feature 폴더 구조가 왜 옳은 선택인지 근거를 정리하고, 파일 타입별 구조와의 비교, 배럴 파일의 함정, 공용 로직을 위한 app/shared 계층 분리 방법까지 자세히 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 26
draft: false
slug: redux-project-structure
tags:
  - Redux
  - Software-Architecture(소프트웨어아키텍처)
  - Design-Pattern(디자인패턴)
  - JavaScript
  - React
  - Frontend(프론트엔드)
  - Web(웹)
  - Maintainability
  - Best-Practices
  - Code-Quality(코드품질)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Advanced
  - Deep-Dive
  - feature폴더구조
  - 파일타입별구조
  - 배럴파일
  - 공용로직분리
  - 도메인경계
  - Modularity
  - Coupling(결합도)
  - Cohesion(응집도)
  - eslint경계강제
---

# 26. Redux 프로젝트 구조 - 확장 가능한 설계

15편, 20편, 25편에서 실습마다 `features/counter/`, `features/todos/`, `features/posts/` 같은 **기능(feature) 단위 폴더 구조**를 계속 사용해왔습니다. 이 편은 그 선택의 근거를 정리하고, 프로젝트가 커질 때 이 구조를 어떻게 확장하는지 다룹니다.

## 학습 목표

- 파일 타입별 구조와 기능 단위 구조의 차이를 설명하고, 후자가 대규모 앱에서 유리한 이유를 설명할 수 있다.
- 여러 기능이 공유하는 로직을 위한 `app/`, `shared/` 계층을 설계할 수 있다.
- 배럴 파일(`index.js` re-export)의 편의성과 함정을 함께 설명할 수 있다.

## 파일 타입별 구조: 왜 흔히 보이지만 문제가 되는가

Redux 초기 문서와 예제에서 흔히 보이는 구조는 **파일의 역할(타입)로 폴더를 나누는 방식**입니다.

```
src/
  actions/
    counterActions.js
    todosActions.js
  reducers/
    counterReducer.js
    todosReducer.js
  components/
    Counter.jsx
    TodoList.jsx
```

이 구조의 문제는, `counter` 기능 하나를 수정하려면 `actions/`, `reducers/`, `components/` **세 폴더를 오가며** 파일을 찾아야 한다는 것입니다. 기능이 10개, 20개로 늘어나면 이 탐색 비용이 누적됩니다. 07편에서 액션·리듀서·selector가 항상 같은 기능을 다룬다는 것을 봤듯, **함께 바뀌는 코드는 함께 위치해야** 탐색과 수정이 쉽습니다.

## 기능 단위 구조: 15·20·25편에서 써온 방식

```
src/
  features/
    counter/
      counterSlice.js      # 리듀서 + 액션 생성자 (17편)
      counterSelectors.js  # selector (14편)
      Counter.jsx           # UI 컴포넌트
    todos/
      todosSlice.js
      todosSelectors.js
      TodoList.jsx
    posts/                  # 25편의 postsApi처럼 RTK Query 엔드포인트도 여기 포함
      postsApi.js
      PostDetail.jsx
  app/
    store.js
  App.jsx
```

`counter` 기능을 수정할 일이 생기면 `features/counter/` **폴더 하나만** 열면 됩니다. 이 원칙을 Redux 공식 문서는 "Ducks 패턴"이라고도 부르며(액션·리듀서를 기능별로 하나의 파일/폴더로 묶는 커뮤니티 컨벤션에서 유래), RTK의 `createSlice`가 액션과 리듀서를 애초에 하나로 묶어 반환하는 것도 이 철학과 맞닿아 있습니다.

## 여러 기능이 공유하는 로직: app/과 shared/

기능이 늘어나면 **여러 기능이 공통으로 쓰는 로직**이 생깁니다. 이를 위한 계층을 분리합니다.

```
src/
  app/
    store.js              # 18편: configureStore로 전체 리듀서 조합
    hooks.js               # 28편에서 다룰 타입 지정된 useSelector/useDispatch
  features/
    counter/
    todos/
    posts/
  shared/
    components/
      Button.jsx           # 여러 feature가 공통으로 쓰는 UI 컴포넌트
      Spinner.jsx
    api/
      baseApi.js            # 24편의 createApi 기본 설정(baseUrl 등)을 공유
    utils/
      formatDate.js
```

- **`app/`**: Store 조립, 앱 전역 설정처럼 "애플리케이션 자체"에 대한 코드.
- **`features/`**: 각 도메인 기능. 서로 직접 import하지 않는 것이 원칙(예: `todos`가 `counter`의 내부 파일을 직접 참조하지 않는다).
- **`shared/`**: 여러 feature가 함께 쓰는, 특정 도메인에 속하지 않는 코드.

이 분리는 08편에서 강조한 "예측 가능성"을 구조 수준으로 확장한 것입니다. 어떤 코드를 찾을 때 "이건 특정 기능의 것인가, 앱 전역 설정인가, 공용 유틸인가"를 폴더 이름만으로 짐작할 수 있습니다.

## 경계를 코드 리뷰가 아니라 도구로 강제하기

"`features`끼리 서로 직접 import하지 않는다"는 규칙은 팀원 모두가 기억하고 지켜야 하는 **약속**으로만 두면, 프로젝트가 커질수록 조금씩 어겨지기 쉽습니다. `eslint-plugin-boundaries` 같은 ESLint 플러그인은 이 규칙을 정적 분석으로 강제해, 어기는 import가 있으면 커밋 전에 에러로 잡아냅니다.

```javascript
// eslint.config.js (개념 예시 — 실제 옵션은 플러그인 문서를 따른다)
module.exports = {
  plugins: ["boundaries"],
  rules: {
    "boundaries/element-types": [
      "error",
      {
        rules: [
          // features는 서로를 직접 import할 수 없고, shared/app만 참조 가능
          { from: "features", disallow: ["features"], allow: ["shared", "app"] },
        ],
      },
    ],
  },
};
```

이렇게 하면 "리뷰어가 눈으로 발견해야 하는 규칙"이 "빌드가 실패하는 규칙"으로 바뀌어, 팀 규모가 커져도 경계가 조용히 무너지는 것을 막을 수 있습니다.

## RTK Query의 baseApi 분리 패턴

25편에서 `postsApi`를 만들 때 `createApi`를 직접 호출했지만, 여러 API 슬라이스가 있는 프로젝트에서는 `injectEndpoints`로 기본 설정을 공유하는 것이 일반적입니다.

```javascript
// shared/api/baseApi.js
import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const baseApi = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({ baseUrl: "/api" }),
  tagTypes: ["Post", "Comment", "User"], // 프로젝트 전체 태그를 한곳에서 관리
  endpoints: () => ({}), // 엔드포인트는 각 feature에서 주입
});
```

```javascript
// features/posts/postsApi.js
import { baseApi } from "../../shared/api/baseApi";

export const postsApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getPosts: builder.query({ query: () => "/posts", providesTags: ["Post"] }),
  }),
});

export const { useGetPostsQuery } = postsApi;
```

`injectEndpoints`를 쓰면 `baseQuery`, `tagTypes` 같은 공통 설정을 한 곳(`baseApi.js`)에서만 관리하면서, 각 기능은 자신의 엔드포인트만 선언할 수 있습니다. Store에는 `baseApi`의 리듀서/미들웨어 하나만 등록하면 됩니다.

## 배럴 파일: 편의성과 함정

기능 폴더의 내부 파일들을 하나의 진입점으로 재수출하는 **배럴 파일**(`index.js`)은 import 문을 짧게 만들어줍니다.

```javascript
// features/todos/index.js — 배럴 파일
export { default as todosReducer } from "./todosSlice";
export { todoAdded, todoToggled, todoRemoved } from "./todosSlice";
export { selectAllTodos, selectCompletedCount } from "./todosSelectors";
```

```javascript
// 배럴 파일이 있으면
import { todosReducer, todoAdded, selectAllTodos } from "features/todos";
// 배럴 파일이 없으면
import todosReducer, { todoAdded } from "features/todos/todosSlice";
import { selectAllTodos } from "features/todos/todosSelectors";
```

편리해 보이지만, 배럴 파일에는 실무에서 자주 부딪히는 함정이 있습니다.

- **번들 크기**: 일부 번들러 설정에서는 배럴 파일의 export 하나만 써도 파일 전체가 번들에 포함될 수 있다(트리 셰이킹이 항상 완벽하지 않음).
- **순환 참조**: `features/todos/index.js`가 `features/posts`를 참조하고, `posts`의 배럴 파일이 다시 `todos`를 참조하면 순환 의존성이 생기기 쉽다.
- **탐색 어려움**: "이 함수가 실제로 어느 파일에 정의되어 있는가"를 IDE의 "정의로 이동" 없이 육안으로 찾기 어려워진다.

이런 이유로, 큰 프로젝트에서는 배럴 파일을 아예 쓰지 않거나, feature 최상위 딱 한 단계에서만(내부 하위 폴더까지 전파하지 않고) 제한적으로 사용하는 경우가 많습니다. 프로젝트 규모가 작다면 배럴 파일의 편의성이 더 크므로, 이는 "항상 옳은 규칙"이 아니라 **규모에 따라 판단할 트레이드오프**입니다.

## 실무 체크리스트

- 새 기능을 추가할 때 하나의 `features/<기능명>/` 폴더 안에서 대부분의 작업이 끝나는가?
- 여러 기능이 공유하는 코드가 특정 feature 폴더 안에 우연히 놓여있지 않고 `shared/`로 분리되어 있는가?
- "feature끼리 직접 import하지 않는다"는 규칙을 사람의 리뷰에만 의존하지 않고, ESLint 같은 도구로 강제하고 있는가?
- 배럴 파일을 쓴다면, 프로젝트 규모와 번들러 설정을 고려해 의도적으로 선택한 것인가?

## 연습 과제

### 기초(★☆☆)
- 25편의 `postsApi`, `commentsApi` 관련 코드를 `features/posts/`, `features/comments/` 폴더로 재배치해보세요.

### 중급(★★☆)
- 여러 feature가 공통으로 쓰는 `formatDate` 유틸 함수를 `shared/utils/`로 분리하고, 각 feature에서 상대 경로로 import해보세요.

### 고급(★★★)
- `baseApi.injectEndpoints` 패턴으로 `postsApi`와 `commentsApi`를 하나의 `baseApi` 위에 분리해 구현해보세요.

## 요약

- 기능 단위(feature) 폴더 구조는 함께 바뀌는 코드를 함께 위치시켜, 파일 타입별 구조보다 대규모 앱에서 탐색·유지보수가 쉽다.
- `app/`(앱 전역), `features/`(도메인별), `shared/`(공용) 세 계층으로 나누면 책임 경계가 명확해진다.
- 배럴 파일은 편의성과 번들 크기·순환 참조 위험 사이의 트레이드오프이므로, 프로젝트 규모에 맞게 판단한다.

## 참고 문헌 및 출처(추천)

- Redux 공식 문서, "Structuring Reducers, Reducer Structure Approaches"
- Redux Toolkit 공식 문서, "Redux Essentials, Part 6: Performance and Normalizing Data" (프로젝트 구조 관련 서두)
- Redux Toolkit 공식 문서, "RTK Query, Code Splitting" (injectEndpoints)

---

## 다음 글

- 다음: [27. 정규화(Normalization) - 복잡한 데이터 관리](../normalization/)
