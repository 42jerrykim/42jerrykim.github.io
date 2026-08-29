---
draft: false
slug: path-command-executable-search-path-windows
title: "[CMD] 07. path - 실행 파일 검색 경로"
description: "path 명령으로 PATH 환경 변수를 조회·설정하는 법과 .exe·.com·.bat·.cmd 확장자 탐색 순서, path 명령의 세션 한정 변경과 setx의 영구 반영 차이를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 70
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
- path
- PATH
- 환경변수
- Environment
- Automation(자동화)
- Documentation(문서화)
- Best-Practices
- Troubleshooting(트러블슈팅)
- Configuration(설정)
- Comparison(비교)
- Registry
- Command-Line
- Education(교육)
- Productivity(생산성)
- CLI
image: "wordcloud.png"
---

path는 CMD가 실행 파일을 찾을 디렉터리 목록, 즉 `PATH` 환경 변수를 조회하거나 설정하는 내장 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [06장: doskey](/post/cmd/doskey-command-line-editing-macros-history-windows/)에서 명령줄 편집과 매크로를 다룬 뒤 이어진다. path는 01장에서 배운 "외부 명령어"가 애초에 어떻게 발견되는지를 설명하는 장이므로, 지금까지 아무 생각 없이 입력해온 `dir`·`doskey` 같은 명령이 실제로는 이 탐색 규칙을 거친다는 것을 이 장에서 확인한다.

**이 장의 깊이**: 입문–중급. **다루지 않는 것**: 시스템·사용자 환경 변수를 영구적으로 설정하는 GUI(시스템 속성) 절차나 `setx` 명령 자체의 상세 옵션은 다루지 않고, path 명령과의 관계만 짚는다.

## 개요 + 정신 모델

path 명령이 다루는 대상은 `PATH`라는 이름의 환경 변수 하나다. Microsoft Learn은 이렇게 정의한다.

> "Sets the command path in the PATH environment variable, specifying the set of directories used to search for executable (.exe) files. If used without parameters, this command displays the current command path." — Microsoft Learn, "path"

중요한 것은 이 탐색이 어떤 순서로 일어나는가다. Windows는 확장자를 생략한 명령을 입력했을 때 다음 순서로 파일을 찾는다.

> "The Windows operating system searches using default file name extensions in the following order of precedence: .exe, .com, .bat, and .cmd." — Microsoft Learn, "path"

이 순서를 알면 07장 제목 아래 예로 든 것과 같은 상황 — 같은 디렉터리에 `acct.exe`와 `acct.bat`가 함께 있을 때 `acct`만 입력하면 항상 `.exe`가 먼저 실행되고, `.bat`를 실행하려면 확장자를 명시해야 한다는 함정을 미리 대비할 수 있다.

## 사용법

```
path [[<드라이브>:]<경로>[;...][;%PATH%]]
path ;
```

## 옵션

| 사용 | 설명 |
|---|---|
| `path` | 현재 PATH 표시 |
| `path <경로>` | PATH를 새 경로로 설정(기존 값 전체 대체) |
| `path <경로>;%PATH%` | 기존 PATH 앞에 새 경로 추가 |
| `path %PATH%;<경로>` | 기존 PATH 뒤에 새 경로 추가 |
| `path ;` | PATH를 비움(현재 세션의 명령 경로를 현재 디렉터리로만 한정) |

## 예시

```
path
path c:\user\taxes;b:\user\invest;b:\bin
path C:\Tools;%PATH%
path ;
```

## 주의사항·함정

**세션 한정 변경**: path 명령으로 바꾼 PATH는 그 CMD 세션에만 적용되고, 창을 닫으면 원래 시스템·사용자 PATH로 돌아간다. 모든 새 CMD 세션에 영구히 반영하려면 `setx PATH "%PATH%;C:\Tools"`를 쓰거나 시스템 속성의 환경 변수 대화상자에서 직접 편집해야 한다. 다만 `setx`로 설정한 값은 그 시점 이후 새로 여는 세션부터 적용되며, 이미 열려 있는 CMD 창에는 반영되지 않는다는 점도 함께 기억해야 한다.

**같은 이름의 파일이 여러 개면 먼저 나오는 것이 이긴다**: 여러 디렉터리에 같은 이름과 확장자의 파일이 있으면, 현재 디렉터리를 먼저 검색한 뒤 PATH에 나열된 순서대로 디렉터리를 검색한다. 원하는 버전의 실행 파일이 다른 위치의 동명 파일에 가려질 수 있으므로, PATH에 새 디렉터리를 추가할 때는 앞뒤 순서를 의도적으로 정해야 한다.

**구분자는 세미콜론**: 유닉스 셸의 `PATH`는 콜론(`:`)으로 디렉터리를 구분하지만, Windows는 세미콜론(`;`)을 쓴다. 두 생태계를 오가며 PATH 문자열을 손으로 조합할 때 이 차이로 실수하기 쉽다.

**PowerShell에서는 `$env:Path`로 다룬다**: PowerShell은 PATH를 `$env:Path`라는 환경 변수 항목으로 노출한다. 조회는 `$env:Path`만 입력하면 되고, 변경은 `$env:Path = "..."`로 전체를 덮어쓰거나 `$env:Path += ";C:\new\dir"`로 뒤에 추가하는 식이며, Windows PowerShell에서도 CMD와 마찬가지로 세미콜론(`;`)을 구분자로 쓴다. 다만 PowerShell에는 `$env:Path -split ';'`로 문자열을 배열로 쪼개 각 디렉터리를 개별 항목으로 다루는 기능이 있는데, 이는 CMD의 path 명령에는 없는 편의 기능이다.

## 흔한 오개념

<strong>"path 명령과 PATH 환경 변수는 서로 다른 것이다"</strong>는 오해가 있다. 둘은 같은 대상을 가리킨다 — path는 PATH 환경 변수를 읽고 쓰는 명령일 뿐이다. 혼란은 오히려 다른 지점에서 생긴다. "path로 바꾼 값이 왜 다음에 CMD를 열었을 때 사라졌는가"라는 질문의 답은 세션 한정 변경이라는 위 주의사항에 있지, path와 PATH가 별개라서가 아니다.

## 다음 장에서는

다음은 08장 — path로 찾아낸 실행 파일이 실제로 실행되는 위치, 즉 현재 디렉터리를 옮겨 다니는 `cd` 명령을 다룬다.

## 평가 기준

- `path`, `path <경로>`, `path %PATH%;<경로>`, `path ;`의 각기 다른 효과를 설명할 수 있다.
- Windows가 확장자를 생략한 명령을 `.exe → .com → .bat → .cmd` 순서로 찾는다는 것을 알고, 동명 파일이 있을 때의 함정을 설명할 수 있다.
- path 명령의 변경이 세션 한정이며 영구 반영에는 `setx`나 시스템 속성이 필요하다는 것을 설명할 수 있다.
- 유닉스 PATH(`:`)와 Windows PATH(`;`)의 구분자 차이를 안다.

## 참고

- [path | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/path)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
