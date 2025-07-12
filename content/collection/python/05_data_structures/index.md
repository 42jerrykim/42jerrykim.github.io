---
draft: true
title: "05. 자료구조"
description: "리스트, 튜플, 딕셔너리, 세트 등 파이썬의 내장 자료구조"
collection_order: 5
---

# 챕터 5: 자료구조

> "적절한 자료구조 선택은 효율적인 프로그램의 첫걸음" - 데이터를 체계적으로 관리하는 방법을 익혀봅시다.

## 학습 목표
- 파이썬의 내장 자료구조 특성을 이해할 수 있다
- 상황에 맞는 적절한 자료구조를 선택할 수 있다
- 각 자료구조의 메서드와 연산을 활용할 수 있다
- 자료구조의 성능 특성을 파악할 수 있다

## 리스트 (List)

### 기본 연산

```python
# 리스트 생성
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# 요소 추가
fruits.append("orange")        # 끝에 추가
fruits.insert(1, "grape")      # 특정 위치에 추가
fruits.extend(["kiwi", "mango"]) # 여러 요소 추가

# 요소 제거
fruits.remove("banana")        # 값으로 제거
last_fruit = fruits.pop()      # 마지막 요소 제거 후 반환
fruits.pop(0)                 # 특정 인덱스 제거

# 리스트 조작
fruits.sort()                 # 정렬
fruits.reverse()              # 뒤집기
count = fruits.count("apple") # 개수 세기
```

### 리스트 컴프리헨션

```python
# 기본 형태
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 조건부 컴프리헨션
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 중첩 루프
matrix = [[i*j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
```

## 튜플 (Tuple)

```python
# 튜플 생성
point = (3, 4)
colors = ("red", "green", "blue")
single = (42,)  # 단일 요소 튜플은 콤마 필요

# 튜플 언패킹
x, y = point
first, *middle, last = (1, 2, 3, 4, 5)
print(x, y)           # 3 4
print(first, middle, last)  # 1 [2, 3, 4] 5

# 네임드 튜플
from collections import namedtuple
Person = namedtuple('Person', ['name', 'age', 'city'])
p = Person('Alice', 30, 'Seoul')
print(p.name, p.age)  # Alice 30
```

## 딕셔너리 (Dictionary)

```python
# 딕셔너리 생성
student = {"name": "Alice", "age": 20, "grade": "A"}
scores = dict(math=90, english=85, science=92)

# 요소 접근 및 수정
student["age"] = 21
student["major"] = "Computer Science"

# 안전한 접근
age = student.get("age", 0)  # 키가 없으면 기본값 반환
major = student.setdefault("major", "Undecided")

# 딕셔너리 메서드
keys = student.keys()     # 키 목록
values = student.values() # 값 목록
items = student.items()   # 키-값 쌍

# 딕셔너리 컴프리헨션
squared_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

## 세트 (Set)

```python
# 세트 생성
fruits = {"apple", "banana", "cherry"}
numbers = set([1, 2, 3, 3, 4, 4, 5])  # 중복 자동 제거

# 세트 연산
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

union = set1 | set2           # 합집합: {1, 2, 3, 4, 5, 6}
intersection = set1 & set2    # 교집합: {3, 4}
difference = set1 - set2      # 차집합: {1, 2}

# 세트 메서드
fruits.add("orange")          # 요소 추가
fruits.remove("banana")       # 요소 제거 (없으면 오류)
fruits.discard("grape")       # 요소 제거 (없어도 OK)
```

## 실습 프로젝트

### 🛠️ 학생 성적 관리 시스템

```python
class StudentManager:
    def __init__(self):
        self.students = {}
    
    def add_student(self, name, scores):
        """학생과 점수 추가"""
        self.students[name] = scores
    
    def get_average(self, name):
        """학생의 평균 점수"""
        if name in self.students:
            return sum(self.students[name]) / len(self.students[name])
        return None
    
    def get_top_students(self, n=3):
        """상위 n명의 학생"""
        averages = {name: self.get_average(name) 
                   for name in self.students}
        sorted_students = sorted(averages.items(), 
                               key=lambda x: x[1], reverse=True)
        return sorted_students[:n]
    
    def get_subject_stats(self, subject_index):
        """특정 과목의 통계"""
        scores = [scores[subject_index] 
                 for scores in self.students.values() 
                 if subject_index < len(scores)]
        
        if scores:
            return {
                'max': max(scores),
                'min': min(scores),
                'avg': sum(scores) / len(scores)
            }
        return None

# 사용 예제
manager = StudentManager()
manager.add_student("Alice", [90, 85, 92])
manager.add_student("Bob", [78, 90, 88])
manager.add_student("Charlie", [95, 89, 94])

print(f"Alice 평균: {manager.get_average('Alice'):.1f}")
print(f"상위 3명: {manager.get_top_students()}")
```

### 🛠️ 단어 빈도 분석기

```python
from collections import Counter
import re

def analyze_text(text):
    """텍스트 분석 함수"""
    # 단어 추출 (영문자만)
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    # 빈도 계산
    word_count = Counter(words)
    
    # 고유 단어 수
    unique_words = len(set(words))
    
    # 가장 빈번한 단어들
    most_common = word_count.most_common(5)
    
    return {
        'total_words': len(words),
        'unique_words': unique_words,
        'most_common': most_common,
        'word_frequencies': dict(word_count)
    }

# 사용 예제
text = """Python is a great programming language. 
Python is easy to learn and Python is powerful."""

result = analyze_text(text)
print(f"총 단어 수: {result['total_words']}")
print(f"고유 단어 수: {result['unique_words']}")
print(f"빈번한 단어: {result['most_common']}")
```

## 체크리스트

### ✅ 기본 자료구조
- [ ] 리스트 생성, 수정, 삭제 가능
- [ ] 튜플의 불변성 이해
- [ ] 딕셔너리 키-값 조작
- [ ] 세트의 중복 제거 특성 활용

### ✅ 고급 활용
- [ ] 컴프리헨션 문법 숙달
- [ ] 자료구조 간 변환
- [ ] 중첩 구조 처리
- [ ] 상황별 적절한 자료구조 선택

### ✅ 성능 고려
- [ ] 시간 복잡도 이해
- [ ] 메모리 효율성 고려
- [ ] 내장 함수 활용
- [ ] collections 모듈 활용

## 다음 단계

🎉 **축하합니다!** 파이썬 자료구조를 마스터했습니다.

이제 [06. 파일 입출력](../06_file_io/)으로 넘어가서 파일과 외부 데이터를 처리하는 방법을 학습해봅시다.

---

💡 **팁:**
- 리스트는 순서가 중요할 때, 세트는 중복 제거가 필요할 때
- 딕셔너리는 빠른 검색이 필요할 때 사용하세요
- 컴프리헨션은 간결하지만 가독성도 고려하세요
- 큰 데이터에서는 성능을 고려한 자료구조를 선택하세요 