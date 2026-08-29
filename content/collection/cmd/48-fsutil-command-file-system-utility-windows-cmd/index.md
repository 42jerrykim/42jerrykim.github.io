---
draft: false
slug: fsutil-command-file-system-utility-windows-cmd
title: "[CMD] 48. fsutil - 파일 시스템 저수준 조회와 구성"
description: "fsutil로 하드 링크, 스파스 파일, 더러운 비트, 볼륨 정보 등 파일 시스템 저수준 속성을 다루는 법과 하위 명령 체계, 고급 사용자 전용 도구라는 Microsoft의 경고, 24장(mklink)의 하드 링크와의 관계를 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 480
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
- fsutil
- NTFS
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Security(보안)
- Education(교육)
- CLI
- Sparse-File
- Configuration(설정)
- Comparison(비교)
- Beginner
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

fsutil은 FAT·NTFS 파일 시스템과 관련된 저수준 작업을 수행하는 유틸리티다. 리파스 포인트 관리, 스파스 파일 처리, 볼륨 마운트 해제 등 다른 CMD 명령으로는 다룰 수 없는 세부 기능에 접근한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [47장: compact](/post/cmd/compact-command-ntfs-compression-windows-cmd/)에서 NTFS 압축을 다룬 뒤 이어진다. compact가 NTFS의 한 가지 기능(압축)만 다뤘다면, fsutil은 그보다 훨씬 넓은 범위의 NTFS·FAT 저수준 기능을 하위 명령으로 묶어 제공한다.

**이 장의 깊이**: 고급. Microsoft Learn 자체가 이 명령을 "고급 사용자 전용"으로 명시한다.

> "You must log on as an administrator or a member of the Administrators group to use `fsutil`. Only advanced users with a thorough understanding of Windows operating systems should use this powerful command." — Microsoft Learn, "fsutil"

**다루지 않는 것**: 24장(mklink)에서 다룬 사용자 친화적 링크 생성 명령과 겹치는 `fsutil hardlink` 등은 그 관계만 짚고, 하위 명령 각각의 전체 옵션은 참고 링크의 공식 문서를 따로 확인해야 한다.

## 사용법

```
fsutil <하위명령> [<인수>...]
```

인수 없이 실행하면 지원되는 하위 명령 목록을 표시한다.

## 주요 하위 명령군

| 하위 명령 | 역할 |
|---|---|
| `fsutil dirty` | 볼륨의 "더러움" 비트를 조회·설정(42장 chkdsk·43장 chkntfs와 연동) |
| `fsutil file` | 파일 단위 동작: 새 파일 생성, 유효 데이터 길이 설정, 할당 범위 조회 |
| `fsutil fsinfo` | 드라이브 목록, 볼륨 정보, NTFS 전용 정보, 파일 시스템 통계 조회 |
| `fsutil hardlink` | 파일의 하드 링크 목록 조회 또는 생성 |
| `fsutil reparsepoint` | 리파스 포인트(디렉터리 정션·볼륨 마운트 지점의 기반) 조회·삭제 |
| `fsutil sparse` | 스파스 파일(대부분이 0으로 채워져 실제 디스크 공간을 쓰지 않는 파일) 관리 |
| `fsutil quota` | NTFS 볼륨의 사용자별 디스크 할당량 관리 |
| `fsutil volume` | 볼륨 마운트 해제, 여유 공간 조회, 특정 클러스터를 쓰는 파일 찾기 |
| `fsutil usn` | 볼륨의 모든 파일 변경 이력을 기록하는 USN 변경 저널 관리 |
| `fsutil 8dot3name` | 8.3 형식 짧은 파일 이름 생성 여부 조회·변경 |

## 예시

```
fsutil volume diskfree C:
fsutil fsinfo volumeinfo C:
fsutil file createnew bigfile.bin 1048576
fsutil sparse setflag myfile.bin
fsutil hardlink list C:\Data\report.txt
fsutil dirty query C:
```

## 주의사항·함정

**`fsutil hardlink`와 24장(mklink)은 같은 대상을 다른 인터페이스로 다룬다**: 24장에서 배운 `mklink /h`가 하드 링크를 만드는 사용자 친화적 명령이었다면, `fsutil hardlink list`는 이미 존재하는 파일이 몇 개의 하드 링크를 갖고 있는지, 그 이름들이 무엇인지 조회하는 진단 도구다. 하드 링크를 새로 만들 때는 mklink가 더 간단하지만, 이미 있는 파일의 링크 관계를 파악할 때는 fsutil이 필요하다.

**`fsutil dirty`는 42–43장의 chkdsk·chkntfs와 직접 연결된다**: 42장(chkdsk)에서 다룬 "볼륨이 더러운 상태"라는 개념을 fsutil로 직접 조회·설정할 수 있다. `fsutil dirty query C:`로 지금 더러운 상태인지 확인하고, `fsutil dirty set C:`로 강제로 더러움을 표시해 다음 재부팅 시 자동 chkdsk를 유도할 수 있다.

**`fsutil file createnew`로 만든 파일은 예측 불가능한 데이터를 담을 수 있다**: 지정한 크기만큼 새 파일을 즉시 만들지만, 그 내용은 0으로 채워지는 것이 보장되지 않는다 — 디스크에 이전에 있던 데이터의 잔여물이 노출될 수 있어, 보안이 중요한 상황에서는 이 하위 명령으로 만든 파일의 초기 내용을 신뢰해서는 안 된다.

**잘못 사용하면 데이터 손상으로 이어질 수 있다**: fsutil은 파일 시스템의 내부 구조에 가까운 수준에서 동작하는 하위 명령이 많아, 각 하위 명령의 정확한 동작을 이해하지 못한 채 실행하면 파일 시스템 무결성에 영향을 줄 수 있다. 프로덕션 시스템에서는 반드시 문서를 확인하고, 가능하면 테스트 환경에서 먼저 검증한 뒤 사용해야 한다.

**`fsutil file setzerodata`는 지정한 범위를 실제로 0으로 덮어쓴다**: 이 하위 명령은 파일의 특정 바이트 범위를 명시적으로 0으로 채워 넣는데, 스파스 파일을 만드는 것과 달리 실제 데이터를 지우는 파괴적 동작이다. 오프셋과 길이를 잘못 지정하면 해당 구간에 있던 실제 데이터가 되돌릴 수 없이 사라지므로, 실행 전 반드시 범위를 재확인해야 한다.

**PowerShell로 완전히 대체할 수 없다**: `fsutil fsinfo volumeinfo`나 `fsutil volume diskfree` 같은 읽기 전용 조회는 `Get-Volume`·`Get-Disk`·`Get-Partition`으로 어느 정도 대체할 수 있지만, 하드 링크 조회(`fsutil hardlink`), 스파스 파일 관리(`fsutil sparse`), 리파스 포인트 조회(`fsutil reparsepoint`), USN 변경 저널 관리(`fsutil usn`) 같은 저수준 쓰기 작업에는 PowerShell에 직접 대응하는 cmdlet이 없다. 이런 기능이 필요하면 여전히 fsutil을 직접 호출하거나 이를 감싸는 별도 스크립트를 작성해야 한다.

## 흔한 오개념

<strong>"fsutil file createnew로 만든 파일은 일반적인 새 파일처럼 내용이 비어 있다"</strong>는 오해가 있다. 지정한 크기만큼 파일을 즉시 할당하지만 그 내용을 0으로 채우는 과정은 보장하지 않아, 디스크에 남아 있던 이전에 삭제된 파일의 잔여 데이터가 그대로 노출될 수 있다. 민감한 정보를 다루던 디스크에서 이 방식으로 파일을 만들면 의도치 않게 과거 데이터가 새 파일 안에 섞여 들어갈 수 있으므로, 보안이 중요한 상황에서는 사용 전 내용을 직접 덮어써 초기화해야 한다.

## 다음 장에서는

다음은 49장 — 볼륨의 이름(레이블)을 만들고 바꾸고 지우는 `label` 명령을 다룬다.

## 평가 기준

- fsutil의 하위 명령 체계를 이해하고, 필요한 기능을 적절한 하위 명령군에서 찾을 수 있다.
- `fsutil hardlink`와 mklink가 같은 대상을 다루는 서로 다른 인터페이스(진단 vs 생성)라는 것을 설명할 수 있다.
- `fsutil dirty`가 chkdsk·chkntfs와 어떻게 연결되는지 설명할 수 있다.
- fsutil이 고급 사용자 전용 도구이며 잘못 쓰면 파일 시스템 손상으로 이어질 수 있다는 것을 안다.

## 참고

- [fsutil | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
