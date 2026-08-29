---
draft: false
slug: sc-command-manage-windows-services-cmd
title: "[CMD] 56. sc - Windows 서비스 조회와 구성"
description: "sc로 Windows 서비스를 조회·생성·시작·중지·삭제하는 법과 sc create의 옵션마다 등호 뒤에 공백이 반드시 필요한 문법 함정, 시작 유형(auto·demand·disabled 등)의 의미를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 560
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
- sc
- 서비스관리
- Windows-Service
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Security(보안)
- Networking(네트워킹)
- Configuration(설정)
- Beginner
- Workflow(워크플로우)
- Productivity(생산성)
image: "wordcloud.png"
---

sc(Service Control)는 Windows 서비스를 조회·생성·구성·시작·중지·삭제하는 명령이다. 서비스 제어 관리자(Service Control Manager) 데이터베이스와 레지스트리에 직접 항목을 만든다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [55장: taskkill](/post/cmd/taskkill-command-terminate-process-windows-cmd/)에서 프로세스를 종료하는 법을 다룬 뒤 이어진다. tasklist·taskkill이 눈에 보이는 프로세스를 다뤘다면, sc는 백그라운드에서 조용히 돌아가는 서비스라는 더 근본적인 계층을 다룬다.

**이 장의 깊이**: 고급. **다루지 않는 것**: 서비스를 특정 시각에 자동 실행하는 것은 57장(schtasks)에서 다룬다. sc는 "항상 떠 있는 백그라운드 프로세스"를, schtasks는 "정해진 시점에 실행되는 작업"을 다룬다는 차이가 있다.

## 사용법

```
sc [\\<컴퓨터>] <하위명령> [<서비스이름>] [<옵션>...]
```

## 자주 쓰는 하위 명령

| 하위 명령 | 역할 |
|---|---|
| `query` | 서비스 상태·목록 조회 |
| `qc` | 서비스 구성 조회 |
| `create` | 새 서비스 생성(레지스트리·SCM에 항목 등록) |
| `start` | 서비스 시작 |
| `stop` | 서비스 중지 |
| `delete` | 서비스 삭제 |
| `config` | 기존 서비스 설정 변경(시작 유형, 경로 등) |

### sc create 주요 옵션

| 옵션 | 설명 |
|---|---|
| `type= own\|share\|kernel\|filesys\|rec\|interact` | 서비스 종류(기본 `own`) |
| `start= boot\|system\|auto\|demand\|disabled\|delayed-auto` | 시작 유형(기본 `demand`, 수동 시작) |
| `binpath= <경로>` | 서비스 실행 파일 경로(필수, 기본값 없음) |
| `depend= <의존서비스>` | 이 서비스보다 먼저 시작되어야 하는 서비스·그룹(`/`로 구분) |
| `obj= <계정이름>` | 서비스가 실행될 계정(기본 `LocalSystem`) |
| `displayname= <표시이름>` | 사용자 인터페이스에 보일 친숙한 이름 |

## 예시

```
sc query
sc query wuauserv
sc qc wuauserv
sc start wuauserv
sc stop wuauserv
sc config MyService start= auto
sc \\server01 query
sc create NewService binpath= c:\windows\system32\NewServ.exe type= share start= auto depend= +TDI NetBIOS
```

## 주의사항·함정

**등호 뒤에 반드시 공백이 있어야 한다**: sc의 문법 중 가장 자주 실수하는 지점이다.

> "Each command-line option (parameter) must include the equal sign as part of the option name. A space is required between an option and its value (for example, **type= own**. If the space is omitted, the operation fails." — Microsoft Learn, "sc.exe create"

즉 `start=auto`(공백 없음)는 실패하고, 반드시 `start= auto`(등호 바로 뒤에 공백)로 써야 한다. 다른 대부분의 CMD 옵션이 `/옵션:값`이나 `/옵션값` 형태인 것과 문법 관례 자체가 다르기 때문에, 익숙한 CMD 사용자일수록 오히려 이 공백을 빠뜨리기 쉽다.

**시작 유형은 6가지로 세분화되어 있다**: `auto`(부팅마다 자동 시작), `demand`(수동 시작, 기본값), `disabled`(시작 불가), `boot`/`system`(부트로더·커널 초기화 단계에서 시작되는 드라이버 전용), `delayed-auto`(다른 자동 시작 서비스들이 시작된 후 약간 지연되어 시작)로 나뉜다. 부팅 시간을 줄이려는 목적이라면 `auto` 대신 `delayed-auto`를 고려할 수 있다 — 부팅 초반의 혼잡을 피하면서도 결국 자동으로 시작된다.

**서비스를 잘못 중지·삭제하면 시스템이 불안정해질 수 있다**: 이름과 역할을 정확히 확인하지 않고 시스템 서비스를 `stop`이나 `delete`하면 다른 프로그램이나 OS 자체의 동작에 영향을 줄 수 있다. `sc qc <서비스이름>`으로 의존 관계와 구성을 먼저 확인하는 것이 안전하다.

**원격 서비스 제어에는 별도 권한이 필요하다**: `\\컴퓨터` 형식으로 원격 서버를 대상으로 지정할 수 있지만, 그 컴퓨터에 대한 관리 권한이 있어야 하며 방화벽·네트워크 설정에 따라 원격 관리 자체가 막혀 있을 수 있다.

**`sc delete`는 실행 중인 서비스를 먼저 멈추지 않는다**: `sc delete`는 서비스 제어 관리자와 레지스트리에서 서비스 등록 정보만 제거할 뿐, 그 서비스가 지금 실행 중이라면 프로세스 자체는 그대로 남아 계속 동작한다. 삭제 명령이 성공했다는 메시지를 보고 서비스가 즉시 멈췄을 거라 기대하면 안 된다 — 실행 중인 프로세스는 `sc stop`으로 따로 멈추거나 시스템이 재부팅될 때까지 계속 동작한다.

**PowerShell에서는 `Get-Service`·`Set-Service`·`New-Service`·`Stop-Service`/`Start-Service`가 대응 명령이다**: PowerShell의 서비스 관련 cmdlet들은 sc의 `옵션= 값`(등호 뒤 공백 필수)이라는 독특한 문법 없이 일반적인 매개변수 형태(`-Name`, `-StartupType` 등)로 서비스를 다룰 수 있어 전반적으로 다루기 쉽다. 다만 `New-Service`로 새 서비스를 등록할 때의 세부 옵션 이름·범위는 `sc create`와 완전히 같지 않으므로, 기존 sc 스크립트를 그대로 옮기기보다는 대상 cmdlet의 매개변수를 다시 확인해야 한다.

## 흔한 오개념

<strong>"`sc delete`를 실행하면 서비스가 즉시 완전히 사라진다"</strong>는 오해가 있다. 서비스가 실행 중인 상태에서 `sc delete`를 실행해도 등록 정보만 삭제될 뿐 이미 떠 있는 프로세스는 멈추지 않는다 — `sc query`로 확인하면 상태가 한동안 "삭제 대기 중"으로 남아 있거나, 프로세스 자체는 계속 동작하다가 다음 재부팅에서야 완전히 정리된다. 실행 중인 서비스를 즉시 없애려면 `sc stop`으로 먼저 멈춘 뒤 `sc delete`를 실행해야 한다.

## 다음 장에서는

다음은 57장 — 특정 시각·조건에 프로그램을 자동으로 실행하도록 예약하는 `schtasks` 명령을 다룬다.

## 평가 기준

- sc로 서비스를 조회·시작·중지·구성·삭제할 수 있다.
- sc create의 옵션이 등호 뒤에 공백을 요구하는 독특한 문법 규칙을 지킬 수 있다.
- 6가지 시작 유형(auto, demand, disabled, boot, system, delayed-auto)의 차이를 설명할 수 있다.
- sc(상시 백그라운드 서비스)와 57장에서 다룰 schtasks(정해진 시점 실행)의 역할 차이를 안다.

## 참고

- [sc.exe create | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sc-create)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
