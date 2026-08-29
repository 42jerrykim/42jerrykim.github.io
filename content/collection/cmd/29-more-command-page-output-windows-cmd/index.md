---
draft: false
slug: more-command-page-output-windows-cmd
title: "[CMD] 29. more - 출력을 한 화면씩 표시"
description: "more로 긴 출력을 한 화면씩 나눠 보는 법과 파이프·리다이렉션·파일 인자 세 가지 입력 방식의 차이, more 프롬프트에서 쓸 수 있는 P·S 서브명령, 유닉스 more·less와의 기능 차이를 Microsoft Learn 기준으로 정리했습니다."
date: 2026-08-28
lastmod: 2026-08-28
collection_order: 290
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
- more
- 페이저
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

more는 긴 출력을 한 번에 한 화면(페이지)씩 보여주고, 사용자 입력에 따라 다음 페이지로 넘기는 명령이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [28장: sort](/post/cmd/sort-command-sort-text-lines-windows-cmd/)에서 정렬을 다룬 뒤 이어지며, Part 3(텍스트 검색과 출력 제어)의 마지막 장이다. find·findstr로 걸러내고 sort로 정렬한 결과가 여전히 화면 하나를 넘칠 만큼 길 때, more가 그 마지막 단계를 담당한다.

**이 장의 깊이**: 입문–중급.

## 사용법

```
<명령> | more [/c] [/p] [/s] [/t<n>] [+<n>]
more [[/c] [/p] [/s] [/t<n>] [+<n>]] < [<드라이브>:][<경로>]<파일이름>
more [/c] [/p] [/s] [/t<n>] [+<n>] [<파일들>]
```

세 가지 문법이 각각 파이프 입력, 리다이렉션 입력, 파일 인자 직접 지정에 대응한다.

## 옵션

| 옵션 | 설명 |
|---|---|
| `/c` | 페이지를 표시하기 전에 화면을 지움 |
| `/p` | 폼피드 문자를 확장해서 표시 |
| `/s` | 여러 개의 연속 빈 줄을 한 줄로 압축 |
| `/t<n>` | 탭을 n칸 공백으로 표시 |
| `+<n>` | 첫 파일을 n번째 줄부터 표시 시작 |

### more 프롬프트(`-- More --`)에서 쓸 수 있는 키

| 키 | 동작 |
|---|---|
| Space | 다음 화면 표시 |
| Enter | 한 줄씩 표시 |
| F | 명령줄에 나열된 다음 파일 표시 |
| Q | more 종료 |
| = | 현재 줄 번호 표시 |
| P `<n>` | 다음 n줄 표시 |
| S `<n>` | 다음 n줄 건너뜀 |
| ? | 사용 가능한 명령 목록 표시 |

## 예시

```
type longfile.txt | more
more < clients.new
more clients.new
more +10 readme.txt
more /c /s < clients.new
more =
```

마지막 두 예시처럼, `/c /s` 조합은 화면을 지우고 연속 빈 줄까지 압축해 깔끔하게 보여주고, more 프롬프트에서 `=`를 입력하면 프롬프트 자체가 `-- More [Line: 24] --`처럼 현재 줄 번호를 함께 표시하도록 바뀐다.

## 주의사항·함정

**입력 방식에 따라 옵션 위치가 다르다**: 파이프로 넘길 때는 옵션이 more 뒤에 오지만(`type file | more /c`), 리다이렉션으로 줄 때는 옵션이 `<` 앞뒤 어디든 올 수 있고, 파일을 인자로 직접 줄 때는 옵션이 파일 이름보다 먼저 와야 한다. 이 셋을 혼동하면 옵션이 무시되거나 파일 이름으로 잘못 해석될 수 있다.

**대화형 프롬프트가 자동화 스크립트를 멈추게 한다**: more는 사람이 스페이스나 엔터를 눌러줄 것을 전제로 설계됐다. 배치 스크립트나 CI 파이프라인처럼 사람이 개입할 수 없는 환경에서 파이프 뒤에 more를 무심코 붙이면, 첫 화면을 다 채운 순간 스크립트가 응답 없이 멈춘 것처럼 보인다. 자동화 스크립트에서는 more 대신 결과를 파일로 리다이렉션하거나 `/c`(화면만 지움, 페이지 넘김 자체는 여전히 필요) 같은 옵션에 의존하지 말고 애초에 more를 넣지 않는 편이 안전하다.

## 흔한 오개념

<strong>"CMD의 more는 유닉스 more나 less와 기능이 동일하다"</strong>는 오해가 있다. 이름은 같지만 CMD의 more는 뒤로 스크롤하는 기능이 없고(`less`의 대표 장점), 검색 기능도 없다. `P n`/`S n` 서브명령으로 줄 단위 이동은 가능하지만, 유닉스 `less`가 제공하는 `/pattern` 검색이나 위아래 자유 이동에는 미치지 못한다. 더 강력한 탐색이 필요하다면 CMD 생태계 안에서는 PowerShell의 `Out-Host -Paging`이나 서드파티 페이저를 고려해야 한다.

## 다음 장에서는

다음은 30장 — 메시지를 출력하고 배치 스크립트의 에코 여부를 설정하는 `echo` 명령으로 Part 4(배치 스크립팅)가 시작된다.

## 평가 기준

- more로 파이프·리다이렉션·파일 인자 세 가지 방식의 긴 출력을 한 화면씩 볼 수 있다.
- more 프롬프트에서 P, S, =, Q 등 서브명령을 활용할 수 있다.
- 자동화 스크립트에 more를 넣으면 대화형 프롬프트 때문에 멈출 수 있다는 것을 설명할 수 있다.
- CMD의 more가 유닉스 `less`와 달리 뒤로 스크롤·검색 기능이 없다는 것을 안다.

## 참고

- [more | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/more)
- [Command-Line Syntax Key | Microsoft Learn](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/command-line-syntax-key)
