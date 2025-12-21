---
title: "[Algorithm] C++/Python 백준 2711번 : 오타맨 고창영"
description: "백준 2711번 오타맨 고창영 문제는 주어진 문자열에서 특정 위치의 오타를 제거해 올바른 문자열로 복구하는 단순 구현 문제입니다. 입력 형식 파싱, 인덱스 조정, 문자열 처리 등을 연습할 수 있으며, 테스트 케이스마다 1-based 위치로 오타 문자를 제외한 결과 문자열을 출력해야 하는 것이 특징입니다. C++/Python의 슬라이싱, 문자열 조작 기법에 대한 이해를 향상시킬 수 있습니다."
categories: 
- Algorithm
- Implementation
- String 
tags:
- Implementation
- StringManipulation
- C++
- Python
- BruteForce
- O(T * N)
- Array
- InputParsing
- ProblemSolving
image: "tmp_wordcloud.png"
date: 2024-10-17
---

고창영은 맨날 오타를 낸다. 오타맨 고창영은 타이핑할 때 항상 한 글자를 틀리게 치는데, 이번에는 특정 위치에서 오타를 냈다. 이러한 상황에서 고창영이 실수로 잘못 입력한 문장을 주면, 오타를 제거한 올바른 문자열을 출력해야 한다. 이 문제는 문자열 처리와 구현 능력을 요구하며, 간단한 알고리즘을 통해 해결할 수 있다.

문제 : [https://www.acmicpc.net/problem/2711](https://www.acmicpc.net/problem/2711)

## 문제 설명

고창영은 오타를 내는 것을 평소에 자주 하는데, 이번에는 입력한 문자열의 특정 위치에서 정확히 한 글자를 잘못 입력했다. 각 테스트 케이스마다 오타가 발생한 위치와 그 문자열이 주어질 때, 오타를 제거한 올바른 문자열을 출력하는 프로그램을 작성해야 한다. 

입력의 첫 줄에는 테스트 케이스의 개수 `T`가 주어진다. 각 테스트 케이스는 한 줄로 구성되며, 첫 번째 숫자는 오타가 발생한 위치 `P`를 나타내고, 그 다음에 잘못 입력된 문자열 `S`가 주어진다. 문자열의 첫 글자는 1번째 문자로 간주되며, 문자열의 길이는 최대 80자이다. 모든 문자열은 대문자로만 이루어져 있으며, 오타의 위치 `P`는 항상 문자열의 길이보다 작거나 같다. 각 테스트 케이스마다 오타가 제거된 문자열을 출력하면 된다.

예를 들어, 오타 위치가 4이고 문자열이 "MISSPELL"이라면, 4번째 문자인 'S'를 제거하여 "MISPELL"을 출력해야 한다.

## 접근 방식

이 문제는 주어진 문자열에서 특정 위치의 문자를 제거하는 단순한 구현 문제이다. 각 테스트 케이스마다 다음 단계를 수행하면 된다:

1. **입력 받기**: 테스트 케이스의 개수 `T`를 입력받고, 각 테스트 케이스마다 오타 위치 `P`와 문자열 `S`를 입력받는다.
2. **오타 제거**: 문자열 `S`에서 `P`번째 문자를 제거한다. C++에서는 `erase` 함수를 사용하여 쉽게 제거할 수 있다.
3. **출력하기**: 수정된 문자열을 출력한다.

문자열의 인덱스는 보통 0부터 시작하지만, 문제에서 주어진 위치는 1부터 시작하므로, 실제 제거할 인덱스는 `P-1`이 된다. 이를 통해 정확하게 오타를 제거할 수 있다.

시간 복잡도는 각 테스트 케이스마다 문자열의 특정 위치에서 문자를 제거하는 작업이므로, 전체 시간 복잡도는 O(T * N)이 된다. 여기서 `T`는 테스트 케이스의 수, `N`은 각 문자열의 최대 길이(80)이다. 이 범위 내에서는 효율적으로 동작할 수 있다.

## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    
    int T;
    cin >> T; // 테스트 케이스의 개수 입력
    
    while(T--){
        int P;
        string S;
        cin >> P >> S; // 오타 위치와 문자열 입력
        
        // 오타 위치가 유효한지 확인 후 제거
        if(P >= 1 && P <= S.length()){
            S.erase(P-1, 1); // 1-based 인덱스를 0-based로 변환하여 문자 제거
        }
        
        cout << S << "\n"; // 결과 출력
    }
}
```

### 코드 설명

1. **입출력 속도 최적화**:
    ```cpp
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    ```
    - `ios::sync_with_stdio(false)`와 `cin.tie(NULL)`을 사용하여 C++의 표준 입출력 속도를 최적화한다. 이를 통해 대량의 입력을 빠르게 처리할 수 있다.

2. **테스트 케이스 입력**:
    ```cpp
    int T;
    cin >> T; // 테스트 케이스의 개수 입력
    ```
    - 첫 번째 입력으로 테스트 케이스의 개수 `T`를 입력받는다.

3. **각 테스트 케이스 처리**:
    ```cpp
    while(T--){
        int P;
        string S;
        cin >> P >> S; // 오타 위치와 문자열 입력
        
        // 오타 위치가 유효한지 확인 후 제거
        if(P >= 1 && P <= S.length()){
            S.erase(P-1, 1); // 1-based 인덱스를 0-based로 변환하여 문자 제거
        }
        
        cout << S << "\n"; // 결과 출력
    }
    ```
    - `while(T--)` 루프를 통해 모든 테스트 케이스를 처리한다.
    - 각 테스트 케이스마다 오타 위치 `P`와 문자열 `S`를 입력받는다.
    - `S.erase(P-1, 1)`을 사용하여 `P`번째 문자를 제거한다. `erase` 함수는 첫 번째 인자로 시작 인덱스, 두 번째 인자로 제거할 문자 수를 받는다.
    - 수정된 문자열 `S`를 출력한다.

### 예제 실행

**입력:**
```
4
4 MISSPELL
1 PROGRAMMING
7 CONTEST
3 BALLOON
```

**출력:**
```
MISPELL
ROGRAMMING
CONTES
BALOON
```

## C++ without library 코드와 설명

다음은 C++ 표준 라이브러리를 사용하지 않고, `stdio.h`와 `malloc.h`만을 사용하여 문제를 해결한 코드이다.

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
    int T;
    scanf("%d", &T); // 테스트 케이스의 개수 입력
    
    while(T--){
        int P;
        char S[81];
        scanf("%d %s", &P, S); // 오타 위치와 문자열 입력
        
        int len = strlen(S);
        if(P >= 1 && P <= len){
            // P번째 문자를 제거하기 위해 이후 문자들을 한 칸씩 앞으로 이동
            for(int i = P-1; i < len; i++){
                S[i] = S[i+1];
            }
        }
        
        printf("%s\n", S); // 결과 출력
    }
}
```

### 코드 설명

1. **입력 받기**:
    ```c
    int T;
    scanf("%d", &T); // 테스트 케이스의 개수 입력
    ```
    - `scanf`를 사용하여 테스트 케이스의 개수 `T`를 입력받는다.

2. **각 테스트 케이스 처리**:
    ```c
    while(T--){
        int P;
        char S[81];
        scanf("%d %s", &P, S); // 오타 위치와 문자열 입력
        
        int len = strlen(S);
        if(P >= 1 && P <= len){
            // P번째 문자를 제거하기 위해 이후 문자들을 한 칸씩 앞으로 이동
            for(int i = P-1; i < len; i++){
                S[i] = S[i+1];
            }
        }
        
        printf("%s\n", S); // 결과 출력
    }
    ```
    - 각 테스트 케이스마다 오타 위치 `P`와 문자열 `S`를 `scanf`로 입력받는다.
    - 문자열의 길이를 `strlen`으로 구한다.
    - `P`번째 문자를 제거하기 위해, `P-1` 인덱스부터 문자열 끝까지 각 문자를 한 칸씩 앞으로 이동시킨다.
    - 수정된 문자열 `S`를 `printf`로 출력한다.

### 예제 실행

**입력:**
```
4
4 MISSPELL
1 PROGRAMMING
7 CONTEST
3 BALLOON
```

**출력:**
```
MISPELL
ROGRAMMING
CONTES
BALOON
```

## Python 코드와 설명

다음은 Python을 사용하여 문제를 해결한 코드이다.

```python
import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    T = int(data[0]) # 테스트 케이스의 개수 입력
    index = 1
    
    for _ in range(T):
        P = int(data[index])
        S = data[index + 1]
        index += 2
        
        # P번째 문자를 제거하기 위해 슬라이싱을 사용
        if 1 <= P <= len(S):
            S = S[:P-1] + S[P:]
        
        print(S) # 결과 출력

if __name__ == "__main__":
    main()
```

### 코드 설명

1. **입력 받기**:
    ```python
    import sys

    def main():
        input = sys.stdin.read
        data = input().split()
    ```
    - `sys.stdin.read`를 사용하여 모든 입력을 한 번에 읽어온 후, `split()`을 사용하여 공백 기준으로 나눈다.

2. **테스트 케이스 처리**:
    ```python
    T = int(data[0]) # 테스트 케이스의 개수 입력
    index = 1
    
    for _ in range(T):
        P = int(data[index])
        S = data[index + 1]
        index += 2
    ```
    - 첫 번째 요소는 테스트 케이스의 개수 `T`이다.
    - 이후 `T`번 반복하면서, 각 테스트 케이스마다 오타 위치 `P`와 문자열 `S`를 가져온다.

3. **오타 제거 및 출력**:
    ```python
        # P번째 문자를 제거하기 위해 슬라이싱을 사용
        if 1 <= P <= len(S):
            S = S[:P-1] + S[P:]
        
        print(S) # 결과 출력
    ```
    - `P`번째 문자를 제거하기 위해 문자열을 슬라이싱하여 `P-1`까지와 `P` 이후 부분을 합친다.
    - 수정된 문자열 `S`를 출력한다.

### 예제 실행

**입력:**
```
4
4 MISSPELL
1 PROGRAMMING
7 CONTEST
3 BALLOON
```

**출력:**
```
MISPELL
ROGRAMMING
CONTES
BALOON
```

## 결론

이번 문제는 문자열에서 특정 위치의 문자를 제거하는 간단한 구현 문제였다. C++과 Python 모두에서 문자열 처리 기능을 활용하여 효율적으로 해결할 수 있었다. C++에서는 `erase` 함수를 사용하여 쉽게 문자를 제거할 수 있었고, Python에서는 슬라이싱을 통해 동일한 작업을 수행할 수 있었다. 또한, C++ 표준 라이브러리를 사용하지 않고도 `for` 루프를 활용하여 직접 문자를 이동시키는 방식으로 문제를 해결할 수 있었다.

이 문제를 통해 문자열 조작의 기본적인 방법을 다시 한 번 복습할 수 있었으며, 입력과 출력을 효율적으로 처리하는 방법에 대해 학습할 수 있었다. 추가적으로, 더 복잡한 문자열 처리 문제가 주어진다면 이와 같은 기본적인 접근 방식을 기반으로 다양한 알고리즘을 적용할 수 있을 것이다.