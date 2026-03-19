---
draft: true
title: "[CMD] bcdedit - 부팅 구성 데이터 편집"
description: "bcdedit 명령어는 Windows CMD에서 BCD(부팅 구성 데이터) 저장소의 항목을 보거나 수정할 때 사용합니다. 부팅 메뉴, 기본 OS, 타임아웃 등 부팅 동작을 변경할 수 있으며 관리자 권한이 필요합니다."
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

bcdedit은 Windows 명령 프롬프트(CMD)에서 BCD(Boot Configuration Data) 저장소를 조회·편집할 때 사용하는 도구이다. 부팅 메뉴 항목 추가·삭제, 기본 OS 변경, 타임아웃 설정, 디버그 옵션 등이 가능하다. 관리자 권한이 필요하다.

## 사용법

```
bcdedit /명령 [인수]
```

## 주요 명령

- `/enum`: 항목 나열(현재, all, firmware 등)
- `/set`: 항목의 속성 설정
- `/delete`: 항목 또는 속성 삭제
- `/copy`: 항목 복사
- `/create`: 새 항목 생성
- `/default`: 기본 부팅 항목 지정
- `/timeout 초`: 부팅 메뉴 타임아웃(초)

## 예시

```
bcdedit /enum
bcdedit /default {current}
bcdedit /timeout 10
bcdedit /set {current} description "My Windows"
```

## 주의사항

- GUID를 잘못 지정하면 부팅이 안 될 수 있다. 변경 전에 `bcdedit /enum`으로 현재 구성을 확인하고, 복구 방법(설치 미디어 등)을 준비한 뒤 진행한다.
