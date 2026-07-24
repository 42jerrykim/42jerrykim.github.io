---
image: "wordcloud.png"
slug: dynamic-programming
collection_order: 43
draft: false
title: "[Computer Terms] 동적 계획법 (Dynamic Programming)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "부분 문제 중복과 최적 부분 구조 개념을 바탕으로 메모이제이션(Top-down)과 타뷸레이션(Bottom-up)을 피보나치 코드로 비교하고 시간복잡도 개선을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Algorithm(알고리즘)
- Dynamic-Programming(동적계획법)
- Memoization(메모이제이션)
- Tabulation(타뷸레이션)
- Overlapping-Subproblems(부분문제중복)
- Optimal-Substructure(최적부분구조)
- Recursion(재귀)
- Fibonacci(피보나치)
- Knapsack-Problem(배낭문제)
- Time-Complexity(시간복잡도)
- C
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

이 챕터는 [시간 복잡도](/post/computerterms/time-complexity/)의 빅오 표기법과 재귀 함수 호출을 이미 안다고 가정한다. [정렬 알고리즘](/post/computerterms/sorting-algorithms/)에서 다룬 분할정복과 이번 챕터의 동적 계획법은 "문제를 작은 문제로 나눈다"는 점에서 비슷해 보이지만 핵심 차이가 있으므로, 그 차이를 함께 짚는다. 배낭 문제의 2차원 DP 테이블 최적화(공간 압축) 같은 심화 기법은 범위 밖이며 다루지 않는다.

## 왜 재귀만으로는 부족한가

피보나치 수열을 재귀로 그대로 옮기면 `fib(n) = fib(n-1) + fib(n-2)`로 코드는 수학 정의와 똑같이 짧다. 그런데 `fib(5)`를 계산하는 과정을 추적해보면 `fib(3)`이 두 번, `fib(2)`가 세 번 등 같은 부분 문제가 반복해서 계산되는 것이 보인다. n이 커질수록 이 중복 계산은 기하급수적으로 늘어나 `fib(40)` 근처만 되어도 순수 재귀는 수 초가 걸린다. 동적 계획법은 이 **중복 계산을 한 번만 하고 결과를 저장해 재사용**하는 것으로 이 문제를 해결한다.

## 부분 문제 중복과 최적 부분 구조

동적 계획법(Dynamic Programming, DP)이 적용 가능한 문제는 두 가지 성질을 가진다. **부분 문제 중복(Overlapping Subproblems)**은 큰 문제를 재귀적으로 풀 때 같은 작은 문제가 여러 번 반복해서 나타나는 성질이다. 앞서 본 피보나치의 `fib(3)` 중복 호출이 대표적이다. 이 성질이 없다면(모든 부분 문제가 서로 다르다면) 저장해 재사용할 것이 없으므로 DP를 적용할 이유가 없다 — 이 경우는 순수 분할정복(병합정렬 등)에 해당한다.

**최적 부분 구조(Optimal Substructure)**는 문제 전체의 최적해가 부분 문제들의 최적해로부터 구성될 수 있는 성질이다. 배낭 문제에서 "물건 n개로 용량 W를 채우는 최적해"는 "물건 n-1개로 용량 W를 채우는 최적해"와 "물건 n-1개로 용량 W-무게(n)을 채우는 최적해에 물건 n을 추가한 값" 중 더 큰 쪽으로 구성된다. 이 두 성질이 모두 있어야 DP가 성립한다 — 부분 문제 중복만 있고 최적 부분 구조가 없다면, 부분 문제의 최적해를 조합해도 전체 최적해가 되지 않는다.

## 메모이제이션(Top-down)과 타뷸레이션(Bottom-up)

DP를 구현하는 방식은 두 가지다. **메모이제이션(Memoization)**은 재귀 함수 구조를 그대로 두되, 호출 결과를 캐시(배열이나 해시맵)에 저장해 같은 인자로 다시 호출되면 캐시된 값을 즉시 반환하는 방식이다. 재귀 호출이 큰 문제에서 작은 문제로 내려가므로 **Top-down**이라 부른다. **타뷸레이션(Tabulation)**은 반대로 가장 작은 부분 문제부터 테이블(배열)을 채워나가 최종적으로 원하는 큰 문제의 답에 도달하는 반복문 기반 방식으로, **Bottom-up**이라 부른다.

다음은 세 가지 버전의 피보나치 구현이다. 순수 재귀, 메모이제이션, 타뷸레이션 순서로 같은 문제를 어떻게 다른 시간 복잡도로 푸는지 비교한다.

```c
#include <stdio.h>
#include <string.h>

#define MAX_N 50

/* 1. 순수 재귀: O(2^n), n=40만 되어도 체감될 만큼 느려진다 */
long long fib_naive(int n) {
    if (n <= 1) return n;
    return fib_naive(n - 1) + fib_naive(n - 2);
}

/* 2. 메모이제이션(Top-down): O(n), 재귀 구조를 유지하되 캐시로 중복 계산을 제거 */
long long memo[MAX_N];
int computed[MAX_N];

long long fib_memo(int n) {
    if (n <= 1) return n;
    if (computed[n]) return memo[n];        /* 이미 계산된 값이면 즉시 반환 */
    computed[n] = 1;
    memo[n] = fib_memo(n - 1) + fib_memo(n - 2);
    return memo[n];
}

/* 3. 타뷸레이션(Bottom-up): O(n), 반복문으로 작은 값부터 채워 올라감 */
long long fib_tab(int n) {
    if (n <= 1) return n;
    long long table[MAX_N];
    table[0] = 0;
    table[1] = 1;
    for (int i = 2; i <= n; i++) {
        table[i] = table[i - 1] + table[i - 2];
    }
    return table[n];
}

int main(void) {
    int n = 30;
    memset(computed, 0, sizeof(computed));

    printf("naive: %lld\n", fib_naive(n));   /* 832040 */
    printf("memo:  %lld\n", fib_memo(n));    /* 832040 */
    printf("tab:   %lld\n", fib_tab(n));     /* 832040 */
    return 0;
}
```

세 함수는 같은 결과를 내지만 비용이 다르다. `fib_naive`는 호출 트리가 이진 트리 형태로 뻗어나가 O(2^n)이고, `fib_memo`와 `fib_tab`은 각 `n`에 대해 정확히 한 번씩만 계산하므로 O(n)이다. `n = 30`일 때 `fib_naive`는 약 270만 번의 함수 호출이 필요하지만, 나머지 둘은 30번의 계산으로 끝난다. 이 코드는 `gcc -std=c11 -Wall fibonacci.c -o fibonacci`로 컴파일·실행할 수 있으며, `n`을 40 이상으로 올려 `fib_naive`만 실행 시간이 급격히 늘어나는 것을 직접 확인할 수 있다.

## 비교: 메모이제이션 vs 타뷸레이션

| 항목 | 메모이제이션(Top-down) | 타뷸레이션(Bottom-up) |
|---|---|---|
| 구현 방식 | 재귀 + 캐시 | 반복문 + 테이블 |
| 코드 가독성 | 원래 재귀 정의와 유사해 이해 쉬움 | 채우는 순서를 미리 설계해야 함 |
| 계산 범위 | 실제로 필요한 부분 문제만 계산 | 테이블 전체를 채움(불필요한 부분 포함 가능) |
| 함수 호출 오버헤드 | 재귀 호출 스택 비용 있음 | 없음(반복문) |
| 공간 최적화 | 캐시 전체 유지 필요 | 최근 몇 개 값만 유지하도록 압축 가능(예: 피보나치는 변수 2개로 축소 가능) |

이 표에서 실무 판단의 기준은 **부분 문제 전체가 필요한가, 일부만 필요한가**다. 입력에 따라 실제로 방문하는 부분 문제가 적다면 메모이제이션이 불필요한 계산을 건너뛰어 유리하고, 대부분의 부분 문제를 결국 다 방문해야 한다면 타뷸레이션이 재귀 호출 오버헤드 없이 더 빠르다.

## 흔한 오개념

**"동적 계획법은 그냥 캐시를 쓰는 재귀다"** — 캐시는 구현 수단일 뿐, DP의 본질은 문제가 부분 문제 중복과 최적 부분 구조를 모두 만족한다는 **수학적 성질**이다. 이 성질이 없는 문제에 캐시만 붙인다고 DP가 되는 것은 아니다. 예를 들어 최장 경로(Longest Path, 사이클 있는 그래프) 문제는 최적 부분 구조가 성립하지 않아 DP로 풀 수 없다.

**"타뷸레이션이 항상 메모이제이션보다 빠르므로 무조건 Bottom-up으로 짜야 한다"** — 함수 호출 오버헤드가 없다는 점에서 일반적으로는 맞지만, 부분 문제 공간이 크면서 실제로 필요한 부분 문제는 일부뿐인 경우(예: 희소한 상태 공간을 갖는 문제)에는 메모이제이션이 불필요한 계산을 건너뛰어 오히려 더 빠르고 메모리도 적게 쓴다.

## 다른 개념과의 연결

동적 계획법은 [정렬 알고리즘](/post/computerterms/sorting-algorithms/)의 분할정복과 "문제를 작은 문제로 나눈다"는 접근은 같지만, 분할정복은 부분 문제들이 서로 겹치지 않는다는 점에서 다르다(병합정렬의 왼쪽/오른쪽 절반은 서로 독립적이다). [최단 경로 알고리즘](/post/computerterms/shortest-path-algorithms/)의 벨만-포드도 "간선을 거쳐 갈 때 더 짧아지면 갱신한다"는 점에서 DP의 relaxation 아이디어를 그래프에 적용한 사례로 볼 수 있다. 다음 챕터에서는 부분 문제를 저장·재사용하는 대신 매 단계 지역적으로 최선인 선택만 하고 다시 돌아보지 않는 **그리디 알고리즘**을 다룬다 — DP가 필요한 문제에 그리디를 잘못 적용하면 왜 틀린 답이 나오는지가 다음 챕터의 핵심이다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 어떤 문제가 부분 문제 중복과 최적 부분 구조를 만족하는지 판단해 DP 적용 가능 여부를 설명할 수 있다. 순수 재귀의 시간 복잡도가 왜 지수적으로 폭발하는지, 메모이제이션이 이를 어떻게 다항 시간으로 줄이는지 설명할 수 있다. 메모이제이션과 타뷸레이션 중 문제 특성에 따라 어느 것을 선택할지 판단할 수 있다.

## 참고 자료

> Bellman, R. (1957). *Dynamic Programming*. Princeton University Press. — 동적 계획법이라는 용어와 접근법을 처음 정립한 원저.

- [Visualgo: Dynamic Programming](https://visualgo.net/en) — 배낭 문제 등 대표 DP 문제의 상태 전이를 시각화한 자료
- [Python docs: functools.lru_cache](https://docs.python.org/3/library/functools.html#functools.lru_cache) — 메모이제이션을 언어 표준 라이브러리로 구현하는 방법
