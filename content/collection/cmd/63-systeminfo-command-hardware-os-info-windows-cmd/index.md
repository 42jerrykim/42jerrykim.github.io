---
draft: false
slug: systeminfo-command-hardware-os-info-windows-cmd
title: "[CMD] 63. systeminfo - 하드웨어·OS 구성 정보 표시"
description: "systeminfo로 컴퓨터의 OS 구성·보안 정보·제품 ID·하드웨어 속성을 한 번에 조회하는 법과 원격 컴퓨터 지정 옵션, 출력이 길어질 때 리다이렉션·파이프로 다루는 관행을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 630
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
- systeminfo
- 시스템정보
- Monitoring(모니터링)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Networking(네트워킹)
- Configuration(설정)
- Productivity(생산성)
- DevOps
- Administration
- Advanced
image: "wordcloud.png"
---

systeminfo는 컴퓨터와 운영체제에 대한 상세 구성 정보 — OS 구성, 보안 정보, 제품 ID, RAM·디스크 공간·네트워크 카드 같은 하드웨어 속성 — 을 표시하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [62장: openfiles](/post/cmd/openfiles-command-remote-open-files-windows-cmd/)로 Part 6(프로세스·서비스와 권한 관리)를 마친 뒤 이어지며, <strong>Part 7(시스템 정보와 구성)</strong>의 첫 장이다. 지금까지 조작·관리해온 대상을 이 장부터는 "지금 이 시스템이 전반적으로 어떤 상태인가"를 진단하는 시야로 종합한다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: Windows 버전만 간단히 확인하는 것은 64장(ver)에서, 드라이버 목록은 65장(driverquery)에서 각각 더 좁은 범위로 다룬다.

## 사용법

```
systeminfo [/s <컴퓨터> [/u <도메인>\<사용자> [/p <비밀번호>]]] [/fo {TABLE | LIST | CSV}] [/nh]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/s <컴퓨터>` | 원격 컴퓨터 이름·IP(기본은 로컬) |
| `/u <도메인>\<사용자>` | 원격 조회 시 사용할 계정 |
| `/p <비밀번호>` | `/u` 계정의 비밀번호 |
| `/fo TABLE\|LIST\|CSV` | 출력 형식 |
| `/nh` | 열 머리글 생략(TABLE·CSV일 때 유효) |

## 예시

```
systeminfo
systeminfo /fo csv
systeminfo /s srvmain
systeminfo /s srvmain2 /u maindom\hiropln
systeminfo /s srvmain2 /u maindom\hiropln /p p@ssW23 /fo list
```

## 주의사항·함정

**출력이 매우 길다**: systeminfo는 OS 이름·버전·제조사·설치 날짜·부팅 시간·핫픽스 목록·네트워크 어댑터까지 한 화면에 담기 어려울 만큼 많은 정보를 쏟아낸다. 29장(more)에서 배운 페이저나 파일 리다이렉션과 조합하는 것이 사실상 필수다(`systeminfo | more`, `systeminfo > info.txt`).

**원격 조회에는 권한과 네트워크 설정이 함께 필요하다**: `/s`로 원격 컴퓨터를 지정할 때는 해당 컴퓨터에 대한 접근 권한뿐 아니라, 방화벽이 원격 관리 트래픽을 허용하고 있어야 한다. 권한은 있는데 방화벽이 막혀 있으면 조용히 시간 초과로 실패할 수 있다.

**필요한 항목만 빠르게 뽑으려면 findstr과 조합한다**: 00장(과정 개요)과 command-categories 부록에서 이미 예시로 든 것처럼, `systeminfo | findstr /i "OS Name"`처럼 27장(findstr)과 조합하면 전체 출력을 다 훑지 않고도 원하는 필드만 빠르게 확인할 수 있다.

**원격 컴퓨터 이름에 백슬래시를 쓰면 안 된다**: `/s` 옵션에 대해 Microsoft Learn은 다음과 같이 명시한다.

> "Specifies the name or IP address of a remote computer (do not use backslashes)." — Microsoft Learn, "systeminfo"

즉 `\\srvmain`처럼 UNC 경로 형식의 선행 백슬래시를 붙이면 안 되고, `systeminfo /s srvmain`처럼 컴퓨터 이름이나 IP만 그대로 적어야 한다. 다른 명령에서 익숙한 `\\서버명` 표기를 습관적으로 붙이면 조회에 실패한다.

**PowerShell 등가는 `Get-ComputerInfo`다**: systeminfo의 평면 텍스트 출력과 달리 `Get-ComputerInfo`는 훨씬 풍부한 필드를 가진 구조화된 객체를 반환해 `Select-Object`나 `Where-Object`로 바로 다룰 수 있다. 실행 속도 차이는 환경에 따라 달라질 수 있어 이 글에서는 단정하지 않는다.

## 흔한 오개념

<strong>"systeminfo `/fo csv` 출력은 PowerShell에서 `Get-ComputerInfo`와 동등하게 다룰 수 있다"</strong>는 오해가 있다. `/fo csv`는 필드를 쉼표로 구분한 평면 텍스트일 뿐 타입 정보나 중첩 구조가 없어서, `Import-Csv`로 읽어도 모든 값이 문자열로 취급된다. 반면 `Get-ComputerInfo`는 애초에 구조화된 객체를 반환하므로 숫자·날짜 필드를 바로 연산에 쓸 수 있다는 차이가 있다.

## 다음 장에서는

다음은 64장 — 단 한 줄로 Windows 버전만 간단히 확인하는 `ver` 명령을 다룬다.

## 평가 기준

- systeminfo로 로컬·원격 컴퓨터의 하드웨어·OS 구성 정보를 조회할 수 있다.
- 출력이 길 때 페이저·리다이렉션·findstr과 조합하는 실전 패턴을 적용할 수 있다.
- 원격 조회에 권한뿐 아니라 방화벽 설정도 필요하다는 것을 안다.

## 참고

- [systeminfo | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/systeminfo)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
