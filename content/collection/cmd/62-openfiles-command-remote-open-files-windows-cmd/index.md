---
draft: false
slug: openfiles-command-remote-open-files-windows-cmd
title: "[CMD] 62. openfiles - 원격으로 열린 파일 조회와 연결 해제"
description: "openfiles로 파일 공유를 통해 원격 사용자가 열어 둔 파일을 조회·연결 해제하는 법과 로컬 파일 추적(Maintain Objects List)을 켜려면 재부팅이 필요한 이유, 성능 영향을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 620
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
- openfiles
- 파일공유
- Networking(네트워킹)
- Security(보안)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Configuration(설정)
- Beginner
- Workflow(워크플로우)
- Productivity(생산성)
- DevOps
image: "wordcloud.png"
---

openfiles는 관리자가 파일 공유를 통해 열린 파일·디렉터리를 조회·연결 해제하는 명령이다. Part 6(프로세스·서비스와 권한 관리)의 마지막 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [61장: cacls](/post/cmd/cacls-command-legacy-acl-windows-cmd/)에서 레거시 ACL 명령을 다룬 뒤 이어지며, Part 6의 마지막 장이다. 60–61장이 "누가 접근할 수 있는가"를 설정하는 명령이었다면, openfiles는 "지금 실제로 누가 무엇을 열어 놓고 있는가"를 확인하는 진단 명령이다.

**이 장의 깊이**: 중급.

## 사용법

```
openfiles /query [/s <시스템> [/u [<도메인>\]<사용자> [/p [<비밀번호>]]]] [/fo {TABLE | LIST | CSV}] [/nh] [/v]
openfiles /disconnect [/s <시스템> [/u [<도메인>\]<사용자> [/p [<비밀번호>]]]] {[/id <파일ID>] | [/a <사용자>] | [/o {read | write | read/write}]} [/op <파일이름>]
openfiles /local [on | off]
```

## 옵션

### 조회(`/query`)

| 옵션 | 설명 |
|---|---|
| `/fo TABLE\|LIST\|CSV` | 출력 형식 |
| `/nh` | 열 머리글 생략 |
| `/v` | 상세 정보 표시 |

### 연결 해제(`/disconnect`)

| 옵션 | 설명 |
|---|---|
| `/id <파일ID>` | 지정한 파일 ID로 연결 해제(와일드카드 지원) |
| `/a <사용자>` | 지정한 사용자의 모든 열린 파일 연결 해제 |
| `/o read\|write\|read/write` | 지정한 열기 모드의 연결만 해제 |
| `/op <파일이름>` | 지정한 파일 이름으로 열린 모든 연결 해제 |

### 로컬 추적(`/local`)

| 값 | 설명 |
|---|---|
| `on` | 로컬 파일 핸들 추적(Maintain Objects List) 활성화 |
| `off` | 비활성화(기본값) |

## 예시

```
openfiles /query
openfiles /query /fo table /nh
openfiles /query /fo list /v
openfiles /disconnect /id 26843578
openfiles /disconnect /a hiropln
openfiles /disconnect /o read/write
openfiles /local
openfiles /local on
```

## 주의사항·함정

**기본적으로는 원격 공유를 통해 열린 파일만 보인다**: `/query`를 옵션 없이 실행해도 곧바로 로컬에서 애플리케이션이 열어 둔 파일까지 보이지는 않는다. 이는 openfiles가 원래 파일 서버 관리 용도로 설계되어, 네트워크 공유를 거쳐 원격 사용자가 연 파일을 추적하는 데 최적화되어 있기 때문이다.

**로컬 파일까지 보려면 설정을 켜고 재부팅해야 한다**: `/local on`으로 Maintain Objects List 플래그를 활성화해야 로컬에서 열린 파일까지 추적 대상이 되는데, 이 변경은 즉시 적용되지 않는다.

> "Changes made by using the **on** or **off** option don't take effect until you restart the system. Enabling the **Maintain Objects List** global flag might slow down your system." — Microsoft Learn, "openfiles"

즉 `/local on`을 실행한 직후 `/query`를 돌려도 로컬 파일은 여전히 보이지 않는다 — 재부팅 후에야 반영된다. 또한 이 플래그는 시스템 전체의 파일 핸들을 추가로 추적하는 기능이라 활성화 상태를 유지하면 성능에 영향을 줄 수 있다는 경고도 함께 명시되어 있다.

**연결 해제는 파일을 저장하지 않은 채로 세션을 끊는다**: `/disconnect`로 원격 사용자의 파일 연결을 강제로 끊으면, 그 사용자가 저장하지 않은 변경 사항을 잃을 수 있다. 55장(taskkill)의 `/f`와 비슷한 성격의 위험이다 — 정말 그 연결을 끊어야 하는지 확인한 뒤 실행해야 한다.

**관리자 권한이 필요하다**: 원격 사용자의 파일 접근 정보를 조회·차단하는 작업이므로 관리자 권한 없이는 실행할 수 없다.

**PowerShell/SMB 모듈 등가는 `Get-SmbOpenFile`이다**: SMB 공유를 통해 열린 파일 핸들을 조회하려면 PowerShell의 SmbShare 모듈에 있는 `Get-SmbOpenFile`을, 연결을 강제로 끊으려면 `Close-SmbOpenFile`을 쓴다. 다만 openfiles의 `/local` 기능 — 재부팅 후 로컬 파일 핸들까지 추적하는 기능 — 에 대응하는 간단한 PowerShell 명령은 없다. SMB 모듈은 어디까지나 네트워크 공유를 거친 핸들을 다루는 도구이기 때문이다.

## 흔한 오개념

<strong>"`openfiles /local on`을 실행하면 바로 로컬 파일 추적이 시작된다"</strong>는 오해가 있다. 이 옵션은 Maintain Objects List라는 전역 플래그를 켜는 스위치일 뿐이고, 위 주의사항에서 본 것처럼 변경 사항은 시스템을 재시작해야 적용된다. `/local on` 직후 `/query`를 실행해도 결과는 그대로다 — 로컬 애플리케이션이 열어 둔 파일은 재부팅 후에야 목록에 나타나기 시작한다.

## 다음 장에서는

다음은 63장 — 컴퓨터의 하드웨어·OS 구성 정보를 표시하는 `systeminfo` 명령으로 Part 7(시스템 정보와 구성)이 시작된다.

## 평가 기준

- openfiles로 원격 사용자가 열어 둔 파일을 조회하고 특정 연결을 해제할 수 있다.
- 기본적으로는 로컬 파일이 아니라 공유를 통한 원격 접근만 보인다는 것을 안다.
- `/local on`이 재부팅 후에야 적용되고 성능에 영향을 줄 수 있다는 것을 설명할 수 있다.
- `/disconnect`가 저장되지 않은 데이터 손실로 이어질 수 있는 위험을 설명할 수 있다.

## 참고

- [openfiles | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/openfiles)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
