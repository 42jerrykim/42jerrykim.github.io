---
draft: false
slug: goto-command-batch-label-jump-windows-cmd
title: "[CMD] 35. goto - 배치 파일 레이블로 실행 흐름 이동"
description: "goto로 배치 파일 안의 레이블로 점프하는 법과 되돌아오지 않는다는 call과의 차이, 특수 레이블 :EOF로 배치를 깔끔하게 종료하는 관용구, 레이블을 찾지 못했을 때 배치가 중단되는 함정을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 350
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
- goto
- 레이블
- Batch
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Education(교육)
- CLI
- Comparison(비교)
- Command-Extensions
- Advanced
- Configuration(설정)
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

goto는 배치 프로그램 안에서 레이블이 붙은 줄로 실행 흐름을 옮기는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [34장: call](/post/cmd/call-command-batch-subroutine-windows-cmd/)에서 "호출 후 복귀"를 다룬 뒤 이어진다. goto는 복귀가 없는 단순 점프라는 점에서 call과 대비된다 — 이 둘의 차이를 명확히 하는 것이 이 장의 핵심이다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
goto <레이블>
```

레이블은 콜론(`:`)으로 시작하는 줄로 정의한다.

## 옵션

별도 옵션은 없다. 레이블 이름에 공백은 쓸 수 있지만 세미콜론(`;`)이나 등호(`=`) 같은 다른 구분자는 쓸 수 없다.

## 예시

```bat
echo off
format a: /s
if not errorlevel 1 goto end
echo An error occurred during formatting.
:end
echo End of batch program.
```

```bat
:process
echo Processing...
goto end
:end
echo Done.
```

## 주의사항·함정

**goto는 복귀하지 않는다**: call과 가장 크게 다른 점이다. `goto`로 레이블에 도달하면 그 지점부터 실행이 계속될 뿐, 원래 goto를 호출한 위치로 돌아오는 개념 자체가 없다. 34장의 call이 "다녀오겠습니다"라면, goto는 "이사갑니다"에 가깝다.

**`:EOF`는 배치 파일을 깔끔하게 끝내는 특수 레이블이다**: 명령 확장이 켜져 있으면(기본값), `goto :EOF`는 실제로 그런 이름의 레이블을 정의하지 않아도 배치 파일의 끝으로 바로 이동해 실행을 종료한다.

> "If command extensions are enabled (the default), and you use the **goto** command with a target label of **:EOF**, you transfer control to the end of the current batch script file and exit the batch script file without defining a label." — Microsoft Learn, "goto"

34장에서 본 것처럼, `call :레이블`로 호출된 서브루틴 끝에 `goto :eof`를 넣으면 호출한 위치로 정확히 복귀한다 — 서브루틴이 파일의 물리적 끝까지 흘러가지 않고 그 자리에서 "여기서 이 서브루틴은 끝"이라고 명시하는 관용구다.

**존재하지 않는 레이블로 이동하면 배치가 중단된다**: 지정한 레이블이 파일 안에 없으면 다음 메시지와 함께 배치 실행이 그대로 멈춘다.

> "Label not found" — Microsoft Learn, "goto"

오타가 난 레이블 이름은 CMD가 문법 검사 단계에서 미리 잡아주지 않고, 실제로 그 goto 줄이 실행되는 순간에야 발견된다.

**PowerShell에는 goto·레이블 구문이 아예 없다**: 언어 설계 차원에서 의도적으로 뺀 것이다. 관용적인 PowerShell 코드는 goto 기반 흐름 제어 대신 함수, `while`·`do-while` 같은 반복문, `switch` 문으로 같은 로직을 표현한다. 이는 기능이 빠진 것이 아니라, goto를 지양하라는 일반적인 프로그래밍 모범 사례를 언어 차원에서 반영한 결과다.

## 흔한 오개념

<strong>"goto와 call은 결국 같은 일을 한다"</strong>는 오해가 흔하다. 둘 다 레이블로 이동한다는 점은 같지만, call은 "새 배치 컨텍스트"를 만들어 나중에 복귀할 수 있게 하고 goto는 그런 컨텍스트 없이 그냥 다음 실행 위치를 바꿀 뿐이다. 반복문처럼 여러 번 되돌아와야 하는 로직이라면 goto와 조건문(32장)을 조합하는 것으로 충분하지만, "결과를 받아 이어서 처리해야 하는" 서브루틴이 필요하다면 call이 적합하다.

## 다음 장에서는

다음은 36장 — 배치 매개변수 `%1`, `%2`의 위치를 한 칸씩 옮기는 `shift` 명령을 다룬다.

## 평가 기준

- goto로 레이블로 이동하는 배치 프로그램을 작성할 수 있다.
- goto와 call의 근본적인 차이(복귀 여부)를 설명할 수 있다.
- `goto :EOF`가 무엇을 하는지, call로 호출된 서브루틴 끝에서 왜 유용한지 설명할 수 있다.
- 존재하지 않는 레이블로 이동하면 배치가 중단된다는 것을 안다.

## 참고

- [goto | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/goto)
- [if | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/if)
