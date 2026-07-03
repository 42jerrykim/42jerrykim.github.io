---
name: ai-tools-post-writing
description: >-
  content/post/ 하위 AI 도구·서비스 활용 글(Claude Code, ChatGPT, Cursor, AI 에이전트·플러그인·워크플로
  가이드) 작성 가이드. 아키텍처/기능 설명·적용 시나리오·판단 기준·장단점 구조와 태그·체크리스트를 표준화한다.
  content/post/ 하위 AI 도구·서비스 소개·활용 가이드 글 작성 시 사용한다.
---

# AI·도구 활용 포스트 작성 가이드 (content/post/)

`content/post/<연도>/`에 실리는 **AI 도구·서비스 활용 글**(Claude Code 설정, ChatGPT/Cursor 활용법, AI 에이전트·플러그인 소개, 리서치 도구 리뷰 등)을 작성할 때 따르는 가이드다. [`blog-post-writing`](../blog-post-writing/SKILL.md), [`rules-that-must-be-followed`](../rules-that-must-be-followed/SKILL.md)과 함께 적용한다.

**적용 예시**: `everything-claude-code`(설정 모음 소개), `insane-research-claude-code-deep-research-plugin`(플러그인 리뷰), AI 코딩 에이전트·프롬프트 엔지니어링 활용 가이드.

---

## 1. 제목/메타 규칙

- **카테고리 접두어**: `[AI]` 사용 (세부 도구명이 핵심이면 `[Claude Code]`, `[ChatGPT]` 등으로 대체 가능)
- **메인 제목**: `{도구/프로젝트명}: {핵심 가치 요약}` 형태. 예: `[AI] Everything Claude Code: 강력한 AI 코딩 에이전트 설정 가이드`
- **총 길이**: 70자 이내

## 2. 날짜/폴더 규칙

- 경로: `content/post/<연도>/YYYY-MM-DD-<영문-슬러그>/index.md`
- `date`/`lastmod`는 작성/수정 당일. 도구가 빠르게 변하는 분야이므로, 버전·업데이트 반영 시 `lastmod` 갱신을 특히 신경 쓴다.
- 폴더 슬러그: 도구명+핵심 키워드 (예: `everything-claude-code`, `insane-research-claude-code-deep-research-plugin`).

## 3. Front Matter 템플릿

```yaml
---
title: "[AI] 도구/프로젝트명: 핵심 가치 요약"
description: "제작자/출처와 도구의 핵심 기능을 1문장, 이 글이 다루는 항목(아키텍처·적용 기준·장단점 등)을 1-2문장으로. 150자 내외."
date: YYYY-MM-DDTHH:MM:SS+09:00
lastmod: YYYY-MM-DD
categories:
  - AI
tags:  # 50개 이상, 영어+한글 쌍
  - AI
  - 인공지능
image: "image.png"
---
```

## 4. 본문 구조 가이드

실제 게시 글(`everything-claude-code` 등)에서 관찰되는 "소개 → 구조 → 기능 → 판단 기준 → 평가" 구조:

1. **개요**: 도구 정보(제작자·출처·버전)와 추천 대상을 1-2문단으로.
2. **아키텍처/구조**: 도구를 구성하는 핵심 요소(에이전트·훅·명령어 등)를 개념 수준에서 먼저 문단으로 설명.
3. **주요 기능 상세**: 요소별 H3 하위 절로 분해, 각 기능의 목적·동작 방식·간단한 사용 예시.
4. **왜 사용해야 할까 — 실제 이점**: 도입 전/후 차이, 해결하는 구체적 문제를 서술.
5. **적용 시나리오와 판단 기준**: 어떤 팀/상황에 적합한지, 언제 과한 도구인지 판단 기준을 제시(무조건 추천 금지).
6. **장단점과 종합 평가**: 한계·리스크(보안, 학습 곡선, 벤더 종속 등)를 반드시 포함.
7. **시작하기**: 설치·설정 최소 단계 (재현 가능하게).
8. **참고 문헌**: 공식 저장소·문서 링크(접근 확인 필수).

- **과장 금지**: "무조건 좋다"류 단정 대신, 한계·트레이드오프를 반드시 균형 있게 다룬다.
- **재현성**: 설정 예시·명령은 실제로 실행 가능한 형태로 제공한다.
- **출처 신뢰도**: 도구 제작자·저장소·버전을 명시해 검증 가능하게 한다.

## 5. 태그 전략

`data/tags.yaml`의 `ai_and_data`, `devops_and_tools`, `general_topics` 카테고리에서 50개 이상 선정. 도구명(Claude Code, ChatGPT, Cursor)과 개념(Prompt-Engineering/프롬프트엔지니어링, Automation/자동화)을 영어+한글 쌍으로 채운다.

## 6. 작성 체크리스트

- [ ] 경로가 `content/post/<연도>/YYYY-MM-DD-<슬러그>/index.md`인가?
- [ ] title 70자 이내, description 150자 내외인가?
- [ ] tags 50개 이상(영어+한글)인가?
- [ ] `draft: true`(신규 글), date/lastmod가 오늘 날짜인가?
- [ ] "개요 → 아키텍처 → 기능 상세 → 적용 시나리오/판단 기준 → 장단점" 구조를 따랐는가?
- [ ] **판단 기준**(언제 적합/부적합)과 **한계·리스크**를 반드시 다뤘는가? (무조건 추천 금지)
- [ ] 설치/설정 단계가 그대로 재현 가능한가?
- [ ] 도구 제작자·저장소·버전을 명시했는가?
- [ ] 참고 문헌 링크가 접근 가능한가?
