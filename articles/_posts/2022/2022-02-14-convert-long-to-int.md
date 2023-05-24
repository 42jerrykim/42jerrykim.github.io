---
title: "[C#] long -> int 변환하기"
category: 
- .NET
- CSharp
tag:
- CSharp
- .NET
- .NET
- Convert
- long
- int
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
---

기본 데이터 형식을 다른 데이터 형식으로 변환하는 방법에 대해서 알아본다.

# 변환하는 방법

[Convert 클래스](https://docs.microsoft.com/ko-kr/dotnet/api/system.convert)을 사용해서 원하는 목표를 이룰 수 있다.

# 예시

```csharp
long vIn = 0;
uint vOut = Convert.ToUInt32(vIn);
```
