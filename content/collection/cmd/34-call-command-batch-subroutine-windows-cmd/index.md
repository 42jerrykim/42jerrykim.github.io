---
draft: false
slug: call-command-batch-subroutine-windows-cmd
title: "[CMD] 34. call - 배치 파일과 레이블 호출"
description: "call로 다른 배치 파일이나 같은 파일 안의 레이블을 서브루틴처럼 호출하는 법과 call 없이 배치 파일을 부르면 돌아오지 않는 함정, 재귀 호출 시 종료 조건이 필수인 이유, call과 파이프·리다이렉션을 함께 쓰면 안 되는 제약을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 340
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
- call
- 서브루틴
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Education(교육)
- CLI
- Comparison(비교)
- Recursion
- Beginner
- Configuration(설정)
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

call은 다른 배치 프로그램(또는 같은 파일 안의 레이블)을 호출하고, 그 실행이 끝나면 호출한 배치 프로그램을 멈추지 않고 이어서 실행하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [33장: for](/post/cmd/for-command-loop-batch-windows-cmd/)에서 반복을 다룬 뒤 이어진다. if(분기)와 for(반복)에 이어, call은 코드를 재사용 가능한 단위로 나누는 세 번째 제어 구조다.

**이 장의 깊이**: 중급. **다루지 않는 것**: 레이블 자체로 이동만 하고 돌아오지 않는 것은 35장(goto)에서 다룬다. call은 "호출 후 복귀"에, goto는 "단순 점프"에 각각 대응한다.

## 사용법

```
call [<드라이브>:][<경로>]<파일이름> [<배치인수>]
call [:<레이블> [<인수>]]
```

`<파일이름>`은 반드시 `.bat` 또는 `.cmd` 확장자를 가진 파일이어야 한다.

## 옵션

명령 프롬프트에서 직접 실행하면 call은 아무 효과가 없다 — 스크립트나 배치 파일 안에서만 의미가 있다.

## 예시

```
call checknew
call checknew %1 %2
call scripts\setup.cmd arg1 arg2
call :subroutine 100
```

레이블을 호출하는 패턴은 CMD에서 함수에 가장 가까운 표현이다.

```bat
@echo off
call :greet World
call :greet CMD
goto :eof

:greet
echo Hello, %~1!
goto :eof
```

## 주의사항·함정

**call 없이 다른 배치 파일을 실행하면 돌아오지 않는다**: 배치 파일 이름만 그대로 쓰면(`other.bat`), 현재 배치의 실행이 그 파일로 완전히 넘어가고 other.bat이 끝나도 원래 배치로 복귀하지 않는다. 호출 후 원래 위치로 돌아와 이어서 실행하려면 반드시 `call`을 붙여야 한다.

**레이블 호출은 새 배치 컨텍스트를 만든다**: `call :레이블`로 레이블을 호출하면, 그 지점부터 새로운 배치 파일 컨텍스트가 시작된다.

> "By using **call** with the `<label>` parameter, you create a new batch file context and pass control to the statement after the specified label. The first time the end of the batch file is encountered (that is, after jumping to the label), control returns to the statement after the **call** statement. The second time the end of the batch file is encountered, the batch script is exited." — Microsoft Learn, "call"

즉 파일 끝(또는 `goto :eof`)에 처음 도달하면 호출한 위치로 돌아오고, 그다음에 다시 파일 끝에 도달하면(더 이상 호출부가 없으므로) 배치 전체가 종료된다. 이 "두 번째 끝"이라는 개념이 익숙하지 않으면 `call :subroutine` 뒤에 `goto :eof`를 왜 넣어야 하는지 이해하기 어렵다.

**재귀 호출은 반드시 종료 조건이 있어야 한다**: 배치 파일이 자기 자신을 call로 호출하는 것은 가능하지만, 종료 조건 없이 재귀하면 부모와 자식이 무한히 루프를 돈다.

> "You can create a batch program that calls itself. However, you must provide an exit condition. Otherwise, the parent and child batch programs can loop endlessly." — Microsoft Learn, "call"

**파이프·리다이렉션과 함께 쓰면 안 된다**: Microsoft Learn은 call에 `|`, `<`, `>`를 함께 쓰지 말라고 명시적으로 경고한다. 출력을 리다이렉션하려면 call로 실행되는 명령 자체보다는 그 결과를 담은 배치 파일 안에서 처리하거나, call 문 전체를 감싸는 바깥쪽에서 리다이렉션해야 한다.

**`exit /b`로 종료 코드를 돌려받을 수 있다**: 호출된 배치가 `exit /b <코드>`로 끝나면, 그 코드는 `%errorlevel%`을 통해 호출한 쪽에서 확인할 수 있다(38장에서 exit를 본격적으로 다룬다).

**PowerShell은 같은 스크립트 안이면 함수 이름만 쓰고, 외부 파일은 `&`나 `.`으로 부른다**: 스크립트 안에서 앞서 정의한 함수를 호출할 때는 `call MyFunction`이 아니라 그냥 `MyFunction`이라고 쓴다. 반면 외부 스크립트 파일을 실행하려면 호출 연산자 `&`(예: `& .\script.ps1`)나 점 하나로 시작하는 닷소싱 `. .\script.ps1`을 쓰는데, 이 둘의 결정적 차이는 격리 여부다 — 닷소싱은 그 스크립트의 변수·함수를 **현재 스코프**에 그대로 가져오지만, `call`은 (setlocal과 조합하지 않는 한) 호출된 배치의 환경 변경을 항상 격리해 원래 배치에 영향을 주지 않는다.

## 흔한 오개념

<strong>"PowerShell의 `&`(호출 연산자)는 CMD의 call처럼 환경을 격리해줄 것이다"</strong>는 오해가 있다. 실제로는 정반대의 짝이 존재한다. `&`는 자식 스코프에서 스크립트를 실행해 CMD의 call과 비슷하게 변수·함수가 격리되지만, 닷소싱(`.`)은 그 격리를 하지 않고 스크립트의 변수·함수를 호출한 쪽 스코프에 그대로 병합한다. "call처럼 부르는 방법이니 당연히 격리되겠지"라고 짐작하고 닷소싱을 쓰면, 의도치 않게 현재 세션의 변수가 스크립트 내용으로 덮어써지는 사고가 난다.

## 다음 장에서는

다음은 35장 — call처럼 되돌아오지 않고, 같은 배치 파일 안의 레이블로 실행 흐름을 단순히 옮기는 `goto` 명령을 다룬다.

## 평가 기준

- call로 다른 배치 파일이나 레이블을 호출하고, 실행이 끝난 뒤 원래 위치로 복귀하는 흐름을 설명할 수 있다.
- call 없이 배치 파일을 실행하면 왜 복귀하지 않는지 설명할 수 있다.
- 레이블 호출이 "새 배치 컨텍스트"를 만든다는 것과, 파일 끝에 두 번째로 도달했을 때 배치 전체가 종료되는 이유를 설명할 수 있다.
- 재귀 호출에 종료 조건이 반드시 필요한 이유와, call에 파이프·리다이렉션을 함께 쓰면 안 되는 제약을 안다.

## 참고

- [call | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/call)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
