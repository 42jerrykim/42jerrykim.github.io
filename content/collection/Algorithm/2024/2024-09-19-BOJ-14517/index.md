---
image: "tmp_wordcloud.png"
description: "백준 14517번 문제는 주어진 문자열에서 부분수열 중 팰린드롬이 되는 경우의 수를 효율적으로 계산하는 동적 계획법(DP) 유형의 문제입니다. 분할 정복 및 중복 제거 방법론도 함께 고려해야 하며, DP 점화식 설계와 구간별 상태 관리가 중요한 문제로, 최적화된 구현이 필요합니다."
categories: Algorithm
date: "2024-09-19T00:00:00Z"

header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- DynamicProgramming
- Inclusion-Exclusion
- Implementation
- Optimization
- O(N^2)
- 2D DP Array
- Counting
- DPg
title: '[Algorithm] C++/Python 백준 14517번 : 팰린드롬 개수 구하기 (Large)'
---

팰린드롬(palindrome)이란 앞에서부터 읽으나 뒤에서부터 읽으나 같은 단어를 말한다. 예를 들어, 'aba'나 'a'는 팰린드롬이며, 'abaccbcb'나 'anavolimilana'는 팰린드롬이 아니다. 이번 문제에서는 주어진 문자열의 부분수열 중에서 팰린드롬이 되는 부분수열의 개수를 구하는 것이 목표이다. 부분수열이란 문자열에서 일부 문자를 선택하여 순서를 유지하면서 만든 새로운 문자열을 말하며, 공집합은 포함하지 않는다.

예를 들어, 문자열 'abb'의 모든 부분수열은 {'a'}, {'b'}, {'b'}, {'ab'}, {'ab'}, {'bb'}, {'abb'}이며, 이 중 팰린드롬인 부분수열은 {'a'}, {'b'}, {'b'}, {'bb'}으로 총 4개가 된다. 문제에서는 이러한 팰린드롬 부분수열의 개수를 구하고, 그 결과를 10,007로 나눈 나머지를 출력해야 한다.

문자열의 길이가 최대 1000이므로, 효율적인 알고리즘을 사용해야 한다. 이 문제는 동적 계획법(Dynamic Programming)을 이용하여 해결할 수 있으며, 부분문자열 간의 관계를 이용하여 팰린드롬 부분수열의 개수를 효율적으로 계산할 수 있다.

문제 : [https://www.acmicpc.net/problem/14517](https://www.acmicpc.net/problem/14517)

|![/assets/images/undefined/algorithm.png](/assets/images/undefined/algorithm.png)|
|:---:|
| |

## 접근 방식

이 문제를 해결하기 위해 동적 계획법(Dynamic Programming, DP)을 사용하였다. DP 테이블을 이용하여 문자열의 특정 구간에서의 팰린드롬 부분수열의 개수를 저장함으로써, 중복 계산을 피하고 효율적으로 문제를 해결할 수 있다.

**동적 계획법 (Dynamic Programming)**

1. **DP 테이블 정의**:
   - `dp[i][j]`를 문자열 `S`의 `i`번째 문자부터 `j`번째 문자까지의 부분 문자열에서 팰린드롬 부분수열의 개수라고 정의한다.

2. **기저 사례**:
   - `i == j`일 때, `dp[i][j] = 1`이다. 이는 단일 문자가 팰린드롬이기 때문이다.

3. **점화식**:
   - 만약 `S[i] == S[j]`라면:
     $dp[i][j] = dp[i+1][j] + dp[i][j-1] + 1 \mod 10007$
     여기서 `+1`은 `S[i]`와 `S[j]`가 같은 경우, 이 두 문자를 양 끝에 추가한 새로운 팰린드롬을 의미한다.
   
   - 만약 `S[i] != S[j]`라면:
     $dp[i][j] = (dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1] + 10007) \mod 10007$
     이는 `S[i]` 또는 `S[j]`를 포함하는 경우의 수를 합한 후, 중복된 경우를 빼준다. `+10007`은 음수가 되는 것을 방지하기 위한 조치이다.

4. **DP 테이블 채우기**:
   - 부분 문자열의 길이를 2부터 시작하여 점차 길이를 늘려가며 `dp[i][j]`를 계산한다.
   - 최종적으로 `dp[0][n-1]`이 전체 문자열에서의 팰린드롬 부분수열의 개수가 된다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <string>

using namespace std;

const int MOD = 10007;

int main(){
    string S;
    cin >> S; // 문자열 입력
    int n = S.length();
    // dp[i][j]는 S[i..j] 구간의 팰린드롬 부분수열의 개수를 저장
    vector<vector<int>> dp(n, vector<int>(n, 0));
    
    // 기저 사례: 단일 문자
    for(int i=0; i<n; ++i){
        dp[i][i] = 1;
    }
    
    // 부분 문자열의 길이를 2부터 n까지 증가시키며 DP 테이블을 채움
    for(int length=2; length<=n; ++length){
        for(int i=0; i + length -1 < n; ++i){
            int j = i + length -1;
            if(S[i] == S[j]){
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] + 1) % MOD;
            }
            else{
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1] + MOD) % MOD;
            }
        }
    }
    
    cout << dp[0][n-1] << "\n"; // 전체 문자열에서의 팰린드롬 부분수열의 개수 출력
    return 0;
}
```

**코드 설명**

1. **입력 처리**:
   - 문자열 `S`를 입력받는다.

2. **DP 테이블 초기화**:
   - 2차원 벡터 `dp`를 생성하여 모든 값을 0으로 초기화한다.
   - 단일 문자는 항상 팰린드롬이므로 `dp[i][i] = 1`로 설정한다.

3. **DP 테이블 채우기**:
   - 부분 문자열의 길이를 2부터 시작하여 `n`까지 증가시킨다.
   - 각 길이에 대해, 시작 인덱스 `i`를 고정하고 끝 인덱스 `j`를 계산한다.
   - `S[i]`와 `S[j]`가 같은 경우와 다른 경우에 따라 점화식을 적용하여 `dp[i][j]`를 계산한다.
   - 결과를 `MOD`로 나눈 나머지를 저장하여 값의 범위를 제한한다.

4. **결과 출력**:
   - 전체 문자열에서의 팰린드롬 부분수열의 개수는 `dp[0][n-1]`에 저장되어 있으므로 이를 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MOD 10007

int main(){
    char S[1001];
    scanf("%s", S); // 문자열 입력
    int n = strlen(S);
    // 2차원 배열 동적 할당
    int **dp = (int **)malloc(n * sizeof(int *));
    for(int i=0; i<n; ++i){
        dp[i] = (int *)malloc(n * sizeof(int));
        for(int j=0; j<n; ++j){
            dp[i][j] = 0;
        }
    }
    
    // 기저 사례: 단일 문자
    for(int i=0; i<n; ++i){
        dp[i][i] = 1;
    }
    
    // DP 테이블 채우기
    for(int length=2; length<=n; ++length){
        for(int i=0; i + length -1 < n; ++i){
            int j = i + length -1;
            if(S[i] == S[j]){
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] + 1) % MOD;
            }
            else{
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1] + MOD) % MOD;
            }
        }
    }
    
    printf("%d\n", dp[0][n-1]); // 결과 출력
    
    // 메모리 해제
    for(int i=0; i<n; ++i){
        free(dp[i]);
    }
    free(dp);
    
    return 0;
}
```

**코드 설명**

1. **입력 처리**:
   - `scanf`를 사용하여 문자열 `S`를 입력받는다.

2. **DP 테이블 초기화**:
   - 동적 메모리 할당을 통해 2차원 배열 `dp`를 생성하고 모든 값을 0으로 초기화한다.
   - 단일 문자는 항상 팰린드롬이므로 `dp[i][i] = 1`로 설정한다.

3. **DP 테이블 채우기**:
   - 부분 문자열의 길이를 2부터 시작하여 `n`까지 증가시킨다.
   - 각 길이에 대해, 시작 인덱스 `i`를 고정하고 끝 인덱스 `j`를 계산한다.
   - `S[i]`와 `S[j]`가 같은 경우와 다른 경우에 따라 점화식을 적용하여 `dp[i][j]`를 계산한다.
   - 결과를 `MOD`로 나눈 나머지를 저장하여 값의 범위를 제한한다.

4. **결과 출력**:
   - 전체 문자열에서의 팰린드롬 부분수열의 개수는 `dp[0][n-1]`에 저장되어 있으므로 이를 출력한다.

5. **메모리 해제**:
   - 동적 할당된 메모리를 해제하여 메모리 누수를 방지한다.

## Python 코드와 설명

```python
MOD = 10007

def count_palindromic_subsequences(S):
    n = len(S)
    # dp[i][j]는 S[i..j] 구간의 팰린드롬 부분수열의 개수를 저장
    dp = [[0]*n for _ in range(n)]
    
    # 기저 사례: 단일 문자
    for i in range(n):
        dp[i][i] = 1
    
    # 부분 문자열의 길이를 2부터 n까지 증가시키며 DP 테이블을 채움
    for length in range(2, n+1):
        for i in range(n - length +1):
            j = i + length -1
            if S[i] == S[j]:
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] + 1) % MOD
            else:
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1] + MOD) % MOD
    return dp[0][n-1]

if __name__ == "__main__":
    S = input().strip()
    result = count_palindromic_subsequences(S)
    print(result)
```

**코드 설명**

1. **입력 처리**:
   - `input().strip()`을 사용하여 문자열 `S`를 입력받는다.

2. **DP 테이블 초기화**:
   - 리스트 컴프리헨션을 이용하여 2차원 리스트 `dp`를 생성하고 모든 값을 0으로 초기화한다.
   - 단일 문자는 항상 팰린드롬이므로 `dp[i][i] = 1`로 설정한다.

3. **DP 테이블 채우기**:
   - 부분 문자열의 길이를 2부터 시작하여 `n`까지 증가시킨다.
   - 각 길이에 대해, 시작 인덱스 `i`를 고정하고 끝 인덱스 `j`를 계산한다.
   - `S[i]`와 `S[j]`가 같은 경우와 다른 경우에 따라 점화식을 적용하여 `dp[i][j]`를 계산한다.
   - 결과를 `MOD`로 나눈 나머지를 저장하여 값의 범위를 제한한다.

4. **결과 출력**:
   - 전체 문자열에서의 팰린드롬 부분수열의 개수는 `dp[0][n-1]`에 저장되어 있으므로 이를 출력한다.

## 결론

이번 문제는 동적 계획법을 이용하여 효율적으로 팰린드롬 부분수열의 개수를 구하는 방법을 학습할 수 있는 좋은 예제였다. 특히, 부분 문자열 간의 관계를 이용한 점화식 설정과 모듈러 연산을 통한 값의 범위 제한이 중요한 포인트였다. 다양한 언어(C++, Python)로 구현해보면서 알고리즘의 이해도를 높일 수 있었으며, 메모리 관리와 같은 세부적인 구현 방식의 차이를 비교해보는 것도 유익했다. 추가적인 최적화 방안으로는 메모리 사용을 줄이기 위해 1차원 DP 배열을 사용하는 방법 등이 있을 수 있다. 이번 문제를 통해 DP의 다양한 활용 방법과 문제 해결 전략을 더욱 깊이 이해할 수 있었다.