---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 31. heapq & bisect - 우선순위 큐/이진 검색 패턴"
slug: "heapq-and-bisect-heap-priority-queue-binary-search-sorted-list-heappop"
description: "파이썬 heapq와 bisect 모듈을 빠르게 쓰기 위한 치트시트입니다. 우선순위 큐 구현, 최소/최대 힙, 정렬된 리스트에서 이진 검색, nlargest/nsmallest 패턴과 주의점을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 31
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - heapq
  - heap
  - 힙
  - priority-queue
  - 우선순위큐
  - bisect
  - binary-search
  - 이진검색
  - 이진탐색
  - sorted-list
  - 정렬리스트
  - min-heap
  - max-heap
  - 최소힙
  - 최대힙
  - nlargest
  - nsmallest
  - heappush
  - heappop
  - heapify
  - insort
  - bisect_left
  - bisect_right
  - algorithm
  - 알고리즘
  - data-structure
  - 자료구조
  - performance
  - 성능
  - O(log n)
  - efficiency
  - 효율
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
heapq는 우선순위 큐를, bisect는 정렬된 리스트에서 이진 검색을 제공합니다. 이 치트시트는 최소/최대 힙, 정렬 유지 삽입, nlargest/nsmallest 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- **가장 작은/큰 N개**를 효율적으로 찾고 싶을 때
- **정렬된 리스트**를 유지하면서 삽입/검색하고 싶을 때

## 핵심 패턴

- `heapq`: 리스트를 힙으로 사용 (최소 힙)
- `bisect`: 정렬된 리스트에서 O(log n) 검색/삽입 위치 찾기
- 최대 힙: 값에 `-`를 붙여서 최소 힙으로 구현

## heapq - 우선순위 큐

```python
import heapq

# 빈 리스트를 힙으로 사용
heap = []

# 삽입 - O(log n)
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 4)
heapq.heappush(heap, 1)
heapq.heappush(heap, 5)

print(heap)  # [1, 1, 4, 3, 5] - 최소값이 항상 heap[0]

# 최소값 꺼내기 - O(log n)
smallest = heapq.heappop(heap)
print(smallest)  # 1
print(heap)      # [1, 3, 4, 5]

# 최소값 확인 (제거 안 함)
print(heap[0])   # 1
```

```python
# 기존 리스트를 힙으로 변환 - O(n)
data = [5, 7, 9, 1, 3]
heapq.heapify(data)
print(data)  # [1, 3, 9, 7, 5]
```

```python
# heappushpop: push 후 pop (더 효율적)
result = heapq.heappushpop(heap, 2)

# heapreplace: pop 후 push
result = heapq.heapreplace(heap, 10)
```

## 최대 힙 구현

```python
import heapq

# 방법 1: 값에 -를 붙여서 최소 힙 사용
max_heap = []
for val in [3, 1, 4, 1, 5]:
    heapq.heappush(max_heap, -val)

largest = -heapq.heappop(max_heap)  # 5
print(largest)

# 방법 2: 튜플 사용 (우선순위, 값)
max_heap = []
for val in [3, 1, 4, 1, 5]:
    heapq.heappush(max_heap, (-val, val))

_, largest = heapq.heappop(max_heap)
print(largest)  # 5
```

## nlargest / nsmallest

```python
import heapq

data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

# 가장 큰 3개
print(heapq.nlargest(3, data))   # [9, 6, 5]

# 가장 작은 3개
print(heapq.nsmallest(3, data))  # [1, 1, 2]

# key 함수 사용
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35},
]
oldest = heapq.nlargest(2, users, key=lambda x: x["age"])
print(oldest)  # [{'name': 'Charlie', 'age': 35}, {'name': 'Alice', 'age': 30}]
```

> **성능 팁**: 전체 정렬 `sorted()[-n:]`보다 `nlargest(n)`이 효율적 (n이 작을 때)

## bisect - 정렬된 리스트 이진 검색

```python
import bisect

# 정렬된 리스트
sorted_list = [1, 3, 4, 4, 6, 8]

# 삽입 위치 찾기 (왼쪽)
pos = bisect.bisect_left(sorted_list, 4)
print(pos)  # 2 (첫 번째 4의 위치)

# 삽입 위치 찾기 (오른쪽)
pos = bisect.bisect_right(sorted_list, 4)  # 또는 bisect.bisect()
print(pos)  # 4 (마지막 4 다음 위치)

# 값 존재 확인
def binary_search(arr, x):
    i = bisect.bisect_left(arr, x)
    return i < len(arr) and arr[i] == x

print(binary_search(sorted_list, 4))  # True
print(binary_search(sorted_list, 5))  # False
```

```python
# 정렬 유지하며 삽입 - O(n) (삽입 자체는 O(n))
import bisect

sorted_list = [1, 3, 5, 7]

bisect.insort(sorted_list, 4)  # insort_right와 동일
print(sorted_list)  # [1, 3, 4, 5, 7]

bisect.insort_left(sorted_list, 5)
print(sorted_list)  # [1, 3, 4, 5, 5, 7]
```

## 실전 패턴

```python
# 등급 계산 (bisect 활용)
import bisect

def get_grade(score: int) -> str:
    breakpoints = [60, 70, 80, 90]
    grades = ['F', 'D', 'C', 'B', 'A']
    i = bisect.bisect(breakpoints, score)
    return grades[i]

print(get_grade(85))  # B
print(get_grade(92))  # A
print(get_grade(55))  # F
```

```python
# 작업 스케줄러 (heapq 활용)
import heapq
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class Task:
    priority: int
    name: str = field(compare=False)
    
tasks = []
heapq.heappush(tasks, Task(2, "medium task"))
heapq.heappush(tasks, Task(1, "high priority"))
heapq.heappush(tasks, Task(3, "low priority"))

while tasks:
    task = heapq.heappop(tasks)
    print(f"Processing: {task.name}")
# Processing: high priority
# Processing: medium task
# Processing: low priority
```

```python
# Running Median (두 개의 힙 사용)
import heapq

class RunningMedian:
    def __init__(self):
        self.small = []  # max heap (negated)
        self.large = []  # min heap
    
    def add(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def median(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2

rm = RunningMedian()
for n in [2, 3, 4]:
    rm.add(n)
    print(rm.median())  # 2.0, 2.5, 3.0
```

## 자주 하는 실수/주의점

- **heapq는 최소 힙만 제공**: 최대 힙은 `-` 붙여서 구현
- **heap[0]만 최소값 보장**: 나머지 순서는 정렬 아님
- **bisect.insort는 O(n)**: 삽입 위치 찾기는 O(log n)이지만, 실제 삽입은 O(n)
- **리스트가 정렬되어 있어야 함**: bisect는 정렬된 리스트에서만 동작
- **nlargest/nsmallest 선택 기준**:
  - n이 작으면: `nlargest(n, data)` 사용
  - n이 1이면: `min(data)` / `max(data)` 사용
  - n이 크면: `sorted(data)[:n]` 사용

## 관련 링크(공식 문서)

- [heapq — Heap queue algorithm](https://docs.python.org/3/library/heapq.html)
- [bisect — Array bisection algorithm](https://docs.python.org/3/library/bisect.html)
