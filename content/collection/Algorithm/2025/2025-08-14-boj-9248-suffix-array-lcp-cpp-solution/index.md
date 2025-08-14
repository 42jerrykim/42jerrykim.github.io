---
title: "[Algorithm] cpp 백준 9248번: Suffix Array - 접미사 배열과 LCP O(n log n)"
description: "접미사 배열을 O(n log n) 더블링으로 구축하고, LCP 배열은 카사이 알고리즘으로 O(n)에 계산합니다. 안정 정렬·랭크 갱신·경계 처리와 엣지 케이스 점검까지 담은 실전 풀이."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- String
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-9248
- cpp
- C++
- 문자열
- String
- Suffix Array
- 접미사 배열
- LCP
- Longest Common Prefix
- 카사이
- Kasai
- Doubling
- 더블링
- Rank
- 랭크
- Stable Sort
- 안정 정렬
- Counting Sort
- 계수 정렬
- Two-Key Sort
- 두 단계 정렬
- Lexicographic
- 사전순
- Implementation
- 구현
- Implementation Details
- 구현 디테일
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
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- String Algorithms
- 문자열 알고리즘
- SA-IS
- 접미사 배열 구축
- Prefix
- 접두사
- Indexing
- 인덱싱
- O(n log n)
- O(n)
- Memory
- 메모리
image: "wordcloud.png"
---

## 문제
- 링크: [BOJ 9248 Suffix Array](https://www.acmicpc.net/problem/9248)
- 요약: 문자열 S(길이 ≤ 500,000)가 주어질 때, 접미사 배열(SA)과 LCP 배열을 출력한다. LCP 첫 값은 문자 `x`로 표기한다.
- 제한/스펙: 시간 3초, 메모리 256MB, 소문자 알파벳.

## 입력/출력
```
입력: 소문자 문자열 S 한 줄
출력: 1행 SA(1-based), 2행 LCP(선두는 x), 공백 구분
```

예시 (문제 제공):
```
입력
abracadabra

출력
11 8 1 4 6 9 2 5 7 10 3
x 1 4 1 1 0 3 0 0 0 2
```

## 접근 개요
- SA: 더블링(doubling) 방식으로 O(n log n)에 구성. 길이 \(k\)와 \(k\) 이후의 2-키(rank, rank_{i+k})로 안정 계수 정렬.
- LCP: 카사이(Kasai) 알고리즘으로 O(n)에 계산. 인접 접미사 간 공통 접두사 길이를 효율적으로 누적/감소.
- 대규모 입력(최대 50만)에 맞춰 모든 정렬은 계수 정렬 기반, 불필요한 재할당 최소화.

## 알고리즘 설계
- 초기 랭크: 문자값(0 예약을 위해 1부터)로 부여하고 계수 정렬로 초기 SA 구성.
- k를 1→2→4→…로 두 배씩 키우며 다음을 반복:
  - 두 번째 키가 비는 suffix(i≥n−k)는 앞에 두고, 나머지는 i−k를 이용해 2-키 정렬 순서 유도.
  - 현재 랭크 기준으로 계수 정렬 1회로 SA 갱신.
  - 인접 쌍의 (rank[i], rank[i+k]) 비교로 새로운 랭크 재부여. 모든 랭크가 서로 달라지면 조기 종료.
- LCP(Kasai): rank 배열을 통해 각 위치 i의 이전 접미사와의 공통 접두사 길이를 누적 비교, 매 단계 1씩 감소해 총 O(n).

간단 의사코드:
```
rank[i] <- s[i]+1
SA <- counting_sort_by(rank)
for k in {1,2,4,...} until ranks are unique:
  orderSecond <- [n-k..n-1] + [sa[j]-k where sa[j]>=k]
  SA <- counting_sort_by(rank[orderSecond])
  rerank by pairs (rank[i], rank[i+k] or 0)

LCP:
rankInSa[sa[i]] <- i
h <- 0
for i in [0..n-1]:
  if rankInSa[i]==0: h<-0; continue
  j <- sa[rankInSa[i]-1]
  while s[i+h]==s[j+h]: h++
  lcp[rankInSa[i]] <- h
  if h>0: h--
```

## 복잡도
- 시간: SA O(n log n), LCP O(n)
- 공간: O(n)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static vector<int> buildSuffixArray(const string& s) {
    int n = (int)s.size();
    vector<int> sa(n), rankCurrent(n), rankPrev(n), counting(max(256, n) + 1, 0);

    // Initial ranking by single characters (shifted to 1..256, sentinel 0 reserved)
    for (int i = 0; i < n; i++) rankCurrent[i] = (unsigned char)s[i] + 1;

    // Initial SA by counting sort on first key (characters)
    fill(counting.begin(), counting.end(), 0);
    for (int i = 0; i < n; i++) counting[rankCurrent[i]]++;
    for (int i = 1; i < (int)counting.size(); i++) counting[i] += counting[i - 1];
    for (int i = n - 1; i >= 0; i--) sa[--counting[rankCurrent[i]]] = i;

    // Doubling
    int maxRank = max(256, n);
    for (int k = 1; k < n; k <<= 1) {
        // Sort by second key via induced ordering
        int p = 0;
        for (int i = n - k; i < n; i++) rankPrev[p++] = i;               // suffixes with empty second part
        for (int i = 0; i < n; i++) if (sa[i] >= k) rankPrev[p++] = sa[i] - k;

        // Counting sort by first key (rankCurrent)
        fill(counting.begin(), counting.end(), 0);
        for (int i = 0; i < n; i++) counting[rankCurrent[rankPrev[i]]]++;
        for (int i = 1; i <= maxRank; i++) counting[i] += counting[i - 1];
        for (int i = n - 1; i >= 0; i--) sa[--counting[rankCurrent[rankPrev[i]]]] = rankPrev[i];

        // Re-rank
        rankPrev.swap(rankCurrent);
        rankCurrent[sa[0]] = 1;
        p = 1;
        for (int i = 1; i < n; i++) {
            int a = sa[i - 1], b = sa[i];
            int a1 = rankPrev[a], b1 = rankPrev[b];
            int a2 = (a + k < n) ? rankPrev[a + k] : 0;
            int b2 = (b + k < n) ? rankPrev[b + k] : 0;
            if (a1 == b1 && a2 == b2) {
                rankCurrent[b] = p;
            } else {
                rankCurrent[b] = ++p;
            }
        }
        maxRank = p;
        if (p == n) break;
    }
    return sa;
}

static vector<int> buildLCP(const string& s, const vector<int>& sa) {
    int n = (int)s.size();
    vector<int> rankInSa(n), lcp(n, 0);
    for (int i = 0; i < n; i++) rankInSa[sa[i]] = i;

    int h = 0;
    for (int i = 0; i < n; i++) {
        int r = rankInSa[i];
        if (r == 0) { h = 0; continue; }
        int j = sa[r - 1];
        while (i + h < n && j + h < n && s[i + h] == s[j + h]) h++;
        lcp[r] = h;
        if (h > 0) h--;
    }
    return lcp;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    if (!(cin >> s)) return 0;
    int n = (int)s.size();

    vector<int> sa = buildSuffixArray(s);
    vector<int> lcp = buildLCP(s, sa);

    // Output SA (1-based)
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << (sa[i] + 1);
    }
    cout << '\n';

    // Output LCP with leading 'x'
    cout << 'x';
    for (int i = 1; i < n; i++) {
        cout << ' ' << lcp[i];
    }
    cout << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- 길이 1 문자열, 모든 문자가 동일한 문자열(예: `aaaaa`)
- 전부 서로 다른 문자(예: `abcdefg`), 반복 패턴(예: `abababab`)
- 사전순 경계(작은/큰 문자 교차), 접두사/접미사 포함관계가 많은 경우
- 매우 긴 입력(최대 5e5)에서 시간/메모리 여유 확인

## 제출 전 점검
- 출력 형식: SA 1-based, LCP 첫 항은 `x`
- 오버플로 없음(int로 충분), 인덱스 범위와 경계(빈 두 번째 키는 0)
- 초기화/리셋 누락 없음, 표준 입출력 최적화 활성화

## 참고자료
- [Suffix array - Wikipedia](https://en.wikipedia.org/wiki/Suffix_array)
- [Kasai algorithm for LCP - cp-algorithms](https://cp-algorithms.com/string/suffix-array.html#kasai)


