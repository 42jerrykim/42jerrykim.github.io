---
draft: false
collection_order: 4
slug: meaningful-naming-conventions-exercises
title: "[Clean Code] 04. 네이밍 리팩토링 실습"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "한 글자 변수와 줄임말로 뒤덮인 주문 처리 코드를 03장의 네이밍 원칙에 따라 단계적으로 리팩토링하며, 이름 변경만으로 코드 이해 속도가 얼마나 달라지는지 Before/After 표와 코드 리뷰 우선순위 기준으로 직접 확인하는 실습이다."
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
- Debugging(디버깅)
- Implementation(구현)
- Modularity
- Pitfalls(함정)
- OOP(객체지향)
- Encapsulation(캡슐화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Type-Safety
- Documentation(문서화)
- Testing(테스트)
- Interface(인터페이스)
- Domain-Driven-Design
- IDE(Integrated Development Environment)
- VSCode
- Abstraction(추상화)
- Type-Safety
- Documentation(문서화)
---

## 이 장을 읽기 전에

이 장은 [03장: 의미있는 이름 짓기](/post/clean-code/meaningful-naming-conventions-variables-functions/)에서 다룬 원칙(그릇된 정보 피하기, 발음·검색 가능성, 인코딩 지양)을 실제 코드에 적용하는 실습이다. 03장을 먼저 읽었다는 전제로 진행하며, 함수 분해나 클래스 책임 분리 같은 구조적 리팩토링은 다루지 않는다 — 이는 [05~06장](/post/clean-code/clean-functions-single-responsibility-principle/)의 범위다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 실습 1 전체 | 한 글자 변수명이 코드 이해를 얼마나 어렵게 만드는지 체감한다 |
| 실무자 | 실습 2, "판단 기준" | 팀 코드 리뷰에서 네이밍 이슈를 우선순위화하는 기준을 세운다 |

## 실습 1: 한 글자 변수명 리팩토링

아래 주문 처리 코드는 문법 오류 없이 동작하지만, 모든 변수와 메서드가 한두 글자로 압축되어 있어 각 줄이 무엇을 하는지 추측해야만 읽을 수 있다.

```java
// 실습 대상: 압축된 변수명의 주문 처리 코드
public class OrderProcessor {
    private int c = 0;
    private double t = 0.0;

    public void p(Map<String, Object> o) {
        String s = (String) o.get("status");
        if (s.equals("pending")) {
            double a = (Double) o.get("amount");
            int q = (Integer) o.get("quantity");
            String pid = (String) o.get("productId");

            if (check(pid, q)) {
                o.put("status", "confirmed");
                t += a;
                c++;
            }
        }
    }

    public boolean check(String id, int q) {
        return getStock(id) >= q;
    }

    private int getStock(String productId) { return 100; }
}
```

이 코드를 처음 읽는 사람은 `p()`가 "process"의 줄임이라는 것, `c`가 확정된 주문 수라는 것, `t`가 누적 매출이라는 것을 모두 추측으로 알아내야 한다. 추측이 틀리면 버그로 이어진다 — 예를 들어 `t`를 "total quantity"로 오해하고 수정하면 매출 계산 로직이 조용히 깨진다.

리팩토링의 첫 단계는 필드와 메서드 이름을 의도가 드러나는 이름으로 바꾸는 것이다. 이때 `Map<String, Object>`로 느슨하게 표현된 주문 데이터도 함께 짚어볼 필요가 있다 — 타입이 없는 `Map`은 어떤 키가 존재하는지 컴파일 시점에 보장하지 못하므로, 이름을 아무리 잘 지어도 `o.get("status")`가 실제로 어떤 키를 기대하는지는 여전히 문자열 검색에 의존해야 한다. 이는 11장에서 다루는 "객체와 자료구조의 비대칭" 문제와도 연결되지만, 이 장에서는 우선 이름 자체에 집중해 개선한다.

```java
// 리팩토링 결과: 의도가 드러나는 이름
public class OrderProcessor {
    private int confirmedOrderCount = 0;
    private double totalRevenue = 0.0;

    public void processOrder(Map<String, Object> order) {
        String status = (String) order.get("status");
        if (status.equals("pending")) {
            double orderAmount = (Double) order.get("amount");
            int requestedQuantity = (Integer) order.get("quantity");
            String productId = (String) order.get("productId");

            if (isStockSufficient(productId, requestedQuantity)) {
                order.put("status", "confirmed");
                totalRevenue += orderAmount;
                confirmedOrderCount++;
            }
        }
    }

    public boolean isStockSufficient(String productId, int requestedQuantity) {
        return getAvailableStock(productId) >= requestedQuantity;
    }

    private int getAvailableStock(String productId) { return 100; }
}
```

## 실습 2: Before/After 비교와 근거

이름을 바꾼 것만으로 로직은 한 줄도 바뀌지 않았지만, 코드를 읽는 데 필요한 "추측 횟수"는 크게 줄었다. 아래 표는 각 변경이 어떤 네이밍 원칙에 대응하는지 정리한 것이다.

| Before | After | 적용된 원칙 |
|:--|:--|:--|
| `c` | `confirmedOrderCount` | 의도를 분명히 밝히는 이름 |
| `t` | `totalRevenue` | 의도를 분명히 밝히는 이름 |
| `p()` | `processOrder()` | 메서드는 동사구로 |
| `check()` | `isStockSufficient()` | 불리언 반환에 `is` 접두어 |
| `q` | `requestedQuantity` | 그릇된 정보(단순 `q`는 재고 수량과 혼동 가능) 회피 |

이 표에서 특히 `check()` → `isStockSufficient()` 변경이 중요한 이유는, 원래 이름이 "무엇을 확인하는지"를 알려주지 않아 호출부에서 `if (check(pid, q))`만 봐서는 재고 확인인지 유효성 확인인지 구분할 수 없었기 때문이다. `is` 접두어와 구체적인 대상(`Stock`, `Sufficient`)을 추가하면 호출부 코드만 보고도 조건의 의미를 알 수 있다.

## 판단 기준: 네이밍 리뷰 우선순위

코드 리뷰에서 모든 이름 이슈를 동일한 무게로 다룰 필요는 없다. 공개 API의 메서드 이름, 클래스 이름처럼 넓은 범위에서 반복적으로 노출되는 이름은 우선순위가 높다 — 한 번 잘못 지어지면 여러 호출부와 문서, 테스트 코드에 퍼져 나중에 바꾸는 비용이 커지기 때문이다. 반대로 짧은 지역 변수는 IDE의 리팩토링 기능(Rename)으로 즉시, 안전하게 고칠 수 있어 상대적으로 낮은 우선순위로 미뤄도 무방하다. 이 판단 기준은 "이 이름이 얼마나 넓은 범위에서, 얼마나 많은 코드에 영향을 미치는가"로 요약할 수 있다.

## 다음 장에서는

[05장: 함수는 작게, 한 가지만](/post/clean-code/clean-functions-single-responsibility-principle/)에서는 이름을 넘어 함수 자체의 크기와 책임을 다루는 원칙을 살펴본다.

## 평가 기준

- [ ] 압축된 이름이 코드 이해에 걸리는 시간을 늘리는 구체적 사례를 재현할 수 있다.
- [ ] Before/After 변경 각각을 03장에서 배운 네이밍 원칙과 짝지어 설명할 수 있다.
- [ ] 코드 리뷰에서 네이밍 이슈의 우선순위를 "영향 범위" 기준으로 판단할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 2장.
- [Google Java Style Guide — Naming](https://google.github.io/styleguide/javaguide.html#s5-naming)
