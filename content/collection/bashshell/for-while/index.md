---
draft: true
title: "[Bash Shell] 반복문(for, while, until)"
description: "Bash 스크립트에서 반복에 쓰는 for·while·until의 사용법, 리스트·범위·C 스타일·무한 루프와 break·continue 예제를 다룹니다."
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
- for
- while
- until
- 반복문
- loop
- 스크립트
- Script
- break
- continue
image: "tmp_wordcloud.png"
---

Bash **반복문**에는 **for**, **while**, **until**이 있다. 리스트·파일·숫자 범위를 돌리거나 조건이 참/거짓인 동안 반복할 때 쓴다.

## for — 리스트·범위

```bash
# 리스트
for x in a b c; do
  echo "$x"
done

# 파일명 (와일드카드)
for f in *.txt; do
  echo "$f"
done

# C 스타일 (Bash)
for ((i=0; i<10; i++)); do
  echo $i
done

# 범위
for i in {1..5}; do
  echo $i
done
```

## while — 조건이 참인 동안

```bash
while [ 조건 ]; do
  명령
done

# 읽기
while read line; do
  echo "$line"
done < file.txt
```

## until — 조건이 거짓인 동안

```bash
until [ 조건 ]; do
  명령
done
```

## break·continue

- `break`: 루프 즉시 탈출.
- `continue`: 이번 반복만 건너뛰고 다음 반복으로.

## 참고

- [Bash Manual: Looping Constructs](https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs.html)
