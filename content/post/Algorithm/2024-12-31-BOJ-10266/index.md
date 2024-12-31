---
title: "[Algorithm] C++/Python 백준 10266번 : 시계 사진들"
categories: 
- Algorithm
- String
- Pattern-Matching
tags:
- KMP
- String
- Implementation
- O(N)
- Circular-array
- Pattern-matching
- Problem-solving
image: "index.png"
date: 2024-12-31
---

시계 사진 두 장이 주어졌을 때, 두 사진이 가리키는 시각이 '같을 수 있는지'를 판별하는 문제이다. 각 사진 속 시계에는 숫자나 특별한 표기가 없고, 동일한 길이와 목적을 가진 바늘들이 여러 개 존재한다. 문제의 핵심은 이 바늘들의 상대적인 '간격'이 동일한지 확인하는 것이다. 시계는 원형 구조를 가지므로, 직선적인 관점이 아닌 원주상에서의 간격을 비교해 주어야 한다. 이를 위해서는 KMP(또는 Rolling Hash 등 문자열 매칭 알고리즘)와 같은 접두사-접미사 일치 알고리즘을 적용할 수 있다. 아래에서 문제와 풀이 과정을 상세히 살펴본다.

문제 : [https://www.acmicpc.net/problem/10266](https://www.acmicpc.net/problem/10266)

## 문제 설명

시계 사진의 각도 정보를 분석해 두 시계가 같은 시각을 나타낼 수 있는지 확인하는 문제이다.  
- 시계 바늘의 개수 \( n \)이 주어진다. 각 시계 바늘은 어떤 기준(12시 방향이라 가정 가능)을 중심으로 측정된 '시계 방향 각도' 값을 갖는다.  
- 하나의 시계 사진에는 \( n \)개의 바늘이 있고, 각 바늘의 각도는 서로 다르다.  
- 각도는 \( 0 \leq a_i < 360{,}000 \)으로 주어진다. 이는 360도를 1도 = 1000분으로 나눈 세분화(360 × 1000 = 360,000) 방식이다. 예를 들어, 180도는 180,000으로 표현된다.
- 이 문제에서 '두 사진의 시각이 동일하다'는 것은, '두 시계의 각도 배열을 어떤 기준으로 회전했을 때 동일한 분포를 갖게 되는가'로 해석할 수 있다. 시계가 원형 구조이므로 한 장의 시계 사진을 특정 각도만큼 돌려서 다른 시계 사진과 동일하게 맞출 수 있다면, 두 사진은 같은 시각을 나타내는 것이다.
- 그러나 수천 분의 1도 단위까지 고려되므로, 모든 가능한 각도 회전을 일일이 시도하는 것은 비효율적이다. \( n \)이 최대 200,000까지 가능하므로 \( O(n^2) \) 수준의 알고리즘은 시간 내에 불가능하다.
- 따라서, 각 시계의 바늘들 사이 '인접 각도 차'를 구하여 이를 문자열로 보고, 첫 번째 시계의 차분 배열을 2번 이어붙인 뒤 두 번째 시계의 차분 배열이 그 안에 부분 수열로 등장하는지를 KMP 알고리즘으로 확인함으로써 문제를 해결한다.

위 문제를 다시 요약하면, **정렬된 각도들 사이의 간격(차분) 배열이 순환 구조에서 동일한지**를 판별하는 것이다. 시계가 원형이기 때문에, '처음 각도'부터 '마지막 각도'까지의 거리도 고려해야 하며, 이를 연결하여 문자열 매칭 알고리즘을 활용하게 된다.

본 문제에서 요구하는 상세 사항:
- 입력:  
  1) 첫 줄: 바늘의 수 \( n \)  
  2) 둘째 줄: 첫 번째 시계 사진의 각도 \( n \)개  
  3) 셋째 줄: 두 번째 시계 사진의 각도 \( n \)개  
- 출력:  
  - 두 시계가 같은 시각을 나타낼 수 있다면 "possible"  
  - 아니라면 "impossible"  

위 요건을 만족하는 동시에 빠른 시간 안에 해답을 구해야 한다. 시계의 모든 바늘 위치를 비교하려면, 원을 펼친 뒤 문자열 매칭으로 접근하는 방식이 가장 효율적이다.

## 접근 방식

1. **정렬(Sort)**  
   두 시계 사진 각각에 대해, 각 바늘의 각도 배열을 오름차순으로 정렬한다.  
2. **차분 배열(Difference Array) 생성**  
   - 정렬된 각도 배열을 \([a_0, a_1, \dots, a_{n-1}]\)라고 할 때, '인접 바늘'간 각도 차이를 구한다.  
   - 마지막 각도와 첫 각도도 연결해주어야 원형 구조를 반영할 수 있다.  
   - 예:  
     \[
       \text{diff}[i] = (a_{i+1} - a_i) \mod 360{,}000 \quad (i = 0..n-2)
     \]  
     \[
       \text{diff}[n-1] = (a_{0} + 360{,}000 - a_{n-1}) \mod 360{,}000
     \]
3. **문자열 매칭(KMP) 알고리즘**  
   - 첫 번째 시계 사진의 차분 배열을 2배로 이어붙인다. 즉, \(\text{diff1} + \text{diff1}\). 이는 회전 가능한 모든 경우의 수를 직선적으로 표현하기 위함이다.  
   - 두 번째 시계 사진의 차분 배열이 이 '2배로 확장된 배열'에 등장하는지 KMP 알고리즘으로 검사한다.  
   - 등장한다면, 두 시계 사진은 동일 시각 표현이 가능하므로 "possible"을, 등장하지 않는다면 "impossible"을 출력한다.  

이 방식은 각 시계 사진을 정렬하는 데 \( O(n \log n) \), 차분 배열을 만드는 데 \( O(n) \), KMP 알고리즘으로 매칭을 수행하는 데 \( O(n) \) 정도가 소요되어 전체적으로 \( O(n \log n) \)에 수렴한다. \( n \)이 최대 200,000이므로 이 방법은 시간 안에 충분히 해결 가능하다.

## C++ 코드와 설명

아래는 위 알고리즘을 C++로 구현한 코드이다. 불필요한 입출력 시간을 줄이기 위해 `ios::sync_with_stdio(false);`와 `cin.tie(nullptr);`를 사용하였고, KMP 알고리즘의 구현에는 접두사 함수(prefix function, 파이 함수) 계산 함수를 별도로 두었다.

```cpp
#include <bits/stdc++.h>
using namespace std;

/**
 * 접두사(prefix) 배열을 구하는 함수이다.
 * KMP에서 패턴 내에서의 겹치는 접두사와 접미사의 최대 길이를 pi 배열에 저장한다.
 */
vector<int> computePrefix(const vector<int>& pattern) {
    int m = pattern.size();
    vector<int> pi(m, 0);
    int j = 0;
    for (int i = 1; i < m; i++) {
        while (j > 0 && pattern[i] != pattern[j]) {
            j = pi[j - 1];
        }
        if (pattern[i] == pattern[j]) {
            pi[i] = ++j;
        }
    }
    return pi;
}

/**
 * KMP 알고리즘으로 text에서 pattern이 등장하는지 확인한다.
 * 등장하면 true, 아니면 false를 반환한다.
 */
bool kmpSearch(const vector<int>& text, const vector<int>& pattern) {
    int n = text.size();
    int m = pattern.size();
    if (m > n) return false;

    vector<int> pi = computePrefix(pattern);
    int j = 0;
    for (int i = 0; i < n; i++) {
        while (j > 0 && text[i] != pattern[j]) {
            j = pi[j - 1];
        }
        if (text[i] == pattern[j]) {
            j++;
            if (j == m) {
                return true;
            }
        }
    }
    return false;
}

/**
 * 각도 배열로부터 인접한 각도 차이를 계산하여 diff 배열을 만든다.
 * 마지막 각도와 첫 각도도 연결하여 원형 구조를 반영한다.
 */
vector<int> buildDiff(const vector<int>& angles) {
    int n = angles.size();
    vector<int> diff(n);
    for (int i = 0; i < n - 1; i++) {
        diff[i] = (angles[i + 1] - angles[i] + 360000) % 360000;
    }
    diff[n - 1] = (angles[0] + 360000 - angles[n - 1]) % 360000;
    return diff;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> clock1(n), clock2(n);
    for (int i = 0; i < n; i++) cin >> clock1[i];
    for (int i = 0; i < n; i++) cin >> clock2[i];

    // 1. 각도 배열 정렬
    sort(clock1.begin(), clock1.end());
    sort(clock2.begin(), clock2.end());

    // 2. 차분 배열 만들기
    vector<int> diff1 = buildDiff(clock1);
    vector<int> diff2 = buildDiff(clock2);

    // 3. diff1을 2배로 늘려서 diff2가 부분 수열로 등장하는지 확인
    //    KMP를 통해 확인한다.
    vector<int> doubledDiff1(diff1.begin(), diff1.end());
    doubledDiff1.insert(doubledDiff1.end(), diff1.begin(), diff1.end());

    bool canMatch = kmpSearch(doubledDiff1, diff2);

    if (canMatch) cout << "possible\n";
    else cout << "impossible\n";

    return 0;
}
```

### 코드 동작 단계별 설명
1. **입력 처리**:  
   \( n \)과 두 시계 사진 각각의 각도 배열을 입력받는다.
2. **정렬**:  
   각 시계 사진의 각도 배열을 오름차순으로 정렬한다.  
3. **차분 배열 생성**:  
   `buildDiff` 함수를 통해 인접 각도 차이를 구하고, 마지막 각도와 첫 각도를 연결한다.
4. **차분 배열 확장**:  
   첫 번째 시계의 차분 배열을 2회 이어붙여서, 모든 회전 케이스를 선형적으로 표현한다.
5. **KMP 검색**:  
   확장된 첫 번째 시계 차분 배열 안에 두 번째 시계의 차분 배열이 부분 패턴으로 존재하는지 검사한다. 존재한다면 "possible", 아니면 "impossible"을 출력한다.

## Python 코드와 설명

아래는 동일한 알고리즘을 Python으로 구현한 예시이다. Python은 기본적으로 정수 나눗셈 및 모듈러 계산 시 주의해야 할 점이 있지만, 여기서는 360,000 이상의 값을 다루므로 오버플로 문제가 거의 발생하지 않는다. 대신, 입력 처리와 정렬 시에 시간 초과가 발생하지 않도록 주의가 필요하다(가능하다면 빠른 입출력 방식 사용).

```python
import sys

def compute_prefix(pattern):
    # KMP prefix 함수
    m = len(pattern)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j
    return pi

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m > n:
        return False
    
    pi = compute_prefix(pattern)
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
            if j == m:
                return True
    return False

def build_diff(angles):
    n = len(angles)
    diff = [0] * n
    for i in range(n - 1):
        diff[i] = (angles[i + 1] - angles[i] + 360000) % 360000
    diff[n - 1] = (angles[0] + 360000 - angles[n - 1]) % 360000
    return diff

def main():
    input = sys.stdin.readline

    n = int(input().strip())
    clock1 = list(map(int, input().split()))
    clock2 = list(map(int, input().split()))

    # 1. 정렬
    clock1.sort()
    clock2.sort()

    # 2. 차분 배열
    diff1 = build_diff(clock1)
    diff2 = build_diff(clock2)

    # 3. diff1 2회 반복
    doubled_diff1 = diff1 + diff1

    # 4. kmp 탐색
    if kmp_search(doubled_diff1, diff2):
        print("possible")
    else:
        print("impossible")

if __name__ == "__main__":
    main()
```

### 코드 동작 단계별 설명
1. **입력 및 정렬**:  
   `sys.stdin.readline`을 사용해 빠른 입력을 받는다. 각 시계의 각도를 리스트로 받고 정렬한다.
2. **차분 배열 생성**:  
   `build_diff` 함수를 이용해 인접한 각도 차이를 구한다.
3. **확장된 차분 배열 생성**:  
   첫 번째 시계의 차분 배열을 2배로 늘린다.
4. **KMP로 검색**:  
   `kmp_search` 함수를 통해 두 번째 시계 차분 배열이 2배 확장된 첫 번째 시계 차분 배열에 존재하는지 판별한다.
5. **결과 출력**:  
   매칭되면 "possible", 매칭되지 않으면 "impossible"을 출력한다.

## 결론

원형 구조를 선형으로 풀어내어 문자열 매칭 알고리즘(KMP)을 적용하는 것은, 많은 '원형' 문제에서 자주 등장하는 기법이다. 이 문제에서는 시계의 특성상 회전을 무수히 많이 고려해야 하지만, 차분 배열을 두 배로 늘리는 방식으로 모든 회전 케이스를 한 번에 처리할 수 있었다. 이를 통해 \( O(n \log n) \) (정렬) + \( O(n) \) (KMP) = \( O(n \log n) \) 안에 문제를 효율적으로 해결할 수 있다.

추가적으로, 문제를 풀면서 느낀 점은 '원형 문제를 풀기 위해서 문자열 매칭을 활용하는 전략'이 매우 강력하다는 것이다. 원형 구간에서의 비교, 패턴 매칭, 자료 구조 설계 등 다양한 문제에서 유사한 아이디어를 적용할 수 있다. 또한, Python에서 KMP를 사용할 때는 prefix 배열 계산 방식에 주의해야 하며, C++에서는 오버플로를 피하기 위해 64비트 정수(`long long`)를 적절히 활용하는 것도 중요하다.

이상으로, 백준 10266번 문제 "시계 사진들"에 대한 풀이 과정을 살펴보았다. KMP 알고리즘의 원리를 다시 복습해볼 수 있는 좋은 기회가 되었으며, 동시에 '회전을 선형으로 펼치는' 아이디어가 언제 어디서나 응용될 수 있음을 확인할 수 있었다. 필요하다면 Rolling Hash나 Z-algorithm 같은 다른 문자열 알고리즘을 사용해 볼 수도 있지만, KMP가 구현과 시간 복잡도 면에서 충분히 적합한 해결책이다.  