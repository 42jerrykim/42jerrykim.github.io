---
draft: false
slug: tmux-prefix-key-command-mode
title: "[Tmux] 05. Prefix 키와 커맨드 모드"
description: "tmux의 기본 prefix 키(Ctrl+b)가 입력을 가로채는 방식과, 콜론(:)으로 진입하는 커맨드 모드를 다룹니다. prefix 옵션 변경, send-prefix로 리터럴 키 전달, list-keys로 바인딩을 확인하는 법을 실전 예제로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 5
categories:
- Tmux
tags:
- Tmux
- Terminal
- Shell(셸)
- Session(세션)
- Keyboard(키보드)
- Configuration(설정)
- Productivity(생산성)
- Workflow(워크플로우)
- Best-Practices
- SSH(Secure Shell)
- Interface(인터페이스)
- Deep-Dive
- OS(운영체제)
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

지금까지는 `Ctrl+b`가 세션·윈도우·패널 명령을 실행시켜 준다는 것을 당연하게 받아들이고 썼다. 이 장은 그 `Ctrl+b`가 정확히 어떤 메커니즘으로 동작하는지, 그리고 단축키 없이 명령 이름을 직접 타이핑하는 <strong>커맨드 모드</strong>(`:`)가 무엇인지 다룬다. 05장부터 시작하는 2부(Prefix·설정)의 첫 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [04장: 윈도우와 패널 기초](/post/tmux/tmux-window-pane-basics-split-zoom/)에서 실제로 눌러 본 `Ctrl+b` 뒤 명령 키 조합이 왜 그렇게 동작하는지 설명한다.

**이 장의 깊이**: **입문**에서 **중급**(prefix 변경 시 생기는 충돌을 스스로 진단할 수 있는 수준) 사이를 오간다. **다루지 않는 것**: `tmux.conf` 파일 자체의 문법(설정을 어디에, 어떤 형식으로 쓰는가)은 06장에서, 개별 키를 원하는 동작에 재배치하는 `bind-key` 문법은 07장에서, 상태바에 표시되는 내용을 바꾸는 법은 08장에서 각각 다룬다. 이 장은 prefix라는 개념 자체와 커맨드 모드에 집중한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| `Ctrl+b`를 기계적으로 눌러 온 초보자 | 정신 모델, 예시 | prefix가 입력을 가로채는 방식을 이해하고, 커맨드 모드로 명령을 직접 실행할 수 있다 |
| prefix를 다른 키로 바꾸고 싶은 사람 | 예시(prefix 변경), 주의사항·함정 | 셸·다른 프로그램과 충돌하지 않는 prefix를 고를 수 있다 |
| 단축키를 다 외우기 부담스러운 사람 | 비교/트레이드오프, 예시(커맨드 모드) | `:` 커맨드 모드로 이름 기반 명령 실행을 대안으로 쓸 수 있다 |
| SSH로 원격 서버를 오가며 여러 클라이언트를 쓰는 사람 | 정신 모델, 주의사항·함정 | prefix 처리가 로컬·원격 클라이언트에서 왜 동일하게 동작하는지 이해한다 |

## 정신 모델: prefix가 입력을 가로채는 방식

tmux 클라이언트는 사용자가 입력하는 모든 키를 먼저 자기 자신이 소비할지, 아니면 그대로 활성 패널의 프로그램(셸, vim 등)에 전달할지 판단한다. 평상시에는 모든 입력이 그대로 통과되지만, 사용자가 <strong>prefix 키</strong>(기본값 `Ctrl+b`)를 누르는 순간 tmux는 "다음에 오는 키 하나는 명령으로 해석하라"는 대기 상태로 들어간다. 이 대기 상태에서 눌린 키가 알려진 명령 키(예: `c`는 새 윈도우, `%`는 패널 분할)라면 그 명령을 실행하고, 그렇지 않으면 아무 동작도 하지 않는다. 이 대기는 무한정 지속되지 않는다 — `prefix-timeout` 옵션이 지정한 시간(기본적으로 일정 시간)이 지나면 tmux는 대기를 포기하고 이후 입력을 다시 평범한 입력으로 취급한다.

이 처리는 클라이언트가 로컬 터미널이든 SSH로 접속한 원격 클라이언트든 동일하게 일어난다. SSH는 키 입력을 그대로 원격 서버로 전달하는 통로일 뿐이고, 실제로 prefix인지 판단하는 주체는 (SSH로 접속했다면) 원격 서버에서 실행 중인 tmux 클라이언트이기 때문이다. 즉 로컬에서 익힌 prefix 동작은 원격 세션에서도 그대로 재현된다.

## Prefix 옵션과 커맨드 모드

| 명령/옵션 | 설명 |
|---|---|
| `prefix` (옵션) | prefix로 쓸 키를 지정한다. `None`으로 설정하면 prefix 자체를 없앨 수 있다 |
| `prefix2` (옵션) | 두 번째 prefix 키를 추가로 지정한다. 지정하면 두 prefix 중 아무 키나 눌러도 된다 |
| `prefix-timeout` (옵션) | prefix를 누른 뒤 다음 키를 기다리는 시간(밀리초). `0`이면 타임아웃을 끈다 |
| `send-prefix` | prefix 키(또는 `-2`로 prefix2) 자체를 활성 패널에 그대로 전달한다. 기본 바인딩에서 `Ctrl+b`를 두 번 누르면 이 명령이 실행된다 |
| `command-prompt` | 클라이언트에 커맨드 프롬프트를 연다. 템플릿 없이 실행하면 화면 아래에 `:`가 뜨고, 그 뒤에 명령 이름을 직접 입력해 실행할 수 있다 |
| `list-keys`(`lsk`) | 현재 등록된 키 바인딩을 나열한다. 기본 형식은 `bind-key` 명령 형태로 출력된다 |
| `set-option`(`set`) | `-g`를 붙이면 전역(global) 옵션을, 생략하면 세션 단위 옵션을 설정한다. `prefix`를 바꿀 때는 보통 `-g`를 함께 쓴다 |

## 예시

### 지금 prefix가 무엇인지 확인하기

```bash
# 현재 전역 prefix 값 확인
tmux show-options -g prefix
# 예: prefix C-b
```

### 커맨드 모드로 명령 이름 직접 실행하기

단축키를 외우지 못했거나 애초에 단축키가 없는 명령도, prefix 뒤 `:`를 누르면 화면 아래에 프롬프트가 뜨고 명령 이름을 그대로 입력해 실행할 수 있다.

```text
Ctrl+b 뒤 :
:new-window -n build
:kill-session -t old-project
```

### prefix 키 두 번 눌러 리터럴 키 전달하기

`Ctrl+b`로 시작하는 프로그램(예: 다른 터미널 멀티플렉서 안에서 다시 tmux를 쓰는 경우)에 실제 `Ctrl+b` 입력을 그대로 보내야 할 때는 prefix를 두 번 누른다.

```text
Ctrl+b 뒤 Ctrl+b  →  활성 패널의 프로그램에 리터럴 Ctrl+b가 전달된다
```

### prefix 키를 바꾸기

기본 prefix가 불편하면(예: 자주 쓰는 다른 프로그램의 단축키와 겹칠 때) prefix 자체를 바꿀 수 있다. 아래는 `Ctrl+b`를 `Ctrl+a`로 바꾸는 가장 흔한 예시이며, 세부 `bind-key` 문법은 07장에서 더 다룬다.

```bash
# 전역 prefix를 Ctrl+a로 바꾼다
tmux set -g prefix C-a

# 기존 prefix(Ctrl+b)에 걸려 있던 기본 바인딩을 해제한다
tmux unbind C-b

# 새 prefix를 두 번 누르면 리터럴 Ctrl+a가 전달되도록 다시 연결한다
tmux bind C-a send-prefix

# 바뀐 바인딩을 확인한다
tmux list-keys -T prefix | head
```

## 비교/트레이드오프

명령을 실행하는 방법은 단축키와 커맨드 모드 두 가지다.

| 구분 | 단축키(prefix + 한 글자) | 커맨드 모드(`:` + 명령 이름) |
|---|---|---|
| 속도 | 외우고 있으면 가장 빠르다 | 타이핑이 필요해 상대적으로 느리다 |
| 학습 부담 | 자주 쓰는 명령마다 별도로 외워야 한다 | 명령 이름만 알면 되고, 옵션까지 그대로 타이핑할 수 있다 |
| 단축키 없는 명령 | 실행 불가(먼저 07장에서 다루는 방식으로 바인딩해야 함) | 어떤 명령이든 이름만 알면 바로 실행 가능 |
| 적합한 상황 | 매일 반복하는 조작(패널 분할, 윈도우 전환) | 가끔 쓰는 명령, 옵션이 많아 정확히 입력해야 하는 명령 |

이 장에서 다룬 `command-prompt`는 사람이 그 자리에서 상호작용하며 명령을 실행하는 창이다. 같은 명령을 매번 사람이 타이핑하지 않고 스크립트로 미리 정해 자동 실행하는 방법은 13장(tmux 커맨드라인과 스크립팅)에서 별도로 다룬다.

## 주의사항·함정

**셸 자체의 단축키와 충돌**: prefix를 `Ctrl+a`로 바꾸는 것은 흔한 선택이지만, Emacs 스타일 줄 편집을 쓰는 셸(기본 Bash 등)에서는 `Ctrl+a`가 원래 "줄 맨 앞으로 이동"이다. prefix로 가로채면 그 셸 단축키를 쓸 수 없게 되므로, `Ctrl+a`를 고를 때는 이 트레이드오프를 감수하는 것인지 먼저 확인해야 한다.

**운영체제·터미널 앱이 먼저 가로채는 조합**: 일부 터미널 에뮬레이터나 운영체제는 특정 `Ctrl` 조합을 tmux에 전달하기 전에 자신이 먼저 소비한다(예: 특정 창 관리 단축키와 겹치는 조합). prefix를 바꾼 뒤 아무 반응이 없다면, tmux 설정 문제가 아니라 터미널 앱·OS 단계에서 이미 가로채였을 가능성부터 의심한다.

**`prefix-timeout`이 너무 짧으면**: 대기 시간을 너무 짧게 줄이면 prefix를 누른 직후 명령 키를 입력하는 타이밍을 놓쳐 아무 일도 일어나지 않는 경우가 잦아진다. 반응이 없다고 느껴질 때 이 옵션값부터 확인하는 것도 진단 순서 중 하나다.

## 흔한 오개념

<strong>"prefix 키를 누르면 그 키 입력 자체는 어디에도 못 간다"</strong>는 생각은 절반만 맞다. 기본적으로 prefix 입력 자체는 활성 패널에 전달되지 않지만, `send-prefix`(기본적으로 prefix를 두 번 누르는 것과 같다)를 쓰면 그 키를 리터럴로 전달할 수 있다.

<strong>"명령은 반드시 prefix + 한 글자 단축키로만 실행할 수 있다"</strong>는 오해도 흔하다. `command-prompt`(prefix 뒤 `:`)를 쓰면 단축키가 아예 없는 명령도 이름으로 직접 실행할 수 있다.

<strong>"prefix를 바꾸면 그 순간부터 모든 세션에 즉시 적용된다"</strong>는 생각도 정확하지 않다. `set -g`는 전역 옵션을 바꾸지만, 이미 실행 중인 세션에 이 값이 어떻게 반영되는지, 그리고 세션별로 다른 옵션을 줄 수 있는지는 06장에서 다루는 옵션 범위(global/session/window/pane)를 알아야 정확히 설명할 수 있다.

## 다음 장에서는

[06장: tmux.conf 기초 - 설정 문법과 reload](/post/tmux/tmux-conf-basics-set-options-reload/)에서는 이 장에서 명령줄로 실행해 본 `set -g prefix` 같은 설정을, 매번 다시 입력하지 않고 파일 하나로 관리하는 법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- prefix 키가 입력을 가로채는 흐름(대기 상태 진입 → 명령 키 해석 → 타임아웃)을 설명할 수 있다.
- `send-prefix`로 prefix 키 자체를 리터럴로 전달하는 방법을 설명할 수 있다.
- 커맨드 모드(`:`)로 단축키 없는 명령을 이름으로 직접 실행할 수 있다.
- prefix를 바꿀 때 셸·터미널 앱·OS와 충돌할 수 있는 지점을 미리 점검할 수 있다.
- `list-keys`, `show-options -g prefix`로 현재 바인딩과 prefix 설정을 직접 확인할 수 있다.

## 참고 및 출처

1. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — 기본 prefix(`C-b`)와 `send-prefix` 기본 바인딩, `prefix`/`prefix2`/`prefix-timeout` 옵션, `command-prompt`·`list-keys`·`set-option` 공식 설명.
2. [tmux/tmux](https://github.com/tmux/tmux) — tmux 공식 소스 저장소.
