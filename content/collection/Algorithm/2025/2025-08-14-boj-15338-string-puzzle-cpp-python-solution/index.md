---
title: "[Algorithm] C++/Python 백준 15338번: String Puzzle - 루트 압축 점프"
description: "길이 n(≤1e9) 비공개 문자열에 위치 고정 힌트와 구간 복사 힌트가 주어진다. 각 구간을 왼쪽으로 d만큼 당기는 함수로 모델링하고 p에서 반복 적용해 유일한 루트를 찾는다. 루트→문자 맵으로 쿼리를 O(log b)로 결정한다."
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
- Problem-15338
- cpp
- python
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
- Code Review
- 코드리뷰
- Template
- 템플릿
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Binary Search
- 이분탐색
- String
- 문자열
- Math
- 수학
- Modulo
- 모듈러
- Congruence
- 합동
- Segment
- 구간
- Mapping
- 매핑
- Jump Compression
- 점프 압축
- Root Compression
- 루트 압축
- Equivalence
- 동치
- ICPC
- Asia Tsukuba
- 2017
- Residue Class
- 잔여 클래스
- Interval
- 인터벌
- Simulation
- 시뮬레이션
- Sliding Window
- 슬라이딩윈도우
- Hashing
- 해싱
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/15338
- 요약: 길이 n(최대 1e9)의 비공개 문자열에 대해 두 종류의 힌트가 주어진다. (1) 일부 위치의 문자가 직접 주어지고, (2) 특정 구간 [y, y+L-1]의 부분문자열이 [h, h+L-1]과 동일하다는 정보가 주어진다. q개의 위치 z_i에 대해 해당 문자가 유일하게 결정되면 그 문자, 아니면 ? 를 출력한다. 입력은 모순이 없음을 보장한다.
- 제한/스펙: n ≤ 1e9, a, b, q ≤ 1000, y_i 엄격 증가, h_i < y_i, 마지막 구간 길이는 n까지 확장.

## 입력/출력
예제 1
```
입력
9 4 5 4
3 C
4 I
7 C
9 P
2 1
4 0
6 2
7 0
8 4
8 1
9 6
출력
ICPC
```

예제 2
```
입력
1000000000 1 1 2
20171217 A
3 1
42
987654321
출력
?A
```

## 접근 개요
- 구간 [y, y+L-1]와 [h, h+L-1]가 동일하다는 것은 모든 j ∈ [y..y+L-1]에 대해 c[j] = c[j-d] (d = y-h > 0)를 의미한다. 즉, j가 해당 구간의 "오른쪽"에 있으면 항상 왼쪽으로 d만큼 끌어당길 수 있다.
- 모든 j에 대해 왼쪽으로만 이동하는 함수 f(j) = (j ∈ [y..y+L-1]? j-d : j)를 반복 적용하면, 더 이상 어떤 구간의 오른쪽에도 속하지 않는 유일한 루트 위치 root(j)에 도달한다.
- 같은 root를 공유하는 모든 위치는 같은 문자이므로, 미리 주어진 고정 문자 힌트 x의 루트를 계산해 root→문자 맵을 만든 뒤, 쿼리 z는 root(z)로 조회한다. 없으면 ?.

### Mermaid 다이어그램 (아이디어 스케치)
```mermaid
flowchart LR
  subgraph Segment i
    Y[y = startPositions[i]] --- R[y+L-1]
  end
  J[j ∈ [y..y+L-1]] -- "left shift by d = y-h" --> Jd[j-d]
  style J fill:#f6f6,stroke:#333,stroke-width:1px
  style Jd fill:#f6f6,stroke:#333,stroke-width:1px
```

## 알고리즘 설계
- 전처리: 입력의 y_i가 오름차순이므로 각 세그먼트 i의 길이 L = (y_{i+1} - y_i), 마지막은 n+1 - y_b. d_i = y_i - h_i (h_i=0이면 매핑 없음).
- 루트 찾기 findRoot(p):
  - 이진 탐색으로 p가 속한 세그먼트 i를 찾는다(없으면 p가 루트).
  - 그 세그먼트가 매핑을 가진다면(S 구간) d_i만큼 왼쪽으로 반복 이동해야 한다. 같은 세그먼트 안에서는 등차수열이므로 한 번에 steps = (p - y_i)/d_i + 1번 점프로 p ← p - steps·d_i 하면 p < y_i가 된다(세그먼트 탈출).
  - 이를 더 이상 이동 불가할 때까지 반복하면 반드시 유일한 root(p)에 도달한다(왼쪽 단조 감소이므로 종료 보장).
- 고정 문자 힌트 x마다 root(x)를 구해 root→문자를 기록. 쿼리 z는 root(z)로 조회하여 있으면 문자, 없으면 ? 출력.

## 복잡도
- 세그먼트 탐색 이진탐색 O(log b) × (왼쪽 점프 횟수 ≤ 세그먼트 수 b) → findRoot는 O(b log b) 상한. a, q ≤ 1000이므로 전체 O((a+q)·b·log b) 내에서 충분히 통과.
- 추가 메모리 O(a).

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    int a, b, q;
    if (!(cin >> n >> a >> b >> q)) return 0;

    vector<long long> fixedPos(a);
    vector<char> fixedChar(a);
    for (int i = 0; i < a; ++i) cin >> fixedPos[i] >> fixedChar[i];

    vector<long long> ys(b), hs(b);
    for (int i = 0; i < b; ++i) cin >> ys[i] >> hs[i];

    vector<long long> Z(q);
    for (int i = 0; i < q; ++i) cin >> Z[i];

    vector<long long> segLen(b), delta(b);
    for (int i = 0; i < b; ++i) {
        segLen[i] = (i + 1 < b ? ys[i + 1] - ys[i] : (n + 1 - ys[i]));
        delta[i] = (hs[i] > 0 ? ys[i] - hs[i] : 0);
    }

    auto findSeg = [&](long long p) -> int {
        if (b == 0) return -1;
        if (p < ys[0]) return -1;
        int i = int(upper_bound(ys.begin(), ys.end(), p) - ys.begin()) - 1;
        return i;
    };

    function<long long(long long)> findRoot = [&](long long p) -> long long {
        while (true) {
            int i = findSeg(p);
            if (i < 0) return p;
            if (hs[i] == 0) return p; // no mapping on this segment
            long long y = ys[i], d = delta[i];
            long long steps = (p - y) / d + 1; // minimal to exit: p - steps*d < y
            p -= steps * d;
        }
    };

    unordered_map<long long, char> rootToChar;
    rootToChar.reserve(a * 2 + 8);
    for (int i = 0; i < a; ++i) {
        long long r = findRoot(fixedPos[i]);
        if (!rootToChar.count(r)) rootToChar.emplace(r, fixedChar[i]);
    }

    string out;
    out.reserve(q);
    for (int i = 0; i < q; ++i) {
        long long r = findRoot(Z[i]);
        auto it = rootToChar.find(r);
        out.push_back(it == rootToChar.end() ? '?' : it->second);
    }
    cout << out << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from bisect import bisect_right

def solve() -> None:
    data = sys.stdin.read().strip().split()
    it = iter(data)
    n = int(next(it))
    a = int(next(it))
    b = int(next(it))
    q = int(next(it))

    fixed_pos = []
    fixed_char = []
    for _ in range(a):
        fixed_pos.append(int(next(it)))
        fixed_char.append(next(it))

    ys = [0]*b
    hs = [0]*b
    for i in range(b):
        ys[i] = int(next(it))
        hs[i] = int(next(it))

    Z = [int(next(it)) for _ in range(q)]

    seg_len = [0]*b
    delta = [0]*b
    for i in range(b):
        seg_len[i] = (ys[i+1] - ys[i]) if i+1 < b else (n + 1 - ys[i])
        delta[i] = (ys[i] - hs[i]) if hs[i] > 0 else 0

    def find_seg(p: int) -> int:
        if b == 0:
            return -1
        if p < ys[0]:
            return -1
        i = bisect_right(ys, p) - 1
        return i

    def find_root(p: int) -> int:
        while True:
            i = find_seg(p)
            if i < 0:
                return p
            if hs[i] == 0:
                return p
            y = ys[i]
            d = delta[i]
            steps = (p - y) // d + 1
            p -= steps * d

    root_to_char: dict[int, str] = {}
    for x, c in zip(fixed_pos, fixed_char):
        r = find_root(x)
        if r not in root_to_char:
            root_to_char[r] = c

    out_chars = []
    for z in Z:
        r = find_root(z)
        out_chars.append(root_to_char.get(r, '?'))
    sys.stdout.write(''.join(out_chars) + '\n')

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- h_i = 0(경계만 표시)인 세그먼트: 더 이상 이동 불가 → 현재 위치가 루트.
- d ≥ L(비겹침)·d < L(겹침) 모두에서 한 번에 탈출 점프가 정확히 작동하는지.
- p < y_1, b = 0, a = 0, q = 1 등 최소 입력.
- 매우 큰 n에서도(실제 접근 위치는 최대 y_b 인근) 시간/메모리 영향 없음.

## 참고자료
- ICPC Asia Tsukuba 2017, Problem J "String Puzzle" 문제 설명.

