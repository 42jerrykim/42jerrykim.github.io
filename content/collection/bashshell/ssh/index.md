---
draft: true
title: "[Bash Shell] ssh - 원격 접속·원격 명령 실행"
description: "리눅스·유닉스에서 SSH로 원격 호스트에 로그인하거나 원격에서 명령을 실행하는 방법, 키 인증·옵션·설정 파일을 다룹니다."
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
- ssh
- 원격
- remote
- SSH
- 키인증
- Security
- 보안
- Networking
- 네트워킹
image: "tmp_wordcloud.png"
---

`ssh`(Secure Shell)는 **암호화된 채널**로 원격 호스트에 로그인하거나, 원격에서 **명령 한 줄**을 실행할 때 쓴다.

## 사용법

```bash
ssh [옵션] [사용자@]호스트 [명령]
```

- **명령**을 주면 셸 로그인 없이 그 명령만 실행하고 종료한다.

## 자주 쓰는 옵션

| 옵션 | 설명 |
|------|------|
| `-i FILE` | 비밀키 파일 (기본: ~/.ssh/id_rsa 등) |
| `-p PORT` | 포트 지정 (기본 22) |
| `-o 옵션` | 설정 오버라이드 (예: StrictHostKeyChecking=no, 비권장) |
| `-N` | 원격 명령 실행 없이 터널만 (포트 포워딩 시) |
| `-L`, `-R` | 로컬·리모트 포트 포워딩 |

## 키 인증

- 비밀번호 대신 **공개키**로 인증: `ssh-keygen`으로 키 쌍 생성 후, 공개키를 원격 `~/.ssh/authorized_keys`에 넣는다.
- `ssh-copy-id user@host`로 공개키를 한 번에 복사할 수 있다.

## 설정 파일

- `~/.ssh/config`: 호스트별 사용자·키·포트 등 지정.

## 예시

```bash
ssh user@example.com
ssh -i ~/.ssh/mykey user@example.com
ssh user@example.com "ls /tmp"
```

## 참고

- [OpenSSH manual](https://www.openssh.com/manual.html)
