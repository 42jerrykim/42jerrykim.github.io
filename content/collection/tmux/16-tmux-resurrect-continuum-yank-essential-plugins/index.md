---
draft: false
slug: tmux-resurrect-continuum-yank-essential-plugins
title: "[Tmux] 16. 필수 플러그인 실전 - resurrect·continuum·yank"
description: "tmux-resurrect로 세션을 저장·복원하고, tmux-continuum으로 자동 저장·자동 복원을 설정하고, tmux-yank로 클립보드 연동을 보강하는 법을 다룹니다. 각 플러그인의 요구사항과 설정 옵션을 공식 문서 기준으로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 16
categories:
- Tmux
tags:
- Tmux
- Terminal
- Open-Source(오픈소스)
- Automation(자동화)
- Configuration(설정)
- OS(운영체제)
- Session(세션)
- Comparison(비교)
- Keyboard(키보드)
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

4부(자동화·확장)의 마지막 장이다. 15장에서 배운 TPM으로 실제로 설치해 쓰는 대표적인 플러그인 세 가지 — <strong>tmux-resurrect</strong>(세션 저장·복원), <strong>tmux-continuum</strong>(자동 저장·자동 복원), <strong>tmux-yank</strong>(클립보드 연동 보강) — 를 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [15장: 플러그인 생태계와 TPM](/post/tmux/tmux-plugin-manager-tpm-ecosystem/)에서 배운 설치 방법으로 실제 플러그인 세 개를 설치·설정한다. 01장에서 다룬 서버 생명주기, 10장에서 다룬 `set-clipboard`도 전제로 한다.

**이 장의 깊이**: **입문**에서 **중급**(세 플러그인의 의존 관계와 각각의 함정을 진단할 수 있는 수준) 사이를 오간다. **다루지 않는 것**: `tmux-copycat`(정규식 검색)·`tmux-open`(파일·URL 열기) 같은 다른 인기 플러그인은 이름만 언급하고 상세히 다루지 않는다. vim/neovim 세션 복원처럼 `tmux-resurrect`의 고급 옵션은 공식 문서 링크로 대신한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 재부팅할 때마다 세션 구성을 잃어 온 사람 | 정신 모델, tmux-resurrect | 세션을 저장하고 복원할 수 있다 |
| 저장·복원조차 자동으로 맡기고 싶은 사람 | tmux-continuum, 주의사항·함정 | 자동 저장·자동 복원을 설정하고 흔한 함정을 피할 수 있다 |
| 10장의 `set-clipboard`가 터미널 미지원으로 안 됐던 사람 | tmux-yank, 비교/트레이드오프 | 외부 클립보드 프로그램 기반의 대안을 쓸 수 있다 |
| 세 플러그인을 함께 설치하려는 사람 | 예시(설치와 설정) | 의존 관계와 플러그인 목록 순서를 올바르게 구성할 수 있다 |

## 정신 모델: 왜 이 세 플러그인이 "필수"로 꼽히는가

01장에서 다뤘듯 tmux 서버는 컴퓨터가 꺼지면 함께 사라진다. 세션·윈도우·패널을 아무리 정성껏 구성해도 재부팅 한 번이면 전부 날아간다는 뜻이다. <strong>tmux-resurrect</strong>는 이 상태를 파일로 저장했다가 그대로 복원해 이 문제를 정면으로 해결하고, <strong>tmux-continuum</strong>은 그 저장·복원을 사람이 신경 쓰지 않아도 되게 자동화·주기화한다. <strong>tmux-yank</strong>는 성격이 다르다 — 10장에서 다룬 `set-clipboard`가 터미널의 이스케이프 시퀀스 지원에 의존했던 것과 달리, 시스템에 설치된 외부 클립보드 프로그램(`xsel`/`xclip` 등)을 직접 호출해 더 폭넓은 환경에서 클립보드 연동을 보강한다.

## tmux-resurrect: 저장과 복원

이 플러그인의 목표는 단순하다 — 저장하는 순간의 tmux 환경을 최대한 그대로, 손실 없이 재현하는 것이다. 그래서 단순히 창 이름과 명령만이 아니라 레이아웃의 세부 사항, 어떤 세션·윈도우가 활성 상태였는지까지 폭넓게 기록한다.

| 항목 | 내용 |
|---|---|
| 키바인딩 | `prefix` + `Ctrl-s`(저장), `prefix` + `Ctrl-r`(복원) |
| 저장 대상 | 모든 세션·윈도우·패널과 순서, 패널별 작업 디렉터리, 정확한 패널 레이아웃(줌 상태 포함), 활성/이전 세션·윈도우, 세션 그룹, 패널 안에서 실행 중이던 프로그램(선택적으로 vim/neovim 세션까지) |
| 요구사항 | tmux 1.9 이상, `bash`(리눅스·macOS·Cygwin에서 테스트됨) |
| 멱등성 | 이미 존재하는 패널·윈도우는 덮어쓰지 않는다. 유일한 예외는 패널이 하나뿐인 새 tmux를 복원 대상으로 실행했을 때, 그 패널만 덮어쓰는 경우다 |

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-resurrect'
```

`prefix I`로 설치한 뒤 `prefix Ctrl-s`로 지금 상태를 저장하고, 재부팅 후 tmux를 다시 띄우고 `prefix Ctrl-r`로 그대로 복원한다.

## tmux-continuum: 자동 저장과 자동 복원

tmux-continuum은 tmux-resurrect가 설치돼 있어야 동작하는 확장 플러그인이다.

| 기능 | 동작 |
|---|---|
| 지속적 저장 | 15분 간격으로 백그라운드에서 자동 저장한다. 상태바가 켜져 있어야 한다(`status-right`에 건 훅으로 동작하기 때문) |
| 자동 시작 | 컴퓨터·서버가 켜질 때 tmux를 자동으로 실행한다(별도 시스템 설정 필요) |
| 자동 복원 | `set -g @continuum-restore 'on'`을 설정하면 tmux 서버가 <strong>처음 시작될 때만</strong> 마지막 저장 상태를 복원한다. `tmux.conf`를 다시 불러오는 것만으로는 이 복원이 일어나지 않는다 |

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @continuum-restore 'on'
```

공식 문서는 다른 플러그인(주로 테마)이 `status-right`를 덮어쓰면 continuum의 자동 저장이 멈출 수 있다고 경고하며, 이를 피하려면 <strong>continuum을 플러그인 목록의 맨 마지막</strong>에 두라고 권한다.

## tmux-yank: 클립보드 연동 보강

10장에서 다룬 `set-clipboard`가 특정 터미널 에뮬레이터에서 동작하지 않을 때, tmux-yank는 그 터미널의 지원 여부와 무관하게 시스템에 이미 설치된 클립보드 프로그램을 직접 실행해 같은 목적을 달성한다.

| 항목 | 내용 |
|---|---|
| 지원 환경 | 리눅스, macOS, Cygwin, WSL |
| 필요한 외부 프로그램 | 리눅스는 `xsel`(권장) 또는 `xclip`(X), Wayland는 `wl-copy`. macOS 일부 버전은 `reattach-to-user-namespace`. WSL은 `clip.exe`(기본 포함) |
| 일반 모드 키 | `prefix` + `y`(명령줄 내용을 클립보드로), `prefix` + `Y`(현재 패널의 작업 디렉터리를 클립보드로) |
| 카피 모드 키 | `y`(선택 영역을 클립보드로 복사), `Y`(복사와 동시에 명령줄에 붙여넣기까지) |
| 주요 옵션 | `@yank_selection`(리눅스의 `primary`/`secondary`/`clipboard` 중 선택), `@yank_action`(`copy-pipe`로 바꾸면 10장에서 다룬 `copy-selection-and-cancel`처럼 카피 모드를 바로 종료하지 않고 유지) |

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tmux-yank'
```

## 예시

### 세 플러그인 한 번에 설치하기

```bash
# ~/.tmux.conf
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-yank'
set -g @continuum-restore 'on'
set -g @plugin 'tmux-plugins/tmux-continuum'   # 자동 저장 훅 충돌을 피해 맨 마지막에 둔다

run '~/.tmux/plugins/tpm/tpm'
```

설정 후 `tmux source ~/.tmux.conf`로 반영하고 `prefix I`로 세 플러그인을 한 번에 설치한다.

### 클립보드 연동 방식 비교해 보기

10장에서 `set-clipboard on`이 터미널 미지원으로 동작하지 않았다면, 같은 텍스트를 이번에는 tmux-yank로 복사해 본다.

```text
카피 모드 진입(prefix [) → 영역 선택 → y (tmux-yank가 xsel/xclip 등으로 직접 클립보드에 전달)
```

## 비교/트레이드오프

클립보드로 내용을 보내는 방법은 10장의 `set-clipboard`와 이 장의 tmux-yank, 두 가지다.

| 구분 | `set-clipboard`(10장) | tmux-yank |
|---|---|---|
| 동작 방식 | 터미널의 이스케이프 시퀀스(OSC 계열)를 통해 전달 | 시스템에 설치된 외부 프로그램(`xsel`/`xclip` 등)을 직접 호출 |
| 의존성 | 터미널 에뮬레이터가 해당 시퀀스를 지원해야 함 | 클립보드 프로그램이 시스템에 설치돼 있어야 함 |
| 설치 필요 여부 | 별도 설치 없이 옵션만 켜면 됨 | 플러그인 설치와 경우에 따라 외부 프로그램 설치가 필요 |
| 적합한 상황 | 지원되는 최신 터미널을 쓰는 경우 | 터미널 지원 여부와 무관하게 확실히 동작하는 방법이 필요한 경우 |

## 주의사항·함정

**continuum 플러그인 순서**: 다른 플러그인(특히 테마)이 `status-right`를 덮어쓰면 continuum의 자동 저장 훅이 무력화된다. 플러그인 목록에서 continuum을 항상 마지막에 두는 것이 공식적으로 권장되는 회피책이다.

**"reload하면 자동 복원되겠지"라는 착각**: continuum의 자동 복원은 tmux 서버가 <strong>처음</strong> 시작될 때만 일어난다. 이미 떠 있는 서버에서 `tmux source-file`로 설정을 다시 불러와도 복원은 트리거되지 않는다. 테스트하려면 서버 자체를 완전히 내렸다가 새로 띄워야 한다.

**tmux-yank가 조용히 실패하는 경우**: 필요한 외부 클립보드 프로그램(`xsel`/`xclip`/`reattach-to-user-namespace` 등)이 시스템에 없으면 tmux-yank는 겉으로는 별다른 오류 없이 그냥 동작하지 않을 수 있다. 클립보드 연동이 안 될 때는 이 프로그램이 실제로 설치돼 있는지부터 확인한다.

## 흔한 오개념

<strong>"tmux-continuum만 설치하면 자동으로 저장·복원된다"</strong>는 생각은 틀렸다. continuum은 독립 플러그인이 아니라 tmux-resurrect에 의존하는 확장이므로, resurrect가 먼저 설치돼 있어야 한다.

<strong>"설정 파일을 reload하면 continuum이 즉시 복원해 준다"</strong>는 오해도 흔하다. 자동 복원은 오직 tmux 서버가 새로 시작될 때만 일어나며, 이미 실행 중인 서버에 설정을 다시 적용하는 것으로는 트리거되지 않는다.

<strong>"tmux-yank와 10장의 set-clipboard는 결국 같은 방식이다"</strong>는 생각도 정확하지 않다. `set-clipboard`는 터미널의 이스케이프 시퀀스에 의존하고, tmux-yank는 시스템의 외부 클립보드 프로그램을 직접 호출한다는 점에서 메커니즘 자체가 다르다.

## 다음 장에서는

[17장: tmux와 SSH - 원격 세션 유지](/post/tmux/tmux-ssh-remote-session-persistence/)부터는 5부(통합과 비교)로 넘어가, 지금까지 배운 모든 것을 원격 서버 작업에 실제로 적용하는 법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- tmux-resurrect가 저장·복원하는 대상과 그 멱등성 규칙을 설명할 수 있다.
- tmux-continuum이 tmux-resurrect에 의존하며, 자동 복원이 서버 최초 시작 시에만 일어난다는 것을 설명할 수 있다.
- continuum을 플러그인 목록 마지막에 둬야 하는 이유를 설명할 수 있다.
- tmux-yank와 10장의 `set-clipboard`가 서로 다른 메커니즘으로 동작한다는 것을 구분할 수 있다.
- 세 플러그인을 TPM으로 함께 설치하고 설정할 수 있다.

## 참고 및 출처

1. [tmux-plugins/tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect) — 공식 README, 저장·복원 대상, 요구사항, 멱등성.
2. [tmux-plugins/tmux-continuum](https://github.com/tmux-plugins/tmux-continuum) — 공식 README, 자동 저장·복원 조건, 알려진 문제(플러그인 순서).
3. [tmux-plugins/tmux-yank](https://github.com/tmux-plugins/tmux-yank) — 공식 README, 지원 환경, 키바인딩, 옵션.
