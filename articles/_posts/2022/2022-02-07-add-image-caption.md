---
title: "[Jekyll] 이미지에 캡션 추가하기"
category: [Jekyll, Markdown]
tag:
 - image
 - caption
 - Jekyll
 - Markdown
header:
 teaser: /assets/images/2022/2022-02-09-214658.png
---

이미지를 사용하여 포스팅하는 경우에 이미지에 캡션을 추가하고 싶은 욕구가 막 생길 때가 있다. 이럴 때 사용할 수 있는 방법을 알아보도록 한다. Jekyll을 사용하여 웹사이트를 구성한 경우에는 크게 Markdown만을 사용하여 캡션을 추가하도록 하거나 Jekyll의 기능을 사용하여 추가하는 방법이 있을 것이다.

# figure를 이용한 방법

[Minimal Mistake의 Figure](https://mmistakes.github.io/minimal-mistakes/docs/helpers/#figure)을 사용하여 이미지에 캡션을 추가 할 수 있다.

## 미리 보기

{% include figure image_path="https://uchanlee.dev/static/0a50572e45511d65424f1fe40d68ba13/0a47e/image-1.1.png" alt="this is a placeholder image" caption="그림 1.1 엔지니어링 직원 수의 증가 추이" %}

# image caption을 이용한 방법

```markdown
![그림 1.1 엔지니어링 직원 수의 증가 추이](https://uchanlee.dev/static/0a50572e45511d65424f1fe40d68ba13/0a47e/image-1.1.png)

{:.image-caption}
그림 1.1 엔지니어링 직원 수의 증가 추이
```

```css
.image-caption {
    text-align: center;
    font-size: small;
}

img {
    width: 100%;
}
```
## 미리 보기

![그림 1.1 엔지니어링 직원 수의 증가 추이](https://uchanlee.dev/static/0a50572e45511d65424f1fe40d68ba13/0a47e/image-1.1.png)

{:.image-caption}
그림 1.1 엔지니어링 직원 수의 증가 추이

# Markdown을 최대한 활용한 방법 (최종 적용 방법)

위의 방법들을 사용하는 것도 괜찮은 방법이지만 나의 경우에는 Markdown을 최대한 활용하고 꾸미는 부분만 Jekyll의 도움을 받는 것을 선호하기 때문에 이와 같은 방법을 사용하였다.

표를 사용하여 기본적인틀을 잡고 css를 수정해서 다듬어 보았다.

```markdown
| ![그림 1.1 엔지니어링 직원 수의 증가 추이](https://uchanlee.dev/static/0a50572e45511d65424f1fe40d68ba13/0a47e/image-1.1.png)| 
|:--:| 
| *그림 1.1 엔지니어링 직원 수의 증가 추이* |
```

```css
table {
    display: revert;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
}

img {
    width: 100%;
}
```

## 미리 보기

| ![그림 1.1 엔지니어링 직원 수의 증가 추이](https://uchanlee.dev/static/0a50572e45511d65424f1fe40d68ba13/0a47e/image-1.1.png)| 
|:--:| 
| *그림 1.1 엔지니어링 직원 수의 증가 추이* |

그림을 여러개 넣는 경우에도 깔끔하게 보여줄 수 있다.

| ![그림 1.1 엔지니어링 직원 수의 증가 추이](https://uchanlee.dev/static/0a50572e45511d65424f1fe40d68ba13/0a47e/image-1.1.png) | ![그림 1.1 엔지니어링 직원 수의 증가 추이](https://uchanlee.dev/static/0a50572e45511d65424f1fe40d68ba13/0a47e/image-1.1.png) | 
|:--:|:--:| 
| *그림 1.1 엔지니어링 직원 수의 증가 추이* | *그림 1.1 엔지니어링 직원 수의 증가 추이* |
