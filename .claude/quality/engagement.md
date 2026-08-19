# 성과판 (Engagement Board)

독자 반응 신호의 세션 간 상태(state)다. [`scoreboard.md`](scoreboard.md)가 **내적 품질**(루브릭 점수)을 기록한다면, 이 판은 **외적 반응**(검색 노출·클릭·조회·댓글)을 기록한다. 두 축은 섞지 않는다 — 인기 지표는 품질 점수에 반영하지 않고, 품질 점수는 인기 지표를 예측하지 않는다. 두 축의 대조(상관 분석)는 [`engagement-report`](../skills/engagement-report/SKILL.md) 스킬의 분기 회고에서만 수행한다.

- **수집 주기**: 주 1회 (`engagement-report` 스킬이 수행하고 이 파일을 갱신한다)
- **데이터 소스**: Google Search Console(등록 완료) / GA4 속성 `378371944`, 측정 ID `G-E99XGK8V2Y`(태그 2026-08-04 배포) / utterances(GitHub issues)
- **표 갱신 규칙**: 아래 각 표는 **최신 스냅샷**이다. 수집할 때마다 표 전체를 교체하고, 수집 이력에 한 줄을 추가한다. 과거 스냅샷과의 비교가 필요하면 git 이력을 본다.

## 수집 이력

| 날짜 | 소스 | 기간 | 비고 |
|------|------|------|------|
| 2026-08-04 | GSC(브라우저), utterances(gh api) | GSC 최근 3개월 | 시딩. GA4는 태그 배포 직후라 데이터 없음. GSC 사이트 전체: 클릭 279 / 노출 1.21만 / CTR 2.3% / 평균 순위 7.4 |
| 2026-08-04 | GSC(브라우저), utterances(gh api), GA4(브라우저) | GSC 최근 3개월 | 주간 자동 수집(같은 날 재실행). engagement-report 스킬 자체가 오늘 PR #91로 병합돼 시딩 스냅샷과 동일 시점 — GSC 사이트 전체·상위 페이지/검색어·utterances 전부 시딩과 숫자 변동 없음(최종 업데이트 4.5시간 전, 동일 3개월 창). GA4는 여전히 "사용 가능한 데이터 없음"(태그 배포 당일). 아래 표는 갱신할 신규 데이터가 없어 유지, 백로그도 근거 변동 없어 갱신 없음 — 다음 주 월요일부터 실질적 변화 추적 시작 |
| 2026-08-10 | utterances(gh api) | — | 야간 자율 실행(스케줄 태스크), 대화형 세션 아님. GSC·GA4는 API 자격 미설정 + Chrome 확장 미연결(`list_connected_browsers` 결과 빈 배열) — **미수집**. utterances는 `gh api`로 조회, 이슈 4건 모두 지난 스냅샷(2026-08-04)과 댓글·반응 수 동일 — 신규 변동 없음. 아래 GSC·GA4 표는 갱신할 데이터가 없어 유지, 백로그도 근거 변동 없어 갱신 없음 |
| 2026-08-17 | utterances(gh api) | — | 야간 자율 실행(스케줄 태스크), 대화형 세션 아님. GSC·GA4는 API 자격 여전히 미설정(`~/.config/gcp/` 없음) + Chrome 확장 미연결(`list_connected_browsers` 결과 빈 배열) — **미수집**. utterances는 `gh api`로 조회, 이슈 4건 모두 지난 스냅샷(2026-08-10)과 댓글·반응 수 동일 — 신규 변동 없음. 아래 GSC·GA4 표는 갱신할 데이터가 없어 유지, 백로그도 근거 변동 없어 갱신 없음 |

## 검색 성과 — 상위 페이지 (GSC, 최근 3개월)

총 138개 페이지 중 상위 10개. 클릭수 내림차순.

| 페이지 경로 | 클릭 | 노출 | CTR | 비고 |
|------------|-----:|-----:|----:|------|
| /post/2024-08-19-collision-detection/ | 83 | 1,289 | 6.4% | 사이트 1위. sweep and prune 쿼리도 이 글로 유입 |
| /post/2024-08-22-jax-vs-pytorch/ | 74 | 679 | 10.9% | jax 관련 쿼리 3종 합산 클릭 45 |
| /post/2024-08-13-disagree-and-commit/ | 22 | 308 | 7.1% | |
| /post/2023-06-02-dynamic-loading-in-cpp/ | 17 | 629 | 2.7% | |
| /post/2024-10-15-crlf/ | 14 | 1,616 | 0.9% | **노출 1위인데 CTR 최저** — 제목/description 개선 1순위 |
| /post/2024-08-27-database/ | 9 | 279 | 3.2% | |
| /post/2024-09-23-distrubute-system/ | 8 | 496 | 1.6% | slug 오타(distrubute)가 눈에 띔 — URL 변경은 유입 끊김 위험, 건드리지 않음 |
| /post/2024-09-01-aicd/ | 6 | 427 | 1.4% | |
| /post/2022-03-29-cpp-cout-precision/ | 6 | 372 | 1.6% | |
| /post/2024-08-22-relational-vs-non-relational-datebase/ | 5 | 452 | 1.1% | |

> **시딩 시점의 관찰**: 상위 10개가 전부 구형 `/post/` 글이고 컬렉션 글은 없다. 컬렉션(약 1,500편)은 최근 작성이라 색인·순위가 아직 쌓이지 않았을 가능성과, 검색 수요와 다른 주제라는 가능성이 모두 있다 — 몇 주치 스냅샷이 쌓이면 분기 회고에서 판별한다.

## 검색 성과 — 상위 검색어 (GSC, 최근 3개월)

총 298개 검색어 중 상위 10개.

| 검색어 | 클릭 | 노출 |
|--------|-----:|-----:|
| jax vs pytorch | 24 | 164 |
| jax pytorch | 16 | 33 |
| disagree and commit | 14 | 105 |
| pytorch jax | 5 | 13 |
| crlf lf 차이 | 4 | 208 |
| lf crlf 차이 | 3 | 61 |
| collision detection | 3 | 42 |
| 고립성의 | 3 | 16 |
| sweep and prune | 3 | 13 |
| dlopen | 2 | 107 |

## 페이지 성과 (GA4)

아직 데이터 없음 — 측정 태그가 2026-08-04에 배포됐다. 첫 수집은 배포 7일 후부터 의미가 있다.

## 댓글·반응 (utterances)

`gh api`로 수집. utterances-bot이 만든 이슈 = 댓글이 달린 글.

| 글 경로(pathname) | 댓글 | 반응 | 이슈 |
|------------------|-----:|-----:|------|
| cpp/dlopen/ | 2 | 0 | [#1](https://github.com/42jerrykim/42jerrykim.github.io/issues/1) |
| docker/remove-all-docker-container/ | 1 | 0 | [#3](https://github.com/42jerrykim/42jerrykim.github.io/issues/3) |
| lattepanda/install-ubuntu-16.04-on-lattepanda/ | 1 | 0 | [#2](https://github.com/42jerrykim/42jerrykim.github.io/issues/2) |
| post/2024-11-28-reactive-html-noteboot/ | 0 | 0 | [#4](https://github.com/42jerrykim/42jerrykim.github.io/issues/4) |
