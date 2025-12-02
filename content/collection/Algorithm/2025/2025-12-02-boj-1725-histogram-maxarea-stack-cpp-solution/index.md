---
title: "[Algorithm] cpp 백준 1725번: 히스토그램"
description: "히스토그램에서 최대 넓이 직사각형을 찾는 고전 문제입니다. 스택을 활용한 선형 시간 알고리즘으로 O(n) 복잡도를 달성하며, 좌우 경계 확장 개념과 엣지 케이스 처리를 완벽히 정리했습니다."
date: 2025-12-02
lastmod: 2025-12-02
categories:
- Algorithm
- Stack
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-1725
- cpp
- C++
- Stack
- 스택
- Data Structures
- 자료구조
- Histogram
- 히스토그램
- Maximum Rectangle
- 최대직사각형
- Maximal Area
- 최대 넓이
- Greedy
- 그리디
- Linear Time
- 선형시간
- O(n)
- Monotonic Stack
- 단조스택
- Problem Solving
- 문제 해결
- Competitive Programming
- 경쟁프로그래밍
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Implementation
- 구현
- Pitfalls
- 실수 포인트
- Boundary Extension
- 경계 확장
- Height Array
- 높이 배열
- Width Calculation
- 너비 계산
- Optimization
- 최적화
- Classic Problem
- 고전 문제
- Stack-based Algorithm
- 스택기반 알고리즘
- Two Pointers Concept
- 투포인터 개념
- Nested Loops
- 중첩 루프
- Brute Force Alternative
- 완전탐색 대안
- Fast I/O
- 빠른 입출력
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- University Contest
- 대학 대회
image: "wordcloud.png"
---

## 문제 정보

- **문제**: https://www.acmicpc.net/problem/1725
- **요약**: 히스토그램의 각 칸 높이가 주어질 때, 히스토그램 내부에 그릴 수 있는 가장 넓이가 큰 직사각형의 넓이를 구합니다. 직사각형의 밑변은 항상 히스토그램의 아래쪽과 평행합니다.
- **제한**: N ≤ 100,000, 각 높이 ≤ 1,000,000,000, 시간 0.7초, 메모리 128MB

## 입출력 형식/예제

```text
입력 예시
7
2
1
4
5
1
3
3

출력 예시
8
```

**설명**: 높이 배열 [2, 1, 4, 5, 1, 3, 3]에서 높이 4 또는 5인 위치의 인접한 2개 칸이 만드는 너비 2, 높이 4의 직사각형(넓이 8)이 최대입니다.

## 접근 개요(아이디어 스케치)

- **핵심 관찰**: 각 막대를 높이로 삼아 만들 수 있는 직사각형을 고려할 때, 좌우로 확장하며 그 높이를 유지할 수 있는 최대 범위를 찾아야 합니다.
- **완전 탐색의 한계**: 모든 쌍(i, j)에 대해 최소 높이를 계산하면 O(n²) 또는 O(n²) 쿼리가 필요합니다.
- **스택 활용**: 단조 스택을 유지하면서 현재 높이보다 높은 이전 막대들을 pop하고, pop할 때마다 그 막대를 기준으로 만들 수 있는 최대 직사각형을 계산합니다.
- **선형 시간**: 각 막대는 정확히 1회 push, 1회 pop되므로 O(n)에 해결 가능합니다.

## 알고리즘 설계

### 상태 및 전이

**스택의 역할**: 인덱스를 저장하는 단조 증가 스택
- 스택에는 높이가 증가 또는 같은 순서로 막대의 인덱스가 저장됩니다.
- 현재 막대 높이가 스택 top의 높이보다 낮으면, top을 pop하고 직사각형 계산합니다.

**직사각형 계산 (pop 시)**:
```
높이 = arr[스택.top()]
너비 = 현재 인덱스 - (새로운 스택.top() + 1)
       또는 (스택이 비면) 현재 인덱스
넓이 = 높이 × 너비
```

**스택이 비는 경우**:
- 스택이 비면, 현재 위치 앞의 모든 칸이 해당 높이 이상입니다.
- 너비 = 현재 인덱스

**루프 종료 후**:
- 스택에 남은 원소들을 모두 pop하면서 직사각형을 계산합니다.
- 이때 오른쪽 경계는 배열 끝(n)입니다.

### 올바름 근거

1. **각 막대당 1회 계산**: 모든 막대는 정확히 한 번만 스택에서 pop되며, 그때 최대 확장 범위를 계산합니다.
2. **최대 범위 보장**: pop할 때 좌측 경계는 스택의 새로운 top(또는 시작), 우측 경계는 현재 위치입니다. 이 범위 내에서는 해당 높이 이상의 모든 막대가 포함됩니다.
3. **전역 최적성**: 모든 가능한 높이와 범위 조합이 정확히 1회씩 검사되므로, 최댓값을 놓칠 수 없습니다.

## 복잡도

- **시간**: O(n) - 각 인덱스는 1회 push, 1회 pop
- **공간**: O(n) - 스택 저장 공간

## 구현 (C++)

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <iostream>
#include <stack>
#include <algorithm>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    
    long long arr[100001];
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }
    
    stack<int> st;
    long long maxArea = 0;
    
    // 각 위치에서 현재 높이보다 높은 이전 막대들을 처리
    for (int i = 0; i < n; i++) {
        while (!st.empty() && arr[st.top()] > arr[i]) {
            int height = arr[st.top()];
            st.pop();
            
            // 너비 계산: 스택의 새로운 top(또는 시작)부터 현재 위치 직전까지
            int width = st.empty() ? i : i - st.top() - 1;
            maxArea = max(maxArea, (long long)height * width);
        }
        st.push(i);
    }
    
    // 스택에 남은 막대들 처리 (오른쪽 끝까지 확장 가능)
    while (!st.empty()) {
        int height = arr[st.top()];
        st.pop();
        
        int width = st.empty() ? n : n - st.top() - 1;
        maxArea = max(maxArea, (long long)height * width);
    }
    
    cout << maxArea << '\n';
    
    return 0;
}
```

**코드 설명**

1. **입력 파싱**:
   - n과 n개의 높이값을 배열에 저장합니다.
   - 높이가 최대 10억이므로 `long long` 사용합니다.

2. **단조 스택 유지**:
   - 각 위치 i에서, 스택 top의 높이가 현재 높이보다 크면 pop합니다.
   - Pop하면서 그 막대를 기준으로 직사각형을 계산합니다.

3. **너비 계산**:
   - 스택이 비어있으면: 왼쪽 끝부터 i-1까지 → 너비 = i
   - 스택이 있으면: 스택 top 직후부터 i-1까지 → 너비 = i - st.top() - 1

4. **최종 처리**:
   - 루프 종료 후 스택에 남은 원소들은 오른쪽 끝까지 확장 가능합니다.
   - 너비 = n (오른쪽 끝) 또는 n - st.top() - 1

5. **오버플로우 방지**:
   - 높이가 최대 10억, 너비도 최대 10만이므로 곱하면 최대 10^14
   - `long long`으로 충분합니다.

## 코너 케이스 체크리스트

- **모두 같은 높이**: n × height 계산되는지 확인
- **단조 증가 배열**: 마지막 원소가 가장 넓은 직사각형 후보인지 확인
- **단조 감소 배열**: 첫 번째 원소가 n 너비로 계산되는지 확인
- **높이 1개**: 그 값 × 1 또는 그 값 × n 출력
- **높이가 0인 칸**: 0 높이로 계산되므로 넓이는 0
- **n=1, height=10^9**: 10^9 출력
- **n=10만, 모두 10^9**: 10^14 오버플로우 체크

## 제출 전 점검

- Fast I/O 설정 (`ios_base::sync_with_stdio(false)`, `cin.tie(NULL)`) 확인
- 스택 연산 정확성 (pop 전 empty 체크, 인덱스 범위)
- 너비 계산: `i - st.top() - 1` vs `i` 구분 확인
- `long long` 사용으로 오버플로우 방지
- 최종 루프에서도 정확한 너비 계산 (n - st.top() - 1)
- 개행 문자 처리

## 참고자료/유사문제

- **문제**: https://www.acmicpc.net/problem/1725
- **출처**: University of Ulm Local Contest 2003
- **유사 알고리즘**: 단조 스택, 그리디, 분할 정복 (다른 풀이)
- **관련 문제**:
  - [LeetCode 84: Largest Rectangle in Histogram (동일 문제, 영문)](https://leetcode.com/problems/largest-rectangle-in-histogram/description/)
  - 분할 정복으로도 O(n log n) 풀이 가능

---

**추천 학습 경로**:
1. 완전 탐색 O(n²) 풀이부터 이해하기
2. 단조 스택의 개념 파악하기
3. 너비 계산 로직 정확히 이해하기
4. 오버플로우/엣지 케이스 체크하기

