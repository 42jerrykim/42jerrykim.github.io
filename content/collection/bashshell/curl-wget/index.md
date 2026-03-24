---
draft: true
title: "[Bash Shell] curl, wget - HTTP·다운로드"
description: "리눅스·유닉스에서 URL로 HTTP 요청·파일 다운로드를 하는 curl과 wget의 사용법, 옵션과 실무 예제를 다룹니다."
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
- curl
- wget
- HTTP
- 다운로드
- download
- API
- Networking
image: "wordcloud.png"
---

`curl`과 `wget`은 **URL**에서 데이터를 가져오거나 **파일을 다운로드**할 때 쓴다. curl은 다양한 프로토콜·헤더 조작에, wget은 재귀·미러링에 강하다.

---

## curl

### 사용법

```bash
curl [옵션] URL...
```

### 자주 쓰는 옵션

| 옵션 | 설명 |
|------|------|
| `-o FILE` | 출력을 FILE로 저장 |
| `-O` | URL의 파일명으로 저장 |
| `-L` | 리다이렉트 따라감 |
| `-H "Header: value"` | 헤더 추가 |
| `-X METHOD` | HTTP 메서드 지정 |
| `-d DATA` | POST 데이터 |

### 예시

```bash
curl -O https://example.com/file.zip
curl -L -o page.html https://example.com
curl -X POST -d "key=value" https://api.example.com
```

---

## wget

### 사용법

```bash
wget [옵션] URL...
```

### 자주 쓰는 옵션

| 옵션 | 설명 |
|------|------|
| `-O FILE` | 저장 파일명 지정 |
| `-q` | 조용 모드 |
| `-r` | 재귀 다운로드 |
| `-np` | 상위 디렉터리로 올라가지 않음 |

### 예시

```bash
wget https://example.com/file.zip
wget -O saved.zip "https://example.com/file"
```

---

## 참고

- [curl man page](https://curl.se/docs/manpage.html)
- [GNU wget manual](https://www.gnu.org/software/wget/manual/wget.html)
