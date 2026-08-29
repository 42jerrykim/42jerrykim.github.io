---
draft: false
slug: driverquery-command-device-driver-status-windows-cmd
title: "[CMD] 65. driverquery - 설치된 장치 드라이버 상태 조회"
description: "driverquery로 설치된 장치 드라이버 목록과 서명 정보를 조회하는 법과 /v와 /si가 서명된 드라이버에서는 함께 쓰일 수 없는 제약, /nh가 list 형식에서는 무효한 옵션 조합을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 650
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
- driverquery
- 드라이버조회
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Security(보안)
- Hardware
- Configuration(설정)
- Productivity(생산성)
- DevOps
- Administration
- Advanced
image: "wordcloud.png"
---

driverquery는 관리자가 설치된 장치 드라이버 목록과 그 속성을 표시할 수 있게 하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [64장: ver](/post/cmd/ver-command-windows-version-cmd/)에서 OS 버전을 확인하는 법을 다룬 뒤 이어진다. OS 버전이 소프트웨어 계층의 정보였다면, driverquery는 하드웨어와 OS를 잇는 드라이버 계층의 정보를 다룬다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
driverquery [/s <시스템> [/u [<도메인>\]<사용자> [/p <비밀번호>]]] [/fo {table | list | csv}] [/nh] [/v | /si]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/fo table` | 표 형식(기본값) |
| `/fo list` | 목록 형식 |
| `/fo csv` | 쉼표로 구분된 값 형식 |
| `/nh` | 머리글 행 생략(`list` 형식에는 적용 안 됨) |
| `/v` | 상세 출력(서명된 드라이버에는 유효하지 않음) |
| `/si` | 서명된 드라이버 정보 제공 |
| `/s <시스템>` | 원격 컴퓨터 지정 |

## 예시

```
driverquery
driverquery /fo csv
driverquery /nh
driverquery /s server1
driverquery /s server1 /u maindom\user1 /p p@ssw3d
```

## 주의사항·함정

**`/v`와 `/si`는 서로 다른 목적이라 함께 쓰기 어렵다**: Microsoft Learn은 `/v`가 서명된 드라이버에는 유효하지 않다고 명시한다.

> "/v — Displays verbose output. **/v** is not valid for signed drivers." — Microsoft Learn, "driverquery"

즉 서명 정보(`/si`)를 자세히 보고 싶다고 해서 `/v`를 함께 붙이면 원하는 결과를 얻지 못할 수 있다 — 두 옵션은 각각 독립적인 조회 모드에 가깝다.

**`/nh`는 `list` 형식에서 무효하다**: 표 형식(`table`)이나 CSV에서는 머리글을 생략할 수 있지만, 목록(`list`) 형식은 애초에 각 항목이 "필드: 값" 구조로 출력되므로 생략할 "머리글 행"이라는 개념 자체가 없다.

**원격 조회는 `/s`가 먼저 있어야 `/u`를 쓸 수 있다**: 54장(tasklist)·63장(systeminfo)에서 이미 본 패턴과 동일하다 — `/u`, `/p`는 항상 `/s`와 함께여야 의미가 있다.

**PowerShell 등가는 `Get-CimInstance -ClassName Win32_PnPSignedDriver`다**: CIM/WMI 기반 조회라서 driverquery의 텍스트·CSV 출력보다 필드가 훨씬 풍부한 구조화된 객체를 돌려준다. 오프라인 이미지(마운트된 WIM/VHD)의 드라이버까지 다루려면 DISM 기반의 `Get-WindowsDriver`를 대신 써야 한다 — driverquery는 실행 중인 시스템만 대상으로 한다는 점이 다르다.

## 흔한 오개념

<strong>"`/si`를 붙여야 서명되지 않은 드라이버까지 볼 수 있다"</strong>는 오해가 있다. driverquery는 옵션 없이 실행해도 서명 여부와 무관하게 설치된 드라이버를 모두 나열한다. `/si`는 조회 대상을 넓히는 옵션이 아니라, 이미 나열된 드라이버들에 서명자·서명 여부 같은 추가 정보를 붙여 보여주는 옵션일 뿐이다.

## 다음 장에서는

다음은 66장 — 사용자·컴퓨터에 적용된 그룹 정책 결과를 표시하는 `gpresult` 명령을 다룬다.

## 평가 기준

- driverquery로 설치된 드라이버 목록을 조회하고 출력 형식을 선택할 수 있다.
- `/v`와 `/si`가 서로 다른 목적의 옵션이라는 것을 설명할 수 있다.
- `/nh`가 `list` 형식에서는 의미가 없는 이유를 안다.

## 참고

- [driverquery | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/driverquery)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
