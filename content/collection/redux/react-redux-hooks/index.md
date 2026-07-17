---
title: "[Redux] 12. React-Redux Hooks - useSelector와 useDispatch"
description: "실무 Redux 코드는 대부분 connect 대신 useSelector와 useDispatch를 씁니다. 두 Hook의 동작 원리와, useSelector가 새 객체를 반환할 때 무한 리렌더가 발생하는 흔한 함정을 코드로 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 12
draft: false
slug: react-redux-hooks
image: "wordcloud.png"
tags:
  - Redux
  - React
  - JavaScript
  - Frontend(프론트엔드)
  - Web(웹)
  - State
  - Performance(성능)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Pitfalls(함정)
  - Debugging(디버깅)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Intermediate
  - Edge-Cases(엣지케이스)
  - useSelector
  - useDispatch
  - 리액트훅
  - 무한리렌더
  - 얕은비교선택자
  - useState대체
  - 커스텀훅
---

# 12. React-Redux Hooks - useSelector와 useDispatch

11편의 `connect()`가 여전히 유효하다고 했지만, 실무 코드 대부분은 이제 **Hooks 방식**을 씁니다. 함수형 컴포넌트와 자연스럽게 어울리고, `mapStateToProps`/`mapDispatchToProps`를 별도로 정의할 필요가 없어 코드가 짧아집니다.

## 학습 목표

- `useSelector`로 상태의 일부를 구독하고, `useDispatch`로 Action을 dispatch할 수 있다.
- `useSelector`가 리렌더 여부를 판단하는 방식(얕은 비교)을 설명할 수 있다.
- `useSelector`에서 매번 새 객체를 반환해 생기는 불필요한 리렌더 문제를 진단하고 고칠 수 있다.

## useSelector: 상태의 일부를 구독한다

`useSelector`는 selector 함수를 받아, 그 함수가 반환하는 값을 컴포넌트에 연결합니다.

```jsx
import { useSelector } from "react-redux";

function Counter() {
  const count = useSelector((state) => state.counter.count);
  return <span>{count}</span>;
}
```

`useSelector`는 내부적으로 08편의 참조 비교(`===`)를 사용해, **selector가 반환하는 값이 이전 렌더링과 다를 때만** 컴포넌트를 리렌더링합니다. `state.counter.count`처럼 원시값(숫자·문자열·불리언)을 반환하면 값 자체가 비교되므로 예측 가능하게 동작합니다.

**왜 하필 참조 비교(`===`)를 기본값으로 골랐을까요?** 11편의 `connect()`가 쓰는 얕은 비교(객체의 각 속성을 하나씩 비교)는 객체의 속성 개수만큼 비교 연산이 필요합니다. 반면 참조 비교는 객체 크기와 무관하게 **항상 한 번의 연산**으로 끝나 성능이 예측 가능하고, `useSelector`를 어디서 몇 번 호출하든 비용이 일정합니다. 이 선택은 동시에 개발자에게 "selector는 되도록 원시값이나 안정된 참조를 반환하도록 작게 쪼개라"는 방향을 자연스럽게 유도합니다 — 객체를 반환하고 싶은 유혹이 들 때마다, 뒤에서 볼 "매번 새 객체 반환" 문제를 먼저 마주치게 되기 때문입니다.

## useDispatch: dispatch 함수를 가져온다

`useDispatch`는 Store의 `dispatch` 함수를 그대로 반환합니다.

```jsx
import { useDispatch } from "react-redux";

function IncrementButton() {
  const dispatch = useDispatch();
  return (
    <button onClick={() => dispatch({ type: "counter/incremented" })}>
      +1
    </button>
  );
}
```

두 Hook을 조합하면 `connect()`보다 훨씬 짧은 코드로 같은 결과를 얻습니다.

```jsx
// connect() 버전 (11편)
function Counter({ count, onIncrement }) {
  return <button onClick={onIncrement}>{count}</button>;
}
export default connect(
  (state) => ({ count: state.counter.count }),
  (dispatch) => ({ onIncrement: () => dispatch({ type: "counter/incremented" }) })
)(Counter);

// Hooks 버전 (이 편)
function Counter() {
  const count = useSelector((state) => state.counter.count);
  const dispatch = useDispatch();
  return <button onClick={() => dispatch({ type: "counter/incremented" })}>{count}</button>;
}
```

Hooks 버전은 `mapStateToProps`/`mapDispatchToProps`를 따로 정의할 필요가 없고, 컴포넌트 안에서 상태와 액션을 바로 사용합니다. 다만 이 방식은 컴포넌트가 Redux를 직접 알게 되므로(11편에서 강조한 "프레젠테이션 컴포넌트는 Redux를 몰라야 한다"는 분리가 약해집니다), 재사용성이 중요한 컴포넌트라면 여전히 `connect()`나 컨테이너/프레젠테이션 분리를 고려할 수 있습니다.

## 흔한 함정: useSelector에서 매번 새 객체를 반환하기

`useSelector`가 **매번 다른 참조를 가진 새 객체**를 반환하면, 값이 실제로 바뀌지 않았는데도 매 렌더링마다 리렌더가 발생합니다.

```jsx
// 나쁜 예: selector가 매번 새 객체를 만들어 반환한다
function OrderSummaryBad() {
  const summary = useSelector((state) => ({
    total: state.cart.total,
    itemCount: state.cart.items.length,
  })); // 매 렌더링마다 { total, itemCount } 새 객체 생성 → 매번 "달라짐"으로 판정

  return <div>{summary.itemCount}개, {summary.total}원</div>;
}
```

`state.cart`가 전혀 바뀌지 않아도, selector 함수 자체가 호출될 때마다 새 객체 리터럴 `{ total, itemCount }`를 만들기 때문에 `useSelector`의 참조 비교는 항상 "다르다"고 판단합니다. 그 결과 이 컴포넌트는 **Store의 다른 부분이 바뀔 때마다 불필요하게 리렌더**됩니다.

```jsx
// 개선 1: 원시값을 각각 별도로 구독한다
function OrderSummaryGood() {
  const total = useSelector((state) => state.cart.total);
  const itemCount = useSelector((state) => state.cart.items.length);
  return <div>{itemCount}개, {total}원</div>;
}

// 개선 2: 커스텀 비교 함수를 두 번째 인자로 전달한다
import { shallowEqual, useSelector } from "react-redux";

function OrderSummaryGood2() {
  const summary = useSelector(
    (state) => ({ total: state.cart.total, itemCount: state.cart.items.length }),
    shallowEqual // 객체의 각 속성을 얕게 비교해, 값이 같으면 리렌더하지 않음
  );
  return <div>{summary.itemCount}개, {summary.total}원</div>;
}
```

`shallowEqual`은 반환된 객체의 **속성값들을 하나씩** 비교하므로, 참조는 달라도 내용이 같으면 리렌더를 건너뜁니다. 원시값 여러 개를 각각 구독하는 방식(개선 1)이 더 간단하고 명시적이라 우선 권장되고, 객체 형태로 묶어야 할 이유가 있을 때만 `shallowEqual`을 씁니다. 이 주제는 13편(컴포넌트 최적화)에서 리렌더 성능 관점으로 더 깊이 다룹니다.

## Hooks의 성능 특성: connect와의 차이

`connect()`는 여러 `mapStateToProps` 호출을 배치로 처리해 최적화하지만, `useSelector`는 각 Hook 호출이 **독립적으로** 구독을 관리합니다. 즉 한 컴포넌트에서 `useSelector`를 여러 번 호출하면, 각 호출이 개별적으로 리렌더 여부를 판단합니다.

```jsx
function Dashboard() {
  const user = useSelector((state) => state.user); // 구독 1
  const cartCount = useSelector((state) => state.cart.items.length); // 구독 2

  // user가 바뀌면 이 컴포넌트가 리렌더되고, cartCount도 그 시점 값으로 다시 계산된다.
  // 두 구독은 독립적이지만 결과적으로 같은 컴포넌트의 리렌더를 함께 발생시킨다.
  return <div>{user.name}님, 장바구니 {cartCount}개</div>;
}
```

이 특성 때문에, 한 컴포넌트가 여러 개의 무관한 상태 조각을 구독하면 그중 하나만 바뀌어도 전체가 리렌더됩니다. 컴포넌트를 상태 단위로 잘게 쪼개는 것이 이 문제를 완화하는 방법이며, 13편에서 구체적으로 다룹니다.

## 실무 체크리스트

- `useSelector`가 반환하는 값이 원시값인가, 아니면 매번 새로 만들어지는 객체/배열인가?
- 객체를 반환해야 한다면 `shallowEqual`을 함께 쓰거나, 원시값 여러 개로 나눠 구독했는가?
- `useDispatch()`로 얻은 `dispatch`를 매 렌더링마다 새로 만든 함수로 감싸서 자식 컴포넌트의 리렌더를 유발하고 있지 않은가?

## 연습 과제

### 기초(★☆☆)
- `Counter`를 `connect()` 버전에서 `useSelector`/`useDispatch` 버전으로 직접 리팩터링해보세요.

### 중급(★★☆)
- `OrderSummaryBad`를 실제로 렌더링하고 React DevTools Profiler로 불필요한 리렌더가 발생하는지 확인한 뒤, `shallowEqual` 버전으로 고쳐보세요.

### 고급(★★★)
- 하나의 컴포넌트에서 `useSelector`를 5번 이상 호출하는 대신, 컴포넌트를 상태 단위로 쪼개 각각 하나씩만 구독하도록 리팩터링해보세요.

## 요약

- `useSelector`는 참조 비교로 리렌더 여부를 판단하고, `useDispatch`는 dispatch 함수를 그대로 반환한다.
- selector가 매번 새 객체를 반환하면 값이 안 바뀌어도 리렌더가 발생하므로, 원시값으로 나누거나 `shallowEqual`을 쓴다.
- `useSelector` 호출은 각각 독립적으로 구독을 관리하므로, 컴포넌트를 상태 단위로 잘게 나누는 것이 성능에 유리하다.

## 참고 문헌 및 출처(추천)

- React-Redux 공식 문서, "useSelector" API 레퍼런스
- React-Redux 공식 문서, "useDispatch" API 레퍼런스
- React-Redux 공식 문서, "Hooks FAQ: Why should I not create functions in mapDispatchToProps or useSelector?"

---

## 다음 글

- 다음: [13. 컴포넌트 최적화 - 리렌더링 제어](../component-optimization/)
