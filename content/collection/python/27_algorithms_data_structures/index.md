---
draft: false
image: "wordcloud.png"
title: "[Python Master] 27. 고급 알고리즘과 자료구조 - 복잡도 분석"
slug: "python-advanced-algorithms-data-structures-big-o-guide"
description: "시간복잡도 관점에서 고급 자료구조와 알고리즘 설계 방법을 정리합니다. 문제를 모델링하고 최적화하는 사고 과정을 중심으로 실제 구현과 성능 판단 기준을 함께 다룹니다."
tags:
  - Python
  - Implementation(구현)
  - Software-Architecture(소프트웨어아키텍처)
  - Algorithm(알고리즘)
  - Backend(백엔드)
  - Best-Practices
  - Clean-Code(클린코드)
  - Refactoring(리팩토링)
  - Testing(테스트)
  - Debugging(디버깅)
  - Logging(로깅)
  - Security(보안)
  - Performance(성능)
  - Concurrency(동시성)
  - Async(비동기)
  - OOP(객체지향)
  - Data-Structures(자료구조)
  - DevOps
  - Deployment(배포)
  - Design-Pattern(디자인패턴)
  - Web(웹)
  - Database(데이터베이스)
  - Networking(네트워킹)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Automation(자동화)
  - Documentation(문서화)
  - Git
  - Code-Quality(코드품질)
lastmod: 2026-01-17
collection_order: 27
---
# 챕터 27: 고급 알고리즘과 자료구조 전략

## 학습 목표
- 알고리즘의 복잡도를 분석하고 최적화할 수 있다
- 고급 자료구조를 구현하고 활용할 수 있다
- 문제 해결을 위한 적절한 알고리즘을 선택할 수 있다
- 실제 애플리케이션에 알고리즘을 적용할 수 있다

## 핵심 개념(이론)

### 1) 고급 알고리즘과 자료구조의 역할과 경계
이 챕터의 핵심은 “무엇을 할 수 있나”가 아니라, **어떤 문제를 해결하고 어디까지 책임지는지**를 분명히 하는 것입니다.
경계가 흐리면 코드는 커질수록 결합이 늘어나고 수정 비용이 커집니다.

### 2) 왜 이 개념이 필요한가(실무 동기)
실무에서는 예외 상황, 성능, 협업, 테스트가 항상 문제를 만듭니다.
따라서 이 주제는 기능이 아니라 <strong>품질(신뢰성/유지보수성/보안)</strong>을 위한 기반으로 이해해야 합니다.

### 3) 트레이드오프: 간단함 vs 확장성
대부분의 선택은 “더 단순하게”와 “더 확장 가능하게” 사이에서 균형을 잡는 일입니다.
초기에는 단순함을, 장기 운영/팀 협업이 커질수록 확장성을 더 우선합니다.

### 4) 실패 모드(Failure Modes)를 먼저 생각하라
무엇이 실패하는지(입력, I/O, 동시성, 외부 시스템)를 먼저 떠올리면 설계가 안정적으로 변합니다.
이 챕터의 예제는 실패 모드를 축소해서 보여주므로, 실제 적용 시에는 더 많은 방어가 필요합니다.

### 5) 학습 포인트: 외우지 말고 “판단 기준”을 남겨라
핵심은 API를 외우는 것이 아니라, “언제 무엇을 선택할지” 판단 기준을 정리하는 것입니다.
이 기준이 쌓이면 새로운 라이브러리/도구가 나와도 빠르게 적응할 수 있습니다.

## 선택 기준(Decision Guide)
- 기본은 **가독성/명확성** 우선(최적화는 측정 이후).
- 외부 의존이 늘수록 **경계/추상화**와 **테스트**를 먼저 강화.
- 복잡도가 증가하면 “규칙을 코드로”가 아니라 “구조로” 담는 방향을 고려.

## 흔한 오해/주의점
- 도구/문법이 곧 실력이라는 오해가 있습니다. 실력은 문제를 단순화하고 구조화하는 능력입니다.
- 극단적 최적화/과설계는 학습과 유지보수를 방해할 수 있습니다.

## 요약
- 고급 알고리즘과 자료구조는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 핵심 내용

### 복잡도 분석: 알고리즘의 비용을 정량화하기

알고리즘을 비교하려면 먼저 "얼마나 빠른가"와 "얼마나 많은 메모리를 쓰는가"를 입력 크기 `n`에 대한 함수로 표현해야 한다. **Big-O(빅오)** 표기법은 입력이 커질 때 실행 시간이 늘어나는 상한을 나타내고, <strong>Θ(세타)</strong>는 상한과 하한이 같은 정확한 증가율을, <strong>Ω(오메가)</strong>는 하한을 나타낸다. 실무에서 "이 함수는 O(n log n)이다"라고 말할 때는 대체로 최악의 경우(worst case) 또는 평균적인 경우(average case)의 상한을 의미하며, 어떤 경우를 기준으로 하는지 명시하지 않으면 오해가 생기기 쉽다. 예를 들어 삽입 정렬은 최선의 경우(이미 정렬된 입력) O(n)이지만 최악의 경우 O(n²)이므로, "삽입 정렬은 O(n)이다"라는 진술은 최선의 경우에만 참이다. <strong>상각 분석(amortized analysis)</strong>은 개별 연산이 아니라 연산을 여러 번 반복했을 때의 평균 비용을 계산하는 방법으로, 파이썬 `list.append()`가 "O(1)"로 불리는 이유이기도 하다. 리스트가 꽉 차면 내부적으로 더 큰 배열을 할당하고 기존 요소를 복사하는 O(n) 작업이 가끔 발생하지만, 할당 크기를 지수적으로 늘리기 때문에 이 비용을 전체 삽입 횟수로 나누면 평균 O(1)이 된다.

### 정렬 알고리즘: 분할 정복 구현과 내장 정렬의 현실

<strong>병합 정렬(merge sort)</strong>은 **분할 정복(divide and conquer)** 전략의 대표적인 예로, 리스트를 반으로 나눠 각각 재귀적으로 정렬한 뒤 두 정렬된 리스트를 하나로 병합한다. 분할에 O(log n)단계가 필요하고 각 단계에서 병합에 O(n)이 걸리므로 전체 시간 복잡도는 최선·평균·최악 모두 O(n log n)으로 일정하다는 것이 병합 정렬의 핵심 장점이며, 대신 병합 과정에서 별도의 리스트를 만들기 때문에 O(n)의 추가 공간이 필요하다.

```python
def merge_sort(arr):
    """병합 정렬: 분할 정복으로 리스트를 정렬한다. 최선/평균/최악 모두 O(n log n)이다."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    """정렬된 두 리스트를 하나의 정렬된 리스트로 합친다 (O(n))."""
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


if __name__ == "__main__":
    data = [5, 2, 9, 1, 5, 6]
    print(merge_sort(data))  # [1, 2, 5, 5, 6, 9]
```

<strong>퀵 정렬(quick sort)</strong>도 분할 정복을 쓰지만 병합 대신 **피벗(pivot)** 기준으로 리스트를 작은 값과 큰 값으로 나누는 **분할(partition)** 단계에서 대부분의 작업을 끝낸다는 점이 다르다. 피벗이 데이터를 절반씩 나누면 평균 O(n log n)이지만, 이미 정렬된 데이터에서 항상 첫 번째나 마지막 원소를 피벗으로 고르는 구현은 분할이 한쪽으로 치우쳐 최악의 경우 O(n²)까지 나빠질 수 있다. 아래 구현은 이해하기 쉽도록 리스트 컴프리헨션으로 분할하지만, 그 결과 왼쪽·오른쪽 부분 리스트를 새로 만들어야 하므로 표준 in-place 구현(같은 배열 안에서 교환)보다 메모리를 더 사용한다.

```python
def quick_sort(arr):
    """퀵 정렬: 피벗 기준으로 분할해 정렬한다. 평균 O(n log n), 최악 O(n^2)."""
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


if __name__ == "__main__":
    data = [5, 2, 9, 1, 5, 6]
    print(quick_sort(data))  # [1, 2, 5, 5, 6, 9]
```

그렇다면 실무에서는 언제 이런 구현을 직접 써야 할까. 정답은 "거의 항상 쓰지 않는다"이다. 파이썬 내장 `sorted()`와 `list.sort()`는 <strong>팀소트(Timsort)</strong>라는 하이브리드 알고리즘을 C로 구현한 것으로, 병합 정렬과 삽입 정렬을 조합해 이미 정렬된 구간(run)을 감지하고 재사용하는 **적응형(adaptive)** 정렬이며, 최악의 경우에도 O(n log n)을 보장하고 값이 같은 원소의 상대 순서를 유지하는 <strong>안정 정렬(stable sort)</strong>이기도 하다. 순수 파이썬으로 작성한 재귀 함수는 매 호출마다 인터프리터 수준의 오버헤드가 있는 반면, `sorted()`는 C 레벨 루프로 동작하므로 같은 알고리즘적 복잡도라도 실측 성능 차이가 크다. 아래 벤치마크로 이를 직접 확인할 수 있다.

```python
import random
import timeit


def compare_sorting_performance():
    """정렬 함수 3종의 실행 시간을 비교한다."""
    data = [random.randint(1, 100_000) for _ in range(5_000)]

    results = {
        "merge_sort": timeit.timeit(lambda: merge_sort(data.copy()), number=5),
        "quick_sort": timeit.timeit(lambda: quick_sort(data.copy()), number=5),
        "sorted (Timsort)": timeit.timeit(lambda: sorted(data), number=5),
    }

    for name, elapsed in sorted(results.items(), key=lambda x: x[1]):
        print(f"{name}: {elapsed:.4f}초 (5회 합산)")


if __name__ == "__main__":
    compare_sorting_performance()
```

Python 3.13.5, Windows 환경에서 무작위 정수 5,000개를 5회 반복 정렬해 측정한 결과는 `sorted()` 0.0023초, `quick_sort` 0.0367초, `merge_sort` 0.0482초로, `sorted()`가 직접 구현한 퀵 정렬보다 약 16배, 병합 정렬보다 약 21배 빨랐다(정확한 배율은 하드웨어·파이썬 버전·데이터 분포에 따라 달라지는 구현 정의 값이므로 참고용으로만 받아들여야 한다). 따라서 실무 판단 기준은 명확하다. 학습 목적이나 코딩 테스트가 아니라면 정렬은 `sorted()`/`list.sort()`를 쓰고, 직접 구현이 필요한 경우는 "정렬 도중 커스텀 로직을 끼워 넣어야 한다" 같은 표준 라이브러리로 표현할 수 없는 특수한 요구사항이 있을 때로 한정한다.

### 탐색: 이진 탐색 구현과 bisect 모듈

정렬된 데이터에서 원하는 값을 찾을 때 <strong>선형 탐색(linear search)</strong>은 처음부터 끝까지 훑으므로 O(n)이 걸리지만, <strong>이진 탐색(binary search)</strong>은 매번 탐색 범위를 절반으로 줄여 O(log n)만에 끝난다. 이진 탐색이 성립하려면 데이터가 반드시 정렬되어 있어야 하고, "중간값이 목표보다 작으면 오른쪽 절반만, 크면 왼쪽 절반만 본다"는 불변식을 매 반복에서 유지해야 한다는 점이 구현의 핵심이다.

```python
def binary_search(arr, target):
    """정렬된 리스트에서 이진 탐색으로 target의 인덱스를 찾는다 (O(log n))."""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


if __name__ == "__main__":
    numbers = [1, 3, 5, 7, 9, 11, 13]
    print(binary_search(numbers, 7))   # 3
    print(binary_search(numbers, 4))   # -1
```

직접 구현한 이진 탐색은 "값이 있는지, 있다면 어디인지"만 답하지만, 실무에서 더 자주 필요한 질문은 "이 값을 정렬 상태를 유지하며 삽입하려면 어디에 넣어야 하는가"이다. 표준 라이브러리 `bisect` 모듈은 이 질문에 최적화되어 있으며, C로 구현되어 있어 직접 구현보다 빠르고 엣지 케이스(중복값 처리 등)도 이미 검증되어 있으므로, 정렬된 시퀀스를 다룰 때는 이진 탐색을 직접 구현하기보다 `bisect`를 우선 고려하는 것이 표준 라이브러리 우선 원칙에 맞다.

```python
import bisect


def bisect_search(arr, target):
    """bisect 모듈로 target의 존재 여부와 삽입 위치를 함께 찾는다."""
    index = bisect.bisect_left(arr, target)
    found = index < len(arr) and arr[index] == target
    return index, found


if __name__ == "__main__":
    numbers = [1, 3, 5, 7, 9, 11, 13]
    print(bisect_search(numbers, 7))   # (3, True)
    print(bisect_search(numbers, 4))   # (2, False), 4는 5 앞자리에 들어가야 함

    bisect.insort(numbers, 4)          # 정렬 상태를 유지하며 삽입
    print(numbers)                     # [1, 3, 4, 5, 7, 9, 11, 13]
```

### 자료구조 직접 구현: 연결 리스트, 스택/큐, 이진 탐색 트리

파이썬 `list`는 내부적으로 연속된 메모리 배열이라 인덱스 접근이 O(1)로 빠르지만, 맨 앞에 원소를 넣거나 뺄 때는 뒤의 모든 원소를 한 칸씩 밀어야 해 O(n)이 걸린다. <strong>연결 리스트(linked list)</strong>는 각 원소(노드)가 다음 노드의 참조만 가지고 메모리 어디에나 흩어져 존재할 수 있는 구조로, 맨 앞 삽입·삭제는 참조만 바꾸면 되므로 O(1)이지만 대신 임의 인덱스 접근이나 값 탐색은 노드를 하나씩 따라가야 해 O(n)이 된다. 즉 리스트와 연결 리스트는 서로 강점이 반대이며, "앞쪽 삽입·삭제가 잦은가, 인덱스 접근이 잦은가"가 선택 기준이다.

```python
class Node:
    """연결 리스트의 노드: 값과 다음 노드에 대한 참조를 가진다."""
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    """단방향 연결 리스트: 앞쪽 삽입/삭제는 O(1), 탐색/뒤쪽 삽입은 O(n)이다."""

    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def prepend(self, value):
        """맨 앞에 노드를 추가한다 (O(1))."""
        node = Node(value)
        node.next = self.head
        self.head = node
        self._size += 1

    def append(self, value):
        """맨 뒤에 노드를 추가한다 (O(n), 꼬리 포인터가 없어 순회가 필요하다)."""
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self._size += 1

    def find(self, value):
        """값을 순차 탐색해 인덱스를 반환한다 (O(n))."""
        current = self.head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def delete(self, value):
        """첫 번째로 일치하는 값을 가진 노드를 삭제한다 (O(n))."""
        if self.head is None:
            return False
        if self.head.value == value:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def to_list(self):
        """디버깅용: 파이썬 리스트로 변환한다."""
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result


if __name__ == "__main__":
    ll = SinglyLinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    print(ll.to_list())   # [0, 1, 2]
    print(ll.find(2))     # 2
    ll.delete(1)
    print(ll.to_list())   # [0, 2]
```

<strong>스택(stack)</strong>은 마지막에 넣은 값을 가장 먼저 꺼내는 **LIFO(Last-In-First-Out)** 구조이고, <strong>큐(queue)</strong>는 먼저 넣은 값을 먼저 꺼내는 **FIFO(First-In-First-Out)** 구조다. 파이썬 `list`로 스택을 만들면 `append()`/`pop()`이 모두 리스트의 끝에서 일어나므로 둘 다 O(1)이라 문제가 없지만, 같은 `list`로 큐를 만들어 `pop(0)`으로 앞에서 꺼내면 남은 원소를 전부 한 칸씩 당겨야 해서 O(n)이 된다. `collections.deque`는 내부적으로 양방향 연결된 블록 구조로 구현되어 있어 양쪽 끝 모두에서 삽입·삭제가 O(1)이므로, 큐가 필요하면 `list`가 아니라 `deque`를 쓰는 것이 표준적인 선택이다.

```python
from collections import deque
import time


class Stack:
    """스택: LIFO. list.append/pop은 둘 다 끝에서 동작해 O(1)이다."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("빈 스택에서 pop을 호출했다")
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0


class ListQueue:
    """list로 구현한 큐: dequeue가 pop(0)이라 앞의 모든 요소를 당겨야 해 O(n)이다."""

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)      # O(1)

    def dequeue(self):
        return self._items.pop(0)     # O(n), 비효율적

    def is_empty(self):
        return len(self._items) == 0


class DequeQueue:
    """collections.deque로 구현한 큐: 양쪽 끝 모두 O(1)이다."""

    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)       # O(1)

    def dequeue(self):
        return self._items.popleft()   # O(1)

    def is_empty(self):
        return len(self._items) == 0


def compare_queue_performance(n=20_000):
    """list 기반 큐와 deque 기반 큐의 dequeue 성능을 비교한다."""
    list_queue = ListQueue()
    deque_queue = DequeQueue()
    for i in range(n):
        list_queue.enqueue(i)
        deque_queue.enqueue(i)

    start = time.perf_counter()
    while not list_queue.is_empty():
        list_queue.dequeue()
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    while not deque_queue.is_empty():
        deque_queue.dequeue()
    deque_time = time.perf_counter() - start

    print(f"list 기반 큐: {list_time:.4f}초")
    print(f"deque 기반 큐: {deque_time:.4f}초 (약 {list_time / deque_time:.0f}배 빠름)")


if __name__ == "__main__":
    compare_queue_performance()
```

같은 Python 3.13.5, Windows 환경에서 원소 20,000개를 넣고 전부 꺼내는 시간을 측정하면 `list` 기반 큐는 약 0.0220초, `deque` 기반 큐는 약 0.0021초로 `deque`가 약 10배 빨랐다. 원소 수가 늘어날수록 `list.pop(0)`의 O(n) 비용이 누적되어 이 격차는 더 벌어지므로, 큐가 필요한 코드에서 `list`를 쓰고 있다면 `deque`로 바꾸는 것만으로도 눈에 띄는 성능 개선을 얻을 수 있다.

<strong>이진 탐색 트리(Binary Search Tree, BST)</strong>는 모든 노드에 대해 "왼쪽 서브트리의 값은 노드보다 작고, 오른쪽 서브트리의 값은 노드보다 크다"는 불변식을 유지하는 트리로, 이 불변식 덕분에 특정 값을 찾을 때 매 단계 왼쪽 또는 오른쪽 서브트리 하나를 통째로 배제할 수 있어 삽입·탐색이 평균 O(log n)이다. 다만 이 O(log n)은 트리가 좌우로 어느 정도 균형 잡혀 있다는 전제에서만 성립하며, 이미 정렬된 데이터를 순서대로 삽입하면 모든 노드가 오른쪽 자식만 갖는 사슬 형태(편향 트리)가 되어 사실상 연결 리스트와 같은 O(n)으로 나빠진다. 이 문제를 구조적으로 해결하는 것이 삽입·삭제 시 스스로 균형을 재조정하는 AVL 트리, 레드-블랙 트리 같은 <strong>자가 균형 이진 탐색 트리(self-balancing BST)</strong>이며, 이 챕터에서는 균형 유지 로직까지는 다루지 않고 기본 BST의 구조와 한계를 이해하는 데 초점을 둔다.

```python
class BSTNode:
    """이진 탐색 트리의 노드."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """이진 탐색 트리: 왼쪽 < 루트 < 오른쪽 불변식을 유지한다. 평균 O(log n), 편향 시 최악 O(n)."""

    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = BSTNode(value)
            return
        self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = BSTNode(value)
            else:
                self._insert(node.right, value)

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self._search(node.left, value)
        return self._search(node.right, value)

    def inorder(self):
        """중위 순회: 오름차순으로 정렬된 값을 반환한다."""
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.value)
        self._inorder(node.right, result)


if __name__ == "__main__":
    bst = BinarySearchTree()
    for value in [5, 3, 8, 1, 4, 7, 9]:
        bst.insert(value)

    print(bst.inorder())   # [1, 3, 4, 5, 7, 8, 9]
    print(bst.search(7))   # True
    print(bst.search(6))   # False
```

### 연산별 시간복잡도 한눈에 보기

앞서 다룬 알고리즘과 자료구조의 대표 연산을 표기법 기준으로 정리하면 다음과 같다. 값은 모두 점근적(asymptotic) 표기이며, 딕셔너리처럼 해시 기반 구조의 "최악"은 극히 드문 해시 충돌 상황을 가정한 것으로 실무에서는 사실상 평균 성능만 신경 쓰면 된다.

| 알고리즘/자료구조 | 연산 | 평균 | 최악 | 비고 |
|---|---|---|---|---|
| 병합 정렬 | 정렬 | O(n log n) | O(n log n) | 항상 일정, 추가 공간 O(n) |
| 퀵 정렬 (본문 구현) | 정렬 | O(n log n) | O(n²) | 피벗이 한쪽으로 치우치면 저하 |
| `sorted()` / Timsort | 정렬 | O(n log n) | O(n log n) | 적응형·안정 정렬, C 구현 |
| 선형 탐색 | 탐색 | O(n) | O(n) | 정렬 불필요 |
| 이진 탐색 / `bisect` | 탐색 | O(log n) | O(log n) | 정렬된 데이터 필수 |
| `list.append()` | 끝에 삽입 | O(1) 상각 | O(n) | 재할당 시에만 O(n) |
| `list.insert(0, x)` / `pop(0)` | 앞에 삽입/삭제 | O(n) | O(n) | 뒤 요소 전체 이동 |
| `collections.deque` | 양끝 삽입/삭제 | O(1) | O(1) | 큐 구현에 표준적 선택 |
| 연결 리스트 | 앞 삽입/삭제 | O(1) | O(1) | 탐색은 O(n) |
| 연결 리스트 | 값 탐색 | O(n) | O(n) | 인덱스 접근도 O(n) |
| `dict` (해시 테이블) | 삽입/조회 | O(1) | O(n) | 최악은 해시 충돌 시 |
| 이진 탐색 트리 | 삽입/탐색 | O(log n) | O(n) | 편향 시 연결 리스트와 동일 |
| BFS/DFS | 그래프 전체 순회 | O(V + E) | O(V + E) | V=정점 수, E=간선 수 |
| 다익스트라(heapq) | 최단 경로 | O((V+E) log V) | O((V+E) log V) | 음수 가중치 불가 |
| 동전 교환 DP | 최소 동전 개수 | O(amount × 동전 종류) | 동일 | 타뷸레이션 기준 |

### 실전 문제 해결: 스택과 큐로 실무 문제 풀기

스택과 큐는 추상적인 개념이 아니라 특정 형태의 문제를 자연스럽게 표현하는 도구다. **괄호 짝 검사**는 스택이 가장 먼저 등장하는 고전적인 예로, 여는 괄호를 만나면 스택에 쌓아두고 닫는 괄호를 만나면 스택 맨 위(가장 최근에 열린 괄호)와 짝이 맞는지 확인하는 방식이 문제의 "가장 최근에 열린 것부터 닫혀야 한다"는 구조와 정확히 일치하기 때문에 성립한다.

```python
def is_balanced(expression):
    """괄호 짝이 맞는지 스택으로 검사한다. 여는 괄호는 push, 닫는 괄호는 짝을 pop해서 확인한다."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []

    for char in expression:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack.pop() != pairs[char]:
                return False

    return not stack


if __name__ == "__main__":
    print(is_balanced("(a[b]{c})"))   # True
    print(is_balanced("(a[b)c]"))     # False, 괄호가 교차됨
    print(is_balanced("((a)"))        # False, 짝이 부족함
```

큐가 자연스러운 문제는 "가까운 것부터 순서대로 퍼뜨려 나가는" 탐색이다. 그래프를 인접 리스트(각 노드가 자신과 연결된 이웃 목록을 갖는 딕셔너리)로 표현하면, <strong>너비 우선 탐색(BFS)</strong>은 큐에서 노드를 하나 꺼내 방문 처리하고 그 이웃을 모두 큐에 넣는 과정을 반복해 시작점에서 가까운 노드부터 차례로 방문한다. 전체 정점과 간선을 한 번씩만 보므로 시간 복잡도는 O(V + E)다.

```python
from collections import deque


def bfs(graph, start):
    """인접 리스트로 표현된 그래프를 너비 우선 탐색한다 (O(V + E))."""
    visited = {start}
    order = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


if __name__ == "__main__":
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D"],
        "D": ["B", "C", "E"],
        "E": ["D"],
    }
    print(bfs(graph, "A"))   # ['A', 'B', 'C', 'D', 'E']
```

### 확장 학습: 가중 그래프의 최단 경로와 동적 계획법

간선마다 비용(가중치)이 다른 그래프에서 최단 경로를 구할 때는 BFS만으로 부족하다. **다익스트라(Dijkstra) 알고리즘**은 "지금까지 알려진 가장 가까운 미방문 노드부터 확정한다"는 탐욕적 전략을 쓰며, 매 단계 가장 짧은 거리의 노드를 빠르게 꺼내기 위해 표준 라이브러리 `heapq`(최소 힙)를 활용하면 O((V+E) log V)에 전체를 계산할 수 있다. 다만 이 알고리즘은 간선 가중치가 모두 0 이상이라는 전제에서만 정확하며, 음수 가중치가 있으면 벨만-포드 알고리즘 같은 다른 접근이 필요하다는 점을 기억해야 한다.

```python
import heapq


def dijkstra(graph, start):
    """가중치 그래프에서 start로부터 각 노드까지의 최단 거리를 구한다 (O((V+E) log V))."""
    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, node = heapq.heappop(pq)
        if current_dist > distances[node]:
            continue  # 이미 더 짧은 경로로 처리된 노드는 건너뛴다

        for neighbor, weight in graph[node]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances


if __name__ == "__main__":
    weighted_graph = {
        "A": [("B", 4), ("C", 1)],
        "B": [("D", 1)],
        "C": [("B", 2), ("D", 5)],
        "D": [],
    }
    print(dijkstra(weighted_graph, "A"))   # {'A': 0, 'B': 3, 'C': 1, 'D': 4}
```

<strong>동적 계획법(Dynamic Programming, DP)</strong>은 큰 문제를 겹치는 더 작은 하위 문제로 쪼갤 수 있고(**중복 부분 문제**), 하위 문제의 최적해를 조합하면 전체 최적해가 나올 때(**최적 부분 구조**) 적용할 수 있는 기법으로, 이미 계산한 하위 문제의 답을 저장해 재계산을 피하는 것이 핵심이다. 재귀 호출 결과를 캐시에 저장하는 방식을 **메모이제이션(memoization, 하향식)**, 가장 작은 하위 문제부터 반복문으로 차곡차곡 채워 올라가는 방식을 <strong>타뷸레이션(tabulation, 상향식)</strong>이라 부른다. 동전 교환 문제(주어진 동전 종류로 특정 금액을 만드는 최소 동전 개수)는 "금액 `k`를 만드는 최소 동전 수는, 각 동전 `c`에 대해 `k-c`를 만드는 최소 동전 수에 1을 더한 값 중 최솟값"이라는 최적 부분 구조가 성립하므로 타뷸레이션으로 풀 수 있다.

```python
def coin_change(coins, amount):
    """최소 동전 개수 문제를 타뷸레이션(상향식 DP)으로 푼다 (O(amount * len(coins)))."""
    dp = [0] + [float("inf")] * amount

    for target in range(1, amount + 1):
        for coin in coins:
            if coin <= target and dp[target - coin] + 1 < dp[target]:
                dp[target] = dp[target - coin] + 1

    return dp[amount] if dp[amount] != float("inf") else -1


if __name__ == "__main__":
    print(coin_change([1, 3, 4], 6))   # 2, (3 + 3)
    print(coin_change([2], 3))         # -1, 홀수 금액은 짝수 동전으로 불가능
```

이 챕터는 자료구조·그래프·DP의 핵심 사고방식을 다루는 데 집중했고, 문자열 패턴 매칭(KMP, 라빈-카프, 보이어-무어), 최소 신장 트리(크루스칼, 프림), 세그먼트 트리·펜윅 트리 같은 구간 쿼리 자료구조, 유전 알고리즘 같은 메타휴리스틱은 의도적으로 범위 밖에 두었다. 이 영역들은 대체로 특정 문제 유형(대량 텍스트 검색, 네트워크 설계, 구간 합 갱신, NP-hard 근사)에 특화되어 있어 필요할 때 개별적으로 학습하는 편이 효율적이며, 유클리드 호제법으로 최대공약수를 구하는 것처럼 자주 쓰이는 수학적 계산은 직접 구현하기보다 표준 라이브러리(`math.gcd`, `functools.reduce`)를 먼저 확인하는 것이 이 챕터 전체를 관통하는 "표준 라이브러리 우선" 원칙에 맞는다.

## 실습 프로젝트

### 프로젝트 1: 역색인 기반 간이 검색 엔진

검색 엔진의 핵심 아이디어는 문서를 순서대로 훑는 대신, "단어 → 그 단어를 포함한 문서 ID 목록"을 미리 만들어 두는 <strong>역색인(inverted index)</strong>이다. 문서가 추가될 때마다 단어별로 딕셔너리에 문서 ID를 저장해 두면, 검색 시에는 문서 전체를 다시 읽을 필요 없이 딕셔너리 조회와 집합 연산만으로 결과를 얻을 수 있다. 아래 구현은 공백으로 구분된 여러 단어를 모두 포함하는 문서를 집합의 교집합(AND 검색)으로 찾는다.

```python
from collections import defaultdict


class SearchEngine:
    """단어-문서 역색인을 만들어 다중 단어 AND 검색을 지원하는 간이 검색 엔진."""

    def __init__(self):
        self.index = defaultdict(set)
        self.documents = {}

    def add_document(self, doc_id, text):
        """문서를 색인에 추가한다. 단어별로 문서 ID 집합을 유지한다."""
        self.documents[doc_id] = text
        for word in set(text.lower().split()):
            self.index[word].add(doc_id)

    def search(self, query):
        """공백으로 구분된 모든 단어를 포함하는 문서 ID를 교집합으로 찾는다."""
        words = query.lower().split()
        if not words:
            return set()

        result = self.index.get(words[0], set()).copy()
        for word in words[1:]:
            result &= self.index.get(word, set())
        return result


if __name__ == "__main__":
    engine = SearchEngine()
    engine.add_document(1, "python is a great programming language")
    engine.add_document(2, "java is also a programming language")
    engine.add_document(3, "python is easy to learn")

    print(engine.search("python programming"))    # {1}
    print(engine.search("programming language"))  # {1, 2}
```

### 프로젝트 2: 다익스트라 기반 내비게이션 최단 경로

실무의 최단 경로 문제는 거리뿐 아니라 실제 경로도 함께 요구하는 경우가 많다. 위에서 구현한 `dijkstra` 함수를 확장해, 각 노드에 도달할 때 "어느 노드에서 왔는지"를 함께 기록해 두면 목적지에서부터 역추적해 전체 경로를 복원할 수 있다.

```python
import heapq


def shortest_path(graph, start, end):
    """다익스트라로 최단 거리와 실제 경로를 함께 구한다."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, node = heapq.heappop(pq)
        if node == end:
            break
        if current_dist > distances[node]:
            continue

        for neighbor, weight in graph[node]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = node
                heapq.heappush(pq, (distance, neighbor))

    if distances[end] == float("inf"):
        return None, float("inf")

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return path, distances[end]


if __name__ == "__main__":
    city_map = {
        "서울": [("대전", 140), ("강릉", 200)],
        "대전": [("서울", 140), ("대구", 150)],
        "강릉": [("서울", 200), ("대구", 220)],
        "대구": [("대전", 150), ("강릉", 220), ("부산", 90)],
        "부산": [("대구", 90)],
    }
    path, distance = shortest_path(city_map, "서울", "부산")
    print(f"경로: {' -> '.join(path)}, 총 거리: {distance}km")
    # 경로: 서울 -> 대전 -> 대구 -> 부산, 총 거리: 380km
```

## 체크리스트

- [ ] 임의의 알고리즘 코드를 보고 최선/평균/최악 시간 복잡도를 구분해 설명할 수 있다
- [ ] 정렬이 필요한 상황에서 직접 구현 대신 `sorted()`를 먼저 고려해야 하는 이유를 실측 근거와 함께 설명할 수 있다
- [ ] 큐를 구현할 때 `list` 대신 `collections.deque`를 선택해야 하는 이유를 시간 복잡도로 설명할 수 있다
- [ ] 연결 리스트, 스택/큐, 이진 탐색 트리 중 주어진 문제에 어떤 자료구조가 적합한지 판단할 수 있다
- [ ] 스택과 큐 중 어느 쪽이 주어진 문제(괄호 검사, 너비 우선 탐색 등)에 적합한지 구조적 근거를 들어 선택할 수 있다

## 다음 단계
알고리즘과 자료구조의 복잡도 분석과 직접 구현 능력을 갖췄다면, [28. 프로젝트 아키텍처](/post/python/python-project-architecture-layered-clean-architecture-guide/)로 넘어가 이 지식을 대규모 프로젝트 구조 설계에 적용하는 방법을 학습합니다.
