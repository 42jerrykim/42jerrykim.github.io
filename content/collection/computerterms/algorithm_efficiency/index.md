---
image: "wordcloud.png"
slug: algorithm-efficiency
collection_order: 2
description: "알고리즘 효율성(Algorithm Efficiency)은 주어진 문제를 해결할 때 자원(시간, 공간)을 얼마나 적게 사용하는지를 판단하는 기준입니다. 시간 복잡도와 공간 복잡도를 분석하여 다양한 입력 크기에서 알고리즘의 성능을 비교, 최적화하며, 효율적 문제 해결에 필수적입니다."
title: "[Computer Terms] Algorithm Efficiency, Computational Complexity 알고리즘 효율성, 계산 복잡도"
date: 2022-03-14
categories: ComputerTerms
tags:
- Technology(기술)
- Education(교육)
- Go
- Algorithm(알고리즘)
- Graph(그래프)
- Self-Hosted(셀프호스팅)
- Tutorial(튜토리얼)
- Guide(가이드)
- Problem-Solving(문제해결)
- Time-Complexity(시간복잡도)
- Memory(메모리)
- Reference(참고)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- How-To
- Tips
- Beginner
- Advanced
- Case-Study
- Deep-Dive
- 실습
- Markdown(마크다운)
- Productivity(생산성)
- Innovation(혁신)
- Review(리뷰)
- Configuration(설정)
- Workflow(워크플로우)
- Web(웹)
- Blog(블로그)
- Open-Source(오픈소스)
---

## 알고리즘의 효율성/성능

알고리즘 효율성은, 계산에 필요한 자원의 소요 량(量)이 적을수록 좋은 것 임
* 시간과 공간 측면에서 적게 소요되는 것이, 효율적이고 좋은 알고리즘 임


## 알고리즘 효율성의 관점 구분

계산 시간   : 시간 복잡도 (Time Complexity)
* 주로, 수행 시간 관점에서, 알고리즘이 사용한 기본 연산의 수 (스텝 수,명령 수)
* 주요 기본 연산 : 정수의 비교,덧셈,곱셈,나눗셈 등

소요 메모리 : 공간 복잡도 (Space Complexity)
* 계산에 소요되는 컴퓨터 메모리


## 알고리즘 효율성의 척도 : 계산 복잡도 (Computational Complexity, Complexity Metric)

주로, 시간 복잡도 위주로 따짐 다만, 최근의 빅데이터 처리에는 공간 복잡도도 점차 중요해 짐

## 알고리즘 효율성의 분석 : 수행 시간 및 소요 메모리 분석

효율성 분석
* 알고리즘을 실행하는 데 필요한 시간,공간을 측정하는 것

분석 대상  :  (입력) 크기, (분석대상) 소요 시간 및 공간
* 문제의 **입력 크기**가 증가함에 따라, **처리 시간(연산 수) 및 소요 메모리**가 얼마나 증가하는가를 분석함
* 입력 크기의 ex) 배열의 크기, 다항식 차수, 행렬의 항목 수, 이진 입력 비트 수, 그래프에서 정점 및 가지 수 등

표현 방식  :  다항식 함수 형태
* 주로, **소요 공간** 보다는 **수행 시간**에 대해, 기본 연산 횟수를, 입력 크기 n에 따른 함수 f(n)을, 다항식 함수 형태로 표현
* 이는, 기계적인 속도나 프로그래밍 스타일과는 무관함

분석 방법  :  최악, 평균, 최선
* 최악 경우(worst-case), 평균 경우(average-case), 최선 경우(best-case)    ☞ 시간 복잡도 참조
* 알고리즘 실행 시간을 정확히 측정하기 보다는, 입력 크기가 증가함에 따라, 소요 시간이 어떻게 변하는 지에 관심이 있음

표기법  :  점근적 표기법
* big-O (빅 오 표기법) : O() => 점근적 **상한선**(관례상 최악의 경우 분석에 가장 흔히 쓰이지만, 정의 자체는 최선·평균 경우에도 쓸 수 있다)
* big-Omega (빅 오메가 표기법) : Ω() => 점근적 **하한선**(관례상 최선의 경우 분석에 흔히 쓰임)
* big-Theta (빅 세타 표기법) : Θ() => 상한과 하한이 같은 차수로 만나는 **엄격한 점근 한계**(관례상 평균 경우 분석에 흔히 쓰임)

## 흔한 오개념

**"Big-O는 최악의 경우만을 뜻하는 표기법이다"** — Big-O(O)는 "이 함수보다 느리게 증가하지 않는다"는 점근적 **상한**을 뜻할 뿐, 최악/평균/최선 중 어느 경우를 분석하든 쓸 수 있는 수학적 표기법이다. 다만 실무에서 "이 알고리즘이 아무리 나빠도 이 정도 성능은 보장한다"는 안전 마진이 중요하므로 최악의 경우 분석에 O를 붙여 쓰는 관례가 굳어졌을 뿐이다. Ω(빅 오메가)를 최악의 경우에, O를 최선의 경우에 적용하는 것도 수학적으로는 유효하다.

**"시간 복잡도가 낮으면 항상 더 빠르다"** — [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)에서 다루듯, 점근적 표기법은 입력 크기가 충분히 클 때의 증가율만 비교한다. 상수 계수와 캐시 지역성 같은 실측 요인 때문에, 입력이 작을 때는 이론상 더 느린 O(n²) 알고리즘이 실제로는 O(n log n) 알고리즘보다 빠른 경우가 흔하다.

## 다른 개념과의 연결

이 챕터에서 다룬 점근적 표기법(O, Ω, Θ)의 구체적 계산 규칙과 예시는 [시간 복잡도](/post/computerterms/time-complexity/)에서, 효율성 분석의 상위 개념인 알고리즘 자체의 정의는 [알고리즘](/post/computerterms/algorithm/)에서 다룬다. 실측 성능이 점근적 복잡도와 어긋나는 실제 사례(캐시 지역성)는 [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)를 참고.

## 참고 자료

> Knuth, D. E. (1976). "Big Omicron and Big Omega and Big Theta". *ACM SIGACT News*, 8(2), 18–24.

- [Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms* (MIT Press), Chapter 3: Growth of Functions](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/) — O/Ω/Θ 표기법의 표준 정의
- [MIT OCW 6.006: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — 점근적 분석을 다루는 대학 강의 자료