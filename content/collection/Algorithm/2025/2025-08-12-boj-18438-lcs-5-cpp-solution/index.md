---
title: "[BOJ] LCS 5 (18438) - Hirschberg C++"
description: "백준 18438 LCS 5는 최대 7000 길이의 두 문자열에 대해 LCS의 길이와 실제 수열을 모두 출력해야 하는 문제입니다. 4MB 메모리 제한 때문에 전형적인 2차원 DP 테이블을 저장할 수 없으므로, O(nm) 시간에 O(min(n,m)) 메모리만 사용하는 Hirschberg 알고리즘으로 안전하게 복원합니다. 전방·후방 1차원 DP, 분할 지점 선택, 경계 처리와 빠른 입출력까지 반영한 C++ 구현과 복잡도 분석을 제공합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "Baekjoon"
- "백준"
- "18438"
- "LCS"
- "Longest Common Subsequence"
- "최장 공통 부분 수열"
- "LCS 5"
- "Hirschberg"
- "히르슈베르크"
- "Divide and Conquer"
- "분할정복"
- "DP"
- "Dynamic Programming"
- "동적 계획법"
- "Memory Optimization"
- "메모리 최적화"
- "Space Complexity"
- "공간 복잡도"
- "Time Complexity"
- "시간 복잡도"
- "O(NM)"
- "O(min(n,m))"
- "Reconstruction"
- "복원"
- "Backtracking"
- "역추적"
- "String"
- "문자열"
- "Special Judge"
- "스페셜 저지"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른 입출력"
- "Edge Cases"
- "경계 조건"
- "Correctness"
- "정당성"
- "Optimization"
- "최적화"
- "Stable"
- "안정성"
- "Tutorial"
- "해설"
- "Solution Code"
- "정답 코드"
- "Problem Solving"
- "문제 해결"
- "Competitive Programming"
- "컴페티티브 프로그래밍"
- "Baekjoon 18438"
- "BOJ 18438"
- "문제풀이"
- "코드"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 18438 - LCS 5](https://www.acmicpc.net/problem/18438)

### 아이디어 요약
- 메모리 4MB, 문자열 최대 7000이므로 2차원 DP 테이블 보관은 불가합니다.
- Hirschberg 알고리즘을 사용해 절반 분할 + 전/후방 1차원 LCS 길이 계산으로 분할 지점을 찾고, 좌/우 재귀로 실제 LCS를 복원합니다.
- 시간은 `O(nm)`, 메모리는 `O(min(n,m))`로 제한을 만족하며, 스페셜 저지이므로 임의의 LCS 하나를 출력하면 됩니다.

### C++ 풀이

```cpp
// 더 많은 정보는 42jerrykim.github.io에서 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

static vector<int> lcsForward(const string& a, int al, int ar,
                              const string& b, int bl, int br) {
    const int m = br - bl;
    vector<int> prev(m + 1, 0), curr(m + 1, 0);
    for (int i = al; i < ar; ++i) {
        curr[0] = 0;
        const char ca = a[i];
        for (int j = 1; j <= m; ++j) {
            if (ca == b[bl + j - 1]) curr[j] = prev[j - 1] + 1;
            else curr[j] = prev[j] >= curr[j - 1] ? prev[j] : curr[j - 1];
        }
        prev.swap(curr);
    }
    return prev; // LCS lengths with prefixes of b[bl..br)
}

static vector<int> lcsBackward(const string& a, int al, int ar,
                               const string& b, int bl, int br) {
    const int m = br - bl;
    vector<int> prev(m + 1, 0), curr(m + 1, 0);
    for (int i = ar - 1; i >= al; --i) {
        curr[0] = 0;
        const char ca = a[i];
        for (int j = 1; j <= m; ++j) {
            if (ca == b[br - j]) curr[j] = prev[j - 1] + 1;
            else curr[j] = prev[j] >= curr[j - 1] ? prev[j] : curr[j - 1];
        }
        prev.swap(curr);
    }
    return prev; // LCS lengths with suffixes of b[bl..br)
}

static void hirschberg(const string& a, int al, int ar,
                       const string& b, int bl, int br,
                       string& out) {
    if (al >= ar || bl >= br) return;
    if (ar - al == 1) {
        const char ca = a[al];
        for (int j = bl; j < br; ++j) {
            if (b[j] == ca) { out.push_back(ca); break; }
        }
        return;
    }

    const int am = al + (ar - al) / 2;
    const vector<int> L1 = lcsForward(a, al, am, b, bl, br);
    const vector<int> L2 = lcsBackward(a, am, ar, b, bl, br);

    const int m = br - bl;
    int split = 0, best = -1;
    for (int k = 0; k <= m; ++k) {
        int val = L1[k] + L2[m - k];
        if (val > best) { best = val; split = k; }
    }

    hirschberg(a, al, am, b, bl, bl + split, out);
    hirschberg(a, am, ar, b, bl + split, br, out);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    if (!(cin >> s >> t)) return 0;

    string lcs;
    lcs.reserve(min(s.size(), t.size()));
    hirschberg(s, 0, (int)s.size(), t, 0, (int)t.size(), lcs);

    cout << lcs.size() << '\n' << lcs << '\n';
    return 0;
}
```

### 복잡도
- 시간: `O(nm)`
- 메모리: `O(min(n,m))`

참고: 문제: `https://www.acmicpc.net/problem/18438`


