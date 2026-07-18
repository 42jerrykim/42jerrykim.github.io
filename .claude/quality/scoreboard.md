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
| content/collection/design-patterns/00-design-patterns-overview/index.md | 95.2 | 2026-07-18 | 3(2차 라운드, 총 6회) | 통과 | 없음(경미: 문단 비율 29.4%로 40% 앵커 미달이지만 통과 임계엔 영향 없음) |
| content/collection/design-patterns/01-design-patterns-philosophy-and-history/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 없음(경미: 핵심메시지/결론 중복) |
| content/collection/design-patterns/02-pattern-analysis-framework/index.md | 56.5(치명결함 직접수정 완료, 미재채점) | 2026-07-18 | 3 | 에스컬레이션 | 가중평균 계산오류 치명결함 수정 완료(L532-533), 오개념 절 부재, 문단 비율 부족 |
| content/collection/design-patterns/03-oop-design-deep-understanding/index.md | 93.1 | 2026-07-18 | 2 | 통과 | 없음(경미: 핵심메시지/결론 중복) |
| content/collection/design-patterns/04-factory-patterns-evolution/index.md | 85.3 | 2026-07-18 | 3 | 에스컬레이션 | 오개념 절 부재, 선택가이드/판단기준 텍스트 중복, Abstract Factory 구조 Mermaid 부재 |
| content/collection/design-patterns/04-factory-patterns-evolution-practice/index.md | 71.8 | 2026-07-18 | 3 | 에스컬레이션 | 문단 비율 부족, 추가도전/실무적용 답없는 리스트, 표/Mermaid 부재 |
| content/collection/design-patterns/05-singleton-controversial-pattern/index.md | 79.9 | 2026-07-18 | 3 | 에스컬레이션 | 오개념 절 부재, 결정트리 Mermaid 미전환, GoF 인용 출처태그 누락 |
| content/collection/design-patterns/05-singleton-controversial-pattern-practice/index.md | 75.7 | 2026-07-18 | 3 | 에스컬레이션 | 체크리스트/추가도전 근거 부족, 멀티스레드 시나리오 Mermaid 부재 |
| content/collection/design-patterns/06-builder-prototype-deep-understanding/index.md | 82.3 | 2026-07-18 | 3 | 에스컬레이션 | 오개념 절 부재, Type-Safe Builder/ComplexConfig 미완성 로직, 결정트리 Mermaid 미전환 |
| content/collection/design-patterns/06-builder-prototype-deep-understanding-practice/index.md | 83.5 | 2026-07-18 | 3 | 에스컬레이션 | 표/Mermaid 부재, 오개념 절 부재, 실습2 기준답안 부족 |
| content/collection/design-patterns/07-adapter-facade-interface-philosophy/index.md | 85.3 | 2026-07-18 | 3 | 에스컬레이션 | 오개념 절 부재, Facade 계층구조 Mermaid 부재 |
| content/collection/design-patterns/07-adapter-facade-interface-philosophy-practice/index.md | 85.3 | 2026-07-18 | 3 | 에스컬레이션 | 오개념 절 부재, placeOrder 흐름 Mermaid 부재 |
| content/collection/design-patterns/08-decorator-composite-recursive-beauty/index.md | 91.3 | 2026-07-18 | 3 | 통과 | 없음(경미: GUIExample의 Window/Label 미정의, 트리구조 Mermaid 권장) |
| content/collection/design-patterns/08-decorator-composite-recursive-beauty-practice/index.md | 80.5 | 2026-07-18 | 3 | 에스컬레이션 | GoF 1차출처 부재, 표/Mermaid 부재 |
| content/collection/design-patterns/09-proxy-pattern-multifaceted/index.md | 80.2 | 2026-07-18 | 3 | 에스컬레이션 | 성능수치 모순 치명결함 해소(확인됨), 학습목표 절 부재, import 부재 |
| content/collection/design-patterns/09-proxy-pattern-multifaceted-practice/index.md | 80.5 | 2026-07-18 | 3 | 에스컬레이션 | 표/Mermaid 부재, 오개념 절 부재 |
| content/collection/design-patterns/10-bridge-flyweight-separation-efficiency/index.md | 76.3(치명결함 직접수정 완료, 미재채점) | 2026-07-18 | 3 | 에스컬레이션 | 저자용 자가점검 메타블록 치명결함 신규발견·수정 완료(L1285-1294), PatternDecisionGuide 주석전용 코드 |
| content/collection/design-patterns/10-bridge-flyweight-separation-efficiency-practice/index.md | 82.3 | 2026-07-18 | 3 | 에스컬레이션 | 실습목표 서술 얕음, 내재/외재 상태 표 부재 |
| content/collection/design-patterns/11-observer-event-driven-architecture/index.md | 82.6(API버그 직접수정 완료) | 2026-07-18 | 3 | 에스컬레이션 | asObservable() 존재하지않는 API 수정 완료(L902), 안티패턴 비교 부재 |
| content/collection/design-patterns/11-observer-event-driven-architecture-practice/index.md | 82.3 | 2026-07-18 | 3 | 에스컬레이션 | Observer/StockObserver 타입 불일치, import 부재, MVC절 이론편과 중복 |
| content/collection/design-patterns/12-strategy-state-algorithm-encapsulation/index.md | 85.0(컴파일버그 직접수정 완료) | 2026-07-18 | 3 | 에스컬레이션 | SortingContext 클래스 중복선언 치명적 버그 수정 완료(L814), 안티패턴 비교 부재 |
| content/collection/design-patterns/12-strategy-state-algorithm-encapsulation-practice/index.md | 84.1 | 2026-07-18 | 3 | 에스컬레이션 | GoF 1차출처 본문 인용 부재, import 부재 |
| content/collection/design-patterns/13-command-chain-responsibility/index.md | 85.0 | 2026-07-18 | 3 | 에스컬레이션 | 코드블록 5개 전체 import 부재, CoR GoF 인용 부재, 안티패턴 비교 부재 |
| content/collection/design-patterns/13-command-chain-responsibility-practice/index.md | 78.4 | 2026-07-18 | 3 | 에스컬레이션 | 평가기준/오개념/1차출처 절 부재, 실습3·4 Mermaid 부재 |
| content/collection/design-patterns/14-template-method-iterator-depth/index.md | 89.2 | 2026-07-18 | 3 | 에스컬레이션 | import 부재, 데모 main() 축약 필요(90점 임계 근접) |
| content/collection/design-patterns/15-interpreter-mediator-parsing-coordination/index.md | 89.2 | 2026-07-18 | 3 | 에스컬레이션 | import 부재, 파서 코드 앞 개요 문단 필요(90점 임계 근접) |
| content/collection/design-patterns/16-memento-visitor-state-operation-separation/index.md | 92.2 | 2026-07-18 | 3 | 통과 | 없음(경미: 데모 main() 축약, 결론/주의사항 중복) |
| content/collection/design-patterns/17-pattern-combinations-interactions/index.md | 89.2 | 2026-07-18 | 3 | 에스컬레이션 | 지원타입 고지 확장 필요, 결론부 체크리스트 재진술(90점 임계 근접) |
| content/collection/design-patterns/18-functional-programming-design-patterns/index.md | 87.4 | 2026-07-18 | 3 | 에스컬레이션 | 표 5개 연속배치 연결문단 부족, 미정의 타입(PaymentResult 등) |
| content/collection/design-patterns/19-concurrency-distributed-patterns/index.md | 86.2 | 2026-07-18 | 3 | 에스컬레이션 | Order 타입 이름충돌(Actor vs Aggregate), 표 4개 연속배치 |
| content/collection/design-patterns/20-ddd-design-patterns/index.md | 80.2 | 2026-07-18 | 3 | 에스컬레이션 | 실습과제 절이 practice 파일과 중복, 토론주제 위치 이상 |
| content/collection/design-patterns/20-ddd-design-patterns-practice/index.md | 87.1 | 2026-07-18 | 3 | 에스컬레이션 | 참고자료/1차출처 절 부재, 추가도전과제 힌트 부족(90점 임계 근접) |
| content/collection/design-patterns/21-pattern-performance-optimization/index.md | 79.3(Java문법버그 직접수정 완료) | 2026-07-18 | 3 | 에스컬레이션 | named-parameter 미지원 문법(컴파일불가) 수정 완료(L737-751), 실습과제 절이 practice와 중복 |
| content/collection/design-patterns/21-pattern-performance-optimization-practice/index.md | 80.2 | 2026-07-18 | 3 | 에스컬레이션 | JITOptimizationBenchmark 미정의 정렬전략 클래스, 참고자료 부재 |
| content/collection/design-patterns/22-antipatterns-refactoring/index.md | 86.2 | 2026-07-18 | 3 | 에스컬레이션 | OrderProcessingContext/Result 미정의, 문단 비율 부족 |
| content/collection/design-patterns/22-antipatterns-refactoring-practice/index.md | 89.2 | 2026-07-18 | 3 | 에스컬레이션 | 실무적용 절 과제와 무관·미정의 타입(90점 임계 근접, 가장 유력) |
| content/collection/design-patterns/23-pattern-code-review-design-review/index.md | 82.9 | 2026-07-18 | 3 | 에스컬레이션 | Observer 예시·자동화 절 다수 미정의 타입, 워크플로우 Mermaid 부재 |
| content/collection/design-patterns/23-pattern-code-review-design-review-practice/index.md | 77.2 | 2026-07-18 | 3 | 에스컬레이션 | 판단기준 절 부재, 다수 과제 미정의 타입으로 컴파일 불가 |
| content/collection/design-patterns/24-discovering-defining-new-patterns/index.md | 76.3 | 2026-07-18 | 3 | 에스컬레이션 | 환각인용 치명결함 해소(확인됨), 문단 비율 8%, 안티패턴 비교 부재, 필드 미선언 |
| content/collection/design-patterns/24-discovering-defining-new-patterns-practice/index.md | 80.2(import버그 직접수정 완료) | 2026-07-18 | 3 | 에스컬레이션 | Arrays/Duration import 누락 수정 완료(L277-280), 문단 비율 14%, 안티패턴 비교 부재 |
