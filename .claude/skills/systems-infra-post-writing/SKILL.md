---
name: systems-infra-post-writing
description: >-
  content/post/ 하위 시스템·인프라 글(OS/Windows·Linux, 가상화, 네트워킹, 보안, CI-CD·빌드 자동화,
  셸/배치 스크립트 단발 팁) 작성 가이드. 제목·태그·트러블슈팅 중심 본문 구조·체크리스트를 표준화한다. content/post/
  하위 OS·인프라·CI-CD·보안 주제 글 작성 시 사용한다.
---

# 시스템·인프라 포스트 작성 가이드 (content/post/)

`content/post/<연도>/`에 실리는 **시스템·인프라 운영 글**(Windows/Linux 설정, 가상화, 네트워킹, 보안, CI/CD·빌드 파이프라인 최적화 등)을 작성할 때 따르는 가이드다. `content/collection/bashshell/`·`content/collection/cmd/`의 **명령어 레퍼런스**는 [`shell-command-post-writing`](../shell-command-post-writing/SKILL.md)을 따르고, 이 스킬은 **특정 명령어 하나가 아니라 문제 해결·구축 과정 전체**를 다루는 글에 적용한다. [`blog-post-writing`](../blog-post-writing/SKILL.md), [`rules-that-must-be-followed`](../rules-that-must-be-followed/SKILL.md)과 함께 적용한다.

**적용 예시**: Hugo 빌드 최적화, GitHub Actions 캐시 전략, Surface Go Linux 설치기, 가상화(Hyper-V)·원격 데스크톱 설정, 네트워킹·보안 트러블슈팅.

---

## 1. 제목/메타 규칙

- **카테고리 접두어**: 다루는 플랫폼·도구로 표기. 예: `[Hugo]`, `[Linux]`, `[Windows]`, `[CI/CD]`, `[Security]`
- **메인 제목**: "문제 상황 → 해결" 또는 "핵심 수치 개선" 형태를 권장. 예: `[Hugo] GitHub Pages 1GB 한계 극복 - 빌드 최적화 실전 가이드`
- **정량 성과가 있으면 제목/description에 구체 수치**(예: "17분→2분", "1.8GB→600MB")를 포함해 검색 가치를 높인다.
- **총 길이**: 70자 이내

## 2. 날짜/폴더 규칙

- 경로: `content/post/<연도>/YYYY-MM-DD-<영문-슬러그>/index.md`
- `date`/`lastmod`는 작성/수정 당일(로컬 타임존). 후속 업데이트(도구 버전 변경 등) 시 `lastmod` 갱신.
- 폴더 슬러그: 도구+문제 키워드 조합 (예: `hugo-build-optimization-github-pages`, `github-actions-hugo-webp-cache-build-time`).

## 3. Front Matter 템플릿

```yaml
---
title: "[도구/플랫폼] 문제 상황 - 해결 방식 요약"
description: "환경(도구·버전·플랫폼)과 문제 상황을 1문장, 해결 전략과 정량 성과(가능하면 수치)를 1-2문장으로. 150자 내외."
date: YYYY-MM-DD
lastmod: YYYY-MM-DD
categories:
  - 도구/플랫폼  # 예: Hugo, Linux, Windows
  - 보조분류  # 예: Optimization, CI-CD, Security
tags:  # 25개 이상, 영/한 병용 개념은 Tag(태그) 형식
  - Technology
  - 기술
image: "image.png"
---
```

## 4. 본문 구조 가이드

실제 게시 글(`hugo-build-optimization-github-pages`, `github-actions-hugo-webp-cache-build-time` 등)에서 관찰되는 "문제→해결→검증" 구조:

1. **개요**: 환경(버전·플랫폼)과 이 글이 해결하는 문제를 1-2문단으로 요약.
2. **문제**: 증상·제약을 구체적으로 서술한다(에러 메시지, 한계 수치, 재현 조건).
3. **해결 전략**: 선택한 접근 방식과 그 방식을 고른 이유(대안과의 트레이드오프)를 문단으로 설명.
4. **구현**: 실제 설정 파일·명령·스크립트를 단계별로 제시. 각 코드 블록 앞에 목적 2문장 이상.
5. **(해당 시) 대안**: 검토했지만 채택하지 않은 방식과 그 이유를 짧게 남긴다.
6. **적용 전후 비교**: 정량 지표(시간·용량·비용 등)를 표로 정리해 개선 효과를 검증 가능하게 제시한다.
7. **요약**: 핵심 변경점과 재현 시 주의사항을 1문단 또는 체크리스트로.
8. **참고 문헌**: 공식 문서·이슈 트래커 등 1차 출처.

- **재현 가능성**: 설정 파일·명령은 그대로 복사해 실행 가능한 형태로 쓴다(생략된 인자·환경변수 없이).
- **정량 성과**: "빨라졌다"가 아니라 실측 전후 수치(측정 조건 포함)를 반드시 남긴다.
- **플랫폼 차이**: Windows/Linux, GNU/BSD 등 이식성 차이가 있으면 명시한다.

## 5. 태그 전략

`data/tags.yaml`의 `devops_and_tools`, `system_and_low_level`, `web_and_backend`, `frameworks_and_platforms`, `general_topics` 카테고리에서 25개 이상 선정. 도구명(Hugo, Docker, GitHub Actions)과 병기 승인 태그(CI-CD, Optimization(최적화))로 채운다.

## 6. 작성 체크리스트

- [ ] 경로가 `content/post/<연도>/YYYY-MM-DD-<슬러그>/index.md`인가?
- [ ] title 70자 이내, description 150자 내외인가? 정량 성과가 있으면 제목/description에 반영했는가?
- [ ] tags 25개 이상(`data/tags.yaml` 승인 태그)인가?
- [ ] `draft: true`(신규 글), date/lastmod가 오늘 날짜인가?
- [ ] "문제 → 해결 전략 → 구현 → 전후 비교" 구조를 따랐는가?
- [ ] 설정·명령·스크립트가 그대로 재현 가능한 형태인가?
- [ ] 정량 성과(시간·용량 등)에 실측 전후 수치가 있는가?
- [ ] 플랫폼/이식성 차이를 다뤘는가(해당 시)?
- [ ] 참고 문헌이 1차 출처 우선이고 링크가 접근 가능한가?
- [ ] 특정 명령어 1개의 옵션·문법이 핵심이라면 이 스킬 대신 [`shell-command-post-writing`](../shell-command-post-writing/SKILL.md)이 더 적합한지 확인했는가?
