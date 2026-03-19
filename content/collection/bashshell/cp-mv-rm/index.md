---
draft: true
title: "[Bash Shell] cp, mv, rm - 복사·이동·삭제"
description: "리눅스·유닉스에서 파일·디렉터리를 복사하는 cp, 이동·이름변경하는 mv, 삭제하는 rm의 사용법과 -r·-i·-f 등 주요 옵션, 실무 예제를 다룹니다."
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
- cp
- mv
- rm
- 복사
- 이동
- 삭제
- recursive
- force
- backup
image: "wordcloud.png"
---

`cp`는 **복사**, `mv`는 **이동·이름 변경**, `rm`은 **삭제**를 수행한다. 디렉터리 작업 시 `-r` 옵션이 필요하다.

---

## cp — 복사

### 사용법

```bash
cp [옵션] 소스... 대상
```

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-r`, `-R`, `--recursive` | 디렉터리 재귀 복사 |
| `-i`, `--interactive` | 덮어쓰기 전 확인 |
| `-f`, `--force` | 덮어쓰기 강제 |
| `-p` | 속성(시간, 권한) 유지 |
| `-a`, `--archive` | 아카이브 모드(-rp와 유사, 심볼릭 링크 등 유지) |

### 예시

```bash
# 파일 복사
cp file.txt backup.txt

# 디렉터리 복사
cp -r src src.bak

# 속성 유지
cp -a /data /backup/data
```

---

## mv — 이동·이름 변경

### 사용법

```bash
mv [옵션] 소스... 대상
```

같은 파일시스템에서는 이름만 바뀌고, 다른 파일시스템으로는 복사 후 원본 삭제된다.

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-i`, `--interactive` | 덮어쓰기 전 확인 |
| `-f`, `--force` | 덮어쓰기 강제 |
| `-n`, `--no-clobber` | 기존 파일 덮어쓰지 않음 |

### 예시

```bash
# 이름 변경
mv old.txt new.txt

# 다른 디렉터리로 이동
mv file.txt ~/docs/

# 여러 파일 한 디렉터리로
mv a.txt b.txt dest/
```

---

## rm — 삭제

### 사용법

```bash
rm [옵션] 파일...
```

**휴지통 없이 바로 삭제**되므로 사용에 주의한다.

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-r`, `-R`, `--recursive` | 디렉터리 재귀 삭제 |
| `-i`, `--interactive` | 삭제 전 확인 |
| `-f`, `--force` | 확인 없이 강제 삭제 |
| `-d`, `--dir` | 빈 디렉터리 삭제 허용 |

### 예시

```bash
# 파일 삭제
rm file.txt

# 디렉터리 삭제 (재귀)
rm -r temp/

# 확인하며 삭제
rm -ri project/
```

---

## 참고

- [GNU coreutils: cp, mv, rm](https://www.gnu.org/software/coreutils/manual/html_node/cp-invocation.html)
