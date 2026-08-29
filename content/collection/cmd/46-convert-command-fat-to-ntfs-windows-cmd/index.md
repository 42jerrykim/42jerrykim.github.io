---
draft: false
slug: convert-command-fat-to-ntfs-windows-cmd
title: "[CMD] 46. convert - FAT·FAT32 볼륨을 NTFS로 변환"
description: "convert /fs:ntfs로 기존 파일을 유지한 채 FAT·FAT32 볼륨을 NTFS로 변환하는 법과 되돌릴 수 없다는 제약, 현재 드라이브 변환이 재부팅으로 예약되는 동작, diskpart의 동명 하위 명령과 혼동하지 않는 법을 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 460
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
- convert
- NTFS
- FAT32
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Security(보안)
- Education(교육)
- CLI
- Legacy
- Comparison(비교)
- Configuration(설정)
- Beginner
- Administration
image: "wordcloud.png"
---

convert는 FAT·FAT32 볼륨을 기존 파일과 디렉터리를 그대로 유지한 채 NTFS 파일 시스템으로 변환하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [45장: format](/post/cmd/format-command-format-disk-windows-cmd/)에서 볼륨을 새로 포맷하는 법을 다룬 뒤 이어진다. format이 데이터를 지우고 새로 시작하는 방법이었다면, convert는 데이터를 유지한 채 파일 시스템만 바꾸는 대안이다.

**이 장의 깊이**: 중급. **참고 사항**: 이 명령은 Microsoft의 현재 Windows 명령줄 참조 문서 체계에서 별도 페이지가 유지되지 않는다 — `convert`라는 이름이 44장(diskpart)의 `convert basic`/`dynamic`/`gpt`/`mbr` 하위 명령과 겹치면서, 현재 공식 문서의 `windows-commands/convert` 페이지는 diskpart 쪽 하위 명령만 안내한다. 이 장의 내용은 Microsoft가 별도로 보관 중인 이전 버전(Windows Server 2012 R2 문서) 페이지를 1차 출처로 삼았다.

## 사용법

```
convert [<볼륨>] /fs:ntfs [/v] [/cvtarea:<파일이름>] [/nosecurity] [/x]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `<볼륨>` | 변환할 드라이브 문자·마운트 지점·볼륨 이름 |
| `/fs:ntfs` | 필수. NTFS로 변환 |
| `/v` | 자세한 모드. 변환 중 모든 메시지 표시 |
| `/cvtarea:<파일이름>` | MFT와 NTFS 메타데이터를 미리 만들어둔 연속 placeholder 파일에 기록(단편화 감소 목적) |
| `/nosecurity` | 변환된 파일·디렉터리에 모든 사용자가 접근 가능하도록 보안 설정 |
| `/x` | 필요 시 볼륨을 먼저 마운트 해제 |

## 예시

```
convert e: /fs:ntfs /v
```

`/cvtarea`를 쓰려면 변환 전에 `fsutil file createnew`로 placeholder 파일을 미리 만들어 둬야 한다 — convert 자신은 이 파일을 만들지 않고 덮어쓸 뿐이다.

```
fsutil file createnew C:\placeholder.txt 26214400
convert C: /fs:ntfs /cvtarea:placeholder.txt
```

## 주의사항·함정

**되돌릴 수 없다**: NTFS로 변환한 볼륨은 다시 FAT나 FAT32로 되돌릴 수 없다. 변환 전에는 되돌릴 필요가 없다는 확신이 있어야 하고, 중요한 데이터라면 변환과 무관하게 백업을 먼저 해두는 것이 안전하다.

**현재 드라이브나 시스템 볼륨은 재부팅으로 예약된다**: 42장(chkdsk)에서 본 것과 같은 패턴이다. convert가 드라이브를 잠글 수 없으면(그 드라이브가 시스템 볼륨이거나 현재 사용 중인 드라이브라면) 다음 재부팅 시 변환하도록 예약할 수 있다. 재부팅을 바로 할 수 없는 상황이라면, 변환이 완료될 때까지 추가 시간이 걸린다는 점을 미리 계획에 반영해야 한다.

**변환된 볼륨은 처음부터 NTFS였던 볼륨만큼 최적화되어 있지 않다**: 기존 디스크 사용 패턴 때문에 MFT(마스터 파일 테이블)가 새로 포맷한 NTFS 볼륨과 다른 위치에 생성되어, 변환 직후에는 성능이 원래 NTFS만큼 나오지 않을 수 있다. 성능이 중요한 볼륨이라면 변환 대신 데이터를 백업한 뒤 45장(format)으로 아예 새로 NTFS 포맷하는 방법을 고려할 만하다.

**diskpart의 convert와 이름만 같다**: 44장에서 다룬 것처럼, diskpart 안의 `convert basic`/`dynamic`/`gpt`/`mbr`은 디스크의 파티션 구성 방식을 바꾸는 명령이지 파일 시스템을 바꾸는 명령이 아니다. 이 장의 convert(FAT→NTFS)는 cmd.exe 프롬프트에서 직접 실행하는 완전히 다른 독립 실행 파일이다.

**PowerShell에는 파일을 보존한 채 변환하는 cmdlet이 없다**: `Format-Volume -FileSystem NTFS`는 이름만 보면 비슷해 보이지만 볼륨을 새로 포맷하는 명령이라 기존 파일이 전부 사라진다. convert.exe처럼 FAT·FAT32의 기존 파일을 그대로 유지한 채 파일 시스템만 NTFS로 바꾸는 비파괴적 변환 기능은 PowerShell cmdlet으로 제공되지 않으며, 이 작업에는 여전히 convert.exe가 유일한 선택지다.

## 흔한 오개념

<strong>"NTFS로 변환해도 나중에 FAT로 되돌릴 수 있다"</strong>는 오해가 있다. 실제로 convert에 의한 FAT/FAT32 → NTFS 변환은 한 방향으로만 진행되며, 되돌리는 내장 명령은 존재하지 않는다. FAT로 되돌리려면 볼륨을 백업한 뒤 새로 FAT로 포맷하고 데이터를 복원하는 수밖에 없다.

## 다음 장에서는

다음은 47장 — NTFS 볼륨에서 파일·디렉터리의 압축 상태를 표시하고 바꾸는 `compact` 명령을 다룬다.

## 평가 기준

- convert로 FAT·FAT32 볼륨을 데이터 손실 없이 NTFS로 변환할 수 있다.
- 변환이 되돌릴 수 없다는 것과, 시스템 볼륨 변환이 재부팅으로 예약될 수 있다는 것을 설명할 수 있다.
- 변환된 볼륨이 처음부터 NTFS였던 볼륨과 성능 면에서 어떻게 다를 수 있는지 안다.
- convert.exe와 diskpart의 convert 하위 명령이 서로 다른 대상을 다룬다는 것을 설명할 수 있다.

## 참고

- [Convert2 | Microsoft Learn(보관된 문서)](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc730863(v=ws.11))
- [diskpart | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskpart)
