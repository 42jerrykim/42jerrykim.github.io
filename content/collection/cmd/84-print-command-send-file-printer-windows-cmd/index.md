---
draft: false
slug: print-command-send-file-printer-windows-cmd
title: "[CMD] 84. print - 텍스트 파일 인쇄"
description: "print로 텍스트 파일을 로컬·네트워크 프린터로 보내 백그라운드 인쇄하는 법과 /d로 포트·네트워크 프린터를 지정하는 문법, mode 명령과의 역할 분담을 Microsoft Learn 기준으로 정리한 이 컬렉션의 마지막 장입니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 840
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
- print
- 인쇄
- Printing(프린팅)
- Legacy(레거시)
- Comparison(비교)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Administration
- Education(교육)
- CLI
- Configuration(설정)
- Networking(네트워킹)
- Automation(자동화)
- Curriculum
image: "wordcloud.png"
---

print는 텍스트 파일을 인쇄 대기열로 보내는 명령으로, 이 컬렉션 전체 85개 챕터의 마지막 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [83장: graftabl](/post/cmd/graftabl-command-extended-character-set-windows-cmd/)에서 레거시 표시 명령을 다룬 뒤 이어지며, Part 9(부팅 구성과 기타 유틸리티)와 이 컬렉션 전체를 마무리하는 마지막 장이다.

**이 장의 깊이**: 입문. **다루지 않는 것**: PDF나 서식이 있는 문서의 인쇄는 다루지 않는다 — 텍스트 파일 인쇄만 이 장의 범위다.

## 개요 + 정신 모델

print의 핵심 가치는 "백그라운드 인쇄"에 있다.

> "Sends a text file to a printer. A file can print in the background if you send it to a printer connected to a serial or parallel port on the local computer." — Microsoft Learn, "print"

즉 print는 파일을 프린터로 보낸 뒤 인쇄가 끝날 때까지 CMD 세션을 붙잡아두지 않는다. 인쇄 작업을 대기열에 넣고 즉시 프롬프트로 돌아오므로, 배치 스크립트 안에서 보고서를 인쇄하면서 다음 작업을 계속 진행하는 자동화에 적합하다.

## 사용법

```
print [/d:<프린터>] [<드라이브>:][<경로>]<파일이름>[ ...]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/d:<프린터>` | 인쇄에 쓸 프린터. 병렬 포트는 `LPT1`~`LPT3`, 직렬 포트는 `COM1`~`COM4`. 네트워크 프린터는 `\\서버이름\프린터이름` 큐 이름으로 지정. 생략 시 기본값은 `LPT1` |
| `<드라이브>:` | 인쇄할 파일이 있는 논리·물리 드라이브(현재 드라이브면 생략 가능) |
| `<경로>` | 인쇄할 파일의 위치(현재 디렉터리면 생략 가능) |
| `<파일이름>[ ...]` | 필수. 인쇄할 파일. 한 명령에 여러 파일 지정 가능 |

## 예시

```
print /d:lpt2 report.txt
print /d:\\copyroom\printer1 c:\accounting\report.txt
print report.txt
print /d:"My Printer" file1.txt file2.txt
print file1.txt file2.txt file3.txt
```

## 주의사항·함정

**텍스트 파일 전용이다**: print는 서식 없는 텍스트 파일을 프린터가 이해하는 형식으로 그대로 흘려보내는 단순한 명령이다. Word 문서나 PDF처럼 서식이 있는 파일을 인쇄하려면 print가 아니라 해당 애플리케이션의 인쇄 기능이나 PowerShell의 인쇄 cmdlet을 써야 한다.

**프린터 지정 없이 실행하면 조용히 `LPT1`로 간다**: `/d`를 생략했을 때 기본값이 `LPT1`이라는 점을 모르면, 실제로 쓰려는 프린터가 아닌 엉뚱한 포트로 인쇄 작업이 전송되어 "인쇄가 안 된다"는 혼란을 겪을 수 있다. 네트워크 프린터를 쓰는 환경에서는 `/d:\\서버\프린터이름` 형식을 항상 명시하는 편이 안전하다.

**프린터 이름에 공백이 있으면 따옴표가 필요하다**: `"My Printer"`처럼 공백이 포함된 프린터 이름은 따옴표로 감싸야 한다. 08장(cd)·72장(ipconfig)에서 이미 반복된, CMD 전반에 걸친 공백 처리 규칙이 여기서도 동일하게 적용된다.

**더 폭넓은 프린터 구성은 mode가 담당한다**: print는 파일을 보내는 것 자체에 집중하고, 포트 구성이나 프린터 상태 조회, 코드 페이지 전환 준비 같은 더 폭넓은 설정 작업은 67장(mode)의 영역이다.

> "You can perform many configuration tasks from the command prompt by using the [Mode command](/post/cmd/mode-command-configure-system-devices-windows-cmd/), including configuring a printer connected to a parallel or a serial port, displaying printer status, or preparing a printer for code page switching." — Microsoft Learn, "print"

즉 "프린터로 파일을 보낸다"는 print, "프린터 포트 자체를 구성한다"는 mode로 역할이 나뉜다.

## 흔한 오개념

<strong>"print는 최신 Windows 인쇄 시스템과 무관한 죽은 명령이다"</strong>는 절반만 맞는 오해다. GUI 애플리케이션의 인쇄나 PDF 인쇄에는 쓰이지 않지만, 레거시 배치 스크립트 안에서 로그·보고서 텍스트 파일을 자동으로 인쇄하는 워크플로우는 지금도 존재한다. 다만 새로 자동화를 짠다면 PowerShell의 `Out-Printer`처럼 더 유연한 대안을 우선 고려하는 것이 일반적이다.

## 컬렉션을 마치며

여기까지가 CMD 컬렉션의 85개 챕터(00장 + 84개 번호 챕터) 전체다. 00장에서 제시한 9개 Part — 기초와 탐색, 파일과 디렉터리 조작, 텍스트 검색과 출력 제어, 배치 스크립팅, 디스크와 파일 시스템 관리, 프로세스·서비스와 권한 관리, 시스템 정보와 구성, 네트워크와 원격 진단, 부팅 구성과 기타 유틸리티 — 를 순서대로 따라왔다면, 이제 낯선 Windows 환경에 던져졌을 때 스스로 탐색하고, 파일을 다루고, 문제를 진단하고, 레거시 배치 스크립트를 읽고 고칠 수 있는 실무 역량을 갖췄을 것이다. 특정 명령어의 세부 옵션이 기억나지 않을 때는 [00장의 커리큘럼 표](/post/cmd/getting-started-cmd/)나 [명령어 종류 총정리](/post/cmd/command-categories/)로 언제든 돌아와 필요한 장을 다시 찾아볼 수 있다.

## 평가 기준

- print로 텍스트 파일을 로컬·네트워크 프린터로 보내고, `/d`로 대상을 명시적으로 지정할 수 있다.
- `/d`를 생략했을 때 기본값이 `LPT1`이라는 점을 알고, 그로 인한 혼란을 예방할 수 있다.
- print(파일 전송)와 mode(포트·프린터 구성)의 역할 차이를 설명할 수 있다.
- 이 컬렉션 9개 Part가 다룬 역량 전체를 한 문장으로 요약할 수 있다.

## 참고

- [print | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/print)
- [Mode command | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mode)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
