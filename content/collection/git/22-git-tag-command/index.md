---
draft: false
collection_order: 22
slug: git-tag-command-release-tagging
title: "[Git] 22. git tag — 릴리스 태깅"
date: 2026-09-04
lastmod: 2026-09-04
description: "git tag로 특정 커밋에 릴리스 버전 같은 영구적인 이름을 붙이는 법, 가벼운 태그와 주석 달린(annotated) 태그의 차이, 태그를 원격에 push하는 별도 절차를 정리한 Git 4부 마무리 챕터다."
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
- CI-CD(Continuous Integration/Continuous Deployment)
- Open-Source(오픈소스)
- Career(커리어)
- Semantic-Versioning(시맨틱버저닝)
- Command-Line
- CLI
- Security(보안)
image: "wordcloud.png"
---

브랜치(11장)가 계속 앞으로 움직이는 포인터라면, 태그는 한 번 특정 커밋을 가리키면 그 자리에 고정되는 이름표다. "v1.0.0을 배포했다"는 사실을 나중에도 정확히 추적하려면, 그 시점의 커밋에 브랜치가 아니라 태그로 이름을 붙여야 한다. 이 장은 태그의 두 종류와 각각의 용도를 다룬다.

## 개요

```bash
git tag v1.0.0                          # 가벼운(lightweight) 태그
git tag -a v1.0.0 -m "1.0.0 정식 릴리스"   # 주석 달린(annotated) 태그
git tag                                  # 전체 태그 목록
git tag -d v1.0.0                        # 태그 삭제
```

기본적으로 태그는 현재 체크아웃된 커밋(HEAD)을 가리키지만, 특정 커밋 해시를 지정해 과거 커밋에 태그를 붙일 수도 있다.

```bash
git tag v0.9.0 a1b2c3d
```

## 기본 개념

가벼운 태그와 주석 달린 태그의 차이는 11장에서 다룬 브랜치와의 비교로 이해하면 명확하다. 가벼운 태그는 브랜치처럼 특정 커밋을 가리키는 참조 파일 하나일 뿐이다. 주석 달린 태그는 그와 달리 Git 객체 저장소에 별도의 태그 객체(34장에서 다룰 객체 모델의 네 번째 유형)를 만들어, 태그를 만든 사람, 날짜, 메시지, 그리고 필요하면 GPG 서명(43장)까지 저장한다.

| 구분 | 가벼운 태그(lightweight) | 주석 달린 태그(annotated) |
|---|---|---|
| 생성 명령 | `git tag <이름>` | `git tag -a <이름> -m "메시지"` |
| 저장 방식 | 커밋을 직접 가리키는 참조 | 별도의 태그 객체를 거쳐 커밋을 가리킴 |
| 작성자·날짜·메시지 | 없음 | 있음 |
| GPG 서명 가능 여부 | 불가능 | 가능 |
| 적합한 용도 | 개인적인 임시 마킹 | 공개 릴리스(대부분의 프로젝트가 권장) |

## 종류/세부

### 태그를 원격에 push하기

17-20장에서 다룬 `git push`는 기본적으로 커밋만 전송하고 태그는 전송하지 않는다. 태그를 원격에 공유하려면 명시적으로 지정해야 한다.

```bash
git push origin v1.0.0        # 태그 하나만 push
git push origin --tags         # 아직 원격에 없는 모든 태그를 한 번에 push
```

이 별도 절차 때문에 "로컬에서는 태그가 보이는데 GitHub 릴리스 페이지에는 안 보인다"는 혼란이 자주 생긴다 — 태그를 만든 뒤 push를 잊었을 가능성이 크다.

### 시맨틱 버저닝과 태그 이름 관례

대부분의 프로젝트는 태그 이름에 시맨틱 버저닝(Semantic Versioning, `MAJOR.MINOR.PATCH` 형식)을 따르고, 앞에 `v`를 붙이는 관례(`v1.2.3`)를 쓴다. 이 관례 자체는 Git이 강제하지 않지만, GitHub의 릴리스 기능이나 여러 패키지 관리자(npm 등)가 이 형식을 전제로 자동화를 구성하는 경우가 많아 사실상 표준처럼 자리 잡았다.

### 특정 태그로 되돌아가기

특정 릴리스 시점의 코드를 확인하고 싶다면 태그로 detached HEAD(12장) 상태에 진입한다.

```bash
git switch --detach v1.0.0
```

이 시점에서 버그를 재현하거나 코드를 확인한 뒤, 계속 작업할 필요가 없다면 다시 원래 브랜치로 전환하면 된다.

## 주의사항·함정

**같은 이름의 태그를 다시 만들면 오류가 난다**: 태그는 한 번 만들어지면 그 이름이 가리키는 커밋이 고정되는 것이 관례이므로, 이미 존재하는 태그 이름으로 다시 `git tag`를 실행하면 Git이 거부한다. 실수로 잘못된 커밋에 태그를 붙였다면 `-f`(force) 옵션으로 덮어쓸 수 있지만, 이미 그 태그를 push해 다른 사람이 참조하고 있다면 20장의 강제 push와 같은 위험이 따른다.

**가벼운 태그로 릴리스를 관리하면 나중에 누가 언제 태그를 붙였는지 알 수 없다**: 프로젝트 초기에는 편해 보여도, 나중에 "이 릴리스 태그는 누가 무슨 근거로 붙였는가"를 확인해야 할 때 주석 정보가 없으면 곤란하다. 공개 릴리스에는 처음부터 주석 달린 태그를 쓰는 습관이 낫다.

**`--tags`로 한 번에 push하면 의도치 않은 태그까지 함께 올라갈 수 있다**: 로컬에서 실험적으로 만들어두고 아직 공개하고 싶지 않은 태그가 있다면, `--tags`로 전체를 push하기 전에 `git tag` 목록을 먼저 확인하는 것이 안전하다.

## Reference

- [Git Basics - Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
- [git-tag Documentation](https://git-scm.com/docs/git-tag)
