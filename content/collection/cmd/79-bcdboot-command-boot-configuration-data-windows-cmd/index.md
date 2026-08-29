---
draft: false
slug: bcdboot-command-boot-configuration-data-windows-cmd
title: "[CMD] 79. bcdboot - 시동 구성 데이터 복사"
description: "bcdboot로 Windows 디렉터리에서 시스템 파티션으로 부팅 파일을 복사해 BCD 저장소를 새로 만들거나 복구하는 법과 복구 환경·설치 미디어에서 부팅이 깨진 시스템을 되살리는 실전 절차를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 790
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
- bcdboot
- 부팅복구
- BCD
- Boot(부팅)
- Recovery(복구)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Administration
- Education(교육)
- CLI
- Configuration(설정)
- System(시스템)
- Disk(디스크)
- Enterprise
image: "wordcloud.png"
---

bcdboot는 지정한 Windows 디렉터리를 원본으로 삼아 시스템 파티션에 부팅에 필요한 파일을 복사하고, BCD(Boot Configuration Data) 저장소를 새로 만들거나 복구하는 명령이다. Part 9(부팅 구성과 기타 유틸리티)의 첫 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [78장: net user](/post/cmd/net-user-command-manage-user-accounts-windows-cmd/)로 Part 8(네트워크와 원격 진단)을 마친 뒤 이어지며, <strong>Part 9(부팅 구성과 기타 유틸리티)</strong>의 첫 장이다. 지금까지 실행 중인 시스템 안에서 파일·프로세스·네트워크를 다뤘다면, 이 장부터는 그 시스템이 애초에 부팅되는 방식 자체를 다룬다.

**이 장의 깊이**: 고급. **다루지 않는 것**: BCD 저장소의 개별 항목을 조회·수정하는 것은 80장(bcdedit)에서 다룬다. bcdboot는 "부팅 파일을 어디에 배치할 것인가"를, bcdedit는 "이미 배치된 항목을 어떻게 편집할 것인가"를 각각 담당한다.

## 개요 + 정신 모델

bcdboot의 핵심 동작은 단순하다.

> "Enables you to quickly set up a system partition, or to repair the boot environment located on the system partition. The system partition is set up by copying a simple set of Boot Configuration Data (BCD) files to an existing empty partition." — Microsoft Learn, "bcdboot"

즉 bcdboot는 이미 설치되어 있는 Windows 디렉터리(원본)를 읽어, 그 안의 부팅 파일 사본을 시스템 파티션(대상)에 복사하고 그 파티션에 맞는 BCD 저장소를 새로 생성한다. 새 시스템을 처음 배포할 때 시스템 파티션을 준비하는 용도로도, 기존 시스템의 BCD가 손상되어 부팅이 안 될 때 복구 환경에서 재생성하는 용도로도 쓰인다.

## 사용법

```
bcdboot <원본> [/l <로케일>] [/s <볼륨문자>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `<원본>` | 부팅 환경 파일의 원본으로 사용할 Windows 디렉터리 경로 |
| `/l <로케일>` | 로케일 지정(기본값은 US English) |
| `/s <볼륨문자>` | 시스템 파티션의 볼륨 문자(기본값은 펌웨어가 식별한 시스템 파티션) |

## 예시

```
bcdboot C:\Windows
bcdboot C:\Windows /s S:
bcdboot D:\Windows /s C: /l ko-KR
bcdboot C:\Windows /l en-US
bcdboot D:\Windows /s S:
```

## 주의사항·함정

**복구 환경에서 드라이브 문자가 평소와 다르다**: Windows 복구 환경(WinRE)이나 설치 미디어로 부팅해 bcdboot를 실행할 때는, 평상시 `C:`였던 Windows 설치 드라이브가 다른 문자로 잡히는 경우가 흔하다. 실행 전 `diskpart`의 `list volume`이나 `dir`로 실제 Windows 디렉터리가 어느 드라이브에 있는지 먼저 확인해야 한다 — 44장(diskpart)에서 다룬 대화형 파티션 관리가 이 확인 과정에 바로 이어진다.

**대상 파티션은 비어 있어야 정상 동작한다**: 원문이 명시하듯 대상은 "기존의 빈 파티션(an existing empty partition)"이다. 이미 다른 부팅 관련 파일이 들어 있는 파티션에 실행하면 예상과 다른 결과가 나올 수 있으므로, 새 시스템 파티션을 준비하는 시나리오에서만 안전하게 쓸 수 있다.

**잘못된 원본·대상 지정은 부팅 불능으로 이어진다**: `<원본>` 경로를 잘못 지정하거나 `/s`로 엉뚱한 파티션을 지정하면, 정상 부팅 중이던 시스템의 부팅 환경이 덮어써질 위험이 있다. 42장(chkdsk)·44장(diskpart)과 마찬가지로 이 명령은 관리자 권한과 신중한 대상 확인을 요구하는 "복구 불가 동작" 범주에 속한다.

**PowerShell에는 대응하는 cmdlet이 없다**: Windows 설치 디렉터리에서 부팅 파일을 시스템 파티션으로 복사하고 그 자리에 새 BCD 저장소를 만드는 bcdboot 고유의 기능을 대체하는 PowerShell cmdlet은 존재하지 않는다. 이 복구 작업은 여전히 CMD(또는 WinRE·설치 미디어의 명령 프롬프트)에서 bcdboot.exe를 직접 실행해야 하는, PowerShell로 옮겨가지 않은 몇 안 되는 영역 중 하나다.

## 흔한 오개념

<strong>"bcdboot는 지금 부팅되어 있는 Windows에만 쓸 수 있다"</strong>는 오해다. 실제로는 Windows 복구 환경(WinRE)이나 설치 미디어로 부팅한 뒤, 현재 실행 중인 시스템이 아니라 디스크에 있는 다른(꺼져 있는) Windows 설치의 부팅 파일을 고치는 용도로 가장 흔하게 쓰인다. 이때 `<원본>`에는 복구 환경 자신의 Windows 디렉터리가 아니라, 부팅이 안 되는 그 다른 설치의 Windows 디렉터리 경로(예: `D:\Windows`)를 지정해야 한다.

## 다음 장에서는

다음은 80장 — BCD 저장소의 개별 항목을 조회·편집하는 `bcdedit` 명령을 다룬다.

## 평가 기준

- bcdboot로 Windows 디렉터리를 원본 삼아 시스템 파티션에 부팅 파일을 복사할 수 있다.
- `/s`·`/l` 옵션으로 대상 파티션·로케일을 지정하는 이유를 설명할 수 있다.
- 복구 환경에서 드라이브 문자가 평소와 다를 수 있어 사전 확인이 필요하다는 것을 안다.
- bcdboot(파일 배치)와 bcdedit(항목 편집)의 역할 차이를 구분할 수 있다.

## 참고

- [bcdboot | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/bcdboot)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
