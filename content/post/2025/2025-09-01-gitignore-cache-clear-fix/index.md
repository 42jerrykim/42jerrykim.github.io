---
title: "[Git] .gitignore 즉시 반영 안될 때 - 캐시 삭제 가이드"
description: ".gitignore가 바로 적용되지 않을 때의 원인과 해결책을 정리했습니다. git rm --cached로 인덱스만 비우고 규칙을 재적용하는 안전 절차, git check-ignore로 원인 추적, 인코딩·줄바꿈·공백 등 흔한 함정까지 포함합니다."
date: 2025-09-01
lastmod: 2025-09-01
categories:
- "Git"
- "Github"
tags:
- "git"
- "github"
- "gitignore"
- "ignore-files"
- "git-rm"
- "git-rm-cached"
- "staging-area"
- "index-cache"
- "git-cache"
- "cache-clear"
- "git-check-ignore"
- "debugging-gitignore"
- "git-status"
- "git-add"
- "git-commit"
- "git-push"
- "global-gitignore"
- "core.excludesFile"
- "info-exclude"
- "windows"
- "macos"
- "linux"
- "visual-studio"
- "android-studio"
- "intellij"
- "vscode"
- "utf-8"
- "utf-16"
- "eol"
- "crlf"
- "lf"
- "line-endings"
- "file-encoding"
- "binary-encoding"
- "tabs-vs-spaces"
- "trailing-whitespace"
- "negation-patterns"
- "globbing"
- "pathspec"
- "double-asterisk"
- "directory-pattern"
- "node_modules"
- "build-artifacts"
- "logs"
- "lock-files"
- "temp-files"
- "thumbs.db"
- ".DS_Store"
- "best-practices"
- "how-to"
- "troubleshooting"
- "faq"
- "tutorial"
- "지트"
- "깃"
- "깃허브"
- "깃이그노어"
- "무시규칙"
- "캐시삭제"
- "인덱스제거"
- "윈도우"
- "맥"
- "리눅스"
image: "wordcloud.png"
---

개발을 하다 보면 `.gitignore`에 분명히 추가했는데도 `node_modules`, 빌드 산출물, 로그 파일 등이 계속 `git status`에 잡히는 경험을 하게 됩니다. 이는 해당 파일들이 이미 한 번 “추적(tracked)” 상태가 되었기 때문으로, 규칙을 고쳐 쓰는 것만으로는 소급 적용되지 않습니다. 이 글은 인덱스(스테이징 영역)만 안전하게 비워 규칙을 재적용하는 방법, 특정 파일·폴더만 선택적으로 해제하는 방법, `git check-ignore -v`로 원인을 정확히 추적하는 요령, 그리고 패턴/인코딩/줄바꿈/공백 등 실제 현장에서 자주 놓치는 함정을 정리했습니다. Git 공식 문서와 주요 가이드를 바탕으로 실수 없이 적용할 수 있는 최소-위험 절차를 제시합니다.

## 요약
- **문제**: `.gitignore`를 새로 추가/수정했는데 무시 규칙이 즉시 적용되지 않음 (이미 추적 중인 파일은 계속 추적됨)
- **핵심 해결**: 인덱스(스테이징)에서만 제거해 규칙을 재적용

```bash
git rm -r --cached .
git add .
git commit -m "Apply .gitignore rules by clearing index cache"
git push
```

위 절차는 인덱스만 비우고 실제 파일은 보존합니다. 명령 동작은 공식 문서의 `--cached` 설명과 일치합니다.

## 배경: 왜 즉시 적용되지 않을까?
Git은 이미 버전 관리에 들어간(추적 중인) 파일을 `.gitignore`로 소급해 “자동 해제”하지 않습니다. 따라서 한 번 추적된 파일은 **인덱스에서 제거**해야 이후 커밋에서 무시 규칙이 반영됩니다.

## 안전 절차 (전체 인덱스 비우기)
1) 변경사항 커밋(또는 스태시)으로 안전 확보
2) 인덱스만 초기화 후 규칙 재적용

```bash
git rm -r --cached .
git add .
git commit -m ".gitignore re-apply"
```

참고: `git rm --cached`는 “인덱스에서만 제거, 워킹 트리 파일은 그대로”입니다. 공식 문서에는 다음과 같이 명시됩니다: 

> Use this option to unstage and remove paths only from the index. Working tree files will be left alone.

## 부분 적용 (특정 파일/폴더만)
전체가 과하다면 대상만 선택하세요.

```bash
# 단일 파일만 추적 해제
git rm --cached path/to/file

# 디렉터리만 추적 해제
git rm -r --cached path/to/directory

git add .
git commit -m "Stop tracking generated assets"
```

## 디버깅 체크리스트
- **규칙 충돌/우선순위**: 어느 규칙이 먹히는지 추적

```bash
git check-ignore -v path/to/suspect
```

- **패턴 작성**
  - 디렉터리 전체: `logs/`
  - 어디서든 매칭: `**/logs`
  - 예외 규칙: `!important.log` (단, 디렉터리 단위로 무시된 하위 파일은 예외 불가)
- **인코딩/줄바꿈**
  - `.gitignore`는 일반 텍스트(UTF-8)이어야 하며, **UTF-16/UCS-2** 저장 시 인식 실패 가능
  - CRLF/LF 줄바꿈 문제로 한 줄로 뭉개지는 경우 확인
- **공백/주석**
  - 행 맨 앞 공백, 행 끝 공백은 피하세요
  - 같은 줄 우측에 주석을 붙이면 규칙이 주석 처리된 것으로 해석될 수 있음 (주석은 별도 라인에)
- **파일명**
  - Windows에서 `.gitignore.txt`로 저장되지 않았는지 확인 (확장자 없음)

## 전역/로컬 제외 규칙도 활용
- 전역 무시 파일: 사용자 환경 전역에 공통 적용

```bash
touch ~/.gitignore
git config --global core.excludesFile ~/.gitignore
```

- 로컬 전용(공유하지 않음): 리포지토리 내부 `.git/info/exclude`

## 자주 묻는 질문(FAQ)
- Q. “`git rm -r --cached .`는 위험한가요?”
  - A. 워킹 트리 파일은 삭제하지 않습니다. 인덱스만 갱신하고, 이후 `git add .`로 규칙을 반영합니다. 그래도 불안하다면 **대상 파일/폴더만** `--cached`로 제거하세요.
- Q. 규칙이 맞는 것 같은데 왜 계속 추적되나요?
  - A. 이미 추적 중인 파일입니다. 먼저 `--cached`로 인덱스에서 제거한 뒤 커밋하세요.
- Q. 예외 규칙이 통하지 않아요
  - A. 디렉터리 단위 무시(`logs/`)에 의해 무시된 하위 파일은 예외(`!logs/important.log`)로 되살릴 수 없습니다.

## 빠른 레퍼런스 명령 모음
```bash
# 전체 인덱스 비우고 규칙 재적용
git rm -r --cached . && git add . && git commit -m ".gitignore re-apply"

# 특정 파일/폴더만 추적 해제
git rm --cached <file>
git rm -r --cached <directory>

# 어떤 규칙이 적용됐는지 추적
git check-ignore -v <path>
```

## 참고 자료
- 원문 가이드: [Contributor9, “.gitignore 파일이 바로 적용이 안될때 해결방법: git 캐시 삭제”](https://adjh54.tistory.com/376)
- Git 공식 문서: [git rm](https://git-scm.com/docs/git-rm), [git check-ignore](https://git-scm.com/docs/git-check-ignore)
- GitHub Docs: [Ignoring files](https://docs.github.com/en/get-started/git-basics/ignoring-files)
- Atlassian 튜토리얼: [.gitignore file - ignoring files in Git](https://www.atlassian.com/git/tutorials/saving-changes/gitignore)
- 토론/사례: [Stack Overflow - “Gitignore not working”](https://stackoverflow.com/questions/25436312/gitignore-not-working)


