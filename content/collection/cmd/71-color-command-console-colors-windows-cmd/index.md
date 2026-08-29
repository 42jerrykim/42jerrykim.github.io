---
draft: false
slug: color-command-console-colors-windows-cmd
title: "[CMD] 71. color - 콘솔 전경·배경색 설정"
description: "color로 콘솔 창의 전경·배경색을 16색 코드로 바꾸는 법과 두 자리 중 배경·전경이 각각 어디에 대응하는지, 같은 색을 지정하면 ERRORLEVEL 1과 함께 조용히 무시되는 함정을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 710
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
- color
- 콘솔색상
- ERRORLEVEL
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Troubleshooting(트러블슈팅)
- Customization
- Configuration(설정)
- Productivity(생산성)
- DevOps
- Administration
- Advanced
image: "wordcloud.png"
---

color는 현재 세션의 명령 프롬프트 창 전경색과 배경색을 바꾸는 명령이다. Part 7(시스템 정보와 구성)의 마지막 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [70장: chcp](/post/cmd/chcp-command-active-code-page-windows-cmd/)에서 문자 인코딩을 다룬 뒤 이어지며, Part 7의 마지막 장이다. chcp가 "무슨 문자가 보이는가"였다면, color는 "그 문자가 어떤 색으로 보이는가"를 다룬다.

**이 장의 깊이**: 입문.

## 사용법

```
color [<속성>]
```

인수 없이 실행하면 기본 색으로 복원된다.

## 옵션

`/?` 외에 별도 옵션은 없다. `<속성>`은 1~2자리 16진수다.

### 색 코드

| 값 | 색 |
|---|---|
| 0 | 검정 |
| 1 | 파랑 |
| 2 | 녹색 |
| 3 | 청록 |
| 4 | 빨강 |
| 5 | 자주 |
| 6 | 노랑 |
| 7 | 흰색 |
| 8 | 회색 |
| 9 | 연파랑 |
| A | 연녹색 |
| B | 연청록 |
| C | 연빨강 |
| D | 연자주 |
| E | 연노랑 |
| F | 밝은흰색 |

## 예시

```
color 84
color e
color
```

## 주의사항·함정

**두 자리를 지정하면 배경과 전경 순서로 적용된다**: `color`에 두 자리 16진수를 주면, 첫 번째 자리는 배경색, 두 번째 자리는 전경(글자)색을 가리킨다 — `color 1F`처럼 파란 배경에 밝은흰색 글자를 만드는 조합이 대표적인 예다. 한 자리만 지정하면(위 예시의 `color e`) 그 값은 전경색에만 적용되고 배경은 기본값 그대로 유지된다.

**같은 색을 두 자리에 반복하면 조용히 무시된다**: 배경과 전경을 같은 값으로 지정하면 글자와 배경이 구분되지 않아 화면이 사실상 비어 보이게 되는데, color는 이 상황을 막아준다.

> "If you specify the same value for two hexadecimal digits, the ERRORLEVEL is set to `1` and no change is made to either the foreground or the background color." — Microsoft Learn, "color"

즉 `color 11`처럼 같은 값을 두 번 쓰면 색이 전혀 바뀌지 않고 `%ERRORLEVEL%`만 1로 설정된다. 화면에 아무 에러 메시지도 뜨지 않으므로, 배치 스크립트에서 색 변경이 실패했는지 확인하려면 이 종료 코드를 직접 검사해야 한다.

**세션 한정이다**: 04장(prompt)·05장(title)에서 이미 본 패턴과 같다 — color로 바꾼 색은 그 CMD 세션에만 적용되고, 창을 닫으면 사라진다. 매번 같은 색으로 시작하고 싶다면 배치 파일 시작 부분에 color를 넣거나, 콘솔 창의 기본값 자체를 속성 대화상자에서 바꿔야 한다.

**PowerShell 대안은 `$Host.UI.RawUI.ForegroundColor`·`$Host.UI.RawUI.BackgroundColor`다**: 이 두 속성에 각각 색을 대입해 전경·배경을 바꿀 수 있다. color처럼 한 자리 16진수 코드(0-F)로 지정하는 방식이 아니라 `Green`·`Black`처럼 이름이 붙은 색상값(`ConsoleColor` 열거형 멤버)을 대입한다는 점이 근본적으로 다르다 — 색 지정 모델 자체가 16진수 니블 방식에서 이름 기반 방식으로 완전히 바뀐다.

## 흔한 오개념

<strong>"두 자리 색 코드에서 앞자리가 전경색이고 뒷자리가 배경색"</strong>이라고 착각하는 경우가 흔하다. 실제로는 정반대로 앞자리가 배경색, 뒷자리가 전경(글자)색이다 — `color 1F`는 파란 배경에 밝은흰색 글자를 만드는 것이지, 밝은흰색 배경에 파란 글자를 만드는 것이 아니다.

## 다음 장에서는

다음은 72장 — 로컬 컴퓨터의 TCP/IP 네트워크 구성을 표시하는 `ipconfig` 명령으로 Part 8(네트워크와 원격 진단)이 시작된다.

## 평가 기준

- color로 콘솔의 전경·배경색을 16진수 코드로 설정할 수 있다.
- 두 자리 코드에서 배경과 전경이 각각 어느 자리에 대응하는지 설명할 수 있다.
- 같은 색을 두 번 지정하면 변경 없이 ERRORLEVEL만 1로 설정된다는 것을 안다.
- color 설정이 세션 한정이라는 것을 안다.

## 참고

- [color | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/color)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
