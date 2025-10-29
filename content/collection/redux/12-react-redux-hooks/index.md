---
draft: true
title: "[Redux] 12. React-Redux Hooks - useSelector와 useDispatch"
date: 2025-10-14
lastmod: 2025-10-14
tags: ["Redux", "React", "React-Redux", "Hooks", "useSelector", "useDispatch", "React Hooks", "리액트훅스", "상태관리", "State Management", "웹개발", "프론트엔드", "리액트", "리덕스", "Modern Redux", "현대적리덕스", "Functional Components", "함수형컴포넌트", "Custom Hooks", "커스텀훅스", "useStore", "TypeScript", "타입스크립트", "JavaScript", "자바스크립트", "개발", "코딩", "Redux Patterns", "리덕스패턴", "Performance", "성능", "Optimization", "최적화", "Equality Function", "비교함수", "Memoization", "메모이제이션", "Best Practices", "모범사례", "Clean Code", "클린코드", "Redux Tutorial", "리덕스튜토리얼", "개발자가이드"]
description: "현대적인 React-Redux Hooks 완벽 마스터. useSelector로 간결한 상태 조회, useDispatch로 액션 발송, 성능 최적화까지 connect HOC를 대체하는 Hooks API를 실전 예제로 학습합니다"
series: ["Redux 완전 정복"]
series_order: 12
---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- ✅ useSelector로 Redux State 읽기
- ✅ useDispatch로 Action 발송하기
- ✅ connect HOC를 Hooks로 전환
- ✅ Custom Hooks로 로직 재사용
- ✅ 성능 최적화 기법 적용

## 왜 Hooks를 사용하는가?

connect HOC vs Hooks 비교:

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

**주의**: useStore는 거의 사용하지 않음. useSelector와 useDispatch로 충분!

## 성능 최적화

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

## 실전 예제: Todo 앱

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




