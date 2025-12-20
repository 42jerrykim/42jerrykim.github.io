---
title: "[Algorithm] C++/Python 백준 2336번 : 굉장한 학생"
description: "백준 2336번 '굉장한 학생' 문제는 세 번의 시험 성적이 주어졌을 때, 세 시험 모두에서 다른 어떤 학생에게도 뒤처지지 않는 '굉장한 학생'의 수를 효율적으로 계산하는 알고리즘과 자료구조 구현법을 설명한다."
categories: 
- Algorithm
- Platinum II
- Data Structures
- Binary Indexed Tree
tags:
- Fenwick Tree
- Greedy
- O(N log N)
- Binary Indexed Tree
- Competitive Programming
- Implementation
image: "index.png"
date: 2025-02-03
---

본 글에서는 백준 문제 [2336번: 굉장한 학생](https://www.acmicpc.net/problem/2336)에 대해 상세하게 설명하고 풀이 과정을 소개하고자 한다. 세 번의 시험에서 학생들의 순위가 주어졌을 때, 모든 시험에서 다른 학생보다 우월한 학생이 존재하지 않는 학생을 '굉장한 학생'이라 정의하는 본 문제는, 단순한 구현 문제로 보일 수 있으나 N이 최대 500,000까지 가능하므로 효율적인 자료 구조와 알고리즘을 필요로 한다. 특히, 첫 번째 시험 순위 기준으로 정렬한 뒤 Fenwick Tree(또는 Binary Indexed Tree)를 활용하여 두 번째와 세 번째 시험의 성적을 효과적으로 관리하는 방식이 핵심이다. 본 글에서는 C++과 Python 두 가지 언어로 최적화된 코드를 제시하고, 각 코드의 세부 동작 원리를 상세하게 분석할 것이다.

## 문제 설명

N명의 학생이 참여하여 세 번의 시험을 치른다. 모든 학생은 세 번의 시험에 응시하며, 각 시험에서는 동일한 등수를 가진 학생이 단 한 명도 없도록 순위가 매겨진다. 여기서 학생 A가 학생 B보다 세 번의 시험 모두에서 더 좋은 성적을 거두었다면, A는 B보다 '대단하다'고 정의된다. 반대로, 자신보다 '대단한' 학생이 존재하지 않는 학생을 '굉장한 학생'이라고 부른다. 문제의 목표는 주어진 세 시험의 순위 정보를 바탕으로 '굉장한 학생'의 총 수를 계산하는 것이다.  
문제의 입력은 첫 줄에 학생 수 N이 주어지며, 이후 세 개의 줄에 걸쳐 각 시험의 등수 순서대로 학생 번호가 주어진다. 예를 들어, 첫 번째 시험에서는 1등부터 N등까지 학생 번호가 주어지고, 마찬가지로 두 번째와 세 번째 시험에 대한 정보가 순서대로 주어진다.  
학생의 번호는 1부터 N까지 매겨지며, 각 시험의 결과는 서로 다른 순위를 보장한다. 문제를 해결하기 위해서는 세 시험의 결과를 어떻게 효율적으로 비교할 수 있을지, 그리고 특정 학생보다 더 좋은 성적을 가진 학생이 존재하는지 여부를 빠르게 판단할 수 있는 자료 구조를 설계하는 것이 중요하다.  
이 문제는 N이 최대 500,000까지 가능하기 때문에 단순한 중첩 반복문(Brute Force) 방식으로는 시간 초과가 발생할 수 있다. 따라서, 첫 번째 시험을 기준으로 학생들을 순회하며, 이미 처리된 학생들 중 두 번째 시험과 세 번째 시험의 정보를 Fenwick Tree를 이용하여 관리하고, 현재 학생보다 좋은 순위(작은 값)를 가진 학생들의 최소 세 번째 시험 성적을 빠르게 조회하는 방법을 사용한다. 이를 통해 각 학생에 대해 O(log N)의 시간 내에 비교를 수행할 수 있으며, 전체 알고리즘은 O(N log N)의 시간 복잡도를 갖게 된다.

## 접근 방식

문제를 효율적으로 해결하기 위해 다음과 같은 전략을 사용한다.  
1. **첫 번째 시험 기준 정렬**: 세 번의 시험 중 첫 번째 시험 결과를 기준으로 학생들을 정렬한다. 첫 번째 시험에서 높은 순위를 가진 학생들은 이미 처리되었으므로, 이들을 활용하여 나중에 처리될 학생과의 비교가 용이하다.  
2. **Fenwick Tree 활용**: 두 번째 시험 순위를 인덱스로 사용하여, 현재까지 처리된 학생들 중 각 구간의 최소 세 번째 시험 순위를 관리한다. 이를 통해, 현재 학생보다 두 번째 시험에서 더 좋은 성적을 가진 학생들 중에서 세 번째 시험 성적이 가장 낮은(즉, 좋은) 값을 빠르게 조회할 수 있다.  
3. **비교 및 업데이트**: 현재 학생의 두 번째 시험 순위보다 좋은 학생들(인덱스 1부터 r2-1)의 최소 세 번째 시험 순위를 조회한 후, 이 값이 현재 학생의 세 번째 시험 순위보다 작은 경우, 이미 어떤 학생이 모든 시험에서 우위에 있음을 의미한다. 그렇지 않은 경우 해당 학생은 '굉장한 학생'으로 카운트되며, Fenwick Tree에 현재 학생의 세 번째 시험 성적을 업데이트한다.

이와 같이 Fenwick Tree를 사용하면 각 업데이트와 쿼리에 O(log N) 시간이 소요되어 전체 알고리즘은 O(N log N)의 시간 복잡도를 갖게 된다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;

// 학생 정보를 저장하는 구조체
struct Student {
    int id;   // 학생 번호
    int r1, r2, r3;  // 각각 첫 번째, 두 번째, 세 번째 시험 순위
};

// Fenwick Tree (Binary Indexed Tree)를 구현하여 구간 내 최소값을 관리한다.
struct Fenw {
    int n;
    vector<int> tree;
    
    // 생성자: n 크기의 트리를 초기값(INT_MAX)으로 초기화
    Fenw(int n) : n(n), tree(n + 1, INT_MAX) {}
    
    // update 함수: index i부터 n까지 최소값을 갱신
    void update(int i, int val) {
        for (; i <= n; i += i & -i)
            tree[i] = min(tree[i], val);
    }
    
    // query 함수: 1부터 i까지의 구간에서 최소값을 반환
    int query(int i) {
        int res = INT_MAX;
        for (; i > 0; i -= i & -i)
            res = min(res, tree[i]);
        return res;
    }
};

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N;
    cin >> N;
    
    // 학생 번호는 1부터 N까지, 각 학생의 시험 결과를 저장할 배열
    vector<Student> students(N + 1);
    
    // 첫 번째 시험 순위 입력 처리
    for (int i = 1; i <= N; i++){
        int id;
        cin >> id;
        students[id].id = id;
        students[id].r1 = i; // i번째 입력은 i등
    }
    
    // 두 번째 시험 순위 입력 처리
    for (int i = 1; i <= N; i++){
        int id;
        cin >> id;
        students[id].r2 = i;
    }
    
    // 세 번째 시험 순위 입력 처리
    for (int i = 1; i <= N; i++){
        int id;
        cin >> id;
        students[id].r3 = i;
    }
    
    // 첫 번째 시험 순위를 기준으로 학생들을 정렬
    vector<Student> arr;
    arr.reserve(N);
    for (int id = 1; id <= N; id++){
        arr.push_back(students[id]);
    }
    sort(arr.begin(), arr.end(), [](const Student &a, const Student &b){
        return a.r1 < b.r1;
    });
    
    // Fenwick Tree 초기화: 두 번째 시험의 순위 범위를 인덱스로 사용
    Fenw fenw(N);
    
    int cntGreat = 0;  // 굉장한 학생 수를 카운트하는 변수
    
    // 첫 번째 시험 순위가 좋은 순서대로 학생들을 처리
    for (auto &st : arr) {
        // 현재 학생의 두 번째 시험 순위보다 더 좋은 학생들(인덱스 1부터 r2-1)의 최소 세 번째 시험 순위를 조회
        int bestThird = fenw.query(st.r2 - 1);
        
        // 만약 조회된 최소 세 번째 시험 순위가 현재 학생의 r3보다 큰 경우,
        // 현재까지 처리된 학생들 중 어떤 학생도 모든 시험에서 현재 학생을 능가하지 않았음을 의미한다.
        if (bestThird > st.r3) {
            cntGreat++;  // 굉장한 학생으로 카운트
        }
        // 현재 학생의 세 번째 시험 순위를 Fenwick Tree에 업데이트
        fenw.update(st.r2, st.r3);
    }
    
    cout << cntGreat << "\n";
    return 0;
}
```

### C++ 코드 동작 설명

1. **입력 처리**  
   - 세 번의 시험 결과를 각각 읽어 학생의 구조체 변수에 저장한다. 첫 번째 시험에서는 입력 순서대로 i등을 부여한다.

2. **정렬**  
   - 첫 번째 시험 결과를 기준으로 학생들을 오름차순 정렬한다. 이로써 앞서 처리한 학생들은 모두 첫 번째 시험에서 우위에 있다.

3. **Fenwick Tree 초기화 및 쿼리**  
   - Fenwick Tree를 두 번째 시험의 순위를 인덱스로 초기화한 후, 현재 학생보다 좋은 두 번째 시험 순위를 가진 학생들의 구간 내 최소 세 번째 시험 순위를 조회한다.

4. **조건 비교 및 업데이트**  
   - 만약 조회된 최소 세 번째 시험 순위가 현재 학생의 r3보다 크다면, 현재 학생은 '굉장한 학생'으로 카운트된다. 이후, Fenwick Tree를 현재 학생의 두 번째 시험 순위 위치에서 세 번째 시험 순위를 업데이트한다.

5. **결과 출력**  
   - 굉장한 학생의 총 수를 출력한다.

## Python 코드와 설명

```python
import sys
import math

# 빠른 입력을 위한 sys.stdin.readline 사용
input = sys.stdin.readline
INT_MAX = 10**9

# Fenwick Tree (Binary Indexed Tree) 클래스 구현
class Fenw:
    def __init__(self, n):
        self.n = n
        self.tree = [INT_MAX] * (n + 1)
    
    # update 함수: index i부터 n까지 최소값을 갱신
    def update(self, i, val):
        while i <= self.n:
            self.tree[i] = min(self.tree[i], val)
            i += i & -i
    
    # query 함수: 1부터 i까지의 구간에서 최소값을 반환
    def query(self, i):
        res = INT_MAX
        while i > 0:
            res = min(res, self.tree[i])
            i -= i & -i
        return res

def main():
    N = int(input())
    
    # 학생의 시험 결과를 저장할 리스트. index 0은 사용하지 않음.
    students = [[0, 0, 0] for _ in range(N + 1)]
    
    # 첫 번째 시험 순위 입력 처리
    order = list(map(int, input().split()))
    for i, id in enumerate(order, start=1):
        students[id][0] = i  # 첫 번째 시험 순위
    
    # 두 번째 시험 순위 입력 처리
    order = list(map(int, input().split()))
    for i, id in enumerate(order, start=1):
        students[id][1] = i  # 두 번째 시험 순위
    
    # 세 번째 시험 순위 입력 처리
    order = list(map(int, input().split()))
    for i, id in enumerate(order, start=1):
        students[id][2] = i  # 세 번째 시험 순위
    
    # 첫 번째 시험 순위를 기준으로 학생 번호를 정렬
    arr = []
    for id in range(1, N + 1):
        # 각 원소는 (r1, r2, r3, id)의 튜플이다.
        arr.append((students[id][0], students[id][1], students[id][2], id))
    arr.sort(key=lambda x: x[0])
    
    fenw = Fenw(N)  # Fenwick Tree 초기화 (두 번째 시험 순위 범위 사용)
    cntGreat = 0  # 굉장한 학생 수 카운트
    
    # 첫 번째 시험 순위 순으로 학생들을 처리
    for r1, r2, r3, id in arr:
        # 현재 학생보다 두 번째 시험에서 좋은 학생들의 최소 세 번째 시험 순위를 조회
        bestThird = fenw.query(r2 - 1)
        
        # 조회 결과가 현재 학생의 r3보다 크면, 굉장한 학생임
        if bestThird > r3:
            cntGreat += 1
        # Fenwick Tree에 현재 학생의 r3를 업데이트
        fenw.update(r2, r3)
    
    sys.stdout.write(str(cntGreat) + "\n")

if __name__ == "__main__":
    main()
```

### Python 코드 동작 설명

1. **입력 처리**  
   - `sys.stdin.readline`을 사용하여 빠르게 입력을 받는다. 각 시험 결과를 읽어 학생별로 첫 번째, 두 번째, 세 번째 시험 순위를 저장한다.

2. **정렬**  
   - 첫 번째 시험 결과를 기준으로 학생들을 정렬한다. 각 학생은 (r1, r2, r3, id) 형태의 튜플로 저장된다.

3. **Fenwick Tree 초기화 및 쿼리**  
   - Fenw 클래스 인스턴스를 생성하여 두 번째 시험 순위를 인덱스로 사용한다.  
   - 현재 학생의 두 번째 시험 순위보다 좋은 학생들의 최소 세 번째 시험 순위를 query() 함수를 통해 조회한다.

4. **조건 비교 및 업데이트**  
   - 만약 조회된 최소 세 번째 시험 순위가 현재 학생의 r3보다 큰 경우 굉장한 학생으로 판단하여 카운트를 증가시킨다.  
   - 이후 update() 함수를 통해 현재 학생의 세 번째 시험 순위를 Fenwick Tree에 반영한다.

5. **결과 출력**  
   - 굉장한 학생의 총 수를 출력한다.

## 결론

본 문제는 단순해 보이는 구현 문제이나, N의 크기가 매우 클 수 있다는 점에서 효율적인 자료 구조 선택이 핵심이다. Fenwick Tree를 사용하여 두 번째 시험의 순위를 인덱스로 관리함으로써 각 학생에 대해 빠른 쿼리와 업데이트가 가능하게 되었으며, 결과적으로 전체 알고리즘은 O(N log N) 시간 복잡도로 해결할 수 있었다. 또한, C++과 Python 두 가지 언어로 구현하여 다양한 환경에서 문제 해결이 가능함을 보였다. 앞으로도 이러한 문제에서 자료 구조의 선택과 효율적인 알고리즘 설계가 얼마나 중요한지 다시 한번 느낄 수 있었으며, 다른 최적화 기법이나 자료 구조(예: Segment Tree)를 적용해볼 수도 있음을 생각해보게 되었다.
```