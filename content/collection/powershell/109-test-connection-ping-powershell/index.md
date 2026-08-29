---
draft: true
collection_order: 109
slug: test-connection-ping-powershell
title: "[PowerShell] 109. Test-Connection — ping 대응"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell의 Test-Connection이 전통적인 ping 명령을 객체 파이프라인 방식으로 대체하는 원리와 -Count/-Quiet/-Traceroute/-TcpPort 매개변수, PingStatus 객체의 속성을 정리한 Part 16 시작 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- Network(네트워크)
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
- Test-Connection
- Ping
- ICMP
- Traceroute
- Network-Diagnostics
- Cross-Platform
image: "wordcloud.png"
---

## 개요

<strong>Test-Connection</strong>은 ICMP 에코 요청(ping)을 보내 원격 컴퓨터의 응답 여부를 확인하는 cmdlet으로, CMD·Bash의 `ping` 명령이 하던 일을 PowerShell의 객체 파이프라인 안으로 가져온 것이다. 지금까지 프로세스(89–90장)·서비스(91장)·이벤트 로그(93장) 같은 로컬 시스템 관리를 다뤘다면, Part 16(네트워크와 웹)은 이 장을 시작으로 원격 대상과의 연결성·경로·DNS·HTTP 통신을 진단하는 도구로 넘어간다.

정신 모델은 "전통적인 `ping`이 화면에 텍스트 줄을 찍고 사라진다면, `Test-Connection`은 각 응답마다 **TestConnectionCommand+PingStatus** 객체를 파이프라인에 흘려보내 `Where-Object`·`Measure-Object`(17장) 같은 다른 cmdlet과 곧바로 조합할 수 있게 한다"는 것이다. 즉 ping 결과를 눈으로 읽는 대신 코드로 판단할 수 있게 된다.

## 사용법

```powershell
Test-Connection -TargetName <컴퓨터명/IP> [-Count <n>] [-Quiet] [-Traceroute] [-TcpPort <포트>]
```

## 종류

| 매개변수 집합 | 트리거 매개변수 | 동작 |
|---|---|---|
| DefaultPing(기본) | (없음) | 기본 4회 ICMP 에코 요청 |
| RepeatPing | `-Repeat` | 중단할 때까지 계속 ping(첫 대상만) |
| TraceRoute | `-Traceroute` | 대상까지의 경로(홉)를 추적 |
| MtuSizeDetect | `-MtuSize` | 경로 MTU 크기 탐지 |
| TcpPort | `-TcpPort <포트>` | ICMP 대신 지정한 TCP 포트로 연결 테스트 |

| 주요 매개변수 | 의미 |
|---|---|
| `-Count` | 보낼 에코 요청 수(기본 4) |
| `-Quiet` | 불리언 값만 반환(하나라도 성공하면 `$true`) |
| `-TimeoutSeconds` | 응답 대기 시간(기본 5초, PowerShell 6.0+) |
| `-IPv4`/`-IPv6` | 사용할 프로토콜 강제 지정 |
| `-ResolveDestination` | 대상의 DNS 이름을 함께 확인 |

## 예시

```powershell
Test-Connection -TargetName Server01 -IPv4                       # 기본 4회 ping, PingStatus 객체 스트림 출력

Test-Connection -TargetName Server01, Server02, Server12          # 여러 대상에 동시에 ping

Test-Connection -TargetName Server01 -Count 3 -Delay 2             # 3회, 2초 간격

if (Test-Connection -TargetName Server01 -Quiet) {                 # 불리언 값으로 조건 분기(84장 New-PSSession과 조합)
    New-PSSession -ComputerName Server01
}

Test-Connection -TargetName www.google.com -Traceroute             # 경로 추적, TraceStatus 객체 반환

Test-Connection bing.com -TcpPort 443 -Detailed -Count 4            # ICMP 대신 443번 포트로 TCP 연결 테스트(PS 7.4+)

$job = Start-Job -ScriptBlock {                                     # 78장 백그라운드 Job과 조합해 다수 서버 동시 점검
    Test-Connection -TargetName (Get-Content -Path "Servers.txt")
}
Receive-Job $job -Wait
```

## 주의사항·함정

**`-Source` 매개변수는 PowerShell 6 이상에서 지원되지 않는다**: Windows PowerShell 5.1 스크립트를 그대로 pwsh로 옮기면서 `-Source`를 쓰던 코드가 있다면 오류가 난다. PowerShell 6+에서는 로컬 컴퓨터에서만 ping을 보낼 수 있고, 다른 발신지를 지정하려면 84장에서 배운 `Invoke-Command`로 해당 컴퓨터에서 원격 실행해야 한다.

**`-Quiet`는 "하나라도 성공하면 `$true`"이지 "전부 성공"이 아니다**: 기본 4회 중 1회만 응답해도 `-Quiet`는 `$true`를 반환한다. 안정적인 연결인지 확인하려면 `-Quiet` 없이 전체 `PingStatus` 객체를 받아 `Measure-Object`로 성공률을 직접 계산해야 한다.

**`Test-Connection`이 반환하는 객체 타입은 사용한 매개변수에 따라 완전히 달라진다**: 기본 ping은 `PingStatus`, `-Traceroute`는 `TraceStatus`, `-MtuSize`는 `PingMtuStatus`, `-TcpPort`는 `-Detailed` 유무에 따라 `Boolean` 또는 `TcpPortStatus`를 반환한다. 스크립트에서 결과 객체의 속성에 접근하기 전에 어떤 매개변수 조합을 썼는지 먼저 확인해야 한다.

**연속 ping(`-Repeat`)은 여러 대상을 지정해도 첫 번째 대상만 처리한다**: `-Repeat`와 `-Count`는 함께 쓸 수 없는 매개변수 집합이며, `-TargetName`에 배열을 넘겨도 나머지 대상은 조용히 무시된다. 여러 서버를 지속적으로 감시하려면 각 대상마다 별도의 백그라운드 Job을 띄워야 한다.

**이식성**: CMD `ping`과 Bash `ping`은 모두 텍스트 줄을 표준 출력에 찍을 뿐이라, 응답 시간이나 성공 여부를 스크립트에서 활용하려면 정규식으로 파싱해야 한다. `Test-Connection`은 이 파싱 단계를 완전히 없애고 `Latency`·`Status`·`Address` 같은 속성에 바로 접근하게 해준다는 점이 셸 스크립팅과 PowerShell 스크립팅의 근본적 차이를 보여주는 예다. 다만 Linux `ping`의 `-i`(간격)·`-c`(횟수) 같은 옵션 이름과 `Test-Connection`의 `-Delay`·`-Count`는 이름이 달라 그대로 옮겨 쓸 수 없다.

## Reference

- [Test-Connection (Microsoft.PowerShell.Management) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/test-connection?view=powershell-7.5)
