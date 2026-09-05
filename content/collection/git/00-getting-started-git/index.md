---
draft: false
collection_order: 0
slug: getting-started-git
title: "[Git] 00. 과정 개요와 커리큘럼"
date: 2026-09-04
lastmod: 2026-09-04
description: "Git 45챕터 커리큘럼의 과정 개요. 스냅샷 기반 버전 관리라는 정신 모델, 9개 Part 학습 순서의 설계 근거, 00-44장 전체 목차, 선수 지식과 완주 후 실무자가 갖추는 협업·히스토리 관리 역량을 정리한 과정 개요 챕터다."
categories:
- Git
tags:
- Git
- GitHub
- Version-Control(버전관리)
- DevOps
- Terminal
- Guide(가이드)
- Quick-Reference
- Productivity(생산성)
- Open-Source(오픈소스)
- Career(커리어)
- Education(교육)
- Troubleshooting(트러블슈팅)
- Workflow(워크플로우)
- Configuration(설정)
- How-To
- Tips
- Comparison(비교)
- Reference(참고)
- Beginner
- Advanced
- Collaboration(협업)
- Best-Practices
- Documentation(문서화)
- Distributed-Systems(분산시스템)
- 커리큘럼
- 로드맵
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 챕터는 "Git" 컬렉션의 첫 챕터이므로 선행 챕터가 없다. 필요한 선수 지식은 이 장의 "선수 지식" 절에서 별도로 정리한다.

난이도는 입문(터미널을 열어본 적은 있지만 `git`을 처음 쓰는 수준)에서 중급(9개 Part의 순서 논리와 merge·rebase 같은 선택지 사이의 트레이드오프를 판단할 수 있는 수준) 사이를 오간다. 특정 명령의 옵션이나 실행 예시는 다루지 않는다 — 이 장은 지도(map)이지 명령어 레퍼런스가 아니다.

이 장이 다루지 않는 것은 다음과 같다. `git add`·`git rebase`처럼 개별 명령의 옵션과 예시는 01장 이후 각 번호 챕터에서 다룬다. GitHub·GitLab 같은 특정 호스팅 서비스의 UI 조작법(이슈 트래커, 프로젝트 보드 등)은 이 컬렉션의 범위 밖이며, Git 자체의 명령과 개념(원격 저장소, Pull Request가 전제하는 워크플로)만 다룬다.

## 선수 지식

터미널·명령 프롬프트에서 `cd`, `ls`(또는 `dir`) 같은 기본 명령으로 디렉터리를 오가는 경험이면 충분하다. 특정 프로그래밍 언어 지식은 필요하지 않다 — Git은 언어에 무관한 파일 버전 관리 도구다.

## 당신의 수준에 맞는 경로

| 수준 | 읽을 부분 | 핵심 목표 |
|---|---|---|
| Git이 완전히 처음인 입문자 | 전체를 순서대로 | 스냅샷 모델이 왜 중요한지, 어디서부터 시작해야 하는지 이해한다 |
| SVN 등 중앙집중형 VCS 경험자 | 도입, 핵심 개념, 비교/트레이드오프 | 중앙집중형에서 쓰던 습관이 분산형 모델에서 어떻게 달라지는지 파악한다 |
| 명령어 몇 개(add, commit, push)만 외워서 쓰던 실무자 | 3부(브랜치와 병합), 5부(히스토리 되돌리기) | merge 충돌과 실수 복구처럼 급할 때 필요한 지식을 체계적으로 채운다 |
| 여러 명이 함께 쓰는 저장소를 관리해야 하는 담당자 | 4부(원격 저장소와 협업), 8부(확장 기능) | 브랜치 전략, Pull Request 워크플로, hooks·submodule 같은 협업 도구를 확인한다 |
| Git 내부 동작을 정확히 이해하고 싶은 개발자 | 7부(내부 구조) | blob·tree·commit·refs가 실제로 어떻게 저장되는지 확인한다 |

## 도입

Git은 2005년 리누스 토르발스(Linus Torvalds)가 리눅스 커널 개발을 위해 만든 분산 버전 관리 시스템(Distributed Version Control System)이다. 당시 리눅스 커널 프로젝트는 상용 도구인 BitKeeper를 쓰고 있었는데, 라이선스 문제로 더 이상 무료로 쓸 수 없게 되자 토르발스는 대안을 직접 만들기로 했다. 그가 세운 목표는 속도, 단순한 설계, 비선형 개발(수천 개의 병렬 브랜치)에 대한 강력한 지원, 완전한 분산 구조, 리눅스 커널 같은 대규모 프로젝트를 효율적으로 다룰 수 있는 능력이었다. 이 목표들이 지금까지도 Git의 설계 전반에 그대로 남아 있다.

CVS·SVN 같은 이전 세대 버전 관리 시스템이 "중앙 서버에 있는 하나의 히스토리를 여러 사람이 체크아웃해 쓰는" 중앙집중형 모델이었다면, Git은 저장소를 clone하는 모든 사람이 전체 히스토리의 완전한 사본을 로컬에 가진다. 이 차이가 이 컬렉션 전체의 뼈대를 이룬다. 중앙 서버가 없어도 로컬에서 커밋·브랜치·병합·히스토리 조회가 모두 가능하고, 네트워크 연결은 다른 사람과 변경 사항을 주고받을 때만 필요하다.

Git을 배우는 일은 특정 언어나 프레임워크에 국한된 지식이 아니라 현대 소프트웨어 개발 전반의 공용 인프라에 가깝다. 첫째, 오픈소스 생태계 대부분이 Git 위에서 돌아간다 — GitHub·GitLab·Bitbucket 같은 호스팅 서비스는 모두 Git 저장소를 다루는 UI일 뿐, 내부 버전 관리 엔진은 Git이다. 둘째, CI/CD 파이프라인 대부분이 Git의 커밋·태그·브랜치 이벤트를 트리거로 삼는다. 셋째, 여러 사람이 동시에 같은 코드베이스를 수정하는 협업 워크플로(코드 리뷰, Pull Request, 브랜치 전략)가 Git의 브랜치·병합 모델을 전제로 설계되어 있다. 이 세 가지가 이 컬렉션이 9개 Part로 나뉘는 이유이기도 하다 — 각 Part는 이 역량들을 순서대로 습득하도록 설계되어 있다.

## 핵심 개념

<strong>Git</strong>은 파일의 변경 이력을 스냅샷(snapshot) 단위로 기록하는 분산 버전 관리 시스템이다. 여기서 "스냅샷"이라는 표현이 중요한데, CVS·SVN 같은 도구가 파일별로 "이전 버전과의 차이(diff)"를 저장하는 반면, Git은 커밋할 때마다 그 시점의 전체 파일 트리를 통째로 찍어 저장한다(단, 바뀌지 않은 파일은 이전 스냅샷의 파일을 가리키는 참조로 재사용해 중복 저장을 피한다). 이 설계 덕분에 특정 커밋으로 되돌아가거나 두 커밋을 비교하는 연산이 diff를 누적 계산할 필요 없이 빠르게 끝난다.

Git을 처음 배우는 사람이 가장 먼저 정리해야 할 구분은 <strong>작업 트리(Working Tree)</strong>, <strong>스테이징 영역(Staging Area, Index)</strong>, <strong>저장소(Repository)</strong>라는 3단계 영역이다. 작업 트리는 실제로 파일을 편집하는 디렉터리이고, 스테이징 영역은 다음 커밋에 포함할 변경 사항을 임시로 모아두는 공간이며, 저장소는 커밋된 히스토리가 영구히 저장되는 곳이다. `git add`는 작업 트리의 변경을 스테이징 영역으로 옮기고, `git commit`은 스테이징 영역의 내용을 저장소에 새 스냅샷으로 기록한다. 이 구분은 05장에서 더 자세히 짚는다.

이 정신 모델이 커리큘럼 순서를 결정한다. Git이 무엇이고 어떻게 설치·설정하는지(1부)를 모르면 아무것도 시작할 수 없고, 3단계 영역과 기본 스냅샷 워크플로(2부)를 모르면 브랜치(3부)를 만들어도 무엇이 커밋되는지 예측할 수 없다. 원격 저장소와 협업(4부)은 로컬 히스토리를 다른 사람과 주고받는 법을 다루고, 히스토리 되돌리기(5부)는 실수를 안전하게 복구하는 법을, 작업 관리 심화(6부)는 stash·bisect 같은 일상적으로 유용한 도구를 채운다. 내부 구조(7부)는 지금까지 배운 명령들이 실제로 무엇을 저장하고 조작하는지 설명해 응용력을 높이고, 확장 기능(8부)과 운영·트러블슈팅(9부)은 대규모·엔터프라이즈 환경에서 필요한 도구로 마무리한다.

## 비교/트레이드오프

Git을 배우는 방식에는 두 갈래가 있고, 이 컬렉션은 둘 다를 지원하도록 설계됐다.

| 구분 | 필요할 때 검색해서 익히기 | 커리큘럼을 순서대로 읽기 |
|---|---|---|
| 장점 | 당장 급한 `git push` 오류 하나를 가장 빠르게 해결한다 | 빠진 개념 없이 체계적으로 습득하고, 3단계 영역 모델 없이 명령어부터 외우다 막히는 상황을 피한다 |
| 위험 | 스테이징·브랜치 모델을 모른 채 명령어를 복사해 쓰다가 충돌·히스토리 사고에서 응용이 막힌다 | 초반 진입 비용이 검색보다 크다 |
| 적합한 상황 | 이미 기초가 있고 특정 명령의 옵션만 확인하려는 경우 | 처음 Git을 배우거나, merge·rebase 선택 기준처럼 원리를 체계적으로 이해하려는 경우 |

또 다른 트레이드오프는 중앙집중형 VCS(SVN 등)와 Git의 분산형 모델 사이에 있다. 중앙집중형은 하나의 서버가 유일한 진실 공급원(single source of truth)이라 개념이 단순하고 접근 권한 통제가 쉽지만, 서버 연결이 끊기면 커밋 자체가 불가능하고 브랜치 생성·병합 비용이 크다. Git은 모든 clone이 완전한 히스토리 사본이라 오프라인에서도 커밋·브랜치·히스토리 조회가 가능하고 브랜치 생성이 사실상 즉시 끝나지만, "무엇이 진실인가"를 팀이 규칙(브랜치 전략, 코드 리뷰 정책)으로 합의해야 한다. 이 컬렉션은 이 차이가 실제로 드러나는 지점(브랜치 모델, 원격 저장소와의 동기화)을 각 챕터에서 짚어주는 데 집중한다.

아래 다이어그램은 9개 Part가 어떤 순서로 서로를 전제하는지 요약한 것이다.

```mermaid
flowchart LR
    basics["Part 1</br>기초 환경과 설정"]
    snapshot["Part 2</br>스냅샷 워크플로"]
    branch["Part 3</br>브랜치와 병합"]
    remote["Part 4</br>원격 저장소와 협업"]
    history["Part 5</br>히스토리 되돌리기"]
    advanced["Part 6</br>작업 관리 심화"]
    internals["Part 7</br>내부 구조"]
    extension["Part 8</br>확장 기능"]
    ops["Part 9</br>운영·트러블슈팅"]

    basics --> snapshot --> branch --> remote --> history --> advanced --> internals --> extension --> ops
```

이 화살표는 물리적으로 강제되는 순서가 아니라 학습 효율을 위한 권장 순서다. 예를 들어 이미 `git add`·`git commit`을 써본 독자는 2부(스냅샷 워크플로)의 명령 자체는 낯설지 않겠지만, 병합 충돌이 실제로 왜 발생하고 3-way merge가 무엇을 비교하는지(3부 14장)는 커밋 히스토리가 갈라지는 경험을 해봐야 필요성이 체감된다.

## 흔한 오개념

<strong>"Git과 GitHub은 같은 것이다"</strong>는 가장 흔한 오해다. Git은 로컬에서 동작하는 버전 관리 도구 자체이고, GitHub은 그 Git 저장소를 호스팅하고 Pull Request·이슈 트래커 같은 협업 기능을 얹은 서비스 중 하나다. GitLab, Bitbucket, 사내 자체 호스팅 Git 서버도 모두 같은 Git 프로토콜 위에서 동작한다. GitHub 계정이 없어도 로컬 저장소만으로 Git의 커밋·브랜치·병합을 전부 쓸 수 있다는 사실이 이 구분을 가장 잘 보여준다.

<strong>"커밋은 diff(변경 내용)를 저장한다"</strong>는 오해도 흔하다. 실제로 각 커밋은 그 시점의 전체 파일 트리에 대한 스냅샷을 가리키며, `git diff`나 `git log -p`가 보여주는 "변경 내용"은 두 스냅샷을 비교해 그때그때 계산해낸 결과다. 이 차이를 모르면 34장에서 다루는 Git 객체 모델(blob·tree·commit)을 이해하기 어렵고, `git revert`와 `git reset`의 동작 차이도 헷갈리기 쉽다.

<strong>"브랜치는 무겁고 신중하게 만들어야 하는 것이다"</strong>는 오해도 있다. SVN 같은 중앙집중형 VCS에서 브랜치는 저장소 디렉터리 구조를 통째로 복사하는 비용이 큰 작업이었지만, Git의 브랜치는 특정 커밋을 가리키는 41바이트짜리 포인터(참조) 하나를 새로 만드는 것에 불과해 생성·삭제 비용이 사실상 0에 가깝다. 이 가벼움이 3부에서 다루는 "기능 하나마다 브랜치를 새로 만드는" 워크플로의 전제가 된다.

## 커리큘럼 전체 구성

이 과정은 9개 Part, 총 45개 챕터(00장 포함)로 구성된다. Part 구분은 임의의 분류가 아니라 "설치·설정을 할 수 있다 → 스냅샷을 기록할 수 있다 → 브랜치로 작업을 나누고 합칠 수 있다 → 원격 저장소로 협업할 수 있다 → 실수를 되돌릴 수 있다 → 일상적인 작업을 더 편하게 관리할 수 있다 → 내부 동작을 이해한다 → 특수 상황에 확장 기능을 쓸 수 있다 → 대규모·엔터프라이즈 환경을 운영할 수 있다"라는 의존성 순서를 따른다.

이 컬렉션은 이 표를 목차이자 진행 상황판으로 함께 쓴다. 00장부터 44장까지 전체 45개 챕터가 모두 작성되어 이 과정은 완결됐다.

| Part | 챕터 | 제목 |
|---|---|---|
| 0. 개요 | 00 | 과정 개요와 커리큘럼 |
| 1. 기초 환경과 설정 | 01 | [Git 소개 — 분산 버전 관리 시스템과 탄생 배경](/post/git/git-introduction-distributed-version-control-system/) |
| 1. 기초 환경과 설정 | 02 | [Git 설치와 최초 설정 — git config](/post/git/git-install-config-user-setup/) |
| 1. 기초 환경과 설정 | 03 | [git init과 .git 디렉터리 구조](/post/git/git-init-dot-git-directory-structure/) |
| 1. 기초 환경과 설정 | 04 | [작업 트리·스테이징 영역·저장소 3단계 모델](/post/git/git-three-stage-model-working-tree-staging-repository/) |
| 2. 스냅샷 워크플로 | 05 | [git add — 스테이징](/post/git/git-add-command-staging-files/) |
| 2. 스냅샷 워크플로 | 06 | [git status — 상태 확인](/post/git/git-status-command-check-working-tree-state/) |
| 2. 스냅샷 워크플로 | 07 | [git diff — 변경 비교](/post/git/git-diff-command-compare-changes/) |
| 2. 스냅샷 워크플로 | 08 | [git commit — 커밋 작성 규칙](/post/git/git-commit-command-writing-good-commits/) |
| 2. 스냅샷 워크플로 | 09 | [git log — 히스토리 조회](/post/git/git-log-command-view-history/) |
| 2. 스냅샷 워크플로 | 10 | [.gitignore — 추적 제외 규칙](/post/git/gitignore-file-exclude-patterns/) |
| 3. 브랜치와 병합 | 11 | [브랜치 개념과 git branch](/post/git/git-branch-concept-and-command/) |
| 3. 브랜치와 병합 | 12 | [git switch/checkout — 브랜치 전환](/post/git/git-switch-checkout-branch-transition/) |
| 3. 브랜치와 병합 | 13 | [git merge — 병합과 충돌 해결](/post/git/git-merge-command-and-conflict-resolution/) |
| 3. 브랜치와 병합 | 14 | [Fast-forward vs 3-way merge](/post/git/fast-forward-vs-three-way-merge/) |
| 3. 브랜치와 병합 | 15 | [git rebase — 히스토리 재배치](/post/git/git-rebase-command-rewriting-history/) |
| 3. 브랜치와 병합 | 16 | [merge vs rebase 선택 기준](/post/git/merge-vs-rebase-choosing-criteria/) |
| 4. 원격 저장소와 협업 | 17 | [git remote — 원격 저장소 등록](/post/git/git-remote-command-managing-remote-repositories/) |
| 4. 원격 저장소와 협업 | 18 | [git clone](/post/git/git-clone-command-copy-repository/) |
| 4. 원격 저장소와 협업 | 19 | [git fetch vs git pull](/post/git/git-fetch-vs-git-pull/) |
| 4. 원격 저장소와 협업 | 20 | [git push와 upstream 추적](/post/git/git-push-command-upstream-tracking/) |
| 4. 원격 저장소와 협업 | 21 | [Fork와 Pull Request 워크플로(GitHub Flow)](/post/git/fork-pull-request-workflow-github-flow/) |
| 4. 원격 저장소와 협업 | 22 | [git tag — 릴리스 태깅](/post/git/git-tag-command-release-tagging/) |
| 5. 히스토리 되돌리기 | 23 | [git reset — soft/mixed/hard](/post/git/git-reset-command-soft-mixed-hard/) |
| 5. 히스토리 되돌리기 | 24 | [git revert — 안전한 되돌리기](/post/git/git-revert-command-safe-undo/) |
| 5. 히스토리 되돌리기 | 25 | [git restore와 git checkout -- \<file\>](/post/git/git-restore-checkout-file-discard-changes/) |
| 5. 히스토리 되돌리기 | 26 | [git cherry-pick](/post/git/git-cherry-pick-command/) |
| 5. 히스토리 되돌리기 | 27 | [git rebase -i — 인터랙티브 리베이스](/post/git/git-rebase-interactive-mode/) |
| 5. 히스토리 되돌리기 | 28 | [git reflog — 실수 복구](/post/git/git-reflog-command-recover-lost-commits/) |
| 6. 작업 관리 심화 | 29 | [git stash — 임시 저장](/post/git/git-stash-command-temporary-storage/) |
| 6. 작업 관리 심화 | 30 | [git clean — 미추적 파일 정리](/post/git/git-clean-command-remove-untracked-files/) |
| 6. 작업 관리 심화 | 31 | [git add -p — 부분 스테이징](/post/git/git-add-patch-mode-partial-staging/) |
| 6. 작업 관리 심화 | 32 | [git blame — 변경 이력 추적](/post/git/git-blame-command-track-line-history/) |
| 6. 작업 관리 심화 | 33 | [git bisect — 버그 커밋 이분 탐색](/post/git/git-bisect-command-binary-search-bug-commit/) |
| 7. 내부 구조 | 34 | [Git 객체 모델 — blob/tree/commit](/post/git/git-object-model-blob-tree-commit/) |
| 7. 내부 구조 | 35 | [Git refs와 HEAD](/post/git/git-refs-and-head-reference-model/) |
| 7. 내부 구조 | 36 | [Packfile과 git gc](/post/git/packfile-and-git-gc/) |
| 8. 확장 기능 | 37 | [Git submodule](/post/git/git-submodule-nested-repository/) |
| 8. 확장 기능 | 38 | [Git worktree](/post/git/git-worktree-multiple-checkouts/) |
| 8. 확장 기능 | 39 | [Git hooks](/post/git/git-hooks-automation-scripts/) |
| 8. 확장 기능 | 40 | [.gitattributes](/post/git/gitattributes-file-path-specific-behavior/) |
| 8. 확장 기능 | 41 | [Git LFS(Large File Storage)](/post/git/git-lfs-large-file-storage/) |
| 9. 운영·트러블슈팅 | 42 | [대용량 저장소 관리 — shallow clone과 filter-repo](/post/git/large-repository-management-shallow-clone-filter-repo/) |
| 9. 운영·트러블슈팅 | 43 | [커밋 서명(GPG/SSH signing)과 보안](/post/git/commit-signing-gpg-ssh-security/) |
| 9. 운영·트러블슈팅 | 44 | [자주 발생하는 Git 에러와 해결법 총정리](/post/git/common-git-errors-and-solutions/) |
