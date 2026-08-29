---
draft: false
slug: for-command-loop-batch-windows-cmd
title: "[CMD] 33. for - 파일·디렉터리·숫자 범위 반복"
description: "for로 파일 집합, 디렉터리(/d), 재귀 순회(/r), 숫자 범위(/l), 명령 출력 파싱(/f)을 반복 처리하는 법과 대화형에서는 %, 배치 파일에서는 %%를 써야 하는 규칙, 경로 변형 수식어(%~dpI 등)를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 330
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
- Advanced
- for
- 반복문
- Loop
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Education(교육)
- CLI
- Comparison(비교)
- Command-Extensions
- Beginner
- Configuration(설정)
- Administration
image: "wordcloud.png"
---

for는 파일 집합, 디렉터리, 문자열 목록, 숫자 범위, 명령 출력을 반복 처리하는 내장 명령이다. CMD 배치 스크립팅에서 가장 다재다능하면서도 가장 문법이 복잡한 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [32장: if](/post/cmd/if-command-conditional-batch-windows-cmd/)에서 조건 분기를 다룬 뒤 이어진다. if가 "한 번 검사해 분기"였다면, for는 "여러 항목에 대해 같은 작업을 반복"한다 — 두 제어 구조가 합쳐지면 대부분의 배치 스크립트 로직을 표현할 수 있다.

**이 장의 깊이**: 중급–고급. `/f` 옵션은 특히 복잡하므로 예제 위주로 다룬다. **다루지 않는 것**: `for`로 반복하는 대상이 될 파일 목록·명령 출력 자체를 만드는 방법(dir, findstr 등)은 이미 앞선 장들에서 다뤘다.

## 개요 + 정신 모델

for의 다섯 가지 형태(기본, `/d`, `/r`, `/l`, `/f`)는 모두 "집합을 순회하며 변수를 하나씩 치환한다"는 같은 뼈대를 공유하고, `/d`·`/r`·`/l`·`/f`는 그 집합을 어떻게 만드는지만 바꾼다. 기본형은 와일드카드로 파일 집합을 만들고, `/d`는 파일 대신 디렉터리를, `/r`은 디렉터리 트리를 재귀적으로, `/l`은 숫자 시퀀스를, `/f`는 파일 내용·명령 출력·문자열을 줄 단위로 쪼갠 토큰을 집합으로 삼는다.

## 사용법

```
for {%%|%}<변수> in (<집합>) do <명령> [<명령줄옵션>]
for /d {%%|%}<변수> in (<집합>) do <명령>
for /r [[<드라이브>:]<경로>] {%%|%}<변수> in (<집합>) do <명령>
for /l {%%|%}<변수> in (<시작>,<증가>,<끝>) do <명령>
for /f [<파싱옵션>] {%%|%}<변수> in (<집합>) do <명령>
```

## 옵션

### 형태

| 형태 | 대상 |
|---|---|
| 기본 | 지정한 집합(파일·문자열) |
| `/d` | 디렉터리만(집합에 와일드카드가 있으면) |
| `/r [경로]` | 지정 경로(생략 시 현재 디렉터리)부터 재귀적으로 모든 하위 디렉터리 순회 |
| `/l` | `(시작,증가,끝)` 형태의 숫자 시퀀스. 증가값이 음수면 감소 |
| `/f` | 파일 내용, 명령 출력(백틱), 리터럴 문자열(따옴표)을 줄 단위로 파싱 |

### `/f` 파싱 옵션

| 키워드 | 설명 |
|---|---|
| `eol=<c>` | 줄 끝(주석 처리) 문자 지정 |
| `skip=<n>` | 파일 앞부분 n줄 건너뜀 |
| `delims=<xxx>` | 구분자 집합 지정(기본은 공백·탭) |
| `tokens=<x,y,m-n>` | 각 줄에서 몇 번째 토큰을 변수로 받을지 지정. 마지막이 `*`면 나머지 전체를 추가 변수로 |
| `usebackq` | 백틱 문자열을 명령으로, 작은따옴표 문자열을 리터럴로, 공백 있는 파일명을 큰따옴표로 감싸 지정 |

### 변수 치환 수식어(변수 I 기준)

| 수식어 | 결과 |
|---|---|
| `%~I` | 둘러싼 따옴표 제거 |
| `%~fI` | 정규화된 전체 경로 |
| `%~dI` | 드라이브 문자만 |
| `%~pI` | 경로만 |
| `%~nI` | 파일 이름만(확장자 제외) |
| `%~xI` | 확장자만 |
| `%~zI` | 파일 크기 |
| `%~tI` | 날짜·시간 |
| `%~dpI` | 드라이브+경로 |
| `%~nxI` | 이름+확장자 |
| `%~$PATH:I` | PATH에서 검색해 처음 찾은 전체 경로 |

## 예시

```
for %f in (*.doc *.txt) do type %f
for /d %d in (C:\*) do @echo %d
for /r "C:\My Dir\" %A in (*.*) do echo %~ftzA
for /l %i in (1,1,10) do echo %i
for /f "eol=; tokens=2,3* delims=," %i in (myfile.txt) do @echo %i %j %k
for /f "usebackq delims==" %i in (`set`) do @echo %i
```

배치 파일 안에서는 모든 `%f`, `%d`, `%A`, `%i`를 `%%f`, `%%d`, `%%A`, `%%i`로 두 배 써야 한다.

```bat
for %%f in (*.txt) do echo %%f
```

## 주의사항·함정

**대화형과 배치 파일의 변수 표기가 다르다**: 이 장에서 가장 먼저 걸리는 함정이다. 명령 프롬프트에서 직접 입력할 때는 `%f` 한 글자로 충분하지만, 배치 파일(`.bat`/`.cmd`) 안에 같은 명령을 넣으면 `%%f`로 두 배 써야 한다.

> "Use a single percent sign (`%`) to carry out the **for** command at the command prompt. Use double percent signs (`%%`) to carry out the **for** command within a batch file." — Microsoft Learn, "for"

이를 지키지 않으면(배치 파일에 `%f`만 씀) 변수가 무시되고 오류 메시지가 표시된다.

**변수 이름은 대소문자를 구분하고, 최대 52개까지 활성화할 수 있다**: `%a`와 `%A`는 서로 다른 변수로 취급된다. 또한 숫자(`0`–`9`)는 배치 매개변수(`%0`–`%9`)와 겹치므로 for 변수 이름으로 쓸 수 없다.

**`/f`는 기본적으로 첫 토큰만 넘긴다**: `tokens=` 옵션 없이 `/f`를 쓰면 각 줄의 첫 번째 공백 구분 토큰만 변수에 담긴다. 여러 필드를 다루려면 `tokens=1,2,3`처럼 명시해야 하고, 명시한 토큰 수만큼 `%i`부터 알파벳 순서로 추가 변수(`%j`, `%k`, ...)가 암묵적으로 할당된다.

**공백이 있는 파일명은 `usebackq`가 필요하다**: `usebackq` 없이 파일명을 큰따옴표로 감싸면, 그 따옴표는 "리터럴 문자열을 파싱하라"는 의미로 해석되어 파일이 아니라 그 문자열 자체를 파싱하게 된다. 공백이 있는 경로를 다루려면 반드시 `usebackq`를 함께 써야 한다.

**`for /f`로 명령 출력을 파싱하면 자식 프로세스가 뜬다**: 백틱으로 감싼 명령은 별도의 자식 cmd.exe로 실행되어 그 출력이 메모리에 캡처된 뒤 파일처럼 파싱된다. 무거운 명령을 반복문 안에서 이런 식으로 여러 번 호출하면 예상보다 느려질 수 있다.

**괄호로 묶은 반복 블록 안에서 변수를 갱신하며 같은 블록에서 참조하면 옛 값만 보인다**: CMD는 `do (...)` 블록 전체를 실행 전에 한 번에 읽어 그 시점에 `%변수%` 자리를 미리 치환해버린다. 그래서 반복마다 값이 바뀌는 변수를 같은 블록 안에서 `%변수%`로 읽으면, 매 반복의 최신 값이 아니라 블록에 처음 진입하기 전의 값만 보인다.

```bat
setlocal
set sum=0
for /l %%i in (1,1,3) do (
  set /a sum+=%%i
  echo %sum%
)
```

이 스크립트는 `1`, `2`, `3`이 아니라 **`0`을 세 번** 출력한다 — `%sum%`이 `for` 문 전체가 파싱되는 시점(반복이 시작되기도 전)의 값인 `0`으로 이미 고정되어버렸기 때문이다. `set /a sum+=%%i`는 실제로 매 반복마다 값을 누적하고 있지만, 같은 블록 안의 `%sum%`은 그 갱신을 반영하지 못한다.

이 문제는 40장(setlocal)에서 다루는 `setlocal enabledelayedexpansion`을 켜고 `%sum%` 대신 `!sum!`(느낌표로 감싼 지연 확장 변수)을 쓰면 해결된다.

```bat
setlocal enabledelayedexpansion
set sum=0
for /l %%i in (1,1,3) do (
  set /a sum+=%%i
  echo !sum!
)
```

이번엔 반복마다 최신 값이 실제로 갱신되어 `1`, `3`, `6`이 정확히 출력된다. 이 함정은 `for`뿐 아니라 `if`의 괄호 블록에서도 똑같이 나타난다 — 32장(if)의 주의사항·함정에서 같은 문제를 조건문 맥락으로 다시 다룬다.

**PowerShell은 반복문 자체가 더 다양하고, `%`/`%%` 구분이 없다**: `for`, `foreach`, 파이프라인 기반의 `ForEach-Object`까지 여러 반복 구문을 상황에 맞게 골라 쓸 수 있다. 그리고 CMD처럼 대화형 프롬프트에서는 `%변수`, 배치 파일 안에서는 `%%변수`로 표기를 바꿔야 하는 규칙 자체가 없다 — PowerShell은 스크립트로 저장해 실행하든 콘솔에 한 줄씩 입력하든 항상 같은 `$변수` 문법을 쓴다. 이 장 초반에 다룬 "가장 먼저 걸리는 함정"이 PowerShell에는 애초에 존재하지 않는 셈이다.

## 흔한 오개념

<strong>"for /f는 항상 공백으로만 필드를 나눈다"</strong>는 오해가 있다. 기본 구분자는 공백·탭이지만 `delims=`로 임의의 문자 집합(쉼표, 세미콜론 등)을 지정할 수 있다. CSV 파일을 파싱할 때 `delims=,`를 빠뜨리면 쉼표가 구분자로 인식되지 않아 한 줄 전체가 하나의 토큰으로 잡히는 실수를 자주 한다.

## 다음 장에서는

다음은 34장 — 다른 배치 파일이나 같은 파일 안의 레이블을 서브루틴처럼 호출하는 `call` 명령을 다룬다.

## 평가 기준

- 기본형·`/d`·`/r`·`/l`·`/f` 다섯 형태의 차이를 설명하고 상황에 맞게 선택할 수 있다.
- 대화형에서는 `%`, 배치 파일에서는 `%%`를 써야 하는 이유를 설명할 수 있다.
- `/f`의 `tokens=`, `delims=`, `usebackq` 옵션을 조합해 구조화된 텍스트를 파싱할 수 있다.
- `%~dpI`, `%~nxI` 같은 경로 변형 수식어를 활용할 수 있다.

## 참고

- [for | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/for)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
