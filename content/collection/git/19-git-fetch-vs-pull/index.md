---
draft: false
collection_order: 19
slug: git-fetch-vs-git-pull
title: "[Git] 19. git fetch vs git pull"
date: 2026-09-04
lastmod: 2026-09-04
description: "git fetch가 원격 데이터만 받아와 안전하게 검토할 여지를 남기는 것과 달리 git pull이 fetch 직후 자동으로 merge(또는 rebase)까지 실행한다는 차이, pull.rebase 설정으로 기본 동작을 바꾸는 법을 정리한 Git 챕터다."
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
- Collaboration(협업)
- Networking(네트워킹)
- Open-Source(오픈소스)
- Career(커리어)
- Configuration(설정)
- Command-Line
- CLI
image: "wordcloud.png"
---

`git pull`은 편리해서 습관적으로 쓰이지만, 그 편리함 뒤에 숨어 있는 자동 병합(또는 자동 리베이스) 때문에 예상치 못한 충돌이나 지저분한 병합 커밋을 만나는 경우가 있다. 이 장은 `git fetch`와 `git pull`이 실제로 서로 다른 두 단계로 이뤄진 조합이라는 사실을 밝힌다.

## 개요

두 명령의 관계를 한 줄로 요약하면, `git pull`은 `git fetch` 다음에 `git merge`(또는 설정에 따라 `git rebase`)를 자동으로 실행하는 축약형이다.

```bash
git fetch origin           # 원격의 최신 데이터를 받아오기만 함(작업 트리는 그대로)
git pull origin main       # fetch + merge(또는 rebase)를 한 번에 실행
```

## 기본 개념

`git fetch`는 원격 저장소의 새 커밋·브랜치 정보를 로컬의 `refs/remotes/origin/` 아래로 내려받을 뿐, 현재 작업 중인 브랜치나 작업 트리를 전혀 건드리지 않는다. 이 성질 때문에 fetch는 "지금 무슨 변경이 있었는지 안전하게 확인만 하고 싶을 때" 쓰기 좋다.

```bash
git fetch origin
git log main..origin/main --oneline    # fetch로 받아온 새 커밋만 미리보기(아직 병합 전)
git diff main origin/main               # 실제 변경 내용까지 확인
```

이렇게 확인한 뒤 원하는 방식(merge 또는 rebase)으로 직접 반영할지 결정할 수 있다는 것이 fetch의 장점이다. 반면 `git pull`은 이 확인 단계 없이 곧바로 병합까지 진행하므로, 로컬에 커밋되지 않은 작업이 남아 있거나 병합 충돌이 날 수 있는 상황이라면 예고 없이 그 상황과 맞닥뜨리게 된다.

## 종류/세부

### pull의 기본 동작을 병합에서 리베이스로 바꾸기

`git pull`은 기본적으로 merge를 실행하지만, `pull.rebase` 설정으로 rebase를 실행하도록 바꿀 수 있다.

```bash
git config --global pull.rebase true    # 이후 모든 git pull이 fetch + rebase로 동작
git pull --rebase origin main            # 이번 한 번만 rebase로 실행(설정과 무관하게)
```

16장에서 다룬 merge vs rebase 선택 기준이 여기서도 그대로 적용된다 — 원격의 최신 커밋을 로컬의 아직 push하지 않은 커밋 앞에 깔끔하게 반영하고 싶다면 `pull --rebase`가 직선 히스토리를 유지하는 데 유리하지만, 이미 다른 사람과 공유 중인 브랜치에서는 15장의 위험이 그대로 적용된다.

### 무엇을 fetch할지 지정하기

인자 없는 `git fetch`는 등록된 원격(기본은 `origin`)의 모든 브랜치를 대상으로 하지만, 특정 브랜치만 받아오도록 좁힐 수 있다.

```bash
git fetch origin develop        # develop 브랜치의 최신 정보만
git fetch --all                 # 등록된 모든 원격에서 한 번에
git fetch --prune                # 원격에서 이미 삭제된 브랜치의 로컬 추적 참조도 함께 정리
```

`--prune`은 팀원이 원격 브랜치를 삭제했는데 로컬에는 그 흔적(`refs/remotes/origin/old-branch`)이 남아 `git branch -a`(11장) 목록을 어지럽히는 상황을 정리할 때 유용하다.

## 주의사항·함정

**커밋되지 않은 변경이 있는 상태에서 `git pull`을 실행하면 충돌 위험이 있다**: pull은 곧바로 merge를 실행하므로, 12장에서 설명한 브랜치 전환 시 충돌과 유사하게 로컬 변경과 겹치는 부분이 있으면 문제가 생길 수 있다. 중요한 작업 중이라면 먼저 커밋하거나 `git stash`(29장)로 치워둔 뒤 pull하는 편이 안전하다.

**"pull이 항상 최신 상태로 만들어준다"는 오해**: pull은 명시한 원격·브랜치의 정보만 가져온다. 다른 원격(예: 17장에서 다룬 `upstream`)의 변경 사항은 그 원격을 대상으로 별도로 fetch·pull해야 반영된다.

**fetch만 하고 병합을 잊어버리는 경우**: fetch로 최신 정보를 받아왔지만 병합(또는 rebase)을 실행하지 않으면, 로컬 브랜치는 여전히 예전 상태에 머물러 있다. `git status`(06장)의 "Your branch is behind 'origin/main' by N commits" 메시지가 이 상태를 알려주는 신호다.

## Reference

- [git-fetch Documentation](https://git-scm.com/docs/git-fetch)
- [git-pull Documentation](https://git-scm.com/docs/git-pull)
