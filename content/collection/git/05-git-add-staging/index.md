---
draft: false
collection_order: 5
slug: git-add-command-staging-files
title: "[Git] 05. git add — 스테이징"
date: 2026-09-04
lastmod: 2026-09-04
description: "git add로 파일을 스테이징 영역에 등록하는 기본 사용법, 여러 파일·전체 디렉터리를 한 번에 추가하는 옵션, 04장에서 다룬 3단계 모델에서 add가 실제로 무엇을 바꾸는지를 정리한 Git 챕터다."
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
- Index
- Snapshot
- Command-Line
- CLI
- Configuration(설정)
- Advanced
- Career(커리어)
image: "wordcloud.png"
---

`git add .`를 습관처럼 입력하는 사람은 많지만, 그 명령이 정확히 무엇을 스테이징 영역에 넣는지(현재 디렉터리 기준인지, 저장소 전체 기준인지), 그리고 이후 그 파일을 다시 수정하면 스테이징 상태가 어떻게 되는지까지 아는 사람은 드물다. 이 장은 `git add`의 동작 범위와 자주 쓰는 변형을 다룬다.

## 개요

`git add`는 작업 트리의 변경 사항(새 파일, 수정된 파일, 삭제된 파일)을 스테이징 영역으로 옮기는 명령이다. 대상 지정 방식에 따라 범위가 달라진다.

```bash
git add README.md              # 특정 파일 하나만 스테이징
git add src/ tests/             # 지정한 디렉터리 이하 전체
git add .                       # 현재 디렉터리 기준 이하 전체(상위 디렉터리는 제외)
git add -A                      # 저장소 전체(삭제된 파일 포함) — 현재 위치 무관
git add -u                      # 이미 추적 중인 파일의 수정·삭제만(새 파일은 제외)
```

`git add .`와 `git add -A`의 차이가 실무에서 가장 자주 헷갈리는 지점이다. `git add .`는 명령을 실행한 디렉터리를 기준으로 그 하위만 대상으로 삼지만, `git add -A`는 저장소 루트 전체를 대상으로 한다. 저장소의 하위 디렉터리 안에서 `git add .`를 실행했는데 다른 디렉터리의 변경이 스테이징되지 않았다면, 이 범위 차이가 원인이다.

## 기본 개념

`git add`가 실제로 하는 일은 파일 내용을 압축해 Git 객체 저장소(`objects/`)에 blob으로 저장하고, `.git/index` 파일에 그 blob의 해시와 파일 경로를 기록하는 것이다. 즉 `git add`를 실행한 시점에 이미 파일 내용은 저장소 안에 blob 형태로 존재하게 된다(단, 아직 커밋으로 묶이지 않았을 뿐이다). 이 저장 방식은 34장의 Git 객체 모델에서 더 자세히 다룬다.

이 사실에서 실무적으로 중요한 결론이 하나 나온다 — <strong>`git add`한 뒤 파일을 다시 수정하면</strong>, 스테이징 영역에는 add 시점의 내용이 그대로 남아 있고 작업 트리에는 그 이후의 수정 내용이 남는다. 이 상태에서 `git status`를 실행하면 같은 파일이 "스테이징된 변경"과 "스테이징되지 않은 변경" 두 목록에 동시에 나타난다. 커밋하려면 다시 한번 `git add`를 실행해 최신 상태를 스테이징 영역에 반영해야 한다.

## 종류/세부

### 대화형·부분 스테이징 미리보기

파일 하나 안에서 일부 변경만 스테이징하고 싶을 때 쓰는 `-p`(patch) 옵션이 있다. 이 옵션은 파일을 "hunk" 단위로 쪼개 하나씩 스테이징 여부를 물어보는데, 자세한 조작법은 31장에서 다룬다. 여기서는 존재만 짚어둔다.

```bash
git add -p src/app.js
```

### 스테이징 결과 확인

`git add` 직후 무엇이 스테이징됐는지 확인하는 가장 빠른 방법은 `git status`(06장)이며, 스테이징된 내용의 실제 diff까지 보려면 `git diff --staged`(07장)를 쓴다. 두 명령 모두 이후 장에서 이어서 다룬다.

### 실수로 스테이징한 파일 되돌리기

의도치 않게 `git add .`로 큰 빌드 산출물이나 비밀 파일까지 스테이징했다면, 커밋하기 전에 스테이징만 취소할 수 있다.

```bash
git restore --staged path/to/file   # 최신 Git(2.23+)
# 또는
git reset HEAD path/to/file          # 이전 버전과 호환되는 표기
```

이 명령은 스테이징 영역만 되돌릴 뿐 작업 트리의 파일 내용은 그대로 유지한다 — 파일 자체를 지우거나 수정 내용을 버리지 않는다.

## 주의사항·함정

**`.gitignore`에 없는 대용량 파일을 실수로 add하기 쉽다**: 빌드 산출물 디렉터리(`node_modules/`, `dist/` 등)를 `.gitignore`에 등록하지 않은 채 `git add -A`를 실행하면, 수천 개의 불필요한 파일이 스테이징된다. `git status`로 스테이징 결과를 커밋 전에 항상 확인하는 습관이 이 실수를 막는다.

**빈 디렉터리는 add되지 않는다**: Git은 파일만 추적하고 디렉터리 자체는 추적하지 않으므로, 파일이 하나도 없는 빈 디렉터리는 `git add`로도 스테이징되지 않는다. 디렉터리 구조 자체를 저장소에 남기고 싶다면 그 안에 `.gitkeep` 같은 이름의 빈 파일을 관례적으로 하나 만들어 추가한다.

**대소문자만 다른 파일명 변경은 일부 환경에서 인식되지 않을 수 있다**: macOS·Windows의 기본 파일 시스템은 대소문자를 구분하지 않으므로, `File.js`를 `file.js`로 이름만 바꾼 뒤 `git add`해도 변경이 감지되지 않는 경우가 있다. 이 경우 `git mv` 명령이나 두 단계 이름 변경(다른 이름으로 먼저 바꿨다가 원하는 이름으로 다시 바꾸는 방법)이 필요할 수 있다.

## Reference

- [git-add Documentation](https://git-scm.com/docs/git-add)
