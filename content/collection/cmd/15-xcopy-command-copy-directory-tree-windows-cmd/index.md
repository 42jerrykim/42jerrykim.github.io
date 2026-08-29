---
draft: false
slug: xcopy-command-copy-directory-tree-windows-cmd
title: "[CMD] 15. xcopy - 디렉터리 트리 복사"
description: "xcopy로 디렉터리 트리를 통째로 복사하는 법과 /s·/e·/i 옵션의 관계, 배치 스크립트에서 ERRORLEVEL로 처리해야 하는 xcopy 종료 코드 표를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 150
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
- xcopy
- 디렉터리복사
- File-System
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- ERRORLEVEL
- Batch
- Deployment(배포)
- Education(교육)
- CLI
- Comparison(비교)
- Configuration(설정)
- Advanced
image: "wordcloud.png"
---

xcopy는 파일과 디렉터리(하위 디렉터리 포함)를 복사하는 명령이다. 14장의 copy가 개별 파일만 다루는 것과 달리, xcopy는 트리 전체를 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [14장: copy](/post/cmd/copy-command-copy-files-windows-cmd/)에서 개별 파일 복사를 다룬 뒤 이어진다. copy가 다루지 못하는 "디렉터리 트리 전체"가 이 장의 핵심 주제다.

**이 장의 깊이**: 중급. 옵션이 많아 이 장의 분량이 Part 2에서 가장 길다. **다루지 않는 것**: 재시도·미러링처럼 더 견고한 복사가 필요하면 16장(robocopy)에서 다룬다.

## 사용법

```
xcopy <원본> [<대상>] [/w] [/p] [/c] [/v] [/q] [/f] [/l] [/g] [/d[:MM-DD-YYYY]] [/u] [/i] [/s [/e]] [/t] [/k] [/r] [/h] [{/a|/m}] [/n] [/o] [/x] [/exclude:파일1[+파일2]] [{/y|/-y}] [/z]
```

## 옵션

### 범위

| 옵션 | 설명 |
|---|---|
| `/s` | 비어 있지 않은 하위 디렉터리까지 복사(생략하면 한 디렉터리만) |
| `/e` | 빈 하위 디렉터리까지 복사(`/s`, `/t`와 함께 사용) |
| `/t` | 디렉터리 구조(트리)만 복사하고 파일은 복사하지 않음 |
| `/i` | 대상이 없을 때 대상을 디렉터리로 간주해 자동 생성(확인 메시지 생략) |

### 필터

| 옵션 | 설명 |
|---|---|
| `/d[:날짜]` | 지정 날짜 이후 변경된 원본만 복사. 날짜 생략 시 대상보다 새 파일만 복사 |
| `/u` | 대상에 이미 있는 파일만 갱신 |
| `/a` | 보관 속성이 설정된 파일만 복사(속성은 그대로 둠) |
| `/m` | 보관 속성이 설정된 파일만 복사하고, 원본의 보관 속성은 끔 |
| `/h` | 숨김·시스템 파일도 복사(기본은 제외) |
| `/exclude:파일` | 지정한 파일에 나열된 패턴과 일치하면 복사 대상에서 제외 |

### 동작 제어

| 옵션 | 설명 |
|---|---|
| `/y` \| `/-y` | 덮어쓸 때 확인 안 함 \| 확인함 |
| `/k` | 대상 파일의 읽기 전용 속성을 원본과 동일하게 유지(기본은 제거) |
| `/p` | 각 대상 파일 생성 전에 확인 |
| `/l` | 실제로 복사하지 않고 복사될 목록만 출력 |
| `/f` | 복사 중 원본·대상 파일명 출력 |
| `/z` | 네트워크 복사를 재시작 가능 모드로 진행 |

## 예시

```
xcopy a: b: /s /e
xcopy a: b: /s /e /h
xcopy \rawdata \reports /d:12-29-2025
xcopy \rawdata \reports /u
xcopy \rawdata \reports /d:12-29-2025 /l > xcopy.out
xcopy \customer h:\public\address /s /e /k /p /i
```

배치 스크립트에서는 xcopy의 종료 코드를 `if errorlevel`로 검사해 실패 원인을 구분하는 것이 일반적이다.

```bat
@echo off
xcopy %1 %2 /s /e
if errorlevel 4 goto lowmemory
if errorlevel 2 goto abort
if errorlevel 0 goto exit
:lowmemory
echo 메모리 부족 또는 잘못된 드라이브·문법
goto exit
:abort
echo CTRL+C로 복사를 중단함
goto exit
:exit
```

## 주의사항·함정

**대상이 파일인지 디렉터리인지 되묻는다**: 대상 경로가 아직 없고 백슬래시로 끝나지도 않으면, xcopy는 파일로 만들지 디렉터리로 만들지 대화형으로 묻는다.

> "Does `<Destination>` specify a file name or directory name on the target(F = file, D = directory)?" — Microsoft Learn, "xcopy"

배치 스크립트처럼 사람이 응답할 수 없는 환경에서 이 프롬프트가 뜨면 스크립트가 그 자리에서 멈춘 것처럼 보인다. `/i`를 쓰면 원본이 여러 파일이거나 디렉터리일 때 대상을 자동으로 디렉터리로 간주해 이 프롬프트 자체를 없앨 수 있다.

**종료 코드로 실패 원인을 구분한다**: xcopy는 성공·실패를 세분화한 종료 코드를 반환한다.

| 종료 코드 | 의미 |
|---|---|
| 0 | 오류 없이 복사 완료 |
| 1 | 복사할 파일을 찾지 못함 |
| 2 | 사용자가 CTRL+C로 중단 |
| 4 | 초기화 오류(메모리·디스크 공간 부족, 잘못된 드라이브명·문법) |
| 5 | 디스크 쓰기 오류 |

위 예시의 배치 파일처럼 `if errorlevel`을 큰 값부터 검사하는 순서를 지켜야 한다 — `if errorlevel 2`는 "종료 코드가 2 이상"이라는 뜻이라, 검사 순서를 반대로 하면 항상 가장 낮은 조건에서 걸린다(30장 이후 4부에서 `if`와 `%ERRORLEVEL%`을 본격적으로 다룰 때 이 규칙을 다시 짚는다).

**파일명 경로가 너무 길면 메모리 부족 오류**: 파일 경로가 255자를 넘으면 "메모리 부족" 오류가 날 수 있다는 것이 Microsoft Learn에 명시되어 있다. 깊은 폴더 구조를 다루는 배포 스크립트에서 예상치 못하게 마주칠 수 있는 함정이다.

**`Copy-Item -Recurse`에는 `/d`, `/u` 같은 세밀한 필터 스위치가 없다**: PowerShell의 대응 명령은 `Copy-Item -Recurse`이지만, xcopy의 `/d:날짜`(지정 날짜 이후 변경된 파일만 복사)나 `/u`(대상에 이미 있는 파일만 갱신)처럼 조건을 붙여 복사 대상을 걸러내는 내장 스위치를 제공하지 않는다. 같은 결과를 얻으려면 `Get-ChildItem`으로 파일 목록을 가져온 뒤 `Where-Object`로 날짜나 존재 여부를 직접 걸러내고 그 결과를 다시 `Copy-Item`에 넘기는 식으로 별도 파이프라인을 구성해야 한다. xcopy 한 줄짜리 증분 백업 스크립트를 PowerShell로 옮길 때 이 부분이 여러 줄로 늘어나는 이유다.

## 흔한 오개념

<strong>"xcopy와 copy는 옵션만 다를 뿐 같은 명령이다"</strong>는 오해가 있다. copy는 파일 단위로만 동작하고 0바이트 파일이나 디렉터리를 복사할 수 없는 반면, xcopy는 애초에 디렉터리 트리를 다루도록 설계된 별도 명령이다. 옵션 집합이 겹치는 것(`/y`, `/v` 등)은 일관성을 위한 설계일 뿐, 두 명령의 근본적인 대상 범위가 다르다는 사실을 가린다.

## 다음 장에서는

다음은 16장 — xcopy보다 더 견고한 재시도·미러링 기능을 갖춘 `robocopy`를 다룬다.

## 평가 기준

- `/s`, `/e`, `/i`를 조합해 디렉터리 트리를 원하는 범위로 복사할 수 있다.
- xcopy가 대상 종류를 되묻는 상황과, `/i`로 그 프롬프트를 피하는 방법을 설명할 수 있다.
- xcopy 종료 코드 표를 읽고, 배치 스크립트에서 `if errorlevel`로 실패 원인을 구분해 처리할 수 있다.
- copy와 xcopy의 근본적인 대상 범위 차이를 설명할 수 있다.

## 참고

- [xcopy | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/xcopy)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
