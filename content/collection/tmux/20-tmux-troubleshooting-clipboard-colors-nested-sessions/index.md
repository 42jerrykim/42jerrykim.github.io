---
draft: false
slug: tmux-troubleshooting-clipboard-colors-nested-sessions
title: "[Tmux] 20. 트러블슈팅 - 클립보드·색상·중첩 세션"
description: "색상이 깨지거나 클립보드 연동이 안 되거나 중첩 세션에서 prefix가 안 먹히는 세 가지 흔한 문제를 계층별로 진단합니다. default-terminal·terminal-overrides·escape-time을 실전 체크리스트로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 20
categories:
- Tmux
tags:
- Tmux
- Terminal
- Troubleshooting(트러블슈팅)
- Debugging(디버깅)
- SSH(Secure Shell)
- Configuration(설정)
- Best-Practices
- Deep-Dive
- Vim
- Session(세션)
- Keyboard(키보드)
- OS(운영체제)
- Productivity(생산성)
- Workflow(워크플로우)
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

6부(실전과 마무리)의 첫 장이다. 이 장은 새로운 개념을 소개하지 않는다. 대신 지금까지 여러 챕터에서 예고만 하고 미뤄 왔던 세 가지 흔한 문제 — 색상이 깨지는 것, 클립보드 연동이 안 되는 것, 중첩된 세션에서 prefix가 엉뚱하게 동작하는 것 — 을 실제로 진단하고 고치는 법을 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [19장: 대안 도구 비교](/post/tmux/tmux-vs-screen-zellij-wezterm-comparison/)로 5부를 마친 뒤, 01장(서버-클라이언트 구조)·05장(prefix)·10장(클립보드)·17장(SSH)에서 예고된 문제들을 실제로 해결한다.

**이 장의 깊이**: **중급**이다. 새 개념 없이, 이미 배운 것을 진단이라는 다른 각도로 재구성한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| tmux에서 색이 이상하게 보이는 사람 | 색상이 깨질 때 | 문제가 터미널 앱·`$TERM`·tmux 설정 중 어디에 있는지 좁힐 수 있다 |
| 10·16장을 따라 했는데도 클립보드가 안 되는 사람 | 클립보드가 안 될 때 | 진단 체크리스트로 원인을 하나씩 배제할 수 있다 |
| 01·17장에서 예고된 중첩 세션 문제를 실제로 겪은 사람 | 중첩 세션에서 prefix가 안 먹힐 때 | 안쪽/바깥쪽 중 어느 세션이 반응하는지 확인하고 대응할 수 있다 |
| 팀의 tmux 문제를 대신 진단해 줘야 하는 사람 | 정신 모델, 전체 | 증상만 듣고도 어느 계층부터 확인해야 할지 판단할 수 있다 |

## 정신 모델: 증상이 아니라 계층을 진단한다

지금까지 이 컬렉션은 tmux를 여러 계층으로 나눠 설명해 왔다 — 서버-클라이언트 구조(01장), 키 입력 처리(05장), 클립보드 연동(10장), SSH와의 관계(17장). 문제가 생겼을 때도 이 계층 구분을 그대로 진단 도구로 쓸 수 있다. "화면이 이상하다"는 증상 하나만 보고 tmux 설정을 뒤지기 전에, 그 증상이 터미널 앱 계층·tmux 설정 계층·원격 연결 계층 중 어디서 비롯됐는지부터 좁히는 것이 훨씬 빠르다.

## 색상이 깨질 때

색상 문제는 거의 항상 세 곳 중 하나(또는 여러 곳)의 불일치에서 온다. 이 세 계층이 서로 맞아떨어져야만 의도한 색이 화면에 그대로 나타나므로, 하나라도 어긋나면 색이 밋밋해지거나 아예 엉뚱한 색으로 보인다.

| 확인 대상 | 무엇을 봐야 하는가 |
|---|---|
| 터미널 에뮬레이터 자체 | 256색·트루컬러(RGB)를 실제로 지원하는 앱인지 |
| 바깥쪽 `$TERM` | tmux를 실행하기 전 셸의 `$TERM`이 터미널 앱의 실제 능력과 맞는지 |
| tmux의 `default-terminal` | 공식 문서는 이 값이 반드시 `screen`, `tmux` 또는 그 파생값이어야 tmux가 올바르게 동작한다고 명시한다 |
| `terminal-features`/`terminal-overrides` | 터미널이 지원하는 기능(`256`, `RGB`, `clipboard` 등)을 tmux에게 알려주거나, 개별 terminfo 항목을 직접 오버라이드하는 옵션 |

```bash
# 세 계층을 순서대로 확인한다
echo $TERM                              # 바깥쪽 터미널이 보고하는 TERM
tmux show-options -g default-terminal   # tmux 안에서 쓰는 TERM
tput colors                             # 지금 셸이 인식하는 색상 수
```

```tmux
# ~/.tmux.conf 예시: 트루컬러 지원을 tmux에 명시적으로 알려주기
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"
```

## 클립보드가 안 될 때

클립보드 연동은 경로가 두 가지(터미널 이스케이프 시퀀스 방식과 외부 프로그램 방식)라서 오히려 어디서 막혔는지 헷갈리기 쉽다. 10장과 16장에서 다룬 두 가지 경로를 체크리스트로 되짚는다.

| 확인 순서 | 질문 |
|---|---|
| 1 | `set-clipboard`가 `on` 또는 `external`로 설정돼 있는가?(`tmux show-options -g set-clipboard`) |
| 2 | 지금 쓰는 터미널 에뮬레이터가 클립보드 이스케이프 시퀀스를 실제로 지원하는가? |
| 3 | tmux-yank를 쓴다면, 리눅스의 `xsel`/`xclip`, macOS의 `reattach-to-user-namespace` 같은 외부 클립보드 프로그램이 설치돼 있는가? |
| 4 | SSH로 원격 서버에 있다면, 그 서버 안에서도 위 1–3이 모두 성립하는가? |

## 중첩 세션에서 prefix가 안 먹힐 때

01장과 17장에서 예고했던 문제다 — 로컬 tmux 세션 안에서 SSH로 원격 서버에 접속한 뒤 그 서버에서 다시 tmux를 실행하면, prefix(기본 `Ctrl+b`)를 눌렀을 때 바깥쪽(로컬) 세션이 먼저 소비해 버린다.

```text
prefix 뒤 prefix           → 05장에서 배운 send-prefix 기본 바인딩으로,
                              바깥쪽 prefix를 안쪽 세션에 리터럴로 전달한다
```

더 근본적인 해결은 05장에서 배운 `prefix2` 옵션으로 안쪽 세션의 보조 prefix를 다르게 두는 것이다.

```tmux
# 안쪽(원격) 서버의 tmux.conf
set -g prefix2 C-a
bind-key C-a send-prefix -2
```

## 주의사항·함정

**`escape-time`이 길어서 생기는 Vim 지연**: Vim에서 `Esc`를 눌렀는데 반응이 느리게 느껴진다면, tmux가 `escape-time` 옵션만큼 다음 키 입력을 기다리며 이스케이프 시퀀스인지 판단하고 있는 것일 수 있다. `set -sg escape-time 10`처럼 짧게 줄이는 것이 커뮤니티에서 흔히 쓰이는 해결책이다.

**`terminal-overrides`와 `terminal-features`를 혼동하지 않는다**: `terminal-features`는 `256`·`RGB`·`clipboard`처럼 표준화된 기능 클래스를 선언하는 옵션이고, `terminal-overrides`는 개별 terminfo 항목 값을 직접 덮어쓰는 옵션이다. 이 둘은 서로 다른 문제를 위한 것이라 하나로 되는 걸 다른 하나로 시도하면 헛수고가 된다.

**중첩 세션에서는 어느 쪽이 반응하는지 먼저 확인한다**: 문제를 진단할 때 로컬 tmux.conf를 고쳐야 할지 원격 서버의 tmux.conf를 고쳐야 할지부터 헷갈리기 쉽다. `Ctrl+b`를 눌렀을 때 어느 쪽 상태바가 반응하는지 먼저 관찰하면 어느 설정 파일을 고쳐야 할지 명확해진다.

## 흔한 오개념

<strong>"tmux 설정만 고치면 색상 문제는 항상 해결된다"</strong>는 생각은 틀렸다. `default-terminal`이나 `terminal-overrides`를 아무리 정확히 맞춰도, 바깥쪽 터미널 에뮬레이터 자체가 그 색상 모드를 지원하지 않으면 아무 효과가 없다.

<strong>"클립보드는 `set-clipboard`만 켜면 항상 된다"</strong>는 오해도 10장에서 이미 짚었지만, 실전에서는 위 체크리스트의 네 항목을 모두 통과해야 한다는 것을 다시 강조할 필요가 있다.

<strong>"중첩 세션에서 prefix를 두 번 누르면 항상 안쪽에 전달된다"</strong>는 생각도 정확하지 않다. `send-prefix`가 기본 바인딩(prefix 두 번)에 실제로 연결돼 있어야 하며, 누군가 이 기본 바인딩을 다른 용도로 바꿔 놓았다면 기대한 대로 동작하지 않는다.

## 다음 장에서는

[21장: 실전 워크플로우 설계와 로드맵](/post/tmux/tmux-workflow-design-roadmap/)에서는 이 컬렉션의 마지막 장으로, 지금까지 배운 것을 실제 시나리오별 레이아웃으로 종합한다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- 색상 문제를 터미널 앱·`$TERM`·tmux 설정 세 계층으로 나눠 진단할 수 있다.
- 클립보드 연동 문제를 네 단계 체크리스트로 좁혀 나갈 수 있다.
- 중첩 세션에서 어느 쪽 tmux가 prefix를 소비하는지 확인하고 `prefix2`로 대응할 수 있다.
- `escape-time`이 Vim의 체감 반응 속도에 미치는 영향을 설명할 수 있다.
- `terminal-features`와 `terminal-overrides`의 용도 차이를 구분할 수 있다.

## 참고 및 출처

1. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — `default-terminal`·`terminal-features`·`terminal-overrides`·`escape-time`·`prefix2` 공식 설명.
2. [tmux/tmux](https://github.com/tmux/tmux) — tmux 공식 소스 저장소.
