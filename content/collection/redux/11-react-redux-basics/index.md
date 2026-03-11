---
draft: true
title: "[Redux] 11. React-Redux 시작하기 - Provider와 connect"
date: 2025-10-14
lastmod: 2025-10-14
description: "React와 Redux를 연결하는 React-Redux 라이브러리 완벽 마스터. Provider로 Store 제공, connect HOC로 컴포넌트 연결, mapStateToProps와 mapDispatchToProps 패턴을 실전 예제로 학습합니다."
slug: react-redux-basics
tags:
  - JavaScript
  - TypeScript
  - React
  - Frontend
  - 프론트엔드
  - Web
  - 웹
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
  - Adapter
  - Facade
  - Proxy
series: ["Redux 완전 정복"]
series_order: 11
---

Phase 3의 첫 장으로 **React와 Redux를 연결**하는 방법을 다룹니다. 지금까지는 Redux만으로 store·reducer·dispatch를 배웠지만, 실제 화면은 React 컴포넌트이므로 **Provider**로 store를 앱에 넣고, **connect** 또는 훅으로 컴포넌트가 state를 읽고 action을 보내게 해야 합니다. 이 장에서는 Provider 설정과 connect(mapStateToProps, mapDispatchToProps) 패턴을 익히면 12장(훅)에서 더 간단한 useSelector·useDispatch로 이어집니다.

## 이 글을 읽은 후 달성해야 할 목표 (평가 기준)

이 챕터를 마치면 다음을 할 수 있어야 합니다:

- React-Redux를 설치하고 **Provider**로 Redux **Store**를 React 앱에 제공할 수 있다.
- **connect** HOC로 컴포넌트와 Redux를 연결하고, mapStateToProps·mapDispatchToProps를 구분할 수 있다.
- **State**를 Props로, **Action** 발송 함수를 Props로 전달하는 패턴을 적용할 수 있다.

## 왜 React-Redux가 필요한가?

**Redux**는 UI 라이브러리와 무관하게 동작하는 **상태** 관리 라이브러리입니다. **Store**를 만들고 **dispatch**·**subscribe**를 호출하는 API는 있지만, React 컴포넌트가 **Store**를 어떻게 구독하고, **상태**가 바뀔 때만 리렌더되게 하려면 React와 연결하는 레이어가 필요합니다. 그 역할을 하는 공식 바인딩이 **React-Redux**입니다.

React만 쓴다면 **Context API**로 전역 **상태**를 넘길 수는 있습니다. 다만 Context는 값이 바뀔 때 해당 Context를 쓰는 **모든** 컴포넌트가 리렌더될 수 있어서, **Store**의 일부만 바뀌었을 때 불필요한 리렌더가 많아질 수 있습니다. React-Redux는 **구독(subscription)**을 사용해 **선택한 state**가 바뀐 컴포넌트만 리렌더되게 하고, **connect** 또는 **useSelector**로 "어떤 state를 쓸지"를 선언적으로 지정할 수 있게 합니다.

아래처럼 Redux만으로는 React 트리에 **Store**를 넣을 방법이 없고, **Provider**로 한 번 감싼 뒤에야 하위 컴포넌트가 **Store**에 접근할 수 있습니다.

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

**React-Redux**는 Redux **Store**와 React 컴포넌트를 연결하는 공식 바인딩 라이브러리입니다. **Provider**로 **Store**를 주입하고, **connect** 또는 12장의 Hooks로 컴포넌트와 **Store**를 연결합니다.

## React-Redux 설치 및 설정

프로젝트에 **react-redux**와 **redux**를 설치한 뒤, **Store**를 만드는 파일과 **Provider**로 앱을 감싸는 진입점을 둡니다. 아래는 설치 명령과 권장 폴더 구조입니다.

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

**Provider**는 React-Redux가 제공하는 컴포넌트로, **Store**를 React **Context**에 넣어 줍니다. **Provider**로 감싼 트리 안의 모든 컴포넌트는 **connect**나 **useSelector**·**useDispatch**를 통해 같은 **Store**에 접근할 수 있습니다. 앱의 최상위(예: `index.js`의 `ReactDOM.render` 안)에서 한 번만 사용하고, **store** prop으로 생성한 **Store** 인스턴스를 넘깁니다.

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
- Redux **Store**를 React Context에 넣어 줌
- 모든 하위 컴포넌트가 **Store**에 접근 가능
- 앱의 최상위에서 한 번만 사용

내부적으로는 Context의 **Provider**에 **store**를 **value**로 넘기는 형태입니다. 하위에서는 **useContext**로 **store**를 꺼내 **getState**·**dispatch**·**subscribe**를 쓸 수 있지만, 실제로는 **connect**나 Hooks가 이 구독을 대신 처리합니다.

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

**connect**는 **고차 컴포넌트(HOC)**입니다. **Store**의 **상태**와 **dispatch**를 컴포넌트의 **props**로 넘기기 위해 **mapStateToProps**와 **mapDispatchToProps**를 인자로 받고, "Redux와 연결된" 새 컴포넌트를 반환합니다. 프레젠테이셔널 컴포넌트(UI만 담당)는 **Store**를 모르게 두고, **connect**로 감싼 컨테이너에서만 **Store**에 접근하는 패턴이 전통적인 React-Redux 방식입니다. 아래는 **connect**의 기본 사용법입니다.

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

**mapStateToProps**는 **Store**의 **state**를 인자로 받아 컴포넌트에 넘길 **props** 객체를 반환합니다. **mapDispatchToProps**는 **dispatch**를 받아 **Action**을 발송하는 함수들을 **props**로 넘깁니다. 두 함수 모두 **connect**의 첫 번째·두 번째 인자로 넘기면, 반환된 컴포넌트는 **Store** 구독과 **dispatch** 주입을 자동으로 처리합니다.

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

**mapStateToProps**는 **Store**의 **state** 중 컴포넌트에 필요한 부분만 골라 **props**로 넘기는 함수입니다. 이 함수가 반환하는 객체가 바뀔 때만(React-Redux는 얕은 비교) 해당 컴포넌트가 리렌더되므로, **state** 전체가 아니라 필요한 필드만 반환하고, 파생 데이터는 **Reselect**로 메모이제이션하면 불필요한 리렌더를 줄일 수 있습니다. **ownProps**를 두 번째 인자로 받으면 부모가 넘긴 **props**에 따라 **state**를 선택할 수 있습니다.

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

**mapDispatchToProps**는 **dispatch** 함수를 컴포넌트가 쓸 수 있는 **props**(보통 **Action Creator**를 호출하는 함수들)로 바꿔 줍니다. 함수 형태로 작성하면 **dispatch**를 인자로 받아 객체를 반환하고, 객체 형태로 **Action Creator**만 나열하면 React-Redux가 **bindActionCreators**로 감싸서 **dispatch**와 연결해 줍니다. 객체 형태가 코드가 짧고, **Action Creator**를 그대로 재사용할 수 있어 많이 사용됩니다.

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

### 판단 기준과 비판적 시각

컨테이너/프레젠테이셔널 분리는 **재사용 가능한 UI**와 **Redux에 묶인 로직**을 나눌 때 유용합니다. 다만 작은 앱에서는 컨테이너가 과하게 늘어나 보일러플레이트가 커질 수 있으므로, "한 컴포넌트에 **connect** 하나"에 집착하기보다는 **관심사가 명확히 갈리는 경우**에만 분리하는 것이 좋습니다. 12장의 **useSelector**·**useDispatch**를 쓰면 컨테이너를 따로 두지 않고도 같은 **Store**를 사용할 수 있어, 신규 코드에서는 Hooks를 쓰는 경우가 많습니다. 기존 **connect** 기반 코드는 유지하면서 새 컴포넌트만 Hooks로 작성하는 식으로 점진적으로 전환해도 됩니다.

## 실전 예제: Todo 앱

아래는 **Provider**·**connect**·**mapStateToProps**·**mapDispatchToProps**를 사용해 Todo 앱을 구성하는 예입니다. **Store** 설정부터 프레젠테이셔널·컨테이너 분리, **App**에서 **Provider**로 감싸기까지 한 번에 따라갈 수 있습니다.

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



