---
title: "[Redux] 14. 데이터 선택자 - Selector 패턴"
description: "필터링·정렬 같은 파생 데이터 계산을 컴포넌트 안에 직접 쓰면 매 렌더링마다 다시 계산됩니다. Reselect의 createSelector로 입력이 바뀔 때만 재계산하는 메모이제이션 selector를 만드는 방법을 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 14
draft: false
slug: selector-patterns
image: "wordcloud.png"
tags:
  - Redux
  - React
  - JavaScript
  - Performance(성능)
  - Optimization(최적화)
  - Design-Pattern(디자인패턴)
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
  - Deep-Dive
  - selector패턴
  - reselect라이브러리
  - createSelector
  - 메모이제이션
  - 파생데이터
  - 캐시무효화
  - 재사용가능선택자
  - Implementation(구현)
---

# 14. 데이터 선택자 - Selector 패턴

13편에서 "구독 범위를 좁혀라"고 했지만, 필터링·정렬·합계 같은 **계산이 필요한 파생 데이터**는 단순히 좁게 구독하는 것만으로는 부족합니다. 이 편은 **Selector 패턴**과 **Reselect** 라이브러리로, 계산 비용이 있는 파생 데이터를 필요할 때만 다시 계산하는 방법을 다룹니다.

## 학습 목표

- Selector 함수로 상태 접근 로직을 컴포넌트에서 분리할 수 있다.
- `createSelector`로 메모이제이션된 selector를 만들어 불필요한 재계산을 막을 수 있다.
- 메모이제이션 selector의 캐시가 무효화되는 조건을 설명할 수 있다.

## Selector 함수: 상태 접근 로직을 한곳에 모은다

**Selector**는 상태를 받아 필요한 값을 반환하는 단순한 함수입니다. 이미 12–13편에서 `useSelector((state) => ...)`에 인라인으로 써왔지만, 이를 **이름 있는 함수로 분리**하면 재사용성과 가독성이 좋아집니다.

```javascript
// selectors.js — 상태 접근 로직을 한곳에 모은다
export const selectAllTodos = (state) => state.todos;
export const selectCartItemCount = (state) => state.cart.items.length;
export const selectTodoById = (state, id) => state.todos.find((todo) => todo.id === id);
```

컴포넌트는 이 selector를 가져다 `useSelector`에 넘기기만 하면 되고, 상태가 `state.cart.items`에 있는지 다른 경로에 있는지는 알 필요가 없습니다.

```jsx
import { useSelector } from "react-redux";
import { selectCartItemCount } from "./selectors";

function CartBadge() {
  const itemCount = useSelector(selectCartItemCount);
  return <span>{itemCount}</span>;
}
```

이렇게 분리하면 상태 구조가 바뀌었을 때 **selector 파일 한 곳만 수정**하면 되고, 여러 컴포넌트가 같은 selector를 재사용할 수 있습니다. 27편(정규화)에서 상태 구조를 리팩터링할 때 이 이점이 특히 커집니다.

## 계산 비용이 있는 파생 데이터의 문제

단순 필드 접근을 넘어, **필터링·정렬·합계** 같은 계산이 필요한 selector를 생각해봅시다.

```javascript
// 계산 비용이 있는 selector: 호출할 때마다 filter + reduce를 다시 실행
export const selectCompletedTodoCount = (state) =>
  state.todos.filter((todo) => todo.done).length;

export const selectCartTotal = (state) =>
  state.cart.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
```

이 selector들은 03편에서 배운 `filter`/`reduce`를 쓰지만, `useSelector`에 직접 연결하면 **컴포넌트가 리렌더될 때마다(다른 이유로 리렌더되더라도) 매번 새로 계산**됩니다. 목록이 크거나 계산이 복잡할수록 이는 실질적인 성능 문제가 됩니다.

## createSelector: 입력이 바뀔 때만 재계산한다

**Reselect** 라이브러리의 `createSelector`는 **메모이제이션**된 selector를 만듭니다. 입력값이 이전과 같으면 저장해둔 결과를 재사용하고, 입력이 바뀔 때만 실제로 다시 계산합니다.

```javascript
import { createSelector } from "reselect"; // 15편까지는 Toolkit 없이 이 라이브러리를 직접 설치해 쓴다(16편부터는 @reduxjs/toolkit이 재수출하는 동일한 함수를 쓴다)

const selectTodos = (state) => state.todos; // 입력 selector: 원본 상태 조각을 그대로 반환

export const selectCompletedTodoCount = createSelector(
  [selectTodos], // 입력 selector 목록
  (todos) => todos.filter((todo) => todo.done).length // 결과 계산 함수
);
```

`createSelector`는 두 부분으로 구성됩니다.

- **입력 selector**: 원본 상태에서 필요한 조각을 가져온다(`selectTodos`).
- **결과 함수**: 입력 selector들의 결과를 받아 최종 값을 계산한다.

`createSelector`가 반환하는 최종 selector는 다음 규칙으로 동작합니다. **모든 입력 selector의 반환값이 이전 호출과 참조가 같으면(`===`), 결과 함수를 다시 실행하지 않고 캐시된 값을 그대로 반환합니다.** `todos` 배열의 참조가 바뀌지 않았다면(즉 todos와 무관한 다른 상태가 바뀌어 컴포넌트가 리렌더된 것이라면), `filter().length` 계산을 다시 하지 않습니다.

## 캐시가 무효화되는 조건

메모이제이션이 효과를 보려면 입력 selector가 반환하는 값의 **참조 안정성**이 중요합니다. 08편에서 배운 원칙이 여기서도 그대로 적용됩니다.

```javascript
// 위험: 입력 selector가 매번 새 배열을 만들어 반환하면 캐시가 항상 무효화된다
const selectActiveTodosBad = (state) => state.todos.filter((t) => !t.done); // 매번 새 배열!

export const selectActiveTodoTextsBad = createSelector(
  [selectActiveTodosBad], // 이 입력이 매번 새 참조이므로 캐시가 절대 재사용되지 않는다
  (activeTodos) => activeTodos.map((t) => t.text)
);
```

`selectActiveTodosBad`가 이미 `filter()`로 새 배열을 만들어 반환하고 있으므로, 이를 `createSelector`의 입력으로 쓰면 캐시가 무의미해집니다. **입력 selector는 상태에서 원본 조각을 그대로 꺼내기만 하고, 계산은 결과 함수 안에서** 해야 캐싱이 제대로 작동합니다.

```javascript
// 개선: 원본 조각만 반환하는 selector를 입력으로 쓰고, 계산은 결과 함수 안에서
export const selectActiveTodoTexts = createSelector(
  [selectTodos], // state.todos를 그대로 반환(원본 참조 유지)
  (todos) => todos.filter((t) => !t.done).map((t) => t.text) // 계산은 여기서만
);
```

## 여러 입력을 조합하는 selector

`createSelector`는 여러 입력 selector를 조합할 수도 있습니다.

```javascript
const selectCartItems = (state) => state.cart.items;
const selectDiscountRate = (state) => state.cart.discountRate;

export const selectCartTotalAfterDiscount = createSelector(
  [selectCartItems, selectDiscountRate],
  (items, discountRate) => {
    const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    return Math.round(subtotal * (1 - discountRate));
  }
);
```

`items`와 `discountRate` 중 **어느 하나라도 바뀌어야만** 최종 계산이 다시 실행됩니다. 둘 다 그대로면 이전 결과를 그대로 재사용합니다.

## 매개변수가 있는 selector: 팩토리 패턴

`id`처럼 컴포넌트마다 다른 값을 받아야 하는 selector는, `createSelector`를 **한 번만** 만들면 모든 컴포넌트가 같은 캐시를 공유하게 되어 오히려 캐시가 계속 무효화되는 문제가 생깁니다. 이런 경우 컴포넌트별로 독립된 selector 인스턴스를 만드는 **팩토리 패턴**을 씁니다.

```javascript
// 컴포넌트마다 독립된 캐시를 갖도록 selector를 "만드는 함수"를 export
export const makeSelectTodoById = () =>
  createSelector(
    [selectTodos, (state, id) => id],
    (todos, id) => todos.find((todo) => todo.id === id)
  );
```

```jsx
function TodoItemById({ id }) {
  // 컴포넌트 인스턴스마다 독립된 selector를 useMemo로 한 번만 생성
  const selectTodoById = useMemo(makeSelectTodoById, []);
  const todo = useSelector((state) => selectTodoById(state, id));
  // ...
}
```

이 패턴은 13편의 `TodoItemById`처럼 리스트 항목마다 반복 렌더링되는 컴포넌트에서 특히 중요합니다.

## 실무 체크리스트

- 필터링·정렬·합계 같은 계산이 필요한 selector에 `createSelector`를 적용했는가?
- `createSelector`의 입력 selector가 매번 새 참조를 반환하는 계산을 포함하고 있지 않은가?
- 리스트 항목마다 쓰이는 매개변수 있는 selector를, 컴포넌트별 캐시가 섞이지 않도록 팩토리 패턴으로 만들었는가?

## 연습 과제

### 기초(★☆☆)
- `selectCartTotal`을 `createSelector`를 사용한 메모이제이션 버전으로 바꿔보세요.

### 중급(★★☆)
- `selectCartItems`와 검색어 상태(`state.cart.searchQuery`)를 조합해, 검색어를 포함하는 상품만 걸러내는 selector를 작성해보세요.

### 고급(★★★)
- 콘솔에 로그를 남기는 결과 함수로 selector를 감싸서, 상태의 다른 부분이 바뀔 때 결과 함수가 실제로 재실행되지 않는지(캐시가 재사용되는지) 직접 확인해보세요.

## 요약

- Selector 함수로 상태 접근 로직을 컴포넌트에서 분리하면 재사용성과 유지보수성이 좋아진다.
- `createSelector`는 입력이 바뀔 때만 결과를 재계산하는 메모이제이션 selector를 만든다.
- 입력 selector는 원본 조각만 반환해야 캐시가 제대로 작동하며, 매개변수가 있는 selector는 컴포넌트별로 독립된 인스턴스를 만들어야 한다.

## 참고 문헌 및 출처(추천)

- Reselect 공식 문서(GitHub), "createSelector"
- Redux 공식 문서, "Deriving Data with Selectors"
- Redux Toolkit 공식 문서, "createSelector" — RTK에 내장된 Reselect 재수출

---

## 다음 글

- 다음: [15. 실습: Counter와 Todo 앱 만들기](../practice-counter-todo/)
