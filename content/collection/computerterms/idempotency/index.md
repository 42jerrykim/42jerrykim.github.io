---
image: "wordcloud.png"
slug: idempotency
collection_order: 71
draft: false
title: "[Computer Terms] 멱등성 (Idempotency)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "같은 요청을 여러 번 보내도 결과가 한 번 보낸 것과 같아야 한다는 멱등성의 원리와, 네트워크 재시도가 분산 시스템에서 필수인 이유, 멱등키 패턴을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- API(Application Programming Interface)
- HTTP(HyperText Transfer Protocol)
- REST(Representational State Transfer)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Best-Practices
- Reliability
- Error-Handling(에러처리)
- System-Design
- Backend(백엔드)
- Idempotency(멱등성)
- Idempotency-Key(멱등키)
- Retry(재시도)
- Network-Timeout(네트워크타임아웃)
- At-Least-Once(최소한번전달)
- Distributed-Systems(분산시스템)
- API-Design(API설계)
- Payment-System(결제시스템)
- Duplicate-Request(중복요청)
- Safe-Method(안전한메서드)
---

## 이 장을 읽기 전에

[HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 HTTP 메서드(GET, POST, PUT 등)의 기본 동작과, [벡터 시계](/post/computerterms/vector-clocks/)에서 다룬 "분산 시스템에서는 정확한 순서를 보장하기 어렵다"는 배경을 안다고 가정한다. 이 챕터는 순서 문제를 넘어, "같은 요청이 실수로 여러 번 도착했을 때도 안전한가"라는 별도의 문제를 다룬다.

## 재시도는 선택이 아니라 필수다

클라이언트가 서버에 요청을 보냈는데 응답이 오지 않고 타임아웃이 발생했다고 하자. 이때 클라이언트는 세 가지 경우를 구분할 수 없다. 요청이 서버에 도착하지 못했거나, 요청은 도착해서 처리됐지만 응답이 돌아오는 길에 유실됐거나, 서버가 처리 중에 멈췄을 수도 있다. 이 **불확실성**은 네트워크가 신뢰할 수 없는 매체인 이상 근본적으로 해소할 수 없다 — 아무리 타임아웃을 길게 잡아도 "정말 실패한 것"과 "느리게 성공한 것"을 확실히 구분할 방법은 없다.

이런 상황에서 클라이언트가 택할 수 있는 안전한 전략은 결국 **재시도(retry)**뿐이다. 응답을 못 받았으니 같은 요청을 다시 보내는 것이다. 문제는 이 재시도가 만들 수 있는 부작용이다. 만약 첫 번째 요청이 실제로는 서버에 도달해 "계좌에서 1만 원 출금"을 이미 처리했는데, 클라이언트가 응답을 못 받아 같은 요청을 재전송하면 계좌에서 1만 원이 두 번 빠져나갈 수 있다. 재시도 자체는 분산 시스템에서 피할 수 없는 전략이지만, 그 재시도가 안전하려면 서버 쪽에 특별한 성질이 필요하다 — 이것이 멱등성이다.

## 멱등성의 정의

**멱등성(Idempotency)**은 어떤 연산을 한 번 수행한 결과와, 같은 연산을 여러 번 반복 수행한 결과가 동일한 성질을 말한다. 수학에서 빌려온 개념으로, 예를 들어 절댓값 함수는 `abs(abs(x)) = abs(x)`이므로 멱등이다. 시스템 설계에서 이 개념을 요청/연산에 적용하면, "같은 요청을 1번 보내는 것"과 "정확히 같은 요청을 5번 보내는 것"이 서버 상태에 남기는 최종 결과가 같아야 한다는 뜻이 된다. 여기서 핵심은 **최종 상태**가 같다는 것이지, 서버가 요청을 실제로 처리하는 횟수나 응답을 반환하는 횟수가 1번으로 줄어든다는 뜻이 아니다 — 5번 보내면 서버는 5번 응답할 수 있지만, 그 5번의 응답이 만들어낸 데이터 상태는 1번 보낸 것과 똑같아야 한다.

"계좌에서 1만 원 출금"은 멱등하지 않다 — 반복할수록 잔액이 계속 줄어든다. 반면 "계좌 잔액을 정확히 5만 원으로 설정"은 멱등하다 — 몇 번을 반복해도 잔액은 항상 5만 원이 된다. 두 연산의 차이는 **상대적 변경**(기존 값에 얼마를 더하거나 뺄지)이냐 **절대적 대입**(값을 무엇으로 고정할지)이냐에 있다.

## HTTP 메서드와 멱등성

[HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 HTTP 메서드는 RFC 9110 명세에서 멱등성 여부가 명확히 규정돼 있다. **GET**, **PUT**, **DELETE**는 멱등이다. GET은 데이터를 읽기만 하니 당연히 몇 번을 호출해도 서버 상태가 변하지 않는다. PUT은 "이 리소스를 정확히 이 값으로 덮어써라"는 의미이므로, 같은 PUT을 여러 번 보내도 결과는 마지막 값으로 고정된다. DELETE도 "이 리소스를 삭제된 상태로 만들어라"이므로, 이미 삭제된 리소스를 다시 삭제해도(대개 404를 반환하더라도) 최종 상태는 "존재하지 않음"으로 동일하다. 반면 **POST**는 멱등이 아니다 — 명세상 POST는 "새 리소스를 생성하라"는 의미를 가지는 경우가 많아, 같은 POST를 두 번 보내면 리소스가 두 개 생길 수 있다.

```text
PUT /accounts/42/balance {"balance": 50000}
→ 1번 호출: 잔액 50000으로 설정
→ 3번 반복 호출: 여전히 잔액 50000 (멱등)

POST /accounts/42/transactions {"amount": -10000}
→ 1번 호출: 거래 1건 생성, 잔액 -10000
→ 3번 반복 호출: 거래 3건 생성, 잔액 -30000 (멱등 아님)
```

여기서 주의할 점은, 멱등성이 "서버가 실제로 아무 부작용 없이 요청을 무시한다"는 뜻이 아니라는 것이다. PUT을 반복해도 서버는 매번 쓰기 연산을 수행하고 로그를 남길 수 있다. 멱등성이 보장하는 것은 **최종적으로 관찰되는 리소스 상태**일 뿐, 내부적으로 몇 번 실행됐는지는 별개 문제다.

## POST를 멱등하게 만들기: 멱등키 패턴

결제·주문 생성처럼 본질적으로 POST(새 리소스 생성)를 써야 하는 작업에서도 재시도 안전성이 필요하다. 이때 실무에서 널리 쓰는 해법이 **멱등키(Idempotency Key)** 패턴이다. 클라이언트가 요청을 보낼 때 그 요청을 식별하는 고유한 키(보통 UUID)를 헤더에 함께 담아 보내고, 서버는 그 키로 "이미 처리한 요청인지"를 판단해 두 번째 이후 요청에는 새로 처리하지 않고 **첫 번째 처리 결과를 그대로 반환**한다.

```python
import uuid
from typing import Dict

# 서버 측: 멱등키별로 이미 처리한 응답을 저장해 두는 저장소
idempotency_store: Dict[str, dict] = {}

def create_payment(idempotency_key: str, amount: int) -> dict:
    # 이미 같은 키로 처리한 요청이면 저장된 결과를 그대로 반환한다
    if idempotency_key in idempotency_store:
        return idempotency_store[idempotency_key]

    # 처음 보는 키라면 실제로 결제를 처리한다
    payment_id = str(uuid.uuid4())
    result = {"payment_id": payment_id, "amount": amount, "status": "completed"}

    # 처리 결과를 키에 연결해 저장해 둔다 (재시도 시 재사용)
    idempotency_store[idempotency_key] = result
    return result


# 클라이언트가 재시도할 때도 같은 키를 재사용해야 한다
key = str(uuid.uuid4())
first_response = create_payment(key, 10000)
retry_response = create_payment(key, 10000)  # 네트워크 오류로 재전송했다고 가정
assert first_response == retry_response  # 결제가 두 번 발생하지 않는다
```

이 코드에서 핵심은 클라이언트가 **재시도할 때 새 키를 발급하지 않고 원래 요청과 같은 키를 재사용**해야 한다는 것이다. 매번 새 키를 쓰면 서버 입장에서는 "처음 보는 요청"이 되어 멱등키의 목적이 무너진다. 실무에서는 이 저장소에 TTL(예: 24시간)을 두어, 그 기간이 지난 키는 만료시켜 저장 공간이 무한히 늘어나지 않게 한다. Stripe 같은 결제 API가 이 패턴을 `Idempotency-Key` 헤더로 공식 제공하는 대표적인 사례다.

## 흔한 오개념

**"멱등성은 서버가 중복 요청을 자동으로 막아준다는 뜻이다"** — 멱등성은 HTTP 메서드의 **명세상 약속**일 뿐, 서버 구현이 저절로 그렇게 동작하는 것이 아니다. POST로 만든 API가 내부적으로 멱등하게 구현되지 않았다면(예: 매번 새 row를 INSERT), 재시도는 여전히 중복 데이터를 만든다. PUT/DELETE도 마찬가지로, 실제로 멱등하게 구현하는 책임은 서버 개발자에게 있다 — 명세는 "이렇게 동작해야 한다"는 계약이지, 자동으로 보장되는 물리 법칙이 아니다.

**"멱등하면 재시도해도 항상 똑같은 응답을 받는다"** — 멱등성은 리소스의 **최종 상태**가 같다는 뜻이지, HTTP 응답 자체가 완전히 동일하다는 뜻은 아니다. DELETE를 두 번 호출하면 첫 번째는 `200 OK`, 두 번째는 이미 삭제된 리소스이므로 `404 Not Found`를 반환할 수 있다 — 응답 코드는 다르지만, "그 리소스는 존재하지 않는다"는 최종 상태는 두 경우 모두 동일하므로 여전히 멱등이다.

## 다른 개념과의 연결

멱등키 패턴이 해결하는 문제는 메시지 전달 보장 방식과 직접 연결된다 — 네트워크가 **최소 한 번 전달(at-least-once delivery)**만 보장하는 시스템(재전송으로 인해 같은 메시지가 여러 번 도착할 수 있음)에서는, 수신 측 연산이 멱등하지 않으면 중복 처리를 피할 수 없다. 다음 챕터에서 다룰 서킷 브레이커는 이 재시도 자체가 장애 전파의 원인이 될 수 있는 상황(재시도 폭주가 이미 힘든 서버를 더 무너뜨리는 경우)을 막는 장치를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 분산 시스템에서 재시도가 왜 피할 수 없는 전략인지, 그리고 그 재시도가 왜 위험할 수 있는지 설명할 수 있다. 상대적 변경과 절대적 대입 연산의 차이로 멱등성 여부를 판단할 수 있다. GET·PUT·DELETE·POST 각각의 멱등성 여부와 그 이유를 RFC 명세 기준으로 설명할 수 있다. 멱등키 패턴이 왜 필요하고, 클라이언트가 재시도 시 키를 재사용해야 하는 이유를 설명할 수 있다.

## 참고 자료

> Fielding, R. et al. (2022). "HTTP Semantics". *RFC 9110*, Section 9.2.2 (Idempotent Methods). IETF.

- [MDN Web Docs: Idempotent](https://developer.mozilla.org/en-US/docs/Glossary/Idempotent) — 멱등성 개념과 HTTP 메서드별 정리
- [Stripe API Documentation: Idempotent Requests](https://stripe.com/docs/api/idempotent_requests) — 멱등키 패턴을 실제 결제 API에 적용한 사례
