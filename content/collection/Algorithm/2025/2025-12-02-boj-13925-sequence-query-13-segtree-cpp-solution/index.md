---
title: "[Algorithm] 13925 수열과 쿼리 13"
description: "구간 덧셈, 곱셈, 값 설정과 구간 합 쿼리를 처리하는 Lazy Propagation 세그먼트 트리 문제. 선형 함수 f(x)=mul*x+add로 모든 연산을 통합하여 해결합니다."
category: "Algorithm"
tags:
  - 알고리즘
  - 세그먼트트리
  - Lazy Propagation
  - 구간쿼리
  - MOD연산
  - 수열처리
  - 범위업데이트
  - 범위쿼리
  - 라지데이터
  - 고급자료구조
  - segment tree
  - lazy propagation
  - range update
  - range query
  - modular arithmetic
  - sequence queries
  - data structure
  - competitive programming
  - algorithm
  - C++ solution
  - 백준
  - baekjoon
  - BOJ
  - 수열과쿼리
  - 선형함수
  - 함수합성
  - 구간덧셈
  - 구간곱셈
  - 구간값설정
  - MOD10^9+7
  - 최적화
  - 효율적알고리즘
  - 트리기반자료구조
  - 동적쿼리
  - 배열처리
  - 온라인처리
  - 시간복잡도O(logN)
  - 공간복잡도O(N)
  - 분할정복
  - 펜윅트리
  - 고급쿼리처리
date: 2025-12-02
lastmod: 2025-12-02
image: wordcloud.png
---

## 문제 분석

**BOJ 13925 - 수열과 쿼리 13**은 다음 네 가지 쿼리를 효율적으로 처리해야 합니다:

1. **쿼리 1**: 구간 `[x, y]`에 모든 원소에 `v`를 더함 (덧셈)
2. **쿼리 2**: 구간 `[x, y]`에 모든 원소에 `v`를 곱함 (곱셈)
3. **쿼리 3**: 구간 `[x, y]`의 모든 원소를 `v`로 설정 (값 설정)
4. **쿼리 4**: 구간 `[x, y]`의 합을 구함 (MOD 10^9+7)

## 핵심 아이디어

일반적인 Lazy Propagation 세그먼트 트리는 한 종류의 연산만 처리합니다. 이 문제의 핵심은 **세 가지 다른 연산을 선형 함수로 통합**하는 것입니다.

모든 연산을 다음과 같이 표현할 수 있습니다:
$$f(x) = \text{mul} \cdot x + \text{add}$$

- **덧셈** (+v): `mul = 1, add = v` → f(x) = 1·x + v = x + v
- **곱셈** (×v): `mul = v, add = 0` → f(x) = v·x + 0 = v·x
- **값 설정** (=v): `mul = 0, add = v` → f(x) = 0·x + v = v

## Lazy 연산 합성

기존의 미적용 연산 `(mul, add)`에 새로운 연산 `(mul', add')`를 적용할 때:

$$f'(f(x)) = \text{mul'} \cdot (\text{mul} \cdot x + \text{add}) + \text{add'}$$
$$= (\text{mul'} \cdot \text{mul}) \cdot x + (\text{mul'} \cdot \text{add} + \text{add'})$$

따라서:
- `new_mul = (mul' × mul) % MOD`
- `new_add = (mul' × add + add') % MOD`

## 구현 코드

```cpp
// 더 많은 정보: https://42jerrykim.github.io
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
const ll MOD = 1e9 + 7;

struct LazySegTree {
    int n;
    vector<ll> tree, lazy_mul, lazy_add;
    
    LazySegTree(int n) : n(n) {
        tree.resize(4 * n);
        lazy_mul.resize(4 * n, 1);
        lazy_add.resize(4 * n, 0);
    }
    
    void build(vector<ll>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start] % MOD;
        } else {
            int mid = (start + end) / 2;
            build(arr, node * 2, start, mid);
            build(arr, node * 2 + 1, mid + 1, end);
            tree[node] = (tree[node * 2] + tree[node * 2 + 1]) % MOD;
        }
    }
    
    void push_down(int node, int start, int end) {
        if (lazy_mul[node] != 1 || lazy_add[node] != 0) {
            int mid = (start + end) / 2;
            int left = node * 2, right = node * 2 + 1;
            
            // 왼쪽 자식에 lazy 값 적용
            tree[left] = (tree[left] * lazy_mul[node] % MOD + 
                         lazy_add[node] * (mid - start + 1) % MOD) % MOD;
            lazy_mul[left] = lazy_mul[left] * lazy_mul[node] % MOD;
            lazy_add[left] = (lazy_add[left] * lazy_mul[node] % MOD + lazy_add[node]) % MOD;
            
            // 오른쪽 자식에 lazy 값 적용
            tree[right] = (tree[right] * lazy_mul[node] % MOD + 
                          lazy_add[node] * (end - mid) % MOD) % MOD;
            lazy_mul[right] = lazy_mul[right] * lazy_mul[node] % MOD;
            lazy_add[right] = (lazy_add[right] * lazy_mul[node] % MOD + lazy_add[node]) % MOD;
            
            // 부모의 lazy 초기화
            lazy_mul[node] = 1;
            lazy_add[node] = 0;
        }
    }
    
    void update(int node, int start, int end, int l, int r, ll mul, ll add) {
        if (r < start || end < l) return;
        if (l <= start && end <= r) {
            // 현재 노드의 값에 연산 적용
            tree[node] = (tree[node] * mul % MOD + add * (end - start + 1) % MOD) % MOD;
            // Lazy 값 합성
            lazy_mul[node] = lazy_mul[node] * mul % MOD;
            lazy_add[node] = (lazy_add[node] * mul % MOD + add) % MOD;
            return;
        }
        push_down(node, start, end);
        int mid = (start + end) / 2;
        update(node * 2, start, mid, l, r, mul, add);
        update(node * 2 + 1, mid + 1, end, l, r, mul, add);
        tree[node] = (tree[node * 2] + tree[node * 2 + 1]) % MOD;
    }
    
    ll query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];
        push_down(node, start, end);
        int mid = (start + end) / 2;
        return (query(node * 2, start, mid, l, r) + 
                query(node * 2 + 1, mid + 1, end, l, r)) % MOD;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    
    vector<ll> arr(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> arr[i];
    }
    
    LazySegTree st(n + 1);
    st.build(arr, 1, 1, n);
    
    int m;
    cin >> m;
    
    while (m--) {
        int op, x, y;
        ll v;
        cin >> op >> x >> y;
        
        if (op == 1) {
            // 구간 덧셈
            cin >> v;
            st.update(1, 1, n, x, y, 1, v % MOD);
        } else if (op == 2) {
            // 구간 곱셈
            cin >> v;
            st.update(1, 1, n, x, y, v % MOD, 0);
        } else if (op == 3) {
            // 구간 값 설정
            cin >> v;
            st.update(1, 1, n, x, y, 0, v % MOD);
        } else {
            // 구간 합 쿼리
            cout << st.query(1, 1, n, x, y) << '\n';
        }
    }
    
    return 0;
}
```

## 알고리즘 상세 설명

### 1. 노드 값 업데이트

연산 `(mul, add)`를 구간 `[l, r]`에 적용할 때:
- 크기가 `cnt = r - l + 1`인 구간의 합: 
  - 기존: `S`
  - 새로운: `S' = (S * mul + add * cnt) % MOD`

### 2. Lazy 값 적용

구간 업데이트 시 자식 노드에 lazy 정보를 전파:
- 자식의 새로운 mul: `child_mul = child_mul * parent_mul`
- 자식의 새로운 add: `child_add = child_add * parent_mul + parent_add`

### 3. Push Down 과정

쿼리 또는 업데이트 전에 미적용된 lazy 값을 자식에 전파하는 과정입니다.

## 시간 복잡도 분석

| 작업 | 시간복잡도 |
|------|-----------|
| 빌드 | O(N) |
| 각 쿼리 | O(log N) |
| 전체 | O((N + M) log N) |

N = 100,000, M = 100,000일 때 약 1,700만 연산으로 충분합니다.

## 예제 풀이

**입력:**
```
4
1 2 3 4
4
4 1 4
1 1 3 10
2 2 4 2
4 1 4
```

**실행 과정:**

1. 초기 배열: `[1, 2, 3, 4]`
2. `4 1 4`: 구간 [1, 4]의 합 = 1 + 2 + 3 + 4 = **10**
3. `1 1 3 10`: 구간 [1, 3]에 10을 더함 → `[11, 12, 13, 4]`
4. `2 2 4 2`: 구간 [2, 4]에 2를 곱함 → `[11, 24, 26, 8]`
5. `4 1 4`: 구간 [1, 4]의 합 = 11 + 24 + 26 + 8 = **69** (MOD 10^9+7)

**출력:**
```
10
69
```

## 주의사항

1. **MOD 연산**: 모든 계산에서 `% MOD`를 적용하여 오버플로우 방지
2. **Lazy 합성 순서**: `mul'(mul * x + add) + add'` 순서 준수
3. **구간 크기**: 합 계산 시 구간의 원소 개수(`end - start + 1`)를 고려해야 함
4. **초기 lazy 값**: `lazy_mul = 1, lazy_add = 0` (항등원)

## 확장 학습

- [세그먼트 트리 기초](https://en.wikipedia.org/wiki/Segment_tree)
- [Lazy Propagation 기법](https://codeforces.com/blog/entry/18051)

## 풀이 팁

이 문제가 어려운 이유는 **세 가지 서로 다른 연산을 하나의 프레임워크로 통합**해야 한다는 점입니다. 핵심은 모든 연산을 선형 함수로 표현하고, lazy 값을 합성 함수로 처리하는 것입니다. 비슷한 문제로 BOJ 13424, BOJ 14178 등이 있으니 참고하세요.

