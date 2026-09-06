---
draft: false
collection_order: 38
slug: git-worktree-multiple-checkouts
title: "[Git] 38. Git worktree"
date: 2026-09-04
lastmod: 2026-09-04
description: "git worktree가 하나의 .git 저장소를 공유하면서 여러 브랜치를 서로 다른 디렉터리에 동시에 체크아웃하는 원리, 브랜치 전환 없이 병렬 작업이 가능한 이유, stash 없이 급한 작업을 처리하는 대안 시나리오를 정리한 Git 챕터다."
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
- File-System(파일시스템)
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
- Configuration(설정)
- Command-Line
- CLI
image: "wordcloud.png"
---

29장의 `git stash`는 브랜치를 전환하기 전 커밋되지 않은 변경을 임시로 치워두는 방법이었다. 하지만 애초에 브랜치를 전환할 필요 없이, 서로 다른 브랜치를 <strong>동시에</strong> 서로 다른 디렉터리에서 열어두고 작업할 수 있다면 더 간단하다. `git worktree`가 이 방식을 제공한다.

## 개요

```bash
git worktree add ../project-hotfix hotfix/urgent-bug
```

이 명령은 현재 저장소 옆에 `project-hotfix`라는 새 디렉터리를 만들고, 그 안에 `hotfix/urgent-bug` 브랜치를 체크아웃한다. 원래 디렉터리의 작업 트리는 전혀 건드리지 않은 채, 완전히 별개의 작업 트리가 하나 더 생기는 것이다.

```bash
git worktree list       # 현재 저장소에 연결된 모든 worktree 확인
git worktree remove ../project-hotfix   # 다 쓴 worktree 제거
```

## 기본 개념

여러 worktree는 서로 다른 디렉터리에 있지만 <strong>단 하나의 `.git` 저장소(34장에서 다룬 객체·참조 전체)를 공유</strong>한다. 즉 한 worktree에서 커밋한 내용은 같은 저장소를 공유하는 다른 worktree에서도 `git log`(09장)로 곧바로 조회할 수 있다 — 원격 저장소를 거칠 필요가 없다. 다만 <strong>같은 브랜치를 두 worktree에서 동시에 체크아웃할 수는 없다</strong>. 브랜치는 11장에서 다뤘듯 HEAD가 가리키는 대상이므로, 한 브랜치가 이미 다른 worktree에서 체크아웃되어 있다면 Git이 중복 체크아웃을 막는다.

## 종류/세부

### 대표 시나리오 — stash 없이 급한 작업 처리

29장에서 다룬 stash의 대안으로 worktree를 쓰면, 하던 작업을 전혀 건드리지 않고 다른 브랜치에서 작업할 수 있다.

```bash
# feature/login 브랜치에서 한창 작업 중인 상태 그대로 두고
git worktree add ../urgent-fix main
cd ../urgent-fix
# 여기서 긴급 수정 작업(원래 디렉터리의 작업 트리는 전혀 영향받지 않음)
git commit -am "긴급 수정"
git push origin main
cd ../original-project    # 원래 작업하던 디렉터리로 돌아가면 하던 작업이 그대로 남아 있음
```

이 방식은 stash처럼 나중에 pop을 잊거나 충돌할 위험 없이, 물리적으로 완전히 분리된 두 작업 공간을 유지한다.

### 새 브랜치를 만들면서 worktree 추가

```bash
git worktree add -b feature/new-idea ../new-idea main
```

이 명령은 `main`에서 갈라져 나온 `feature/new-idea`라는 새 브랜치를 만들면서 동시에 `../new-idea` 디렉터리에 worktree를 생성한다.

### 정리

worktree 디렉터리를 그냥 파일 탐색기에서 삭제하면, `.git` 저장소 안에는 그 worktree에 대한 메타데이터가 여전히 남아 "찾을 수 없는 worktree"로 표시된다.

```bash
git worktree prune    # 디렉터리가 이미 사라진 worktree의 메타데이터 정리
```

정식으로 제거할 때는 `git worktree remove`를 쓰는 편이 안전하다 — 커밋되지 않은 변경이 있으면 삭제를 막아준다.

## 주의사항·함정

**worktree를 많이 만들면 디스크 공간이 그만큼 늘어난다**: 34장에서 설명했듯 `.git` 객체 자체는 공유되지만, 각 worktree는 독립적인 작업 트리(실제 체크아웃된 파일들)를 갖는다. 대용량 저장소에서 worktree를 여러 개 만들면 그만큼 디스크 사용량이 늘어난다는 점을 감안해야 한다.

**같은 브랜치를 두 곳에서 체크아웃하려 하면 오류가 난다**: "이미 다른 worktree에서 체크아웃된 브랜치"라는 오류를 만난다면, 그 브랜치가 정확히 어느 worktree에서 쓰이고 있는지 `git worktree list`로 확인해야 한다.

**빌드 도구나 IDE가 여러 worktree를 인식하지 못할 수 있다**: 일부 오래된 개발 도구는 프로젝트 루트가 하나라고 가정하고 만들어져, worktree 구조에서 예상과 다르게 동작할 수 있다. 새로 도입하기 전에 사용 중인 도구가 여러 작업 디렉터리 구조를 지원하는지 확인하는 편이 안전하다.

## Reference

- [git-worktree Documentation](https://git-scm.com/docs/git-worktree)
