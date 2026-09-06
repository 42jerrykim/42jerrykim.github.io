---
draft: false
collection_order: 42
slug: large-repository-management-shallow-clone-filter-repo
title: "[Git] 42. 대용량 저장소 관리 — shallow clone과 filter-repo"
date: 2026-09-04
lastmod: 2026-09-04
description: "18장에서 다룬 shallow clone을 CI 환경에서 실전 활용하는 법, 실수로 커밋된 민감 정보·대용량 파일을 히스토리 전체에서 제거하는 git filter-repo 절차, 36장의 gc·41장의 LFS와 연결되는 저장소 크기 관리 전략을 정리한 Git 9부 첫 챕터다."
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
- Security(보안)
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
- Command-Line
- CLI
image: "wordcloud.png"
---

프로젝트가 몇 년간 이어지면 커밋 수가 수만 개에 이르고, 한때 실수로 커밋됐다가 지금은 삭제된 대용량 파일이나 민감 정보가 여전히 히스토리 어딘가에 남아 있을 수 있다. 9부의 첫 챕터인 이 장은 저장소 자체의 크기와 clone 속도를 관리하는 실전 기법을 다룬다.

## 개요

저장소가 커지는 문제에 대한 접근은 크게 두 갈래다 — <strong>필요한 만큼만 내려받기</strong>(shallow clone, 18장에서 이미 다뤘다)와 <strong>불필요한 과거 내용을 히스토리에서 완전히 제거하기</strong>(filter-repo)다.

```bash
git clone --depth 1 https://github.com/org/large-repo.git    # 18장 복습: 최신 커밋만
git filter-repo --path secrets.env --invert-paths              # 히스토리 전체에서 특정 파일 제거
```

## 기본 개념

18장에서 shallow clone을 "CI 빌드처럼 최신 코드만 필요할 때" 쓰는 방법으로 소개했다. 이 장에서는 그 실전 활용을 좀 더 구체적으로 살펴본다 — CI 파이프라인은 대개 매번 새로운 임시 환경에서 저장소를 새로 clone하므로, 과거 히스토리를 보존할 필요가 없다. 이런 환경에서 `--depth 1`은 clone 시간을 크게 줄이는 가장 직접적인 방법이다.

반면 히스토리 자체에서 무언가를 완전히 지워야 하는 상황(민감 정보 유출, 실수로 커밋된 대용량 바이너리)은 shallow clone으로 해결되지 않는다 — 이미 존재하는 저장소의 과거 커밋을 <strong>재작성</strong>해야 하며, 이는 15장·20장에서 다룬 리베이스·강제 push의 위험이 극대화된 형태다.

## 종류/세부

### git filter-repo로 히스토리에서 파일 제거하기

`git filter-repo`는 Git 프로젝트가 공식적으로 권장하는 히스토리 재작성 도구로, 예전에 널리 쓰이던 `git filter-branch`보다 빠르고 안전하다(`filter-branch`는 Git 자체 문서에서도 더 이상 권장하지 않는다).

```bash
git filter-repo --path secrets.env --invert-paths
```

이 명령은 저장소의 <strong>모든 커밋</strong>을 순회하며 `secrets.env` 파일에 대한 모든 흔적을 제거하고, 그 결과로 모든 커밋의 해시가 바뀐 완전히 새로운 히스토리를 만든다. `--invert-paths`는 "지정한 경로만 남기기"가 아니라 "지정한 경로를 제외한 나머지를 남기기"로 조건을 반전시키는 옵션이다.

### 민감 정보 제거 후 절차

파일 하나를 지우는 것으로 끝나지 않는다. 히스토리를 재작성한 뒤에는 다음 절차가 모두 필요하다.

1. `filter-repo`로 로컬 히스토리 재작성
2. 노출됐던 민감 정보(비밀번호, API 키 등) 자체를 즉시 폐기·재발급 — 히스토리에서 지웠다고 이미 유출된 값이 안전해지는 것은 아니다
3. 모든 원격 저장소에 강제 push(20장의 위험이 그대로 적용됨)
4. 이 저장소를 clone해둔 모든 협업자에게 통보 — 각자 로컬 저장소를 새로 clone하거나 신중하게 재작성된 히스토리로 맞춰야 함
5. 36장에서 다룬 `git gc --prune=now`로 이전 객체를 실제로 디스크에서 제거(원격 서버 쪽도 별도 정리가 필요할 수 있음)

### 대용량 파일을 찾아내기

무엇이 저장소를 부풀리고 있는지 모른다면, 먼저 큰 객체를 식별하는 단계가 필요하다.

```bash
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sort -k3 -n -r | head -10
```

이 명령 조합은 34장에서 다룬 객체 모델을 활용해, 저장소 전체 객체 중 크기가 큰 순서로 상위 목록을 뽑아낸다. 이렇게 찾은 대용량 파일이 여전히 필요하다면 41장의 Git LFS로 옮기는 것이 정답이고, 더 이상 필요 없다면 `filter-repo`로 히스토리에서 제거하는 것이 정답이다.

## 주의사항·함정

**filter-repo는 15장·20장의 위험을 훨씬 큰 규모로 만든다**: 리베이스가 몇 개 커밋의 해시를 바꾸는 것이라면, `filter-repo`는 저장소의 <strong>모든</strong> 커밋 해시를 바꾼다. 이 작업 전에는 반드시 저장소를 별도로 백업하고, 팀 전체가 작업을 멈추는 시점을 조율해야 한다.

**민감 정보는 히스토리 삭제만으로 안전해지지 않는다**: 위 절차에서 강조했듯, 이미 공개 저장소에 노출됐던 비밀번호나 토큰은 filter-repo로 히스토리에서 지워도 이미 그 값을 본 사람이나 크롤러가 있을 수 있다. 유일하게 확실한 대응은 그 값 자체를 폐기하고 새 값으로 교체하는 것이다.

**shallow clone 상태에서 filter-repo 같은 작업을 시도하면 예상과 다르게 동작한다**: 히스토리 재작성 도구는 전체 히스토리를 전제로 동작하므로, shallow 저장소(18장)에서는 먼저 `git fetch --unshallow`로 전체 히스토리를 받아온 뒤 작업해야 한다.

## Reference

- [git-filter-repo (GitHub)](https://github.com/newren/git-filter-repo)
- [gitrevisions Documentation - shallow](https://git-scm.com/docs/shallow)
