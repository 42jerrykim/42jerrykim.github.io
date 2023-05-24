---
title: "[C/C++] Lamda를 사용해서 unique_ptr의 자원을 자동으로 해제하기"
cagegory: Cpp
tag:
- Cpp
- Pointer
- Smart pointer
- unique_ptr
- shared_ptr
- weak_ptr
- Lamda
---

C/C++언어를 사용하다 보면 동적으로 할당한 자원을 해제 하지 않이서 문제가 발생하는 경우가 많다. 이럴때 `unique_ptr`을 사용하면 함수에서 빠져나갈때 자원을 자동으로 해제 할 수 있도록 만들수 있다.

# 스마트 포인터

우선은 스마트 포인터에서 대해서 알아 보자

스마트 포인터에는 크게 다음 3가지의 포인터가 존재한다.

* unique_ptr
* shared_ptr
* weak_ptr

> C++03의 `auto_ptr`은 `unique_ptr`을 만들려던 시도의 실패작이므로 사용해선 안된다.

|![](https://docs.microsoft.com/ko-kr/cpp/cpp/media/unique_ptr.png?view=msvc-170)|
|:---:|
|두 unique_ptr 인스턴스 사이의 소유권 이전 관계도|

# Custom Deleter (커스텀 삭제자)

`unique_ptr`이 소유하던 포인터를 소멸시킬 때, 그 객체를 `delete` 하는 방식으로 소멸시킨다. 다른 방식의 소멸 구현이 필요할 때는 그 객체만을 위한 Deleter를 만들어 지정할 수 있다. Custom Deleter 는 Functor가 될 수도 있고, 아래 예제와 같이 Lambda 함수가 될 수도 있다.

```cpp
auto deleter = [](Human* human)
{
  delete[] human->name;
  delete human;
}

// Deleter를 지정한다.
std::unique_ptr<Human, decltype(deleter)> ptr(new Human, deleter);
```
( 물론 함수 포인터도 가능하며 std::function도 사용 가능하다. )

`ptr`이 해제 되는 시점에 `deleter`가 호출되면서 `human`에 대한 자원을 해제 한다.

다음은 class가 아닌 객체에 대해서 `std::unique_ptr`을 지정하는 방법이다.

```cpp
// 클래스가 아닌 경우에 deletor를 지정 하는 방법
struct tzplatform_context* context = nullptr;
if (tzplatform_context_create(&context))
{
    _ERR("Couldn't create tzplatform context");
    return "";
}

auto deleter = [](tzplatform_context* tc) { tzplatform_context_destroy(tc); };
std::unique_ptr<tzplatform_context, decltype(deleter)> ptr(context, deleter); // context에 new 없이 그냥 사용한다.
```

# Deleter를 등록하는 여러 방법

```cpp
#include <iostream>
#include <cstdlib>
#include <memory>
#include <string>
#include <functional>

using namespace std;

class go
{
public:
    go() {}
    ~go()
    {
        cout << "go die.\n";
    }
};

auto d = [](go * gp)
{
    delete gp;
    cout << "deletor done.\n";
};

class go_de
{
public:
    void operator() (go* g)
    {
        d (g);
    }
};

int main()
{
    {
        unique_ptr<go, go_de> b{ new go{} };//1
    }
    {
        //unique_ptr<go, decltype(d)> b{ new go{}}; complie error //2
        unique_ptr<go, decltype(d)> a{ new go{}, d };//3
    }
    {
        unique_ptr<go, function<void(go*)>> a{ new go{}, d };//4
        //i.e. unique_ptr<go, function<void(go*)>> a{ new go{}, [](go* gp){ delete gp; cout << "deletor done.\n"; }};
    }
    return 0;
}
```

# 참고

* [방법: unique_ptr 인스턴스 만들기 및 사용](https://docs.microsoft.com/ko-kr/cpp/cpp/how-to-create-and-use-unique-ptr-instances)
* [스마트 포인터(Smart Pointer) 란?](https://dydtjr1128.github.io/cpp/2019/05/10/Cpp-smart-pointer.html)
* [(C++11) std::unique_ptr](https://blog.frec.kr/cpp/modern-cpp-0/)
* [C++ Replaces Deleter of unique_ptr with lambda](https://programmer.group/c-replaces-deleter-of-unique_ptr-with-lambda.html)
