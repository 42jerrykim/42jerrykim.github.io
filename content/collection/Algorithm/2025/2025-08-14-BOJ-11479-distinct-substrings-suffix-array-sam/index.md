---
title: "[Algorithm] cpp-python 백준 11479번: 서로 다른 부분 문자열의 개수"
description: "문자열 S의 서로 다른 부분 문자열 개수를 효율적으로 구합니다. 접미사 배열+LCP(카사이)로 n(n+1)/2−ΣLCP를 계산하거나 접미사 자동자(SAM)로 상태 길이 차 합을 이용해 O(n)에 해결합니다. 경계·중복 처리와 구현 포인트를 정리했습니다."
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
- Problem-11479
- cpp
- python
- C++
- Python
- String
- 문자열
- Distinct Substrings
- 서로 다른 부분 문자열
- Suffix Array
- 접미사배열
- SA
- Doubling
- Radix Sort
- Counting Sort
- LCP
- 최장공통접두사
- Kasai
- 카사이
- Suffix Automaton
- 접미사 자동자
- SAM
- Endpos Equivalence
- endpos 등가류
- Automaton
- 자동자
- Data Structures
- 자료구조
- Implementation
- 구현
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
- Template
- 템플릿
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Hashing
- 해싱
- Binary Search
- 이분탐색
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Geometry
- 기하
- Math
- 수학
- Modulo
- 모듈러
- Implementation Details
- 구현 디테일
- LPSA
- 접두사
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/11479
- 요약: 문자열 `S`가 주어졌을 때, 서로 다른 부분 문자열의 개수를 구합니다. 전체 부분 문자열 수 `n(n+1)/2`에서 중복을 제거해야 합니다.

### 제한/스펙
- 길이 `n`은 입력 조건에 따라 충분히 큼(집합으로는 불가) → 선형 또는 `O(n log n)` 솔루션 필요
- 시간 제한/메모리 제한: 대입력 기준 통과 가능한 접미사 배열/자동자 권장

## 입출력
```
입력
ababa

출력
9
```

```
입력
aaa

출력
3
```

## 접근 개요
- 핵심 관찰: 서로 다른 부분 문자열의 개수 = 모든 접미사를 사전순 정렬했을 때, 이웃 접미사 간 LCP의 합을 전체 부분 문자열 수에서 뺀 값.
- 두 가지 대표 해법
  - 접미사 배열 + LCP(Kasai): 정렬 `O(n log n)`(더블링) + LCP `O(n)` → 합산으로 계산.
  - 접미사 자동자(SAM): 각 상태의 `len(state) − len(link(state))`의 합이 서로 다른 부분 문자열 수와 같음 → 전체 `O(n)`.

## 알고리즘 설계
- 접미사 배열
  - 랭크 더블링으로 길이 `2^k` 접두사 기준 정렬. 최종 SA를 얻은 뒤 Kasai 알고리즘으로 LCP 배열을 `O(n)`에 계산.
  - 정당성: 인접 접미사 LCP의 누적 합이 중복 개수의 총합과 동일함. 전체 부분 문자열 수 `n(n+1)/2`에서 이를 빼면 서로 다른 개수.
- 접미사 자동자
  - 상태 전이(알파벳 개수)에 대해 확장하며 최대 일치 길이(`len`)와 접미 링크(`link`)를 유지.
  - 정당성: 각 상태는 endpos 등가류를 대표하며, 그 상태가 새로 만든 서로 다른 부분 문자열의 수는 `len(v) − len(link(v))`.

## 복잡도
- 접미사 배열: 시간 `O(n log n)`, 공간 `O(n)`
- 접미사 자동자: 시간 `O(n)`, 공간 `O(n)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s; if(!(cin >> s)) return 0;
    int n = (int)s.size();
    vector<int> sa(n), rnk(n), tmp(n);
    for(int i=0;i<n;i++){ sa[i]=i; rnk[i]=(unsigned char)s[i]; }

    for(int k=1;;k<<=1){
        auto cmp = [&](int a, int b){
            if(rnk[a]!=rnk[b]) return rnk[a]<rnk[b];
            int ra = a+k<n ? rnk[a+k] : -1;
            int rb = b+k<n ? rnk[b+k] : -1;
            return ra<rb;
        };
        sort(sa.begin(), sa.end(), cmp);
        tmp[sa[0]] = 0;
        for(int i=1;i<n;i++) tmp[sa[i]] = tmp[sa[i-1]] + (cmp(sa[i-1], sa[i])?1:0);
        for(int i=0;i<n;i++) rnk[i]=tmp[i];
        if(rnk[sa[n-1]]==n-1) break;
    }

    vector<int> pos(n), lcp(n);
    for(int i=0;i<n;i++) pos[sa[i]] = i;
    int h=0;
    for(int i=0;i<n;i++){
        int r = pos[i];
        if(r==0) continue;
        int j = sa[r-1];
        while(i+h<n && j+h<n && s[i+h]==s[j+h]) h++;
        lcp[r]=h;
        if(h) h--;
    }

    long long total = 1LL*n*(n+1)/2;
    long long sumLcp = 0;
    for(int i=1;i<n;i++) sumLcp += lcp[i];
    cout << (total - sumLcp) << '\n';
    return 0;
}
```

## 구현 (Python, Suffix Automaton)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys

def count_distinct_substrings(s: str) -> int:
    # SAM arrays
    max_states = 2 * len(s)
    link = [-1] * max_states
    length = [0] * max_states
    # transitions as dict per state for simplicity; can be optimized
    nexts = [dict() for _ in range(max_states)]

    size = 1  # number of states
    last = 0  # active state

    for ch in s:
        c = ch
        cur = size
        size += 1
        length[cur] = length[last] + 1
        p = last
        while p != -1 and c not in nexts[p]:
            nexts[p][c] = cur
            p = link[p]
        if p == -1:
            link[cur] = 0
        else:
            q = nexts[p][c]
            if length[p] + 1 == length[q]:
                link[cur] = q
            else:
                clone = size
                size += 1
                length[clone] = length[p] + 1
                nexts[clone] = nexts[q].copy()
                link[clone] = link[q]
                while p != -1 and nexts[p].get(c, -1) == q:
                    nexts[p][c] = clone
                    p = link[p]
                link[q] = link[cur] = clone
        last = cur

    # sum over states (exclude state 0's contribution being 0)
    total = 0
    for v in range(1, size):
        total += length[v] - length[link[v]]
    return total

def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    print(count_distinct_substrings(data))

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- 빈 문자열(입력에서 미제공) 또는 길이 1 → 결과 1
- 모든 문자가 동일한 경우(`aaaa...`) → 결과 `n`
- 모든 문자가 서로 다른 경우 → 결과 `n(n+1)/2`
- 아스키/유니코드 입력 시 Python SAM은 딕셔너리 전이로 안전

## 제출 전 점검
- C++: 입출력 버퍼 설정, 정렬 비교자와 랭크 갱신의 일관성, `long long` 누적
- LCP 인덱스: `lcp[0]=0`, 합산은 `i=1..n-1`
- Python: SAM 클론 생성 시 전이 복사, 상태 수 `≤ 2n`

## 참고자료
- 접미사 배열/카사이 알고리즘 개요와 LCP 누적 아이디어
- 접미사 자동자(SAM) 기본 성질: `sum(len[v] − len[link[v]])`


