---
draft: false
collection_order: 8
slug: code-comments-documentation-exercises
title: "[Clean Code] 08장. 주석 걷어내기 실습"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "중복 주석과 이력 기록 주석, 주석 처리된 죽은 코드로 뒤덮인 주문 서비스 코드를 07장의 기준에 따라 정리하며, 지운다·옮긴다·유지한다는 3단계 판단 절차를 실제 리뷰 상황처럼 적용해 어떤 주석을 남길지 직접 확인하는 실습이다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Documentation(문서화)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Refactoring(리팩토링)
- Java
- Code-Review(코드리뷰)
- Implementation(구현)
- Pitfalls(함정)
- Git
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Debugging(디버깅)
- Error-Handling(에러처리)
- Testing(테스트)
- Modularity
- Interface(인터페이스)
- API(Application Programming Interface)
- Productivity(생산성)
- Type-Safety
- OOP(객체지향)
- Software-Architecture(소프트웨어아키텍처)
---

## 이 장을 읽기 전에

이 장은 [07장: 주석은 실패를 의미한다](/post/clean-code/code-comments-documentation-best-practices/)에서 다룬 좋은 주석/나쁜 주석 구분을 실제 코드에 적용하는 실습이다. 07장을 먼저 읽었다는 전제로 진행한다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 실습 1 전체 | 중복 주석을 식별하고 코드로 대체하는 절차를 익힌다 |
| 실무자 | 실습 2, "판단 기준" | 팀 코드 리뷰에서 "이 주석은 남겨야 하는가"를 즉시 판단한다 |

## 실습 1: 중복 주석 걷어내기

아래 주문 서비스 코드는 거의 모든 줄에 주석이 달려 있지만, 그 주석들 대부분은 바로 아래 코드가 말하는 내용을 그대로 반복한다.

```java
// 실습 대상: 주석이 코드를 그대로 중복하는 경우
public boolean processOrder(Order o) {
    // null 체크
    if (o == null) {
        return false; // null이면 false 반환
    }
    // 주문 상태가 PENDING인지 확인
    if (!o.getStatus().equals("PENDING")) {
        return false; // PENDING이 아니면 false 반환
    }
    // 재고 확인 후 상태를 CONFIRMED로 변경
    if (hasStock(o)) {
        o.setStatus("CONFIRMED"); // 상태 변경
        return true; // 성공
    }
    return false;
}
```

이 주석들을 하나씩 지워도 코드의 의미는 전혀 손실되지 않는다. `if (o == null) return false;`라는 코드 자체가 이미 "null이면 false를 반환한다"는 문장이기 때문이다. 07장에서 다룬 기준으로 판단하면, 이 주석들은 모두 "코드가 이미 말하는 것을 반복"하는 나쁜 주석에 해당한다.

```java
// 리팩토링 결과: 이름으로 의도를 표현하고 중복 주석 제거
public boolean processOrder(Order order) {
    if (!isValidPendingOrder(order)) {
        return false;
    }
    return confirmIfStockAvailable(order);
}

private boolean isValidPendingOrder(Order order) {
    return order != null && "PENDING".equals(order.getStatus());
}

private boolean confirmIfStockAvailable(Order order) {
    if (!hasStock(order)) {
        return false;
    }
    order.setStatus("CONFIRMED");
    return true;
}
```

이 리팩토링은 단순히 주석을 지운 것이 아니라, 각 조건이 검증하는 내용을 `isValidPendingOrder`, `confirmIfStockAvailable`이라는 이름으로 승격시켰다. 그 결과 주석 없이도 `processOrder` 하나만 읽으면 전체 흐름("유효성 검사 후 재고가 있으면 확정한다")을 파악할 수 있다.

## 실습 2: 이력 기록 주석과 죽은 코드 정리

다음으로 흔한 패턴은 파일 상단에 변경 이력을 손으로 기록해 둔 주석과, 예전 구현을 지우지 못하고 주석 처리로 남겨둔 코드다.

```java
/**
 * 변경 이력
 * 2019-03-01 김철수: 최초 작성
 * 2020-06-15 이영희: 할인 로직 추가
 * 2022-01-10 박민수: 재고 확인 로직 개선
 */
public class OrderService {
    public boolean processOrder(Order order) {
        // 예전 방식 - 더 이상 사용 안 함
        // if (order.getTotal() > 10000) {
        //     order.setDiscount(0.1);
        // }
        return confirmIfStockAvailable(order);
    }
}
```

이 이력 주석은 `git log --follow OrderService.java`가 훨씬 정확하고 검색 가능한 형태로 같은 정보를 이미 제공하므로 삭제 대상이다. 주석 처리된 할인 로직도 마찬가지다 — 이 코드가 왜 비활성화됐는지, 다시 필요할지 아무도 확신할 수 없는 채로 남아 있으면 다음 사람은 지우기를 주저하게 된다. 만약 이 로직이 정말 나중에 필요할 수도 있다면, 주석 처리가 아니라 버전 관리 이력에 맡기고 코드에서는 완전히 삭제하는 것이 맞다.

## 판단 기준: 리뷰에서 주석을 남길지 즉시 판단하기

코드 리뷰 중 주석을 마주치면 다음 순서로 판단한다. 먼저 "이 주석을 지우면 코드의 의미가 달라지는가"를 묻는다. 달라지지 않는다면(단순 중복이라면) 지운다. 다음으로 "이 정보가 함수·변수 이름으로 옮겨질 수 있는가"를 묻는다. 옮겨질 수 있다면 이름을 개선하고 주석을 지운다. 마지막까지 남는 주석—법적 고지, 비직관적 설계 결정의 이유, 외부 시스템 제약—만 유지한다. 이 세 단계를 거치면 실습 1, 2에서 다룬 모든 사례가 "지운다" 또는 "코드로 옮긴다"로 처리되고, 정말 필요한 주석만 남는다는 것을 확인할 수 있다.

## 다음 장에서는

[09장: 형식 맞추기와 코드 스타일](/post/clean-code/code-formatting-style-consistency/)에서는 주석을 넘어 코드 자체의 시각적 형식이 가독성에 미치는 영향을 다룬다.

## 평가 기준

- [ ] 중복 주석을 식별하고 이름 개선으로 대체할 수 있다.
- [ ] 이력 기록 주석과 주석 처리된 죽은 코드를 버전 관리 시스템으로 대체해야 하는 이유를 설명할 수 있다.
- [ ] "지운다 / 코드로 옮긴다 / 유지한다" 3단계 판단 절차를 실제 코드 리뷰에 적용할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 4장.
- [Git 공식 문서 — git-log](https://git-scm.com/docs/git-log)
