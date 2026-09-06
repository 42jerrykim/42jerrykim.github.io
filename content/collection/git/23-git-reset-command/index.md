---
draft: false
collection_order: 23
slug: git-reset-command-soft-mixed-hard
title: "[Git] 23. git reset — soft/mixed/hard"
date: 2026-09-04
lastmod: 2026-09-04
description: "git reset이 HEAD가 가리키는 위치를 옮기는 명령이라는 원리, soft/mixed/hard 세 모드가 04장의 3단계 모델 중 어디까지 되돌리는지, hard reset의 데이터 손실 위험을 정리한 Git 5부 첫 챕터다."
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
- Diagnostics(진단)
image: "wordcloud.png"
---

`git reset --hard`는 인터넷 검색으로 Git 문제를 해결하려는 사람들이 가장 쉽게 마주치는 명령 중 하나이면서, 동시에 가장 흔하게 데이터를 잃게 만드는 명령이기도 하다. 이 장은 5부의 첫 챕터로, `reset`의 세 모드가 04장의 3단계 모델(작업 트리·스테이징 영역·저장소) 중 정확히 어디까지 되돌리는지 구분한다.

## 개요

`git reset`은 현재 브랜치(HEAD)가 가리키는 커밋을 다른 커밋으로 옮기는 명령이며, 세 가지 모드가 옮기는 범위를 결정한다.

```bash
git reset --soft HEAD~1     # HEAD만 이전 커밋으로 이동, 스테이징·작업 트리는 그대로
git reset --mixed HEAD~1    # HEAD와 스테이징 영역까지 이전 커밋 상태로(기본값, 옵션 생략 시)
git reset --hard HEAD~1     # HEAD·스테이징 영역·작업 트리까지 전부 이전 커밋 상태로
```

`HEAD~1`은 현재 커밋의 바로 이전 커밋을 가리키는 표기로, 09장에서 다룬 커밋 그래프를 부모 방향으로 한 칸 거슬러 올라간 지점이다.

## 기본 개념

세 모드의 차이는 04장의 3단계 모델과 정확히 대응하며, 문단만으로는 "어디까지 영향을 주는가"를 헷갈리기 쉬우므로 그림으로 범위를 겹쳐 보는 편이 명확하다.

```mermaid
flowchart TB
    subgraph soft["--soft"]
        direction LR
        s1["저장소(HEAD)"]:::changed --> s2["스테이징 영역"] --> s3["작업 트리"]
    end
    subgraph mixed["--mixed(기본값)"]
        direction LR
        m1["저장소(HEAD)"]:::changed --> m2["스테이징 영역"]:::changed --> m3["작업 트리"]
    end
    subgraph hard["--hard"]
        direction LR
        h1["저장소(HEAD)"]:::changed --> h2["스테이징 영역"]:::changed --> h3["작업 트리"]:::changed
    end
    classDef changed fill:#f96,stroke:#333
```

`--soft`는 HEAD만 옮기므로, 되돌려진 커밋의 변경 사항은 스테이징 영역에 그대로 남아 있다 — 커밋을 취소하고 다시 커밋 메시지만 고쳐 쓰고 싶을 때 유용하다. `--mixed`(옵션을 생략했을 때의 기본값)는 HEAD와 스테이징 영역까지 옮기므로, 변경 사항은 작업 트리에 스테이징 안 된 상태로 남는다 — 커밋 단위를 다시 나누고 싶을 때 유용하다. `--hard`는 셋 다 옮기므로, 작업 트리의 실제 파일 내용까지 되돌려진 커밋 상태로 강제로 맞춰지며, 그 사이의 모든 변경 사항이 사라진다.

## 종류/세부

### 특정 파일만 되돌리기

`reset`은 브랜치 전체가 아니라 특정 파일만 대상으로 지정할 수도 있다. 이 경우 05장에서 다룬 "스테이징만 취소"하는 동작이 된다.

```bash
git reset HEAD~1 -- README.md   # README.md만 이전 커밋 상태로 스테이징 되돌림(작업 트리는 유지)
git restore --staged README.md   # 05장에서 다룬 최신 방식 표기(HEAD의 최신 커밋 기준)
```

### 잘못된 커밋을 완전히 취소하기(soft reset + 재커밋)

방금 만든 커밋의 메시지를 고치고 싶다면 08장의 `--amend`가 더 직접적이지만, 여러 커밋을 하나로 합치면서 메시지도 새로 쓰고 싶다면 soft reset이 더 유연하다.

```bash
git reset --soft HEAD~3    # 최근 3개 커밋을 취소하되 변경 내용은 스테이징 영역에 유지
git commit -m "새 메시지로 하나의 커밋으로 재작성"
```

이 패턴은 27장에서 다루는 `rebase -i`의 "squash"와 결과가 비슷하지만, 조작이 더 단순한 대신 세밀한 순서 조정은 할 수 없다.

## 주의사항·함정

**`--hard`는 커밋되지 않은 작업을 되돌릴 수 없이 지운다**: 이것이 이 명령에 대한 가장 중요한 경고다. 스테이징되지 않은 작업 트리의 변경, 스테이징됐지만 커밋되지 않은 변경 모두 `--hard` 앞에서는 흔적 없이 사라진다. 실행 전 `git status`(06장)로 지금 무엇이 사라질지 반드시 확인해야 한다.

**되돌려진 커밋 자체는 즉시 사라지는 것이 아니다**: `reset`으로 브랜치 포인터가 옮겨지면, 그 이전에 가리키던 커밋들은 어떤 브랜치에서도 참조되지 않는 상태(unreachable)가 된다. 완전히 삭제되는 것은 아니고 28장의 `git reflog`로 복구할 여지가 얼마간 남아 있지만, 이는 안전망이지 의도적으로 의존할 방법은 아니다.

**이미 push된 커밋을 reset하면 15장·20장과 같은 문제가 생긴다**: `reset`도 리베이스와 마찬가지로 브랜치 히스토리를 재작성하는 효과를 낸다. 이미 원격에 공유된 커밋을 reset한 뒤 push하려면 강제 push가 필요하며, 그로 인한 위험은 20장에서 다룬 것과 동일하다. 공유된 히스토리를 안전하게 취소하고 싶다면 24장에서 다루는 `git revert`가 더 나은 선택이다.

## Reference

- [Git Tools - Reset Demystified](https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified)
- [git-reset Documentation](https://git-scm.com/docs/git-reset)
