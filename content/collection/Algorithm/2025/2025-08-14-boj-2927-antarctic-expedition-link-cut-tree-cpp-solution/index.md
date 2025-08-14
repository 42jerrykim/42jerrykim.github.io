---
title: "[Algorithm] cpp 백준 2927번: 남극 탐험"
description: "LCT(링크-컷 트리)로 동적 연결과 경로 합을 처리하는 풀이. bridge로 다른 컴포넌트만 연결, penguins로 노드 값 갱신, excursion으로 경로 합 질의. Splay 기반 access/makeroot로 O(log N) 보장, 엣지 케이스 및 올바름 근거 포함."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Dynamic Tree"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-2927"
- "cpp"
- "C++"
- "Data Structures"
- "자료구조"
- "Tree"
- "트리"
- "Dynamic Tree"
- "동적트리"
- "Link-Cut Tree"
- "링크컷트리"
- "Splay Tree"
- "스플레이트리"
- "Path Query"
- "경로쿼리"
- "Path Sum"
- "경로합"
- "Dynamic Connectivity"
- "동적연결성"
- "Online Query"
- "온라인쿼리"
- "Node Update"
- "노드업데이트"
- "Lazy Propagation"
- "지연전파"
- "Reversal"
- "뒤집기"
- "Access"
- "MakeRoot"
- "FindRoot"
- "Link"
- "Cut"
- "Connectivity"
- "연결성"
- "Forest"
- "포리스트"
- "Graph"
- "그래프"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Optimization"
- "최적화"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Testing"
- "테스트"
- "Invariant"
- "불변식"
- "Query"
- "질의"
- "Update"
- "갱신"
- "Sum Aggregation"
- "합집계"
- "Path Aggregation"
- "경로집계"
- "Rooting"
- "루팅"
- "Adversarial Cases"
- "최악케이스"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/2927
- 요약: 섬 N개(1…N)와 펭귄 마리 수가 주어진다. 명령은 세 가지다.
  - `bridge A B`: A, B 가 다른 컴포넌트일 때만 다리로 연결하고 "yes" 출력, 이미 경로가 있으면 "no" 출력
  - `penguins A X`: 섬 A의 펭귄 수를 X로 갱신(출력 없음)
  - `excursion A B`: A에서 B로 갈 수 있으면 경로 상 모든 섬의 펭귄 수 합을 출력, 아니면 "impossible" 출력
- 제한: \(1 \le N \le 30{,}000\), \(1 \le Q \le 300{,}000\), 펭귄 수는 \([0, 1000]\)

## 입력/출력
```
입력
N
P1 P2 ... PN
Q
<Q개의 명령: bridge | penguins | excursion>

출력
각 bridge, excursion 명령마다 한 줄 출력
```

### 예시
```
입력
3
1 2 3
5
excursion 1 3
bridge 1 2
excursion 1 2
bridge 2 3
excursion 1 3

출력
impossible
yes
3
yes
6
```

## 접근 개요
- 이 문제는 간선이 오직 "연결되지 않은 두 정점 사이"에만 추가되므로, 전체 그래프는 항상 "포리스트(여러 트리의 집합)" 상태다.
- 경로 합 질의와 노드 단위 갱신이 동시에 필요하므로, 동적 트리 자료구조인 Link-Cut Tree(LCT)를 사용하면 각 연산을 \(O(\log N)\)에 처리할 수 있다.
- 매핑
  - `bridge A B`: 컴포넌트가 다르면 `link(A, B)` 수행 후 "yes", 같으면 "no"
  - `penguins A X`: `setValue(A, X)`로 노드 값 갱신
  - `excursion A B`: 연결 여부(`connected`) 확인 후 연결이면 `queryPathSum(A, B)` 출력, 아니면 "impossible"

```mermaid
flowchart TD
  S[명령 입력] -->|bridge A B| B1{connected(A,B)?}
  B1 -- 예 --> BN[print "no"]
  B1 -- 아니오 --> BL[link(A,B)] --> BY[print "yes"]

  S -->|penguins A X| P[setValue(A,X)]

  S -->|excursion A B| E1{connected(A,B)?}
  E1 -- 아니오 --> EI[print "impossible"]
  E1 -- 예 --> EQ[sum=queryPathSum(A,B)] --> EP[print sum]
```

## 알고리즘 설계
- 핵심 연산
  - `makeRoot(x)`: `access(x)` 후 경로 뒤집기 플래그로 루트화
  - `connected(u,v)`: `findRoot(u) == findRoot(v)`
  - `link(u,v)`: `makeRoot(u)` 후 `findRoot(v) != u`이면 `parent[u]=v`로 연결
  - `setValue(x,val)`: `access(x)` 후 노드 값 교체 및 `pushUp`
  - `queryPathSum(u,v)`: `makeRoot(u)` → `access(v)` → `subtreeSum[v]`가 \(u\)에서 \(v\)까지 경로 합
- 집계 및 Lazy
  - 각 노드가 `nodeValue`(자기 값)과 `subtreeSum`(Splay 서브트리 합)을 가진다.
  - 경로 방향 반전을 위해 `reversed` 플래그를 두고, `toggleReverse`/`pushDown`에서 자식 스왑.
- 올바름 근거(스케치)
  - LCT의 `access`는 임의 노드까지의 경로를 우측 사슬로 만들어 경로 질의/갱신을 국소화한다.
  - `makeRoot(u)`로 트리의 루트가 \(u\)가 되면 `access(v)` 후 \(v\)의 Splay 서브트리 합이 정확히 \(u\to v\) 경로 합이 된다.
  - `bridge`는 다른 컴포넌트일 때만 수행되어 사이클이 생기지 않아 LCT 전제(포리스트)가 유지된다.

## 복잡도
- 각 연산(bridge/connected/setValue/queryPathSum)은 Splay 회전의 분할 상환으로 \(O(\log N)\).
- \(N \le 3\times 10^4\), \(Q \le 3\times 10^5\)에서도 충분히 통과.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct LinkCutTree {
    int n;
    vector<int> parent, leftChild, rightChild;
    vector<int> reversed;
    vector<long long> nodeValue, subtreeSum;

    LinkCutTree(int n = 0) { init(n); }

    void init(int n_) {
        n = n_;
        parent.assign(n + 1, 0);
        leftChild.assign(n + 1, 0);
        rightChild.assign(n + 1, 0);
        reversed.assign(n + 1, 0);
        nodeValue.assign(n + 1, 0);
        subtreeSum.assign(n + 1, 0);
    }

    bool isSplayRoot(int x) const {
        int p = parent[x];
        return p == 0 || (leftChild[p] != x && rightChild[p] != x);
    }

    void pushUp(int x) {
        subtreeSum[x] = subtreeSum[leftChild[x]] + subtreeSum[rightChild[x]] + nodeValue[x];
    }

    void toggleReverse(int x) {
        if (!x) return;
        swap(leftChild[x], rightChild[x]);
        reversed[x] ^= 1;
    }

    void pushDown(int x) {
        if (reversed[x]) {
            toggleReverse(leftChild[x]);
            toggleReverse(rightChild[x]);
            reversed[x] = 0;
        }
    }

    void rotate(int x) {
        int y = parent[x], z = parent[y];
        int isRight = (rightChild[y] == x);
        int b = isRight ? leftChild[x] : rightChild[x];

        if (!isSplayRoot(y)) {
            if (leftChild[z] == y) leftChild[z] = x;
            else if (rightChild[z] == y) rightChild[z] = x;
        }
        parent[x] = z;

        if (isRight) {
            leftChild[x] = y;
            rightChild[y] = b;
            if (b) parent[b] = y;
        } else {
            rightChild[x] = y;
            leftChild[y] = b;
            if (b) parent[b] = y;
        }
        parent[y] = x;

        pushUp(y);
        pushUp(x);
    }

    void splay(int x) {
        static vector<int> stk;
        stk.clear();
        int y = x;
        stk.push_back(y);
        while (!isSplayRoot(y)) {
            y = parent[y];
            stk.push_back(y);
        }
        while (!stk.empty()) {
            pushDown(stk.back());
            stk.pop_back();
        }
        while (!isSplayRoot(x)) {
            int y = parent[x], z = parent[y];
            if (!isSplayRoot(y)) {
                bool zigzig = (leftChild[z] == y) == (leftChild[y] == x);
                rotate(zigzig ? y : x);
            }
            rotate(x);
        }
        pushUp(x);
    }

    void access(int x) {
        int last = 0;
        for (int y = x; y; y = parent[y]) {
            splay(y);
            rightChild[y] = last;
            pushUp(y);
            last = y;
        }
        splay(x);
    }

    void makeRoot(int x) {
        access(x);
        toggleReverse(x);
    }

    int findRoot(int x) {
        access(x);
        while (leftChild[x]) {
            pushDown(x);
            x = leftChild[x];
        }
        splay(x);
        return x;
    }

    bool connected(int u, int v) {
        if (u == v) return true;
        return findRoot(u) == findRoot(v);
    }

    bool link(int u, int v) {
        makeRoot(u);
        if (findRoot(v) == u) return false; // already connected
        parent[u] = v;
        return true;
    }

    void setValue(int x, long long val) {
        access(x);
        nodeValue[x] = val;
        pushUp(x);
    }

    long long queryPathSum(int u, int v) {
        makeRoot(u);
        access(v);
        return subtreeSum[v];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    LinkCutTree lct(N);

    for (int i = 1; i <= N; i++) {
        long long a; cin >> a;
        lct.nodeValue[i] = a;
        lct.subtreeSum[i] = a;
    }

    int Q; cin >> Q;
    string op;
    for (int i = 0; i < Q; i++) {
        cin >> op;
        if (op[0] == 'b') { // bridge
            int A, B; cin >> A >> B;
            if (lct.connected(A, B)) {
                cout << "no\n";
            } else {
                lct.link(A, B);
                cout << "yes\n";
            }
        } else if (op[0] == 'p') { // penguins
            int A; long long X; cin >> A >> X;
            lct.setValue(A, X);
        } else { // excursion
            int A, B; cin >> A >> B;
            if (!lct.connected(A, B)) {
                cout << "impossible\n";
            } else {
                cout << lct.queryPathSum(A, B) << '\n';
            }
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `excursion A A` 처럼 동일 노드 경로(자기 자신 합) 처리
- `bridge`를 반복해도 이미 연결이면 반드시 "no" 출력
- `penguins`로 0/최대값(1000) 갱신
- 단일 노드, 서로 다른 트리에 대한 `excursion`은 "impossible"
- 큰 입력(Q=300k)에서도 입출력 최적화(`sync_with_stdio(false)`, `tie(nullptr)`) 적용

## 제출 전 점검
- 입출력 포맷/개행 확인
- 64-bit 누적 합 사용(`long long`)
- LCT 연산 순서: `makeRoot` → `access` → 집계 확인
- `connected` 확인 없이 `link`하지 않도록 주의

## 참고자료
- Sleator, Tarjan. Self-Adjusting Binary Search Trees (Splay Trees)
- Link-Cut Trees: Dynamic Trees supporting path queries

