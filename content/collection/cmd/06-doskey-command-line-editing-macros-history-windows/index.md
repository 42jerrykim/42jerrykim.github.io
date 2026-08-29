---
draft: false
slug: doskey-command-line-editing-macros-history-windows
title: "[CMD] 06. doskey - 명령줄 편집과 매크로"
description: "doskey로 명령 히스토리를 불러오고, F7 등 편집 키를 활용하고, $1-$9·$*로 인자를 받는 매크로를 만드는 법을 정리합니다. 매크로가 배치 파일에서는 실행되지 않는다는 핵심 함정을 Microsoft Learn 기준으로 다룹니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 60
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
- Advanced
- doskey
- 매크로
- 히스토리
- Command-Line
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Productivity(생산성)
- Configuration(설정)
- Workflow(워크플로우)
- Comparison(비교)
- PowerShell
- Education(교육)
- CLI
image: "wordcloud.png"
---

doskey는 명령줄 히스토리(과거 명령 불러오기), 명령줄 편집, 매크로(단축 명령) 정의를 관리하는 명령이다. Microsoft Learn은 이를 "Doskey.exe를 호출해 이전에 입력한 명령줄 명령을 다시 불러오고, 명령줄을 편집하고, 매크로를 만든다"고 정의한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [05장: title](/post/cmd/title-command-set-console-window-title-windows/)에서 창 표시를 다룬 뒤 이어진다. doskey는 Part 1에서 가장 다루는 범위가 넓은 명령이다 — 08장(cd)·09장(dir) 등 이후 자주 쓰게 될 명령을 매크로로 줄여 쓰는 법을 미리 익혀두면 이어지는 장의 예시를 더 빠르게 반복 실습할 수 있다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 배치 파일 자체의 반복 실행 문법(`for`, `call`)은 4부에서 다룬다. doskey 매크로는 대화형 세션 전용이라는 점이 이 장의 핵심이며, 그 이유는 아래 "주의사항·함정"에서 설명한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 반복 입력을 줄이고 싶은 사람 | 개요, 매크로 정의 예시 | 자주 쓰는 명령을 매크로로 등록해 대화형 세션에서 타이핑을 줄인다 |
| 과거 명령을 스크립트로 재활용하려는 사람 | `/history`, `/macros` 절 | 히스토리·매크로 목록을 파일로 뽑아 배치 초안으로 활용한다 |

## 사용법

```
doskey [/reinstall] [/listsize=<크기>] [/macros:[all|<실행파일이름>]] [/history] [/insert|/overstrike] [/exename=<실행파일이름>] [/macrofile=<파일이름>] [<매크로이름>=[<텍스트>]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/reinstall` | Doskey.exe를 새로 설치하고 명령 히스토리 버퍼를 초기화 |
| `/listsize=<크기>` | 히스토리 버퍼에 저장할 최대 명령 수 지정 |
| `/macros`(약칭 `/m`) | 현재 정의된 모든 매크로 표시. `>`로 파일에 리다이렉션 가능 |
| `/macros:all` | 모든 실행 파일에 대한 매크로 표시 |
| `/history`(약칭 `/h`) | 메모리에 저장된 모든 명령 표시. `>`로 파일에 리다이렉션 가능 |
| `/insert` \| `/overstrike` | 새 텍스트를 기존 텍스트 사이에 삽입할지, 덮어쓸지 지정 |
| `/exename=<실행파일이름>` | 매크로가 적용될 프로그램(exe)을 지정 |
| `/macrofile=<파일이름>` | 파일에 저장된 매크로 정의를 불러와 설치 |
| `<매크로이름>=[<텍스트>]` | 매크로 정의. 텍스트를 비우면 해당 매크로 삭제 |

### 명령 불러오기 키

| 키 | 동작 |
|---|---|
| ↑ | 바로 이전에 쓴 명령 불러오기 |
| ↓ | 그 다음 명령 불러오기 |
| Page Up | 현재 세션에서 가장 처음 쓴 명령 |
| Page Down | 현재 세션에서 가장 최근 쓴 명령 |
| F7 | 저장된 모든 명령을 대화 상자로 표시 |
| F8 | 현재까지 입력한 문자로 시작하는 히스토리만 표시 |
| Alt+F7 | 현재 히스토리 버퍼 전체 삭제 |

### 매크로 정의용 특수 문자

| 문자 | 의미 |
|---|---|
| `$G` / `$g` | 출력 리다이렉션(`>`) |
| `$G$G` / `$g$g` | 출력 추가 리다이렉션(`>>`) |
| `$L` / `$l` | 입력 리다이렉션(`<`) |
| `$B` / `$b` | 파이프(`\|`) |
| `$T` / `$t` | 매크로 안에서 명령 구분(`&`에 대응) |
| `$$` | `$` 문자 자체 |
| `$1`–`$9` | 매크로 실행 시 넘길 개별 인자(배치 파일의 `%1`에 대응) |
| `$*` | 매크로 이름 뒤에 입력한 나머지 전체를 그대로 치환 |

## 예시

```
doskey /history
doskey ls=dir $*
doskey up=cd ..
doskey mc=md $1$tcd $1
doskey /macrofile=mymacros.txt
doskey /macros > macinit.txt
doskey vlist=
```

`mc` 매크로는 `$t`로 두 명령(`md`, `cd`)을 이어 붙여, 디렉터리를 만들고 그 안으로 바로 이동하는 동작을 한 번에 수행한다. 마지막 예시(`doskey vlist=`)처럼 텍스트를 비운 채 정의하면 해당 매크로가 삭제된다.

## 주의사항·함정

**매크로는 배치 파일에서 실행할 수 없다**: 이 장의 가장 중요한 함정이다. Microsoft Learn은 이를 명확히 못박는다.

> "You cannot run a **doskey** macro from a batch program." — Microsoft Learn, "doskey"

doskey 매크로는 대화형 명령줄 버퍼에서만 동작하는 편의 기능이지, 배치 스크립팅 도구가 아니다. 반복되는 명령 조합을 배치 파일 안에서 재사용하고 싶다면 doskey 매크로가 아니라 4부에서 다룰 배치 파일 함수 패턴(`call :레이블`)이나 별도의 `.bat` 파일을 만들어야 한다.

**매크로가 내장 명령과 이름이 같으면 매크로가 우선한다**: 매크로 이름을 내장 명령과 똑같이 지으면 해당 세션에서는 원래 명령 대신 매크로가 실행된다. 원래 명령을 실행하려면 이름 앞에 공백을 하나 이상 넣어야 하는데, 이 규칙을 모르면 왜 명령이 다르게 동작하는지 혼란스러울 수 있다.

**세션 종료 시 사라진다**: CMD 창을 닫으면 매크로와 히스토리 버퍼는 모두 사라진다. 영구적으로 쓰려면 로그온 스크립트나 AutoRun 레지스트리 키(01장 참고)에서 `doskey /macrofile=...`을 실행하도록 설정해야 한다.

**PowerShell에는 대응 기능이 다르게 존재한다**: PowerShell은 doskey 대신 PSReadLine 모듈이 명령줄 편집·히스토리를 담당하고, 매크로에 해당하는 개념은 함수나 별칭(`Set-Alias`)으로 구현한다. CMD의 doskey 매크로 문법을 PowerShell 프로필에 그대로 옮겨 쓸 수는 없다.

## 흔한 오개념

<strong>"한 CMD 창에서 만든 doskey 매크로는 새로 여는 다른 CMD 창에도 자동으로 적용된다"</strong>는 오해가 있다. 매크로와 히스토리 버퍼는 그것을 정의한 그 CMD 프로세스에만 유효하다. 이미 열려 있는 창에서 `doskey ls=dir $*`를 실행한 뒤 새 CMD 창을 하나 더 열어보면, 그 새 창은 매크로가 하나도 없는 빈 상태로 시작한다는 것을 바로 확인할 수 있다. 여러 창에서 같은 매크로를 쓰려면 `/macrofile`로 각 세션마다 다시 불러오거나, 로그온 스크립트·AutoRun에 등록해 창을 열 때마다 자동 실행되게 해야 한다.

## 다음 장에서는

다음은 07장 — 명령어가 어디서 실행되는지를 결정하는 `path` 명령을 다룬다.

## 평가 기준

- doskey로 매크로를 정의하고, `$1`–`$9`·`$*`로 인자를 받는 매크로를 작성할 수 있다.
- 명령 히스토리를 불러오는 키(↑/↓, F7, F8)의 차이를 설명할 수 있다.
- doskey 매크로가 배치 파일에서는 실행되지 않는다는 것과, 그 대신 무엇을 써야 하는지 설명할 수 있다.
- 매크로 이름이 내장 명령과 겹칠 때 어떤 것이 우선하는지, 원래 명령을 실행하려면 어떻게 해야 하는지 안다.

## 참고

- [doskey | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/doskey)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
