---
draft: false
slug: type-command-display-file-contents-windows-cmd
title: "[CMD] 20. type - 텍스트 파일 내용 출력"
description: "type으로 텍스트 파일 내용을 화면에 출력하는 법과 바이너리 파일에 쓰면 안 되는 이유, PowerShell에서 Get-Content 별칭으로 재사용되는 관계, more·리다이렉션과의 조합을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 200
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
- type
- 파일출력
- File-System
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- PowerShell
- Linux(리눅스)
- Education(교육)
- Batch
- CLI
- Comparison(비교)
- Configuration(설정)
- Advanced
image: "wordcloud.png"
---

type은 텍스트 파일의 내용을 화면(표준 출력)에 그대로 출력하는 내장 명령이다. 유닉스의 `cat`에 대응한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [19장: ren, rename](/post/cmd/ren-rename-command-rename-files-windows-cmd/)에서 파일 이름을 바꾸는 법을 다룬 뒤 이어진다. 지금까지 Part 2는 파일을 만들고 옮기고 지우고 이름을 바꾸는 "조작"이었다면, 이 장부터 21–23장(attrib, comp, fc)까지는 파일을 있는 그대로 "들여다보는" 쪽으로 초점이 옮겨간다.

**이 장의 깊이**: 입문. **다루지 않는 것**: 파일 안에서 특정 문자열을 찾는 것은 3부(find, findstr)에서, 긴 출력을 페이지 단위로 넘겨 보는 것은 29장(more)에서 각각 다룬다.

## 사용법

```
type [<드라이브>:][<경로>]<파일이름>
```

## 옵션

별도 옵션은 없다. 공백이 있는 파일명은 따옴표로 감싸고, 파일명을 여러 개 나열하면 순서대로 이어서 출력한다.

## 예시

```
type readme.txt
type *.log
type file1.txt file2.txt
type holiday.mar | more
```

## 주의사항·함정

**바이너리 파일에 쓰면 안 된다**: type은 텍스트 파일 전용으로 설계됐다. 바이너리 파일이나 프로그램이 만든 파일에 쓰면 제어 코드가 화면에 그대로 출력되어 알아볼 수 없는 문자가 뒤섞인다.

> "If you display a binary file or a file that is created by a program, you may see strange characters on the screen, including formfeed characters and escape-sequence symbols. ... In general, avoid using the **type** command to display binary files." — Microsoft Learn, "type"

**PowerShell에서는 Get-Content의 별칭일 뿐이다**: CMD의 type과 PowerShell의 `type`은 이름은 같지만 서로 다른 구현이다.

> "In PowerShell, **type** is a built-in alias to the [Get-Content cmdlet], which also displays the contents of a file, but using a different syntax." — Microsoft Learn, "type"

즉 PowerShell에서 `type file.txt`가 동작하는 것은 CMD 명령이 PowerShell에서도 통해서가 아니라, PowerShell이 `Get-Content`에 `type`이라는 별칭을 붙여뒀기 때문이다. `Get-Content`는 파일을 줄 단위 객체 배열로 반환하는 등 CMD의 type과는 출력 형식·활용 방식이 다르다.

**긴 출력은 페이저나 리다이렉션과 조합한다**: 파일이 길면 `type file.txt | more`로 한 화면씩 볼 수 있고(29장에서 more를 본격적으로 다룬다), `type a.txt > b.txt`로 다른 파일에 저장할 수도 있다. 인코딩이 맞지 않아 한글이 깨진다면 06장(doskey) 이후 다룰 `chcp`로 코드 페이지를 맞추거나, PowerShell의 `Get-Content`(인코딩 옵션이 더 풍부하다)를 대안으로 고려할 만하다.

## 흔한 오개념

<strong>"type은 어떤 파일이든 화면에 보여주기만 할 뿐이라 안전하다"</strong>는 오해가 있다. 단순히 "이상한 문자가 섞여 보인다" 수준을 넘어, 바이너리 데이터 안에 우연히 ANSI 이스케이프 시퀀스나 제어 문자가 섞여 있으면 커서가 엉뚱한 곳으로 튀거나 경고음이 울리는 등 콘솔 자체가 예상치 못하게 반응할 수 있다. 아주 큰 텍스트 로그 파일도 마찬가지로 위험한데, 페이저 없이 그대로 type하면 수만 줄이 순식간에 스크롤되어 화면과 스크롤백 버퍼를 채워버린다. type은 사람이 읽기 위해 만들어진 일반 텍스트 파일에만 쓰는 것이 안전하다.

## 다음 장에서는

다음은 21장 — 파일의 읽기 전용·숨김·시스템 속성을 표시하고 바꾸는 `attrib` 명령을 다룬다.

## 평가 기준

- type으로 텍스트 파일 내용을 출력하고, 여러 파일을 이어서 출력할 수 있다.
- type을 바이너리 파일에 쓰면 안 되는 이유를 설명할 수 있다.
- PowerShell의 `type`이 CMD 명령이 아니라 `Get-Content`의 별칭이라는 것을 설명할 수 있다.
- 긴 출력을 다루는 두 가지 방법(페이저 조합, 파일 리다이렉션)을 안다.

## 참고

- [type | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/type)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
