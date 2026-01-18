---
title: "[Algorithm] C++ 백준 18874번: Haircut"
description: "페닉윅 트리(Fenwick Tree)로 각 임계값(j=0..N-1)에 대해 배열 최댓값을 j로 제한했을 때 역위(inversion) 개수를 효율적으로 계산한다. O(N^2 log N) 풀이로 최악의 경우 O(N log N) 단일 쿼리를 N번 수행한다."
date: 2026-01-05
lastmod: 2026-01-05
categories:
- "Algorithm"
- "Data Structure"
- "Fenwick Tree"
- "Inversion"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "Baekjoon"
- "백준"
- "18874"
- "BOJ-18874"
- "Haircut"
- "Hair"
- "Inversion"
- "역위"
- "Inversion Count"
- "역위 개수"
- "Fenwick Tree"
- "펜윅 트리"
- "Binary Indexed Tree"
- "BIT"
- "이진 인덱스 트리"
- "Data Structure"
- "자료구조"
- "Segment Tree"
- "세그먼트 트리"
- "Range Query"
- "범위 쿼리"
- "Point Update"
- "점 업데이트"
- "Prefix Sum"
- "누적합"
- "USACO"
- "USA Computing Olympiad"
- "Gold"
- "골드"
- "Difficulty"
- "난이도"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Problem Solving"
- "문제해결"
- "Coding Test"
- "코딩테스트"
- "C++"
- "CPP"
- "GNU++17"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "O(N^2 log N)"
- "O(N log N)"
- "Edge Case"
- "엣지 케이스"
- "Thresholding"
- "임계값 처리"
- "Array Modification"
- "배열 수정"
- "Clamping"
- "값 제한"
- "Counting Inversions"
- "역위 세기"
- "Pair Analysis"
- "쌍 분석"
- "USACO 2020"
- "2020 US Open"
- "Open Contest"
image: "wordcloud.png"
---

각 임계값 \(j = 0, 1, \ldots, N-1\)에 대해 배열의 원소를 \(j\) 이상으로 제한(clamping)한 뒤, 그 배열에서 역위(inversion) 개수를 구하는 문제다.
\(N\)이 최대 \(10^5\)이고 각 임계값마다 쿼리를 해야 하므로, **페닉윅 트리(Fenwick Tree)**를 이용한 \(O(N \log N)\) 역위 계산을 활용한다.

## 문제 정보

**문제 링크**: [https://www.acmicpc.net/problem/18874](https://www.acmicpc.net/problem/18874)

**문제 요약**:
- \(N\)개 원소로 이루어진 배열 \(A\)가 주어진다 (\(0 \le A_i \le N\)).
- 각 \(j = 0, 1, \ldots, N-1\)에 대해, \(A\)의 모든 원소를 \(\min(A_i, j)\)로 대체한 배열의 **역위 개수**를 구한다.
- 역위: \(i < i'\)이면서 \(A_i > A_{i'}\)인 쌍 \((i, i')\)의 개수

**제한 조건**:
- 시간 제한: 1초
- 메모리 제한: 512MB
- \(1 \le N \le 10^5\)
- \(0 \le A_i \le N\)

## 입출력 예제

**입력 1**:

```text
5
5 2 3 3 0
```

**출력 1**:

```text
0
4
4
5
7
```

**설명**: 
- \(j=0\): \([0,0,0,0,0]\) → 역위 0
- \(j=1\): \([1,1,1,1,0]\) → 역위 4 (인덱스 4보다 앞의 모든 원소가 더 크므로)
- \(j=2\): \([2,2,2,2,0]\) → 역위 4
- \(j=3\): \([3,2,3,3,0]\) → 역위 5 (i=0,2,3,4 다 포함)
- \(j=4\): \([4,2,3,3,0]\) → 역위 7

## 접근 방식

### 핵심 관찰: 페닉윅 트리로 각 \(j\)마다 역위를 \(O(N \log N)\)에 계산

**역위 정의 재해석**: 배열을 왼쪽에서 오른쪽으로 훑으면서, 각 위치 \(i\)에서 값 \(v = \min(A_i, j)\)를 봤을 때, "이미 본 원소 중 \(v\)보다 큰 개수"를 센다.

**Fenwick Tree 활용**:
1. 값 범위를 0~N으로 정규화 (이미 주어진 범위)
2. 배열을 왼쪽부터 훑으면서:
   - 현재 값 \(v = \min(A_i, j)\)에 대해
   - Fenwick Tree에서 쿼리: "\(v+1\)~N 범위의 개수" (즉, 값이 \(v\)보다 큰 원소 개수)
   - 그 개수를 역위 카운트에 더한다
   - Fenwick Tree에 \(v\)에 대한 카운트를 +1 업데이트

### 알고리즘 설계 (Mermaid Flowchart)

```mermaid
flowchart TD
    A["입력: N, 배열 A[0..N-1]"] --> B["각 j=0 to N-1 반복"]
    B --> C["Fenwick Tree 초기화"]
    C --> D["i=0 to N-1 반복"]
    D --> E["v = min(A[i], j)"]
    E --> F["쿼리: FW.sum(v+1) = v보다 큰 원소 개수"]
    F --> G["inversions += 쿼리 결과"]
    G --> H["업데이트: FW.add(v+1, 1)"]
    H --> I{"i < N?"}
    I -- "yes" --> D
    I -- "no" --> J["inversions 출력"]
    J --> K{"j < N-1?"}
    K -- "yes" --> B
    K -- "no" --> L["완료"]
```

### 구현 포인트

- **값 범위**: \(0 \le \min(A_i, j) \le j \le N-1\)이므로 Fenwick Tree 크기는 N이면 충분
- **쿼리**: "값 \(v\)보다 큰 원소 개수" = \(\text{sum}(v+1, N)\)
- **정규화**: 원본 배열이 이미 0~N 범위이므로 추가 정규화 불필요
- **오버플로우**: 역위 개수가 최대 \(\binom{N}{2} = \frac{N(N-1)}{2}\)이므로 \(10^5 \cdot 10^5 / 2 \approx 5 \times 10^9\)로 `long long` 필수

## 복잡도 분석

| 항목 | 복잡도 | 비고 |
|---|---|---|
| **시간 복잡도** | \(O(N^2 \log N)\) | 각 임계값 \(j\)마다 \(O(N \log N)\) 역위 계산 |
| **공간 복잡도** | \(O(N)\) | Fenwick Tree 배열 |

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **j=0** | 모든 원소가 0이 됨 | 역위 0 (같은 값들) |
| **모두 같은 값** | \(A = [k, k, k, \ldots]\) | \(j \ge k\)일 때 모두 같으므로 역위 0 |
| **감소 수열** | \(A = [N-1, N-2, \ldots, 0]\) | 최대 역위 \(\binom{N}{2}\) |
| **오버플로우** | 역위 개수가 \(2^{31}-1\) 초과 | `long long` 사용 |
| **j 범위** | \(j\)는 0부터 N-1까지 (N은 제외) | 반복 범위 주의 |

## 구현 코드 (C++)

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    int n;
    vector<long long> bit;
    Fenwick(int n = 0) : n(n), bit(n + 1, 0) {}
    void add(int i, long long v) { // 1-indexed
        for (; i <= n; i += i & -i) bit[i] += v;
    }
    long long sum(int i) const { // sum [1..i]
        long long r = 0;
        for (; i > 0; i -= i & -i) r += bit[i];
        return r;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;
    vector<int> A(N);
    for (int i = 0; i < N; i++) {
        cin >> A[i];
        if (A[i] > N - 1) A[i] = N - 1; // clamp to [0, N-1]
    }

    Fenwick fw(N);
    vector<long long> cnt(N, 0);

    // Precompute: for each value v, count inversions at all thresholds >= v
    for (int i = 0; i < N; i++) {
        int v = A[i];              // 0..N-1
        long long le = fw.sum(v + 1);  // elements with value <= v
        long long larger = i - le; // previous elements > v (these form inversions)
        cnt[v] += larger;
        fw.add(v + 1, 1);
    }

    // Answer: for each j, sum inversions from all thresholds <= j
    long long cur = 0;
    for (int j = 0; j <= N - 1; j++) {
        cout << cur << "\n";
        cur += cnt[j];
    }
    return 0;
}
```

## 마무리

이 문제는 단순히 "역위를 N번 세기"로 접근할 수 있지만, 중요한 최적화 포인트는 **이미 계산한 역위 정보를 재활용**하는 것이다.

각 임계값 \(j\)에서 신규로 추가되는 역위는 "값이 정확히 \(j\)인 원소들"이 기여하는 부분뿐이므로, 값별로 먼저 역위 카운트를 계산한 뒤 누적합을 이용하는 방식이 효율적이다.

Fenwick Tree 외에도 Merge Sort 기반 역위 계산이나 좌표 압축 후 세그먼트 트리를 사용할 수도 있지만, 페닉윅 트리가 가장 간결하고 구현하기 쉽다.

## 참고 문헌 및 출처

- [백준 18874번 문제](https://www.acmicpc.net/problem/18874)
- [USACO 2020 US Open Contest, Gold Division](http://www.usaco.org/)
