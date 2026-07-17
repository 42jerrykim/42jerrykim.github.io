---
title: "[Redux] 30. 테스팅과 실전 프로젝트 - E-Commerce 앱 (시리즈 마무리)"
description: "리듀서·thunk·컴포넌트 테스트 작성법을 정리하고, 1~29편의 개념을 모두 조합한 장바구니·상품 목록·주문 E-Commerce 미니 프로젝트로 시리즈를 마무리합니다. 전체 30편 대응표를 포함합니다."
date: 2026-07-17
lastmod: 2026-07-17
collection_order: 30
draft: false
slug: testing-ecommerce-app
tags:
  - Redux
  - Testing(테스트)
  - Redux-Toolkit
  - React
  - JavaScript
  - TypeScript
  - Frontend(프론트엔드)
  - Web(웹)
  - Case-Study
  - Best-Practices
  - Code-Quality(코드품질)
  - Tutorial(튜토리얼)
  - Education(교육)
  - Documentation(문서화)
  - Reference(참고)
  - Guide(가이드)
  - Advanced
  - Deep-Dive
  - 리듀서단위테스트
  - thunk테스트
  - RTL컴포넌트테스트
  - 이커머스실전프로젝트
  - 시리즈마무리
  - TDD(Test-Driven Development)
  - Error-Handling(에러처리)
---

# 30. 테스팅과 실전 프로젝트 - E-Commerce 앱

Redux 시리즈의 마지막 편입니다. 테스트 작성법을 정리하고, 1~29편의 개념을 모두 동원해 상품 목록·장바구니·주문이라는 세 기능을 가진 E-Commerce 미니 프로젝트를 완성합니다.

## 학습 목표

- 리듀서, thunk, RTK Query 엔드포인트, 컴포넌트 각각에 맞는 테스트 전략을 구사할 수 있다.
- 여러 slice와 RTK Query API가 얽힌 실전 규모의 프로젝트를 처음부터 조립할 수 있다.
- 1~30편의 어느 개념이 실전 프로젝트의 어느 부분에 대응하는지 스스로 설명할 수 있다.

## 리듀서 테스트: 순수 함수의 이점

07·08편에서 리듀서가 "입력이 같으면 출력이 같은 순수 함수"라고 배웠습니다. 이 특성 덕분에 리듀서 테스트는 **mock이 전혀 필요 없습니다.**

```javascript
// cartSlice.test.js
import cartReducer, { itemAdded, itemRemoved } from "./cartSlice";

test("itemAdded는 새 상품을 장바구니에 추가한다", () => {
  const initialState = { items: [] };
  const action = itemAdded({ id: "p1", price: 10000, quantity: 1 });

  const newState = cartReducer(initialState, action);

  expect(newState.items).toHaveLength(1);
  expect(newState.items[0]).toEqual({ id: "p1", price: 10000, quantity: 1 });
  expect(initialState.items).toHaveLength(0); // 08편: 원본 state는 절대 변경되지 않아야 한다
});
```

`initialState.items`가 여전히 빈 배열인지 확인하는 마지막 줄이 중요합니다. 08편에서 배운 불변성 원칙이 실제로 지켜지고 있는지를 테스트가 직접 검증합니다.

## Thunk 테스트: 가짜 dispatch/getState 주입

22편의 thunk는 `(dispatch, getState)`를 받는 함수이므로, 실제 Store 없이도 **가짜 함수를 직접 주입**해 테스트할 수 있습니다.

```javascript
// checkoutThunk.test.js
import { checkoutCart } from "./cartSlice";

test("장바구니가 비어있으면 checkoutRejected를 dispatch한다", async () => {
  const dispatch = jest.fn(); // 실제 Store 없이 함수 호출만 기록하는 가짜 dispatch
  const getState = () => ({ cart: { items: [] } });

  await checkoutCart()(dispatch, getState); // thunk 함수를 직접 호출

  expect(dispatch).toHaveBeenCalledWith({
    type: "cart/checkoutRejected",
    payload: "장바구니가 비어 있습니다",
  });
});
```

## RTK Query 테스트: MSW로 네트워크 계층 모킹

24편의 RTK Query 엔드포인트는 실제 fetch를 수행하므로, **MSW(Mock Service Worker)**로 네트워크 계층에서 가짜 응답을 준비하는 것이 표준적인 방법입니다.

```javascript
// productsApi.test.js
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";
import { productsApi } from "./productsApi";
import { setupApiStore } from "../../test-utils/setupApiStore"; // configureStore로 테스트 전용 store를 만드는 헬퍼

const server = setupServer(
  http.get("/api/products", () => HttpResponse.json([{ id: "p1", name: "키보드", price: 50000 }]))
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test("getProducts는 상품 목록을 가져와 캐시한다", async () => {
  const storeRef = setupApiStore(productsApi);
  const result = await storeRef.store.dispatch(productsApi.endpoints.getProducts.initiate());

  expect(result.data).toEqual([{ id: "p1", name: "키보드", price: 50000 }]);
});
```

MSW는 실제 네트워크 계층(fetch)을 가로채므로, `fetchBaseQuery` 내부 구현을 몰라도 됩니다. "이 URL로 요청이 오면 이 응답을 준다"는 선언만으로 24편에서 만든 API 슬라이스 전체를 검증할 수 있습니다.

## 컴포넌트 테스트: React Testing Library

12편의 `useSelector`/`useDispatch`를 쓰는 컴포넌트는 실제 Store로 감싸서 테스트합니다. 컴포넌트의 내부 구현이 아니라, **사용자가 보는 화면과 상호작용**을 기준으로 검증합니다.

```jsx
// Cart.test.jsx
import { render, screen, fireEvent } from "@testing-library/react";
import { Provider } from "react-redux"; // 11편의 Provider
import { configureStore } from "@reduxjs/toolkit";
import cartReducer from "./cartSlice";
import { Cart } from "./Cart";

function renderWithStore(preloadedState) {
  const store = configureStore({ reducer: { cart: cartReducer }, preloadedState });
  return render(
    <Provider store={store}>
      <Cart />
    </Provider>
  );
}

test("삭제 버튼을 클릭하면 해당 상품이 목록에서 사라진다", () => {
  renderWithStore({ cart: { items: [{ id: "p1", name: "키보드", quantity: 1 }] } });

  expect(screen.getByText("키보드")).toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "삭제" }));
  expect(screen.queryByText("키보드")).not.toBeInTheDocument();
});
```

`preloadedState`로 원하는 초기 상태를 직접 주입할 수 있다는 점이 핵심입니다. "장바구니에 상품이 이미 있는 상태"를 재현하기 위해 UI를 여러 번 클릭할 필요 없이, 상태를 바로 설정해 원하는 시나리오만 정확히 테스트합니다.

## 실전 프로젝트: E-Commerce 미니 앱

지금까지 배운 모든 것을 조합해, 상품 목록·장바구니·주문 세 기능을 가진 앱을 설계합니다.

```
src/
  app/
    store.ts            # 18·28편: configureStore + RootState/AppDispatch
    hooks.ts             # 28편: 타입 지정된 useAppSelector/useAppDispatch
  features/
    products/
      productsApi.ts     # 24·27·28편: RTK Query + entityAdapter + TypeScript
      ProductList.tsx
    cart/
      cartSlice.ts        # 17편: createSlice, 08편: 불변 업데이트
      cartSelectors.ts     # 14편: createSelector로 합계 메모이제이션
      Cart.tsx
    checkout/
      checkoutThunk.ts     # 22편: 복잡한 검증+dispatch 조합
      OrderConfirmation.tsx
  shared/
    api/baseApi.ts         # 26편: injectEndpoints 공유 기반
```

```typescript
// features/cart/cartSlice.ts — 17·28편 통합
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}
interface CartState {
  items: CartItem[];
}

const cartSlice = createSlice({
  name: "cart",
  initialState: { items: [] } as CartState,
  reducers: {
    itemAdded: (state, action: PayloadAction<CartItem>) => {
      const existing = state.items.find((i) => i.id === action.payload.id);
      if (existing) {
        existing.quantity += action.payload.quantity; // Immer draft — 08편의 원칙이 내부적으로 지켜짐
      } else {
        state.items.push(action.payload);
      }
    },
    itemRemoved: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter((i) => i.id !== action.payload);
    },
  },
});

export const { itemAdded, itemRemoved } = cartSlice.actions;
export default cartSlice.reducer;
```

```typescript
// features/cart/cartSelectors.ts — 14편
import { createSelector } from "@reduxjs/toolkit";
import type { RootState } from "../../app/store";

const selectCartItems = (state: RootState) => state.cart.items;

export const selectCartTotal = createSelector([selectCartItems], (items) =>
  items.reduce((sum, item) => sum + item.price * item.quantity, 0)
);
```

```typescript
// features/checkout/checkoutThunk.ts — 22·28편
import type { AppDispatch, RootState } from "../../app/store";
import { itemRemoved } from "../cart/cartSlice";

export const submitOrder = () => async (dispatch: AppDispatch, getState: () => RootState) => {
  const { items } = getState().cart;
  if (items.length === 0) {
    dispatch({ type: "checkout/rejected", payload: "장바구니가 비어 있습니다" });
    return;
  }
  dispatch({ type: "checkout/started" });
  try {
    const response = await fetch("/api/orders", { method: "POST", body: JSON.stringify({ items }) });
    const order = await response.json();
    dispatch({ type: "checkout/succeeded", payload: order });
    items.forEach((item) => dispatch(itemRemoved(item.id))); // 09편: 성공 후 후속 액션 조합
  } catch (error) {
    dispatch({ type: "checkout/failed", payload: (error as Error).message });
  }
};
```

## 전체 30편 대응표

| 편 | 주제 | 이 프로젝트에서의 위치 |
|---|---|---|
| 01-05 | JS/TS 기초 | `PayloadAction<T>`, 구조 분해, `reduce()`, async/await 전반 |
| 06-10 | Redux 핵심 개념 | `createStore` 원리, 불변성, 데이터 흐름, DevTools |
| 11-15 | React-Redux 연동 | `Provider`, `useSelector`/`useDispatch`, 컴포넌트 최적화, selector 패턴 |
| 16-20 | Redux Toolkit | `cartSlice.ts`의 `createSlice`, `configureStore` |
| 21-25 | 미들웨어와 사이드 이펙트 | `checkoutThunk.ts`, `productsApi.ts`의 RTK Query |
| 26-28 | 고급 패턴과 아키텍처 | 폴더 구조, `productsApi`의 정규화, 전체 코드의 TypeScript화 |
| 29-30 | 실무 마스터 레벨 | DevTools 디버깅 워크플로, 이 편의 테스트 전략 |

## 시리즈를 마치며

01편의 `var`/`let`/`const` 스코프 규칙에서 시작해, 30편의 타입 안전한 E-Commerce 프로젝트까지 왔습니다. 돌아보면 이 시리즈는 하나의 질문을 계속 반복해서 던졌습니다. **"이 상태 변화가 예측 가능한가?"**

- 07편의 순수 리듀서 규칙은 "같은 입력엔 같은 출력"을 보장했습니다.
- 08편의 불변성은 "무엇이 바뀌었는지 참조 비교만으로 알 수 있게" 했습니다.
- 09편의 단방향 데이터 흐름은 "상태가 어디서 왜 바뀌었는지 추적 가능하게" 했습니다.
- 21~24편의 미들웨어 체계는 "부수 효과가 있어야만 하는 곳"을 명확한 경계 안에 가뒀습니다.
- 27편의 정규화와 28편의 타입은 "데이터가 커져도 그 예측 가능성이 무너지지 않게" 지탱했습니다.

Redux Toolkit이 보일러플레이트를 줄여준 것은 사실이지만, 이 시리즈가 순수 Redux(Phase 1-3)부터 시작한 이유는 그 예측 가능성이 **어디에서, 왜 나오는지**를 먼저 손으로 확인하길 바랐기 때문입니다. RTK가 감춘 것이 무엇인지 아는 개발자와 모르는 개발자는, 문제가 생겼을 때 정확히 그 지점에서 갈립니다.

이제 새로운 프로젝트에서 상태 관리가 복잡해지기 시작할 때, "정말 Redux가 필요한가"(10편), "필요하다면 어떤 도구 조합이 적절한가"(22~24편), "구조를 어떻게 잡을 것인가"(26~27편)를 스스로 판단할 수 있는 기반을 갖췄을 것입니다. 다음은 실제 프로젝트에 이 판단을 적용해볼 차례입니다.

## 실무 체크리스트

- 리듀서는 mock 없이, thunk는 가짜 dispatch/getState로, RTK Query는 MSW로, 컴포넌트는 실제 Store를 감싸는 방식으로 테스트 전략을 구분하고 있는가?
- 컴포넌트 테스트가 내부 구현이 아니라 사용자가 보는 화면과 상호작용을 기준으로 작성되어 있는가?
- 새 프로젝트를 시작할 때 이 시리즈의 판단 기준(10편, 22~24편, 26~27편)을 참고해 도구와 구조를 선택하고 있는가?

## 연습 과제

### 기초(★☆☆)
- `cartSlice`의 `itemAdded`가 이미 담긴 상품의 수량을 올바르게 누적하는지 리듀서 단위 테스트로 검증해보세요.

### 중급(★★☆)
- `submitOrder` thunk가 성공 시 장바구니의 모든 항목에 대해 `itemRemoved`를 dispatch하는지, 가짜 dispatch로 호출 횟수와 인자를 검증해보세요.

### 고급(★★★)
- `ProductList` → `Cart` → `OrderConfirmation`으로 이어지는 전체 흐름(상품 추가 → 장바구니 확인 → 주문 제출)을 하나의 통합 테스트로 작성해보세요.

## 요약

- 리듀서는 순수 함수이므로 mock 없이, thunk는 가짜 dispatch/getState로, RTK Query는 MSW로, 컴포넌트는 실제 Store로 감싸 테스트한다.
- E-Commerce 프로젝트는 1~29편의 거의 모든 개념이 하나의 코드베이스 안에서 자연스럽게 조합될 수 있음을 보여준다.
- Redux 학습의 핵심은 도구(RTK)의 사용법이 아니라, 상태 변화의 예측 가능성을 지키는 원칙(순수성·불변성·단방향 흐름)이다.

## 참고 문헌 및 출처(추천)

- Redux 공식 문서, "Writing Tests"
- Redux Toolkit 공식 문서, "Usage With TypeScript, Testing"
- Mock Service Worker(MSW) 공식 문서, "Redux Toolkit Integration"
- Testing Library 공식 문서, "Guiding Principles"

---

## 시리즈 목차

- 전체 커리큘럼: [00. Redux 마스터하기 - 학습 로드맵](../getting-started-redux/)
