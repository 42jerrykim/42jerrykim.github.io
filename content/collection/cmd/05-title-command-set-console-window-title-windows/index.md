---
draft: false
slug: title-command-set-console-window-title-windows
title: "[CMD] 05. title - 콘솔 창 제목 설정"
description: "title 명령으로 CMD 창의 제목 표시줄 텍스트를 바꾸는 법과, 여러 창을 동시에 열었을 때 배치 파일 진행 단계를 제목으로 구분하는 관례, 세션 범위 한계를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 50
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
- title
- 창제목
- Console
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Productivity(생산성)
- Configuration(설정)
- Workflow(워크플로우)
- Multitasking
- Education(교육)
- Tutorial(튜토리얼)
- Troubleshooting(트러블슈팅)
- CLI
image: "wordcloud.png"
---

title은 현재 CMD 창의 제목 표시줄에 보이는 텍스트를 설정하는 내장 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [04장: prompt](/post/cmd/prompt-command-customize-command-line-windows/)에서 명령 입력줄 앞의 프롬프트 문자열을 바꾸는 법을 다룬 뒤 이어진다. prompt가 "창 안"의 텍스트를 바꾼다면, title은 "창 자체"의 표시를 바꾼다는 점에서 대비된다.

**이 장의 깊이**: 입문. 옵션이 텍스트 인수 하나뿐이라 짧다.

## 사용법

```
title [<문자열>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `<문자열>` | 창 제목으로 표시할 텍스트 |
| `/?` | 명령 프롬프트에서 도움말 표시 |

## 예시

```
title Backup Script
title Step 2 - Copying files
```

Microsoft Learn은 배치 파일 진행 단계에 따라 제목을 바꿨다가 되돌리는 예시를 다음과 같이 제시한다.

```bat
@echo off
title Updating Files
copy \\server\share\*.xls c:\users\common\*.xls
echo Files Updated.
title Command Prompt
```

여러 CMD 창을 동시에 띄워 놓고 작업할 때, 각 배치 파일 시작 부분에 `title`을 넣어두면 작업 표시줄에서 어떤 창이 어떤 작업을 하고 있는지 한눈에 구분할 수 있다.

## 주의사항·함정

**세션 범위이며, 되돌리는 방법이 title뿐이다**: 제목은 해당 CMD 세션에만 적용되고 다른 CMD 창에는 영향을 주지 않는다. 더 특이한 점은 한 번 바꾼 제목을 원래대로 되돌리는 방법이 다시 `title` 명령을 실행하는 것뿐이라는 사실이다. Microsoft Learn은 이를 명시적으로 언급한다.

> "After a window title is set, you can reset it only by using the **title** command." — Microsoft Learn, "title"

즉 배치 파일이 도중에 비정상 종료되어 제목을 원래대로 되돌리는 마지막 `title` 명령을 실행하지 못하면, 그 CMD 창은 이전 작업의 제목을 계속 달고 있게 된다.

**특수문자는 그대로 표시되지만 따옴표는 제외된다**: 제목 문자열에 특수문자를 넣으면 그대로 표시되지만, 인용에 쓴 큰따옴표 자체는 제목에 포함되지 않는다.

**PowerShell에서는 명령이 아니라 속성 할당이다**: PowerShell에서 콘솔 창 제목을 바꾸는 방법은 `title` 같은 별도 명령이 아니라 `$host.UI.RawUI.WindowTitle = "새 제목"`처럼 호스트 객체의 속성에 문자열을 대입하는 것이다. CMD의 title이 인수를 받는 명령이라면 PowerShell 쪽은 값을 읽고 쓸 수 있는 속성이라, `$host.UI.RawUI.WindowTitle`을 그냥 출력해 현재 제목을 조회할 수도 있다. 다만 이 속성의 실제 동작은 Windows Terminal·콘솔 호스트·ISE 등 PowerShell을 담는 호스트 구현에 따라 달라질 수 있어, 모든 환경에서 동일하게 보장되지는 않는다.

## 흔한 오개념

<strong>"title로 제목을 바꾸면 작업 관리자에 표시되는 프로세스 이름도 함께 바뀐다"</strong>는 오해가 있다. 실제로 title이 바꾸는 것은 콘솔 창의 제목 표시줄 텍스트뿐이다. 작업 관리자의 "세부 정보" 탭에서 보이는 프로세스 이미지 이름은 여전히 `cmd.exe`로 남아 있고, 여러 CMD 창을 띄워 놓았을 때 그중 어느 것이 어떤 작업을 하는지는 작업 관리자가 아니라 작업 표시줄의 창 제목으로 구분해야 한다.

## 다음 장에서는

다음은 06장 — 명령줄 편집과 매크로, 히스토리를 관리하는 `doskey`를 다룬다.

## 평가 기준

- title과 prompt가 각각 무엇을 바꾸는지(창 제목 vs 입력줄 프롬프트) 구분해 설명할 수 있다.
- 배치 파일 진행 단계를 제목으로 표시하는 관례적 패턴을 작성할 수 있다.
- 제목을 되돌리는 유일한 방법이 title 명령 자체라는 것과, 그로 인해 배치 파일이 비정상 종료되면 어떤 문제가 생기는지 설명할 수 있다.

## 참고

- [title | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/title)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
