# CLAUDE.md — 42jerrykim.github.io

**프로젝트**: Hugo 블로그 (`42jerrykim.github.io`)

## 핵심 규칙

- **구조**: `content/post/<연도>/` 또는 `content/collection/<컬렉션>/<연도>/`
- **파일**: `YYYY-MM-DD-slug/index.md` (대표이미지 `image.png` 함께)
- **내부 링크**: `/post/<section-slug>/<page-slug>/` (대상 `_index.md`의 `slug` 확인)
- **날짜**: 터미널에서 `Get-Date -Format "yyyy-MM-dd"` 확인
- **링크 검증**: HTTP 접근 확인 필수 (404/5xx 불가)
- **tags**: 50개 이상, `data/tags.yaml` 기반

## 작업별 가이드

- **일반 포스트**: 자유 주제, `content/post/<연도>/`
- **컬렉션 포스트**: frontmatter에 `categories` 포함, 필요 시 `collection_order` 지정
- **새 컬렉션**: `_index.md` + 00 챕터 생성
- **시리즈**: 선후 관계/커리큘럼 명시, 학습 목표 포함

## 상세 규칙이 필요할 때

필요한 규칙·스킬을 명시적으로 요청하면 로드합니다:
- `/blog-post-writing` — 포스트 작성 가이드
- `/educational-content-writing` — 교육 콘텐츠 품질  
- `/movie-review-writing` — 영화 리뷰
- `rules-that-must-be-followed` — 전역 규칙 (frontmatter, Mermaid, 링크 등)
