---
draft: true
title: "[Bash Shell] touch - 타임스탬프·빈 파일 생성"
description: "리눅스·유닉스에서 파일의 접근·수정 시간을 바꾸거나 빈 파일을 만드는 touch 명령어의 사용법, -a·-m·-r 옵션과 실무 예제를 다룹니다."
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
- touch
- 타임스탬프
- mtime
- atime
- 빈파일
- timestamp
image: "tmp_wordcloud.png"
---

`touch`는 **파일의 접근·수정 시간**을 갱신하거나, 파일이 없으면 **빈 파일**을 만든다. 빈 플래그 파일 생성·빌드 의존성 갱신에 자주 쓴다.

## 사용법

```bash
touch [옵션] 파일...
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-a` | 접근 시간(atime)만 변경 |
| `-m` | 수정 시간(mtime)만 변경 |
| `-r FILE`, `--reference=FILE` | FILE의 시간을 참조로 사용 |
| `-t STAMP` | [[CC]YY]MMDDhhmm[.ss] 형식으로 시간 지정 |
| `-c`, `--no-create` | 파일이 없으면 만들지 않음 |

## 예시

```bash
# 빈 파일 생성 (이미 있으면 mtime만 갱신)
touch newfile.txt

# 여러 파일
touch a.txt b.txt c.txt

# 수정 시간만 갱신 (스크립트에서 "최신" 표시용)
touch -m lockfile

# 참조 파일과 같은 시간으로
touch -r source.txt target.txt
```

## 참고

- [GNU coreutils: touch](https://www.gnu.org/software/coreutils/manual/html_node/touch-invocation.html)
