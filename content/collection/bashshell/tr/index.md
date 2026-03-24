---
draft: true
title: "[Bash Shell] tr - 문자 변환·삭제"
description: "리눅스·유닉스에서 표준 입력의 문자를 바꾸거나 삭제하는 tr의 사용법, 집합·문자 클래스, 대소문자 변환 등 실무 예제를 다룹니다."
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
- tr
- 문자변환
- translate
- 삭제
- 대소문자
image: "wordcloud.png"
---

`tr`(translate)는 **표준 입력**의 문자를 다른 문자로 바꾸거나 **삭제**한다. 한 줄씩만 처리하며 파일 인자를 받지 않는다.

## 사용법

```bash
tr [옵션] 집합1 [집합2]
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-d 집합` | 집합에 있는 문자 삭제 |
| `-s 집합` | 연속된 문자를 하나로 (squeeze) |
| `-c` | 집합을 제외한 문자 (complement) |

## 문자 집합

- `a-z`, `A-Z`, `0-9` 등 범위
- `[:lower:]`, `[:upper:]`, `[:digit:]` 등 클래스 (GNU tr)

## 예시

```bash
# 소문자 → 대문자
echo "hello" | tr 'a-z' 'A-Z'

# 줄바꿈을 공백으로
tr '\n' ' ' < file.txt

# 숫자 삭제
tr -d '0-9' < file.txt

# 연속 공백을 하나로
tr -s ' ' < file.txt
```

## 참고

- [GNU coreutils: tr](https://www.gnu.org/software/coreutils/manual/html_node/tr-invocation.html)
