---
draft: true
title: "[Bash Shell] tar - 아카이브·압축 해제"
description: "리눅스·유닉스에서 여러 파일을 하나의 아카이브로 묶고 풀 때 쓰는 tar의 사용법, -c·-x·-t·-f·-z·-j 옵션과 실무 예제를 다룹니다."
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
- tar
- 아카이브
- archive
- 압축
- gzip
- Compression
image: "tmp_wordcloud.png"
---

`tar`는 **여러 파일을 하나의 아카이브**로 묶거나 풀 때 쓴다. gzip·bzip2와 조합해 .tar.gz, .tar.bz2를 만든다.

## 사용법

```bash
tar [옵션] [아카이브] [파일...]
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-c` | 아카이브 생성 |
| `-x` | 아카이브 풀기 |
| `-t` | 목록만 출력 |
| `-f FILE` | 아카이브 파일 지정 (필수) |
| `-v` | 처리한 파일 나열 |
| `-z` | gzip 사용 (.gz) |
| `-j` | bzip2 사용 (.bz2) |
| `-C DIR` | 풀 때 대상 디렉터리 |

## 예시

```bash
# 아카이브 생성
tar -cvf backup.tar dir/

# gzip 압축
tar -czvf backup.tar.gz dir/

# 풀기
tar -xvf backup.tar
tar -xzvf backup.tar.gz -C /target/
```

## 참고

- [GNU tar manual](https://www.gnu.org/software/tar/manual/tar.html)
