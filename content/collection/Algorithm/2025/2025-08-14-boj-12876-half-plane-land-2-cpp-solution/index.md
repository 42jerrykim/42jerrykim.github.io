---
title: "[Algorithm] C++ 백준 12876번: 반평면 땅따먹기 2"
description: "직선 (a, b)을 동적으로 추가/삭제하고 질의 x마다 ax+b의 최댓값을 구하는 문제를 세그먼트 트리(시간 구간) 오프라인 + 롤백 가능한 Li Chao Tree로 해결한다. 공집합 시 EMPTY 처리, 64비트 안전, O(N log N log X) 복잡도로 30만 연산을 통과한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Data Structures
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-12876
- C++
- cpp
- Data Structures
- 자료구조
- Li Chao Tree
- Convex Hull Trick
- CHT
- 세그먼트 트리
- Segment Tree
- Offline Processing
- 오프라인 처리
- Rollback
- 롤백
- Dynamic Lines
- 동적 직선 집합
- Line Container
- 라인 컨테이너
- Max Query
- 최대값 질의
- Range Add
- 구간 추가
- Time SegTree
- 시간 세그트리
- Query on X
- x좌표 질의
- 64-bit Integer
- 64비트 정수
- __int128
- Overflow Safety
- 오버플로 안전
- Fast IO
- 빠른 입출력
- Complexity Analysis
- 복잡도 분석
- Proof of Correctness
- 정당성 증명
- Exchange/Divide and Conquer on Structure
- 구조 분할 정복
- Persistent-like
- 준영속
- Competitive Programming
- 경쟁프로그래밍
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Templates
- 템플릿
- Geometry-ish
- 기하 아이디어
- Function Maximum
- 함수 최대값
- Integer Domain
- 정수 좌표
- Logarithmic
- 로그 복잡도
- DS on SegTree
- 세그트리 내 자료구조
- Recursive DFS
- 재귀 DFS
- KAIST RUN Contest
- 카이스트 RUN
- Editorial
- 에디토리얼
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/12876
- 요약: 공집합에서 시작해 연산 순서대로 (1) 직선 `(a, b)` 추가, (2) 특정 추가 연산으로 넣었던 직선 제거, (3) 주어진 `x`에 대해 남아있는 모든 직선 중 `ax + b`의 최댓값을 출력한다. 집합이 비어 있으면 `EMPTY`를 출력한다.

### 제한/스펙
- `1 ≤ N ≤ 300,000` (연산 개수)
- `-1e9 ≤ a, b, x ≤ 1e9`
- 출력 시 공집합이면 `EMPTY`, 아니면 최댓값(정수)

## 입출력 형식/예제

예제 입력 1
```
7
3 1
1 1 2
3 3
1 -1 100
3 1
2 4
3 1
```

예제 출력 1
```
EMPTY
5
99
5
```

## 접근 개요(아이디어 스케치)
- 핵심 모델: 각 원소는 직선 `y = a x + b`. 질의는 고정된 `x`에서의 최대값.
- 난점: 직선이 중간에 삭제되므로 단순 Li Chao Tree의 “온라인 추가만” 구조로는 제거를 처리하기 어렵다.
- 오프라인 전환: 각 추가 연산의 “활성 시간 구간” `[start, end)`을 복원한다. 이 구간에 해당하는 노드에 직선을 보관하는 “시간 축 세그먼트 트리”를 만든다.
- DFS 진행: 세그먼트 트리 DFS를 돌며 현재 노드 구간에 해당하는 직선들을 Li Chao Tree에 삽입한다. 리프(하나의 시간점)에서 질의를 평가하고 상위로 되돌아갈 때 Li Chao Tree 상태를 롤백한다.
- Li Chao 롤백: 노드별로 바뀐 라인의 이전 값을 스택에 저장해 되돌릴 수 있게 구현하면, 시간 축을 따라 직선의 삽입/제거 효과를 모사할 수 있다.

```mermaid
flowchart TD
  A[연산 파싱] --> B[추가 연산의 start/end 계산]
  B --> C[시간 세그먼트 트리에 (라인, 구간) 배치]
  C --> D[DFS]
  D --> E[노드에 속한 라인들 Li Chao에 삽입]
  E --> F{리프?}
  F -- 예 --> G[해당 시간의 질의들 평가]
  F -- 아니오 --> H[좌/우 자식 DFS]
  H --> I[리턴 시 Li Chao 롤백]
```

## 알고리즘 설계
- 상태/자료구조:
  - 시간 세그먼트 트리: 노드마다 그 구간 전체에서 “활성인 직선” 목록 저장
  - Li Chao Tree: 구간 최대값 질의용. 각 갱신 시 이전 라인을 기록해 롤백 지원
- 절차:
  1) 입력을 한 번 훑어 각 추가 연산의 종료 시점(삭제 시각, 없으면 `n+1`)을 결정
  2) `[start, end)` 구간에 해당 직선을 세그먼트 트리에 배치
  3) DFS로 세그먼트 트리를 순회하며 각 노드 직선을 Li Chao에 추가, 리프 시간에 모인 질의를 모두 평가
  4) 자식 방문 종료 후 Li Chao를 롤백하여 상위 상태 복원
- 정당성(요지): 각 시간 `t`에서 활성인 직선 집합은 해당 리프까지의 경로에 추가된 직선들의 합집합과 정확히 일치한다. Li Chao Tree는 “최댓값” 유지에 적합하고, 롤백은 상위 구간의 상태를 보존한다.

## 복잡도
- 시간: 각 직선이 O(log N)개 노드에 배치되고, Li Chao 삽입/질의가 O(log X) → 전체 O(N log N log X)
- 공간: 세그먼트 트리의 버킷 합 O(N log N) (실제 상수는 낮음), Li Chao 노드 풀 O(삽입 수)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
static const ll X_MIN = -1000000000LL;
static const ll X_MAX =  1000000000LL + 1; // [X_MIN, X_MAX)
static const long long NEG_INF = (long long)-4e18;

struct Line { ll m, b; }; // y = m x + b

struct LiChao {
    struct Node {
        Line ln; int lc, rc; // child indices
        Node() : ln({0, NEG_INF}), lc(0), rc(0) {}
    };
    vector<Node> pool; int root = 0;
    vector<pair<int, Line>> history; // (index, old line)

    LiChao() { pool.reserve(1<<22); pool.push_back(Node()); }
    int new_node(){ pool.push_back(Node()); return (int)pool.size()-1; }
    inline __int128 f(const Line& L, ll x) const { return (__int128)L.m * x + L.b; }

    void add_line(Line nw){ add_line(root, X_MIN, X_MAX, nw); }
    void add_line(int &n, ll l, ll r, Line nw){
        if(n==0) n = new_node();
        int idx = n; ll mid = (l + r) >> 1;
        Line lo = pool[idx].ln, hi = nw;
        bool leftBetter = f(hi, l) > f(lo, l);
        bool midBetter  = f(hi, mid) > f(lo, mid);
        if(midBetter) swap(lo, hi);
        if(pool[idx].ln.m != lo.m || pool[idx].ln.b != lo.b){
            history.emplace_back(idx, pool[idx].ln);
            pool[idx].ln = lo;
        }
        if(r - l == 1) return;
        if(leftBetter != midBetter) add_line(pool[idx].lc, l, mid, hi);
        else                        add_line(pool[idx].rc, mid, r, hi);
    }

    ll query(ll x) const { return root? (ll)query_rec(root, X_MIN, X_MAX, x) : NEG_INF; }
    __int128 query_rec(int n, ll l, ll r, ll x) const{
        if(n==0) return (__int128)NEG_INF;
        const Node &nd = pool[n]; __int128 res = f(nd.ln, x);
        if(r - l == 1) return res; ll mid = (l + r) >> 1;
        if(x < mid) return max(res, query_rec(nd.lc, l, mid, x));
        return max(res, query_rec(nd.rc, mid, r, x));
    }

    void rollback(size_t checkpoint){
        while(history.size() > checkpoint){ auto [idx, oldLine] = history.back(); history.pop_back(); pool[idx].ln = oldLine; }
    }
};

struct SegmentTree {
    int n; vector<vector<Line>> bucket; // 1..n+1 구간
    SegmentTree(int n_) : n(n_), bucket(4*(n_+5)) {}
    void add_range(int node, int L, int R, int ql, int qr, const Line &ln){
        if(qr<=L || R<=ql) return; if(ql<=L && R<=qr){ bucket[node].push_back(ln); return; }
        int mid=(L+R)>>1; add_range(node<<1, L, mid, ql, qr, ln); add_range(node<<1|1, mid, R, ql, qr, ln);
    }
};

int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; if(!(cin>>n)) return 0;

    vector<int> type(n+1); vector<long long> A(n+1), B(n+1), X(n+1);
    vector<int> start(n+1, -1), fin(n+1, -1);
    vector<vector<pair<long long,int>>> queriesAt(n+2);
    int qcnt=0;
    for(int i=1;i<=n;++i){
        cin>>type[i];
        if(type[i]==1){ cin>>A[i]>>B[i]; start[i]=i; fin[i]=n+1; }
        else if(type[i]==2){ int idx; cin>>idx; fin[idx]=i; }
        else { cin>>X[i]; queriesAt[i].push_back({X[i], qcnt++}); }
    }

    SegmentTree seg(n+1);
    for(int i=1;i<=n;++i){ if(type[i]==1){ int L=start[i], R=fin[i]; if(L<R) seg.add_range(1,1,n+1,L,R, Line{A[i],B[i]}); } }

    vector<string> ans(qcnt); LiChao lichao; int active=0;
    function<void(int,int,int)> dfs = [&](int node,int L,int R){
        size_t cp = lichao.history.size(); int saved=active;
        for(const auto &ln: seg.bucket[node]){ lichao.add_line(ln); ++active; }
        if(L+1==R){
            for(auto &q: queriesAt[L]){ if(active==0) ans[q.second] = "EMPTY"; else ans[q.second] = to_string(lichao.query(q.first)); }
        } else {
            int mid=(L+R)>>1; dfs(node<<1,L,mid); dfs(node<<1|1,mid,R);
        }
        lichao.rollback(cp); active=saved;
    };
    dfs(1,1,n+1);

    for(int i=0;i<qcnt;++i) cout<<ans[i]<<'\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- 집합이 비어 있는 상태에서의 질의 → 반드시 `EMPTY`
- 같은 `(a, b)`가 여러 번 추가되는 경우 → 최대값은 동일하므로 영향 없음(롤백 구조상 올바르게 처리)
- `a`, `b`, `x`의 최댓값 조합 → 내부 계산은 `__int128`로 안전하게 평가 후 `long long`으로 출력
- 삭제가 없는 직선(끝까지 활성) → 구간 `[start, n+1)`에 정상 배치

## 제출 전 점검
- Li Chao 평가 시 `__int128` 사용 여부 확인
- 시간 세그먼트 트리 DFS에서 삽입/롤백 균형 확인
- 공집합 시 문자열 출력 처리(`EMPTY`)
- 빠른 입출력 설정 및 경계 포함 관계 재확인(`[start, end)`)

## 참고자료/유사문제
- Li Chao Tree(Convex Hull Trick) 소개 및 응용
- 시간 세그먼트 트리(오프라인 동적 추가/삭제) 전형


