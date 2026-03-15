---
draft: true
title: "[Bash Shell] awk - 텍스트·필드 처리"
description: "리눅스·유닉스에서 필드 단위로 텍스트를 처리하는 awk의 사용법, 패턴·액션, 내장 변수(NR, NF, FS), 실무 예제를 다룹니다."
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
- awk
- 필드
- 텍스트처리
- NR
- NF
- FS
- 스크립트
image: "tmp_wordcloud.png"
---

`awk`는 **필드(열) 단위**로 텍스트를 처리하는 도구다. 패턴에 맞는 줄을 골라 특정 필드를 출력·계산할 때 쓴다.

## 사용법

```bash
awk '패턴 { 액션 }' [파일...]
awk -f 스크립트.awk [파일...]
```

- 필드 구분자는 공백(기본) 또는 `-F`로 지정. `$1`, `$2`, …는 첫 번째, 두 번째 필드. `$0`는 줄 전체.

## 내장 변수

| 변수 | 설명 |
|------|------|
| NR | 현재 줄 번호 |
| NF | 현재 줄의 필드 수 |
| FS | 필드 구분자 (입력) |
| OFS | 필드 구분자 (출력) |

## 예시

```bash
# 첫 번째 필드만 출력
awk '{ print $1 }' file.txt

# 구분자 지정 (예: 콜론)
awk -F: '{ print $1, $3 }' /etc/passwd

# 10번째 줄만
awk 'NR==10' file.txt

# NF가 3 이상인 줄만
awk 'NF>=3' file.txt

# 합계 등 계산
awk '{ sum += $1 } END { print sum }' numbers.txt
```

## 참고

- [GNU awk manual](https://www.gnu.org/software/gawk/manual/gawk.html)
