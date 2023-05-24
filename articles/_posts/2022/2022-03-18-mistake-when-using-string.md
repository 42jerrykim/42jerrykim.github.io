---
title: "[C#] string 객체 사용에서 흔히 하는 실수 "
category:
  - .NET
  - CSharp
tag:
  - CSharp
  - .NET
  - GarvageCollection
  - Programming
  - String
  - 실수
  - 개발자
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
---

한 메서드 안의 로컬 변수들은 그 메서드가 끝날 때 해제되게 된다. Value 타입의 변수는 함수 리턴과 동시에 스택에서 해제되고, Reference 타입의 변수는 GC (Garbage Collector)에 의해 힙상에서 자동 해제되게 된다. 프로그래머들이 흔히 범하는 실수중의 하나는 레퍼런스 타입의 객체를 불필요하게 너무 많이 만드는 것이다.

# 문제 상황

예를 들어, 아래 예제는 루프를 돌며 string 객체를 계속 N개 만큼 새로 생성하고 있다.

```csharp
public string Get1ToN_Bad(int n)
{
   string s = "";
   for (int i = 1; i <= n; i++)
   {
      s += i.ToString() + ".";
   }
   return s;
}
```

string 객체는 한번 생성자를 통해 생성되면, 내부에 있는 그 값을 변경할 수 없다. 따라서 새로운 값이 동일 변수에 할당되면 이는 내부적으로 새로운 string 객체를 만들고 새로운 값을 할당한 후 동일 변수에 치환하게 된다. 새 string 객체 할당으로 예전 string 객체는 불필요하게 되어 GC가 나중에 해제하게 된다. 만약 위의 함수에서 N의 값이 작으면 큰 부담이 없겠지만, 만약 백만, 천만등 으로 커진다면 성능에 문제를 가져올 수 있다.

# 해결 방법

그렇다면 이런 문제를 어떻게 해결할 수 있을까? 하나의 방식으로 아래와 같이 객체를 새로 할당하지 않고 데이타를 변경할 수 있는 StringBuilder를 사용하는 것이다. 물론 StringBuilder도 내부적으로 버퍼가 모자라면 기존 버퍼의 2개에 해당하는 새 버퍼를 할당하고 여기에 데이타를 복제하게 된다. 하지만 해당 StringBuilder 객체를 해제하고 새로 객체를 생성하는 것은 아니며, GC가 수많은 옛 해제 객체들을 해제해야 하는 부담은 없게 된다.

```csharp
public string Get1ToN_Good(int n)
{
    StringBuilder sb = new StringBuilder();
    for (int i = 1; i <= n; i++)
    {
        sb.Append(i.ToString() + ",");
    }
    return sb.ToString();
}
```

또한, 성능향상을 위해 미리 버퍼를 크게 할당하도록 capacity를 StringBuilder 생성시 지정할 수도 있다.

> 루프를 사용할 때는 항상 그 안에 불필요하게 레퍼런스 객체를 생성/소멸하지는 않는 확인해야 한다.

# 참고

* [string 객체 사용에서 흔히 하는 실수](https://www.csharpstudy.com/Mistake/Article/3)