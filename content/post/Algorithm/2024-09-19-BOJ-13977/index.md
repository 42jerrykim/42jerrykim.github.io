---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-09-19T00:00:00Z"

header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Combinatorics
- NumberTheory
- FastExponentiation
- ModularInverse
- Factorial
- Implementation
- MathematicalIdea
- DynamicProgramming
title: '[Algorithm] C++/Python 백준 13977번 : 이항 계수와 쿼리'
---

이 문제는 주어진 여러 쌍의 $N$과 $K$에 대해 이항 계수 $\binom{N}{K}$를 계산하고, 그 결과를 1,000,000,007로 나눈 나머지를 구하는 문제이다. 입력으로는 여러 개의 쿼리 $M$이 주어지며, 각 쿼리마다 $N$과 $K$가 주어진다. 이때, $N$의 최대값이 4,000,000으로 매우 크기 때문에, 효율적으로 이항 계수를 계산할 필요가 있다. 단순히 팩토리얼을 계산하고 나누는 방식으로는 시간 초과가 발생할 수 있다. 따라서, 미리 팩토리얼과 그 역원을 미리 계산해두고 이를 활용하여 빠르게 이항 계수를 구하는 방법을 사용해야 한다.

문제 : [https://www.acmicpc.net/problem/13977](https://www.acmicpc.net/problem/13977)

|![](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 접근 방식

이 문제를 해결하기 위해서는 이항 계수를 효율적으로 계산할 수 있는 방법이 필요하다. 이항 계수 $\binom{N}{K}$는 다음과 같이 계산할 수 있다:

$\binom{N}{K} = \frac{N!}{K!(N-K)!}$

여기서, $N!$, $K!$, $(N-K)!$를 직접 계산하는 것은 $N$이 4,000,000까지 주어지므로 비효율적이다. 따라서, 미리 모든 팩토리얼 값을 계산해두고, 페르마의 소정리를 이용하여 모듈로 역수를 구한 뒤, 이를 이용해 $\binom{N}{K}$를 빠르게 계산할 수 있다. 구체적으로는 다음과 같은 단계를 따른다:

1. **팩토리얼 미리 계산**: $0!$부터 $4,000,000!$까지의 값을 미리 계산하고, 이를 모듈로 $1,000,000,007$로 저장한다.
2. **역팩토리얼 계산**: $N!$의 역수를 계산하기 위해 페르마의 소정리를 이용하여 $fact[N]^{MOD-2} \mod MOD$를 계산하고, 이를 통해 모든 역팩토리얼을 미리 계산해둔다.
3. **이항 계수 계산**: 각 쿼리마다 $\binom{N}{K} = fact[N] \times inv\_fact[K] \times inv\_fact[N-K] \mod MOD$를 계산하여 출력한다.

이러한 방식을 통해 $M$개의 쿼리를 효율적으로 처리할 수 있다.


## C++ 코드와 설명

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

const int MOD = 1000000007;

// Fast exponentiation to compute (base^exp) % MOD
ll powmod(ll base, ll exp, ll mod) {
    ll res = 1;
    base %= mod;
    while(exp > 0){
        if(exp & 1LL){
            res = res * base % mod; // 현재 비트가 1이면 결과에 base를 곱함
        }
        base = base * base % mod; // base를 제곱함
        exp >>= 1LL; // 다음 비트로 이동
    }
    return res;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    
    int M;
    cin >> M;
    
    // Maximum N is up to 4,000,000
    const int MAX = 4000000;
    vector<ll> fact(MAX+1, 1);
    for(int i=1; i<=MAX; ++i){
        fact[i] = fact[i-1] * i % MOD; // 팩토리얼을 미리 계산
    }
    
    // Compute inverse factorial
    vector<ll> inv_fact(MAX+1, 1);
    inv_fact[MAX] = powmod(fact[MAX], MOD-2, MOD); // 마지막 팩토리얼의 역수 계산
    for(int i=MAX-1; i>=0; --i){
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD; // 역팩토리얼을 역순으로 계산
    }
    
    while(M--){
        ll N, K;
        cin >> N >> K;
        if(K < 0 || K > N){
            cout << "0\n"; // K가 유효하지 않으면 0 출력
            continue;
        }
        // C(N,K) = fact[N] * inv_fact[K] % MOD * inv_fact[N-K] % MOD
        ll comb = fact[N] * inv_fact[K] % MOD;
        comb = comb * inv_fact[N-K] % MOD;
        cout << comb << "\n"; // 결과 출력
    }
}
```

**코드 설명**

1. **powmod 함수**: 페르마의 소정리를 이용하여 빠르게 거듭제곱을 계산한다. 이 함수는 $base^{exp} \mod mod$를 계산하며, 이항 계수의 역수를 구하는 데 사용된다.
2. **팩토리얼 계산**: $0!$부터 $4,000,000!$까지의 값을 미리 계산하여 `fact` 벡터에 저장한다.
3. **역팩토리얼 계산**: 마지막 팩토리얼의 역수를 `powmod` 함수를 이용하여 계산한 후, 이를 바탕으로 모든 역팩토리얼을 역순으로 계산하여 `inv_fact` 벡터에 저장한다.
4. **쿼리 처리**: 각 쿼리마다 $N$과 $K$를 입력받아, 유효성을 검사한 후, 미리 계산된 팩토리얼과 역팩토리얼을 이용하여 $\binom{N}{K}$를 계산하고 출력한다.

## C++ without library 코드와 설명

```cpp
#include <iostream>
using namespace std;

typedef long long ll;

const int MOD = 1000000007;

// Fast exponentiation to compute (base^exp) % MOD
ll powmod(ll base, ll exp, ll mod) {
    ll res = 1;
    base %= mod;
    while(exp > 0){
        if(exp & 1){
            res = res * base % mod; // 현재 비트가 1이면 결과에 base를 곱함
        }
        base = base * base % mod; // base를 제곱함
        exp >>= 1; // 다음 비트로 이동
    }
    return res;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    
    int M;
    cin >> M;
    
    // Maximum N is up to 4,000,000
    const int MAX = 4000000;
    ll fact[MAX+1];
    fact[0] = 1;
    for(int i=1; i<=MAX; ++i){
        fact[i] = fact[i-1] * i % MOD; // 팩토리얼을 미리 계산
    }
    
    // Compute inverse factorial
    ll inv_fact[MAX+1];
    inv_fact[MAX] = powmod(fact[MAX], MOD-2, MOD); // 마지막 팩토리얼의 역수 계산
    for(int i=MAX-1; i>=0; --i){
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD; // 역팩토리얼을 역순으로 계산
    }
    
    while(M--){
        ll N, K;
        cin >> N >> K;
        if(K < 0 || K > N){
            cout << "0\n"; // K가 유효하지 않으면 0 출력
            continue;
        }
        // C(N,K) = fact[N] * inv_fact[K] % MOD * inv_fact[N-K] % MOD
        ll comb = fact[N] * inv_fact[K] % MOD;
        comb = comb * inv_fact[N-K] % MOD;
        cout << comb << "\n"; // 결과 출력
    }
}
```

**코드 설명**

이 코드는 C++의 표준 라이브러리를 사용하지 않고, 기본적인 `iostream`만을 사용하여 동일한 기능을 구현하였다. 팩토리얼과 역팩토리얼을 배열에 직접 저장하고, `powmod` 함수를 이용하여 거듭제곱을 계산한다. 로직은 이전 C++ 코드와 동일하며, 각 부분에 대한 설명은 동일하다.

## Python 코드와 설명

```python
MOD = 10**9 + 7

def powmod(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2:
            result = result * base % mod  # 현재 비트가 1이면 결과에 base를 곱함
        base = base * base % mod  # base를 제곱함
        exp //= 2  # 다음 비트로 이동
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    M = int(data[0])
    queries = data[1:]
    
    MAX = 4000000
    fact = [1] * (MAX + 1)
    for i in range(1, MAX + 1):
        fact[i] = fact[i-1] * i % MOD  # 팩토리얼을 미리 계산
    
    inv_fact = [1] * (MAX + 1)
    inv_fact[MAX] = powmod(fact[MAX], MOD-2, MOD)  # 마지막 팩토리얼의 역수 계산
    for i in range(MAX-1, -1, -1):
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD  # 역팩토리얼을 역순으로 계산
    
    idx = 0
    for _ in range(M):
        N = int(queries[idx])
        K = int(queries[idx+1])
        idx += 2
        if K < 0 or K > N:
            print(0)  # K가 유효하지 않으면 0 출력
            continue
        comb = fact[N] * inv_fact[K] % MOD
        comb = comb * inv_fact[N-K] % MOD
        print(comb)  # 결과 출력

if __name__ == "__main__":
    main()
```

**코드 설명**

1. **powmod 함수**: C++ 코드와 동일하게 빠른 거듭제곱을 구현하였다. Python에서는 내장 함수 `pow`를 사용할 수도 있으나, 문제의 요구사항에 맞추어 직접 구현하였다.
2. **팩토리얼 계산**: 리스트 `fact`를 이용하여 $0!$부터 $4,000,000!$까지의 값을 미리 계산하고 저장한다.
3. **역팩토리얼 계산**: 마지막 팩토리얼의 역수를 `powmod` 함수를 이용하여 계산한 후, 이를 바탕으로 모든 역팩토리얼을 역순으로 계산하여 리스트 `inv_fact`에 저장한다.
4. **쿼리 처리**: 입력을 한 번에 읽어 리스트로 저장한 후, 각 쿼리마다 $N$과 $K$를 읽어 유효성을 검사한 후, 이항 계수를 계산하여 출력한다.

## 결론

이번 문제를 통해 대규모 이항 계수를 효율적으로 계산하는 방법을 학습할 수 있었다. 특히, 팩토리얼과 그 역수를 미리 계산해두는 방식은 많은 쿼리를 빠르게 처리할 수 있게 해준다. 또한, 페르마의 소정리를 이용한 모듈로 역수 계산은 수학적 아이디어가 중요한 역할을 한다는 것을 깨달았다. 추가적으로, Python에서는 내장 함수를 활용하여 더 간결하게 코드를 작성할 수 있지만, C++에서는 효율적인 구현을 위해 세부적인 최적화가 필요함을 확인할 수 있었다. 앞으로 유사한 문제를 풀 때, 이번에 배운 방법들을 응용하여 더 빠르고 효율적인 코드를 작성할 수 있을 것이다.