# CLAUDE.md — 42jerrykim.github.io 프로젝트 규칙

Claude Code가 이 프로젝트에서 작업할 때 자동으로 읽는 규칙 파일입니다.

---

## 전역 필수 규칙 (모든 작업에 항상 적용)

@.cursor/rules/rules-that-must-be-followed.mdc

---

## 프로젝트 구조

Hugo 정적 사이트 블로그 (`42jerrykim.github.io`).

- **일반 포스트**: `content/post/<연도>/<YYYY-MM-DD-slug>/index.md`
- **컬렉션 포스트**: `content/collection/<컬렉션명>/<연도>/<폴더>/index.md`
- **태그 목록**: `data/tags.yaml`
- **퍼마링크 규칙**: `config/_default/permalinks.yaml`

내부 링크 형식: `/post/<section-slug>/<page-slug>/` — 링크 전 대상 `_index.md`의 `slug` 값을 반드시 확인할 것.

---

## 포스트 작성 스킬

### 블로그 포스트 작성 (기본 워크플로우)

@.cursor/skills/blog-post-writing/SKILL.md

@.cursor/skills/blog-post-writing/reference.md

### 전체 파이프라인 (Research → Draft → QA → PublishPrep)

@.cursor/skills/blog-agent-pipeline/SKILL.md

---

## 컬렉션별 전용 규칙

### AI 컬렉션 글 작성 표준 (모든 컬렉션 글에 적용)

@.cursor/rules/ai-collection-writing-standards.mdc

AI를 이용해 **이론 중심 + 예제 보충식** 전문가 수준의 컬렉션 글을 작성할 때 필수. 
본문 구성(문단 비율), 깊이, 정확성, 출처, 안티패턴을 다룬다.

### 컬렉션 내부 링크 (`content/collection/**/index.md` 편집 시)

@.cursor/rules/hugo-collection-internal-links.mdc

### 교육·시리즈형 글 (`content/collection/**/index.md` 편집 시)

@.cursor/rules/ai-educational-content-quality.mdc

@.cursor/skills/educational-content-writing/SKILL.md

### 영화 리뷰 (`content/collection/Movies/`)

@content/collection/Movies/.cursor/rules/movie-review-writing-rules.mdc

@.cursor/skills/movie-review-writing/SKILL.md

@.cursor/skills/movie-review-writing/reference.md

### TV 시리즈 리뷰 (`content/collection/TV-Show/`)

@content/collection/TV-Show/.cursor/rules/tv-series-review-writing-rules.mdc

### 알고리즘 (`content/collection/Algorithm/`)

@content/collection/Algorithm/.cursor/rules/algorithm-post-writing-rules.mdc

### 영단어 (`content/collection/Vocabulary/`)

@content/collection/Vocabulary/.cursor/rules/vocabulary-post-writing-rules.mdc

### Bash Shell (`content/collection/bashshell/`)

@content/collection/bashshell/.cursor/rules/bashshell-post-writing-rules.mdc

### CMD (`content/collection/cmd/`)

@content/collection/cmd/.cursor/rules/cmd-post-writing-rules.mdc

---

## 작업 유형별 라우팅

| 작업 | 적용 스킬/규칙 |
|------|--------------|
| **모든 컬렉션 글** (AI 작성) | **ai-collection-writing-standards** (필수) + 하위 규칙 |
| Movies 리뷰 작성 | movie-review-writing 스킬 + Movies 규칙 + ai-collection-writing-standards |
| TV-Show 리뷰 작성 | TV-Show 규칙 + blog-post-writing 스킬 + ai-collection-writing-standards |
| Algorithm 풀이 작성 | Algorithm 규칙 + blog-post-writing 스킬 + ai-collection-writing-standards |
| Vocabulary 단어 작성 | Vocabulary 규칙 + blog-post-writing 스킬 + ai-collection-writing-standards |
| Bash/CMD 포스트 작성 | 해당 컬렉션 규칙 + blog-post-writing 스킬 + ai-collection-writing-standards |
| 교육 시리즈 작성 | educational-content-writing 스킬 + ai-collection-writing-standards |
| 처음부터 끝까지 신규 포스트 | blog-agent-pipeline 스킬 + ai-collection-writing-standards (컬렉션 글) |
| 그 외 일반 포스트 | blog-post-writing 스킬 + 전역 규칙 |

---

## Claude Code 전용 지침

**날짜 확인** (추측 금지 — 반드시 터미널로 확인):
```powershell
Get-Date -Format "yyyy-MM-dd"
```

**링크 검증**: URL 추가 전 HTTP 접근 가능 여부 확인 필수. 404·5xx URL 추가 불가.

**배치 마크다운 개선** (선택): `script/md-improve/generate-improve-commands.ps1`
