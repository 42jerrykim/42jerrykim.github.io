---
draft: false
collection_order: 2
slug: clean-code-fundamentals-exercises
title: "[Clean Code] 02장. 나쁜 코드 진단과 개선 실습"
date: 2026-07-17
last_modified_at: 2026-07-17
description: "학생 성적 처리 코드를 예제로 나쁜 코드의 다섯 가지 증상(매직 넘버, 모호한 이름, 다중 책임 함수 등)을 진단하고 단계적으로 리팩토링하는 실습을 진행한다. 01장에서 배운 Clean Code 판단 기준을 실제 코드에 적용해 보는 연습이다."
categories: Clean Code
tags:
- Clean-Code(클린코드)
- Refactoring(리팩토링)
- Code-Quality(코드품질)
- Best-Practices
- Readability
- Maintainability
- Testing(테스트)
- Debugging(디버깅)
- Code-Review(코드리뷰)
- Java
- Python
- Implementation(구현)
- Modularity
- Pitfalls(함정)
- Coupling(결합도)
- Cohesion(응집도)
- Tutorial(튜토리얼)
- Guide(가이드)
- Education(교육)
- Career(커리어)
- Productivity(생산성)
- Documentation(문서화)
- Design-Pattern(디자인패턴)
- OOP(객체지향)
- Encapsulation(캡슐화)
- Abstraction(추상화)
---

## 이 장을 읽기 전에

이 장은 [01장: Clean Code란 무엇인가](/post/clean-code/clean-code-fundamentals-what-is-clean-code/)에서 정의한 기준(가독성, 기술 부채, 저자로서의 책임)을 전제로 한다. 아직 01장을 읽지 않았다면 먼저 읽기를 권한다. 이 장의 깊이는 초급이며, 특정 언어의 고급 문법이 아니라 "무엇이 나쁜 코드의 증상인가"를 식별하는 안목을 기르는 데 집중한다. 함수 분해의 세부 기법은 [05~06장](/post/clean-code/clean-functions-single-responsibility-principle/)에서 본격적으로 다룬다.

| 수준 | 읽을 부분 | 핵심 목표 |
|:--:|:--|:--|
| 입문자 | 실습 1, 실습 2 전체 | 나쁜 코드의 구체적 증상(매직 넘버, 모호한 이름, 긴 함수)을 눈으로 식별한다 |
| 실무자 | 실습 3, "흔한 실수" | 리팩토링 우선순위를 정하는 판단 기준을 세운다 |

## 실습 개요

이 실습의 목표는 이론을 눈으로 확인하는 데 그치지 않고, 직접 코드를 진단하고 고치는 손 근육을 만드는 것이다. 아래 학생 성적 처리 코드는 문법적으로는 완전히 정상이며 컴파일도, 실행도 된다. 그런데도 이 코드는 Clean Code 관점에서 여러 증상을 동시에 보인다. 먼저 증상을 나열하지 않고 스스로 읽어 보면서 어디서 걸리는지 느껴보는 것이 이 실습의 첫 단계다.

```java
// 실습 대상: 학생 성적 처리 시스템
public class StudentGradeProcessor {
    public void processStudentGrades() {
        ArrayList<String> students = new ArrayList<>();
        students.add("John,85,90,78");
        students.add("Jane,92,88,95");

        for (int i = 0; i < students.size(); i++) {
            String[] parts = students.get(i).split(",");
            String n = parts[0];
            int s1 = Integer.parseInt(parts[1]);
            int s2 = Integer.parseInt(parts[2]);
            int s3 = Integer.parseInt(parts[3]);
            double avg = (s1 + s2 + s3) / 3.0;
            String grade;
            if (avg >= 90) grade = "A";
            else if (avg >= 80) grade = "B";
            else if (avg >= 70) grade = "C";
            else if (avg >= 60) grade = "D";
            else grade = "F";
            System.out.println(n + ": " + avg + " (" + grade + ")");
        }
    }
}
```

## 실습 1: 증상 진단

이 코드를 읽으면서 "왜 걸리는가"를 구체적으로 짚어보면 최소 다섯 가지 증상이 드러난다. 첫째, `n`, `s1`, `s2`, `s3`, `avg` 같은 변수 이름은 타입은 알려주지만 의도를 알려주지 않는다. 둘째, 학생 데이터가 문자열을 콤마로 파싱하는 방식으로 하드코딩돼 있어, 데이터 소스가 바뀌면(파일, DB, API) 전체 로직을 다시 써야 한다. 셋째, 등급 기준(90, 80, 70, 60)이 매직 넘버로 흩어져 있어 기준이 바뀔 때 코드 전체를 검색해야 한다. 넷째, 한 함수가 파싱·계산·등급 판정·출력을 모두 담당해 "한 가지 일"을 하지 않는다. 다섯째, 성적을 출력만 할 뿐 반환하지 않아 다른 코드에서 재사용하거나 테스트하기 어렵다.

이 다섯 가지는 우연히 한 코드에 모인 것이 아니라, 실무 코드에서 반복적으로 나타나는 전형적인 패턴이다. 아래 표로 정리하면 각 증상이 어떤 원칙과 연결되는지 명확해진다.

| 증상 | 관련 원칙 | 이 시리즈에서 다루는 장 |
|:--|:--|:--:|
| 의도가 드러나지 않는 이름 | 의미있는 네이밍 | [03장](/post/clean-code/meaningful-naming-conventions-variables-functions/) |
| 매직 넘버 | 검색하기 쉬운 이름 | [03장](/post/clean-code/meaningful-naming-conventions-variables-functions/) |
| 한 함수가 여러 일을 함 | 단일 책임 원칙 | [05장](/post/clean-code/clean-functions-single-responsibility-principle/) |
| 데이터 파싱 로직 하드코딩 | 객체와 자료구조 분리 | [11장](/post/clean-code/objects-vs-data-structures-design-patterns/) |
| 반환값 없이 출력만 함 | 명령과 조회 분리 | [05장](/post/clean-code/clean-functions-single-responsibility-principle/) |

## 실습 2: 단계적 개선

리팩토링은 한 번에 모든 것을 고치는 대신, 하나의 증상씩 순서대로 제거하는 편이 안전하다. 먼저 매직 넘버와 등급 판정 로직을 `enum`으로 옮겨 하드코딩된 기준을 한곳에 모은다.

```java
public enum Grade {
    A(90), B(80), C(70), D(60), F(0);

    private final int threshold;
    Grade(int threshold) { this.threshold = threshold; }

    public static Grade fromAverage(double average) {
        for (Grade grade : values()) {
            if (average >= grade.threshold) return grade;
        }
        return F;
    }
}
```

`enum`으로 등급 기준을 옮기면 기준이 바뀔 때 이 한 곳만 수정하면 된다는 이점이 생긴다. 다음으로 학생 데이터를 원시 문자열이 아니라 전용 클래스로 표현해, 파싱과 계산 책임을 분리한다.

```java
public class Student {
    private final String name;
    private final List<Integer> scores;

    public Student(String name, List<Integer> scores) {
        this.name = name;
        this.scores = new ArrayList<>(scores);
    }

    public String getName() { return name; }

    public double calculateAverage() {
        return scores.stream().mapToInt(Integer::intValue).average().orElse(0.0);
    }

    public Grade getLetterGrade() {
        return Grade.fromAverage(calculateAverage());
    }
}
```

마지막으로 출력을 전담하는 `GradeReporter`를 분리하면, `Student`는 성적 계산만, `GradeReporter`는 표시 형식만 책임지게 되어 각 클래스가 한 가지 이유로만 변경된다.

```java
public class GradeReporter {
    public void printGradeReport(List<Student> students) {
        students.forEach(this::printStudentGrade);
    }

    private void printStudentGrade(Student student) {
        System.out.printf("%s: %.1f (%s)%n",
            student.getName(), student.calculateAverage(), student.getLetterGrade());
    }
}
```

리팩토링 전후를 비교하면, 코드 줄 수는 오히려 늘었지만 각 조각의 책임은 훨씬 명확해졌다. 이것이 3장에서 다룰 "짧음과 깨끗함은 다르다"는 원칙이 실제 코드에서 드러나는 방식이다.

## 실습 3: 자가 점검

리팩토링이 끝났다고 판단하기 전에, 다음 질문을 스스로에게 던져본다. 이 질문들은 임의의 체크리스트가 아니라 01장에서 다룬 정의(가독성, 기술 부채, 저자의 책임)를 코드 단위로 되짚는 것이다. `Student` 클래스만 보고 이 클래스가 학생의 평균 점수와 등급을 계산한다는 것을 짐작할 수 있는가? `Grade` enum의 기준값을 바꾸는 담당자가 `StudentGradeProcessor`, `Student`, `GradeReporter` 세 클래스를 모두 열어봐야 하는가, 아니면 `Grade` 한 곳만 보면 되는가? 만약 성적 데이터를 파일이 아니라 REST API에서 읽어와야 한다면, 지금 구조에서 몇 개의 클래스를 수정해야 하는가?

세 번째 질문에 "하나만 고치면 된다(파싱 담당 클래스만)"고 답할 수 있다면, 이는 관심사가 잘 분리됐다는 신호다. 반대로 "거의 다 고쳐야 한다"고 답한다면, 아직 결합도가 높다는 뜻이며 이는 20장에서 다루는 의존성 주입으로 더 개선할 수 있는 여지다.

## 흔한 실수

리팩토링을 처음 연습할 때 가장 흔한 실수는 **한 번에 너무 많이 바꾸는 것**이다. 이름 변경, 클래스 분리, 자료구조 교체를 동시에 진행하면 어느 지점에서 버그가 생겼는지 추적하기 어렵고, 테스트 없이 진행했다면 되돌리기도 어렵다. 실무에서는 리팩토링을 작은 단계로 쪼개고, 각 단계마다 기존 테스트(또는 최소한 수동 실행 확인)를 통과하는지 확인한 뒤 다음 단계로 넘어간다. 이 습관은 16장에서 다루는 TDD, 23장에서 다루는 점진적 리팩토링 전략과 직접 연결된다.

또 다른 흔한 실수는 **리팩토링과 기능 추가를 한 커밋에 섞는 것**이다. 리뷰어 입장에서는 "이름을 바꾼 것"과 "로직을 바꾼 것"이 뒤섞인 diff는 검토하기 매우 어렵다. 리팩토링 커밋과 기능 커밋을 분리하면, 문제가 생겼을 때 원인을 훨씬 빠르게 좁힐 수 있다.

## 다음 장에서는

[03장: 의미있는 이름 짓기](/post/clean-code/meaningful-naming-conventions-variables-functions/)에서는 이 실습에서 다룬 "의도가 드러나지 않는 이름" 문제를 체계적인 네이밍 원칙으로 정리한다.

## 평가 기준

- [ ] 코드를 읽고 매직 넘버, 모호한 이름, 다중 책임 함수 등 나쁜 코드의 구체적 증상을 최소 세 가지 이상 식별할 수 있다.
- [ ] 하나의 증상씩 순서대로 제거하는 단계적 리팩토링 방법을 실제 코드에 적용할 수 있다.
- [ ] 리팩토링 결과가 결합도를 실제로 낮췄는지 "데이터 소스가 바뀐다면 몇 곳을 고쳐야 하는가"와 같은 질문으로 검증할 수 있다.
- [ ] 리팩토링과 기능 추가를 커밋 단위에서 분리해야 하는 이유를 설명할 수 있다.

## 참고 및 출처

- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall. 1장.
- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.). Addison-Wesley.
- [Refactoring.Guru — 리팩토링 카탈로그](https://refactoring.guru/refactoring)
