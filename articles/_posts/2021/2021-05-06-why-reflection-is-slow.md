---
title: "[C#] 왜 리플렉션은 느린가?"
categories: 
  - .NET
tags: 
  - .NET
  - CSharp
  - Reflection
  - 리플렉션
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
---

# Reflection이 느린 이유

* [Why is reflection slow?](https://mattwarren.org/2016/12/14/Why-is-Reflection-slow/) 글 참고 하여 작성함

## 배경

* [CLR Type System Design Goals](https://github.com/dotnet/coreclr/blob/32f0f9721afb584b4a14d69135bea7ddc129f755/Documentation/botr/type-system.md#design-goals-and-non-goals)
    * Goals
        * **Accessing information needed at runtime from executing (non-reflection) code is very fast.**
    * Non-Goals
        * **All uses of reflection are fast.**
* [EEClass](https://github.com/dotnet/coreclr/blob/32f0f9721afb584b4a14d69135bea7ddc129f755/Documentation/botr/type-loader.md#key-data-structures)
    * MethodTable data are split into “hot” and “cold” structures to improve working set and cache utilization. MethodTable itself is meant to only store “hot” data that are needed in program steady state. **EEClass stores “cold” data that are typically only needed by type loading, JITing or reflection.** Each MethodTable points to one EEClass.

## 어떤 동작때문에 느린것인가?

* Fetching the Method information
* Argument Validation and Error Handling
* Security Checks

## Reflection에는 어느정도의 비용이 들어 가는가?

### Reading a Property (‘Get’)

|Method|Mean|StdErr|Scaled|Bytes Allocated/Op|
|-|-:|-:|-:|-:|
|GetViaProperty|0.2159 ns|0.0047 ns|1.00|0.00|
|GetViaReflection|197.9258 ns|0.2704 ns|923.08|0.01|

### Writing a Property (‘Set’)

|Method|Mean|StdErr|Scaled|Bytes Allocated/Op|
|---|---:|---:|---:|---:|
|SetViaProperty|1.4043 ns|0.0200 ns|6.55|0.00|
|SetViaReflection|287.1039 ns|0.3288 ns|1,338.99|115.63|