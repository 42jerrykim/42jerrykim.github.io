---
draft: true
title: "[CMD] goto - 배치 파일에서 레이블로 이동"
description: "goto 명령어는 Windows CMD 배치 파일에서 지정한 레이블로 실행 위치를 옮길 때 사용합니다. 조건 분기, 서브루틴 대체, 무한 루프 방지 방법을 정리합니다."
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

goto는 Windows 명령 프롬프트(CMD) 배치 파일에서 지정한 레이블(:이름)이 있는 줄로 실행을 점프할 때 사용하는 내장 명령어이다. 조건 분기나 단순 반복을 구현할 때 쓴다.

## 사용법

```
goto 레이블
```

레이블은 한 줄에 `:레이블` 형태로 쓴다. 레이블 이름만 쓰고, 드라이브·경로·콜론 하나는 허용되지 않는다.

## 옵션

- 옵션 없음. 레이블 이름은 공백 없이 한 단어로 한다.

## 예시

```
goto end
:process
echo Processing...
goto end
:end
echo Done.
```

## 주의사항

- 존재하지 않는 레이블로 goto하면 배치가 종료된다.
- 레이블은 실행 흐름상 그 아래로 떨어지지 않게 하려면 레이블 다음에 바로 다른 goto나 exit를 두는 것이 좋다.
- 복잡한 제어 흐름은 call과 서브루틴 레이블을 쓰는 편이 읽기 쉽다.
