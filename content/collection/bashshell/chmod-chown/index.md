---
draft: true
title: "[Bash Shell] chmod, chown - 권한·소유자 변경"
description: "리눅스·유닉스에서 파일·디렉터리의 권한을 바꾸는 chmod, 소유자·그룹을 바꾸는 chown의 사용법, 8진수·기호 모드, 실무 예제를 다룹니다."
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
- chmod
- chown
- chgrp
- 권한
- permission
- 소유자
- owner
- 755
- 644
image: "wordcloud.png"
---

`chmod`는 **권한(퍼미션)**을, `chown`은 **소유자·그룹**을 바꾼다. 보안·배포 시 자주 쓴다.

---

## chmod — 권한 변경

### 사용법

```bash
chmod [옵션] 모드 파일...
chmod [옵션] 8진수 파일...
```

### 8진수 모드 (자주 쓰는 값)

| 값 | 의미 |
|----|------|
| 7 | rwx (읽기+쓰기+실행) |
| 6 | rw- |
| 5 | r-x |
| 4 | r-- |
| 0 | --- |

- 세 자리: 소유자·그룹·그 외 (예: 755 = rwxr-xr-x).
- 네 자리면 앞에 setuid 등(4,2,1) 추가.

### 기호 모드

- `u,g,o,a`: 소유자, 그룹, 그 외, 모두.
- `+,-,=`: 추가, 제거, 지정.
- `r,w,x`: 읽기, 쓰기, 실행.

### 예시

```bash
chmod 755 script.sh
chmod u+x file
chmod -R 644 dir/
```

---

## chown — 소유자·그룹 변경

### 사용법

```bash
chown [옵션] 사용자[:그룹] 파일...
```

- 루트(또는 권한 있는 사용자)만 실행 가능.

### 예시

```bash
chown www-data log.txt
chown user:group file.txt
chown -R deploy:deploy /var/app
```

---

## 참고

- [chmod(1)], [chown(1)] — man 페이지
