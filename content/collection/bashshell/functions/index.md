---
draft: true
title: "[Bash Shell] 함수(functions) - 정의·호출·인자·return"
description: "Bash 스크립트에서 함수를 정의하고 호출하는 방법, 인자($1, $@), return·exit 코드, 지역 변수(local) 등 실무 예제를 다룹니다."
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
- function
- 함수
- local
- return
- 인자
- 스크립트
- Script
image: "tmp_wordcloud.png"
---

Bash **함수**는 반복되는 로직을 묶어서 이름으로 호출할 수 있게 한다. **인자**는 위치 매개변수(`$1`, `$2`, …), **반환**은 exit 상태(0~255)로 전달한다.

## 정의

```bash
# 방식 1
function name() {
  명령
}

# 방식 2
name() {
  명령
}
```

## 인자

- `$1`, `$2`, …: 첫 번째, 두 번째 인자.
- `$@`: 모든 인자(각각 따로 인용됨).
- `$*`: 모든 인자를 하나의 문자열로.
- `$#`: 인자 개수.

## 반환

- `return N`: 함수의 종료 상태를 N(0~255)으로 설정. **출력값**이 아니라 **exit status**만 반환한다.
- 실제 값을 반환하려면 `echo`로 출력하고 호출부에서 `$(함수)`로 받는다.

## 지역 변수

- `local var=value`: 함수 안에서만 쓰는 변수. 함수 밖 변수와 격리된다.

## 예시

```bash
myfunc() {
  local msg="$1"
  echo "Hello, $msg"
  return 0
}

myfunc "world"
result=$(myfunc "world")   # 출력을 변수에 저장
```

## 참고

- [Bash Manual: Shell Functions](https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html)
