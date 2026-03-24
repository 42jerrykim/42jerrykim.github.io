---
draft: true
title: "[Bash Shell] xargs - 표준 입력을 명령 인자로"
description: "리눅스·유닉스에서 표준 입력의 항목을 받아 다른 명령의 인자로 넘기는 xargs의 사용법, -0·-I·-P 옵션과 find·파이프 조합 예제를 다룹니다."
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
- xargs
- 인자
- arguments
- find
- batch
- Pipeline
image: "wordcloud.png"
---

`xargs`는 **표준 입력**으로 받은 줄·항목을 **다른 명령의 인자**로 넘긴다. `find` 결과를 한 번에 처리할 때 자주 쓴다.

## 사용법

```bash
xargs [옵션] [명령 [인자...]]
```

## 주요 옵션

| 옵션 | 설명 |
|------|------|
| `-0`, `--null` | 널 문자로 구분 (find -print0와 조합) |
| `-I replace-str` | replace-str을 입력 항목으로 치환 |
| `-P N` | 최대 N개 프로세스 병렬 실행 (GNU xargs) |
| `-n N` | 한 번에 최대 N개 인자만 전달 |

## 예시

```bash
# find 결과를 rm에 전달 (공백·줄바꿈 있는 이름도 안전)
find . -name "*.tmp" -print0 | xargs -0 rm

# 각 줄을 인자로
echo -e "a\nb\nc" | xargs -I {} echo item: {}

# 병렬 실행
cat urls.txt | xargs -P 4 -I {} curl -O {}
```

## 참고

- [GNU findutils: xargs](https://www.gnu.org/software/findutils/manual/html_node/xargs-invocation.html)
