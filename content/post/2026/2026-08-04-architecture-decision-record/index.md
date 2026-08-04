---
title: "[Programming] ADR(Architecture Decision Record): 설계 결정을 기록하는 법"
description: "6개월 전 왜 이 라이브러리를 골랐는지 아무도 설명 못하는 문제를 Michael Nygard가 2011년 제안한 ADR로 푸는 법. Context/Decision/Status/Consequences 5개 섹션 템플릿, adr-tools 사용법, 도입 시 흔한 실수 5가지를 정리한다."
date: 2026-08-04
lastmod: 2026-08-04
draft: false
categories:
  - Programming
  - Software-Architecture
tags:
  - Software-Architecture(소프트웨어아키텍처)
  - Documentation(문서화)
  - Best-Practices
  - Maintainability(유지보수성)
  - Git
  - GitHub
  - Version-Control(버전관리)
  - Collaboration(협업)
  - Code-Review(코드리뷰)
  - Software-Engineering(소프트웨어공학)
  - Guide(가이드)
  - Reference(참고)
  - Case-Study
  - Culture(문화)
  - Technology(기술)
  - Process(프로세스)
  - Pitfalls(함정)
  - Automation(자동화)
  - Deep-Dive
  - Modularity
  - Implementation(구현)
  - ADR
  - Architecture-Decision-Record
  - Michael-Nygard
  - Martin-Fowler
  - adr-tools
  - Engineering-Culture
  - Decision-Making
  - Onboarding
  - Knowledge-Management
image: "wordcloud.png"
---

새로 합류한 팀원이 코드를 읽다가 묻는다. "이 부분은 왜 이렇게 만들었어요?" 답할 수 있는 사람이 아무도 없다. 만든 사람은 이미 팀을 떠났고, 남은 사람들은 "예전부터 그랬다"는 말만 되풀이한다. 그러면 새 팀원은 두 가지 중 하나를 한다 — 이유도 모른 채 기존 구조를 답습하거나, 근거도 모른 채 뒤엎는다. 둘 다 위험하다.

<strong>Architecture Decision Record(ADR)</strong>는 이 문제를 "결정이 내려진 순간에 근거를 함께 적어 코드와 같은 저장소에 버전 관리"하는 방식으로 푼다. 거창한 설계 문서가 아니라 결정 하나당 1–2페이지짜리 마크다운 파일 하나다. 이 글에서는 ADR이 왜 지금 형태로 자리 잡았는지, 실제로 어떻게 작성하고 도구로 관리하는지, 그리고 도입할 때 흔히 걸려 넘어지는 지점을 정리한다.

---

## ADR이 풀려고 한 문제

ADR이라는 용어와 형식은 Michael Nygard가 2011년 11월 15일 Cognitect 블로그에 올린 "Documenting Architecture Decisions"에서 처음 제안했다. Nygard가 관찰한 것은 두 극단이었다. 한쪽은 애자일 문화의 "문서 최소화" 원칙 아래 아키텍처 결정의 근거를 아예 기록하지 않는 팀이다. 코드가 곧 설계라는 원칙은 좋지만, 몇 달 뒤 "왜 이 라이브러리를 선택했는가"를 아무도 설명하지 못하는 결과로 이어진다. 다른 쪽은 시스템 전체 구조를 담는 대형 아키텍처 문서(Software Architecture Document)다. Nygard는 원문에서 "Large documents are never kept up to date"(대형 문서는 결코 최신 상태로 유지되지 않는다)라고 단언했다 — 결정 하나가 바뀔 때마다 방대한 문서 전체를 손봐야 하는 비용이 실제로는 감당되지 않기 때문이다.

두 극단 사이에서 Nygard가 택한 절충안은 "시스템 전체"가 아니라 "하나의 결정" 단위로 문서를 쪼개는 것이었다. 결정마다 짧은 마크다운 파일 하나를 만들고, 이를 코드와 함께 버전 관리되는 저장소 안에 둔다. 문서가 작으니 실제로 유지되고, 코드와 같은 저장소에 있으니 리뷰(PR)와 검색이 가능하다. Martin Fowler는 이 아이디어를 자신의 bliki에서 "제품이나 생태계와 관련된 단일 결정을 포착하고 설명하는 짧은 문서"로 정리했고, ADR을 쓰는 과정 자체가 결정을 명확히 하고 팀의 합의를 끌어내는 데도 도움이 된다고 덧붙였다.

## 5개 섹션 템플릿

Nygard가 제안한 원형 템플릿은 다섯 섹션으로 구성된다. 앞의 세 섹션(Title·Context·Decision)이 "무엇을, 왜 결정했는가"를 담는다면, 뒤의 두 섹션(Status·Consequences)은 "이 결정이 지금도 유효한가, 적용한 결과 무엇을 얻고 무엇을 잃었는가"를 담아 시간이 지나도 판단 근거를 다시 꺼내볼 수 있게 한다.

| 섹션 | 내용 |
|------|------|
| Title | "ADR 1: Deployment on Ruby on Rails 3.0.10"처럼 짧은 명사구 |
| Context | 기술적·정치적·사회적·프로젝트 로컬 요인 등 "작용 중인 힘"을 옹호가 아닌 중립적 사실 위주로 서술 |
| Decision | 능동태로 "We will…" 형태로 결정을 명시 |
| Status | proposed / accepted / deprecated / superseded(대체 ADR 링크 포함) |
| Consequences | 결정을 적용한 뒤의 결과 — 긍정적·부정적·중립적 영향 모두 |

여기서 실무에 가장 크게 영향을 주는 건 Status와 Consequences다. Nygard는 결정이 바뀌면 기존 ADR 파일을 고쳐 쓰지 말고, 새 ADR을 만들어 이전 ADR의 status를 superseded로 바꾸고 새 ADR을 링크하라고 권한다. 즉 ADR은 최신 상태를 유지하는 살아있는 문서가 아니라, 그 시점에 왜 그렇게 결정했는지를 남기는 거의 불변(immutable)의 이력이다. "지금 맞는 답"이 아니라 "그때는 왜 그게 맞는 답이었는지"를 남기는 것이 목적이라, 나중에 결정이 뒤집혀도 파일을 지우지 않는다. Consequences 섹션이 부정적 영향까지 솔직하게 적도록 요구하는 것도 같은 맥락이다 — 좋은 점만 적으면 다음 사람이 같은 트레이드오프를 다시 검토하는 시간을 아낄 수 없다.

## adr-tools로 실제로 써보기

ADR은 형식이 단순해서 손으로 마크다운 파일을 만들어도 되지만, npryce가 만든 오픈소스 커맨드라인 도구 `adr-tools`를 쓰면 번호 매기기와 supersede 처리를 자동화할 수 있다.

```bash
# 저장소에 ADR 디렉터리 초기화 (기본 doc/adr)
adr init doc/adr

# 새 ADR 작성 — 순번을 자동으로 매기고 편집기를 연다
adr new "Use PostgreSQL for primary datastore"

# 기존 ADR을 대체하는 새 ADR 작성 — 5번 ADR을 대체한다고 명시
adr new -s 5 "Migrate primary datastore to CockroachDB"
```

`adr new`로 생성된 파일은 `doc/adr/0001-use-postgresql-for-primary-datastore.md`처럼 순번이 붙은 이름으로 저장되고, 앞서 본 5개 섹션 골격이 이미 채워진 채로 열린다. 실제로 채워 넣으면 다음과 같은 형태가 된다.

```markdown
# 3. Use PostgreSQL for primary datastore

## Status
Accepted

## Context
결제 이력 조회 API가 초당 트랜잭션 처리량보다 복잡한 조인 쿼리 성능에 더 민감하다.
팀 내 RDB 운영 경험은 MySQL과 PostgreSQL 양쪽에 고르게 있다.

## Decision
PostgreSQL 15를 주 데이터스토어로 채택한다.
JSONB 컬럼과 부분 인덱스를 결제 메타데이터 저장에 활용한다.

## Consequences
- 복잡한 조인 쿼리의 실행 계획을 EXPLAIN ANALYZE로 세밀하게 튜닝할 수 있다.
- 팀의 MySQL 운영 노하우(레플리케이션 설정 등)는 재사용하지 못하고 새로 익혀야 한다.
- 벤더 락인 없이 RDS·Cloud SQL·Aurora 등 여러 관리형 서비스로 이전 가능하다.
```

이 파일은 코드와 같은 PR로 리뷰받고 같은 커밋 이력에 남는다. 별도의 위키나 문서 도구를 쓰지 않는 이유가 여기에 있다 — 코드를 리뷰하는 것과 똑같은 절차로 "왜 이렇게 짰는지"도 리뷰받을 수 있다.

## 왜 위키나 대형 문서가 아니라 이 형태인가

ADR 이전에도 결정을 남기는 시도는 있었다. 문서를 아예 안 쓰거나, 시스템 전체를 다루는 방대한 문서를 쓰거나, 위키·이슈 트래커에 그때그때 흩어 적는 방식이다. 세 방식 모두 "결정 단위로 쪼개서 코드와 함께 버전 관리한다"는 핵심 아이디어가 빠져 있어서, 결국 결정의 근거가 사라지거나 문서 자체가 낡아버렸다.

| 대안 | 아이디어 | 왜 충분하지 않았는가 |
|------|----------|---------------------|
| 문서화 생략(애자일 순수주의) | 코드가 곧 설계라는 원칙으로 별도 문서를 남기지 않음 | 몇 달 후 "왜 이 라이브러리를 선택했는가"를 아무도 설명하지 못함 |
| 대형 아키텍처 문서(SAD) | 시스템 전체 구조를 하나의 종합 문서로 기술 | 갱신 비용이 너무 높아 실제로는 유지되지 않고 낡은 채로 방치됨 |
| 위키·이슈 트래커에 산발적으로 기록 | 결정이 나올 때마다 어딘가에는 적어둠 | 검색·추적이 안 되고, 결정 간의 대체 관계가 연결되지 않음 |

이 비교에서 드러나는 ADR의 제약 조건은 명확하다. 문서 유지비용을 최소화하는 것이 최우선이었기 때문에, 형식은 핵심 정보를 맨 앞에 두는 역피라미드 구조로 짧게 유지하고, 텍스트 에디터와 git만으로 작성·리뷰·검색이 가능해야 했다. 만약 ADR 없이 대형 SAD 방식을 고수했다면 문서가 코드 변경 속도를 따라가지 못해 신뢰할 수 없는 상태로 방치됐을 가능성이 높다 — 이는 Nygard가 실제로 겪은 실패 패턴이다. 반대로 문서화를 아예 생략했다면, 이후 합류자는 이미 검토되고 기각된 대안을 다시 시도하거나, 더 이상 유효하지 않은 이유로 굳어진 결정을 맹목적으로 답습하는 비용을 반복해서 치르게 된다.

## 실전 팁: 자주 하는 실수

1. **기존 ADR을 고쳐 쓴다.** 결정이 바뀌었다고 이전 ADR 파일을 수정해버리면 "그때 왜 그렇게 결정했는지"라는 이력 자체가 사라진다. 새 ADR을 만들고 이전 ADR의 status를 superseded로 바꾸는 것이 원칙이다.
2. **모든 결정을 ADR로 남기려 한다.** 변수명 하나 바꾸는 수준의 결정까지 ADR로 쓰면 팀이 문서화 자체에 피로를 느끼고 결국 아무것도 안 쓰게 된다. "나중에 다시 물어볼 가능성이 있는, 되돌리기 비용이 큰 결정"만 대상으로 삼는 편이 지속 가능하다.
3. **Context를 옹호(advocacy) 문체로 쓴다.** "이게 최선이라 골랐다"처럼 결론을 정당화하는 서술이 아니라, 그 순간 작용하고 있던 기술적·조직적 제약을 중립적으로 나열해야 나중에 상황이 바뀌었을 때 그 결정이 여전히 유효한지 판단할 수 있다.
4. **Consequences에 긍정적 결과만 적는다.** 부정적 영향과 트레이드오프까지 적어야 다음 사람이 같은 검토를 반복하지 않는다. 장점만 적힌 ADR은 광고 카피와 다를 게 없다.
5. **코드 저장소와 별도 위치(위키·이슈 트래커)에 둔다.** ADR이 코드와 같은 PR 리뷰·같은 커밋 이력을 타지 않으면, 코드가 바뀔 때 ADR도 함께 갱신해야 한다는 압력 자체가 생기지 않는다.

## 이 글을 읽은 후 확인할 점

아래 질문에 스스로 답할 수 있으면 ADR을 팀에 도입할 준비가 된 것이다.

1. ADR과 위키·회의록의 차이를 설명할 수 있는가 — 결정 단위로 쪼개져 코드와 같은 저장소에서 버전 관리된다는 점이 왜 검색성·유지비용에서 다른 결과를 만드는지 말할 수 있어야 한다.
2. 결정이 바뀌었을 때 기존 ADR을 고쳐 쓸지, 새 ADR을 만들어 superseded 처리할지 판단할 수 있는가.
3. Context 섹션을 옹호(advocacy) 문체가 아니라 중립적 사실 나열로 쓸 수 있는가 — "이게 최선이었다"가 아니라 "그때 어떤 제약이 작용했다"로 쓰는 차이다.
4. 어떤 결정까지 ADR로 남기고 어떤 결정은 남기지 않을지, "되돌리기 비용"을 기준으로 선을 그을 수 있는가.

## 요약

| 항목 | 내용 |
|------|------|
| 목적 | 아키텍처 결정의 배경과 근거를 결정 시점에 기록해, 나중에 "왜 이렇게 만들었는지" 추적 가능하게 함 |
| 형식 | Title / Context / Decision / Status / Consequences 5섹션, 1–2페이지 마크다운 |
| 위치 | 코드와 같은 저장소(예: `doc/adr/`), 버전 관리·PR 리뷰 대상 |
| 결정이 바뀌면 | 기존 파일을 고치지 않고 새 ADR을 만들어 이전 ADR을 superseded 처리 |
| 도구 | `adr-tools`(npryce)로 번호 매기기·supersede 자동화 |
| 대상 | 되돌리기 비용이 크고 나중에 다시 물어볼 가능성이 있는 결정만 |

처음 도입할 때는 팀 전체 결정을 소급해서 ADR로 남기려 하지 말고, 지금 막 논의 중인 결정 하나만 골라 첫 ADR을 써보는 편이 저항이 적다. 화려한 도구가 필요 없다. 텍스트 에디터와 git, 그리고 "이 결정을 나중에 설명할 수 있어야 한다"는 습관만 있으면 시작할 수 있다.

## 참고 자료

- [Michael Nygard, "Documenting Architecture Decisions" (2011-11-15, Cognitect)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Martin Fowler, bliki: Architecture Decision Record](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html)
- [adr.github.io — Architectural Decision Records 커뮤니티 리소스](https://adr.github.io/)
- [npryce/adr-tools — ADR 관리 커맨드라인 도구 (GitHub)](https://github.com/npryce/adr-tools)
