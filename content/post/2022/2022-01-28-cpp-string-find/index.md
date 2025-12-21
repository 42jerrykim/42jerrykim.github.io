---
image: "tmp_wordcloud.png"
description: "C++의 std::string::find 함수를 활용하여 문자열 내에서 특정 서브스트링 또는 문자가 존재하는지 효과적으로 찾는 방법과 다양한 함수 원형, 사용 예시, 반환값, 실전 코드 사례를 포함해 초보자도 쉽게 이해할 수 있도록 설명합니다."
categories:
- Cpp
date: "2022-01-28T00:00:00Z"
tag:
- Cpp
- string
- find
- 문자열
- 검색
title: '[C/C++] 문자열에서 특정 문자열이 있는지 찾는 방법'
---

std::string::find를 사용하여 문자열에서 특정 문자열이 있는지 찾는 방법

## 함수 원형

```cpp
size_t find (const string& str, size_t pos = 0) const;
size_t find (const char* s, size_t pos = 0) const;
size_t find (const char* s, size_t pos, size_t n) const;
size_t find (char c, size_t pos = 0) const;
```

## 인자에 대한 설명

* str : 찾고자 하는 문자열
* pos : str을 pos 위치부터 찾기 시작합니다. ex) pos=3이면 인덱스 3부터 찾아 나감
* s : 캐릭터형의 배열을 가리키는 포인터
* n : 연속으로 일치해야 하는 최소 길이
* c : 찾고자 하는 캐릭터(배열이 아니라 문자 하나)

## Return 값

첫 번째로 일치하는 문자의 위치를 return 해 줍니다.
일치하는 위치를 찾지 못한 경우 string::npos를 return합니다.

## 예시
### Sample Code

```cpp
#include <iostream>
#include <string>

using namespace std;

int main()
{
    string s1 = "hello! C world";
    string s2 = "world";

    ssize_t pos = s1.find(s2);
    if (pos != string::npos) {
        cout << "found!" << '\n';
        cout << pos << endl;
    }
}
```

### 결과

```cpp
found!
9
```
