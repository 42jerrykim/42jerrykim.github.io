---
draft: false
slug: netstat-command-network-connections-windows-cmd
title: "[CMD] 75. netstat - 활성 연결과 리스닝 포트 조회"
description: "netstat으로 활성 TCP 연결, 리스닝 포트, 라우팅 테이블을 조회하는 법과 -o로 프로세스 ID를 확인해 taskkill과 연계하는 실전 패턴, -b가 시간이 걸리고 권한이 필요한 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 750
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
- netstat
- 네트워크연결
- TCP/IP
- Networking(네트워킹)
- Process
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
image: "wordcloud.png"
---

netstat은 활성 TCP 연결, 컴퓨터가 리스닝 중인 포트, 이더넷 통계, IP 라우팅 테이블, IPv4·IPv6 프로토콜별 통계를 표시하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [74장: tracert](/post/cmd/tracert-command-trace-route-windows-cmd/)에서 경로 추적을 다룬 뒤 이어진다. tracert가 "밖으로 나가는 경로"를 봤다면, netstat은 "지금 이 컴퓨터 자체가 맺고 있는 연결과 열어 둔 포트"를 보여준다. 54장(tasklist)·55장(taskkill)에서 다룬 프로세스 관리와 이 장을 조합하면, 어떤 프로세스가 어떤 네트워크 연결을 쓰고 있는지 추적할 수 있다.

**이 장의 깊이**: 중급.

## 사용법

```
netstat [-a] [-b] [-e] [-n] [-o] [-p <프로토콜>] [-r] [-s] [<간격>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| (없음) | 활성 TCP 연결 표시 |
| `-a` | 모든 활성 TCP 연결과 리스닝 중인 TCP·UDP 포트 표시 |
| `-b` | 각 연결·리스닝 포트를 만든 실행 파일 표시(시간이 걸리고 충분한 권한 필요) |
| `-e` | 이더넷 통계(송수신 바이트·패킷 수). `-s`와 조합 가능 |
| `-n` | 주소·포트를 이름으로 확인하지 않고 숫자로 표시 |
| `-o` | 각 연결의 프로세스 ID(PID) 포함(`-a`, `-n`, `-p`와 조합 가능) |
| `-p <프로토콜>` | 지정 프로토콜(tcp, udp, tcpv6, udpv6)만 표시 |
| `-r` | IP 라우팅 테이블 표시(`route print`와 동일) |
| `-s` | 프로토콜별 통계 표시(기본 TCP·UDP·ICMP·IP, IPv6 설치 시 해당 통계도) |
| `<간격>` | 지정한 초마다 다시 표시(Ctrl+C로 중단) |

### 상태(State) 값

| 상태 | 의미 |
|---|---|
| LISTEN | 연결 대기 중 |
| ESTABLISHED | 연결 수립됨 |
| TIME_WAIT | 연결 종료 후 대기 |
| CLOSE_WAIT | 상대가 연결을 닫음, 로컬의 닫기 대기 중 |

## 예시

```
netstat
netstat -a
netstat -n -o
netstat -o 5
netstat -e -s
netstat -s -p tcp
netstat -ano | findstr :443
```

## 주의사항·함정

**`-o`로 PID를 확인하면 taskkill·작업 관리자와 바로 연계할 수 있다**: `netstat -ano`(예시 마지막 줄)로 나온 PID를, 55장(taskkill)의 `taskkill /pid`나 Windows 작업 관리자의 프로세스 탭에서 찾으면 "어떤 프로그램이 이 포트를 점유하고 있는가"를 정확히 특정할 수 있다. `-o`는 `-a`, `-n`, `-p`와 조합할 수 있어 실무에서는 거의 항상 `-ano`처럼 함께 쓰인다.

**`-b`는 느리고 권한이 필요하다**: 각 연결을 만든 실행 파일을 추적하는 것은 시스템 호출 비용이 커서 다른 옵션보다 눈에 띄게 느리고, 충분한 권한이 없으면 그냥 실패한다.

> "Note that this option can be time-consuming and will fail unless you have sufficient permissions." — Microsoft Learn, "netstat"

관리자 권한 없이 `-b`를 실행하면 오류 없이 조용히 정보가 누락될 수 있으니, 실행 파일 이름까지 필요하다면 관리자 권한 CMD에서 실행해야 한다.

**`-n`은 결과를 빠르게 만들지만 가독성을 낮춘다**: 이름 확인을 생략하므로 응답이 빠르지만, IP 주소·포트 번호만 숫자로 나온다. 스크립트에서 파싱할 때는 `-n`이 형식이 일정해 유리하지만, 사람이 눈으로 훑을 때는 이름이 있는 편이 더 읽기 쉽다.

**`-r`은 `route print`의 동의어다**: 라우팅 테이블을 보는 방법이 두 가지 있는 셈이다 — `netstat -r`과 `route print`는 같은 결과를 낸다. 네트워크 문제를 진단할 때 굳이 route 명령을 따로 배우지 않고도 netstat 하나로 라우팅 정보까지 확인할 수 있다.

**PowerShell에서는 연결 조회 명령 자체가 나뉘어 있다**: PowerShell의 대응 명령은 `Get-NetTCPConnection`(TCP)과 `Get-NetUDPEndpoint`(UDP)로 프로토콜별로 나뉘어 있고, netstat의 `-o`처럼 `OwningProcess` 속성으로 PID를 바로 담고 있다. 다만 netstat -b처럼 프로세스 이름까지 한 번에 보여주지는 않으므로, `Get-NetTCPConnection | Select-Object -Property *,@{Name='ProcessName';Expression={(Get-Process -Id $_.OwningProcess).ProcessName}}`처럼 `Get-Process`와 PID를 교차 참조하는 파이프라인을 직접 구성해야 프로세스 이름까지 얻을 수 있다.

## 흔한 오개념

<strong>"netstat의 출력은 실행한 그 순간의 완벽한 실시간 스냅샷이다"</strong>는 오해가 흔하다. netstat이 연결 정보를 수집하기 시작하는 시점과 그 결과를 다 출력하는 시점 사이에는 약간의 시간차가 존재하며, 연결 수가 많을수록 이 간격은 더 벌어진다. 그 사이에 아주 짧게 맺혔다가 끊어지는 연결은 아예 결과에 잡히지 않거나, 같은 상황에서 짧은 간격으로 여러 번 실행해도 매번 조금씩 다른 결과가 나올 수 있다. netstat의 출력은 "그 순간의 정확한 사진"이 아니라 "수집에 걸린 시간 동안의 근사치"로 다뤄야 한다.

## 다음 장에서는

다음은 76장 — DNS 인프라를 진단하는 `nslookup` 명령을 다룬다.

## 평가 기준

- netstat으로 활성 연결·리스닝 포트를 조회하고 `-a`·`-n`·`-o` 옵션을 조합할 수 있다.
- `-o`로 확인한 PID를 taskkill·작업 관리자와 연계해 특정 프로세스를 찾는 흐름을 재현할 수 있다.
- `-b`가 느리고 권한이 필요한 이유를 설명할 수 있다.
- `netstat -r`이 `route print`와 같은 결과를 낸다는 것을 안다.

## 참고

- [netstat | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netstat)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
