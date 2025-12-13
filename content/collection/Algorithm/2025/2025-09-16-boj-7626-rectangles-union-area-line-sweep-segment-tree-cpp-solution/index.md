---
title: "[Algorithm] C++ 백준 7626번: 직사각형"
description: "N=200,000개의 축에 평행한 직사각형의 합집합 면적을 구합니다. x축 스위프라인과 y좌표 압축+세그먼트 트리(커버 카운트/덮인 길이 유지)로 각 x 구간의 덮인 y길이를 O(log N)에 갱신하고 면적을 누적해 3초 내 통과합니다. 오버플로/엣지 케이스와 구현 포인트를 정리했습니다."
date: 2025-09-16
lastmod: 2025-09-16
categories:
- Algorithm
- Geometry
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-7626
- cpp
- C++
- Line Sweep
- 스위프라인
- Scanline
- 스캔라인
- Segment Tree
- 세그먼트 트리
- Coordinate Compression
- 좌표압축
- Rectangle Union
- 직사각형
- Union Area
- 면적합집합
- Axis-Aligned
- 축정렬
- Coverage
- 덮임길이
- Events
- 이벤트
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
- Geometry
- 기하
- Sweeping
- 스위핑
- 64-bit
- Long Long
- 대용량입력
- 빠른입출력
- 커버카운트
- 면적계산
- 정수오버플로
image: "wordcloud.png"
---

## 문제 정보
- 문제: https://www.acmicpc.net/problem/7626
- 요약: 축에 평행한 직사각형 N개가 덮는 전체 면적을 구합니다. 서로 겹치는 구역은 한 번만 계산합니다.
- 제한/스펙: N ≤ 200,000, 좌표는 0 ≤ x,y ≤ 1e9, 3초, 128MB

## 입출력 형식/예제
```text
입력
2
0 3 1 2
1 2 0 3

출력
5
```

## 접근 개요(아이디어 스케치)
- x축으로 스위프하면서 이벤트(왼쪽 변=추가, 오른쪽 변=제거)를 처리합니다.
- y좌표를 압축한 뒤, 세그먼트 트리로 현재 덮인 y 길이(`covered_length`)를 유지합니다.
- 인접한 이벤트 사이의 `Δx`와 직전 상태의 `covered_length`를 곱해 면적을 누적합니다.

## 알고리즘 설계
1) 각 직사각형 [x1,x2)×[y1,y2)에 대해 이벤트 (x1, [y1,y2), +1), (x2, [y1,y2), -1)를 만든 뒤 x로 정렬
2) y좌표 압축: 모든 y1, y2를 모아 정렬·중복 제거 → 구간은 인접 원본 y의 차로 길이 계산
3) 세그먼트 트리 노드가 담당 구간의 커버 카운트 `cover>0`이면 그 구간 길이를 전부 덮인 것으로 설정, 아니면 자식 합으로 갱신
4) 이벤트를 같은 x에서 모두 반영한 후 다음 x까지의 `Δx * covered_y_length`를 면적으로 더함
5) 모든 이벤트 처리 후 누적 면적 출력(64-bit)

### 올바름 근거(요지)
- 스위프 구간 [xᵢ, xᵢ₊₁)에서 덮인 y 길이는 불변이며, 그 길이×폭(Δx)이 해당 스트립의 정확한 면적입니다.
- 세그먼트 트리의 `cover>0 ⇒ 구간 전체가 덮임` 규칙과 좌표 압축 길이 합산으로 중복 없이 정확히 측정됩니다.

## 복잡도
- 시간: O(N log N) — 이벤트 정렬 O(N log N) + 각 이벤트 당 세그먼트 트리 갱신 O(log N)
- 공간: O(N) — 좌표 압축과 세그먼트 트리

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Event {
    long long x;
    int y1_idx, y2_idx;
    int delta; // +1 add, -1 remove
    bool operator<(const Event& o) const { return x < o.x; }
};

struct SegmentTree {
    int n; // number of elementary intervals = ys.size() - 1
    const vector<long long>& ys;
    vector<int> cover;
    vector<long long> covered;

    SegmentTree(const vector<long long>& ys_) : ys(ys_) {
        n = (int)ys.size() - 1;
        cover.assign(n * 4, 0);
        covered.assign(n * 4, 0);
    }

    void pull(int node, int l, int r) {
        if (cover[node] > 0) {
            covered[node] = ys[r] - ys[l];
        } else {
            if (l + 1 == r) covered[node] = 0;
            else covered[node] = covered[node << 1] + covered[node << 1 | 1];
        }
    }

    void update(int node, int l, int r, int ql, int qr, int val) {
        if (qr <= l || r <= ql) return;
        if (ql <= l && r <= qr) {
            cover[node] += val;
            pull(node, l, r);
            return;
        }
        int mid = (l + r) >> 1;
        update(node << 1, l, mid, ql, qr, val);
        update(node << 1 | 1, mid, r, ql, qr, val);
        pull(node, l, r);
    }

    void update(int l, int r, int val) { // [l, r)
        if (l >= r) return;
        update(1, 0, n, l, r, val);
    }

    long long totalCovered() const { return covered[1]; }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    vector<long long> x1(N), x2(N), y1(N), y2(N);
    vector<long long> ys; ys.reserve(2 * N);
    for (int i = 0; i < N; ++i) {
        cin >> x1[i] >> x2[i] >> y1[i] >> y2[i];
        ys.push_back(y1[i]);
        ys.push_back(y2[i]);
    }

    sort(ys.begin(), ys.end());
    ys.erase(unique(ys.begin(), ys.end()), ys.end());

    vector<Event> ev; ev.reserve(2 * N);
    for (int i = 0; i < N; ++i) {
        int y1i = (int)(lower_bound(ys.begin(), ys.end(), y1[i]) - ys.begin());
        int y2i = (int)(lower_bound(ys.begin(), ys.end(), y2[i]) - ys.begin());
        ev.push_back({x1[i], y1i, y2i, +1});
        ev.push_back({x2[i], y1i, y2i, -1});
    }
    sort(ev.begin(), ev.end());

    SegmentTree seg(ys);
    long long area = 0;
    long long prevX = ev.empty() ? 0 : ev[0].x;

    size_t i = 0, M = ev.size();
    while (i < M) {
        long long curX = ev[i].x;
        long long dx = curX - prevX;
        if (dx != 0) {
            area += dx * seg.totalCovered();
            prevX = curX;
        }
        while (i < M && ev[i].x == curX) {
            seg.update(ev[i].y1_idx, ev[i].y2_idx, ev[i].delta);
            ++i;
        }
    }

    cout << area << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- 완전히 분리된 직사각형들 — 단순 합
- 완전히 포함되는 직사각형 — 중복 면적 제거 확인
- 공통 변만 맞닿는 경우 — 면적 0의 교집합은 카운트되지 않음
- 동일한 x에서 여러 이벤트 — 같은 x의 추가/제거를 모두 반영 후 `Δx` 처리
- 큰 좌표(1e9) — 길이 계산과 면적 누적은 `long long`

## 제출 전 점검
- 입출력: fast I/O 사용, 개행/공백 형식 준수
- 오버플로: `Δx`·`covered_y`·`area` 모두 64-bit
- 세그트리: `cover>0` 규칙, 리프 구간 처리(l+1==r) 확인
- 좌표 압축: 인덱스 범위, 빈 구간 업데이트 회피(`[l,r)` 형태)

## 참고자료/유사문제
- 문제: https://www.acmicpc.net/problem/7626
- 스위프라인+면적합집합: `Klee's measure problem` (1D/2D 일반화)
- 세그먼트 트리 with 커버 카운트: 구간 덮임 길이 유지 기법


