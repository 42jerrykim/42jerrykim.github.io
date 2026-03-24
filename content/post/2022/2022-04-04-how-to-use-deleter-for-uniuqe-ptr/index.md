---
title: "[C++] Lambda를 사용한 unique_ptr Custom Deleter 가이드"
description: "C++ unique_ptr에 람다 기반 커스텀 Deleter를 지정해 동적 메모리·C API 리소스를 안전히 해제하는 방법을 다룹니다. Functor·decltype·std::function 등록 방식, 주의사항, 실전 예제를 포함한 150자 요약입니다."
categories:
  - Cpp
date: "2022-04-04T00:00:00Z"
lastmod: "2026-03-16"
image: "wordcloud.png"
tags:
  - C++
  - C
  - Memory
  - 메모리
  - Tutorial
  - 튜토리얼
  - Guide
  - 가이드
  - How-To
  - Tips
  - Reference
  - 참고
  - Implementation
  - 구현
  - Best-Practices
  - Documentation
  - 문서화
  - Technology
  - 기술
  - Education
  - 교육
  - Blog
  - 블로그
  - Web
  - 웹
  - Open-Source
  - 오픈소스
  - Troubleshooting
  - 트러블슈팅
  - Configuration
  - 설정
  - Productivity
  - 생산성
  - Career
  - 커리어
  - Workflow
  - 워크플로우
  - Migration
  - 마이그레이션
  - Comparison
  - 비교
  - Design-Pattern
  - 디자인패턴
  - OOP
  - 객체지향
  - Clean-Code
  - 클린코드
  - Code-Quality
  - 코드품질
  - Error-Handling
  - 에러처리
  - Pitfalls
  - 함정
  - Type-Safety
  - Optimization
  - 최적화
  - Performance
  - 성능
  - Debugging
  - 디버깅
  - Software-Architecture
  - 소프트웨어아키텍처
  - Interface
  - 인터페이스
  - Encapsulation
  - 캡슐화
  - RAII
  - Smart-Pointer
  - unique_ptr
  - Lambda
  - Modern-Cpp
  - Cpp11
  - Git
  - GitHub
  - String
  - HTML
  - Markdown
  - 마크다운
  - Review
  - 리뷰
  - Hardware
  - 하드웨어
  - Beginner
  - Advanced
  - Case-Study
  - Deep-Dive
  - 실습
  - 컴파일러
  - Compiler
  - OS
  - 운영체제
  - 시스템프로그래밍
---

C/C++에서 동적으로 할당한 자원을 해제하지 않으면 메모리 누수나 이중 해제 같은 문제가 발생한다. **`std::unique_ptr`**을 쓰면 스코프를 벗어날 때 자원이 자동으로 해제되므로, 수동 `delete` 실수를 줄일 수 있다. 이 글에서는 **커스텀 Deleter**를 람다로 지정해 `unique_ptr`이 단순 `delete` 말고도 복잡한 해제 로직(배열·C API 등)을 수행하도록 하는 방법을 정리한다.

## 스마트 포인터 개요

스마트 포인터는 **RAII**에 따라 소유한 자원을 소멸 시점에 자동으로 해제하는 래퍼다. C++ 표준 라이브러리에는 다음 세 가지가 있다.

| 타입 | 용도 |
|------|------|
| **unique_ptr** | 단일 소유권. 이동만 가능, 복사 불가. |
| **shared_ptr** | 참조 카운팅 기반 공유 소유권. |
| **weak_ptr** | `shared_ptr` 순환 참조 완화용. |

> C++03의 `auto_ptr`은 C++11에서 deprecated, C++17에서 제거되었다. `unique_ptr`로 대체해야 한다.

아래 다이어그램은 `unique_ptr`이 소유권을 가지는 시점과, 스코프를 벗어날 때 **Deleter가 호출되는 흐름**을 요약한다.

```mermaid
flowchart LR
  subgraph ScopeInner["스코프 내부"]
    CreatePtr["unique_ptr 생성</br>자원 소유"]
    CreatePtr --> ScopeExit["스코프 종료"]
  end
  ScopeExit --> DeleterCall["Deleter 호출</br>기본 delete"]
  DeleterCall --> ResourceFreed["자원 해제 완료"]
```

## unique_ptr과 소유권 이전

`unique_ptr`은 **한 시점에 하나의 인스턴스만** 한 객체를 소유한다. 복사는 불가하고, **이동(`std::move`)** 으로만 소유권을 넘길 수 있다. 이동 후 기존 `unique_ptr`은 빈 상태가 되므로, 이동한 뒤에는 기존 포인터를 역참조하면 안 된다.  
자세한 소유권 이전 관계는 [Microsoft Learn: unique_ptr 인스턴스 만들기 및 사용](https://docs.microsoft.com/ko-kr/cpp/cpp/how-to-create-and-use-unique-ptr-instances) 문서의 다이어그램을 참고하면 좋다.

## Custom Deleter (커스텀 삭제자)

기본적으로 `unique_ptr`은 소멸 시 **`delete`** 한 번으로 포인터를 해제한다. 다음처럼 **다른 방식의 해제**가 필요할 때는 Custom Deleter를 지정한다.

- 멤버로 동적 배열을 가진 구조체: `delete[]` 후 `delete`
- C API로 생성한 핸들: `xxx_destroy()`, `xxx_close()` 등 전용 해제 함수 호출
- 파일 핸들·소켓 등: `fclose`, `close` 등

Deleter는 **함수 포인터**, **함수 객체(Functor)**, **람다**, **`std::function`** 등으로 줄 수 있다. 아래는 람다를 사용한 예이다.

### 클래스 객체 + 추가 자원 해제

```cpp
auto deleter = [](Human* human) {
  delete[] human->name;
  delete human;
};

std::unique_ptr<Human, decltype(deleter)> ptr(new Human, deleter);
```

`ptr`이 스코프를 벗어나 소멸될 때 `deleter`가 호출되며, `human->name`과 `human`이 순서대로 해제된다.

### C API 리소스 (new 없이 생성한 포인터)

`new`로 만든 포인터가 아니라, C API가 반환한 포인터도 Deleter로 감싸면 RAII로 관리할 수 있다.

```cpp
struct tzplatform_context* context = nullptr;
if (tzplatform_context_create(&context) != 0) {
    _ERR("Couldn't create tzplatform context");
    return "";
}

auto deleter = [](tzplatform_context* tc) { tzplatform_context_destroy(tc); };
std::unique_ptr<tzplatform_context, decltype(deleter)> ptr(context, deleter);
```

`context`는 `new`가 아니므로 Deleter에서 `delete`를 호출하면 안 되고, 반드시 `tzplatform_context_destroy()`만 호출해야 한다.

## Deleter를 등록하는 여러 방법

Deleter 타입을 템플릿 인자로 넘기고, 생성 시 Deleter 객체도 함께 넘겨야 한다. 람다를 쓰면 **`decltype(람다)`** 로 타입을 알 수 있다. 아래 표와 예제는 네 가지 등록 방식을 정리한 것이다.

| 방법 | Deleter 타입 | 특징 |
|------|----------------|------|
| Functor(클래스) | `go_de` | 타입 이름이 명시적. `operator()`만 구현하면 됨. |
| 람다 + decltype | `decltype(d)` | 람다를 **두 번째 인자로 반드시 전달**. 생략 시 컴파일 에러. |
| std::function | `std::function<void(go*)>` | 타입이 커지고 인라인 제한이 있을 수 있음. |
| 함수 포인터 | `void(*)(go*)` | 함수 주소만 넘기면 됨. |

```cpp
// 42jerrykim.github.io에서 더 많은 정보를 확인할 수 있다
#include <iostream>
#include <memory>
#include <functional>

using namespace std;

class go {
public:
    go() {}
    ~go() { cout << "go die.\n"; }
};

auto d = [](go* gp) {
    delete gp;
    cout << "deleter done.\n";
};

class go_de {
public:
    void operator()(go* g) { d(g); }
};

int main() {
    {
        unique_ptr<go, go_de> b{ new go{} };  // 1) Functor
    }
    {
        // unique_ptr<go, decltype(d)> b{ new go{} };  // 2) 컴파일 에러: deleter 인자 누락
        unique_ptr<go, decltype(d)> a{ new go{}, d };  // 3) 람다 + decltype: 반드시 d 전달
    }
    {
        unique_ptr<go, function<void(go*)>> a{ new go{}, d };  // 4) std::function
    }
    return 0;
}
```

### 주의사항

- **`std::make_unique`** 는 Custom Deleter를 인자로 받지 않는다. Deleter를 쓰려면 `unique_ptr<T, Deleter>(raw_ptr, deleter)` 형태로 생성해야 한다.
- **람다 + `decltype`** 사용 시, 생성자 두 번째 인자에 **같은 람다(또는 동일 타입의 호출 가능 객체)** 를 꼭 넘겨야 한다. 빠뜨리면 컴파일 에러가 난다.
- Deleter가 **상태를 가진 경우**(캡처가 있는 람다 등)에는 크기·정렬 요구가 달라질 수 있으므로, 타입과 전달 방식을 잘 맞추는 것이 좋다.

## 정리

- `unique_ptr`은 스코프를 벗어날 때 자동으로 자원을 해제하므로, 메모리 누수와 이중 해제 위험을 줄일 수 있다.
- 기본은 `delete` 한 번이므로, **배열(`delete[]`)·C API·파일 등** 다른 해제 방식이 필요하면 **Custom Deleter**를 지정한다.
- Deleter는 **람다 + `decltype`**, **Functor**, **`std::function`**, **함수 포인터** 등으로 등록할 수 있으며, 람다 사용 시에는 생성자에 Deleter 객체를 반드시 함께 넘겨야 한다.

## 참고 문헌

- [방법: unique_ptr 인스턴스 만들기 및 사용](https://docs.microsoft.com/ko-kr/cpp/cpp/how-to-create-and-use-unique-ptr-instances) — Microsoft Learn
- [스마트 포인터(Smart Pointer) 란?](https://dydtjr1128.github.io/cpp/2019/05/10/Cpp-smart-pointer.html) — dydtjr1128's Blog
- [(C++11) std::unique_ptr](https://blog.frec.kr/cpp/modern-cpp-0/) — Frec's Blog
