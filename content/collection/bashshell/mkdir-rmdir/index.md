---
draft: true
title: "[Bash Shell] mkdir, rmdir - 디렉터리 생성·삭제"
description: "리눅스·유닉스에서 디렉터리를 만드는 mkdir과 빈 디렉터리를 제거하는 rmdir의 사용법, -p 옵션으로 상위 경로 생성·재귀 삭제, 실무 예제를 다룹니다."
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
- mkdir
- rmdir
- 디렉터리
- 디렉토리
- 생성
- 삭제
- recursive
- parent
image: "wordcloud.png"
---

`mkdir`은 **디렉터리**를 만들고, `rmdir`은 **빈 디렉터리**만 제거한다. 비어 있지 않은 디렉터리 삭제는 `rm -r`을 사용한다.

---

## mkdir — 디렉터리 생성

### 사용법

```bash
mkdir [옵션] 디렉터리...
```

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-p`, `--parents` | 상위 경로가 없으면 함께 생성. 이미 있으면 에러 내지 않음 |
| `-m MODE` | 권한을 MODE로 설정 (예: `mkdir -m 755 dir`) |
| `-v`, `--verbose` | 생성된 디렉터리 출력 |

### 예시

```bash
# 단일 디렉터리
mkdir project

# 여러 개 한 번에
mkdir dir1 dir2 dir3

# 상위 경로까지 생성
mkdir -p src/main/java

# 권한 지정
mkdir -m 700 private
```

---

## rmdir — 빈 디렉터리 삭제

### 사용법

```bash
rmdir [옵션] 디렉터리...
```

**비어 있는** 디렉터리만 제거한다. 파일이나 하위 디렉터리가 있으면 실패한다.

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-p`, `--parents` | 지정한 경로와 그 상위 빈 디렉터리까지 제거 |
| `--ignore-fail-on-non-empty` | 비어 있지 않아도 에러만 무시하고 계속 |

### 예시

```bash
# 빈 디렉터리 삭제
rmdir empty_dir

# a/b/c가 모두 비어 있으면 a, b, c 순으로 제거
rmdir -p a/b/c
```

---

## 참고

- [GNU coreutils: mkdir](https://www.gnu.org/software/coreutils/manual/html_node/mkdir-invocation.html)
- [GNU coreutils: rmdir](https://www.gnu.org/software/coreutils/manual/html_node/rmdir-invocation.html)
