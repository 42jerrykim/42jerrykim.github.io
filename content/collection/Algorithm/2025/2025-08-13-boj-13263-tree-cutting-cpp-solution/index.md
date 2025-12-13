---
title: "[Algorithm] C++ 백준 13263번 : 나무 자르기"
description: "증가하는 높이 a와 감소하는 비용 b의 단조성을 활용해 점화식 dp[i]=min_{j<i}(dp[j]+b[j]*a[i])의 하한선을 직선 하포로 관리하고, CHT(단조 큐)로 O(n) 시간에 계산합니다. 교차 지점 비교와 128비트 연산으로 오버플로를 방지하며 구현 포인트와 정당성을 간명히 정리했습니다."
date: 2025-08-13
lastmod: 2025-08-13
categories:
- "Algorithm"
- "Dynamic Programming"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-13263"
- "cpp"
- "C++"
- "Dynamic Programming"
- "동적계획법"
- "DP Optimization"
- "DP 최적화"
- "Convex Hull Trick"
- "컨벡스 헐 트릭"
- "CHT"
- "Monotonic CHT"
- "단조 큐"
- "Li Chao Tree"
- "Li Chao"
- "Lower Envelope"
- "하한선"
- "Lines Container"
- "직선 집합"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Optimization"
- "최적화"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Editorial"
- "에디토리얼"
- "Code Review"
- "코드리뷰"
- "Template"
- "템플릿"
- "Testing"
- "테스트"
- "Complexity Analysis"
- "복잡도 분석"
- "Invariant"
- "불변식"
- "Greedy"
- "그리디"
- "Binary Search"
- "이분탐색"
- "Two Pointers"
- "투포인터"
- "Sliding Window"
- "슬라이딩윈도우"
- "Hashing"
- "해싱"
- "String"
- "문자열"
- "Geometry"
- "기하"
- "Math"
- "수학"
- "Modulo"
- "모듈러"
- "Debugging"
- "디버깅"
- "BOJ13263"
- "나무 자르기"
- "__int128"
- "64-bit"
- "오버플로 방지"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/13263
- 요약: 높이 배열 `a`와 충전 비용 배열 `b`가 각각 엄격 증가/감소합니다. 모든 나무를 0이 될 때까지 자를 때 필요한 총 충전 비용의 최솟값을 구합니다.

## 입력/출력
```
<입력>
n
a1 a2 ... an
b1 b2 ... bn

<출력>
최솟값
```

예시
```
입력
5
1 2 3 4 5
5 4 3 2 0

출력
25
```

## 접근 개요
- 핵심 점화식: `dp[i] = min_{j<i} (dp[j] + b[j] * a[i])`.
- 단조성: `a`는 엄격 증가, `b`는 엄격 감소 → 기울기 감소 직선 집합, 질의 `x=a[i]` 증가.
- 최적화: Convex Hull Trick을 단조 큐(two-pointer)로 구현해 각 `a[i]`에 대한 최소값을 O(1) 평균으로 갱신, 전체 O(n).

## 알고리즘 설계
- 선형함수 `y = m x + c`를 `m=b[j], c=dp[j]`로 해석하고, 최소 하한선(lower envelope)을 유지합니다.
- 두 직선의 교차 비교를 정수 산술로 처리하여 부동소수 오차를 제거합니다. 값 계산은 `__int128` 중간 연산으로 오버플로를 방지합니다.
- 정당성: `a` 증가로 질의가 왼→오 순서, `b` 감소로 기울기 단조 → 최적 직선 인덱스는 절대 뒤로 이동하지 않음. 따라서 앞선 직선을 유지하는 단조 큐로 전역 최소가 보장됩니다.

의사코드 요약
```
dp[1] = 0
hull = [{m=b[1], c=dp[1]}]; head=0
for i in 2..n:
    while head+1<hull.size and f(hull[head], a[i]) >= f(hull[head+1], a[i]): head++
    dp[i] = f(hull[head], a[i])
    cur = {m=b[i], c=dp[i]}
    while hull.size-head >= 2 and isBad(hull[-2], hull[-1], cur): pop_back()
    push_back(cur)
answer = dp[n]
```

## 복잡도
- 시간: O(n)
- 공간: O(n)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

struct Line { long long m, b; };

static inline __int128 eval128(const Line& l, long long x) {
    return (__int128)l.m * x + l.b;
}

static inline bool isBad(const Line& l1, const Line& l2, const Line& l3) {
    // (c2 - c1)/(m1 - m2) >= (c3 - c2)/(m2 - m3)  → l2는 필요 없음
    return (__int128)(l2.b - l1.b) * (l2.m - l3.m) >= (__int128)(l3.b - l2.b) * (l1.m - l2.m);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; cin >> n;
    vector<long long> a(n + 1), b(n + 1), dp(n + 1, 0);
    for (int i = 1; i <= n; ++i) cin >> a[i];
    for (int i = 1; i <= n; ++i) cin >> b[i];

    // dp[i] = min_{j<i} (dp[j] + b[j] * a[i])
    vector<Line> hull; hull.reserve(n);
    hull.push_back({b[1], dp[1]});
    int head = 0;

    for (int i = 2; i <= n; ++i) {
        while ((int)hull.size() - head >= 2 && eval128(hull[head], a[i]) >= eval128(hull[head + 1], a[i])) {
            ++head;
        }
        dp[i] = (long long)eval128(hull[head], a[i]);

        Line cur{b[i], dp[i]};
        while ((int)hull.size() - head >= 2 && isBad(hull[(int)hull.size() - 2], hull.back(), cur)) hull.pop_back();
        hull.push_back(cur);
    }

    cout << dp[n] << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- `a`는 엄격 증가, `b`는 엄격 감소라는 전제 확인(문제 보장).
- `n=1`일 때 `dp[1]=0`, 출력 `0`.
- 매우 큰 값: `a[i], b[i] ≤ 1e9` → 중간 계산은 `__int128`로 처리.
- 동일 기울기 없음(엄격 감소) → 동률 처리 분기 불필요.

## 제출 전 점검
- 입출력 개행/버퍼링 확인(`sync_with_stdio(false)`, `tie(nullptr)`).
- 인덱스 1-based 일관성 유지.
- 오버플로 방지: 비교와 합성은 128비트 사용 후 `long long` 캐스팅.

## 참고자료
- Convex Hull Trick(단조 CHT) 기본 개념, 직선 하한선 유지 및 포인터 전진 기법

