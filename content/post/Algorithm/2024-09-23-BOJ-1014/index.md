---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-23T00:00:00Z"
aliases: ["/algorithm/BOJ-1014/"]
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Dynamic Programming
- Bitmasking
- Memoization
- Optimization
- O(N^3)
- Arrays
- Masking
- Problem Solving
title: '[Algorithm] C++/Python 백준 1014번 : 컨닝'
---

서강대학교의 최백준 교수님은 "컨닝의 기술"이라는 과목을 가르치고 있다. 이 과목은 상당히 까다롭기로 유명하여, 일부 학생들은 시험 도중 다른 학생의 답안을 베끼려는 시도를 한다.

시험은 N행, M열의 직사각형 교실에서 진행되며, 각 칸은 학생이 앉을 수 있는 자리이다. 그러나 일부 학생들이 책상을 부숴버려서 앉을 수 없는 자리도 존재한다.

모든 학생은 **자신의 왼쪽**, **오른쪽**, **왼쪽 대각선 위**, **오른쪽 대각선 위**에 있는 학생의 답안을 베낄 수 있다고 가정한다. 따라서 학생들이 서로 컨닝을 할 수 없도록 자리를 배치해야 한다.

교실의 배치도가 주어졌을 때, 컨닝이 불가능하도록 최대한 많은 학생을 배치할 수 있는 최대 학생 수를 구하는 프로그램을 작성하시오.

**입력:**

첫째 줄에 테스트 케이스의 개수 C가 주어진다.

각 테스트 케이스는 두 부분으로 이루어져 있다.

- 첫 번째 줄: 교실의 세로 길이 N과 가로 길이 M이 주어진다. (1 ≤ N, M ≤ 10)
- 두 번째 부분: N개의 줄에 걸쳐 교실의 배치도가 주어진다. 각 줄은 M개의 문자로 이루어져 있으며, '.'은 앉을 수 있는 자리, 'x'는 앉을 수 없는 자리를 의미한다.

**출력:**

각각의 테스트 케이스마다 컨닝이 불가능하도록 학생을 배치했을 때, 배치할 수 있는 최대 학생 수를 출력한다.

**예제 입력:**

```
4
2 3
...
...
2 3
x.x
xxx
2 3
x.x
x.x
10 10
....x.....
..........
..........
..x.......
..........
x...x.x...
.........x
...x......
........x.
.x...x....
```

**예제 출력:**

```
4
1
2
46
```

**문제 링크:** [https://www.acmicpc.net/problem/1014](https://www.acmicpc.net/problem/1014)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제는 교실에 학생을 배치할 때, **컨닝이 불가능하도록 최대한 많은 학생을 배치하는 것**이 목표이다. 학생들이 컨닝을 할 수 없는 조건을 만족하면서 최대 학생 수를 찾기 위해 다음과 같은 알고리즘과 전략을 사용한다.

**사용된 알고리즘 및 전략**

- **동적 계획법(Dynamic Programming)**: 이전 상태의 결과를 이용하여 현재 상태의 결과를 계산함으로써 중복 계산을 방지한다.
- **비트마스킹(Bitmasking)**: 각 자리의 상태(학생이 앉았는지 여부)를 비트로 표현하여 효율적으로 상태를 관리한다.
- **메모이제이션(Memoization)**: 이미 계산한 상태를 저장하여 동일한 계산의 반복을 피한다.

**해결 방법**

1. **자리 배치의 상태 표현**: 각 행의 자리 배치를 비트마스크로 표현한다. 예를 들어, 3개의 자리에서 `101`은 첫 번째와 세 번째 자리에 학생이 앉았음을 의미한다.

2. **유효한 자리 배치 생성**: 한 행에서 가능한 모든 유효한 자리 배치를 생성한다. 유효한 자리 배치는 다음 조건을 만족해야 한다.
   - 학생이 앉을 수 없는 자리에 학생이 배치되지 않아야 한다.
   - 한 행에서 인접한 자리에 학생이 배치되지 않아야 한다.

3. **동적 계획법 적용**:
   - `dp[row][mask]`는 `row`번째 행까지 배치했을 때, 현재 행의 자리 배치가 `mask`일 때의 최대 학생 수를 저장한다.
   - 현재 행의 자리 배치와 이전 행의 자리 배치가 컨닝 조건을 만족하는지 확인한다.
     - 현재 행의 학생이 이전 행의 왼쪽 위 대각선이나 오른쪽 위 대각선에 앉은 학생과 컨닝할 수 없도록 해야 한다.
   - 이 조건을 만족하면 `dp` 테이블을 갱신한다.

4. **최대 학생 수 계산**: 모든 행에 대해 동적 계획법을 수행한 후, 마지막 행의 모든 상태 중 최대 값을 선택한다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstring>

using namespace std;

const int MAX_N = 12; // 최대 행 수
const int MAX_M = 12; // 최대 열 수
const int MAX_STATE = 1 << MAX_M; // 가능한 상태 수 (2^M)

int N, M; // 교실의 크기
char classroom[MAX_N][MAX_M]; // 교실의 자리 정보
vector<int> valid_masks[MAX_N]; // 각 행에서 가능한 유효한 자리 배치
int dp[MAX_N + 1][MAX_STATE]; // 동적 계획법 테이블

// 비트마스크에서 1의 개수를 세는 함수
int count_bits(int mask) {
    int count = 0;
    while (mask) {
        count++;
        mask &= (mask - 1); // 최하위 비트 제거
    }
    return count;
}

// 해당 행에서의 자리 배치(mask)가 유효한지 확인하는 함수
bool is_valid_mask(int row, int mask) {
    for (int j = 0; j < M; ++j) {
        if (mask & (1 << j)) { // 학생이 앉는 자리라면
            if (classroom[row][j] == 'x') return false; // 앉을 수 없는 자리
            if (j > 0 && (mask & (1 << (j - 1)))) return false; // 왼쪽에 학생이 있는 경우
        }
    }
    return true;
}

int main() {
    int C; // 테스트 케이스 수
    cin >> C;
    while (C--) {
        cin >> N >> M;
        for (int i = 0; i < N; ++i) {
            cin >> classroom[i]; // 교실 배치 입력
            valid_masks[i].clear(); // 유효한 마스크 초기화
        }
        // 각 행에서 가능한 유효한 자리 배치 생성
        for (int i = 0; i < N; ++i) {
            for (int mask = 0; mask < (1 << M); ++mask) {
                if (is_valid_mask(i, mask)) {
                    valid_masks[i].push_back(mask);
                }
            }
        }
        memset(dp, -1, sizeof(dp)); // DP 테이블 초기화
        dp[0][0] = 0; // 초기 상태
        // 동적 계획법 진행
        for (int row = 0; row < N; ++row) {
            for (int prev_mask = 0; prev_mask < (1 << M); ++prev_mask) {
                if (dp[row][prev_mask] == -1) continue; // 이전 상태가 유효하지 않으면 패스
                for (int curr_mask : valid_masks[row]) {
                    // 이전 행과 현재 행의 자리 배치가 컨닝 조건을 만족하는지 확인
                    if ((curr_mask & (prev_mask << 1)) == 0 && (curr_mask & (prev_mask >> 1)) == 0) {
                        int curr_count = count_bits(curr_mask); // 현재 행에서 앉은 학생 수
                        // 최대 학생 수 갱신
                        if (dp[row + 1][curr_mask] < dp[row][prev_mask] + curr_count) {
                            dp[row + 1][curr_mask] = dp[row][prev_mask] + curr_count;
                        }
                    }
                }
            }
        }
        // 결과 계산
        int result = 0;
        for (int mask = 0; mask < (1 << M); ++mask) {
            if (dp[N][mask] > result) {
                result = dp[N][mask];
            }
        }
        cout << result << endl; // 최대 학생 수 출력
    }
    return 0;
}
```

**코드의 동작 설명:**

1. **입력 처리 및 초기화**:
   - 테스트 케이스 수 `C`를 입력받는다.
   - 각 테스트 케이스마다 교실의 크기 `N`, `M`과 교실 배치 `classroom`을 입력받는다.
   - `valid_masks`를 초기화하여 각 행에서 가능한 유효한 자리 배치를 저장할 준비를 한다.

2. **유효한 자리 배치 생성**:
   - 각 행에 대해 가능한 모든 자리 배치(0부터 `2^M - 1`까지의 비트마스크)를 검사한다.
   - `is_valid_mask` 함수를 통해 해당 자리 배치가 유효한지 확인한다.
     - 앉을 수 없는 자리에 학생이 앉아 있으면 유효하지 않다.
     - 같은 행에서 인접한 두 자리에 학생이 앉아 있으면 유효하지 않다.
   - 유효한 자리 배치는 `valid_masks`에 저장된다.

3. **동적 계획법(DP) 수행**:
   - `dp` 배열을 `-1`로 초기화하고, `dp[0][0]`을 `0`으로 설정한다.
   - 각 행에 대해 이전 행의 모든 유효한 자리 배치(`prev_mask`)를 순회한다.
   - 현재 행의 모든 유효한 자리 배치(`curr_mask`)를 순회하면서 다음을 확인한다.
     - 이전 행과 현재 행의 자리 배치가 컨닝 조건을 만족하는지 확인한다.
       - `curr_mask & (prev_mask << 1)`과 `curr_mask & (prev_mask >> 1)`가 모두 `0`이어야 한다.
       - 이는 현재 행의 학생이 이전 행의 왼쪽 위 또는 오른쪽 위 대각선에 있는 학생과 겹치지 않음을 의미한다.
     - 조건을 만족하면 `dp[row + 1][curr_mask]`를 갱신한다.
       - `dp[row + 1][curr_mask] = max(dp[row + 1][curr_mask], dp[row][prev_mask] + 현재 행의 학생 수)`

4. **결과 계산 및 출력**:
   - 마지막 행의 모든 자리 배치에 대해 최대 학생 수를 계산한다.
   - 결과를 출력한다.

## C++ without library 코드와 설명

`stdio.h`와 `malloc.h`만을 사용하여 코드를 작성하면 다음과 같다:

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_N 12
#define MAX_M 12
#define MAX_STATE (1 << MAX_M)

int N, M;
char classroom[MAX_N][MAX_M + 1];
int valid_masks[MAX_N][MAX_STATE];
int valid_mask_count[MAX_N];
int dp[MAX_N + 1][MAX_STATE];

int count_bits(int mask) {
    int count = 0;
    while (mask) {
        count++;
        mask &= (mask - 1); // 최하위 비트 제거
    }
    return count;
}

int is_valid_mask(int row, int mask) {
    int prev = -2;
    for (int j = 0; j < M; ++j) {
        if (mask & (1 << j)) {
            if (classroom[row][j] == 'x') return 0; // 앉을 수 없는 자리
            if (j - prev == 1) return 0; // 인접한 학생
            prev = j;
        }
    }
    return 1;
}

int main() {
    int C;
    scanf("%d", &C);
    while (C--) {
        scanf("%d %d", &N, &M);
        for (int i = 0; i < N; ++i) {
            scanf("%s", classroom[i]);
            valid_mask_count[i] = 0;
        }
        for (int i = 0; i < N; ++i) {
            for (int mask = 0; mask < (1 << M); ++mask) {
                if (is_valid_mask(i, mask)) {
                    valid_masks[i][valid_mask_count[i]++] = mask;
                }
            }
        }
        memset(dp, -1, sizeof(dp));
        dp[0][0] = 0;
        for (int row = 0; row < N; ++row) {
            for (int prev_mask = 0; prev_mask < (1 << M); ++prev_mask) {
                if (dp[row][prev_mask] == -1) continue;
                for (int k = 0; k < valid_mask_count[row]; ++k) {
                    int curr_mask = valid_masks[row][k];
                    if ((curr_mask & (prev_mask << 1)) == 0 && (curr_mask & (prev_mask >> 1)) == 0) {
                        int curr_count = count_bits(curr_mask);
                        if (dp[row + 1][curr_mask] < dp[row][prev_mask] + curr_count) {
                            dp[row + 1][curr_mask] = dp[row][prev_mask] + curr_count;
                        }
                    }
                }
            }
        }
        int result = 0;
        for (int mask = 0; mask < (1 << M); ++mask) {
            if (dp[N][mask] > result) {
                result = dp[N][mask];
            }
        }
        printf("%d\n", result);
    }
    return 0;
}
```

**코드의 동작 설명:**

- **헤더 파일 및 상수 정의**:
  - 표준 입출력과 메모리 관리를 위한 헤더 파일 `stdio.h`, `stdlib.h`, `string.h`를 포함한다.
  - 최대 행 수 `MAX_N`, 최대 열 수 `MAX_M`, 최대 상태 수 `MAX_STATE`를 정의한다.

- **전역 변수 선언**:
  - 교실 크기 `N`, `M`과 교실 배치 `classroom`을 선언한다.
  - 각 행에서의 유효한 마스크를 저장할 `valid_masks`와 그 개수를 저장할 `valid_mask_count`를 선언한다.
  - 동적 계획법 테이블 `dp`를 선언한다.

- **비트 개수 세기 함수 `count_bits`**:
  - 비트마스크에서 설정된 비트(학생 수)의 개수를 센다.

- **유효한 마스크 검사 함수 `is_valid_mask`**:
  - 주어진 행에서의 자리 배치가 유효한지 검사한다.
  - 인접한 자리에 학생이 앉아있지 않고, 앉을 수 없는 자리에 학생이 앉지 않아야 한다.

- **메인 함수**:
  - 테스트 케이스 수를 입력받는다.
  - 각 테스트 케이스마다 입력을 처리하고, 유효한 마스크를 생성한다.
  - 동적 계획법을 수행하여 최대 학생 수를 계산한다.
  - 결과를 출력한다.

- **차이점**:
  - C++의 `vector`와 같은 STL을 사용할 수 없으므로, 배열과 직접적인 메모리 관리를 통해 구현한다.
  - `memset`과 같은 C 표준 라이브러리 함수를 사용한다.

## 결론

이 문제는 **동적 계획법과 비트마스킹**을 결합하여 효율적으로 해결할 수 있었다. 각 행의 자리 배치를 비트마스크로 표현하고, 컨닝 조건을 만족하는지 검사하여 상태를 전이하는 방식이 핵심이었다.

문제를 풀면서 상태 공간을 효율적으로 관리하는 방법과, 메모이제이션을 통해 중복 계산을 피하는 동적 계획법의 중요성을 다시 한번 느낄 수 있었다.

추가적으로, C++에서 표준 라이브러리를 사용하지 않고도 동일한 알고리즘을 구현할 수 있었다.

이번 문제를 통해 복잡한 조건이 있는 최적화 문제에서도 알고리즘의 기본 원칙을 적용하면 해결할 수 있음을 알게 되었다.