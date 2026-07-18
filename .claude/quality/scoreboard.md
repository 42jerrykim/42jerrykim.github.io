# 품질 점수판 (Quality Scoreboard)

`post-quality-loop` 루프의 세션 간 상태(state)다. 글별 최신 채점 결과를 기록해, 자율 모드가 "미채점/최저점 글"을 고르는 인덱스로 쓴다.

- **상태 값**: `미채점` / `진행중` / `통과` / `에스컬레이션`
- **점수**: 0~100 (루브릭 총점). 미채점이면 `-`.
- **채점일**: 터미널 오늘 날짜(`yyyy-MM-dd`).
- **시딩**: 본문(아래 표)이 비어 있으면 `SKILL.md`의 "점수판 운영 — 시딩" 절차로 게시글을 1회 등록한다.

| 글 경로 | 최신점수 | 채점일 | 반복수 | 상태 | 주요 미달항목 |
|---------|---------:|--------|-------:|------|---------------|
| content/collection/multithreading-design-patterns/12-coroutine-reinterpretation/index.md | 93.1 | 2026-07-09 | 2 | 통과 | 없음(경미: ActiveObject 104줄 코드 블록의 문단 비율) |
| content/collection/multithreading-design-patterns/13-lockfree-reclamation/index.md | 96.1 | 2026-07-09 | 2 | 통과 | 없음 |
| content/collection/cleanarchitecture/00-clean-architecture-overview-introduction/index.md | 86.2 | 2026-07-18 | 3 | 에스컬레이션 | 항목3 구조(리스트-only 절 다수), 항목4 안티패딩("핵심 개념" 절과 코드 도입부 문장 중복), 항목5 코드(Java 예제 import/보조타입 미정의), 항목7 Edge-Cases 태그가 본문과 불일치 |
| content/collection/cleanarchitecture/01-architecture-history-evolution-introduction/index.md | 91 | 2026-07-18 | 2 | 통과 | 없음(경미: 흔한 오해 절 부재, 다음장 하이퍼링크 없음) |
| content/collection/cleanarchitecture/02-layered-architecture-limitations-history/index.md | 84.1 | 2026-07-18 | 3 | 에스컬레이션 | 항목3 구조(일부 절 리스트-only), 항목2 MVC 상세절이 00 배정범위를 벗어남 |
| content/collection/cleanarchitecture/03-hexagonal-architecture-ports-adapters/index.md | 89.2 | 2026-07-18 | 3 | 에스컬레이션 | 항목3 구조(장점/한계 절 문단비율 20%), 항목5 코드(Order/Money 등 보조타입 미정의). 90점에 0.8점 차 |
| content/collection/cleanarchitecture/04-onion-architecture-domain-centric-design/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 없음(경미: 패키지구조 절 리드문단 부재, 코드 보조타입 미정의) |
| content/collection/cleanarchitecture/05-clean-architecture-birth-uncle-bob/index.md | 85 | 2026-07-18 | 3 | 에스컬레이션 | 항목5 코드(코드예제 전무), 항목2 흔한오해 절 부재 |
| content/collection/cleanarchitecture/06-introduction-software-design-architecture/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/07-design-vs-architecture-definition/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/08-two-values-behavior-structure/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/09-programming-paradigms-introduction/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/10-paradigm-overview-three-types/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/11-structured-programming-goto-elimination/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/12-object-oriented-programming-polymorphism/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/13-functional-programming-immutability/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/14-solid-principles-introduction/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/15-srp-single-responsibility-principle/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/16-ocp-open-closed-principle/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/17-lsp-liskov-substitution-principle/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/18-isp-interface-segregation-principle/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/19-dip-dependency-inversion-principle/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/20-component-principles-introduction/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/21-components-deployment-units-history/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/22-component-cohesion-rep-ccp-crp/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/23-component-coupling-adp-sdp-sap/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/24-architecture-introduction-system-design/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/25-what-is-architecture-system-lifecycle/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/26-independence-usecase-operation-development/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/27-boundaries-drawing-lines-plugin-architecture/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/28-boundary-anatomy-monolith-to-services/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/29-policy-and-level-high-level-dependency/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/30-business-rules-entities-usecases/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/31-screaming-architecture-intent-driven-structure/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/32-clean-architecture-concentric-circles-dependency/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/33-presenter-humble-object-testability/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/34-partial-boundaries-cost-benefit-balance/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/35-layers-and-boundaries-practical-setup/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/36-main-component-lowest-level-policy/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/37-services-architecture-boundaries-microservices/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/38-test-boundary-testing-as-system-part/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/39-clean-embedded-architecture-hardware-separation/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/40-details-introduction-interchangeable-parts/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/41-database-is-detail-persistence/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/42-web-is-detail-gui-history/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/43-framework-is-detail-coupling-risk/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/44-case-study-video-sales-system/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/45-missing-chapter-package-structure/index.md | - | - | 0 | 미채점 | - |
