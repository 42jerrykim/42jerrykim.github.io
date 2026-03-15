---
draft: true
title: "[Bash Shell] cd와 pwd - 디렉터리 이동·현재 경로"
description: "리눅스·유닉스 셸에서 작업 디렉터리를 바꾸는 cd와 현재 디렉터리 경로를 출력하는 pwd의 사용법, 옵션, 홈·이전 디렉터리 등 실무 예제를 상세히 다룹니다."
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
- cd
- pwd
- 디렉터리
- 경로
- 작업디렉터리
- current-directory
- 홈디렉터리
- 심볼릭링크
- PWD
- OLDPWD
image: "tmp_wordcloud.png"
---

`cd`(change directory)는 **작업 디렉터리**를 바꾸는 셸 내장 명령이고, `pwd`(print working directory)는 **현재 작업 디렉터리의 절대 경로**를 출력한다. 스크립트·일상 작업에서 가장 자주 쓰는 조합이다.

---

## pwd — 현재 경로 출력

### 사용법

```bash
pwd [옵션]
```

현재 셸이 있는 디렉터리의 절대 경로를 한 줄로 출력한다.

### 옵션

| 옵션 | 설명 |
|------|------|
| `-L`, `--logical` | 심볼릭 링크를 따라가지 않고 논리적 경로(기본 동작) |
| `-P`, `--physical` | 심볼릭 링크를 따라가 실제 물리 경로 출력 |

### 예시

```bash
# 현재 경로 확인
pwd
# 예: /home/user/project

# 스크립트에서 현재 디렉터리 기준 경로 잡을 때
SCRIPT_DIR=$(pwd)
```

---

## cd — 디렉터리 이동

### 사용법

```bash
cd [-L|-P] [디렉터리]
```

**디렉터리**로 작업 디렉터리를 변경한다. 인자를 생략하면 **홈 디렉터리**(`$HOME`)로 이동한다.

### 경로 지정

| 대상 | 예시 |
|------|------|
| 절대 경로 | `cd /var/log` |
| 상대 경로 | `cd src/utils`, `cd ..` |
| 홈 디렉터리 | `cd`, `cd ~` |
| 다른 사용자 홈 | `cd ~otheruser` (권한 있을 때) |
| 이전 디렉터리 | `cd -` |

### 옵션

| 옵션 | 설명 |
|------|------|
| `-L` | 심볼릭 링크를 따라감(기본) |
| `-P` | 심볼릭 링크를 따라가지 않고 실제 경로로 이동 |

### 예시

```bash
# 홈으로 이동
cd
cd ~

# 절대 경로
cd /tmp

# 상대: 한 단계 위
cd ..

# 상대: 하위 디렉터리
cd project/src

# 이전 디렉터리로 돌아가기 (OLDPWD)
cd -

# 스크립트에서 스크립트 위치로 이동할 때 (일반적으로 스크립트 경로 기준으로 처리)
cd "$(dirname "$0")"
```

### 셸 변수

- **PWD**: 현재 작업 디렉터리(절대 경로). `cd` 시 셸이 갱신한다.
- **OLDPWD**: 직전 작업 디렉터리. `cd -`가 이 값을 사용한다.

---

## 참고

- [Bash Manual: Bourne Shell Builtins (cd, pwd)](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html)
