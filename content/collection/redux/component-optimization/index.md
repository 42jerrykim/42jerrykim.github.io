---
title: "[Redux] 13. 컴포넌트 최적화 - 리렌더링 제어"
description: "구독 범위를 잘못 잡으면 상태 일부만 바뀌어도 앱 전체가 다시 그려집니다. 구독 범위 좁히기, React.memo, 리스트 컴포넌트 분리라는 세 가지 기법으로 불필요한 리렌더를 실측 가능한 수준까지 줄이는 방법을 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 13
draft: false
slug: component-optimization
tags:
  - Redux
  - React
  - JavaScript
  - Performance(성능)
  - Optimization(최적화)
  - Frontend(프론트엔드)
  - Web(웹)
  - Debugging(디버깅)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Intermediate
  - Deep-Dive
  - 리렌더링
  - 구독범위
  - reactmemo
  - 컴포넌트분리
  - 프로파일러
  - 메모이제이션
  - 리스트가상화
  - Profiling(프로파일링)
---

# 13. 컴포넌트 최적화 - 리렌더링 제어

12편에서 `useSelector`가 리렌더를 유발하는 조건을 봤습니다. 이 편은 실제 앱에서 "왜 이 컴포넌트가 필요 이상으로 자주 그려지는가"를 진단하고, 구체적인 세 가지 기법으로 줄이는 방법을 다룹니다.

## 학습 목표

- `useSelector`의 구독 범위를 좁혀 불필요한 리렌더를 줄일 수 있다.
- `React.memo`로 props가 바뀌지 않은 컴포넌트의 리렌더를 건너뛸 수 있다.
- 리스트를 렌더링할 때 항목 단위로 컴포넌트를 분리해야 하는 이유를 설명할 수 있다.

## 문제 진단: React DevTools Profiler로 확인한다

최적화를 하기 전에 **실제로 무엇이 얼마나 자주 리렌더되는지** 측정해야 합니다. React DevTools의 Profiler 탭에서 "Highlight updates when components render" 옵션을 켜면, 화면에서 리렌더되는 컴포넌트가 실시간으로 표시됩니다. 추측으로 최적화를 시작하면 실제로 문제가 아닌 곳에 시간을 쓰기 쉬우므로, 이 관찰 단계를 건너뛰지 않는 것이 중요합니다.

## 기법 1: 구독 범위 좁히기

가장 먼저 확인할 것은 컴포넌트가 **필요한 것보다 넓은 범위**를 구독하고 있지 않은가입니다.

```jsx
// 나쁜 예: cart 전체를 구독 — cart의 어떤 필드가 바뀌어도 리렌더됨
function CartBadgeBad() {
  const cart = useSelector((state) => state.cart);
  return <span>{cart.items.length}</span>;
}

// 개선: 실제로 쓰는 값(개수)만 구독
function CartBadgeGood() {
  const itemCount = useSelector((state) => state.cart.items.length);
  return <span>{itemCount}</span>;
}
```

`CartBadgeBad`는 `cart.total`이나 `cart.discountCode`처럼 화면에 표시하지 않는 필드가 바뀌어도 리렌더됩니다. `CartBadgeGood`은 `items.length`라는 숫자(원시값)만 구독하므로, 그 값이 실제로 바뀔 때만 리렌더됩니다.

## 기법 2: React.memo로 props가 안 바뀐 컴포넌트를 건너뛴다

부모 컴포넌트가 리렌더되면 기본적으로 모든 자식도 함께 리렌더됩니다. **자식이 받는 props가 바뀌지 않았다면** `React.memo`로 이 리렌더를 건너뛸 수 있습니다.

```jsx
const TodoItem = React.memo(function TodoItem({ text, done, onToggle }) {
  console.log("TodoItem 렌더링:", text);
  return (
    <li onClick={onToggle} style={{ textDecoration: done ? "line-through" : "none" }}>
      {text}
    </li>
  );
});
```

`React.memo`는 이전 props와 새 props를 얕은 비교로 확인해, 같으면 리렌더를 건너뜁니다. 하지만 함정이 있습니다. 부모가 `onToggle` 같은 콜백을 **매 렌더링마다 새로 만든 함수**로 전달하면, 함수의 참조가 매번 달라지므로 `React.memo`가 무력화됩니다.

```jsx
// 나쁜 예: 부모가 렌더링될 때마다 새 함수를 만들어 전달
function TodoListBad({ todos }) {
  return (
    <ul>
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          text={todo.text}
          done={todo.done}
          onToggle={() => dispatch({ type: "todos/toggled", payload: { id: todo.id } })} // 매번 새 함수!
        />
      ))}
    </ul>
  );
}
```

이 문제는 `useCallback`으로 함수 자체를 메모이제이션하거나, 항목별 id를 클릭 핸들러 안에서 클로저로 캡처하지 않고 이벤트 위임으로 처리하는 방식으로 해결합니다.

```jsx
// 개선: useCallback으로 핸들러의 참조를 안정시킨다
function TodoList({ todos }) {
  const dispatch = useDispatch();

  const handleToggle = useCallback(
    (id) => dispatch({ type: "todos/toggled", payload: { id } }),
    [dispatch] // dispatch는 Redux Store가 존재하는 한 항상 안정적인 참조다
  );

  return (
    <ul>
      {todos.map((todo) => (
        <TodoItem key={todo.id} text={todo.text} done={todo.done} onToggle={() => handleToggle(todo.id)} />
      ))}
    </ul>
  );
}
```

주의할 점은 `onToggle={() => handleToggle(todo.id)}`도 여전히 매 렌더링마다 새 화살표 함수를 만든다는 것입니다. 완전히 최적화하려면 `id`를 `TodoItem`에 prop으로 넘기고 `TodoItem` 내부에서 `onToggle(id)`를 호출하는 형태로 바꿔야 합니다. 이런 세부 조정은 "측정해서 실제로 병목일 때만" 적용하는 편이 좋습니다.

## 기법 3: 리스트는 항목 단위 컴포넌트로 분리한다

리스트를 렌더링할 때, 각 항목을 별도 컴포넌트로 분리하지 않으면 **목록의 상태 하나만 바뀌어도 전체 목록이 다시 그려집니다.**

```jsx
// 나쁜 예: 목록 전체를 하나의 컴포넌트 안에서 map으로 렌더링
function TodoListInline() {
  const todos = useSelector((state) => state.todos); // 배열 전체를 구독
  const dispatch = useDispatch();

  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id} onClick={() => dispatch({ type: "todos/toggled", payload: { id: todo.id } })}>
          {todo.text}
        </li>
      ))}
    </ul>
  );
}
```

`todos` 배열에서 항목 하나의 `done`만 바뀌어도(08편에서 본 것처럼 `map()`이 새 배열을 반환하므로) `todos` 배열 참조 전체가 바뀌고, 이 컴포넌트 전체가 리렌더되며 **모든** `<li>`가 다시 그려집니다. 항목을 별도 컴포넌트로 분리하고, 각 컴포넌트가 **자신의 id로 필요한 값만** 구독하게 하면 이 문제가 해결됩니다.

```jsx
function TodoListSeparated() {
  const todoIds = useSelector((state) => state.todos.map((t) => t.id)); // id 배열만 구독
  return (
    <ul>
      {todoIds.map((id) => (
        <TodoItemById key={id} id={id} />
      ))}
    </ul>
  );
}

function TodoItemById({ id }) {
  // 이 항목의 text/done만 구독 — 다른 항목이 바뀌어도 이 컴포넌트는 리렌더되지 않는다
  const todo = useSelector((state) => state.todos.find((t) => t.id === id));
  const dispatch = useDispatch();
  return (
    <li onClick={() => dispatch({ type: "todos/toggled", payload: { id } })}>
      {todo.text}
    </li>
  );
}
```

이 패턴이 14편(Selector 패턴)의 메모이제이션된 selector와 결합되면, 대규모 목록에서도 변경된 항목만 정확히 리렌더되는 구조를 만들 수 있습니다.

## 최적화의 순서: 측정 → 진단 → 적용

성능 최적화는 다음 순서를 지키는 것이 중요합니다.

1. **측정**: Profiler로 실제로 리렌더가 과도한 컴포넌트를 찾는다.
2. **진단**: 구독 범위가 너무 넓은지, props 참조가 매번 바뀌는지, 리스트가 통째로 렌더링되는지 원인을 특정한다.
3. **적용**: 원인에 맞는 기법(구독 좁히기, `React.memo`+`useCallback`, 항목 분리)만 적용한다.

모든 컴포넌트에 `React.memo`를 습관적으로 붙이는 것은 오히려 비교 비용만 늘릴 수 있습니다. 측정 없이 최적화부터 하지 않는 것이 원칙입니다.

## 실무 체크리스트

- `useSelector`가 실제로 화면에 쓰는 값보다 넓은 범위(전체 슬라이스)를 구독하고 있지 않은가?
- `React.memo`로 감싼 컴포넌트에 콜백을 전달할 때 `useCallback`으로 참조를 안정시켰는가?
- 배열을 렌더링할 때 항목 하나의 변경이 전체 목록의 리렌더로 이어지고 있지 않은가?
- 최적화를 적용하기 전에 Profiler로 실제 병목을 확인했는가?

## 연습 과제

### 기초(★☆☆)
- `CartBadgeBad`를 React DevTools Profiler로 관찰해, `cart.total`만 바뀌어도 리렌더되는지 확인해보세요.

### 중급(★★☆)
- `TodoListInline`을 `TodoListSeparated` 구조로 리팩터링하고, 항목 하나를 토글했을 때 다른 항목들이 리렌더되지 않는지 Profiler로 확인해보세요.

### 고급(★★★)
- 100개 이상의 항목을 가진 목록에서 항목 분리 전/후의 리렌더 횟수와 소요 시간을 Profiler로 비교하는 실험을 설계해보세요.

## 요약

- 최적화는 측정으로 시작한다. React DevTools Profiler로 실제 병목을 먼저 찾는다.
- `useSelector`의 구독 범위를 필요한 만큼만 좁히면 대부분의 불필요한 리렌더가 사라진다.
- `React.memo`는 `useCallback`과 함께 써야 효과가 있고, 리스트는 항목 단위 컴포넌트로 분리해야 변경이 국소화된다.

## 참고 문헌 및 출처(추천)

- React 공식 문서, "React.memo" API 레퍼런스
- React 공식 문서, "useCallback" API 레퍼런스
- Redux 공식 문서, "Using Redux with React, Performance"

---

## 다음 글

- 다음: [14. 데이터 선택자 - Selector 패턴](../selector-patterns/)
