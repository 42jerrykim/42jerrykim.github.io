---
title: "[Algorithm] C++/Python 백준 18251번 : 내 생각에 A번인 단순 dfs 문제가 이 대회에서 E번이 되어버린 건에 관하여 (Easy)"
date: "2025-02-08"
categories:
- Algorithm
- Platinum IV
tags:
- perfect binary tree
- Kadane's Algorithm
- Maximum Sum
- 다이나믹 프로그래밍
- 그래프 이론
- 그래프 탐색
- 깊이 우선 탐색
- 스위핑
- 구현
- 트리
- 최적화
- 최대 부분 합
- 최적화
image: "index.png"
---


이 문제는 포화 이진 트리(Perfect Binary Tree)에서 노드들의 가중치 합이 최대가 되는 직사각형 영역을 찾는 문제이다. 문제의 핵심은 트리 구조를 기하학적으로 해석하여, 노드들의 위치를 x-y 좌표계에 매핑하고, 이들 노드들로 구성될 수 있는 모든 가능한 직사각형 영역 중에서 가중치 합이 최대인 영역을 효율적으로 찾는 것이다.

문제 : [https://www.acmicpc.net/problem/18251](https://www.acmicpc.net/problem/18251)

이 문제를 해결하기 위해서는 perfect binary tree의 node layout에서 rectangular area의 최대 합을 찾아야 한다. 여기서 node들은 특정 순서로 배열되어 있으며, key challenge는 node weights의 합을 최대화하는 최적의 rectangular area를 효율적으로 결정하는 것이다.

### 접근 방식

문제의 주요 특징은 다음과 같다:

1. **트리 구조**: 포화 이진 트리이므로 모든 레벨이 완전히 채워져 있고, 노드 개수는 N = 2^k - 1 형태이다.
2. **좌표계 매핑**: 
   - x좌표: in-order traversal 순서에 따라 결정된다. 즉, 왼쪽 서브트리 노드들은 현재 노드보다 작은 x좌표를, 오른쪽 서브트리 노드들은 큰 x좌표를 가진다.
   - y좌표: 트리의 깊이(레벨)에 따라 결정된다. 루트 노드가 가장 높은 y좌표를 가지며, 깊이가 깊어질수록 y좌표는 감소한다.
3. **직사각형 조건**: 
   - 축에 평행해야 하며, 변이 노드에 걸치면 안 된다.
   - 하나 이상의 노드를 포함해야 한다.

문제 해결을 위한 주요 접근 방식은 다음과 같다:

1. **Tree Structure Analysis**: 이 트리는 perfect binary tree이다. 즉, leaf node를 제외한 모든 node는 정확히 두 개의 child node를 가진다. Node들은 in-order traversal이 x-coordinate를 제공하고, depth(level)이 y-coordinate를 제공하도록 배열되어 있다.
2. **Coordinate Calculation**: 각 node에 대해 in-order traversal에서의 위치를 기반으로 x-coordinate를 계산하고, 트리에서의 level을 기반으로 y-coordinate를 계산한다.
3. **Depth Intervals**: 가능한 모든 depth interval에 대해 해당 depth 범위 내의 모든 node를 수집하고 x-coordinate를 기준으로 정렬한다.
4. **Kadane's Algorithm**: 각 depth interval에 대해 정렬된 node list에 Kadane's algorithm을 적용하여 maximum subarray sum을 찾는다. 이는 최적의 rectangular area에 해당한다.

이 문제는 트리 구조를 기하학적으로 해석하고, 다차원 데이터에서 최적의 영역을 찾는 문제로, 트리 탐색과 동적 프로그래밍 기법을 결합하여 해결할 수 있다. 시간 복잡도는 O(N^2)이며, N이 최대 262,143까지 가능하므로 효율적인 구현이 중요하다.

### Solution Code
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

using namespace std;

struct Node {
    int x, y, w;
    Node(int x, int y, int w) : x(x), y(y), w(w) {}
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    vector<int> W(N);
    for (int i = 0; i < N; ++i) {
        cin >> W[i];
    }

    int H = 32 - __builtin_clz(N + 1) - 1; // log2(N+1)

    vector<Node> nodes;
    nodes.reserve(N);

    for (int u = 1; u <= N; ++u) {
        int depth_u = 32 - __builtin_clz(u);
        int sum_ancestors = 0;

        int current = u;
        while (current != 1) {
            int parent = current / 2;
            if (current % 2 == 1) { // right child
                int depth_parent = 32 - __builtin_clz(parent);
                int h_a = H - (depth_parent - 1);
                int left_size_a = (1 << (h_a - 1)) - 1;
                sum_ancestors += left_size_a + 1;
            }
            current = parent;
        }

        int h_u = H - (depth_u - 1);
        int left_size_u = (1 << (h_u - 1)) - 1;
        int x = sum_ancestors + left_size_u + 1;
        int y = depth_u;

        nodes.emplace_back(x, y, W[u - 1]);
    }

    sort(nodes.begin(), nodes.end(), [](const Node& a, const Node& b) {
        return a.x < b.x;
    });

    long long max_sum = LLONG_MIN;

    for (int d1 = 1; d1 <= H; ++d1) {
        for (int d2 = d1; d2 <= H; ++d2) {
            long long current_sum = 0;
            long long best_sum = LLONG_MIN;
            for (const Node& node : nodes) {
                if (node.y < d1 || node.y > d2) {
                    continue;
                }
                if (current_sum <= 0) {
                    current_sum = node.w;
                } else {
                    current_sum += node.w;
                }
                if (current_sum > best_sum) {
                    best_sum = current_sum;
                }
            }
            if (best_sum > max_sum) {
                max_sum = best_sum;
            }
        }
    }

    cout << max_sum << endl;

    return 0;
}
```

### 설명

1. **트리 구조와 좌표**: 각 노드의 x 좌표는 in-order traversal에서의 위치에 의해 결정되며, y 좌표는 트리에서의 depth에 의해 결정된다.
2. **Depth 구간**: 각 depth 구간에 대해, 해당 depth 범위 내의 노드들을 수집하고 x 좌표를 기준으로 정렬하여 연속적인 범위를 형성한다.
3. **Kadane's Algorithm**: 이 알고리즘은 각 depth 구간에 대해 정렬된 노드 리스트 내에서 maximum sum subarray를 찾기 위해 사용되며, 이를 통해 최적의 직사각형 영역을 효율적으로 결정한다.

이 접근 방식은 perfect binary tree의 구조와 효율적인 알고리즘을 활용하여 제약 조건을 처리하며, 큰 입력에 대해서도 최적의 성능을 보장한다.

## 결론

이 문제는 트리 구조를 기하학적으로 해석하고, 다차원 데이터에서 최적의 영역을 찾는 문제로, 트리 탐색과 동적 프로그래밍 기법을 결합하여 해결할 수 있다. 시간 복잡도는 O(N^2)이며, N이 최대 262,143까지 가능하므로 효율적인 구현이 중요하다.