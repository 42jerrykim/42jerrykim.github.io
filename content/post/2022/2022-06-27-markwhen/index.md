---
image: "tmp_wordcloud.png"
categories:
- MarkWhen
date: "2022-06-27T00:00:00Z"
header:
  teaser: /assets/images/undefined/export.png
tags:
- MarkWhen
- Markdown
- 타임라인
- 마크다운
title: '[MarkWhen] MarkWhen - 마크다운으로 계단식 타임라인 만들기'
---

마크다운으로 계단식 타임라인을 만들 수 있는 웹서비스를 소개 한다.

아래의 예시를 살펴 보면 대충 어떤 느낌인지 감이 올것이다.

```markdown
title: Project planning example

#Project1: #d336b1

group Project 1 #Project1
// Supports ISO8601
2022-01/2022-03: Sub task #John
2022-03/2022-06: Sub task 2 #Michelle
More info about sub task 2

2022-07: Yearly planning

group Project 2 #Project2
2022-04/4 months: Larger sub task #Danielle

// Supports American date formats
03/2022 - 1 year: Longer ongoing task #Michelle
10/2022 - 2 months: Holiday season

group Project 3
01/2023: Project kickoff
02/2023-04/2023: Other stuff

section Overall

2022: Year of the something
2023: Year of something else
```

위의 텍스트의 결과물이다.

|![](/assets/images/undefined/export.png)|
|:---:|
|예시|

아래의 사이트에서 확인 해 볼 수 있다.

[https://markwhen.com/](https://markwhen.com/)

## 특징

* 헤더, 이벤트, 그룹, 섹션 으로 구성
* 기간은 마우스로 조정 가능
* Timeline / Map / Doc 보기 지원
* URL 공유 가능
* PDF / PNG 내보내기
* Vue & TypeScript 오픈소스

