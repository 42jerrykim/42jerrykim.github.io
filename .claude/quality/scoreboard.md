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
| content/collection/cleanarchitecture/06-introduction-software-design-architecture/index.md | 78.7 | 2026-07-18 | 3 | 에스컬레이션 | 항목3 구조(문단비율 34.8%), 항목1 인용 출처 미검증, 00장 커리큘럼 표 문구 불일치 |
| content/collection/cleanarchitecture/07-design-vs-architecture-definition/index.md | 88.6 | 2026-07-18 | 3 | 에스컬레이션 | 항목5 코드(OrderRepository 보조타입 미정의), 항목7 무관 태그 5개. 90점에 1.4점 차 |
| content/collection/cleanarchitecture/08-two-values-behavior-structure/index.md | 80.2 | 2026-07-18 | 3 | 에스컬레이션 | 항목2 판단기준 얕음, 항목4 우선순위 3중 반복, 항목5 OrderController 미정의 타입 |
| content/collection/cleanarchitecture/09-programming-paradigms-introduction/index.md | 78.1 | 2026-07-18 | 3 | 에스컬레이션 | 항목7 태그 6개 본문 불일치, 항목2 흔한오개념 절 없음 |
| content/collection/cleanarchitecture/10-paradigm-overview-three-types/index.md | 86.2 | 2026-07-18 | 3 | 에스컬레이션 | 항목7 태그 3개 본문 불일치, 항목3/4 리스트 의존·매핑 3중 반복 |
| content/collection/cleanarchitecture/11-structured-programming-goto-elimination/index.md | 87.7 | 2026-07-18 | 3 | 에스컬레이션 | 항목5 checkCustomerCredit 중복 정의, 항목1 "로마에서" 미검증 서술. 90점에 2.3점 차 |
| content/collection/cleanarchitecture/12-object-oriented-programming-polymorphism/index.md | 93.1 | 2026-07-18 | 3 | 통과 | 없음(경미: 플러그인 절 리드문단 부재, drawAll 클래스 밖 선언) |
| content/collection/cleanarchitecture/13-functional-programming-immutability/index.md | 94.6 | 2026-07-18 | 2 | 통과 | 없음(경미: 람다계산법 연도 서술 단순화, Order 생성자 방어적 복사 부재) |
| content/collection/cleanarchitecture/14-solid-principles-introduction/index.md | 94 | 2026-07-18 | 2 | 통과 | 없음(경미: SRP 정의 blockquote 옆 인라인 출처 미표기) |
| content/collection/cleanarchitecture/15-srp-single-responsibility-principle/index.md | 91.6 | 2026-07-18 | 2 | 통과 | 없음 |
| content/collection/cleanarchitecture/16-ocp-open-closed-principle/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 없음(경미: "두 가지 의미"·"요구사항" 절 리스트-only) |
| content/collection/cleanarchitecture/17-lsp-liskov-substitution-principle/index.md | 97 | 2026-07-18 | 2 | 통과 | 없음(경미: Algorithm 태그 본문 불일치) |
| content/collection/cleanarchitecture/18-isp-interface-segregation-principle/index.md | 90.1 | 2026-07-18 | 2 | 통과 | 없음(임계값 근접, 이후 보강 완료) |
| content/collection/cleanarchitecture/19-dip-dependency-inversion-principle/index.md | 97 | 2026-07-18 | 3 | 통과 | 없음(경미: 소스코드의존성 vs 제어흐름 절 문단 얇음) |
| content/collection/cleanarchitecture/20-component-principles-introduction/index.md | 92.2 | 2026-07-19 | 3 | 통과 | 없음 |
| content/collection/cleanarchitecture/21-components-deployment-units-history/index.md | 90.7 | 2026-07-19 | 2 | 통과 | 없음 |
| content/collection/cleanarchitecture/22-component-cohesion-rep-ccp-crp/index.md | 96.1 | 2026-07-19 | 3 | 통과 | 없음(경미: 문단비율 34.9%, 40% 기준 근소 미달이나 통과) |
| content/collection/cleanarchitecture/23-component-coupling-adp-sdp-sap/index.md | 97 | 2026-07-19 | 3 | 통과 | 없음 |
| content/collection/cleanarchitecture/24-architecture-introduction-system-design/index.md | 85.9 | 2026-07-19 | 3 | 에스컬레이션 | 항목2 학습목표 문항이 본문 흔한오해 절과 불일치, 항목7 태그 11개 본문 근거 약함. 90점에 4.1점 차 |
| content/collection/cleanarchitecture/25-what-is-architecture-system-lifecycle/index.md | 87.7 | 2026-07-19 | 3 | 에스컬레이션 | 항목5 정책/세부사항 분리 예제 미정의 타입, 항목1 1960년대 서술 미검증, 항목3 일부 절 표/리스트 의존. 90점에 2.3점 차 |
| content/collection/cleanarchitecture/26-independence-usecase-operation-development/index.md | 72.7 | 2026-07-19 | 3 | 에스컬레이션 | 항목7 무관 태그 6개(반복 재현), 항목3 계층/디커플링 소절 리스트·코드 의존 |
| content/collection/cleanarchitecture/27-boundaries-drawing-lines-plugin-architecture/index.md | 83.2 | 2026-07-19 | 3 | 에스컬레이션 | 항목5 WikiPagePersistence 구현체 컴파일 불가(throws 불일치, 미구현 메서드), 항목7 무관 태그 4개. 90점에 6.8점 차 |
| content/collection/cleanarchitecture/28-boundary-anatomy-monolith-to-services/index.md | 67 | 2026-07-19 | 3 | 에스컬레이션 | 항목1 ServiceLoader 메커니즘 서술 오류(치명결함), 항목5 코드 컴파일 불가 |
| content/collection/cleanarchitecture/29-policy-and-level-high-level-dependency/index.md | 84.7 | 2026-07-19 | 3 | 에스컬레이션 | 항목7 무관 태그 4개, 항목1 인용 페이지 미표기, 항목4 수준/변경빈도 절 중복. 90점에 5.3점 차 |
| content/collection/cleanarchitecture/30-business-rules-entities-usecases/index.md | 91.6 | 2026-07-19 | 3 | 에스컬레이션 | 항목1 L44-45 인용이 원저 두 문장을 하나로 합성한 비-verbatim 직접인용(치명결함), 태그 7개 data/tags.yaml 미등재. 90점 이상이나 치명결함 잔존으로 미통과 |
| content/collection/cleanarchitecture/31-screaming-architecture-intent-driven-structure/index.md | 92.2 | 2026-07-19 | 2 | 통과 | 없음(경미: 표 2개 리드인 문단 보강 여지) |
| content/collection/cleanarchitecture/32-clean-architecture-concentric-circles-dependency/index.md | 93.1 | 2026-07-19 | 2 | 통과 | 없음(경미: 일부 절 리드/해설 문단 보강 여지) |
| content/collection/cleanarchitecture/33-presenter-humble-object-testability/index.md | 90.7 | 2026-07-19 | 2 | 통과 | 없음(경미: DB/외부서비스 경계 코드 앞 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/34-partial-boundaries-cost-benefit-balance/index.md | 92.2 | 2026-07-19 | 2 | 통과 | 없음(경미: 표/다이어그램 앞 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/35-layers-and-boundaries-practical-setup/index.md | 90.7 | 2026-07-19 | 3 | 통과 | 없음(경미: 일부 절 리드 문단 보강 여지, 종결 인용문 재검증 권고) |
| content/collection/cleanarchitecture/36-main-component-lowest-level-policy/index.md | 96.1 | 2026-07-19 | 3 | 통과 | 없음 |
| content/collection/cleanarchitecture/37-services-architecture-boundaries-microservices/index.md | 91.3 | 2026-07-19 | 2 | 통과 | 없음(경미: 일부 절 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/38-test-boundary-testing-as-system-part/index.md | 92 | 2026-07-19 | 1 | 통과 | 없음(경미: 일부 절 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/39-clean-embedded-architecture-hardware-separation/index.md | 98.2 | 2026-07-19 | 3 | 통과 | 없음(경미: Mermaid 노드 ID 표기 관례 미준수) |
| content/collection/cleanarchitecture/40-details-introduction-interchangeable-parts/index.md | 96.1 | 2026-07-19 | 3 | 통과 | 없음(경미: 일부 절 문단 비율 보강 여지) |
| content/collection/cleanarchitecture/41-database-is-detail-persistence/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/42-web-is-detail-gui-history/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/43-framework-is-detail-coupling-risk/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/44-case-study-video-sales-system/index.md | - | - | 0 | 미채점 | - |
| content/collection/cleanarchitecture/45-missing-chapter-package-structure/index.md | - | - | 0 | 미채점 | - |
| content/collection/design-patterns/00-design-patterns-overview/index.md | 91 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/01-design-patterns-philosophy-and-history/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 없음(경미: 핵심메시지/결론 중복) |
| content/collection/design-patterns/02-pattern-analysis-framework/index.md | 91.3 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/03-oop-design-deep-understanding/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 없음(경미: 핵심메시지/결론 중복) |
| content/collection/design-patterns/04-factory-patterns-evolution/index.md | 91.6 | 2026-07-19 | 8 | 통과 | 없음 |
| content/collection/design-patterns/04-factory-patterns-evolution-practice/index.md | 92 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/05-singleton-controversial-pattern/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/05-singleton-controversial-pattern-practice/index.md | 96.1 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/06-builder-prototype-deep-understanding/index.md | 93 | 2026-07-19 | 5 | 통과 | 없음 |
| content/collection/design-patterns/06-builder-prototype-deep-understanding-practice/index.md | 93 | 2026-07-19 | 8 | 통과 | 없음 |
| content/collection/design-patterns/07-adapter-facade-interface-philosophy/index.md | 90.7 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/07-adapter-facade-interface-philosophy-practice/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/08-decorator-composite-recursive-beauty/index.md | 91.3 | 2026-07-18 | 3 | 통과 | 없음(경미: GUIExample의 Window/Label 미정의, 트리구조 Mermaid 권장) |
| content/collection/design-patterns/08-decorator-composite-recursive-beauty-practice/index.md | 97 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/09-proxy-pattern-multifaceted/index.md | 93.1 | 2026-07-19 | 5 | 통과 | 없음 |
| content/collection/design-patterns/09-proxy-pattern-multifaceted-practice/index.md | 93.1 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/10-bridge-flyweight-separation-efficiency/index.md | 91.3 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/10-bridge-flyweight-separation-efficiency-practice/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/11-observer-event-driven-architecture/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/11-observer-event-driven-architecture-practice/index.md | 92.2 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/12-strategy-state-algorithm-encapsulation/index.md | 97 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/12-strategy-state-algorithm-encapsulation-practice/index.md | 93.1 | 2026-07-19 | 5 | 통과 | 없음 |
| content/collection/design-patterns/13-command-chain-responsibility/index.md | 96.1 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/13-command-chain-responsibility-practice/index.md | 97 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/14-template-method-iterator-depth/index.md | 93.1 | 2026-07-19 | 9 | 통과 | 없음(경미: L985-986 표 앞 리드 문단 1곳 부재, 본문과 결속 약한 태그 일부) |
| content/collection/design-patterns/15-interpreter-mediator-parsing-coordination/index.md | 96.1 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/16-memento-visitor-state-operation-separation/index.md | 92.2 | 2026-07-18 | 3 | 통과 | 없음(경미: 데모 main() 축약, 결론/주의사항 중복) |
| content/collection/design-patterns/17-pattern-combinations-interactions/index.md | 97 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/18-functional-programming-design-patterns/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 없음 |
| content/collection/design-patterns/19-concurrency-distributed-patterns/index.md | 93.1 | 2026-07-19 | 5 | 통과 | 없음(채점 시 안전분류기 일시 unavailable — 결과 재확인 권장) |
| content/collection/design-patterns/20-ddd-design-patterns/index.md | 100 | 2026-07-19 | 5 | 통과 | 없음 |
| content/collection/design-patterns/20-ddd-design-patterns-practice/index.md | 97 | 2026-07-19 | 7 | 통과 | 없음 |
| content/collection/design-patterns/21-pattern-performance-optimization/index.md | 93 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/21-pattern-performance-optimization-practice/index.md | 97 | 2026-07-19 | 7 | 통과 | 없음 |
| content/collection/design-patterns/22-antipatterns-refactoring/index.md | 97 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/22-antipatterns-refactoring-practice/index.md | 94.6 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/23-pattern-code-review-design-review/index.md | 96.1 | 2026-07-19 | 6 | 통과 | 없음 |
| content/collection/design-patterns/23-pattern-code-review-design-review-practice/index.md | 100 | 2026-07-19 | 5 | 통과 | 없음 |
| content/collection/design-patterns/24-discovering-defining-new-patterns/index.md | 93 | 2026-07-19 | 5 | 통과 | 없음 |
| content/collection/design-patterns/24-discovering-defining-new-patterns-practice/index.md | 97 | 2026-07-19 | 5 | 통과 | 없음 |
