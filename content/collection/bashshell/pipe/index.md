---
draft: true
title: "[Bash Shell] 파이프(Pipe) - 명령어 출력을 입력으로 연결"
description: "리눅스·유닉스 셸에서 한 명령의 표준 출력을 다음 명령의 표준 입력으로 넘기는 파이프(|)의 개념, 사용법, 실무 예제와 리디렉션과의 차이를 다룹니다."
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
- pipe
- 파이프
- Pipeline
- stdout
- stdin
- Redirection
- 리디렉션
image: "wordcloud.png"
---

**파이프**(`|`)는 한 명령의 **표준 출력(stdout)**을 다음 명령의 **표준 입력(stdin)**으로 연결한다. 파일에 쓰지 않고 여러 명령을 이어 실행할 때 쓴다.

## 사용법

```bash
명령1 | 명령2 [| 명령3 ...]
```

- `명령1`의 stdout이 `명령2`의 stdin으로 전달된다.
- 표준 오류(stderr)는 파이프를 타지 않고 터미널로 나간다. stderr까지 넘기려면 `2>&1` 등으로 합친 뒤 파이프한다.

## 예시

```bash
# 프로세스 목록에서 nginx만
ps aux | grep nginx

# 로그에서 에러 줄만 세기
cat app.log | grep -i error | wc -l

# 정렬 후 중복 제거
sort list.txt | uniq

# 페이지 단위 보기
ls -l | less
```

## 리디렉션과의 차이

- **리디렉션** (`>`, `<`): 명령 ↔ **파일** 간 입출력.
- **파이프** (`|`): 명령 ↔ **다른 명령** 간 출력→입력.

둘을 같이 쓸 수 있다: `명령1 < input.txt | 명령2 > output.txt`

## 참고

- [Bash Manual: Pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)
- 같은 컬렉션의 **I/O Redirection** 글 — 표준 입출력·리디렉션 개념
