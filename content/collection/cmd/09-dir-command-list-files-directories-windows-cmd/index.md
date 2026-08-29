---
draft: false
slug: dir-command-list-files-directories-windows-cmd
title: "[CMD] 09. dir - 파일·디렉터리 목록 조회"
description: "dir 명령의 /a·/o·/s·/b 등 전체 스위치를 용도별로 정리하고, 와일드카드가 8.3 짧은 파일 이름까지 매칭해 의도치 않은 파일이 함께 걸리는 함정을 Microsoft Learn의 실제 사례로 설명합니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 90
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
- dir
- 디렉터리목록
- File-System
- Wildcard
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Comparison(비교)
- Linux(리눅스)
- Command-Line
- Education(교육)
- Productivity(생산성)
- CLI
- Configuration(설정)
image: "wordcloud.png"
---

dir은 지정한 디렉터리(생략하면 현재 디렉터리)의 파일과 하위 디렉터리 목록을 표시하는 내장 명령이다. 유닉스·리눅스의 `ls`에 대응한다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [08장: cd](/post/cmd/cd-chdir-command-change-directory-windows-cmd/)에서 디렉터리를 옮겨 다니는 법을 다룬 뒤 이어진다. cd로 원하는 위치에 도달했다면, dir은 그 자리에서 무엇을 볼 수 있는지 확인하는 명령이다.

**이 장의 깊이**: 입문–중급. 스위치가 많아 이 장의 옵션 표가 Part 1에서 가장 길다. **다루지 않는 것**: 파일 안의 텍스트를 검색하는 것은 3부(find, findstr)에서, 트리 형태로 계층 구조를 보는 것은 10장(tree)에서 각각 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 지금 당장 특정 파일을 찾는 사람 | 사용법, 예시의 "기본 조회"·"필터링" | 와일드카드와 자주 쓰는 스위치 조합으로 원하는 파일을 바로 찾는다 |
| 스크립트에서 dir 출력을 가공하려는 사람 | 옵션 전체, 주의사항·함정 | `/b`·`/a:-d`처럼 파싱하기 좋은 출력 형식을 선택하고, 와일드카드의 8.3 매칭 함정을 피한다 |

## 사용법

```
dir [<드라이브>:][<경로>][<파일이름>] [/p] [/q] [/w] [/d] [/a[[:]<속성>]] [/o[[:]<정렬순서>]] [/t[[:]<시간필드>]] [/s] [/b] [/l] [/n] [/x] [/c] [/4] [/r]
```

## 옵션

### 표시 형식

| 옵션 | 설명 |
|---|---|
| `/w` | 가로로 여러 열(최대 5개) 표시 |
| `/d` | `/w`와 같은 형식이되 파일이 열 단위로 정렬 |
| `/b` | 파일·디렉터리 이름만 나열(다른 정보 생략). `/w`보다 우선 |
| `/n` | 긴 목록 형식, 파일 이름을 화면 오른쪽에 표시 |
| `/l` | 이름을 정렬하지 않고 소문자로 표시 |
| `/x` | 8.3 형식 짧은 이름을 `/n`과 같은 형식으로 긴 이름 앞에 함께 표시 |
| `/4` | 연도를 4자리로 표시 |
| `/c` | 파일 크기에 천 단위 구분 기호 표시(기본값). `/-c`로 숨김 |

### 필터·범위

| 옵션 | 설명 |
|---|---|
| `/a[[:]<속성>]` | 지정한 속성의 항목만 표시. d(디렉터리) h(숨김) s(시스템) l(재구문분석지점) r(읽기전용) a(보관대상) i(색인제외). 생략하면 숨김·시스템 파일 제외한 전체, 값 없이 `/a`만 쓰면 숨김·시스템 포함 전체 |
| `/s` | 하위 디렉터리까지 재귀적으로 모두 표시 |
| `/q` | 파일 소유자 정보 표시 |
| `/r` | 파일의 대체 데이터 스트림 표시 |

### 정렬

| 옵션 | 설명 |
|---|---|
| `/o[[:]<정렬순서>]` | n(이름) e(확장자) g(디렉터리 우선) s(크기, 작은 순) d(날짜, 오래된 순). `-` 접두어로 역순 |
| `/t[[:]<시간필드>]` | c(생성) a(마지막 접근) w(마지막 기록) 중 정렬·표시 기준 시간 선택 |

### 화면 제어

| 옵션 | 설명 |
|---|---|
| `/p` | 한 화면씩 멈춤 |

## 예시

### 기본 조회

```
dir
dir /a:h
dir *.txt /s /b
dir /o:n
```

### 정렬·필터 조합

```
dir /s /w /o /p
dir /s /w /o /p /a:-d
dir /a:r-h
```

두 번째 예시는 `/a:-d`로 디렉터리 이름은 빼고 파일 이름과 확장자만 보이도록 필터링한다. 세 번째 예시(`/a:r-h`)처럼 속성 값을 여러 개 조합하면 지정한 속성을 모두 만족하는 항목만 표시된다 — 읽기 전용이면서 숨김이 아닌 파일만 걸러낸다.

### 파이프·리다이렉션 조합

```
dir > \records\dir.doc
dir c:\*.txt /w/o/s/p
```

출력을 다른 명령으로 넘기거나 파일로 리다이렉션하려면 `/a:-d`와 `/b`를 함께 써서 파일 이름만 한 줄씩 나오도록 만드는 것이 안전하다.

## 주의사항·함정

**와일드카드가 8.3 짧은 이름까지 매칭한다**: Microsoft Learn이 직접 예로 든 함정이다. 디렉터리에 `t.txt2`와 `t97.txt` 두 파일이 있을 때 `dir t97*`을 실행하면 `t97.txt`뿐 아니라 `t.txt2`까지 함께 나온다.

> "You might expect that typing `dir t97\*` would return the file t97.txt. However, typing `dir t97\*` returns both files, because the asterisk wildcard matches the file t.txt2 to t97.txt by using its short name map *T97B4~1.TXT*." — Microsoft Learn, "dir"

`*` 와일드카드가 파일의 8.3 형식 짧은 이름(`T97B4~1.TXT`)까지 매칭 대상으로 삼기 때문에 생기는 현상이다. 더 위험한 것은 Microsoft Learn이 같은 원리가 `del`에도 그대로 적용된다고 경고한다는 점이다 — `del t97\*`도 의도하지 않은 `t.txt2`까지 함께 지운다. `/x`로 짧은 이름을 미리 확인하거나, 삭제 전에 반드시 같은 와일드카드로 `dir`을 먼저 실행해 대상을 확인하는 습관이 필요하다(18장에서 del을 다룰 때 이 함정을 다시 짚는다).

**대용량 디렉터리에서 `/s`**: 하위 디렉터리가 많은 트리에서 `/s`를 쓰면 출력이 매우 길어진다. `/p`로 화면을 멈추거나 3부(29장: more)에서 다룰 페이저와 파이프로 조합하는 것이 좋다.

**유닉스 `ls`와의 대응 차이**: `ls -a`가 숨김 파일까지 보여주는 것과 달리, dir은 옵션 없이도 숨김·시스템 파일만 제외한 전체를 보여주고 `/a`로 숨김·시스템까지 포함시킨다는 점에서 기본값의 방향이 반대다. `ls -l`의 상세 정보는 dir의 기본 출력에 이미 포함되어 있어 별도 옵션이 필요 없다.

**PowerShell의 `dir`은 다른 명령의 별칭일 뿐이다**: PowerShell 세션에서 `dir`을 입력하면 CMD의 내장 dir이 아니라 `Get-ChildItem`의 별칭이 실행된다. 그래서 `dir /s`, `dir /a:h`, `dir /b`처럼 이 장에서 배운 CMD 전용 스위치를 PowerShell에 그대로 옮겨 치면 매개변수 바인딩 오류가 난다 — `Get-ChildItem`은 재귀 조회에 `-Recurse`, 숨김 포함에 `-Force`, 이름만 출력에 `-Name`처럼 완전히 다른 매개변수 이름을 쓰기 때문이다. CMD에서 익힌 dir 스위치를 그대로 복사해 PowerShell 창에 붙여넣었다가 오류를 마주치는 것은 실제로 흔히 발생하는 실수다.

## 흔한 오개념

<strong>"dir의 기본 출력은 항상 파일 이름 알파벳순으로 정렬되어 있다"</strong>는 오해가 있다. `/o`(또는 `/o:n`)를 명시하지 않으면 dir은 파일 시스템이 디렉터리 항목을 반환하는 순서를 그대로 보여줄 뿐이며, 이 순서는 파일 시스템과 생성·이름 변경 이력에 따라 달라질 수 있어 반드시 알파벳순이라는 보장이 없다. 스크립트에서 파일을 이름 순서대로 처리해야 한다면 눈에 보이는 정렬 상태를 신뢰하지 말고 `/o:n`을 명시적으로 지정해야 한다.

## 다음 장에서는

다음은 10장 — dir이 평면적으로 나열하는 목록을 계층 구조 그림으로 바꿔 보여주는 `tree` 명령을 다룬다.

## 평가 기준

- `/a`, `/o`, `/s`, `/b` 등 자주 쓰는 스위치를 조합해 원하는 형태의 목록을 만들 수 있다.
- 와일드카드가 8.3 짧은 이름까지 매칭한다는 함정을 설명하고, 삭제 명령 실행 전 확인 절차의 필요성을 안다.
- 스크립트에서 파싱하기 좋은 출력을 만들 때 `/b`와 `/a:-d`를 함께 쓰는 이유를 설명할 수 있다.
- dir의 기본 숨김 파일 처리 방식이 유닉스 `ls`와 반대 방향이라는 것을 안다.

## 참고

- [dir | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dir)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
