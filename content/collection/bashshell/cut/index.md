---
draft: true
title: "[Bash Shell] cut - 필드·문자열 잘라내기"
description: "리눅스·유닉스에서 줄의 필드나 문자 위치를 잘라 출력하는 cut의 사용법, -d·-f·-c 옵션과 CSV·고정폭 텍스트 처리 예제를 다룹니다."
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
- cut
- 필드
- 컬럼
- 텍스트처리
- delimiter
image: "tmp_wordcloud.png"
---

`cut`은 **필드(-f)** 또는 **문자 위치(-c)**로 줄을 잘라 출력한다. 구분자로 나뉜 로그·CSV에서 특정 열만 뽑을 때 쓴다.

## 사용법

```bash
cut [옵션] [파일...]
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-d C` | 필드 구분자 (기본: 탭) |
| `-f LIST` | 출력할 필드 (예: 1, 1-3, 1,4) |
| `-c LIST` | 출력할 문자 위치 (예: 1-10) |
| `-s` | 구분자가 없는 줄은 건너뜀 |

## 예시

```bash
# 첫 번째 필드 (구분자 기본 탭)
cut -f1 file.txt

# 콜론 구분, 1번과 3번 필드
cut -d: -f1,3 /etc/passwd

# 1~10번 문자만
cut -c1-10 file.txt
```

## 참고

- [GNU coreutils: cut](https://www.gnu.org/software/coreutils/manual/html_node/cut-invocation.html)
