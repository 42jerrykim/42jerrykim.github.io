---
title: "[Algorithm] C++/Python 백준 15773번: Touch The Sky"
description: "고도 h≤L에서만 풍선을 불 수 있고 한 번 불 때마다 D만큼 상승한다. 최대 몇 개의 풍선을 순서대로 사용할 수 있는지 구한다. E=L+D 오름차순 정렬 + 최대 힙으로 누적 D를 관리하며, 누적이 현재 E를 초과하면 가장 큰 D를 제거한다. 교환 논법으로 그리디 정당화, O(N log N), 64비트 정수 주의."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Greedy
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-15773
- cpp
- python
- C++
- Python
- Greedy
- 그리디
- Priority Queue
- 우선순위큐
- Heap
- 힙
- Sorting
- 정렬
- Scheduling
- 스케줄링
- Deadline
- 데드라인
- Earliest Finish Time
- 조기완료정렬
- L+D Trick
- L+D 정렬
- Proof of Correctness
- 정당성 증명
- Exchange Argument
- 교환 논법
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Implementation
- 구현
- Implementation Details
- 구현 디테일
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Big Integer
- 64비트정수
- Long Long
- 자료구조
- Data Structures
- Binary Heap
- 이진 힙
- Admissible Order
- 허용 순서
- Constructive Proof
- 구성적 증명
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Template
- 템플릿
- Testing
- 테스트
- Invariant
- 불변식
- Math
- 수학
- Greedy Scheduling
- 그리디 스케줄링
- Touch The Sky
- Balloon
- 풍선
- Constraint Satisfaction
- 제약충족
- Algorithm Design
- 알고리즘 설계
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/15773
- 요약: 고도 `h`가 풍선 `i`의 제한 `L_i` 이하일 때만 해당 풍선을 불 수 있고, 불면 고도가 `D_i`만큼 즉시 증가한다. 한 번에 하나씩 순차적으로 진행할 때, 터뜨릴 수 있는 풍선의 최대 개수를 구한다.

### 제한/스펙
- `1 ≤ N ≤ 250,000`
- `0 ≤ L_i ≤ 1e15`, `1 ≤ D_i ≤ 1e9`
- 시간 제한 1초, 메모리 1GB → `O(N log N)` 풀이 필요, 누적합은 64비트 정수 사용

## 입출력 형식/예제

예제 입력 1
```
3
1 4
1 5
9 2
```

예제 출력 1
```
2
```

예제 입력 2
```
4
0 1
0 2
0 3
0 4
```

예제 출력 2
```
1
```

## 접근 개요(아이디어 스케치)
- 관찰: 어떤 시점의 고도 `h`는 지금까지 사용한 풍선들의 `D` 합이다. 풍선 `i`를 사용할 수 있는 필요충분조건은 사용 직전 `h ≤ L_i`.
- 핵심 트릭: 각 풍선에 대해 `E_i = L_i + D_i` 를 정의하고 `E` 오름차순으로 본다. 이 순서의 접두집합에서 선택한 풍선들의 `D` 누적합이 항상 현재 `E`를 넘지 않게 유지하면, 선택 집합을 어떤 순서로든 실제로 수행할 수 있다.
- 그리디: `E` 오름차순으로 순회하며 `D`를 최대 힙에 넣고 누적합 `S`를 더한다. `S > E`가 되면 가장 큰 `D` 하나를 제거하여 `S`를 줄인다. 이렇게 하면 같은 접두집합에서 가능한 한 많은 개수를 유지한다.
- 정당성(교환 논법 요지): 현재 접두집합에서 누적합이 `E`를 넘을 때 제거할 항목으로 가장 큰 `D`를 빼면, 이후 어떤 `E`에 대해서도 제약을 더 느슨하게 만들어(또는 같게 유지하여) 향후 선택 가능성을 최대화한다. 따라서 선택 개수를 최대로 하는 전략이다.

```mermaid
graph TD
  A[입력 N, (L_i, D_i)] --> B[E_i = L_i + D_i 계산]
  B --> C[E 오름차순 정렬]
  C --> D{다음 풍선}
  D -->|push D_i, S+=D_i| E[최대 힙 유지]
  E --> F{S > E_i?}
  F -->|Yes| G[힙에서 가장 큰 D 제거, S-=max]
  F -->|No| H[유지]
  G --> D
  H --> D
```

## 알고리즘 설계
- 상태: 누적 상승량 `S`, 최대 힙 `PQ`(선택한 풍선들의 `D` 저장)
- 절차:
  1) 모든 풍선에 대해 `E=L+D`를 계산하고 `E` 오름차순으로 정렬
  2) 각 원소를 순회하며 `D`를 `PQ`에 넣고 `S += D`
  3) `S > E`이면 `PQ`에서 가장 큰 `D`를 꺼내 `S`에서 빼기
  4) 순회 종료 시 `PQ` 크기가 사용할 수 있는 최대 개수
- 올바름 근거: 접두집합에서 `S ≤ 현재 E` 불변식을 유지. 위반 시 가장 큰 `D` 제거가 이후 모든 `E`에 가장 유리. 선택 집합에 대해 실제 수행 순서는 “사용 직전 고도 ≤ L”을 만족하도록 구성 가능.

## 복잡도
- 시간: 정렬 `O(N log N)` + 힙 연산 `O(N log N)` → 전체 `O(N log N)`
- 공간: 힙 `O(N)`

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; if(!(cin >> N)) return 0;
    vector<pair<long long,long long>> a; a.reserve(N);
    for(int i=0;i<N;++i){
        long long L,D; cin >> L >> D;
        a.emplace_back(L + D, D); // (E, D)
    }

    sort(a.begin(), a.end()); // by E asc

    priority_queue<long long> pq; // store D (max-heap)
    long long sumD = 0;
    for(const auto &p : a){
        long long E = p.first, D = p.second;
        pq.push(D);
        sumD += D;
        if(sumD > E){
            sumD -= pq.top();
            pq.pop();
        }
    }

    cout << (int)pq.size() << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
import heapq

def solve() -> None:
    data = sys.stdin.read().strip().split()
    it = iter(data)
    try:
        n = int(next(it))
    except StopIteration:
        return

    balloons = []  # (E, D)
    for _ in range(n):
        L = int(next(it)); D = int(next(it))
        balloons.append((L + D, D))

    balloons.sort()  # by E asc

    max_heap = []  # store -D to simulate max-heap
    sum_d = 0
    for E, D in balloons:
        heapq.heappush(max_heap, -D)
        sum_d += D
        if sum_d > E:
            largest = -heapq.heappop(max_heap)
            sum_d -= largest

    print(len(max_heap))

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- `L_i = 0`만 있는 경우: 첫 풍선만 가능 → 최대 1
- 매우 큰 `L_i`(최대 `1e15`)와 큰 `D_i`(최대 `1e9`) 혼재: `sumD`는 64비트(`long long`) 필요
- 같은 `E`가 다수: 정렬 안정성에 영향 없음(임의 순서 가능)
- `N`이 큰 케이스(25만): 입출력 가속(빠른 IO), `O(N log N)` 구현 필수
- 모든 풍선을 선택 가능한 경우: 힙 크기 `N`
- 한 개도 선택 불가한 구성: 답 `0`

## 제출 전 점검
- 64비트 정수 사용 여부(`long long`)
- 힙에서 제거 시 누적합 업데이트 정확성
- 입력 파싱/개행 처리, 빠른 입출력 설정
- 정렬 키가 `E=L+D`가 맞는지 재확인

## 참고자료/유사문제
- 데드라인 기반 작업 최대 개수 그리디(접두집합 누적시간 ≤ 데드라인, 위반 시 가장 긴 작업 제거)와 동일한 증명 틀을 사용. 여기서는 시작 제약을 `E=L+D`로 치환하여 적용.


