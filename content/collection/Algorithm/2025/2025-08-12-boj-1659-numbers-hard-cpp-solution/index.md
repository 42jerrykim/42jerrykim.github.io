---
title: "[Algorithm] BOJ 1659 - 수 (Hard) C++ 풀이 - O(n+m) DP"
description: "백준 1659 수 (Hard): S∪T 병합 정렬 뒤 약한 연결(최근접 반대 타입)과 균형 구간 강한 매칭 비용(|∑S−∑T|)을 결합한 선형 DP로 최소 총비용을 구한다. 시간 O(n+m), 메모리 O(n+m)인 C++ 구현과 핵심 아이디어를 함께 정리한다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "1659"
- "수"
- "Numbers"
- "Hard"
- "ICPC"
- "Seoul Regional 2007"
- "Asia Regional"
- "문제해결"
- "Problem Solving"
- "Algorithm"
- "알고리즘"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "DP"
- "Dynamic Programming"
- "O(n+m)"
- "Linear Time"
- "선형 시간"
- "Prefix Sum"
- "접두사 합"
- "Greedy"
- "그리디"
- "두 집합"
- "Set Pairing"
- "짝짓기"
- "비용 최소화"
- "Absolute Difference"
- "절댓값"
- "Sorted Merge"
- "병합 정렬"
- "In-order Matching"
- "비교 불교차"
- "Non-crossing"
- "교차 금지"
- "강한 연결"
- "약한 연결"
- "Strong Matching"
- "Weak Matching"
- "Balance"
- "균형"
- "Counting"
- "세기"
- "Two Pointers"
- "투 포인터"
- "Nearest Neighbor"
- "가장 가까운 원소"
- "Gap Sum"
- "간격 합"
- "Implementation"
- "구현"
- "Optimization"
- "최적화"
- "Int64"
- "long long"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 1659 - 수 (Hard)](https://www.acmicpc.net/problem/1659)

### 아이디어 요약
- S, T를 하나의 정렬된 시퀀스로 병합해 인덱스 i마다 타입(+1=S, -1=T)과 값 `value[i]`를 기록합니다.
- 두 가지 선택으로 DP를 구성합니다.
  - 약한 연결: `i`를 가장 가까운 반대 타입 원소와 연결. 비용은 좌우 이웃 중 더 가까운 거리.
  - 강한 연결: 마지막으로 같은 균형(`prefixDiff`)을 보인 위치 `j` 이후 구간 `(j+1..i)`을 일대일(비교차)로 묶기. 이때 최소 비용은 `|(구간 S 합) - (구간 T 합)|`로 O(1)에 계산됩니다.
- 점화식: `dp[i] = min(dp[i-1] + nearestOppDist[i], dp[j] + |sumS(i)-sumS(j) - (sumT(i)-sumT(j))|)`.
- `j`는 `prefixDiff` 값이 같은 마지막 인덱스로 해시/배열에 저장하며, 초기 상태로 균형 0의 인덱스를 `-1`로 둡니다.

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
    vector<long long> S(n), T(m);
    for (int i = 0; i < n; ++i) cin >> S[i];
    for (int j = 0; j < m; ++j) cin >> T[j];

    // 병합: value, type(+1=S, -1=T)
    const int N = n + m;
    vector<long long> value(N);
    vector<int> type(N); // +1 for S, -1 for T
    {
        int i = 0, j = 0, k = 0;
        while (i < n || j < m) {
            if (j == m || (i < n && S[i] <= T[j])) { value[k] = S[i]; type[k] = +1; ++i; }
            else { value[k] = T[j]; type[k] = -1; ++j; }
            ++k;
        }
    }

    // 균형 prefixDiff, 그리고 S/T 값 누적합
    vector<int> prefixDiff(N);
    vector<long long> prefS(N), prefT(N);
    for (int i = 0; i < N; ++i) {
        prefixDiff[i] = (i ? prefixDiff[i - 1] : 0) + type[i];
        prefS[i] = (i ? prefS[i - 1] : 0LL) + (type[i] == +1 ? value[i] : 0LL);
        prefT[i] = (i ? prefT[i - 1] : 0LL) + (type[i] == -1 ? value[i] : 0LL);
    }

    // 각 i의 가장 가까운 반대 타입 거리 (약한 연결 비용)
    const long long INF = (long long)4e18;
    vector<long long> nearestOppDist(N, INF);
    int lastS = -1, lastT = -1;
    for (int i = 0; i < N; ++i) {
        if (type[i] == +1) { if (lastT != -1) nearestOppDist[i] = min(nearestOppDist[i], value[i] - value[lastT]); lastS = i; }
        else { if (lastS != -1) nearestOppDist[i] = min(nearestOppDist[i], value[i] - value[lastS]); lastT = i; }
    }
    int nextS = -1, nextT = -1;
    for (int i = N - 1; i >= 0; --i) {
        if (type[i] == +1) { if (nextT != -1) nearestOppDist[i] = min(nearestOppDist[i], value[nextT] - value[i]); nextS = i; }
        else { if (nextS != -1) nearestOppDist[i] = min(nearestOppDist[i], value[nextS] - value[i]); nextT = i; }
    }

    // dp[i]: 0..i까지 조건 만족 최소 비용
    vector<long long> dp(N);
    // 균형값 -> 마지막 인덱스. 균형 0의 시작 위치를 -1로 설정
    int offset = N + 5;
    vector<int> lastIndex(2 * offset + 1, INT_MIN);
    auto getLast = [&](int bal) -> int {
        int idx = bal + offset;
        if (idx < 0 || idx >= (int)lastIndex.size()) return INT_MIN;
        return lastIndex[idx];
    };
    auto setLast = [&](int bal, int pos) {
        int idx = bal + offset;
        if (0 <= idx && idx < (int)lastIndex.size()) lastIndex[idx] = pos;
    };
    setLast(0, -1);

    for (int i = 0; i < N; ++i) {
        long long best = (i > 0 ? dp[i - 1] : 0LL) + nearestOppDist[i];

        int bal = prefixDiff[i];
        int j = getLast(bal); // j < i 이고 prefixDiff[j] == prefixDiff[i]
        if (j != INT_MIN) {
            long long sumS = prefS[i] - (j >= 0 ? prefS[j] : 0LL);
            long long sumT = prefT[i] - (j >= 0 ? prefT[j] : 0LL);
            long long strongCost = llabs(sumS - sumT);
            long long candidate = (j >= 0 ? dp[j] : 0LL) + strongCost;
            best = min(best, candidate);
        }

        dp[i] = best;
        setLast(bal, i);
    }

    cout << dp[N - 1] << '\n';
    return 0;
}
```

### 복잡도
- 시간: O(n+m)
- 공간: O(n+m)

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`

필요 시 예제 입력(문제 페이지의 예시)로 빠르게 검증해 볼 수 있습니다.


