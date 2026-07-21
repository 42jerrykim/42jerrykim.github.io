---
image: "wordcloud.png"
slug: authentication-and-authorization
collection_order: 24
draft: false
title: "[Computer Terms] 인증과 인가 (Authentication, Authorization)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "인증은 사용자가 누구인지 확인하는 것이고, 인가는 그 사용자가 무엇을 할 수 있는지 결정하는 것입니다. 세션 기반과 토큰(JWT) 기반 인증을 비교하고 권한 상승 취약점을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Security(보안)
- Authentication(인증)
- Authorization(인가)
- JWT
- Session(세션)
- Cookie(쿠키)
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
- Debugging(디버깅)
- Performance(성능)
- Advanced
---

## 이 장을 읽기 전에

[HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 HTTP의 무상태성과 쿠키의 역할, [암호화와 해싱](/post/computerterms/encryption-and-hashing/)에서 다룬 비밀번호 해시·서명을 안다고 가정한다.

## 인증과 인가는 다른 질문에 답한다

**인증(Authentication)**은 "당신이 누구인지 증명하라"는 질문에 답하는 과정이다 — 아이디·비밀번호, 생체 인식, OTP가 모두 인증 수단이다. **인가(Authorization)**는 인증으로 확인된 사용자가 "무엇을 할 수 있는가"를 결정하는 과정이다 — 로그인은 됐지만 관리자 전용 페이지에는 접근할 수 없는 것이 인가 실패의 예다. 두 개념을 구분하지 못하면 "로그인만 하면 뭐든 할 수 있다"는 식의 설계 실수로 이어지기 쉽다.

## 세션 기반 인증: 서버가 기억한다

로그인에 성공하면 서버는 그 사용자를 식별하는 **세션(Session)**을 만들어 서버 측 저장소(메모리, [해시테이블](/post/computerterms/hash-tables/) 또는 [캐싱](/post/computerterms/caching-and-invalidation/)에서 다룬 Redis 같은 키-값 저장소)에 저장하고, 클라이언트에게는 그 세션을 가리키는 무작위 ID만 쿠키로 내려준다. 이후 요청마다 클라이언트가 이 쿠키를 함께 보내면, 서버는 쿠키의 세션 ID로 저장소를 조회해 "누구의 요청인지"를 알아낸다.

```text
로그인 성공 → 서버: 세션 저장소[abc123] = {user_id: 42, role: "user"}
              서버 → 클라이언트: Set-Cookie: session_id=abc123

이후 요청 → 클라이언트 → 서버: Cookie: session_id=abc123
           서버: 세션 저장소[abc123] 조회 → user_id 42로 인증 확인
```

이 방식은 서버가 언제든 세션을 무효화(로그아웃, 강제 만료)할 수 있다는 장점이 있지만, 모든 서버 인스턴스가 같은 세션 저장소를 공유해야 하므로 서버를 수평 확장할 때 별도의 공유 저장소가 필요하다.

## 토큰 기반 인증: 클라이언트가 증거를 들고 다닌다

**JWT(JSON Web Token)** 같은 토큰 기반 인증은 서버가 세션을 따로 저장하지 않는다. 대신 로그인 성공 시 사용자 정보(`user_id`, `role` 등)를 담은 토큰을 만들어, 서버만 아는 비밀키로 **서명(Sign)**해 클라이언트에게 준다. 이후 요청마다 클라이언트가 이 토큰을 실어 보내면, 서버는 저장소를 조회하는 대신 서명이 유효한지만 검증한다 — 서명이 유효하다는 것은 "이 토큰의 내용이 발급 이후 변조되지 않았다"는 것을 보장한다.

```text
로그인 성공 → 서버: payload = {user_id: 42, role: "user"}
              서버: token = sign(payload, server_secret_key)
              서버 → 클라이언트: token

이후 요청 → 클라이언트 → 서버: Authorization: Bearer <token>
           서버: verify(token, server_secret_key) → 서명이 유효하면 payload 신뢰
                 (저장소 조회 없이 payload.role로 바로 인가 판단)
```

토큰 기반은 서버가 상태를 저장하지 않으므로([HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 HTTP 자체의 무상태성과 잘 어울린다) 서버를 여러 대로 확장하기 쉽다. 대신 세션 기반과 달리, 발급된 토큰은 만료 시각이 될 때까지 서버가 개별적으로 무효화하기 어렵다 — 토큰 자체에 서명이 담겨 있어 유효 기간 내내 유효하기 때문이다. 이 문제는 보통 짧은 만료 시간 + 별도의 토큰 폐기 목록(블랙리스트)을 조합해 완화한다.

## 비교: 세션 기반 vs 토큰 기반

| 특성 | 세션 기반 | 토큰 기반(JWT) |
|---|---|---|
| 상태 저장 위치 | 서버(공유 저장소 필요) | 클라이언트(토큰 자체에 담김) |
| 서버 확장성 | 저장소 공유 필요 | 서버 간 상태 공유 불필요 |
| 즉시 무효화(로그아웃) | 쉬움 (저장소에서 삭제) | 어려움 (만료까지 유효, 블랙리스트 필요) |
| 요청마다 비용 | 저장소 조회 | 서명 검증(저장소 조회 없음) |

## 인가 설계의 흔한 함정: 권한 상승

인증에는 성공했지만 인가 검사를 제대로 하지 않으면, 일반 사용자가 관리자 API를 그대로 호출해 권한을 얻는 **권한 상승(Privilege Escalation)** 취약점이 생긴다. 흔한 원인은 "로그인 여부만 확인하고 역할(role)은 확인하지 않는" 코드다.

```text
잘못된 예: if (is_logged_in(request)) { delete_all_users(); }
올바른 예: if (is_logged_in(request) && request.user.role == "admin") { delete_all_users(); }
```

프런트엔드에서 관리자 메뉴를 숨기는 것만으로는 인가가 완성되지 않는다 — 클라이언트 쪽 UI 숨김은 사용성을 위한 것일 뿐, 실제 권한 검사는 반드시 서버가 매 요청마다 다시 확인해야 한다.

## 흔한 오개념

**"HTTPS를 쓰면 인증·인가는 안전하다"** — HTTPS(TLS)는 [암호화와 해싱](/post/computerterms/encryption-and-hashing/)에서 다룬 대로 통신 구간의 도청·변조를 막을 뿐이다. 서버 코드 자체가 역할 검사를 빠뜨리면, 암호화된 통신으로 권한 상승 요청을 그대로 보내는 것을 막지 못한다. 전송 계층 보안과 애플리케이션 계층 인가는 서로 다른 문제다.

**"토큰에 민감한 정보를 넣어도 안전하다, 어차피 서명돼 있으니까"** — JWT의 서명은 **변조 방지**를 보장하지, **내용을 숨기는 것**을 보장하지 않는다. 표준 JWT의 payload는 암호화가 아니라 Base64로만 인코딩돼 있어, 토큰을 가진 사람은 누구나 내용을 그대로 읽을 수 있다. 비밀번호나 주민등록번호 같은 값을 payload에 넣는 것은 심각한 정보 노출로 이어진다.

## 다른 개념과의 연결

세션 저장소는 [캐싱과 캐시 무효화](/post/computerterms/caching-and-invalidation/)에서 다룬 키-값 저장소의 실제 활용 사례이며, JWT 서명은 [암호화와 해싱](/post/computerterms/encryption-and-hashing/)에서 다룬 비대칭키 서명 원리를 그대로 쓴다. 보안 갈래는 이 챕터로 마무리되며, 다음은 코드 구조 자체를 판단하는 소프트웨어 설계 갈래로 이어진다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 인증과 인가의 차이를 예시와 함께 설명할 수 있다. 세션 기반과 토큰 기반 인증의 상태 저장 위치 차이가 서버 확장성과 즉시 무효화 가능 여부에 미치는 영향을 설명할 수 있다. 권한 상승 취약점이 발생하는 전형적인 코드 패턴과, 왜 프런트엔드 UI 숨김만으로는 부족한지 설명할 수 있다.

## 참고 자료

> Jones, M., Bradley, J., & Sakimura, N. (2015). *RFC 7519: JSON Web Token (JWT)*. IETF.

- [OWASP Top 10: Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/) — 인가 실패가 실무에서 가장 흔한 취약점 범주로 꼽히는 이유
- [Auth0: JWT vs Session](https://auth0.com/docs/secure/tokens/json-web-tokens) — 세션 기반과 토큰 기반 인증의 실무 선택 기준
