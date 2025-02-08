---
title: "[Algorithm] C++/Python 백준 16978번 : 수열과 쿼리 22"
categories: 
- Algorithm
- Platinum IV
- DataStructure
- SegmentTree
tags:
- PersistentSegmentTree
- SegmentTree
- DivideAndConquer
- Persistence
- O(logN)
- Tree
- RangeQuery
- Implementation
image: "index.png"
date: 2025-02-08
---

이번 글에서는 백준 16978번 "수열과 쿼리 22" 문제를 다룰 예정이다. 이 문제는 업데이트와 구간 합 쿼리를 동시에 처리해야 하는 상황에서, 여러 버전의 수열 상태를 효율적으로 관리하는 방안을 묻는다. 일반적인 세그먼트 트리를 사용하면 한 시점에 대한 상태만 관리하기 쉽지만, 본 문제는 과거 버전의 상태 역시 쿼리로 요청될 수 있다는 점이 매우 독특하다. 이를 해결하기 위해 영속적 세그먼트 트리(Persistent Segment Tree)라는 기법을 사용할 수 있으며, 업데이트마다 새로운 버전을 생성하되, 변경된 노드만 복사함으로써 메모리를 효율적으로 관리할 수 있다.

문제 : [https://www.acmicpc.net/problem/16978](https://www.acmicpc.net/problem/16978)

## 문제 설명

길이가 N인 정수 수열 A₁, A₂, …, Aₙ이 주어진다. 이때 다음 두 가지 종류의 쿼리를 처리해야 한다. 첫 번째는 “1 i v” 형태로 주어지는 업데이트 쿼리로, 수열의 i번째 원소를 v로 변경한다. 두 번째는 “2 k i j” 형태의 합 쿼리로, k번째 업데이트까지 적용된 상태의 수열에서 i번째부터 j번째 원소까지의 합을 구한다. 즉, 본 문제의 핵심은 업데이트가 이루어질 때마다 새로운 버전을 따로 생성하여, 과거의 버전 또한 쿼리에 대해 유효한 상태를 유지해주어야 한다는 데 있다.

예를 들어, 업데이트 쿼리를 3번 수행했다면, 우리는 0번(초기 상태), 1번, 2번, 3번 버전에 해당하는 네 가지 서로 다른 상태의 수열을 갖게 된다. 이때 “2 2 3 5”라는 쿼리가 들어온다면, 이는 두 번째 업데이트까지 적용된 상태(버전 2)에서 3번째 인덱스부터 5번째 인덱스까지의 합을 요구하는 것이다. 만약 일반적인 세그먼트 트리를 사용한다면, 매번 업데이트에 따라 전체 트리를 다시 구성하거나, 과거의 상태를 별도로 저장해야 하는 부담이 발생할 수 있다. 하지만 영속적 세그먼트 트리에서는 변경된 부분만 새로운 버전으로 복사하고, 나머지는 기존 트리를 참조하게 하여 매 업데이트마다 O(log N)의 시간과 O(log N)의 추가 메모리만으로 모든 버전을 관리할 수 있다.

구체적으로, N과 M(쿼리의 개수)은 최대 100,000까지 주어질 수 있다. 각 쿼리를 매번 O(N)에 처리한다면 최악의 경우 시간 초과가 발생한다. 그러나 세그먼트 트리를 사용하면, 업데이트와 구간 합 모두 O(log N)에 처리할 수 있으므로, M번의 쿼리를 처리해도 최악의 경우 O(M log N) 시간 내에 해결이 가능하다. 다만, 이 문제는 한발 더 나아가서 여러 버전을 유지해야 하므로, 일반 세그먼트 트리 대신 버전을 분기하면서 저장하는 영속적 세그먼트 트리를 활용한다. 이러한 기법은 업데이트마다 전체 트리를 복제하지 않고, 경로상에 있는 노드만 복사하여 새로운 버전을 만든다. 그 결과, 대량의 업데이트 쿼리와 합 쿼리를 모두 빠르게 처리하는 것이 가능해진다.

## 접근 방식

1. **초기 세그먼트 트리 구성**  
   - 길이가 N인 수열을 입력받아, 구간 [1, N]에 대해 세그먼트 트리를 구성한다.  
   - 이 트리가 0번 버전(초기 버전)이 된다.

2. **업데이트 쿼리(1 i v) 처리**  
   - “1 i v” 형태의 쿼리가 들어오면, 이전 버전을 기반으로 i번째 원소를 v로 변경한 새로운 버전을 생성한다.  
   - 영속적 세그먼트 트리는 변경되는 경로상의 노드만 새롭게 할당하고, 나머지는 기존 버전의 노드를 그대로 활용한다.

3. **버전 관리**  
   - 업데이트가 일어날 때마다 새로운 루트 노드의 인덱스(혹은 포인터)를 별도의 구조(예: 배열 roots)에 저장한다.  
   - roots[k]는 k번째 업데이트 이후의 세그먼트 트리 루트를 가리킨다.

4. **합 쿼리(2 k i j) 처리**  
   - “2 k i j” 형태의 쿼리는, k번째 업데이트까지 적용된 수열 버전을 사용하여 [i, j] 구간 합을 구한다.  
   - 즉, roots[k]에 저장된 루트를 참조하여 세그먼트 트리의 query 함수를 호출하고, 구간 합을 O(log N)에 계산한다.

5. **시간 및 메모리 복잡도**  
   - 각 업데이트와 쿼리는 O(log N)에 처리되므로, M번의 쿼리를 O(M log N) 시간 안에 해결할 수 있다.  
   - 버전마다 모든 노드를 복제하지 않고 필요한 노드만 새로 할당하므로, 메모리 효율도 준수하게 유지된다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

// 충분한 노드 개수를 할당하였다.
const int MAX_NODES = 4500000;

// 노드 구조체: 구간 합(sum)과 왼쪽, 오른쪽 자식 인덱스를 저장한다.
struct Node {
    int l, r;
    long long sum;
};

Node tree[MAX_NODES];
int tot = 0;

// build: 구간 [s, e]에서 초기 수열 arr를 기반으로 세그먼트 트리를 구축한다.
int build(int s, int e, const vector<int>& arr) {
    int cur = tot++; 
    if(s == e){
        tree[cur].sum = arr[s-1]; // 배열은 0부터 시작하므로 s-1 사용
        tree[cur].l = -1; 
        tree[cur].r = -1;
        return cur;
    }
    int mid = (s + e) / 2;
    tree[cur].l = build(s, mid, arr);
    tree[cur].r = build(mid+1, e, arr);
    // 두 자식 노드의 합을 구한다.
    tree[cur].sum = tree[tree[cur].l].sum + tree[tree[cur].r].sum;
    return cur;
}

// update: 이전 버전 prev를 참조하여, 구간 [s, e]에서 pos를 val로 갱신한 새로운 버전을 만든다.
int update(int prev, int s, int e, int pos, int val) {
    int cur = tot++; 
    if(s == e){
        // 리프 노드에서 값을 갱신
        tree[cur].sum = val;
        tree[cur].l = -1;
        tree[cur].r = -1;
        return cur;
    }
    int mid = (s + e) / 2;
    if(pos <= mid) {
        // 왼쪽 서브트리를 업데이트
        tree[cur].l = update(tree[prev].l, s, mid, pos, val);
        // 오른쪽 서브트리는 이전 버전 그대로 참조
        tree[cur].r = tree[prev].r;
    } else {
        // 왼쪽 서브트리는 이전 버전 그대로 참조
        tree[cur].l = tree[prev].l;
        // 오른쪽 서브트리를 업데이트
        tree[cur].r = update(tree[prev].r, mid+1, e, pos, val);
    }
    // 자식들의 합을 통해 현재 노드 합 계산
    tree[cur].sum = tree[tree[cur].l].sum + tree[tree[cur].r].sum;
    return cur;
}

// query: 버전 cur에서, 구간 [lq, rq]의 합을 구한다.
long long query(int cur, int s, int e, int lq, int rq) {
    if(rq < s || e < lq) return 0; 
    if(lq <= s && e <= rq) return tree[cur].sum;
    int mid = (s + e) / 2;
    return query(tree[cur].l, s, mid, lq, rq) + query(tree[cur].r, mid+1, e, lq, rq);
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;
    vector<int> arr(N);
    for(int i=0; i<N; i++){
        cin >> arr[i];
    }

    // 0번 버전(초기 버전) 트리 생성
    int root0 = build(1, N, arr);
    vector<int> roots;
    roots.push_back(root0);
    int updateCount = 0;

    int M;
    cin >> M;
    for(int i=0; i<M; i++){
        int type;
        cin >> type;
        if(type == 1){
            // 업데이트 쿼리
            int idx, val;
            cin >> idx >> val;
            // 가장 최근 버전을 기반으로 새로운 버전을 만든다.
            int newRoot = update(roots[updateCount], 1, N, idx, val);
            roots.push_back(newRoot);
            updateCount++;
        } else {
            // 합 쿼리
            int k, l, r;
            cin >> k >> l >> r;
            long long ans = query(roots[k], 1, N, l, r);
            cout << ans << "\n";
        }
    }
    return 0;
}
```

### C++ 코드 동작 단계별 설명
1. **build 함수**에서 N개의 원소를 바탕으로 0번 버전 트리를 구성한다.  
2. 각 업데이트(“1 i v”)가 발생할 때마다, `update` 함수를 호출하여 변경 경로의 노드만 새로 할당하고, 나머지는 이전 버전의 노드를 참조하게 만든다.  
3. 여러 개의 버전 루트를 `roots` 벡터에 차곡차곡 저장한다.  
4. 합 쿼리(“2 k i j”)가 들어오면, `roots[k]`를 루트로 하는 트리에서 [i, j] 구간 합을 `query` 함수로 구한다.  
5. 모든 쿼리가 처리된 뒤, 각 결과를 순서대로 출력한다.

## Python 코드와 설명

```python
import sys
sys.setrecursionlimit(300000)
input = sys.stdin.readline

tree = []
tot = 0

# build: 구간 [s, e]에 대해 초기 수열 arr로 트리를 구성한다.
def build(s, e, arr):
    global tot
    cur = tot
    tot += 1
    # 노드를 임시 할당한다. (l, r, sum) 형태
    tree.append((None, None, 0))

    if s == e:
        tree[cur] = (-1, -1, arr[s-1])  # 리프 노드에 실제 값 저장
        return cur

    mid = (s + e) // 2
    left = build(s, mid, arr)
    right = build(mid+1, e, arr)
    tree[cur] = (left, right, tree[left][2] + tree[right][2])  # 자식 합
    return cur

# update: 이전 버전 prev를 바탕으로 pos 위치를 val로 갱신한다.
def update(prev, s, e, pos, val):
    global tot
    cur = tot
    tot += 1
    tree.append((None, None, 0))

    if s == e:
        tree[cur] = (-1, -1, val)  # 리프 노드 갱신
        return cur

    mid = (s + e) // 2
    l, r, _sum = tree[prev]
    if pos <= mid:
        newLeft = update(l, s, mid, pos, val)
        tree[cur] = (newLeft, r, tree[newLeft][2] + tree[r][2])
    else:
        newRight = update(r, mid+1, e, pos, val)
        tree[cur] = (l, newRight, tree[l][2] + tree[newRight][2])
    return cur

# query: 현재 버전(cur)에서 [lq, rq] 구간 합을 구한다.
def query(cur, s, e, lq, rq):
    if rq < s or e < lq:
        return 0
    if lq <= s and e <= rq:
        return tree[cur][2]
    mid = (s + e) // 2
    l, r, _sum = tree[cur]
    return query(l, s, mid, lq, rq) + query(r, mid+1, e, lq, rq)

def main():
    global tot
    N = int(input())
    arr = list(map(int, input().split()))
    # 0번 버전 트리 생성
    root0 = build(1, N, arr)
    roots = [root0]  # 모든 버전의 루트를 관리한다.
    updateCount = 0

    M = int(input())
    for _ in range(M):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            # 업데이트 쿼리: (1, i, v)
            _, i, v = tmp
            newRoot = update(roots[updateCount], 1, N, i, v)
            roots.append(newRoot)
            updateCount += 1
        else:
            # 합 쿼리: (2, k, i, j)
            _, k, i, j = tmp
            ans = query(roots[k], 1, N, i, j)
            print(ans)

if __name__ == '__main__':
    main()
```

### Python 코드 동작 단계별 설명

1. `tree` 리스트를 전역에 두고, 노드를 (l, r, sum) 형태로 저장한다.  
2. `build` 함수를 통해 0번 버전을 생성한다.  
3. `update` 함수는 pos에 해당하는 원소를 val로 변경하면서, 새 노드를 생성하여 새로운 버전을 만든다. 변경되지 않는 자식은 기존 노드를 그대로 참조한다.  
4. `roots` 리스트를 통해 여러 버전에 접근할 수 있도록 관리한다.  
5. 합 쿼리가 들어오면 `roots[k]`에서 `query` 함수를 수행해 [i, j] 구간 합을 빠르게 계산한다.

## 결론

본 문제는 단순히 세그먼트 트리를 구성하고 업데이트, 쿼리를 수행하는 것을 넘어, 여러 버전의 수열 상태를 동시에 관리해야 한다는 점이 핵심이다. 영속적 세그먼트 트리를 활용하면, 과거 버전에 대한 쿼리를 빠르게 처리하면서, 새로운 업데이트 버전을 생성해도 메모리를 과도하게 소모하지 않는다. 이를 통해 최대 100,000번의 쿼리가 주어져도 문제를 효과적으로 해결할 수 있다. 구현 시에는 각 버전을 루트 노드로 잘 구분하여 저장하는 것과, 변경되는 노드만 복사해 새로운 버전을 만드는 로직에 주의해야 한다. 더 나아가, 비슷한 방식으로 구간 최소/최대 등의 쿼리를 수행할 수도 있으며, 다양한 문제 유형에 영속적 자료 구조를 응용해볼 수 있다.  