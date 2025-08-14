---
title: "[Algorithm] cpp-python 백준 8202번: Conspiracy (스플릿 그래프)"
description: "POI 2010/2011 ‘Conspiracy’를 스플릿 그래프 인식 정리로 해결합니다. Hammer–Simeone 차수 조건으로 분할 가능 여부를 판정하고, 기준 분할에서 단일 이동과 교환 스왑 규칙으로 모든 유효 분할 수를 O(n^2)로 계산합니다. 엣지·완전 그래프 등 코너 케이스와 정당성 근거, 구현 포인트까지 제공합니다."
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
- Problem-8202
- cpp
- python
- Graph
- 그래프
- Split Graph
- 스플릿 그래프
- Split Graph Recognition
- 스플릿 그래프 판정
- Hammer–Simeone
- Degree Sequence
- 차수열
- Clique
- 클리크
- Independent Set
- 독립집합
- Partition Counting
- 분할 개수
- POI
- Polish Olympiad in Informatics
- Conspiracy
- 음모
- Bitset
- 비트셋
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Proof of Correctness
- 정당성 증명
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- O(n^2)
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Greedy
- 그리디
- Dynamic Programming
- 동적계획법
- Graph Theory
- 그래프 이론
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
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/8202
- 요약: n명의 사람을 두 그룹으로 나눈다. 지원조는 서로 모두 알고 있어야 하고(클리크), 공모자는 서로 전혀 몰라야 한다(독립집합). 두 그룹은 모두 비어 있으면 안 된다. 가능한 분할의 수를 구하라.
- 제한: n ≤ 5,000, 인접 정보는 대칭으로 주어진다.

## 입력/출력
```
입력: 
- 첫 줄에 n (2 ≤ n ≤ 5,000)
- 다음 n줄: i번째 줄에 k_i 와 i의 지인 목록 a_{i,1}, ..., a_{i,k_i} (오름차순)
출력:
- 조건을 만족하는 분할의 총 개수. 없으면 0
```

예시
```
입력
4
2 2 3
2 1 3
3 1 2 4
1 3

출력
3
```

## 접근 개요
- 핵심 관찰: 조건을 만족하는 그래프는 꼭짓점을 클리크 K와 독립집합 S로 나눌 수 있는 스플릿 그래프이다.
- 판정: Hammer–Simeone 차수 조건으로 스플릿 그래프 여부를 O(n log n) + O(n)로 판정한다.
- 카운팅: 차수 내림차순으로 만든 기준 분할(K|S)에서
  - 단일 이동: K의 꼭짓점 x가 S와 인접 0이면 x를 S로 이동 가능, S의 y가 K의 모든 꼭짓점과 인접이면 y를 K로 이동 가능(단, 각 군집이 비지 않도록 크기 조건 확인).
  - 교환 스왑: x∈K, y∈S에 대해 y는 K\{x}의 모든 꼭짓점과 인접, x는 S\{y}의 모든 꼭짓점과 비인접이면 (x↔y) 스왑이 가능.
- 전체 경우의 수 = 기준 분할(양쪽 비공백일 때만 1) + 단일 이동 수 + 모든 가능한 (x,y) 스왑 수.

```mermaid
flowchart TD
  A[차수 내림차순 정렬] --> B[k = max { i | d_i ≥ i-1 }]
  B --> C{∑_{i≤k} d_i = k(k-1)+∑_{i>k} min(d_i,k)?}
  C -- No --> Z[정답 0]
  C -- Yes --> D[기준 분할 K|S 구성]
  D --> E[단일 이동 카운트]
  D --> F[교환 스왑 카운트]
  E --> G[합산]
  F --> G[정답]
```

## 알고리즘
1) 인접 비트셋 구성: 각 정점 i에 대해 adj[i] 비트셋으로 이웃 관리(메모리 효율/빠른 popcount).
2) 차수열 정렬: d를 내림차순 정렬하고 k = max{i | d_i ≥ i-1} 계산.
3) Hammer–Simeone 체크: ∑_{i≤k} d_i 가 k(k-1)+∑_{i>k} min(d_i,k) 와 같지 않으면 스플릿 그래프가 아니므로 0.
4) 기준 분할: 정렬 기준 상위 k개를 K, 나머지를 S로 둔다.
5) 단일 이동 조건:
   - x∈K가 S의 어떤 정점과도 인접하지 않으면 x를 S로 이동 가능(K 크기 ≥ 2일 때만 집합 비공백 유지).
   - y∈S가 K의 모든 정점과 인접하면 y를 K로 이동 가능(S 크기 ≥ 2 조건).
6) 교환 스왑 조건(x∈K, y∈S):
   - y의 K 내 비인접 개수 ≤ 1, x의 S 내 인접 개수 ≤ 1이며,
   - (y의 유일 비인접이 존재한다면 그 정점이 x), (x의 유일 인접이 존재한다면 그 정점이 y).
7) 위 세 항을 합산하면 답.

## 정당성(스케치)
- Hammer–Simeone 정리: 차수 내림차순에서 정의한 k에 대해 ∑_{i≤k} d_i = k(k-1)+∑_{i>k} min(d_i,k) 가 성립할 필요충분조건으로 그래프가 스플릿 그래프임을 보장.
- 기준 분할 K|S는 위 정리로 유도된 ‘정규(split) 분해’ 중 하나이며, 추가 가능한 분해는 오직 (i) S와 간선이 없는 K의 정점 이동, (ii) K에 모두 인접한 S의 정점 이동, (iii) 그 조합인 (x,y) 스왑으로만 생성됨을 확인할 수 있다.
- 스왑 조건은 K의 완전성과 S의 독립성을 동시에 유지하기 위한 필요충분 조건으로 구성되어 중복 없이 모든 분해를 세게 된다.

## 복잡도
- 시간: O(n^2) — 비트셋 기반 인접 검사/집계(popcount)와 단순 카운팅
- 공간: O(n^2) 비트(인접 비트셋), 보조 배열 O(n)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const int MAXN = 5005;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; if(!(cin >> n)) return 0;
    vector<bitset<MAXN>> adj(n);

    for(int i=0;i<n;++i){
        int k; cin >> k;
        for(int t=0;t<k;++t){
            int a; cin >> a; int j = a-1;
            if(j<0||j>=n||j==i) continue;
            adj[i].set(j);
            adj[j].set(i);
        }
    }

    vector<int> degree(n);
    for(int i=0;i<n;++i) degree[i] = (int)adj[i].count();

    vector<int> order(n); iota(order.begin(), order.end(), 0);
    sort(order.begin(), order.end(), [&](int a, int b){
        if(degree[a] != degree[b]) return degree[a] > degree[b];
        return a < b;
    });

    vector<int> ds(n+1,0);
    for(int i=1;i<=n;++i) ds[i] = degree[order[i-1]];
    int k = 0; for(int i=1;i<=n;++i) if(ds[i] >= i-1) k = i;

    long long sumTop = 0, rhs = 1LL*k*(k-1);
    for(int i=1;i<=k;++i) sumTop += ds[i];
    for(int i=k+1;i<=n;++i) rhs += min(ds[i], k);

    if(sumTop != rhs){ cout << 0 << '\n'; return 0; }

    vector<int> Klist, Slist; Klist.reserve(k); Slist.reserve(n-k);
    vector<char> inK(n, 0);
    for(int i=0;i<k;++i){ inK[order[i]] = 1; Klist.push_back(order[i]); }
    for(int i=k;i<n;++i) Slist.push_back(order[i]);

    int Ksize = (int)Klist.size();
    int Ssize = (int)Slist.size();

    long long answer = 0;
    if(Ksize>0 && Ssize>0) answer += 1; // 기준 분할

    // K -> S 단일 이동 후보 카운트
    vector<int> sNeighborCount(n, 0);
    vector<int> soleSNeighbor(n, -1);
    vector<int> countXSingles(n, 0);
    int Xcount = 0; // x in K with zero neighbors in S

    for(int x: Klist){
        int cnt = 0, yfound = -1;
        for(int y: Slist){
            if(adj[x].test(y)){
                ++cnt;
                if(cnt==1) yfound = y; else break;
            }
        }
        sNeighborCount[x] = cnt;
        if(cnt==0) ++Xcount;
        else if(cnt==1){ soleSNeighbor[x] = yfound; ++countXSingles[yfound]; }
    }

    // S -> K 단일 이동 후보 카운트
    vector<int> nonNeighborKCount(n, 2);
    vector<int> soleKNonNeighbor(n, -1);
    int Ycount = 0; // y in S adjacent to all K

    for(int y: Slist){
        int cnt = 0, xnon = -1;
        for(int x: Klist){
            if(!adj[y].test(x)){
                ++cnt; if(cnt==1) xnon = x; else break;
            }
        }
        if(cnt==0){ nonNeighborKCount[y]=0; ++Ycount; }
        else if(cnt==1){ nonNeighborKCount[y]=1; soleKNonNeighbor[y]=xnon; }
        else nonNeighborKCount[y]=2;
    }

    if(Ksize>=2) answer += Xcount;
    if(Ssize>=2) answer += Ycount;

    long long pairs = 0;
    for(int y: Slist){
        int nk = nonNeighborKCount[y];
        if(nk==0){
            pairs += Xcount; // x with 0 S-neighbors
            pairs += countXSingles[y]; // x whose sole S-neighbor is y
        }else if(nk==1){
            int x0 = soleKNonNeighbor[y];
            if(sNeighborCount[x0]==0) ++pairs;
            else if(sNeighborCount[x0]==1 && soleSNeighbor[x0]==y) ++pairs;
        }
    }
    answer += pairs;

    cout << answer << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys

def solve():
    input = sys.stdin.readline
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    # 비트셋을 파이썬 int로 표현 (0..n-1 비트 사용)
    adj = [0] * n
    for i in range(n):
        parts = list(map(int, input().split()))
        if not parts:
            parts = [0]
        k = parts[0]
        for a in parts[1:]:
            j = a - 1
            if 0 <= j < n and j != i:
                adj[i] |= (1 << j)
                adj[j] |= (1 << i)

    degree = [adj[i].bit_count() for i in range(n)]

    order = list(range(n))
    order.sort(key=lambda x: (-degree[x], x))

    ds = [0] * (n + 1)
    for i in range(1, n + 1):
        ds[i] = degree[order[i - 1]]

    k = 0
    for i in range(1, n + 1):
        if ds[i] >= i - 1:
            k = i

    sum_top = sum(ds[1 : k + 1])
    rhs = k * (k - 1)
    for i in range(k + 1, n + 1):
        rhs += min(ds[i], k)

    if sum_top != rhs:
        print(0)
        return

    Klist = order[:k]
    Slist = order[k:]
    Ksize = len(Klist)
    Ssize = len(Slist)

    # 마스크들
    mask_all = (1 << n) - 1
    Kmask = 0
    for x in Klist:
        Kmask |= (1 << x)
    Smask = ((mask_all ^ Kmask) & mask_all)

    answer = 0
    if Ksize > 0 and Ssize > 0:
        answer += 1

    # K -> S 이동 후보
    sNeighborCount = [0] * n
    soleSNeighbor = [-1] * n
    countXSingles = [0] * n
    Xcount = 0

    for x in Klist:
        b = adj[x] & Smask
        cnt = b.bit_count()
        sNeighborCount[x] = cnt
        if cnt == 0:
            Xcount += 1
        elif cnt == 1:
            lone = (b & -b)
            y = (lone.bit_length() - 1)
            soleSNeighbor[x] = y
            countXSingles[y] += 1

    # S -> K 이동 후보
    nonNeighborKCount = [2] * n
    soleKNonNeighbor = [-1] * n
    Ycount = 0

    for y in Slist:
        nb_in_K = (adj[y] & Kmask).bit_count()
        non_cnt = Ksize - nb_in_K
        if non_cnt <= 0:
            nonNeighborKCount[y] = 0
            Ycount += 1
        elif non_cnt == 1:
            non_mask = (Kmask & (~adj[y])) & mask_all
            lone = (non_mask & -non_mask)
            x0 = (lone.bit_length() - 1)
            nonNeighborKCount[y] = 1
            soleKNonNeighbor[y] = x0
        else:
            nonNeighborKCount[y] = 2

    if Ksize >= 2:
        answer += Xcount
    if Ssize >= 2:
        answer += Ycount

    # 스왑
    pairs = 0
    for y in Slist:
        nk = nonNeighborKCount[y]
        if nk == 0:
            pairs += Xcount
            pairs += countXSingles[y]
        elif nk == 1:
            x0 = soleKNonNeighbor[y]
            if sNeighborCount[x0] == 0:
                pairs += 1
            elif sNeighborCount[x0] == 1 and soleSNeighbor[x0] == y:
                pairs += 1
    answer += pairs

    print(answer)

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- 완전 그래프: 기준 분할은 K=n, S=∅이지만 K에서 한 정점씩 S로 이동해 정확히 n개의 분할 가능.
- 간선이 전혀 없는 그래프: 기준 분할은 K=1, S=n-1이며 S→K 이동은 불가. 스왑 없음.
- n=2 최소 크기: 두 정점이 연결됐으면 답=2, 아니면 답=0.
- 애매 정점(경계 정점)이 다수인 경우: 단일 이동/스왑 규칙으로 중복 없이 카운팅됨.
- 한쪽이 비어 있는 기준 분할: 단일 이동/스왑 규칙이 자동으로 비공백 조건을 보장하도록 크기 체크 포함.

## 제출 전 점검
- 입출력 형식/개행 확인, 64-bit 사용, 초기화/인덱스 범위 점검.
- C++: `-O2` 권장, `bitset` 사용으로 메모리/속도 균형.
- Python: 큰 n에서 느릴 수 있으니 제출은 C++ 권장.

## 참고자료
- Hammer, P. L., & Simeone, B. (1981). The splittance of a graph. (스플릿 그래프 판정의 고전적 결과)
- POI 2010/2011 Conspiracy 문제 설명
