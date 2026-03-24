---
draft: true
title: "[Bash Shell] 변수와 인용(Quoting) - 확장·따옴표 차이"
description: "Bash에서 변수 확장·공백·특수문자를 다룰 때 쓰는 인용(quoting)과 따옴표 종류(쌍따옴표·홑따옴표·이스케이프)의 차이, 실무 예제를 다룹니다."
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
- quoting
- 인용
- 변수
- variable
- 쌍따옴표
- 홑따옴표
- 이스케이프
- expand
- Parameter-Expansion
image: "wordcloud.png"
---

Bash에서 **인용(quoting)**은 공백·특수문자·변수 확장을 제어한다. **쌍따옴표(`"`)**, **홑따옴표(`'`)**, **백슬래시(`\`)**의 동작이 다르다.

## 쌍따옴표 `"..."`

- **변수 확장** (`$VAR`), **명령 치환** (`` `cmd` ``, `$(cmd)`), **역슬래시 이스케이프** (`\$`, `\"`, `` \` ``)가 해석된다.
- 공백·와일드카드(`*`, `?`)는 리터럴로 취급되어 단일 인자로 유지된다.

```bash
name="hello world"
echo "$name"    # hello world
echo "$(date)" # 명령 치환 결과
```

## 홑따옴표 `'...'`

- **모든 문자를 리터럴**로 취급. 변수·명령 치환·이스케이프가 해석되지 않는다.
- 홑따옴표 안에 홑따옴표를 넣을 수 없고, `'\''`처럼 나눠서 쓴다.

```bash
echo '$HOME'    # $HOME 그대로 출력
```

## 백슬래시 `\`

- 다음 문자 한 개를 이스케이프. `\$`, `\``, `\"` 등으로 특수 의미를 없앤다.

## 변수 확장 시 인용

- 값에 공백·특수문자가 있으면 **반드시 인용**하는 것이 안전하다: `"$var"`. `$var`만 쓰면 단어 분할·글로빙이 적용된다.

## 참고

- [Bash Manual: Quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html)
