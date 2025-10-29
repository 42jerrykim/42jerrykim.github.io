---
draft: true
title: "[Redux] 13. 컴포넌트 최적화 - 리렌더링 제어"
date: 2025-10-14
lastmod: 2025-10-14
tags: ["Redux", "React", "Performance", "Optimization", "성능최적화", "리렌더링", "Re-rendering", "React.memo", "useMemo", "useCallback", "메모이제이션", "Memoization", "웹개발", "프론트엔드", "리액트", "리덕스", "React Performance", "성능", "최적화기법", "Optimization Techniques", "Profiler", "프로파일러", "DevTools", "개발자도구", "Virtual DOM", "가상돔", "Reconciliation", "재조정", "Pure Components", "순수컴포넌트", "Equality Check", "동등성검사", "shallowEqual", "얕은비교", "Deep Comparison", "깊은비교", "JavaScript", "TypeScript", "개발", "코딩", "Best Practices", "모범사례", "Redux Patterns", "리덕스패턴", "Component Patterns", "컴포넌트패턴", "Performance Monitoring", "성능모니터링", "Bundle Size", "번들사이즈"]
description: "Redux 앱의 성능 최적화 완벽 가이드. React.memo로 불필요한 리렌더링 방지, useMemo와 useCallback으로 연산 최적화, Profiler로 성능 측정하는 실전 최적화 기법을 마스터합니다"
series: ["Redux 완전 정복"]
series_order: 13
---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- ✅ React 리렌더링 원리 이해
- ✅ React.memo로 컴포넌트 메모이제이션
- ✅ useMemo로 값 메모이제이션
- ✅ useCallback으로 함수 메모이제이션
- ✅ Redux Selector 최적화
- ✅ React Profiler로 성능 측정

## 왜 최적화가 필요한가?

Redux 앱에서 성능 문제가 발생하는 경우:

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

## 실전 최적화 예제

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




