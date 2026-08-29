---
draft: false
slug: copy-command-copy-files-windows-cmd
title: "[CMD] 14. copy - 파일 복사"
description: "copy 명령으로 파일을 복사하는 법과 +로 여러 파일을 하나로 합치는 기능, /a·/b ASCII·바이너리 모드가 위치에 따라 의미가 달라지는 함정, /v 검증 옵션을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 140
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
- copy
- 파일복사
- File-System
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Comparison(비교)
- Batch
- Linux(리눅스)
- Education(교육)
- CLI
- Configuration(설정)
- Deployment(배포)
- Advanced
image: "wordcloud.png"
---

copy는 하나 이상의 파일을 다른 위치나 같은 디렉터리에 다른 이름으로 복사하는 내장 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [13장: rmdir, rd](/post/cmd/rmdir-rd-command-remove-directory-windows-cmd/)에서 디렉터리를 지우는 법을 다룬 뒤 이어진다. 이 장부터 세 장(14–16장)은 복사 계열 명령 copy·xcopy·robocopy를 연속으로 다루며, 뒤로 갈수록 다루는 범위가 넓어진다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 디렉터리 트리 전체 복사는 15장(xcopy)·16장(robocopy)에서 다룬다. copy는 개별 파일(또는 파일 목록) 복사에 범위를 한정한다.

## 개요 + 정신 모델

copy가 다루는 대상은 언제나 개별 파일이지, 디렉터리 트리가 아니다. Microsoft Learn도 0바이트 파일이나 디렉터리 전체를 복사해야 한다면 xcopy를 쓰라고 명시적으로 안내한다.

> "To copy files that are 0 bytes long, or to copy all of a directory's files and subdirectories, use the [xcopy command](xcopy)." — Microsoft Learn, "copy"

copy의 또 다른 정신 모델은 "여러 원본을 `+`로 이으면 하나의 대상으로 합쳐진다"는 것이다. 이는 옵션이 아니라 copy의 기본 문법 자체에 내장된 동작이라, 파일을 나눠 합치는 텍스트 결합 도구로도 쓸 수 있다.

## 사용법

```
copy [/d] [/v] [/n] [/y | /-y] [/z] [/a | /b] <원본> [/a | /b] [+<원본> [/a | /b] [+ ...]] [<대상> [/a | /b]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/v` | 새로 쓴 파일이 올바르게 기록됐는지 검증(속도는 느려짐) |
| `/y` | 덮어쓸 때 확인 메시지 없이 진행 |
| `/-y` | 덮어쓸 때 항상 확인 메시지 표시 |
| `/n` | 8자·확장자 3자를 넘는 파일명을 짧은 이름(8.3 형식)으로 복사 |
| `/z` | 네트워크 파일을 재시작 가능 모드로 복사(연결이 끊겨도 이어서 진행) |
| `/d` | 암호화된 원본을 대상에서는 복호화된 상태로 저장 |
| `/a` | ASCII 텍스트 파일로 취급 |
| `/b` | 바이너리 파일로 취급(기본값, 파일을 합칠 때는 예외) |

## 예시

```
copy report.txt report.bak
copy *.txt D:\Backup\
copy robin.typ c:\birds
copy file1.txt + file2.txt combined.txt
copy mar89.rpt + apr89.rpt + may89.rpt Report
copy *.txt Combined.doc
copy /b *.exe Combined.exe
```

마지막 두 줄처럼 와일드카드로 여러 파일을 하나의 대상 이름으로 합칠 수도 있다. 이때 copy는 합친 파일들을 기본적으로 ASCII로 간주하므로, 실행 파일처럼 바이너리 데이터를 합칠 때는 반드시 `/b`를 명시해야 CTRL+Z를 파일 끝으로 오인해 데이터가 잘리는 사고를 막을 수 있다.

## 주의사항·함정

**`/a`, `/b`의 의미는 위치에 따라 달라진다**: 이 장에서 가장 헷갈리기 쉬운 규칙이다. `/a`나 `/b`가 원본 뒤에 오면 그 원본 파일을 해당 모드로 읽으라는 뜻이고, 대상 뒤에 오면 결과 파일을 어떤 모드로 쓸지 지정하는 뜻이 된다.

> "The effect of **/a** depends on its position in the command-line string: If **/a** follows *source*, the **copy** command treats the file as an ASCII file and copies data that precedes the first end-of-file character (CTRL+Z). If **/a** follows *destination*, the **copy** command adds an end-of-file character (CTRL+Z) as the last character of the file." — Microsoft Learn, "copy"

즉 같은 스위치라도 명령줄에서의 위치가 의미를 바꾼다. 여러 파일이 나열된 줄에서 `/a`나 `/b`를 하나만 쓰면, `copy`를 만날 때까지(또는 다음 `/a`/`/b`를 만날 때까지) 그 앞의 모든 파일에 적용된다는 점도 함께 기억해야 한다.

**자기 자신에게 복사할 수 없다**: 대상을 지정하지 않으면 원본과 같은 이름으로 현재 디렉터리에 복사를 시도하는데, 원본이 이미 그 자리에 있으면 복사가 거부된다.

> "File cannot be copied onto itself / 0 File(s) copied" — Microsoft Learn, "copy"

**`/y`의 기본값은 배치 스크립트 안에서 달라진다**: 대화형 세션에서는 기본적으로 덮어쓰기 전에 확인을 묻지만, 배치 스크립트 안에서 실행되는 copy는 이 확인을 건너뛴다. `COPYCMD` 환경 변수에 `/y`를 미리 설정해두면 어느 쪽이든 동작을 통일할 수 있고, 그 설정을 일회성으로 무시하려면 `/-y`를 함께 쓴다.

**`Copy-Item`은 `+`를 이용한 파일 합치기를 지원하지 않는다**: PowerShell의 대응 명령은 `Copy-Item`이지만, copy의 `copy file1.txt+file2.txt combined.txt` 같은 연결(concatenation) 문법에 대응하는 기능이 없다. 여러 파일을 하나로 합치려면 `Get-Content file1.txt,file2.txt | Set-Content combined.txt`처럼 내용을 읽어 다시 쓰는 방식으로 직접 구현해야 한다. copy의 `+` 문법으로 파일을 합치던 옛 배치 스크립트를 PowerShell로 옮길 때 이 부분이 자동 변환되지 않고 수작업 재작성이 필요한 대표적인 지점이다.

## 흔한 오개념

<strong>"대상을 지정하지 않고 copy를 실행하면 원본이 그 자리에서 덮어써지거나 손상될 위험이 있다"</strong>는 오해가 있다. 실제로는 원본과 대상이 같은 경로로 겹치는 상황을 CMD가 감지해 복사 자체를 거부하고 "File cannot be copied onto itself / 0 File(s) copied" 메시지만 남긴다. 즉 이런 실수를 해도 원본 파일은 전혀 손상되지 않으며, 단순히 아무 일도 일어나지 않는 명령으로 끝난다.

## 다음 장에서는

다음은 15장 — copy로는 다룰 수 없는 디렉터리 트리 전체 복사를 지원하는 `xcopy` 명령을 다룬다.

## 평가 기준

- copy로 파일을 복사하고, `+`로 여러 파일을 하나로 합칠 수 있다.
- `/a`, `/b`의 의미가 원본 뒤에 오는지 대상 뒤에 오는지에 따라 달라진다는 것을 설명할 수 있다.
- copy가 디렉터리 트리나 0바이트 파일 복사에는 적합하지 않다는 것과, 그럴 때 xcopy를 써야 하는 이유를 안다.
- 대화형 세션과 배치 스크립트에서 덮어쓰기 확인의 기본 동작이 다르다는 것을 안다.

## 참고

- [copy | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/copy)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
