---
title: "[Algorithm] C++ 백준 13974번: 파일 합치기 2"
description: "연속한 파일만 합칠 수 있을 때 최소 비용을 구하는 구간 DP 문제입니다. dp[i][j]=min(dp[i][k]+dp[k+1][j])+sum(i..j)에 크누스 최적화를 적용해 O(N^2)로 해결합니다. 누적합으로 구간합을 O(1)로 계산하며 64비트 정수, 메모리 사용에 유의합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Dynamic Programming
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-13974
- cpp
- C++
- Dynamic Programming
- 동적계획법
- Interval DP
- 구간 DP
- Knuth Optimization
- 크누스 최적화
- Quadrangle Inequality
- 사각 부등식
- Monge Array
- 몽주 배열
- Prefix Sum
- 누적합
- Range Sum
- 구간합
- File Merge
- 파일 합치기
- File Merging
- Optimal Merge (Ordered)
- DP Optimization
- 최적화
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Data Structures
- 자료구조
- Arrays
- 배열
- Long Long
- 64-bit Integer
- Fast IO
- 입출력 최적화
- Memory Optimization
- 메모리 최적화
- O(N^2)
- 512MB Limit
- Problem Solving
- 문제해결
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13974
- 요약: 크기가 주어진 K개의 장(파일)을 연속성이 유지되도록 두 개씩 합쳐 한 개가 될 때까지 진행한다. 두 파일을 합칠 때의 비용은 두 파일 크기의 합이며, 전체 최소 비용을 구한다.

### 제한/스펙
- 테스트케이스 `T`
- `3 ≤ K ≤ 5000`, 각 파일 크기 `1..10000`
- 시간 6초, 메모리 512MB

## 입출력 형식/예제

예제 입력 1
```
2
4
40 30 30 50
15
1 21 3 4 5 35 5 4 3 5 98 21 14 17 32
```

예제 출력 1
```
300
864
```

## 접근 개요(아이디어 스케치)
- 구간 DP 기본형: `dp[i][j] = min_{i≤k<j}( dp[i][k] + dp[k+1][j] ) + sum(i..j)`
- 구간 합 `sum(i..j)`는 누적합으로 O(1) 계산.
- 이 문제의 비용 구조는 사각 부등식(Quadrangle Inequality)을 만족해 최적 분할점이 단조(모노톤)하게 이동한다. 이에 따라 크누스 최적화 적용이 가능하여 `k` 탐색 구간을 `opt[i][j-1]..opt[i+1][j]`로 줄여 전체 시간복잡도를 `O(N^2)`로 낮춘다.

```mermaid
flowchart TD
  A[파일 크기 a1..aK] --> B[누적합 prefix]
  B --> C[구간합 sum(i..j) = prefix[j]-prefix[i-1]]
  C --> D[dp[i][j] = min(dp[i][k]+dp[k+1][j]) + sum(i..j)]
  D --> E[opt[i][j] ∈ [opt[i][j-1], opt[i+1][j]]]
  E --> F[O(N^2)로 채우기]
```

## 알고리즘 설계
- 상태: `dp[i][j]` = i..j를 하나로 합치는 최소 비용, `opt[i][j]` = 해당 최소를 만드는 분할점 k.
- 점화식: 위와 동일. 길이 1 구간은 비용 0, `opt[i][i]=i`로 시작.
- 전개 순서: 구간 길이 `len=2..K`, 시작점 `i=1..K-len+1`, 끝점 `j=i+len-1`.
- 탐색 범위 축소: `k ∈ [opt[i][j-1], opt[i+1][j]]`만 확인.
- 합계 계산: `sum(i..j)=prefix[j]-prefix[i-1]`.

## 복잡도
- 시간: `O(K^2)` (크누스 최적화). `K=5000`에서도 C++로 충분.
- 공간: `O(K^2)` — `dp`(8바이트) + `opt`(4바이트) ≈ 300MB 내외. 512MB 제한 내에서 동작.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; if(!(cin >> T)) return 0;
    while(T--){
        int K; cin >> K;
        vector<long long> a(K + 1), prefix(K + 1, 0);
        for(int i = 1; i <= K; ++i){
            cin >> a[i];
            prefix[i] = prefix[i - 1] + a[i];
        }

        const long long INF = (1LL << 62);
        vector<vector<long long>> dp(K + 2, vector<long long>(K + 2, 0));
        vector<vector<int>> opt(K + 2, vector<int>(K + 2, 0));
        for(int i = 1; i <= K; ++i) opt[i][i] = i;

        for(int len = 2; len <= K; ++len){
            for(int i = 1; i + len - 1 <= K; ++i){
                int j = i + len - 1;
                long long sum = prefix[j] - prefix[i - 1];
                dp[i][j] = INF;

                int L = opt[i][j - 1];
                int R = opt[i + 1][j];
                if(L > R) swap(L, R);

                for(int k = L; k <= R; ++k){
                    long long cand = dp[i][k] + dp[k + 1][j] + sum;
                    if(cand < dp[i][j]){
                        dp[i][j] = cand;
                        opt[i][j] = k;
                    }
                }
            }
        }

        cout << dp[1][K] << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- 동일 크기 다수: 최적 분할점 단조 성질로 안전함.
- 큰 합계: 누적합과 답은 64비트(`long long`).
- K가 큰 경우(5000): 메모리 사용량을 고려해 전역/정적 대형 배열 대신 벡터 사용(둘 다 가능). 입출력 가속 필수.
- T>1: 각 테스트마다 `dp/opt`를 새로 생성하여 상태 누수 방지.

## 제출 전 점검
- `sum(i..j)` 계산 인덱스 범위 재확인(`prefix[j]-prefix[i-1]`).
- `opt` 초기화 및 탐색 범위(`opt[i][j-1]..opt[i+1][j]`).
- 빠른 입출력 설정(속도).
- 64비트 정수 사용으로 오버플로 방지.

## 참고자료/유사문제
- 크누스 최적화(Quadrangle Inequality) 개요 문헌, BOJ 11066(파일 합치기)와의 비교.


