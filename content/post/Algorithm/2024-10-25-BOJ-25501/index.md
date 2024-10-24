---
title: "[Algorithm] C++/Python 백준 25501번 : 재귀의 귀재"
categories: 
- Algorithm
- Recursion
- String
- Implementation
tags:
- Recursion
- String
- Implementation
- Counting
- O(N)
- Recursive Algorithms
- Problem Solving
image: "tmp_wordcloud.png"
date: 2024-04-27
---

재귀는 많은 알고리즘 문제에서 강력한 도구로 활용된다. 특히 문자열 처리 문제에서 재귀를 사용하면 간결하고 효율적인 해결책을 제시할 수 있다. 이번 포스트에서는 백준의 문제 **25501번: 재귀의 귀재**를 통해 재귀 함수를 이용한 팰린드롬 판별과 재귀 호출 횟수 세는 방법을 알아보겠다.

문제 : [https://www.acmicpc.net/problem/25501](https://www.acmicpc.net/problem/25501)

## 문제 설명

백준 온라인 저지의 **25501번: 재귀의 귀재** 문제는 주어진 문자열이 팰린드롬인지 여부를 판단하고, 이를 판별하는 과정에서 재귀 함수가 몇 번 호출되는지를 세는 문제이다. 팰린드롬이란, 앞에서부터 읽었을 때와 뒤에서부터 읽었을 때가 같은 문자열을 말한다. 예를 들어, "ABBA"나 "ABABA"는 팰린드롬이지만, "ABCA"는 팰린드롬이 아니다.

문제는 다음과 같은 방식으로 진행된다:

1. 문자열 S가 주어진다.
2. 재귀 함수를 사용하여 S가 팰린드롬인지 판별한다.
3. 재귀 함수가 호출된 횟수를 세어 출력한다.

입력으로는 테스트케이스의 수 T와 그에 따른 T개의 문자열 S가 주어지며, 각 문자열에 대해 팰린드롬 여부와 재귀 호출 횟수를 출력해야 한다.

## 접근 방식

이 문제를 해결하기 위해 재귀 함수를 사용하여 문자열의 양 끝 문자부터 비교해 나가는 방식을 채택하였다. 재귀 함수는 문자열의 좌측 인덱스 l과 우측 인덱스 r을 받아 다음과 같이 동작한다:

1. **기본 사례(Base Case)**: 
   - 만약 l이 r 이상이 되면, 모든 문자가 일치했으므로 팰린드롬이다.
2. **재귀 단계(Recursive Step)**:
   - S[l]과 S[r]이 다르면, 더 이상 확인할 필요 없이 팰린드롬이 아니다.
   - S[l]과 S[r]이 같다면, l을 증가시키고 r을 감소시켜 다음 문자들을 비교하기 위해 재귀 호출을 한다.

또한, 재귀 호출의 횟수를 세기 위해 전역 변수나 참조 변수를 활용하여 호출될 때마다 카운트를 증가시킨다.

이 접근 방식은 문자열의 길이에 비례하는 시간 복잡도 O(N)을 가지며, N은 문자열의 길이이다. 이는 문자열의 절반만을 확인하면 되기 때문에 효율적이다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

// 재귀 호출 횟수를 세기 위한 전역 변수
int cnt;

// 재귀 함수를 통해 팰린드롬 여부를 판별
int recursion(const string &s, int l, int r) {
    cnt++; // 함수 호출 시 카운트 증가
    if (l >= r) return 1; // 기본 사례: 모든 문자가 일치
    if (s[l] != s[r]) return 0; // 문자가 다르면 팰린드롬 아님
    return recursion(s, l + 1, r - 1); // 다음 문자들 비교를 위해 재귀 호출
}

// 팰린드롬 여부를 판단하는 함수
int isPalindrome(const string &s) {
    return recursion(s, 0, s.size() - 1);
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    
    int T;
    cin >> T;
    while(T--){
        string S;
        cin >> S;
        cnt = 0; // 카운트 초기화
        int result = isPalindrome(S);
        cout << result << " " << cnt << "\n";
    }
}
```

### 코드의 동작 단계별 설명

1. **입력 및 초기화**:
   - `ios::sync_with_stdio(false);`와 `cin.tie(NULL);`을 통해 입출력 속도를 최적화한다.
   - 테스트케이스의 수 T를 입력받는다.

2. **테스트케이스 처리**:
   - 각 테스트케이스마다 문자열 S를 입력받는다.
   - 재귀 호출 횟수를 세기 위해 `cnt`를 0으로 초기화한다.
   - `isPalindrome` 함수를 호출하여 팰린드롬 여부를 판단하고, 그 결과와 재귀 호출 횟수를 출력한다.

3. **재귀 함수 `recursion`**:
   - 함수가 호출될 때마다 `cnt`를 1 증가시킨다.
   - 현재 좌측 인덱스 l이 우측 인덱스 r보다 크거나 같으면 모든 문자가 일치한 것이므로 1을 반환한다.
   - S[l]과 S[r]이 다르면 팰린드롬이 아니므로 0을 반환한다.
   - S[l]과 S[r]이 같으면, l을 증가시키고 r을 감소시켜 다음 문자들을 비교하기 위해 재귀 호출을 한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <string.h>

// 재귀 호출 횟수를 세기 위한 전역 변수
int cnt;

// 재귀 함수를 통해 팰린드롬 여부를 판별
int recursion(const char *s, int l, int r) {
    cnt++; // 함수 호출 시 카운트 증가
    if (l >= r) return 1; // 기본 사례: 모든 문자가 일치
    if (s[l] != s[r]) return 0; // 문자가 다르면 팰린드롬 아님
    return recursion(s, l + 1, r - 1); // 다음 문자들 비교를 위해 재귀 호출
}

// 팰린드롬 여부를 판단하는 함수
int isPalindrome(const char *s) {
    return recursion(s, 0, strlen(s) - 1);
}

int main(){
    int T;
    scanf("%d", &T);
    while(T--){
        char S[1001];
        scanf("%s", S);
        cnt = 0; // 카운트 초기화
        int result = isPalindrome(S);
        printf("%d %d\n", result, cnt);
    }
}
```

### 코드의 동작 단계별 설명

1. **입력 및 초기화**:
   - `scanf`를 사용하여 테스트케이스의 수 T를 입력받는다.

2. **테스트케이스 처리**:
   - 각 테스트케이스마다 문자열 S를 입력받는다. 문자열의 최대 길이가 1000이므로 `char S[1001];`로 선언한다.
   - 재귀 호출 횟수를 세기 위해 `cnt`를 0으로 초기화한다.
   - `isPalindrome` 함수를 호출하여 팰린드롬 여부를 판단하고, 그 결과와 재귀 호출 횟수를 `printf`를 통해 출력한다.

3. **재귀 함수 `recursion`**:
   - 함수가 호출될 때마다 `cnt`를 1 증가시킨다.
   - 현재 좌측 인덱스 l이 우측 인덱스 r보다 크거나 같으면 모든 문자가 일치한 것이므로 1을 반환한다.
   - S[l]과 S[r]이 다르면 팰린드롬이 아니므로 0을 반환한다.
   - S[l]과 S[r]이 같으면, l을 증가시키고 r을 감소시켜 다음 문자들을 비교하기 위해 재귀 호출을 한다.

## Python 코드와 설명

```python
import sys
sys.setrecursionlimit(10000)

# 재귀 호출 횟수를 세기 위한 전역 변수
cnt = 0

def recursion(s, l, r):
    global cnt
    cnt += 1  # 함수 호출 시 카운트 증가
    if l >= r:
        return 1  # 기본 사례: 모든 문자가 일치
    if s[l] != s[r]:
        return 0  # 문자가 다르면 팰린드롬 아님
    return recursion(s, l + 1, r - 1)  # 다음 문자들 비교를 위해 재귀 호출

def isPalindrome(s):
    return recursion(s, 0, len(s) - 1)

def main():
    input = sys.stdin.read
    data = input().split()
    T = int(data[0])
    for i in range(1, T + 1):
        S = data[i]
        global cnt
        cnt = 0  # 카운트 초기화
        result = isPalindrome(S)
        print(result, cnt)

if __name__ == "__main__":
    main()
```

### 코드의 동작 단계별 설명

1. **입력 및 초기화**:
   - `sys.setrecursionlimit(10000)`을 통해 재귀 한도를 늘려 긴 문자열도 처리할 수 있도록 한다.
   - 표준 입력을 읽어 모든 데이터를 한 번에 받아 처리한다.

2. **테스트케이스 처리**:
   - 첫 번째 입력 값 T를 테스트케이스의 수로 설정한다.
   - 각 테스트케이스마다 문자열 S를 입력받고, 재귀 호출 횟수를 세기 위해 `cnt`를 0으로 초기화한다.
   - `isPalindrome` 함수를 호출하여 팰린드롬 여부를 판단하고, 그 결과와 재귀 호출 횟수를 출력한다.

3. **재귀 함수 `recursion`**:
   - 함수가 호출될 때마다 `cnt`를 1 증가시킨다.
   - 현재 좌측 인덱스 l이 우측 인덱스 r보다 크거나 같으면 모든 문자가 일치한 것이므로 1을 반환한다.
   - S[l]과 S[r]이 다르면 팰린드롬이 아니므로 0을 반환한다.
   - S[l]과 S[r]이 같으면, l을 증가시키고 r을 감소시켜 다음 문자들을 비교하기 위해 재귀 호출을 한다.

## 결론

이번 문제를 통해 재귀 함수를 사용하여 문자열이 팰린드롬인지 여부를 판단하고, 재귀 호출의 횟수를 효율적으로 세는 방법을 배웠다. 재귀는 코드의 가독성을 높이고, 복잡한 문제를 단순하게 해결할 수 있는 강력한 도구이다. 하지만 재귀 호출의 깊이가 깊어질 경우 스택 오버플로우가 발생할 수 있으므로, 필요한 경우 재귀 한도를 조정하거나 반복문으로 대체하는 방안도 고려해야 한다. 또한, 재귀 호출 횟수를 세는 방식은 전역 변수를 사용하거나 함수의 인자로 참조 변수를 전달하는 방법으로 구현할 수 있으며, 이는 문제의 요구사항에 따라 적절히 선택해야 한다. 이번 문제를 통해 재귀의 활용과 효율적인 구현 방법에 대해 깊이 이해할 수 있었다.