---
image: "wordcloud.png"
slug: searching-algorithms
collection_order: 41
draft: false
title: "[Computer Terms] 탐색 알고리즘 (Searching Algorithms)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "선형 탐색과 이진 탐색의 시간 복잡도를 비교하고, 이진 탐색이 정렬된 데이터를 전제로 하는 이유를 구간 배제 논리로 설명하며, 실무에서 흔한 오프바이원·오버플로 버그를 컴파일 가능한 C 코드와 종료 조건·중간값 계산·경계 갱신별 비교표로 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Algorithm(알고리즘)
- Searching(탐색)
- Binary-Search(이진탐색)
- Linear-Search(선형탐색)
- Time-Complexity(시간복잡도)
- C
- Off-by-One(오프바이원)
- Precondition(전제조건)
- Sorted-Array(정렬된배열)
- Divide-and-Conquer(분할정복)
- Computer-Science(컴퓨터과학)
- Data-Structure(자료구조)
- Debugging(디버깅)
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

이 챕터는 [정렬 알고리즘](/post/computerterms/sorting-algorithms/)과 [시간 복잡도](/post/computerterms/time-complexity/)를 먼저 읽었다고 가정한다. 정렬된 배열이 무엇인지, 빅오 표기법이 무엇을 뜻하는지 안다면 바로 진행해도 좋다. 해시테이블 기반 탐색(평균 O(1))은 [해시테이블](/post/computerterms/hash-tables/) 챕터에서 이미 다뤘으므로 여기서는 다루지 않고, 배열에서의 비교 기반 탐색만 다룬다.

## 왜 탐색을 정렬 다음에 배우는가

탐색은 정렬과 뗄 수 없는 짝이다. 데이터를 정렬해두는 이유의 상당 부분이 "이후에 더 빠르게 찾기 위해서"다. 정렬에 O(n log n)을 투자하고 나면, 탐색은 O(n)에서 O(log n)으로 줄어든다. 이 교환 관계를 이해해야 "매번 몇 번 조회할 데이터인가"에 따라 정렬을 미리 해둘지, 그냥 순서대로 훑을지를 판단할 수 있다.

## 선형 탐색: 정렬이 필요 없는 기본형

**선형 탐색(Linear Search)**은 배열의 첫 원소부터 끝까지 하나씩 확인하며 찾는 값과 일치하는지 비교하는 가장 단순한 탐색이다. 정렬 여부와 무관하게 항상 동작하며, 최악의 경우(찾는 값이 마지막에 있거나 없는 경우) O(n)의 비교가 필요하다. 구현이 단순하고 정렬 비용이 없다는 장점 때문에, 데이터가 작거나 한 번만 조회할 경우에는 오히려 선형 탐색이 정렬 비용까지 포함한 총 비용에서 더 유리하다.

## 이진 탐색: 정렬을 전제로 한 O(log n)

**이진 탐색(Binary Search)**은 정렬된 배열의 중간 원소와 찾는 값을 비교해, 찾는 값이 더 작으면 왼쪽 절반을, 더 크면 오른쪽 절반을 다시 탐색하는 과정을 반복한다. 매 비교마다 탐색 범위가 절반으로 줄어들므로 O(log n)에 끝난다. 이 알고리즘이 **정렬된 데이터를 전제로 하는 이유**는 명확하다 — "중간값보다 작으면 왼쪽에 있다"는 판단 자체가 왼쪽 구간의 모든 값이 중간값보다 작다는 정렬 성질에 의존하기 때문이다. 정렬되지 않은 배열에 이진 탐색을 적용하면 찾는 값이 실제로는 배제한 구간에 있을 수 있어, 잘못된 "없음" 결과를 낼 수 있다.

다음은 이진 탐색의 반복문 기반 구현이다. `low`, `high`가 현재 탐색 구간의 양 끝 인덱스를 가리키고, `mid`가 중간 인덱스를 가리킨다.

```c
#include <stdio.h>

int binary_search(const int arr[], int n, int target) {
    int low = 0, high = n - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2;   /* (low+high)/2 대신 오버플로 방지 */

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;   /* 찾지 못함 */
}

int main(void) {
    int arr[] = {1, 3, 5, 7, 9, 11, 13};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("index of 7: %d\n", binary_search(arr, n, 7));    /* 3 */
    printf("index of 4: %d\n", binary_search(arr, n, 4));    /* -1 */
    return 0;
}
```

`low = mid + 1`, `high = mid - 1`처럼 `mid` 자체를 다음 구간에서 제외하는 것이 중요하다. 이 코드는 `gcc -std=c11 -Wall binary_search.c -o binary_search`로 컴파일·실행할 수 있으며, 반복문마다 구간이 정확히 절반씩 줄어드는 것을 `low`, `high` 값을 출력해 직접 확인할 수 있다.

## 실무에서 흔한 오프바이원 버그

이진 탐색은 알고리즘 자체는 단순하지만, 구현 시 **오프바이원(Off-by-One) 버그**가 잦기로 악명 높다. 대표적인 실수는 세 가지다. 첫째, 종료 조건을 `low < high`로 쓰면 `low == high`인 마지막 원소 하나가 남은 구간을 검사하지 못하고 종료된다 — 올바른 조건은 `low <= high`다. 둘째, `mid = (low + high) / 2`는 `low`, `high`가 매우 큰 정수일 때 덧셈에서 정수 오버플로가 날 수 있다 — `low + (high - low) / 2`로 쓰면 이를 피할 수 있다. 셋째, 값을 찾은 뒤 `low = mid`로 갱신하면(마이너스 1을 빼먹으면) 같은 `mid`가 무한히 재검사되어 무한 루프에 빠질 수 있다. Bentley(1986)는 이진 탐색이 "개념은 간단하지만 정확히 구현하기는 놀라울 정도로 어렵다"고 지적했다. 이 지적을 뒷받침하는 유명한 사례로, Bloch(2006)는 자바 표준 라이브러리와 여러 교과서에 실린 이진 탐색 구현 다수가 `(low + high) / 2`의 정수 오버플로 버그를 20년 넘게 포함하고 있었다고 밝혔다.

## 비교: 무엇이 다르고, 언제 무엇을 쓰는가

| 항목 | 선형 탐색 | 이진 탐색 |
|---|---|---|
| 전제 조건 | 없음 | 정렬된 배열 |
| 시간 복잡도 | O(n) | O(log n) |
| 구현 난이도 | 낮음 | 오프바이원 위험 있음 |
| 삽입·삭제 후 재탐색 | 추가 비용 없음 | 정렬 상태 유지 비용 필요 |
| 유리한 상황 | 데이터가 작거나 한 번만 조회 | 데이터가 크고 반복 조회 |

이 표에서 실무 판단의 핵심은 **"몇 번 조회할 것인가"**다. 정렬에는 O(n log n) 비용이 들기 때문에, 배열을 딱 한 번만 조회하고 버릴 것이라면 정렬 비용까지 합친 총 비용은 선형 탐색(O(n))이 더 낮다. 반대로 같은 배열을 여러 번 반복 조회한다면, 최초 한 번의 정렬 비용을 여러 번의 탐색으로 상각(Amortize)할 수 있어 이진 탐색이 유리해진다.

## 흔한 오개념

**"이진 탐색은 정렬된 배열이면 항상 이진 탐색이 가장 빠르다"** — 배열이 매우 작으면(대략 원소 10개 이하) 캐시 지역성과 분기 예측 덕분에 선형 탐색이 실측으로 더 빠른 경우가 많다. 이진 탐색은 매 단계마다 예측하기 어려운 분기(`mid` 값에 따라 왼쪽/오른쪽 결정)를 타므로 CPU 파이프라인 관점에서 불리하고, 원소 수가 적으면 O(log n)과 O(n)의 실제 비교 횟수 차이가 거의 없다.

**"정렬만 되어 있으면 이진 탐색을 아무 자료구조에나 쓸 수 있다"** — 이진 탐색은 임의 접근(인덱스로 O(1) 접근)을 전제로 한다. [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)에서 다뤘듯 연결리스트는 인덱스 접근이 O(n)이므로, 정렬된 연결리스트에 "중간으로 건너뛰기"를 시도하면 그 자체가 O(n)이 되어 이진 탐색의 이점이 사라진다. 정렬된 연결리스트를 빠르게 탐색하려면 [트리](/post/computerterms/trees/) 챕터에서 다룬 이진 탐색 트리 같은 별도 구조가 필요하다.

## 다른 개념과의 연결

이진 탐색의 "탐색 범위를 절반으로 줄인다"는 아이디어는 [정렬 알고리즘](/post/computerterms/sorting-algorithms/)의 병합정렬·퀵정렬이 쓰는 분할정복과 본질적으로 같은 패턴이다. 값을 임의 접근으로 찾는다는 점에서 [해시테이블](/post/computerterms/hash-tables/)의 평균 O(1) 탐색과도 자주 비교되는데, 해시테이블은 순서 정보를 포기하는 대신 더 빠른 탐색을 얻는 트레이드오프를 가진다. 다음 챕터에서는 탐색을 "값 하나 찾기"에서 "그래프에서 가장 짧은 경로 찾기"로 확장한 **최단 경로 알고리즘**을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 선형 탐색과 이진 탐색 중 데이터 크기와 조회 빈도에 따라 어느 쪽이 총 비용 관점에서 유리한지 설명할 수 있다. 이진 탐색이 정렬된 데이터를 전제로 하는 이유를 왼쪽/오른쪽 구간 배제 논리로 설명할 수 있다. 이진 탐색 구현에서 종료 조건·중간값 계산·경계 갱신 중 어디서 오프바이원 버그가 생기는지 찾아 고칠 수 있다.

## 참고 자료

> Bentley, J. (1986). *Programming Pearls*, Column 4: Writing Correct Programs. Addison-Wesley. — 이진 탐색 구현의 오프바이원·오버플로 버그 사례를 다룬 고전.

- [Bloch, J. (2006). "Extra, Extra – Read All About It: Nearly All Binary Searches and Mergesorts are Broken." Google Research Blog](https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/) — `(low+high)/2` 오버플로 버그가 실제 라이브러리 구현에 20년 넘게 존재했던 사례
- [Visualgo: Sorting](https://visualgo.net/en/sorting) — 정렬 알고리즘 시각화 도구(이진 탐색이 전제하는 정렬된 배열 상태를 시각적으로 확인 가능)
- [cppreference: std::binary_search](https://en.cppreference.com/w/cpp/algorithm/binary_search) — 표준 라이브러리 이진 탐색의 전제 조건과 반환값 규약
