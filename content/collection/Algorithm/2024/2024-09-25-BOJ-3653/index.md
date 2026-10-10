---
description: "백준 3653 영화 수집은 DVD를 꺼내 맨 위로 올릴 때 그 위에 쌓인 개수를 묻는 문제입니다. 위치 슬롯을 비워 두고 Fenwick Tree로 prefix sum을 O(log N)에 구하는 풀이와 정확성 근거, 복잡도, 코너 케이스를 C++·Python 코드로 정리합니다."
image: "wordcloud.png"
categories: Algorithm
date: "2024-09-25T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Data-Structures(자료구조)
- Time-Complexity(시간복잡도)
- Simulation(시뮬레이션)
- Stack(스택)
- Algorithm(알고리즘)
- BOJ(백준)
- Competitive-Programming(경쟁프로그래밍)
- Problem-Solving(문제해결)
- C++
- Implementation(구현)
- Coding-Test(코딩테스트)
- Optimization(최적화)
- Code-Quality(코드품질)
- Python
- Tree(트리)
- Space-Complexity(공간복잡도)
- Edge-Cases(엣지케이스)
- Best-Practices
- Complexity-Analysis(복잡도분석)
- Debugging(디버깅)
- Performance(성능)
- Pitfalls(함정)
- Segment-Tree(세그먼트트리)
- Range-Query
- Prefix-Sum
title: '[Algorithm] C++/Python 백준 3653번 : 영화 수집'
---

상근이는 영화 DVD를 수집하는 열성적인 수집가이다. 그는 자신의 DVD 콜렉션을 탑처럼 쌓아 보관한다. 영화를 보고 싶을 때마다 DVD의 위치를 찾아서, 쌓여 있는 콜렉션이 무너지지 않도록 조심스럽게 해당 DVD를 꺼낸다. 영화를 다 본 후에는 그 DVD를 가장 위에 놓는다.

하지만 상근이가 보유한 DVD의 수가 너무 많아, 원하는 DVD를 찾는 데 시간이 오래 걸린다. 각 DVD의 위치를 쉽게 찾기 위해, 찾으려는 DVD 위에 몇 개의 DVD가 있는지만 알면 된다. 각 DVD는 표지에 붙어 있는 번호로 구별할 수 있다.

이때, 각 DVD의 위치를 기록하는 프로그램을 작성하고자 한다. 상근이가 영화를 한 편 볼 때마다 그 DVD 위에 몇 개의 DVD가 있었는지를 출력해야 한다. 또한, 상근이는 매번 영화를 볼 때마다 본 DVD를 가장 위에 놓는다.

프로그램은 여러 테스트 케이스를 처리해야 하며, 각 테스트 케이스마다 상근이가 가지고 있는 영화의 수 $n$과 보려고 하는 영화의 수 $m$이 주어진다. 이어서 $m$개의 영화 번호가 순서대로 주어진다. 가장 처음에는 영화들이 1번부터 $n$번까지 번호 순서대로 쌓여 있으며, 가장 위에 있는 영화의 번호는 1번이다.

각각의 영화에 대해, 그 영화를 볼 때 해당 DVD 위에 몇 개의 DVD가 있었는지를 구해야 한다.

문제 : [https://www.acmicpc.net/problem/3653](https://www.acmicpc.net/problem/3653)

|![/assets/images/undefined/algorithm.png](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 학습 목표

이 글을 읽고 나면 다음을 설명할 수 있어야 한다.

- "위에 쌓인 DVD 수"를 위치 슬롯의 구간 합 문제로 바꾸는 이유
- 슬롯을 `m + i`에서 시작해 `top--`로 내려오며 재활용하는 방식이 왜 정확한지(불변식)
- Fenwick Tree와 세그먼트 트리 중 이 문제에 무엇이 더 적합한지, 그리고 전체 복잡도 $O((n+m)\log(n+m))$의 도출

## 접근 방식

문제의 제약은 테스트 케이스마다 $n, m \le 100{,}000$이다. DVD를 꺼낼 때마다 배열을 선형으로 훑으면 질의 하나에 $O(n)$, 전체로 $O(nm)$이라 최악 $10^{10}$ 번의 연산이 되어 시간 초과가 난다. 필요한 것은 "특정 DVD보다 위쪽에 있는 DVD가 몇 개인가"를 로그 시간에 답하는 구조다.

핵심 발상은 DVD를 옮기는 대신 **위치 번호만 새로 배정**하는 것이다. 탑의 위쪽을 낮은 번호로 보고, 각 슬롯에 DVD가 있으면 1, 없으면 0을 기록하면 "위에 쌓인 개수"는 `1`부터 `현재 위치 - 1`까지의 prefix sum이 된다. 맨 위로 올리는 동작은 기존 슬롯의 값을 0으로 되돌리고, 지금까지 쓰인 어떤 슬롯보다 더 위쪽(더 작은 번호)의 빈 슬롯에 1을 기록하는 것으로 표현된다. 이 점 갱신과 prefix sum 질의를 모두 $O(\log N)$에 처리하는 자료구조가 Fenwick Tree(이진 인덱스 트리)다.

슬롯 배정 규칙은 다음 불변식으로 정리된다. 초기에 DVD `i`는 슬롯 `m + i`를 차지하고, 슬롯 `1`부터 `m`까지는 비어 있다. `k`번째 요청(`k`는 1부터)에서 꺼낸 DVD는 슬롯 `m - k + 1`로 올라간다. 코드의 `top`은 처음에 `m`이고 요청마다 하나씩 줄어드는 "다음에 쓸 가장 위쪽 빈 슬롯"이다. 요청이 `m`번뿐이므로 `top`은 1 아래로 내려가지 않고, 이미 사용한 위쪽 슬롯은 항상 그 아래(번호가 큰) 슬롯보다 위에 있으므로 번호 순서가 곧 쌓인 순서와 일치한다.

작은 예로 $n=3, m=2$에서 요청이 `3, 1`일 때 슬롯 상태를 따라가 보자. 슬롯 번호는 위가 작은 쪽이다.

| 단계 | 슬롯 1 | 슬롯 2 | 슬롯 3 | 슬롯 4 | 슬롯 5 | 출력 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 초기 | 0 | 0 | DVD1 | DVD2 | DVD3 | - |
| 요청 3 | 0 | DVD3 | DVD1 | DVD2 | 0 | 2 |
| 요청 1 | DVD1 | DVD3 | 0 | DVD2 | 0 | 1 |

요청 3에서 DVD3은 슬롯 5에 있고 그 앞(슬롯 1–4)의 합이 2이므로 2를 출력한다. 이후 슬롯 5를 비우고 `top = 2`에 올린다. 요청 1에서 DVD1은 슬롯 3에 있고 앞의 합은 슬롯 2의 DVD3 하나라서 1이 된다.

대안으로 세그먼트 트리도 같은 점 갱신과 구간 합을 지원한다. 하지만 이 문제는 prefix sum만 필요하고 구간 갱신이 없어서, 구현이 짧고 상수가 작은 Fenwick Tree가 더 적합하다. 오프라인으로 모든 요청을 미리 읽어 처리하는 방법도 있지만 이 문제에서는 온라인 풀이만으로 충분하다.

| 항목 | 값 |
|---|---|
| 초기화 | $O(n \log(n+m))$ (또는 선형 빌드 가능) |
| 요청 하나 | 질의 1회 + 갱신 2회 = $O(\log(n+m))$ |
| 전체 | $O((n+m)\log(n+m))$ |
| 메모리 | $O(n+m)$ |

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
using namespace std;

// Fenwick Tree 클래스 정의
class FenwickTree {
    vector<int> tree;
    int size;
public:
    // 생성자: 트리 크기를 설정하고 0으로 초기화
    FenwickTree(int n) : size(n) {
        tree.resize(n + 1, 0);
    }
    // 특정 인덱스에 val을 더함 (업데이트)
    void update(int idx, int val) {
        while (idx <= size) {
            tree[idx] += val;
            idx += idx & -idx;
        }
    }
    // 1부터 idx까지의 합을 구함 (쿼리)
    int query(int idx) {
        int res = 0;
        while (idx > 0) {
            res += tree[idx];
            idx -= idx & -idx;
        }
        return res;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; // 테스트 케이스 수
    cin >> T;
    while (T--) {
        int n, m; // 영화의 수 n, 보려고 하는 영화의 수 m
        cin >> n >> m;
        FenwickTree fenwick(n + m); // Fenwick Tree 초기화

        vector<int> pos(n + 1); // 각 영화의 위치 저장
        for (int i = 1; i <= n; ++i) {
            pos[i] = m + i; // 초기 위치 설정 (m + i)
            fenwick.update(pos[i], 1); // 위치에 1을 더함 (영화 존재 표시)
        }

        int top = m; // 가장 위의 위치를 나타내는 변수
        for (int i = 0; i < m; ++i) {
            int movie;
            cin >> movie; // 보고 싶은 영화 번호 입력
            int idx = pos[movie]; // 현재 영화의 위치
            // 해당 영화 위에 있는 DVD의 개수 계산
            int res = fenwick.query(idx - 1);
            cout << res << ' ';

            fenwick.update(idx, -1); // 기존 위치에서 영화 제거
            pos[movie] = top--; // 영화를 가장 위로 이동
            fenwick.update(pos[movie], 1); // 새로운 위치에 영화 추가
        }
        cout << '\n';
    }
    return 0;
}
```

**코드 설명**

`FenwickTree` 클래스는 `idx & -idx`로 최하위 비트를 더하거나 빼며 트리를 오르내리는 표준 구현이다. 크기를 `n + m`으로 잡는 이유는 초기 슬롯이 `m + 1`부터 `m + n`까지 놓이기 때문이다. `pos[i] = m + i`로 초기 위치를 정하고 해당 슬롯에 1을 더해 DVD의 존재를 표시한다. 요청마다 `query(idx - 1)`이 그 DVD 위의 개수를 돌려주고, 그 값을 출력한 뒤 `update(idx, -1)`로 기존 슬롯을 비우고 `pos[movie] = top--`로 새 슬롯을 배정하여 1을 더한다. 처음 두 줄의 `ios::sync_with_stdio(false)`와 `cin.tie(nullptr)`는 테스트 케이스가 많을 때 입출력 시간을 줄이기 위한 것이다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>

#define MAXN 200005

int tree[MAXN];
int size;

void update(int idx, int val) {
    while (idx <= size) {
        tree[idx] += val;
        idx += idx & -idx;
    }
}

int query(int idx) {
    int res = 0;
    while (idx > 0) {
        res += tree[idx];
        idx -= idx & -idx;
    }
    return res;
}

int pos[100005];

int main() {
    int T;
    scanf("%d", &T);
    while (T--) {
        int n, m;
        scanf("%d %d", &n, &m);
        size = n + m;

        // 트리 초기화
        for (int i = 1; i <= size; ++i) tree[i] = 0;

        // 위치 초기화
        for (int i = 1; i <= n; ++i) {
            pos[i] = m + i;
            update(pos[i], 1);
        }

        int top = m;
        for (int i = 0; i < m; ++i) {
            int movie;
            scanf("%d", &movie);
            int idx = pos[movie];
            int res = query(idx - 1);
            printf("%d ", res);
            update(idx, -1);
            pos[movie] = top--;
            update(pos[movie], 1);
        }
        printf("\n");
    }
    return 0;
}
```

**코드 설명**

로직은 위 클래스 버전과 같고 STL 없이 전역 배열만 쓴다. `tree`는 200,005칸으로 $n + m \le 200{,}000$을 수용하고, `pos`는 100,005칸으로 $n \le 100{,}000$을 수용한다. 테스트 케이스마다 `tree`를 `size`까지만 0으로 지우므로 케이스가 많아도 초기화 비용이 입력 크기에 비례한다. 입출력은 `scanf`와 `printf`를 그대로 사용한다.

## Python 코드와 설명

```python
import sys
input = sys.stdin.readline

def update(tree, idx, val, size):
    while idx <= size:
        tree[idx] += val
        idx += idx & -idx

def query(tree, idx):
    res = 0
    while idx > 0:
        res += tree[idx]
        idx -= idx & -idx
    return res

T = int(input())
for _ in range(T):
    n, m = map(int, input().split())
    size = n + m
    tree = [0] * (size + 2)
    pos = [0] * (n + 1)
    for i in range(1, n + 1):
        pos[i] = m + i
        update(tree, pos[i], 1, size)

    movies = list(map(int, input().split()))
    top = m
    res = []
    for movie in movies:
        idx = pos[movie]
        count = query(tree, idx - 1)
        res.append(str(count))
        update(tree, idx, -1, size)
        pos[movie] = top
        update(tree, top, 1, size)
        top -= 1
    print(' '.join(res))
```

**코드 설명**

Python 버전도 같은 알고리즘이며 `sys.stdin.readline`으로 입력을 빠르게 읽고, 결과를 리스트에 모아 `' '.join(res)`로 한 번에 출력한다. 함수 호출 비용 때문에 C++보다 느리므로 입력이 최대 크기일 때는 시간 제한에 여유가 적다는 점을 감안해야 한다.

## 결론

핵심은 DVD를 실제로 옮기지 않고 위치 슬롯의 0/1 배열과 prefix sum으로 "위에 쌓인 개수"를 표현한 것이다. 슬롯을 `m`칸 비워 두고 `top`을 줄여 가며 재활용하면 번호 순서가 쌓인 순서와 일치한다는 불변식이 유지되고, Fenwick Tree가 갱신과 질의를 $O(\log(n+m))$에 처리해 전체 $O((n+m)\log(n+m))$로 문제를 해결한다. 같은 발상은 "원소를 옮기면서 앞쪽 개수를 세는" 다른 문제(예: 순서 재배열 후 inversion 개수 계산)에도 이어진다.

Fenwick Tree의 구조와 증명은 [CP-Algorithms의 Fenwick Tree 문서](https://cp-algorithms.com/data_structures/fenwick.html)에 정리되어 있다. 원 논문은 Peter M. Fenwick, "A New Data Structure for Cumulative Frequency Tables", Software: Practice and Experience 24(3), 1994이다.

## 코너 케이스 및 실수 포인트

| 케이스 | 설명 | 처리 방법 |
|---|---|---|
| **같은 영화 연속 요청** | 맨 위에 있는 DVD를 다시 요청하면 답은 0 | 기존 슬롯 제거 후 새 슬롯 추가 순서를 지키면 자연히 0이 나온다 |
| **m이 n보다 큰 경우** | 같은 DVD를 여러 번 요청 가능 | 트리 크기를 `n`이 아닌 `n + m`으로 잡고 `top`이 1 아래로 내려가지 않음을 확인 |
| **다중 테스트 케이스** | 이전 케이스의 트리·위치가 남음 | 케이스마다 `tree`를 다시 0으로 초기화 |
| **오버플로우** | 답은 최대 $n-1$이라 `int`로 충분 | `long long`은 필요 없다 |
| **출력 형식** | 케이스마다 한 줄, 값은 공백 구분 | 줄 끝 공백이 허용되는지 채점 환경에 맞춰 점검 |
