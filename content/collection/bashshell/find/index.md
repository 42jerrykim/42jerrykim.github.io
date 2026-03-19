---
draft: true
title: "[Bash Shell] find - 파일·디렉터리 검색"
description: "리눅스·유닉스에서 이름·타입·날짜·크기 등 조건으로 파일과 디렉터리를 검색하는 find 명령어의 사용법, 주요 옵션(-name, -type, -mtime), 실무 예제와 xargs 조합을 상세히 다룹니다."
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
- find
- 파일검색
- 디렉터리검색
- 검색
- 재귀
- recursive
- glob
- 패턴
- mtime
- type
- exec
- xargs
- Pipeline
image: "wordcloud.png"
---

`find`는 리눅스·유닉스에서 **경로 아래**를 재귀적으로 탐색하며, 이름·타입·수정 시간·크기 등 **조건에 맞는 파일·디렉터리**를 찾아 경로를 출력하는 명령어다. 스크립트·백업·정리 작업에서 필수적으로 사용된다.

## 사용법

```bash
find [경로...] [표현식]
```

- **경로**: 검색을 시작할 디렉터리. 생략 시 현재 디렉터리(`.`)로 간주.
- **표현식**: 검색 조건·동작. 여러 개를 나열하면 AND로 묶인다. `-o`로 OR, `!`로 부정.

## 주요 옵션·표현식

### 검색 범위·순서

| 옵션 | 설명 |
|------|------|
| `-maxdepth N` | 최대 깊이 N까지만 검색 (1이면 해당 디렉터리만) |
| `-mindepth N` | 최소 깊이 N부터 검색 |
| `-depth` | 디렉터리 내용을 먼저, 그 다음 디렉터리 자체 (rm 등과 조합 시 유용) |

### 이름·경로

| 표현식 | 설명 |
|--------|------|
| `-name PATTERN` | 파일명이 PATTERN과 일치 (glob: `*`, `?`, `[]`) |
| `-iname PATTERN` | `-name`과 같으나 대소문자 무시 |
| `-path PATTERN` | 경로 전체가 PATTERN과 일치 |
| `-regex PATTERN` | 경로가 정규식 PATTERN과 일치 |

### 타입

| 표현식 | 설명 |
|--------|------|
| `-type d` | 디렉터리만 |
| `-type f` | 일반 파일만 |
| `-type l` | 심볼릭 링크만 |
| `-type s` | 소켓, `-type p` 파이프 등 |

### 시간

| 표현식 | 설명 |
|--------|------|
| `-mmin N` | 수정이 N분 이내(이전: `-N`, 초과: `+N`) |
| `-mtime N` | 수정이 N일 이내(`-N` 이내, `+N` 초과) |
| `-amin N`, `-atime N` | 접근 시간 기준 |
| `-cmin N`, `-ctime N` | 상태 변경 시간 기준 |

### 크기·기타

| 표현식 | 설명 |
|--------|------|
| `-size N[cwbkMG]` | 크기. `+N` 초과, `-N` 미만. c=바이트, k=KB, M=MB 등 |
| `-empty` | 빈 파일·디렉터리 |
| `-perm MODE` | 권한이 MODE와 일치 |
| `-user NAME`, `-group NAME` | 소유자·그룹 |

### 동작

| 표현식 | 설명 |
|--------|------|
| `-print` | 경로 출력 (기본 동작) |
| `-print0` | 널 문자로 구분 (xargs -0와 조합) |
| `-exec CMD \;` | 매칭마다 CMD 실행. `{}`는 해당 경로로 치환 |
| `-execdir CMD \;` | 해당 디렉터리에서 CMD 실행 |
| `-delete` | 매칭 항목 삭제 |
| `-quit` | 첫 매칭 후 종료 |

## 예시

### 이름으로 검색

```bash
# 현재 디렉터리 아래 .log 파일
find . -name "*.log"

# 대소문자 무시
find /var -iname "*.LOG"

# 이름이 config로 시작하는 파일
find . -name "config*"
```

### 타입·깊이 제한

```bash
# 디렉터리만, 최대 깊이 2
find . -maxdepth 2 -type d

# 현재 디렉터리 직하위 .txt 파일만 (깊이 1)
find . -maxdepth 1 -type f -name "*.txt"
```

### 시간 기준

```bash
# 7일 이내 수정된 파일
find /tmp -type f -mtime -7

# 30일 넘게 수정 안 된 파일
find /var/log -type f -mtime +30

# 1시간 이내 변경된 파일
find . -type f -mmin -60
```

### 크기·빈 파일

```bash
# 100MB 초과 파일
find /home -type f -size +100M

# 빈 디렉터리
find . -type d -empty
```

### exec·삭제

```bash
# 매칭 파일에 chmod 적용
find . -name "*.sh" -exec chmod +x {} \;

# 30일 지난 로그 삭제 (주의해서 사용)
find /var/log -name "*.log" -mtime +30 -delete
```

### print0과 xargs

```bash
# 공백·줄바꿈이 있는 파일명도 안전하게 처리
find . -name "*.txt" -print0 | xargs -0 grep -l "keyword"
```

## 참고

- [GNU find manual](https://www.gnu.org/software/findutils/manual/html_mono/find.html)
- [find (Unix) - Wikipedia](https://en.wikipedia.org/wiki/Find_(Unix))
