---
draft: false
slug: pipe-operator-linux-command-chaining
title: "[Bash Shell] 19. 파이프(|) - 명령어 연결"
description: "파이프(|)는 커널이 제공하는 익명 버퍼로 한 프로세스의 표준출력을 다른 프로세스의 표준입력에 직접 연결하며, 연결된 명령들이 순차가 아니라 동시에 실행된다는 정신 모델과 파이프라인 종료 코드·PIPESTATUS·버퍼링 관련 함정을 예제로 정리합니다."
date: 2026-03-15
lastmod: 2026-08-23
collection_order: 190
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- Automation(자동화)
- Process
- File-System
- Pipeline
- Stdout
- Stdin
- Guide(가이드)
- Tutorial(튜토리얼)
- Reference(참고)
- Beginner
- Pitfalls(함정)
- Best-Practices
- Error-Handling(에러처리)
- Pipe(파이프)
- Pipelining(파이프라이닝)
- Buffering(버퍼링)
- FIFO(선입선출)
- Kernel
- Concurrency(동시성)
- Parallel-Computing(병렬컴퓨팅)
- Fork(포크)
- IPC
- Pipefail
- Exit-Status
image: "wordcloud.png"
---

**파이프**(`|`)는 한 명령의 <strong>표준 출력(stdout)</strong>을 다음 명령의 <strong>표준 입력(stdin)</strong>에 직접 연결한다. 중간에 파일을 거치지 않고 여러 명령을 이어 붙여 하나의 데이터 흐름을 만들 때 쓴다.

## 이 장을 읽기 전에

직전 챕터인 [18장: sort, uniq, wc](/post/bashshell/sort-uniq-wc-commands-sort-count-lines/)까지가 Part 2(텍스트 처리)였다. `grep`·`sed`·`awk`·`cut`·`tr`·`sort`·`uniq`·`wc`는 각자 입력 스트림 하나를 받아 변형된 출력 스트림 하나를 내보내는 독립된 도구였고, 지금까지는 이들을 한 번에 하나씩만 실행했다. 이 장은 Part 3(파이프라인과 입출력)의 첫 챕터로, Part 2에서 배운 개별 명령들을 실제로 연결해 "필터를 이어 붙인 파이프라인"을 만드는 방법을 다룬다. 즉 이 장 자체가 새 명령을 소개하지는 않는다 — 이미 아는 명령들을 조합하는 셸의 메커니즘을 다룬다.

난이도는 입문–중급이다. 표준입출력(stdin/stdout)이 무엇인지 감각적으로만 알면 따라올 수 있고, 뒤쪽 "주의사항·함정"·"흔한 오개념"은 셸이 프로세스를 어떻게 띄우는지(서브셸)까지 이해해야 완전히 소화된다.

**다루지 않는 것**: 명령의 출력을 **파일**로 보내거나 파일에서 읽어오는 방법(`>`, `<`, `>>`, Here Document)은 [20장: 리다이렉션](/post/bashshell/io-redirection-linux-bash-tutorial/)에서 다룬다. 파이프와 리다이렉션은 자주 섞어 쓰지만 서로 다른 메커니즘이다 — 이 장 "핵심 개념"에서 둘의 차이를 짚는다. 이름 있는 파이프(FIFO, `mkfifo`)처럼 프로세스 간 통신을 위한 고급 기법도 이 장의 범위 밖이다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요 + 정신 모델, 핵심 개념의 사용법·리디렉션과의 차이 | `\|`로 두 명령을 이어 쓸 수 있고, 파이프와 리디렉션을 구분할 수 있다 |
| 중급 | 핵심 개념 전체, 예시 | 3단 이상의 파이프라인을 구성하고 stderr가 파이프를 타지 않는다는 점을 안다 |
| 심화 | 주의사항·함정, 흔한 오개념 | 파이프라인 종료 코드의 함정과 버퍼링 방식 변화를 실무 스크립트에 반영할 수 있다 |

## 개요 + 정신 모델

파이프는 **커널이 제공하는 익명 버퍼**다. 셸이 `cmd1 | cmd2`를 만나면 커널에 `pipe(2)` 시스템 콜로 읽기 끝(read end)과 쓰기 끝(write end) 한 쌍의 파일 디스크립터를 요청하고, `cmd1`의 표준 출력을 그 쓰기 끝에, `cmd2`의 표준 입력을 읽기 끝에 연결한다. 이 버퍼에는 이름도 없고 디스크에 흔적도 남기지 않는다 — 두 프로세스가 살아 있는 동안만 커널 메모리 안에 존재하다가, 양쪽 다 파일 디스크립터를 닫으면 사라진다.

여기서 가장 중요하지만 자주 오해되는 사실 하나: 파이프로 연결된 명령들은 **순차적으로 실행되지 않는다.** `cmd1 | cmd2`를 실행하면 셸은 `cmd1`과 `cmd2`를 각각 별도의 프로세스로 **동시에** 띄운다. `cmd1`이 출력을 전부 만든 뒤에 `cmd2`가 시작되는 것이 아니라, `cmd1`이 한 줄을 내보내는 순간 `cmd2`가 이미 그 줄을 소비하기 시작할 수 있다. 이 동시 실행을 가능하게 하는 것이 바로 파이프 버퍼다 — 버퍼가 비어 있으면 읽는 쪽(`cmd2`)이 대기하고, 버퍼가 가득 차면 쓰는 쪽(`cmd1`)이 대기한다. 이 상호 대기(블로킹)가 곧 두 프로세스 사이의 자연스러운 흐름 제어(flow control)이며, `cmd1`이 대용량 파일 전체를 메모리에 올리지 않고도 `cmd2`에 스트리밍으로 넘길 수 있는 이유다.

## 핵심 개념

### 사용법

```bash
명령1 | 명령2 [| 명령3 ...]
```

- `명령1`의 stdout이 `명령2`의 stdin으로 전달된다. 세 개 이상 이어 붙이면 각 단계가 앞 단계의 출력을 입력으로 받는 필터 체인이 된다.
- 표준 오류(stderr)는 파이프를 타지 않고 그대로 터미널로 나간다. stderr까지 다음 명령에 넘기려면 `2>&1`로 stderr를 stdout에 먼저 합친 뒤 파이프해야 한다(자세한 내용은 [20장: 리다이렉션](/post/bashshell/io-redirection-linux-bash-tutorial/)).

### 파이프의 정체: 파일 디스크립터 한 쌍

셸 입장에서 파이프는 특별한 문법이 아니라, `cmd1`과 `cmd2`를 `fork`하기 전에 미리 만들어 둔 두 개의 파일 디스크립터를 각 자식 프로세스의 표준 출력/표준 입력 자리에 연결(`dup2`)하는 절차다. 리눅스에서 파이프 버퍼의 기본 용량은 16페이지, 즉 4KB 페이지 기준 65,536바이트(64KB)다.

> "Since Linux 2.6.11, the pipe capacity is 16 pages (i.e., 65,536 bytes in a system with a page size of 4096 bytes)." — `pipe(7)`, Linux man-pages

이 값은 `fcntl(2)`의 `F_GETPIPE_SZ`/`F_SETPIPE_SZ`로 조회·조정할 수 있지만, 일반적인 셸 사용에서 직접 다룰 일은 거의 없다. 알아 둘 실전 의미는 하나다 — 버퍼가 유한하므로, `cmd2`가 느리게 소비하면 `cmd1`은 버퍼가 빌 때까지 강제로 대기하게 된다는 것.

### 리디렉션과의 차이

- **리디렉션** (`>`, `<`): 명령 ↔ **파일** 간 입출력 연결.
- **파이프** (`|`): 명령 ↔ **다른 명령**(의 표준입출력) 간 연결.

둘은 같은 줄에서 함께 쓸 수 있다: `명령1 < input.txt | 명령2 > output.txt`처럼 입력은 파일에서 읽고, 중간 처리는 파이프로 넘기고, 최종 결과만 파일에 쓰는 조합이 실무에서 흔하다.

## 예시

```bash
# 프로세스 목록에서 nginx 관련 줄만 걸러낸다
ps aux | grep nginx

# 로그에서 대소문자 무관 error 줄만 세기 (grep → wc 2단 파이프)
cat app.log | grep -i error | wc -l

# 정렬 후 중복을 제거하고, 등장 횟수 기준 내림차순 재정렬 (sort → uniq → sort 3단 파이프)
sort list.txt | uniq -c | sort -rn

# 긴 출력을 페이지 단위로 보기
ls -l | less

# 최근 명령 이력에서 ssh 관련 줄만 최근 20개 범위로 보기
history | tail -20 | grep ssh

# /etc/passwd의 첫 번째 필드(계정명)만 뽑아 정렬
cut -d: -f1 /etc/passwd | sort

# sed로 치환한 결과를 grep으로 다시 확인
sed 's/foo/bar/' notes.txt | grep bar

# 파이프와 리디렉션을 함께 사용: 파일에서 읽고 파이프로 처리한 뒤 파일에 저장
sort < list.txt | uniq > result.txt

# stderr는 파이프를 타지 않으므로, 존재하지 않는 경로의 오류 메시지는 grep에 걸리지 않는다
ls /no/such/directory | grep "No such"
# 2>&1로 먼저 합쳐야 오류 메시지도 grep 대상이 된다
ls /no/such/directory 2>&1 | grep "No such"
```

`cmd1 | cmd2 | cmd3` 형태의 데이터 흐름을 그림으로 보면 다음과 같다. 화살표는 "완료 후 전달"이 아니라 "흐르는 대로 전달"이다 — `cmd1`이 아직 실행 중인 동안에도 이미 버퍼에 쓰인 만큼은 `cmd2`가 바로 읽어 처리하기 시작한다.

```mermaid
flowchart LR
    cmd1Proc["cmd1 프로세스"] -->|"stdout 쓰기"| buf1(("커널 파이프 버퍼</br>최대 64KB"))
    buf1 -->|"stdin 읽기"| cmd2Proc["cmd2 프로세스"]
    cmd2Proc -->|"stdout 쓰기"| buf2(("커널 파이프 버퍼</br>최대 64KB"))
    buf2 -->|"stdin 읽기"| cmd3Proc["cmd3 프로세스"]
    cmd3Proc -->|"stdout"| terminalOut["터미널 화면"]
```

세 프로세스(`cmd1Proc`, `cmd2Proc`, `cmd3Proc`)는 커널이 동시에 스케줄링하는 별도의 프로세스이며, 두 개의 파이프 버퍼가 그 사이에서 흐름을 조절하는 완충 지대 역할을 한다.

## 주의사항·함정

**파이프라인의 종료 코드는 기본적으로 마지막 명령의 것만 반영된다.** `$?`는 파이프라인 전체가 아니라 가장 오른쪽 명령의 종료 코드만 담는다. 그래서 중간 명령이 실패해도 마지막 명령이 성공하면 파이프라인 전체가 "성공"으로 보일 수 있다.

```bash
grep "존재하지않는패턴" app.log | wc -l
echo "종료 코드: $?"   # grep이 매치 실패(1)여도, wc가 성공(0)했으므로 0이 출력된다
```

GNU Bash Reference Manual은 이를 다음과 같이 규정한다.

> "The exit status of a pipeline is the exit status of the last command in the pipeline, unless the `pipefail` option is enabled." — GNU Bash Reference Manual, "Pipelines"

Bash는 이 한계를 두 가지 방법으로 보완한다. 하나는 배열 변수 `PIPESTATUS`로, 직전 파이프라인을 구성한 각 명령의 종료 코드를 순서대로 담고 있다(`${PIPESTATUS[0]}`이 첫 명령, `${PIPESTATUS[1]}`이 두 번째 명령의 코드). 다른 하나는 `set -o pipefail`로, 켜두면 파이프라인 중 하나라도 실패했을 때 그 실패 코드를 파이프라인 전체의 종료 코드로 채택한다 — 자동화 스크립트에서 중간 실패를 놓치지 않으려면 사실상 필수에 가까운 옵션이며, [33장: 종료 코드와 set -e/-x, trap](/post/bashshell/exit-status-set-trap-bash-error-handling/)에서 `set -e`·`trap`과 함께 자세히 다룬다.

```bash
echo "PIPESTATUS: ${PIPESTATUS[@]}"

set -o pipefail
grep "존재하지않는패턴" app.log | wc -l
echo "pipefail 켠 뒤 종료 코드: $?"   # grep의 실패(1)가 파이프라인 전체 코드로 채택된다
```

`pipefail`은 POSIX 표준이 아니라 bash·zsh·ksh가 제공하는 확장이다. POSIX가 규정하는 기본 동작은 항상 마지막 명령의 종료 코드만 사용하는 쪽이며, `dash`처럼 `/bin/sh`로 흔히 쓰이는 최소 POSIX 셸에는 `pipefail`이 없다. 스크립트 상단에 `#!/bin/sh`를 쓰면서 `set -o pipefail`을 기대하면 셸에 따라 옵션 자체가 없다는 오류가 날 수 있다 — 이 옵션이 필요하면 셔뱅을 `#!/bin/bash`로 명시해야 한다.

**파이프로 연결하면 출력 버퍼링 방식이 줄 단위에서 블록 단위로 바뀐다.** 대부분의 표준 라이브러리는 출력 대상이 터미널(tty)인지 아닌지에 따라 버퍼링 전략을 자동으로 바꾼다. 터미널에 직접 출력할 때는 한 줄이 완성될 때마다 즉시 내보내는 **줄 단위 버퍼링**을 쓰지만, 출력이 파이프나 파일로 연결되면 성능을 위해 수 KB 단위로 모았다가 한 번에 내보내는 **완전 버퍼링**으로 자동 전환된다. 그 결과 `producer | consumer` 파이프라인에서 `producer`가 로그를 실시간으로 찍고 있어도, `consumer` 쪽에서는 버퍼가 찰 때까지 아무것도 보이지 않다가 한꺼번에 쏟아지는 것처럼 보일 수 있다. 실시간성이 필요하면 `stdbuf -oL`로 강제로 줄 단위 버퍼링을 지정하거나(`stdbuf -oL producer | consumer`), 프로그램이 자체적으로 제공하는 플러시 옵션(`grep --line-buffered`, `python3 -u`, `awk`의 `fflush()`)을 쓴다.

**이름 있는 파이프(FIFO)와 혼동하지 않는다.** 이 장에서 다룬 `|`는 이름이 없는 익명 파이프로, 그 줄의 파이프라인이 끝나면 사라진다. `mkfifo`로 만드는 이름 있는 파이프는 파일시스템에 이름을 가진 채로 남아 서로 다른 시점에 실행된 프로세스끼리도 데이터를 주고받을 수 있다는 점에서 다른 도구다.

## 흔한 오개념

<strong>"`cmd1`이 완전히 끝난 뒤에야 `cmd2`가 시작된다"</strong>는 가장 흔한 오해다. 실제로는 앞서 "개요 + 정신 모델"에서 설명했듯 두 명령이 동시에 시작되고, 파이프 버퍼를 매개로 데이터가 흐르는 대로 처리된다. `cmd1 | cmd2`를 "cmd1의 결과 파일을 cmd2가 나중에 읽는 것"으로 상상하면, 왜 `tail -f app.log | grep ERROR`가 로그 파일이 끝나기를 기다리지 않고 실시간으로 계속 결과를 출력하는지를 설명할 수 없다. 파이프는 배치가 아니라 스트리밍이다.

<strong>"파이프 앞뒤 명령이 같은 셸 변수 공간을 공유한다"</strong>도 자주 틀리는 지점이다. Bash는 다중 명령 파이프라인의 각 명령을 별도의 서브셸(자식 프로세스)에서 실행한다.

> "Each command in a multi-command pipeline, where pipes are created, is executed in its own subshell, which is a separate process." — GNU Bash Reference Manual, "Pipelines"

이 때문에 `cat file.txt | while read -r line; do count=$((count+1)); done; echo "$count"`처럼 파이프 오른쪽의 `while` 루프 안에서 변수를 갱신해도, 그 `while`은 서브셸에서 실행되므로 서브셸이 끝나는 순간 갱신한 값과 함께 사라진다 — 파이프라인이 끝난 뒤 부모 셸에서 `$count`를 출력하면 갱신되지 않은 값(대개 빈 값)이 나온다. 이 문제를 피하려면 파이프 대신 프로세스 치환(`while read -r line; do ...; done < <(cat file.txt)`)을 쓰거나, bash 4 이상에서 `shopt -s lastpipe`로 파이프라인의 마지막 명령만 현재 셸에서 실행되게 설정한다.

## 다음 장에서는

[20장: 리다이렉션](/post/bashshell/io-redirection-linux-bash-tutorial/)에서는 명령의 표준 입출력을 다른 명령이 아니라 **파일**로 연결하는 `>`·`>>`·`<`·Here Document를 다룬다. 이 장이 "명령 ↔ 명령"을 잇는 법이었다면, 다음 장은 "명령 ↔ 파일"을 잇는 법이다. 두 메커니즘을 조합하면 이 장의 마지막 예시(`sort < list.txt | uniq > result.txt`)처럼 훨씬 유연한 데이터 처리 파이프라인을 구성할 수 있다.

## 평가 기준

- 파이프(`|`)가 두 프로세스의 표준입출력을 연결하는 커널의 익명 버퍼라는 점을 설명하고, 리디렉션(`>`, `<`)과 무엇이 다른지 구분할 수 있다.
- 파이프로 연결된 명령들이 순차가 아니라 동시에 실행되며, 파이프 버퍼가 그 사이의 흐름 제어(블로킹)를 담당한다는 점을 설명할 수 있다.
- 파이프라인의 종료 코드(`$?`)가 기본적으로 마지막 명령의 것만 반영한다는 함정을 알고, `PIPESTATUS`와 `set -o pipefail`로 이를 보완하는 방법을 적용할 수 있다.
- 파이프로 연결되면 출력 버퍼링이 줄 단위에서 블록 단위로 바뀌어 실시간성이 떨어질 수 있다는 점과, `stdbuf`·프로그램별 플러시 옵션으로 완화하는 방법을 설명할 수 있다.
- 파이프라인의 각 명령이 별도 서브셸에서 실행되어 변수를 공유하지 않는다는 점을 알고, `while read` 루프에서 이 문제를 피하는 대안(프로세스 치환, `lastpipe`)을 선택할 수 있다.

## 참고

- [Pipelines — GNU Bash Reference Manual](https://doc.guix.gnu.org/bash/latest/en/html_node/Pipelines.html)
- [pipe(7) — Linux manual page](https://man7.org/linux/man-pages/man7/pipe.7.html)
- [Shell Command Language: Pipelines — POSIX.1-2017](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_09)
