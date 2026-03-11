---
draft: true
title: "[Redux] 00. 커리큘럼 - 학습 로드맵"
date: 2026-03-11
lastmod: 2026-03-11
description: "Redux 완전 정복 시리즈의 전체 커리큘럼과 Phase별 챕터 목록, 추천 학습 경로를 한눈에 정리한 도입 챕터. JavaScript 기초부터 실무 마스터까지 30편 구성과 학습 순서를 확인한 뒤 01편부터 순서대로 시작할 수 있습니다."
slug: getting-started-redux
tags:
  - JavaScript
  - TypeScript
  - React
  - Frontend
  - 프론트엔드
  - Web
  - 웹
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - State
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
  - Performance
  - 성능
  - Functional-Programming
  - 함수형프로그래밍
  - Observer
  - Event-Driven
  - API
  - Async
  - 비동기
  - Caching
  - 캐싱
  - Scalability
  - 확장성
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
  - Data-Structures
  - 자료구조
  - Git
  - IDE
  - VSCode
  - How-To
  - Tips
  - Technology
  - 기술
  - Education
  - 교육
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
  - Optimization
  - 최적화
  - Type-Safety
  - Interface
  - 인터페이스
  - Encapsulation
  - 캡슐화
  - Configuration
  - 설정
collection_order: 0
---

# Redux 완전 정복 - 초보부터 전문가까지

**Redux**는 JavaScript 앱을 위한 예측 가능한 **상태 관리** 라이브러리입니다. 복잡해지는 프론트엔드에서 "어떤 화면에서든 같은 데이터를 일관되게 다루고, 변경 이력을 추적할 수 있는 구조"가 필요해졌고, Flux 패턴을 단순화한 Redux가 그 답이 되었습니다.

> "You might not need Redux." — Dan Abramov, [You Might Not Need Redux (2016)](https://medium.com/@dan_abramov/you-might-not-need-redux-be46360cf367). Redux는 만능이 아니지만, **상태 관리**가 복잡해지는 순간 선택지가 됩니다. 이 시리즈는 그 선택을 할 수 있도록, 기초부터 실무까지 체계적으로 다룹니다.

이 챕터는 시리즈 소개이자 커리큘럼·학습 방법·참고 자료를 한곳에 모은 도입 페이지입니다. **왜 이 페이지부터 읽어야 할까요?** 실제 Redux 코드를 작성하기 전에, 전체 로드맵을 보면 "지금 내가 어디쯤에 있는지"와 "다음에 무엇을 배우면 되는지"를 항상 확인할 수 있습니다. 그래서 01편으로 들어가기 직전에, 이 커리큘럼 한 번만 훑어 두는 것을 권합니다.

## 프로젝트 개요

이 절에서는 이 시리즈가 어떤 목표를 두고, 어떤 독자를 위한 것인지 한눈에 정리합니다.

이 프로젝트는 **JavaScript를 잘 다루지 못하는 개발자도 Redux를 통해 SW 전문가 수준으로 성장**할 수 있도록 설계된 체계적인 학습 가이드입니다.

총 **30편**의 글을 통해 JavaScript 기초부터 **Redux**의 고급 기법까지, 현대적인 Redux Toolkit과 RTK Query를 활용한 실무 능력을 완벽하게 습득합니다.

## 학습 목표

- JavaScript/TypeScript 기초부터 Redux까지 단계적 학습
- Redux Toolkit을 활용한 현대적인 상태 관리 패턴 마스터
- React-Redux Hooks를 통한 효율적인 컴포넌트 연동
- 비동기 처리와 사이드 이펙트 관리 (Thunk, Saga, RTK Query)
- 실전 프로젝트를 통한 아키텍처 설계 및 최적화 능력 배양
- 테스팅, 디버깅, 성능 최적화 등 전문가 수준의 실무 역량 개발

## 커리큘럼 한눈에 보기

아래는 Phase별로 어떤 주제를 다루는지, 그리고 각 편의 제목과 링크를 한 테이블로 모은 것입니다. 학습 순서를 정할 때 이 표를 기준으로 "다음에 읽을 글"을 고르면 됩니다.

### Phase 1: JavaScript/TypeScript 기초 다지기 (1-5편)

이 절에서는 1~5편이 다루는 범위와, Redux 학습과의 연결을 요약합니다.

JavaScript를 잘 모르는 분을 위한 필수 기초입니다.

| 편 | 제목 | 링크 |
|----|------|------|
| 01 | JavaScript 핵심 개념 - 변수, 함수, 객체 | [01. JavaScript 핵심 개념](01-javascript-fundamentals/) |
| 02 | ES6+ 필수 문법 - 구조 분해, 스프레드, 템플릿 리터럴 | [02. ES6+ 필수 문법](02-es6-essential-syntax/) |
| 03 | 배열과 객체 다루기 - map, filter, reduce | [03. 배열과 객체 다루기](03-array-object-manipulation/) |
| 04 | 비동기 JavaScript - Promise와 async/await | [04. 비동기 JavaScript](04-asynchronous-javascript/) |
| 05 | TypeScript 기초 - 타입 시스템 이해하기 | [05. TypeScript 기초](05-typescript-basics/) |

### Phase 2: Redux 핵심 개념 (6-10편)

앞의 Phase 1이 JS/TS 기초라면, 이 Phase에서는 Redux 자체의 개념에 집중합니다.

Redux의 철학과 기본 원리를 완전히 이해하는 단계입니다.

| 편 | 제목 | 링크 |
|----|------|------|
| 06 | Redux란 무엇인가 - Flux 아키텍처와 상태 관리 | [06. Redux란 무엇인가](06-what-is-redux/) |
| 07 | Redux의 핵심 - Action, Reducer, Store | [07. Redux 핵심 개념](07-redux-core-concepts/) |
| 08 | 불변성의 중요성 - Immutability in Redux | [08. 불변성](08-immutability-in-redux/) |
| 09 | Redux 데이터 흐름 이해하기 | [09. Redux 데이터 흐름](09-redux-data-flow/) |
| 10 | Redux를 사용하는 이유와 적절한 사용 시기 | [10. 언제 Redux를 쓸까](10-when-to-use-redux/) |

### Phase 3: React-Redux 연동 (11-15편)

Redux 개념을 익힌 뒤, 실제 화면(React 컴포넌트)과 Store를 어떻게 연결하는지 다룹니다.

React와 Redux를 효과적으로 연결하는 단계입니다.

| 편 | 제목 | 링크 |
|----|------|------|
| 11 | React-Redux 시작하기 - Provider와 connect | [11. React-Redux 시작하기](11-react-redux-basics/) |
| 12 | React-Redux Hooks - useSelector와 useDispatch | [12. React-Redux Hooks](12-react-redux-hooks/) |
| 13 | 컴포넌트 최적화 - 리렌더링 제어 | [13. 컴포넌트 최적화](13-component-optimization/) |
| 14 | 데이터 선택자 - Selector 패턴 | [14. Selector 패턴](14-selector-patterns/) |
| 15 | 실습: Counter와 Todo 앱 만들기 | [15. 실습: Counter와 Todo](15-practice-counter-todo/) |

### Phase 4: Redux Toolkit - 현대적인 Redux (16-20편)

Redux Toolkit으로 생산성을 높이는 단계입니다. (챕터 예정)

| 편 | 제목 |
|----|------|
| 16 | Redux Toolkit 소개 - 왜 RTK인가? |
| 17 | createSlice - 간결한 리듀서 작성 |
| 18 | configureStore - Store 설정 자동화 |
| 19 | createAsyncThunk - 비동기 액션 간편화 |
| 20 | 실습: Redux Toolkit으로 실전 앱 만들기 |

### Phase 5: 미들웨어와 사이드 이펙트 (21-25편)

비동기 처리와 복잡한 로직을 다루는 단계입니다. (챕터 예정)

| 편 | 제목 |
|----|------|
| 21 | Redux 미들웨어의 이해 |
| 22 | Redux Thunk - 가장 간단한 비동기 처리 |
| 23 | Redux Saga - 강력한 사이드 이펙트 관리 |
| 24 | RTK Query - 데이터 페칭의 혁명 |
| 25 | 실습: RTK Query로 블로그 앱 만들기 |

### Phase 6: 고급 패턴과 아키텍처 (26-28편)

전문가 수준의 Redux 아키텍처 설계 단계입니다. (챕터 예정)

| 편 | 제목 |
|----|------|
| 26 | Redux 프로젝트 구조 - 확장 가능한 설계 |
| 27 | 정규화 (Normalization) - 복잡한 데이터 관리 |
| 28 | Redux와 TypeScript - 타입 안전한 상태 관리 |

### Phase 7: 실무 마스터 레벨 (29-30편)

실전 프로젝트와 최적화, 테스팅 단계입니다. (챕터 예정)

| 편 | 제목 |
|----|------|
| 29 | Redux 성능 최적화와 디버깅 |
| 30 | 테스팅과 실전 프로젝트 - E-Commerce 앱 |

아래는 Phase별 상세 목차입니다.

### Phase별 상세 목차

**Phase 1 (1-5편)**  
1. [JavaScript 핵심 개념 - 변수, 함수, 객체](01-javascript-fundamentals/) — 변수 선언 (var, let, const), 함수 정의와 화살표 함수, 객체와 배열 기본 조작  
2. [ES6+ 필수 문법 - 구조 분해, 스프레드, 템플릿 리터럴](02-es6-essential-syntax/) — 구조 분해 할당, 스프레드 연산자와 Rest 파라미터, 템플릿 리터럴  
3. [배열과 객체 다루기 - map, filter, reduce](03-array-object-manipulation/) — 고차 함수, map/filter/reduce, 불변성 유지 패턴  
4. [비동기 JavaScript - Promise와 async/await](04-asynchronous-javascript/) — 비동기 필요성, Promise, async/await  
5. [TypeScript 기초 - 타입 시스템 이해하기](05-typescript-basics/) — 기본 타입과 인터페이스, 제네릭 기초  

**Phase 2 (6-10편)**  
6. [Redux란 무엇인가 - Flux 아키텍처와 상태 관리](06-what-is-redux/)  
7. [Redux의 핵심 - Action, Reducer, Store](07-redux-core-concepts/)  
8. [불변성의 중요성 - Immutability in Redux](08-immutability-in-redux/)  
9. [Redux 데이터 흐름 이해하기](09-redux-data-flow/)  
10. [Redux를 사용하는 이유와 적절한 사용 시기](10-when-to-use-redux/)  

**Phase 3 (11-15편)**  
11. [React-Redux 시작하기 - Provider와 connect](11-react-redux-basics/)  
12. [React-Redux Hooks - useSelector와 useDispatch](12-react-redux-hooks/)  
13. [컴포넌트 최적화 - 리렌더링 제어](13-component-optimization/)  
14. [데이터 선택자 - Selector 패턴](14-selector-patterns/)  
15. [실습: Counter와 Todo 앱 만들기](15-practice-counter-todo/)  

**Phase 4~7 (16-30편, 예정)**  
16. Redux Toolkit 소개 — 17. createSlice — 18. configureStore — 19. createAsyncThunk — 20. 실습 RTK 앱 — 21. 미들웨어 — 22. Thunk — 23. Saga — 24. RTK Query — 25. 실습 블로그 앱 — 26. 프로젝트 구조 — 27. 정규화 — 28. Redux와 TypeScript — 29. 성능 최적화와 디버깅 — 30. 테스팅과 E-Commerce 앱

## 각 글의 구성

이 절에서는 **한 편 한 편의 챕터가 어떤 블록으로 이루어져 있는지**를 요약합니다. 글을 읽을 때 "학습 목표 → 핵심 개념 → 실습 코드 → 체크리스트" 순서로 보면 효율적입니다.

각 챕터는 다음과 같은 구조로 구성됩니다:

### **기본 구성**
- **학습 목표**: 이 챕터에서 달성할 구체적인 학습 목표
- **핵심 개념**: 반드시 이해해야 할 핵심 내용
- **실습 코드**: 직접 따라할 수 있는 예제 코드
- **흔한 실수**: 초보자가 자주 하는 실수와 해결 방법
- **체크리스트**: 학습 완료 확인을 위한 체크리스트

### **JavaScript 기초 챕터 (1-5편)**
- **왜 배워야 하는가**: 해당 개념이 Redux에서 어떻게 사용되는지
- **단계별 설명**: 초보자도 이해할 수 있는 상세한 설명
- **실습 문제**: 손으로 직접 코딩하며 익히는 연습 문제

### **Redux 실전 챕터 (6-30편)**
- **실무 사례**: 실제 프로젝트에서의 활용 예시
- **Best Practices**: 업계 표준 패턴과 모범 사례
- **안티패턴**: 피해야 할 나쁜 패턴들
- **심화 학습**: 더 깊이 공부하고 싶은 분들을 위한 고급 주제

## 학습 방법론

여기서는 **어떤 순서로, 얼마나 시간을 두고 학습할지**에 대한 실질적인 가이드를 다룹니다. "초보자를 위한 단계적 접근"과 "효과적인 학습 프로세스"를 먼저 읽은 뒤, 자신에 맞는 "추천 학습 경로"를 선택하면 됩니다.

### 초보자를 위한 단계적 접근

1. **JavaScript 기초 탄탄히** (1-5편)  
   급하게 넘어가지 말고 충분히 연습, 모든 예제 코드를 직접 타이핑, 에러를 두려워하지 말고 실험하기.

2. **Redux 개념 완벽 이해** (6-10편)  
   각 개념의 '왜'를 이해하기, 그림과 다이어그램으로 시각화, 작은 예제부터 시작.

3. **실습으로 체화** (11-30편)  
   이론 학습 후 반드시 실습, 에러 메시지 읽는 법 익히기, 공식 문서 참조 습관 들이기.

### 효과적인 학습 프로세스

한 편의 글을 "읽기만 하고 끝" 내지 "코드만 복사해서 실행"하면 기억에 잘 남지 않습니다. 아래 흐름은 **개념 학습 → 따라하기 → 응용 → 실습 → 복습**까지 한 사이클을 정리한 것입니다. 각 단계를 건너뛰지 않고 따라가면 이해가 오래 유지되고, 실무에서 바로 꺼내 쓸 수 있습니다.

```
1. 개념 학습 (읽기)
   ↓
2. 예제 따라하기 (타이핑)
   ↓
3. 변형해보기 (응용)
   ↓
4. 문제 해결하기 (실습)
   ↓
5. 복습과 정리 (체크리스트)
```

이 사이클을 한 챕터마다 한 번씩 적용해 보세요. 특히 2번(직접 타이핑)과 4번(실습 문제)을 생략하면 "알 것 같은데 막상 코드를 못 짜는" 상태가 되기 쉽습니다.

### 학습 팁

- **하루 1-2시간, 꾸준히**: 한꺼번에 많이 하는 것보다 매일 조금씩
- **손으로 직접 코딩**: 복사-붙여넣기 금지!
- **에러는 친구**: 에러 메시지를 읽고 이해하는 연습
- **커뮤니티 활용**: 막힐 때는 질문하기 (Stack Overflow, Discord)
- **프로젝트 만들기**: 배운 내용으로 작은 프로젝트 직접 만들어보기

## 기대 효과

이 시리즈를 완주하면 다음과 같은 역량을 갖추게 됩니다:

### **기술적 역량**
- Modern JavaScript/TypeScript 능숙한 사용
- Redux/Redux Toolkit을 활용한 상태 관리 마스터
- React-Redux를 통한 효율적인 컴포넌트 설계
- 비동기 처리와 사이드 이펙트 관리 능력

### **실무 능력**
- 실전 프로젝트 구조 설계 및 구현
- 성능 최적화와 디버깅 기법
- 테스트 작성과 코드 품질 관리
- 확장 가능한 아키텍처 설계

### **전문가 수준**
- Redux 공식 문서를 스스로 읽고 학습하는 능력
- 새로운 라이브러리와 패턴을 빠르게 습득
- 팀원들에게 Redux를 가르칠 수 있는 수준
- 복잡한 상태 관리 문제를 설계부터 해결까지 완수

## 이 시리즈를 읽은 후 달성해야 할 목표 (평가 기준)

다음 항목을 스스로 설명·선택·구현할 수 있으면 학습 목표를 달성한 것입니다.

| 영역 | 평가 기준 |
|------|-----------|
| 개념 | **상태 관리**가 왜 필요한지, Flux/Redux의 단방향 데이터 흐름을 설명할 수 있다. |
| 원칙 | Redux의 세 가지 원칙(Single Source of Truth, Read-Only State, Pure Reducers)을 설명하고 코드로 보여줄 수 있다. |
| 판단 | 프로젝트 규모·요구사항에 따라 Redux를 쓸지, Context API 등 대안을 쓸지 판단할 수 있다. |
| 구현 | Action, Reducer, Store를 조합해 작은 앱(Counter, Todo)을 구현할 수 있다. |
| 연동 | React-Redux(Provider, connect 또는 Hooks)로 컴포넌트와 Store를 연결할 수 있다. |
| 최적화 | 불필요한 리렌더링을 줄이기 위해 selector·메모이제이션·React.memo를 적용할 수 있다. |

## 사용법

### **추천 학습 경로**

**1. JavaScript 초보자**  
Phase 1 (1-5편) → Phase 2 (6-10편) → Phase 3 (11-15편) → Phase 4 (16-20편) → Phase 5 (21-25편) → Phase 6-7 (26-30편).  
**예상 소요 시간**: 3-4개월 (하루 1-2시간)

**2. JavaScript는 알지만 Redux는 처음**  
Phase 1 (빠르게 복습) → Phase 2 (6-10편) → Phase 4 (16-20편) → Phase 3 (11-15편) → Phase 5 (21-25편) → Phase 6-7 (26-30편).  
**예상 소요 시간**: 2-3개월

**3. 기존 Redux 사용자 (RTK 학습 목적)**  
Phase 4 (16-20편) → Phase 5 (21-25편) → Phase 6-7 (26-30편).  
**예상 소요 시간**: 1-2개월

### **참고 학습 방법**
- 특정 주제가 궁금할 때 해당 챕터만 선택적으로 학습
- 실무에서 문제 발생 시 관련 챕터 참조
- 코드 리뷰나 아키텍처 설계 시 Best Practices 참고

## 실습 프로젝트

### **Phase별 프로젝트**

**Phase 3: 기본 앱**  
- **Counter 앱**: Redux 기초 이해  
- **Todo 앱**: CRUD 작업과 상태 관리  

**Phase 4: 실전 앱**  
- **사용자 관리 시스템**: Redux Toolkit 활용  
- **날씨 앱**: API 연동과 비동기 처리  

**Phase 5: 고급 앱**  
- **블로그 앱**: RTK Query로 완전한 CRUD  
- **소셜 미디어 피드**: 무한 스크롤과 캐싱  

**Phase 7: 최종 프로젝트**  
- **E-Commerce 앱**: 장바구니, 결제, 주문 관리 — 상품 목록 및 검색, 장바구니 관리, 사용자 인증, 주문 처리, 결제 시뮬레이션

## 참고 자료

### **공식 문서**
- [Redux 공식 문서](https://redux.js.org/)
- [Redux Toolkit 공식 문서](https://redux-toolkit.js.org/)
- [React-Redux 공식 문서](https://react-redux.js.org/)
- [RTK Query 공식 문서](https://redux-toolkit.js.org/rtk-query/overview)

### **추천 학습 자료**
- [Redux Essentials 튜토리얼](https://redux.js.org/tutorials/essentials/part-1-overview-concepts)
- [Redux Fundamentals 튜토리얼](https://redux.js.org/tutorials/fundamentals/part-1-overview)
- [Egghead.io - Redux 코스](https://egghead.io/courses/fundamentals-of-redux-course-from-dan-abramov-bd5cc867)

### **유용한 도구**
- [Redux DevTools Extension](https://github.com/reduxjs/redux-devtools)
- [Redux Toolkit Templates](https://redux-toolkit.js.org/introduction/getting-started#using-create-react-app)
- [TypeScript Redux Template](https://github.com/reduxjs/cra-template-redux-typescript)

## 커리큘럼 맵

Phase 1부터 7까지의 **진행 순서**와 **Phase 간 연결 관계**를 한눈에 보려면 아래 다이어그램을 참고하세요. Phase 2(Redux 핵심)를 마친 뒤에는 Phase 3(React-Redux)과 Phase 4(Redux Toolkit) 중 어느 쪽을 먼저 갈지 선택할 수 있고, 두 경로 모두 Phase 5(미들웨어)로 합쳐집니다. 자신의 수준(JS 초보인지, Redux만 새로 배우는지)에 맞는 경로를 골라 순서대로 진행하면 됩니다.

```mermaid
flowchart TD
  subgraph phase1 [Phase 1]
    JS["JavaScript</br>기초 (1-5편)"]
  end
  subgraph phase2 [Phase 2]
    ReduxCore["Redux 핵심 개념</br>(6-10편)"]
  end
  subgraph phase3 [Phase 3]
    ReactRedux["React-Redux 연동</br>(11-15편)"]
  end
  subgraph phase4 [Phase 4]
    RTK["Redux Toolkit</br>(16-20편)"]
  end
  subgraph phase5 [Phase 5]
    Middleware["미들웨어 and 사이드 이펙트</br>(21-25편)"]
  end
  subgraph phase6 [Phase 6]
    Advanced["고급 패턴 and 아키텍처</br>(26-28편)"]
  end
  subgraph phase7 [Phase 7]
    Master["실무 마스터</br>(29-30편)"]
  end
  JS --> ReduxCore
  ReduxCore --> ReactRedux
  ReduxCore --> RTK
  ReactRedux --> Middleware
  RTK --> Middleware
  Middleware --> Advanced
  Advanced --> Master
```

(노드 라벨의 `&`는 Mermaid 파서 호환을 위해 `and`로 표기했습니다.)

위 맵에서 화살표는 "이 Phase를 끝낸 뒤 다음으로 권장하는 Phase"를 의미합니다. 실제 학습 시에는 "추천 학습 경로" 절의 시나리오(초보자 / Redux만 처음 / RTK 목적)에 맞는 경로를 선택하면 됩니다.

## 학습 지원

- **자주 묻는 질문**: 각 챕터마다 FAQ 섹션이 포함되어 있습니다.
- **트러블슈팅**: 흔한 에러와 해결 방법을 상세히 설명합니다.
- **커뮤니티**: [Reactiflux Discord](https://www.reactiflux.com/), [Stack Overflow - Redux 태그](https://stackoverflow.com/questions/tagged/redux), [Reddit - r/reactjs](https://www.reddit.com/r/reactjs/)

---

**"Redux를 배우는 것은 단순히 라이브러리를 익히는 것이 아니라, 상태 관리에 대한 깊은 이해를 얻는 여정입니다."**

JavaScript를 잘 모르는 당신도, 이 시리즈를 마치면 Redux 전문가가 될 수 있습니다.

**Let's start your Redux journey!**

## 다음 단계

다음 챕터부터 시작하세요: [01. JavaScript 핵심 개념 - 변수, 함수, 객체](01-javascript-fundamentals/).
