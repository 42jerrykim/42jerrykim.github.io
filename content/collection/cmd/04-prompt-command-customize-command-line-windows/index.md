---
draft: false
slug: prompt-command-customize-command-line-windows
title: "[CMD] 04. prompt - 프롬프트 표시 형식 변경"
description: "prompt 명령으로 CMD 프롬프트 문자열을 $p, $g, $t 등 메타 문자로 원하는 형식으로 바꾸는 법과 pushd 스택 깊이를 보여주는 $+, 네트워크 드라이브를 표시하는 $m까지 Microsoft Learn 기준 전체 메타 문자표로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 40
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
- prompt
- 프롬프트
- Customization
- Console
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Productivity(생산성)
- Configuration(설정)
- Workflow(워크플로우)
- Command-Extensions
- Education(교육)
- Tutorial(튜토리얼)
image: "wordcloud.png"
---

prompt는 명령을 입력하기 전에 표시되는 CMD 프롬프트 문자열을 원하는 형식으로 바꾸는 내장 명령이다. `$` 뒤에 오는 메타 문자를 조합해 경로·시간·날짜 등을 프롬프트에 끼워 넣는다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [03장: cls](/post/cmd/cls-command-clear-screen-windows-cmd/)에서 화면 자체를 다룬 뒤 이어진다. 이 장부터는 화면에 무엇을 지우느냐가 아니라 무엇을 어떻게 보여주느냐로 초점이 옮겨간다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 콘솔 창의 색상을 바꾸는 것은 71장(color)에서, 창 제목을 바꾸는 것은 05장(title)에서 각각 별도로 다룬다. prompt는 오직 명령 입력줄 앞에 붙는 문자열만 다룬다.

## 사용법

```
prompt [<텍스트>]
```

인수 없이 `prompt`만 실행하면 기본값(`$p$g`, 즉 현재 드라이브·경로 뒤에 `>`)으로 복원된다.

## 옵션 — 메타 문자표

| 문자 | 의미 |
|---|---|
| `$q` | `=` (등호) |
| `$$` | `$` (달러 기호) |
| `$t` | 현재 시간 |
| `$d` | 현재 날짜 |
| `$p` | 현재 드라이브와 경로 |
| `$v` | Windows 버전 번호 |
| `$n` | 현재 드라이브 |
| `$g` | `>` (초과 기호) |
| `$l` | `<` (미만 기호) |
| `$b` | `|` (파이프 기호) |
| `$_` | 줄바꿈 |
| `$e` | ANSI 이스케이프 코드(27) |
| `$h` | 백스페이스(직전 문자 삭제) |
| `$a` | `&` (앰퍼샌드) |
| `$c` | `(` (왼쪽 괄호) |
| `$f` | `)` (오른쪽 괄호) |
| `$s` | 공백 |

명령 확장이 켜져 있으면(01장 참고) 다음 두 문자도 추가로 지원된다.

| 문자 | 의미 |
|---|---|
| `$+` | [11장: pushd, popd](/post/cmd/pushd-popd-command-directory-stack-windows-cmd/)로 쌓은 디렉터리 스택의 깊이만큼 `+` 문자를 표시 |
| `$m` | 현재 드라이브가 네트워크 드라이브면 그 원격 이름을, 아니면 빈 문자열을 표시 |

## 예시

```
prompt $p$g
prompt [$t] $p$g
prompt --$g
prompt $p$+$g
prompt
```

세 번째 예시(`prompt --$g`)는 프롬프트를 `-->` 형태의 화살표로 바꾼다. 네 번째 예시는 `$+`를 더해 현재 pushd 스택 깊이를 프롬프트에서 바로 확인할 수 있게 한다 — 11장에서 배울 디렉터리 스택을 대화형으로 추적할 때 유용하다.

## 주의사항·함정

**세션 범위**: prompt로 바꾼 형식은 그 CMD 세션에만 적용되고 창을 닫으면 사라진다. 매번 같은 프롬프트를 쓰고 싶다면 배치 파일이나 AutoRun 레지스트리 키(01장 참고)에 `prompt` 명령을 넣어야 한다.

**`$p`는 디스크 접근 비용이 있다**: Microsoft Learn은 `$p`를 쓰면 매 명령마다 디스크를 읽어 현재 드라이브·경로를 확인한다고 명시한다.

> "If you include the **$p** character in the text parameter, your disk is read after you enter each command (to determine the current drive and path). This can take extra time, especially for floppy disk drives." — Microsoft Learn, "prompt"

플로피 디스크 시절 남은 경고이긴 하지만, 네트워크 드라이브를 프롬프트에 자주 포함시키는 구성에서는 지금도 체감할 수 있는 지연으로 이어질 수 있다.

**PowerShell은 메타 문자가 아니라 함수로 프롬프트를 정의한다**: PowerShell에서 프롬프트를 바꾸는 방식은 CMD의 `$` 메타 문자 치환과 근본적으로 다르다. `$PROFILE` 스크립트에 문자열을 반환하는 `function prompt { ... }`를 정의하면 그 반환값이 매번 프롬프트로 쓰인다. 즉 CMD의 prompt가 고정된 메타 문자 조합을 해석하는 치환 방식이라면, PowerShell은 조건문이나 외부 명령 호출까지 담을 수 있는 함수 실행 방식이라 표현력의 범위 자체가 다르다.

## 흔한 오개념

<strong>"prompt는 배치 파일 실행에는 영향을 주지 않는다"</strong>는 생각은 절반만 맞다. prompt 자체는 화면 표시 형식만 바꾸므로 배치 파일의 로직에는 영향이 없지만, `@echo off`가 걸린 배치 파일이라도 그 안에서 `prompt` 명령을 실행하면 이후 대화형 프롬프트로 돌아왔을 때의 형식이 바뀐 채로 남는다. 배치 파일 안에서 일시적으로 프롬프트를 바꿨다면 스크립트 끝에서 원래 값으로 복원하거나, 40장(setlocal, endlocal)의 환경 범위 안에서 실행해 자동으로 되돌아가게 하는 편이 안전하다.

## 다음 장에서는

다음은 05장 — 프롬프트가 아니라 CMD 창 자체의 제목 표시줄을 바꾸는 `title` 명령을 다룬다.

## 평가 기준

- `$p`, `$g`, `$t`, `$d` 등 자주 쓰는 메타 문자를 조합해 원하는 프롬프트 형식을 직접 만들 수 있다.
- `$+`, `$m`처럼 명령 확장이 켜져 있을 때만 동작하는 메타 문자가 있다는 것을 안다.
- prompt 설정이 세션 범위라는 것과, 영구 적용을 위해 무엇이 필요한지 설명할 수 있다.
- `$p`가 디스크 접근을 유발할 수 있다는 성능상 함정을 설명할 수 있다.

## 참고

- [prompt | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/prompt)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
