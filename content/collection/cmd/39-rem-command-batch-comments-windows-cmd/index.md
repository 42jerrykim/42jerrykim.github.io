---
draft: false
slug: rem-command-batch-comments-windows-cmd
title: "[CMD] 39. rem - 배치 파일 주석"
description: "rem으로 배치 파일에 주석을 남기는 법과 리다이렉션·파이프 문자를 주석 줄에 쓸 수 없는 제약, 관행적으로 쓰이는 :: 대체 표기의 위험성, rem/||()를 이용한 여러 줄 주석 트릭을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 390
categories:
- CMD
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- Command
- Guide(가이드)
- Reference(참고)
- Quick-Reference
- How-To
- Tips
- Beginner
- rem
- 주석
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Education(교육)
- CLI
- Comparison(비교)
- Advanced
- Configuration(설정)
- Command-Extensions
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

rem은 배치·스크립트·config.sys 파일에 주석을 기록하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [38장: exit](/post/cmd/exit-command-terminate-cmd-windows/)에서 스크립트 종료를 다룬 뒤 이어진다. 4부(배치 스크립팅)의 제어 구조를 거의 다 배운 시점에서, 그 코드를 설명하는 주석 문법을 짚고 넘어간다.

**이 장의 깊이**: 입문. 옵션이 없어 짧지만, 표기법을 둘러싼 함정이 의외로 많다.

## 사용법

```
rem [<주석>]
```

## 옵션

`/?` 외에 별도 옵션은 없다. rem 뒤에 오는 나머지 텍스트 전체가 주석으로 처리된다.

## 예시

```bat
@echo off
rem  This batch program formats and checks new disks.
rem  It is named Checknew.bat.
rem
rem echo Insert new disk in Drive B.
pause
format b: /v chkdsk b:
```

```
rem Set prompt to indicate current directory
prompt $p$g
```

## 주의사항·함정

**리다이렉션·파이프 문자를 주석 안에 쓸 수 없다**: Microsoft Learn은 rem 주석 안에서 `<`, `>`, `|`를 쓸 수 없다고 명시한다. 예를 들어 파이프 예시를 설명하는 주석에 그 파이프 문자를 그대로 옮겨 적으면 파싱 오류가 날 수 있다 — 그런 문자는 캐럿(`^`)으로 이스케이프하거나 아예 다른 표현으로 바꿔 써야 한다.

**주석은 화면에 출력되지 않는다**: rem 줄 자체는 실행되지 않고 화면에도 나타나지 않는다. `echo on` 상태라면 명령 에코 기능 때문에 rem 줄이 화면에 그대로 보일 수는 있지만, 이는 rem이 무언가를 "출력"해서가 아니라 에코가 실행되는 모든 줄을 보여주기 때문이다.

**`::`는 rem의 대체 표기가 아니라 우연한 부작용이다**: 많은 배치 스크립트가 짧은 주석에 `rem` 대신 `::`를 쓴다. 이는 실제로는 "빈 이름의 레이블"로 해석되는 부작용을 이용한 관행일 뿐, CMD가 공식적으로 지원하는 주석 문법이 아니다. `if`나 `for`의 괄호 블록 안에서 `::`를 쓰면 레이블로 취급되어 예상과 다르게 동작하거나 오류가 날 수 있다. 호환성과 명확성을 위해서는 `rem`을 쓰는 편이 안전하다.

**여러 줄 주석은 조건부 실행으로 흉내 낼 수 있다**: rem 자체에는 여러 줄 주석 문법이 없지만, `Rem/||(...)`처럼 "항상 실패하는 조건"을 이용해 괄호 블록 전체를 실행하지 않게 만드는 트릭이 있다.

```bat
Rem/||(
  이 블록은 실행되지 않는다.
  블록 안의 닫는 괄호는 캐럿으로 이스케이프해야 한다 ^)
)
```

`Rem/`은 항상 성공(0)으로 평가되므로, `||`(직전 명령이 실패했을 때만 다음을 실행) 뒤의 블록은 절대 실행되지 않는다 — 여러 줄에 걸친 설명을 담을 때 쓰이는 잘 알려지지 않은 트릭이다.

**PowerShell의 주석은 문법 자체가 완전히 다르고, rem 같은 파싱 부작용이 없다**: 한 줄 주석은 `#`, 블록 주석은 `<# ... #>`을 쓴다. rem은 이름 그대로 여전히 하나의 "명령"이라서 반복문 안에서 매번 파싱·실행되는 대상이지만, PowerShell의 `#` 주석은 파서가 애초에 코드로 취급하지 않으므로 rem처럼 반복 실행 경로에서 파싱 부담을 남기거나(빈 레이블을 흉내 낸 `::`가 겪는 것 같은) 문맥에 따라 다르게 해석될 위험이 없다.

## 흔한 오개념

<strong>"rem과 ::는 완전히 동일하게 바꿔 쓸 수 있는 주석 표기다"</strong>는 오해가 있다. 위에서 다뤘듯 `::`는 공식 주석 문법이 아니라 "빈 이름의 레이블"로 해석되는 우연한 부작용일 뿐이라, `rem`과 파싱 규칙이 다르다. 특히 `if`나 `for`의 괄호로 묶인 블록 안에서 `::`를 주석처럼 쓰면 레이블로 잘못 인식되어 문법 오류가 나거나 블록 실행이 중간에 깨질 수 있다 — 같은 위치에 `rem`을 썼다면 일어나지 않았을 문제다. 블록 바깥의 짧은 주석에서는 `::`가 대체로 무난하게 동작하지만, 괄호 블록 안에서는 항상 `rem`을 쓰는 편이 안전하다.

## 다음 장에서는

다음은 40장 — 환경 변수와 현재 디렉터리 변경을 블록 안으로 제한하는 `setlocal`, `endlocal` 명령을 다룬다.

## 평가 기준

- rem으로 배치 파일에 주석을 남길 수 있다.
- 주석 줄에 리다이렉션·파이프 문자를 직접 쓸 수 없다는 제약을 안다.
- `::`가 공식 주석 문법이 아니라 빈 레이블의 부작용이며, 조건문 블록 안에서 문제가 될 수 있다는 것을 설명할 수 있다.
- `Rem/||(...)` 패턴으로 여러 줄 주석을 흉내 내는 원리를 설명할 수 있다.

## 참고

- [rem | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/rem)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
