---
image: "wordcloud.png"
slug: content-negotiation
collection_order: 91
draft: false
title: "[Computer Terms] 콘텐츠 협상 (Content Negotiation)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "콘텐츠 협상은 같은 URL이 Accept·Accept-Language 헤더에 따라 형식·언어가 다른 응답을 주는 HTTP 메커니즘입니다. Vary 헤더가 캐싱과 상호작용하는 방식을 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Web(웹)
- HTTP(HyperText Transfer Protocol)
- API(Application Programming Interface)
- Caching(캐싱)
- CDN(Content Delivery Network)
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
- Backend(백엔드)
- JSON(JavaScript Object Notation)
- XML(eXtensible Markup Language)
- Localization
- Content-Negotiation
---

## 이 장을 읽기 전에

[HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 HTTP 요청·응답 헤더의 구조와, [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 다룬 캐시 키의 개념을 안다고 가정한다.

## 같은 URL이 다른 응답을 줄 수 있다

[REST와 GraphQL](/post/computerterms/rest-and-graphql/)에서 REST를 다룰 때 "URL은 자원을 나타낸다"고 했다. 그런데 같은 자원이라도 클라이언트마다 원하는 **표현 형식**은 다를 수 있다 — 어떤 클라이언트는 JSON을, 어떤 클라이언트는 XML을 원할 수 있고, 같은 페이지라도 사용자에 따라 한국어 번역과 영어 원문 중 다른 것을 받아야 할 수 있다. **콘텐츠 협상(Content Negotiation)**은 클라이언트가 요청 헤더로 원하는 형식·언어·인코딩을 알리고, 서버가 그중 가장 적합한 표현을 골라 응답하는 HTTP의 표준 메커니즘이다.

## Accept 헤더: 원하는 형식을 알리기

클라이언트는 `Accept` 요청 헤더로 받고 싶은 미디어 타입을 알린다. 여러 형식을 동시에 명시하고, `q` 값(품질 계수, 0에서 1 사이)으로 우선순위를 매길 수도 있다.

```text
클라이언트 → 서버:
  GET /users/42 HTTP/1.1
  Accept: application/json, application/xml;q=0.8

서버 → 클라이언트 (JSON을 우선 선택):
  HTTP/1.1 200 OK
  Content-Type: application/json

  {"id": 42, "name": "jerry"}
```

위 요청은 "JSON을 가장 선호하고(기본값 `q=1`), XML도 받아들이지만 우선순위는 낮다(`q=0.8`)"는 뜻이다. 서버는 자신이 지원하는 형식 중 클라이언트의 선호도가 가장 높은 것을 골라 `Content-Type` 헤더로 실제 선택한 형식을 알려준다. 서버가 요청받은 형식 중 어느 것도 지원하지 않으면 `406 Not Acceptable` 상태 코드로 응답할 수 있다.

## Accept-Language: 같은 방식으로 언어를 협상하기

같은 원리가 언어에도 적용된다. `Accept-Language` 헤더는 브라우저가 사용자의 언어 설정을 기준으로 자동 생성하며, 서버는 이를 보고 번역된 콘텐츠나 지역화된 문구를 돌려준다.

```text
클라이언트 → 서버:
  GET /article/99 HTTP/1.1
  Accept-Language: ko-KR, ko;q=0.9, en;q=0.5

서버 → 클라이언트 (한국어 번역을 선택):
  HTTP/1.1 200 OK
  Content-Language: ko-KR
  Content-Type: text/html; charset=utf-8
```

`ko-KR`(한국(대한민국)의 한국어)을 최우선으로, 일반 한국어(`ko`)를 그다음으로, 영어(`en`)를 최후 순위로 받아들이겠다는 뜻이다. 서버는 보유한 번역 중 이 우선순위에 가장 잘 맞는 것을 고른다. 이 방식은 URL에 언어 코드를 직접 넣는 방식(`/ko/article/99`, `/en/article/99`)과 달리 URL이 하나로 유지된다는 장점이 있지만, 사용자가 명시적으로 언어를 바꾸는 UI를 만들려면 URL 방식이 더 다루기 쉽다는 트레이드오프도 있다 — 실무에서는 두 방식을 함께 쓰는 경우도 흔하다(기본은 `Accept-Language`로 자동 선택하되, URL 파라미터로 사용자가 재정의할 수 있게 함).

## Vary 헤더: 협상 결과를 캐시에 알리기

콘텐츠 협상은 [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 다룬 캐싱과 정면으로 부딪힌다. CDN이나 브라우저 캐시는 보통 URL을 키로 삼아 응답을 저장하는데, 콘텐츠 협상이 적용되면 **같은 URL이 요청 헤더에 따라 다른 응답**을 낸다 — URL만 키로 쓰면 한국어 사용자에게 캐시된 영어 응답이 잘못 나갈 위험이 생긴다.

```text
서버 → 클라이언트:
  HTTP/1.1 200 OK
  Content-Type: application/json
  Content-Language: ko-KR
  Vary: Accept, Accept-Language
```

**`Vary`** 헤더는 캐시에게 "이 응답을 재사용하려면 URL뿐 아니라 나열된 요청 헤더 값도 같아야 한다"고 알리는 지시다. `Vary: Accept, Accept-Language`가 붙으면, 캐시는 URL과 `Accept`·`Accept-Language` 값의 조합을 키로 삼아 응답을 저장한다 — 같은 URL이라도 `Accept-Language: ko-KR`로 받은 응답과 `Accept-Language: en`으로 받은 응답을 별도로 캐싱해, 서로 다른 사용자에게 잘못된 언어의 캐시가 전달되는 사고를 막는다.

## 비교: 콘텐츠 협상 방식

| 방식 | 예시 | 캐싱 영향 | 적합한 상황 |
|---|---|---|---|
| 헤더 기반(`Accept*`) | `Accept-Language: ko-KR` | `Vary` 필요, 캐시 키 복잡해짐 | API, 브라우저가 자동으로 헤더를 채워주는 경우 |
| URL 기반(경로·쿼리) | `/ko/article/99`, `?lang=ko` | URL 자체가 캐시 키라 단순 | 사용자가 명시적으로 전환하는 UI, CDN 캐싱 최우선 |
| 도메인 기반 | `ko.example.com` | 도메인별로 완전히 분리된 캐싱 | 지역별로 인프라 자체를 분리하는 대규모 서비스 |

## 흔한 오개념

**"Vary 헤더를 붙이면 캐싱 성능이 항상 좋아진다"** — `Vary`는 캐시가 틀린 응답을 주는 사고를 막아주지만, 그 대가로 캐시 적중률을 낮출 수 있다. `Vary: Accept, Accept-Language`처럼 값이 다양한 헤더를 여러 개 나열하면, 사실상 같은 콘텐츠라도 요청 헤더 조합마다 별도로 캐싱되어 캐시가 잘게 쪼개진다. 특히 `Vary: User-Agent`처럼 값의 경우의 수가 매우 많은 헤더를 지정하면 캐시 적중률이 크게 떨어질 수 있어, 실무에서는 `Vary`에 나열하는 헤더를 꼭 필요한 것만으로 최소화하고, 언어처럼 값의 경우의 수가 많은 협상은 오히려 URL 기반으로 바꿔 캐싱을 단순화하는 경우가 많다.

**"콘텐츠 협상은 REST API에만 쓰인다"** — `Accept-Language`를 이용한 언어 협상은 API보다 오히려 일반 웹 페이지(HTML 응답)에서 더 흔히 쓰인다. 콘텐츠 협상은 REST의 자원-URL 모델과 별개로 HTTP 자체의 기능이므로, JSON·XML 형식 선택뿐 아니라 이미지 포맷(`Accept: image/webp,image/*`), 압축 방식(`Accept-Encoding: gzip`) 등 HTTP로 무엇을 주고받든 폭넓게 적용된다.

## 다른 개념과의 연결

`Vary` 헤더가 캐시 키를 확장하는 방식은 [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 다룬 캐시 키 설계와 직결된다. `Accept` 헤더로 JSON·XML 중 형식을 고르는 것은 [REST와 GraphQL](/post/computerterms/rest-and-graphql/)에서 다룬 자원 표현의 유연성을 넓히는 또 하나의 축이다. 웹/프로토콜 갈래는 이 챕터로 마무리되며, 지금까지 다룬 REST·GraphQL·gRPC·웹소켓·SSE·쿠키·콘텐츠 협상은 모두 "클라이언트와 서버가 데이터를 어떤 형태로, 어떤 방향으로, 어디에 저장해 주고받는가"라는 하나의 질문에 대한 서로 다른 답이었다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. `Accept`·`Accept-Language` 헤더로 클라이언트가 원하는 표현을 요청하는 원리를 설명할 수 있다. `Vary` 헤더가 캐시 키를 어떻게 확장하는지, 그리고 그 대가가 무엇인지 설명할 수 있다. 헤더 기반과 URL 기반 협상 중 상황에 맞는 방식을 근거를 갖고 선택할 수 있다.

## 참고 자료

> "HTTP provides mechanisms for content negotiation." — Fielding, R., & Reschke, J. (2014). *RFC 7231: HTTP/1.1 Semantics and Content*, Section 3.4. IETF.

- [MDN: Content negotiation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation) — Accept 계열 헤더와 협상 방식 전체 레퍼런스
- [MDN: Vary](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary) — Vary 헤더와 캐싱 상호작용 상세 가이드
