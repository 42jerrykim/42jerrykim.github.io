---
draft: true
title: "[CMD] bcdboot - 부팅 구성 데이터 복사"
description: "bcdboot 명령어는 Windows CMD에서 부팅에 필요한 파일을 시스템 파티션에 복사하고 BCD(부팅 구성 데이터) 저장소를 만들거나 수정할 때 사용합니다. 복구·부팅 복구 시 관리자가 사용합니다."
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

bcdboot는 Windows 명령 프롬프트(CMD)에서 Windows 부팅에 필요한 파일을 지정한 파티션에 복사하고, BCD(Boot Configuration Data) 저장소를 생성·수정할 때 사용하는 도구이다. 복구 환경이나 설치 미디어에서 부팅을 복구할 때 관리자가 사용한다.

## 사용법

```
bcdboot 원본Windows경로 [/l 로케일] [/s 볼륨문자:] [/v] [/m [OS로더GUID]]
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `/s 볼륨문자:` | 부팅 파일을 넣을 시스템 파티션(드라이브 문자) |
| `/l 로케일` | 로케일(예: ko-KR, en-US) |
| `/v` | 자세한 로그 |
| `/m` | 기존 부팅 로더와 병합 |

## 예시

```
bcdboot C:\Windows /s S:
bcdboot D:\Windows /s C: /l ko-KR
```

## 주의사항

- 잘못된 파티션에 적용하면 부팅이 깨질 수 있다. 복구·설치 문서를 참고하고, 필요 시 백업 후 진행한다. 관리자 권한이 필요하다.
