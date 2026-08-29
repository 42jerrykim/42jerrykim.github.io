---
draft: false
slug: ftype-command-file-type-open-command-windows-cmd
title: "[CMD] 82. ftype - 파일 형식 실행 명령 표시·수정"
description: "ftype으로 파일 형식이 열릴 때 실행할 명령줄을 조회·설정하는 법과 %1·%*같은 치환 변수의 의미, assoc와 조합해 새 확장명에 프로그램을 연결하는 절차를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 820
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
- ftype
- 파일형식
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
- Scripting(스크립팅)
- Automation(자동화)
image: "wordcloud.png"
---

ftype은 파일 형식에 대해 실행할 열기 명령줄을 표시하거나 설정하는 내장 명령으로, 81장(assoc)이 연결한 파일 형식이 실제로 어떤 프로그램으로 열릴지를 결정한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [81장: assoc](/post/cmd/assoc-command-file-extension-association-windows-cmd/)에서 확장명-형식 연결을 다룬 뒤 이어진다. assoc가 "이 확장명이 어느 형식 이름인가"를 정했다면, ftype은 "그 형식 이름이 열릴 때 어느 프로그램을 어떻게 실행하는가"를 정한다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 확장명을 파일 형식 이름에 연결하는 작업 자체는 81장(assoc)이 담당한다; 이 장은 그 형식 이름이 열릴 때 무엇을 실행할지만 다룬다.

## 개요 + 정신 모델

ftype이 다루는 대상은 <strong>열기 명령 문자열(open command string)</strong>이다.

> "Displays or modifies file types that are used in file name extension associations. If used without an assignment operator (=), this command displays the current open command string for the specified file type." — Microsoft Learn, "ftype"

인수 없이 `ftype`만 실행하면 열기 명령이 정의된 모든 파일 형식이 나열된다. 형식 이름 하나만 인수로 주면 그 형식의 현재 열기 명령을 보여준다. `형식이름=명령줄`처럼 등호로 대입하면 새 열기 명령을 설정한다.

## 사용법

```
ftype [<파일형식>[=[<열기명령줄>]]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `<파일형식>` | 조회·수정할 파일 형식 이름(assoc로 확장명과 연결된 이름) |
| `<열기명령줄>` | 해당 형식의 파일을 열 때 실행할 명령줄 |
| (인수 없음) | 열기 명령이 정의된 모든 파일 형식 목록 표시 |

### 열기 명령줄의 치환 변수

| 변수 | 치환 값 |
|---|---|
| `%0` 또는 `%1` | 연결을 통해 실행되는 파일 이름 |
| `%*` | 모든 매개변수 |
| `%2`, `%3`, ... | 첫 번째(`%2`), 두 번째(`%3`) 매개변수 |
| `%~<n>` | n번째 매개변수부터 시작하는 나머지 전체 매개변수(n은 2~9) |

## 예시

```
ftype
ftype txtfile
ftype txtfile=notepad.exe %1
ftype example=
assoc .pl=PerlScript
ftype PerlScript=perl.exe %1 %*
```

## 주의사항·함정

**PowerShell에서 직접 지원되지 않는다**: assoc와 마찬가지로 ftype도 cmd.exe 전용 내장 명령이다.

> "This command is only supported within cmd.exe and is not available from PowerShell. Though you can use `cmd /c ftype` as a workaround." — Microsoft Learn, "ftype"

**assoc와 ftype은 항상 짝으로 움직인다**: 새 확장명에 프로그램을 연결하려면 두 단계가 모두 필요하다. 먼저 `assoc`로 확장명을 형식 이름에 연결하고, 그다음 `ftype`으로 그 형식 이름이 열릴 때 실행할 명령줄을 지정한다. 원문의 Perl 스크립트 예시(`assoc .pl=PerlScript` 뒤 `ftype PerlScript=perl.exe %1 %*`)가 이 2단계 절차를 그대로 보여준다. 한쪽만 설정하면 파일이 열리지 않거나 엉뚱하게 동작한다.

**`PATHEXT`와 조합하면 확장명 생략도 가능하다**: 원문은 `.pl` 확장명을 매번 타이핑하지 않고 Perl 스크립트를 실행하려면 `set PATHEXT=.pl;%PATHEXT%`로 환경 변수를 확장하라고 안내한다. assoc·ftype으로 연결을 만든 뒤 `PATHEXT`에 확장명을 추가하면, `script.pl` 대신 `script`만 입력해도 실행된다 — 07장(path)에서 다룬 실행 파일 검색 경로 개념과 `PATHEXT`가 함께 작동하는 방식이다.

**시스템 기본 형식을 바꾸면 영향 범위가 크다**: `txtfile`, `exefile`처럼 시스템이 기본 제공하는 형식의 열기 명령을 바꾸면 모든 사용자·모든 프로그램에서 그 형식의 동작이 달라진다. 테스트는 새로 만든 사용자 정의 형식(예: 원문의 `PerlScript`)에서 먼저 해보는 것이 안전하다.

## 흔한 오개념

<strong>"ftype으로 열기 명령을 설정하면 그 파일 형식을 실행하는 모든 경로(탐색기 더블클릭, start 명령, 다른 프로그램의 호출)가 똑같이 그 명령을 따른다"</strong>는 오해가 흔하다. 81장(assoc)에서 다룬 것처럼, 최신 Windows 탐색기의 더블클릭 동작은 UserChoice·기본 앱 설정의 영향을 받아 assoc·ftype으로 만든 설정을 무시할 수 있다. 따라서 ftype의 효과는 탐색기 UI보다 명령줄에서(예: `assoc`·`ftype`을 설정한 뒤 CMD 프롬프트에서 확장명 없이 파일 이름만 입력했을 때) 가장 확실하게 확인된다 — 탐색기의 모든 실행 경로를 ftype이 통제한다고 단정해서는 안 된다.

## 다음 장에서는

다음은 83장 — 그래픽 모드에서 확장 문자 세트를 표시하는 레거시 명령 `graftabl`을 다룬다.

## 평가 기준

- ftype으로 파일 형식의 열기 명령줄을 조회하고 `형식=명령줄` 문법으로 설정할 수 있다.
- `%1`·`%*` 같은 치환 변수가 열기 명령줄에서 어떻게 동작하는지 설명할 수 있다.
- assoc와 ftype이 항상 2단계로 함께 쓰여야 새 확장명 연결이 완성된다는 것을 안다.
- `PATHEXT`와 조합해 확장명을 생략하고 실행하는 방법을 안다.

## 참고

- [ftype | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ftype)
- [assoc | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/assoc)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
