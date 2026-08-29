---
draft: false
slug: chkntfs-command-disk-check-boot-windows-cmd
title: "[CMD] 43. chkntfs - 부팅 시 자동 디스크 검사 설정"
description: "chkntfs로 부팅 시 chkdsk 자동 실행 대상 볼륨을 조회·제외·예약하는 법과 /x가 누적되지 않고 덮어쓰기되는 반면 /c는 누적된다는 비대칭, 카운트다운 시간을 0으로 두면 취소가 불가능해지는 함정을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 430
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
- chkntfs
- 부팅검사
- NTFS
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Security(보안)
- Education(교육)
- CLI
- Comparison(비교)
- Configuration(설정)
- Beginner
- Administration
- Productivity(생산성)
image: "wordcloud.png"
---

chkntfs는 컴퓨터 시작 시 자동 디스크 검사(chkdsk)가 실행될 볼륨을 조회하거나 그 설정을 바꾸는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [42장: chkdsk](/post/cmd/chkdsk-command-check-disk-errors-windows-cmd/)에서 디스크를 직접 검사하는 법을 다룬 뒤 이어진다. chkdsk가 "지금 당장 검사"였다면, chkntfs는 "다음 부팅 때 무엇을 검사할지 예약·관리"하는 명령이다.

**이 장의 깊이**: 중급. **Administrators 그룹** 구성원이어야 실행할 수 있다.

## 사용법

```
chkntfs <볼륨> [...]
chkntfs [/d]
chkntfs [/t[:<시간>]]
chkntfs [/x <볼륨> [...]]
chkntfs [/c <볼륨> [...]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `<볼륨>` | 지정한 볼륨의 파일 시스템 종류와 예약 상태 표시 |
| `/d` | 카운트다운 시간을 제외한 모든 설정을 기본값으로 복원(모든 볼륨이 부팅 시 검사 대상) |
| `/t[:시간]` | Autochk.exe 실행 전 카운트다운 시간(초)을 표시하거나 변경 |
| `/x <볼륨>` | 지정한 볼륨을 다음 부팅 시 검사에서 제외(더러움 표시가 있어도) |
| `/c <볼륨>` | 지정한 볼륨을 다음 부팅 시 검사하도록 예약 |

## 예시

```
chkntfs c:
chkntfs /t
chkntfs /t:30
chkntfs /x d: e:
chkntfs /d
chkntfs /x c: d: e:
chkntfs /c d:
```

마지막 세 줄은 D 볼륨만 부팅 시 검사 대상으로 남기고 C·E는 제외하는 순서를 보여준다 — 먼저 `/d`로 기본값을 복원하고, `/x`로 원치 않는 볼륨을 모두 제외한 뒤, `/c`로 원하는 볼륨만 다시 예약한다.

## 주의사항·함정

**`/x`는 덮어쓰지만 `/c`는 누적된다**: 이 장에서 가장 자주 놓치는 비대칭이다.

> "The **/x** command-line option isn't accumulative. If you type it more than once, the most recent entry overrides the previous entry." — Microsoft Learn, "chkntfs"
>
> "The **/c** command-line option is accumulative. If you type **/c** more than once, each entry remains." — Microsoft Learn, "chkntfs"

즉 `chkntfs /x c:`를 실행한 뒤 `chkntfs /x d:`를 실행하면 C의 제외 설정은 사라지고 D만 제외된다. 반면 `/c`는 실행할 때마다 예약 목록에 더해진다. 특정 볼륨만 정확히 검사하도록 만들고 싶다면, 위 예시처럼 `/d`로 초기화 → `/x`로 전부 제외 → `/c`로 원하는 것만 다시 추가하는 순서를 지켜야 한다.

**카운트다운을 0으로 두면 취소할 수 없다**: `/t:0`으로 설정할 수는 있지만, Microsoft Learn은 이렇게 하면 시간이 걸리는 자동 검사를 취소할 기회 자체가 사라진다고 경고한다.

> "Although you can set the Autochk.exe initiation countdown time to zero, doing so will prevent you from canceling a potentially time-consuming automatic file check." — Microsoft Learn, "chkntfs"

부팅마다 큰 볼륨의 전체 검사가 예약되어 있는데 카운트다운이 0이면, 급하게 부팅해야 하는 상황에서도 검사를 건너뛸 수 없다.

**"더럽다"는 표시는 chkntfs가 만드는 게 아니다**: chkntfs는 볼륨이 "더러운"(dirty, 즉 비정상 종료 등으로 무결성 확인이 필요한) 상태인지 조회·설정할 뿐, 이 상태 자체는 시스템이 파일 쓰기 도중 문제를 겪었을 때 자동으로 표시된다. 42장(chkdsk)에서 언급한 `fsutil dirty` 명령으로 이 더러움 표시를 직접 조회·설정할 수도 있다.

**PowerShell에 직접 대응하는 cmdlet은 없다**: chkntfs가 하는 "부팅 시 어떤 볼륨을 검사할지 예약·제외하는" 기능을 그대로 감싼 PowerShell cmdlet은 존재하지 않는다. 개념적으로 가장 가까운 것은 `Repair-Volume`이 갖는 예약·스캔 동작 정도이지만, `Repair-Volume`은 즉시 검사를 트리거하는 데 초점이 맞춰져 있어 chkntfs처럼 특정 볼륨을 부팅 대상에서 명시적으로 제외하거나 카운트다운을 조정하는 기능은 제공하지 않는다. 이런 부팅 시점 예약 제어가 필요하면 여전히 chkntfs를 직접 쓰거나 레지스트리(`BootExecute` 값)를 조작해야 한다.

## 흔한 오개념

<strong>"/x와 /c는 서로 반대되는 토글 스위치다"</strong>는 오해가 있다. 실제로는 /x는 실행할 때마다 이전 지정을 덮어쓰는 반면 /c는 실행할 때마다 목록에 누적되는, 서로 다른 저장 방식으로 동작한다. `/x c:`를 실행한 뒤 `/c c:`를 실행해도 단순히 "제외를 취소하고 포함으로 되돌린" 것이 아니라, /x 쪽 설정은 최신 값 하나로 덮어써지고 /c 쪽 설정은 그와 별개로 계속 쌓여간다.

## 다음 장에서는

다음은 44장 — 디스크와 파티션을 대화형으로 관리하는 `diskpart` 명령을 다룬다.

## 평가 기준

- chkntfs로 부팅 시 자동 검사 대상 볼륨을 조회·제외·예약할 수 있다.
- `/x`는 덮어쓰고 `/c`는 누적된다는 비대칭을 설명하고, 특정 볼륨만 검사 대상으로 남기는 순서를 재현할 수 있다.
- 카운트다운을 0으로 설정하면 왜 위험한지 설명할 수 있다.
- "더러운" 볼륨 표시가 chkntfs가 아니라 시스템 상태에서 비롯된다는 것을 안다.

## 참고

- [chkntfs | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/chkntfs)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
