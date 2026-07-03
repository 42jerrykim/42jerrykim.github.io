---
name: blog-post-writing
description: >-
  Hugo 블로그 포스트 작성을 위한 종합 가이드. 컬렉션/일반 포스트의 frontmatter 생성, 본문 구조 템플릿,
  SEO 최적화, 이미지/에셋 관리, 태그 선정(data/tags.yaml), 링크 검증, Mermaid 다이어그램, 한국어/영어
  이중 언어 콘텐츠를 포함한다. 블로그 글 작성, 새 컬렉션 생성, 기술 블로그 포스트 작성 시 사용한다.
  Research→Draft→QA→PublishPrep 전체 파이프라인을 한 번에 진행하려면 `blog-agent-pipeline`을 참고한다.
---

# Hugo 블로그 포스트 작성 스킬

42jerrykim.github.io Hugo 사이트에서 **모든 유형의 블로그 포스트**(컬렉션, 일반 포스트, 기술 블로그, 새 컬렉션)를 일관된 품질로 작성하기 위한 워크플로우다.

> **함께 적용**: frontmatter·Mermaid·링크 검증·날짜 확인 등 전역 필수 규칙은 [`rules-that-must-be-followed`](../rules-that-must-be-followed/SKILL.md) 스킬을 항상 함께 따른다. **제목 형식·날짜·카테고리 접두어** 상세는 [reference.md](reference.md)의 **「제목·날짜·카테고리 접두어 (전역)」** 절을 참고한다.

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

3. **컬렉션별 전용 스킬 확인**: 대상이 아래 컬렉션이면 해당 스킬을 함께 호출해 작성 규칙을 따른다.

| 컬렉션 | 전용 스킬 |
|--------|----------|
| Algorithm | [`algorithm-post-writing`](../algorithm-post-writing/SKILL.md) |
| Vocabulary | [`vocabulary-post-writing`](../vocabulary-post-writing/SKILL.md) |
| Movies | [`movie-review-writing`](../movie-review-writing/SKILL.md) |
| TV-Show | [`tv-series-review-writing`](../tv-series-review-writing/SKILL.md) |
| bashshell / cmd | [`shell-command-post-writing`](../shell-command-post-writing/SKILL.md) |

3-1. **일반 포스트(`content/post/`) 성격별 전용 스킬 확인**: 컬렉션이 아닌 자유 주제 글이면, 주제 성격에 따라 아래 스킬을 함께 호출한다.

| 글 성격 | 전용 스킬 |
|--------|----------|
| 개발·프로그래밍(언어 문법, 구현·최적화, 설계 원칙) | [`dev-programming-post-writing`](../dev-programming-post-writing/SKILL.md) |
| 시스템·인프라(OS, 가상화, 네트워킹, 보안, CI/CD·빌드) | [`systems-infra-post-writing`](../systems-infra-post-writing/SKILL.md) |
| AI·도구 활용(AI 서비스·에이전트·플러그인 가이드) | [`ai-tools-post-writing`](../ai-tools-post-writing/SKILL.md) |
| 교양·생활(역사, 과학, 자기계발, 하드웨어·기기 리뷰) | [`life-knowledge-post-writing`](../life-knowledge-post-writing/SKILL.md) |

4. **태그 후보 수집**: `data/tags.yaml` 읽어 관련 카테고리에서 태그 25개 이상 선정

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
tags:  # 25개 이상, data/tags.yaml 참조 (영/한 병용 개념은 Tag1(태그1) 형식의 단일 승인 태그 사용)
  - Tag1(태그1)
  - Tag2
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

교육·시리즈형 자료(컬렉션 `index.md`)는 [`educational-content-writing`](../educational-content-writing/SKILL.md) 스킬을 함께 호출한다:
- 학습 성과 목표 ("이 글을 읽은 후 점검해 볼 질문")
- 판단 기준 (언제 사용/피할지)
- 비판적 시각 (한계, 트레이드오프)
- **분량은 품질의 결과 (줄 수 하한 없음)**: 최소 분량 기준을 두지 않는다 — "충분한가"는 educational-content-writing §7 내용 완결성으로 판단한다. 중복 요약·답 없는 번호 리스트·작성자용 자기인증("게시 전 자가 점검" 등)·존재하지 않는 파일 참조 금지(안티패딩 원칙). 짧게 느껴지면 줄을 늘리지 말고 실제 코드·측정 수치·사례·빠진 완결성 축으로 보강한다.
- **코드는 컴파일 가능**해야 하고, "정량적"·"측정"을 표방하면 실제 수치·벤치를 포함한다.

이론 중심 컬렉션 글(`content/collection/**/index.md`)을 작성·보강할 때는 [`collection-writing-standards`](../collection-writing-standards/SKILL.md) 스킬도 함께 적용한다 (이론 우선 서술, 예제는 보충 역할).

### Phase 5: 검증

아래 체크리스트로 최종 확인:

- [ ] `draft: true` 설정됨
- [ ] title 70자 이하
- [ ] description 150자 내외
- [ ] tags 25개 이상 (`data/tags.yaml` 기반, 영/한 병용 개념은 `Tag(태그)` 형식 승인 태그 사용)
- [ ] date/lastmod가 오늘 날짜 (터미널 확인값)
- [ ] 카테고리 접두어가 올바름
- [ ] 본문 링크 전부 HTTP 접근 확인 완료 (404/5xx 없음)
- [ ] Mermaid: 노드 ID camelCase, 특수문자 라벨은 `""` 감싸기, 줄바꿈 `</br>`
- [ ] 이미지가 번들 내 존재하고 frontmatter에서 참조됨
- [ ] **컬렉션 `index.md`의 내부 링크**: [reference.md](reference.md)의 **「Hugo 컬렉션 내부 링크」** 규칙(`/post/<section-slug>/<page-slug-or-contentbasename>/`)을 따랐는가?
- [ ] (교육 글) **안티패딩**: 닫는 절(요약·FAQ·체크리스트·네비)이 종류별 1개이고, 중복 요약·답 없는 번호 리스트·"게시 전 자가 점검" 류 메타·존재하지 않는 파일 참조가 없는가?
- [ ] (기술/교육 글) **코드 컴파일 가능**(주석뿐·미정의 타입 아님), "정량적"·"측정" 주장에 **실제 수치·벤치** 동반

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
2. 영/한이 실제로 병용되는 개념은 목록에 등재된 **`Tag(태그)` 병기 형식의 단일 승인 태그**를 그대로 사용(임의로 `Tag`, `태그` 두 줄로 쪼개지 않는다 — Phase 8 통합 이후 두 줄로 쓰면 승인 목록과 표기가 어긋난다)
3. **구체적 태그** 우선 (예: `Dynamic-Programming` > `Algorithm`)
4. 주제와 **간접 관련** 카테고리도 포함 (예: Python 글에 `Coding-Test(코딩테스트)`, `Automation(자동화)` 등)
5. 최종 **25개 이상** 달성

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

기존 규칙([`rules-that-must-be-followed`](../rules-that-must-be-followed/SKILL.md))의 문법 사항을 준수하면서, 다이어그램 사용 전략:

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
- **태그**: `data/tags.yaml` 승인 태그(영/한 병용 개념은 `Tag(태그)` 형식)로 25개 이상
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
5. **전용 작성 스킬 추가 여부 판단**: Algorithm/Movies처럼 고유한 폴더명·Front Matter·본문 구조 규칙이 필요한 컬렉션이면 `.claude/skills/<컬렉션명>-post-writing/SKILL.md`를 새로 작성한다. 단순 주제별 글 모음(전용 규칙 없음)이면 생략 가능.
   - **템플릿**: `name`/`description` frontmatter를 작성하고, 본문에 아래 절을 포함한다 — 제목/메타 규칙, 날짜/버전 관리, 폴더명 규칙, Front Matter 템플릿, 본문 구조 가이드, 작성 체크리스트. 참고 템플릿: [`algorithm-post-writing`](../algorithm-post-writing/SKILL.md)(문제 풀이형) 또는 [`shell-command-post-writing`](../shell-command-post-writing/SKILL.md)(명령어 참조형)
   - **매핑 표 갱신**: 전용 스킬을 새로 만들었다면 아래 3곳의 매핑 표에 컬렉션·접두어·스킬 링크를 추가한다
     - 이 문서 §3 "컬렉션별 전용 스킬 확인" 표
     - [reference.md](reference.md)의 "기존 컬렉션 목록" 표
     - [`blog-agent-pipeline`](../blog-agent-pipeline/SKILL.md)의 "컬렉션별 작성 스킬" 표
     - 루트 `CLAUDE.md`의 "컬렉션 글 작성 시 ..." 목록

---

## 7. 추가 참고

- 컬렉션별 상세 템플릿, 태그 카테고리, **내부 링크(permalinks·slug)**, **제목·날짜**: [reference.md](reference.md)
