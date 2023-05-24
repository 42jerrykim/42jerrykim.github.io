---
title: "[C/C++] define 문을 namespace안에 선언하는건 의미가 없다."
categories:
  - "Cpp"
tags:
  - Language
  - Cpp
  - define
  - namespace
  - Preprocessor
---

전처리기인 Define 문을 namespace로 다른 코드와 분리 하여 사용하고 싶을 수가 있다. 하지만 define문은 namespace로 경계를 나눌 수 없다. 아래의 예시를 보고 왜 경계를 나눌 수 없는지 생각해 보자.

# define 문을 namespace안에 선언하는건 의미가 없다.

아래의 코드 처럼 define을 namespace에 선언이 되어 있다고 생각해보자. 아마 개발자는 define을 namespace로 감싸서 해당 namespace 안에서만 사용하도록 경계를 나누고 싶었던것 같다.

```cpp
namespace MyNamespace
{
  #define SOME_VALUE 0xDEADBABE
}
```

하지만 [Preprocessor](https://en.wikipedia.org/wiki/C_preprocessor)인 define은 namespace로 경계가 나누어 지지 않기 때문에 위와 같은 예시는 컴파일 단계를 지나면 경계를 나눈다는 목적은 사라지고 define 문은 전역으로 사용할 수 있게 된다.

# 특정 경계 안에서 상수를 사용하는 방법

따라서 상수를 namespace와 같이 경계를 나누어서 사용하려는 경우 아래와 같이 Preprocessor가 아닌 구분을 사용해야 한다.

```cpp
namespace MyNamespace
{
  const unsigned int SOME_VALUE = 0xDEADBABE;
}
```

본 예시에서는 namespace로 경계를 나누기 위해서 const를 사용해서 상수를 정의 하였다.
