---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-05-15T00:00:00Z"
header:
  teaser: /assets/images/2024/2024-05-15-illustration_of_fft_approach_for_BOJ_1067.webp
tags:
- FFT
- DP
title: '[Algorithm] C++ 백준 1027번 : 이동'

---

BOJ 1067 문제는 주어진 배열을 왼쪽 또는 오른쪽으로 특정 횟수만큼 회전시키는 문제이다. 입력으로 배열의 길이 `(N)`, 배열의 원소들, 회전 횟수 `(K)`, 회전 방향 `(D)`가 주어지며, `(D)`가 'L'이면 왼쪽으로, 'R'이면 오른쪽으로 배열을 `(K)`번 회전시킨 결과를 출력한다. `(K)`가 `(N)`보다 클 경우, 실제로는 `K % N`번 회전하는 것과 동일하다.

|![이미지](/assets/images/2024/2024-05-15-A_detailed_illustration_of_a_cyclic_array_rotation.png)|
|:---:|
|이미지로 형상화|
지
## 문제 분석 및 접근 방법

BOJ 1067번 문제는 두 개의 수열 `(X)`와 `(Y)`가 주어졌을 때, `(Y)`를 순환 이동시키며 두 수열의 일치하는 요소의 곱의 합이 최대가 되는 값을 구하는 문제이다. `(Y)`를 순환 이동하는 것은 `(Y)`를 두 배 길이로 확장한 후 FFT를 이용하여 문제를 해결할 수 있다.

### 접근 방법

1. `(X)`와 `(Y)`의 길이를 동일하게 `(n)`으로 맞춘다.
2. `(Y)`를 두 배 길이로 확장하여 `(Y' = Y + Y)`로 만든다.
3. FFT를 이용하여 `(X)`와 `(Y')`의 곱을 계산한 후, 최대 곱의 합을 구한다.

### C++ 코드 구현

아래는 주어진 접근 방법을 기반으로 작성된 C++ 코드이다.

```cpp
#include <iostream>
#include <vector>
#include <complex>
#include <cmath>
#include <algorithm>

const double PI = acos(-1);

// FFT 함수
void fft(std::vector<std::complex<double>>& a, bool invert) {
    int n = a.size();
    for (int i = 1, j = 0; i < n; ++i) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1)
            j ^= bit;
        j ^= bit;
        if (i < j)
            std::swap(a[i], a[j]);
    }

    for (int len = 2; len <= n; len <<= 1) {
        double angle = 2 * PI / len * (invert ? -1 : 1);
        std::complex<double> wlen(cos(angle), sin(angle));
        for (int i = 0; i < n; i += len) {
            std::complex<double> w(1);
            for (int j = 0; j < len / 2; ++j) {
                std::complex<double> u = a[i + j];
                std::complex<double> v = a[i + j + len / 2] * w;
                a[i + j] = u + v;
                a[i + j + len / 2] = u - v;
                w *= wlen;
            }
        }
    }

    if (invert) {
        for (std::complex<double>& x : a)
            x /= n;
    }
}

// 두 다항식의 곱셈 함수
std::vector<int> multiply(const std::vector<int>& a, const std::vector<int>& b) {
    std::vector<std::complex<double>> fa(a.begin(), a.end()), fb(b.begin(), b.end());
    int n = 1;
    while (n < a.size() + b.size()) 
        n <<= 1;
    fa.resize(n);
    fb.resize(n);

    fft(fa, false);
    fft(fb, false);
    for (int i = 0; i < n; ++i)
        fa[i] *= fb[i];
    fft(fa, true);

    std::vector<int> result(n);
    for (int i = 0; i < n; ++i)
        result[i] = round(fa[i].real());
    return result;
}

int main() {
    int n;
    std::cin >> n;
    std::vector<int> x(n), y(n);

    for (int i = 0; i < n; ++i)
        std::cin >> x[i];
    for (int i = 0; i < n; ++i)
        std::cin >> y[i];

    std::reverse(y.begin(), y.end());

    std::vector<int> extended_y = y;
    extended_y.insert(extended_y.end(), y.begin(), y.end()); // Y를 두 배 길이로 확장

    std::vector<int> result = multiply(x, extended_y);

    int max_value = *std::max_element(result.begin() + n - 1, result.begin() + 2 * n - 1);

    std::cout << max_value << std::endl;
    return 0;
}
```

### 요약

1. `(X)`와 `(Y)`의 길이를 동일하게 맞춘다.
2. `(Y)`를 두 배 길이로 확장한다.
3. FFT를 이용해 다항식 곱셈을 수행한다.
4. 최대 곱의 합을 찾아 출력한다.

이 코드는 주어진 문제를 해결하기 위해 `(Y)`를 두 배 길이로 확장한 후, FFT를 사용하여 두 수열의 곱을 계산하고 최대 값을 찾는다.