---
draft: false
slug: wmic-command-wmi-query-legacy-windows-cmd
title: "[CMD] 68. wmic - WMI 명령줄 조회(레거시)"
description: "wmic으로 WMI 정보를 명령줄에서 조회하는 법과 Windows 10 21H1부터 공식 지원 중단된 이유, WMI 자체는 계속 유효하지만 명령줄 도구만 대체된다는 구분, PowerShell CIM cmdlet으로 옮기는 방향을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 680
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
- wmic
- WMI
- Legacy
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- PowerShell
- Troubleshooting(트러블슈팅)
- Configuration(설정)
- Productivity(생산성)
- DevOps
- Administration
- Beginner
image: "wordcloud.png"
---

wmic은 대화형 명령 셸 안에서 WMI(Windows Management Instrumentation) 정보를 표시하는 도구다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [67장: mode](/post/cmd/mode-command-configure-system-devices-windows-cmd/)에서 장치 구성을 다룬 뒤 이어진다. mode가 레거시이지만 여전히 쓰이는 명령이었다면, wmic은 명시적으로 지원 중단이 선언된 명령이라는 점에서 한 단계 더 나아간 사례다.

**이 장의 깊이**: 중급. **참고 사항**: 새로 작성하는 스크립트에는 이 명령을 쓰지 않는 것이 좋다 — 아래 "주의사항·함정"에서 이유를 설명한다.

## 사용법

```
wmic </파라미터>
```

## 하위 명령

| 하위 명령 | 역할 |
|---|---|
| `logicaldisk` | 이 컴퓨터의 모든 논리 디스크 속성 표시 |
| `class` | WMIC의 기본 별칭(alias) 모드를 벗어나 WMI 스키마의 클래스에 직접 접근 |
| `path` | WMI 스키마의 인스턴스에 직접 접근 |
| `context` | 현재 전역 스위치 값 표시 |
| `quit` \| `exit` | WMIC 명령 셸 종료 |

이 외에도 `os`(운영 체제), `cpu`(프로세서), `process`(프로세스), `service`(서비스) 등 자주 쓰는 별칭이 있다.

## 예시

```
wmic context
wmic logicaldisk
wmic logicaldisk get name
wmic os get caption,version
wmic process get name,processid
wmic service where "name='wuauserv'" get state
wmic /node:server01 os get caption
wmic /locale:ms_409
```

## 주의사항·함정

**공식적으로 지원 중단되었다**: Microsoft Learn 문서 최상단에 명시적인 경고가 있다.

> "The WMI command-line (WMIC) utility is deprecated as of Windows 10, version 21H1, and as of the 21H1 semi-annual channel release of Windows Server. This utility is superseded by Windows PowerShell for WMI." — Microsoft Learn, "wmic"

**WMI 자체는 영향을 받지 않는다는 점이 중요하다**: 지원 중단은 명령줄 도구(WMIC)에만 해당하고, 그 밑에 있는 WMI 기술 자체는 계속 유효하다.

> "This deprecation applies only to the WMI command-line (WMIC) utility; Windows Management Instrumentation (WMI) itself is not affected." — Microsoft Learn, "wmic"

즉 wmic으로 조회하던 정보 자체는 여전히 시스템에 존재하지만, 그것을 명령줄에서 조회하는 이 특정 인터페이스만 단계적으로 사라진다는 뜻이다. 00장(과정 개요)에서 짧게 언급했던 것처럼, 최신 릴리스에서는 WMIC 기능이 기본 설치에서 빠지는 선택적 기능으로 전환될 예정이다.

**대안은 PowerShell의 WMI/CIM cmdlet이다**: `Get-WmiObject`나 그보다 최신인 `Get-CimInstance`가 wmic의 별칭(alias) 기반 조회를 대체한다. `wmic os get caption,version` 같은 명령은 `Get-CimInstance Win32_OperatingSystem | Select Caption,Version` 형태로 옮겨 쓸 수 있다.

**기존 배치 스크립트를 유지 보수하는 상황이라면 당장 걷어낼 필요는 없다**: 지원 중단은 "당장 동작하지 않는다"는 뜻이 아니라 "미래 버전에서 제거될 수 있다"는 경고다. 이미 있는 오래된 스크립트를 급하게 고칠 필요는 없지만, 새로 자동화를 설계한다면 처음부터 PowerShell CIM cmdlet을 선택하는 편이 안전하다.

## 흔한 오개념

<strong>"wmic이 지원 중단되었으니 WMI 자체도 곧 사라진다"</strong>는 오해가 있다. 실제로 지원 중단은 명령줄 프런트엔드인 wmic.exe에만 해당하고, 그 밑에서 동작하는 WMI/CIM 인프라는 계속 핵심 기술로 남아 있다 — PowerShell의 `Get-CimInstance` 자체가 바로 이 WMI/CIM 인프라를 조회하는 cmdlet이다.

## 다음 장에서는

다음은 69장 — 시스템 날짜·시간을 표시·설정하는 `date`, `time` 명령을 다룬다.

## 평가 기준

- wmic으로 OS·프로세스·디스크·서비스 정보를 조회할 수 있다.
- wmic이 Windows 10 21H1부터 공식 지원 중단되었다는 것을 안다.
- 지원 중단이 WMIC 명령줄 도구에만 해당하고 WMI 기술 자체에는 영향이 없다는 구분을 설명할 수 있다.
- 새 자동화에는 PowerShell CIM cmdlet(`Get-CimInstance`)을 우선 고려해야 하는 이유를 안다.

## 참고

- [wmic | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wmic)
- [Deprecated features in the Windows client | Microsoft Learn](https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features)
