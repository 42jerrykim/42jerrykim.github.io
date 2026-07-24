---
image: "wordcloud.png"
slug: time-complexity
collection_order: 4
draft: false
description: "시간 복잡도는 알고리즘이 입력 크기에 따라 얼마나 빠르게 실행되는지를 수학적으로 분석하는 척도입니다. 빅오·빅오메가·빅세타 표기법으로 최악·최선·평균 실행 시간을 구분하고, 최고차항만 남기는 계산 규칙과 O(1)부터 O(n!)까지의 대표 복잡도 등급을 코드 예시로 다룹니다."
title: "[Computer Terms] Time Complexity 시간 복잡도"
date: 2022-03-14
last_modified_at: 2026-07-22
categories: ComputerTerms
tags:
- Technology(기술)
- Education(교육)
- Algorithm(알고리즘)
- Sorting(정렬)
- Time-Complexity(시간복잡도)
- Space-Complexity(공간복잡도)
- Complexity-Analysis(복잡도분석)
- Worst-Case(최악의경우)
- C
- Computer-Science(컴퓨터과학)
- Data-Structure(자료구조)
- Problem-Solving(문제해결)
- Recursion(재귀)
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
- Optimization(최적화)
---

## 이 장을 읽기 전에

이 챕터는 [알고리즘 효율성](/post/computerterms/algorithm-efficiency/)에서 다룬 O, Ω, Θ 표기법의 정의와 "왜 점근적 분석이 필요한가"를 전제로 한다. 여기서는 그 표기법을 실제로 어떻게 계산하고, 어떤 등급으로 분류하는지를 구체적 규칙과 코드로 다룬다.

## 시간 복잡도란 무엇인가

**시간 복잡도(Time Complexity)**는 [알고리즘 효율성](/post/computerterms/algorithm-efficiency/)에서 다룬 두 척도(시간 복잡도, 공간 복잡도) 중 계산 시간 쪽을 가리키는 개념이다. 산정 기준은 알고리즘이 수행하는 기본 연산의 수—비교, 덧셈, 곱셈, 나눗셈 등 명령·스텝의 개수—이며, 이 연산 수가 입력 크기 n과 어떤 함수 관계를 갖는지를 분석해 f(n) 형태로 표현한다. 입력 크기의 의미는 문제마다 다르다. 정렬 문제라면 정렬 대상 원소의 수, 계승 계산이라면 계산하려는 자연수, 최단 경로 문제라면 그래프의 정점·간선 수가 입력 크기에 해당한다. 분석은 실제 시간을 초 단위로 재는 것이 아니라, 입력 크기가 무한히 증가할 때 알고리즘이 어떻게 작동하는가를 따지는 **점근적(Asymptotic) 방법**을 쓴다.

## O, Ω, Θ: 세 가지 분석 종류

[알고리즘 효율성](/post/computerterms/algorithm-efficiency/)에서 소개한 세 표기법을 시간 복잡도 관점에서 다시 정리하면 다음과 같다. **빅오(Big-O), O()**는 "기껏해야 이 정도"를 뜻하는 점근적 **상한선**으로, 입력 크기가 무한대로 갈 때 알고리즘이 아무리 나빠도 이보다 덜 걸린다는 것을 보장한다(최악의 시나리오). **빅오메가(Big-Omega), Ω()**는 "적어도 이 정도"를 뜻하는 점근적 **하한선**으로, 최소 이만큼의 시간은 걸린다는 것을 보장한다(최선의 시나리오). **빅세타(Big-Theta), Θ()**는 "대략 이 정도"를 뜻하며, 빅오와 빅오메가가 같은 차수에서 만나는 절충점(교집합)이다. 관례상 최악의 경우 분석에는 O를, 최선의 경우 분석에는 Ω를, 평균 경우 분석에는 Θ를 붙여 쓴다.

## 계산 규칙: 어떻게 f(n)을 O(...)로 단순화하는가

실제 연산 수를 센 함수 f(n)을 빅오 표기로 단순화할 때는 네 가지 규칙을 적용한다. 첫째, **가장 큰 차수만 고려**한다 — 예를 들어 n² + n + 1은 입력이 커질수록 n² 항이 지배적이므로 O(n²)이 된다. 둘째, **계수는 무시**한다 — 3n은 O(n)이지 O(3n)이 아니다. 셋째, **작은 상수 차이는 무시**한다 — O(n-1)은 O(n)과 같다. 넷째, **규모가 압도적으로 큰 항만 남긴다** — O(2ⁿ + n²)에서는 2ⁿ이 n²을 압도하므로 O(2ⁿ)만 남는다. 이 규칙들은 모두 "입력이 무한히 커질 때 어느 항이 실행 시간을 지배하는가"라는 하나의 질문에서 나온다.

다음은 배열 정렬 여부에 따라 최선·최악의 경우가 갈리는 선형 탐색을 다시 살펴보되, 이번에는 반복 횟수를 직접 세는 코드다.

```c
#include <stdio.h>

int linear_search_counted(const int arr[], int n, int target, int *comparisons) {
    *comparisons = 0;
    for (int i = 0; i < n; i++) {
        (*comparisons)++;
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}

int main(void) {
    int arr[] = {5, 3, 8, 1, 9};
    int n = sizeof(arr) / sizeof(arr[0]);
    int comparisons;

    linear_search_counted(arr, n, 5, &comparisons);
    printf("target=5 (first element): %d comparisons\n", comparisons);  /* 1: O(1)에 가까움 */

    linear_search_counted(arr, n, 7, &comparisons);
    printf("target=7 (not found): %d comparisons\n", comparisons);      /* 5: O(n) */

    return 0;
}
```

이 코드를 `gcc -std=c11 -Wall linear_search_counted.c -o linear_search_counted`로 컴파일해 배열 크기 n을 10배, 100배로 늘려가며 실행하면, 최악의 경우 비교 횟수가 n에 비례해 늘어나는 것(O(n))을 직접 확인할 수 있다.

## 대표 복잡도 등급

빅오로 표현되는 함수는 몇 가지 대표적인 등급으로 이름 붙여 부른다. 증가 속도가 느린 순서대로 나열하면 상수 시간 O(1), 로그 시간 O(log n), 선형 시간 O(n), 선형로그 시간 O(n log n), 이차 시간 O(n²), 삼차 시간 O(n³), 지수 시간 O(2ⁿ), 계승 시간 O(n!)이며, 종료되지 않는 무한 루프는 O(∞)로 표기한다. 이 등급들의 대소 관계는 다음과 같다.

| 등급 | 표기 | 예시 알고리즘 |
|---|---|---|
| 상수 시간 | O(1) | 배열 인덱스 접근 |
| 로그 시간 | O(log n) | 이진 탐색 |
| 선형 시간 | O(n) | 선형 탐색 |
| 선형로그 시간 | O(n log n) | 병합 정렬, 퀵 정렬(평균) |
| 이차 시간 | O(n²) | 버블 정렬, 삽입 정렬 |
| 삼차 시간 | O(n³) | 단순 행렬 곱셈, 3중 루프 전수 비교 |
| 지수 시간 | O(2ⁿ) | 부분집합 전수 탐색 |
| 계승 시간 | O(n!) | 순열 전수 탐색 |

증가율 순서로는 O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!) < O(∞)이 성립한다. n이 10에서 100으로 늘어날 때 O(n)은 10배, O(n²)은 100배, O(2ⁿ)은 사실상 계산 불가능한 수준으로 커진다는 점이, 왜 지수 시간 알고리즘을 실무에서 기피하는지를 보여준다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. f(n) = n² + n + 1 같은 함수를 최고차항만 남기고 계수를 무시하는 규칙에 따라 O(n²)으로 단순화할 수 있다. O(1)부터 O(n!)까지 대표 복잡도 등급을 증가 속도 순서대로 나열하고, 각 등급에 해당하는 예시 알고리즘을 하나씩 들 수 있다. 같은 알고리즘이 최선·최악의 경우에 서로 다른 복잡도를 가질 수 있다는 것을 구체적 코드 실행 결과로 설명할 수 있다.

## 흔한 오개념

**"Big-O는 최악의 경우만을 뜻한다"** — O는 점근적 **상한**을 뜻하는 표기법일 뿐, 어떤 경우(최악·평균·최선) 분석에도 붙일 수 있다. "최악의 경우 분석에 O를 쓰는 것이 관례"인 것이지, "O = 최악의 경우"라는 등식이 성립하는 것은 아니다.

**"O(n²)은 O(n)보다 항상 느리다"** — 점근적 표기법은 입력 크기 n이 충분히 커질 때의 증가율만 비교한다. 상수 계수와 캐시 지역성 같은 실측 요인 때문에 입력이 작을 때는 이론상 더 느린 O(n²) 코드가 실제로는 더 빠른 경우가 흔하다 — [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)의 캐시 지역성 논의를 참고.

## 다른 개념과의 연결

이 챕터에서 다룬 O/Ω/Θ 표기법의 상위 개념(왜 효율성을 분석해야 하는가)은 [알고리즘 효율성](/post/computerterms/algorithm-efficiency/)에서, 이 표기법이 실제 알고리즘 비교에 쓰이는 예시는 [정렬 알고리즘](/post/computerterms/sorting-algorithms/), [탐색 알고리즘](/post/computerterms/searching-algorithms/)에서 확인할 수 있다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Chapter 3: Growth of Functions. MIT Press.

- [MIT OCW 6.006: Introduction to Algorithms — Asymptotic Notation](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — 점근적 표기법을 다루는 대학 강의 자료
- [Sedgewick & Wayne, *Algorithms* (4th ed.), Section 1.4: Analysis of Algorithms](https://algs4.cs.princeton.edu/14analysis/) — 시간 복잡도 분석 방법론을 다루는 프린스턴대 표준 교재
