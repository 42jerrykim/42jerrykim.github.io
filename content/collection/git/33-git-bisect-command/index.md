---
draft: false
collection_order: 33
slug: git-bisect-command-binary-search-bug-commit
title: "[Git] 33. git bisect — 버그 커밋 이분 탐색"
date: 2026-09-04
lastmod: 2026-09-04
description: "git bisect가 이분 탐색으로 버그를 처음 만든 커밋을 O(log n) 번의 테스트만으로 찾아내는 원리, good/bad로 범위를 좁히는 절차, 테스트 스크립트를 연결해 전 과정을 자동화하는 run 옵션을 정리한 Git 6부 마무리 챕터다."
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
- Diagnostics(진단)
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
- Testing(테스팅)
image: "wordcloud.png"
---

수백 개의 커밋 중 어딘가에서 버그가 생겼다는 것은 알지만 정확히 어느 커밋인지 모를 때, 커밋을 하나씩 순서대로 확인하면 최악의 경우 수백 번의 테스트가 필요하다. `git bisect`는 이 탐색을 이분 탐색(binary search) 방식으로 바꿔, 6부의 마지막 챕터로서 09장의 히스토리 조회 도구들을 실전 디버깅에 응용한다.

## 개요

```bash
git bisect start
git bisect bad                  # 지금 버전에는 버그가 있음
git bisect good v1.0.0           # v1.0.0 시점에는 버그가 없었음(22장의 태그 활용)
```

이 세 명령을 실행하면 Git은 `good`과 `bad` 사이의 커밋 중 정확히 중간 지점으로 자동 체크아웃(12장)한다. 그 지점에서 버그를 재현해보고 결과를 알려준다.

```bash
git bisect good    # 이 지점에는 버그가 없다면
# 또는
git bisect bad     # 이 지점에도 버그가 있다면
```

이 과정을 반복할 때마다 탐색 범위가 절반으로 줄어들고, 최종적으로 Git이 "버그를 처음 만든 커밋"을 정확히 지목한다.

## 기본 개념

이 명령이 효율적인 이유는 이름 그대로 이분 탐색이기 때문이다. `good`과 `bad` 사이에 1,000개의 커밋이 있다면, 순차 탐색은 최악의 경우 1,000번의 테스트가 필요하지만 이분 탐색은 <code>log₂(1,000) ≈ 10</code>번이면 충분하다. 커밋 수가 많은 저장소일수록 이 차이는 극적으로 벌어진다.

| 방식 | 1,000개 커밋 중 탐색에 필요한 최대 테스트 횟수 |
|---|---|
| 순차 탐색(하나씩 확인) | 최대 1,000번 |
| 이분 탐색(`git bisect`) | 최대 약 10번 |

## 종류/세부

### 탐색 종료와 결과 확인

Git이 범위를 하나의 커밋으로 좁히면 다음과 같이 알려준다.

```
9f8e7d6 is the first bad commit
```

이 시점에서 `git show`(09장에서 다룬 `git log -p`와 유사)로 그 커밋이 정확히 무엇을 바꿨는지 확인하고, 원인을 파악한 뒤 탐색을 종료해 원래 브랜치로 돌아간다.

```bash
git bisect reset    # 시작하기 전 브랜치·커밋 상태로 복귀
```

`reset`을 실행하지 않으면 detached HEAD(12장) 상태에 계속 머무르게 되므로, 원인을 찾은 뒤 반드시 실행해야 한다.

### 자동화(`git bisect run`)

버그 재현이 자동화된 테스트 스크립트로 판단 가능하다면, 사람이 매번 `good`/`bad`를 입력하는 대신 스크립트를 연결해 전체 과정을 자동으로 진행할 수 있다.

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run npm test    # 각 커밋마다 npm test를 실행, 종료 코드로 good/bad 자동 판정
```

스크립트의 종료 코드가 0이면 `good`, 0이 아니면(125는 예외로 "판정 불가"를 의미) `bad`로 자동 처리된다. 이 방식은 특정 유닛 테스트 하나가 언제부터 실패하기 시작했는지 찾는 데 특히 유용하며, 사람이 직접 커밋마다 수동으로 확인하는 시간을 절약해준다.

### `--first-parent`로 병합 커밋 건너뛰기

병합 커밋(13장)이 많은 히스토리에서는 병합된 브랜치 내부의 세부 커밋까지 이분 탐색 대상에 포함되면 탐색이 불필요하게 복잡해질 수 있다. `--first-parent` 옵션은 각 병합의 첫 번째 부모만 따라가도록 제한해 이런 경우를 단순화한다.

## 주의사항·함정

**Shallow clone(18장)에서는 bisect가 제한적으로 동작한다**: 이분 탐색은 히스토리 전체 그래프를 필요로 하므로, `--depth`로 잘라낸 shallow 저장소에서는 탐색 범위 안의 커밋이 실제로 존재하지 않아 오류가 나거나 예상과 다르게 동작할 수 있다. bisect가 필요한 저장소라면 전체 히스토리를 가진 clone을 준비하는 편이 안전하다.

**빌드가 실패하는 커밋을 만나면 `good`/`bad` 대신 `skip`을 쓴다**: 탐색 도중 코드가 아예 컴파일되지 않거나 테스트 환경 자체가 갖춰지지 않은 커밋을 만날 수 있다. 이런 커밋은 버그 유무를 판단할 수 없으므로 `git bisect skip`으로 건너뛰면, Git이 그 지점을 피해 다른 커밋으로 탐색을 이어간다.

**탐색 중간에 다른 작업을 하면 결과가 꼬일 수 있다**: `bisect` 세션이 진행 중인 동안에는 detached HEAD 상태로 계속 이동하므로, 이 상태에서 커밋을 만들거나 브랜치를 전환하면 탐색 진행 상황을 잃을 수 있다. 세션이 끝날 때까지는 오직 good/bad 판정에만 집중하고, 끝나면 반드시 `git bisect reset`으로 정리한다.

## Reference

- [Git Tools - Debugging with Git](https://git-scm.com/book/en/v2/Git-Tools-Debugging-with-Git)
- [git-bisect Documentation](https://git-scm.com/docs/git-bisect)
