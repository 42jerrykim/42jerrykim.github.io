---
draft: false
slug: exit-command-terminate-cmd-windows
title: "[CMD] 38. exit - CMD 세션과 배치 스크립트 종료"
description: "exit로 CMD 세션이나 배치 스크립트를 종료하고 종료 코드를 반환하는 법과 /b가 있을 때와 없을 때 종료 범위가 완전히 달라지는 차이, exit code가 ERRORLEVEL로 이어지는 관계를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 380
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
- exit
- ERRORLEVEL
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

exit는 명령 인터프리터(cmd.exe) 또는 현재 실행 중인 배치 스크립트를 종료하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [37장: pause](/post/cmd/pause-command-suspend-batch-windows-cmd/)에서 실행을 멈추는 법을 다룬 뒤 이어진다. pause가 "잠깐 멈춤"이었다면 exit는 "완전히 끝냄"이다 — 4부(배치 스크립팅)에서 다룬 제어 흐름 대부분이 결국 어딘가에서 exit로 수렴한다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: exit로 반환한 코드를 호출한 쪽에서 검사하는 문법은 32장(if)에서 이미 다뤘다.

## 사용법

```
exit [/b] [<종료코드>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/b` | 현재 배치 스크립트만 종료(cmd.exe 자체는 유지). 배치 밖에서 실행하면 cmd.exe를 종료 |
| `<종료코드>` | 숫자. `/b`와 함께면 ERRORLEVEL에, 그렇지 않으면 프로세스 종료 코드에 설정 |

## 예시

```
exit
exit /b 1
exit 0
```

```bat
@echo off
if not exist input.txt (
  echo 입력 파일이 없습니다.
  exit /b 1
)
echo 처리 중...
exit /b 0
```

## 주의사항·함정

**`/b` 유무에 따라 종료 범위가 완전히 달라진다**: 이 장의 핵심 함정이다. `/b` 없이 `exit`만 배치 파일 안에서 실행하면 그 배치를 실행 중인 cmd.exe 프로세스 자체가 종료된다 — 다른 배치 파일이 34장(call)의 방식으로 이 배치를 호출한 것이 아니라 그냥 실행한 것이었다면, 호출한 쪽의 CMD 창까지 함께 닫혀버릴 수 있다. 반면 `/b`를 쓰면 현재 배치 스크립트의 실행만 끝나고, 그 배치를 실행시킨 cmd.exe 세션(또는 그 배치를 call한 부모 배치)은 계속 살아있다.

> "/b — Exits the current batch script instead of exiting Cmd.exe. If executed from outside a batch script, exits Cmd.exe." — Microsoft Learn, "exit"

34장(call)에서 다룬 "서브루틴에서 종료 코드를 돌려받는" 패턴이 정상적으로 동작하려면, 그 서브루틴은 반드시 `exit /b <코드>`로 끝나야 한다 — `/b` 없는 exit를 서브루틴 끝에 쓰면 호출한 쪽까지 통째로 종료되어버린다.

**종료 코드는 상황에 따라 다른 곳에 저장된다**: `/b`와 함께 코드를 지정하면 그 값은 `%ERRORLEVEL%`에 담겨 32장(if)의 `if errorlevel`이나 `if %errorlevel% EQU`로 검사할 수 있다. `/b` 없이 cmd.exe 자체를 종료할 때 지정한 코드는 그 cmd.exe 프로세스의 운영체제 수준 종료 코드가 되어, cmd.exe를 호출한 부모 프로세스(다른 프로그램이나 스크립트 엔진)가 그 값을 받는다.

**대화형 세션에서 `exit`는 창을 닫는다**: 배치 파일이 아니라 대화형으로 입력한 `exit`는 그 CMD 창을 그대로 닫는다. 01장(cmd)에서 `cmd /k`로 연 세션이라면, `exit`를 입력해야 비로소 창이 사라진다.

**PowerShell도 `exit` 키워드를 그대로 쓰지만, 종료 코드를 추적하는 변수가 CMD보다 더 세분화되어 있다**: CMD는 직전 명령의 종료 코드를 `%ERRORLEVEL%` 하나로 관리하지만, PowerShell은 `$LASTEXITCODE`가 **외부** 명령이나 실행 파일의 종료 코드만 담당한다. 네이티브 PowerShell 명령(cmdlet)이 실패했을 때는 보통 `$LASTEXITCODE`를 건드리지 않고, 예외를 던지거나 `$?`를 `$false`로 설정하는 방식으로 실패를 알린다. 이 `$LASTEXITCODE`와 `$?`의 이중 추적 체계는 CMD의 단일 `%ERRORLEVEL%` 변수보다 더 세밀하지만, 그만큼 어느 쪽을 확인해야 하는지 헷갈리기 쉽다.

## 흔한 오개념

<strong>"exit 0은 항상 성공, exit 1은 항상 실패를 뜻하는 절대 규칙이다"</strong>는 오해가 있다. 0을 성공으로 관례적으로 쓰는 것은 맞지만, 이는 운영체제나 CMD가 강제하는 규칙이 아니라 프로그램 작성자와 호출자 사이의 약속일 뿐이다. 15장(xcopy)이나 16장(robocopy)에서 본 것처럼, 어떤 명령은 0이 아닌 값을 "실패 없음"으로 쓰기도 한다 — 종료 코드의 의미는 항상 그 명령의 문서를 확인해야 한다.

## 다음 장에서는

다음은 39장 — 배치 파일에 실행되지 않는 설명을 남기는 `rem` 명령을 다룬다.

## 평가 기준

- exit로 CMD 세션이나 배치 스크립트를 종료하고 종료 코드를 지정할 수 있다.
- `/b`가 있을 때와 없을 때 무엇이 종료되는지(배치 스크립트만 vs cmd.exe 전체) 설명할 수 있다.
- call로 호출된 서브루틴이 `exit /b`로 끝나야 하는 이유를 설명할 수 있다.
- 종료 코드 0이 절대적인 성공 규칙이 아니라 관례라는 것을 안다.

## 참고

- [exit | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/exit)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
