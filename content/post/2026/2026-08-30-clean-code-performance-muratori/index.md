---
title: "[Programming] \"클린 코드\"는 성능을 얼마나 깎아내리는가 — 25배 벤치마크의 반박"
description: "Pragmatic Engineer의 2026년 8월 인터뷰를 계기로, Casey Muratori가 2023년 실측 벤치마크로 보여준 클린 코드와 성능의 관계를 정리한다. 가상 함수 기반 다형성을 switch문·룩업 테이블로 바꾸면 왜 최대 25배 빨라지는지, Uncle Bob의 반박까지 함께 다룬다."
date: 2026-08-30
lastmod: 2026-08-30
draft: false
categories:
  - Programming
  - Performance
tags:
  - Performance(성능)
  - Optimization(최적화)
  - Clean-Code(클린코드)
  - Refactoring(리팩토링)
  - Code-Quality(코드품질)
  - Readability
  - Maintainability
  - Best-Practices
  - Profiling(프로파일링)
  - Benchmark
  - OOP(객체지향)
  - Polymorphism(다형성)
  - Abstraction(추상화)
  - Software-Architecture(소프트웨어아키텍처)
  - C++
  - Cache
  - CPU(Central Processing Unit)
  - Compiler(컴파일러)
  - Memory(메모리)
  - Debugging(디버깅)
  - Testing(테스트)
  - Implementation(구현)
  - Type-Safety
  - Modularity
  - Design-Pattern(디자인패턴)
  - Coupling(결합도)
  - Interface(인터페이스)
  - Case-Study
  - Deep-Dive
  - Comparison(비교)
  - Assembly
image: "wordcloud.png"
---

"섣부른 최적화는 만악의 근원"이라는 말은 성능을 나중에 걱정해도 된다는 면죄부로 자주 인용된다. Handmade Hero와 *Computer, Enhance!*로 알려진 프로그래머 Casey Muratori는 이 통념에 정반대로 답한다 — 성능은 코드를 다 짜고 나서 프로파일러로 튜닝할 문제가 아니라, 설계 단계에서 이미 결정되는 문제라는 것이다. 2026년 8월 26일 The Pragmatic Engineer(Gergely Orosz)가 이 주장을 다시 조명하는 인터뷰 정리글을 공개했지만, Muratori 자신의 진짜 증거는 3년 전인 2023년에 이미 사이클 단위로 측정되어 있었다. 이 글은 그 실측 수치와 논증 구조, 그리고 *Clean Code*의 저자 Robert C. Martin("Uncle Bob")이 내놓은 반박까지 함께 정리한다.

## 무슨 일이 있었나

The Pragmatic Engineer는 [Muratori와의 논의를 정리한 글](https://newsletter.pragmaticengineer.com/p/why-performant-code-matters-but-gets)에서, 그가 업계 전반에 던진 질문을 첫 문장으로 소개한다. "Why does the industry zeitgeist place so little emphasis on software performance when there seems to be overwhelming evidence that performance is critical to their bottom line?"(성능이 수익에 결정적이라는 증거가 이렇게 쌓여 있는데, 업계 전반의 정서는 왜 이렇게 성능에 무관심한가) 라는 물음이다. Muratori가 좋은 최적화자와 평범한 최적화자를 가르는 기준으로 제시한 것은 접근 순서다 — 평범한 최적화자는 이미 짜인 코드를 프로파일러로 찍어 병목을 하나씩 없애 나가지만, 뛰어난 최적화자는 먼저 하드웨어가 이론적으로 낼 수 있는 처리량이 얼마인지부터 계산해 두고, 실측치가 그 상한에 가까워질 때까지 멈추지 않는다. 그는 엔지니어가 최소한 20–30개의 기본 어셈블리 명령어와 CPU의 핵심 개념 세 가지(데이터 이동/캐시, 분기 예측, 실행 유닛 스케줄링)를 이해해야 "성능이 중요하다"고 말할 자격이 있다고 주장하며, 실제로 성능을 앞세워 시장 점유율을 늘린 사례로 파일 탐색기 File Pilot과 비디오 편집기 Blackmagic Blick을 든다. 테스트 주도 개발에 대해서도 그는 "Tests should be a cost/benefit decision, and not put in place by default"(테스트는 비용 대비 이득으로 판단할 문제이지, 기본값으로 깔아 두는 게 아니다)라며 프로젝트에 따라 사전 테스트가 오히려 나쁜 선택일 수 있다고 말한다.

## 2023년의 증거: 사이클 단위로 잰 클린 코드의 비용

인터뷰가 다시 불러온 것은 사실 새 주장이 아니다. Muratori는 2023년 2월 28일 자신의 블로그 *Computer, Enhance!*에 [<strong>"Clean" Code, Horrible Performance</strong>](https://www.computerenhance.com/p/clean-code-horrible-performance)라는 글을 올렸고, 여기서 실제 C++ 코드를 사이클 단위로 측정해 수치를 남겼다. 실험은 여러 도형의 넓이를 합산하는 흔한 예제에서 출발한다. 가상 함수를 이용한 다형성 — 각 도형 클래스가 `Area()`를 오버라이드하고, 호출부는 기반 클래스 포인터로 순회하며 호출하는 전형적인 "클린 코드" 구조 — 를 기준선으로 두고, 이를 단계적으로 걷어낼 때마다 처리 속도가 어떻게 바뀌는지 콜드 상태와 워밍 상태 모두에서 반복 측정했다.

| 단계 | 구조 | 넓이 1회 계산당 사이클 | 기준 대비 배수 |
|------|------|----------------------|----------------|
| 기준선 | 가상 함수 기반 다형성 | 약 35 사이클 | 1배 |
| 1단계 | 열거형 태그 + switch문 분기 | 약 24 사이클 | 약 1.5배 |
| 2단계 | 함수 포인터 대신 룩업 테이블 | 약 3.0–3.5 사이클 | 약 10배 |
| 3단계 | 여러 속성을 한 구조체에 묶어 재설계 | 측정치 비공개 | 약 15배 |
| 4단계 | AVX 명령어로 벡터화 | 측정치 비공개 | 약 20–25배 |

가상 함수 호출 한 번은 겉보기엔 함수 호출 하나지만, 실제로는 객체가 가리키는 **vtable**(가상 함수 테이블)을 메모리에서 읽고, 그 안에서 해당 함수의 주소를 다시 읽어 그 주소로 간접 점프하는 과정이다. 이 두 번의 메모리 접근이 캐시에 없으면 그대로 캐시 미스가 되고, 점프할 함수 주소가 매 반복마다 달라지면 CPU의 분기 예측기가 다음에 어떤 코드를 미리 읽어 둘지 예측하지 못해 파이프라인이 자주 비게 된다. Muratori는 이 실험 결과를 두고 클린 코드 원칙 중 처음 몇 가지 — 특히 다형성으로 분기를 감추라는 원칙 — 가 최근 십수 년간 쌓인 캐시 계층·분기 예측기 발전을 사실상 무효로 만든다고 결론짓는다.

## 왜 구조를 바꾸면 이렇게 차이가 나는가

아래는 위 표의 기준선(가상 함수)과 1단계(switch문) 차이를 보여주는 최소 예제다. 정확한 벤치마크 코드는 원문을 참고해야 하지만, 두 접근이 컴파일러와 CPU에 어떤 정보를 주는지는 이 정도 코드로도 충분히 드러난다.

```cpp
// 가상 함수 기반 다형성 — 호출부는 실제 타입을 몰라도 되지만,
// 매 호출마다 vtable을 거쳐 함수 주소를 간접적으로 읽어야 한다.
#include <vector>
#include <memory>

struct Shape {
    virtual double Area() const = 0;
    virtual ~Shape() = default;
};

struct Circle : Shape {
    double radius;
    double Area() const override { return 3.14159265 * radius * radius; }
};

struct Rectangle : Shape {
    double width, height;
    double Area() const override { return width * height; }
};

double TotalArea(const std::vector<std::unique_ptr<Shape>>& shapes) {
    double total = 0.0;
    for (const auto& shape : shapes) {
        total += shape->Area();  // vtable 조회 → 함수 포인터로 간접 점프
    }
    return total;
}
```

```cpp
// 태그드 유니온 + switch문 — 호출부가 타입을 알아야 하는 대신,
// 분기 대상이 컴파일 타임에 고정되어 컴파일러가 인라이닝하기 쉽다.
#include <vector>

enum class ShapeKind { Circle, Rectangle };

struct ShapeData {
    ShapeKind kind;
    union {
        struct { double radius; } circle;
        struct { double width, height; } rectangle;
    };
};

double TotalArea(const std::vector<ShapeData>& shapes) {
    double total = 0.0;
    for (const auto& shape : shapes) {
        switch (shape.kind) {
            case ShapeKind::Circle:
                total += 3.14159265 * shape.circle.radius * shape.circle.radius;
                break;
            case ShapeKind::Rectangle:
                total += shape.rectangle.width * shape.rectangle.height;
                break;
        }
    }
    return total;
}
```

첫 번째 버전은 `Shape*` 하나로 어떤 도형이든 다룰 수 있다는 유연성을 얻는 대신, 도형이 늘어날수록 vtable도 흩어져 캐시 지역성이 나빠진다. 두 번째 버전은 호출부가 `ShapeKind`를 알아야 한다는 유연성의 손실을 감수하는 대신, 데이터가 배열 하나에 연속으로 붙어 있어 캐시 라인을 낭비 없이 채우고 컴파일러가 `switch`를 점프 테이블로 컴파일해 분기 예측 부담도 줄인다. Muratori의 2단계(룩업 테이블)는 여기서 한 걸음 더 나아가 `switch`조차 없애고 도형 종류를 배열 인덱스로 직접 사용하는데, 이 지점부터 처리 속도가 완만한 개선(1.5배)에서 수직 상승(10배)으로 바뀐다는 것이 이 실험의 핵심 관찰이다.

## 프로파일러는 왜 이 격차를 못 찾는가

Muratori가 인터뷰에서 강조하는 논지는 이 격차가 프로파일러를 더 많이 돌린다고 좁혀지지 않는다는 것이다. 프로파일러는 지금 존재하는 코드 구조 안에서 가장 느린 지점을 찾아줄 뿐이므로, 그 구조 자체가 상한을 낮게 잡아 둔 경우에는 아무리 정밀하게 측정해도 **지역 최적해(local minimum)** 밖으로 나갈 수 없다. 위 예제로 말하면, 가상 함수 버전을 프로파일링해서 얻을 수 있는 최선은 vtable 조회 자체를 없애지 않는 한 35 사이클 근방의 어딘가일 뿐, 애초에 3 사이클대라는 상한이 존재한다는 사실은 프로파일러가 알려주지 않는다. 그래서 그는 좋은 최적화자의 습관을 "하드웨어가 낼 수 있는 이론적 처리량을 먼저 계산해 두고, 실측치와 그 상한 사이의 격차를 좁혀 가는 것"이라고 정의한다 — 이는 앞서 이 블로그에서 다룬 [Napkin Math](/post/2026-08-04-napkin-math-performance-estimation/)의 방법론과 같은 방향이다.

## "섣부른 최적화"라는 핑계

Donald Knuth의 "premature optimization is the root of all evil"은 원래 함수 하나 안에서 97%의 코드는 손대지 말고 나머지 3%의 핫스팟에만 집중하라는, 마이크로 최적화에 대한 경고였다. Muratori가 문제 삼는 것은 이 문장이 아키텍처 수준의 결정 — 클래스 계층을 가상 함수로 짤지, 데이터를 어떻게 배치할지 — 까지 "나중에 생각해도 된다"는 핑계로 확장되어 쓰인다는 점이다. 그는 <strong>"Architect your system to be performant, or you'll have trouble solving problems without a rewrite"</strong>(성능을 고려해 시스템을 설계하라, 그러지 않으면 나중에 다시 쓰지 않고는 문제를 풀 수 없게 된다)라고 말하는데, 이는 성능이 나쁜 아키텍처는 배포 후에 프로파일러로 고칠 수 있는 수준을 넘어 구조 자체를 갈아엎어야만 고쳐진다는 뜻이다. 그는 이런 검증되지 않은 통념을 두고 <strong>"I find there's a lot of received programming wisdom that's just nonsense. Clearly, no one's ever tested it."</strong>(검증된 적 없는 프로그래밍 통념이 너무 많다. 아무도 실제로 테스트해 본 적이 없는 게 분명하다)라고 잘라 말한다.

## Uncle Bob의 반박: 성능은 유일한 목표가 아니다

Muratori의 2023년 글은 곧바로 *Clean Code*의 저자 Robert C. Martin("Uncle Bob")과의 공개 논쟁으로 이어졌고, 그 기록은 지금도 [GitHub 저장소 unclebob/cmuratori-discussion](https://github.com/unclebob/cmuratori-discussion)에 남아 있다. Martin은 Muratori가 측정한 성능 격차 자체를 부정하지 않는다. 대신 자신의 우선순위가 애초에 다르다는 점을 분명히 한다. 그는 <strong>"I never suggested that performance was my main goal. I want the act of programming to be easier, more pleasant, and more productive"</strong>(나는 성능이 내 주된 목표라고 말한 적이 없다. 나는 프로그래밍이라는 행위 자체를 더 쉽고, 더 즐겁고, 더 생산적으로 만들고 싶다)라고 답하며, 유연성과 성능을 저울질하는 기준으로 <strong>"Dynamic things are more flexible than static things, so when you want that flexibility, and you can afford it, go dynamic. If you can't afford it, stay static"</strong>(동적인 것은 정적인 것보다 유연하다. 그 유연성이 필요하고 감당할 수 있다면 동적으로 가라. 감당할 수 없다면 정적으로 남아라)라는 비용/이득 원칙을 제시한다.

| 쟁점 | Casey Muratori | Robert C. Martin(Uncle Bob) |
|------|-----------------|------------------------------|
| 성능의 위치 | 설계 단계에서 반드시 계산해야 할 1차 제약 | 여러 목표(가독성·생산성) 중 하나, 상황에 따라 저울질 |
| 다형성·가상 함수 | 불필요하게 남용되면 캐시·분기 예측을 구조적으로 해침 | "유연성이 필요하고 감당 가능할 때"만 쓰는 도구 |
| 판단 기준 | 하드웨어 이론 상한 대비 실측치의 격차 | 비용 대비 이득(유연성을 감당할 수 있는가) |
| 테스트 | 기본값이 아니라 비용/이득으로 판단할 선택 | 테스트가 곧 생산성·안정성의 기반이라는 입장(*Clean Code* 저서 전반) |

두 사람의 논쟁이 흥미로운 지점은, 결국 "가상 함수를 쓸지 switch문을 쓸지" 같은 기법 선택의 문제가 아니라 **무엇을 최적화 대상으로 삼을 것인가**라는 상위 질문으로 수렴한다는 데 있다. Muratori는 CPU 사이클을, Martin은 프로그래머가 코드를 이해하고 수정하는 데 드는 시간을 각각 1차 지표로 삼고 있어서, 같은 벤치마크 수치를 보고도 "그래서 이 비용을 감당할 가치가 있는가"에 대한 답이 갈린다.

## 판단 기준: 언제 설계 시점부터 성능을 생각해야 하는가

- **핫 루프(hot loop)가 존재를 이미 알고 있는 영역**(렌더링, 파싱, 대량 데이터 순회 등)이라면, 처음부터 데이터를 배열로 연속 배치하고 다형성 대신 태그드 유니온·switch문을 검토할 가치가 있다. 나중에 프로파일러가 찾아줄 격차가 애초에 구조적으로 좁혀져 있기 때문이다.
- **호출 빈도가 낮거나 I/O에 지배되는 코드**(설정 로딩, 드문 관리자 명령 처리 등)라면 Martin의 기준대로 유연성·가독성을 우선해도 실제 체감 성능에는 영향이 거의 없다. 이 경우 다형성이 굳이 배제할 대상은 아니다.
- **팀의 규모와 코드 수명**도 함께 고려해야 한다. Muratori 자신도 인정하듯 그의 기법은 어셈블리 수준 지식을 요구하는데, 이 지식을 팀 전체가 공유하지 못하면 스스로 <strong>"clean" 코드보다 유지보수가 더 어려운</strong> 코드를 만들 위험이 있다 — Martin이 반박에서 강조하는 지점과 정확히 겹치는 트레이드오프다.
- 판단이 서지 않을 때는 두 사람 모두 동의하는 유일한 지점, 즉 "**주장이 아니라 실측**"으로 돌아가는 것이 안전하다. 해당 핫 경로를 실제로 사이클 단위 또는 wall-clock으로 측정해 보지 않고서는 어느 쪽 우선순위가 맞는지 코드만 보고 판단할 수 없다.

## 한계와 남은 트레이드오프

이 글에서 다룬 수치는 Muratori 자신의 실험 환경(특정 CPU, 특정 컴파일러 최적화 플래그)에서 나온 결과이며, 배수 자체는 하드웨어·컴파일러 버전에 따라 달라질 수 있는 구현 정의(implementation-defined) 값이다. 또한 이 논쟁은 극단적으로 단순한 예제(도형 넓이 합산)에서 출발했다는 한계도 있다 — 실제 프로덕션 코드베이스에는 다형성이 성능보다 확장성·플러그인 구조를 위해 꼭 필요한 지점도 존재하며, 그런 지점까지 무조건 switch문으로 되돌리는 것은 Muratori 본인의 논지("측정 없이 통념을 따르지 말라")와도 모순된다. 결국 이 논쟁이 남기는 것은 정답이 아니라, "이 추상화의 비용을 실제로 재본 적이 있는가"라는 질문 그 자체다.

## 참고 자료

- [The Pragmatic Engineer, "Why performant code matters (but gets widely ignored), with Casey Muratori" (2026-08-26)](https://newsletter.pragmaticengineer.com/p/why-performant-code-matters-but-gets)
- [Casey Muratori, "\"Clean\" Code, Horrible Performance" — Computer, Enhance! (2023-02-28)](https://www.computerenhance.com/p/clean-code-horrible-performance)
- [Robert C. Martin & Casey Muratori, GitHub 저장소 "cmuratori-discussion"](https://github.com/unclebob/cmuratori-discussion)
