---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-14T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Stack
- DivideAndConquer
- O(N)
- DataStructure
- LargestRectangle
- Histogram
title: '[Algorithm] C++/Python 백준 6549번 : 히스토그램에서 가장 큰 직사각형'
---

히스토그램은 여러 개의 직사각형이 연속적으로 나열된 도형으로, 각 직사각형은 너비가 1이고 높이는 다양한 값을 가질 수 있다. 이 문제에서는 주어진 히스토그램에서 가장 큰 넓이를 갖는 직사각형을 찾는 것이 목표이다. 예를 들어, 히스토그램의 막대 높이가 `[2, 1, 5, 6, 2, 3]`일 때, 가장 큰 직사각형의 넓이는 `10`이다.

입력은 여러 개의 테스트 케이스로 구성되며, 각 테스트 케이스는 첫 번째 수로 막대의 개수 `N`(1 ≤ N ≤ 100,000)이 주어지고, 이어서 각 막대의 높이 `h_i`(0 ≤ h_i ≤ 1,000,000,000)가 주어진다. 마지막 입력은 `0`으로 표시되며, 이는 입력의 끝을 나타낸다. 각 테스트 케이스마다 히스토그램에서 가장 큰 직사각형의 넓이를 출력해야 한다.

이 문제는 매우 큰 데이터셋을 효율적으로 처리해야 하므로, 시간 복잡도가 낮은 알고리즘을 사용해야 한다.

문제 : [https://www.acmicpc.net/problem/6549](https://www.acmicpc.net/problem/6549)

|![/assets/images/undefined/algorithm.png](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제를 해결하기 위해 **스택(Stack)**을 이용한 선형 시간 알고리즘(O(N))을 사용한다. 일반적인 아이디어는 히스토그램을 왼쪽에서 오른쪽으로 순회하면서 각 막대에 대해 가능한 최대 직사각형의 넓이를 계산하는 것이다. 스택에는 막대의 인덱스를 저장하며, 현재 막대의 높이가 스택의 최상단 막대보다 작을 경우 스택에서 막대를 꺼내면서 최대 넓이를 갱신한다.

이 알고리즘의 핵심은 다음과 같다:

- 스택에는 높이가 증가하는 순서로 막대의 인덱스를 저장한다.
- 현재 막대의 높이가 스택의 최상단 막대보다 작으면, 스택에서 막대를 꺼내고 해당 막대를 높이로 하는 최대 직사각형의 넓이를 계산한다.
- 이 과정을 히스토그램의 끝까지 진행하며, 스택에 남은 막대들도 동일하게 처리한다.

이 방법을 통해 시간 복잡도 O(N)에 문제를 해결할 수 있다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <stack>

using namespace std;

int main() {
    while (true) {
        int n;
        cin >> n; // 히스토그램의 막대 수 입력
        if (n == 0) break; // 입력의 끝이면 종료

        vector<long long> heights(n); // 막대의 높이를 저장할 벡터
        for (int i = 0; i < n; ++i) {
            cin >> heights[i]; // 각 막대의 높이 입력
        }

        stack<int> s; // 인덱스를 저장할 스택
        long long max_area = 0; // 최대 넓이 초기화

        for (int i = 0; i < n; ++i) {
            // 현재 막대의 높이가 스택 최상단 막대보다 작을 때까지 반복
            while (!s.empty() && heights[s.top()] > heights[i]) {
                int tp = s.top(); // 스택 최상단 막대의 인덱스
                s.pop(); // 스택에서 제거
                long long h = heights[tp]; // 스택 최상단 막대의 높이
                long long width = s.empty() ? i : i - s.top() - 1; // 너비 계산
                max_area = max(max_area, h * width); // 최대 넓이 갱신
            }
            s.push(i); // 현재 막대의 인덱스를 스택에 추가
        }

        // 스택에 남은 막대 처리
        while (!s.empty()) {
            int tp = s.top();
            s.pop();
            long long h = heights[tp];
            long long width = s.empty() ? n : n - s.top() - 1;
            max_area = max(max_area, h * width);
        }

        cout << max_area << '\n'; // 최대 넓이 출력
    }
    return 0;
}
```

**코드의 동작 단계별 설명:**

1. **입력 처리**:
   - 히스토그램의 막대 수 `n`을 입력받는다. `n`이 `0`이면 루프를 종료한다.
   - `n`개의 막대 높이를 `heights` 벡터에 저장한다.

2. **스택 초기화 및 최대 넓이 변수 설정**:
   - 인덱스를 저장할 스택 `s`를 초기화한다.
   - 최대 넓이를 저장할 변수 `max_area`를 `0`으로 초기화한다.

3. **히스토그램 순회**:
   - 막대를 하나씩 순회하면서 현재 막대의 높이가 스택 최상단 막대의 높이보다 작을 경우, 스택에서 막대를 꺼내며 최대 넓이를 계산한다.
   - 너비 `width`는 스택이 비어 있으면 현재 인덱스 `i`, 그렇지 않으면 `i - s.top() - 1`이 된다.
   - 최대 넓이는 `max_area`와 계산된 넓이 중 큰 값으로 갱신한다.
   - 현재 막대의 인덱스를 스택에 추가한다.

4. **남은 스택 처리**:
   - 히스토그램 순회를 마친 후에도 스택에 남아 있는 막대들을 처리하여 최대 넓이를 갱신한다.
   - 이때 너비는 스택이 비어 있으면 `n`, 그렇지 않으면 `n - s.top() - 1`이 된다.

5. **결과 출력**:
   - 각 테스트 케이스마다 계산된 `max_area`를 출력한다.

**변경 사항 설명:**

- `h`와 `width` 변수를 `int`에서 `long long`으로 변경하였다. 이는 막대의 높이와 넓이의 곱이 `int` 범위를 초과할 수 있기 때문이다.
- 스택에서 막대의 높이를 가져올 때 임시로 인덱스 `tp`를 사용하여 코드의 가독성을 높였다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <malloc.h>

int main() {
    while (1) {
        int n;
        scanf("%d", &n); // 히스토그램의 막대 수 입력
        if (n == 0) break; // 입력의 끝이면 종료

        long long* heights = (long long*)malloc(n * sizeof(long long)); // 막대 높이 배열 동적 할당
        int* stack = (int*)malloc(n * sizeof(int)); // 스택 배열 동적 할당
        int top = -1; // 스택의 최상단 인덱스

        for (int i = 0; i < n; ++i) {
            scanf("%lld", &heights[i]); // 각 막대의 높이 입력
        }

        long long max_area = 0; // 최대 넓이 초기화
        int i = 0;
        while (i < n) {
            // 스택이 비어 있거나 현재 막대의 높이가 스택 최상단 막대보다 크거나 같으면
            if (top == -1 || heights[stack[top]] <= heights[i]) {
                stack[++top] = i++; // 현재 막대의 인덱스를 스택에 추가
            } else {
                int tp = stack[top--]; // 스택에서 최상단 막대 인덱스 꺼내기
                long long h = heights[tp]; // 높이
                long long width = top == -1 ? i : i - stack[top] - 1; // 너비 계산
                long long area = h * width; // 넓이 계산
                if (area > max_area) max_area = area; // 최대 넓이 갱신
            }
        }

        // 남은 스택 처리
        while (top != -1) {
            int tp = stack[top--];
            long long h = heights[tp];
            long long width = top == -1 ? i : i - stack[top] - 1;
            long long area = h * width;
            if (area > max_area) max_area = area;
        }

        printf("%lld\n", max_area); // 최대 넓이 출력

        free(heights); // 동적 할당 메모리 해제
        free(stack);
    }
    return 0;
}
```

**코드의 동작 단계별 설명:**

1. **입력 처리 및 메모리 할당**:
   - 히스토그램의 막대 수 `n`을 `scanf`로 입력받는다. `n`이 `0`이면 루프를 종료한다.
   - `n` 크기의 `heights` 배열과 `stack` 배열을 동적 할당한다.
   - 각 막대의 높이를 `heights` 배열에 저장한다.

2. **스택 및 변수 초기화**:
   - 스택의 최상단 인덱스를 나타내는 `top`을 `-1`로 초기화한다.
   - 최대 넓이를 저장할 `max_area`를 `0`으로 초기화한다.

3. **히스토그램 순회**:
   - 인덱스 `i`를 `0`부터 시작하여 `n`까지 순회한다.
   - 현재 막대의 높이가 스택 최상단 막대의 높이보다 크거나 같으면 스택에 인덱스를 추가하고 `i`를 증가시킨다.
   - 그렇지 않으면 스택에서 막대 인덱스를 꺼내며 최대 넓이를 계산한다.
   - 너비는 스택이 비어 있으면 `i`, 그렇지 않으면 `i - stack[top] - 1`이 된다.

4. **남은 스택 처리**:
   - 히스토그램 순회를 마친 후에도 스택에 남아 있는 막대들을 처리하여 최대 넓이를 갱신한다.

5. **결과 출력 및 메모리 해제**:
   - 계산된 `max_area`를 출력한다.
   - 동적 할당한 메모리를 해제한다.

**변경 사항 설명:**

- `h`, `width`, `area` 변수를 `long long`으로 선언하여 오버플로우를 방지하였다.
- `scanf`와 `printf`에서 `long long` 자료형을 처리하기 위해 `%lld` 포맷 지정자를 사용하였다.

## Python 코드와 설명

```python
import sys

input = sys.stdin.readline

while True:
    inputs = sys.stdin.readline().split()
    n = int(inputs[0]) # 히스토그램의 막대 수
    if n == 0:
        break # 입력의 끝이면 종료
    heights = list(map(int, inputs[1:])) # 막대 높이 리스트

    stack = [] # 인덱스를 저장할 스택
    max_area = 0 # 최대 넓이 초기화
    i = 0
    while i < n:
        # 스택이 비어 있거나 현재 막대의 높이가 스택 최상단 막대보다 크거나 같으면
        if not stack or heights[stack[-1]] <= heights[i]:
            stack.append(i) # 현재 막대의 인덱스를 스택에 추가
            i += 1
        else:
            tp = stack.pop() # 스택에서 최상단 막대 인덱스 꺼내기
            h = heights[tp] # 높이
            width = i if not stack else i - stack[-1] - 1 # 너비 계산
            area = h * width # 넓이 계산
            if area > max_area:
                max_area = area # 최대 넓이 갱신

    # 남은 스택 처리
    while stack:
        tp = stack.pop()
        h = heights[tp]
        width = i if not stack else i - stack[-1] - 1
        area = h * width
        if area > max_area:
            max_area = area

    print(max_area) # 최대 넓이 출력
```

**코드의 동작 단계별 설명:**

1. **입력 처리**:
   - `sys.stdin.readline()`을 사용하여 입력을 빠르게 처리한다.
   - 한 줄의 입력을 받아 공백으로 분리하여 `inputs` 리스트에 저장한다.
   - 첫 번째 요소를 막대 수 `n`으로 변환한다. `n`이 `0`이면 루프를 종료한다.
   - 나머지 요소들을 막대 높이로 변환하여 `heights` 리스트에 저장한다.

2. **스택 및 변수 초기화**:
   - 인덱스를 저장할 스택 `stack`을 빈 리스트로 초기화한다.
   - 최대 넓이를 저장할 `max_area`를 `0`으로 초기화한다.

3. **히스토그램 순회**:
   - 인덱스 `i`를 `0`부터 시작하여 `n`까지 순회한다.
   - 현재 막대의 높이가 스택 최상단 막대의 높이보다 크거나 같으면 스택에 인덱스를 추가하고 `i`를 증가시킨다.
   - 그렇지 않으면 스택에서 막대 인덱스를 꺼내며 최대 넓이를 계산한다.
   - 너비는 스택이 비어 있으면 `i`, 그렇지 않으면 `i - stack[-1] - 1`이 된다.

4. **남은 스택 처리**:
   - 히스토그램 순회를 마친 후에도 스택에 남아 있는 막대들을 처리하여 최대 넓이를 갱신한다.

5. **결과 출력**:
   - 계산된 `max_area`를 출력한다.

**변경 사항 설명:**

- 입력 속도를 향상시키기 위해 `sys.stdin.readline`을 사용하였다.
- 최대 넓이를 계산할 때 조건문을 추가하여 `max_area`를 갱신하도록 수정하였다.

## 결론

이 문제를 통해 스택을 활용한 효율적인 알고리즘의 중요성을 다시 한 번 느낄 수 있었다. 특히 큰 입력 데이터를 처리할 때 자료형에 대한 정확한 이해와 활용이 얼마나 중요한지 깨달았다. C++ 코드에서 `int`와 `long long`의 차이가 결과에 큰 영향을 미칠 수 있으므로, 항상 변수의 범위를 고려하여 자료형을 선택해야 한다.

추가적인 최적화 방안으로는 입력 속도를 향상시키기 위해 C++에서는 `scanf`와 `printf`를 사용하거나, Python에서는 `sys.stdin.readline`을 사용할 수 있다. 앞으로도 다양한 알고리즘 문제를 통해 알고리즘적 사고와 최적화 기법을 연습해야겠다.