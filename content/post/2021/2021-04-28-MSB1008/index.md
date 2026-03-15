---
image: "tmp_wordcloud.png"
description: ".NET 환경에서 MSBUILD: error MSB1008(Only one project can be specified) 오류의 주요 원인과 올바른 명령어 형식, /p 옵션 사용 실수, 슬루션 빌드 방법 및 관련 해결책을 150자 분량으로 구체적으로 설명합니다."
categories:
- .NET
date: "2021-04-28T00:00:00Z"
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
tags:
- .NET
- CI-CD
- Python
- Bash
- Shell
- REST
- API
- Stack
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
- Hardware
- 하드웨어
- Cloud
- 클라우드
- Mobile
- 모바일
title: '[.NET] MSB1008 한 프로젝트만 지정 오류 해결'
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
