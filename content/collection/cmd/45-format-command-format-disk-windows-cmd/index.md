---
draft: false
slug: format-command-format-disk-windows-cmd
title: "[CMD] 45. format - 드라이브 포맷"
description: "format으로 드라이브를 지정 파일 시스템으로 포맷하는 법과 /q 빠른 포맷이 표면 검사를 생략한다는 차이, subst로 만든 가상 드라이브는 포맷할 수 없는 제약, 5단계 종료 코드를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 450
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
- format
- 포맷
- NTFS
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Security(보안)
- Education(교육)
- CLI
- ERRORLEVEL
- Data-Loss
- Configuration(설정)
- Beginner
- Administration
image: "wordcloud.png"
---

format은 드라이브를 Windows 파일을 담을 수 있는 상태로 포맷하는 명령이다. 하드 디스크를 포맷하려면 Administrators 그룹 구성원이어야 한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [44장: diskpart](/post/cmd/diskpart-command-manage-partitions-windows-cmd/)에서 파티션을 만드는 법을 다룬 뒤 이어진다. diskpart의 `create partition`으로 파티션 구조를 만든 다음 단계가 이 장의 format이다 — diskpart 안에서도 `format` 하위 명령으로 같은 작업을 할 수 있지만, 이 장은 cmd.exe 프롬프트에서 직접 실행하는 독립된 format 명령을 다룬다.

**이 장의 깊이**: 중급–고급. 데이터 손실과 직결되는 명령이므로 주의사항 비중이 크다.

## 사용법

```
format <볼륨> [/FS:<파일시스템>] [/V:<레이블>] [/Q] [/A:<크기>] [/C] [/X] [/P:<횟수>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/FS:<파일시스템>` | FAT, FAT32, NTFS, exFAT, ReFS, UDF 중 지정 |
| `/V:<레이블>` | 볼륨 레이블 지정. `/V:`만 쓰면 레이블 입력 프롬프트 생략 |
| `/Q` | 빠른 포맷. 파일 테이블·루트 디렉터리만 지우고 표면 전체 검사는 생략 |
| `/A:<크기>` | 할당 단위 크기 지정(파일 시스템별 허용 값이 다름) |
| `/C` | NTFS 전용. 새 볼륨의 파일을 기본적으로 압축 상태로 생성 |
| `/X` | 필요 시 볼륨을 먼저 마운트 해제 |
| `/P:<횟수>` | 모든 섹터를 0으로 쓴 뒤 지정 횟수만큼 임의의 값으로 덮어씀(`/Q`와 함께면 무시) |

### 종료 코드

| 종료 코드 | 의미 |
|---|---|
| 0 | 포맷 성공 |
| 1 | 잘못된 매개변수 |
| 4 | 치명적 오류(0·1·5 외 모든 오류) |
| 5 | 사용자가 확인 프롬프트에서 N을 눌러 중단 |

## 예시

```
format a:
format a: /q
format a: /v:DATA
format D: /fs:ntfs /v:Data /q
format E: /fs:fat32
```

## 주의사항·함정

**하드 디스크 포맷은 항상 데이터 손실 경고를 먼저 띄운다**: 이동식이 아닌 디스크를 포맷하려 하면 다음 경고가 표시된다.

> "WARNING, ALL DATA ON NON-REMOVABLE DISK DRIVE x: WILL BE LOST! Proceed with Format (Y/N)?" — Microsoft Learn, "format"

Y를 눌러야 실제 포맷이 진행되며, 이 확인 절차는 실수로 잘못된 드라이브 문자를 지정했을 때의 마지막 안전장치다.

**`/Q`는 표면 검사를 생략한다**: 빠른 포맷은 파일 테이블과 루트 디렉터리만 새로 만들 뿐, 디스크 표면에 배드 섹터가 있는지 검사하지 않는다. Microsoft Learn은 이미 정상으로 알고 있는, 이전에 포맷된 볼륨에만 `/Q`를 쓰라고 권장한다 — 새 디스크이거나 상태가 불확실한 디스크라면 전체 포맷(옵션 없이)으로 표면까지 검사하는 편이 안전하다.

**subst로 만든 가상 드라이브는 포맷할 수 없다**: 51장(subst)에서 다룰 가상 드라이브 문자에는 format을 쓸 수 없고, 네트워크 너머의 디스크도 포맷할 수 없다. format이 통하지 않는다면 그 드라이브가 실제 물리 볼륨이 맞는지부터 확인해야 한다.

**파일 시스템마다 클러스터 수 제한이 있다**: FAT는 클러스터를 65526개까지, FAT32는 65527–4177917개 범위로 제한한다. 지정한 할당 단위 크기(`/A`)로 이 제한을 만족할 수 없으면 format은 처리를 시작하지도 않고 즉시 중단한다.

**NTFS 압축은 할당 단위 4096바이트 이하에서만 지원된다**: `/C`로 압축을 켜려 하면서 그보다 큰 할당 단위를 지정하면 요구 사항이 충돌해 포맷이 진행되지 않는다.

**PowerShell 등가는 `Format-Volume`이다**: `Format-Volume -DriveLetter D -FileSystem NTFS`처럼 매개변수로 파일 시스템·볼륨 레이블을 지정한다. format.exe와 달리 `Format-Volume`은 기본 동작이 빠른 포맷이므로, format의 옵션 없는 실행(표면 전체 검사 포함)과 동일하게 만들려면 `-Full` 스위치를 명시적으로 추가해야 한다는 점이 차이다.

## 흔한 오개념

<strong>"빠른 포맷은 데이터를 완전히 지우므로 복구가 불가능하다"</strong>는 오해가 있다. 실제로는 정반대에 가깝다 — 빠른 포맷은 파일 테이블만 새로 만들 뿐 기존 데이터가 있던 섹터를 실제로 덮어쓰지는 않으므로, 전문 복구 도구로 상당 부분 복구될 수 있다. 데이터를 확실히 없애야 한다면 `/P:<횟수>`로 여러 번 덮어쓰는 옵션을 쓰거나 `/Q` 없이 전체 포맷을 진행해야 한다.

## 다음 장에서는

다음은 46장 — FAT·FAT32 볼륨을 데이터 손실 없이 NTFS로 변환하는 `convert` 명령을 다룬다.

## 평가 기준

- format으로 볼륨을 지정 파일 시스템으로 포맷하고, `/FS`·`/V`·`/Q` 옵션을 조합할 수 있다.
- `/Q`(빠른 포맷)가 표면 검사를 생략한다는 것과, 언제 안전하게 쓸 수 있는지 설명할 수 있다.
- format의 5가지 종료 코드로 배치 스크립트에서 실패 원인을 구분할 수 있다.
- 빠른 포맷이 데이터를 완전히 지우지 않는다는 것과, 완전 삭제에는 `/P`가 필요하다는 것을 설명할 수 있다.

## 참고

- [format | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/format)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
