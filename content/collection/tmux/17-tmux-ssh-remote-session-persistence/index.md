---
draft: false
slug: tmux-ssh-remote-session-persistence
title: "[Tmux] 17. tmux와 SSH - 원격 세션 유지"
description: "SSH의 ControlMaster/ControlPersist 연결 재사용과 tmux의 세션 보존이 서로 다른 계층이라는 것을 다룹니다. 원격 서버 작업의 표준 워크플로우와, 불안정한 네트워크를 위한 mosh 조합을 실전 예제로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 17
categories:
- Tmux
tags:
- Tmux
- Terminal
- SSH(Secure Shell)
- Networking(네트워킹)
- DevOps
- Session(세션)
- Comparison(비교)
- Configuration(설정)
- OS(운영체제)
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

5부(통합과 비교)의 첫 장이다. 지금까지 배운 모든 tmux 지식은 로컬이든 원격이든 동일하게 적용된다고 여러 챕터에서 언급해 왔다. 이 장은 그 전제를 실제로 검증하며, SSH의 연결 유지 기능과 tmux의 세션 보존이 왜 서로 다른 계층이고 어떻게 함께 쓰이는지를 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [16장: 필수 플러그인 실전](/post/tmux/tmux-resurrect-continuum-yank-essential-plugins/)으로 4부를 마친 뒤, 01–03장에서 배운 서버-클라이언트 구조·세션 관리를 실제 원격 작업 시나리오에 적용한다.

**이 장의 깊이**: **입문**에서 **중급**(SSH 연결 재사용과 tmux 세션 보존의 계층 차이를 설명할 수 있는 수준) 사이를 오간다. **다루지 않는 것**: SSH 키 인증·설정 전반은 이 컬렉션의 범위 밖이며, `ssh_config`의 필요한 옵션만 다룬다. `tmux -CC`처럼 특정 터미널 앱(iTerm2 등)에 종속된 제어 모드도 범위 밖이다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| SSH와 tmux를 각각 따로만 써 온 사람 | 정신 모델, 표준 워크플로우 | 둘을 함께 써서 원격 세션이 끊김에도 살아남는 이유를 이해한다 |
| 매번 SSH 재연결이 느려 답답한 사람 | SSH 연결 유지 옵션, 예시 | `ControlMaster`/`ControlPersist`로 재연결 속도를 개선할 수 있다 |
| 지하철·이동 중처럼 네트워크가 불안정한 환경에서 작업하는 사람 | 비교/트레이드오프(mosh) | SSH 대신 mosh를 조합해야 하는 상황을 판단할 수 있다 |
| 서버가 재부팅됐을 때 세션이 사라지는 이유를 모르는 사람 | 주의사항·함정 | tmux 서버의 생명주기와 SSH 재연결이 별개라는 것을 설명할 수 있다 |

## 정신 모델: SSH와 tmux는 서로 다른 계층의 멀티플렉싱

01장에서 tmux 서버-클라이언트 구조를 다룰 때, tmux가 <strong>터미널 상태</strong> 계층에서 세션·윈도우·패널을 관리한다고 배웠다. SSH의 연결 재사용(멀티플렉싱)은 이와 전혀 다른 계층에서 일어난다 — <strong>네트워크 연결</strong> 계층에서, 이미 맺어진 하나의 TCP 연결 위에 여러 SSH 세션을 얹어 재사용하는 것이다. 즉 SSH 멀티플렉싱은 "연결을 다시 맺는 비용을 아끼는 것"이고, tmux 멀티플렉싱은 "터미널 작업 상태를 보존하는 것"이다. 이 둘은 서로 대체재가 아니라 겹치지 않는 문제를 각자 해결하므로, 함께 쓰는 것이 자연스럽다.

## SSH 연결 유지 옵션

| 옵션 | 설명 |
|---|---|
| `ControlMaster` | 여러 SSH 세션이 하나의 네트워크 연결을 공유하도록 켠다(`yes`로 설정하면 `ControlPath`로 지정한 소켓에서 연결을 기다린다) |
| `ControlPath` | 연결 공유에 쓰는 소켓 경로를 지정한다(`%h`/`%p`/`%r` 같은 자리표시자로 호스트별 경로를 구분하는 것이 권장된다) |
| `ControlPersist` | `ControlMaster`와 함께 쓰며, 첫 연결의 클라이언트가 종료된 뒤에도 마스터 연결을 백그라운드에 남겨 다음 접속을 빠르게 한다 |
| `ServerAliveInterval` | 서버로부터 정해진 시간 동안 응답이 없으면 암호화된 채널로 응답을 요청하는 메시지를 보낸다(불필요한 연결 끊김 방지) |

`ControlMaster`와 `ControlPersist`는 거의 항상 함께 켠다. `ControlMaster`만 켜면 첫 연결의 클라이언트가 종료되는 순간 공유용 마스터 연결도 함께 끊어져 버려, 두 번째 접속부터는 다시 처음부터 연결을 맺어야 한다. `ControlPersist`를 추가로 지정해야 그 마스터 연결이 클라이언트 종료 이후에도 백그라운드에 살아남아, 원격 서버를 자주 오가는 워크플로우에서 실질적인 속도 이득을 얻는다.

## 표준 워크플로우: SSH로 접속해 tmux 세션 유지하기

원격 서버 작업의 기본 패턴은 02–03장에서 배운 것을 그대로 반복한다.

```bash
# 원격 서버에 SSH로 접속
ssh user@remote-server

# (서버 안에서) 이미 세션이 있으면 접속하고, 없으면 새로 만든다
tmux new -A -s work

# 작업 후 detach (prefix 뒤 d) 하고 SSH 연결을 끊어도 세션은 서버에 남는다
# 나중에 다시 접속했을 때
ssh user@remote-server
tmux attach -t work
```

### SSH 재연결 속도 개선하기

```bash
# ~/.ssh/config
Host remote-server
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%h-%p-%r
    ControlPersist 10m
```

이렇게 설정하면 같은 서버에 다시 접속할 때 새 TCP 연결과 인증 과정을 반복하지 않고 기존 연결을 재사용해 훨씬 빠르게 붙을 수 있다. 이 속도 개선은 tmux 세션의 지속성과는 무관하게 SSH 계층에서만 일어나는 이점이다.

### 불안정한 네트워크에서는 mosh 조합

지하철이나 카페처럼 네트워크가 자주 끊기는 환경이라면 SSH 대신 UDP 기반의 `mosh`(mobile shell)를 쓰는 것이 근본적인 해법이다. mosh는 IP가 바뀌거나(와이파이↔셀룰러 전환 등) 잠깐 연결이 끊겨도 세션을 그대로 유지하며, 초기 접속만 SSH로 처리한 뒤 이후 통신은 UDP로 전환한다.

```bash
mosh user@remote-server
# (서버 안에서) tmux 사용은 SSH로 접속했을 때와 완전히 동일하다
tmux new -A -s work
```

mosh는 리눅스·macOS 양쪽에 패키지 매니저(예: `apt install mosh`, `brew install mosh`)로 클라이언트·서버를 각각 설치해야 하며, SSH와 달리 운영체제에 기본 포함돼 있지 않다는 점을 미리 확인해 둔다.

## 비교/트레이드오프

| 구분 | SSH + tmux | mosh + tmux |
|---|---|---|
| 네트워크 요구사항 | 안정적인 TCP 연결 유지 필요 | 패킷 손실·IP 변경에도 견딤(UDP) |
| 지연 체감 | 매 입력이 왕복 확인을 기다림 | 추측 로컬 에코로 입력이 즉시 반영되는 것처럼 느껴짐 |
| 설치·설정 | 대부분 시스템에 기본 포함 | 클라이언트·서버 양쪽에 별도 설치 필요 |
| 적합한 상황 | 유선·안정적인 와이파이 환경 | 이동 중, 네트워크 전환이 잦은 환경 |

이 표의 행들은 결국 "네트워크가 얼마나 믿을 만한가"라는 하나의 질문으로 좁혀진다. 유선이나 안정적인 사내망에서는 SSH만으로 충분하고 mosh를 추가로 설치할 이유가 적지만, 네트워크가 자주 끊기거나 IP가 바뀌는 환경에서는 SSH의 TCP 연결 자체가 자주 죽어버려 `ControlPersist`로도 해결이 안 된다 — 이럴 때는 mosh의 UDP 기반 로밍이 문제의 근본 원인을 없애 준다. 어느 쪽을 쓰든 tmux는 여전히 필요하다 — SSH나 mosh는 연결 자체를 다루는 것이고, 연결이 끊긴 동안 터미널 안의 작업 상태를 보존하는 것은 여전히 tmux의 역할이다.

## 주의사항·함정

**중첩 tmux의 prefix 충돌**: 01장에서 예고했듯, 로컬 tmux 세션 안에서 SSH로 원격 서버에 접속한 뒤 그 서버에서 다시 tmux를 실행하면 같은 prefix 키가 어느 쪽에 전달될지 충돌한다. 구체적인 해결책은 20장(트러블슈팅)에서 다룬다.

**`ControlPersist` 소켓 문제는 SSH의 문제, tmux의 문제가 아니다**: `ControlPath`로 지정한 소켓 디렉터리에 문제가 생기면(디스크 공간 부족, 권한 문제 등) 새 SSH 접속 자체가 막힐 수 있다. 이때 tmux 세션에 접속이 안 된다고 tmux 설정을 의심하기 전에, SSH 연결 재사용 계층에서 문제가 없는지 먼저 확인한다.

**서버 재부팅은 SSH 재연결과 다르다**: SSH는 서버가 재시작돼도 다시 접속하면 그만이지만, 01장에서 다뤘듯 tmux 서버 프로세스는 컴퓨터가 꺼지면 완전히 사라진다. 재부팅 후에는 SSH로 다시 접속해도 이전 tmux 세션은 없다 — 16장에서 다룬 tmux-continuum 같은 도구로 미리 저장해 둬야 복원할 수 있다.

## 흔한 오개념

<strong>"tmux를 쓰면 SSH 연결이 끊기는 일 자체가 없어진다"</strong>는 생각은 틀렸다. tmux는 연결이 끊긴 동안 터미널 작업 상태를 보존할 뿐, SSH 연결 자체의 안정성과는 무관하다. 네트워크가 근본적으로 불안정하다면 mosh 같은 도구가 더 직접적인 해법이다.

<strong>"SSH의 `ControlMaster`/`ControlPersist`는 tmux와 같은 일을 한다"</strong>는 오해도 흔하다. 둘 다 "연결·세션을 유지한다"는 말로 뭉뚱그려지기 쉽지만, 하나는 네트워크 연결 재사용이고 다른 하나는 터미널 상태 보존이라는 서로 다른 계층의 문제를 해결한다.

<strong>"서버가 재부팅되면 tmux 세션도 SSH처럼 자동으로 복구된다"</strong>는 생각도 정확하지 않다. tmux 서버 프로세스 자체가 재부팅과 함께 사라지므로, 세션을 되살리려면 사전에 저장해 둔 상태가 있어야 한다.

## 다음 장에서는

[18장: tmux와 Vim/Neovim 통합](/post/tmux/tmux-vim-neovim-integration-navigator/)에서는 원격 서버에서든 로컬에서든, tmux 패널과 Vim/Neovim 사이를 매끄럽게 오가는 통합 방법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- SSH의 연결 재사용과 tmux의 세션 보존이 서로 다른 계층의 문제라는 것을 설명할 수 있다.
- `ControlMaster`/`ControlPersist`로 SSH 재연결 속도를 개선할 수 있다.
- 네트워크가 불안정한 환경에서 mosh를 SSH의 대안으로 판단할 수 있다.
- 서버 재부팅 후 tmux 세션이 사라지는 이유를 01장의 서버 생명주기 개념으로 설명할 수 있다.
- 원격 접속 문제가 생겼을 때 SSH 계층과 tmux 계층 중 어느 쪽을 먼저 진단해야 하는지 판단할 수 있다.

## 참고 및 출처

1. [ssh_config(5) - OpenBSD Manual](https://man.openbsd.org/ssh_config) — `ControlMaster`·`ControlPath`·`ControlPersist`·`ServerAliveInterval` 공식 설명.
2. [Mosh: the mobile shell](https://mosh.org/) — mosh의 UDP 기반 로밍·재연결 특성.
3. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — tmux 서버-클라이언트 구조 참고.
