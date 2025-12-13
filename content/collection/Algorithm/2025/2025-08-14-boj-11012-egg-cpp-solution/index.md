---
title: "[Algorithm] C++ 백준 11012번: Egg - 2D 직사각형 쿼리 스위핑+BIT"
description: "n개의 점과 m개의 직사각형 [l,r]×[b,t]가 주어질 때, 각 직사각형 안의 점 개수를 모두 합한 값을 구한다. x를 기준으로 오프라인 스위핑을 수행하고, y는 좌표 압축 후 펜윅 트리(Fenwick Tree)로 누적 빈도를 관리한다. 쿼리는 (r,+1),(l-1,−1) 이벤트로 분해해 포함-배제를 구현하여 총합을 O((n+m) log n)에 계산한다. 64비트 누적, 경계(b=0) 처리, 중복 좌표 대응을 주의한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Fenwick Tree
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-11012
- cpp
- C++
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
- Binary Indexed Tree
- Fenwick Tree
- 펜윅트리
- BIT
- Coordinate Compression
- 좌표압축
- Sweep Line
- 스위핑
- Offline Query
- 오프라인 쿼리
- Inclusion-Exclusion
- 포함배제
- Range Query
- 범위쿼리
- Rectangle Query
- 직사각형쿼리
- 2D Range Counting
- 2D 범위 카운팅
- Orthogonal Range Counting
- 직교 범위 카운팅
- Event Processing
- 이벤트 처리
- Prefix Sum
- 누적합
- Sorting
- 정렬
- Geometry
- 기하
- Math
- 수학
- Egg
- Rectangle
- 좌표평면
- Algorithm Design
- 알고리즘 설계
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/11012
- 요약: `n`개의 점 `(x,y)`와 `m`개의 직사각형 영역 `[l,r]×[b,t]`가 주어진다. 각 직사각형에 포함되는 점의 개수를 모두 더한 총합을 출력한다. 좌표는 중복 가능.

### 제한/스펙
- 테스트케이스 `T ≤ 20`
- 점 개수 `1 ≤ n ≤ 10000`, 쿼리 개수 `0 ≤ m ≤ 50000`
- 좌표 범위 `0 ≤ x,y ≤ 1e5`
- 직사각형 경계 `0 ≤ l ≤ r ≤ 1e5`, `0 ≤ b ≤ t ≤ 1e5`
- 목표: 전체 합계를 빠르게 계산(`O((n+m) log n)`)

## 입출력 형식/예제

예제 입력 1
```
2
3 1
3 5
2 3
1 1
1 2
1 3 3 2
5 3
2 2
1 1
1 2
1 3
2 5
2 3
```

예제 출력 1
```
2
4
```

## 접근 개요(아이디어 스케치)
- 핵심: 모든 직사각형에 대해 포함된 점의 개수를 더한다는 것은, 각 점이 몇 개의 직사각형에 포함되는지를 모두 합한 값과 같다.
- 오프라인 스위핑: x를 기준으로 정렬해 진행. 각 쿼리 `[l,r]×[b,t]`를 두 이벤트 `(r, +1, b, t)`와 `(l-1, -1, b, t)`로 분해해 포함-배제를 구현한다.
- 펜윅 트리(BIT): 현재까지 추가된 점들의 y-좌표 빈도를 좌표 압축 후 BIT로 관리. 이벤트 시점의 y구간 `[b,t]` 빈도 합을 구해 계수(+1/−1)를 곱해 누적한다.

```mermaid
flowchart TD
  A[점 (x,y) 정렬] --> B[쿼리 각자 (r,+1),(l-1,-1) 이벤트화]
  B --> C[x 오름차순으로 이벤트 순회]
  C --> D{다음 이벤트 x'까지 점 추가}
  D -->|x_i ≤ x'| E[BIT에 y_i 카운트+1]
  C --> F[BIT로 [b,t] 구간합]
  F --> G[계수(+1/−1) 곱해 정답 누적]
```

## 알고리즘 설계
- 전처리: 점들을 `x` 오름차순 정렬. 모든 쿼리를 이벤트 `(x, b, t, coeff)`로 변환하고 `x` 오름차순 정렬.
- 좌표 압축: BIT는 점들의 `y`만 압축(빈도 구조이므로 쿼리의 `y`는 상한 탐색으로 처리 가능).
- 스위핑:
  1) 이벤트를 순서대로 보며, 해당 `x` 이하의 모든 점을 BIT에 추가.
  2) `cnt = sum(t) - sum(b-1)`을 구하고 `answer += coeff * cnt`.
- 올바름 근거: 각 쿼리의 점 개수는 `(# x≤r) - (# x≤l-1)`로 표현 가능. y는 `[b,t]` 구간합으로 제한. 선형성에 의해 모든 쿼리를 합쳐도 동일.

## 복잡도
- 시간: 점 추가 `n`회 + 이벤트 `2m`회 각각 `O(log n)` → 총 `O((n+m) log n)`
- 공간: BIT와 보조 배열 `O(n)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    int n;
    vector<int> bit;
    Fenwick(int n = 0) { init(n); }
    void init(int n_) { n = n_; bit.assign(n + 1, 0); }
    void add(int idx, int delta) {
        for (; idx <= n; idx += idx & -idx) bit[idx] += delta;
    }
    long long sum(int idx) const {
        long long s = 0;
        for (; idx > 0; idx -= idx & -idx) s += bit[idx];
        return s;
    }
};

struct Event {
    int x, b, t, coeff; // coeff = +1 for r, -1 for l-1
    bool operator<(const Event& other) const { return x < other.x; }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n, m;
        cin >> n >> m;

        vector<pair<int,int>> points(n);
        vector<int> y_vals;
        y_vals.reserve(n);
        for (int i = 0; i < n; ++i) {
            int x, y; cin >> x >> y;
            points[i] = {x, y};
            y_vals.push_back(y);
        }

        vector<Event> events;
        events.reserve(2 * m);
        for (int i = 0; i < m; ++i) {
            int l, r, b, t; 
            cin >> l >> r >> b >> t;
            events.push_back({r, b, t, +1});
            events.push_back({l - 1, b, t, -1});
        }

        sort(points.begin(), points.end()); // by x
        sort(events.begin(), events.end()); // by x

        sort(y_vals.begin(), y_vals.end());
        y_vals.erase(unique(y_vals.begin(), y_vals.end()), y_vals.end());

        auto y_index_upper = [&](int y) -> int {
            // number of unique point-ys <= y
            return int(upper_bound(y_vals.begin(), y_vals.end(), y) - y_vals.begin());
        };

        Fenwick fw((int)y_vals.size());

        long long answer = 0;
        int p = 0; // pointer over points
        for (const auto& ev : events) {
            while (p < n && points[p].first <= ev.x) {
                int y = points[p].second;
                int idx = y_index_upper(y); // 1..N
                if (idx > 0) fw.add(idx, 1);
                ++p;
            }
            int up_t = y_index_upper(ev.t);
            int up_bm1 = y_index_upper(ev.b - 1);
            long long cnt = fw.sum(up_t) - fw.sum(up_bm1);
            answer += (long long)ev.coeff * cnt;
        }

        cout << answer << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `m=0`: 쿼리 없음 → 출력 `0`이어야 함.
- `b=0`: `b-1=-1` 처리는 `upper_bound` 기반 인덱싱으로 자동 0처리.
- 동일 좌표 점 다수: y좌표 압축은 점의 y만 사용하므로 중복 카운트 정확.
- 매우 좁은/선분형 직사각형: 경계 포함 규칙 `[l,r]`·`[b,t]` 정확히 반영.
- 모든 점이 쿼리 밖/안: 누적이 0 또는 `m*n`에 근접 → 64비트 결과 사용.

## 제출 전 점검
- 결과형 `long long` 사용(최대 약 `5e4×1e4 = 5e8`이지만 합산 안전성 확보).
- 이벤트 `(l-1)` 생성 시 `l=0`일 때 음수 x 가능 → 점 추가 조건 `x_i ≤ ev.x`로 정상 동작.
- BIT 인덱스는 1-base, `upper_bound` 반환값 그대로 사용(0 가능).
- 입출력 가속 설정(`sync_with_stdio(false), tie(nullptr)`).

## 참고자료/유사문제
- 직교 범위 카운팅(Orthogonal Range Counting) 표준 기법: 오프라인 스위핑 + BIT.
- 포함-배제 기반의 범위 합 분해: `(x≤r) - (x≤l-1)`.


