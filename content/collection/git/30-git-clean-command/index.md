---
draft: false
collection_order: 30
slug: git-clean-command-remove-untracked-files
title: "[Git] 30. git clean — 미추적 파일 정리"
date: 2026-09-04
lastmod: 2026-09-04
description: "git clean이 .gitignore로도 걸러지지 않는 미추적 파일을 일괄 삭제하는 원리, 되돌릴 수 없는 삭제를 실행하기 전 -n(dry-run)으로 미리 확인해야 하는 이유, -d와 -x 옵션의 범위 차이를 정리한 Git 챕터다."
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
- File-System(파일시스템)
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
- Diagnostics(진단)
image: "wordcloud.png"
---

빌드 산출물이나 임시 파일이 작업 디렉터리에 잔뜩 쌓여 `git status`(06장)의 untracked 목록이 지저분해졌을 때, 파일을 하나씩 손으로 지우는 대신 한 번에 정리하는 명령이 `git clean`이다. 다만 이 명령은 Git 명령 중에서도 특히 위험한 축에 속한다 — 삭제된 파일은 23장의 `reset --hard`와 마찬가지로 복구할 방법이 사실상 없다.

## 개요

```bash
git clean -n     # dry-run: 무엇이 삭제될지 미리보기만(실제로 지우지 않음)
git clean -f      # 실제 삭제 실행(force, 기본 설정에서는 이 플래그가 필수)
```

`git clean`은 25장의 `git restore`, 23장의 `git reset`과 성격이 다르다는 점을 분명히 해야 한다 — 그 명령들은 <strong>Git이 추적 중인 파일</strong>의 내용을 되돌리지만, `git clean`은 <strong>애초에 한 번도 커밋된 적 없는 파일 자체</strong>를 디스크에서 지운다. 즉 Git 객체 저장소 어디에도 그 내용이 백업되어 있지 않다.

## 기본 개념

`-n`(dry-run) 없이 `-f` 옵션만으로 곧바로 `git clean -f`를 실행하는 습관은 위험하다. 이 명령이 지우는 대상은 04장에서 다룬 untracked 상태의 파일이며, `.gitignore`(10장)에 등록됐든 아니든 기본적으로는 무시 파일을 제외한 untracked 파일이 대상이 된다. 실행 전 반드시 `-n`으로 삭제 대상 목록을 확인하는 것이 이 명령을 안전하게 쓰는 유일한 방법이다.

```bash
git clean -n
```

```
Would remove notes.txt
Would remove temp/debug.log
```

이 출력을 확인한 뒤에만 `-f`로 바꿔 실제 삭제를 실행한다.

## 종류/세부

### 자주 쓰는 옵션 조합

| 옵션 | 대상 범위 |
|---|---|
| `git clean -f` | untracked 파일(기본, `.gitignore`로 무시된 파일은 제외) |
| `git clean -fd` | untracked 파일 + untracked 디렉터리까지 |
| `git clean -fx` | `.gitignore`로 무시된 파일까지 포함(빌드 산출물 등) |
| `git clean -fdx` | 위 전부(사실상 저장소를 "방금 clone한 것과 같은 상태"로) |

`-d`가 없으면 빈 디렉터리나 untracked 파일만 든 디렉터리가 삭제 대상에서 빠질 수 있다. `-x`는 `.gitignore`가 존재하는 이유(10장)를 생각하면 신중하게 써야 한다 — 의도적으로 무시해둔 빌드 산출물, IDE 설정, 로컬 환경 파일까지 한 번에 지워질 수 있기 때문이다.

### 특정 경로만 정리하기

전체가 아니라 특정 디렉터리만 대상으로 좁힐 수도 있다.

```bash
git clean -fd build/    # build/ 디렉터리 안의 untracked 파일·디렉터리만 정리
```

### 대화형 모드

무엇을 지울지 하나씩 확인하며 진행하고 싶다면 대화형 모드를 쓴다.

```bash
git clean -i
```

이 모드는 05장에서 다룬 `git add -p`의 신중함과 비슷한 접근으로, 전체를 한 번에 지우는 대신 항목별로 선택할 수 있어 `-n`과 `-f`의 중간 정도 안전성을 제공한다.

## 주의사항·함정

**`-n` 없이 `-fdx`를 습관적으로 실행하는 것은 매우 위험하다**: 이 조합은 `.gitignore`로 무시된 파일까지 포함해 저장소 내 모든 untracked 항목을 지운다. 개인 설정 파일, 아직 커밋하지 않은 실험적 파일, `.env` 같은 환경 설정까지 한 번에 사라질 수 있으므로, 반드시 `-n`으로 먼저 확인하는 습관을 들인다.

**`.gitignore`에 등록된 파일이 사라지는 것은 clean의 정상 동작이다**: `-x` 옵션을 켰을 때 사라지는 파일은 버그가 아니라 옵션이 의도한 대로 동작한 것이다. `.gitignore`에 등록된 파일 중 다시 만들기 번거로운 것(예: 로컬 전용 설정 파일)이 있다면, `-x`를 쓰기 전에 그 파일들을 별도로 백업해두거나 애초에 `-x` 없이 실행한다.

**서브모듈(37장)이 있는 저장소에서는 동작이 더 복잡해질 수 있다**: 서브모듈 디렉터리 내부의 untracked 파일은 기본 `git clean`의 대상 범위 밖에 있을 수 있으며, 필요하다면 `--force` 옵션을 두 번 지정(`-ff`)하거나 서브모듈 안에서 별도로 clean을 실행해야 한다. 이 상세 내용은 37장에서 서브모듈을 다룰 때 참고한다.

## Reference

- [Git Tools - Stashing and Cleaning](https://git-scm.com/book/en/v2/Git-Tools-Stashing-and-Cleaning)
- [git-clean Documentation](https://git-scm.com/docs/git-clean)
