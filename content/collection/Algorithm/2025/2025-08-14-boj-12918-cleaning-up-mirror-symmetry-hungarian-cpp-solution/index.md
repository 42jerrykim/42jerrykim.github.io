---
title: "[Algorithm] C++ 백준 12918번: 정리정돈"
description: "헝가리안 알고리즘으로 대칭 쌍 매칭을 최소화해 이동 거리 합의 최솟값을 구합니다. 비용을 √((xi+xj)^2+(yi−yj)^2)로 정의해 할당 최적화 후 2로 나누어 답을 얻습니다. 증명·엣지·복잡도·C++ 구현 포함"
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Geometry
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-12918
- cpp
- C++
- Geometry
- 기하
- Euclidean Distance
- 유클리드 거리
- Symmetry
- 대칭
- Mirror
- 좌우대칭
- Assignment Problem
- 할당 문제
- Hungarian Algorithm
- 헝가리안 알고리즘
- Minimum Cost
- 최소 비용
- Perfect Matching
- 완전 매칭
- Bipartite Matching
- 이분 매칭
- Matching
- 매칭
- Optimization
- 최적화
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
- Math
- 수학
- Modulo
- 모듈러
- Debugging
- 디버깅
- 정리정돈
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/12918
- 요약: 점 N개의 좌표가 주어질 때, 최종 배치가 y축에 대해 선대칭이 되도록 각 물건을 이동한다. 이동 거리 합의 최솟값을 유클리드 거리 기준으로 구한다.
- 제한: N ≤ 100, 좌표는 정수 |x|,|y| ≤ 1000, 점 중복 없음, 시간 2초.

## 입력/출력
```
입력: N, 이어서 N개의 (x, y)
출력: 최소 이동 거리 합을 소수점 셋째 자리에서 반올림하여 출력
```

## 접근 개요
- 핵심 관찰(반사 트릭): 두 점 p=(x1,y1), q=(x2,y2)를 서로 대칭인 위치로 보낼 때 최소 이동 합은 |p − mirror(q)|와 같음. 여기서 mirror(q)=(-x2, y2).
- 따라서 모든 점을 짝지어(자기 자신 포함 가능, 즉 y축 위 배치) 쌍마다 비용 w(i,j)=√((xi+xj)^2+(yi−yj)^2)를 더하면 전체 최소 이동 합이 됨.
- 전체 최적화는 "점들을 쌍으로 묶는 최소 비용 완전 매칭" 문제와 동일. 이를 헝가리안 알고리즘(할당 문제)로 풀 수 있으며, 할당 최솟값을 2로 나누면 답이 된다.

## 알고리즘 설계
1. 점들을 1..N으로 번호 매김.
2. 비용 행렬 C를 구성: C[i][j] = √((xi + xj)^2 + (yi − yj)^2).
3. C에 대해 헝가리안 알고리즘(할당 문제, O(N^3)) 수행 → 최적 값 costAssign.
4. 최종 정답 = costAssign / 2.0.
   - 이유: 각 쌍(i,j)은 대칭 두 점으로 보내는 비용이 동일하게 두 번 카운트되므로(방향 i→mirror(j), j→mirror(i)), 총합을 2로 나눔.
5. 고정소수점(세 자리)으로 출력.

### 올바름 근거(스케치)
- 반사 원리: |p − P'| + |q − Q'| 최소이며 Q'=mirror(P')일 때, mirror(q)=q*에 대해 |p − P'| + |q − Q'| = |p − P'| + |q* − P'| ≥ |p − q*|. 등호는 P'가 선분 p–q* 위에 있을 때 성립.
- 따라서 쌍 (i,j)의 최소 비용은 w(i,j)=|pi − mirror(pj)|.
- 전체는 쌍들의 합을 최소화하는 완전 매칭 문제이며, 대칭 카운팅 특성상 할당 최솟값의 1/2가 최적합이 된다.

## 복잡도
- 시간: O(N^3) (헝가리안 알고리즘), N ≤ 100이면 충분.
- 공간: O(N^2).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using ld = long double;

ld hungarian(const vector<vector<ld>>& a) {
    int n = (int)a.size() - 1;
    const ld INF = 1e100L;

    vector<ld> u(n + 1, 0), v(n + 1, 0), minv(n + 1);
    vector<int> p(n + 1), way(n + 1);

    for (int i = 1; i <= n; ++i) {
        p[0] = i;
        int j0 = 0;
        vector<char> used(n + 1, false);
        fill(minv.begin(), minv.end(), INF);
        do {
            used[j0] = true;
            int i0 = p[j0], j1 = 0;
            ld delta = INF;
            for (int j = 1; j <= n; ++j) if (!used[j]) {
                ld cur = a[i0][j] - u[i0] - v[j];
                if (cur < minv[j]) {
                    minv[j] = cur;
                    way[j] = j0;
                }
                if (minv[j] < delta) {
                    delta = minv[j];
                    j1 = j;
                }
            }
            for (int j = 0; j <= n; ++j) {
                if (used[j]) {
                    u[p[j]] += delta;
                    v[j] -= delta;
                } else {
                    minv[j] -= delta;
                }
            }
            j0 = j1;
        } while (p[j0] != 0);
        do {
            int j1 = way[j0];
            p[j0] = p[j1];
            j0 = j1;
        } while (j0 != 0);
    }

    ld value = 0;
    for (int j = 1; j <= n; ++j) value += a[p[j]][j];
    return value;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    vector<pair<ld, ld>> pt(N + 1);
    for (int i = 1; i <= N; ++i) {
        ld x, y; cin >> x >> y;
        pt[i] = {x, y};
    }

    vector<vector<ld>> cost(N + 1, vector<ld>(N + 1, 0));
    for (int i = 1; i <= N; ++i) {
        for (int j = 1; j <= N; ++j) {
            ld dx = pt[i].first + pt[j].first;   // xi - (-xj)
            ld dy = pt[i].second - pt[j].second; // yi - yj
            cost[i][j] = sqrtl(dx * dx + dy * dy);
        }
    }

    ld match_cost = hungarian(cost);
    ld answer = match_cost / 2.0L;

    cout.setf(std::ios::fixed);
    cout << setprecision(3) << (double)answer << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- 홀수 개의 점: 최적 해에서는 최소 한 점이 y축 위로 이동(자기-짝 처리), 비용은 |x|로 반영됨(공식에서 i=j일 때 2|x|/2).
- y=축 위 점(x=0): 그대로 두어도 0 비용. 다른 점과 짝지어 더 유리하면 그렇게 매칭됨.
- 같은 y, 반대 x에 가까운 점들: 서로 짝이 되어 거의 0 비용 가능.
- 큰 좌표 범위: `long double`로 누적 오차 감소, 최종 출력은 소수 셋째 자리 반올림.

## 제출 전 점검
- 입출력 형식/개행 확인, 고정 소수점 3자리 출력.
- 64-bit/부동소수 연산: `long double` 사용, `sqrtl` 호출.
- N=1,2 등의 최소 케이스 수기 점검.

## 참고자료
- BOJ 12918 정리정돈: https://www.acmicpc.net/problem/12918
- Assignment(Hungarian) 알고리즘 개요: https://e-maxx.ru/algo/assignment_hungary (영문/러시아어)

