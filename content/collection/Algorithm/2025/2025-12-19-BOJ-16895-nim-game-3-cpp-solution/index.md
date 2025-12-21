---
title: "[Algorithm] C++ 백준 16895번: 님 게임 3"
description: "전체 돌더미의 XOR(님합)이 0이면 선공은 필패다. 아니면 어떤 더미 pi를 pi^X로 줄여 님합을 0으로 만드는 모든 첫 수가 승리 수이며, 이를 O(N)으로 센다."
date: 2025-12-19
lastmod: 2025-12-19
categories:
- "Algorithm"
- "BOJ"
- "Game Theory"
- "Bitwise"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "Baekjoon"
- "백준"
- "16895"
- "BOJ-16895"
- "님 게임 3"
- "Nim Game 3"
- "Nim"
- "님 게임"
- "Game Theory"
- "게임 이론"
- "Combinatorial Game"
- "조합 게임"
- "Impartial Game"
- "공정 게임"
- "Normal Play"
- "정상 규칙"
- "Winning Strategy"
- "승리 전략"
- "Optimal Play"
- "최적 플레이"
- "Perfect Play"
- "완전 플레이"
- "Winning Move"
- "승리 수"
- "First Move"
- "첫 수"
- "Move Counting"
- "수 세기"
- "Counting"
- "경우의 수"
- "Nim-sum"
- "님합"
- "XOR"
- "Bitwise XOR"
- "비트 XOR"
- "Bitwise"
- "비트연산"
- "Exclusive OR"
- "배타적 논리합"
- "Invariant"
- "불변식"
- "Proof"
- "증명"
- "Greedy"
- "그리디"
- "Mathematics"
- "수학"
- "Discrete Mathematics"
- "이산수학"
- "Sprague-Grundy"
- "스프라그-그런디"
- "Grundy Number"
- "그런디 수"
- "Take-Away Game"
- "제거 게임"
- "Pile Game"
- "더미 게임"
- "Stone Piles"
- "돌 더미"
- "Strategy"
- "전략"
- "Implementation"
- "구현"
- "Input Parsing"
- "입력 파싱"
- "Complexity"
- "복잡도"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "O(N)"
- "Constraints"
- "제한"
- "N<=1000"
- "Pi<=1000"
- "Competitive Programming"
- "경쟁 프로그래밍"
- "Problem Solving"
- "문제해결"
- "Coding Test"
- "코딩테스트"
- "C++"
image: "wordcloud.png"
---

## 문제 정보

**문제 링크**: [https://www.acmicpc.net/problem/16895](https://www.acmicpc.net/problem/16895)

**문제 요약**:
돌 더미가 \(N\)개 있고, 한 턴에 돌이 있는 더미 하나를 골라 돌을 1개 이상 제거한다. 마지막 돌을 가져가는 사람이 승리한다(구사과 선공).
두 사람이 최적으로 플레이할 때, **구사과가 첫 턴에 선택할 수 있는 “승리하는 첫 수”의 개수**를 출력한다.

**제한 조건**:
- 시간 제한: 1초
- 메모리 제한: 512MB
- \(1 \le N \le 1000\)
- \(1 \le P_i \le 1000\)

## 입출력 예제

**입력**:

```text
3
11 15 8
```

**출력**:

```text
3
```

## 접근 방식

### 핵심 관찰

님 게임(정상 규칙, impartial game)의 표준 정리:
- 모든 더미 크기의 XOR 값을 \(X\)라고 하면, \(X=0\)인 상태는 **패배 상태**(선 플레이어 필패)이다.
- \(X \ne 0\)이면, 어떤 더미 \(p_i\)를 \(p_i' = p_i \oplus X\)로 바꿔서(즉 \(p_i'\)만 남도록 돌을 제거) XOR를 0으로 만드는 수가 존재하며, 그런 수는 모두 **승리 수**다.

따라서 “첫 수로 이길 수 있는 방법 수”는 다음을 세면 된다.
- \(X = p_1 \oplus p_2 \oplus \cdots \oplus p_N\)
- \(X=0\)이면 답은 0
- \(X \ne 0\)이면, 각 더미에 대해 \(t = p_i \oplus X\)를 계산해서 \(t < p_i\)인 경우의 개수를 센다.
  - 이때 \(p_i\)에서 \(p_i - t\)개를 제거하면 새로운 XOR가 0이 된다.

### 알고리즘 흐름(mermaid)

```mermaid
flowchart TD
    A["입력: N, P 배열"] --> B["전체 XOR 계산"]
    B --> C{"XOR가 0인가"}
    C -->|"예"| D["정답 0 출력"]
    C -->|"아니오"| E["각 더미에 대해 t = pi XOR X 계산"]
    E --> F{"t가 pi보다 작은가"}
    F -->|"예"| G["정답 카운트 증가"]
    F -->|"아니오"| H["다음 더미"]
    G --> H
    H --> I["모든 더미 처리 후 정답 출력"]
```

## 정당성(간단 증명)

- \(X=0\)인 상태에서 어떤 한 더미를 줄이면 전체 XOR는 0이 아니게 된다. 즉 다음 플레이어에게 \(X \ne 0\) 상태를 넘겨주게 되고, 최적 플레이에서는 현재 플레이어가 결국 패한다(표준 님 정리).
- \(X \ne 0\)인 상태에서는 \(X\)의 최상위 1비트가 존재하고, 그 비트가 1인 더미를 하나 골라 \(p_i' = p_i \oplus X\)로 줄일 수 있다. 이때 새로운 XOR는
  \[
  X \oplus p_i \oplus p_i' = X \oplus p_i \oplus (p_i \oplus X) = 0
  \]
  이므로 상대를 패배 상태로 보낼 수 있다.
- 가능한 모든 첫 수는 “어떤 \(i\)에 대해 \(t=p_i \oplus X < p_i\)”인 경우와 1:1로 대응하므로, 그 개수가 정답이다.

## 복잡도 분석

| 항목 | 복잡도 | 비고 |
|---|---:|---|
| **시간 복잡도** | \(O(N)\) | XOR 1회 + 더미 1회 순회 |
| **공간 복잡도** | \(O(1)\) | 입력 저장을 제외하면 상수 |

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **XOR=0** | 선공이 이길 수 있는 첫 수가 없음 | 즉시 0 출력 |
| **N=1** | 한 더미만 있는 경우 | 항상 XOR≠0이므로 답은 1 |
| **t=pi** | 제거량이 0이 되는 경우(불가능한 수) | \(t<pi\)만 카운트 |

## 구현 코드 (C++)

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    int x = 0;
    vector<int> p(N);
    for (int i = 0; i < N; i++) {
        cin >> p[i];
        x ^= p[i];
    }

    if (x == 0) {
        cout << 0 << '\n';
        return 0;
    }

    int ans = 0;
    for (int i = 0; i < N; i++) {
        int t = p[i] ^ x;
        if (t < p[i]) ans++;
    }

    cout << ans << '\n';
    return 0;
}
```

## 참고

- [백준 16895번: 님 게임 3](https://www.acmicpc.net/problem/16895)


