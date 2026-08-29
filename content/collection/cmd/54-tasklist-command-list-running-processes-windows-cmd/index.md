---
draft: false
slug: tasklist-command-list-running-processes-windows-cmd
title: "[CMD] 54. tasklist - 실행 중인 프로세스 목록 조회"
description: "tasklist로 로컬·원격 컴퓨터의 실행 중인 프로세스를 조회하는 법과 /fi 필터 이름·연산자·값 조합, WINDOWTITLE·STATUS 필터가 원격 조회에서는 지원되지 않는 제약을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 540
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
- tasklist
- 프로세스목록
- Process
- Monitoring(모니터링)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Linux(리눅스)
- Education(교육)
- CLI
- Networking(네트워킹)
- Configuration(설정)
- Workflow(워크플로우)
- Productivity(생산성)
image: "wordcloud.png"
---

tasklist는 로컬 또는 원격 컴퓨터에서 현재 실행 중인 프로세스 목록을 표시하는 명령이다. Part 6(프로세스·서비스와 권한 관리)의 첫 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [53장: verify](/post/cmd/verify-command-verify-file-writes-windows-cmd/)로 Part 5(디스크와 파일 시스템 관리)를 마친 뒤 이어지며, <strong>Part 6(프로세스·서비스와 권한 관리)</strong>의 첫 장이다. 지금까지의 디스크 관리 명령들이 5장(디스크 공간 부족 등)의 원인을 진단했다면, 이 장부터는 그 원인이 될 수 있는 "지금 실행 중인 프로그램"을 다룬다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 조회한 프로세스를 종료하는 것은 55장(taskkill)에서 다룬다.

## 사용법

```
tasklist [/s <컴퓨터> [/u [<도메인>\]<사용자> [/p <비밀번호>]]] [{/m <모듈> | /svc | /v}] [/fo {table | list | csv}] [/nh] [/fi <필터> [/fi <필터> [...]]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/s <컴퓨터>` | 원격 컴퓨터 이름·IP 지정(기본은 로컬) |
| `/u`, `/p` | 원격 조회 시 사용할 계정·비밀번호(`/s`와 함께만 사용 가능) |
| `/m [모듈]` | 지정한 DLL을 로드한 작업만, 또는 모듈 목록 |
| `/svc` | 각 프로세스의 서비스 정보(`/fo table`일 때만 유효) |
| `/v` | 상세 정보(창 제목, 상태 등). `/svc`와 함께 쓰면 잘림 없이 전체 표시 |
| `/fo table\|list\|csv` | 출력 형식(기본 table) |
| `/nh` | 열 머리글 생략(`/fo`가 table·csv일 때 유효) |
| `/fi <필터>` | 조건에 맞는 프로세스만 표시. 여러 번 지정 가능 |

### 필터 이름·연산자·값

| 필터 이름 | 연산자 | 값 |
|---|---|---|
| STATUS | eq, ne | RUNNING \| NOT RESPONDING \| UNKNOWN(원격 조회 미지원) |
| IMAGENAME | eq, ne | 이미지 이름 |
| PID | eq, ne, gt, lt, ge, le | PID 값 |
| SESSION | eq, ne, gt, lt, ge, le | 세션 번호 |
| CPUtime | eq, ne, gt, lt, ge, le | HH:MM:SS 형식 |
| MEMUSAGE | eq, ne, gt, lt, ge, le | KB 단위 메모리 |
| USERNAME | eq, ne | 사용자 이름 |
| SERVICES | eq, ne | 서비스 이름 |
| WINDOWTITLE | eq, ne | 창 제목(원격 조회 미지원) |
| MODULES | eq, ne | DLL 이름 |

## 예시

```
tasklist
tasklist /fi "imagename eq notepad.exe"
tasklist /v /fi "PID gt 1000" /fo csv
tasklist /fi "USERNAME ne NT AUTHORITY\SYSTEM" /fi "STATUS eq running"
tasklist /s srvmain /svc /fi "MODULES eq ntdll*"
tasklist /s srvmain /u maindom\hiropln /p p@ssW23
```

## 주의사항·함정

**WINDOWTITLE·STATUS 필터는 원격 조회에서 쓸 수 없다**: `/s`로 원격 컴퓨터를 조회할 때는 필터 표에 명시된 대로 이 두 필터가 지원되지 않는다.

> "This filter isn't supported if you specify a remote system." — Microsoft Learn, "tasklist"

원격 서버에서 특정 창 제목이나 응답 없음 상태로 필터링하려던 스크립트가 로컬에서는 되던 것이 원격에서 조용히 무시되는 원인이 여기 있다.

**필터를 여러 번 지정하면 AND 조건이 된다**: `/fi`를 두 번 이상 쓰면 모든 조건을 동시에 만족하는 프로세스만 남는다. 위 예시의 `USERNAME ne ... /fi STATUS eq running`은 "SYSTEM 계정이 아니면서 동시에 실행 중"인 프로세스만 걸러낸다.

**`/svc`는 `/fo table`에서만 유효하다**: 서비스 정보를 함께 보려면 출력 형식을 명시적으로 확인해야 한다 — 다른 형식과 조합하면 옵션이 무시될 수 있다.

**tasklist는 tlist를 대체한다**: 오래된 Windows 리소스 킷의 tlist 도구를 대체하는 명령으로 문서화되어 있다 — 옛 스크립트에서 tlist를 참조하고 있다면 tasklist로 옮겨야 한다.

**PowerShell에서는 `Get-Process`가 대응 명령이다**: `Get-Process`는 tasklist보다 훨씬 풍부한 객체(핸들 수, 스레드, 시작 경로 등)를 돌려주고 파이프라인으로 바로 필터링·정렬할 수 있다. 다만 세션·사용자 이름 정보는 `Get-Process`가 기본으로 보여주지 않는다 — tasklist가 `/svc`나 `USERNAME` 필터로 쉽게 보여주는 정보를 PowerShell에서 얻으려면 `Get-CimInstance Win32_Process`처럼 별도 조회를 추가해야 한다.

## 흔한 오개념

<strong>"tasklist를 그냥 실행하면 이 컴퓨터에 로그온한 모든 사용자의 모든 프로세스가 빠짐없이 보인다"</strong>는 오해가 있다. 관리자 권한 없이 실행하면 다른 사용자 세션에서 실행 중인 프로세스의 소유자·전체 경로 같은 일부 정보는 제한되거나 표시되지 않을 수 있다 — 여러 사용자가 동시에 로그온하는 원격 데스크톱 서버 환경에서 "분명 실행 중인데 정보가 비어 있다"는 혼란이 여기서 나온다. 모든 세션의 프로세스 정보를 온전히 확인하려면 관리자 권한으로 실행해야 한다.

## 다음 장에서는

다음은 55장 — tasklist로 찾은 PID나 이미지 이름으로 프로세스를 종료하는 `taskkill` 명령을 다룬다.

## 평가 기준

- tasklist로 로컬·원격 프로세스 목록을 조회하고 `/fi` 필터를 조합할 수 있다.
- WINDOWTITLE·STATUS 필터가 원격 조회에서 지원되지 않는다는 것을 안다.
- `/fi`를 여러 번 쓰면 AND 조건이 된다는 것을 설명할 수 있다.
- tasklist가 대체한 레거시 도구(tlist)를 안다.

## 참고

- [tasklist | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/tasklist)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
