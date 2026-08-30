---
draft: false
collection_order: 8
slug: clear-host-command-console-title-color
title: "[PowerShell] 08. Clear-Host — 화면 지우기와 콘솔 설정"
date: 2026-08-29
lastmod: 2026-08-29
description: "Clear-Host(cls/clear 별칭)로 화면을 지우는 법과 함수라서 매개변수가 없는 이유, $Host.UI.RawUI로 콘솔 창 제목·전경색·배경색을 코드로 바꾸는 법을 정리한 PowerShell 콘솔 커스터마이징 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Windows(윈도우)
- Shell(셸)
- Terminal
- Configuration(설정)
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Automation(자동화)
- DevOps
- Clear-Host
- Console
- RawUI
- Alias
- Customization
- ANSI
image: "wordcloud.png"
---

## 개요

`Clear-Host`는 현재 화면에 쌓인 명령·출력을 모두 지우고 프롬프트만 남기는 명령이다. CMD의 `cls`, Bash의 `clear`와 하는 일은 같지만, PowerShell에서는 이것이 컴파일된 cmdlet이 아니라 단순 함수(simple function)로 구현되어 있다는 점이 다르다. 이 챕터는 `Clear-Host` 자체와, 콘솔 창의 제목·색상처럼 화면을 지우는 것 이상으로 콘솔 자체를 다루는 설정을 함께 짚는다.

정신 모델은 "`Clear-Host`는 화면(디스플레이)만 지울 뿐 세션 상태는 건드리지 않는다"는 것이다. 화면을 지워도 정의해 둔 변수·함수·히스토리는 그대로 남아 있으며, 반대로 콘솔 창의 제목이나 색상처럼 화면 자체의 속성을 바꾸는 작업은 `Clear-Host`가 아니라 `$Host.UI.RawUI` 객체를 통해 이뤄진다.

## 사용법

```powershell
Clear-Host       # 화면 지우기(매개변수 없음)
cls              # Windows의 내장 별칭
clear            # Windows·Linux·macOS 공통 별칭
```

`Clear-Host`는 고급 함수가 아니라 단순 함수라 매개변수 자체가 없다. 호스트 프로그램(콘솔, Windows Terminal, VS Code 통합 터미널)에 따라 화면을 지우는 실제 구현이 다를 수 있어, "화면을 지운다"는 결과는 같아도 동작 방식은 호스트가 결정한다.

## 콘솔 창 제목·색상 설정

콘솔 창 자체의 속성은 `$Host.UI.RawUI` 객체의 속성을 직접 바꿔서 제어한다.

| 속성 | 설명 |
|---|---|
| `$Host.UI.RawUI.WindowTitle` | 콘솔 창 제목 표시줄 텍스트 |
| `$Host.UI.RawUI.ForegroundColor` | 기본 글자색 |
| `$Host.UI.RawUI.BackgroundColor` | 기본 배경색 |
| `$Host.UI.RawUI.WindowSize` | 콘솔 창 크기(가로×세로 문자 수) |
| `$PSStyle.Formatting.*`(PowerShell 7.2+) | ANSI 색상 코드를 이용한 출력 스트림별 서식 |

```powershell
$Host.UI.RawUI.WindowTitle = "PowerShell $($PSVersionTable.PSVersion)"
$Host.UI.RawUI.ForegroundColor = 'White'
$Host.UI.RawUI.BackgroundColor = 'DarkBlue'
Clear-Host   # 배경색을 바꾼 뒤에는 Clear-Host로 화면 전체에 새 배경색을 적용해야 즉시 반영된다
```

## 주의사항·함정

**배경색을 바꾼 직후에는 `Clear-Host`가 필요하다**: `$Host.UI.RawUI.BackgroundColor`를 바꿔도 이미 화면에 출력된 부분은 이전 배경색 그대로 남는다. 새 배경색을 화면 전체에 적용하려면 색상 변경 직후 `Clear-Host`를 호출해야 한다.

**호스트마다 지원 범위가 다르다**: `$Host.UI.RawUI`의 일부 속성(특히 `WindowSize`, `BufferSize`)은 실제 콘솔 창이 있는 호스트에서만 의미가 있다. VS Code 통합 터미널이나 원격 세션처럼 실제 콘솔 창이 없는 호스트에서는 이런 속성을 읽거나 쓸 때 오류가 날 수 있다.

**이식성**: CMD는 `title`·`color` 명령으로, Bash는 이스케이프 시퀀스(`\e]0;제목\a`)나 `tput` 명령으로 비슷한 설정을 하지만, PowerShell은 이 모든 것을 `$Host.UI.RawUI`라는 하나의 객체 속성 집합으로 통일해서 다룬다. 텍스트 이스케이프 코드를 외울 필요 없이 객체의 속성을 읽고 쓰는 것만으로 콘솔을 제어할 수 있다는 점이 객체 파이프라인의 장점이 콘솔 조작에도 적용된 사례다.

## Reference

- [Clear-Host (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/clear-host)
