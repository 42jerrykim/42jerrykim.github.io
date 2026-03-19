---
draft: true
title: "[Bash Shell] 조건문(if, test, [ ], [[ ]])"
description: "Bash 스크립트에서 조건 분기에 쓰는 if·test·[ ]·[[ ]]의 사용법, 파일·문자열·수치 조건, 실무 예제를 다룹니다."
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
- if
- test
- 조건문
- 스크립트
- Script
- 비교
- 파일테스트
- 문자열테스트
image: "wordcloud.png"
---

Bash **조건문**은 `if`와 **테스트 명령**(`test` 또는 `[ ]`, `[[ ]]`)을 함께 쓴다. `[[ ]]`는 Bash 확장으로, 패턴·문자열 비교에 유리하다.

## 기본 형태

```bash
if test 조건; then
  명령
elif test 조건2; then
  명령2
else
  명령3
fi
```

- `[ 조건 ]`은 `test 조건`과 동일. 앞뒤에 **공백**이 필요하다.

## 파일 테스트

| 테스트 | 의미 |
|--------|------|
| `-f FILE` | 일반 파일인가 |
| `-d FILE` | 디렉터리인가 |
| `-e FILE` | 존재하는가 |
| `-r FILE` | 읽기 가능한가 |
| `-s FILE` | 크기가 0보다 큰가 |

## 문자열

| 테스트 | 의미 |
|--------|------|
| `-z STR` | 길이 0인가 |
| `-n STR` | 길이 0이 아닌가 |
| `STR1 = STR2` | 같음 (공백 주의) |
| `STR1 != STR2` | 다름 |

## 수치 (정수)

| 테스트 | 의미 |
|--------|------|
| `-eq`, `-ne` | 같음, 다름 |
| `-lt`, `-le` | 미만, 이하 |
| `-gt`, `-ge` | 초과, 이상 |

## [[ ]] 확장

- `==`, `!=`로 패턴 매칭 가능: `[[ $x == *.txt ]]`
- `&&`, `||`를 안전하게 사용 가능.

## 예시

```bash
if [ -f "$file" ]; then
  echo "file exists"
fi

if [ -n "$VAR" ]; then
  echo "VAR is set"
fi

if [[ $x == *.log ]]; then
  echo "ends with .log"
fi
```

## 참고

- [Bash Manual: Conditional Constructs](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html)
