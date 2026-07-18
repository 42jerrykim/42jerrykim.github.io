---
draft: false
collection_order: 9
slug: code-formatting-style-consistency
title: "[Clean Code] 09장. 형식 맞추기와 코드 스타일"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "코드 형식이 왜 미학이 아니라 의사소통의 일부인지 세로 밀집도·수직 거리·가로 정렬 원칙으로 설명하고, 개인 취향에 좌우되던 형식 논쟁을 자동 포매터와 팀 컨벤션으로 해소하는 방법을 우선순위 판단 기준과 함께 다룬다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Code-Review(코드리뷰)
- Java
- Python
- JavaScript
- IDE(Integrated Development Environment)
- VSCode
- Git
- CI-CD(Continuous Integration/Continuous Deployment)
- Automation(자동화)
- Productivity(생산성)
- Implementation(구현)
- Pitfalls(함정)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Documentation(문서화)
- Testing(테스트)
- Refactoring(리팩토링)
- DevOps
- Modularity
---

## 이 장을 읽기 전에

이 장은 이전 장들에서 다룬 이름·함수·주석 원칙을 전제로 하지 않는 독립적인 주제이며, 코드의 시각적 배치가 가독성에 미치는 영향을 다룬다. 특정 포매터 도구(Prettier, Black 등) 사용 경험은 필요 없다. 자동화 도구를 실제로 설정해 보는 실습은 [10장](/post/clean-code/code-formatting-style-exercises/)에서 다룬다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | "형식은 의사소통이다"부터 "가로 형식" | 세로/가로 형식이 코드 이해 속도에 미치는 영향을 이해한다 |
| 실무자 | "판단 기준", "비판적 시각" | 팀 컨벤션 논쟁을 자동화 도구 도입으로 해소하는 방법을 익힌다 |

## 형식은 의사소통이다

코드 형식(들여쓰기, 빈 줄, 공백 배치)은 미학의 문제가 아니라 **의사소통의 일부**다. 오늘 구현한 기능의 로직은 다음 버전에서 바뀔 가능성이 높지만, 처음 잡아놓은 형식 스타일은 그 코드가 리팩토링되고 확장되는 내내 유지보수 용이성에 계속 영향을 미친다. 즉 원래 코드는 사라져도 개발자가 세운 형식 규율은 코드베이스에 오래 남는다.

## 세로 형식: 신문 기사처럼 읽히게

좋은 소스 파일은 신문 기사와 비슷한 구조를 갖는다. 파일 상단에는 고차원 개념과 전체 흐름이 나오고, 아래로 내려갈수록 점점 세부적인 구현이 등장한다. 이 흐름은 05장에서 다룬 "내려가기 규칙"이 함수 내부뿐 아니라 파일 전체 구조에도 적용된 것이다.

관련 없는 개념들은 **빈 줄**로 분리해야 한다. 코드 한 줄이 문장이라면, 빈 줄로 구분된 코드 묶음은 문단에 해당한다. 반대로 서로 밀접하게 연관된 코드는 빈 줄 없이 붙여서, 그것이 하나의 생각 단위임을 시각적으로 드러낸다.

```java
// Bad: 밀접한 개념 사이에 불필요한 빈 줄이 있어 하나의 흐름인지 알기 어렵다
public class ReportGenerator {

    private String title;


    public String generate() {

        StringBuilder sb = new StringBuilder();

        sb.append(title);

        return sb.toString();
    }
}

// Good: 관련 있는 코드는 붙이고, 개념이 바뀌는 지점에만 빈 줄을 둔다
public class ReportGenerator {
    private String title;

    public String generate() {
        StringBuilder sb = new StringBuilder();
        sb.append(title);
        return sb.toString();
    }
}
```

세로 밀집도는 **거리**로도 표현된다. 서로 연관성이 깊은 개념은 세로로 가까이 배치해야 하며, 이는 변수 선언에도 적용된다. 지역 변수는 사용되는 위치 근처에서 선언하는 것이 좋고, 인스턴스 변수는 클래스 상단에 모아두는 것이 관례다(관례 자체보다 "일관되게 한 곳에 모은다"는 규칙이 더 중요하다). 서로 호출하는 함수는 세로로 가까이 배치하고, 호출하는 함수가 호출되는 함수보다 먼저 나오게 배치하면(개념적 유사성) 파일을 위에서 아래로 읽는 순서가 곧 실행 흐름을 따라가는 순서와 일치한다.

## 가로 형식: 공백과 들여쓰기

가로 공백은 연산자의 우선순위나 관계의 강도를 시각적으로 표현하는 수단으로 쓰인다.

```java
// 할당 연산자 앞뒤에는 공백을 두어 좌우 개념을 분리하고,
// 함수 호출의 괄호 안쪽에는 공백을 두지 않아 함수와 인수가 강하게 묶여 있음을 표현한다
private int total = calculatePrice(quantity, unitPrice) + shippingFee;
```

들여쓰기는 코드의 계층 구조(파일 → 클래스 → 메서드 → 블록)를 시각적으로 드러낸다. 들여쓰기를 무너뜨려 여러 문장을 한 줄에 압축하면 짧아 보일 수는 있지만, 그 코드가 속한 범위(scope)를 파악하는 데 드는 노력이 오히려 늘어난다.

```java
// Bad: 들여쓰기를 무시하고 한 줄로 압축
public class Sample {public void run(){if(isValid()){process();}}}

// Good: 계층 구조가 들여쓰기로 드러남
public class Sample {
    public void run() {
        if (isValid()) {
            process();
        }
    }
}
```

## 팀 규칙과 자동화

개인의 형식 취향은 자연스럽게 갈리기 마련이다. 중괄호를 같은 줄에 둘지 다음 줄에 둘지, 들여쓰기를 스페이스 2칸으로 할지 4칸으로 할지에 대한 "정답"은 존재하지 않는다. 여기서 중요한 것은 어떤 규칙을 선택하느냐가 아니라, **팀 전체가 하나의 규칙을 일관되게 따르는 것**이다. 한 코드베이스 안에서 파일마다 다른 스타일이 섞이면, 독자는 매번 "이 파일의 스타일은 무엇인가"를 다시 파악해야 하는 불필요한 인지 부하를 진다.

이 문제를 해결하는 현대적인 방법은 사람이 스타일을 강제하는 대신 **자동 포매터**(Prettier, Black, google-java-format)와 **린터**(ESLint, Checkstyle, Pylint)를 CI 파이프라인에 통합하는 것이다. `.editorconfig` 파일로 들여쓰기·줄 끝 문자 같은 기본 규칙을 에디터 차원에서 통일하고, 포매터를 커밋 전 훅(pre-commit hook)이나 CI 게이트에 연결하면 "형식 취향 논쟁"이 코드 리뷰에서 완전히 사라진다. 이 자동화를 실제로 구성하는 과정은 [10장](/post/clean-code/code-formatting-style-exercises/)에서 다룬다.

## 흔한 오개념

**"형식은 개인 취향이라 중요하지 않다"**는 오해가 흔하다. 실제로는 형식이 일관되지 않은 코드베이스는 각 파일을 읽을 때마다 스타일을 다시 파악해야 하는 실질적인 읽기 비용을 만든다. 형식 자체의 "정답"은 없지만, "일관성이 있는가"는 명확히 측정 가능한 품질 기준이다.

**"자동 포매터를 쓰면 형식 원칙을 몰라도 된다"**는 오해도 있다. 포매터는 가로 공백·들여쓰기 같은 기계적 규칙은 강제할 수 있지만, "관련 있는 개념을 세로로 가깝게 배치한다"거나 "함수를 호출 순서대로 배치한다"처럼 **의미에 대한 판단이 필요한 형식 결정**은 여전히 사람이 내려야 한다.

## 판단 기준

팀 컨벤션을 정할 때는 "이 규칙이 코드의 의미 전달에 영향을 주는가"를 기준으로 우선순위를 정한다. 들여쓰기 크기, 중괄호 위치처럼 의미에 영향을 주지 않는 규칙은 자동 포매터에 완전히 위임하고 더 이상 논쟁하지 않는다. 반면 "관련된 필드를 어떻게 그룹핑할 것인가", "긴 메서드 체인을 어떻게 줄바꿈할 것인가"처럼 가독성에 실질적 영향을 주는 규칙은 팀 회의에서 논의하고 스타일 가이드 문서에 근거와 함께 기록해 둘 가치가 있다.

## 비판적 시각

일부 팀에서는 자동 포매터가 보편화된 현재, 이 장에서 다루는 수동 형식 규칙(빈 줄 배치, 함수 순서)이 시대에 뒤떨어졌다고 본다. 실제로 Prettier 같은 도구는 개발자의 선택지를 의도적으로 최소화해, "논쟁 자체를 없애는 것"을 철학으로 삼는다. 이런 관점에서는 세로 밀집도 같은 세밀한 규칙보다 "포매터가 강제하는 대로 따르고 더 생각하지 않는다"는 태도가 팀의 시간을 더 아낀다는 주장도 설득력이 있다. 그럼에도 함수와 변수를 어디에 배치할지, 어떤 개념을 하나의 파일에 묶을지처럼 자동화가 대신할 수 없는 구조적 판단은 여전히 이 장의 원칙(의미 단위로 묶고, 밀접한 것은 가깝게)에 의존한다.

## 다음 장에서는

[10장: 포맷팅·린팅 자동화 실습](/post/clean-code/code-formatting-style-exercises/)에서는 이 장에서 다룬 원칙을 실제 포매터·린터 설정으로 자동화해 본다.

## 평가 기준

- [ ] 세로 밀집도와 수직 거리 개념으로 특정 코드 배치가 왜 읽기 어려운지 설명할 수 있다.
- [ ] 가로 공백이 연산자 우선순위나 관계 강도를 어떻게 시각적으로 표현하는지 예시로 설명할 수 있다.
- [ ] 형식 규칙 중 자동화로 위임할 것과 팀 논의가 필요한 것을 구분할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 5장.
- [EditorConfig 공식 사이트](https://editorconfig.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
