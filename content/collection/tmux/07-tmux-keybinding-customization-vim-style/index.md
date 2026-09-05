---
draft: false
slug: tmux-keybinding-customization-vim-style
title: "[Tmux] 07. 키바인딩 커스터마이징 - bind-key와 vim 스타일 재배치"
description: "bind-key·unbind-key로 원하는 키에 원하는 명령을 연결하는 법과, 키 테이블(prefix/root/커스텀)의 동작 방식을 다룹니다. vim 스타일 패널 이동 재배치와 다단계 키 조합 예제를 tmux 공식 문서 기준으로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 7
categories:
- Tmux
tags:
- Tmux
- Terminal
- Keyboard(키보드)
- Vim
- Configuration(설정)
- Productivity(생산성)
- Workflow(워크플로우)
- Best-Practices
- Deep-Dive
- OS(운영체제)
- Automation(자동화)
- State-Machine(상태기계)
- SSH(Secure Shell)
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

04장에서는 방향키로 패널을 옮겨 다녔고, "07장에서 vim 스타일로 재배치하는 것이 흔한 관례"라고만 예고했다. 이 장은 그 약속을 지켜, `bind-key`/`unbind-key`로 원하는 키에 원하는 명령을 자유롭게 연결하는 법과, 그 바탕이 되는 <strong>키 테이블(key table)</strong> 개념을 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [06장: tmux.conf 기초](/post/tmux/tmux-conf-basics-set-options-reload/)에서 배운 설정 파일 문법 위에서, 이번에는 개별 키 하나하나를 원하는 명령에 연결하는 법을 다룬다.

**이 장의 깊이**: **입문**에서 **중급**(다단계 키 조합을 위한 커스텀 키 테이블을 직접 설계할 수 있는 수준) 사이를 오간다. **다루지 않는 것**: 카피 모드 자체의 vi/emacs 스타일 조작(`mode-keys` 옵션이 좌우하는 `copy-mode`/`copy-mode-vi` 테이블)은 10장에서, 상태바에 무엇을 표시할지는 08장에서 각각 다룬다. 이 장에서 말하는 "vim 스타일"은 카피 모드가 아니라 패널 이동처럼 평소에 쓰는 키를 vim 방향키(`h`/`j`/`k`/`l`)로 재배치하는 것을 뜻한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 기본 키바인딩만 써 온 초보자 | 정신 모델, 명령과 옵션, 예시(vim 스타일 재배치) | 자주 쓰는 조작을 자신에게 익숙한 키로 재배치할 수 있다 |
| vim 사용자로서 방향키 대신 hjkl에 익숙한 사람 | 예시(vim 스타일 재배치), 주의사항·함정 | 패널 이동을 vim 방향키로 바꾸고 반복 입력까지 편하게 만들 수 있다 |
| prefix 뒤 여러 단계로 명령을 묶고 싶은 사람 | 정신 모델(키 테이블), 예시(커스텀 키 테이블) | 커스텀 키 테이블로 다단계 키 조합을 설계할 수 있다 |
| 다른 사람의 tmux.conf를 그대로 가져다 쓰려는 사람 | 주의사항·함정, 비교/트레이드오프 | `-n`(prefix 없이 바인딩)의 위험성을 판단하고 자신의 환경에 맞게 걸러 쓸 수 있다 |

## 정신 모델: 모든 키바인딩은 키 테이블에 속한다

tmux의 키바인딩은 항상 어떤 <strong>키 테이블(key table)</strong>에 등록된다. `bind-key`를 `-T` 없이 실행하면 기본적으로 <strong>prefix</strong> 테이블에 등록되는데, 이 테이블은 prefix 키를 누른 <strong>다음</strong>에 오는 키를 찾아보는 곳이다(예: 기본적으로 `c`가 prefix 테이블의 `new-window`에 연결돼 있어 `Ctrl+b c`가 새 윈도우를 만든다). 반대로 <strong>root</strong> 테이블은 prefix 없이 곧바로 눌린 키를 찾아보는 곳이며, `-n` 플래그는 `-T root`의 줄임 표현이다.

이 구분이 왜 중요한지는 tmux 공식 문서의 경고에서 잘 드러난다 — root 테이블에 `c`를 `new-window`로 바인딩하면(권장되지 않음) prefix 없이 그냥 `c`만 입력해도 새 윈도우가 만들어져 버린다. 셸이나 에디터에서 평범하게 타이핑하는 `c`까지 가로채 버리는 것이다. 그래서 `-n`으로 바인딩할 때는 다른 프로그램과 절대 겹치지 않을 조합(자주 쓰이는 조합자 키 등)을 골라야 한다.

## 명령과 옵션

| 명령 | 주요 옵션 | 설명 |
|---|---|---|
| `bind-key`(`bind`) | `-n`, `-r`, `-T 테이블`, `-N 메모` | 키를 명령에 연결한다. `-n`은 `-T root`의 별칭. `-r`은 이 키가 반복 가능함을 표시한다(05장에서 다룬 `repeat-time`/`initial-repeat-time` 옵션이 이 반복 창을 결정한다). `-N`은 `list-keys -N`으로 볼 수 있는 설명을 붙인다 |
| `unbind-key`(`unbind`) | `-a`, `-n`, `-T 테이블`, `-q` | 바인딩을 해제한다. `-a`는 모든 바인딩을 한 번에 제거하고, `-q`는 없는 키를 해제하려 해도 오류를 내지 않는다 |
| `switch-client -T 테이블` | - | 클라이언트를 지정한 키 테이블로 전환한다. 한 번 눌린 키를 처리한 뒤에는 기본 테이블(보통 root)로 돌아간다. 다단계 키 조합을 만들 때 쓰인다 |
| `list-keys`(`lsk`) | `-T 테이블` | 지정한 테이블에 등록된 바인딩을 나열한다(05장에서 이미 소개) |

## 예시

### vim 스타일로 패널 이동 재배치하기

04장에서 방향키로 패널을 옮기던 `select-pane`을 vim 방향키에 연결한다. `-r`을 붙이면 한 번 prefix를 누른 뒤 짧은 시간 안에는 다시 prefix 없이 같은 키를 눌러도 이동이 반복된다.

```bash
# ~/.tmux.conf
unbind-key -T prefix Left
unbind-key -T prefix Down
unbind-key -T prefix Up
unbind-key -T prefix Right

bind-key -r h select-pane -L
bind-key -r j select-pane -D
bind-key -r k select-pane -U
bind-key -r l select-pane -R
```

### 커스텀 키 테이블로 다단계 조합 만들기

`switch-client -T`를 연쇄하면 3단계 이상의 키 조합도 만들 수 있다. 아래는 tmux 공식 문서가 예시로 드는 패턴을 그대로 옮긴 것이다 — `a`, `b`, `c`를 순서대로 누르면 최종적으로 `list-keys`가 실행된다.

```bash
bind-key -T root   a switch-client -T table1
bind-key -T table1 b switch-client -T table2
bind-key -T table2 c list-keys
```

이 패턴을 실전에 옮기면, 예를 들어 prefix 뒤 `w`를 눌러 "윈도우 관리" 전용 테이블로 들어간 다음, 그 안에서 숫자 키 하나로 즉시 원하는 윈도우로 전환하도록 설계할 수 있다. 키 테이블 전환은 본질적으로 <strong>상태 기계(state machine)</strong>다 — 지금 어떤 테이블에 있는지가 "상태"이고, 키 입력이 다음 상태로 넘어가는 "전이"이며, `switch-client -T` 없이 명령이 실행되면 자동으로 처음 상태(보통 root)로 돌아간다. 매번 사람이 손으로 여러 명령을 순서대로 입력하는 대신 정해진 순서를 키 하나씩으로 유도한다는 점에서, 이 패턴은 아주 단순한 형태의 입력 자동화이기도 하다.

### 확인과 해제

```bash
# prefix 테이블에 지금 등록된 바인딩 전체 확인
tmux list-keys -T prefix

# 특정 키의 바인딩만 해제
tmux unbind-key -T prefix Left

# 위험을 감수하고 모든 바인딩을 초기화 (되돌리려면 tmux.conf를 다시 source)
tmux unbind-key -a
```

## 비교/트레이드오프

키를 prefix 테이블에 둘지, root 테이블에 직접(`-n`) 둘지는 트레이드오프가 뚜렷하다.

| 구분 | prefix 테이블에 바인딩 | root 테이블에 바인딩(`-n`) |
|---|---|---|
| 입력 충돌 위험 | prefix를 누른 뒤에만 활성화돼 낮다 | 다른 프로그램의 평범한 입력과 겹칠 위험이 크다 |
| 입력 속도 | prefix + 키, 두 단계 | 키 하나만으로 즉시 실행 |
| 적합한 상황 | 대부분의 명령(공식 문서도 이 방식을 기본으로 권장) | 아주 드물게 마우스 클릭이나 펑션 키처럼 다른 프로그램과 절대 겹치지 않는 특수 입력에 한정 |

## 주의사항·함정

**`-n`(root 바인딩) 남용**: 공식 문서조차 root 테이블에 흔한 문자를 바인딩하는 것을 "권장하지 않는다"고 명시한다. 셸에서 타이핑하는 모든 글자가 그 바인딩과 겹치는 순간 사라져 버릴 수 있기 때문이다.

**터미널 앱·OS가 먼저 가로채는 키**: 05장에서 prefix 자체를 바꿀 때 다뤘던 문제가 개별 키바인딩에도 그대로 적용된다. 일부 터미널 에뮬레이터나 운영체제는 특정 `Ctrl`/`Alt` 조합을 tmux에 전달하기 전에 자신이 먼저 소비하므로, 새로 만든 바인딩이 반응하지 않으면 tmux 설정이 아니라 터미널 앱·OS 단계를 먼저 의심한다.

**다른 사람의 tmux.conf를 그대로 복사할 때**: 커뮤니티에 공유되는 설정은 대부분 특정 터미널·워크플로우를 전제로 만들어졌다. `-n`으로 바인딩된 키가 많은 설정을 그대로 가져오면, 자신이 평소 쓰는 셸 단축키나 에디터 조합과 충돌할 수 있으므로 `-n` 바인딩만이라도 먼저 훑어보는 것이 안전하다. 이 원칙은 로컬이든 SSH로 접속한 원격 클라이언트든 동일하게 적용된다 — 키 테이블 처리는 클라이언트가 붙어 있는 tmux 서버 쪽에서 일어나기 때문이다.

## 흔한 오개념

<strong>"bind는 항상 prefix 없이 바로 눌리는 키를 정의한다"</strong>는 생각은 정반대다. `-T`나 `-n`을 명시하지 않으면 기본값은 prefix 테이블이며, root 테이블에 바인딩하려면 반드시 `-n`을 명시해야 한다.

<strong>"`-r`을 주면 키를 누르고 있는 동안 계속 반복된다"</strong>는 오해도 흔하다. 실제로는 물리적으로 키를 누르고 있는 것과 무관하게, prefix를 다시 누르지 않고 그 키를 일정 시간(반복 시간 옵션으로 조절) 안에 다시 누르면 명령이 다시 실행되는 방식이다.

<strong>"커스텀 키 테이블은 너무 복잡해서 실무에서는 안 쓴다"</strong>는 생각도 있다. 실제로는 여러 유명 tmux 설정과 플러그인이 prefix 뒤 특정 키로 서브메뉴 성격의 테이블에 진입시키는 패턴을 흔히 쓴다 — 명령 개수가 많아질 때 단축키 하나에 다 우겨넣는 대신 계층을 나누는 자연스러운 방법이기 때문이다.

## 다음 장에서는

[08장: 상태바(Status Line) 커스터마이징](/post/tmux/tmux-status-bar-customization-status-line/)에서는 지금까지 조작 방식을 바꿔온 것과 달리, 화면 아래 상태바에 무엇을 어떻게 보여줄지 바꾸는 법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- prefix 테이블과 root 테이블의 차이, `-n`이 무엇의 줄임인지 설명할 수 있다.
- `bind-key`/`unbind-key`로 원하는 키에 원하는 명령을 연결하고 해제할 수 있다.
- `-r` 플래그가 실제로 무엇을 반복시키는지(물리적 키 누름이 아니라 재입력 창) 정확히 설명할 수 있다.
- `switch-client -T`를 연쇄해 다단계 키 조합을 설계할 수 있다.
- root 테이블에 바인딩하는 것이 왜 위험할 수 있는지 판단하고, prefix 테이블과 상황에 맞게 선택할 수 있다.

## 참고 및 출처

1. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — `bind-key`·`unbind-key`·키 테이블(prefix/root/커스텀)·`switch-client -T` 공식 설명과 예제.
2. [tmux/tmux](https://github.com/tmux/tmux) — tmux 공식 소스 저장소.
