---
draft: false
slug: replace-command-replace-files-windows-cmd
title: "[CMD] 25. replace - 대상 디렉터리의 파일 교체"
description: "replace로 대상 디렉터리의 기존 파일을 원본으로 교체하거나 /a로 없는 파일만 추가하는 법과, /a와 /s·/u를 함께 쓸 수 없는 상호배타 규칙, 숨김·시스템 파일은 갱신할 수 없는 제약을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 250
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
- replace
- 파일교체
- File-System
- ERRORLEVEL
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Deployment(배포)
- Legacy
- CLI
- Batch
- Comparison(비교)
- Configuration(설정)
- Beginner
image: "wordcloud.png"
---

replace는 원본 디렉터리의 파일로 대상 디렉터리에 있는 같은 이름의 파일을 교체하거나, `/a`를 쓰면 대상에 없는 파일만 새로 추가하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [24장: mklink](/post/cmd/mklink-command-symbolic-hard-links-windows-cmd/)에서 링크를 만드는 법을 다룬 뒤 이어지며, Part 2(파일과 디렉터리 조작)의 마지막 장이다. 14–17장(copy·xcopy·robocopy·move)이 "원본을 그대로 옮기거나 복사"하는 명령이었다면, replace는 "대상의 기존 상태를 조건부로 교체·보완"한다는 점에서 더 정교한 배포 시나리오에 쓰인다.

**이 장의 깊이**: 중급. 오래된 명령이라 최신 자동화에서는 robocopy로 대체되는 경우가 많지만, 레거시 배포 스크립트를 유지 보수할 때 여전히 마주칠 수 있다.

## 사용법

```
replace [<드라이브1>:][<경로1>]<파일이름> [<드라이브2>:][<경로2>] [/a] [/p] [/r] [/w]
replace [<드라이브1>:][<경로1>]<파일이름> [<드라이브2>:][<경로2>] [/p] [/r] [/s] [/w] [/u]
```

두 문법이 나뉘어 있는 것은 `/a`와 `/s`·`/u`가 함께 쓰일 수 없기 때문이다.

## 옵션

| 옵션 | 설명 |
|---|---|
| `/a` | 대상에 없는 파일만 추가(기존 파일 교체는 하지 않음). `/s`, `/u`와 함께 쓸 수 없음 |
| `/p` | 각 파일을 교체·추가하기 전에 확인 |
| `/r` | 읽기 전용 파일도 교체(지정하지 않으면 오류로 중단) |
| `/s` | 대상 디렉터리의 하위 디렉터리까지 검색해 일치하는 파일 교체(원본 쪽 하위 디렉터리는 검색하지 않음). `/a`와 함께 쓸 수 없음 |
| `/u` | 대상보다 원본이 더 최신인 파일만 갱신. `/a`와 함께 쓸 수 없음 |
| `/w` | 원본 파일을 찾기 전에 디스크 삽입을 기다림 |

## 예시

```
replace C:\New\*.* D:\Old\ /s /u
replace C:\Src\*.dll D:\App\ /a
replace C:\Patch\*.* D:\Target\ /s /p
replace a:\phones.cli c:\ /s
```

## 주의사항·함정

**`/a`는 `/s`·`/u`와 함께 쓸 수 없다**: Microsoft Learn은 이 상호배타 관계를 명시적으로 규정한다.

> "You can't use this command-line option with the **/s** or **/u** command-line option." — Microsoft Learn, "replace"(`/a` 설명 중)

"없는 파일만 추가"하는 모드(`/a`)와 "하위 디렉터리까지 검색"·"최신 파일만 갱신"하는 모드(`/s`, `/u`)는 replace 안에서 서로 다른 두 가지 사용 방식으로 나뉘어 있어, 옵션을 섞어 쓰면 오류가 난다. 위 사용법 블록에 두 문법이 따로 적힌 이유가 여기에 있다.

**읽기 전용 파일은 `/r` 없이 교체할 수 없다**: 대상 파일이 읽기 전용이면 `/r`을 명시하지 않는 한 오류가 나고 그 파일의 교체가 중단된다. 21장(attrib)에서 다룬 읽기 전용 속성이 여기서도 그대로 영향을 준다.

**숨김·시스템 파일은 갱신할 수 없다**: Microsoft Learn은 replace로 숨김 파일이나 시스템 파일을 업데이트할 수 없다고 명시한다. 이런 파일을 교체 대상으로 삼으려면 attrib로 속성을 먼저 해제해야 한다.

**종료 코드로 배치 스크립트에서 원인을 구분한다**: replace는 세분화된 종료 코드를 반환한다.

| 종료 코드 | 의미 |
|---|---|
| 0 | 성공적으로 교체·추가함 |
| 2 | 원본 파일을 찾지 못함 |
| 3 | 원본 또는 대상 경로를 찾지 못함 |
| 5 | 접근 권한 없음 |
| 8 | 시스템 메모리 부족 |
| 11 | 명령줄 구문 오류 |

15장(xcopy)에서 이미 익힌 것처럼, 배치 파일에서 `if errorlevel`로 이 코드를 검사해 실패 유형별로 대응할 수 있다.

**PowerShell에는 replace에 대응하는 단일 cmdlet이 없다**: "교체만 하고 없으면 추가하지 않음"(기본 모드)과 "없는 파일만 추가"(`/a`)를 나누는 replace 특유의 의미론을 그대로 옮겨주는 cmdlet은 PowerShell에 없다. 같은 동작이 필요하다면 `Test-Path`로 대상 파일 존재 여부를 확인한 뒤 `Copy-Item`을 호출하는 스크립트를 직접 구성해야 하며, 실무에서는 이렇게 손으로 조합하기보다 파일 최신성 비교까지 이미 갖춘 robocopy(16장)를 그대로 쓰는 경우가 더 많다.

## 흔한 오개념

<strong>"옵션 없이 replace를 실행하면 대상에 없는 파일도 알아서 추가해준다"</strong>는 오해가 있다. 실제로는 정반대다. 옵션 없는 기본 동작은 "대상에 이미 존재하는 파일만 교체"이며, 대상에 없는 파일은 조용히 건너뛸 뿐 추가되지 않는다. 원본 디렉터리의 새 파일까지 대상에 채워 넣고 싶다면 반드시 `/a`를 명시해야 하고, 이때는 반대로 기존 파일 교체가 되지 않는다는 점(위 상호배타 규칙)도 함께 기억해야 한다.

## 다음 장에서는

다음은 26장 — 파일이나 출력에서 문자열을 찾는 `find` 명령으로 Part 3(텍스트 검색과 출력 제어)이 시작된다.

## 평가 기준

- replace로 기존 파일을 교체하는 것과 `/a`로 없는 파일만 추가하는 것의 차이를 설명할 수 있다.
- `/a`가 `/s`·`/u`와 함께 쓰일 수 없는 이유를 설명할 수 있다.
- 읽기 전용·숨김·시스템 파일을 replace로 다룰 때의 제약을 안다.
- replace의 종료 코드로 배치 스크립트에서 실패 원인을 구분할 수 있다.

## 참고

- [replace | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/replace)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
