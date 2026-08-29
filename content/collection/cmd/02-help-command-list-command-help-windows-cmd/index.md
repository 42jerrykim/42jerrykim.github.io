---
draft: false
slug: help-command-list-command-help-windows-cmd
title: "[CMD] 02. help - 명령어 도움말 조회"
description: "help 명령으로 CMD 내장 명령 목록과 개별 명령의 상세 도움말을 조회하는 법, help와 명령어 /? 의 관계, 외부 실행 파일에는 통하지 않는 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 20
categories:
- CMD
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- Command
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- How-To
- Tips
- Beginner
- Documentation(문서화)
- PowerShell
- Troubleshooting(트러블슈팅)
- help
- 도움말
- 명령어목록
- CLI
- Command-Line
- Best-Practices
- Education(교육)
- Productivity(생산성)
- Configuration(설정)
- Comparison(비교)
- Workflow(워크플로우)
- Automation(자동화)
image: "wordcloud.png"
---

help는 CMD가 지원하는 명령 목록을 보여주거나, 지정한 명령의 상세 도움말을 표시하는 내장 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [01장: cmd](/post/cmd/cmd-command-interpreter-new-instance-windows/)에서 CMD 자체를 새 인스턴스로 시작하는 법과 내부·외부 명령어 구분을 다룬 뒤 이어진다. 그 구분을 알아야 이번 장의 "왜 help가 모든 명령에 통하지는 않는가"를 이해할 수 있다.

**이 장의 깊이**: 입문 난이도의 짧은 장이다. **다루지 않는 것**: 개별 명령의 구체적인 옵션은 각 명령의 해당 챕터에서 다룬다. 이 장은 "도움말을 찾는 방법" 자체에만 집중한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 지금 당장 명령 옵션이 궁금한 사람 | 사용법, 예시 | `help 명령이름` 또는 `명령이름 /?`로 바로 답을 찾는다 |
| CMD 도움말 체계 자체를 이해하려는 사람 | 전체 | help와 `/?`의 관계, 외부 프로그램에서 통하지 않는 이유까지 이해한다 |

## 개요 + 정신 모델

help는 CMD 내장 명령에 대한 도움말을 표준화된 형식으로 출력하는 조회 도구다. Microsoft Learn은 이를 다음과 같이 정의한다.

> "Displays a list of the available commands or detailed help information on a specified command. If used without parameters, **help** lists and briefly describes every system command." — Microsoft Learn, "help"

정신 모델로 보면 help는 새로운 정보원이 아니라, 각 내장 명령이 `/?` 스위치로 이미 제공하는 도움말을 목록형으로 한 번 더 감싼 것에 가깝다. 즉 `help copy`와 `copy /?`는 사실상 같은 정보를 보여준다 — 01장에서 배운 "내부 명령어" 개념이 여기서 다시 등장한다. help가 다루는 대상은 cmd.exe에 내장된 명령들이지, PATH 상의 임의의 .exe 파일이 아니다.

## 사용법

```
help [<명령이름>]
```

## 옵션

| 사용 | 설명 |
|---|---|
| `help` | 도움말이 제공되는 모든 명령을 목록으로 표시 |
| `help <명령이름>` | 지정한 명령의 상세 도움말 표시 |

## 예시

```
help
help robocopy
dir /?
help create partition primary
```

마지막 예시처럼 `diskpart`처럼 자체 대화형 프롬프트를 가진 도구 안에서도 `help` 명령으로 해당 도구 전용 하위 명령의 도움말을 조회할 수 있다(44장에서 diskpart를 다룰 때 이 패턴을 다시 사용한다).

## 주의사항·함정

**외부 프로그램에는 통하지 않을 수 있다**: help는 cmd.exe에 내장된 명령을 대상으로 하므로, `robocopy.exe`처럼 PATH 상의 실행 파일로 존재하는 외부 명령어는 `help robocopy`로 조회는 되지만 실제로는 그 프로그램이 자체적으로 `/?`를 구현한 결과를 보여주는 것이다. 반면 완전히 CMD와 무관한 서드파티 프로그램은 `help`나 `/?`가 아예 통하지 않을 수 있고, 그럴 때는 해당 프로그램의 `--help`나 `-h` 같은 자체 관례를 따라야 한다.

**PowerShell에는 대응 명령이 다르다**: PowerShell에서 명령(cmdlet)의 도움말을 보려면 `Get-Help <cmdlet이름>`을 쓴다. CMD의 `help`나 `/?` 문법을 PowerShell 세션에 그대로 입력하면 인식되지 않거나 다른 결과가 나온다.

## 흔한 오개념

<strong>"`help`만 입력하면 시스템에서 쓸 수 있는 모든 명령이 목록에 나온다"</strong>는 오해가 있다. 인수 없이 실행한 `help`가 보여주는 목록은 cmd.exe에 내장된 명령들의 개요일 뿐이며, `robocopy`처럼 PATH 상에 존재하는 외부 실행 파일은 이 목록에 나타나지 않는다. `help robocopy`처럼 이름을 직접 지정하면 그 프로그램이 자체 구현한 `/?` 결과가 나올 수도 있지만, 그렇다고 그 명령이 `help` 단독 실행 시 뜨는 전체 목록에 포함되는 것은 아니다.

## 다음 장에서는

다음은 03장 — 화면을 정리하는 가장 단순한 내장 명령 `cls`를 다룬다.

## 평가 기준

- `help`, `help <명령이름>`, `<명령이름> /?` 세 가지 조회 방법의 관계를 설명할 수 있다.
- help가 내장 명령을 대상으로 한다는 점과, 외부 프로그램에는 통하지 않을 수 있는 이유를 설명할 수 있다.
- PowerShell에서 동일한 목적을 위해 `Get-Help`를 쓴다는 것을 안다.

## 참고

- [help | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/help)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
