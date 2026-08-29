---
draft: false
slug: ping-command-test-network-connectivity-windows-cmd
title: "[CMD] 73. ping - 대상 호스트 연결 확인"
description: "ping으로 ICMP 에코 요청을 보내 다른 호스트와의 IP 수준 연결을 확인하는 법과 IP 주소는 되는데 컴퓨터 이름은 안 되면 이름 확인 문제라는 진단 원리, /t 무한 반복과 /f로 PMTU 문제를 진단하는 법을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 730
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
- ping
- ICMP
- Networking(네트워킹)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Linux(리눅스)
- Education(교육)
- CLI
- DNS
- Configuration(설정)
- Advanced
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

ping은 ICMP 에코 요청 메시지를 보내 다른 TCP/IP 컴퓨터와의 IP 수준 연결을 확인하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [72장: ipconfig](/post/cmd/ipconfig-command-network-configuration-windows/)에서 내 쪽 네트워크 설정을 확인하는 법을 다룬 뒤 이어진다. ipconfig로 내 설정을 확인했다면, ping은 그 설정으로 실제 다른 호스트에 도달할 수 있는지 검증하는 첫 단계다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
ping [/t] [/a] [/n <횟수>] [/l <크기>] [/f] [/i <TTL>] [/r <횟수>] [/w <제한시간>] [/4] [/6] <대상이름>
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/t` | 중단할 때까지 계속 전송(Ctrl+Break로 통계 표시, Ctrl+C로 종료) |
| `/a` | 대상 IP의 역방향 이름 확인 수행 |
| `/n <횟수>` | 보낼 에코 요청 수(기본 4) |
| `/l <크기>` | 데이터 필드 크기(바이트, 기본 32, 최대 65500) |
| `/f` | Do not Fragment 플래그 설정(IPv4 전용, PMTU 문제 진단용) |
| `/i <TTL>` | IP 헤더의 Time To Live 값(최대 255) |
| `/r <횟수>` | 왕복 경로를 기록(IPv4 전용, 1–9) |
| `/w <제한시간>` | 응답 대기 시간(ms, 기본 4000) |
| `/4` \| `/6` | IPv4·IPv6 강제 지정(이름으로 대상을 지정할 때만 필요) |

## 예시

```
ping example.microsoft.com
ping /a 10.0.99.221
ping /n 10 /l 1000 10.0.99.221
ping /r 4 10.0.99.221
ping /t 8.8.8.8
```

## 주의사항·함정

**컴퓨터 이름 확인이 다르면 이름 확인 문제를 의심한다**: ping은 연결 자체뿐 아니라 이름 확인 진단에도 쓰인다.

> "You can also use this command to test both the computer name and the IP address of the computer. If pinging the IP address is successful, but pinging the computer name isn't, you might have a name resolution problem." — Microsoft Learn, "ping"

즉 `ping 8.8.8.8`은 되는데 `ping example.com`은 안 된다면, 네트워크 연결 자체는 정상이고 문제는 이름을 IP로 바꾸는 단계(로컬 Hosts 파일, DNS, NetBIOS)에 있다는 뜻이다 — 76장(nslookup)이 바로 이 단계를 더 깊이 진단하는 도구다.

**`/f`는 PMTU 문제를 찾는 전용 도구다**: Do not Fragment 플래그를 설정하면, 경로상의 라우터가 패킷을 조각내지 않고 그대로 전달해야 한다. 이 상태에서 특정 크기 이상의 패킷이 실패하기 시작하는 지점을 찾으면, 경로의 최대 전송 단위(PMTU)를 역산할 수 있다 — VPN이나 터널링 환경에서 특정 크기 이상의 트래픽만 실패하는 문제를 진단할 때 유용하다.

**기본 4회로는 간헐적 문제를 놓치기 쉽다**: 기본 횟수(4회)만으로는 가끔 발생하는 패킷 손실을 포착하지 못할 수 있다. `/t`로 계속 실행하며 패턴을 관찰하거나, `/n`으로 횟수를 늘려 통계적으로 더 신뢰할 수 있는 손실률을 확인하는 것이 안정성 문제 진단에 유리하다.

**응답이 없어도 반드시 네트워크 문제는 아니다**: 많은 방화벽·보안 장비가 ICMP 트래픽 자체를 차단하도록 설정되어 있다. ping이 실패한다고 해서 대상 서버가 완전히 다운되었다고 단정할 수 없다 — 같은 대상에 다른 프로토콜(HTTP 등)로 접근이 되는지 함께 확인해야 한다.

**PowerShell에서는 `Test-Connection`을 쓴다**: PowerShell의 대응 명령은 `Test-Connection`이며, TCP 포트 단위까지 확인하려면 `Test-NetConnection`을 함께 고려할 수 있다. 가장 큰 차이는 출력 형태다 — ping은 텍스트를 그대로 화면에 뿌리므로 스크립트에서 쓰려면 문자열을 파싱해야 하지만, `Test-Connection`은 속성을 가진 객체를 반환하므로 `$result.Latency`처럼 값을 바로 꺼내 조건문이나 로깅에 쓸 수 있다.

## 흔한 오개념

<strong>"ping이 성공하면 그 서버는 정상적으로 동작하고 있다"</strong>는 오해가 흔하다. ping이 확인하는 것은 ICMP 수준의 네트워크 도달 가능성뿐이다. 대상 호스트가 ICMP 에코 요청에 응답한다고 해서 그 위에서 돌아가는 실제 서비스(웹 서버, 데이터베이스 등)까지 정상이라는 보장은 없다 — 해당 서비스가 다운되었거나, 설정이 잘못되었거나, 애플리케이션 수준 방화벽에 막혀 있어도 ICMP 응답 자체는 문제없이 돌아올 수 있다. 연결 확인과 서비스 정상 여부는 서로 다른 계층의 질문이다.

## 다음 장에서는

다음은 74장 — 대상까지 패킷이 거치는 경로를 홉 단위로 추적하는 `tracert` 명령을 다룬다.

## 평가 기준

- ping으로 대상 호스트와의 연결을 확인하고 `/n`·`/l`·`/t`로 테스트 강도를 조정할 수 있다.
- IP 주소는 되는데 컴퓨터 이름은 안 될 때 이름 확인 문제를 의심하는 진단 논리를 설명할 수 있다.
- `/f`로 PMTU 문제를 진단하는 원리를 안다.
- ICMP가 방화벽에 차단될 수 있어 ping 실패가 곧 서버 다운을 의미하지 않는다는 것을 안다.

## 참고

- [ping | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ping)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
