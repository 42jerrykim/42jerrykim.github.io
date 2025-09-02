---
title: "[Software] Cognitive Load(인지 부하) in Code - 실용 가이드"
description: "개발팀이 코드에서 불필요한 인지 부하를 줄이는 실전 가이드. 조건문 단순화, 가드 절, 의미 있는 네이밍, 깊은 모듈 설계와 Sonar Cognitive Complexity 활용법까지 한 번에 정리합니다. 온보딩 단축, 리뷰 표준화, 기술 부채 감축 전략 포함."
date: 2025-09-01
lastmod: 2025-09-01
categories:
- "Software Engineering"
- "Architecture"
tags:
- "cognitive load"
- "cognitive complexity"
- "working memory"
- "sweller"
- "intrinsic load"
- "extraneous load"
- "germane load"
- "sonarsource"
- "cyclomatic complexity"
- "readability"
- "maintainability"
- "refactoring"
- "naming"
- "early return"
- "guard clauses"
- "shallow module"
- "deep module"
- "module boundaries"
- "interfaces"
- "api design"
- "error handling"
- "conditional simplification"
- "boolean logic"
- "meaningful variables"
- "abstraction"
- "overengineering"
- "yak shaving"
- "complexity budget"
- "design tradeoffs"
- "design sacrifice"
- "testability"
- "onboarding"
- "developer experience"
- "DX"
- "productivity"
- "TCO"
- "mental models"
- "schema"
- "chunking"
- "seven plus or minus two"
- "instructional design"
- "multimedia learning"
- "split attention"
- "modality effect"
- "worked example"
- "expertise reversal"
- "measurement"
- "pupil dilation"
- "Paas"
- "Ousterhout"
- "APOSD"
- "Clean Code"
- "Grug Brain"
- "Redis"
- "antirez"
- "Karpathy"
- "Rob Pike"
- "Addy Osmani"
- "code review"
- "static analysis"
- "quality gates"
- "engineering management"
- "team practices"
- "pair programming"
- "knowledge transfer"
- "runbook"
- "SOP"
- "observability"
- "incident response"
- "postmortem"
- "technical debt"
- "tech debt"
- "architecture decision record"
- "ADR"
- "simplicity"
- "KISS"
- "YAGNI"
- "모듈 경계"
- "얕은 모듈"
- "깊은 모듈"
- "인지 부하"
- "인지 복잡도"
- "작업 기억"
- "조건문 단순화"
- "조기 반환"
- "가드 절"
- "가독성"
- "유지보수성"
- "리팩토링"
- "이름 짓기"
- "추상화 남용"
- "과설계"
- "테스트 용이성"
- "온보딩"
- "생산성"
- "정신적 모델"
- "청크"
- "교육심리"
- "시각-청각 통합"
- "분할 주의"
- "전문성 역전"
- "측정"
- "동공 확장"
- "정적분석"
- "코드 품질"
- "기술 부채"
- "단순함"
- "필요한 것만"
image: "wordcloud.png"
---

불필요한 인지 부하를 줄이면 읽기·변경이 쉬워지고 팀 속도가 붙습니다.

## 인지 부하 핵심 개념
- 신경과학·교육심리 관점의 정의: 작업을 이해·완수하기 위해 필요한 정신적 노력. Intrinsic/Extraneous/(Germane) 구분이 널리 쓰입니다. [Wikipedia](https://en.wikipedia.org/wiki/Cognitive_load)
- 코드 관점의 지표: 사람이 느끼는 이해 난이도에 더 근접한 측정을 지향하는 Cognitive Complexity. [SonarSource](https://www.sonarsource.com/resources/cognitive-complexity/)
- 아키텍처 관점의 원리: 얕은 모듈을 피하고, 강력한 기능을 단순한 인터페이스 뒤로 숨기는 깊은 모듈을 설계합니다. [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/aposd.php)
- 실천적 모범 사례 아카이브: 조건문 단순화, 조기 반환, 의미 있는 이름 등 실전 예시. [GitHub: cognitive-load](https://github.com/zakirullin/cognitive-load)

## 코드 레벨 체크리스트
1) 조건문 단순화
- 복잡한 논리를 의미 있는 중간 변수로 분해합니다.
- 중첩을 줄이고 조기 반환(guard clauses)으로 해피 패스를 노출합니다.

2) 흐름 제어 평탄화
- 깊은 if/else 대신 빠른 실패를 적용하고, 예외 처리 경계를 명확히 합니다.

3) 이름과 경계 강화
- 변수·함수·모듈 이름에 의도를 담아 주석 의존도를 낮춥니다.
- 모듈 경계를 좁히고 데이터 흐름을 단순화합니다.

4) 얕은 추상화 거부
- 실질 가치가 없는 래퍼·추상화는 제거하고 실제 복잡도는 내부에서 흡수합니다.

5) 측정과 리뷰 루프
- Cognitive Complexity와 정적 분석을 CI에 걸어 PR에서 대화합니다. [SonarSource](https://www.sonarsource.com/resources/cognitive-complexity/)

## 예시: 조건문 리팩토링
나쁨:
```ts
if (val > LIMIT && (isMember || isAdmin) && (isVerified && !isBanned)) {
  proceed();
}
```
개선:
```ts
const isValid = val > LIMIT;
const isAllowed = isMember || isAdmin;
const isSecure = isVerified && !isBanned;

if (!isValid) return;
if (!isAllowed) return;
if (!isSecure) return;

proceed();
```
아이디어: 의미 있는 중간 변수와 조기 반환은 작업 기억 부담을 줄입니다. 실전 예시는 저장소 정리를 참고하세요. [cognitive-load](https://github.com/zakirullin/cognitive-load)

## 아키텍처: 얕은 vs 깊은 모듈
- 얕은 모듈이 많으면 호출자에 퍼지는 인지 비용이 커집니다.
- 깊은 모듈은 강력한 기능을 간단한 표면 API로 감싸 호출자 부담을 최소화합니다. [APOSD](https://web.stanford.edu/~ouster/cgi-bin/aposd.php)

## 지표의 활용과 한계
- Cyclomatic vs Cognitive Complexity: 분기 수만 세는 지표보다 “이해 난이도”에 근접하지만, 최종 판단은 맥락·리뷰어의 근거 있는 설명이 뒷받침해야 합니다. [SonarSource](https://www.sonarsource.com/resources/cognitive-complexity/)

## 참고 자료
- [GitHub: Cognitive Load is what matters — 예시·원칙 정리 (업데이트 2025-08)](https://github.com/zakirullin/cognitive-load)
- [Wikipedia: Cognitive load](https://en.wikipedia.org/wiki/Cognitive_load)
- [SonarSource: Cognitive Complexity white paper](https://www.sonarsource.com/resources/cognitive-complexity/)
- [John Ousterhout: A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/aposd.php)


