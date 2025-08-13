---
title: "[Algorithm] C++ 백준 3444번 : Robotic Sort"
description: "백준 3444 Robotic Sort는 로봇 팔이 연속 구간을 뒤집는 연산만으로 샘플을 안정적으로 오름차순 정렬하도록 P1..PN을 출력하는 문제입니다. Implicit Treap로 현재 위치 계산과 구간 뒤집기를 O(N log N)으로 처리한 C++ 풀이."
date: 2025-08-12
lastmod: 2025-08-12
categories:
- "BOJ"
- "Algorithm"
tags:
- "BOJ"
- "Baekjoon"
- "백준"
- "3444"
- "Robotic Sort"
- "로보틱 소트"
- "Robot"
- "Reversal"
- "뒤집기"
- "Range Reverse"
- "구간 뒤집기"
- "Stable Sort"
- "안정 정렬"
- "Sorting"
- "정렬"
- "Implicit Treap"
- "Treap"
- "트립"
- "Splay Tree"
- "스플레이 트리"
- "Lazy Propagation"
- "지연 전파"
- "자료구조"
- "Data Structure"
- "Algorithm"
- "알고리즘"
- "ICPC"
- "CERC 2007"
- "Regionals"
- "Competitive Programming"
- "코딩테스트"
- "GNU++17"
- "C++"
- "CPP"
- "Index by pointer"
- "포인터 인덱스"
- "안정성 보장"
- "Order Statistics"
- "순서 통계"
- "Rank query"
- "순위 질의"
- "Sequence"
- "시퀀스"
- "Lazy Reverse"
- "플립"
- "Reverse Operation"
- "연산 시뮬레이션"
- "시뮬레이션"
- "Stable Reordering"
- "위치 추적"
- "Position"
- "인덱스"
- "N log N"
- "O(N log N)"
- "시간복잡도"
- "공간복잡도"
- "문제해설"
- "백준해설"
image: "wordcloud.png"
---

백준 문제 [Robotic Sort (3444)](https://www.acmicpc.net/problem/3444)는 로봇 팔이 연속 구간을 뒤집는 연산만으로 샘플을 안정적으로 오름차순 정렬하도록, 각 단계에서 뒤집기 직전의 목표 원소 위치 `P1..PN`을 출력하는 문제입니다.

### 문제 요약
- 입력: 여러 시나리오, 각 시나리오는 샘플 수 `N (1 ≤ N ≤ 100000)` 과 `N`개의 높이
- 연산: 로봇은 임의의 구간 `[A, B]`를 한 번의 연산으로 뒤집을 수 있음
- 알고리즘: i번째로 작은 샘플의 현재 위치를 `Pi`라 하고, 구간 `[i, Pi]`를 뒤집어 i번째 자리에 고정 (중복 값은 안정적으로 유지)
- 출력: 각 시나리오마다 `P1..PN`

### 접근
- 안정 정렬 요구가 있어 값이 같다면 초기 입력 순서를 보존해야 합니다. 따라서 (값, 초기 인덱스)로 정렬된 목표 순서를 만듭니다.
- i = 1..N에 대해, 아직 정렬되지 않은 구간에서 i번째로 작은 노드의 "현재 위치"를 빠르게 찾고, `[i, pos]`를 뒤집습니다.
- 시퀀스의 구간 뒤집기와 원소의 현재 순위(인덱스)를 모두 `O(log N)`에 처리하기 위해 Implicit Treap(암시적 키 트립) + lazy reverse를 사용합니다.
  - Treap 노드는 값과 초기 인덱스(안정성)를 보유하고, parent 포인터로 현재 순위를 `O(log N)`에 계산합니다.
  - 구간 뒤집기는 lazy flag로 처리합니다.

### C++ 풀이

```cpp
// 더 많은 정보는 https://42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Node {
    Node *l, *r, *p;
    uint32_t pri;
    int sz;
    bool rev;
    int value;
    int id; // original position (1-indexed)
    Node(int v, int i, uint32_t pr) : l(nullptr), r(nullptr), p(nullptr), pri(pr), sz(1), rev(false), value(v), id(i) {}
};

static inline int getSize(Node* t) { return t ? t->sz : 0; }

static inline void push(Node* t) {
    if (!t || !t->rev) return;
    t->rev = false;
    swap(t->l, t->r);
    if (t->l) t->l->rev = !t->l->rev;
    if (t->r) t->r->rev = !t->r->rev;
}

static inline void pull(Node* t) {
    if (!t) return;
    t->sz = 1 + getSize(t->l) + getSize(t->r);
    if (t->l) t->l->p = t;
    if (t->r) t->r->p = t;
}

static Node* merge(Node* a, Node* b) {
    push(a); push(b);
    if (!a || !b) {
        Node* res = a ? a : b;
        if (res) res->p = nullptr;
        return res;
    }
    if (a->pri < b->pri) {
        a->r = merge(a->r, b);
        if (a->r) a->r->p = a;
        pull(a);
        a->p = nullptr;
        return a;
    } else {
        b->l = merge(a, b->l);
        if (b->l) b->l->p = b;
        pull(b);
        b->p = nullptr;
        return b;
    }
}

static void split(Node* t, int k, Node*& a, Node*& b) {
    if (!t) { a = b = nullptr; return; }
    push(t);
    if (getSize(t->l) >= k) {
        split(t->l, k, a, t->l);
        if (t->l) t->l->p = t;
        pull(t);
        b = t;
        b->p = nullptr;
        if (a) a->p = nullptr;
    } else {
        split(t->r, k - getSize(t->l) - 1, t->r, b);
        if (t->r) t->r->p = t;
        pull(t);
        a = t;
        a->p = nullptr;
        if (b) b->p = nullptr;
    }
}

static void reverseRange(Node*& root, int l, int r) {
    if (l > r) return;
    Node *t1, *t2, *t3;
    split(root, l - 1, t1, t2);
    split(t2, r - l + 1, t2, t3);
    if (t2) t2->rev = !t2->rev;
    root = merge(merge(t1, t2), t3);
}

static int getIndex(Node* x) {
    // Push all lazy flags along the path root->x, then compute rank
    vector<Node*> path;
    for (Node* y = x; y; y = y->p) path.push_back(y);
    reverse(path.begin(), path.end());
    for (Node* t : path) push(t);

    int ans = getSize(x->l) + 1;
    for (Node* cur = x; cur->p; cur = cur->p) {
        Node* par = cur->p;
        if (cur == par->r) ans += getSize(par->l) + 1;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    mt19937 rng(712367); // fixed seed for determinism
    while (true) {
        int N;
        if (!(cin >> N)) return 0;
        if (N == 0) break;

        vector<int> A(N);
        for (int i = 0; i < N; ++i) cin >> A[i];

        vector<Node*> nodes(N);
        Node* root = nullptr;
        for (int i = 0; i < N; ++i) {
            nodes[i] = new Node(A[i], i + 1, rng());
            root = merge(root, nodes[i]);
        }

        vector<Node*> order = nodes;
        sort(order.begin(), order.end(), [](const Node* a, const Node* b) {
            if (a->value != b->value) return a->value < b->value;
            return a->id < b->id; // stable by original index
        });

        for (int i = 1; i <= N; ++i) {
            Node* target = order[i - 1];
            int pos = getIndex(target); // 1-indexed current position
            if (i > 1) cout << ' ';
            cout << pos;
            reverseRange(root, i, pos);
        }
        cout << '\n';

        // Optional: nodes are freed by OS on exit
    }
    return 0;
}
```

### 복잡도
- 시간: 각 단계에서 순위 계산과 구간 뒤집기 `O(log N)` → 전체 `O(N log N)`
- 공간: Treap 노드 `O(N)`

### 빌드/실행
- 빌드: `g++ -O2 -pipe -static -s -std=gnu++17 main.cpp -o main`
- 실행: `./main < input.txt > output.txt`


