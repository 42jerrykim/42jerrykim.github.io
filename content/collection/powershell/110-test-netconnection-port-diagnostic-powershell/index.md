---
draft: true
collection_order: 110
slug: test-netconnection-port-diagnostic-powershell
title: "[PowerShell] 110. Test-NetConnection — 포트·경로 진단"
date: 2026-08-29
lastmod: 2026-08-29
description: "Windows 전용 NetTCPIP 모듈의 Test-NetConnection이 -Port/-CommonTCPPort/-DiagnoseRouting으로 109장 Test-Connection보다 훨씬 상세한 연결 진단 정보를 제공하는 방식을 정리한 챕터다."
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
- Test-NetConnection
- Port-Diagnostics
- Route-Diagnostics
- NetTCPIP
- TCP-Connectivity
- Firewall(방화벽)
image: "wordcloud.png"
---

## 개요

<strong>Test-NetConnection</strong>은 109장의 `Test-Connection`보다 한 단계 더 깊은 진단 정보를 제공하는 Windows 전용 cmdlet이다. `Test-Connection`이 범용 크로스플랫폼 ping 대체재라면, `Test-NetConnection`은 NetTCPIP 모듈(94장에서 다룬 CIM 기반 네트워킹 모듈군의 일부)에 속한 Windows 전용 도구로, TCP 포트 연결·경로 추적·경로 선택 진단까지 하나의 명령으로 묶어서 보여준다.

정신 모델은 "`Test-Connection`이 '살아있는가?'를 묻는 청진기라면, `Test-NetConnection`은 '어느 경로로, 어느 포트로, 어떤 인터페이스를 거쳐 도달하는가'까지 보여주는 정밀 진단 장비"라는 것이다. 네트워크 문제를 조사할 때 `Test-Connection`으로 먼저 살아있는지 확인한 뒤, `Test-NetConnection`으로 구체적인 경로·포트 문제를 파고드는 흐름이 자연스럽다.

## 사용법

```powershell
Test-NetConnection [[-ComputerName] <컴퓨터명>] [-Port <포트>] [-InformationLevel Detailed|Quiet]
```

## 종류

| 매개변수 집합 | 트리거 매개변수 | 동작 |
|---|---|---|
| ICMP(기본) | (없음) 또는 `-TraceRoute` | ping 테스트, 필요 시 경로 추적 |
| CommonTCPPort | `-CommonTCPPort <이름>` | 잘 알려진 서비스 포트(HTTP/RDP/SMB/WINRM)로 테스트 |
| RemotePort | `-Port <포트번호>` | 임의의 TCP 포트로 연결 테스트 |
| NetRouteDiagnostics | `-DiagnoseRouting` | 발신지 주소·경로 선택 과정 자체를 진단 |

| 주요 매개변수 | 의미 |
|---|---|
| `-InformationLevel` | `Quiet`(불리언만) 또는 `Detailed`(경로·인터페이스 포함 전체 정보) |
| `-Hops` | `-TraceRoute`와 함께 추적할 최대 홉 수 |
| `-ConstrainInterface` | 경로 진단 시 특정 인터페이스로 강제 제한 |

## 예시

```powershell
Test-NetConnection                                                    # 기본 대상(internetbeacon.msedge.net)으로 ping 테스트

Test-NetConnection -ComputerName "www.contoso.com" -InformationLevel Detailed   # DNS 해석 결과·경로·발신지 주소까지 상세 출력

Test-NetConnection -Port 80 -InformationLevel Detailed                 # 80번 포트 TCP 연결 테스트 + IPsec 규칙·격리 컨텍스트까지 확인

Test-NetConnection -ComputerName "dc01" -CommonTCPPort WINRM             # 83장에서 다룬 WinRM 포트가 열려 있는지 이름으로 바로 확인

Test-NetConnection -ComputerName "www.contoso.com" -DiagnoseRouting -InformationLevel Detailed   # 어떤 발신지 주소·경로가 선택됐는지까지 진단

Test-NetConnection -TraceRoute -Hops 15                                 # 최대 15홉까지 경로 추적
```

## 주의사항·함정

**`Test-NetConnection`은 Windows 전용이며 PowerShell 7의 크로스플랫폼 기반을 벗어난다**: NetTCPIP 모듈은 macOS/Linux의 pwsh에서 사용할 수 없다. 크로스플랫폼 스크립트를 작성한다면 109장의 `Test-Connection -TcpPort`로 대체하거나, 플랫폼을 분기해 Windows에서만 `Test-NetConnection`을 호출해야 한다.

**`-CommonTCPPort`는 4개 값(`HTTP`/`RDP`/`SMB`/`WINRM`)만 허용한다**: HTTPS(443)나 SSH(22) 같은 다른 흔한 포트는 이름으로 지정할 수 없고, 반드시 `-Port` 매개변수에 숫자를 직접 넣어야 한다. 문서화된 값 이외의 문자열을 넣으면 매개변수 검증 오류가 난다.

**`-InformationLevel Detailed` 없이는 진짜 진단 정보가 상당 부분 생략된다**: 기본 출력은 `PingSucceeded`나 `TcpTestSucceeded` 같은 요약 속성 위주라, `NameResolutionResults`·`NetRoute`·`MatchingIPsecRules` 같은 상세 필드를 보려면 명시적으로 `-InformationLevel Detailed`를 지정해야 한다. 문제를 깊이 파고들 필요가 없다면 기본 출력으로 충분하지만, 경로·DNS 문제를 진단할 때는 이 옵션을 빠뜨리기 쉽다.

**`-DiagnoseRouting`은 실제로 트래픽을 보내는 것이 아니라 "어떤 경로가 선택될지"를 시뮬레이션한다**: `RouteSelectionEvents`·`SourceAddressSelectionEvents` 출력은 라우팅 테이블과 정책에 따른 계산 결과이지, 대상이 실제로 응답했는지를 보장하지 않는다. 연결 자체가 되는지 확인하려면 `-Port`나 기본 ICMP 테스트를 함께 사용해야 한다.

**이식성**: `-Port`를 이용한 TCP 연결 테스트는 Linux의 `nc -zv <호스트> <포트>`나 `telnet <호스트> <포트>`와 목적이 같지만, `Test-NetConnection`은 여기에 더해 경로 선택·IPsec 규칙까지 한 번에 보여준다는 점에서 정보량이 훨씬 많다. `-TraceRoute`는 Windows CMD의 `tracert`, Linux의 `traceroute`와 대응하지만, PowerShell 객체이므로 결과를 `Where-Object`로 특정 홉만 걸러내는 등 후처리가 가능하다.

## Reference

- [Test-NetConnection (NetTCPIP) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection?view=windowsserver2025-ps)
