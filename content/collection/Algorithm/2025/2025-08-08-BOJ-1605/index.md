---
title: "[Algorithm] C++ 백준 1605번: 반복 부분문자열"
description: "BOJ 1605 반복 부분문자열 문제다. Suffix Array와 LCP Array를 활용해 가장 긴 반복 부분문자열의 길이를 O(n log n) 시간복잡도로 구한다. 배가법(doubling)과 카운팅 소트로 접미사 배열을 구성하고, Kasai 알고리즘으로 LCP 배열을 계산한다. 인접한 접미사들의 최대 LCP가 정답이다."
date: 2025-08-08
lastmod: 2025-08-09
categories:
- Algorithm
- String
- Data Structures
tags:
 - Algorithm
 - Data Structures
 - String
 - 문자열
 - BOJ
 - C++
 - Suffix Array
 - LCP
 - LCP Array
 - Kasai
 - Doubling
 - Counting Sort
 - Stable Sort
 - Rank
 - Lexicographic Order
 - Longest Repeated Substring
 - LRS
 - Rolling Hash
 - Binary Search
 - Suffix Tree
 - SA-IS
 - DivSufSort
 - Text Indexing
 - Pattern Matching
 - O(n log n)
 - O(n)
 - Time Complexity
 - Space Complexity
 - Implementation
 - Competitive Programming
 - 문자열 알고리즘
 - 접미사배열
 - LCP배열
 - 카사이 알고리즘
 - 반복 부분문자열
 - 최장 반복 부분문자열
 - 이분 탐색
 - 롤링 해시
 - 사전순 정렬
 - 카운팅 소트
 - 안정 정렬
 - 랭크 배열
 - 배가법
 - 서픽스 트리
 - 문자열 인덱싱
 - 패턴 매칭
 - 백준
 - 플래티넘
 - 최적화
 - 구현 디테일
image: wordcloud.png
---

문자열 안에서 적어도 한 번 이상 반복되는 부분문자열(즉, 전체 문자열에서 두 번 이상 등장하는 부분문자열)의 최대 길이를 구하는 문제이다. 길이 \(L\) 은 최대 200,000이므로, 단순한 모든 구간 비교는 시간 내에 불가능하다.

문제: [BOJ 1605 — 반복 부분문자열](https://www.acmicpc.net/problem/1605)

## 문제 정보

- 시간 제한: 2초
- 메모리 제한: 128MB
- 입력 제한: L ≤ 200,000, 문자열은 소문자

## 접근 방식

- 가장 긴 반복 부분문자열의 길이는 접미사 배열(Suffix Array)과 LCP 배열(Kasai)로 구할 수 있다.
- 문자열의 모든 접미사를 사전순으로 정렬한 뒤, 인접한 접미사들 간 LCP(최장 공통 접두사)의 최댓값이 정답이 된다.
- 시간 복잡도: 접미사 배열 배가법(O(n log n)) + Kasai O(n) ⇒ O(n log n)

참고로, 이 문제는 해시(이중 롤링 해시) + 이분 탐색(O(n log n))으로도 풀 수 있으나, 본 글에서는 접미사 배열 기반 풀이를 제공한다.

## C++ 풀이 (Suffix Array + LCP)

```cpp
#include <bits/stdc++.h>
using namespace std;

// Stable counting sort by key in range [0, K)
static void counting_sort(vector<int>& sa, const vector<int>& key, int K) {
    int n = (int)sa.size();
    vector<int> cnt(K + 1, 0), tmp(n);
    for (int i = 0; i < n; ++i) cnt[key[i]]++;
    for (int i = 1; i <= K; ++i) cnt[i] += cnt[i - 1];
    for (int i = n - 1; i >= 0; --i) tmp[--cnt[key[sa[i]]]] = sa[i];
    sa.swap(tmp);
}

static vector<int> build_sa(const string& s) {
    int n = (int)s.size();
    vector<int> sa(n), rnk(n), tmp(n);
    for (int i = 0; i < n; ++i) {
        sa[i] = i;
        rnk[i] = (unsigned char)s[i];
    }
    for (int k = 1;; k <<= 1) {
        int maxRank = *max_element(rnk.begin(), rnk.end());
        int K = max(maxRank + 2, 258);
        vector<int> key2(n);
        for (int i = 0; i < n; ++i) key2[i] = (i + k < n ? rnk[i + k] + 1 : 0);

        counting_sort(sa, key2, K);
        vector<int> key1(n);
        for (int i = 0; i < n; ++i) key1[i] = rnk[i] + 1;
        counting_sort(sa, key1, K);

        tmp[sa[0]] = 0;
        for (int i = 1; i < n; ++i) {
            int a = sa[i - 1], b = sa[i];
            bool diff = (rnk[a] != rnk[b]) || (key2[a] != key2[b]);
            tmp[b] = tmp[a] + (diff ? 1 : 0);
        }
        rnk.swap(tmp);
        if (rnk[sa[n - 1]] == n - 1) break;
    }
    return sa;
}

static vector<int> build_lcp(const string& s, const vector<int>& sa) {
    int n = (int)s.size();
    vector<int> rank(n), lcp(max(0, n - 1));
    for (int i = 0; i < n; ++i) rank[sa[i]] = i;
    int h = 0;
    for (int i = 0; i < n; ++i) {
        int r = rank[i];
        if (r == n - 1) { h = 0; continue; }
        int j = sa[r + 1];
        while (i + h < n && j + h < n && s[i + h] == s[j + h]) ++h;
        lcp[r] = h;
        if (h > 0) --h;
    }
    return lcp;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int L; string s;
    if (!(cin >> L)) return 0;
    cin >> s;
    if (s.empty()) { cout << 0 << '\n'; return 0; }
    auto sa = build_sa(s);
    auto lcp = build_lcp(s, sa);
    int ans = 0;
    for (int v : lcp) ans = max(ans, v);
    cout << ans << '\n';
    return 0;
}
```

## 복잡도

- **시간**: O(n log n)
- **공간**: O(n)


## 문제 요약

- **정의**: 문자열의 부분문자열 중, 전체 문자열에서 두 번 이상 등장하는 부분문자열을 반복 부분문자열이라 한다. 겹쳐서 등장해도 인정한다.
- **목표**: 가장 긴 반복 부분문자열의 길이를 구한다. 없으면 0.

## 입출력 형식

- **입력**
  - 첫 줄: 정수 L (1 ≤ L ≤ 200000)
  - 둘째 줄: 길이 L의 소문자 문자열 s
- **출력**
  - 가장 긴 반복 부분문자열의 길이. 없으면 0

## 예제

입력

```
28
tellmetellmetetetetetetellme
```

출력

```
11
```

## 왜 Suffix Array + LCP로 풀까?

- 모든 접미사를 사전순으로 정렬하면, 반복 부분문자열은 어떤 두 접미사의 공통 접두사로 나타난다.
- 사전순으로 인접한 두 접미사는 공통 접두사 길이가 큰 편이고, 전체 최댓값은 인접한 쌍 중 어딘가에서 반드시 달성된다.
- 따라서, 접미사 배열을 만든 뒤 인접한 접미사들 간 LCP의 최댓값이 곧 정답이다.

증명 스케치: 두 접미사 i, j의 공통 접두사 길이를 x라 하자. 정렬된 접미사 배열에서 i와 j 사이에 있는 접미사들과의 LCP 최소값이 x 이상이므로, 인접한 어느 구간에서 최소 LCP가 x를 달성한다. 그 중 최댓값이 전체 최댓값과 일치한다.

## 구현 디테일

- 접미사 배열은 배가법(doubling)으로 (rank[i], rank[i+k])를 키로 정렬한다.
- 두 번의 안정적 카운팅 소트로 키2(뒤쪽) → 키1(앞쪽) 순으로 정렬해 O(n) per step을 보장한다.
- 경계를 위해 없는 위치의 랭크는 0으로 치환하기 위해 실제 랭크에 +1 오프셋을 준다.
- 모든 랭크가 서로 달라지면 조기 종료한다.
- LCP는 Kasai 알고리즘으로 O(n) 시간에 계산한다. 직전 LCP에서 1만 감소시키며 재활용한다.

## 코너 케이스 체크리스트

- L = 1 → 정답 0
- 모든 문자가 서로 다름 → 정답 0
- 모든 문자가 동일("aaaa…") → 정답은 L-1
- 겹치는 반복 허용: 예) "aaaa"에서 길이 3의 반복("aaa")는 위치 0과 1에서 겹치지만 유효하다
- 입력은 소문자만 가정하므로 알파벳 크기 26, 하지만 구현은 일반 바이트값 기준이라 범용적

## 참고자료

- Suffix Array — Wikipedia: [https://en.wikipedia.org/wiki/Suffix_array](https://en.wikipedia.org/wiki/Suffix_array)
- LCP array — Wikipedia: [https://en.wikipedia.org/wiki/LCP_array](https://en.wikipedia.org/wiki/LCP_array)
- Longest repeated substring problem — Wikipedia: [https://en.wikipedia.org/wiki/Longest_repeated_substring_problem](https://en.wikipedia.org/wiki/Longest_repeated_substring_problem)
- Suffix Array — cp-algorithms: [https://cp-algorithms.com/string/suffix-array.html](https://cp-algorithms.com/string/suffix-array.html)