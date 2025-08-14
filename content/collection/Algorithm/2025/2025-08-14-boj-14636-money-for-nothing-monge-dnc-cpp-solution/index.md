---
title: "[Algorithm] cpp 백준 14636번: Money for Nothing - Monge DnC"
description: "생산자/소비자 후보를 정렬·중복 제거해 비지배 전처리로 파레토 경계를 만들고, 원점 변환된 점집합의 Monge 구조를 이용해 분할정복 최적화로 (e−d)*(q−p) 최대 이익을 계산합니다. 계약 불가 케이스는 0 처리, i128로 오버플로를 방지하며 엣지 케이스 점검을 포함합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Divide and Conquer
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-14636
- cpp
- C++
- Greedy
- 그리디
- Divide and Conquer
- 분할정복
- Divide and Conquer Optimization
- 분할정복 최적화
- Monge
- Monge Array
- Totally Monotone Matrix
- 완전단조행렬
- Pareto Frontier
- 파레토 프론티어
- Non-dominated
- 비지배점
- Envelope
- 경계선
- Sorting
- 정렬
- Two-phase Filtering
- 2단계 전처리
- Optimization
- 최적화
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Complexity Analysis
- 복잡도 분석
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
- Invariant
- 불변식
- Fast IO
- 빠른 입출력
- Overflow
- 오버플로
- __int128
- 128bit
- Long Long
- long long
- Coordinate Compression
- 좌표 압축
- Profit Maximization
- 이익 최대화
- ICPC
- World Finals
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/14636
- 요약: 하나의 생산자 회사와 하나의 소비자 회사를 골라, 생산 시작일 `d` 이후부터 소비자 마감 다음날 `e` 전까지(즉 `e > d`), 하루 1개씩 공급하여 총 이익 `(e - d) * (q - p)`를 최대화합니다. 여기서 `p`는 생산 단가, `q`는 소비 단가이며 `q > p`여야 계약이 유효합니다. 유효한 쌍이 없으면 0을 출력합니다. 제약: \(1 \le m,n \le 5\times 10^5\), 값들은 \(\le 10^9\).

## 입력/출력
```
<입력>
m n
p1 d1
...
pm dm
q1 e1
...
qn en

<출력>
최대 가능한 총 이익 (없으면 0)
```

## 접근 개요
- 핵심 관찰: 수익은 `(e - d) * (q - p)`. 따라서 `d`가 작을수록, `p`가 낮을수록, `e`가 클수록, `q`가 높을수록 유리합니다. 동일 날짜에서 더 비싼 `p`는 지배되며, 동일 날짜에서 더 낮은 `q`는 지배됩니다.
- 비지배 전처리(파레토 경계):
  - 생산자 `(d, p)`: `d` 오름차순으로 정렬 후 같은 날짜는 `p` 최소만 남기고, `d`가 증가할수록 `p`가 엄격히 감소하도록 필터링(오른쪽으로 갈수록 더 싸짐)합니다.
  - 소비자 `(e, q)`: `e` 오름차순 정렬 후 같은 날짜는 `q` 최대만 남기고, 뒤에서부터 스윕하여 `e`가 증가할수록 `q`가 엄격히 증가하도록 필터링(오른쪽으로 갈수록 더 비쌈)합니다.
- 이후 남는 두 단조 수열 `D[i]`(증가), `P[i]`(감소), `E[j]`(증가), `Q[j]`(증가)에서 `E[j] > D[i]` 및 `Q[j] > P[i]`일 때만 `(E[j]-D[i])*(Q[j]-P[i])` 후보가 됩니다.
- 점수 행렬 `Score[i][j] = (E[j]-D[i])*(Q[j]-P[i])`는 완전단조 성질(행별 최적 `j*`가 단조)로 분할정복 최적화가 가능합니다. 이를 이용해 전체 최대값을 효율적으로 탐색합니다.

```mermaid
flowchart TB
  A[입력 m,n 및 (p,d),(q,e)] --> B[정렬·중복축약]
  B --> C[비지배 전처리로 파레토 경계 구축]
  C --> D[단조 수열 D,P,E,Q 확보]
  D --> E[분할정복 최적화로 행별 최적 열 j* 탐색]
  E --> F[유효쌍만 고려하여 최대 수익 계산]
```

## 알고리즘
1) 생산자 처리: `d` 오름차순 정렬 → 같은 `d`는 `p` 최솟값만 유지 → 왼→오로 스윕하며 `p`가 더 작을 때만 남김.
2) 소비자 처리: `e` 오름차순 정렬 → 같은 `e`는 `q` 최댓값만 유지 → 오른→왼으로 스윕하며 `q`가 증가할 때만 남김(역순 뒤집기).
3) 분할정복 최적화(DnC): 중간 행 `im`에 대해 열 구간 `[jl..jr]`에서 최적 열 `bestJ`를 찾고, 좌/우 재귀에 각각 `[jl..bestJ]`, `[bestJ..jr]`로 탐색 구간을 좁혀가며 전역 최대를 갱신합니다. 실제 정답 갱신 시에는 `E[j] > D[i]`, `Q[j] > P[i]`만 인정합니다.
4) 안전성: 곱 중간값은 `~(2e9)*(2e9)` 가능하므로 `__int128`으로 계산, 최종 출력은 64비트로 캐스팅. 유효쌍이 없으면 0.

## 복잡도
- 시간: 정렬 및 전처리 `O((m+n) log(m+n))`, 분할정복 탐색 `O(I log J)`~`O(I + J)` 수준(실무에서는 선형에 가깝게 동작). 전체 대략 `O((m+n) log(m+n))`.
- 공간: 입력과 전처리 벡터 `O(m+n)`.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
using i128 = __int128_t;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n;
    if (!(cin >> m >> n)) return 0;

    vector<pair<int64,int64>> rawProd; rawProd.reserve(m); // (d, p)
    for (int i = 0; i < m; ++i) {
        int64 p, d; cin >> p >> d;
        rawProd.emplace_back(d, p);
    }

    vector<pair<int64,int64>> rawCons; rawCons.reserve(n); // (e, q)
    for (int j = 0; j < n; ++j) {
        int64 q, e; cin >> q >> e;
        rawCons.emplace_back(e, q);
    }

    // Producers: sort by d asc, keep minimal p per d, then keep non-dominated (p strictly decreasing as d increases)
    sort(rawProd.begin(), rawProd.end()); // by d, then p
    vector<pair<int64,int64>> prodByD; prodByD.reserve(rawProd.size());
    for (size_t i = 0; i < rawProd.size(); ) {
        int64 d = rawProd[i].first;
        int64 minp = rawProd[i].second;
        size_t j = i + 1;
        while (j < rawProd.size() && rawProd[j].first == d) {
            minp = min(minp, rawProd[j].second);
            ++j;
        }
        prodByD.emplace_back(d, minp);
        i = j;
    }
    vector<pair<int64,int64>> P; P.reserve(prodByD.size());
    for (auto &pp : prodByD) {
        if (P.empty() || pp.second < P.back().second) P.push_back(pp);
    }
    if (P.empty()) { cout << 0 << '\n'; return 0; }

    // Consumers: sort by e asc, keep maximal q per e, then keep non-dominated maxima (q strictly increasing as e increases after reverse pass)
    sort(rawCons.begin(), rawCons.end()); // by e, then q
    vector<pair<int64,int64>> consByE; consByE.reserve(rawCons.size());
    for (size_t i = 0; i < rawCons.size(); ) {
        int64 e = rawCons[i].first;
        int64 maxq = rawCons[i].second;
        size_t j = i + 1;
        while (j < rawCons.size() && rawCons[j].first == e) {
            maxq = max(maxq, rawCons[j].second);
            ++j;
        }
        consByE.emplace_back(e, maxq);
        i = j;
    }
    // Build consumers frontier with q strictly increasing as e increases.
    // On ties of q, keep the later (larger e) point.
    vector<pair<int64,int64>> C; C.reserve(consByE.size());
    for (const auto &eq : consByE) {
        if (C.empty() || eq.second > C.back().second) {
            C.push_back(eq);
        } else if (eq.second == C.back().second) {
            C.back().first = eq.first; // keep larger e for the same q
        }
    }
    if (C.empty()) { cout << 0 << '\n'; return 0; }

    const int I = (int)P.size();
    const int J = (int)C.size();

    vector<int64> D(I), PP(I), E(J), Q(J);
    for (int i = 0; i < I; ++i) { D[i] = P[i].first; PP[i] = P[i].second; }
    for (int j = 0; j < J; ++j) { E[j] = C[j].first; Q[j] = C[j].second; }

    auto solve = [&](auto&& self, int il, int ir, int jl, int jr, int64 &answer) -> void {
        if (il > ir || jl > jr) return;
        int im = (il + ir) >> 1;

        i128 bestScore = (i128)LLONG_MIN;
        int bestJ = jl;

        for (int j = jl; j <= jr; ++j) {
            // For divide-and-conquer splitting (Monge), use raw score (can be negative)
            i128 sc = (i128)(E[j] - D[im]) * (i128)(Q[j] - PP[im]);
            if (sc > bestScore) {
                bestScore = sc;
                bestJ = j;
            }
            // For actual profit, only count valid contracts: e > d and q > p
            if (E[j] > D[im] && Q[j] > PP[im]) {
                i128 prof = (i128)(E[j] - D[im]) * (i128)(Q[j] - PP[im]);
                if (prof > (i128)answer) answer = (int64)prof;
            }
        }

        self(self, il, im - 1, jl, bestJ, answer);
        self(self, im + 1, ir, bestJ, jr, answer);
    };

    int64 ans = 0;
    solve(solve, 0, I - 1, 0, J - 1, ans);
    cout << ans << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- `e <= d` 또는 `q <= p`인 쌍은 배제되어야 함(수익 0 이하). 전처리 후에도 최종 갱신 시 조건 확인.
- 동일 날짜 다수: 생산자는 같은 `d`에서 `p` 최소만, 소비자는 같은 `e`에서 `q` 최대만 유지.
- 모든 쌍이 무효: 정답 0.
- 극단값(최대 1e9) 곱: 중간 계산은 `__int128`로 처리.

## 제출 전 점검
- 입출력: 빠른 IO 설정 확인.
- 전처리: 단조 수열 여부(`P`의 `p`는 감소, `C`의 `q`는 증가) 재확인.
- 정답 갱신: `E[j] > D[i] && Q[j] > PP[i]` 조건을 반드시 동반.

## 참고자료/유사문제
- ICPC World Finals 2017 D - Money for Nothing (문제 출처)


