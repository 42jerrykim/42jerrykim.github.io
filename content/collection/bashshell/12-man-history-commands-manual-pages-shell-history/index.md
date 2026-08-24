---
draft: false
slug: man-history-commands-manual-pages-shell-history
title: "[Bash Shell] 12. man, history - 매뉴얼과 명령 기록"
description: "man은 설치된 명령어의 공식 매뉴얼을 섹션별로 찾아 읽는 도구이고, history는 셸이 기록한 과거 명령을 조회·재실행하는 도구다. man 섹션 번호 구분과 apropos 검색, HISTSIZE·HISTFILE 환경변수, !!·!$·Ctrl+R 확장까지 예제로 정리해 Part 1을 마무리한다."
date: 2026-03-15
lastmod: 2026-08-23
collection_order: 120
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- Documentation(문서화)
- Automation(자동화)
- Environment
- Quick-Reference
- Configuration(설정)
- History(역사)
- Reference(참고)
- Guide(가이드)
- Tutorial(튜토리얼)
- How-To
- Tips
- Beginner
- Troubleshooting(트러블슈팅)
- man
- 매뉴얼
- manual
- history
- 히스토리
- apropos
- whatis
- HISTSIZE
- HISTFILE
- HISTFILESIZE
- man-pages
- reverse-search
- section-number
image: "wordcloud.png"
---

`man`은 시스템에 설치된 명령어·함수·설정 파일의 **공식 매뉴얼 페이지**를 섹션별로 찾아 읽는 도구이고, `history`는 지금까지 셸에 입력한 명령을 기록해 두었다가 **조회·검색·재실행**할 수 있게 해주는 도구다. 두 도구 모두 "이미 어딘가에 있는 정보를 다시 만들어내지 않고 찾아 쓴다"는 같은 목적을 갖는다 — 하나는 시스템이 미리 써 둔 문서를, 다른 하나는 내가 방금 전에 스스로 입력한 명령을 대상으로 한다는 점만 다르다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [11장: .bashrc와 로그인/비로그인 셸](/post/bashshell/bashrc-bash-profile-login-shell-startup-files/)에서 셸이 시작될 때 어떤 설정 파일을 읽어 프롬프트·별칭·환경변수를 구성하는지 다룬 뒤 이어진다. 이 장은 <strong>Part 1(셸 기초와 탐색)</strong>의 마지막 챕터로, 지금까지 익힌 `cd`·`ls`·`cat`부터 `.bashrc`까지의 명령어들을 스스로 더 찾아보는 도구(`man`)와, 이미 입력했던 명령을 다시 활용하는 도구(`history`)를 정리한다.

**이 장의 깊이**: **입문** 난이도다. 셸 프롬프트에서 명령을 몇 번 실행해 본 경험이면 충분하고, 별도의 스크립팅 지식은 필요 없다. **다루지 않는 것**: 매뉴얼 페이지 자체를 작성하는 문법(troff/groff 매크로)은 다루지 않고, 셸 스크립트 안에서 `HISTCONTROL`의 세부 값(`ignoredups`, `erasedups` 등)을 조합해 기록 정책을 정교하게 튜닝하는 내용도 범위 밖이다 — 여기서는 실무에서 매일 쓰는 "찾기"와 "재사용" 범위만 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| 명령어 사용법이 급한 사람 | "개요 + 정신 모델", "사용법·옵션"의 man, "예시"의 man 부분 | `man`과 `apropos`로 낯선 명령어의 사용법을 스스로 찾아낼 수 있다 |
| 반복 입력을 줄이고 싶은 사람 | "사용법·옵션"의 history, "예시"의 history 부분, "주의사항·함정" 전체 | 히스토리 확장과 `HISTSIZE`/`HISTFILE` 관계를 이해해 이전 명령을 빠르게 재사용할 수 있다 |

## 개요 + 정신 모델

`man`은 **로컬에 설치된 오프라인 사전**에 가깝다. 패키지를 설치하면 그 패키지에 딸린 매뉴얼 페이지도 함께 설치되고, `man`은 인터넷 검색 없이 그 페이지들을 섹션별로 분류해 즉시 보여준다. 검색 대상은 명령어 하나만이 아니라 시스템 콜, 라이브러리 함수, 설정 파일 형식까지 포괄하므로, 같은 이름이 여러 섹션에 걸쳐 존재하는 경우가 흔하다 — 이 구조를 모르면 원하는 문서를 못 찾고 헤매게 된다.

`history`는 셸이 유지하는 <strong>"내가 입력한 명령의 로그"</strong>다. 로그는 두 군데에 나뉘어 존재한다는 점이 핵심 정신 모델이다 — 지금 열려 있는 셸 세션이 메모리에 들고 있는 **히스토리 목록**과, 디스크에 저장돼 다음 세션에서도 이어받는 **히스토리 파일**(`HISTFILE`, 기본값 `~/.bash_history`)이다. 이 둘이 언제 동기화되는지(대개 셸 종료 시점)를 이해하면 뒤에서 다룰 `history -c`의 함정과 여러 터미널을 동시에 쓸 때의 혼란을 피할 수 있다.

## 사용법 · 옵션

### man

```bash
man [섹션] 이름
man -k 키워드
man -f 이름
```

매뉴얼은 주제별로 아래처럼 9개 섹션으로 나뉜다. 같은 이름의 문서가 여러 섹션에 있으면 `man`은 정해진 우선순위(대개 1 → 8 → 2 → 3 → 5 → 4 → 9 → 6 → 7 순)로 검색해 **첫 번째로 찾은 섹션만** 보여주므로, 원하는 섹션이 따로 있다면 번호를 직접 지정해야 한다.

| 섹션 | 내용 |
|------|------|
| 1 | 사용자 실행 명령어·셸 명령 |
| 2 | 시스템 콜(커널이 제공하는 함수) |
| 3 | 라이브러리 함수 |
| 4 | 특수 파일(주로 `/dev` 하위 장치 파일) |
| 5 | 파일 형식과 관례(예: `/etc/passwd`) |
| 6 | 게임 |
| 7 | 기타(매크로 패키지, 규약 등) |
| 8 | 시스템 관리자용 명령어(대개 root 권한 필요) |
| 9 | 커널 루틴(비표준) |

| 옵션 | 설명 |
|------|------|
| `-k 키워드`, 별칭 `apropos` | 매뉴얼 이름·짧은 설명에서 키워드를 정규식으로 검색 |
| `-f 이름`, 별칭 `whatis` | 이름과 정확히 일치하는 페이지의 한 줄 요약만 출력 |
| `-a` | 해당 이름의 모든 섹션을 순서대로 모두 표시 |
| `-w 이름` | 실제 페이지 파일 경로만 출력(내용 없이) |

### history

```bash
history [n]
history -c
history -d 위치
history -a | -n | -r | -w [파일]
```

| 옵션 | 설명 |
|------|------|
| (없음) | 번호와 함께 히스토리 목록 전체 출력. `n`을 주면 최근 n개만 |
| `-c` | **현재 세션의 메모리상** 히스토리 목록을 비운다(히스토리 파일은 그대로) |
| `-d 위치` | 지정한 위치(또는 `시작-끝` 범위)의 항목 하나만 삭제 |
| `-a` | 이번 세션에서 새로 추가된 명령만 히스토리 파일 끝에 append |
| `-n` | 세션 시작 이후 파일에 추가된(다른 세션이 써 넣은) 항목을 현재 목록으로 읽어들임 |
| `-r` | 히스토리 파일 전체를 읽어 현재 목록 뒤에 이어붙임 |
| `-w` | 현재 메모리상의 히스토리 목록으로 파일을 **덮어쓰기** 저장 |
| `-p 인자...` | 히스토리 확장만 수행해 결과를 출력(목록에는 저장하지 않음) — 실제로 실행하기 전 미리보기용 |

### 히스토리 확장 (Bash)

| 표기 | 의미 |
|------|------|
| `!!` | 직전 명령 전체 |
| `!n` | 히스토리 목록의 n번째 명령 |
| `!-n` | 현재로부터 n개 이전 명령 |
| `!문자열` | 그 문자열로 **시작하는** 가장 최근 명령 |
| `!?문자열?` | 그 문자열을 **포함하는** 가장 최근 명령 |
| `!$` | 직전 명령의 마지막 단어(인자) |
| `!*` | 직전 명령의 모든 인자(명령어 자신 제외) |
| `^old^new^` | 직전 명령에서 `old`를 `new`로 바꿔 재실행(빠른 치환) |

위 표의 `!` 확장은 입력한 즉시 텍스트로 치환되는 방식이다. 이와 별개로 **Ctrl+R**은 Readline이 제공하는 **대화형 역방향 검색**(reverse-i-search)으로, 프롬프트에 `(reverse-i-search)`가 뜬 상태에서 검색어를 타이핑하면 히스토리 목록을 실시간으로 훑어 일치하는 명령을 찾아준다. 원하는 명령을 찾으면 Enter로 바로 실행하거나, 화살표 키로 편집 모드로 빠져나와 수정한 뒤 실행할 수 있다 — 명령의 정확한 시작 문자열을 몰라도 일부만 기억나면 찾을 수 있어 `!문자열`보다 활용도가 넓다.

## 예시

### man으로 매뉴얼 찾기

```bash
# 기본: 첫 번째로 매칭되는 섹션(대개 섹션 1)을 보여준다
man ls

# 섹션을 명시적으로 지정 — /etc/passwd 파일 형식을 보고 싶을 때
man 5 passwd

# 시스템 콜 open()의 매뉴얼(섹션 2)
man 2 open

# 이름은 몰라도 "파티션"과 관련된 명령을 찾고 싶을 때
man -k partition

# 정확한 이름의 한 줄 요약만 빠르게 확인
man -f printf
```

### history로 과거 명령 다루기

```bash
# 최근 20개 명령 확인
history 20

# 직전 명령을 그대로 재실행
!!

# 직전 명령의 마지막 인자만 재사용 (예: mkdir foo 다음 cd !$)
mkdir new_project
cd !$

# "git commit"으로 시작했던 가장 최근 명령을 다시 실행
!git

# 직전 명령에서 오타만 고쳐 재실행 (예: gerp를 grep으로)
gerp "TODO" app.py
^gerp^grep^

# 지금까지 쌓인 세션 히스토리를 파일에 즉시 저장(셸 종료를 기다리지 않고)
history -a
```

## 주의사항·함정

**같은 이름이 여러 섹션에 있으면 번호를 지정해야 한다.** `passwd`가 대표적인 예다 — 섹션 1은 비밀번호를 변경하는 **명령어** `passwd(1)`이고, 섹션 5는 `/etc/passwd` **파일 형식**을 설명하는 `passwd(5)`다. `man passwd`만 입력하면 `man`의 검색 우선순위상 대개 섹션 1(명령어)이 먼저 나오므로, 파일 형식을 확인하려던 사람은 원하는 문서를 못 보고 헤매게 된다. `printf(1)`(셸 명령어)과 `printf(3)`(C 라이브러리 함수), `crontab(1)`(사용자 명령)과 `crontab(5)`(crontab 파일 형식)도 같은 함정이 있다 — 이럴 때는 항상 `man 5 passwd`처럼 섹션 번호를 앞에 붙인다.

**`man -k`(apropos)는 별도 데이터베이스를 참조한다.** 리눅스의 `man -k`/`apropos`는 매번 전체 매뉴얼을 뒤지는 것이 아니라 `mandb`(8)가 미리 만들어 둔 색인 데이터베이스를 검색한다. 패키지를 새로 설치한 직후 색인이 아직 갱신되지 않았다면 방금 설치한 명령어가 `apropos` 결과에 나타나지 않을 수 있고, 이때는 `sudo mandb`로 색인을 다시 만들어야 한다. `whatis`(`man -f`와 동일)도 같은 데이터베이스를 쓴다.

**세션 히스토리와 히스토리 파일은 별개다.** `history -c`는 **지금 열려 있는 셸의 메모리상 목록만** 비운다 — 디스크의 `~/.bash_history` 파일은 그대로 남고, 그 셸을 정상 종료하면 오히려 종료 시점의 `$HISTSIZE`개 항목이 다시 파일에 저장돼 버릴 수 있다. 진짜로 기록을 지우고 싶다면 `history -c` 이후 `history -w`로 빈 목록을 파일에 덮어써야 한다. 터미널 창을 여러 개 동시에 열어 쓰는 경우도 흔한 함정이다 — `histappend` 셸 옵션이 꺼져 있으면 나중에 닫히는 세션이 먼저 닫힌 세션의 기록을 파일째로 덮어써 버려 일부 명령이 사라진 것처럼 보인다.

**`!!` 재실행은 부작용이 있는 명령에서 특히 위험하다.** 직전 명령이 `rm`, `git push --force`처럼 되돌리기 어려운 명령이었다면, `!!`나 `sudo !!`를 무심코 입력해 그 명령을 그대로 다시 실행하는 실수가 나올 수 있다. 확신이 없다면 먼저 `history -p '!!'`로 실제 확장 결과만 미리 확인하거나, `!!` 대신 위·아래 화살표로 직접 눈으로 보고 실행하는 편이 안전하다.

## 흔한 오개념

**"`history`도 셸 명령어니까 man 페이지가 따로 있을 것"이라는 오해가 흔하다.** `history`는 외부 실행 파일이 아니라 **bash 내장(builtin) 명령**이라 독립된 `history(1)` man 페이지가 없다. 대신 `bash(1)` man 페이지의 "SHELL BUILTIN COMMANDS" 항목에 통합돼 있거나, 셸 안에서 바로 `help history`로 확인해야 한다. `cd`, `export`, `alias` 같은 다른 내장 명령도 마찬가지다 — man에서 안 보인다고 문서가 없는 게 아니라 찾는 위치가 다를 뿐이다.

**`man -k`로 아무것도 안 나오면 "그런 기능이 없다"고 단정하기 쉽다.** 앞서 다뤘듯 실제로는 색인 데이터베이스가 갱신되지 않았을 가능성이 더 크다. 검색 결과가 비어 있을 때는 기능의 부재를 의심하기 전에 `sudo mandb` 실행 여부부터 점검하는 습관이 필요하다.

## 다음 장에서는

Part 1에서 셸 자체를 탐색하는 법을 배웠다면, Part 2부터는 그 안의 텍스트를 처리하는 도구를 다룬다. 다음은 [13장: grep](/post/bashshell/grep-command-search-text-pattern-linux/) — 파일이나 명령 출력에서 원하는 패턴의 줄을 찾아내는 첫 번째 텍스트 처리 도구다.

## 평가 기준

- man 섹션 번호가 무엇을 구분하는지 설명하고, 같은 이름이 여러 섹션에 걸쳐 있을 때 `man 5 passwd`처럼 원하는 섹션을 지정해 조회할 수 있다.
- `man -k`(apropos)와 `man -f`(whatis)의 차이를 구분하고, 정확한 명령어 이름을 몰라도 키워드로 필요한 매뉴얼을 찾을 수 있다.
- `HISTSIZE`(메모리상 히스토리 목록 크기)와 `HISTFILE`/`HISTFILESIZE`(히스토리 파일 위치·크기)의 관계를 구분해 설명할 수 있다.
- `!!`, `!$`, `^old^new^` 같은 히스토리 확장과 Ctrl+R 대화형 역방향 검색을 사용해 이전 명령을 다시 타이핑하지 않고 재사용할 수 있다.
- `history -c`로 지운 히스토리가 왜 파일에는 남아 있을 수 있는지, 세션 히스토리 목록과 히스토리 파일의 동기화 시점으로 설명할 수 있다.

## 참고

- [man(1) - Linux man page (man7.org)](https://man7.org/linux/man-pages/man1/man.1.html)
- [apropos(1) - Linux man page (man7.org)](https://man7.org/linux/man-pages/man1/apropos.1.html)
- [GNU Bash Reference Manual: Bash History Facilities](https://www.gnu.org/software/bash/manual/html_node/Bash-History-Facilities.html)
- [GNU Bash Reference Manual: Bash History Builtins](https://www.gnu.org/software/bash/manual/html_node/Bash-History-Builtins.html)
- [GNU Bash Reference Manual: History Interaction (Event/Word Designators)](https://www.gnu.org/software/bash/manual/html_node/History-Interaction.html)
