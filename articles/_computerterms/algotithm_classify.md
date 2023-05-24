---
title: "알고리즘 분류, 알고리즘 구분"
date: 2022-03-14
---

# 알고리즘의 주제별 분류

기초적인 알고리즘

* 최대값 또는 최소값 찾기 등
  * 가장 큰 숫자를 기억해가며 진행함 
* 유클리드 알고리즘
  * 두 정수의 최대공약수를 빠르게 구하기

탐색 알고리즘 (Searching Algorithm)

* 탐색 문제 
  * 순서화된 리스트(ordered list)에서 어떤 원소의 위치 및 존재유무를 찾는 것
* 탐색문제의 해 또는 결과
  * 원소의 위치
* 주요 종류
  * 순차 탐색(sequential search)/선형탐색(linear search)
  * 이진 탐색 (binary search) 등
        * 보통, 자료구조 형태에 따라 구분됨

스트링 매칭 알고리즘 (String Matching Algorihm)

* 긴 텍스트에서 짧은 패턴 문자열이 어디에 있는지를 찾는 것 

정렬 알고리즘 (Sorting Algorithm)

* 정렬 문제
  * 수많은 자료를 특정 목적에 맞게 순서있게 재 배열하는 것
* 정렬문제의 해 또는 결과
  * 정렬된 배열
* 주요 종류
  * 선택 정렬 (Selection Sort)
  * 버블 정렬 (Bubble Sort)
  * 삽입 정렬 (Insertion Sort)
  * 퀵 정렬 (Quick Sort)
  * 병합 정렬 (Merge Sort)

그래프 알고리즘 (Graph Algorithm)

* 주요 종류
  * 그래프 순회(Graph Traversal)/탐색,검색(Graph Search) 방법
  * 신장 트리(생성 트리) 작성 방법
  * 최소비용 생성트리 작성 알고리즘
  * 최단경로 알고리즘

해시 알고리즘 (Hash Algorithm)

최적화 알고리즘(Optimizing Algorithm) 등


# 알고리즘에 확률의 개입 여부에 따른 분류

결정 알고리즘 (Deterministic Algorithm)

* 항상 정확한 답을 반환하는 알고리즘
* ex) 
  * 위 1.항에 언급된 대부분의 알고리즘들

확률 알고리즘 (Probabilistic Algorithm), 무작위 알고리즘 (Randomized Algorithm)

* 실행될 명령이 무작위로 결정되는 알고리즘
* ex) 
  * 몬테칼로 알고리즘 : 무작위로 난수를 발생시켜 근사적인 해를 구하는 알고리즘
  * 라스베가스 알고리즘 : 무작위 시간으로 정확한 해를 구하는 알고리즘


# 알고리즘의 설계 기법/설계 전략/설계 패러다임에 의한 분류

※ ☞ 알고리즘 설계 참조

* 분할정복(Divide and Conquer) 전략
  * 규모가 큰 문제를 만만한 작은 조각으로 나눠 각개격파 
* 동적계획법(Dynamic Programming) 전략
* 탐욕 알고리즘(Greedy Algorithm) 전략 등