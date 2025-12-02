---
image: "tmp_wordcloud.png"
title : "[Algorithm] C++ 백준 1008번 : A/B"
date: 2022-01-01T00:00:00Z
categories: Algorithm
tags: 
- C++
- BOJ
- 백준
- 소수점
- 출력
- 입력
- 문제
- 알고리즘
- 코딩
- Programming
- Algorithm
- CodingTest
- ProblemSolving
- DataStructures
- Algorithms
- CodingChallenges
- BaekjoonOnlineJudge
- CompetitiveProgramming
- CodeOptimization
- ProgrammingBasics
- CodingPractice
- AlgorithmStudy
- ProgrammingTutorial
- CodingSkills
- ProblemSolvingSkills
- ComputerScience
- SoftwareEngineering
- CodingEducation
- ProgrammingLanguages
- CodeExamples
- AlgorithmAnalysis
- CodingInterview
- TechnicalSkills
- CodeImplementation
- SoftwareDevelopment
- CodingTips
- AlgorithmDesign
- ProgrammingLogic
- ProblemSolvingTechniques
- ComputationalThinking
- AlgorithmEfficiency
- ProgrammingPractice
- CodingMethodology
- AlgorithmPatterns
- CodingBestPractices
- ComputerProgramming
- CodingExercises
- AlgorithmImplementation
- ProgrammingSkills
- SoftwareEngineering
- AlgorithmOptimization
image: "index.png"
---



[1008번: A/B](https://www.acmicpc.net/problem/1008) 문제는 두 정수 A와 B를 입력받은 다음, A/B를 출력하는 문제이다. +, -, *를 할 수 있었다면 쉬운 문제로 보인다. 하지만 막상 문제를 풀어보면 실패를 맛 볼 수 있다. 어떤 문제가 있어서 실패를 하는지 알아보자.

## 문제 이해

백준 1008번 문제는 두 정수 A와 B를 입력받아 A/B를 출력하는 간단한 문제처럼 보이지만, 실제로는 floating-point 처리와 output formatting에 대한 이해가 필요한 문제이다. 특히, C++에서 실수를 다룰 때 발생할 수 있는 문제점들을 명확히 이해하고 있어야 한다.

## 시행 착오

```cpp
#include <iostream>

int main()
{
    double a, b;
    std::cin >> a >> b;
    std::cout << a / b;
}
```

간단하게 생각하고 위의 코드처럼 작성하였지만 결과는 실패한다.

결과물을 확인할 수 있는 IDE나 [Online compiler](https://rextester.com/l/cpp_online_compiler_gcc)를 사용하면 **소수점**이 짤리는 것을 확인할 수 있다.

## 소수점 짤리지 않게 출력하는 방법

`cin`, `cout`을 사용할 경우 입력은 문제가 없지만 출력의 경우 약간 복잡하다. 두 가지를 알아야 소수점 자리를 고정하여 출력할 수 있다.

하나는 `std::fixed`, 또 하나는 `std::cout.precision()`이다.

```cpp
std::fixed // 소수점 아래로 고정
std::cout.precision(n);	// 실수 전체 자리수 중 n자리까지 표현
```

일단, `precision()`에 대해 말하자면 출력할 실수 전체 자리수를 n자리로 표현하는 것이다. 소수점 아래로 n자리만큼 고정하는 것이 아니다.

아래 예시를 보자.

```cpp
#include <iostream>

int main()
{
    double a = 1234.5678;
    std::cout.precision(6);

    std::cout << a;	// 1234.567에서 반올림된 1234.57이 출력됨
}
```

위와 같이 실수 전체에 대한 자리수 표현이므로 만약 오차범위를 넉넉하게 주려면 `precision`의 파라미터를 큰 수로 넘겨주어야 한다.

만약 정수 부분은 신경쓰지 않고 소수점 아래로만 고정하고 싶은 경우는 어떻게 하느냐..

이럴 때 쓰는 것이 `fixed`이다.

`fixed`는 고정 소수점 표기로 만약 `fixed`를 쓰면 그 다음부터 들어오는 출력들은 소수점 아래로 설정한 `precision`으로 넘겨준 값만큼 출력이 된다.

즉, 다음과 같다는 말이다.

```cpp
#include <iostream>

int main()
{
    double a = 3333.333333;
    
    std::cout.precision(6);
    
    std::cout << a << std::endl; // 3333.33이 출력됨
    
    std::cout << std::fixed; // 고정 소수점 표기로 전환
    std::cout << a << std::endl; // 3333.333333이 출력됨
    
    std::cout.unsetf(std::ios::fixed); // 고정 소수점 표기 해제

    std::cout << a << std::endl; // 3333.33이 출력됨
}
```

위처럼 만약에 `fixed`를 해제하고 싶다면 `cout.unsetf()`에 `std::ios::fixed`를 넘겨주면 된다.

## 정답 코드

```cpp
#include <iostream>

int main()
{
    std::cout.precision(10);
    std::cout << std::fixed; 

    double a, b;
    std::cin >> a >> b;
    std::cout << a / b;
}
```

9자리까지 출력하는 문제이므로 넉넉하게 `std::cout.precision(10);`을 주었다.

## 주의할 점
1. **Precision 문제**: C++에서 실수 연산은 floating-point 방식을 사용하기 때문에 precision 문제가 발생할 수 있다. 이는 특히 소수점 이하 자릿수가 많은 경우에 두드러진다.
2. **Output format**: 기본적으로 `cout`은 실수를 출력할 때 scientific notation을 사용할 수 있으며, 소수점 이하 자릿수를 제한할 수 있다. 따라서 정확한 출력을 위해 output format을 명시적으로 설정해야 한다.

## 추가 설명
### Floating-point의 이해
C++에서 `double` 타입은 일반적으로 64-bit floating-point를 사용한다. 이는 약 15~17자리의 유효숫자를 가질 수 있지만, 정확한 소수점 이하 자릿수를 보장하지는 않는다. 따라서 문제에서 요구하는 정확도를 맞추기 위해서는 output 방식을 조절해야 한다.

### Output format 조절
`std::fixed`와 `std::cout.precision()`을 함께 사용하면 소수점 이하 자릿수를 고정할 수 있다. 이는 특히 문제에서 특정 자릿수까지의 output을 요구할 때 유용하다.

## 예제 코드 분석
```cpp
#include <iostream>

int main() {
    double a = 0.123456789;
    std::cout.precision(5);
    std::cout << a << std::endl;  // 0.12346 출력 (반올림)
    
    std::cout << std::fixed;
    std::cout << a << std::endl;  // 0.12346 출력 (소수점 이하 5자리 고정)
}
```
이 예제는 `precision`과 `fixed`의 차이를 명확히 보여준다. `fixed`를 사용하면 소수점 이하 자릿수를 정확히 제어할 수 있다.

## 결론

C++에서 실수를 처리할 때는 precision 문제와 output format 문제를 해결해야 한다. 이를 위해 `std::fixed`와 `std::cout.precision()`을 함께 사용하여 소수점 이하 자릿수를 정확히 제어할 수 있다.
