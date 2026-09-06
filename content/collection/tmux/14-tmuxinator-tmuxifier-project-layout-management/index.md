---
draft: false
slug: tmuxinator-tmuxifier-project-layout-management
title: "[Tmux] 14. tmuxinator와 tmuxifier - 프로젝트 레이아웃 관리"
description: "13장에서 손으로 짠 부트스트랩 스크립트를 프로젝트별 설정 파일로 관리해 주는 두 도구, tmuxinator(Ruby·YAML)와 tmuxifier(순수 셸 스크립트)를 비교합니다. 설치·설정 파일 형식·명령을 공식 문서 기준으로 다룹니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 14
categories:
- Tmux
tags:
- Tmux
- Terminal
- Shell(셸)
- YAML(YAML Ain't Markup Language)
- Open-Source(오픈소스)
- Automation(자동화)
- Configuration(설정)
- DevOps
- Version-Control(버전관리)
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

13장에서는 세션·윈도우·패널 구성을 tmux 명령만으로 손수 스크립팅했다. 이 장은 그 방식을 프로젝트별 설정 파일로 표준화해 주는 두 커뮤니티 도구 — <strong>tmuxinator</strong>(Ruby gem, YAML 설정)와 <strong>tmuxifier</strong>(순수 셸 스크립트) — 를 다룬다. 둘 다 근본적으로는 13장에서 배운 tmux 명령을 대신 실행해 주는 래퍼다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [13장: tmux 커맨드라인과 스크립팅](/post/tmux/tmux-command-line-scripting-send-keys/)에서 손으로 짠 부트스트랩 스크립트를, 프로젝트 이름 하나로 저장·재현하는 전용 도구로 확장한다.

**이 장의 깊이**: **입문**에서 **중급**(두 도구의 설정 철학 차이를 이해하고 상황에 맞게 고를 수 있는 수준) 사이를 오간다. **다루지 않는 것**: tmux 플러그인을 관리하는 TPM 자체는 15장에서, 세션 저장·자동 복구 같은 개별 플러그인은 16장에서 각각 다룬다. tmuxinator·tmuxifier는 tmux 자체 기능이 아니라 별도로 설치하는 서드파티 도구라는 점에 유의한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 13장의 부트스트랩 스크립트를 파일로 관리하고 싶은 사람 | 정신 모델, tmuxinator, tmuxifier | 두 도구 중 자신에게 맞는 것을 선택해 프로젝트 레이아웃을 저장·재현할 수 있다 |
| Ruby 생태계에 거부감이 없는 사람 | tmuxinator 절 | YAML로 선언적인 프로젝트 설정을 작성할 수 있다 |
| 셸 스크립트에 이미 익숙한 사람 | tmuxifier 절 | 함수 호출로 이루어진 레이아웃 파일을 작성할 수 있다 |
| 기존 tmux 세션을 설정 파일로 뽑아내고 싶은 사람 | tmuxinator 예시(세션 역생성) | 이미 만들어 둔 세션 구성을 설정 파일로 저장할 수 있다 |

## 정신 모델: 13장 스크립트를 파일로 정형화한 것

tmuxinator와 tmuxifier가 하는 일은 근본적으로 13장에서 손으로 짠 것과 같다 — 세션을 만들고, 윈도우를 나누고, 각 자리에 명령을 실행시킨다. 차이는 그 과정을 어떤 형식으로 표현하느냐에 있다. tmuxinator는 "무엇을 원하는가"를 YAML로 선언하면 도구가 알아서 tmux 명령으로 옮겨 실행하는 <strong>선언형</strong> 접근이고, tmuxifier는 "어떤 순서로 무엇을 할지"를 셸 함수 호출로 그대로 적는 <strong>명령형</strong> 접근이다.

## tmuxinator: Ruby gem과 YAML 설정

tmuxinator는 Ruby gem으로 배포되며, 공식 문서는 `gem install tmuxinator`를 권장한다. Homebrew로도 설치할 수 있지만(`brew install tmuxinator`), 공식 문서는 Homebrew 설치에서 보고된 문제들 때문에 문제가 해결될 때까지 RubyGems 설치를 우선하라고 명시한다.

```bash
gem install tmuxinator

# 새 프로젝트 설정 생성 (기본적으로 $EDITOR로 열림)
tmuxinator new myproject
```

새 프로젝트를 만들면 아래와 비슷한 YAML 템플릿이 생성된다.

```yaml
name: myproject
root: ~/code/myproject

windows:
  - editor:
      layout: main-vertical
      panes:
        - editor: vim
        - guard
  - server: bundle exec rails s
  - logs: tail -f log/development.log
```

| 명령 | 설명 |
|---|---|
| `tmuxinator start [project]` | 설정대로 세션을 만들고 접속한다 |
| `tmuxinator stop [project]` | 해당 프로젝트의 세션을 종료한다 |
| `tmuxinator list`(`l`/`ls`) | 등록된 모든 프로젝트를 나열한다 |
| `tmuxinator copy [기존] [새이름]`(`c`/`cp`) | 기존 설정을 복사해 새 프로젝트를 만든다 |
| `tmuxinator delete [project]`(`rm`) | 프로젝트 설정을 삭제한다 |
| `tmuxinator doctor` | 환경을 점검해 설정 문제를 진단한다 |
| `tmuxinator debug [project]` | 실제로 실행될 셸 명령을 미리 보여준다 |

이미 손으로 만들어 둔 tmux 세션이 있다면, 그 구성을 그대로 새 설정 파일로 뽑아낼 수도 있다.

```bash
# 지금 떠 있는 세션 "myproject"의 윈도우·레이아웃·루트 경로를 그대로 옮겨 새 tmuxinator 설정을 만든다
tmuxinator new myproject myproject
```

## tmuxifier: 순수 셸 스크립트 기반

tmuxifier는 Ruby 같은 별도 런타임 없이 셸 스크립트만으로 동작한다. 저장소를 클론하고 `bin` 디렉터리를 `PATH`에 추가한 뒤, 셸 프로필에 초기화 구문을 추가해야 명령이 인식된다.

```bash
git clone https://github.com/jimeh/tmuxifier.git ~/.tmuxifier
export PATH="$HOME/.tmuxifier/bin:$PATH"

# ~/.bashrc 또는 ~/.zshrc 등에 추가
eval "$(tmuxifier init -)"
```

tmuxifier는 <strong>윈도우 레이아웃</strong>(`.window.sh`)과 <strong>세션 레이아웃</strong>(`.session.sh`) 두 종류의 파일을 구분한다. 윈도우 레이아웃은 `new_window`/`window_root`/`split_v`/`split_h`/`run_cmd`/`select_pane` 같은 헬퍼 함수를 순서대로 호출해 하나의 윈도우를 구성한다.

```bash
# my-window.window.sh
window_root "~/code/myproject"
new_window "editor"
split_v 20
run_cmd "tail -f log/development.log"
split_h 60
select_pane 0
```

세션 레이아웃은 이렇게 만든 윈도우 레이아웃을 `load_window`로 불러 모아 하나의 세션으로 묶는다.

```bash
tmuxifier new-window my-window      # my-window.window.sh 생성 + 편집기로 열기
tmuxifier new-session my-project    # my-project.session.sh 생성(안에 load_window "my-window" 추가)
tmuxifier load-session my-project   # 실제로 세션을 만들어 접속
```

## 비교/트레이드오프

세 가지 방식(13장의 직접 스크립팅, tmuxinator, tmuxifier)은 서로 다른 트레이드오프를 가진다.

| 구분 | 13장 직접 스크립팅 | tmuxinator | tmuxifier |
|---|---|---|---|
| 설정 형식 | 자유로운 셸 스크립트 | YAML(선언형) | 셸 함수 호출(명령형) |
| 의존성 | 없음(tmux만 있으면 됨) | Ruby, gem | 없음(셸만 있으면 됨) |
| 프로젝트 전환 | 스크립트 파일을 직접 찾아 실행 | `tmuxinator start 이름` | `tmuxifier load-session 이름` |
| 적합한 상황 | 아주 단순하거나 일회성인 구성 | 팀 전체가 같은 YAML을 공유해야 하는 경우 | 별도 런타임 설치 없이 가볍게 쓰고 싶은 경우 |

## 주의사항·함정

**설정 파일은 프로젝트 저장소에 함께 커밋한다**: tmuxinator의 YAML이나 tmuxifier의 셸 레이아웃 파일은 결국 텍스트 파일이므로, 개인 홈 디렉터리에만 남겨두기보다 프로젝트 저장소에 커밋해 버전 관리하면 팀원 모두가 같은 명령 한 줄로 동일한 개발 환경을 재현할 수 있다. 이는 CI 파이프라인이나 새 팀원 온보딩 스크립트에도 그대로 재사용할 수 있는 자산이 된다.

**Homebrew로 설치한 tmuxinator의 알려진 문제**: 공식 문서는 Homebrew 설치에서 보고된 이슈들 때문에 RubyGems(`gem install`) 설치를 권장한다. Homebrew로 설치한 뒤 이상 동작이 있다면 이 차이부터 의심한다.

**프로젝트 이름에 점(`.`)을 쓸 수 없다**: tmux가 내부적으로 `세션:윈도우.패널` 형식에서 점을 구분자로 쓰기 때문에, tmuxinator 프로젝트 이름에 점이 들어가면 충돌한다.

**tmuxifier 초기화를 빼먹는 실수**: 저장소만 클론하고 셸 프로필에 `eval "$(tmuxifier init -)"`를 추가하지 않으면 `tmuxifier` 명령 자체를 셸이 찾지 못한다. 설치 직후 명령이 안 먹힌다면 이 초기화 단계부터 확인한다.

## 흔한 오개념

<strong>"tmuxinator·tmuxifier는 tmux를 대체하는 새로운 도구다"</strong>는 생각은 틀렸다. 둘 다 13장에서 배운 tmux 명령을 대신 실행해 주는 래퍼일 뿐이며, tmux 자체가 설치돼 있어야 동작한다.

<strong>"두 도구의 설정 파일 형식은 비슷하다"</strong>는 오해도 흔하다. tmuxinator는 YAML로 원하는 결과를 선언하고, tmuxifier는 셸 함수를 순서대로 호출하는 명령형 스크립트를 쓴다는 점에서 철학 자체가 다르다.

<strong>"tmuxinator new는 항상 빈 템플릿만 만들어 준다"</strong>는 생각도 정확하지 않다. `tmuxinator new [project] [session]`처럼 기존 세션 이름을 함께 주면, 그 세션의 윈도우·레이아웃·루트 경로를 그대로 옮겨 새 설정 파일을 만들어 준다.

## 다음 장에서는

[15장: 플러그인 생태계와 TPM](/post/tmux/tmux-plugin-manager-tpm-ecosystem/)에서는 tmuxinator·tmuxifier 같은 외부 도구를 넘어, tmux 플러그인을 설치·관리하는 표준 도구 TPM을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- tmuxinator와 tmuxifier가 근본적으로 13장의 스크립팅을 파일로 정형화한 것이라는 점을 설명할 수 있다.
- tmuxinator의 YAML 설정과 tmuxifier의 셸 함수 방식의 철학적 차이(선언형 vs 명령형)를 설명할 수 있다.
- 두 도구를 설치하고 각각의 방식으로 프로젝트 레이아웃을 만들 수 있다.
- 기존 tmux 세션을 tmuxinator 설정으로 역생성할 수 있다.
- 상황(팀 공유 vs 가벼운 개인 설정)에 따라 어떤 도구를 선택할지 판단할 수 있다.

## 참고 및 출처

1. [tmuxinator/tmuxinator](https://github.com/tmuxinator/tmuxinator) — 공식 README, 설치·명령·설정 파일 형식.
2. [jimeh/tmuxifier](https://github.com/jimeh/tmuxifier) — 공식 README, 설치·윈도우/세션 레이아웃 문법.
3. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — 두 도구가 감싸는 기반 tmux 명령 참고.
