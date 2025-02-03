---
title: "[Algorithm] C++/Python 백준 1605번 : Non-boring sequences"
categories: 
- Algorithm
- Platinum III
- Divide and Conquer
- Segment Tree
tags:
- Divide and Conquer
- Hash Map
- Precomputation
- Time Complexity O(n log n)
- Stack
- Recursion Optimization
date: 2024-06-19
image: "index.png"
---

**연속된 부분 수열이 모두 고유한 원소를 포함하는지 판단하는 문제**

문제 : [https://www.acmicpc.net/problem/1605](https://www.acmicpc.net/problem/1605)

## 문제 설명

길이가 n인 수열이 주어졌을 때, 모든 연속된 부분 수열이 **고유한 원소**를 포함하면 "non-boring"으로 분류됩니다. 고유한 원소란 해당 부분 수열에서 단 한 번만 등장하는 원소를 의미합니다. 예를 들어 `[1, 2, 3, 2, 1]`에서 중앙의 3은 모든 부분 수열에 포함될 때 고유성을 만족시킵니다. 

이 문제의 목표는 주어진 수열이 "non-boring"인지 판단하는 것입니다. 단, n의 최대 크기는 200,000이므로 O(n²) 알고리즘은 사용할 수 없으며, 효율적인 접근 방식이 필요합니다.

## 접근 방식

1. **Precomputation**:  
   각 원소의 **이전 등장 위치(prev)**와 **다음 등장 위치(next)**를 미리 계산합니다. 이를 통해 임의의 구간 [L, R]에서 특정 원소가 고유한지 O(1) 시간에 판단할 수 있습니다.

2. **Divide and Conquer**:  
   - 현재 구간 [L, R]에서 양 끝에서 시작해 고유한 원소를 탐색합니다.
   - 고유한 원소를 찾으면 해당 위치를 기준으로 구간을 분할하여 재귀적으로 검증합니다.
   - Stack을 활용해 재귀 깊이 문제를 회피하고 반복적 분할을 수행합니다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

bool isNonBoring(const vector<int>& arr, int n) {
    vector<int> prev(n, -1); // 각 위치의 이전 등장 인덱스
    vector<int> next(n, n);  // 각 위치의 다음 등장 인덱스
    unordered_map<int, int> last;

    // prev 배열 채우기
    for (int i = 0; i < n; ++i) {
        auto it = last.find(arr[i]);
        if (it != last.end()) prev[i] = it->second;
        last[arr[i]] = i;
    }

    // next 배열 채우기
    last.clear();
    for (int i = n - 1; i >= 0; --i) {
        auto it = last.find(arr[i]);
        if (it != last.end()) next[i] = it->second;
        last[arr[i]] = i;
    }

    stack<pair<int, int>> segments; // 분할 검증할 구간 저장
    segments.push({0, n - 1});

    while (!segments.empty()) {
        auto [l, r] = segments.top();
        segments.pop();
        if (l >= r) continue;

        int a = l, b = r, pos = -1;
        while (a <= b) { // 양 끝에서 고유 원소 탐색
            if (prev[a] < l && next[a] > r) {
                pos = a;
                break;
            }
            if (prev[b] < l && next[b] > r) {
                pos = b;
                break;
            }
            a++, b--; // 좁혀가며 탐색
        }

        if (pos == -1) return false; // 고유 원소 없음

        segments.push({l, pos - 1}); // 왼쪽 구간 분할
        segments.push({pos + 1, r}); // 오른쪽 구간 분할
    }
    return true;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        vector<int> arr(n);
        for (int i = 0; i < n; ++i) cin >> arr[i];
        cout << (isNonBoring(arr, n) ? "non-boring\n" : "boring\n");
    }
}
```

## Python 코드와 설명

```python
def is_non_boring(arr):
    n = len(arr)
    prev = [-1] * n
    next = [n] * n
    last = {}

    # prev 배열 계산
    for i in range(n):
        if arr[i] in last:
            prev[i] = last[arr[i]]
        last[arr[i]] = i

    # next 배열 계산
    last = {}
    for i in range(n-1, -1, -1):
        if arr[i] in last:
            next[i] = last[arr[i]]
        last[arr[i]] = i

    stack = [(0, n-1)]
    
    while stack:
        l, r = stack.pop()
        if l >= r:
            continue
        
        pos = -1
        a, b = l, r
        while a <= b:
            if prev[a] < l and next[a] > r:
                pos = a
                break
            if prev[b] < l and next[b] > r:
                pos = b
                break
            a += 1
            b -= 1
        
        if pos == -1:
            return False
        
        stack.append((l, pos-1))
        stack.append((pos+1, r))
    
    return True

import sys
input = sys.stdin.read
data = input().split()
idx = 0
T = int(data[idx])
idx +=1
for _ in range(T):
    n = int(data[idx])
    idx +=1
    arr = list(map(int, data[idx:idx+n]))
    idx +=n
    print("non-boring" if is_non_boring(arr) else "boring")
```

## 결론

이 알고리즘은 각 분할 단계에서 고유 원소를 빠르게 찾기 위해 **양방향 탐색**을 사용하며, 평균 시간 복잡도는 O(n log n)입니다. Hash Map을 활용한 Precomputation이 핵심이며, Stack 기반 반복 분할은 재귀 제한을 우회합니다. Python 구현 시 주의할 점은 재귀 대신 Stack을 사용해야 한다는 것입니다. 추가 최적화로는 원소 빈도수를 기반으로 희소 원소를 우선 탐색하는 전략을 고려할 수 있습니다.