---
draft: false
collection_order: 27
slug: git-rebase-interactive-mode
title: "[Git] 27. git rebase -i — 인터랙티브 리베이스"
date: 2026-09-04
lastmod: 2026-09-04
description: "git rebase -i로 여러 커밋을 pick/squash/reword/drop 명령으로 재정리하는 법, 편집기에 열리는 todo 목록을 읽는 법, Pull Request를 올리기 전 커밋을 논리적 단위로 정돈하는 실전 절차를 정리한 Git 챕터다."
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

15장에서 미리 언급했던 대화형 리베이스는, 단순히 브랜치를 다른 지점으로 옮기는 것을 넘어 커밋 자체를 합치고 순서를 바꾸고 메시지를 고칠 수 있는 Git에서 가장 강력한 히스토리 편집 도구다. 이 장은 그 편집 절차를 단계별로 다룬다.

## 개요

```bash
git rebase -i HEAD~4    # 최근 4개 커밋을 대화형으로 재정리
```

이 명령을 실행하면 편집기(02장에서 설정한 `core.editor`)가 열리고, 대상 커밋들이 오래된 순서대로 나열된 목록(todo list)이 나타난다.

```
pick a1b2c3d 로그인 폼 UI 추가
pick 9f8e7d6 오타 수정
pick 3f2a1c9 로그인 API 연동
pick 7d6c5b4 console.log 제거

# 리베이스 a1b2c3d..7d6c5b4 (4개 커밋)
#
# 명령:
# p, pick <커밋> = 커밋 그대로 사용
# r, reword <커밋> = 커밋 사용, 메시지만 수정
# e, edit <커밋> = 커밋 사용, 멈춰서 수정할 기회를 줌
# s, squash <커밋> = 커밋 사용, 바로 이전 커밋에 합침
# f, fixup <커밋> = squash와 같지만 이 커밋의 메시지는 버림
# d, drop <커밋> = 커밋 제거
```

각 줄 맨 앞의 단어(`pick` 등)를 원하는 명령으로 바꾸고 저장하면, Git이 그 지시에 따라 커밋들을 하나씩 재적용한다.

## 기본 개념

이 목록에서 주의할 점은 <strong>커밋이 위에서 아래로, 즉 오래된 것부터 최신 순으로 나열된다</strong>는 것이다 — `git log`(09장)의 기본 출력(최신이 위)과 정반대다. "오타 수정" 커밋을 그 직전 커밋("로그인 폼 UI 추가")에 합치고 싶다면, 목록에서 아래 커밋(시간상 나중)의 명령을 `squash`(또는 `fixup`)로 바꾼다 — squash/fixup은 항상 "바로 위 줄(=시간상 이전 커밋)에 합친다"는 의미이기 때문이다.

```
pick a1b2c3d 로그인 폼 UI 추가
fixup 9f8e7d6 오타 수정          # "로그인 폼 UI 추가"에 흡수, 메시지는 버림
pick 3f2a1c9 로그인 API 연동
pick 7d6c5b4 console.log 제거
```

## 종류/세부

### 자주 쓰는 조합

| 상황 | 조작 |
|---|---|
| 실수로 남긴 "오타 수정", "console.log 제거" 같은 자잘한 커밋을 정리 | 해당 줄을 `fixup`으로 바꿔 관련 커밋에 흡수 |
| 커밋 메시지의 오타나 부족한 설명을 고치고 싶음 | 해당 줄을 `reword`로 바꾸면, 저장 후 그 커밋의 메시지만 다시 편집하는 창이 열림 |
| 커밋 순서를 바꾸고 싶음 | 목록에서 해당 줄을 원하는 위치로 잘라 옮김(단, 서로 의존하는 커밋의 순서를 바꾸면 충돌·빌드 실패 위험) |
| 특정 커밋에서 파일을 하나 더 추가하거나 코드를 고치고 싶음 | 해당 줄을 `edit`으로 바꾸면, 그 커밋에서 리베이스가 멈추고 수정 후 `git rebase --continue`로 이어감 |
| 필요 없어진 실험적 커밋을 아예 없애고 싶음 | 해당 줄을 `drop`으로 바꾸거나, 줄 자체를 삭제 |

### 자동 fixup(`--autosquash`)

커밋을 만들 때부터 나중에 합칠 대상을 미리 표시해두면, 대화형 목록을 손으로 재배열하지 않고도 자동으로 정리할 수 있다.

```bash
git commit --fixup=a1b2c3d          # "fixup! 로그인 폼 UI 추가"라는 메시지로 커밋
git rebase -i --autosquash a1b2c3d^  # 편집기가 열릴 때 이미 fixup 대상이 알맞은 위치로 정렬되어 있음
```

이 조합은 코드 리뷰 중 "이 부분 놓쳤어요" 같은 피드백을 받을 때마다 즉시 `--fixup` 커밋을 만들어두고, 나중에 병합 직전 한 번에 정리하는 워크플로에 유용하다.

## 주의사항·함정

**여기서도 "공유된 커밋을 리베이스하지 않는다"는 15장의 황금률이 그대로 적용된다**: 대화형 리베이스는 결국 일반 리베이스와 마찬가지로 커밋 해시를 재작성한다. 아직 push하지 않은 로컬 커밋, 또는 자신만 쓰는 개인 기능 브랜치에서만 안전하게 쓸 수 있다.

**squash/fixup 순서를 반대로 착각하기 쉽다**: 위에서 설명한 "squash는 바로 위 줄에 합쳐진다"는 규칙을 반대로 기억하면, 의도와 다른 커밋에 변경이 흡수된다. 헷갈린다면 목록을 저장하기 전에 각 줄이 어떤 커밋을 가리키는지 커밋 메시지로 한 번 더 확인하는 편이 안전하다.

**충돌이 나면 커밋별로 여러 번 해결해야 할 수 있다**: 15장에서 다룬 것과 동일하게, 재정리 대상 커밋 여러 개에서 각각 충돌이 날 수 있다. `git rebase --continue`로 하나씩 넘어가며 해결하고, 복잡하다고 판단되면 `git rebase --abort`로 시작 전 상태로 되돌릴 수 있다는 안전망을 기억해둔다.

## Reference

- [git-rebase Documentation](https://git-scm.com/docs/git-rebase)
