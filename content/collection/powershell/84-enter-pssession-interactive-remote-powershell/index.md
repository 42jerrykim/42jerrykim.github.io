---
draft: false
collection_order: 84
slug: enter-pssession-interactive-remote-powershell
title: "[PowerShell] 84. Enter-PSSession — 대화형 원격 세션"
date: 2026-08-29
lastmod: 2026-08-29
description: "Enter-PSSession으로 원격 컴퓨터에 대화형으로 접속해 프롬프트가 원격 컴퓨터로 바뀌는 원리와 Exit-PSSession으로 빠져나오는 법, 한 번에 하나의 대화형 세션만 가능하다는 제약, -Credential로 다른 계정을 쓰는 법을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Remoting
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
- Enter-PSSession
- Exit-PSSession
- Interactive-Session
- Remote-Prompt
- PSCredential
- Remote-Session
image: "wordcloud.png"
---

## 개요

`Enter-PSSession`은 원격 컴퓨터 하나와 **대화형** 세션을 시작해, 그 뒤로 입력하는 모든 명령이 로컬이 아니라 원격 컴퓨터에서 실행되게 만든다. 83장에서 WinRM 리스너를 켜 둔 컴퓨터에, 마치 SSH로 로그인한 것처럼 직접 들어가 명령을 입력하는 첫 번째 방법이다.

정신 모델은 "프롬프트 자체가 원격 컴퓨터로 순간이동한다"는 것이다 — 명령을 입력하고 결과를 받는 감각은 로컬과 똑같지만, 실제로 실행되는 위치와 파일이 저장되는 위치가 전부 원격 컴퓨터로 바뀐다.

## 사용법

```powershell
Enter-PSSession -ComputerName <컴퓨터이름> [-Credential <자격증명>]
Exit-PSSession    # 또는 exit
```

## 종류

| 방식 | 설명 |
|---|---|
| `-ComputerName` | 컴퓨터 이름을 직접 지정해 임시 연결(가장 흔한 사용법) |
| `-Session` | 86장에서 만들 지속 세션(`New-PSSession`)에 대화형으로 진입 |
| `-Credential` | 현재 로그인 계정이 아닌 다른 사용자로 인증 |
| `-Port` / `-UseSSL` | 기본 WinRM 포트(5985/HTTP, 5986/HTTPS)가 아닌 값을 쓸 때 |
| `Exit-PSSession` 또는 `exit` | 대화형 세션을 끝내고 로컬 프롬프트로 복귀(동작은 동일) |

## 예시

```powershell
Enter-PSSession -ComputerName Server01           # 프롬프트가 [Server01]: PS C:\> 로 바뀜
Get-Process powershell > C:\ps-test\Process.txt    # 이 파일은 로컬이 아니라 Server01에 저장됨
exit                                                 # 로컬 프롬프트로 복귀

dir C:\ps-test\Process.txt                            # 로컬에서는 이 파일을 찾을 수 없음(원격에 있으므로)

Enter-PSSession -ComputerName Server01 -Credential Domain01\User01   # 다른 계정으로 접속

$s = New-PSSession -ComputerName Server01           # 86장의 지속 세션을 만들고
Enter-PSSession -Session $s                            # 그 세션에 대화형으로 진입
Exit-PSSession                                          # 세션은 유지된 채 대화형 모드만 종료

Enter-PSSession -ComputerName Server01 -Port 90 -Credential Domain01\User01   # 포트 지정
```

## 주의사항·함정

**한 번에 하나의 대화형 세션만 가능하다**: `Enter-PSSession`은 현재 세션 자체를 원격 세션으로 대체하는 방식이라, 다른 컴퓨터에 동시에 대화형으로 접속하려면 먼저 `exit`로 나온 뒤 새로 `Enter-PSSession`을 실행해야 한다. 여러 컴퓨터에 동시에 명령을 내려야 한다면 다음 장의 `Invoke-Command`가 적합한 도구다.

**함수나 스크립트 안에서 호출하도록 설계되지 않았다**: 공식 문서도 명시하듯, `Enter-PSSession`은 현재 대화형 세션을 새 대화형 원격 세션으로 "치환"하는 용도로 설계됐다. 자동화 스크립트 안에서 이 cmdlet을 호출하면 스크립트의 흐름 자체가 원격 세션으로 넘어가 버려 예상과 다르게 동작한다 — 스크립트에서 원격 명령을 실행해야 한다면 `Invoke-Command`를 써야 한다.

**원격 컴퓨터의 사용자 프로필이 적용되므로, 로컬과 명령 프롬프트·별칭이 다르게 보일 수 있다**: `Enter-PSSession`으로 들어간 세션은 접속 계정의 원격 컴퓨터 프로필(06장에서 배운 `$PROFILE`)을 그대로 로드한다. 로컬에서 익숙했던 사용자 정의 함수·별칭이 원격 세션에는 없을 수 있고, 반대로 원격 프로필이 정의한 것들이 낯설게 나타날 수 있다.

**`Disconnect-PSSession`/`Connect-PSSession`으로 대화형 세션을 끊었다 다시 연결할 수는 없다**: 86장에서 다룰 지속 세션과 달리, `Enter-PSSession`이 만든 임시 연결은 연결 해제 후 재연결 기능을 지원하지 않는다. 네트워크가 끊기면 세션 자체가 사라진다.

**이식성**: `ssh user@host`로 원격 셸에 로그인해 프롬프트가 바뀌는 경험과 정확히 같은 개념이다 — 88장에서 다룰 SSH 기반 Remoting을 쓰면 실제로 `Enter-PSSession -HostName`이 이와 매우 비슷한 사용자 경험을 제공한다. CMD에는 대화형 원격 세션에 대응하는 표준 도구가 없다.

## Reference

- [Enter-PSSession (Microsoft.PowerShell.Core) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/enter-pssession)
