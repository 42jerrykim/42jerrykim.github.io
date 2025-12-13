---
title: "[Algorithm] C++ 백준 31603번: 트리 퀴즈"
description: "정렬 키를 (x, LCA, y) 사전순으로 분해한다. 임계 라벨 t까지 F_x(t)=|{y: LCA(x,y)≤t}|를 오일러 투어 구간에 이벤트를 얹은 펜윅으로 일괄 집계하고, 이분으로 최소 L을 찾은 뒤 영속 세그먼트 트리에서 그룹 L 내 y의 k번째를 선택한다. 4초/1GB 제약 대응."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Tree
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-31603
- cpp
- C++
- Tree
- 트리
- LCA
- Lowest Common Ancestor
- 최소 공통 조상
- Euler Tour
- 오일러 투어
- Binary Lifting
- 이진 점프
- Fenwick Tree
- 펜윅트리
- Binary Indexed Tree
- 비트
- Persistent Segment Tree
- 영속 세그먼트 트리
- PST
- Segment Tree
- 세그먼트 트리
- Offline Query
- 오프라인 쿼리
- Parallel Binary Search
- 병렬 이분 탐색
- Parametric Search
- 매개변수 탐색
- Range Add
- 구간 더하기
- Point Query
- 점 질의
- K-th Order Statistic
- k번째 원소
- Order Statistics
- 사전순 정렬
- Lexicographic Order
- Sorting
- 정렬
- Query Processing
- 쿼리 처리
- Depth
- 깊이
- tin tout
- 진입-이탈 시간
- Ancestor
- 조상
- Subtree
- 서브트리
- Events
- 이벤트
- BIT events
- 라벨 임계치
- Label Threshold
- Counting
- 개수 세기
- Range Query
- 구간 질의
- Data Structures
- 자료구조
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Implementation
- 구현
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Fast IO
- 입출력 최적화
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/31603
- 요약: 루트 트리에서 `LCA(x, y)`를 이용해 생성한 길이 `n^2`의 배열 `L`을 비내림차순으로 정렬했을 때, 여러 쿼리 `k`에 대해 `L[k]`를 구한다. 정의상 값은 `((x-1)*n*n + (LCA(x,y)-1)*n + (y-1))`이며 배열은 1-indexed.

### 제한/스펙
- `1 ≤ n ≤ 100000`, `1 ≤ q ≤ 100000`
- 시간 4초, 메모리 1024MB
- 루트의 부모는 `0`, 나머지 노드 `i`는 부모 `p[i]`를 가짐(올바른 루트 트리 보장)

## 입출력

예제 입력 1
```
5 3
3 0 2 2 3
1
18
25
```

예제 출력 1
```
0
82
124
```

## 접근 개요
- 핵심 정렬 키는 `(x, L, y)`의 사전순(여기서 `L = LCA(x, y)`). 따라서 쿼리 `k`에 대해 먼저 `x = (k-1)/n + 1`, `r = (k-1)%n + 1`로 환산하면, 고정된 `x`에 대해 `LCA(x, y)` 오름차순으로 y를 훑었을 때 `r`번째 원소의 `(L, y)`를 찾는 문제가 된다.
- 임계 라벨 `t`까지의 누적 개수 `F_x(t) = |{ y ∈ [1..n] : LCA(x, y) ≤ t }|`를 빠르게 계산해, 이분 탐색으로 최소 `L`을 찾는다. 이후 그룹 `L` 내부에서 `y`를 오름차순으로 `pos = r - F_x(L-1)`번째 선택한다.
- 관건은 `F_x(t)`를 모든 `x`에 대해 빠르게 얻는 것과, 그룹 `L`에서 `y`의 `k`번째를 빠르게 뽑는 것이다.

```mermaid
flowchart TD
  A[오일러 투어 tin/tout, 깊이, binary lifting] --> B[라벨 임계치 t별 이벤트 구성]
  B --> C[Fenwick에 구간가중치 누적 → F_x(t) = BIT.sum(tin[x])]
  C --> D[이분 탐색으로 최소 L 찾기]
  D --> E[영속 세그트리로 (subtree(L) \ subtree(child))의 y 중 k번째]
  E --> F[정답: (x-1)*n^2 + (L-1)*n + (y-1)]
```

## 알고리즘 설계
- 전처리
  - 오일러 투어로 `tin[u], tout[u]`, `depth[u]`, 서브트리 크기 `sz[u]` 계산. 이때 `inv[tin]=u` 보관.
  - binary lifting 테이블 `up[u][j]` 구성(조상 점프용).
  - `inv` 순서(=라벨 순서 1..n)로 영속 세그먼트 트리(PST) 버전 `root[t]`를 만든다. 이는 "라벨 ≤ t"인 노드의 존재를 세그트리에 누적한 것과 동일하며, 구간 k번째 질의가 가능하다.

- `F_x(t)`의 일괄 집계(오프라인)
  - 사실 `F_x(t)`는 "라벨 `≤ t`인 어떤 노드 `l`이 `LCA(x, y)`가 되는 모든 `y`"를 세는 문제다.
  - 트리 관찰: `LCA(x,y)=l`인 모든 `y`는 `subtree(l)`에 속하며, `l ≠ x`이면 경로 `l→x`의 첫 자식 `c`의 서브트리는 제외된다. 임계치 `t`까지 누적시, `l`가 활성화되는 시점에 `[tin[l], tout[l]]`에 `+sz[l]`를 더하고, `l`의 자식 `c`마다 부모라벨이 활성화될 때 `[tin[c], tout[c]]`에 `-sz[c]`를 더하면 `BIT.sum(tin[x]) = F_x(t)`가 된다.
  - 구현은 라벨 `t`를 1..n으로 순회하며 이벤트(구간 +v/-v)를 펜윅 트리에 누적하고, 이분 탐색 중간값에 해당하는 쿼리들을 동일 `t` 버킷에 모아 한 번에 판정한다. 전체가 `O((n+q) log n)` 수준.

- 그룹 `L`에서 `y`의 `pos`번째 찾기
  - `L = x`이면 전체 `subtree(L)`이 대상. `L ≠ x`이면 경로 `L→x`의 첫 자식 `c`를 찾아 `subtree(L) \ subtree(c)`만 대상.
  - 라벨 기준 오름차순 `y`의 `k`번째는 PST 두 버전 차로 구간의 k번째를 구할 수 있다: `kth( root[tout(L)] - root[tin(L)-1] - (root[tout(c)] - root[tin(c)-1]), pos )`.

- 올바름 근거(요지)
  - `(x, L, y)` 사전순: 고정 `x`에서 먼저 `L`이 증가하며, 같은 `L`에서는 `y` 증가. `F_x(t)`는 정확히 임계치까지의 누적 개수를 준다.
  - 이벤트 구성은 각 `l`이 활성화될 때 `subtree(l)` 전체를 포함시키고, 더 깊은 LCA를 갖는 `y`가 속한 자식 서브트리를 부모 라벨 활성화 시점에 차감하여 상위 LCA 집합만 남긴다.
  - PST는 라벨≤T 노드만 포함되도록 축적되어 특정 서브트리 구간의 k번째 라벨을 정확히 찾는다.

## 복잡도
- 전처리: DFS/Binary Lifting/PST 구축 `O(n log n)`
- 쿼리: 병렬 이분 탐색 판정 각 단계 `O(n + q)` 이벤트 스윕, 전체 `O((n + q) log n)`
- 메모리: PST 노드 수 ≈ `O(n log n)`(상수 최적화 필수), Fenwick `O(n)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    int n;
    vector<long long> f;
    Fenwick() {}
    Fenwick(int n): n(n), f(n+2, 0) {}
    void reset() { fill(f.begin(), f.end(), 0); }
    void add(int i, long long v){ for(; i<=n+1; i+=i&-i) f[i]+=v; }
    long long sum(int i){ long long s=0; for(; i>0; i-=i&-i) s+=f[i]; return s; }
};

struct PST {
    struct Node { int l, r, s; };
    int n;
    vector<Node> t;
    vector<int> root; // versions by Euler time
    PST(int n): n(n) {
        t.reserve(n * 40);
        t.push_back({0,0,0}); // node 0: null
        root.assign(n+1, 0);
    }
    int newnode(int from){
        t.push_back(t[from]);
        return (int)t.size()-1;
    }
    int upd(int prev, int L, int R, int pos){
        int cur = newnode(prev);
        t[cur].s = t[prev].s + 1;
        if(L==R) return cur;
        int mid = (L+R)>>1;
        if(pos<=mid){
            int nl = upd(t[prev].l, L, mid, pos);
            t[cur].l = nl;
        }else{
            int nr = upd(t[prev].r, mid+1, R, pos);
            t[cur].r = nr;
        }
        return cur;
    }
    // kth in (A = subtree(L)) \ (B = subtree(c)) using versions
    int kth_diff(int aR, int aL, int bR, int bL, int L, int R, int k){
        if(L==R) return L;
        int aLch = t[aL].l, aRch = t[aR].l;
        int bLch = t[bL].l, bRch = t[bR].l;
        int leftCnt = (t[aRch].s - t[aLch].s) - (t[bRch].s - t[bLch].s);
        int mid = (L+R)>>1;
        if(k<=leftCnt){
            return kth_diff(aRch, aLch, bRch, bLch, L, mid, k);
        }else{
            int aLr = t[aL].r, aRr = t[aR].r;
            int bLr = t[bL].r, bRr = t[bR].r;
            return kth_diff(aRr, aLr, bRr, bLr, mid+1, R, k-leftCnt);
        }
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    if(!(cin >> n >> q)) return 0;
    vector<int> par(n+1);
    int root = -1;
    for(int i=1;i<=n;i++){
        cin >> par[i];
        if(par[i]==0) root = i;
    }
    vector<vector<int>> g(n+1);
    for(int i=1;i<=n;i++) if(par[i]!=0) g[par[i]].push_back(i);

    const int LOG = 17; // since n<=1e5
    vector<array<int, 18>> up(n+1);
    vector<int> depth(n+1,0), tin(n+1,0), tout(n+1,0), inv(n+1,0), sz(n+1,0);

    // Iterative DFS for tin/tout, depth, up[0], sz
    int timer = 0;
    vector<pair<int,int>> st;
    up[root][0] = 0;
    depth[root]=0;
    st.push_back({root, 0});
    while(!st.empty()){
        auto [u, state] = st.back(); st.pop_back();
        if(state==0){
            tin[u] = ++timer;
            inv[timer] = u;
            sz[u] = 1;
            st.push_back({u, 1});
            for(int v: g[u]){
                up[v][0] = u;
                depth[v] = depth[u] + 1;
                st.push_back({v, 0});
            }
        }else{
            for(int v: g[u]) sz[u] += sz[v];
            tout[u] = timer;
        }
    }

    for(int j=1;j<=LOG;j++){
        for(int v=1; v<=n; v++){
            up[v][j] = up[ up[v][j-1] ][j-1];
        }
    }

    auto jump = [&](int x, int k){
        for(int j=0;j<=LOG;j++){
            if(k & (1<<j)) x = up[x][j];
        }
        return x;
    };

    // Persistent segment tree over labels 1..n, versions by Euler time
    PST pst(n);
    pst.root[0] = 0;
    for(int i=1;i<=n;i++){
        int id = inv[i]; // node id whose label is i
        pst.root[i] = pst.upd(pst.root[i-1], 1, n, id);
    }

    // Build events for F_x(t): range-add via difference on Euler index
    // At threshold t = node label l: +sz[l] on [tin[l], tout[l]]
    // At threshold t = parent label of c: -sz[c] on [tin[c], tout[c]]
    vector<vector<pair<int,int>>> events(n+2);
    for(int l=1;l<=n;l++){
        events[l].push_back({tin[l],  sz[l]});
        events[l].push_back({tout[l]+1, -sz[l]});
        if(par[l]!=0){
            int t = par[l];
            events[t].push_back({tin[l],  -sz[l]});
            events[t].push_back({tout[l]+1, +sz[l]});
        }
    }

    // Read queries: map k -> (x, r)
    struct Query { long long k; int x; int r; };
    vector<Query> qs(q);
    for(int i=0;i<q;i++){
        long long k; cin >> k;
        int x = int((k-1) / n) + 1;
        int r = int((k-1) % n) + 1;
        qs[i] = {k, x, r};
    }

    // Parallel binary search to find label L for each query
    vector<int> lo(q, 1), hi(q, n);
    vector<vector<int>> buckets(n+2);
    Fenwick bit(n+2);
    while(true){
        bool changed = false;
        for(int t=1;t<=n;t++) buckets[t].clear();
        for(int i=0;i<q;i++){
            if(lo[i]<hi[i]){
                int mid = (lo[i]+hi[i])>>1;
                buckets[mid].push_back(i);
                changed = true;
            }
        }
        if(!changed) break;
        bit.reset();
        for(int t=1;t<=n;t++){
            for(auto &ev: events[t]) bit.add(ev.first, ev.second);
            for(int idx: buckets[t]){
                int x = qs[idx].x;
                long long val = bit.sum(tin[x]);
                if(val >= qs[idx].r) hi[idx] = t;
                else lo[idx] = t+1;
            }
        }
    }
    vector<int> L(q);
    for(int i=0;i<q;i++) L[i] = lo[i];

    // One more pass to get F_x(L-1)
    vector<vector<int>> buck2(n+1);
    for(int i=0;i<=n;i++) buck2[i].clear();
    for(int i=0;i<q;i++){
        int t = L[i]-1; if(t<0) t=0;
        buck2[t].push_back(i);
    }
    vector<long long> Fless(q, 0);
    bit.reset();
    // t=0 first (no events applied)
    for(int idx: buck2[0]){
        int x = qs[idx].x;
        (void)x; // value is zero at t=0
        Fless[idx] = 0;
    }
    for(int t=1;t<=n;t++){
        for(auto &ev: events[t]) bit.add(ev.first, ev.second);
        for(int idx: buck2[t]){
            int x = qs[idx].x;
            Fless[idx] = bit.sum(tin[x]);
        }
    }

    // Answer each query: find y within group L with rank pos = r - F(L-1)
    for(int i=0;i<q;i++){
        int x = qs[i].x;
        int l = L[i];
        int pos = qs[i].r - (int)Fless[i];
        int c = 0;
        if(l != x){
            int k = depth[x] - depth[l] - 1;
            c = jump(x, k);
        }
        int aR = pst.root[ tout[l] ];
        int aL = pst.root[ tin[l]-1 ];
        int bR = (c ? pst.root[ tout[c] ] : 0);
        int bL = (c ? pst.root[ tin[c]-1 ] : 0);
        int y = pst.kth_diff(aR, aL, bR, bL, 1, n, pos);
        long long N = (long long)n;
        long long res = (long long)(x-1) * N * N + (long long)(l-1) * N + (long long)(y-1);
        cout << res << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `x = L`인 경우(루트 포함)와 `x ≠ L`에서 `child c` 추출 로직 분기
- `pos = r - F_x(L-1)` 계산 시 1-indexed 일관성
- Fenwick 이벤트의 시작/끝 오프바이원: `[tin, tout]`와 `tout+1`에 주의
- PST 버전 인덱싱: `root[tin-1]`이 0 버전일 수 있음(경계 처리)
- 깊이 차 `depth[x]-depth[L]-1`이 0이 될 때 `c=0`으로 처리됨(=제외 없음)

## 제출 전 점검
- 오일러 라벨/버전 일관성 확인(`inv[tin]=u`)
- Fenwick 초기화/이벤트 누적 순서 정확성
- 이분 탐색 수렴 조건(`lo==hi`)과 버킷 재할당 누락 여부 점검
- 64비트 누적(`n^2` 곱셈) 오버플로 방지(중간 계산은 `long long`)
- 빠른 입출력 설정 확인

## 참고자료/유사문제
- LCA + 오프라인 집계 + k번째 선택(영속 세그먼트 트리) 조합 전형 문제들
- 트리에서의 사전순 정렬/랭크 질의 → 임계치 누적 후 그룹 내 선택 패턴


