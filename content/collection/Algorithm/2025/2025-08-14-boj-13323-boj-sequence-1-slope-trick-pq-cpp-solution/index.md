---
title: "[Algorithm] C++ 백준 13323번: BOJ 수열 1 - Slope Trick"
description: "수열 B가 엄격히 증가하도록 하면서 |B_i−A_i|의 합을 최소화하는 문제. A_i−i로 변환해 비내림 수열 적합 문제로 줄이고, 최대 힙으로 중간값을 유지하는 slope trick을 적용해 O(N log N)로 해결한다. 32비트 범위, 경계·반례까지 점검한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Greedy"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-13323"
- "cpp"
- "C++"
- "Python"
- "Data Structures"
- "자료구조"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Optimization"
- "최적화"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Editorial"
- "에디토리얼"
- "Code Review"
- "코드리뷰"
- "Template"
- "템플릿"
- "Testing"
- "테스트"
- "Complexity Analysis"
- "복잡도 분석"
- "Invariant"
- "불변식"
- "Greedy"
- "그리디"
- "Dynamic Programming"
- "동적계획법"
- "Graph"
- "그래프"
- "Tree"
- "트리"
- "BFS"
- "DFS"
- "Shortest Path"
- "최단경로"
- "Dijkstra"
- "다익스트라"
- "Segment Tree"
- "세그먼트 트리"
- "Fenwick Tree"
- "펜윅트리"
- "Disjoint Set Union"
- "유니온파인드"
- "Binary Search"
- "이분탐색"
- "Two Pointers"
- "투포인터"
- "Sliding Window"
- "슬라이딩윈도우"
- "Hashing"
- "해싱"
- "String"
- "문자열"
- "Geometry"
- "기하"
- "Math"
- "수학"
- "Modulo"
- "모듈러"
- "Implementation Details"
- "구현 디테일"
- "Slope Trick"
- "Median"
- "중앙값"
- "Priority Queue"
- "우선순위 큐"
- "Heap"
- "힙"
- "Monotone"
- "단조"
- "비내림"
- "L1"
- "절댓값 합"
- "BOJ 수열 1"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13323
- 요약: 수열 `A`가 주어질 때, 정수 수열 `B`를 `B1 < B2 < ... < BN` (엄격 증가)로 만들면서 `∑|Bi − Ai|`의 최솟값을 구한다. `B`는 32비트 정수 범위를 만족해야 한다.
- 제한/스펙: `1 ≤ N ≤ 1,000,000`, `0 ≤ Ai ≤ 2×10^9`, 답은 64비트 정수 범위 사용 권장.

## 입력/출력
```
입력
7
9 4 8 20 14 15 18

출력
13
```

## 접근 개요
- 핵심 관찰: `B`가 엄격 증가이면 `C'i = Bi − i`는 비내림(= 단조 증가 허용) 수열이 된다.
- 변형: `Ci = Ai − i`로 바꾸면 `∑|Bi − Ai| = ∑|C'i − Ci|`. 즉, "비내림 수열에의 L1 적합" 문제가 된다.
- 해법 스케치: prefix마다 `Ci`들의 중앙값이 최적이며, 비내림 제약은 중앙값이 내려가지 않도록 보정해야 한다. 최대 힙 하나로 "현재 허용 가능한 중앙값 상한"을 유지하고, 위반 시 상단을 `Ci`로 낮추며 차이를 더한다. 이는 slope trick의 전형 패턴이다.

## 알고리즘 설계
- 자료구조: 최대 힙 `H` (C++ `priority_queue<long long>`)
- 절차:
  1) 순서대로 `Ci = Ai − i`를 `H`에 삽입한다.
  2) 만약 `top(H) > Ci`라면, `ans += top(H) − Ci`, `H.pop()` 후 `Ci`를 다시 `H`에 넣는다.
  3) 위 보정은 중앙값(또는 그 이상)을 낮춰 비내림 제약을 만족시키는 연산이며, 그 비용이 최소임을 보장한다.
- 정당성 요약:
  - L1 최소합에서 최적 해는 각 prefix에 대해 중앙값을 선택한다.
  - 비내림 제약으로 중앙값이 감소하려 할 때만 보정이 필요하며, 감소량만큼의 차이 합이 불가피하다.
  - 힙 상단만 조정하면 전체 제약이 유지된다(국소 보정 → 전역 적합).

### 의사코드
```
ans = 0
H = empty max-heap
for i in 1..N:
    Ci = Ai - i
    push(H, Ci)
    if top(H) > Ci:
        ans += top(H) - Ci
        pop(H)
        push(H, Ci)
print(ans)
```

## 복잡도
- 시간: O(N log N) (힙 연산)
- 공간: O(N) (최악의 경우 힙에 N개)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; 
    if(!(cin >> N)) return 0;
    priority_queue<long long> pq; // max-heap for C = A - i
    long long answer = 0;
    for(long long i = 1; i <= N; ++i){
        long long A; cin >> A;
        long long C = A - i;
        pq.push(C);
        if(pq.top() > C){
            answer += pq.top() - C;
            pq.pop();
            pq.push(C);
        }
    }
    cout << answer;
    return 0;
}
```

## 코너 케이스 체크리스트
- `N=1` 단일 원소
- 이미 엄격 증가인 경우(보정 0)
- 모든 값 동일/감소(보정 다수)
- 큰 값/경계: `Ai=0`, `Ai=2×10^9`, `N=10^6`
- 오버플로: 누적 합은 64비트 사용

## 제출 전 점검
- 입력 빠짐/개행, `long long` 사용, 인덱스 `i`는 1-base로 `A−i` 계산
- 힙 위반 시에만 보정 수행 확인
- I/O 최적화(`sync_with_stdio(false)`, `tie(nullptr)`) 적용

## 참고자료
- Slope Trick — 비내림/비비증 수열에 대한 L1 최적화의 대표 기법
- 문제: BOI 2004 변형. 중앙값 유지 + 제약 보정 아이디어


