---
name: blog-post-writing
description: >-
  Hugo 블로그 포스트 작성을 위한 종합 가이드. 컬렉션/일반 포스트의 frontmatter 생성, 본문 구조 템플릿,
  SEO 최적화, 이미지/에셋 관리, 태그 선정(data/tags.yaml), 링크 검증, Mermaid 다이어그램, 한국어/영어
  이중 언어 콘텐츠를 포함한다. 블로그 글 작성, 새 컬렉션 생성, 기술 블로그 포스트 작성 시 사용한다.
---

# Hugo 블로그 포스트 작성 스킬

이 스킬은 42jerrykim.github.io Hugo 사이트에서 **모든 유형의 블로그 포스트**(컬렉션, 일반 포스트, 기술 블로그, 새 컬렉션)를 일관된 품질로 작성하기 위한 프레임워크다.

> **기존 규칙과의 관계**: 이 스킬은 `.cursor/rules/rules-that-must-be-followed.mdc`(alwaysApply)를 **보완**한다. frontmatter·Mermaid·링크 검증 등 전역 불변은 해당 규칙이 강제한다. **제목 형식·날짜·카테고리 접두어** 상세는 [reference.md](reference.md)의 **「제목·날짜·카테고리 접두어 (전역)」** 절을 따른다. 여기서는 **워크플로우·구조·전략**에 집중한다.
>
> **미디어 작품 한글 제목**: 영화·드라마 등은 해당 컬렉션의 `.cursor/rules/`를 따른다. 영화 리뷰의 본문·추천 작품 표기 세부는 `content/collection/Movies/.cursor/rules/movie-review-writing-rules.mdc`의 **「본문·추천 작품의 한국어 제목」** 절을 참고한다.

---

## 1. 워크플로우

포스트 작성 시 아래 단계를 순서대로 따른다.

### Phase 1: 준비

1. **날짜 확인**: 터미널에서 `Get-Date -Format "yyyy-MM-dd"` 실행
2. **콘텐츠 유형 결정**: 아래 표에서 해당하는 유형을 선택

| 유형 | 경로 | 특징 |
|------|------|------|
| **컬렉션 포스트** | `content/collection/<컬렉션명>/<연도>/<폴더>/index.md` | 시리즈/카테고리별 정리, `categories` 포함 |
| **일반 포스트** | `content/post/<연도>/<폴더>/index.md` | 단독 글, 자유 주제 |
| **새 컬렉션** | `content/collection/<새이름>/_index.md` + 하위 글 | 신규 시리즈 생성 |

3. **컬렉션별 전용 규칙 확인**: 대상 컬렉션 폴더 아래 `.cursor/rules/`가 있으면 해당 규칙을 먼저 읽는다 (각 `.mdc`는 `content/collection/<해당컬렉션>/**/*.md`용 **`globs`**가 있어, 해당 경로 편집 시 Cursor가 컨텍스트에 넣기 쉽다)
   - Algorithm → `algorithm-post-writing-rules.mdc`
   - Vocabulary → `vocabulary-post-writing-rules.mdc`
   - Movies → `movie-review-writing-rules.mdc`
   - TV-Show → `tv-series-review-writing-rules.mdc`
   - Bash Shell → `bashshell-post-writing-rules.mdc`
   - CMD → `cmd-post-writing-rules.mdc`

4. **태그 후보 수집**: `data/tags.yaml` 읽어 관련 카테고리에서 태그 50개 이상 선정

### Phase 2: 폴더 및 파일 생성

1. **폴더명 형식**: `YYYY-MM-DD-<slug-keywords>`
   - 소문자, 하이픈 구분, 영문만, 공백 없음
   - 컬렉션별 폴더명 규칙이 있으면 그것을 우선 (예: Algorithm은 `BOJ-번호` 포함)

2. **콘텐츠 번들 구조**:
```
YYYY-MM-DD-my-post-slug/
├── index.md          # 본문
├── image.png         # 대표 이미지 (또는 wordcloud.png, poster.png)
└── (기타 에셋)
```

3. **이미지 규칙**:
   - 대표 이미지는 번들 내에 배치하고, frontmatter에서 파일명만 참조: `image: "image.png"`
   - Algorithm 컬렉션은 `wordcloud.png` 사용 (wordcloud_generator.py로 생성)
   - 외부 이미지 URL 대신 번들 내 파일을 권장

### Phase 3: Frontmatter 작성

필수 필드 템플릿 (상세 템플릿은 [reference.md](reference.md) 참조):

```yaml
---
title: "[카테고리] 70자 이하 SEO 최적화 제목"
description: "150자 내외, 핵심 키워드 포함, 독자가 얻을 정보를 명확히"
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
draft: true
categories:
  - 주카테고리
tags:  # 50개 이상, 영어+한글 쌍, data/tags.yaml 참조
  - Tag1
  - 태그1
image: "image.png"
---
```

**카테고리 접두어 매핑**:

| 컬렉션 | 접두어 | 예시 |
|--------|--------|------|
| Algorithm | `[Algorithm]` | `[Algorithm] C++ 백준 1234번: 문제명` |
| Movies | `[Movie]` | `[Movie] 영화 제목 리뷰` |
| TV-Show | `[TV Series]` | `[TV Series] 드라마 제목 리뷰` |
| Vocabulary | `[Vocabulary]` | `[Vocabulary] 단어 뜻과 활용` |
| Bash Shell | `[Bash]` | `[Bash] 명령어 사용법` |
| CMD | `[CMD]` | `[CMD] 명령어 사용법` |
| 기술 블로그 | 주제에 맞게 | `[Python] 비동기 프로그래밍 가이드` |

### Phase 4: 본문 작성

#### 범용 포스트 구조

```markdown
(도입 1-2문단: 독자 훅, 주제 동기, 이 글에서 다루는 내용)

---

## 핵심 개념/배경
(용어 정의, 배경 설명 — 첫 등장 용어는 **굵게**)

## 본론 (주제에 맞게 H2 섹션 2-4개)
(설명 → 예시/코드/다이어그램 → 비교/트레이드오프)

## 실전 적용 / 예제
(코드 블록, 스크린샷, 또는 사례)

## 마무리
(핵심 요약 표 또는 체크리스트, 다음 글 링크)

## 참고 및 출처
(접근 가능한 URL만 포함)
```

#### 기술 블로그 추가 요소

- **코드 블록**: 반드시 언어 지정 (`cpp`, `python`, `bash` 등)
- **코드 앞**: 개념·목적을 2문장 이상 설명
- **코드 뒤**: 주의점·트레이드오프를 1-2문장으로 정리
- **복잡도/성능**: 표로 정리 권장

#### 교육 콘텐츠 추가 요소

교육·시리즈형 자료는 [`.cursor/skills/educational-content-writing/SKILL.md`](../educational-content-writing/SKILL.md)도 함께 따른다:
- 학습 성과 목표 ("이 글을 읽은 후 점검해 볼 질문")
- 판단 기준 (언제 사용/피할지)
- 비판적 시각 (한계, 트레이드오프)
- 최소 500줄 본문

### Phase 5: 검증

아래 체크리스트로 최종 확인:

- [ ] `draft: true` 설정됨
- [ ] title 70자 이하
- [ ] description 150자 내외
- [ ] tags 50개 이상 (영어+한글, `data/tags.yaml` 기반)
- [ ] date/lastmod가 오늘 날짜 (터미널 확인값)
- [ ] 카테고리 접두어가 올바름
- [ ] 본문 링크 전부 HTTP 접근 확인 완료 (404/5xx 없음)
- [ ] Mermaid: 노드 ID camelCase, 특수문자 라벨은 `""` 감싸기, 줄바꿈 `</br>`
- [ ] 이미지가 번들 내 존재하고 frontmatter에서 참조됨
- [ ] 내부 링크는 [reference.md](reference.md) **「Hugo 컬렉션 내부 링크」** (`/post/<section-slug>/<page-slug-or-contentbasename>/`)

---

## 2. SEO 최적화 가이드

### Title

- **70자 이하** 엄수
- **카테고리 접두어** + **핵심 키워드** 배치
- 독자가 검색할 법한 자연어 포함 (예: "사용법", "가이드", "리뷰", "풀이")

### Description

- **150자 내외**로 작성
- 글의 핵심 가치를 명확히 전달
- 주요 키워드 1-2개 자연스럽게 포함
- "이 글에서는 ~를 다룹니다" 식의 직접적 표현 권장

### Tags

태그 선정 전략 (상세 카테고리 목록은 [reference.md](reference.md) 참조):

1. `data/tags.yaml`에서 해당 주제의 **직접 관련 카테고리** 태그 선정
2. **영어+한글 쌍**으로 작성하여 양쪽 검색 커버
3. **구체적 태그** 우선 (예: `Dynamic-Programming` > `Algorithm`)
4. 주제와 **간접 관련** 카테고리도 포함 (예: Python 글에 `코딩테스트`, `자동화` 등)
5. 최종 **50개 이상** 달성

---

## 3. 이미지/에셋 관리

| 상황 | 방법 |
|------|------|
| 대표 이미지 | 번들 내 `image.png` 또는 컬렉션별 규칙 파일 참조 |
| 본문 삽입 이미지 | `![alt text](파일명.png)` — 번들 내 상대 경로 |
| 워드클라우드 (Algorithm) | `python script/wordcloud_generator.py "<번들 경로>"` |
| 외부 이미지 | 가능한 한 다운로드 후 번들에 포함. 불가능 시 접근 확인 후 URL 사용 |

---

## 4. Mermaid 다이어그램

기존 규칙의 문법 사항을 준수하면서, 다이어그램 사용 전략:

| 다이어그램 유형 | 적합한 콘텐츠 |
|----------------|--------------|
| `flowchart TD` | 알고리즘 로직, 의사결정, 워크플로우 |
| `sequenceDiagram` | API 호출 흐름, 시스템 간 통신 |
| `classDiagram` | 디자인 패턴, 객체 구조 |
| `stateDiagram-v2` | 상태 머신, 라이프사이클 |
| `gantt` | 프로젝트 타임라인, 학습 로드맵 |
| `graph LR` | 개념 관계도, 의존성 |

---

## 5. 한국어/영어 이중 언어 전략

사이트 기본 언어는 **한국어(ko)**이다.

- **본문**: 한국어로 작성
- **기술 용어**: 첫 등장 시 **영어(한국어)** 형태로 병기, 이후 한국어 사용
  - 예: **Dynamic Programming(동적 계획법)**은 ... 이후 "동적 계획법"으로 표기
- **코드/명령어**: 원문(영어) 그대로 사용
- **태그**: 영어+한글 쌍으로 50개 이상
- **인용문**: 원문 유지 후 한국어 번역 병기 가능

---

## 6. 새 컬렉션 생성

기존 컬렉션에 해당하지 않는 새 시리즈를 만들 때:

1. `content/collection/<새이름>/` 디렉터리 생성
2. `_index.md` 작성 (메타데이터만, 본문 최소화):
```yaml
---
title: "컬렉션 제목"
description: "150자 설명"
slug: "kebab-case-slug"
---
```
3. **00 챕터** 생성하여 소개/커리큘럼 배치 (`collection_order: 0`)
4. 각 챕터에 `collection_order` 순번 부여
5. (선택) 컬렉션 전용 `.cursor/rules/` 작성 규칙 생성

---

## 7. 추가 참고

- 컬렉션별 상세 템플릿, 태그 카테고리, **내부 링크(permalinks·slug)**, **제목·날짜**: [reference.md](reference.md)
- 컬렉션 `index.md` 편집 시 자동 트리거: `.cursor/rules/hugo-collection-internal-links.mdc` → 위 reference의 **「Hugo 컬렉션 내부 링크」** 준수
- 교육·시리즈형 품질(분량·00 챕터·체크리스트): [`.cursor/skills/educational-content-writing/SKILL.md`](../educational-content-writing/SKILL.md) — 트리거 규칙: `.cursor/rules/ai-educational-content-quality.mdc`
