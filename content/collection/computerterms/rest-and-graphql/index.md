---
image: "wordcloud.png"
slug: rest-and-graphql
collection_order: 34
draft: false
title: "[Computer Terms] REST와 GraphQL"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "REST는 자원을 URL과 HTTP 메서드로 표현하는 API 설계 스타일이고, GraphQL은 클라이언트가 필요한 데이터의 모양을 직접 지정하는 쿼리 언어입니다. 오버페칭·언더페칭 문제와 REST의 캐싱 이점 대 GraphQL의 유연성 트레이드오프로 두 방식을 비교합니다."
tags:
- Technology(기술)
- Education(교육)
- Web(웹)
- REST
- GraphQL
- API
- HTTP
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
- Performance(성능)
- Caching(캐싱)
- Database(데이터베이스)
- Debugging(디버깅)
- Advanced
- How-To
---

## 이 장을 읽기 전에

[HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 HTTP 메서드·상태 코드·무상태성을 안다고 가정한다. REST와 GraphQL은 새로운 통신 프로토콜이 아니라, 그 위에서 클라이언트와 서버가 데이터를 주고받는 **API 설계 방식**의 차이다.

## REST: 자원을 URL과 메서드로 표현하기

**REST(Representational State Transfer)**는 서버가 다루는 데이터를 **자원(Resource)**으로 보고, 각 자원에 고유한 URL을 부여한 뒤 [HTTP와 HTTPS](/post/computerterms/http-and-https/)의 메서드로 행위를 표현하는 설계 스타일이다. `GET /users/42`는 42번 사용자를 조회하고, `PUT /users/42`는 그 사용자 정보를 갱신하며, `DELETE /users/42`는 삭제한다 — URL은 "무엇을", 메서드는 "어떤 행위를"을 나타낸다는 일관된 규칙이 핵심이다.

```text
GET    /users/42/posts        → 42번 사용자의 게시글 목록
GET    /users/42/posts/7      → 42번 사용자의 7번 게시글
POST   /users/42/posts        → 42번 사용자의 새 게시글 작성
DELETE /users/42/posts/7      → 42번 사용자의 7번 게시글 삭제
```

## REST의 한계: 오버페칭과 언더페칭

REST는 자원 하나에 URL 하나가 대응하므로, 클라이언트가 필요한 데이터의 모양을 세밀하게 조정하기 어렵다. 사용자 목록 화면에서 이름만 필요한데도 `GET /users`가 이메일·주소·가입일 등 모든 필드를 함께 내려주면 **오버페칭(Overfetching)**이다. 반대로 사용자 목록과 각 사용자의 최근 게시글을 함께 보여줘야 한다면, `GET /users`로 목록을 받은 뒤 사용자마다 `GET /users/{id}/posts`를 또 호출해야 하는 **언더페칭(Underfetching)**이 생긴다 — 화면 하나를 그리는 데 요청이 N+1번 필요해지는 문제다.

## GraphQL: 필요한 데이터의 모양을 직접 지정하기

**GraphQL**은 클라이언트가 하나의 요청으로, 필요한 필드만 정확히 지정해 받아올 수 있는 쿼리 언어다. 위의 오버페칭·언더페칭 문제를 클라이언트가 쿼리를 통해 직접 해결한다.

```graphql
# 사용자 이름과, 각 사용자의 최근 게시글 제목만 한 번의 요청으로 가져옴
query {
  users {
    name
    posts(limit: 3) {
      title
    }
  }
}
```

```json
{
  "data": {
    "users": [
      { "name": "jerry", "posts": [{ "title": "첫 글" }, { "title": "둘째 글" }] }
    ]
  }
}
```

REST였다면 `GET /users`(모든 필드 포함, 오버페칭) 후 사용자마다 `GET /users/{id}/posts`(언더페칭 문제)를 반복해야 했을 조회가, GraphQL에서는 정확히 필요한 필드만 한 번에 온다. 다만 이 유연성에는 대가가 있다 — REST는 [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 다룬 URL 기반 캐싱(CDN, 브라우저 캐시)을 그대로 활용할 수 있지만, GraphQL은 모든 요청이 보통 하나의 엔드포인트(`POST /graphql`)로 몰리고 쿼리마다 응답 모양이 달라, URL 기반 캐싱 전략을 그대로 쓰기 어렵다.

## 비교: REST vs GraphQL

| 특성 | REST | GraphQL |
|---|---|---|
| 엔드포인트 구조 | 자원마다 별도 URL | 보통 단일 엔드포인트 |
| 필요한 필드만 받기 | 어려움(오버페칭 흔함) | 쉬움(쿼리로 직접 지정) |
| 여러 자원 한 번에 조회 | 여러 요청 필요(언더페칭) | 한 요청으로 가능 |
| HTTP 캐싱 활용 | 쉬움(URL 기반) | 어려움(별도 캐싱 전략 필요) |
| 학습 곡선 | 낮음(HTTP 메서드만 알면 됨) | 높음(스키마·리졸버 이해 필요) |

## 흔한 오개념

**"GraphQL이 REST보다 항상 더 나은 선택이다"** — GraphQL은 오버페칭·언더페칭 문제를 해결하지만, 서버가 임의의 쿼리 조합을 처리해야 하므로 [정규화와 인덱스](/post/computerterms/normalization-and-indexes/)에서 다룬 N+1 쿼리 문제가 서버 내부에서 오히려 더 쉽게 발생할 수 있다(사용자마다 게시글을 각각 조회하는 리졸버를 잘못 짜면). 또한 REST의 URL 기반 캐싱을 포기하는 대가가 트래픽이 많은 서비스에서는 상당할 수 있다. 클라이언트의 데이터 요구가 다양하고 자주 바뀌는 프런트엔드(모바일 앱, SPA)에는 GraphQL이, 단순하고 캐싱 효율이 중요한 공개 API에는 REST가 더 적합한 경우가 많다.

**"REST API면 무조건 자원 지향적이다"** — 실무에서 `POST /doSomething`처럼 행위를 URL에 담는 RPC 스타일 엔드포인트를 "REST API"라 부르는 경우가 흔하다. 엄밀한 REST는 URL이 자원(명사)만 나타내고 행위는 HTTP 메서드가 담당해야 하므로, 이런 설계는 REST의 원래 정의에서 벗어난 것이다.

## 다른 개념과의 연결

REST의 캐싱 친화성은 [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 다룬 URL 기반 무효화 전략과 직결된다. 다음 챕터에서는 REST·GraphQL과 달리 클라이언트-서버가 지속적으로 양방향 통신해야 하는 상황(실시간 채팅 등)을 위한 웹소켓과, 그 통신을 가로막는 CORS 정책을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 오버페칭과 언더페칭이 각각 무엇이고, REST에서 왜 발생하기 쉬운지 설명할 수 있다. GraphQL이 이 문제를 해결하는 방식과, 그 대가로 잃는 것(URL 기반 캐싱)을 설명할 수 있다. 서비스 특성에 따라 REST와 GraphQL 중 하나를 근거를 갖고 선택할 수 있다.

## 참고 자료

> Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures* (PhD dissertation), Chapter 5: REST. UC Irvine.

- [GraphQL Official Documentation](https://graphql.org/learn/) — GraphQL 스키마·쿼리·리졸버 공식 가이드
- [Microsoft: Web API Design Best Practices](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design) — REST API 설계 원칙과 자원 지향 URL 규칙
