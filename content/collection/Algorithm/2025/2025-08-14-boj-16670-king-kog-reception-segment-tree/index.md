---
title: "[Algorithm] C++ 백준 16670번: King Kog의 접견실 - 세그먼트 트리"
description: "기사들의 방문(도착 시각 t, 소요 d)이 실시간으로 추가/취소되는 상태에서 공주가 시각 t에 도착했을 때의 대기 시간을 즉시 구합니다. 누적 처리량 P(t)와 선형 시간 t를 결합한 백로그 공식 W(t) = (P(t) - t) - min_{u≤t}(P(u) - u) 를 활용하고, 좌표 압축 + 지연 전파 세그먼트 트리로 접수/취소는 suffix 가산, 질의는 점/구간 최소를 O(log N)에 처리해 q ≤ 3e5를 안정적으로 통과합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Data Structures
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16670
- cpp
- C++
- Data Structures
- 자료구조
- Segment Tree
- 세그먼트 트리
- Lazy Propagation
- 지연 전파
- Coordinate Compression
- 좌표압축
- Range Update
- 구간 업데이트
- Range Add
- 구간 가산
- Range Minimum Query
- 구간 최소 질의
- Prefix Minimum
- 최소 접두사
- Online Queries
- 온라인 쿼리
- Queue
- 대기열
- Scheduling
- 스케줄링
- Workload
- 백로그
- Backlog
- 누적 처리량
- Prefix Sum Model
- 모델링
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
- Optimization
- 최적화
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
- Set Maintenance
- 집합 유지
- Cancellation
- 취소 처리
- Event Processing
- 이벤트 처리
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/16670
- 요약: 기사들은 도착 시각 `t`와 소요 시간 `d`를 미리 접수합니다. 접수는 시각 오름차순으로 처리되며, 앞선 방문이 끝나야 다음이 시작됩니다. 접수/취소/질의가 섞여 주어질 때, 공주가 시각 `t`에 도착하면 얼마를 기다리는지 출력합니다. 동일 시각 도착 시 공주는 기사 뒤에 섭니다.
- 제한: `1 ≤ q ≤ 3·10^5`, `1 ≤ t, d ≤ 10^6`. 각 시점에 접수된 기사들의 시각은 서로 다릅니다. 취소는 아직 취소되지 않은 과거 접수만 가리킵니다.

## 입력/출력 예시
```
입력
19
? 3
+ 2 2
? 3
? 4
+ 5 2
? 5
? 6
+ 1 2
? 2
? 3
? 4
? 5
? 6
? 7
? 9
- 8
? 2
? 3
? 6

출력
0
1
0
2
1
3
2
1
2
1
0
0
2
1
1
```

## 접근 개요
- 핵심 공식: 접수 집합에서 누적 처리량을 `P(t) = Σ_{u≤t} d(u)`라 두면, 시각 `t`의 대기 시간(백로그)은
  
  \[ W(t) = (P(t) - t) - \min_{u \le t} (P(u) - u) \]
  
  입니다. 이는 “작업 유입은 `P`, 처리 속도는 1”인 단위 처리 모델에서의 표준 백로그 공식입니다. 공주는 기사보다 뒤에 서므로 `t`에 도착한 기사도 `P(t)`에 포함됩니다.
- 자료구조 설계: 시간 축을 접수/질의에 등장한 모든 `t`로 좌표압축하고,
  - `F[i] = P(c_i) - c_i`를 위한 세그먼트 트리(지연 전파, 구간 가산/구간 최소)
  - `G[i]`로 `min_{u≤t}(P(u)-u)` 후보를 얻기 위한 세그먼트 트리(접두 구간 최소)
  를 유지합니다. 접수 `(+ t d)`는 해당 좌표부터 끝까지 `+d`(suffix 가산), 질의는 `F[pos] - min(0, min G[1..pos]))`로 계산합니다. 취소는 동일 연산을 부호 반대로 되돌립니다.

```mermaid
flowchart TB
  A[이벤트 스트림 q개] --> B[좌표 압축(모든 t)]
  B --> C1[세그트리 F: P(t)-t]
  B --> C2[세그트리 G: min_{u≤t}(P(u)-u) 후보]
  C1 --> D[질의 시 F(pos)]
  C2 --> E[질의 시 minPrefix(pos)]
  D --> F[W(t) = F - min(0, minPrefix)]
  E --> F
```

## 알고리즘 설계
- 좌표압축: 모든 `+`/`?`의 시간 `t`를 모아 정렬·중복제거 후 1-index로 매핑합니다.
- 세그먼트 트리 갱신
  - 접수 `(+ t d)`: `pos = idx(t)`
    - `F`: `[pos..M] += d`
    - `G`: `[pos..M] += d` 후, 같은 시각에서의 “도착 직전” 값을 반영하려 `G[pos] -= d`
  - 취소 `(- i)`: 위 연산을 그대로 반대로 적용
- 질의 `( ? t )`: `pos = idx(t)`
  - `Fpos = min(F[pos..pos])`가 곧 `P(t)-t`
  - `minG = min(G[1..pos])`, 여유구간(초기 공백 시간) 허용을 위해 `min(0, minG)`와 비교
  - 결과 `W(t) = Fpos - min(0, minG)`

## 정당성(요지)
- 단위 처리율 모델에서 백로그는 과거 임의 시점 `u`부터 현재까지 “유입량 − 처리량”의 최대 누적이며, 이는 `(P(t)-t) - min_{u≤t}(P(u)-u)`로 정리됩니다. 접수는 시각 순으로만 진행되고 공주는 같은 시각 기사 뒤에 서므로, `P` 정의와 공식이 정확히 문제 가정을 반영합니다.

## 복잡도
- 시간: 접수/취소/질의 각각 `O(log M)` (`M`=고유 시간 수, `M ≤ 2q`)
- 공간: `O(M)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct SegmentTree {
    int n;
    vector<long long> tree;
    vector<long long> lazy;

    SegmentTree() : n(0) {}
    SegmentTree(int n_, const vector<long long>& base) { init(n_, base); }

    void init(int n_, const vector<long long>& base) {
        n = n_;
        tree.assign(4 * n + 4, 0);
        lazy.assign(4 * n + 4, 0);
        build(1, 1, n, base);
    }

    void build(int node, int l, int r, const vector<long long>& base) {
        if (l == r) {
            tree[node] = base[l];
            return;
        }
        int mid = (l + r) >> 1;
        build(node << 1, l, mid, base);
        build(node << 1 | 1, mid + 1, r, base);
        tree[node] = min(tree[node << 1], tree[node << 1 | 1]);
    }

    inline void apply(int node, long long val) {
        tree[node] += val;
        lazy[node] += val;
    }

    inline void push(int node) {
        if (lazy[node] != 0) {
            apply(node << 1, lazy[node]);
            apply(node << 1 | 1, lazy[node]);
            lazy[node] = 0;
        }
    }

    void range_add(int L, int R, long long val) { range_add(1, 1, n, L, R, val); }
    void range_add(int node, int l, int r, int L, int R, long long val) {
        if (R < l || r < L) return;
        if (L <= l && r <= R) { apply(node, val); return; }
        push(node);
        int mid = (l + r) >> 1;
        range_add(node << 1, l, mid, L, R, val);
        range_add(node << 1 | 1, mid + 1, r, L, R, val);
        tree[node] = min(tree[node << 1], tree[node << 1 | 1]);
    }

    long long query_min(int L, int R) { return query_min(1, 1, n, L, R); }
    long long query_min(int node, int l, int r, int L, int R) {
        if (R < l || r < L) return LLONG_MAX / 4;
        if (L <= l && r <= R) return tree[node];
        push(node);
        int mid = (l + r) >> 1;
        return min(query_min(node << 1, l, mid, L, R),
                   query_min(node << 1 | 1, mid + 1, r, L, R));
    }
};

struct Event {
    char type;              // '+', '-', '?'
    long long t{0}, d{0};   // for '+': t, d; for '?': t
    int ref{-1};            // for '-': referenced join index (0-based)
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q; if (!(cin >> q)) return 0;

    vector<Event> events(q);
    vector<long long> all_times; all_times.reserve(q * 2);

    for (int i = 0; i < q; ++i) {
        char c; cin >> c; events[i].type = c;
        if (c == '+') {
            long long t, d; cin >> t >> d;
            events[i].t = t; events[i].d = d;
            all_times.push_back(t);
        } else if (c == '-') {
            int idx; cin >> idx; events[i].ref = idx - 1; // 0-based
        } else { // '?'
            long long t; cin >> t; events[i].t = t; all_times.push_back(t);
        }
    }

    sort(all_times.begin(), all_times.end());
    all_times.erase(unique(all_times.begin(), all_times.end()), all_times.end());
    int m = (int)all_times.size();
    auto get_index = [&](long long t) -> int {
        return int(lower_bound(all_times.begin(), all_times.end(), t) - all_times.begin()) + 1; // 1-based
    };

    // Base arrays: initially P=0 → F[i] = -c_i, G[i] = -c_i
    vector<long long> baseF(m + 1, 0), baseG(m + 1, 0);
    for (int i = 1; i <= m; ++i) {
        baseF[i] = -all_times[i - 1];
        baseG[i] = -all_times[i - 1];
    }

    SegmentTree segF(m, baseF);
    SegmentTree segG(m, baseG);

    vector<int> join_pos(q, -1);
    vector<long long> join_d(q, 0);
    vector<char> is_active(q, 0);

    for (int i = 0; i < q; ++i) {
        if (events[i].type == '+') {
            int pos = get_index(events[i].t);
            long long d = events[i].d;
            is_active[i] = 1; join_pos[i] = pos; join_d[i] = d;

            // suffix add: all future times see increased P
            segF.range_add(pos, m, d);
            segG.range_add(pos, m, d);
            // at exact arrival instant, consider value just-before-arrival
            segG.range_add(pos, pos, -d);
        } else if (events[i].type == '-') {
            int j = events[i].ref;
            if (j >= 0 && is_active[j]) {
                int pos = join_pos[j]; long long d = join_d[j];
                is_active[j] = 0;
                segF.range_add(pos, m, -d);
                segG.range_add(pos, m, -d);
                segG.range_add(pos, pos, +d);
            }
        } else { // '?'
            int pos = get_index(events[i].t);
            long long Fpos = segF.query_min(pos, pos);           // P(t) - t
            long long minG = segG.query_min(1, pos);             // min_{u≤t}(P(u)-u) 후보
            long long mval = min(0LL, minG);                     // 공백 구간 허용
            long long wait = Fpos - mval;                        // 백로그
            cout << wait << '\n';
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- 접수 없음 상태에서의 질의: `W(t)=0`이어야 하며, `min(0, minG)` 처리로 보장
- 동일 시각 중복 접수 금지 조건 반영: 입력 보장, 자료구조는 좌표 단위 단일 점만 가감
- 취소는 반드시 유효한 과거 접수만: 역연산으로 정확히 되돌림
- 매우 큰 `q`(3e5): `O(log M)` 연산, 빠른 입출력 사용
- 시간 경계 `t=1`/`1e6`: 좌표압축으로 안전

## 제출 전 점검
- 입출력 버퍼링(`sync_with_stdio(false)`, `tie(nullptr)`) 적용 여부
- 세그먼트 트리 범위/인덱스(1-index) 일관성
- 64-bit 정수 사용: 누적 합과 결과는 `long long`
- 취소 처리 시 중복 취소/잘못된 인덱스는 입력상 없음(문제 보장)

## 참고자료
- 큐잉에서의 백로그 표준 정식: `W(t) = (P(t)-t) - min_{u≤t}(P(u)-u)`
- 세그먼트 트리(지연 전파) 개요와 응용


