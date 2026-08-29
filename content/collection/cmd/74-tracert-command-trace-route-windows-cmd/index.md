---
draft: false
slug: tracert-command-trace-route-windows-cmd
title: "[CMD] 74. tracert - 패킷 경로 추적"
description: "tracert로 대상까지 패킷이 거치는 경로를 홉 단위로 추적하는 법과 TTL을 1씩 늘려가며 ICMP 시간 초과 메시지로 경로를 알아내는 원리, 일부 라우터가 응답하지 않아 별표로 표시되는 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 740
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
- Advanced
- tracert
- 경로추적
- ICMP
- Networking(네트워킹)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Linux(리눅스)
- Education(교육)
- CLI
- Configuration(설정)
- Beginner
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

tracert는 대상까지 도달하는 경로를 점진적으로 증가하는 TTL 값의 ICMP 에코 요청으로 알아내는 진단 도구다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [73장: ping](/post/cmd/ping-command-test-network-connectivity-windows-cmd/)에서 대상까지의 연결 여부를 확인하는 법을 다룬 뒤 이어진다. ping이 "도달하는가"만 답했다면, tracert는 "어느 경로로, 어디까지 도달하는가"를 홉 단위로 보여준다.

**이 장의 깊이**: 중급.

## 개요 + 정신 모델

tracert의 핵심 원리는 IP 헤더의 TTL(Time To Live) 필드를 의도적으로 조작하는 것이다.

> "Each router along the path is required to decrement the TTL in an IP packet by at least 1 before forwarding it. ... When the TTL on a packet reaches 0, the router is expected to return an ICMP time Exceeded message to the source computer." — Microsoft Learn, "tracert"

tracert는 이 성질을 역이용한다. TTL을 1로 설정한 첫 패킷을 보내면 첫 번째 라우터에서 TTL이 0이 되어 "시간 초과" 메시지가 돌아오고, 그 라우터의 주소를 알 수 있다. 다음에는 TTL을 2로 보내 두 번째 라우터의 응답을 받고, 이런 식으로 TTL을 1씩 늘려가며 대상에 도달할 때까지(또는 최대 홉 수에 이를 때까지) 반복한다.

## 사용법

```
tracert [/d] [/h <최대홉수>] [/j <호스트목록>] [/w <제한시간>] [/4] [/6] <대상이름>
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/d` | 중간 라우터의 IP를 이름으로 확인하지 않음(결과 반환 속도 향상) |
| `/h <최대홉수>` | 최대 홉 수(기본 30) |
| `/j <호스트목록>` | Loose Source Route 옵션으로 중간 경유지 지정(IPv4 전용) |
| `/w <제한시간>` | 각 요청의 응답 대기 시간(ms, 기본 4000) |
| `/4` \| `/6` | IPv4·IPv6 강제 지정 |

## 예시

```
tracert www.microsoft.com
tracert /d www.microsoft.com
tracert /h 15 www.microsoft.com
```

## 주의사항·함정

**일부 라우터는 응답하지 않고 별표(`*`)로 표시된다**: 모든 라우터가 시간 초과 메시지를 반환하는 것은 아니다.

> "However, some routers don't return time Exceeded messages for packets with expired TTL values and are invisible to the **tracert** command. In this case, a row of asterisks (\*) is displayed for that hop." — Microsoft Learn, "tracert"

즉 특정 홉이 별표로만 나온다고 해서 그 구간에서 패킷이 실제로 사라졌다는 뜻은 아니다 — 그 라우터가 ICMP 시간 초과 응답 자체를 보내지 않도록 설정되어 있을 뿐, 패킷은 계속 다음 홉으로 전달되고 있을 수 있다. 최종 목적지까지 도달했는지(`Trace complete`)가 더 중요한 판단 기준이다.

**`/d`로 속도를 높일 수 있다**: 각 홉의 IP를 사람이 읽기 쉬운 이름으로 역방향 확인하는 과정이 매 홉마다 지연을 유발한다. 빠른 결과가 급하다면 `/d`로 이 확인을 건너뛰고 IP 주소만 볼 수 있다.

**표시되는 것은 "가까운 쪽" 인터페이스다**: 각 홉에 나오는 주소는 그 라우터의 여러 인터페이스 중, 패킷을 보낸 쪽에 더 가까운 인터페이스를 가리킨다. 라우터 하나가 여러 IP를 가질 수 있으므로, tracert 결과의 IP가 그 라우터의 "유일한 주소"라고 오해하면 안 된다.

**더 정밀한 진단에는 pathping이 있다**: tracert는 경로만 보여주지만, 각 구간의 지연·패킷 손실률까지 정량적으로 측정하려면 Microsoft Learn도 추천하는 `pathping` 명령을 대신 고려할 수 있다 — 이 컬렉션에서는 별도로 다루지 않지만, tracert로 경로를 먼저 확인한 뒤 특정 구간이 의심스러우면 pathping으로 더 깊이 들어가는 흐름이 실무에서 자연스럽다.

**PowerShell에서는 경로 추적 기능이 별도 명령이 아니라 옵션으로 붙는다**: PowerShell의 대응 기능은 `Test-NetConnection -TraceRoute`이며(최신 PowerShell 버전에서는 `Test-Connection -TraceRoute`도 쓸 수 있다), tracert처럼 한 줄씩 출력되는 텍스트가 아니라 홉 목록을 구조화된 데이터로 반환한다. 즉 `(Test-NetConnection example.com -TraceRoute).TraceRoute`처럼 홉 IP 배열을 바로 변수에 담아 스크립트에서 순회·비교할 수 있다는 점이 tracert의 텍스트 출력과 다르다.

## 흔한 오개념

<strong>"각 홉에 표시되는 응답 시간이 그 라우터의 실제 패킷 전달 성능을 보여준다"</strong>는 오해가 흔하다. 많은 라우터는 ICMP 시간 초과 응답 생성을 의도적으로 낮은 우선순위로 처리한다 — 그런 응답을 만드는 일이 라우터 본연의 업무인 실제 트래픽 전달과 자원을 다투기 때문이다. 따라서 특정 홉에서 응답 시간이 유난히 길거나 아예 응답이 없다고 해서 그 라우터가 실제 TCP·UDP 트래픽을 전달할 때도 느리다는 뜻은 아니다 — 그 라우터는 진짜 데이터는 문제없이 빠르게 전달하면서, ICMP 시간 초과 응답만 느리게 보내거나 아예 보내지 않도록 설정되어 있을 수 있다.

## 다음 장에서는

다음은 75장 — 활성 연결과 리스닝 포트를 표시하는 `netstat` 명령을 다룬다.

## 평가 기준

- tracert로 대상까지의 경로를 홉 단위로 추적할 수 있다.
- TTL을 1씩 늘려가며 ICMP 시간 초과 메시지로 경로를 알아내는 원리를 설명할 수 있다.
- 별표(`*`)로 표시된 홉이 반드시 패킷 손실을 의미하지 않는 이유를 설명할 수 있다.
- 더 정밀한 구간별 지연·손실 측정이 필요할 때 pathping을 고려할 수 있다는 것을 안다.

## 참고

- [tracert | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tracert)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
