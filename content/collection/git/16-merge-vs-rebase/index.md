---
draft: false
collection_order: 16
slug: merge-vs-rebase-choosing-criteria
title: "[Git] 16. merge vs rebase 선택 기준"
date: 2026-09-04
lastmod: 2026-09-04
description: "13-15장에서 다룬 merge와 rebase를 실무에서 언제 선택할지, 공유 브랜치와 개인 브랜치를 나누는 기준, 두 방식을 함께 쓰는 팀 워크플로 패턴을 정리한 Git 3부 마무리 챕터다."
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
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
- Code-Review(코드리뷰)
- Command-Line
- CLI
image: "wordcloud.png"
---

"merge를 써야 하는가, rebase를 써야 하는가"는 Git을 어느 정도 다뤄본 사람들 사이에서도 종종 의견이 갈리는 주제다. 정답이 하나로 정해진 문제가 아니라, 13장과 15장에서 각각 살펴본 두 방식의 결과가 다르기 때문에 상황에 따라 선호가 갈리는 트레이드오프에 가깝다. 이 장은 3부를 마무리하며 그 선택 기준을 정리한다.

## 개요

두 방식이 만들어내는 히스토리의 모양부터 다르다.

| 구분 | git merge | git rebase |
|---|---|---|
| 원본 커밋 | 그대로 유지 | 새 해시로 재작성 |
| 히스토리 모양 | 브랜치가 갈라졌다 합쳐진 그래프 | 하나의 직선 |
| 충돌 해결 횟수 | 한 번(전체를 한 번에 비교) | 옮기는 커밋 수만큼 반복될 수 있음 |
| 공유된 커밋에 적용 가능 여부 | 안전 | 위험(15장의 "황금률") |
| "이 기능이 언제 브랜치에서 들어왔는가" 추적 | 병합 커밋으로 명확히 남음 | 흔적이 사라짐(직선으로 흡수됨) |

## 기본 개념

이 선택은 근본적으로 "히스토리를 실제로 있었던 일의 기록으로 볼 것인가, 읽기 쉬운 최종 결과로 다듬을 것인가"라는 관점 차이에서 나온다. Merge는 "이 시점에 두 갈래 작업이 실제로 이렇게 합쳐졌다"는 사실을 있는 그대로 남긴다. Rebase는 "이 작업은 처음부터 최신 지점에서 시작한 것처럼 보이게" 히스토리를 다듬어, 결과를 읽는 사람 입장에서 더 단순하게 만든다. 어느 쪽이 "진짜" 히스토리인가는 철학의 문제이지 기술적 정답의 문제가 아니다.

## 종류/세부

### 실무에서 흔히 쓰이는 절충 패턴

대부분의 팀은 둘 중 하나만 쓰기보다, 상황별로 나눠 쓰는 패턴을 택한다.

| 상황 | 권장 |
|---|---|
| 아직 아무에게도 공유하지 않은 내 로컬 기능 브랜치를 최신 main에 맞추고 싶을 때 | rebase — 깔끔한 직선 히스토리로 유지 |
| Pull Request를 올리기 전, 지저분한 작업 커밋들을 정리하고 싶을 때 | `rebase -i`(27장) — 논리적 단위로 재구성 |
| 이미 다른 사람과 공유 중인 브랜치(팀 전체가 pull해서 쓰는 브랜치) | merge — 리베이스로 인한 히스토리 어긋남 방지 |
| Pull Request를 최종적으로 main에 반영할 때 | 팀 정책에 따라 다름(GitHub의 "Squash and merge", "Rebase and merge", "Create a merge commit" 옵션이 각각 이 셋에 대응) |

GitHub 같은 호스팅 서비스가 Pull Request 병합 버튼에서 세 가지 옵션을 제공하는 것도 이 트레이드오프를 팀마다 다르게 선택할 수 있게 하기 위해서다. Squash and merge는 기능 브랜치의 모든 커밋을 하나로 합쳐 병합하는 방식으로, 개인 브랜치의 지저분한 작업 이력을 감추면서도 리베이스처럼 원본 커밋을 재작성하지 않는 절충안이다.

### 판단을 위한 질문 두 가지

브랜치 하나를 놓고 merge와 rebase 중 고민된다면, 다음 두 질문으로 좁힐 수 있다. 첫째, 이 브랜치를 나 말고 다른 사람도 pull해서 쓰고 있는가 — 그렇다면 rebase는 위험하다(15장). 둘째, 이 브랜치가 왜 따로 존재했는지(무슨 기능이었는지)를 나중에 히스토리에서 확인할 필요가 있는가 — 그렇다면 병합 커밋을 남기는 merge(또는 `--no-ff`, 14장)가 유리하다.

## 주의사항·함정

**"rebase가 항상 더 좋은 방법"이라는 오해**: 히스토리가 깔끔해 보인다는 이유로 rebase를 무조건 선호하는 경우가 있지만, 15장에서 다뤘듯 공유된 커밋에 적용하면 협업자 전체의 히스토리가 꼬인다. "깔끔함"과 "안전함"은 서로 다른 축이며, 상황에 따라 어느 쪽을 우선할지 판단해야 한다.

**"merge를 쓰면 히스토리가 지저분해서 나쁘다"는 오해**: 갈라졌다 합쳐지는 그래프 모양은 실제로 두 갈래에서 독립적으로 작업이 있었다는 사실을 정확히 반영한다. 이것이 "지저분하다"고 느껴진다면, 문제는 merge 자체가 아니라 기능 브랜치를 너무 오래 유지한 것(main과 너무 오래 갈라져 있던 것)일 수 있다.

**squash merge 후 로컬 브랜치를 rebase하면 혼란스러운 결과가 나온다**: GitHub에서 Squash and merge로 Pull Request를 병합한 뒤, 로컬의 원래 기능 브랜치에서 `git rebase main`을 실행하면 이미 main에 반영된 커밋들이 다시 "새로운 변경"으로 인식되어 재적용을 시도하는 경우가 있다. 이런 상황에서는 기능 브랜치를 아예 삭제하고 최신 main에서 새로 시작하는 편이 간단할 때가 많다.

## Reference

- [Git Branching - Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
- [Distributed Git - Distributed Workflows](https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows)
