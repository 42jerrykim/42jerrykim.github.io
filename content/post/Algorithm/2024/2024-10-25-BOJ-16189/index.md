---
title: "[Algorithm] C++/Python 백준 16189번 : Repetitive Palindrome"
categories: 
- Algorithm
- Strings
tags:
- String
- Palindrome
- Implementation
- O(N)
- Problem Type: Implementation
image: "tmp_wordcloud.png"
date: 2024-10-25
---

문자열과 정수 \( k \)가 주어질 때, 문자열 \( s \)를 \( k \)번 반복하여 새로운 문자열 \( t \)를 만든다. 이때 \( t \)가 회문(palindrome)인지 여부를 판단하는 문제이다. 회문이란 앞에서 읽으나 뒤에서 읽으나 같은 문자열을 말한다. 예를 들어, "abba"는 회문이지만 "abc"는 회문이 아니다. 이 문제에서는 \( t \)가 회문인지 아닌지를 판단하여 "YES" 또는 "NO"를 출력해야 한다.

이 문제의 핵심은 매우 큰 \( k \) 값(최대 \( 10^{18} \))에도 불구하고 효율적으로 \( t \)의 회문 여부를 판단하는 것이다. 문자열 \( s \)의 길이가 최대 \( 250,000 \)이므로, 시간 복잡도를 고려하여 최적의 알고리즘을 선택해야 한다.

문제를 해결하기 위해서는 \( t \)를 실제로 생성하지 않고도 \( t \)가 회문인지 판단할 수 있는 방법을 찾아야 한다. 이는 \( t \)가 \( s \)의 반복으로 구성되었을 때, \( s \) 자체가 회문인지 여부에 따라 \( t \)의 회문 여부가 결정된다는 점에서 가능하다. 따라서 \( s \)가 회문이라면 어떤 횟수로 반복하더라도 \( t \)는 회문이 되고, 그렇지 않다면 \( t \) 역시 회문이 될 수 없다.

문제를 해결하는 접근 방식과 각 프로그래밍 언어별 구현 방법을 상세히 살펴보겠다.

문제 : [https://www.acmicpc.net/problem/16189](https://www.acmicpc.net/problem/16189)

## 문제 설명

주어진 문자열 \( s \)와 정수 \( k \)에 대해, \( s \)를 \( k \)번 반복하여 새로운 문자열 \( t \)를 만든다. 예를 들어, \( s = "abc" \)이고 \( k = 3 \)이라면 \( t = "abcabcabc" \)가 된다. 이때 \( t \)가 회문인지 아닌지를 판단해야 한다.

입력으로는 첫 번째 줄에 소문자로 이루어진 문자열 \( s \)가 주어지며, 두 번째 줄에는 정수 \( k \)가 주어진다. 문자열 \( s \)의 길이는 최대 \( 250,000 \)이며, \( k \)는 최대 \( 10^{18} \)이다.

출력으로는 \( t \)가 회문이면 "YES"를, 그렇지 않으면 "NO"를 출력해야 한다.

### 예제

**예제 입력 1**
```
abc
3
```

**예제 출력 1**
```
NO
```

**예제 입력 2**
```
abba
1
```

**예제 출력 2**
```
YES
```

## 접근 방식

문제의 핵심은 \( t \)가 회문인지 판단하는 것이다. \( t \)는 \( s \)를 \( k \)번 반복한 문자열이므로, \( t \)가 회문이 되기 위해서는 \( s \) 자체가 회문이어야 한다. 이는 \( s \)를 반복하여 만든 \( t \)의 양 끝에서부터 대응되는 문자가 항상 같아야 하기 때문이다.

따라서, \( s \)가 회문인지 먼저 확인한다. \( s \)가 회문이라면 어떤 \( k \)에 대해서도 \( t \)는 회문이 되며, 그렇지 않다면 \( t \)는 회문이 될 수 없다.

이 접근 방식을 통해 문제를 해결할 수 있으며, 시간 복잡도는 \( O(N) \)으로 효율적이다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    string s;
    cin >> s;          // 문자열 s 입력
    long long k;
    cin >> k;          // 정수 k 입력
    
    bool is_palindrome = true;
    int n = s.length();
    
    // 문자열 s가 회문인지 확인
    for(int i = 0; i < n / 2; ++i){
        if(s[i] != s[n - 1 - i]){
            is_palindrome = false;
            break;
        }
    }
    
    if(is_palindrome){
        cout << "YES";
    }
    else{
        cout << "NO";
    }
}
```

### 코드 설명

1. **입출력 최적화**: `ios::sync_with_stdio(false);`와 `cin.tie(0);`을 사용하여 C++의 표준 입출력과 C의 입출력 간의 동기화를 끊고, `cin`과 `cout`의 묶음을 해제하여 입출력 속도를 향상시킨다.
2. **입력 받기**: 문자열 `s`와 정수 `k`를 입력받는다.
3. **회문 여부 확인**:
   - 문자열의 길이 `n`을 구한다.
   - 문자열의 첫 절반과 마지막 절반을 비교하여 회문인지 확인한다.
   - 만약 어떤 위치에서 문자들이 다르면 `is_palindrome`을 `false`로 설정하고 반복을 종료한다.
4. **결과 출력**: `is_palindrome`이 `true`이면 "YES"를, 그렇지 않으면 "NO"를 출력한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
    char s[250001];
    long long k;
    
    // 문자열 s 입력
    scanf("%s", s);
    // 정수 k 입력
    scanf("%lld", &k);
    
    int n = strlen(s);
    int left = 0;
    int right = n - 1;
    int is_palindrome = 1;
    
    // 문자열 s가 회문인지 확인
    while(left < right){
        if(s[left] != s[right]){
            is_palindrome = 0;
            break;
        }
        left++;
        right--;
    }
    
    if(is_palindrome){
        printf("YES");
    }
    else{
        printf("NO");
    }
    
    return 0;
}
```

### 코드 설명

1. **입력 받기**: `scanf`를 사용하여 문자열 `s`와 정수 `k`를 입력받는다.
2. **문자열 길이 구하기**: `strlen` 함수를 사용하여 문자열 `s`의 길이 `n`을 구한다.
3. **회문 여부 확인**:
   - 두 포인터 `left`와 `right`를 문자열의 양 끝에 설정한다.
   - `left`가 `right`보다 작을 동안 다음을 반복한다:
     - `s[left]`와 `s[right]`를 비교한다.
     - 만약 다르면 `is_palindrome`을 `0`으로 설정하고 반복을 종료한다.
     - 동일하면 `left`를 증가시키고 `right`를 감소시킨다.
4. **결과 출력**: `is_palindrome`이 `1`이면 "YES"를, 그렇지 않으면 "NO"를 출력한다.

이 코드는 C++의 표준 라이브러리를 사용하지 않고, C의 표준 입출력과 문자열 함수를 사용하여 구현되었다. 이는 메모리 사용을 최소화하고, 특정 환경에서의 컴파일 속도를 향상시킬 수 있다.

## Python 코드와 설명

```python
def is_repetitive_palindrome(s, k):
    # 문자열 s가 회문인지 확인
    return "YES" if s == s[::-1] else "NO"

# 입력 받기
s = input().strip()
k = int(input())

# 결과 출력
print(is_repetitive_palindrome(s, k))
```

### 코드 설명

1. **회문 여부 확인 함수**:
   - `s[::-1]`을 사용하여 문자열 `s`를 뒤집는다.
   - 원래의 `s`와 뒤집은 문자열을 비교하여 동일하면 "YES"를, 그렇지 않으면 "NO"를 반환한다.
2. **입력 받기**:
   - `input().strip()`을 사용하여 문자열 `s`를 입력받고, 양쪽 공백을 제거한다.
   - `int(input())`을 사용하여 정수 `k`를 입력받는다.
3. **결과 출력**: `is_repetitive_palindrome` 함수를 호출하여 결과를 출력한다.

이 Python 코드는 간결하고 효율적이며, 문자열 슬라이싱을 활용하여 회문 여부를 빠르게 판단할 수 있다. 또한, \( k \)의 값은 실제로 사용되지 않으므로, \( s \)만을 검사하여 결과를 도출한다.

## 결론

이번 문제는 \( k \)의 값이 매우 클 수 있지만, 실제로는 \( s \)의 회문 여부만을 판단하면 되기 때문에 효율적으로 해결할 수 있었다. \( s \)가 회문이라면 어떤 횟수로 반복하더라도 \( t \)는 회문이 되고, 그렇지 않다면 \( t \)도 회문이 될 수 없다는 점을 이용하여 문제를 단순화할 수 있었다.

추가적으로, 다양한 프로그래밍 언어로 구현함으로써 각 언어의 입출력 방식과 문자열 처리 방법에 대한 이해를 높일 수 있었다. 특히, C++에서는 표준 라이브러리를 활용한 방법과 라이브러리를 사용하지 않는 방법 두 가지를 모두 구현하여, 상황에 따라 적절한 방법을 선택할 수 있는 능력을 기를 수 있었다.

이번 문제를 통해 문자열 처리와 효율적인 알고리즘 설계의 중요성을 다시 한번 깨달았으며, 앞으로도 유사한 문제들을 해결할 때 이러한 접근 방식을 응용할 수 있을 것으로 기대된다.