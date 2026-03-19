---
image: "tmp_wordcloud.png"
description: "C# Source Generator는 컴파일 시점에 사용자 코드를 분석(Inspect)하여 새로운 C# 소스 코드를 자동 생성하는 Roslyn 기반 기능입니다. 런타임 리플렉션 대체·AOT 친화·빌드 시점 메타프로그래밍을 가능하게 하며, 본문에서는 Hello World 예제와 .NET Standard 2.0 프로젝트 구성 방법을 단계별로 소개합니다."
date: "2022-04-05T00:00:00Z"
lastmod: "2026-03-16T00:00:00Z"
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
tags:
  - CSharp
  - .NET
  - OOP
  - API
  - String
  - Builder
  - Design-Pattern
  - Blog
  - 블로그
  - Technology
  - 기술
  - Web
  - 웹
  - Tutorial
  - 가이드
  - Review
  - 리뷰
  - Markdown
  - 마크다운
  - Security
  - Guide
  - Productivity
  - 생산성
  - Education
  - 교육
  - Reference
  - 참고
  - Best-Practices
  - Documentation
  - 문서화
  - Open-Source
  - 오픈소스
  - Innovation
  - 혁신
  - Troubleshooting
  - 트러블슈팅
  - Configuration
  - 설정
  - How-To
  - Tips
  - Comparison
  - 비교
  - Career
  - 커리어
  - Workflow
  - 워크플로우
  - Migration
  - 마이그레이션
  - Backend
  - 백엔드
  - Compiler
  - 컴파일러
  - Automation
  - 자동화
  - Performance
  - 성능
  - Code-Quality
  - 코드품질
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - Type-Safety
  - Implementation
  - 구현
  - Testing
  - 테스트
  - Debugging
  - 디버깅
  - Interface
  - 인터페이스
  - Abstraction
  - 추상화
  - Modularity
  - Software-Architecture
  - 소프트웨어아키텍처
  - Maintainability
  - Beginner
  - Deep-Dive
  - 실습
  - Optimization
  - 최적화
  - Error-Handling
  - 에러처리
  - Readability
  - Code-Review
  - 코드리뷰
  - Case-Study
  - Hardware
  - 하드웨어
title: "[C#] Source Generator 개요와 Hello World 예제"
---

## 개요

**C# Source Generator**는 컴파일 시점에 사용자 코드를 검사(Inspect)하고, 그 결과로 새로운 C# 소스 코드를 생성해 같은 컴파일 단위에 넣을 수 있게 해 주는 Roslyn 기반 기능이다. 런타임 리플렉션 없이 타입·구조를 분석하고, 생성된 코드는 기존 코드와 함께 한 번에 컴파일된다.

Source Generator가 제공하는 두 가지 핵심 기능은 다음과 같다.

1. **컴파일 객체 접근**: 현재 컴파일 중인 코드의 Compilation 객체를 얻을 수 있다. Syntax Tree·Semantic Model과 연동해 분석 로직을 작성할 수 있다.
2. **소스 추가**: 컴파일 과정 중에 새 C# 소스 파일을 컴파일에 추가할 수 있다. 즉, 분석 결과를 C# 코드로 만들어 기존 프로젝트에 끼워 넣는 방식이다.

이를 통해 런타임 리플렉션 부담을 줄이고, AOT(Ahead-of-Time) 컴파일·트리밍 친화적인 코드 생성이 가능해진다.

### 동작 흐름

Source Generator는 컴파일 파이프라인 안에서 한 단계로 동작한다. 사용자 소스 → Compilation 구성 → Generator 실행 → 생성 소스 추가 → 최종 컴파일 순서로 이어진다.

```mermaid
flowchart LR
  UserCode["사용자 C# 소스"]
  Compilation["Compilation</br>구성"]
  SourceGen["Source Generator</br>실행"]
  GeneratedSource["생성된 소스</br>추가"]
  FinalComp["최종 컴파일"]

  UserCode --> Compilation
  Compilation --> SourceGen
  SourceGen -->|"AddSource()"| GeneratedSource
  GeneratedSource --> FinalComp
  Compilation -.->|"구성 참조"| SourceGen
```

## 기존 코드 생성·분석 방식과의 비교

Source Generator를 쓰기 전에 흔히 쓰이던 방식은 다음과 같다.

| 방식 | 설명 | 한계 |
|------|------|------|
| **런타임 리플렉션** | 앱 실행 시 타입·멤버를 조회해 동작 결정 | 시작 시 비용, AOT/트리밍에 불리 |
| **MSBuild 작업 연동** | CSC를 여러 번 호출해 중간 결과를 활용 | 빌드 시간 증가, 복잡도 상승 |
| **IL Weaving** | 빌드 후 IL을 수정 | 도구 의존성, 디버깅·호환 이슈 |

Source Generator는 **컴파일 단계**에서만 동작하며, 사용자 소스를 **수정하지 않고** **추가만** 할 수 있다. 그래서 기존 코드 동작이 바뀌지 않으며, 런타임 비용을 줄이면서도 강한 타입 정보를 활용할 수 있다.

## 프로젝트 구성

### 생성기 프로젝트(.NET Standard 2.0)

Source Generator는 .NET Standard 2.0 라이브러리로 작성한다. Roslyn 패키지를 참조하고, `[Generator]`와 `ISourceGenerator`를 사용한다.

**프로젝트 파일 예시**

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

- **TFM**: `netstandard2.0`을 사용한다.
- **패키지**: `Microsoft.CodeAnalysis.CSharp`, `Microsoft.CodeAnalysis.Analyzers`를 PackageReference로 추가하고, 생성기는 실행 시점에 노출되지 않도록 `PrivateAssets="all"` 등을 설정한다.

**Generator 클래스 골격**

Generator는 [ISourceGenerator](https://learn.microsoft.com/en-us/dotnet/api/microsoft.codeanalysis.isourcegenerator)를 구현하고 `[Generator]` 특성을 붙인다.

```csharp
using Microsoft.CodeAnalysis;

namespace SourceGenerator
{
    [Generator]
    public class HelloSourceGenerator : ISourceGenerator
    {
        public void Execute(GeneratorExecutionContext context)
        {
            // 여기서 생성할 소스 내용을 만들고 context.AddSource()로 추가
        }

        public void Initialize(GeneratorInitializationContext context)
        {
            // 필요 시 Syntax/Semantic 모델 캐싱 등 초기화
        }
    }
}
```

- `Execute`: 컴파일 시 호출되며, `context.Compilation`으로 사용자 코드를 분석하고 `context.AddSource()`로 생성 소스를 넣는다.
- `Initialize`: `Execute`가 여러 번 호출될 수 있으므로, 여기서 공통 초기화·캐싱을 할 수 있다.

## Hello World 예제

### 1. HelloWorldGenerator 구현

생성기 프로젝트에 다음 클래스를 추가한다. 컴파일에 포함된 Syntax Tree 목록을 출력하는 `HelloWorldGenerated.HelloWorld.SayHello()` 메서드를 생성한다.

```csharp
// HelloWorldGenerator.cs

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
            var sourceBuilder = new StringBuilder(@"
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

            foreach (SyntaxTree tree in context.Compilation.SyntaxTrees)
            {
                sourceBuilder.AppendLine($@"Console.WriteLine(@"" - {tree.FilePath}"");");
            }

            sourceBuilder.Append(@"
        }
    }
}");

            context.AddSource("helloWorldGenerated", SourceText.From(sourceBuilder.ToString(), Encoding.UTF8));
        }

        public void Initialize(GeneratorInitializationContext context)
        {
            // 이 예제에서는 초기화 없음
        }
    }
}
```

- `context.Compilation.SyntaxTrees`: 현재 컴파일에 포함된 모든 Syntax Tree를 열거한다.
- `context.AddSource(파일명, SourceText)`: 생성된 문자열을 가상의 C# 파일로 컴파일에 추가한다. 파일명은 고유해야 하며, 일반적으로 `.cs`는 붙이지 않아도 된다.

### 2. 생성 코드를 사용하는 콘솔 프로젝트

콘솔 앱 프로젝트에서 위 생성기 프로젝트를 **Analyzer**로 참조한다.

```csharp
// Program.cs

using System;

namespace GeneratedDemo
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Running HelloWorld:\n");
            HelloWorldGenerated.HelloWorld.SayHello();
        }
    }
}
```

빌드 시 Generator가 `HelloWorldGenerated.HelloWorld`를 생성하므로, 위처럼 정적으로 호출할 수 있다.

**콘솔 프로젝트에서 생성기 참조 예시**

- 프로젝트 참조에 `OutputItemType="Analyzer"`, `ReferenceOutputAssembly="false"`를 주면, 생성기 DLL은 실행 파일에 포함되지 않고 Analyzer로만 사용된다.
- 최신 SDK에서는 ProjectReference만 추가해도 Source Generator로 인식되는 경우가 많다. 문제가 있으면 [공식 문서](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/source-generators-overview)의 참조 방식을 따른다.

## 활용 팁

- **즉시 반영**: 생성된 코드는 다음 컴파일부터 사용 가능하다. IDE에서 생성 타입이 안 보이면 한 번 빌드하거나 솔루션을 다시 로드해 보자.
- **재빌드**: Generator 구현을 수정한 뒤에는 전체 재빌드(Clean + Build)를 하는 것이 안전하다.
- **디버깅**: Visual Studio 16.10 이후에는 "Roslyn Component" 디버그 런치로 Generator에 브레이크포인트를 걸 수 있다. 솔루션 탐색기에서 Analyzers 하위에 "Source Generators"로 생성된 파일 목록을 볼 수 있다.

## 참고 문헌

- [Introducing C# Source Generators](https://devblogs.microsoft.com/dotnet/introducing-c-source-generators/) — .NET Blog 공식 소개
- [Source Generators (Microsoft Learn)](https://learn.microsoft.com/en-us/dotnet/csharp/roslyn-sdk/source-generators-overview) — Roslyn SDK 문서
- [Source Generators Cookbook](https://github.com/dotnet/roslyn/blob/main/docs/features/source-generators.cookbook.md) — 권장 패턴·예제
- [Source Generators 샘플](https://github.com/dotnet/roslyn-sdk/tree/main/samples/CSharp/SourceGenerators) — dotnet/roslyn-sdk 저장소
- [C# - Source Generator 소개 (정성태)](https://www.sysnet.pe.kr/2/0/12223) — 한글 실습 가이드
- [New C# Source Generator Samples](https://devblogs.microsoft.com/dotnet/new-c-source-generator-samples/) — CSV·Mustache 등 예제
- [Solving the source generator 'marker attribute' problem (Andrew Lock)](https://andrewlock.net/creating-a-source-generator-part-8-solving-the-source-generator-marker-attribute-problem-part2/) — 마커 특성 배포 전략
