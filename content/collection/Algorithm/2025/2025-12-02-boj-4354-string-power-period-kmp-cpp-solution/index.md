---
title: "[Algorithm] C++ 백준 4354번: 문자열 제곱"
description: "문자열 s = a^n을 만족하는 최대 n을 KMP failure function으로 O(n)에 구합니다. 주기성 판별과 약수 계산을 통해 정확하게 해결하고, 엣지 케이스 처리까지 정리한 풀이입니다."
date: 2025-12-02
lastmod: 2025-12-02
categories:
- Algorithm
- String
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-4354
- cpp
- C++
- String
- 문자열
- KMP
- Knuth-Morris-Pratt
- Failure Function
- 실패함수
- Period
- 주기
- Periodicity
- 주기성
- String Matching
- 문자열 매칭
- Pattern Matching
- 패턴 매칭
- Prefix
- 접두사
- Suffix
- 접미사
- Edge Cases
- 코너 케이스
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Linear Time
- 선형시간
- Fast I/O
- 빠른 입출력
- Multiple Test Cases
- 다중 테스트
- Problem Solving
- 문제 해결
- Competitive Programming
- 경쟁프로그래밍
- String Theory
- 문자열 이론
- Divisor
- 약수
- String Period
- 문자열 주기
- Periodicity Detection
- 주기 감지
- Proof of Correctness
- 정당성 증명
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
image: "wordcloud.png"
---

## 문제 정보

- 문제: https://www.acmicpc.net/problem/4354
- 요약: 알파벳 소문자로 이루어진 문자열 s가 주어질 때, s = a^n을 만족하는 가장 큰 n을 찾는 프로그램을 작성합니다. 예를 들어 "ababab" = "ab"^3이므로 답은 3입니다.
- 제한: 문자열 길이는 1 이상 1,000,000 이하, 10개 이하의 테스트 케이스, 마지막 입력은 마침표(".")

## 입출력 형식/예제

```text
입력 예시
abcd
aaaa
ababab
.

출력 예시
1
4
3
```

**예제 설명**:
- "abcd": 모든 문자가 다르므로 "abcd"^1만 가능 → 1
- "aaaa": "a"^4 → 4
- "ababab": "ab"^3 → 3

## 접근 개요(아이디어 스케치)

- **핵심 관찰**: 문자열 s = a^n이려면 a의 길이는 len(s)의 약수여야 합니다.
- **KMP 활용**: KMP failure function의 마지막 값을 이용하면 최소 주기(period)를 O(n)에 구할 수 있습니다.
- **주기 판정**: len - failure[len-1] = period일 때, len % period == 0이면 s = a^(len/period)입니다.
- **효율성**: 모든 약수를 검사하는 것보다 KMP failure function을 활용하는 것이 더 빠릅니다.

## 알고리즘 설계

### KMP Failure Function을 이용한 주기 찾기

1. **Failure Function 구성**:
   - failure[i] = s[0..i]에서 prefix와 suffix가 일치하는 최대 길이
   - 예: "ababab"의 failure = [0,0,1,2,3,4]

2. **주기 계산**:
   - period = len - failure[len-1]
   - len이 period로 나누어떨어지면 s = a^(len/period)

3. **정확성 근거**:
   - failure[len-1] = k는 s[0..k-1] == s[len-k..len-1]을 의미합니다.
   - 이는 문자열의 처음 k개 문자와 마지막 k개 문자가 같다는 뜻입니다.
   - 따라서 period = len - k가 주기가 될 수 있는 최소값입니다.
   - len % period == 0이면 문자열이 완벽하게 주기적입니다.

## 복잡도

- 시간: O(n), KMP failure function 구성이 선형 시간
- 공간: O(n), failure function 배열 저장

## 구현 (C++)

```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    string s;
    while (cin >> s && s != ".") {
        int len = s.length();
        
        // KMP failure function 구성
        vector<int> failure(len, 0);
        for (int i = 1; i < len; i++) {
            int j = failure[i - 1];
            while (j > 0 && s[i] != s[j]) {
                j = failure[j - 1];
            }
            if (s[i] == s[j]) {
                j++;
            }
            failure[i] = j;
        }
        
        // 최소 주기 구하기
        int period = len - failure[len - 1];
        
        // 주기가 len을 나누어떨어뜨리는지 확인
        if (len % period == 0) {
            cout << len / period << "\n";
        } else {
            cout << 1 << "\n";
        }
    }
    
    return 0;
}
```

**코드 설명**

1. **입력 처리**:
   - 문자열을 읽고, "."일 때까지 반복 처리합니다.
   - cin >> s로 공백 없는 문자열을 입력받습니다.

2. **Failure Function 구성**:
   - failure[i]는 s[0..i]에서 prefix와 suffix가 일치하는 최대 길이입니다.
   - KMP 패턴 매칭 알고리즘의 전처리 단계와 동일합니다.

3. **주기 계산**:
   - period = len - failure[len-1]로 최소 주기를 구합니다.
   - 예: "ababab"에서 len=6, failure[5]=4이므로 period=2

4. **답 출력**:
   - len % period == 0이면 n = len / period
   - 아니면 n = 1 (문자열 자신의 1제곱만 가능)

## 코너 케이스 체크리스트

- 길이 1인 문자열 (예: "a") → 1 출력
- 모든 문자가 같은 경우 (예: "aaaa") → 문자열 길이 출력
- 모든 문자가 다른 경우 (예: "abcd") → 1 출력
- 길이가 소수인 경우 (예: "abcab", 길이 5) → 1 출력 (주기 없음)
- 부분적 반복 (예: "ababab") → 주기 찾기 정확히 수행
- 매우 큰 문자열 (최대 1,000,000) → O(n) 시간에 처리
- 10개 이하의 다중 테스트 케이스 → 마침표로 종료

## 제출 전 점검

- 문자열 입력이 "."인 경우 종료하는지 확인
- Failure function 초기화가 0으로 되어 있는지 확인
- 주기 계산 후 len % period == 0 조건 확인
- 출력 형식 (개행 문자 "\n" 사용) 확인
- Fast I/O 설정 (ios::sync_with_stdio, cin.tie) 확인
- 배열 인덱스가 0부터 len-1까지 올바르게 처리되는지 확인

## 참고자료/유사문제

- **KMP 알고리즘**: Knuth-Morris-Pratt pattern matching (O(n+m) 시간)
- **관련 개념**: String periodicity, Failure function (Z-algorithm도 유사하게 적용 가능)
- **유사 문제**: BOJ 1786 (찾기), BOJ 2180 (문자열 주기)
- **더 읽을거리**: "Introduction to Algorithms" - Chapter 32 (String Matching)


 