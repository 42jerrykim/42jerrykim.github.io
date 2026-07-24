---
image: "wordcloud.png"
slug: algorithm-efficiency
collection_order: 2
draft: false
description: "알고리즘 효율성은 문제를 해결할 때 시간·공간 자원을 얼마나 적게 쓰는지를 판단하는 기준입니다. 시간 복잡도와 공간 복잡도를 나눠 분석하고, 최악·평균·최선의 경우를 빅오·빅오메가·빅세타 표기법으로 구분하는 방법을 실제 코드 예시와 함께 다룹니다."
title: "[Computer Terms] 알고리즘 효율성과 계산 복잡도 (Algorithm Efficiency)"
date: 2022-03-14
last_modified_at: 2026-07-22
categories: ComputerTerms
tags:
- Technology(기술)
- Education(교육)
- Algorithm(알고리즘)
- Time-Complexity(시간복잡도)
- Space-Complexity(공간복잡도)
- Complexity-Analysis(복잡도분석)
- Worst-Case(최악의경우)
- Graph(그래프)
- Computer-Science(컴퓨터과학)
- Data-Structure(자료구조)
- Problem-Solving(문제해결)
- Memory(메모리)
- Optimization(최적화)
- C
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Advanced
- Fundamentals(기초)
- Comparison(비교)
- Case-Study
- Software-Engineering(소프트웨어공학)
- Performance(성능)
- Implementation(구현)
---

## 이 장을 읽기 전에

이 챕터는 [알고리즘](/post/computerterms/algorithm/)에서 다룬 알고리즘의 정의와 효율성 성질을 전제로 한다. 여기서는 "효율적이다"라는 말이 구체적으로 무엇을 재는지, 어떻게 표기하는지를 다룬다. 바로 다음 챕터인 [알고리즘 분류](/post/computerterms/algorithm-classification/)는 효율성과 별개로 알고리즘을 주제·설계 기법별로 나누는 방법을 다루고, 점근적 표기법의 구체적 계산 규칙과 예시는 그 뒤를 잇는 [시간 복잡도](/post/computerterms/time-complexity/)에서 이어서 다룬다.

## 효율성은 왜 필요한가

컴퓨팅 자원은 항상 한정되어 있다. 계산 시간과 메모리 모두 유한한 자원이므로, 같은 문제를 푸는 여러 알고리즘이 있을 때 어느 것이 자원을 덜 쓰는지 판단할 척도가 필요하다. **알고리즘 효율성(Algorithm Efficiency)**은 이 자원 소비량의 많고 적음을 나타내는 개념으로, 소요량이 적을수록 효율적이고 좋은 알고리즘으로 평가한다. 효율성은 크게 두 관점으로 나뉜다. **시간 복잡도(Time Complexity)**는 알고리즘이 수행하는 기본 연산(비교, 덧셈, 곱셈, 나눗셈 등)의 횟수를 재고, **공간 복잡도(Space Complexity)**는 계산에 소요되는 메모리량을 잰다. 전통적으로는 시간 복잡도를 위주로 따졌지만, 대용량 데이터를 다루는 오늘날에는 공간 복잡도도 점차 중요해지고 있다. 이 두 관점을 종합해 알고리즘의 효율을 재는 척도를 **계산 복잡도(Computational Complexity)**라 부른다.

## 무엇을, 어떻게 분석하는가

효율성 분석의 목표는 알고리즘 실행에 필요한 시간과 공간을 측정하는 것이다. 분석 대상은 **입력 크기**(배열의 길이, 행렬의 항목 수, 그래프의 정점·간선 수 등)이며, 이 크기가 커짐에 따라 처리 시간(연산 수)과 소요 메모리가 얼마나 늘어나는지를 살핀다. 이 관계는 보통 입력 크기 n에 대한 함수 f(n) 형태의 다항식으로 표현하며, 이 함수는 특정 컴퓨터의 처리 속도나 프로그래밍 언어·스타일과는 무관하다 — 어떤 하드웨어에서 실행하든 "입력이 2배가 되면 연산 수가 몇 배가 되는가"라는 증가율 자체는 변하지 않기 때문이다.

같은 알고리즘이라도 입력의 배치(예: 이미 정렬된 배열인지 역순인지)에 따라 걸리는 시간이 달라질 수 있으므로, 분석은 보통 **최악의 경우(worst-case)**, **평균의 경우(average-case)**, **최선의 경우(best-case)** 세 시나리오로 나눠 이뤄진다. 이때 중요한 것은 알고리즘의 실행 시간을 초 단위로 정확히 재는 것이 아니라, 입력 크기가 커짐에 따라 소요 시간이 어떤 비율로 늘어나는지를 파악하는 것이다.

## 점근적 표기법: O, Ω, Θ

이 증가율을 수학적으로 표현하는 방법이 **점근적 표기법(Asymptotic Notation)**이다. 세 가지가 널리 쓰인다.

| 표기법 | 이름 | 의미 | 관례상 쓰이는 경우 |
|---|---|---|---|
| O(f(n)) | 빅오(Big-O) | 점근적 **상한선** — "이보다 느리게 증가하지 않는다" | 최악의 경우 분석 |
| Ω(f(n)) | 빅오메가(Big-Omega) | 점근적 **하한선** — "이보다 빠르게 증가하지 않는다" | 최선의 경우 분석 |
| Θ(f(n)) | 빅세타(Big-Theta) | 상한과 하한이 같은 차수로 만나는 **엄격한 점근 한계** | 평균 경우 분석 |

세 표기법 모두 수학적 정의 자체는 최악·평균·최선 중 어느 경우에도 적용할 수 있다는 점을 분명히 해둘 필요가 있다. 다음은 배열에서 특정 값을 선형 탐색하는 C 함수로, 최선의 경우(Ω(1), 첫 원소가 정답)와 최악의 경우(O(n), 값이 없거나 마지막에 있음)가 어떻게 갈리는지 보여준다.

```c
#include <stdio.h>

int linear_search(const int arr[], int n, int target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) {
            return i;   /* 최선의 경우: i == 0 이면 Ω(1) */
        }
    }
    return -1;          /* 최악의 경우: 끝까지 못 찾으면 O(n) */
}

int main(void) {
    int arr[] = {5, 3, 8, 1, 9};
    printf("index of 5: %d\n", linear_search(arr, 5, 5));   /* 0, 최선의 경우 */
    printf("index of 7: %d\n", linear_search(arr, 5, 7));   /* -1, 최악의 경우 */
    return 0;
}
```

`gcc -std=c11 -Wall linear_search.c -o linear_search`로 컴파일해, `target`을 배열의 첫 값(최선)과 배열에 없는 값(최악)으로 바꿔가며 비교 횟수가 어떻게 달라지는지 직접 셀 수 있다. 이 비교 횟수를 입력 크기 n의 함수로 일반화하는 구체적 계산 규칙(최고차항만 남기기, 계수 무시하기 등)은 [시간 복잡도](/post/computerterms/time-complexity/)에서 이어서 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 시간 복잡도와 공간 복잡도가 각각 무엇을 측정하는지 구분해 설명할 수 있다. 최악·평균·최선의 경우 분석이 왜 필요한지, 같은 알고리즘도 입력 배치에 따라 성능이 달라질 수 있는 예시로 설명할 수 있다. O, Ω, Θ 세 표기법의 수학적 의미 차이와 관례적 쓰임의 차이를 구분해 설명할 수 있다.

## 흔한 오개념

**"Big-O는 최악의 경우만을 뜻하는 표기법이다"** — Big-O(O)는 "이 함수보다 느리게 증가하지 않는다"는 점근적 **상한**을 뜻할 뿐, 최악/평균/최선 중 어느 경우를 분석하든 쓸 수 있는 수학적 표기법이다. 다만 실무에서 "이 알고리즘이 아무리 나빠도 이 정도 성능은 보장한다"는 안전 마진이 중요하므로 최악의 경우 분석에 O를 붙여 쓰는 관례가 굳어졌을 뿐이다. Ω(빅 오메가)를 최악의 경우에, O를 최선의 경우에 적용하는 것도 수학적으로는 유효하다.

**"시간 복잡도가 낮으면 항상 더 빠르다"** — [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)에서 다루듯, 점근적 표기법은 입력 크기가 충분히 클 때의 증가율만 비교한다. 상수 계수와 캐시 지역성 같은 실측 요인 때문에, 입력이 작을 때는 이론상 더 느린 O(n²) 알고리즘이 실제로는 O(n log n) 알고리즘보다 빠른 경우가 흔하다.

## 다른 개념과의 연결

이 챕터에서 다룬 점근적 표기법(O, Ω, Θ)의 구체적 계산 규칙과 예시는 [시간 복잡도](/post/computerterms/time-complexity/)에서, 효율성 분석의 상위 개념인 알고리즘 자체의 정의와 필수 특징은 [알고리즘](/post/computerterms/algorithm/)에서 다룬다. 실측 성능이 점근적 복잡도와 어긋나는 실제 사례(캐시 지역성)는 [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)를 참고. 바로 다음 챕터인 [알고리즘 분류](/post/computerterms/algorithm-classification/)에서는 효율성과 독립적인 축—주제별·설계 기법별 분류—을 다룬다.

## 참고 자료

> Knuth, D. E. (1976). "Big Omicron and Big Omega and Big Theta". *ACM SIGACT News*, 8(2), 18–24. [DOI: 10.1145/1008328.1008329](https://dl.acm.org/doi/10.1145/1008328.1008329)

- [Sedgewick & Wayne, *Algorithms* (4th ed.), Section 1.4: Analysis of Algorithms](https://algs4.cs.princeton.edu/14analysis/) — 차수(order-of-growth) 분석과 최악 경우 성능 보장을 다루는 표준 자료
- [MIT OCW 6.006: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — 점근적 분석을 다루는 대학 강의 자료
