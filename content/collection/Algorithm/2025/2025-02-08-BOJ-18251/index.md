---
title: "[Algorithm] C++/Python 백준 18251번 내 생각에 A번인 DFS 문제가 E번이 된 사연 (Easy)"
desctiption: "백준 18251번 : 내 생각에 A번인 단순 dfs 문제가 이 대회에서 E번이 되어버린 건에 관하여 (Easy)"
categories: 
- Algorithm
- Platinum IV
- Dynamic Programming
- Graph Theory
tags:
- Dynamic Programming
- DFS
- Brute Force
- Kadane's Algorithm
- O(N log² N)
- Tree
- Graph Theory
- Sweep Line
image: "index.png"
date: 2025-02-08
---

이번 포스트에서는 백준 18251번 **"내 생각에 A번인 단순 dfs 문제가 이 대회에서 E번이 되어버린 건에 관하여 (Easy)"** 문제를 다루고자 한다. 문제는 한 눈에 보기에는 단순해 보이는 DFS 문제처럼 보이지만, 내부에는 트리의 좌표 계산, 정렬, 그리고 구간별 최대 부분합(Kadane’s Algorithm) 등 여러 알고리즘 기법이 복합적으로 쓰여 있다. 포화(Full) 이진트리의 각 노드를 평면 상에 배치한 후, 축에 평행한 직사각형 내부에 포함된 노드들의 가중치 합이 최대가 되도록 하는 문제로, 좌표계의 성질과 트리의 구조를 동시에 고려해야 하는 흥미로운 문제이다.

문제 : [https://www.acmicpc.net/problem/18251](https://www.acmicpc.net/problem/18251)

## 문제 설명

문제에서는 욱제가 종이에 **포화이진트리**를 그린 뒤, 각 노드에 정수 가중치를 부여한 상황이 주어진다. 포화이진트리란 모든 내부 노드가 두 개의 자식 노드를 가지며, 리프 노드들이 모두 같은 깊이를 갖는 이진트리이다. 노드들은 트리의 성질에 맞게 배치되는데, 각 노드는 고유한 (x, y) 좌표를 가지며 다음과 같은 조건을 만족한다.

1. 모든 노드에 대해, 왼쪽 서브트리에 속한 노드들의 x좌표는 해당 노드의 x좌표보다 작고, 오른쪽 서브트리에 속한 노드들의 x좌표는 해당 노드의 x좌표보다 크다.
2. 자식 노드의 y좌표는 부모 노드의 y좌표보다 작으며, 같은 깊이에 있는 노드들은 동일한 y좌표를 갖는다.
3. 직사각형은 축에 평행하며, 그 경계가 노드의 위치와 겹치면 안 된다. 단, 직사각형은 반드시 한 개 이상의 노드를 포함해야 한다.

문제의 입력으로는 첫 줄에 노드의 개수 N (N은 2^k - 1 꼴의 자연수, 1 ≤ N ≤ 262,143)이 주어지고, 둘째 줄에 1번 노드부터 N번 노드까지의 가중치가 공백으로 구분되어 주어진다. 노드 번호는 루트가 1번이며, i번 노드의 왼쪽 자식은 2×i, 오른쪽 자식은 2×i+1로 주어진다.

문제의 핵심은 노드들이 평면 상에 배치되는 규칙에 있다. x좌표는 트리의 구조에 따라 결정되며, 이는 각 노드가 in-order 순서에서 몇 번째에 위치하는지를 응용한 방식으로 계산된다. y좌표는 단순히 노드의 깊이를 의미한다. 욱제는 이 노드들이 가지는 좌표 정보를 활용하여, 직사각형 영역 내부에 포함되는 노드들의 가중치 합이 최대가 되는 영역을 찾고자 한다.

문제 해결의 관건은 직사각형의 y축 경계가 트리의 레벨(깊이)과 일치한다는 점이다. 즉, y좌표는 노드의 깊이에 대응되므로 직사각형의 위/아래 경계를 어떤 두 깊이 d1과 d2 (d1 ≤ d2)로 정할 수 있고, x좌표는 노드들의 in-order 순서에 따라 정렬되어 있기 때문에, 선택된 y 구간에 해당하는 노드들을 x좌표 순으로 나열한 후 연속 구간에 대해 최대 부분합(Kadane’s Algorithm) 문제로 전환할 수 있다. 이처럼 트리의 좌표 계산, 정렬, 그리고 구간 최대 합 문제를 결합한 형태로 문제를 접근할 수 있다.

## 접근 방식

문제를 해결하기 위한 전체 전략은 다음과 같다.

1. **좌표 계산:**  
   - 각 노드의 깊이(= y좌표)는 노드 번호를 이용하여 계산한다. (예를 들어, 노드 번호의 bit length를 활용할 수 있다.)  
   - x좌표는 노드가 in-order 순서에서 몇 번째 위치에 있는지를 결정하는 방식으로 계산된다.  
   - 구체적으로, 현재 노드 u에 대해, 루트로부터 내려오며 오른쪽 자식인 경우 그 조상 서브트리의 왼쪽 부분에 존재하는 노드의 수를 누적하여 x좌표에 반영한다. 그리고 u가 속한 서브트리의 왼쪽 자식 노드 개수를 추가하여 최종 x좌표를 결정한다.

2. **노드 정렬:**  
   - 계산된 각 노드의 (x, y, w) 정보를 이용하여 x좌표 기준으로 오름차순 정렬한다.  
   - 이렇게 하면, x축 방향으로 연속된 구간을 쉽게 탐색할 수 있게 된다.

3. **직사각형 후보 영역 탐색:**  
   - 직사각형의 y경계는 노드의 깊이와 일치하므로, 가능한 모든 깊이 쌍 (d1, d2)를 고려한다.
   - 각 (d1, d2) 쌍에 대해, 해당 깊이 범위에 속하는 노드들만을 대상으로 x좌표 순서대로 나열한 후, 연속된 구간에서 가중치의 합이 최대가 되는 구간을 Kadane’s Algorithm을 이용해 찾는다.
   - 모든 (d1, d2) 쌍에 대해 구한 최대 합 중 전체 최대값을 결과로 출력한다.

4. **시간 복잡도 고려:**  
   - 트리의 높이 H는 log₂(N+1)에 해당하므로, 가능한 깊이 쌍의 수는 O(H²)이다.
   - 각 쌍마다 전체 노드를 순회하게 되므로 전체 복잡도는 O(N · H²)이며, N의 최댓값과 H가 작동 가능한 범위 내에 있으므로 C++에서 충분히 빠르게 동작한다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

// Node 구조체: x좌표, y좌표(깊이), 가중치를 저장한다.
struct Node {
    int x, y, w;
    Node(int x, int y, int w) : x(x), y(y), w(w) {}
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;
    
    // 각 노드의 가중치를 입력받는다.
    vector<int> W(N);
    for (int i = 0; i < N; ++i) {
        cin >> W[i];
    }
    
    // H: 포화이진트리의 높이 계산 (N = 2^H - 1 이므로, H = log2(N+1))
    int H = 32 - __builtin_clz(N + 1) - 1;
    
    vector<Node> nodes;
    nodes.reserve(N);
    
    // 1번부터 N번 노드까지 각 노드의 (x, y) 좌표와 가중치를 계산
    for (int u = 1; u <= N; ++u) {
        // 노드 u의 깊이: bit count를 이용하여 계산 (루트의 깊이는 1)
        int depth_u = 32 - __builtin_clz(u);
        int sum_ancestors = 0;
        int current = u;
        // 루트까지 거슬러 올라가며, 오른쪽 자식인 경우 그에 따른 offset을 누적
        while (current != 1) {
            int parent = current / 2;
            if (current % 2 == 1) { // current가 오른쪽 자식인 경우
                int depth_parent = 32 - __builtin_clz(parent);
                int h_a = H - (depth_parent - 1);
                int left_size_a = (1 << (h_a - 1)) - 1;  // 부모의 왼쪽 서브트리 노드 수
                sum_ancestors += left_size_a + 1;
            }
            current = parent;
        }
        
        // 현재 노드 u가 속한 서브트리에서 왼쪽 부분의 노드 개수
        int h_u = H - (depth_u - 1);
        int left_size_u = (1 << (h_u - 1)) - 1;
        // x좌표는 조상에서 누적된 offset과 현재 서브트리 내 왼쪽 노드 수를 합산하여 결정
        int x = sum_ancestors + left_size_u + 1;
        int y = depth_u;  // y좌표는 노드의 깊이
        nodes.emplace_back(x, y, W[u - 1]);
    }
    
    // x좌표 기준으로 노드를 정렬하여, x축 상의 연속 구간 탐색을 용이하게 함
    sort(nodes.begin(), nodes.end(), [](const Node& a, const Node& b) {
        return a.x < b.x;
    });
    
    long long max_sum = LLONG_MIN;
    
    // 가능한 모든 y좌표 구간 (d1 ~ d2)을 고려
    for (int d1 = 1; d1 <= H; ++d1) {
        for (int d2 = d1; d2 <= H; ++d2) {
            long long current_sum = 0;
            long long best_sum = LLONG_MIN;
            // x좌표 순으로 정렬된 노드들 중, 깊이가 [d1, d2]에 해당하는 노드에 대해 Kadane’s Algorithm 적용
            for (const Node& node : nodes) {
                if (node.y < d1 || node.y > d2) continue;  // 현재 y구간에 포함되지 않는 노드 건너뛰기
                // current_sum가 음수이면 새 구간 시작, 그렇지 않으면 현재 노드의 가중치를 더함
                current_sum = (current_sum <= 0 ? node.w : current_sum + node.w);
                best_sum = max(best_sum, current_sum);
            }
            max_sum = max(max_sum, best_sum);
        }
    }
    
    cout << max_sum << "\n";
    
    return 0;
}
```

## 코드 동작 설명 (C++)


1. **입력 및 초기화:**  
   - 노드 개수 N과 각 노드의 가중치를 입력받는다.
   - 트리의 높이 H를 `H = log2(N+1)`로 계산한다.

2. **좌표 계산:**  
   - 각 노드 u에 대해, u의 깊이(depth_u)와 조상 노드들을 거슬러 올라가며 오른쪽 자식인 경우 해당 서브트리의 왼쪽 노드 개수를 누적하여 x좌표를 산출한다.
   - u가 속한 서브트리 내 왼쪽 부분의 노드 수를 더하여 최종 x좌표를 결정하고, y좌표는 depth_u로 설정한다.

3. **정렬:**  
   - 모든 노드를 x좌표 기준 오름차순으로 정렬한다.

4. **최대 가중치 합 계산:**  
   - 가능한 모든 y좌표 구간 (d1, d2)를 이중 반복문으로 탐색한다.
   - 각 구간에 대해, 정렬된 노드들 중 해당 구간에 포함되는 노드들의 가중치를 순회하며 Kadane’s Algorithm을 적용하여 최대 연속 합을 구한다.
   - 모든 구간에서 얻은 최대 합 중 가장 큰 값을 결과로 출력한다.

## Python 코드와 설명

```python
import sys
import math

def main():
    input = sys.stdin.readline
    N = int(input())
    weights = list(map(int, input().split()))
    
    # 트리의 높이 H를 계산 (N = 2^H - 1 이므로 H = log2(N+1))
    H = math.floor(math.log2(N + 1))
    
    nodes = []
    # 1번부터 N번 노드까지 (x, y, 가중치) 정보를 계산
    for u in range(1, N + 1):
        # 노드의 깊이: bit_length()를 사용 (루트의 깊이는 1)
        depth_u = u.bit_length()
        sum_ancestors = 0
        current = u
        # 루트까지 거슬러 올라가며, 오른쪽 자식인 경우 조상 서브트리의 왼쪽 노드 개수를 누적
        while current != 1:
            parent = current // 2
            if current % 2 == 1:  # current가 오른쪽 자식이면
                depth_parent = parent.bit_length()
                h_a = H - (depth_parent - 1)
                left_size_a = (1 << (h_a - 1)) - 1
                sum_ancestors += left_size_a + 1
            current //= 2
        
        # 현재 노드가 속한 서브트리에서 왼쪽에 있는 노드 수를 계산
        h_u = H - (depth_u - 1)
        left_size_u = (1 << (h_u - 1)) - 1
        x = sum_ancestors + left_size_u + 1  # x좌표 계산
        y = depth_u  # y좌표는 노드의 깊이
        nodes.append((x, y, weights[u - 1]))
    
    # x좌표 기준으로 노드를 정렬
    nodes.sort(key=lambda node: node[0])
    
    max_sum = -10**18  # 매우 작은 초기값 설정
    # 가능한 모든 y구간 (d1 ~ d2)에 대해 탐색
    for d1 in range(1, H + 1):
        for d2 in range(d1, H + 1):
            current_sum = 0
            best_sum = -10**18
            # x좌표 순서대로, 깊이가 [d1, d2] 범위에 속하는 노드들에 대해 Kadane’s Algorithm 적용
            for x, y, w in nodes:
                if y < d1 or y > d2:
                    continue  # 해당 y구간에 포함되지 않으면 건너뛴다.
                current_sum = w if current_sum <= 0 else current_sum + w
                best_sum = max(best_sum, current_sum)
            max_sum = max(max_sum, best_sum)
    
    print(max_sum)

if __name__ == '__main__':
    main()
```

 ## 코드 동작 설명 (Python)

1. **입력 및 트리 높이 계산:**  
   - `sys.stdin.readline`을 통해 노드 개수 N과 각 노드의 가중치를 입력받는다.
   - N을 이용해 트리의 높이 H를 `log2(N+1)`로 계산한다.

2. **노드 좌표 계산:**  
   - 각 노드 u에 대해, u의 깊이(= y좌표)를 `u.bit_length()`로 구한다.
   - 루트부터 u까지 거슬러 올라가면서, 현재 노드가 오른쪽 자식일 경우 조상 서브트리의 왼쪽 노드 개수를 누적하여 x좌표에 반영한다.
   - u가 속한 서브트리의 왼쪽 노드 개수를 추가해 최종 x좌표를 산출한다.

3. **정렬 및 최대 부분합 계산:**  
   - 모든 노드를 x좌표 기준으로 정렬한 후, 가능한 모든 y구간 (d1, d2)에 대해 노드를 순회한다.
   - 각 구간에 대해 Kadane’s Algorithm을 적용하여 연속된 노드들의 가중치 합의 최대값을 찾는다.
   - 전체 구간 중 최대 합을 최종 결과로 출력한다.

## 결론

이 문제는 단순해 보이는 DFS 문제처럼 시작되었으나, **트리의 좌표 계산**과 **직사각형 영역**이라는 기하학적 성질, 그리고 **최대 부분합 문제(Kadane’s Algorithm)**가 결합되어 있는 다층적인 문제이다.  
문제 해결의 핵심은 노드의 x좌표를 올바르게 계산하고, y좌표 구간을 고정한 뒤 x축 상의 연속 구간에 대해 최대 합을 효율적으로 구하는 것이다. C++의 경우 빠른 입출력과 비트 조작을 통해 효율적으로 구현할 수 있으며, Python 역시 같은 로직으로 구현 가능하나 N의 크기와 반복문의 횟수를 고려하면 PyPy나 추가 최적화가 필요할 수 있다.  
이와 같이 여러 알고리즘 기법을 복합적으로 적용하는 문제는 기본 알고리즘에 익숙해진 후 응용력과 문제해결 능력을 기르는 데 큰 도움이 된다.
