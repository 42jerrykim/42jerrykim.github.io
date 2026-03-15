---
draft: true
title: "[CMD] pushd / popd - 디렉터리 스택"
description: "pushd는 현재 디렉터리를 스택에 저장한 뒤 지정한 경로로 이동하고, popd는 스택에서 복원한 디렉터리로 돌아갈 때 사용합니다. 네트워크 경로를 임시 드라이브로 연결하는 동작도 합니다."
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

pushd와 popd는 Windows 명령 프롬프트(CMD)에서 현재 디렉터리를 스택에 저장했다가 나중에 복원할 때 사용하는 내장 명령어이다. pushd는 현재 경로를 스택에 넣고 지정한 경로로 이동하며, popd는 스택에서 꺼낸 경로로 되돌아간다.

## 사용법

```
pushd [드라이브:][경로]
popd
```

## 옵션

- pushd에 경로를 주면 그 경로로 이동하고, 이전 경로는 스택에 들어간다. 네트워크 경로(\\서버\공유)를 주면 임시 드라이브 문자가 할당될 수 있다.
- popd는 별도 인수 없이 스택의 맨 위에 저장된 디렉터리로 이동한다.

## 예시

```
pushd C:\Projects
pushd \\server\share
popd
popd
```

## 주의사항

- pushd와 popd는 쌍으로 맞추어 사용하는 것이 좋다. popd를 너무 많이 하면 오류가 난다.
- setlocal과 함께 쓰면 setlocal 블록 안에서만 pushd 상태가 유지되고, endlocal 시 스택도 정리된다.
