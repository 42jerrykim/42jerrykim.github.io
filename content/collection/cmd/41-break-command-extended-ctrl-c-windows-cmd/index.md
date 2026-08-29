---
draft: false
slug: break-command-extended-ctrl-c-windows-cmd
title: "[CMD] 41. break - 확장된 Ctrl+C 검사(레거시)"
description: "break가 현재 Windows에서는 아무 효과가 없는 MS-DOS 호환용 레거시 명령이라는 것과, 아무 일도 하지 않는 특성을 이용해 파일을 만들거나 비우는 break>file 트릭, diskpart의 동명 명령과 헷갈리지 않는 법을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 410
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
- break
- Legacy
- Batch
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Education(교육)
- CLI
- Comparison(비교)
- MS-DOS
- Configuration(설정)
- Advanced
- Debugging
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

break는 MS-DOS 시절 확장된 Ctrl+C 검사를 켜거나 끄던 명령이지만, 현재 Windows 명령 프롬프트에서는 실질적인 효과가 없다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [40장: setlocal, endlocal](/post/cmd/setlocal-endlocal-command-variable-scope-windows-cmd/)에서 변수 유효 범위를 다룬 뒤 이어지며, Part 4(배치 스크립팅)의 마지막 장이다. 지금까지 11개 장이 실제로 동작하는 제어 구조였다면, 이 장은 예외적으로 "왜 이 명령이 사실상 아무것도 하지 않는가"를 이해하는 데 초점을 맞춘다.

**이 장의 깊이**: 입문. 레거시 명령이라 실무 활용도는 낮지만, CMD 명령 목록을 훑다 보면 반드시 마주치는 이름이므로 짧게 정리한다.

## 사용법

```
break=[on|off]
```

## 옵션

Microsoft Learn 최신 문서는 이 명령에 대해 다음과 같은 경고를 가장 먼저 제시한다.

> "This command is no longer in use. It is included only to preserve compatibility with existing MS-DOS files, but it has no effect at the command line because the functionality is automatic." — Microsoft Learn, "break"

즉 `on`/`off` 인수 자체는 여전히 받아들여지지만, 그 값이 실제 동작에 영향을 주지 않는다. 인수 없이 `break`만 실행하면 현재(무의미한) 설정 값을 표시한다.

## 예시

```
break
break on
break off
```

디버거로 배치 파일을 디버깅 중일 때는 조금 다른 의미를 갖는다.

> "If command extensions are enabled and running on the Windows platform, inserting the **break** command into a batch file enters a hard-coded breakpoint if being debugged by a debugger." — Microsoft Learn, "break"

즉 평소에는 아무 효과가 없지만, 디버거가 붙어 있는 상태라면 그 줄에서 강제로 실행을 멈추는 하드코딩된 중단점 역할을 한다.

## 주의사항·함정

**break는 아무 일도 하지 않는다는 특성 자체가 활용된다**: 아이러니하게도, "아무것도 하지 않는다"는 성질을 역이용해 파일을 만들거나 비우는 용도로 쓰이곤 한다.

```
rem -- cleans the content of the file --
break>log
```

`break`는 아무 출력도 생성하지 않지만, `>` 리다이렉션은 명령 실행 여부와 무관하게 대상 파일을 열어(없으면 생성, 있으면 비움) 그 자리에서 바로 닫는다. 그 결과 `break>log`는 log 파일을 0바이트로 만들거나 새로 생성하는 짧은 관용구로 쓰인다. `type nul>file`이나 `copy nul file`처럼 같은 목적의 다른 관용구도 있지만, break를 쓰는 것도 흔히 보이는 스타일 중 하나다.

**diskpart에도 같은 이름의 다른 명령이 있다**: Microsoft Learn 문서 체계에서 `break`라는 이름은 diskpart 대화형 셸 안에서 미러 볼륨을 두 개의 단순 볼륨으로 분리하는 완전히 다른 명령과 이름이 겹친다. CMD의 break(레거시 Ctrl+C 검사)와 diskpart의 break(미러 볼륨 분리, 44장에서 diskpart를 다룰 때 함께 언급한다)는 실행되는 맥락(cmd.exe 프롬프트 vs diskpart 프롬프트)이 다른, 완전히 무관한 명령이라는 점을 혼동하지 않아야 한다.

**PowerShell에는 진짜로 대응할 만한 명령이 없다**: 이 장의 CMD `break`가 cmd.exe에서는 아무 일도 하지 않는 레거시 명령이기 때문이다. 다만 이름이 같은 PowerShell의 `break` 키워드는 전혀 다른, 실제로 동작하는 기능이다 — 아래 흔한 오개념에서 이어서 다룬다.

## 흔한 오개념

<strong>"break on으로 설정하면 Ctrl+C 응답성이 실제로 달라진다"</strong>는 오해가 있다. MS-DOS 시절에는 디스크 I/O처럼 시간이 걸리는 작업 도중에도 Ctrl+C를 확인하도록 하는 실질적 스위치였지만, 현대 Windows에서는 이 검사가 항상 자동으로 이뤄지므로 `break on`/`break off`는 값만 저장할 뿐 실제 Ctrl+C 응답성에 아무 차이를 만들지 않는다.

<strong>"PowerShell의 break를 알면 CMD의 break 명령도 반복문을 빠져나가게 해줄 것이다"</strong>는 오해도 흔하다. PowerShell의 `break` 키워드는 `for`, `foreach`, `while` 같은 반복문을 즉시 빠져나가는, 실제로 활발히 쓰이는 제어 흐름 기능이다. 하지만 CMD의 `break` 명령은 이 장에서 다룬 대로 레거시 Ctrl+C 검사 설정일 뿐 반복문과는 아무 관계가 없다 — 애초에 CMD의 `for` 반복문 자체에는 중간에 빠져나가는 `break`에 해당하는 메커니즘이 없다. 두 `break`는 이름만 같을 뿐 기능적으로 완전히 무관하며, PowerShell 경험이 있는 사람일수록 오히려 이 이름의 우연한 일치에 걸리기 쉽다.

## 다음 장에서는

다음은 42장 — 디스크 오류를 검사하는 `chkdsk` 명령으로 Part 5(디스크와 파일 시스템 관리)가 시작된다.

## 평가 기준

- break가 현재 Windows에서 실질적인 효과가 없는 MS-DOS 호환용 레거시 명령이라는 것을 설명할 수 있다.
- 디버거가 붙어 있을 때 break가 하드코딩된 중단점으로 동작한다는 것을 안다.
- `break>file` 관용구가 왜 파일을 비우거나 생성하는 용도로 쓰이는지 설명할 수 있다.
- cmd.exe의 break와 diskpart의 break가 이름만 같을 뿐 무관한 명령이라는 것을 안다.

## 참고

- [break | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/break)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
