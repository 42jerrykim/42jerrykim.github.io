---
draft: true
title: "[Bash Shell] nohup - 터미널 종료 후에도 실행 유지"
description: "리눅스·유닉스에서 로그아웃·터미널 종료 후에도 프로세스를 계속 실행하게 하는 nohup의 사용법, nohup.out, 백그라운드 실행 예제를 다룹니다."
date: 2026-03-15
lastmod: 2026-03-15
categories:
- Bash Shell
tags:
- Bash
- Shell
- Linux
- 리눅스
- Terminal
- 터미널
- Command
- 셸
- Guide
- 가이드
- Tutorial
- 튜토리얼
- Reference
- 참고
- Quick-Reference
- File-System
- Process
- Automation
- 자동화
- Deployment
- 배포
- Error-Handling
- 에러처리
- Troubleshooting
- 트러블슈팅
- Workflow
- 워크플로우
- Best-Practices
- Documentation
- 문서화
- Configuration
- 설정
- Education
- 교육
- Technology
- 기술
- Productivity
- 생산성
- How-To
- Tips
- Beginner
- Advanced
- Comparison
- 비교
- Case-Study
- Deep-Dive
- 실습
- Review
- 리뷰
- Markdown
- 마크다운
- Open-Source
- 오픈소스
- History
- 역사
- nohup
- SIGHUP
- 백그라운드
- background
- 데몬
- disown
- nohup.out
- 장시간실행
- 배치
image: "tmp_wordcloud.png"
---

`nohup`(no hang up)은 **SIGHUP**을 무시하게 해, 터미널이 끊겨도 프로세스가 종료되지 않도록 한다. 장시간 작업·배치를 백그라운드로 돌릴 때 쓴다.

## 사용법

```bash
nohup 명령 [인자...]
```

- 표준 출력은 기본적으로 **nohup.out**으로 리디렉션된다. `nohup 명령 > out.log 2>&1 &`처럼 직접 지정하는 경우가 많다.

## 예시

```bash
# 터미널 닫아도 계속 실행
nohup ./longrun.sh &

# 출력·에러를 파일로
nohup python train.py > train.log 2>&1 &
```

## 참고

- [nohup(1) - Linux man page](https://man7.org/linux/man-pages/man1/nohup.1.html)
