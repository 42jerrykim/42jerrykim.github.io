---
title: "[Minimal Mistakes] Minimal Mistakes 페이지 넓게 보기"
category: [Minimal Mistakes, Jekyll]
tag:
 - Jekyll
 - Minimal Mistakes
 - Theme
header:
 teaser: /assets/images/2022/2022-02-09-214522.png
---

[Minimal Mistakes Jekyll theme](https://github.com/mmistakes/minimal-mistakes)을 사용하여 Gibhub 페이지를 구성한 경우에는 최대 너비가 지정되어 있어 일정 크기 이상으로 넓어지지 않는다. [Sample Post](https://mmistakes.github.io/minimal-mistakes/year-archive/)에서 [Minimal Mistakes Jekyll theme](https://github.com/mmistakes/minimal-mistakes)가 어떻게 동작하는지 확인 할 수 있다. 이런 경우에 더 넓은 페이지를 구성하고 싶은 사람들을 위한 가이드이다. 

# 적용 방법
## 1. main.scss 추가 하기
[Customizing](https://mmistakes.github.io/minimal-mistakes/docs/stylesheets/#customizing)의 내용 중에서 2번을 참고하여 assets/css/main.scss 파일을 생성하고 아래의 내용으로 main.scss를 채운다.

```scss
---
# Only the main Sass file needs front matter (the dashes are enough)
---

@charset "utf-8";

@import "minimal-mistakes/skins/{{ site.minimal_mistakes_skin | default: 'default' }}"; // skin
@import "minimal-mistakes"; // main partials
```
## 2. 최대 넓이 확장하기

추가된 main.scss에 아래의 내용을 추가하면 웹사이트의 최대 너비 제한이 풀린다.

```scss
$max-width: 100%;
```

다만 주의해야 되는 것은 main.scss에 아무 위치에 ```$max-width: 100%;```를 추가하면 안 된다. 아래의 코드처럼 ```$max-width: 100%;```을 ```@import```가 시작하기 전에 작성한다.

```scss
---
# Only the main Sass file needs front matter (the dashes are enough)
---

@charset "utf-8";

$max-width: 100%;

@import "minimal-mistakes/skins/{{ site.minimal_mistakes_skin | default: 'default' }}"; // skin
@import "minimal-mistakes"; // main partials
```

## 3. breadcrumbs 정렬 오류 수정하기

[Breadcrumbs (beta)](https://mmistakes.github.io/minimal-mistakes/docs/navigation/#breadcrumbs-beta)를 설정한경우 최대 너비가 달라지는것에 대응을 못하는것을 확인 할 수 있을것이다.

우리는 main.scss에서 커스터마이징을 할 수 있다는 것을 알고 있기 때문에 main.scss에 아래와 같은 내용을 추가하여 대응 한다.

```css
.breadcrumbs {
    @include clearfix;
    margin: 0 auto;
    max-width: 100%;
    padding-left: 1em;
    padding-right: 1em;
    font-family: $sans-serif;
    -webkit-animation: $intro-transition;
    animation: $intro-transition;
    -webkit-animation-delay: 0.3s;
    animation-delay: 0.3s;

    @include breakpoint($x-large) {
        max-width: $max-width;
    }

    ol {
        padding: 0;
        list-style: none;
        font-size: $type-size-6;

        @include breakpoint($large) {
        float: right;
        width: calc(100% - #{$right-sidebar-width-narrow});
        }

        @include breakpoint($x-large) {
        width: calc(100% - #{$right-sidebar-width});
        }
    }

    li {
        display: inline;
    }

    .current {
        font-weight: bold;
    }
}
```

```@import```의 아래쪽에 선언한다.

# 최종 코드

```scss
---
# Only the main Sass file needs front matter (the dashes are enough)
---

@charset "utf-8";

$max-width: 100%;

@import "minimal-mistakes/skins/{{ site.minimal_mistakes_skin | default: 'default' }}"; // skin
@import "minimal-mistakes"; // main partials

.breadcrumbs {
    @include clearfix;
    margin: 0 auto;
    max-width: 100%;
    padding-left: 1em;
    padding-right: 1em;
    font-family: $sans-serif;
    -webkit-animation: $intro-transition;
    animation: $intro-transition;
    -webkit-animation-delay: 0.3s;
    animation-delay: 0.3s;

    @include breakpoint($x-large) {
        max-width: $max-width;
    }

    ol {
        padding: 0;
        list-style: none;
        font-size: $type-size-6;

        @include breakpoint($large) {
        float: right;
        width: calc(100% - #{$right-sidebar-width-narrow});
        }

        @include breakpoint($x-large) {
        width: calc(100% - #{$right-sidebar-width});
        }
    }

    li {
        display: inline;
    }

    .current {
        font-weight: bold;
    }
}
```

위와같이 적용하면 본 웹사이트 처럼 와이드한 페이지가 잘 나오는것을 확인 할 수 있을것이다.
