# 품질 점수판 (Quality Scoreboard)

`post-quality-loop` 루프의 세션 간 상태(state)다. 글별 최신 채점 결과를 기록해, 자율 모드가 "미채점/최저점 글"을 고르는 인덱스로 쓴다.

- **상태 값**: `미채점` / `진행중` / `통과` / `에스컬레이션`
- **점수**: 0~100 (루브릭 총점). 미채점이면 `-`.
- **채점일**: 터미널 오늘 날짜(`yyyy-MM-dd`).
- **루브릭버전**: 채점 당시 [`rubric.md`](rubric.md)의 "루브릭 버전"(예: `1.0`). 미채점이면 `-`.
- **만료 규칙**: 아래 두 조건 중 하나라도 해당하면 그 행의 `통과`/`에스컬레이션` 판정은 **즉시 무효**이며, 선정 로직(`SKILL.md` Stage 0)은 해당 글을 `미채점`과 동일하게 취급해 재채점 대상에 포함한다. 무효 판정 자체는 표의 `상태` 값을 바꾸지 않는다(재채점이 실제로 일어난 시점에만 갱신) — 판별은 선정 시점에 계산한다.
  1. **버전 불일치**: 행의 `루브릭버전`이 `rubric.md`의 현재 버전과 다르면 채점일과 무관하게 즉시 무효.
  2. **기간 만료**: 버전이 같아도 `채점일`로부터 **365일**이 지나면 무효.
- **시딩**: 본문(아래 표)이 비어 있으면 `SKILL.md`의 "점수판 운영 — 시딩" 절차로 게시글을 1회 등록한다.

| 글 경로 | 최신점수 | 채점일 | 반복수 | 상태 | 루브릭버전 | 주요 미달항목 |
|---------|---------:|--------|-------:|------|:----------:|---------------|
| content/collection/multithreading-design-patterns/12-coroutine-reinterpretation/index.md | 93.1 | 2026-07-09 | 2 | 통과 | 1.0 | 없음(경미: ActiveObject 104줄 코드 블록의 문단 비율) |
| content/collection/multithreading-design-patterns/13-lockfree-reclamation/index.md | 96.1 | 2026-07-09 | 2 | 통과 | 1.0 | 없음 |
| content/collection/cleanarchitecture/00-clean-architecture-overview-introduction/index.md | 94.0 | 2026-07-20 | 6 | 통과 | 1.0 | 없음(경미: OrderController placeOrder() 반환타입 제네릭 불일치, 어댑터 블록 내 public 클래스 2개 공존, Concentric-Circles 태그 tags.yaml 미등재) |
| content/collection/cleanarchitecture/01-architecture-history-evolution-introduction/index.md | 91 | 2026-07-18 | 2 | 통과 | 1.0 | 없음(경미: 흔한 오해 절 부재, 다음장 하이퍼링크 없음) |
| content/post/2026/2026-07-25-omniroute-ai-gateway/index.md | 100 | 2026-07-25 | 2 | 통과 | 1.0 | 없음 |
| content/collection/cleanarchitecture/02-layered-architecture-limitations-history/index.md | 90.7 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: Reenskaug 1979 인용 서지사항 검증 링크 부재, 프레임워크종속성/계층건너뛰기 절 코드 뒤 해설 여지) |
| content/collection/cleanarchitecture/03-hexagonal-architecture-ports-adapters/index.md | 96.1 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: 장점/한계 절 일부 문단 확장 여지) |
| content/collection/cleanarchitecture/04-onion-architecture-domain-centric-design/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 1.0 | 없음(경미: 패키지구조 절 리드문단 부재, 코드 보조타입 미정의) |
| content/collection/cleanarchitecture/05-clean-architecture-birth-uncle-bob/index.md | 97 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: 미승인 태그 11개 data/tags.yaml 미등재, Guide 태그 본문 근거 약함) |
| content/collection/cleanarchitecture/06-introduction-software-design-architecture/index.md | 94.6 | 2026-07-20 | 6 | 통과 | 1.0 | 없음(경미: "천국: 좋은 아키텍처" 소절 리스트 후 연결문단 여지) |
| content/collection/cleanarchitecture/07-design-vs-architecture-definition/index.md | 96.1 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: 일부 절 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/08-two-values-behavior-structure/index.md | 96.1 | 2026-07-20 | 5 | 통과 | 1.0 | 없음(경미: "소프트웨어의 어원"/"논리적 반박" 절 리드 문단 여지, 인용 4회 반복에 장 번호 미표기) |
| content/collection/cleanarchitecture/09-programming-paradigms-introduction/index.md | 94.0 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: Repository/MySqlRepository/MongoRepository 다중 public 공존, FP 스니펫 미래핑, 신규 태그 7개 tags.yaml 미등재) |
| content/collection/cleanarchitecture/10-paradigm-overview-three-types/index.md | 92.2 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: goto 절 연결문단, "왜 세 가지뿐" 중복 정리 여지) |
| content/collection/cleanarchitecture/11-structured-programming-goto-elimination/index.md | 94.6 | 2026-07-20 | 5 | 통과 | 1.0 | 없음(경미: L46 Dijkstra 인용 blockquote 서식 보강 여지) |
| content/collection/cleanarchitecture/12-object-oriented-programming-polymorphism/index.md | 93.1 | 2026-07-18 | 3 | 통과 | 1.0 | 없음(경미: 플러그인 절 리드문단 부재, drawAll 클래스 밖 선언) |
| content/collection/cleanarchitecture/13-functional-programming-immutability/index.md | 94.6 | 2026-07-18 | 2 | 통과 | 1.0 | 없음(경미: 람다계산법 연도 서술 단순화, Order 생성자 방어적 복사 부재) |
| content/collection/cleanarchitecture/14-solid-principles-introduction/index.md | 94 | 2026-07-18 | 2 | 통과 | 1.0 | 없음(경미: SRP 정의 blockquote 옆 인라인 출처 미표기) |
| content/collection/cleanarchitecture/15-srp-single-responsibility-principle/index.md | 91.6 | 2026-07-18 | 2 | 통과 | 1.0 | 없음 |
| content/collection/cleanarchitecture/16-ocp-open-closed-principle/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 1.0 | 없음(경미: "두 가지 의미"·"요구사항" 절 리스트-only) |
| content/collection/cleanarchitecture/17-lsp-liskov-substitution-principle/index.md | 97 | 2026-07-18 | 2 | 통과 | 1.0 | 없음(경미: Algorithm 태그 본문 불일치) |
| content/collection/cleanarchitecture/18-isp-interface-segregation-principle/index.md | 90.1 | 2026-07-18 | 2 | 통과 | 1.0 | 없음(임계값 근접, 이후 보강 완료) |
| content/collection/cleanarchitecture/19-dip-dependency-inversion-principle/index.md | 97 | 2026-07-18 | 3 | 통과 | 1.0 | 없음(경미: 소스코드의존성 vs 제어흐름 절 문단 얇음) |
| content/collection/cleanarchitecture/20-component-principles-introduction/index.md | 92.2 | 2026-07-19 | 3 | 통과 | 1.0 | 없음 |
| content/collection/cleanarchitecture/21-components-deployment-units-history/index.md | 90.7 | 2026-07-19 | 2 | 통과 | 1.0 | 없음 |
| content/collection/cleanarchitecture/22-component-cohesion-rep-ccp-crp/index.md | 96.1 | 2026-07-19 | 3 | 통과 | 1.0 | 없음(경미: 문단비율 34.9%, 40% 기준 근소 미달이나 통과) |
| content/collection/cleanarchitecture/23-component-coupling-adp-sdp-sap/index.md | 97 | 2026-07-19 | 3 | 통과 | 1.0 | 없음 |
| content/collection/cleanarchitecture/24-architecture-introduction-system-design/index.md | 97.0 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: Technology/Framework-Independence 태그 근거 보강 여지) |
| content/collection/cleanarchitecture/25-what-is-architecture-system-lifecycle/index.md | 93.1 | 2026-07-20 | 5 | 통과 | 1.0 | 없음(경미: 표-헤딩 전환 2곳, MySqlOrderRepository 스텁 로직 보강 여지) |
| content/collection/cleanarchitecture/26-independence-usecase-operation-development/index.md | 90.1 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: "네 가지 독립성"/"디커플링 모드" 헤딩 리드문단 여지, 신규태그 9개 tags.yaml 미등재이나 승인태그 16개로 하한 충족. 통과 후 Throughput 표기·Encapsulation 근거 보강 완료) |
| content/collection/cleanarchitecture/27-boundaries-drawing-lines-plugin-architecture/index.md | 94.0 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: PaymentGateway 예제 Payment/PaymentResult 미정의, MySqlWikiPagePersistence try-with-resources 미사용, 신규 태그 4개 tags.yaml 미등재) |
| content/collection/cleanarchitecture/28-boundary-anatomy-monolith-to-services/index.md | 91.6 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: package/import 서술과 코드 정합성 보강 여지) |
| content/collection/cleanarchitecture/29-policy-and-level-high-level-dependency/index.md | 93.1 | 2026-07-20 | 5 | 통과 | 1.0 | 없음(경미: "수준의 정의" 표·"암호화 프로그램" 하위 절 전환 문단 보강 여지) |
| content/collection/cleanarchitecture/30-business-rules-entities-usecases/index.md | 100 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(Tier 0 개선: 인용 재검증 완료, 코드 자기완결화, 태그 재구성) |
| content/collection/cleanarchitecture/31-screaming-architecture-intent-driven-structure/index.md | 92.2 | 2026-07-19 | 2 | 통과 | 1.0 | 없음(경미: 표 2개 리드인 문단 보강 여지) |
| content/collection/cleanarchitecture/32-clean-architecture-concentric-circles-dependency/index.md | 93.1 | 2026-07-19 | 2 | 통과 | 1.0 | 없음(경미: 일부 절 리드/해설 문단 보강 여지) |
| content/collection/cleanarchitecture/33-presenter-humble-object-testability/index.md | 90.7 | 2026-07-19 | 2 | 통과 | 1.0 | 없음(경미: DB/외부서비스 경계 코드 앞 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/34-partial-boundaries-cost-benefit-balance/index.md | 92.2 | 2026-07-19 | 2 | 통과 | 1.0 | 없음(경미: 표/다이어그램 앞 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/35-layers-and-boundaries-practical-setup/index.md | 90.7 | 2026-07-19 | 3 | 통과 | 1.0 | 없음(경미: 일부 절 리드 문단 보강 여지, 종결 인용문 재검증 권고) |
| content/collection/cleanarchitecture/36-main-component-lowest-level-policy/index.md | 96.1 | 2026-07-19 | 3 | 통과 | 1.0 | 없음 |
| content/collection/cleanarchitecture/37-services-architecture-boundaries-microservices/index.md | 91.3 | 2026-07-19 | 2 | 통과 | 1.0 | 없음(경미: 일부 절 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/38-test-boundary-testing-as-system-part/index.md | 92 | 2026-07-19 | 1 | 통과 | 1.0 | 없음(경미: 일부 절 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/39-clean-embedded-architecture-hardware-separation/index.md | 98.2 | 2026-07-19 | 3 | 통과 | 1.0 | 없음(경미: Mermaid 노드 ID 표기 관례 미준수) |
| content/collection/cleanarchitecture/40-details-introduction-interchangeable-parts/index.md | 96.1 | 2026-07-19 | 3 | 통과 | 1.0 | 없음(경미: 일부 절 문단 비율 보강 여지) |
| content/collection/cleanarchitecture/41-database-is-detail-persistence/index.md | 90.4 | 2026-07-20 | 4 | 통과 | 1.0 | 없음(경미: 항목3 문단비율 21.5%로 40% 기준 미달이나 통과, DB교체 시나리오 절 잔여 연속 블록 1곳) |
| content/collection/cleanarchitecture/42-web-is-detail-gui-history/index.md | 96.1 | 2026-07-19 | 3 | 통과 | 1.0 | 없음(경미: 일부 절 문단 비율 보강 여지) |
| content/collection/cleanarchitecture/43-framework-is-detail-coupling-risk/index.md | 96.1 | 2026-07-19 | 2 | 통과 | 1.0 | 없음(경미: 일부 절 문단 비율 보강 여지) |
| content/collection/cleanarchitecture/44-case-study-video-sales-system/index.md | 93.1 | 2026-07-19 | 3 | 통과 | 1.0 | 없음(경미: 태그 1개 불일치, 문단 비율 보강 여지) |
| content/collection/cleanarchitecture/45-missing-chapter-package-structure/index.md | 94.6 | 2026-07-19 | 2 | 통과 | 1.0 | 없음(경미: L38 서술 완화 여지) |
| content/collection/design-patterns/00-design-patterns-overview/index.md | 91 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/01-design-patterns-philosophy-and-history/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 1.0 | 없음(경미: 핵심메시지/결론 중복) |
| content/collection/design-patterns/02-pattern-analysis-framework/index.md | 91.3 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/03-oop-design-deep-understanding/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 1.0 | 없음(경미: 핵심메시지/결론 중복) |
| content/collection/design-patterns/04-factory-patterns-evolution/index.md | 91.6 | 2026-07-19 | 8 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/04-factory-patterns-evolution-practice/index.md | 92 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/05-singleton-controversial-pattern/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/05-singleton-controversial-pattern-practice/index.md | 96.1 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/06-builder-prototype-deep-understanding/index.md | 93 | 2026-07-19 | 5 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/06-builder-prototype-deep-understanding-practice/index.md | 93 | 2026-07-19 | 8 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/07-adapter-facade-interface-philosophy/index.md | 90.7 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/07-adapter-facade-interface-philosophy-practice/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/08-decorator-composite-recursive-beauty/index.md | 91.3 | 2026-07-18 | 3 | 통과 | 1.0 | 없음(경미: GUIExample의 Window/Label 미정의, 트리구조 Mermaid 권장) |
| content/collection/design-patterns/08-decorator-composite-recursive-beauty-practice/index.md | 97 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/09-proxy-pattern-multifaceted/index.md | 93.1 | 2026-07-19 | 5 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/09-proxy-pattern-multifaceted-practice/index.md | 93.1 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/10-bridge-flyweight-separation-efficiency/index.md | 91.3 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/10-bridge-flyweight-separation-efficiency-practice/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/11-observer-event-driven-architecture/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/11-observer-event-driven-architecture-practice/index.md | 92.2 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/12-strategy-state-algorithm-encapsulation/index.md | 97 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/12-strategy-state-algorithm-encapsulation-practice/index.md | 93.1 | 2026-07-19 | 5 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/13-command-chain-responsibility/index.md | 96.1 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/13-command-chain-responsibility-practice/index.md | 97 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/14-template-method-iterator-depth/index.md | 93.1 | 2026-07-19 | 9 | 통과 | 1.0 | 없음(경미: L985-986 표 앞 리드 문단 1곳 부재, 본문과 결속 약한 태그 일부) |
| content/collection/design-patterns/15-interpreter-mediator-parsing-coordination/index.md | 96.1 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/16-memento-visitor-state-operation-separation/index.md | 92.2 | 2026-07-18 | 3 | 통과 | 1.0 | 없음(경미: 데모 main() 축약, 결론/주의사항 중복) |
| content/collection/design-patterns/17-pattern-combinations-interactions/index.md | 97 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/18-functional-programming-design-patterns/index.md | 93.1 | 2026-07-19 | 4 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/19-concurrency-distributed-patterns/index.md | 93.1 | 2026-07-19 | 5 | 통과 | 1.0 | 없음(채점 시 안전분류기 일시 unavailable — 결과 재확인 권장) |
| content/collection/design-patterns/20-ddd-design-patterns/index.md | 100 | 2026-07-19 | 5 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/20-ddd-design-patterns-practice/index.md | 97 | 2026-07-19 | 7 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/21-pattern-performance-optimization/index.md | 93 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/21-pattern-performance-optimization-practice/index.md | 97 | 2026-07-19 | 7 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/22-antipatterns-refactoring/index.md | 97 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/22-antipatterns-refactoring-practice/index.md | 94.6 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/23-pattern-code-review-design-review/index.md | 96.1 | 2026-07-19 | 6 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/23-pattern-code-review-design-review-practice/index.md | 100 | 2026-07-19 | 5 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/24-discovering-defining-new-patterns/index.md | 93 | 2026-07-19 | 5 | 통과 | 1.0 | 없음 |
| content/collection/design-patterns/24-discovering-defining-new-patterns-practice/index.md | 97 | 2026-07-19 | 5 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/00-getting-started-computer-terms/index.md | 95.2 | 2026-07-22 | 3 | 통과 | 1.0 | 없음(경미: 표 의존도가 높아 항목3에서 표를 빼면 갈래 목록 자체는 문단만으로 전달 안 됨) |
| content/collection/computerterms/aba-problem/index.md | 92.8 | 2026-07-22 | 1 | 통과 | 1.0 | 없음(경미: IEEE 링크 WAF 챌린지로 자동검증 불가) |
| content/collection/computerterms/aicd/index.md | 96.1 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/algorithm/index.md | 94.6 | 2026-07-22 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/algorithm_efficiency/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/algotithm_classify/index.md | 98.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/arrays-and-linked-lists/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/atomic-operations-and-cas/index.md | 100 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/authentication-and-authorization/index.md | 97 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/cache-hierarchy/index.md | 91 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/caching-and-invalidation/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/cap-theorem-and-consensus/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음(경미: Reliability 태그 본문 근거 약함) |
| content/collection/computerterms/cdn-caching/index.md | 100 | 2026-07-22 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/ci-cd-and-testing-types/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/circuit-breaker/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 1.0 | 없음(경미: Release It! 장 번호 표기를 "Stability Patterns" 부로 완화) |
| content/collection/computerterms/closures-and-scope/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/code-review/index.md | 91.6 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/compilers-and-interpreters/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/containers-and-virtualization/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/content-delivery-networks/index.md | 91.6 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/content-negotiation/index.md | 97 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/cookies-and-local-storage/index.md | 97 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/coroutines-and-async-await/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/coupling-and-cohesion/index.md | 97 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/cpu-and-pipelining/index.md | 94.6 | 2026-07-22 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/cpu-scheduling/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/daemons-and-zombie-processes/index.md | 98.2 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/deadlocks/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/design-patterns-overview/index.md | 95.2 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/digital-signatures-and-certificates/index.md | 97 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/dns-and-sockets/index.md | 97 | 2026-07-22 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/dynamic-programming/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/encryption-and-hashing/index.md | 93.4 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/event-driven-architecture/index.md | 94 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/event-sourcing/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/factory-pattern/index.md | 95.2 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/feature-flags/index.md | 94 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/file-systems/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/firewalls-and-nat/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/floating-point-representation/index.md | 91 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/forward-and-reverse-proxies/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/full-text-search-indexes/index.md | 97 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/functional-programming-paradigm/index.md | 100 | 2026-07-24 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/garbage-collection/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/generics-and-polymorphism/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/graphs/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/greedy-algorithms/index.md | 97 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/grpc/index.md | 95.2 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/hash-tables/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/heaps-and-priority-queues/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/hexagonal-architecture/index.md | 97 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/http-and-https/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/http3-and-quic/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/idempotency/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/inter-process-communication/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/interrupts-and-system-calls/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/load-balancing/index.md | 91.6 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/memory-management/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/memory-safety-and-ownership/index.md | 97 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/message-queues/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/multilevel-caching/index.md | 100 | 2026-07-22 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/mvc-and-mvvm/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/mvcc/index.md | 96.1 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/normalization-and-indexes/index.md | 97 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/nosql-and-query-optimization/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/oauth-and-oidc/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/observer-pattern/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/osi-and-tcp-ip/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/processes-and-threads/index.md | 97 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/query-planner-internals/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/race-conditions-and-locks/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/rate-limiting/index.md | 97 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/refactoring-and-code-smells/index.md | 97 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/registers-and-isa/index.md | 98.2 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/rest-and-graphql/index.md | 97 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/searching-algorithms/index.md | 91.6 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/segment-trees/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/semantic-versioning/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/semaphores-and-monitors/index.md | 91.6 | 2026-07-22 | 1 | 통과 | 1.0 | 없음(경미: 브린치 한센 연도 정정 반영) |
| content/collection/computerterms/server-sent-events/index.md | 97 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/sharding-and-replication/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/shortest-path-algorithms/index.md | 100 | 2026-07-22 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/signals/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/simd/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/skip-lists/index.md | 97 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/solid-principles-overview/index.md | 100 | 2026-07-24 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/sorting-algorithms/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/stacks-and-queues/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/thread-pools/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음(경미: Debugging 태그를 Throughput으로 교체) |
| content/collection/computerterms/time-series-databases/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/time_complexity/index.md | 92.8 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/transaction-isolation-levels/index.md | 94 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/trees/index.md | 97 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/tries/index.md | 93.4 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/type-systems/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/union-find/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/vector-clocks/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/version-control-internals/index.md | 94.6 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/von-neumann-architecture/index.md | 100 | 2026-07-22 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/web-application-firewalls/index.md | 100 | 2026-07-24 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/web-vulnerabilities/index.md | 94.6 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/webhooks/index.md | 100 | 2026-07-22 | 3 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/websockets-and-cors/index.md | 100 | 2026-07-24 | 2 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/write-through-and-write-back/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 1.0 | 없음 |
| content/collection/computerterms/zero-trust-security/index.md | 94 | 2026-07-24 | 1 | 통과 | 1.0 | 없음 |
| content/post/2026/2026-07-22-p95-p99-latency-percentile-guide/index.md | 91 | 2026-07-22 | 1 | 통과 | 1.0 | 없음(경미: "이 글을 읽은 후" 학습 성과 목표 절 부재, Bigtable SRE Book 챕터 인용 정밀도, cacm.acm.org 대체 접근 경로 미병기) |
| content/post/2026/2026-07-22-iterm2-vs-securecrt-logging-comparison/index.md | 95 | 2026-07-22 | 2 | 통과 | 1.0 | 없음(선택: "이 글에서 다루는 내용" 미리보기 불릿을 문단으로 축약하면 구조 항목 여지 있으나 통과에 영향 없음) |
| content/post/2026/2026-07-22-qbittorrent-vs-utorrent-comparison/index.md | 94.6 | 2026-07-22 | 3 | 통과 | 1.0 | 없음(3차 채점 후 L99 Cloudwards 인용 정밀도를 추가로 정정, 재채점 생략) |
| content/collection/cmd/command-categories/index.md | 96.1 | 2026-07-22 | 3 | 통과 | 1.0 | 없음(경미: 네트워크·기타 유틸리티 절 판단 기준 문단 여지, 코드블록 언어 태그 미통일) |
| content/post/2026/2026-07-22-pikvm-v4-mini-review/index.md | 93.1 | 2026-07-22 | 3 | 통과 | 1.0 | 없음(경미: RDP(Remote Desktop Protocol) 태그 본문 근거 약함, 종합 평가 문단이 장단점 절과 일부 재진술) |
| content/collection/TV-Show/2026/2026-07-22-young-sheldon-medford-texas-setting-filming-location/index.md | 94.6 | 2026-07-25 | 12 | 통과 | 1.0 | 없음(경미: L96 체로키 카운티 소속 서술의 팬 위키 원문 링크 미첨부, L108 쿠퍼가 외경 거리 매체별 상이(2/3/6마일) 각주 미표기). 12회차에서 안티패딩·구조 결함 해소: "정리" 절(종합평가와 중복)을 삭제하고, "확인 전 체크리스트"·"이 글을 읽은 후 확인할 것" 중복 닫는 절을 "확인 체크리스트" 하나로 통합(읽기 전/읽은 후 하위 소절), "다른 시트콤 비교" 절의 1문장 판단기준을 질문유형·층위·절·오류 4열 표로 확장. 11회차까지의 구조적 긴장(좁은 범위 특집 vs 정식 리뷰 기대)은 critic이 "정식 Act5 리뷰가 같은 컬렉션에 상호링크로 존재하므로 이 특집에 강제하지 않음"으로 판단해 해소 |
| content/collection/optimization-00-series-overview/00-introduction/index.md | 96 | 2026-07-25 | 2 | 통과 | 1.0 | 없음(경미: "권장 큰 줄기"·"왜 이 로드맵인가" 절 그룹핑 서술 일부 중복, 일부 범용 태그 본문 결속 약함) |
| content/collection/optimization-01-profiling/00-introduction/index.md | 83.5 | 2026-07-25 | 3 | 에스컬레이션 | 1.0 | 치명결함 0건이나 3회 반복 후 90점 미달. 잔여: L81 Intel VTune "XPU Offload Analysis(NPU 통합)" 명칭 미검증, L91 "Polar Signals 사례" 출처 미표기, 04번 챕터 핵심내용에 Ftrace 미병기. 사람 검토 후 추가 반복 여부 판단 필요 |
| content/collection/optimization-01-profiling/01-microbenchmark-design/index.md | 100 | 2026-07-25 | 1 | 통과 | 1.0 | 없음 |
| content/collection/optimization-01-profiling/02-google-benchmark/index.md | 100 | 2026-07-25 | 1 | 통과 | 1.0 | 없음(1차 채점에서 릴리스일 오탐 있었으나 GitHub API 재검증 결과 본문이 정확함을 확인, 수정 없이 통과) |
| content/collection/optimization-01-profiling/03-sampling-profiling/index.md | 94.6 | 2026-07-25 | 1 | 통과 | 1.0 | 없음(경미: L74 VTune 릴리스 일자 검증 여지) |
| content/collection/optimization-01-profiling/04-tracing-profiling/index.md | 91.6 | 2026-07-25 | 1 | 통과 | 1.0 | 없음(경미: L70 Tracy 릴리스 시기 오표기(2026 상반기→실제 2025-12), perfetto_demo.cc 트레이스 세션 시작/저장 로직 생략) |
| content/collection/optimization-01-profiling/05-flame-graph/index.md | 94.6 | 2026-07-25 | 1 | 통과 | 1.0 | 없음(경미: ACM Queue 권/호 검증 여지, off-CPU 오버헤드 정량 근거 보강 여지) |
| content/collection/optimization-01-profiling/06-intel-vtune/index.md | 100 | 2026-07-25 | 1 | 통과 | 1.0 | 없음 |
| content/collection/optimization-01-profiling/07-linux-perf-advanced/index.md | 100 | 2026-07-25 | 1 | 통과 | 1.0 | 없음 |
| content/collection/optimization-01-profiling/08-hardware-counters/index.md | 96.1 | 2026-07-25 | 1 | 통과 | 1.0 | 없음(경미: 코드/출력 블록 연속 구간 문단 보강 여지, Yasin 논문 직접 링크 여지) |
| content/collection/optimization-01-profiling/09-tail-latency/index.md | 100 | 2026-07-25 | 1 | 통과 | 1.0 | 없음 |
| content/collection/optimization-01-profiling/10-statistical-benchmarking/index.md | 94.6 | 2026-07-25 | 1 | 통과 | 1.0 | 없음(경미: L72 Kalibera&Jones venue 오표기 OOPSLA/ISMM→ISMM) |
| content/collection/optimization-01-profiling/11-continuous-profiling/index.md | 94.6 | 2026-07-25 | 1 | 통과 | 1.0 | 없음(경미: Pyroscope/Parca 연혁 인용 링크 여지) |
| content/collection/optimization-01-profiling/12-performance-ab-testing/index.md | 97.0 | 2026-07-26 | 1 | 통과 | 1.0 | 없음(경미: L34-42 비승인 태그 9개 data/tags.yaml 미등재, L73 Spinnaker 카나리 문서 "첫머리" 배치 서술 검증 여지) |
| content/collection/optimization-01-profiling/13-amd-uprof/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-01-profiling/14-windows-etw/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-01-profiling/15-valgrind-callgrind/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-01-profiling/16-bpf-profiling/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-01-profiling/17-distributed-tracing-overhead/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-01-profiling/18-profiling-workflow-guide/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-01-profiling/19-profiler-output-interpretation/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-01-profiling/20-memory-profiling-heap/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/00-introduction/index.md | 96.1 | 2026-07-25 | 1 | 통과 | 1.0 | 없음(경미: L238 트랙 읽기 순서 요약이 L128과 일부 중복, 태그 표기 결합형 통일 여지) |
| content/collection/optimization-02-cpp-language/01-cpp-execution-model-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/02-smart-pointer-cost-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/03-abstraction-cost/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/04-stl-container-cost/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/05-string-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/06-object-lifetime/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/07-temporary-removal/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/08-templates-constexpr/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/09-modern-cpp-features/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/10-coroutine-performance/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/11-exception-deep-dive/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/12-inlining-techniques/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/13-variant-optional-expected/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/14-span-and-views/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/15-lambda-performance/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/16-small-buffer-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/17-parameter-passing/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/18-abi-link-performance-boundaries/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-02-cpp-language/19-type-erasure-cost-patterns/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/00-introduction/index.md | 96.1 | 2026-07-25 | 3 | 통과 | 1.0 | 없음(경미: L99/L139 추천 읽기 순서 표현 불일치) |
| content/collection/optimization-03-compiler/01-optimization-flags/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/02-lto-thinlto/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/03-pgo-workflow/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/04-compiler-comparison/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/05-inlining-diagnostics/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/06-code-generation-analysis/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/07-function-multiversioning/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/08-compiler-intrinsics/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/09-sanitizer-overhead/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/10-debug-info-and-performance/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/11-cpp20-modules/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/12-build-parallelization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/13-static-analyzer/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/14-bolt-post-link-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-03-compiler/15-autofdo/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/00-introduction/index.md | 97.0 | 2026-07-25 | 2 | 통과 | 1.0 | 없음(경미: Networking·IO·Testing 등 본문 결속 약한 범용 태그 다수, 16번 챕터 mimalloc 미병기) |
| content/collection/optimization-04-memory-allocation/01-container-cost-model/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/02-allocation-strategy/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/03-custom-allocator/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/04-pmr-allocator/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/05-aos-vs-soa/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/06-cache-friendly-patterns/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/07-padding-alignment/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/08-large-pages/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/09-numa-allocation/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/10-memory-fragmentation/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/11-memory-bandwidth/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/12-stack-vs-heap/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/13-virtual-memory-management/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/14-memory-leak-detection/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/15-memory-lifetime-cacheline-intuition/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-04-memory-allocation/16-global-allocator-tuning/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/00-introduction/index.md | 88.9 | 2026-07-25 | 3 | 에스컬레이션 | 1.0 | 치명결함 0건이나 3회 반복 후 90점 근소 미달. 잔여: "다루지 않는 것" 절에 캐시 일관성/메모리 모델·SIMD 범위 밖 명시 부재, 1차 출처 1개 추가 여지 |
| content/collection/optimization-05-cpu-microarchitecture/01-cpu-pipeline-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/02-branch-prediction/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/03-cache-hierarchy/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/04-cache-miss-analysis/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/05-ilp-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/06-out-of-order-execution/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/07-tlb-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/08-modern-cpu-architecture/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/09-hardware-performance-counters/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/10-speculative-execution/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/11-frequency-scaling/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/12-power-management/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/13-apple-silicon-architecture/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/14-smt-hyperthreading/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/15-uop-cache-dsb/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/16-risc-v-architecture/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/17-frontend-vs-backend-bound/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-05-cpu-microarchitecture/18-dependency-chains-port-pressure/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/00-introduction/index.md | 96.1 | 2026-07-25 | 3 | 통과 | 1.0 | 없음(경미: "달성할 목표"·"평가 기준" 절 일부 중복, 네비게이션 절 2개 중복 여지) |
| content/collection/optimization-06-os-runtime/01-context-switch-cost/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/02-syscall-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/03-cpu-pinning-affinity/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/04-numa-cpu-affinity/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/05-realtime-scheduling/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/06-precise-time-measurement/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/07-kernel-bypass-overview/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/08-io-uring-overview/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/09-xdp-ebpf-overview/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/10-huge-tlb-pages/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/11-container-performance/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/12-irq-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/13-cgroups-v2/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/14-memory-locking/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/15-signal-handling/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/16-process-vs-thread/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/17-ebpf-kernel-performance-safety/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-06-os-runtime/18-cloud-tail-latency/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/00-introduction/index.md | 95.2 | 2026-07-25 | 2 | 통과 | 1.0 | 없음(경미: "책임지는 범위"·"다루지 않는 것" 리스트 앞 연결 문단 여지, Intel 링크 WebFetch 403이나 실제 접근 가능) |
| content/collection/optimization-07-concurrency/01-synchronization-cost-analysis/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/02-lock-selection-criteria/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/03-false-sharing-avoidance/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/04-memory-model-practical/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/05-lock-free-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/06-lock-free-data-structures/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/07-hazard-pointers-rcu/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/08-spsc-mpmc-queues/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/09-cpp20-atomics/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/10-thread-pool-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/11-coroutine-concurrency/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/12-wait-free-programming/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/13-jthread-stop-token/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/14-seqlock-pattern/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/15-thread-local-storage/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/16-executors-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/17-senders-receivers-cpp26/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/18-parallel-execution-policies/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/19-condition-variable-patterns/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/20-barrier-latch/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-07-concurrency/21-thread-per-core-io-uring/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/00-introduction/index.md | 95.2 | 2026-07-25 | 3 | 통과 | 1.0 | 없음(경미: 측정 항목 리스트 근거 문단 여지) |
| content/collection/optimization-08-optimization-techniques/01-simd-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/02-simd-intrinsics-practical/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/03-avx512-avx10-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/04-auto-vectorization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/05-prefetch-strategy/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/06-branchless-programming/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/07-hand-written-assembly/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/08-lookup-table-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/09-bit-manipulation-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/10-hotpath-extreme-tuning/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/11-maintainability-tradeoff/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/12-arm-neon-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/13-portable-simd-libraries/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/14-cpp26-std-simd/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/15-cache-oblivious-algorithms/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/16-gpu-offloading-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/17-ai-inference-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-08-optimization-techniques/18-simd-string-processing/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/00-introduction/index.md | 100 | 2026-07-25 | 2 | 통과 | 1.0 | 없음 |
| content/collection/optimization-09-io-network/01-io-cost-intuition/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/02-io-patterns-cost/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/03-async-io-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/04-io-uring-advanced/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/05-iocp-windows-io/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/06-zero-copy-techniques/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/07-memory-mapped-io/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/08-direct-io/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/09-filesystem-characteristics/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/10-block-device-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/11-io-multiplexing-patterns/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/12-vectored-io/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/13-posix-aio-vs-io-uring/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/14-database-io-patterns/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/15-file-locking-performance/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/16-storage-stack-customization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-09-io-network/17-logging-performance-strategy/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/00-introduction/index.md | 92.2 | 2026-07-25 | 1 | 통과 | 1.0 | 없음(경미: description 118자로 하한 근접, 범위/경계 리스트 문단 비중 29%, WebTransport Baseline 기준 명시 여지) |
| content/collection/optimization-10-network/01-network-latency-intuition/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/02-network-latency-structure/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/03-socket-options-tuning/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/04-tcp-performance-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/05-udp-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/06-serialization-performance-comparison/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/07-zero-copy-serialization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/08-next-gen-zero-copy-formats/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/09-protocol-design/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/10-message-framing/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/11-dpdk-advanced/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/12-xdp-ebpf-network-advanced/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/13-rdma-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/14-ultra-ethernet-consortium/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/15-grpc-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/16-quic-protocol/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/17-tls-ssl-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/18-connection-pooling/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/19-websocket-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/20-http2-http3/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-10-network/21-network-compression-strategy/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/00-introduction/index.md | 91.3 | 2026-07-25 | 2 | 통과 | 1.0 | 없음(경미: "범위와 경계" Mermaid 단독 의존, Phase별 궤적과 커리큘럼 표 일부 중복) |
| content/collection/optimization-11-design-decisions/01-performance-terminology-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/02-when-to-optimize/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/03-when-to-stop-optimizing/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/04-readability-vs-performance/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/05-performance-budgeting/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/06-slo-sla-definition/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/07-latency-vs-throughput/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/08-low-latency-architecture-patterns/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/09-caching-strategy/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/10-database-access-optimization/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/11-team-performance-culture/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/12-performance-code-review/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/13-capacity-planning/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/14-load-testing-design/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/15-cost-performance-analysis/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/16-regulated-secure-performance-tradeoffs/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/17-memory-safety-tradeoffs/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-11-design-decisions/18-event-driven-architecture-performance/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/00-introduction/index.md | 97.0 | 2026-07-25 | 2 | 통과 | 1.0 | 없음(경미: Code-Review·Debugging·Logging·Git·GitHub·Cloud 태그 본문 결속 약함) |
| content/collection/optimization-12-regression-prevention/01-performance-regression-fundamentals/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/02-performance-test-automation/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/03-benchmark-ci-integration/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/04-pr-performance-gate/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/05-performance-budgeting/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/06-baseline-management/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/07-variance-management/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/08-observability-platform/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/09-alerting-strategy/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/10-canary-deployment/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/11-performance-incident-response/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/12-long-term-trend-analysis/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/13-performance-debt-management/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/14-benchmark-as-code/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/15-monitoring-dashboard/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/16-postmortem-analysis/index.md | - | - | 0 | 미채점 | - | - |
| content/collection/optimization-12-regression-prevention/17-distributed-cluster-performance-regression/index.md | - | - | 0 | 미채점 | - | - |
