---
image: "wordcloud.png"
slug: mvc-and-mvvm
collection_order: 95
draft: false
title: "[Computer Terms] MVC와 MVVM (Model-View-Controller/ViewModel)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "MVC와 MVVM은 화면과 데이터를 분리하는 공통 목표 아래, Controller와 ViewModel이 각각 다른 방식으로 View와 Model을 중재하는 UI 아키텍처 패턴입니다. 데이터 바인딩의 역할을 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Software-Architecture(소프트웨어아키텍처)
- OOP(객체지향)
- Interface(인터페이스)
- Coupling(결합도)
- Cohesion(응집도)
- Encapsulation(캡슐화)
- Composition(합성)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Maintainability
- Code-Quality(코드품질)
- Modularity
- Readability
- Frontend(프론트엔드)
- Web(웹)
- Observer
---

## 이 장을 읽기 전에

[결합도와 응집도](/post/computerterms/coupling-and-cohesion/)의 낮은 결합도 기준과 [옵저버 패턴](/post/computerterms/observer-pattern/)의 Subject-Observer 구조를 안다고 가정한다. 이 챕터는 그 개념들이 화면(UI) 계층에서 어떻게 구체적인 아키텍처 패턴으로 나타나는지를 다룬다. 난이도는 초급–중급이며, 특정 프레임워크(React, Vue, WPF 등)의 구현 세부사항이나 상태 관리 라이브러리(Redux 등) 비교는 다루지 않는다.

## 화면과 데이터가 뒤섞이면 생기는 문제

버튼 클릭 이벤트 처리 코드 안에 곧바로 데이터 계산 로직과 화면 갱신 코드를 함께 작성하는 방식은 작은 프로그램에서는 문제가 없다. 하지만 같은 데이터를 여러 화면(모바일 앱과 웹 대시보드)에서 보여줘야 하거나, 화면 없이 데이터 로직만 테스트하고 싶을 때 문제가 드러난다. 데이터 계산 로직이 특정 UI 프레임워크의 위젯 객체와 뒤섞여 있으면, 로직만 따로 떼어 재사용하거나 테스트할 수 없다.

**MVC(Model-View-Controller)**와 **MVVM(Model-View-ViewModel)**은 모두 화면(View)과 데이터(Model)를 분리한다는 공통 목표를 가진 UI 아키텍처 패턴이다. **Model**은 데이터와 비즈니스 로직을 담당하고, **View**는 사용자에게 보여지는 화면을 담당한다. 이 둘을 직접 연결하지 않고 중간에 중재자를 두는 것이 두 패턴의 공통점이며, 그 중재자가 무엇을 하는지가 두 패턴의 차이를 만든다.

## MVC: Controller가 입력을 받아 Model과 View를 갱신한다

MVC는 1970년대 후반 트리그브 린스카우그(Trygve Reenskaug)가 스몰토크(Smalltalk) 환경에서 처음 고안한 패턴이다. **Controller**는 사용자의 입력(버튼 클릭, 폼 제출)을 받아 Model을 갱신하고, 그 결과를 반영하도록 View에 명시적으로 지시한다.

```python
# Model: 데이터와 로직만 담당, View나 Controller를 전혀 모른다
class TodoModel:
    def __init__(self):
        self.items: list[str] = []

    def add_item(self, text: str) -> None:
        self.items.append(text)


# View: 화면 출력만 담당
class TodoView:
    def render(self, items: list[str]) -> None:
        print("할 일 목록:")
        for item in items:
            print(f"- {item}")


# Controller: 입력을 받아 Model을 갱신하고, View 갱신을 명시적으로 호출
class TodoController:
    def __init__(self, model: TodoModel, view: TodoView):
        self.model = model
        self.view = view

    def handle_add(self, text: str) -> None:
        self.model.add_item(text)
        self.view.render(self.model.items)  # Controller가 직접 View 갱신을 지시


controller = TodoController(TodoModel(), TodoView())
controller.handle_add("우유 사기")
# 할 일 목록:
# - 우유 사기
```

이 구조에서 Model은 View나 Controller의 존재를 전혀 모른다 — [결합도와 응집도](/post/computerterms/coupling-and-cohesion/)의 낮은 결합도가 유지된다. 다만 `handle_add`에서 보듯, Model이 바뀔 때마다 "View를 어떻게 갱신할지"를 Controller가 명시적인 코드(`self.view.render(...)`)로 지시해야 한다는 점이 핵심이다.

## MVVM: ViewModel과 데이터 바인딩

MVVM은 마이크로소프트가 2005년경 WPF(Windows Presentation Foundation)와 함께 도입한 패턴이다. **ViewModel**은 Model의 데이터를 View가 표시하기 좋은 형태로 가공해 노출하고, View는 이 ViewModel의 상태를 관찰한다. 여기서 핵심 차이가 **데이터 바인딩(Data Binding)**이다 — View는 ViewModel의 속성이 바뀌면 프레임워크가 자동으로 화면을 갱신해주는 구독 관계를 맺는다. 이 구조는 [옵저버 패턴](/post/computerterms/observer-pattern/)의 Subject(ViewModel)-Observer(View) 관계와 본질적으로 같다 — ViewModel이 상태 변화를 통지하면, 구독 중인 View가 자동으로 반응한다.

```python
class TodoViewModel:
    def __init__(self, model: TodoModel):
        self.model = model
        self._observers: list = []  # View가 구독하는 목록 (옵저버 패턴)

    def bind(self, observer) -> None:
        self._observers.append(observer)

    def add_item(self, text: str) -> None:
        self.model.add_item(text)
        for observer in self._observers:
            observer(self.model.items)  # 상태가 바뀌면 구독자에게 자동 통지


# View는 ViewModel의 변화를 구독만 하면 되고, "언제 갱신할지"를 직접 지시하지 않는다
view_model = TodoViewModel(TodoModel())
view_model.bind(lambda items: print("갱신됨:", items))
view_model.add_item("우유 사기")  # 갱신됨: ['우유 사기']
```

MVC의 Controller가 `self.view.render(...)`처럼 View 갱신을 **명령형으로 직접 호출**했던 것과 달리, MVVM에서는 ViewModel이 상태 변화를 통지하기만 하고 View가 그 통지를 구독해 스스로 갱신한다. 실제 프레임워크(WPF, Vue, Android Jetpack)에서는 이 구독·통지 과정을 프레임워크가 자동으로 처리해주므로, 개발자가 "View의 특정 텍스트 필드를 갱신하라"는 코드를 명시적으로 쓸 필요가 없다 — 이것이 데이터 바인딩이 Controller의 명시적 갱신 코드를 줄여주는 방식이다.

## 비교: MVC vs MVVM

| 특성 | MVC | MVVM |
|---|---|---|
| 중재자 | Controller | ViewModel |
| View 갱신 방식 | Controller가 View 메서드를 명령형으로 직접 호출 | View가 ViewModel의 상태 변화를 구독(데이터 바인딩)해 자동 갱신 |
| View와 중재자의 관계 | Controller가 View 구현체를 알아야 함 | ViewModel은 View를 몰라도 됨(상태만 노출) |
| 테스트 용이성 | Controller 테스트 시 View 목 객체 필요할 수 있음 | ViewModel은 View 없이도 상태·로직만 독립적으로 테스트 가능 |
| 대표 사용 사례 | 전통적인 서버 사이드 웹 프레임워크(Ruby on Rails, Django) | 데이터 바인딩을 지원하는 클라이언트 프레임워크(WPF, Vue, Android) |

## 흔한 오개념

**"MVVM이 MVC보다 항상 더 나은 상위 호환이다"** — MVVM의 데이터 바인딩은 프레임워크의 바인딩 엔진이 필요하고, 바인딩 관계가 복잡해지면 "어떤 상태 변화가 어떤 화면 갱신을 유발하는지" 추적하기 어려워질 수 있다. 반면 MVC의 명시적 호출은 코드를 그대로 따라가면 흐름을 파악할 수 있다는 장점이 있다. 어떤 패턴이 더 적합한지는 프레임워크의 바인딩 지원 여부와 팀의 익숙함에 따라 달라진다.

**"Model이 View나 Controller/ViewModel을 알아도 된다"** — 두 패턴 모두 Model이 View나 중재자를 참조하는 것을 금지한다. 위 예시에서 `TodoModel`은 `TodoView`나 `TodoViewModel`을 전혀 import하지 않는다. Model이 View를 알게 되면, 화면 없이 데이터 로직만 테스트하거나 다른 화면에서 재사용하는 것이 불가능해져 두 패턴이 추구하는 분리 목표 자체가 무너진다.

## 다른 개념과의 연결

MVVM의 데이터 바인딩은 [옵저버 패턴](/post/computerterms/observer-pattern/)의 Subject-Observer 구조가 UI 프레임워크 수준에 적용된 구체적인 사례다. 다음 챕터에서는 옵저버 패턴을 클래스 수준을 넘어 서로 다른 서비스 사이의 통신 구조로 확장한 이벤트 드리븐 아키텍처를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. MVC의 Controller와 MVVM의 ViewModel이 각각 View를 어떻게 갱신하는지 그 방식의 차이를 설명할 수 있다. 데이터 바인딩이 옵저버 패턴과 어떤 관계인지 설명할 수 있다. 주어진 코드에서 Model이 View를 직접 참조하는 위반 사례를 찾아낼 수 있다.

## 참고 자료

> Reenskaug, T. (1979). "THING-MODEL-VIEW-EDITOR: an Example from a planningsystem." *Xerox PARC technical note*.

- [Martin Fowler: GUI Architectures](https://martinfowler.com/eaaDev/uiArchs.html) — MVC부터 MVVM까지 UI 아키텍처 패턴의 계보를 정리한 글
- [Microsoft Learn: The MVVM Pattern](https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm) — MVVM과 데이터 바인딩의 실무 적용 문서
