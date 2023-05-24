---
title: "[.NET] .NET 7 Preview 2 소개 - 더 새로운 경험"
category:
  - .NET
tag:
  - CSharp
  - .NET
  - GarvageCollection
  - Programming
  - NativeAOT
  - RegEx
  - dotnet new
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
# last_modified_at: 2022-01-16
---

새롭게 선보인 .NET 7 Preview 2에는 아래와 같은 기능이 소개 되었다.

* RegEx 소스 생성기(RegEx source generators)
* NativeAOT를 실험 상태에서 벗어나 개발 Mainline으로 변경
* ```dotnet new``` CLI 관련된 중요 업데이트

# Regex Source Generator

런타임에 이 엔진을 빌드하는 오버헤드 없이 특정 패턴에 최적화된 특수 Regex 엔진을 사용하여 얻을 수 있는 모든 큰 이점을 누리고 싶었던 적이 있습니까?

Preview 1에 포함된 새로운 Regex Source Generator를 발표하게 되어 기쁩니다. 시작 비용 없이 컴파일된 엔진의 모든 성능 이점을 제공하며, 훌륭한 디버깅 경험을 제공하고 트리밍과 같은 추가 이점이 있습니다. -친숙한. 패턴이 컴파일 타임에 알려지면 새로운 정규식 소스 생성기가 가야 할 길입니다.

사용을 시작하려면 포함하는 유형을 부분 유형으로 바꾸고 최적화된 Regex 개체를 반환할 RegexGenerator 속성을 사용하여 새 부분 메서드를 선언하기만 하면 됩니다. 소스 생성기는 해당 메소드의 구현을 채우고 패턴이나 전달한 추가 옵션을 변경할 때 자동으로 업데이트됩니다. 다음은 예입니다.

## Before

```csharp
public class Foo
{
  public Regex regex = new Regex(@"abc|def", RegexOptions.IgnoreCase);

  public bool Bar(string input)
  {
    bool isMatch = regex.IsMatch(input);
    // ..
  }
}
```

## After

```csharp
public partial class Foo  // <-- Make the class a partial class
{
  [RegexGenerator(@"abc|def", RegexOptions.IgnoreCase)] // <-- Add the RegexGenerator attribute and pass in your pattern and options
  public static partial Regex MyRegex(); //  <-- Declare the partial method, which will be implemented by the source generator

  public bool Bar(string input)
  {
    bool isMatch = MyRegex().IsMatch(input); // <-- Use the generated engine by invoking the partial method.
    // ..
  }
}
```

# NativeAOT Update

NativeAOT를 실험 상태에서 벗어나 개발 .NET 7에 포함

[.NET Runtime - Native AOT](https://github.com/dotnet/runtimelab/tree/feature/NativeAOT)에서 내용을 확인 할 수 있다.

# 참고

* [Announcing .NET 7 Preview 2 – The New, ‘New’ Experience](https://devblogs.microsoft.com/dotnet/announcing-dotnet-7-preview-2/)
* [.NET 7 Inches Closer to NativeAOT in Preview 2](https://visualstudiomagazine.com/articles/2022/03/17/net-7-preview-2.aspx?m=1)
* [.NET Runtime - Native AOT](https://github.com/dotnet/runtimelab/tree/feature/NativeAOT)