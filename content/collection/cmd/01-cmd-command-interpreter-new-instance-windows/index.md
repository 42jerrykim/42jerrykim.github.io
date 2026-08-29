---
draft: false
slug: cmd-command-interpreter-new-instance-windows
title: "[CMD] 01. cmd - 새 인스턴스 시작과 내부·외부 명령어"
description: "cmd.exe 새 인스턴스를 시작하는 cmd 명령의 /c·/k·/e·/v 스위치와 내부·외부 명령어 구분, 명령 확장, AutoRun 레지스트리 키, PowerShell과의 관계를 Microsoft Learn 기준으로 정리한 CMD 커리큘럼 1장이다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 10
categories:
- CMD
tags:
- Windows(윈도우)
- Shell(셸)
- Terminal
- Command
- Automation(자동화)
- Process
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- Troubleshooting(트러블슈팅)
- How-To
- Tips
- Beginner
- PowerShell
- Configuration(설정)
- Registry
- Batch
- cmd
- cmd.exe
- 명령프롬프트
- 내부명령어
- 외부명령어
- 명령확장
- Command-Extensions
- ERRORLEVEL
- Best-Practices
- Documentation(문서화)
image: "wordcloud.png"
---

cmd는 Windows 명령 인터프리터 cmd.exe의 새 인스턴스를 시작하는 명령이다. 인수 없이 실행하면 대화형 셸이 열리고, `/c` 또는 `/k`로 문자열을 넘기면 그 문자열을 명령으로 실행한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [00장: 과정 개요와 커리큘럼](/post/cmd/getting-started-cmd/)에서 다룬 9개 Part의 전체 지도를 전제로 시작한다. 이 장부터 <strong>Part 1(CMD 기초와 탐색)</strong>이 시작된다.

**이 장의 깊이**: 입문 난이도다. cmd 자체를 새 창에서 실행하는 문법과, 이후 모든 장에서 반복해 쓰일 "내부/외부 명령어" 구분·"명령 확장"이라는 두 개념을 다룬다. **다루지 않는 것**: 배치 파일 안에서 변수를 다루는 법은 31장(set) 이후 4부에서, 파이프·리다이렉션(`|`, `>`, `&&`) 연산자 자체의 상세 동작은 각 명령 챕터의 예시에서 필요할 때마다 짚는다. 이 장은 그 연산자들이 존재한다는 사실과 문법만 소개한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| CMD가 완전히 처음인 사람 | 개요+정신 모델, 사용법, 예시 | `cmd /c`와 `cmd /k`의 차이를 이해하고 새 CMD 창을 목적에 맞게 연다 |
| 배치 스크립트를 유지 보수해야 하는 사람 | 명령 확장·AutoRun 절, 주의사항·함정 | 기존 스크립트가 의존하는 명령 확장·지연된 변수 확장 설정을 읽고 판단한다 |

## 개요 + 정신 모델

cmd.exe는 Windows NT 계열에서 동작하는 하나의 독립된 프로세스다. "CMD 창을 연다"는 것은 사실 explorer.exe나 다른 부모 프로세스가 cmd.exe라는 새 자식 프로세스를 실행하는 것이고, 그 자식은 부모의 환경 변수를 그대로 물려받는다. Microsoft Learn은 이를 다음과 같이 설명한다.

> "In the command shell, each instance of `cmd` inherits the environment of its parent application. Therefore, you can change the variables in the new `cmd` environment without affecting the environment of the parent application." — Microsoft Learn, "cmd"

이 정신 모델이 중요한 이유는, CMD 창 안에서 `set` 명령으로 환경 변수를 바꿔도 그 창을 닫으면 변경 사항이 사라지는 이유를 설명해주기 때문이다 — 변경한 것은 상속받은 사본이지 원본이 아니다. 또한 CMD가 실행하는 명령은 두 종류로 나뉜다는 점도 이 장에서 짚어야 할 핵심 개념이다. `cd`·`dir`·`echo`·`set`처럼 cmd.exe 프로세스 안에 내장되어 별도 실행 파일 없이 처리되는 <strong>내부 명령어</strong>와, `xcopy.exe`·`robocopy.exe`처럼 `PATH` 상의 디렉터리에 실제 파일로 존재하는 <strong>외부 명령어</strong>다. `where dir`을 실행하면 파일을 찾지 못해 실패하지만 `where robocopy`는 실제 경로를 반환하는 것으로 이 구분을 직접 확인할 수 있다.

## 사용법

```
cmd [/c|/k] [/s] [/q] [/d] [/a|/u] [/t:{<b><f>|<f>}] [/e:{on|off}] [/f:{on|off}] [/v:{on|off}] [<문자열>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/c` | 문자열로 지정한 명령을 실행한 뒤 명령 처리기를 종료한다 |
| `/k` | 문자열로 지정한 명령을 실행한 뒤 명령 처리기를 계속 실행한다 |
| `/s` | `/c`·`/k`와 함께 쓰면 문자열 양 끝의 첫·마지막 따옴표만 제거하는 특수 파싱 규칙을 적용한다 |
| `/q` | 에코를 끈다 |
| `/d` | AutoRun 명령 실행을 비활성화한다 |
| `/a` \| `/u` | 출력 형식을 ANSI(`/a`) 또는 유니코드(`/u`)로 지정한다 |
| `/e:on`\|`off` | 명령 확장(command extensions)을 켜거나 끈다 |
| `/f:on`\|`off` | 파일·디렉터리 이름 자동 완성을 켜거나 끈다 |
| `/v:on`\|`off` | 지연된 환경 변수 확장(`!변수!`)을 켜거나 끈다 |

## 명령 확장과 AutoRun

`/e:off`로 명령 확장을 끄면 `assoc`, `call`, `cd`(`chdir`), `color`, `del`(`erase`), `endlocal`, `for`, `ftype`, `goto`, `if`, `md`(`mkdir`), `popd`, `prompt`, `pushd`, `set`, `setlocal`, `shift`, `start` 등 다수 명령의 확장 동작이 비활성화된다. 예를 들어 명령 확장이 켜져 있을 때 `cd`는 공백이 포함된 경로를 따옴표 없이 받아들이지만, 꺼져 있으면 반드시 따옴표가 필요하다 — 08장에서 이 차이를 실제로 확인한다. 명령 확장은 기본적으로 켜져 있고, 레지스트리의 `HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor\EnableExtensions`와 `HKEY_CURRENT_USER` 쪽 동일 키로 컴퓨터·사용자 단위 기본값을 바꿀 수 있다.

`/d`를 지정하지 않으면 cmd는 시작할 때마다 `HKEY_LOCAL_MACHINE\Software\Microsoft\Command Processor\AutoRun`과 `HKEY_CURRENT_USER` 쪽 동일 키를 확인해, 값이 있으면 다른 어떤 명령보다 먼저 실행한다. 조직에서 공유 스크립트나 보안 정책을 모든 CMD 세션에 강제로 적용할 때 이 메커니즘을 쓴다.

## 예시

```
cmd
cmd /c dir
cmd /k
start cmd /k "cd C:\Projects && dir"
cmd /v:on /c "set x=1 & if !x!==1 echo yes"
```

## 주의사항·함정

**`/c`와 `/k`를 혼동하면 스크립트가 멈춘 것처럼 보인다**: 배치 파일이나 CI 스크립트에서 서브셸을 한 번 실행하고 끝내려 했는데 실수로 `/k`를 쓰면, 명령 실행 후에도 창이 종료되지 않고 대화형 프롬프트로 남아 자동화 파이프라인이 그 자리에서 멈춘 것처럼 보인다. 한 번 실행하고 끝내는 용도에는 반드시 `/c`를 쓴다.

**특수문자는 인용해야 한다**: Microsoft Learn은 `& < > [ ] | { } ^ = ; ! ' + , `~ [공백]` 문자를 인용부호 없이 인자에 넣으면 안 된다고 명시한다.

> "You must use quotation marks around the following special characters: & &lt; &gt; [ ] | { } ^ = ; ! ' + , ` ~ [white space]." — Microsoft Learn, "cmd"

**PowerShell과의 관계**: Microsoft Learn 자체가 이 페이지에 "더 고급 기능이 필요하면 PowerShell을 검토하라"는 안내를 명시적으로 넣어 두었다.

> "Users seeking more advanced capabilities are encouraged to explore PowerShell for enhanced scripting and automation." — Microsoft Learn, "cmd"

이 컬렉션이 CMD를 다루는 이유는 이 안내와 모순되지 않는다 — 새로 자동화를 설계한다면 PowerShell을 우선 고려하되, 이미 존재하는 방대한 CMD 배치 자산을 읽고 고칠 줄 아는 능력은 여전히 필요하다는 것이 00장에서 밝힌 이 컬렉션의 전제다.

## 흔한 오개념

<strong>"명령 하나를 입력할 때마다 cmd.exe가 새로 뜬다"</strong>는 오해가 있다. 대화형 세션에서는 하나의 cmd.exe 프로세스가 계속 살아있는 상태로 명령을 순서대로 처리한다. 새 cmd.exe 프로세스가 뜨는 것은 `cmd` 명령으로 명시적으로 새 인스턴스를 요청했을 때, 또는 배치 파일을 이중 실행했을 때뿐이다.

<strong>"CMD 명령어는 실패하면 항상 화면에 에러가 보인다"</strong>는 오해도 흔하다. Microsoft Learn은 "명령이 성공하면 종료 코드 0을 반환하거나 종료 코드가 없다"고만 설명할 뿐, 실패 시 항상 화면에 에러가 표시된다고 보장하지 않는다 — 일부 외부 명령은 표준 에러로 조용히 실패하고, 이를 확인하려면 `%ERRORLEVEL%`을 직접 검사해야 한다. 이 주제는 4부(배치 스크립팅)에서 `if`와 함께 다시 다룬다.

## 다음 장에서는

다음은 02장 — CMD가 지원하는 명령을 스스로 찾아보는 `help` 명령을 다룬다.

## 평가 기준

- `cmd /c`와 `cmd /k`의 차이를 설명하고, 상황에 맞게 선택할 수 있다.
- 내부 명령어와 외부 명령어를 `where` 명령으로 구분할 수 있다.
- 명령 확장이 무엇이며, 확장이 꺼졌을 때 어떤 명령들의 동작이 달라지는지 설명할 수 있다.
- AutoRun 레지스트리 키가 어떤 상황에서 쓰이는지, `/d` 옵션이 왜 존재하는지 설명할 수 있다.
- 인용이 필요한 특수문자 목록을 알고, 인자에 특수문자가 섞인 명령을 안전하게 작성할 수 있다.

## 참고

- [cmd | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
