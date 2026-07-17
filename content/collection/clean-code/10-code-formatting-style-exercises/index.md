---
draft: true
collection_order: 10
slug: code-formatting-style-exercises
title: "[Clean Code] 10장. 포맷팅·린팅 자동화 실습"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "한 줄에 여러 문장이 압축된 사용자 관리 코드를 정리하고, Prettier·ESLint 같은 포매터·린터를 pre-commit 훅과 CI 파이프라인에 연결해 형식 논쟁을 팀 차원에서 자동으로 없애는 방법을 단계별로 실습한다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Java
- JavaScript
- Python
- Git
- CI-CD(Continuous Integration/Continuous Deployment)
- Automation(자동화)
- Productivity(생산성)
- Code-Review(코드리뷰)
- Implementation(구현)
- Pitfalls(함정)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- DevOps
- Documentation(문서화)
- Testing(테스트)
- Refactoring(리팩토링)
- IDE(Integrated Development Environment)
- Modularity
---

## 이 장을 읽기 전에

이 장은 [09장: 형식 맞추기와 코드 스타일](/post/clean-code/code-formatting-style-consistency/)에서 다룬 세로/가로 형식 원칙을 실제 자동화 도구로 강제하는 실습이다. 09장을 먼저 읽었다는 전제로 진행하며, 특정 CI 플랫폼(GitHub Actions 등) 문법 지식은 필요하지 않다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 실습 1 전체 | 압축된 코드를 사람이 직접 정리하며 형식의 가치를 체감한다 |
| 실무자 | 실습 2, "판단 기준" | 팀 저장소에 포매터·린터를 실제로 강제하는 파이프라인을 설계한다 |

## 실습 1: 압축된 코드 정리

아래 코드는 문법적으로는 완전히 정상이지만, 여러 문장이 한 줄에 압축돼 있어 각 문장의 경계를 눈으로 찾아야 한다.

```java
// 실습 대상: 형식이 무너진 코드
import java.util.*;import java.time.*;
public class UserManager{
private List<User>users=new ArrayList<>();private Map<String,String>userSessions=new HashMap<>();
private final int MAX_SESSIONS=100;
public boolean addUser(String name,String email,int age){
if(name==null||name.trim().isEmpty()){return false;}
users.add(new User(name,email,age));return true;}}
```

09장에서 다룬 원칙(개념은 빈 줄로 분리, 들여쓰기로 계층을 드러내기)을 그대로 적용하면 다음과 같이 정리된다.

```java
// 리팩토링 결과: 계층과 개념 구분이 들여쓰기와 빈 줄로 드러남
import java.util.*;
import java.time.*;

public class UserManager {
    private static final int MAX_SESSIONS = 100;

    private List<User> users = new ArrayList<>();
    private Map<String, String> userSessions = new HashMap<>();

    public boolean addUser(String name, String email, int age) {
        if (name == null || name.trim().isEmpty()) {
            return false;
        }
        users.add(new User(name, email, age));
        return true;
    }
}
```

이 작업을 손으로 직접 해보면, 형식이 무너진 코드를 읽는 데 걸리는 시간과 정리된 코드를 읽는 데 걸리는 시간의 차이를 체감할 수 있다. 하지만 실무에서는 이 정리 작업을 사람이 매번 손으로 하지 않는다 — 다음 실습에서 이 과정을 자동화한다.

## 실습 2: 포매터·린터를 파이프라인에 연결하기

자동 포매터는 저장 시점 또는 커밋 시점에 위 정리 작업을 자동으로 수행한다. Java 생태계의 google-java-format, JavaScript/TypeScript의 Prettier, Python의 Black은 모두 "선택지를 최소화해 논쟁을 없앤다"는 같은 철학을 공유한다. 아래는 Prettier와 ESLint를 pre-commit 훅에 연결하는 설정 예시다.

```json
// .prettierrc — 프로젝트 전체가 공유하는 단일 형식 규칙
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

```yaml
# .github/workflows/lint.yml — CI에서 형식·린트 위반을 자동 차단
name: Lint
on: [pull_request]
jobs:
  format-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx prettier --check .
      - run: npx eslint .
```

이 설정의 핵심은 `--check` 플래그다. 이는 포매터가 코드를 고쳐 쓰는 대신, "정해진 형식과 다른 부분이 있으면 실패시킨다"는 게이트 역할을 한다. 이렇게 하면 형식이 어긋난 PR은 리뷰어가 사람 눈으로 지적하기 전에 CI 단계에서 자동으로 걸러진다 — 09장에서 다룬 "형식 논쟁을 사람이 아니라 도구에 위임한다"는 원칙이 실제 파이프라인으로 구현된 것이다.

## 판단 기준: 어디까지 자동화하고 어디부터 논의할 것인가

포매터가 강제할 수 있는 규칙(들여쓰기, 따옴표 종류, 줄 길이)은 예외 없이 자동화 설정에 위임하고, 팀 회의에서 다시 논의하지 않는다. 반면 "이 클래스를 어떻게 나눌 것인가", "이 필드들을 어떤 순서로 배치할 것인가"처럼 의미 판단이 필요한 규칙은 자동화 도구가 대신할 수 없으므로, 코드 리뷰에서 계속 사람이 판단해야 한다. 이 경계를 명확히 나누지 않으면, 자동화할 수 있는 규칙까지 매번 코드 리뷰에서 지적하며 시간을 낭비하게 된다.

## 다음 장에서는

[11장: 객체와 자료구조의 비대칭](/post/clean-code/objects-vs-data-structures-design-patterns/)에서는 형식을 넘어, 데이터를 다루는 두 가지 상반된 방식을 다룬다.

## 평가 기준

- [ ] 압축된 코드를 09장의 형식 원칙에 따라 직접 정리할 수 있다.
- [ ] 포매터를 `--check` 모드로 CI에 연결해 형식 위반을 자동 차단하는 파이프라인을 설계할 수 있다.
- [ ] 자동화로 위임할 규칙과 사람이 계속 판단해야 할 규칙을 구분할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 5장.
- [Prettier 공식 문서](https://prettier.io/)
- [ESLint 공식 문서](https://eslint.org/)
- [Black 공식 문서](https://black.readthedocs.io/en/stable/)
