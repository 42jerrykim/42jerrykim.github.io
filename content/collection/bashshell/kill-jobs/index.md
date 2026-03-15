---
draft: true
title: "[Bash Shell] kill, jobs, fg, bg - 프로세스 종료·작업 제어"
description: "리눅스·유닉스에서 프로세스를 종료하는 kill, 백그라운드·포그라운드 작업을 보는 jobs와 전환하는 fg·bg의 사용법, 시그널·작업 번호 예제를 다룹니다."
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
- Thread
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
- kill
- jobs
- fg
- bg
- signal
- SIGTERM
- SIGKILL
- background
- foreground
image: "tmp_wordcloud.png"
---

`kill`은 **시그널**을 보내 프로세스를 종료·제어하고, `jobs`·`fg`·`bg`는 셸이 관리하는 **작업(Job)** 목록 확인·포그라운드·백그라운드 전환에 쓴다.

---

## kill — 시그널 전송

### 사용법

```bash
kill [-시그널] PID...
kill -l [시그널번호]
```

### 자주 쓰는 시그널

| 시그널 | 번호 | 설명 |
|--------|------|------|
| TERM | 15 | 정상 종료 요청 (기본) |
| KILL | 9 | 강제 종료 |
| HUP | 1 | 재시작 등에 사용 |
| INT | 2 | Ctrl+C와 동일 |

### 예시

```bash
kill 12345
kill -9 12345
kill -TERM 12345
```

---

## jobs — 작업 목록

### 사용법

```bash
jobs [-l]
```

현재 셸의 백그라운드·중지된 작업 목록을 보여준다. `%N`은 작업 번호다.

---

## fg — 포그라운드로

### 사용법

```bash
fg [%작업번호]
```

지정한 작업(또는 현재 작업)을 포그라운드로 가져온다.

---

## bg — 백그라운드로

### 사용법

```bash
bg [%작업번호]
```

중지된 작업을 백그라운드에서 다시 실행한다.

### 예시

```bash
# 장시간 명령 실행 후 Ctrl+Z로 중지
# jobs 로 확인 후
bg %1
fg %1
```

---

## 참고

- [Bash Manual: Job Control](https://www.gnu.org/software/bash/manual/html_node/Job-Control.html)
