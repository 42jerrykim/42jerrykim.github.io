---
draft: false
slug: label-command-volume-label-windows-cmd
title: "[CMD] 49. label - 볼륨 레이블 만들기와 삭제"
description: "label로 드라이브의 볼륨 이름을 만들고 바꾸고 삭제하는 법과 NTFS 32자·대소문자 유지 규칙, 인수 없이 실행했을 때 대화형으로 레이블을 지우는 절차를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 490
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
- label
- 볼륨레이블
- NTFS
- File-System
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Education(교육)
- CLI
- Comparison(비교)
- Configuration(설정)
- Advanced
- Administration
- Productivity(생산성)
- Workflow(워크플로우)
image: "wordcloud.png"
---

label은 디스크의 볼륨 레이블(이름)을 만들거나 바꾸거나 삭제하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [48장: fsutil](/post/cmd/fsutil-command-file-system-utility-windows-cmd/)에서 저수준 파일 시스템 조작을 다룬 뒤 이어진다. 이 장부터 49–51장(label, vol, subst)은 다시 가벼운 난이도로 돌아와, 볼륨을 사람이 알아보기 쉽게 다루는 편의 명령들을 짧게 묶어 다룬다.

**이 장의 깊이**: 입문. **다루지 않는 것**: 레이블을 직접 바꾸지 않고 조회만 하는 것은 50장(vol)에서 다룬다.

## 사용법

```
label [/mp] [<볼륨>] [<레이블>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/mp` | 대상을 마운트 지점 또는 볼륨 이름으로 취급 |
| `<볼륨>` | 드라이브 문자·마운트 지점·볼륨 이름 |
| `<레이블>` | 설정할 레이블 문자열 |

인수 없이 `label`만 실행하면 현재 레이블을 표시하고 새 레이블을 입력하도록 요청한다.

## 예시

```
label a:sales-july
label D: MyData
label
```

인수 없이 실행했을 때의 흐름은 다음과 같다.

```
Volume in drive C: is Main Disk
Volume Serial Number is 6789-ABCD
Volume label (32 characters, ENTER for none)?
```

여기서 그냥 Enter를 누르면 다음 확인이 뜬다.

```
Delete current volume label (Y/N)?
```

Y를 누르면 레이블이 삭제되고, N을 누르면 기존 레이블이 그대로 유지된다.

## 주의사항·함정

**NTFS 레이블은 최대 32자, 대소문자를 그대로 유지한다**: NTFS 볼륨 레이블은 공백을 포함해 최대 32자까지 쓸 수 있고, 입력한 대소문자 그대로 표시된다.

> "An NTFS volume label can be up to 32 characters in length, including spaces. NTFS volume labels retain and display the case that was used when the label was created." — Microsoft Learn, "label"

FAT32처럼 오래된 파일 시스템은 이보다 짧은 제한(보통 11자)을 갖고 대소문자를 자동으로 대문자로 바꾸는 경우가 많아, 같은 명령이라도 파일 시스템에 따라 결과가 달라질 수 있다.

**레이블을 지우는 방법은 두 가지가 있다**: 인수 없이 실행한 뒤 대화형으로 Enter → Y를 누르는 방법과, `label 볼륨: ""`처럼 빈 문자열을 직접 넘기는 방법이다(스크립트에서는 후자가 더 실용적이다).

**시스템 드라이브도 레이블을 바꿀 수 있다**: 볼륨 레이블은 파일 시스템 자체를 건드리는 작업이 아니라 단순한 이름표이므로, C: 드라이브처럼 시스템이 사용 중인 볼륨이라도 레이블 변경 자체에는 특별한 위험이나 재부팅 예약이 필요 없다.

**PowerShell 대응 cmdlet은 `Get-Volume`과 `Set-Volume`이다**: 레이블을 조회할 때는 `Get-Volume`으로 `FileSystemLabel` 속성을 확인하고, 변경할 때는 `Set-Volume -NewFileSystemLabel`을 쓴다. label처럼 인수 없이 실행했을 때 대화형으로 삭제 여부를 묻는 흐름은 없고, `Set-Volume -NewFileSystemLabel ""`처럼 빈 문자열을 직접 넘겨야 레이블이 지워진다는 점이 다르다.

## 흔한 오개념

<strong>"볼륨 레이블의 32자 제한은 모든 파일 시스템에 동일하게 적용된다"</strong>는 오해가 있다. NTFS는 공백을 포함해 최대 32자를 허용하고 입력한 대소문자를 그대로 유지하지만, FAT32처럼 오래된 파일 시스템은 보통 11자까지만 허용하고 대소문자를 자동으로 대문자로 바꾼다. 같은 `label` 명령을 실행해도 대상 드라이브의 파일 시스템에 따라 실제로 저장되는 레이블의 길이와 표기가 달라질 수 있다.

## 다음 장에서는

다음은 50장 — 레이블을 바꾸지 않고 현재 값만 조회하는 `vol` 명령을 다룬다.

## 평가 기준

- label로 볼륨 레이블을 설정·변경·삭제할 수 있다.
- NTFS 레이블의 32자 제한과 대소문자 유지 규칙을 설명할 수 있다.
- 인수 없이 label을 실행했을 때의 대화형 삭제 흐름을 재현할 수 있다.

## 참고

- [label | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/label)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
