---
title: "[Algorithm] C++ 백준 18186번: 라면 사기 (Large)"
description: "인접 공장 묶음 구매(2·3연속)와 단건 구매 단가를 비교해 그리디로 좌→우 처리한다. B≤C면 전부 단건, B>C면 2연속 선처리(불균형 보정) 후 3연속, 그다음 2연속, 단건 순으로 소진하여 최소 비용을 달성한다. 시간 O(N)."
date: 2025-09-04
lastmod: 2025-09-04
categories:
- Algorithm
- Greedy
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-18186
- cpp
- C++
- Greedy
- 그리디
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
- Simulation
- 시뮬레이션
- Cost Minimization
- 비용 최소화
- Adjacent Purchase
- 인접 구매
- Ramen
- 라면
- Large
- Large-Variant
- Greedy Strategy
- 그리디 전략
- Purchase Bundling
- 묶음 구매
- Local-Global Optimality
- 국소 전역 최적
- Early Decision
- 선결정
- Array Processing
- 배열 처리
- Linear Scan
- 선형 스캔
- Industrial Plants
- 공장
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/18186
- 요약: N개 공장에서 각자 필요한 수량을 최소 비용으로 구매. 단건(B), 인접 2연속(B+C), 인접 3연속(B+2C) 구매를 조합한다.

## 입력/출력
```text
<입력>
N B C
A1 A2 ... AN
```
```text
<출력>
최소 비용
```

## 접근 개요
- B≤C이면 인접 묶음이 이득이 없어 전부 단건 구매가 최적.
- B>C이면 좌→우 순회하며 (a[i+1] > a[i+2])인 불균형 구간에서 2연속을 일부 먼저 적용해 3연속 적용량을 극대화.
- 이후 3연속 → 남은 2연속 → 단건 순으로 처리.

## 알고리즘
- 배열 a를 길이 N+2로 패딩.
- i=0..N-1 순회 중:
  - if a[i+1] > a[i+2]: t2 = min(a[i], a[i+1] - a[i+2]); a[i] -= t2; a[i+1] -= t2; cost += (B+C)*t2
  - t3 = min(a[i], a[i+1], a[i+2]); 소진 및 비용 가산
  - t2 = min(a[i], a[i+1]); 소진 및 비용 가산
  - 잔여 a[i]는 단건 비용 가산

## 복잡도
- 시간: O(N)
- 공간: O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main(){ios::sync_with_stdio(false);cin.tie(nullptr);
    int n; long long B,C; if(!(cin>>n>>B>>C)) return 0; 
    vector<long long>a(n+2); for(int i=0;i<n;++i) cin>>a[i];
    long long ans=0;
    if(B<=C){
        for(int i=0;i<n;++i) ans += a[i]*B; 
        cout<<ans<<'\n'; return 0;
    }
    for(int i=0;i<n;++i){
        if(a[i+1]>a[i+2]){
            long long t2=min(a[i], a[i+1]-a[i+2]);
            if(t2>0){a[i]-=t2; a[i+1]-=t2; ans += (B+C)*t2;}
        }
        long long t3=min(a[i], min(a[i+1], a[i+2]));
        if(t3>0){a[i]-=t3; a[i+1]-=t3; a[i+2]-=t3; ans += (B+2*C)*t3;}
        long long t2=min(a[i], a[i+1]);
        if(t2>0){a[i]-=t2; a[i+1]-=t2; ans += (B+C)*t2;}
        if(a[i]>0){ ans += B*a[i]; a[i]=0; }
    }
    cout<<ans<<'\n';
    return 0;}
```

## 코너 케이스 체크리스트
- B≤C, B>C 극단값
- a[i]=0 구간 연속
- a[i+1]≤a[i+2] 및 a[i+1]>a[i+2] 혼재
- N=3 최소 길이, 최대 입력

## 참고자료
- BOJ 18186 라면 사기 (Large)


