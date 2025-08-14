---
title: "[Algorithm] cpp 백준 5466번: 상인"
description: "IOI 2009 상인 문제. 집 S에서 출발·복귀하며 U/D 비용으로 강을 오르내리며 시장을 방문해 이익 합을 최대로 한다. 날짜별 비내림 방문 제약을 활용해 좌/우 이동 비용을 선형식으로 흡수한 최대 변환과 같은 날 내부 양방향 스위핑 DP를 결합, 좌표압축+펜윅 트리로 O(N log N) 최적 이익을 계산한다."
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
- Problem-5466
- cpp
- C++
- Data Structures
- 자료구조
- Fenwick Tree
- 펜윅트리
- Binary Indexed Tree
- BIT
- Coordinate Compression
- 좌표압축
- DP
- 동적계획법
- Day Grouping
- 날짜 그룹화
- Sweep
- 스위핑
- Max Transform
- 최대 변환
- Prefix Max
- 접두 최대
- Suffix Max
- 접미 최대
- Greedy
- 그리디
- Optimization
- 최적화
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
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Sorting
- 정렬
- IOI
- IOI 2009
- Merchant
- 상인
- Danube
- 도나우강
- Cost Model
- 비용모델
- Affine Transform
- 아핀 변환
- Range Query
- 구간 쿼리
- Prefix/Suffix (Concept)
- 개념 정리
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Testing
- 테스트
- Invariant
- 불변식
- Binary Search
- 이분탐색
- Segment Tree
- 세그먼트 트리
- Math
- 수학
- Modulo
- 모듈러
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/5466
- 요약: 집 `S`에서 출발해 강을 따라 여러 시장을 날짜 순으로 방문하고 다시 집으로 돌아온다. 강을 거슬러갈 때 미터당 `U`, 내려갈 때 미터당 `D` 비용이 들며, 각 시장을 방문하면 이익 `M`을 얻는다. 방문 순서 제약(날짜 비내림) 하에서 최종 이익의 최댓값을 구한다.

### 제한/스펙
- `1 ≤ N ≤ 500000`
- `1 ≤ D ≤ U ≤ 10`, `1 ≤ S ≤ 500001`
- `1 ≤ T_k ≤ 500000`, `1 ≤ L_k ≤ 500001`, `1 ≤ M_k ≤ 4000`
- 시간 제한 1초, 메모리 128MB → `O(N log N)` 설계 필요

## 입출력 형식/예제
- 입력: `N U D S`, 이어서 `N`개의 줄에 `T L M`
- 출력: 여행 종료 후 얻을 수 있는 최대 이익(정수)

예제 입력 1
```
4
5 3 100
2 80 100
20 125 130
10 75 150
5 120 110
```

예제 출력 1
```
50
```

## 접근 개요(아이디어 스케치)
- 날짜가 다르면 방문 순서는 날짜 오름차순으로 강제된다. 같은 날(`T` 동일)에는 순서가 자유로워 “같은 날 내부”에서 여러 시장을 연속 방문해 이익을 누적할 수 있다.
- 임의의 위치 `x`에서 `y`로 이동 비용은 방향에 따라 `U|x−y|` 또는 `D|x−y|`로 비대칭이다. 이를 선형식으로 흡수하면, “이전 날 종료 위치들의 최적값”에서 “오늘 특정 위치 `p`로 진입”하는 최댓값을 두 개의 변환으로 빠르게 얻을 수 있다.
- 좌표압축 후, 이전 날까지의 최적값 `base[i]`(압축 인덱스 `i` 위치에서 오늘 시작 직전의 최대 이익)를 유지하면서, 다음을 미리 준비한다:
  - `leftFenwick`: 각 위치 `i`에 `base[i] + D*pos[i]`를 저장해 `j`까지의 prefix 최대를 질의
  - `rightFenwick`: 역인덱스에 `base[i] - U*pos[i]`를 저장해 `j+1..P` 구간의 최대를 질의
- 이렇게 얻은 오늘의 “진입 최적값” `H[k]`들을 기반으로, 같은 날 내부에서의 방문은 두 번의 스위핑으로 커버된다:
  - 왼→오른 스윕: 내려가며(`D`) 누적 이익을 더한 경우의 최댓값 `V1`
  - 오른→왼 스윕: 올라가며(`U`) 누적 이익을 더한 경우의 최댓값 `V2`
- `newBase = max(V1, V2)`로 오늘 방문 후 각 위치의 최적값을 갱신하고, 이를 트리에 반영한다. 마지막에 임의 위치에서 집 `S`로 귀환 비용을 빼 최댓값을 취한다.

```mermaid
flowchart TD
  A[입력 N, U, D, S, (T,L,M)] --> B[좌표압축: S와 모든 L]
  B --> C[아이템을 (T, L_idx) 기준 정렬]
  C --> D[날짜별 그룹 처리]
  D --> E[H[k] 계산: max(leftPrefix, rightSuffix)]
  E --> F[같은 날 내부: 좌→우 스윕으로 V1]
  E --> G[같은 날 내부: 우→좌 스윕으로 V2]
  F --> H[newBase = max(V1, V2)로 갱신]
  G --> H
  H --> I[펜윅 트리 두 개에 반영]
  I --> D
  D --> J[모든 날 처리 후 종료]
  J --> K[모든 위치 p에 대해 base[p] - cost(p→S) 최댓값]
```

## 알고리즘 설계
- 상태 정의(좌표압축 후 `P`개 위치):
  - `base[i]`: 오늘 시작 직전, 위치 `i`에서의 최대 이익(집 복귀 비용은 아직 미차감)
  - `leftFenwick`에 `base[i] + D*pos[i]` 저장 → `≤ idx` prefix 최대
  - `rightFenwick`에 `base[i] - U*pos[i]` 저장(역인덱스) → `> idx` suffix 최대
- 오늘 날짜 그룹 내 정렬: 같은 날 시장들은 `idx`(좌표) 오름차순으로 정렬해 처리
- 진입값 `H[k]`(오늘 들어와서 위치 `pos[k]`에 서기 직전 최대 이익):
  - `H[k] = max( max_{i≤idx} (base[i] + D*pos[i]) - D*pos[k], max_{i>idx} (base[i] - U*pos[i]) + U*pos[k] )`
- 같은 날 내부 누적(이익 `M`들의 누적합 `pref`):
  - 좌→우: `V1[b] = pref[b] - D*pos[b] + max_{a≤b}( H[a] - pref[a-1] + D*pos[a] )`
  - 우→좌: `V2[a] = U*pos[a] - pref[a-1] + max_{b≥a}( H[b] - U*pos[b] + pref[b] )`
- 갱신: `base[idx_k] = max(base[idx_k], max(V1[k], V2[k]))`를 모두 반영하고 두 펜윅에 업데이트
- 종료: 답은 `max_p base[p] - cost(p→S)` 와 `0` 중 큰 값(아무 시장도 방문하지 않는 선택 가능)

## 복잡도
- 시간: `O(N log N)` (정렬 + 펜윅 질의/갱신)
- 공간: `O(N)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct FenwickMax {
    int n;
    vector<long long> bit;
    static constexpr long long NEG_INF = -(1LL<<60);
    FenwickMax() {}
    FenwickMax(int n): n(n), bit(n+1, NEG_INF) {}
    void init(int n_) { n = n_; bit.assign(n+1, NEG_INF); }
    void update(int idx, long long val) {
        for (int i = idx; i <= n; i += i & -i) bit[i] = max(bit[i], val);
    }
    long long query(int idx) const {
        long long res = NEG_INF;
        for (int i = idx; i > 0; i -= i & -i) res = max(res, bit[i]);
        return res;
    }
};

struct Item {
    int day;
    int idx;
    int pos;
    int profit;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, U, D, S;
    if (!(cin >> N >> U >> D >> S)) return 0;

    vector<Item> items; items.reserve(N);
    vector<int> coords; coords.reserve(N + 1); coords.push_back(S);

    for (int i = 0; i < N; ++i) {
        int T, L, M; cin >> T >> L >> M;
        items.push_back({T, 0, L, M});
        coords.push_back(L);
    }

    sort(coords.begin(), coords.end());
    coords.erase(unique(coords.begin(), coords.end()), coords.end());
    int P = (int)coords.size();
    auto get_idx = [&](int x){ return int(lower_bound(coords.begin(), coords.end(), x) - coords.begin()) + 1; };
    for (auto &it : items) it.idx = get_idx(it.pos);
    int S_idx = get_idx(S);

    sort(items.begin(), items.end(), [](const Item& a, const Item& b){
        if (a.day != b.day) return a.day < b.day;
        return a.idx < b.idx;
    });

    const long long NEG_INF = -(1LL<<60);
    vector<long long> base(P+1, NEG_INF);
    base[S_idx] = 0;

    FenwickMax fenwLeft(P), fenwRight(P);
    fenwLeft.update(S_idx, base[S_idx] + 1LL*D*coords[S_idx-1]);
    fenwRight.update(P - S_idx + 1, base[S_idx] - 1LL*U*coords[S_idx-1]);

    int i = 0;
    while (i < N) {
        int j = i, curDay = items[i].day;
        while (j < N && items[j].day == curDay) ++j;

        int m = j - i;
        vector<int> idxs(m+1), pos(m+1), profit(m+1);
        for (int k = 1; k <= m; ++k) {
            idxs[k] = items[i + k - 1].idx;
            pos[k] = items[i + k - 1].pos;
            profit[k] = items[i + k - 1].profit;
        }

        vector<long long> H(m+1, NEG_INF);
        for (int k = 1; k <= m; ++k) {
            int idx = idxs[k];
            long long leftBest = fenwLeft.query(idx);
            long long rightBest = fenwRight.query(P - idx);
            long long cand = NEG_INF;
            if (leftBest != NEG_INF) cand = max(cand, leftBest - 1LL*D*pos[k]);
            if (rightBest != NEG_INF) cand = max(cand, rightBest + 1LL*U*pos[k]);
            H[k] = cand;
        }

        vector<long long> pref(m+1, 0);
        for (int k = 1; k <= m; ++k) pref[k] = pref[k-1] + profit[k];

        vector<long long> V1(m+1, NEG_INF);
        long long prefBest = NEG_INF;
        for (int b = 1; b <= m; ++b) {
            long long T1 = H[b] - pref[b-1] + 1LL*D*pos[b];
            prefBest = max(prefBest, T1);
            V1[b] = pref[b] - 1LL*D*pos[b] + prefBest;
        }

        vector<long long> V2(m+1, NEG_INF);
        long long suffBest = NEG_INF;
        for (int a = m; a >= 1; --a) {
            long long T2 = H[a] - 1LL*U*pos[a] + pref[a];
            suffBest = max(suffBest, T2);
            V2[a] = 1LL*U*pos[a] - pref[a-1] + suffBest;
        }

        for (int k = 1; k <= m; ++k) {
            int idx = idxs[k];
            long long newBase = max(V1[k], V2[k]);
            if (newBase > base[idx]) {
                base[idx] = newBase;
                fenwLeft.update(idx, base[idx] + 1LL*D*pos[k]);
                fenwRight.update(P - idx + 1, base[idx] - 1LL*U*pos[k]);
            }
        }

        i = j;
    }

    long long ans = 0;
    for (int p = 1; p <= P; ++p) {
        if (base[p] == NEG_INF) continue;
        long long cost = (coords[p-1] <= S) ? 1LL*D*(S - coords[p-1]) : 1LL*U*(coords[p-1] - S);
        ans = max(ans, base[p] - cost);
    }
    cout << ans << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- 아무 시장도 방문하지 않는 선택(답 `0`)이 유리한 경우
- 같은 날에 매우 많은 시장이 몰린 경우: 두 스윕의 누적/인덱스 처리 검증
- `S`가 어떤 시장 좌표보다 왼쪽/오른쪽에 치우친 경우의 방향별 비용 처리
- `U=D`인 대칭 비용, `U`와 `D`가 작아 이익 누적이 쉽지 않은 경우
- 좌표압축 시 `S` 포함 여부(필수)

## 제출 전 점검
- 날짜별 그룹 경계에서만 `base`→`H` 계산, 같은 날 내부에서는 이동 비용을 스윕식으로만 반영되는지 확인
- 펜윅 트리 인덱싱(1-based)과 역인덱스(`P - idx + 1`) 일관성
- 64비트 정수 사용(`long long`)
- 정렬 키: `(day asc, idx asc)`

## 참고자료/유사문제
- IOI 2009 Day 2 “Merchant(상인)” 고전 문제
- 좌표압축 + 펜윅/세그먼트 변환으로 이동비용을 선형식에 흡수하는 기법


