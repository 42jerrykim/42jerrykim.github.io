---
draft: false
collection_order: 10
slug: gitignore-file-exclude-patterns
title: "[Git] 10. .gitignore — 추적 제외 규칙"
date: 2026-09-04
lastmod: 2026-09-04
description: ".gitignore 패턴 문법(와일드카드, 디렉터리 전용 표기, 부정 패턴), 이미 추적 중인 파일에는 무시 규칙이 적용되지 않는 이유, 전역 gitignore와 저장소별 규칙의 관계를 정리한 Git 챕터다."
categories:
- Git
tags:
- Git
- GitHub
- Version-Control(버전관리)
- Terminal
- Configuration(설정)
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
- File-System(파일시스템)
- Security(보안)
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
- Command-Line
image: "wordcloud.png"
---

`node_modules/`, `build/`, `.env` 같은 파일이 실수로 커밋되어 저장소 크기가 비대해지거나 비밀 정보가 유출되는 사고는, 대개 `.gitignore` 파일을 프로젝트 시작 시점에 제대로 설정하지 않았을 때 생긴다. 이 장은 `.gitignore` 패턴 문법과, 이미 추적 중인 파일에는 이 규칙이 통하지 않는다는 자주 놓치는 예외를 다룬다.

## 개요

`.gitignore`는 저장소 루트(또는 하위 디렉터리)에 두는 일반 텍스트 파일로, 각 줄에 무시할 파일·디렉터리 패턴을 적는다.

```gitignore
# 주석은 #으로 시작
node_modules/
*.log
.env
dist/
!dist/keep-this.txt
```

이 규칙에 매칭되는 파일은 `git status`(06장)의 Untracked files 목록에도, `git add .`의 대상에도 나타나지 않는다.

## 기본 개념

패턴 문법은 셸의 glob과 비슷하지만 몇 가지 고유한 규칙이 있다.

| 패턴 | 의미 |
|---|---|
| `*.log` | 확장자가 `.log`인 모든 파일(모든 디렉터리 포함) |
| `build/` | 이름이 `build`인 디렉터리 전체(끝의 `/`가 디렉터리 전용임을 명시) |
| `/config.json` | 저장소 루트의 `config.json`만(하위 디렉터리의 동명 파일은 무시하지 않음) |
| `**/temp` | 모든 깊이의 `temp`라는 이름의 파일·디렉터리 |
| `!important.log` | 앞선 규칙으로 무시된 대상 중 이 파일만 예외로 다시 추적 |

부정 패턴(`!`)은 상위 디렉터리 자체가 이미 무시된 경우에는 적용되지 않는다는 점이 자주 걸리는 함정이다 — `build/`로 디렉터리 전체를 무시했다면, 그 안의 특정 파일만 `!build/keep.txt`로 되살리려 해도 Git은 애초에 `build/` 디렉터리 자체를 순회하지 않으므로 예외가 적용되지 않는다.

## 종류/세부

### 이미 추적 중인 파일에는 적용되지 않는다

`.gitignore`는 <strong>아직 한 번도 커밋되지 않은(untracked)</strong> 파일에만 작동한다. 실수로 이미 커밋해버린 파일을 뒤늦게 `.gitignore`에 추가해도, Git은 이미 추적 중인 파일이므로 계속 변경 사항을 감시한다. 추적을 중단하려면 명시적으로 인덱스에서 제거해야 한다.

```bash
echo "config.json" >> .gitignore
git rm --cached config.json   # 작업 트리의 파일은 남기고 추적만 중단
git commit -m "config.json 추적 중단"
```

`--cached` 옵션이 핵심이다 — 이 옵션 없이 `git rm config.json`을 실행하면 작업 트리의 실제 파일까지 삭제된다.

### 전역 gitignore vs 저장소별 gitignore

| 종류 | 위치 | 적용 범위 | 용도 |
|---|---|---|---|
| 저장소별 `.gitignore` | 저장소 루트(또는 하위) | 그 저장소만, 커밋되어 팀 전체가 공유 | 프로젝트 고유의 빌드 산출물, 언어별 캐시 |
| 전역 gitignore | `git config --global core.excludesfile`로 지정한 경로 | 이 컴퓨터의 모든 저장소 | 개인 편집기 설정 파일(`.vscode/`, `.idea/` 등), OS 파일(`.DS_Store`) |
| 로컬 전용 제외 규칙 | `.git/info/exclude` | 이 저장소, 이 컴퓨터만(커밋되지 않음) | 팀과 공유하고 싶지 않은 개인적인 무시 규칙 |

팀 프로젝트의 `.gitignore`에 개인 편집기 설정까지 넣으면 다른 편집기를 쓰는 팀원에게는 불필요한 항목이 된다. 이런 개인 취향에 가까운 규칙은 전역 gitignore나 `.git/info/exclude`로 분리하는 것이 관례다.

```bash
git config --global core.excludesfile ~/.gitignore_global
```

## 주의사항·함정

**커밋 직후 `.gitignore`를 추가해도 이미 커밋된 파일은 사라지지 않는다**: 위에서 설명한 `git rm --cached`를 실행하지 않으면, `.gitignore`에 패턴을 추가한 것만으로는 이미 히스토리에 기록된 과거 커밋의 내용이 지워지지 않는다. 비밀 정보가 이미 커밋됐다면 43장에서 다루는 히스토리 재작성이 필요하다.

**언어·프레임워크별 표준 템플릿을 처음부터 쓰는 편이 안전하다**: 프로젝트 시작 시점에 어떤 파일을 무시해야 할지 직접 하나씩 나열하기보다, GitHub이 제공하는 [gitignore 템플릿 저장소](https://github.com/github/gitignore) 같은 검증된 목록으로 시작하는 편이 빠뜨리는 항목을 줄인다.

**패턴 순서가 뒤바뀌면 부정 패턴이 무시된다**: `.gitignore` 안에서 규칙은 위에서 아래로 적용되며, 나중에 나온 규칙이 앞선 규칙을 덮어쓸 수 있다. `!important.log`가 `*.log`보다 먼저 나오면 아직 `*.log` 규칙이 적용되기 전이라 의도한 예외가 반영되지 않을 수 있으므로, 부정 패턴은 관련된 무시 규칙 뒤에 두는 것이 안전하다.

## Reference

- [gitignore Documentation](https://git-scm.com/docs/gitignore)
