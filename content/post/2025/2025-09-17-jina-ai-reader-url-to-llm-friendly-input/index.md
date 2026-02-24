---
title: "[AI Tools] Jina AI Reader: URL을 LLM 친화적 입력으로 변환"
description: "Jina AI Reader는 URL 앞에 r.jina.ai 프리픽스만 붙이면 웹페이지·PDF를 LLM 친화적 마크다운으로 변환한다. 스트리밍·JSON 모드, 이미지 캡션, 헤더 제어, SPA 대기까지 지원해 에이전트·RAG 품질을 손쉽게 높인다."
date: 2025-09-17
lastmod: 2025-09-17
categories:
- "AI Tools"
- "Open Source"
tags:
- LLM
- Cache
- Proxy
- Markdown
- HTML
- Open-Source
- GitHub
- API
- Windows
- Linux
- English
- Productivity
- 자동화
- 캐싱
- Blog
- 블로그
- Technology
- 기술
- Web
- 웹
- Tutorial
- 가이드
- Review
- 리뷰
- 마크다운
- JavaScript
- Bash
- Shell
- Git
- Tree
- AI
- Design-Pattern
- Guide
- 생산성
- Education
- 교육
- Reference
- 참고
- Best-Practices
- Documentation
- 문서화
- 오픈소스
- Innovation
- 혁신
- Troubleshooting
- 트러블슈팅
- Configuration
- 설정
- How-To
- Tips
image: "image.png"
---

## 개요

웹 콘텐츠를 LLM이 이해하기 쉬운 입력으로 바꾸는 데 가장 간편한 도구가 나왔다. **Jina AI Reader**는 어떤 URL이든 앞에 `https://r.jina.ai/`를 붙여 요청하면, 브라우저 렌더링을 거쳐 읽기 좋은 마크다운으로 돌려준다. 기능과 배경은 긱뉴스 소개글과 공식 저장소에서 확인할 수 있다: [Jina AI Reader - URL을 LLM 친화적인 입력으로 바꿔주는 도구 (GeekNews)](https://news.hada.io/topic?id=14498), [GitHub - jina-ai/reader](https://github.com/jina-ai/reader).

## 왜 유용한가

- **입력 품질 향상**: 원문 레이아웃·광고·노이즈를 제거하고 요긴한 본문만 마크다운으로 정제해 에이전트·RAG의 정확도를 높인다.
- **브라우저 이슈 해결**: SPA·동적 로딩·이미지 캡션 등 브라우저 의존 영역을 서버에서 처리해 코드가 단순해진다.
- **무료·오픈소스**: 공개 인프라(`r.jina.ai`, `s.jina.ai`)와 소스 코드가 함께 제공돼 확장/자체 호스팅이 가능하다.

## 핵심 기능 한눈에 보기

- **Read**: `https://r.jina.ai/https://your.url`로 어떤 URL이든 LLM 친화적 마크다운으로 변환
- **Search**: `https://s.jina.ai/your+query`로 웹 검색 결과 상위 5건을 읽고 요약된 형태로 제공
- **이미지 캡션(선택)**: `X-With-Generated-Alt: true`로 이미지에 자동 캡션 주입
- **스트리밍 모드**: `Accept: text/event-stream`으로 점진적 수신, 마지막 청크가 가장 완전함
- **JSON 모드**: `Accept: application/json`으로 단순 JSON 응답
- **요청 헤더 제어**: `x-respond-with`, `x-timeout`, `x-wait-for-selector`, `x-proxy-url`, `x-no-cache` 등 풍부한 옵션
- **SPA 대응**: 해시 라우팅/프리로드 사이트에서 대기 셀렉터·타임아웃으로 메인 콘텐츠 포착

## 빠르게 시작하기

### 단일 URL 읽기

```text
https://r.jina.ai/https://en.wikipedia.org/wiki/Artificial_intelligence
```

### 웹 검색(Top-5 자동 읽기 포함)

```text
https://s.jina.ai/Who%20will%20win%202024%20US%20presidential%20election%3F
```

### 스트리밍/JSON/이미지 캡션 예시(cURL)

```bash
curl -H "Accept: text/event-stream" "https://r.jina.ai/https://example.com"
curl -H "Accept: application/json" "https://r.jina.ai/https://example.com"
curl -H "X-With-Generated-Alt: true" "https://r.jina.ai/https://example.com"
```

### SPA·동적 로딩 페이지 팁

```bash
curl -H "x-timeout: 30" "https://r.jina.ai/https://example.com"
curl -H "x-wait-for-selector: #content" "https://r.jina.ai/https://example.com"
```

## 실전 활용 팁(GeekNews 사례에서 발췌)

- **북마클릿**으로 현재 페이지를 곧장 Reader로 열기:

```javascript
javascript:(function(){window.location.href = "https://r.jina.ai/" + document.URL;})()
```

- macOS **Automator 서비스** 스크립트(우클릭 → 서비스에서 실행):

```applescript
on run {input, parameters}
  try
    set selectedURL to item 1 of input
    set finalURL to "https://r.jina.ai/" & selectedURL
    tell application "System Events"
      open location finalURL
    end tell
  on error errMsg
    display dialog "Error: " & errMsg
  end try
  return input
end run
```

## 언제 쓰면 좋은가

- **에이전트/오토메이션**: 브라우저 제어 없이도 안정적인 본문 추출이 필요할 때
- **RAG 파이프라인**: 크롤링 → 정제 → 임베딩 전처리를 간단히 할 때
- **리서치/요약**: 다수의 기사/문서를 일관된 마크다운으로 받아 비교·요약할 때

## 참고 링크

- 긱뉴스 소개글: [Jina AI Reader - URL을 LLM 친화적인 입력으로 바꿔주는 도구](https://news.hada.io/topic?id=14498)
- 공식 저장소: [GitHub - jina-ai/reader](https://github.com/jina-ai/reader)


