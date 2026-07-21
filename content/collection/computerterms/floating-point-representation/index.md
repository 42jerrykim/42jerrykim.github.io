---
image: "wordcloud.png"
slug: floating-point-representation
collection_order: 63
draft: false
title: "[Computer Terms] 부동소수점 표현 (IEEE 754 Floating Point)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "부호·지수·가수로 실수를 근사하는 IEEE 754 형식을 설명하고, 0.1+0.2가 정확히 0.3이 되지 않는 이유와 부동소수점 값을 비교할 때 epsilon 오차 허용이 필요한 이유를 컴파일 가능한 C 코드로 재현해 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Computer-Architecture(컴퓨터구조)
- CPU
- Performance(성능)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Software-Engineering(소프트웨어공학)
- Memory(메모리)
- Debugging(디버깅)
- C
- IEEE-754(부동소수점표준)
- Floating-Point(부동소수점)
- Numerical-Computing(수치계산)
- Precision(정밀도)
- Standard(표준)
- Testing(테스트)
---

## 이 장을 읽기 전에

[SIMD](/post/computerterms/simd/)에서 수치 연산을 대량으로 처리하는 벡터 연산을 다뤘다. 이 챕터는 그 수치 연산이 다루는 실수 자체가 컴퓨터 안에서 어떻게 표현되는지, 그리고 왜 그 표현이 수학적으로 정확한 실수와 다를 수밖에 없는지를 다룬다. 이 챕터는 SIMD·성능보다는 정확성·디버깅 관점에서 실수 연산을 이해하는 데 필요한 기초다.

## IEEE 754: 부호·지수·가수로 실수를 근사하기

정수는 유한한 비트로 정확히 표현할 수 있지만, 실수는 무한히 많은 소수점 아래 자리를 가질 수 있어 유한한 비트로는 근본적으로 **근사**할 수밖에 없다. **IEEE 754**는 이 근사를 표준화한 규격으로, 실수를 부호(Sign), 지수(Exponent), 가수(Mantissa/Significand) 세 부분으로 나눠 표현한다. 32비트 단정밀도(`float`)는 부호 1비트, 지수 8비트, 가수 23비트로 구성되고, 64비트 배정밀도(`double`)는 부호 1비트, 지수 11비트, 가수 52비트로 구성된다. 값은 대략 `(-1)^부호 × 1.가수 × 2^(지수 - 편향값)` 형태로 계산되며, 이는 과학적 표기법(예: `1.234 × 10^5`)을 2진수 버전으로 옮긴 것과 같은 발상이다.

```text
부호(1비트) | 지수(8비트, float 기준) | 가수(23비트, float 기준)
    S       |        EEEEEEEE         |  MMMMMMMMMMMMMMMMMMMMMMM
```

## 0.1 + 0.2가 정확히 0.3이 되지 않는 이유

문제는 10진수로 유한한 소수(`0.1`, `0.2`)조차 2진수로는 **무한소수**가 되는 경우가 많다는 데 있다. `0.1`을 2진수로 바꾸면 `0.0001100110011...`처럼 `0011`이 무한 반복되는데, IEEE 754는 유한한 비트(가수 23비트 또는 52비트)만 쓸 수 있으므로 이 무한소수를 어딘가에서 잘라 근사값으로 저장한다. `0.1`과 `0.2`는 각각 아주 근소하게 다른 근사 오차를 갖고 저장되고, 이 둘을 더하면 오차가 누적돼 `0.3`을 표현하는 이진 근사값과 정확히 일치하지 않는 값이 나온다. 이는 버그가 아니라 **2진 부동소수점으로 10진 소수를 정확히 표현할 수 없다는 근본적 한계**다.

```c
#include <stdio.h>

int main(void) {
    double a = 0.1;
    double b = 0.2;
    double sum = a + b;

    printf("a + b      = %.20f\n", sum);          /* 0.30000000000000004441... */
    printf("0.3        = %.20f\n", 0.3);           /* 0.29999999999999998890... */
    printf("a + b == 0.3 ? %s\n", (sum == 0.3) ? "true" : "false");   /* false */

    return 0;
}
```

`gcc -std=c11 float_demo.c -o float_demo && ./float_demo`로 컴파일·실행하면 `sum`과 `0.3`이 서로 다른 비트 패턴으로 저장돼 있어 `==` 비교가 `false`를 반환하는 것을 직접 확인할 수 있다. `%.20f`로 소수점 아래 20자리까지 출력하면, `0.1 + 0.2`의 실제 저장값이 수학적인 `0.3`보다 아주 미세하게 큰 값이라는 것이 드러난다.

## 부동소수점 비교에는 오차 허용(epsilon)이 필요하다

위 예시가 보여주듯, 부동소수점 값 두 개를 `==`로 직접 비교하는 것은 대부분의 상황에서 안전하지 않다. 대신 두 값의 차이가 아주 작은 허용 오차(**epsilon**) 이내인지를 확인하는 방식을 쓴다.

```c
#include <stdio.h>
#include <math.h>

int nearly_equal(double a, double b, double epsilon) {
    return fabs(a - b) < epsilon;
}

int main(void) {
    double sum = 0.1 + 0.2;

    printf("직접 비교 (==): %s\n", (sum == 0.3) ? "true" : "false");            /* false */
    printf("epsilon 비교:  %s\n", nearly_equal(sum, 0.3, 1e-9) ? "true" : "false"); /* true */

    return 0;
}
```

`epsilon` 값은 다루는 수치의 크기와 요구 정밀도에 따라 달라져야 한다 — 아주 큰 수를 비교할 때 `1e-9`처럼 작은 고정 epsilon을 그대로 쓰면, 그 수 자체의 표현 오차가 이미 epsilon보다 커서 여전히 오탐이 날 수 있다(구현 정의: 실무에서는 상대 오차 방식이나 언어별 부동소수점 비교 유틸리티를 함께 검토해야 한다).

## 비교: 정수 표현 vs 부동소수점 표현

| 특성 | 정수(`int`) | 부동소수점(`float`/`double`) |
|---|---|---|
| 표현 방식 | 값을 그대로 2진수로 저장 | 부호·지수·가수로 근사 |
| 정확도 | 표현 범위 내에서 항상 정확 | 대부분의 10진 소수를 근사값으로만 표현 |
| 덧셈 결합법칙 | 항상 성립 | 반올림 오차로 인해 항상 성립하지는 않음 |
| 동등 비교(`==`) | 안전 | 대부분 위험, epsilon 비교 권장 |

## 흔한 오개념

**"0.1 + 0.2 != 0.3은 특정 언어나 컴파일러의 버그다"** — 이는 C뿐 아니라 IEEE 754를 따르는 거의 모든 언어(Python, Java, JavaScript 등)에서 똑같이 재현된다. 언어의 결함이 아니라, 10진 소수를 유한한 2진 비트로 정확히 표현할 수 없다는 부동소수점 표준 자체의 근본 한계다.

**"double을 쓰면 float보다 항상 정확해서 오차 문제가 사라진다"** — `double`은 가수 비트가 더 많아 근사 오차가 작아질 뿐, 근사 자체가 사라지지는 않는다. `0.1 + 0.2 != 0.3`은 `double`에서도 여전히 재현된다(위 코드가 실제로 `double`을 쓴 예시다). 정밀도를 높이는 것과 오차를 완전히 없애는 것은 다른 문제다.

## 다른 개념과의 연결

[SIMD](/post/computerterms/simd/)에서 다룬 벡터 연산은 부동소수점 배열에 자주 쓰이는데, 반복 순서에 따라 반올림 오차가 누적되는 순서가 달라질 수 있어 SIMD로 재정렬된 연산이 스칼라 연산과 미세하게 다른 결과를 낼 수 있다는 점이 여기서 이어진다. 다음 챕터에서는 명령어와 데이터가 같은 메모리 공간에 저장되는 폰 노이만 구조를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. IEEE 754가 부호·지수·가수로 실수를 근사하는 방식을 설명할 수 있다. `0.1 + 0.2 != 0.3`이 왜 버그가 아니라 2진 부동소수점의 근본적 한계인지 설명할 수 있다. 부동소수점 비교에 epsilon이 필요한 이유와, epsilon 선택 시 주의할 점을 설명할 수 있다.

## 참고 자료

> IEEE Standard for Floating-Point Arithmetic (IEEE 754-2019), IEEE Computer Society.

- [Wikipedia: IEEE 754](https://en.wikipedia.org/wiki/IEEE_754) — IEEE 754 형식의 비트 구성과 특수값(NaN, Infinity 등) 개요
- [floating-point-gui.de: What Every Programmer Should Know About Floating-Point Arithmetic](https://floating-point-gui.de/) — 부동소수점 비교·오차 허용에 대한 실무 가이드
