---
image: "tmp_wordcloud.png"
description: "C#에서 long 형식을 int 또는 uint로 변환하는 다양한 방법과 주의할 점을 상세히 설명합니다. Convert 클래스의 활용법, 예제 코드, 데이터 손실 위험성과 안전한 변환 사례를 집중적으로 안내합니다."
date: "2022-02-14T00:00:00Z"
header:
  teaser: https://media.vlpt.us/images/jinuku/post/e62f8f63-4001-46f9-b811-dc6f62f0828e/40cc3e52-745d-48b8-8a09-02c21efc36e5.png
tags:
- CSharp
- .NET
- API
- Networking
- Technology
- Tutorial
- Blog
- 블로그
- 기술
- Web
- 웹
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
- Mobile
- 모바일
- Cloud
- 클라우드
title: '[C#] long -> int 변환하기'
---

기본 데이터 형식을 다른 데이터 형식으로 변환하는 방법에 대해서 알아본다.

## 변환하는 방법

[Convert 클래스](https://docs.microsoft.com/ko-kr/dotnet/api/system.convert)을 사용해서 원하는 목표를 이룰 수 있다.

## 예시

```csharp
long vIn = 0;
uint vOut = Convert.ToUInt32(vIn);
```
