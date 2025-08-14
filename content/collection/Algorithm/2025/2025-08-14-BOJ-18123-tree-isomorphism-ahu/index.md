---
title: "[Algorithm] cpp-python 백준 18123번: 평행우주"
description: "각 별자리는 s≤30의 트리로 주어집니다. 위상(동형)만을 비교하므로 번호를 무시하고 트리 중심에서 AHU 문자열 정규형을 만들어 대표값을 구한 뒤, 두 중심일 땐 사전순 최소를 택해 중복을 제거합니다. 서로 다른 정규형의 개수가 한 우주에 공존 가능한 별자리 최대 수가 됩니다. 전체 별 수 합 ≤1e6 조건에서 선형에 가깝게 처리되어 안전합니다."
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
- Problem-18123
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
- Tree
- 트리
- Graph
- 그래프
- Tree Isomorphism
- 트리 동형
- AHU
- AHU 인코딩
- Canonical Form
- 정규형
- Rooted Tree
- 루트 트리
- Unlabeled Tree
- 무라벨 트리
- Tree Center
- 트리 중심
- Centroid
- 센트로이드
- Encoding
- 문자열 인코딩
- String
- 문자열
- Hashing
- 해싱
- Unordered Set
- unordered_set
- DFS
- BFS
- Sorting
- 정렬
- Lexicographic
- 사전순
- Adjacency List
- 인접 리스트
- 입력 파싱
- 제한조건
- Correctness
- 올바름
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/18123
- 요약: 여러 평행우주의 별자리들이 트리로 주어지며, 두 별자리가 위치만 바꿔 얻어질 수 있으면 같은 위상(트리 동형)으로 본다. 같은 위상이 하나의 우주에 중복 존재할 수 없을 때, 우리 우주에서 동시에 존재 가능한 별자리의 최대 개수를 구한다.

### 제한/스펙
- 별자리 수 n: 1 ≤ n ≤ 1,000,000
- 각 별자리의 정점 수 s: 1 ≤ s ≤ 30, 모든 별의 총합 ≤ 1,000,000
- 무방향 트리, 정점 라벨(번호)은 위상 판단에서 무시
- 시간 제한 1초, 메모리 제한 1024MB

## 입력/출력 형식
```
입력
n
s
u v  (× s-1)
...
(위 과정을 n번 반복)

출력
서로 다른 위상의 개수(정수 1개)
```

### 예제
```
입력
3
4
0 1
1 2
2 3
4
0 2
2 3
3 1
4
0 1
1 2
1 3

출력
2
```
설명: 첫 번째와 두 번째 별자리는 같은 위상, 세 번째는 다른 위상 → 최대 2개 공존.

## 접근 개요
- 핵심 관찰: 별자리의 위상은 트리의 동형성 문제입니다. 정점 라벨을 무시하므로, 트리의 구조만 동일하면 같은 위상입니다.
- 표준 해법: 트리 중심(center)에서 루트를 잡고 AHU 인코딩으로 문자열 정규형을 생성합니다. 중심이 2개면 두 루트의 정규형 중 사전순 최소를 대표값으로 사용합니다.
- 전략: 모든 별자리에 대해 대표 문자열을 만들어 집합으로 모으고, 서로 다른 대표 문자열의 개수를 출력합니다.

## 알고리즘 설계
1) 각 별자리의 인접 리스트를 구성합니다.
2) 트리 중심을 구합니다(잎을 벗겨가며 1~2개가 남을 때까지). s ≤ 30이라 O(s)면 충분합니다.
3) 중심을 루트로 DFS 하여 자식 서브트리의 정규형을 재귀적으로 생성하고, 자식 코드들을 사전순 정렬해 괄호로 감싼 문자열을 반환합니다. 중심이 2개면 두 루트의 결과 중 작은 문자열을 선택합니다.
4) 대표 문자열을 해시 집합에 넣습니다.
5) 최종적으로 집합의 크기를 출력합니다.

### 올바름 근거(요지)
- AHU 인코딩은 무라벨 트리의 동형성 판정을 위한 정규형을 생성합니다. 두 트리가 동형이면 동일 문자열, 동형이 아니면 다른 문자열을 반환합니다.
- 중심에서 루팅하면 경로 길이 왜곡을 최소화하여 같은 비정규 루팅에서 달라질 수 있는 인코딩 충돌을 방지합니다. 중심이 2개인 경우 양쪽 루팅 중 사전순 최소를 택하면 대표가 유일합니다.

## 복잡도
- 각 별자리: O(s log d) 정도(자식 코드 정렬 비용). s ≤ 30이므로 상수에 가깝습니다.
- 전체: O(Σs) 수준에서 충분(총 정점 ≤ 1e6). 메모리도 O(Σs).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static string encode_rooted(int u, int parent, const vector<vector<int>>& adj) {
    vector<string> childCodes;
    childCodes.reserve(adj[u].size());
    for (int v : adj[u]) {
        if (v == parent) continue;
        childCodes.push_back(encode_rooted(v, u, adj));
    }
    sort(childCodes.begin(), childCodes.end());
    string res = "(";
    for (const string& s : childCodes) res += s;
    res += ")";
    return res;
}

static vector<int> find_centers(const vector<vector<int>>& adj) {
    int n = (int)adj.size();
    if (n == 1) return {0};
    vector<int> degree(n);
    queue<int> q;
    for (int i = 0; i < n; ++i) {
        degree[i] = (int)adj[i].size();
        if (degree[i] == 1) q.push(i);
    }
    int remaining = n;
    while (remaining > 2) {
        int sz = (int)q.size();
        remaining -= sz;
        while (sz--) {
            int u = q.front(); q.pop();
            degree[u] = 0;
            for (int v : adj[u]) {
                if (degree[v] > 0) {
                    if (--degree[v] == 1) q.push(v);
                }
            }
        }
    }
    vector<int> centers;
    for (int i = 0; i < n; ++i) if (degree[i] > 0) centers.push_back(i);
    if (centers.empty()) centers.push_back(q.front());
    return centers;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    unordered_set<string> shapes;
    shapes.reserve((size_t)min(1000000, n) * 2);

    for (int i = 0; i < n; ++i) {
        int s; cin >> s;
        vector<vector<int>> adj(s);
        for (int e = 0; e < s - 1; ++e) {
            int u, v; cin >> u >> v;
            adj[u].push_back(v);
            adj[v].push_back(u);
        }
        vector<int> centers = find_centers(adj);
        if (centers.size() == 1) {
            string code = encode_rooted(centers[0], -1, adj);
            shapes.insert(move(code));
        } else {
            string a = encode_rooted(centers[0], -1, adj);
            string b = encode_rooted(centers[1], -1, adj);
            if (a < b) shapes.insert(move(a));
            else shapes.insert(move(b));
        }
    }

    cout << shapes.size() << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from collections import deque
input = sys.stdin.readline

def find_centers(adj):
    n = len(adj)
    if n == 1:
        return [0]
    deg = [len(adj[i]) for i in range(n)]
    q = deque(i for i in range(n) if deg[i] == 1)
    remaining = n
    while remaining > 2:
        for _ in range(len(q)):
            u = q.popleft()
            remaining -= 1
            deg[u] = 0
            for v in adj[u]:
                if deg[v] > 0:
                    deg[v] -= 1
                    if deg[v] == 1:
                        q.append(v)
    return [i for i in range(n) if deg[i] > 0] or ([q[0]] if q else [0])

def encode_rooted(u, p, adj):
    children = []
    for v in adj[u]:
        if v == p:
            continue
        children.append(encode_rooted(v, u, adj))
    children.sort()
    return '(' + ''.join(children) + ')'

def main():
    data = input().split()
    if not data:
        return
    it = iter(data + sys.stdin.read().split())
    n = int(next(it))
    shapes = set()
    for _ in range(n):
        s = int(next(it))
        adj = [[] for _ in range(s)]
        for _ in range(s - 1):
            u = int(next(it)); v = int(next(it))
            adj[u].append(v); adj[v].append(u)
        centers = find_centers(adj)
        if len(centers) == 1:
            code = encode_rooted(centers[0], -1, adj)
        else:
            a = encode_rooted(centers[0], -1, adj)
            b = encode_rooted(centers[1], -1, adj)
            code = a if a < b else b
        shapes.add(code)
    print(len(shapes))

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- s=1(단일 정점 트리): 중심은 자기 자신, 인코딩은 "()"가 됩니다.
- 선형 사슬/별 모양 같이 극단적 구조: 중심 1~2개 정확히 탐지되는지 확인.
- 동일 구조지만 정점 번호만 다른 입력: 반드시 같은 정규형으로 수렴해야 합니다.
- 중심 2개인 짝수 지름 트리: 두 루팅 결과 중 사전순 최소를 대표로 사용.

## 제출 전 점검
- 입출력 버퍼링 및 빠른 입력 사용 여부 확인(C++의 `sync_with_stdio(false)`, Python의 `sys.stdin`).
- 재귀 깊이: s ≤ 30이므로 재귀 안전. 그래도 C++은 스택에 안전, Python도 충분.
- 해시 충돌: AHU는 문자열 정규형이라 충돌 없음. 다만 메모리 사용량을 고려해 `set`/`unordered_set` 적절 사용.
- 총합 1e6 입력 크기에서 전체 시간/메모리 예산 내 동작 확인.

## 참고자료
- AHU 트리 동형성(정규형) 기본 개념: `https://cp-algorithms.com/graph/tree_isomorphism.html`


