---
draft: false
slug: cacls-command-legacy-acl-windows-cmd
title: "[CMD] 61. cacls - ACL 표시·수정(레거시)"
description: "cacls로 파일 ACL을 표시·수정하는 법과 Microsoft가 공식적으로 지원 중단을 선언한 이유, icacls로 옵션 문법을 그대로 옮길 수 없는 차이, OI·CI·IO 상속 표기를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 610
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
- cacls
- ACL
- Permission
- Security(보안)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- Legacy
- Configuration(설정)
- Workflow(워크플로우)
- Productivity(생산성)
- DevOps
image: "wordcloud.png"
---

cacls는 지정한 파일의 임의 접근 제어 목록(DACL)을 표시하거나 수정하는 명령이다. Microsoft가 공식적으로 지원 중단(deprecated)을 선언했다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [60장: icacls](/post/cmd/icacls-command-file-directory-acl-windows-cmd/)에서 현재 권장되는 ACL 관리 명령을 다룬 뒤 이어진다. 이 장은 그 icacls가 왜, 무엇을 대체했는지 이해하기 위해 옛 명령을 짧게 다룬다.

**이 장의 깊이**: 입문. 레거시 명령이라 실무에서 새로 배울 이유는 많지 않지만, 오래된 배치 파일을 유지 보수할 때 마주칠 수 있다.

## 사용법

```
cacls <파일이름> [/t] [/m] [/l] [/s[:sddl]] [/e] [/c] [/g <사용자>:<권한>] [/r <사용자> [...]] [/p <사용자>:<권한> [...]] [/d <사용자> [...]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/t` | 현재 디렉터리와 모든 하위 디렉터리의 ACL 변경 |
| `/e` | 기존 ACL을 대체하지 않고 편집 |
| `/c` | 접근 거부 오류가 나도 계속 진행 |
| `/g <사용자>:<권한>` | 권한 부여. n(없음) r(읽기) w(쓰기) c(변경) f(완전 제어) |
| `/r <사용자>` | 권한 취소(`/e`와 함께일 때만 유효) |
| `/p <사용자>:<권한>` | 권한 교체 |
| `/d <사용자>` | 접근 거부 |

## 예시

```
cacls myfile.txt
cacls C:\Data /e /g Users:R
cacls /t /e /p User2:F folder
```

## 주의사항·함정

**Microsoft가 공식적으로 지원 중단을 선언했다**: cacls의 현재 공식 문서 최상단에는 다음 경고가 있다.

> "This command has been deprecated. Please use icacls instead." — Microsoft Learn, "cacls"

즉 향후 Windows 버전에서 이 명령 자체가 사라지거나 동작이 바뀔 수 있다는 뜻이다. 새로 작성하는 스크립트에는 cacls를 쓸 이유가 없다.

**icacls로 옵션을 그대로 옮길 수 없다**: 두 명령의 권한 문자 체계와 옵션 이름이 다르다. cacls의 `/g`(부여), `/d`(거부), `/p`(교체)는 icacls에서 각각 `/grant`, `/deny`, `/grant:r`에 대응하지만 이름도 다르고 권한 마스크 표기(cacls의 `n/r/w/c/f` vs icacls의 `N/F/M/RX/R/W/D`와 확장 권한)도 다르다. 오래된 배치 파일의 cacls 명령을 icacls로 옮길 때는 한 줄씩 옵션을 대응시켜 다시 작성해야지, 옵션 이름만 바꿔 끼워 넣는 방식으로는 동작하지 않는다.

**cacls에는 icacls의 여러 기능이 아예 없다**: `/save`·`/restore`로 ACL을 백업·복원하는 기능, 세분화된 상속 옵션(`(OI)`, `(CI)`, `(IO)`, `(NP)`), 소유자 변경(`/setowner`) 같은 기능이 cacls에는 없다. 복잡한 권한 작업이 필요하다면 애초에 icacls로 넘어가야 한다.

**출력에 나타나는 상속 표기는 icacls와 공유된다**: cacls의 조회 결과에도 `OI`(이 폴더와 파일), `CI`(이 폴더와 하위 폴더), `IO`(하위 폴더·파일에만, 현재 개체 제외) 같은 표기가 등장하는데, 이는 60장(icacls)에서 다룬 상속 옵션과 같은 의미 체계를 공유한다 — 두 명령이 결국 같은 Windows ACL 모델을 서로 다른 문법으로 다루고 있다는 근거다.

**`/e` 없이 `/g`·`/p`·`/d`를 쓰면 기존 ACL 전체가 사라진다**: `/e`(편집 모드)를 붙이지 않고 `/g`(부여)·`/p`(교체)·`/d`(거부)를 실행하면, 지정한 사용자의 권한만 바뀌는 게 아니라 파일에 있던 기존 ACL 전체가 새 ACL로 통째로 대체된다. 즉 이전에 다른 사용자나 관리자에게 부여되어 있던 접근 권한까지 조용히 사라질 수 있다 — cacls를 다루다 실무에서 가장 자주 사고로 이어지는 함정이다. 기존 항목을 보존한 채 편집하려면 반드시 `/e`를 함께 써야 한다.

**cacls를 새로 배울 이유는 없다**: 60장에서 다룬 icacls가 공식 후속 명령이고, PowerShell에서는 `Get-Acl`/`Set-Acl`이 그 자리를 대신한다. cacls는 이미 지원 중단(deprecated)으로 명시되어 있으므로, 새로 작성하는 배치 스크립트든 PowerShell 스크립트든 cacls를 선택할 이유가 없다 — 기존 스크립트를 유지 보수할 때 문법을 해석하는 용도로만 남아 있다.

## 흔한 오개념

<strong>"cacls `/g`는 icacls의 `/grant`처럼 권한을 추가만 한다"</strong>는 오해가 있다. icacls의 `/grant`(`:r` 없이)는 기존 명시적 권한에 더해지지만, cacls의 `/g`는 `/e`와 함께 쓰지 않는 한 대상 파일의 ACL 전체를 지정한 항목으로 대체해버린다 — 같은 자리에 있는 옵션이라고 동작까지 같을 거라 가정하면 다른 사용자의 접근 권한을 실수로 지워버릴 수 있다.

## 다음 장에서는

다음은 62장 — Part 6의 마지막 장으로, 파일 공유를 통해 원격 사용자가 열어 둔 파일을 조회·연결 해제하는 `openfiles` 명령을 다룬다.

## 평가 기준

- cacls로 파일 ACL을 조회·부여·거부할 수 있다.
- cacls가 공식적으로 지원 중단되었고 icacls로 대체해야 한다는 것을 안다.
- cacls와 icacls의 옵션·권한 표기가 달라 그대로 옮겨 쓸 수 없다는 것을 설명할 수 있다.
- cacls에는 없고 icacls에만 있는 기능(백업/복원, 세분화된 상속 옵션, 소유자 변경)을 안다.

## 참고

- [cacls | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cacls)
- [icacls | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls)
