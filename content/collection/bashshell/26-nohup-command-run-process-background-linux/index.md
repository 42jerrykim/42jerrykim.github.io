---
draft: false
title: "[Bash Shell] 26. nohup - 로그아웃 후에도 실행 유지"
slug: nohup-command-run-process-background-linux
collection_order: 260
description: "nohup은 SIGHUP을 무시하게 만들고 표준출력을 nohup.out으로 리디렉션하는 두 가지 일만 한다. huponexit·& 만으로는 왜 부족한지, tmux·screen·systemd 사용자 서비스·disown과의 차이를 실전 예제로 다룬다."
date: 2026-03-15
lastmod: 2026-08-24
categories:
- Bash Shell
tags:
- Bash
- Shell(셸)
- Linux(리눅스)
- Terminal
- Command
- Process(프로세스)
- Signal(시그널)
- Daemon(데몬)
- System-Administration(시스템관리)
- Session(세션)
- Systemd
- Tmux
- Fork(포크)
- Automation(자동화)
- File-System(파일시스템)
- nohup
- SIGHUP
- nohup.out
- disown
- huponexit
- 백그라운드
- 데몬화
- 세션분리
- 로그아웃
- Job-Control
- GNU-Coreutils
- POSIX
- 장시간실행
image: "wordcloud.png"
---

## 이 장을 읽기 전에

직전 챕터인 [25장: kill, jobs](/post/bashshell/kill-jobs-commands-process-signal-job-control/)에서는 프로세스에 시그널을 보내 종료하고(`kill`), 현재 셸이 띄운 작업을 포그라운드·백그라운드로 전환하는 법(`jobs`/`fg`/`bg`)을 다뤘다. 이 장은 Part 4(프로세스와 작업 제어)의 마지막 챕터로, "터미널을 닫아도 그 작업이 살아남게 만드는 법"이라는 한 가지 구체적인 문제를 다룬다. 이 장이 전제하는 지식은 `&`로 프로세스를 백그라운드에 보내는 법과, `kill`이 프로세스에 시그널을 전달한다는 사실(25장) 정도다. 별도의 셸 스크립팅 지식은 필요 없다. 난이도는 입문–중급이며, 셸이 작업에 `SIGHUP`을 재전송하는 조건(`huponexit`)까지 이해하려면 약간의 시스템 지식이 필요하다.

**다루지 않는 것**: 시그널이 무엇이고 `kill`로 어떻게 전달하는지는 [25장: kill, jobs](/post/bashshell/kill-jobs-commands-process-signal-job-control/)에서 이미 다뤘다. 스크립트 안에서 시그널을 가로채 정리 작업을 실행하는 `trap`은 33장(종료 코드와 `set -e/-x`, `trap`)에서 다룬다. 터미널 멀티플렉서(`tmux`/`screen`) 자체의 사용법은 이 컬렉션의 범위 밖이며, 이 장에서는 nohup과의 차이를 이해하는 데 필요한 만큼만 비교한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 입문 | 개요+정신 모델, 사용법·옵션, 예시 1–3번 | `nohup 명령 &`으로 터미널을 닫아도 살아남는 백그라운드 작업을 실행하고, `nohup.out`에서 출력을 확인할 수 있다 |
| 중급 | 예시 4–8번, 주의사항·함정 | 출력을 원하는 파일로 직접 리디렉션하고, 이미 실행 중인 작업에 `disown`을 사후 적용하는 법을 nohup과 구분해 쓸 수 있다 |
| 심화 | 주의사항·함정의 `huponexit`, 흔한 오개념, 현대적 대안 비교 | nohup이 세션 분리를 하지 않는다는 것을 설명하고, 상황에 맞게 `tmux`·`systemd` 사용자 서비스 중 무엇을 쓸지 판단할 수 있다 |

## 개요 + 정신 모델

`nohup`(no hang up)은 이름과 달리 매우 좁은 일만 하는 명령이다. 커널이 프로세스에 전달할 수 있는 여러 시그널 중 **`SIGHUP`(시그널 번호 1) 단 하나**를 대상으로, 앞으로 실행할 프로그램이 그 시그널을 무시(`SIG_IGN`)하도록 시그널 처리 방식을 미리 설정한 뒤 원래 명령을 그대로 실행한다. 그리고 표준출력이 터미널에 연결돼 있다면, 터미널이 사라진 뒤에도 출력이 갈 곳이 남아 있도록 `nohup.out` 파일로 자동 리디렉션한다. GNU coreutils 문서와 POSIX 명세 모두 `nohup`의 역할을 정확히 이 두 가지로 규정한다 — SIGHUP을 무시하게 만드는 것, 그리고 터미널로 향하던 표준출력의 목적지를 파일로 바꿔주는 것.

이 정신 모델에서 진짜 중요한 부분은 오히려 nohup이 "하지 않는" 일이다. 전통적인 유닉스 데몬화(daemonization)는 `fork(2)`를 두 번 거쳐 부모와의 관계를 끊고, `setsid(2)`로 새로운 세션의 리더가 되어 제어 터미널 자체와의 연결을 완전히 분리하는 절차를 거친다. `nohup`은 이런 세션 분리를 전혀 하지 않는다 — `nohup`으로 실행한 프로세스는 여전히 원래 세션·프로세스 그룹에 속해 있고, 여전히 같은 제어 터미널을 참조한다. 달라지는 것은 딱 하나, 그 프로세스가 `SIGHUP`이라는 특정 시그널 하나에 반응하지 않도록 설정됐다는 사실뿐이다. 같은 이유로 `nohup`은 프로세스를 백그라운드로 보내지도 않는다. `nohup 명령`만 실행하면 포그라운드에서 그대로 실행되며 터미널을 점유한다. 백그라운드 실행은 셸의 `&` 연산자가 담당하는 완전히 별개의 기능이고, `nohup 명령 &`처럼 둘을 함께 쓰는 것은 관용적으로 자주 붙어 다니는 조합일 뿐 `nohup` 자체의 기능이 아니다. 즉 "SIGHUP 무시"와 "백그라운드 실행"과 "세션 분리(진짜 데몬화)"는 서로 독립적인 세 가지 개념이며, `nohup`은 이 중 첫 번째만 담당한다.

## 사용법 · 옵션

```bash
nohup 명령 [인자...]
```

GNU coreutils `nohup`이 받는 자체 옵션은 사실상 없다시피 하다 — 실행할 명령과 그 인자를 그대로 전달하는 것이 전부다.

| 옵션 | 설명 |
|---|---|
| (없음) | `명령`을 `SIGHUP` 무시 상태로 그대로 실행한다 |
| `--help` | 사용법을 출력하고 종료한다 |
| `--version` | 버전 정보를 출력하고 종료한다 |

`nohup`에는 "출력을 이 파일에 저장하라"는 전용 옵션이 없다. 표준출력이 터미널이면 현재 디렉터리의 `nohup.out`에(권한이 없으면 `$HOME/nohup.out`에) 자동으로 append하거나, 셸의 리디렉션(`>`)으로 직접 지정해야 한다.

## 예시

```bash
# 1. 기본: 터미널을 닫아도 계속 실행되는 백그라운드 작업
nohup ./longrun.sh &

# 2. 자동 생성되는 nohup.out을 실시간으로 확인
tail -f nohup.out

# 3. 출력·에러를 원하는 파일로 직접 지정 (nohup.out 대신)
nohup python train.py > train.log 2>&1 &

# 4. nohup 자체의 실행 실패와 명령의 실행 실패를 종료 코드로 구분
nohup ./존재하지않는스크립트.sh; echo "exit=$?"   # 명령을 못 찾으면 127

# 5. SIGHUP이 실제로 무시 설정됐는지 /proc으로 직접 검증
nohup sleep 300 &
grep SigIgn /proc/$!/status   # 비트마스크에 SIGHUP(1번 비트) 자리가 켜져 있는지 확인

# 6. nohup 없이 시작한 잡을 사후에 SIGHUP 면역으로 전환
sleep 300 &
disown -h %1        # 작업 목록엔 남기되, 셸 종료 시 SIGHUP만 면제

# 7. 원격 서버에서 로그아웃해도 유지되는 배치 작업 실행
ssh build-server 'nohup ./deploy.sh > deploy.log 2>&1 & disown'

# 8. tmux 세션 안에서는 애초에 nohup이 필요 없는 이유를 확인
tmux new -s build   # 세션을 detach해도 세션 자체가 살아있어 프로세스가 안 끊긴다

# 9. 현재 셸의 huponexit 설정 여부 확인
shopt huponexit

# 10. 여러 명령을 하나의 nohup 아래 묶어 순차 실행
nohup bash -c './step1.sh && ./step2.sh' > pipeline.log 2>&1 &
```

## 주의사항 · 함정

**`huponexit`과 SIGHUP 재전송 조건은 셸 설정에 따라 갈린다.** 대화형 로그인 셸이 정상 종료될 때 bash는 자신이 띄운 실행 중·정지된 작업 전체에 `SIGHUP`을 재전송한다(정지된 작업에는 먼저 `SIGCONT`를 보내 신호를 확실히 받게 만든다). 이는 로그인 셸의 기본 동작이며, `shopt -s huponexit`로 이 옵션을 켜면 로그인 셸이 아닌 일반 대화형 셸이 종료될 때도 동일하게 작업들에 `SIGHUP`이 전달된다. 반대로 터미널 에뮬레이터가 강제 종료되거나 SSH 연결이 끊기는 것처럼 터미널이 물리적으로 끊기는 경우는, 셸이 재전송하는 것이 아니라 tty 드라이버가 포그라운드 프로세스 그룹에 직접 `SIGHUP`을 보낸다. 두 경로 중 어느 쪽이든 `nohup`으로 `SIGHUP`을 무시하게 만든 프로세스는 살아남지만, "터미널이 닫히면 항상 셸이 알아서 잡을 정리해준다"거나 반대로 "`nohup` 없는 백그라운드 잡은 절대 안전하지 않다"고 일반화하면 안 된다 — 실제 동작은 로그인 셸 여부와 `huponexit` 설정에 좌우된다.

**`&`만으로는 `SIGHUP`이 처리되지 않는다.** `&`는 프로세스를 백그라운드 작업으로 셸의 작업 테이블에 등록할 뿐, 그 프로세스의 시그널 처리 방식은 전혀 바꾸지 않는다. `SIGHUP`을 무시하도록 만드는 것은 오직 `nohup`(또는 실행 중인 잡에 사후로 적용하는 `disown -h`, 스크립트 안에서 직접 거는 `trap '' HUP`)뿐이다. `cmd &`만 실행한 채 터미널을 닫으면, 위에서 설명한 조건(로그인 셸 종료 또는 tty 끊김)에 따라 그 잡도 `SIGHUP`을 그대로 받을 수 있다.

**`nohup.out`은 권한에 따라 조용히 다른 곳에 쓰이거나, 아예 실행이 거부될 수 있다.** POSIX 명세는 표준출력이 터미널일 때의 리디렉션 우선순위를 명확히 규정한다 — 먼저 현재 디렉터리에 `nohup.out`을 만들려 시도하고, 쓰기 권한이 없으면 `$HOME/nohup.out`으로 폴백하며, 둘 다 만들 수 없으면 아예 명령을 실행하지 않는다. 크론잡처럼 작업 디렉터리가 쓰기 금지된 환경에서는 로그가 예상 못 한 홈 디렉터리에 쌓이거나, 최악의 경우 스크립트가 조용히 아예 실행되지 않을 수 있다. 리디렉션을 직접 지정하지 않은 채 반복 실행하면 `nohup.out`이 계속 append되어 무한정 커질 수도 있다 — 장시간 서비스에는 `> file 2>&1`로 출력 위치를 명시하고 로그 로테이션을 함께 고려해야 한다.

**`disown`으로 사후 처리하면 출력 스트림 문제가 남는다.** 이미 `&`로 백그라운드에 보낸 뒤 `disown` 또는 `disown -h`를 적용하면 `SIGHUP` 문제는 해결되지만, 표준출력이 이미 터미널에 연결된 채로 시작됐다는 사실은 바뀌지 않는다. 터미널이 사라진 뒤 그 프로세스가 여전히 표준출력에 쓰려고 하면 입출력 오류를 만나 죽을 수 있다 — `nohup`이 시작 시점에 자동으로 출력을 파일로 돌려놓는 것과 달리, `disown`은 시그널 처리만 바꿀 뿐 출력 리디렉션까지 대신해주지는 않는다. 처음부터 `nohup ... > file 2>&1 &`로 시작하는 편이 이 함정을 원천적으로 피한다.

## 흔한 오개념

**"`nohup`이 프로세스를 데몬으로 만들어준다"는 오해다.** `nohup`은 `SIGHUP`을 무시하게 만들 뿐, `setsid(2)`로 새 세션을 만들거나 제어 터미널과의 연결을 끊는 세션 분리를 전혀 하지 않는다. 여전히 원래 세션·프로세스 그룹에 속해 있으므로, 엄밀한 의미의 데몬(제어 터미널이 없는 프로세스)과는 다르다. 진짜 데몬이 필요하면 `systemd` 서비스 유닛으로 등록하거나 `setsid` 계열 도구를 쓰는 것이 맞는 방법이다.

**"`nohup 명령 &`에서 백그라운드 실행은 nohup 덕분"이라는 오해다.** 백그라운드로 보내는 것은 셸의 `&` 연산자이지 `nohup`이 아니다. `nohup 명령`만 실행하면 포그라운드에서 실행되며 `Ctrl+C`로 여전히 인터럽트할 수 있다(SIGHUP과 SIGINT는 별개의 시그널이다). 두 기능이 자주 같이 쓰여서 하나처럼 느껴질 뿐, 개념적으로는 독립적이다.

## 다음 장에서는

지금까지 Part 4(프로세스와 작업 제어)에서 `ps`·`top`으로 실행 중인 프로세스를 살펴보고([23장](/post/bashshell/ps-command-process-status-linux/), [24장](/post/bashshell/top-command-realtime-process-monitoring/)), `kill`·`jobs`로 시그널을 보내고 작업을 전환하며([25장](/post/bashshell/kill-jobs-commands-process-signal-job-control/)), 이 장에서 터미널 종료 후에도 작업을 살려두는 법을 배웠다면, [27장: if, test](/post/bashshell/if-test-command-bash-conditional-statements/)부터는 그 지식을 활용해 셸 스크립트 자체를 작성하는 문법을 다루는 Part 5(셸 스크립팅)로 넘어간다. 지금까지는 터미널에 명령을 하나씩 입력해 실행했다면, 다음 장부터는 여러 명령을 조건·반복·함수로 엮어 하나의 스크립트로 자동화하는 법을 다룬다.

## 평가 기준

- `nohup`이 하는 일이 "SIGHUP 무시 설정"과 "표준출력의 nohup.out 리디렉션" 두 가지뿐이라는 것을 설명하고, 세션 분리(진짜 데몬화)와 구분할 수 있다.
- `nohup`·`&`·`disown`이 각각 담당하는 역할(시그널 처리 / 백그라운드 등록 / 사후 SIGHUP 면제)이 서로 독립적이라는 것을 설명할 수 있다.
- 로그인 셸 종료와 `huponexit` 설정에 따라 백그라운드 작업이 `SIGHUP`을 받는 조건이 달라진다는 것을 설명할 수 있다.
- 상황에 맞게 `nohup`, `disown`, `tmux`/`screen`, `systemd` 사용자 서비스 중 어떤 것을 선택할지 판단할 수 있다.
- `nohup.out`의 생성 위치 우선순위(현재 디렉터리 → `$HOME` → 실행 거부)와 그로 인한 실무 함정을 설명할 수 있다.

## 참고

- [nohup(1) - Linux man page](https://man7.org/linux/man-pages/man1/nohup.1.html)
- [nohup - POSIX.1-2017 (The Open Group Base Specifications)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/nohup.html)
- [bash(1) - Linux manual page (SHELL BUILTIN COMMANDS: shopt, disown 절)](https://man7.org/linux/man-pages/man1/bash.1.html)
- [GNU Bash Reference Manual (공식 유지관리자 미러)](https://tiswww.case.edu/php/chet/bash/bashref.html)
