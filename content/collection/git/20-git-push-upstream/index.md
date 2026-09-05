---
draft: false
collection_order: 20
slug: git-push-command-upstream-tracking
title: "[Git] 20. git push와 upstream 추적"
date: 2026-09-04
lastmod: 2026-09-04
description: "git push로 로컬 커밋을 원격에 반영하는 법, -u 옵션으로 로컬·원격 브랜치의 upstream 추적 관계를 설정하는 이유, push가 거부되는 경우와 --force-with-lease의 안전성을 정리한 Git 챕터다."
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
- Security(보안)
- Command-Line
- CLI
image: "wordcloud.png"
---

`git push`가 거부되며 "Updates were rejected because the tip of your current branch is behind"라는 메시지를 처음 만나면, 무엇을 어떻게 해야 할지 막막할 수 있다. 이 장은 push의 기본 동작과, 그 거부가 실제로는 협업 중 데이터 손실을 막는 안전장치라는 점을 다룬다.

## 개요

`git push`는 로컬 브랜치의 커밋을 원격 저장소에 반영한다.

```bash
git push origin main              # origin의 main 브랜치에 로컬 main의 커밋을 반영
git push -u origin feature/login  # 최초 push 시 upstream 추적 관계도 함께 설정
git push                          # upstream이 설정된 이후에는 원격·브랜치 생략 가능
```

`-u`(`--set-upstream`)는 로컬 브랜치와 원격 브랜치 사이에 "이 로컬 브랜치는 저 원격 브랜치를 추적한다"는 관계를 기록한다. 이 관계가 한 번 설정되면 이후에는 `git push`, `git pull`(19장)을 인자 없이 실행해도 Git이 어느 원격의 어느 브랜치를 대상으로 할지 스스로 판단한다.

## 기본 개념

Upstream 추적 관계는 06장에서 다룬 `git status`의 "ahead N / behind N" 표시, 09장의 `git log --graph --all`에서 보이는 `origin/main` 참조와도 연결된다. 이 관계 덕분에 Git은 로컬 브랜치가 원격보다 몇 커밋 앞서 있는지, 뒤처져 있는지를 계산할 수 있다. `git clone`(18장)으로 저장소를 복제하면 기본 브랜치에는 이 관계가 자동으로 설정되지만, 로컬에서 새로 만든 브랜치(11장의 `git branch`, `git switch -c`)는 처음 push할 때 명시적으로 `-u`를 붙여줘야 한다.

## 종류/세부

### Push가 거부되는 경우와 그 이유

원격 브랜치가 로컬이 알고 있는 상태보다 앞서 있으면(다른 사람이 먼저 push했거나, 다른 컴퓨터에서 먼저 작업했을 때) push가 거부된다.

```
! [rejected]        main -> main (fetch first)
error: failed to push some refs
```

이 거부는 버그가 아니라 <strong>다른 사람의 커밋을 실수로 덮어쓰지 못하게 막는 안전장치</strong>다. 올바른 대응은 먼저 원격의 최신 내용을 받아와 반영(`git fetch` + merge/rebase, 19장)한 뒤 다시 push하는 것이다.

```bash
git pull origin main    # 또는 git fetch + git rebase(16장의 선택 기준에 따라)
git push origin main
```

### 강제 push와 `--force-with-lease`

15장에서 다룬 리베이스처럼 이미 push된 커밋을 로컬에서 재작성했다면, 일반 push는 거부되고 강제 push가 필요하다.

```bash
git push --force origin feature/login          # 위험: 원격의 최신 상태를 확인 없이 덮어씀
git push --force-with-lease origin feature/login  # 안전: 마지막으로 내가 fetch한 상태와 원격이 같을 때만 덮어씀
```

`--force`는 원격 브랜치를 로컬 상태로 완전히 덮어쓰며, 그사이 다른 사람이 push한 커밋이 있었다면 그 커밋을 통째로 지워버릴 수 있다. `--force-with-lease`는 push하기 전에 "내가 마지막으로 확인한 원격 상태와 지금 원격의 실제 상태가 같은가"를 검사해, 다른 사람이 그사이 push했다면 실패시킨다. 리베이스 후 강제 push가 필요한 상황에서는 `--force-with-lease`를 기본으로 쓰는 것이 안전하다.

| 옵션 | 다른 사람의 push 여부 확인 | 위험도 |
|---|---|---|
| `--force` | 확인하지 않음 | 높음(타인의 작업을 덮어쓸 수 있음) |
| `--force-with-lease` | 확인함(예상과 다르면 거부) | 낮음(개인 브랜치에서 안전하게 사용 가능) |

### 브랜치와 태그 삭제

원격 브랜치나 태그(22장)를 삭제할 때도 push 명령을 쓴다.

```bash
git push origin --delete feature/login    # 원격 브랜치 삭제
git push origin --delete v1.0.0            # 원격 태그 삭제
```

## 주의사항·함정

**메인 브랜치에 `--force`를 실행하면 팀 전체에 영향을 준다**: `main`이나 `develop`처럼 여러 사람이 공유하는 브랜치에 강제 push를 하면, 그 브랜치를 기준으로 작업하던 모든 사람의 히스토리가 어긋난다. 대부분의 팀은 GitHub 등에서 이런 브랜치에 강제 push 자체를 금지하는 보호 규칙(branch protection)을 걸어둔다.

**`-u` 없이 push한 브랜치는 다음에도 매번 전체 인자를 입력해야 한다**: upstream이 설정되지 않은 브랜치에서 `git push`만 실행하면 Git이 오류를 내며 "어디로 push할지 모르겠다"고 알려준다. 처음 push할 때 `-u`를 붙이는 습관이 이후 작업을 편하게 만든다.

**로컬 브랜치를 삭제해도 원격 브랜치는 남아 있다**: 11장에서 다룬 `git branch -d`는 로컬 참조만 지운다. 원격에 올린 브랜치까지 정리하려면 위에서 설명한 `git push origin --delete`가 별도로 필요하다.

## Reference

- [git-push Documentation](https://git-scm.com/docs/git-push)
