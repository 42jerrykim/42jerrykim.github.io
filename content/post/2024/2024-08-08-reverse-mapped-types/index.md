---
draft: false
image: "wordcloud.png"
teaser: /assets/images/2024/2024-08-08-reverse-mapped-types.png
description: "TypeScript의 Reverse Mapped Types(리버스 맵핑 타입)는 매핑 타입을 역으로 실행해 인자 값으로부터 타입 매개변수를 추론하는 기능이다. infer, Box/Unboxify·unwrap 예제, 상태 머신·이벤트 바인딩 등 실전 활용과 요구사항·한계·FAQ, 공식 문서 포함 참고 문헌 3편까지 개념부터 정리했다."
categories: typescript
date: "2024-08-08T00:00:00Z"
lastmod: "2026-03-17T00:00:00Z"
header: null
title: "[TypeScript] Reverse Mapped Types 이해와 실전 활용"
tags:
  - TypeScript
  - JavaScript
  - Compiler
  - 컴파일러
  - Implementation
  - 구현
  - Software-Architecture
  - 소프트웨어아키텍처
  - Code-Quality
  - 코드품질
  - Edge-Cases
  - 엣지케이스
  - Recursion
  - 재귀
  - Functional-Programming
  - 함수형프로그래밍
  - Web
  - 웹
  - Blog
  - 블로그
  - Technology
  - 기술
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - Review
  - 리뷰
  - Reference
  - 참고
  - Best-Practices
  - Documentation
  - 문서화
  - Open-Source
  - 오픈소스
  - Type-Safety
  - Interface
  - 인터페이스
  - Design-Pattern
  - 디자인패턴
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - Testing
  - 테스트
  - Frontend
  - 프론트엔드
  - API
  - Maintainability
  - Readability
  - How-To
  - Tips
  - Comparison
  - 비교
  - Migration
  - 마이그레이션
  - Education
  - 교육
  - Troubleshooting
  - 트러블슈팅
  - Configuration
  - 설정
  - Workflow
  - 워크플로우
  - Productivity
  - 생산성
  - Markdown
  - 마크다운
  - Debugging
  - 디버깅
  - Error-Handling
  - 에러처리
  - Abstraction
  - 추상화
  - Polymorphism
  - 다형성
  - Generic
  - 제네릭
  - Infer
  - Mapped-Types
  - Conditional-Types
  - Advanced
  - Deep-Dive
  - Case-Study
---

## 이 글에서 다루는 내용

- **Reverse Mapped Types**의 정의와 TypeScript에서의 역할
- **제네릭 함수·매핑 타입 역전**과 `infer`를 이용한 타입 추론
- **Box/Unboxify·unwrap** 등 기초 예제와 타입 안전성
- **요구사항**(소스 타입·매핑 타입·제약)과 **한계**(추론 실패·비추론 가능 타입)
- **실전 예제**: 상태 머신, 이벤트 리스너 바인딩, 재귀적 제약
- **FAQ**와 **참고 문헌** 3편

---

## 서론

### 리버스 맵핑 타입이란?

**리버스 맵핑 타입(Reverse Mapped Types)**은 TypeScript에서 “매핑 타입을 역으로 실행”할 수 있게 하는 고급 타입 기능이다. 보통은 **함수의 타입 매개변수를 인자 값으로부터 추론**하는 메커니즘으로 쓰이고, 타입 수준에서는 **`infer`** 키워드로 비슷한 “역방향 추론”을 할 수 있다. 즉, “반환 타입 → 매개변수”가 아니라 **“매개변수(값) → 반환 타입”** 쪽으로 타입을 끌어내는 것이다.

### TypeScript에서의 중요성

TypeScript는 정적 타입으로 **재사용성**과 **타입 안전성**을 높인다. 리버스 맵핑 타입은 이 장점을 더 키워 준다. 복잡한 객체·이벤트·상태 구조를 타입으로만 안전하게 다루고, 컴파일 타임에 잘못된 사용을 걸러 낼 수 있다.

### 이 글의 목적과 구성

이 글은 리버스 맵핑 타입의 **개념 → 활용 → 요구사항·한계 → 실전 예제 → FAQ → 참고 문헌** 순으로 정리한다. 각 절에 코드 예제를 두어, 직접 따라 해 보거나 프로젝트에 적용할 때 참고할 수 있도록 했다.

---

## 리버스 맵핑 타입이란?

### 기본 개념

일반 **매핑 타입**은 기존 타입의 각 프로퍼티를 어떤 규칙으로 **변형**해 새 타입을 만든다.  
**리버스 맵핑 타입**은 그 반대다. “이미 변형된 타입(매핑된 타입)”을 인자로 받아, **원래 소스 타입(또는 그에 대응하는 타입)**을 추론한다.

```mermaid
flowchart LR
  SourceType["소스 타입 T"]
  MappedType["매핑 타입 MappedType T"]
  ReverseStep["역추론 infer"]
  ResultType["결과 타입 T 복원"]
  SourceType --> MappedType
  MappedType --> ReverseStep
  ReverseStep --> ResultType
```

- **정방향**: `T` → `MappedType<T>` (키/값 변형)
- **역방향**: `MappedType<T>` 형태의 **값**을 넘기면, 컴파일러가 그로부터 `T`를 추론

### 제네릭 함수와 타입 추론

제네릭 함수는 “타입을 인자처럼” 쓰고, **호출 시 전달된 값**으로 그 타입을 추론한다.

```typescript
function foo<T>(a: ReadonlyArray<T>): ReadonlyArray<T> {
  return [...a];
}
foo([1, 2, 3]);       // T = number
foo(["a", "b", "c"]); // T = string
```

리버스 맵핑 타입은 이 “값 → 타입 추론”을 **매핑 타입**과 결합해, “매핑된 형태의 객체”를 넘겼을 때 **원본 타입**을 복원하거나, 그에 맞는 반환 타입을 쓰게 한다.

### 매핑 타입의 역전

예를 들어 `Partial<T>`는 모든 프로퍼티를 선택적으로 만든다.  
리버스 맵핑 타입은 “모든 프로퍼티가 `Box<원본값>` 형태인 객체”를 받아, **원본 타입**을 추론해 반환 타입으로 쓴다. 즉, **매핑의 입력(소스 타입)**을 출력 쪽에서 다시 찾아내는 것이다.

### 간단한 예제: Box와 Unboxify

`Box<T>`는 값을 하나 감싸는 타입이다. “역”은 “Box를 벗겨 내서 `T`만 뽑는” 타입이다. 조건부 타입과 `infer`로 표현할 수 있다.

```typescript
type Box<T> = { value: T };

type Unboxify<T> = T extends Box<infer U> ? U : never;

type NumberBox = Box<number>;
type UnboxedNumber = Unboxify<NumberBox>; // number
```

여기서 `Unboxify`는 “`Box<U>` 형태면 `U`를 추출, 아니면 `never`”라는 **타입 수준의 역매핑**이다.  
함수로 쓰면 아래처럼 “값으로부터 타입 추론”이 이뤄진다.

```typescript
type BoxedRecord<T> = {
  [K in keyof T]: Box<T[K]>;
};

function unwrap<T>(record: BoxedRecord<T>): T {
  const result = {} as T;
  for (const key in record) {
    result[key] = record[key].value;
  }
  return result;
}

unwrap({
  a: { value: "hi there" },
  b: { value: 42 },
});
// 반환 타입: { a: string; b: number }
```

`record`의 **값(매핑된 타입)**으로부터 `T`가 역추론되어, 반환 타입이 `T`로 정해진다.

---

## 리버스 맵핑 타입의 활용

### 장점

- **타입 안전성**: 반환 타입이 인자 구조에 맞게 자동으로 결정된다.
- **재사용성**: 한 번 정의한 “역매핑” 타입/함수를 여러 곳에서 재사용할 수 있다.
- **문맥 민감 정보**: 같은 키라도 객체마다 값 타입이 다르면, 각각에 맞는 타입이 추론된다(아래 컨텍스트 민감 예제 참고).

### 타입 추론 과정

컴파일러는 대략 다음 순서로 동작한다.

1. 함수에 넘긴 **인자 타입**을 본다.
2. 인자가 **매핑 타입** 형태인지 확인한다(예: `{ [K in keyof T]: Box<T[K]> }`).
3. 매핑 타입의 “소스”가 될 수 있는 `T`를 **역으로 추론**한다.
4. 그 `T`를 반환 타입 등에 사용한다.

### 실제 예제: unwrap 함수

`Unboxify`를 객체 전체에 적용한 형태다.

```typescript
type Box<T> = { value: T };
type Unboxify<T extends Record<string, Box<unknown>>> = {
  [K in keyof T]: T[K]["value"];
};

function unwrap<T extends Record<string, Box<unknown>>>(record: T): Unboxify<T> {
  const result = {} as Unboxify<T>;
  for (const key in record) {
    result[key] = record[key].value;
  }
  return result;
}

const myBox = unwrap({
  a: { value: "Hello, TypeScript!" },
  b: { value: 42 },
});
// myBox.a: string, myBox.b: number
```

### 타입 안전성

리버스 맵핑 타입을 쓰면 “박스 안에 넣은 타입”과 “실제 값”이 어긋나면 컴파일 시점에 걸러진다.

```typescript
const invalidBox: Box<number> = { value: "This is a string" }; // 컴파일 오류
```

런타임 오류를 줄이고, 리팩터링 시 반환 타입이 자동으로 따라가게 할 수 있다.

---

## 리버스 맵핑 타입의 요구사항

### 소스 타입의 요구사항

- **객체 타입**이어야 하며, 프로퍼티는 키–값 쌍으로 명확히 정의되는 편이 좋다.
- 리버스 맵핑이 “키 집합”과 “값 타입 규칙”을 복원할 수 있도록, 구조가 **일관된 매핑 타입**으로 표현 가능해야 한다.

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};
```

같은 식으로 구조가 정해진 타입은 역매핑과 잘 맞는다.

### 부분적으로 추론 가능한 타입

일부 프로퍼티만 선택적이어도, 추론 가능한 부분만큼은 역매핑이 동작할 수 있다. 다만 “전부 추론”이 안 되는 키가 있으면 그쪽은 `never`나 넓은 타입으로 떨어질 수 있다.

### 매핑 타입의 요구사항

역매핑을 쓰려면, **인자 타입이 “매핑 타입” 형태**여야 한다. 예:

```typescript
type MappedType<T> = {
  [K in keyof T]: T[K];
};
```

이런 식으로 `keyof T`와 `T[K]`가 드러나 있어야, 컴파일러가 `T`를 역으로 풀 수 있다.

### 제약 조건과 타입 추론

제네릭에 `extends`로 제약을 걸면, 역추론이 더 정확해진다.

```typescript
type Unboxify<T extends Record<string, { value: unknown }>> = {
  [K in keyof T]: T[K]["value"];
};
```

“`value`를 가진 객체만” 받겠다고 하면, 그 구조를 가정하고 `T`를 복원한다.

---

## 리버스 맵핑 타입의 한계

### 제약 조건의 복잡성

제약이 여러 개 겹치거나, 매핑 타입이 너무 복잡하면 추론이 실패하거나 `any`/`never`에 가까워질 수 있다. **가능한 한 단순한 매핑 + 단순한 제약**이 유지보수와 동작 예측에 유리하다.

### 타입 추론 실패 시 동작

추론에 실패하면 TypeScript는 해당 제네릭을 넓은 타입(예: `any`)으로 두거나 오류를 낼 수 있다. 그러면 타입 안전성이 떨어지므로, “이 인자면 반드시 T가 추론된다”라고 설계할 수 있는 형태로 매핑 타입을 만드는 것이 좋다.

### 비추론 가능한 타입의 예

- 서로 다른 제네릭이 얽힌 복잡한 객체
- 재귀적으로만 정의된 타입
- “키가 `keyof T`에 없다”처럼 정보가 부족한 매핑

이런 경우에는 역매핑 대신 **명시적 제네릭**이나 **오버로드**를 사용하는 편이 낫다.

---

## 실용적인 예제

### 상태 머신

상태와 이벤트를 타입으로 두고, 설정 객체를 넘기면 **상태 타입**을 역추론하게 할 수 있다.

```typescript
type StateConfig<T> = {
  initial?: keyof T;
  states?: {
    [K in keyof T]: StateConfig<T[K]> & {
      on?: Record<string, keyof T>;
    };
  };
};

declare function createMachine<T>(config: StateConfig<T>): T;

createMachine({
  initial: "a",
  states: {
    a: { on: { NEXT: "a" } },
    b: {
      initial: "nested",
      on: { NEXT: "b" },
      states: {
        nested: { on: { TEST: "nested" } },
      },
    },
  },
});
```

설정 객체의 **구조**로부터 상태 타입 `T`가 역으로 추론된다.

### 이벤트 리스너 바인딩

이벤트 이름과 핸들러를 타입 안전하게 묶을 수 있다.

```typescript
type PossibleEventType<K> = K extends `on${infer Type}` ? Type : never;

type TypeListener<T extends ReadonlyArray<string>> = {
  [I in keyof T]: {
    type: T[I];
    listener: (ev: T[I]) => void;
  };
};

declare function bindAll<
  T extends HTMLElement,
  Types extends ReadonlyArray<PossibleEventType<keyof T>>
>(target: T, listeners: TypeListener<Types>): void;

bindAll({} as HTMLInputElement, [
  { type: "blur",  listener: (ev) => { /* ev: "blur"  */ } },
  { type: "click", listener: (ev) => { /* ev: "click" */ } },
]);
```

`type` 필드 값으로부터 `ev` 타입이 문맥에 맞게 좁혀진다.

### 재귀적 제약 (중첩 객체 매핑)

중첩 객체까지 재귀적으로 매핑·역매핑할 때도 같은 원리가 적용된다.

```typescript
type NestedObject<T> = {
  [K in keyof T]: T[K] extends object ? NestedObject<T[K]> : T[K];
};

type User = {
  name: string;
  address: { city: string; zip: number };
};

type MappedUser = NestedObject<User>;
```

---

## 자주 묻는 질문(FAQ)

**Q. 리버스 맵핑 타입은 언제 쓰면 좋나요?**

API 응답을 “한 겹 감싼 타입”으로 받고, 그걸 풀어서 원본 형태의 타입을 쓰고 싶을 때, 또는 이벤트/상태처럼 “설정 객체 구조 → 타입”을 자동으로 맞추고 싶을 때 유용하다.

**Q. 성능(컴파일 타임)에는 어떤 영향이 있나요?**

타입은 컴파일 타임에만 사용되므로 **런타임 성능**에는 영향이 없다. 다만 매핑/역매핑이 매우 복잡하면 **컴파일 시간**이 늘어날 수 있으므로, 필요한 범위에서만 쓰고 단순하게 유지하는 것이 좋다.

**Q. 일반 매핑 타입과의 차이는 무엇인가요?**

- **일반 매핑 타입**: `T` → `MappedType<T>` (정방향, “타입을 변형”).
- **리버스 맵핑 타입**: “매핑된 형태의 값”을 넘기면, 그로부터 **소스 타입 `T`를 추론**해 반환 타입 등에 사용. 방향이 반대이고, **값 기반 추론**이 핵심이다.

---

## 관련 기술

- **TypeScript 제네릭**: 타입 매개변수로 재사용 가능한 타입/함수 정의.
- **조건부 타입(Conditional Types)**: `T extends U ? A : B`와 **`infer`**로 타입 추출. 리버스 맵핑의 “역추론”은 여기서 많이 쓰인다.
- **매핑 타입(Mapped Types)**: `[K in keyof T]: ...` 형태로 타입을 변형. 역매핑의 “정방향”에 해당한다.

공식 핸드북의 [Creating Types from Types](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html), [Conditional Types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html), [Mapped Types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html)를 함께 보면 이해에 도움이 된다.

---

## 결론

- **리버스 맵핑 타입**은 “매핑 타입을 역으로 실행”해, **인자(값)로부터 타입 매개변수를 추론**하게 하는 TypeScript 기능이다.
- **Box/Unboxify·unwrap** 같은 단순 예제로 시작해, **상태 머신·이벤트 바인딩**처럼 실전 패턴에 적용할 수 있다.
- **요구사항**(객체 형태, 매핑 타입 구조, 제약)과 **한계**(복잡한 제약, 추론 실패, 비추론 가능 타입)를 알고 쓰면, 타입 안전성과 개발 경험을 동시에 높일 수 있다.

추가로 TypeScript 공식 문서와 아래 참고 문헌을 참고하면, `infer`와 매핑 타입을 더 깊이 다룰 수 있다.

---

## Reference

1. [What the heck are reverse mapped types?](https://andreasimonecosta.dev/posts/what-the-heck-are-reverse-mapped-types/) — Andrea Simone Costa. 리버스 맵핑 타입 개념과 컴파일러 동작 설명.
2. [TypeScript: Creating Types from Types](https://www.typescriptlang.org/docs/handbook/2/types-from-types.html) — TypeScript 공식 핸드북. 제네릭·매핑·조건부 타입 등 타입 조작 개요.
3. [TypeScript: Conditional Types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html) — TypeScript 공식 핸드북. `infer`를 사용한 타입 추론과 조건부 타입.
