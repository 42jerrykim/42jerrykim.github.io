---
title: "[Redux] 27. 정규화(Normalization) - 복잡한 데이터 관리"
description: "중첩된 게시글·댓글·작성자 데이터를 배열 그대로 저장할 때 생기는 중복 업데이트 문제를, ID를 키로 쓰는 정규화된 상태 구조와 Redux Toolkit의 createEntityAdapter로 해결하는 방법을 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 27
draft: false
slug: normalization
tags:
  - Redux
  - Redux-Toolkit
  - Data-Structures(자료구조)
  - Software-Architecture(소프트웨어아키텍처)
  - JavaScript
  - Performance(성능)
  - Frontend(프론트엔드)
  - Web(웹)
  - Best-Practices
  - Tutorial(튜토리얼)
  - Education(교육)
  - Code-Quality(코드품질)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Advanced
  - Deep-Dive
  - 정규화패턴
  - createEntityAdapter
  - id를키로쓰는저장
  - 중복데이터문제
  - 정규화선택자
  - Database(데이터베이스)
  - System-Design
  - Optimization(최적화)
---

# 27. 정규화(Normalization) - 복잡한 데이터 관리

25편의 블로그 앱에서 게시글과 댓글, 작성자 정보가 서로 얽히기 시작하면 배열 그대로 상태에 저장하는 방식이 한계를 드러냅니다. 이 편은 **정규화(Normalization)**라는, 관계형 데이터베이스에서 가져온 개념으로 이 문제를 해결합니다.

## 학습 목표

- 중첩·중복된 배열 구조가 업데이트 시 어떤 문제를 일으키는지 구체적인 버그로 설명할 수 있다.
- ID를 키로 쓰는 정규화된 상태 구조를 직접 설계할 수 있다.
- `createEntityAdapter`로 정규화된 CRUD 로직을 자동 생성할 수 있다.

## 문제: 중첩된 배열 구조의 중복 업데이트

게시글 목록에 작성자 정보가 통째로 포함된 구조를 생각해봅시다.

```javascript
// 비정규화된 상태: 작성자 정보가 게시글마다 중복으로 들어있다
const state = {
  posts: [
    { id: 1, title: "Redux 시작하기", author: { id: 7, name: "김리덕스" } },
    { id: 2, title: "정규화란?", author: { id: 7, name: "김리덕스" } }, // 같은 작성자가 중복 저장됨
    { id: 3, title: "타입스크립트 팁", author: { id: 9, name: "이타입" } },
  ],
};
```

`김리덕스`가 닉네임을 바꾸면 어떻게 될까요? 이 사람이 쓴 **모든 게시글의 `author` 필드를 찾아 전부** 업데이트해야 합니다. 게시글이 수백 개라면 리듀서 안에서 `state.posts.map(...)`으로 전체를 순회하며 조건에 맞는 항목을 찾아 고쳐야 하고, 하나라도 놓치면 화면에 낡은 이름이 남는 버그가 생깁니다.

```javascript
// 08편에서 배운 map()으로 불변 업데이트를 시도해도, 여전히 "전체 순회"가 필요하다
function userReducer(state, action) {
  switch (action.type) {
    case "user/renamed":
      return {
        ...state,
        posts: state.posts.map((post) =>
          post.author.id === action.payload.userId
            ? { ...post, author: { ...post.author, name: action.payload.newName } }
            : post
        ), // 게시글이 몇 개든 매번 전체를 순회해야 하나를 고칠 수 있다
      };
  }
}
```

## 해결책: ID를 키로 쓰는 정규화된 구조

관계형 데이터베이스가 데이터를 중복 없이 테이블로 나누듯, Redux 상태도 **엔티티 종류별로, ID를 키로 하는 객체**로 나눠 저장할 수 있습니다.

```javascript
// 정규화된 상태: 각 엔티티가 ID를 키로 단 한 번만 저장된다
const state = {
  posts: {
    byId: {
      1: { id: 1, title: "Redux 시작하기", authorId: 7 }, // author 전체가 아니라 authorId만 참조
      2: { id: 2, title: "정규화란?", authorId: 7 },
      3: { id: 3, title: "타입스크립트 팁", authorId: 9 },
    },
    allIds: [1, 2, 3], // 목록 순서를 유지하기 위한 ID 배열
  },
  users: {
    byId: {
      7: { id: 7, name: "김리덕스" }, // 작성자 정보는 여기 단 한 곳에만 존재
      9: { id: 9, name: "이타입" },
    },
    allIds: [7, 9],
  },
};
```

이제 `김리덕스`의 이름을 바꾸는 일은 **`users.byId[7]` 한 곳만 수정**하면 끝납니다.

```javascript
function usersReducer(state, action) {
  switch (action.type) {
    case "user/renamed":
      return {
        ...state,
        byId: {
          ...state.byId,
          [action.payload.userId]: {
            ...state.byId[action.payload.userId],
            name: action.payload.newName, // O(1)로 정확히 한 엔티티만 갱신
          },
        },
      };
  }
}
```

게시글이 몇 개든 관계없이 **한 번의 객체 속성 갱신**으로 끝납니다. 화면에서 게시글의 작성자 이름을 표시할 때는 `state.users.byId[post.authorId].name`처럼 참조로 조인합니다.

## 정규화된 데이터를 위한 selector

14편의 selector 패턴이 여기서 특히 중요해집니다. 컴포넌트가 정규화된 구조를 직접 알 필요 없이, selector가 "조인"을 대신 수행합니다.

```javascript
export const selectPostWithAuthor = (state, postId) => {
  const post = state.posts.byId[postId];
  const author = state.users.byId[post.authorId];
  return { ...post, author }; // UI가 필요로 하는 형태로 조립해서 반환
};
```

## createEntityAdapter: 정규화 로직 자동 생성

이 정규화 패턴(byId/allIds 구조, CRUD 리듀서, 관련 selector)은 매우 반복적이기 때문에, RTK는 `createEntityAdapter`로 이를 표준화합니다.

```javascript
import { createSlice, createEntityAdapter } from "@reduxjs/toolkit";

const postsAdapter = createEntityAdapter(); // 기본적으로 { ids: [], entities: {} } 구조를 사용

const postsSlice = createSlice({
  name: "posts",
  initialState: postsAdapter.getInitialState({ status: "idle" }), // 19편의 status와 결합 가능
  reducers: {
    postAdded: postsAdapter.addOne,       // 정규화된 추가 로직이 자동 제공됨
    postUpdated: postsAdapter.updateOne,  // 정규화된 부분 업데이트 로직이 자동 제공됨
    postRemoved: postsAdapter.removeOne,  // 정규화된 삭제 로직이 자동 제공됨
    postsReceived: postsAdapter.setAll,   // 서버에서 받은 배열 전체를 정규화해서 저장
  },
});

// 자동 생성된 selector들 — entities/ids 구조를 몰라도 사용 가능
export const {
  selectAll: selectAllPosts,
  selectById: selectPostById,
  selectIds: selectPostIds,
} = postsAdapter.getSelectors((state) => state.posts);
```

`createEntityAdapter`가 만드는 상태 구조는 앞서 손으로 만든 `byId`/`allIds`와 사실상 동일하며, 필드 이름만 `entities`/`ids`로 관례화되어 있습니다. `addOne`, `updateOne`, `removeOne`, `setAll` 같은 리듀서 함수를 직접 구현할 필요 없이 그대로 `reducers`에 연결할 수 있고, `getSelectors()`가 `selectAll`, `selectById` 같은 표준 selector도 함께 만들어줍니다.

## 서버 응답을 정규화하기: setAll

25편의 `getPosts` 쿼리가 반환하는 배열을 `postsReceived`로 dispatch하면, `setAll`이 배열을 자동으로 정규화된 구조로 변환합니다.

```javascript
dispatch(postsReceived([
  { id: 1, title: "Redux 시작하기", authorId: 7 },
  { id: 2, title: "정규화란?", authorId: 7 },
]));
// 이후 state.posts는 { ids: [1, 2], entities: { 1: {...}, 2: {...} } } 형태가 된다
```

24편의 RTK Query와 결합할 때는, `getPosts` 쿼리의 결과를 컴포넌트에서 그대로 배열로 쓰거나, 필요하다면 `transformResponse` 옵션으로 응답 자체를 정규화된 형태로 변환할 수도 있습니다.

## 정규화가 항상 필요한 것은 아니다

정규화는 다음 상황에서 뚜렷한 이점을 줍니다.

- 같은 엔티티(작성자, 태그 등)가 **여러 목록에 중복해서 나타난다.**
- 엔티티 하나를 업데이트/삭제하는 연산이 **빈번하다.**
- ID로 특정 항목 하나를 빠르게 찾아야 하는 경우가 많다(`byId[id]`는 O(1), 배열 `find()`는 O(n)).

반대로 게시글 하나에 딸린 댓글처럼, **다른 곳에서 재사용되지 않고 항상 부모와 함께 다뤄지는 데이터**는 굳이 정규화하지 않아도 됩니다. 모든 상태를 정규화하는 것은 오히려 불필요한 복잡도를 더할 수 있으므로, "중복이 실제로 문제가 되는 데이터"에 선택적으로 적용하는 것이 원칙입니다.

## 실무 체크리스트

- 같은 엔티티가 여러 목록에 중복으로 나타나 업데이트 시 여러 곳을 고쳐야 하는 상태가 있는가?
- 그런 데이터가 있다면 `createEntityAdapter`로 정규화해 O(1) 업데이트 구조로 바꿨는가?
- 모든 상태를 습관적으로 정규화하려 하고 있지는 않은가(재사용되지 않는 데이터는 정규화가 불필요할 수 있다)?

## 연습 과제

### 기초(★☆☆)
- 25편의 `posts` 배열을 `byId`/`allIds` 구조로 손수 정규화해보고, 게시글 하나의 제목을 수정하는 리듀서를 작성해보세요.

### 중급(★★☆)
- `createEntityAdapter`로 `postsSlice`를 다시 작성하고, `addOne`/`updateOne`/`removeOne`이 실제로 정규화된 구조를 올바르게 갱신하는지 확인해보세요.

### 고급(★★★)
- 정규화된 `posts`와 `users` 두 엔티티를 조합해, 특정 작성자가 쓴 모든 게시글 제목 목록을 반환하는 메모이제이션 selector(14편의 `createSelector` 활용)를 작성해보세요.

## 요약

- 중첩·중복된 배열 구조는 엔티티 하나를 바꿀 때 전체를 순회해야 하는 비효율과 누락 위험을 만든다.
- ID를 키로 쓰는 정규화된 구조는 엔티티 하나의 업데이트를 O(1)로 만들고, 중복 저장을 없앤다.
- `createEntityAdapter`가 정규화된 CRUD 리듀서와 표준 selector를 자동 생성해준다.

## 참고 문헌 및 출처(추천)

- Redux Toolkit 공식 문서, "createEntityAdapter" API 레퍼런스
- Redux 공식 문서, "Normalizing State Shape"
- Redux 공식 문서, "Redux Essentials, Part 6: Performance and Normalizing Data"

---

## 다음 글

- 다음: [28. Redux와 TypeScript - 타입 안전한 상태 관리](../redux-typescript/)
