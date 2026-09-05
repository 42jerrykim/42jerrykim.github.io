---
draft: false
collection_order: 8
slug: git-commit-command-writing-good-commits
title: "[Git] 08. git commit — 커밋 작성 규칙"
date: 2026-09-04
lastmod: 2026-09-04
description: "git commit이 스테이징 영역을 저장소에 스냅샷으로 기록하는 방식, 좋은 커밋 메시지의 제목/본문 관례, --amend로 마지막 커밋을 고치는 법과 그 위험을 정리한 Git 챕터다."
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
- Collaboration(협업)
- Code-Review(코드리뷰)
- Advanced
- Open-Source(오픈소스)
- Career(커리어)
image: "wordcloud.png"
---

`git commit -m "fix"`, `git commit -m "update"`처럼 내용을 알 수 없는 커밋 메시지가 쌓인 저장소는, 나중에 `git log`나 `git blame`으로 "이 코드가 왜 이렇게 바뀌었는가"를 추적할 때 아무 도움이 되지 않는다. 이 장은 `git commit`이 실제로 무엇을 기록하는지와, 그 기록을 나중에 쓸모 있게 만드는 메시지 관례를 다룬다.

## 개요

`git commit`은 스테이징 영역(04장)의 현재 내용을 저장소에 새 스냅샷으로 기록하는 명령이다. 메시지를 함께 지정하지 않으면 02장에서 설정한 `core.editor`가 열리고, `-m` 옵션으로 짧은 메시지는 명령줄에서 바로 지정할 수 있다.

```bash
git commit -m "커밋 제목"
git commit                     # 편집기가 열려 메시지를 여러 줄로 작성
git commit -am "커밋 제목"      # 이미 추적 중인 파일을 자동 스테이징 후 커밋(05장)
```

커밋이 성공하면 Git은 그 커밋의 해시(SHA-1, 40자 16진수), 브랜치 이름, 변경된 파일 수와 삽입/삭제 줄 수를 요약해 보여준다. 이 해시는 이후 26장의 `cherry-pick`, 23장의 `reset`처럼 특정 커밋을 지칭할 때 그대로 쓰인다.

## 기본 개념

각 커밋 객체는 스냅샷을 가리키는 트리(tree) 참조 외에도, 작성자(author)와 커미터(committer) 정보, 부모 커밋의 해시, 그리고 커밋 메시지를 함께 저장한다. 작성자와 커미터가 다를 수 있다는 점이 흥미로운데, 예를 들어 다른 사람이 작성한 패치를 `cherry-pick`(26장)으로 가져오면 원저자는 author로 남고 지금 이 명령을 실행한 사람이 committer로 기록된다. 이 구조는 34장의 Git 객체 모델에서 다시 짚는다.

커밋 메시지는 자유 텍스트지만, Git 프로젝트 자체를 포함한 대부분의 오픈소스 커뮤니티가 따르는 관례가 있다. 첫 줄(제목)은 50자 내외로 변경 내용을 명령형으로 요약하고, 빈 줄을 하나 띄운 뒤 본문에서 "무엇을"이 아니라 "왜" 그렇게 바꿨는지 설명한다.

```
짧고 명령형인 제목 (50자 이내)

본문은 필요할 때만 작성한다. 여기서는 코드를 보면 알 수 있는
"무엇을 바꿨는가"보다, 코드만 봐서는 알 수 없는 "왜 이렇게
바꿨는가"(배경, 트레이드오프, 참고한 이슈 번호 등)를 설명한다.
```

## 종류/세부

### 마지막 커밋 수정(`--amend`)

커밋 직후 오타를 발견했거나 파일 하나를 빠뜨렸다면, 새 커밋을 추가하는 대신 마지막 커밋 자체를 고칠 수 있다.

```bash
git add forgotten-file.txt
git commit --amend --no-edit    # 메시지는 그대로 두고 스테이징된 내용만 추가
git commit --amend              # 메시지도 함께 수정(편집기가 열림)
```

`--amend`는 마지막 커밋을 지우고 그 자리에 완전히 새로운 커밋(새 해시)을 만드는 것과 같다 — 즉 "수정"이 아니라 "교체"다. 이 차이는 이미 원격 저장소에 push한 커밋을 amend할 때 문제가 된다.

### 여러 개의 작은 커밋 vs 하나의 큰 커밋

| 방식 | 장점 | 단점 |
|---|---|---|
| 작은 단위로 자주 커밋 | 리뷰하기 쉽고, `git bisect`(33장)로 문제 커밋을 좁히기 쉬움 | 히스토리가 길어짐 |
| 기능 완성 후 한 번에 커밋 | 히스토리가 간결함 | 리뷰·문제 추적이 어려움, 작업 중 실수 시 되돌릴 단위가 커짐 |

이 트레이드오프에 대한 실무적 절충안이 15장·27장에서 다루는 리베이스다 — 작업 중에는 작은 단위로 자주 커밋해 안전망을 확보하고, 원격에 push하거나 Pull Request를 올리기 전에 `git rebase -i`로 관련 커밋들을 논리적인 단위로 재정리한다.

## 주의사항·함정

**`--amend`로 이미 공유된 커밋을 고치면 협업자와 히스토리가 어긋난다**: 다른 사람이 이미 pull해간 커밋을 amend하면 해시가 바뀐 새 커밋이 생기고, 그 협업자의 로컬 히스토리는 옛 커밋을 그대로 가리키고 있어 이후 push/pull 시 충돌이나 예기치 않은 병합이 발생한다. amend는 아직 아무에게도 공유하지 않은 로컬 커밋에만 쓰는 것이 안전하다.

**작성자 정보가 잘못된 채로 커밋되기 쉽다**: 02장에서 `--local` 설정을 프로젝트별로 나누지 않았다면, 회사 컴퓨터에서 개인 프로젝트에 커밋할 때 회사 이메일이 그대로 기록된다. 커밋 전에 `git config user.email`로 현재 적용되는 값을 확인하는 습관이 이 실수를 막는다.

**커밋 메시지에 민감 정보를 적으면 안 된다**: 커밋 메시지도 코드 내용과 마찬가지로 저장소 히스토리에 영구히 남는다. 비밀번호·API 키·개인정보를 메시지에 적었다면 히스토리 재작성이 필요하며, 이는 43장의 보안 챕터에서 다룬다.

## Reference

- [git-commit Documentation](https://git-scm.com/docs/git-commit)
