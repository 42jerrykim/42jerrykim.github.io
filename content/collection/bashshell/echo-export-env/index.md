---
draft: true
title: "[Bash Shell] echo, export, env - 출력·환경 변수"
description: "리눅스·유닉스 셸에서 문자열을 출력하는 echo, 셸 변수를 자식 프로세스에 넘기는 export, 환경을 보거나 명령을 실행하는 env의 사용법과 실무 예제를 다룹니다."
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
- echo
- export
- env
- 환경변수
- environment
- variable
- PATH
image: "wordcloud.png"
---

`echo`는 **문자열을 표준 출력**하고, `export`는 **변수를 환경 변수**로 만들어 자식 프로세스에 전달하며, `env`는 **환경을 보거나** 그 환경으로 **명령을 실행**한다.

---

## echo — 출력

### 사용법

```bash
echo [-n] [문자열...]
```

- `-n`: 줄바꿈을 붙이지 않음.
- Bash에서는 `echo -e`로 이스케이프(\n 등) 해석. 이식성은 `printf`가 낫다.

### 예시

```bash
echo "Hello"
echo -n "no newline"
echo $HOME
```

---

## export — 환경 변수 내보내기

### 사용법

```bash
export name[=value]...
```

지정한 변수를 **환경**에 넣어, 이후 실행되는 자식 프로세스에서 사용할 수 있게 한다.

### 예시

```bash
export PATH="/usr/local/bin:$PATH"
export MY_CONFIG=production
```

---

## env — 환경 보기·명령 실행

### 사용법

```bash
env [옵션] [name=value...] [명령 [인자...]]
```

- 인자 없으면 현재 환경을 출력.
- `name=value`와 명령을 주면, 그 변수들을 추가/덮어쓴 환경으로 명령을 실행.

### 예시

```bash
env
env LANG=C sort file.txt
env -i PATH=/usr/bin:/bin command   # 깨끗한 환경으로 실행
```

---

## 참고

- [Bash Manual: Bourne Shell Builtins](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html)
