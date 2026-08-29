---
draft: false
slug: find-command-search-text-string-windows-cmd
title: "[CMD] 26. find - 파일·출력에서 문자열 검색"
description: "find로 파일이나 파이프 입력에서 문자열이 포함된 줄을 찾는 법과 와일드카드·정규식을 지원하지 않는 단순 검색기라는 한계, 캐리지리턴을 넘어 매칭하지 못하는 함정, 종료 코드로 배치에서 검색 성공 여부를 판정하는 법을 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 260
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
- find
- 텍스트검색
- Pipe(파이프)
- ERRORLEVEL
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
- Advanced
image: "wordcloud.png"
---

find는 파일이나 표준 입력(파이프)에서 지정한 문자열이 포함된 줄을 검색해 출력하는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [25장: replace](/post/cmd/replace-command-replace-files-windows-cmd/)로 Part 2(파일과 디렉터리 조작)를 마친 뒤 이어지며, <strong>Part 3(텍스트 검색과 출력 제어)</strong>의 첫 장이다. 20장(type)에서 파일 내용을 통째로 출력하는 법을 배웠다면, 이 장부터는 그 내용에서 원하는 줄만 걸러내는 쪽으로 넘어간다.

**이 장의 깊이**: 입문. **다루지 않는 것**: 와일드카드·정규식이 필요하면 27장(findstr)에서 다룬다. find는 순수 문자열 매칭에 범위를 한정한다.

## 개요 + 정신 모델

find가 세상을 보는 방식은 단순하다 — 입력을 줄 단위로 읽어, 지정한 문자열이 그 줄에 있는지 없는지만 판정하는 필터다. 정규식도 와일드카드도 이해하지 못하며, 오직 리터럴 문자열만 찾는다.

> "You can't use wildcards (**\*** and **?**) in the searched string. To search for a string with wild cards and regex patterns, you can use the **FINDSTR** command." — Microsoft Learn, "find"

파일 이름을 생략하면 표준 입력에서 읽어 필터로 동작한다는 점에서, 파이프 뒤에 붙는 첫 필터로 가장 자주 쓰인다.

## 사용법

```
find [/v] [/c] [/n] [/i] [/off[line]] "<문자열>" [[<드라이브>:][<경로>]<파일이름>[...]]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/v` | 지정한 문자열이 **없는** 줄만 표시 |
| `/c` | 일치하는 줄의 개수만 표시 |
| `/n` | 각 줄 앞에 줄 번호 표시 |
| `/i` | 대소문자 구분 없이 검색 |

### 종료 코드

| 종료 코드 | 의미 |
|---|---|
| 0 | 문자열을 찾음 |
| 1 | 문자열을 찾지 못함 |
| 2 | 파일을 찾지 못했거나 잘못된 스위치 |

## 예시

```
find "error" log.txt
find /i "warning" *.log
dir /s /b | find ".txt"
find /c "OK" result.txt
tasklist | find /v /i "agent"
sc query Winmgmt | find "RUNNING" >nul 2>&1 && (echo 서비스 실행 중) || (echo 서비스 중지됨)
```

마지막 예시는 find의 종료 코드를 배치 조건 분기(`&&`/`||`)와 결합해, 특정 서비스가 실행 중인지 화면 출력 없이 판정하는 실전 패턴이다.

## 주의사항·함정

**`/c`와 `/n`을 함께 쓰면 `/n`이 무시된다**: 두 옵션을 같이 지정하면 find는 `/n`을 조용히 무시하고 개수만 보여준다. 줄 번호가 안 나온다고 옵션 파싱이 잘못됐다고 오해하기 쉬운 지점이다.

**캐리지리턴을 넘어서는 매칭을 못한다**: find는 캐리지리턴 문자를 인식하지 못하므로, 찾으려는 문자열이 줄바꿈으로 끊겨 있으면 매칭에 실패한다.

> "This command doesn't report a match for the string tax file if a carriage return occurs between the words tax and file." — Microsoft Learn, "find"

**따옴표가 포함된 문자열은 겹쳐 써야 한다**: 검색할 문자열 자체에 큰따옴표가 들어있다면, 그 안의 각 따옴표를 큰따옴표 두 개로 겹쳐 써야 한다(`"""이 문장은 따옴표를 포함한다"""`).

**PowerShell에서는 `Select-String`이 대응 명령이다**: `Select-String`은 정규식을 기본으로 지원한다는 점에서 리터럴 문자열 매칭만 되는 find보다 오히려 findstr(27장)에 가깝다. 출력 형식도 다른데, find가 매칭된 줄을 그대로 텍스트로 뿌리는 반면 `Select-String`은 줄 번호·파일 이름·매칭된 텍스트를 담은 `MatchInfo` 객체를 반환하므로, 파이프라인 뒤에서 그 객체의 속성을 골라 쓰거나 추가로 가공하기가 훨씬 쉽다.

## 흔한 오개념

<strong>"find는 grep의 CMD 버전이라 비슷하게 쓰면 된다"</strong>는 오해가 흔하다. find는 정규식도 와일드카드도 지원하지 않는 순수 리터럴 문자열 매칭기일 뿐이라, grep에 익숙한 사용자가 기대하는 패턴 매칭 기능 대부분이 빠져 있다. 정규식이 필요한 순간 바로 다음 장의 findstr로 넘어가야 한다는 것이 이 장의 핵심 메시지다.

## 다음 장에서는

다음은 27장 — 정규식과 와일드카드, 재귀 검색까지 지원하는 `findstr` 명령을 다룬다.

## 평가 기준

- find로 파일이나 파이프 입력에서 문자열을 검색하고, `/v`·`/c`·`/n`·`/i`를 조합할 수 있다.
- find가 와일드카드·정규식을 지원하지 않는 순수 리터럴 매칭기라는 것을 설명할 수 있다.
- find의 종료 코드로 배치 스크립트에서 검색 성공 여부를 조건 분기에 활용할 수 있다.
- find와 grep의 근본적인 기능 차이를 설명할 수 있다.

## 참고

- [find | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/find)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
