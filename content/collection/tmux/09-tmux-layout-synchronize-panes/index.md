---
draft: false
slug: tmux-layout-synchronize-panes
title: "[Tmux] 09. 레이아웃과 패널 동기화 - synchronize-panes"
description: "select-layout의 7가지 프리셋 배치(even/main/tiled)와 main-pane-width/height 옵션, synchronize-panes로 여러 패널에 입력을 동시에 보내는 법을 다룹니다. 여러 서버를 한 번에 관리하는 실전 예제로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 9
categories:
- Tmux
tags:
- Tmux
- Terminal
- Automation(자동화)
- DevOps
- SSH(Secure Shell)
- Networking(네트워킹)
- Algorithm(알고리즘)
- Case-Study
- Configuration(설정)
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

3부(고급 조작)의 첫 장이다. 04장에서는 `split-window -h`/`-v`로 패널을 하나씩 손으로 나눴다. 패널이 서너 개를 넘어가면 그때마다 위치를 손으로 맞추는 대신, tmux가 미리 정의해 둔 배치 알고리즘 중 하나를 고르는 편이 빠르다. 이 장은 그 <strong>레이아웃(layout)</strong> 기능과, 여러 패널에 같은 입력을 동시에 보내는 <strong>synchronize-panes</strong>를 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [08장: 상태바 커스터마이징](/post/tmux/tmux-status-bar-customization-status-line/)으로 2부를 마친 뒤, 04장에서 손으로 나눴던 패널 배치를 자동화하는 3부의 첫 챕터다.

**이 장의 깊이**: **입문**에서 **중급**(레이아웃 문자열을 재사용하고, synchronize-panes의 예외 조건까지 설명할 수 있는 수준) 사이를 오간다. **다루지 않는 것**: 패널을 다른 윈도우로 옮기거나 합치는 것은 11장에서, 여러 클라이언트가 같은 세션을 보는 것은 12장에서, 카피 모드는 10장에서 각각 다룬다. 이 장은 "이미 있는 패널을 어떻게 자동으로 배치할지"와 "여러 패널에 같은 입력을 어떻게 동시에 보낼지"에 집중한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 패널을 늘 손으로 나누고 크기를 맞춰 온 사람 | 정신 모델, 프리셋 레이아웃, 예시 | 프리셋 레이아웃으로 패널 배치를 한 번에 정리할 수 있다 |
| 여러 서버를 동시에 관리해야 하는 사람 | 예시(synchronize-panes), 주의사항·함정 | 여러 SSH 패널에 같은 명령을 동시에 입력하되 그 위험을 관리할 수 있다 |
| 에디터 패널을 유독 크게 쓰고 싶은 사람 | 프리셋 레이아웃(main-vertical), 예시 | `main-pane-width`로 메인 패널의 크기를 원하는 비율로 고정할 수 있다 |
| 매번 같은 레이아웃을 재현하고 싶은 사람 | 예시(레이아웃 문자열 재사용) | `list-windows`로 뽑은 레이아웃 문자열을 다른 윈도우에도 그대로 적용할 수 있다 |

## 정신 모델: 레이아웃은 미리 정의된 배치 알고리즘

04장의 `split-window`는 매번 사람이 "지금 이 패널을 어느 방향으로 나눌지"를 하나하나 결정하는 방식이다. <strong>레이아웃</strong>은 그 반대다 — 지금 윈도우 안에 있는 패널 전체를 대상으로, 미리 정의된 배치 알고리즘 중 하나를 적용해 한 번에 재배치한다. `select-layout`으로 원하는 레이아웃을 직접 고를 수도 있고, `next-layout`(기본적으로 prefix 뒤 `Space`에 연결돼 있다)으로 프리셋을 순서대로 돌려볼 수도 있다.

## 7가지 프리셋 레이아웃

7개의 프리셋은 크게 세 가지 사고방식으로 나뉜다. `even-*` 계열은 모든 패널을 똑같은 크기로 대접하고, `main-*` 계열은 패널 하나를 다른 패널보다 의도적으로 크게 키워 "주인공"으로 삼으며, `tiled`는 패널 개수에 따라 행과 열을 자동으로 계산해 격자로 채운다. 어떤 작업에 몇 개의 패널이 필요한지가 정해지면, 이 세 사고방식 중 어느 것이 맞는지도 대체로 자연스럽게 정해진다.

| 레이아웃 | 배치 |
|---|---|
| `even-horizontal` | 모든 패널을 좌우로 균등하게 펼친다 |
| `even-vertical` | 모든 패널을 위아래로 균등하게 펼친다 |
| `main-horizontal` | 큰 메인 패널을 위쪽에 두고, 나머지는 아래쪽 공간에 좌우로 펼친다(`main-pane-height`로 메인 패널 높이 지정) |
| `main-horizontal-mirrored` | `main-horizontal`과 같지만 메인 패널이 아래쪽에 온다 |
| `main-vertical` | 큰 메인 패널을 왼쪽에 두고, 나머지는 오른쪽 공간에 위아래로 펼친다(`main-pane-width`로 메인 패널 너비 지정) |
| `main-vertical-mirrored` | `main-vertical`과 같지만 메인 패널이 오른쪽에 온다 |
| `tiled` | 모든 패널을 행과 열로 최대한 고르게 펼친다 |

## 명령과 옵션

레이아웃을 다루는 명령은 "프리셋을 고르기·순환하기·크기를 조정하기"로 나뉘고, `synchronize-panes`는 배치가 아니라 입력 방식 자체를 바꾸는 별도의 옵션이다. 두 기능은 서로 독립적이라 프리셋 레이아웃과 무관하게 언제든 동기화를 켜고 끌 수 있다.

| 명령/옵션 | 주요 옵션 | 설명 |
|---|---|---|
| `select-layout`(`selectl`) | `-n`/`-p`(다음/이전 레이아웃), `-o`(마지막 배치 되돌리기), `-E`(현재 패널과 이웃을 균등하게) | 레이아웃 이름을 인자로 주면 그 레이아웃을 적용하고, 생략하면 마지막으로 쓴 프리셋을 다시 적용한다. `list-windows`가 출력하는 레이아웃 문자열을 그대로 인자로 줘도 된다 |
| `next-layout` | - | 다음 프리셋 레이아웃으로 순환한다(기본 바인딩: prefix 뒤 `Space`) |
| `previous-layout` | - | 이전 프리셋 레이아웃으로 순환한다 |
| `main-pane-width`/`main-pane-height` | `%` 접미사 허용 | `main-vertical`/`main-horizontal`(및 mirrored 버전)의 메인 패널 크기를 지정한다. `40%`처럼 창 크기 대비 비율로도 줄 수 있다 |
| `tiled-layout-max-columns` | - | `tiled` 레이아웃에서 열 개수 상한을 지정한다. 기본값 `0`은 제한 없음을 뜻한다 |
| `synchronize-panes` | `on`/`off` | 이 옵션이 켜진 윈도우에서, 한 패널에 입력한 키를 같은 윈도우의 다른 모든 패널에도 그대로 복제한다(카피 모드 등 다른 모드에 들어가 있는 패널은 제외) |

## 예시

### 여러 패널을 프리셋으로 한 번에 정렬하기

에디터처럼 화면을 넓게 써야 하는 패널이 하나 있고 나머지는 보조적인 역할일 때는 `main-vertical`처럼 메인 패널을 두는 레이아웃이 적합하다. 반대로 여러 서버의 로그를 동등한 비중으로 지켜봐야 한다면 `tiled`처럼 모든 패널을 균등하게 배치하는 쪽이 낫다.

```bash
# 현재 윈도우의 모든 패널을 격자 형태로 고르게 배치
tmux select-layout tiled

# 왼쪽에 큰 메인 패널(에디터), 오른쪽에 나머지 패널을 위아래로
tmux select-layout main-vertical
tmux set-window-option main-pane-width 60%
```

### 레이아웃 문자열을 뽑아 다른 윈도우에 그대로 적용하기

`list-windows`는 지금 레이아웃을 `select-layout`에 그대로 넣을 수 있는 문자열로 보여준다. 같은 배치를 다른 윈도우에도 재현하고 싶을 때 유용하다.

```bash
$ tmux list-windows
0: bash* (1 panes) [80x24] [layout bb62,159x48,0,0{79x48,0,0,79x48,80,0}] @0

$ tmux select-layout 'bb62,159x48,0,0{79x48,0,0,79x48,80,0}'
```

### synchronize-panes로 여러 서버에 같은 명령 동시 입력하기

이름을 붙인 여러 패널 각각에서 서로 다른 서버로 SSH 접속을 해 둔 상태에서 `synchronize-panes on`을 켜면, 한 패널에 타이핑하는 모든 키가 나머지 패널에도 그대로 들어간다. 여러 서버에 같은 패키지를 한 번에 설치하는 등의 작업에 흔히 쓰이는 패턴이다.

```bash
# 여러 SSH 패널을 만든 뒤 동기화 입력을 켠다
tmux set-window-option synchronize-panes on

# (모든 패널에 동시에 들어간다) 예: apt update && apt upgrade -y

# 작업이 끝나면 반드시 끈다
tmux set-window-option synchronize-panes off
```

이 패턴은 데브옵스 실무에서 특히 자주 쓰인다. 네트워크로 연결된 여러 대의 서버에 SSH로 각각 접속해 두고 패치 배포나 설정 동기화처럼 반복적인 작업을 실행해야 할 때, pssh나 Ansible 같은 전용 병렬 실행 도구 없이도 tmux만으로 즉석에서 같은 효과를 낼 수 있다. 다만 서버마다 SSH 연결 지연(latency)이 다르면 같은 명령을 동시에 보내도 화면에 결과가 찍히는 시점이 패널마다 어긋날 수 있다는 점은 감안해야 한다 — 동기화는 입력 시점을 맞출 뿐, 각 서버의 응답 속도까지 맞춰주지는 않는다.

## 비교/트레이드오프

패널을 배치하는 방법은 04장에서 배운 수동 분할과 이 장의 프리셋 레이아웃 두 가지다.

| 구분 | 수동 분할(`split-window -h`/`-v`) | 프리셋 레이아웃(`select-layout`) |
|---|---|---|
| 제어력 | 패널 하나하나의 위치를 원하는 대로 정할 수 있다 | 미리 정의된 배치 중에서 고른다 |
| 속도 | 패널이 많아지면 분할·이동을 여러 번 반복해야 한다 | 한 번의 명령으로 전체 배치를 재구성한다 |
| 재현성 | 같은 배치를 다시 만들려면 같은 순서를 반복해야 한다 | 레이아웃 이름이나 레이아웃 문자열로 정확히 재현 가능 |
| 적합한 상황 | 비대칭적이고 특수한 배치가 필요할 때 | 대칭적이거나 표준적인 배치로 충분할 때 |

## 주의사항·함정

**`synchronize-panes on` 상태에서의 사고**: 이 기능의 가장 큰 위험은, 여러 서버에 명령을 동시에 보내는 도중 실수로 파일 삭제나 서버 재시작처럼 되돌릴 수 없는 명령을 입력하면 그 명령이 동기화된 모든 패널에 그대로 실행된다는 점이다. 위험한 명령을 입력하기 전에는 반드시 동기화를 끄는 습관을 들인다.

**레이아웃 문자열은 패널 개수를 초과해 적용할 수 없다**: 특정 패널 개수를 전제로 만들어진 레이아웃 문자열은, 그보다 패널이 더 많은 윈도우에는 적용할 수 없다. 패널 개수가 다른 윈도우 사이에서 레이아웃을 재사용하려면 이 제약을 먼저 확인해야 한다.

**동기화가 카피 모드 패널은 건너뛴다**: `synchronize-panes`는 다른 모드(예: 카피 모드)에 들어가 있는 패널에는 입력을 복제하지 않는다. "왜 이 패널만 반응이 없지"라는 의문이 든다면, 그 패널이 지금 카피 모드 같은 다른 모드에 있는지부터 확인한다.

## 흔한 오개념

<strong>"레이아웃을 바꾸면 패널 안에서 돌던 프로그램도 다시 시작된다"</strong>는 생각은 틀렸다. 레이아웃은 패널의 크기와 배치만 바꿀 뿐, 각 패널 안에서 실행 중인 프로세스는 그대로 유지된다.

<strong>"synchronize-panes는 패널의 화면 내용까지 똑같이 만든다"</strong>는 오해도 흔하다. 실제로 복제되는 것은 <strong>입력</strong>뿐이다. 각 패널이 그 입력에 어떻게 반응하는지는 패널마다 실행 중인 프로그램에 달려 있으므로, 화면(출력)은 패널마다 다를 수 있다.

<strong>"`next-layout`은 별도로 바인딩하지 않으면 쓸 수 없다"</strong>는 생각도 정확하지 않다. 기본 키바인딩에 이미 prefix 뒤 `Space`로 연결돼 있으므로, 07장에서 배운 재배치 없이도 바로 쓸 수 있다.

## 다음 장에서는

[10장: 카피 모드와 버퍼 - 클립보드 연동](/post/tmux/tmux-copy-mode-buffers-clipboard/)에서는 패널 화면을 스크롤하며 텍스트를 선택·복사하고 클립보드와 연동하는 법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- 7가지 프리셋 레이아웃의 이름과 배치 방식을 구분해 설명할 수 있다.
- `main-pane-width`/`main-pane-height`로 메인 패널의 크기를 원하는 비율로 지정할 수 있다.
- `list-windows`로 뽑은 레이아웃 문자열을 다른 윈도우에 재적용할 수 있다.
- `synchronize-panes`가 복제하는 것이 입력이지 화면 출력이 아니라는 점을 설명할 수 있다.
- `synchronize-panes`를 켠 상태에서 위험한 명령을 실행하는 것이 왜 사고로 이어지는지 설명하고 예방할 수 있다.

## 참고 및 출처

1. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — 7가지 프리셋 레이아웃, `select-layout`·`next-layout`·`previous-layout`, `main-pane-width`/`main-pane-height`, `synchronize-panes` 공식 설명.
2. [tmux/tmux](https://github.com/tmux/tmux) — tmux 공식 소스 저장소.
