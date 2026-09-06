---
draft: false
slug: tmux-swap-move-break-join-pane-window
title: "[Tmux] 11. 윈도우/패널 재배치 - swap·move·break·join"
description: "swap-window/swap-pane으로 위치를 맞바꾸고, move-window로 번호를 옮기고, break-pane으로 패널을 독립 윈도우로 떼어낸 뒤 join-pane으로 되돌리는 재배치 명령을 다룹니다. 각 동사의 차이를 실전 예제로 확인합니다."
date: 2026-09-04
lastmod: 2026-09-06
collection_order: 11
categories:
- Tmux
tags:
- Tmux
- Terminal
- Workflow(워크플로우)
- Productivity(생산성)
- Best-Practices
- Deep-Dive
- Comparison(비교)
- Troubleshooting(트러블슈팅)
- Migration(마이그레이션)
- Session(세션)
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
- Automation(자동화)
- Configuration(설정)
- Refactoring(리팩토링)
image: "wordcloud.png"
---

03–04장에서는 세션·윈도우·패널을 <strong>만들고 없애는</strong> 조작만 다뤘다. 이 장은 이미 만들어진 것들의 자리를 바꾸는 네 가지 동사 — <strong>swap</strong>(맞바꾸기), <strong>move</strong>(옮기기), <strong>break</strong>(떼어내기), <strong>join</strong>(합치기) — 를 다룬다.

## 이 장을 읽기 전에

**선행 챕터**: 이 장은 [10장: 카피 모드와 버퍼](/post/tmux/tmux-copy-mode-buffers-clipboard/)에서 패널 안의 텍스트를 다룬 것과 달리, 다시 패널·윈도우 자체의 배치로 돌아온다. 03장(세션)·04장(윈도우·패널 기초)에서 다룬 생성·삭제 조작을 전제로 한다.

**이 장의 깊이**: **입문**에서 **중급**(swap과 move의 차이, break와 join이 서로 정확히 반대 동작이라는 것을 설명할 수 있는 수준) 사이를 오간다. **다루지 않는 것**: 여러 클라이언트가 같은 세션을 함께 보는 것은 12장에서 다룬다. `move-pane`/`move-window`가 지원하는 플로팅 패널(popup) 전용 옵션은 상대적으로 최신이고 니치한 기능이라 이 컬렉션의 범위 밖으로 남겨둔다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| 패널·윈도우를 한 번 만든 자리에서만 써 온 사람 | 정신 모델, 명령과 옵션, 예시 | 이미 만든 윈도우·패널의 위치를 재배치할 수 있다 |
| 윈도우 번호가 듬성듬성해져 불편한 사람 | 예시(윈도우 번호 정리) | `move-window -r`로 번호를 순서대로 다시 매길 수 있다 |
| 패널을 잘못된 윈도우에 만들어 버린 사람 | 예시(패널 분리·재합류) | `break-pane`/`join-pane`으로 패널을 다른 윈도우로 옮길 수 있다 |
| swap과 move를 자주 헷갈리는 사람 | 비교/트레이드오프 | 두 동사가 원본 자리에 남기는 결과가 어떻게 다른지 구분할 수 있다 |

## 정신 모델: 네 가지 동사로 나뉘는 재배치

이 장이 다루는 명령은 모두 "이미 존재하는 윈도우 또는 패널을 다른 위치로 옮긴다"는 목적을 공유하지만, 원본 자리에 무엇이 남는지가 서로 다르다. <strong>swap</strong>(`swap-window`/`swap-pane`)은 두 대상의 위치를 맞바꿀 뿐 둘 다 그대로 존재한다. <strong>move</strong>(`move-window`)는 대상을 새 자리로 옮기고 원래 번호는 비워진다. <strong>break</strong>(`break-pane`)는 한 윈도우에 속해 있던 패널을 떼어내 독립된 새 윈도우로 만든다. <strong>join</strong>(`join-pane`)은 그 반대로, 다른 윈도우의 패널을 지금 윈도우의 새 분할 자리로 데려온다. 이 네 동사의 의미를 구분해 두면, 각 명령의 옵션이 무엇을 위한 것인지도 훨씬 예측하기 쉬워진다.

이 장에서 다루는 모든 재배치는 <strong>같은 세션 안에서</strong> 일어난다는 점도 짚어 둘 만하다 — 다른 세션에 있는 윈도우와 맞바꾸거나 그리로 옮기려면, 먼저 03장에서 다룬 방법으로 그 세션으로 전환해야 한다. 또한 이 장에서 하는 일은 코드 리팩토링과 성격이 비슷하다. 처음부터 완벽한 배치를 계획할 필요 없이, 작업하다가 구조가 어색해지면 그때그때 정리하면 된다는 점에서 그렇다. `move-window`/`move-pane`은 그중에서도 좁은 의미의 "이주(migration)"에 해당한다 — 대상을 원래 자리에서 완전히 들어내 새 자리에 재배치하고 원래 자리는 비운다는 점에서, 두 자리를 동시에 채우는 swap과 뚜렷이 구분된다.

## 명령과 옵션

| 명령 | 주요 옵션 | 설명 |
|---|---|---|
| `swap-window`(`swapw`) | `-s 원본`, `-t 대상`, `-d` | 두 윈도우의 위치(번호)를 맞바꾼다. `-d`를 주면 현재 윈도우가 바뀌지 않는다 |
| `swap-pane`(`swapp`) | `-s`, `-t`, `-U`, `-D`, `-d`, `-Z` | 두 패널을 맞바꾼다. `-U`/`-D`는 대상 패널을 번호 기준 이전/다음 패널과 바꾼다. `-Z`는 창이 줌 상태였다면 그대로 유지한다 |
| `move-window`(`movew`) | `-s`, `-t`, `-r` | 윈도우를 새 번호로 옮긴다(원래 번호는 비워짐). `-r`은 `base-index`를 기준으로 세션의 모든 윈도우 번호를 빈틈없이 다시 매긴다 |
| `break-pane`(`breakp`) | `-s 원본패널`, `-t 대상윈도우`, `-a`/`-b`, `-d` | 패널을 그 윈도우에서 떼어내 새 윈도우의 유일한 패널로 만든다. `-d`를 주면 새 윈도우가 현재 윈도우가 되지 않는다 |
| `join-pane`(`joinp`) | `-s`, `-t`, `-h`/`-v`, `-b` | `split-window`처럼 대상 패널을 분할하되, 새 패널을 만드는 대신 다른 곳의 패널을 그 자리로 옮겨온다. `break-pane`을 정확히 반대로 되돌리는 데 쓸 수 있다 |
| `move-pane`(`movep`) | (플로팅 전용 옵션 제외) | 플로팅 패널 관련 옵션이 없으면 `join-pane`과 완전히 동일하게 동작한다 |

## 예시

### 윈도우 순서 맞바꾸기

```bash
# 윈도우 1과 3의 위치를 맞바꾼다 (둘 다 그대로 존재, 번호만 교환)
tmux swap-window -s 1 -t 3
```

### 패널을 위/아래 이웃과 맞바꾸기

```bash
# 현재 패널을 번호 기준 다음 패널과 맞바꾼다
tmux swap-pane -D

# 현재 패널을 번호 기준 이전 패널과 맞바꾼다
tmux swap-pane -U
```

### 윈도우 번호를 빈틈없이 정리하기

윈도우를 여러 개 닫다 보면 0, 2, 5처럼 번호가 듬성듬성해진다. `-r`은 이를 순서대로 다시 채운다.

```bash
tmux move-window -r
```

윈도우 번호가 0부터 시작할지 1부터 시작할지는 `base-index` 옵션이 정하며, `-r`은 그 기준값을 그대로 존중해 다시 번호를 매긴다. 06장에서 배운 대로 `set -g base-index 1`처럼 `tmux.conf`에 미리 설정해 두면, 이후 `-r`로 정리할 때마다 항상 1번부터 채워진다.

### 패널을 떼어냈다 다시 합치기

`break-pane`과 `join-pane`은 정확히 서로 반대되는 동작이라, 실수로 잘못 만든 패널을 정리했다가 마음이 바뀌면 되돌릴 수 있다.

```bash
# 지금 패널을 독립된 새 윈도우로 떼어낸다
tmux break-pane -n isolated

# 마음이 바뀌면, 그 윈도우의 패널을 다시 원래 윈도우의 오른쪽에 합류시킨다
tmux join-pane -h -s isolated -t 0
```

이런 재배치를 매번 손으로 입력하는 대신, 자주 쓰는 조합을 셸 함수나 스크립트로 묶어두면 반복 작업을 줄일 수 있다 — 명령을 스크립트로 자동화하는 구체적인 방법은 13장에서 다룬다.

## 비교/트레이드오프

swap과 move는 겉보기엔 비슷하지만 원본 자리의 운명이 다르다.

| 구분 | `swap-window`/`swap-pane` | `move-window` |
|---|---|---|
| 원본 자리 | 상대방이 그 자리를 대신 차지한다(맞교환) | 비워진다 |
| 대상 개수 | 항상 둘(원본·대상)을 함께 다룬다 | 하나만 옮기면 된다 |
| 적합한 상황 | 두 윈도우·패널의 순서만 바꾸고 싶을 때 | 번호를 정리하거나 특정 위치로 이동시키고 싶을 때(`-r`과 조합하면 특히 유용) |

## 주의사항·함정

**`break-pane`으로 마지막 패널을 떼어내면**: 한 윈도우에 패널이 하나만 남아 있는 상태에서 그 패널을 `break-pane`으로 떼어내면, 원래 윈도우에는 패널이 하나도 남지 않으므로 04장에서 배운 규칙대로 그 윈도우 자체가 사라진다.

**`swap-pane -U`/`-D`의 기준은 화면 위치가 아니라 번호**: `-U`/`-D`는 화면상 위·아래가 아니라 패널의 인덱스 번호를 기준으로 이전/다음을 판단한다. 레이아웃에 따라 화면에서 위에 있는 패널이 번호상으로는 더 나중일 수 있으므로, 원하는 결과가 안 나오면 `select-pane`으로 먼저 패널 번호를 확인한다.

**플로팅 관련 옵션은 이 컬렉션 범위 밖**: `move-pane`/`move-window`가 지원하는 `-X`/`-Y`/`-z` 같은 옵션은 플로팅(popup) 패널을 움직이는 데 쓰이며, 이 컬렉션에서는 다루지 않는 상대적으로 최신 기능이다. 일반 패널을 재배치하는 목적이라면 이 옵션들은 신경 쓰지 않아도 된다.

## 흔한 오개념

<strong>"move-pane과 join-pane은 서로 다른 명령이다"</strong>는 생각은 정확하지 않다. 공식 문서는 `move-pane`을 "플로팅 패널 관련 옵션이 없으면 `join-pane`과 동일하게 동작한다"고 명시한다. 이름이 다를 뿐 기본 동작은 사실상 같다.

<strong>"`break-pane`으로 떼어낸 패널은 되돌릴 수 없다"</strong>는 오해도 흔하다. `join-pane`이 정확히 그 반대 동작을 하므로, 원하는 위치에 다시 합류시킬 수 있다.

<strong>"swap은 move처럼 한쪽 자리를 비운다"</strong>는 생각도 틀렸다. swap은 이름 그대로 맞바꾸기이므로 두 윈도우·패널 모두 사라지지 않고 자리만 교환된다.

## 다음 장에서는

[12장: 세션 그룹과 다중 클라이언트 - 페어 프로그래밍](/post/tmux/tmux-session-groups-multiple-clients-pairing/)에서는 지금까지 혼자 쓰던 세션을 여러 클라이언트가 함께 보는 법 — 페어 프로그래밍에 쓰이는 세션 공유 — 을 다룬다.

## 평가 기준

이 장을 읽은 후 다음을 할 수 있어야 한다.

- swap·move·break·join 네 동사가 원본 자리에 남기는 결과의 차이를 설명할 수 있다.
- `swap-window`/`swap-pane`으로 두 윈도우·패널의 위치를 맞바꿀 수 있다.
- `move-window -r`로 윈도우 번호를 빈틈없이 재정렬할 수 있다.
- `break-pane`과 `join-pane`이 서로 정확히 반대 동작이라는 것을 이해하고 활용할 수 있다.
- `swap-pane -U`/`-D`가 화면 위치가 아니라 패널 번호를 기준으로 동작한다는 것을 설명할 수 있다.

## 참고 및 출처

1. [tmux(1) - OpenBSD Manual](https://man.openbsd.org/tmux) — `swap-window`·`swap-pane`·`move-window`·`break-pane`·`join-pane`·`move-pane` 공식 옵션과 설명.
2. [tmux/tmux](https://github.com/tmux/tmux) — tmux 공식 소스 저장소.
