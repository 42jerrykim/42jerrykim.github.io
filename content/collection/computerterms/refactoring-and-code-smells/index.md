---
image: "wordcloud.png"
slug: refactoring-and-code-smells
collection_order: 32
draft: false
title: "[Computer Terms] 리팩토링과 코드 스멜 (Refactoring, Code Smell)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "리팩토링은 동작을 바꾸지 않으면서 코드 구조를 개선하는 작업입니다. 코드 스멜을 신호로 언제 리팩토링할지 판단하고, 테스트로 안전망을 갖춘 상태에서 Extract Method를 적용하는 과정을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Refactoring(리팩토링)
- Code-Smell(코드스멜)
- Software-Architecture(소프트웨어아키텍처)
- Testing(테스트)
- Code-Quality(코드품질)
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
- Debugging(디버깅)
---

## 이 장을 읽기 전에

[결합도와 응집도](/post/computerterms/coupling-and-cohesion/), [디자인 패턴 개요](/post/computerterms/design-patterns-overview/)에서 다룬 "좋은 설계"의 기준을 안다고 가정한다. 이 챕터는 그 기준에 못 미치는 **기존** 코드를, 동작을 유지한 채 어떻게 그 기준에 맞게 고쳐 나가는지를 다룬다.

## 리팩토링의 정의: 동작은 그대로, 구조만 바꾼다

**리팩토링(Refactoring)**은 외부에서 관찰 가능한 동작(입력에 대한 출력)을 바꾸지 않으면서, 코드 내부 구조를 개선하는 작업이다. "동작을 바꾸지 않는다"는 조건이 핵심이다 — 버그를 고치거나 기능을 추가하는 것은 리팩토링이 아니다. 이 조건 덕분에 리팩토링 전후로 같은 테스트를 돌려 여전히 통과하는지 확인할 수 있다. 리팩토링과 기능 추가를 같은 커밋에 섞으면, 테스트가 실패했을 때 "구조를 바꿔서 깨진 것인지, 새 기능에 버그가 있는 것인지" 구분할 수 없다 — 두 작업을 분리하는 것이 리팩토링을 안전하게 만드는 첫 번째 규율이다.

## 코드 스멜: 리팩토링이 필요하다는 신호

**코드 스멜(Code Smell)**은 코드가 당장 잘못 동작하는 것은 아니지만, 구조적으로 문제가 있을 가능성을 암시하는 패턴이다. 대표적인 예로 **긴 메서드(Long Method)**(한 함수가 너무 많은 일을 함, [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)에서 다룬 낮은 응집도의 징후), **중복 코드(Duplicated Code)**(같은 로직이 여러 곳에 복사됨), **긴 매개변수 목록(Long Parameter List)**(함수가 너무 많은 것을 알아야 함, 높은 결합도의 징후)이 있다.

## Extract Method: 가장 기본적인 리팩토링 기법

다음 코드는 "긴 메서드"와 "중복 코드" 스멜을 동시에 보인다.

```python
# 리팩토링 전: 주문 출력 로직이 이메일용, 콘솔용 두 곳에 중복되고 섞여 있음
def print_order_summary(order):
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    tax = total * 0.1
    grand_total = total + tax
    print(f"소계: {total}원")
    print(f"세금: {tax}원")
    print(f"총액: {grand_total}원")

def email_order_summary(order):
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    tax = total * 0.1
    grand_total = total + tax
    send_email(f"소계: {total}원, 세금: {tax}원, 총액: {grand_total}원")
```

**Extract Method(메서드 추출)**는 반복되는 로직을 별도 함수로 뽑아내는 리팩토링이다. 이 작업을 하기 전에 먼저 기존 동작을 보장하는 테스트를 준비해 두면, 추출 과정에서 실수로 로직이 바뀌었을 때 즉시 알아챌 수 있다.

```python
# 리팩토링 후: 계산 로직을 한 곳으로 추출, 각 함수는 자신의 책임(계산 vs 출력)만 담당
def calculate_order_total(order):
    total = sum(item.price * item.quantity for item in order.items)
    tax = total * 0.1
    return total, tax, total + tax

def print_order_summary(order):
    total, tax, grand_total = calculate_order_total(order)
    print(f"소계: {total}원")
    print(f"세금: {tax}원")
    print(f"총액: {grand_total}원")

def email_order_summary(order):
    total, tax, grand_total = calculate_order_total(order)
    send_email(f"소계: {total}원, 세금: {tax}원, 총액: {grand_total}원")
```

이제 세율이 바뀌면 `calculate_order_total` 한 곳만 고치면 된다 — [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)에서 다룬 단일 책임 원칙("변경 이유가 하나")이 리팩토링을 거쳐 실제로 달성된 모습이다. 리팩토링 전후로 `print_order_summary(sample_order)`와 `email_order_summary(sample_order)`의 출력이 동일한지 테스트로 확인하면, 이 변경이 진짜 "구조만 바뀌고 동작은 그대로"인지 검증할 수 있다.

## 비교: 리팩토링 vs 재작성

| 특성 | 리팩토링 | 재작성(Rewrite) |
|---|---|---|
| 동작 변경 여부 | 없음(엄격히 유지) | 있을 수 있음 |
| 진행 단위 | 작은 단계로 점진적, 매 단계 테스트 가능 | 큰 단위로 한 번에 |
| 위험도 | 낮음(단계마다 검증) | 높음(전체를 다시 검증해야 함) |
| 적합한 상황 | 기존 구조가 대체로 맞지만 국소적으로 나쁨 | 기존 설계 자체가 요구사항과 근본적으로 안 맞음 |

## 흔한 오개념

**"코드 스멜이 있으면 무조건 리팩토링해야 한다"** — 코드 스멜은 "리팩토링을 고려해볼 신호"이지 "반드시 고쳐야 하는 결함"이 아니다. 다시는 손댈 일이 없는 코드, 곧 폐기될 기능의 코드에 시간을 들여 리팩토링하는 것은 우선순위가 낮다. [SOLID 원칙 개요](/post/computerterms/solid-principles-overview/)에서 다룬 과잉 설계와 마찬가지로, 리팩토링도 "이 코드를 앞으로 얼마나 자주, 얼마나 많은 사람이 건드릴 것인가"를 먼저 따져야 한다.

**"테스트 없이도 조심하면 안전하게 리팩토링할 수 있다"** — 리팩토링의 핵심 전제는 "동작이 바뀌지 않았다는 것을 확인할 수 있어야 한다"는 것이다. 테스트가 없으면 그 확인 자체가 불가능해, 리팩토링인지 실수로 동작을 바꾼 것인지 구분할 방법이 없다. 테스트가 없는 코드를 리팩토링해야 한다면, 먼저 현재 동작을 캡처하는 테스트부터 작성하는 것이 순서다.

## 다른 개념과의 연결

이 챕터로 소프트웨어 설계 갈래(결합도·응집도, SOLID, 디자인 패턴, 리팩토링)가 하나의 흐름으로 완결된다 — 원칙(결합도·응집도, SOLID)으로 무엇이 좋은 설계인지 판단하고, 패턴으로 그 설계를 구현하며, 리팩토링으로 기존 코드를 그 상태로 옮겨간다. Computer Terms 컬렉션 전체는 이 챕터를 포함해 12개 갈래로 마무리된다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 리팩토링과 기능 추가·버그 수정을 구분하고, 왜 같은 커밋에 섞으면 안 되는지 설명할 수 있다. 주어진 코드에서 긴 메서드·중복 코드 같은 코드 스멜을 찾아낼 수 있다. Extract Method로 중복 로직을 추출할 때 테스트가 왜 필요한지 설명할 수 있다.

## 참고 자료

> Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.). Addison-Wesley.

- [Refactoring.com: Catalog of Refactorings](https://refactoring.com/catalog/) — Extract Method를 포함한 표준 리팩토링 기법 카탈로그(마틴 파울러 공식 사이트)
- [Refactoring Guru: Code Smells](https://refactoring.guru/refactoring/smells) — 코드 스멜 유형별 정리와 대응하는 리팩토링 기법
