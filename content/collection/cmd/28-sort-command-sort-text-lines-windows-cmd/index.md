---
draft: false
slug: sort-command-sort-text-lines-windows-cmd
title: "[CMD] 28. sort - 텍스트 입력 정렬"
description: "sort로 파일이나 파이프 입력을 줄 단위로 정렬하는 법과 대소문자를 구분하지 않는 기본 동작, /+n으로 특정 열부터 비교하는 법, 입력 파일에 바로 덮어쓰면 안 되는 이유를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 280
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
- sort
- 정렬
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
- Advanced
- Administration
image: "wordcloud.png"
---

sort는 파일 또는 표준 입력의 내용을 읽어 줄 단위로 정렬하고, 그 결과를 화면·파일·다른 장치로 내보내는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [27장: findstr](/post/cmd/findstr-command-regex-search-windows-cmd/)에서 패턴 검색을 다룬 뒤 이어진다. find·findstr로 걸러낸 결과를 다시 정렬해서 보는 조합이 이 장의 대표적인 활용 사례다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 정렬된 결과에서 중복을 제거하거나 개수를 세는 전용 명령은 CMD에 따로 없다(sort의 `/unique` 옵션이 유일한 관련 기능이다).

## 사용법

```
sort [/r] [/+<n>] [/m <킬로바이트>] [/l <로케일>] [/rec <문자수>] [[<드라이브1>:][<경로1>]<파일1>] [/t [<드라이브2>:][<경로2>]] [/o [<드라이브3>:][<경로3>]<파일3>]
명령 | sort [/r] [/+<n>]
```

## 옵션

| 옵션 | 설명 |
|---|---|
| `/r` | 역순(내림차순) 정렬 |
| `/+<n>` | 각 줄의 n번째 문자부터 비교 시작(기본 1). n보다 짧은 줄은 다른 줄보다 먼저 배치 |
| `/m <킬로바이트>` | 정렬에 사용할 메모리 크기 지정(최소 160KB) |
| `/l <로케일>` | 정렬 순서 로케일 재정의(기본 로케일 외 대안은 C 로케일뿐) |
| `/rec <문자수>` | 한 줄의 최대 문자 수(기본 4096, 최대 65535) |
| `/o <파일>` | 정렬 결과를 저장할 파일 지정 |
| `/unique` | 고유한 결과만 반환 |

## 예시

```
sort names.txt
sort /r numbers.txt
type list.txt | sort
dir /b | sort
sort /r expenses.txt
find "Jones" maillist.txt | sort
sort /+10 report.txt
sort input.txt /o output.txt
```

## 주의사항·함정

**대소문자를 구분하지 않는다**: sort는 대문자와 소문자를 구분하지 않고 정렬한다.

> "The **sort** command doesn't distinguish between uppercase and lowercase letters and has no limit on file size." — Microsoft Learn, "sort"

`Apple`과 `apple`이 같은 취급을 받으므로, 대소문자를 구분하는 정렬 결과가 필요하다면 sort만으로는 해결할 수 없다.

**입력 파일에 직접 덮어쓰면 안 된다**: `sort input.txt > input.txt`처럼 입력과 출력을 같은 파일로 지정하면 안 된다. 리다이렉션(`>`)은 명령이 실행되기 전에 먼저 대상 파일을 열어 비우기 때문에, sort가 파일을 읽기 시작하는 시점에는 이미 내용이 사라진 뒤다. 안전하게 파일을 갱신하려면 다른 이름으로 출력한 뒤 바꿔치거나, 명령 자체가 제공하는 `/o` 옵션을 쓴다 — Microsoft Learn도 입력 파일은 `filename1` 인자로 직접 지정하고 출력은 `/o`로 지정하는 방식이 리다이렉션보다 빠르고 안전하다고 안내한다.

**숫자를 문자열로 정렬한다**: sort는 숫자의 크기가 아니라 문자 코드 순서로 정렬한다. `2`, `10`, `9`를 정렬하면 `10`, `2`, `9` 순서로 나온다(맨 앞자리 `1`이 `2`, `9`보다 문자 코드가 작기 때문). 자릿수를 맞춰 앞에 0을 채우거나(`02`, `09`, `10`), 별도 도구로 후처리해야 진짜 숫자 순서를 얻을 수 있다.

**메모리가 부족하면 2단계로 나눠 처리한다**: 정렬할 데이터가 지정한(또는 기본) 메모리 크기를 넘으면 sort는 정렬과 병합을 두 단계로 나눠 진행하며, 중간 결과를 임시 파일에 저장한다. `/m`으로 실제보다 큰 메모리를 지정하면 오히려 성능이 나빠지거나 런타임 오류가 날 수 있다.

**PowerShell의 대응 명령은 `Sort-Object`이지만 정렬 대상의 성격이 다르다**: `Sort-Object`는 텍스트 줄이 아니라 구조화된 객체를 지정한 속성 기준으로 정렬하도록 설계됐다(예: `Get-ChildItem | Sort-Object Length`로 파일을 크기순으로 정렬). 평범한 텍스트를 파이프로 흘려보내면 sort와 비슷하게 줄 단위 정렬 결과를 얻을 수 있지만, 그건 `Sort-Object`의 본래 기능 중 극히 일부일 뿐이다. 객체 속성 기준 정렬이라는 `Sort-Object`의 핵심 능력에는 CMD의 텍스트 전용 sort로 대응할 방법이 아예 없다.

## 흔한 오개념

<strong>"sort는 숫자도 알아서 크기순으로 정렬해준다"</strong>는 오해가 흔하다. sort는 어디까지나 문자 단위 비교이므로, 로그 파일의 숫자 필드를 정렬할 때 `10`이 `9`보다 앞에 오는 상황을 자주 마주치게 된다. 진짜 숫자 정렬이 필요하다면 자릿수를 맞추거나 배치 스크립트에서 별도 로직을 짜야 한다.

## 다음 장에서는

다음은 29장 — Part 3의 마지막 장으로, 긴 출력을 한 화면씩 나눠 보여주는 `more` 명령을 다룬다.

## 평가 기준

- sort로 파일이나 파이프 입력을 정렬하고, `/r`로 역순 정렬을 할 수 있다.
- `/+n`으로 특정 문자 위치부터 비교를 시작하는 법을 설명할 수 있다.
- sort가 대소문자를 구분하지 않는다는 것과, 입력 파일에 직접 리다이렉션으로 덮어쓰면 안 되는 이유를 설명할 수 있다.
- sort가 숫자를 크기가 아니라 문자열로 비교한다는 것과, 그로 인한 정렬 결과의 함정을 설명할 수 있다.

## 참고

- [sort | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sort)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
