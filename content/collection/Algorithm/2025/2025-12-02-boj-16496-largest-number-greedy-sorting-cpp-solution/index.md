---
title: "[Algorithm] C++ 백준 16496번: 큰 수 만들기"
description: "주어진 음이 아닌 정수들을 재배열하여 만들 수 있는 가장 큰 수를 그리디 정렬으로 O(n log n)에 구합니다. 커스텀 비교함수(a+b vs b+a)와 엣지 케이스 처리까지 한 문서에 정리했습니다."
date: 2025-12-02
lastmod: 2025-12-02
categories:
- Algorithm
- Greedy
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-16496
- cpp
- C++
- Greedy
- 그리디
- Sorting
- 정렬
- String
- 문자열
- Custom Comparator
- 커스텀 비교함수
- Lexicographical
- 사전순
- Edge Cases
- 코너 케이스
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Proof of Correctness
- 정당성 증명
- Greedy Algorithm
- 그리디 알고리즘
- Problem Solving
- 문제 해결
- Competitive Programming
- 경쟁프로그래밍
- Data Structures
- 자료구조
- Vector
- 벡터
- Transitive
- 이행성
- Local Optimality
- 국소 최적성
- Global Optimality
- 전역 최적성
- Number Arrangement
- 숫자 배열
- Concatenation
- 연결
- String Comparison
- 문자열 비교
- Zero Handling
- 0 처리
- Leading Zeros
- 선행 0
- Integer Parsing
- 정수 파싱
- Fast I/O
- 빠른 입출력
- Testing
- 테스트
- Pitfalls
- 실수 포인트
- Complexity Analysis
- 복잡도 분석
image: "wordcloud.png"
---

## 문제 정보

- 문제: https://www.acmicpc.net/problem/16496
- 요약: 음이 아닌 정수 N개를 배열하여 만들 수 있는 가장 큰 수를 구합니다. 수는 공백으로 구분되고, 1,000,000,000 이하의 음이 아닌 정수입니다. 0을 제외한 나머지 수는 0으로 시작하지 않습니다.
- 제한: N ≤ 1,000, 각 수 ≤ 1,000,000,000, 시간 2초, 메모리 512MB

## 입출력 형식/예제

```text
입력 예시 1
5
3 30 34 5 9

출력 예시 1
9534330
```

```text
입력 예시 2
5
0 0 0 0 1

출력 예시 2
10000
```

## 접근 개요(아이디어 스케치)

- 핵심 관찰: 두 수 `a`와 `b`를 배열할 때, `a+b`와 `b+a`를 비교하여 더 큰 쪽을 앞에 배치합니다. 예를 들어 "3"과 "30"의 경우 "330" > "303"이므로 "3"을 앞에 배치합니다.
- 그리디 선택: 이 비교 함수로 모든 수를 정렬하고, 앞에서부터 순서대로 이어붙입니다.
- 엣지 케이스: 모든 수가 0이면 "0"을 출력하고, 그렇지 않으면 결과 그대로 출력합니다.
- 시간 복잡도: 정렬 O(N log N × L), 여기서 L은 문자열 비교 비용입니다.

## 알고리즘 설계

1) **비교 함수:** `compare(a, b) = (a + b > b + a)`. 이 함수는 전이적(transitive) 성질을 만족합니다.
2) **정렬:** `sort` 함수에 커스텀 비교자를 적용하여 문자열 벡터를 정렬합니다.
3) **연결:** 정렬된 문자열들을 순서대로 이어붙여 결과 문자열을 생성합니다.
4) **0 처리:** 결과 문자열의 첫 문자가 '0'이면 "0"만 출력합니다.

### 올바름 근거(요지)

- **비교 함수의 전이성:** `compare(a, b)`가 true이고 `compare(b, c)`가 true이면, `compare(a, c)`도 true입니다. 이는 수학적으로 증명 가능하며, 정렬의 정확성을 보장합니다.
- **그리디 선택 성질:** 각 위치에서 국소적으로 최적의 선택(가장 큰 연결 결과를 만드는 배치)이 전역 최적해를 도출합니다.
- **정당성:** 어떤 두 인접한 수의 배치 순서를 바꾸면 결과가 더 작아지므로, 정렬된 배열의 순서대로 이어붙인 결과가 최대값입니다.

## 복잡도

- 시간: O(N log N × L), 여기서 N은 수의 개수, L은 평균 문자열 길이입니다.
- 공간: O(N × L), 문자열 벡터 저장 공간

## 구현 (C++)

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

// 사용자 정의 비교 함수: 두 문자열을 이어붙였을 때 더 큰 값을 만드는 순서로 정렬
bool compare(const string &a, const string &b) {
    return a + b > b + a;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n;
    cin >> n;
    
    vector<string> numbers(n);
    for (int i = 0; i < n; i++) {
        cin >> numbers[i];
    }
    
    // 커스텀 비교 함수로 정렬
    sort(numbers.begin(), numbers.end(), compare);
    
    // 결과 문자열 생성
    string result = "";
    for (const string &num : numbers) {
        result += num;
    }
    
    // 모든 숫자가 0인 경우 처리 (예: 0, 0, 0 -> "000"이 아닌 "0" 출력)
    if (result[0] == '0') {
        cout << "0\n";
    } else {
        cout << result << "\n";
    }
    
    return 0;
}
```

**코드 설명**

1. **헤더 및 입력:**
   - `#include <bits/stdc++.h>`로 표준 라이브러리 포함
   - Fast I/O 설정으로 입출력 속도 향상
   - `n`과 `n`개의 숫자를 문자열 배열에 저장

2. **비교 함수:**
   - `a + b`와 `b + a`를 문자열 연결로 비교합니다.
   - 결과가 더 크면 `a`를 앞에 배치합니다.

3. **정렬:**
   - `sort` 함수와 커스텀 비교자 `compare`를 사용하여 정렬합니다.

4. **결과 생성:**
   - 정렬된 순서대로 모든 문자열을 이어붙입니다.

5. **엣지 케이스 처리:**
   - 결과 문자열의 첫 문자가 '0'이면 (모든 숫자가 0인 경우), "0"만 출력합니다.

## 코너 케이스 체크리스트

- 모든 입력이 0인 경우 (예: 0, 0, 0) → "0" 출력되는지 확인
- 한 자리 숫자만 있는 경우 (예: 3, 5, 9) → 내림차순 정렬되는지 확인
- 자릿수가 다른 수들의 배치 (예: 3, 30) → 커스텀 비교 적용 확인
- 1개의 수만 있는 경우 → 그 수 그대로 출력
- 0과 양수가 섞인 경우 (예: 0, 0, 1) → "10000" 출력 확인
- 큰 숫자들 (최대 1,000,000,000) → 오버플로 없음 확인

## 제출 전 점검

- Fast I/O 설정 (ios::sync_with_stdio, cin.tie) 확인
- 비교 함수에서 문자열 연결 연산 정확성 확인
- 0 처리 로직이 첫 문자만 확인하는지 검증 (모든 0인 경우만 "0")
- 개행 문자 처리 확인

## 참고자료/유사문제

- 문제: https://www.acmicpc.net/problem/16496
- 유사 알고리즘: 그리디 알고리즘, 커스텀 정렬, 문자열 처리
- 관련 문제: Largest Number (LeetCode 179)


