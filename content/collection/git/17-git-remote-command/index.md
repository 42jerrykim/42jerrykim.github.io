---
draft: false
collection_order: 17
slug: git-remote-command-managing-remote-repositories
title: "[Git] 17. git remote — 원격 저장소 등록"
date: 2026-09-04
lastmod: 2026-09-04
description: "git remote로 원격 저장소를 등록·조회·삭제하는 법, origin이라는 이름이 관례일 뿐인 이유, HTTPS와 SSH 두 프로토콜의 차이와 여러 원격을 함께 쓰는 fork 시나리오를 정리한 Git 4부 첫 챕터다."
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
- SSH(Secure Shell)
- Open-Source(오픈소스)
- Career(커리어)
- Command-Line
- CLI
image: "wordcloud.png"
---

3부까지는 로컬 저장소 하나만으로 완결되는 명령들을 다뤘다. 이제 4부에서는 시야를 넓혀, 00장에서 언급했던 "모든 clone이 완전한 히스토리 사본을 가진다"는 분산 모델이 실제로 어떻게 다른 컴퓨터와 데이터를 주고받는지 다룬다. 그 첫 단계가 원격 저장소를 등록하는 `git remote`다.

## 개요

원격 저장소는 URL로 식별되지만, 매번 URL을 전부 입력하지 않도록 짧은 별명(이름)을 붙여 등록한다.

```bash
git remote add origin https://github.com/user/repo.git
git remote -v                        # 등록된 원격 목록과 URL 확인
git remote remove origin              # 등록 제거
git remote rename origin upstream     # 이름 변경
```

`git remote -v`를 실행하면 같은 이름에 대해 fetch용 URL과 push용 URL이 각각 표시된다. 대부분의 경우 둘은 같은 URL이지만, 읽기는 HTTPS로 하고 쓰기는 SSH로 하는 등 분리해 설정하는 것도 가능하다.

## 기본 개념

<strong>origin</strong>이라는 이름은 Git이 강제하는 예약어가 아니라 관례다. `git clone`(18장)으로 저장소를 복제하면 Git이 자동으로 그 원본 저장소를 `origin`이라는 이름으로 등록해주기 때문에, 대부분의 프로젝트에서 이 이름이 자연스럽게 쓰이게 됐을 뿐이다. 원격 저장소 이름은 몇 글자든 원하는 대로 지을 수 있으며, 오픈소스 프로젝트에서 자신의 fork는 `origin`으로, 원본 저장소는 `upstream`으로 구분해 부르는 관례도 이 자유도에서 나온다.

## 종류/세부

### 여러 원격을 등록하는 fork 워크플로

오픈소스 프로젝트에 기여할 때 흔한 구조는 원본 저장소를 GitHub에서 fork한 뒤, 자신의 fork는 `origin`으로, 원본은 `upstream`으로 등록해 두 원격을 함께 쓰는 것이다.

```bash
git remote add origin https://github.com/my-account/project.git
git remote add upstream https://github.com/original-owner/project.git
```

이렇게 등록하면 평소 작업은 `origin`에 push하고, 원본 프로젝트의 최신 변경을 반영하고 싶을 때는 `upstream`에서 fetch(19장)해 자신의 main 브랜치에 병합·리베이스한다. 이 패턴은 21장의 Fork와 Pull Request 워크플로에서 자세히 다룬다.

### HTTPS vs SSH

원격 저장소 URL은 대개 두 가지 프로토콜 형태로 제공된다.

| 프로토콜 | URL 형태 | 인증 방식 |
|---|---|---|
| HTTPS | `https://github.com/user/repo.git` | 개인 액세스 토큰(비밀번호는 더 이상 지원 안 함) 또는 credential helper |
| SSH | `git@github.com:user/repo.git` | SSH 키 쌍 |

HTTPS는 방화벽 환경에서 대체로 문제없이 동작하고 초기 설정이 간단하지만, push할 때마다 토큰 인증이 필요할 수 있다(credential helper로 캐싱 가능). SSH는 키를 한 번 등록해두면 이후 비밀번호 없이 인증되지만, SSH 포트(22번)가 막힌 네트워크에서는 접속 자체가 안 될 수 있다. 이미 등록한 원격의 프로토콜을 바꾸고 싶다면 `git remote set-url`을 쓴다.

```bash
git remote set-url origin git@github.com:user/repo.git
```

### 원격의 상세 정보 조회

특정 원격에 대해 어떤 브랜치들이 있는지, push/fetch 권한이 어떻게 설정되어 있는지 자세히 보고 싶다면 `show`를 쓴다.

```bash
git remote show origin
```

## 주의사항·함정

**`git remote add`로 등록만 하고 fetch하지 않으면 아무것도 받아지지 않는다**: `git remote add`는 URL을 로컬 설정에 기록할 뿐, 실제로 데이터를 가져오지는 않는다. 원격의 브랜치·커밋 정보를 받아오려면 반드시 `git fetch`(19장)를 실행해야 한다.

**원격 URL이 바뀌었는데 로컬 설정을 갱신하지 않아 push가 실패하는 경우**: 조직이 저장소를 다른 계정·서비스로 이전했거나 저장소 이름을 바꿨다면, 로컬에 등록된 원격 URL은 자동으로 갱신되지 않는다. `git remote set-url`로 새 URL을 반영해야 한다.

**원격 이름과 브랜치 이름을 혼동하기 쉽다**: `git push origin main`에서 `origin`은 원격 저장소의 이름이고 `main`은 브랜치 이름으로, 서로 다른 개념을 가리키는 별개의 인자다. 초보자가 자주 헷갈리는 지점이며, 20장에서 push 문법을 다룰 때 다시 짚는다.

## Reference

- [Git Basics - Working with Remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)
- [git-remote Documentation](https://git-scm.com/docs/git-remote)
