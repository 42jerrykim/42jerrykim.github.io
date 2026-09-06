---
draft: false
collection_order: 28
slug: git-reflog-command-recover-lost-commits
title: "[Git] 28. git reflog — 실수 복구"
date: 2026-09-04
lastmod: 2026-09-04
description: "git reflog가 HEAD의 이동 이력을 별도로 기록해 hard reset이나 브랜치 강제 삭제로 잃어버린 것처럼 보이는 커밋을 되찾는 원리, reflog의 로컬 전용 특성과 만료 기간을 정리한 Git 5부 마무리 챕터다."
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
- Diagnostics(진단)
- Open-Source(오픈소스)
- Career(커리어)
- Configuration(설정)
image: "wordcloud.png"
---

23장에서 `git reset --hard`를 다루며 "되돌려진 커밋은 즉시 사라지는 것이 아니라 얼마간 복구할 여지가 남는다"고 언급했다. `git reflog`가 바로 그 복구를 가능하게 하는 안전망이다. 이 장은 5부를 마무리하며, 실수로 브랜치를 잘못 되돌리거나 삭제했을 때 가장 먼저 확인해야 할 이 명령을 다룬다.

## 개요

```bash
git reflog
```

```
a1b2c3d (HEAD -> main) HEAD@{0}: reset: moving to HEAD~3
d4e5f6g HEAD@{1}: commit: 기능 C 추가
9f8e7d6 HEAD@{2}: commit: 기능 B 추가
3f2a1c9 HEAD@{3}: commit: 기능 A 추가
```

이 목록은 09장에서 다룬 `git log`와 근본적으로 다른 것을 보여준다 — `git log`가 커밋 그래프(부모 관계)를 따라가는 히스토리라면, `reflog`는 <strong>이 컴퓨터에서 HEAD가 실제로 어떤 순서로 어디를 가리켰는지</strong>의 이동 기록이다. 위 예시에서 `reset: moving to HEAD~3`이 실행되기 전, HEAD는 `d4e5f6g`(기능 C 추가)를 가리키고 있었다는 사실이 `HEAD@{1}`에 그대로 남아 있다.

## 기본 개념

23장에서 `reset --hard`로 커밋을 되돌리면 그 커밋들이 즉시 삭제되는 것이 아니라 unreachable(어느 브랜치에서도 참조되지 않는) 상태가 될 뿐이라고 설명했다. reflog는 정확히 이런 상황을 위한 기록이다 — 브랜치 참조(`refs/heads/main`)는 방금 과거로 옮겨졌지만, reflog에는 "옮기기 직전에 어디를 가리켰는지"가 그대로 남아 있으므로, 그 지점으로 다시 돌아가는 것이 가능하다.

```bash
git reset --hard HEAD@{1}    # reflog에서 확인한 "기능 C 추가" 시점으로 복구
```

## 종류/세부

### 대표적인 복구 시나리오

**시나리오 1: 잘못된 hard reset을 되돌리기**

```bash
git reset --hard HEAD~3    # 실수로 3개 커밋을 날림
git reflog                  # HEAD@{1}이 reset 직전 상태임을 확인
git reset --hard HEAD@{1}   # 복구
```

**시나리오 2: 강제 삭제한 브랜치의 커밋 복구**

11장에서 다룬 `git branch -D`로 브랜치를 강제 삭제했다면, 브랜치 이름 자체는 사라지지만 그 브랜치에서 마지막으로 커밋했던 시점은 reflog에 남아 있을 수 있다.

```bash
git reflog                              # 삭제된 브랜치의 마지막 커밋 해시를 찾음
git switch -c recovered-branch a1b2c3d   # 그 해시로 새 브랜치를 만들어 복구
```

**시나리오 3: 리베이스가 잘못됐을 때**

15장·27장의 리베이스 도중 예상과 다른 결과가 나왔는데 이미 `--abort`할 시점을 놓쳤다면, reflog에서 리베이스 시작 전 상태를 찾아 되돌릴 수 있다.

```bash
git reflog                    # "rebase (start): checkout main" 같은 항목 확인
git reset --hard HEAD@{5}      # 리베이스 시작 직전 지점으로
```

### reflog의 한계

| 특성 | 내용 |
|---|---|
| 저장 위치 | 로컬 저장소(`.git/logs/`)에만 존재 |
| 원격 공유 여부 | 공유되지 않음(clone·push/pull로 전달되지 않음) |
| 보존 기간 | 기본적으로 도달 가능한 커밋은 90일, 도달 불가능한 커밋은 30일(설정으로 조정 가능) |
| 대상 | HEAD뿐 아니라 각 브랜치별로도 개별 reflog가 존재(`git reflog show <branch>`) |

reflog가 로컬에만 존재한다는 점이 중요하다 — 다른 컴퓨터나 원격 저장소에는 이 기록이 없으므로, 같은 실수를 다른 환경에서는 reflog로 복구할 수 없다.

## 주의사항·함정

**reflog도 영구적인 백업은 아니다**: 위 표에서 보듯 도달 불가능한 커밋은 기본 30일 후 가비지 컬렉션(36장) 대상이 될 수 있다. 실수를 발견했다면 가능한 한 빨리 reflog로 확인·복구하는 것이 안전하며, "나중에 처리해도 되겠지"라고 미루면 복구 창이 닫힐 수 있다.

**`git reflog expire`나 `git gc --aggressive`를 실수로 실행하면 복구 여지가 줄어든다**: 이런 명령은 정상적인 저장소 유지보수 목적이지만, 아직 검토하지 않은 최근 reflog 항목까지 만료시켜 복구 가능성을 낮출 수 있다. 복구가 필요한 상황이라면 이런 정리 명령을 먼저 실행하지 않는다.

**reflog 항목 번호(`HEAD@{N}`)는 새 작업을 할 때마다 계속 바뀐다**: `git reflog`로 확인한 시점과 실제로 `reset`을 실행하는 시점 사이에 다른 Git 명령(체크아웃, 커밋 등)을 실행하면 번호가 밀릴 수 있다. 복구 직전에 다시 한번 `git reflog`로 정확한 번호(또는 해시)를 확인하는 편이 안전하다.

## Reference

- [Git Internals - Maintenance and Data Recovery](https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery)
- [git-reflog Documentation](https://git-scm.com/docs/git-reflog)
