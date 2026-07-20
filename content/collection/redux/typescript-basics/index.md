---
title: "[Redux] 05. TypeScript 기초 - 타입 시스템 이해하기"
description: "실무 Redux 코드는 대부분 TypeScript로 작성됩니다. 기본 타입, 인터페이스, 제네릭을 Action과 State에 타입을 붙이는 데 필요한 만큼 정리하고, 28편(Redux와 TypeScript)의 기초를 다집니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 5
draft: false
slug: typescript-basics
image: "wordcloud.png"
tags:
  - TypeScript
  - JavaScript
  - Type-Safety
  - Frontend(프론트엔드)
  - Web(웹)
  - Beginner
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Interface(인터페이스)
  - Error-Handling(에러처리)
  - How-To
  - Guide(가이드)
  - Documentation(문서화)
  - Reference(참고)
  - Software-Architecture(소프트웨어아키텍처)
  - Refactoring(리팩토링)
  - 타입추론
  - 인터페이스타입별칭
  - 제네릭
  - 유니온타입
  - 판별유니온
  - 타입가드
  - 컴파일타임검증
---

# 05. TypeScript 기초 - 타입 시스템 이해하기

Redux 공식 문서와 대부분의 실무 프로젝트는 이제 TypeScript를 기본으로 씁니다. Action의 `type` 문자열을 오타 없이 다루고, State의 형태를 컴파일 시점에 검증하는 것이 TypeScript가 Redux에 주는 가장 큰 이점입니다. Phase 1의 마지막 편으로, 이후 모든 편의 코드 예제를 이해하는 데 필요한 최소한의 타입 시스템을 정리합니다.

## 학습 목표

- 기본 타입과 타입 추론을 이용해 변수·함수에 타입을 명시할 수 있다.
- 인터페이스와 타입 별칭으로 객체의 형태를 정의할 수 있다.
- 제네릭과 유니온 타입으로 재사용 가능하고 정확한 타입을 만들 수 있다.

## 기본 타입과 타입 추론

TypeScript는 JavaScript에 **정적 타입 검사**를 추가한 언어입니다. 변수 선언 시 타입을 명시할 수도 있지만, 초기값이 있으면 TypeScript가 자동으로 타입을 **추론**합니다.

```typescript
let count: number = 0;      // 명시적 타입
let total = 0;               // 추론됨: number
let name = "Kim";            // 추론됨: string
let isDone = false;          // 추론됨: boolean

total = "문자열"; // 컴파일 에러: string 형식은 number 형식에 할당할 수 없습니다
```

함수의 매개변수와 반환값에도 타입을 붙일 수 있습니다.

```typescript
function add(a: number, b: number): number {
  return a + b;
}

add(1, "2"); // 컴파일 에러: "2"는 number가 아님
```

## 인터페이스와 타입 별칭: 객체의 형태를 정의한다

<strong>인터페이스(interface)</strong>와 <strong>타입 별칭(type alias)</strong>은 객체가 어떤 속성을 가져야 하는지 정의합니다. Redux의 State와 Action 형태를 정의할 때 가장 많이 쓰입니다.

```typescript
interface Todo {
  id: number;
  text: string;
  done: boolean;
}

const todo: Todo = { id: 1, text: "학습", done: false };

// 필수 속성이 빠지면 컴파일 에러
const invalid: Todo = { id: 2, text: "복습" }; // 에러: done 속성이 없습니다
```

`interface`와 `type`은 대부분의 경우 서로 바꿔 쓸 수 있지만, 관례상 **객체 형태 정의에는 `interface`, 유니온 타입이나 함수 타입에는 `type`**을 사용합니다.

```typescript
type Status = "idle" | "loading" | "succeeded" | "failed"; // 유니온 타입

interface RequestState {
  status: Status;
  error: string | null;
}
```

## 제네릭: 타입을 매개변수로 받는다

<strong>제네릭(Generic)</strong>은 함수나 타입이 다룰 데이터 타입을 나중에 지정할 수 있게 해줍니다. 배열이나 API 응답처럼 "형태는 같지만 내용물 타입이 다른" 경우에 유용합니다.

```typescript
function firstElement<T>(arr: T[]): T | undefined {
  return arr[0];
}

const firstNumber = firstElement([1, 2, 3]);     // 타입: number | undefined
const firstTodo = firstElement<Todo>([todo]);    // 타입: Todo | undefined
```

Redux Toolkit의 `createAsyncThunk`, RTK Query의 `useQuery` 같은 함수들이 내부적으로 제네릭을 광범위하게 사용해, "이 API가 어떤 타입의 데이터를 반환하는지"를 호출부에서 정확히 추론하게 해줍니다(19편, 24편에서 실제로 사용합니다).

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
}

const userResponse: ApiResponse<{ id: number; name: string }> = {
  data: { id: 1, name: "Kim" },
  status: 200,
};
```

## 판별 유니온: Redux Action 타입의 핵심 도구

여러 종류의 Action을 하나의 타입으로 안전하게 표현하려면 <strong>판별 유니온(Discriminated Union)</strong>을 씁니다. 공통 속성(보통 `type`)의 값으로 어떤 종류인지 구분합니다.

```typescript
interface AddTodoAction {
  type: "todos/add";
  payload: { text: string };
}

interface ToggleTodoAction {
  type: "todos/toggle";
  payload: { id: number };
}

type TodoAction = AddTodoAction | ToggleTodoAction;

function todoReducer(state: Todo[], action: TodoAction): Todo[] {
  switch (action.type) {
    case "todos/add":
      // 이 분기 안에서 TypeScript는 action이 AddTodoAction임을 알고,
      // action.payload.text에 정확한 타입으로 접근할 수 있게 해준다
      return [...state, { id: Date.now(), text: action.payload.text, done: false }];
    case "todos/toggle":
      return state.map((todo) =>
        todo.id === action.payload.id ? { ...todo, done: !todo.done } : todo
      );
    default:
      return state;
  }
}
```

`switch (action.type)`의 각 `case` 안에서 TypeScript가 `action`의 구체적인 타입을 자동으로 좁혀주는 것을 <strong>타입 좁히기(Type Narrowing)</strong>라고 합니다. 이 덕분에 `action.payload`에 존재하지 않는 속성을 잘못 참조하면 컴파일 시점에 에러가 납니다. 이 패턴은 07편(Action, Reducer, Store)과 28편(Redux와 TypeScript)에서 그대로 확장됩니다.

## any를 피해야 하는 이유

`any` 타입은 TypeScript의 타입 검사를 사실상 꺼버립니다.

```typescript
function processAction(action: any) {
  console.log(action.paylod.text); // 오타(payload → paylod)인데도 컴파일 에러 없음!
}
```

`any` 대신 타입을 정확히 모를 때는 `unknown`을 쓰고, 사용하기 전에 타입을 검증(타입 가드)하는 편이 안전합니다.

```typescript
function processActionSafe(action: unknown) {
  if (typeof action === "object" && action !== null && "type" in action) {
    console.log((action as { type: string }).type); // 검증 후에만 접근
  }
}
```

## 실무 체크리스트

- 함수의 매개변수와 반환값에 타입이 명시되어 있거나, 타입 추론으로 충분히 명확한가?
- 객체 형태를 나타낼 때는 `interface`, 여러 액션 타입을 묶을 때는 유니온 타입을 쓰고 있는가?
- 코드에 `any`가 남아 있다면, `unknown` + 타입 가드로 바꿀 수 있는가?

## 연습 과제

### 기초(★☆☆)
- `User` 인터페이스(`id`, `name`, `email`)를 정의하고, 이 인터페이스를 타입으로 쓰는 변수를 만들어보세요.

### 중급(★★☆)
- `RemoveTodoAction`(`type: "todos/remove"`, `payload: { id: number }`)을 추가해 `TodoAction` 유니온을 확장하고, `todoReducer`에 해당 케이스를 구현해보세요.

### 고급(★★★)
- `ApiResponse<T>` 제네릭 인터페이스를 사용해, `User` 배열을 담는 응답과 단일 `Todo`를 담는 응답 두 가지 타입을 각각 만들어보세요.

## 요약

- TypeScript는 타입 추론과 명시적 타입 지정을 함께 지원하며, 컴파일 시점에 오류를 잡아준다.
- 인터페이스로 State/Action의 형태를, 제네릭으로 재사용 가능한 타입을 정의한다.
- 판별 유니온과 `switch (action.type)`의 타입 좁히기는 Redux Action을 안전하게 다루는 핵심 패턴이다.

## 참고 문헌 및 출처(추천)

- TypeScript 공식 문서, "Everyday Types" — 기본 타입과 인터페이스
- TypeScript 공식 문서, "Narrowing" — 판별 유니온과 타입 좁히기
- Redux 공식 문서, "Usage With TypeScript" — Redux에서 권장하는 타입 패턴

---

## 다음 글

- 다음: [06. Redux란 무엇인가 - Flux 아키텍처와 상태 관리](../what-is-redux/)
