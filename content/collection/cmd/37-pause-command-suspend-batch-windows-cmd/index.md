---
draft: false
slug: pause-command-suspend-batch-windows-cmd
title: "[CMD] 37. pause - 배치 실행 일시 정지"
description: "pause로 배치 파일 실행을 사용자 입력이 있을 때까지 멈추는 법과 CTRL+C로 배치를 완전히 중단하는 법의 차이, 자동화·예약 작업에서 pause를 넣으면 안 되는 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 370
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
- pause
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Education(교육)
- CLI
- Comparison(비교)
- Scheduling
- Advanced
- Configuration(설정)
- Workflow(워크플로우)
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

pause는 배치 프로그램의 실행을 멈추고 "계속하려면 아무 키나 누르십시오..." 메시지를 표시하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [36장: shift](/post/cmd/shift-command-batch-parameters-windows-cmd/)에서 인자 처리를 다룬 뒤 이어진다. 지금까지 배운 제어 구조(if, for, call, goto, shift)가 자동으로 흘러가는 로직이었다면, pause는 그 흐름에 사람의 개입을 끼워 넣는 유일한 명령이다.

**이 장의 깊이**: 입문. 옵션이 없어 짧다.

## 사용법

```
pause
```

## 옵션

`/?` 외에 별도 옵션은 없다.

## 예시

```bat
@echo off
:Begin
copy a:*.*
echo Put a new disk into Drive A
pause
goto begin
```

## 주의사항·함정

**CTRL+C로 배치 자체를 중단할 수 있다**: pause로 멈춘 상태에서 아무 키가 아니라 CTRL+C를 누르면, 다음 확인 메시지가 뜬다.

> "If you press CTRL+C to stop a batch program, the following message appears, 'Terminate batch job (Y/N)?'." — Microsoft Learn, "pause"

여기서 Y를 누르면 배치 프로그램이 그 자리에서 완전히 끝나고 운영체제로 제어가 돌아간다. pause는 "잠깐 멈춤"과 "완전히 중단"을 같은 지점에서 사용자가 선택할 수 있게 하는 이중 용도를 갖는다.

**자동화·예약 작업에는 넣으면 안 된다**: pause는 사람이 물리적으로 키를 눌러줄 것을 전제로 한다. 예약 작업(57장에서 다룰 schtasks)이나 CI 파이프라인, 원격 세션이 끊긴 상태로 실행되는 스크립트에 pause가 들어 있으면, 그 지점에서 영원히 응답을 기다리며 멈춘 것처럼 보인다. 디버깅이나 사람이 직접 실행하는 스크립트에서만 pause를 쓰고, 무인 실행 스크립트에서는 애초에 넣지 않는 것이 안전하다.

**더블클릭 실행 시 창이 바로 닫히는 것을 막는 관용구**: 탐색기에서 배치 파일을 더블클릭하면 실행이 끝나자마자 CMD 창도 함께 닫혀, 마지막 출력을 확인할 새도 없이 사라지는 경우가 많다. 스크립트 맨 끝에 pause를 하나 두면 결과를 확인할 시간을 벌 수 있다 — 이 컬렉션의 여러 배치 예시(20장 type의 첫 예시 등)에서 이미 암묵적으로 전제하고 있던 관용구다.

**PowerShell의 대응 명령은 두 가지다**: 한 줄 텍스트 입력을 기다리며 Enter가 눌려야 넘어가는 `Read-Host -Prompt "계속하려면 Enter를 누르세요"`와, 아무 키나 누르면(Enter 없이도) 즉시 넘어가는 `[System.Console]::ReadKey()`가 있다. pause는 "아무 키나 누르면" 넘어간다는 점에서 줄 단위 입력을 요구하는 `Read-Host`보다는 `ReadKey()`의 동작 방식에 더 가깝다.

## 흔한 오개념

<strong>"pause가 있으면 사람이 직접 키를 누르기 전까지는 절대 넘어가지 않는다"</strong>는 오해가 있다. 실제로는 표준 입력에 키 입력 하나를 미리 흘려보내면(`echo.| script.bat`처럼 파이프로 빈 줄을 밀어 넣거나, `script.bat < nul`로 표준 입력을 nul 장치에 연결) pause는 사람의 개입 없이도 조용히 통과된다. 이는 CI 파이프라인이나 예약 작업처럼 무인 환경에서 우연히 pause가 남아 있어도 스크립트가 멈추지 않게 해주는 유용한 특성이 될 수 있지만, 반대로 정말 사람의 확인이 필요해서 넣은 pause가 자동화 도구(예: 다른 배치 파일이 `< nul`로 이 스크립트를 호출하는 경우)에 의해 의도치 않게 건너뛰어질 위험이기도 하다.

## 다음 장에서는

다음은 38장 — 현재 CMD 세션이나 배치 스크립트를 종료하고 종료 코드를 반환하는 `exit` 명령을 다룬다.

## 평가 기준

- pause로 배치 실행을 멈추고 사용자 입력을 기다리게 할 수 있다.
- pause 상태에서 CTRL+C를 누르면 배치 자체를 완전히 중단할 수 있다는 것을 안다.
- 자동화·예약 작업 스크립트에 pause를 넣으면 안 되는 이유를 설명할 수 있다.

## 참고

- [pause | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pause)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
