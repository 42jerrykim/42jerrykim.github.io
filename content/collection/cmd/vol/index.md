---
draft: true
title: "[CMD] vol - 볼륨 레이블·일련 번호"
description: "vol 명령어는 Windows CMD에서 지정한 드라이브의 볼륨 레이블과 일련 번호를 표시할 때 사용합니다. 드라이브 문자만 지정하면 해당 드라이브 정보가 출력됩니다."
date: 2025-03-15
lastmod: 2025-03-15
categories: CMD
image: "tmp_wordcloud.png"
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

vol은 Windows 명령 프롬프트(CMD)에서 지정한 드라이브의 볼륨 레이블(이름)과 볼륨 일련 번호를 표시할 때 사용하는 내장 명령어이다. 인수 없이 쓰면 현재 드라이브의 정보가 나온다.

## 사용법

```
vol [드라이브:]
```

## 옵션

- 옵션 없음. 드라이브 문자만 선택적으로 지정한다.

## 예시

```
vol
vol C:
vol D:
```

## 주의사항

- 볼륨 레이블을 변경하려면 label 명령을 사용한다.
- 읽기 전용이거나 네트워크 드라이브에서도 정보는 표시된다.
