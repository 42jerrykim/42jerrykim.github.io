---
draft: true
title: "[Redux] 14. 데이터 선택자 - Selector 패턴"
date: 2025-10-14
lastmod: 2025-10-14
description: "Redux Selector 패턴과 Reselect 라이브러리 완벽 마스터. 효율적인 데이터 선택, 메모이제이션으로 성능 향상, Selector 조합으로 재사용 가능한 로직 작성법을 실전 예제로 학습합니다."
slug: selector-patterns
tags:
  - JavaScript
  - TypeScript
  - React
  - Frontend
  - 프론트엔드
  - Web
  - 웹
  - Memoization
  - Performance
  - 성능
  - Optimization
  - 최적화
  - Caching
  - 캐싱
  - Cache
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
series_order: 14
---

13장에서 리렌더 원리와 React.memo·useMemo를 봤다면, 이 장에서는 **Selector 패턴**으로 "store에서 필요한 값만 골라 쓰는" 방법과 **Reselect**로 메모이제이션된 selector를 만드는 방법을 다룹니다. state가 커질수록 "일부만 바뀌었는데 selector가 매번 새 참조를 반환해 리렌더가 난다"는 문제를 막으려면 이 장의 패턴이 필수입니다. 15장(실습)에서 Counter·Todo 앱을 만들 때 바로 적용할 수 있습니다.

## 이 글을 읽은 후 달성해야 할 목표 (평가 기준)

이 챕터를 마치면 다음을 할 수 있어야 합니다:

- **Selector** 패턴의 개념과 **메모이제이션**으로 불필요한 리렌더를 줄이는 원리를 설명할 수 있다.
- Reselect로 **메모이제이션**된 **Selector**를 작성하고, Input/Output **Selector**를 조합할 수 있다.
- 정규화된 **State**에서 데이터를 선택하고, Parametric **Selector**·Selector Factory를 적용할 수 있다.

## Selector란 무엇인가?

**Selector**는 **Redux** **Store**의 **state**에서 컴포넌트가 필요한 데이터를 추출하는 **순수 함수**입니다. **state** 전체를 넘기면 원하는 필드나 파생 데이터(필터링·집계 등)를 반환하도록 작성합니다. Selector를 **useSelector**에 넘기면, React-Redux는 선택 결과를 **참조 비교**해서 바뀌었을 때만 리렌더하므로, Selector가 매번 **새 배열·객체**를 반환하면 불필요한 리렌더가 늘어납니다. Selector를 별도 함수로 두면 로직 재사용·테스트·**state** 구조 변경 시 한 곳만 수정할 수 있고, **Reselect**로 메모이제이션하면 참조가 안정되어 성능이 좋아집니다. 아래는 컴포넌트에서 직접 **state**를 다루는 방식과 Selector로 분리하는 방식을 비교한 예입니다.

```javascript
// ❌ 컴포넌트에서 직접 State 접근
function TodoList() {
    const todos = useSelector(state => state.todos);
    const filter = useSelector(state => state.filter);
    
    // 필터링 로직이 컴포넌트에 있음 (재사용 어려움)
    const visibleTodos = todos.filter(todo => {
        if (filter === 'completed') return todo.completed;
        if (filter === 'active') return !todo.completed;
        return true;
    });
}

// ✅ Selector 함수로 분리
// selectors.js
export const selectVisibleTodos = (state) => {
    const { todos, filter } = state;
    switch (filter) {
        case 'completed':
            return todos.filter(t => t.completed);
        case 'active':
            return todos.filter(t => !t.completed);
        default:
            return todos;
    }
};

// 컴포넌트
function TodoList() {
    const visibleTodos = useSelector(selectVisibleTodos);
}
```

**Selector의 장점**:
- 로직 재사용
- 테스트 용이
- **State** 구조 변경 시 한 곳만 수정
- 성능 최적화 가능

## 기본 Selector 패턴

가장 단순한 Selector는 **state**의 한 조각(예: `state.todos`)을 그대로 반환합니다. 파생 값(길이, 필터된 개수 등)도 **state**만 인자로 받아 계산해 반환하는 함수로 두면, 여러 컴포넌트에서 같은 로직을 재사용할 수 있습니다. 다만 **filter**·**map**처럼 매 렌더마다 **새 배열**을 반환하면 **useSelector**가 "바뀌었다"고 보므로, 그런 경우는 다음 절의 **Reselect**로 메모이제이션하는 것이 좋습니다.

### Simple Selector

```javascript
// selectors.js

// 단순 State 선택
export const selectTodos = (state) => state.todos;
export const selectFilter = (state) => state.filter;
export const selectUser = (state) => state.user;

// 계산된 값
export const selectTodoCount = (state) => state.todos.length;

export const selectCompletedCount = (state) => 
    state.todos.filter(t => t.completed).length;

export const selectActiveCount = (state) =>
    state.todos.filter(t => !t.completed).length;

// 사용
function Stats() {
    const total = useSelector(selectTodoCount);
    const completed = useSelector(selectCompletedCount);
    const active = useSelector(selectActiveCount);
    
    return (
        <div>
            <span>Total: {total}</span>
            <span>Completed: {completed}</span>
            <span>Active: {active}</span>
        </div>
    );
}
```

### Derived State (파생 상태)

```javascript
// 여러 State를 조합한 파생 데이터
export const selectVisibleTodos = (state) => {
    const todos = selectTodos(state);
    const filter = selectFilter(state);
    
    switch (filter) {
        case 'completed':
            return todos.filter(t => t.completed);
        case 'active':
            return todos.filter(t => !t.completed);
        default:
            return todos;
    }
};

export const selectTodoStats = (state) => {
    const todos = selectTodos(state);
    
    return {
        total: todos.length,
        completed: todos.filter(t => t.completed).length,
        active: todos.filter(t => !t.completed).length,
        completionRate: todos.length > 0
            ? (todos.filter(t => t.completed).length / todos.length) * 100
            : 0
    };
};
```

파생 **state**는 여러 Selector 결과를 조합해 만듭니다. **selectVisibleTodos**처럼 **todos**와 **filter**를 합쳐 "보이는 목록"을 반환하는 Selector는 **useSelector**에서 자주 쓰입니다. 이때 매번 새 배열을 반환하므로 **Reselect**로 메모이제이션하면 **todos**·**filter**가 바뀔 때만 재계산됩니다.

## Reselect - 메모이제이션 Selector

**Reselect**의 **createSelector**는 "입력 Selector 결과"가 바뀔 때만 "결과 함수"를 실행하고, 그렇지 않으면 이전에 계산한 값을 그대로 반환합니다. **useSelector**는 반환값의 **참조**가 바뀌면 리렌더하므로, **filter**·**map** 결과처럼 매번 새 참조가 나오는 Selector를 **createSelector**로 감싸면 불필요한 리렌더와 연산을 줄일 수 있습니다. Input Selector(입력)와 Result Function(출력 계산)을 나누어 두는 패턴이 핵심입니다.

### Reselect 설치 및 기본 사용

```bash
npm install reselect
```

```javascript
import { createSelector } from 'reselect';

// Input Selectors (메모이제이션 안 됨)
const selectTodos = (state) => state.todos;
const selectFilter = (state) => state.filter;

// Output Selector (메모이제이션됨!)
export const selectVisibleTodos = createSelector(
    [selectTodos, selectFilter],  // Input Selectors
    (todos, filter) => {          // Result Function
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

// 사용
function TodoList() {
    // todos나 filter가 변경될 때만 재계산!
    const visibleTodos = useSelector(selectVisibleTodos);
}
```

### 메모이제이션 작동 원리

```javascript
// Reselect는 입력값이 같으면 이전 결과를 반환
const selector = createSelector(
    [state => state.todos],
    (todos) => {
        console.log('Calculating...');
        return todos.filter(t => t.completed);
    }
);

// 첫 호출
selector(state); // "Calculating..." 출력, 계산 수행

// 두 번째 호출 (todos 동일)
selector(state); // 아무것도 출력 안 됨, 캐시된 결과 반환!

// 세 번째 호출 (todos 변경됨)
selector(newState); // "Calculating..." 출력, 재계산
```

### 여러 Input Selector

```javascript
// 3개 이상의 Input Selector
const selectTodos = state => state.todos;
const selectFilter = state => state.filter;
const selectSearchQuery = state => state.searchQuery;
const selectSortBy = state => state.sortBy;

export const selectFilteredAndSortedTodos = createSelector(
    [selectTodos, selectFilter, selectSearchQuery, selectSortBy],
    (todos, filter, query, sortBy) => {
        let result = todos;
        
        // 1. 필터링
        if (filter !== 'all') {
            result = result.filter(t => 
                filter === 'completed' ? t.completed : !t.completed
            );
        }
        
        // 2. 검색
        if (query) {
            result = result.filter(t =>
                t.text.toLowerCase().includes(query.toLowerCase())
            );
        }
        
        // 3. 정렬
        result = [...result].sort((a, b) => {
            switch (sortBy) {
                case 'date':
                    return b.createdAt - a.createdAt;
                case 'name':
                    return a.text.localeCompare(b.text);
                default:
                    return 0;
            }
        });
        
        return result;
    }
);
```

## Selector 조합 (Composition)

### Selector를 조합하여 재사용

```javascript
// Base Selectors
const selectTodos = state => state.todos;
const selectFilter = state => state.filter;

// Level 1: 필터링된 Todos
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

// Level 2: 필터링된 Todos의 통계
export const selectVisibleTodoStats = createSelector(
    [selectVisibleTodos],  // 다른 Selector 재사용!
    (visibleTodos) => ({
        count: visibleTodos.length,
        completed: visibleTodos.filter(t => t.completed).length,
        active: visibleTodos.filter(t => !t.completed).length
    })
);

// Level 3: 우선순위별 그룹핑
export const selectVisibleTodosByPriority = createSelector(
    [selectVisibleTodos],
    (visibleTodos) => {
        return {
            high: visibleTodos.filter(t => t.priority === 'high'),
            medium: visibleTodos.filter(t => t.priority === 'medium'),
            low: visibleTodos.filter(t => t.priority === 'low')
        };
    }
);
```

### 정규화된 State에서 Selector

```javascript
// State 구조
const state = {
    todos: {
        byId: {
            '1': { id: '1', text: 'Learn Redux', userId: 'a' },
            '2': { id: '2', text: 'Build App', userId: 'b' }
        },
        allIds: ['1', '2']
    },
    users: {
        byId: {
            'a': { id: 'a', name: 'Alice' },
            'b': { id: 'b', name: 'Bob' }
        },
        allIds: ['a', 'b']
    }
};

// Selectors
const selectTodosById = state => state.todos.byId;
const selectTodoIds = state => state.todos.allIds;
const selectUsersById = state => state.users.byId;

// 정규화된 todos를 배열로 변환
export const selectTodosList = createSelector(
    [selectTodosById, selectTodoIds],
    (todosById, ids) => ids.map(id => todosById[id])
);

// Todo에 User 정보 결합
export const selectTodosWithUsers = createSelector(
    [selectTodosList, selectUsersById],
    (todos, usersById) => {
        return todos.map(todo => ({
            ...todo,
            user: usersById[todo.userId]
        }));
    }
);

// 특정 User의 Todos
const selectUserId = (state, userId) => userId;

export const selectTodosByUser = createSelector(
    [selectTodosList, selectUserId],
    (todos, userId) => todos.filter(t => t.userId === userId)
);
```

## Parametric Selector (매개변수가 있는 Selector)

**매개변수**가 있는 Selector(예: `todoId`로 Todo 하나만 고르기)는 **useSelector**에 그대로 넘기기 어렵습니다. 인라인으로 `state => state.todos.find(t => t.id === todoId)`를 넘기면 매 렌더마다 **새 함수**가 생성되어 Reselect의 캐시가 동작하지 않습니다. **Selector Factory**(함수가 Selector를 반환)나 **re-reselect**의 **createCachedSelector**로 **todoId**별로 캐시를 두거나, **useCallback**으로 선택자 함수 참조를 고정하는 방식을 씁니다.

### 문제점

```javascript
// ❌ 매번 새 함수 생성 → 캐시 안 됨
function TodoDetail({ todoId }) {
    const todo = useSelector(state =>
        state.todos.find(t => t.id === todoId)
    );
    // todoId가 같아도 매번 새 함수이므로 캐시 안 됨!
}
```

### 해결 방법 1: Selector Factory

```javascript
// Selector Factory
export const makeSelectTodoById = () =>
    createSelector(
        [
            state => state.todos,
            (state, todoId) => todoId
        ],
        (todos, todoId) => todos.find(t => t.id === todoId)
    );

// 컴포넌트
function TodoDetail({ todoId }) {
    // 컴포넌트마다 별도의 selector 인스턴스
    const selectTodoById = useMemo(makeSelectTodoById, []);
    
    const todo = useSelector(state => 
        selectTodoById(state, todoId)
    );
    
    return <div>{todo?.text}</div>;
}
```

### 해결 방법 2: createCachedSelector (Re-reselect)

```bash
npm install re-reselect
```

```javascript
import createCachedSelector from 're-reselect';

// 여러 매개변수에 대해 각각 캐시
export const selectTodoById = createCachedSelector(
    [
        state => state.todos,
        (state, todoId) => todoId
    ],
    (todos, todoId) => todos.find(t => t.id === todoId)
)(
    (state, todoId) => todoId  // Cache key
);

// 사용
function TodoDetail({ todoId }) {
    const todo = useSelector(state => selectTodoById(state, todoId));
    // todoId별로 캐시됨!
}
```

### 해결 방법 3: useCallback

```javascript
function TodoDetail({ todoId }) {
    const selectTodo = useCallback(
        state => state.todos.find(t => t.id === todoId),
        [todoId]
    );
    
    const todo = useSelector(selectTodo);
    
    return <div>{todo?.text}</div>;
}
```

### 일반 Selector vs 메모이제이션 Selector 한눈에 보기

| 구분 | 일반 Selector (순수 함수) | 메모이제이션 Selector (Reselect) |
|------|---------------------------|-----------------------------------|
| **반환** | 매 호출마다 새 참조 가능 (filter/map 등) | 입력이 같으면 이전 참조 반환 |
| **useSelector** | 참조가 바뀌면 리렌더 | 참조가 안정되어 불필요한 리렌더 감소 |
| **사용 시점** | 단순 필드 선택, 재사용·테스트 목적 | 파생 데이터(필터·정렬·집계) 계산 |
| **비용** | 없음 | 비교·캐시 메모리 |

### 판단 기준과 비판적 시각

**단순 필드 선택**(예: `state => state.todos`)은 **createSelector** 없이 써도 됩니다. **파생 데이터**를 만드는 Selector는 **createSelector**로 메모이제이션하는 것이 좋고, **매개변수**가 있으면 Factory·**createCachedSelector**·**useCallback** 중 하나로 "선택자 참조"를 안정시키는 것이 좋습니다. 한편 Selector를 과도하게 쪼개거나 모든 것을 메모이제이션하면 코드만 복잡해지고, **state**가 작거나 리렌더 비용이 낮으면 효과가 미미할 수 있습니다. **state** 구조가 복잡해지고, 리스트·필터·통계가 한 화면에 많아질 때 Selector 패턴과 Reselect를 도입하는 것이 적절합니다.

## 고급 Selector 패턴

### 기본값 처리

```javascript
export const selectUser = createSelector(
    [state => state.user],
    (user) => user || { name: 'Guest', id: null }
);

export const selectTodoById = (todoId) => createSelector(
    [state => state.todos],
    (todos) => todos.find(t => t.id === todoId) || null
);
```

### 조건부 Selector

```javascript
export const selectTodosByStatus = createSelector(
    [
        state => state.todos,
        state => state.filter,
        state => state.showCompleted
    ],
    (todos, filter, showCompleted) => {
        let result = todos;
        
        if (!showCompleted) {
            result = result.filter(t => !t.completed);
        }
        
        if (filter && filter !== 'all') {
            result = result.filter(t => t.category === filter);
        }
        
        return result;
    }
);
```

### 복잡한 데이터 변환

```javascript
// 중첩된 데이터를 Flat하게
export const selectFlatComments = createSelector(
    [state => state.comments],
    (comments) => {
        const flatten = (items, parentId = null) => {
            return items.reduce((acc, item) => {
                acc.push({ ...item, parentId });
                if (item.replies) {
                    acc.push(...flatten(item.replies, item.id));
                }
                return acc;
            }, []);
        };
        
        return flatten(comments);
    }
);

// 트리 구조 생성
export const selectCommentTree = createSelector(
    [selectFlatComments],
    (flatComments) => {
        const buildTree = (items, parentId = null) => {
            return items
                .filter(item => item.parentId === parentId)
                .map(item => ({
                    ...item,
                    children: buildTree(items, item.id)
                }));
        };
        
        return buildTree(flatComments);
    }
);
```

## TypeScript와 Selector

### 타입 안전한 Selector

```typescript
// types.ts
export interface RootState {
    todos: Todo[];
    filter: FilterType;
    user: User | null;
}

export interface Todo {
    id: string;
    text: string;
    completed: boolean;
    userId: string;
}

// selectors.ts
import { createSelector } from 'reselect';
import { RootState, Todo } from './types';

// Input Selector with types
const selectTodos = (state: RootState): Todo[] => state.todos;
const selectFilter = (state: RootState): FilterType => state.filter;

// Output Selector
export const selectVisibleTodos = createSelector(
    [selectTodos, selectFilter],
    (todos: Todo[], filter: FilterType): Todo[] => {
        // 타입 체크됨!
        return todos.filter(todo => {
            // ...
        });
    }
);

// Parametric Selector
export const selectTodoById = (todoId: string) =>
    createSelector(
        [selectTodos],
        (todos: Todo[]): Todo | undefined =>
            todos.find(t => t.id === todoId)
    );
```

### Typed Hooks

```typescript
// hooks/useTypedSelector.ts
import { TypedUseSelectorHook, useSelector } from 'react-redux';
import { RootState } from '../types';

export const useTypedSelector: TypedUseSelectorHook<RootState> = useSelector;

// 사용
import { useTypedSelector } from './hooks/useTypedSelector';
import { selectVisibleTodos } from './selectors';

function TodoList() {
    // 타입 자동 추론!
    const todos = useTypedSelector(selectVisibleTodos);
    // todos의 타입은 Todo[]
}
```

## 실전 Selector 예제

```javascript
// selectors/todoSelectors.js
import { createSelector } from 'reselect';

// Input Selectors
const selectTodosById = state => state.todos.byId;
const selectTodoIds = state => state.todos.allIds;
const selectUsersById = state => state.users.byId;
const selectFilter = state => state.filter;
const selectSearchQuery = state => state.searchQuery;
const selectSortBy = state => state.sortBy;

// Level 1: 정규화된 데이터를 배열로
export const selectAllTodos = createSelector(
    [selectTodosById, selectTodoIds],
    (todosById, ids) => ids.map(id => todosById[id])
);

// Level 2: User 정보 추가
export const selectTodosWithUsers = createSelector(
    [selectAllTodos, selectUsersById],
    (todos, usersById) => todos.map(todo => ({
        ...todo,
        user: usersById[todo.userId]
    }))
);

// Level 3: 필터링
export const selectFilteredTodos = createSelector(
    [selectTodosWithUsers, selectFilter, selectSearchQuery],
    (todos, filter, query) => {
        let result = todos;
        
        // Status 필터
        if (filter !== 'all') {
            result = result.filter(t =>
                filter === 'completed' ? t.completed : !t.completed
            );
        }
        
        // 검색
        if (query) {
            result = result.filter(t =>
                t.text.toLowerCase().includes(query.toLowerCase()) ||
                t.user.name.toLowerCase().includes(query.toLowerCase())
            );
        }
        
        return result;
    }
);

// Level 4: 정렬
export const selectSortedTodos = createSelector(
    [selectFilteredTodos, selectSortBy],
    (todos, sortBy) => {
        const sorted = [...todos];
        
        switch (sortBy) {
            case 'date':
                return sorted.sort((a, b) => b.createdAt - a.createdAt);
            case 'name':
                return sorted.sort((a, b) => a.text.localeCompare(b.text));
            case 'user':
                return sorted.sort((a, b) => 
                    a.user.name.localeCompare(b.user.name)
                );
            default:
                return sorted;
        }
    }
);

// Level 5: 통계
export const selectTodoStats = createSelector(
    [selectFilteredTodos],
    (todos) => ({
        total: todos.length,
        byUser: todos.reduce((acc, todo) => {
            const userName = todo.user.name;
            acc[userName] = (acc[userName] || 0) + 1;
            return acc;
        }, {}),
        byStatus: {
            completed: todos.filter(t => t.completed).length,
            active: todos.filter(t => !t.completed).length
        }
    })
);

// 사용
function TodoDashboard() {
    const todos = useSelector(selectSortedTodos);
    const stats = useSelector(selectTodoStats);
    
    return (
        <div>
            <h2>총 {stats.total}개</h2>
            <ul>
                {todos.map(todo => (
                    <li key={todo.id}>
                        {todo.text} by {todo.user.name}
                    </li>
                ))}
            </ul>
        </div>
    );
}
```

## 실습 문제 🏋️‍♂️

### 문제 1: 기본 Selector 작성
```javascript
// TODO: 완료된 Todo의 개수를 반환하는 Selector

// 답안:
export const selectCompletedCount = createSelector(
    [state => state.todos],
    (todos) => todos.filter(t => t.completed).length
);
```

### 문제 2: 조합 Selector
```javascript
// TODO: 
// 1. 카테고리별 Todo 필터링 Selector
// 2. 필터링된 Todo를 날짜순 정렬 Selector

// 답안:
const selectTodos = state => state.todos;
const selectCategory = state => state.category;

export const selectTodosByCategory = createSelector(
    [selectTodos, selectCategory],
    (todos, category) => {
        if (category === 'all') return todos;
        return todos.filter(t => t.category === category);
    }
);

export const selectSortedTodosByCategory = createSelector(
    [selectTodosByCategory],
    (todos) => [...todos].sort((a, b) => b.createdAt - a.createdAt)
);
```

## 체크리스트 ✅

- [ ] Selector 패턴의 장점을 이해한다
- [ ] createSelector로 메모이제이션 Selector를 만들 수 있다
- [ ] Input/Output Selector를 구분할 수 있다
- [ ] Selector를 조합하여 재사용할 수 있다
- [ ] 매개변수가 있는 Selector를 작성할 수 있다
- [ ] 정규화된 State에서 데이터를 선택할 수 있다

## 다음 단계 🚀

**다음 챕터**: `15. 실습: Counter와 Todo 앱 만들기`에서 지금까지 배운 모든 내용을 종합하여 완전한 앱을 만들어봅니다!

### 추가 학습 자료
- [Reselect 공식 문서](https://github.com/reduxjs/reselect)
- [Re-reselect](https://github.com/toomuchdesign/re-reselect)
- [Redux Selector 패턴](https://redux.js.org/usage/deriving-data-selectors)

---

**핵심 요약**: Selector는 Redux 앱의 성능과 유지보수성을 크게 향상시킵니다. Reselect로 메모이제이션하고 조합하여 사용하세요! 💪




