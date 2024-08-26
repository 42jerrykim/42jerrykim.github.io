---
title: "[SoftwareTesting] 소스 코드 테스트를 위한 메트릭"
categories: SoftwareTesting
tags:
- code coverage
- test coverage
- software engineering
- software testing
- unit testing
- integration testing
- regression testing
- test suite
- requirements coverage
- statement coverage
- branch coverage
- condition coverage
- edge coverage
- function coverage
- path coverage
- risk coverage
- compatibility coverage
- boundary value coverage
- parameter value coverage
- fault injection
- modified condition/decision coverage
- multiple condition coverage
- data-flow coverage
- static analysis
- test planning
- test design
- test execution
- test metrics
- test automation
- continuous integration
- quality assurance
- software quality
- agile testing
- test case management
- test strategy
- test results
- test scenarios
- test data
- test environment
- test documentation
- test optimization
- test maintenance
- software reliability
- software performance
- software scalability
- software security
- software defects
- software bugs
- software quality assurance
- software development lifecycle
header:
teaser: /assets/images/undefined/teaser.jpg
---

소스 코드 테스트에서의 메트릭은 소프트웨어 품질을 보장하는 데 중요한 역할을 한다. 특히 코드 커버리지와 테스트 커버리지는 소프트웨어 엔지니어링에서 필수적인 개념으로, 특정 테스트 스위트를 실행할 때 프로그램의 소스 코드가 얼마나 실행되었는지를 백분율로 측정한다. 높은 코드 커버리지를 가진 프로그램은 테스트 중에 더 많은 소스 코드가 실행되므로, 낮은 코드 커버리지를 가진 프로그램에 비해 발견되지 않은 소프트웨어 버그가 존재할 가능성이 낮다. 다양한 메트릭이 테스트 커버리지를 계산하는 데 사용되며, 기본적인 것들로는 프로그램의 서브루틴과 문장이 실행된 비율이 있다. 코드 커버리지는 체계적인 소프트웨어 테스트 방법 중 하나로, 1963년 Miller와 Maloney에 의해 처음으로 발표되었다. 테스트 스위트에 의해 실행된 코드의 비율을 측정하기 위해 여러 가지 커버리지 기준이 사용되며, 이는 일반적으로 테스트 스위트가 충족해야 하는 규칙이나 요구 사항으로 정의된다. 이러한 커버리지 기준에는 함수 커버리지, 문장 커버리지, 엣지 커버리지, 분기 커버리지, 조건 커버리지 등이 포함된다. 각 기준은 소프트웨어의 다양한 측면을 테스트하는 데 도움을 주며, 이를 통해 소프트웨어의 품질을 높이고 버그를 조기에 발견할 수 있다.


|![]()|
|:---:|
||


<!--
##### Outline #####
-->

<!--
---
## 소스 코드 테스트를 위한 메트릭
**소스 코드 기반의 커버리지 개요**  
**소프트웨어 엔지니어링에서의 코드 커버리지**  
**테스트 스위트 실행 시 코드 실행 비율**  
**높은 코드 커버리지의 중요성**  

## 기본 커버리지 기준
**기능 커버리지**  
**문장 커버리지**  
**엣지 커버리지**  
**조건 커버리지**  

## 수정된 조건/결정 커버리지
**결정 커버리지의 정의**  
**MC/DC의 필요성**  
**예시 코드 분석**  

## 다중 조건 커버리지
**모든 조건 조합 테스트**  
**테스트 케이스 예시**  

## 매개변수 값 커버리지
**매개변수의 일반적인 값 테스트**  
**버그 발생 가능성 감소**  

## 기타 커버리지 기준
**LCSAJ 커버리지**  
**경로 커버리지**  
**루프 커버리지**  
**상태 커버리지**  
**데이터 흐름 커버리지**  

## safety-critical 애플리케이션에서의 커버리지
**100% 커버리지 요구 사항**  
**커버리지 목표 설정의 비판**  

## 테스트 커버리지 정책 구현
**최종 제품 인증을 위한 커버리지 요구 사항**  
**테스트 결과를 통한 추가 테스트 개발**  

## 테스트 커버리지 기술
**테스트 계획 수립**  
**유닛 테스트 작성**  
**정적 분석 도구 사용**  
**테스트 케이스 개선**  
**자동화된 테스트 실행**  
**테스트 결과 추적**  
**테스트 커버리지 검토**  
**제3자 도구 활용**  
**품질 향상**  
**테스트 케이스 최적화**  
**지속적 통합 시스템 설정**  

## 테스트 커버리지 기법
**테스트 전략 선택**  
**테스트 케이스 우선순위 지정**  
**조기 및 빈번한 테스트**  
**팀원 간 협업**  
**테스트 커버리지 지속적 평가 및 수정**  
**자동화의 현명한 사용**  
**적절한 테스트 데이터 확보**  
**테스트 설계에 투자**  
**방어적 사고**  
**테스트 커버리지 추적**  
**결과 검토 및 분석**  
**코드 변경 모니터링**  

## 테스트 커버리지 향상을 위한 모범 사례
**명확한 목표 및 목표 정의**  
**테스트의 중요한 영역 식별**  
**테스트 방법의 조합 사용**  
**테스트 커버리지 지속적 모니터링 및 평가**  
**테스트 케이스 정기적 업데이트**  
**테스트 커버리지는 팀의 노력**  
**코드 커버리지 도구 구현**  

## 요약
**테스트 커버리지의 중요성**  
**소프트웨어 품질 보장**  
**테스트 커버리지 기술의 활용**  

## 자주 묻는 질문
**테스트 커버리지 측정 방법**  
**좋은 테스트 커버리지란?**  
**소프트웨어 테스트에서의 테스트 커버리지란?**  
**테스트 커버리지 개선 방법**  
**수동 테스트에서의 테스트 커버리지란?**  
**충분한 테스트 커버리지란?**  
**최대 테스트 커버리지란?**  
**100% 테스트 커버리지란?**  

## 결론
**테스트 커버리지의 역할**  
**소프트웨어 품질 보장**  
**테스트 커버리지의 지속적 개선 필요성**  

---
-->

<!--
---
## 소스 코드 테스트를 위한 메트릭
**소스 코드 기반의 커버리지 개요**  
**소프트웨어 엔지니어링에서의 코드 커버리지**  
**테스트 스위트 실행 시 코드 실행 비율**  
**높은 코드 커버리지의 중요성**  
-->

## 소스 코드 테스트를 위한 메트릭

**소스 코드 기반의 커버리지 개요**  

소스 코드 커버리지는 소프트웨어 테스트에서 코드의 실행 비율을 측정하는 중요한 지표이다. 이는 테스트가 얼마나 효과적으로 코드의 다양한 경로를 실행하는지를 나타내며, 코드의 품질과 안정성을 높이는 데 기여한다. 커버리지를 측정함으로써 개발자는 테스트의 부족한 부분을 파악하고, 이를 보완하기 위한 추가 테스트 케이스를 작성할 수 있다.

**소프트웨어 엔지니어링에서의 코드 커버리지**  

소프트웨어 엔지니어링에서는 코드 커버리지가 소프트웨어 품질 보증의 핵심 요소로 자리 잡고 있다. 코드 커버리지는 주로 유닛 테스트, 통합 테스트, 시스템 테스트 등 다양한 테스트 단계에서 측정된다. 이를 통해 개발자는 코드의 결함을 조기에 발견하고, 수정할 수 있는 기회를 가지게 된다.

**테스트 스위트 실행 시 코드 실행 비율**  

테스트 스위트는 여러 테스트 케이스를 포함하는 집합으로, 소프트웨어의 특정 기능이나 모듈을 검증하는 데 사용된다. 테스트 스위트를 실행할 때, 각 테스트 케이스가 코드의 어느 부분을 실행했는지를 분석하여 코드 실행 비율을 계산한다. 이 비율은 코드의 품질을 평가하는 데 중요한 역할을 한다.

**높은 코드 커버리지의 중요성**  

높은 코드 커버리지는 소프트웨어의 신뢰성을 높이는 데 기여한다. 코드 커버리지가 높을수록, 코드의 결함이 발견될 가능성이 줄어들고, 이는 최종 사용자에게 더 나은 품질의 소프트웨어를 제공하는 결과로 이어진다. 따라서 개발팀은 코드 커버리지를 지속적으로 모니터링하고, 이를 개선하기 위한 노력을 기울여야 한다.

<!--
## 기본 커버리지 기준
**기능 커버리지**  
**문장 커버리지**  
**엣지 커버리지**  
**조건 커버리지**  
-->

## 기본 커버리지 기준

**기능 커버리지**  

기능 커버리지는 소프트웨어의 특정 기능이 테스트되었는지를 측정하는 지표이다. 이는 소프트웨어의 요구 사항이 얼마나 잘 충족되었는지를 평가하는 데 중요한 역할을 한다. 기능 커버리지를 높이기 위해서는 모든 기능이 테스트 케이스에 포함되어야 하며, 각 기능이 예상대로 작동하는지를 확인해야 한다. 이를 통해 소프트웨어의 품질을 보장할 수 있다.

**문장 커버리지**  

문장 커버리지는 코드의 각 문장이 테스트 케이스에 의해 실행되었는지를 측정하는 지표이다. 이는 코드의 각 라인이 적어도 한 번은 실행되었는지를 확인함으로써, 코드의 기본적인 동작이 올바른지를 평가하는 데 도움을 준다. 문장 커버리지를 높이기 위해서는 다양한 입력값을 사용하여 테스트 케이스를 작성해야 하며, 이를 통해 코드의 모든 경로가 실행되도록 해야 한다.

**엣지 커버리지**  

엣지 커버리지는 코드의 각 분기점에서의 경로가 테스트되었는지를 측정하는 지표이다. 이는 조건문이나 반복문과 같은 제어 구조에서의 경로를 평가하는 데 중요하다. 엣지 커버리지를 높이기 위해서는 각 조건의 참과 거짓에 대해 테스트 케이스를 작성해야 하며, 이를 통해 코드의 모든 분기 경로가 테스트되도록 해야 한다.

**조건 커버리지**  

조건 커버리지는 각 조건이 참과 거짓으로 평가되는 경우를 모두 테스트했는지를 측정하는 지표이다. 이는 복잡한 조건문에서의 모든 가능한 경로를 확인하는 데 중요하다. 조건 커버리지를 높이기 위해서는 다양한 조합의 입력값을 사용하여 테스트 케이스를 작성해야 하며, 이를 통해 모든 조건이 적절히 평가되도록 해야 한다. 

이러한 기본 커버리지 기준들은 소프트웨어 테스트의 기초를 형성하며, 각 기준을 충족시키는 것이 소프트웨어의 품질을 높이는 데 필수적이다.

<!--
## 수정된 조건/결정 커버리지
**결정 커버리지의 정의**  
**MC/DC의 필요성**  
**예시 코드 분석**  
-->

## 수정된 조건/결정 커버리지

**결정 커버리지의 정의**  

결정 커버리지는 소프트웨어 테스트에서 특정 조건이 참 또는 거짓으로 평가되는 모든 경우를 테스트하는 것을 의미한다. 이는 각 조건이 독립적으로 평가되는지를 확인하여, 코드의 모든 분기 경로가 테스트되었는지를 보장하는 데 중요한 역할을 한다. 결정 커버리지는 코드의 복잡성을 줄이고, 버그를 조기에 발견할 수 있도록 도와준다. 

**MC/DC의 필요성**  

MC/DC(Modified Condition/Decision Coverage)는 결정 커버리지의 한 형태로, 각 조건이 결과에 미치는 영향을 독립적으로 평가하는 것을 목표로 한다. MC/DC는 특히 safety-critical 시스템에서 요구되는 커버리지 기준으로, 각 조건이 참 또는 거짓으로 평가될 때 결과에 미치는 영향을 명확히 하기 위해 필요하다. 이를 통해 소프트웨어의 신뢰성을 높이고, 잠재적인 결함을 사전에 방지할 수 있다.

**예시 코드 분석**  

다음은 MC/DC를 적용한 간단한 예시 코드이다.

```python
def example_function(a, b):
    if a > 0 and b > 0:
        return "Both are positive"
    elif a > 0 and b <= 0:
        return "Only a is positive"
    elif a <= 0 and b > 0:
        return "Only b is positive"
    else:
        return "Neither is positive"
```

위의 코드에서 `a`와 `b`의 조건을 각각 독립적으로 평가하여, 모든 가능한 조합을 테스트해야 한다. 예를 들어, `a`가 양수이고 `b`가 음수인 경우, `a`의 조건이 결과에 미치는 영향을 확인할 수 있다. 이를 통해 각 조건이 결과에 미치는 영향을 명확히 파악할 수 있으며, 이는 MC/DC의 핵심이다. 

이와 같은 방식으로 결정 커버리지를 적용하면, 코드의 품질을 높이고, 소프트웨어의 신뢰성을 강화할 수 있다.

<!--
## 다중 조건 커버리지
**모든 조건 조합 테스트**  
**테스트 케이스 예시**  
-->

## 다중 조건 커버리지

**모든 조건 조합 테스트**  

다중 조건 커버리지는 소프트웨어 테스트에서 모든 조건의 조합을 테스트하는 기법이다. 이 기법은 각 조건이 참 또는 거짓일 때의 모든 가능한 조합을 고려하여 테스트 케이스를 작성하는 것을 목표로 한다. 이를 통해 소프트웨어의 다양한 경로를 검증하고, 특정 조건 조합에서 발생할 수 있는 버그를 발견할 수 있다. 다중 조건 커버리지는 특히 복잡한 로직을 가진 소프트웨어에서 유용하다. 

예를 들어, 다음과 같은 조건문이 있다고 가정해 보자.

```java
if (A && B) {
    // 코드 블록 1
} else if (A && !B) {
    // 코드 블록 2
} else if (!A && B) {
    // 코드 블록 3
} else {
    // 코드 블록 4
}
```

이 경우, A와 B의 모든 조합을 고려하여 테스트 케이스를 작성해야 한다. A와 B가 각각 참(true) 또는 거짓(false)일 때의 모든 조합을 테스트하여 각 코드 블록이 올바르게 실행되는지를 확인해야 한다.

**테스트 케이스 예시**  

다중 조건 커버리지를 적용하기 위한 테스트 케이스 예시는 다음과 같다.

1. A = true, B = true → 코드 블록 1 실행
2. A = true, B = false → 코드 블록 2 실행
3. A = false, B = true → 코드 블록 3 실행
4. A = false, B = false → 코드 블록 4 실행

이러한 테스트 케이스를 통해 모든 조건 조합이 테스트되며, 각 조건의 조합에 따른 소프트웨어의 동작을 검증할 수 있다. 다중 조건 커버리지는 소프트웨어의 신뢰성을 높이는 데 중요한 역할을 한다. 

이와 같은 방식으로 다중 조건 커버리지를 활용하면, 소프트웨어의 품질을 높이고, 잠재적인 버그를 사전에 발견할 수 있는 기회를 제공한다. 따라서, 소프트웨어 개발 과정에서 다중 조건 커버리지를 적극적으로 활용하는 것이 중요하다.

<!--
## 매개변수 값 커버리지
**매개변수의 일반적인 값 테스트**  
**버그 발생 가능성 감소**  
-->

## 매개변수 값 커버리지

**매개변수의 일반적인 값 테스트**  

매개변수 값 커버리지는 소프트웨어 테스트에서 특정 함수나 메서드의 매개변수에 대해 다양한 값을 입력하여 테스트하는 기법이다. 이 기법은 매개변수의 다양한 조합을 통해 소프트웨어의 동작을 검증하고, 예상치 못한 버그를 발견하는 데 도움을 준다. 매개변수 값 커버리지를 통해 개발자는 각 매개변수가 소프트웨어의 동작에 미치는 영향을 이해하고, 이를 통해 더 나은 품질의 소프트웨어를 제공할 수 있다.

예를 들어, 특정 함수가 두 개의 매개변수를 받는다고 가정해보자. 이 함수는 두 매개변수의 값에 따라 다른 결과를 반환할 수 있다. 따라서, 매개변수 값 커버리지를 적용하여 각 매개변수에 대해 다양한 값을 입력하고, 그 결과를 비교함으로써 함수의 동작을 검증할 수 있다. 이 과정에서 매개변수의 경계값, 일반적인 값, 비정상적인 값 등을 포함하여 다양한 테스트 케이스를 생성하는 것이 중요하다.

**버그 발생 가능성 감소**  

매개변수 값 커버리지를 통해 다양한 입력값을 테스트함으로써 소프트웨어의 버그 발생 가능성을 줄일 수 있다. 특히, 매개변수의 조합이 복잡한 경우, 모든 조합을 테스트하는 것은 현실적으로 불가능할 수 있다. 이때 매개변수 값 커버리지를 활용하면, 가장 중요한 조합을 선택하여 테스트할 수 있으며, 이를 통해 소프트웨어의 안정성을 높일 수 있다.

또한, 매개변수 값 커버리지는 코드의 가독성을 높이고, 유지보수를 용이하게 만드는 데도 기여한다. 매개변수에 대한 명확한 테스트 케이스가 존재하면, 개발자는 코드 변경 시 발생할 수 있는 문제를 사전에 예방할 수 있다. 따라서, 매개변수 값 커버리지는 소프트웨어 개발 과정에서 필수적인 요소로 자리 잡고 있다.

결론적으로, 매개변수 값 커버리지는 소프트웨어의 품질을 높이고, 버그 발생 가능성을 줄이는 데 중요한 역할을 한다. 이를 통해 개발자는 더 나은 소프트웨어를 제공할 수 있으며, 사용자에게도 안정적인 경험을 제공할 수 있다.

<!--
## 기타 커버리지 기준
**LCSAJ 커버리지**  
**경로 커버리지**  
**루프 커버리지**  
**상태 커버리지**  
**데이터 흐름 커버리지**  
-->

## 기타 커버리지 기준

**LCSAJ 커버리지**  

LCSAJ(Limited Code Structure and Analysis of Jumps) 커버리지는 프로그램의 코드 구조를 분석하여 특정 경로를 따라 실행되는 코드의 비율을 측정하는 방법이다. 이 커버리지는 코드의 복잡성을 줄이고, 테스트 케이스의 효율성을 높이는 데 도움을 준다. LCSAJ 커버리지를 통해 개발자는 코드의 특정 부분이 얼마나 잘 테스트되었는지를 파악할 수 있으며, 이를 통해 추가적인 테스트가 필요한 영역을 식별할 수 있다.

**경로 커버리지**  

경로 커버리지는 프로그램의 모든 가능한 실행 경로를 테스트하는 것을 목표로 한다. 이는 코드의 모든 분기와 루프를 포함하여, 가능한 모든 경로를 탐색하는 방식이다. 경로 커버리지는 매우 철저한 테스트 방법이지만, 복잡한 프로그램에서는 모든 경로를 테스트하는 것이 비현실적일 수 있다. 따라서 경로 커버리지는 주로 중요한 기능이나 복잡한 알고리즘에 대해 적용된다.

**루프 커버리지**  

루프 커버리지는 프로그램 내의 루프 구조가 얼마나 잘 테스트되었는지를 측정하는 방법이다. 루프는 프로그램의 흐름에서 중요한 역할을 하며, 루프의 반복 횟수나 조건에 따라 프로그램의 동작이 달라질 수 있다. 루프 커버리지를 통해 개발자는 루프가 다양한 조건에서 어떻게 작동하는지를 확인할 수 있으며, 이를 통해 잠재적인 버그를 사전에 발견할 수 있다.

**상태 커버리지**  

상태 커버리지는 프로그램의 다양한 상태가 얼마나 잘 테스트되었는지를 측정하는 방법이다. 프로그램은 다양한 입력에 따라 여러 상태로 전환될 수 있으며, 각 상태에서의 동작이 중요하다. 상태 커버리지를 통해 개발자는 특정 상태에서 발생할 수 있는 문제를 사전에 식별하고, 이를 해결하기 위한 테스트 케이스를 작성할 수 있다.

**데이터 흐름 커버리지**  

데이터 흐름 커버리지는 프로그램 내의 데이터가 어떻게 흐르는지를 분석하여, 데이터의 생성, 사용, 삭제 과정을 추적하는 방법이다. 이 커버리지는 변수의 생명 주기와 데이터의 흐름을 이해하는 데 도움을 주며, 데이터 관련 버그를 발견하는 데 유용하다. 데이터 흐름 커버리지를 통해 개발자는 데이터가 올바르게 처리되고 있는지를 확인할 수 있으며, 이를 통해 소프트웨어의 품질을 높일 수 있다.

<!--
## safety-critical 애플리케이션에서의 커버리지
**100% 커버리지 요구 사항**  
**커버리지 목표 설정의 비판**  
-->

## safety-critical 애플리케이션에서의 커버리지

**100% 커버리지 요구 사항**  

safety-critical 애플리케이션은 생명이나 재산에 직접적인 영향을 미치는 소프트웨어를 의미한다. 이러한 애플리케이션에서는 소프트웨어의 결함이 치명적인 결과를 초래할 수 있기 때문에, 100% 커버리지를 요구하는 경우가 많다. 예를 들어, 항공기 제어 시스템이나 의료 기기 소프트웨어는 모든 코드 경로가 테스트되어야 하며, 이는 안전성을 보장하기 위한 필수 조건이다. 

100% 커버리지를 달성하기 위해서는 모든 기능, 조건, 경로가 테스트되어야 하며, 이를 위해 다양한 테스트 기법이 사용된다. 그러나 100% 커버리지를 달성하는 것이 항상 현실적이지는 않으며, 특정 상황에서는 불가능할 수도 있다. 따라서, safety-critical 애플리케이션의 경우, 커버리지 목표를 설정할 때는 실제로 달성 가능한 목표를 설정하는 것이 중요하다.

**커버리지 목표 설정의 비판**  

커버리지 목표를 설정하는 것은 소프트웨어 개발 과정에서 중요한 단계이다. 그러나 이러한 목표가 항상 유용한 것은 아니다. 예를 들어, 100% 커버리지를 목표로 설정할 경우, 개발자들은 코드의 모든 부분을 테스트하기 위해 지나치게 많은 시간과 자원을 소모할 수 있다. 이는 실제로 소프트웨어의 품질을 향상시키기보다는 비효율적인 결과를 초래할 수 있다.

또한, 커버리지 목표가 지나치게 높을 경우, 개발자들은 테스트의 질보다는 양에 집중하게 될 위험이 있다. 이는 테스트가 실제로 중요한 시나리오를 다루지 못하게 만들 수 있으며, 결과적으로 소프트웨어의 결함을 발견하지 못할 수도 있다. 따라서, 커버리지 목표를 설정할 때는 실제로 중요한 기능과 경로를 우선적으로 테스트하는 것이 필요하다.

결론적으로, safety-critical 애플리케이션에서의 커버리지 목표는 신중하게 설정되어야 하며, 단순히 숫자에 집착하기보다는 소프트웨어의 실제 품질을 향상시키는 방향으로 나아가야 한다.

<!--
## 테스트 커버리지 정책 구현
**최종 제품 인증을 위한 커버리지 요구 사항**  
**테스트 결과를 통한 추가 테스트 개발**  
-->

## 테스트 커버리지 정책 구현

**최종 제품 인증을 위한 커버리지 요구 사항**  

소프트웨어 개발에서 테스트 커버리지는 제품의 품질을 보장하는 중요한 요소이다. 최종 제품 인증을 위해서는 특정 커버리지 기준을 충족해야 한다. 이러한 기준은 제품의 복잡성, 사용되는 기술, 그리고 고객의 요구 사항에 따라 달라질 수 있다. 일반적으로, 80% 이상의 코드 커버리지를 목표로 설정하는 것이 좋으며, 이는 제품의 신뢰성을 높이는 데 기여한다. 

또한, 커버리지 요구 사항은 프로젝트 초기 단계에서부터 명확히 정의되어야 하며, 이를 통해 개발팀은 테스트 계획을 수립하고, 필요한 테스트 케이스를 작성할 수 있다. 최종 제품 인증을 위한 커버리지 요구 사항은 고객과의 협의를 통해 결정되며, 이를 통해 고객의 기대에 부합하는 제품을 제공할 수 있다.

**테스트 결과를 통한 추가 테스트 개발**  

테스트 결과는 소프트웨어의 품질을 평가하는 중요한 지표이다. 테스트를 수행한 후, 결과를 분석하여 추가적인 테스트가 필요한 영역을 식별할 수 있다. 예를 들어, 특정 기능에서 높은 결함률이 발견되었다면, 해당 기능에 대한 추가 테스트 케이스를 개발하여 문제를 해결해야 한다. 

또한, 테스트 결과를 기반으로 커버리지 지표를 지속적으로 모니터링하고, 이를 통해 테스트 전략을 조정하는 것이 중요하다. 테스트 결과를 분석하는 과정에서 발견된 문제점은 개발팀과의 협의를 통해 해결 방안을 모색해야 하며, 이를 통해 소프트웨어의 품질을 지속적으로 향상시킬 수 있다. 

테스트 커버리지 정책은 단순히 커버리지 수치를 높이는 것이 아니라, 실제로 소프트웨어의 품질을 보장하는 데 중점을 두어야 한다. 따라서, 테스트 결과를 통해 추가 테스트를 개발하고, 이를 통해 제품의 신뢰성을 높이는 것이 중요하다.

<!--
## 테스트 커버리지 기술
**테스트 계획 수립**  
**유닛 테스트 작성**  
**정적 분석 도구 사용**  
**테스트 케이스 개선**  
**자동화된 테스트 실행**  
**테스트 결과 추적**  
**테스트 커버리지 검토**  
**제3자 도구 활용**  
**품질 향상**  
**테스트 케이스 최적화**  
**지속적 통합 시스템 설정**  
-->

## 테스트 커버리지 기술

**테스트 계획 수립**  

테스트 계획은 소프트웨어 개발 과정에서 매우 중요한 단계이다. 이 단계에서는 테스트의 범위, 목표, 자원, 일정 등을 정의한다. 테스트 계획을 수립함으로써 팀원들은 각자의 역할을 명확히 이해하고, 테스트 진행 상황을 효과적으로 관리할 수 있다. 또한, 테스트 계획은 프로젝트의 전반적인 품질 보증 전략의 기초가 된다.

**유닛 테스트 작성**  

유닛 테스트는 소프트웨어의 개별 구성 요소를 검증하는 과정이다. 각 모듈이나 함수가 예상대로 작동하는지를 확인하기 위해 작성된다. 유닛 테스트는 코드 변경 시 발생할 수 있는 버그를 조기에 발견할 수 있도록 도와준다. 이를 통해 개발자는 코드의 품질을 높이고, 유지보수 비용을 줄일 수 있다.

**정적 분석 도구 사용**  

정적 분석 도구는 소스 코드를 실행하지 않고도 코드의 품질을 평가할 수 있는 도구이다. 이러한 도구는 코드의 스타일, 구조, 복잡성 등을 분석하여 잠재적인 문제를 발견할 수 있다. 정적 분석을 통해 개발자는 코드의 품질을 향상시키고, 버그를 사전에 예방할 수 있다.

**테스트 케이스 개선**  

테스트 케이스는 소프트웨어의 특정 기능이나 모듈을 검증하기 위해 작성된 문서이다. 테스트 케이스를 지속적으로 개선함으로써 테스트의 효율성을 높일 수 있다. 이를 위해 테스트 케이스의 결과를 분석하고, 실패한 테스트의 원인을 파악하여 수정하는 과정이 필요하다.

**자동화된 테스트 실행**  

자동화된 테스트는 수동으로 테스트를 수행하는 대신, 자동화 도구를 사용하여 테스트를 실행하는 방법이다. 자동화된 테스트는 반복적인 작업을 줄이고, 테스트의 일관성을 높일 수 있다. 또한, 코드 변경 시 자동으로 테스트를 실행하여 빠르게 피드백을 받을 수 있는 장점이 있다.

**테스트 결과 추적**  

테스트 결과를 추적하는 것은 테스트의 효과성을 평가하는 데 중요한 요소이다. 테스트 결과를 기록하고 분석함으로써, 어떤 부분에서 문제가 발생했는지를 파악할 수 있다. 이를 통해 향후 테스트 계획을 수정하고, 품질 향상을 위한 전략을 수립할 수 있다.

**테스트 커버리지 검토**  

테스트 커버리지는 테스트가 코드의 어느 정도를 검증했는지를 나타내는 지표이다. 테스트 커버리지를 정기적으로 검토함으로써, 테스트의 효과성을 평가하고, 부족한 부분을 보완할 수 있다. 높은 테스트 커버리지는 소프트웨어의 품질을 보장하는 데 중요한 역할을 한다.

**제3자 도구 활용**  

제3자 도구는 테스트 커버리지, 성능 분석, 버그 추적 등을 지원하는 외부 도구를 의미한다. 이러한 도구를 활용함으로써, 개발팀은 보다 효율적으로 테스트를 수행하고, 품질을 향상시킬 수 있다. 제3자 도구는 팀의 작업을 간소화하고, 테스트 프로세스를 개선하는 데 기여한다.

**품질 향상**  

소프트웨어의 품질 향상은 모든 개발팀의 목표이다. 테스트 커버리지 기술을 통해 품질을 향상시키기 위해서는 지속적인 개선과 피드백이 필요하다. 팀원 간의 협업과 소통을 통해 품질 향상을 위한 전략을 수립하고, 이를 실행하는 것이 중요하다.

**테스트 케이스 최적화**  

테스트 케이스 최적화는 테스트의 효율성을 높이기 위한 과정이다. 불필요한 테스트를 제거하고, 중요한 테스트에 집중함으로써 테스트 시간을 단축할 수 있다. 최적화된 테스트 케이스는 더 나은 품질 보증을 가능하게 한다.

**지속적 통합 시스템 설정**  

지속적 통합(CI) 시스템은 코드 변경 시 자동으로 빌드 및 테스트를 수행하는 시스템이다. 이를 통해 개발자는 코드 변경의 영향을 즉시 확인할 수 있으며, 버그를 조기에 발견할 수 있다. 지속적 통합 시스템은 소프트웨어 개발의 효율성을 높이고, 품질을 보장하는 데 중요한 역할을 한다.

<!--
## 테스트 커버리지 기법
**테스트 전략 선택**  
**테스트 케이스 우선순위 지정**  
**조기 및 빈번한 테스트**  
**팀원 간 협업**  
**테스트 커버리지 지속적 평가 및 수정**  
**자동화의 현명한 사용**  
**적절한 테스트 데이터 확보**  
**테스트 설계에 투자**  
**방어적 사고**  
**테스트 커버리지 추적**  
**결과 검토 및 분석**  
**코드 변경 모니터링**  
-->

## 테스트 커버리지 기법

**테스트 전략 선택**  

테스트 전략은 소프트웨어 개발 과정에서 테스트를 어떻게 수행할 것인지에 대한 계획을 의미한다. 효과적인 테스트 전략을 수립하기 위해서는 프로젝트의 요구 사항, 리스크, 자원 등을 고려해야 한다. 예를 들어, 애자일 개발 환경에서는 반복적인 테스트와 피드백이 중요하므로, 지속적인 통합(CI)과 지속적인 배포(CD) 전략을 채택하는 것이 유리하다. 

**테스트 케이스 우선순위 지정**  

테스트 케이스의 우선순위를 지정하는 것은 제한된 시간과 자원 내에서 가장 중요한 기능을 테스트하는 데 도움이 된다. 일반적으로 비즈니스에 가장 큰 영향을 미치는 기능이나, 사용자에게 가장 많이 사용되는 기능을 우선적으로 테스트해야 한다. 이를 통해 중요한 결함을 조기에 발견할 수 있다.

**조기 및 빈번한 테스트**  

소프트웨어 개발 초기 단계에서부터 테스트를 시작하는 것이 중요하다. 조기 테스트는 결함을 조기에 발견하고 수정할 수 있는 기회를 제공한다. 또한, 빈번한 테스트를 통해 소프트웨어의 품질을 지속적으로 유지할 수 있다. 이를 위해 자동화된 테스트 도구를 활용하는 것이 효과적이다.

**팀원 간 협업**  

테스트는 혼자서 수행하는 작업이 아니다. 개발자, 테스터, 비즈니스 분석가 등 다양한 팀원 간의 협업이 필요하다. 팀원 간의 원활한 소통과 협업을 통해 테스트의 효율성을 높일 수 있으며, 각자의 전문성을 활용하여 더 나은 테스트 결과를 도출할 수 있다.

**테스트 커버리지 지속적 평가 및 수정**  

테스트 커버리지는 지속적으로 평가하고 수정해야 한다. 초기에는 높은 커버리지를 목표로 하더라도, 시간이 지남에 따라 새로운 기능이 추가되거나 기존 기능이 변경될 수 있다. 따라서 정기적으로 테스트 커버리지를 점검하고, 필요한 경우 테스트 케이스를 수정하거나 추가해야 한다.

**자동화의 현명한 사용**  

자동화된 테스트는 반복적인 작업을 줄이고, 테스트의 일관성을 높이는 데 도움이 된다. 그러나 모든 테스트를 자동화할 수는 없으므로, 자동화가 적합한 테스트와 수동 테스트가 필요한 부분을 구분하는 것이 중요하다. 예를 들어, 회귀 테스트는 자동화에 적합하지만, 사용자 경험을 평가하는 테스트는 수동으로 수행하는 것이 좋다.

**적절한 테스트 데이터 확보**  

테스트를 수행하기 위해서는 적절한 테스트 데이터가 필요하다. 실제 운영 환경과 유사한 데이터를 사용하여 테스트를 수행하면, 더 현실적인 결과를 얻을 수 있다. 또한, 다양한 경계 조건과 예외 상황을 고려한 테스트 데이터를 준비하는 것이 중요하다.

**테스트 설계에 투자**  

테스트 설계는 테스트의 성공 여부를 결정짓는 중요한 요소이다. 초기 단계에서 충분한 시간을 투자하여 테스트 케이스를 설계하고, 각 테스트 케이스의 목적과 기대 결과를 명확히 해야 한다. 잘 설계된 테스트 케이스는 테스트의 효율성을 높이고, 결함 발견 확률을 증가시킨다.

**방어적 사고**  

방어적 사고는 소프트웨어 개발 및 테스트 과정에서 발생할 수 있는 문제를 미리 예측하고 대비하는 사고 방식을 의미한다. 이를 통해 예상치 못한 결함이나 오류를 사전에 방지할 수 있다. 예를 들어, 입력 값의 유효성을 검증하는 로직을 추가하여 잘못된 데이터로 인한 오류를 방지할 수 있다.

**테스트 커버리지 추적**  

테스트 커버리지를 추적하는 것은 테스트의 효과성을 평가하는 데 필수적이다. 커버리지 도구를 사용하여 어떤 코드가 테스트되었는지, 어떤 부분이 테스트되지 않았는지를 확인할 수 있다. 이를 통해 테스트의 빈틈을 찾아내고, 추가적인 테스트 케이스를 작성할 수 있다.

**결과 검토 및 분석**  

테스트 결과는 단순히 통과 여부만을 확인하는 것이 아니라, 결과를 분석하여 개선점을 찾아내는 것이 중요하다. 테스트 결과를 정기적으로 검토하고, 결함의 원인을 분석하여 향후 테스트에 반영해야 한다. 이를 통해 지속적인 품질 향상을 이룰 수 있다.

**코드 변경 모니터링**  

소프트웨어는 지속적으로 변경되기 때문에, 코드 변경 사항을 모니터링하는 것이 중요하다. 변경된 코드에 대한 테스트를 수행하여 새로운 결함이 발생하지 않도록 해야 한다. 또한, 코드 변경이 기존 기능에 미치는 영향을 분석하여 필요한 경우 추가적인 테스트를 수행해야 한다. 

이와 같은 테스트 커버리지 기법을 통해 소프트웨어의 품질을 높이고, 사용자에게 더 나은 경험을 제공할 수 있다.

<!--
## 테스트 커버리지 향상을 위한 모범 사례
**명확한 목표 및 목표 정의**  
**테스트의 중요한 영역 식별**  
**테스트 방법의 조합 사용**  
**테스트 커버리지 지속적 모니터링 및 평가**  
**테스트 케이스 정기적 업데이트**  
**테스트 커버리지는 팀의 노력**  
**코드 커버리지 도구 구현**  
-->

## 테스트 커버리지 향상을 위한 모범 사례

**명확한 목표 및 목표 정의**  

테스트 커버리지를 향상시키기 위해서는 명확한 목표를 설정하는 것이 중요하다. 목표는 팀의 비전과 일치해야 하며, 구체적이고 측정 가능해야 한다. 예를 들어, 특정 기능에 대한 테스트 커버리지를 80% 이상으로 설정할 수 있다. 이러한 목표는 팀원들이 무엇을 달성해야 하는지를 명확히 이해하는 데 도움을 준다.

**테스트의 중요한 영역 식별**  

소프트웨어의 모든 부분이 동일한 중요성을 가지지는 않다. 따라서, 테스트의 중요한 영역을 식별하는 것이 필요하다. 비즈니스 로직, 사용자 인터페이스, 데이터베이스와 같은 핵심 영역은 우선적으로 테스트해야 한다. 이를 통해 리소스를 효율적으로 사용할 수 있으며, 가장 중요한 부분에서의 결함을 조기에 발견할 수 있다.

**테스트 방법의 조합 사용**  

단일 테스트 방법만으로는 충분하지 않다. 다양한 테스트 방법을 조합하여 사용하는 것이 효과적이다. 유닛 테스트, 통합 테스트, 시스템 테스트, 회귀 테스트 등을 적절히 조합하여 사용하면, 각 테스트 방법의 장점을 극대화할 수 있다. 이를 통해 더 높은 커버리지를 달성할 수 있다.

**테스트 커버리지 지속적 모니터링 및 평가**  

테스트 커버리지는 지속적으로 모니터링하고 평가해야 한다. 정기적으로 커버리지 리포트를 생성하고, 이를 팀과 공유하여 현재 상태를 파악하는 것이 중요하다. 이를 통해 어떤 부분이 부족한지, 어떤 테스트가 필요한지를 명확히 알 수 있다. 또한, 커버리지 목표에 도달하기 위한 전략을 수정할 수 있다.

**테스트 케이스 정기적 업데이트**  

소프트웨어는 지속적으로 변화하기 때문에, 테스트 케이스도 정기적으로 업데이트해야 한다. 새로운 기능이 추가되거나 기존 기능이 변경될 때마다 관련된 테스트 케이스를 수정하거나 추가해야 한다. 이를 통해 테스트의 유효성을 유지하고, 커버리지를 높일 수 있다.

**테스트 커버리지는 팀의 노력**  

테스트 커버리지는 개인의 노력이 아닌 팀의 협력으로 이루어져야 한다. 팀원 간의 소통과 협업이 중요하며, 각자의 역할을 명확히 이해하고 책임을 다해야 한다. 팀 전체가 테스트 커버리지 향상에 기여할 수 있도록 분위기를 조성하는 것이 필요하다.

**코드 커버리지 도구 구현**  

효율적인 테스트 커버리지 관리를 위해 코드 커버리지 도구를 구현하는 것이 좋다. 이러한 도구는 코드의 어떤 부분이 테스트되었는지를 시각적으로 보여주며, 커버리지 리포트를 생성하는 데 도움을 준다. 이를 통해 팀은 커버리지 목표를 달성하기 위한 전략을 수립하고, 필요한 테스트 케이스를 추가할 수 있다.

<!--
## 요약
**테스트 커버리지의 중요성**  
**소프트웨어 품질 보장**  
**테스트 커버리지 기술의 활용**  
-->

## 요약

**테스트 커버리지의 중요성**  

테스트 커버리지는 소프트웨어 개발 과정에서 매우 중요한 요소이다. 이는 코드의 어느 부분이 테스트되었는지를 측정하여, 소프트웨어의 품질을 보장하는 데 기여한다. 높은 테스트 커버리지는 버그를 조기에 발견하고, 유지보수 비용을 줄이며, 최종 사용자에게 더 나은 경험을 제공하는 데 도움을 준다. 따라서, 개발팀은 테스트 커버리지를 지속적으로 모니터링하고 개선해야 한다.

**소프트웨어 품질 보장**  

소프트웨어 품질은 고객의 신뢰를 얻고, 비즈니스 성공에 필수적이다. 테스트 커버리지는 소프트웨어의 품질을 보장하는 중요한 도구로 작용한다. 코드의 다양한 경로와 조건을 테스트함으로써, 소프트웨어의 안정성과 신뢰성을 높일 수 있다. 이는 고객의 요구 사항을 충족시키고, 시장에서의 경쟁력을 강화하는 데 기여한다.

**테스트 커버리지 기술의 활용**  

테스트 커버리지를 효과적으로 활용하기 위해서는 다양한 기술과 도구를 사용하는 것이 중요하다. 예를 들어, 정적 분석 도구를 통해 코드의 품질을 사전에 점검하고, 자동화된 테스트를 통해 반복적인 테스트 작업을 효율적으로 수행할 수 있다. 또한, 테스트 커버리지 도구를 사용하여 코드의 커버리지를 시각적으로 분석하고, 개선할 부분을 식별하는 것이 필요하다. 이러한 기술들은 소프트웨어 개발 과정에서 테스트 커버리지를 극대화하는 데 도움을 준다.

<!--
## 자주 묻는 질문
**테스트 커버리지 측정 방법**  
**좋은 테스트 커버리지란?**  
**소프트웨어 테스트에서의 테스트 커버리지란?**  
**테스트 커버리지 개선 방법**  
**수동 테스트에서의 테스트 커버리지란?**  
**충분한 테스트 커버리지란?**  
**최대 테스트 커버리지란?**  
**100% 테스트 커버리지란?**  
-->

## 자주 묻는 질문

**테스트 커버리지 측정 방법**  

테스트 커버리지는 소프트웨어 테스트의 품질을 평가하는 중요한 지표이다. 이를 측정하기 위해서는 코드의 각 부분이 테스트되었는지를 확인해야 한다. 일반적으로 코드 커버리지 도구를 사용하여 테스트가 실행된 코드의 비율을 계산한다. 예를 들어, 문장 커버리지, 분기 커버리지, 조건 커버리지 등의 다양한 측정 방법이 있다. 이러한 도구들은 테스트 실행 후 커버리지 리포트를 생성하여 개발자에게 유용한 정보를 제공한다.

**좋은 테스트 커버리지란?**  

좋은 테스트 커버리지는 소프트웨어의 모든 중요한 기능이 테스트되었음을 의미한다. 일반적으로 80% 이상의 커버리지를 목표로 하는 것이 좋지만, 단순히 숫자에만 의존해서는 안 된다. 중요한 것은 테스트가 실제로 소프트웨어의 결함을 발견할 수 있는지를 평가하는 것이다. 따라서, 커버리지가 높더라도 테스트의 질이 낮다면 의미가 없다. 

**소프트웨어 테스트에서의 테스트 커버리지란?**  

소프트웨어 테스트에서의 테스트 커버리지는 코드의 특정 부분이 테스트되었는지를 나타내는 지표이다. 이는 코드의 품질을 보장하고, 결함을 조기에 발견하는 데 도움을 준다. 테스트 커버리지는 다양한 형태로 측정될 수 있으며, 각 형태는 특정한 테스트 목표에 맞춰져 있다. 예를 들어, 문장 커버리지는 코드의 각 문장이 실행되었는지를 측정하고, 분기 커버리지는 각 조건의 결과가 테스트되었는지를 평가한다.

**테스트 커버리지 개선 방법**  

테스트 커버리지를 개선하기 위해서는 먼저 현재 커버리지 수준을 평가해야 한다. 이후, 테스트 케이스를 추가하거나 수정하여 커버리지를 높일 수 있다. 또한, 코드 리뷰를 통해 테스트가 누락된 부분을 찾아내고, 자동화된 테스트 도구를 활용하여 테스트의 효율성을 높이는 것도 좋은 방법이다. 마지막으로, 팀원 간의 협업을 통해 다양한 시나리오를 테스트하는 것이 중요하다.

**수동 테스트에서의 테스트 커버리지란?**  

수동 테스트에서의 테스트 커버리지는 테스트 케이스가 수동으로 실행되었을 때 코드의 어느 부분이 테스트되었는지를 나타낸다. 수동 테스트는 자동화된 테스트에 비해 시간이 많이 소요되지만, 특정한 상황이나 사용자 경험을 평가하는 데 유용하다. 수동 테스트의 커버리지를 높이기 위해서는 테스트 계획을 철저히 세우고, 다양한 시나리오를 고려해야 한다.

**충분한 테스트 커버리지란?**  

충분한 테스트 커버리지는 소프트웨어의 주요 기능이 모두 테스트되었음을 의미한다. 이는 소프트웨어의 안정성과 신뢰성을 높이는 데 기여한다. 일반적으로 70% 이상의 커버리지를 목표로 하며, 중요한 기능에 대한 테스트가 포함되어야 한다. 그러나 커버리지가 높더라도 테스트의 질이 낮다면 충분하다고 할 수 없다.

**최대 테스트 커버리지란?**  

최대 테스트 커버리지는 가능한 모든 코드 경로와 조건이 테스트되었음을 의미한다. 이는 100% 커버리지를 목표로 하며, 모든 기능이 완벽하게 테스트되었음을 나타낸다. 그러나 현실적으로 모든 경로를 테스트하는 것은 매우 어렵고, 비용이 많이 들 수 있다. 따라서, 최대 커버리지를 목표로 하되, 실제로는 중요한 기능에 집중하는 것이 바람직하다.

**100% 테스트 커버리지란?**  

100% 테스트 커버리지는 모든 코드가 테스트되었음을 의미한다. 이는 이상적인 목표이지만, 실제로는 모든 경로와 조건을 테스트하는 것이 불가능할 수 있다. 그러나 100% 커버리지를 목표로 하는 것은 소프트웨어의 품질을 높이는 데 도움이 된다. 이를 위해서는 철저한 테스트 계획과 다양한 테스트 기법을 활용해야 한다.

<!--
## 결론
**테스트 커버리지의 역할**  
**소프트웨어 품질 보장**  
**테스트 커버리지의 지속적 개선 필요성**  
-->

## 결론

**테스트 커버리지의 역할**  

테스트 커버리지는 소프트웨어 개발 과정에서 매우 중요한 역할을 한다. 이는 코드의 어느 부분이 테스트되었는지를 측정하여, 소프트웨어의 품질을 보장하는 데 기여한다. 높은 테스트 커버리지는 버그를 조기에 발견하고, 코드의 안정성을 높이며, 유지보수 비용을 줄이는 데 도움을 준다. 또한, 테스트 커버리지를 통해 개발자는 코드의 복잡성을 이해하고, 필요한 경우 리팩토링을 통해 코드 품질을 향상시킬 수 있다.

**소프트웨어 품질 보장**  

소프트웨어 품질 보장은 고객의 신뢰를 얻고, 비즈니스의 성공을 좌우하는 중요한 요소이다. 테스트 커버리지는 소프트웨어의 품질을 보장하는 데 필수적인 도구로 작용한다. 이를 통해 개발자는 소프트웨어의 기능이 요구사항을 충족하는지 확인하고, 예상치 못한 오류를 사전에 방지할 수 있다. 또한, 테스트 커버리지를 통해 소프트웨어의 성능, 보안, 사용성 등을 평가할 수 있으며, 이는 최종 사용자에게 더 나은 경험을 제공하는 데 기여한다.

**테스트 커버리지의 지속적 개선 필요성**  

소프트웨어 개발 환경은 끊임없이 변화하고 있으며, 이에 따라 테스트 커버리지도 지속적으로 개선되어야 한다. 새로운 기능이 추가되거나 기존 기능이 변경될 때마다 테스트 커버리지를 재평가하고, 필요한 경우 새로운 테스트 케이스를 작성해야 한다. 또한, 테스트 커버리지 도구와 기법을 최신 상태로 유지하고, 팀원 간의 협업을 통해 테스트 커버리지를 지속적으로 향상시켜야 한다. 이를 통해 소프트웨어의 품질을 높이고, 고객의 기대에 부응할 수 있는 소프트웨어를 개발할 수 있다.

<!--
##### Reference #####
-->

## Reference


* [https://en.wikipedia.org/wiki/Code_coverage](https://en.wikipedia.org/wiki/Code_coverage)
* [https://muuktest.com/blog/test-coverage-techniques](https://muuktest.com/blog/test-coverage-techniques)
* [https://www.browserstack.com/guide/test-coverage-techniques](https://www.browserstack.com/guide/test-coverage-techniques)
* [https://medium.com/@case_lab/how-to-ensure-100-test-case-coverage-of-requirements-d0eaf82550ac](https://medium.com/@case_lab/how-to-ensure-100-test-case-coverage-of-requirements-d0eaf82550ac)
* [https://www.lambdatest.com/learning-hub/test-coverage](https://www.lambdatest.com/learning-hub/test-coverage)
* [https://muuktest.com/blog/test-coverage](https://muuktest.com/blog/test-coverage)
* [https://www.simform.com/blog/test-coverage/](https://www.simform.com/blog/test-coverage/)


<!--
Metric for source code testing

This article is about coverage based on source code. For coverage based on
requirements, see

[ Test coverage ](/wiki/Test_coverage "Test coverage")

.

In [ software engineering ](/wiki/Software_engineering "Software engineering")
, **code coverage** , also called **test coverage** , is a percentage measure
of the degree to which the [ source code ](/wiki/Source_code "Source code") of
a [ program ](/wiki/Computer_program "Computer program") is executed when a
particular [ test suite ](/wiki/Test_suite "Test suite") is run. A program
with high code coverage has more of its source code executed during testing,
which suggests it has a lower chance of containing undetected [ software bugs
](/wiki/Software_bug "Software bug") compared to a program with low code
coverage.  [  1  ]  [  2  ]  Many different metrics can be used to calculate
test coverage. Some of the most basic are the percentage of program [
subroutines ](/wiki/Subroutine "Subroutine") and the percentage of program [
statements ](/wiki/Statement_\(computer_science\) "Statement \(computer
science\)") called during execution of the test suite.

Code coverage was among the first methods invented for systematic [ software
testing ](/wiki/Software_testing "Software testing") . The first published
reference was by Miller and Maloney in _[ Communications of the ACM
](/wiki/Communications_of_the_ACM "Communications of the ACM") _ , in 1963.  [
3  ]

To measure what percentage of code has been executed by a [ test suite
](/wiki/Test_suite "Test suite") , one or more _coverage criteria_ are used.
These are usually defined as rules or requirements, which a test suite must
satisfy.  [  4  ]

###  Basic coverage criteria

[  [ edit  ](/w/index.php?title=Code_coverage&action=edit&section=2 "Edit
section: Basic coverage criteria") ]

There are a number of coverage criteria, but the main ones are:  [  5  ]

  * **Function coverage** – has each function (or [ subroutine ](/wiki/Subroutine "Subroutine") ) in the program been called? 
  * **Statement coverage** – has each [ statement ](/wiki/Statement_\(computer_science\) "Statement \(computer science\)") in the program been executed? 
  * **Edge coverage** – has every [ edge ](/wiki/Graph_theory "Graph theory") in the [ control-flow graph ](/wiki/Control-flow_graph "Control-flow graph") been executed? 
    * **Branch coverage** – has each branch (also called the [ DD-path ](/wiki/DD-path "DD-path") ) of each control structure (such as in [ _if_ and _case_ statements ](/wiki/Conditional_\(programming\) "Conditional \(programming\)") ) been executed? For example, given an _if_ statement, have both the _true_ and _false_ branches been executed? (This is a subset of edge coverage **.** ) 
  * **Condition coverage** – has each Boolean sub-expression evaluated both to true and false? (Also called predicate coverage.) 

For example, consider the following [ C ](/wiki/C_\(programming_language\) "C
\(programming language\)") function:

    
    
    int foo (int x, int y)
    {
        int z = 0;
        if ((x > 0) && (y > 0))
        {
            z = x;
        }
        return z;
    }
    

Assume this function is a part of some bigger program and this program was run
with some test suite.

  * _Function coverage_ will be satisfied if, during this execution, the function ` foo ` was called at least once. 
  * _Statement coverage_ for this function will be satisfied if it was called for example as ` foo(1,1) ` , because in this case, every line in the function would be executed—including ` z = x; ` . 
  * _Branch coverage_ will be satisfied by tests calling ` foo(1,1) ` and ` foo(0,1) ` because, in the first case, both ` if ` conditions are met and ` z = x; ` is executed, while in the second case, the first condition, ` (x>0) ` , is not satisfied, which prevents the execution of ` z = x; ` . 
  * _Condition coverage_ will be satisfied with tests that call ` foo(1,0) ` , ` foo(0,1) ` , and ` foo(1,1) ` . These are necessary because in the first case, ` (x>0) ` is evaluated to ` true ` , while in the second, it is evaluated to ` false ` . At the same time, the first case makes ` (y>0) ` ` false ` , the second case does not evaluate ` (y>0) ` (because of the lazy-evaluation of the boolean operator), the third case makes it ` true ` . 

In programming languages that do not perform [ short-circuit evaluation
](/wiki/Short-circuit_evaluation "Short-circuit evaluation") , condition
coverage does not necessarily imply branch coverage. For example, consider the
following [ Pascal ](/wiki/Pascal_\(programming_language\) "Pascal
\(programming language\)") code fragment:

Condition coverage can be satisfied by two tests:

  * ` a=true ` , ` b=false `
  * ` a=false ` , ` b=true `

However, this set of tests does not satisfy branch coverage since neither case
will meet the ` if ` condition.

[ Fault injection ](/wiki/Fault_injection "Fault injection") may be necessary
to ensure that all conditions and branches of [ exception-handling
](/wiki/Exception_handling "Exception handling") code have adequate coverage
during testing.

###  Modified condition/decision coverage

[  [ edit  ](/w/index.php?title=Code_coverage&action=edit&section=3 "Edit
section: Modified condition/decision coverage") ]

A combination of function coverage and branch coverage is sometimes also
called **decision coverage** . This criterion requires that every [ point of
entry and exit ](/wiki/Entry_and_exit_points "Entry and exit points") in the
program has been invoked at least once, and every decision in the program has
taken on all possible outcomes at least once. In this context, the decision is
a [ boolean expression ](/wiki/Boolean_expression "Boolean expression")
comprising conditions and zero or more boolean operators. This definition is
not the same as branch coverage,  [  6  ]  however, the term _decision
coverage_ is sometimes used as a synonym for it.  [  7  ]

**Condition/decision coverage** requires that both decision and condition
coverage be satisfied. However, for [ safety-critical ](/wiki/Safety-critical
"Safety-critical") applications (such as [ avionics software
](/wiki/Avionics_software "Avionics software") ) it is often required that
**modified condition/decision coverage (MC/DC)** be satisfied. This criterion
extends condition/decision criteria with requirements that each condition
should affect the decision outcome independently.

For example, consider the following code:

The condition/decision criteria will be satisfied by the following set of
tests:

a  |  b  |  c   
---|---|---  
true  |  true  |  true   
false  |  false  |  false   
  
However, the above tests set will not satisfy modified condition/decision
coverage, since in the first test, the value of 'b' and in the second test the
value of 'c' would not influence the output. So, the following test set is
needed to satisfy MC/DC:

a  |  b  |  c   
---|---|---  
false  |  true  |  **false**  
false  |  **true** |  **true**  
**false** |  **false** |  true   
**true** |  false  |  **true**  
  
###  Multiple condition coverage

[  [ edit  ](/w/index.php?title=Code_coverage&action=edit&section=4 "Edit
section: Multiple condition coverage") ]

This criterion requires that all combinations of conditions inside each
decision are tested. For example, the code fragment from the previous section
will require eight tests:

a  |  b  |  c   
---|---|---  
false  |  false  |  false   
false  |  false  |  true   
false  |  true  |  false   
false  |  true  |  true   
true  |  false  |  false   
true  |  false  |  true   
true  |  true  |  false   
true  |  true  |  true   
  
###  Parameter value coverage

[  [ edit  ](/w/index.php?title=Code_coverage&action=edit&section=5 "Edit
section: Parameter value coverage") ]

**Parameter value coverage** (PVC) requires that in a method taking
parameters, all the common values for such parameters be considered. The idea
is that all common possible values for a parameter are tested.  [  8  ]  For
example, common values for a string are: 1) [ null ](/wiki/Null_object "Null
object") , 2) empty, 3) whitespace (space, tabs, newline), 4) valid string, 5)
invalid string, 6) single-byte string, 7) double-byte string. It may also be
appropriate to use very long strings. Failure to test each possible parameter
value may result in a bug. Testing only one of these could result in 100% code
coverage as each line is covered, but as only one of seven options are tested,
there is only 14.2% PVC.

###  Other coverage criteria

[  [ edit  ](/w/index.php?title=Code_coverage&action=edit&section=6 "Edit
section: Other coverage criteria") ]

There are further coverage criteria, which are used less often:

  * **[ Linear Code Sequence and Jump ](/wiki/Linear_Code_Sequence_and_Jump "Linear Code Sequence and Jump") (LCSAJ) coverage ** a.k.a. **JJ-Path coverage** – has every LCSAJ/JJ-path been executed?  [  9  ] 
  * **Path coverage** – Has every possible route through a given part of the code been executed? 
  * **Entry/exit coverage** – Has every possible call and return of the function been executed? 
  * **Loop coverage** – Has every possible loop been executed zero times, once, and more than once? 
  * **State coverage** – Has each state in a [ finite-state machine ](/wiki/Finite-state_machine "Finite-state machine") been reached and explored? 
  * **Data-flow coverage** – Has each variable definition and its usage been reached and explored?  [  10  ] 

[ Safety-critical ](/wiki/Safety-critical "Safety-critical") or [ dependable
](/wiki/Dependability "Dependability") applications are often required to
demonstrate 100% of some form of test coverage. For example, the [ ECSS
](/wiki/European_Cooperation_for_Space_Standardization "European Cooperation
for Space Standardization") -E-ST-40C standard demands 100% statement and
decision coverage for two out of four different criticality levels; for the
other ones, target coverage values are up to negotiation between supplier and
customer.  [  11  ]  However, setting specific target values - and, in
particular, 100% - has been criticized by practitioners for various reasons
(cf.  [  12  ]  ) [ Martin Fowler ](/wiki/Martin_Fowler_\(software_engineer\)
"Martin Fowler \(software engineer\)") writes: "I would be suspicious of
anything like 100% - it would smell of someone writing tests to make the
coverage numbers happy, but not thinking about what they are doing".  [  13  ]

Some of the coverage criteria above are connected. For instance, path coverage
implies decision, statement and entry/exit coverage. Decision coverage implies
statement coverage, because every statement is part of a branch.

Full path coverage, of the type described above, is usually impractical or
impossible. Any module with a succession of  n  {\displaystyle n}
![{\\displaystyle
n}](https://wikimedia.org/api/rest_v1/media/math/render/svg/a601995d55609f2d9f5e233e36fbe9ea26011b3b)
decisions in it can have up to  2  n  {\displaystyle 2^{n}}  ![{\\displaystyle
2^{n}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/8226f30650ee4fe4e640c6d2798127e80e9c160d)
paths within it; loop constructs can result in an infinite number of paths.
Many paths may also be infeasible, in that there is no input to the program
under test that can cause that particular path to be executed. However, a
general-purpose algorithm for identifying infeasible paths has been proven to
be impossible (such an algorithm could be used to solve the [ halting problem
](/wiki/Halting_problem "Halting problem") ).  [  14  ]  [ Basis path testing
](/wiki/Basis_path_testing "Basis path testing") is for instance a method of
achieving complete branch coverage without achieving complete path coverage.
[  15  ]

Methods for practical path coverage testing instead attempt to identify
classes of code paths that differ only in the number of loop executions, and
to achieve "basis path" coverage the tester must cover all the path classes.
[ _[ citation needed  ](/wiki/Wikipedia:Citation_needed "Wikipedia:Citation
needed") _ ]  [ _[ clarification needed  ](/wiki/Wikipedia:Please_clarify
"Wikipedia:Please clarify") _ ]

The target software is built with special options or libraries and run under a
controlled environment, to map every executed function to the function points
in the source code. This allows testing parts of the target software that are
rarely or never accessed under normal conditions, and helps reassure that the
most important conditions (function points) have been tested. The resulting
output is then analyzed to see what areas of code have not been exercised and
the tests are updated to include these areas as necessary. Combined with other
test coverage methods, the aim is to develop a rigorous, yet manageable, set
of regression tests.

In implementing test coverage policies within a software development
environment, one must consider the following:

  * What are coverage requirements for the end product certification and if so what level of test coverage is required? The typical level of rigor progression is as follows: Statement, Branch/Decision, [ Modified Condition/Decision Coverage ](/wiki/Modified_Condition/Decision_Coverage "Modified Condition/Decision Coverage") (MC/DC), LCSAJ ( [ Linear Code Sequence and Jump ](/wiki/Linear_Code_Sequence_and_Jump "Linear Code Sequence and Jump") ) 
  * Will coverage be measured against tests that verify requirements levied on the system under test ( [ DO-178B ](/wiki/DO-178B "DO-178B") )? 
  * Is the object code generated directly traceable to source code statements? Certain certifications, (i.e. DO-178B Level A) require coverage at the assembly level if this is not the case: "Then, additional verification should be performed on the object code to establish the correctness of such generated code sequences" ( [ DO-178B ](/wiki/DO-178B "DO-178B") ) para-6.4.4.2.  [  16  ] 

Software authors can look at test coverage results to devise additional tests
and input or configuration sets to increase the coverage over vital functions.
Two common forms of test coverage are statement (or line) coverage and branch
(or edge) coverage. Line coverage reports on the execution footprint of
testing in terms of which lines of code were executed to complete the test.
Edge coverage reports which branches or code decision points were executed to
complete the test. They both report a coverage metric, measured as a
percentage. The meaning of this depends on what form(s) of coverage have been
used, as 67% branch coverage is more comprehensive than 67% statement
coverage.

Generally, test coverage tools incur computation and logging in addition to
the actual program thereby slowing down the application, so typically this
analysis is not done in production. As one might expect, there are classes of
software that cannot be feasibly subjected to these coverage tests, though a
degree of coverage mapping can be approximated through analysis rather than
direct testing.

There are also some sorts of defects which are affected by such tools. In
particular, some [ race conditions ](/wiki/Race_condition "Race condition") or
similar [ real time ](/wiki/Real-time_computing "Real-time computing")
sensitive operations can be masked when run under test environments; though
conversely, some of these defects may become easier to find as a result of the
additional overhead of the testing code.

Most professional software developers use C1 and C2 coverage. C1 stands for
statement coverage and C2 for branch or condition coverage. With a combination
of C1 and C2, it is possible to cover most statements in a code base.
Statement coverage would also cover function coverage with entry and exit,
loop, path, state flow, control flow and data flow coverage. With these
methods, it is possible to achieve nearly 100% code coverage in most software
projects.  [  17  ]

Test coverage is one consideration in the safety certification of avionics
equipment. The guidelines by which avionics gear is certified by the [ Federal
Aviation Administration ](/wiki/Federal_Aviation_Administration "Federal
Aviation Administration") (FAA) is documented in [ DO-178B ](/wiki/DO-178B
"DO-178B") [  16  ]  and [ DO-178C ](/wiki/DO-178C "DO-178C") .  [  18  ]

Test coverage is also a requirement in part 6 of the automotive safety
standard [ ISO 26262 ](/wiki/ISO_26262 "ISO 26262") _Road Vehicles -
Functional Safety_ .  [  19  ]

  1. ** ^  ** Brader, Larry; Hilliker, Howie; Wills, Alan (March 2, 2013). "Chapter 2 Unit Testing: Testing the Inside". [ _Testing for Continuous Delivery with Visual Studio 2012_ ](https://msdn.microsoft.com/en-us/library/jj159344.aspx) . Microsoft. p. 30. [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 978-1621140184  ](/wiki/Special:BookSources/978-1621140184 "Special:BookSources/978-1621140184") . Retrieved  16 June  2016  . 
  2. ** ^  ** [ Williams, Laurie ](/wiki/Laurie_Williams_\(software_engineer\) "Laurie Williams \(software engineer\)") ; Smith, Ben; Heckman, Sarah. [ "Test Coverage with EclEmma" ](https://web.archive.org/web/20160314023040/http://realsearchgroup.org/SEMaterials/tutorials/eclemma/) . _Open Seminar Software Engineering_ . North Carolina State University. Archived from [ the original ](http://realsearchgroup.org/SEMaterials/tutorials/eclemma) on 14 March 2016  . Retrieved  16 June  2016  . 
  3. ** ^  ** Joan C. Miller, Clifford J. Maloney (February 1963). [ "Systematic mistake analysis of digital computer programs" ](https://doi.org/10.1145%2F366246.366248) . _[ Communications of the ACM ](/wiki/Communications_of_the_ACM "Communications of the ACM") _ . **6** (2). New York, NY, USA: [ ACM ](/wiki/Association_for_Computing_Machinery "Association for Computing Machinery") : 58–63. [ doi ](/wiki/Doi_\(identifier\) "Doi \(identifier\)") :  [ 10.1145/366246.366248 ](https://doi.org/10.1145%2F366246.366248) . [ ISSN ](/wiki/ISSN_\(identifier\) "ISSN \(identifier\)") [ 0001-0782 ](https://search.worldcat.org/issn/0001-0782) . 
  4. ** ^  ** Paul Ammann, Jeff Offutt (2013). _Introduction to Software Testing_ . Cambridge University Press. 
  5. ** ^  ** Glenford J. Myers (2004). _The Art of Software Testing, 2nd edition_ . Wiley. [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 0-471-46912-2  ](/wiki/Special:BookSources/0-471-46912-2 "Special:BookSources/0-471-46912-2") . 
  6. ** ^  ** Position Paper CAST-10 (June 2002). _[ What is a "Decision" in Application of Modified Condition/Decision Coverage (MC/DC) and Decision Coverage (DC)? ](http://www.faa.gov/aircraft/air_cert/design_approvals/air_software/cast/cast_papers/media/cast-10.pdf) _
  7. ** ^  ** MathWorks. _[ Types of Model Coverage. ](http://www.mathworks.com/help/slvnv/ug/types-of-model-coverage.html) _
  8. ** ^  ** [ "Unit Testing with Parameter Value Coverage (PVC)" ](http://www.rhyous.com/2012/05/08/unit-testing-with-parameter-value-coverage-pvc/) . 
  9. ** ^  ** M. R. Woodward, M. A. Hennell, "On the relationship between two control-flow coverage criteria: all JJ-paths and MCDC", Information and Software Technology 48 (2006) pp. 433-440 
  10. ** ^  ** Ting Su, Ke Wu, Weikai Miao, Geguang Pu, Jifeng He, Yuting Chen, and Zhendong Su. "A Survey on Data-Flow Testing". ACM Comput. Surv. 50, 1, Article 5 (March 2017), 35 pages. 
  11. ** ^  ** ECSS-E-ST-40C: Space engineering - Software. ECSS Secretariat, ESA-ESTEC. March, 2009 
  12. ** ^  ** C. Prause, J. Werner, K. Hornig, S. Bosecker, M. Kuhrmann (2017): _[ Is 100% Test Coverage a Reasonable Requirement? Lessons Learned from a Space Software Project ](https://www.researchgate.net/profile/Marco_Kuhrmann/publication/319141355_Is_100_Test_Coverage_a_Reasonable_Requirement_Lessons_Learned_from_a_Space_Software_Project/links/599467faaca272ec9087f82a/Is-100-Test-Coverage-a-Reasonable-Requirement-Lessons-Learned-from-a-Space-Software-Project.pdf) _ . In: PROFES 2017. Springer. Last accessed: 2017-11-17 
  13. ** ^  ** Martin Fowler's blog: [ TestCoverage. ](https://martinfowler.com/bliki/TestCoverage.html) Last accessed: 2017-11-17 
  14. ** ^  ** Dorf, Richard C.: _Computers, Software Engineering, and Digital Devices_ , Chapter 12, pg. 15. CRC Press, 2006. [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 0-8493-7340-9 ](/wiki/Special:BookSources/0-8493-7340-9 "Special:BookSources/0-8493-7340-9") , [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 978-0-8493-7340-4 ](/wiki/Special:BookSources/978-0-8493-7340-4 "Special:BookSources/978-0-8493-7340-4") ; via [ Google Book Search ](https://books.google.com/books?id=jykvlTCoksMC&dq=%22infeasible+path%22+%22halting+problem%22&pg=PT386)
  15. ** ^  ** Y.N. Srikant; Priti Shankar (2002). _The Compiler Design Handbook: Optimizations and Machine Code Generation_ . CRC Press. p. 249. [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 978-1-4200-4057-9  ](/wiki/Special:BookSources/978-1-4200-4057-9 "Special:BookSources/978-1-4200-4057-9") . 
  16. ^  _**a** _ _**b** _ RTCA/ [ DO-178B ](/wiki/DO-178B "DO-178B") , _Software Considerations in Airborne Systems and Equipment Certification, Radio Technical Commission for Aeronautics,_ December 1, 1992 
  17. ** ^  ** Boris beizer (2009). _Software testing techniques, 2nd edition_ . Dreamtech press. [ ISBN ](/wiki/ISBN_\(identifier\) "ISBN \(identifier\)") [ 978-81-7722-260-9  ](/wiki/Special:BookSources/978-81-7722-260-9 "Special:BookSources/978-81-7722-260-9") . 
  18. ** ^  ** RTCA/ [ DO-178C ](/wiki/DO-178C "DO-178C") , _Software Considerations in Airborne Systems and Equipment Certification, Radio Technical Commission for Aeronautics,_ January, 2012. 
  19. ** ^  ** [ _ISO 26262-6:2011(en) Road vehicles -- Functional safety -- Part 6: Product development at the software level_ ](http://www.iso.org/iso/home/store/catalogue_tc/catalogue_detail.htm?csnumber=51362) . International Standardization Organization. 


-->

<!--






-->

<!--
In a previous post focused on the basics of test coverage, we talked about why
it’s an essential aspect of software testing to achieve these goals. This
time, we’ll be putting the spotlight on test coverage techniques and best
practices to ensure the best results. This may be accomplished by creating a
thorough test strategy that includes all levels of test coverage. [
](https://muuktest.com/blog/test-coverage-techniques/#In_Summary "In Summary")

##  **Achieving High Test Coverage**

Test coverage techniques are key to obtaining great results but need to be
included from the outset of the project. Understanding the application’s
requirements and use cases from the very beginning is also an important part
of the puzzle.

There are four primary areas to concentrate on in order to obtain high test
coverage:

  * Test Planning 
  * Test Design Techniques 
  * Test Execution 
  * Test Coverage Metrics 

Now let’s take a closer look into the different aspects to focus on during the
above phases.

**Identify Areas of Test Coverage:** Determine what aspects of your
application must be tested and evaluate all sorts of required tests. When
establishing the scope of what has to be tested, keep in mind the user’s
journey and the various flows inside the application.

**Write Unit Tests:** Start by creating automated unit tests for all
application functionality. Take advantage of code coverage tools to discover
any coverage gaps. If you’re not writing any unit tests, collaborate with the
development team to learn more about the ones that are already written and
ensure that they’re thorough enough.

**Use Modular Code:** Build programs with a modular architecture, breaking
complicated tasks down into small, loosely connected, reusable functions and
classes. This will facilitate unit testing.

**Employ Static Analysis:** Use static analysis tools to examine the code for
any flaws. This will assist to decrease the number of possible defects and
boost trust in the software’s quality.

**Improve Your Test Cases:** Determine what kind of tests will be conducted
and write complete test cases for each type of test. Look for scenarios that
may be difficult to test and devise techniques to make them simpler to test.

**Automate Test Execution:** Employ automation tools to speed up the process
and reduce manual effort. Automated test execution can also provide continuous
feedback on test coverage for improved visibility. Automate any manual testing
operations, such as data entry, configuration updates, and regression testing.
Automation will aid in ensuring that testing is carried out precisely and
consistently.

**Track Test Results:** Keep track of test results and utilize them to
discover areas for improvement. Resolve any difficulties that emerge and run
the tests again to confirm the findings.

**Review Test Coverage:** Keep an eye on the test coverage and compare it to
the required level. Consider what areas still need to be addressed and create
test cases for them. Examine the scope of the tests and any adjustments that
need to be made.

**Utilize Third-Party Tools:** Make use of third-party tools that are built to
automatically test web applications. This can save you time and effort, as
well as ensure that you’re testing your web application in a consistent
manner.

**Focus On Quality:** Spend time reworking legacy code and correcting problems
to guarantee a high degree of test coverage.

**Optimize** Test Cases: Optimize the test cases to ensure they are
comprehensive and efficient. Make sure the tests are well-structured and
regularly updated.

**Enable Continuous Integration:** Set up a continuous integration (CI)
system, such as [ Jenkins ](https://www.jenkins.io/) or [ Travis
](https://www.travis-ci.com/) , to guarantee that tests are executed during
development and on each deployment. Tests should be integrated into the
development process and included in your continuous integration and delivery
pipeline. This ensures that your apps have high-fidelity testing.

##  **Test Coverage Techniques**

**Select a Testing Strategy:** Determine the breadth of your test coverage and
the types of testing that will best accomplish the intended result. Consider
including testing for functional, regression, acceptability, unit, system,
load, and security.

**Prioritize test cases:** Prioritizing your test cases will assist you in
ensuring that the most essential tests are carried out first. Sort the test
cases according to their significance to the application. Begin with your
application’s most essential or frequently used features or situations, then
go to less crucial or edge cases.

**Test early and often:** Early and frequent testing helps you catch defects
early in the development cycle, which might help you detect bugs before they
become costly to fix.

**Collaborate with team members:** By working together, you may have a deeper
knowledge of the application’s behavior and how to test it successfully. Every
team member’s expertise is significant, and each team member may add to the
application’s greater test coverage.

**Continuously evaluate and modify test coverage:** As your application
evolves, it’s critical to regularly evaluate and adapt test coverage. This
will assist you in ensuring the application has been adequately tested. So
keep in mind that this is a continual process, and you should constantly
assess and adapt tests.

**Use Automation wisely:** Automated tests can assist minimize the amount of
manual testing required and can remove boring and repeated tests. Automated
tests also give higher coverage since they can cover corner cases, edge
situations, and all variants of scenarios that would take too long to test
manually.

**Ensure Adequate Test Data:** Adequate test data is required for successful
test coverage. Tests may overlook crucial cases or fail in unexpected ways if
the correct data is not available.

**Invest in Test Design:** The quality of test coverage is determined by test
design. Time should be spent to ensure that tests cover all possible
scenarios, including corner cases, edge cases, and scenarios with varied data.
Experimenting with various test methodologies, technologies, and approaches
can help discover coverage gaps and generate new ideas for improving test
coverage.

**Think Defensively:** Test coverage should extend beyond a system’s
functional needs to search for potential failure from external sources.
Defensive testing should include security, performance, and scalability.

**Track Test Coverage:** Keep track of which test cases have been completed
and which still need to be tested. This will aid in identifying coverage gaps
and ensuring that all chunks of the application are tested.

**Review and Analyze Results:** Once the tests have been completed, go over
the findings and look for defects or places where coverage might be increased.
Defects speak a lot about test coverage.

**Monitor Code Changes:** Keep track of code changes and create test cases to
cover new code when it’s added or modified.

##  **Best Practices for Improving Your Test Coverage**

Now we’ll go through some excellent practices for increasing test coverage.
Unit testing approaches, integrated testing strategies, and regression testing
methods will be covered. By adhering to these best practices, you can verify
that your code has been fully tested and that any modifications made have been
thoroughly tested before being deployed into production.

  * Define clear objectives and goals 
  * Identify critical areas for testing 
  * Use a combination of testing methods 
  * Continuously monitor and evaluate test coverage 
  * Update test cases regularly 
  * Test coverage is a team effort 
  * Implement a code coverage tool 

##  **In Summary**

Test coverage may appear to be a simple concept, yet it plays a critical role
in the quality of your product. Implementing the concepts and approaches
mentioned in this article will undoubtedly result in optimal test coverage.
Try to do research and learn more about your product/system’s behavior, which
can help you achieve high test coverage.


-->

<!--






-->

<!--
Building software is helpful, but it is also prone to many errors. Software
that has poor design doesn’t just ruin the user experience but also causes
many functional problems along the way. The [ Consortium for Information &
Software Quality (CISQ) report ](https://www.it-
cisq.org/pdf/CPSQ-2020-report.pdf "CISQ Report 2020") indicates that poor-
quality software costs about $2.08 trillion in the US alone.

It is crucial to build useful products and test them using a solid testing
strategy for good test coverage. It helps benchmark the health of a product.
Different test coverage techniques help in developing a testing strategy. In
this guide, you’ll learn about the different test coverage techniques that
every tester must know.

###  What does Test Coverage mean?

Test coverage defines what percentage of application code is tested and
whether the test cases cover all the code. It is calculated as

![Test Coverage Formula](https://www.browserstack.com/guide/test-coverage-
techniques) ![Test Coverage
Formula](https://browserstack.wpenginepowered.com/wp-
content/uploads/2022/05/1-What-is-Test-Coverage-.png)

For example, if you have 10,000 lines of code, your test cases should be able
to test the entire codebase. If only 5,000 lines of code are tested out of
10,000, the coverage is 50%.

###  Test Coverage vs. Code Coverage

Code coverage is a metric related to [ unit testing
](https://www.browserstack.com/guide/unit-testing-best-practices "Best
Practices for Unit Testing") . It measures the percentage of lines and
execution paths in the code covered by at least one test case. It only
measures how thoroughly the unit tests cover the existing code. Test coverage
is a job for the QA developers and testers who measure how well an application
is tested.

###  Benefits of Test Coverage

Before learning about the different types of testing coverage techniques,
let’s look at the benefits of testing your application early and defining your
test coverage.

  * **Early Detection:** It helps to detect any errors in your application at the initial stages of software development. Identifying gaps in the requirements and test cases can save a lot of time and effort in the future. 
  * **Eliminate Redundancy:** It is unnecessary to consider all test cases sometimes. Developers can identify such redundant cases and report them to make the code lighter. 
  * **Fewer Resources:** Better test coverage means fewer defects in production and user acceptance testing defects. This translates to fewer resources allocated for testing. 
  * **Smoother Testing Cycles:** Test coverage helps [ optimize regression tests ](https://www.browserstack.com/guide/regression-testing "Regression Testing: A Detailed Guide") , test case prioritization, test suite augmentation, and test suite minimization. All these, in turn, help in a smoother and more efficient [ software development life cycle ](https://www.browserstack.com/guide/learn-software-development-process "Understanding Software Development Process") . 

###  Test Coverage Techniques

Test coverage techniques help you track the quality of your tests and cover
the areas that are not validated yet. Some popular techniques are

  1. **Product coverage** which tells us how much of a product is covered 
  2. **Risk coverage** informs us about the risks in an application 
  3. **Requirements coverage** track how many of the requirements are met successfully 
  4. **Compatibility coverage** checks the compatibility across multiple browsers and devices 
  5. **Boundary value coverage** checks the tests around the minimum and maximum boundary values 
  6. **Branch coverage** checks the percentage of branches or decision points in the code that are executed 

**![Different Test Coverage
Techniques](https://www.browserstack.com/guide/test-coverage-techniques)
![Different Test Coverage
Techniques](https://browserstack.wpenginepowered.com/wp-
content/uploads/2023/05/Different-Test-Coverage-Techniques.png) **

####  1\. Product Coverage

Product coverage tells us which parts of a product are tested. Say there is a
counter that is to be tested. A counter is a simple application that can
either increment or decrement a number, similar to adding items to a shopping
cart. The operations of the counter have to be tested i.e. incrementing and
decrementing the counter. But there may be other factors that need to be
tested. For example, should the counter handle negative numbers?

Product coverage can be increased by prioritizing requirements, preparing a
checklist of testing requirements, and [ implementing effective test
automation ](https://www.browserstack.com/guide/effective-test-automation-
strategy "Key Elements of an Effective Test Automation Strategy") to reduce
testing times. Several cloud-based test automation tools like [ BrowserStack
](https://www.browserstack.com/live "Cross browser testing on desktop &
mobile") allow users to set up their website for testing in a few simple
steps.

A product with good product coverage verifies every possible scenario like the
ones described above.

####  2\. Risk Coverage

This test coverage technique helps to assess the risks related to the
application and tests them thoroughly.

![Software Testing Prioritization in Test
Coverage](https://www.browserstack.com/guide/test-coverage-techniques)
![Software Testing Prioritization in Test
Coverage](https://browserstack.wpenginepowered.com/wp-
content/uploads/2023/05/Software-Testing-Prioritization-in-Test-
Coverage-700x705.png) The above image gives us an estimate of what must be
tested and how critical it is. It shows the probability of something happening
and the (negative) business impact it would have. Based on this, four zones
have been defined:

  * **Very likely scenario with high impact** – It must be tested 
  * **Unlikely scenario with high impact** – It should be tested 
  * **Very likely scenario with low impact** – It could be tested if there is time 
  * **Unlikely scenario with low impact** – the test is too expensive for the value it provides, so testing is not required 

Say there is an application that depends on a third-party API. There is a risk
here of the API going offline. Analyzing how the application should work in
such a case is what risk coverage is all about.

If you want to say that your application is covered, all of its [ relevant
risks should be listed ](https://www.browserstack.com/guide/risk-based-
testing-in-agile "What is risk-based testing in agile?") and answer the
questions they elicit.

####  3\. Requirements Coverage

![Requirements Coverage](https://www.browserstack.com/guide/test-coverage-
techniques) ![Requirements
Coverage](https://browserstack.wpenginepowered.com/wp-
content/uploads/2022/05/4-Requirements-Coverage.png)

Requirements coverage is the most basic and essential test coverage technique
that helps assess if it meets the user’s requirements. It is simply a way of
testing whether the required functionalities exist or not. If the software has
promised certain deliveries, these promises must be met using this technique.

####  4\. Compatibility Coverage

[ Device fragmentation ](https://www.browserstack.com/blog/understanding-
browser-os-and-device-fragmentation/ "Testing for Fragmentation: Understanding
Browser, OS and Device Fragmentation") is an exceptionally huge problem that
many firms can run into because it can cause [ compatibility issues
](https://www.browserstack.com/guide/common-cross-browser-compatibility-issues
"Cross Browser compatibility issues") and hamper a product’s user experience.
There are _9000+ devices, 8 browsers, and 21 operating systems_ available
today. Testing across all combinations of device-browser-OS is a mammoth task.
The compatibility test coverage technique ensures that the application is
compatible across browsers and operating systems.

![Test Coverage Techniques of Compatibility
Testing](https://www.browserstack.com/guide/test-coverage-techniques) ![Test
Coverage Techniques of Compatibility
Testing](https://browserstack.wpenginepowered.com/wp-
content/uploads/2023/05/Test-Coverage-Techniques-of-Compatibility-
Testing-700x330.png) There are different categories of compatibility testing,
such as:

  * **Browser Testing:** Testing across browsers provides helpful information about how the application works across different browsers. [ BrowserStack Live ](https://www.browserstack.com/live "Cross browser testing on desktop & mobile") provides 3000+ browsers and devices to test an application ensuring that you don’t miss out on your user’s preferred browser-device-OS combinations. [ **_Try for Free_ ** ](/users/sign_up) . 
  * **Hardware Testing:** The application is tested with different hardware configurations. 
  * **Software compatibility** : This involves testing the software with other software. An example would be testing Microsoft Word compatibility with Microsoft Outlook. 
  * **Network testing:** Assess the performance of an application in [ different network conditions ](https://www.browserstack.com/guide/how-to-simulate-slow-network-conditions "How to simulate slow network conditions for app testing \(Android and iOS\)") like 3G,4G, and Wi-Fi. 
  * **Mobile testing:** It involves testing websites across different mobile devices and platforms like Android or iOS. 

####  5\. Boundary Value Coverage

Boundary Value Coverage is a testing technique that focuses on testing the
boundaries and extreme values of input conditions. The idea behind this
technique is that errors are more likely to occur at the edges of input ranges
rather than within the normal range. By testing the boundary values, you can
identify potential issues related to data handling, validation, and boundary
conditions.

The Boundary Value Coverage technique involves selecting test cases that fall
on or near the boundaries of input ranges. It typically includes four
categories of values:

  * **Lower Boundaries:** Test cases where inputs have the minimum valid value or just below it. This helps identify issues related to handling the lower limits and boundary conditions. 
  * **Upper Boundaries:** Test cases where inputs have the maximum valid value or just above it. This helps identify issues related to handling the upper limits and boundary conditions. 
  * **Within Boundaries:** Test cases where inputs fall within the valid range but are not at the extremes. This ensures that the system behaves correctly for typical inputs and helps verify the functionality and behavior within the normal range. 
  * **Invalid Boundaries:** Test cases where inputs are just outside the valid range or have invalid values. This helps identify how the system handles invalid inputs, such as error messages, validation checks, or graceful degradation. 

The number of test cases required for boundary value coverage can vary based
on factors like the complexity of the system, input ranges, and specific
requirements. However, a common approach is to select test cases for the
minimum valid value, just below the minimum, the maximum valid value, and just
above the maximum for each input.

By applying Boundary Value Coverage in testing, you can increase the
likelihood of detecting issues related to boundary conditions, constraints,
and data handling, ultimately improving the quality and reliability of your
software.

####  6\. Branch Coverage

Branch coverage is a software testing metric that measures the percentage of
branches or decision points in the code that have been executed during
testing. A branch represents a point in the code where the program can take
different paths based on a condition or a decision.

Branch coverage aims to ensure that all possible paths and outcomes within the
code are tested. It helps identify areas of the code that have not been
exercised, potentially indicating untested logic or potential bugs. The goal
is to achieve high branch coverage to increase confidence in the reliability
and correctness of the software.

To calculate branch coverage, the testing process needs to track which
branches have been taken during execution. This can be achieved using
techniques such as code instrumentation, where the code is modified to log
information about executed branches, or using specialized testing tools that
can track code coverage.

Branch coverage is typically reported as a percentage, representing the ratio
of executed branches to the total number of branches in the code. For example,
if a code section has 10 branches and during testing, 8 branches are executed,
the branch coverage would be 80%.

**Making the most out of Test Coverage Techniques**

To build stable products, deciding on a test strategy is essential. A [ strong
test strategy ](https://www.browserstack.com/guide/software-testing-
strategies-and-approaches "Software Testing Strategies and Approaches") will
help provide maximum test coverage for the code. The test strategy involves
using the different test coverage techniques mentioned above. Although each
technique has its own unique benefits, the QA team must decide and take the
final call.

[ Let Your QA Team Run Trial Tests on Real Device Cloud
](https://www.browserstack.com/users/sign_up "Create A Free BrowserStack
Account")

With [ proper test planning ](https://www.browserstack.com/guide/test-planning
"Test Planning: A Detailed Guide") , they can understand the features, risks,
compatibility issues, and product requirements. Nowadays, test strategy
techniques use AI with self-correcting [ test cases
](https://www.browserstack.com/guide/writing-good-test-cases "Fundamentals of
Writing Good Test Cases") that learn from previous executions and improve upon
them, significantly reducing test maintenance.

It is not easy to define a strong [ testing strategy for any application
](https://www.browserstack.com/guide/mobile-app-testing-strategies "Mobile app
testing strategy") . But if done well, it greatly benefits the business and
reduces the team efforts in the long run. They help track the progress and
quality of your testing and help the business catch defects early on and
decide which tests to perform and which to avoid. These test coverage
techniques cover the various aspects involved in testing a product and help
build an overall concrete testing strategy.


-->

<!--






-->

<!--
#  How to Ensure 100% Test Case Coverage of Requirements

How to Ensure 100% Test Case Coverage of Requirements

Creating comprehensive test scenarios and cases that ensure 100% coverage of
requirements is a multi-faceted process involving several key strategies.

> The objective is to make sure that every aspect of a software requirement is
> thoroughly tested, including positive, negative, and edge cases.

Letâ€™s delve into a structured approach to achieve this, illustrated with an
example and supported by insights from industry sources.

##  1\. Understanding the Requirements

Begin by clearly understanding the software requirement. For instance, if the
requirement is for a user authentication system, it should include details
like

  * _accepting username and password,_
  * _validating credentials,_
  * _handling incorrect inputs, etc._

##  2\. Developing User Personas

Creating user personas helps envision how different users might interact with
the software. This step is crucial in developing relevant test scenarios and
cases.

For our example, personas might include

  * **a first-time user,**
  * **a returning user with correct credentials,**
  * **a user who has forgotten their password.**

##  3\. Identifying Test Scenarios

Test scenarios are high-level ideas about what to test. For the authentication
system, scenarios could include:

  * _Successful login_
  * _Login with incorrect credentials_
  * _Login with empty credentials_
  * _Password recovery process_

##  4\. Outlining Test Cases

Test cases are specific actions to be performed in testing. For each scenario,
develop test cases covering positive, negative, and edge cases.

For example:

  * **_Positive Test Case 1_ ** _: Enter valid username and password > Expect successful login. _
  * **_Negative Test Case 1_ ** _: Enter invalid username > Expect error message. _
  * **_Negative Test Case 2_ ** _: Enter invalid password > Expect error message. _
  * **_Edge Case 1_ ** _: Enter maximum length allowed for username and password > Expect successful login or appropriate error message. _
  * **_Edge Case 2_ ** _: Leave username and password fields empty > Expect error message. _
  * **_Edge Case 3_ ** _: Exceed the limits of characters allowed for username and password fields > Expect error message. _

##  5\. Incorporating Different Coverage Metrics

Use various coverage metrics like statement coverage, branch coverage, and
path coverage. These metrics ensure different aspects of code and
functionalities are tested.

_Ensuring every line of code in the login functionality is executed at least
once._

_Testing all branches of conditional logic in the login process._

It focuses on ensuring that each possible branch from each decision point in
the code is executed at least once. This type of coverage is crucial for
testing the decision-making logic of an application.

In the login process, consider the following decision points:

**Username and Password Validation:**

  * _If both fields are filled, proceed to credential verification._
  * _If either field is empty, display an error message._

**Credential Verification:**

  * _If the username and password combination is correct, proceed to successful login._
  * _If the combination is incorrect, display an error message._

In branch coverage, you would create test cases to cover each of these
decision branches:

**Test cases for Username and Password validation**

  * _Enter both username and password > Expect the system to proceed to credential verification. _
  * _Enter only username or password > Expect an error message. _

**Test cases for credential verification**

  * _Enter valid username and password > Expect successful login and redirection. _
  * _Enter invalid username or password > Expect an error message. _

Branch coverage ensures that all the decision branches in the code are tested,
but it does not necessarily cover all possible paths as path coverage does.
For example, it might not cover the scenario where both the username and
password fields are empty, as this would be a specific path rather than a
decision branch.

While branch coverage is less comprehensive than path coverage, it is more
focused and often more feasible for large applications where testing every
possible path can be impractical. Branch coverage is particularly useful for
ensuring the robustness of the applicationâ€™s logic and can significantly
reduce the number of bugs related to decision-making processes.

Testing all possible paths in the login process, including different sequences
of user actions.

Letâ€™s take the example of a login process to illustrate path coverage.
Assume the login process involves entering a username and password, and it has
the following logical components:

  1. _Input validation that hecks if the username and password fields are filled._
  2. _Credential verification which verifies if the username and password combination is correct._
  3. _Error handling which displays appropriate error messages._
  4. _Successful login that redirects to the homepage upon successful login._

Now, consider the following paths:

**Path 1. Successful Login**

  * _User enters the correct username and password._
  * _The system verifies credentials._
  * _The user is redirected to the homepage._

**Path 2. Incorrect Credentials**

  * _User enters incorrect username or password._
  * _The system checks credentials and finds a mismatch._
  * _An error message is displayed._

**Path 3. Missing Username**

  * _User enters a password but leaves the username blank._
  * _The input validation fails._
  * _An error message for missing username is displayed._

**Path 4. Missing Password**

  * _User enters a username but leaves the password blank._
  * _The input validation fails._
  * _An error message for missing password is displayed._

**Path 5. Both Fields Empty**

  * _User does not enter username or password._
  * _The input validation fails._
  * _An error message for missing credentials is displayed._

In path coverage testing, each of these paths would be executed at least once.
This helps to ensure that all possible scenarios, including edge cases, are
tested, thereby increasing the likelihood of identifying potential bugs or
issues in the login process.

##  6\. Requirement-Based Coverage

Align test cases with the softwareâ€™s requirements to ensure that all
functionalities and components outlined in the Software Requirement
Specification (SRS) are covered.

##  7\. Risk-Based Coverage

Prioritize testing based on the risk analysis. High-risk areas, like security
aspects of the login system, should be given more attention.

##  8\. Boundary and Equivalence Testing

Test the boundaries and equivalence classes of input data. For example, **test
the minimum and maximum lengths of username and password fields.**

##  9\. Error Guessing

Use expertise and intuition to guess potential error-prone areas.

##  10\. Using Test Case Management Tools

Use tools like [ TestCaseLab ](https://bit.ly/3HZv4g1) for managing and
organizing test cases. This aids in tracking progress, identifying gaps, and
ensuring all test cases are up to date and aligned with current requirements.

##  11\. Regular Review and Updates

Regularly review and update test cases to accommodate changes in requirements
and feedback from testing results. This is vital in agile environments where
requirements may evolve.

##  12\. Monitoring and Tracking

Monitor all test cases to avoid duplications and ensure comprehensive
coverage. Use metrics and feedback to refine the testing process continuously.


-->

<!--






-->

<!--
OVERVIEW

Test coverage is a black-box testing method that entails testing elements
included in the functional requirements specification, software requirements
specification, and other required documents. Since the tests are derived from
these documents, there is minimal or no chance of automation.

For example, say you want to perform [ cross browser testing
](https://www.lambdatest.com/) on your web application to see if it renders
properly in different browsers and operating systems. Your test coverage would
be about equal to the number of browser + OS combinations for which you have
tested your web application's browser compatibility.

Test coverage is a crucial software testing metric that determines the code
covered during the test runs. In other words, it is used for evaluating the [
test execution ](https://www.lambdatest.com/learning-hub/test-execution)
coverage in the software application.

It is a type of [ black box testing ](https://www.lambdatest.com/learning-
hub/black-box-testing) methodology where test cases are written in a manner
that provides maximum coverage of requirements stated in the requirement
specification document. Since the tests are derived from these documents,
there is minimal or no chance of automation.

Test coverage involves validating the features implemented as a part of your
requirements documentation, such as the functional requirements specification
and software requirements specification.

If you have to perform [ cross browser testing ](https://www.lambdatest.com/)
to ensure that your web application renders well from different browsers, you
would be covering many browsers and operating systems.

To calculate test coverage, you can divide the number of lines covered by a
test by the total number of lines in your applicationâ€™s test code.

**Test coverage = line of code covered by test*100/total lines of code**

Besides, we have code coverage as well. These two terminologies are sometimes
confusing for both testing teams and development teams. Test and code coverage
are two of the most popular methodologies for evaluating code effectiveness.
These terms are sometimes used interchangeably due to their similar underlying
principles. However, they are different from what you might think. To know
more about how test and code coverage differs from each other, read our
article on [ code coverage vs. test coverage
](https://www.lambdatest.com/blog/code-coverage-vs-test-coverage/) .or can
also read [ What is code coverage? ](https://www.lambdatest.com/software-
testing-questions/what-is-code-coverage)

##  What is the purpose of Test Coverage?

Test coverage acts as an indirect quality check method as it helps identify a
quantitative measure of how much code you cover. A secondary purpose of it is
the creation of additional test cases that further helps in increasing
coverage.

Additionally, it helps identify gaps in test cases and requirements.
Therefore, testers can spot defects early in the [ software testing life cycle
(STLC) ](https://www.lambdatest.com/blog/software-testing-life-cycle/) . It
eliminates a lot of grunt work that testers would have had to do at a later
stage. Indirectly, this leads to a fine end product, further enhancing
customer satisfaction.

Test coverage helps in removing test cases of low to no relevance to the
current project. In other words, when a developer reports an unnecessary test
case, the overall code becomes lighter. On the other hand, it also helps
discover some portions of software that a test case might not have covered. As
a result, your program becomes error-free and more robust. With extensive data
available on different coverage items, coverage access increases with better
testing effectiveness.

##  Benefits of Test Coverage

In this section, we will cover some striking benefits of test coverage and why
every tester should care about it. Otherwise, why bother learning the metrics,
techniques, and steps to enhance it if you don't even know how beneficial it
is?

  * **Kills the bug:** It helps terminate the bugs & defects of the code in its early stages. This way, the testers donâ€™t need to spend their time and resources hunting for the bugs right before the product delivery when the complexity of the code has risen. A direct impact of this course of action is the reduction in the utility of resources increases the ROI and, in turn, the net profits. 
  * **Eradicates redundancy:** Redundancy can be annoying and savage on time & money simultaneously. It can worsen the complexity of code and hinder its overall framework. Test coverage helps developers identify redundant cases and report them to make their code lighter. 
  * **Expands testing scope:** When you focus on something, it improves. Similarly, implementing test coverage on the software product widens the testing range. And successively, with a broader scope, the efficiency of testing increases, with better traceability and identification of defects in the test cases. 
  * **Improve quality:** With a higher likelihood of detection of bugs & defects, test coverage provides indirect quality assurance. It also appends extra test cases. These cases ultimately lead to improvement in quality. On top of that, it acts as a reliable source of information for clients and stakeholders. 
  * **Streamline testing cycle:** The software development life cycle is a tricky process. Test coverage helps unravel the complexity of this process while determining ways to fix defect and [ regression test ](https://www.lambdatest.com/learning-hub/regression-testing) leakages effortlessly. 

##  Types of Test Coverage

For test coverage, there are four primary techniques.

This classification is based on the facets of the application prioritized in
the coverage.

  * **Product coverage:** This technique revolves around the user's perspective. It involves test cases that examine every possible entry-exit outcome of the product. In simpler words, product coverage deals with the if-then-else statement chart and related conditions. 

In turn, this process leads to the determination of the scope of the
application. Practices like checklists, priority charts, automation, etc., can
extend the range of practice coverage.

  * **Risk coverage:** It incorporates the analysis of all the inherent risks in the product. Measures like risk enlistment, likelihood, and threat are covered through this technique. This can be the most critical coverage technique for applications more prone to impactful risks. Risk coverage assures the stakeholders about the proper risk & regression management. 
  * **Requirement coverage:** The requirement coverage technique focuses on the application product's essential aspectâ€” meeting the requirements. No matter how well built, examined, and secured the product is, itâ€™s just foolâ€™s gold if it doesnâ€™t meet the functional needs it is built for. This is arguably the broadest coverage technique as it ensures the demand fulfillment facet of each component and, thus, comprises a plethora of test cases. 

Requirement coverage is implemented from a combination of the user's and
developerâ€™s perspectives. It is the fundamental process for every software
product, regardless of its genre, complexity, or approach. This technique also
involves the coverage metrics like implementation rate, case-requirement
analysis, etc.

  * **Compatibility coverage:** This class of coverage techniques measures the application's compatibility range across different platforms, browsers, and operating systems. 

It involves test cases that meet the requirements for testing the productâ€™s
cross-platform performance. However, with such a broad spectrum of platforms,
you must avoid redundancy in the testing pattern. The test coverage may only
include the prominent and more usable platforms depending on the availability
of time and resources.

To test your compatibility coverage, one can use cloud-based cross browser
testing platforms like LambdaTest to their websites and mobile apps on an [
online browser farm ](https://www.lambdatest.com/online-browser-farm) and [
device farm ](https://www.lambdatest.com/online-device-farm) of 3000+ real
browsers, devices, and OS combinations. With its [ real device cloud
](https://www.lambdatest.com/real-device-cloud) , you can [ test use cases
](https://www.lambdatest.com/learning-hub/use-case-testing) in real-world
environments and get accurate results.

Subscribe to the [ LambdaTest YouTube channel
](https://www.youtube.com/c/LambdaTest?sub_confirmation=1) for software
testing tutorials around [ Selenium testing
](https://www.lambdatest.com/selenium-automation) , [ Playwright browser
testing ](https://www.lambdatest.com/blog/playwright-framework/) , [ Appium
automation ](https://www.lambdatest.com/appium) , and more.

  * **AI automation coverage:** Going by its name, this coverage technique relies entirely on AI automation instead of manual enlistment, arrangement, etc. Considering the recent development of Artificial Intelligence at the functional level, this is a high but reasonably cost coverage technique. 

However, the outcome of utilizing AI-aided automation tools is visible in the
performance and output. The process becomes incredibly effortless yet high-
quality. Powered by AI, the test coverage keeps improving for the entirety of
its life.

Test coverage techniques are undoubtedly intricate. And so is the information
they comprehend. Thus, testers need to understand and implement them very
cautiously.

##  Test Coverage Metrics

For a document comprising assessable data, nothing is more important than
metrics (along with its presentation). Test coverage metrics are the hub of
all numeric information and formulae relevant to the application code and the
testing process.

Based on the grounds of functionality, metrics can be classified into three
major categories: Code testing, data testing, and [ application testing
](https://www.lambdatest.com/mobile-app-testing) metrics.

  * **Code testing metrics:** The test implementation rate is one of the simplest code-level metrics. This is a piece of crucial information concerning the progress of testing. 

The basic formula for the test implementation rate is,

**â€˜Number of tests executed*100/Number of tests planned to be executedâ€™.**

The metric is easy to present but needs more critical information about the
project's quality and complexity.

  * **Data testing metrics:** This class of coverage metrics involves dynamic information that relates testing conditions with the application's components. With changes in test cases and components, you can utilize this castable data for the effect that the change brings. It encompasses metrics like requirement attainment rate, case-requirement table, etc. 

The requirement coverage rate also has a basic formula,

**'Number of requirements attained*100/Total number of reqirementsâ€™.**

On the other hand, case-coverage analysis is a tabular statistic that exhibits
testing conditions of respective features along with the result of testing. It
is arguably the most crucial statistic, especially from the approversâ€™ point
of view.

  * **Application testing metrics:** The most holistic aspect of coverage metrics is the data relevant at the application level. This category of statistics is more rigid and of little use when dealing with test cases. Details like defect density, unfinished coverage study, etc., are a part of application testing metrics. 

Defect density, with a simple formulaâ€” number of defects detected/size of
the application is a dynamic yet essential piece of information. Not only does
it help realize the requirement of retesting, but it also gives an idea about
the necessity of automation in different test cases. It is the most dependable
source of information to base the position of defect elimination/testing on
the priority list.

The unfinished coverage study is the direct counterpart of the case-
requirement study. It contains the test cases yet to be matched with the
instructed requirements and the current status of the process. Some other
similar metrics that may be relevant to the testing approach and project
requirements are defects for requirement, testing per defect, etc.

[ ![...](https://www.lambdatest.com/resources/images/infra.png)
](https://accounts.lambdatest.com/register)

##  How to enhance Test Coverage?

The difference between average and impressive coverage is small but crucial.
To upgrade the level of coverage, testers need to sincerely keep a few
practices in mind.

Following are the practices that will ensure better quality coverage for every
individual claiming involvement in the productâ€™s development & delivery:

  * **Assemble Information:** Documentation of literally any comprehensive data asks for research. It is essential to thoroughly research the product, testing requirements, and every other factor that takes part in its development. 

Testers, engineers, and developers must have information like the market share
of the product, competitors, general trends & data of the users, etc. It is
equally important to document this data systematically. You can use visual
data representation methods like tables, pie charts, and venn diagrams.

  * **Assess Compatibility:** After gathering complete information about the product, testers should analyze the compatibility aspect of the project. For enhanced coverage, it is essential to assign specific testing devices for particular platform compatibility testing in the correct category. 

These categories can include:

    * Devices commonly used by relevant customers. 
    * Popular devices developed long ago. They give an idea about compatibility in bygone processing conditions. 
    * Devices with early access to platforms and OS. They allow proper testing time for engineers before the operating system becomes relevant. 
    * Devices gaining consistent attraction in the market and emerging to attain the commercially prior category. 
  * **Arrange Environment:** Attaining the apt testing environment is very crucial. An essential measure in the testing process is the imitation of consumer-friendly ambiance. Components like domestic WiFi connectivity, CPUs, drivers, RAM/ROM, etc., must be duly incorporated into the [ testing environment ](https://www.lambdatest.com/blog/what-is-test-environment/) . 

Even the subtlest factors, for instance, the applicationâ€™s performance in
portrait and landscape mode, must be scrutinized. According to a few experts,
testing in natural user ambiance is the game-changing factor in coverage
enhancement.

  * **Analyze combinations:** Now that the research, compatibility, and environment are sorted, it is time to execute the test cases on various devices. To ensure higher productivity, it is essential to select the right combination. You must choose a few devices from every class categorized on priority, performance, and compatibility. 

##  How to expand Test Coverage in a shorter interval?

Efficiency is the key. The only thing better than completing a task is doing
it quickly. Here are some factors that can help expand the coverage of your
tests in a short interval:

  * **Maintain checklists:** Checklists are handy and practical. Maintaining a checklist can help in keeping track of progress. 
  * **Prioritize carefully:** Prioritizing test cases significantly saves time and resources. Testers should categorize test components and risks into the major, minor, and rejectable. 
  * **Simplify data:** The data processed from the research must be short and meaningful. Use logical or visual descriptions during documentation. 
  * **Analyze initial impacts:** Examining the defects and bugs in the early stages is a vital aspect of coverage. This method saves time & redundancy while also preventing dealing with the code in its complex final stages. 
  * **Integrate prioritization with compatibility:** Perform cross-platform testing only on test cases higher on the priority chart while approving the fewer prior ones through a single browser, OS, etc. 

##  How to use Automation to increase Test Coverage?

To systematically incorporate automation into the test coverage to improve its
quality and accuracy, testers need to pre-define a specific procedure.
Following is a detailed description to get an idea of the procedure.

  * **Identify the testing components with automation requirements:** To do this, analyze their positioning on the priority list, risk likelihood, and importance in the application code. 
  * **Choose the relevant testing tool:** Examine the suitability, features, flexibility, and, most importantly, the cost of the [ test tool ](https://www.lambdatest.com/learning-hub/test-tool) . 
  * **Employ experienced or skillful individuals to script the tool:** Ensure their understanding of the product and the tool. 
  * **Construct systematic and high-quality data:** To ensure better performance of the [ test execution tool ](https://www.lambdatest.com/learning-hub/test-execution-tool) , ensure that the data and the data source are compatible and readable by the AI. If possible, utilize data generator software. 
  * **Stability of test tool:** If the application is likely to change/update, ensure that the test tool remains unaffected. 

Furthermore, itâ€™s always wise to run automated tests on automation testing
platforms like LambdaTest to cut your in-house testing costs. LambdaTest
provides a cloud-based scalable [ test infrastructure
](https://www.lambdatest.com/learning-hub/test-infrastructure) that will
exponentially increase your browser coverage by running your test scripts on a
cloud of 3000+ desktop and mobile environments.

##  Test Coverage Best Practices

Testers must follow some commonly recommended practices to achieve the quality
threshold. These may differ with differences in the application genre,
priorities, requirements, etc. However, understanding the basic idea will
likely affect the coverage positively. Some healthy practices include:

  * **Keep updates in mind:** A factor that often slips from testers' minds is that the coverage must have a scope that incorporates the updates/changes the product will undergo. The advisable coverage limit to effortlessly acknowledge changes is 90%. 
  * **Quality is better than quantity:** Quality has always had the edge over quantity. Even from the stakeholders' perspective, the prime concern is eradicating bugs, defects, and regression from high-priority & risk-prone components. Executing a well-thought test coverage on a few high-priority test components is preferable to having a broad and hazy scope of the coverage. 
  * **Say no to redundancy:** Useless data duplication is more damaging than it seems. Not only does it squander resources, but it also decreases the overall quality of the coverage directly or indirectly. Moreover, the duplication of [ test suites ](https://www.lambdatest.com/learning-hub/test-suite) makes it rather strenuous to identify and eliminate defects from the code. 
  * **Perform multi-degree testing:** Implementing test cases at every level of the code is crucial. The three testing levels are: 
    * [ Unit testing ](https://www.lambdatest.com/learning-hub/unit-testing) \- Executed on the smallest testable unit of the code. This elaborate testing pattern ensures the absence of bugs and defects in every code component. 
    * [ Integration testing ](https://www.lambdatest.com/learning-hub/integration-testing) \- Examines smooth networking between the different modules inspected in unit testing. 
    * [ System testing ](https://www.lambdatest.com/learning-hub/system-testing) \- The final testing level executes the approach to the overall software product. In simpler words, it is an end-to-end testing pattern that ensures that the final product runs smoothly, even in the user environment. 
  * **Automation is essential:** Even for its high cost, automation, to whichever extent it is affordable, is critical. AI automation is a must-have, especially for high-priority test cases that demand accuracy. 

[ ![...](https://www.lambdatest.com/resources/images/legacy.png)
](https://accounts.lambdatest.com/register)

##  Conclusion

Now that we understand the role test coverage plays in measuring and ensuring
quality software, it's time for implementation. We hope that this
comprehensive guide and the best practices inspire businesses to put these to
good use.

##  Frequently Asked Questions (FAQs)

##  How do we measure test coverage?

To calculate coverage of your tests, divide the total number of lines in a
software application by the number of lines covered by each test.

##  What is good test coverage?

According to the consensus, 80% coverage is a good target. Reaching a higher
coverage level might be expensive while not producing enough benefits.

##  What is test coverage in software testing?

Test coverage in software testing refers to the extent to which a software
application or system has been tested. It measures the percentage of code or
functionalities covered by test cases, ensuring that all critical aspects of
the software are tested.

##  How to measure test coverage?

Test coverage can be measured by using code coverage tools that track which
parts of the code are executed during testing. These tools generate reports
showing the percentage of code covered, helping identify areas that require
additional testing and improving overall testing effectiveness.

##  How to improve test coverage?

To improve test coverage: 1. Identify and prioritize test scenarios based on
the requirements analysis, 2. Use a combination of testing techniques and
tools, 3. Perform risk-based and exploratory testing, 4. Enhance test cases
based on feedback and lessons learned, 5. Leverage test automation for
efficient and extensive testing, 6. Collaborate with stakeholders and track
test coverage metrics.

##  What is test coverage in manual testing?

Test coverage in manual testing means how much of the application's
functionality and code is covered by the tests performed manually. It helps
determine how well the manual testing process ensures that all important parts
of the application are tested and working correctly.

##  How much test coverage is enough?

The optimal level of test coverage depends on various factors such as project
complexity, risk tolerance, and resources. There is no fixed percentage, but
aiming for a range of 70-80% coverage is generally considered good practice.

##  What is maximum test coverage?

Maximum test coverage refers to achieving the highest possible level of test
execution to ensure thorough testing of requirements and functionalities
outlined in various documents such as FRS, SRS, and URS.

##  How can I improve my test coverage?

To improve test coverage, create comprehensive test cases that cover a wide
range of test scenarios relevant to the current release. Prioritize testing
before the release to efficiently cover more scenarios within a scheduled
timeframe.

##  What is 100% test coverage?

Achieving 100% test coverage means ensuring that all parts of your code are
tested by unit tests. It helps identify and fix bugs before they impact users,
improving code quality and reducing the risk of undetected issues in untested
portions of the codebase.


-->

<!--






-->

<!--
As a software tester, one of the main goals of our work is to ensure that the
software being tested is high quality, runs smoothly, and meets the
requirements of the end-users. Test coverage is an essential aspect of
software testing that you need to know to achieve these goals. [
](https://muuktest.com/blog/test-coverage/#In_Summary "In Summary")

While Test Coverage might be a common term used in our daily processes, are we
using it enough? Once a production defect arises, the first thing that comes
to mind is “Did we cover that scenario during testing?” We’ll then refer to
our documentation and ensure that it’s covered or not. Of course, exhaustive
testing is impossible and probably a myth. But we can achieve a high test
coverage using some techniques and tools. At least we can ensure that our
application is tested thoroughly based on the requirements, product knowledge,
risks/assumptions, etc.

##  **What is Test Coverage?**

Test coverage is a measurement used to describe the degree to which the source
code/requirements of an application are tested by a particular set of test
cases. It is usually expressed as a percentage that measures how much of the
program code has been tested. Test coverage helps identify areas of the
program that are not tested, so they can be tested to ensure the program works
correctly.

For example, let’s say that there are 15 requirements. A total of 90 test
cases were developed and tagged to 12 requirements. Yet for some reason, the
remaining three requirements are not covered by the tests. In this case, we
would say the test coverage is 80%. This is an optimal coverage percentage.

##  **Importance of Test Coverage**

The importance of test coverage cannot be overemphasized. It helps ensure that
your test suite is comprehensive and that all the critical functionality of
your application has been covered. By ensuring that your application has high
test coverage, you can be confident that it’s high quality and meets the
requirements of the end users.

Test coverage can also:

  * Identify errors and differences in system behavior. 
  * Identify gaps in requirements and design specifications. 
  * Improve system reliability, performance, and scalability. 
  * Identify areas for improvement and assist in the decision-making process for further testing or when to deploy a product. 
  * Identify development bottlenecks and ensure quality while also providing confidence to stakeholders. 
  * Minimize the risks associated with software changes, making sure that the system performs as needed even after changes are implemented 
  * Ensure system security by verifying that all components of the system are tested and covered, thus minimizing the chances of security breaches and data loss. 

A high test coverage indicates that most of the possible [ scenarios
](https://www.geeksforgeeks.org/software-testing-scenario-testing/?ref=gcse)
have been tested, therefore reducing potential errors.

[ ![Ensure comprehensive test coverage with MuukTest.](https://no-
cache.hubspot.com/cta/default/6035238/3993828a-01cb-4588-9568-f860cf345bda.png)
](https://cta-
redirect.hubspot.com/cta/redirect/6035238/3993828a-01cb-4588-9568-f860cf345bda)

##  **The Difference Between Test Coverage and Code Coverage**

To implement high test coverage, you need to understand the Code Coverage
which is usually confused with test coverage.

Test coverage measures the total amount of testing done on a project, whereas
code coverage measures the percentage of the source code that has been tested.
Test coverage is concerned with the efficiency of the tests, whereas code
coverage is concerned with the overall effectiveness of the source code. Test
coverage is concerned with implemented tests, whereas code coverage is
concerned with code that has been evaluated.

![Test Coverage](https://muuktest.com/hs-fs/hubfs/Imported_Blog_Media/test-
coverage-1024x538-1.jpg?width=1024&height=538&name=test-
coverage-1024x538-1.jpg)

There are several types of code coverage, each with its benefits:

1\. **Statement Coverage:** The most basic type of test coverage, also known
as “Line Coverage”, tests each line of code to ensure it is executed at least
once during the execution of the program.

2\. **Decision Coverage:** A more advanced type of test coverage, it tests
each decision point and verifies that both the true and false paths have been
taken and all statements have been executed at least once.

3\. **Condition Coverage:** This is a more specific type of test coverage that
tests all combinations of conditions within decisions. It covers all the
possible outcomes that can occur within the decision and verifies that each
condition is tested.

4\. **Path Coverage** : Path coverage tests all possible paths through a
program, including loops and branches. It is the most comprehensive type of
testing available and covers every possible execution path in the program.

5\. **Structural Coverage:** A kind of white box testing that tests how
functionality is implemented in the program. It verifies that all logical
structures like if/then/else, switch/case, and while/do loops are tested and
executed.

Each type of code coverage has its advantages and disadvantages, but they all
help to ensure that all the code is thoroughly tested before it is released
into production.

##  **Benefits of Test Coverage**

  * **Identify Bugs Early:** Test coverage aids in the early detection and resolution of defects. This is crucial to avoid unexpected behavior and costly corrections later on. 
  * **Improved Quality:** Having thorough test coverage improves the overall quality of the software product since more issues can be detected and corrected more rapidly. This contributes to the software’s increased stability and dependability. 
  * **Increased Confidence:** Comprehensive test coverage also contributes to the user and stakeholder’s trust in the software product. The knowledge that the program has been tested in a variety of environments might assist to increase trust in the product. 
  * **Balanced Prioritization:** Test coverage contributes to ensuring that testing is balanced across all aspects of the product. Without test coverage, there may be an overemphasis on certain software components while others go untested. 
  * **Increased Scope of Testing:** Test coverage ensures that all testable scenarios are adequately tested. Without test coverage, some cases may be dismissed or overlooked, potentially leading to future difficulties. 
  * **Improved Documentation:** Tests can also serve as documentation by demonstrating how specific features and functionality should work. This also aids in avoiding typical misconceptions about how applications should behave. 
  * **Reduced Maintenance Costs:** Testing efficiently will also reduce the time and resources required to perform maintenance, which may lead to cost savings. Most of the defects would’ve been uncovered at an earlier stage, allowing for more cost-effective fixes and less maintenance post-production.   

##  **Challenges Faced While Implementing Test Coverage**

Even though test coverage is beneficial for all of the reasons described
above, it’s not always easy to implement. There are several challenges to
consider:

  * Insufficient funding and resources: Adequate testing necessitates sufficient resources like systems, tools, hardware devices, and training/learning materials. Allotments, team size, and testing time are additional factors. These resources can be costly, and organizations with limited resources may be unable to hire testers or all the hardware devices needed for testing. 

  * Not enough time: Many times, test coverage is completed during the final stages of development, which can be a time-consuming process. Companies may not have the luxury of time to undertake thorough test coverage since time is critical when introducing a product to the market. 

  * Difficulties in Identifying the Test Cases: More sophisticated systems need more complex and many test cases to cover all conceivable situations and edge cases. It is difficult to develop and identify all of the necessary test cases, and a lack of appropriate test cases may result in bugs and issues. 

  * Not enough Automation Tools/Set-up: Manually setting up and designing tests might take a significant amount of time and work. Deploying automation technologies can help ease this, but doing so needs additional costs, resources, and training. 

  * Lack of domain knowledge: Throughout the testing process, it is critical to have knowledgeable and experienced testers who understand the application’s domain and user requirements. A lack of adequate domain expertise might make identifying and designing correct test cases and scenarios challenging. 

  * Difficulty in determining whether the tests are sufficiently comprehensive: Even after having selected the group of test cases and scenarios to test, it is difficult to determine whether the test cases are sufficiently comprehensive. 

  * Dependency on external factors: When we have some external dependencies like database, third-party API, etc, it becomes very difficult to keep the tests updated and cover the expected behaviors. 

[ ![Ensure comprehensive test coverage with MuukTest.](https://no-
cache.hubspot.com/cta/default/6035238/3993828a-01cb-4588-9568-f860cf345bda.png)
](https://cta-
redirect.hubspot.com/cta/redirect/6035238/3993828a-01cb-4588-9568-f860cf345bda)

##  **In Summary**

Test coverage is an important part of software testing. It helps to ensure
that all the code is tested and no bugs are left behind. It’s a powerful
metric that ensures that the software meets the desired quality standards. It
helps to identify areas of improvement and provides valuable insights into the
effectiveness of the testing process. By leveraging the power of test
coverage, organizations can ensure that their software testing process is
comprehensive and effective, leading to better quality assurance in their
products. With test coverage, teams can ensure that their software is ready
for release with confidence.

Test coverage is a crucial aspect of software testing that you need to
understand to ensure that your application is of high quality, runs smoothly,
and meets the requirements of the end users. By ensuring that your test suite
covers all the levels of test coverage, you can be confident that your
application is fully tested and meets the needs of its users.


-->

<!--






-->

<!--
###  **#1. Statement Coverage**

Statement coverage ensures that all the statements in the source code have
been tested at least once. It provides the details of both executed and failed
code blocks out of total code blocks.

Let’s understand it with the example of the flow diagram. In the given
example, this path 1A-2C-3D-E-4G-5H covers all the statements and hence it
requires only on a test case to cover all the requirements. One test case
means one statement coverage.

![Test coverage](https://www.simform.com/wp-content/uploads/2018/03/statement-
coverage-1024x502.png)

In complex code, a single path is not sufficient to cover all the statements.
In that case, you need to write multiple test cases to cover all the
statements.

**Advantages:**

  * It can be applied directly to object code and does not require processing source code. 
  * It verifies what the written code is expected to do and not to do 

**Disadvantages:**

  * It covers only true conditions of every statement. 
  * Does not report when loop reaches to the terminations. 
  * Statement coverage is completely insensitive to the logical operators (|| and &&). 

Statement coverage is the basic coverage and hence does not guarantee 100%
coverage.

###  **#2. Decision/Branch coverage**

It is impossible for developers to write code in a continuous mode, at any
points they need to branch out the code to meet the functionality
requirements. Branching in the code is actually a jump from one decision point
to another point. Branch Coverage checks every possible path or branch in the
code is covered.

![test coverage](https://www.simform.com/wp-content/uploads/2018/03/branch-
coverage-1024x502.png)

Branch coverage can be calculated by finding the minimum number of paths which
ensure that all the edges have been covered. In the given example, there is no
single path that ensures coverage of all the edges at one go.

For example, if you follow this path 1A-2C-3D-E-4G-5H which covers the maximum
number of edges(A, C, D, E, G and H), you will still miss the two edges B and
F. You need to follow another path 1A-2B-E-4F to cover the remaining two
edges. By combining the above two paths you can ensure of travelling through
all the paths. For this test coverage example, our branch coverage is 2 as we
are following two paths and it requires two test cases to meet the
requirements.

**Advantages:**

  * It covers both the true and false conditions unlikely the statement coverage. 
  * It validates if all branches are tested. 

**Disadvantages:**

  * It ignores branches within Boolean expressions which occur due to short-circuit operators. 

###  **#3. Path Coverage**

Path testing is a structural testing method that involves using the source
code of a program in order to find every possible executable path.

Path Coverage ensures coverage of all the paths from start to end. In this
example, there are four possible paths:

  1. 1A-2B-E-4F 
  2. 1A-2B-E-4G-5H 
  3. 1A-2C-3D-E-4G-5H 
  4. 1A-2C-3D-E-4F 

![test coverage](https://www.simform.com/wp-content/uploads/2018/03/path-
coverage-1024x502.png)

**Advantages:**

  * It helps to reduce redundant tests. 
  * Path coverage provides high test coverage because it covers all statements and branches in the code. 

**Disadvantages:**

  * Testing each path is challenging as well as time-consuming because a number of paths are exponential to the number of branches. For example, a function containing 10 if-statements has 1024 paths to test. 
  * Sometimes many paths are impossible to exercise due to relationships of data. 

###  **#4. Condition Coverage**

Condition coverage checks if both the outcomes(“true” or false”) of every
condition have been exercised. The outcome of the decision point is only
relevant for checking the conditions. It requires two test cases per condition
for two outcomes.

**Advantages:**

  * Condition coverage measures the conditions independently of each other. 
  * It has better sensitivity to the control flow. 

**Disadvantages:**

  * Similar to the branch/decision coverage. 

###  **#5. Boundary Value Coverage**

This coverage metric is very useful for those applications in which error
occurred due to input numbers. And these errors occurred at boundary values.
In boundary value coverage, test cases are selected at the endpoints of the
equivalence classes. For this test coverage example, below are boundary values
for an application which requires 3-digit number as an input.

  1. 100(Minimum) 
  2. 99(Just below the minimum boundary value) 
  3. 999(Maximum) 
  4. 1000(Just above the maximum boundary value) 

**Advantages:**

  * It is quite easy to test a small set of data in place of testing a whole lot of data sets. 
  * It is easy to use because of it’s easy to automate nature and uniformity of identified tests. 

**Disadvantages:**

  * It can not test dependencies between two inputs. 
  * It can not cover code which contains boolean  functions.   

###  **#6. Product Coverage**

Product coverage refers to the process of testing a software solution from a
product perspective and evaluating specific product areas. It involves
evaluating the performance of software across various scenarios by

  * Defining and prioritizing requirements 
  * Developing a checklist 
  * Implementing effective test automation 

###  **#7. Risk Coverage**

The risk coverage technique is used to comprehensively evaluate all software-
related risks and rigorously test the application. It involves identifying and
assessing all potential risks and the issues that may arise from them,
including low-probability scenarios that could significantly impact the
software.

###  **#8. Requirements Coverage**

Requirements coverage is used to assess whether the end-product encompasses
all the committed functionalities and fulfills the customer’s stipulated
requirements. It measures the number of requirements addressed and the types
of tests executed to validate them.

![requirements coverage](https://www.simform.com/wp-
content/uploads/2021/06/requirements-coverage.jpg)

###  **#9. Compatability Coverage**

Compatibility coverage is a technique used to ensure the software works
seamlessly across all browsers, operating systems, and devices without any
issues or complications. It involves testing the product’s compatibility-
related problems, including mobile testing, hardware testing, browser testing,
network testing, and other subtypes.

![compatibility coverage](https://www.simform.com/wp-
content/uploads/2021/06/compatibility-coverage.jpg)


-->

<!--






-->

