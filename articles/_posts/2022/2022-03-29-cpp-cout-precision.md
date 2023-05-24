---
title: "[C/C++] C언어, C++ 소수점 자릿수 조절하기"
category: Cpp
tag:
 - Cpp
 - cout
 - 소수점
 - 정확도
 - 출력
---

`cin`, `cout` 을 사용할 경우 입력은 문제가 없지만 출력의 경우 약간 복잡하다. 두 가지를 알아야 소수점 자리를 고정하여 출력 할 수 있다.

# 소수점 짤리지 않게 출력하는 방법

하나는 `std::fixed`, 또 하나는 `std::cout.precision()` 이다.

```cpp
std::fixed // 소수점 아래로 고정
std::cout.precision(n);	// 실수 전체 자리수 중 n자리 까지 표현
```

일단, `precision()` 에 대해 말하자면 출력 할 실수 전체 자리수를 n자리로 표현 것이다. 소수점 아래로 n자리만큼 고정하는 것이 아니다.

아래 예시를 보자.

```cpp
#include <iostream>

int main()
{
    double a = 1234.5678;
    std::cout.precision(6);

    std::cout << a;	// 1234.567 에서 반올림 된 1234.57 이 출력 됨
}
```
 
위와 같이 실수 전체에 대한 자리수 표현이다보니 만약 오차범위를 넉넉하게 주려면 `precision` 의 파라미터를 큰 수로 넘겨주어야 한다.

만약 정수 부분은 신경쓰지 않고 소수점 아래로만 고정하고 싶은 경우는 어떻게 하느냐..

이럴 때 쓰는 것이 `fixed` 다.

fixed 는 고정 소수점 표기로 만약 fixed를 쓰면 그 다음부터 들어오는 출력들은 소수점 아래로 설정한 `precision`으로 넘겨준 값 만큼 출력이 된다.

즉, 다음과 같다는 말이다.

```cpp
#include <iostream>

int main()
{
    double a = 3333.333333;
    
    std::cout.precision(6);
    
    std::cout << a << std::endl; // 3333.33 이 출력됨
    
    std::cout << std::fixed; // 고정 소수점 표기로 전환
    std::cout << a << std::endl; // 3333.333333 이 출력 됨
    
    std::cout.unsetf(std::ios::fixed); // 고정 소수점 표기 해제

    std::cout << a << std::endl; // 3333.33 이 출력됨
}
```

위처럼 만약에 `fixed`를 해제하고 싶다면 `cout.unsetf()` 에 `std::ios::fixed` 를 넘겨주면 된다.
