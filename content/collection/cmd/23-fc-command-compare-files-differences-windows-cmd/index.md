---
draft: false
slug: fc-command-compare-files-differences-windows-cmd
title: "[CMD] 23. fc - 파일 줄 단위·바이트 단위 비교"
description: "fc로 두 파일을 텍스트(줄 단위)와 바이너리(바이트 단위) 모드로 비교하는 법과 재동기화 실패 메시지의 의미, 종료 코드로 배치 스크립트에서 차이 유무를 판정하는 법, PowerShell fc 별칭 충돌을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 230
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
- fc
- 파일비교
- File-System
- ERRORLEVEL
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- PowerShell
- Comparison(비교)
- Batch
- CLI
- QA
- Configuration(설정)
- Advanced
image: "wordcloud.png"
---

fc(File Compare)는 두 파일을 비교해 차이를 보여주는 명령이다. 기본은 텍스트 모드(줄 단위)이고, `/b`로 바이너리 모드(바이트 단위)로 전환한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [22장: comp](/post/cmd/comp-command-compare-files-byte-windows-cmd/)에서 순수 바이트 단위 비교를 다룬 뒤 이어지며, Part 2(파일과 디렉터리 조작)의 마지막에서 두 번째 장이다. comp가 "같다/다르다"만 빠르게 답했다면, fc는 무엇이 어떻게 다른지 상세히 보여준다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
fc /a [/c] [/l] [/lb<n>] [/n] [/off[line]] [/t] [/u] [/w] [/<nnnn>] [<드라이브1>:][<경로1>]<파일1> [<드라이브2>:][<경로2>]<파일2>
fc /b [<드라이브1>:][<경로1>]<파일1> [<드라이브2>:][<경로2>]<파일2>
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/a` | ASCII 비교 결과를 축약해 각 차이 구간의 첫·끝 줄만 표시 |
| `/b` | 바이너리 모드(바이트 단위). `.exe`·`.com`·`.sys`·`.obj`·`.lib`·`.bin` 확장자는 이 모드가 기본값 |
| `/c` | 대소문자 무시 |
| `/l` | ASCII(줄) 모드로 비교. 위 확장자를 제외한 나머지 파일의 기본값 |
| `/lb<n>` | 내부 줄 버퍼 크기 지정(기본 100줄). 연속 차이가 이보다 많으면 비교 취소 |
| `/n` | 줄 번호 표시 |
| `/t` | 탭을 공백으로 바꾸지 않고 그대로 유지(기본은 8칸 단위로 변환) |
| `/u` | 유니코드 텍스트 파일로 비교 |
| `/w` | 연속 공백·탭을 하나로 압축해 비교 |
| `/<nnnn>` | 재동기화로 간주할 연속 일치 줄 수(기본 2) |

## 예시

```
fc file1.txt file2.txt
fc /a monthly.rpt sales.rpt
fc /b profits.bat earnings.bat
fc /n /w old.log new.log
fc *.bat new.bat
```

## 주의사항·함정

**파일 확장자가 비교 모드의 기본값을 결정한다**: `.exe`, `.com`, `.sys`, `.obj`, `.lib`, `.bin` 확장자는 명시하지 않아도 자동으로 바이너리 모드(`/b`)로 비교되고, 그 외 확장자는 텍스트 모드(`/l`)가 기본이다. 스크립트 파일(`.bat`)을 fc로 비교했는데 예상과 다른 형식의 출력이 나온다면 먼저 이 자동 판단 규칙을 의심해야 한다 — 예시의 `fc /b profits.bat earnings.bat`처럼 `.bat` 파일이라도 명시적으로 `/b`를 지정하면 바이트 단위로 비교할 수 있다.

**긴 연속 차이는 재동기화에 실패한다**: 텍스트 모드는 내부 버퍼(기본 100줄)에 파일을 읽어와 비교하다가, 한쪽에만 있는 삽입·삭제 구간을 만나면 다시 같아지는 지점(재동기화)을 찾아 이어간다. 연속된 차이가 버퍼 크기를 넘으면 다음 메시지와 함께 비교를 포기한다.

> "Resynch failed. Files are too different." — Microsoft Learn, "fc"

`/lb`로 버퍼 크기를 늘리면 더 큰 차이 구간도 재동기화를 시도할 수 있다.

**종료 코드로 차이 유무를 판정한다**: fc는 세 가지 종료 코드를 반환한다.

| 종료 코드 | 의미 |
|---|---|
| 0 | 파일이 동일함 |
| 1 | 파일이 다름 |
| 2 | 비교 중 오류 발생 |

배치 스크립트에서 `fc file1 file2 >nul` 뒤 `if errorlevel 1`로 분기하면, 화면 출력 없이 "다른가/같은가"만 프로그램적으로 판정할 수 있다.

**PowerShell에서는 `fc.exe`로 명시해야 한다**: fc라는 이름은 PowerShell에서 `Format-Custom` cmdlet의 별칭과 충돌한다.

> "You can use this command within PowerShell, but be sure to spell out the full executable (fc.exe) since 'fc' is also an alias for Format-Custom." — Microsoft Learn, "fc"

PowerShell 세션에서 그냥 `fc a.txt b.txt`를 입력하면 CMD의 fc가 아니라 `Format-Custom`이 실행되어 전혀 다른 결과가 나온다. `fc.exe a.txt b.txt`처럼 확장자를 명시해야 원래 의도한 명령이 실행된다.

## 흔한 오개념

<strong>"fc는 파일 내용을 살펴보고 텍스트인지 바이너리인지 스스로 판단해 비교 방식을 고른다"</strong>는 오해가 있다. 실제로 fc는 파일 내용을 전혀 들여다보지 않고, 위에서 다룬 확장자 목록(`.exe`, `.com`, `.sys`, `.obj`, `.lib`, `.bin`)에 해당하는지만 기계적으로 확인한다. 그래서 실제로는 바이너리인 파일을 `.dat`처럼 목록에 없는 확장자로 저장해두면 fc는 그것을 텍스트로 취급해 비교하고, 반대로 순수 텍스트 파일이라도 `.bin`으로 저장돼 있으면 바이너리 모드로 비교된다. 확장자가 실제 파일 형식과 다를 가능성이 있다면 자동 판단을 믿지 말고 `/b`나 `/l`을 직접 명시해야 한다.

## 다음 장에서는

다음은 24장 — 파일·디렉터리에 대한 심볼릭 링크와 하드 링크를 만드는 `mklink` 명령을 다룬다.

## 평가 기준

- fc로 텍스트(줄 단위)와 바이너리(바이트 단위) 모드를 구분해 파일을 비교할 수 있다.
- 확장자에 따라 기본 비교 모드가 자동으로 달라진다는 것을 설명할 수 있다.
- "재동기화 실패" 메시지가 나오는 이유와 `/lb`로 대응하는 법을 안다.
- fc의 종료 코드로 배치 스크립트에서 차이 유무를 판정할 수 있다.
- PowerShell에서 `fc`가 `Format-Custom`과 충돌하며 `fc.exe`로 명시해야 하는 이유를 설명할 수 있다.

## 참고

- [fc | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fc)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
