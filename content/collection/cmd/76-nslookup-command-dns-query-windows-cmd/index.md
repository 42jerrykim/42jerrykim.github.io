---
draft: false
slug: nslookup-command-dns-query-windows-cmd
title: "[CMD] 76. nslookup - DNS 질의와 인프라 진단"
description: "nslookup으로 도메인 이름과 IP 주소를 상호 조회하는 법과 비대화형·대화형 두 모드의 차이, timed out·No response·Nonexistent domain 등 오류 메시지가 가리키는 서로 다른 원인을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 760
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
- nslookup
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
- Beginner
- Administration
- Productivity(생산성)
- Workflow(워크플로우)
image: "wordcloud.png"
---

nslookup은 DNS(Domain Name System) 인프라를 진단하는 데 쓰는 정보를 표시하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [75장: netstat](/post/cmd/netstat-command-network-connections-windows-cmd/)에서 연결 상태를 다룬 뒤 이어진다. 73장(ping)에서 "IP 주소는 되는데 컴퓨터 이름은 안 되면 이름 확인 문제"라고 진단했던 상황을 실제로 파고드는 도구가 이 장의 nslookup이다.

**이 장의 깊이**: 중급–고급. **선행 지식**: DNS 동작 원리에 대한 기본적인 이해가 있으면 이 장을 훨씬 수월하게 소화할 수 있다.

## 개요 + 정신 모델

nslookup은 두 가지 모드로 동작한다는 것이 이 장의 핵심 정신 모델이다.

> "If you need to look up only a single piece of data, or you're using nslookup in scripts, command lines, or PowerShell, use the noninteractive mode. ... If you need to look up more than one piece of data or set several configurations, you can use interactive mode." — Microsoft Learn, "nslookup"

비대화형(명령) 모드는 한 줄로 결과를 즉시 얻는 스크립트 친화적 방식이고, 대화형 모드는 `>` 프롬프트에 들어가 여러 질의와 설정 변경을 연속으로 수행하는 방식이다. 첫 인자에 하이픈(`-`)을 주거나 인자 없이 `nslookup`만 실행하면 대화형 모드로 들어간다.

## 사용법

```
nslookup <컴퓨터이름> [<DNS서버>]
nslookup -<옵션> <컴퓨터이름>
nslookup -
nslookup
```

## 옵션

### 비대화형 모드

| 사용 | 설명 |
|---|---|
| `nslookup <이름> [서버]` | 첫 인자는 찾을 이름·IP, 두 번째(생략 가능)는 사용할 DNS 서버 |
| `nslookup -type=<레코드유형> <이름>` | 특정 리소스 레코드 유형만 조회(예: AAAA) |
| `nslookup -debug <이름>` | 주고받은 패킷에 대한 디버그 정보 표시 |

### 대화형 모드(주요 하위 명령)

| 하위 명령 | 역할 |
|---|---|
| `server <이름>` | 기본 DNS 서버 변경 |
| `set all` | 현재 설정 값 전체 표시 |
| `set type=<유형>` | 질의할 리소스 레코드 유형 변경 |
| `set timeout=<초>` | 응답 대기 시간 변경 |
| `set retry=<횟수>` | 재시도 횟수 설정 |
| `exit` | 대화형 모드 종료 |

## 예시

```
nslookup mydomain.com 1.1.1.1
nslookup 4.4.4.4
nslookup -debug mydomain.com
nslookup -type=AAAA mydomain.com
nslookup -debug -type=A+AAAA -nosearch -recurse mydomain.com 1.1.1.1
```

대화형 모드:

```
nslookup - 1.1.1.1
> set all
> mydomain.com
> server 4.4.4.4
> set type=HINFO
> exit
```

## 주의사항·함정

**오류 메시지마다 원인이 다르게 좁혀진다**: nslookup의 오류 메시지는 막연한 "실패"가 아니라 원인을 구체적으로 가리킨다.

| 오류 메시지 | 의미 |
|---|---|
| `timed out` | 서버가 일정 시간·재시도 내에 응답하지 않음 |
| `No response from server` | 그 서버에서 DNS 서비스 자체가 실행되지 않음 |
| `No records` | 이름은 유효하지만 현재 질의 유형의 레코드가 없음 |
| `Nonexistent domain` | 컴퓨터 또는 도메인 이름 자체가 존재하지 않음 |
| `Server failure` | DNS 서버 내부 데이터베이스 불일치 |

`No response from server`와 `Nonexistent domain`을 혼동하면 엉뚱한 곳(서버가 죽었다고 생각해 DNS 팀에 연락)을 고치려 들 수 있다 — 전자는 서버 자체의 문제, 후자는 애초에 존재하지 않는 이름을 찾고 있다는 뜻이다.

**대화형 모드에서 내장 명령을 컴퓨터 이름으로 쓰려면 이스케이프해야 한다**: `server`, `set`처럼 nslookup의 내장 하위 명령과 이름이 겹치는 호스트를 조회하려면, 이스케이프 문자(`\`)를 앞에 붙여야 한다 — 그렇지 않으면 nslookup이 호스트 이름이 아니라 명령으로 해석한다.

**마침표로 끝나지 않는 이름에는 기본 도메인이 자동으로 붙는다**: 조회할 이름이 마침표로 끝나지 않으면, `domain`·`srchlist`·`defname`·`search` 설정에 따라 기본 DNS 도메인 이름이 자동으로 뒤에 붙는다. 짧은 이름으로 조회했는데 예상과 다른 결과가 나온다면 이 자동 접미사 규칙을 의심해야 한다.

**PowerShell에서는 `Resolve-DnsName`을 쓴다**: PowerShell의 대응 명령은 `Resolve-DnsName`이며, nslookup처럼 사람이 읽는 텍스트 블록을 출력하는 대신 레코드 유형·TTL·주소 등을 속성으로 가진 객체를 반환한다. 스크립트에서 특정 레코드 값만 뽑아 쓰려면 `(Resolve-DnsName mydomain.com -Type AAAA).IPAddress`처럼 바로 접근할 수 있어, nslookup 출력을 문자열로 파싱하는 것보다 훨씬 안정적이다.

## 흔한 오개념

<strong>"nslookup이 실패하거나 응답이 없으면 대상 사이트·서버가 다운된 것이다"</strong>는 오해가 있다. nslookup이 진단하는 것은 어디까지나 이름을 IP로 바꾸는 DNS 조회 단계일 뿐이다 — DNS 서버 설정 오류, 전파 지연, 로컬 DNS 캐시 문제 등으로 이름 확인 자체가 실패해도 실제 서비스는 멀쩡히 떠 있을 수 있다. 이런 경우 IP 주소로 직접 접근하면(또는 73장의 ping으로 IP 자체를 확인하면) 서비스가 정상 응답한다는 것을 확인할 수 있다 — 문제는 서버가 아니라 이름과 IP를 잇는 DNS 단계에 있었던 것이다.

## 다음 장에서는

다음은 77장 — 네트워크 어댑터의 MAC 주소를 표시하는 `getmac` 명령을 다룬다.

## 평가 기준

- nslookup으로 도메인 이름과 IP 주소를 상호 조회할 수 있다.
- 비대화형·대화형 두 모드의 차이와 각각 언제 쓰는지 설명할 수 있다.
- `No response from server`와 `Nonexistent domain` 등 오류 메시지가 가리키는 서로 다른 원인을 구분할 수 있다.
- 마침표로 끝나지 않는 이름에 기본 도메인이 자동으로 붙는다는 것을 안다.

## 참고

- [nslookup | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/nslookup)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
