---
title: "[AI] zg(zvec-grep): 온디바이스 하이브리드 검색으로 에이전트 도구 호출 줄이기"
description: "Qwen 팀이 오픈소스로 공개한 CLI 도구 zg(zvec-grep)는 ripgrep·BM25·벡터 검색을 하나로 묶어 자연어 의도로 코드를 찾게 한다. 3단계 검색 구조와 벤치마크로 확인된 도구 호출·토큰 절감폭, 적용 판단 기준을 정리했다."
date: 2026-09-20
lastmod: 2026-09-20
draft: false
categories:
  - AI
tags:
  - AI(인공지능)
  - On-Device-AI(온디바이스AI)
  - Information-Retrieval(정보검색)
  - Vector-Database(벡터데이터베이스)
  - Embedding(임베딩)
  - MCP(Model Context Protocol)
  - Full-Text-Search(전문검색)
  - Open-Source(오픈소스)
  - Automation(자동화)
  - Productivity(생산성)
  - Benchmark(벤치마크)
  - Workflow(워크플로우)
  - Node.js
  - Shell(셸)
  - Best-Practices
  - How-To
  - Case-Study
  - Deep-Dive
  - zg
  - zvec-grep
  - ripgrep
  - Qwen
  - Alibaba
  - BM25
  - Claude-Code
  - Codex
  - Cursor
  - OpenCode
  - Semantic-Search
  - Local-First
  - Coding-Agent
  - Search-Tool
image: "wordcloud.png"
---

코딩 에이전트에게 "테마 환경설정이 시작할 때 어떻게 복원되는지 찾아줘"라고 시키면, 에이전트는 `restore`, `theme`, `preference` 같은 단어로 `rg`를 여러 번 돌려본다. 실제 구현 함수 이름이 `hydratePreferences`라면 이 검색은 전부 빗나간다. Qwen 팀(Alibaba)이 2026년 9월 2일 오픈소스로 공개한 CLI 도구 zg(zvec-grep)는 이 간극—사람이 쓰는 자연어 의도와 코드베이스의 실제 어휘 사이의 간극—을 메우기 위해 만들어졌다. ripgrep(rg) 수준의 정확한 텍스트 매칭에 벡터 검색과 BM25를 얹어, 정확한 키워드를 몰라도 의도만으로 탐색을 시작할 수 있게 한다.

이 글은 zg의 3단계 검색 구조, 공식 발표에서 밝힌 벤치마크 수치, 그리고 이 도구를 실제로 언제 도입할 가치가 있는지 판단 기준까지 정리한다.

---

## 왜 만들었나 — grep이 못 찾는 질문들

ripgrep 같은 텍스트 검색 도구는 함수명·설정값·오류 메시지처럼 검색 대상을 정확히 특정할 수 있을 때 빠르고 정밀하다. 문제는 에이전트가 코드 이해, 장애 진단, 지식 질의응답, 리서치 분석까지 맡으면서 검색 입력이 명시적 문자열에서 "시스템이 어떻게 동작하는가", "이 개념은 코드에서 뭐라고 불리는가" 같은 자연어 표현으로 옮겨갔다는 데 있다. "access request process"를 찾고 있는데 실제 문서에는 "account authorization and approval"로 쓰여 있는 경우, 정확한 키워드 없이는 텍스트 일치 검색이 관련 내용을 그냥 지나친다. 검색 범위를 넓히면 이번에는 관련도 순위가 없는 결과가 쏟아져, 에이전트가 여러 질의를 반복하고 흩어진 파일들을 읽어 문맥을 조립해야 한다. 이 과정에서 도구 호출 수·응답 시간·컨텍스트 소비가 함께 늘어나고, 그렇게 모은 근거도 여전히 불완전할 수 있다(출처: [Zvec 공식 블로그, "From rg to zg: Local Search Beyond Keywords"](https://zvec.org/en/blog/2026-08-28-zvec-grep-open-source/)).

zg는 이 문제를 "rg의 속도와 정확한 검증 능력은 유지하면서, 의미 기반 발견·관련도 순위화·컨텍스트 조직화를 추가한다"는 방향으로 풀었다.

## 구조 — 탐색에서 검증까지 3단계

zg는 검색을 하나의 고정된 파이프라인으로 강제하지 않는다. 대신 의미 검색(semantic search) · BM25 · 하이브리드 검색 · ripgrep 검증이라는 네 가지 모드를 하나의 CLI/MCP 인터페이스 안에 두고, 단서가 충분하면 곧바로 정확한 검색 단계로 건너뛸 수 있게 한다. 공식 문서가 제시하는 기본 흐름은 아래 3단계다.

```mermaid
flowchart LR
    Query["자연어 질의</br>(예: 테마 설정 복원 로직)"] --> Explore["1. 탐색</br>Semantic Search"]
    Explore --> Narrow["2. 좁혀나가기</br>BM25 · 하이브리드 검색"]
    Narrow --> Verify["3. 검증</br>ripgrep 정확 매칭"]
    Verify --> Result["파일 위치 +</br>관련 근거"]
    Query -.->|"단서가 이미 충분하면 바로 점프"| Verify
```

**탐색** 단계는 개념·의도 기반의 개방형 질의에 의미 검색을 쓴다. **좁혀나가기** 단계는 키워드 힌트가 어느 정도 있을 때 BM25나 하이브리드 검색으로 후보를 관련도 순으로 좁힌다. **검증** 단계는 좁혀진 후보를 ripgrep으로 정확히 대조해 실제 위치를 확인한다. 이 구조는 "의미 검색으로 넓게 찾고 → 관련도로 좁히고 → 정확한 매칭으로 검증한다"는 원칙을 하나의 인터페이스로 압축한 것이며, 동시에 코드·문서·구조화 데이터의 심볼·제목·계층 구조를 보존하는 다중 포맷 추출, 여러 검색 경로 결과를 통합·재순위화해 온디맨드 미리보기로 토큰 소비를 최소화하는 컨텍스트 효율성, 그리고 파일 스캔·인덱싱·임베딩 생성이 기기 내에서 끝나는 로컬 우선 원칙까지 4가지 설계 원칙 위에 서 있다(출처: 위와 동일).

## 온디바이스 임베딩 — 16M 파라미터로 충분한 이유

zg의 기본 임베딩 모델은 **potion-code-16m-v2**로, 1,600만 개 파라미터의 정적(static) 모델이다. 로컬 캐시 용량은 약 32MB에 불과하고 GPU 없이 CPU만으로 동작한다. 공식 발표는 이 경량 모델이 "SWE-QA-Bench에서 qwen/qwen3.7-text-embedding에 근접한 작업 성능"을 낸다고 밝혔다. 성능 지표로는 Apple M4 Pro에서 Django 저장소(3,457개 파일) 전체를 30초 이내에 인덱싱한다(출처: 위와 동일). zg는 이 기본 모델 외에도 코드·문서·다국어·장문 입력·경량 실행용으로 나뉜 11개의 온디바이스 모델을 지원해, 저장소 특성에 맞게 임베딩 모델을 바꿔 쓸 수 있다. 실제로 GitHub 저장소의 사용 예시는 `zg index --embedding local/potion-retrieval-32m`처럼 다른 모델을 명시적으로 지정하는 방법을 보여준다(출처: [zvec-ai/zvec-grep GitHub 저장소](https://github.com/zvec-ai/zvec-grep)).

데이터 프라이버시 측면에서는 파일 스캔·콘텐츠 추출·임베딩 생성·인덱싱·검색이 모두 기기 내부에서 처리되고, 원격 임베딩 기능은 사용자가 명시적으로 승인해야만 켜진다 — "원격 기능은 자동으로 활성화되지 않는다"는 것이 공식 문서의 설명이다(출처: 위와 동일).

## MCP와 에이전트 자동 감지

zg는 macOS·Linux·Windows에서 CLI와 MCP(Model Context Protocol) 두 인터페이스를 모두 지원한다. 설치 시 Codex, Claude Code, Cursor, OpenCode 같은 코딩 에이전트를 자동으로 감지해 별도의 수동 배포나 통합 설정 없이 연결한다. CLI와 MCP는 같은 로컬 인덱스를 공유하므로, 터미널에서 직접 검색하든 에이전트가 도구로 호출하든 인덱스를 중복으로 구축할 필요가 없다.

```bash
# 1단계: 설치 (Node.js 22 이상 필요)
npm install -g @zvec/zvec-grep
zg install   # 연결된 에이전트 자동 감지 및 설정

# 2단계: 저장소 인덱스 구축
cd your-repository
zg index

# 3단계: 검색 실행 (CLI)
zg query --human "theme preference persistence on startup"

# 또는 연결된 에이전트에 자연어로 그대로 요청
# "Find how theme preferences are restored on startup."
```

지원 콘텐츠 유형도 코드에 한정되지 않는다. C/C++·Go·Java·JavaScript/TypeScript·Python·Rust·Vue·Svelte는 구조 파싱으로 심볼·시그니처·계층을 추출하고, Markdown·평문·reStructuredText·HTML/XML은 문서로, CSV·JSON·TOML·YAML은 구조화 데이터로 처리한다(출처: 위와 동일).

## 벤치마크로 확인된 효과

공식 발표가 제시한 두 벤치마크 결과는 다음과 같다.

| 벤치마크 | 문항 수 | 도구 호출 | 입력 토큰 | 기타 지표 |
|---|---|---|---|---|
| SWE-QA-Bench(코드 저장소 QA) | 20문제 | 50% 이상 감소 | 절반 가까이 감소 | Judge 점수 1.50점 상승 |
| BrowseComp-Plus(심화 리서치) | 80문제 | 43.52% 감소 | 37.56% 감소 | 정확도 98.67% → 99.00%, 에이전트 실행시간 38.58% 감소 |

(출처: [Zvec 공식 블로그](https://zvec.org/en/blog/2026-08-28-zvec-grep-open-source/), [GeekNews 요약, 2026-09-04 확인](https://news.hada.io/topic?id=33183))

주목할 점은 BrowseComp-Plus에서 정확도가 떨어지지 않고 오히려 소폭 올랐다는 것이다. 즉 zg 도입이 "품질을 희생해 비용만 줄이는" 트레이드오프가 아니라, 같은 정확도(또는 더 나은 정확도)를 더 적은 도구 호출·토큰으로 얻는 방향으로 작동했다는 뜻이다. 이 결과는 Pylint·Matplotlib·Django 같은 실제 오픈소스 저장소에서 구조적 질문을 푸는 사례로도 검증되었다.

## 적용 시나리오와 판단 기준

zg가 도움이 되는 상황과 굳이 필요 없는 상황은 뚜렷이 갈린다.

**도입을 고려할 만한 경우**: 대규모 저장소에서 에이전트가 반복적으로 코드 이해·장애 진단·문서 탐색 작업을 수행하고, 검색어가 코드의 실제 심볼명과 자연어 사이에서 자주 어긋나는 팀. Claude Code·Cursor·Codex·OpenCode처럼 zg가 이미 자동 감지하는 에이전트 환경을 쓰고 있다면 통합 비용이 거의 없다. 토큰·도구 호출 수가 곧 비용인 에이전트 파이프라인에서는 벤치마크가 보여준 30–50%대 절감폭이 실질적인 운영비 절감으로 이어질 수 있다.

**과한 선택일 수 있는 경우**: 검색 대상이 이미 명확한 함수명·오류 문자열·설정 키로 특정되는 소규모 저장소라면, ripgrep 단독으로도 충분히 빠르고 정확하다. 의미 검색·BM25 인덱스를 추가로 구축·유지하는 비용(인덱싱 시간, 로컬 캐시 용량, Node.js 22 런타임 의존성)이 얻는 이득보다 클 수 있다. 또한 zg가 현재 지원하는 콘텐츠는 코드·문서·구조화 데이터 위주이며, PDF·Word·PowerPoint나 이미지 OCR·크로스모달 검색은 로드맵 단계로 아직 제공되지 않는다(출처: [Zvec 공식 블로그](https://zvec.org/en/blog/2026-08-28-zvec-grep-open-source/)).

## 한계와 신뢰도 — 벤더 자체 벤치마크라는 점

zg는 2026년 9월 2일 공개된 지 얼마 되지 않은 프로젝트다. 도입 판단에 앞서 짚어둘 만한 지점이 몇 가지 있다.

- **벤치마크 표본이 작고 자체 실행 결과다**: SWE-QA-Bench는 20문제, BrowseComp-Plus는 80문제로 표본 크기가 크지 않고, 보고된 절감폭은 모두 Qwen/Zvec 팀이 자체적으로 실행한 결과다. 제3자 매체(MarkTechPost)도 이 점을 지적하며 "독립적 검증이 다음 단계"라고 평가했다(출처: [MarkTechPost, "Qwen Developers Open-Sources zg (zvec-grep)", 2026-09-02](https://www.marktechpost.com/2026/09/02/qwen-developers-open-sources-zg-zvec-grep-a-local-first-search-layer-unifying-ripgrep-bm25-and-vector-search/)).
- **문서와 실제 기능 사이에 사소한 불일치가 있었다**: 같은 매체는 런칭 게시물이 11개의 온디바이스 모델을 언급했지만 당시 문서에는 10개만 명시돼 있었다고 짚었다. 막 공개된 프로젝트답게 문서가 코드를 완전히 따라잡지 못한 흔적으로 볼 수 있다.
- **런타임·플랫폼 의존성**: Node.js 22 이상이 필수이며, GPU 없이 동작하도록 설계됐지만 대규모 모노레포에서의 인덱싱 시간·디스크 사용량은 아직 폭넓게 검증되지 않았다.

이 세 가지는 zg가 쓸모없다는 뜻이 아니라, "벤더가 제시한 수치"와 "자신의 저장소·워크플로에서 실측한 결과"를 구분해서 판단해야 한다는 뜻에 가깝다. 실제 도입 전에는 자신의 저장소 규모와 에이전트 워크플로로 직접 `zg index` → `zg query`를 돌려 도구 호출·토큰 소비 변화를 재보는 편이 안전하다.

## 시작하기

```bash
# Node.js 22 이상 확인
node --version

# 전역 설치
npm install -g @zvec/zvec-grep

# 연결된 에이전트 자동 감지 (Codex, Claude Code, Cursor, OpenCode)
zg install

# 저장소 루트에서 인덱스 구축
cd /path/to/your/repo
zg index

# 자연어 질의로 검색
zg query --human "여기에 찾고 싶은 로직을 자연어로 쓴다"
```

라이선스는 Apache 2.0으로 상업적 사용도 허용된다. 이후 그래프 검색·재순위화 같은 검색 기능 확장, PDF/Word/PowerPoint·이미지 OCR 지원, iOS/Android 같은 제한된 리소스 환경 대응이 공식 로드맵에 올라 있다(출처: [Zvec 공식 블로그](https://zvec.org/en/blog/2026-08-28-zvec-grep-open-source/)).

## 참고 및 출처

- [Zvec 공식 블로그, "From rg to zg: Local Search Beyond Keywords" (2026-08-28)](https://zvec.org/en/blog/2026-08-28-zvec-grep-open-source/)
- [zvec-ai/zvec-grep GitHub 저장소](https://github.com/zvec-ai/zvec-grep)
- [Qwen Developers, X(트위터) 공개 발표 (2026-09-02)](https://x.com/QwenDevs/status/2095157452904018263)
- [GeekNews, "zg(zvec-grep) — 키워드를 넘어서는 로컬 검색 인프라" (2026-09-04 확인)](https://news.hada.io/topic?id=33183)
- [MarkTechPost, "Qwen Developers Open-Sources zg (zvec-grep): A Local-First Search Layer Unifying ripgrep, BM25, and Vector Search" (2026-09-02)](https://www.marktechpost.com/2026/09/02/qwen-developers-open-sources-zg-zvec-grep-a-local-first-search-layer-unifying-ripgrep-bm25-and-vector-search/)
