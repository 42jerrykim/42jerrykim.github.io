---
draft: false
slug: ipconfig-command-network-configuration-windows
title: "[CMD] 72. ipconfig - TCP/IP 네트워크 구성 확인"
description: "ipconfig로 IPv4·IPv6 주소·서브넷 마스크·기본 게이트웨이를 확인하는 법과 /all로 전체 구성을 보는 차이, DHCP 임대를 갱신·해제하는 /renew·/release, DNS 캐시를 지우는 /flushdns를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 720
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
- ipconfig
- 네트워크설정
- TCP/IP
- DHCP
- DNS
- Networking(네트워킹)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Linux(리눅스)
- Education(교육)
- CLI
- Configuration(설정)
- Advanced
image: "wordcloud.png"
---

ipconfig는 현재 TCP/IP 네트워크 구성 값을 표시하고, DHCP·DNS 설정을 갱신하는 명령이다. Part 8(네트워크와 원격 진단)의 첫 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [71장: color](/post/cmd/color-command-console-colors-windows-cmd/)로 Part 7(시스템 정보와 구성)을 마친 뒤 이어지며, <strong>Part 8(네트워크와 원격 진단)</strong>의 첫 장이다. 지금까지 로컬 시스템의 상태를 진단했다면, 이 장부터는 그 시스템이 네트워크 너머와 어떻게 연결되어 있는지를 다룬다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 다른 호스트까지의 연결 자체를 확인하는 것은 73장(ping)에서, 경로를 추적하는 것은 74장(tracert)에서 각각 다룬다. ipconfig는 "내 쪽 설정이 무엇인가"에 범위를 한정한다.

## 사용법

```
ipconfig [/allcompartments] [/all] [/renew [<어댑터>]] [/release [<어댑터>]] [/flushdns] [/displaydns] [/registerdns] [/showclassid <어댑터>] [/setclassid <어댑터> [<classID>]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| (없음) | 모든 어댑터의 IPv4·IPv6 주소, 서브넷 마스크, 기본 게이트웨이 표시 |
| `/all` | 모든 어댑터의 전체 TCP/IP 구성 표시 |
| `/release [어댑터]` | DHCP 서버에 DHCPRELEASE 전송, IP 주소 구성 폐기 |
| `/renew [어댑터]` | DHCP 구성 갱신(자동 IP 할당 어댑터에서만 가능) |
| `/flushdns` | DNS 클라이언트 확인자 캐시를 지우고 초기화 |
| `/displaydns` | DNS 확인자 캐시 내용 표시 |
| `/registerdns` | DNS 이름·IP 주소를 수동으로 동적 등록 |
| `/showclassid <어댑터>` | 지정 어댑터의 DHCP 클래스 ID 표시 |
| `/setclassid <어댑터> [ID]` | 지정 어댑터의 DHCP 클래스 ID 설정(생략 시 제거) |

## 예시

```
ipconfig
ipconfig /all
ipconfig /renew "Local Area Connection"
ipconfig /flushdns
ipconfig /displaydns
ipconfig /showclassid Local*
ipconfig /setclassid "Local Area Connection" TEST
```

## 주의사항·함정

**자동 IP 할당 환경에서 가장 유용하다**: ipconfig는 DHCP·APIPA(자동 사설 IP 할당)·대체 구성 중 어느 것이 실제로 적용되었는지 사용자가 직접 판단할 수 있게 해준다.

> "This command is most useful on computers that are configured to obtain an IP address automatically. This enables users to determine which TCP/IP configuration values have been configured by DHCP, Automatic Private IP Addressing (APIPA), or an alternate configuration." — Microsoft Learn, "ipconfig"

정적 IP를 수동으로 설정한 환경에서는 ipconfig의 진단 가치가 상대적으로 낮아진다 — 이미 설정한 값이 그대로 보일 뿐이기 때문이다.

**어댑터 이름에 공백이 있으면 따옴표가 필요하다**: `Local Area Connection`처럼 공백이 포함된 어댑터 이름을 지정할 때는 반드시 따옴표로 감싸야 한다. 08장(cd)에서 배운 공백 경로 처리 규칙과 같은 원리다.

**어댑터 이름에 와일드카드를 쓸 수 있다**: `Local*`처럼 접두어로 시작하는 이름을, `*Con*`처럼 포함하는 이름을 각각 매칭할 수 있다 — 09장(dir)의 파일 와일드카드와 비슷한 감각으로 여러 어댑터를 한 번에 지정할 수 있다.

**DNS 문제 진단에는 `/flushdns`가 먼저다**: 이름 확인이 이상하게 동작할 때, 오래된 캐시된 항목(부정적 캐시 포함)을 지우는 것이 가장 먼저 시도해볼 조치다. 캐시를 지운 뒤에도 같은 문제가 재현되면 DNS 서버 자체나 네트워크 경로 문제로 좁혀갈 수 있다.

**PowerShell에는 더 세분화된 대응 cmdlet들이 있다**: 기본 `ipconfig`에 대략 대응하는 것은 `Get-NetIPConfiguration`이고, `/all`에 해당하는 더 상세한 정보는 `Get-NetIPAddress`나 `Get-DnsClientServerAddress`로 나누어 조회한다. `/flushdns`에 대응하는 것은 `Clear-DnsClientCache`다. ipconfig가 하나의 명령에 정보를 모아 텍스트로 쏟아낸다면, PowerShell 쪽은 목적별로 cmdlet이 나뉘어 있는 대신 각 결과가 객체로 반환되어 `Select-Object`나 `Where-Object`로 원하는 필드만 골라 스크립트에 바로 활용하기 쉽다.

## 흔한 오개념

<strong>"ipconfig는 유닉스의 ifconfig와 완전히 같은 명령이다"</strong>는 오해가 있다. 이름은 비슷하지만 ipconfig는 DHCP 임대 갱신·DNS 캐시 관리 같은 Windows 고유 기능까지 포함한 훨씬 넓은 범위의 명령이고, 유닉스 계열의 `ifconfig`(또는 최신 배포판의 `ip` 명령)는 주로 인터페이스 자체의 활성화·주소 할당에 집중한다. 옵션 체계도 완전히 다르므로 한쪽 지식을 다른 쪽에 그대로 옮길 수 없다.

## 다음 장에서는

다음은 73장 — ICMP로 다른 호스트와의 연결을 확인하는 `ping` 명령을 다룬다.

## 평가 기준

- ipconfig로 네트워크 구성을 조회하고 `/all`로 상세 정보를 볼 수 있다.
- `/release`·`/renew`로 DHCP 임대를 해제·갱신할 수 있다.
- `/flushdns`가 DNS 문제 진단에서 왜 첫 조치로 쓰이는지 설명할 수 있다.
- ipconfig와 유닉스 `ifconfig`가 이름만 비슷할 뿐 범위가 다르다는 것을 안다.

## 참고

- [ipconfig | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
