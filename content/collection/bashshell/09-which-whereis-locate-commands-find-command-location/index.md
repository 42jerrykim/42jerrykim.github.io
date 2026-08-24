---
draft: false
slug: which-whereis-locate-commands-find-command-location
title: "[Bash Shell] 09. which, whereis, locate - 명령어와 파일 찾기"
description: "PATH에서 실행 파일 경로만 찾는 which, 실행파일·소스코드·매뉴얼 위치를 함께 찾는 whereis, 미리 만들어둔 파일명 데이터베이스로 시스템 전체를 빠르게 검색하는 locate의 사용법과 역할 차이, updatedb로 갱신되는 DB의 최신성 문제까지 다룬다."
date: 2026-03-15
lastmod: 2026-08-23
collection_order: 90
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- File-System
- Automation(자동화)
- PATH
- Environment
- Database(데이터베이스)
- Configuration(설정)
- Documentation(문서화)
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Quick-Reference
- Troubleshooting(트러블슈팅)
- How-To
- Tips
- Beginner
- Searching(탐색)
- which
- whereis
- locate
- updatedb
- mlocate
- plocate
- 실행파일탐색
- 명령어탐색
- 파일검색
image: "wordcloud.png"
---

`which`는 **PATH를 실시간으로 훑어** 실행 파일 경로를 찾고, `whereis`는 **실행파일·소스·매뉴얼을 한꺼번에** 찾으며, `locate`는 **미리 만들어둔 파일명 데이터베이스**로 시스템 전체를 순식간에 검색한다. 셋 다 "무언가를 찾는다"는 점은 같지만, 찾는 방식과 찾는 대상이 완전히 다르다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [8장: ln](/post/bashshell/ln-command-hard-symbolic-links-linux/)에서 하드링크·심볼릭 링크로 같은 파일을 여러 경로에서 가리키는 법을 다룬 뒤 이어진다. 지금까지 파일을 만들고(`touch`), 옮기고 지우고(`cp`/`mv`/`rm`), 링크를 걸어(`ln`) 파일 하나가 여러 경로를 가질 수 있다는 것까지 배웠다면, 이 장에서는 반대로 "이름만 알고 있는 파일이나 명령어가 실제로 어느 경로에 있는지"를 찾아내는 도구로 넘어간다.

**이 장의 깊이**: **입문** 난이도다. 세 명령어 모두 옵션 수가 적고 사용법이 단순해, 각 명령이 정확히 무엇을 검색 대상으로 삼는지 구분하는 데 초점을 맞춘다. **다루지 않는 것**: 셸이 명령어를 찾을 때 실제로 거치는 내부 순서(해시 테이블, 빌트인, PATH 탐색 순서)와 `type`/`hash`/`command`로 그 과정을 정확히 들여다보는 법은 [10장: PATH, type, hash, command](/post/bashshell/path-type-hash-command-shell-command-lookup/)에서 다룬다. `locate`가 참조하는 데이터베이스를 직접 설계하거나 튜닝하는 고급 관리자 작업(`updatedb.conf` 세부 설정 등)도 이 장의 범위 밖이다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|------|---------|---------|
| 명령어 경로를 지금 당장 찾아야 하는 사람 | "사용법·옵션"의 which·locate 부분, "예시"의 "which로 실행 파일 찾기"·"locate로 시스템 전체 검색" | `which`로 지금 실행될 명령의 경로를, `locate`로 파일명 일부만 알고 있는 파일을 빠르게 찾는다 |
| 세 명령의 차이와 함정까지 이해하려는 사람 | "개요+정신 모델"부터 "주의사항·함정", "흔한 오개념" 전체 | which·whereis·locate가 서로 다른 정신 모델로 동작한다는 것을 설명하고, locate의 DB 최신성 문제와 which의 한계를 파악해 상황에 맞는 도구를 고른다 |

---

## 개요 + 정신 모델

세 명령어는 "명령어/파일을 찾는다"는 목적은 같지만, **무엇을 조회하는가**가 근본적으로 다르다. `which`는 지금 이 셸 세션의 `PATH` 환경변수에 나열된 디렉터리를 앞에서부터 차례로 뒤져, 인자로 준 이름과 일치하는 첫 번째 실행 파일의 경로를 알려준다. 즉 `which`의 세계는 오직 `PATH` 하나뿐이고, "지금 이 이름을 입력하면 셸이 어떤 파일을 실행할 것인가"라는 질문에 답하도록 설계됐다(정확히는 "POSIX 표준을 엄격히 따르는 셸이라면 무엇을 실행할지"이며, 이 전제가 뒤에서 다룰 함정의 원인이 된다).

`whereis`는 `PATH`가 아니라 **미리 정해진 표준 디렉터리 목록**(`/bin`, `/usr/bin`, `/usr/share/man` 등)을 뒤진다는 점에서 출발부터 다르다. 검색 대상도 실행 파일 하나가 아니라 **실행 파일(binary) + 매뉴얼 페이지(manual) + 소스 코드(source)** 세 종류를 동시에 찾아 보여준다. 그래서 `whereis grep`을 실행하면 `/usr/bin/grep`(실행 파일)과 `/usr/share/man/man1/grep.1.gz`(매뉴얼)가 한 줄에 함께 출력될 수 있다. `which`가 "지금 실행될 파일 하나"를 묻는 질문이라면, `whereis`는 "이 프로그램과 관련된 파일들이 시스템 어디에 흩어져 있는가"를 묻는 질문이다.

`locate`는 앞의 둘과 아예 다른 층위에서 동작한다. `which`·`whereis`는 명령을 실행하는 그 순간 디렉터리를 직접 읽어(라이브 조회) 결과를 만들지만, `locate`는 파일시스템을 전혀 건드리지 않고 **`updatedb`가 미리 만들어둔 파일명 데이터베이스**(보통 `/var/lib/mlocate/mlocate.db`)만 검색한다. 이 데이터베이스에는 검색 대상 디렉터리 트리 전체의 파일 경로가 스냅샷으로 저장되어 있어, 실제로 디스크를 순회하는 `find`보다 비교할 수 없이 빠르다. 대신 그 대가로 데이터베이스가 마지막으로 갱신된 시점 이후의 변화(새 파일 생성, 파일 삭제)는 즉시 반영되지 않는다 — 이 트레이드오프가 뒤에서 다룰 가장 흔한 함정의 원인이다.

## 사용법 · 옵션

### which — PATH에서 실행 파일

```bash
which [-a] 명령...
```

| 옵션 | 설명 |
|------|------|
| `-a`, `--all` | PATH에서 찾은 **모든** 일치 경로를 출력한다(기본값은 첫 번째 일치만 출력) |

`which`는 의도적으로 매우 단순한 도구다. 옵션이 사실상 `-a` 하나뿐이며, 실행 파일을 찾으면 그 경로를 표준 출력에, 못 찾으면 아무 것도 출력하지 않고 0이 아닌 종료 코드를 반환한다.

### whereis — 바이너리·매뉴얼·소스

```bash
whereis [-bmsu] [-B 디렉터리... -f] [-M 디렉터리... -f] [-S 디렉터리... -f] 이름...
```

| 옵션 | 설명 |
|------|------|
| `-b` | 실행 파일(binary)만 검색한다 |
| `-m` | 매뉴얼 페이지(manual)만 검색한다 |
| `-s` | 소스 코드(source)만 검색한다 |
| `-u` | 요청한 각 유형의 항목이 정확히 하나가 아닌(없거나 여러 개인) "특이한" 결과만 보여준다 — 예: `whereis -m -u *`로 매뉴얼 페이지가 없는 실행 파일을 찾는 시스템 점검에 쓴다 |
| `-B 디렉터리...` `-f` | 실행 파일을 검색할 디렉터리를 직접 지정한다(`-f`로 목록의 끝과 이름 인자의 시작을 구분) |
| `-M 디렉터리...` `-f` | 매뉴얼 페이지를 검색할 디렉터리를 직접 지정한다 |
| `-S 디렉터리...` `-f` | 소스 코드를 검색할 디렉터리를 직접 지정한다 |

옵션을 하나도 주지 않으면 `whereis`는 기본적으로 실행 파일·매뉴얼·소스 세 가지를 모두 검색한다.

### locate — 파일명 데이터베이스 검색

```bash
locate [옵션] 패턴...
```

| 옵션 | 설명 |
|------|------|
| `-i`, `--ignore-case` | 패턴과 파일명 모두 대소문자를 구분하지 않는다 |
| `-r`, `--regexp` | 패턴을 glob이 아니라 **정규식**으로 해석한다 |
| `-c`, `--count` | 매칭된 파일명 대신 총 매칭 개수만 출력한다 |
| `-n N`, `--limit N` | 결과를 최대 N개까지만 출력한다 |
| `-e`, `--existing` | `locate`를 실행하는 **지금 이 순간 실제로 존재하는** 파일만 결과에 포함한다(DB에는 있지만 이미 삭제된 파일을 걸러낼 때 유용) |
| `-b`, `--basename` | 전체 경로가 아니라 파일명(마지막 구성 요소)만 패턴과 비교한다 |
| `-w`, `--wholename` | 전체 경로를 패턴과 비교한다(기본값) |

`locate` 자체는 데이터베이스를 읽기만 하고 갱신하지 않는다. 데이터베이스를 만들고 최신 상태로 유지하는 것은 별도 명령인 `updatedb`의 역할이다.

## 예시

### which로 실행 파일 찾기

```bash
# python 실행 파일의 경로 확인
which python

# PATH에 여러 python이 있다면 전부 출력(우선순위 확인에 유용)
which -a python

# 존재하지 않는 명령이면 아무것도 출력하지 않고 종료 코드 1을 반환
which no_such_command; echo $?
```

### whereis로 관련 파일 한 번에 찾기

```bash
# ls의 실행 파일과 매뉴얼 페이지를 함께 확인
whereis ls

# grep의 실행 파일 경로만 확인
whereis -b grep

# awk의 매뉴얼 페이지 위치만 확인
whereis -m awk

# /usr/bin 디렉터리에서 매뉴얼 페이지가 없는 실행 파일 점검
cd /usr/bin && whereis -m -u *
```

### locate로 시스템 전체 검색

```bash
# 확장자가 .conf인 파일을 시스템 전체에서 검색
locate "*.conf"

# 대소문자 구분 없이 readme 관련 파일 검색
locate -i readme

# /etc 아래의 .conf 파일만 정규식으로 검색
locate -r '^/etc/.*\.conf$'

# 매칭된 개수만 확인
locate -c "*.log"

# 방금 만든 파일은 DB에 없어 검색되지 않는다 → updatedb로 DB를 먼저 갱신
touch /tmp/brand_new_file.txt
locate brand_new_file.txt        # 아무것도 안 나올 수 있다
sudo updatedb
locate brand_new_file.txt        # 갱신 후에는 나온다

# -e로 DB에는 있지만 이미 삭제된 파일을 결과에서 제외
locate -e old_report.pdf
```

## 주의사항 · 함정

**`locate`는 실시간 검색이 아니라 스냅샷 검색이다.** `locate`가 참조하는 `mlocate`/`plocate` 데이터베이스(기본 경로 `/var/lib/mlocate/mlocate.db`)는 `updatedb`가 만든 시점의 파일시스템 상태를 담고 있을 뿐이다. `updatedb`는 보통 cron이 매일 한 번 실행하도록 설정되어 있어(Debian 계열 `updatedb(8)` 문서: "updatedb is usually run daily by cron(8) to update the default database."), 방금 만든 파일은 다음 갱신 전까지 `locate` 결과에 나타나지 않는다. 급하게 방금 생성한 파일을 찾아야 한다면 `locate` 대신 `find`를 쓰거나, `sudo updatedb`로 즉시 갱신한 뒤 다시 검색해야 한다. 참고로 일부 최신 배포판은 전통적인 `mlocate` 대신 더 빠른 `plocate`를 채택했는데, `plocate`는 "largely argument-compatible with mlocate(1), but is significantly faster"(plocate 공식 문서)라 옵션 사용법은 거의 같지만 완전히 동일하지는 않다.

**`whereis`와 `which`는 검색 범위와 대상 자체가 다르다.** `which`는 오직 현재 셸의 `PATH`만 보고 실행 파일 하나의 경로를 찾는 반면, `whereis`는 `PATH`와 무관하게 고정된 표준 디렉터리 집합에서 실행 파일·소스·매뉴얼 페이지까지 함께 찾는다. 그래서 `PATH`에 없는 디렉터리에 설치된 프로그램이라도 `whereis`의 표준 검색 경로에 포함되어 있으면 찾아낼 수 있고, 반대로 `PATH`의 특이한 디렉터리(표준 위치가 아닌 곳)에 있는 실행 파일은 `which`는 찾아도 `whereis`는 못 찾을 수 있다. 두 명령을 "거의 같은 것"으로 혼동하면 안 되는 이유다.

**`which`는 셸 빌트인이나 alias를 제대로 찾지 못할 수 있다.** `which`는 `/usr/bin/which`처럼 셸 바깥에서 실행되는 독립된 외부 프로그램이라, 현재 셸 프로세스 안에만 존재하는 alias·함수·빌트인 명령의 정의를 애초에 들여다볼 방법이 없다. Debian `which(1)` 매뉴얼도 이 동작을 "which returns the pathnames of the files (or links) which would be executed in the current environment, had its arguments been given as commands in a strictly POSIX-conformant shell"라고 설명하는데, 여기서 "엄격히 POSIX를 따르는 셸"이라는 전제 자체가 실제 우리가 쓰는 bash(alias·함수·빌트인이 얹힌)와는 다를 수 있다는 뜻이다. 예를 들어 `cd`처럼 셸 빌트인으로만 존재하는 명령을 `which cd`로 조회하면 아무 경로도 못 찾거나 오해의 소지가 있는 결과를 낼 수 있다. 이 한계를 정확히 보완해 빌트인·alias·함수·PATH를 모두 구분해서 알려주는 도구가 다음 장에서 다룰 `type`이다.

## 흔한 오개념

**"`which some_command`가 아무것도 출력하지 않으면 그 명령은 시스템에 없는 것이다"라는 오해.** 실제로는 "PATH 어디에도 실행 파일로 존재하지 않는다"는 뜻일 뿐이다. `cd`, `alias`, 사용자가 셸 함수로 정의한 명령처럼 애초에 파일이 아니라 셸 내부에만 존재하는 명령은 `which`가 찾지 못해도 셸에서는 멀쩡히 동작한다. "명령이 없다"와 "PATH에 실행 파일로 없다"를 구분해야 하며, 정확한 판정은 다음 장의 `type`으로 해야 한다.

**"`locate` 결과에 나온 파일은 지금도 실제로 존재한다"는 오해.** `locate`는 스냅샷 데이터베이스를 검색하므로, DB가 만들어진 뒤 삭제된 파일도 다음 `updatedb` 갱신 전까지는 여전히 결과에 나타난다. 이미 지운 파일이 검색 결과에 계속 나와 당황할 수 있는데, `locate -e`(`--existing`)를 쓰면 지금 이 순간 실제로 파일시스템에 존재하는 항목만 걸러서 보여준다.

## 다음 장에서는

이 장에서는 `which`/`whereis`/`locate`로 명령어와 파일의 위치를 찾는 도구를 다뤘다면, 다음 장에서는 셸이 애초에 명령어를 어떤 순서로 찾는지 그 근거(PATH)를 다룬다 — [10장: PATH, type, hash, command](/post/bashshell/path-type-hash-command-shell-command-lookup/)에서 `type`으로 빌트인·alias·함수·실행 파일을 정확히 구분하고, `hash`로 셸이 이미 찾아둔 경로를 캐싱하는 원리를 살펴본다.

## 평가 기준

- `which`·`whereis`·`locate`가 각각 무엇을(PATH·표준 디렉터리 집합·파일명 DB) 검색 대상으로 삼는지 설명할 수 있다.
- 상황에 맞게 세 명령 중 하나를 선택할 수 있다 — 지금 실행될 명령 경로 확인은 `which`, 관련 파일(실행파일+매뉴얼+소스) 전체 확인은 `whereis`, 시스템 전체에서 파일명으로 빠르게 검색은 `locate`.
- `locate`가 실시간 검색이 아니라 `updatedb`가 만든 스냅샷 DB를 조회한다는 것을 설명하고, 방금 만든 파일이 검색되지 않을 때 `updatedb` 또는 `find`로 대응할 수 있다.
- `which`가 셸 빌트인·alias·함수를 찾지 못할 수 있는 이유를 설명하고, 더 정확한 판정이 필요할 때 `type`으로 넘어갈 판단을 할 수 있다.

## 참고

- [which(1) - Debian manpages (debianutils)](https://manpages.debian.org/testing/debianutils/which.1.en.html)
- [whereis(1) - Linux manual page](https://man7.org/linux/man-pages/man1/whereis.1.html)
- [locate(1) - Linux manual page](https://man7.org/linux/man-pages/man1/locate.1.html)
- [updatedb(8) - Debian manpages (mlocate)](https://manpages.debian.org/testing/mlocate/updatedb.8.en.html)
- [plocate(1) - Debian manpages](https://manpages.debian.org/testing/plocate/plocate.1.en.html)
