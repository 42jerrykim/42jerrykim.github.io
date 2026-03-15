---
draft: true
title: "[Bash Shell] scp - SSH로 파일·디렉터리 복사"
description: "리눅스·유닉스에서 SSH를 이용해 로컬↔원격 간 파일·디렉터리를 복사하는 scp의 사용법, 옵션과 sftp·rsync와의 차이를 다룹니다."
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
- scp
- 복사
- 전송
- SSH
- 원격
- remote
- Security
- 보안
- Networking
- 네트워킹
- rsync
- sftp
image: "tmp_wordcloud.png"
---

`scp`(secure copy)는 **SSH**를 사용해 **로컬↔원격** 간에 파일·디렉터리를 복사한다. 인증·포트는 ssh와 동일하게 쓰인다.

## 사용법

```bash
# 원격 → 로컬
scp [옵션] [사용자@]호스트:원격경로 로컬경로

# 로컬 → 원격
scp [옵션] 로컬경로 [사용자@]호스트:원격경로
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-r` | 디렉터리 재귀 복사 |
| `-i FILE` | 비밀키 파일 |
| `-P PORT` | 포트 (ssh는 -p, scp는 -P) |

## 예시

```bash
# 원격 파일을 로컬로
scp user@host:/path/file.txt ./

# 로컬 파일을 원격으로
scp ./file.txt user@host:/path/

# 디렉터리 전체
scp -r user@host:/path/dir ./
```

## 참고

- [scp(1) - Linux man page](https://man7.org/linux/man-pages/man1/scp.1.html)
- 대용량·동기화에는 **rsync** over SSH(`rsync -avz -e ssh ...`)가 더 유리한 경우가 많다.
