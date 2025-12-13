---
title: "[Algorithm] C++/Python 백준 16901번: XOR MST"
description: "XOR 가중치 완전그래프의 MST를 비트 최상위부터 그룹을 나누는 분할정복과 이분 트라이로 계산합니다. 각 레벨에서 교차 간선 비용을 2^b + 하위 최소 XOR로 구해 전체 비용을 누적합니다. 구현 포인트와 코너 케이스, C++·Python 코드와 정당성 근거까지 정리했습니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Graph
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16901
- cpp
- python
- C++
- Python
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
- Dynamic Programming
- 동적계획법
- Graph
- 그래프
- Tree
- 트리
- BFS
- DFS
- Shortest Path
- 최단경로
- Dijkstra
- 다익스트라
- Segment Tree
- 세그먼트 트리
- Fenwick Tree
- 펜윅트리
- Disjoint Set Union
- 유니온파인드
- Binary Search
- 이분탐색
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Hashing
- 해싱
- String
- 문자열
- Geometry
- 기하
- Math
- 수학
- Modulo
- 모듈러
- Debugging
- 디버깅
- Bitwise
- 비트연산
- XOR
- XOR MST
- Minimum Spanning Tree
- 최소스패닝트리
- Divide and Conquer
- 분할정복
- Trie
- 트라이
- Binary Trie
- 이분트라이
- MST
- Prim
- Kruskal
- Bit DP
- 비트DP
- O(N log A)
- Logarithmic
- 로그복잡도
- Data Structures
- 자료구조
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16901
- 요약: 정점 i에 값 A_i가 적힌 무방향 완전그래프에서 간선 가중치가 A_i xor A_j일 때, MST의 총 비용을 구한다.

### 제한/스펙
- 1 ≤ N ≤ 200,000
- 0 ≤ A_i < 2^30
- 시간 제한 2초, 메모리 제한 512MB

## 입력/출력
```
입력
N
A_1 A_2 ... A_N

출력
MST 비용
```

### 예제 1
```
입력
5
1 2 3 4 5

출력
8
```

### 예제 2
```
입력
4
1 2 3 4

출력
8
```

## 접근 개요(아이디어 스케치)
- 핵심 관찰: 최상위 비트 b에서 A를 두 그룹(해당 비트 0/1)으로 나누면, 서로 다른 그룹을 잇는 모든 간선은 최소 2^b의 비용을 갖는다. 교차 간선의 실제 비용은 2^b + (하위 비트 XOR 최소값)이다.
- 전략: 비트 b=29→0 순으로 분할정복. 각 단계에서 좌/우 그룹 내부 MST 비용을 재귀로 계산하고, 두 그룹을 잇는 최소 교차 간선 비용을 더한다.
- 하위 비트 최소 XOR는 한쪽 그룹을 이분 트라이에 넣고, 다른 쪽 그룹을 질의해 O(size·b)로 구한다.

## 알고리즘 설계
1) 함수 solve(S, b): 집합 S와 비트 b에 대해
   - b<0 또는 |S|≤1이면 0 반환
   - S를 b번째 비트 기준으로 L(0), R(1)로 분할
   - res = solve(L, b-1) + solve(R, b-1)
   - L, R가 모두 비지 않으면 교차 간선 비용 추가
     - lower = b-1에 대해 한쪽을 트라이에 삽입, 다른 쪽을 질의해 하위 XOR 최소값 minLower 산출
     - res += 2^b + (lower<0이면 0, 아니면 minLower)
2) 정당성: 각 레벨에서 L/R 내부의 간선은 상위비트가 동일해 2^b를 추가하지 않는다. 서로 다른 그룹을 연결하는 최소 간선은 반드시 2^b를 포함하며, 그 중 하위 비트 XOR가 최소인 간선이 MST에 들어간다. 분할정복으로 모든 상위비트에 대해 국소 최적(최소 교차 간선)을 선택해도, 각 레벨 간 간섭이 없어 전역 최적(MST)을 이룬다.

## 복잡도
- 시간: O(N · log A_max) 수준. 각 원소가 각 비트 레벨에서 한 번씩 트라이 삽입/질의를 수행.
- 공간: O(N · log A_max)까지(트라이 노드 수 상한). 구현 상 상수는 작다.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const int MAX_BIT = 29;

struct BinaryTrie {
    struct Node { int next[2]; Node(){ next[0] = next[1] = -1; } };
    vector<Node> nodes;
    BinaryTrie(){ nodes.reserve(1); nodes.push_back(Node()); }

    void insert(int value, int maxBit) {
        int cur = 0;
        for (int b = maxBit; b >= 0; --b) {
            int bit = (value >> b) & 1;
            if (nodes[cur].next[bit] == -1) {
                nodes[cur].next[bit] = (int)nodes.size();
                nodes.push_back(Node());
            }
            cur = nodes[cur].next[bit];
        }
    }

    int queryMinXor(int value, int maxBit) const {
        int cur = 0, cost = 0;
        for (int b = maxBit; b >= 0; --b) {
            int bit = (value >> b) & 1;
            int prefer = bit; // 동일 비트를 우선해 XOR 최소화 시도
            int nxt = nodes[cur].next[prefer];
            if (nxt == -1) {
                prefer ^= 1;
                nxt = nodes[cur].next[prefer];
                cost |= (1 << b);
            }
            cur = nxt;
        }
        return cost;
    }
};

long long solveMSTCost(vector<int> &a, int bit) {
    if (bit < 0 || a.size() <= 1) return 0;

    vector<int> leftGroup, rightGroup;
    leftGroup.reserve(a.size());
    rightGroup.reserve(a.size());
    for (int x : a) {
        if ((x >> bit) & 1) rightGroup.push_back(x);
        else leftGroup.push_back(x);
    }

    long long res = 0;
    if (!leftGroup.empty())  res += solveMSTCost(leftGroup, bit - 1);
    if (!rightGroup.empty()) res += solveMSTCost(rightGroup, bit - 1);

    if (!leftGroup.empty() && !rightGroup.empty()) {
        int lowerMaxBit = bit - 1;
        if (lowerMaxBit < 0) {
            res += (1LL << bit);
        } else {
            BinaryTrie trie;
            trie.nodes.reserve((int)rightGroup.size() * (lowerMaxBit + 1) / 2 + 1);
            for (int y : rightGroup) trie.insert(y, lowerMaxBit);

            int bestLower = INT_MAX;
            for (int x : leftGroup)
                bestLower = min(bestLower, trie.queryMinXor(x, lowerMaxBit));

            res += (1LL << bit) + bestLower;
        }
    }
    return res;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; 
    if (!(cin >> N)) return 0;
    vector<int> A(N);
    for (int i = 0; i < N; ++i) cin >> A[i];

    cout << solveMSTCost(A, MAX_BIT) << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

MAX_BIT = 29

class BinaryTrie:
    __slots__ = ("nxt",)
    def __init__(self):
        # nxt: list of [child0, child1]
        self.nxt = [[-1, -1]]

    def insert(self, value: int, max_bit: int) -> None:
        cur = 0
        for b in range(max_bit, -1, -1):
            bit = (value >> b) & 1
            if self.nxt[cur][bit] == -1:
                self.nxt[cur][bit] = len(self.nxt)
                self.nxt.append([-1, -1])
            cur = self.nxt[cur][bit]

    def query_min_xor(self, value: int, max_bit: int) -> int:
        cur = 0
        cost = 0
        for b in range(max_bit, -1, -1):
            bit = (value >> b) & 1
            prefer = bit
            nxt = self.nxt[cur][prefer]
            if nxt == -1:
                prefer ^= 1
                nxt = self.nxt[cur][prefer]
                cost |= (1 << b)
            cur = nxt
        return cost

def solve_group(arr, bit):
    if bit < 0 or len(arr) <= 1:
        return 0
    left, right = [], []
    for x in arr:
        if (x >> bit) & 1:
            right.append(x)
        else:
            left.append(x)

    res = 0
    if left:
        res += solve_group(left, bit - 1)
    if right:
        res += solve_group(right, bit - 1)

    if left and right:
        lower_bit = bit - 1
        if lower_bit < 0:
            res += (1 << bit)
        else:
            trie = BinaryTrie()
            for y in right:
                trie.insert(y, lower_bit)
            best_lower = 1 << 30
            for x in left:
                best_lower = min(best_lower, trie.query_min_xor(x, lower_bit))
            res += (1 << bit) + best_lower
    return res

def main():
    N = int(input().strip())
    A = list(map(int, input().split()))
    print(solve_group(A, MAX_BIT))

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- 모든 수가 동일할 때: 모든 XOR=0, 답은 0.
- N=1: 간선 없음, 답 0.
- 값이 0 또는 2^k 경계값(단일 비트만 1)들: 상위비트 분할 정확성 확인.
- 중복 원소 다수: 트라이 질의/삽입 시 성능과 올바름 유지.
- 매우 큰 N에서 입력이 한 줄로 주어지는 경우: 입출력 최적화(ios::sync_with_stdio, fast IO) 사용.

## 제출 전 점검
- 입출력 개행/공백 처리 확인
- 64-bit 정수 사용(C++에서 누적 합 long long)
- 분할정복 종료 조건(bit<0, |S|≤1) 확인
- 트라이 질의 시 없는 방향으로만 갔을 때 비용 비트 추가 로직 확인

## 참고자료/유사문제
- 비트 기반 분할정복 + 이분 트라이로 XOR MST 계산하는 고전 아이디어 정리 글들
- Minimum XOR Pair, XOR Basis 등 비트/트라이 응용 문제들


