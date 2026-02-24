---
draft: true
title: "[Redux] 11. React-Redux 시작하기 - Provider와 connect"
date: 2025-10-14
lastmod: 2025-10-14
tags:
- React
- 프론트엔드
- Software-Architecture
- Nuance
- JavaScript
- TypeScript
- Implementation
- Best-Practices
description: "React와 Redux를 연결하는 React-Redux 라이브러리 완벽 마스터. Provider로 Store 제공, connect HOC로 컴포넌트 연결, mapStateToProps와 mapDispatchToProps 패턴을 실전 예제로 학습합니다"
series: ["Redux 완전 정복"]
series_order: 11
---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- ✅ React-Redux 라이브러리 설치와 설정
- ✅ Provider로 Redux Store를 React 앱에 제공
- ✅ connect HOC로 컴포넌트와 Redux 연결
- ✅ mapStateToProps로 State를 Props로 전달
- ✅ mapDispatchToProps로 Action Dispatch 함수 전달

## 왜 React-Redux가 필요한가?

Redux는 독립적인 라이브러리이므로 React와 직접 연결되지 않습니다:

```javascript
// ❌ Redux만으로는 React와 연동 불가
import { createStore } from 'redux';

const store = createStore(reducer);
// React 컴포넌트가 store를 어떻게 알 수 있을까?

// ✅ React-Redux가 연결해줌
import { Provider } from 'react-redux';

<Provider store={store}>
    <App />
</Provider>
```

**React-Redux**: Redux Store와 React 컴포넌트를 연결하는 공식 바인딩 라이브러리

## React-Redux 설치 및 설정

### 설치

```bash
# npm
npm install react-redux

# yarn
yarn add react-redux

# Redux도 함께 설치 (아직 안 했다면)
npm install redux
```

### 기본 프로젝트 구조

```
src/
├── store/
│   ├── index.js         # Store 생성
│   └── reducers/
│       └── counterReducer.js
├── components/
│   ├── Counter.js       # 프레젠테이셔널 컴포넌트
│   └── CounterContainer.js  # 컨테이너 컴포넌트
├── App.js
└── index.js
```

## Provider - Redux Store 제공

### Provider 컴포넌트

```javascript
// src/store/index.js
import { createStore } from 'redux';
import rootReducer from './reducers';

const store = createStore(rootReducer);

export default store;

// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import store from './store';
import App from './App';

ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
);
```

**Provider의 역할**:
- Redux Store를 React Context에 넣어줌
- 모든 하위 컴포넌트가 Store에 접근 가능
- 앱의 최상위에서 한 번만 사용

### Provider의 작동 원리

```javascript
// Provider 내부 동작 (간소화 버전)
function Provider({ store, children }) {
    return (
        <ReduxContext.Provider value={store}>
            {children}
        </ReduxContext.Provider>
    );
}

// 하위 컴포넌트에서 접근
function ChildComponent() {
    const store = useContext(ReduxContext);
    // store.getState(), store.dispatch() 사용 가능
}
```

## connect - 컴포넌트와 Redux 연결

### connect 기본 사용법

```javascript
import { connect } from 'react-redux';

// 1. 프레젠테이셔널 컴포넌트 (순수 React)
function Counter({ count, increment, decrement }) {
    return (
        <div>
            <h1>Count: {count}</h1>
            <button onClick={increment}>+1</button>
            <button onClick={decrement}>-1</button>
        </div>
    );
}

// 2. mapStateToProps: State → Props
const mapStateToProps = (state) => ({
    count: state.counter.count
});

// 3. mapDispatchToProps: Dispatch → Props
const mapDispatchToProps = (dispatch) => ({
    increment: () => dispatch({ type: 'INCREMENT' }),
    decrement: () => dispatch({ type: 'DECREMENT' })
});

// 4. connect로 연결
export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Counter);
```

### connect HOC 이해하기

```javascript
// connect는 Higher Order Component (HOC)
// 컴포넌트를 받아서 새로운 컴포넌트를 반환

const ConnectedCounter = connect(
    mapStateToProps,
    mapDispatchToProps
)(Counter);

// 위 코드는 다음과 같음:
function ConnectedCounter(props) {
    const state = useSelector(mapStateToProps);
    const dispatch = useDispatch();
    
    return (
        <Counter
            {...props}
            count={state.count}
            increment={() => dispatch({ type: 'INCREMENT' })}
            decrement={() => dispatch({ type: 'DECREMENT' })}
        />
    );
}
```

**HOC의 장점**:
- 컴포넌트를 Redux와 분리 (테스트 쉬움)
- 재사용 가능한 컴포넌트
- 관심사의 분리 (UI vs 로직)

## mapStateToProps - State를 Props로

### 기본 사용법

```javascript
// Redux State
const state = {
    counter: { count: 0 },
    user: { name: 'Alice', id: 1 },
    todos: [...]
};

// mapStateToProps: 필요한 state만 추출
const mapStateToProps = (state) => ({
    count: state.counter.count,
    userName: state.user.name
});

// Counter 컴포넌트에서 props로 받음
function Counter({ count, userName }) {
    return <div>Count: {count}, User: {userName}</div>;
}
```

### ownProps 활용

```javascript
// ownProps: 컴포넌트가 받은 props
function TodoItem({ todoId }) {
    return <div>...</div>;
}

const mapStateToProps = (state, ownProps) => {
    const todo = state.todos.find(t => t.id === ownProps.todoId);
    return {
        todo: todo,
        isCompleted: todo?.completed || false
    };
};

export default connect(mapStateToProps)(TodoItem);

// 사용
<TodoItem todoId={1} />
```

### Selector 함수 사용

```javascript
// selectors.js - 재사용 가능한 selector
export const getCount = (state) => state.counter.count;
export const getTodos = (state) => state.todos;
export const getCompletedTodos = (state) => 
    state.todos.filter(todo => todo.completed);

// mapStateToProps에서 사용
import { getCount, getCompletedTodos } from './selectors';

const mapStateToProps = (state) => ({
    count: getCount(state),
    completedTodos: getCompletedTodos(state)
});
```

### 성능 최적화: 메모이제이션

```javascript
import { createSelector } from 'reselect';

// ❌ 매번 새 배열 생성 (불필요한 리렌더링)
const mapStateToProps = (state) => ({
    completedTodos: state.todos.filter(t => t.completed) // 항상 새 배열!
});

// ✅ Reselect로 메모이제이션
const getCompletedTodos = createSelector(
    [state => state.todos],
    (todos) => todos.filter(t => t.completed)
    // todos가 변경될 때만 재계산
);

const mapStateToProps = (state) => ({
    completedTodos: getCompletedTodos(state)
});
```

## mapDispatchToProps - Action Dispatch

### 기본 사용법

```javascript
// 방법 1: 함수 형태
const mapDispatchToProps = (dispatch) => ({
    increment: () => dispatch({ type: 'INCREMENT' }),
    decrement: () => dispatch({ type: 'DECREMENT' }),
    incrementBy: (amount) => dispatch({ 
        type: 'INCREMENT_BY', 
        payload: amount 
    })
});

// 방법 2: 객체 형태 (간편!)
import { increment, decrement, incrementBy } from './actions';

const mapDispatchToProps = {
    increment,
    decrement,
    incrementBy
};

// 두 방법 모두 결과는 같음
```

### Action Creator 활용

```javascript
// actions.js
export const addTodo = (text) => ({
    type: 'ADD_TODO',
    payload: {
        id: Date.now(),
        text,
        completed: false
    }
});

export const toggleTodo = (id) => ({
    type: 'TOGGLE_TODO',
    payload: id
});

export const removeTodo = (id) => ({
    type: 'REMOVE_TODO',
    payload: id
});

// TodoList.js
import { addTodo, toggleTodo, removeTodo } from './actions';

const mapDispatchToProps = {
    addTodo,
    toggleTodo,
    removeTodo
};

function TodoList({ todos, addTodo, toggleTodo, removeTodo }) {
    const [text, setText] = useState('');
    
    const handleSubmit = (e) => {
        e.preventDefault();
        addTodo(text);  // dispatch(addTodo(text)) 자동 호출
        setText('');
    };
    
    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input value={text} onChange={e => setText(e.target.value)} />
                <button type="submit">Add</button>
            </form>
            <ul>
                {todos.map(todo => (
                    <li key={todo.id}>
                        <span 
                            onClick={() => toggleTodo(todo.id)}
                            style={{ 
                                textDecoration: todo.completed ? 'line-through' : 'none' 
                            }}
                        >
                            {todo.text}
                        </span>
                        <button onClick={() => removeTodo(todo.id)}>X</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default connect(null, mapDispatchToProps)(TodoList);
```

### ownProps와 함께 사용

```javascript
const mapDispatchToProps = (dispatch, ownProps) => ({
    handleClick: () => {
        dispatch({ type: 'ITEM_CLICKED', payload: ownProps.itemId });
    }
});
```

## 컨테이너 vs 프레젠테이셔널 패턴

### 패턴 개념

```javascript
// ✅ 프레젠테이셔널 컴포넌트 (Presentational)
// - UI만 담당
// - Redux를 모름
// - props로 모든 것을 받음
// - 재사용 가능

function TodoItem({ todo, onToggle, onRemove }) {
    return (
        <li>
            <span 
                onClick={onToggle}
                style={{ 
                    textDecoration: todo.completed ? 'line-through' : 'none' 
                }}
            >
                {todo.text}
            </span>
            <button onClick={onRemove}>X</button>
        </li>
    );
}

// ✅ 컨테이너 컴포넌트 (Container)
// - 로직 담당
// - Redux와 연결
// - 프레젠테이셔널 컴포넌트를 감쌈
// - 재사용 어려움

const mapStateToProps = (state, ownProps) => ({
    todo: state.todos.find(t => t.id === ownProps.todoId)
});

const mapDispatchToProps = (dispatch, ownProps) => ({
    onToggle: () => dispatch(toggleTodo(ownProps.todoId)),
    onRemove: () => dispatch(removeTodo(ownProps.todoId))
});

const TodoItemContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(TodoItem);

export default TodoItemContainer;
```

### 폴더 구조

```
src/
├── components/          # 프레젠테이셔널 컴포넌트
│   ├── TodoItem.js
│   ├── TodoList.js
│   └── TodoForm.js
├── containers/          # 컨테이너 컴포넌트
│   ├── TodoItemContainer.js
│   ├── TodoListContainer.js
│   └── TodoFormContainer.js
├── store/
│   ├── actions/
│   ├── reducers/
│   └── index.js
└── App.js
```

## 실전 예제: Todo 앱

### Redux Store 설정

```javascript
// store/reducers/todosReducer.js
const initialState = {
    todos: [],
    filter: 'all'
};

export default function todosReducer(state = initialState, action) {
    switch (action.type) {
        case 'ADD_TODO':
            return {
                ...state,
                todos: [...state.todos, action.payload]
            };
        
        case 'TOGGLE_TODO':
            return {
                ...state,
                todos: state.todos.map(todo =>
                    todo.id === action.payload
                        ? { ...todo, completed: !todo.completed }
                        : todo
                )
            };
        
        case 'REMOVE_TODO':
            return {
                ...state,
                todos: state.todos.filter(todo => todo.id !== action.payload)
            };
        
        case 'SET_FILTER':
            return { ...state, filter: action.payload };
        
        default:
            return state;
    }
}

// store/index.js
import { createStore } from 'redux';
import todosReducer from './reducers/todosReducer';

const store = createStore(
    todosReducer,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
);

export default store;
```

### Action Creators

```javascript
// store/actions/todoActions.js
export const addTodo = (text) => ({
    type: 'ADD_TODO',
    payload: {
        id: Date.now(),
        text,
        completed: false
    }
});

export const toggleTodo = (id) => ({
    type: 'TOGGLE_TODO',
    payload: id
});

export const removeTodo = (id) => ({
    type: 'REMOVE_TODO',
    payload: id
});

export const setFilter = (filter) => ({
    type: 'SET_FILTER',
    payload: filter
});
```

### 프레젠테이셔널 컴포넌트

```javascript
// components/TodoList.js
import React from 'react';

function TodoList({ todos, onToggle, onRemove }) {
    if (todos.length === 0) {
        return <p>No todos yet!</p>;
    }
    
    return (
        <ul>
            {todos.map(todo => (
                <li key={todo.id}>
                    <span
                        onClick={() => onToggle(todo.id)}
                        style={{
                            textDecoration: todo.completed ? 'line-through' : 'none',
                            cursor: 'pointer'
                        }}
                    >
                        {todo.text}
                    </span>
                    <button onClick={() => onRemove(todo.id)}>Delete</button>
                </li>
            ))}
        </ul>
    );
}

export default TodoList;
```

### 컨테이너 컴포넌트

```javascript
// containers/TodoListContainer.js
import { connect } from 'react-redux';
import TodoList from '../components/TodoList';
import { toggleTodo, removeTodo } from '../store/actions/todoActions';

// Selector: filter에 따라 todos 필터링
const getVisibleTodos = (todos, filter) => {
    switch (filter) {
        case 'completed':
            return todos.filter(t => t.completed);
        case 'active':
            return todos.filter(t => !t.completed);
        default:
            return todos;
    }
};

const mapStateToProps = (state) => ({
    todos: getVisibleTodos(state.todos, state.filter)
});

const mapDispatchToProps = {
    onToggle: toggleTodo,
    onRemove: removeTodo
};

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(TodoList);
```

### App 컴포넌트

```javascript
// App.js
import React from 'react';
import { Provider } from 'react-redux';
import store from './store';
import TodoListContainer from './containers/TodoListContainer';
import TodoFormContainer from './containers/TodoFormContainer';
import FilterContainer from './containers/FilterContainer';

function App() {
    return (
        <Provider store={store}>
            <div className="App">
                <h1>Todo App with Redux</h1>
                <TodoFormContainer />
                <FilterContainer />
                <TodoListContainer />
            </div>
        </Provider>
    );
}

export default App;
```

## 실습 문제 🏋️‍♂️

### 문제 1: Counter 컴포넌트 연결

```javascript
// TODO: Counter 컴포넌트를 Redux에 연결하세요
// State: { count: 0 }
// Actions: increment, decrement, reset

// 답안:
function Counter({ count, increment, decrement, reset }) {
    return (
        <div>
            <h1>{count}</h1>
            <button onClick={increment}>+</button>
            <button onClick={decrement}>-</button>
            <button onClick={reset}>Reset</button>
        </div>
    );
}

const mapStateToProps = (state) => ({
    count: state.count
});

const mapDispatchToProps = (dispatch) => ({
    increment: () => dispatch({ type: 'INCREMENT' }),
    decrement: () => dispatch({ type: 'DECREMENT' }),
    reset: () => dispatch({ type: 'RESET' })
});

export default connect(mapStateToProps, mapDispatchToProps)(Counter);
```

### 문제 2: 사용자 정보 표시

```javascript
// TODO: UserProfile 컴포넌트를 Redux에 연결
// State: { user: { name, email, avatar } }

// 답안:
function UserProfile({ user }) {
    if (!user) return <div>Loading...</div>;
    
    return (
        <div>
            <img src={user.avatar} alt={user.name} />
            <h2>{user.name}</h2>
            <p>{user.email}</p>
        </div>
    );
}

const mapStateToProps = (state) => ({
    user: state.user
});

export default connect(mapStateToProps)(UserProfile);
```

## 흔한 실수 ⚠️

### 실수 1: Provider 위치

```javascript
// ❌ Provider가 App 내부에
function App() {
    return (
        <Provider store={store}>
            <Routes />
        </Provider>
    );
}

// ✅ Provider가 App 외부에
ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById('root')
);
```

### 실수 2: mapStateToProps에서 새 객체/배열 생성

```javascript
// ❌ 매번 새 배열 (불필요한 리렌더링)
const mapStateToProps = (state) => ({
    todos: state.todos.filter(t => t.completed) // 항상 새 배열!
});

// ✅ Selector 사용
import { getCompletedTodos } from './selectors';

const mapStateToProps = (state) => ({
    todos: getCompletedTodos(state) // 메모이제이션
});
```

### 실수 3: connect 파라미터 순서

```javascript
// ❌ 순서 틀림
connect(mapDispatchToProps, mapStateToProps)(Component);

// ✅ 올바른 순서
connect(mapStateToProps, mapDispatchToProps)(Component);
```

## 체크리스트 ✅

- [ ] React-Redux를 설치하고 설정할 수 있다
- [ ] Provider로 Store를 제공할 수 있다
- [ ] connect HOC의 개념을 이해한다
- [ ] mapStateToProps로 State를 Props로 전달할 수 있다
- [ ] mapDispatchToProps로 Action을 dispatch할 수 있다
- [ ] 컨테이너/프레젠테이셔널 패턴을 적용할 수 있다
- [ ] 실습 문제를 모두 해결했다

## 다음 단계 🚀

**다음 챕터**: `12. React-Redux Hooks - useSelector와 useDispatch`에서 더 현대적이고 간편한 Hooks API를 배웁니다!

### 추가 학습 자료
- [React-Redux 공식 문서](https://react-redux.js.org/)
- [connect API Reference](https://react-redux.js.org/api/connect)
- [Container/Presentational Pattern](https://medium.com/@dan_abramov/smart-and-dumb-components-7ca2f9a7c7d0)

---

**핵심 요약**: connect는 강력하지만 다음 챕터에서 배울 Hooks가 더 간단합니다. 하지만 connect의 개념을 이해하면 Redux의 작동 원리를 깊이 이해할 수 있습니다! 💪



