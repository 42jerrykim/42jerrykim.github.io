---
draft: false
slug: del-erase-command-delete-files-windows-cmd
title: "[CMD] 18. del, erase - 파일 삭제"
description: "del(erase)로 파일을 삭제하는 법과 복구할 수 없다는 경고, /a 속성 필터, 와일드카드가 8.3 짧은 이름까지 매칭해 의도치 않은 파일까지 지우는 함정을 09장의 dir 사례와 이어서 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 180
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
- del
- erase
- 파일삭제
- File-System
- Wildcard
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- PowerShell
- Linux(리눅스)
- Education(교육)
- CLI
- Comparison(비교)
- Configuration(설정)
image: "wordcloud.png"
---

del(또는 erase)은 하나 이상의 파일을 삭제하는 내장 명령이다. 두 이름은 완전히 같은 동작을 한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [17장: move](/post/cmd/move-command-move-files-directories-windows-cmd/)에서 파일을 옮기는 법을 다룬 뒤 이어진다. move·copy가 파일을 보존하며 다루는 명령이었다면, del은 파일을 되돌릴 수 없이 없애는 첫 명령이다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 디렉터리를 지우는 것은 13장(rmdir)에서 이미 다뤘다. 이 장은 파일 삭제에만 집중한다.

## 사용법

```
del [/p] [/f] [/s] [/q] [/a[:]<속성>] <이름들>
erase [/p] [/f] [/s] [/q] [/a[:]<속성>] <이름들>
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/p` | 각 파일 삭제 전에 확인 메시지 표시 |
| `/f` | 읽기 전용 파일도 강제로 삭제 |
| `/s` | 현재 디렉터리와 모든 하위 디렉터리에서 지정한 파일을 삭제하며, 삭제되는 이름을 표시 |
| `/q` | 조용한 모드. 삭제 확인을 묻지 않음 |
| `/a[:]<속성>` | 지정한 속성을 가진 파일만 삭제. r(읽기전용) h(숨김) i(색인제외) s(시스템) a(보관대상) l(재구문분석지점). `-` 접두어로 "아님"을 표시 |

## 예시

```
del c:\test
del c:\test\*.*
del "c:\test folder\*.*"
del *.bat
del /a:r *.*
del /s /q "*abc*.txt"
```

## 주의사항·함정

**복구할 수 없다**: Microsoft Learn은 이 페이지 최상단에 경고를 별도로 둘 만큼 이 점을 강조한다.

> "If you use **del** to delete a file from your disk, you can't retrieve it." — Microsoft Learn, "del"

휴지통을 거치는 탐색기 삭제와 달리, del로 지운 파일은 즉시 사라진다. 되돌릴 방법이 없다는 전제 위에서 아래 두 가지 안전장치를 항상 습관화해야 한다.

**`*.*`를 지우려 하면 CMD가 한 번 더 확인한다**: 모든 파일을 지우는 패턴에는 CMD 자체가 추가 확인을 넣어 둔다.

> "Are you sure (Y/N)?" — Microsoft Learn, "del"

이 확인은 `*.*` 패턴에만 발동하는 특별 처리이지, 다른 와일드카드 패턴(`*.txt` 등)에는 적용되지 않는다는 점에 유의해야 한다. `/q`를 함께 쓰면 이 확인마저 생략되므로, 배치 스크립트에서 `/s /q`를 조합할 때는 대상 경로를 다시 한번 검토하는 것이 안전하다.

**와일드카드는 09장(dir)에서 본 8.3 짧은 이름 매칭 함정을 그대로 물려받는다**: 09장에서 `dir t97*`가 `t.txt2`와 `t97.txt` 두 파일을 함께 찾아낸 이유를 다뤘다 — `*` 와일드카드가 파일의 8.3 형식 짧은 이름까지 매칭 대상으로 삼기 때문이다. Microsoft Learn은 del을 실행하기 전에 반드시 같은 패턴으로 dir을 먼저 실행해 볼 것을 권장한다.

> "Before you use wildcard characters with the **del** command, use the same wildcard characters with the **dir** command to list all the files that will be deleted." — Microsoft Learn, "del"

즉 `del t97\*`을 실행하기 전에 `dir t97\*`을 먼저 실행해 어떤 파일이 실제로 매칭되는지 확인하는 절차가, 복구 불가능한 del 명령에서는 선택이 아니라 사실상 필수 습관이다.

**명령 확장을 끄면 `/s`의 출력이 바뀐다**: 13장(rmdir)에서 본 것과 같은 패턴이다. 명령 확장이 꺼져 있으면 `/s`는 삭제된 파일이 아니라 찾지 못한 파일의 이름을 표시하는 것으로 바뀐다.

## 흔한 오개념

<strong>"del과 erase는 옵션이 조금 다른 별개 명령이다"</strong>는 오해가 있다. 이름만 다를 뿐 완전히 같은 명령이며 옵션·동작에 차이가 전혀 없다. Microsoft Learn 문서도 두 이름을 한 페이지, 같은 문법 블록으로 함께 설명한다.

<strong>"PowerShell의 del은 CMD의 del과 똑같이 동작한다"</strong>는 오해도 흔하다. PowerShell에서 `del`은 `Remove-Item` cmdlet의 별칭일 뿐이라 이름은 같아도 실제 구현과 옵션 문법이 다르다. CMD 전용 스위치(`/a:r`, `/s /q` 등)를 PowerShell의 `del`에 그대로 넘기면 인식되지 않는다.

## 다음 장에서는

다음은 19장 — 이동 없이 파일·디렉터리 이름만 바꾸는 `ren`(`rename`) 명령을 다룬다.

## 평가 기준

- del과 erase가 동일한 명령이라는 것을 안다.
- 삭제가 복구 불가능하다는 것과, `*.*` 패턴에 대한 CMD의 추가 확인이 언제 발동하고 언제 생략되는지 설명할 수 있다.
- 와일드카드의 8.3 짧은 이름 매칭 함정을 알고, 삭제 전 `dir`로 대상을 먼저 확인하는 습관의 필요성을 설명할 수 있다.
- CMD의 del과 PowerShell의 `del`(Remove-Item 별칭)이 다른 구현이라는 것을 안다.

## 참고

- [del | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/del)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
