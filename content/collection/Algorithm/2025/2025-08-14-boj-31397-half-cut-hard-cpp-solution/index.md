---
title: "[Algorithm] C++ 백준 31397번: 반 나누기 (Hard)"
description: "볼록다각형에서 둘레가 같은 두 조각을 만들기 위해 둘레 절반 간격의 두 점을 연결하고, 신발끈 누적합과 경계 호길이 파라미터화로 부분 넓이를 빠르게 계산하여 이분탐색으로 넓이 절반을 만족하는 절단점을 찾는 풀이."
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
- Problem-31397
- cpp
- C++
- Python
- Geometry
- 기하
- Computational Geometry
- 계산기하
- Convex Polygon
- 볼록다각형
- Polygon
- 다각형
- Shoelace
- 신발끈공식
- Shoelace Formula
- Perimeter
- 둘레
- Area
- 넓이
- Arc Length
- 호길이
- Bisection
- 이분탐색
- Prefix Sum
- 누적합
- Numerical Methods
- 수치해석
- Root Finding
- 근 찾기
- Long Double
- 부동소수점
- Precision
- 정밀도
- Parametric Search
- 매개변수탐색
- Segment
- 선분
- Chord
- 현
- Cut
- 절단
- Special Judge
- 스페셜저지
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
- Robustness
- 견고성
- Prefix Perimeter
- 둘레누적
- Prefix Cross
- 교차누적
- Upper Bound
- 상한
- Monotonicity
- 단조성
- Contest
- solvedac
- Grand Arena #4
- Hard
- 난이도상
image: "wordcloud.png"
---

## 문제
- **링크**: [반 나누기 (Hard) - BOJ 31397](https://www.acmicpc.net/problem/31397)
- **요약**: 볼록다각형을 직선 한 번으로 잘라 두 조각의 넓이와 둘레를 모두 같게 만들 수 있는지, 가능하면 절단선의 양 끝점을 각 변의 내분 좌표(인덱스 `j, k`와 비율 `α, β`)로 출력합니다.
- **제한/스펙**: 시간 1초, 메모리 1024MB, N ≤ 200,000, 정수 좌표(공선 3점 없음), 스페셜 저지.

## 입력/출력 예시
```
입력
3
0 0
10 0
5 10

출력
YES
1 0.500000000000
2 1.000000000000
```

## 접근 개요
- **둘레 조건의 관찰**: 절단선의 두 끝점을 `S, T`라 하면, 각 조각의 둘레는 각각 `arc(S→T) + |ST|`, `arc(T→S) + |ST|`입니다. 둘레가 같으려면 `arc(S→T) = arc(T→S)` → 즉, 경계 위에서 **둘레의 절반**만큼 떨어진 두 점을 연결해야 합니다.
- **넓이 조건 충족**: 경계 길이 기준 시작점 `s`를 잡고, `t = s + (총둘레)/2`로 잡으면 둘레는 자동으로 같아집니다. 이제 함수 `f(s) = area(s, t) - 전체넓이/2`의 근을 **이분법**으로 찾으면 됩니다.
- **면적의 빠른 계산**: 신발끈 공식의 **누적 교차합**과 **둘레 누적합**으로 임의의 경계상 위치 `s, t`에서의 부분 다각형 `S → … → T → S`의 면적을 O(1)에 계산합니다(내분점 처리 포함). `f(s)`는 O(log N) (이분탐색으로 구간 위치 찾기)로 계산되며, 전체는 O(log N · 반복횟수)로 충분합니다.

## 알고리즘 설계
- **전처리**
  - 정점 `P[0..N-1]`(CCW)로부터, `prefLen[i] = ∑ |P[k]P[k+1]| (k=0..i-1)`과 `prefCross[i] = ∑ cross(P[k], P[k+1])`를 준비합니다.
  - 총둘레 `L = prefLen[N]`, 전체넓이 `A = prefCross[N]/2`.
- **경계상 점 찾기 `locate(s)`**
  - `upper_bound(prefLen, s)`로 `s`가 위치한 변 인덱스 `e`를 찾고, 변 내 비율 `α = (s - prefLen[e]) / |P[e]P[e+1]|`로 점 `S = (1-α)P[e] + α P[e+1]`를 구합니다.
- **부분 다각형 넓이 `area_s_to_t(s, t)`**
  - `t < s`면 `t += L`(한 바퀴 랩 처리). 최종 정점열은 `S → P[e+1] → … → P[et] → T → S`.
  - 교차합은 `cross(S, P[e+1]) + (prefCross[et] - prefCross[e+1]) (+ 랩 구간 보정) + cross(P[et], T) + cross(T, S)`로 O(1) 계산.
- **이분 탐색**
  - 함수 `f(s) = area_s_to_t(s, s + L/2) - A/2`는 `f(s+L/2) = -f(s)`를 만족하므로, 구간 `[0, L/2]`에 근이 존재합니다. 100회 이분으로 충분한 정밀도를 맞춥니다.
- **출력**
  - `S`가 있는 변 시작 인덱스 `j`(1-indexed)와 내분비 `α`, `T`의 `k, β`를 소수점 12자리로 출력합니다.

## 정당성 근거
- **둘레 동등성**: 두 조각의 둘레가 같으려면 경계호의 길이가 같아야 하므로, 경계 위의 두 점은 총둘레의 정확히 절반만큼 떨어져 있어야 합니다.
- **연속성과 대칭성**: `area(s, s+L/2)`는 `s`에 대해 연속이며 `area(s+L/2, s+L) = A - area(s, s+L/2)`이므로 `f(s+L/2) = -f(s)`. 중간값 정리에 의해 `[0, L/2]`에 근 존재.
- **면적 계산의 정확성**: 신발끈 공식은 임의 다각형의 넓이를 정확히 계산합니다. 경계상 분할점은 내분점으로 처리되어 교차합에 선형 반영되며, 오차는 부동소수점 정밀도로만 제한됩니다.

## 복잡도
- `locate`: O(log N)
- `area` 계산: O(1) + `locate` 2회 → O(log N)
- 이분 100회 → 전체 O(100 · log N), 메모리 O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Point { long double x, y; };
static inline Point operator+(const Point& a, const Point& b){ return {a.x+b.x, a.y+b.y}; }
static inline Point operator-(const Point& a, const Point& b){ return {a.x-b.x, a.y-b.y}; }
static inline Point operator*(const Point& a, long double k){ return {a.x*k, a.y*k}; }
static inline long double cross(const Point& a, const Point& b){ return a.x*b.y - a.y*b.x; }
static inline long double dist(const Point& a, const Point& b){ long double dx=a.x-b.x, dy=a.y-b.y; return sqrtl(dx*dx+dy*dy); }

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; if(!(cin>>N)) return 0;
    vector<Point> P(N);
    for(int i=0;i<N;i++){ long long xi, yi; cin>>xi>>yi; P[i] = {(long double)xi, (long double)yi}; }

    vector<long double> prefLen(N+1, 0.0L), prefCross(N+1, 0.0L);
    for(int i=0;i<N;i++){
        int j=(i+1==N?0:i+1);
        prefLen[i+1] = prefLen[i] + dist(P[i], P[j]);
        prefCross[i+1] = prefCross[i] + cross(P[i], P[j]);
    }
    long double L = prefLen[N];
    long double halfL = L * 0.5L;
    long double A = prefCross[N] * 0.5L;

    auto locate = [&](long double s){
        // s in [0, L)
        int e = int(upper_bound(prefLen.begin(), prefLen.end(), s) - prefLen.begin()) - 1;
        if(e < 0) e = 0; if(e >= N) e = N-1;
        long double segStart = prefLen[e];
        long double segLen = prefLen[e+1] - segStart;
        long double alpha = (segLen>0 ? (s - segStart)/segLen : 0.0L);
        if(alpha < 0) alpha = 0; if(alpha > 1) alpha = 1;
        Point pt = P[e] + (P[(e+1==N?0:e+1)] - P[e]) * alpha;
        return tuple<int,long double,Point>(e, alpha, pt);
    };

    auto area_s_to_t = [&](long double s, long double t){
        if(t < s) t += L;
        auto [es, fs, S] = locate(fmodl(s + L, L));
        auto [et, ft, T] = locate(fmodl(t, L));

        long double sumC = 0.0L;
        int esn = (es+1==N?0:es+1);
        sumC += cross(S, P[esn]);

        long double middle = 0.0L;
        if(t <= L){
            if(et >= es+1) middle = prefCross[et] - prefCross[es+1];
        } else {
            middle = (prefCross[N] - prefCross[es+1]) + (prefCross[et] - prefCross[0]);
        }
        sumC += middle;

        sumC += cross(P[et], T);
        sumC += cross(T, S);
        return sumC * 0.5L;
    };

    auto f = [&](long double s){ return area_s_to_t(s, s + halfL) - A * 0.5L; };

    long double left = 0.0L, right = halfL;
    long double fl = f(left), fr = f(right);
    if(fabsl(fl) >= 1e-18L && fabsl(fr) >= 1e-18L){
        for(int it=0; it<100; ++it){
            long double mid = (left + right) * 0.5L;
            long double fm = f(mid);
            if((fl <= 0 && fm <= 0) || (fl >= 0 && fm >= 0)){ left = mid; fl = fm; }
            else { right = mid; fr = fm; }
        }
    }

    long double sStar = (left + right) * 0.5L;
    long double tStar = sStar + halfL; if(tStar >= L) tStar -= L;
    auto [js, alpha, Spt] = locate(sStar);
    auto [kt, beta,  Tpt] = locate(tStar);
    if(alpha < 0) alpha = 0; if(alpha > 1) alpha = 1;
    if(beta  < 0) beta  = 0; if(beta  > 1) beta  = 1;

    cout.setf(std::ios::fixed); cout<<setprecision(12);
    cout << "YES\n";
    cout << (js+1) << ' ' << alpha << "\n";
    cout << (kt+1) << ' ' << beta  << "\n";
    return 0;
}
```

## Mermaid로 보는 흐름
```mermaid
flowchart TD
  A[정점/좌표 입력] --> B[둘레/신발끈 누적합 전처리]
  B --> C[함수 f(s)=area(s,s+L/2)-A/2 정의]
  C --> D{이분탐색 [0, L/2]}
  D -->|중간값 mid| E[locate(mid), locate(mid+L/2)]
  E --> F[부분 다각형 교차합 O(1) 계산]
  F --> G[부호로 구간 갱신]
  G --> D
  D -->|수렴| H[내분정보 (j,α), (k,β) 출력]
```

## 코너 케이스 체크리스트
- `S, T`가 꼭짓점에 위치(α=0 또는 1)하는 경우
- 매우 길거나 짧은 변(분모 안정성), 동일 길이 반복 변
- 정밀도: 출력 오차 허용 `1e-6` → `long double`과 소수점 12자리 출력 사용
- `t < s` 랩어라운드 처리(한 바퀴 보정)
- N이 큰 경우(≤ 2e5): O(100·logN)로 충분

## 제출 전 점검
- 출력 형식: `YES` 후 2줄, `j α` 와 `k β`(1-indexed, 12자리 고정 소수)
- 인덱스/모듈러 처리: `x[N+1]=x[1]` 가정 반영 여부
- 내분비 범위 보정: `α, β ∈ [0,1]`

## 참고자료
- 신발끈 공식: [Wikipedia](https://en.wikipedia.org/wiki/Shoelace_formula)
- 다각형 둘레/호길이 파라미터화 아이디어(계산기하 일반론)


