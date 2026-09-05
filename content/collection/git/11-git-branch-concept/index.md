---
draft: false
collection_order: 11
slug: git-branch-concept-and-command
title: "[Git] 11. 브랜치 개념과 git branch"
date: 2026-09-04
lastmod: 2026-09-04
description: "Git 브랜치가 커밋을 가리키는 가벼운 포인터에 불과하다는 실체, git branch로 브랜치를 만들고 목록을 보고 삭제하는 법, 브랜치가 저비용인 이유를 정리한 Git 3부 첫 챕터다."
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
- Command-Line
- CLI
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
- Configuration(설정)
image: "wordcloud.png"
---

새 기능을 작업할 때마다 브랜치를 새로 만드는 습관은 실무에서 거의 당연하게 여겨지지만, 왜 그렇게 가볍게 브랜치를 만들어도 괜찮은지는 브랜치가 실제로 무엇인지 알아야 이해된다. 이 장은 00장에서 미리 언급했던 "브랜치는 41바이트짜리 포인터"라는 설명을 실제 명령으로 확인한다.

## 개요

`git branch`는 브랜치를 만들고, 목록을 보고, 삭제하는 명령이다.

```bash
git branch                      # 현재 브랜치 목록 확인(현재 브랜치에 * 표시)
git branch feature/login        # 새 브랜치 생성(전환은 하지 않음)
git branch -d feature/login     # 병합된 브랜치 삭제(안전)
git branch -D feature/login     # 병합 여부와 무관하게 강제 삭제
```

`git branch feature/login`은 새 브랜치를 만들 뿐 그 브랜치로 전환하지는 않는다. 브랜치 전환은 `git switch`나 `git checkout`으로 하며, 이는 12장에서 다룬다.

## 기본 개념

브랜치의 실체는 03장에서 살펴본 `.git/refs/heads/` 디렉터리 안의 파일 하나다. 파일 이름이 브랜치 이름이고, 파일 내용은 그 브랜치가 가리키는 최신 커밋의 해시(40자)뿐이다. 새 브랜치를 만드는 것은 이 파일 하나를 새로 쓰는 것과 같으므로, 저장소 크기와 무관하게 사실상 즉시 끝난다.

```
.git/refs/heads/main            → 커밋 해시 A
.git/refs/heads/feature/login   → 커밋 해시 A (분기 시점에는 main과 같은 커밋을 가리킴)
```

이 구조를 알면 "브랜치를 만들면 파일이 전부 복사되는가"라는 흔한 의문에 답할 수 있다 — 복사되지 않는다. 새 브랜치는 만들어진 시점에 원본 브랜치와 정확히 같은 커밋을 가리키며, 이후 그 브랜치 위에서 커밋이 쌓일 때마다 포인터가 새 커밋으로 옮겨간다. 여러 브랜치가 같은 커밋 히스토리를 공유하다가 각자 다른 지점에서 갈라져 나가는 구조가 이렇게 만들어진다.

## 종류/세부

### 브랜치 목록 옵션

브랜치가 많아지면 목록을 필터링하거나 추가 정보를 함께 보고 싶을 때가 있다.

```bash
git branch -v                    # 각 브랜치의 최신 커밋 정보까지 표시
git branch --merged              # 현재 브랜치에 이미 병합된 브랜치만
git branch --no-merged           # 아직 병합되지 않은 브랜치만
git branch -a                    # 원격 브랜치까지 포함한 전체 목록(17장에서 원격을 다룬 뒤 유용해짐)
```

`--merged`로 나온 브랜치 목록은 안전하게 삭제해도 되는 후보다 — 이미 현재 브랜치에 그 내용이 모두 반영되어 있으므로, 삭제해도 커밋이 유실되지 않는다. 반대로 `--no-merged`에 나온 브랜치를 `-d`(소문자)로 삭제하려 하면 Git이 경고를 띄우고 거부하는데, 이는 아직 반영되지 않은 작업이 사라질 위험을 막기 위한 안전장치다.

### 브랜치 이름 규칙

Git 자체는 브랜치 이름에 특별한 규칙을 강제하지 않지만(공백·물결표·콜론 등 일부 문자만 금지), 팀 단위로는 관례를 정해 쓰는 경우가 많다.

| 접두어 관례 | 용도 |
|---|---|
| `feature/기능명` | 새 기능 개발 |
| `fix/버그명` | 버그 수정 |
| `release/버전` | 릴리스 준비 |
| `hotfix/이슈` | 운영 환경 긴급 수정 |

이런 접두어 규칙 자체는 21장에서 다루는 브랜치 전략(GitHub Flow 등)의 일부로, Git이 강제하는 것이 아니라 팀이 합의해 따르는 관례라는 점을 00장의 흔한 오개념에서 이미 짚었다.

## 주의사항·함정

**현재 체크아웃된 브랜치는 삭제할 수 없다**: `git branch -d`로 지금 작업 중인 브랜치 자체를 지우려 하면 오류가 난다. 다른 브랜치로 전환(12장)한 뒤에야 삭제가 가능하다.

**`-D`(대문자)는 안전장치를 건너뛴다**: 병합되지 않은 브랜치를 강제로 삭제하면 그 브랜치에만 있던 커밋은 어떤 브랜치 참조에서도 가리켜지지 않는 상태(unreachable)가 된다. 완전히 사라지는 것은 아니고 28장의 `git reflog`로 복구할 여지가 남아 있지만, Git이 이런 커밋을 가비지 컬렉션(36장)으로 정리하기 전까지의 유예 기간에만 가능하므로 확신 없이 `-D`를 쓰지 않는 편이 안전하다.

**로컬 브랜치 삭제가 원격 브랜치까지 지우지는 않는다**: `git branch -d feature/login`은 로컬 저장소의 참조만 지운다. 원격 저장소(GitHub 등)에 올라간 같은 이름의 브랜치는 별도로 삭제해야 하며, 이는 20장에서 원격 push와 함께 다룬다.

## Reference

- [Git Branching - Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [git-branch Documentation](https://git-scm.com/docs/git-branch)
