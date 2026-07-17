---
title: "[Redux] 15. 실습: Counter와 Todo 앱 만들기"
description: "06~14편에서 배운 Action·Reducer·Store·useSelector·useDispatch·createSelector를 하나로 엮어 Counter와 Todo 앱을 처음부터 끝까지 만듭니다. Phase 3을 마치는 종합 실습입니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 15
draft: false
slug: practice-counter-todo
image: "wordcloud.png"
tags:
  - Redux
  - React
  - JavaScript
  - Frontend(프론트엔드)
  - Web(웹)
  - State
  - Case-Study
  - 실습
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Intermediate
  - Implementation(구현)
  - Deep-Dive
  - 종합실습
  - counter앱
  - todo앱
  - 컴포넌트조립
  - 액션크리에이터
  - 슬라이스구조
  - 프로젝트폴더구조
---

# 15. 실습: Counter와 Todo 앱 만들기

Phase 3의 마지막 편입니다. 06~14편에서 각각 배운 개념(Action·Reducer·Store, Provider, useSelector/useDispatch, 리렌더 최적화, Selector 패턴)을 한 번에 조립해 Counter 앱과 Todo 앱을 완성합니다. 이 두 앱은 작지만, 실무 Redux 프로젝트의 기본 골격을 그대로 담고 있습니다.

## 학습 목표

- 1~14편의 개념을 조합해 순수 Redux(Toolkit 없이)로 동작하는 앱을 완성할 수 있다.
- 기능별로 리듀서와 selector를 나누는 프로젝트 폴더 구조를 적용할 수 있다.
- 완성된 앱에서 각 코드 조각이 어느 편의 개념과 대응하는지 스스로 설명할 수 있다.

## 프로젝트 구조

```
src/
  store.js              # createStore + combineReducers (07·09편)
  features/
    counter/
      counterSlice.js   # counter 리듀서 + 액션 생성자 (07편)
      counterSelectors.js # counter 관련 selector (14편)
      Counter.jsx        # UI 컴포넌트 (11·12편)
    todos/
      todosSlice.js
      todosSelectors.js
      TodoList.jsx
  App.jsx                # Provider로 감싼 루트 컴포넌트 (11편)
```

폴더를 **기능(feature) 단위**로 나누는 이 구조는 26편(프로젝트 구조)에서 "확장 가능한 Redux 구조"로 더 깊이 다룹니다.

## Counter 리듀서와 액션 생성자

```javascript
// features/counter/counterSlice.js
const initialState = { count: 0 };

// 액션 생성자 (07편)
export const incremented = () => ({ type: "counter/incremented" });
export const decremented = () => ({ type: "counter/decremented" });
export const incrementedBy = (amount) => ({ type: "counter/incrementedBy", payload: amount });

// 순수 리듀서 (07·08편): 매개변수 변경 없이 항상 새 객체 반환
export function counterReducer(state = initialState, action) {
  switch (action.type) {
    case "counter/incremented":
      return { count: state.count + 1 };
    case "counter/decremented":
      return { count: state.count - 1 };
    case "counter/incrementedBy":
      return { count: state.count + action.payload };
    default:
      return state;
  }
}
```

리듀서와 별도로, 이 상태에 접근하는 방법도 selector로 분리해둡니다. 컴포넌트는 `state.counter.count`라는 경로를 직접 알 필요 없이 이 함수 하나만 가져다 씁니다.

```javascript
// features/counter/counterSelectors.js
export const selectCount = (state) => state.counter.count; // 14편: 이름 있는 selector로 분리
```

## Todo 리듀서와 액션 생성자

```javascript
// features/todos/todosSlice.js
const initialState = [];

export const todoAdded = (text) => ({ type: "todos/added", payload: { id: Date.now(), text } });
export const todoToggled = (id) => ({ type: "todos/toggled", payload: { id } });
export const todoRemoved = (id) => ({ type: "todos/removed", payload: { id } });

export function todosReducer(state = initialState, action) {
  switch (action.type) {
    case "todos/added":
      return [...state, { id: action.payload.id, text: action.payload.text, done: false }]; // 03·08편: 불변 추가
    case "todos/toggled":
      return state.map((todo) =>
        todo.id === action.payload.id ? { ...todo, done: !todo.done } : todo
      ); // 08편: map으로 불변 업데이트
    case "todos/removed":
      return state.filter((todo) => todo.id !== action.payload.id); // 03편: filter로 불변 삭제
    default:
      return state;
  }
}
```

todos는 완료 개수처럼 계산이 필요한 파생 데이터를 자주 필요로 하므로, 이 selector 파일에서 14편의 `createSelector`를 바로 사용합니다.

```javascript
// features/todos/todosSelectors.js
import { createSelector } from "reselect";

export const selectAllTodos = (state) => state.todos;

// 14편: 계산 비용이 있는 파생 데이터는 createSelector로 메모이제이션
export const selectCompletedCount = createSelector(
  [selectAllTodos],
  (todos) => todos.filter((todo) => todo.done).length
);
```

## Store 조립

```javascript
// store.js
import { createStore, combineReducers } from "redux";
import { counterReducer } from "./features/counter/counterSlice";
import { todosReducer } from "./features/todos/todosSlice";

const rootReducer = combineReducers({
  counter: counterReducer, // 07편: 여러 리듀서를 하나의 상태 트리로 합침
  todos: todosReducer,
});

export const store = createStore(rootReducer);
```

## UI 컴포넌트

가장 단순한 `Counter`부터 조립합니다. 12편에서 배운 대로 `useSelector`가 원시값(`count`)을 구독하므로, 이 컴포넌트는 다른 상태가 바뀌어도 불필요하게 리렌더되지 않습니다.

```jsx
// features/counter/Counter.jsx
import { useSelector, useDispatch } from "react-redux";
import { selectCount } from "./counterSelectors";
import { incremented, decremented } from "./counterSlice";

export function Counter() {
  const count = useSelector(selectCount); // 12편: 원시값을 구독해 정확한 리렌더 판정
  const dispatch = useDispatch();

  return (
    <div>
      <button onClick={() => dispatch(decremented())}>-1</button>
      <span>{count}</span>
      <button onClick={() => dispatch(incremented())}>+1</button>
    </div>
  );
}
```

`TodoList`는 `Counter`보다 복잡합니다. 13편의 항목 분리 패턴(`TodoItem`을 별도 컴포넌트로 두기)과 `useCallback`으로 핸들러 참조를 안정시키는 기법을 함께 적용합니다.

```jsx
// features/todos/TodoList.jsx
import { useState, useCallback } from "react";
import { useSelector, useDispatch } from "react-redux";
import { selectAllTodos, selectCompletedCount } from "./todosSelectors";
import { todoAdded, todoToggled, todoRemoved } from "./todosSlice";

function TodoItem({ id, text, done, onToggle, onRemove }) {
  return (
    <li style={{ textDecoration: done ? "line-through" : "none" }}>
      <span onClick={() => onToggle(id)}>{text}</span>
      <button onClick={() => onRemove(id)}>삭제</button>
    </li>
  ); // 13편: 항목 단위 컴포넌트로 분리해 개별 리렌더만 발생하게 함
}

export function TodoList() {
  const [input, setInput] = useState("");
  const todos = useSelector(selectAllTodos);
  const completedCount = useSelector(selectCompletedCount); // 14편: 메모이제이션된 파생 데이터
  const dispatch = useDispatch();

  const handleToggle = useCallback((id) => dispatch(todoToggled(id)), [dispatch]); // 13편
  const handleRemove = useCallback((id) => dispatch(todoRemoved(id)), [dispatch]);

  const handleAdd = () => {
    if (input.trim() === "") return;
    dispatch(todoAdded(input));
    setInput("");
  };

  return (
    <div>
      <p>완료: {completedCount} / {todos.length}</p>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={handleAdd}>추가</button>
      <ul>
        {todos.map((todo) => (
          <TodoItem key={todo.id} {...todo} onToggle={handleToggle} onRemove={handleRemove} />
        ))}
      </ul>
    </div>
  );
}
```

마지막으로 이 두 컴포넌트를 하나의 앱으로 묶습니다. 11편에서 배운 `Provider`가 `store`를 트리 전체에 주입해야, `Counter`와 `TodoList` 어디에서든 `useSelector`/`useDispatch`를 쓸 수 있습니다.

```jsx
// App.jsx
import { Provider } from "react-redux";
import { store } from "./store";
import { Counter } from "./features/counter/Counter";
import { TodoList } from "./features/todos/TodoList";

export default function App() {
  return (
    <Provider store={store}> {/* 11편: Store를 트리 전체에 주입 */}
      <Counter />
      <TodoList />
    </Provider>
  );
}
```

## 코드와 편 번호 대응표

| 코드 요소 | 대응하는 편 |
|---|---|
| `combineReducers({ counter, todos })` | 07편(Action, Reducer, Store) |
| `{ ...todo, done: !todo.done }` | 08편(불변성) |
| `dispatch(action)` 이후 상태 갱신 순서 | 09편(데이터 흐름) |
| `<Provider store={store}>` | 11편(Provider와 connect) |
| `useSelector`, `useDispatch` | 12편(React-Redux Hooks) |
| `TodoItem`을 별도 컴포넌트로 분리 | 13편(컴포넌트 최적화) |
| `createSelector(selectAllTodos, ...)` | 14편(Selector 패턴) |

## 실무 체크리스트

- 각 기능(counter, todos)의 리듀서·액션 생성자·selector가 같은 폴더에 응집돼 있는가?
- 리듀서가 여전히 순수 함수 규칙(매개변수 미변경, 부수 효과 없음)을 지키고 있는가?
- 계산 비용이 있는 selector(`selectCompletedCount`)에 메모이제이션을 적용했는가?

## 연습 과제

### 기초(★☆☆)
- Todo 항목에 "우선순위"(`high`/`normal`/`low`) 필드를 추가하고, 이를 반영하는 액션과 리듀서 케이스를 작성해보세요.

### 중급(★★☆)
- `selectAllTodos`를 기반으로, 우선순위가 `high`인 항목만 걸러내는 메모이제이션 selector를 추가해보세요.

### 고급(★★★)
- Counter와 Todo 상태를 조합해, "Todo 완료 개수가 Counter 값 이상이면 축하 메시지를 보여주는" 파생 selector를 `createSelector`의 다중 입력으로 구현해보세요.

## 요약

- 순수 Redux만으로도 기능 단위 폴더 구조, 불변 리듀서, 최적화된 UI 연동을 갖춘 완결된 앱을 만들 수 있다.
- 1~14편의 개념은 서로 독립된 지식이 아니라, 하나의 앱 안에서 유기적으로 맞물려 동작한다.
- 다음 Phase부터는 이 순수 Redux 코드를 Redux Toolkit으로 다시 작성해, 얼마나 짧아지는지 직접 비교하게 된다.

## 참고 문헌 및 출처(추천)

- Redux 공식 문서, "Redux Essentials, Part 1: Redux Overview and Concepts"
- Redux 공식 문서, "Structuring Reducers" — 기능 단위 폴더 구조 권장 사항
- React 공식 문서, "Thinking in React" — 컴포넌트 분리 설계 원칙

---

## 다음 글

- 다음: [16. Redux Toolkit 소개 - 왜 RTK인가?](../redux-toolkit-introduction/)
