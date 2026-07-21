---
image: "wordcloud.png"
slug: cookies-and-local-storage
collection_order: 90
draft: false
title: "[Computer Terms] 쿠키와 로컬 스토리지 (Cookie, Local Storage)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "쿠키는 매 요청에 자동으로 전송되는 브라우저 저장소이고, 로컬 스토리지는 JS로만 접근하는 저장소입니다. CSRF·XSS 위험과 HttpOnly·Secure 속성을 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Web(웹)
- HTTP(HyperText Transfer Protocol)
- Authentication(인증)
- Security(보안)
- Frontend(프론트엔드)
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
- Browser
- Session(세션)
- Cookie
- Local-Storage
- XSS
- CSRF
---

## 이 장을 읽기 전에

[인증과 인가](/post/computerterms/authentication-and-authorization/)에서 다룬 세션 쿠키의 개념과, [웹 취약점](/post/computerterms/web-vulnerabilities/)에서 다룬 XSS·CSRF 공격을 안다고 가정한다. 이 챕터는 그 세션 쿠키를 "브라우저가 데이터를 어디에, 어떻게 저장하는가"라는 저장소 메커니즘 관점에서 상세히 다룬다.

## 브라우저가 데이터를 저장하는 세 가지 방법

브라우저는 서버가 로그인 상태나 사용자 설정 같은 데이터를 클라이언트 쪽에 남겨두고 싶을 때 쓸 수 있는 저장소를 여러 개 제공한다. 가장 오래된 것이 **쿠키(Cookie)**이고, 이후 HTML5에서 **로컬 스토리지(Local Storage)**와 **세션 스토리지(Session Storage)**가 추가됐다. 셋 다 브라우저에 데이터를 남긴다는 점은 같지만, [인증과 인가](/post/computerterms/authentication-and-authorization/)에서 세션 쿠키를 다룰 때 이미 마주쳤던 핵심 차이 — **누가 이 데이터를 서버로 보내는가** — 가 셋의 용도를 가른다.

## 쿠키: 서버가 지정하고 브라우저가 자동으로 실어 보낸다

**쿠키**는 서버가 응답 헤더 `Set-Cookie`로 값을 지정하면, 브라우저가 그 값을 저장해두고 **같은 도메인으로 가는 모든 요청에 자동으로** 실어 보내는 저장소다.

```text
서버 → 브라우저:
  HTTP/1.1 200 OK
  Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Lax

브라우저 → 서버 (이후 같은 도메인으로 가는 모든 요청에 자동 포함):
  GET /profile HTTP/1.1
  Cookie: session_id=abc123
```

[인증과 인가](/post/computerterms/authentication-and-authorization/)에서 로그인 세션을 쿠키로 유지하는 이유가 바로 이 자동 전송이다 — 클라이언트 코드가 매 요청마다 세션 ID를 직접 실어 보내지 않아도, 브라우저가 알아서 처리한다. 하지만 이 "자동으로 실린다"는 편의성이 그대로 위험 요인이 된다. 사용자가 악성 사이트를 열기만 해도 그 사이트의 스크립트가 은행 사이트로 요청을 보낼 수 있고, 브라우저는 그 요청에도 은행 세션 쿠키를 자동으로 실어 보낸다 — [웹 취약점](/post/computerterms/web-vulnerabilities/)에서 다룬 **CSRF(Cross-Site Request Forgery)**가 바로 이 자동 전송을 악용하는 공격이다.

## 로컬 스토리지·세션 스토리지: JS로만 접근, 자동 전송 없음

**로컬 스토리지**는 브라우저의 `window.localStorage` 객체를 통해 JavaScript 코드가 직접 읽고 쓰는 저장소다. 쿠키와 달리 서버로 자동 전송되지 않는다 — 서버에 값을 보내려면 클라이언트 코드가 명시적으로 요청 본문이나 헤더에 담아야 한다.

```javascript
// 저장
localStorage.setItem("theme", "dark");

// 읽기
const theme = localStorage.getItem("theme");

// 서버로 보내려면 명시적으로 담아야 한다(쿠키처럼 자동 전송 안 됨)
fetch("/api/settings", {
  method: "POST",
  headers: { "Authorization": `Bearer ${localStorage.getItem("token")}` },
});
```

**세션 스토리지(`window.sessionStorage`)**는 API가 로컬 스토리지와 동일하지만, 저장된 값이 탭을 닫으면 사라진다는 점만 다르다 — 로컬 스토리지는 사용자가 직접 지우거나 만료 정책을 두지 않는 한 브라우저를 껐다 켜도 남아 있다.

자동 전송이 없다는 특성은 CSRF 위험을 없애지만 대신 다른 위험을 연다. 로컬 스토리지 값은 그 페이지에서 실행되는 모든 JavaScript가 `localStorage.getItem(...)` 한 줄로 읽을 수 있다. 만약 페이지에 [웹 취약점](/post/computerterms/web-vulnerabilities/)에서 다룬 **XSS(Cross-Site Scripting)** 취약점이 있어 공격자의 스크립트가 삽입되면, 그 스크립트는 로컬 스토리지에 저장된 토큰을 그대로 읽어 공격자 서버로 전송할 수 있다. 쿠키에 `HttpOnly` 속성을 붙이면 JavaScript가 아예 접근하지 못하게 막을 수 있지만, 로컬 스토리지에는 이런 접근 차단 옵션 자체가 없다.

## HttpOnly와 Secure: 쿠키를 보호하는 속성

쿠키에는 위험을 줄이는 몇 가지 속성을 붙일 수 있다. **`HttpOnly`**는 JavaScript의 `document.cookie`로 해당 쿠키를 읽지 못하게 막아, XSS로 스크립트가 삽입되더라도 쿠키 값을 훔칠 수 없게 한다. **`Secure`**는 HTTPS 연결에서만 쿠키를 전송하게 강제해, [HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 평문 HTTP 구간에서 쿠키가 도청되는 것을 막는다. **`SameSite`**는 다른 사이트에서 시작된 요청에 쿠키를 실어 보낼지를 제어해 CSRF 위험을 줄인다(`Strict`는 항상 차단, `Lax`는 일반 링크 이동은 허용, `None`은 항상 허용).

## 비교: 쿠키 vs 로컬 스토리지

| 특성 | 쿠키 | 로컬 스토리지 |
|---|---|---|
| 서버로 자동 전송 | 예(매 요청마다) | 아니오(명시적 코드 필요) |
| 저장 용량 | 약 4KB | 약 5–10MB(브라우저마다 다름) |
| 만료 설정 | `Expires`/`Max-Age`로 서버가 지정 가능 | 만료 개념 없음(직접 지워야 함) |
| JS 접근 차단 | `HttpOnly`로 가능 | 불가능(항상 JS로 읽힘) |
| 주요 위험 | CSRF(자동 전송 악용) | XSS(스크립트가 값을 직접 읽음) |
| 적합한 데이터 | 인증 세션, 서버가 매 요청마다 봐야 하는 값 | UI 설정, 서버가 몰라도 되는 클라이언트 전용 상태 |

## 흔한 오개념

**"로컬 스토리지가 쿠키보다 안전하니 토큰은 로컬 스토리지에 저장해야 한다"** — 실무에서 JWT 같은 인증 토큰을 로컬 스토리지에 저장하는 경우가 흔하지만, 이는 CSRF 위험을 XSS 위험으로 바꾸는 것에 가깝다. 로컬 스토리지는 CSRF에서는 안전해도, XSS 취약점 하나만 있으면 스크립트가 토큰을 그대로 탈취할 수 있어 오히려 더 광범위한 피해(토큰이 임의 위치로 유출)로 이어질 수 있다. `HttpOnly` + `Secure` + `SameSite=Lax` 쿠키가 XSS로부터 토큰 자체는 보호하면서 CSRF도 `SameSite`로 완화하는, 더 균형 잡힌 선택으로 평가받는 경우가 많다.

**"쿠키는 오래된 기술이라 곧 사라진다"** — 서드파티 쿠키(다른 도메인이 삽입하는 추적용 쿠키)는 브라우저·규제 양쪽에서 제한이 강화되고 있지만, 이는 광고 추적 목적의 쿠키에 해당하는 이야기다. 같은 사이트가 자신의 세션을 유지하기 위해 쓰는 **퍼스트파티 쿠키**는 [인증과 인가](/post/computerterms/authentication-and-authorization/)의 핵심 메커니즘으로 계속 쓰이며, 서드파티 쿠키 규제와는 별개의 문제다.

## 다른 개념과의 연결

쿠키의 자동 전송 특성은 [웹 취약점](/post/computerterms/web-vulnerabilities/)에서 다룬 CSRF 공격의 전제 조건이고, 로컬 스토리지의 JS 접근 가능성은 같은 글의 XSS 공격과 직결된다. 다음 챕터에서는 저장소를 벗어나, 같은 URL이 클라이언트가 원하는 형식에 따라 다른 응답을 돌려주는 콘텐츠 협상을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 쿠키와 로컬 스토리지의 자동 전송 여부 차이와, 그로부터 각각 CSRF·XSS 위험이 어떻게 갈리는지 설명할 수 있다. `HttpOnly`·`Secure`·`SameSite` 속성이 각각 어떤 공격을 완화하는지 설명할 수 있다. 데이터 종류(인증 토큰 vs UI 설정)에 따라 적합한 저장소를 선택할 수 있다.

## 참고 자료

> "This document defines the HTTP Cookie and Set-Cookie header fields." — Barth, A. (2011). *RFC 6265: HTTP State Management Mechanism*, Section 1. IETF.

- [MDN: Using HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies) — 쿠키 속성과 보안 옵션 전체 레퍼런스
- [MDN: Window.localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage) — 로컬 스토리지 API와 용량·저장 방식
