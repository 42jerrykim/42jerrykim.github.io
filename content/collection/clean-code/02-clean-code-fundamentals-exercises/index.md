---
draft: true
title: "clean-code"
---
# Chapter 1: Clean Code 개념과 중요성 - 실습 과제

## 실습 개요
이 실습은 Clean Code의 개념을 이해하고 실제 코드에서 품질을 평가하며 개선 방향을 설정하는 것을 목표로 합니다.

## 실습 1: 코드 품질 분석 (40분)

### 목표
자신이 작성한 코드 중 가장 나쁜 코드와 가장 좋은 코드를 선정하여 Clean Code 관점에서 분석합니다.

### 분석 대상 예시 코드

#### 나쁜 코드 예시
```java
// Bad Code Example - 학생 성적 처리 시스템
public class StudentGradeProcessor {
    public void processStudentGrades() {
        ArrayList<String> students = new ArrayList<>();
        students.add("John,85,90,78");
        students.add("Jane,92,88,95");
        students.add("Bob,76,82,89");
        
        for (int i = 0; i < students.size(); i++) {
            String[] parts = students.get(i).split(",");
            String n = parts[0];
            int s1 = Integer.parseInt(parts[1]);
            int s2 = Integer.parseInt(parts[2]);
            int s3 = Integer.parseInt(parts[3]);
            double avg = (s1 + s2 + s3) / 3.0;
            String grade;
            if (avg >= 90) {
                grade = "A";
            } else if (avg >= 80) {
                grade = "B";
            } else if (avg >= 70) {
                grade = "C";
            } else if (avg >= 60) {
                grade = "D";
            } else {
                grade = "F";
            }
            System.out.println(n + ": " + avg + " (" + grade + ")");
        }
    }
}
```

#### 좋은 코드 예시
```java
// Good Code Example - 리팩토링된 학생 성적 처리 시스템
public class Student {
    private final String name;
    private final List<Integer> scores;
    
    public Student(String name, List<Integer> scores) {
        this.name = name;
        this.scores = new ArrayList<>(scores);
    }
    
    public String getName() {
        return name;
    }
    
    public double calculateAverage() {
        return scores.stream()
                     .mapToInt(Integer::intValue)
                     .average()
                     .orElse(0.0);
    }
    
    public Grade getLetterGrade() {
        double average = calculateAverage();
        return Grade.fromAverage(average);
    }
}

public enum Grade {
    A(90), B(80), C(70), D(60), F(0);
    
    private final int threshold;
    
    Grade(int threshold) {
        this.threshold = threshold;
    }
    
    public static Grade fromAverage(double average) {
        for (Grade grade : values()) {
            if (average >= grade.threshold) {
                return grade;
            }
        }
        return F;
    }
}

public class GradeReporter {
    public void printGradeReport(List<Student> students) {
        students.forEach(this::printStudentGrade);
    }
    
    private void printStudentGrade(Student student) {
        double average = student.calculateAverage();
        Grade grade = student.getLetterGrade();
        System.out.printf("%s: %.1f (%s)%n", 
                         student.getName(), average, grade);
    }
}

public class StudentGradeProcessor {
    private final StudentDataParser parser;
    private final GradeReporter reporter;
    
    public StudentGradeProcessor() {
        this.parser = new StudentDataParser();
        this.reporter = new GradeReporter();
    }
    
    public void processStudentGrades(List<String> studentData) {
        List<Student> students = parser.parseStudentData(studentData);
        reporter.printGradeReport(students);
    }
}
```

### 분석 과제
다음 관점에서 두 코드를 비교 분석하세요:

1. **가독성**: 코드를 읽고 이해하기 얼마나 쉬운가?
2. **유지보수성**: 요구사항 변경 시 수정하기 얼마나 쉬운가?
3. **재사용성**: 다른 곳에서 사용하기 얼마나 쉬운가?
4. **테스트 가능성**: 단위 테스트를 작성하기 얼마나 쉬운가?

### 분석 템플릿
```markdown
## 나쁜 코드 분석
### 문제점:
- [ ] 긴 메서드 (한 메서드에서 너무 많은 일을 함)
- [ ] 의미 없는 변수명 (n, s1, s2, s3)
- [ ] 매직 넘버 사용 (90, 80, 70, 60)
- [ ] 단일 책임 원칙 위반
- [ ] 하드코딩된 데이터

### 개선이 필요한 이유:
1. 
2. 
3. 

## 좋은 코드 분석
### 장점:
- [ ] 명확한 클래스와 메서드 이름
- [ ] 단일 책임 원칙 준수
- [ ] enum을 통한 상수 관리
- [ ] 스트림 API 활용
- [ ] 의존성 주입 패턴

### Clean Code 원칙 적용:
1. 
2. 
3. 
```

## 실습 2: Clean Code 정의 재작성 (20분)

### 목표
학습한 내용을 바탕으로 자신만의 언어로 Clean Code를 재정의합니다.

### 작업 과제
1. **개인 정의 작성**
   - Clean Code가 무엇인지 본인의 경험을 바탕으로 정의
   - 왜 Clean Code가 중요한지 구체적인 이유 설명

2. **핵심 원칙 도출**
   - Clean Code의 핵심 원칙 3-5가지 선정
   - 각 원칙에 대한 간단한 예시 제시

### 정의 템플릿
```markdown
## 나만의 Clean Code 정의

### Clean Code란?
Clean Code는 _________________________________ 
이다. 왜냐하면 _____________________________

### 핵심 원칙
1. **[원칙명]**: [설명]
   - 예시: 
   
2. **[원칙명]**: [설명]
   - 예시:
   
3. **[원칙명]**: [설명]
   - 예시:

### 개인 경험과 연결
이전에 작성했던 코드 중에서 _________________ 
경험이 있었는데, 이는 Clean Code 원칙 중 _______
를 위반한 사례였다.
```

## 실습 3: 팀 프로젝트 코드 품질 개선 계획 (30분)

### 목표
현재 진행 중인 팀 프로젝트에서 코드 품질을 개선하기 위한 구체적인 계획을 수립합니다.

### 현황 분석 체크리스트
```markdown
## 현재 프로젝트 코드 품질 체크리스트

### 네이밍
- [ ] 변수명이 의도를 명확히 표현하는가?
- [ ] 함수명이 하는 일을 정확히 설명하는가?
- [ ] 클래스명이 책임을 잘 나타내는가?

### 함수
- [ ] 함수가 한 가지 일만 하는가?
- [ ] 함수의 크기가 적절한가? (20줄 이내)
- [ ] 함수 인수의 개수가 적절한가? (3개 이하)

### 주석
- [ ] 코드 자체로 의도를 표현하고 있는가?
- [ ] 불필요한 주석이 없는가?
- [ ] 주석이 코드와 일치하는가?

### 형식
- [ ] 일관된 들여쓰기를 사용하는가?
- [ ] 적절한 빈 줄로 코드 블록을 구분하는가?
- [ ] 팀 내에서 합의된 스타일을 따르는가?

### 객체와 자료구조
- [ ] 객체와 자료구조를 적절히 구분해서 사용하는가?
- [ ] 디미터 법칙을 준수하는가?
- [ ] 불필요한 getter/setter가 없는가?
```

### 개선 계획 템플릿
```markdown
## 코드 품질 개선 계획

### 현재 문제점 분석
| 영역 | 문제점 | 심각도 (1-5) | 영향도 |
|------|---------|---------------|---------|
| 네이밍 | 변수명이 모호함 | 4 | 가독성 저하 |
| 함수 | 긴 함수가 많음 | 5 | 유지보수 어려움 |
| 주석 | 과도한 주석 사용 | 3 | 코드 복잡성 증가 |

### 개선 우선순위
1. **1순위**: [가장 시급한 문제]
   - 이유: 
   - 예상 소요 시간: 
   - 담당자: 

2. **2순위**: [두 번째 문제]
   - 이유: 
   - 예상 소요 시간: 
   - 담당자: 

### 실행 계획
#### 단기 계획 (1주일)
- [ ] 새로 작성하는 코드에 네이밍 규칙 적용
- [ ] 함수 길이 20줄 이내로 제한
- [ ] 코드 리뷰 시 Clean Code 체크리스트 활용

#### 중기 계획 (1개월)
- [ ] 기존 코드 중 핵심 모듈 리팩토링
- [ ] 팀 코딩 컨벤션 문서 작성
- [ ] 자동화 도구 도입 (Linter, Formatter)

#### 장기 계획 (3개월)
- [ ] 전체 코드베이스 리팩토링
- [ ] 테스트 코드 작성
- [ ] 지속적인 코드 품질 모니터링 체계 구축

### 성공 지표
- 코드 리뷰 시간 50% 단축
- 버그 발생률 30% 감소
- 새로운 기능 개발 속도 20% 향상
```

## 평가 기준

### 실습 1: 코드 분석 (40점)
- Clean Code 관점에서의 정확한 분석 (20점)
- 구체적인 개선점 제시 (10점)
- 분석의 논리적 일관성 (10점)

### 실습 2: 정의 재작성 (30점)
- 개인적 이해도가 잘 반영된 정의 (15점)
- 핵심 원칙의 적절성 (10점)
- 경험과의 연결 (5점)

### 실습 3: 개선 계획 (30점)
- 현황 분석의 정확성 (10점)
- 실행 가능한 개선 계획 (15점)
- 측정 가능한 성공 지표 (5점)

## 제출 형식
- 파일명: `01_clean-code-fundamentals_실습_[이름].md`
- 제출 기한: 다음 강의 시작 전
- 형식: Markdown 문서

## 추가 자료
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [PEP 8 - Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Martin Fowler의 "Refactoring" 관련 블로그 글 