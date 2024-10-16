---
title: "[Algorithm] C++/Python 백준 28702번 : FizzBuzz 스페셜 저지"
categories: Algorithm
tags:
- Mathematics
- Strings
- Simulation
- Brute Force
- Modulo
- FizzBuzz
image: "tmp_wordcloud.png"
date: 2024-10-16
---

이번 포스팅에서는 백준 온라인 저지의 28702번 문제인 **"FizzBuzz 스페셜 저지"**를 다뤄보겠습니다. 이 문제는 고전적인 FizzBuzz 문제를 변형한 것으로, 주어진 연속된 세 개의 출력값을 기반으로 다음에 올 출력을 예측하는 문제입니다. 수학적 사고와 문자열 처리가 요구되는 재미있는 문제입니다.

문제 : [https://www.acmicpc.net/problem/28702](https://www.acmicpc.net/problem/28702)

## 문제 설명

**FizzBuzz 문제**는 다음과 같은 규칙을 따르는 고전적인 프로그래밍 문제입니다. 양의 정수 `i`가 1부터 시작하여 1씩 증가할 때, 각 `i`에 대해 다음의 규칙에 따라 문자열을 출력합니다.

1. `i`가 **3의 배수이면서 5의 배수**이면 `"FizzBuzz"`를 출력합니다.
2. `i`가 **3의 배수이지만 5의 배수가 아니면** `"Fizz"`를 출력합니다.
3. `i`가 **3의 배수가 아니지만 5의 배수이면** `"Buzz"`를 출력합니다.
4. `i`가 **3의 배수도 아니고 5의 배수도 아니면** `i`를 그대로 출력합니다.

예를 들어, `i`가 1부터 15까지일 때의 출력은 다음과 같습니다.

```
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
```

**문제**에서는 FizzBuzz 문제에서 **연속으로 출력된 세 개의 문자열**이 주어집니다. 이때, 이 세 문자열 **다음에 올 문자열**을 구하는 것이 목표입니다. 입력으로 주어지는 세 개의 문자열은 각 줄에 하나씩 주어지며, 길이는 8 이하입니다. 주어진 입력은 항상 FizzBuzz 문제에서 연속으로 출력된 세 개의 문자열에 대응함이 보장됩니다.

예를 들어, 입력이 다음과 같을 때:

```
Fizz
Buzz
11
```

이 경우 다음에 올 출력은 `"Fizz"`가 됩니다.

또 다른 예로, 입력이 다음과 같을 때:

```
980803
980804
FizzBuzz
```

다음에 올 출력은 `"980806"`이 됩니다.

문제의 목표는 주어진 세 개의 연속된 FizzBuzz 출력값을 기반으로, 그 다음에 올 출력을 정확히 예측하여 출력하는 것입니다. 만약 가능한 출력이 여러 개라면, 그 중 아무거나 하나를 출력하면 됩니다.

## 접근 방식

이 문제를 해결하기 위해서는 주어진 세 개의 문자열을 기반으로, **FizzBuzz 규칙**에 따라 다음에 올 출력을 예측해야 합니다. 주요한 접근 방식은 다음과 같습니다.

1. **입력된 문자열 분석**: 세 개의 입력된 문자열을 하나씩 확인하여, 각 문자열이 `"Fizz"`, `"Buzz"`, `"FizzBuzz"` 중 하나인지, 아니면 숫자인지를 판별합니다.

2. **가능한 `i` 값 계산**: 입력된 문자열이 숫자라면, 그 숫자가 FizzBuzz 순서상의 몇 번째 숫자인지 역으로 추정할 수 있습니다. 예를 들어, 입력된 숫자가 `n`이고, 그것이 `k`번째 입력이라면, 실제 FizzBuzz 순서상의 위치 `i`는 `i = n - k`가 됩니다.

3. **일관성 검증**: 세 개의 입력에 대해 계산된 `i` 값이 모두 일관성 있는지 확인합니다. 만약 일관성이 없다면, 입력된 세 개의 문자열이 연속된 FizzBuzz 출력값이 아니라는 의미이므로 문제의 조건에 위배됩니다.

4. **다음 출력 계산**: 일관성 있는 시작점 `i`를 찾았다면, `i + 3`번째 값에 대해 FizzBuzz 규칙을 적용하여 다음 출력을 계산합니다.

5. **숫자가 없는 경우 처리**: 만약 세 개의 입력된 문자열 모두가 `"Fizz"`, `"Buzz"`, `"FizzBuzz"`로만 이루어져 있다면, FizzBuzz 패턴의 주기가 15임을 이용하여 가능한 모든 시작점을 탐색합니다 (1부터 15까지). 각 가능한 시작점에 대해 주어진 세 개의 문자열이 해당 위치에서의 FizzBuzz 출력과 일치하는지 확인하고, 일치하는 경우 다음 출력을 계산합니다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>

using namespace std;

// 주어진 시작점 i와 입력된 문자열 s가 일치하는지 확인하는 함수
bool isValid(long long i, const vector<string>& s) {
    for (int k = 0; k < 3; ++k) {
        long long ik = i + k;  // 현재 위치의 i 값
        string sk = s[k];      // 입력된 문자열
        if (sk == "FizzBuzz") {
            if (ik % 15 != 0) return false;
        } else if (sk == "Fizz") {
            if (ik % 3 != 0 || ik % 5 == 0) return false;
        } else if (sk == "Buzz") {
            if (ik % 5 != 0 || ik % 3 == 0) return false;
        } else {
            // 숫자인 경우
            long long nk = atoll(sk.c_str());
            if (ik != nk) return false;
            if (ik % 3 == 0 || ik % 5 == 0) return false;
        }
    }
    return true;
}

// 주어진 i 값에 대해 FizzBuzz 출력을 계산하는 함수
string FizzBuzz(long long i) {
    if (i % 15 == 0) return "FizzBuzz";
    else if (i % 3 == 0) return "Fizz";
    else if (i % 5 == 0) return "Buzz";
    else return to_string(i);
}

int main() {
    vector<string> s(3);
    for (int i = 0; i < 3; ++i) {
        cin >> s[i];  // 입력된 세 개의 문자열
    }

    bool hasNumber = false;
    long long i_value = -1;

    // 숫자가 있는지 확인하고 가능한 i 값 계산
    for (int k = 0; k < 3; ++k) {
        if (s[k] != "Fizz" && s[k] != "Buzz" && s[k] != "FizzBuzz") {
            hasNumber = true;
            long long nk = atoll(s[k].c_str());  // 문자열을 숫자로 변환
            long long i_candidate = nk - k;      // 가능한 시작점 계산
            if (i_value == -1) {
                i_value = i_candidate;
            } else if (i_value != i_candidate) {
                // 일관성 없는 경우 종료
                cout << "No solution" << endl;
                return 0;
            }
        }
    }

    if (hasNumber) {
        // 숫자가 있는 경우
        if (i_value < 1) {
            cout << "No solution" << endl;
            return 0;
        }
        if (isValid(i_value, s)) {
            cout << FizzBuzz(i_value + 3) << endl;  // 다음 출력 계산
            return 0;
        } else {
            cout << "No solution" << endl;
            return 0;
        }
    } else {
        // 숫자가 없는 경우 가능한 시작점 탐색
        for (int i_mod15 = 1; i_mod15 <= 15; ++i_mod15) {
            long long i_candidate = i_mod15;
            bool valid = isValid(i_candidate, s);
            if (valid) {
                cout << FizzBuzz(i_candidate + 3) << endl;  // 다음 출력 계산
                return 0;
            }
        }
        cout << "No solution" << endl;
        return 0;
    }
}
```

위의 코드는 입력된 세 개의 문자열을 기반으로 다음에 올 FizzBuzz 출력을 계산하는 프로그램입니다.

- **입력 처리**:
  ```cpp
  vector<string> s(3);
  for (int i = 0; i < 3; ++i) {
      cin >> s[i];  // 세 개의 문자열 입력
  }
  ```
  세 개의 문자열을 입력받아 벡터 `s`에 저장합니다.

- **숫자 확인 및 가능한 시작점 계산**:
  ```cpp
  bool hasNumber = false;
  long long i_value = -1;

  for (int k = 0; k < 3; ++k) {
      if (s[k] != "Fizz" && s[k] != "Buzz" && s[k] != "FizzBuzz") {
          hasNumber = true;
          long long nk = atoll(s[k].c_str());  // 문자열을 숫자로 변환
          long long i_candidate = nk - k;      // 가능한 시작점 계산
          if (i_value == -1) {
              i_value = i_candidate;
          } else if (i_value != i_candidate) {
              // 시작점이 일관성 없으면 종료
              cout << "No solution" << endl;
              return 0;
          }
      }
  }
  ```
  입력된 문자열 중 숫자가 있는지 확인하고, 숫자가 있다면 가능한 시작점 `i_value`를 계산합니다. 만약 여러 숫자가 있고 계산된 시작점이 서로 다르면 일관성이 없으므로 종료합니다.

- **시작점 검증 및 다음 출력 계산**:
  ```cpp
  if (hasNumber) {
      // 숫자가 있는 경우
      if (i_value < 1) {
          cout << "No solution" << endl;
          return 0;
      }
      if (isValid(i_value, s)) {
          cout << FizzBuzz(i_value + 3) << endl;  // 다음 출력 계산
          return 0;
      } else {
          cout << "No solution" << endl;
          return 0;
      }
  }
  ```
  계산된 시작점이 유효한지 `isValid` 함수를 통해 확인하고, 유효하다면 `i + 3`번째 FizzBuzz 출력을 계산하여 출력합니다.

- **숫자가 없는 경우 가능한 시작점 탐색**:
  ```cpp
  else {
      // 숫자가 없는 경우
      for (int i_mod15 = 1; i_mod15 <= 15; ++i_mod15) {
          long long i_candidate = i_mod15;
          bool valid = isValid(i_candidate, s);
          if (valid) {
              cout << FizzBuzz(i_candidate + 3) << endl;  // 다음 출력 계산
              return 0;
          }
      }
      cout << "No solution" << endl;
      return 0;
  }
  ```
  숫자가 없다면 FizzBuzz 패턴의 주기인 15를 이용하여 가능한 시작점을 모두 탐색합니다. 유효한 시작점을 찾으면 다음 출력을 계산하여 출력합니다.

- **`isValid` 함수**:
  ```cpp
  bool isValid(long long i, const vector<string>& s) {
      for (int k = 0; k < 3; ++k) {
          long long ik = i + k;
          string sk = s[k];
          if (sk == "FizzBuzz") {
              if (ik % 15 != 0) return false;
          } else if (sk == "Fizz") {
              if (ik % 3 != 0 || ik % 5 == 0) return false;
          } else if (sk == "Buzz") {
              if (ik % 5 != 0 || ik % 3 == 0) return false;
          } else {
              long long nk = atoll(sk.c_str());
              if (ik != nk) return false;
              if (ik % 3 == 0 || ik % 5 == 0) return false;
          }
      }
      return true;
  }
  ```
  주어진 시작점 `i`에서 입력된 세 개의 문자열이 FizzBuzz 규칙과 일치하는지 확인합니다.

- **`FizzBuzz` 함수**:
  ```cpp
  string FizzBuzz(long long i) {
      if (i % 15 == 0) return "FizzBuzz";
      else if (i % 3 == 0) return "Fizz";
      else if (i % 5 == 0) return "Buzz";
      else return to_string(i);
  }
  ```
  주어진 `i`에 대해 FizzBuzz 출력을 반환합니다.

## C++ without library 코드와 설명

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 문자열이 숫자인지 확인하는 함수
int isNumber(char *s) {
    return !(strcmp(s, "Fizz") == 0 || strcmp(s, "Buzz") == 0 || strcmp(s, "FizzBuzz") == 0);
}

// 주어진 시작점 i와 입력된 문자열 s가 일치하는지 확인하는 함수
int isValid(long long i, char s[3][9]) {
    int k;
    for (k = 0; k < 3; ++k) {
        long long ik = i + k;
        char *sk = s[k];
        if (strcmp(sk, "FizzBuzz") == 0) {
            if (ik % 15 != 0) return 0;
        } else if (strcmp(sk, "Fizz") == 0) {
            if (ik % 3 != 0 || ik % 5 == 0) return 0;
        } else if (strcmp(sk, "Buzz") == 0) {
            if (ik % 5 != 0 || ik % 3 == 0) return 0;
        } else {
            long long nk = atoll(sk);
            if (ik != nk) return 0;
            if (ik % 3 == 0 || ik % 5 == 0) return 0;
        }
    }
    return 1;
}

// 주어진 i 값에 대해 FizzBuzz 출력을 계산하는 함수
void FizzBuzz(long long i, char *result) {
    if (i % 15 == 0) strcpy(result, "FizzBuzz");
    else if (i % 3 == 0) strcpy(result, "Fizz");
    else if (i % 5 == 0) strcpy(result, "Buzz");
    else sprintf(result, "%lld", i);
}

int main() {
    char s[3][9];
    int i;
    for (i = 0; i < 3; ++i) {
        scanf("%8s", s[i]);  // 최대 길이가 8인 문자열 입력
    }

    int hasNumber = 0;
    long long i_value = -1;

    for (i = 0; i < 3; ++i) {
        if (isNumber(s[i])) {
            hasNumber = 1;
            long long nk = atoll(s[i]);
            long long i_candidate = nk - i;
            if (i_value == -1) {
                i_value = i_candidate;
            } else if (i_value != i_candidate) {
                // 일관성 없는 경우
                printf("No solution\n");
                return 0;
            }
        }
    }

    if (hasNumber) {
        if (i_value < 1) {
            printf("No solution\n");
            return 0;
        }
        if (isValid(i_value, s)) {
            char result[9];
            FizzBuzz(i_value + 3, result);
            printf("%s\n", result);
            return 0;
        } else {
            printf("No solution\n");
            return 0;
        }
    } else {
        int i_mod15;
        for (i_mod15 = 1; i_mod15 <= 15; ++i_mod15) {
            long long i_candidate = i_mod15;
            if (isValid(i_candidate, s)) {
                char result[9];
                FizzBuzz(i_candidate + 3, result);
                printf("%s\n", result);
                return 0;
            }
        }
        printf("No solution\n");
        return 0;
    }
}
```

위 코드는 표준 라이브러리의 사용을 최소화하여 작성된 C 언어 기반의 프로그램입니다.

- **입력 처리**:
  ```c
  char s[3][9];
  int i;
  for (i = 0; i < 3; ++i) {
      scanf("%8s", s[i]);  // 최대 길이가 8인 문자열 입력
  }
  ```
  세 개의 문자열을 최대 길이 8로 입력받아 2차원 배열 `s`에 저장합니다.

- **숫자인지 확인하는 함수**:
  ```c
  int isNumber(char *s) {
      return !(strcmp(s, "Fizz") == 0 || strcmp(s, "Buzz") == 0 || strcmp(s, "FizzBuzz") == 0);
  }
  ```
  문자열이 `"Fizz"`, `"Buzz"`, `"FizzBuzz"` 중 하나인지 확인하여 숫자인지를 판단합니다.

- **가능한 시작점 계산 및 일관성 확인**:
  ```c
  int hasNumber = 0;
  long long i_value = -1;

  for (i = 0; i < 3; ++i) {
      if (isNumber(s[i])) {
          hasNumber = 1;
          long long nk = atoll(s[i]);
          long long i_candidate = nk - i;
          if (i_value == -1) {
              i_value = i_candidate;
          } else if (i_value != i_candidate) {
              printf("No solution\n");
              return 0;
          }
      }
  }
  ```
  입력된 문자열 중 숫자가 있는 경우 가능한 시작점 `i_value`를 계산하고, 일관성을 확인합니다.

- **시작점 검증 및 다음 출력 계산**:
  ```c
  if (hasNumber) {
      if (i_value < 1) {
          printf("No solution\n");
          return 0;
      }
      if (isValid(i_value, s)) {
          char result[9];
          FizzBuzz(i_value + 3, result);
          printf("%s\n", result);
          return 0;
      } else {
          printf("No solution\n");
          return 0;
      }
  }
  ```
  계산된 시작점이 유효한지 확인하고, 유효하다면 다음 FizzBuzz 출력을 계산하여 출력합니다.

- **숫자가 없는 경우 가능한 시작점 탐색**:
  ```c
  else {
      int i_mod15;
      for (i_mod15 = 1; i_mod15 <= 15; ++i_mod15) {
          long long i_candidate = i_mod15;
          if (isValid(i_candidate, s)) {
              char result[9];
              FizzBuzz(i_candidate + 3, result);
              printf("%s\n", result);
              return 0;
          }
      }
      printf("No solution\n");
      return 0;
  }
  ```
  숫자가 없는 경우 1부터 15까지의 가능한 시작점을 모두 탐색하여 유효한 시작점을 찾습니다.

- **`isValid` 함수**:
  ```c
  int isValid(long long i, char s[3][9]) {
      int k;
      for (k = 0; k < 3; ++k) {
          long long ik = i + k;
          char *sk = s[k];
          if (strcmp(sk, "FizzBuzz") == 0) {
              if (ik % 15 != 0) return 0;
          } else if (strcmp(sk, "Fizz") == 0) {
              if (ik % 3 != 0 || ik % 5 == 0) return 0;
          } else if (strcmp(sk, "Buzz") == 0) {
              if (ik % 5 != 0 || ik % 3 == 0) return 0;
          } else {
              long long nk = atoll(sk);
              if (ik != nk) return 0;
              if (ik % 3 == 0 || ik % 5 == 0) return 0;
          }
      }
      return 1;
  }
  ```
  시작점 `i`에서 입력된 세 개의 문자열이 FizzBuzz 규칙과 일치하는지 확인합니다.

- **`FizzBuzz` 함수**:
  ```c
  void FizzBuzz(long long i, char *result) {
      if (i % 15 == 0) strcpy(result, "FizzBuzz");
      else if (i % 3 == 0) strcpy(result, "Fizz");
      else if (i % 5 == 0) strcpy(result, "Buzz");
      else sprintf(result, "%lld", i);
  }
  ```
  주어진 `i`에 대해 FizzBuzz 출력을 `result`에 저장합니다.

## Python 코드와 설명

```python
s = [input() for _ in range(3)]  # 세 개의 문자열 입력

def is_number(s):
    return s not in ("Fizz", "Buzz", "FizzBuzz")

def is_valid(i, s):
    for k in range(3):
        ik = i + k
        sk = s[k]
        if sk == "FizzBuzz":
            if ik % 15 != 0:
                return False
        elif sk == "Fizz":
            if ik % 3 != 0 or ik % 5 == 0:
                return False
        elif sk == "Buzz":
            if ik % 5 != 0 or ik % 3 == 0:
                return False
        else:
            try:
                nk = int(sk)
                if ik != nk:
                    return False
                if ik % 3 == 0 or ik % 5 == 0:
                    return False
            except ValueError:
                return False
    return True

def fizzbuzz(i):
    if i % 15 == 0:
        return "FizzBuzz"
    elif i % 3 == 0:
        return "Fizz"
    elif i % 5 == 0:
        return "Buzz"
    else:
        return str(i)

has_number = False
i_value = None

for k in range(3):
    if is_number(s[k]):
        has_number = True
        nk = int(s[k])
        i_candidate = nk - k
        if i_value is None:
            i_value = i_candidate
        elif i_value != i_candidate:
            print("No solution")
            exit()

if has_number:
    if i_value < 1:
        print("No solution")
    elif is_valid(i_value, s):
        print(fizzbuzz(i_value + 3))
    else:
        print("No solution")
else:
    for i_candidate in range(1, 16):
        if is_valid(i_candidate, s):
            print(fizzbuzz(i_candidate + 3))
            break
    else:
        print("No solution")
```

위의 Python 코드는 입력된 세 개의 문자열을 기반으로 다음 FizzBuzz 출력을 계산하는 프로그램입니다.

- **입력 처리**:
  ```python
  s = [input() for _ in range(3)]  # 세 개의 문자열 입력
  ```
  세 개의 문자열을 리스트 `s`에 저장합니다.

- **문자열이 숫자인지 확인하는 함수**:
  ```python
  def is_number(s):
      return s not in ("Fizz", "Buzz", "FizzBuzz")
  ```
  문자열이 `"Fizz"`, `"Buzz"`, `"FizzBuzz"` 중 하나가 아니면 숫자로 판단합니다.

- **시작점이 유효한지 확인하는 함수**:
  ```python
  def is_valid(i, s):
      for k in range(3):
          ik = i + k
          sk = s[k]
          if sk == "FizzBuzz":
              if ik % 15 != 0:
                  return False
          elif sk == "Fizz":
              if ik % 3 != 0 or ik % 5 == 0:
                  return False
          elif sk == "Buzz":
              if ik % 5 != 0 or ik % 3 == 0:
                  return False
          else:
              try:
                  nk = int(sk)
                  if ik != nk:
                      return False
                  if ik % 3 == 0 or ik % 5 == 0:
                      return False
              except ValueError:
                  return False
      return True
  ```
  시작점 `i`에서 입력된 세 개의 문자열이 FizzBuzz 규칙과 일치하는지 확인합니다.

- **FizzBuzz 출력 계산 함수**:
  ```python
  def fizzbuzz(i):
      if i % 15 == 0:
          return "FizzBuzz"
      elif i % 3 == 0:
          return "Fizz"
      elif i % 5 == 0:
          return "Buzz"
      else:
          return str(i)
  ```
  주어진 `i`에 대해 FizzBuzz 출력을 반환합니다.

- **가능한 시작점 계산 및 일관성 확인**:
  ```python
  has_number = False
  i_value = None

  for k in range(3):
      if is_number(s[k]):
          has_number = True
          nk = int(s[k])
          i_candidate = nk - k
          if i_value is None:
              i_value = i_candidate
          elif i_value != i_candidate:
              print("No solution")
              exit()
  ```
  입력된 문자열 중 숫자가 있는 경우 가능한 시작점 `i_value`를 계산하고, 일관성을 확인합니다.

- **시작점 검증 및 다음 출력 계산**:
  ```python
  if has_number:
      if i_value < 1:
          print("No solution")
      elif is_valid(i_value, s):
          print(fizzbuzz(i_value + 3))
      else:
          print("No solution")
  ```
  계산된 시작점이 유효한지 확인하고, 유효하다면 다음 FizzBuzz 출력을 계산하여 출력합니다.

- **숫자가 없는 경우 가능한 시작점 탐색**:
  ```python
  else:
      for i_candidate in range(1, 16):
          if is_valid(i_candidate, s):
              print(fizzbuzz(i_candidate + 3))
              break
      else:
          print("No solution")
  ```
  숫자가 없는 경우 1부터 15까지의 가능한 시작점을 모두 탐색하여 유효한 시작점을 찾습니다.

## 결론

이번 문제는 고전적인 FizzBuzz 문제를 응용하여, 주어진 출력값으로부터 원래의 수열을 역추적하고 다음 출력을 예측하는 흥미로운 문제였습니다. 문자열 처리와 수학적인 규칙을 결합하여 문제를 해결할 수 있었으며, 특히 입력된 값이 모두 문자열인 경우 FizzBuzz 패턴의 주기를 활용하는 것이 핵심이었습니다. 이와 같은 문제를 통해 다양한 접근 방식을 연습하고, 문제 해결 능력을 향상시킬 수 있었습니다.