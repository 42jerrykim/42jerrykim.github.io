---
title: "[Algorithm] C++/Python 백준 13034번: 다각형 게임 - Sprague–Grundy DP"
description: "볼록 다각형에서 선분을 서로 교차시키지 않고 기존 선분의 끝점과도 겹치지 않게 잇는 게임을 스프라그–그런디 정리로 모델링합니다. 한 번의 선택이 다각형을 두 부분으로 분할한다는 불변식에서 g[n]=mex{g[a]⊕g[n-2-a]}를 세우고, O(N^2) DP로 승패(1/2)를 판정합니다. 엣지/실수 포인트 점검 포함."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Game Theory
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- C++
- Python
- Implementation
- 구현
- Time-Complexity
- 시간복잡도
- Space-Complexity
- 공간복잡도
- Edge-Cases
- 엣지케이스
- Pitfalls
- 함정
- Optimization
- 최적화
- Competitive-Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Code-Review
- 코드리뷰
- Testing
- 테스트
- Complexity-Analysis
- 복잡도분석
- Greedy
- 그리디
- Dynamic-Programming
- 동적계획법
- Graph
- 그래프
- Tree
- 트리
- BFS
- DFS
- Shortest-Path
- 최단경로
- Dijkstra
- Bellman-Ford
- Floyd-Warshall
- Topological-Sort
- 위상정렬
- Segment-Tree
- 세그먼트트리
- Fenwick-Tree
- Disjoint-Set
- Binary-Search
- 이분탐색
- Two-Pointers
- Sliding-Window
- Hashing
- 해싱
- String
- 문자열
- Geometry
- Math
- 수학
- Modular-Arithmetic
- 모듈러
- Debugging
- 디버깅
- Game-Theory
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13034
- 요약: N개의 꼭짓점을 가진 볼록 다각형에서, 두 꼭짓점을 골라 선분을 긋되 기존 선분과 교차하거나 끝점이 겹치면 안 됩니다. 더 이상 그을 수 없는 사람이 패배합니다. 선공(성관)과 후공(홍준)이 최적으로 플레이할 때 승자를 구합니다.

## 입력/출력
- 입력: 한 줄에 정수 N (3 ≤ N ≤ 1000)
- 출력: 선공이 이기면 1, 후공이 이기면 2

예시
```
입력
3

출력
1
```
```
입력
4

출력
1
```
```
입력
15

출력
2
```
```
입력
191

출력
2
```

## 접근 개요
- 핵심 관찰: 한 번의 선분 선택은 다각형을 두 부분으로 분할합니다. 그리고 선택된 두 꼭짓점은 이후 어떤 선분의 끝점으로도 사용할 수 없습니다. 즉, 각 부분 문제에서는 그 구간 내부의 꼭짓점들만 사용 가능합니다.
- 불변식: 양쪽 부분 문제는 서로 독립인 임partial game이므로, 전체 그런디 수는 두 부분 그런디 수의 XOR 입니다.
- 전이식: 양 끝점을 제외한 한쪽 구간 내부 꼭짓점 수를 a (0 ≤ a ≤ n-2)라 하면, 다른 쪽은 b = n-2-a이고, 그런디는
  - \( g[n] = \mathrm{mex}\{\, g[a] \oplus g[b] \mid a=0..n-2,\ b=n-2-a \,\} \)
- 기저: \(g[0]=g[1]=0\) (더 이상 그을 수 없는 상태)

### 전이 흐름도 (Mermaid)
```mermaid
flowchart TD
  A[현재 꼭짓점 수 n] --> B{a = 0..n-2}
  B --> C[g[a] XOR g[n-2-a]]
  C --> D[값들 집합]
  D --> E[mex 집합 = g[n]]
```

## 알고리즘
- DP로 0..N까지의 그런디 수를 누적 계산
  - seen 배열에 가능한 \(g[a]\oplus g[b]\)를 표시한 뒤 mex를 취함
- 최종 \(g[N] > 0\)이면 선공이 이김(1), 아니면 후공(2)

## 복잡도
- 시간: \(O(N^2)\) — 각 n마다 a를 0..n-2 순회
- 공간: \(O(N)\) — 그런디 테이블 저장

## 구현 (C++)
```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
#include <bits/stdc++.h>
using namespace std;

int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
    int N; if(!(cin>>N)) return 0;
    vector<int> g(N+1,0);
    if(N>=0) g[0]=0; if(N>=1) g[1]=0;
    for(int n=2;n<=N;++n){
        vector<char> seen(n+5,0);
        for(int a=0;a<=n-2;++a){
            int b=n-2-a;
            int val=g[a]^g[b];
            if(val<(int)seen.size()) seen[val]=1;
        }
        int mex=0; while(mex<(int)seen.size() && seen[mex]) ++mex;
        g[n]=mex;
    }
    cout<<(g[N]?1:2) << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    g = [0]*(N+1)
    if N >= 1:
        g[1] = 0
    for n in range(2, N+1):
        seen = [False]*(n+5)
        for a in range(0, n-1):
            b = n-2-a
            val = g[a]^g[b]
            if val < len(seen):
                seen[val] = True
        mex = 0
        while mex < len(seen) and seen[mex]:
            mex += 1
        g[n] = mex
    print(1 if g[N] else 2)

if __name__ == "__main__":
    solve()
```

## 정당성 스케치
- 독립합 원리: 선택한 선분이 두 부분을 만들고, 이후 각 부분 내에서만 선택이 가능하므로 게임은 두 서브게임의 합입니다.
- 이런 임partial game은 스프라그–그런디 정리에 의해 전체 그런디 = 부분 그런디 XOR가 되어 전이식이 성립합니다.
- 기저 상태(0,1)에서는 어떤 선분도 추가할 수 없으므로 그런디가 0인 무승부(패배) 상태입니다.

## 코너 케이스 체크리스트
- N=3,4 같은 최소값에서 전이가 올바르게 작동하는지
- 매우 큰 N(최대 1000)에서 시간/공간 초과 없는지
- a=0 또는 a=n-2 처럼 한쪽이 비는 경우 처리
- 입력 개행/공백 처리, 출력 형식(개행) 확인

## 제출 전 점검
- 입출력 형식, 개행, 초기화 및 배열 범위 점검
- 그런디 기저값(g[0], g[1]) 확인
- a 순회 범위 0..n-2 확인, XOR/mex 구현

## 참고
- Sprague–Grundy theorem, impartial games 기초 자료

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **최소 입력** | N=1 또는 빈 입력 | 반복문 범위·예외 처리 확인 |
| **오버플로우** | 답이 $2^{31}$ 초과 가능 | `long long` (C++) 등 사용 |
