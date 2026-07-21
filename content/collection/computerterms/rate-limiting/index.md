---
image: "wordcloud.png"
slug: rate-limiting
collection_order: 86
draft: false
title: "[Computer Terms] 레이트 리미팅 (Rate Limiting)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "레이트 리미팅은 짧은 시간에 과도한 요청을 보내는 클라이언트를 제한해 서비스 남용과 무차별 대입 공격을 막습니다. 토큰 버킷과 슬라이딩 윈도우 알고리즘을 코드로 비교합니다."
tags:
- Technology(기술)
- Education(교육)
- Security(보안)
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
- Web(웹)
- API
- Rate-Limiting(레이트리미팅)
- Token-Bucket(토큰버킷)
- Brute-Force-Attack(무차별대입공격)
- Algorithm(알고리즘)
- Load-Balancing(로드밸런싱)
- Caching(캐싱)
---

## 이 장을 읽기 전에

[웹 취약점](/post/computerterms/web-vulnerabilities/)에서 다룬 공격 패턴, 그중에서도 로그인 폼에 가능한 비밀번호를 순서대로 대입하는 무차별 대입 공격의 개념을 안다고 가정한다. 이 챕터는 "공격 패턴 자체를 막는 것"이 아니라 "요청의 빈도를 제한해 공격을 무력화하는 것"으로 관점을 바꾼다.

## 요청 내용이 아니라 요청 빈도를 제한한다

[웹 취약점](/post/computerterms/web-vulnerabilities/)에서 다룬 SQL 인젝션·XSS는 요청 하나의 **내용**이 악성인지를 검사해서 막는다. 하지만 무차별 대입 공격이나 API 남용은 요청 하나하나는 정상적인 형태를 갖추고 있다 — 로그인 시도 하나, 검색 요청 하나는 그 자체로 아무 문제가 없다. 문제는 그런 정상적인 요청을 짧은 시간에 수천, 수만 번 반복한다는 데 있다. **레이트 리미팅(Rate Limiting)**은 이런 상황을 위한 방어 기법으로, 요청의 내용이 아니라 **단위 시간당 허용되는 요청 횟수**를 제한해, 정해진 한도를 넘는 클라이언트의 요청을 거부하거나 지연시킨다.

레이트 리미팅이 막는 문제는 크게 두 갈래다. 하나는 로그인 폼에 비밀번호를 초당 수백 번 대입하는 무차별 대입 공격처럼 명백한 악의적 요청이고, 다른 하나는 악의는 없지만 특정 클라이언트가 과도한 트래픽을 보내 서버 자원을 독점해 다른 사용자에게 피해를 주는 상황(서비스 남용, 실수로 만든 무한 루프 클라이언트 등)이다. 두 경우 모두 "누가·얼마나 자주 요청했는가"를 추적해 한도를 넘으면 `429 Too Many Requests` 같은 응답으로 요청을 거부하는 동일한 메커니즘으로 대응할 수 있다.

## 토큰 버킷: 순간적인 버스트를 허용하면서 평균 속도를 제한한다

가장 널리 쓰이는 알고리즘은 **토큰 버킷(Token Bucket)**이다. 각 클라이언트마다 정해진 용량의 "버킷"을 두고, 일정한 속도로 버킷에 토큰을 채운다. 요청이 들어올 때마다 토큰을 하나 소비하고, 버킷에 남은 토큰이 없으면 요청을 거부한다.

```python
import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity          # 버킷 최대 용량(토큰 개수)
        self.refill_rate = refill_rate    # 초당 채워지는 토큰 개수
        self.tokens = capacity            # 현재 토큰 개수(초기값은 가득 참)
        self.last_refill = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def allow_request(self):
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True    # 요청 허용
        return False       # 요청 거부(429 반환)

# 예: 용량 10, 초당 2개씩 채워지는 버킷
bucket = TokenBucket(capacity=10, refill_rate=2)
print(bucket.allow_request())  # True, 토큰 9개 남음
```

토큰 버킷의 특징은 버킷 용량만큼 **순간적인 버스트(burst)를 허용**한다는 점이다. 사용자가 한동안 요청을 보내지 않아 버킷이 가득 차 있었다면, 그 즉시 용량만큼(위 예시라면 10개) 연속 요청을 처리할 수 있다. 이는 실제 사용 패턴(가끔 몰아서 여러 요청을 보내는 것)과 잘 맞아, 평상시 사용성을 해치지 않으면서 평균 속도(초당 2개)는 장기적으로 강제한다.

## 슬라이딩 윈도우: 시간 구간 경계의 허점을 없앤다

더 단순한 접근은 **고정 윈도우(Fixed Window)**다. "매 분 정각부터 60초 동안 최대 100개"처럼 시간을 일정 구간으로 나누고, 각 구간마다 카운터를 0부터 다시 센다. 구현은 간단하지만 경계에서 허점이 생긴다 — 한 구간의 마지막 1초와 다음 구간의 첫 1초에 각각 100개씩 몰아 보내면, 실제로는 2초 사이에 200개 요청이 통과한다.

**슬라이딩 윈도우(Sliding Window)**는 이 문제를 "지금부터 정확히 과거 60초"라는 이동하는 구간으로 계산해 해결한다.

```python
from collections import deque
import time

class SlidingWindowLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.timestamps = deque()     # 최근 요청 시각들만 보관

    def allow_request(self):
        now = time.time()
        # 윈도우 밖으로 벗어난(오래된) 타임스탬프 제거
        while self.timestamps and self.timestamps[0] <= now - self.window_seconds:
            self.timestamps.popleft()

        if len(self.timestamps) < self.max_requests:
            self.timestamps.append(now)
            return True     # 요청 허용
        return False        # 요청 거부

# 예: 60초 동안 최대 100개 요청만 허용
limiter = SlidingWindowLimiter(max_requests=100, window_seconds=60)
```

슬라이딩 윈도우는 고정 윈도우의 경계 허점을 없애지만, 클라이언트마다 최근 요청 타임스탬프 전체(또는 근사 카운터)를 계속 보관해야 하므로 고정 윈도우보다 메모리 비용이 크다. 실무에서는 정확한 타임스탬프 목록 대신, 현재 윈도우와 이전 윈도우의 카운터를 가중 평균하는 **근사 슬라이딩 윈도우**로 메모리와 정확도의 균형을 맞추는 경우가 많다.

## 비교: 토큰 버킷 vs 슬라이딩 윈도우

| 특성 | 토큰 버킷 | 슬라이딩 윈도우 |
|---|---|---|
| 순간적인 버스트 허용 | 버킷 용량만큼 허용 | 설정에 따라 제한적 |
| 경계 허점 | 없음(연속적으로 토큰 소비) | 없음(윈도우가 매 요청마다 이동) |
| 메모리 비용 | 낮음(토큰 개수 하나만 추적) | 상대적으로 높음(타임스탬프 이력 필요) |
| 대표 사용처 | API 게이트웨이, CDN 트래픽 제어 | 로그인 시도 제한, 정밀한 남용 탐지 |

## 흔한 오개념

**"IP 주소만 기준으로 제한하면 충분하다"** — 여러 사용자가 같은 공용 네트워크(회사, 카페 와이파이)를 쓰면 하나의 IP 뒤에 수십 명이 몰려 있을 수 있고, 반대로 공격자는 프록시·봇넷으로 IP를 계속 바꿔가며 우회할 수 있다. 실무에서는 IP뿐 아니라 로그인된 사용자 ID, API 키, 세션 토큰 등 여러 식별자를 조합해 제한 기준을 세운다.

**"레이트 리미팅을 걸면 무차별 대입 공격은 완전히 막힌다"** — 레이트 리미팅은 공격 **속도**를 늦춰 실질적인 성공 확률을 크게 낮출 뿐, 공격 자체를 불가능하게 만들지는 않는다. 공격자가 시간을 들여 한도 바로 아래 속도로 천천히 시도하거나, 여러 IP로 분산해 각각 한도 내에서 공격하면 여전히 뚫릴 수 있다. 계정 잠금, 캡차, 다요소 인증 같은 다른 방어와 함께 써야 한다.

## 다른 개념과의 연결

토큰 버킷·슬라이딩 윈도우 카운터는 여러 서버 인스턴스가 같은 한도를 공유해야 하므로 [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 다룬 Redis 같은 공유 저장소에 흔히 구현되고, 레이트 리미터가 배치되는 위치는 [로드 밸런싱](/post/computerterms/load-balancing/)의 진입점(API 게이트웨이)과 겹치는 경우가 많다. 다음 챕터에서는 이렇게 개별 요청을 통제하는 것을 넘어, 네트워크 위치와 무관하게 모든 요청을 매번 검증하는 제로 트러스트 보안 모델을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 레이트 리미팅이 요청 내용이 아니라 빈도를 기준으로 방어하는 이유와, 이것이 막는 두 갈래 문제(악의적 공격, 선의의 남용)를 설명할 수 있다. 토큰 버킷과 슬라이딩 윈도우 알고리즘의 동작 방식과 트레이드오프를 코드 수준에서 비교할 수 있다. 레이트 리미팅만으로 무차별 대입 공격을 완전히 막을 수 없는 이유를 설명할 수 있다.

## 참고 자료

> Fielding, R., & Reschke, J. (Eds.). (2014). *RFC 7231: Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content*, Section 6.5.4 (429 Too Many Requests는 RFC 6585에서 정의). IETF.

- [Stripe Engineering: Scaling your API with rate limiters](https://stripe.com/blog/rate-limiters) — 토큰 버킷·슬라이딩 윈도우 실무 구현 비교
- [OWASP: API Security Top 10 – Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/) — 레이트 리미팅 부재가 유발하는 취약점 분류
