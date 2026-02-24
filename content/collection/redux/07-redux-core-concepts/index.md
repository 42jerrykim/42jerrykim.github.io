---
draft: true
title: "[Redux] 07. Redux의 핵심 - Action, Reducer, Store"
date: 2025-10-14
lastmod: 2025-10-14
tags:
- Action
- 액션
- 프론트엔드
- JavaScript
- TypeScript
- Code-Quality
- Implementation
- Best-Practices
- Clean-Code
- 클린코드
- Software-Architecture
- 소프트웨어아키텍처
description: "Redux의 3대 핵심 개념 완벽 정복. Action으로 무엇을 할지 정의, Reducer로 상태 변경 로직 구현, Store로 전체 관리하는 Redux의 작동 원리를 실제 코드와 함께 깊이 있게 학습합니다"
series: ["Redux 완전 정복"]
series_order: 7
---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- ✅ Action의 구조와 Action Creator 작성
- ✅ Reducer의 원리와 순수 함수로 작성
- ✅ Store 생성과 API 사용
- ✅ dispatch, getState, subscribe 활용
- ✅ combineReducers로 Reducer 조합

## Redux의 3대 핵심

Redux는 세 가지 핵심 개념으로 구성됩니다:

```
Action (무엇을 할지)
    ↓
Reducer (어떻게 변경할지)
    ↓
Store (상태 저장소)
```

## Action - 무엇이 일어났는지

### Action의 구조

```javascript
// Action은 plain JavaScript 객체
const action = {
    type: 'ADD_TODO',      // 필수: 액션 타입
    payload: {             // 선택: 데이터
        id: 1,
        text: 'Learn Redux'
    }
};

// FSA (Flux Standard Action) 형식
const fsaAction = {
    type: 'ADD_TODO',
    payload: { id: 1, text: 'Learn Redux' },
    error: false,          // 에러 여부 (선택)
    meta: { timestamp: Date.now() }  // 메타데이터 (선택)
};
```

**Action 규칙**:
- 반드시 `type` 프로퍼티 포함
- 직렬화 가능한 값만 사용 (함수, Promise 등 불가)
- 타입은 보통 대문자 상수

### Action Types

```javascript
// ❌ 문자열 직접 사용 (오타 위험)
dispatch({ type: 'ADD_TODO', payload: todo });
dispatch({ type: 'ADD_TOD0', payload: todo }); // 오타!

// ✅ 상수로 정의
const ADD_TODO = 'ADD_TODO';
const TOGGLE_TODO = 'TOGGLE_TODO';
const REMOVE_TODO = 'REMOVE_TODO';

dispatch({ type: ADD_TODO, payload: todo });

// ✅ 더 나은 방법: 모듈별로 구분
const ADD_TODO = 'todos/ADD_TODO';
const TOGGLE_TODO = 'todos/TOGGLE_TODO';
const REMOVE_TODO = 'todos/REMOVE_TODO';

// TypeScript Enum
enum TodoActionTypes {
    ADD_TODO = 'todos/ADD_TODO',
    TOGGLE_TODO = 'todos/TOGGLE_TODO',
    REMOVE_TODO = 'todos/REMOVE_TODO'
}
```

### Action Creator

```javascript
// 단순 Action Creator
function addTodo(text) {
    return {
        type: 'ADD_TODO',
        payload: {
            id: Date.now(),
            text,
            completed: false
        }
    };
}

// 사용
dispatch(addTodo('Learn Redux'));

// 복잡한 로직 포함
function toggleTodo(id) {
    return {
        type: 'TOGGLE_TODO',
        payload: id,
        meta: {
            timestamp: Date.now(),
            source: 'user-click'
        }
    };
}

// 조건부 Action
function removeTodoIfCompleted(id) {
    return (dispatch, getState) => {
        const todo = getState().todos.find(t => t.id === id);
        
        if (todo && todo.completed) {
            dispatch({
                type: 'REMOVE_TODO',
                payload: id
            });
        }
    };
}
```

### Action Creator 패턴

```javascript
// 1. 기본 패턴
const increment = () => ({ type: 'INCREMENT' });
const decrement = () => ({ type: 'DECREMENT' });

// 2. Payload Creator 패턴
const createAction = (type) => (payload) => ({
    type,
    payload
});

const addTodo = createAction('ADD_TODO');
const removeTodo = createAction('REMOVE_TODO');

// 3. Prepare 패턴 (Redux Toolkit 스타일)
function addTodo(text) {
    return {
        type: 'ADD_TODO',
        payload: prepare(text)
    };
}

function prepare(text) {
    return {
        id: Date.now(),
        text,
        completed: false,
        createdAt: new Date().toISOString()
    };
}

// 4. TypeScript Generic 패턴
function createAction<T>(type: string) {
    return (payload: T) => ({
        type,
        payload
    });
}

const addTodo = createAction<{ text: string }>('ADD_TODO');
```

## Reducer - 상태를 어떻게 변경할지

### Reducer의 기본 구조

```javascript
// Reducer: (state, action) => newState
function counterReducer(state = 0, action) {
    switch (action.type) {
        case 'INCREMENT':
            return state + 1;
        
        case 'DECREMENT':
            return state - 1;
        
        case 'INCREMENT_BY':
            return state + action.payload;
        
        default:
            return state;
    }
}

// 사용
let state = counterReducer(undefined, { type: '@@INIT' }); // 0
state = counterReducer(state, { type: 'INCREMENT' }); // 1
state = counterReducer(state, { type: 'INCREMENT' }); // 2
```

### 순수 함수 규칙

```javascript
// ✅ 순수 함수 - 좋은 Reducer
function todoReducer(state = [], action) {
    switch (action.type) {
        case 'ADD_TODO':
            // 새 배열 반환
            return [...state, action.payload];
        
        case 'TOGGLE_TODO':
            // map으로 새 배열 생성
            return state.map(todo =>
                todo.id === action.payload
                    ? { ...todo, completed: !todo.completed }
                    : todo
            );
        
        default:
            return state;
    }
}

// ❌ 순수하지 않은 함수 - 나쁜 Reducer
function badReducer(state = [], action) {
    switch (action.type) {
        case 'ADD_TODO':
            state.push(action.payload); // 원본 수정!
            return state;
        
        case 'REMOVE_TODO':
            const index = state.findIndex(t => t.id === action.payload);
            state.splice(index, 1); // 원본 수정!
            return state;
        
        case 'FETCH_TODOS':
            fetch('/api/todos'); // 부수 효과!
            return state;
        
        default:
            return state;
    }
}
```

**순수 함수 체크리스트**:
- [ ] 같은 입력 → 항상 같은 출력
- [ ] 부수 효과 없음 (API 호출, 랜덤 값, 날짜 등)
- [ ] 인자를 변경하지 않음

### 복잡한 State 다루기

```javascript
// 중첩된 객체 업데이트
const initialState = {
    user: {
        id: 1,
        profile: {
            name: 'Alice',
            email: 'alice@example.com',
            settings: {
                theme: 'dark',
                notifications: true
            }
        }
    },
    todos: []
};

function appReducer(state = initialState, action) {
    switch (action.type) {
        case 'UPDATE_THEME':
            return {
                ...state,
                user: {
                    ...state.user,
                    profile: {
                        ...state.user.profile,
                        settings: {
                            ...state.user.profile.settings,
                            theme: action.payload
                        }
                    }
                }
            };
        
        case 'UPDATE_USER_NAME':
            return {
                ...state,
                user: {
                    ...state.user,
                    profile: {
                        ...state.user.profile,
                        name: action.payload
                    }
                }
            };
        
        default:
            return state;
    }
}
```

### Reducer 패턴들

```javascript
// 1. Lookup Table 패턴
const handlers = {
    'INCREMENT': (state) => state + 1,
    'DECREMENT': (state) => state - 1,
    'RESET': () => 0
};

function counterReducer(state = 0, action) {
    const handler = handlers[action.type];
    return handler ? handler(state, action) : state;
}

// 2. createReducer 헬퍼
function createReducer(initialState, handlers) {
    return (state = initialState, action) => {
        const handler = handlers[action.type];
        return handler ? handler(state, action) : state;
    };
}

const todoReducer = createReducer([], {
    'ADD_TODO': (state, action) => [...state, action.payload],
    'REMOVE_TODO': (state, action) => 
        state.filter(t => t.id !== action.payload)
});

// 3. Immer 사용 (불변성 쉽게)
import produce from 'immer';

function todoReducer(state = [], action) {
    return produce(state, draft => {
        switch (action.type) {
            case 'ADD_TODO':
                draft.push(action.payload);
                break;
            
            case 'TOGGLE_TODO':
                const todo = draft.find(t => t.id === action.payload);
                if (todo) {
                    todo.completed = !todo.completed;
                }
                break;
        }
    });
}
```

## combineReducers - Reducer 조합

### 기본 사용법

```javascript
import { combineReducers } from 'redux';

// 개별 Reducer
function todosReducer(state = [], action) {
    switch (action.type) {
        case 'ADD_TODO':
            return [...state, action.payload];
        default:
            return state;
    }
}

function filterReducer(state = 'all', action) {
    switch (action.type) {
        case 'SET_FILTER':
            return action.payload;
        default:
            return state;
    }
}

// 조합
const rootReducer = combineReducers({
    todos: todosReducer,
    filter: filterReducer
});

// State 구조
// {
//     todos: [],
//     filter: 'all'
// }
```

### 중첩된 Reducer

```javascript
// User Reducers
const userProfileReducer = combineReducers({
    name: nameReducer,
    email: emailReducer,
    avatar: avatarReducer
});

const userReducer = combineReducers({
    profile: userProfileReducer,
    settings: settingsReducer,
    permissions: permissionsReducer
});

// Root Reducer
const rootReducer = combineReducers({
    user: userReducer,
    todos: todosReducer,
    posts: postsReducer
});

// State 구조
// {
//     user: {
//         profile: { name, email, avatar },
//         settings: { ... },
//         permissions: { ... }
//     },
//     todos: [...],
//     posts: [...]
// }
```

### 커스텀 combineReducers

```javascript
// combineReducers의 동작 원리
function customCombineReducers(reducers) {
    return (state = {}, action) => {
        const nextState = {};
        
        for (const key in reducers) {
            const reducer = reducers[key];
            const previousStateForKey = state[key];
            const nextStateForKey = reducer(previousStateForKey, action);
            nextState[key] = nextStateForKey;
        }
        
        return nextState;
    };
}

// 사용
const rootReducer = customCombineReducers({
    todos: todosReducer,
    filter: filterReducer
});
```

## Store - 상태 관리의 중심

### Store 생성

```javascript
import { createStore } from 'redux';

// 기본 생성
const store = createStore(rootReducer);

// 초기 상태 지정
const preloadedState = {
    todos: [
        { id: 1, text: 'Learn Redux', completed: false }
    ],
    filter: 'all'
};

const store = createStore(rootReducer, preloadedState);

// Enhancer 사용
const store = createStore(
    rootReducer,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);
```

### Store API

```javascript
// 1. getState() - 현재 상태 읽기
const state = store.getState();
console.log(state);
// { todos: [...], filter: 'all' }

// 2. dispatch(action) - 액션 발송
store.dispatch({ type: 'ADD_TODO', payload: { id: 2, text: 'Build App' } });

store.dispatch(addTodo('Learn React'));

// 3. subscribe(listener) - 상태 변경 구독
const unsubscribe = store.subscribe(() => {
    console.log('State changed:', store.getState());
});

// 구독 취소
unsubscribe();

// 4. replaceReducer(nextReducer) - Reducer 교체 (핫 리로딩)
store.replaceReducer(newRootReducer);
```

### Subscribe 패턴

```javascript
// 기본 Subscribe
const unsubscribe = store.subscribe(() => {
    const state = store.getState();
    console.log('New state:', state);
});

// 특정 값 변경 감지
let previousValue = store.getState().counter.count;

store.subscribe(() => {
    const state = store.getState();
    const currentValue = state.counter.count;
    
    if (currentValue !== previousValue) {
        console.log('Count changed:', previousValue, '->', currentValue);
        previousValue = currentValue;
    }
});

// Debounce 적용
import debounce from 'lodash/debounce';

const handleChange = debounce(() => {
    console.log('State changed:', store.getState());
}, 1000);

store.subscribe(handleChange);

// 여러 구독자 관리
const subscribers = new Set();

function subscribe(listener) {
    subscribers.add(listener);
    
    return () => {
        subscribers.delete(listener);
    };
}

function notifySubscribers() {
    const state = store.getState();
    subscribers.forEach(listener => listener(state));
}

store.subscribe(notifySubscribers);
```

## 실전 Redux 구현

### 완전한 Todo 앱 Redux

```javascript
// types.js
export const ADD_TODO = 'todos/ADD_TODO';
export const TOGGLE_TODO = 'todos/TOGGLE_TODO';
export const REMOVE_TODO = 'todos/REMOVE_TODO';
export const SET_FILTER = 'filter/SET_FILTER';

// actions.js
export const addTodo = (text) => ({
    type: ADD_TODO,
    payload: {
        id: Date.now(),
        text,
        completed: false
    }
});

export const toggleTodo = (id) => ({
    type: TOGGLE_TODO,
    payload: id
});

export const removeTodo = (id) => ({
    type: REMOVE_TODO,
    payload: id
});

export const setFilter = (filter) => ({
    type: SET_FILTER,
    payload: filter
});

// reducers/todos.js
import { ADD_TODO, TOGGLE_TODO, REMOVE_TODO } from '../types';

const initialState = [];

export default function todosReducer(state = initialState, action) {
    switch (action.type) {
        case ADD_TODO:
            return [...state, action.payload];
        
        case TOGGLE_TODO:
            return state.map(todo =>
                todo.id === action.payload
                    ? { ...todo, completed: !todo.completed }
                    : todo
            );
        
        case REMOVE_TODO:
            return state.filter(todo => todo.id !== action.payload);
        
        default:
            return state;
    }
}

// reducers/filter.js
import { SET_FILTER } from '../types';

const initialState = 'all';

export default function filterReducer(state = initialState, action) {
    switch (action.type) {
        case SET_FILTER:
            return action.payload;
        
        default:
            return state;
    }
}

// reducers/index.js
import { combineReducers } from 'redux';
import todos from './todos';
import filter from './filter';

export default combineReducers({
    todos,
    filter
});

// store.js
import { createStore } from 'redux';
import rootReducer from './reducers';

const store = createStore(
    rootReducer,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);

export default store;

// index.js - 사용 예제
import store from './store';
import { addTodo, toggleTodo, setFilter } from './actions';

// 구독
store.subscribe(() => {
    console.log('State:', store.getState());
});

// Action dispatch
store.dispatch(addTodo('Learn Redux'));
store.dispatch(addTodo('Build App'));
store.dispatch(toggleTodo(1));
store.dispatch(setFilter('active'));

console.log('Final State:', store.getState());
```

### TypeScript Redux

```typescript
// types.ts
export const ADD_TODO = 'todos/ADD_TODO' as const;
export const TOGGLE_TODO = 'todos/TOGGLE_TODO' as const;
export const REMOVE_TODO = 'todos/REMOVE_TODO' as const;

export interface Todo {
    id: number;
    text: string;
    completed: boolean;
}

export interface TodoState {
    todos: Todo[];
    filter: 'all' | 'active' | 'completed';
}

// actions.ts
import { ADD_TODO, TOGGLE_TODO, REMOVE_TODO } from './types';

export const addTodo = (text: string) => ({
    type: ADD_TODO,
    payload: {
        id: Date.now(),
        text,
        completed: false
    }
});

export const toggleTodo = (id: number) => ({
    type: TOGGLE_TODO,
    payload: id
});

export const removeTodo = (id: number) => ({
    type: REMOVE_TODO,
    payload: id
});

export type TodoAction =
    | ReturnType<typeof addTodo>
    | ReturnType<typeof toggleTodo>
    | ReturnType<typeof removeTodo>;

// reducer.ts
import { TodoState, TodoAction } from './types';
import { ADD_TODO, TOGGLE_TODO, REMOVE_TODO } from './types';

const initialState: TodoState = {
    todos: [],
    filter: 'all'
};

export default function todoReducer(
    state: TodoState = initialState,
    action: TodoAction
): TodoState {
    switch (action.type) {
        case ADD_TODO:
            return {
                ...state,
                todos: [...state.todos, action.payload]
            };
        
        case TOGGLE_TODO:
            return {
                ...state,
                todos: state.todos.map(todo =>
                    todo.id === action.payload
                        ? { ...todo, completed: !todo.completed }
                        : todo
                )
            };
        
        case REMOVE_TODO:
            return {
                ...state,
                todos: state.todos.filter(todo => todo.id !== action.payload)
            };
        
        default:
            return state;
    }
}
```

## 실습 문제 🏋️‍♂️

### 문제 1: Counter Reducer 작성
```javascript
// TODO: 다음 기능을 가진 Counter Reducer 작성
// - INCREMENT: +1
// - DECREMENT: -1
// - INCREMENT_BY: 특정 값만큼 증가
// - RESET: 0으로 초기화

// 답안:
const initialState = 0;

function counterReducer(state = initialState, action) {
    switch (action.type) {
        case 'INCREMENT':
            return state + 1;
        
        case 'DECREMENT':
            return state - 1;
        
        case 'INCREMENT_BY':
            return state + action.payload;
        
        case 'RESET':
            return 0;
        
        default:
            return state;
    }
}
```

### 문제 2: Action Creator 작성
```javascript
// TODO: User Action Creator 작성
// - loginUser(username, password)
// - logoutUser()
// - updateProfile(profileData)

// 답안:
export const loginUser = (username, password) => ({
    type: 'user/LOGIN',
    payload: { username, password }
});

export const logoutUser = () => ({
    type: 'user/LOGOUT'
});

export const updateProfile = (profileData) => ({
    type: 'user/UPDATE_PROFILE',
    payload: profileData
});
```

## 체크리스트 ✅

- [ ] Action의 구조를 이해하고 작성할 수 있다
- [ ] Action Creator를 만들 수 있다
- [ ] 순수 함수로 Reducer를 작성할 수 있다
- [ ] combineReducers로 Reducer를 조합할 수 있다
- [ ] Store를 생성하고 API를 사용할 수 있다
- [ ] dispatch, getState, subscribe를 활용할 수 있다

## 다음 단계 🚀

**다음 챕터**: `08. 불변성의 중요성 - Immutability in Redux`에서 Redux에서 가장 중요한 불변성 개념을 깊이 있게 학습합니다!

### 추가 학습 자료
- [Redux Core Concepts](https://redux.js.org/introduction/core-concepts)
- [Reducers](https://redux.js.org/tutorials/fundamentals/part-3-state-actions-reducers)
- [Store](https://redux.js.org/tutorials/fundamentals/part-4-store)

---

**핵심 요약**: Action, Reducer, Store는 Redux의 심장입니다. 이 세 가지를 완벽히 이해하면 Redux의 80%를 마스터한 것입니다! 💪




