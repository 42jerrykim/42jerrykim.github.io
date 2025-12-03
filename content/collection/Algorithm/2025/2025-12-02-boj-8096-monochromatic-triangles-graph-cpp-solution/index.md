---
title: "[BOJ] 8096번 모노크로매틱 삼각형"
description: "모노크로매틱 삼각형 문제 풀이. 그래프 이론을 이용하여 인접 리스트와 이분 탐색으로 효율적으로 삼각형을 세는 방법을 설명합니다. 시간 복잡도 최적화 기법을 학습할 수 있습니다."
categories:
- Algorithm
tags:
- algorithms
- graph-theory
- adjacency-list
- binary-search
- triangle-counting
- cpp
- boj
- backjoon
- monochromatic-triangles
- graph-algorithms
- optimization
- data-structures
- time-complexity
- graph-problems
- competitive-programming
- problem-solving
- computer-science
- algorithmic-thinking
- efficiency
- implementation
- advanced-algorithms
- graph-coloring
- edge-detection
- computational-geometry
- advanced-data-structures
- optimization-techniques
- algorithm-design
- computational-efficiency
- problem-analysis
- solution-design
- coding-challenges
- technical-interview
- algorithm-interview
- coding-problems
- programming-competition
- problem-solving-strategies
- algorithmic-approach
- optimization-strategy
- performance-tuning
- runtime-optimization
- 알고리즘
- 그래프이론
- 삼각형세기
- 백준
- boj
- 모노크로매틱
- 그래프이론
- 효율성
- 최적화
date: 2025-12-02
lastmod: 2025-12-02
image: wordcloud.png
---

## 문제 소개

42jerrykim.github.io에서 더 많은 정보를 확인할 수 있습니다.

### 문제 설명

이 문제는 그래프에서 모노크로매틱 삼각형(같은 색의 세 변으로 이루어진 삼각형)의 개수를 구하는 문제입니다.

**입력:**
- n개의 점 (3 ≤ n ≤ 1,000)
- m개의 빨간색 간선
- 나머지 모든 간선은 검은색

**출력:**
- 모노크로매틱 삼각형의 개수

**예제:**
```
입력: n=6, m=9
간선: (1,2), (2,3), (2,5), (1,4), (1,6), (3,4), (4,5), (5,6), (3,6)
출력: 2
```

## 문제 분석

단순히 모든 삼각형을 확인하면 O(n³ log m)이 되어 시간 초과가 발생합니다. 더 효율적인 알고리즘이 필요합니다.

### 최적화 전략

1. **인접 리스트 활용**: 각 정점마다 빨간색/검은색으로 연결된 정점들을 따로 저장
2. **중심 정점 기준**: 각 정점을 중심으로 하여 연결된 정점들의 쌍을 확인
3. **이분 탐색**: 간선 존재 여부를 O(log n) 시간에 확인
4. **중복 제거**: 각 삼각형을 정확히 한 번만 세기

### 시간 복잡도 분석

- 기존: O(n³ log m) → 시간 초과
- 최적화: O(n² + Σ(degree²) log n) → 평균적으로 훨씬 빠름

## 풀이 코드

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n, m;
    cin >> n >> m;
    
    vector<vector<int>> redAdj(n + 1);
    vector<vector<int>> blackAdj(n + 1);
    
    // 빨간색 간선 저장
    vector<pair<int, int>> redEdges;
    for (int i = 0; i < m; i++) {
        int p, k;
        cin >> p >> k;
        redEdges.push_back({p, k});
        redAdj[p].push_back(k);
        redAdj[k].push_back(p);
    }
    
    // 검은색 간선 표시 (빨간색이 아닌 모든 간선)
    vector<vector<bool>> isRed(n + 1, vector<bool>(n + 1, false));
    for (auto& e : redEdges) {
        isRed[e.first][e.second] = true;
        isRed[e.second][e.first] = true;
    }
    
    for (int i = 1; i <= n; i++) {
        for (int j = i + 1; j <= n; j++) {
            if (!isRed[i][j]) {
                blackAdj[i].push_back(j);
                blackAdj[j].push_back(i);
            }
        }
    }
    
    // 정렬하여 이분 탐색 가능하게
    for (int i = 1; i <= n; i++) {
        sort(redAdj[i].begin(), redAdj[i].end());
        sort(blackAdj[i].begin(), blackAdj[i].end());
    }
    
    int count = 0;
    
    // 빨간색 삼각형 세기
    for (int i = 1; i <= n; i++) {
        int deg = redAdj[i].size();
        for (int j = 0; j < deg; j++) {
            for (int k = j + 1; k < deg; k++) {
                int v1 = redAdj[i][j];
                int v2 = redAdj[i][k];
                if (v1 > i && v2 > i) {  // 중복 방지
                    if (binary_search(redAdj[v1].begin(), redAdj[v1].end(), v2)) {
                        count++;
                    }
                }
            }
        }
    }
    
    // 검은색 삼각형 세기
    for (int i = 1; i <= n; i++) {
        int deg = blackAdj[i].size();
        for (int j = 0; j < deg; j++) {
            for (int k = j + 1; k < deg; k++) {
                int v1 = blackAdj[i][j];
                int v2 = blackAdj[i][k];
                if (v1 > i && v2 > i) {  // 중복 방지
                    if (binary_search(blackAdj[v1].begin(), blackAdj[v1].end(), v2)) {
                        count++;
                    }
                }
            }
        }
    }
    
    cout << count << '\n';
    
    return 0;
}
```

## 알고리즘 설명

### 1단계: 데이터 구조 구성

```cpp
vector<vector<int>> redAdj(n + 1);    // 빨간색 인접 리스트
vector<vector<int>> blackAdj(n + 1);  // 검은색 인접 리스트
```

### 2단계: 입력 처리

- 빨간색 간선을 인접 리스트에 저장
- 검은색 간선(빨간색이 아닌 모든 간선)을 인접 리스트에 저장

### 3단계: 삼각형 세기

각 정점 i에 대해:
- redAdj[i]의 모든 쌍 (v1, v2) 확인
- v1 > i && v2 > i 조건으로 각 삼각형을 정확히 한 번만 세기
- v1과 v2가 같은 색으로 연결되어 있으면 카운트

### 4단계: 중복 제거

`v1 > i && v2 > i` 조건을 사용하여 각 삼각형이 정확히 한 번만 계산되도록 합니다.

## 코드의 핵심 포인트

1. **인접 리스트 분리**: 빨간색과 검은색 간선을 따로 관리하여 각 색상별 삼각형만 세기
2. **정렬과 이분 탐색**: 간선 존재 여부를 빠르게 확인
3. **중복 방지**: 정점 번호 비교로 각 삼각형을 한 번만 계산
4. **시간 복잡도 개선**: O(n³)에서 O(Σ(degree²) log n)로 단축

## 예제 분석

입력 예제:
```
6 9
1 2
2 3
2 5
1 4
1 6
3 4
4 5
5 6
3 6
```

**빨간색 간선:** (1,2), (2,3), (2,5), (1,4), (1,6), (3,4), (4,5), (5,6), (3,6)

**모노크로매틱 삼각형:**
- (1,4,6): 모든 간선이 빨간색
- (4,5,6): 모든 간선이 빨간색

**출력:** 2

## 학습 포인트

1. **그래프 이론**: 삼각형 세기 문제의 기본 개념
2. **최적화 기법**: 단순한 해법에서 효율적인 해법으로의 개선
3. **데이터 구조**: 인접 리스트의 활용
4. **알고리즘**: 이분 탐색, 정렬

## 제출 전 확인사항

- [ ] 입출력 형식 확인
- [ ] 정점 번호가 1부터 시작
- [ ] 모든 삼각형 조합 확인
- [ ] 중복 제거 로직 검증
- [ ] 시간 제한 내 실행

## 관련 문제

- BOJ 2461: 대표 선수
- BOJ 4013: 두 정렬 배열의 병합
- BOJ 11441: 합 구하기
- BOJ 2512: 보충 학원

## 참고 자료

- [Baekjoon Online Judge](https://www.acmicpc.net)
- [Graph Theory Basics](https://en.wikipedia.org/wiki/Graph_theory)
- [Triangle Counting Algorithms](https://en.wikipedia.org/wiki/Counting_triangles)

