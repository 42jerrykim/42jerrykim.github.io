---
title: "[Web] 게이트키퍼 없는 웹 - 에이전트 인증·인가 원칙"
description: "Cloudflare의 'signed agents/verified bots'는 개방형 웹에 게이트키퍼를 들이는 위험이 있다. DNS 공개키·위임 체인·요청 서명 기반 인증과 작업 단위 제약 토큰(마카룬·비스킷), OPA·Cedar로 열린 표준 구현 길을 정리한다."
date: 2025-09-01
lastmod: 2025-09-01
categories: 
- "Web"
- "Security"
tags: 
- "open-web"
- "gatekeepers"
- "verified-bots"
- "signed-agents"
- "cloudflare"
- "allowlist"
- "whitelist"
- "blacklist"
- "bot-management"
- "decentralization"
- "protocols"
- "standards"
- "w3c"
- "html5"
- "flash"
- "silverlight"
- "dns"
- "dns-based-auth"
- "dnssec"
- "public-keys"
- "authentication"
- "authorization"
- "oauth"
- "jwt"
- "macaroon"
- "macaroons"
- "biscuit"
- "capability-tokens"
- "opa"
- "rego"
- "cedar"
- "rbac"
- "abac"
- "delegation"
- "chain-of-delegation"
- "request-signature"
- "task-scoped-credentials"
- "verifiable-credentials"
- "ai-agents"
- "agents"
- "agent-identity"
- "agent-authorization"
- "bot-passport"
- "vendor-lock-in"
- "interoperability"
- "portability"
- "security"
- "privacy"
- "policy-engine"
- "open-standards"
- "internet"
- "web-architecture"
- "protocol-design"
- "dns-txt"
- "dns-publish-keys"
- "zero-trust"
- "agent-discovery"
- "aid"
- "pkarr"
- "개방형-웹"
- "게이트키퍼"
- "화이트리스트"
- "블랙리스트"
- "표준"
- "프로토콜"
- "인증"
- "인가"
- "위임"
- "위임-체인"
- "요청-서명"
- "작업-범위-자격증명"
- "검증가능-자격증명"
- "정책엔진"
- "보안"
- "프라이버시"
- "상호운용성"
- "이식성"
- "벤더-종속"
- "에이전트"
- "AI-에이전트"
- "공개키"
- "플래시"
- "실버라이트"
- "클라우드플레어"
image: "wordcloud.png"
---

Positiveblue의 글 "The Web Does Not Need Gatekeepers"는 에이전트 시대의 웹 거버넌스에 중요한 문제 제기를 던진다. 한 회사가 운영하는 허가목록(allowlist)식 "서명된 에이전트" 모델이 개방형 웹의 기본 원리와 충돌한다는 주장이다. 핵심은 간단하다. 인터넷은 프로토콜로 열려 있었기에 혁신이 가능했고, 다음 세대 사용자(에이전트)에게도 그 원칙이 유지되어야 한다. [원문](https://positiveblue.substack.com/p/the-web-does-not-need-gatekeepers)

## 왜 ‘게이트키퍼 없는 웹’인가

- **역사적 선례**: 폐쇄 플러그인(Flash, Silverlight)은 개방 표준(HTML5)에 밀려났다. 개방형 표준이 혁신을 가속한 대표적 사례다. [HTML5 W3C 권고(2014)](https://www.w3.org/TR/2014/REC-html5-20141028/), [Adobe Flash EOL](https://www.adobe.com/products/flashplayer/end-of-life.html), [Silverlight 지원 종료](https://learn.microsoft.com/ko-kr/lifecycle/announcements/silverlight-end-of-support)
- **구조적 위험**: 단일 사업자가 발급·심사하는 "봇 여권"은 웹을 벤더 정책의 정원으로 바꾼다. 목록에 오르지 못하면 기본적으로 의심받는 구조는 개방형 기본값을 훼손한다. 관련 맥락: [Cloudflare Bot 솔루션 개요](https://developers.cloudflare.com/bots/)

## 에이전트 시대 인증과 인가는 무엇이 달라져야 하나

- **인증(Authentication)**: "누가 행동하는가"를 검증해야 한다. 단일 서명 토큰만으로는 위임 체인과 실제 요청 주체를 담보하기 어렵다. 제안은 다음과 같다.
  - DNS에 공개키를 게시해 제3자 신원을 검증 가능한 방식으로 확인한다(기업 도메인이 키를 소유 증명). 기본 상태는 개방, 각 사이트는 필요 시 차단·허용 정책을 추가. 
  - 실제 요청을 만든 주체가 체인 최종 주체임을 증명하도록 각 단계가 서명에 참여한다(위임 체인 + 요청 레벨 서명).
- **인가(Authorization)**: "무엇을 할 수 있는가"를 작업(Task) 단위로 부여해야 한다. 일반 목적 에이전트에게 관리자 키를 장기 보관시키는 관행은 위험하다.
  - 제약 가능한 짧은 수명 토큰(예: 마카룬, 비스킷)으로 권한을 축소하며 위임한다. [Macaroons](https://en.wikipedia.org/wiki/Macaroons_(computer_science)), [Biscuit](https://github.com/eclipse-biscuit/biscuit)
  - 정책은 중앙 코드와 분리해 고수준 정책 언어로 선언·검증한다. [OPA/Rego](https://www.openpolicyagent.org/), [AWS Cedar](https://www.cedarpolicy.com/en)

## ‘서명된 에이전트’ 접근의 기술적 한계

1) **인증·인가 혼동**: 패스포트 같은 단일 신원 표식으로 인가 문제까지 해결하려는 설계는 실패하기 쉽다.
2) **양도 위험**: 이동 가능한 토큰 하나로 신원을 증명하면 제3자에게 토큰을 넘겨도 동일 권한이 행사된다.
3) **단일 실패 지점**: 중앙 허가목록은 오판·정책 변경·사업 리스크에 따라 대규모 정지·오탐을 유발할 수 있다.

## 대안 아키텍처

1) **도메인-키 정체성(DNS 기반)**
   - 기업은 `example.com`의 DNS에 공개키를 게시하고, 에이전트/하위 에이전트는 그 키 체인에 따라 서명한다.
   - 검증자는 DNSSEC 또는 신뢰 가능한 리졸버와 캐시 정책으로 무결성을 보강한다.
2) **위임 체인 + 요청 서명**
   - 사용자→상위 에이전트→하위 에이전트 순의 위임을 체인으로 명시하고, 실제 HTTP 요청에는 마지막 주체의 서명을 포함한다.
3) **작업 단위 인가(Task-scoped)**
   - "저녁값 결제" 토큰과 "3개월 지출 요약" 토큰은 서로 다른 제약을 갖고, 상호 전용·짧은 수명·하위 위임 가능해야 한다(마카룬/비스킷의 제약식·블록).
4) **정책 분리와 감시**
   - 인가 결정은 OPA(Rego)나 Cedar 정책으로 외부화하고, 감사 추적·재현 가능한 결정 로그를 남긴다.

## 실무 체크리스트

- **DNS 키 게시**: 서비스별 공개키 게시 계획 수립(DNS TXT/SRV; 회전 주기·키 롤오버 포함).
- **요청 서명 표준화**: 요청 본문/헤더 포함 방식, 재전송 방지(Nonce/타임스탬프) 합의.
- **제약 토큰 도입**: 마카룬/비스킷을 PoC로 붙여 작업 단위 권한·짧은 TTL·체인 위임 검증.
- **정책 엔진**: OPA(Rego) 또는 Cedar로 RBAC/ABAC 정책을 코드와 분리하고 테스트 케이스화.
- **모의 차단/허용**: 중앙 허가목록 없이도 공격 완화가 가능한지 Bot 방어 룰셋과 레이트리밋을 리허설. 참고: [Cloudflare Bot](https://developers.cloudflare.com/bots/)

## 결론: 게이트는 기업이 아니라 프로토콜이 지켜야 한다

웹의 힘은 개방과 상호운용성이다. 에이전트가 주류 사용자가 되는 다음 세대에도, 인증·인가·과금은 **기업 승인**이 아니라 **공개 프로토콜**로 해결되어야 한다. 위임 체인과 요청 서명, 작업 단위 제약 토큰, 정책 엔진은 이미 손에 잡히는 도구들이다. 이제 필요한 것은 구현과 합의다.

## 참고 링크
- Positiveblue, "The Web Does Not Need Gatekeepers" — `https://positiveblue.substack.com/p/the-web-does-not-need-gatekeepers`
- Cloudflare, "Cloudflare bot solutions" — `https://developers.cloudflare.com/bots/`
- W3C, "HTML5 Recommendation (2014-10-28)" — `https://www.w3.org/TR/2014/REC-html5-20141028/`
- Adobe, "Adobe Flash Player End of Life" — `https://www.adobe.com/products/flashplayer/end-of-life.html`
- Microsoft Learn, "Silverlight 지원 종료" — `https://learn.microsoft.com/ko-kr/lifecycle/announcements/silverlight-end-of-support`
- Wikipedia, "Macaroons (computer science)" — `https://en.wikipedia.org/wiki/Macaroons_(computer_science)`
- GitHub, "Biscuit authorization token" — `https://github.com/eclipse-biscuit/biscuit`
- Open Policy Agent — `https://www.openpolicyagent.org/`
- AWS Cedar — `https://www.cedarpolicy.com/en`
- Agent Interface Discovery(AID) — `http://aid.agentcommunity.org`


