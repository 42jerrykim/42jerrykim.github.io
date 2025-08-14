---
title: "[Algorithm] cpp 백준 8987번: 수족관 3 - 카르테시안 트리"
description: "수평 바닥을 구간 높이 배열로 모델링한 뒤, 최소 높이 기준으로 구간을 분할하는 카르테시안 트리를 구성해 각 노드 직사각형 넓이를 계산합니다. 분할로 얻는 이득을 우선순위 큐에 넣어 상위 K개를 합하면 최대 배수량을 얻습니다. 구현은 O(N)~O(N log N)으로 안정적이며, 64-bit 정수 오버플로와 구간 경계 처리, 입력 형식 차이 등을 면밀히 점검합니다."
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
- Problem-8987
- cpp
- C++
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Code Review
- 코드리뷰
- Template
- 템플릿
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Greedy
- 그리디
- Segment Tree
- 세그먼트 트리
- Cartesian Tree
- 카르테시안 트리
- Monotonic Stack
- 단조 스택
- DFS
- 우선순위 큐
- Priority Queue
- Divide and Conquer
- 분할정복
- Histogram
- 히스토그램
- Geometry
- 기하
- KOI
- 한국정보올림피아드
- KOI-2013
- 고등부
- Aquarium
- 수족관 3
- Range Minimum
- 구간 최소
- Postorder
- 후위순회
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/8987
- 요약: 수직·수평이 번갈아 나오는 바닥 다각형이 주어진다. 수평 선분 가운데에만 구멍을 뚫을 수 있고, K개의 구멍으로 배출되는 물의 양을 최대화하라. 물의 양은 면적과 동일하다.

## 입력/출력
```
<입력>
N
x1 y1
x2 y2
...
xN yN
K

<출력>
최대 배출량(정수)
```

## 접근 개요
- 핵심 관찰: 바닥의 수평 구간마다 높이가 일정하므로, 좌→우 구간 높이 배열 `h[i]`와 경계 `x[i]`로 표현 가능.
- 최소 높이에서 구간을 둘로 쪼개며 생기는 직사각형 넓이의 합을 계층적으로 더하면 전체 면적을 분해할 수 있음.
- 이 구조는 `h`에 대한 카르테시안 트리(열 값이 키, 중위 순회가 원래 순서)로 정확히 모델링됨.
- 각 노드에서 생성되는 넓이 = `(x[R+1]-x[L]) * (h[node]-h[parent])`. 서브트리에 대해 좌/우 최적을 선택하는 그리디가 성립하고, “분할의 덜 이득나는 쪽”을 후보로 남겨 K개를 고르면 된다.

```mermaid
flowchart TB
  A[수평 구간 높이 h, 경계 x 구성] --> B[카르테시안 트리(최소 힙 성질)]
  B --> C[후위 순회로 서브트리 구간 [L..R]과 사각형 넓이 계산]
  C --> D[왼/오른쪽 최대 이득 중 큰 값을 채택, 작은 값은 PQ에 보류]
  D --> E[루트 누적 이득을 PQ에 추가]
  E --> F[우선순위 큐에서 K개 pop하여 합산 = 최대 배수량]
```

## 알고리즘 설계
- 전처리
  - 입력 꼭짓점에서 수평 구간만 골라 `yH[]`, 경계 `xB[]`(크기 = |yH|+1)를 만든다.
  - `yH`에 대해 단조 스택으로 최소-카르테시안 트리를 O(N)에 구성한다.
- 후위 순회
  - 각 노드 `u`의 서브트리 인덱스 범위 `[LB[u], RB[u]]`를 계산하고, 직사각형 넓이 `rect[u] = (xB[RB+1]-xB[LB]) * (h[u]-h[parent])`를 더한다.
  - 왼쪽/오른쪽 서브트리의 최대 이득 `lval, rval` 중 큰 값을 현재 노드에 더하고, 작은 값 `min(lval, rval)`은 우선순위 큐에 넣는다.
- 마무리
  - 루트의 누적 이득 또한 PQ에 넣고, 상위 K개를 꺼내 합산한다.

## 복잡도
- 시간: 카르테시안 트리 구성 O(N), 후위 순회 O(N), PQ 연산 O(N log N) → 전체 O(N log N) 이내
- 공간: O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    vector<long long> vx(N), vy(N);
    for (int i = 0; i < N; ++i) cin >> vx[i] >> vy[i];
    int K; cin >> K;

    // 수평 구간 추출: yH[i]는 i번째 구간의 높이, xB는 경계(크기 = M+1)
    vector<long long> xB, yH;
    xB.reserve(N/2 + 2);
    yH.reserve(N/2 + 2);
    xB.push_back(vx[0]);
    for (int i = 0; i < N - 1; ++i) {
        if (vy[i] == vy[i + 1]) {
            yH.push_back(vy[i]);
            xB.push_back(vx[i + 1]);
        }
    }
    const int M = (int)yH.size();
    if (M == 0) { cout << 0 << '\n'; return 0; }

    // 최소 카르테시안 트리 구성
    vector<int> leftChild(M, -1), rightChild(M, -1), parent(M, -1);
    vector<int> st; st.reserve(M);
    for (int i = 0; i < M; ++i) {
        int last = -1;
        while (!st.empty() && yH[st.back()] > yH[i]) {
            last = st.back(); st.pop_back();
        }
        if (!st.empty()) {
            parent[i] = st.back();
            rightChild[st.back()] = i;
        }
        if (last != -1) {
            parent[last] = i;
            leftChild[i] = last;
        }
        st.push_back(i);
    }
    int root = -1;
    for (int i = 0; i < M; ++i) if (parent[i] == -1) { root = i; break; }

    // 후위 순회로 구간, 이득, PQ 구성
    vector<int> LB(M), RB(M);
    vector<long long> best(M, 0);
    priority_queue<long long> pq;

    vector<int> stk;
    stk.reserve(2*M + 5);
    stk.push_back(root);
    while (!stk.empty()) {
        int u = stk.back(); stk.pop_back();
        if (u >= 0) {
            stk.push_back(~u);
            if (rightChild[u] != -1) stk.push_back(rightChild[u]);
            if (leftChild[u] != -1) stk.push_back(leftChild[u]);
        } else {
            u = ~u;
            LB[u] = (leftChild[u] != -1 ? LB[leftChild[u]] : u);
            RB[u] = (rightChild[u] != -1 ? RB[rightChild[u]] : u);
            long long parentH = (parent[u] != -1 ? yH[parent[u]] : 0LL);
            long long width = xB[RB[u] + 1] - xB[LB[u]];
            long long rect = width * (yH[u] - parentH);
            long long lval = (leftChild[u] != -1 ? best[leftChild[u]] : 0LL);
            long long rval = (rightChild[u] != -1 ? best[rightChild[u]] : 0LL);
            best[u] = rect + max(lval, rval);
            pq.push(min(lval, rval));
        }
    }
    pq.push(best[root]);

    long long ans = 0;
    for (int i = 0; i < K && !pq.empty(); ++i) {
        ans += pq.top(); pq.pop();
    }
    cout << ans << '\n';
}
```

## 코너 케이스 체크리스트
- 모든 물이 빠지는 단순 바닥(단일 수평 구간)
- 단조 증가/감소/교차 형태의 높이 배열 `h`
- 동일 높이 인접 구간 처리(경계 `xB` 누락/중복 여부)
- 64-bit 곱 오버플로 방지(`long long` 유지)
- `K`가 후보 개수 이상일 때의 처리(빈 PQ 체크)

## 제출 전 점검
- 입출력 버퍼링 및 개행 형식 확인
- 경계 인덱스: 폭 계산은 `xB[RB+1] - xB[LB]`
- 부모 높이: 루트는 0으로 간주
- PQ: 각 노드에서 `min(left, right)`를 push, 루트 누적값 추가

## 참고자료/유사문제
- 카르테시안 트리 개요 및 히스토그램 분해 응용
- JusticeHui 블로그의 문제 해설(그리디 + 세그트리 + DFS 관점)


