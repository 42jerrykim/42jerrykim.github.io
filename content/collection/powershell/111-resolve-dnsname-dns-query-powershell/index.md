---
draft: true
collection_order: 111
slug: resolve-dnsname-dns-query-powershell
title: "[PowerShell] 111. Resolve-DnsName — DNS 질의"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell의 DnsClient 모듈 Resolve-DnsName이 nslookup 대신 A/AAAA/MX/TXT 등 다양한 레코드 타입을 객체로 조회하고 -Server로 특정 DNS 서버에 질의하는 방법을 정리한 챕터다."
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
- Resolve-DnsName
- DNS
- DNS-Record
- Nslookup
- DnsClient-Module
- DNS-Lookup
image: "wordcloud.png"
---

## 개요

<strong>Resolve-DnsName</strong>은 이름을 IP 주소로, 혹은 그 반대로 변환하는 DNS 질의를 수행하는 cmdlet으로, 전통적인 `nslookup` 도구의 기능적 대응물이다. 109–110장이 "그 대상에 도달할 수 있는가"를 다뤘다면, 이 장은 그보다 한 단계 앞선 질문인 "그 이름은 어떤 주소를 가리키는가"를 다룬다 — 네트워크 문제의 상당수가 연결 자체가 아니라 이름 해석 단계에서 발생하기 때문에, 진단 순서상 `Resolve-DnsName`을 먼저 확인하는 경우가 많다.

정신 모델은 "`nslookup`이 대화형 프롬프트에서 텍스트 답을 주는 전화번호부 문의라면, `Resolve-DnsName`은 그 답을 `Microsoft.DnsClient.Commands.DnsRecord` 객체로 돌려줘 `Where-Object`로 특정 레코드 타입만 걸러내거나 `Select-Object`로 필요한 필드만 뽑아낼 수 있게 한다"는 것이다.

## 사용법

```powershell
Resolve-DnsName -Name <조회할이름> [-Type <레코드타입>] [-Server <DNS서버>]
```

## 종류

| 주요 `-Type` 값 | 의미 |
|---|---|
| `A_AAAA`(기본) | IPv4·IPv6 주소 모두 질의 |
| `A` | IPv4 주소만 |
| `AAAA` | IPv6 주소만 |
| `MX` | 메일 라우팅 정보 |
| `TXT` | 텍스트 레코드(SPF, 도메인 검증 등) |
| `NS` | 네임 서버 |
| `CNAME` | 정규 이름(별칭) |
| `SOA` | 존(zone)의 권한 시작 정보 |
| `PTR` | 역방향 조회(IP → 이름) |
| `ANY`/`ALL` | 모든 레코드 타입 와일드카드 질의 |

| 기타 매개변수 | 의미 |
|---|---|
| `-Server` | 조회할 DNS 서버를 명시적으로 지정(기본은 인터페이스에 설정된 DNS 서버) |
| `-DnsOnly` | LLMNR·NetBIOS를 쓰지 않고 DNS 프로토콜만 사용 |
| `-CacheOnly` | 로컬 캐시만 조회(실제 네트워크 질의 없음) |
| `-NoRecursion` | 서버에 재귀 질의를 하지 말라고 지시 |

## 예시

```powershell
Resolve-DnsName -Name www.bing.com                          # 기본 A_AAAA 질의

Resolve-DnsName -Name www.bing.com -Type A                   # IPv4 주소만 명시적으로 질의

Resolve-DnsName -Name contoso.com -Type MX                    # 메일 서버(MX 레코드) 확인

Resolve-DnsName -Name contoso.com -Type TXT                   # SPF/도메인 검증용 TXT 레코드 확인

Resolve-DnsName -Name www.bing.com -Server 10.0.0.1            # 사내 DNS 서버 10.0.0.1에 직접 질의(공용 DNS와 응답 비교 시 유용)

Resolve-DnsName -Name www.bing.com -DnsOnly                    # LLMNR/NetBIOS 폴백 없이 순수 DNS 프로토콜로만 질의

(Resolve-DnsName -Name www.bing.com -Type A).IPAddress          # 객체 속성으로 IP 주소만 바로 추출(89장식 파이프라인 사고)
```

## 주의사항·함정

**`Resolve-DnsName`은 Windows 전용이며 DnsClient 모듈에 속한다**: `nslookup`이나 `dig`와 달리 macOS/Linux의 pwsh에는 이 cmdlet이 없다. 크로스플랫폼 스크립트에서는 .NET의 `[System.Net.Dns]::GetHostAddresses()`를 직접 호출하거나 플랫폼별로 분기해야 한다.

**기본 `-Type`(`A_AAAA`)은 IPv4와 IPv6를 동시에 반환하므로 결과가 예상보다 많을 수 있다**: 특정 레코드 타입만 필요하다면 `-Type A`처럼 명시적으로 좁혀야 한다. 반환된 객체는 `Type` 속성(`A`, `AAAA`, `CNAME` 등)이 서로 다르므로, 후속 처리에서 `Where-Object { $_.Type -eq 'A' }`로 걸러내는 패턴이 자주 필요하다.

**`-Server`를 지정하지 않으면 조회 결과가 로컬 DNS 캐시나 사내 DNS 서버의 응답에 좌우된다**: 공용 DNS 서버(예: 8.8.8.8)에서 보이는 실제 인터넷 상의 응답과, 조직 내부 DNS 서버가 돌려주는 응답(내부 전용 레코드나 스플릿 DNS 설정)이 다를 수 있다. DNS 전파 문제를 조사할 때는 `-Server`로 여러 서버에 동일한 이름을 질의해 결과를 비교해야 한다.

**`-CacheOnly`를 빼먹으면 매 호출마다 실제 네트워크 질의가 나가 응답이 느려질 수 있다**: 대량의 이름을 반복적으로 조회하는 스크립트에서는 로컬 DNS 캐시(`Get-DnsClientCache`로 확인 가능)를 먼저 활용하는 편이 효율적이다. 다만 캐시된 값은 TTL이 지나면 만료되므로, 최신 상태가 중요하다면 캐시를 신뢰하지 말고 매번 질의해야 한다.

**이식성**: Linux/macOS의 `dig`는 `dig contoso.com MX +short`처럼 옵션이 훨씬 세분화돼 있고 원시 프로토콜 수준의 정보(응답 시간, 플래그 비트 등)를 자세히 보여주는 반면, `Resolve-DnsName`은 그 결과를 구조화된 객체로 바로 반환한다는 점이 강점이다. `nslookup`은 Windows·Linux 양쪽에 모두 존재하는 몇 안 되는 크로스플랫폼 DNS 도구지만 대화형 텍스트 출력만 제공하므로, 스크립트에서 파싱해야 하는 CMD식 접근에 여전히 머물러 있다.

## Reference

- [Resolve-DnsName (DnsClient) | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/dnsclient/resolve-dnsname?view=windowsserver2025-ps)
