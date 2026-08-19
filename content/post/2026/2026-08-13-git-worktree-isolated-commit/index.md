---
title: "[Git] worktree로 지저분한 브랜치에서 파일 하나만 격리 커밋하기"
description: "작업 브랜치가 무관한 WIP로 지저분할 때 git worktree로 별도 작업 디렉터리를 만들어 파일 하나만 깨끗하게 커밋·PR로 올리는 방법을 실제 PR 사례로 정리한다. stash보다 안전한 이유와 브랜치 충돌 복구 응용까지 다룬다."
date: 2026-08-13
lastmod: 2026-08-13
draft: false
categories:
  - Git
  - Workflow
tags:
  - Git
  - GitHub
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Automation(자동화)
  - DevOps(데브옵스)
  - Productivity(생산성)
  - Workflow(워크플로우)
  - How-To
  - Tips
  - Best-Practices
  - Code-Review(코드리뷰)
  - Collaboration(협업)
  - Version-Control(버전관리)
  - Shell(셸)
  - Concurrency(동시성)
  - worktree
  - git-worktree
  - cherry-pick
  - Pull-Request
  - Branch-Management
  - AI-Agent
  - Claude-Code
  - Session-Isolation
  - Multi-Agent
  - WIP
image: "wordcloud.png"
---

## 개요

작업 중인 브랜치가 이미 다른 목적의 커밋되지 않은 변경사항(WIP)으로 지저분한 상태에서, 그와 전혀 무관한 파일 하나만 급하게 별도 PR로 올려야 하는 상황이 있다. 이때 무심코 `git add .`를 하면 무관한 WIP까지 같은 커밋에 섞여 들어가고, `git stash`로 잠시 치워두는 방법도 stash pop을 잊거나 충돌이 나면 작업 트리 상태를 잃을 위험이 남는다. `git worktree`로 완전히 별도의 임시 작업 디렉터리를 만들면 원래 작업 트리를 물리적으로 전혀 건드리지 않고 파일 하나만 격리해 커밋할 수 있다. 이 글은 실제로 이 기법을 써서 병합된 PR 사례로 절차를 보이고, `stash`·브랜치 전환 대비 이 방법이 더 안전한 이유, 그리고 여러 자동화 세션이 같은 체크아웃을 동시에 쓰다 브랜치가 꼬였을 때 같은 원리로 복구한 응용 사례까지 정리한다.

## git worktree란 무엇인가

`git worktree`는 하나의 `.git` 저장소(커밋·오브젝트·레퍼런스 데이터베이스)를 공유하면서 **여러 개의 독립된 작업 디렉터리**를 동시에 둘 수 있게 해주는 Git 내장 명령이다([공식 문서](https://git-scm.com/docs/git-worktree)). 일반적으로 하나의 클론(clone)에는 작업 디렉터리가 하나뿐이라 다른 브랜치로 전환하려면 `git checkout`/`git switch`로 지금 디렉터리의 내용 자체를 바꿔야 하고, 이 과정에서 커밋되지 않은 변경사항이 있으면 stash하거나 커밋해야 한다. `git worktree add`는 이 제약을 없앤다 — 원래 디렉터리는 지금 상태 그대로 두고, 다른 경로에 다른 브랜치를 체크아웃한 두 번째(세 번째, ...) 작업 디렉터리를 새로 만든다. 새 worktree는 `HEAD`·인덱스 같은 자신만의 관리 파일(`.git/worktrees/<name>/`)만 따로 두고, 오브젝트·레퍼런스 저장소 자체는 `commondir`를 통해 원본 `.git`을 그대로 직접 참조해 공유한다. 그래서 오브젝트를 복제하지 않으므로 디스크 사용량도 체크아웃된 워킹 파일 크기만큼만 추가된다.

stash나 브랜치 전환과 근본적으로 다른 지점은 **원래 작업 트리를 전혀 건드리지 않는다**는 것이다. stash는 현재 디렉터리의 변경사항을 임시로 치웠다가 되돌리는 방식이라 pop을 잊거나 stash 목록이 꼬이면 변경사항을 찾기 어려워질 수 있고, 브랜치 전환은 추적되지 않는 파일이 충돌하면 전환 자체가 막히거나 예상 못 한 파일이 사라질 수 있다. worktree는 애초에 별도의 물리적 디렉터리이므로 이런 위험이 구조적으로 없다.

## 실전 절차 — 태그 게시글 수 표시 기능을 별도 PR로

이 저장소(42jerrykim.github.io)에서 실제로 있었던 사례다. "태그 옆에 게시글 수를 `(n)` 형태로 보여달라"는 요청이 들어왔는데, 마침 현재 브랜치는 태그 3,600여 개를 정리하는 대규모 태그 통합(consolidation) 작업으로 커밋되지 않은 변경이 잔뜩 쌓인 상태였다. 이 상태에서 태그 개수 표시 기능까지 같은 브랜치에 커밋하면, 무관한 두 작업이 하나의 PR에 섞여 리뷰도 롤백도 어려워진다. 대신 다음 절차로 완전히 분리했다.

```bash
# 1. origin/main을 기준으로 하는 새 브랜치를 만든다(현재 지저분한 브랜치와 무관)
git branch feat/tag-post-count origin/main

# 2. 별도 경로에 그 브랜치를 체크아웃하는 새 작업 디렉터리를 만든다
git worktree add /tmp/tag-count-worktree feat/tag-post-count

# 3. 그 worktree 안에서만 파일을 만들고 커밋한다 (원래 디렉터리는 전혀 손대지 않음)
cd /tmp/tag-count-worktree
cat > layouts/partials/article/components/tags.html <<'EOF'
{{ if .Params.Tags }}
    <section class="article-tags">
        {{ range (.GetTerms "tags") }}
            <a href="{{ .RelPermalink }}">{{ .LinkTitle }} ({{ len .Pages }})</a>
        {{ end }}
    </section>
{{ end }}
EOF
git add layouts/partials/article/components/tags.html
git commit -m "feat: show tag post count on article pages"
git push -u origin feat/tag-post-count

# 4. PR을 만들고 나면 임시 작업 디렉터리를 정리한다
cd -
git worktree remove --force /tmp/tag-count-worktree
```

핵심은 새로 만든 파일이 테마(`hugo-theme-stack`)가 제공하는 태그 파셜을 그대로 오버라이드한다는 점이다. Hugo는 빌드 시점에 이미 각 태그(taxonomy term)에 속한 페이지 목록을 계산해두므로, `.GetTerms "tags"`로 현재 글의 태그 term들을 가져와 각각의 `.Pages`(그 태그가 붙은 글 목록)의 길이만 세면 추가 연산 없이 카운트를 구할 수 있다. 이 PR([#44, "feat: show tag post count on article pages"](https://github.com/42jerrykim/42jerrykim.github.io/pull/44))은 이렇게 만든 worktree 안에서만 작업해 2026년 7월 3일 병합됐고, 원래 브랜치의 태그 통합 작업은 전혀 영향을 받지 않은 채 별도로 계속됐다.

## stash·브랜치 전환과 비교

세 방식 모두 "지금 상태를 건드리지 않고 다른 작업을 하고 싶다"는 같은 목적에 쓰이지만, 안전성과 비용의 트레이드오프가 다르다.

| 방식 | 원래 작업 트리 보존 | 실패 시 위험 | 디스크 비용 |
|---|---|---|---|
| `git stash` | 임시로 비움(되돌려야 함) | pop 누락·충돌 시 변경사항 추적 어려움 | 거의 없음 |
| `git checkout`으로 브랜치 전환 | 전환 시점에 그 디렉터리 내용이 바뀜 | 추적 안 된 파일 충돌 시 전환 자체가 막히거나 파일 유실 가능 | 거의 없음 |
| `git worktree add` | 완전 보존(별도 디렉터리) | 없음(원본 미접촉) | 오브젝트는 공유, 체크아웃된 파일만큼만 추가 |

정리 작업(3번째 열)이 필요 없다는 점에서 stash·브랜치 전환이 더 간편해 보이지만, "지금 당장은 무관한 작은 변경 하나만 안전하게 별도 PR로 올려야 한다"는 상황에서는 원본을 물리적으로 아예 건드리지 않는 worktree 쪽이 실패 모드 자체가 없다는 확실한 이점이 있다.

## 응용 — 여러 자동화 세션이 브랜치를 충돌시켰을 때 복구

이 저장소는 `post-quality-loop`, `engagement-report` 같은 여러 스케줄 작업이 같은 로컬 체크아웃을 시차를 두고 사용한다. 두 작업이 겹치면 한쪽이 만든 커밋이 의도한 `main`이 아니라 다른 작업이 방금 체크아웃해놓은 브랜치 위에 잘못 얹히는 사고가 날 수 있다. 이럴 때 `git checkout main`으로 직접 되돌리는 것은 다른 세션이 아직 진행 중인 작업 상태를 깨뜨릴 위험이 있어 섣불리 시도하기 어렵다.

같은 격리 원리를 복구에도 그대로 적용할 수 있다. `git worktree add ../recovery-worktree main`으로 지금 체크아웃과 완전히 독립된 작업 디렉터리를 새로 만들고, 그 안에서 `git cherry-pick <잘못 얹힌 커밋 해시>`로 원하는 커밋만 골라 `main` 위에 다시 얹은 뒤 push하고, `git worktree remove`로 정리하면 된다([cherry-pick 공식 문서](https://git-scm.com/docs/git-cherry-pick)). 이 과정 내내 다른 세션이 쓰고 있는 원래 브랜치·체크아웃은 전혀 건드리지 않는다. "격리된 worktree"의 쓸모가 지저분한 브랜치에서 파일 하나를 안전하게 떼어내는 상황뿐 아니라, 잘못된 브랜치에 이미 얹힌 커밋을 다른 작업에 영향을 주지 않고 올바른 브랜치로 옮기는 복구 상황까지 넓어지는 지점이다.

## 실전 팁 — 자주 하는 실수

1. **`worktree remove`에 `--force`를 빼먹는다.** 커밋되지 않은 변경이나 추적되지 않은 파일이 worktree 안에 남아 있으면 일반 `remove`는 거부된다. 임시 worktree는 목적을 다했으면 안에 아무것도 안 남기고 지우는 것이 전제이므로, 커밋·push까지 끝낸 뒤에만 제거해야 하고 남은 게 있으면 먼저 커밋하거나 버릴지 확인해야 한다.
2. **worktree 경로를 저장소 안쪽에 만든다.** `/tmp/xxx`나 저장소 바깥 경로를 쓰지 않고 저장소 디렉터리 내부(`.worktrees/xxx` 등)에 만들면, `.gitignore`로 제외하지 않는 이상 `git status`가 원래 작업 트리에서도 그 디렉터리를 추적 대상으로 잡아 오히려 지저분해진다.
3. **다 쓴 worktree를 `git worktree list`로 확인하지 않고 방치한다.** 삭제를 잊은 worktree가 쌓이면 `git branch -d`로 브랜치를 지우려 할 때 "체크아웃 중이라 지울 수 없다"는 오류가 나서 원인 파악에 시간이 든다. `git worktree list`로 주기적으로 잔여 worktree를 확인하고 `git worktree prune`으로 정리한다.

## 이 글을 읽은 후 할 수 있어야 하는 것

- `stash`·브랜치 전환·`worktree` 세 방식이 "원래 작업 트리를 건드리는가"를 기준으로 어떻게 실패 모드가 갈리는지 설명할 수 있다.
- 지저분한 브랜치에서 무관한 파일 하나만 골라 별도 PR로 격리해 커밋하는 절차를 `git worktree add`부터 `remove`까지 직접 재현할 수 있다.
- 여러 세션·자동화가 같은 체크아웃을 공유하다 브랜치가 잘못 얹히는 사고가 났을 때, 원래 브랜치를 건드리지 않고 `cherry-pick` 기반으로 복구하는 절차를 적용할 수 있다.

## 요약

지저분한 브랜치에서 무관한 변경 하나만 안전하게 분리해 커밋해야 할 때, `git worktree add`로 별도 작업 디렉터리를 새로 만들면 원래 작업 트리를 전혀 건드리지 않고 격리된 상태에서 커밋·PR·정리까지 마칠 수 있다. stash나 브랜치 전환보다 정리 절차가 하나 더 필요하지만, 그 대가로 "실패해도 원본이 손상될 위험" 자체가 없어진다. 같은 원리는 파일 하나를 떼어내는 상황뿐 아니라, 여러 자동화 세션이 브랜치를 충돌시켰을 때 `cherry-pick`으로 커밋만 골라 옮겨 복구하는 데도 그대로 쓸 수 있다.

## 참고 자료

- [git-worktree, Git 공식 문서](https://git-scm.com/docs/git-worktree)
- [git-cherry-pick, Git 공식 문서](https://git-scm.com/docs/git-cherry-pick)
- [feat: show tag post count on article pages, PR #44](https://github.com/42jerrykim/42jerrykim.github.io/pull/44)
