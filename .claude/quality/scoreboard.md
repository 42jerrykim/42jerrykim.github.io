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
