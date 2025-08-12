---
title: "[BOJ] Double Clique (16041) - C++ 풀이"
description: "백준 16041 Double Clique를 스플릿 그래프 특성으로 환원해 정렬된 차수 누적 합 등식(sum_S−s(s−1)=2m−sum_S)으로 분할 크기 s를 찾고, 제거·추가·교환 경우의 수를 합산해 1e9+7로 정답을 출력하는 C++ 풀이."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "16041"
- "Double Clique"
- "DoubleClique"
- "NAIPC 2018"
- "NAIPC"
- "North American Invitational Programming Contest"
- "그래프"
- "Graph"
- "Graph Theory"
- "그래프 이론"
- "스플릿 그래프"
- "Split Graph"
- "독립 집합"
- "Independent Set"
- "클릭"
- "Clique"
- "보수 그래프"
- "Complement Graph"
- "차수"
- "Degree"
- "차수 합"
- "Degree Sum"
- "핸드셰이킹 렘마"
- "Handshaking Lemma"
- "정렬"
- "Sorting"
- "O(n log n)"
- "시간복잡도"
- "Time Complexity"
- "조합론"
- "Combinatorics"
- "세기 문제"
- "Counting"
- "케이스 분석"
- "Case Analysis"
- "구현"
- "Implementation"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "모듈로"
- "Modular Arithmetic"
- "1e9+7"
- "mod 1e9+7"
- "에지"
- "Edges"
- "정점"
- "Vertices"
- "문제해설"
- "Editorial"
- "해설"
- "풀이"
- "알고리즘"
- "Algorithm"
- "코딩테스트"
- "Competitive Programming"
- "ICPC"
- "자료구조"
- "Data Structures"
- "분할"
- "Partition"
- "스플릿"
- "검증"
- "Validation"
- "증명"
- "Proof"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 16041 - Double Clique](https://www.acmicpc.net/problem/16041)

### 아이디어 요약
- Double Clique란 `S`가 `G`에서 클릭이고, `V−S`가 `G'`(보수 그래프)에서 클릭인 부분집합입니다. 이는 원래 그래프 `G`에서 `S`는 클릭, `T=V−S`는 독립 집합이 되는 스플릿(split) 그래프 분할을 의미합니다.
- 정점 차수를 내림차순으로 정렬하고 상위 `s`개의 차수 합을 `sum_S`라 하면, 스플릿 분할의 필요충분식은 `sum_S − s(s−1) = 2m − sum_S` 입니다.
  - 좌변은 `S`와 `T` 사이 간선 수 `X`, 우변은 전체 차수합 `2m`에서 `S`의 차수합을 뺀 `sum_T = X`와 동일해야 합니다.
- 위 등식이 처음 성립하는 `s`를 찾아 분할 `(S,T)`를 결정합니다. 이후 경우의 수는 다음 세 가지를 모두 더합니다.
  1) 기본 집합 `S` 자체.
  2) `S` 내부에서 차수가 정확히 `s−1`인 정점 `x`를 제거해도 `T`에 간선이 없어 `S\\{x}`가 유효.
  3) `T`에서 차수가 정확히 `s`인 정점 `y`를 추가하여 `S∪{y}`가 유효. 또한 이런 `y`와 `S` 내부에서 차수 `s`인 정점 `x`를 교환해도 유효(`S∪{y}\\{x}`).
- 총합을 `1e9+7`로 모듈러 하여 출력합니다. 인접 리스트는 필요 없고 차수만 있으면 됩니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;
    vector<int> deg(n, 0);
    for (int i = 0; i < m; ++i) {
        int a, b; cin >> a >> b;
        --a; --b;
        deg[a]++; deg[b]++;
    }

    vector<pair<int,int>> v(n);
    for (int i = 0; i < n; ++i) v[i] = {deg[i], i};
    sort(v.begin(), v.end(), [](const auto& x, const auto& y){
        if (x.first != y.first) return x.first > y.first;
        return x.second < y.second;
    });

    const long long MOD = 1000000007LL;
    long long tot2 = 2LL * m;
    long long sum = 0;
    vector<long long> freq(n + 1, 0); // freq[d]: # of vertices in S with degree d
    int size = -1;

    for (int i = 0; i < n; ++i) {
        long long s = i + 1;
        if (tot2 - s * (s - 1) < 0) break; // early impossibility
        sum += v[i].first;
        int d = v[i].first;
        if (d <= n) freq[d]++;

        long long rest = sum - s * (s - 1); // edges between S and T
        if (rest == tot2 - sum) {          // T has no internal edges
            size = (int)s;
            break;
        }
    }

    if (size == -1) {
        cout << 0 << '\n';
        return 0;
    }

    long long res = 1; // base set S
    for (int i = 0; i < size; ++i) {
        if (deg[v[i].second] == size - 1) {
            res++;
            if (res >= MOD) res -= MOD;
        }
    }
    for (int i = size; i < n; ++i) {
        if (deg[v[i].second] == size) {
            res++; if (res >= MOD) res -= MOD;     // add this vertex to S
            res = (res + freq[size]) % MOD;        // swap with any vertex in S of degree == size
        }
    }

    cout << (res % MOD) << '\n';
    return 0;
}
```

### 복잡도
- 정렬 `O(n log n)`, 입력 처리 `O(m)` → 전체 `O(n log n + m)` 시간, `O(n)` 추가 메모리.

### 참고
- 문제: `https://www.acmicpc.net/problem/16041`
- 콘테스트: NAIPC 2018 B - Double Clique


