---
draft: false
slug: compact-command-ntfs-compression-windows-cmd
title: "[CMD] 47. compact - NTFS 파일·디렉터리 압축"
description: "compact로 NTFS 볼륨의 파일·디렉터리 압축 상태를 표시·변경하는 법과 디렉터리 압축 설정이 이미 있는 파일에는 소급 적용되지 않는다는 함정, FAT 볼륨에서는 쓸 수 없는 제약을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 470
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
- compact
- NTFS압축
- NTFS
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Performance
- Education(교육)
- CLI
- Comparison(비교)
- Configuration(설정)
- Beginner
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

compact는 NTFS 파티션에 있는 파일·디렉터리의 압축 상태를 표시하거나 바꾸는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [46장: convert](/post/cmd/convert-command-fat-to-ntfs-windows-cmd/)에서 FAT를 NTFS로 바꾸는 법을 다룬 뒤 이어진다. NTFS가 전제되어야 쓸 수 있는 기능이라는 점에서 자연스럽게 이어진다.

**이 장의 깊이**: 중급.

## 사용법

```
compact [/C | /U] [/S[:<디렉터리>]] [/A] [/I] [/F] [/Q] [<파일이름> [...]]
```

인수 없이 실행하면 현재 디렉터리와 그 안의 파일들의 압축 상태를 표시한다.

## 옵션

| 옵션 | 설명 |
|---|---|
| `/C` | 지정한 디렉터리·파일 압축. 디렉터리에 적용하면 이후 추가되는 파일도 압축되도록 표시 |
| `/U` | 압축 해제. 디렉터리에 적용하면 이후 추가되는 파일은 압축되지 않도록 표시 |
| `/S[:디렉터리]` | 지정 디렉터리(기본은 현재 디렉터리)와 모든 하위 디렉터리에 적용 |
| `/A` | 숨김·시스템 파일도 표시·처리(기본은 제외) |
| `/I` | 오류가 나도 계속 진행(기본은 오류 시 중단) |
| `/F` | 이미 압축된 파일도 강제로 다시 압축(부분 압축 복구용) |
| `/Q` | 핵심 정보만 표시 |

## 예시

```
compact /c /s
compact /c /s *.*
compact /c /i /s:\
compact /c /s:\tmp *.bmp
compact /c /f zebra.bmp
compact /u c:\tmp
```

## 주의사항·함정

**디렉터리에 압축을 설정해도 이미 있는 파일은 그대로다**: 이 장의 가장 중요한 함정이다. Microsoft Learn은 이를 명확히 짚는다.

> "The compression state of a directory indicates whether files are automatically compressed when they are added to the directory. Setting the compression state of a directory does not necessarily change the compression state of files that are already in the directory." — Microsoft Learn, "compact"

즉 `compact /c C:\Data`만 실행하면 앞으로 그 디렉터리에 추가되는 파일은 자동으로 압축되지만, 이미 그 안에 있던 기존 파일은 압축되지 않은 채로 남는다. 기존 파일까지 압축하려면 `/s`로 디렉터리 자체와 그 안의 파일들을 함께 지정해야 한다 — 두 번째 예시(`compact /c /s *.*`)가 그 패턴이다.

**FAT·FAT32 볼륨에서는 쓸 수 없다**: NTFS 파일 시스템 압축 기능의 명령줄 버전이므로, FAT나 FAT32 볼륨에는 애초에 적용할 수 없다. 46장(convert)으로 NTFS로 바꾼 뒤에야 이 명령을 쓸 수 있다.

**중단된 압축은 `/f`로 강제 완료해야 한다**: 시스템 크래시로 압축이 일부만 진행된 파일은 이후 compact 실행에서 "이미 압축됨"으로 오인되어 건너뛰어질 수 있다. `/c`와 `/f`를 함께 지정해야 그런 파일을 처음부터 다시 완전히 압축한다.

**압축은 CPU와 맞바꾸는 트레이드오프다**: 압축된 파일은 읽기·쓰기마다 실시간으로 압축·해제 연산이 필요하므로 디스크 공간을 아끼는 대신 CPU 사용량이 늘어난다. 이미 압축된 형식(zip, jpg, mp4 등)은 NTFS 압축을 걸어도 추가로 줄어들지 않으면서 CPU 비용만 발생할 수 있어, 어떤 파일에 compact를 적용할지 선별하는 것이 중요하다.

**압축과 EFS 암호화는 동시에 적용할 수 없다**: NTFS는 파일 단위로 압축과 암호화 중 하나만 허용한다. 이미 EFS로 암호화된 파일이나 폴더에 `compact /c`를 실행하면 압축이 걸리지 않거나 오류가 발생하고, 반대로 압축된 파일을 암호화하면 압축이 자동으로 해제된다. 두 기능을 함께 쓰려는 시도는 처음부터 실패하도록 설계되어 있다.

**PowerShell에 compact.exe를 직접 감싼 cmdlet은 없다**: `Set-ItemProperty`로 파일의 일반 속성(읽기 전용, 숨김 등)은 바꿀 수 있지만, NTFS 압축 상태는 그런 표준 파일 속성이 아니라 별도의 FSCTL 호출이 필요한 NTFS 전용 기능이라 `Set-ItemProperty`만으로는 켜고 끌 수 없다. 압축을 스크립트로 자동화해야 하는 경우 PowerShell에서도 여전히 `compact.exe`를 외부 프로세스로 호출하거나, Win32 API(`DeviceIoControl`의 `FSCTL_SET_COMPRESSION`)를 직접 호출하는 방식을 쓰는 경우가 많다.

## 흔한 오개념

<strong>"compact로 압축한 파일에 EFS 암호화도 함께 걸 수 있다"</strong>는 오해가 있다. NTFS에서 압축과 EFS 암호화는 동일 파일·폴더에 동시에 적용할 수 없는 상호 배타적 속성이다. 한쪽을 켜면 다른 쪽은 자동으로 꺼지며, 이미 암호화된 파일에 `compact /c`를 실행하면 압축이 적용되지 않고 실패하는 경우가 흔하다.

## 다음 장에서는

다음은 48장 — 파일 시스템 저수준 속성을 조회·구성하는 `fsutil` 명령을 다룬다.

## 평가 기준

- compact로 파일·디렉터리의 NTFS 압축 상태를 조회·변경할 수 있다.
- 디렉터리 압축 설정이 이미 있는 파일에는 자동으로 적용되지 않는다는 것과, `/s`로 기존 파일까지 함께 압축하는 방법을 설명할 수 있다.
- compact가 FAT·FAT32 볼륨에서는 동작하지 않는 이유를 안다.
- 압축이 디스크 공간과 CPU 사용량 사이의 트레이드오프라는 것과, 이미 압축된 형식 파일에는 효과가 적다는 것을 설명할 수 있다.

## 참고

- [compact | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/compact)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
