---
image: "wordcloud.png"
slug: web-application-firewalls
collection_order: 84
draft: false
title: "[Computer Terms] 웹 방화벽 (WAF, Web Application Firewall)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "WAF는 SQL 인젝션·XSS 같은 공격 패턴을 코드 수정 없이 네트워크 계층에서 탐지·차단합니다. 시그니처 기반 탐지의 장단점과 코드 수준 방어를 대체하지 못하는 이유를 다룹니다."
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
- SQL-Injection(SQL인젝션)
- XSS
- OWASP
- Firewall(방화벽)
- WAF
- Network-Security(네트워크보안)
- Signature-Based-Detection(시그니처기반탐지)
- Reverse-Proxy(리버스프록시)
---

## 이 장을 읽기 전에

[웹 취약점](/post/computerterms/web-vulnerabilities/)에서 다룬 SQL 인젝션·XSS·CSRF의 공격 원리, [방화벽과 NAT](/post/computerterms/firewalls-and-nat/)에서 다룬 네트워크 계층 방화벽이 IP·포트 단위로 트래픽을 걸러내는 방식을 안다고 가정한다. 이 챕터는 그 방화벽 개념을 애플리케이션 계층(HTTP 요청 내용)까지 확장한다.

## 코드를 고치지 않고 요청 내용을 검사한다

[웹 취약점](/post/computerterms/web-vulnerabilities/)에서 SQL 인젝션·XSS를 막는 정석 해법은 파라미터화 쿼리와 입력 이스케이핑이라고 다뤘다. 하지만 이 해법은 애플리케이션 코드 자체를 수정해야 적용된다 — 만약 이미 운영 중인 레거시 서비스에 취약한 코드가 있는데 당장 배포할 수 없거나, 프레임워크·서드파티 라이브러리의 결함이라 서비스 쪽에서 직접 고칠 수 없다면 어떻게 할까? **웹 방화벽(WAF, Web Application Firewall)**은 이런 상황을 위한 계층이다. WAF는 클라이언트와 웹 서버 사이에 [정방향·역방향 프록시](/post/computerterms/forward-and-reverse-proxies/)처럼 위치해, 서버에 요청이 도달하기 **전에** HTTP 요청의 내용(URL, 헤더, 바디)을 검사하고 공격 패턴으로 판단되면 서버에 전달하지 않고 차단한다.

```text
클라이언트 요청: GET /search?q=' OR '1'='1
                       │
                       ▼
                 [WAF] 요청 본문·쿼리스트링 검사
                       │
          ┌────────────┴────────────┐
     패턴 일치(SQL 인젝션 시그니처)   패턴 불일치
          │                          │
          ▼                          ▼
    403 차단, 서버 전달 안 함     정상적으로 서버로 전달
```

이 위치 덕분에 WAF는 애플리케이션 코드를 한 줄도 바꾸지 않고도 알려진 공격 패턴을 즉시 막을 수 있다. 클라우드 서비스(AWS WAF, Cloudflare 등)나 리버스 프록시(Nginx의 ModSecurity 모듈 등)로 배포하는 경우가 많아, 새 배포 사이클 없이 규칙(rule)만 추가해 대응 속도를 높일 수 있다는 것이 실무에서 WAF를 쓰는 핵심 이유다.

## 시그니처 기반 탐지: 알려진 패턴은 잘 막고, 새 패턴은 놓친다

WAF가 요청이 악성인지 판단하는 가장 기본적인 방법은 **시그니처 기반 탐지(Signature-Based Detection)**다. `' OR '1'='1`, `<script>`, `UNION SELECT` 같은 알려진 공격 패턴을 정규식이나 규칙 집합으로 미리 정의해두고, 들어오는 요청이 이 패턴과 일치하는지 대조한다.

```text
WAF 규칙 예시(단순화):
  RULE: 쿼리스트링 또는 바디에 "(?i)(union\s+select|or\s+1=1|<script)" 패턴이 있으면 차단

요청 A: GET /product?id=5                     → 패턴 불일치 → 통과
요청 B: GET /product?id=5 UNION SELECT * FROM users  → 패턴 일치 → 차단
```

시그니처 기반 탐지는 이미 알려진 공격 유형에는 빠르고 정확하게 대응하지만, 근본적인 한계가 있다. 시그니처에 없는 새로운 공격 기법(제로데이)이나, 문자를 인코딩·공백을 변형하는 등 시그니처를 우회하도록 살짝 바꾼 변종 공격은 탐지하지 못한다. 예를 들어 `UNION SELECT`를 `UNI/**/ON SEL/**/ECT`처럼 주석으로 쪼개거나 대소문자·인코딩을 바꾸는 우회 기법이 계속 등장하며, WAF 공급자는 이런 우회를 막기 위해 시그니처를 지속적으로 갱신해야 한다. 최근 WAF들은 시그니처만이 아니라 요청 빈도·이상 패턴을 함께 보는 이상 탐지(anomaly detection)나 머신러닝 기반 탐지를 병행하지만, 이 역시 오탐(정상 요청을 차단)과 미탐(공격을 통과시킴) 사이의 트레이드오프에서 자유롭지 않다.

## WAF는 코드 수준 방어를 대체하지 않는다

WAF의 역할을 오해하기 쉬운 지점이 바로 여기다 — WAF는 애플리케이션 코드의 취약점을 **고치는 것이 아니라 우회 통로를 하나 더 막는 것**이다. 근본 원인(파라미터화 쿼리를 쓰지 않는 것, 입력을 이스케이핑하지 않는 것)은 코드 안에 그대로 남아 있고, WAF가 놓친 변종 패턴이나 WAF 규칙 자체의 설정 실수, 혹은 WAF가 적용되지 않는 내부 네트워크 경로를 통한 요청은 여전히 취약점을 그대로 파고들 수 있다. OWASP는 이런 관계를 "심층 방어(Defense in Depth)"의 한 계층으로 WAF를 위치시킨다 — 코드 수준 방어(파라미터화 쿼리, 이스케이핑)가 1차 방어선이고, WAF는 그 위에 놓이는 보조 계층이다.

## 비교: 코드 수준 방어 vs WAF

| 특성 | 코드 수준 방어(파라미터화 쿼리 등) | WAF |
|---|---|---|
| 적용 위치 | 애플리케이션 코드 내부 | 네트워크/프록시 계층 |
| 근본 원인 해결 여부 | 해결함(쿼리 구조 자체를 안전하게) | 해결 안 함(우회 통로만 차단) |
| 새 코드 배포 필요 여부 | 필요함 | 불필요(규칙 추가만으로 대응) |
| 새 공격 패턴 대응 | 원인이 사라지므로 안전 | 시그니처 갱신 전까지 취약 |

## 흔한 오개념

**"WAF를 도입하면 SQL 인젝션·XSS는 걱정하지 않아도 된다"** — [웹 취약점](/post/computerterms/web-vulnerabilities/)에서 다룬 파라미터화 쿼리·이스케이핑을 대체할 수 있는 도구가 아니다. 시그니처 우회 기법이 계속 등장하고, WAF 뒤에 있는 내부 서비스 간 호출처럼 WAF를 거치지 않는 경로가 있을 수 있다. WAF는 심층 방어의 한 계층일 뿐, 유일한 방어선으로 설계하면 안 된다.

**"WAF와 방화벽은 같은 것이다"** — [방화벽과 NAT](/post/computerterms/firewalls-and-nat/)에서 다룬 전통적인 방화벽은 IP·포트·프로토콜 단위로 트래픽을 걸러내는 네트워크 계층(3–4계층) 장비다. WAF는 HTTP 요청의 URL·헤더·바디 내용까지 들여다보는 애플리케이션 계층(7계층) 필터로, 다루는 정보의 계층 자체가 다르다. 조직은 보통 두 계층을 함께 운용한다.

## 다른 개념과의 연결

WAF가 검사하는 HTTP 요청 구조는 [HTTP와 HTTPS](/post/computerterms/http-and-https/)에서 다룬 요청·응답 모델을 그대로 쓰고, WAF의 배치 위치는 [정방향·역방향 프록시](/post/computerterms/forward-and-reverse-proxies/)에서 다룬 리버스 프록시 패턴과 겹친다. 다음 챕터에서는 "이 데이터를 누가 작성했는가"를 증명하는 [디지털 서명과 인증서](/post/computerterms/digital-signatures-and-certificates/)를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. WAF가 애플리케이션 코드를 수정하지 않고 어떻게 공격을 차단하는지 설명할 수 있다. 시그니처 기반 탐지의 장점과, 새로운 공격 패턴에 취약한 이유를 설명할 수 있다. WAF가 코드 수준 방어(파라미터화 쿼리 등)를 대체하지 못하고 보완하는 관계임을 설명할 수 있다.

## 참고 자료

> OWASP Foundation. (2021). *OWASP Top 10:2021*.

- [OWASP: Web Application Firewall](https://owasp.org/www-community/Web_Application_Firewall) — WAF의 정의와 배치 방식
- [AWS: What is AWS WAF?](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html) — 시그니처(규칙) 기반 탐지의 실무 구현 사례
