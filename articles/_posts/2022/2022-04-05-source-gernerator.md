---
title: "[C#] Source Generators"
category: 
- .NET
- CSharp
tag:
- CSharp
- .NET
- Inspect
- Object
- Syntex
- Semantic
- Model
- Source
- Gernerator
- Source Generators
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
---

Source Generators를 사용하면 C# 개발자가 컴파일되는 사용자 코드를 검사(Inspect)할 수 있다. Source Generators는 컴파일 과정중에 새 C# 코드를 추가 할 수 있다. 이러한 방식으로 컴파일 과정둥에 동작하는 코드가 있다면, 해당 코드는 프로그램을 검사(Inspect)하고 새로운 코드를 생성하여 기존에 있는 코드와 같이 컴파일 되도록 한다.

Source Generators는 개발자에게 새로운 두가지에 기능을 제공한다.

1. 코드에서 컴파일된 객체(compilation object)를 검색(Retrieve) 할 수 있다. 해당 객체는 검사 할 수 있으며 syntax and semantic models과 함께 동작하는 코드를 작성 할 수 있다.
2. 컴파일 과정중에 새로운 객체를 추가 할 수 있다. 다른 말로 표현하면, 컴파일 과정중에 새로운 소스코드를 추가할 수 있다는 얘기이다.


Source Generators는 아래의 그림처럼 동작한다.

|![](https://docs.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/media/source-generators/source-generator-visualization.png#lightbox)|
|:---:|
|Source Generators 동작 다이어그램|

# 일반적인 적용 방법

* 런타임 리플렉션
* Juggling MSBuild tasks.
* Intermediate Language (IL) weaving (본 글에서는 다루지 않는다).

# 예제 코드

## 기본적인 코드

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>netstandard2.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.CodeAnalysis.CSharp" Version="4.0.1" PrivateAssets="all" />
    <PackageReference Include="Microsoft.CodeAnalysis.Analyzers" Version="3.3.3">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>

</Project>
```

`netstandard2.0` TFP을 사용한다. `Microsoft.CodeAnalysis.Analyzers` and `Microsoft.CodeAnalysis.CSharp`을 PackageReference에 추가 한다.

아래와 같이 SourceGenerator을 사용할 클래스를 생성한다. SourceGenerator는 [Microsoft.CodeAnalysis.ISourceGenerator](https://docs.microsoft.com/en-us/dotnet/api/microsoft.codeanalysis.isourcegenerator)을 상속해서 사용 할 수 있다.

```csharp
using Microsoft.CodeAnalysis;

namespace SourceGenerator
{
    [Generator]
    public class HelloSourceGenerator : ISourceGenerator
    {
        public void Execute(GeneratorExecutionContext context)
        {
            // Code generation goes here
        }

        public void Initialize(GeneratorInitializationContext context)
        {
            // No initialization required for this one
        }
    }
}
```
## HelloWorld

### HelloWorldGernerator.cs

생성기 프로젝트를 만들고 아래의 내용을 채워 넣는다.

```csharp
// HelloWorldGernerator.cs

using System.Text;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.Text;

namespace SourceGeneratorSamples
{
    [Generator]
    public class HelloWorldGenerator : ISourceGenerator
    {
        public void Execute(GeneratorExecutionContext context)
        {
            // begin creating the source we'll inject into the users compilation
            StringBuilder sourceBuilder = new StringBuilder(@"
using System;
namespace HelloWorldGenerated
{
    public static class HelloWorld
    {
        public static void SayHello() 
        {
            Console.WriteLine(""Hello from generated code!"");
            Console.WriteLine(""The following syntax trees existed in the compilation that created this program:"");
");

            // using the context, get a list of syntax trees in the users compilation
            IEnumerable<SyntaxTree> syntaxTrees = context.Compilation.SyntaxTrees;

            // add the filepath of each tree to the class we're building
            foreach (SyntaxTree tree in syntaxTrees)
            {
                sourceBuilder.AppendLine($@"Console.WriteLine(@"" - {tree.FilePath}"");");
            }

            // finish creating the source to inject
            sourceBuilder.Append(@"
        }
    }
}");

            // inject the created source into the users compilation
            context.AddSource("helloWorldGenerated", SourceText.From(sourceBuilder.ToString(), Encoding.UTF8));
        }

        public void Initialize(GeneratorInitializationContext context)
        {
            // No initialization required
        }
    }
}
```

`public void Execute(GeneratorExecutionContext context)`에 생성할 코드에 대한 내용을 채운다. `public void Initialize(GeneratorInitializationContext context)`는 syntax and semantic models을 캐싱하여 사용할 수 있다. 이는 `Execute()`가 한 번만 불리는 것이 아니라 여러 번 불릴 수 있기 때문이라고 추측한다.

### UseHelloWorldGernerator

생성된 코드를 사용할 수 있는 프로젝트를 새로 생성한다. 본 글에서는 Console Project를 가정한다.

```csharp
// UseHelloWorldGernerator.cs
namespace GeneratedDemo
{
    public static class UseHelloWorldGenerator
    {
        public static void Run()
        {
            // The static call below is generated at build time, and will list the syntax trees used in the compilation
            HelloWorldGenerated.HelloWorld.SayHello();
        }
    }
}
```

컴파일 과정에서 생성될 `HelloWorldGenerated`를 사용하는 코드를 작성한다.

```csharp
// Program.cs

using System;

namespace GeneratedDemo
{
    class Program
    {
        static void Main(string[] args)
        {
            // Run the various scenarios
            Console.WriteLine("Running HelloWorld:\n");
            UseHelloWorldGenerator.Run();
        }
    }
}
```

# 팁

* 사용하는 코드는 바로 컴파일 되어 동작한다.
* 생성기 코드를 수정하는 경우에는 전체 재빌드를 해주어야 잘 동작한다.

# 참고
* [Introducing C# Source Generators](https://devblogs.microsoft.com/dotnet/introducing-c-source-generators/)
* [Source Generators Cookbook](https://github.com/dotnet/roslyn/blob/main/docs/features/source-generators.cookbook.md)
* [Source Generators](https://docs.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/source-generators-overview)
* [SourceGenerators Sample](https://github.com/dotnet/roslyn-sdk/tree/main/samples/CSharp/SourceGenerators)
* [https://github.com/dotnet/roslyn/blob/main/docs/features/source-generators.md](https://github.com/dotnet/roslyn/blob/main/docs/features/source-generators.md)
* [New C# Source Generator Samples](https://devblogs.microsoft.com/dotnet/new-c-source-generator-samples/)
* [https://gist.github.com/TessenR/ab40df2d6e971a8d6e5c6c6295d85d11](https://gist.github.com/TessenR/ab40df2d6e971a8d6e5c6c6295d85d11)
* [https://www.youtube.com/watch?v=052xutD86uI](https://www.youtube.com/watch?v=052xutD86uI)
* [C# - Source Generator 소개](https://www.sysnet.pe.kr/2/0/12223)
* [Solving the source generator 'marker attribute' problem - Part 2](https://andrewlock.net/creating-a-source-generator-part-8-solving-the-source-generator-marker-attribute-problem-part2/)
