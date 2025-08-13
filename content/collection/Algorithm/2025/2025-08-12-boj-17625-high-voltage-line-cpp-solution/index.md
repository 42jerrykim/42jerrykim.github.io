---
title: "[Algorithm] C++ 백준 17625번 : 고압선"
description: "백준 17625 고압선 문제를 회전 스윕(Rotating Sweep Line)으로 해결합니다. 모든 (i,j)쌍의 평행/수직 이벤트를 각도 정렬하여 인접 스왑만으로 순서를 유지하고, 수직이등분선과 선분 양측의 인접 점을 이용해 거주지점까지의 직선거리의 최솟값을 최대화하는 최적의 고압선 값을 안정적으로 구하는 C++ 풀이를 정리합니다."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "Algorithm"
- "BOJ"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "17625"
- "High Voltage Line"
- "고압선"
- "Geometry"
- "기하"
- "Computational Geometry"
- "계산기하"
- "Rotating Sweep"
- "Rotating Sweep Line"
- "회전 스윕"
- "Sweep Line"
- "스윕 라인"
- "Angle Sort"
- "각도 정렬"
- "Event Sorting"
- "이벤트 정렬"
- "Adjacency Swap"
- "인접 스왑"
- "Label Maintenance"
- "라벨 유지"
- "Perpendicular Bisector"
- "수직이등분선"
- "Projection"
- "사영"
- "Line Distance"
- "점-직선 거리"
- "Cross Product"
- "교차곱"
- "Dot Product"
- "내적"
- "Vector Length"
- "벡터 길이"
- "Half-plane"
- "반평면"
- "Two-point Case"
- "두 점 케이스"
- "Three-point Case"
- "세 점 케이스"
- "Special Judge"
- "스페셜 저지"
- "Precision"
- "정밀도"
- "Double Precision"
- "배정밀도"
- "Overflow Safe"
- "오버플로 방지"
- "Time Complexity"
- "시간복잡도"
- "O(n^2 log n)"
- "Implementation"
- "구현"
- "C++"
- "CPP"
- "GNU++17"
- "Fast IO"
- "빠른입출력"
- "KOI"
- "한국정보올림피아드"
- "2019 KOI"
- "Olympiad"
- "Problem Solving"
- "문제풀이"
- "Algorithm"
- "알고리즘"
- "Solution Code"
- "정답 코드"
image: "wordcloud.png"
---

문제: [BOJ 17625 - 고압선](https://www.acmicpc.net/problem/17625)

### 아이디어 요약
- **최적 직선의 형태**는 두 가지 후보로 수렴합니다.
  - **두 점 p1, p2의 수직이등분선**: 두 점까지의 최단거리를 동일하게 하면서 양측에 점이 존재하도록 하는 경우.
  - **세 점 p1, p2, p3에 대해 p1에서 선분 p2p3에 내린 수선의 수직이등분선**: 선분 양측에서 가장 가까운 점이 각각 하나씩 존재하도록 하는 경우.
- 모든 쌍 `(i, j)`에 대해 두 이벤트를 준비합니다.
  - `flag=+1`: 방향이 선분 `(i,j)`와 **평행**인 이벤트 → 각도 순으로 진행하면서 라벨 배열에서 **인접 스왑**을 수행합니다.
  - `flag=-1`: 방향이 선분 `(i,j)`에 **수직**(= `rot90`)인 이벤트 → 이 시점에 `(i, j)`가 사영상 인접하다면, 두 점의 거리(= 수직이등분선 반지름×2)가 후보가 됩니다.
- 평행 이벤트 직후, 현재 `(i,j)`의 양끝에서 각각 한 칸 떨어진 좌우 이웃 점만 보면 선분에 내린 거리의 최솟값 후보를 빠르게 갱신할 수 있습니다.
- 이벤트를 방향(각도) 기준으로 정렬하면 각 이벤트마다 **인접한 두 점 한 쌍만** 순서가 바뀌므로, 전체 복잡도는 `O(n^2 log n)`입니다.

### C++ 풀이

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using Point = pair<ll,ll>;
#define x first
#define y second

istream& operator>>(istream& in, Point& t){ in >> t.x >> t.y; return in; }
Point operator+(Point a, Point b){ return {a.x+b.x, a.y+b.y}; }
Point operator-(Point a, Point b){ return {a.x-b.x, a.y-b.y}; }
ll operator*(Point a, Point b){ return a.x*b.x + a.y*b.y; }             // dot
ll operator/(Point a, Point b){ return a.x*b.y - a.y*b.x; }             // cross

static inline double length(Point p){ return sqrt((long double)p.x*p.x + (long double)p.y*p.y); }
static inline double dist_point_line(const Point& a, const Point& b, const Point& c){
    // |(b-a) x (c-a)| / |b-a|
    return fabsl((long double)((b-a)/(c-a))) / length(b-a);
}

// Rotate by +90 degrees with a canonical representative to keep ordering stable
static inline Point Rot90(Point p){
    return p.y >= 0 ? Point{p.y, -p.x} : Point{-p.y, p.x};
}

int N;
int Idx[2020], Ord[2020];
Point A[2020];

struct Line{
    int i, j, flag; // flag: +1 parallel, -1 perpendicular (=rot90)
    Point s, e, dir;
    Line(int i_, int j_, int f_) : i(i_), j(j_), flag(f_), s(A[i_]), e(A[j_]){
        if(e < s) swap(s, e);
        dir = (flag == 1) ? (e - s) : Rot90(e - s);
    }
    bool operator<(const Line& l) const{
        long long cr = dir / l.dir;                // angle order by cross sign
        if(cr) return cr > 0;                      // CCW first
        return tie(flag, s, e) < tie(l.flag, l.s, l.e); // deterministic tie-break
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if(!(cin >> N)) return 0;
    for(int i=1;i<=N;i++) cin >> A[i];
    sort(A+1, A+N+1);

    for(int i=1;i<=N;i++) Ord[i]=Idx[i]=i;

    vector<Line> lines; lines.reserve(1LL*N*(N-1));
    for(int i=1;i<=N;i++){
        for(int j=i+1;j<=N;j++){
            lines.emplace_back(i,j, +1);
            lines.emplace_back(i,j, -1);
        }
    }
    sort(lines.begin(), lines.end());

    double mxTwice = 0.0; // store 2 * answer
    for(const auto& line : lines){
        if(line.flag == 1){
            int a = line.i, b = line.j;
            // Adjacent swap in the current labeling
            swap(Idx[a], Idx[b]);
            swap(Ord[Idx[a]], Ord[Idx[b]]);

            int pa = Idx[line.i], pb = Idx[line.j];
            if(pa > pb) swap(pa, pb);

            if(pa-1 >= 1)  mxTwice = max(mxTwice, dist_point_line(line.s, line.e, A[Ord[pa-1]]));
            if(pb+1 <= N)  mxTwice = max(mxTwice, dist_point_line(line.s, line.e, A[Ord[pb+1]]));
        }else{
            // Perpendicular event: (i,j) adjacent along projection → perpendicular bisector candidate
            if(abs(Idx[line.i] - Idx[line.j]) == 1){
                mxTwice = max(mxTwice, length(A[line.i] - A[line.j]));
            }
        }
    }

    cout.setf(ios::fixed);
    cout << setprecision(10) << (mxTwice * 0.5) << '\n';
    return 0;
}
```

### 복잡도
- **시간**: `O(n^2 log n)` (모든 쌍 이벤트 생성 + 각도 정렬 + 선형 스윕)
- **공간**: `O(n^2)` (이벤트 저장) + `O(n)` (라벨/인덱스 배열)

### 참고
- 문제: `https://www.acmicpc.net/problem/17625`
- 핵심 테크닉: 회전 스윕(각도 정렬) + 인접 스왑 유지 + 수직이등분선 후보 체크


