---
draft: true
title: "[Bash Shell] top - 실시간 프로세스·리소스 모니터링"
description: "리눅스에서 CPU·메모리 사용량과 프로세스 목록을 실시간으로 보여주는 top의 사용법, 정렬·필터·키보드 단축키와 실무 활용을 다룹니다."
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
- top
- 모니터링
- Monitoring
- CPU
- 메모리
- Memory
- 프로세스
- 시스템
- 리소스
- 실시간
- Performance
- 성능
image: "wordcloud.png"
---

`top`은 **실시간**으로 시스템 요약(CPU, 메모리)과 **프로세스 목록**을 보여준다. 정렬·필터로 부하 원인을 찾을 때 쓴다.

## 사용법

```bash
top [옵션]
```

## 자주 쓰는 옵션

| 옵션 | 설명 |
|------|------|
| `-d 초` | 갱신 간격 |
| `-p PID` | 특정 PID만 |
| `-u 사용자` | 특정 사용자 프로세스만 |
| `-n N` | N번 갱신 후 종료 (배치 모드) |

## 실행 중 단축키

| 키 | 동작 |
|----|------|
| P | CPU 사용률 순 정렬 |
| M | 메모리 사용률 순 정렬 |
| k | 프로세스에 시그널 보내기 (kill) |
| q | 종료 |
| 1 | CPU 코어별 표시 |

## 참고

- [top(1) - Linux man page](https://man7.org/linux/man-pages/man1/top.1.html)
