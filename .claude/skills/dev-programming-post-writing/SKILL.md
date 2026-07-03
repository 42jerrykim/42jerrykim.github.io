---
name: dev-programming-post-writing
description: >-
  content/post/ 하위 개발·프로그래밍 단발 글(언어 문법, 라이브러리·구현 최적화, 설계/구현 기법, S-expression·정규식·OOP
  등) 작성 가이드. 컬렉션(Algorithm/Vocabulary 등)에 속하지 않는 자유 주제 프로그래밍 글의 제목·태그·본문 구조·체크리스트를
  표준화한다. content/post/ 하위 프로그래밍/언어/구현 주제 글 작성 시 사용한다.
---

# 개발·프로그래밍 포스트 작성 가이드 (content/post/)

`content/post/<연도>/`에 실리는 **자유 주제 개발·프로그래밍 글**(언어 문법 해설, 자료구조·라이브러리 구현, 최적화 기법, 설계 원칙 등)을 작성할 때 따르는 가이드다. `content/collection/Algorithm/`(BOJ 문제 풀이)이나 `content/collection/Vocabulary/`처럼 전용 컬렉션이 이미 있는 주제는 각각 [`algorithm-post-writing`](../algorithm-post-writing/SKILL.md) 등 해당 스킬을 따르고, 이 스킬은 **컬렉션에 속하지 않는 단발 프로그래밍 글**에 적용한다. [`blog-post-writing`](../blog-post-writing/SKILL.md), [`rules-that-must-be-followed`](../rules-that-must-be-followed/SKILL.md)과 함께 적용한다.

**적용 예시**: 언어 문법/개념 해설(S-expression, 정규식), 라이브러리·자료구조 직접 구현과 최적화(메모리 최적화, 캐시 친화적 구조), 설계 원칙(OOP, Clean Code), 특정 언어 생태계 가이드(Python/C#/C++/.NET) 중 시리즈가 아닌 단발 글.

---

## 1. 제목/메타 규칙

- **카테고리 접두어**: 다루는 언어·주제로 대괄호 표기. 예: `[Programming]`, `[Python]`, `[CSharp]`, `[Cpp]`, `[.NET]`, `[Algorithm]`(컬렉션이 아닌 단발 알고리즘/자료구조 글일 때)
- **메인 제목**: 핵심 개념 + 부제(콜론 또는 대시로 연결). 예: `[Programming] S-expression 문법: dotted pair부터 quasiquote까지`, `[CSharp] SO 라이브러리 메모리 최적화`
- **총 길이**: 70자 이내

## 2. 날짜/폴더 규칙

- 경로: `content/post/<연도>/YYYY-MM-DD-<영문-슬러그>/index.md`
- `date`/`lastmod`는 작성/수정 당일(로컬 타임존, `Get-Date -Format "yyyy-MM-dd"`). 의미 있는 개정 시 `lastmod` 갱신
- 폴더 슬러그: 핵심 키워드를 소문자·하이픈으로 (예: `s-expression-syntax`, `so-library-memory-optimization`)

## 3. Front Matter 템플릿

```yaml
---
title: "[Programming] 핵심 개념: 부제"
description: "핵심 개념 정의와 이 글이 다루는 범위(문법/구현/최적화 등)를 1문장, 다루는 세부 항목을 2-3문장으로 나열. 150자 내외."
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
categories:
  - 주제분류  # 예: Programming, Python, CSharp
  - 보조분류  # 예: Language, Data-Structures, Optimization
tags:  # 25개 이상, 영/한 병용 개념은 Tag(태그) 형식
  - Programming
  - 프로그래밍
image: "image.png"
---
```

## 4. 본문 구조 가이드

실제 게시 글(`s-expression-syntax`, `so-library-memory-optimization` 등)에서 관찰되는 구조:

1. **개요**: 다루는 개념의 정의와 이 글의 범위를 1-2문단으로.
2. **핵심 개념/원리**: 용어 정의(첫 등장 시 **굵게**) → 원리·구조 설명(문단 중심) → 필요 시 표/다이어그램으로 보조.
3. **세부 문법·구현 치트시트 또는 단계별 구현**: H3 하위 절로 유형별/단계별 분해. 각 절 코드 블록 앞에 목적을 2문장 이상 설명.
4. **비교/차이 (해당 시)**: 언어·구현체·버전 간 차이를 표로 정리 (예: Scheme vs Common Lisp vs Clojure 리더 문법 차이).
5. **실전 팁: 자주 하는 실수**: 흔한 오해·함정을 번호 매겨 각 1-2문장 근거와 함께 제시 (답 없는 나열 금지).
6. **요약**: 핵심 메시지를 1문단 또는 표로.
7. **참고 자료**: 접근 가능한 1차 출처(언어 스펙, 공식 문서) 우선.

- **코드 블록**: 반드시 언어 지정. 컴파일/실행 가능해야 하며 미정의 타입·주석뿐 블록으로 핵심을 대체하지 않는다.
- **정량 주장**: "몇 배 빠르다" 등은 실제 벤치 수치(플랫폼·플래그 명시) 또는 "구현 정의"로 완화한다.

## 5. 태그 전략

`data/tags.yaml`의 `programming_languages`, `code_quality`, `software_engineering`, `data_structures`, `complexity_analysis`, `general_topics` 카테고리에서 25개 이상 선정. 다루는 언어(예: Python, C++)와 병기 승인 태그(예: Recursion(재귀), Compiler(컴파일러))로 채운다.

## 6. 작성 체크리스트

- [ ] 경로가 `content/post/<연도>/YYYY-MM-DD-<슬러그>/index.md`인가?
- [ ] title 70자 이내, description 150자 내외인가?
- [ ] tags 25개 이상(`data/tags.yaml` 승인 태그)이고 무관한 보일러플레이트 태그가 없는가?
- [ ] `draft: true`(신규 글), date/lastmod가 오늘 날짜인가?
- [ ] 핵심 코드 블록이 언어 지정 + 컴파일/실행 가능한가?
- [ ] "자주 하는 실수"류 절에 각 항목마다 근거가 있는가? (답 없는 리스트 금지)
- [ ] 정량 주장에 실제 수치 또는 "구현 정의" 표기가 있는가?
- [ ] 참고 자료가 1차 출처 우선이고 링크가 접근 가능한가?
- [ ] 이미 전용 컬렉션(Algorithm/Vocabulary 등)이 있는 주제라면 이 스킬 대신 해당 컬렉션 스킬을 따랐는가?
