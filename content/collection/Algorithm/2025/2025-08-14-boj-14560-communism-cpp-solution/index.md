---
title: "[Algorithm] cpp 백준 14560번: Communism - 합차 제한 MITM"
description: "세 사람에게 N≤30개의 일을 배분할 때 아드와 래리 보수 합의 차이가 D를 넘지 않도록 하는 가짓수를 구한다. 전수탐색 대신 절반 분할, 남은 절대합 기반 가지치기, 정렬·이분탐색으로 O(3^(N/2))에 해결."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Brute Force
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-14560
- 14560
- Communism
- cpp
- C++
- Meet-in-the-Middle
- Meet in the Middle
- 미들미들
- 반으로 나누기
- 부분합
- 브루트포스
- 완전탐색
- 조합 탐색
- 가지치기
- pruning
- 두 포인터
- two pointers
- 이분 탐색
- binary search
- 정렬
- sorting
- 시간복잡도
- Time Complexity
- 공간복잡도
- Space Complexity
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
- Implementation
- 구현
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Greedy
- 그리디
- Dynamic Programming
- 동적계획법
- Graph
- 그래프
- Tree
- 트리
- BFS
- DFS
- Shortest Path
- 최단경로
- Dijkstra
- 다익스트라
- Segment Tree
- 세그먼트 트리
- Fenwick Tree
- 펜윅트리
- Disjoint Set Union
- 유니온파인드
- Binary Search
- 이분탐색
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Hashing
- 해싱
- String
- 문자열
- Geometry
- 기하
- Math
- 수학
- Modulo
- 모듈러
- Debugging
- 디버깅
- 세 사람 분배
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/14560
- 요약: N(≤30)개의 일을 린카루/아드/래리 세 사람에게 나눌 때, 아드와 래리의 총보수 합의 차이가 D를 넘지 않도록 하는 배분의 수를 구한다.
- 제한: N ≤ 30, 1 ≤ A_i ≤ 10^16, 0 ≤ D ≤ 10^18, 시간 1초, 메모리 512MB

## 입력/출력
```
<입력>
N
A1 A2 ... AN
D

<출력>
조건을 만족하는 서로 다른 배분 가짓수
```

예제 1
```
입력
3
1 2 3
1

출력
9
```

예제 2
```
입력
3
1 2 3
0

출력
3
```

## 접근 개요
- 각 일을 누구에게 주는지는 세 가지: 린카루(차이 0), 아드(차이 +A_i), 래리(차이 −A_i).
- 전체 배분은 (아드−래리) 차이 s에 대해 |s| ≤ D를 만족해야 한다. 린카루에게 가는 일은 차이 계산에 영향이 없다.
- N ≤ 30에서 3^N 전탐색은 불가능하므로, 반으로 나누어(meet-in-the-middle) 각 절반에서 만들 수 있는 차이 값을 생성한다.
- 한쪽 리스트를 정렬한 뒤, 다른 쪽의 값 x에 대해 s2 ∈ [−D−x, D−x]인 원소 수를 이분 탐색으로 더한다.

## Mermaid로 보는 흐름
```mermaid
flowchart TD
  A[일 목록 A] --> B[절반 분할 L/R]
  B --> C[왼쪽 L: (아드-래리) 가능한 합 S1 생성]
  B --> D[오른쪽 R: (아드-래리) 가능한 합 S2 생성]
  C --> E[S2 정렬]
  D --> E
  E --> F[각 x∈S1에 대해 S2에서 -D-x..D-x 범위 개수 합산]
  F --> G[정답]
```

## 알고리즘 설계
- 상태: 각 원소 A_i를 {0, +A_i, −A_i} 중 하나로 더한 누적값 s(=아드−래리).
- 분할: 정렬로 |A_i| 큰 것부터 배치해 강한 가지치기를 유도하고, 15/15로 분할.
- 가지치기(pruning): 인덱스 i 이후 남은 절대합 rem과 상대 절반의 절대합 other를 이용해, 가능한 최종 s의 구간 [cur−rem, cur+rem]이 [−D−other, D+other]와 교집합이 없으면 탐색 중단.
- 집계: S2만 정렬. 각 x∈S1에 대해 이분 탐색으로 S2에서 [−D−x, D−x] 개수를 더한다.
- 특수 처리: D ≥ sum(A)면 모든 배분이 유효이므로 3^N을 즉시 출력.

## 복잡도
- 시간: O(3^(N/2) log 3^(N/2)) ≈ O(3^(N/2)·N) + 가지치기 효과로 더 빠름.
- 공간: O(3^(N/2)) 리스트 두 개 저장.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

static inline long long pow3(int n){
    long long r = 1;
    for(int i=0;i<n;i++) r *= 3LL;
    return r;
}

static void gen_with_prune(
    const vector<long long>& vals,
    const vector<long long>& suffixAbs,
    int idx,
    long long cur,
    long long otherAbsSum,
    long long D,
    vector<long long>& out
){
    long long rem = suffixAbs[idx];
    if (cur - rem >  D + otherAbsSum) return;
    if (cur + rem < -D - otherAbsSum) return;

    if (idx == (int)vals.size()){
        out.push_back(cur);
        return;
    }
    gen_with_prune(vals, suffixAbs, idx+1, cur, otherAbsSum, D, out);          // Lin
    gen_with_prune(vals, suffixAbs, idx+1, cur + vals[idx], otherAbsSum, D, out); // Ad
    gen_with_prune(vals, suffixAbs, idx+1, cur - vals[idx], otherAbsSum, D, out); // Larry
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if(!(cin >> N)) return 0;
    vector<long long> A(N);
    for(int i=0;i<N;i++) cin >> A[i];
    long long D; cin >> D;

    long long totalAbs = 0;
    for(long long v: A) totalAbs += v;
    if(D >= totalAbs){
        cout << pow3(N) << '\n';
        return 0;
    }

    sort(A.begin(), A.end(), [](long long x, long long y){
        return llabs(x) > llabs(y);
    });
    int n1 = N/2;
    int n2 = N - n1;
    vector<long long> L(A.begin(), A.begin()+n1), R(A.begin()+n1, A.end());

    long long sumAbsL = 0, sumAbsR = 0;
    for(long long v: L) sumAbsL += llabs(v);
    for(long long v: R) sumAbsR += llabs(v);

    vector<long long> suffL(n1+1, 0), suffR(n2+1, 0);
    for(int i=n1-1;i>=0;i--) suffL[i] = suffL[i+1] + llabs(L[i]);
    for(int i=n2-1;i>=0;i--) suffR[i] = suffR[i+1] + llabs(R[i]);

    size_t capL = 1, capR = 1;
    for(int i=0;i<n1;i++) capL *= 3;
    for(int i=0;i<n2;i++) capR *= 3;
    vector<long long> S1; S1.reserve(capL);
    vector<long long> S2; S2.reserve(capR);

    gen_with_prune(L, suffL, 0, 0LL, sumAbsR, D, S1);
    gen_with_prune(R, suffR, 0, 0LL, sumAbsL, D, S2);

    sort(S2.begin(), S2.end());

    long long ans = 0;
    for(long long x: S1){
        long long lo = -D - x;
        long long hi =  D - x;
        auto itL = lower_bound(S2.begin(), S2.end(), lo);
        auto itR = upper_bound(S2.begin(), S2.end(), hi);
        ans += (long long)(itR - itL);
    }

    cout << ans << '\n';
    return 0;
}
```

## 구현 (Python, 스켈레톤)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from bisect import bisect_left, bisect_right

def main():
    input = sys.stdin.readline
    N = int(input().strip())
    A = list(map(int, input().split()))
    D = int(input().strip())
    # 동일한 아이디어로 구현 가능. C++ 버전을 참고.
    # 시간 제한상 파이썬은 PyPy에서만 통과 가능할 수 있음.
    pass

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- D ≥ sum(A): 모든 배분 가능 → 3^N.
- D = 0: (아드−래리)=0인 경우만 유효.
- 큰 수 A_i(최대 1e16), D(최대 1e18): 64-bit 정수 사용 및 오버플로 주의.
- 동일 가중치 다수: 카운팅 중복 여부는 범위 이분탐색로 정확히 처리.

## 제출 전 점검
- 표준 입력/출력, 개행/공백 형식 확인.
- 64-bit 정수 사용(long long).
- 분할/정렬 후 가지치기 분기 누락 여부 점검.

## 참고자료/유사문제
- meet-in-the-middle 기법 개요: 부분집합 합, 3-way 분배 문제군.

