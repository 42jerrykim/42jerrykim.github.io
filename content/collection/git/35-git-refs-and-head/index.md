---
draft: false
collection_order: 35
slug: git-refs-and-head-reference-model
title: "[Git] 35. Git refs와 HEAD"
date: 2026-09-04
lastmod: 2026-09-04
description: "브랜치·태그·HEAD가 모두 커밋 해시를 가리키는 참조(ref)일 뿐이라는 통일된 모델, HEAD가 브랜치를 가리키는 상태와 커밋을 직접 가리키는 detached 상태의 차이, symbolic-ref로 참조 구조를 직접 들여다보는 법을 정리한 Git 챕터다."
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
- Data-Structure(자료구조)
- Distributed-Systems(분산시스템)
- Command-Line
image: "wordcloud.png"
---

34장에서 "브랜치·태그는 객체가 아니라 참조"라고 짧게 정리했다. 이 장은 그 참조(ref) 모델을 정면으로 다루며, 11장의 브랜치·22장의 태그·12장의 HEAD가 사실은 모두 같은 메커니즘의 변형이라는 것을 확인한다.

## 개요

Git의 참조는 `.git/refs/` 아래에 흩어져 있는 일반 텍스트 파일이며, 각 파일의 내용은 커밋 해시 하나(또는 다른 참조를 가리키는 표기)뿐이다.

```
.git/refs/heads/main              → 커밋 해시(11장의 로컬 브랜치)
.git/refs/heads/feature/login     → 커밋 해시(다른 로컬 브랜치)
.git/refs/remotes/origin/main     → 커밋 해시(18-19장에서 다룬 원격 추적 브랜치)
.git/refs/tags/v1.0.0             → 커밋 해시(22장의 가벼운 태그) 또는 태그 객체 해시(주석 달린 태그)
```

브랜치와 원격 추적 브랜치, 태그는 저장 위치(디렉터리)만 다를 뿐 구조 자체는 동일하다. 이 통일성 덕분에 `git log <아무 참조 이름>`, `git diff <아무 참조 이름>`처럼 이 컬렉션 전체에서 다룬 명령들이 브랜치든 태그든 구분 없이 똑같은 문법으로 받아들일 수 있다.

## 기본 개념

<strong>HEAD</strong>는 이 참조 체계에서 특별한 역할을 하는, "지금 내가 어디에 있는가"를 가리키는 참조다. 03장에서 살펴본 대로 `.git/HEAD` 파일을 열어보면 보통 다음과 같은 한 줄이 들어 있다.

```
ref: refs/heads/main
```

이것이 <strong>symbolic ref</strong>다 — HEAD가 커밋 해시를 직접 담는 것이 아니라, "다른 참조 파일을 가리킨다"는 한 단계 간접 참조를 담고 있다. `git switch main`(12장)을 실행하면 이 `.git/HEAD` 파일의 내용이 `ref: refs/heads/main`으로 다시 쓰이는 것이 전부다. 새 커밋을 만들면 Git은 HEAD가 가리키는 참조(`refs/heads/main`)의 내용을 새 커밋 해시로 갱신하고, 그 결과로 "현재 브랜치가 앞으로 나아갔다"는 상태가 만들어진다.

## 종류/세부

### Detached HEAD와의 연결

12장에서 다룬 detached HEAD 상태는 이 구조로 정확히 설명된다. `git switch --detach <커밋>`을 실행하면 `.git/HEAD`가 symbolic ref(다른 참조를 가리키는 형태) 대신 커밋 해시를 직접 담는다.

```
# 일반 상태
ref: refs/heads/main

# Detached HEAD 상태
a1b2c3d4e5f6...
```

이 상태에서 새 커밋을 만들면 HEAD 파일의 해시 값만 갱신될 뿐, 어떤 브랜치 참조도 그 새 커밋을 가리키지 않는다. 12장에서 설명했던 "detached HEAD에서 만든 커밋은 다른 브랜치로 전환하면 유실 위험이 있다"는 경고가 바로 이 구조에서 나온 것이다 — 그 커밋을 가리키는 브랜치 참조가 애초에 없기 때문이다.

### 참조를 직접 조회하는 명령

```bash
git symbolic-ref HEAD              # HEAD가 지금 어느 참조를 가리키는지 확인
git rev-parse HEAD                 # HEAD가 (간접적으로) 가리키는 실제 커밋 해시 확인
git rev-parse --abbrev-ref HEAD    # 현재 브랜치 이름만 짧게 확인(스크립트에서 자주 사용)
git update-ref refs/heads/main a1b2c3d   # 참조 파일을 저수준으로 직접 갱신(일반적으로는 쓸 필요 없음)
```

`git rev-parse --abbrev-ref HEAD`는 셸 스크립트나 CI 설정에서 "지금 어느 브랜치에서 실행 중인가"를 프로그래밍적으로 확인할 때 자주 쓰인다.

### Packed refs

브랜치·태그 수가 아주 많아지면 `.git/refs/` 아래 개별 파일이 수천 개까지 늘어날 수 있다. Git은 이런 경우를 위해 여러 참조를 `.git/packed-refs`라는 파일 하나로 압축해 관리하는 최적화를 제공한다. 이는 참조의 논리적 동작에는 영향을 주지 않는 저장 효율화이며, 36장에서 다루는 packfile과 유사한 발상이다.

## 주의사항·함정

**`.git/HEAD`나 `.git/refs/` 파일을 직접 편집하지 않는다**: 34장에서 객체 디렉터리를 직접 건드리지 말라고 경고한 것과 같은 이유다. 참조 구조를 실수로 손상시키면 저장소가 일관성을 잃을 수 있으므로, 이 파일들을 바꾸고 싶다면 `git switch`, `git branch`, `git tag`, 필요하다면 `git update-ref` 같은 정식 명령을 거쳐야 한다.

**참조 이름에 슬래시(`/`)를 쓰면 디렉터리 구조가 생긴다**: `feature/login`처럼 슬래시를 포함한 브랜치 이름은 `.git/refs/heads/feature/login`이라는 실제 하위 디렉터리 구조로 저장된다. 이 때문에 `feature`라는 이름의 브랜치와 `feature/login`이라는 이름의 브랜치를 동시에 만들 수 없다 — 파일 시스템 관점에서 `feature`가 파일이면서 동시에 디렉터리일 수는 없기 때문이다.

**원격 추적 브랜치(`refs/remotes/`)를 로컬 브랜치와 혼동하지 않는다**: 18장에서 다룬 것처럼 `refs/remotes/origin/main`은 마지막 fetch 시점의 원격 상태를 반영하는 읽기 전용에 가까운 참조다. 이 참조를 직접 `git commit`의 대상으로 삼아 작업할 수는 없으며, 반드시 로컬 브랜치(`refs/heads/`)를 통해야 한다.

## Reference

- [Git Internals - Git References](https://git-scm.com/book/en/v2/Git-Internals-Git-References)
