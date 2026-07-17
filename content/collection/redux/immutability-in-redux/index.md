---
title: "[Redux] 08. 불변성의 중요성 - Immutability in Redux"
description: "리듀서에서 상태를 직접 변경하면 리렌더가 일어나지 않거나, Redux DevTools의 시간여행 디버깅이 무의미해집니다. 불변성이 왜 필요한지, 얕은 비교가 이를 어떻게 이용하는지 실제 버그 재현 코드로 확인합니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 8
draft: false
slug: immutability-in-redux
tags:
  - Redux
  - JavaScript
  - React
  - State
  - Immutability
  - Frontend(프론트엔드)
  - Web(웹)
  - Performance(성능)
  - Debugging(디버깅)
  - Software-Architecture(소프트웨어아키텍처)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Pitfalls(함정)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Intermediate
  - 불변성
  - 얕은비교
  - 참조동등성
  - 리렌더최적화
  - 시간여행디버깅
  - immer라이브러리
  - 중첩업데이트
---

# 08. 불변성의 중요성 - Immutability in Redux

02·03편에서 스프레드와 `map`/`filter`가 "원본을 바꾸지 않고 새 값을 만드는" 도구라고 배웠습니다. 이 편은 Redux가 **왜** 그렇게까지 불변성을 강제하는지, 어기면 정확히 어떤 문제가 생기는지를 다룹니다.

## 학습 목표

- React-Redux가 리렌더 여부를 판단하는 데 쓰는 "얕은 비교"의 동작 원리를 설명할 수 있다.
- 상태를 직접 변경했을 때 실제로 어떤 버그가 생기는지 코드로 재현할 수 있다.
- 중첩된 상태를 안전하게 업데이트하는 패턴과 Immer 라이브러리의 역할을 이해한다.

## 얕은 비교: React-Redux가 변경을 감지하는 방법

React-Redux는 상태가 "바뀌었는지"를 확인할 때, 객체 내부를 깊이 들여다보지 않고 **참조(reference)가 같은지만** 비교합니다(`===` 연산자, 얕은 비교).

```javascript
const state1 = { count: 0 };
const state2 = { count: 0 };
const state3 = state1;

console.log(state1 === state2); // false — 내용은 같지만 다른 객체(다른 참조)
console.log(state1 === state3); // true — 같은 객체를 가리킴(같은 참조)
```

이 방식이 빠른 이유는 객체가 아무리 크고 깊어도 참조 하나만 비교하면 되기 때문입니다. 하지만 이 방식이 성립하려면 **"값이 바뀌었으면 반드시 새 참조를 만들어야 한다"**는 규칙을 개발자가 지켜야 합니다.

## 상태를 직접 변경하면 생기는 버그

리듀서에서 상태를 직접 변경(mutate)하면, 값은 바뀌었지만 **참조는 그대로**이므로 React-Redux가 변경을 감지하지 못합니다.

```javascript
// 나쁜 예: 상태를 직접 변경
function todosReducerBad(state = [], action) {
  switch (action.type) {
    case "todos/toggled": {
      const todo = state.find((t) => t.id === action.payload.id);
      if (todo) {
        todo.done = !todo.done; // 배열 안의 객체를 직접 변경!
      }
      return state; // 배열 자체의 참조는 바뀌지 않았다
    }
    default:
      return state;
  }
}
```

이 리듀서는 실제로 `todo.done` 값을 바꾸지만, `state`(배열)의 참조가 그대로이므로 `useSelector`로 이 배열을 구독하는 컴포넌트는 **리렌더되지 않습니다.** 게다가 리듀서가 원본을 직접 바꿔버렸기 때문에, Redux DevTools에서 이전 상태로 "되감기"를 해도 이미 원본이 오염되어 있어 정확한 과거 상태를 복원할 수 없습니다. 06편에서 말한 "시간여행 디버깅"이 이 원칙이 지켜질 때만 신뢰할 수 있는 이유입니다.

```javascript
// 개선: 불변성을 지키며 새 배열·새 객체를 반환
function todosReducerGood(state = [], action) {
  switch (action.type) {
    case "todos/toggled":
      return state.map((todo) =>
        todo.id === action.payload.id ? { ...todo, done: !todo.done } : todo
      );
    default:
      return state;
  }
}
```

이번에는 `map()`이 항상 **새 배열**을 반환하고, 바뀐 항목만 `{ ...todo, done: !todo.done }`으로 **새 객체**가 됩니다. 바뀌지 않은 항목은 원래 참조를 그대로 유지하므로, 해당 항목을 개별적으로 구독하는 컴포넌트(14편의 selector 패턴)는 불필요하게 리렌더되지 않습니다.

## 중첩된 상태를 업데이트할 때의 함정

02편에서 본 "얕은 복사의 함정"이 리듀서에서 특히 자주 문제가 됩니다.

```javascript
const state = {
  user: { id: 1, profile: { nickname: "Kim" } },
};

// 나쁜 예: 스프레드 한 번으로는 중첩된 값을 안전하게 바꾸지 못한다
function badUpdate(state, newNickname) {
  const next = { ...state };
  next.user.profile.nickname = newNickname; // user와 profile은 여전히 원본 참조!
  return next;
}
```

`{ ...state }`는 최상위 속성만 새로 복사하고, `user`와 `profile`은 원본과 **같은 참조**를 그대로 가리킵니다. 그래서 `next.user.profile.nickname = newNickname`은 사실 원본 `state.user.profile`까지 변경해버립니다.

```javascript
// 개선: 중첩된 단계마다 스프레드를 적용
function goodUpdate(state, newNickname) {
  return {
    ...state,
    user: {
      ...state.user,
      profile: {
        ...state.user.profile,
        nickname: newNickname,
      },
    },
  };
}
```

상태가 깊이 중첩될수록 이런 코드는 빠르게 장황해집니다. 이 문제 때문에 실무에서는 **정규화**(중첩 대신 평평한 구조로 저장, 27편에서 다룸)로 애초에 중첩을 줄이거나, **Immer** 같은 라이브러리를 씁니다.

## Immer: "직접 바꾸는 것처럼" 쓰고 불변 업데이트를 얻는다

**Immer**는 "초안(draft)"이라는 프록시 객체를 통해, 마치 직접 변경하는 것처럼 코드를 쓰면 실제로는 불변 업데이트된 새 객체를 만들어주는 라이브러리입니다.

```javascript
import { produce } from "immer";

const goodUpdateWithImmer = (state, newNickname) =>
  produce(state, (draft) => {
    draft.user.profile.nickname = newNickname; // 직접 대입처럼 보이지만 안전하다
  });
```

`produce()`는 `draft`에 가해진 "변경"을 추적해, 실제로는 원본을 바꾸지 않고 필요한 부분만 새로 만든 객체를 반환합니다. Redux Toolkit의 `createSlice`(17편)는 Immer를 내장하고 있어서, 리듀서 안에서 `state.field = value`처럼 써도 실제로는 불변성이 지켜집니다. 이 편에서 배운 "왜 불변성이 필요한가"를 이해하고 나면, Immer가 무엇을 대신해주는지도 정확히 알 수 있습니다.

## 실무 체크리스트

- 리듀서에서 배열·객체의 속성을 직접 대입(`arr[i].x = y`, `obj.field = value`)하고 있지 않은가?
- 중첩된 상태를 업데이트할 때 중첩 단계마다 스프레드를 적용했는가, 아니면 Immer를 쓰고 있는가?
- 변경되지 않은 항목까지 불필요하게 새 객체로 만들어 리렌더를 낭비하고 있지 않은가?

## 연습 과제

### 기초(★☆☆)
- `todosReducerBad`를 실행 전후로 `console.log(prevState === nextState)`를 찍어, 참조가 바뀌지 않았음을 직접 확인해보세요.

### 중급(★★☆)
- 3단계로 중첩된 객체(`{ a: { b: { c: 1 } } }`)에서 `c` 값만 바꾸는 불변 업데이트를 스프레드로 작성하고, Immer 버전과 코드량을 비교해보세요.

### 고급(★★★)
- `todosReducerGood`을 실행할 때, 변경된 항목과 변경되지 않은 항목 각각의 참조가 이전 상태와 같은지 다른지 확인하는 테스트를 작성해보세요.

## 요약

- React-Redux는 참조 비교(얕은 비교)로 변경을 감지하므로, 값이 바뀌면 반드시 새 참조를 만들어야 한다.
- 상태를 직접 변경하면 리렌더가 일어나지 않거나 시간여행 디버깅이 깨지는 버그로 이어진다.
- 중첩된 상태는 단계마다 스프레드하거나, Immer로 "직접 바꾸는 것처럼" 쓰면서 불변성을 지킬 수 있다.

## 참고 문헌 및 출처(추천)

- Redux 공식 문서, "Immutable Update Patterns"
- Immer 공식 문서, "Introduction" — Immer의 동작 원리(구조적 공유, Proxy)
- Redux 공식 문서, "Why Redux? / Immutability"

---

## 다음 글

- 다음: [09. Redux 데이터 흐름 이해하기](../redux-data-flow/)
