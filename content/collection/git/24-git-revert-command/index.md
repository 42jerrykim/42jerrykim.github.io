---
draft: false
collection_order: 24
slug: git-revert-command-safe-undo
title: "[Git] 24. git revert — 안전한 되돌리기"
date: 2026-09-04
lastmod: 2026-09-04
description: "git revert가 히스토리를 재작성하지 않고 반대 변경을 담은 새 커밋을 추가하는 방식으로 안전하게 되돌리는 원리, reset과의 근본적인 차이, 병합 커밋을 되돌릴 때 -m이 필요한 이유를 정리한 Git 챕터다."
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

23장에서 다룬 `git reset`은 이미 공유된 커밋에는 위험하다고 경고했다. `git revert`는 그 위험을 피하면서도 같은 목적(잘못된 커밋을 되돌리기)을 달성하는 명령이다. 두 명령의 결과가 겉보기엔 비슷해 보이지만, 히스토리에 남기는 흔적이 근본적으로 다르다.

## 개요

`git revert`는 지정한 커밋의 변경 내용을 반대로 적용하는 <strong>새 커밋</strong>을 만든다.

```bash
git revert a1b2c3d              # a1b2c3d 커밋의 변경을 취소하는 새 커밋 생성(편집기가 열려 메시지 확인)
git revert --no-edit a1b2c3d    # 기본 메시지("Revert ...")를 그대로 사용
```

예를 들어 어떤 커밋이 `config.debug = true`를 추가했다면, 그 커밋을 revert하면 `config.debug = true`를 제거하는 내용의 새 커밋이 만들어진다. 원래 커밋은 히스토리에서 지워지지 않고 그대로 남아 있으며, 그 위에 "취소하는 내용"이 새로 쌓이는 방식이다.

## 기본 개념

이 방식이 23장의 `reset`과 근본적으로 다른 지점은 <strong>기존 커밋 해시를 하나도 건드리지 않는다</strong>는 것이다. reset은 브랜치 포인터를 과거로 옮겨 이후 커밋들을 (일시적으로) 참조 불가능하게 만들지만, revert는 브랜치를 계속 앞으로만 진행시키면서 "취소"라는 의미를 담은 새 커밋을 추가한다.

| 구분 | git reset | git revert |
|---|---|---|
| 히스토리 재작성 여부 | 재작성함(포인터가 과거로 이동) | 재작성하지 않음(새 커밋 추가) |
| 이미 push된 커밋에 사용 | 위험(강제 push 필요, 20장) | 안전(일반 push로 충분) |
| 되돌린 사실이 히스토리에 남는가 | 남지 않음(마치 그 커밋이 없었던 것처럼 보임) | 남음("Revert ..." 커밋으로 명시적으로 기록) |
| 적합한 상황 | 아직 공유되지 않은 로컬 커밋 정리 | 이미 공유된 브랜치(main 등)의 실수 되돌리기 |

이 표가 실무에서 두 명령을 선택하는 가장 직접적인 기준이다 — 이미 팀원들이 pull해간 `main` 브랜치에서 잘못된 커밋을 되돌려야 한다면, 거의 항상 `reset`이 아니라 `revert`를 써야 한다.

## 종류/세부

### 병합 커밋을 되돌리기

13장에서 다룬 병합 커밋은 부모가 둘이므로, 되돌릴 때 "어느 부모 쪽 히스토리를 기준으로 되돌릴지" 지정해야 한다.

```bash
git revert -m 1 <병합-커밋-해시>
```

`-m 1`은 첫 번째 부모(대개 병합을 받아들인 쪽 브랜치, 예를 들어 `main`)를 기준으로 삼아 되돌리라는 뜻이다. 이 옵션 없이 일반 커밋처럼 revert를 시도하면 Git이 "어느 부모를 기준으로 할지 모호하다"는 오류를 낸다.

### 여러 커밋을 한 번에 되돌리기

```bash
git revert HEAD~2..HEAD    # 최근 두 커밋을 각각 되돌리는 새 커밋을 순서대로 생성
git revert --no-commit a1b2c3d b2c3d4e   # 여러 커밋을 되돌린 뒤 한 번에 커밋(중간에 커밋하지 않음)
```

`--no-commit`(축약 `-n`)은 되돌리는 작업만 스테이징 영역에 반영하고 커밋은 나중에 한 번에 하도록 미뤄, 여러 revert를 하나의 커밋으로 묶고 싶을 때 쓴다.

## 주의사항·함정

**revert가 항상 충돌 없이 끝나는 것은 아니다**: 되돌리려는 커밋 이후에 같은 부분이 다시 수정됐다면, revert도 13장에서 다룬 것과 같은 형식의 충돌을 일으킬 수 있다. 이 경우 절차는 병합 충돌 해결과 동일하다 — 마커를 해결하고 `git add` 후 `git revert --continue`.

**revert한 뒤 다시 그 기능을 붙이려 하면 예상과 다르게 동작할 수 있다**: 한 번 revert한 커밋을 나중에 다시 살리고 싶어 원래 커밋을 `cherry-pick`(26장)하면, 이미 revert가 그 변경을 취소해둔 상태라 다시 revert가 필요해지는 등 혼란스러운 상황이 될 수 있다. 이런 경우 원래 커밋의 diff를 참고해 새로 커밋을 작성하는 편이 오히려 명확할 때가 많다.

**revert 메시지만 보고 원래 무엇이 왜 되돌려졌는지 알기 어려울 수 있다**: 기본 메시지("Revert 'xxx'")는 무엇을 되돌렸는지는 알려주지만 왜 되돌렸는지는 설명하지 않는다. `--no-edit`을 쓰지 않고 편집기를 열어 되돌린 이유(버그 재현, 성능 저하 등)를 본문에 남기면 08장에서 다룬 좋은 커밋 메시지 관례를 그대로 지킬 수 있다.

## Reference

- [git-revert Documentation](https://git-scm.com/docs/git-revert)
