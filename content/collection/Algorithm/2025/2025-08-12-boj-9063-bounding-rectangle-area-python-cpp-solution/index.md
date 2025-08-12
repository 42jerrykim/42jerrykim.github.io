---
title: "[BOJ] 9063 - Bounding Rectangle Area - Python/C++ Solution"
description: "백준 9063(축에 평행한 최소 직사각형) 문제를 Python/C++로 풉니다. 좌표의 최솟값·최댓값을 선형 스캔해 넓이를 구하고 N≤1은 0 처리. O(N) 복잡도와 입출력 최적화, 오버플로우 주의까지 정리."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "BOJ"
- "Algorithm"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "9063"
- "Bounding Rectangle"
- "Minimum Bounding Rectangle"
- "AABB"
- "Axis-Aligned Bounding Box"
- "Geometry"
- "Computational Geometry"
- "좌표기하"
- "직사각형"
- "최소직사각형"
- "넓이"
- "면적"
- "좌표"
- "좌표평면"
- "Points"
- "Min"
- "Max"
- "최소값"
- "최댓값"
- "스캔"
- "선형탐색"
- "O(N)"
- "시간복잡도"
- "구현"
- "수학"
- "Algorithm"
- "알고리즘"
- "Coding Test"
- "코딩테스트"
- "Competitive Programming"
- "CP"
- "Python"
- "파이썬"
- "C++"
- "씨플플"
- "STL"
- "ios::sync_with_stdio"
- "sys.stdin"
- "입력파싱"
- "Input Parsing"
- "Edge Cases"
- "엣지케이스"
- "N<=1"
- "Long Long"
- "정수 오버플로우"
- "Integer Overflow"
- "예제"
- "테스트케이스"
- "Solution"
- "풀이"
- "해설"
- "Problem Solving"
- "문제풀이"
- "Geometry Basics"
- "Rectangle Area"
- "Without Sorting"
- "No Data Structure"
image: "featured-image.jpg"
draft: true
---

### 문제 요약
- N개의 점이 주어질 때, 이 점들을 모두 포함하는 축에 평행한 최소 직사각형의 넓이를 구하라.
- N ≤ 1이면 넓이는 0이다.

### 접근 방법
- x좌표의 최솟값/최댓값, y좌표의 최솟값/최댓값을 한 번의 순회로 갱신한다.
- 넓이 = (max_x - min_x) × (max_y - min_y). 단, N ≤ 1이면 0을 출력.
- 시간복잡도 O(N), 추가 메모리 O(1).

### Python 풀이
```python
# 더 많은 정보는 https://42jerrykim.github.io 에서 확인하세요.
import sys

def main():
    input = sys.stdin.readline
    n_line = input().strip()
    if not n_line:
        print(0)
        return
    n = int(n_line)

    min_x = 10**18
    max_x = -10**18
    min_y = 10**18
    max_y = -10**18

    for _ in range(n):
        parts = input().split()
        if not parts:
            continue
        x, y = map(int, parts)
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y

    if n <= 1:
        print(0)
    else:
        print((max_x - min_x) * (max_y - min_y))

if __name__ == "__main__":
    main()
```

### C++ 풀이
```cpp
// 더 많은 정보는 https://42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) {
        cout << 0 << '\n';
        return 0;
    }

    long long min_x = LLONG_MAX, max_x = LLONG_MIN;
    long long min_y = LLONG_MAX, max_y = LLONG_MIN;

    for (long long i = 0; i < n; ++i) {
        long long x, y;
        cin >> x >> y;
        min_x = min(min_x, x);
        max_x = max(max_x, x);
        min_y = min(min_y, y);
        max_y = max(max_y, y);
    }

    if (n <= 1) {
        cout << 0 << '\n';
    } else {
        cout << (max_x - min_x) * (max_y - min_y) << '\n';
    }
    return 0;
}
```

### 복잡도
- 시간복잡도: O(N)
- 공간복잡도: O(1)

### 엣지 케이스
- N = 0, 1 → 0 출력
- 모든 점의 x 또는 y가 동일한 경우 → 한 변 길이가 0이므로 넓이 0

### 참고
- 문제: `[BOJ 9063]`(https://www.acmicpc.net/problem/9063)


