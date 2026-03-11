---
draft: true
title: "[Redux] 10. Redux를 사용하는 이유와 적절한 사용 시기"
date: 2025-10-14
lastmod: 2025-10-14
description: "Redux 도입 결정을 위한 완벽 가이드. Redux가 필요한 경우와 불필요한 경우, Context API와 다른 상태 관리 라이브러리와의 비교, 프로젝트 규모별 최적 선택 기준을 실전 사례로 학습합니다."
slug: when-to-use-redux
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
  - Scalability
  - 확장성
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
  - Data-Structures
  - 자료구조
  - API
  - Async
  - 비동기
  - Caching
  - 캐싱
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
  - Encapsulation
  - 캡슐화
series: ["Redux 완전 정복"]
series_order: 10
---

06~09장에서 Redux의 개념과 데이터 흐름을 익혔다면, 이 장에서는 **언제 Redux를 도입하고 언제 피할지**를 판단하는 기준을 다룹니다. "Redux는 만능이 아니다"는 Dan Abramov의 글을 참고로, 장단점·대안(Context API, Zustand 등)·프로젝트 규모에 따른 선택을 정리합니다. Phase 2(Redux 핵심)를 마무리하는 장이므로, 다음 Phase 3(React-Redux)로 넘어가기 전에 한 번 정리해 두면 좋습니다.

## 이 글을 읽은 후 달성해야 할 목표 (평가 기준)

이 챕터를 마치면 다음을 할 수 있어야 합니다:

- Redux의 장단점을 설명하고, 프로젝트 규모·요구사항에 따라 Redux를 쓸지 말지 **판단**할 수 있다.
- Context API, MobX, Zustand 등 대안과 비교하고, 상황에 맞는 **선택**을 할 수 있다.
- Redux 없이 시작했다가 나중에 도입하는 전략을 설명할 수 있다.

## Redux는 만능이 아닙니다

Redux 창시자 Dan Abramov의 말:

> "Redux를 사용하지 않고도 멋진 앱을 만들 수 있습니다. 실제로 대부분의 앱은 Redux가 필요하지 않습니다."  
> — Dan Abramov, [You Might Not Need Redux (2016)](https://medium.com/@dan_abramov/you-might-not-need-redux-be46360cf367)

```javascript
// ❌ 잘못된 사고방식
"React 앱 = 무조건 Redux"

// ✅ 올바른 사고방식
"문제 파악 → 적절한 도구 선택 → Redux는 선택지 중 하나"
```

## Redux의 장점

Redux를 쓸지 말지는 **상태 복잡도**·**팀 규모**·**디버깅·테스트 요구**에 따라 결정하는 것이 좋습니다. 아래는 Redux가 빛을 발하는 대표적인 장점들입니다. 각 항목은 "일반 React state vs Redux" 비교로 이해하면 선택에 도움이 됩니다.

### 예측 가능한 상태 관리

```javascript
// Redux: 모든 상태 변화가 명시적
dispatch({ type: 'INCREMENT' });
// State가 어떻게 변경되는지 명확

// vs 일반 setState
setCount(count + 1);
// 여러 곳에서 호출되면 추적 어려움
```

### 중앙 집중식 상태

**Store** 하나에서 **전역 state**를 관리하면 컴포넌트 간 동기화 부담이 줄고, **useSelector**로 필요한 슬라이스만 구독할 수 있습니다. 반대로 state가 여러 컴포넌트에 흩어지면 공유·갱신 시점을 맞추기 어렵습니다.

```javascript
// ✅ Redux: 한 곳에서 모든 상태 관리
const state = {
    user: { ... },
    todos: [ ... ],
    settings: { ... }
};

// ❌ 분산된 상태
// 컴포넌트 A에 user
// 컴포넌트 B에 todos
// 컴포넌트 C에 settings
// → 동기화 어려움
```

### Time Travel Debugging

```javascript
// Redux DevTools로 가능
// 1. 이전 상태로 되돌리기
// 2. 특정 Action 재실행
// 3. State 변화 추적

// 일반 React State로는 불가능
```

### Middleware 확장성

```javascript
// 로깅, 비동기 처리, API 호출 등 확장 가능
const store = configureStore({
    reducer: rootReducer,
    middleware: [
        logger,
        thunk,
        api,
        crashReporter
    ]
});
```

### 서버 사이드 렌더링 (SSR)

```javascript
// Redux는 SSR과 잘 맞음
// 1. 서버에서 초기 상태 생성
const preloadedState = await fetchData();

// 2. 클라이언트로 전달
const store = createStore(reducer, preloadedState);

// 3. 클라이언트에서 hydration
```

### 강력한 생태계

```
- Redux DevTools
- Redux Toolkit
- RTK Query
- Redux Persist
- Redux Saga
- Reselect
- 수많은 미들웨어
```

## Redux의 단점

### 보일러플레이트 코드

```javascript
// Redux: 많은 설정 필요
// 1. Action Types
const ADD_TODO = 'ADD_TODO';

// 2. Action Creators
const addTodo = (text) => ({ type: ADD_TODO, payload: text });

// 3. Reducer
function todoReducer(state = [], action) { ... }

// 4. Store 설정
const store = createStore(reducer);

// vs Context API: 간단
const TodoContext = createContext();
const [todos, setTodos] = useState([]);
```

### 학습 곡선

```javascript
// 배워야 할 것들
// - Redux 기본 개념 (Action, Reducer, Store)
// - 불변성
// - Middleware
// - Thunk/Saga (비동기)
// - Selector
// - Redux Toolkit
// - DevTools
// → 초보자에게 부담
```

### 작은 앱에는 과함

```javascript
// 간단한 Todo 앱
// Redux: 100줄 이상
// useState: 20줄

// Counter 앱
// Redux: 50줄
// useState: 5줄
```

### 간접성 (Indirection)

```javascript
// Redux: 여러 파일을 거침
// actions/todos.js → types.js → reducers/todos.js → store.js → Component

// useState: 직접적
// const [todos, setTodos] = useState([]);
```

## Redux가 필요한 경우 ✅

### 여러 컴포넌트가 같은 상태 공유

```javascript
// ✅ Redux 적합
<App>
  <Header user={user} /> {/* 사용자 정보 */}
  <Sidebar user={user} /> {/* 사용자 정보 */}
  <Main>
    <Profile user={user} /> {/* 사용자 정보 */}
    <Settings user={user} /> {/* 사용자 정보 */}
    <ActivityFeed user={user} /> {/* 사용자 정보 */}
  </Main>
  <Footer user={user} /> {/* 사용자 정보 */}
</App>

// Redux 없이는 Props Drilling 지옥
```

### 복잡한 상태 업데이트 로직

```javascript
// ✅ Redux 적합: 복잡한 상태 전환
function orderReducer(state = initialState, action) {
    switch (action.type) {
        case 'PLACE_ORDER':
            // 재고 확인
            // 가격 계산
            // 쿠폰 적용
            // 배송비 계산
            // 포인트 적용
            // 최종 금액 계산
            return { ... };
        
        case 'CANCEL_ORDER':
            // 환불 처리
            // 재고 복구
            // 포인트 환급
            return { ... };
    }
}

// useState로는 관리 어려움
```

### 상태 변화를 추적해야 할 때

```javascript
// ✅ Redux 적합
// - 디버깅 필요
// - 로깅 필요
// - 사용자 행동 분석
// - Undo/Redo 기능

// Redux DevTools로 모든 Action 추적 가능
```

### 팀 협업

```javascript
// ✅ Redux 적합
// - 명확한 패턴과 규칙
// - 코드 리뷰 용이
// - 일관된 상태 관리
// - 새 팀원 온보딩 쉬움

// vs 각자 다른 방식으로 상태 관리
```

### 서버 상태와 클라이언트 상태 혼재

```javascript
// ✅ Redux 적합
const state = {
    // 서버 상태
    user: { ... },
    posts: [ ... ],
    comments: [ ... ],
    
    // 클라이언트 상태
    ui: {
        isMenuOpen: false,
        theme: 'dark',
        selectedTab: 'home'
    }
};
```

## Redux가 불필요한 경우 ❌

### 작은 앱 (컴포넌트 5개 미만)

```javascript
// ❌ Redux 과함
// Simple Todo App
// - TodoList
// - TodoItem
// - TodoForm

// ✅ useState로 충분
function App() {
    const [todos, setTodos] = useState([]);
    return <TodoList todos={todos} setTodos={setTodos} />;
}
```

### 지역 상태만 있는 경우

```javascript
// ❌ Redux 불필요
function Form() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    // 이 상태들은 Form 컴포넌트에서만 사용
    // Redux 필요 없음
}
```

### 단순한 CRUD 앱

```javascript
// ❌ Redux 과함
// - 데이터 조회
// - 데이터 추가
// - 데이터 수정
// - 데이터 삭제

// ✅ React Query나 SWR로 충분
function TodoList() {
    const { data: todos } = useQuery('todos', fetchTodos);
    const mutation = useMutation(addTodo);
    
    // 서버 상태 관리는 React Query가 더 나음
}
```

### 프로토타입/MVP

```javascript
// ❌ Redux로 시작하면 개발 느림
// ✅ 빠른 개발이 중요
// → useState, Context API로 시작
// → 필요하면 나중에 Redux 추가
```

## 대안 비교

### Context API

```javascript
// 장점
// - React 내장
// - 간단한 API
// - 작은 앱에 적합

// 단점
// - 성능 최적화 어려움
// - 미들웨어 없음
// - DevTools 없음

// 사용 시기
// - 테마, 언어 등 전역 설정
// - 사용자 정보 (읽기 위주)
// - 5개 미만의 전역 상태

// Context API 예제
const ThemeContext = createContext();

function App() {
    const [theme, setTheme] = useState('dark');
    
    return (
        <ThemeContext.Provider value={{ theme, setTheme }}>
            <Layout />
        </ThemeContext.Provider>
    );
}
```

### MobX

```javascript
// 장점
// - 자동 반응성
// - 간단한 API
// - 보일러플레이트 적음

// 단점
// - "마법" 같은 동작
// - 디버깅 어려움
// - 암시적 동작

// MobX 예제
import { makeObservable, observable, action } from 'mobx';

class TodoStore {
    todos = [];
    
    constructor() {
        makeObservable(this, {
            todos: observable,
            addTodo: action
        });
    }
    
    addTodo(text) {
        this.todos.push({ id: Date.now(), text });
        // 자동으로 컴포넌트 업데이트
    }
}
```

### Zustand

```javascript
// 장점
// - 매우 간단
// - 보일러플레이트 최소
// - Redux와 비슷한 패턴

// 단점
// - 작은 생태계
// - DevTools 제한적

// Zustand 예제
import create from 'zustand';

const useStore = create(set => ({
    count: 0,
    increment: () => set(state => ({ count: state.count + 1 }))
}));

function Counter() {
    const { count, increment } = useStore();
    return <button onClick={increment}>{count}</button>;
}
```

### Recoil

```javascript
// 장점
// - React 친화적
// - 원자적 상태
// - 비동기 지원

// 단점
// - 실험적
// - 작은 커뮤니티

// Recoil 예제
import { atom, useRecoilState } from 'recoil';

const countState = atom({
    key: 'count',
    default: 0
});

function Counter() {
    const [count, setCount] = useRecoilState(countState);
    return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### React Query / SWR

```javascript
// 장점
// - 서버 상태 관리 특화
// - 캐싱, 재검증 자동
// - Redux보다 간단

// 사용 시기
// - API 데이터 위주
// - 서버 상태가 대부분

// React Query 예제
import { useQuery, useMutation } from 'react-query';

function Todos() {
    const { data: todos } = useQuery('todos', fetchTodos);
    const mutation = useMutation(addTodo);
    
    return <div>{/* ... */}</div>;
}
```

## 선택 기준표

### 프로젝트 규모별

```
🟢 소형 (컴포넌트 < 10개)
→ useState + useContext

🟡 중형 (컴포넌트 10-50개)
→ Zustand or Context API + React Query

🔴 대형 (컴포넌트 > 50개)
→ Redux Toolkit

🔵 엔터프라이즈
→ Redux Toolkit + RTK Query
```

### 팀 규모별

```
👤 1-2명 (개인/소규모)
→ useState, Context API
→ 빠른 개발 우선

👥 3-5명 (스타트업)
→ Zustand or MobX
→ 간단하면서도 확장 가능

👥👥 6-10명 (중소기업)
→ Redux Toolkit
→ 명확한 패턴 필요

👥👥👥 10명+ (대기업)
→ Redux Toolkit + 엄격한 규칙
→ 일관성과 유지보수성 중요
```

### 상태 종류별

```
🎨 UI 상태 (테마, 모달 등)
→ useState or Context API

📊 서버 상태 (API 데이터)
→ React Query or SWR

🔄 복잡한 비즈니스 로직
→ Redux or MobX

🌐 전역 설정
→ Context API

📱 오프라인 동기화
→ Redux + Redux Persist
```

## 마이그레이션 전략

### 점진적 도입

```javascript
// 1단계: useState로 시작
function App() {
    const [user, setUser] = useState(null);
    const [todos, setTodos] = useState([]);
}

// 2단계: Context API로 확장
const AppContext = createContext();

// 3단계: 필요한 부분만 Redux
// - 복잡한 todos만 Redux
// - user는 Context 유지

// 4단계: 점진적 마이그레이션
// - 하나씩 Redux로 이동
```

### Redux 도입 체크리스트

```
시작 전 확인:
□ 여러 컴포넌트에서 같은 상태 공유?
□ 복잡한 상태 업데이트 로직?
□ 디버깅 도구 필요?
□ 팀원 모두 Redux 학습 가능?
□ 보일러플레이트 감수 가능?

하나라도 No면 다른 대안 고려
```

## 실전 의사결정 예제

### 예제 1: 블로그 앱

```
기능:
- 글 목록 조회
- 글 작성
- 댓글 작성
- 좋아요

판단:
❌ Redux 불필요
✅ React Query로 충분

이유:
- 대부분 서버 상태
- 복잡한 로직 없음
- UI 상태 최소
```

### 예제 2: 대시보드 앱

```
기능:
- 실시간 차트
- 필터링
- 정렬
- 여러 위젯
- 사용자 설정

판단:
✅ Redux 적합

이유:
- 복잡한 클라이언트 상태
- 여러 컴포넌트 상태 공유
- 실시간 동기화 필요
```

### 예제 3: E-Commerce 앱

```
기능:
- 상품 목록
- 장바구니
- 결제
- 주문 내역

판단:
✅ Redux + React Query

이유:
- 상품 데이터: React Query
- 장바구니: Redux (복잡한 로직)
- 결제: Redux (상태 추적 필요)
```

### 한계와 트레이드오프

Redux는 **보일러플레이트가 많고**, 작은 앱에서는 오버헤드가 될 수 있습니다. **학습 곡선**이 있고, Context·Zustand 등 대안에 비해 설정이 무겁다는 비판도 있습니다. 반면 규모가 커질수록 **예측 가능한 데이터 흐름**과 **DevTools·미들웨어 생태계**가 장점이 되므로, 프로젝트 단계와 팀 상황에 맞는 **트레이드오프**를 고려해 선택하는 것이 중요합니다.

## 체크리스트 ✅

- [ ] Redux의 장단점을 이해한다
- [ ] 프로젝트에 Redux가 필요한지 판단할 수 있다
- [ ] 대안들과 비교할 수 있다
- [ ] 프로젝트 규모에 맞는 도구를 선택할 수 있다
- [ ] 점진적 마이그레이션 전략을 수립할 수 있다

## 다음 단계 🚀

축하합니다! Phase 2 (Redux 핵심 개념)를 완료했습니다!

**다음 단계**: [11. React-Redux 기초](../11-react-redux-basics/)에서 Phase 3 React-Redux를 배우거나, 필요하면 Phase 4 Redux Toolkit으로 넘어가세요!

### 추가 학습 자료
- [You Might Not Need Redux](https://medium.com/@dan_abramov/you-might-not-need-redux-be46360cf367)
- [Context API vs Redux](https://blog.isquaredsoftware.com/2021/01/context-redux-differences/)
- [Redux Style Guide](https://redux.js.org/style-guide/style-guide)

---

**핵심 요약**: Redux는 강력하지만 모든 앱에 필요하지 않습니다. 프로젝트 특성을 파악하고 적절한 도구를 선택하세요! 작게 시작하고 필요할 때 확장하는 것이 현명합니다! 💪




