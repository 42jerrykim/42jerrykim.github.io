---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-20T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Two Pointers
- Sorting
- Hashing
- Pruning
- O(N²)
- Array
- Combinatorics
- Brute Force
- Problem Solving
title: '[Algorithm] C++/Python 백준 16287번 : Parcel'

---

국제대학소포센터(ICPC: International Collegiate Parcel Center)는 전세계 대학생들을 대상으로 소포 무료 배송 이벤트를 진행하고 있다. 이 이벤트의 조건은 소포를 구성하는 물품이 정확히 4개이어야 하며, 이 4개 물품의 무게 합이 정확히 정해진 정수 무게 $ W $ 그램이어야 한다는 것이다. 부산대학교에 있는 찬수는 영국 왕립대학에 있는 수환에게 보내고 싶은 물품이 매우 많아, 이 조건을 만족하는 물품 조합이 있는지 빠르게 확인하고자 한다. 문제는 서로 다른 $ n $개의 정수로 이루어진 집합 $ A $에서 4개의 원소를 선택하여 그 합이 정확히 $ W $가 되는지 여부를 판단하는 것이다.

문제 : [https://www.acmicpc.net/problem/16287](https://www.acmicpc.net/problem/16287)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제는 네 개의 원소를 선택하여 특정 합을 만드는 전형적인 4-합(4-sum) 문제로 볼 수 있다. 단순한 브루트 포스 방법으로는 $ O(N^4) $의 시간 복잡도로 해결할 수 있으나, 이는 $ N $이 최대 5,000일 때 시간 내에 불가능하다. 따라서 보다 효율적인 접근 방법이 필요하다.

본 문제의 접근 방식은 다음과 같다:

1. **정렬:** 주어진 집합 $ A $를 오름차순으로 정렬한다. 이는 이후의 탐색을 효율적으로 수행하기 위함이다.
2. **두 개의 합을 미리 계산:** 먼저, 배열의 각 원소에 대해 두 개의 원소의 합을 미리 계산하여 해시 테이블이나 배열을 이용해 저장한다.
3. **두 포인터 기법:** 네 개의 원소 중 두 개를 고정한 후, 나머지 두 개의 합이 목표 값 $ W $에서 고정한 두 원소의 합을 뺀 값이 되는지 확인한다.
4. **합의 존재 여부 확인:** 미리 계산한 두 개의 합이 존재하는지 빠르게 확인하여 조건을 만족하는지 판단한다.
5. **최적화:** 가능한 합의 범위를 제한하고, 불필요한 계산을 줄이기 위해 가지치기(Pruning) 기법을 적용한다.

이러한 접근 방식을 통해 시간 복잡도를 $ O(N^2) $으로 줄여 문제를 효율적으로 해결할 수 있다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    
    int W, N;
    cin >> W >> N;
    vector<int> A(N);
    for(auto &x : A) cin >> x;
    
    sort(A.begin(), A.end());
    bool found = false;
    // S will store all possible sums of two numbers before the current i
    vector<bool> S(400001, false);
    
    for(int i = 2; i < N-1 && !found; ++i){
        // Update S with sums involving A[i-1] and all previous elements
        for(int j = 0; j < i-1; ++j){
            if(A[j] + A[i-1] <= 400000){
                S[A[j] + A[i-1]] = true;
            }
        }
        // Now check for pairs (A[i], A[j]) such that W - A[i] - A[j] exists in S
        for(int j = i+1; j < N && !found; ++j){
            int target = W - A[i] - A[j];
            if(target < 0 || target > 400000) continue;
            if(S[target]){
                found = true;
            }
        }
    }
    
    cout << (found ? "YES" : "NO") << '\n';
}
```

**코드 설명**

1. **입력 및 정렬:**
   - `W`와 `N`을 입력받고, 배열 `A`에 물품의 무게를 저장한다.
   - 배열 `A`를 오름차순으로 정렬하여 탐색을 용이하게 한다.

2. **합 집합 `S` 초기화:**
   - `S`는 두 원소의 합이 가능한지 여부를 저장하는 불리언 배열로, 인덱스는 합을 나타낸다.
   - `S`의 크기는 문제의 최대 합 $ 400,000 $을 고려하여 설정한다.

3. **합 집합 업데이트 및 확인:**
   - 외부 루프 `i`는 두 번째 원소의 인덱스를 나타낸다.
   - 내부 루프 `j`는 현재 `i` 이전의 원소들과 `A[i-1]`의 합을 `S`에 저장한다.
   - 이후 또 다른 내부 루프 `j`는 `i` 이후의 원소들과 현재 `A[i]`의 합을 계산하고, `W - A[i] - A[j]`가 `S`에 존재하는지 확인한다.
   - 조건을 만족하는 경우 `found`를 `true`로 설정하고 루프를 종료한다.

4. **결과 출력:**
   - `found`가 `true`이면 "YES", 그렇지 않으면 "NO"를 출력한다.

이 코드는 두 개의 원소 합을 미리 저장하고, 나머지 두 개의 원소 합을 확인함으로써 네 개의 원소 합이 $ W $가 되는지를 효율적으로 판별한다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>

int main(){
    int W, N;
    scanf("%d %d", &W, &N);
    int *A = (int*)malloc(sizeof(int)*N);
    for(int i = 0; i < N; ++i){
        scanf("%d", &A[i]);
    }
    // Simple insertion sort
    for(int i = 1; i < N; ++i){
        int key = A[i];
        int j = i-1;
        while(j >=0 && A[j] > key){
            A[j+1] = A[j];
            j--;
        }
        A[j+1] = key;
    }
    int found = 0;
    // Initialize S
    char *S = (char*)calloc(400001, sizeof(char));
    for(int i = 2; i < N-1 && !found; ++i){
        // Update S with sums involving A[i-1]
        for(int j = 0; j < i-1; ++j){
            if(A[j] + A[i-1] <= 400000){
                S[A[j] + A[i-1]] = 1;
            }
        }
        // Check for pairs
        for(int j = i+1; j < N && !found; ++j){
            int target = W - A[i] - A[j];
            if(target < 0 || target > 400000) continue;
            if(S[target]){
                found = 1;
            }
        }
    }
    printf("%s\n", found ? "YES" : "NO");
    free(A);
    free(S);
}
```

**코드 설명**

1. **입력 및 정렬:**
   - `scanf`를 사용하여 `W`와 `N`을 입력받고, 동적 메모리 할당을 통해 배열 `A`에 물품의 무게를 저장한다.
   - 삽입 정렬(Insertion Sort)을 사용하여 배열 `A`를 오름차순으로 정렬한다. 이는 라이브러리를 사용하지 않고 정렬을 수행하기 위함이다.

2. **합 집합 `S` 초기화:**
   - `S`는 두 원소의 합이 가능한지 여부를 저장하는 캐릭터 배열로, `calloc`을 사용하여 초기화한다.

3. **합 집합 업데이트 및 확인:**
   - 외부 루프 `i`는 두 번째 원소의 인덱스를 나타낸다.
   - 내부 루프 `j`는 현재 `i` 이전의 원소들과 `A[i-1]`의 합을 `S`에 저장한다.
   - 이후 또 다른 내부 루프 `j`는 `i` 이후의 원소들과 현재 `A[i]`의 합을 계산하고, `W - A[i] - A[j]`가 `S`에 존재하는지 확인한다.
   - 조건을 만족하는 경우 `found`를 `1`로 설정하고 루프를 종료한다.

4. **결과 출력:**
   - `printf`를 사용하여 `found`의 값에 따라 "YES" 또는 "NO"를 출력한다.

5. **메모리 해제:**
   - 동적으로 할당된 메모리 `A`와 `S`를 `free`를 사용하여 해제한다.

이 코드는 C++의 고급 라이브러리를 사용하지 않고, 기본적인 C 라이브러리만을 사용하여 문제를 해결한다. 삽입 정렬과 직접적인 메모리 관리를 통해 효율성을 유지한다.

## Python 코드와 설명

```python
import sys

def main():
    input = sys.stdin.read
    data = input().split()
    W = int(data[0])
    N = int(data[1])
    A = list(map(int, data[2:2+N]))
    A.sort()
    S = set()
    found = False
    for i in range(2, N-1):
        # Update S with sums involving A[i-1]
        for j in range(i-1):
            s = A[j] + A[i-1]
            if s <= 400000:
                S.add(s)
        # Check for pairs
        for j in range(i+1, N):
            target = W - A[i] - A[j]
            if target in S:
                found = True
                break
        if found:
            break
    print("YES" if found else "NO")

if __name__ == "__main__":
    main()
```

**코드 설명**

1. **입력 및 정렬:**
   - `sys.stdin.read`를 사용하여 모든 입력을 한 번에 읽어들인다.
   - 입력 데이터를 공백 기준으로 분할한 후, `W`와 `N`, 그리고 배열 `A`에 물품의 무게를 저장한다.
   - `A.sort()`를 사용하여 배열 `A`를 오름차순으로 정렬한다.

2. **합 집합 `S` 초기화:**
   - `S`는 두 원소의 합을 저장하는 집합(Set)으로, 빠른 탐색을 위해 사용된다.

3. **합 집합 업데이트 및 확인:**
   - 외부 루프 `i`는 두 번째 원소의 인덱스를 나타낸다.
   - 내부 루프 `j`는 현재 `i` 이전의 원소들과 `A[i-1]`의 합을 `S`에 추가한다.
   - 이후 또 다른 내부 루프 `j`는 `i` 이후의 원소들과 현재 `A[i]`의 합을 계산하고, `W - A[i] - A[j]`가 `S`에 존재하는지 확인한다.
   - 조건을 만족하는 경우 `found`를 `True`로 설정하고 루프를 종료한다.

4. **결과 출력:**
   - `print`를 사용하여 `found`의 값에 따라 "YES" 또는 "NO"를 출력한다.

이 코드는 Python의 내장 자료구조인 집합(Set)을 활용하여 두 원소의 합을 효율적으로 저장하고 탐색한다. Python의 간결한 문법을 통해 코드의 가독성을 높였다.

## 결론

이번 문제는 네 개의 원소를 선택하여 특정 합을 만드는 전형적인 4-합 문제로, 단순한 브루트 포스 방법으로는 시간 초과가 발생할 수 있었다. 이를 해결하기 위해 두 개의 합을 미리 계산하여 저장하고, 이를 기반으로 나머지 두 개의 합을 효율적으로 탐색하는 접근 방식을 사용하였다. C++, C, Python 등 다양한 언어로 구현해보면서 각 언어의 장단점을 이해할 수 있었으며, 특히 정렬과 해시 테이블(또는 집합)을 활용한 최적화가 중요한 역할을 함을 확인할 수 있었다. 추가적으로, 메모리 사용을 줄이기 위한 다양한 방법이나, 더 큰 입력에 대응하기 위한 최적화 방안 등을 고민해볼 수 있었으며, 이러한 최적화 기법은 다양한 알고리즘 문제 해결에 있어 유용하게 활용될 수 있을 것이다.