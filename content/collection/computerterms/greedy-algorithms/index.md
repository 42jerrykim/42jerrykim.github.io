---
image: "wordcloud.png"
slug: greedy-algorithms
collection_order: 44
draft: false
title: "[Computer Terms] 그리디 알고리즘 (Greedy Algorithms)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "매 단계 지역 최적 선택이 전역 최적을 보장하는 조건과, 동전 거스름돈 문제가 그리디로 항상 풀리지 않는 반례를 활동 선택 문제 코드와 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Algorithm(알고리즘)
- Greedy(그리디)
- Greedy-Choice-Property(그리디선택속성)
- Optimal-Substructure(최적부분구조)
- Coin-Change(동전거스름돈)
- Activity-Selection(활동선택문제)
- Dynamic-Programming(동적계획법)
- Counterexample(반례)
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

이 챕터는 [동적 계획법](/post/computerterms/dynamic-programming/)에서 다룬 최적 부분 구조 개념과 [최단 경로 알고리즘](/post/computerterms/shortest-path-algorithms/)의 다익스트라를 먼저 읽었다고 가정한다. 다익스트라는 이미 그리디 알고리즘의 한 사례로 소개된 바 있다. 이 챕터는 그리디 선택이 정답을 보장하는 조건과 실패하는 반례에 집중하며, 그리디 알고리즘의 정확성을 수학적으로 증명하는 교환 논증(Exchange Argument) 같은 심화 기법은 범위 밖이므로 다루지 않는다.

## 왜 매번 최선의 선택이 항상 정답은 아닌가

**그리디 알고리즘(Greedy Algorithm)**은 전체 최적해를 한 번에 계산하는 대신, 매 단계에서 그 순간 가장 좋아 보이는 선택을 하고 이후 다시 되돌아보지 않는 방식이다. [최단 경로 알고리즘](/post/computerterms/shortest-path-algorithms/) 챕터의 다익스트라가 매번 현재까지 가장 짧은 정점을 확정해나간 것이 그리디의 실제 사례다. 그리디는 [동적 계획법](/post/computerterms/dynamic-programming/)처럼 부분 문제를 전부 저장하고 비교하지 않으므로 구현이 단순하고 빠르다. 문제는 이 "당장 최선"이 "전체 최선"과 항상 일치하지는 않는다는 점이다 — 이 챕터는 언제 일치하고 언제 어긋나는지를 다룬다.

## 그리디가 성립하는 조건

그리디 알고리즘이 정답을 보장하려면 두 조건이 필요하다. **그리디 선택 속성(Greedy Choice Property)**은 지역적으로(현재 시점에서) 최적인 선택을 계속 쌓아 나가면 전역 최적해에 도달할 수 있다는 성질이다. **최적 부분 구조**는 DP와 같은 개념으로, 문제의 최적해가 부분 문제의 최적해로 구성된다는 성질이다. 이 두 조건이 모두 성립하는 문제(예: 다익스트라의 최단 경로, 최소 신장 트리)는 그리디로 풀어도 정확하지만, 조건이 깨지는 문제(예: 배낭 문제의 0/1 변형)는 그리디가 틀린 답을 낸다.

## 활동 선택 문제: 그리디가 통하는 사례

**활동 선택 문제(Activity Selection Problem)**는 시작 시각과 끝나는 시각이 정해진 여러 활동 중, 서로 겹치지 않게 최대한 많은 활동을 선택하는 문제다. 이 문제의 그리디 전략은 "끝나는 시각이 가장 이른 활동부터 순서대로 고르고, 이미 선택한 활동과 겹치지 않으면 채택한다"이다. 직관적으로 끝나는 시각이 이를수록 다음 활동을 고를 여유 시간이 더 많이 남기 때문에, 이 전략은 실제로 최적해를 보장한다(끝나는 시각 기준 정렬 후 첫 선택이 항상 최적해의 일부로 교체 가능하다는 것이 증명되어 있다).

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int start;
    int finish;
} Activity;

int compare_by_finish(const void *a, const void *b) {
    return ((Activity *)a)->finish - ((Activity *)b)->finish;
}

int select_activities(Activity acts[], int n, int selected[]) {
    qsort(acts, n, sizeof(Activity), compare_by_finish);   /* 끝나는 시각 기준 정렬 */

    int count = 0;
    int last_finish = -1;

    for (int i = 0; i < n; i++) {
        if (acts[i].start >= last_finish) {   /* 이전 선택과 겹치지 않으면 채택 */
            selected[count++] = i;
            last_finish = acts[i].finish;
        }
    }
    return count;
}

int main(void) {
    Activity acts[] = {{1, 4}, {3, 5}, {0, 6}, {5, 7}, {8, 9}, {5, 9}};
    int n = sizeof(acts) / sizeof(acts[0]);
    int selected[6];

    int count = select_activities(acts, n, selected);

    printf("selected %d activities: ", count);
    for (int i = 0; i < count; i++) {
        printf("(%d,%d) ", acts[selected[i]].start, acts[selected[i]].finish);
    }
    printf("\n");   /* (1,4) (5,7) (8,9) 같은 3개 조합 */
    return 0;
}
```

핵심은 `last_finish`를 매번 방금 채택한 활동의 끝나는 시각으로만 갱신하고, 이후 다시 앞으로 되돌아가 선택을 바꾸지 않는다는 점이다. 이 코드는 `gcc -std=c11 -Wall activity_selection.c -o activity_selection`로 컴파일·실행할 수 있으며, 정렬 기준을 시작 시각이나 활동 길이로 바꾸면 최적해를 놓치는 반례를 직접 만들어 확인할 수 있다.

## 동전 거스름돈: 그리디가 실패하는 반례

**동전 거스름돈 문제**는 주어진 금액을 최소 개수의 동전으로 거슬러주는 문제다. 한국 원화(1, 5, 10, 50, 100, 500원)나 미국 센트(1, 5, 10, 25센트)처럼 화폐 단위가 "표준적(Canonical)"으로 설계된 체계에서는 "가장 큰 단위의 동전부터 최대한 많이 사용한다"는 그리디 전략이 실제로 최적해를 낸다. 그런데 화폐 단위가 이 조건을 만족하지 않으면 그리디는 실패한다. 예를 들어 동전 단위가 {1, 3, 4}뿐인 화폐 체계에서 6원을 거슬러줘야 한다면, 그리디는 4원짜리를 먼저 집어 4+1+1=3개를 쓰지만, 실제 최적해는 3+3=2개다. 그리디는 4원을 고른 뒤 "이미 4원을 골랐다"는 선택을 되돌아보지 않으므로 이 최적해를 찾지 못한다.

이 반례가 성립하는 이유는 동전 거스름돈 문제가 그리디 선택 속성을 항상 만족하지는 않기 때문이다. {1, 3, 4} 같은 임의의 동전 단위 집합에서는 최적해를 보장하려면 그리디 대신 [동적 계획법](/post/computerterms/dynamic-programming/)으로 풀어야 한다 — "금액 k를 거스르는 최소 동전 개수"를 작은 금액부터 타뷸레이션으로 채워나가면, 화폐 단위가 무엇이든 항상 정확한 최적해를 구할 수 있다.

## 비교: 그리디 vs 동적 계획법

| 항목 | 그리디 알고리즘 | 동적 계획법 |
|---|---|---|
| 선택 방식 | 매 단계 지역 최적, 되돌아보지 않음 | 모든 부분 문제를 비교해 전역 최적 선택 |
| 정확성 보장 조건 | 그리디 선택 속성 + 최적 부분 구조 | 부분 문제 중복 + 최적 부분 구조 |
| 시간 복잡도 | 보통 더 빠름(O(n log n) 이하가 흔함) | 보통 더 느림(부분 문제 수에 비례) |
| 구현 난이도 | 단순 | 상태 정의·전이식 설계 필요 |
| 정확성 실패 시 | 조용히 차선책을 반환(에러 없음) | 조건만 맞으면 항상 정확 |

이 표에서 가장 위험한 항목은 **"정확성 실패 시 조용히 차선책을 반환한다"**는 점이다. 그리디는 틀린 입력에서도 그럴듯한 답을 내놓기 때문에, 테스트 케이스가 우연히 표준적인 화폐 단위 같은 "그리디가 통하는" 경우만 다루면 버그가 드러나지 않는다. 이 알고리즘을 실무에 적용하기 전에는 반드시 그리디 선택 속성이 실제로 성립하는지 증명하거나, 최소한 반례를 찾아보는 검증이 필요하다.

## 흔한 오개념

**"동전 거스름돈은 항상 큰 단위부터 쓰면 최소 개수가 나온다"** — 이는 한국 원화·미국 달러처럼 특정 화폐 체계에서만 성립하는 우연이다. {1, 3, 4}처럼 표준적이지 않은 단위 집합에서는 위에서 본 것처럼 그리디가 최적해를 놓친다. 화폐 단위가 그리디 선택 속성을 만족하는지는 단위 집합마다 별도로 증명해야 하는 성질이지, 동전 거스름돈이라는 문제 유형 자체가 보장하는 성질이 아니다.

**"그리디가 실패하면 조합을 다 시도해보는 완전 탐색밖에 답이 없다"** — 그리디가 실패한다고 곧바로 지수 시간 완전 탐색으로 가야 하는 것은 아니다. 동전 거스름돈처럼 최적 부분 구조는 유지되는 문제라면 동적 계획법으로 다항 시간(O(금액 × 동전 종류 수))에 정확한 답을 구할 수 있다. 그리디의 실패는 "더 정교한 다항 시간 알고리즘이 필요하다"는 신호이지, "지수 시간이 불가피하다"는 신호가 아니다.

## 다른 개념과의 연결

[최단 경로 알고리즘](/post/computerterms/shortest-path-algorithms/)의 다익스트라는 그리디 선택 속성이 성립하는 대표 사례이고, 반대로 이 챕터의 동전 거스름돈 반례는 [동적 계획법](/post/computerterms/dynamic-programming/)이 왜 필요한지를 보여주는 짝이다. 두 챕터를 함께 보면 "지역 최적의 누적이 언제 전역 최적이 되는가"라는 알고리즘 설계의 핵심 질문에 답할 수 있다. 이것으로 알고리즘 갈래의 핵심 주제(정렬·탐색·최단 경로·DP·그리디)를 마무리하며, 이후 챕터는 이 알고리즘들이 실제 시스템에서 어떻게 조합되어 쓰이는지를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 그리디 알고리즘이 정답을 보장하는 조건(그리디 선택 속성, 최적 부분 구조)을 설명할 수 있다. 동전 거스름돈 문제에서 그리디가 실패하는 화폐 단위 반례를 직접 구성할 수 있다. 그리디가 실패하는 문제를 동적 계획법으로 다시 풀 수 있는 이유를 최적 부분 구조 관점에서 설명할 수 있다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Chapter 16: Greedy Algorithms. MIT Press.

- [Visualgo: Greedy](https://visualgo.net/en) — 활동 선택 문제 등 그리디 알고리즘의 선택 과정을 시각화한 자료
- [GeeksforGeeks: Greedy Algorithms](https://www.geeksforgeeks.org/greedy-algorithms/) — 동전 거스름돈 반례를 포함한 그리디 실패 사례 정리
