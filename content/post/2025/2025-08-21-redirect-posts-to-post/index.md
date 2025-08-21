---
title: "[Hugo] /posts/에서 /post/로 URL 리다이렉트 설정하기"
description: "Hugo에서 posts/ 경로를 post/로 리다이렉트하는 방법을 알아보세요. Alias, 서버 리다이렉트, Netlify 리다이렉트 등 다양한 방법을 소개합니다."
date: "2025-08-21"
lastmod: "2025-08-21"
categories:
- "Hugo"
- "웹 최적화"
- "SEO"
tags:
- "hugo"
- "redirect"
- "alias"
- "url"
- "리다이렉트"
- "301"
- "htaccess"
- "nginx"
- "netlify"
- "정적 사이트"
image: "redirect-guide.png"
---

# Hugo에서 /posts/를 /post/로 리다이렉트 설정하기

Hugo 정적 사이트에서 `http://localhost:12345/posts/` 경로를 `http://localhost:12345/post/`로 리다이렉트하는 방법을 여러 가지로 알아보겠습니다.

## 방법 1: Hugo Alias 사용 (권장)

### 1.1 섹션 페이지에 Alias 설정

`content/post/_index.md` 파일에 aliases를 추가합니다:

```yaml
---
title: "Posts"
type: post
aliases:
  - /posts/
---
```

### 1.2 개별 포스트에 Alias 설정

각 포스트의 프론트매터에 aliases를 추가합니다:

```yaml
---
title: "My Post Title"
date: "2025-08-21"
aliases:
  - /posts/my-post-title
  - /posts/2025/08/21/my-post-title
---
```

## 방법 2: 서버 수준 301 리다이렉트

### 2.1 Apache (.htaccess)

```apache
# Hugo 프로젝트의 public 폴더나 서버 설정에 추가
Redirect 301 /posts/ /post/
RedirectMatch 301 ^/posts/(.*)$ /post/$1
```

### 2.2 Nginx

```nginx
location /posts/ {
    return 301 /post/;
}

location ~ ^/posts/(.*)$ {
    return 301 /post/$1;
}
```

### 2.3 로컬 개발 서버용

Hugo 개발 서버에서는 직접적인 리다이렉트가 어려울 수 있습니다. 대신:

1. Hugo 설정에서 `uglyURLs = true` 사용
2. 또는 `permalinks` 설정을 조정

## 방법 3: Netlify 리다이렉트

Netlify를 사용하는 경우 `public/_redirects` 파일을 생성합니다:

```
/posts/*  /post/:splat  301
/posts/   /post/       301
```

## 방법 4: Hugo 설정에서 URL 구조 변경

`config.toml`에서 URL 구조를 변경할 수 있습니다:

```toml
[permalinks]
  posts = "/post/:year/:month/:day/:title/"
```

## 실제 구현 예시

### Hugo 설정 파일 수정

```toml
# config.toml
baseURL = "http://localhost:12345"
languageCode = "ko-kr"

[permalinks]
  post = "/post/:year/:month/:day/:title/"

# 섹션 설정
[[menu.main]]
  name = "Posts"
  url = "/post/"
  weight = 1
```

### 커스텀 Alias 템플릿 활용

이미 `layouts/alias.html`이 최적화되어 있습니다:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>{{ .Permalink }}</title>
    <link rel="canonical" href="{{ .Permalink }}"/>
    <meta charset="utf-8" />
    <meta http-equiv="refresh" content="0; url={{ .Permalink }}" />
  </head>
</html>
```

## 권장 구현 순서

1. **즉시 적용**: Netlify나 서버 리다이렉트 설정
2. **SEO 대응**: Hugo alias로 canonical URL 설정
3. **장기적 해결**: Hugo 설정에서 URL 구조 표준화

## 테스트 방법

### 1. Hugo 개발 서버에서 테스트

```bash
hugo server -D
```

브라우저에서 다음 URL들을 테스트:
- `http://localhost:12345/posts/` → `http://localhost:12345/post/`로 리다이렉트 확인
- `http://localhost:12345/posts/sample-post` → `http://localhost:12345/post/sample-post`로 리다이렉트 확인

### 2. HTML 소스 확인

리다이렉트 페이지의 HTML에서:
- `link rel="canonical"`이 올바른 URL을 가리키는지 확인
- `meta http-equiv="refresh"`가 올바른 URL로 설정되어 있는지 확인

## 주의사항

1. **대소문자 구분**: `/posts/`와 `/Posts/`는 다른 URL로 인식됩니다
2. **트레일링 슬래시**: `/posts`와 `/posts/`는 다른 URL입니다
3. **301 vs 302**: SEO를 위해서는 301 리다이렉트를 사용하세요
4. **검색 엔진**: Google Search Console에서 리다이렉트가 제대로 작동하는지 모니터링하세요

## 결론

Hugo에서 URL 리다이렉트를 구현하는 가장 좋은 방법은 상황에 따라 다릅니다:

- **빠른 해결**: 서버나 Netlify 리다이렉트
- **Hugo 네이티브**: Alias 기능 활용
- **장기적**: Hugo 설정에서 URL 구조 표준화

현재 프로젝트에서는 이미 최적화된 alias 템플릿이 준비되어 있으므로, 프론트매터에 aliases를 추가하는 방법이 가장 적합합니다.

---

**42jerrykim.github.io에서 더 많은 정보를 확인하세요!**
