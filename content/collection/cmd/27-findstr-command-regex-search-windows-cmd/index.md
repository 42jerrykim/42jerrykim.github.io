---
draft: false
slug: findstr-command-regex-search-windows-cmd
title: "[CMD] 27. findstr - 정규식 지원 문자열 검색"
description: "findstr로 정규식·와일드카드 기반 텍스트 검색을 하는 법과 옵션을 지정하지 않아도 정규식 모드가 기본값이라는 함정, CMD 고유 메타문자(\\<, \\>)와 /s 재귀 검색, /c로 공백 포함 문자열을 다루는 법을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 270
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
- Advanced
- findstr
- 정규식
- Regex
- Pipe(파이프)
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Linux(리눅스)
- Education(교육)
- Batch
- CLI
- Comparison(비교)
- Configuration(설정)
image: "wordcloud.png"
---

findstr은 파일이나 파이프 입력에서 문자열 패턴을 검색하는 명령이다. 26장의 find보다 훨씬 강력하며, 정규식과 재귀 디렉터리 검색을 지원한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [26장: find](/post/cmd/find-command-search-text-string-windows-cmd/)에서 단순 리터럴 검색을 다룬 뒤 이어진다. find가 예고한 "정규식이 필요하면 findstr"이 바로 이 장이다.

**이 장의 깊이**: 중급. CMD 고유의 정규식 메타문자 표기가 익숙한 정규식 문법과 다르므로 주의 깊게 다룬다. **다루지 않는 것**: PowerShell이나 .NET의 정규식 문법은 findstr의 메타문자와 다르며, 이 장은 findstr 자체의 메타문자만 다룬다.

## 사용법

```
findstr [/b] [/e] [/l | /r] [/s] [/i] [/x] [/v] [/n] [/m] [/o] [/p] [/f:<파일>] [/c:<문자열>] [/g:<파일>] [/d:<디렉터리목록>] <문자열들> [<드라이브>:][<경로>]<파일이름>[...]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/b` | 줄 시작과 일치할 때만 |
| `/e` | 줄 끝과 일치할 때만 |
| `/l` | 검색 문자열을 리터럴로 처리 |
| `/r` | 검색 문자열을 정규식으로 처리(**기본값**) |
| `/s` | 현재 디렉터리와 하위 디렉터리 검색 |
| `/i` | 대소문자 구분 없음 |
| `/x` | 줄 전체가 정확히 일치할 때만 |
| `/v` | 일치하지 **않는** 줄만 표시 |
| `/n` | 줄 번호 표시 |
| `/m` | 일치하는 파일 이름만 표시 |
| `/o` | 각 일치 줄 앞에 문자 오프셋 표시 |
| `/c:<문자열>` | 지정한 텍스트를 리터럴 검색 문자열로 사용(공백 포함 문자열에 필요) |
| `/g:<파일>` | 검색 문자열 목록을 파일에서 읽음 |
| `/f:<파일>` | 검색할 파일 목록을 파일에서 읽음 |
| `/d:<디렉터리목록>` | 세미콜론으로 구분한 여러 디렉터리를 검색 |

### 정규식 메타문자

| 메타문자 | 의미 |
|---|---|
| `.` | 임의의 한 문자 |
| `*` | 앞선 문자·클래스의 0회 이상 반복 |
| `^` | 줄의 시작 |
| `$` | 줄의 끝 |
| `[class]` | 문자 집합 중 하나 |
| `[^class]` | 문자 집합에 속하지 않는 문자 |
| `[x-y]` | 범위 안의 문자 |
| `\x` | 메타문자를 리터럴로 사용(이스케이프) |
| `\<string` | 단어의 시작 |
| `string\>` | 단어의 끝 |

## 예시

```
findstr hello there x.y
findstr /c:"hello there" x.y
findstr Windows proposal.txt
findstr /s /i Windows *.*
findstr /b /n /r /c:"^ *FOR" *.bas
findstr /g:stringlist.txt /f:filelist.txt > results.out
findstr /s /i /m \<computer\> *.*
findstr /s /i /m \<comp.* *.*
```

## 주의사항·함정

**정규식이 기본값이다**: 이 장에서 가장 자주 놓치는 함정이다. findstr은 스위치를 지정하지 않으면 검색 문자열을 리터럴이 아니라 정규식으로 해석한다.

> "/r — Processes search strings as regular expressions. This is the default setting." — Microsoft Learn, "findstr"

즉 `findstr "a.b" file.txt`를 실행하면 `.`이 "점 문자 자체"가 아니라 "임의의 한 문자"로 해석되어, `axb`나 `a5b` 같은 줄까지 함께 매칭된다. 순수하게 점 문자 그대로를 찾고 싶다면 `\.`로 이스케이프하거나 `/l`로 리터럴 모드를 명시해야 한다.

**메타문자 표기가 표준 정규식과 다르다**: 단어 경계를 나타낼 때 PCRE·POSIX 계열의 `\b` 대신 findstr은 `\<`(단어 시작)와 `\>`(단어 끝)를 따로 쓴다. 다른 정규식 엔진에 익숙한 사람일수록 이 표기 차이에서 자주 걸린다.

**공백이 포함된 검색어는 `/c:`가 필요하다**: 공백으로 구분된 여러 문자열을 지정하면 findstr은 그것들을 OR 조건으로 각각 검색한다. "hello there"를 하나의 문자열로 찾고 싶다면 `/c:"hello there"`처럼 명시해야 한다 — 그냥 따옴표로만 감싸면 "hello"와 "there" 중 하나라도 있는 줄을 찾는 것으로 오해되기 쉽다.

**여러 검색어를 파일로 관리할 수 있다**: `/g:`로 검색 문자열 목록을, `/f:`로 검색 대상 파일 목록을 각각 별도 파일에서 읽어올 수 있다. 검색 조건이 많아지는 배치 스크립트에서 명령줄이 지나치게 길어지는 것을 피할 수 있다.

## 흔한 오개념

<strong>"findstr은 find에 옵션 몇 개를 더한 것뿐이다"</strong>는 오해가 있다. 두 명령은 기본 동작 방식 자체가 다르다 — find는 항상 리터럴 매칭만 하는 반면, findstr은 기본이 정규식이다. find에서 findstr로 옵션만 바꿔 쓰면 되겠거니 생각하고 정규식 메타문자가 든 검색어를 find에 그대로 옮기면(정규식이 무시되고 리터럴로 처리됨) 전혀 다른 결과를 얻는다.

## 다음 장에서는

다음은 28장 — 텍스트 입력을 줄 단위로 정렬하는 `sort` 명령을 다룬다.

## 평가 기준

- findstr로 정규식·리터럴 문자열을 검색하고, `/s`로 하위 디렉터리까지 재귀 검색할 수 있다.
- findstr의 기본 모드가 리터럴이 아니라 정규식이라는 것과, 리터럴 검색을 강제하려면 `/l`을 써야 한다는 것을 설명할 수 있다.
- `\<`, `\>` 같은 findstr 고유 메타문자 표기를 다른 정규식 엔진과 구분해 설명할 수 있다.
- 공백이 포함된 문자열을 검색할 때 `/c:`가 필요한 이유를 설명할 수 있다.

## 참고

- [findstr | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/findstr)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
