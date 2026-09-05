---
draft: false
collection_order: 13
slug: git-merge-command-and-conflict-resolution
title: "[Git] 13. git merge — 병합과 충돌 해결"
date: 2026-09-04
lastmod: 2026-09-04
description: "git merge가 두 브랜치의 히스토리를 하나로 합치는 기본 사용법, 병합 충돌이 발생하는 조건과 <<<<<<< 마커를 읽고 해결하는 절차, 병합 커밋의 구조를 정리한 Git 챕터다."
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
- Code-Review(코드리뷰)
- Open-Source(오픈소스)
- Career(커리어)
image: "wordcloud.png"
---

`git merge`를 실행했다가 처음 보는 `<<<<<<<`, `=======`, `>>>>>>>` 마커로 뒤덮인 파일을 마주치면 당황하기 쉽다. 하지만 이 마커는 Git이 스스로 판단하지 못한 부분을 사람에게 넘겨주는 명확한 신호일 뿐이며, 구조를 알면 침착하게 해결할 수 있다. 이 장은 병합이 성공하는 경우와 충돌하는 경우를 나눠 다룬다.

## 개요

`git merge`는 현재 브랜치에 다른 브랜치의 변경 사항을 합친다.

```bash
git switch main
git merge feature/login
```

이 명령은 `main` 브랜치에 `feature/login` 브랜치의 커밋들을 반영한다. 두 브랜치가 겹치는 부분 없이 수정됐다면 Git은 자동으로 병합을 완료하고 새로운 병합 커밋을 만든다(겹치지 않는 경우 중에서도 한 브랜치가 다른 브랜치의 조상일 때는 14장에서 다루는 fast-forward가 일어나 병합 커밋조차 생기지 않는다).

## 기본 개념

병합 충돌(merge conflict)은 두 브랜치가 <strong>같은 파일의 같은 부분</strong>을 서로 다르게 수정했을 때 발생한다. Git은 자동으로 어느 쪽 변경을 채택해야 할지 판단할 수 없으므로, 해당 부분을 충돌 마커로 감싸 파일에 남기고 병합을 일시 중단한다.

```
<<<<<<< HEAD
현재 브랜치(main)의 내용
=======
병합하려는 브랜치(feature/login)의 내용
>>>>>>> feature/login
```

`<<<<<<< HEAD`부터 `=======`까지가 현재 브랜치의 내용, `=======`부터 `>>>>>>> feature/login`까지가 병합해오는 브랜치의 내용이다. 해결 절차는 이 마커들을 지우고 최종적으로 남길 내용만 남긴 뒤, 그 파일을 다시 스테이징(05장)하고 커밋하는 것이다.

```bash
# 충돌 마커를 직접 편집해 해결한 뒤
git add conflicted-file.js
git commit          # 메시지는 보통 자동으로 "Merge branch 'feature/login'"로 채워짐
```

## 종류/세부

### 충돌 상태에서 쓰는 도구

충돌이 여러 파일에 걸쳐 있을 때 상황을 파악하는 데 쓰는 명령들이다.

```bash
git status                     # 어느 파일이 충돌 상태인지(both modified) 표시
git diff                       # 충돌 마커가 포함된 상태의 diff 확인
git merge --abort               # 병합 자체를 취소하고 병합 시작 전 상태로 완전히 되돌림
```

`--abort`는 충돌 해결이 너무 복잡해 보이거나 애초에 병합을 잘못 시작했다고 판단될 때 유용하다 — 병합 시도 이전 상태로 정확히 되돌아가므로, 처음부터 다시 계획을 세워 시도할 수 있다.

### 병합 커밋의 구조

일반 커밋(08장)은 부모 커밋이 하나지만, 병합 커밋은 부모가 둘(또는 그 이상, octopus merge의 경우)이다. `git log --graph`(09장)에서 봤던 갈라졌다 합쳐지는 그래프 모양이 바로 이 다중 부모 구조에서 나온다.

```bash
git log --oneline --graph -3
```

```
*   e5f6a7b (HEAD -> main) Merge branch 'feature/login'
|\
| * 9f8e7d6 (feature/login) 로그인 기능 구현
* | 3f2a1c9 main에서의 다른 수정
|/
```

### 병합 전략 옵션

특정 파일에서 항상 한쪽 브랜치의 내용을 우선하고 싶을 때 전략 옵션을 쓸 수 있다.

```bash
git merge -X ours feature/login    # 충돌 시 현재 브랜치(main) 내용을 우선
git merge -X theirs feature/login  # 충돌 시 병합해오는 브랜치 내용을 우선
```

이 옵션은 충돌이 발생한 hunk에만 적용되며, 병합해오는 브랜치의 다른 변경 사항 자체를 무시하는 것은 아니다.

## 주의사항·함정

**충돌 마커를 지우지 않고 그대로 커밋하는 실수**: 충돌 해결 중 `<<<<<<<`, `=======`, `>>>>>>>` 마커 중 일부를 실수로 남긴 채 커밋하면, 그 마커가 코드의 일부로 그대로 포함돼 문법 오류나 예상치 못한 동작을 일으킨다. 커밋 전에 파일 전체에서 마커 문자열이 남아 있지 않은지 검색하는 습관이 필요하다.

**병합 커밋이 히스토리를 지저분하게 만든다는 불만**: 짧은 수명의 기능 브랜치를 자주 병합하면 `git log --graph` 출력에 병합 커밋이 많이 쌓여 읽기 번거로워질 수 있다. 이 불만에 대한 대안이 16장에서 다루는 리베이스 기반 워크플로다 — 다만 리베이스는 병합과 다른 트레이드오프를 가지므로, 어느 쪽이 항상 옳다고 단정할 수 없다.

**같은 두 브랜치를 실수로 여러 번 병합하는 경우**: 이미 병합된 브랜치를 다시 병합하려 하면, Git은 변경 사항이 없다는 것을 인식하고 "Already up to date"를 출력하며 아무 일도 하지 않는다. 이는 오류가 아니라 정상 동작이다.

## Reference

- [Git Branching - Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [git-merge Documentation](https://git-scm.com/docs/git-merge)
