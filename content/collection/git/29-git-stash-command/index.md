---
draft: false
collection_order: 29
slug: git-stash-command-temporary-storage
title: "[Git] 29. git stash — 임시 저장"
date: 2026-09-04
lastmod: 2026-09-04
description: "git stash가 커밋하지 않은 변경을 임시로 치워두고 나중에 복원하는 원리, 스택 구조로 여러 stash를 관리하는 법, 브랜치 전환 시 충돌을 피하는 대표 시나리오와 stash 자체가 커밋으로 구현된다는 사실을 정리한 Git 6부 첫 챕터다."
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
- Advanced
- Snapshot
- Open-Source(오픈소스)
- Career(커리어)
- Configuration(설정)
image: "wordcloud.png"
---

12장에서 "커밋되지 않은 변경이 있으면 브랜치 전환이 거부된다"는 상황을 언급하며 `git stash`를 대안으로 짧게 소개했다. 6부의 첫 챕터인 이 장은 그 stash를 정면으로 다룬다 — 아직 커밋할 준비가 안 된 변경을 임시로 치워두고, 나중에 정확히 그 상태로 복원하는 도구다.

## 개요

```bash
git stash                          # 현재 변경 사항을 스택에 저장하고 작업 트리를 마지막 커밋 상태로 되돌림
git stash pop                      # 가장 최근 stash를 복원하고 스택에서 제거
git stash list                     # 저장된 stash 목록 확인
git stash apply                    # 복원하되 스택에는 그대로 남겨둠(pop과의 차이)
```

`git stash`를 실행하면 작업 트리는 마치 아무것도 수정하지 않은 것처럼 깨끗해지지만, 그 변경 사항은 사라진 것이 아니라 별도의 저장 공간(스택)에 보관된다.

## 기본 개념

Stash가 실제로 무엇을 저장하는지는 04장의 3단계 모델로 설명된다 — 기본적으로 stash는 <strong>스테이징된 변경과 스테이징되지 않은 변경 모두</strong>를 함께 저장하고, 작업 트리를 HEAD 상태로 되돌린다. 이 저장 방식은 34장에서 다룰 Git 객체 모델을 그대로 활용한다 — 사실 stash는 특수한 형태의 커밋으로 구현되어 있으며, `git stash list`가 보여주는 각 항목도 내부적으로는 커밋 해시를 가진다. 이 사실은 아래에서 다루는 특정 파일만 복원하기, stash를 브랜치로 만들기 같은 고급 기능의 토대가 된다.

## 종류/세부

### 대표 시나리오 — 브랜치 전환 전 임시 대피

작업 중이던 변경을 커밋할 준비는 안 됐는데 급하게 다른 브랜치로 전환해야 할 때가 stash의 가장 흔한 용도다.

```bash
git stash                    # 지금 작업을 임시로 치움
git switch main
git switch -c hotfix/urgent-bug
# ... 긴급 수정 후 커밋, push ...
git switch feature/original-work
git stash pop                 # 하던 작업을 그대로 복원
```

### 여러 stash를 스택으로 관리하기

`git stash`는 이름 그대로 스택(stack) 구조이며, 여러 번 stash하면 목록이 쌓인다.

```bash
git stash list
```

```
stash@{0}: WIP on feature/login: 3f2a1c9 로그인 폼 작업 중
stash@{1}: WIP on main: 9f8e7d6 실험적 리팩터링
```

`pop`·`apply`는 인자를 생략하면 가장 최근(`stash@{0}`)을 대상으로 하지만, 특정 stash를 지정할 수도 있다.

```bash
git stash pop stash@{1}
git stash drop stash@{1}     # 복원 없이 목록에서만 제거
```

### `pop` vs `apply`

| 명령 | 작업 트리에 복원 | 스택에서 제거 |
|---|---|---|
| `git stash pop` | O | O |
| `git stash apply` | O | X |

`apply`는 같은 stash를 여러 브랜치에 반복해서 적용하고 싶을 때 유용하다 — 예를 들어 실험적인 변경을 만들어두고, 이 브랜치 저 브랜치에 번갈아 적용해보며 어디에 잘 맞는지 확인하는 경우다.

### 추적되지 않는 파일까지 포함하기

기본 `git stash`는 이미 추적 중인 파일의 변경만 대상으로 하며, untracked 파일(04장)은 그대로 작업 트리에 남는다. untracked 파일까지 함께 치우고 싶다면 옵션이 필요하다.

```bash
git stash -u    # untracked 파일까지 포함(--include-untracked)
git stash -a    # .gitignore로 무시된 파일까지 전부 포함(--all)
```

## 주의사항·함정

**`pop` 시 충돌이 나면 stash가 스택에서 자동으로 제거되지 않는다**: 12장·13장에서 다룬 것과 유사한 충돌이 stash 복원 중에도 발생할 수 있다. 이 경우 `pop`은 충돌을 해결할 때까지 stash 항목을 스택에 남겨두므로, 충돌을 해결한 뒤 `git stash drop`으로 수동으로 정리해야 한다.

**stash를 오래 방치하면 무엇이 들어 있었는지 잊어버리기 쉽다**: `git stash list`의 기본 메시지("WIP on ...")는 브랜치 이름과 마지막 커밋만 알려줄 뿐 구체적인 내용을 설명하지 않는다. 오래 보관할 stash라면 메시지를 직접 지정해두는 편이 나중에 헷갈리지 않는다.

```bash
git stash push -m "로그인 폼 리팩터링 진행 중"
```

**stash는 브랜치 전용 임시 저장이 아니라 저장소 전체에서 공유된다**: 어느 브랜치에서 stash했든 `git stash list`는 저장소 전체의 stash를 모두 보여준다. 다른 브랜치로 전환한 뒤 실수로 엉뚱한 stash를 pop하면, 원래 의도한 브랜치와 무관한 변경이 섞여 들어올 수 있다.

## Reference

- [Git Tools - Stashing and Cleaning](https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning)
- [git-stash Documentation](https://git-scm.com/docs/git-stash)
