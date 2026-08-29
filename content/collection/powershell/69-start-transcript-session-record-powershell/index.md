---
draft: true
collection_order: 69
slug: start-transcript-session-record-powershell
title: "[PowerShell] 69. Start-Transcript — 세션 기록"
date: 2026-08-29
lastmod: 2026-08-29
description: "Start-Transcript로 PowerShell 세션의 입력·출력 전체를 텍스트 파일로 기록하는 법과 -Path/-Append/-IncludeInvocationHeader 매개변수, Stop-Transcript와의 관계, 프로필에 등록해 세션 전체를 기록하는 법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Error-Handling
- Guide(가이드)
- Education(교육)
- Beginner
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Automation(자동화)
- DevOps
- Start-Transcript
- Stop-Transcript
- Session-Logging
- Audit-Trail
- Troubleshooting
- Console-Log
image: "wordcloud.png"
---

## 개요

`Start-Transcript`는 사용자가 입력한 모든 명령과 콘솔에 나타난 모든 출력을 하나의 텍스트 파일로 기록하는 cmdlet이다. 68장까지 다룬 `Write-Verbose`/`Write-Debug`가 스크립트 작성자가 의도적으로 남기는 진단 메시지였다면, `Start-Transcript`는 그런 의도와 무관하게 세션에서 실제로 일어난 모든 것을 있는 그대로 녹화한다는 점에서 성격이 다르다.

정신 모델은 "화면 녹화와 비슷하지만 텍스트 버전"이라는 것이다. 문제가 재현되지 않을 때, 나중에 "그때 정확히 무슨 명령을 실행했고 어떤 결과가 나왔는지" 되짚어 볼 유일한 방법이 되기도 한다.

## 사용법

```powershell
Start-Transcript [[-Path] <String>] [-Append] [-NoClobber] [-IncludeInvocationHeader]
# ... 세션 작업 수행 ...
Stop-Transcript
```

## 종류

| 매개변수 | 설명 |
|---|---|
| `-Path` | 저장 위치(생략 시 Windows는 `$HOME\Documents`, Linux/macOS는 `$HOME`에 자동 생성된 이름으로 저장) |
| `-OutputDirectory` | 파일명은 자동 생성하되 디렉터리만 지정 |
| `-Append` | 기존 트랜스크립트 파일 끝에 이어서 기록 |
| `-NoClobber` | 기존 파일이 있으면 실패시켜 덮어쓰기 방지 |
| `-IncludeInvocationHeader` | 각 명령이 실행된 시각까지 함께 기록 |
| `-UseMinimalHeader` | 파일 맨 위에 붙는 상세 헤더 대신 짧은 헤더 사용(PowerShell 6.2+) |
| `$Transcript` | `-Path`를 생략했을 때 사용할 경로를 미리 지정해 두는 기본 설정 변수 |

## 예시

```powershell
Start-Transcript                                          # 기본 위치에 자동 이름으로 시작
Get-Process | Where-Object CPU -gt 100
Stop-Transcript                                             # 기록 종료, 저장 경로 출력

Start-Transcript -Path "C:\transcripts\session.txt" -NoClobber   # 명시적 경로 + 덮어쓰기 방지

$sharePath = '\\Server01\Transcripts'
$filename = "Transcript-$($Env:USERNAME)-$(Get-Date -Format 'yyyyMMddHHmmss').txt"
$Transcript = Join-Path -Path $sharePath -ChildPath $filename   # $Transcript 기본 설정 변수 활용
Start-Transcript

Start-Transcript -Path .\logs\troubleshoot.txt -IncludeInvocationHeader   # 각 명령의 실행 시각까지 기록

# 06장에서 다룬 $PROFILE에 등록하면 매 세션마다 자동 기록
# $PROFILE 파일에 아래 줄 추가:
# Start-Transcript -OutputDirectory "$HOME\Documents\PSTranscripts"
```

## 주의사항·함정

**`Write-Host`(29장)로 출력한 내용도 트랜스크립트에는 남지만, 파이프라인으로는 여전히 전달되지 않는다**: 트랜스크립트는 "화면에 보인 모든 것"을 기록하므로 `Write-Host`의 출력도 파일에는 남는다. 다만 이것이 `Write-Host`가 파이프라인에 값을 전달하게 됐다는 뜻은 아니다 — 29장에서 배운 두 스트림의 근본적인 차이는 트랜스크립트 유무와 무관하게 그대로다.

**동시에 여러 트랜스크립트를 시작하면 파일명이 자동으로 구분된다**: PowerShell 5.0부터 기본 파일명에 호스트 이름과 무작위 문자열이 포함되므로, 같은 컴퓨터에서 세션을 여러 개 열어도 서로 다른 트랜스크립트 파일이 덮어써지지 않는다. 다만 이는 파일명을 명시적으로 지정하지 않았을 때만 해당하며, `-Path`로 같은 경로를 여러 세션에서 동시에 지정하면 여전히 충돌할 수 있다.

**중첩된 `Start-Transcript` 호출은 오류를 낸다**: 이미 트랜스크립트가 진행 중인 세션에서 `Start-Transcript`를 다시 호출하면 오류가 난다. 스크립트 안에서 트랜스크립트를 시작하기 전에 이미 세션이 기록 중인지 확실치 않다면, `try`/`catch`(65장)로 감싸 오류를 무시하거나 기존 트랜스크립트를 먼저 정지시켜야 한다.

**민감한 정보가 그대로 텍스트 파일에 남는다**: 트랜스크립트는 화면에 표시된 모든 것을 그대로 저장하므로, 세션 중에 자격 증명이나 비밀 값을 화면에 출력했다면 그 값도 트랜스크립트 파일 안에 평문으로 남는다. 감사 목적으로 세션 전체를 기록해야 하는 환경이라면, 민감한 값을 화면에 직접 출력하지 않는 습관과 트랜스크립트 파일 자체의 접근 권한 관리가 함께 필요하다.

**이식성**: Bash의 `script` 명령이 터미널 세션 전체를 기록한다는 점에서 가장 가까운 대응이지만, ANSI 이스케이프 시퀀스까지 그대로 담아 사람이 읽기엔 오히려 텍스트가 지저분해지는 경우가 많다. CMD에는 세션 전체를 기록하는 표준 명령이 없어 리다이렉션(`> log.txt`)으로 출력만 부분적으로 남기는 방법이 주로 쓰인다. `Start-Transcript`는 입력 명령까지 함께 기록해 재현성 측면에서 더 완결적이다.

## Reference

- [Start-Transcript (Microsoft.PowerShell.Host) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.host/start-transcript)
