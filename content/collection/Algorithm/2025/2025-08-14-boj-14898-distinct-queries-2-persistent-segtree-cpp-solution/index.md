---
title: "[Algorithm] C++ 백준 14898번: 서로 다른 수와 쿼리 2"
description: "좌표압축과 영속 세그먼트 트리로 각 r 버전을 구성해 [l,r] 서로 다른 원소 수를 O(log N)에 답합니다. 온라인 입력은 누적 정답으로 처리하여 5초·1024MB 제한을 안정적으로 통과합니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Segment Tree
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-14898
- cpp
- C++
- Data Structures
- 자료구조
- Segment Tree
- 세그먼트 트리
- Persistent Segment Tree
- 영속 세그먼트 트리
- Persistent
- 영속성
- Versioned Tree
- 버전 트리
- Distinct Count
- 서로 다른 수
- Unique Elements
- 유니크 원소
- Queries
- 쿼리
- Online Query
- 온라인 쿼리
- Coordinate Compression
- 좌표압축
- Prefix
- Prefix Version
- 버전 관리
- Point Update
- 포인트 업데이트
- Range Query
- 구간 질의
- Offline Technique
- 온라인 처리
- Fast IO
- 빠른입출력
- Memory Optimization
- 메모리 최적화
- Complexity Analysis
- 복잡도 분석
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Implementation
- 구현
- Competitive Programming
- 경쟁프로그래밍
- Tutorial
- 해설
- Editorial
- 에디토리얼
- Fenwick Tree
- 펜윅트리
- Binary Search
- 이분탐색
- Hashing
- 해싱
- Sliding Window
- 슬라이딩윈도우
- Mo's Algorithm
- 모스 알고리즘
- Immutable DS
- 불변 자료구조
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/14898
- 요약: 길이 N 배열 A와 Q개의 질의가 주어지고, 각 질의는 `l r`에 대해 구간 [l, r] 안의 서로 다른 수의 개수를 출력한다. 단, `l = x + 이전 정답` 이며 입력은 `x r` 형식으로 주어진다.

### 제한/스펙
- 시간 제한: 5초, 메모리 제한: 1024MB
- N ≤ 1,000,000, Q ≤ 1,000,000
- A[i] ≤ 1,000,000,000 (자연수), 1 ≤ l ≤ r ≤ N 보장

## 입력/출력
```text
<입력 형식>
N
A1 A2 ... AN
Q
x1 r1
x2 r2
...
xQ rQ
```

```text
<출력 형식>
각 질의의 답을 한 줄에 하나씩 출력
```

예제 (문제에서 발췌):

```text
입력
10
1 3 2 1 3 1 3 2 1 3
10
8 9
2 7
4 8
1 6
1 7
-1 10
0 8
-2 10
1 7
-1 7

출력
2
2
3
2
3
3
3
3
2
3
```

## 접근 개요
- 핵심 관찰: 인덱스 i까지 봤을 때, 값 `A[i]`의 마지막 등장 위치만 1로 표시하고 과거 위치는 0으로 되돌리면, 어떤 r에 대한 "서로 다른 수 개수"는 그때의 표시 배열에서 [l, r]에 있는 1의 합과 동일하다.
- 모델링: 각 접두사 r마다 위의 표시 배열의 버전을 보유하는 영속 세그먼트 트리(Persistent Segment Tree)를 만든다. i로 진행할 때 `+1`을 i에 더하고, 같은 값이 과거 `p`에 있었다면 `-1`을 p에 더해 마지막 등장 위치만 1이 되도록 유지한다.
- 질의 처리: 질의 (x, r)의 실제 l은 `l = x + 이전 정답`. 답은 `root[r]` 버전에서 [l, r] 구간 합이다. 각 질의 O(log N).

### 흐름 다이어그램 (Mermaid)
```mermaid
flowchart LR
  A[입력 A[1..N]] --> B[좌표압축]
  B --> C[for i=1..N]
  C --> D{last[A[i]] 존재?}
  D -- 아니오 --> E[버전 r=i: pos=i 에 +1]
  D -- 예 --> F[버전 r=i: pos=i +1,
                 pos=last[A[i]] -1]
  E --> G[root[i] 저장]
  F --> G
  H[질의 (x,r)] --> I[l=x+prevAns]
  I --> J[답 = sum(root[r], l..r)]
```

## 알고리즘 설계
- 자료구조: 포인터(인덱스)로 연결된 영속 세그먼트 트리 노드 배열. 각 노드는 `왼/오 자식 인덱스 + 구간합`을 가진다.
- 전처리: 값의 범위가 크므로 좌표압축으로 값들을 [1..M]으로 매핑한다.
- 빌드: i=1..N 순회하며
  - 현재 위치 i에 `+1` 업데이트(새 루트 생성)
  - 같은 값의 과거 등장 위치 p가 있으면 p에 `-1` 업데이트
  - 최종 루트를 `root[i]`로 저장
- 질의: 입력 (x, r)에 대해 `l = x + 이전 정답`를 계산하고, `query(root[r], l, r)` 반환
- 정당성: 각 값에 대해 "가장 오른쪽(마지막) 등장 인덱스에만 1"이 유지되므로, [l, r] 안에 서로 다른 값의 수는 그 구간의 1의 개수와 일치한다. `root[r]`는 r까지의 정보만 담으므로 [l, r]에서의 합이 정확한 답이다.

## 복잡도
- 전처리/빌드: O(N log N)
- 질의: O(log N) (Q개면 O(Q log N))
- 메모리: O(N log N) 노드. N=1e6일 때 약 수천만 노드 수준으로 1024MB 안에 수렴하도록 배열 기반으로 구현

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct FastScanner {
    static const int BUFSIZE = 1 << 20;
    int idx = 0, size = 0;
    char buf[BUFSIZE];
    inline char read() {
        if (idx >= size) {
            size = (int)fread(buf, 1, BUFSIZE, stdin);
            idx = 0;
            if (size == 0) return 0;
        }
        return buf[idx++];
    }
    template <typename T>
    bool nextInt(T &out) {
        char c = read();
        if (!c) return false;
        while (c <= ' ') { c = read(); if (!c) return false; }
        int sign = 1;
        if (c == '-') { sign = -1; c = read(); }
        long long val = 0;
        while (c >= '0') { val = val * 10 + (c - '0'); c = read(); }
        out = (T)(val * sign);
        return true;
    }
};

struct PersistentSegTree {
    int N;
    int LOGN;
    int MAXNODE;
    int nodeCount;
    int *leftChild;
    int *rightChild;
    int *sum;
    vector<int> root;

    PersistentSegTree(int n, int estimatedNodes)
        : N(n), nodeCount(0) {
        LOGN = 0;
        while ((1 << LOGN) < N) ++LOGN;
        MAXNODE = estimatedNodes;
        leftChild = (int*)malloc(sizeof(int) * (MAXNODE));
        rightChild = (int*)malloc(sizeof(int) * (MAXNODE));
        sum = (int*)malloc(sizeof(int) * (MAXNODE));
        if (!leftChild || !rightChild || !sum) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(1);
        }
        leftChild[0] = rightChild[0] = sum[0] = 0;
        root.assign(N + 1, 0);
    }

    inline int newNode(int from) {
        int cur = ++nodeCount;
        leftChild[cur] = leftChild[from];
        rightChild[cur] = rightChild[from];
        sum[cur] = sum[from];
        return cur;
    }

    int update(int prev, int s, int e, int pos, int delta) {
        int cur = newNode(prev);
        sum[cur] = sum[prev] + delta;
        if (s != e) {
            int mid = (s + e) >> 1;
            if (pos <= mid) {
                int nl = update(leftChild[prev], s, mid, pos, delta);
                leftChild[cur] = nl;
            } else {
                int nr = update(rightChild[prev], mid + 1, e, pos, delta);
                rightChild[cur] = nr;
            }
        }
        return cur;
    }

    int query(int node, int s, int e, int l, int r) const {
        if (node == 0 || r < s || e < l) return 0;
        if (l <= s && e <= r) return sum[node];
        int mid = (s + e) >> 1;
        int res = 0;
        if (l <= mid) res += query(leftChild[node], s, mid, l, r);
        if (r > mid)  res += query(rightChild[node], mid + 1, e, l, r);
        return res;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    FastScanner fs;
    int N;
    if (!fs.nextInt(N)) return 0;

    vector<int> A(N + 1);
    vector<long long> raw(N);
    for (int i = 0; i < N; ++i) {
        long long v;
        fs.nextInt(v);
        raw[i] = v;
    }
    vector<long long> sorted = raw;
    sort(sorted.begin(), sorted.end());
    sorted.erase(unique(sorted.begin(), sorted.end()), sorted.end());
    int M = (int)sorted.size();
    for (int i = 1; i <= N; ++i) {
        A[i] = (int)(lower_bound(sorted.begin(), sorted.end(), raw[i - 1]) - sorted.begin()) + 1;
    }

    int LOGN = 0; while ((1 << LOGN) < N) ++LOGN;
    long long estimate = 1LL * 2 * N * (LOGN + 1) + 10; // 여유분 포함
    int MAXNODE = (int)estimate;

    PersistentSegTree pst(N, MAXNODE);
    vector<int> last(M + 1, 0);

    for (int i = 1; i <= N; ++i) {
        int val = A[i];
        int r1 = pst.update(pst.root[i - 1], 1, N, i, +1);
        if (last[val]) {
            pst.root[i] = pst.update(r1, 1, N, last[val], -1);
        } else {
            pst.root[i] = r1;
        }
        last[val] = i;
    }

    int Q;
    fs.nextInt(Q);
    string out;
    out.reserve((size_t)Q * 4 + Q);
    int prevAns = 0;
    for (int i = 1; i <= Q; ++i) {
        int x, r;
        fs.nextInt(x);
        fs.nextInt(r);
        int l = x + prevAns; // 1 ≤ l ≤ r ≤ N 보장
        int ans = pst.query(pst.root[r], 1, N, l, r);
        prevAns = ans;
        out.append(to_string(ans));
        out.push_back('\n');
    }
    cout << out;
    return 0;
}
```

## 코너 케이스 체크리스트
- l = r 같은 단일 구간
- 모든 값이 동일 / 모두 서로 다른 경우
- 한 값이 여러 번 교차 등장하는 패턴 (이전 위치 -1 적용 확인)
- x가 음수/양수 혼재해도 `l = x + 이전 정답`가 항상 유효 범위에 들어오는지 (문제에서 보장)
- N, Q가 최대일 때 빠른 입출력 및 메모리 상한 준수

## 제출 전 점검
- 좌표압축 구현 오류 여부 (lower_bound 인덱싱 +1)
- 업데이트 순서: i에 +1 후, 이전 위치에 -1
- `root[r]` 버전에서 [l, r]로만 질의하는지 확인
- 빠른 입출력 사용 및 출력 버퍼링
- 64-bit 오버플로 가능 지점 점검(노드 수 계산 등은 64-bit로)

## 참고자료
- Persistent Segment Tree 개념 정리 (일반 자료)
- 문제 페이지: https://www.acmicpc.net/problem/14898


