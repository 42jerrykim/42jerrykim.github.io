---
draft: true
title: "[Redux] 05. TypeScript 기초 - 타입 시스템 이해하기"
date: 2025-10-14
lastmod: 2025-10-14
tags: ["Redux", "TypeScript", "타입시스템", "Type System", "정적타입", "Static Typing", "Type Safety", "타입안전성", "Interface", "인터페이스", "Type Alias", "Generic", "제네릭", "웹개발", "프론트엔드", "TypeScript Basics", "TS", "타입추론", "Type Inference", "Union Types", "Intersection Types", "Literal Types", "Type Guards", "타입가드", "Utility Types", "유틸리티타입", "개발", "코딩", "타입스크립트기초", "타입정의", "Type Definition", "타입체크", "Type Checking", "JavaScript", "자바스크립트", "TypeScript Tutorial", "Learn TypeScript", "개발자가이드", "Best Practices", "Clean Code", "코드품질", "Code Quality", "IDE Support", "자동완성", "Autocomplete", "Refactoring", "리팩토링"]
description: "Redux Toolkit과 함께 사용하는 TypeScript 기초 완벽 마스터. 타입 시스템으로 안전한 Redux 코드 작성, 인터페이스와 제네릭으로 타입 재사용, 실전 Redux 타입 정의 패턴까지 학습합니다"
series: ["Redux 완전 정복"]
series_order: 5
---

## 학습 목표

이 챕터를 마치면 다음을 할 수 있습니다:

- ✅ TypeScript의 기본 타입 시스템 이해
- ✅ 인터페이스와 타입 별칭으로 복잡한 타입 정의
- ✅ 제네릭을 활용한 재사용 가능한 타입 작성
- ✅ Redux에서 TypeScript를 효과적으로 활용

## 왜 TypeScript를 배워야 할까?

Redux + TypeScript = 강력한 개발 경험:

```typescript
// JavaScript - 런타임 에러!
const user = { name: "Alice", age: 25 };
console.log(user.email); // undefined (에러 아님)

// TypeScript - 컴파일 타임에 에러 발견!
interface User {
    name: string;
    age: number;
}

const user: User = { name: "Alice", age: 25 };
console.log(user.email); // ❌ Error: Property 'email' does not exist
```

**장점**:
1. **조기 에러 발견**: 실행 전에 버그 발견
2. **자동완성**: IDE가 가능한 속성/메서드 제안
3. **리팩토링 안전**: 타입 변경 시 영향받는 코드 자동 표시
4. **문서화**: 타입 자체가 문서 역할

## 기본 타입 (Basic Types)

### 원시 타입

```typescript
// 문자열
let name: string = "Alice";
name = "Bob"; // OK
// name = 123; // Error

// 숫자
let age: number = 25;
age = 30; // OK
// age = "30"; // Error

// 불리언
let isActive: boolean = true;
isActive = false; // OK
// isActive = "true"; // Error

// null과 undefined
let nothing: null = null;
let notDefined: undefined = undefined;

// any - 모든 타입 허용 (가급적 사용 자제!)
let anything: any = "string";
anything = 123; // OK
anything = true; // OK
```

### 배열과 튜플

```typescript
// 배열
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ["a", "b", "c"];

// 다차원 배열
let matrix: number[][] = [
    [1, 2, 3],
    [4, 5, 6]
];

// 튜플 - 고정 길이, 각 위치별 타입 지정
let tuple: [string, number] = ["Alice", 25];
tuple = ["Bob", 30]; // OK
// tuple = [30, "Bob"]; // Error - 순서 중요!

// 튜플 배열
let users: [string, number][] = [
    ["Alice", 25],
    ["Bob", 30]
];
```

### 객체 타입

```typescript
// 객체
let user: { name: string; age: number } = {
    name: "Alice",
    age: 25
};

// 선택적 속성 (?)
let optionalUser: {
    name: string;
    age?: number; // 있어도 되고 없어도 됨
} = {
    name: "Bob" // age 없어도 OK
};

// 읽기 전용 속성 (readonly)
let readonlyUser: {
    readonly id: number;
    name: string;
} = {
    id: 1,
    name: "Alice"
};

// readonlyUser.id = 2; // Error
readonlyUser.name = "Bob"; // OK
```

## 인터페이스 (Interface)

### 기본 인터페이스

```typescript
// 인터페이스 정의
interface User {
    id: number;
    name: string;
    email: string;
    age?: number; // 선택적
}

// 사용
const user1: User = {
    id: 1,
    name: "Alice",
    email: "alice@example.com"
    // age는 선택적이므로 생략 가능
};

const user2: User = {
    id: 2,
    name: "Bob",
    email: "bob@example.com",
    age: 30
};

// Redux State
interface TodoState {
    todos: Todo[];
    filter: 'all' | 'active' | 'completed';
    loading: boolean;
    error: string | null;
}
```

### 인터페이스 확장

```typescript
interface Person {
    name: string;
    age: number;
}

// Person을 확장
interface Employee extends Person {
    employeeId: number;
    department: string;
}

const employee: Employee = {
    name: "Alice",
    age: 25,
    employeeId: 12345,
    department: "Engineering"
};

// 다중 확장
interface Admin extends Person, Employee {
    privileges: string[];
}
```

### 함수 인터페이스

```typescript
// 함수 시그니처
interface MathOperation {
    (a: number, b: number): number;
}

const add: MathOperation = (a, b) => a + b;
const subtract: MathOperation = (a, b) => a - b;

// Redux Action Creator
interface AddTodoAction {
    type: 'ADD_TODO';
    payload: {
        id: number;
        text: string;
    };
}

interface ActionCreator {
    (text: string): AddTodoAction;
}

const addTodo: ActionCreator = (text) => ({
    type: 'ADD_TODO',
    payload: { id: Date.now(), text }
});
```

## 타입 별칭 (Type Alias)

### 기본 타입 별칭

```typescript
// 타입 별칭
type ID = number | string;
type Status = 'pending' | 'success' | 'error';

let userId: ID = 123; // OK
userId = "abc"; // OK

let status: Status = 'pending'; // OK
// status = 'invalid'; // Error

// 객체 타입
type User = {
    id: ID;
    name: string;
    status: Status;
};

const user: User = {
    id: 1,
    name: "Alice",
    status: 'success'
};
```

### 인터페이스 vs 타입 별칭

```typescript
// Interface는 확장 가능
interface IUser {
    name: string;
}

interface IUser {
    age: number; // 선언 병합 - OK
}

// Type은 재선언 불가
type TUser = {
    name: string;
};

// type TUser = { age: number }; // Error

// Union과 Intersection은 Type만 가능
type StringOrNumber = string | number; // OK
type Combined = User & Employee; // OK

// 일반적 가이드:
// - 객체 형태는 Interface 선호
// - Union/Intersection은 Type
// - Redux에서는 둘 다 많이 사용
```

## 유니온과 인터섹션

### 유니온 타입 (Union)

```typescript
// 여러 타입 중 하나
type ID = number | string;

function printId(id: ID) {
    console.log(id);
}

printId(123); // OK
printId("abc"); // OK
// printId(true); // Error

// Type Guard
function processId(id: ID) {
    if (typeof id === 'string') {
        console.log(id.toUpperCase()); // string 메서드 사용 가능
    } else {
        console.log(id.toFixed(2)); // number 메서드 사용 가능
    }
}

// Redux Action Types
type TodoAction =
    | { type: 'ADD_TODO'; payload: Todo }
    | { type: 'TOGGLE_TODO'; payload: number }
    | { type: 'REMOVE_TODO'; payload: number };

function todoReducer(state: TodoState, action: TodoAction) {
    switch (action.type) {
        case 'ADD_TODO':
            return {
                ...state,
                todos: [...state.todos, action.payload] // payload는 Todo
            };
        case 'TOGGLE_TODO':
            return {
                ...state,
                todos: state.todos.map(todo =>
                    todo.id === action.payload // payload는 number
                        ? { ...todo, completed: !todo.completed }
                        : todo
                )
            };
    }
}
```

### 인터섹션 타입 (Intersection)

```typescript
// 여러 타입을 결합
type Person = {
    name: string;
    age: number;
};

type Employee = {
    employeeId: number;
    department: string;
};

type Staff = Person & Employee;

const staff: Staff = {
    name: "Alice",
    age: 25,
    employeeId: 12345,
    department: "Engineering"
    // 모든 속성 필요!
};

// Mixin 패턴
type Timestamps = {
    createdAt: Date;
    updatedAt: Date;
};

type Todo = {
    id: number;
    text: string;
    completed: boolean;
} & Timestamps;
```

## 제네릭 (Generics)

### 제네릭 기본

```typescript
// 제네릭 없이
function getFirstNumber(arr: number[]): number {
    return arr[0];
}

function getFirstString(arr: string[]): string {
    return arr[0];
}

// 제네릭 사용 ⭐
function getFirst<T>(arr: T[]): T {
    return arr[0];
}

// 사용
const firstNumber = getFirst<number>([1, 2, 3]); // number
const firstString = getFirst<string>(["a", "b"]); // string
const firstAny = getFirst([1, "a", true]); // number | string | boolean (자동 추론)
```

### 제네릭 인터페이스

```typescript
// 제네릭 인터페이스
interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
}

// 사용
type UserResponse = ApiResponse<User>;
type TodosResponse = ApiResponse<Todo[]>;

const userRes: UserResponse = {
    data: { id: 1, name: "Alice", email: "alice@example.com" },
    status: 200,
    message: "Success"
};

const todosRes: TodosResponse = {
    data: [
        { id: 1, text: "Learn TS", completed: false }
    ],
    status: 200,
    message: "Success"
};
```

### Redux에서 제네릭 활용

```typescript
// Redux State
interface ReduxState<T> {
    data: T | null;
    loading: boolean;
    error: string | null;
}

interface TodosState extends ReduxState<Todo[]> {
    filter: 'all' | 'active' | 'completed';
}

interface UserState extends ReduxState<User> {
    isLoggedIn: boolean;
}

// Action Creator
interface Action<T = any> {
    type: string;
    payload?: T;
}

function createAction<T>(type: string, payload: T): Action<T> {
    return { type, payload };
}

const addTodoAction = createAction('ADD_TODO', { 
    id: 1, 
    text: "Learn Redux" 
});
// type: "ADD_TODO", payload: { id: number, text: string }

// Thunk
type ThunkAction<R> = (
    dispatch: Dispatch,
    getState: () => RootState
) => R;

const fetchTodos: ThunkAction<Promise<void>> = async (dispatch, getState) => {
    dispatch({ type: 'FETCH_REQUEST' });
    const todos = await fetch('/api/todos').then(r => r.json());
    dispatch({ type: 'FETCH_SUCCESS', payload: todos });
};
```

## 유틸리티 타입 (Utility Types)

### Partial, Required, Readonly

```typescript
interface Todo {
    id: number;
    text: string;
    completed: boolean;
}

// Partial - 모든 속성을 선택적으로
type PartialTodo = Partial<Todo>;
// { id?: number; text?: string; completed?: boolean; }

const partialTodo: PartialTodo = { text: "Learn TS" }; // OK

// Required - 모든 속성을 필수로
interface OptionalTodo {
    id: number;
    text?: string;
}

type RequiredTodo = Required<OptionalTodo>;
// { id: number; text: string; } - text 필수!

// Readonly - 모든 속성을 읽기 전용으로
type ReadonlyTodo = Readonly<Todo>;

const todo: ReadonlyTodo = { id: 1, text: "Learn TS", completed: false };
// todo.completed = true; // Error
```

### Pick, Omit

```typescript
interface User {
    id: number;
    name: string;
    email: string;
    password: string;
}

// Pick - 특정 속성만 선택
type UserPreview = Pick<User, 'id' | 'name'>;
// { id: number; name: string; }

// Omit - 특정 속성 제외
type UserWithoutPassword = Omit<User, 'password'>;
// { id: number; name: string; email: string; }

// Redux에서 활용
interface TodoState {
    todos: Todo[];
    loading: boolean;
    error: string | null;
    filter: string;
}

// loading과 error만 추출
type LoadingState = Pick<TodoState, 'loading' | 'error'>;
```

### Record, ReturnType

```typescript
// Record - 키-값 타입 매핑
type Role = 'admin' | 'user' | 'guest';
type RolePermissions = Record<Role, string[]>;

const permissions: RolePermissions = {
    admin: ['read', 'write', 'delete'],
    user: ['read', 'write'],
    guest: ['read']
};

// ReturnType - 함수 반환 타입 추출
function getUser() {
    return { id: 1, name: "Alice" };
}

type User = ReturnType<typeof getUser>;
// { id: number; name: string; }

// Redux에서
function createTodoAction(text: string) {
    return { type: 'ADD_TODO' as const, payload: { text } };
}

type TodoAction = ReturnType<typeof createTodoAction>;
// { type: 'ADD_TODO'; payload: { text: string; } }
```

## Redux TypeScript 실전 예제

### 타입 안전한 Redux Store

```typescript
// types.ts
export interface Todo {
    id: number;
    text: string;
    completed: boolean;
}

export interface TodoState {
    todos: Todo[];
    filter: 'all' | 'active' | 'completed';
    loading: boolean;
    error: string | null;
}

// Action Types
export type TodoAction =
    | { type: 'ADD_TODO'; payload: Omit<Todo, 'id'> }
    | { type: 'TOGGLE_TODO'; payload: number }
    | { type: 'REMOVE_TODO'; payload: number }
    | { type: 'SET_FILTER'; payload: TodoState['filter'] }
    | { type: 'FETCH_TODOS_REQUEST' }
    | { type: 'FETCH_TODOS_SUCCESS'; payload: Todo[] }
    | { type: 'FETCH_TODOS_FAILURE'; payload: string };

// reducer.ts
const initialState: TodoState = {
    todos: [],
    filter: 'all',
    loading: false,
    error: null
};

export function todoReducer(
    state: TodoState = initialState,
    action: TodoAction
): TodoState {
    switch (action.type) {
        case 'ADD_TODO':
            return {
                ...state,
                todos: [
                    ...state.todos,
                    { ...action.payload, id: Date.now() }
                ]
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
        
        case 'SET_FILTER':
            return { ...state, filter: action.payload };
        
        case 'FETCH_TODOS_REQUEST':
            return { ...state, loading: true, error: null };
        
        case 'FETCH_TODOS_SUCCESS':
            return { ...state, loading: false, todos: action.payload };
        
        case 'FETCH_TODOS_FAILURE':
            return { ...state, loading: false, error: action.payload };
        
        default:
            return state;
    }
}

// actions.ts
export const addTodo = (text: string): TodoAction => ({
    type: 'ADD_TODO',
    payload: { text, completed: false }
});

export const toggleTodo = (id: number): TodoAction => ({
    type: 'TOGGLE_TODO',
    payload: id
});
```

## 실습 문제 🏋️‍♂️

### 문제 1: 인터페이스 정의
```typescript
// TODO: Product 인터페이스 정의
// - id (number)
// - name (string)
// - price (number)
// - category (string)
// - inStock (boolean, 선택적)

// 답안:
interface Product {
    id: number;
    name: string;
    price: number;
    category: string;
    inStock?: boolean;
}
```

### 문제 2: 제네릭 함수
```typescript
// TODO: 배열의 마지막 요소를 반환하는 제네릭 함수

// 답안:
function getLast<T>(arr: T[]): T | undefined {
    return arr[arr.length - 1];
}

const lastNumber = getLast([1, 2, 3]); // 3
const lastString = getLast(['a', 'b']); // 'b'
```

### 문제 3: Redux State 타입
```typescript
// TODO: User Redux State 타입 정의
// - user: User | null
// - loading: boolean
// - error: string | null
// - isAuthenticated: boolean

// 답안:
interface User {
    id: number;
    name: string;
    email: string;
}

interface UserState {
    user: User | null;
    loading: boolean;
    error: string | null;
    isAuthenticated: boolean;
}
```

## 체크리스트 ✅

- [ ] TypeScript 기본 타입을 이해한다
- [ ] 인터페이스와 타입 별칭을 작성할 수 있다
- [ ] 유니온과 인터섹션 타입을 활용할 수 있다
- [ ] 제네릭의 개념을 이해하고 사용할 수 있다
- [ ] 유틸리티 타입을 활용할 수 있다
- [ ] Redux에서 TypeScript를 적용할 수 있다
- [ ] 실습 문제를 모두 해결했다

## 다음 단계 🚀

축하합니다! JavaScript/TypeScript 기초를 모두 마쳤습니다.

**다음 챕터**: `06. Redux란 무엇인가 - Flux 아키텍처와 상태 관리`에서 본격적으로 Redux를 배우기 시작합니다!

### 추가 학습 자료
- [TypeScript 공식 문서](https://www.typescriptlang.org/docs/)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

---

**핵심 요약**: TypeScript는 Redux 코드를 더 안전하고 유지보수하기 쉽게 만듭니다. 타입 정의에 익숙해지면 개발 속도가 오히려 빨라집니다! 💪

