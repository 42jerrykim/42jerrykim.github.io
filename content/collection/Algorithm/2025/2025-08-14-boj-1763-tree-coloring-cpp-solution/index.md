---
title: "[Algorithm] C++ 백준 1763번: 트리 색칠 - 비율 그리디"
description: "부모 선행 제약 아래 비용 C[i]·F[i]를 최소화하기 위해, 누적가중치/누적크기 비율이 최대인 정점을 고르고 가장 가까운 미방문 조상으로 병합하는 그리디를 적용합니다. 교차곱 비교와 경로 압축으로 정확·빠르게 구현합니다."
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
- Problem-1763
- cpp
- C++
- Tree
- 트리
- Greedy
- 그리디
- Disjoint Set Union
- 유니온파인드
- Union-Find
- DSU
- Merging
- 병합
- Ratio
- 비율
- Average Weight
- 평균 가중치
- Sorting
- 정렬
- Topological Order
- 위상정렬
- Parent Compression
- 조상 압축
- Path Compression
- 경로 압축
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Complexity Analysis
- 복잡도 분석
- Proof of Correctness
- 정당성 증명
- Correctness
- 올바름
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
- Testing
- 테스트
- Simulation
- 시뮬레이션
- Priority Queue
- 우선순위 큐
- Greedy Choice
- 그리디 선택
- Exchange Argument
- 교환 논증
- Tree Coloring
- 트리 색칠
- Parent First
- 부모 선행
- Ordering
- 순서
- Integer Arithmetic
- 정수 연산
- __int128
- 오버플로 방지
- BFS/DFS
- 그래프
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/1763
- 요약: 루트가 있는 트리에서 노드 i를 F[i]번째로 색칠하면 비용이 C[i]·F[i]. 부모가 먼저 색칠되어야 하며(루트 선행), 전체 비용 합을 최소화하는 색칠 순서를 구한다.
- 제한/스펙: N ≤ 1000, 1 ≤ R ≤ N. 간선은 부모 U, 자식 V가 직접 주어진다.

## 입력/출력
예제 1
```
입력
5 1
1 2 1 2 4
1 2
1 3
2 4
3 5

출력
33
```

## 접근 개요
- 핵심 관찰: 어떤 노드의 서브트리를 하나의 블록으로 봤을 때, 블록의 현재 누적가중치(sum)와 누적크기(size)를 유지하면, 두 블록 A,B를 부모 쪽으로 올려 쌓는 순서를 바꿔도 비용 차이는 (sumA/sizeA)와 (sumB/sizeB)의 비교로 결정된다. 비율이 큰 블록을 먼저 올릴수록 전체 비용이 감소한다.
- 그리디 전략: 매 단계 방문되지 않은 정점들 중 비율 sum/size가 최대인 정점 x를 고르고, 아직 방문 전인 가장 가까운 조상 dad로 병합한다. 비용은 sum[x]·size[dad]만큼 증가한다. 병합 후 dad의 (sum,size)에 x의 값을 누적한다.
- 구현 포인트: 비율 비교는 부동소수점 오차를 피하기 위해 교차곱(sumA·sizeB vs sumB·sizeA)을 정수로 비교하고, 조상 찾기는 “아직 색칠 전인 가장 가까운 조상”으로 경로 압축해 가속한다.

## 알고리즘
1) 입력으로 부모-자식이 직접 주어지므로 `parent[v]=u` 배열을 구성하고, 루트 R에 대해서는 `parent[R]=R`로 둔다.
2) 각 정점은 독립 블록으로 시작: `sum[i]=C[i]`, `size[i]=1`, `visited[i]=false`.
3) N-1회 반복(루트를 제외한 모든 정점을 한 번씩 병합):
   - 비방문 정점 i(루트 제외) 중에서 `sum[i]/size[i]` 비율이 최대인 `best`를 선출.
   - `dad = findNearestUnvisitedAncestor(parent[best])`를 구해 비용 `ans += sum[best] * size[dad]`를 더한 뒤, `dad` 블록에 `best`를 병합: `sum[dad]+=sum[best]`, `size[dad]+=size[best]`, `visited[best]=true`.
   - `findNearestUnvisitedAncestor`는 “이미 병합 끝난 정점은 부모로 건너뛰는” 경로 압축으로 구현.
4) 마지막으로 루트 블록 자체를 색칠하는 비용 `+ sum[R]`를 더한다.

### 올바름(스케치)
- 두 블록 A,B를 쌓는 순서 비교에서 비용 차이는 (sumA/sizeA) ≥ (sumB/sizeB)일 때 A를 먼저 배치하는 편이 손해가 없다(교환 논증). 이 국소 최적 선택을 전체 과정에 반복 적용하면 전역 최적 순서를 얻는다.
- 부모 선행 제약은 “아직 방문 전인 가장 가까운 조상으로만 병합” 규칙으로 보존되며, 한 번 병합된 블록은 더 큰 블록으로만 커져 비율 비교의 일관성이 유지된다.

## 복잡도
- 매 단계 O(N) 선출 × (N-1) 단계 = O(N^2). N ≤ 1000이므로 충분히 통과한다. 추가 메모리 O(N).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, R;
    if (!(cin >> N >> R)) return 0;

    vector<long long> weight(N + 1);
    for (int i = 1; i <= N; ++i) cin >> weight[i];

    vector<int> parent(N + 1, 0);
    for (int i = 0; i < N - 1; ++i) {
        int U, V; // U is parent of V
        cin >> U >> V;
        parent[V] = U;
    }
    parent[R] = R;

    vector<long long> groupWeight = weight; // 누적 가중치
    vector<int> groupSize(N + 1, 1);        // 누적 크기
    vector<char> visited(N + 1, 0);         // 병합 완료 표시

    function<int(int)> findNearestUnvisitedAncestor = [&](int x) -> int {
        if (!visited[x]) return x;
        return parent[x] = findNearestUnvisitedAncestor(parent[x]);
    };

    long long answer = 0;

    // N-1번: 루트를 제외한 모든 정점을 한 번씩 선택해 위로 병합
    for (int step = 0; step < N - 1; ++step) {
        int best = -1;
        for (int i = 1; i <= N; ++i) {
            if (i == R || visited[i]) continue;
            if (best == -1) {
                best = i;
            } else {
                // 최대 ratio: groupWeight[i] / groupSize[i]
                __int128 lhs = (__int128)groupWeight[i] * groupSize[best];
                __int128 rhs = (__int128)groupWeight[best] * groupSize[i];
                if (lhs > rhs) best = i;
            }
        }

        int dad = findNearestUnvisitedAncestor(parent[best]);
        visited[best] = 1;

        // 이번에 best 블록을 dad 위로 올려 쌓으면서 발생하는 비용
        answer += groupWeight[best] * (long long)groupSize[dad];

        // dad 블록에 병합
        groupWeight[dad] += groupWeight[best];
        groupSize[dad] += groupSize[best];
        parent[best] = dad; // 경로 압축 일관성
    }

    // 마지막에 루트가 칠해질 때 드는 비용
    answer += groupWeight[R];

    cout << answer << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- N=1(간선 없음): 답은 C[R].
- 체인/스타 등 편향 트리: 비율 선출·조상 병합이 여전히 올바르게 동작.
- 큰 가중치: 교차곱 비교에 `__int128`을 사용해 오버플로를 회피.
- 입력 간선이 부모→자식으로 직접 주어지므로 별도 루트 탐색/방향 정리는 불필요.

## 참고자료
- Beijing Regional 2004 F. BOJ 1763 “트리 색칠”.
- 관련 아이디어: 비율 그리디·교환 논증, 조상 경로 압축.


