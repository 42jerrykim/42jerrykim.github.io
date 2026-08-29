---
draft: false
slug: shift-command-batch-parameters-windows-cmd
title: "[CMD] 36. shift - 배치 매개변수 위치 이동"
description: "shift로 %0-%9 배치 매개변수를 한 칸씩 밀어 10개가 넘는 인자를 처리하는 법과 /n으로 특정 위치부터만 미는 법, shift가 되돌릴 수 없다는 제약, %*에는 영향을 주지 않는다는 함정을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 360
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
- shift
- 배치매개변수
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

shift는 배치 파일의 매개변수(`%0`부터 `%9`까지)를 한 칸씩 앞으로 미는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [35장: goto](/post/cmd/goto-command-batch-label-jump-windows-cmd/)에서 레이블 점프를 다룬 뒤 이어진다. goto·if와 조합해 "인자가 없어질 때까지 반복" 패턴을 만드는 것이 이 장의 대표적인 활용이다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
shift [/n <N>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| (없음) | `%1`을 `%0`으로, `%2`를 `%1`로... 한 칸씩 밀어 넣음 |
| `/n <N>` | N번째(0–8) 인자부터 shift 시작. 명령 확장 필요(기본 활성화) |

## 예시

```bat
@echo off
rem MYCOPY.BAT copies any number of files to a directory.
rem mycopy dir file1 file2 ...
set todir=%1
:getfile
shift
if "%1"=="" goto end
copy %1 %todir%
goto getfile
:end
set todir=
echo All done
```

```
SHIFT /2
```

## 주의사항·함정

**10개가 넘는 인자를 다룰 수 있게 해준다**: 배치 매개변수는 `%0`부터 `%9`까지 10개뿐이지만, shift로 11번째 이후 인자를 `%9` 자리로 하나씩 밀어 넣으면 개수 제한 없이 순회할 수 있다.

**`/n`은 지정한 위치 앞은 그대로 둔다**: `/n`을 쓰면 그 번호보다 앞선 인자는 밀리지 않는다.

> "For example, **SHIFT /2** would shift **%3** to **%2**, **%4** to **%3**, and so on, and leave **%0** and **%1** unaffected." — Microsoft Learn, "shift"

프로그램 이름(`%0`)이나 첫 번째 고정 인자(`%1`)는 그대로 유지하면서 나머지만 순회하고 싶을 때 유용하다.

**`%*`에는 영향을 주지 않는다**: shift로 `%1`, `%2`... 개별 변수는 밀리지만, 모든 인자를 한 번에 나타내는 `%*`는 shift의 영향을 받지 않는다.

> "The **shift** command has no effect on the **%\*** batch parameter." — Microsoft Learn, "shift"

`%*`로 전체 인자를 다시 넘기는 로직과 shift로 하나씩 소비하는 로직을 같은 스크립트에서 섞어 쓰면, `%*`는 여전히 원래 인자 전체를 가리킨다는 점에 유의해야 한다.

**되돌릴 수 없다**: shift를 실행하면 그 전의 `%0` 값은 영영 사라진다.

> "There's no backward **shift** command. After you implement the **shift** command, you can't recover the batch parameter (**%0**) that existed before the shift." — Microsoft Learn, "shift"

shift 전에 참조해야 할 값이 있다면 shift를 실행하기 전에 반드시 별도 변수(31장에서 다룬 set)에 저장해 둬야 한다.

**PowerShell 함수는 애초에 `%1`, `%2` 위치 접근에 덜 의존한다**: `param($Name, $Path)`처럼 `param()` 블록으로 이름 붙은 매개변수를 선언하는 것이 관용적인 방식이라, shift로 위치를 밀어야 할 일 자체가 잘 생기지 않는다. 위치·가변 인자를 다뤄야 할 때 쓰는 `$args` 배열도 `$args[2]`처럼 원하는 인덱스에 바로 접근할 수 있어서, CMD의 배치 매개변수처럼 목록 전체를 물리적으로 밀어야만 뒤쪽 인자에 닿을 수 있는 제약이 없다.

## 흔한 오개념

<strong>"shift는 배열 인덱스를 옮기는 것과 같다"</strong>는 오해가 있다. shift는 배치 매개변수라는 특수한 슬롯(`%0`–`%9`) 자체의 내용을 물리적으로 밀어내는 것이지, 어딘가에 저장된 배열을 인덱스로 순회하는 것이 아니다. CMD에는 진짜 배열 자료형이 없으므로, shift는 "인자 개수를 알 수 없는 가변 인자 처리"라는 좁은 문제에 특화된 도구로 이해하는 편이 정확하다.

## 다음 장에서는

다음은 37장 — 사용자가 키를 누를 때까지 배치 실행을 멈추는 `pause` 명령을 다룬다.

## 평가 기준

- shift로 배치 매개변수를 밀어 10개 넘는 인자를 순회하는 스크립트를 작성할 수 있다.
- `/n`으로 특정 위치 이후만 shift하는 방법을 설명할 수 있다.
- shift가 `%*`에는 영향을 주지 않고 되돌릴 수도 없다는 두 가지 제약을 설명할 수 있다.

## 참고

- [shift | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/shift)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
