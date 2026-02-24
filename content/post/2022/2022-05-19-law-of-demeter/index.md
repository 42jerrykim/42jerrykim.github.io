---
image: "wordcloud.png"
categories:
- OOP
date: "2022-05-19T00:00:00Z"
lastmod: "2025-09-04"
title: "[OOP] 디미터의 법칙(Law of Demeter) - 결합도 낮추는 객체 협력 가이드"
description: "디미터의 법칙(Law of Demeter)은 객체가 오직 가까운 이웃과만 상호작용하도록 하여 결합도를 낮추고 응집도를 높이는 설계 원칙입니다. 흔한 위반 사례, 리팩터링 방법, 실전 예제를 정리했습니다."
tags:
- OOP
- encapsulation
- Software-Architecture
- refactoring
- abstraction
- interface
- Dependency-Injection
- facade
- Code-Quality
- Clean-Code
- Testing
- 객체지향
- 캡슐화
- 응집도
- 결합도
- SOLID
- 추상화
- 인터페이스
- 의존성주입
- 코드품질
- Blog
- 블로그
- Technology
- 기술
- Web
- 웹
- Tutorial
- 가이드
- Review
- 리뷰
- Markdown
- 마크다운
- Java
- API
- String
- Guide
- Productivity
- 생산성
- Education
- 교육
- Reference
- 참고
- Best-Practices
- Documentation
- 문서화
- Open-Source
- 오픈소스
- Innovation
- 혁신
- Troubleshooting
---

디미터의 법칙은 객체가 자신의 가까운 이웃과만 대화하게 만들어 불필요한 결합을 줄이고 응집을 높이는 객체지향 설계 원칙입니다. 긴 점 체이닝과 내부 구조 노출을 줄이고, 도메인 언어로 말하는 메서드를 제공하도록 이끕니다.

## 디미터의 법칙(Law of Demeter)이란?

- 핵심 문장: "낯선 이에게 말하지 말라. 오직 가까운 이웃에게만 말하라."
- 객체는 다음 대상으로만 메시지를 보내야 합니다.
  - 자기 자신(`this`)
  - 자신의 필드(직접 구성요소)
  - 메서드 매개변수로 받은 객체
  - 자신이 직접 생성한 객체
  - 컬렉션에서 바로 얻은 원소(한 단계)

이 원칙은 내부 구조를 감추고, 협력을 메시지 중심으로 설계하게 만듭니다.

## 위반을 의심할 신호

- 여러 점이 이어진 긴 체인: `a.getB().getC().doD()`
- 게터를 통해 내부를 파고드는 절차적 코드
- "이 객체의 속성 값들을 꺼내서 내가 처리"하는 패턴(Feature Envy)
- 테스트에서 과도한 목/스텁이 필요함
- 사소한 내부 변경이 광범위한 수정으로 번짐

## 안티패턴: 기차 충돌(Train Wreck)

### Before

```java
// 내부 구조가 외부로 새는 나쁜 예
String zip = order.getCustomer().getAddress().getZipCode();
```

### After

```java
// 의도를 드러내는 메시지
String zip = order.getCustomerZipCode();

// 또는 책임을 적절한 객체로 이동
public class Order {
  public String getCustomerZipCode() {
    return customer.getZipCode();
  }
}
```

## 리팩터링 전략

- 메서드 이동(Move Method): 로직이 관심을 갖는 데이터가 있는 곳으로 옮깁니다.
- 위임 숨기기(Hide Delegate): 내부 협력자를 감추는 퍼블릭 메서드를 제공합니다.
- 메서드 추출(Extract Method): 의도를 드러내는 도메인 언어로 묶습니다.
- 묻지 말고 말하라(Tell, Don’t Ask): 데이터 꺼내서 처리하지 말고, 해야 할 일을 요청합니다.
- 파사드/래퍼 도입: 복잡한 서브시스템을 단순 인터페이스로 감쌉니다.
- 값/DTO 경계 구분: 바운더리에서만 단순 데이터 전달을 허용합니다.

## 균형 있게 적용하기

- 플루언트 인터페이스/빌더는 의도된 체이닝일 수 있습니다.
- 값 객체(예: `money.amount().toString()`)에서의 짧은 체인은 허용될 수 있습니다.
- 읽기 전용 DTO에서 단순 접근은 괜찮지만, 도메인 로직은 도메인 객체에 둡니다.

## 체크리스트

- 퍼블릭 API가 내부 구조를 노출하지 않는가?
- 점 체이닝 없이 요구사항을 한 문장으로 표현하는 메서드가 있는가?
- 데이터 조회가 아닌 "행동 요청" 메시지가 중심인가?
- 변경 파급 범위가 작고 테스트가 단순한가?
- 빌더/DSL 등 의도된 체이닝을 과용하지 않았는가?

## 마무리

디미터의 법칙은 만능 규칙이 아니라, 변화에 강한 협력 구조를 만들기 위한 기본 가드레일입니다. "무엇을 해야 하는가"를 메시지로 표현하고, "어떻게 하는가"는 객체 내부로 숨기면 코드는 더 단단해집니다.
