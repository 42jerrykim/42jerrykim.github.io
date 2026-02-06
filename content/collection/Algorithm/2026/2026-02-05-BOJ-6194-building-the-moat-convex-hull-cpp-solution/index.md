---
title: "[Algorithm] C++ 백준 6194번: Building the Moat"
description: "모든 점을 둘러싸는 최소 길이의 폐곡선은 점들의 볼록 껍질(Convex Hull) 둘레와 같다. Andrew monotonic chain으로 hull을 구해 인접 변 길이를 합산해 두 자리까지 출력한다."
date: 2026-02-05
lastmod: 2026-02-05
categories:
- "Algorithm"
- "BOJ"
- "Computational Geometry"
- "Convex Hull"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "Baekjoon"
- "백준"
- "6194"
- "BOJ-6194"
- "Problem-6194"
- "Building the Moat"
- "모트 만들기"
- "USACO"
- "USA Computing Olympiad"
- "Computational Geometry"
- "계산기하"
- "Geometry"
- "기하"
- "Convex Hull"
- "볼록 껍질"
- "Convex Hull Perimeter"
- "볼록 껍질 둘레"
- "Andrew Monotonic Chain"
- "모노토닉 체인"
- "Graham Scan"
- "그레이엄 스캔"
- "CCW"
- "반시계"
- "Cross Product"
- "외적"
- "Orientation Test"
- "방향 판정"
- "Polygon"
- "다각형"
- "Perimeter"
- "둘레"
- "Euclidean Distance"
- "유클리드 거리"
- "Sorting"
- "정렬"
- "O(N log N)"
- "NlogN"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Implementation"
- "구현"
- "Precision"
- "정밀도"
- "Floating Point"
- "부동소수점"
- "Long Double"
- "롱 더블"
- "Two Decimals"
- "소수점 둘째 자리"
- "Edge Case"
- "엣지 케이스"
- "No Collinear"
- "세 점 일직선 없음"
- "Integer Coordinates"
- "정수 좌표"
- "Closed Loop"
- "폐곡선"
- "Minimal Fence"
- "최소 둘레"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Problem Solving"
- "문제해결"
- "Coding Test"
- "코딩테스트"
image: "wordcloud.png"
---

문제: [BOJ 6194 - Building the Moat](https://www.acmicpc.net/problem/6194)

이 문제의 “최단 길이의 moat(폐곡선)”은 결국 **점들을 모두 포함하는 볼록 다각형의 최소 둘레**이고, 이는 점 집합의 **볼록 껍질(Convex Hull) 둘레**와 같습니다.  
따라서 볼록 껍질을 만든 뒤, 변 길이를 모두 더해서 소수 둘째 자리까지 출력하면 됩니다.

## 문제 정보

**문제 링크**: [https://www.acmicpc.net/problem/6194](https://www.acmicpc.net/problem/6194)

**문제 요약**:
- \(N\)개의 점(우물)이 주어진다.
- 모든 점이 다각형 위 또는 내부에 포함되도록, 점들 사이를 직선으로 연결한 **폐곡선**을 만든다.
- 그 길이(둘레)의 최솟값을 구해 소수점 둘째 자리까지 출력한다.

**제한 조건**:
- 시간 제한: 1초
- 메모리 제한: 128MB
- \(8 \le N \le 5{,}000\)
- 좌표 범위: \(1..45{,}000\)
- 어떤 세 점도 한 직선 위에 놓이지 않음

## 입출력 예제

**입력 1**:

```text
20
2 10
3 7
22 15
12 11
20 3
28 9
1 12
9 3
14 14
25 6
8 1
25 1
28 4
24 12
4 15
13 5
26 5
21 11
24 4
1 8
```

**출력 1**:

```text
70.87
```

## 접근 방식

### 핵심 관찰

- 모든 점을 둘러싸는 최소 둘레의 폐곡선은, 점들을 꼭짓점으로 하는 어떤 단순 다각형 중에서도 **볼록 다각형**에서 최솟값을 갖습니다.
- 그리고 “주어진 점들을 포함하는 최소 볼록 다각형”은 바로 **볼록 껍질(Convex Hull)** 입니다.
- 결국 답은 **Convex Hull의 둘레**입니다.

즉, 해야 할 일은:
- 점들을 정렬한 뒤
- Andrew monotonic chain으로 볼록 껍질(반시계 순서)을 구하고
- 인접한 점 사이 거리의 합을 출력

입니다.

### 알고리즘 설계 (Mermaid Flowchart)

```mermaid
flowchart TD
    A["입력: N과 점들 (x, y)"] --> B["점 정렬: x 오름차순, y 오름차순"]
    B --> C["아래쪽 껍질 생성</br>while \"cross <= 0\" 이면 pop"]
    C --> D["위쪽 껍질 생성</br>while \"cross <= 0\" 이면 pop"]
    D --> E["중복 끝점 제거 후 hull 완성"]
    E --> F["둘레 계산: Σ dist(hull[i], hull[i+1])"]
    F --> G["소수점 둘째 자리로 출력"]
```

### 단계별 로직

1. **정렬**: 점들을 \((x, y)\) 사전순으로 정렬합니다.
2. **아래 hull**: 왼쪽에서 오른쪽으로 훑으며, 마지막 두 점과 새 점이 “우회전/일직선(비볼록)”이면 pop합니다.
3. **위 hull**: 오른쪽에서 왼쪽으로 훑으며 동일하게 pop합니다.
4. **둘레 계산**: hull이 \(m\)개 점일 때, \(\sum_{i=0}^{m-1} \text{dist}(h[i], h[(i+1)\bmod m])\).

> 이 문제는 “세 점이 일직선”이 없으므로, collinear 처리로 인한 애매함이 없고 깔끔하게 동작합니다.

## 정당성(간단 설명)

- 볼록 껍질은 주어진 점들을 모두 포함하는 볼록 다각형 중 면적/둘레 관점에서 “가장 바깥 경계”를 이룹니다.
- 어떤 점이 hull 바깥에 존재하면 그 점을 포함하도록 경계를 바깥으로 이동해야 하므로 둘레가 줄어들 수 없습니다.
- 따라서 최단 moat의 경계는 hull의 경계와 일치하며, 답은 hull 둘레입니다.

## 복잡도 분석

| 항목 | 복잡도 | 비고 |
|---|---|---|
| **시간 복잡도** | \(O(N \log N)\) | 정렬 \(O(N \log N)\) + hull 구성 \(O(N)\) |
| **공간 복잡도** | \(O(N)\) | 점 배열 + hull |

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **정밀도** | 제곱근 합산 오차 | `long double`로 합산 후 `setprecision(2)` |
| **중복 점** | 문제는 unique 보장 | 별도 처리 불필요(있으면 정렬 후 중복 제거 권장) |
| **hull 크기** | 최소 3 | \(N \ge 8\), collinear 없음이라 hull이 안정적 |
| **CCW 판정 부호** | pop 조건 실수 | monotonic chain에서 `cross <= 0` 사용(반시계 hull) |

## 구현 코드 (C++)

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다
#include <bits/stdc++.h>
using namespace std;

struct Point {
    long long x, y;
    bool operator<(const Point& other) const {
        if (x != other.x) return x < other.x;
        return y < other.y;
    }
};

static long long cross(const Point& O, const Point& A, const Point& B) {
    return (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x);
}

static long double dist(const Point& a, const Point& b) {
    long double dx = (long double)a.x - (long double)b.x;
    long double dy = (long double)a.y - (long double)b.y;
    return sqrtl(dx * dx + dy * dy);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;
    vector<Point> p(N);
    for (int i = 0; i < N; i++) cin >> p[i].x >> p[i].y;

    sort(p.begin(), p.end());

    vector<Point> H;
    H.reserve(2 * N);

    // Lower hull
    for (int i = 0; i < N; i++) {
        while ((int)H.size() >= 2 && cross(H[H.size() - 2], H.back(), p[i]) <= 0) H.pop_back();
        H.push_back(p[i]);
    }

    // Upper hull
    size_t lowerSize = H.size();
    for (int i = N - 2; i >= 0; i--) {
        while (H.size() > lowerSize && cross(H[H.size() - 2], H.back(), p[i]) <= 0) H.pop_back();
        H.push_back(p[i]);
        if (i == 0) break; // prevent i underflow
    }

    // Last point equals first point
    if (!H.empty()) H.pop_back();

    long double perim = 0.0L;
    int M = (int)H.size();
    for (int i = 0; i < M; i++) {
        perim += dist(H[i], H[(i + 1) % M]);
    }

    cout << fixed << setprecision(2) << (double)perim << "\n";
    return 0;
}
```

## 참고 문헌 및 출처

- [백준 6194번 문제](https://www.acmicpc.net/problem/6194)

## 작성 체크리스트

- [x] 폴더명이 `YYYY-MM-DD-BOJ-번호-슬러그` 형식인가?
- [x] Front Matter의 tags가 50개 이상인가? (한글/영어 포함)
- [x] description이 150자 내외로 핵심을 요약했는가?
- [x] Mermaid 다이어그램으로 로직을 시각화했는가? (라벨 따옴표 규칙 준수)
- [x] 복잡도 분석이 표(Table) 형식인가?
- [x] 코드 최상단에 지정 주석이 포함되었는가?
- [x] 코너 케이스 체크리스트가 포함되었는가?
- [x] `date`와 `lastmod`가 오늘 날짜(2026-02-05)로 설정되었는가?

