---
draft: true
title: "04. 함수"
description: "함수 정의, 매개변수, 반환값, 스코프 이해"
collection_order: 4
---

# 챕터 4: 함수

> "Don't Repeat Yourself (DRY)" - 함수는 코드의 재사용성과 가독성을 극대화하는 핵심 도구입니다.

## 학습 목표
- 함수를 정의하고 호출할 수 있다
- 매개변수와 인수의 다양한 형태를 이해할 수 있다
- 스코프와 네임스페이스를 파악할 수 있다
- 람다 함수와 고차 함수를 활용할 수 있다

## 함수 기본

### 함수 정의와 호출

<function_calls>
<invoke name="create_diagram">
<parameter name="content">flowchart TD
    A["함수 정의<br/>def function_name():"] --> B["함수 호출<br/>function_name()"]
    B --> C["매개변수 전달<br/>function_name(arg1, arg2)"]
    C --> D["반환값 받기<br/>result = function_name()"]
    
    E["함수 구조"] --> F["def 키워드"]
    E --> G["함수명"]
    E --> H["매개변수 ()"]
    E --> I["콜론 :"]
    E --> J["들여쓰기 된 코드 블록"]
    E --> K["return 문 (선택사항)"]
    
    style A fill:#e8f5e8
    style B fill:#fff2cc
    style C fill:#e1f5fe
    style D fill:#fce4ec
</code_block_to_apply_changes_from>
</invoke>
</function_calls>

## 핵심 내용

### 함수 기본
- **함수 정의**: def 키워드 사용법
- **함수 호출**: 매개변수 전달 방식
- **반환값**: return 문 활용
- **독스트링**: 함수 문서화

### 매개변수와 인수
- **위치 인수**: 순서 기반 전달
- **키워드 인수**: 이름 기반 전달
- **기본값 매개변수**: 선택적 인수 처리
- **가변 인수**: *args, **kwargs 활용

### 스코프와 네임스페이스
- **지역 스코프**: 함수 내부 변수
- **전역 스코프**: 모듈 레벨 변수
- **global 키워드**: 전역 변수 수정
- **nonlocal 키워드**: 중첩 함수 변수 접근

### 고급 함수 개념
- **람다 함수**: 익명 함수 정의
- **고차 함수**: 함수를 인수로 받는 함수
- **내장 고차 함수**: map(), filter(), reduce()
- **함수 내 함수**: 중첩 함수 정의

### 함수형 프로그래밍 기초
- **순수 함수**: 부작용 없는 함수
- **재귀 함수**: 자기 자신을 호출하는 함수
- **클로저**: 변수 캡처 메커니즘
- **함수 디코레이터**: 함수 기능 확장

## 실습 프로젝트
1. 수학 함수 라이브러리 (기본 함수)
2. 문자열 처리 도구 (매개변수 활용)
3. 재귀를 활용한 팩토리얼 계산기
4. 함수형 프로그래밍 스타일 데이터 처리

## 체크리스트
- [ ] 함수 정의와 호출 능숙
- [ ] 매개변수 종류별 사용법 이해
- [ ] 스코프 규칙 파악
- [ ] 람다 함수 활용
- [ ] 재귀 함수 구현 능력

## 다음 단계
함수를 마스터했다면, 데이터를 효과적으로 저장하고 조작하는 자료구조를 학습합니다. 

# 스코프 예제
global_var = "전역 변수"

def outer_function():
    outer_var = "외부 함수 변수"
    
    def inner_function():
        inner_var = "내부 함수 변수"
        print(f"내부에서 접근: {global_var}, {outer_var}, {inner_var}")
    
    inner_function()
    print(f"외부에서 접근: {global_var}, {outer_var}")

outer_function()

# global 키워드
counter = 0

def increment():
    global counter  # 전역 변수 수정
    counter += 1
    return counter

print(increment())  # 1
print(increment())  # 2

## 람다 함수와 고차 함수

# 람다 함수 기본
square = lambda x: x ** 2
print(square(5))  # 25

# 여러 매개변수
add = lambda x, y: x + y
print(add(3, 7))  # 10

# 고차 함수 활용
numbers = [1, 2, 3, 4, 5]

# map() - 모든 요소에 함수 적용
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]

# filter() - 조건에 맞는 요소만 필터링
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4]

# sorted() - 사용자 정의 키로 정렬
students = [("Alice", 85), ("Bob", 90), ("Charlie", 78)]
sorted_by_score = sorted(students, key=lambda student: student[1])
print(sorted_by_score)  # [('Charlie', 78), ('Alice', 85), ('Bob', 90)]

## 재귀 함수

# 팩토리얼 계산 (재귀)
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

print(factorial(5))  # 120

# 피보나치 수열 (재귀)
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

print([fibonacci(i) for i in range(10)])  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

## 실습 프로젝트

###️ 프로젝트: 수학 라이브러리

import math

def calculator():
    """간단한 계산기 함수 모음"""
    
    def add(a, b):
        """덧셈"""
        return a + b
    
    def multiply(a, b):
        """곱셈"""
        return a * b
    
    def power(base, exponent):
        """거듭제곱"""
        return base ** exponent
    
    def factorial(n):
        """팩토리얼"""
        if n < 0:
            return None
        elif n <= 1:
            return 1
        else:
            return n * factorial(n - 1)
    
    def is_prime(n):
        """소수 판별"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    # 함수들을 딕셔너리로 반환
    return {
        'add': add,
        'multiply': multiply,
        'power': power,
        'factorial': factorial,
        'is_prime': is_prime
    }

# 사용 예제
calc = calculator()
print(f"3 + 5 = {calc['add'](3, 5)}")
print(f"4! = {calc['factorial'](4)}")
print(f"17은 소수? {calc['is_prime'](17)}")

## 체크리스트

### 함수 기본
- [ ] def 키워드로 함수 정의 가능
- [ ] 매개변수와 반환값 활용
- [ ] 독스트링 작성 습관
- [ ] 함수 호출과 결과 처리

### 고급 매개변수
- [ ] 기본값 매개변수 활용
- [ ] *args, **kwargs 사용
- [ ] 키워드 인수 활용
- [ ] 매개변수 순서 규칙 이해

### 스코프와 고급 개념
- [ ] 지역/전역 스코프 이해
- [ ] 람다 함수 활용
- [ ] 재귀 함수 구현
- [ ] 고차 함수 활용

## 다음 단계

🎉 **축하합니다!** 파이썬 함수를 마스터했습니다.

이제 [05. 자료구조](../05_data_structures/)로 넘어가서 리스트, 딕셔너리, 세트 등 파이썬의 강력한 자료구조를 학습해봅시다.

---

💡 **팁:**
- 함수는 하나의 일만 잘하도록 설계하세요
- 의미 있는 함수명과 매개변수명을 사용하세요
- 독스트링으로 함수의 목적을 명확히 하세요
- 부작용을 최소화하는 순수 함수를 지향하세요 