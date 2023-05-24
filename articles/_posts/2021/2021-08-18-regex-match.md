---
title: "[Regex] C#에서 Regex로 검색한 결과를 재사용하는 방법"
categories:
  - Regex
tags:
  - Regex
  - CSharp
  - match
  - Lamda
---

문자열에서 내가 원하는것을 검색하고 변경하고 삭제하는 작업을 하는데 있어서 Regex는 매우 좋은 방법이다. 본 글에서는 Regex에서 검색된 결과를 재사용하는 방법에 대해서 알아 본다.

``` { id:'Outsider', sex:"23" } ```가 있을때 쌍따옴표로 감싸진 "23"을 23으로 변경하는 방법을 예시를 들어서 살펴 보자.

# match와 람다 사용

``` Regex.Replace() ```를 사용해서 정규식을 이용해서 "23"을 검색하면 검색의 결과가 ``` match ```로 전달된다 
이때 람다를 사용해서 ```match```를 재사용하여 변경을 할 수 있다.

## Sample code

```csharp
string str = "{ id:'Outsider', sex:\"23\" }";
Console.WriteLine(str);
str = Regex.Replace(str, "\"[0-9]+\"", match => match.Value.Replace("\"", "")); // 
Console.WriteLine(str);
```

## Sample code의 출력 결과

``` json
{ id:'Outsider', sex:"23" }
{ id:'Outsider', sex:23 }
```

# 여담

IDE에서 Regex를 테스트 하는것는 빌드 시간이 있어서 살짝 딜레이가 있다. 온라인에서 실시간으로 확인 할 수 있는 사이트가 있으니 [regexr.com](https://regexr.com/)을 활용하도록 하자. 주의 할것은 사이트에서 작업한 내용을 코드에서 사용할때는 ```"```, ```\```와 같은 Escape 문자를 잘 처리해야 하는것만 명심하자.