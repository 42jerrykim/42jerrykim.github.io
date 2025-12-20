---
title: "[Algorithm] C++/Python 백준 10999번 : 구간 합 구하기 2"
description: "세그먼트 트리와 Lazy Propagation(지연 갱신)을 활용해, 크기가 최대 1,000,000에 달하는 배열에 대하여 대규모 구간 덧셈 및 구간 합 쿼리를 O(log N) 시간 내에 빠르고 효율적으로 처리하는 방법을 구현하고 설명합니다."
categories: 
- Algorithm
- Segment Tree
- Range Query
tags:
- SegmentTree
- LazyPropagation
- Implementation
- Optimization
- O(log N)
- DataStructure
- Mathematics
- RangeUpdate
- RangeQuery
image: "index.png"
date: 2024-01-01
---

최근에 세그먼트 트리(Segment Tree)와 Lazy Propagation을 이용한 문제를 접하게 되었고, 그 대표적인 예시 중 하나가 바로 백준 10999번 **구간 합 구하기 2**이다. 많은 범위를 빠르게 갱신하고, 특정 구간의 합을 빠르게 구해야 할 때 사용하기 좋은 알고리즘이다. 오늘은 이 문제를 어떻게 해결할 수 있는지 살펴보도록 한다.

문제 : [https://www.acmicpc.net/problem/10999](https://www.acmicpc.net/problem/10999)

---

## 문제 설명

이 문제는 \(N\)개의 수로 이루어진 배열이 주어지고, 총 \(M + K\)번의 연산을 수행하는 과정을 다룬다. 두 종류의 연산이 존재한다. 첫 번째는 특정 구간 \([b, c]\)에 동일한 값을 더하는 연산이고, 두 번째는 특정 구간 \([b, c]\)의 합을 구하는 연산이다. 이 과정에서 수의 크기는 매우 클 수도 있으며(문제에서 -2^63 이상, 2^63-1 이하의 정수라고 명시), \(N\) 또한 최대 1,000,000에 이를 수 있다. 따라서 단순하게 모든 연산을 반복문으로 처리하면 시간 초과가 발생하기 쉽다.

이를 좀 더 구체적으로 살펴보면, 예를 들어 배열이 \([1, 2, 3, 4, 5]\)로 시작한다고 할 때, “3번째부터 4번째 수에 6을 더한다”는 연산을 수행하면 배열은 \([1, 2, 9, 10, 5]\)가 된다. 그리고 “2번째부터 5번째 수의 합을 구한다”는 쿼리에 대해선 \(2 + 9 + 10 + 5 = 26\)이라는 결과를 얻게 된다. 그다음 “1번째부터 3번째 수에 -2를 더한다”면 배열은 \([-1, 0, 7, 10, 5]\)가 되고, 다시 “2번째부터 5번째 수의 합을 구한다”는 쿼리를 처리하면 \(0 + 7 + 10 + 5 = 22\)가 된다.

이렇게 **구간별로 대규모 업데이트**와 **구간 합 쿼리**가 빈번하게 일어나는 상황에서, 단순한 방법(매번 \([b, c]\) 범위를 순회하여 갱신하거나 합을 구하는 방식)으로는 시간 복잡도가 \(O(N)\)에 달하여, 대규모 입력에 대해서는 절대 시간 내에 해결하기 어렵다. 특히 \(N\)의 최댓값이 1,000,000, 그리고 쿼리 횟수 역시 최대 20,000에 달하므로, 이 둘을 곱하면 최악의 경우 \(2 \times 10^4 \times 10^6 = 2 \times 10^{10}\)번 연산이라는, 매우 큰 수를 처리해야 하는 문제가 발생한다.

따라서 구간 합(혹은 구간에 대한 연산)을 빠르게 처리하기 위한 자료 구조인 **Segment Tree(세그먼트 트리)**와, 구간 업데이트를 효율적으로 처리하는 **Lazy Propagation(지연 갱신) 기법**을 함께 사용하여 \(O(\log N)\) 시간 복잡도로 구간 연산을 처리할 수 있어야 한다. 이를 통해 최대 \(M + K\)번의 연산에도 충분히 빠른 시간 안에 답을 구할 수 있게 된다.

위와 같이, 이 문제는 **세그먼트 트리 + 지연 갱신**을 구현하면 해결할 수 있다. 세그먼트 트리는 구간의 합을 저장하고, Lazy 배열을 사용해 “아직 반영되지 않은 구간 업데이트”를 효율적으로 처리한다. 이 방식의 핵심 아이디어는, 실제로 모든 노드의 값을 매번 업데이트하지 않고, ‘필요한 시점’이 왔을 때에만 자식 노드로 갱신을 전파(propagate)하는 데에 있다. 이러한 접근법을 통해 업데이트와 쿼리 모두 \(O(\log N)\) 내에 처리할 수 있게 된다. 

## 접근 방식

1. **Segment Tree 구축**  
   - 길이 \(N\)인 배열을 빠르게 관리하기 위해, 트리로 구간을 분할하고, 각 구간의 합을 노드에 저장한다.  
   - 일반적으로 트리는 크기가 \(4N\) 정도이면 충분하다.  

2. **Lazy Propagation(지연 갱신)**  
   - 업데이트가 빈번할 경우, 모든 노드를 직접 갱신하면 비효율적이다.  
   - Lazy 배열을 두어, “아직 아래로 전파하지 않은 업데이트 정보”를 임시로 저장하고, 필요할 때만 자식 노드로 정보를 넘겨준다.  

3. **구간 업데이트**  
   - 한 구간 전체에 동일한 값을 더해주어야 한다면, 그 구간을 담당하는 노드에 Lazy 값을 설정한다.  
   - 해당 노드가 실제로 참조될 때(혹은 그 자식 노드를 조회해야 할 때) Lazy 값을 확인하여 본인에게 먼저 반영하고, 자식들에게도 propagate한다.  

4. **구간 합 쿼리**  
   - 현재 노드가 담당하는 구간이 쿼리 구간과 전혀 겹치지 않으면 0을 반환한다.  
   - 노드의 Lazy 값을 propagate로 먼저 처리하여, 트리에 최신화된 정보가 들어 있도록 한다.  
   - 쿼리 구간에 완전히 포함되는 노드라면, 그 노드가 가진 트리 값을 반환한다.  
   - 그렇지 않다면, 자식 노드로 쿼리를 나눠서 구간 합을 구해 합산한다.  

---

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

// 최대 N 크기(문제에서 최대 1,000,000)
static const int MAXN = 1000000;

// 세그먼트 트리 배열과 Lazy 배열
ll segtree[4 * MAXN];
ll lazy[4 * MAXN];

// 입력받을 원본 배열
ll arr[MAXN + 1];

// 세그먼트 트리를 구성하는 함수
// node: 현재 노드 번호
// start, end: arr에서 현재 노드가 담당하는 구간
void build_tree(int node, int start, int end) {
    if (start == end) {
        segtree[node] = arr[start];
        return;
    }
    int mid = (start + end) / 2;
    build_tree(node * 2, start, mid);
    build_tree(node * 2 + 1, mid + 1, end);
    segtree[node] = segtree[node * 2] + segtree[node * 2 + 1];
}

// Lazy 값을 자식에게 전파(propagate)하고, 현재 노드 정보를 갱신한다.
void propagate(int node, int start, int end) {
    if (lazy[node] != 0) {
        segtree[node] += (end - start + 1) * lazy[node];
        // 리프 노드가 아니면 자식 노드 lazy값에 누적
        if (start != end) {
            lazy[node * 2] += lazy[node];
            lazy[node * 2 + 1] += lazy[node];
        }
        lazy[node] = 0;
    }
}

// 구간 [l, r]에 val을 더해주는 함수
void update_range(int node, int start, int end, int l, int r, ll val) {
    // 이전에 남아있는 lazy가 있으면 우선 반영
    propagate(node, start, end);

    // 범위를 벗어난 경우
    if (r < start || end < l) {
        return;
    }
    // 현재 구간이 [l, r]에 완전히 포함되는 경우
    if (l <= start && end <= r) {
        lazy[node] += val;
        propagate(node, start, end);
        return;
    }
    // 부분적으로 겹치는 경우 자식 노드에 나누어서 업데이트
    int mid = (start + end) / 2;
    update_range(node * 2, start, mid, l, r, val);
    update_range(node * 2 + 1, mid + 1, end, l, r, val);
    // 자식 노드들을 업데이트한 뒤, 현재 노드 값 갱신
    segtree[node] = segtree[node * 2] + segtree[node * 2 + 1];
}

// 구간 [l, r]의 합을 구하는 함수
ll query_range(int node, int start, int end, int l, int r) {
    // lazy 값이 있으면 반영
    propagate(node, start, end);

    // 범위를 벗어난 경우
    if (r < start || end < l) {
        return 0LL;
    }
    // 현재 구간이 [l, r]에 완전히 포함
    if (l <= start && end <= r) {
        return segtree[node];
    }
    // 자식 노드에 쿼리를 나누어서 처리
    int mid = (start + end) / 2;
    ll left_sum = query_range(node * 2, start, mid, l, r);
    ll right_sum = query_range(node * 2 + 1, mid + 1, end, l, r);
    return left_sum + right_sum;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M, K;
    cin >> N >> M >> K;

    for(int i = 1; i <= N; i++) {
        cin >> arr[i];
    }

    // 세그먼트 트리 빌드
    build_tree(1, 1, N);

    // 총 M+K 번의 연산 처리
    for(int i = 0; i < M + K; i++){
        ll a, b, c;
        cin >> a >> b >> c;

        if(a == 1) {
            // 구간 [b, c]에 값을 더함
            ll d; 
            cin >> d;
            if(b > c) swap(b, c);
            update_range(1, 1, N, b, c, d);
        }
        else {
            // 구간 [b, c] 합을 출력
            if(b > c) swap(b, c);
            cout << query_range(1, 1, N, b, c) << "\n";
        }
    }

    return 0;
}
```

### C++ 코드 동작 단계별 설명

1. **입력 받기**: \(N\), \(M\), \(K\)를 받고 배열 `arr`에 데이터를 채운다.  
2. **build_tree** 함수 호출: 세그먼트 트리 `segtree` 배열과 지연 배열 `lazy`를 초기화한다.  
3. **연산 처리**: 총 \(M + K\)번의 연산을 순서대로 처리한다.  
   - `a == 1`이면, 구간 업데이트(더하기) 명령이므로 `update_range`를 실행한다.  
   - `a == 2`이면, 구간 합 쿼리 명령이므로 `query_range`를 실행한다.  
4. **Lazy Propagation**: 모든 업데이트와 쿼리는 `propagate`를 통해, 노드에 잠재된 Lazy 값을 미리 반영하고, 필요 시 자식 노드로 이전한다.  

---

## Python 코드와 설명

> **주의**: Python에서는 재귀 깊이에 주의해야 한다. 필요하다면 `sys.setrecursionlimit()`를 사용한다.

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

# 최대 N
MAXN = 1000000

# 전역 세그먼트 트리와 Lazy 배열
segtree = [0] * (4 * MAXN)
lazy = [0] * (4 * MAXN)
arr = []

def build_tree(node, start, end):
    if start == end:
        segtree[node] = arr[start]
        return
    mid = (start + end) // 2
    build_tree(node*2, start, mid)
    build_tree(node*2 + 1, mid+1, end)
    segtree[node] = segtree[node*2] + segtree[node*2 + 1]

def propagate(node, start, end):
    if lazy[node] != 0:
        segtree[node] += (end - start + 1) * lazy[node]
        if start != end:
            lazy[node*2] += lazy[node]
            lazy[node*2 + 1] += lazy[node]
        lazy[node] = 0

def update_range(node, start, end, left, right, val):
    propagate(node, start, end)

    if right < start or end < left:
        return
    
    if left <= start and end <= right:
        lazy[node] += val
        propagate(node, start, end)
        return
    
    mid = (start + end) // 2
    update_range(node*2, start, mid, left, right, val)
    update_range(node*2 + 1, mid+1, end, left, right, val)
    segtree[node] = segtree[node*2] + segtree[node*2 + 1]

def query_range(node, start, end, left, right):
    propagate(node, start, end)

    if right < start or end < left:
        return 0
    
    if left <= start and end <= right:
        return segtree[node]
    
    mid = (start + end) // 2
    left_sum = query_range(node*2, start, mid, left, right)
    right_sum = query_range(node*2 + 1, mid+1, end, left, right)
    return left_sum + right_sum

def main():
    N, M, K = map(int, input().split())
    global arr
    arr = [0] + [int(input()) for _ in range(N)]  # 1-based index

    build_tree(1, 1, N)

    for _ in range(M + K):
        data = list(map(int, input().split()))
        if data[0] == 1:
            # update
            _, b, c, d = data
            if b > c:
                b, c = c, b
            update_range(1, 1, N, b, c, d)
        else:
            # query
            _, b, c = data
            if b > c:
                b, c = c, b
            print(query_range(1, 1, N, b, c))

if __name__ == "__main__":
    main()
```

### Python 코드 동작 단계별 설명

1. **전역 리스트 선언**: `segtree`와 `lazy` 배열을 \(4 \times N\) 크기로 준비한다.  
2. **build_tree**: 입력받은 `arr`를 토대로 세그먼트 트리를 구성한다.  
3. **propagate**: 현재 노드에 Lazy 값이 있으면 구간의 길이만큼 더해주고, 자식 노드가 존재한다면 그 자식 노드들의 Lazy 값에도 동일한 값을 더한다. 작업이 끝나면 현재 노드의 Lazy 값은 0으로 초기화한다.  
4. **update_range**: 구간 \([left, right]\)에 주어진 val을 더해주어야 할 때 사용한다.  
5. **query_range**: 구간 \([left, right]\)의 합을 구하여 반환한다.  
6. **main**: N, M, K를 받은 뒤, 배열을 입력받아 트리를 구성하고, 이후 M+K번의 연산(update / query)을 차례대로 처리한다.  

## 결론

본 문제는 대규모 입력에 대해 구간 합과 구간 업데이트 연산을 빠르게 처리해야 하므로, **세그먼트 트리(Segment Tree)**와 **Lazy Propagation** 기법을 적절히 활용하여 시간 복잡도를 \(O(\log N)\)으로 유지하는 것이 핵심이다. 단순 반복문으로 구현할 경우 시간 초과에 직면할 가능성이 높으며, 세그먼트 트리를 구축하고 Lazy 배열을 운용함으로써 문제를 해결할 수 있다.  

추가적인 최적화로는, 재귀 함수를 반복문으로 바꾸는 방법(Iterative Segment Tree), 혹은 C++에서는 `ios::sync_with_stdio(false)`, `cin.tie(nullptr)` 등의 입출력 최적화를 사용하는 방법이 있다. 그러나 대체로 위 코드와 같은 전형적인 세그먼트 트리 + 지연 갱신 구현만으로도 시간 제한 내에 해결이 가능하다.  

이상으로 백준 10999번 **구간 합 구하기 2** 문제 풀이를 살펴보았다. 이 과정을 통해 **Lazy Propagation**이 주는 이점을 다시금 확인할 수 있었으며, 세그먼트 트리를 조금 더 유연하게 사용할 수 있는 기회가 되었다. 앞으로도 유사한 구간 연산 문제를 만났을 때, 이 기법을 적절하게 적용해보길 바란다.