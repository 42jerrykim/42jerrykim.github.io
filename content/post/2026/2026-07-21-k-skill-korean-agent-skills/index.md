---
title: "[AI] k-skill: 한국인을 위한 Claude Code 스킬 114개 모음집"
description: "NomaDamas가 만든 k-skill은 SRT/KTX 예매부터 등기부등본, 공공데이터 조회까지 한국인 일상 업무 114개를 Claude Code SKILL.md 스킬로 묶은 오픈소스 저장소다. credential 정책, 설치법, 적용 판단 기준을 정리했다."
date: 2026-07-21T10:00:00+09:00
lastmod: 2026-07-21
draft: true
categories:
  - AI
tags:
  - AI(인공지능)
  - LLM(Large Language Model)
  - Automation(자동화)
  - Open-Source(오픈소스)
  - GitHub
  - Git
  - Productivity(생산성)
  - Workflow(워크플로우)
  - Guide(가이드)
  - Tutorial(튜토리얼)
  - How-To
  - Tips
  - Case-Study
  - Best-Practices
  - Documentation(문서화)
  - Technology(기술)
  - Web(웹)
  - API(Application Programming Interface)
  - REST(Representational State Transfer)
  - Configuration(설정)
  - Software-Architecture(소프트웨어아키텍처)
  - Security(보안)
  - Authentication(인증)
  - Privacy(프라이버시)
  - Networking(네트워킹)
  - HTTP(HyperText Transfer Protocol)
  - Python
  - Node.js
  - MCP(Model Context Protocol)
  - Deployment(배포)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Cloud(클라우드)
  - Terminal
  - IDE(Integrated Development Environment)
image: wordcloud.png
---

SRT 표를 잡고, 등기부등본을 떼고, 다이소 매장 재고를 확인하고, 로또 당첨 번호를 대조하는 일. 전부 한국에서만 필요한 작업이고, 전부 서로 다른 사이트를 열어야 하는 일이다. NomaDamas가 만든 [k-skill](https://github.com/NomaDamas/k-skill)은 이런 한국 특화 업무 114개를 Claude Code SKILL.md 스킬로 패키징해 한 번에 설치할 수 있게 만든 오픈소스 저장소다. 이 글에서는 k-skill의 구조와 핵심 설계 결정, 설치 방법, 그리고 실제로 쓸 만한지 판단하는 기준을 정리한다.

---

## 개요

k-skill은 2026-03-24에 만들어져 2026-07-21 기준 GitHub 스타 6,395개, 포크 724개를 기록한 저장소다. MIT 라이선스로 공개돼 있고, 운영 조직인 [NomaDamas](https://github.com/NomaDamas)는 스스로를 "Markr AI가 후원하는 AI 오픈소스 해커 하우스"로 소개한다. README는 목표를 명확히 밝힌다 — "SRT, KTX, KBO, 로또, 당근, 쿠팡, 카톡, 정부24, 홈택스 등등 귀찮은 것을 AI 에이전트에게 다 시켜버리세요." Claude Code, Codex, OpenCode, OpenClaw/ClawHub 등 여러 코딩 에이전트를 지원하며, 별도 클라이언트 API 레이어 없이 필요하면 프록시 서버에 HTTP 요청만 보내는 방식을 택했다.

저장소 루트를 GitHub API로 확인하면 문서·스크립트·패키지용 폴더(`.github`, `docs`, `examples`, `legacy`, `packages`, `python-packages`, `scripts`, `tools`, `.changeset`)를 제외하고 스킬 이름과 1:1로 대응하는 디렉터리가 114개 있다. 각 디렉터리에는 `SKILL.md`와 실행용 helper 스크립트(대부분 Python 또는 Node.js)가 들어 있어, 하나의 스킬이 곧 하나의 독립 패키지처럼 동작한다.

## 아키텍처: SKILL.md와 크로스 에이전트 설계

개별 스킬의 구조를 가장 잘 보여주는 예시가 `srt-booking`이다. 이 스킬의 `SKILL.md`는 YAML frontmatter(`name`, `description`, `license`, `metadata.category/locale/phase`)로 시작해 "언제 쓰는가 / 언제 쓰지 않는가 / 사전 요구사항 / 필요 환경변수 / 입력값 / 워크플로" 순서로 구성된다. `SRTrain` 파이썬 패키지 위에 `scripts/srt_booking.py`라는 얇은 helper를 얹어 조회·예약·취소를 처리하고, 결제까지는 자동화하지 않는다는 경계를 "When not to use" 절에 명시해 둔다.

이 포맷 자체가 Claude Code의 스킬 규격과 호환되기 때문에, 벤더 종속적인 SDK 없이도 Codex·OpenCode 같은 다른 에이전트에 그대로 이식할 수 있다는 게 k-skill의 핵심 설계 방향이다. 실제로 저장소는 Claude Code 전용 설치(`/plugin marketplace add`)와, 어떤 에이전트에서도 쓸 수 있는 범용 `skills` npm CLI 설치(`npx skills add <owner/repo>`) 두 경로를 모두 문서화하고 있다.

## 핵심 설계: Credential Resolution Order와 Hosted Proxy 이원화

k-skill을 단순한 "웹 스크래퍼 모음"과 구분 짓는 지점은 인증 정보를 다루는 방식이다. `docs/security-and-secrets.md`는 인증이 필요한 모든 스킬이 따르는 4단계 우선순위, 이른바 **Credential Resolution Order**를 정의한다.

<pre class="mermaid">
flowchart TD
    checkEnv{"환경변수에 이미 값이 있는가?"} -->|"예"| useEnv["그대로 사용"]
    checkEnv -->|"아니오"| checkVault{"에이전트가 secret vault를 쓰는가?</br>(1Password CLI, Bitwarden CLI, Keychain 등)"}
    checkVault -->|"예"| useVault["vault에서 꺼내 환경변수로 주입"]
    checkVault -->|"아니오"| checkFile{"~/.config/k-skill/secrets.env 존재?"}
    checkFile -->|"예"| useFile["dotenv 파일 사용(권한 0600)"]
    checkFile -->|"아니오"| askUser["사용자에게 물어 vault 또는 파일에 저장"]
</pre>

이 순서는 SRT/KTX 예매처럼 사용자 본인 계정 로그인이 필요한 스킬에 적용된다. 하지만 서울 지하철 도착정보·미세먼지·한강 수위·한국 날씨처럼 API 키만 있으면 되는 공개 데이터 스킬은 전혀 다른 경로를 탄다. 운영자가 관리하는 `k-skill-proxy.nomadamas.org`가 기본값으로 요청을 대신 처리해, 사용자는 아무 키도 발급받지 않고 바로 쓸 수 있다. 이 두 경로가 나뉘는 기준을 저장소 `CLAUDE.md`는 이렇게 못박는다 — "upstream이 API 키를 필요로 해야" 프록시 라우트에 편입하고, 키가 아예 필요 없는 완전 공개 엔드포인트는 스킬 코드가 프록시를 거치지 않고 직접 호출한다.

<pre class="mermaid">
flowchart TD
    needCall["스킬이 외부 데이터를 조회해야 함"] --> needsKey{"upstream이 API 키를 요구하는가?"}
    needsKey -->|"아니오(완전 공개 엔드포인트)"| direct["스킬 코드가 직접 호출</br>(예: 조선왕조실록 검색)"]
    needsKey -->|"예"| delegable{"운영자가 대신 관리 가능한 키인가?"}
    delegable -->|"예"| proxy["k-skill-proxy 경유</br>(hosted fallback, 사용자 키 불필요)"]
    delegable -->|"아니오(본인 계정 로그인 필수)"| byok["사용자 본인 credential 필요</br>(BYOK, 예: SRT/KTX 예매)"]
</pre>

쿠팡 상품 검색처럼 "선택사항"으로 분류된 스킬도 있다. 사용자가 운영 키를 직접 들고 있으면 로컬 HMAC 경로가 열려 더 풍부한 결과를 받고, 없으면 hosted fallback으로 그대로 동작한다. README의 기능 표는 "사용자 로그인" 컬럼으로 이 구분을 명시해, 설치 전에 어떤 스킬이 즉시 쓸 수 있는지 한눈에 판단할 수 있게 해 둔다.

| 구분 | 예시 스킬 | 사용자가 준비할 것 |
|------|----------|-------------------|
| 로그인 필요(BYOK) | `srt-booking`, `ktx-booking`, `toss-securities`, `korean-patent-search` | 본인 계정 ID/비밀번호 또는 API 키 |
| 로그인 불필요(hosted proxy) | `seoul-subway-arrival`, `korea-weather`, `fine-dust-location`, `korean-law-search`, `korean-stock-search` | 없음 — 설치 즉시 동작 |
| 선택사항(BYOK면 더 풍부) | `coupang-product-search` | 없어도 동작, 운영 키가 있으면 로컬 HMAC 경로 활성화 |

## 대표 기능 살펴보기

README의 기능 표는 크게 다섯 갈래로 나뉜다.

### 교통·예약

SRT/KTX/고속버스/시외버스 예매, 자연휴양림 빈 객실 조회, 캐치테이블 예약 스나이핑, 항공권 가격 비교가 여기 속한다. `srt-booking`은 열차 조회는 물론 호차별 좌석번호·콘센트 좌석 확인까지 지원하지만, 결제 자체는 자동화하지 않는다는 경계를 스킬 문서에 명시한다.

### 공공·행정

법령 검색, 등기부등본 자동화, 법인등기 신청 컨설팅, 국세청 사업자등록·체납 조회, 나라장터·국방전자조달 공고, 지방선거 후보자 조회 등이 있다. `iros-registry-automation`처럼 로그인·결제가 필요한 흐름은 자동 진행 대신 브라우저 handoff로 넘기는 설계를 취한다.

### 생활 정보

날씨, 미세먼지, 한강 수위, 지하철 도착정보, 서울 실시간 혼잡도, 따릉이 대여소, 생활쓰레기 배출정보, 학교 급식 식단처럼 조회 전용이면서 로그인이 필요 없는 스킬이 가장 많다. 대부분 hosted proxy로 바로 동작한다.

### 커머스·자산

쿠팡, 다이소, 올리브영, 당근, 번개장터 같은 상거래 검색과 부동산 실거래가, 토스증권, 대신증권 리포트 조회가 여기 속한다.

### 콘텐츠·언어

한국어 맞춤법 검사, AI가 쓴 티 나는 한국어를 사람 글처럼 다듬는 `korean-humanizer`, HWP 문서를 Markdown/JSON으로 변환하는 `hwp`, 조선왕조실록 키워드 검색까지 포함한다.

## 엔지니어링 관행: 릴리스 파이프라인과 크롤링 스킬 원칙

저장소 `CLAUDE.md`는 실전에서 부딪힌 문제를 규칙으로 남겨 뒀다. Changesets 기반 릴리스를 쓰기 때문에 `.changeset/*.md` 파일 존재나 `package.json`의 `version` 필드를 고정 값으로 assert하는 테스트를 금지한다 — 두 값 모두 릴리스 시점에 `changeset version`이 소비·변경하므로, 이를 테스트로 고정하면 다음 버전업 커밋에서 CI가 그대로 깨진다. 또한 크롤링/검색형 스킬은 방법을 고정하기 전에 site-agnostic discovery(공개 입구, 브라우저에서 보이는 데이터 흐름, RSS/sitemap/정적 JSON, 차단·로그인벽 등 실패 모드 확인)를 먼저 수행한 뒤에야 site-dependent 접근 방법을 `SKILL.md`와 helper 코드에 패키징하도록 못박는다. `k-skill-proxy` 자체는 별도 `dev` 브랜치에서 개발되고, `main`에 머지되면 gpu01 서버의 cron이 이를 감지해 테스트·백업·systemd 재시작·`/health` smoke test까지 자동 수행한다.

## 설치 방법

Claude Code에서는 플러그인 마켓플레이스로 전체 스킬을 한 번에 설치할 수 있다.

```text
/plugin marketplace add NomaDamas/k-skill
/plugin install k-skill@k-skill
```

설치하면 스킬이 `/k-skill:<스킬 이름>` 네임스페이스로 호출된다(예: `/k-skill:lotto-results`). 설치 직후에는 공통 설정 스킬을 한 번 실행해 credential 확보와 환경변수 확인을 진행하는 것이 권장 흐름이다.

```text
k-skill-setup 스킬을 사용해서 공통 설정을 진행해줘.
```

Claude Code가 아닌 다른 에이전트(Codex, OpenCode 등)에서는 `skills` npm CLI로 동일한 스킬 세트를 설치할 수 있다.

```bash
npx --yes skills add NomaDamas/k-skill --all -g
```

특정 스킬만 먼저 테스트하고 싶다면 `--skill` 플래그로 선택 설치도 가능하다.

```bash
npx --yes skills add NomaDamas/k-skill \
  --skill korea-weather \
  --skill lotto-results \
  --skill kbo-results
```

## 적용 시나리오와 판단 기준

k-skill은 한국 거주자이면서 AI 에이전트에게 반복적인 조회·예약 업무를 위임하려는 사용자에게 가장 잘 맞는다. 특히 날씨·미세먼지·지하철 도착정보처럼 hosted proxy로 즉시 동작하는 조회형 스킬은 설치 부담이 거의 없어 "일단 전체 설치해 보고 필요한 것만 남긴다"는 저장소의 권장 흐름이 실제로 합리적이다.

반대로 신중해야 할 상황도 있다. SRT/KTX 예매, 토스증권 조회, 팝빌 전자세금계산서 발행처럼 본인 계정 자격 증명을 직접 넘기는 스킬은, 자격 증명을 어디에 어떻게 보관하는지(secret vault vs `~/.config/k-skill/secrets.env`)를 사용자가 이해하고 있어야 안전하게 쓸 수 있다. 또한 예매·결제 자동화는 대상 사이트의 이용약관에 저촉될 소지가 있으므로, 결제 직전 handoff로 설계된 스킬이라도 실제 사용 전에 각 서비스의 자동화 정책을 스스로 확인하는 것이 안전하다. 100개가 넘는 스킬을 전부 설치하면 관리해야 할 스킬 목록 자체가 부담이 될 수 있는데, 이런 경우를 위해 저장소는 사용 빈도 통계를 기반으로 불필요한 스킬 삭제 후보를 추천하는 `k-skill-cleaner` 스킬도 함께 제공한다.

## 장단점과 종합 평가

k-skill의 가장 큰 장점은 스킬 하나하나가 "한국 사이트를 어떻게 다뤄야 하는가"라는, 개인이 처음부터 조사하기엔 번거로운 지식을 이미 정리해서 제공한다는 점이다. Credential Resolution Order와 hosted proxy 이원화 설계는 "즉시 쓸 수 있는 조회형 기능"과 "본인 인증이 필요한 개인화 작업"을 명확히 분리해, 사용자가 어디까지 자신의 자격 증명을 넘겨야 하는지 예측 가능하게 만든다. MIT 라이선스로 코드가 전부 공개돼 있어 helper 스크립트가 실제로 무엇을 호출하는지 직접 확인할 수 있다는 점도 신뢰도를 높인다.

다만 한계도 뚜렷하다. hosted proxy에 의존하는 스킬들은 운영자(NomaDamas)의 서버 가용성과 요금 정책에 사용자 경험이 종속되는 단일 장애점을 안고 있다. 다이소몰처럼 보안 정책 변경으로 특정 조회 기능이 막히는 사례가 실제로 문서에 기록돼 있듯, 대상 사이트의 정책 변화에 취약한 구조이기도 하다. 또한 저장소 규모가 114개 스킬로 계속 커지고 있어, 필요한 기능만 선별해서 쓰지 않으면 오히려 관리 부담이 늘어날 수 있다. 예매·결제·개인정보 조회처럼 민감한 영역의 스킬은 편의성과 별개로, 자격 증명을 에이전트에게 넘기는 행위 자체의 위험을 사용자 스스로 판단해야 한다.

## 참고 및 출처

- [NomaDamas/k-skill — GitHub 저장소](https://github.com/NomaDamas/k-skill)
- [k-skill 공식 홈페이지](https://k-skill.nomadamas.org)
- [저장소 README.md](https://github.com/NomaDamas/k-skill/blob/main/README.md)
- [저장소 CLAUDE.md](https://github.com/NomaDamas/k-skill/blob/main/CLAUDE.md)
- [docs/install.md — 설치 방법](https://github.com/NomaDamas/k-skill/blob/main/docs/install.md)
- [docs/setup.md — 공통 설정 가이드](https://github.com/NomaDamas/k-skill/blob/main/docs/setup.md)
- [docs/security-and-secrets.md — 보안/시크릿 정책](https://github.com/NomaDamas/k-skill/blob/main/docs/security-and-secrets.md)
- [srt-booking/SKILL.md — 개별 스킬 SKILL.md 예시](https://github.com/NomaDamas/k-skill/blob/main/srt-booking/SKILL.md)
- [CONTRIBUTING.md — 기여 가이드](https://github.com/NomaDamas/k-skill/blob/main/CONTRIBUTING.md)
