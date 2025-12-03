---
title: "[Algorithm] C++ 백준 13329번: Meteor Shower"
description: "각 다각형을 최소각·최대각 꼭짓점으로 압축한 선분으로 바꾼 뒤, 각도 스위핑과 ccw 기반 비교(set)를 이용해 현재 각도에서 최전면 선분만 표시합니다. 표시된 선분 수를 제외해 완전히 가려진 다각형 개수를 계산하는 풀이입니다."
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
- Problem-13329
- cpp
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
- Convex Hull
- 컨벡스헐
- Angular Sweep
- 각도 스위핑
- Sweeping
- 스위핑
- CCW
- 반시계
- Cross Product
- 외적
- Set
- 집합
- Comparator
- 비교함수
- Segment
- 선분
- Visibility
- 가시성
- Lower Hull
- 아래 껍질
- Polar Angle
- 극각
- Event
- 이벤트
- Sorting
- 정렬
- Robustness
- 견고성
- Overflow
- 오버플로
- __int128
- 정수연산
- Precision
- 정밀도
- Implementation Details
- 구현 디테일
- Tips
- 팁
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13329
- 요약: 원점 `(0, 0)`에서 레이저를 쏠 때, 어떤 각도에서도 관측되지 않는(완전히 가려지는) 볼록다각형의 개수를 구합니다. 모든 꼭짓점은 `y ≥ 1`이며 서로 다른 다각형은 교차하지 않습니다.

## 입력/출력
```
입력: n, 이어서 각 다각형마다 정점 수 m과 m개의 (x, y) (반시계, y≥1). 전체 정점 수 ≤ 1e6.
출력: 완전히 보이지 않는(보일 수 없는) 다각형의 개수.
```

## 접근 개요
- 관찰 1: 원점에서의 가시성은 각도(극각)만으로 판단됩니다. 다각형이 볼록이고 `y≥1`인 상반평면에 있으므로, 다각형의 최저각 정점과 최고각 정점만 원점에서 본 "각도 범위"를 규정합니다.
- 관찰 2: 각 볼록다각형을 "최소각 꼭짓점 → 최대각 꼭짓점"을 잇는 선분으로 압축해도, 해당 각도 구간에서의 가시성 판정은 변하지 않습니다.
- 따라서 문제는 "n개의 각도 구간 선분 중, 어떤 각도에서도 최전면이 되지 않는 선분 수"로 환원됩니다.

## 알고리즘 설계
1) 각 다각형에서 극각이 가장 작은 꼭짓점(`p_min`)과 가장 큰 꼭짓점(`p_max`)를 찾습니다. 모든 점이 `y≥1`이므로 단조 극각 비교가 가능합니다.
2) 각 다각형을 선분 `[p_min → p_max]`로 압축하고, 두 끝점을 이벤트로 모아 각도 기준으로 정렬합니다(동각 없음 가정 제공).
3) 각도 스위핑:
   - 이벤트를 순서대로 보며, 시작점이면 해당 선분을 활성 집합에 삽입, 끝점이면 제거합니다.
   - 활성 집합의 정렬 기준은 "겹치는 각도 구간에서 원점과 더 가까운 선분이 먼저"가 되도록 `ccw`(외적 부호)를 활용합니다.
   - 매 이벤트 직후 집합의 맨 앞 원소가 현재 각도에서 보이는(최전면) 선분입니다. 이를 표시합니다.
4) 표시된 선분 수를 `vis`라고 하면, 답은 `n - vis`입니다.

### 정당성(요지)
- 볼록성과 비교차 조건 때문에, 한 각도에서의 최전면은 해당 각도를 덮는 선분들 간의 국소 비교만으로 결정됩니다.
- 선분 정렬 비교는 두 선분이 겹치는 각도 구간 내의 점의 상대적 전면성을 `ccw` 부호로 일관되게 판정합니다(포함/엇갈림 케이스 분기).
- 이벤트 간 각도 구간에서는 최전면이 변하지 않으며, 이벤트 시점에서만 변할 수 있으므로 스위핑으로 충분합니다.

## 복잡도
- 정점 스캔: 전체 정점 수를 `V`라 하면 `O(V)`.
- 이벤트 정렬 및 집합 연산: `O(n log n)`.
- 총합: `O(V + n log n)` (여기서 `V ≤ 1e6`, `n ≤ 1e5`).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

struct Point { int64 x, y; };

static inline __int128 sq(__int128 v){ return v*v; }
static inline __int128 dist2(const Point& p){ return sq((__int128)p.x) + sq((__int128)p.y); }

// ccw of (b - a) x (c - a)
static inline int ccw(const Point& a, const Point& b, const Point& c){
    __int128 vx1 = (__int128)b.x - a.x;
    __int128 vy1 = (__int128)b.y - a.y;
    __int128 vx2 = (__int128)c.x - a.x;
    __int128 vy2 = (__int128)c.y - a.y;
    __int128 t = vx1 * vy2 - vy1 * vx2;
    if (t > 0) return 1;
    if (t < 0) return -1;
    return 0;
}

// 각도 비교: +x 반평면 우선, 같은 반평면이면 원점 기준 각도 오름차순
static inline bool angle_cmp(const Point& a, const Point& b){
    bool ah = (a.x > 0) || (a.x == 0 && a.y > 0);
    bool bh = (b.x > 0) || (b.x == 0 && b.y > 0);
    if (ah ^ bh) return ah > bh;
    int t = ccw({0,0}, a, b);
    if (t != 0) return t > 0;
    // 동각은 없다고 가정되지만 안전하게 거리로 분기
    return dist2(a) < dist2(b);
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; 
    if (!(cin >> n)) return 0;

    vector<pair<Point,int>> ev; ev.reserve(2*n);
    vector<Point> stp(n+1), enp(n+1);
    vector<int> si(n+1), ei(n+1);

    for (int i = 1; i <= n; ++i){
        int m; cin >> m;
        vector<Point> v(m);
        for (int j = 0; j < m; ++j) cin >> v[j].x >> v[j].y; // y >= 1

        // p1 = 각도 최소, p2 = 각도 최대
        Point p1 = *max_element(v.begin(), v.end(), angle_cmp); // 뒤집어 사용할 것이므로 max/min 반대로 선정
        Point p2 = *min_element(v.begin(), v.end(), angle_cmp);

        stp[i] = p1; enp[i] = p2;
        ev.emplace_back(p1, +i);
        ev.emplace_back(p2, -i);
    }

    // 각도 정렬 후 reverse (angle_cmp가 +x -> -x 순서를 만들므로 뒤집어 사용)
    sort(ev.begin(), ev.end(), [&](const auto& A, const auto& B){ return angle_cmp(A.first, B.first); });
    reverse(ev.begin(), ev.end());

    for (int i = 0; i < (int)ev.size(); ++i){
        int id = ev[i].second;
        if (id > 0) si[id] = i; else ei[-id] = i;
    }

    struct Node { int id; };
    struct SegLess {
        const vector<int>& si; const vector<int>& ei; const vector<Point>& stp; const vector<Point>& enp;
        bool operator()(const Node& A, const Node& B) const {
            int a = A.id, b = B.id; if (a == b) return false;
            if (si[a] <= si[b] && ei[b] <= ei[a]) return ccw(stp[a], enp[a], stp[b]) > 0; // a가 b 포함
            if (si[b] <= si[a] && ei[a] <= ei[b]) return ccw(stp[b], enp[b], stp[a]) < 0; // b가 a 포함
            if (si[a] < si[b]) return ccw(stp[a], enp[a], stp[b]) > 0; // 엇갈림
            return ccw(stp[b], enp[b], stp[a]) < 0;
        }
    } segLess{si, ei, stp, enp};

    set<Node, SegLess> S(segLess);
    vector<char> seen(n+1, 0);

    for (int i = 0; i < (int)ev.size(); ++i){
        int id = ev[i].second;
        if (id > 0){
            S.insert({id});
        }else{
            id = -id;
            auto it = S.find({id});
            if (it != S.end()) S.erase(it);
        }
        if (!S.empty()) seen[S.begin()->id] = 1; // 현재 각도에서 보이는 선분
    }

    int vis = 0; for (int i = 1; i <= n; ++i) vis += seen[i];
    cout << (n - vis) << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- 동각(같은 극각) 없음: 문제 보장. 동각 대비 분기(거리 비교)는 안전장치.
- 좌표 범위: `|x| ≤ 1e8`, `y ≥ 1` → 거리 제곱은 64-bit 안전, 외적은 `__int128`로 계산.
- 다각형 불교차 및 볼록성: 전면 비교의 지역성 성립(스위핑으로 충분).
- 이벤트 경계: 매 이벤트 직후에만 전면이 바뀔 수 있으므로, 그 시점에서만 표시.

## 제출 전 점검
- 입출력 형식/개행 확인(마지막 개행 포함).
- 정수 오버플로 방지(`__int128` 사용).
- `ios::sync_with_stdio(false); cin.tie(nullptr);`로 I/O 가속.

## 참고자료
- BOJ 13329 Meteor Shower 문제: https://www.acmicpc.net/problem/13329
- 관련 풀이 아이디어(각도 스위핑, 선분 압축): "백준13329 Meteor Shower" 정리 글 등


