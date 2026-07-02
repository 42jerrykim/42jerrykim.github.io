# 교육 콘텐츠 석학 기준 Gap 진단 리포트

- **작성일**: 2026-07-02
- **방법**: 전 과목 대표 샘플링. 각 교육 컬렉션에서 대표 글 1편씩을 정독하고, "해당 과목을 가르치는 MIT/Stanford/Oxford 교수라면 이 글로 충분하다고 볼까?"라는 SME 관점으로 7대 완결성 축(C1~C7)에 대조 — 축 정의는 [`educational-content-writing` 스킬 §7](../.claude/skills/educational-content-writing/SKILL.md)로 편입됨.
- **범위**: 진단(글 수정·PR 없음) + 가이드라인 산출. 사용자 승인 범위대로 본문은 수정하지 않았다.
- **대상 규모(참고)**: 교육성 컬렉션 기술 글 700+편(Algorithm 359, python/cheatsheet 100+, optimization 시리즈, design-patterns 41, cleanarchitecture 47, clean-code 24, ooad 21 등), Vocabulary 124편. 아래는 그 **대표 표본**이다.

---

## 요약: 전반 수준과 공통 패턴

- **형식 성숙도는 높다.** 대부분의 글이 학습 목표·비교표·Mermaid·"다음 장" 링크·체크리스트를 갖췄고, `educational-content-writing` 스킬이 잘 적용돼 있다.
- **내용 완결성(SME 관점)은 글마다 편차가 크다.** 정본에 충실하고 오개념·대안까지 다룬 최상급(디자인패턴 싱글톤, 클린아키텍처 SRP)과, 형식은 갖췄으나 **정작 그 주제의 메커니즘·근거가 비어 있는** 글(Python 데코레이터, 어휘)이 공존한다.
- **가장 자주·가장 치명적으로 누락되는 축은 C7(심화·검증)과 C4(오개념)**, 그리고 **정합성 결함(복잡도/사실 불일치, 태그 과약속)** 이다.

| 표본 | 과목 | 종합 | 강점 축 | 취약 축 | 치명 결함 |
|------|------|------|---------|---------|-----------|
| design-patterns/05 싱글톤 | 설계 | ★★★★☆ | C1·C2·C4·C5 | C7 | 벤치마크 수치 미검증 |
| cleanarchitecture/15 SRP | 아키텍처 | ★★★★☆ | C1·C2·C4 | C7 | 출처·연습 부재(경미) |
| Algorithm/BOJ 18874 | 알고리즘 | ★★★☆☆ | C1·C3 | C4·C6 | **복잡도 서술↔코드 불일치** |
| python/13 데코레이터 | 언어 | ★★☆☆☆ | (형식) | C1·C4·C7 | 메커니즘 공백 + 일반론 필러 |
| Vocabulary/conception | 어휘 | ★★☆☆☆ | C1(일부) | C2·C4·C7 | **태그 과약속**(IPA·어원·반의어 없음) |
| bashshell/awk | 도구 | ★★★☆☆(부분열람) | C1 | — | 태그 보일러플레이트 |

---

## 표본별 상세

### 1. design-patterns/05 싱글톤 — ★★★★☆ (모범)
[content/collection/design-patterns/05-singleton-controversial-pattern/index.md](../content/collection/design-patterns/05-singleton-controversial-pattern/index.md)

**석학 판정**: 통과에 가깝다. GoF 원 의도(C2), 5가지 구현·DCL 리오더링·`volatile`·Bill Pugh·Enum(C1), 안티패턴 논쟁·테스트 곤란·분산 환경 한계(C4), DI/정적 메서드/함수형 대안과 결정 트리(C5), 리팩토링 단계까지 갖춰 학부 디자인패턴 강의 자료로 손색없다.

**석학이라면 추가로 요구할 것**:
- **C7(심화·검증) — 유일한 실질 공백**: 참고 문헌 절이 없다. 최소한 GoF 『Design Patterns』(1994) 싱글톤 항목과 Joshua Bloch 『Effective Java』 Item 3(Enum 싱글톤)·Item 89(직렬화)를 blockquote 출처로 달아야 한다.
- **미검증 수치(정합성)**: JMH 벤치마크 표(Enum 1.8ns, Synchronized 45.2ns 등)에 **플랫폼·JVM·JMH 버전·플래그·출처가 없다.** 교수라면 "이 숫자 어디서 나왔나"를 첫 질문으로 던진다. 실측 재현 코드 링크를 걸거나 "예시 수치, 환경에 따라 다름"으로 명시해야 한다.
- **테스트 대안 최신화**: "static 메서드 mocking은 복잡"이라 했으나 Mockito 3.4+의 `mockStatic`으로 가능해졌다. 현대 도구 반영 필요.

### 2. cleanarchitecture/15 SRP — ★★★★☆ (모범)
[content/collection/cleanarchitecture/15-srp-single-responsibility-principle/index.md](../content/collection/cleanarchitecture/15-srp-single-responsibility-principle/index.md)

**석학 판정**: Uncle Bob 원전에 충실. "하나의 일" 오해 교정→액터 정의(C4), Employee 예제의 우발적 중복·병합 충돌(C1), 퍼사드 해법, Conway's Law 연결(C5), 과분리 안티패턴(C4)까지 정확하다.

**추가 요구**:
- **C7 출처**: Martin 『Clean Architecture』(2017) 및 SRP의 원 출처인 『Agile Software Development』(2003)를 명시하면 완결. Conway 1968 논문(*How Do Committees Invent?*)도 링크 가치.
- **연습(C6 심화)**: "다음은 SRP 위반인가?" 판별 연습 2~3개가 있으면 판단력 전이가 강해진다. (clean-code 컬렉션은 exercises 짝이 있는데 이 컬렉션은 없음 → 시리즈 일관성 검토 권장)
- 분량이 320줄로 다른 장 대비 얇다 — 코드 예제의 `/* ... */` 자리에 실제 로직을 채우면 좋다.

### 3. Algorithm/BOJ 18874 Haircut — ★★★☆☆ (치명 결함 1)
[content/collection/Algorithm/2026/2026-01-05-BOJ-18874-haircut-fenwick-tree-inversion-cpp-solution/index.md](../content/collection/Algorithm/2026/2026-01-05-BOJ-18874-haircut-fenwick-tree-inversion-cpp-solution/index.md)

**치명 결함 — 복잡도 서술과 실제 코드 불일치**:
- description·"복잡도 분석" 표·Mermaid 플로차트는 **O(N² log N)** (임계값 j마다 O(N log N) 역위 계산을 N번)을 주장한다.
- 그러나 실제 **코드는 단일 패스 O(N log N)** 이다: 값별 기여도를 한 번의 Fenwick 순회로 `cnt[v]`에 모으고 누적합으로 각 j의 답을 낸다. 마무리 문단도 "이미 계산한 정보를 재활용"이라 설명해 코드와는 맞지만 앞의 복잡도 표와는 모순된다.
- **석학 판정**: 불합격 사유. 알고리즘 글에서 명시된 복잡도가 코드와 다른 것은 학생을 직접 오도한다. 표·플로차트를 O(N log N) 단일 패스로 통일해야 한다.

**추가 요구**:
- **C4 오개념/정당성**: "왜 값별 기여를 누적하면 각 임계값의 답이 되는가"의 불변식 한 단락이 빠졌다. 이게 이 문제의 핵심 통찰인데 코드 주석 한 줄로만 처리됐다.
- **C6 대안 비교**: Merge Sort 역위·좌표압축 세그트리를 "가능하다"고 언급만 하고 트레이드오프 표가 없다.
- **표기**: "페닉윅"은 Fenwick의 오기 → "펜윅". (다수 알고리즘 글에 전파됐을 가능성 → 일괄 점검 권장)

### 4. python/13 데코레이터 — ★★☆☆☆ (구조적 공백)
[content/collection/python/13_decorators/index.md](../content/collection/python/13_decorators/index.md)

**석학 판정**: 코드 예제(로깅·재시도·캐시·property)는 실행 가능하고 풍부하나, **정작 데코레이터의 메커니즘(C1)이 설명되지 않았고 그 자리를 주제 무관 일반론이 차지**했다.

- **C1 메커니즘 공백**: "핵심 개념(이론)" 절 전체가 "경계를 분명히 하라", "트레이드오프", "실패 모드를 먼저 생각하라" 같은 **어느 주제에나 붙는 일반론**이다. 정작 필요한 것 — `@deco`가 `f = deco(f)`로 디슈가링된다는 사실, 클로저로 상태를 잡는 원리, **매개변수 있는 데코레이터의 3중 중첩** 구조, `functools.wraps`가 `__name__·__doc__·__wrapped__`에 하는 일 — 은 코드에 암묵적으로만 있고 서술이 없다.
- **C1 표준 라이브러리 누락**: 체크리스트엔 `@functools.lru_cache`가 있으나 본문은 **손수 만든 캐시 시스템(70줄)만** 보여준다. 석학이라면 "왜 `lru_cache`/`cache`를 먼저 안 보여주나? 언제 직접 만들어야 하나?"를 지적한다.
- **C4 오개념 미교정**: 데코레이터의 대표 함정이 전부 빠졌다 — (a) `wraps` 없으면 introspection이 깨진다는 **실패 시연**, (b) `CountCalls` 같은 **클래스 데코레이터를 메서드에 붙이면 디스크립터 프로토콜이 깨져** `self`가 안 넘어가는 문제, (c) 스택 순서(`@a @b def f` = `a(b(f))`)는 체크리스트에만 있고 본문 설명이 없다.
- **C2/C7**: PEP 318(데코레이터 도입) 역사·1차 출처 없음.
- 사소: `@property`의 넓이를 `3.14159` 하드코딩 → `math.pi` 권장.

### 5. Vocabulary/conception — ★★☆☆☆ (태그 과약속)
[content/collection/Vocabulary/2025/2025-02-08-conception/index.md](../content/collection/Vocabulary/2025/2025-02-08-conception/index.md)

**치명 결함 — frontmatter가 본문보다 훨씬 많이 약속**: 태그에 `Etymology/어원`, `Pronunciation/발음`, `Antonym/반의어`, `Nuance/뉘앙스`가 있으나 **본문엔 셋 다 없다.** 또 `Markdown·Technology·기술·Documentation` 등 어휘와 무관한 보일러플레이트 태그가 다수다.

**석학(어휘론/언어교육) 판정**: 3가지 의미와 몇 개 연어·유의어는 있으나 어휘 학습 글의 필수를 다수 결여.
- **C1/발음**: IPA(`/kənˈsɛpʃən/`)·강세 없음.
- **C2/어원**: `conception ← 라틴어 concipere (con- "함께" + capere "잡다")` → conceive/concept/capture와의 뿌리 연결이 없다. 어원은 다의(개념/임신/구상)가 왜 한 단어에 묶이는지 설명하는 **핵심 기억 고리**인데 빠졌다.
- **품사 가족**: conceive(v.)/conceptual(adj.)/conceivable(adj.) 파생 없음.
- **C4 변별**: idea/concept/notion 차이를 한 줄씩만 — conception 자체와의 대비(왜 "the conception of X"인가)가 약하다. 반의어(misconception 등) 없음.
- **C7/한눈에 정리**: `vocabulary-post-writing` 스킬이 요구하는 요약 표가 없다.

### 6. bashshell/awk — ★★★☆☆ (부분 열람)
[content/collection/bashshell/awk/index.md](../content/collection/bashshell/awk/index.md)

- 본문 초반·frontmatter만 확인. description은 정신 모델(필드/레코드·NR/NF/FS)을 정확히 짚어 방향은 옳다.
- **태그 보일러플레이트**: `Markdown·Deployment·배포·Review·Case-Study` 등 awk와 무관한 태그가 다수 — §3 결함 2 재현. 태그는 본문 실재 항목으로 좁혀야 한다.
- 도구 레퍼런스 공통 권고: GNU awk vs POSIX/BSD 차이(C4 이식성)와 man 링크(C7)를 반드시 포함.

---

## 우선순위 권고 (수정은 별도 승인 필요)

**즉시(정확성 오류 — 학생을 직접 오도)**
1. Algorithm/BOJ 18874: 복잡도 표·플로차트를 실제 코드에 맞춰 **O(N log N) 단일 패스**로 통일. → 다른 Fenwick/역위 글도 동일 유형 점검.
2. "페닉윅"→"펜윅" 표기 일괄 점검(Algorithm 컬렉션).

**단기(완결성 — 형식은 됐으나 알맹이 부족)**
3. python/13 데코레이터: 일반론 필러 절을 **메커니즘 서술**(디슈가링·클로저·3중 중첩·`wraps`)로 교체, `lru_cache` 먼저 제시, 대표 함정 3종 추가. → python 시리즈 다른 장도 "핵심 개념(이론)" 절이 동일 템플릿 필러인지 점검.
4. Vocabulary 전반: 태그가 약속한 IPA·어원·반의어를 본문에 채우거나, 못 채우면 **태그에서 제거**. `vocabulary-post-writing` 스킬 준수 여부 일괄 점검(124편).

**지속(품질 상향)**
5. 태그 보일러플레이트(Markdown/Technology/Deployment 등 무관 태그)를 컬렉션 공통으로 정리.
6. 모든 교육 글에 **C7(1차 출처·다음 학습)** 을 최소 1개 추가하는 것을 신규 게이트로.

**신규 글 게이트**: 위 결함이 재발하지 않도록 [`educational-content-writing` 스킬](../.claude/skills/educational-content-writing/SKILL.md) §7(내용 완결성)·§8(품질 체크리스트)을 작성 전후에 적용한다. 채점 루프는 [`post-quality-loop/rubric.md`](../.claude/skills/post-quality-loop/rubric.md) 항목 1·2·7에 동일 기준이 반영되어 있다.
