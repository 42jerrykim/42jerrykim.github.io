---
draft: false
collection_order: 9
slug: git-log-command-view-history
title: "[Git] 09. git log — 히스토리 조회"
date: 2026-09-04
lastmod: 2026-09-04
description: "git log의 기본 출력을 읽는 법, --oneline·--graph·--stat 같은 자주 쓰는 조합, 작성자·날짜·경로로 히스토리를 필터링하는 방법을 정리한 Git 챕터다."
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
- Configuration(설정)
image: "wordcloud.png"
---

`git log`는 옵션 없이 실행하면 커밋마다 해시·작성자·날짜·메시지 전체를 세로로 길게 나열해, 몇십 개만 넘어가도 전체 흐름을 파악하기 어렵다. 실무에서는 대부분 몇 가지 옵션 조합을 alias로 등록해두고 쓴다. 이 장은 그 조합들이 각각 무엇을 보여주는지 정리한다.

## 개요

기본 출력은 커밋 하나당 4~5줄을 차지한다.

```bash
git log
```

```
commit 3f2a1c9e8b7d6a5c4b3a2f1e0d9c8b7a6f5e4d3c
Author: Jerry Kim <user@example.com>
Date:   Fri Sep 4 10:00:00 2026 +0900

    커밋 제목

    커밋 본문
```

가장 자주 쓰이는 축약 조합은 한 커밋을 한 줄로 보여주는 `--oneline`이다.

```bash
git log --oneline
```

```
3f2a1c9 커밋 제목
a1b2c3d 이전 커밋
```

## 기본 개념

`git log`가 보여주는 목록은 08장에서 다룬 커밋 객체의 그래프를 현재 브랜치의 HEAD에서부터 부모 방향으로 따라간 결과다. 커밋마다 부모 커밋 해시를 저장하고 있으므로(08장), `git log`는 이 부모 포인터를 계속 따라가며 히스토리를 나열한다 — 브랜치가 갈라졌다 합쳐진 적이 있다면 이 그래프는 단순한 직선이 아니라 여러 갈래가 합류하는 구조가 된다. 이 분기·병합 구조를 시각적으로 보려면 `--graph` 옵션이 필요하다.

```bash
git log --oneline --graph --all
```

```
*   a1b2c3d (HEAD -> main) Merge branch 'feature'
|\
| * 9f8e7d6 (feature) 기능 구현
* | 3f2a1c9 다른 수정
|/
* 0d1e2f3 공통 조상 커밋
```

`--all`은 현재 체크아웃된 브랜치뿐 아니라 저장소에 있는 모든 브랜치의 히스토리를 함께 그린다. 이 조합은 실무에서 `git config --global alias.lg "log --oneline --graph --all"`처럼 alias(02장)로 등록해두고 습관적으로 쓰는 경우가 많다.

## 종류/세부

### 자주 쓰는 필터

특정 조건에 맞는 커밋만 골라 보고 싶을 때 쓰는 옵션들이다.

| 옵션 | 필터 대상 |
|---|---|
| `--author="이름"` | 특정 작성자의 커밋만 |
| `--since="2 weeks ago"` / `--until="..."` | 날짜 범위 |
| `-- path/to/file` | 특정 파일·디렉터리의 변경 이력만 |
| `--grep="키워드"` | 커밋 메시지에 특정 단어가 포함된 것만 |
| `-p` | 각 커밋의 diff(07장 형식)까지 함께 표시 |
| `--stat` | 커밋별 변경 파일·줄 수 요약 |

```bash
git log --author="Jerry" --since="1 week ago" --oneline
git log --oneline -- src/app.js
```

### 특정 파일의 변경 이력 추적

파일 경로를 지정한 `git log`는 그 파일에 영향을 준 커밋만 걸러 보여준다. 파일이 이름 변경(rename)을 거쳤다면 `--follow` 옵션을 추가해야 이름 변경 이전의 이력까지 이어서 추적한다.

```bash
git log --follow --oneline -- src/renamed-file.js
```

이 명령은 32장에서 다루는 `git blame`(파일의 각 줄이 누구의 어느 커밋에서 왔는지)과 함께 코드 고고학(code archaeology)의 기본 도구로 쓰인다.

## 주의사항·함정

**`--all` 없이는 다른 브랜치의 커밋이 보이지 않는다**: `git log`는 기본적으로 현재 체크아웃된 브랜치의 히스토리만 보여준다. 다른 브랜치에서 작업한 커밋이 갑자기 안 보인다고 당황하기 전에, 지금 어느 브랜치에 있는지(`git status`, 06장)와 `--all` 옵션 여부를 먼저 확인한다.

**로컬 히스토리는 원격 저장소의 최신 상태를 실시간 반영하지 않는다**: `git log`가 보여주는 원격 브랜치 관련 정보(`origin/main` 등)는 마지막으로 `git fetch`(19장)한 시점의 스냅샷이다. 다른 사람이 방금 push한 커밋은 fetch하기 전까지 보이지 않는다.

**대화형 페이저 때문에 스크립트에서 예상과 다르게 동작할 수 있다**: 터미널에서 `git log`를 실행하면 결과가 길 경우 `less` 같은 페이저로 넘어가 스크롤 대기 상태가 된다. 스크립트나 CI 환경에서 이 동작이 걸림돌이 된다면 `--no-pager` 전역 옵션이나 `git --no-pager log`로 페이저를 끈다.

## Reference

- [git-log Documentation](https://git-scm.com/docs/git-log)
