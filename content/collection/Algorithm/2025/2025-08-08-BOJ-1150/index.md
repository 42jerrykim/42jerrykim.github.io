---
title: "[Algorithm] C++ 백준 1150번 : 백업"
categories:
- Algorithm
- Greedy
- Data Structures
tags:
- Greedy
- Priority Queue
- Doubly Linked List
- Matching
- O((N + K) log N)
date: 2025-08-08
draft: true
---

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





