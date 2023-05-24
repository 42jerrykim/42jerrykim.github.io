---
title: "[Jekyll] 코드 카피 버튼 만들기"
category: [Jekyll, Markdown]
tag:
 - Code
 - Copy
 - Jekyll
 - Markdown
header:
 teaser: /assets/images/2022/2022-02-28-150429.png
---

아래의 그림처럼 개발 블로그에서는 코드 복사를 위한 Copy 버튼이 있는 것을 종종 확인 할 수 있다. Java Script를 이용하여 콘텐츠의 내용을 바꾸지 않고 Copy 버튼을 삽입 할 수 있는 방법에 대해서 알아본다.

|![코드 카피 버튼](/assets/images/2022/2022-02-28-150429.png)| 
|:--:| 
| 코드 카피 버튼 |


# 적용 코드

성격이 급한 사람들을 위한 코드이다.

```html
<script>
  var codeBlocks = document.querySelectorAll('pre.highlight');
  
  codeBlocks.forEach(function (codeBlock) {
    var copyButton = document.createElement('button');
    copyButton.className = 'copy btn'; // btn은 minimal mistake에서 지원하는 버튼을 사용하기 위해 추가 하였다.
    copyButton.type = 'button';
    copyButton.ariaLabel = 'Copy code to clipboard';
    copyButton.innerText = 'Copy';
  
    codeBlock.append(copyButton);
  
    copyButton.addEventListener('click', function () {
      var code = codeBlock.querySelector('.rouge-code').innerText.trim();
      window.navigator.clipboard.writeText(code);
  
      copyButton.innerText = 'Copied';
      
      var fourSeconds = 4000;
      setTimeout(function () {
        copyButton.innerText = 'Copy';
      }, fourSeconds);
    });
  });
</script>
```

위의 코드를 게시글을 표시하는데 필요한 html에 추가한다. 본 블로그에서는 `page__date.html`에 추가하였다. 아니면 `single.html`에 추가하는 방법도 있을 것이다.

```css
pre.highlight {
    .copy {
        color: $text-color;
        position: absolute;
        right: 1rem;
        top: 1rem;
        opacity: 20%;
        background:  $primary-color;
    }

    &:active .copy,
    &:focus .copy,
    &:hover .copy {
      opacity: 1;
    }
}
```

버튼을 이쁘게 보이기 위한 css이다. main.scss에 추가한다.

[GitHub Commit](https://github.com/Reevid/Reevid.github.io/commit/4173b700ae7252bfb5d10860295d888bdaf023d6)을 참조 하는것도 괜찮은 방법이다.

# 결론

다른 방법도 있겠지만 Markdown으로 작성된 글을 다른곳에서도 사용 할수 있도록 하기 위해서 JS를 이용하여 처리 하였다.

# 참고

* [Jekyll: Copy code to clipboard](https://remarkablemark.org/blog/2021/06/01/add-copy-code-to-clipboard-button-to-jeyll-site/)
* [jekyll-clipboardjs](https://github.com/marcoaugustoandrade/jekyll-clipboardjs)
* [How to Add a Copy-to-Clipboard Button to Jekyll](https://www.aleksandrhovhannisyan.com/blog/how-to-add-a-copy-to-clipboard-button-to-your-jekyll-blog/)