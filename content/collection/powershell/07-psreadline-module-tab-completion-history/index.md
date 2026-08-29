---
draft: true
collection_order: 7
slug: psreadline-module-tab-completion-history
title: "[PowerShell] 07. PSReadLine — 탭 완성과 명령 히스토리"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell 콘솔의 명령줄 편집을 담당하는 PSReadLine 모듈의 탭 완성, Predictive IntelliSense, 커스텀 키 바인딩, 히스토리 파일 위치와 민감정보(비밀번호·토큰) 자동 필터링 동작을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Module
- Windows(윈도우)
- Shell(셸)
- Terminal
- Productivity(생산성)
- Automation(자동화)
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
- Configuration(설정)
- DevOps
- PSReadLine
- Tab-Completion
- Command-History
- IntelliSense
- Key-Binding
- Security(보안)
image: "wordcloud.png"
---

## 개요

**PSReadLine**은 PowerShell 콘솔의 명령줄 편집 경험을 담당하는 모듈로, Windows PowerShell 5.1부터 기본 포함되어 있다. Bash의 GNU Readline이 하는 일과 비슷하게, 한 줄 입력 편집을 구문 강조·다중 줄 히스토리·사용자 지정 키 바인딩까지 갖춘 완전한 편집기로 끌어올린다. PSReadLine이 없다면 PowerShell 콘솔은 화살표 키로 커서만 옮길 수 있는 수준의 입력줄에 머물렀을 것이다.

정신 모델은 "지금 타이핑 중인 명령줄 자체가 하나의 편집 가능한 버퍼이고, PSReadLine이 그 버퍼에 대한 모든 키 입력을 가로채 처리한다"는 것이다. 탭 완성, 구문 오류 표시, 예측 제안(Predictive IntelliSense)은 모두 이 버퍼 위에서 동작하는 기능이며, `Set-PSReadLineKeyHandler`로 원하는 동작을 원하는 키에 재배치할 수 있다.

## 사용법

PSReadLine은 Windows PowerShell 5.1 이상에서 이미 로드되어 있으므로 별도 설치 없이 바로 쓸 수 있지만, 최신 기능이 필요하면 PowerShell Gallery에서 최신 버전으로 갱신한다.

```powershell
Install-Module -Name PSReadLine -AllowClobber -Force   # 최신 버전으로 갱신
Set-PSReadLineOption -PredictionSource History          # Predictive IntelliSense 활성화
Set-PSReadLineOption -PredictionSource None              # 비활성화
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward   # 키 재배치
```

## 매개변수

| 기능 | 기본 동작 | 관련 cmdlet |
|---|---|---|
| 탭 완성 | `Tab` 키로 명령·매개변수·경로 자동완성 | 기본 활성화 |
| 명령 예측 | 히스토리·플러그인 기반으로 입력을 미리 제안 | `Set-PSReadLineOption -PredictionSource` |
| 구문 강조 | 명령줄의 문자열·연산자·변수를 색으로 구분 | `Set-PSReadLineOption -Colors` |
| 커스텀 키 바인딩 | 특정 키에 원하는 동작(내장 함수 또는 스크립트 블록)을 연결 | `Set-PSReadLineKeyHandler` |
| 편집 모드 | `Cmd` 모드(기본)와 `Emacs` 모드 전환 | `Set-PSReadLineOption -EditMode` |
| F1 도움말 조회 | 커서 근처 cmdlet의 `Get-Help -Full`을 별도 화면으로 표시 | 내장(PSReadLine 2.2.2+) |

## 예시

```powershell
Get-Module PSReadLine -ListAvailable          # 설치된 PSReadLine 버전 확인
Set-PSReadLineOption -EditMode Emacs          # Emacs 스타일 키 바인딩으로 전환
Set-PSReadLineOption -Colors @{ Command = 'Cyan' }   # 명령어 색상 지정
Get-PSReadLineKeyHandler                      # 현재 적용된 전체 키 바인딩 목록
```

## 주의사항·함정

**히스토리 파일에는 실제로 입력한 명령이 그대로 저장된다**: PSReadLine은 세션 종료 후에도 유지되는 히스토리 파일(`$Env:APPDATA\Microsoft\Windows\PowerShell\PSReadLine\` 등, 호스트별로 별도 파일)에 입력한 명령을 기록한다. `password`, `token`, `apikey`, `secret` 같은 문자열이 포함된 명령줄은 자동으로 히스토리 저장에서 제외되지만, 이 필터는 완벽하지 않으므로 민감정보를 명령줄에 직접 입력하는 습관 자체를 피하는 것이 안전하다(100장에서 `PSCredential`을 다룬다).

**PowerShell ISE에서는 동작하지 않는다**: PSReadLine은 기본 콘솔 호스트, Windows Terminal, VS Code에서 동작하지만 Windows PowerShell ISE에는 적용되지 않는다. ISE에서 익힌 단축키가 다른 호스트에서 다르게 동작하는 이유가 여기에 있다.

**버전에 따라 기능 차이가 크다**: Windows PowerShell 5.1에는 PSReadLine 2.0.0이 고정 포함되어 있어 Predictive IntelliSense 같은 최신 기능이 없다. `Install-Module -Name PSReadLine -AllowClobber -Force`로 최신 버전을 설치하면 5.1에서도 최신 기능 상당수를 쓸 수 있지만, 일부 기능은 PowerShell 7.2 이상을 요구한다.

**이식성**: GNU Readline(Bash)과 PSReadLine은 목적이 같지만 설정 방식이 다르다 — Readline은 `~/.inputrc` 텍스트 파일로 설정하는 반면, PSReadLine은 `Set-PSReadLineOption`/`Set-PSReadLineKeyHandler` cmdlet 호출로 설정하며, 이 호출을 06장에서 다룬 프로파일 스크립트에 넣어야 매 세션 적용된다.

## Reference

- [about_PSReadLine - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/psreadline/about/about_psreadline)
