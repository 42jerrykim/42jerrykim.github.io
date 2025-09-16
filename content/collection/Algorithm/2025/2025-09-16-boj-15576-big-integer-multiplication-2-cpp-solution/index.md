---
title: "[Algorithm] cpp 백준 15576번: 큰 수 곱셈 (2)"
description: "300,000자리까지의 초대형 정수 A·B를 FFT 기반 컨볼루션으로 O(n log n)에 곱합니다. 자리수 묶기(Base=1000), 안전 반올림, 캐리 정규화와 0 처리 같은 구현 디테일까지 정리해 제출 안정성을 높입니다. 시간·공간 복잡도와 실수 포인트를 한 문서에 모았습니다."
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
- Problem-15576
- cpp
- C++
- FFT
- Fast Fourier Transform
- 빠른 푸리에 변환
- Convolution
- 컨볼루션
- Big Integer
- 큰수
- Arbitrary Precision
- 임의정밀도
- Multiplication
- 곱셈
- String
- 문자열
- Parsing
- 파싱
- Base
- 진법
- Base 1000
- 자리수 묶기
- Digit Grouping
- Carry
- 자리올림
- Rounding
- 반올림
- Precision
- 정밀도
- Complex
- 복소수
- Double
- 부동소수점
- Accuracy
- 정확도
- Optimization
- 최적화
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Edge Cases
- 코너 케이스
- Implementation
- 구현
- Competitive Programming
- 경쟁프로그래밍
- O(n log n)
- Complexity Analysis
- 복잡도 분석
- Number Theory
- 수학
- String Processing
- 문자열처리
- Round-off Error
- 반올림 오차
- Stable
- 안정성
- High Performance
- 고성능
image: "wordcloud.png"
aliases: /algorithm/BOJ-15576/
---

## 문제
- 링크: https://www.acmicpc.net/problem/15576
- 요약: 두 비음수가 문자열로 주어질 때, 두 수의 곱을 출력합니다. 각 수의 길이는 최대 300,000자리이며, 불필요한 선행 0은 주어지지 않습니다(0 자체는 예외). 정답 역시 매우 길 수 있으므로 문자열로 출력해야 합니다.

## 입력/출력
```text
입력 예시
893724358493284 238947328947329
```
```text
출력 예시
213553048277135320552236238436
```

## 접근 개요
- 단순 곱셈은 O(n·m)으로 TLE입니다. 자릿수를 묶어(예: 10^3) 계수 다항식으로 보고, FFT로 컨볼루션을 수행해 O(n log n)으로 곱을 구합니다.
- 부동소수점 오차를 줄이기 위해 Base=1000(3자리 묶기)를 사용, 역변환 후 반올림(llround) + 캐리 정규화로 정확한 정수를 복원합니다.
- 입력에 0이 포함되면 즉시 0을 출력해 가지치기합니다.

## 알고리즘 설계
1) 문자열을 뒤에서 3자리씩 끊어 `vector<int>`(LSB 우선)로 변환
2) 복소수 기반 Cooley–Tukey FFT로 두 벡터를 컨볼루션
3) 실수부를 반올림하여 정수 계수 벡터 획득
4) 한 번에 캐리 정규화(올림/내림), 선행 0 제거
5) 최상위 블록 그대로 출력, 이하 블록은 자릿수(3) 맞춰 0 패딩 후 이어붙임

### 올바름/정밀도 근거(요지)
- 계수 컨볼루션은 다항식 곱의 계수를 정확히 재현하며, 자리수 묶기와 캐리 정규화를 통해 10진 곱과 동치가 됩니다.
- Base=1000은 double 정밀도에서 라운딩 오차 전파를 충분히 억제해 BOJ 데이터셋에서 안전합니다.

## 복잡도
- 시간: O(N log N), 여기서 N은 묶인 자릿수 길이의 다음 2의 거듭제곱
- 공간: O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io에서 확인할 수 있습니다.
#include <bits/stdc++.h>
using namespace std;

using cd = complex<double>;
const double PI = acos(-1.0);

static void fft(vector<cd> &a, bool invert) {
    int n = (int)a.size();

    static vector<int> rev;
    static vector<cd> roots{cd(0, 0), cd(1, 0)};

    if ((int)rev.size() != n) {
        rev.assign(n, 0);
        int k = __builtin_ctz(n);
        for (int i = 0; i < n; i++) {
            rev[i] = (rev[i >> 1] >> 1) | ((i & 1) << (k - 1));
        }
    }

    if ((int)roots.size() < n) {
        int k = __builtin_ctz((int)roots.size());
        roots.resize(n);
        while ((1 << k) < n) {
            double angle = 2 * PI / (1 << (k + 1));
            for (int i = 1 << (k - 1); i < (1 << k); i++) {
                roots[2 * i] = roots[i];
                double ang = angle * (2 * i + 1 - (1 << k));
                roots[2 * i + 1] = cd(cos(ang), sin(ang));
            }
            ++k;
        }
    }

    for (int i = 0; i < n; i++) {
        if (i < rev[i]) swap(a[i], a[rev[i]]);
    }

    for (int len = 1; len < n; len <<= 1) {
        for (int i = 0; i < n; i += 2 * len) {
            for (int j = 0; j < len; j++) {
                cd u = a[i + j];
                cd v = a[i + j + len] * roots[len + j];
                a[i + j] = u + v;
                a[i + j + len] = u - v;
            }
        }
    }

    if (invert) {
        reverse(a.begin() + 1, a.end());
        for (cd &x : a) x /= n;
    }
}

static vector<long long> convolution(const vector<int> &a, const vector<int> &b) {
    int n1 = (int)a.size();
    int n2 = (int)b.size();
    int n = 1;
    while (n < n1 + n2) n <<= 1;

    vector<cd> fa(n), fb(n);
    for (int i = 0; i < n1; i++) fa[i] = cd(a[i], 0);
    for (int i = 0; i < n2; i++) fb[i] = cd(b[i], 0);

    fft(fa, false);
    fft(fb, false);
    for (int i = 0; i < n; i++) fa[i] *= fb[i];
    fft(fa, true);

    vector<long long> res(n);
    for (int i = 0; i < n; i++) res[i] = llround(fa[i].real());
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    if (!(cin >> s >> t)) return 0;

    auto isZero = [](const string &x) {
        for (char c : x) if (c != '0') return false;
        return true;
    };
    if (isZero(s) || isZero(t)) { cout << 0 << '\n'; return 0; }

    const int base = 1000;      // 10^3
    const int base_digits = 3;  // group size

    auto toBase = [&](const string &x) {
        vector<int> v;
        for (int i = (int)x.size(); i > 0; i -= base_digits) {
            int l = max(0, i - base_digits);
            int val = 0;
            for (int j = l; j < i; j++) val = val * 10 + (x[j] - '0');
            v.push_back(val);
        }
        return v; // least significant block first
    };

    vector<int> a = toBase(s);
    vector<int> b = toBase(t);

    vector<long long> c = convolution(a, b);

    long long carry = 0;
    for (size_t i = 0; i < c.size(); i++) {
        long long cur = c[i] + carry;
        c[i] = (int)(cur % base);
        carry = cur / base;
    }
    while (carry > 0) { c.push_back((int)(carry % base)); carry /= base; }
    while (c.size() > 1 && c.back() == 0) c.pop_back();

    string out = to_string(c.back());
    for (int i = (int)c.size() - 2; i >= 0; i--) {
        string chunk = to_string((int)c[i]);
        if ((int)chunk.size() < base_digits) out += string(base_digits - (int)chunk.size(), '0');
        out += chunk;
    }
    cout << out << '\n';
    return 0;
}
```

## 코너 케이스 체크리스트
- A=0 또는 B=0 → 즉시 0 출력
- 한쪽이 한 자리(예: "1")인 경우 — 곱 결과 그대로 출력되는지
- 길이가 매우 긴 동일 자리수 패턴(예: 모두 9) — 캐리 연쇄 확인
- 선행 0 제거 정확성 — 최종 벡터의 상위 0 제거 여부
- Base 자리수 패딩 — 출력 시 중간 블록은 3자리 0 패딩

## 제출 전 점검
- 입출력 개행, fast I/O, 64-bit 사용 여부 확인
- 라운딩(llround) 후 캐리 정규화 루프 누락/오버플로 확인
- 선행 0 제거 후 빈 문자열 방지(최소 한 블록 보장)

## 참고자료
- 문제: https://www.acmicpc.net/problem/15576
- FFT/컨볼루션 배경: https://cp-algorithms.com/algebra/fft.html


