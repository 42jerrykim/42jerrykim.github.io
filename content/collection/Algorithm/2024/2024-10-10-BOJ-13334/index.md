---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-10-10T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- PriorityQueue
- Greedy
- Sorting
- Sweeping
- DataStructure
title: '[Algorithm] C++/Python 백준 13334번 : 철로'
---

철로 문제는 우선순위 큐와 그리디 알고리즘을 활용하여 효율적으로 해결할 수 있는 문제이다. 수평선 상에 위치한 여러 사람들의 집과 사무실 위치가 주어질 때, 일정한 길이의 철로를 적절히 배치하여 최대한 많은 사람들이 철로를 이용할 수 있도록 하는 것이 목표이다. 이 글에서는 해당 문제를 해결하기 위한 접근 방법과 C++ 및 Python 코드 구현을 상세하게 설명한다.

문제 : [https://www.acmicpc.net/problem/13334](https://www.acmicpc.net/problem/13334)

|![/assets/images/undefined/algorithm.png](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 문제 설명

수평선 위에 집과 사무실이 위치한 **n명의 사람들**이 있다. 각 사람의 집과 사무실은 수평선 상의 특정 지점에 있으며, 이 지점들은 서로 다를 필요는 없다. 즉, 어떤 사람의 집이 다른 사람의 사무실과 같은 위치에 있을 수 있다.

이 사람들의 통근을 돕기 위해 길이가 **d인 철로**를 건설하려 한다. 이 철로는 수평선 상의 어떤 구간이며, 이 구간 위로 기차가 운행된다. 목표는 이 철로 구간에 **집과 사무실 위치가 모두 포함되는 사람들의 수를 최대화**하는 것이다.

예산의 한계로 철로의 길이 **d는 고정된 값**이다. 따라서 우리는 길이 d인 구간을 적절히 선택하여 최대한 많은 사람들이 그 철로를 이용할 수 있도록 해야 한다.

**입력으로** n명의 사람들의 집과 사무실 위치가 주어지며, 각 위치는 정수로 표현된다. 또한 철로의 길이 d가 주어진다.

**목표는** 길이 d의 구간을 적절히 선택하여, 그 구간에 집과 사무실 위치가 모두 포함되는 사람들의 최대 수를 구하는 것이다.

## 접근 방식

이 문제는 주어진 사람들의 집과 사무실 위치를 기반으로, 길이 d인 구간 내에 최대한 많은 사람들의 집과 사무실이 포함되도록 하는 **최대 커버(interval covering)** 문제이다. 이를 효율적으로 해결하기 위해 다음과 같은 알고리즘과 자료 구조를 사용한다:

1. **Interval 생성**: 각 사람의 집과 사무실 위치 중 작은 값을 시작점, 큰 값을 끝점으로 하는 인터벌을 만든다.

2. **유효한 Interval 필터링**: 각 인터벌의 길이가 d를 초과하는 경우 고려할 필요가 없으므로, 길이가 d 이하인 인터벌만을 선택한다.

3. **끝점을 기준으로 정렬**: 선택된 인터벌들을 끝점을 기준으로 오름차순 정렬한다. 이는 스위핑(sweeping) 기법을 적용하기 위함이다.

4. **우선순위 큐 사용**: 시작점을 관리하기 위해 최소 힙(min-heap)을 사용한다. 현재 고려하는 끝점에서 시작하여, 시작점이 (현재 끝점 - d) 이상인 인터벌들만 힙에 유지한다.

5. **최대 인원 수 계산**: 각 단계에서 힙에 남아 있는 인터벌들의 수가 현재 구간에 포함되는 사람들의 수이며, 이를 통해 최대값을 갱신한다.

이러한 접근 방식은 시간 복잡도가 O(n log n)이므로, 주어진 n의 범위 내에서 효율적으로 동작한다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

// 집과 사무실 위치를 나타내는 구조체
struct Interval {
    long long start;
    long long end;
};

int main() {
    int n;
    scanf("%d", &n);
    vector<Interval> intervals;

    // 입력 받기
    for (int i = 0; i < n; ++i) {
        long long h, o;
        scanf("%lld %lld", &h, &o);
        long long a = min(h, o);
        long long b = max(h, o);
        intervals.push_back({a, b});
    }

    long long d;
    scanf("%lld", &d);

    // 유효한 인터벌 필터링
    vector<Interval> validIntervals;
    for (auto &interval : intervals) {
        if (interval.end - interval.start <= d) {
            validIntervals.push_back(interval);
        }
    }

    // 끝점을 기준으로 오름차순 정렬
    sort(validIntervals.begin(), validIntervals.end(), [](const Interval &a, const Interval &b) {
        return a.end < b.end;
    });

    // 최소 힙 선언
    priority_queue<long long, vector<long long>, greater<long long>> minHeap;
    int maxCount = 0;

    // 스위핑 수행
    for (auto &interval : validIntervals) {
        minHeap.push(interval.start);
        // 힙에서 유효하지 않은 시작점 제거
        while (!minHeap.empty() && minHeap.top() < interval.end - d) {
            minHeap.pop();
        }
        // 현재 힙 크기가 해당 구간에 포함되는 사람 수
        int currentCount = minHeap.size();
        if (currentCount > maxCount) {
            maxCount = currentCount;
        }
    }

    printf("%d\n", maxCount);
    return 0;
}
```

**코드 설명**

1. **입력 처리**:
   - 사람 수 `n`을 입력받는다.
   - 각 사람의 집 `h`와 사무실 `o` 위치를 입력받아, 시작점과 끝점으로 구성된 `Interval`을 생성한다.

2. **유효한 인터벌 필터링**:
   - 각 인터벌의 길이가 `d` 이하인 경우만 `validIntervals`에 추가한다.

3. **인터벌 정렬**:
   - `validIntervals`를 끝점을 기준으로 오름차순 정렬한다.

4. **스위핑과 힙 사용**:
   - 최소 힙 `minHeap`을 사용하여 시작점을 관리한다.
   - 현재 인터벌의 끝점에서 길이 `d`를 뺀 값보다 작은 시작점을 가진 인터벌들은 힙에서 제거한다.
   - 힙의 크기는 현재 구간에 포함되는 사람들의 수이며, 이를 이용하여 `maxCount`를 갱신한다.

5. **결과 출력**:
   - 최대 인원 수 `maxCount`를 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    long long start;
    long long end;
} Interval;

int compare(const void* a, const void* b) {
    Interval* ia = (Interval*)a;
    Interval* ib = (Interval*)b;
    if (ia->end != ib->end) {
        return ia->end > ib->end ? 1 : -1;
    }
    return 0;
}

typedef struct {
    long long* data;
    int size;
    int capacity;
} MinHeap;

void initHeap(MinHeap* heap, int capacity) {
    heap->data = (long long*)malloc(sizeof(long long) * capacity);
    heap->size = 0;
    heap->capacity = capacity;
}

void swap(long long* a, long long* b) {
    long long temp = *a;
    *a = *b;
    *b = temp;
}

void push(MinHeap* heap, long long value) {
    int idx = heap->size++;
    heap->data[idx] = value;
    while (idx > 0 && heap->data[idx] < heap->data[(idx - 1) / 2]) {
        swap(&heap->data[idx], &heap->data[(idx - 1) / 2]);
        idx = (idx - 1) / 2;
    }
}

long long top(MinHeap* heap) {
    return heap->data[0];
}

void pop(MinHeap* heap) {
    heap->data[0] = heap->data[--heap->size];
    int idx = 0;
    while (1) {
        int left = idx * 2 + 1;
        int right = idx * 2 + 2;
        int smallest = idx;
        if (left < heap->size && heap->data[left] < heap->data[smallest]) {
            smallest = left;
        }
        if (right < heap->size && heap->data[right] < heap->data[smallest]) {
            smallest = right;
        }
        if (smallest == idx) break;
        swap(&heap->data[idx], &heap->data[smallest]);
        idx = smallest;
    }
}

int main() {
    int n;
    scanf("%d", &n);
    Interval* intervals = (Interval*)malloc(sizeof(Interval) * n);
    int i;
    for (i = 0; i < n; ++i) {
        long long h, o;
        scanf("%lld %lld", &h, &o);
        intervals[i].start = h < o ? h : o;
        intervals[i].end = h > o ? h : o;
    }

    long long d;
    scanf("%lld", &d);

    Interval* validIntervals = (Interval*)malloc(sizeof(Interval) * n);
    int validCount = 0;
    for (i = 0; i < n; ++i) {
        if (intervals[i].end - intervals[i].start <= d) {
            validIntervals[validCount++] = intervals[i];
        }
    }

    qsort(validIntervals, validCount, sizeof(Interval), compare);

    MinHeap heap;
    initHeap(&heap, validCount);

    int maxCount = 0;

    for (i = 0; i < validCount; ++i) {
        push(&heap, validIntervals[i].start);
        while (heap.size > 0 && top(&heap) < validIntervals[i].end - d) {
            pop(&heap);
        }
        if (heap.size > maxCount) {
            maxCount = heap.size;
        }
    }

    printf("%d\n", maxCount);

    free(intervals);
    free(validIntervals);
    free(heap.data);
    return 0;
}
```

**코드 설명**

- **자료구조 구현**: 표준 라이브러리를 사용할 수 없으므로, 최소 힙을 직접 구현하였다.
  - `MinHeap` 구조체를 정의하여 힙의 기능을 제공한다.
  - `push`, `pop`, `top` 함수로 힙을 조작한다.
- **입력 처리 및 유효한 인터벌 필터링**: 이전 코드와 동일한 방식으로 처리한다.
- **정렬**: `qsort` 함수를 사용하여 끝점을 기준으로 인터벌을 정렬한다.
- **스위핑 및 힙 사용**: 힙에 시작점을 추가하고, 필요에 따라 힙에서 제거하면서 최대 인원 수를 계산한다.
- **메모리 관리**: `malloc`과 `free`를 사용하여 동적으로 할당한 메모리를 관리한다.

## Python 코드와 설명

```python
import sys
import heapq

# 입력을 빠르게 받기 위해 readline 사용
input = sys.stdin.readline

n = int(input())
intervals = []

# 입력 받기
for _ in range(n):
    h, o = map(int, input().split())
    a, b = min(h, o), max(h, o)
    intervals.append((a, b))

d = int(input())

# 유효한 인터벌 필터링
valid_intervals = [(a, b) for a, b in intervals if b - a <= d]

# 끝점을 기준으로 정렬
valid_intervals.sort(key=lambda x: x[1])

min_heap = []
max_count = 0

# 스위핑 수행
for start, end in valid_intervals:
    heapq.heappush(min_heap, start)
    # 힙에서 유효하지 않은 시작점 제거
    while min_heap and min_heap[0] < end - d:
        heapq.heappop(min_heap)
    current_count = len(min_heap)
    if current_count > max_count:
        max_count = current_count

print(max_count)
```

**코드 설명**

1. **입력 처리**:
   - `sys.stdin.readline`을 사용하여 입력을 빠르게 받는다.
   - 각 사람의 집과 사무실 위치를 입력받아 `(시작점, 끝점)` 형태의 튜플로 저장한다.

2. **유효한 인터벌 필터링**:
   - 리스트 컴프리헨션을 사용하여 길이가 `d` 이하인 인터벌만 선택한다.

3. **인터벌 정렬**:
   - `sort` 함수를 사용하여 끝점을 기준으로 인터벌을 정렬한다.

4. **스위핑과 힙 사용**:
   - `heapq` 모듈의 `heappush`와 `heappop`을 사용하여 최소 힙을 구현한다.
   - 힙에 시작점을 추가하고, 필요에 따라 힙에서 제거하면서 최대 인원 수를 갱신한다.

5. **결과 출력**:
   - 최대 인원 수를 출력한다.

## 결론

이 문제는 스위핑 기법과 우선순위 큐를 활용한 그리디 알고리즘의 전형적인 예시이다. 인터벌을 끝점을 기준으로 정렬하고, 최소 힙을 사용하여 시작점을 관리함으로써 효율적으로 최대 인원 수를 계산할 수 있었다. 이를 통해 시간 복잡도를 O(n log n)으로 유지하면서도 큰 입력에 대해 빠르게 동작하는 코드를 작성할 수 있었다.

이번 문제를 통해 인터벌 스케줄링과 우선순위 큐의 활용 방법을 더욱 깊이 있게 이해할 수 있었다. 또한, 라이브러리를 사용할 수 없는 환경에서도 기본적인 자료구조와 알고리즘을 직접 구현하는 연습이 되었으며, 이는 알고리즘 문제 해결 능력을 향상시키는 데 큰 도움이 되었다.