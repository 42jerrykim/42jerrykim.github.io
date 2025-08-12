---
title: "[BOJ] Prefixuffix (8235) - 롤링 해시 O(n) C++ 풀이"
description: "백준 8235 Prefixuffix는 접두사와 접미사의 회전 동치 최대 길이를 구하는 문자열 문제입니다. 두 포인터와 롤링 해시(모듈러)로 T=A+B+X+B+A 구조를 O(n)에 찾아 C++로 구현하고, 경계 처리와 충돌 안정성까지 설명합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "8235"
- "Prefixuffix"
- "Prefix"
- "Suffix"
- "접두사"
- "접미사"
- "회전 동치"
- "Cyclic Equivalence"
- "문자열"
- "String"
- "해싱"
- "Hashing"
- "Rolling Hash"
- "Polynomial Hash"
- "모듈러 해시"
- "Modular Hash"
- "64-bit Hash"
- "Substr Hash"
- "서브스트링 해시"
- "두 포인터"
- "Two Pointers"
- "O(n)"
- "시간복잡도"
- "Time Complexity"
- "POI"
- "Polish Olympiad in Informatics"
- "Stage 3"
- "문제해설"
- "Editorial"
- "솔루션"
- "정답 코드"
- "Solution Code"
- "C++"
- "CPP"
- "GNU++17"
- "빠른입출력"
- "Fast IO"
- "경계 조건"
- "Edge Cases"
- "해시 충돌"
- "Hash Collision"
- "안정성"
- "Stability"
- "인덱싱"
- "Indexing"
- "문자열 알고리즘"
- "String Algorithms"
- "Competitive Programming"
- "Problem Solving"
- "PS"
- "코딩테스트"
- "Practice"
- "Study"
- "센티넬"
- "Sentinel"
- "Prefix Equals Suffix"
- "회전"
- "Rotation"
- "비교 최적화"
- "Comparison Optimization"
image: "featured-image.jpg"
draft: true
---

문제: [BOJ 8235 - Prefixuffix](https://www.acmicpc.net/problem/8235)

### 아이디어 요약
- 접두사 `P`와 접미사 `S`가 서로 회전 동치이면서 길이가 최대가 되도록, 문자열 `T`를 `T = A + B + X + B + A`로 표현합니다. 그러면 `P = A+B`, `S = B+A`가 되어 회전 동치가 보장됩니다.
- 길이 제약 `|P| = |S| ≤ n/2`를 만족하려면 `|A| = i`, `|B| = j`에 대해 `i + j ≤ n/2`입니다.
- 중요한 단조성: `i`(=|A|)를 1 줄일 때 최적 `j`(=|B|)는 최대 2만 증가합니다. 따라서 `i`를 감소시키며 `j`를 두 포인터처럼 관리하면 인덱스 이동 총량이 `O(n)`입니다.
- 구간 비교는 롤링 해시로 `O(1)`에 수행합니다. 충돌 가능성을 낮추기 위해 모듈러 해시를 사용하고 인덱스 경계(빈 문자열 포함)를 안전하게 처리합니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

// 모듈러 롤링 해시 (P=917, MOD=993244853)
const ll P = 917;
const ll MOD = 993244853;

struct Hasher {
    vector<ll> ha, pw; // ha[i] = hash of s[i..], pw[k] = P^k mod MOD
    Hasher() {}
    explicit Hasher(const string& s) {
        int n = (int)s.size();
        ha.assign(n + 1, 0);
        pw.assign(n + 1, 1);
        pw[1] = P;
        for (int i = n - 1; i >= 0; --i) {
            ha[i] = (ha[i + 1] * P + s[i]) % MOD;
        }
        for (int i = 2; i <= n; ++i) pw[i] = pw[i - 1] * P % MOD;
    }
    // [l, r] (0-based, inclusive)
    inline ll get(int l, int r) const {
        if (r < l) return 0; // 빈 구간
        ll res = (ha[l] - ha[r + 1] * pw[r - l + 1]) % MOD;
        if (res < 0) res += MOD;
        return res;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    string t;
    if (!(cin >> n >> t)) return 0;

    // 1-indexed 보정용 센티넬을 앞에 두고 해싱
    string s = "#" + t;
    Hasher H(s);

    auto same = [&](int l1, int r1, int l2, int r2) -> bool {
        if (r1 < l1 && r2 < l2) return true;   // 둘 다 빈 문자열
        if (r1 < l1 || r2 < l2) return false;  // 한쪽만 빈 문자열
        return H.get(l1, r1) == H.get(l2, r2);
    };

    int ans = 0;
    int j = 0; // |B|
    for (int i = n / 2; i >= 1; --i) { // i = |A|
        j = min(n / 2 - i, j + 2);
        // 양 끝의 A가 같아야 T = A + B + X + B + A 성립
        if (!same(1, i, n - i + 1, n)) continue;

        ans = max(ans, i); // B = 0인 경우

        // B를 가능한 한 크게 확장
        while (j >= 0 && !same(i + 1, i + j, n - i + 1 - j, n - i)) --j;
        ans = max(ans, i + j); // |P| = |A| + |B|
    }

    cout << ans << '\n';
    return 0;
}
```

### 복잡도
- 시간: `O(n)` (두 포인터 이동 총량 선형 + 해시 비교 `O(1)`)
- 공간: `O(n)` (해시 누적과 거듭제곱 테이블)

### 참고
- 문제: `https://www.acmicpc.net/problem/8235`
- 아이디어: `T = A + B + X + B + A` 구조로 환원 + 단조성 이용한 두 포인터 + 롤링 해시 비교


