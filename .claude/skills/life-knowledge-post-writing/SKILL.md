---
name: life-knowledge-post-writing
description: >-
  content/post/ 하위 교양·생활 글(역사, 과학, 자기계발, 하드웨어·기기 리뷰 등 비기술 실무 주제) 작성 가이드.
  스토리텔링형 서술, 타임라인·비교, 출처 기반 사실 검증, 기기 리뷰형 장단점 구조와 태그·체크리스트를 표준화한다.
  content/post/ 하위 역사·과학·자기계발·기기 리뷰 글 작성 시 사용한다.
---

# 교양·생활 포스트 작성 가이드 (content/post/)

`content/post/<연도>/`에 실리는 **교양·생활 글**(역사, 과학·수학 교양, 자기계발, 자전거·노트북 등 하드웨어 기기 리뷰)을 작성할 때 따르는 가이드다. 개발/인프라 실무 지식이 아니라 **읽을거리·의사결정 참고 자료** 성격의 글에 적용한다. [`blog-post-writing`](../blog-post-writing/SKILL.md), [`rules-that-must-be-followed`](../rules-that-must-be-followed/SKILL.md)과 함께 적용한다.

**적용 예시**: `history-of-calendars-fascinating-story`(역사 교양), `quantum-computing-bitcoin-threat`(과학/보안 교양), `four-pillars-of-success-park-yonghoo`(자기계발), `cannondale-smartsense-gen2-cycling-safety`·`surface-go-1st-gen-linux-install-guide`(기기 리뷰·가이드).

이 스킬은 두 하위 유형(**역사·과학·자기계발형**, **기기 리뷰형**)을 함께 다루며, 본문 구조는 §4에서 유형별로 나눈다.

---

## 1. 제목/메타 규칙

- **카테고리 접두어**: 주제 성격으로 표기. 예: `[History]`, `[Science]`, `[Cycling]`, `[Hardware]`
- **메인 제목**: 역사/과학형은 "주제: 흥미 유발 부제"(예: `[History] 달력의 재미난 역사: 인류가 시간을 길들인 1만 년`), 기기 리뷰형은 "제품명: 핵심 특징 요약"(예: `[Cycling] Cannondale SmartSense Gen2: 자전거 안전 기술의 진화`)
- **총 길이**: 70자 이내

## 2. 날짜/폴더 규칙

- 경로: `content/post/<연도>/YYYY-MM-DD-<영문-슬러그>/index.md`
- `date`/`lastmod`는 작성/수정 당일. 기기 리뷰는 후속 펌웨어/모델 변경 시 `lastmod` 갱신.
- 폴더 슬러그: 주제/제품 핵심 키워드 (예: `history-of-calendars-fascinating-story`, `cannondale-smartsense-gen2-cycling-safety`).

## 3. Front Matter 템플릿

```yaml
---
title: "[카테고리] 주제/제품명: 부제 또는 핵심 요약"
description: "다루는 시대/주제 또는 제품의 핵심 특징을 1문장, 이 글에서 얻을 정보(타임라인, 비교, 장단점 등)를 1-2문장으로. 150자 내외."
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
categories:
  - 주제분류  # 예: History, Science, Cycling
  - 보조분류
tags:  # 25개 이상, 영/한 병용 개념은 Tag(태그) 형식
  - Tutorial
  - 가이드
image: "image.png"
---
```

## 4. 본문 구조 가이드

### 4.1 역사·과학·자기계발형

실제 게시 글(`history-of-calendars-fascinating-story` 등)에서 관찰되는 구조:

1. **개요**: 다루는 시대/주제 범위를 1-2문단으로.
2. **핵심 사건/개념 전개**: 시간순 또는 논리 전개 순으로 H2 절을 나누고, 각 절은 **연도·인물·1차 출처**를 명시한다.
3. **타임라인 또는 비교 구조**: 사건이 많으면 타임라인 절이나 표로 흐름을 요약해 독자가 전체 구조를 먼저 훑게 한다.
4. **의미/시사점**: 사실 나열에 그치지 않고, 현재에 주는 의미나 남은 논쟁을 서술한다.
5. **종합 정리 및 참고 문헌**: 핵심 요약 + 1차/2차 출처.

### 4.2 기기·제품 리뷰형

실제 게시 글(`cannondale-smartsense-gen2-cycling-safety` 등)에서 관찰되는 구조:

1. **개요**: 제품 정보 요약(모델명·핵심 스펙) + 추천 대상.
2. **핵심 구성요소/기능**: 요소별 H3 하위 절, 각 절에 이전 모델·경쟁 제품 대비 차이를 명시.
3. **비교(구모델/경쟁 제품)**: 표로 스펙·기능 차이를 정리.
4. **활용 가이드**: 연동·설정·페어링 등 실사용 단계별 설명.
5. **주요 Q&A**: 구매 전 흔한 질문에 답변 형식으로.
6. **종합 평가**: 장점/단점/한 줄 평.
7. **참고 자료**: 공식 스펙 페이지·리뷰 등.

- **사실 검증**: 역사·과학형은 연도·인물·수치를 추측하지 않는다 — 불확실하면 "~라고 알려져 있다"로 완화하고, 출처(저자·연도·문헌)를 반드시 남긴다.
- **균형**: 기기 리뷰형은 장점만 나열하지 않고 단점을 반드시 포함한다.
- **스토리텔링**: 역사·과학형은 사실 나열보다 인과관계·서사 흐름으로 서술해 읽는 재미를 준다.

## 5. 태그 전략

`data/tags.yaml`의 `general_topics` 및 주제별 카테고리(역사=`Culture`/역사 관련, 과학=`ai_and_data`/`system_and_low_level`와 무관하면 일반, 기기=하드웨어 관련)에서 25개 이상 선정. 주제 고유명사(제품명, 인물명, 사건명)와 병기 승인 태그(Tag(태그) 형식)로 채운다.

## 6. 작성 체크리스트

- [ ] 경로가 `content/post/<연도>/YYYY-MM-DD-<슬러그>/index.md`인가?
- [ ] title 70자 이내, description 150자 내외인가?
- [ ] tags 25개 이상(`data/tags.yaml` 승인 태그)인가?
- [ ] `draft: true`(신규 글), date/lastmod가 오늘 날짜인가?
- [ ] (역사·과학형) 연도·인물·수치에 출처가 있고, 불확실한 부분은 완화 표현을 썼는가?
- [ ] (역사·과학형) 타임라인/비교 구조로 전체 흐름을 먼저 보여주는가?
- [ ] (기기 리뷰형) 이전 모델·경쟁 제품과의 비교표가 있는가?
- [ ] (기기 리뷰형) 장점과 단점을 균형 있게 다뤘는가?
- [ ] 참고 자료/문헌 링크가 접근 가능한가?
