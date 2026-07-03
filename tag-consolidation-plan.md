---
title: 태그 파편화 분석 및 통합 계획
date: 2026-07-03
status: Phase 1·2 실행 완료 (script/normalize_tags.py), Phase 3·4 대기
---

## 실행 결과 (2026-07-03)

- Phase 1 (승인 태그의 대소문자/하이픈 변형 병합, 135건): 178개 파일 수정, 중복 15줄 제거
- Phase 2 (미승인 표기 통일 + `data/tags.yaml` 신규 승인 태그 64개 추가, 63건 매핑): 약 100개 파일 수정
- 결과: 고유 태그 3,876개 → **3,687개**, 1회성 태그 2,928개 → **2,811개**, 승인 태그 커버리지 93.6% → **95.4%**
- 사용한 스크립트: `script/normalize_tags.py`(적용기), `script/tag_normalization_phase1_mapping.json` / `script/tag_normalization_phase2_mapping.json`(매핑 근거, 감사용으로 보존)
- 모든 변경 후 `content/**/index.md` 1,324개 frontmatter가 YAML로 정상 파싱됨을 확인. 대소문자 정규화 과정에서 우연히 발견된 기존 완전 중복 태그(같은 파일 내 동일 태그 2회 기입)도 함께 정리됨.
- Phase 3(포스트당 연결 태그 최소 보장 룰)과 Phase 4(린트/CI 검사)는 아직 미실행 — 사람 판단이 더 필요한 정책 변경이라 별도 확인 후 진행 권장.

## 1. 현황 데이터

- 분석 대상: `content/**/index.md` 1,350개 파일 중 frontmatter 파싱 성공 1,324개 (draft 381개 포함)
- 태그 없는 포스트: 61개
- 고유 태그 수: **3,876개**
- 전체 태그 사용 횟수: 76,081회 (포스트당 평균 57.5개 — `rules-that-must-be-followed`의 "50개 이상" 규칙에 부합)
- **1회만 사용된 태그: 2,928개 (전체 고유 태그의 75.5%)**
- `data/tags.yaml` 승인 태그: 562개 (실사용 551개, 사용량 71,238회 = 전체 사용량의 93.6%)
- 승인 목록 밖 태그: 3,325개 (고유 태그 수의 85.8%)이지만 사용량은 4,843회(6.4%)뿐

### 해석

`data/tags.yaml` 승인 태그 체계 자체는 이미 실사용의 93.6%를 커버하고 있어 잘 작동 중이다. **파편화는 승인 목록 밖의 롱테일(3,325개, 대부분 1회성)에 집중**되어 있으며, 크게 세 원인으로 나뉜다.

## 2. 파편화 원인 분류

### 원인 A — 대소문자/표기 불일치 (스크립트로 즉시 수정 가능, 최우선)

같은 개념인데 대문자 승인형과 소문자 변형이 공존한다. 정규화(소문자·하이픈 제거) 기준으로 **182개 그룹**이 중복. 사용량 상위 예시:

| 승인형(횟수) | 비승인 변형(횟수) |
|---|---|
| Testing (720) | testing (41) |
| Debugging (526) | debugging (52) |
| Security (261) | security (46) |
| Pitfalls (320) | pitfalls (47) |
| Refactoring (482) | refactoring (36) |
| Deployment (350) | deployment (32) |
| Networking (205) | networking (34) |
| Concurrency (110) | concurrency (34) |
| Database (74) | database (34) |
| Backend (272) | backend (31) |
| Web (349) | web (33) |
| Async (67) | async (35) |
| OOP (129) | oop (35) |
| Clean-Code (556) | clean-code (33) |
| Logging (159) | logging (38) |

이 변형들은 Hugo 태그 페이지(`/tags/testing/` vs `/tags/Testing/`)를 분리시켜, 같은 개념의 글을 서로 다른 태그 페이지로 갈라놓는다. 즉 "연결 역할"을 가장 직접적으로 해치는 유형.

> 참고: `Documentation`/`문서화`, `Testing`/`테스트`처럼 영·한 병기는 `data/tags.yaml` 설계상 의도된 것(주석: "Korean equivalents are listed as separate approved tags")이므로 병합 대상이 아니다.

### 원인 B — 승인 목록에 없지만 반복 사용되는 태그 (승인 목록 편입 후보)

2회 이상 쓰였지만 `data/tags.yaml`에 없는 태그 409개. 대소문자 문제(원인 A)를 빼면 실질적으로 새로운 개념군:

- 시스템/개발: `System-Design`(7), `Regex`(7), `Reliability`/`신뢰성`(8), `Production`(7), `Mutex`(3), `RAII`(3), `Kernel`/`커널`(6), `Pipeline`(8), `Observability`(4), `Synchronization`/`동기화`(6)
- 영화/드라마(MCU 계열 다수): `Marvel`(9), `Superhero`/`슈퍼히어로`(18), `MCU`(6), `Disney`(4), `Netflix`(4)
- Vocabulary 컬렉션: `phrasal verb`/`구동사`(11), `collocation`(7), `pronunciation`(8), `usage notes`(41), `vocabulary building`(38), `study English`(38), `EN/KR examples`(42), `context`/`맥락`(85)

이 그룹은 각 컬렉션 내부에서는 이미 반복적으로 쓰이는 "연결 태그"인데, 표기가 제각각(대소문자, 띄어쓰기, 언더스코어/하이픈)이라 승인 목록에 등록되지 못한 채 흩어져 있다.

### 원인 C — 구조적으로 롱테일일 수밖에 없는 태그 (병합 대상 아님)

- 알고리즘/BOJ 문제별 기법 태그: `Problem-30239`, `Rerooting-DP`/`리루팅DP`, `Matrix-Exponentiation` 등 — 문제 고유 ID·세부 기법이라 원래 1회성
- Bash/CMD 컬렉션의 개별 명령어 태그: `chmod`, `cp`, `mv`, `rm`, `curl` 등 — 포스트마다 다른 명령어를 다루므로 자연스러운 분산
- 영화/드라마 리뷰의 배우·감독·스튜디오 고유명사: `Chris-Evans`, `Robert-Zemeckis`, `Warner-Bros` 등 — 실제로 같은 배우가 여러 리뷰에 나오면 자동으로 연결되므로 표기만 통일하면 됨(원인 A/B에 포함)

이 카테고리는 "파편화"라기보다 정상적인 특수성이다. 여기까지 통합하려 하면 태그의 검색성이 오히려 떨어진다. **손대지 않는다.**

## 3. 통합 계획

### Phase 1 — 표기 정규화 일괄 치환 (스크립트, 최우선, 저위험)

대상: 원인 A의 182개 그룹 + 원인 B에서 casing만 다른 것들.

- `data/tags.yaml`의 승인 표기를 정답(canonical)으로 삼아 `content/**/index.md` frontmatter의 `tags:` 리스트를 스크립트로 일괄 치환 (`testing` → `Testing` 등)
- 정확 일치(대소문자/공백/하이픈 차이만) 케이스만 자동 처리 — 의미가 다를 수 있는 건 제외
- 같은 포스트 안에 승인형·비승인형이 동시에 있으면 치환 후 중복 제거
- 처리 방식: Python 스크립트(`script/normalize_tags.py` 신규) + YAML frontmatter 파서로 안전하게 재작성, 커밋 전 `git diff` 샘플 검토
- 예상 효과: 고유 태그 수 3,876개 → 약 3,700개대로 감소, 상위 182개 개념의 태그 페이지 통합(예: `/tags/testing/`이 사라지고 `/tags/Testing/`으로 761개 글이 모임)

### Phase 2 — 반복 태그의 승인 목록 편입 + 표기 통일

대상: 원인 B의 409개 중 2회 이상, 특히 5회 이상 사용된 것.

1. `data/tags.yaml`에 새 카테고리 또는 기존 카테고리에 추가:
   - `system_design_and_architecture`: System-Design, Regex, Reliability/신뢰성, Production, Observability, Pipeline
   - `concurrency_and_systems`: Mutex, RAII, Kernel/커널, Synchronization/동기화
   - `movies_genre_franchise` (컬렉션 전용): Marvel, Superhero/슈퍼히어로, MCU, Disney, Netflix
   - `vocabulary_meta`: Phrasal-Verb/구동사, Collocation, Pronunciation, Usage-Notes, Context/맥락, EN-KR-Examples
2. 표기 통일 규칙 확정 (예: `phrasal verb` → `Phrasal-Verb`, `EN/KR examples` → `EN-KR-Examples`) 후 Phase 1과 동일한 스크립트로 일괄 치환
3. 각 컬렉션 전용 스킬(`movie-review-writing`, `vocabulary-post-writing` 등)의 태그 가이드에 신규 승인 태그를 반영해 향후 글 작성 시 표준 표기가 자동으로 쓰이게 함

### Phase 3 — 롱테일은 유지, 대신 "연결 태그 최소 보장" 룰 추가

- 개별 포스트가 50개 이상 태그를 채울 때, 최소 N개(예: 10개)는 `data/tags.yaml` 승인 태그(카테고리/기술/장르 등 상위 개념)에서 나오도록 권장 문구를 `rules-that-must-be-followed`에 추가
- 이렇게 하면 롱테일 고유 태그(문제 ID, 배우명, 명령어명)는 그대로 두되, 각 글이 최소한 상위 개념 태그로는 다른 글과 반드시 연결되도록 보장

### Phase 4 — 재발 방지 (린트/CI)

- 이미 작업 중인 `script/lint_frontmatter.py`(title/description/tag count 검사)를 확장해 태그 표기 검증 추가:
  - `tags:`의 각 항목이 `data/tags.yaml` 승인 목록에 있는지, 없다면 원인 A 패턴(대소문자만 다른 승인 태그가 존재)인지 검사
  - 원인 A 패턴 매치 시 CI에서 `::error`로 실제 오탈자 표기를 지적 (신규/수정 파일 대상, 기존 정책과 동일하게 added는 hard-fail, modified는 warning)
- `.github/workflows/lint-content.yml`에 이미 연결되어 있다면 검사 스텝만 추가

## 4. 실행 순서 제안

| 단계 | 작업 | 방식 | 리스크 |
|---|---|---|---|
| 1 | 원인 A 182개 그룹 일괄 치환 | 스크립트 | 낮음 (기계적 대소문자 정규화) |
| 2 | 원인 B 표기 통일안 검토·확정 (사람이 목록 승인) | 수동 검토 후 스크립트 실행 | 중간 (신규 카테고리 이름 결정 필요) |
| 3 | `data/tags.yaml`에 신규 승인 태그 추가 | 수동 편집 | 낮음 |
| 4 | 관련 컬렉션 스킬 파일에 신규 태그 반영 | 수동 편집 | 낮음 |
| 5 | `rules-that-must-be-followed`에 "연결 태그 최소 보장" 룰 추가 | 수동 편집 | 낮음 |
| 6 | `lint_frontmatter.py`에 태그 표기 검사 추가 | 스크립트 개발 | 중간 (오탐 방지 위해 승인 목록과 정확히 동기화 필요) |

Phase 1은 리스크가 가장 낮고 효과가 즉시 드러나므로 먼저 진행하고, 결과를 커밋 단위로 나눠 diff 검토 후 병합하는 것을 권장한다. Phase 2 이후는 판단이 필요한 작업이라 순차적으로 사람 확인을 거치는 게 안전하다.

## 5. 이번 분석에서 제외한 것

- 롱테일 고유명사·문제 ID·명령어 태그(원인 C)는 통합 대상에서 의도적으로 제외했다. 억지로 병합하면 검색 정밀도가 떨어진다.
- draft 상태 포스트(381개)도 통계에 포함했다. 통합 스크립트 실행 시 draft 여부와 무관하게 모든 포스트에 적용하는 것을 권장한다(태그 표기 일관성은 draft/publish와 무관).
