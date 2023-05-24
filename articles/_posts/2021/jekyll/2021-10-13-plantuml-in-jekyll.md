---
title: "[Jekyll] Jekyll에서 Plantuml 사용하기"
categories:
  - Jekyll
  - Plantuml
tags:
  - Jekyll
  - Plantuml
  - markdown
  - diagram
  - Image
header:
  teaser: /plantuml/md-sample-sequence.svg
---

온라인에서 무료로 UML을 그리는 툴 중에서 ![PlantUML](https://plantuml.com/)이라는 사이트가 있다. 해당 사이트에서 다양한 기능을 제공하고 있다. 본 글에서는 GitHub Page에서 PlantUML을 사용 할 수 있는 방법을 알아본다.

# PlantUML

텍스트를 기반으로 UML을 그려주는 툴 중의 하나이다. 온라인에서 바로 UML을 그려 볼 수 있다. VS Code Plugin등 다양한 곳에서 사용할 수 있도록 지원하고 있다.

# Jekyll에서 Plantuml 사용하기

Github Action을 사용하여 Github에서 랜더링을 하거나 Plantuml의 온라인 툴을 사용하여 이미지를 직접 출력하는 두가지 방식이 있다. 둘중에 적합하다고 생각하는 방법을 고민하고 적용해 보도록 한다.

## 1. GitHub Action을 사용하는 방법

[https://github.com/marketplace?query=plantuml](https://github.com/marketplace?query=plantuml) 에서 적용가능한 Action을 확인 할 수 있다. 가장 별점이 높은 [Generate Plantuml](https://github.com/marketplace/actions/generate-plantuml)을 사용해 보았다.

### 적용시 주의점

해당 페이지에 있는 내용을 따라 하면서 살짝 어려웠던 부분은 sample에는 md 파일에서 바로 svg를 생성해 주는 느낌이었지만 별도의 PlantUML 파일을 만들어서 작업해야 해야 동작하는 것을 확인 할 수 있었다.

md-sample-sequence.plantuml 파일을 생성하고 아래의 코드로 내용을 채운다.

```
@startuml
actor Foo1
boundary Foo2
control Foo3
entity Foo4
database Foo5
collections Foo6
Foo1 -> Foo2 : To boundary
Foo1 -> Foo3 : To control
Foo1 -> Foo4 : To entity
Foo1 -> Foo5 : To database
Foo1 -> Foo6 : To collections
@enduml
```

Push가 되면 Github Action이 동작하는 것을 확인 할 수 있다.

![](/assets/images/undefined/120211.png)

파일이 생성되어 추가된 것을 확인할 수 있다.

![](/assets/images/undefined/115850.png)

```markdown
![](/plantuml/md-sample-sequence.svg)
```
위와 같은 코드를 추가하면 다음과 같이 생성된 UML을 사용 할 수 있다.

![](/plantuml/md-sample-sequence.svg)

## 2. 이미지 링크를 삽입하는 방법

PlantUML 에서 링크를 이용한 방법이다.

[PlantUML 온라인](http://www.plantuml.com/plantuml/uml/SyfFKj2rKt3CoKnELR1Io4ZDoSa70000)에 들어가 보면 UML을 실시간으로 확인하고 편집 할 수 있다. 이미 생성되어 있는 링크도 `DecodeURL`를 통해 편집이 가능하다는 장점을 가지고 있다.

### 적용 방법

이것을 md 파일에 아래처럼 이미지 링크를 추가 한다.

``` markdown
![PlantUML model](https://www.plantuml.com/plantuml/png/JSyz3i8m30NWtQVm1HYWFmC3wiG9k82RPAWKR2bn1suFhgdayUMJtekNhjHqVrUWfDBmANA5LNREr3wMRf24jKcrC41XtVI04J8fhTIBfGcIr5gIRiBT7cQmAhmyZXAyuqlmx8qqEFr7eemklXXXSZZd8yrEuI-m5Cw_-xu0)
```

최종적으로 아래의 그림처럼 이미지가 추가된 것을 확인 할 수 있다.

|![PlantUML model](https://www.plantuml.com/plantuml/png/JSyz3i8m30NWtQVm1HYWFmC3wiG9k82RPAWKR2bn1suFhgdayUMJtekNhjHqVrUWfDBmANA5LNREr3wMRf24jKcrC41XtVI04J8fhTIBfGcIr5gIRiBT7cQmAhmyZXAyuqlmx8qqEFr7eemklXXXSZZd8yrEuI-m5Cw_-xu0)|
|:--:|
|PlantUML model|

이미지 주소에서 png만 지우면 다시 편집할 수 있는 장점이 있지만 주소가 바뀌는것을 주의해야 한다.

# 결론

Action을 사용하는것이 나중에 유지보수를 하는 면에 있어서도 더 편할 수 있을것 같다.

|![](/plantuml/md-sample-sequence.svg)|![PlantUML model](https://www.plantuml.com/plantuml/png/JSyz3i8m30NWtQVm1HYWFmC3wiG9k82RPAWKR2bn1suFhgdayUMJtekNhjHqVrUWfDBmANA5LNREr3wMRf24jKcrC41XtVI04J8fhTIBfGcIr5gIRiBT7cQmAhmyZXAyuqlmx8qqEFr7eemklXXXSZZd8yrEuI-m5Cw_-xu0)|
|:--:|:--:|
|GitHub Action을 사용한 결과|이미지 링크를 사용한 결과|

또한, Github Action을 사용한 결과물의 화질이 더 좋은것을 확인 할 수 있다.
