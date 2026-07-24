---
description: "알고리즘을 주제(탐색·정렬·그래프·문자열)별, 확률 개입 여부(결정적·확률적)별, 설계 기법(분할정복·동적계획법·그리디)별 세 가지 축으로 분류하고, 분할정복과 동적계획법을 혼동하기 쉬운 이유까지 구체적 예시와 함께 설명합니다."
image: "wordcloud.png"
slug: "algorithm-classification"
collection_order: 3
draft: false
title: "[Computer Terms] 알고리즘 분류, 알고리즘 구분"
date: 2022-03-14
last_modified_at: 2026-07-22
categories: ComputerTerms
tags:
- Technology(기술)
- Education(교육)
- Algorithm(알고리즘)
- Dynamic-Programming(동적계획법)
- Greedy(그리디)
- Binary-Search(이진탐색)
- Sorting(정렬)
- Graph(그래프)
- Hashing(해싱)
- Divide-and-Conquer(분할정복)
- Recursion(재귀)
- Computer-Science(컴퓨터과학)
- Data-Structure(자료구조)
- Problem-Solving(문제해결)
- Worst-Case(최악의경우)
- Complexity-Analysis(복잡도분석)
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
- Implementation(구현)
---

## 이 장을 읽기 전에

이 챕터는 [알고리즘](/post/computerterms/algorithm/)에서 다룬 알고리즘의 정의를 전제로 한다. 여기서는 개별 알고리즘 하나하나가 아니라, 수많은 알고리즘을 어떤 기준으로 묶어 이해할지를 다룬다. 각 분류에 속하는 알고리즘의 구체적 구현과 시간 복잡도는 [정렬 알고리즘](/post/computerterms/sorting-algorithms/), [탐색 알고리즘](/post/computerterms/searching-algorithms/), [동적 계획법](/post/computerterms/dynamic-programming/), [그리디 알고리즘](/post/computerterms/greedy-algorithms/) 등 각 챕터에서 이어서 다룬다.

## 왜 분류가 필요한가

알고리즘은 수천 가지가 존재하지만, 이들을 아무 기준 없이 나열하면 새로운 문제를 만났을 때 "어떤 접근을 시도해볼 것인가"를 판단하기 어렵다. 분류는 알고리즘을 세 가지 서로 독립적인 축으로 나눠보는 관점을 제공한다. **무엇을 하는가**(주제별 분류), **답이 항상 같은가**(확률 개입 여부), **어떤 전략으로 문제를 쪼개는가**(설계 기법)다. 같은 알고리즘도 이 세 축에서 각각 다른 이름표를 가질 수 있다 — 예를 들어 퀵 정렬은 주제별로는 "정렬 알고리즘", 확률 개입 여부로는 무작위 피벗을 쓰면 "확률 알고리즘", 설계 기법으로는 "분할정복"에 해당한다.

## 주제별 분류: 무엇을 하는 알고리즘인가

가장 직관적인 분류 축은 알고리즘이 풀려는 문제의 종류다. **탐색 알고리즘(Searching Algorithm)**은 리스트에서 특정 원소의 위치나 존재 여부를 찾는다(선형 탐색, 이진 탐색 등). **정렬 알고리즘(Sorting Algorithm)**은 자료를 특정 기준에 맞춰 순서 있게 재배열한다(선택·버블·삽입·퀵·병합 정렬 등). **그래프 알고리즘(Graph Algorithm)**은 그래프의 순회·탐색, 신장 트리 구성, 최단 경로 탐색 등을 다룬다. **문자열 매칭 알고리즘(String Matching Algorithm)**은 긴 텍스트 안에서 짧은 패턴 문자열의 위치를 찾는다. 이 밖에도 해시 알고리즘, 최적화 알고리즘 등 문제 도메인마다 별도의 이름을 가진 알고리즘 군이 존재한다.

## 확률 개입 여부에 따른 분류

같은 입력을 두 번 실행했을 때 항상 같은 답이 나오는지를 기준으로도 알고리즘을 나눌 수 있다. **결정 알고리즘(Deterministic Algorithm)**은 같은 입력에 대해 항상 같은 실행 경로를 거쳐 같은 결과를 낸다 — 앞서 다룬 대부분의 탐색·정렬·그래프 알고리즘이 여기 속한다. **확률 알고리즘(Probabilistic Algorithm)**, 다른 말로 **무작위 알고리즘(Randomized Algorithm)**은 실행 중 내리는 일부 결정이 난수에 의존한다. 이 중에서도 두 갈래가 구분된다. **몬테카를로 알고리즘(Monte Carlo Algorithm)**은 무작위성을 이용해 근사적인 해를 빠르게 구하되 정확도를 100% 보장하지 않고, **라스베가스 알고리즘(Las Vegas Algorithm)**은 실행 시간은 무작위로 달라지지만 답은 항상 정확하다. 앞서 언급한 무작위 피벗 퀵 정렬이 라스베가스 알고리즘의 대표적인 예다 — 어떤 피벗을 고르든 최종적으로 정렬된 배열은 항상 정확하지만, 정렬에 걸리는 시간(비교 횟수)은 실행마다 달라질 수 있다.

## 설계 기법에 의한 분류

세 번째 축은 문제를 어떤 전략으로 쪼개고 재조합하는가다. **분할정복(Divide and Conquer)**은 큰 문제를 서로 독립적인 작은 부분 문제들로 나눈 뒤 각각을 재귀적으로 풀고 결과를 합친다(병합 정렬이 대표적). **동적 계획법(Dynamic Programming)**은 부분 문제들이 서로 겹칠 때(중복 부분 문제) 한 번 계산한 결과를 저장해 재사용함으로써 지수 시간 폭발을 막는다. **탐욕 알고리즘(Greedy Algorithm)**은 매 단계마다 그 순간 가장 좋아 보이는 선택을 하며, 문제가 그리디 선택 속성을 만족할 때만 전역 최적해를 보장한다. 다음 표는 세 기법이 "부분 문제를 어떻게 다루는가"를 기준으로 한 핵심 차이를 정리한 것이다.

| 설계 기법 | 부분 문제의 독립성 | 최적해 보장 조건 | 대표 예시 |
|---|---|---|---|
| 분할정복 | 서로 독립적(겹치지 않음) | 항상 보장 | 병합 정렬, 퀵 정렬 |
| 동적 계획법 | 서로 겹침(중복 부분 문제) | 최적 부분 구조 성립 시 보장 | 피보나치, 배낭 문제 |
| 탐욕 알고리즘 | 겹침 여부 무관, 부분 문제를 저장하지 않음 | 그리디 선택 속성 성립 시에만 보장 | 활동 선택, 최소 신장 트리 |

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 주제별·확률 개입 여부·설계 기법이라는 세 분류 축이 서로 독립적이라는 것을 예시(예: 무작위 피벗 퀵 정렬)로 설명할 수 있다. 몬테카를로와 라스베가스 알고리즘의 차이를 "무엇이 무작위인가"(정확도 vs. 실행 시간) 기준으로 구분할 수 있다. 분할정복과 동적 계획법을 "부분 문제가 겹치는가"라는 기준으로 구분할 수 있다.

## 흔한 오개념

**"분할정복과 동적계획법은 같은 것이다"** — 둘 다 문제를 작은 부분 문제로 나눈다는 공통점이 있지만, 분할정복은 부분 문제들이 서로 겹치지 않는 것을 전제로 하는 반면(병합 정렬처럼 나뉜 절반이 서로 독립적), [동적 계획법](/post/computerterms/dynamic-programming/)은 부분 문제가 반복해서 겹칠 때(중복 부분 문제) 그 결과를 저장해 재사용한다는 점이 다르다. 이 차이를 모르면 동적계획법이 필요한 문제에 분할정복만 적용해 지수 시간으로 폭발하는 코드를 짜게 된다.

**"그리디 알고리즘은 항상 동적계획법보다 나쁜 근사해만 준다"** — [그리디 알고리즘](/post/computerterms/greedy-algorithms/)에서 다루듯, 그리디 선택 속성이 성립하는 문제(활동 선택, 최소 신장 트리 등)에서는 그리디가 동적계획법 없이도 정확한 최적해를 더 빠르게 낸다. 그리디가 부정확해지는 것은 그 속성이 성립하지 않는 문제(0/1 배낭 문제 등)에 잘못 적용했을 때뿐이다.

## 다른 개념과의 연결

주제별 분류에서 언급한 탐색·정렬 알고리즘의 구체적 구현은 [탐색 알고리즘](/post/computerterms/searching-algorithms/), [정렬 알고리즘](/post/computerterms/sorting-algorithms/)에서, 설계 기법 분류의 동적계획법·그리디는 각각 [동적 계획법](/post/computerterms/dynamic-programming/), [그리디 알고리즘](/post/computerterms/greedy-algorithms/)에서 코드와 함께 자세히 다룬다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Part II–III: Sorting and Order Statistics, Data Structures. MIT Press.

- [Sedgewick & Wayne, *Algorithms* (4th ed.) 공식 강의 자료](https://algs4.cs.princeton.edu/home/) — 알고리즘 분류 체계를 다루는 프린스턴대 표준 교재
- [Skiena, *The Algorithm Design Manual*](https://www.algorist.com/) — 설계 기법(분할정복·DP·그리디)별 분류와 실무 적용 가이드
