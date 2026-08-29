---
draft: false
slug: icacls-command-file-directory-acl-windows-cmd
title: "[CMD] 60. icacls - 파일·디렉터리 ACL 관리"
description: "icacls로 파일·디렉터리의 접근 제어 목록(DACL)을 표시·부여·거부·백업·복원하는 법과 F·M·RX 등 기본 권한 마스크, 상속 옵션(OI·CI·IO), /grant:r로 기존 권한을 대체하는 차이를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 600
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
- icacls
- ACL
- Permission
- Security(보안)
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Education(교육)
- CLI
- NTFS
- Configuration(설정)
- Beginner
- Workflow(워크플로우)
- Productivity(생산성)
image: "wordcloud.png"
---

icacls는 지정한 파일에 대한 임의 접근 제어 목록(DACL)을 표시하거나 수정하고, 저장해 둔 DACL을 지정한 디렉터리의 파일에 적용하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [59장: shutdown](/post/cmd/shutdown-command-restart-shutdown-windows-cmd/)에서 시스템 생명주기를 다룬 뒤 이어지며, Part 6의 나머지 세 장(60–62장)은 "누가 무엇에 접근할 수 있는가"라는 권한 관리로 초점이 옮겨간다. 21장(attrib)에서 다룬 읽기 전용·숨김 같은 단순 속성과 달리, 이 장의 ACL은 사용자·그룹 단위로 세분화된 권한 목록이다.

**이 장의 깊이**: 고급.

## 사용법

```
icacls <이름> [/grant[:r] <SID>:<권한>[...]] [/deny <SID>:<권한> [...]] [/remove[:g|:d] <SID>[...]] [/t] [/c] [/l] [/q]
icacls <이름> [/save <ACL파일>] [/setowner <사용자>] [/verify] [/reset]
icacls <디렉터리> [/restore <ACL파일>] [/substitute <이전SID> <새SID> [...]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/t` | 현재 디렉터리와 모든 하위 디렉터리·파일에 적용 |
| `/c` | 파일 오류가 나도 계속 진행 |
| `/l` | 심볼릭 링크 자체에 적용(대상이 아니라) |
| `/save <파일>` | 일치하는 파일들의 DACL을 파일로 저장 |
| `/restore <파일>` | 저장된 DACL을 디렉터리의 파일들에 다시 적용 |
| `/setowner <사용자>` | 소유자를 지정한 사용자로 변경 |
| `/grant[:r] <SID>:<권한>` | 권한 부여. `:r` 없으면 기존 명시적 권한에 추가, `:r`이면 대체 |
| `/deny <SID>:<권한>` | 명시적 거부 ACE 추가(같은 권한의 명시적 허용은 제거) |
| `/remove[:g\|:d] <SID>` | ACE 제거. `g`는 부여된 권한만, `d`는 거부된 권한만 |
| `/reset` | 상속된 기본 ACL로 초기화 |

### 기본 권한 마스크

| 마스크 | 의미 |
|---|---|
| `N` | 접근 없음 |
| `F` | 완전 접근 |
| `M` | 수정 |
| `RX` | 읽기 및 실행 |
| `R` | 읽기 전용 |
| `W` | 쓰기 전용 |
| `D` | 삭제 |

### 상속 옵션(괄호로 표기, 디렉터리에만 적용)

| 표기 | 의미 |
|---|---|
| `(I)` | 상위 컨테이너로부터 상속됨 |
| `(OI)` | 개체 상속(이 디렉터리 안의 파일에 상속) |
| `(CI)` | 컨테이너 상속(하위 디렉터리에 상속) |
| `(IO)` | 상속 전용(이 개체 자신에는 적용 안 됨) |
| `(NP)` | 전파 안 함(중첩된 하위 컨테이너까지는 전파 안 됨) |

## 예시

```
icacls myfile.txt
icacls C:\Data /grant Users:RX /t
icacls C:\Data /grant "User:(OI)(CI)F"
icacls folder /save aclbackup.txt
icacls folder /restore aclbackup.txt
icacls c:\windows\* /save aclfile /t
icacls test1 /grant User1:(d,wdac)
icacls "myDirectory" /setintegritylevel (CI)(OI)H
```

## 주의사항·함정

**`/grant`와 `/grant:r`는 결과가 다르다**: `:r`을 붙이지 않으면 새 권한이 기존에 명시적으로 부여된 권한에 더해지지만, `:r`을 붙이면 그 사용자의 기존 명시적 권한을 완전히 대체한다. 이전에 부여했던 권한을 유지한 채 추가만 하고 싶은지, 아니면 처음부터 다시 정의하고 싶은지에 따라 선택이 갈린다 — 실수로 `:r`을 붙이면 의도치 않게 이전 권한이 사라질 수 있다.

**ACE는 항상 정해진 순서로 정렬된다**: icacls는 다음 순서를 유지한다 — 명시적 거부, 명시적 허용, 상속된 거부, 상속된 허용.

> "This command preserves the canonical order of ACE entries as: Explicit denials, Explicit grants, Inherited denials, Inherited grants." — Microsoft Learn, "icacls"

즉 명시적 거부가 있으면 그보다 뒤에 오는 어떤 허용(상속된 허용이든 명시적 허용이든)보다 항상 우선한다. 특정 사용자에게 접근을 완전히 막고 싶다면 `/deny`가 다른 어떤 `/grant`보다 확실한 이유가 여기 있다.

**cacls를 대체한다**: icacls는 61장에서 다룰 레거시 cacls 명령을 대체하는 도구로 공식 문서에도 명시되어 있다. 상속·고급 권한·백업/복원 같은 기능이 cacls에는 없다.

**시스템 디렉터리의 ACL을 바꾸기 전에는 백업이 먼저다**: `/save`로 현재 상태를 미리 저장해두면, `/restore`로 언제든 되돌릴 수 있다. 중요한 폴더의 권한을 바꾸기 전에 이 습관을 들이면 실수를 되돌릴 방법을 남겨둘 수 있다.

**`/reset`은 되돌릴 수 없다**: `/reset`은 파일·디렉터리의 ACL을 상위 컨테이너로부터 상속된 기본 권한으로 초기화하는데, 이 과정에서 그동안 명시적으로 추가해 둔 커스텀(비상속) 권한 항목은 모두 사라진다. 되돌리기 기능은 없으므로, 실행 전에 `icacls file /save`로 현재 ACL을 백업해 두지 않았다면 원래 권한 구성을 복원할 방법이 없다.

**PowerShell 등가는 `Get-Acl`/`Set-Acl`이다**: icacls의 플랫 문자열 문법과 달리 PowerShell은 ACL을 객체로 다룬다 — `Get-Acl`로 `FileSystemSecurity` 객체를 가져와 접근 규칙을 추가·제거한 뒤 `Set-Acl`로 다시 적용하는 식이다. 객체 기반이라 스크립트에서 조건부로 권한을 조작하기는 더 강력하지만, icacls의 `/grant SID:F` 같은 한 줄짜리 문법에 비해 학습 곡선이 가파르고 코드도 길어진다.

## 흔한 오개념

<strong>"`/reset`은 단순히 기본값으로 되돌리는 안전한 명령이다"</strong>는 오해가 있다. 실제로는 상위 컨테이너에서 상속되지 않은 모든 커스텀 권한 항목을 영구히 제거하는 파괴적인 작업이며, 사전에 `/save`로 백업해두지 않았다면 그 권한 구성을 다시 만들어낼 방법이 없다.

## 다음 장에서는

다음은 61장 — icacls가 대체한 레거시 명령 `cacls`를 다룬다.

## 평가 기준

- icacls로 파일·디렉터리의 ACL을 조회·부여·거부·백업·복원할 수 있다.
- `/grant`와 `/grant:r`의 차이(추가 vs 대체)를 설명할 수 있다.
- ACE의 정렬 순서(명시적 거부 > 명시적 허용 > 상속된 거부 > 상속된 허용)를 설명할 수 있다.
- icacls가 cacls를 대체하는 이유를 안다.

## 참고

- [icacls | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
