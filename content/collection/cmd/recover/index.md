---
draft: true
title: "[CMD] recover - 불량 디스크에서 파일 복구"
description: "recover 명령어는 Windows CMD에서 불량이거나 결함이 있는 디스크에서 읽을 수 있는 데이터를 복구할 때 사용합니다. 파일 단위로 복구를 시도하며, 손상된 섹터는 건너뜁니다."
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

recover는 Windows 명령 프롬프트(CMD)에서 결함이 있거나 불량 섹터가 있는 디스크에서 지정한 파일을 읽을 수 있는 만큼만 복구할 때 사용하는 명령어이다. 읽을 수 있는 데이터만 복사하고, 손상된 부분은 건너뛴다. **한 번에 하나의 파일만 지정할 수 있다.**

## 사용법

```
recover [드라이브:][경로]파일이름
```

## 옵션

- 옵션 없음. 복구할 파일 하나만 지정한다.

## 예시

```
recover D:\Damage\important.doc
```

## 주의사항

- 복구된 파일은 손상된 섹터 부분이 빈 공간이나 쓰레기로 채워질 수 있다. 중요한 데이터는 전문 복구 도구나 서비스를 고려한다.
- 디스크가 물리적으로 불량이면 반복 사용이 디스크를 더 악화시킬 수 있으므로, 우선 chkdsk /r로 배드 섹터 처리 여부를 확인한 뒤 사용한다.
