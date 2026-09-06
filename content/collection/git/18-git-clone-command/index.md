---
draft: false
collection_order: 18
slug: git-clone-command-copy-repository
title: "[Git] 18. git clone"
date: 2026-09-04
lastmod: 2026-09-04
description: "git clone이 원격 저장소의 전체 히스토리를 로컬에 복제하는 과정, 클론 직후 자동으로 설정되는 origin과 추적 브랜치, --depth를 이용한 shallow clone의 트레이드오프를 정리한 Git 챕터다."
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
- Distributed-Systems(분산시스템)
- Command-Line
- CLI
image: "wordcloud.png"
---

`git clone`은 대부분의 사람이 Git으로 하는 첫 번째 명령이지만, 그 뒤에서 정확히 무슨 일이 일어나는지(전체 히스토리를 통째로 내려받는다는 사실, 자동으로 만들어지는 원격 설정과 추적 브랜치)까지 아는 사람은 드물다. 이 장은 clone의 결과물을 뜯어본다.

## 개요

`git clone`은 원격 저장소의 전체 데이터(`.git` 디렉터리 전체, 03장)를 새 디렉터리에 복제하고, 그 저장소의 최신 커밋을 작업 트리에 체크아웃한다.

```bash
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git my-folder-name    # 다른 디렉터리 이름으로 복제
```

명령이 끝나면 그 결과는 `git init`(03장)으로 만든 저장소와 근본적으로 같은 형태이지만, 세 가지가 자동으로 설정되어 있다는 점이 다르다: 원격 `origin`이 그 URL로 등록되고(17장), 원격의 모든 브랜치 정보가 `refs/remotes/origin/`에 복사되며, 원격의 기본 브랜치(대개 `main`)를 추적하는 로컬 브랜치가 자동으로 만들어져 체크아웃된다.

## 기본 개념

00장에서 설명한 "모든 clone은 완전한 히스토리 사본을 가진다"는 분산 모델의 원칙이 여기서 실제로 확인된다. `git clone`은 최신 스냅샷 하나만 받아오는 것이 아니라, 그 저장소의 첫 커밋부터 지금까지의 전체 커밋 객체·트리·blob(34장에서 다룰 객체 모델)을 함께 내려받는다. 그래서 clone이 끝난 직후에도 네트워크 연결 없이 `git log`(09장)로 전체 히스토리를 조회하거나 과거 어느 커밋으로도 자유롭게 이동(12장)할 수 있다.

## 종류/세부

### Shallow clone — 히스토리 일부만 받기

리눅스 커널처럼 수십만 개의 커밋이 쌓인 거대한 저장소를 통째로 clone하면 시간과 디스크 공간이 상당히 든다. 과거 히스토리가 필요 없고 최신 코드만 필요하다면(예: CI 빌드 환경) `--depth` 옵션으로 clone 범위를 제한할 수 있다.

```bash
git clone --depth 1 https://github.com/user/large-repo.git
```

`--depth 1`은 각 브랜치의 최신 커밋 하나만 받아오고 그 이전 히스토리는 아예 내려받지 않는다. 이렇게 만들어진 저장소를 shallow(얕은) 저장소라 부르며, 이후 필요에 따라 히스토리를 더 받아올 수도 있다(42장에서 자세히 다룬다). 다만 shallow 저장소에서는 `git log`로 과거 커밋을 조회하거나 33장의 `git bisect` 같은 명령이 제한적으로만 동작한다는 트레이드오프가 있다.

| 방식 | 장점 | 단점 |
|---|---|---|
| 전체 clone(기본값) | 히스토리 전체 조회·리베이스·bisect가 자유로움 | 대용량 저장소는 시간·디스크 비용이 큼 |
| Shallow clone(`--depth N`) | 빠르고 가벼움, CI에서 흔히 사용 | 과거 히스토리 조회·일부 명령 제한 |

### 특정 브랜치만 clone

기본적으로 clone은 원격 저장소의 기본 브랜치만 체크아웃하지만(다른 브랜치 정보는 여전히 받아온다), 처음부터 특정 브랜치만 지정해 clone할 수도 있다.

```bash
git clone --branch develop --single-branch https://github.com/user/repo.git
```

`--single-branch`를 함께 쓰면 지정한 브랜치 하나의 히스토리만 받아와 저장소 크기를 더 줄일 수 있다.

## 주의사항·함정

**대용량 저장소를 무심코 전체 clone하면 오래 걸린다**: 오래되고 큰 오픈소스 프로젝트를 처음 clone할 때 예상보다 훨씬 오래 걸린다면, 프로젝트 규모에 비해 `.git` 디렉터리 자체가 크기 때문일 가능성이 높다. CI 환경이나 단순 코드 확인이 목적이라면 `--depth`로 범위를 좁히는 것이 실용적이다.

**Shallow clone에서 push나 특정 명령이 예상과 다르게 동작할 수 있다**: shallow 저장소는 일부 워크플로(전체 히스토리를 요구하는 리베이스, 특정 CI 도구의 태그 조회 등)에서 제약이 있을 수 있다. 문제가 발생하면 `git fetch --unshallow`로 전체 히스토리를 뒤늦게 받아올 수 있다.

**clone 직후 원격 브랜치와 로컬 브랜치를 혼동하기 쉽다**: `git branch -a`(11장)로 보이는 `remotes/origin/develop` 같은 항목은 원격 브랜치의 로컬 사본(읽기 전용 참조)일 뿐, 그대로 커밋을 쌓을 수 있는 로컬 브랜치가 아니다. 그 브랜치에서 작업하려면 `git switch develop`처럼 로컬 추적 브랜치를 만들어야 하며(12장), 이 관계는 20장에서 upstream 추적으로 다시 다룬다.

## Reference

- [git-clone Documentation](https://git-scm.com/docs/git-clone)
