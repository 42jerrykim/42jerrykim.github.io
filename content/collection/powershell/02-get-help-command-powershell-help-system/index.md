---
draft: false
collection_order: 2
slug: get-help-command-powershell-help-system
title: "[PowerShell] 02. Get-Help — 도움말 조회와 Update-Help"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell의 콘솔 내 도움말 시스템 Get-Help의 사용법과 -Full/-Examples/-Online 매개변수, 최초 실행 시 Update-Help가 필요한 이유, about_* 개념 문서를 찾는 법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Windows(윈도우)
- Shell(셸)
- Terminal
- Documentation(문서화)
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Quick-Reference
- Best-Practices
- Reference(참고)
- How-To
- Tips
- Troubleshooting(트러블슈팅)
- Configuration(설정)
- Comparison(비교)
- Automation(자동화)
- DevOps
- Localization
- Man-Page
- Get-Help
- Update-Help
- about-Topics
- Online-Help
- Help-System
image: "wordcloud.png"
---

## 개요

CMD의 `help`나 Bash의 `man`처럼, PowerShell도 콘솔을 벗어나지 않고 명령의 사용법을 찾는 자체 도움말 시스템을 갖추고 있다. 그 진입점이 `Get-Help`다. `Get-Help`는 cmdlet·함수·CIM 명령·워크플로·프로바이더·별칭·스크립트에 대한 정보를 표시하며, `Get-Help Get-Process`처럼 이름을 넘기면 해당 명령의 개요·문법·매개변수를 보여주고, `Get-Help about_*`처럼 패턴을 넘기면 일치하는 개념 문서 목록을 보여준다.

정신 모델은 "cmdlet 이름을 정확히 모를 때도, 관련 키워드 하나로 시작해 점점 좁혀 나갈 수 있는 검색 도구"다. `Get-Help`는 입력이 정확한 명령 이름이면 그 문서를, 여러 문서 제목에 걸쳐 있는 단어면 후보 목록을, 어느 제목에도 없는 단어면 본문에 그 단어가 포함된 문서 목록을 보여준다 — 이 3단계 동작 방식을 알면 무엇을 검색하든 막다른 골목에 몰리지 않는다.

## 사용법

```powershell
Get-Help [[-Name] <String>] [-Full] [-Detailed] [-Examples] [-Parameter <String[]>] [-Online] [-ShowWindow] [<CommonParameters>]
```

가장 간단한 형태는 이름만 넘기는 것이다. `<cmdlet-name> -?`도 `Get-Help <cmdlet-name>`과 동일하게 동작하지만 cmdlet에만 쓸 수 있다. `help`나 `man`은 `Get-Help`를 내부적으로 호출해 한 화면씩 페이징해서 보여주는 함수다.

## 매개변수

| 매개변수 | 설명 |
|---|---|
| `-Name` | 조회할 cmdlet·함수·개념(about_*) 이름. 위치 매개변수라 생략 가능하고 와일드카드를 지원한다 |
| `-Full` | 매개변수 설명·예제·입출력 타입·추가 설명까지 전체 문서를 표시한다 |
| `-Detailed` | 매개변수 설명과 예제를 추가한 기본 문서를 표시한다(`-Full`보다 적은 정보) |
| `-Examples` | 이름·개요·예제만 표시한다 |
| `-Parameter <String[]>` | 지정한 매개변수의 설명만 표시한다. `*`를 쓰면 전체 매개변수 설명을 본다 |
| `-Online` | 기본 브라우저로 해당 명령의 온라인 문서(Microsoft Learn)를 연다 |
| `-ShowWindow` | 검색·설정 기능이 있는 별도 창으로 도움말을 표시한다(Windows 전용, PowerShell 7.0에서 재도입) |
| `-Category` | `Cmdlet`, `Function`, `Provider`, `HelpFile` 등 특정 유형의 문서만 검색한다 |

## 예시

```powershell
Get-Help Get-Process                          # 기본 개요 문서
Get-Help Get-Process -Full                    # 매개변수·예제·입출력 타입까지 전체
Get-Help Get-Process -Examples                # 예제만
Get-Help Get-Process -Online                  # 브라우저로 온라인 문서 열기
Get-Help Get-Process -Parameter *             # 모든 매개변수 설명
Get-Help about_*                              # 설치된 모든 개념(about_) 문서 목록
Get-Help about_Comparison_Operators           # 비교 연산자 개념 문서
Get-Help -Name remoting                       # 제목·본문에 "remoting"이 포함된 문서 목록
Get-Alias gcm | Get-Help                      # 별칭을 넘기면 원래 명령(Get-Command)의 도움말을 표시
Get-Help Add-Member -Full | Out-String -Stream | Select-String -Pattern Clixml   # 도움말 본문에서 키워드 검색
```

## 주의사항·함정

**최초 설치 직후에는 도움말 파일이 없다**: PowerShell 3.0부터, Windows 운영체제와 함께 제공되는 모듈은 도움말 파일을 포함하지 않는다. 도움말 파일 없이 `Get-Help`를 실행하면 자동 생성된 기본 정보(문법 정도)만 나온다. `Update-Help`(관리자 권한 필요, 인터넷 연결 필요)를 한 번 실행해 도움말 파일을 내려받아야 `-Full`·`-Examples`·`-Parameter`가 실제 내용을 보여준다.

```powershell
Update-Help                          # 설치된 모든 모듈의 도움말을 최신화
Update-Help -Module Microsoft.PowerShell.Utility   # 특정 모듈만 갱신
```

**로캘 문제로 도움말이 안 보일 수 있다**: `Get-Help`는 Windows에 설정된 로캘(예: `ko-KR`)의 도움말을 먼저 찾고, 없으면 상위 로캘, 그다음 `en-US` 폴백 순으로 찾는다. 사내 프록시·방화벽 때문에 `Update-Help`가 실패하면 `Save-Help`로 인터넷이 되는 다른 컴퓨터에서 도움말 파일을 내려받아 옮기는 방법도 있다.

**이식성**: CMD의 `help`는 내부 명령어 목록만 보여주고 옵션 설명은 명령마다 제각각인 텍스트에 의존하지만, `Get-Help`는 모든 cmdlet에 대해 `-Syntax`/`-Full`/`-Examples`처럼 구조화된 형식을 일관되게 제공한다. Bash의 `man`은 시스템에 설치된 매뉴얼 페이지를 읽기만 하는 반면, PowerShell은 `Update-Help`로 스스로 콘텐츠를 최신화한다는 점도 다르다.

## Reference

- [Get-Help (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/get-help)
- [about_Updatable_Help - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_updatable_help)
