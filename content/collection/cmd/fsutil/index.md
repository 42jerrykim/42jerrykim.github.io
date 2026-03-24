---
draft: true
title: "[CMD] fsutil - 파일 시스템 유틸리티"
description: "fsutil 명령어는 Windows CMD에서 NTFS 볼륨과 관련된 다양한 하위 명령(파일, 볼륨, 쿼터, 동작 등)을 실행할 때 사용합니다. 관리자 권한이 필요한 작업이 많습니다."
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

fsutil은 Windows 명령 프롬프트(CMD)에서 파일 시스템(NTFS 등) 관련 작업을 하는 유틸리티이다. 여러 하위 명령(file, volume, quota, behavior, fsinfo 등)으로 파일·볼륨 정보 조회, 동작 설정, 스파스 파일 생성 등을 할 수 있다.

## 사용법

```
fsutil 하위명령 [인수...]
```

## 주요 하위 명령

- **fsutil file**: 파일별 동작(createnew, setvaliddata, queryallocranges 등)
- **fsutil volume**: 볼륨 관련(diskfree, query 등)
- **fsutil fsinfo**: 파일 시스템 정보(ntfsinfo, volumeinfo 등)
- **fsutil behavior**: 동작 설정(query, set 등)
- **fsutil sparse**: 스파스 파일 관리

## 예시

```
fsutil volume diskfree C:
fsutil fsinfo volumeinfo C:
fsutil file createnew bigfile.bin 1048576
fsutil sparse setflag myfile.bin
```

## 주의사항

- 많은 하위 명령이 관리자 권한을 요구한다. 잘못 사용하면 데이터 손상이나 시스템 문제가 될 수 있으므로 문서를 참고한 뒤 사용한다.
- createnew, setvaliddata 등은 디스크 할당·스파스 파일 등 고급 용도에 쓰인다.
