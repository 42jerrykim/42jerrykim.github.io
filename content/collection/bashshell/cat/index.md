---
draft: true
title: "[Bash Shell] cat, head, tail - 파일 내용 보기"
description: "리눅스·유닉스에서 파일 내용을 출력하는 cat, head, tail 명령어의 사용법과 옵션을 다룹니다. 전체 출력·앞뒤 N줄·실시간 로그 추적 등 로그 확인과 파이프 조합에 바로 활용할 수 있습니다."
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
- String
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
- cat
- head
- tail
- 파일내용
- 로그
- 로그추적
- follow
- 파이프
- Pipeline
- 텍스트
- stdout
image: "tmp_wordcloud.png"
---

`cat`, `head`, `tail`은 리눅스·유닉스에서 **파일 내용을 터미널(표준 출력)**으로 보여주는 명령어다. `cat`은 전체, `head`는 앞부분, `tail`은 뒷부분(및 실시간 추적)을 다룬다. 로그 확인·파이프 입력으로 자주 쓴다.

---

## cat — 파일 연결·전체 출력

### 사용법

```bash
cat [옵션] [파일...]
```

파일을 지정하면 순서대로 내용을 이어서 출력한다. 파일 없이 쓰면 표준 입력을 그대로 출력한다.

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-n`, `--number` | 줄 번호 붙여서 출력 |
| `-b`, `--number-nonblank` | 빈 줄 제외하고 줄 번호 |
| `-s`, `--squeeze-blank` | 연속 빈 줄을 한 줄로 |
| `-A` | 제어 문자·줄 끝 표시 (tab=`^I`, 줄끝=`$`) |
| `-E` | 줄 끝에 `$` 표시 |
| `-T` | 탭을 `^I`로 표시 |

### 예시

```bash
# 파일 전체 출력
cat config.ini

# 줄 번호와 함께
cat -n app.log

# 여러 파일 이어서 출력
cat header.txt body.txt footer.txt > full.txt

# 표준 입력을 그대로 전달 (파이프·리디렉션과 동일한 역할)
echo "hello" | cat
```

---

## head — 앞 N줄·앞 N바이트

### 사용법

```bash
head [옵션] [파일...]
```

기본값은 **앞 10줄**이다. 여러 파일이면 각 파일마다 헤더와 함께 출력한다.

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-n N`, `-N` | 앞 N줄만 (예: `head -5`, `head -n 5`) |
| `-c N` | 앞 N바이트만 |
| `-q` | 파일명 헤더 생략 (여러 파일일 때) |
| `-v` | 파일명 헤더 항상 출력 |

### 예시

```bash
# 앞 10줄 (기본)
head log.txt

# 앞 20줄
head -n 20 log.txt
head -20 log.txt

# 앞 1KB만
head -c 1024 data.bin

# 파이프와 조합
ps aux | head -5
```

---

## tail — 뒤 N줄·실시간 추적

### 사용법

```bash
tail [옵션] [파일...]
```

기본값은 **뒤 10줄**이다. 로그 파일의 최신 내용을 보거나, `-f`로 실시간 추적할 때 쓴다.

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-n N`, `-N` | 뒤 N줄만 (예: `tail -5`, `tail -n 5`) |
| `-c N` | 뒤 N바이트만 |
| `-f`, `--follow` | 파일 끝을 계속 감시하며 새로 추가되는 줄 출력 |
| `--retry` | 파일이 아직 없으면 재시도 (로그 로테이션 시 유용) |
| `-q` | 파일명 헤더 생략 |
| `-v` | 파일명 헤더 출력 |

### 예시

```bash
# 뒤 10줄 (기본)
tail log.txt

# 뒤 50줄
tail -n 50 app.log
tail -50 app.log

# 로그 실시간 보기 (Ctrl+C로 종료)
tail -f /var/log/syslog

# 여러 파일 동시 추적
tail -f access.log error.log
```

---

## 참고

- [GNU coreutils: cat](https://www.gnu.org/software/coreutils/manual/html_node/cat-invocation.html)
- [GNU coreutils: head and tail](https://www.gnu.org/software/coreutils/manual/html_node/head-invocation.html)
