---
draft: false
slug: tmux-vs-screen-zellij-wezterm-comparison
title: "[Tmux] 19. 대안 도구 비교 - screen, Zellij, WezTerm"
description: "GNU screen, Zellij, WezTerm을 tmux와 비교합니다. 각 도구의 설계 철학(최소주의, 발견형 UI와 협업, 터미널 자체에 내장된 멀티플렉싱) 차이와 언제 tmux 대신 고려할 만한지를 다룹니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 19
categories:
- Tmux
tags:
- Tmux
- Terminal
- Comparison(비교)
- Open-Source(오픈소스)
- OS(운영체제)
- GPU(Graphics Processing Unit)
- Collaboration(협업)
- Configuration(설정)
- Session(세션)
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

5부(통합과 비교)의 마지막 장이다. 지금까지 tmux 하나에 집중해 왔다면, 이 장은 시야를 넓혀 tmux의 자리를 상대화한다. <strong>GNU screen</strong>(tmux보다 오래된 원조 격), <strong>Zellij</strong>(현대적으로 다시 설계된 대안), <strong>WezTerm</strong>(멀티플렉싱을 터미널 에뮬레이터 자체에 내장한 도구)을 비교하며, 각각 언제 tmux 대신 고려할 만한지 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [18장: tmux와 Vim/Neovim 통합](/post/tmux/tmux-vim-neovim-integration-navigator/)으로 5부의 통합 이야기를 마무리하며, 01장에서 짧게 언급했던 GNU screen과의 관계를 본격적으로 다룬다.

**이 장의 깊이**: **입문**에서 **중급**(각 도구의 설계 철학 차이를 근거로 상황별 선택을 판단할 수 있는 수준) 사이를 오간다. **다루지 않는 것**: 각 대안 도구의 상세한 조작법(예: Zellij의 실제 단축키, WezTerm의 Lua 설정 문법)은 이 컬렉션의 범위 밖이다. 이 장은 "tmux와 무엇이, 왜 다른가"에 집중한다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| tmux만 써 봤고 대안을 궁금해하는 사람 | 정신 모델, 각 도구 소개, 비교표 | 세 대안 도구가 tmux와 근본적으로 무엇이 다른지 이해한다 |
| GNU screen에 익숙한 사람 | GNU screen 절, 주의사항·함정 | screen과 tmux의 키바인딩이 왜 호환되지 않는지 설명할 수 있다 |
| 팀 협업이나 최신 UX를 중시하는 사람 | Zellij 절, 비교/트레이드오프 | Zellij가 강점을 갖는 상황을 판단할 수 있다 |
| 로컬 개발 환경을 새로 꾸미는 사람 | WezTerm 절, 흔한 오개념 | WezTerm의 내장 멀티플렉싱이 tmux를 완전히 대체하지 못하는 이유를 이해한다 |

## 정신 모델: 세 가지 서로 다른 설계 철학

이 세 도구는 tmux의 "열등한 대체재"가 아니라, 각자 다른 문제를 우선시하도록 설계됐다. GNU screen은 tmux보다 먼저 나온 원조 격 도구로 최소한의 기능에 집중한다. Zellij는 러스트로 처음부터 다시 설계되어 발견 가능한 UI와 협업을 중시한다. WezTerm은 애초에 별도의 멀티플렉서 프로그램을 두지 않고, 터미널 에뮬레이터 자신에게 탭·분할 기능을 내장한다. 이 마지막 차이가 특히 근본적이다 — tmux는 어떤 터미널 에뮬레이터 위에서도 동일하게 동작하는 반면, WezTerm의 멀티플렉싱은 WezTerm이라는 특정 터미널 앱 안에서만 유효하다.

## GNU screen: tmux 이전의 원조

| 항목 | 내용 |
|---|---|
| 기본 prefix | `Ctrl-a` |
| 세션 재연결 | `screen -r`로 분리된 세션에 다시 접속 |
| 세션 목록 | `screen -list` |
| 이름 지정 | `screen -S 이름`으로 새 세션에 이름을 붙인다 |

01장에서 다뤘듯, tmux는 screen이 먼저 제공하던 터미널 분리 개념을 이어받으면서도 서버-클라이언트 구조와 키바인딩 체계를 다시 설계했다. 그래서 기능은 많이 겹치지만 기본 단축키를 그대로 옮겨 쓸 수 있는 완전한 호환 관계는 아니다.

## Zellij: 발견 가능한 UI와 협업 중심의 재해석

Zellij는 자신을 "배터리가 포함된 터미널 워크스페이스"로 소개하며, 러스트로 작성됐다.

| 특징 | 설명 |
|---|---|
| 발견 가능한 UI | 화면 하단에 지금 누를 수 있는 키 힌트를 항상 보여줘, 단축키를 외우지 않아도 조작할 수 있다 |
| 플러그인 시스템 | WebAssembly로 컴파일되는 언어라면 무엇으로든 플러그인을 만들 수 있다 |
| 레이아웃 | 파일로 미리 정의한 배치를 불러와 "개인 자동화"를 지원한다(14장에서 다룬 tmuxinator·tmuxifier와 목적이 비슷하다) |
| 협업 | 여러 사람이 진짜로 함께 세션을 다루는 협업 기능과 내장 웹 클라이언트를 제공한다 |

## WezTerm: 터미널과 멀티플렉서의 통합

WezTerm은 GPU 가속을 쓰는 크로스플랫폼 터미널 에뮬레이터이자 멀티플렉서다.

| 특징 | 설명 |
|---|---|
| 아키텍처 | 별도 멀티플렉서 프로그램 없이, 터미널 에뮬레이터 자체가 탭·분할·SSH 도메인을 제공한다 |
| 렌더링 | GPU 가속으로 스크롤과 텍스트 렌더링이 빠르다 |
| 설정 | Lua 스크립트로 설정하며, 같은 설정을 Windows·macOS·Linux에서 동일하게 쓸 수 있다 |
| 지원 플랫폼 | Windows, macOS, Linux, FreeBSD |

## 네 도구 한눈에 비교

| 구분 | tmux | GNU screen | Zellij | WezTerm |
|---|---|---|---|---|
| 기반 언어 | C | C | Rust | Rust |
| 설정 방식 | tmux 자체 명령 문법(`tmux.conf`) | screen 자체 설정(`.screenrc`) | YAML/KDL 레이아웃 | Lua |
| UI 힌트 | 없음(단축키 암기 필요) | 없음 | 화면 하단에 상시 표시 | 터미널 자체 UI에 통합 |
| 플러그인 생태계 | TPM 기반 커뮤니티 플러그인(15–16장) | 제한적 | WASM 기반 | Lua API 기반 |
| 멀티플렉서 위치 | 어떤 터미널 위에서도 동작하는 독립 계층 | 어떤 터미널 위에서도 동작하는 독립 계층 | 어떤 터미널 위에서도 동작하는 독립 계층 | 터미널 자신에게 내장 |

## 비교/트레이드오프

| 상황 | 권장 |
|---|---|
| 원격 서버에 SSH로 접속해 세션을 유지해야 함 | tmux 또는 screen(설치된 쪽) — 터미널 앱과 무관하게 동작 |
| 팀원과 실시간으로 화면을 함께 조작하며 UI 힌트도 필요 | Zellij의 협업·발견형 UI가 강점 |
| 로컬 개발 환경의 렌더링 성능과 설정 편의성을 우선 | WezTerm 하나로 터미널과 멀티플렉서를 겸함 |
| 오래된 서버, 설치할 수 있는 패키지가 제한적 | 이미 설치돼 있을 가능성이 높은 tmux나 screen |

이 표가 보여주듯 선택 기준은 "로컬에서 쓰는가, 원격 서버에서도 써야 하는가"로 크게 갈린다. WezTerm의 내장 멀티플렉싱은 로컬 작업에는 강력하지만, WezTerm이 깔려 있지 않은 원격 서버에 SSH로 접속하는 순간에는 그 이점을 쓸 수 없다.

## 주의사항·함정

**screen과 tmux는 키바인딩이 호환되지 않는다**: 기본 prefix부터 다르고(`Ctrl-a` vs `Ctrl-b`), 다른 단축키도 그대로 옮겨지지 않는다. 한쪽에 익숙한 사람이 다른 쪽을 처음 쓰면 손에 익은 습관이 오히려 방해가 될 수 있다.

**WezTerm의 멀티플렉싱은 WezTerm 안에서만 유효하다**: 로컬에서 WezTerm의 탭·분할을 쓰다가 SSH로 원격 서버에 접속하면, 그 원격 서버 안에서는 여전히 tmux나 screen 같은 원격 세션 지속성 도구가 따로 필요하다.

**Zellij는 상대적으로 최신 도구다**: 02장에서 다뤘던 "오래된 배포판의 패키지가 최신 도구를 지원하지 않을 수 있다"는 문제가 Zellij에는 더 크게 적용될 수 있다. 오래된 서버라면 아예 패키지 저장소에 없을 가능성도 염두에 둔다.

## 흔한 오개념

<strong>"더 새로운 도구가 나오면 무조건 갈아타야 한다"</strong>는 생각은 틀렸다. 각 도구는 우열 관계가 아니라 서로 다른 문제를 우선시하도록 설계된 것이므로, 자신의 상황(원격 서버 작업 비중, 협업 필요성, 렌더링 성능 등)에 맞는 도구를 고르는 것이 중요하다.

<strong>"WezTerm을 쓰면 tmux가 아예 필요 없어진다"</strong>는 오해도 흔하다. 로컬 작업만 한다면 맞는 말일 수 있지만, WezTerm이 설치되지 않은 원격 서버에 접속하는 순간 그 서버 안의 세션 지속성은 여전히 tmux나 screen에 의존해야 한다.

<strong>"Zellij가 최신이니 모든 면에서 tmux보다 낫다"</strong>는 생각도 정확하지 않다. 발견형 UI와 협업 기능은 강점이지만, 커뮤니티 플러그인·설정 공유의 성숙도나 오래된 환경에서의 설치 가능성은 아직 tmux가 앞서 있는 경우가 많다.

## 다음 장에서는

[20장: 트러블슈팅 - 클립보드·색상·중첩 세션](/post/tmux/tmux-troubleshooting-clipboard-colors-nested-sessions/)부터는 6부(실전과 마무리)로 넘어가, 지금까지 여러 챕터에서 예고했던 색상 깨짐·클립보드 미동작·중첩 세션 같은 문제를 진단하고 해결하는 법을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- GNU screen, Zellij, WezTerm이 각각 어떤 설계 철학을 우선시하는지 설명할 수 있다.
- WezTerm의 멀티플렉싱이 tmux와 근본적으로 다른 계층에 있다는 것을 설명할 수 있다.
- screen과 tmux의 키바인딩이 호환되지 않는 이유를 설명할 수 있다.
- 원격 서버 작업 비중, 협업 필요성, 렌더링 성능 등을 기준으로 상황에 맞는 도구를 선택할 수 있다.
- 최신 도구가 무조건 더 낫다는 가정 없이, 각 도구의 트레이드오프를 비판적으로 판단할 수 있다.

## 참고 및 출처

1. [GNU Screen Manual](https://www.gnu.org/software/screen/manual/screen.html) — prefix 키, 세션 재연결·목록·이름 지정 공식 설명.
2. [zellij-org/zellij](https://github.com/zellij-org/zellij) — 공식 README, 설계 철학과 기능 소개.
3. [wezterm/wezterm](https://github.com/wezterm/wezterm) — 공식 저장소, GPU 가속·멀티플렉싱·Lua 설정 소개.
