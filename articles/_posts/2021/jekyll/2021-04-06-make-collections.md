---
title: "[Jekyll] 모아 볼 수 있는 콜렉션 만들기"
categories:
  - Jekyll
tags:
  - Jekyll
  - Category
  - Posts
  - _config.yml
---

포스팅만을 이용해서 글을 작성하는것은 블로거로써 충분한 일이지만 종류별로 세분화 할 수 있는 글을 모아두기에는 적절하지 않은것 같아서 아래와 같이 콜렉션 별로 글을 볼 수 있도록 추가 하였다.

# 장점
* 기존의 카테고리는 모든글을 표시하지만 콜렉션은 몇몇개의 글만 선정해서 표시하는것이 가능하다.

![Image Alt 텍스트](/assets/images/jekyll/1.png)

단점은 Posts에 있는 글은 Collections에서 볼 수 있지만 Collection으로 지정된 글은 Posts에서 볼 수 있는 방법은 아직 찾지 못했다.

# 적용 방법

## 링크 만들기

우선 메인 페이지에서 볼 수 있는 링크를 만들어야 한다. 링그는 _data/navigation.yml에 아래처럼 collections을 추가 한다.
```
main:
  - title: "Posts"
    url: /posts/
  - title: "Categories"
    url: /categories/
  - title: "Tags"
    url: /tags/
  - title: "Collections"
    url: /collections/
  - title: "About"
    url: /about/
```

## Collections 페이지 만들기
Collections 내용의 레이아웃을 잡기 위해서 _pages에 collection-archive.html을 추가한다. 내용은 아래와 같다.

{% gist 3ff61cafb5a9b285bef00fc12092b21f %}

## Collections에 표시되는 글 작성하기
작성된 글이 표시되기 위해서는 아래의 3가지 작업이 필요하다.

1. 별도의 폴더에 글 작성하기
1. _configure.xml에 default:에 내용 추가 하기
1. _configure.xml에 collections:에 내용 추가 하기

3가지 중에 하나라도 되지 않는다면 내용이 표시 되지 않는다.

### 1. 별도의 폴더에 글 작성하기

![Image Alt 텍스트](/assets/images/jekyll/2.png)

그림처럼 최상위 레벨에 _algorithm이라는 폴더를 생성하고 bubblesort.md 글을 하나 넣는다. Posts에 표시되는 글 처럼 날짜를 표시할 필요는 없다.

bubblesort.md의 내용은 아래와 같이 채운다.
```
---
title: "Bubble Sort"
---

게시물을 내용을 작성한다.

```
title만 있어도 잘 동작한다.

### 2. _configure.xml에 default:에 내용 추가 하기

{% gist e2f763e399b19830c19c4266df17fef8 %}

각 post별로 목차를 보여주기 위해서 ```toc```관련된 내용이 추가되어 있다.

### 3. _configure.xml에 collections:에 내용 추가 하기

{% gist c21893cc7ef9fb248d3e290cbaac400e %}

```Title:```에 적혀 있는 내용이 Collections 페이지 에서 표시되는 머릿글로 사용된다.

# 총평
카테고리별로 게시글을 모아서 보여주는 페이지도 있으니 콜렉션은 다시 찾아 볼만한 글들만 정리해서 보여주는 개념으로 사용하면 좋을것 같다.