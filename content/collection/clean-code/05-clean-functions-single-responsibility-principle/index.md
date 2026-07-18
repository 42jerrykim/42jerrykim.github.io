---
draft: false
collection_order: 5
slug: clean-functions-single-responsibility-principle
title: "[Clean Code] 05. 함수는 작게, 한 가지만"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "함수를 작게 만들고 한 가지 일만 하도록 설계하는 원칙을 추상화 수준, 인수 개수, 부수 효과, 명령-조회 분리라는 네 가지 관점에서 다룬다. switch 문을 다형성으로 대체하는 방법과 과도한 분해의 한계도 함께 살펴본다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Refactoring(리팩토링)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- SOLID
- Design-Pattern(디자인패턴)
- OOP(객체지향)
- Polymorphism(다형성)
- Abstraction(추상화)
- Functional-Programming(함수형프로그래밍)
- Error-Handling(에러처리)
- Java
- Python
- Testing(테스트)
- Modularity
- Pitfalls(함정)
- Coupling(결합도)
- Cohesion(응집도)
- Implementation(구현)
- Code-Review(코드리뷰)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
---

## 이 장을 읽기 전에

이 장은 [03~04장](/post/clean-code/meaningful-naming-conventions-variables-functions/)에서 다룬 네이밍 원칙을 전제로 하며, 좋은 이름이 붙은 함수라도 크기와 책임이 잘못되면 여전히 읽기 어렵다는 점에서 출발한다. 최소한 하나의 언어에서 함수(메서드)를 작성하고 조건문·반복문을 다뤄 본 경험이 필요하다. 이 장은 함수 단위의 설계를 다루며, 클래스 단위의 책임 분리는 [18장](/post/clean-code/clean-classes-solid-principles-oop/)에서 본격적으로 확장한다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "작게 만들어라"부터 "함수 인수"까지 | 함수를 작게 쪼개는 구체적 기법과 그 이유를 이해한다 |
| 실무자 | "흔한 오개념", "판단 기준", "비판적 시각" | 함수 분해를 어디까지 밀어붙일지, 언제 멈춰야 할지 판단 기준을 세운다 |

## 작게 만들고 한 가지만 하라

함수 설계에서 가장 먼저 세울 기준은 크기다. 함수가 작을수록 한눈에 파악할 수 있고, 테스트할 경로가 줄어들며, 다른 맥락에서 재사용하기도 쉬워진다. 함수를 작게 만드는 구체적인 기법 중 하나는 조건문·반복문의 본문을 한 줄로 유지하는 것이다. 대개 그 한 줄은 의미 있는 이름을 가진 다른 함수 호출이며, 이렇게 하면 감싸는 함수(enclosing function)의 크기가 줄어들 뿐 아니라 그 자체로 문서 역할을 한다. 함수 안에서 들여쓰기 수준이 1~2단을 넘어서기 시작하면, 이는 그 함수가 너무 많은 일을 하고 있다는 신호로 읽어야 한다.

"작게"라는 기준보다 더 근본적인 규칙은 **함수가 한 가지 일만 해야 한다**는 것이다. 여기서 "한 가지"를 판단하는 실용적인 방법은, 그 함수에서 의미 있는 이름을 가진 다른 함수를 추출할 수 있는지를 보는 것이다. 추출이 가능하다는 것은 원래 함수가 최소 두 가지 이상의 추상화 수준(또는 책임)을 섞고 있었다는 뜻이다. 아래 예제는 위키 페이지를 HTML로 렌더링하는 함수를 보여준다.

```java
// 여러 일을 한꺼번에 하는 함수: 조건 분기, 페이지 탐색, 문자열 조립이 뒤섞여 있다
public static String testableHtml(PageData pageData, boolean includeSuiteSetup) {
    WikiPage wikiPage = pageData.getWikiPage();
    StringBuffer buffer = new StringBuffer();
    if (pageData.hasAttribute("Test")) {
        if (includeSuiteSetup) {
            WikiPage suiteSetup = PageCrawlerImpl.getInheritedPage(
                SuiteResponder.SUITE_SETUP_NAME, wikiPage);
            if (suiteSetup != null) {
                WikiPagePath pagePath = suiteSetup.getPageCrawler().getFullPath(suiteSetup);
                buffer.append("!include -setup .")
                      .append(PathParser.render(pagePath)).append("\n");
            }
        }
        buffer.append(pageData.getContent());
    }
    return buffer.toString();
}

// 한 가지 흐름만 남기고 세부사항을 하위 함수로 위임한 버전
public static String renderPageWithSetupsAndTeardowns(PageData pageData, boolean isSuite) {
    if (pageData.hasAttribute("Test")) {
        WikiPage testPage = pageData.getWikiPage();
        StringBuffer newPageContent = new StringBuffer();
        includeSetupPages(testPage, newPageContent, isSuite);
        newPageContent.append(pageData.getContent());
        includeTeardownPages(testPage, newPageContent, isSuite);
        pageData.setContent(newPageContent.toString());
    }
    return pageData.getHtml();
}
```

두 번째 버전은 "테스트 페이지라면 설정과 해제를 감싸서 렌더링한다"는 한 문장으로 요약된다. 이렇게 함수 전체를 하나의 `TO` 문단(TO 무엇을 하려면, ~한다)으로 서술할 수 있다면, 그 함수는 실제로 한 가지 작업만 하고 있다는 신호다.

## 추상화 수준 통일과 인수 개수

함수가 정말 한 가지 일만 하려면, 함수 내 모든 문장의 추상화 수준이 같아야 한다. `getHtml()`처럼 높은 수준의 호출과 `.append("\n")`처럼 낮은 수준의 문자열 조작이 한 함수 안에 섞이면, 독자는 각 줄이 핵심 로직인지 세부 구현인지 판단하는 데 별도의 노력을 들여야 한다. 좋은 코드는 위에서 아래로 읽을 때 추상화 수준이 한 번에 한 단계씩 낮아지는 **내려가기 규칙(Stepdown Rule)**을 따른다 — 마치 신문 기사가 헤드라인에서 시작해 점점 세부사항으로 내려가는 것과 같다.

함수 인수의 개수도 추상화 수준만큼 이해도에 영향을 준다. 인수가 늘어날수록 함수를 호출하는 쪽과 읽는 쪽 모두 "이 인수가 무엇을 뜻하는지, 순서가 맞는지"를 추론해야 하는 부담이 커진다. 이상적인 인수 개수는 0개이며, 3개를 넘어가면 재고할 필요가 있고 4개 이상은 특별한 근거가 있어야 한다. 특히 `render(boolean isSuite)`처럼 불리언으로 함수의 동작을 분기시키는 **플래그 인수**는 그 함수가 실제로는 두 가지 일(스위트용 렌더링과 단일 테스트용 렌더링)을 한다고 스스로 광고하는 것과 같다 — 이 경우 `renderForSuite()`와 `renderForSingleTest()`로 분리하는 편이 낫다. 인수가 2~3개 필요하다면, 관련된 인수를 하나의 객체로 묶을 수 있는지도 검토해야 한다. `makeCircle(double x, double y, double radius)`보다 `makeCircle(Point center, double radius)`가 나은 이유는 단순히 인수 개수가 줄어서가 아니라, `x`와 `y`가 항상 함께 다뤄지는 하나의 개념(좌표)이라는 사실이 시그니처에 드러나기 때문이다.

## Switch 문과 다형성

`switch` 문은 본질적으로 N가지 경우를 처리하므로 "한 가지 일"이라는 기준과 부딪힌다. 문제는 `switch` 문 자체가 아니라, 같은 조건식이 코드베이스 여러 곳에 반복되는 상황이다.

```java
// 새 직원 유형이 추가될 때마다 이 switch 문을 찾아 고쳐야 한다
public Money calculatePay(Employee e) throws InvalidEmployeeType {
    switch (e.type) {
        case COMMISSIONED: return calculateCommissionedPay(e);
        case HOURLY:        return calculateHourlyPay(e);
        case SALARIED:      return calculateSalariedPay(e);
        default: throw new InvalidEmployeeType(e.type);
    }
}
```

이 코드는 새 직원 유형이 추가될 때마다 함수가 길어질 뿐 아니라, 급여 계산 외에 근무일 판정이나 급여 지급 방식을 다루는 다른 함수에도 똑같은 `switch` 문이 반복될 가능성이 높다. 다형성을 이용하면 이 반복을 한 곳(팩토리)으로 모을 수 있다.

```java
public abstract class Employee {
    public abstract Money calculatePay();
}

public class EmployeeFactory {
    public Employee makeEmployee(EmployeeRecord record) throws InvalidEmployeeType {
        switch (record.type) {
            case COMMISSIONED: return new CommissionedEmployee(record);
            case HOURLY:        return new HourlyEmployee(record);
            case SALARIED:      return new SalariedEmployee(record);
            default: throw new InvalidEmployeeType(record.type);
        }
    }
}
```

이제 `switch` 문은 객체를 생성하는 팩토리 한 곳에만 존재하고, 이후 급여 계산·근무일 판정 등은 각 `Employee` 하위 클래스의 다형성 호출로 처리된다. 이 패턴은 [18장](/post/clean-code/clean-classes-solid-principles-oop/)에서 다룰 개방-폐쇄 원칙(OCP)의 구체적인 적용 사례이기도 하다.

## 부수 효과와 명령-조회 분리

함수 이름이 약속한 것 외에 몰래 다른 일을 하면, 그 함수는 독자에게 거짓말을 하는 셈이다. 아래 `checkPassword`는 이름만 보면 비밀번호를 확인할 뿐이지만, 실제로는 세션을 초기화하는 부수 효과를 숨기고 있다.

```java
public boolean checkPassword(String userName, String password) {
    User user = UserGateway.findByName(userName);
    if (user != null) {
        String phrase = cryptographer.decrypt(user.getPhraseEncodedByPassword(), password);
        if ("Valid Password".equals(phrase)) {
            Session.initialize(); // 숨겨진 부수 효과
            return true;
        }
    }
    return false;
}
```

이 함수를 호출하는 사람은 "비밀번호만 확인한다"고 믿고 다른 시점에 이 함수를 재사용했다가, 의도치 않게 세션이 초기화되는 버그를 만들 수 있다. 이 문제는 **명령과 조회를 분리하라(Command Query Separation)**는 원칙과 직결된다. 함수는 무언가를 수행하거나(명령), 무언가에 답하거나(조회) 둘 중 하나만 해야 한다. `if (set("username", "unclebob"))`처럼 설정과 성공 여부 확인을 한 함수로 처리하면, 호출부 코드만으로는 "설정이 성공했다"는 뜻인지 "username이 이미 unclebob으로 설정되어 있다"는 뜻인지 구분할 수 없다.

같은 맥락에서 오류 코드를 반환하는 함수도 명령-조회 분리를 미묘하게 위반한다. `if (deletePage(page) == E_OK)`처럼 오류 코드를 반환하면 호출자는 즉시 그 결과를 확인해야 하고, 여러 단계가 중첩되면 들여쓰기가 깊어지는 **화살촉 코드(arrow code)**가 만들어진다. 예외를 사용하면 오류 처리 코드를 정상 흐름에서 분리할 수 있다.

```java
// 오류 코드 대신 예외를 사용하고, try/catch도 별도 함수로 뽑아낸다
public void delete(Page page) {
    try {
        deletePageAndAllReferences(page);
    } catch (Exception e) {
        logError(e);
    }
}

private void deletePageAndAllReferences(Page page) throws Exception {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
}
```

오류 처리 자체도 "한 가지 일"이므로, 오류 처리를 담당하는 함수는 오류 처리만 해야 한다. 이 주제는 [13장](/post/clean-code/error-handling-exceptions-best-practices/)에서 예외 설계 전반으로 확장해서 다룬다.

## 흔한 오개념

**"함수가 20줄을 넘으면 무조건 나쁘다"**는 오해가 흔하지만, Martin이 제시한 크기는 절대적인 줄 수 규칙이 아니라 "한 가지 일만 한다면 자연스럽게 짧아진다"는 결과에 가깝다. 알고리즘의 성격상 분해하면 오히려 흐름을 놓치는 경우(예: 상태 기계의 전이 테이블)도 있으며, 이때는 줄 수보다 "이 함수가 실제로 몇 가지 책임을 지는가"를 기준으로 판단해야 한다.

**"함수를 잘게 쪼갤수록 항상 더 좋다"**는 오개념도 있다. 과도하게 쪼개진 함수는 호출 스택을 따라가야만 전체 로직을 이해할 수 있게 되어, 오히려 데이터 흐름을 추적하기 어렵게 만들 수 있다. 이는 아래 "비판적 시각"에서 더 다룬다.

## 판단 기준

함수를 더 쪼갤지 판단할 때는 "이 함수에서 의미 있는 이름의 함수를 하나 더 추출할 수 있는가"를 먼저 묻는다. 추출할 수 있다면 대체로 쪼개는 편이 낫다. 다만 추출한 결과 호출자가 전체 흐름을 이해하기 위해 3단계 이상의 함수 호출을 따라가야 한다면, 그 분해가 오히려 읽기를 방해하지 않는지 재검토해야 한다. 성능이 critical한 루프 내부(예: 초당 수백만 번 호출되는 함수)에서는 함수 호출 자체의 오버헤드나 인라이닝 실패 가능성을 프로파일링으로 확인한 뒤 분해 여부를 결정하는 것이 안전하다.

## 비판적 시각

함수를 작게 쪼개는 원칙에 대한 대표적인 반론은, 지나치게 잘게 나뉜 함수들이 오히려 "이 데이터가 어디서 와서 어떻게 바뀌는지"를 추적하기 어렵게 만든다는 것이다. 게임 엔진 개발자 Casey Muratori를 비롯한 일부 실무자들은 함수 하나에 로직을 어느 정도 모아두는 편이, 여러 개의 한 줄짜리 함수로 흩어놓는 것보다 데이터 흐름을 파악하기 쉽고 캐시 지역성도 유리하다고 주장한다. 이 관점은 특히 성능이 중요한 도메인에서 설득력을 얻는다. 실무적인 절충점은 "이 함수가 다루는 데이터가 명확히 하나의 개념 단위(주문, 사용자, 좌표)로 묶이는가"를 기준 삼아, 개념적으로 응집된 로직은 한 함수에 남기고 서로 다른 추상화 수준이 섞이는 지점에서만 분해하는 것이다.

## 다음 장에서는

[06장: 함수 리팩토링 실습](/post/clean-code/clean-functions-refactoring-exercises/)에서는 이 장의 원칙을 실제 긴 함수에 적용해 단계적으로 분해해 본다.

## 평가 기준

- [ ] "한 가지 일"을 판단하는 기준(다른 함수를 추출할 수 있는가)을 설명하고 적용할 수 있다.
- [ ] 반복되는 `switch` 문을 다형성으로 대체해야 하는 이유와 방법을 설명할 수 있다.
- [ ] 플래그 인수가 왜 함수가 두 가지 일을 한다는 신호인지 설명할 수 있다.
- [ ] 명령과 조회를 분리해야 하는 이유를 오류 코드 반환의 문제와 연결해 설명할 수 있다.
- [ ] 함수 분해를 어디까지 밀어붙일지 판단하는 기준(추적성, 성능)을 제시할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 3장.
- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.). Addison-Wesley. "Extract Function".
