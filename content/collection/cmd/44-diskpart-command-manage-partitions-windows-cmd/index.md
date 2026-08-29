---
draft: false
slug: diskpart-command-manage-partitions-windows-cmd
title: "[CMD] 44. diskpart - 디스크와 파티션 대화형 관리"
description: "diskpart로 디스크·파티션·볼륨을 선택하고 생성·포맷·삭제하는 법과 select로 옮겨가는 포커스(focus) 개념, /s로 스크립트를 자동화하는 법, 잘못된 디스크 선택이 데이터를 지우는 위험을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 440
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
- diskpart
- 파티션관리
- NTFS
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Security(보안)
- Education(교육)
- CLI
- Automation(자동화)
- Configuration(설정)
- Comparison(비교)
- Beginner
- Administration
image: "wordcloud.png"
---

diskpart는 컴퓨터의 디스크·파티션·볼륨·가상 하드 디스크(VHD)를 관리하는 대화형 명령 인터프리터를 시작하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [43장: chkntfs](/post/cmd/chkntfs-command-disk-check-boot-windows-cmd/)에서 자동 검사 예약을 다룬 뒤 이어진다. 42–43장이 이미 존재하는 볼륨을 검사하는 도구였다면, diskpart는 그 볼륨 자체를 만들고 없애는 더 근본적인 도구다.

**이 장의 깊이**: 고급. diskpart는 그 자체로 별도의 명령 인터프리터이므로, 하위 명령 전체를 다루지 않고 핵심 개념(포커스)과 자주 쓰는 흐름만 다룬다. **다루지 않는 것**: 개별 하위 명령의 모든 옵션은 참고 링크의 공식 문서를 따로 확인해야 한다.

**중요**: diskpart는 로컬 Administrators 그룹 권한이 필요하다.

## 개요 + 정신 모델

diskpart의 핵심 정신 모델은 <strong>포커스(focus)</strong>다. diskpart 안의 거의 모든 명령은 "지금 포커스가 맞춰진 대상"에 대해 동작한다.

> "Before you can use **diskpart** commands, you must first list, and then select an object to give it focus. After an object has focus, any diskpart commands that you type will act on that object." — Microsoft Learn, "diskpart"

즉 `select disk 1`을 실행하면 이후의 `create`, `format`, `assign` 같은 명령은 모두 디스크 1에 대해 실행된다. 포커스는 계층적으로 연쇄된다 — 파티션에 포커스를 주면 그 파티션이 속한 볼륨에도, 볼륨에 포커스를 주면(그 볼륨이 단일 파티션에 매핑된다면) 그 파티션과 디스크에도 함께 포커스가 옮겨간다. 어떤 명령을 실행하기 전에는 반드시 `list`로 대상을 확인하고 `select`로 포커스를 정확히 맞추는 습관이 diskpart를 안전하게 쓰는 전제 조건이다.

## 사용법

```
diskpart [<파라미터>]
```

파라미터 없이 실행하면 대화형 프롬프트(`DISKPART>`)가 열린다. `diskpart /s <스크립트파일>`로 하위 명령을 담은 텍스트 파일을 넘기면 대화 없이 자동으로 실행된다.

## 자주 쓰는 하위 명령

| 명령 | 역할 |
|---|---|
| `list disk` \| `list volume` \| `list partition` | 대상 목록 표시(포커스가 맞춰진 항목에 `*` 표시) |
| `select disk <n>` \| `select volume <n>` | 지정한 디스크·볼륨으로 포커스 이동 |
| `create partition primary [size=<n>]` | 주 파티션 생성 |
| `format fs=ntfs [quick] [label=<이름>]` | 포커스된 볼륨을 지정 파일 시스템으로 포맷 |
| `assign [letter=<x>]` | 포커스된 볼륨에 드라이브 문자 할당 |
| `delete partition` | 포커스된 파티션 삭제 |
| `clean` | 포커스된 디스크의 모든 파티션·볼륨 형식 제거 |
| `convert basic` \| `convert dynamic` \| `convert gpt` \| `convert mbr` | 디스크 형식(기본/동적, MBR/GPT) 변환 |
| `break` | 미러 볼륨을 두 개의 단순 볼륨으로 분리(41장에서 언급한 cmd.exe의 break와는 완전히 무관한 동명의 diskpart 하위 명령이다) |
| `exit` | diskpart 인터프리터 종료 |

## 예시

```
diskpart
list disk
select disk 1
create partition primary
format fs=ntfs label=Backup quick
assign letter=E
exit
```

`diskpart /s`로 위 흐름을 자동화한 스크립트 파일 예시:

```
rem setup-disk1.txt
select disk 1
create partition primary
format fs=ntfs quick
assign letter=E
exit
```

```
diskpart /s setup-disk1.txt
```

## 주의사항·함정

**포커스를 잘못 맞추면 엉뚱한 디스크가 지워진다**: diskpart의 파괴적 명령(`clean`, `delete partition`, `format`)은 대상 이름을 매번 묻지 않고 "지금 포커스가 맞춰진 대상"에 조용히 실행된다. 앞서 다른 디스크를 select했다가 select를 바꾸는 것을 깜빡하면, 의도하지 않은 디스크가 지워질 수 있다. 파괴적 명령을 실행하기 직전에는 반드시 `list disk`(또는 `list volume`)로 `*` 표시가 어디 있는지 재확인하는 것이 diskpart 사용의 기본 원칙이다.

**convert 하위 명령은 46장(convert.exe)과 이름만 같을 뿐 완전히 다르다**: diskpart 안의 `convert basic`/`dynamic`/`gpt`/`mbr`은 디스크의 파티션 구성 방식(기본 디스크 ↔ 동적 디스크, MBR ↔ GPT)을 바꾸는 명령이다. 46장에서 다룰 독립 실행 파일 convert.exe는 FAT/FAT32 볼륨을 NTFS 파일 시스템으로 바꾸는 완전히 다른 도구다. 두 "convert"는 실행되는 프롬프트(diskpart 안 vs cmd.exe 프롬프트)도, 다루는 대상(디스크 파티션 형식 vs 파일 시스템)도 다르다.

**스크립트 자동화는 강력한 만큼 위험도 크다**: `/s`로 스크립트를 실행하면 대화형 확인 없이 하위 명령이 순서대로 실행된다. 프로덕션 서버에 적용하기 전에는 테스트 환경에서 스크립트 전체 흐름을 먼저 검증해야 한다 — `select`가 잘못된 디스크 번호를 가리키는 순간, 그 뒤의 모든 명령이 잘못된 대상에 적용된다.

**PowerShell Storage 모듈이 사실상의 후속 도구다**: `Get-Disk`, `Initialize-Disk`, `New-Partition`, `Format-Volume`, `Clear-Disk`는 각각 diskpart의 `list disk`, 새 디스크 초기화, `create partition`, `format`, `clean`에 대응한다. diskpart가 포커스 개념에 의존하는 대화형 REPL인 것과 달리, 이 cmdlet들은 매 호출마다 대상을 `-DiskNumber`·`-DriveLetter` 같은 명시적 매개변수로 받는 방식이라 포커스를 잘못 옮겨 엉뚱한 디스크를 지우는 diskpart 특유의 위험이 구조적으로 줄어든다. Microsoft도 새로운 자동화 스크립트에서는 diskpart보다 이 Storage 모듈 cmdlet을 우선 사용하도록 권장하는 현대적 대체재로 취급한다.

## 흔한 오개념

<strong>"clean은 디스크를 완전히 초기화(보안 삭제)한다"</strong>는 오해가 있다. `clean`은 파티션·볼륨 형식 정보(파티션 테이블 등)만 제거할 뿐 디스크 전체에 0을 기록하지는 않아, 복구 도구로 이전 데이터가 상당 부분 복구될 수 있다. 실제로 전체 섹터를 0으로 덮어쓰는 더 철저하고 느린 작업은 `clean all`이며, 두 명령은 소요 시간과 결과가 전혀 다르다.

## 다음 장에서는

다음은 45장 — 드라이브를 지정한 파일 시스템으로 포맷하는 `format` 명령을 다룬다.

## 평가 기준

- diskpart의 포커스 개념을 설명하고, list·select로 원하는 대상을 정확히 지정할 수 있다.
- 대화형 diskpart 세션에서 디스크를 파티셔닝·포맷·드라이브 문자 할당하는 기본 흐름을 재현할 수 있다.
- `/s`로 스크립트 자동화를 할 수 있고, 그 위험성(확인 없는 순차 실행)을 설명할 수 있다.
- diskpart의 `convert` 하위 명령과 독립 실행 파일 convert.exe가 이름만 같을 뿐 다른 대상을 다룬다는 것을 설명할 수 있다.

## 참고

- [diskpart | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskpart)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
