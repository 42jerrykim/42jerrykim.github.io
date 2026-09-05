---
draft: false
collection_order: 31
slug: git-add-patch-mode-partial-staging
title: "[Git] 31. git add -p — 부분 스테이징"
date: 2026-09-04
lastmod: 2026-09-04
description: "git add -p가 파일 하나를 hunk 단위로 쪼개 일부 변경만 선택적으로 스테이징하는 원리, 대화형 프롬프트의 각 명령(y/n/s/e) 의미, 한 파일에 섞인 서로 다른 목적의 수정을 커밋 단위로 분리하는 실전 절차를 정리한 Git 챕터다."
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
- Code-Review(코드리뷰)
- Open-Source(오픈소스)
- Career(커리어)
- Configuration(설정)
image: "wordcloud.png"
---

한 파일 안에서 버그 수정과 무관한 리팩터링을 동시에 진행하다 보면, 그 둘을 서로 다른 커밋으로 나누고 싶어질 때가 있다. 05장에서 `git add -p`의 존재만 짧게 언급했는데, 이 장은 그 대화형 부분 스테이징을 실제로 다룬다.

## 개요

```bash
git add -p              # 변경된 모든 추적 파일을 대상으로 hunk 단위 대화형 스테이징
git add -p src/app.js   # 특정 파일만 대상으로
```

이 명령을 실행하면 07장에서 다룬 `git diff` 형식의 변경 조각(hunk)이 하나씩 나타나고, 각각을 스테이징할지 말지 선택하라는 프롬프트가 뜬다.

```
@@ -10,6 +10,9 @@ function calculateTotal(items) {
   let total = 0;
   for (const item of items) {
     total += item.price;
+    if (item.discount) {
+      total -= item.discount;
+    }
   }
   return total;
 }
Stage this hunk [y,n,q,a,d,s,e,?]?
```

## 기본 개념

<strong>hunk</strong>는 07장에서 살펴본 diff의 `@@ ... @@` 헤더로 구분되는 변경 덩어리 하나를 가리킨다. 한 파일에 여러 곳을 수정했다면 Git은 이를 여러 hunk로 나눠 보여주고, 각 hunk마다 독립적으로 "이번 커밋에 포함할지"를 물어본다. 이 방식으로 04장에서 다룬 스테이징 영역에는 파일 전체가 아니라 그 파일의 <strong>일부 변경만</strong> 반영할 수 있다.

## 종류/세부

### 프롬프트 명령어

각 hunk에서 선택할 수 있는 명령은 다음과 같다.

| 입력 | 동작 |
|---|---|
| `y` | 이 hunk를 스테이징 |
| `n` | 이 hunk를 건너뜀(스테이징 안 함) |
| `q` | 남은 모든 hunk에 대해 더 묻지 않고 종료 |
| `a` | 이 파일의 남은 hunk를 전부 스테이징 |
| `d` | 이 파일의 남은 hunk를 전부 건너뜀 |
| `s` | 이 hunk를 더 작은 단위로 쪼개기(split) |
| `e` | hunk 내용을 직접 편집(edit)해서 원하는 부분만 반영 |
| `?` | 도움말 표시 |

`s`(split)는 하나의 hunk 안에 서로 무관한 두 줄 변경이 섞여 있을 때, 그 hunk를 더 잘게 나눠 각각 따로 결정할 수 있게 해준다. 다만 Git이 자동으로 나눌 수 있는 크기에는 한계가 있어, 아주 가까이 붙어 있는 줄들은 더 쪼개지지 않을 수 있다 — 이럴 때 `e`(edit)로 hunk의 diff 텍스트 자체를 직접 편집해 원하는 줄만 남기고 나머지는 지우는 방법을 쓴다.

### 실전 시나리오 — 뒤섞인 변경을 커밋 두 개로 분리

한 파일에서 버그를 수정하면서 동시에 변수 이름도 정리했다고 가정하자. 이 둘을 각각 별개의 커밋(08장에서 다룬 "논리적 단위" 원칙)으로 나누고 싶다면:

```bash
git add -p src/app.js
# 버그 수정에 해당하는 hunk만 y로 스테이징, 이름 변경 hunk는 n
git commit -m "할인 계산 버그 수정"

git add src/app.js       # 남은 변경(이름 정리) 전체 스테이징
git commit -m "변수 이름을 의미에 맞게 정리"
```

이렇게 분리하면 09장의 `git log`나 32장의 `git blame`으로 나중에 "이 버그가 언제 수정됐는가"를 찾을 때, 무관한 이름 변경까지 뒤섞이지 않은 깔끔한 커밋을 확인할 수 있다.

### `git diff --staged`로 최종 확인

부분 스테이징이 끝나면 실제로 무엇이 커밋에 포함될지 07장의 `git diff --staged`로 반드시 확인한다.

```bash
git diff --staged
```

## 주의사항·함정

**새 파일(untracked)에는 `-p`가 hunk를 나눠 보여주지 않는다**: 기본적으로 `git add -p`는 이미 추적 중인 파일의 수정에만 적용된다. 새로 만든 파일 전체를 부분적으로만 스테이징하고 싶다면 `git add -N`(intent-to-add)으로 먼저 파일을 추적 대상으로 등록한 뒤 `-p`를 써야 한다.

**변경이 서로 의존적이면 부분 스테이징이 컴파일 불가능한 상태를 만들 수 있다**: 어떤 hunk가 다른 hunk에서 정의한 변수나 함수에 의존한다면, 한쪽만 스테이징해 커밋하면 그 커밋 시점의 코드가 실행되지 않을 수 있다. 26장에서 다룬 cherry-pick의 의존성 문제와 같은 종류의 위험이다 — 커밋하기 전 `git diff --staged`로 실제로 그 상태가 온전한지 확인하는 습관이 필요하다.

**`s`로 쪼개도 원하는 만큼 세밀하게 나뉘지 않을 수 있다**: Git의 자동 분할은 변경된 줄 사이의 문맥(context) 줄 수에 따라 한계가 있다. 정말 세밀한 제어가 필요하다면 결국 `e`(직접 편집)가 가장 확실한 방법이다.

## Reference

- [git-add Documentation](https://git-scm.com/docs/git-add)
