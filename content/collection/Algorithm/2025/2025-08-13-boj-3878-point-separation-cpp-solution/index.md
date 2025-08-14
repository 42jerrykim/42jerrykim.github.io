---
title: "[Algorithm] cpp 백준 3878번: 점 분리"
description: "볼록껍질과 선분 교차·포함 판정을 이용해 흰 점과 검은 점의 ‘직선에 의한 엄격 분리’ 가능 여부를 판단합니다. 접촉(점·변 포함)도 분리 불가로 처리하며, O((n+m) log(n+m))에 해결합니다."
date: 2025-08-13
lastmod: 2025-08-13
categories:
- "Algorithm"
- "Geometry"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-3878"
- "cpp"
- "C++"
- "Geometry"
- "기하"
- "Convex Hull"
- "볼록껍질"
- "Line Separation"
- "직선분리"
- "Linear Separability"
- "선형분리"
- "Polygon"
- "다각형"
- "Polygon Intersection"
- "다각형교차"
- "Segment Intersection"
- "선분교차"
- "CCW"
- "Cross Product"
- "외적"
- "Orientation"
- "방향성"
- "Point in Polygon"
- "점내부판정"
- "Monotone Chain"
- "모노톤체인"
- "Computational Geometry"
- "계산기하"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Implementation"
- "구현"
- "Optimization"
- "최적화"
- "Testing"
- "테스트"
- "Invariant"
- "불변식"
- "Separation Theorem"
- "분리정리"
- "Separating Line"
- "분리직선"
- "Strict Separation"
- "엄격분리"
- "Touching Case"
- "접촉케이스"
- "Degenerate Case"
- "특이케이스"
- "Integer Coordinates"
- "정수좌표"
- "Robustness"
- "견고성"
- "ICPC"
- "Regional-2009-Tokyo"
- "Asia Regional"
- "Editorial"
- "에디토리얼"
- "Code Review"
- "코드리뷰"
- "Competitive Programming"
- "경쟁프로그래밍"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/3878
- 요약: 평면상의 검은 점 집합과 흰 점 집합을 하나의 직선으로 서로 다른 반평면에 완전히 분리할 수 있는지 판별합니다. 직선은 어떤 점도 지나가면 안 되므로 접촉(점이나 변 위)에 해당해도 분리 불가입니다.

## 입력/출력
- 여러 테스트 케이스가 주어집니다. 각 케이스마다 검은 점 개수 `n`, 흰 점 개수 `m`이 주어지고, 이어서 각 점의 정수 좌표가 주어집니다.
- 각 케이스마다 분리가 가능하면 `YES`, 불가능하면 `NO`를 출력합니다.

## 접근 개요
- 직선으로 두 집합이 엄격히 분리되려면 두 집합의 볼록껍질이 서로 교차하거나 닿지 않아야 합니다. 즉, 두 볼록다각형이 완전히 서로 떨어져 있어야 합니다.
- 따라서 각 집합의 볼록껍질을 만들고, 다각형 간 교차(선분 교차, 한쪽 다각형이 다른 쪽 내부/경계 포함)를 검사해 접촉·교차가 있으면 `NO`, 전혀 없으면 `YES`입니다.

## 알고리즘
1. 검은 점, 흰 점 각각에 대해 단조 체인(Monotone Chain)으로 볼록껍질을 생성합니다. 퇴화(점·선분) 케이스도 그대로 유지합니다.
2. 두 볼록껍질에 대해 다음을 검사합니다.
   - 변-변 선분 교차가 있는가? (경계 접촉 포함)
   - 한 다각형의 임의 한 점이 다른 다각형 내부 또는 경계에 있는가? (점 포함 검사)
3. 위 조건 중 하나라도 참이면 접촉/교차이므로 `NO`. 전부 거짓이면 `YES`.

올바름 근거(요지): 두 집합의 선형 분리 가능성은 그 볼록껍질의 선형 분리 가능성과 동치입니다. 또, 한 점도 직선을 지나면 안 되므로 경계 접촉 역시 허용되지 않습니다.

## 복잡도
- 볼록껍질: O((n+m) log(n+m))
- 다각형 교차 검사: O(h_b · h_w) (각 껍질 꼭짓점 수)
- 전체: O((n+m) log(n+m))

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Point {
	long long x, y;
	bool operator<(const Point& other) const {
		if (x != other.x) return x < other.x;
		return y < other.y;
	}
	bool operator==(const Point& other) const {
		return x == other.x && y == other.y;
	}
};

static long long cross(const Point& a, const Point& b, const Point& c) {
	// (b - a) x (c - a)
	return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

static bool onSegment(const Point& a, const Point& b, const Point& p) {
	if (cross(a, b, p) != 0) return false;
	return min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
	       min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}

static bool segmentsIntersect(const Point& a, const Point& b, const Point& c, const Point& d) {
	long long ab_c = cross(a, b, c);
	long long ab_d = cross(a, b, d);
	long long cd_a = cross(c, d, a);
	long long cd_b = cross(c, d, b);

	if (ab_c == 0 && onSegment(a, b, c)) return true;
	if (ab_d == 0 && onSegment(a, b, d)) return true;
	if (cd_a == 0 && onSegment(c, d, a)) return true;
	if (cd_b == 0 && onSegment(c, d, b)) return true;

	bool ab_strict = (ab_c > 0 && ab_d < 0) || (ab_c < 0 && ab_d > 0);
	bool cd_strict = (cd_a > 0 && cd_b < 0) || (cd_a < 0 && cd_b > 0);
	return ab_strict && cd_strict;
}

static vector<Point> convexHull(vector<Point> pts) {
	if (pts.size() <= 1) return pts;
	sort(pts.begin(), pts.end());
	pts.erase(unique(pts.begin(), pts.end()), pts.end());
	if (pts.size() <= 1) return pts;

	vector<Point> lower, upper;
	for (const auto& p : pts) {
		while (lower.size() >= 2 && cross(lower[lower.size()-2], lower.back(), p) <= 0)
			lower.pop_back();
		lower.push_back(p);
	}
	for (int i = (int)pts.size() - 1; i >= 0; --i) {
		const auto& p = pts[i];
		while (upper.size() >= 2 && cross(upper[upper.size()-2], upper.back(), p) <= 0)
			upper.pop_back();
		upper.push_back(p);
	}
	lower.pop_back();
	upper.pop_back();
	lower.insert(lower.end(), upper.begin(), upper.end());
	return lower;
}

// Returns: 0 = outside, 1 = inside, 2 = on boundary
static int containsPointConvexOrDegenerate(const vector<Point>& poly, const Point& p) {
	int n = (int)poly.size();
	if (n == 0) return 0;
	if (n == 1) return (poly[0] == p) ? 2 : 0;
	if (n == 2) return onSegment(poly[0], poly[1], p) ? 2 : 0;

	bool hasPos = false, hasNeg = false;
	for (int i = 0; i < n; ++i) {
		const Point& a = poly[i];
		const Point& b = poly[(i + 1) % n];
		long long c = cross(a, b, p);
		if (c == 0 && onSegment(a, b, p)) return 2;
		if (c > 0) hasPos = true;
		if (c < 0) hasNeg = true;
		if (hasPos && hasNeg) return 0; // Outside for convex polygon
	}
	return 1; // Inside (all cross products have the same sign)
}

static bool polygonsIntersectOrTouch(const vector<Point>& A, const vector<Point>& B) {
	int na = (int)A.size(), nb = (int)B.size();

	// Handle degenerate sizes
	if (na == 0 || nb == 0) return false;

	if (na == 1 && nb == 1) return A[0] == B[0];
	if (na == 1) return containsPointConvexOrDegenerate(B, A[0]) != 0;
	if (nb == 1) return containsPointConvexOrDegenerate(A, B[0]) != 0;

	// Edge intersections
	auto edgeIntersects = [&](const vector<Point>& P, const vector<Point>& Q) {
		int n = (int)P.size(), m = (int)Q.size();
		for (int i = 0; i < n; ++i) {
			Point a = P[i], b = P[(i + 1) % n];
			for (int j = 0; j < m; ++j) {
				Point c = Q[j], d = Q[(j + 1) % m];
				if (segmentsIntersect(a, b, c, d)) return true;
			}
		}
		return false;
	};
	if (edgeIntersects(A, B)) return true;

	// Containment (A inside B or B inside A)
	if (containsPointConvexOrDegenerate(B, A[0]) != 0) return true;
	if (containsPointConvexOrDegenerate(A, B[0]) != 0) return true;

	return false;
}

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int T;
	if (!(cin >> T)) return 0;
	while (T--) {
		int n, m;
		cin >> n >> m;

		vector<Point> black(n), white(m);
		for (int i = 0; i < n; ++i) cin >> black[i].x >> black[i].y;
		for (int i = 0; i < m; ++i) cin >> white[i].x >> white[i].y;

		// If either set is empty, trivially separable
		if (n == 0 || m == 0) {
			cout << "YES\n";
			continue;
		}

		vector<Point> hb = convexHull(black);
		vector<Point> hw = convexHull(white);

		bool touchOrIntersect = polygonsIntersectOrTouch(hb, hw);
		// Strict linear separability exists iff convex hulls are disjoint (no touch, no intersection)
		cout << (touchOrIntersect ? "NO" : "YES") << "\n";
	}
	return 0;
}
```

## 코너 케이스 체크리스트
- 한쪽 집합이 1점/2점(퇴화 껍질)인 경우: 점 포함/선분 포함을 경계 포함으로 처리 → 분리 불가
- 두 껍질이 변·꼭짓점에서 ‘닿기만’ 하는 경우도 분리 불가
- 모든 좌표가 정수이므로 64-bit 정수 연산으로 외적 안전 처리

## 제출 전 점검
- 입력/출력 형식 및 개행 확인
- `long long` 범위, 초기화/인덱스 범위 점검
- 껍질 생성 시 중복 제거 및 퇴화 케이스 처리 확인


