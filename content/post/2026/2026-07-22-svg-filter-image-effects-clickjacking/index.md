---
title: "[HTML] SVG 필터로 포토샵 없이 만드는 이미지 이펙트와 클릭재킹 위협"
description: "SVG 필터로 포토샵 없이 이미지 이펙트를 만드는 법을 정리한다. feTurbulence·feDisplacementMap 왜곡, feGaussianBlur·feColorMatrix gooey UI, feBlend 합성을 다루고 SVG 필터를 악용한 클릭재킹 보안 취약점 사례도 함께 소개한다."
date: 2026-07-22
lastmod: 2026-07-22
categories:
  - HTML
  - WebDevelopment
  - Frontend
tags:
  - HTML(HyperText Markup Language)
  - CSS(Cascading Style Sheets)
  - JavaScript
  - Web(웹)
  - Frontend(프론트엔드)
  - Security(보안)
  - Technology(기술)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Animation(애니메이션)
  - Visual-Effects(시각효과)
  - Open-Source(오픈소스)
  - Best-Practices
  - Tips
  - How-To
  - Reference(참고)
  - Beginner
  - Comparison(비교)
  - Implementation(구현)
  - Cheatsheet(치트시트)
  - Innovation(혁신)
  - Productivity(생산성)
  - SVG
  - SVG-Filter
  - feDisplacementMap
  - feTurbulence
  - Clickjacking
  - Liquid-Glass
  - YouTube
draft: true
image: "wordcloud.png"
---

## 들어가며

유튜브 [코딩애플](https://www.youtube.com/watch?v=RrYPBkmnUwc) 채널의 <a href="https://www.youtube.com/watch?v=RrYPBkmnUwc">"진정한 남자는 포토샵 대신 html 쓴다고 함"</a> 영상은 포토샵이나 일러스트레이터 없이 HTML과 SVG만으로 지글거리는 왜곡 효과, 말랑한 gooey UI, 리퀴드 글래스 디자인까지 만들 수 있다는 걸 보여준다. 핵심은 SVG 필터(filter)라는 기능인데, 이름은 낯설지만 원리는 단순하다. 화면에 그려진 픽셀들을 정해진 규칙에 따라 조작하는 것뿐이다. 이 글은 영상에서 다룬 SVG 필터 기법들을 하나씩 정리하고, 영상 마지막에 언급된 SVG 필터 기반 클릭재킹(clickjacking) 취약점 사례도 함께 살펴본다.

## SVG와 필터의 기본 원리

SVG(Scalable Vector Graphics)는 픽셀이 아니라 좌표와 선으로 그림을 표현하는 벡터 그래픽 포맷이다. `<svg>` 태그 안에 `<path>` 같은 태그로 좌표를 나열하면 선이 그려지고, 이 선들이 모여 도형과 그림이 된다. HTML 문서 안에 `<svg>` 태그를 직접 써도 되고, `<img>`나 CSS `background`로 불러와도 된다.

SVG **필터**는 이 SVG 위에 그려진 결과물(또는 SVG로 감싼 HTML 요소)의 픽셀을 규칙에 따라 재가공하는 기능이다. `<filter>` 태그 안에 `feGaussianBlur`, `feColorMatrix`, `feTurbulence` 같은 필터 프리미티브(primitive) 태그를 순서대로 나열하면, 앞 단계의 출력이 다음 단계의 입력으로 이어지는 파이프라인이 만들어진다. 이렇게 정의한 필터는 `filter="url(#필터ID)"` 속성으로 SVG 요소에, 또는 CSS `filter: url(#필터ID)`로 일반 HTML 요소에도 적용할 수 있다. 아래 예시처럼 필터를 만들어 두고 CSS의 `filter` 속성으로 연결하는 방식이 가장 흔하다.

```html
<svg width="0" height="0" style="position:absolute">
  <filter id="myFilter">
    <feGaussianBlur in="SourceGraphic" stdDeviation="0" />
  </filter>
</svg>
<div style="filter:url(#myFilter)">이 안의 내용이 필터를 통과한다</div>
```

`in="SourceGraphic"`은 "원본 화면을 입력으로 받는다"는 뜻이고, 필터 프리미티브마다 `result` 속성으로 중간 결과에 이름을 붙여 다음 단계의 `in`/`in2`로 재사용할 수 있다. 이 체이닝(chaining) 구조 덕분에 인스타그램 필터 같은 색보정부터, 뒤에서 다룰 왜곡·블렌드·마스킹 효과까지 전부 이 하나의 파이프라인 안에서 조합할 수 있다.

## 지글거리는 왜곡 효과: feTurbulence + feDisplacementMap

가장 눈에 띄는 효과는 `feTurbulence`와 `feDisplacementMap`을 조합한 왜곡이다. `feTurbulence`는 [Perlin 노이즈](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feTurbulence) 기반의 랜덤한 잡음 이미지를 생성하는 프리미티브이고, `feDisplacementMap`은 이 노이즈 이미지의 밝기 정보를 기준으로 원본 이미지의 픽셀을 이리저리 밀어내는 프리미티브다. 즉 노이즈 이미지가 밝을수록 그 위치의 픽셀을 더 많이 옮기는 식으로, 밝기 지도(map)를 변위(displacement) 지도로 사용하는 셈이다.

```html
<svg width="300" height="300">
  <filter id="squiggle">
    <feTurbulence type="fractalNoise" baseFrequency="0.1" numOctaves="1" seed="1" result="noise">
      <animate attributeName="seed" values="1;2;3;4;5" dur="0.4s" repeatCount="indefinite" />
    </feTurbulence>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="4" />
  </filter>
  <image href="photo.png" width="240" height="240" filter="url(#squiggle)" />
</svg>
```

`<animate>` 태그로 `seed` 값을 0.4초마다 1씩 바꾸면 노이즈 패턴이 계속 달라지면서 이미지가 미세하게 떨리는 "지글지글" 효과가 만들어진다. 이 기법은 스누피 스타일 낙서 애니메이션이나 손그림 느낌의 텍스트 효과에서 자주 쓰이는데, `scale` 값을 키우면 왜곡 폭이 커지고 `baseFrequency`를 낮추면 노이즈 패턴이 성기고 굵어진다. 같은 원리를 이미지 대신 텍스트나 `<rect>`에 적용하면 아지랑이처럼 흔들리는 배경이나 넘실거리는 물결 효과도 구현할 수 있다. (코드 원본: [codingapple1/svg-filters](https://github.com/codingapple1/svg-filters) 저장소의 `turbulence` 폴더 예제를 참고해 구성했다.)

## 말랑한 gooey UI: feGaussianBlur + feColorMatrix

두 번째로 자주 쓰이는 조합은 UI 디자인에서 흔히 "gooey 효과" 또는 "메타볼(metaball)"이라 불리는 액체 느낌의 UI다. 원리는 다음과 같다. 먼저 서로 다른 두 도형에 각각 `feGaussianBlur`로 흐림 효과를 주고 약간 겹치게 배치한다. 흐려진 두 도형의 경계가 겹치는 부분은 반투명한 회색 그라디언트로 이어지는데, 여기에 `feColorMatrix`로 투명도(alpha) 채널의 대비(contrast)만 극단적으로 높이면 흐릿하게 이어지던 부분이 다시 선명한 하나의 덩어리로 뭉쳐 보인다. 슬라임처럼 서로 들러붙는 것처럼 보이는 이유다.

```html
<svg width="0" height="0" style="position:absolute">
  <filter id="goo">
    <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blurred" />
    <feColorMatrix in="blurred" mode="matrix"
      values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" />
  </filter>
</svg>
```

`feColorMatrix`는 픽셀의 R, G, B, A 값을 5×4 행렬로 곱하고 더하는 프리미티브다. 위 예시의 마지막 행 `0 0 0 18 -7`은 "이 픽셀의 투명도(A)에 18을 곱하고 −7을 더하라"는 뜻이라, 원래 흐릿하게 반투명했던 경계 픽셀들이 투명도 0(완전 투명) 또는 1(완전 불투명)에 가깝게 극단적으로 갈라진다. 그 결과 흐림 효과로 뭉개졌던 경계가 다시 뚜렷한 곡선으로 되살아나면서, 마치 두 방울이 서로 끌어당겨 하나로 합쳐지는 듯한 UI가 만들어진다. 이 기법은 이미지뿐 아니라 문자나 이모지에도 그대로 적용할 수 있어, 버튼을 누르면 글자가 액체처럼 뭉개지며 바뀌는 인터랙션도 구현 가능하다. (코드 원본: [codingapple1/svg-filters](https://github.com/codingapple1/svg-filters) 저장소의 `gooey` 폴더 예제를 참고해 구성했다.)

## 텍스트·레이어 합성: feBlend

`feBlend`는 포토샵의 레이어 블렌드 모드(곱하기, 스크린, 오버레이 등)를 SVG 필터 안에서 그대로 구현하는 프리미티브다. 두 개의 입력(`in`, `in2`)을 지정한 `mode`(예: `multiply`, `screen`, `darken`, `lighten`)로 합성하기 때문에, 별도 이미지 편집 도구 없이도 텍스트 위에 패턴을 곱하거나 두 색상 레이어를 겹치는 디자인을 만들 수 있다. gooey 효과에서 쓴 `feColorMatrix`로 투명도만 조절하는 방식과 달리, `feBlend`는 색상 자체를 합성하기 때문에 텍스트 디자인이나 이미지 합성에 더 어울린다.

## 리퀴드 글래스 디자인: 마스크와 그라디언트

애플이 iOS/macOS 최신 디자인 언어로 선보인 "리퀴드 글래스(Liquid Glass)"도 SVG로 흉내 낼 수 있다. 실제 유리처럼 굴절을 시뮬레이션하는 대신, 다음 요소들을 조합해 눈속임을 만드는 방식이다. 무지개색 `linearGradient`를 하나 만들고, 원본 이미지의 밝기 정보로 만든 마스크용 이미지를 `<mask>`에 연결한 다음, 그 마스크를 씌운 그라디언트 사각형을 `mix-blend-mode: overlay`로 원본 이미지 위에 겹친다.

```html
<svg width="300" height="300">
  <linearGradient id="holoGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#ff5ec4" />
    <stop offset="50%" stop-color="#1e88eb" />
    <stop offset="100%" stop-color="#ff5ec4" />
    <animate attributeName="x1" values="0;2" dur="1.5s" repeatCount="indefinite" />
  </linearGradient>
  <mask id="brightnessMask">
    <image href="subject.png" width="300" height="225" style="filter:brightness(10)" />
  </mask>
  <rect width="300" height="225" fill="url(#holoGrad)" mask="url(#brightnessMask)" style="mix-blend-mode:overlay" />
</svg>
```

`linearGradient`의 `x1` 좌표를 애니메이션으로 계속 움직이면 무지갯빛이 스치듯 흘러가는 홀로그램 느낌이 나고, 여기에 테두리 픽셀만 늘리고 블러를 주는 방식을 더하면 유리 표면이 빛을 굴절시키는 듯한 착시를 만들 수 있다. (코드 원본: [codingapple1/svg-filters](https://github.com/codingapple1/svg-filters) 저장소의 `holo` 폴더 예제를 참고해 구성했다.)

## SVG 필터 vs CSS 필터 vs Canvas·WebGL

같은 이미지 이펙트를 구현하는 방법은 SVG 필터 말고도 여러 가지가 있다. 아래 표로 언제 어떤 방식이 더 적합한지 정리했다.

| 방식 | 픽셀 단위 조작 | 벡터·텍스트에 직접 적용 | 구현 난이도 | 대표 용도 |
| --- | --- | --- | --- | --- |
| SVG 필터 (`feGaussianBlur` 등) | 가능 | 가능(텍스트도 그대로 왜곡·블렌드) | 중간(필터 체이닝 문법 학습 필요) | gooey UI, 왜곡 텍스트, 리퀴드 글래스 |
| CSS `filter`/`backdrop-filter` | 제한적(사전 정의된 함수만) | 불가(래스터화 후 적용) | 낮음 | 단순 블러·그레이스케일·명도 조절 |
| Canvas 2D / WebGL | 완전 자유(픽셀 배열 직접 접근) | 불가(수동 텍스트 렌더링 필요) | 높음(셰이더·픽셀 연산 직접 작성) | 실시간 이미지 처리, 게임 그래픽 |

SVG 필터는 CSS의 정해진 필터 함수보다 훨씬 세밀하게 픽셀을 조작하면서도, Canvas/WebGL처럼 셰이더 코드를 직접 짜지 않아도 된다는 점이 장점이다. 다만 성능 면에서는 GPU 가속을 받는 CSS 필터나 최적화된 WebGL 셰이더보다 느릴 수 있어, 인터랙션이 잦은 대형 UI에는 성능 프로파일링이 필요하다.

## 실전 팁: 자주 하는 실수

1. **`stdDeviation`/`scale` 값을 무작정 키운다**: `feGaussianBlur`의 `stdDeviation`이나 `feDisplacementMap`의 `scale`을 과하게 키우면 필터가 적용되는 영역이 원래 요소의 경계(bounding box)를 벗어나 잘려 보인다. `<filter>` 태그에 `x`, `y`, `width`, `height` 속성으로 필터링 영역을 원본보다 넉넉하게(예: `x="-50%" width="200%"`) 잡아줘야 잘림 없이 렌더링된다.
2. **필터 애니메이션을 남발해 렌더링 비용을 키운다**: `feTurbulence`나 `feGaussianBlur`처럼 계산량이 큰 프리미티브를 `<animate>`로 매 프레임 재계산시키면, 특히 저사양 기기나 모바일 브라우저에서 프레임 드랍이 발생하기 쉽다. 반복 애니메이션이 꼭 필요하지 않다면 정적인 필터로 대체하거나, `will-change: filter` 같은 힌트로 브라우저의 합성 레이어 처리를 유도하는 편이 안전하다.
3. **브라우저별 SVG 필터 지원 차이를 확인하지 않는다**: 대부분의 필터 프리미티브는 최신 Chrome·Firefox·Safari에서 지원되지만, 색공간 처리(`color-interpolation-filters`)나 일부 프리미티브의 렌더링 결과가 브라우저마다 미세하게 다를 수 있다. 프로덕션에 쓰기 전에는 실제 타깃 브라우저에서 시각적으로 확인하는 과정이 필요하다.

## 보안 주의: SVG 필터로 만드는 클릭재킹

SVG 필터는 오래되고 사람들이 잘 안 쓰는 기능이다 보니 최근 보안 연구자들 사이에서 취약점 소재로도 주목받고 있다. 2025년 12월 lyra.horse 블로그에 공개된 ["SVG Filter Clickjacking"](https://lyra.horse/blog/2025/12/svg-clickjacking/) 글은 SVG 필터만으로 교차 출처(cross-origin) iframe 위에 정교한 클릭재킹 공격을 구현한 사례를 다룬다.

핵심 아이디어는 필터가 픽셀 색상을 읽고 조작할 수 있다는 점을 역이용하는 것이다. `feTile`로 특정 픽셀 영역만 잘라낸 뒤 `feComposite`의 산술 연산으로 그 픽셀이 특정 색인지 아닌지를 이진값으로 바꿔 "읽어내고", `feMorphology`·`feBlend`·`feColorMatrix`를 조합해 조건에 따라 화면 일부를 숨기거나 드러내는 알파 매트를 만든다. 여기에 `feBlend`와 `feComposite`를 더 조합하면 NOT, AND, OR, XOR 같은 논리 게이트까지 구현할 수 있어(연구자는 실제로 전가산기 회로와 QR 코드 생성기까지 SVG 필터만으로 만들어 보였다), 상대방 화면의 상태 변화를 실시간으로 감지하며 가짜 UI를 겹쳐 씌우는 다단계 공격이 가능해진다. 연구자는 이 기법으로 Google Docs에서 실제로 악용 가능한 시나리오를 찾아 신고했고, 구글 취약점 보상 프로그램(VRP)에서 3,133.70달러를 지급받았다.

일반적인 SVG `<image>`나 `<foreignObject>`를 이용한 클릭재킹은 이미 잘 알려진 위협이지만, 이 사례가 흥미로운 점은 별도의 스크립트 실행 권한 없이 순수하게 선언적인 필터 프리미티브 조합만으로 "픽셀을 읽고 조건 분기하는" 로직을 구현했다는 데 있다. 사용자 입력을 받는 페이지에 외부 SVG나 필터를 삽입할 수 있게 허용한다면, `Content-Security-Policy`의 `frame-src`/`frame-ancestors` 제한과 별개로 필터 자체의 표현력이 예상보다 넓다는 점을 염두에 둘 필요가 있다.

## 요약

SVG 필터는 `feTurbulence`(노이즈 생성), `feDisplacementMap`(픽셀 재배치), `feGaussianBlur`(흐림), `feColorMatrix`(색상·투명도 행렬 변환), `feBlend`(레이어 합성) 같은 프리미티브를 파이프라인처럼 이어 붙여 포토샵 없이도 왜곡, gooey UI, 리퀴드 글래스 같은 시각 효과를 브라우저 안에서 직접 구현하게 해준다. CSS 필터보다 세밀하고 Canvas/WebGL보다 진입 장벽이 낮다는 점이 매력이지만, 렌더링 비용과 브라우저 호환성은 별도로 확인해야 하고, 같은 픽셀 조작 능력이 클릭재킹 같은 보안 취약점의 소재가 될 수 있다는 점도 함께 알아둘 만하다.

## 참고 자료

- [코딩애플, "진정한 남자는 포토샵 대신 html 쓴다고 함"](https://www.youtube.com/watch?v=RrYPBkmnUwc) — 이 글이 다루는 SVG 필터 기법들을 소개한 원본 영상
- [codingapple1/svg-filters (GitHub)](https://github.com/codingapple1/svg-filters) — 영상에서 사용한 예제 코드 저장소
- [MDN, feTurbulence](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feTurbulence)
- [MDN, feDisplacementMap](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feDisplacementMap)
- [MDN, feGaussianBlur](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feGaussianBlur)
- [MDN, feColorMatrix](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feColorMatrix)
- [MDN, feBlend](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/feBlend)
- [MDN, CSS filter](https://developer.mozilla.org/en-US/docs/Web/CSS/filter)
- [lyra, "SVG Filter Clickjacking" (2025-12-04)](https://lyra.horse/blog/2025/12/svg-clickjacking/) — SVG 필터를 이용한 클릭재킹 취약점과 Google Docs 사례 분석
