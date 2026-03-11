---
draft: true
title: "[Redux] 15. 실습: Counter와 Todo 앱 만들기"
date: 2025-10-14
lastmod: 2025-10-14
description: "지금까지 배운 Redux 지식을 총동원한 실전 프로젝트. Counter 앱으로 기초 다지기, Todo 앱으로 CRUD 마스터, Redux Hooks와 Selector 패턴을 적용한 완전한 애플리케이션 구축하기."
slug: practice-counter-todo
tags:
  - JavaScript
  - TypeScript
  - React
  - Frontend
  - 프론트엔드
  - Web
  - 웹
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - 실습
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
  - Performance
  - 성능
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
  - Memoization
  - Optimization
  - 최적화
  - Functional-Programming
  - 함수형프로그래밍
series: ["Redux 완전 정복"]
series_order: 15
---

Phase 3의 마지막 장으로 **01~14장에서 배운 내용을 한 번에 쓰는 실습**을 합니다. Redux store 설정, reducer·action 작성, React-Redux Provider·useSelector·useDispatch 연결, 그리고 Counter·Todo 앱을 처음부터 구현해 보면서 CRUD와 리렌더 최적화까지 경험합니다. 이 장을 마치면 Redux Toolkit(Phase 4)이나 실제 프로젝트에 Redux를 도입할 준비가 됩니다. 코드를 직접 타이핑하고 단계별로 실행해 보는 것을 권합니다.

## 이 글을 읽은 후 달성해야 할 목표 (평가 기준)

이 챕터를 마치면 다음을 할 수 있어야 합니다:

- Redux 프로젝트를 처음부터 설정하고, **Store**·**Reducer**·**Action**을 조합해 Counter·Todo 앱을 구현할 수 있다.
- React-Redux **Hooks**(useSelector, useDispatch)와 **Selector** 패턴을 실전에 적용할 수 있다.
- CRUD 흐름과 성능 최적화(불필요한 리렌더 방지)를 코드로 보여줄 수 있다.

## 프로젝트 개요

두 개의 앱을 만들어 Redux를 완벽히 이해합니다:

1. **Counter 앱**: Redux 기초 다지기
2. **Todo 앱**: 실전 CRUD 애플리케이션

## 프로젝트 1: Counter 앱

Counter 앱으로 **Store**·**Slice**·**Provider**·**useSelector**·**useDispatch** 흐름을 한 번에 익힙니다. 먼저 Create React App으로 프로젝트를 만들고 Redux 관련 패키지를 설치합니다.

### 프로젝트 생성

```bash
# Create React App
npx create-react-app redux-counter --template typescript
cd redux-counter

# Redux 설치
npm install @reduxjs/toolkit react-redux

# (선택) Redux DevTools 확장
# 크롬 웹스토어에서 "Redux DevTools" 설치
```

설치가 끝나면 **store**·**components** 폴더를 두고, **Store** 설정·Slice·진입점 역할을 나눕니다. 아래 구조를 참고하면 됩니다.

### 폴더 구조

```
src/
├── store/
│   ├── index.ts         # Store 설정
│   ├── counterSlice.ts  # Counter Reducer & Actions
│   └── types.ts         # TypeScript 타입
├── components/
│   └── Counter.tsx
├── App.tsx
└── index.tsx
```

**Redux Toolkit**의 **createSlice**로 **Reducer**와 **Action Creator**를 한 번에 정의합니다. **configureStore**로 **Store**를 만들고, **RootState**·**AppDispatch** 타입을 export해 **useSelector**·**useDispatch**에서 쓰면 됩니다. 아래는 Counter용 Slice와 Store 설정입니다.

### Redux Store 설정

```typescript
// src/store/types.ts
export interface CounterState {
    count: number;
}

export interface RootState {
    counter: CounterState;
}

// src/store/counterSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { CounterState } from './types';

const initialState: CounterState = {
    count: 0
};

const counterSlice = createSlice({
    name: 'counter',
    initialState,
    reducers: {
        increment: (state) => {
            state.count += 1;
        },
        decrement: (state) => {
            state.count -= 1;
        },
        incrementByAmount: (state, action: PayloadAction<number>) => {
            state.count += action.payload;
        },
        reset: (state) => {
            state.count = 0;
        }
    }
});

export const { increment, decrement, incrementByAmount, reset } = 
    counterSlice.actions;

export default counterSlice.reducer;

// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

export const store = configureStore({
    reducer: {
        counter: counterReducer
    }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

**Store**를 React 트리에 넣기 위해 **Provider**로 앱 최상위를 감쌉니다. **index.tsx**에서 **store**를 import해 **Provider**의 **store** prop으로 넘기면, 하위 컴포넌트에서 **useSelector**·**useDispatch**를 사용할 수 있습니다.

### Provider 설정

```typescript
// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from './store';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);

root.render(
    <React.StrictMode>
        <Provider store={store}>
            <App />
        </Provider>
    </React.StrictMode>
);
```

### Counter 컴포넌트

**useSelector**로 **count**를 읽고, **useDispatch**로 **increment**·**decrement** 등을 호출하는 **Counter** UI를 만듭니다. **RootState** 타입을 쓰면 **state.counter.count** 자동완성이 되고, **dispatch**에 **action creator**를 넘기면 타입이 보장됩니다. 아래는 Counter 컴포넌트 예시입니다.

```typescript
// src/components/Counter.tsx
import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState } from '../store';
import { 
    increment, 
    decrement, 
    incrementByAmount, 
    reset 
} from '../store/counterSlice';

export default function Counter() {
    const count = useSelector((state: RootState) => state.counter.count);
    const dispatch = useDispatch();
    const [amount, setAmount] = useState<string>('5');

    const handleIncrementByAmount = () => {
        const value = parseInt(amount);
        if (!isNaN(value)) {
            dispatch(incrementByAmount(value));
        }
    };

    return (
        <div className="counter">
            <h1>Redux Counter</h1>
            <div className="display">
                <h2>{count}</h2>
            </div>
            <div className="controls">
                <button onClick={() => dispatch(decrement())}>-1</button>
                <button onClick={() => dispatch(increment())}>+1</button>
                <button onClick={() => dispatch(reset())}>Reset</button>
            </div>
            <div className="custom-amount">
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                />
                <button onClick={handleIncrementByAmount}>
                    Add Amount
                </button>
            </div>
        </div>
    );
}

// src/App.tsx
import Counter from './components/Counter';
import './App.css';

function App() {
    return (
        <div className="App">
            <Counter />
        </div>
    );
}

export default App;
```

### 스타일링

```css
/* src/App.css */
.App {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.counter {
    background: white;
    padding: 3rem;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    text-align: center;
}

.counter h1 {
    margin-bottom: 2rem;
    color: #333;
}

.display {
    margin: 2rem 0;
}

.display h2 {
    font-size: 4rem;
    color: #667eea;
    margin: 0;
}

.controls {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

button {
    flex: 1;
    padding: 1rem;
    font-size: 1.2rem;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: transform 0.1s, background-color 0.2s;
    background-color: #667eea;
    color: white;
}

button:hover {
    background-color: #5568d3;
}

button:active {
    transform: scale(0.95);
}

.custom-amount {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
}

.custom-amount input {
    flex: 1;
    padding: 0.8rem;
    font-size: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
}

.custom-amount input:focus {
    outline: none;
    border-color: #667eea;
}
```

## 프로젝트 2: Todo 앱

Counter에서 익힌 **Store**·**Provider**·Hooks에 더해, **여러 Slice**(todos, filter), **Selector**, **CRUD** 흐름을 Todo 앱에 적용합니다. 추가·완료 토글·삭제·필터를 구현하고, 13·14장의 **React.memo**·**Reselect**를 선택적으로 적용할 수 있습니다. 먼저 폴더 구조와 Slice 정의부터 진행합니다.

### 프로젝트 구조

```
src/
├── store/
│   ├── index.ts
│   ├── todosSlice.ts
│   ├── filterSlice.ts
│   └── selectors.ts
├── components/
│   ├── TodoList.tsx
│   ├── TodoItem.tsx
│   ├── TodoForm.tsx
│   ├── TodoFilter.tsx
│   └── TodoStats.tsx
├── App.tsx
└── index.tsx
```

### Todos Slice

Todo 항목의 **state**(목록)와 **추가·완료 토글·삭제** 액션을 **createSlice**로 정의합니다. **id**·**text**·**completed** 필드를 두고, **불변성**은 Redux Toolkit이 Immer로 처리해 주므로 **state**를 직접 수정하는 형태로 작성해도 됩니다.

```typescript
// src/store/todosSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface Todo {
    id: string;
    text: string;
    completed: boolean;
    createdAt: number;
}

interface TodosState {
    todos: Todo[];
}

const initialState: TodosState = {
    todos: []
};

const todosSlice = createSlice({
    name: 'todos',
    initialState,
    reducers: {
        addTodo: {
            reducer: (state, action: PayloadAction<Todo>) => {
                state.todos.push(action.payload);
            },
            prepare: (text: string) => ({
                payload: {
                    id: Date.now().toString(),
                    text,
                    completed: false,
                    createdAt: Date.now()
                }
            })
        },
        toggleTodo: (state, action: PayloadAction<string>) => {
            const todo = state.todos.find(t => t.id === action.payload);
            if (todo) {
                todo.completed = !todo.completed;
            }
        },
        removeTodo: (state, action: PayloadAction<string>) => {
            state.todos = state.todos.filter(t => t.id !== action.payload);
        },
        editTodo: (state, action: PayloadAction<{ id: string; text: string }>) => {
            const todo = state.todos.find(t => t.id === action.payload.id);
            if (todo) {
                todo.text = action.payload.text;
            }
        },
        clearCompleted: (state) => {
            state.todos = state.todos.filter(t => !t.completed);
        },
        toggleAll: (state) => {
            const allCompleted = state.todos.every(t => t.completed);
            state.todos.forEach(todo => {
                todo.completed = !allCompleted;
            });
        }
    }
});

export const { 
    addTodo, 
    toggleTodo, 
    removeTodo, 
    editTodo,
    clearCompleted,
    toggleAll
} = todosSlice.actions;

export default todosSlice.reducer;
```

**전체/활성/완료** 필터 상태를 **filter** 슬라이스로 분리해 두면 **todos**와 독립적으로 관리할 수 있습니다. **setFilter** 액션 하나로 **currentFilter**만 바꾸고, **Selector**에서 **todos**와 **filter**를 조합해 보여줄 목록을 계산합니다.

### Filter Slice

```typescript
// src/store/filterSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export type FilterType = 'all' | 'active' | 'completed';

interface FilterState {
    currentFilter: FilterType;
}

const initialState: FilterState = {
    currentFilter: 'all'
};

const filterSlice = createSlice({
    name: 'filter',
    initialState,
    reducers: {
        setFilter: (state, action: PayloadAction<FilterType>) => {
            state.currentFilter = action.payload;
        }
    }
});

export const { setFilter } = filterSlice.actions;
export default filterSlice.reducer;
```

**todos**와 **filter**를 조합해 **보이는 목록**과 **통계**를 메모이제이션하는 **Selector**를 정의합니다. **createSelector**로 두면 **todos**·**filter**가 바뀔 때만 재계산됩니다.

### Selectors

**필터링된 Todo 목록**과 **통계**(전체·완료·미완료 개수)는 **Reselect**의 **createSelector**로 메모이제이션합니다. **useSelector**에 넘기면 **todos**·**filter**가 바뀔 때만 재계산되어 불필요한 리렌더를 줄일 수 있습니다.

```typescript
// src/store/selectors.ts
import { createSelector } from '@reduxjs/toolkit';
import { RootState } from './index';

const selectTodos = (state: RootState) => state.todos.todos;
const selectFilter = (state: RootState) => state.filter.currentFilter;

export const selectVisibleTodos = createSelector(
    [selectTodos, selectFilter],
    (todos, filter) => {
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

export const selectTodoStats = createSelector(
    [selectTodos],
    (todos) => ({
        total: todos.length,
        completed: todos.filter(t => t.completed).length,
        active: todos.filter(t => !t.completed).length
    })
);
```

**todos**·**filter** 두 슬라이스를 **configureStore**의 **reducer**에 넣어 **Store**를 만들고, **RootState**·**AppDispatch**를 export해 **useSelector**·**useDispatch** 타입에 사용합니다.

### Store 설정

```typescript
// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import todosReducer from './todosSlice';
import filterReducer from './filterSlice';

export const store = configureStore({
    reducer: {
        todos: todosReducer,
        filter: filterReducer
    }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### Todo Components

아래는 **TodoList**·**TodoItem**·**TodoForm**·**Filter** 컴포넌트를 **useSelector**·**useDispatch**와 Selector로 연결한 예입니다. **TodoItem**은 **React.memo**로 감싸고, **onToggle**·**onRemove**는 **useCallback**으로 고정해 불필요한 리렌더를 줄입니다. 전체 코드가 길어 핵심 패턴만 발췌했으며, 스타일은 생략할 수 있습니다.

```typescript
// src/components/TodoForm.tsx
import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { addTodo } from '../store/todosSlice';

export default function TodoForm() {
    const [text, setText] = useState('');
    const dispatch = useDispatch();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (text.trim()) {
            dispatch(addTodo(text.trim()));
            setText('');
        }
    };

    return (
        <form onSubmit={handleSubmit} className="todo-form">
            <input
                type="text"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="What needs to be done?"
                className="todo-input"
            />
            <button type="submit" className="add-button">Add</button>
        </form>
    );
}

// src/components/TodoItem.tsx
import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { toggleTodo, removeTodo, editTodo } from '../store/todosSlice';
import type { Todo } from '../store/todosSlice';

interface TodoItemProps {
    todo: Todo;
}

export const TodoItem = React.memo(function TodoItem({ todo }: TodoItemProps) {
    const dispatch = useDispatch();
    const [isEditing, setIsEditing] = useState(false);
    const [editText, setEditText] = useState(todo.text);

    const handleSave = () => {
        if (editText.trim()) {
            dispatch(editTodo({ id: todo.id, text: editText.trim() }));
            setIsEditing(false);
        }
    };

    const handleCancel = () => {
        setEditText(todo.text);
        setIsEditing(false);
    };

    if (isEditing) {
        return (
            <li className="todo-item editing">
                <input
                    type="text"
                    value={editText}
                    onChange={(e) => setEditText(e.target.value)}
                    onBlur={handleSave}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') handleSave();
                        if (e.key === 'Escape') handleCancel();
                    }}
                    autoFocus
                />
            </li>
        );
    }

    return (
        <li className={`todo-item ${todo.completed ? 'completed' : ''}`}>
            <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => dispatch(toggleTodo(todo.id))}
            />
            <span onDoubleClick={() => setIsEditing(true)}>
                {todo.text}
            </span>
            <button 
                onClick={() => dispatch(removeTodo(todo.id))}
                className="delete-button"
            >
                ×
            </button>
        </li>
    );
});

// src/components/TodoList.tsx
import React from 'react';
import { useSelector } from 'react-redux';
import { selectVisibleTodos } from '../store/selectors';
import { TodoItem } from './TodoItem';

export default function TodoList() {
    const todos = useSelector(selectVisibleTodos);

    if (todos.length === 0) {
        return <p className="empty-message">No todos to show!</p>;
    }

    return (
        <ul className="todo-list">
            {todos.map(todo => (
                <TodoItem key={todo.id} todo={todo} />
            ))}
        </ul>
    );
}

// src/components/TodoFilter.tsx
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { setFilter, FilterType } from '../store/filterSlice';

export default function TodoFilter() {
    const currentFilter = useSelector(
        (state: RootState) => state.filter.currentFilter
    );
    const dispatch = useDispatch();

    const filters: FilterType[] = ['all', 'active', 'completed'];

    return (
        <div className="todo-filters">
            {filters.map(filter => (
                <button
                    key={filter}
                    onClick={() => dispatch(setFilter(filter))}
                    className={currentFilter === filter ? 'active' : ''}
                >
                    {filter.charAt(0).toUpperCase() + filter.slice(1)}
                </button>
            ))}
        </div>
    );
}

// src/components/TodoStats.tsx
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { selectTodoStats } from '../store/selectors';
import { clearCompleted, toggleAll } from '../store/todosSlice';

export default function TodoStats() {
    const stats = useSelector(selectTodoStats);
    const dispatch = useDispatch();

    return (
        <div className="todo-stats">
            <div className="stats-info">
                <span>{stats.active} items left</span>
                <span>Total: {stats.total}</span>
                <span>Completed: {stats.completed}</span>
            </div>
            <div className="stats-actions">
                <button onClick={() => dispatch(toggleAll())}>
                    Toggle All
                </button>
                {stats.completed > 0 && (
                    <button onClick={() => dispatch(clearCompleted())}>
                        Clear Completed
                    </button>
                )}
            </div>
        </div>
    );
}
```

### App 컴포넌트

```typescript
// src/App.tsx
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import TodoFilter from './components/TodoFilter';
import TodoStats from './components/TodoStats';
import './App.css';

function App() {
    return (
        <div className="App">
            <div className="todo-container">
                <h1>Redux Todo App</h1>
                <TodoForm />
                <TodoFilter />
                <TodoList />
                <TodoStats />
            </div>
        </div>
    );
}

export default App;
```

### 스타일링

```css
/* src/App.css */
.App {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
}

.todo-container {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    width: 100%;
    max-width: 600px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.todo-container h1 {
    text-align: center;
    color: #333;
    margin-bottom: 2rem;
}

.todo-form {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.todo-input {
    flex: 1;
    padding: 1rem;
    font-size: 1rem;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
}

.todo-input:focus {
    outline: none;
    border-color: #667eea;
}

.add-button {
    padding: 1rem 2rem;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1rem;
}

.add-button:hover {
    background: #5568d3;
}

.todo-filters {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    justify-content: center;
}

.todo-filters button {
    padding: 0.5rem 1rem;
    border: 2px solid #e0e0e0;
    background: white;
    border-radius: 8px;
    cursor: pointer;
}

.todo-filters button.active {
    background: #667eea;
    color: white;
    border-color: #667eea;
}

.todo-list {
    list-style: none;
    padding: 0;
    margin: 0 0 1.5rem 0;
}

.todo-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border-bottom: 1px solid #e0e0e0;
}

.todo-item.completed span {
    text-decoration: line-through;
    color: #999;
}

.todo-item input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
}

.todo-item span {
    flex: 1;
    cursor: pointer;
}

.todo-item.editing input[type="text"] {
    flex: 1;
    padding: 0.5rem;
    font-size: 1rem;
    border: 2px solid #667eea;
    border-radius: 5px;
}

.delete-button {
    background: #ff4757;
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    cursor: pointer;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.delete-button:hover {
    background: #ee5a6f;
}

.empty-message {
    text-align: center;
    color: #999;
    padding: 2rem;
}

.todo-stats {
    border-top: 2px solid #e0e0e0;
    padding-top: 1rem;
}

.stats-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
    color: #666;
}

.stats-actions {
    display: flex;
    gap: 0.5rem;
}

.stats-actions button {
    padding: 0.5rem 1rem;
    background: white;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
}

.stats-actions button:hover {
    background: #f5f5f5;
}
```

## 확장 기능 추가하기

기본 Counter·Todo 구현이 끝나면 **LocalStorage**에 **state**를 저장·복원하거나, **검색** 기능을 넣어 볼 수 있습니다. **state** 구조가 바뀌면 직렬화·복원 로직을 함께 수정해야 합니다.

### LocalStorage 연동

```typescript
// src/store/middleware/localStorage.ts
import { Middleware } from '@reduxjs/toolkit';

const LOCAL_STORAGE_KEY = 'redux-todos';

export const localStorageMiddleware: Middleware = store => next => action => {
    const result = next(action);
    
    // Save to localStorage after every action
    if (action.type.startsWith('todos/')) {
        const state = store.getState();
        localStorage.setItem(
            LOCAL_STORAGE_KEY,
            JSON.stringify(state.todos)
        );
    }
    
    return result;
};

// Load from localStorage
export const loadState = () => {
    try {
        const serialized = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (serialized === null) {
            return undefined;
        }
        return JSON.parse(serialized);
    } catch (err) {
        return undefined;
    }
};

// src/store/index.ts (수정)
import { configureStore } from '@reduxjs/toolkit';
import todosReducer from './todosSlice';
import filterReducer from './filterSlice';
import { localStorageMiddleware, loadState } from './middleware/localStorage';

const preloadedState = {
    todos: loadState() || { todos: [] },
    filter: { currentFilter: 'all' as const }
};

export const store = configureStore({
    reducer: {
        todos: todosReducer,
        filter: filterReducer
    },
    preloadedState,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(localStorageMiddleware)
});
```

### 검색 기능

```typescript
// searchSlice.ts 추가
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SearchState {
    query: string;
}

const initialState: SearchState = {
    query: ''
};

const searchSlice = createSlice({
    name: 'search',
    initialState,
    reducers: {
        setSearchQuery: (state, action: PayloadAction<string>) => {
            state.query = action.payload;
        }
    }
});

export const { setSearchQuery } = searchSlice.actions;
export default searchSlice.reducer;

// selectors.ts (수정)
export const selectFilteredTodos = createSelector(
    [selectTodos, selectFilter, (state: RootState) => state.search.query],
    (todos, filter, query) => {
        let result = todos;
        
        // Filter
        if (filter !== 'all') {
            result = result.filter(t =>
                filter === 'completed' ? t.completed : !t.completed
            );
        }
        
        // Search
        if (query) {
            result = result.filter(t =>
                t.text.toLowerCase().includes(query.toLowerCase())
            );
        }
        
        return result;
    }
);
```

## 체크리스트 ✅

- [ ] Counter 앱을 성공적으로 만들었다
- [ ] Todo 앱의 CRUD 기능이 모두 작동한다
- [ ] Redux DevTools로 Action과 State를 확인했다
- [ ] Selector를 사용하여 성능 최적화를 적용했다
- [ ] LocalStorage로 데이터를 영구 저장했다

## 다음 단계 🚀

축하합니다! Phase 3를 완료했습니다!

**다음 챕터**: `16. Redux Toolkit 소개`에서 더 현대적이고 강력한 Redux Toolkit을 본격적으로 배웁니다!

### 추가 과제
- [ ] 카테고리 기능 추가
- [ ] 드래그 앤 드롭으로 순서 변경
- [ ] 우선순위 필드 추가
- [ ] 마감일 기능 추가
- [ ] 다크 모드 구현

---

**핵심 요약**: 실습이 최고의 학습입니다. 직접 코드를 작성하며 Redux를 체득하세요! 💪




