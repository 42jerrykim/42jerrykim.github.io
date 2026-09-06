---
draft: false
slug: tmux-plugin-manager-tpm-ecosystem
title: "[Tmux] 15. 플러그인 생태계와 TPM"
description: "TPM(Tmux Plugin Manager)을 설치하고, tmux.conf에 플러그인 목록을 선언해 prefix+I/U/alt+u로 설치·업데이트·제거하는 법을 다룹니다. 설정 순서 함정과 대안 도구까지 공식 문서 기준으로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 15
categories:
- Tmux
tags:
- Tmux
- Terminal
- Shell(셸)
- OS(운영체제)
- Open-Source(오픈소스)
- Configuration(설정)
- Version-Control(버전관리)
- Keyboard(키보드)
- Comparison(비교)
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

14장까지는 세션·레이아웃을 자동화하는 도구를 다뤘다. 이 장부터는 tmux 자체의 기능을 확장하는 <strong>플러그인 생태계</strong>를 다룬다. 그 시작은 플러그인을 설치·관리해 주는 사실상의 표준 도구, <strong>TPM(Tmux Plugin Manager)</strong>이다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [14장: tmuxinator와 tmuxifier](/post/tmux/tmuxinator-tmuxifier-project-layout-management/)에서 다룬 서드파티 도구에 이어, tmux 기능 자체를 확장하는 플러그인 매니저를 다룬다. 06장에서 배운 `tmux.conf` 문법과 reload 개념을 그대로 활용한다.

**이 장의 깊이**: **입문** 난이도다. **다루지 않는 것**: 개별 플러그인(예: 세션 저장·자동 복구, 클립보드 연동)의 구체적인 사용법은 16장에서 다룬다. 이 장은 TPM이라는 매니저 자체의 설치·설정·조작에 집중한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 플러그인을 써 본 적 없는 사람 | 정신 모델, 설치와 설정, 예시 | TPM을 설치하고 첫 플러그인을 추가할 수 있다 |
| 플러그인을 수동으로 git clone해 관리해 온 사람 | 비교/트레이드오프 | TPM으로 전환했을 때의 이점을 판단할 수 있다 |
| 설정을 추가했는데 플러그인이 안 보이는 사람 | 주의사항·함정 | `run` 줄의 위치, 설치와 업데이트의 차이를 진단할 수 있다 |
| 오래된 서버에 TPM을 쓰려는 사람 | 주의사항·함정(요구사항) | tmux 버전 등 요구사항을 미리 확인할 수 있다 |

## 정신 모델: 플러그인 목록을 선언하면 TPM이 설치·로드한다

TPM의 동작 방식은 06장에서 배운 설정 파일의 연장선에 있다. `tmux.conf`에 `set -g @plugin '...'` 줄로 원하는 플러그인을 하나씩 선언하고, 파일 맨 끝에 TPM 자신을 초기화하는 `run` 줄을 둔다. tmux가 설정 파일을 읽을 때 이 `run` 줄이 실행되면서 TPM이 활성화되고, 선언된 플러그인 목록을 인식한다. 실제로 플러그인을 내려받아 설치하는 것은 별도의 키 입력(`prefix` + `I`)으로 트리거되는 능동적인 동작이다 — 설정 파일에 적어 넣는 것과 실제 설치는 분리된 단계다.

## 설치와 설정

TPM은 tmux 1.9 이상, `git`, `bash`가 있으면 리눅스·macOS·Cygwin에서 동작한다.

```bash
# TPM 저장소를 클론한다
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

`tmux.conf` 맨 아래에 아래 블록을 추가한다. `run` 줄은 반드시 파일의 <strong>가장 마지막</strong>에 있어야 한다.

```bash
# ~/.tmux.conf

# 플러그인 목록
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'

# 다른 형식 예시
# set -g @plugin 'github_username/plugin_name'
# set -g @plugin 'github_username/plugin_name#branch'
# set -g @plugin 'git@github.com:user/plugin'
# set -g @plugin 'git@bitbucket.com:user/plugin'

# TPM 초기화 (항상 파일의 맨 마지막 줄)
run '~/.tmux/plugins/tpm/tpm'
```

06장에서 배운 대로 설정을 반영한다.

```bash
tmux source ~/.tmux.conf
```

## 키바인딩

TPM은 대문자와 소문자 조합으로 설치·업데이트·제거를 구분한다. 대문자 `I`(Install)와 `U`(Update)는 각각 새 플러그인 설치와 기존 플러그인 갱신을 맡고, 소문자가 섞인 `Alt+u`(uninstall)는 목록에서 빠진 플러그인을 실제로 지우는 별도 동작이다.

| 키 | 동작 |
|---|---|
| `prefix` + `I`(대문자) | 목록에 새로 추가한 플러그인을 설치하고 tmux 환경을 새로고침한다 |
| `prefix` + `U`(대문자) | 이미 설치된 플러그인을 최신 버전으로 업데이트한다 |
| `prefix` + `Alt` + `u`(소문자) | 목록에서 제거(주석 처리 포함)한 플러그인을 실제로 삭제한다 |

## 예시

### 플러그인 추가하고 설치하기

```bash
# tmux.conf에 플러그인 한 줄 추가
set -g @plugin 'tmux-plugins/tmux-sensible'
```

설정 파일을 저장한 뒤 `prefix` 뒤 `I`를 누르면, 이 플러그인이 `~/.tmux/plugins/` 아래로 clone되고 즉시 로드된다.

### 업데이트와 제거

```text
prefix 뒤 U             → 설치된 모든 플러그인을 최신 버전으로 갱신
(tmux.conf에서 플러그인 줄을 지우거나 주석 처리한 뒤)
prefix 뒤 Alt+u         → 목록에서 빠진 플러그인을 실제로 삭제
```

## 비교/트레이드오프

플러그인을 관리하는 방법은 TPM을 쓰는 것과 직접 관리하는 것으로 나뉜다.

| 구분 | TPM 사용 | 수동 관리(직접 `git clone` + `run`) |
|---|---|---|
| 추가 절차 | `tmux.conf`에 한 줄 추가 후 `prefix I` | 저장소를 직접 clone하고 `run` 줄을 손으로 추가 |
| 업데이트 | `prefix U` 한 번으로 일괄 처리 | 각 플러그인 디렉터리에서 직접 `git pull` |
| 제거 | 목록에서 지우고 `prefix Alt+u` | 디렉터리를 직접 삭제하고 설정도 함께 정리 |
| 적합한 상황 | 플러그인을 여러 개 쓰거나 자주 바꾸는 경우 | 플러그인이 한두 개뿐이고 세세한 제어가 필요한 경우 |

TPM이 사실상 표준이지만 유일한 선택지는 아니다. `tpack`처럼 TUI와 자동 업데이트를 갖춘 대안 매니저도 존재하므로, TPM의 최소한의 인터페이스가 부족하게 느껴진다면 대안을 검토할 수 있다.

## 주의사항·함정

**`run` 줄의 위치**: TPM 초기화 줄은 반드시 `tmux.conf`의 가장 마지막에 있어야 한다. 이 줄보다 뒤에 다른 설정을 추가하면 그 설정이 TPM 관련 동작과 충돌하거나 예상대로 로드되지 않을 수 있다.

**설치(`I`)와 업데이트(`U`)는 다른 동작이다**: 새로 추가한 플러그인은 `prefix I`로 처음 설치해야 하고, 이미 설치된 플러그인을 최신 버전으로 갱신하는 것은 `prefix U`다. `U`만 반복해서는 새로 목록에 추가한 플러그인이 인식되지 않는다.

**오래된 환경에서의 요구사항 미달**: TPM은 tmux 1.9 이상과 `git`을 요구한다. 02장에서 다룬 것처럼 오래된 배포판의 패키지 저장소 버전이 이 기준보다 낮으면, TPM 자체가 정상 동작하지 않을 수 있으므로 `tmux -V`로 먼저 버전을 확인한다.

## 흔한 오개념

<strong>"tmux.conf에 플러그인을 적기만 하면 자동으로 설치된다"</strong>는 생각은 틀렸다. 설정 파일에 선언하는 것은 TPM에게 "이 플러그인을 관리 대상으로 알아 두라"는 신호일 뿐이며, 실제 설치는 `prefix I`를 눌러야 일어난다.

<strong>"`prefix U` 한 번이면 새로 추가한 플러그인도 함께 잡힌다"</strong>는 오해도 흔하다. 업데이트는 이미 설치된 플러그인의 버전을 갱신할 뿐이고, 새 플러그인은 별도로 설치(`prefix I`) 단계를 거쳐야 한다.

<strong>"TPM이 유일한 플러그인 관리 방법이다"</strong>는 생각도 정확하지 않다. TPM이 커뮤니티에서 가장 널리 쓰이지만, `tpack`처럼 TUI와 자동 업데이트를 지원하는 대안도 있고, 플러그인을 아예 손으로 clone해 관리하는 것도 가능하다.

## 다음 장에서는

[16장: 필수 플러그인 실전 - resurrect·continuum·yank](/post/tmux/tmux-resurrect-continuum-yank-essential-plugins/)에서는 TPM으로 실제로 설치해 쓰는 대표적인 플러그인 세 가지를 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- TPM을 설치하고 `tmux.conf`에 플러그인 목록을 선언할 수 있다.
- `prefix I`(설치)와 `prefix U`(업데이트)의 차이를 설명할 수 있다.
- `run` 줄이 왜 설정 파일의 맨 마지막에 있어야 하는지 설명할 수 있다.
- 플러그인을 제거할 때 목록 삭제와 `prefix Alt+u`가 왜 함께 필요한지 설명할 수 있다.
- TPM과 수동 관리, 그리고 대안 도구 사이의 트레이드오프를 판단할 수 있다.

## 참고 및 출처

1. [tmux-plugins/tpm](https://github.com/tmux-plugins/tpm) — 공식 README, 설치·설정·키바인딩·요구사항.
2. [tmux/tmux](https://github.com/tmux/tmux) — tmux 공식 소스 저장소.
