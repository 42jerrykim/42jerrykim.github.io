---
draft: false
slug: tmux-command-line-scripting-send-keys
title: "[Tmux] 13. tmux 커맨드라인과 스크립팅 - send-keys, run-shell"
description: "tmux 명령을 셸 스크립트로 조합해 세션을 자동으로 부트스트랩하는 법을 다룹니다. send-keys로 패널에 명령을 주입하고, run-shell·if-shell로 외부 명령을 실행하거나 조건 분기하는 패턴을 실전 예제로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 13
categories:
- Tmux
tags:
- Tmux
- Terminal
- Shell(셸)
- Automation(자동화)
- DevOps
- Comparison(비교)
- Session(세션)
- Case-Study
- SSH(Secure Shell)
- Productivity(생산성)
- Workflow(워크플로우)
- Best-Practices
- Deep-Dive
- Education(교육)
- Curriculum(커리큘럼)
- Tutorial(튜토리얼)
- Guide(가이드)
- How-To
- Tips
- Reference(참고)
- Beginner
- Advanced
- Documentation(문서화)
- Cheatsheet(치트시트)
- Quick-Reference
image: "wordcloud.png"
---

4부(자동화·확장)의 첫 장이다. 지금까지 배운 모든 tmux 명령은 사실 인터랙티브하게 입력할 때만 쓰는 것이 아니라, 셸 스크립트 안에서 그대로 호출할 수 있는 평범한 커맨드라인 도구다. 이 장은 <strong>send-keys</strong>로 패널에 명령을 자동으로 입력시키고, <strong>run-shell</strong>/<strong>if-shell</strong>로 외부 명령을 실행하거나 조건에 따라 분기하는 법을 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [12장: 세션 그룹과 다중 클라이언트](/post/tmux/tmux-session-groups-multiple-clients-pairing/)로 3부(고급 조작)를 마친 뒤, 4부(자동화·확장)의 첫 장으로서 지금까지 손으로 입력해 온 명령을 스크립트로 옮긴다.

**이 장의 깊이**: **입문**에서 **중급**(부트스트랩 스크립트를 직접 작성하고 조건 분기까지 다룰 수 있는 수준) 사이를 오간다. **다루지 않는 것**: 세션·윈도우 레이아웃을 프로젝트별로 저장하고 불러오는 전용 도구(tmuxinator·tmuxifier)는 14장에서, 플러그인 생태계는 15–16장에서 각각 다룬다. 이 장은 tmux 자체 명령만으로 스크립팅하는 원리에 집중한다 — 사실 14장의 도구들도 결국 이 장에서 배우는 명령 조합을 자동화한 것이다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| tmux 명령을 대화형으로만 써 온 사람 | 정신 모델, 명령과 옵션, 예시 | tmux 명령을 셸 스크립트 안에서 그대로 호출할 수 있다는 것을 이해한다 |
| 매번 같은 세션·윈도우 구성을 손으로 반복하는 사람 | 예시(부트스트랩 스크립트) | 세션 생성부터 명령 실행까지 한 스크립트로 자동화할 수 있다 |
| send-keys를 써봤는데 명령이 실행되지 않아 당황한 사람 | 주의사항·함정 | Enter를 명시적으로 보내야 한다는 것을 이해하고 실수를 피할 수 있다 |
| 원격 서버 작업 환경을 스크립트로 표준화하려는 사람 | 예시(run-shell), 흔한 오개념 | SSH로 접속한 서버에서도 같은 부트스트랩 스크립트를 재사용할 수 있다 |

## 정신 모델: tmux 명령은 셸에서 호출 가능한 평범한 CLI

`tmux new-session`, `tmux send-keys`처럼 지금까지 터미널에 직접 입력해 온 모든 명령은, 사실 `git`이나 `curl`과 다를 것 없는 평범한 커맨드라인 도구 호출이다. 즉 이 명령들을 셸 스크립트 안에 순서대로 나열하면, "세션을 만들고 → 윈도우를 나누고 → 각 패널에 필요한 명령을 실행시키는" 전체 과정을 사람이 한 단계씩 입력하지 않고 스크립트 한 번 실행으로 재현할 수 있다. 14장에서 다루는 tmuxinator·tmuxifier 같은 도구들은 결국 이 원리를 설정 파일 하나로 감싸 편하게 만든 것일 뿐, 근본적으로 하는 일은 이 장에서 배우는 명령 조합과 같다.

## 명령과 옵션

| 명령 | 주요 옵션 | 설명 |
|---|---|---|
| `send-keys`(`send`) | `-l`, `-H`, `-N 반복횟수`, `-t 대상패널` | 지정한 패널에 키 입력을 순서대로 보낸다. `-l`은 키 이름 해석 없이 문자 그대로 보내고, `-H`는 16진수로 지정한 문자를 보낸다 |
| `run-shell`(`run`) | `-b`(백그라운드), `-C`(tmux 명령 실행), `-d 초`, `-E`(stderr를 stdout으로), `-c 시작경로` | `/bin/sh`로 셸 명령을 실행한다(`-C`를 주면 셸 명령 대신 tmux 명령을 실행). 추가 인자는 `#{1}`, `#{2}`로 셸 명령 안에서 참조할 수 있다 |
| `if-shell`(`if`) | `-b`(백그라운드 실행), `-F`(형식 문자열 평가) | `/bin/sh`로 실행한 셸 명령이 성공하면 첫 번째 tmux 명령을, 실패하면 두 번째 명령을 실행한다 |
| `wait-for`(`wait`) | `-S`(신호 보내기), `-L`(채널 잠금) | 여러 tmux 명령·스크립트 사이의 실행 순서를 동기화하는 저수준 도구. 복잡한 부트스트랩 스크립트에서 "이 작업이 끝날 때까지 기다렸다가 다음 단계로" 같은 조율이 필요할 때 쓴다 |

## 예시

### 세션을 만들고 명령을 자동으로 주입하기

`send-keys`로 문자열만 보내면 패널에 그 글자가 입력만 될 뿐 실행되지 않는다. 실행까지 시키려면 `Enter`를 별도 인자로 명시해야 한다.

```bash
# 이름을 붙인 세션을 백그라운드로 만들고
tmux new -s dev -d

# 그 세션의 패널에 명령을 입력한 뒤 Enter를 별도로 보내 실제로 실행시킨다
tmux send-keys -t dev 'cd ~/project && vim .' Enter
```

### 세션·윈도우·패널을 한 스크립트로 부트스트랩하기

03–04장에서 손으로 하던 세션·윈도우·패널 구성을, 순서대로 나열한 tmux 명령만으로 재현할 수 있다.

```bash
#!/bin/sh
tmux new -s dev -d -n editor
tmux send-keys -t dev:editor 'vim .' Enter

tmux new-window -t dev -n server
tmux send-keys -t dev:server 'npm run dev' Enter

tmux split-window -t dev:server -h
tmux send-keys -t dev:server.1 'tail -f logs/app.log' Enter

tmux attach -t dev
```

### run-shell로 외부 명령 실행하고 인자 넘기기

```bash
# 인자 foo, bar는 스크립트 안에서 #{1}, #{2}로 참조된다
tmux run-shell 'notify-send.sh #{1} #{2}' "빌드 완료" "프로젝트 A"
```

### if-shell로 조건에 따라 분기하기

03장에서 배운 `has-session`을 셸 명령으로 활용하면, 세션이 있으면 접속하고 없으면 새로 만드는 스크립트를 짤 수 있다.

```bash
tmux if-shell "tmux has-session -t dev 2>/dev/null" \
  "tmux attach -t dev" \
  "tmux new -s dev"
```

## 비교/트레이드오프

매번 손으로 조작하는 것과 스크립트로 부트스트랩하는 것은 상황에 따라 유불리가 갈린다.

| 구분 | 손으로 매번 조작 | 스크립트로 부트스트랩 |
|---|---|---|
| 초기 비용 | 없음(바로 시작) | 스크립트를 작성하는 시간이 든다 |
| 재현성 | 같은 구성을 다시 만들려면 순서를 기억해야 한다 | 스크립트 하나로 항상 동일하게 재현된다 |
| 유지보수 | 구성이 바뀌면 그때그때 손으로 조정 | 스크립트를 한 번만 고치면 이후 모두 반영 |
| 적합한 상황 | 일회성 작업, 아주 단순한 구성 | 반복되는 프로젝트 환경, 팀원 간 표준화 |

## 주의사항·함정

**`send-keys`에서 Enter를 빼먹는 실수**: 가장 흔한 실수는 명령 문자열만 `send-keys`로 보내고 `Enter`를 빠뜨리는 것이다. 이 경우 패널에 글자만 입력된 채 실행되지 않아 "명령이 안 먹힌다"고 오인하기 쉽다.

**`run-shell`이 기본적으로 결과를 뷰 모드로 보여주며 대기한다는 것**: `-b`(백그라운드) 없이 `run-shell`을 쓰면, 명령이 끝날 때까지 그 표준 출력을 뷰 모드 화면에 띄운 채 기다린다. 오래 걸리는 명령을 이 방식으로 실행하면 화면이 멈춘 것처럼 느껴질 수 있으므로, 백그라운드 처리가 필요하면 `-b`를 명시한다.

**`if-shell`의 셸 명령은 `/bin/sh`로 실행된다**: bash 전용 문법(배열, `[[ ]]` 등)을 `if-shell`의 조건식에 그대로 쓰면 `/bin/sh`가 이를 이해하지 못해 실패할 수 있다. 조건식은 POSIX 셸 문법으로 작성하는 것이 안전하다.

## 흔한 오개념

<strong>"send-keys는 명령을 실행까지 시켜 준다"</strong>는 생각은 정확하지 않다. `send-keys`는 어디까지나 키 입력을 흉내 낼 뿐이며, 셸이 그 입력을 실행하려면 `Enter`까지 별도로 보내야 한다.

<strong>"run-shell은 tmux 명령만 실행할 수 있다"</strong>는 오해도 있다. 기본 동작은 일반 셸 명령을 실행하는 것이고, tmux 명령을 실행하려면 `-C` 옵션을 명시해야 한다.

<strong>"이런 자동화는 tmuxinator 같은 전용 도구가 있어야만 가능하다"</strong>는 생각도 틀렸다. 이 장에서 다룬 명령만으로도 동일한 자동화를 스크립트로 직접 짤 수 있으며, 14장에서 다루는 도구들은 이 방식을 더 편리한 설정 파일로 감싼 것일 뿐이다.

## 다음 장에서는

[14장: tmuxinator와 tmuxifier - 프로젝트 레이아웃 관리](/post/tmux/tmuxinator-tmuxifier-project-layout-management/)에서는 이 장에서 손으로 짠 부트스트랩 스크립트를, 프로젝트별 설정 파일로 저장하고 불러오는 전용 도구를 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- tmux 명령이 셸 스크립트 안에서 그대로 호출 가능한 CLI라는 것을 설명할 수 있다.
- `send-keys`로 패널에 명령을 주입하고, `Enter`를 명시해 실제로 실행시킬 수 있다.
- `run-shell`과 `if-shell`의 차이(무조건 실행 vs 조건에 따른 분기)를 설명할 수 있다.
- 여러 명령을 조합해 세션·윈도우·패널을 한 번에 구성하는 부트스트랩 스크립트를 작성할 수 있다.
- `run-shell`을 백그라운드로 돌려야 하는 상황을 판단할 수 있다.

## 참고 및 출처

1. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — `send-keys`·`run-shell`·`if-shell`·`wait-for` 공식 옵션과 설명, 예제.
2. [tmux/tmux](https://github.com/tmux/tmux) — tmux 공식 소스 저장소.
