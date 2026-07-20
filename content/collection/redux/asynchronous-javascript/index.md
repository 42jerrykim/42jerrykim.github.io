---
title: "[Redux] 04. 비동기 JavaScript - Promise와 async/await"
description: "Redux의 Reducer는 반드시 동기·순수해야 하지만, 실제 앱은 API 호출 같은 비동기 작업 없이 동작할 수 없습니다. Promise와 async/await의 동작 원리를 21~24편의 미들웨어를 이해하는 데 필요한 만큼 정리합니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 4
draft: false
slug: asynchronous-javascript
image: "wordcloud.png"
tags:
  - JavaScript
  - Async(비동기)
  - Frontend(프론트엔드)
  - Web(웹)
  - Beginner
  - Tutorial(튜토리얼)
  - Education(교육)
  - Best-Practices
  - Code-Quality(코드품질)
  - Error-Handling(에러처리)
  - API(Application Programming Interface)
  - HTTP(HyperText Transfer Protocol)
  - How-To
  - Guide(가이드)
  - Documentation(문서화)
  - Reference(참고)
  - Debugging(디버깅)
  - Edge-Cases(엣지케이스)
  - Promise객체
  - 이벤트루프
  - 마이크로태스크
  - asyncawait
  - 콜백지옥
  - 비동기액션
  - 경쟁상태
---

# 04. 비동기 JavaScript - Promise와 async/await

Redux의 리듀서는 "같은 입력에 항상 같은 출력을 내는 순수 함수"여야 하고, 비동기 작업(예측 불가능한 타이밍에 완료됨)을 포함할 수 없습니다. 그런데도 실제 앱은 API 호출 없이 동작할 수 없습니다. 이 모순을 어떻게 푸는지가 21~24편(미들웨어, Thunk, Saga, RTK Query)의 핵심 주제이며, 이 편은 그 전에 필요한 비동기 JavaScript 기초를 다집니다.

## 학습 목표

- Promise의 세 가지 상태(대기·이행·거부)와 `.then()`/`.catch()` 체이닝을 설명할 수 있다.
- `async`/`await`로 Promise 기반 코드를 동기 코드처럼 읽기 쉽게 작성할 수 있다.
- 비동기 작업에서 에러를 놓치지 않고 처리하는 방법을 적용할 수 있다.

## Promise: 미래에 완료될 작업을 표현하는 객체

**Promise**는 아직 완료되지 않았지만 언젠가 완료될(또는 실패할) 작업을 나타내는 객체입니다. 세 가지 상태를 가집니다.

- **pending(대기)**: 아직 결과가 나오지 않은 상태
- **fulfilled(이행)**: 작업이 성공적으로 끝난 상태
- **rejected(거부)**: 작업이 실패한 상태

```javascript
function fetchUser(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (id > 0) {
        resolve({ id, name: "Kim" }); // 성공: fulfilled로 전환
      } else {
        reject(new Error("Invalid id")); // 실패: rejected로 전환
      }
    }, 100);
  });
}

fetchUser(1)
  .then((user) => console.log(user)) // { id: 1, name: "Kim" }
  .catch((error) => console.error(error.message));
```

`.then()`은 이행된 값을 받아 처리하고, `.catch()`는 거부된 이유(에러)를 처리합니다. 실무에서는 대부분 `fetch()`나 axios 같은 라이브러리가 이미 Promise를 반환하므로, `new Promise(...)`를 직접 쓰는 경우는 드뭅니다.

```javascript
fetch("/api/users/1")
  .then((response) => response.json())
  .then((user) => console.log(user))
  .catch((error) => console.error("요청 실패:", error));
```

## async/await: Promise를 동기 코드처럼 읽는다

`.then()` 체이닝이 길어지면 코드를 순서대로 읽기 어려워집니다(흔히 "콜백 지옥"의 Promise 버전). `async`/`await`는 같은 동작을 동기 코드처럼 보이게 해줍니다.

```javascript
async function loadUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const user = await response.json();
    return user;
  } catch (error) {
    console.error("사용자 로드 실패:", error.message);
    throw error; // 호출한 쪽에서도 실패를 알 수 있도록 다시 던짐
  }
}
```

`async` 함수는 **항상 Promise를 반환**합니다. `await`는 Promise가 이행되거나 거부될 때까지 그 함수의 실행을 일시 정지시키지만, **다른 코드(이벤트 루프)는 계속 실행**됩니다. 즉 `await`가 전체 프로그램을 멈추는 것이 아니라, 해당 `async` 함수 내부의 다음 줄만 미룹니다.

## 이벤트 루프와 마이크로태스크: await가 다른 코드를 막지 않는 원리

방금 본 동작의 근거는 JavaScript의 **이벤트 루프**가 작업을 두 종류의 큐로 나눠 처리하기 때문입니다. `setTimeout`, DOM 이벤트, I/O 콜백은 **매크로태스크(macrotask)** 큐에, Promise의 `.then`/`.catch`와 `await` 재개 지점은 **마이크로태스크(microtask)** 큐에 들어갑니다. 이벤트 루프는 **콜스택이 완전히 비워질 때마다 마이크로태스크 큐를 모두 비운 뒤에야** 매크로태스크 큐에서 다음 작업 하나를 꺼냅니다.

```javascript
console.log("1: 동기 코드");
setTimeout(() => console.log("2: setTimeout (매크로태스크)"), 0);
Promise.resolve().then(() => console.log("3: Promise.then (마이크로태스크)"));
console.log("4: 동기 코드 끝");

// 실제 출력 순서: 1, 4, 3, 2
```

`setTimeout(..., 0)`이 "즉시" 실행될 것 같지만, 콜스택이 비워진 뒤 이벤트 루프는 마이크로태스크 큐(3번)를 먼저 전부 처리하고, 그다음에야 매크로태스크 큐(2번)로 넘어갑니다. `await`로 일시 정지된 `async` 함수의 나머지 부분도 마이크로태스크로 큐에 들어가므로, 동기 코드(`console.log("4: ...")`)가 항상 그보다 먼저 실행됩니다.

## 에러 처리: try/catch를 놓치지 않는다

`async`/`await`에서 에러 처리를 빠뜨리는 것은 흔한 실수입니다. `try`/`catch`가 없으면 실패한 Promise는 <strong>처리되지 않은 거부(unhandled rejection)</strong>가 되어, 실무에서는 이 에러가 조용히 사라지거나 콘솔에만 남고 사용자에게 아무 피드백도 가지 않는 경우가 많습니다.

```javascript
// 나쁜 예: try/catch 없이 await만 사용
async function loadUserBad(id) {
  const response = await fetch(`/api/users/${id}`); // 네트워크 실패 시 예외가 그대로 전파됨
  return response.json();
}

// 개선: 실패를 명시적으로 처리
async function loadUserGood(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`사용자를 불러오지 못했습니다 (HTTP ${response.status})`);
    }
    return await response.json();
  } catch (error) {
    // 여기서 로깅, 재시도, 사용자 알림 등 실제 처리를 한다
    console.error(error.message);
    return null;
  }
}
```

## 여러 비동기 작업을 동시에 실행하기

`await`를 순차적으로 나열하면 각 작업이 끝나야 다음이 시작되어 불필요하게 느려집니다. 서로 의존하지 않는 작업은 `Promise.all()`로 동시에 실행합니다.

```javascript
// 느림: user를 기다린 뒤에야 orders 요청이 시작됨
async function loadSequential(userId) {
  const user = await fetchUser(userId);
  const orders = await fetchOrders(userId);
  return { user, orders };
}

// 빠름: 두 요청이 동시에 시작되고, 둘 다 끝나면 결과를 받는다
async function loadParallel(userId) {
  const [user, orders] = await Promise.all([fetchUser(userId), fetchOrders(userId)]);
  return { user, orders };
}
```

`Promise.all()`은 배열의 Promise 중 **하나라도 거부되면 즉시 전체가 거부**됩니다. 일부가 실패해도 나머지 결과를 살리고 싶다면 `Promise.allSettled()`를 사용합니다.

## 경쟁 상태: 오래된 응답이 최신 응답을 덮어쓰는 문제

여러 비동기 요청을 연달아 보낼 때, **네트워크 지연 순서가 요청을 보낸 순서와 다를 수 있다**는 점을 놓치면 **경쟁 상태(race condition)** 버그가 생깁니다. 검색창에 빠르게 타이핑하는 상황을 생각해봅시다.

```javascript
// 문제: 응답이 도착한 순서가 요청을 보낸 순서와 다를 수 있다
async function search(query) {
  const response = await fetch(`/api/search?q=${query}`);
  const results = await response.json();
  renderResults(results); // 이 응답이 여전히 "최신" 요청의 응답인지 확인하지 않는다
}

search("리");    // 서버 부하로 3초 후 응답
search("리액트"); // 짧은 검색어라 1초 후 응답이 먼저 도착
```

`"리액트"`의 응답이 1초 만에 먼저 화면을 그리고, 2초 뒤 `"리"`의 낡은 응답이 도착해 그 화면을 덮어써 버립니다. 사용자는 `"리액트"`를 입력했는데 `"리"`에 대한 검색 결과를 보게 되는 버그입니다.

```javascript
// 개선: 응답을 반영하기 직전에, 그 요청이 여전히 최신 요청인지 확인한다
let latestQuery = "";

async function search(query) {
  latestQuery = query; // 요청을 보낼 때 "지금 최신 요청"을 기록
  const response = await fetch(`/api/search?q=${query}`);
  const results = await response.json();
  if (query === latestQuery) { // 응답이 도착한 시점에도 여전히 최신 요청인지 재확인
    renderResults(results);
  } // 아니라면 이미 낡은 응답이므로 조용히 버린다
}
```

`latestQuery`를 매번 손으로 비교하는 이 방식은 동작하지만 번거롭고 빠뜨리기 쉽습니다. 23편의 `takeLatest`와 24편의 RTK Query는 바로 이 패턴을 라이브러리 차원에서 자동으로 처리해, 개발자가 이 비교 로직을 직접 작성하지 않아도 되게 해줍니다.

## 왜 리듀서에는 비동기 코드를 넣을 수 없는가

Redux의 리듀서는 `(state, action) => newState` 형태의 **순수 함수**여야 합니다. 비동기 작업(예: `await fetch(...)`)을 리듀서 안에 넣으면, 같은 액션이 들어와도 네트워크 상태에 따라 다른 결과가 나올 수 있어 순수성이 깨지고, Redux DevTools의 시간여행 디버깅(상태를 재생하는 기능)도 무의미해집니다.

```javascript
// 절대 이렇게 쓰지 않는다: 리듀서 안에서 비동기 호출
function userReducer(state, action) {
  if (action.type === "user/load") {
    fetch(`/api/users/${action.payload}`).then((res) => res.json()); // 리듀서가 값을 즉시 반환하지 못함
    return state;
  }
  return state;
}
```

그래서 Redux는 비동기 로직을 리듀서 **바깥**(미들웨어)에서 처리하고, 리듀서에는 "요청 시작", "성공", "실패"라는 세 개의 **동기 액션**만 전달하는 패턴을 씁니다. 이 패턴은 21~22편(미들웨어, Thunk)에서 구체적으로 구현합니다.

```javascript
// 비동기 작업의 각 단계를 동기 액션으로 표현 (21~22편에서 실제로 dispatch하는 방법을 다룸)
const userLoadStarted = () => ({ type: "user/loadStarted" });
const userLoadSucceeded = (user) => ({ type: "user/loadSucceeded", payload: user });
const userLoadFailed = (error) => ({ type: "user/loadFailed", payload: error.message });
```

## 실무 체크리스트

- `async` 함수 내부의 `await` 호출을 `try`/`catch`로 감싸 에러를 명시적으로 처리했는가?
- 서로 의존하지 않는 비동기 작업을 불필요하게 순차 실행(`await` 나열)하고 있지 않은가?
- 연속으로 같은 요청을 다시 보낼 수 있는 상황(검색어 입력 등)에서, 응답이 도착한 순서가 요청을 보낸 순서와 다를 수 있음을 고려했는가?
- 리듀서 안에 비동기 코드나 네트워크 호출이 섞여 있지 않은가?

## 연습 과제

### 기초(★☆☆)
- `fetchUser`를 `.then()` 체이닝 버전과 `async`/`await` 버전 두 가지로 작성하고 가독성을 비교해보세요.

### 중급(★★☆)
- 실패할 수 있는 비동기 함수를 작성하고, `try`/`catch`로 실패 시 기본값을 반환하도록 만들어보세요.

### 고급(★★★)
- 서로 독립적인 API 호출 3개를 `Promise.all()`로 동시에 실행하는 코드와, 순차적으로 실행하는 코드를 각각 작성해 실행 시간을 비교해보세요.
- `console.log`, `setTimeout(..., 0)`, `Promise.resolve().then()`을 섞어 순서를 예측한 뒤 실제로 실행해 마이크로태스크가 매크로태스크보다 먼저 실행되는지 확인해보세요. 이어서 `search` 함수의 경쟁 상태 버그를 의도적으로 재현(느린 응답을 `setTimeout`으로 지연)한 뒤, `latestQuery` 비교로 고쳐보세요.

## 요약

- Promise는 미래에 완료될 작업을 나타내며, `async`/`await`는 이를 동기 코드처럼 읽기 쉽게 만든다.
- 이벤트 루프는 마이크로태스크(Promise, await)를 매크로태스크(setTimeout)보다 항상 먼저 모두 처리한다.
- 응답 도착 순서가 요청 순서와 다를 수 있으므로, 최신 요청인지 확인하지 않으면 경쟁 상태(오래된 응답이 최신 결과를 덮어씀) 버그가 생긴다.
- 리듀서는 반드시 순수·동기여야 하므로, 비동기 로직은 리듀서 바깥(미들웨어)에서 처리하고 리듀서에는 동기 액션만 전달한다.

## 참고 문헌 및 출처(추천)

- MDN Web Docs, "Using promises" — Promise 체이닝과 에러 처리 공식 가이드
- MDN Web Docs, "async function" — async/await의 정확한 동작 규칙
- MDN Web Docs, "The event loop" — 매크로태스크/마이크로태스크 큐와 실행 순서 규칙
- Redux 공식 문서, "Writing Logic with Thunks" — 리듀서가 비동기를 다룰 수 없는 이유와 대안

---

## 다음 글

- 다음: [05. TypeScript 기초 - 타입 시스템 이해하기](../typescript-basics/)
