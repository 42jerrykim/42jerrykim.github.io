---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-25T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- FenwickTree
- DataStructures
- O(log N)
- Simulation
- Stack
title: '[Algorithm] C++/Python 백준 3653번 : 영화 수집'

---

상근이는 영화 DVD를 수집하는 열성적인 수집가이다. 그는 자신의 DVD 콜렉션을 탑처럼 쌓아 보관한다. 영화를 보고 싶을 때마다 DVD의 위치를 찾아서, 쌓여 있는 콜렉션이 무너지지 않도록 조심스럽게 해당 DVD를 꺼낸다. 영화를 다 본 후에는 그 DVD를 가장 위에 놓는다.

하지만 상근이가 보유한 DVD의 수가 너무 많아, 원하는 DVD를 찾는 데 시간이 오래 걸린다. 각 DVD의 위치를 쉽게 찾기 위해, 찾으려는 DVD 위에 몇 개의 DVD가 있는지만 알면 된다. 각 DVD는 표지에 붙어 있는 번호로 구별할 수 있다.

이때, 각 DVD의 위치를 기록하는 프로그램을 작성하고자 한다. 상근이가 영화를 한 편 볼 때마다 그 DVD 위에 몇 개의 DVD가 있었는지를 출력해야 한다. 또한, 상근이는 매번 영화를 볼 때마다 본 DVD를 가장 위에 놓는다.

프로그램은 여러 테스트 케이스를 처리해야 하며, 각 테스트 케이스마다 상근이가 가지고 있는 영화의 수 $n$과 보려고 하는 영화의 수 $m$이 주어진다. 이어서 $m$개의 영화 번호가 순서대로 주어진다. 가장 처음에는 영화들이 1번부터 $n$번까지 번호 순서대로 쌓여 있으며, 가장 위에 있는 영화의 번호는 1번이다.

각각의 영화에 대해, 그 영화를 볼 때 해당 DVD 위에 몇 개의 DVD가 있었는지를 구해야 한다.

문제 : [https://www.acmicpc.net/problem/3653](https://www.acmicpc.net/problem/3653)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제는 DVD 콜렉션을 스택으로 관리하면서, 각 DVD의 위치 변화를 효율적으로 추적해야 한다. 각 DVD에 대해 그 위에 몇 개의 DVD가 있는지를 빠르게 계산해야 하므로, 매번 선형 탐색을 하면 시간 초과가 발생한다.

이를 해결하기 위해 **Fenwick Tree**(이진 인덱스 트리)를 사용한다. Fenwick Tree는 배열의 부분 합을 효율적으로 계산하고 업데이트할 수 있는 자료 구조로, $O(\log N)$의 시간 복잡도로 쿼리와 업데이트를 수행할 수 있다.

DVD의 위치를 Fenwick Tree의 인덱스로 매핑하고, 각 위치에 DVD가 있는지를 표시한다. DVD를 가장 위로 옮길 때마다 해당 DVD의 위치를 업데이트하고, 그 위에 몇 개의 DVD가 있는지를 계산하기 위해 현재 위치보다 작은 인덱스의 합을 구한다.

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

1. **Fenwick Tree 클래스 정의**: 배열의 부분 합을 빠르게 계산하기 위해 Fenwick Tree를 사용한다.

2. **입력 처리**: 테스트 케이스 수 `T`를 입력받고, 각 테스트 케이스마다 `n`과 `m`을 입력받는다.

3. **초기화**:
   - 각 영화의 초기 위치를 `pos[i] = m + i`로 설정한다. 이는 새로운 영화가 쌓일 공간(`m`개)을 고려하여 기존 영화의 위치를 설정한 것이다.
   - Fenwick Tree에 해당 위치에 영화가 있음을 표시하기 위해 `update` 함수를 호출하여 1을 더한다.

4. **영화 시청 및 위치 업데이트**:
   - 각 요청된 영화 번호를 입력받는다.
   - 해당 영화의 현재 위치 `idx`를 가져온다.
   - Fenwick Tree의 `query` 함수를 사용하여 `idx - 1` 위치까지의 합을 구한다. 이는 해당 영화 위에 있는 DVD의 수를 의미한다.
   - 결과를 출력한다.
   - 현재 위치에서 해당 영화를 제거하기 위해 `update(idx, -1)`을 호출한다.
   - 영화를 가장 위로 이동시키기 위해 `pos[movie] = top--`으로 위치를 갱신하고, Fenwick Tree에 `update(pos[movie], 1)`로 새로운 위치에 영화를 추가한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>

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

1. **헤더 파일 포함**: `stdio.h`와 `stdlib.h`만 포함한다.

2. **전역 변수 선언**:
   - `tree[]`: Fenwick Tree 배열을 전역 변수로 선언한다.
   - `size`: 트리의 크기를 나타내는 변수.
   - `pos[]`: 각 영화의 위치를 저장하는 배열.

3. **Fenwick Tree 함수 정의**:
   - `update(int idx, int val)`: 트리의 특정 인덱스에 값을 더하거나 뺀다.
   - `query(int idx)`: 1부터 `idx`까지의 합을 구한다.

4. **메인 함수**:
   - 테스트 케이스 수를 입력받는다.
   - 각 테스트 케이스마다 `n`과 `m`을 입력받고, 트리와 위치 배열을 초기화한다.
   - 각 영화의 초기 위치를 설정하고, 트리에 반영한다.
   - 각 영화 요청에 대해:
     - 현재 위치에서 위에 있는 DVD 수를 계산하여 출력한다.
     - 해당 영화를 트리에서 제거하고, 새로운 위치로 이동시킨 후 트리에 반영한다.

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

1. **입출력 최적화**: `sys.stdin.readline`을 사용하여 입력 속도를 높인다.

2. **Fenwick Tree 함수 정의**:
   - `update(tree, idx, val, size)`: 트리의 특정 인덱스에 값을 더하거나 뺀다.
   - `query(tree, idx)`: 1부터 `idx`까지의 합을 구한다.

3. **메인 로직**:
   - 테스트 케이스 수를 입력받는다.
   - 각 테스트 케이스마다 `n`과 `m`을 입력받고, 트리와 위치 배열을 초기화한다.
   - 각 영화의 초기 위치를 설정하고, 트리에 반영한다.
   - 영화 요청 리스트를 입력받는다.
   - 각 영화 요청에 대해:
     - 현재 위치에서 위에 있는 DVD 수를 계산하여 결과 리스트에 추가한다.
     - 해당 영화를 트리에서 제거하고, 새로운 위치로 이동시킨 후 트리에 반영한다.
   - 결과 리스트를 공백으로 구분하여 출력한다.

## 결론

이 문제는 Fenwick Tree를 활용하여 스택에 쌓인 DVD의 위치를 효율적으로 관리하는 것이 핵심이다. 각 영화의 위치를 트리 인덱스로 매핑하고, 업데이트와 쿼리를 $O(\log N)$에 수행함으로써 시간 초과 없이 모든 테스트 케이스를 처리할 수 있었다. 이와 같은 자료 구조를 활용한 문제는 초기에는 복잡해 보일 수 있지만, 원리를 이해하고 나면 다양한 응용이 가능하므로 연습을 통해 익숙해지는 것이 중요하다.