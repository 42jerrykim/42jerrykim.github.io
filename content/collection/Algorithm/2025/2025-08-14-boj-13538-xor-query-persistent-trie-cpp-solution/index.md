---
title: "[Algorithm] cpp 백준 13538번: XOR 쿼리 - 퍼시스턴트 트라이"
description: "비어있는 배열에 대한 삽입/삭제(되돌리기) 버전을 유지하는 퍼시스턴트 이진 트라이로, 구간 내 최대 XOR, x 이하 개수, k번째 수를 모두 O(log V)로 처리합니다. 50만 쿼리를 2초 내에 안정적으로 해결하는 구현/정당성/복잡도까지 정리했습니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Data Structures
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-13538
- cpp
- C++
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
- Greedy
- 그리디
- Dynamic Programming
- 동적계획법
- Graph
- 그래프
- Tree
- 트리
- Binary Trie
- 이진 트라이
- Persistent Trie
- 퍼시스턴트 트라이
- Persistence
- 버전 관리
- Range Query
- 구간 쿼리
- XOR
- XOR Query
- 최대 XOR
- Count Less Equal
- 이하 개수
- Order Statistics
- 순위 통계
- Kth Smallest
- k번째 수
- Offline Online
- 온라인 쿼리
- Rollback
- 되돌리기
- Segment Tree
- 세그먼트 트리
- Fenwick Tree
- 펜윅트리
- Data Structures
- 자료구조
- Bitwise
- 비트 연산
- 19-bit
- 좌표 범위
- 수학
- Math
image: "wordcloud.png"
---

## 문제
- 링크: [백준 13538 XOR 쿼리](https://www.acmicpc.net/problem/13538)
- 요약: 비어있는 배열 `A`에 대해 다음 쿼리를 처리합니다.
  - `1 x`: 배열 끝에 `x` 추가
  - `2 L R x`: `A[L..R]` 중 `x ⊕ y`가 최대가 되는 `y` 출력
  - `3 k`: 배열의 마지막 `k`개 제거
  - `4 L R x`: `A[L..R]` 중 `x` 이하 원소의 개수 출력
  - `5 L R k`: `A[L..R]` 중 k번째로 작은 수 출력
- 제한: `M ≤ 5e5`, 값과 질의 인자는 `≤ 5e5`, 시간 2초, 메모리 512MB

## 입력/출력
```
입력: M, 이어서 M개의 쿼리
출력: 2, 4, 5번 쿼리의 정답을 등장 순서대로 한 줄에 하나씩
```

## 접근 개요
- 핵심은 모든 시점(배열 길이)에 대한 버전을 유지하는 퍼시스턴트 이진 트라이입니다.
- `roots[t]` = 길이 `t`까지 삽입했을 때의 트라이 루트. 삽입 시 경로상의 노드만 복사해 새 루트를 만듭니다.
- 구간 `[L..R]` 질의는 두 버전 `roots[R]`와 `roots[L-1]`의 카운트 차이를 사용해 해당 구간에 존재하는 값들만 보며 탐색합니다.
  - 최대 XOR: 각 비트에서 원하는 방향에 값이 존재하는지(카운트 차이>0)로 그리디 이동
  - `≤ x` 개수: 상위 비트부터 `k`와의 비교로 누적
  - k번째 수: 왼쪽(0-자식) 크기와 `k` 비교로 좌우 결정
- 삭제(되돌리기)는 노드 삭제가 아니라 포인터만 `curLen -= k`로 과거 버전 루트를 다시 가리킵니다.

## 알고리즘 설계
- 비트 폭: `MAX_BITS = 19` (값 ≤ 500,000 < 2^19)
- 노드 구조: `child0[], child1[], cnt[]`의 평행 배열로 구현(메모리/속도 유리)
- 연산 복잡도:
  - `append`: O(log V) 노드 복사(경로 길이)로 새 루트 생성
  - `max xor / count ≤ x / k-th`: 모두 O(log V) 비트 탐색
  - `pop k`: O(1) 포인터 이동
- 메모리: 대략 `삽입 수 × (MAX_BITS+1)`개의 노드만 생성. 최대 약 10M 노드(여유 포함) ≈ 120~130MB 수준

## 정당성(핵심 근거)
- 퍼시스턴트 구조에서 `[L..R]`의 존재성은 `roots[R]` 누적 카운트 − `roots[L-1]` 누적으로 표현됩니다.
- 최대 XOR는 각 비트에서 상보 비트를 우선 선택하되, 해당 방향의 구간 내 개수가 양수일 때만 택하는 그리디가 전역 최적입니다.
- `≤ x`와 k번째 수는 트라이에서 누적 카운트로 정의된 전형적 순위 통계 탐색으로, 매 단계 선택이 전체 순서와 일치합니다.

## 복잡도
- 시간: 쿼리당 O(log V) (V = 값 범위, 여기서는 2^19)
- 공간: O((삽입 수) × log V)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

static const int MAX_BITS = 19;                  // supports values up to 2^19-1 >= 500000
static const int MAX_NODES = 10500000;          // ~ (max inserts) * (MAX_BITS+1) with margin

int child0[MAX_NODES];
int child1[MAX_NODES];
int cntNode[MAX_NODES];
int nodeCount = 0;

inline int cloneNode(int from) {
    int id = ++nodeCount;
    child0[id] = child0[from];
    child1[id] = child1[from];
    cntNode[id] = cntNode[from];
    return id;
}

int insertValue(int oldRoot, int value) {
    int newRoot = cloneNode(oldRoot);
    cntNode[newRoot]++;

    int curNew = newRoot;
    int curOld = oldRoot;
    for (int bit = MAX_BITS - 1; bit >= 0; --bit) {
        int b = (value >> bit) & 1;
        int nextOld = (b == 0 ? child0[curOld] : child1[curOld]);
        int nextNew = cloneNode(nextOld);
        cntNode[nextNew]++;

        if (b == 0) child0[curNew] = nextNew;
        else        child1[curNew] = nextNew;

        curNew = nextNew;
        curOld = nextOld;
    }
    return newRoot;
}

inline int getCnt(int node) { return node ? cntNode[node] : 0; }

int queryMaxXorY(int rootR, int rootLminus1, int x) {
    int hi = rootR, lo = rootLminus1;
    int y = 0;
    for (int bit = MAX_BITS - 1; bit >= 0; --bit) {
        int xb = (x >> bit) & 1;
        int want = 1 - xb;

        int hiWant = (want == 0 ? child0[hi] : child1[hi]);
        int loWant = (want == 0 ? child0[lo] : child1[lo]);
        int haveWant = getCnt(hiWant) - getCnt(loWant);

        int go;
        if (haveWant > 0) go = want;
        else go = 1 - want;

        if (go) y |= (1 << bit);

        hi = (go == 0 ? child0[hi] : child1[hi]);
        lo = (go == 0 ? child0[lo] : child1[lo]);
    }
    return y;
}

int queryCountLess(int rootR, int rootLminus1, int k) {
    // count of values in (L..R) that are < k
    int hi = rootR, lo = rootLminus1;
    int res = 0;
    for (int bit = MAX_BITS - 1; bit >= 0; --bit) {
        int kb = (k >> bit) & 1;
        if (kb == 1) {
            // add all with 0 at this bit
            int hi0 = child0[hi], lo0 = child0[lo];
            res += getCnt(hi0) - getCnt(lo0);
            hi = child1[hi];
            lo = child1[lo];
        } else {
            hi = child0[hi];
            lo = child0[lo];
        }
        if (!hi && !lo) break;
    }
    return res;
}

int queryKth(int rootR, int rootLminus1, int k) {
    int hi = rootR, lo = rootLminus1;
    int y = 0;
    for (int bit = MAX_BITS - 1; bit >= 0; --bit) {
        int hi0 = child0[hi], lo0 = child0[lo];
        int leftCnt = getCnt(hi0) - getCnt(lo0);
        if (k <= leftCnt) {
            hi = hi0; lo = lo0;
        } else {
            k -= leftCnt;
            y |= (1 << bit);
            hi = child1[hi];
            lo = child1[lo];
        }
    }
    return y;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M;
    if (!(cin >> M)) return 0;

    vector<int> roots(M + 2, 0); // roots[len] = trie root after 'len' appends
    int curLen = 0;              // current array size

    for (int i = 0; i < M; ++i) {
        int type; cin >> type;
        if (type == 1) {
            int x; cin >> x;
            roots[curLen + 1] = insertValue(roots[curLen], x);
            curLen++;
        } else if (type == 2) {
            int L, R, x; cin >> L >> R >> x;
            int y = queryMaxXorY(roots[R], roots[L - 1], x);
            cout << y << '\n';
        } else if (type == 3) {
            int k; cin >> k;
            curLen -= k; // move back to previous version
        } else if (type == 4) {
            int L, R, x; cin >> L >> R >> x;
            int ans = queryCountLess(roots[R], roots[L - 1], x + 1); // <= x
            cout << ans << '\n';
        } else if (type == 5) {
            int L, R, k; cin >> L >> R >> k;
            int y = queryKth(roots[R], roots[L - 1], k);
            cout << y << '\n';
        }
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- `x = 0`, `x`가 최대값(=500000)인 경우
- `L = R` 단일 원소 구간, 전체 구간
- `3 k` 직후 즉시 `1 x` 또는 질의 조합(버전 되돌림 정확성)
- `5 L R k`에서 `k = 1`/`k = R-L+1` 극단값
- 값이 모두 동일/단조/교차 패턴

## 제출 전 점검
- 비트 폭이 충분한가? `MAX_BITS = 19` 확인
- 배열 인덱스 보정(`roots[L-1]`) 정확성
- `≤ x`는 `countLess(x+1)`로 처리했는지
- 입출력 버퍼링(`sync_with_stdio(false), tie(nullptr)`) 적용

## 참고자료
- [cp-algorithms: Trie and persistent data structures](https://cp-algorithms.com/)


