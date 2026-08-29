---
draft: false
slug: attrib-command-file-attributes-windows-cmd
title: "[CMD] 21. attrib - 파일 속성 표시와 변경"
description: "attrib로 읽기 전용·숨김·시스템·보관 등 파일 속성을 조회·변경하는 법과, 숨김·시스템 속성은 먼저 해제해야 다른 속성을 바꿀 수 있다는 순서 제약, xcopy가 참조하는 보관 속성의 관계를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 210
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
- attrib
- 파일속성
- File-System
- NTFS
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Comparison(비교)
- Education(교육)
- Batch
- CLI
- Security(보안)
- Configuration(설정)
- Advanced
image: "wordcloud.png"
---

attrib는 파일이나 디렉터리에 부여된 속성(읽기 전용, 숨김, 시스템, 보관 등)을 표시하거나 변경하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [20장: type](/post/cmd/type-command-display-file-contents-windows-cmd/)에서 파일 내용을 들여다보는 법을 다룬 뒤 이어진다. type이 파일의 내용을 다뤘다면, attrib는 내용이 아니라 파일 시스템이 그 파일에 대해 기록하는 메타데이터(속성)를 다룬다. 13장(rmdir)에서 "숨김·시스템 파일 때문에 디렉터리를 못 지운다"는 상황이 나왔을 때 예고했던 명령이 바로 이 장의 attrib다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: NTFS 접근 제어 목록(ACL) 기반의 권한 관리는 6부(icacls)에서 별도로 다룬다. attrib가 다루는 속성은 ACL과 무관한, 훨씬 단순한 파일 시스템 플래그다.

## 사용법

```
attrib [{+|-}r] [{+|-}a] [{+|-}s] [{+|-}h] [{+|-}o] [{+|-}i] [<드라이브>:][<경로>][<파일이름>] [/s [/d] [/l]]
```

인수 없이 `attrib`만 실행하면 현재 디렉터리 모든 파일의 속성을 표시한다.

## 옵션

### 속성

| 속성 | 설명 |
|---|---|
| `+r` / `-r` | 읽기 전용 설정/해제 |
| `+h` / `-h` | 숨김 설정/해제 |
| `+s` / `-s` | 시스템 파일 설정/해제 |
| `+a` / `-a` | 보관(archive) 설정/해제. 마지막 백업 이후 변경된 파일을 표시하며 xcopy가 참조 |
| `+o` / `-o` | 오프라인 설정/해제 |
| `+i` / `-i` | 콘텐츠 색인 제외 설정/해제 |

### 범위

| 옵션 | 설명 |
|---|---|
| `/s` | 현재 디렉터리와 모든 하위 디렉터리의 일치하는 파일에 적용 |
| `/d` | 디렉터리 자체에도 적용 |
| `/l` | 심볼릭 링크가 가리키는 대상이 아니라 링크 자체에 적용 |

## 예시

```
attrib report.txt
attrib +r readme.txt
attrib -h +r *.bak
attrib -r b:\public\*.* /s
attrib +a a:*.* & attrib -a a:*.bak
```

## 주의사항·함정

**숨김·시스템 속성은 먼저 해제해야 다른 속성을 바꿀 수 있다**: Microsoft Learn은 숨김·시스템 속성이 설정된 파일의 경우, 다른 속성을 바꾸기 전에 그 속성부터 먼저 해제해야 한다고 명시한다.

> "Sets (**+**) or clears (**-**) the System file attribute. If a file uses this attribute set, you must clear the attribute before you can change any other attributes for the file." — Microsoft Learn, "attrib"(숨김 속성에도 동일하게 적용)

즉 숨김이면서 읽기 전용인 파일의 읽기 전용만 해제하려 해도, 먼저 `-h`로 숨김을 풀지 않으면 명령이 의도대로 동작하지 않을 수 있다. 13장(rmdir)에서 다룬 "숨김·시스템 파일 때문에 디렉터리를 못 지운다" 상황을 해결하려면 이 순서(먼저 `-h -s`, 그다음 필요한 조작)를 지켜야 한다.

**보관 속성은 xcopy·robocopy의 필터 기준이 된다**: `+a`/`-a`로 다루는 보관(archive) 속성은 "마지막 백업 이후 이 파일이 바뀌었는가"를 나타내는 플래그다. 15장(xcopy)의 `/a`·`/m` 옵션이 바로 이 속성을 기준으로 파일을 골라 복사한다 — `/m`은 복사 후 이 속성을 꺼서 "이미 백업했다"고 표시하지만 `/a`는 속성을 건드리지 않는다는 차이가 있었다. attrib로 이 속성을 직접 조작하면 증분 백업 스크립트의 판단 기준을 사람이 강제로 바꾸는 셈이 된다.

**중요한 시스템 파일의 속성을 함부로 바꾸지 않는다**: 시스템(S)·숨김(H) 속성이 붙은 파일은 대개 운영체제가 의도적으로 보호하고 있는 파일이다. 속성을 해제해 삭제·수정 가능하게 만드는 것은 편집기가 실수로 덮어쓰거나 바이러스 백신이 조용히 처리하는 것을 막던 방어선을 없애는 행위이므로, 무엇을 하려는지 명확할 때만 사용해야 한다.

**PowerShell에는 attrib의 `+r`/`-h` 같은 짧은 스위치 문법이 없다**: PowerShell에서 파일 속성을 확인하려면 `(Get-Item file).Attributes`나 `Get-ItemProperty`를 쓰고, 변경하려면 `Set-ItemProperty -Path file -Name Attributes -Value 'ReadOnly,Hidden'` 또는 `(Get-Item file).Attributes = 'ReadOnly'`처럼 `System.IO.FileAttributes` 열거형 이름을 직접 지정해야 한다. 이 열거형은 attrib가 다루는 R·A·S·H보다 더 세분화된 속성까지 노출하지만, `+r` 한 글자로 끝나던 attrib에 비하면 매번 속성 이름을 정확히 기억해서 써야 하므로 즉흥적으로 치기에는 덜 직관적이다.

## 흔한 오개념

<strong>"attrib +h로 파일을 숨기면 실질적으로 파일을 보호하거나 접근을 막을 수 있다"</strong>는 오해가 있다. 숨김 속성은 순전히 표시상의 필터일 뿐 어떤 접근 제어 메커니즘도 아니다. 파일 탐색기에서 "숨김 항목 표시" 옵션 하나만 켜거나, CMD에서 `dir /a:h`를 실행하면 누구나 그 파일을 곧바로 찾아 열람·수정·삭제할 수 있다. 실제로 접근을 제한하려면 attrib가 아니라 NTFS 권한(ACL)을 다루는 6부의 icacls가 필요하다.

## 다음 장에서는

다음은 22장 — 두 파일을 바이트 단위로 비교하는 `comp` 명령을 다룬다.

## 평가 기준

- attrib로 파일의 읽기 전용·숨김·시스템·보관 속성을 조회·변경할 수 있다.
- 숨김·시스템 속성을 먼저 해제해야 다른 속성을 바꿀 수 있다는 순서 제약을 설명할 수 있다.
- 보관 속성이 xcopy의 `/a`·`/m` 옵션과 어떻게 연결되는지 설명할 수 있다.
- attrib가 다루는 속성과 ACL(6부에서 다룰 icacls)이 서로 다른 메커니즘이라는 것을 안다.

## 참고

- [attrib | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/attrib)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
