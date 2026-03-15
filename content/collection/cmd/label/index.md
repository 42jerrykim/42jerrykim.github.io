---
draft: true
title: "[CMD] label - 볼륨 레이블 만들기·변경·삭제"
description: "label 명령어는 Windows CMD에서 디스크 볼륨의 이름(레이블)을 만들거나 바꾸거나 삭제할 때 사용합니다. vol로 현재 레이블을 확인할 수 있습니다."
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

label은 Windows 명령 프롬프트(CMD)에서 지정한 드라이브의 볼륨 레이블(이름)을 만들거나 변경하거나 삭제할 때 사용하는 명령어이다. 레이블은 최대 32자(NTFS) 또는 11자(FAT)까지다.

## 사용법

```
label [드라이브:][레이블]
```

## 옵션

- 드라이브만 지정하면 현재 레이블을 보여 주고 새 레이블 입력을 묻는다.
- 레이블을 지정하면 해당 드라이브의 레이블이 바뀐다. 레이블을 비우려면 빈 따옴표 등으로 삭제할 수 있다(프롬프트에서 Enter만 누르면 "레이블을 삭제하시겠습니까?"라고 묻는다).

## 예시

```
label C:
label D: MyData
label E: ""
```

## 주의사항

- 시스템 드라이브나 사용 중인 볼륨도 레이블은 변경 가능하다. 드라이브 문자만 올바르게 지정하면 된다.
- vol 명령으로 현재 레이블을 확인할 수 있다.
