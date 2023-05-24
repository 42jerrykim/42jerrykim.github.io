---
title : "[MathJax] Markdown에서 LaTeX로 수식 작성하기"
category:
 - MathJax
tag:
 - LaTeX
 - MathJax
 - Markdown
 - Kramdown
 - Jekyll
 - 수학
 - 수식
 - GitHub Page
 - GitHub
header:
 teaser: /assets/images/2022/2022-02-24-145445.png

---

수학자들이 사용할 것만 같은 화려한 수식이 아니더라도 분수나 제곱근과 같이 수식으로 표현해야 좋은 내용이 있다. 본 게시글에서는 여러분의 웹 페이지에 [MathJax](https://www.mathjax.org/)를 사용하여 수식을 표시하는 방법에 대해서 알아볼 것이다.

# MathJax? Latex?

| ![](/assets/images/2022/2022-02-24-145445.png) |
|:--:|
|MathJax를 사용하여 수식을 보기 좋게 표시 할 수 있다.|

문서를 표현할 때 문자와 그림 등의 요소를 조합하여 표시 할 수 있는 [LaTeX](https://www.latex-project.org/)(LaTeX은 레이텍 또는 라텍이라고 읽는다.)라는 시스템이 있다. LaTeX을 이용하면 수식이 삽입된 문서를 아름답게 표시할 수 있어서, 주로 수리과학을 기반으로 하는 분야의 논문을 작성할 때 LaTeX이 사용된다.

[MathJax](https://www.mathjax.org/)는 오픈소스로 LaTeX, MathML, 그리고 AsciiMath 표기법을 사용한 수식을 표시해주는 JavaScript 엔진이다. Markdown으로 작성된 텍스트를 Jekyll을 통하여 웹페이지로 표시하는 것과 비슷하게 수식을 LaTex 표기법으로 작성하면 웹페이지에 수식을 표시할 수 있도록 구현한 시스템이다.

자세한 내용은 [MathJax Documentation](http://docs.mathjax.org/en/latest/)을 참고하자.

|타입|표기법|표시해줄 수 있는 엔진|
|:--:|:--:|:--:|
|게시글|Markdown, Kramdown, ... |GitHub, Jekyll, ...|
|수식|LaTeX, MathML, AsciiMath, ...|MathJax, ...|

표기법에 따라서 원하는 내용을 작성하고, 적절한 엔진을 선택해서 아름답게 표시 할 수 있다.

# MathJax 적용 방법 

[MathJax.org](https://www.mathjax.org/)의 [Getting Started](https://www.mathjax.org/#docs) 페이지에서 제공하는 설명대로 다음의 코드를 자신의 웹 페이지에 추가하면 된다.


| ![설치 방법](/assets/images/2022/2022-02-24-144643.png) |
|:--:|
| *설치 방법* |

나는 Web Integration을 사용하여 MathJax를 적용하였다.

## MathJax 적용 방법 - Web Integration

```js
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

위의 코드를 `<head> </head>`사이에 기입한다.

코드만 추가하면 끝이다. 엄청 간단하다.

# 수식 작성하기

앞서 코드를 적용하고 나면 해당 웹 페이지에 있는 텍스트 중, `$$`로 좌우가 감싸진 문자열은 LaTeX 문법으로 인식하여 수식으로 변환해준다.

```latex
$$( a^2 )$$
```
위의 코드를 게시글에 추가하면 아래와 같은 수식이 표시되는것을 확인할 수 있다.

$$( a^2 )$$

```latex
$( a^2 )$
```

# LaTex 문법

[Typesetting mathematics](https://www.latex-project.org/help/documentation/#typesetting-complex-mathematics)에서 LaTeX의 여러 문법중 수식과 관련된 내용을 확인 할 수 있다.

## 이차방정식의 근의 공식

```latex
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}$$
```

$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}$$

## 첨자

```latex
$$a_1, a^2, a_1^2$$
$$y_i=x_i^3+x_{i-1}^2+x_{i-2}$$
```

$$a_1, a^2, a_1^2$$

$$y_i=x_i^3+x_{i-1}^2+x_{i-2}$$

## 분수

분수 표기법에는 두 가지 방법이 있습니다.

1. `\over`를 사용하면 \over를 기준으로 왼쪽에 있는 수식은 모두 분자, 오른쪽에 있는 수식은 모두 분모로 들어가게 됩니다.
1. `\frac`을 사용하게 되면 첫 번째 문자는 분자, 두 번째 문자는 분모로 들어가게 됩니다. 두 문자 이상이라면 중괄호{ }를 통하여 묶어주면 됩니다.

```latex
$$s^2+2s+s\over s+\sqrt s+1$$
$$\frac{1+s}{s(s+2)}$$
```

$$s^2+2s+s\over s+\sqrt s+1$$

$$\frac{1+s}{s(s+2)}$$

## 절대값 표기법

일반적으로 절대값을 표기할 때는 키보드 위의 | 문자를 사용하게 됩니다.
하지만 이렇게 하면 분수와 같이 큰 객체에 맞게 resizable한 기호를 사용할 수 없습니다.
그럴 땐 `\vert`와 `\left`, `\right`를 통하여 좌우 기호를 명시해주면 됩니다.

```latex
$$\vert x \vert$$
$$\left\lvert \frac{s^2+1}{s^3+2s^2+3s+1} \right\rvert$$
```

$$\vert x \vert$$

$$\left\lvert \frac{s^2+1}{s^3+2s^2+3s+1} \right\rvert$$

# Cheat Sheet

매번 문법에 관련된 문서를 보고 작성하는것은 어려우니 [Cheat Sheet](https://drive.google.com/file/d/1dEEAXMhHo9TgmZmXSNWSVlG6YOeWp_gj/view)를 보는것도 괜찮은 방법이다.

# 참고

* [The Latex Project](https://www.latex-project.org/)
* [MathJax Documentation](http://docs.mathjax.org/en/latest/)
* [MathJax로 LaTeX 사용하기](https://johngrib.github.io/wiki/mathjax-latex/)
* [MathJax로 수식 입력하는 방법](https://sasamath.com/blog/tip-collection/how-to-write-equations-in-mathjax/)
* [[LaTex] Markdown 수식 작성법](https://velog.io/@d2h10s/LaTex-Markdown-%EC%88%98%EC%8B%9D-%EC%9E%91%EC%84%B1%EB%B2%95)