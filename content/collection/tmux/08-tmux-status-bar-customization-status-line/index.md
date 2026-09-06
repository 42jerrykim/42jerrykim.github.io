---
draft: false
slug: tmux-status-bar-customization-status-line
title: "[Tmux] 08. 상태바(Status Line) 커스터마이징"
description: "tmux 상태바가 주기적으로 다시 그려지는 원리와 status-left/status-right, 포맷 변수(#S, #W 등), STYLES(fg=/bg=) 문법을 다룹니다. 조건부 표현식과 길이 제한 함정을 실전 예제로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 8
categories:
- Tmux
tags:
- Tmux
- Terminal
- Configuration(설정)
- Interface(인터페이스)
- Keyboard(키보드)
- Session(세션)
- Deep-Dive
- Automation(자동화)
- Monitoring(모니터링)
- Environment
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

지금까지는 tmux를 어떻게 조작하는지(입력)에 집중했다. 이 장은 반대로 tmux가 화면 맨 아래에 무엇을 어떻게 보여주는지(출력) — <strong>상태바(status line)</strong> — 를 다룬다. 2부(Prefix·설정)의 마지막 장이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [07장: 키바인딩 커스터마이징](/post/tmux/tmux-keybinding-customization-vim-style/)에서 입력을 다룬 것과 짝을 이루는, 출력(표시) 커스터마이징 장이다. 06장에서 배운 `set -g` 문법을 그대로 상태바 옵션에도 쓴다.

**이 장의 깊이**: **입문**에서 **중급**(포맷 변수와 조건부 표현식으로 원하는 정보를 조합할 수 있는 수준) 사이를 오간다. **다루지 않는 것**: 카피 모드 안에서 보이는 인디케이터는 10장에서, 플러그인으로 상태바에 CPU·배터리 같은 외부 정보를 추가하는 것은 15–16장에서 각각 다룬다. 포맷 언어 자체는 정규식·퍼지 매치 같은 고급 연산자까지 매우 방대한데, 이 장은 실무에서 가장 자주 쓰는 변수·조건부 기본형까지만 다룬다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 기본 상태바를 그대로 써 온 사람 | 정신 모델, 옵션과 포맷 변수, 예시 | 세션·윈도우 이름 외에 원하는 정보를 상태바에 추가할 수 있다 |
| 상태바가 너무 밋밋하거나 반대로 복잡하다고 느끼는 사람 | 비교/트레이드오프, 예시(스타일 적용) | 정보량과 가독성의 균형을 자신의 워크플로우에 맞게 조정할 수 있다 |
| 커스텀 상태바를 만들었는데 글자가 잘리는 사람 | 주의사항·함정 | `status-left-length`/`status-right-length`가 왜 잘림의 원인인지 진단할 수 있다 |
| 세션 상태를 한눈에 모니터링하고 싶은 사람 | 예시(조건부 표현식) | attach 여부 같은 상태를 조건부로 표시할 수 있다 |

## 정신 모델: 상태바는 포맷 문자열을 주기적으로 다시 그린 것

상태바는 화면에 고정으로 박힌 텍스트가 아니라, tmux가 `status-interval` 옵션이 지정한 주기(기본 15초, `0`이면 시간에 의한 재계산을 끈다)마다 `status-left`/`status-right` <strong>포맷 문자열</strong>을 다시 평가해 그린 결과다. 포맷 문자열 안에서 `#{session_name}`처럼 중괄호로 감싼 이름은 그 순간의 실제 값(지금 세션 이름, 윈도우 이름, 시각 등)으로 치환되며, `#S`처럼 자주 쓰는 몇 개는 더 짧은 별칭도 제공된다. 색이나 굵기 같은 스타일은 `#[fg=색상,속성]`처럼 대괄호로 감싼 조각을 문자열 중간에 끼워 넣어 그 지점부터 적용한다.

즉 상태바 커스터마이징은 "무엇을 보여줄지"(포맷 변수)와 "어떻게 보여줄지"(스타일)를 문자열 하나로 조합하는 작업이다. 이 둘을 분리해서 생각하면 복잡해 보이는 상태바 설정도 읽어 내려가기 쉬워진다.

## 옵션과 포맷 변수

상태바 관련 옵션은 "언제·어디에 그릴지"를 정하는 것과 "무엇을·어떻게 그릴지"를 정하는 것으로 나뉜다. `status-interval`·`status-position`·`status-justify`·`status-keys`는 상태바 자체의 동작 방식을 결정하고, `status-left`/`status-right`와 그 길이·스타일 옵션은 실제로 표시될 내용과 겉모습을 결정한다. 아래 표는 이 둘을 함께 정리한 것이다.

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `status-interval` | 15(초) | 상태바를 다시 그리는 주기. `0`이면 시간 기반 갱신을 끈다 |
| `status-position` | `bottom` | 상태바를 화면 위(`top`)/아래(`bottom`) 중 어디에 둘지 |
| `status-justify` | `left` | 윈도우 목록을 상태바의 왼쪽/가운데/오른쪽 중 어디에 배치할지 |
| `status-keys` | `emacs` | 상태바(커맨드 프롬프트 등)에서 vi/emacs 중 어떤 편집 키를 쓸지. `$VISUAL`/`$EDITOR`에 `vi`가 포함되면 자동으로 vi가 기본값이 된다 |
| `status-left` | `"[#S] "` | 상태바 왼쪽에 표시할 포맷 문자열(기본값은 세션 이름) |
| `status-left-length` | 10 | 왼쪽 영역의 최대 길이(글자 수) |
| `status-right` | 창 제목·날짜·시간 | 상태바 오른쪽에 표시할 포맷 문자열 |
| `status-right-length` | 40 | 오른쪽 영역의 최대 길이 |
| `status-left-style`/`status-right-style`/`status-style` | - | 각 영역의 색·속성(STYLES 문법, 아래 참고) |

자주 쓰는 포맷 변수(및 짧은 별칭)는 다음과 같다.

| 변수 | 별칭 | 의미 |
|---|---|---|
| `#{session_name}` | `#S` | 세션 이름 |
| `#{window_name}` | `#W` | 윈도우 이름 |
| `#{window_index}` | `#I` | 윈도우 번호 |
| `#{pane_index}` | `#P` | 패널 번호 |
| `#{pane_title}` | `#T` | 패널 제목(실행 중인 프로그램이 설정) |
| `#{host}` | `#H` | 로컬 호스트 이름 |

스타일은 `fg=색상`(글자색), `bg=색상`(배경색), `bold`/`underscore` 같은 속성을 공백이나 쉼표로 나열해 지정한다. 색상은 `red`/`blue` 같은 이름, `colour0`~`colour255`, `#ffffff` 같은 16진 RGB 중 하나를 쓸 수 있다.

## 예시

### 지금 상태바 설정 확인하기

```bash
tmux show-options -g status-left
tmux show-options -g status-right
```

### 세션·호스트 정보를 담은 상태바 구성하기

```bash
# ~/.tmux.conf
set -g status-left-length 30
set -g status-left "#[fg=green,bold][#S]#[default] #{host} "

set -g status-right-length 60
set -g status-right "#[fg=cyan]%Y-%m-%d %H:%M#[default]"

set -g status-style "bg=black,fg=white"
```

### 조건부 표현식으로 상태에 따라 다르게 표시하기

`#{?조건,참일때,거짓일때}` 형태의 조건부를 쓰면, 03장에서 다룬 "이 세션에 몇 명이 attach했는가" 같은 정보도 상태바에서 바로 확인할 수 있다.

```bash
# 이 세션에 다른 클라이언트가 붙어 있으면 "shared", 아니면 "solo"를 표시
set -g status-right "#{?session_many_attached,shared,solo} #{host}"
```

## 비교/트레이드오프

상태바에 정보를 얼마나 담을지는 취향과 화면 크기의 트레이드오프다.

| 구분 | 최소 정보(기본값에 가까움) | 풍부한 정보(여러 포맷 변수 조합) |
|---|---|---|
| 가독성 | 한눈에 들어온다 | 정보가 많을수록 훑어보는 데 시간이 걸린다 |
| 화면 공간 | 좁은 터미널에서도 안 잘림 | `status-*-length`를 넉넉히 잡지 않으면 잘리기 쉽다 |
| 유용성 | 세션·윈도우 이름 정도만 확인 가능 | 접속자 수, 경로, 시간 등을 한 화면에서 모니터링 가능 |
| 적합한 상황 | 노트북처럼 화면이 좁은 환경 | 넓은 모니터, 운영 대시보드처럼 여러 정보를 항상 봐야 하는 환경 |

## 주의사항·함정

**길이 제한으로 잘리는 커스텀 상태바**: `status-left-length`(기본 10)와 `status-right-length`(기본 40)는 생각보다 짧다. 포맷 문자열을 길게 바꿔놓고 길이 옵션은 그대로 두면, 애써 만든 내용이 중간에서 잘려 나온다. 커스텀 문자열을 늘릴 때는 반드시 길이 옵션도 함께 늘린다.

**조건부 표현식 안의 특수문자 이스케이프**: `#{?...}` 조건부 안에서 쉼표(`,`)나 닫는 중괄호(`}`)를 문자 그대로 쓰고 싶다면 `#,`, `#}`처럼 이스케이프해야 한다. 그냥 쓰면 조건부의 인자 구분자로 오인돼 파싱이 깨진다.

**`status-interval 0`의 부작용**: 갱신 주기를 0으로 끄면 CPU 사용량이 살짝 줄어들 수 있지만, 시계처럼 시간이 지나야 값이 바뀌는 포맷 변수도 더 이상 자동으로 갱신되지 않는다. 시간 표시가 필요한 상태바에서는 이 옵션을 함부로 0으로 두지 않는다.

## 흔한 오개념

<strong>"상태바는 한 번 그려지면 tmux를 재시작하기 전까진 안 바뀐다"</strong>는 생각은 틀렸다. `status-interval`이 지정한 주기마다 포맷 문자열이 다시 평가되므로, 시간·접속자 수처럼 변하는 값은 그때그때 갱신된다.

<strong>"`#S`, `#W` 같은 짧은 별칭이 쓸 수 있는 전부다"</strong>는 오해도 흔하다. 실제로는 훨씬 많은 값이 `#{변수명}` 형태로 존재하며, `#S` 같은 짧은 별칭은 그중 자주 쓰이는 몇 개에만 주어진 축약형이다.

<strong>"스타일은 `status-style` 하나로만 정할 수 있다"</strong>는 생각도 정확하지 않다. `status-left-style`/`status-right-style`로 좌우를 따로 지정할 수 있고, `#[fg=...,bg=...]`를 포맷 문자열 중간에 끼워 넣으면 한 문자열 안에서도 구간별로 다른 스타일을 줄 수 있다.

## 다음 장에서는

[09장: 레이아웃과 패널 동기화 - synchronize-panes](/post/tmux/tmux-layout-synchronize-panes/)부터는 3부(고급 조작)로 넘어가, 여러 패널을 미리 정의된 레이아웃으로 한 번에 배치하고 동시에 조작하는 법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- 상태바가 `status-interval` 주기로 다시 그려진다는 것을 설명하고, 그 주기를 조정할 수 있다.
- `status-left`/`status-right`에 포맷 변수(`#S`, `#{host}` 등)를 조합해 원하는 정보를 표시할 수 있다.
- `fg=`/`bg=`/속성으로 상태바 각 영역의 스타일을 지정할 수 있다.
- 조건부 표현식(`#{?조건,참,거짓}`)으로 상태에 따라 다른 내용을 표시할 수 있다.
- `status-*-length`가 잘림 문제의 원인이 될 수 있음을 진단하고 조정할 수 있다.

## 참고 및 출처

1. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — `status-*` 옵션, FORMATS(포맷 변수·조건부 표현식), STYLES(`fg=`/`bg=`/속성) 공식 설명.
2. [tmux/tmux](https://github.com/tmux/tmux) — tmux 공식 소스 저장소.
