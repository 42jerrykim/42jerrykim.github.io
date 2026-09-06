---
draft: false
collection_order: 6
slug: git-status-command-check-working-tree-state
title: "[Git] 06. git status — 상태 확인"
date: 2026-09-04
lastmod: 2026-09-04
description: "git status가 작업 트리·스테이징 영역·저장소 사이의 차이를 어떻게 세 구역으로 나눠 보여주는지, --short 축약 표기, 브랜치 추적 정보까지 읽는 법을 정리한 Git 챕터다."
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
- Configuration(설정)
- Advanced
- Career(커리어)
- Open-Source(오픈소스)
image: "wordcloud.png"
---

`git status`는 Git을 쓰는 동안 가장 많이 입력하게 되는 명령이지만, 출력 화면을 "빨간 글씨는 나쁜 것, 초록 글씨는 좋은 것" 정도로만 이해하고 넘어가는 경우가 많다. 이 장은 그 출력이 실제로 04장의 3단계 모델 중 어느 부분을 비교한 결과인지 구역별로 뜯어본다.

## 개요

`git status`는 옵션 없이 실행하면 세 가지 정보를 순서대로 보여준다: 현재 브랜치와 원격 브랜치 대비 앞서거나 뒤처진 커밋 수, 스테이징된 변경(Changes to be committed), 스테이징되지 않은 변경(Changes not staged for commit)과 추적되지 않는 파일(Untracked files).

```bash
git status
```

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   src/app.js

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        notes.txt
```

이 세 구역은 정확히 04장에서 다룬 파일 상태와 대응한다. "Changes to be committed"는 스테이징 영역과 마지막 커밋의 차이, "Changes not staged for commit"은 작업 트리와 스테이징 영역의 차이, "Untracked files"는 한 번도 스테이징된 적 없는 새 파일 목록이다.

## 기본 개념

같은 파일(`src/app.js`)이 만약 add한 뒤 다시 수정됐다면, "Changes to be committed"와 "Changes not staged for commit" 두 구역에 동시에 나타날 수 있다. 이는 오류가 아니라 05장에서 설명한 대로 스테이징 영역의 스냅샷과 작업 트리의 현재 내용이 서로 다른 시점을 가리키기 때문에 생기는 정상적인 표시다. 이 경우 최신 변경까지 커밋에 포함하려면 `git add`를 한 번 더 실행해야 한다.

## 종류/세부

### 축약 출력(`--short`)

기본 출력은 사람이 읽기엔 친절하지만 파일이 많아지면 화면을 많이 차지한다. `-s`(또는 `--short`) 옵션은 같은 정보를 파일당 한 줄로 압축한다.

```bash
git status -s
```

```
 M README.md
M  src/app.js
?? notes.txt
```

두 글자짜리 코드에서 첫 번째 자리는 스테이징 영역 상태, 두 번째 자리는 작업 트리 상태를 가리킨다. `M `(첫 자리 M, 둘째 자리 공백)은 "스테이징됨, 이후 추가 수정 없음"을, ` M`(첫 자리 공백, 둘째 자리 M)은 "스테이징 안 됨"을 의미하며, `MM`처럼 두 자리 모두 표시되면 위에서 설명한 "add 후 재수정" 상태다. `??`는 untracked 파일을 뜻한다.

| 코드 | 의미 |
|---|---|
| ` M` | 작업 트리에서만 수정됨(스테이징 안 됨) |
| `M ` | 스테이징 영역까지 반영됨(추가 수정 없음) |
| `MM` | 스테이징 후 다시 수정됨(두 상태 모두 존재) |
| `A ` | 새 파일이 스테이징됨 |
| `??` | 추적되지 않는 새 파일 |
| `D ` / ` D` | 삭제가 스테이징됨 / 삭제됐지만 스테이징 안 됨 |

### 브랜치 추적 정보만 보기

원격 브랜치 대비 몇 커밋 앞서거나 뒤처졌는지만 빠르게 보고 싶다면 `--branch`(축약 `-b`)를 짧은 출력과 함께 쓴다.

```bash
git status -sb
```

```
## main...origin/main [ahead 2]
 M README.md
```

`[ahead 2]`는 로컬이 원격보다 커밋 2개 앞서 있다는 뜻이며, 아직 `git push`(20장)하지 않은 로컬 커밋이 있다는 신호다.

## 주의사항·함정

**`.gitignore`가 없으면 Untracked files 목록이 순식간에 길어진다**: 빌드 산출물이나 IDE 설정 폴더를 무시 규칙 없이 두면, `git status` 출력이 실제로 중요한 변경을 파악하기 어려울 정도로 길어진다. 10장에서 다루는 `.gitignore` 설정이 이 문제의 정석적인 해결책이다.

**"Your branch is up to date"는 fetch를 최근에 했을 때만 정확하다**: 이 문구는 로컬에 저장된 원격 브랜치 정보(`refs/remotes/origin/main` 등)를 기준으로 판단한 결과이며, 실시간으로 원격 서버에 접속해 확인하는 것이 아니다. 다른 사람이 방금 push한 커밋은 `git fetch`(19장)를 실행하기 전까지 이 판단에 반영되지 않는다.

**대규모 저장소에서 `git status`가 느리게 느껴질 수 있다**: 파일 수가 매우 많은 저장소에서는 작업 트리 전체를 스캔하는 비용 때문에 `git status`가 체감될 만큼 느려질 수 있다. 이런 경우 `core.fsmonitor`, `core.untrackedCache` 같은 설정으로 파일 시스템 변경 감지를 캐싱해 속도를 개선할 수 있으며, 42장의 대용량 저장소 관리에서 다시 다룬다.

## Reference

- [git-status Documentation](https://git-scm.com/docs/git-status)
