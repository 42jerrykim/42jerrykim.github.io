---
title: "[Algorithm] cpp 백준 9250번: 문자열 집합 판별"
description: "아호-코라식 자동자로 집합 S 패턴을 통합하고, 질의 문자열을 선형 주행하며 실패 링크·out 전이로 부분 문자열 매칭을 즉시 감지합니다. 전이 초기화·루트 귀속·빠른 입출력을 점검해 1초·256MB를 안정 통과하는 O(총 길이) 풀이입니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- String
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-9250
- cpp
- C++
- Python
- String
- 문자열
- Pattern Matching
- 패턴 매칭
- Aho-Corasick
- 아호코라식
- Trie
- 트라이
- Automaton
- 자동자
- Failure Link
- 실패링크
- Failure Function
- 실패함수
- BFS
- BFS구현
- Multi-pattern
- 멀티패턴
- Substring
- 부분문자열
- String Matching
- 문자열 매칭
- Online Query
- 온라인 질의
- Deterministic Automaton
- 결정적 자동자
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
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Hashing
- 해싱
- KMP
- KMP대안
- Automata Theory
- 자동자이론
- Finite State Machine
- 유한상태기계
- Graph
- 그래프
- Queue
- 큐
- Memory
- 메모리
- Fast IO
- 빠른 입출력
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/9250
- 요약: 집합 `S`(크기 \(N\))의 문자열들 중, 질의 문자열의 "부분 문자열"로 등장하는 것이 하나라도 있으면 YES, 아니면 NO를 출력합니다. 모든 문자열은 소문자.
- 제한: \(1 \le N,Q \le 1000\), 패턴 길이 ≤ 100, 질의 길이 ≤ 10000, 메모리 256MB, 시간 1초.

## 입력/출력
```
<입력>
N
S1
S2
...
SN
Q
T1
T2
...
TQ

<출력>
각 질의 Ti에 대해 YES 또는 NO
```

## 접근 개요
- 핵심: N개의 패턴을 트라이에 넣고 아호-코라식(Aho-Corasick) 실패 링크를 구축해 하나의 자동자로 통합합니다.
- 각 질의 문자열을 선형으로 주행하면서 현재 상태에서의 전이/실패 링크를 따라가고, 매칭 상태(`out`)에 도달하면 즉시 YES입니다.
- 알파벳 26개 고정 전이를 사용해 상수 시간 전이를 보장, 전체는 입력 총 길이 선형 시간에 동작합니다.

```mermaid
flowchart LR
  A[트라이 구성 (N개 패턴 삽입)] --> B[실패 링크 BFS 구축]
  B --> C[output 전파 (fail을 통해 매칭 상태 상속)]
  C --> D[각 질의 문자열 선형 주행]
  D -->|매칭(out=true) 도달| E[YES]
  D -->|끝까지 매칭 없음| F[NO]
```

## 알고리즘 설계
- 트라이 노드 필드: `next[26]`, `fail`, `out`.
- 빌드
  - 모든 패턴을 삽입해 말단 노드 `out=true` 표시.
  - 루트의 자식 큐잉 후 BFS로 `fail`을 채우고, `next`의 공백 전이는 `fail` 전이로 채웁니다.
  - 각 노드에서 `out |= out[fail]`로 매칭 상태를 전파합니다.
- 질의 처리
  - 상태를 0에서 시작해 각 문자마다 `state = next[state][c]`로 이동합니다.
  - 이동 직후 `out[state]`가 참이면 해당 질의 답은 YES이며 조기 종료합니다. 끝까지 없으면 NO.

## 복잡도
- 시간: \(O(\sum |S_i| + \sum |T_j| + 26\cdot\text{states})\) ≈ 입력 총 길이 선형
- 공간: \(O(\text{states} \times 26)\). 최악 states ≤ \(\sum |S_i|\) (여기서는 최대 10^5 수준), 26전이 테이블도 256MB 제한 내에서 안전합니다.

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Node {
    int next[26];
    int fail;
    bool out;
    Node() {
        fill(begin(next), end(next), -1);
        fail = 0;
        out = false;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<Node> trie(1); // root = 0

    auto add_pattern = [&](const string &s) {
        int u = 0;
        for (char ch : s) {
            int c = ch - 'a';
            if (trie[u].next[c] == -1) {
                trie[u].next[c] = (int)trie.size();
                trie.emplace_back();
            }
            u = trie[u].next[c];
        }
        trie[u].out = true;
    };

    for (int i = 0; i < N; ++i) {
        string s; cin >> s;
        add_pattern(s);
    }

    // Build failure links (Aho-Corasick)
    queue<int> q;
    for (int c = 0; c < 26; ++c) {
        int v = trie[0].next[c];
        if (v == -1) trie[0].next[c] = 0;
        else {
            trie[v].fail = 0;
            q.push(v);
        }
    }

    while (!q.empty()) {
        int v = q.front(); q.pop();
        for (int c = 0; c < 26; ++c) {
            int u = trie[v].next[c];
            if (u == -1) {
                trie[v].next[c] = trie[trie[v].fail].next[c];
            } else {
                trie[u].fail = trie[trie[v].fail].next[c];
                trie[u].out = trie[u].out || trie[trie[u].fail].out;
                q.push(u);
            }
        }
    }

    int Q; cin >> Q;
    while (Q--) {
        string t; cin >> t;
        int state = 0;
        bool found = false;
        for (char ch : t) {
            int c = ch - 'a';
            state = trie[state].next[c];
            if (trie[state].out) { found = true; break; }
        }
        cout << (found ? "YES" : "NO") << '\n';
    }
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from collections import deque
input = sys.stdin.readline

class Node:
    __slots__ = ("nxt", "fail", "out")
    def __init__(self):
        self.nxt = [-1] * 26
        self.fail = 0
        self.out = False

def solve():
    N_line = input().strip()
    if not N_line:
        return
    N = int(N_line)
    trie = [Node()]  # root = 0

    def add_pattern(s: str):
        u = 0
        for ch in s:
            c = ord(ch) - 97
            if trie[u].nxt[c] == -1:
                trie[u].nxt[c] = len(trie)
                trie.append(Node())
            u = trie[u].nxt[c]
        trie[u].out = True

    for _ in range(N):
        add_pattern(input().strip())

    # build failure links
    q = deque()
    for c in range(26):
        v = trie[0].nxt[c]
        if v == -1:
            trie[0].nxt[c] = 0
        else:
            trie[v].fail = 0
            q.append(v)

    while q:
        v = q.popleft()
        vf = trie[v].fail
        for c in range(26):
            u = trie[v].nxt[c]
            if u == -1:
                trie[v].nxt[c] = trie[vf].nxt[c]
            else:
                trie[u].fail = trie[vf].nxt[c]
                if trie[trie[u].fail].out:
                    trie[u].out = True
                q.append(u)

    Q = int(input())
    out_lines = []
    for _ in range(Q):
        t = input().strip()
        state = 0
        ans = "NO"
        for ch in t:
            state = trie[state].nxt[ord(ch) - 97]
            if trie[state].out:
                ans = "YES"
                break
        out_lines.append(ans)
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- 패턴 중복, 서로의 접두사/접미사 관계(실패 링크 전파로 처리됨)
- 질의 내 다중 매칭 발생(첫 매칭에서 조기 종료 가능)
- 알파벳 범위 확인(소문자 a-z 이외 입력 없음 가정)
- 빈 패턴은 미출현(문제 조건), 질의는 길이 ≥ 1 가정

## 제출 전 점검
- 빠른 입출력 활성화(`sync_with_stdio(false)`, `tie(nullptr)`), Python은 `sys.stdin.readline`
- 실패 링크 BFS 후 `out |= out[fail]` 전파 여부 확인
- 전이표 초기화(-1)와 루트의 없는 간선 `0` 귀속 처리 확인
- 메모리 상수배(26 전이)와 상태 수 점검

## 참고자료/유사문제
- Aho–Corasick algorithm (Wikipedia)
- 다중 패턴 문자열 매칭, 실패 함수/링크 기초


