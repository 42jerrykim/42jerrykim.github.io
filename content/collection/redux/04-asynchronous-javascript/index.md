---
draft: true
title: "[Redux] 04. 비동기 JavaScript - Promise와 async/await"
date: 2025-10-14
lastmod: 2025-10-14
description: "Redux 비동기 처리의 기초인 Promise와 async/await 완벽 마스터. API 호출, 데이터 페칭, 에러 처리까지 Redux에서 필수적인 비동기 프로그래밍 패턴을 실전 예제로 학습합니다."
slug: asynchronous-javascript
tags:
  - JavaScript
  - TypeScript
  - React
  - Frontend
  - 프론트엔드
  - Web
  - 웹
  - API
  - Async
  - 비동기
  - Error-Handling
  - 에러처리
  - Implementation
  - 구현
  - Concurrency
  - 동시성
  - Code-Quality
  - 코드품질
  - Best-Practices
  - Clean-Code
  - 클린코드
  - Software-Architecture
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - Functional-Programming
  - 함수형프로그래밍
  - State
  - Observer
  - Event-Driven
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
  - Pitfalls
  - 함정
  - Edge-Cases
  - 엣지케이스
  - Performance
  - 성능
  - HTTP
  - JSON
  - Caching
  - 캐싱
  - Scalability
  - 확장성
  - Latency
  - Throughput
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
  - Data-Structures
  - 자료구조
  - Maintainability
  - Modularity
  - Readability
  - Type-Safety
  - Workflow
  - 워크플로우
series: ["Redux 완전 정복"]
series_order: 4
---

Redux 앱에서는 **API 호출·데이터 페칭**처럼 비동기 작업이 필수입니다. 이 장에서는 **Promise**와 **async/await**을 정리하고, 나중에 Redux Thunk·RTK Query를 배울 때 필요한 비동기 패턴을 미리 익힙니다. 06~10장은 Redux 개념이지만, 실제로 "서버에서 데이터를 가져와 store에 넣는" 흐름을 이해하려면 이 장의 비동기 기초가 필요합니다.

## 이 글을 읽은 후 달성해야 할 목표 (평가 기준)

이 챕터를 마치면 다음을 할 수 있어야 합니다:

- **Promise**의 개념과 then/catch 사용법을 설명하고, **async/await**으로 비동기 코드를 작성할 수 있다.
- API 호출과 데이터 페칭을 구현하고, 비동기 에러를 처리할 수 있다.
- Redux Thunk·비동기 **Action** 학습에 필요한 비동기 패턴을 적용할 수 있다.

## 왜 비동기 프로그래밍이 필요한가?

Redux 앱에서는 **서버에서 데이터를 가져오거나**, **사용자 입력을 저장하는 것**처럼 **완료 시점이 늦어지는 작업**이 반드시 필요합니다. 이런 작업을 동기 코드처럼 다루면 화면이 멈추므로, Promise·async/await으로 비동기 흐름을 다루고, 나중에는 Redux Thunk나 RTK Query로 "요청 시작 → 성공/실패 액션 dispatch" 패턴을 쓰게 됩니다. 아래는 사용자 데이터를 fetch한 뒤 Redux에 넣는 흐름을 단순화한 예입니다.

```javascript
// 사용자 데이터 가져오기
dispatch({ type: 'FETCH_USER_REQUEST' });
// 서버 응답 대기 (비동기!)
const user = await fetch('/api/user').then(res => res.json());
dispatch({ type: 'FETCH_USER_SUCCESS', payload: user });

// Todo 목록 로드
// 장바구니 업데이트
// 결제 처리
// 등등... 모두 비동기!
```

**핵심**: JavaScript는 싱글 스레드이므로 비동기 처리가 필수!

## 동기 vs 비동기

Redux에서 **API 호출**·**데이터 페칭**은 모두 **비동기**입니다. **dispatch** 후 서버 응답을 기다리는 동안 화면이 멈추지 않으려면 **Promise**나 **async/await**으로 비동기 흐름을 다뤄야 하고, 나중에 배울 **Redux Thunk**·**RTK Query**도 이 개념 위에 있습니다. 먼저 동기와 비동기의 차이를 구분합니다.

### 동기 코드 (Synchronous)

```javascript
console.log("1. 시작");
console.log("2. 중간");
console.log("3. 끝");

// 출력 순서: 1 → 2 → 3 (순차적)
```

### 비동기 코드 (Asynchronous)

```javascript
console.log("1. 시작");

setTimeout(() => {
    console.log("2. 타임아웃 (3초 후)");
}, 3000);

console.log("3. 끝");

// 출력 순서: 1 → 3 → 2
// setTimeout은 비동기이므로 기다리지 않음!
```

### 왜 비동기가 필요한가?

```javascript
// ❌ 만약 동기로 처리한다면...
const data = fetchDataFromServer(); // 3초 걸림
// 3초 동안 브라우저 멈춤! (화면 업데이트 안 됨)
console.log(data);

// ✅ 비동기로 처리
fetchDataFromServer()
    .then(data => console.log(data));
// 즉시 다음 코드 실행, 화면도 정상 작동!
```

## Callback - 전통적인 비동기 처리

예전에는 비동기 결과를 **콜백 함수**로 넘겼지만, 중첩이 깊어지면 **콜백 지옥**이 됩니다. Redux에서는 **Thunk**나 **RTK Query**로 비동기를 다루며, 그 내부는 **Promise** 기반이므로 콜백보다 **then**·**async/await**을 익히는 것이 중요합니다. 아래는 콜백의 기본과 한계입니다.

### Callback 기본

```javascript
// Callback 함수
function fetchData(callback) {
    setTimeout(() => {
        const data = { id: 1, name: "Alice" };
        callback(data);
    }, 1000);
}

// 사용
fetchData((data) => {
    console.log(data); // 1초 후 출력
});
```

### Callback Hell 🔥

```javascript
// ❌ 콜백 지옥 (Callback Hell)
fetchUser(userId, (user) => {
    fetchPosts(user.id, (posts) => {
        fetchComments(posts[0].id, (comments) => {
            fetchLikes(comments[0].id, (likes) => {
                console.log(likes); // 😱 들여쓰기 깊어짐
            });
        });
    });
});

// 가독성 나쁨, 에러 처리 어려움
```

**문제점**:
- 가독성 저하
- 에러 처리 복잡
- 유지보수 어려움

## Promise - 더 나은 비동기 처리

**Redux Thunk**는 **dispatch** 안에서 **Promise**를 반환하는 비동기 함수를 실행하고, **RTK Query**의 **useQuery**·**useMutation**도 내부적으로 **Promise**를 사용합니다. **fetch** API 역시 **Promise**를 반환하므로, **then**·**catch**·**async/await**을 다룰 수 있어야 Redux 비동기 패턴을 이해할 수 있습니다.

### Promise 기본 개념

```javascript
// Promise 생성
const promise = new Promise((resolve, reject) => {
    // 비동기 작업
    setTimeout(() => {
        const success = true;
        
        if (success) {
            resolve("성공 데이터"); // 성공
        } else {
            reject("에러 메시지"); // 실패
        }
    }, 1000);
});

// Promise 사용
promise
    .then(data => console.log(data)) // 성공 시
    .catch(error => console.error(error)) // 실패 시
    .finally(() => console.log("완료")); // 항상 실행
```

### Promise States (상태)

```javascript
// Pending (대기) - 초기 상태
const pending = new Promise((resolve, reject) => {
    // 아직 resolve나 reject 안 됨
});

// Fulfilled (이행) - 성공
const fulfilled = Promise.resolve("성공");

// Rejected (거부) - 실패
const rejected = Promise.reject("실패");

// 상태 확인
promise
    .then(data => {
        console.log("상태: Fulfilled");
        console.log("데이터:", data);
    })
    .catch(error => {
        console.log("상태: Rejected");
        console.log("에러:", error);
    });
```

### Promise Chaining (체이닝)

```javascript
// ✅ Callback Hell을 Promise로 해결
fetchUser(userId)
    .then(user => fetchPosts(user.id))
    .then(posts => fetchComments(posts[0].id))
    .then(comments => fetchLikes(comments[0].id))
    .then(likes => console.log(likes))
    .catch(error => console.error(error));

// 훨씬 읽기 쉬움!

// 값 변환하며 체이닝
Promise.resolve(5)
    .then(n => n * 2)      // 10
    .then(n => n + 3)      // 13
    .then(n => n * n)      // 169
    .then(result => console.log(result)); // 169
```

### 실전 예제: fetch API

```javascript
// fetch는 Promise를 반환
fetch('https://jsonplaceholder.typicode.com/users/1')
    .then(response => {
        if (!response.ok) {
            throw new Error('HTTP error');
        }
        return response.json(); // 또 다른 Promise
    })
    .then(user => {
        console.log(user.name);
        return fetch(`/api/posts?userId=${user.id}`);
    })
    .then(response => response.json())
    .then(posts => console.log(posts))
    .catch(error => console.error('에러:', error));
```

### Promise 정적 메서드

```javascript
// Promise.all - 모든 Promise 완료 대기
const promise1 = fetch('/api/users');
const promise2 = fetch('/api/posts');
const promise3 = fetch('/api/comments');

Promise.all([promise1, promise2, promise3])
    .then(([users, posts, comments]) => {
        console.log('모두 완료!', users, posts, comments);
    })
    .catch(error => {
        console.log('하나라도 실패하면 여기로');
    });

// Promise.race - 가장 빠른 것 하나만
Promise.race([promise1, promise2, promise3])
    .then(result => console.log('가장 빠른 결과:', result));

// Promise.allSettled - 모든 결과 (성공/실패 무관)
Promise.allSettled([promise1, promise2, promise3])
    .then(results => {
        results.forEach(result => {
            if (result.status === 'fulfilled') {
                console.log('성공:', result.value);
            } else {
                console.log('실패:', result.reason);
            }
        });
    });
```

## async/await - 가장 현대적인 방법 ⭐

### 기본 문법

```javascript
// async 함수는 항상 Promise를 반환
async function fetchUser() {
    return "사용자 데이터";
}

fetchUser().then(data => console.log(data));

// await는 Promise가 완료될 때까지 대기
async function getUser() {
    const response = await fetch('/api/user');
    const user = await response.json();
    return user;
}

// 사용
getUser().then(user => console.log(user));
```

### 동기 코드처럼 작성

```javascript
// Promise 체이닝
function getUserData() {
    return fetchUser(1)
        .then(user => fetchPosts(user.id))
        .then(posts => fetchComments(posts[0].id))
        .then(comments => console.log(comments));
}

// async/await - 훨씬 읽기 쉬움! ⭐
async function getUserData() {
    const user = await fetchUser(1);
    const posts = await fetchPosts(user.id);
    const comments = await fetchComments(posts[0].id);
    console.log(comments);
}
```

### 에러 처리 (try-catch)

```javascript
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('에러 발생:', error.message);
        return null; // 기본값 반환
        
    } finally {
        console.log('완료'); // 성공/실패 관계없이 실행
    }
}

// 사용
const data = await fetchData();
```

### 병렬 처리

```javascript
// ❌ 순차 처리 (느림)
async function sequential() {
    const user = await fetchUser(); // 1초
    const posts = await fetchPosts(); // 1초
    const comments = await fetchComments(); // 1초
    // 총 3초!
}

// ✅ 병렬 처리 (빠름)
async function parallel() {
    const [user, posts, comments] = await Promise.all([
        fetchUser(),    // 동시 실행
        fetchPosts(),   // 동시 실행
        fetchComments() // 동시 실행
    ]);
    // 총 1초!
}

// 조건부 병렬 처리
async function conditionalParallel() {
    const user = await fetchUser();
    
    // user 정보가 필요한 요청은 순차
    const posts = await fetchPosts(user.id);
    
    // 독립적인 요청은 병렬
    const [likes, shares] = await Promise.all([
        fetchLikes(posts[0].id),
        fetchShares(posts[0].id)
    ]);
}
```

## Redux에서 비동기 처리 미리보기

### 기본 패턴

```javascript
// Action Types
const FETCH_TODOS_REQUEST = 'FETCH_TODOS_REQUEST';
const FETCH_TODOS_SUCCESS = 'FETCH_TODOS_SUCCESS';
const FETCH_TODOS_FAILURE = 'FETCH_TODOS_FAILURE';

// Async Action Creator (Thunk)
const fetchTodos = () => async (dispatch) => {
    // 요청 시작
    dispatch({ type: FETCH_TODOS_REQUEST });
    
    try {
        const response = await fetch('/api/todos');
        const todos = await response.json();
        
        // 성공
        dispatch({ 
            type: FETCH_TODOS_SUCCESS, 
            payload: todos 
        });
        
    } catch (error) {
        // 실패
        dispatch({ 
            type: FETCH_TODOS_FAILURE, 
            payload: error.message 
        });
    }
};

// Reducer
const todoReducer = (state = initialState, action) => {
    switch(action.type) {
        case FETCH_TODOS_REQUEST:
            return { ...state, loading: true, error: null };
        
        case FETCH_TODOS_SUCCESS:
            return { ...state, loading: false, todos: action.payload };
        
        case FETCH_TODOS_FAILURE:
            return { ...state, loading: false, error: action.payload };
        
        default:
            return state;
    }
};
```

### Redux Toolkit 미리보기

```javascript
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

// Async Thunk (자동으로 pending/fulfilled/rejected 생성)
const fetchTodos = createAsyncThunk(
    'todos/fetch',
    async () => {
        const response = await fetch('/api/todos');
        return response.json();
    }
);

// Slice
const todoSlice = createSlice({
    name: 'todos',
    initialState: { todos: [], loading: false, error: null },
    extraReducers: (builder) => {
        builder
            .addCase(fetchTodos.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchTodos.fulfilled, (state, action) => {
                state.loading = false;
                state.todos = action.payload;
            })
            .addCase(fetchTodos.rejected, (state, action) => {
                state.loading = false;
                state.error = action.error.message;
            });
    }
});
```

## 실습 문제 🏋️‍♂️

### 문제 1: Promise 기본
```javascript
// TODO: 1초 후 랜덤 숫자(1-10)를 반환하는 Promise 작성
// 5보다 크면 resolve, 작으면 reject

// 답안:
const randomPromise = new Promise((resolve, reject) => {
    setTimeout(() => {
        const num = Math.floor(Math.random() * 10) + 1;
        if (num > 5) {
            resolve(num);
        } else {
            reject(`${num}은 너무 작습니다`);
        }
    }, 1000);
});

randomPromise
    .then(num => console.log('성공:', num))
    .catch(error => console.error('실패:', error));
```

### 문제 2: async/await로 변환
```javascript
// 다음 Promise 체인을 async/await로 변환

function fetchUserPosts(userId) {
    return fetch(`/api/users/${userId}`)
        .then(res => res.json())
        .then(user => fetch(`/api/posts?userId=${user.id}`))
        .then(res => res.json())
        .then(posts => posts);
}

// 답안:
async function fetchUserPosts(userId) {
    const userRes = await fetch(`/api/users/${userId}`);
    const user = await userRes.json();
    
    const postsRes = await fetch(`/api/posts?userId=${user.id}`);
    const posts = await postsRes.json();
    
    return posts;
}

// 또는 더 간결하게:
async function fetchUserPosts(userId) {
    const user = await fetch(`/api/users/${userId}`).then(r => r.json());
    const posts = await fetch(`/api/posts?userId=${user.id}`).then(r => r.json());
    return posts;
}
```

### 문제 3: 에러 처리
```javascript
// TODO: 다음 요구사항을 만족하는 함수 작성
// 1. URL에서 데이터 fetch
// 2. HTTP 에러 처리
// 3. 네트워크 에러 처리
// 4. 타임아웃 처리 (5초)

// 답안:
async function fetchWithTimeout(url, timeout = 5000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
        const response = await fetch(url, {
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
        
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('요청 시간 초과');
        }
        throw error;
    }
}

// 사용
try {
    const data = await fetchWithTimeout('/api/data', 5000);
    console.log(data);
} catch (error) {
    console.error('에러:', error.message);
}
```

### 문제 4: Promise.all 활용
```javascript
// TODO: 여러 사용자의 정보를 동시에 가져오기
const userIds = [1, 2, 3, 4, 5];

// 답안:
async function fetchMultipleUsers(userIds) {
    try {
        const promises = userIds.map(id => 
            fetch(`/api/users/${id}`).then(res => res.json())
        );
        
        const users = await Promise.all(promises);
        return users;
        
    } catch (error) {
        console.error('일부 사용자 fetch 실패:', error);
        
        // 또는 allSettled로 개별 처리
        const results = await Promise.allSettled(promises);
        return results
            .filter(r => r.status === 'fulfilled')
            .map(r => r.value);
    }
}

const users = await fetchMultipleUsers(userIds);
```

## 실전 패턴

### 재시도 로직
```javascript
async function fetchWithRetry(url, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            const response = await fetch(url);
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        }
    }
}
```

### 캐싱
```javascript
const cache = new Map();

async function fetchWithCache(url) {
    if (cache.has(url)) {
        console.log('캐시에서 반환');
        return cache.get(url);
    }
    
    const data = await fetch(url).then(r => r.json());
    cache.set(url, data);
    return data;
}
```

## 체크리스트 ✅

- [ ] Promise의 3가지 상태를 이해한다
- [ ] Promise 체이닝을 사용할 수 있다
- [ ] async/await로 깔끔한 코드를 작성할 수 있다
- [ ] try-catch로 에러를 처리할 수 있다
- [ ] Promise.all로 병렬 처리를 할 수 있다
- [ ] fetch API로 HTTP 요청을 보낼 수 있다
- [ ] 실습 문제를 모두 해결했다

## 다음 단계 🚀

**다음 챕터**: `05. TypeScript 기초 - 타입 시스템 이해하기`에서는 Redux를 더 안전하게 사용하기 위한 TypeScript 기초를 배웁니다.

### 추가 학습 자료
- [MDN - Promise](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [MDN - async/await](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Statements/async_function)
- [JavaScript.info - Promises](https://ko.javascript.info/promise-basics)

---

**핵심 요약**: async/await는 비동기 코드를 동기 코드처럼 읽기 쉽게 만듭니다. Redux에서 API 호출 시 필수적이니 확실히 익히세요! 💪

