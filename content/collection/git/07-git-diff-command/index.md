---
draft: false
collection_order: 7
slug: git-diff-command-compare-changes
title: "[Git] 07. git diff — 변경 비교"
date: 2026-09-04
lastmod: 2026-09-04
description: "git diff의 기본 출력 형식을 읽는 법, --staged로 비교 대상을 바꾸는 법, 두 커밋·브랜치 사이의 diff를 조회하는 법, 파일 이름 변경 감지 옵션까지 정리한 Git 챕터다."
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
- Code-Review(코드리뷰)
- Configuration(설정)
- Advanced
- Career(커리어)
- Open-Source(오픈소스)
image: "wordcloud.png"
---

`git status`가 "무엇이 바뀌었는가"를 파일 목록으로 알려준다면, `git diff`는 "정확히 어느 줄이 어떻게 바뀌었는가"를 보여준다. 06장에서 다룬 세 구역 개념을 그대로 이어받아, `git diff`가 기본적으로 어느 두 지점을 비교하는지부터 짚는다.

## 개요

옵션 없는 `git diff`는 작업 트리와 스테이징 영역을 비교한다 — 즉 "아직 `git add`하지 않은 변경"만 보여준다.

```bash
git diff
```

```diff
diff --git a/README.md b/README.md
index e69de29..8b13789 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,2 @@
+# My Project
+
```

`@@ -1 +1,2 @@`는 "hunk 헤더"로, 원본 파일 1번째 줄부터 1줄, 수정본 1번째 줄부터 2줄이 이 구간에 해당한다는 뜻이다. `-`로 시작하는 줄은 삭제된 줄, `+`로 시작하는 줄은 추가된 줄이며, 접두어 없는 줄은 두 버전 모두에 존재하는 변경 없는 문맥(context) 줄이다.

## 기본 개념

`git diff`가 비교하는 두 지점은 옵션에 따라 달라지며, 이 선택이 04장의 3단계 모델 중 어느 경계를 보고 싶은가에 대응한다.

| 명령 | 비교 대상 |
|---|---|
| `git diff` | 작업 트리 ↔ 스테이징 영역 |
| `git diff --staged`(또는 `--cached`) | 스테이징 영역 ↔ 마지막 커밋(HEAD) |
| `git diff HEAD` | 작업 트리 ↔ 마지막 커밋(스테이징 여부 무관 전체 변경) |
| `git diff <commit1> <commit2>` | 임의의 두 커밋 사이 |
| `git diff branchA branchB` | 두 브랜치의 최신 커밋 사이 |

`git commit` 직전에 무엇이 실제로 기록될지 최종 확인하고 싶다면 `git diff --staged`가 정확한 답이다 — 옵션 없는 `git diff`는 이미 스테이징된 내용을 보여주지 않으므로, 이 구분을 모르면 "분명히 수정했는데 diff에 안 나온다"는 혼란으로 이어진다(05장에서 다룬 문제와 같은 원인이다).

## 종류/세부

### 특정 파일만 비교

여러 파일을 수정했을 때 특정 파일의 변경만 보고 싶다면 경로를 뒤에 덧붙인다.

```bash
git diff -- src/app.js
git diff --staged -- src/app.js
```

`--`는 이후 인자가 브랜치·커밋 이름이 아니라 파일 경로임을 명시하는 구분자로, 브랜치 이름과 파일 이름이 우연히 같을 때의 모호함을 없앤다.

### 요약만 보기

파일별 변경 줄 수만 빠르게 훑고 싶다면 전체 diff 대신 통계 요약을 쓴다.

```bash
git diff --stat
```

```
 README.md  | 2 ++
 src/app.js | 5 +++--
 2 files changed, 5 insertions(+), 2 deletions(-)
```

### 이름 변경 감지

Git은 파일을 명시적으로 "이름 변경"으로 기록하지 않고 삭제+생성으로 저장하지만(34장에서 다룰 스냅샷 모델의 결과), `git diff`는 내용이 비슷한 삭제·생성 쌍을 휴리스틱으로 찾아 이름 변경으로 표시해준다.

```bash
git diff -M    # 유사도 기준 이름 변경 감지(기본적으로도 어느 정도 활성화되어 있음)
```

```diff
diff --git a/old-name.js b/new-name.js
similarity index 95%
rename from old-name.js
rename to new-name.js
```

## 주의사항·함정

**바이너리 파일은 의미 있는 diff를 보여주지 않는다**: 이미지·컴파일된 산출물처럼 텍스트가 아닌 파일은 `git diff`가 "Binary files a/image.png and b/image.png differ"만 출력하고 내용 비교를 생략한다. 이런 파일의 버전 관리가 잦다면 40장에서 다루는 `.gitattributes`로 diff 드라이버를 별도로 지정하거나, 41장의 Git LFS를 검토하는 편이 낫다.

**대용량 파일에서 diff 계산이 느릴 수 있다**: 한 줄이 매우 긴 파일(압축된 CSS, 생성된 코드 등)이나 파일 크기 자체가 큰 경우, 줄 단위 비교 알고리즘의 계산 비용이 커져 `git diff`가 느리게 응답할 수 있다. `--stat`으로 먼저 어느 파일이 문제인지 좁힌 뒤 필요한 파일만 개별로 비교하는 방식이 실용적이다.

**색상 출력이 파이프로 넘기면 사라진다**: 터미널에서는 삭제·추가 줄이 색으로 구분되지만, `git diff | grep ...`처럼 다른 명령으로 파이프하면 기본적으로 색상 코드가 빠진다. 강제로 색을 유지하려면 `git diff --color=always`를 쓴다.

## Reference

- [git-diff Documentation](https://git-scm.com/docs/git-diff)
