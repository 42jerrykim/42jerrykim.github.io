---
draft: false
slug: assoc-command-file-extension-association-windows-cmd
title: "[CMD] 81. assoc - 파일 확장명 연결 표시·수정"
description: "assoc로 파일 확장명과 파일 형식의 연결을 조회·설정·제거하는 법과 ftype과의 역할 분담, PowerShell에서 직접 지원되지 않아 cmd /c로 우회해야 하는 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 810
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
- assoc
- 파일연결
- File-System
- Comparison(비교)
- PowerShell
- Troubleshooting(트러블슈팅)
- Documentation(문서화)
- Best-Practices
- Administration
- Education(교육)
- CLI
- Configuration(설정)
- Registry(레지스트리)
- Workflow(워크플로우)
- Productivity(생산성)
image: "wordcloud.png"
---

assoc는 파일 확장명과 파일 형식의 연결을 표시하거나 수정하는 내장 명령으로, Part 9(부팅 구성과 기타 유틸리티)에서 부팅 관련 명령 이후 다루는 첫 "기타 유틸리티"다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [80장: bcdedit](/post/cmd/bcdedit-command-boot-configuration-editor-windows-cmd/)로 부팅 구성 관련 명령을 마친 뒤 이어진다. 여기서부터는 부팅과 무관하게, CMD 전반에 남아 있지만 어느 Part에도 딱 들어맞지 않는 명령들을 다룬다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 확장명이 가리키는 파일 형식이 실제로 어떤 프로그램으로 열릴지는 82장(ftype)에서 다룬다. assoc는 "확장명 ↔ 형식 이름"의 연결만 관리하고, "형식 이름 ↔ 실행 명령"의 연결은 ftype이 관리한다.

## 개요 + 정신 모델

Windows의 파일 열기 메커니즘은 두 단계로 나뉜다. assoc는 그중 첫 단계, 즉 <strong>확장명(.txt)을 파일 형식 이름(txtfile)에 연결하는 계층</strong>만 다룬다.

> "Displays or modifies file name extension associations. If used without parameters, **assoc** displays a list of all the current file name extension associations." — Microsoft Learn, "assoc"

인수 없이 `assoc`만 실행하면 시스템에 등록된 모든 확장명-형식 연결이 나열된다. 특정 확장명 하나의 연결만 보려면 `assoc .txt`처럼 확장명만 인수로 준다. 연결을 바꾸려면 `.확장명=형식이름`처럼 등호로 대입한다.

## 사용법

```
assoc [<.확장명>[=[<파일형식>]]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `<.확장명>` | 조회·수정할 파일 확장명 |
| `<파일형식>` | 해당 확장명에 연결할 파일 형식 이름 |
| (인수 없음) | 현재 등록된 모든 확장명-형식 연결 목록 표시 |

## 예시

```
assoc
assoc .txt
assoc .log=txtfile
assoc .bak=
assoc .=txtfile
assoc | more
assoc>assoc.txt
```

## 주의사항·함정

**PowerShell에서 직접 지원되지 않는다**: assoc는 cmd.exe 안에서만 동작하는 내장 명령이다.

> "This command is only supported within cmd.exe and is not available from PowerShell. Though you can use `cmd /c assoc` as a workaround." — Microsoft Learn, "assoc"

PowerShell 스크립트 안에서 확장명 연결을 확인해야 한다면 `cmd /c assoc`처럼 하위 CMD 프로세스를 통해 우회 호출해야 한다 — PowerShell 고유의 `New-ItemProperty` 등 레지스트리 직접 조작으로 대체하는 방법도 있지만, 간단한 조회라면 우회 호출이 더 빠르다.

**연결을 제거하려면 등호 뒤에 공백을 넣어야 한다**: `.bak=`처럼 등호 뒤에 아무것도 쓰지 않으면 해당 확장명의 연결이 제거된다.

> "To remove the file type association for a file name extension, add a white space after the equal sign by pressing the SPACEBAR." — Microsoft Learn, "assoc"

이 규칙을 놓치고 등호만 입력하면 명령이 예상과 다르게 동작할 수 있어, 스크립트로 자동화할 때 특히 주의가 필요하다.

**변경에는 관리자 권한이 필요하다**: 조회는 일반 권한으로 가능하지만, 연결을 바꾸거나 제거하려면 관리자 권한이 필요하다. 시스템 전역 연결을 실수로 바꾸면 특정 확장명 파일을 더블클릭했을 때 엉뚱한 프로그램이 열리게 되므로, 변경 전에 `assoc .확장명`으로 기존 값을 기록해 두는 것이 안전하다.

## 흔한 오개념

<strong>"assoc로 연결을 바꾸면 현재 로그인한 사용자의 탐색기 더블클릭 동작도 즉시, 무조건 바뀐다"</strong>는 오해가 흔하다. 최신 Windows에서는 "기본 앱"·"연결 프로그램" 설정이 사용자별로 훨씬 복잡한 방식(UserChoice 레지스트리 해시 포함)으로 저장되며, 이 설정이 assoc·ftype 같은 레거시 명령으로 만든 변경을 무시하거나 덮어쓸 수 있다. 그래서 명령줄에서 `assoc`가 연결이 바뀌었다고 보고해도, 실제로 파일 탐색기에서 그 확장명 파일을 더블클릭하면 여전히 예전에 연결되어 있던 프로그램이 열리는 경우가 흔하다.

## 다음 장에서는

다음은 82장 — 파일 형식이 실제로 어떤 명령으로 열리는지를 정의하는 `ftype` 명령을 다룬다.

## 평가 기준

- assoc로 확장명-형식 연결을 조회하고, `.확장명=형식` 문법으로 새 연결을 설정할 수 있다.
- 등호 뒤 공백으로 연결을 제거하는 규칙을 정확히 적용할 수 있다.
- assoc가 PowerShell에서 직접 지원되지 않아 `cmd /c`로 우회해야 하는 이유를 안다.
- assoc(확장명↔형식)와 ftype(형식↔실행 명령)의 역할 분담을 설명할 수 있다.

## 참고

- [assoc | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/assoc)
- [ftype | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ftype)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
