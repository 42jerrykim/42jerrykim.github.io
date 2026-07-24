---
image: "wordcloud.png"
slug: sorting-algorithms
collection_order: 40
draft: false
title: "[Computer Terms] 정렬 알고리즘 (Sorting Algorithms)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "버블·삽입·선택정렬 같은 O(n²) 단순 정렬과 병합·퀵정렬 같은 O(n log n) 분할정복 정렬을 비교하고, 안정 정렬 개념과 퀵정렬 최악의 경우를 C 코드로 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Algorithm(알고리즘)
- Sorting(정렬)
- Quicksort(퀵정렬)
- Merge-Sort(병합정렬)
- Bubble-Sort(버블정렬)
- Insertion-Sort(삽입정렬)
- Selection-Sort(선택정렬)
- Stable-Sort(안정정렬)
- Divide-and-Conquer(분할정복)
- Time-Complexity(시간복잡도)
- C
- Recursion(재귀)
- Worst-Case(최악의경우)
- Pivot(피벗)
- Computer-Science(컴퓨터과학)
- Data-Structure(자료구조)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Fundamentals(기초)
- Comparison(비교)
- Case-Study
- Software-Engineering(소프트웨어공학)
- Performance(성능)
- Implementation(구현)
---

## 이 장을 읽기 전에

이 챕터는 [시간 복잡도](/post/computerterms/time-complexity/)의 빅오 표기법과 [알고리즘 분류](/post/computerterms/algorithm-classification/)에서 다룬 분할정복(Divide and Conquer) 개념을 이미 안다고 가정한다. 재귀 함수를 읽고 쓸 수 있어야 병합정렬·퀵정렬의 동작을 따라갈 수 있다. 정렬 자체의 응용(데이터베이스 인덱스, 다음 챕터의 이진 탐색 전제 조건)은 다루지만, 정렬 네트워크나 병렬 정렬 같은 고급 주제는 범위 밖이며 여기서 다루지 않는다.

## 왜 정렬이 알고리즘의 시작점인가

정렬은 데이터를 특정 순서로 재배열하는, 실무에서 가장 자주 마주치는 연산이다. 데이터베이스의 `ORDER BY`, 검색 결과 랭킹, 다음 챕터에서 다룰 이진 탐색의 전제 조건이 모두 정렬에 의존한다. 그런데 같은 "정렬"이라는 문제를 푸는 방법은 알고리즘마다 시간 복잡도가 완전히 다르다 — 원소가 10개일 때는 체감이 안 되지만, 100만 개가 되면 O(n²) 알고리즘과 O(n log n) 알고리즘의 실행 시간 차이는 초 단위에서 시간 단위로 벌어진다. 이 챕터는 그 차이가 어디서 오는지를 다룬다.

## 단순 정렬: 버블·삽입·선택정렬

**버블정렬(Bubble Sort)**은 인접한 두 원소를 비교해 순서가 틀리면 교환하는 과정을 배열 끝까지 반복하고, 이를 배열 전체에 대해 다시 반복한다. 한 번 순회할 때마다 가장 큰(또는 작은) 원소가 거품처럼 끝으로 이동하는 모습에서 이름이 붙었다. **선택정렬(Selection Sort)**은 매 단계마다 정렬되지 않은 구간에서 최솟값을 찾아 맨 앞과 교환한다. **삽입정렬(Insertion Sort)**은 이미 정렬된 앞부분에 새 원소를 알맞은 위치에 끼워 넣는 방식으로, 카드를 손에서 정렬하는 방식과 유사하다.

세 알고리즘 모두 이중 반복문 구조라 최악의 경우 O(n²)이다. 다만 삽입정렬은 데이터가 이미 거의 정렬된 상태(Nearly Sorted)라면 안쪽 반복문이 일찍 끝나 O(n)에 가까운 성능을 낸다 — 이 특성 때문에 실무 라이브러리 정렬(예: Timsort)은 작은 구간이나 부분 정렬된 데이터에 삽입정렬을 보조 알고리즘으로 섞어 쓴다.

## 분할정복 정렬: 병합정렬과 퀵정렬

**병합정렬(Merge Sort)**은 배열을 절반으로 계속 나누어(분할) 원소가 하나 남을 때까지 쪼갠 뒤, 두 정렬된 절반을 하나로 합치는(정복) 과정을 재귀적으로 반복한다. 분할은 O(log n)번 일어나고, 매 분할 단계마다 병합에 O(n)이 걸리므로 전체는 O(n log n)이다. 병합 과정에서 왼쪽·오른쪽 원소 중 같은 값이 있으면 항상 왼쪽(원래 순서상 앞) 원소를 먼저 넣도록 구현하면, 원래 순서가 유지되는 **안정 정렬(Stable Sort)**이 된다.

**안정 정렬**이란 정렬 기준 값이 같은 두 원소의 상대적 순서가 정렬 후에도 유지되는 성질이다. 예를 들어 이름순으로 이미 정렬된 학생 명단을 점수 기준으로 다시 정렬할 때, 안정 정렬이면 점수가 같은 학생들은 여전히 이름순으로 나열된다. 이 성질은 다중 기준 정렬(1차: 점수, 2차: 이름)을 구현할 때 실질적인 차이를 만든다.

다음은 병합정렬의 컴파일 가능한 구현이다. `merge` 함수가 두 정렬된 구간을 하나로 합치는 핵심 로직이며, `merge_sort`는 배열을 절반으로 나누어 재귀 호출한다.

```c
#include <stdio.h>
#include <stdlib.h>

void merge(int arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    int *L = malloc(n1 * sizeof(int));
    int *R = malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {   /* <= 를 써야 안정 정렬이 된다 */
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    free(L);
    free(R);
}

void merge_sort(int arr[], int left, int right) {
    if (left >= right) return;   /* 원소가 1개 이하면 이미 정렬됨 */
    int mid = left + (right - left) / 2;
    merge_sort(arr, left, mid);
    merge_sort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

int main(void) {
    int arr[] = {5, 2, 8, 1, 9, 3};
    int n = sizeof(arr) / sizeof(arr[0]);

    merge_sort(arr, 0, n - 1);

    for (int i = 0; i < n; i++) printf("%d ", arr[i]);
    printf("\n");   /* 1 2 3 5 8 9 */
    return 0;
}
```

`L[i] <= R[j]` 조건에서 등호를 포함한 것이 안정 정렬의 핵심이다. 왼쪽 값이 같을 때도 오른쪽보다 먼저 넣으므로, 원래 왼쪽 구간에 있던 원소의 상대 순서가 보존된다. 이 코드는 `gcc -std=c11 -Wall merge_sort.c -o merge_sort`로 컴파일·실행할 수 있으며, 병합 단계에서 임시 배열 `L`, `R`을 쓰기 때문에 O(n) 추가 공간이 필요하다.

**퀵정렬(Quicksort)**은 배열에서 피벗(Pivot)을 하나 고른 뒤, 피벗보다 작은 원소는 왼쪽에, 큰 원소는 오른쪽에 모으는 파티션(Partition) 작업을 하고, 양쪽 구간을 재귀적으로 정렬한다. 평균적으로 파티션이 배열을 절반씩 나누면 O(n log n)이지만, **피벗을 항상 최솟값 또는 최댓값으로 고르면 한쪽 구간이 텅 비고 다른 쪽에 n-1개가 남는 불균형 분할이 반복**되어 최악의 경우 O(n²)로 떨어진다. 이미 정렬된 배열에서 항상 첫 원소를 피벗으로 고르는 구현이 이 최악의 경우의 대표적 예다. 실무 구현은 피벗을 무작위로 고르거나(Randomized Quicksort), 처음·중간·끝 값의 중앙값을 쓰는 방식(Median-of-Three)으로 이 최악의 경우가 발생할 확률을 낮춘다.

## 비교: 무엇이 다르고, 언제 무엇을 쓰는가

| 알고리즘 | 평균 시간 | 최악 시간 | 추가 공간 | 안정성 |
|---|---|---|---|---|
| 버블정렬 | O(n²) | O(n²) | O(1) | 안정 |
| 선택정렬 | O(n²) | O(n²) | O(1) | 불안정 |
| 삽입정렬 | O(n²) | O(n²) | O(1) | 안정 |
| 병합정렬 | O(n log n) | O(n log n) | O(n) | 안정 |
| 퀵정렬 | O(n log n) | O(n²) | O(log n) (스택) | 불안정 |

이 표에서 실무 판단에 가장 중요한 것은 **퀵정렬의 최악 시간과 병합정렬의 안전성 트레이드오프**다. 퀵정렬은 평균적으로 병합정렬보다 상수 인자가 작아 실측 속도가 더 빠르고 제자리(In-place)에 가깝게 동작해 공간도 적게 쓰지만, 입력이 적대적으로 구성되면(또는 피벗 선택이 나쁘면) O(n²)로 떨어질 위험이 있다. 반면 병합정렬은 최악의 경우에도 O(n log n)을 보장하고 안정 정렬이라, 대용량 외부 정렬이나 안정성이 필요한 다중 기준 정렬에 적합하다.

## 흔한 오개념

**"정렬 알고리즘은 다 O(n log n)이 최선이니 아무거나 골라도 성능은 비슷하다"** — 비교 기반 정렬의 이론적 하한이 O(n log n)인 것은 맞지만, 이는 점근적 하한일 뿐 상수 인자·공간 사용·안정성까지 같다는 뜻이 아니다. 데이터가 거의 정렬된 상태라면 O(n²) 알고리즘인 삽입정렬이 실측으로 병합정렬보다 빠를 수 있고, 값의 범위가 작은 정수 배열이라면 비교 없이 세는 계수 정렬(Counting Sort)이 O(n)으로 이론 하한을 뛰어넘는다.

**"퀵정렬은 이름값 대로 항상 가장 빠르다"** — 평균적으로는 빠르지만, 피벗 선택이 나쁘면 최악의 경우 O(n²)로 버블정렬과 같은 등급까지 떨어진다. 이 최악의 경우가 실제로 문제가 되는 상황(예: 이미 정렬된 대용량 로그 파일을 재정렬)이 있기 때문에, 표준 라이브러리들은 순수 퀵정렬 대신 재귀 깊이가 임계값을 넘으면 힙정렬로 전환하는 Introsort 같은 하이브리드 알고리즘을 쓴다.

## 다른 개념과의 연결

퀵정렬의 파티션 로직은 [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)에서 다룬 임의 접근 O(1) 성질에 의존한다 — 연결리스트에서는 인덱스 접근이 O(n)이라 같은 방식의 파티션이 비효율적이다. 병합정렬의 분할정복 구조는 [시간 복잡도](/post/computerterms/time-complexity/) 챕터의 재귀 관계식(T(n) = 2T(n/2) + O(n))으로 O(n log n)이 유도되는 대표 사례다. 다음 챕터에서는 정렬된 데이터를 전제로 O(log n)에 원하는 값을 찾는 **탐색 알고리즘**을 다룬다 — 정렬 비용과 탐색 비용을 함께 저울질하는 것이 실무의 핵심 판단이다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. O(n²) 단순 정렬과 O(n log n) 분할정복 정렬 중 데이터 크기·정렬 상태에 따라 어느 쪽이 실측으로 유리한지 근거를 들어 설명할 수 있다. 안정 정렬이 왜 필요한지 다중 기준 정렬 예시로 설명할 수 있다. 퀵정렬의 최악의 경우가 언제 발생하는지, 그리고 이를 완화하는 피벗 선택 전략을 설명할 수 있다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Chapter 7: Quicksort, Chapter 8: Sorting in Linear Time. MIT Press.

- [Visualgo: Sorting](https://visualgo.net/en/sorting) — 버블·삽입·선택·병합·퀵정렬의 동작을 단계별로 시각화한 자료
- [Python docs: sorted() and Timsort](https://docs.python.org/3/howto/sorting.html) — 실무 표준 라이브러리 정렬(Timsort)이 삽입정렬을 보조로 쓰는 방식 설명
