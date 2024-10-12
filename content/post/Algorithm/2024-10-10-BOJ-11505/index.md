---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-10-10T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Segment Tree
- Range Query
- Modular Arithmetic
- Data Structures
- Efficient Algorithms
- Time Complexity
- O(log N)
title: '[Algorithm] C++/Python 백준 11505번 : 구간 곱 구하기'
---

어떤 N개의 수가 주어져 있을 때, 이 수들에 대한 구간 곱을 효율적으로 구하고, 중간에 수의 변경이 빈번히 일어나는 상황을 고려해보자. 예를 들어, 수열이 1, 2, 3, 4, 5로 주어지고, 세 번째 수를 6으로 바꾼 후에 두 번째부터 다섯 번째까지의 곱을 구하면 240이 된다. 여기서 다섯 번째 수를 2로 변경하고, 세 번째부터 다섯 번째까지의 곱을 구하면 48이 된다.

이러한 문제를 해결하기 위해서는 수의 변경과 구간 곱 계산을 효율적으로 처리할 수 있는 자료 구조가 필요하다. 이 글에서는 백준 온라인 저지 11505번 "구간 곱 구하기" 문제를 해결하기 위한 알고리즘과 코드 구현에 대해 알아보겠다.

문제 : [https://www.acmicpc.net/problem/11505](https://www.acmicpc.net/problem/11505)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 문제 설명

어떤 N개의 수가 주어져 있다. 이 수들은 수열을 이루며, 수의 개수 N은 1 이상 1,000,000 이하이다. 이때, 다음과 같은 두 가지 쿼리를 처리해야 한다:

1. **수의 변경**: 특정 위치의 수를 다른 수로 변경한다.
2. **구간 곱 계산**: 특정 구간에 있는 수들의 곱을 구한다.

하지만 여기서 중요한 것은 수의 변경과 구간 곱 계산이 매우 빈번하게 일어난다는 것이다. 따라서 단순히 모든 연산을 수행할 때마다 배열을 순회하며 곱을 계산하면 시간 초과가 발생한다.

또한, 모든 연산의 결과는 1,000,000,007로 나눈 나머지를 출력해야 한다. 이는 결과 값이 매우 커질 수 있으므로, 계산 중간에도 모듈러 연산을 적용하여 오버플로우를 방지해야 한다.

**예시**:

- 초기 수열: `1, 2, 3, 4, 5`
- 첫 번째 연산: 세 번째 수를 `6`으로 변경
- 두 번째 연산: 두 번째부터 다섯 번째 수까지의 곱을 구함 ⇒ `2 * 6 * 4 * 5 = 240`
- 세 번째 연산: 다섯 번째 수를 `2`로 변경
- 네 번째 연산: 세 번째부터 다섯 번째 수까지의 곱을 구함 ⇒ `6 * 4 * 2 = 48`

이러한 연산들을 효율적으로 처리하기 위해서는 적절한 자료 구조와 알고리즘이 필요하다.

## 접근 방식

이 문제는 수의 변경과 구간 곱 계산을 효율적으로 처리해야 하므로, **세그먼트 트리(Segment Tree)**를 사용하는 것이 적합하다. 세그먼트 트리는 구간에 대한 정보를 트리 형태로 저장하여, 업데이트와 쿼리를 O(log N)의 시간 복잡도로 처리할 수 있다.

하지만 일반적인 세그먼트 트리에서는 덧셈 연산을 주로 사용하며, **곱셈의 경우에는 0이 포함될 때 주의**해야 한다. 곱셈에서 0이 하나라도 있으면 전체 곱셈 결과가 0이 되므로, 각 노드에서 해당 구간에 0이 존재하는지 여부를 추가로 저장해야 한다.

따라서, 각 세그먼트 트리의 노드는 다음과 같은 정보를 저장한다:

- `zero_count`: 해당 구간에 포함된 0의 개수
- `product`: 해당 구간의 모든 0이 아닌 수들의 곱을 MOD로 나눈 나머지

이를 통해, 쿼리 시에 해당 구간에 0이 하나라도 존재하면 결과는 0이 되며, 그렇지 않다면 곱셈 연산을 수행하면 된다.

## C++ 코드와 설명

먼저, 필요한 헤더를 포함한다.

```cpp
#include <iostream>
#include <vector>
#define MOD 1000000007

using namespace std;
```

데이터를 저장할 구조체를 정의한다.

```cpp
struct Node {
    int zero_count;       // 구간 내 0의 개수
    int64_t product;      // 구간 내 0이 아닌 수들의 곱
};
```

전역 변수 및 배열을 선언한다.

```cpp
int N, M, K;
vector<int64_t> arr;      // 초기 수열을 저장할 배열
vector<Node> tree;        // 세그먼트 트리
```

세그먼트 트리를 구축하는 함수이다.

```cpp
void build(int node, int start, int end) {
    if (start == end) {
        // 리프 노드일 경우
        if (arr[start] == 0) {
            tree[node].zero_count = 1;
            tree[node].product = 1; // 곱셈의 항등원
        } else {
            tree[node].zero_count = 0;
            tree[node].product = arr[start] % MOD;
        }
    } else {
        // 내부 노드일 경우
        int mid = (start + end) / 2;
        build(node * 2, start, mid);          // 왼쪽 자식 노드
        build(node * 2 + 1, mid + 1, end);    // 오른쪽 자식 노드

        tree[node].zero_count = tree[node * 2].zero_count + tree[node * 2 + 1].zero_count;

        if (tree[node].zero_count > 0) {
            tree[node].product = 1; // 0이 존재하므로 곱은 0
        } else {
            tree[node].product = (tree[node * 2].product * tree[node * 2 + 1].product) % MOD;
        }
    }
}
```

특정 위치의 값을 변경하는 업데이트 함수이다.

```cpp
void update(int node, int start, int end, int idx, int64_t val) {
    if (start == end) {
        // 리프 노드 업데이트
        arr[idx] = val;
        if (val == 0) {
            tree[node].zero_count = 1;
            tree[node].product = 1;
        } else {
            tree[node].zero_count = 0;
            tree[node].product = val % MOD;
        }
    } else {
        int mid = (start + end) / 2;
        if (idx <= mid) {
            update(node * 2, start, mid, idx, val); // 왼쪽 자식 노드 갱신
        } else {
            update(node * 2 + 1, mid + 1, end, idx, val); // 오른쪽 자식 노드 갱신
        }

        tree[node].zero_count = tree[node * 2].zero_count + tree[node * 2 + 1].zero_count;

        if (tree[node].zero_count > 0) {
            tree[node].product = 1;
        } else {
            tree[node].product = (tree[node * 2].product * tree[node * 2 + 1].product) % MOD;
        }
    }
}
```

구간 곱을 계산하는 쿼리 함수이다.

```cpp
int64_t query(int node, int start, int end, int l, int r) {
    if (r < start || end < l) {
        // 구간이 겹치지 않음
        return 1; // 곱셈의 항등원 반환
    }
    if (l <= start && end <= r) {
        // 구간이 완전히 포함됨
        if (tree[node].zero_count > 0) {
            return 0;
        } else {
            return tree[node].product % MOD;
        }
    }

    int mid = (start + end) / 2;
    int64_t left_product = query(node * 2, start, mid, l, r);
    int64_t right_product = query(node * 2 + 1, mid + 1, end, l, r);

    return (left_product * right_product) % MOD;
}
```

메인 함수에서는 입력을 받고 쿼리를 처리한다.

```cpp
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> M >> K;
    arr.resize(N + 1);
    tree.resize(4 * N);

    for (int i = 1; i <= N; ++i) {
        cin >> arr[i];
    }

    build(1, 1, N);

    int total_ops = M + K;

    for (int i = 0; i < total_ops; ++i) {
        int a;
        int64_t b, c;
        cin >> a >> b >> c;

        if (a == 1) {
            // 값 변경 연산
            update(1, 1, N, b, c);
        } else if (a == 2) {
            // 구간 곱 계산 연산
            int64_t result = query(1, 1, N, b, c);
            cout << result % MOD << '\n';
        }
    }

    return 0;
}
```

## C++ without library 코드와 설명

이번에는 표준 라이브러리 없이 C 스타일로 코드를 작성하겠다.

```cpp
#include <stdio.h>
#include <stdlib.h>
#define MOD 1000000007
#define MAX_N 1000000

typedef struct {
    int zero_count;
    long long product;
} Node;

int N, M, K;
long long arr[MAX_N + 1];
Node tree[4 * MAX_N];

void build(int node, int start, int end) {
    if (start == end) {
        if (arr[start] == 0) {
            tree[node].zero_count = 1;
            tree[node].product = 1;
        } else {
            tree[node].zero_count = 0;
            tree[node].product = arr[start] % MOD;
        }
    } else {
        int mid = (start + end) / 2;
        build(node * 2, start, mid);
        build(node * 2 + 1, mid + 1, end);

        tree[node].zero_count = tree[node * 2].zero_count + tree[node * 2 + 1].zero_count;

        if (tree[node].zero_count > 0) {
            tree[node].product = 1;
        } else {
            tree[node].product = (tree[node * 2].product * tree[node * 2 + 1].product) % MOD;
        }
    }
}

void update(int node, int start, int end, int idx, long long val) {
    if (start == end) {
        arr[idx] = val;
        if (val == 0) {
            tree[node].zero_count = 1;
            tree[node].product = 1;
        } else {
            tree[node].zero_count = 0;
            tree[node].product = val % MOD;
        }
    } else {
        int mid = (start + end) / 2;
        if (idx <= mid) {
            update(node * 2, start, mid, idx, val);
        } else {
            update(node * 2 + 1, mid + 1, end, idx, val);
        }

        tree[node].zero_count = tree[node * 2].zero_count + tree[node * 2 + 1].zero_count;

        if (tree[node].zero_count > 0) {
            tree[node].product = 1;
        } else {
            tree[node].product = (tree[node * 2].product * tree[node * 2 + 1].product) % MOD;
        }
    }
}

long long query(int node, int start, int end, int l, int r) {
    if (r < start || end < l) {
        return 1;
    }
    if (l <= start && end <= r) {
        if (tree[node].zero_count > 0) {
            return 0;
        } else {
            return tree[node].product % MOD;
        }
    }

    int mid = (start + end) / 2;
    long long left_product = query(node * 2, start, mid, l, r);
    long long right_product = query(node * 2 + 1, mid + 1, end, l, r);

    return (left_product * right_product) % MOD;
}

int main() {
    scanf("%d %d %d", &N, &M, &K);

    for (int i = 1; i <= N; ++i) {
        scanf("%lld", &arr[i]);
    }

    build(1, 1, N);

    int total_ops = M + K;

    for (int i = 0; i < total_ops; ++i) {
        int a;
        long long b, c;
        scanf("%d %lld %lld", &a, &b, &c);

        if (a == 1) {
            update(1, 1, N, b, c);
        } else if (a == 2) {
            long long result = query(1, 1, N, b, c);
            printf("%lld\n", result % MOD);
        }
    }

    return 0;
}
```

**코드 설명**

- `stdio.h`와 `stdlib.h`만 사용하여 입출력과 동적 메모리 할당을 처리한다.
- 배열과 구조체를 사용하여 세그먼트 트리를 구현한다.
- 업데이트와 쿼리 함수는 앞서 설명한 C++ 코드와 동일한 로직을 따른다.

## Python 코드와 설명

이제 메모리 초과를 방지하기 위해 `threading` 모듈을 사용하지 않고, 메모리 사용을 최적화한 Python 코드를 작성하겠다.

```python
import sys

MOD = 1000000007
input = sys.stdin.readline

def build():
    # 리프 노드 초기화
    for i in range(N):
        idx = size + i
        val = arr[i]
        if val == 0:
            tree_zero[idx] = 1
            tree_prod[idx] = 1
        else:
            tree_zero[idx] = 0
            tree_prod[idx] = val % MOD

    # 내부 노드 초기화
    for idx in range(size - 1, 0, -1):
        left = idx << 1
        right = left | 1
        tree_zero[idx] = tree_zero[left] + tree_zero[right]
        if tree_zero[idx]:
            tree_prod[idx] = 1
        else:
            tree_prod[idx] = (tree_prod[left] * tree_prod[right]) % MOD

def update(pos, val):
    idx = size + pos
    if val == 0:
        tree_zero[idx] = 1
        tree_prod[idx] = 1
    else:
        tree_zero[idx] = 0
        tree_prod[idx] = val % MOD
    idx >>= 1
    while idx:
        left = idx << 1
        right = left | 1
        tree_zero[idx] = tree_zero[left] + tree_zero[right]
        if tree_zero[idx]:
            tree_prod[idx] = 1
        else:
            tree_prod[idx] = (tree_prod[left] * tree_prod[right]) % MOD
        idx >>= 1

def query(l, r):
    l += size
    r += size
    zero_count = 0
    result = 1
    while l <= r:
        if l % 2 == 1:
            zero_count += tree_zero[l]
            if zero_count == 0:
                result = (result * tree_prod[l]) % MOD
            l += 1
        if r % 2 == 0:
            zero_count += tree_zero[r]
            if zero_count == 0:
                result = (result * tree_prod[r]) % MOD
            r -= 1
        l >>= 1
        r >>= 1
    return 0 if zero_count else result % MOD

N, M, K = map(int, input().split())
arr = [int(input()) for _ in range(N)]
size = 1
while size < N:
    size <<= 1

tree_zero = [0] * (size << 1)
tree_prod = [1] * (size << 1)

build()

for _ in range(M + K):
    cmd = ''
    while cmd.strip() == '':
        cmd = input()
    a, b, c = map(int, cmd.strip().split())
    if a == 1:
        # 업데이트 연산
        update(b - 1, c)
    else:
        # 쿼리 연산
        res = query(b - 1, c - 1)
        print(res)
```

**코드 설명**

- **입력 최적화**: `sys.stdin.readline()`을 사용하여 입력을 빠르게 받는다.
- **세그먼트 트리 구현**:
  - 배열 크기를 가장 가까운 `2의 제곱 수`로 설정하여 완전 이진 트리를 만든다.
  - 리프 노드와 내부 노드를 초기화하는 `build()` 함수를 사용한다.
  - 업데이트 연산은 `update()` 함수를 통해 O(log N) 시간에 처리한다.
  - 쿼리 연산은 `query()` 함수를 통해 O(log N) 시간에 처리한다.
- **메모리 사용 최적화**:
  - `threading` 모듈을 사용하지 않아 추가적인 메모리 사용을 방지한다.
  - 배열 인덱싱을 효율적으로 처리하여 메모리 낭비를 최소화한다.
- **입력 처리 주의사항**:
  - 입력 줄이 비어 있을 경우를 대비하여 `while` 문을 사용하여 입력을 받는다.
  - 이는 온라인 저지에서 입력의 끝에 공백이 있을 수 있기 때문이다.

## 결론

이번 문제는 세그먼트 트리를 이용하여 수의 변경과 구간 곱 계산을 효율적으로 처리하는 방법을 학습할 수 있었다. 특히, 곱셈 연산에서 0이 존재할 경우를 처리하기 위해 추가적인 정보를 저장하는 아이디어가 중요했다. 이를 통해 O(log N)의 시간 복잡도로 모든 연산을 수행할 수 있었다.

이번 문제는 세그먼트 트리를 이용하여 수의 변경과 구간 곱 계산을 효율적으로 처리하는 방법을 학습할 수 있었다. 특히, Python에서 메모리 초과를 방지하기 위해 `threading` 모듈을 사용하지 않고도 효율적인 코드를 작성하는 것이 중요했다. 이를 통해 O(log N)의 시간 복잡도로 모든 연산을 수행할 수 있었다.

앞으로도 이러한 자료 구조와 알고리즘을 활용하여 다양한 문제를 효율적으로 해결할 수 있도록 노력해야겠다.