---
draft: true
title: "[Redux] 08. 불변성의 중요성 - Immutability in Redux"
date: 2025-10-14
lastmod: 2025-10-14
tags: ["Redux", "Immutability", "불변성", "Immutable", "State Management", "상태관리", "Pure Functions", "순수함수", "Spread Operator", "스프레드연산자", "Immer", "이머", "웹개발", "프론트엔드", "JavaScript", "TypeScript", "Deep Copy", "깊은복사", "Shallow Copy", "얕은복사", "Reference", "참조", "Redux Patterns", "리덕스패턴", "Performance", "성능", "Optimization", "최적화", "React", "리액트", "개발", "코딩", "Best Practices", "모범사례", "Redux Core", "리덕스핵심", "Data Structures", "자료구조", "Functional Programming", "함수형프로그래밍", "Clean Code", "클린코드", "Redux Tutorial", "개발자가이드"]
description: "Redux에서 가장 중요한 불변성 원칙 완벽 마스터. 왜 불변성이 필요한지부터 Spread 연산자, Immer 라이브러리 활용까지 불변 데이터 업데이트 패턴을 실전 예제로 학습합니다"
series: ["Redux 완전 정복"]
series_order: 8
---

## 🎯 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- ✅ 불변성의 개념과 필요성 이해
- ✅ 배열과 객체를 불변하게 업데이트
- ✅ Spread 연산자로 깊은 복사 구현
- ✅ Immer 라이브러리로 간편한 불변 업데이트
- ✅ 불변성 관련 흔한 실수 방지

## 📚 불변성이란?

불변성(Immutability): 데이터를 직접 수정하지 않고 새로운 데이터를 생성하는 것

```javascript
// ❌ 가변적 (Mutable) - 원본 수정
const numbers = [1, 2, 3];
numbers.push(4); // 원본이 변경됨
console.log(numbers); // [1, 2, 3, 4]

// ✅ 불변적 (Immutable) - 새 배열 생성
const numbers = [1, 2, 3];
const newNumbers = [...numbers, 4]; // 새 배열 생성
console.log(numbers); // [1, 2, 3] - 원본 유지
console.log(newNumbers); // [1, 2, 3, 4]
```

## 1. 왜 불변성이 중요한가?

### 1.1 Redux에서 불변성이 필수인 이유

```javascript
// ❌ 불변성 위반 - Redux가 변경을 감지 못함
function todoReducer(state = [], action) {
    switch (action.type) {
        case 'ADD_TODO':
            state.push(action.payload); // 원본 수정!
            return state; // 같은 참조 반환
        
        default:
            return state;
    }
}

// Redux는 참조 비교
const oldState = [{ id: 1, text: 'Learn Redux' }];
const newState = oldState;
oldState === newState; // true → 변경 감지 안 됨!

// ✅ 불변성 유지 - Redux가 변경을 감지
function todoReducer(state = [], action) {
    switch (action.type) {
        case 'ADD_TODO':
            return [...state, action.payload]; // 새 배열!
        
        default:
            return state;
    }
}

const oldState = [{ id: 1, text: 'Learn Redux' }];
const newState = [...oldState, { id: 2, text: 'Build App' }];
oldState === newState; // false → 변경 감지!
```

### 1.2 React 리렌더링

```javascript
// React는 참조 비교로 리렌더링 결정
function TodoList() {
    const todos = useSelector(state => state.todos);
    
    // todos 참조가 변경되어야 리렌더링
    return (
        <ul>
            {todos.map(todo => (
                <li key={todo.id}>{todo.text}</li>
            ))}
        </ul>
    );
}

// ❌ 불변성 위반 → 리렌더링 안 됨
dispatch({
    type: 'ADD_TODO',
    payload: { id: 3, text: 'Test App' }
});
// state.todos.push(...) → 참조 동일 → 리렌더링 안 됨!

// ✅ 불변성 유지 → 리렌더링 됨
dispatch({
    type: 'ADD_TODO',
    payload: { id: 3, text: 'Test App' }
});
// [...state.todos, ...] → 새 참조 → 리렌더링!
```

### 1.3 Time Travel Debugging

```javascript
// 불변성 덕분에 이전 상태 유지
const history = [];

// Action dispatch할 때마다 저장
store.subscribe(() => {
    history.push(store.getState());
});

// 이전 상태로 되돌리기
function undo() {
    if (history.length > 1) {
        history.pop(); // 현재 상태 제거
        const previousState = history[history.length - 1];
        // previousState를 복원
    }
}
```

## 2. 배열 불변 업데이트

### 2.1 추가 (Add)

```javascript
const state = [1, 2, 3];

// ❌ 원본 수정
state.push(4);

// ✅ 불변 업데이트
const newState1 = [...state, 4]; // 끝에 추가
const newState2 = [4, ...state]; // 앞에 추가
const newState3 = [...state.slice(0, 2), 4, ...state.slice(2)]; // 중간에 추가

// Redux Reducer
case 'ADD_TODO':
    return [...state, action.payload];

case 'PREPEND_TODO':
    return [action.payload, ...state];

case 'INSERT_TODO':
    const index = action.payload.index;
    return [
        ...state.slice(0, index),
        action.payload.todo,
        ...state.slice(index)
    ];
```

### 2.2 제거 (Remove)

```javascript
const state = [
    { id: 1, text: 'Learn Redux' },
    { id: 2, text: 'Build App' },
    { id: 3, text: 'Test App' }
];

// ❌ 원본 수정
state.splice(1, 1);

// ✅ 불변 업데이트
const newState1 = state.filter(item => item.id !== 2);

const newState2 = [
    ...state.slice(0, 1),
    ...state.slice(2)
];

// Redux Reducer
case 'REMOVE_TODO':
    return state.filter(todo => todo.id !== action.payload);

case 'REMOVE_TODO_AT':
    const index = action.payload;
    return [
        ...state.slice(0, index),
        ...state.slice(index + 1)
    ];
```

### 2.3 수정 (Update)

```javascript
const state = [
    { id: 1, text: 'Learn Redux', completed: false },
    { id: 2, text: 'Build App', completed: false }
];

// ❌ 원본 수정
state[0].completed = true;

// ✅ 불변 업데이트
const newState = state.map(todo =>
    todo.id === 1
        ? { ...todo, completed: true }
        : todo
);

// Redux Reducer
case 'TOGGLE_TODO':
    return state.map(todo =>
        todo.id === action.payload
            ? { ...todo, completed: !todo.completed }
            : todo
    );

case 'UPDATE_TODO':
    return state.map(todo =>
        todo.id === action.payload.id
            ? { ...todo, ...action.payload.updates }
            : todo
    );
```

### 2.4 정렬 (Sort)

```javascript
const state = [3, 1, 4, 1, 5, 9];

// ❌ 원본 수정
state.sort();

// ✅ 불변 업데이트
const newState = [...state].sort((a, b) => a - b);

// Redux Reducer
case 'SORT_TODOS':
    return [...state].sort((a, b) => {
        if (a.priority !== b.priority) {
            const priorities = { high: 3, medium: 2, low: 1 };
            return priorities[b.priority] - priorities[a.priority];
        }
        return a.text.localeCompare(b.text);
    });
```

## 3. 객체 불변 업데이트

### 3.1 속성 추가/수정

```javascript
const state = {
    user: { id: 1, name: 'Alice' },
    theme: 'dark'
};

// ❌ 원본 수정
state.user.email = 'alice@example.com';

// ✅ 불변 업데이트
const newState = {
    ...state,
    user: {
        ...state.user,
        email: 'alice@example.com'
    }
};

// Redux Reducer
case 'UPDATE_USER':
    return {
        ...state,
        user: {
            ...state.user,
            ...action.payload
        }
    };
```

### 3.2 속성 제거

```javascript
const state = {
    id: 1,
    name: 'Alice',
    email: 'alice@example.com',
    password: 'secret'
};

// ❌ 원본 수정
delete state.password;

// ✅ 불변 업데이트 (방법 1: 구조 분해)
const { password, ...newState } = state;

// ✅ 불변 업데이트 (방법 2: Object.keys)
const newState = Object.keys(state)
    .filter(key => key !== 'password')
    .reduce((obj, key) => {
        obj[key] = state[key];
        return obj;
    }, {});

// Redux Reducer
case 'REMOVE_PASSWORD':
    const { password, ...rest } = state.user;
    return {
        ...state,
        user: rest
    };
```

### 3.3 중첩 객체 업데이트

```javascript
const state = {
    user: {
        id: 1,
        profile: {
            name: 'Alice',
            address: {
                city: 'Seoul',
                country: 'Korea'
            }
        }
    }
};

// ❌ 원본 수정
state.user.profile.address.city = 'Busan';

// ✅ 불변 업데이트
const newState = {
    ...state,
    user: {
        ...state.user,
        profile: {
            ...state.user.profile,
            address: {
                ...state.user.profile.address,
                city: 'Busan'
            }
        }
    }
};

// Redux Reducer
case 'UPDATE_CITY':
    return {
        ...state,
        user: {
            ...state.user,
            profile: {
                ...state.user.profile,
                address: {
                    ...state.user.profile.address,
                    city: action.payload
                }
            }
        }
    };
```

## 4. 복잡한 State 업데이트 패턴

### 4.1 배열 내 객체 업데이트

```javascript
const state = {
    todos: [
        { id: 1, text: 'Learn Redux', tags: ['redux', 'react'] },
        { id: 2, text: 'Build App', tags: ['react'] }
    ]
};

// Todo 텍스트 수정
case 'UPDATE_TODO_TEXT':
    return {
        ...state,
        todos: state.todos.map(todo =>
            todo.id === action.payload.id
                ? { ...todo, text: action.payload.text }
                : todo
        )
    };

// Todo에 태그 추가
case 'ADD_TAG_TO_TODO':
    return {
        ...state,
        todos: state.todos.map(todo =>
            todo.id === action.payload.todoId
                ? { ...todo, tags: [...todo.tags, action.payload.tag] }
                : todo
        )
    };
```

### 4.2 정규화된 State

```javascript
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

// Todo 추가
case 'ADD_TODO':
    const newTodo = action.payload;
    return {
        ...state,
        todos: {
            byId: {
                ...state.todos.byId,
                [newTodo.id]: newTodo
            },
            allIds: [...state.todos.allIds, newTodo.id]
        }
    };

// Todo 제거
case 'REMOVE_TODO':
    const { [action.payload]: removed, ...remainingTodos } = state.todos.byId;
    return {
        ...state,
        todos: {
            byId: remainingTodos,
            allIds: state.todos.allIds.filter(id => id !== action.payload)
        }
    };

// Todo 업데이트
case 'UPDATE_TODO':
    return {
        ...state,
        todos: {
            ...state.todos,
            byId: {
                ...state.todos.byId,
                [action.payload.id]: {
                    ...state.todos.byId[action.payload.id],
                    ...action.payload.updates
                }
            }
        }
    };
```

## 5. Immer - 불변성을 쉽게

### 5.1 Immer 기본 사용

```bash
npm install immer
```

```javascript
import produce from 'immer';

const state = [
    { id: 1, text: 'Learn Redux', completed: false },
    { id: 2, text: 'Build App', completed: false }
];

// ❌ 복잡한 불변 업데이트
const newState = state.map(todo =>
    todo.id === 1
        ? { ...todo, completed: true }
        : todo
);

// ✅ Immer로 간단하게
const newState = produce(state, draft => {
    const todo = draft.find(t => t.id === 1);
    if (todo) {
        todo.completed = true; // 직접 수정처럼 보이지만 불변 업데이트!
    }
});
```

### 5.2 Immer로 Redux Reducer 작성

```javascript
import produce from 'immer';

const initialState = {
    todos: [],
    filter: 'all',
    loading: false
};

// 전통적인 방식
function todoReducer(state = initialState, action) {
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
        
        default:
            return state;
    }
}

// ✅ Immer 방식
function todoReducer(state = initialState, action) {
    return produce(state, draft => {
        switch (action.type) {
            case 'ADD_TODO':
                draft.todos.push(action.payload);
                break;
            
            case 'TOGGLE_TODO':
                const todo = draft.todos.find(t => t.id === action.payload);
                if (todo) {
                    todo.completed = !todo.completed;
                }
                break;
            
            case 'SET_LOADING':
                draft.loading = action.payload;
                break;
        }
    });
}
```

### 5.3 중첩 업데이트가 쉬워짐

```javascript
const state = {
    user: {
        id: 1,
        profile: {
            name: 'Alice',
            settings: {
                theme: 'dark',
                notifications: {
                    email: true,
                    push: false
                }
            }
        }
    }
};

// ❌ 전통적인 방식 (복잡!)
const newState = {
    ...state,
    user: {
        ...state.user,
        profile: {
            ...state.user.profile,
            settings: {
                ...state.user.profile.settings,
                notifications: {
                    ...state.user.profile.settings.notifications,
                    push: true
                }
            }
        }
    }
};

// ✅ Immer (간단!)
const newState = produce(state, draft => {
    draft.user.profile.settings.notifications.push = true;
});
```

## 6. 성능 고려사항

### 6.1 얕은 복사 vs 깊은 복사

```javascript
// 얕은 복사 (Shallow Copy)
const original = { a: 1, b: { c: 2 } };
const copy = { ...original };

copy.a = 10; // OK
copy.b.c = 20; // 원본도 변경됨!

console.log(original.b.c); // 20

// 깊은 복사 (Deep Copy) - 필요할 때만
const deepCopy = JSON.parse(JSON.stringify(original));
// 또는 lodash
import cloneDeep from 'lodash/cloneDeep';
const deepCopy = cloneDeep(original);

// Redux에서는 보통 얕은 복사로 충분
// 중첩된 부분만 필요할 때 복사
```

### 6.2 대용량 배열 처리

```javascript
// ❌ 느림: 매번 새 배열 생성
const state = [...Array(10000).keys()];

function slowUpdate(state) {
    return state.map(item => item * 2); // 10000개 모두 처리
}

// ✅ 빠름: 변경된 것만 복사
function fastUpdate(state) {
    const index = 5000;
    return [
        ...state.slice(0, index),
        state[index] * 2,
        ...state.slice(index + 1)
    ];
}

// ✅ 더 나은 방법: 정규화
const normalizedState = {
    byId: {
        '1': { value: 1 },
        '2': { value: 2 },
        // ...
    },
    allIds: ['1', '2', ...]
};

// 하나만 업데이트
function updateOne(state, id, value) {
    return {
        ...state,
        byId: {
            ...state.byId,
            [id]: { ...state.byId[id], value }
        }
    };
}
```

## 7. 흔한 실수와 해결법

### 실수 1: 배열 메서드 혼동

```javascript
// ❌ 원본 수정 메서드
state.push()
state.pop()
state.shift()
state.unshift()
state.splice()
state.reverse()
state.sort()

// ✅ 불변 메서드
state.concat()
state.slice()
state.map()
state.filter()
state.reduce()
```

### 실수 2: 중첩 깊이 놓침

```javascript
// ❌ 한 단계만 복사
const newState = {
    ...state,
    user: state.user // 참조 공유!
};
newState.user.name = 'Bob'; // 원본도 변경!

// ✅ 모든 레벨 복사
const newState = {
    ...state,
    user: {
        ...state.user,
        name: 'Bob'
    }
};
```

### 실수 3: Return 누락

```javascript
// ❌ produce 내에서 명시적 반환
const newState = produce(state, draft => {
    draft.count += 1;
    return draft; // 필요 없음!
});

// ✅ 아무것도 반환하지 않기
const newState = produce(state, draft => {
    draft.count += 1;
    // 자동으로 draft가 반환됨
});
```

## 8. 실습 문제 🏋️‍♂️

### 문제 1: 배열 불변 업데이트
```javascript
const todos = [
    { id: 1, text: 'Learn Redux', completed: false },
    { id: 2, text: 'Build App', completed: false }
];

// TODO: id가 1인 todo의 completed를 true로 변경

// 답안:
const updatedTodos = todos.map(todo =>
    todo.id === 1
        ? { ...todo, completed: true }
        : todo
);
```

### 문제 2: 중첩 객체 업데이트
```javascript
const state = {
    user: {
        profile: {
            settings: {
                theme: 'dark'
            }
        }
    }
};

// TODO: theme를 'light'로 변경

// 답안:
const newState = {
    ...state,
    user: {
        ...state.user,
        profile: {
            ...state.user.profile,
            settings: {
                ...state.user.profile.settings,
                theme: 'light'
            }
        }
    }
};

// 또는 Immer
const newState = produce(state, draft => {
    draft.user.profile.settings.theme = 'light';
});
```

## 9. 체크리스트 ✅

- [ ] 불변성의 개념과 필요성을 이해한다
- [ ] 배열을 불변하게 업데이트할 수 있다
- [ ] 객체를 불변하게 업데이트할 수 있다
- [ ] 중첩된 데이터를 불변하게 업데이트할 수 있다
- [ ] Immer 라이브러리를 사용할 수 있다
- [ ] 불변성 관련 흔한 실수를 피할 수 있다

## 10. 다음 단계 🚀

**다음 챕터**: `09. Redux 데이터 흐름 이해하기`에서 Redux의 단방향 데이터 흐름을 시각화하고 전체 프로세스를 완벽히 이해합니다!

### 추가 학습 자료
- [Immutable Update Patterns](https://redux.js.org/usage/structuring-reducers/immutable-update-patterns)
- [Immer 공식 문서](https://immerjs.github.io/immer/)
- [Immutability in JavaScript](https://developer.mozilla.org/en-US/docs/Glossary/Immutable)

---

**핵심 요약**: 불변성은 Redux의 생명입니다. 원본을 수정하지 말고 항상 새로운 값을 반환하세요! Immer를 사용하면 훨씬 쉽습니다! 💪




