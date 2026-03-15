---
draft: true
title: "[Bash Shell] gzip, gunzip - 압축·해제"
description: "리눅스·유닉스에서 gzip으로 파일을 압축·해제하는 방법, -k·-d·-r 옵션과 tar와의 조합, 실무 예제를 다룹니다."
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
- gzip
- gunzip
- 압축
- Compression
- .gz
image: "tmp_wordcloud.png"
---

`gzip`은 **단일 파일**을 .gz로 압축하고, `gunzip`(또는 `gzip -d`)은 압축을 푼다. 원본은 기본적으로 제거된다.

## 사용법

```bash
gzip [옵션] [파일...]
gunzip [옵션] [파일...]
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-d` | 압축 해제 (gunzip과 동일) |
| `-k` | 원본 파일 유지 |
| `-r` | 디렉터리 재귀 |
| `-N` | 압축 수준 (1~9, 기본 6) |

## 예시

```bash
gzip file.txt      # file.txt.gz 생성, file.txt 제거
gzip -k file.txt   # 원본 유지
gunzip file.txt.gz
```

## 참고

- [GNU gzip manual](https://www.gnu.org/software/gzip/manual/gzip.html)
