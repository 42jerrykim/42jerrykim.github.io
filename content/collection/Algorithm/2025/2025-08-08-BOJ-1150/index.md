---
title: "[Algorithm] C++ 백준 1150번 : 백업"
categories:
- Algorithm
- Greedy
- Data Structures
description: "BOJ 1150번 백업 문제다. N개 지점에서 K개 케이블을 선택해 총 길이를 최소화하는 greedy 알고리즘이다. 우선순위 큐와 이중연결리스트로 인접한 케이블 쌍을 효율적으로 관리하며, 선택 시 겹치지 않게 처리한다. O((N+K)logN) 시간복잡도로 해결한다."
tags:
  - Algorithm
  - 알고리즘
  - Data Structures
  - 자료구조
  - Doubly Linked List
  - 이중연결리스트
  - Greedy
  - 그리디
  - Matching
  - 매칭
  - Priority Queue
  - 우선순위큐
  - Min Heap
  - 최소힙
  - Graph Theory
  - 그래프이론
  - Path Graph
  - 경로그래프
  - Edge Selection
  - 간선선택
  - Optimization
  - 최적화
  - Dynamic Programming
  - 동적계획법
  - Time Complexity
  - 시간복잡도
  - Space Complexity
  - 공간복잡도
  - O((N + K) log N)
  - BOJ
  - 백준
  - C++
  - Implementation
  - 구현
  - Competitive Programming
  - 경쟁프로그래밍
  - Network
  - 네트워크
  - Cable
  - 케이블
  - Distance
  - 거리
  - Minimization
  - 최소화
  - Pair Selection
  - 쌍선택
  - Adjacent
  - 인접
  - Non-overlapping
  - 비겹침
  - Coordinate
  - 좌표
  - Linear
  - 선형
  - Backup
  - 백업
  - Company
  - 회사
date: 2025-08-08
image: wordcloud.png
---

n개의 회사가 직선상에 배치되어 있고, k개의 네트워크 케이블로 정확히 k개의 회사 쌍을 연결해야 한다. 각 회사는 최대 하나의 케이블에만 연결될 수 있으며, 목표는 연결된 회사 쌍들 간의 거리 합을 최소화하는 것이다. 

이 문제는 경로 그래프에서 비인접한 k개의 간선을 선택해 가중치 합을 최소화하는 문제로 모델링할 수 있다. 그리디 알고리즘과 우선순위 큐, 이중 연결 리스트를 활용해 O((N + K) log N) 시간복잡도로 해결 가능하다.

문제: [https://www.acmicpc.net/problem/1150](https://www.acmicpc.net/problem/1150)

## 문제 요약

직선 위에 위치한 `n`개의 회사 좌표가 오름차순으로 주어진다. `k`개의 네트워크 케이블만 사용할 수 있으며, 한 회사는 하나의 케이블에만 연결될 수 있다. 정확히 `k`개의 쌍을 만들어 각 쌍의 거리 합을 최소화하라.

## 접근

- 인접한 회사 간 거리 `d[i] = s[i+1] - s[i]`를 간선 가중치로 하는 경로 그래프에서, 서로 인접하지 않게 정확히 `k`개의 간선을 골라 합을 최소화하는 문제와 동치다.
- 그리디 + 우선순위큐 + 이중 연결 리스트(좌/우 포인터)를 이용한다.
  - 가장 작은 `d[i]`를 선택하면 그 양옆 `d[i-1], d[i+1]`은 동시에 사용할 수 없으니 제거한다.
  - 선택 위치 `i`의 값은 "좌+우-현재"로 보정해 추후 병합 비용을 반영한다.
- 각 연산은 우선순위큐 갱신으로 처리해 총 `O((n + k) log n)`.

## C++17 풀이

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Item {
    long long val;
    int idx;
    int ver;
    bool operator<(const Item& other) const {
        if (val != other.val) return val > other.val; // min-heap behavior
        return idx > other.idx;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    if (!(cin >> n >> k)) return 0;
    vector<long long> s(n);
    for (int i = 0; i < n; ++i) cin >> s[i];

    int m = n - 1; // number of diffs
    vector<long long> val(m + 1, 0);
    for (int i = 1; i <= m; ++i) val[i] = s[i] - s[i - 1];

    const long long INF = (long long)4e18;

    vector<int> L(m + 1), R(m + 1);
    for (int i = 1; i <= m; ++i) {
        L[i] = (i == 1 ? 0 : i - 1);
        R[i] = (i == m ? 0 : i + 1);
    }

    vector<char> removed(m + 1, 0);
    vector<int> ver(m + 1, 0);

    priority_queue<Item> pq;
    for (int i = 1; i <= m; ++i) {
        pq.push({val[i], i, ver[i]});
    }

    long long answer = 0;
    for (int picks = 0; picks < k; ++picks) {
        Item cur;
        while (true) {
            if (pq.empty()) {
                cout << answer << "\n";
                return 0;
            }
            cur = pq.top(); pq.pop();
            if (cur.ver != ver[cur.idx]) continue;
            if (removed[cur.idx]) continue;
            break;
        }

        int i = cur.idx;
        answer += cur.val;

        int Li = L[i];
        int Ri = R[i];

        if (Li != 0) removed[Li] = 1;
        if (Ri != 0) removed[Ri] = 1;

        long long leftVal  = (Li == 0 ? INF : val[Li]);
        long long rightVal = (Ri == 0 ? INF : val[Ri]);

        int LL = (Li == 0 ? 0 : L[Li]);
        int RR = (Ri == 0 ? 0 : R[Ri]);

        L[i] = LL;
        if (LL != 0) R[LL] = i;
        R[i] = RR;
        if (RR != 0) L[RR] = i;

        val[i] = leftVal + rightVal - cur.val;
        ver[i] += 1;
        pq.push({val[i], i, ver[i]});
    }

    cout << answer << "\n";
    return 0;
}
```

## 복잡도

- 시간: `O((n + k) log n)`
- 공간: `O(n)`

## 포인트 정리

- 인접 차이 `d[i]`를 간선으로 보고, 서로 인접하지 않게 `k`개 선택하는 최소합 문제.
- 선택 시 좌우 제거, 선택 노드 값은 "좌+우-현재"로 갱신하여 이후 최적 병합 비용 반영.






