---
draft: false
collection_order: 12
slug: git-switch-checkout-branch-transition
title: "[Git] 12. git switch/checkout — 브랜치 전환"
date: 2026-09-04
lastmod: 2026-09-04
description: "git switch로 브랜치를 전환하는 법과, 오래된 git checkout이 브랜치 전환·파일 복원·커밋 체크아웃을 한 명령에 묶어 생긴 혼란, detached HEAD 상태가 위험하지 않은 이유를 정리한 Git 챕터다."
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
- Open-Source(오픈소스)
- Career(커리어)
- Configuration(설정)
- File-System(파일시스템)
image: "wordcloud.png"
---

11장에서 만든 브랜치는 그 자체로는 아무 효과가 없다 — 실제로 그 브랜치 위에서 작업하려면 HEAD(03장에서 다룬, "지금 어디에 있는가"를 가리키는 참조)를 그 브랜치로 옮겨야 한다. 이 장은 그 전환 명령과, 오래된 `git checkout`이 왜 여러 용도로 겹쳐 쓰여 혼란을 낳았는지를 다룬다.

## 개요

Git 2.23(2019년)부터 브랜치 전환 전용 명령 `git switch`가 도입됐다.

```bash
git switch feature/login          # 기존 브랜치로 전환
git switch -c feature/payment     # 새 브랜치를 만들면서 동시에 전환(-c는 create)
git switch -                      # 바로 직전에 있던 브랜치로 되돌아가기
```

그 이전까지, 그리고 지금도 여전히 널리 쓰이는 명령은 `git checkout`이다.

```bash
git checkout feature/login        # switch와 동일한 브랜치 전환
git checkout -b feature/payment   # switch -c와 동일
```

## 기본 개념

`git checkout`이 혼란을 낳은 이유는 이 명령 하나가 서로 다른 세 가지 작업(브랜치 전환, 특정 커밋으로 이동, 파일 내용 복원)을 인자의 형태만으로 구분해 처리했기 때문이다. `git checkout <branch>`는 브랜치 전환이지만, `git checkout -- <file>`은 05장에서 다룬 스테이징과 무관하게 파일 내용을 되돌리는 완전히 다른 동작이다. 이 중의성을 해소하기 위해 Git 2.23은 브랜치 전환을 `git switch`로, 파일 복원을 `git restore`로 분리했다.

| 오래된 방식(`checkout`) | 새 방식(2.23+) | 하는 일 |
|---|---|---|
| `git checkout <branch>` | `git switch <branch>` | 브랜치 전환 |
| `git checkout -b <branch>` | `git switch -c <branch>` | 브랜치 생성 후 전환 |
| `git checkout -- <file>` | `git restore <file>` | 파일 내용을 마지막 커밋 상태로 복원(25장) |
| `git checkout <commit>` | (전용 대체 명령 없음, `switch --detach`) | 특정 커밋으로 이동(detached HEAD) |

새 프로젝트라면 의도가 명확한 `switch`·`restore`를 쓰는 편이 실수를 줄인다. 다만 인터넷의 수많은 기존 자료와 스크립트가 여전히 `checkout`을 쓰므로, 두 계열 모두 읽을 줄 알아야 한다.

## 종류/세부

### Detached HEAD 상태

브랜치 이름이 아니라 커밋 해시나 태그로 직접 전환하면, HEAD가 브랜치를 거치지 않고 커밋을 곧바로 가리키는 detached HEAD 상태가 된다.

```bash
git switch --detach a1b2c3d
# 또는
git checkout a1b2c3d
```

```
On branch main            →     HEAD detached at a1b2c3d
```

이 상태에서 새 커밋을 만들면 그 커밋은 어떤 브랜치 참조에도 연결되지 않는다. 다른 브랜치로 전환하는 순간, 그 커밋을 가리키는 브랜치가 하나도 없다면 해당 커밋은 unreachable 상태가 되어 결국 36장의 가비지 컬렉션 대상이 될 수 있다. 이 상태에서 작업한 내용을 보존하고 싶다면 전환하기 전에 반드시 새 브랜치를 만들어 현재 커밋에 이름을 붙여야 한다.

```bash
git switch -c keep-this-work   # detached HEAD에서 작업한 커밋을 새 브랜치로 보존
```

### 전환 중 충돌

작업 트리에 커밋되지 않은 변경이 남아 있는 상태에서 다른 브랜치로 전환하면, 그 변경이 전환 대상 브랜치의 같은 파일과 겹칠 경우 Git이 전환을 거부한다.

```
error: Your local changes to the following files would be overwritten by checkout
```

이때 선택지는 세 가지다 — 변경을 커밋(08장)하거나, 스테이징하지 않고 임시로 치워두는 `git stash`(29장)를 쓰거나, `git switch --force`로 변경을 버리고 강제 전환한다. 마지막 방법은 커밋되지 않은 작업을 되돌릴 수 없이 잃는 위험이 있다.

## 주의사항·함정

**detached HEAD를 "위험한 상태"로 오해하기 쉽다**: detached HEAD 자체는 읽기 전용 열람(과거 커밋 확인, 빌드 재현 등)에 흔히 쓰이는 정상적인 상태다. 위험은 그 상태에서 새로 커밋한 뒤 브랜치로 보존하지 않고 다른 곳으로 전환할 때만 생긴다.

**`checkout`으로 파일을 복원하려다 실수로 브랜치를 전환하는 사고**: `git checkout <이름>`에서 `<이름>`이 브랜치 이름과 파일 이름 둘 다에 해당할 수 있다면, Git은 우선 브랜치로 해석한다. 의도한 것이 파일 복원이라면 `git checkout -- <file>`처럼 `--` 구분자를 반드시 붙이거나, 아예 `git restore <file>`을 쓰는 편이 이런 혼동을 원천적으로 막는다.

**전환 후 원격 추적 브랜치와의 관계가 자동으로 설정되지 않을 수 있다**: 원격 브랜치를 처음 체크아웃할 때 로컬 브랜치 이름이 원격과 정확히 같으면 Git이 자동으로 추적 관계를 설정해주지만, 이름을 다르게 지정하면 수동으로 업스트림을 설정해야 한다. 이는 20장의 push/upstream에서 다시 다룬다.

## Reference

- [git-switch Documentation](https://git-scm.com/docs/git-switch)
- [git-checkout Documentation](https://git-scm.com/docs/git-checkout)
