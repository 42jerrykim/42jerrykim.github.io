---
draft: false
collection_order: 3
slug: git-init-dot-git-directory-structure
title: "[Git] 03. git init과 .git 디렉터리 구조"
date: 2026-09-04
lastmod: 2026-09-04
description: "git init으로 저장소를 만드는 방법과 .git 디렉터리 내부의 HEAD, objects, refs, config가 각각 무엇을 저장하는지, bare 저장소와 일반 저장소의 차이를 정리한 Git 입문 챕터다."
categories:
- Git
tags:
- Git
- GitHub
- Version-Control(버전관리)
- Terminal
- Configuration(설정)
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
- Distributed-Systems(분산시스템)
- File-System(파일시스템)
- Repository
- Metadata(메타데이터)
- Server(서버)
- DevOps
- Workflow(워크플로우)
- Open-Source(오픈소스)
image: "wordcloud.png"
---

새 프로젝트에서 `git init`을 실행하면 현재 디렉터리에 `.git`이라는 숨김 폴더가 생긴다. 대부분의 사용자는 이 폴더를 열어볼 일 없이 `git add`·`git commit`만 반복하지만, `.git` 폴더 안에 실제로 무엇이 들어 있는지 알아두면 이후 챕터에서 다루는 브랜치·리셋·reflog 같은 명령이 정확히 무엇을 바꾸는지 훨씬 분명하게 이해할 수 있다.

## 개요

`git init`은 현재 디렉터리를 Git 저장소로 초기화하는 명령이다. 실행하면 그 디렉터리 안에 `.git`이라는 하위 디렉터리가 생성되고, 이 `.git` 디렉터리 자체가 저장소의 전체 히스토리·설정·참조를 담는다.

```bash
mkdir my-project && cd my-project
git init
```

이미 파일이 있는 기존 디렉터리에서 실행해도 안전하다 — `git init`은 기존 파일을 건드리지 않고 버전 관리 메타데이터만 추가한다. 저장소를 초기화한 뒤 어떤 하위 디렉터리가 생겼는지 확인하려면 아래처럼 조회한다.

```bash
ls -a .git
```

## 기본 개념

`.git` 디렉터리는 작업 트리(실제로 편집하는 파일들)와 분리된, Git이 관리하는 모든 정보의 저장소다. 이 디렉터리를 통째로 삭제하면 커밋 히스토리·브랜치·설정이 전부 사라지고 남는 것은 마지막으로 체크아웃된 작업 트리 파일뿐이다 — 즉 `.git` 폴더 자체가 "버전 관리 이력"의 실체다.

| 항목 | 역할 |
|---|---|
| `HEAD` | 현재 체크아웃된 브랜치(또는 커밋)를 가리키는 참조 |
| `config` | 이 저장소에만 적용되는 로컬 설정(02장의 `--local` 범위) |
| `objects/` | 커밋·트리·blob 등 모든 데이터가 저장되는 곳(34장에서 자세히 다룬다) |
| `refs/` | 브랜치·태그가 가리키는 커밋 해시를 저장하는 디렉터리 |
| `index` | 스테이징 영역의 실제 상태를 담은 파일 |
| `hooks/` | 커밋·푸시 등 특정 시점에 자동 실행되는 스크립트가 위치하는 곳(39장) |

`HEAD` 파일을 직접 열어보면 대개 `ref: refs/heads/main`처럼 브랜치 이름을 가리키는 한 줄이 들어 있다. 즉 "현재 브랜치"라는 개념은 실제로는 `HEAD`가 `refs/heads/` 아래의 어떤 파일을 가리키느냐로 결정되며, 그 파일 안에는 해당 브랜치의 최신 커밋 해시가 들어 있다. 이 구조는 35장에서 refs를 다룰 때 다시 짚는다.

## 종류/세부

### 일반 저장소 vs bare 저장소

`git init`에는 `--bare` 옵션이 있다. 일반 저장소는 `.git` 디렉터리와 작업 트리(편집 가능한 파일들)가 함께 있지만, bare 저장소는 작업 트리 없이 `.git` 디렉터리의 내용물만 최상위에 존재한다.

| 구분 | 일반 저장소 | bare 저장소 |
|---|---|---|
| 작업 트리 | 있음(파일을 직접 편집) | 없음 |
| 생성 명령 | `git init` | `git init --bare` |
| 용도 | 개발자가 직접 작업하는 로컬 저장소 | 여러 사람이 push/pull하는 공유 원격 저장소 서버 |
| 직접 커밋 | 가능 | 불가능(작업 트리가 없어 파일을 편집할 수 없다) |

사내에 자체 Git 서버를 구축할 때 원격 저장소로 쓰는 것이 보통 bare 저장소다 — 사람이 직접 그 서버 디렉터리에서 파일을 편집할 일이 없고, 오직 clone·push·pull의 대상으로만 쓰이기 때문에 작업 트리가 없는 편이 디스크 공간과 혼란을 모두 줄인다. GitHub·GitLab이 내부적으로 각 저장소를 저장하는 방식도 이 bare 저장소 개념에 기반한다.

```bash
git init --bare my-project.git
```

### 이미 초기화된 디렉터리에서 다시 init하면

이미 `.git` 디렉터리가 있는 곳에서 `git init`을 다시 실행해도 기존 히스토리는 삭제되지 않는다. Git은 이미 존재하는 설정을 유지한 채 누락된 하위 디렉터리만 다시 만들며, 주로 `.git/config`의 템플릿을 재적용하거나 손상된 하위 구조를 복구할 때 이 방식을 쓴다.

## 주의사항·함정

**`.git` 디렉터리를 실수로 삭제하면 복구가 매우 어렵다**: 휴지통이나 스냅샷 백업이 없다면, `.git`을 삭제한 시점에서 아직 원격 저장소에 push하지 않은 로컬 커밋은 사실상 되돌릴 수 없다. 중요한 작업은 항상 원격 저장소(4부)에 정기적으로 push해 두는 것이 유일하게 확실한 대비책이다.

**중첩 Git 저장소(Git 안의 Git)**: 이미 Git 저장소인 디렉터리 안의 하위 디렉터리에서 또 `git init`을 실행하면, 바깥쪽 저장소와 별개인 새 저장소가 생긴다. 이 상태를 인지하지 못하면 하위 디렉터리의 변경 사항이 바깥쪽 저장소의 `git status`에 보이지 않아 "커밋했는데 반영이 안 됐다"는 혼란으로 이어진다. 의도적으로 저장소 안에 다른 저장소를 포함하고 싶다면 일반 중첩 대신 submodule(37장)을 쓰는 것이 올바른 방법이다.

**`git init` 직후 브랜치 이름은 설정에 따라 다르다**: 2020년 이후 Git 커뮤니티는 기본 브랜치 이름을 `master`에서 `main`으로 바꾸는 흐름을 따랐지만, 실제 기본값은 `init.defaultBranch` 설정(02장)이나 설치된 Git 버전에 따라 달라진다. 여러 컴퓨터에서 작업한다면 `git config --global init.defaultBranch main`으로 명시적으로 통일해 두는 편이 혼란을 줄인다.

## Reference

- [git-init Documentation](https://git-scm.com/docs/git-init)
- [Git Internals - .git Directory (gitrepository-layout)](https://git-scm.com/docs/gitrepository-layout)
