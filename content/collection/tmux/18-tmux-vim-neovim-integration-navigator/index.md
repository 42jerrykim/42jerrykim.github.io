---
draft: false
slug: tmux-vim-neovim-integration-navigator
title: "[Tmux] 18. tmux와 Vim/Neovim 통합"
description: "vim-tmux-navigator로 tmux 패널과 Vim/Neovim 분할 창 사이를 같은 방향키로 매끄럽게 오가는 법을 다룹니다. bind-key -n과 if-shell로 프로세스를 감지하는 동작 원리를 07·10·13장 개념과 연결해 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 18
categories:
- Tmux
tags:
- Tmux
- Terminal
- Vim
- Keyboard(키보드)
- Automation(자동화)
- IDE(Integrated Development Environment)
- Deep-Dive
- Comparison(비교)
- Open-Source(오픈소스)
- Configuration(설정)
- Productivity(생산성)
- Workflow(워크플로우)
- Best-Practices
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

04장에서 패널 사이를 `select-pane`으로 옮겨 다니는 법을 배웠지만, 그 패널 안에서 Vim이 실행 중이라면 이야기가 달라진다. Vim은 `:split`으로 만든 자신의 분할 창을 오갈 때 별도의 단축키(`Ctrl+w` 계열)를 쓰기 때문이다. 이 장은 이 두 세계의 경계를 지워, 하나의 키 조합으로 tmux 패널과 Vim 분할 창을 매끄럽게 오가게 해 주는 <strong>vim-tmux-navigator</strong>를 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [17장: tmux와 SSH](/post/tmux/tmux-ssh-remote-session-persistence/)에 이어, 07장(키바인딩)·10장(카피 모드 키 테이블)·13장(if-shell)에서 배운 개념을 하나의 실전 통합 사례로 묶는다.

**이 장의 깊이**: **중급**(if-shell 기반 프로세스 감지 로직을 읽고 커스터마이징할 수 있는 수준)이다. **다루지 않는 것**: Vim/Neovim 자체의 분할 창 사용법이나 다른 에디터(Emacs 등)와의 통합은 범위 밖이다. 이 장은 tmux 쪽에서 무엇을 어떻게 설정해야 하는지에 집중한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| Vim 분할과 tmux 패널을 서로 다른 키로 오가 온 사람 | 정신 모델, 설치, 예시 | 하나의 키 조합으로 둘을 매끄럽게 오갈 수 있다 |
| 이 플러그인이 어떻게 동작하는지 궁금한 사람 | 동작 원리 | `bind-key -n`과 `if-shell`이 어떻게 조합되는지 설명할 수 있다 |
| 카피 모드에서도 같은 방향키를 쓰고 싶은 사람 | 예시(카피 모드 바인딩) | `copy-mode-vi` 키 테이블에도 같은 매핑을 걸 수 있다 |
| tmux 자체 분할과 에디터 내장 터미널 중 고민하는 사람 | 비교/트레이드오프 | 상황에 맞게 둘 중 하나를 선택할 수 있다 |

## 정신 모델: 패널 경계를 지우는 것

`vim-tmux-navigator`(Mislav Marohnić의 설정을 정리한 플러그인)가 하려는 일은 단순하다 — `Ctrl+h`/`j`/`k`/`l`을 눌렀을 때, 지금 포커스가 Vim 안이면 Vim의 분할 이동으로, tmux 패널의 경계라면 tmux의 `select-pane`으로 자연스럽게 이어지게 만드는 것이다. 사용자 입장에서는 지금 이동하는 대상이 Vim의 내부 분할인지 tmux의 패널인지 신경 쓸 필요가 없어진다.

## 동작 원리: if-shell로 프로세스를 감지한다

이 플러그인의 tmux 쪽 설정은 새로운 메커니즘이 아니라, 07장에서 배운 <strong>root 테이블 바인딩</strong>(`bind-key -n`)과 13장에서 배운 <strong>if-shell</strong>을 조합한 실전 사례다. 핵심은 `$is_vim`이라는 셸 조건이다 — 지금 패널에서 실행 중인 프로세스를 `ps`로 확인해, 그 이름이 vim·neovim·fzf 계열 패턴과 일치하면 "이 패널은 Vim이 쓰고 있다"고 판단한다. 판단 결과에 따라 `if-shell`이 분기한다: Vim이 맞으면 그 키 입력을 13장에서 배운 `send-keys`로 그대로 전달해 Vim 자신의 매핑이 처리하게 하고, 아니면 tmux의 `select-pane`을 실행해 패널을 이동한다. 사람이 매번 "지금 여기가 Vim인가 tmux인가"를 판단해 다른 키를 누르는 대신, 이 판단 자체를 셸 조건으로 자동화했다는 점이 이 플러그인의 핵심이다.

이렇게 tmux 패널과 Vim/Neovim의 분할 창이 하나의 조작 체계로 묶이면, 에디터·터미널·로그를 오가는 경험은 별도의 IDE 없이도 사실상 경량 통합 개발 환경에 가까워진다 — 각 도구는 여전히 독립적이지만, 이동 방식만큼은 하나로 통일되기 때문이다.

```tmux
# ~/.tmux.conf
vim_pattern='(\S+/)?g?\.?(view|l?n?vim?x?|fzf)(diff)?(-wrapped)?'
is_vim="ps -o state= -o comm= -t '#{pane_tty}' \
    | grep -iqE '^[^TXZ ]+ +${vim_pattern}$'"

bind-key -n 'C-h' if-shell "$is_vim" 'send-keys C-h' 'select-pane -L'
bind-key -n 'C-j' if-shell "$is_vim" 'send-keys C-j' 'select-pane -D'
bind-key -n 'C-k' if-shell "$is_vim" 'send-keys C-k' 'select-pane -U'
bind-key -n 'C-l' if-shell "$is_vim" 'send-keys C-l' 'select-pane -R'
```

`-n`을 쓰는 이유도 07장에서 다룬 그대로다 — prefix 없이 `Ctrl+h`를 바로 눌러야 Vim의 방향 이동처럼 자연스럽게 느껴지기 때문이다. 다만 07장에서 경고했듯, root 테이블 바인딩은 다른 프로그램의 같은 조합과 충돌할 위험을 늘 수반한다.

## 설치

| 대상 | 방법 |
|---|---|
| Vim | Vundle 등 플러그인 매니저로 `christoomey/vim-tmux-navigator` 추가, 또는 Vim 8+ 네이티브 패키지 기능으로 `~/.vim/pack/plugin/start/`에 clone |
| Neovim | `lazy.nvim` 등 최신 플러그인 매니저 설정에 등록(공식적으로 지원) |
| tmux | 위 코드 스니펫을 `tmux.conf`에 직접 추가하거나, TPM으로 `set -g @plugin 'christoomey/vim-tmux-navigator'` 후 `prefix I` |

## 예시

### 카피 모드에도 같은 키 매핑 걸기

10장에서 다룬 대로 카피 모드는 `mode-keys`에 따라 별도 키 테이블을 쓴다. 카피 모드 안에서도 같은 방향키로 패널을 이동하고 싶다면 `copy-mode-vi` 테이블에 동일하게 바인딩한다.

```tmux
bind-key -T copy-mode-vi 'C-h' select-pane -L
bind-key -T copy-mode-vi 'C-j' select-pane -D
bind-key -T copy-mode-vi 'C-k' select-pane -U
bind-key -T copy-mode-vi 'C-l' select-pane -R
```

### 키 매핑 바꾸기

TPM으로 설치했다면 방향키 대신 다른 키를 쓰도록 옵션으로 조정할 수 있다.

```tmux
set -g @vim_navigator_mapping_left "C-Left C-h"   # C-h와 C-Left 둘 다 허용
set -g @vim_navigator_mapping_prev ""             # C-\ 바인딩은 비활성화
```

## 비교/트레이드오프

여러 창을 동시에 보는 방법은 tmux 패널과 에디터 내장 터미널(예: Neovim의 `:terminal`) 두 가지가 있다.

| 구분 | tmux 패널 분할 | 에디터 내장 터미널 |
|---|---|---|
| 적용 범위 | 에디터 밖의 모든 프로그램(로그, 서버, 다른 셸)까지 포괄 | 에디터 세션 안에서만 유효 |
| 세션 독립성 | 에디터를 껐다 켜도 tmux 세션은 그대로 유지 | 에디터 프로세스가 끝나면 내장 터미널도 함께 사라짐 |
| 학습 비용 | tmux 자체의 개념(세션·윈도우·패널)을 먼저 알아야 함 | 이미 에디터에 익숙하면 추가 학습 거의 없음 |
| 적합한 상황 | 에디터 밖의 여러 프로세스를 함께 다뤄야 하는 경우 | 에디터 안에서 짧은 명령만 실행하면 되는 경우 |

`vim-tmux-navigator`는 이 둘을 대립시키지 않고, tmux 패널과 Vim 분할을 하나로 잇는 절충안에 가깝다.

## 주의사항·함정

**tmux 버전에 따른 `C-\` 바인딩 문법 차이**: 공식 스니펫은 tmux 3.0을 기준으로 `C-\` 이스케이프 방식을 분기한다. 오래된 tmux 버전에서 최신 스니펫을 그대로 쓰면 이 특정 키 바인딩만 예상과 다르게 동작할 수 있다.

**감지 패턴에 걸리지 않는 변종**: `$is_vim`의 정규식은 흔한 vim/neovim 실행 파일 이름 패턴을 다루지만, 래퍼 스크립트나 독특한 별칭으로 실행하면 감지가 안 될 수 있다. 이럴 때는 `@vim_navigator_pattern`으로 감지 정규식을 직접 조정한다.

**root 테이블 바인딩의 충돌 위험**: `-n`으로 프리픽스 없이 바인딩하므로, 07장에서 다룬 대로 셸이나 다른 프로그램이 이미 `Ctrl+h`/`j`/`k`/`l`을 다른 용도로 쓰고 있다면 충돌할 수 있다.

## 흔한 오개념

<strong>"이 플러그인은 Vim 전용이라 Neovim에서는 못 쓴다"</strong>는 생각은 틀렸다. `lazy.nvim`을 비롯한 Neovim 플러그인 매니저도 공식적으로 지원한다.

<strong>"`Ctrl+h`/`j`/`k`/`l`은 항상 tmux 패널을 이동시킨다"</strong>는 오해도 흔하다. 실제로는 현재 패널에서 Vim이 실행 중이면 그 입력이 Vim 쪽으로 위임되어 Vim의 분할 이동으로 처리된다.

<strong>"이 통합은 tmux의 새로운 특별 기능이다"</strong>는 생각도 정확하지 않다. 근본적으로는 07장의 `bind-key -n`과 13장의 `if-shell`을 조합한 것일 뿐, tmux 자체에 이 플러그인 전용 기능이 추가된 것은 아니다.

## 다음 장에서는

[19장: 대안 도구 비교 - screen, Zellij, WezTerm](/post/tmux/tmux-vs-screen-zellij-wezterm-comparison/)에서는 tmux를 GNU screen, Zellij, WezTerm 같은 다른 터미널 멀티플렉서와 비교한다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- `vim-tmux-navigator`가 해결하는 문제(Vim 분할과 tmux 패널의 단축키 불일치)를 설명할 수 있다.
- `bind-key -n`과 `if-shell`이 어떻게 조합돼 프로세스 감지 기반 분기를 만드는지 설명할 수 있다.
- 카피 모드(`copy-mode-vi`)에도 같은 방향키 매핑을 추가할 수 있다.
- root 테이블 바인딩의 충돌 위험을 인지하고 필요 시 커스텀 패턴으로 대응할 수 있다.
- tmux 패널 분할과 에디터 내장 터미널 중 상황에 맞는 것을 선택할 수 있다.

## 참고 및 출처

1. [christoomey/vim-tmux-navigator](https://github.com/christoomey/vim-tmux-navigator) — 공식 README, 설치·설정·동작 원리.
2. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — `bind-key`·`if-shell`·`copy-mode-vi` 참고.
