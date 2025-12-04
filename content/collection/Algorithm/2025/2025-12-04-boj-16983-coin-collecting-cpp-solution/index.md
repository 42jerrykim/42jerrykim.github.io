---
title: "[Algorithm] C++ 백준 16983번: Coin Collecting"
date: 2025-12-04
lastmod: 2025-12-04
categories:
  - Algorithm
  - Greedy
tags: ["Algorithm", "C++", "Baekjoon", "BOJ", "Problem Solving", "Coin Collecting", "JOI", "Greedy", "Implementation", "Simulation", "Optimization", "16983", "Coding Test", "Competitive Programming", "Data Structure", "Math", "Geometry", "Manhattan Distance", "Grid", "Coordinates", "Flow", "Constructive", "Min Cost", "Efficiency", "Programming", "Source Code", "Solution", "Explanation", "Computer Science", "Software Engineering", "ICPC", "Olympiad", "Education", "Study", "Logic", "Reasoning", "Thinking", "Development", "Coding", "Practice", "Challenge", "Skill", "Knowledge", "Learning", "Tutorial", "Guide", "Reference", "Tips", "Review", "Analysis", "Strategy", "Technique"]
description: "백준 16983번 Coin Collecting 문제는 2N개의 동전을 Nx2 격자에 배치하는 최소 이동 횟수를 구하는 문제입니다. 그리디 알고리즘을 통해 각 열의 동전 과부족을 계산하고, 수직 및 수평 이동을 최적화하여 문제를 해결하는 C++ 정답 코드와 상세한 풀이를 제공합니다."
image: "wordcloud.png"
---

## 문제 정보

*   **문제 링크**: [https://www.acmicpc.net/problem/16983](https://www.acmicpc.net/problem/16983)
*   **요약**: $2N$개의 동전을 $N \times 2$ 격자 ($1 \le x \le N, 1 \le y \le 2$)의 각 칸에 정확히 하나씩 배치하기 위한 최소 이동 횟수를 구하는 문제입니다.
*   **제한**: 시간 제한 1초, 메모리 제한 512MB. $N \le 100,000$. 좌표 범위 $-10^9 \sim 10^9$.

## 입출력 형식/예제

입력으로 동전의 개수 $N$과 $2N$개의 동전 좌표가 주어집니다. 출력으로 최소 이동 횟수를 출력합니다.

```text
// 예제 입력 1
3
0 0
0 4
4 0
2 1
2 5
-1 1

// 예제 출력 1
15
```

---

## 접근 개요(아이디어 스케치)

이 문제는 전체 상태를 고려하는 탐색이나 DP보다는, 국소적인 최적해가 전역 최적해로 이어지는 **그리디(Greedy)** 방식으로 접근해야 합니다. 동전을 "어떤 순서"로 옮기느냐보다 "각 열(Column)에서의 과부족 상태"를 해소하며 지나가는 관점이 중요합니다.

1.  **좌표 압축(정규화)**: 목표 영역 밖의 동전은 무조건 경계까지 이동해야 하므로 미리 이동시킵니다.
2.  **스위핑(Sweeping)**: 왼쪽 열부터 오른쪽으로 진행하며, 현재 열의 1행, 2행에 필요한 동전의 수를 맞춥니다.
3.  **유량 제어(Flow Control)**: 남거나 부족한 동전은 오른쪽 열로 넘깁니다. 이때 수직 이동으로 상하 균형을 맞추는 것이 이동 비용을 줄이는 핵심입니다.

```mermaid
graph TD
    A[시작] --> B[좌표 정규화: 1<=X<=N, 1<=Y<=2 범위로 보정]
    B --> C[비용 누적: 정규화 과정의 거리 합산]
    C --> D[각 열 순회 x=1 to N]
    D --> E{각 행의 누적 과부족 b1, b2 계산}
    E --> F{부호가 다른가? b1*b2 < 0}
    F -- Yes --> G[수직 이동으로 상쇄: min|b1|,|b2| 만큼 이동]
    F -- No --> H[수직 이동 없음]
    G --> I[수평 이동 비용 추가: |b1| + |b2|]
    H --> I
    I --> J[다음 열로 진행]
    J --> K[최종 비용 출력]
```

---

## 알고리즘 설계

1.  **초기화 및 입력 처리**:
    *   $N$과 동전 좌표를 입력받습니다.
    *   좌표가 $1 \le x \le N$, $1 \le y \le 2$ 범위를 벗어나면 경계값으로 보정하고, 그 거리만큼 정답(`ans`)에 더합니다.
    *   보정된 좌표를 기준으로 `cnt[x][y]` 배열에 동전 개수를 기록합니다.

2.  **그리디 순회**:
    *   $x = 1$부터 $N$까지 순회하며 두 개의 누적 변수 `b1`, `b2`를 관리합니다.
    *   `b1`: 1행에서 현재까지 누적된 동전의 잉여/부족 개수.
    *   `b2`: 2행에서 현재까지 누적된 동전의 잉여/부족 개수.
    *   각 열에서 `b1 += (cnt[x][1] - 1)`, `b2 += (cnt[x][2] - 1)`을 수행합니다.

3.  **최적화 로직 (핵심)**:
    *   만약 `b1`과 `b2`의 부호가 다르다면(하나는 남고 하나는 부족), **수직 이동**을 통해 서로 상쇄하는 것이 이득입니다.
    *   수직 이동 횟수 `move = min(abs(b1), abs(b2))`를 정답에 더하고, `b1`, `b2` 값을 갱신합니다.
    *   상쇄 후 남은 `b1`, `b2`의 절댓값 합(`abs(b1) + abs(b2)`)은 다음 열로 넘어가야 하는 **수평 이동** 횟수가 되므로 정답에 더합니다.

---

## 복잡도 분석

*   **시간 복잡도**: $O(N)$
    *   입력을 받으며 정규화하는 데 $O(N)$, 1부터 $N$까지 순회하며 연산하는 데 $O(N)$이 소요됩니다.
*   **공간 복잡도**: $O(N)$
    *   동전의 개수를 저장하기 위한 `cnt` 배열의 크기가 $N$에 비례합니다.

---

## C++ 정답 코드

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

using namespace std;

int N;
long long ans = 0;
int cnt[100005][3]; // cnt[x][y]: x열 y행에 있는 동전의 개수

int main() {
    // 입출력 속도 향상
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    cin >> N;

    for (int i = 0; i < 2 * N; ++i) {
        int x, y;
        cin >> x >> y;

        // X 좌표 정규화 (1 ~ N 범위로 보정)
        if (x < 1) {
            ans += (1 - x);
            x = 1;
        } else if (x > N) {
            ans += (x - N);
            x = N;
        }

        // Y 좌표 정규화 (1 ~ 2 범위로 보정)
        if (y < 1) {
            ans += (1 - y);
            y = 1;
        } else if (y > 2) {
            ans += (y - 2);
            y = 2;
        }

        cnt[x][y]++;
    }

    long long b1 = 0; // 1행의 누적 과부족 (양수: 잉여, 음수: 부족)
    long long b2 = 0; // 2행의 누적 과부족

    for (int i = 1; i <= N; ++i) {
        // 현재 열의 동전 개수를 반영하여 과부족 갱신
        b1 += (cnt[i][1] - 1);
        b2 += (cnt[i][2] - 1);

        // 1행과 2행의 과부족 부호가 다르면 수직 이동으로 상쇄
        // 예: 1행은 남고(+), 2행은 부족(-)하면 1행 -> 2행으로 이동
        if (b1 > 0 && b2 < 0) {
            long long move = min(b1, -b2);
            ans += move; // 수직 이동 비용 추가
            b1 -= move;
            b2 += move;
        } else if (b1 < 0 && b2 > 0) {
            long long move = min(-b1, b2);
            ans += move; // 수직 이동 비용 추가
            b1 += move;
            b2 -= move;
        }

        // 남은 과부족만큼 다음 열로 수평 이동
        ans += abs(b1) + abs(b2);
    }

    cout << ans << endl;

    return 0;
}
```

---

## 코너 케이스 체크리스트

*   [x] **최소 $N$ ($N=1$)**: 입력 루프와 로직이 $N=1$일 때도 정상 동작하는가?
*   [x] **좌표 범위**: $X, Y$ 좌표가 음수이거나 매우 큰 경우(`long long` 필요성, 정규화 로직) 처리되었는가?
*   [x] **모든 동전이 한곳에 몰려있는 경우**: 누적 변수 `b1`, `b2`가 커질 때 오버플로우가 발생하지 않는가? (`long long` 사용)
*   [x] **이미 정답인 상태**: 이동 횟수가 0으로 출력되는가?

---

## 제출 전 점검

1.  **자료형**: 답(`ans`)과 누적 변수(`b1`, `b2`)는 $2N \times N$ 정도까지 커질 수 있으므로 `long long`을 사용해야 합니다.
2.  **배열 크기**: $N=100,000$이므로 `cnt` 배열은 `100005` 이상의 크기를 가져야 합니다.
3.  **입출력**: 많은 양의 입력을 처리하므로 `ios_base::sync_with_stdio(false); cin.tie(NULL);`을 사용합니다.

---

## 참고자료/유사문제

* [백준 2138번: 전구와 스위치](https://www.acmicpc.net/problem/2138)
* [백준 11000번: 강의실 배정](https://www.acmicpc.net/problem/11000)
