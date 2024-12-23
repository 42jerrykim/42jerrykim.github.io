---
image: "tmp_wordcloud.png"
categories: Git
date: "2021-04-07T00:00:00Z"
tags:
- Git
- stage
- KakaoTalk
title: '[Git] git 수정 이전으로 내용 되돌리기'
---

Git에서 수정한 내용들을 되돌리고 싶을때 사용할 수 있는 방법이다.

## 모든 변경 파일 되돌리기

stage 에 들어가지 않은 수정한 파일들을 수정 이전으로 되돌리기.

> 모든 수정 사항을 버리므로 주의

```
git reset --hard
```

## 특정 파일만 되돌리기

`git checkout –  filename` 형식으로 `filename` 에 되돌릴 파일의 경로 입력. 아래는 `src/hello.c` 의 변경을 취소하는 경우

```
git checkout -- src/hello.c
```