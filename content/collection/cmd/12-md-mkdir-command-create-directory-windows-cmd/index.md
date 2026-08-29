---
draft: false
slug: md-mkdir-command-create-directory-windows-cmd
title: "[CMD] 12. md, mkdir - 디렉터리 생성"
description: "md(mkdir) 명령으로 새 디렉터리를 만드는 법과, 명령 확장이 켜져 있을 때 중간 경로가 없어도 한 번에 다단계 디렉터리 트리를 만드는 동작, 확장이 꺼졌을 때 필요한 단계별 생성 방식을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 120
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
- md
- mkdir
- 디렉터리생성
- File-System
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Comparison(비교)
- Command-Extensions
- Linux(리눅스)
- Education(교육)
- Batch
- CLI
- Troubleshooting(트러블슈팅)
- Configuration(설정)
image: "wordcloud.png"
---

md(또는 mkdir)는 새 디렉터리(폴더)를 만드는 내장 명령이다. 두 이름은 완전히 동일한 명령을 가리킨다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [11장: pushd, popd](/post/cmd/pushd-popd-command-directory-stack-windows-cmd/)로 Part 1(CMD 기초와 탐색)을 마친 뒤 이어지며, <strong>Part 2(파일과 디렉터리 조작)</strong>의 첫 장이다. Part 1이 이미 존재하는 디렉터리를 오가는 법이었다면, Part 2는 그 대상 자체를 만들고 지우고 옮기는 법을 다룬다.

**이 장의 깊이**: 입문. **다루지 않는 것**: 만든 디렉터리를 지우는 것은 13장(rmdir)에서 다룬다.

## 사용법

```
mkdir [<드라이브>:]<경로>
md [<드라이브>:]<경로>
```

## 옵션

md/mkdir는 별도 스위치 없이 경로 하나만 받는다.

## 예시

```
md NewFolder
md D:\Projects\2026\January
mkdir "Folder With Spaces"
mkdir \Taxes\Property\Current
```

## 주의사항·함정

**명령 확장 여부에 따라 다단계 생성이 갈린다**: 01장에서 다룬 명령 확장이 켜져 있으면(기본값) 중간 경로가 존재하지 않아도 `mkdir \Taxes\Property\Current` 한 줄로 `Taxes`, `Taxes\Property`, `Taxes\Property\Current`를 한 번에 만든다.

> "Command extensions, which are enabled by default, allow you to use a single **mkdir** command to create intermediate directories in a specified path." — Microsoft Learn, "mkdir"

명령 확장이 꺼져 있으면 이 동작이 사라지고, 같은 결과를 얻으려면 `md \Taxes`, `md \Taxes\Property`, `md \Taxes\Property\Current`를 순서대로 실행해야 한다. 명령 확장이 꺼진 환경(예: 오래된 배치 스크립트가 `cmd /e:off`로 명시적으로 확장을 끈 경우)에서 다단계 `mkdir` 한 줄이 실패한다면 이 차이를 의심해야 한다.

**이미 있는 이름과 충돌하면 오류**: 같은 이름의 디렉터리(또는 파일)가 이미 있으면 오류가 나고 아무 것도 만들어지지 않는다. 배치 스크립트에서 반복 실행해도 안전하게 만들려면, 먼저 대상이 있는지 확인(`if not exist`, 4부에서 다룬다)한 뒤 md를 실행하는 패턴을 쓴다.

**공백이 있는 경로**: 공백이 포함된 경로는 따옴표로 감싼다(`mkdir "Folder With Spaces"`).

**PowerShell에서는 `New-Item`으로 같은 동작을 얻는다**: PowerShell의 대응 명령은 `New-Item -ItemType Directory -Path "..." -Force`다. 여기서 `-Force`는 단순히 "이미 있어도 오류 없이 넘어간다"는 뜻에 그치지 않고, 지정한 경로의 중간 부모 디렉터리가 없어도 함께 만들어준다는 점에서 md의 명령 확장 기반 다단계 생성과 결과가 비슷하다. 다만 md는 확장이 켜져 있으면 스위치 없이 기본 동작으로 이 일을 하는 반면, `New-Item`은 `-Force`를 명시적으로 붙여야 한다는 차이가 있으므로 배치 스크립트를 PowerShell로 옮길 때 이 플래그를 빠뜨리지 않아야 한다.

## 흔한 오개념

<strong>"mkdir -p처럼 중간 경로를 항상 자동으로 만들어준다"</strong>는 오해가 있다. 유닉스 `mkdir -p`에 해당하는 동작은 CMD에서 별도 스위치 없이 명령 확장이 켜져 있을 때만 자동으로 적용되는 기본 동작이라는 점이 다르다. 확장이 꺼진 환경까지 고려한 이식성 있는 배치 스크립트를 짜야 한다면, 이 기본 동작에 기대지 않고 단계별로 만드는 편이 안전하다.

## 다음 장에서는

다음은 13장 — md로 만든 디렉터리를 지우는 `rmdir`(`rd`) 명령을 다룬다.

## 평가 기준

- md와 mkdir가 동일한 명령이라는 것을 안다.
- 명령 확장이 켜져 있을 때와 꺼져 있을 때 다단계 디렉터리 생성이 어떻게 다른지 설명할 수 있다.
- 이미 존재하는 이름과 충돌할 때의 동작과, 배치 스크립트에서 안전하게 재실행하는 패턴의 필요성을 안다.

## 참고

- [mkdir | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mkdir)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
