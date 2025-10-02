---
title: "[Algorithm] cpp 백준 12728번: n제곱 계산"
description: "정수부의 마지막 세 자리를 구하는 문제를 선형 점화식 s_n=6s_{n-1}-4s_{n-2}와 행렬 거듭제곱으로 O(log n)에 해결합니다. s_n-1≡⌊(3+√5)^n⌋을 이용해 모듈러 1000에서 안전히 계산하고 출력 서식·엣지 케이스까지 점검합니다."
date: 2025-09-16
lastmod: 2025-09-16
categories:
- Algorithm
- Math
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-12728
- cpp
- C++
- Matrix Exponentiation
- 행렬 거듭제곱
- Linear Recurrence
- 선형 점화식
- Recurrence
- 점화식
- Modular Arithmetic
- 모듈러 연산
- Modulo
- 모듈러
- Power
- 거듭제곱
- Matrix
- 행렬
- Fast Power
- 빠른 거듭제곱
- Binary Exponentiation
- 이진 거듭제곱
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Implementation
- 구현
- Precision
- 정밀도
- Rounding
- 반올림
- Number Theory
- 수학
- Math
- Integer Part
- 정수부
- Last Three Digits
- 마지막 세 자리
- Formatting
- 서식
- Zero Padding
- 0 패딩
- Case Format
- 출력 형식
- Fast I/O
- 빠른 입출력
- Overflow
- 오버플로
- 64-bit
- 64비트
- Matrix Power Mod
- 행렬 거듭제곱 모듈러
- ICPC
- Code Jam
- Google Code Jam
- Contest
- 대회
- Editorial
- 에디토리얼
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
image: "wordcloud.png"
aliases: /algorithm/BOJ-12728/
---

## 문제 정보
- 문제: https://www.acmicpc.net/problem/12728
- 요약: 실수 (3+√5)^n 의 정수부의 마지막 세 자리를 출력합니다. 정수부가 세 자리보다 작으면 0으로 채워 정확히 3자리를 만듭니다. 여러 테스트 케이스에 대해 "Case #X: Y" 형식으로 출력합니다.
- 제한: T ≤ 100, 2 ≤ n ≤ 2·10^9, 시간 5초, 메모리 512MB

## 입출력 형식/예제
```text
입력
2
5
2

출력
Case #1: 935
Case #2: 027
```

## 접근 개요(아이디어 스케치)
- 켤레를 이용해 a=3+√5, b=3-√5라 두면 s_n = a^n + b^n 은 항상 정수이며 s_0=2, s_1=6, s_n = 6s_{n-1} - 4s_{n-2}를 만족합니다.
- b≈0.7639… 이므로 n≥1에서 0<b^n<1 → ⌊a^n⌋ = s_n − 1. 따라서 답은 (s_n − 1) mod 1000 입니다.
- s_n 을 2×2 전이 행렬 [[6, -4], [1, 0]] 의 거듭제곱으로 O(log n) 에 구하고, 연산은 모두 mod 1000 에서 수행합니다.

## 알고리즘 설계
1) 점화식: s_0=2, s_1=6, s_n=6s_{n-1}-4s_{n-2}. 벡터 v_n=[s_n, s_{n-1}]^T, 행렬 A=[[6,-4],[1,0]] 로 v_n = A^{n-1} v_1.
2) 모듈러: mod=1000. 음수 계수는 (mod−4)로 치환하여 안전하게 연산합니다.
3) 거듭제곱: 이진 거듭제곱으로 A^{n-1}을 O(log n)에 계산.
4) 결과: s = (A^{n-1}·[6,2])_0 mod 1000, ans = (s−1) mod 1000. 앞자리는 0 패딩하여 3자리로 출력.
5) 다중 테스트: 각 케이스를 "Case #X: Y" 형식으로 출력.

### 올바름 근거(요지)
- 켤레 합 s_n=a^n+b^n 은 정수이며, 0<b^n<1 이므로 ⌊a^n⌋=s_n−1.
- 선형 점화식은 전이 행렬로 등가이며, 모듈러 환 Z/1000Z에서의 연산은 마지막 세 자리에만 영향을 주므로 정당합니다.
- 이진 거듭제곱은 반복 제곱의 표준 기법으로 O(log n) 시간에 올바른 결과를 산출합니다.

## 복잡도
- 시간: O(T log n)
- 공간: O(1)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Mat { long long a00, a01, a10, a11; };
static const long long MOD = 1000;

static inline Mat mul(const Mat& x, const Mat& y){
    Mat r;
    r.a00 = (x.a00 * y.a00 + x.a01 * y.a10) % MOD;
    r.a01 = (x.a00 * y.a01 + x.a01 * y.a11) % MOD;
    r.a10 = (x.a10 * y.a00 + x.a11 * y.a10) % MOD;
    r.a11 = (x.a10 * y.a01 + x.a11 * y.a11) % MOD;
    return r;
}

static Mat mpow(Mat base, long long exp){
    Mat res{1,0,0,1};
    while(exp>0){
        if(exp&1) res = mul(res, base);
        base = mul(base, base);
        exp >>= 1;
    }
    return res;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; if(!(cin >> T)) return 0;
    for(int tc=1; tc<=T; ++tc){
        long long n; cin >> n;

        long long s;
        if(n==0){
            s = 2 % MOD; // not used by constraints but kept for completeness
        }else if(n==1){
            s = 6 % MOD;
        }else{
            Mat A{6 % MOD, (MOD + (-4 % MOD)) % MOD, 1, 0};
            Mat B = mpow(A, n-1);
            s = (B.a00 * 6 + B.a01 * 2) % MOD; // [s_n, s_{n-1}]^T = B * [6,2]^T
        }

        long long ans = (s - 1) % MOD;
        if(ans < 0) ans += MOD;
        cout << "Case #" << tc << ": " << setw(3) << setfill('0') << ans << '\n';
    }
    return 0;
}
```

## 코너 케이스 체크리스트
- 최소 n=2, 최대 n=2·10^9 — 로그 시간 거듭제곱으로 처리되는지
- s_n ≡ 0 (mod 1000) 인 경우 → ans=999 출력되는지(0 패딩 포함)
- 출력 형식 "Case #X: Y" 및 줄바꿈, 3자리 0 패딩 준수
- 음수 계수 처리: -4 → (mod−4)로 치환되어 음수 모듈러 안전성 확보

## 제출 전 점검
- fast I/O 설정 확인, 64-bit 정수 사용 여부 확인
- 행렬 곱/제곱에서 모듈러 누락 없음, 오버플로 방지
- 여러 케이스 처리 시 상태 초기화(서식, 누적 변수) 점검

## 참고자료/유사문제
- 문제: https://www.acmicpc.net/problem/12728
- 켤레/선형 점화식 배경: https://cp-algorithms.com/algebra/binet-form.html
- 행렬 거듭제곱: https://cp-algorithms.com/algebra/binary-exp.html#matrix-exponentiation


