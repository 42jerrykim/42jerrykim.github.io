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
| content/post/2026/2026-07-22-p95-p99-latency-percentile-guide/index.md | 91 | 2026-07-22 | 1 | 통과 | 없음(경미: "이 글을 읽은 후" 학습 성과 목표 절 부재, Bigtable SRE Book 챕터 인용 정밀도, cacm.acm.org 대체 접근 경로 미병기) |
| content/post/2026/2026-07-22-iterm2-vs-securecrt-logging-comparison/index.md | 95 | 2026-07-22 | 2 | 통과 | 없음(선택: "이 글에서 다루는 내용" 미리보기 불릿을 문단으로 축약하면 구조 항목 여지 있으나 통과에 영향 없음) |
| content/post/2026/2026-07-22-qbittorrent-vs-utorrent-comparison/index.md | 94.6 | 2026-07-22 | 3 | 통과 | 없음(3차 채점 후 L99 Cloudwards 인용 정밀도를 추가로 정정, 재채점 생략) |
| content/collection/cmd/command-categories/index.md | 96.1 | 2026-07-22 | 3 | 통과 | 없음(경미: 네트워크·기타 유틸리티 절 판단 기준 문단 여지, 코드블록 언어 태그 미통일) |
| content/post/2026/2026-07-22-pikvm-v4-mini-review/index.md | 93.1 | 2026-07-22 | 3 | 통과 | 없음(경미: RDP(Remote Desktop Protocol) 태그 본문 근거 약함, 종합 평가 문단이 장단점 절과 일부 재진술) |
| content/collection/TV-Show/2026/2026-07-22-young-sheldon-medford-texas-setting-filming-location/index.md | 85.0 | 2026-07-22 | 11 | 에스컬레이션 | 자동 루프(3회) 에스컬레이션 후 사람이 직접 이어받아 8회 추가 반복. 원래 치명결함(러프킨→러스크 오류, 25번 스테이지 계승 환각, 깨진 fandom.com 링크)은 전부 해소되고 치명결함 0건 상태. 캐릭터 분석·숨겨진 내용 분석·종합 평가 절을 신규 추가해 컬렉션 형식에 맞췄으나, 이 글이 의도적으로 좁힌 범위("촬영지·설정 특집")와 정식 시즌 리뷰를 기대하는 컬렉션 루브릭 사이의 구조적 긴장으로 85점대에서 정체(11회 반복 동안 65.7~89 사이 진동). 추가 반복의 한계효용이 낮다고 판단해 사람 승인 대기 |
