---
draft: false
slug: chkdsk-command-check-disk-errors-windows-cmd
title: "[CMD] 42. chkdsk - 디스크 오류 검사와 수정"
description: "chkdsk로 볼륨의 파일 시스템 오류를 검사·수정하는 법과 /f·/r·/x 옵션의 관계, 사용 중인 볼륨은 다음 재부팅에 예약된다는 동작, 4단계 종료 코드를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 420
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
- chkdsk
- 디스크검사
- NTFS
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- ERRORLEVEL
- Security(보안)
- Education(교육)
- CLI
- Comparison(비교)
- Configuration(설정)
- Beginner
- Administration
image: "wordcloud.png"
---

chkdsk는 볼륨의 파일 시스템과 파일 시스템 메타데이터를 논리적·물리적 오류 관점에서 검사하는 명령이다. Part 5(디스크와 파일 시스템 관리)의 첫 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [41장: break](/post/cmd/break-command-extended-ctrl-c-windows-cmd/)로 Part 4(배치 스크립팅)를 마친 뒤 이어지며, <strong>Part 5(디스크와 파일 시스템 관리)</strong>의 첫 장이다. 지금까지 4개 Part는 파일 하나하나를 다뤘다면, 이 장부터는 시선이 파일이 놓인 디스크 전체로 넓어진다.

**이 장의 깊이**: 중급. **다루지 않는 것**: 부팅 시 자동 검사를 예약·해제하는 것은 43장(chkntfs)에서, 파티션 자체를 만들고 없애는 것은 44장(diskpart)에서 다룬다.

**중요**: chkdsk를 실행하려면 로컬 Administrators 그룹 구성원 권한이 최소로 필요하다.

## 사용법

```
chkdsk [<볼륨>[[<경로>]<파일이름>]] [/f] [/v] [/r] [/x] [/i] [/c] [/l[:<크기>]] [/b] [/scan] [/spotfix] [/offlinescanandfix]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| (없음) | 볼륨 상태만 표시하고 오류를 수정하지 않음 |
| `/f` | 디스크 오류 수정. 드라이브를 잠글 수 있어야 함 |
| `/r` | 배드 섹터를 찾아 읽을 수 있는 정보를 복구. `/f`의 기능을 포함 |
| `/x` | 필요 시 볼륨을 먼저 마운트 해제(모든 열린 핸들 무효화). `/f`의 기능을 포함 |
| `/i` | NTFS 전용. 색인 항목 검사를 간소화해 시간 단축 |
| `/c` | NTFS 전용. 폴더 구조 내 순환 검사를 생략해 시간 단축 |
| `/b` | NTFS 전용. 배드 클러스터 목록을 지우고 전체 재검사. `/r`의 기능을 포함 |
| `/scan` | NTFS 전용. 온라인 스캔 실행 |
| `/spotfix` | NTFS 전용. 스팟 수정 실행 |

### 종료 코드

| 종료 코드 | 의미 |
|---|---|
| 0 | 오류 없음 |
| 1 | 오류를 발견하고 수정함 |
| 2 | 디스크 정리를 수행했거나(`/f` 없이) 수행하지 않음 |
| 3 | 디스크를 검사할 수 없었거나 오류를 수정하지 못함 |

## 예시

```
chkdsk d: /f
chkdsk *.*
chkdsk C: /scan
```

## 주의사항·함정

**사용 중인 볼륨은 다음 재부팅으로 예약된다**: `/f`로 오류 수정을 요청했는데 드라이브에 열린 파일이 있으면 chkdsk는 즉시 실행되지 못하고 다음 메시지를 표시한다.

> "Chkdsk cannot run because the volume is in use by another process. Would you like to schedule this volume to be checked the next time the system restarts? (Y/N)" — Microsoft Learn, "chkdsk"

시스템 드라이브(부팅 파티션)라면, Y를 선택했을 때 재부팅 자체를 chkdsk가 자동으로 트리거한다. 43장(chkntfs)에서 다루는 `chkntfs /c`도 같은 예약을 프로그래밍적으로 걸 수 있는 대안이다.

**`/f` 없이 실행하면 아무것도 고치지 않는다**: 옵션 없이 chkdsk만 실행하면 상태 보고만 하고 오류를 수정하지 않는다. 활성 파티션에서 `/f` 없이 실행하면 드라이브를 잠글 수 없어 실제로는 존재하지 않는 오류(허위 오류)를 보고할 수도 있다.

**`/r`, `/x`, `/b`는 각각 더 약한 옵션의 기능을 포함한다**: `/r`은 `/f`를, `/x`는 `/f`를, `/b`는 `/r`(따라서 `/f`도)을 포함한다. 즉 `/r`만 지정해도 오류 수정까지 함께 이뤄진다 — 옵션을 여러 개 겹쳐 쓸 필요는 없지만, 이 포함 관계를 모르면 `/f`를 빠뜨렸다고 착각하기 쉽다.

**HDD와 SSD에서 소요 시간이 다르다**: `/r`처럼 모든 섹터를 순회하는 검사는 회전 디스크(HDD)에서는 물리적으로 헤드가 이동해야 해서 느리고, SSD에서는 탐색 지연이 없어 상대적으로 빠르다. 다만 SSD에서 `/r`을 반복 실행하면 쓰기·삭제 사이클이 늘어나 수명에 미세한 영향을 줄 수 있다는 점도 Microsoft Learn이 언급한다.

**중단해도 볼륨이 더 나빠지지는 않는다**: chkdsk 실행 중 중단을 권장하지는 않지만, 중단한다고 해서 실행 전보다 볼륨이 더 손상되지는 않는다 — 다시 실행하면 남은 손상을 검사·복구한다.

**PowerShell에서는 `Repair-Volume`이 chkdsk를 대체한다**: `Repair-Volume -DriveLetter C -Scan`은 옵션 없는 chkdsk(상태 보고만)에, `Repair-Volume -DriveLetter C -OfflineScanAndFix`는 `/f`처럼 오류를 실제로 수정하는 동작에 대략 대응한다. 다만 cmdlet 단위 매핑이 완전히 1:1은 아니다 — `-Scan`은 온라인 스캔만 수행하고 실제 수정은 하지 않으며, 볼륨을 오프라인으로 전환해 수정하려면 `-OfflineScanAndFix`를 명시적으로 지정해야 한다.

## 흔한 오개념

<strong>"chkdsk는 항상 즉시 실행된다"</strong>는 오해가 있다. 시스템 드라이브처럼 볼륨이 사용 중이면 `/f`나 `/x`를 지정해도 chkdsk는 그 자리에서 실행되지 않고 다음 재부팅으로 검사를 예약할 뿐이다. 명령을 실행했는데 화면에 아무 변화가 없어 보인다고 실패로 오해하기 쉽지만, 실제로는 재부팅 시점까지 대기 중인 상태다.

## 다음 장에서는

다음은 43장 — 부팅 시 자동으로 chkdsk가 실행되도록 예약하는 `chkntfs` 명령을 다룬다.

## 평가 기준

- chkdsk로 볼륨 상태를 조회하고, `/f`·`/r`·`/x`로 오류를 수정할 수 있다.
- 사용 중인 볼륨에서 `/f`를 실행하면 왜 다음 재부팅으로 예약되는지 설명할 수 있다.
- `/r`, `/x`, `/b`가 각각 더 약한 옵션을 포함하는 관계를 설명할 수 있다.
- HDD와 SSD에서 `/r` 검사 시간과 주의사항이 어떻게 다른지 안다.

## 참고

- [chkdsk | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/chkdsk)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
