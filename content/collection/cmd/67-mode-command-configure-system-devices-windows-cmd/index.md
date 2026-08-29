---
draft: false
slug: mode-command-configure-system-devices-windows-cmd
title: "[CMD] 67. mode - 콘솔·직렬·병렬 포트 구성"
description: "mode로 콘솔 화면 버퍼 크기, 코드 페이지, 직렬(COM) 포트 통신 속도, 병렬 포트 리다이렉션을 구성하는 법과 시리얼 프린터를 쓰려면 mode를 두 번 실행해야 하는 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 670
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
- mode
- 콘솔설정
- Legacy
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Hardware
- Troubleshooting(트러블슈팅)
- Configuration(설정)
- Productivity(생산성)
- DevOps
- Administration
- Beginner
image: "wordcloud.png"
---

mode는 시스템 상태를 표시하거나, 시스템 설정을 바꾸거나, 포트·장치를 재구성하는 명령이다. DOS 시절부터 이어진 명령이라 다루는 대상이 여러 갈래로 나뉜다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [66장: gpresult](/post/cmd/gpresult-command-group-policy-info-windows-cmd/)에서 그룹 정책 결과를 다룬 뒤 이어진다. mode는 이 컬렉션에서 다루는 명령 중 다루는 대상이 가장 이질적이다 — 콘솔 화면 크기부터 시리얼 포트 통신 속도까지 한 명령 아래 여러 하위 기능이 모여 있다.

**이 장의 깊이**: 중급. 콘솔 관련 기능만 현대적으로 자주 쓰이고, 나머지는 레거시 하드웨어를 다룰 때만 필요하다.

## 사용법

```
mode [<장치>] [/status]
mode con[:] [cols=<c>] [lines=<n>]
mode con[:] cp select=<코드페이지>
mode com<m>[:] [baud=<b>] [parity=<p>] [data=<d>] [stop=<s>]
mode LPT<n>[:]=COM<m>[:]
```

## 옵션

### 콘솔 화면 버퍼

| 옵션 | 설명 |
|---|---|
| `cols=<c>` | 화면 버퍼의 열 수(기본 80) |
| `lines=<n>` | 화면 버퍼의 줄 수(기본 25) |

### 직렬(COM) 포트

| 옵션 | 설명 |
|---|---|
| `baud=<b>` | 전송 속도(bps). 11=110, 96=9600, 19=19200 등 약어 코드 사용 |
| `parity=<p>` | 패리티 비트(n 없음, e 짝수(기본), o 홀수, m/s 일부 장치 전용) |
| `data=<d>` | 문자당 데이터 비트(5–8, 기본 7) |
| `stop=<s>` | 정지 비트(1, 1.5, 2) |

### 기타

| 옵션 | 설명 |
|---|---|
| `/status` | 지정한 장치(또는 전체)의 상태 표시 |
| `codepage select=<번호>` | CON 장치의 코드 페이지 설정 |
| `rate=<r> delay=<d>` | 키보드 타자 반복 속도·지연 설정 |

## 예시

```
mode con cols=120 lines=30
mode con cp select=949
mode com1 baud=9600
mode /status
mode com1 48,e,,,b
mode lpt1=com1
```

## 주의사항·함정

**시리얼 프린터로 출력을 보내려면 mode를 두 번 실행해야 한다**: 병렬(LPT) 프린터로 가던 출력을 시리얼(COM) 프린터로 우회시키려면, 먼저 시리얼 포트 자체를 설정한 뒤 병렬 포트를 그 시리얼 포트로 리다이렉션해야 한다.

> "To set up your system so that it sends parallel printer output to a serial printer, you must use the **mode** command twice. The first time, you must use **mode** to configure the serial port. The second time, you must use **mode** to redirect parallel printer output to the serial port you specified in the first **mode** command." — Microsoft Learn, "mode"

위 예시의 `mode com1 48,e,,,b`(COM1 설정) 다음 줄 `mode lpt1=com1`(LPT1을 COM1로 리다이렉션)이 정확히 이 두 단계 순서를 보여준다. 순서를 바꾸거나 한 단계만 실행하면 인쇄가 되지 않는다.

**리다이렉션을 해제하려면 LPT를 단독으로 다시 지정한다**: `mode lpt1`처럼 리다이렉션 없이 LPT 포트만 지정하면, 이전에 걸어 둔 LPT→COM 리다이렉션이 풀리고 파일을 다시 LPT1로 직접 인쇄할 수 있게 된다.

**모든 키보드가 타자 반복 속도 설정을 지원하지는 않는다**: `rate=`/`delay=` 조합은 하드웨어에 따라 무시될 수 있다. 설정이 반영되지 않는다고 스크립트가 잘못된 것은 아닐 수 있다.

**콘솔 설정은 터미널 속성으로 대체되는 경우가 많다**: 현대 Windows Terminal이나 콘솔 호스트 속성 대화상자에서 글꼴·창 크기를 설정하는 경우가 흔해, `mode con cols=/lines=`는 자동화 스크립트에서 화면 크기를 강제로 맞춰야 할 때 정도로 용도가 좁아졌다.

**콘솔 크기와 시리얼 포트, PowerShell 대안이 서로 다르다**: 콘솔 창의 크기·버퍼 크기는 `$Host.UI.RawUI.WindowSize`·`$Host.UI.RawUI.BufferSize` 속성으로 PowerShell에서도 동일하게 다룰 수 있다. 하지만 `mode com<m>` 계열이 담당하는 시리얼 포트 설정(전송 속도, 패리티 등)에는 대응하는 PowerShell 내장 cmdlet이 없다 — .NET의 `System.IO.Ports.SerialPort` 클래스를 직접 인스턴스화해서 `BaudRate`·`Parity` 등 속성을 설정해야 한다. 즉 mode 하나가 담당하던 두 기능이 PowerShell에서는 콘솔은 속성 하나, 시리얼 포트는 완전히 다른 .NET 클래스로 갈라진다.

## 흔한 오개념

<strong>"mode의 모든 기능에 대응하는 PowerShell cmdlet이 하나쯤 있을 것"</strong>이라는 오해가 있다. 실제로는 콘솔 크기는 `$Host.UI.RawUI` 속성으로, 시리얼 포트는 cmdlet 없이 .NET `SerialPort` 클래스로 다뤄야 하는 등 mode가 한데 묶어 처리하던 기능들이 PowerShell에서는 장치 종류별로 서로 다른 방식으로 흩어져 있다.

## 다음 장에서는

다음은 68장 — WMI 정보를 명령줄로 조회하는 레거시 도구 `wmic`을 다룬다.

## 평가 기준

- mode로 콘솔 화면 버퍼 크기와 코드 페이지를 설정할 수 있다.
- 시리얼 프린터로 출력을 리다이렉션하려면 mode를 두 번(포트 설정 → 리다이렉션) 실행해야 하는 이유를 설명할 수 있다.
- LPT 포트를 단독으로 지정하면 리다이렉션이 해제된다는 것을 안다.
- 콘솔 관련 설정이 현대에는 대부분 터미널 속성으로 대체되었다는 것을 안다.

## 참고

- [mode | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mode)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
