---
draft: true
title: "[Redux] 03. 배열과 객체 다루기 - map, filter, reduce"
date: 2025-10-14
lastmod: 2025-10-14
description: "Redux 상태 관리의 핵심인 배열/객체 조작 메서드 완벽 정복. map, filter, reduce를 활용한 불변성 유지, 고차 함수로 간결한 Reducer 작성법을 실전 예제와 함께 마스터합니다."
slug: array-object-manipulation
tags:
  - JavaScript
  - TypeScript
  - React
  - Frontend
  - 프론트엔드
  - Web
  - 웹
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Functional-Programming
  - 함수형프로그래밍
  - Data-Structures
  - 자료구조
  - Array
  - 배열
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - State
  - Observer
  - Refactoring
  - 리팩토링
  - Testing
  - 테스트
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - Reference
  - 참고
  - Readability
  - Maintainability
  - Modularity
  - Documentation
  - 문서화
  - Error-Handling
  - 에러처리
  - Pitfalls
  - 함정
  - Edge-Cases
  - 엣지케이스
  - Debugging
  - 디버깅
  - Performance
  - 성능
  - Type-Safety
  - Interface
  - 인터페이스
  - Encapsulation
  - 캡슐화
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
  - JSON
  - API
  - Async
  - 비동기
  - Caching
  - 캐싱
  - Scalability
  - 확장성
  - Deep-Dive
  - Beginner
  - Advanced
  - Event-Driven
  - Workflow
  - 워크플로우
series: ["Redux 완전 정복"]
series_order: 3
---

01·02장에서 변수·함수·객체·배열과 ES6+ 문법을 봤다면, 이 장에서는 **배열을 변환·필터·집계하는 map, filter, reduce**와 Redux reducer에서의 활용을 집중적으로 다룹니다. Redux의 상태 업데이트는 대부분 "기존 배열/객체를 수정하지 않고 새로 만드는" 패턴이라, 이 고차 함수들을 익혀 두면 07·08장의 reducer 코드를 훨씬 쉽게 읽고 작성할 수 있습니다.

## 이 글을 읽은 후 달성해야 할 목표 (평가 기준)

이 챕터를 마치면 다음을 할 수 있어야 합니다:

- **map**, **filter**, **reduce**로 배열을 변환·필터·집계하고, **불변성**을 유지하며 **State**를 업데이트할 수 있다.
- 고차 함수를 조합하여 Redux **Reducer**를 작성하고, 부수 효과 없이 새 **상태**를 반환할 수 있다.

## 왜 배열 메서드가 Redux에 중요한가?

Redux의 상태 업데이트는 대부분 **기존 배열·객체를 수정하지 않고 새로 만드는** 패턴입니다. 그때 쓰는 것이 **map**(특정 항목만 바꾸기), **filter**(항목 제거), **reduce**(집계 또는 하나의 값으로 줄이기)입니다. 아래 코드는 Redux reducer에서 "특정 id의 todo만 completed를 토글하고 나머지는 그대로 두는" 전형적인 패턴입니다. map으로 새 배열을 만들어 반환하면 불변성이 지켜집니다.

```javascript
// Redux Reducer의 전형적인 패턴
case 'TOGGLE_TODO':
    return {
        ...state,
        todos: state.todos.map(todo =>    // map으로 변환
            todo.id === action.payload
                ? { ...todo, completed: !todo.completed }
                : todo
        )
    };

case 'FILTER_COMPLETED':
    return {
        ...state,
        visibleTodos: state.todos.filter(todo => todo.completed)  // filter로 필터링
    };
```

**핵심**: 배열 메서드는 원본을 변경하지 않고 새 배열을 반환 = 불변성 유지!

## map() - 배열 요소 변환

Redux **Reducer**에서 **todos**·**posts** 같은 배열 **state**를 바꿀 때는 원본을 수정하지 않고 **map**으로 **새 배열**을 만들어 반환합니다. 특정 **id**만 **completed**를 바꾸거나 **payload**로 필드를 덮어쓸 때 **map(todo => ...)** 패턴이 핵심입니다. Redux에서 **map**은 불변 업데이트의 기본 도구입니다.

### 기본 사용법

```javascript
const numbers = [1, 2, 3, 4, 5];

// 각 요소를 2배로
const doubled = numbers.map(n => n * 2);
console.log(doubled); // [2, 4, 6, 8, 10]
console.log(numbers); // [1, 2, 3, 4, 5] - 원본 유지!

// 인덱스와 원본 배열 접근
const withIndex = numbers.map((num, index, array) => ({
    value: num,
    index: index,
    total: array.length
}));
// [
//   { value: 1, index: 0, total: 5 },
//   { value: 2, index: 1, total: 5 },
//   ...
// ]
```

### 객체 배열 변환

**state**가 **객체 배열**(예: todos, users)일 때 **map**으로 특정 **id**의 항목만 바꾸고 나머지는 그대로 두는 패턴이 자주 나옵니다. **스프레드**와 함께 **{ ...todo, completed: true }**처럼 필요한 필드만 덮어쓰면 됩니다.

```javascript
const users = [
    { id: 1, firstName: "Alice", lastName: "Kim" },
    { id: 2, firstName: "Bob", lastName: "Lee" }
];

// 전체 이름 추출
const fullNames = users.map(user => `${user.firstName} ${user.lastName}`);
console.log(fullNames); // ["Alice Kim", "Bob Lee"]

// 특정 속성만 추출
const userIds = users.map(user => user.id);
console.log(userIds); // [1, 2]

// 속성 추가/변환
const enrichedUsers = users.map(user => ({
    ...user,
    fullName: `${user.firstName} ${user.lastName}`,
    createdAt: new Date()
}));
```

### Redux에서의 map 활용 ⭐

```javascript
// Todo 완료 토글
case 'TOGGLE_TODO':
    return {
        ...state,
        todos: state.todos.map(todo =>
            todo.id === action.payload.id
                ? { ...todo, completed: !todo.completed }
                : todo
        )
    };

// 여러 필드 업데이트
case 'UPDATE_TODO':
    return {
        ...state,
        todos: state.todos.map(todo =>
            todo.id === action.payload.id
                ? { ...todo, ...action.payload.updates }
                : todo
        )
    };

// 모든 Todo에 속성 추가
case 'ADD_TIMESTAMP':
    return {
        ...state,
        todos: state.todos.map(todo => ({
            ...todo,
            updatedAt: new Date().toISOString()
        }))
    };

// 조건부 변환
case 'MARK_ALL_COMPLETE':
    return {
        ...state,
        todos: state.todos.map(todo => ({ ...todo, completed: true }))
    };
```

## filter() - 조건부 필터링

**Reducer**에서 항목 **삭제**(REMOVE_TODO)나 **필터링**(완료/미완료만 보기)할 때 **filter**로 조건에 맞는 요소만 남긴 **새 배열**을 반환합니다. **원본 배열을 변경하지 않으므로** 불변성이 유지되고, Redux가 **참조 비교**로 변경을 감지할 수 있습니다.

### 기본 사용법

```javascript
const numbers = [1, 2, 3, 4, 5, 6];

// 짝수만 필터링
const evens = numbers.filter(n => n % 2 === 0);
console.log(evens); // [2, 4, 6]

// 3보다 큰 수
const greaterThanThree = numbers.filter(n => n > 3);
console.log(greaterThanThree); // [4, 5, 6]

// 인덱스 활용
const oddIndices = numbers.filter((n, index) => index % 2 === 1);
console.log(oddIndices); // [2, 4, 6]
```

### 객체 배열 필터링

```javascript
const users = [
    { id: 1, name: "Alice", age: 25, active: true },
    { id: 2, name: "Bob", age: 30, active: false },
    { id: 3, name: "Charlie", age: 35, active: true }
];

// active 사용자만
const activeUsers = users.filter(user => user.active);

// 30세 이상
const adults = users.filter(user => user.age >= 30);

// 복합 조건
const youngActiveUsers = users.filter(
    user => user.age < 30 && user.active
);

// 특정 ID 제외
const withoutUser2 = users.filter(user => user.id !== 2);
```

### Redux에서의 filter 활용 ⭐

```javascript
// Todo 삭제
case 'REMOVE_TODO':
    return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.payload)
    };

// 완료된 Todo만 보기
case 'SHOW_COMPLETED':
    return {
        ...state,
        visibleTodos: state.todos.filter(todo => todo.completed)
    };

// 미완료 Todo만
case 'SHOW_ACTIVE':
    return {
        ...state,
        visibleTodos: state.todos.filter(todo => !todo.completed)
    };

// 검색 필터
case 'SEARCH_TODOS':
    return {
        ...state,
        visibleTodos: state.todos.filter(todo =>
            todo.text.toLowerCase().includes(action.payload.toLowerCase())
        )
    };

// 여러 조건
case 'FILTER_TODOS':
    const { status, tag } = action.payload;
    return {
        ...state,
        visibleTodos: state.todos.filter(todo => {
            const statusMatch = status === 'all' || 
                (status === 'completed' ? todo.completed : !todo.completed);
            const tagMatch = !tag || todo.tags.includes(tag);
            return statusMatch && tagMatch;
        })
    };
```

## reduce() - 배열을 하나의 값으로 축소

**Reducer**라는 이름은 Redux **Reducer**와 같은 "하나의 값으로 줄인다"는 의미에서 왔습니다. Redux에서는 **reduce**로 **배열을 byId/allIds 형태로 정규화**하거나, **합계·개수** 같은 파생 값을 한 번에 계산할 때 씁니다. **map**·**filter**로는 표현하기 어려운 "배열 → 하나의 값" 변환에 **reduce**를 사용합니다.

### 기본 사용법

```javascript
const numbers = [1, 2, 3, 4, 5];

// 합계
const sum = numbers.reduce((acc, num) => acc + num, 0);
console.log(sum); // 15

// 곱셈
const product = numbers.reduce((acc, num) => acc * num, 1);
console.log(product); // 120

// 최댓값
const max = numbers.reduce((acc, num) => Math.max(acc, num));
console.log(max); // 5

// 동작 과정 이해
numbers.reduce((acc, num) => {
    console.log(`acc: ${acc}, num: ${num}`);
    return acc + num;
}, 0);
// acc: 0, num: 1   -> 1
// acc: 1, num: 2   -> 3
// acc: 3, num: 3   -> 6
// acc: 6, num: 4   -> 10
// acc: 10, num: 5  -> 15
```

### 객체/배열 생성

```javascript
const users = [
    { id: 1, name: "Alice", role: "admin" },
    { id: 2, name: "Bob", role: "user" },
    { id: 3, name: "Charlie", role: "admin" }
];

// ID를 키로 하는 객체 생성
const usersById = users.reduce((acc, user) => {
    acc[user.id] = user;
    return acc;
}, {});
// { 
//   '1': { id: 1, name: "Alice", role: "admin" },
//   '2': { id: 2, name: "Bob", role: "user" },
//   '3': { id: 3, name: "Charlie", role: "admin" }
// }

// 역할별 그룹핑
const usersByRole = users.reduce((acc, user) => {
    const { role } = user;
    if (!acc[role]) {
        acc[role] = [];
    }
    acc[role].push(user);
    return acc;
}, {});
// {
//   admin: [{ id: 1, ... }, { id: 3, ... }],
//   user: [{ id: 2, ... }]
// }

// 카운팅
const roleCounts = users.reduce((acc, user) => {
    acc[user.role] = (acc[user.role] || 0) + 1;
    return acc;
}, {});
// { admin: 2, user: 1 }
```

### Redux에서의 reduce 활용 ⭐

```javascript
// 배열을 정규화된 객체로 변환
case 'FETCH_TODOS_SUCCESS':
    const todosById = action.payload.reduce((acc, todo) => {
        acc[todo.id] = todo;
        return acc;
    }, {});
    const allIds = action.payload.map(todo => todo.id);
    
    return {
        ...state,
        todosById,
        allIds,
        loading: false
    };

// 통계 계산
case 'CALCULATE_STATS':
    const stats = state.todos.reduce((acc, todo) => {
        acc.total++;
        if (todo.completed) acc.completed++;
        else acc.active++;
        return acc;
    }, { total: 0, completed: 0, active: 0 });
    
    return { ...state, stats };

// 복잡한 변환
case 'PROCESS_TODOS':
    const processed = state.todos.reduce((acc, todo) => {
        if (todo.priority === 'high') {
            acc.urgent.push(todo);
        } else if (todo.completed) {
            acc.done.push(todo);
        } else {
            acc.pending.push(todo);
        }
        return acc;
    }, { urgent: [], done: [], pending: [] });
    
    return { ...state, ...processed };
```

## 메서드 체이닝 (Method Chaining)

### 기본 체이닝

```javascript
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// 짝수를 골라서 2배로 만들고 합계 구하기
const result = numbers
    .filter(n => n % 2 === 0)     // [2, 4, 6, 8, 10]
    .map(n => n * 2)              // [4, 8, 12, 16, 20]
    .reduce((sum, n) => sum + n, 0); // 60

console.log(result); // 60
```

### 실전 체이닝

```javascript
const todos = [
    { id: 1, text: "Learn JS", completed: true, priority: 'high' },
    { id: 2, text: "Learn Redux", completed: false, priority: 'high' },
    { id: 3, text: "Build App", completed: false, priority: 'low' }
];

// 미완료 고우선순위 Todo의 텍스트 배열
const urgentTexts = todos
    .filter(todo => !todo.completed)
    .filter(todo => todo.priority === 'high')
    .map(todo => todo.text);
// ["Learn Redux"]

// 완료율 계산
const completionRate = todos
    .reduce((acc, todo) => {
        acc.total++;
        if (todo.completed) acc.completed++;
        return acc;
    }, { total: 0, completed: 0 });

const percentage = (completionRate.completed / completionRate.total) * 100;
// 33.33...
```

### Redux Selector 패턴 ⭐

```javascript
// Selector 함수 (상태에서 파생 데이터 생성)
const getVisibleTodos = (state, filter) => {
    return state.todos
        .filter(todo => {
            switch(filter) {
                case 'completed':
                    return todo.completed;
                case 'active':
                    return !todo.completed;
                default:
                    return true;
            }
        })
        .sort((a, b) => {
            // 우선순위 순 정렬
            const priorities = { high: 3, medium: 2, low: 1 };
            return priorities[b.priority] - priorities[a.priority];
        });
};

// 사용
const visibleTodos = getVisibleTodos(state, 'active');

// 복잡한 Selector
const getTodoStats = (state) => {
    return state.todos.reduce((stats, todo) => {
        stats.total++;
        stats.byStatus[todo.completed ? 'completed' : 'active']++;
        stats.byPriority[todo.priority] = (stats.byPriority[todo.priority] || 0) + 1;
        return stats;
    }, {
        total: 0,
        byStatus: { completed: 0, active: 0 },
        byPriority: {}
    });
};
```

## 기타 유용한 배열 메서드

### find() - 첫 번째 일치 요소 찾기

```javascript
const users = [
    { id: 1, name: "Alice" },
    { id: 2, name: "Bob" },
    { id: 3, name: "Charlie" }
];

const user = users.find(u => u.id === 2);
console.log(user); // { id: 2, name: "Bob" }

// Redux에서
case 'SELECT_TODO':
    const selectedTodo = state.todos.find(
        todo => todo.id === action.payload
    );
    return { ...state, selectedTodo };
```

### some() / every()

```javascript
const numbers = [1, 2, 3, 4, 5];

// some: 하나라도 조건 만족?
const hasEven = numbers.some(n => n % 2 === 0);
console.log(hasEven); // true

// every: 모두 조건 만족?
const allPositive = numbers.every(n => n > 0);
console.log(allPositive); // true

// Redux 검증
case 'CHECK_ALL_COMPLETE':
    const allComplete = state.todos.every(todo => todo.completed);
    return { ...state, allComplete };
```

### sort() - 정렬 (⚠️ 원본 변경!)

```javascript
const numbers = [3, 1, 4, 1, 5, 9];

// ❌ 원본 변경
numbers.sort((a, b) => a - b); 

// ✅ 불변성 유지
const sorted = [...numbers].sort((a, b) => a - b);

// Redux에서
case 'SORT_TODOS':
    return {
        ...state,
        todos: [...state.todos].sort((a, b) => {
            // 우선순위 순
            if (a.priority !== b.priority) {
                const priorities = { high: 3, medium: 2, low: 1 };
                return priorities[b.priority] - priorities[a.priority];
            }
            // 같은 우선순위면 이름 순
            return a.text.localeCompare(b.text);
        })
    };
```

## 실습 문제 🏋️‍♂️

### 문제 1: map과 filter 조합
```javascript
const products = [
    { id: 1, name: "Laptop", price: 1000, inStock: true },
    { id: 2, name: "Mouse", price: 20, inStock: true },
    { id: 3, name: "Keyboard", price: 50, inStock: false }
];

// TODO: 재고 있는 상품의 이름만 추출
// 답안:
const availableProducts = products
    .filter(p => p.inStock)
    .map(p => p.name);
// ["Laptop", "Mouse"]
```

### 문제 2: reduce로 객체 변환
```javascript
const todos = [
    { id: 1, text: "Learn JS", completed: true },
    { id: 2, text: "Learn Redux", completed: false },
    { id: 3, text: "Build App", completed: true }
];

// TODO: ID를 키로 하는 객체로 변환
// 답안:
const todosById = todos.reduce((acc, todo) => {
    acc[todo.id] = todo;
    return acc;
}, {});
```

### 문제 3: Redux Reducer 작성
```javascript
// TODO: 다음 Reducer 작성
// 1. COMPLETE_ALL: 모든 todo를 완료 상태로
// 2. REMOVE_COMPLETED: 완료된 todo 모두 삭제
// 3. PRIORITY_FILTER: 특정 우선순위 todo만 필터링

// 답안:
const todoReducer = (state, action) => {
    switch(action.type) {
        case 'COMPLETE_ALL':
            return {
                ...state,
                todos: state.todos.map(todo => ({ 
                    ...todo, 
                    completed: true 
                }))
            };
        
        case 'REMOVE_COMPLETED':
            return {
                ...state,
                todos: state.todos.filter(todo => !todo.completed)
            };
        
        case 'PRIORITY_FILTER':
            return {
                ...state,
                visibleTodos: state.todos.filter(
                    todo => todo.priority === action.payload
                )
            };
        
        default:
            return state;
    }
};
```

### 문제 4: 복잡한 데이터 처리
```javascript
const orders = [
    { id: 1, userId: 'A', total: 100, status: 'completed' },
    { id: 2, userId: 'B', total: 200, status: 'pending' },
    { id: 3, userId: 'A', total: 150, status: 'completed' },
    { id: 4, userId: 'C', total: 300, status: 'completed' }
];

// TODO: 사용자별 완료된 주문 총액 계산
// 예: { A: 250, C: 300 }

// 답안:
const userTotals = orders
    .filter(order => order.status === 'completed')
    .reduce((acc, order) => {
        acc[order.userId] = (acc[order.userId] || 0) + order.total;
        return acc;
    }, {});
```

## 성능 고려사항 ⚡

### 체이닝 vs 단일 reduce
```javascript
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// 체이닝 (배열을 여러 번 순회)
const result1 = numbers
    .filter(n => n % 2 === 0)  // 순회 1
    .map(n => n * 2)           // 순회 2
    .reduce((sum, n) => sum + n, 0); // 순회 3

// 단일 reduce (한 번만 순회)
const result2 = numbers.reduce((sum, n) => {
    if (n % 2 === 0) {
        return sum + (n * 2);
    }
    return sum;
}, 0);

// 둘 다 결과는 같지만 reduce가 더 효율적
```

### 성능 팁
```javascript
// ❌ 불필요한 중간 배열 생성
const result = todos
    .map(t => ({ ...t, processed: true }))
    .filter(t => t.active)
    .map(t => t.name);

// ✅ filter 먼저 (배열 크기 줄이기)
const result = todos
    .filter(t => t.active)
    .map(t => t.name);
```

## 체크리스트 ✅

- [ ] map으로 배열 요소를 변환할 수 있다
- [ ] filter로 조건부 필터링을 할 수 있다
- [ ] reduce로 배열을 단일 값/객체로 변환할 수 있다
- [ ] 메서드 체이닝을 효과적으로 사용할 수 있다
- [ ] Redux에서 불변성을 유지하며 배열을 조작할 수 있다
- [ ] find, some, every 등 다른 메서드도 활용할 수 있다
- [ ] 실습 문제를 모두 해결했다

## 다음 단계 🚀

**다음 챕터**: `04. 비동기 JavaScript - Promise와 async/await`에서는 Redux에서 API 호출 등 비동기 작업을 처리하는 방법을 배웁니다.

### 추가 학습 자료
- [MDN - Array](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Array)
- [JavaScript Array Explorer](https://arrayexplorer.netlify.app/)
- [고차 함수 이해하기](https://eloquentjavascript.net/05_higher_order.html)

---

**핵심 요약**: map, filter, reduce는 Redux의 핵심입니다. 이 세 가지 메서드만 완벽히 익혀도 Redux State 조작의 90%를 할 수 있습니다! 💪

