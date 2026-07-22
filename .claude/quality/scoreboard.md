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
| content/collection/cleanarchitecture/00-clean-architecture-overview-introduction/index.md | 94.0 | 2026-07-20 | 6 | 통과 | 없음(경미: OrderController placeOrder() 반환타입 제네릭 불일치, 어댑터 블록 내 public 클래스 2개 공존, Concentric-Circles 태그 tags.yaml 미등재) |
| content/collection/cleanarchitecture/01-architecture-history-evolution-introduction/index.md | 91 | 2026-07-18 | 2 | 통과 | 없음(경미: 흔한 오해 절 부재, 다음장 하이퍼링크 없음) |
| content/collection/cleanarchitecture/02-layered-architecture-limitations-history/index.md | 90.7 | 2026-07-20 | 4 | 통과 | 없음(경미: Reenskaug 1979 인용 서지사항 검증 링크 부재, 프레임워크종속성/계층건너뛰기 절 코드 뒤 해설 여지) |
| content/collection/cleanarchitecture/03-hexagonal-architecture-ports-adapters/index.md | 96.1 | 2026-07-20 | 4 | 통과 | 없음(경미: 장점/한계 절 일부 문단 확장 여지) |
| content/collection/cleanarchitecture/04-onion-architecture-domain-centric-design/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 없음(경미: 패키지구조 절 리드문단 부재, 코드 보조타입 미정의) |
| content/collection/cleanarchitecture/05-clean-architecture-birth-uncle-bob/index.md | 97 | 2026-07-20 | 4 | 통과 | 없음(경미: 미승인 태그 11개 data/tags.yaml 미등재, Guide 태그 본문 근거 약함) |
| content/collection/cleanarchitecture/06-introduction-software-design-architecture/index.md | 94.6 | 2026-07-20 | 6 | 통과 | 없음(경미: "천국: 좋은 아키텍처" 소절 리스트 후 연결문단 여지) |
| content/collection/cleanarchitecture/07-design-vs-architecture-definition/index.md | 96.1 | 2026-07-20 | 4 | 통과 | 없음(경미: 일부 절 리드 문단 보강 여지) |
| content/collection/cleanarchitecture/08-two-values-behavior-structure/index.md | 96.1 | 2026-07-20 | 5 | 통과 | 없음(경미: "소프트웨어의 어원"/"논리적 반박" 절 리드 문단 여지, 인용 4회 반복에 장 번호 미표기) |
| content/collection/cleanarchitecture/09-programming-paradigms-introduction/index.md | 94.0 | 2026-07-20 | 4 | 통과 | 없음(경미: Repository/MySqlRepository/MongoRepository 다중 public 공존, FP 스니펫 미래핑, 신규 태그 7개 tags.yaml 미등재) |
| content/collection/cleanarchitecture/10-paradigm-overview-three-types/index.md | 92.2 | 2026-07-20 | 4 | 통과 | 없음(경미: goto 절 연결문단, "왜 세 가지뿐" 중복 정리 여지) |
| content/collection/cleanarchitecture/11-structured-programming-goto-elimination/index.md | 94.6 | 2026-07-20 | 5 | 통과 | 없음(경미: L46 Dijkstra 인용 blockquote 서식 보강 여지) |
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
| content/collection/cleanarchitecture/24-architecture-introduction-system-design/index.md | 97.0 | 2026-07-20 | 4 | 통과 | 없음(경미: Technology/Framework-Independence 태그 근거 보강 여지) |
| content/collection/cleanarchitecture/25-what-is-architecture-system-lifecycle/index.md | 93.1 | 2026-07-20 | 5 | 통과 | 없음(경미: 표-헤딩 전환 2곳, MySqlOrderRepository 스텁 로직 보강 여지) |
| content/collection/cleanarchitecture/26-independence-usecase-operation-development/index.md | 90.1 | 2026-07-20 | 4 | 통과 | 없음(경미: "네 가지 독립성"/"디커플링 모드" 헤딩 리드문단 여지, 신규태그 9개 tags.yaml 미등재이나 승인태그 16개로 하한 충족. 통과 후 Throughput 표기·Encapsulation 근거 보강 완료) |
| content/collection/cleanarchitecture/27-boundaries-drawing-lines-plugin-architecture/index.md | 94.0 | 2026-07-20 | 4 | 통과 | 없음(경미: PaymentGateway 예제 Payment/PaymentResult 미정의, MySqlWikiPagePersistence try-with-resources 미사용, 신규 태그 4개 tags.yaml 미등재) |
| content/collection/cleanarchitecture/28-boundary-anatomy-monolith-to-services/index.md | 91.6 | 2026-07-20 | 4 | 통과 | 없음(경미: package/import 서술과 코드 정합성 보강 여지) |
| content/collection/cleanarchitecture/29-policy-and-level-high-level-dependency/index.md | 93.1 | 2026-07-20 | 5 | 통과 | 없음(경미: "수준의 정의" 표·"암호화 프로그램" 하위 절 전환 문단 보강 여지) |
| content/collection/cleanarchitecture/30-business-rules-entities-usecases/index.md | 100 | 2026-07-20 | 4 | 통과 | 없음(Tier 0 개선: 인용 재검증 완료, 코드 자기완결화, 태그 재구성) |
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
| content/collection/cleanarchitecture/41-database-is-detail-persistence/index.md | 90.4 | 2026-07-20 | 4 | 통과 | 없음(경미: 항목3 문단비율 21.5%로 40% 기준 미달이나 통과, DB교체 시나리오 절 잔여 연속 블록 1곳) |
| content/collection/cleanarchitecture/42-web-is-detail-gui-history/index.md | 96.1 | 2026-07-19 | 3 | 통과 | 없음(경미: 일부 절 문단 비율 보강 여지) |
| content/collection/cleanarchitecture/43-framework-is-detail-coupling-risk/index.md | 96.1 | 2026-07-19 | 2 | 통과 | 없음(경미: 일부 절 문단 비율 보강 여지) |
| content/collection/cleanarchitecture/44-case-study-video-sales-system/index.md | 93.1 | 2026-07-19 | 3 | 통과 | 없음(경미: 태그 1개 불일치, 문단 비율 보강 여지) |
| content/collection/cleanarchitecture/45-missing-chapter-package-structure/index.md | 94.6 | 2026-07-19 | 2 | 통과 | 없음(경미: L38 서술 완화 여지) |
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
| content/collection/computerterms/00-getting-started-computer-terms/index.md | 95.2 | 2026-07-22 | 3 | 통과 | 없음(경미: 표 의존도가 높아 항목3에서 표를 빼면 갈래 목록 자체는 문단만으로 전달 안 됨) |
| content/collection/computerterms/aba-problem/index.md | 92.8 | 2026-07-22 | 1 | 통과 | 없음(경미: IEEE 링크 WAF 챌린지로 자동검증 불가) |
| content/collection/computerterms/aicd/index.md | 96.1 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/algorithm/index.md | 94.6 | 2026-07-22 | 3 | 통과 | 없음 |
| content/collection/computerterms/algorithm_efficiency/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/algotithm_classify/index.md | 98.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/arrays-and-linked-lists/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/atomic-operations-and-cas/index.md | 100 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/authentication-and-authorization/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/cache-hierarchy/index.md | 91 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/caching-and-invalidation/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/cap-theorem-and-consensus/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음(경미: Reliability 태그 본문 근거 약함) |
| content/collection/computerterms/cdn-caching/index.md | 100 | 2026-07-22 | 3 | 통과 | 없음 |
| content/collection/computerterms/ci-cd-and-testing-types/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/circuit-breaker/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 없음(경미: Release It! 장 번호 표기를 "Stability Patterns" 부로 완화) |
| content/collection/computerterms/closures-and-scope/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/code-review/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/compilers-and-interpreters/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/containers-and-virtualization/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/content-delivery-networks/index.md | 91.6 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/content-negotiation/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/cookies-and-local-storage/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/coroutines-and-async-await/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/coupling-and-cohesion/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/cpu-and-pipelining/index.md | 94.6 | 2026-07-22 | 3 | 통과 | 없음 |
| content/collection/computerterms/cpu-scheduling/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/daemons-and-zombie-processes/index.md | 98.2 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/deadlocks/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/design-patterns-overview/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/digital-signatures-and-certificates/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/dns-and-sockets/index.md | 97 | 2026-07-22 | 3 | 통과 | 없음 |
| content/collection/computerterms/dynamic-programming/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/encryption-and-hashing/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/event-driven-architecture/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/event-sourcing/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/factory-pattern/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/feature-flags/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/file-systems/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/firewalls-and-nat/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/floating-point-representation/index.md | 91 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/forward-and-reverse-proxies/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/full-text-search-indexes/index.md | 97 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/functional-programming-paradigm/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/garbage-collection/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/generics-and-polymorphism/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/graphs/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/greedy-algorithms/index.md | 97 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/grpc/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/hash-tables/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/heaps-and-priority-queues/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/hexagonal-architecture/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/http-and-https/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/http3-and-quic/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/idempotency/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/inter-process-communication/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/interrupts-and-system-calls/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/load-balancing/index.md | 91.6 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/memory-management/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/memory-safety-and-ownership/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/message-queues/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/multilevel-caching/index.md | 100 | 2026-07-22 | 3 | 통과 | 없음 |
| content/collection/computerterms/mvc-and-mvvm/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/mvcc/index.md | 96.1 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/normalization-and-indexes/index.md | 97 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/nosql-and-query-optimization/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/oauth-and-oidc/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/observer-pattern/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/osi-and-tcp-ip/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/processes-and-threads/index.md | 97 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/query-planner-internals/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/race-conditions-and-locks/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/rate-limiting/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/refactoring-and-code-smells/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/registers-and-isa/index.md | 98.2 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/rest-and-graphql/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/searching-algorithms/index.md | 91.6 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/segment-trees/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/semantic-versioning/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/semaphores-and-monitors/index.md | 91.6 | 2026-07-22 | 1 | 통과 | 없음(경미: 브린치 한센 연도 정정 반영) |
| content/collection/computerterms/server-sent-events/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/sharding-and-replication/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/shortest-path-algorithms/index.md | 100 | 2026-07-22 | 3 | 통과 | 없음 |
| content/collection/computerterms/signals/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/simd/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/skip-lists/index.md | 97 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/solid-principles-overview/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/sorting-algorithms/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/stacks-and-queues/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/thread-pools/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 없음(경미: Debugging 태그를 Throughput으로 교체) |
| content/collection/computerterms/time-series-databases/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/time_complexity/index.md | 92.8 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/transaction-isolation-levels/index.md | 94 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/trees/index.md | 97 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/tries/index.md | 93.4 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/type-systems/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/union-find/index.md | 94.6 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/vector-clocks/index.md | 92.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/version-control-internals/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/von-neumann-architecture/index.md | 100 | 2026-07-22 | 2 | 통과 | 없음 |
| content/collection/computerterms/web-application-firewalls/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/web-vulnerabilities/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/webhooks/index.md | 100 | 2026-07-22 | 3 | 통과 | 없음 |
| content/collection/computerterms/websockets-and-cors/index.md | - | - | 0 | 미채점 | - |
| content/collection/computerterms/write-through-and-write-back/index.md | 95.2 | 2026-07-22 | 1 | 통과 | 없음 |
| content/collection/computerterms/zero-trust-security/index.md | - | - | 0 | 미채점 | - |
