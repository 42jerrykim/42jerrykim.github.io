---
name: blog-agent-pipeline
description: >-
  Cursor IDE에서 Hugo 블로그 글을 끝까지 작성하는 멀티스테이지 파이프라인. Research(자료·링크 검증) →
  Draft(blog-post-writing 준수) → QA(메타·Mermaid·링크) → PublishPrep(draft 해제 전 최종 확인) 순으로
  한 채팅에서 순차 실행한다. 블로그 에이전트·파이프라인·하네스 워크플로·신규 포스트 전 과정에 사용한다.
---

# 블로그 작성 에이전트 파이프라인 (Cursor IDE)

이 스킬은 **한 번의 에이전트 세션**에서 아래 네 단계를 **순서대로** 수행하도록 지시한다. 각 단계가 끝날 때마다 짧은 **단계 요약**(산출물, 미해결 이슈, 다음 단계 입력)을 사용자에게 보고한다.

> **관계**: 전역 규칙은 `.cursor/rules/rules-that-must-be-followed.mdc`가 우선한다. 초안 구조·경로·태그 전략은 [`.cursor/skills/blog-post-writing/SKILL.md`](../blog-post-writing/SKILL.md) 및 [`reference.md`](../blog-post-writing/reference.md)를 따른다.

---

## 시작 전 필수 읽기 (매 파이프라인 실행 시)

에이전트는 파일을 수정하기 **전에** 아래를 읽는다 (이미 세션에 있으면 생략 가능).

| 우선순위 | 경로 | 용도 |
|----------|------|------|
| 필수 | `.cursor/rules/rules-that-must-be-followed.mdc` | draft, tags, description, title, 날짜, 링크 검증, Mermaid |
| 필수 | `.cursor/skills/blog-post-writing/SKILL.md` | 경로, frontmatter, 본문 구조, 검증 체크리스트 |
| 필수 | `.cursor/skills/blog-post-writing/reference.md` | 제목·날짜·접두어, Hugo 내부 링크 |
| 필수 | `data/tags.yaml` | tags 50개 이상 선정 |
| 조건부 | `.cursor/rules/hugo-collection-internal-links.mdc` | 컬렉션 `index.md` 등 내부 링크 편집 시 |
| 조건부 | 대상 포스트가 속한 컬렉션의 `.cursor/rules/*.mdc` | 아래 표 참고; 각 파일은 `globs`로 해당 컬렉션 `**/*.md`에 자동 연결됨 |
| 조건부 | `.cursor/skills/educational-content-writing/SKILL.md` | optimization·designpattern 등 교육 시리즈 트랙 글 |
| 조건부 | `.cursor/skills/movie-review-writing/SKILL.md` | Movies 컬렉션 영화 리뷰 |

**컬렉션별 규칙 파일 (해당 경로 under `content/collection/`일 때만 읽기)**

| 컬렉션 폴더 | 규칙 파일 |
|-------------|-----------|
| `Algorithm/` | `Algorithm/.cursor/rules/algorithm-post-writing-rules.mdc` |
| `Vocabulary/` | `Vocabulary/.cursor/rules/vocabulary-post-writing-rules.mdc` |
| `Movies/` | `Movies/.cursor/rules/movie-review-writing-rules.mdc` |
| `TV-Show/` | `TV-Show/.cursor/rules/tv-series-review-writing-rules.mdc` |
| `bashshell/` | `bashshell/.cursor/rules/bashshell-post-writing-rules.mdc` |
| `cmd/` | `cmd/.cursor/rules/cmd-post-writing-rules.mdc` |

**참고 (Cursor Rules)**: 위 `.mdc`들은 워크스페이스 루트 기준 `globs`가 설정되어 있어, 해당 컬렉션 하위 `.md`를 열거나 편집할 때 Agent 컨텍스트에 포함되기 쉽다. 다른 경로만 다루는 채팅에서는 `@movie-review-writing-rules` 등으로 규칙을 명시하거나, 관련 포스트 파일을 컨텍스트에 포함한다.

---

## Stage 1 — Research

**목적**: 주제에 맞는 근거·용어·참고 자료를 모으고, **본문에 넣을 URL만** 남긴다.

**입력**: 사용자가 제공한 주제, 컬렉션 유형(또는 일반 포스트), 선택 키워드.

**산출물**

1. **검증된 링크 목록**: 각 URL에 대해 HTTP(또는 브라우저·fetch 도구)로 접근 가능함을 확인한 것만 포함. 404·5xx·차단 시 제외하거나 대체 URL 명시.
2. **작성 메모**: 목차 초안, 반드시 넣을 섹션, 인용·수치 출처, 피해야 할 주장.
3. **경로 결정**: `content/post/<연도>/` vs `content/collection/<컬렉션>/<연도>/`, 폴더명 `YYYY-MM-DD-<slug>` (컬렉션별 예외는 해당 규칙 따름).

**체크리스트**

- [ ] 날짜는 추측하지 않음 — 이후 Draft에서 터미널로 `Get-Date -Format "yyyy-MM-dd"` 확인 예정임을 메모에 명시.
- [ ] 외부 링크는 **검증 후** 목록에만 포함.
- [ ] Movies/TV-Show 등은 해당 컬렉션 규칙에서 요구하는 조사 항목(출처 수 등)을 메모에 반영.

**단계 종료 보고**: 검증 링크 개수, 메모 요약, 선택한 콘텐츠 경로.

---

## Stage 2 — Draft

**목적**: `index.md` 초안을 저장소에 생성하거나 갱신한다.

**입력**: Stage 1 산출물.

**행동**

1. 터미널에서 오늘 날짜 확인 후 `date` / `lastmod`에 사용.
2. `blog-post-writing`의 Phase 2~4에 따라 폴더·`index.md`·에셋 생성.
3. Frontmatter: **`draft: true`**, title ≤70자, description ~150자, tags ≥50 (영·한, `data/tags.yaml` 기반), `categories` 등 컬렉션 요구 필드 반영.
4. 알고리즘 코드 블록이 있으면 전역 규칙대로 상단 주석 포함.
5. Mermaid 사용 시 `rules-that-must-be-followed` 문법 준수.
6. 본문에 넣는 모든 외부 링크는 **추가 시점에** 다시 접근 가능 여부 확인.

**교육 시리즈·특수 컬렉션**: `educational-content-writing`, `movie-review-writing` 등 조건부 스킬을 이 단계에서 함께 적용.

**체크리스트 (초안 완료 시)**

- [ ] `draft: true`
- [ ] title / description / tags 개수·형식
- [ ] 날짜 = 터미널 확인값
- [ ] 본문 링크 검증 완료
- [ ] 내부 링크는 `reference.md`의 Hugo 컬렉션 내부 링크 규칙 준수

**단계 종료 보고**: 생성·수정한 파일 경로 목록, 미완료 에셋(이미지·워드클라우드 등) 여부.

---

## Stage 3 — QA

**목적**: 규칙 위반·누락을 수정한다. **새 주장·새 링크 대량 추가는 하지 않는다** (필요 시 Research로 되돌리라고 사용자에게 안내).

**입력**: Stage 2에서 확정한 `index.md` 경로.

**행동**

1. `blog-post-writing` § Phase 5 체크리스트를 전항목 점검.
2. Mermaid 노드 ID·따옴표·`</br>` 규칙 재확인.
3. 본문·참고의 **모든 외부 URL** 재검증 (깨진 링크 제거 또는 대체).
4. 컬렉션 규칙의 체크리스트(영화 리뷰 Act 구조, Vocabulary 섹션 등)가 있으면 전부 대조.

**체크리스트**

- [ ] Phase 5 항목 전부 통과
- [ ] 컬렉션 전용 규칙 체크리스트 통과
- [ ] 교육 글인 경우 `educational-content-writing` 분량·구조 요구 충족

**단계 종료 보고**: 수정한 항목 요약, 남은 리스크(선택).

---

## Stage 4 — PublishPrep

**목적**: 배포 직전 **사람이 검토**했다는 전제 하에 `draft: false` 전환만 안내하거나 수행한다.

**원칙**

- 사용자가 명시적으로 “배포해 줘 / draft 해제”를 요청하지 않으면 **`draft: true`를 유지**한다.
- 해제 시 `lastmod`를 터미널 오늘 날짜로 갱신한다.

**체크리스트**

- [ ] Stage 3 QA 완료 확인
- [ ] 사용자 승인 후에만 `draft: false`

**단계 종료 보고**: 최종 상태(`draft` 값), 권장 후속 작업(로컬 `hugo` 빌드 등).

---

## 오케스트레이션 규칙

1. 사용자가 “Research만” 또는 “Draft부터”처럼 범위를 지정하면 **해당 단계부터** 시작한다.
2. 기본은 **1 → 2 → 3**까지 자동 진행하고, **4는 사용자 요청 시에만** 수행한다.
3. 중간에 규칙과 충돌하면 **전역 규칙**을 따르고, 스킬과의 차이를 보고에 한 줄 명시한다.
