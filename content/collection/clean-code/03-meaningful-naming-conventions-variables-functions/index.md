---
draft: false
collection_order: 3
slug: meaningful-naming-conventions-variables-functions
title: "[Clean Code] 03. 의미있는 이름 짓기"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "변수·함수·클래스 이름이 왜 코드의 첫 번째 문서 역할을 하는지 설명하고, 그릇된 정보 피하기·발음 가능성·검색 가능성·헝가리안 표기법 지양 등 구체적 네이밍 원칙을 실전 예제와 판단 기준·비판적 시각으로 상세히 다룬다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Refactoring(리팩토링)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Code-Review(코드리뷰)
- Java
- Python
- JavaScript
- Debugging(디버깅)
- Documentation(문서화)
- Implementation(구현)
- Modularity
- Pitfalls(함정)
- Type-Safety
- OOP(객체지향)
- Interface(인터페이스)
- Encapsulation(캡슐화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- IDE(Integrated Development Environment)
- VSCode
- Domain-Driven-Design
image: "wordcloud.png"
---

## 이 장을 읽기 전에

이 장은 [02장](/post/clean-code/clean-code-fundamentals-exercises/)에서 진단한 "의도가 드러나지 않는 이름" 문제를 체계적인 원칙으로 정리한다. 특정 언어의 문법 지식은 필요 없지만, 변수와 함수를 선언해 본 최소한의 경험이 있어야 예제를 이해하기 쉽다. 이 장은 네이밍 자체에 집중하며, 함수의 크기나 책임 분리는 [05장](/post/clean-code/clean-functions-single-responsibility-principle/)에서 다룬다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "의도를 분명히 밝혀라"부터 "인코딩을 피하라"까지 | 이름이 코드에서 하는 역할(문서화)을 이해하고 기본 원칙을 익힌다 |
| 실무자 | "흔한 오개념", "판단 기준", "비판적 시각" | 팀 컨벤션과 개인 취향이 충돌할 때 원칙에 근거해 판단한다 |

## 이름은 코드의 첫 번째 문서다

코드에서 이름은 변수·함수·클래스가 "왜 존재하는지", "무엇을 하는지", "어떻게 사용하는지"에 답해야 한다. 이 세 질문에 이름만으로 답할 수 없어서 별도 주석을 덧붙여야 한다면, 그 이름은 이미 실패한 것이다. 좋은 이름을 고르는 데는 시간이 걸리지만, 그 코드를 읽는 모든 사람—리뷰어, 후임자, 6개월 뒤의 자신—이 절약하는 시간의 총합은 그보다 훨씬 크다. 이는 이름 짓기가 "사소한 스타일 문제"가 아니라 코드베이스 전체의 읽기 비용을 좌우하는 설계 결정인 이유이기도 하다.

```java
// 의도가 드러나지 않는 이름
int d; // 경과 일수
List<int[]> list1 = new ArrayList<int[]>();
for (int[] x : theList)
    if (x[0] == 4)
        list1.add(x);

// 의도가 드러나는 이름
int elapsedTimeInDays;
List<Cell> flaggedCells = new ArrayList<Cell>();
for (Cell cell : gameBoard)
    if (cell.isFlagged())
        flaggedCells.add(cell);
```

두 코드는 완전히 동일한 로직을 수행하지만, 아래쪽 코드만 읽고도 "지뢰찾기 게임판에서 깃발이 꽂힌 셀을 모은다"는 의도를 알 수 있다. `int d`가 무엇을 뜻하는지는 주석 없이는 알 수 없고, 주석은 코드가 바뀌어도 갱신되지 않을 위험을 항상 안고 있다(이 위험은 [07장](/post/clean-code/code-comments-documentation-best-practices/)에서 자세히 다룬다).

## 그릇된 정보와 의미 있는 구분

이름은 독자에게 정보를 전달하는 신호이므로, 실제와 다른 신호를 보내면 정보가 아니라 잡음이 된다. `accountList`라는 이름이 실제로는 `Set`이나 `Map`을 가리킨다면, 이 이름은 독자에게 잘못된 자료구조를 연상시킨다. 마찬가지로 `hp`, `aix`, `sco`처럼 유닉스 플랫폼 이름과 우연히 겹치는 변수명, 또는 `l`(소문자 L)과 `1`(숫자 1)처럼 폰트에 따라 구분이 안 되는 이름도 그릇된 정보에 해당한다.

컴파일러를 통과시키기 위한 목적만으로 이름을 짓다 보면 <strong>불용어(noise word)</strong>와 **연번(number-series)** 문제가 생긴다. `copyChars(char a1[], char a2[])`에서 `a1`, `a2`는 컴파일은 되지만 어느 쪽이 원본이고 어느 쪽이 사본인지 이름만으로 알 수 없다. `source`, `destination`으로 바꾸면 이 모호함이 사라진다. `ProductInfo`와 `ProductData`처럼 `Info`, `Data` 같은 불용어를 덧붙인 이름도 마찬가지로, `Product`와 실질적으로 구분되지 않으면서 독자에게 "차이가 있다"는 그릇된 신호만 준다.

## 발음 가능성과 검색 가능성

사람의 뇌는 발음 가능한 단어를 훨씬 잘 기억하고 토론에 활용한다. `genymdhms`(generation year, month, day, hour, minute, second) 같은 이름은 동료와 대화할 때 소리 내어 말할 수 없어, 회의에서 "그 제니엠디에이치엠에스 변수"라는 우스꽝스러운 상황을 만든다. `generationTimestamp`로 바꾸면 "제너레이션 타임스탬프"라고 자연스럽게 말할 수 있다.

검색 가능성도 같은 맥락이다. 문자 하나짜리 이름(`e`)이나 매직 넘버(`7`)는 코드베이스에서 검색했을 때 다른 위치의 `e`, `7`과 뒤섞여 원하는 지점을 찾기 어렵다. 상수를 `WORK_DAYS_PER_WEEK`처럼 이름 붙이면, IDE의 "전체 찾기" 기능으로 이 값이 쓰이는 모든 위치를 정확히 추적할 수 있다. 이름의 길이는 그 이름이 사용되는 범위(scope)에 비례해야 한다는 것이 실무적으로 유용한 기준이다 — 루프 안에서만 쓰이는 인덱스는 `i`로 충분하지만, 모듈 전체에서 참조하는 상수는 구체적이고 검색 가능한 이름이 필요하다.

## 인코딩을 피하고 관례를 따르라

<strong>헝가리안 표기법(Hungarian Notation)</strong>은 1980–90년대 정적 타입 검사가 약한 언어(초기 C, VB)에서 변수 이름에 타입 정보를 접두어로 새겨 넣던 관행이다(`strName`, `iCount`). 현대 언어는 컴파일러와 IDE가 타입을 실시간으로 검사하고 표시해주므로, 이런 인코딩은 정보를 주기보다 이름을 읽기 어렵게 만들고, 타입이 바뀌어도 이름은 그대로 남아 오히려 그릇된 정보가 되는 부작용이 크다. 멤버 변수에 `m_` 접두어를 붙이는 관행도 같은 이유로 대부분의 현대 스타일 가이드에서 권장하지 않는다.

클래스 이름은 명사나 명사구(`Customer`, `WikiPage`, `AddressParser`)가, 메서드 이름은 동사나 동사구(`postPayment`, `deletePage`, `save`)가 적합하다. 접근자·변경자·조건자는 `get`, `set`, `is` 접두어를 붙이는 관례를 따르면, 이름만으로 그 메서드가 값을 반환하는지, 상태를 바꾸는지, 불리언을 반환하는지 예측할 수 있다.

| 대상 | 권장 형태 | 예시 |
|:--|:--|:--|
| 클래스 | 명사/명사구 | `Customer`, `AddressParser` |
| 메서드 | 동사/동사구 | `postPayment`, `deletePage` |
| 조건자 메서드 | is/has/can 접두어 | `isPosted()`, `hasPermission()` |
| 상수 | 대문자 스네이크 케이스 + 의미 있는 이름 | `MAX_RETRY_COUNT` |

## 맥락과 일관성

이름이 스스로 맥락을 담지 못하면, 클래스나 함수라는 그릇 안에 넣어 맥락을 부여해야 한다. `number`, `verb`, `pluralModifier`라는 지역 변수 세 개가 흩어져 있으면 이들이 하나의 메시지를 구성하는 부분이라는 사실이 드러나지 않지만, 이 셋을 `GuessStatisticsMessage`라는 클래스로 묶으면 맥락이 명확해진다. 반대로 이미 충분한 맥락이 있는 곳에 불필요한 접두어를 반복하는 것도 문제다. "Gas Station Deluxe"라는 애플리케이션의 모든 클래스에 `GSD` 접두어를 붙이면, 자동완성 목록이 온통 `GSD`로 시작해 정작 구분에 필요한 정보를 가려버린다.

마지막으로, 한 개념에는 한 단어만 고수해야 한다. `fetch`, `retrieve`, `get`을 프로젝트 전역에서 뒤섞어 쓰면 독자는 이 세 단어가 다른 동작을 뜻하는지 매번 확인해야 한다. 반대로 서로 다른 두 동작에 같은 단어를 재사용하는 <strong>말장난(pun)</strong>도 피해야 한다 — 기존 `add`가 "두 값을 더한다"는 뜻으로 쓰이고 있다면, "컬렉션에 값을 추가한다"는 새 동작에는 `insert`나 `append`처럼 다른 단어를 골라야 한다.

## 흔한 오개념

<strong>"줄임말을 쓰면 코드가 더 효율적이다"</strong>는 오개념이 흔하다. 실제로 변수 이름은 컴파일된 바이너리 크기나 실행 속도에 영향을 주지 않는다. 줄임말이 아끼는 것은 타이핑 시간뿐이고, 그 대가로 모든 독자가 매번 그 줄임말을 해독하는 시간을 치른다. 현대 IDE의 자동완성 기능을 고려하면 긴 이름의 타이핑 비용은 사실상 사라지므로, 이 트레이드오프는 압도적으로 명확한 이름 쪽에 유리하다.

<strong>"이름 짓기는 취향의 문제라 원칙이 없다"</strong>는 오개념도 있다. 실제로는 이 장에서 다룬 것처럼 검증 가능한 기준(발음 가능성, 검색 가능성, 그릇된 정보 여부)이 존재하며, 이 기준들은 코드 리뷰에서 "이 이름이 왜 문제인지"를 구체적으로 논증할 수 있게 해준다.

## 판단 기준: 언제 짧은 이름이 허용되는가

모든 이름을 길고 서술적으로 지어야 하는 것은 아니다. 루프 카운터 `i`, `j`, `k`는 그 범위가 몇 줄 안으로 좁고, 반복문 인덱스라는 관례가 이미 널리 공유돼 있어 별도 설명이 필요 없다. 반대로 그 루프 블록이 20줄을 넘거나 중첩 루프에서 `i`가 어느 배열의 인덱스인지 헷갈리기 시작하면, 즉시 `rowIndex`, `columnIndex`처럼 구체적인 이름으로 바꿔야 한다. 판단 기준은 "이 이름이 사용되는 범위 안에서, 다른 사람이 처음 보고 오해할 여지가 있는가"이다.

## 비판적 시각

네이밍 원칙에도 트레이드오프가 있다. 서술적인 이름을 지나치게 추구하면 `calculateTotalPriceIncludingTaxAndShippingForInternationalOrders`처럼 한눈에 읽기 어려운 긴 이름이 나올 수 있다. 이 경우에는 이름을 줄이는 대신, 애초에 그 함수가 여러 책임을 지고 있다는 신호로 받아들이고 함수 자체를 분리하는 것이 나은 해법일 때가 많다(이 판단은 [05장](/post/clean-code/clean-functions-single-responsibility-principle/)에서 더 다룬다). 또한 도메인 전문가와 소통할 때는 프로그래머 용어(`Visitor`, `Factory`)보다 도메인 용어를 그대로 쓰는 편이 협업에 유리한 경우도 있다 — Eric Evans가 『Domain-Driven Design』(2003)에서 제안한 **유비쿼터스 언어(Ubiquitous Language)** 개념은 코드의 이름이 도메인 전문가의 언어와 일치해야 한다고 강조하며, 이는 순수하게 "프로그래머에게 익숙한 이름"만을 우선하는 관점과 종종 긴장 관계에 놓인다.

## 다음 장에서는

[04장: 네이밍 리팩토링 실습](/post/clean-code/meaningful-naming-conventions-exercises/)에서는 이 장에서 다룬 원칙을 실제 나쁜 네이밍 코드에 적용해 본다.

## 평가 기준

- [ ] 그릇된 정보를 주는 이름과 단순히 짧은 이름의 차이를 구분할 수 있다.
- [ ] 발음 가능성·검색 가능성 기준으로 특정 이름이 왜 문제인지 논증할 수 있다.
- [ ] 헝가리안 표기법이 왜 현대 언어에서 불필요한지 설명할 수 있다.
- [ ] 루프 인덱스처럼 짧은 이름이 허용되는 상황과 그렇지 않은 상황을 구분할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 2장.
- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
- [Google Java Style Guide — Naming](https://google.github.io/styleguide/javaguide.html#s5-naming)
- [PEP 8 — Naming Conventions](https://www.python.org/dev/peps/pep-0008/#naming-conventions)
