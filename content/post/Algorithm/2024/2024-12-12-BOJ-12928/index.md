---
title: "[Algorithm] C++/Python 백준 12928번 : 트리와 경로의 길이"
categories: 
- Algorithm
- Tree
- DynamicProgramming
tags:
- DP
- Tree
- Bitset
- GraphTheory
- Optimization
- O(N^3)
- Combinatorics
- DynamicProgramming
- Implementation
image: "tmp_wordcloud.png"
date: 2024-12-12
---

트리의 구조와 경로의 개수를 다루는 문제이다. 주어진 노드의 개수 N과 길이가 2인 단순 경로의 개수 S가 있을 때, 이를 만족하는 트리를 구성할 수 있는지 판별하는 문제이다. 이 문제는 다소 난해하게 보일 수 있지만, 적절한 수식 변형과 DP(Dynamic Programming)를 활용하여 해결 가능한 형태로 만들 수 있다. 또한, DP를 통해 가능한 차수 분배를 찾고, 그에 따른 경로의 개수를 만족하는지 확인하는 방식으로 풀이가 가능하다.

문제 : [https://www.acmicpc.net/problem/12928](https://www.acmicpc.net/problem/12928)

## 문제 설명

본 문제는 다음과 같은 조건을 만족하는 트리가 존재하는지 판별하는 것이다.

- 트리는 N개의 노드를 가진 연결 그래프이며 사이클이 없다.
- 길이가 2인 단순 경로의 개수가 S개가 되도록 트리를 구성할 수 있는지를 묻는다.

여기서 "길이가 2인 단순 경로"란 서로 다른 세 개의 노드 A, B, C가 있으며, A-B, B-C로 이어질 때 이를 A-B-C라는 단순 경로로 본다. 방향은 고려하지 않으므로 A-B-C나 C-B-A나 같은 경로로 센다. 경로 길이가 2라는 것은 "간선 2개를 연결해 만든 경로"라고 해석할 수 있다. 즉, 어떤 노드 B를 중심으로 양쪽에 각각 한 노드씩 연결된 형태를 세는 것이다.

이 문제를 더욱 구체적으로 살펴보면, 트리에서 노드의 차수(각 노드에 연결된 간선의 수)를 통해 길이가 2인 경로의 개수를 쉽게 계산할 수 있다. 노드 하나를 기준으로, 해당 노드의 차수가 d라고 할 때, 그 노드를 중심으로 형성되는 길이가 2인 경로의 개수는 C(d,2) = d(d-1)/2개이다. 트리 전체에 걸쳐 길이가 2인 경로의 총 개수는 모든 노드에 대해 C(d_i,2)를 합한 값이 된다.

문제의 골자는 다음과 같이 정리할 수 있다.  
- N개의 노드로 이뤄진 트리에는 총 N-1개의 간선이 있고, 모든 노드의 차수 합은 2(N-1)이다. 노드 i의 차수를 d_i라 할 때 Σ d_i = 2(N-1)이다.
- 길이 2인 경로의 수 S = Σ C(d_i,2) = Σ [d_i(d_i-1)/2]이다.
- d_i를 d_i' = d_i - 1이라 하면 Σ d_i' = N-2가 되며, 이 d_i'들을 이용해 식을 변형할 수 있다.
- S = Σ [ (d_i'+1)*d_i' / 2 ] = (Σ d_i'^2 + Σ d_i') / 2. Σ d_i' = N-2이므로 2S = Σ d_i'^2 + (N-2).
- 따라서 Σ d_i'^2 = 2S - N + 2.

결국, 이 문제는 다음과 같은 정수해를 찾는 문제이다:  
- d_i' ≥ 0, Σ d_i' = N-2, Σ d_i'^2 = 2S - N + 2  
이를 만족하는 nonnegative 정수 d_i'들의 집합이 존재하는지 여부를 판별하면 된다.

이는 간단하지 않아 보이나, N이 최대 50, S가 최대 1000이므로 DP를 통해 충분히 해결 가능하다. DP를 사용하여 d_i'의 배치를 전부 탐색하는 방식(비트셋을 활용한 집합 표현)을 사용하면, 가능한 제곱합의 패턴을 모두 살필 수 있다. 이러한 방식으로 조건에 맞는 d_i'의 조합이 있는지 확인하여, 존재하면 1, 없으면 0을 출력한다.

## 접근 방식

접근 방식은 크게 다음 단계로 나눌 수 있다.

1. **수식 변형**:  
   길이 2인 경로의 개수를 노드 차수들로 표현하고, 이를 d_i' = d_i - 1로 치환하여 조건 Σ d_i' = N-2, Σ d_i'^2 = 2S - N + 2를 얻는다.

2. **DP를 통한 조합 탐색**:  
   모든 d_i'에 대해 0 이상인 정수를 할당하는 경우의 수를 고려한다. N, S의 범위가 작으므로,  
   - i번째 노드까지 고려할 때  
   - 합이 j인 d_i'들의 가능한 제곱합 집합을 비트셋 형태로 관리한다.
   
   dp[i][sum_of_d'] = bitset 형태로, 특정 제곱합이 가능한지를 저장한다.

3. **비트셋 연산**:  
   각 노드에 대해 d_i'를 0부터 sum_parts(N-2)까지 할당해보고, 이를 통해 가능한 제곱합 집합을 dp로 업데이트한다. dp의 마지막에서 (N개 노드 고려, 합=N-2)일 때 제곱합이 target_sq(=2S - N + 2) 가능하면 정답이다.

4. **출력**:  
   가능한 경우 1, 불가능한 경우 0을 출력한다.

이 과정은 O(N * (N-2) * (N-2)^2)에 가까운 다소 높은 복잡도를 가질 수 있지만, N이 최대 50이므로 충분히 처리 가능하다.

## C++ 코드와 설명

아래 코드는 STL을 활용한 최적화된 C++ 코드이다.  
- DP 배열로 vector와 bitset을 활용한다.
- dp[i][j]는 i개의 노드를 처리했고, d_i'들의 합이 j일 때 가능한 제곱합 값들을 bitset으로 표현한다.
- 초기 상태 dp[0][0][0] = true에서 시작해 가능한 d_i'를 모두 시도한다.
- 마지막에 dp[N][N-2][target_sq]가 true인지 확인한다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    int N, S;
    cin >> N >> S;

    // 특수 케이스 처리
    if (N == 1) {
        // 노드가 하나면 길이가 2인 경로 존재 불가. S=0일 때만 가능.
        cout << (S == 0 ? 1 : 0) << "\n";
        return 0;
    }
    if (N == 2) {
        // 노드 2개 트리: 간선 1개만 존재, 길이가 2인 경로 없음.
        cout << (S == 0 ? 1 : 0) << "\n";
        return 0;
    }

    int sum_parts = N - 2;
    int target_sq = 2 * S - N + 2;
    if (target_sq < 0) {
        // 제곱합이 음수가 될 수 없으므로 불가능.
        cout << 0 << "\n";
        return 0;
    }

    // dp[i][j]: i개의 노드 고려, 합 j일 때 가능한 제곱합 집합
    vector<vector<bitset<2501>>> dp(N+1, vector<bitset<2501>>(sum_parts+1, 0));
    dp[0][0].set(0, true);

    // 모든 노드에 대해 가능한 d_i' 시도
    for (int i = 0; i < N; i++) {
        for (int j = 0; j <= sum_parts; j++) {
            if (dp[i][j].any()) {
                for (int x = 0; x + j <= sum_parts; x++) {
                    int sq = x * x;
                    dp[i+1][j+x] |= (dp[i][j] << sq);
                }
            }
        }
    }

    cout << (dp[N][sum_parts].test(target_sq) ? 1 : 0) << "\n";
    return 0;
}
```

**동작 단계별 설명**:  
1. 입력 N, S를 받는다.  
2. 특수 케이스(N=1, N=2)를 처리한다.  
3. d_i'의 합과 목표 제곱합(target_sq)을 계산한다.  
4. dp 테이블을 초기화하고, 모든 노드에 대해 d_i'를 할당해보며 가능한 제곱합을 갱신한다.  
5. 마지막에 dp[N][N-2][target_sq] 여부를 확인해 조건 만족 시 1, 아니면 0을 출력한다.

## C++ without library 코드와 설명

아래는 `<bits/stdc++.h>`를 사용하지 않고, `<stdio.h>`와 `<malloc.h>`만 사용한 C++ 코드이다.  
메모리를 동적으로 할당하고, C 스타일의 배열과 비트 연산을 통해 dp를 구성한다.  
비트 연산으로 dp를 표현하기 위해 비트셋 역할을 할 정수 배열을 사용하고, shift 연산을 통해 가능한 제곱합을 반영한다.

```cpp
#include <stdio.h>
#include <malloc.h>

int main(){
    int N, S;
    scanf("%d %d", &N, &S);

    if (N == 1) {
        printf("%d\n", S == 0 ? 1 : 0);
        return 0;
    }
    if (N == 2) {
        printf("%d\n", S == 0 ? 1 : 0);
        return 0;
    }

    int sum_parts = N - 2;
    int target_sq = 2 * S - N + 2;
    if (target_sq < 0) {
        printf("0\n");
        return 0;
    }

    // dp[i][j]: i개 노드, 합이 j일 때 가능한 제곱합 비트마스크
    // target_sq 최대가 약 2500 미만이므로 int 배열로 커버 가능(32비트 int 하나로는 2500비트 커버 불가 -> int 배열 필요)
    // 단순화를 위해 약 2501비트를 표현할 배열로 구성
    // int는 32비트이므로, 2501비트 -> 2501/32+1개 정도 필요
    int MAX_SQ = 2501;
    int INT_SIZE = (MAX_SQ / 32) + 1;

    // dp를 3차원 배열로 표현하기는 어려우므로 동적할당
    // dp[i][j][bit array]
    int ***dp = (int ***)malloc((N+1)*sizeof(int**));
    for (int i = 0; i <= N; i++){
        dp[i] = (int **)malloc((sum_parts+1)*sizeof(int*));
        for (int j = 0; j <= sum_parts; j++){
            dp[i][j] = (int *)malloc(INT_SIZE*sizeof(int));
            for (int k = 0; k < INT_SIZE; k++){
                dp[i][j][k] = 0;
            }
        }
    }

    // 초기 상태 dp[0][0][0bit] = 1 (0번 인덱스비트 세팅)
    dp[0][0][0] = 1; // 0번 비트 set: 여기서는 0번 비트 set을 위해 dp[0][0][0] = 1로 둔다.

    // helper 함수 없이 수동으로 shift 연산
    for (int i = 0; i < N; i++) {
        for (int j = 0; j <= sum_parts; j++) {
            // 현재 dp[i][j]에 세팅된 비트들을 기반으로 새로운 d_i' 할당
            // d_i' = x
            for (int x = 0; x + j <= sum_parts; x++) {
                int sq = x*x;
                // dp[i][j]를 sq만큼 왼쪽 shift
                // 결과를 dp[i+1][j+x]에 OR
                // 비트 시프트: sq비트 왼쪽 이동
                // sq 나누기 32로 block index, sq % 32로 bit index
                // 복잡한 비트 shifting 수행
                // 여기서는 O(N^3*(N-2))가능하므로 단순 시프트 구현

                // temp를 0으로 초기화
                int temp[INT_SIZE];
                for (int idx = 0; idx < INT_SIZE; idx++) temp[idx] = 0;

                // dp[i][j] 시프트
                // dp[i][j]에서 set된 비트를 sq만큼 왼쪽 이동
                for (int idx = 0; idx < INT_SIZE; idx++){
                    unsigned int val = (unsigned int)dp[i][j][idx];
                    if (val == 0) continue;
                    // val의 각 비트를 sq만큼 왼쪽 이동
                    // 큰 sq에 대해 나누어 처리
                    int block_shift = sq / 32;
                    int bit_shift = sq % 32;

                    // block_shift 만큼 뒤 인덱스에 넣어야 함
                    if (idx + block_shift < INT_SIZE) {
                        unsigned long long shifted = ((unsigned long long)val) << bit_shift;
                        // lower part
                        unsigned int low_part = (unsigned int)(shifted & 0xFFFFFFFFULL);
                        temp[idx + block_shift] |= low_part;
                        unsigned long long high_part = (shifted >> 32ULL);
                        if (high_part > 0 && (idx + block_shift + 1 < INT_SIZE)) {
                            temp[idx + block_shift + 1] |= (unsigned int)high_part;
                        }
                    }
                }

                // temp를 dp[i+1][j+x]에 OR
                for (int idx = 0; idx < INT_SIZE; idx++){
                    dp[i+1][j+x][idx] |= temp[idx];
                }
            }
        }
    }

    // target_sq 비트 확인
    int result = 0;
    int block = target_sq / 32;
    int bit = target_sq % 32;
    if ((dp[N][sum_parts][block] & (1 << bit)) != 0) {
        result = 1;
    }

    printf("%d\n", result);

    // 메모리 해제
    for (int i = 0; i <= N; i++){
        for (int j = 0; j <= sum_parts; j++){
            free(dp[i][j]);
        }
        free(dp[i]);
    }
    free(dp);

    return 0;
}
```

**동작 단계별 설명**:  
1. N, S를 입력받는다.  
2. 특수 케이스를 처리한다.  
3. sum_parts, target_sq를 계산하고 불가능하면 0 출력 후 종료한다.  
4. 3차원 dp 배열을 int 비트마스크로 구현한다.  
5. dp를 0으로 초기화 후 dp[0][0][0번째 int] = 1로 설정 (0비트 set).  
6. 각 노드마다 가능한 d_i'를 할당하며 비트마스크를 왼쪽으로 시프트하는 방식으로 제곱합 값을 반영한다.  
7. 마지막에 dp[N][sum_parts]에서 target_sq 비트를 확인하여 결과를 판단한다.

## Python 코드와 설명

Python 코드에서는 C++ 코드와 동일한 로직을 유지하되, Python의 list와 bitset 대용으로 `int`를 이용해 비트마스크를 다룬다. Python의 정수는 임의 정밀도를 가지므로 비트 연산에 용이하다.

```python
import sys
input=sys.stdin.readline

N,S=map(int,input().split())

if N==1:
    print(1 if S==0 else 0)
    sys.exit(0)
if N==2:
    print(1 if S==0 else 0)
    sys.exit(0)

sum_parts = N-2
target_sq = 2*S - N + 2
if target_sq < 0:
    print(0)
    sys.exit(0)

# dp[i][j]: i개 노드 고려, 합이 j일때 가능한 제곱합 비트마스크(정수 사용)
dp = [[0]*(sum_parts+1) for _ in range(N+1)]
dp[0][0] = 1  # 0비트 set

for i in range(N):
    for j in range(sum_parts+1):
        cur = dp[i][j]
        if cur == 0:
            continue
        for x in range(sum_parts+1-j):
            sq = x*x
            # cur를 sq만큼 왼쪽 시프트
            shifted = cur << sq
            dp[i+1][j+x] |= shifted

result = 1 if (dp[N][sum_parts] & (1 << target_sq)) != 0 else 0
print(result)
```

**동작 단계별 설명**:  
1. 입력 N, S를 받고 특수 케이스 처리 후 sum_parts, target_sq 계산  
2. dp 배열을 초기화하고 dp[0][0] = 1로 시작  
3. 각 노드에 대해 d_i'를 0부터 가능한 범위까지 할당하고, 그때마다 cur를 sq만큼 왼쪽 shift하여 dp[i+1][j+x]에 반영  
4. 모든 과정을 마친 뒤 dp[N][sum_parts]에서 target_sq 비트가 set되어 있으면 1, 아니면 0 출력

## 결론

이 문제는 트리 구조에서 특정 길이의 경로 수를 만족하는 구성이 가능한지 판별하는 흥미로운 문제이다. 간단한 그래프 알고리즘만으로는 풀기 어렵지만, 수식 변형을 통해 차수 분포 문제로 전환한 후, DP를 이용해 해결할 수 있다. 이러한 방식으로 문제의 난이도를 낮추고, 구현 가능하게 만드는 과정은 문제 해결에서 중요한 단계이다.

추가적인 최적화로 bitset 사용이나 메모리 접근 최적화를 통해 시간·공간 복잡도를 낮출 수도 있다. 또한, 만약 더 효율적인 수학적 해법이나 특수한 구조를 찾아낸다면, 더 간결한 풀이도 가능할 것이다. 본 풀이를 통해 DP와 비트마스크를 활용한 풀이 전략을 익힐 수 있으며, 향후 유사한 문제 해결에도 적용할 수 있을 것이다.
```