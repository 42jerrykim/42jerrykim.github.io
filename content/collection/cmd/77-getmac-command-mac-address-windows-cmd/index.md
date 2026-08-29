---
draft: false
slug: getmac-command-mac-address-windows-cmd
title: "[CMD] 77. getmac - 네트워크 어댑터 MAC 주소 표시"
description: "getmac으로 로컬·원격 컴퓨터 네트워크 어댑터의 MAC 주소와 연결된 프로토콜 목록을 조회하는 법과 네트워크 분석기에 주소를 입력하거나 어댑터별 사용 프로토콜을 확인하는 실전 용도를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 770
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
- getmac
- MAC주소
- Networking(네트워킹)
- Hardware
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Security(보안)
- Configuration(설정)
- Advanced
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

getmac은 로컬 또는 원격의 모든 네트워크 카드에 대해 매체 액세스 제어(MAC) 주소와 그 주소에 연결된 네트워크 프로토콜 목록을 반환하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [76장: nslookup](/post/cmd/nslookup-command-dns-query-windows-cmd/)에서 DNS 진단을 다룬 뒤 이어진다. 지금까지 IP 계층 위주로 네트워크를 진단했다면, getmac은 그보다 한 단계 아래인 하드웨어 주소(MAC) 계층을 다룬다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
getmac[.exe] [/s <컴퓨터> [/u <도메인>\<사용자> [/p <비밀번호>]]] [/fo {table | list | csv}] [/nh] [/v]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/s <컴퓨터>` | 원격 컴퓨터 이름·IP(기본은 로컬) |
| `/u <도메인>\<사용자>` | 원격 조회 시 사용할 계정 |
| `/p <비밀번호>` | `/u` 계정의 비밀번호 |
| `/fo table\|list\|csv` | 출력 형식(기본 table) |
| `/nh` | 열 머리글 생략(table·csv일 때 유효) |
| `/v` | 상세 정보 표시 |

## 예시

```
getmac
getmac /fo table /nh /v
getmac /s srvmain
getmac /s srvmain /u maindom\hiropln /p p@ssW23
getmac /s srvmain /u maindom\hiropln /p p@ssW23 /fo list /v
```

## 주의사항·함정

**언제 이 명령을 쓰는지가 명확하게 문서화되어 있다**: Microsoft Learn은 getmac의 용도를 두 가지로 구체적으로 짚는다.

> "This command is particularly useful either when you want to enter the MAC address into a network analyzer, or when you need to know what protocols are currently in use on each network adapter on a computer." — Microsoft Learn, "getmac"

즉 네트워크 분석기(패킷 캡처 도구 등)에 특정 어댑터의 MAC 주소를 필터 조건으로 입력해야 할 때, 또는 한 컴퓨터의 여러 네트워크 어댑터 각각이 어떤 프로토콜을 쓰고 있는지 확인해야 할 때가 이 명령의 전형적인 사용 시점이다.

**여러 어댑터가 있으면 각각 별도로 표시된다**: 물리 네트워크 카드가 여러 개거나 가상 어댑터(VPN, 가상머신 네트워크 등)가 함께 있는 컴퓨터에서는, 각 어댑터의 MAC 주소와 프로토콜 목록이 개별 행으로 나온다 — 어떤 어댑터가 실제로 트래픽을 처리하고 있는지 구분하려면 `/v`로 상세 정보를 함께 봐야 할 수 있다.

**원격 조회 옵션은 다른 명령들과 동일한 패턴이다**: `/s`, `/u`, `/p` 조합은 54장(tasklist)·63장(systeminfo)·65장(driverquery)에서 이미 본 것과 완전히 같은 문법이다 — 한 번 익힌 패턴을 이 컬렉션의 여러 원격 조회 명령에 그대로 재사용할 수 있다.

**결과가 비어 있거나 예상과 다른 어댑터만 나올 수 있다**: 비활성화된 물리 NIC, 연결이 끊긴 어댑터, VPN·Hyper-V 가상 스위치 같은 가상 어댑터는 겉보기엔 목록에 있어도 실제로는 트래픽을 처리하지 않는 오래된(stale) MAC 주소를 그대로 보여줄 수 있고, 반대로 정작 찾으려는 물리 어댑터가 비활성 상태라 아예 목록에서 빠질 수도 있다. `/v`로 상세 정보를 함께 보면 각 어댑터의 연결 상태·전송 이름까지 나오므로, 어떤 항목이 실제로 활성 상태인지와 단순히 존재만 하는지를 구분하는 데 도움이 된다.

**PowerShell에서는 `Get-NetAdapter`를 쓴다**: PowerShell의 대응 명령은 `Get-NetAdapter | Select-Object Name, MacAddress`이며, getmac이 MAC 주소와 프로토콜 목록만 나열하는 것과 달리 어댑터 상태(Up/Disabled/Disconnected)·링크 속도 같은 정보까지 한 번에 보여준다. 앞서 언급한 "비활성 어댑터가 결과에 섞여 있는지" 문제를 진단할 때, `Get-NetAdapter`의 상태 컬럼이 getmac의 `/v`보다 더 직접적인 판단 근거가 된다.

## 흔한 오개념

<strong>"getmac이 보여주는 MAC 주소는 하드웨어에 각인된, 변하지 않는 고유값이다"</strong>는 오해가 있다. 많은 최신 어댑터, 특히 VPN·가상머신·가상 스위치 같은 가상 어댑터는 하드웨어 제조사가 구워 넣은(burned-in) 주소가 아니라 운영체제나 드라이버가 소프트웨어적으로 지정한(locally administered) MAC 주소를 쓴다. 따라서 getmac 출력을 "이 컴퓨터의 물리 NIC 공장 주소"로 단정해 자산 관리나 필터링에 그대로 쓰면, 실제 하드웨어 주소와 다른 값을 기준으로 삼는 오류가 생길 수 있다.

## 다음 장에서는

다음은 78장 — Part 8의 마지막 장으로, 로컬·도메인 사용자 계정을 관리하는 `net user` 명령을 다룬다.

## 평가 기준

- getmac으로 로컬·원격 컴퓨터의 MAC 주소와 연결된 프로토콜을 조회할 수 있다.
- getmac이 실무에서 쓰이는 두 가지 대표적인 상황(네트워크 분석기 필터, 어댑터별 프로토콜 확인)을 설명할 수 있다.
- 여러 어댑터가 있는 컴퓨터에서 결과가 어떻게 표시되는지 안다.

## 참고

- [getmac | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/getmac)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
