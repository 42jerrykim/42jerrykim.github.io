---
draft: false
collection_order: 25
slug: git-restore-checkout-file-discard-changes
title: "[Git] 25. git restore와 git checkout -- <file>"
date: 2026-09-04
lastmod: 2026-09-04
description: "작업 트리의 파일 변경을 되돌리는 git restore와 오래된 git checkout -- <file> 표기, --source로 임의 커밋의 특정 파일만 되돌리는 법, 되돌린 변경이 복구 불가능한 이유를 정리한 Git 챕터다."
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
- Open-Source(오픈소스)
- Career(커리어)
- File-System(파일시스템)
- Diagnostics(진단)
image: "wordcloud.png"
---

브랜치 전체가 아니라 파일 하나만 "방금 수정한 내용을 취소하고 싶다"는 요구는 실무에서 매우 자주 생긴다. 12장에서 이미 `checkout -- <file>`과 `restore`의 관계를 짧게 언급했는데, 이 장은 그 되돌리기 동작 자체를 정면으로 다룬다.

## 개요

Git 2.23 이상에서는 파일 내용 복원 전용 명령이 분리되어 있다.

```bash
git restore README.md          # 작업 트리의 변경을 마지막 커밋(HEAD) 상태로 되돌림
git checkout -- README.md      # 위와 동일한 동작(오래된 표기)
```

두 명령 모두 스테이징되지 않은(unstaged, 04장) 작업 트리 변경만 대상으로 한다. 스테이징까지 된 변경을 되돌리려면 05장에서 다룬 `--staged` 옵션이 필요하다.

## 기본 개념

`git restore`가 존재하는 이유는 12장에서 다룬 `git checkout`의 중의성 문제와 같다 — 예전에는 "파일을 되돌린다"와 "브랜치를 바꾼다"는 서로 다른 두 개념을 같은 명령이 인자 형태로만 구분해 처리했다. `git restore`는 오직 파일 복원만 담당하도록 의도가 명확한 이름으로 새로 만들어졌다.

`git restore`가 다루는 두 영역은 옵션으로 구분한다.

| 명령 | 대상 | 결과 |
|---|---|---|
| `git restore <file>` | 작업 트리 | 파일 내용을 스테이징 영역(비어 있으면 HEAD) 상태로 되돌림 |
| `git restore --staged <file>` | 스테이징 영역 | 스테이징만 취소(05장에서 이미 다룬 내용), 작업 트리는 그대로 |
| `git restore --staged --worktree <file>` | 둘 다 | 스테이징도 취소하고 작업 트리도 마지막 커밋 상태로 되돌림 |

## 종류/세부

### 임의의 커밋에서 파일 복원하기(`--source`)

방금 커밋한 상태가 아니라, 훨씬 이전 커밋에 있던 특정 파일의 버전을 지금 작업 트리로 가져오고 싶을 때가 있다.

```bash
git restore --source a1b2c3d README.md
```

이 명령은 `a1b2c3d` 커밋 시점의 `README.md` 내용으로 지금 작업 트리의 해당 파일만 덮어쓴다. 다른 파일이나 커밋 히스토리 자체에는 영향을 주지 않으므로, "이 파일만 예전 버전으로 되돌리고 싶다"는 상황에 정확히 맞는 도구다.

```bash
git restore --source HEAD~3 -- config.json    # 3개 커밋 전 config.json 버전으로
```

### 전체 파일을 되돌리기(디렉터리 지정)

여러 파일을 한 번에 되돌리고 싶다면 경로에 디렉터리나 `.`을 지정한다.

```bash
git restore .              # 현재 디렉터리 이하 모든 파일의 변경을 되돌림
git restore src/           # src/ 디렉터리 이하만
```

이 명령은 05장에서 다룬 `git add .`의 범위 규칙과 동일하게 동작한다 — 명령을 실행한 위치를 기준으로 한다.

## 주의사항·함정

**되돌린 작업 트리 변경은 복구할 수 없다**: `git restore`(스테이징되지 않은 변경 대상)는 04장에서 설명했듯 아직 Git 객체로 저장된 적이 없는 내용을 되돌린다. 즉 이 명령이 지우는 내용은 애초에 저장소 어디에도 백업되어 있지 않으므로, 23장의 `reset --hard`나 28장의 `reflog`로도 복구할 수 없다. 실행 전 정말로 이 변경을 버려도 되는지 반드시 확인해야 한다.

**`--staged` 여부를 헷갈리면 의도와 다른 영역이 되돌아간다**: "스테이징까지 했는데 취소하고 싶다"면서 `--staged` 없이 `git restore <file>`만 실행하면, 스테이징 영역이 아니라 작업 트리만 되돌아가고 스테이징된 내용은 그대로 남는다. 04장의 3단계 모델을 다시 떠올리며 어느 영역을 되돌리고 싶은지 먼저 명확히 하는 편이 실수를 줄인다.

**오래된 자료의 `checkout -- <file>` 표기를 무조건 최신 방식으로 바꿔 쓸 필요는 없다**: 두 표기는 동일하게 동작하므로, 기존 스크립트나 문서에 있는 `checkout --` 표기를 굳이 찾아 바꿀 필요는 없다. 다만 새로 작성하는 스크립트나 문서라면 의도가 더 명확한 `restore`를 쓰는 편이 나중에 읽는 사람의 혼란을 줄인다.

## Reference

- [git-restore Documentation](https://git-scm.com/docs/git-restore)
- [git-checkout Documentation](https://git-scm.com/docs/git-checkout)
