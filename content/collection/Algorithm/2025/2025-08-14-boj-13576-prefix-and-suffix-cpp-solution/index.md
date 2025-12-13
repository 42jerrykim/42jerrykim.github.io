---
title: "[Algorithm] C++ 백준 13576번: Prefix와 Suffix"
description: "문자열의 접두사이자 접미사인 모든 경계(보더)를 찾고, 각 길이가 부분 문자열로 등장하는 횟수를 구합니다. KMP 접두사함수(π)로 경계 사슬을 추출하고, π 누적 분포로 등장수를 계산하여 l 오름차순으로 출력합니다. O(n) 구현과 정당성·엣지케이스를 정리했습니다."
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
- Problem-13576
- cpp
- C++
- Implementation
- 구현
- String
- 문자열
- String Matching
- 문자열 매칭
- KMP
- 접두사함수
- Prefix Function
- Prefix-Function
- Pi Array
- 파이배열
- Failure Function
- 실패함수
- Border
- 경계
- Prefix
- 접두사
- Suffix
- 접미사
- Prefix equals Suffix
- 접두사=접미사
- Occurrence Counting
- 등장 횟수
- Substring
- 부분 문자열
- Counting
- 카운팅
- Accumulation
- 누적
- Chain of Borders
- 경계 사슬
- Z-Algorithm
- Z 알고리즘
- Linear Time
- 선형시간
- O(n)
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
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Data Structures
- 자료구조
- Implementation Details
- 구현 디테일
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13576
- 요약: 문자열 `S`에 대해 접두사이면서 접미사인 모든 길이 `l`을 찾아, 각 길이가 부분 문자열로 등장하는 횟수 `c`를 함께 출력한다. 결과는 `l` 오름차순.

### 제한/스펙
- `1 ≤ |S| ≤ 100,000`
- 시간 제한 2초, 메모리 제한 512MB → 선형 시간 알고리즘 필요

## 입출력

예제 입력 1
```
ABACABA
```

예제 출력 1
```
3
1 4
3 2
7 1
```

예제 입력 2
```
AAA
```

예제 출력 2
```
3
1 3
2 2
3 1
```

## 접근 개요(아이디어 스케치)
- 핵심 관찰: 접두사와 접미사가 같은 길이 `l`은 접두사함수(π) 사슬을 따라 `l = n, π[n-1], π[π[n-1]-1], ...`로 얻을 수 있다.
- 등장 횟수: 각 위치 `i`에서 `π[i]` 값이 의미하는 길이의 접두사가 그 위치까지의 접미사와 일치하므로 `cnt[π[i]]++`. 이후 `cnt`를 경계 길이의 상위에서 하위로 누적해 작은 경계들의 등장횟수에 반영하고, 각 접두사 자체의 1회 등장을 더하면 전체 부분 문자열 등장수 `c[l]`을 얻는다.
- 알고리즘: (1) π 배열 계산, (2) `cnt` 누적, (3) 경계 길이 모아 정렬 후 `(l, c[l])` 출력. 전체 `O(n)`.

## 알고리즘 설계
1) 접두사함수 `π[i]`: `S[0..i]`의 가장 긴 경계 길이. KMP 전처리로 선형 시간 계산.
2) 등장수 카운팅:
   - `for i in [0..n-1]: cnt[π[i]]++`
   - `for len from n down to 1: cnt[π[len-1]] += cnt[len]`
   - `for l in [1..n]: cnt[l]++` (각 접두사 자체가 전체 문자열에서 1회 등장)
3) 경계 수집: `borders = []`, `k=n`에서 시작해 `k>0` 동안 `borders.push(k); k=π[k-1]`. 정렬 후 길이 오름차순 출력.

## 복잡도
- 시간: `O(n)`
- 공간: `O(n)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    if (!(cin >> s)) return 0;
    int n = (int)s.size();

    // 1) KMP prefix function (pi)
    vector<int> pi(n, 0);
    for (int i = 1; i < n; ++i) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) ++j;
        pi[i] = j;
    }

    // 2) Count occurrences of each prefix as a substring
    vector<long long> cnt(n + 1, 0);
    for (int i = 0; i < n; ++i) cnt[pi[i]]++;
    for (int len = n; len > 0; --len) cnt[pi[len - 1]] += cnt[len];
    for (int l = 1; l <= n; ++l) cnt[l]++; // count the prefix itself

    // 3) Collect all borders (prefix == suffix)
    vector<int> borders;
    for (int k = n; k > 0; k = pi[k - 1]) borders.push_back(k);
    sort(borders.begin(), borders.end());

    cout << borders.size() << '\n';
    for (int len : borders) cout << len << ' ' << cnt[len] << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- `|S|=1`: 경계는 길이 1 하나, 등장수 1.
- 모든 문자가 동일(`"aaaa..."`): 모든 길이가 경계이며 등장수는 `n-l+1` 형태로 증가.
- 경계가 전혀 없는 경우(`"abc"` 등): 길이 `n`만 경계.
- 반복 패턴(`"ababab"`, `"abcababcab"`): π 사슬이 여러 계층으로 이어지는지 확인.
- 큰 입력(최대 1e5): 선형 시간 구현, 불필요한 복사/출력 버퍼링 주의.

## 제출 전 점검
- π 계산 루프의 경계 조건과 while 탈출 조건 확인.
- `cnt` 누적 순서: 큰 길이에서 작은 길이로 전달되는지 확인.
- 출력 정렬: 길이 오름차순인지 확인.
- 64비트 누적(`long long`) 사용해 등장수 합산 시 오버플로 방지.

## 참고자료/유사문제
- KMP / Prefix-function 설명: cp-algorithms “Prefix function”
- BOJ 4354 “문자열 제곱”, 1786 “찾기” 등 KMP 응용 문제


