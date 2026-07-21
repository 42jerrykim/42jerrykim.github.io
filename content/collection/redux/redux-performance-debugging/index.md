---
title: "[Redux] 29. Redux 성능 최적화와 디버깅 심화"
description: "13편의 컴포넌트 최적화를 넘어, Redux DevTools의 액션 필터·상태 diff·시간 여행 디버깅을 실전 워크플로로 정리합니다. 대규모 상태에서 리듀서 자체가 병목이 되는 경우와 그 진단법, 프로덕션 디버깅 전략까지 다룹니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 29
draft: false
slug: redux-performance-debugging
image: "wordcloud.png"
tags:
  - Redux
  - Performance(성능)
  - Debugging(디버깅)
  - Optimization(최적화)
  - JavaScript
  - React
  - Frontend(프론트엔드)
  - Web(웹)
  - Best-Practices
  - Tutorial(튜토리얼)
  - Education(교육)
  - Code-Quality(코드품질)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Advanced
  - Deep-Dive
  - devtools심화
  - 액션필터
  - 상태diff확인
  - 시간여행디버깅
  - 리듀서병목진단
  - 프로덕션디버깅전략
  - Profiling(프로파일링)
  - Logging(로깅)
---

# 29. Redux 성능 최적화와 디버깅 심화

13편에서 컴포넌트 리렌더 최적화를 다뤘습니다. 이 편은 한 단계 더 나아가, **Redux DevTools를 실전 디버깅 도구로 활용하는 법**과 **리듀서 자체가 병목이 되는 드문 경우**를 다룹니다.

## 학습 목표

- Redux DevTools의 액션 필터, 상태 diff, 시간 여행 기능으로 버그를 재현하고 원인을 좁힐 수 있다.
- 리듀서 안의 무거운 계산이 병목이 되는 경우를 식별하고 대응할 수 있다.
- 프로덕션 환경에서 안전하게 디버깅 정보를 수집하는 전략을 설명할 수 있다.

## Redux DevTools 심화: 액션 필터

09편에서 DevTools의 시간 여행 디버깅을 간단히 언급했습니다. 실전에서는 액션이 수백 개씩 쌓이기 때문에, **필터로 원하는 액션만 좁혀보는 것**이 첫 단계입니다.

```javascript
// configureStore(18편)에서 DevTools 옵션을 세밀하게 조정할 수 있다
export const store = configureStore({
  reducer: rootReducer,
  devTools: process.env.NODE_ENV !== "production" && {
    actionsBlacklist: ["persist/REHYDRATE"], // 노이즈가 되는 액션은 제외
    trace: true, // 각 액션이 어느 코드에서 dispatch됐는지 스택 트레이스를 기록
  },
});
```

DevTools UI의 필터 입력창에 `todos/`를 입력하면 `todos` slice와 관련된 액션만 표시됩니다. 특정 기능에서 발생하는 문제를 조사할 때, 관련 없는 액션(폼 입력 변경 등)의 노이즈를 걷어내는 것만으로 원인 파악이 훨씬 빨라집니다.

## 상태 diff로 "무엇이 바뀌었는가" 정확히 보기

DevTools의 **Diff** 탭은 액션 하나가 실행되기 전/후 상태를 비교해 **정확히 어떤 필드가 바뀌었는지**를 보여줍니다. 08편에서 강조한 불변성 규칙 위반(리듀서 밖에서 상태가 직접 변경되는 버그)을 찾을 때 특히 유용합니다.

```
// 예상: todoToggled 액션 후 todos.1.done만 true → false로 바뀌어야 함
// Diff 탭에서 확인했더니 todos.1.done 외에 todos.0.priority까지 바뀌어 있다면
// → 리듀서 로직에 의도치 않은 부수 효과가 있다는 강한 신호
```

이 방식은 "왜 이 컴포넌트가 예상치 못하게 리렌더되는가"(13편의 주제)를 조사할 때도 응용됩니다. 리렌더가 발생한 시점의 액션을 DevTools에서 찾아 Diff를 확인하면, "실제로 그 컴포넌트가 구독하는 상태 조각이 바뀌었는지" 눈으로 검증할 수 있습니다.

## 시간 여행 디버깅으로 버그 재현하기

DevTools는 과거의 특정 액션 시점으로 상태를 되돌릴 수 있습니다(**Jump** 기능). 버그 재현이 어려운 상황(예: "특정 순서로 여러 액션을 dispatch했을 때만 발생하는 버그")에서 유용합니다.

1. 버그가 발생하기 직전까지의 액션 목록을 DevTools에서 확인한다.
2. 의심되는 액션 하나를 **Skip**(건너뛰기)해서, 그 액션이 없었다면 버그가 재현되지 않는지 확인한다.
3. 이 방식으로 "어떤 액션의 조합이 버그를 유발하는가"를 이진 탐색하듯 좁혀나간다.

이 워크플로는 09편에서 배운 "액션 로그가 곧 상태 변화의 완전한 기록"이라는 Redux의 핵심 특성 덕분에 가능합니다. 상태가 액션의 순차 적용 결과이므로, 액션 목록만 있으면 어떤 시점의 상태든 재현할 수 있습니다.

## 리듀서 자체가 병목이 되는 경우

13편은 주로 **불필요한 리렌더**(컴포넌트 층위)를 다뤘습니다. 드물지만, **리듀서 함수 자체의 계산이 무거워서** 매 dispatch마다 지연이 발생하는 경우도 있습니다.

```javascript
// 병목 사례: 매 액션마다 대규모 배열을 정렬
function productsReducer(state, action) {
  switch (action.type) {
    case "products/filterChanged":
      return {
        ...state,
        filtered: state.all
          .filter((p) => p.category === action.payload)
          .sort((a, b) => b.rating - a.rating), // 필터링될 때마다 전체 재정렬 — 배열이 크면 비용이 크다
      };
  }
}
```

이런 경우, DevTools의 각 액션 항목에 표시되는 <strong>처리 시간(ms)</strong>을 확인해 실제로 리듀서가 병목인지부터 확인합니다(추측으로 최적화를 시작하지 않는다는 13편의 원칙이 여기서도 동일하게 적용됩니다). 병목이 확인되면 다음을 고려합니다.

- **정렬을 selector로 옮기고 14편의 `createSelector`로 메모이제이션**한다 — 리듀서가 아니라 selector 층위에서, 실제로 필요한 시점(렌더링 시)에만 계산되게 한다.
- **27편의 정규화**로 데이터 구조 자체를 O(1) 조회가 가능한 형태로 바꾼다.
- 정말 무거운 계산(대규모 데이터 처리)이라면 Web Worker로 메인 스레드 밖에서 처리하는 것도 방법이다.

```javascript
// 개선: 정렬을 리듀서에서 제거하고, 필요한 시점에만 계산되는 selector로 이동
function productsReducer(state, action) {
  switch (action.type) {
    case "products/filterChanged":
      return { ...state, activeCategory: action.payload }; // 리듀서는 단순히 필터 조건만 저장
  }
}

export const selectFilteredProducts = createSelector(
  [(state) => state.products.all, (state) => state.products.activeCategory],
  (allProducts, category) =>
    allProducts.filter((p) => p.category === category).sort((a, b) => b.rating - a.rating)
); // 입력이 바뀔 때만 재계산됨(14편)
```

## 프로덕션 환경 디버깅 전략

18편에서 `configureStore`의 개발용 검사 미들웨어가 프로덕션에서 자동으로 꺼진다고 했습니다. 마찬가지로 **DevTools 자체도 프로덕션에서는 비활성화**하는 것이 원칙입니다(사용자가 앱의 전체 상태와 액션 히스토리를 열어볼 수 있게 되는 것은 정보 노출 위험이 있습니다).

```javascript
export const store = configureStore({
  reducer: rootReducer,
  devTools: process.env.NODE_ENV !== "production", // 프로덕션에서는 자동으로 false
});
```

프로덕션에서 발생한 버그를 조사해야 한다면, DevTools 대신 **에러 리포팅 도구(Sentry 등)와 미들웨어를 결합**하는 방식을 씁니다.

```javascript
// 프로덕션 에러 발생 시 최근 액션 히스토리를 함께 리포팅하는 미들웨어
const errorReportingMiddleware = (store) => (next) => (action) => {
  try {
    return next(action);
  } catch (error) {
    reportError(error, {
      lastAction: action,
      stateSnapshot: store.getState(), // 에러 발생 시점의 상태를 함께 전송
    });
    throw error;
  }
};
```

21편에서 배운 미들웨어 구조가 여기서도 그대로 활용됩니다. try/catch로 감싼 `next(action)` 호출은, 리듀서 실행 중 예외가 발생했을 때 그 순간의 액션과 상태를 함께 기록해 사후 분석을 가능하게 합니다.

## 실무 체크리스트

- 버그를 조사할 때 DevTools의 액션 필터로 관련 없는 노이즈를 걷어내고 있는가?
- 예상치 못한 리렌더나 상태 변화를 조사할 때 Diff 탭으로 "정확히 무엇이 바뀌었는지" 먼저 확인하는가?
- 리듀서 최적화를 시작하기 전에 DevTools의 액션별 처리 시간으로 실제 병목을 확인했는가?
- 프로덕션 빌드에서 DevTools가 비활성화되어 있는가?

## 연습 과제

### 기초(★☆☆)
- DevTools의 액션 필터에 특정 slice 이름을 입력해, 관련 액션만 걸러 보는 것을 연습해보세요.

### 중급(★★☆)
- 의도적으로 무거운 정렬 로직을 리듀서 안에 넣고 DevTools에서 처리 시간을 측정한 뒤, selector로 옮겨 처리 시간이 어떻게 달라지는지 비교해보세요.

### 고급(★★★)
- `errorReportingMiddleware`를 작성하고, 의도적으로 예외를 던지는 리듀서를 만들어 에러 발생 시 마지막 액션과 상태 스냅샷이 정확히 캡처되는지 확인해보세요.

## 요약

- Redux DevTools의 액션 필터·Diff·시간 여행 기능은 "어떤 액션이, 무엇을, 언제 바꿨는가"를 정확히 좁혀가는 도구다.
- 리듀서 자체가 병목이 되는 드문 경우, 무거운 계산을 리듀서에서 selector(14편)나 정규화된 구조(27편)로 옮겨 해결한다.
- 프로덕션에서는 DevTools를 끄고, 필요하다면 미들웨어로 에러 발생 시점의 액션·상태를 별도로 리포팅한다.

## 참고 문헌 및 출처(추천)

- Redux DevTools Extension 공식 문서(GitHub), "Features"
- Redux 공식 문서, "Debugging"
- Redux Toolkit 공식 문서, "configureStore, devTools 옵션"

---

## 다음 글

- 다음: [30. 테스팅과 실전 프로젝트 - E-Commerce 앱 (시리즈 마무리)](../testing-ecommerce-app/)
