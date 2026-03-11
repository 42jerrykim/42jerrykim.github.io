---
draft: true
title: "[Redux] 13. 컴포넌트 최적화 - 리렌더링 제어"
date: 2025-10-14
lastmod: 2025-10-14
description: "Redux 앱의 성능 최적화 완벽 가이드. React.memo로 불필요한 리렌더링 방지, useMemo와 useCallback으로 연산 최적화, Profiler로 성능 측정하는 실전 최적화 기법을 마스터합니다."
slug: component-optimization
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
  - Event-Driven
  - Benchmark
  - Profiling
  - 프로파일링
  - Functional-Programming
  - 함수형프로그래밍
series: ["Redux 완전 정복"]
series_order: 13
---

12장에서 useSelector·useDispatch로 컴포넌트와 store를 연결했다면, 이 장에서는 **불필요한 리렌더를 줄이는 방법**을 다룹니다. useSelector가 반환하는 참조가 바뀌면 컴포넌트가 리렌더되므로, React.memo·useMemo·useCallback과 **Selector**를 어떻게 조합할지가 실무 성능에 직결됩니다. 14장(Selector 패턴)에서 메모이제이션된 selector를 배우기 전에, "언제 리렌더가 일어나는지"를 이해하는 것이 중요합니다.

## 이 글을 읽은 후 달성해야 할 목표 (평가 기준)

이 챕터를 마치면 다음을 할 수 있어야 합니다:

- React 리렌더링 원리를 설명하고, **useSelector** 사용이 리렌더를 유발하는 조건을 구분할 수 있다.
- **React.memo**, **useMemo**, **useCallback**을 상황에 맞게 적용하고, Redux **Selector**와 조합할 수 있다.
- 언제 메모이제이션을 쓸지·피할지 **판단**할 수 있다.
- ✅ React Profiler로 성능 측정

## 왜 최적화가 필요한가?

**useSelector**를 쓰는 컴포넌트는 선택한 **state**가 바뀔 때만 리렌더되지만, 부모가 리렌더되면 **props**가 바뀌지 않아도 자식이 함께 리렌더되는 것이 React의 기본 동작입니다. 리스트가 길거나 **state**가 자주 바뀌면 불필요한 리렌더가 쌓여 성능이 나빠질 수 있습니다. 이 장에서는 **React.memo**, **useCallback**, **useMemo**와 Redux **Selector** 메모이제이션으로 "언제 리렌더할지"를 좁혀서 최적화하는 방법을 다룹니다. 단, 최적화는 **측정 후** 적용하는 것이 좋습니다. 병목이 없는 곳에 메모이제이션을 남발하면 오히려 메모리와 비교 비용만 늘어납니다.

Redux 앱에서 흔히 발생하는 성능 문제와 해결 방향은 아래와 같습니다.

```javascript
// ❌ 성능 문제: 부모가 리렌더링되면 모든 자식도 리렌더링
function TodoList() {
    const todos = useSelector(state => state.todos); // 1000개
    
    return (
        <div>
            {todos.map(todo => (
                <TodoItem key={todo.id} todo={todo} />
                // todo가 변경되지 않아도 계속 리렌더링!
            ))}
        </div>
    );
}

// ✅ 최적화: 변경된 항목만 리렌더링
const TodoItem = React.memo(function TodoItem({ todo }) {
    return <div>{todo.text}</div>;
});
```

## React 리렌더링 이해하기

React는 **state**나 **props**가 바뀌었을 때, 또는 부모가 리렌더되었을 때 컴포넌트를 다시 그립니다. Redux를 쓰면 **useSelector**가 선택한 **state** 조각이 바뀔 때만 해당 컴포넌트가 리렌더되고, **connect**는 **mapStateToProps** 결과가 바뀔 때만 구독 컴포넌트를 리렌더합니다. 그래도 부모가 리렌더되면 자식은 **props**가 같아도 리렌더되므로, 리스트 아이템처럼 개수가 많은 자식은 **React.memo**로 "props가 같으면 스킵"하도록 할 수 있습니다. 먼저 리렌더가 일어나는 경우를 정리합니다.

### 리렌더링이 발생하는 경우

```javascript
// 1. State 변경
const [count, setCount] = useState(0);
setCount(1); // 리렌더링!

// 2. Props 변경
<Child value={count} /> // count 변경 시 Child 리렌더링

// 3. 부모 컴포넌트 리렌더링
function Parent() {
    const [count, setCount] = useState(0);
    return (
        <div>
            <Child /> {/* Parent 리렌더링 시 Child도 리렌더링 */}
        </div>
    );
}

// 4. Context 값 변경
const value = useContext(MyContext);
// Context 값 변경 시 모든 구독 컴포넌트 리렌더링
```

### Redux에서의 리렌더링

```javascript
// Redux State 변경 시
dispatch({ type: 'INCREMENT' });

// useSelector가 있는 모든 컴포넌트 검사
function Component1() {
    const count = useSelector(state => state.count);
    // count 변경 시 리렌더링
}

function Component2() {
    const user = useSelector(state => state.user);
    // user는 변경 안 됨 → 리렌더링 안 함
}
```

## React.memo - 컴포넌트 메모이제이션

**React.memo**는 **props**를 얕은 비교해서 이전과 같으면 리렌더를 건너뜁니다. 리스트의 각 항목처럼 부모만 리렌더돼도 자식이 불필요하게 많이 리렌더되는 경우에, **todo**·**onToggle** 같은 **props**가 실제로 바뀌지 않았을 때만 스킵하도록 할 때 유용합니다. **props**에 객체나 함수가 있으면 참조가 바뀔 때마다 리렌더되므로, 부모에서 **useCallback**·**useMemo**로 같은 참조를 유지해야 **React.memo** 효과가 납니다.

### 기본 사용법

```javascript
// Before: 항상 리렌더링
function TodoItem({ todo, onToggle }) {
    console.log('TodoItem rendered');
    return (
        <li onClick={() => onToggle(todo.id)}>
            {todo.text}
        </li>
    );
}

// After: Props가 변경될 때만 리렌더링
const TodoItem = React.memo(function TodoItem({ todo, onToggle }) {
    console.log('TodoItem rendered');
    return (
        <li onClick={() => onToggle(todo.id)}>
            {todo.text}
        </li>
    );
});
```

### 커스텀 비교 함수

```javascript
// 기본: 얕은 비교 (shallow comparison)
const TodoItem = React.memo(TodoItem);

// 커스텀: 특정 prop만 비교
const TodoItem = React.memo(
    TodoItem,
    (prevProps, nextProps) => {
        // true 반환 시 리렌더링 스킵
        return prevProps.todo.id === nextProps.todo.id &&
               prevProps.todo.text === nextProps.todo.text &&
               prevProps.todo.completed === nextProps.todo.completed;
    }
);

// 또는 lodash 사용
import { isEqual } from 'lodash';

const TodoItem = React.memo(TodoItem, isEqual);
```

### 실전 예제

```javascript
// 최적화된 Todo 컴포넌트
const TodoItem = React.memo(function TodoItem({ todo, onToggle, onRemove }) {
    console.log(`TodoItem ${todo.id} rendered`);
    
    return (
        <li className={todo.completed ? 'completed' : ''}>
            <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => onToggle(todo.id)}
            />
            <span onClick={() => onToggle(todo.id)}>
                {todo.text}
            </span>
            <button onClick={() => onRemove(todo.id)}>×</button>
        </li>
    );
});

function TodoList() {
    const todos = useSelector(state => state.todos);
    const dispatch = useDispatch();
    
    // ⚠️ 문제: 부모가 리렌더링되면 함수도 재생성
    const handleToggle = (id) => {
        dispatch(toggleTodo(id));
    };
    
    return (
        <ul>
            {todos.map(todo => (
                <TodoItem
                    key={todo.id}
                    todo={todo}
                    onToggle={handleToggle} // 매번 새 함수!
                />
            ))}
        </ul>
    );
}
```

## useCallback - 함수 메모이제이션

**useCallback**은 함수 참조를 **의존성 배열**이 바뀔 때만 새로 만들어 줍니다. **React.memo**로 감싼 자식에 **onToggle** 같은 함수를 **props**로 넘길 때, 부모가 리렌더될 때마다 새 함수가 만들어지면 **props**가 바뀐 것으로 간주되어 **React.memo**가 무력화됩니다. **useCallback**으로 **dispatch** 등만 의존성에 두면, 같은 함수 참조가 유지되어 자식이 불필요하게 리렌더되지 않습니다. 의존성 배열을 잘못 쓰면 오래된 **state**를 참조하는 버그가 나므로, 사용하는 값은 모두 배열에 넣어야 합니다.

### 기본 사용법

```javascript
function TodoList() {
    const dispatch = useDispatch();
    
    // ❌ 매번 새 함수 생성
    const handleToggle = (id) => {
        dispatch(toggleTodo(id));
    };
    
    // ✅ 함수 메모이제이션
    const handleToggle = useCallback((id) => {
        dispatch(toggleTodo(id));
    }, [dispatch]); // dispatch가 변경될 때만 새 함수 생성
    
    const handleRemove = useCallback((id) => {
        dispatch(removeTodo(id));
    }, [dispatch]);
    
    return (
        <ul>
            {todos.map(todo => (
                <TodoItem
                    key={todo.id}
                    todo={todo}
                    onToggle={handleToggle}
                    onRemove={handleRemove}
                />
            ))}
        </ul>
    );
}
```

### 의존성 배열 주의

```javascript
function SearchForm() {
    const [query, setQuery] = useState('');
    const dispatch = useDispatch();
    
    // ❌ query를 의존성에 추가 안 함 → 오래된 값 사용
    const handleSearch = useCallback(() => {
        dispatch(search(query));
    }, [dispatch]);
    
    // ✅ 모든 의존성 포함
    const handleSearch = useCallback(() => {
        dispatch(search(query));
    }, [query, dispatch]);
    
    // ✅ 또는 함수형 업데이트
    const handleSearch = useCallback(() => {
        // 최신 query를 인자로 받음
        setQuery(current => {
            dispatch(search(current));
            return current;
        });
    }, [dispatch]);
}
```

### useCallback vs 인라인 함수

```javascript
// ❌ 항상 useCallback 쓰는 건 오히려 느림
const handleClick = useCallback(() => {
    console.log('clicked');
}, []); // 간단한 함수는 그냥 인라인이 나음

// ✅ useCallback이 필요한 경우
// 1. React.memo 컴포넌트의 prop
const handleToggle = useCallback((id) => {
    dispatch(toggleTodo(id));
}, [dispatch]);

<MemoizedTodoItem onToggle={handleToggle} />

// 2. useEffect 의존성
useEffect(() => {
    handleFetch();
}, [handleFetch]); // handleFetch이 변경될 때만 실행
```

## useMemo - 값 메모이제이션

**useMemo**는 **의존성 배열**이 바뀔 때만 계산을 다시 수행하고, 그 외에는 이전 결과를 재사용합니다. **useSelector**로 가져온 **state**를 **filter**·**sort**·**slice** 같은 연산으로 파생 데이터로 만들 때, 매 렌더마다 새 배열을 만들면 참조가 바뀌어 이를 **props**로 받는 자식이 계속 리렌더됩니다. **useMemo**로 **todos**·**filter**가 바뀔 때만 파생 데이터를 만들면 불필요한 리렌더와 연산을 줄일 수 있습니다. 단, 연산이 가벼우면 **useMemo** 자체의 비용이 더 클 수 있으므로, **비용이 큰 계산**이 있을 때만 쓰는 것이 좋습니다.

### 기본 사용법

```javascript
function TodoStats() {
    const todos = useSelector(state => state.todos);
    
    // ❌ 매번 계산
    const stats = {
        total: todos.length,
        completed: todos.filter(t => t.completed).length,
        active: todos.filter(t => !t.completed).length
    };
    
    // ✅ 메모이제이션: todos가 변경될 때만 재계산
    const stats = useMemo(() => ({
        total: todos.length,
        completed: todos.filter(t => t.completed).length,
        active: todos.filter(t => !t.completed).length
    }), [todos]);
    
    return (
        <div>
            <span>Total: {stats.total}</span>
            <span>Completed: {stats.completed}</span>
            <span>Active: {stats.active}</span>
        </div>
    );
}
```

### 복잡한 연산 최적화

```javascript
function ExpensiveComponent() {
    const data = useSelector(state => state.data);
    const filter = useSelector(state => state.filter);
    
    // ❌ 매번 정렬 (느림)
    const sortedData = data
        .filter(item => item.category === filter)
        .sort((a, b) => b.score - a.score)
        .slice(0, 100);
    
    // ✅ 메모이제이션
    const sortedData = useMemo(() => {
        console.log('Sorting data...');
        return data
            .filter(item => item.category === filter)
            .sort((a, b) => b.score - a.score)
            .slice(0, 100);
    }, [data, filter]);
    
    return (
        <ul>
            {sortedData.map(item => (
                <li key={item.id}>{item.name}</li>
            ))}
        </ul>
    );
}
```

### useMemo vs useCallback

```javascript
// useMemo: 값을 메모이제이션
const value = useMemo(() => computeExpensiveValue(a, b), [a, b]);

// useCallback: 함수를 메모이제이션
const callback = useCallback(() => doSomething(a, b), [a, b]);

// useCallback은 useMemo의 문법 설탕
const callback = useMemo(() => () => doSomething(a, b), [a, b]);
```

## Redux Selector 최적화

**useSelector**에 넘기는 선택자에서 **filter**·**map**처럼 매번 새 배열·객체를 반환하면, 참조가 바뀌어 컴포넌트가 매번 리렌더됩니다. **Reselect**의 **createSelector**는 입력 **state** 조각이 바뀔 때만 파생 결과를 다시 계산하고, 같으면 이전 참조를 반환해 불필요한 리렌더를 막습니다. 여러 필드를 한 객체로 반환할 때는 **useSelector**의 두 번째 인자로 **shallowEqual**을 넘겨 1단계 키만 비교하게 할 수도 있습니다. 아래는 **Reselect**·**shallowEqual**·**Selector Factory** 패턴입니다.

### Reselect 사용

```javascript
import { createSelector } from 'reselect';

// Input Selectors
const selectTodos = state => state.todos;
const selectFilter = state => state.filter;

// Memoized Selector
const selectVisibleTodos = createSelector(
    [selectTodos, selectFilter],
    (todos, filter) => {
        console.log('Computing visible todos');
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
    // todos나 filter가 실제로 변경될 때만 재계산
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

### shallowEqual 사용

```javascript
import { shallowEqual } from 'react-redux';

// ❌ 매번 새 객체 → 항상 리렌더링
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

// ✅ 또는 각각 선택
const name = useSelector(state => state.user.name);
const email = useSelector(state => state.user.email);
```

### Selector Factory 패턴

```javascript
// 매개변수가 있는 Selector
const makeSelectTodoById = () =>
    createSelector(
        [
            state => state.todos,
            (state, todoId) => todoId
        ],
        (todos, todoId) => todos.find(t => t.id === todoId)
    );

function TodoDetail({ todoId }) {
    // 컴포넌트마다 별도의 Selector 인스턴스
    const selectTodo = useMemo(makeSelectTodoById, []);
    const todo = useSelector(state => selectTodo(state, todoId));
    
    return <div>{todo?.text}</div>;
}
```

### 판단 기준: 언제 메모이제이션을 쓸지·피할지

| 상황 | 권장 | 비고 |
|------|------|------|
| **React.memo** | 리스트 항목·차트·무거운 자식이 부모 리렌더로 자주 같이 리렌더될 때 | **props**가 객체·함수면 부모에서 **useCallback**·**useMemo**로 참조 유지 필요 |
| **useCallback** | **React.memo** 자식에 넘기는 핸들러, **useEffect** 의존성에 넣는 함수 | 단순 인라인 핸들러는 **useCallback** 생략 가능 |
| **useMemo** | **useSelector** 결과를 filter/sort 등 무거운 연산으로 파생할 때 | 가벼운 연산은 **useMemo** 생략 |
| **Reselect** | **useSelector** 선택자가 매번 새 배열·객체를 반환할 때 | 입력 **state**가 바뀔 때만 재계산되도록 |

### 한계와 비판적 시각

**과도한 메모이제이션**은 피하는 것이 좋습니다. 모든 컴포넌트에 **React.memo**를 붙이거나, 모든 함수에 **useCallback**을 쓰면 비교 비용과 메모리만 늘어나고, 의존성 배열 실수로 오래된 값을 쓰는 버그가 생기기 쉽습니다. 먼저 **React Profiler**나 **Why Did You Render**로 병목이 있는 컴포넌트를 찾고, 리스트의 자식·무거운 파생 데이터·자주 바뀌는 **props**를 받는 컴포넌트에만 **React.memo**·**useCallback**·**useMemo**·**Reselect**를 적용하는 것이 안전합니다.

## 실전 최적화 예제

아래는 **React.memo**·**useCallback**·**useMemo**·**Reselect**·**shallowEqual**을 한 Todo 앱에 모두 적용한 예입니다. 실제로는 측정 후 필요한 부분만 골라 적용하는 것이 좋습니다.

### 완전히 최적화된 Todo 앱

```javascript
import React, { useCallback, useMemo } from 'react';
import { useSelector, useDispatch, shallowEqual } from 'react-redux';
import { createSelector } from 'reselect';

// Selectors
const selectTodos = state => state.todos;
const selectFilter = state => state.filter;

const selectVisibleTodos = createSelector(
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

const selectStats = createSelector(
    [selectTodos],
    (todos) => ({
        total: todos.length,
        completed: todos.filter(t => t.completed).length,
        active: todos.filter(t => !t.completed).length
    })
);

// 메모이제이션된 TodoItem
const TodoItem = React.memo(function TodoItem({ todo, onToggle, onRemove }) {
    return (
        <li className={todo.completed ? 'completed' : ''}>
            <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => onToggle(todo.id)}
            />
            <span>{todo.text}</span>
            <button onClick={() => onRemove(todo.id)}>×</button>
        </li>
    );
});

// Main Component
function TodoApp() {
    const dispatch = useDispatch();
    
    // Selectors
    const visibleTodos = useSelector(selectVisibleTodos);
    const filter = useSelector(selectFilter);
    const stats = useSelector(selectStats, shallowEqual);
    
    // Memoized Handlers
    const handleToggle = useCallback((id) => {
        dispatch({ type: 'TOGGLE_TODO', payload: id });
    }, [dispatch]);
    
    const handleRemove = useCallback((id) => {
        dispatch({ type: 'REMOVE_TODO', payload: id });
    }, [dispatch]);
    
    const handleFilterChange = useCallback((newFilter) => {
        dispatch({ type: 'SET_FILTER', payload: newFilter });
    }, [dispatch]);
    
    return (
        <div>
            {/* Stats */}
            <div className="stats">
                <span>Total: {stats.total}</span>
                <span>Completed: {stats.completed}</span>
                <span>Active: {stats.active}</span>
            </div>
            
            {/* Filters */}
            <FilterButtons
                current={filter}
                onChange={handleFilterChange}
            />
            
            {/* Todo List */}
            <ul>
                {visibleTodos.map(todo => (
                    <TodoItem
                        key={todo.id}
                        todo={todo}
                        onToggle={handleToggle}
                        onRemove={handleRemove}
                    />
                ))}
            </ul>
        </div>
    );
}

// 필터 버튼도 메모이제이션
const FilterButtons = React.memo(function FilterButtons({ current, onChange }) {
    const filters = ['all', 'active', 'completed'];
    
    return (
        <div className="filters">
            {filters.map(filter => (
                <button
                    key={filter}
                    onClick={() => onChange(filter)}
                    className={current === filter ? 'active' : ''}
                >
                    {filter}
                </button>
            ))}
        </div>
    );
});

export default TodoApp;
```

## 성능 측정

### React Profiler

```javascript
import { Profiler } from 'react';

function onRenderCallback(
    id,       // Profiler id
    phase,    // "mount" | "update"
    actualDuration,  // 렌더링 시간
    baseDuration,    // 메모이제이션 없이 걸린 시간
    startTime,
    commitTime,
    interactions
) {
    console.log(`${id} ${phase}:`, actualDuration);
}

<Profiler id="TodoApp" onRender={onRenderCallback}>
    <TodoApp />
</Profiler>
```

### Redux DevTools

```javascript
// Time Travel로 성능 테스트
// 1. Action 발송
// 2. DevTools에서 이전 상태로 되돌림
// 3. 다시 앞으로 진행
// 4. 렌더링 성능 확인
```

### Why Did You Render

```javascript
// 설치: npm install @welldone-software/why-did-you-render

// index.js
import whyDidYouRender from '@welldone-software/why-did-you-render';

if (process.env.NODE_ENV === 'development') {
    whyDidYouRender(React, {
        trackAllPureComponents: true,
    });
}

// 컴포넌트에 표시
TodoItem.whyDidYouRender = true;
```

## 체크리스트 ✅

- [ ] React 리렌더링 원리를 이해한다
- [ ] React.memo로 컴포넌트를 메모이제이션할 수 있다
- [ ] useCallback으로 함수를 메모이제이션할 수 있다
- [ ] useMemo로 값을 메모이제이션할 수 있다
- [ ] Reselect로 Selector를 최적화할 수 있다
- [ ] Profiler로 성능을 측정할 수 있다

## 다음 단계 🚀

**다음 챕터**: `14. 데이터 선택자 - Selector 패턴`에서 Reselect를 깊이 있게 학습하고 복잡한 데이터 변환을 효율적으로 처리합니다!

### 추가 학습 자료
- [React 성능 최적화](https://ko.reactjs.org/docs/optimizing-performance.html)
- [Reselect 공식 문서](https://github.com/reduxjs/reselect)
- [React Profiler](https://ko.reactjs.org/docs/profiler.html)

---

**핵심 요약**: 최적화는 측정 후에! Profiler로 병목을 찾고, 필요한 곳에만 React.memo, useCallback, useMemo를 적용하세요! 💪




