---
draft: false
collection_order: 36
slug: packfile-and-git-gc
title: "[Git] 36. Packfile과 git gc"
date: 2026-09-04
lastmod: 2026-09-04
description: "34장에서 다룬 개별(loose) 객체가 늘어나면 git gc가 이를 델타 압축된 packfile 하나로 묶어 저장 효율을 높이는 원리, unreachable 객체가 정리되는 기준과 유예 기간, 7부를 마무리하며 지금까지의 내부 구조를 종합하는 챕터다."
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
- File-System(파일시스템)
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
- Diagnostics(진단)
- Command-Line
- CLI
image: "wordcloud.png"
---

34장에서 `git add`·`git commit`을 실행할 때마다 개별(loose) 객체가 `.git/objects/` 아래 하나씩 쌓인다고 설명했다. 이 방식은 단순하지만, 커밋이 수만 개 쌓인 저장소에서는 파일 수 자체가 많아져 비효율적이다. `git gc`는 이런 개별 객체들을 압축된 단일 파일(packfile)로 묶어 7부를 마무리한다.

## 개요

```bash
git gc                # 저장소 정리(느슨한 객체를 packfile로 압축, 불필요한 객체 정리)
git gc --aggressive   # 더 철저한 압축(시간이 오래 걸림, 자주 실행할 필요는 없음)
git count-objects -v  # 현재 느슨한 객체 수와 packfile 상태 확인
```

Git은 대부분의 경우 이 명령을 사용자가 직접 실행할 필요가 없도록 자동화해뒀다 — `git commit`, `git pull`(19장) 같은 일상적인 명령을 실행하다가 느슨한 객체 수가 임계치를 넘으면 백그라운드에서 자동으로 `git gc`가 실행된다.

## 기본 개념

Packfile은 여러 객체를 하나의 파일로 묶으면서, 서로 비슷한 객체 사이의 <strong>델타 압축</strong>을 적용한다. 01장에서 "Git은 델타가 아니라 스냅샷을 저장한다"고 설명했던 것과 모순처럼 보일 수 있지만, 층위가 다르다 — 논리적 모델(커밋이 무엇을 표현하는가)은 항상 스냅샷이지만, 물리적 저장(디스크에 실제로 어떻게 기록하는가)은 압축 효율을 위해 비슷한 blob끼리 델타로 인코딩할 수 있다. 사용자나 다른 Git 명령의 관점에서는 여전히 각 커밋이 완전한 스냅샷을 가리키는 것처럼 동작하며, 이 압축은 내부 저장 방식의 최적화일 뿐이다.

```mermaid
flowchart LR
    loose["느슨한 객체 여러 개</br>(.git/objects/xx/...)"] -->|"git gc"| pack["packfile 1개</br>(비슷한 객체는 델타로 압축)"]
```

## 종류/세부

### Unreachable 객체의 운명

23장(`reset --hard`)과 28장(`reflog`)에서 "되돌려진 커밋은 즉시 삭제되지 않고 unreachable 상태로 얼마간 남는다"고 설명했다. `git gc`가 바로 이 상태를 최종적으로 정리하는 단계다.

| 상태 | 의미 | gc의 처리 |
|---|---|---|
| Reachable | 어떤 브랜치·태그에서든 도달 가능 | 보존, packfile로 압축 |
| Unreachable(reflog 보존 기간 내) | 어떤 참조에서도 도달 불가능하지만 reflog에 흔적이 남아 있음 | 보존(28장에서 다룬 기본 30-90일 유예) |
| Unreachable(유예 기간 지남) | 도달 불가능하고 reflog 보존 기간도 지남 | 삭제 대상 |

즉 28장에서 다룬 reflog의 보존 기간과 이 장의 gc 정리 시점은 같은 메커니즘의 양면이다 — reflog가 살아 있는 동안은 gc가 그 커밋을 지우지 않고, reflog 항목이 만료된 뒤에야 실제로 디스크에서 제거된다.

### 저장소 상태 점검

```bash
git count-objects -v
```

```
count: 42
size: 168
in-pack: 15234
packs: 1
size-pack: 5120
prune-packable: 0
garbage: 0
```

`count`(느슨한 객체 수)가 크다면 아직 packfile로 압축되지 않은 최근 작업이 많다는 뜻이며, Git의 자동 gc 임계치(기본 6,700개)에 도달하면 다음 명령 실행 시 자동으로 정리된다.

### 수동 정리가 필요한 경우

대부분은 자동 gc로 충분하지만, 대용량 파일을 실수로 커밋했다가 히스토리에서 완전히 제거한 직후처럼 즉시 디스크 공간을 회수하고 싶을 때는 수동으로 실행할 수 있다.

```bash
git gc --prune=now    # 유예 기간을 무시하고 즉시 unreachable 객체 정리(신중하게 사용)
```

`--prune=now`는 28장에서 설명한 reflog 기반 복구 안전망을 즉시 무효화하므로, 정말로 더 이상 필요 없는 데이터를 확실히 지우고 싶을 때만 사용한다. 이 명령은 43장에서 다루는 민감 정보 제거 시나리오와 함께 다시 등장한다.

## 주의사항·함정

**gc 도중 저장소를 건드리면 손상 위험이 있다**: `git gc`가 실행되는 동안 다른 Git 명령을 동시에 실행하는 것은(특히 `--aggressive`처럼 시간이 오래 걸리는 경우) 저장소 손상으로 이어질 수 있다. gc가 끝날 때까지 기다리는 편이 안전하다.

**`--prune=now`를 습관적으로 쓰면 실수 복구 기회를 스스로 없앤다**: 28장의 reflog 안전망은 기본 유예 기간이 있어야 의미가 있다. 특별한 이유 없이 즉시 정리 옵션을 상시로 켜두면, 정작 필요할 때 복구할 수 있었던 커밋까지 이미 사라진 뒤일 수 있다.

**Packfile이 생겼다고 개별 객체가 완전히 없어지는 것은 아닐 수 있다**: gc 이후에도 아직 압축되지 않은 최근 객체나, 압축 대상에서 제외된 특수한 상황의 객체가 느슨한 상태로 일부 남아 있을 수 있다. `git count-objects`로 실제 상태를 확인하는 것이 추측보다 정확하다.

## Reference

- [Git Internals - Packfiles](https://git-scm.com/book/en/v2/Git-Internals-Packfiles)
- [git-gc Documentation](https://git-scm.com/docs/git-gc)
