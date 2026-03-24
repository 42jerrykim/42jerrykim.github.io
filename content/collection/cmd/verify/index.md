---
draft: true
title: "[CMD] verify - 디스크 쓰기 검증"
description: "verify 명령어는 Windows CMD에서 디스크에 쓰기한 데이터를 자동으로 검증할지 여부를 설정할 때 사용합니다. verify on이면 쓰기 후 읽어서 비교하며, 기본값은 시스템에 따라 다릅니다."
date: 2025-03-15
lastmod: 2025-03-15
categories: CMD
image: "wordcloud.png"
tags:
- Windows
- 윈도우
- Shell
- 셸
- Terminal
- 터미널
- OS
- 운영체제
- Technology
- 기술
- Tutorial
- 튜토리얼
- Guide
- 가이드
- Reference
- 참고
- How-To
- Tips
- Best-Practices
- Documentation
- 문서화
- Beginner
- Advanced
- Automation
- 자동화
- Deployment
- 배포
- Troubleshooting
- 트러블슈팅
- Configuration
- 설정
- Education
- 교육
- Comparison
- 비교
- Productivity
- 생산성
- Workflow
- 워크플로우
- Web
- 웹
- Blog
- 블로그
- Markdown
- 마크다운
- DevOps
- Git
- GitHub
- Linux
- 리눅스
- Monitoring
- 모니터링
- Backend
- 백엔드
- Security
- 보안
- Implementation
- 구현
- Clean-Code
- 클린코드
---

verify는 Windows 명령 프롬프트(CMD)에서 디스크에 데이터를 쓴 뒤 그 데이터를 읽어서 제대로 기록되었는지 검증할지 여부를 설정할 때 사용하는 내장 명령어이다. verify on이면 쓰기 후 검증을 수행하여 안정성을 높일 수 있으나, 쓰기 속도는 느려진다.

## 사용법

```
verify [on | off]
```

## 옵션

- **on**: 쓰기 후 검증 사용
- **off**: 쓰기 후 검증 사용 안 함
- 인수 없이 `verify`만 쓰면 현재 설정(on/off)을 표시한다.

## 예시

```
verify
verify on
verify off
```

## 주의사항

- copy 명령에 /v 옵션이 있으면 해당 복사에만 검증을 한다. verify는 전역 설정이다.
- 현대 NTFS와 디스크에서는 기본적으로 off인 경우가 많다. 중요한 백업 후 검증이 필요하면 별도 읽기 비교나 checksum 도구를 쓰는 경우도 있다.
