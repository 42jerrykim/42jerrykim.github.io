---
draft: false
collection_order: 44
slug: common-git-errors-and-solutions
title: "[Git] 44. 자주 발생하는 Git 에러와 해결법 총정리"
date: 2026-09-04
lastmod: 2026-09-04
description: "이 45챕터 시리즈에서 다룬 명령들이 실무에서 가장 자주 만드는 에러 메시지를 원인별로 모아, 각 에러가 어느 챕터의 어떤 개념과 연결되는지 정리한 Git 시리즈 마지막 챕터다."
categories:
- Git
tags:
- Git
- GitHub
- Version-Control(버전관리)
- Terminal
- Guide(가이드)
- Education(교육)
- Beginner
- Productivity(생산성)
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Troubleshooting(트러블슈팅)
- Workflow(워크플로우)
- DevOps
- Command-Line
- CLI
- Diagnostics(진단)
- Career(커리어)
- Open-Source(오픈소스)
- Configuration(설정)
- Advanced
image: "wordcloud.png"
---

이 시리즈는 00장의 지도(map)에서 시작해 9개 Part를 거쳐 왔다. 마지막 챕터는 새 개념을 소개하는 대신, 실무에서 실제로 가장 자주 마주치는 Git 에러 메시지를 원인별로 모아 이 시리즈의 어느 장과 연결되는지 정리한다 — 급할 때 이 표만 훑어도 어디로 돌아가 자세한 설명을 찾을지 알 수 있도록 하는 것이 목적이다.

## 개요

에러는 크게 네 갈래로 나뉜다 — 커밋 이전 단계(스테이징·설정), 브랜치·병합 단계, 원격 동기화 단계, 히스토리 되돌리기 단계다. 이 분류 자체가 3-6부의 순서와 대체로 대응한다.

## 종류/세부

### 커밋 이전 단계(1-2부 관련)

| 에러 메시지(요약) | 원인 | 해결·참고 챕터 |
|---|---|---|
| `Please tell me who you are` | 작성자 이름·이메일 미설정 | `git config --global user.name/email`([02장](/post/git/git-install-config-user-setup/)) |
| `nothing to commit, working tree clean` | 스테이징된 변경이 없음(단순 안내이지 에러 아님) | [04장](/post/git/git-three-stage-model-working-tree-staging-repository/)의 3단계 모델로 상태 확인 |
| `fatal: not a git repository` | Git 저장소가 아닌 디렉터리에서 명령 실행 | `git init`([03장](/post/git/git-init-dot-git-directory-structure/)) 또는 올바른 디렉터리로 이동 |
| `LF will be replaced by CRLF` (경고) | 줄바꿈 정규화 동작 | [02장](/post/git/git-install-config-user-setup/)의 `core.autocrlf`, [40장](/post/git/gitattributes-file-path-specific-behavior/)의 `.gitattributes` |

### 브랜치·병합 단계(3부 관련)

| 에러 메시지(요약) | 원인 | 해결·참고 챕터 |
|---|---|---|
| `error: Your local changes ... would be overwritten by checkout` | 커밋되지 않은 변경과 전환 대상 브랜치가 충돌 | 커밋하거나 `git stash`([29장](/post/git/git-stash-command-temporary-storage/)) |
| `CONFLICT (content): Merge conflict in <file>` | 두 브랜치가 같은 부분을 다르게 수정 | 충돌 마커 해결([13장](/post/git/git-merge-command-and-conflict-resolution/)) |
| `error: Cannot delete branch '...' checked out at ...` | 현재 체크아웃된 브랜치를 삭제 시도 | 다른 브랜치로 전환 후 삭제([11장](/post/git/git-branch-concept-and-command/), [12장](/post/git/git-switch-checkout-branch-transition/)) |
| `fatal: A branch named '...' already exists` | 동일 이름 브랜치 중복 생성 시도 | `git branch -v`로 기존 브랜치 확인([11장](/post/git/git-branch-concept-and-command/)) |

### 원격 동기화 단계(4부 관련)

| 에러 메시지(요약) | 원인 | 해결·참고 챕터 |
|---|---|---|
| `! [rejected] ... (fetch first)` | 원격이 로컬보다 앞서 있음 | `git pull` 또는 fetch 후 병합([19장](/post/git/git-fetch-vs-git-pull/), [20장](/post/git/git-push-command-upstream-tracking/)) |
| `fatal: The current branch has no upstream branch` | upstream 미설정 상태에서 인자 없이 push | `git push -u origin <branch>`([20장](/post/git/git-push-command-upstream-tracking/)) |
| `Permission denied (publickey)` | SSH 키 미등록 또는 잘못된 키 | [17장](/post/git/git-remote-command-managing-remote-repositories/)의 HTTPS/SSH 프로토콜 확인 |
| `remote: Repository not found` | URL 오타 또는 접근 권한 없음 | `git remote -v`로 URL 확인([17장](/post/git/git-remote-command-managing-remote-repositories/)) |

### 히스토리 되돌리기 단계(5부 관련)

| 에러 메시지(요약) | 원인 | 해결·참고 챕터 |
|---|---|---|
| `error: could not apply ...` (cherry-pick/rebase 중) | 재적용 과정에서 충돌 발생 | 마커 해결 후 `--continue`([15장](/post/git/git-rebase-command-rewriting-history/), [26장](/post/git/git-cherry-pick-command/), [27장](/post/git/git-rebase-interactive-mode/)) |
| 실수로 `reset --hard`한 뒤 변경을 잃음 | 커밋된 데이터만 복구 가능 | `git reflog`([28장](/post/git/git-reflog-command-recover-lost-commits/)) |
| `fatal: refusing to merge unrelated histories` | 공통 조상이 없는 두 히스토리를 병합 시도 | 의도한 것인지 확인 후 `--allow-unrelated-histories`([13장](/post/git/git-merge-command-and-conflict-resolution/), [14장](/post/git/fast-forward-vs-three-way-merge/)) |
| `HEAD detached at <hash>` (경고성 안내) | 브랜치가 아닌 커밋을 직접 체크아웃 | 보존하려면 새 브랜치 생성([12장](/post/git/git-switch-checkout-branch-transition/)) |

## 주의사항·함정

**에러 메시지를 검색 없이 곧바로 강제 옵션(`--force`, `-D` 등)으로 우회하지 않는다**: 이 시리즈 전체에서 반복해서 강조했듯, 대부분의 거부·경고는 데이터 손실을 막기 위한 안전장치([20장](/post/git/git-push-command-upstream-tracking/)의 push 거부, [11장](/post/git/git-branch-concept-and-command/)의 브랜치 삭제 방지 등). 원인을 먼저 이해하지 않고 강제로 넘어가면, 그 안전장치가 막으려던 문제(다른 사람의 작업 덮어쓰기, 병합되지 않은 커밋 유실)가 실제로 일어난다.

**같은 에러라도 원인이 다를 수 있다**: 예를 들어 `rejected (fetch first)`는 다른 사람이 먼저 push했을 수도 있고, 자신이 다른 컴퓨터에서 먼저 작업했을 수도 있다. `git log --oneline --graph --all`([09장](/post/git/git-log-command-view-history/))로 실제 상황을 먼저 파악하는 습관이 성급한 대응보다 낫다.

**이 표에 없는 에러를 만났다면 공식 문서가 가장 정확하다**: Git 각 명령의 공식 문서(`git help <command>` 또는 이 시리즈 각 장의 Reference)는 버전에 따른 옵션 변화까지 반영하므로, 오래된 블로그 글보다 신뢰할 수 있는 1차 출처다.

## 마치며

이 시리즈는 00장의 스냅샷 모델에서 시작해, 기초 설정(1부)과 스냅샷 워크플로(2부)로 Git의 일상적인 사용법을 다졌다. 브랜치와 병합(3부)은 여러 작업을 동시에 진행하는 법을, 원격 저장소와 협업(4부)은 그 작업을 다른 사람과 나누는 법을 다뤘다. 히스토리 되돌리기(5부)와 작업 관리 심화(6부)는 실수를 안전하게 복구하고 일상 작업을 더 편하게 만드는 도구들이었고, 내부 구조(7부)는 지금까지 다룬 명령들이 실제로 무엇을 조작해왔는지 설명했다. 확장 기능(8부)과 운영·트러블슈팅(9부)은 여러 저장소를 조합하거나 대규모 환경을 운영할 때 필요한 도구로 마무리됐다.

이 44개 챕터를 순서대로 읽었다면, 이제 남은 것은 검색으로 채우는 세부 옵션들뿐이다 — 3단계 모델, 객체 모델, 참조 모델이라는 세 가지 정신 모델만 확실히 잡고 있으면, 처음 보는 Git 명령이라도 "이것이 어느 영역을 어떻게 바꾸는가"라는 질문으로 대부분 스스로 답을 찾을 수 있다.
