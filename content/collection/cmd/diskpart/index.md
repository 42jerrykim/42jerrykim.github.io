---
draft: true
title: "[CMD] diskpart - 디스크 파티션 관리"
description: "diskpart 명령어는 Windows CMD에서 디스크 파티션을 생성·삭제·포맷·확장하는 대화형 도구를 실행할 때 사용합니다. 스크립트로 자동화할 수 있으며, 관리자 권한이 필요합니다."
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

diskpart는 Windows 명령 프롬프트(CMD)에서 디스크와 파티션을 관리하는 대화형 도구를 시작할 때 사용하는 명령어이다. 파티션 생성·삭제·포맷·확장, 볼륨 활성화 등이 가능하며, 스크립트 파일을 인수로 넘겨 자동화할 수 있다.

## 사용법

```
diskpart
diskpart /s 스크립트파일
```

실행 후 list disk, select disk n, create partition primary, format, assign 등 하위 명령을 입력한다.

## 주요 하위 명령

- list disk / list volume / list partition: 목록 표시
- select disk n: 디스크 n 선택
- create partition primary [size=n]: 주 파티션 생성
- format fs=ntfs [quick]: 포맷
- assign [letter=x]: 드라이브 문자 할당
- delete partition: 파티션 삭제

## 예시

```
diskpart
list disk
select disk 1
create partition primary size=102400
format fs=ntfs quick
assign letter=E
exit
```

## 주의사항

- 잘못된 디스크·파티션을 선택하면 데이터가 삭제될 수 있다. 반드시 백업 후 진행하고 선택 대상을 확인한다.
- 관리자 권한으로 실행해야 한다.
