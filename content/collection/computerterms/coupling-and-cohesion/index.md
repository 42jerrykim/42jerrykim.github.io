---
image: "wordcloud.png"
slug: coupling-and-cohesion
collection_order: 25
draft: false
title: "[Computer Terms] 결합도와 응집도 (Coupling, Cohesion)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "결합도는 모듈 사이의 의존 정도, 응집도는 한 모듈 내부 요소들의 연관 정도를 가리키는 설계 척도입니다. 낮은 결합도·높은 응집도가 왜 좋은 설계의 기준인지 코드 리팩토링으로 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Software-Architecture(소프트웨어아키텍처)
- Coupling(결합도)
- Cohesion(응집도)
- Refactoring(리팩토링)
- SOLID
- Design-Patterns(디자인패턴)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Software-Engineering(소프트웨어공학)
- Maintainability(유지보수성)
- Code-Quality(코드품질)
---

## 이 장을 읽기 전에

이 챕터부터는 특정 기술 계층이 아니라, 지금까지 다룬 모든 시스템(네트워크의 계층 분리, 자료구조의 책임 분리)에 공통으로 적용되는 **설계 판단 기준**을 다룬다. 별도의 선행 챕터를 전제하지 않지만, [OSI 7계층과 TCP/IP](/post/computerterms/osi-and-tcp-ip/)에서 각 계층이 아래 계층의 세부 구현을 몰라도 되게 설계했던 것이 이 챕터에서 다룰 "낮은 결합도"의 실제 사례라는 점을 참고하면 좋다.

## 왜 "잘 짜인 코드"를 척도로 말해야 하는가

"이 코드는 설계가 나쁘다"는 말은 주관적으로 들리기 쉽다. **결합도(Coupling)**와 **응집도(Cohesion)**는 이 판단을 좀 더 구체적인 질문으로 바꿔준다. 결합도는 "한 모듈을 바꾸면 다른 모듈이 얼마나 함께 바뀌어야 하는가"를 묻고, 응집도는 "한 모듈 안의 요소들이 얼마나 하나의 목적을 위해 뭉쳐 있는가"를 묻는다. 좋은 설계의 일반적인 목표는 **낮은 결합도, 높은 응집도**다 — 모듈끼리는 서로 몰라도 되게, 모듈 안은 한 가지 일에 집중하게 만든다.

## 결합도: 모듈이 서로 얼마나 알아야 하는가

다음 코드는 주문 처리 함수가 이메일 발송의 구체적인 방법(SMTP 서버 주소, 인증 정보)까지 알아야 하는 **높은 결합도**를 보여준다.

```python
# 높은 결합도: OrderProcessor가 SMTP의 세부사항까지 알아야 함
class OrderProcessor:
    def complete_order(self, order):
        # ... 주문 처리 로직 ...
        smtp = SMTPClient("smtp.example.com", port=587, user="noreply", password="secret")
        smtp.connect()
        smtp.send(order.customer_email, "주문이 완료되었습니다")
        smtp.disconnect()
```

이메일 발송 방식을 SMS나 다른 서비스로 바꾸려면 `OrderProcessor` 코드 자체를 수정해야 한다. 아래처럼 "알림을 보낸다"는 인터페이스 뒤로 구체적인 방법을 숨기면, `OrderProcessor`는 무엇으로 알림이 가는지 몰라도 된다 — 결합도가 낮아진다.

```python
# 낮은 결합도: OrderProcessor는 "알림을 보낸다"는 인터페이스만 안다
class OrderProcessor:
    def __init__(self, notifier):
        self.notifier = notifier   # EmailNotifier, SMSNotifier 등 무엇이든 가능

    def complete_order(self, order):
        # ... 주문 처리 로직 ...
        self.notifier.notify(order.customer_id, "주문이 완료되었습니다")


class EmailNotifier:
    def notify(self, customer_id, message):
        smtp = SMTPClient("smtp.example.com", port=587, user="noreply", password="secret")
        smtp.connect()
        smtp.send(lookup_email(customer_id), message)
        smtp.disconnect()
```

`notifier`를 `EmailNotifier`에서 `SMSNotifier`로 바꿔도 `OrderProcessor` 코드는 한 줄도 바뀌지 않는다. 이것이 [OSI 7계층과 TCP/IP](/post/computerterms/osi-and-tcp-ip/)에서 응용 계층이 물리 계층의 세부사항을 몰라도 됐던 것과 같은 원리다 — 계층/모듈 사이의 경계를 인터페이스로 명확히 하면, 한쪽을 바꿔도 반대쪽에 영향이 번지지 않는다.

## 응집도: 한 모듈이 하나의 목적에 집중하는가

응집도는 모듈 "내부"의 문제다. 다음 클래스는 주문 계산, 이메일 발송, 로그 기록이라는 서로 무관한 책임을 한데 모아, **낮은 응집도**를 보인다.

```python
# 낮은 응집도: 서로 무관한 책임(계산, 알림, 로깅)이 한 클래스에 뒤섞임
class OrderManager:
    def calculate_total(self, items):
        return sum(item.price * item.quantity for item in items)

    def send_confirmation_email(self, order):
        ...

    def write_audit_log(self, event):
        ...
```

이 클래스를 수정해야 하는 이유가 "가격 계산 방식이 바뀌어서", "이메일 형식이 바뀌어서", "로그 형식이 바뀌어서"처럼 서로 다른 세 가지가 될 수 있다는 것 자체가 응집도가 낮다는 신호다. 각 책임을 별도 클래스로 분리하면, 각 클래스는 "왜 바뀌어야 하는가"에 대한 이유가 하나씩만 남는다 — 이는 뒤에서 다룰 SOLID 원칙 중 단일 책임 원칙(SRP)과 직결된다.

## 비교: 결합도·응집도 조합

| 결합도 | 응집도 | 특징 |
|---|---|---|
| 낮음 | 높음 | 이상적: 모듈이 독립적이고 각자 하나의 목적에 집중 |
| 낮음 | 낮음 | 모듈은 독립적이지만 내부가 뒤죽박죽 — 무엇을 하는 모듈인지 파악하기 어려움 |
| 높음 | 높음 | 각 모듈은 명확하지만 서로 강하게 얽혀 있어 하나를 고치면 연쇄적으로 수정 필요 |
| 높음 | 낮음 | 최악: 모듈 경계도 불명확하고 서로도 강하게 얽힘 |

## 흔한 오개념

**"함수를 작게 쪼개면 무조건 응집도가 높아진다"** — 함수를 쪼개는 것 자체가 목적이 아니다. 서로 관련 없는 로직을 억지로 하나의 함수로 묶어놓고 이름만 그럴듯하게(`process()`, `handle()`) 붙이면, 함수는 작아도 응집도는 여전히 낮다. 응집도는 "함수 크기"가 아니라 "그 안의 요소들이 하나의 목적을 향하는가"로 판단해야 한다.

**"결합도는 무조건 0으로 만들어야 한다"** — 모듈 간 결합 자체를 완전히 없앨 수는 없다. `OrderProcessor`도 결국 `notifier`라는 인터페이스와는 결합돼 있다. 목표는 결합을 없애는 것이 아니라, **구체적인 구현이 아니라 안정적인 인터페이스에 결합**되도록 만드는 것이다.

## 다른 개념과의 연결

낮은 결합도·높은 응집도라는 기준은 지금까지 이 컬렉션에서 다룬 여러 계층 분리 사례(OSI 7계층, [프로세스와 스레드](/post/computerterms/processes-and-threads/)의 프로세스 격리, [정규화와 인덱스](/post/computerterms/normalization-and-indexes/)의 테이블 분리)를 관통하는 공통 원리다. 다음 챕터에서는 이 기준을 다섯 가지 구체적인 규칙으로 정리한 SOLID 원칙을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 결합도와 응집도가 각각 무엇을 측정하는 척도인지 구분해 설명할 수 있다. 주어진 코드에서 높은 결합도 또는 낮은 응집도의 징후를 찾아낼 수 있다. 인터페이스를 통한 의존성 주입이 결합도를 낮추는 원리를 설명할 수 있다.

## 참고 자료

> Yourdon, E., & Constantine, L. L. (1979). *Structured Design: Fundamentals of a Discipline of Computer Program and Systems Design*. Prentice-Hall.

- [Martin Fowler: CouplingAndCohesion](https://martinfowler.com/ieeeSoftware/coupling.pdf) — 결합도·응집도 개념의 IEEE Software 기고문
- [Refactoring Guru: Coupling](https://refactoring.guru/smells/inappropriate-intimacy) — 높은 결합도가 만드는 대표적인 코드 스멜 카탈로그
