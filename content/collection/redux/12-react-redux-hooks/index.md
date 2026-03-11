---
draft: true
title: "[Redux] 12. React-Redux Hooks - useSelector와 useDispatch"
date: 2025-10-14
lastmod: 2025-10-14
description: "현대적인 React-Redux Hooks 완벽 마스터. useSelector로 간결한 상태 조회, useDispatch로 액션 발송, 성능 최적화까지 connect HOC를 대체하는 Hooks API를 실전 예제로 학습합니다."
slug: react-redux-hooks
tags:
  - JavaScript
  - TypeScript
  - React
  - Frontend
  - 프론트엔드
  - Web
  - 웹
  - Performance
  - 성능
  - Optimization
  - 최적화
  - Memoization
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - State
  - Observer
  - Event-Driven
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Refactoring
  - 리팩토링
  - Testing
  - 테스트
  - Debugging
  - 디버깅
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - Reference
  - 참고
  - Documentation
  - 문서화
  - Error-Handling
  - 에러처리
  - Pitfalls
  - 함정
  - Edge-Cases
  - 엣지케이스
  - Type-Safety
  - Interface
  - 인터페이스
  - Encapsulation
  - 캡슐화
  - Data-Structures
  - 자료구조
  - API
  - Async
  - 비동기
  - Caching
  - 캐싱
  - Scalability
  - 확장성
  - Git
  - IDE
  - How-To
  - Tips
  - Technology
  - 기술
  - Education
  - 교육
  - 실습
  - Case-Study
  - Comparison
  - 비교
  - Deep-Dive
  - Beginner
  - Advanced
  - Maintainability
  - Modularity
  - Readability
  - Workflow
  - 워크플로우
  - JSON
  - HTTP
  - Functional-Programming
  - 함수형프로그래밍
  - Benchmark
  - Profiling
  - 프로파일링
series: ["Redux 완전 정복"]
series_order: 12
---

11장에서 Provider와 connect로 React와 Redux를 연결했다면, 이 장에서는 **React-Redux Hooks(useSelector, useDispatch)**로 같은 동작을 더 짧고 읽기 쉽게 만드는 방법을 다룹니다. 함수형 컴포넌트에서 HOC 없이 state와 dispatch에 접근할 수 있어 현대적인 Redux 코드의 표준이 되었습니다. 이 장을 마치면 13(컴포넌트 최적화)·14(Selector 패턴)에서 성능과 선택자 패턴을 이어서 배울 수 있습니다.

## 이 글을 읽은 후 달성해야 할 목표 (평가 기준)

이 챕터를 마치면 다음을 할 수 있어야 합니다:

- **useSelector**로 Redux **State**를 읽고, **useDispatch**로 **Action**을 발송할 수 있다.
- **connect** HOC 기반 컴포넌트를 Hooks 기반으로 전환할 수 있다.
- Custom Hooks로 로직을 재사용하고, 선택적 구독 등 성능 최적화를 적용할 수 있다.

## 왜 Hooks를 사용하는가?

React 16.8에서 **Hooks**가 도입된 이후, 함수형 컴포넌트에서도 **상태**와 부가 로직을 재사용할 수 있게 되었습니다. 클래스를 쓰지 않고도 `useState`, `useEffect` 등으로 동일한 관심사를 한 곳에 모을 수 있어, 컴포넌트 구조가 단순해졌습니다.

React-Redux에서도 예전에는 **connect** HOC(고차 컴포넌트)로 **Store**와 컴포넌트를 연결했습니다. **connect**는 `mapStateToProps`, `mapDispatchToProps`로 데이터와 액션을 주입하지만, 래핑이 늘어나면 컴포넌트 계층이 깊어지고, TypeScript에서 타입 추론이 번거로우며, 테스트 시 Store를 모킹해야 하는 부담이 있습니다.

그래서 React-Redux는 **useSelector**, **useDispatch** 같은 Hooks API를 제공합니다. 컴포넌트 안에서 직접 **Store**의 일부를 구독하고 **Action**을 발송할 수 있어, 보일러플레이트가 줄고 타입 추론과 테스트가 수월해집니다. 아래는 **connect**와 Hooks 방식의 비교입니다.

```javascript
// ❌ connect HOC - 복잡함
function Counter({ count, increment, decrement }) {
    return <div>...</div>;
}

const mapStateToProps = state => ({ count: state.count });
const mapDispatchToProps = { increment, decrement };

export default connect(mapStateToProps, mapDispatchToProps)(Counter);

// ✅ Hooks - 간결함!
import { useSelector, useDispatch } from 'react-redux';

function Counter() {
    const count = useSelector(state => state.count);
    const dispatch = useDispatch();
    
    return (
        <div>
            <h1>{count}</h1>
            <button onClick={() => dispatch(increment())}>+</button>
            <button onClick={() => dispatch(decrement())}>-</button>
        </div>
    );
}
```

**Hooks의 장점**:
- 더 적은 보일러플레이트
- 타입스크립트와 잘 맞음
- 컴포넌트 구조가 단순
- 테스트가 쉬움

## useSelector - State 읽기

**useSelector**는 **Store**에서 원하는 **상태** 일부를 선택하는 **선택자(selector)** 함수를 인자로 받습니다. React-Redux는 이 선택 결과를 **참조 비교**로 이전 값과 비교하고, 바뀌었을 때만 해당 컴포넌트를 리렌더합니다. 따라서 선택 범위를 좁히면 불필요한 리렌더를 줄일 수 있습니다. 기본 사용법은 다음과 같습니다.

### 기본 사용법

```javascript
import { useSelector } from 'react-redux';

function TodoList() {
    // State에서 todos 가져오기
    const todos = useSelector(state => state.todos);
    
    return (
        <ul>
            {todos.map(todo => (
                <li key={todo.id}>{todo.text}</li>
            ))}
        </ul>
    );
}
```

여러 값을 한 번에 가져와야 할 때는 **useSelector**를 여러 번 호출하거나, 하나의 선택자에서 객체를 반환할 수 있습니다. 객체를 반환하면 매 렌더마다 새 객체가 만들어지므로, 참조가 바뀌어 리렌더가 자주 일어날 수 있습니다. 이때는 두 번째 인자로 **동등 비교 함수**(예: `shallowEqual`)를 넘기는 것이 좋습니다.

### 여러 값 선택하기

```javascript
function Dashboard() {
    // 방법 1: 각각 선택
    const user = useSelector(state => state.user);
    const todos = useSelector(state => state.todos);
    const loading = useSelector(state => state.loading);
    
    // 방법 2: 객체로 한 번에 (주의: 성능 이슈!)
    const { user, todos, loading } = useSelector(state => ({
        user: state.user,
        todos: state.todos,
        loading: state.loading
    }));
    
    return <div>...</div>;
}
```

선택 로직을 **Selector 함수**로 분리해 두면 여러 컴포넌트에서 재사용할 수 있고, 14장에서 다루는 **Reselect**로 메모이제이션하기도 쉽습니다. 아래처럼 별도 파일에 두고 import해서 쓰는 패턴을 권장합니다.

### Selector 함수 재사용

```javascript
// selectors.js - Selector 함수 분리
export const selectTodos = state => state.todos;
export const selectUser = state => state.user;
export const selectLoading = state => state.loading;
export const selectCompletedTodos = state =>
    state.todos.filter(todo => todo.completed);

// 컴포넌트에서 사용
import { selectTodos, selectCompletedTodos } from './selectors';

function TodoList() {
    const todos = useSelector(selectTodos);
    const completedTodos = useSelector(selectCompletedTodos);
    
    return <div>...</div>;
}
```

**매개변수**가 있는 선택(예: `todoId`로 특정 Todo 하나만 고르기)은 주의가 필요합니다. **useSelector**에 인라인으로 `state => state.todos.find(t => t.id === todoId)`를 넘기면 매 렌더마다 **새 함수**가 생성되어, React-Redux가 "선택자가 바뀌었다"고 보고 불필요한 구독·비교가 일어날 수 있습니다. **useCallback**으로 선택자 함수를 고정하거나, **Selector Factory** 패턴을 쓰는 것이 좋습니다.

### 매개변수가 있는 Selector

```javascript
// ❌ 이렇게 하면 안 됨 (매번 새 함수 생성)
function TodoItem({ todoId }) {
    const todo = useSelector(state => 
        state.todos.find(t => t.id === todoId)
    );
}

// ✅ 방법 1: useCallback 사용
function TodoItem({ todoId }) {
    const selectTodo = useCallback(
        state => state.todos.find(t => t.id === todoId),
        [todoId]
    );
    
    const todo = useSelector(selectTodo);
}

// ✅ 방법 2: Selector Factory
// selectors.js
export const makeTodoSelector = () => 
    createSelector(
        [state => state.todos, (state, todoId) => todoId],
        (todos, todoId) => todos.find(t => t.id === todoId)
    );

// 컴포넌트
function TodoItem({ todoId }) {
    const selectTodo = useMemo(makeTodoSelector, []);
    const todo = useSelector(state => selectTodo(state, todoId));
}
```

## useDispatch - Action 발송

**useDispatch**는 Redux **Store**의 **dispatch** 함수를 반환합니다. 이 **dispatch**에 **Action** 객체나 **Action Creator**의 반환값을 넘기면 **Reducer**가 실행되고 **상태**가 갱신됩니다. 보통 **Action Creator**를 import해서 `dispatch(increment())` 형태로 사용하며, **useCallback**으로 핸들러를 감싸면 자식에게 넘길 때 불필요한 리렌더를 줄일 수 있습니다.

### 기본 사용법

```javascript
import { useDispatch } from 'react-redux';

function Counter() {
    const dispatch = useDispatch();
    
    const increment = () => {
        dispatch({ type: 'INCREMENT' });
    };
    
    const decrement = () => {
        dispatch({ type: 'DECREMENT' });
    };
    
    return (
        <div>
            <button onClick={increment}>+</button>
            <button onClick={decrement}>-</button>
        </div>
    );
}
```

### Action Creator 사용

```javascript
// actions.js
export const increment = () => ({ type: 'INCREMENT' });
export const decrement = () => ({ type: 'DECREMENT' });
export const incrementBy = (amount) => ({
    type: 'INCREMENT_BY',
    payload: amount
});

// 컴포넌트
import { increment, decrement, incrementBy } from './actions';

function Counter() {
    const dispatch = useDispatch();
    const count = useSelector(state => state.count);
    
    return (
        <div>
            <h1>{count}</h1>
            <button onClick={() => dispatch(increment())}>+1</button>
            <button onClick={() => dispatch(decrement())}>-1</button>
            <button onClick={() => dispatch(incrementBy(5))}>+5</button>
        </div>
    );
}
```

### useCallback으로 최적화

```javascript
function TodoForm() {
    const dispatch = useDispatch();
    const [text, setText] = useState('');
    
    // ✅ useCallback으로 함수 메모이제이션
    const handleSubmit = useCallback((e) => {
        e.preventDefault();
        if (text.trim()) {
            dispatch(addTodo(text));
            setText('');
        }
    }, [text, dispatch]);
    
    return (
        <form onSubmit={handleSubmit}>
            <input 
                value={text} 
                onChange={e => setText(e.target.value)} 
            />
            <button type="submit">Add</button>
        </form>
    );
}
```

## useStore - Store 직접 접근

**useStore**는 **Store** 인스턴스 자체에 접근할 때 쓰는 Hook입니다. 일반적인 **상태** 읽기와 **Action** 발송은 **useSelector**와 **useDispatch**로 충분하므로, **useStore**는 디버깅용으로 현재 **상태**를 로그하거나, **subscribe**를 직접 붙여야 하는 특수한 경우에만 사용하는 것이 좋습니다. 대부분의 컴포넌트에서는 **useStore**를 쓰지 않습니다.

### useStore Hook

```javascript
import { useStore } from 'react-redux';

function DebugPanel() {
    const store = useStore();
    
    const handleLogState = () => {
        console.log('Current State:', store.getState());
    };
    
    const handleSubscribe = () => {
        const unsubscribe = store.subscribe(() => {
            console.log('State changed:', store.getState());
        });
        
        // Cleanup
        return unsubscribe;
    };
    
    return (
        <div>
            <button onClick={handleLogState}>Log State</button>
            <button onClick={handleSubscribe}>Subscribe</button>
        </div>
    );
}
```

**주의**: **useStore**는 거의 사용하지 않습니다. **useSelector**와 **useDispatch**로 대부분의 요구를 충족할 수 있고, **Store**를 직접 다루면 컴포넌트가 Redux에 과도하게 묶이므로, 디버깅·구독 테스트 등 꼭 필요한 경우에만 쓰는 것이 좋습니다.

## 성능 최적화

**useSelector**는 선택 결과를 **이전 값과 참조 비교**합니다. 선택자에서 매번 **새 객체·배열**을 반환하면 참조가 달라져 컴포넌트가 매 렌더마다 리렌더됩니다. 여러 필드를 한 번에 가져오거나, 파생 데이터를 선택할 때는 **동등 비교 함수(equality function)**를 두 번째 인자로 넘기거나, **Reselect**로 메모이제이션된 선택자를 쓰면 불필요한 리렌더를 줄일 수 있습니다.

### Equality Function (동등 비교 함수)

```javascript
import { shallowEqual } from 'react-redux';

function UserProfile() {
    // ❌ 매번 새 객체 생성 → 항상 리렌더링
    const user = useSelector(state => ({
        name: state.user.name,
        email: state.user.email
    }));
    
    // ✅ shallowEqual로 비교
    const user = useSelector(
        state => ({
            name: state.user.name,
            email: state.user.email
        }),
        shallowEqual
    );
    
    return <div>{user.name} - {user.email}</div>;
}
```

**shallowEqual**은 객체의 1단계 키만 비교합니다. 중첩 객체나 배열 내용까지 비교하려면 **lodash**의 `isEqual` 같은 **깊은 비교**를 쓰거나, 비교할 필드만 골라서 **커스텀 equality 함수**를 만들어 넘길 수 있습니다. 다만 깊은 비교는 비용이 크므로, 필요한 경우에만 사용하는 것이 좋습니다.

### 커스텀 Equality Function

```javascript
// 깊은 비교 (lodash 사용)
import { isEqual } from 'lodash';

const todos = useSelector(
    state => state.todos,
    isEqual
);

// 특정 필드만 비교
const customEqual = (prev, next) => {
    return prev.id === next.id && prev.name === next.name;
};

const user = useSelector(state => state.user, customEqual);
```

**Reselect**의 **createSelector**는 입력 선택자 결과가 바뀌지 않으면 이전 계산 결과를 그대로 반환합니다. **filter**나 **map**처럼 **파생 데이터**를 만드는 선택자가 무거울 때, **todos**나 **filter**가 바뀔 때만 다시 계산되도록 하면 성능이 좋아집니다. 아래는 **visibleTodos**를 메모이제이션하는 예입니다.

### Reselect로 메모이제이션

```javascript
import { createSelector } from 'reselect';

// Memoized Selector
const selectTodos = state => state.todos;
const selectFilter = state => state.filter;

const selectVisibleTodos = createSelector(
    [selectTodos, selectFilter],
    (todos, filter) => {
        console.log('Computing visible todos...');
        switch (filter) {
            case 'completed':
                return todos.filter(t => t.completed);
            case 'active':
                return todos.filter(t => !t.completed);
            default:
                return todos;
        }
    }
);

// 컴포넌트
function TodoList() {
    // todos나 filter가 변경될 때만 재계산
    const visibleTodos = useSelector(selectVisibleTodos);
    
    return (
        <ul>
            {visibleTodos.map(todo => (
                <TodoItem key={todo.id} todo={todo} />
            ))}
        </ul>
    );
}
```

## Custom Hooks - 로직 재사용

### useTodos Hook

```javascript
// hooks/useTodos.js
export function useTodos() {
    const dispatch = useDispatch();
    const todos = useSelector(state => state.todos);
    const filter = useSelector(state => state.filter);
    
    const addTodo = useCallback((text) => {
        dispatch({ type: 'ADD_TODO', payload: { text } });
    }, [dispatch]);
    
    const toggleTodo = useCallback((id) => {
        dispatch({ type: 'TOGGLE_TODO', payload: id });
    }, [dispatch]);
    
    const removeTodo = useCallback((id) => {
        dispatch({ type: 'REMOVE_TODO', payload: id });
    }, [dispatch]);
    
    const setFilter = useCallback((newFilter) => {
        dispatch({ type: 'SET_FILTER', payload: newFilter });
    }, [dispatch]);
    
    const visibleTodos = useMemo(() => {
        switch (filter) {
            case 'completed':
                return todos.filter(t => t.completed);
            case 'active':
                return todos.filter(t => !t.completed);
            default:
                return todos;
        }
    }, [todos, filter]);
    
    return {
        todos: visibleTodos,
        filter,
        addTodo,
        toggleTodo,
        removeTodo,
        setFilter
    };
}

// 컴포넌트에서 사용
function TodoApp() {
    const { 
        todos, 
        filter, 
        addTodo, 
        toggleTodo, 
        removeTodo, 
        setFilter 
    } = useTodos();
    
    return <div>...</div>;
}
```

이렇게 **도메인 로직**(todos 조회·추가·필터 등)을 Custom Hook으로 묶으면, 여러 컴포넌트에서 같은 로직을 재사용할 수 있고, Hook 단위로 테스트하기도 쉬워집니다. **useActions**처럼 **Action Creator** 묶음을 **dispatch**와 바인딩해 주는 Hook도 자주 쓰입니다.

### useActions Hook

```javascript
// hooks/useActions.js
import { useDispatch } from 'react-redux';
import { useMemo } from 'react';
import { bindActionCreators } from 'redux';

export function useActions(actions) {
    const dispatch = useDispatch();
    
    return useMemo(
        () => bindActionCreators(actions, dispatch),
        [actions, dispatch]
    );
}

// 사용
import * as todoActions from '../actions/todoActions';

function TodoList() {
    const actions = useActions(todoActions);
    
    // actions.addTodo, actions.toggleTodo 등 사용 가능
    return (
        <button onClick={() => actions.addTodo('New Todo')}>
            Add
        </button>
    );
}
```

### useSelector + TypeScript

```typescript
// types.ts
export interface RootState {
    counter: { count: number };
    todos: Todo[];
    user: User | null;
}

// hooks/useTypedSelector.ts
import { TypedUseSelectorHook, useSelector } from 'react-redux';
import { RootState } from '../types';

export const useTypedSelector: TypedUseSelectorHook<RootState> = useSelector;

// 컴포넌트에서 사용
import { useTypedSelector } from './hooks/useTypedSelector';

function Counter() {
    // count의 타입이 자동으로 number로 추론됨
    const count = useTypedSelector(state => state.counter.count);
    
    return <div>{count}</div>;
}
```

## connect HOC를 Hooks로 전환

### Before: connect

```javascript
function TodoList({ todos, addTodo, toggleTodo, removeTodo }) {
    return <div>...</div>;
}

const mapStateToProps = state => ({
    todos: state.todos
});

const mapDispatchToProps = {
    addTodo,
    toggleTodo,
    removeTodo
};

export default connect(mapStateToProps, mapDispatchToProps)(TodoList);
```

### After: Hooks

```javascript
import { useSelector, useDispatch } from 'react-redux';
import { addTodo, toggleTodo, removeTodo } from './actions';

function TodoList() {
    const todos = useSelector(state => state.todos);
    const dispatch = useDispatch();
    
    const handleAdd = (text) => dispatch(addTodo(text));
    const handleToggle = (id) => dispatch(toggleTodo(id));
    const handleRemove = (id) => dispatch(removeTodo(id));
    
    return <div>...</div>;
}

export default TodoList;
```

**connect**에서 Hooks로 옮길 때는 **구독 범위**를 그대로 유지하는지 확인하는 것이 좋습니다. **mapStateToProps**에서 골라 주던 필드만 **useSelector**로 같은 조건으로 선택하면, 불필요한 리렌더가 늘어나지 않습니다. TypeScript를 쓰면 **useTypedSelector**처럼 타입이 붙은 Hook을 두어 **RootState** 기준으로 선택하게 하면 편합니다.

## Hooks vs connect: 비교와 판단 기준

### 한눈에 보기

| 구분 | connect (mapStateToProps / mapDispatchToProps) | Hooks (useSelector / useDispatch) |
|------|-----------------------------------------------|-----------------------------------|
| **상태 읽기** | mapStateToProps에서 반환한 객체가 props로 주입됨. 여러 필드를 한 객체로 넘기기 쉬움. | useSelector로 선택자마다 한 값. 여러 값은 여러 번 호출하거나, 객체 반환 시 shallowEqual 권장. |
| **Action 발송** | mapDispatchToProps로 바인딩된 함수가 props로 주입됨. | useDispatch()로 dispatch를 받아 Action Creator 호출. useCallback으로 핸들러 고정 권장. |
| **타입 추론** | 제네릭으로 연결 시 타입 지정 필요. | TypedUseSelectorHook 등으로 RootState 기반 추론 가능. |
| **테스트** | Store/Provider 래핑 또는 mock store 필요. | Hook이므로 render 시 Provider만 주면 됨. |
| **적합한 경우** | 기존 클래스 컴포넌트, 이미 connect로 잘 동작하는 레거시. | 신규 함수형 컴포넌트, 타입 안전성·간결함을 중시할 때. |

### 판단 기준

- **신규 컴포넌트**: **useSelector**·**useDispatch** 기반 Hooks 사용을 권장합니다. 보일러플레이트가 적고 TypeScript와 잘 맞습니다.
- **레거시 connect 컴포넌트**: 한 번에 모두 바꿀 필요는 없습니다. 수정이 잦은 컴포넌트부터 Hooks로 전환하고, **구독 범위**를 동일하게 유지하면 됩니다.
- **클래스 컴포넌트**: Hooks는 함수형 컴포넌트에서만 쓸 수 있으므로, 클래스 컴포넌트는 당분간 **connect**를 유지하는 것이 맞습니다. 점진적으로 함수형으로 바꿀 때 Hooks로 전환하면 됩니다.

### 한계와 비판적 시각

**useSelector**는 선택 결과의 **참조**만 비교합니다. 선택자를 너무 넓게 쓰거나, 매번 새 객체를 반환하면 **구독 단위**가 굵어져 불필요한 리렌더가 늘어날 수 있습니다. **connect**의 **mapStateToProps**는 여러 필드를 한 객체로 넘기더라도, React-Redux가 얕은 비교로 필드별로 바뀐 것만 감지해 주는 동작이 있어, 예전 코드와 동작이 다를 수 있습니다. 따라서 Hooks로 전환할 때는 **shallowEqual**·**Reselect**로 선택 범위와 파생 데이터를 세밀히 나누는 것이 중요합니다. "Hooks가 무조건 더 낫다"기보다, **팀·레거시·성능 요구**에 맞게 **connect**와 Hooks를 선택하는 것이 좋습니다.

## 실전 예제: Todo 앱

아래는 **useSelector**, **useDispatch**, 필터링·통계 선택자를 한 컴포넌트에 모은 예시입니다. 실제 프로젝트에서는 **visibleTodos**나 **stats** 같은 파생 데이터는 14장의 **Selector** 패턴으로 분리하고, Custom Hook으로 빼면 읽기와 유지보수가 더 수월합니다.

### 완전한 Todo 컴포넌트

```javascript
import React, { useState, useCallback } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { addTodo, toggleTodo, removeTodo, setFilter } from './actions';

function TodoApp() {
    const dispatch = useDispatch();
    const [text, setText] = useState('');
    
    // State 선택
    const todos = useSelector(state => state.todos);
    const filter = useSelector(state => state.filter);
    
    // 필터링된 todos
    const visibleTodos = useSelector(state => {
        const { todos, filter } = state;
        switch (filter) {
            case 'completed':
                return todos.filter(t => t.completed);
            case 'active':
                return todos.filter(t => !t.completed);
            default:
                return todos;
        }
    });
    
    // 통계
    const stats = useSelector(state => {
        const total = state.todos.length;
        const completed = state.todos.filter(t => t.completed).length;
        const active = total - completed;
        return { total, completed, active };
    });
    
    // Action Handlers
    const handleSubmit = useCallback((e) => {
        e.preventDefault();
        if (text.trim()) {
            dispatch(addTodo(text));
            setText('');
        }
    }, [text, dispatch]);
    
    const handleToggle = useCallback((id) => {
        dispatch(toggleTodo(id));
    }, [dispatch]);
    
    const handleRemove = useCallback((id) => {
        dispatch(removeTodo(id));
    }, [dispatch]);
    
    const handleFilterChange = useCallback((newFilter) => {
        dispatch(setFilter(newFilter));
    }, [dispatch]);
    
    return (
        <div className="todo-app">
            <h1>Todo App</h1>
            
            {/* Stats */}
            <div className="stats">
                <span>Total: {stats.total}</span>
                <span>Active: {stats.active}</span>
                <span>Completed: {stats.completed}</span>
            </div>
            
            {/* Form */}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="What needs to be done?"
                />
                <button type="submit">Add</button>
            </form>
            
            {/* Filters */}
            <div className="filters">
                <button 
                    onClick={() => handleFilterChange('all')}
                    className={filter === 'all' ? 'active' : ''}
                >
                    All
                </button>
                <button 
                    onClick={() => handleFilterChange('active')}
                    className={filter === 'active' ? 'active' : ''}
                >
                    Active
                </button>
                <button 
                    onClick={() => handleFilterChange('completed')}
                    className={filter === 'completed' ? 'active' : ''}
                >
                    Completed
                </button>
            </div>
            
            {/* Todo List */}
            <ul className="todo-list">
                {visibleTodos.map(todo => (
                    <li key={todo.id} className={todo.completed ? 'completed' : ''}>
                        <input
                            type="checkbox"
                            checked={todo.completed}
                            onChange={() => handleToggle(todo.id)}
                        />
                        <span onClick={() => handleToggle(todo.id)}>
                            {todo.text}
                        </span>
                        <button onClick={() => handleRemove(todo.id)}>×</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default TodoApp;
```

## 실습 문제 🏋️‍♂️

### 문제 1: connect를 Hooks로 변환

```javascript
// Before
function UserProfile({ user, updateUser, logout }) {
    return <div>...</div>;
}

const mapStateToProps = state => ({ user: state.user });
const mapDispatchToProps = { updateUser, logout };
export default connect(mapStateToProps, mapDispatchToProps)(UserProfile);

// TODO: Hooks로 변환

// 답안:
function UserProfile() {
    const user = useSelector(state => state.user);
    const dispatch = useDispatch();
    
    const handleUpdate = (data) => dispatch(updateUser(data));
    const handleLogout = () => dispatch(logout());
    
    return <div>...</div>;
}

export default UserProfile;
```

### 문제 2: Custom Hook 만들기

```javascript
// TODO: useCounter Hook 만들기
// 기능: count 값, increment, decrement, reset 제공

// 답안:
function useCounter() {
    const count = useSelector(state => state.count);
    const dispatch = useDispatch();
    
    const increment = useCallback(() => {
        dispatch({ type: 'INCREMENT' });
    }, [dispatch]);
    
    const decrement = useCallback(() => {
        dispatch({ type: 'DECREMENT' });
    }, [dispatch]);
    
    const reset = useCallback(() => {
        dispatch({ type: 'RESET' });
    }, [dispatch]);
    
    return { count, increment, decrement, reset };
}

// 사용
function Counter() {
    const { count, increment, decrement, reset } = useCounter();
    
    return (
        <div>
            <h1>{count}</h1>
            <button onClick={increment}>+</button>
            <button onClick={decrement}>-</button>
            <button onClick={reset}>Reset</button>
        </div>
    );
}
```

## 흔한 실수 ⚠️

### 실수 1: 객체 Selector에서 shallowEqual 빠뜨림

```javascript
// ❌ 매번 새 객체 → 무한 리렌더링
const data = useSelector(state => ({
    user: state.user,
    todos: state.todos
}));

// ✅ shallowEqual 사용
const data = useSelector(
    state => ({
        user: state.user,
        todos: state.todos
    }),
    shallowEqual
);
```

### 실수 2: useCallback 의존성 배열 누락

```javascript
// ❌ text가 변경되어도 오래된 값 사용
const handleSubmit = useCallback(() => {
    dispatch(addTodo(text));
}, [dispatch]); // text 누락!

// ✅ 모든 의존성 포함
const handleSubmit = useCallback(() => {
    dispatch(addTodo(text));
}, [text, dispatch]);
```

## 체크리스트 ✅

- [ ] useSelector로 State를 읽을 수 있다
- [ ] useDispatch로 Action을 dispatch할 수 있다
- [ ] shallowEqual로 성능 최적화를 할 수 있다
- [ ] Custom Hooks로 로직을 재사용할 수 있다
- [ ] connect HOC를 Hooks로 전환할 수 있다
- [ ] 실습 문제를 모두 해결했다

## 다음 단계 🚀

**다음 챕터**: `13. 컴포넌트 최적화 - 리렌더링 제어`에서 React.memo, useMemo, useCallback을 활용한 성능 최적화를 배웁니다!

### 추가 학습 자료
- [React-Redux Hooks API](https://react-redux.js.org/api/hooks)
- [useSelector Performance](https://react-redux.js.org/api/hooks#useselector)
- [Reselect 라이브러리](https://github.com/reduxjs/reselect)

---

**핵심 요약**: Hooks는 connect보다 간결하고 직관적입니다. 현대적인 Redux 개발에서는 Hooks를 사용하세요! 💪




