---
title: "[Hugo] GitHub Pages에서 301 없이 리디렉션 최적화 - Hugo alias 가이드"
description: "GitHub Pages는 서버단 301/308을 지원하지 않습니다. Hugo aliases와 meta refresh(0s), rel=canonical, robots noindex, noscript 링크를 조합해 검색 노출과 신호를 올바르게 통합하는 설정을 단계별로 안내합니다."
date: "2025-08-29"
lastmod: "2025-08-29"
categories:
- "SEO"
- "Hugo"
tags:
- "SEO"
- "Redirect"
- "301 Redirect"
- "308 Redirect"
- "302 Redirect"
- "307 Redirect"
- "Meta Refresh"
- "Refresh"
- "Hugo"
- "Hugo Aliases"
- "Aliases"
- "GitHub Pages"
- "Canonical"
- "rel=canonical"
- "Robots"
- "noindex"
- "Search Console"
- "Google Search"
- "Indexing"
- "Crawling"
- "Canonicalization"
- "Duplicate URLs"
- "Sitemaps"
- "JavaScript Redirect"
- "Server-side Redirect"
- "Client-side Redirect"
- "Permanent Redirect"
- "Temporary Redirect"
- "HTTP Headers"
- "Static Hosting"
- "Static Site"
- "Jamstack"
- "Cloudflare"
- "Netlify"
- "Vercel"
- "Redirect Rules"
- "Best Practices"
- "Accessibility"
- "noscript"
- "WCAG"
- "Site Move"
- "Migration"
- "HTTP 301"
- "HTTP 308"
- "HTTP 302"
- "HTTP 307"
- "X-Robots-Tag"
- "Robots Meta Tag"
- "hreflang"
- "Consolidation"
- "Signal Consolidation"
- "Canonical Signals"
- "리디렉션"
- "301리디렉션"
- "308리디렉션"
- "임시리디렉션"
- "영구리디렉션"
- "메타리프레시"
- "캐노니컬"
- "표준URL"
- "검색콘솔"
- "구글검색"
- "색인생성"
- "크롤링"
- "중복URL"
- "사이트맵"
- "자바스크립트리디렉션"
- "서버사이드"
- "클라이언트사이드"
- "정적호스팅"
- "정적사이트"
- "베스트프랙티스"
- "접근성"
- "노스크립트"
- "도메인변경"
- "사이트이전"
image: "wordcloud.png"
---

## 요약

- **핵심**: GitHub Pages(`*.github.io`)는 서버단 3xx 헤더(301/308) 설정이 불가합니다. 따라서 Hugo의 `aliases`로 생성되는 **meta refresh(0초) + canonical** 조합이 현실적 대안입니다.
- **추천 설정**: alias 페이지에는 `rel=canonical`을 대상 URL로 지정하고, `robots`에 `noindex,follow`를 적용하며, **noscript 가시 링크**를 제공해 접근성과 크롤링 경로를 보장합니다.
- **효과**: Search Console에서 alias URL이 색인에 남지 않으면서, 신호가 대상 URL로 **강하게 통합**됩니다.

## 배경: 왜 301이 아닌가

- GitHub Pages는 정적 호스팅 특성상 서버 설정(.htaccess/nginx)으로 301/308 헤더를 줄 수 없습니다.
- Google은 3xx가 최선이지만, 불가능한 경우 **meta refresh(0초)**를 **영구 리디렉션 신호**로 해석합니다. canonical과 함께 쓰면 신호가 더 안정적으로 합쳐집니다.

## 구현: Hugo `alias.html` 레이아웃

아래는 현재 사이트의 alias 레이아웃입니다. `rel=canonical`, `meta refresh(0)`, `noscript` 가시 링크를 포함합니다.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>{{ .Permalink }}</title>
    <link rel="canonical" href="{{ .Permalink }}"/>
    <meta charset="utf-8" />
    <meta http-equiv="refresh" content="0; url={{ .Permalink }}" />
  </head>
  <body>
    <noscript>
      <p>
        This page has moved permanently. If you are not redirected automatically, follow this link:
        <a href="{{ .Permalink }}">{{ .Permalink }}</a>
      </p>
    </noscript>
  </body>
</html>
```

## 콘텐츠에 예전 URL 연결하기: Front Matter `aliases`

문서의 앞머리에 과거 경로를 alias로 추가합니다. Hugo가 위 레이아웃을 사용하여 메타 리프레시 페이지를 생성합니다.

```yaml
---
title: "[TV Show] 예시 글"
aliases:
- "/post/old-path-slug/"  # 이전 URL
---
```

## 검증 방법

- 브라우저: 예전 URL 접속 시 즉시 새 URL로 이동하는지 확인합니다.
- 헤더 확인(PowerShell): HTML 메타 리프레시 기반이므로 `-I`로는 200이 보일 수 있습니다. 본문에서 `meta refresh`와 `link rel=canonical`을 점검합니다.

```powershell
irm https://42jerrykim.github.io/post/old-path-slug/ -UseBasicParsing | Select-String -Pattern "http-equiv=\"refresh\"|rel=\"canonical\""
```

## Google 가이드 요약

- **Redirects and Google Search**: meta refresh(0초)는 영구 리디렉션 신호로 해석. 가능하면 서버 측 3xx를 권장.
- **Canonicalization**: 리디렉션과 `rel=canonical`은 함께 사용할 때 표준 URL 판단에 더 강한 신호 제공.
**noindex 주의**: Google은 같은 사이트 내 표준 선택을 막기 위해 noindex를 쓰는 것을 권장하지 않습니다. 대부분의 경우 alias 페이지에도 noindex를 넣지 말고, 리디렉션(또는 meta refresh 0초) + `rel=canonical` 조합만으로 신호를 통합하세요. 꼭 색인 제외가 필요할 때만 신중히 사용하세요.

## 참고 문서

- [Redirects and Google Search (Google Search Central)](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Specify a canonical URL (Google Search Central)](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- [Meta tags Google supports — refresh, robots 등](https://developers.google.com/search/docs/crawling-indexing/special-tags#refresh)

## 마무리

- GitHub Pages 환경에서는 현재 구성이 **Search Console 친화적 최선책**입니다. 향후 서버 측 301/308을 원하면 커스텀 도메인 + Cloudflare(리디렉션 규칙) 또는 Netlify/Vercel 전환을 고려하세요.


