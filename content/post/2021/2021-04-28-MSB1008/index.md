---
image: "tmp_wordcloud.png"
categories:
- .NET
date: "2021-04-28T00:00:00Z"
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
tags:
- .NET
- build
- msbuild
title: '[.NET] MSBUILD : error MSB1008: Only one project can be specified. 해결 방법'

---

```bash
+ dotnet build --no-restore p:DefineConstants=TEST Sample.sln
/usr/share/dotnet-build-tools/sdk/dotnet build --no-restore p:DefineConstants=TEST Sample.sln /nodeReuse:false /p:UseSharedCompilation=false
Microsoft (R) Build Engine version 16.5.0+d4cbfca49 for .NET Core
Copyright (C) Microsoft Corporation. All rights reserved.

MSBUILD : error MSB1008: Only one project can be specified.
Switch: Sample.sln

For switch syntax, type "MSBuild -help"
```
MSBUILD : error MSB1008: Only one project can be specified.
 
```bash
dotnet restore Sample.sln -s /nuget
dotnet build --no-restore Sample.sln 
dotnet clean
dotnet build --no-restore p:DefineConstants="TEST" Sample.sln
 ```
 
 https://stackoverflow.com/questions/3779701/msbuild-error-msb1008-only-one-project-can-be-specified
 https://community.sonarsource.com/t/msbuild-error-msb1008-only-one-project-can-be-specified-switch-sonarscanner-msbuild-exe/26900
 https://pythonq.com/so/visual-studio/33655
 
 ```bash
dotnet restore Sample.sln -s /nuget
dotnet build --no-restore Sample.sln 
dotnet clean
dotnet build --no-restore /p:DefineConstants="TEST" Sample.sln
 ```
