---
draft: false
collection_order: 26
slug: git-cherry-pick-command
title: "[Git] 26. git cherry-pick"
date: 2026-09-04
lastmod: 2026-09-04
description: "git cherry-pick이 다른 브랜치의 특정 커밋 하나만 골라 현재 브랜치에 재적용하는 원리, 핫픽스를 여러 릴리스 브랜치에 반영하는 대표 시나리오, 충돌 해결 절차와 커밋 해시가 바뀌는 이유를 정리한 Git 챕터다."
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
- CI-CD(Continuous Integration/Continuous Deployment)
image: "wordcloud.png"
---

브랜치 전체를 병합하고 싶은 것이 아니라, 다른 브랜치에 있는 커밋 하나만 정확히 골라 가져오고 싶을 때가 있다. 대표적으로 운영 환경에 긴급히 배포된 버그 수정을, 아직 병합되지 않은 다음 릴리스 브랜치에도 똑같이 반영해야 하는 상황이다. `git cherry-pick`이 이 용도로 만들어진 명령이다.

## 개요

```bash
git switch release/2.0
git cherry-pick a1b2c3d    # a1b2c3d 커밋의 변경 내용만 현재 브랜치에 재적용
```

이 명령은 지정한 커밋이 만든 변경(diff)을 계산해, 현재 브랜치의 최신 커밋 위에 그 변경만 새 커밋으로 다시 적용한다. 원본 커밋이 있던 브랜치나 원본 커밋 자체는 전혀 건드리지 않는다.

## 기본 개념

`cherry-pick`의 동작 원리는 15장에서 다룬 리베이스가 각 커밋에 대해 하는 일과 사실상 같다 — 커밋의 diff를 뽑아 다른 위치에 재적용하고, 그 결과를 새로운 해시를 가진 커밋으로 기록한다. 차이는 범위다. 리베이스는 브랜치 전체의 여러 커밋을 통째로 옮기지만, cherry-pick은 지정한 커밋 하나(또는 몇 개)만 선택적으로 가져온다.

이 사실에서 중요한 결론이 나온다 — cherry-pick으로 가져온 커밋은 원본과 diff 내용은 같아도 <strong>해시가 다른 별개의 커밋</strong>이다. 나중에 두 브랜치를 병합(13장)하게 되면, Git은 이 둘을 서로 다른 커밋으로 인식하면서도 실제 diff가 같다는 것을 보고 대개 충돌 없이 처리하지만, 상황에 따라 "이미 반영된 변경을 또 반영하려 한다"는 혼란스러운 충돌이 나타날 수도 있다.

## 종류/세부

### 대표 시나리오 — 핫픽스를 여러 브랜치에 반영

운영 중인 서비스에 긴급 버그가 발견되어 `main`에서 바로 수정하고 배포했는데, 아직 병합되지 않은 `release/2.0` 브랜치에도 같은 수정이 필요한 상황을 생각해보자.

```bash
git switch main
git commit -am "긴급: 로그인 실패 버그 수정"    # main에서 바로 수정·커밋
git push origin main                              # 즉시 배포

git switch release/2.0
git cherry-pick <위 커밋의 해시>                  # release/2.0에도 같은 수정 반영
git push origin release/2.0
```

이런 패턴은 여러 버전을 동시에 유지보수하는 프로젝트(00장에서 언급한 Git Flow 계열 전략을 쓰는 경우)에서 특히 자주 나타난다.

### 여러 커밋을 범위로 지정

```bash
git cherry-pick a1b2c3d^..d4e5f6g    # a1b2c3d부터 d4e5f6g까지 여러 커밋을 순서대로 재적용
git cherry-pick --no-commit a1b2c3d   # 재적용만 하고 커밋은 나중에(-n, 24장의 revert와 같은 옵션)
```

범위 지정 시 시작 커밋에 `^`를 붙이는 이유는 Git의 범위 표기(`A..B`)가 기본적으로 A는 제외하고 B까지 포함하기 때문이다 — `a1b2c3d`부터 포함시키려면 그 부모(`a1b2c3d^`)부터 범위를 잡아야 한다.

### 충돌 해결

cherry-pick도 리베이스·병합과 마찬가지로 충돌이 날 수 있으며, 절차도 동일하다.

```bash
# 충돌 마커(13장 참고)를 해결한 뒤
git add resolved-file.js
git cherry-pick --continue
# 또는 그만두려면
git cherry-pick --abort
```

## 주의사항·함정

**cherry-pick을 반복해 브랜치 전체를 옮기려 하지 않는다**: 특정 커밋 몇 개가 아니라 브랜치의 커밋 대부분을 옮기고 싶다면, cherry-pick을 여러 번 반복하기보다 15장의 리베이스나 13장의 병합이 적절한 도구다. cherry-pick은 소수의 특정 커밋을 골라내는 용도에 최적화되어 있다.

**같은 커밋을 여러 브랜치에 cherry-pick한 뒤 병합하면 혼란스러운 충돌이 날 수 있다**: 위에서 설명했듯 cherry-pick된 커밋은 해시가 다른 별개의 커밋으로 취급된다. 여러 브랜치에 같은 수정을 cherry-pick해 둔 상태에서 그 브랜치들을 나중에 서로 병합하면, Git이 "이미 반영된 것 같은데 커밋 자체는 다르다"는 상황을 만나 예상 밖의 충돌을 낼 수 있다.

**의존 관계가 있는 커밋만 골라 cherry-pick하면 빌드가 깨질 수 있다**: 어떤 커밋이 이전 커밋에서 정의한 함수나 변수에 의존하고 있는데, 그 이전 커밋 없이 해당 커밋만 cherry-pick하면 코드가 컴파일되지 않거나 런타임 오류가 날 수 있다. cherry-pick하려는 커밋이 다른 커밋에 의존하지 않는지 `git show`나 `git log -p`(09장)로 먼저 확인하는 습관이 필요하다.

## Reference

- [git-cherry-pick Documentation](https://git-scm.com/docs/git-cherry-pick)
