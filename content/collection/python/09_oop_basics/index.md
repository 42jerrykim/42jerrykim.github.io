---
draft: true
title: "09. 객체지향 프로그래밍 기초"
description: "클래스/객체/메서드의 기본 개념과 캡슐화 원리를 학습합니다. 특수 메서드와 객체 모델 기초를 통해 파이썬 OOP 코드를 읽고 작성하는 기반을 만듭니다."
tags:
  - Python
  - 파이썬
  - Implementation
  - Software-Architecture
  - Algorithm
  - 알고리즘
  - backend
  - 백엔드
  - Best-Practices
  - clean-code
  - 클린코드
  - refactoring
  - 리팩토링
  - testing
  - 테스트
  - debugging
  - 디버깅
  - logging
  - 로깅
  - security
  - 보안
  - Performance
  - 성능
  - concurrency
  - 동시성
  - async
  - 비동기
  - oop
  - 객체지향
  - Data-Structures
  - 자료구조
  - DevOps
  - deployment
  - 배포
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - web
  - 웹
  - database
  - 데이터베이스
  - networking
  - 네트워킹
  - CI-CD
  - 자동화
  - Documentation
  - 문서화
  - Git
  - Code-Quality
  - 코드품질
lastmod: 2026-01-17
collection_order: 9
---
# 챕터 9: 객체지향 프로그래밍 기초

> "모든 것은 객체다" - 현실 세계를 코드로 모델링하는 강력한 패러다임을 익혀봅시다.

## 학습 목표
- 객체지향 프로그래밍의 개념을 이해할 수 있다
- 클래스를 정의하고 객체를 생성할 수 있다
- 인스턴스 변수와 메서드를 활용할 수 있다
- 생성자와 소멸자를 적절히 사용할 수 있다

## 핵심 개념(이론)

### 1) 객체지향 프로그래밍 기초의 역할과 경계
이 챕터의 핵심은 “무엇을 할 수 있나”가 아니라, **어떤 문제를 해결하고 어디까지 책임지는지**를 분명히 하는 것입니다.
경계가 흐리면 코드는 커질수록 결합이 늘어나고 수정 비용이 커집니다.

### 2) 왜 이 개념이 필요한가(실무 동기)
실무에서는 예외 상황, 성능, 협업, 테스트가 항상 문제를 만듭니다.
따라서 이 주제는 기능이 아니라 **품질(신뢰성/유지보수성/보안)**을 위한 기반으로 이해해야 합니다.

### 3) 트레이드오프: 간단함 vs 확장성
대부분의 선택은 “더 단순하게”와 “더 확장 가능하게” 사이에서 균형을 잡는 일입니다.
초기에는 단순함을, 장기 운영/팀 협업이 커질수록 확장성을 더 우선합니다.

### 4) 실패 모드(Failure Modes)를 먼저 생각하라
무엇이 실패하는지(입력, I/O, 동시성, 외부 시스템)를 먼저 떠올리면 설계가 안정적으로 변합니다.
이 챕터의 예제는 실패 모드를 축소해서 보여주므로, 실제 적용 시에는 더 많은 방어가 필요합니다.

### 5) 학습 포인트: 외우지 말고 “판단 기준”을 남겨라
핵심은 API를 외우는 것이 아니라, “언제 무엇을 선택할지” 판단 기준을 정리하는 것입니다.
이 기준이 쌓이면 새로운 라이브러리/도구가 나와도 빠르게 적응할 수 있습니다.

## 선택 기준(Decision Guide)
- 기본은 **가독성/명확성** 우선(최적화는 측정 이후).
- 외부 의존이 늘수록 **경계/추상화**와 **테스트**를 먼저 강화.
- 복잡도가 증가하면 “규칙을 코드로”가 아니라 “구조로” 담는 방향을 고려.

## 흔한 오해/주의점
- 도구/문법이 곧 실력이라는 오해가 있습니다. 실력은 문제를 단순화하고 구조화하는 능력입니다.
- 극단적 최적화/과설계는 학습과 유지보수를 방해할 수 있습니다.

## 요약
- 객체지향 프로그래밍 기초는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 클래스와 객체

### 기본 클래스 정의

```python
class Person:
    """사람을 나타내는 클래스"""
    
    # 클래스 변수 (모든 인스턴스가 공유)
    species = "Homo sapiens"
    
    def __init__(self, name, age):
        """생성자 메서드"""
        self.name = name    # 인스턴스 변수
        self.age = age      # 인스턴스 변수
    
    def introduce(self):
        """자기소개 메서드"""
        return f"안녕하세요, 저는 {self.name}이고 {self.age}세입니다."
    
    def birthday(self):
        """생일 메서드"""
        self.age += 1
        return f"{self.name}님, 생일 축하합니다! 이제 {self.age}세입니다."

# 객체 생성
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

# 메서드 호출
print(person1.introduce())  # 안녕하세요, 저는 Alice이고 25세입니다.
print(person1.birthday())   # Alice님, 생일 축하합니다! 이제 26세입니다.

# 클래스 변수 접근
print(Person.species)       # Homo sapiens
print(person1.species)      # Homo sapiens
```

### 캡슐화와 프라이빗 속성

```python
class BankAccount:
    def __init__(self, account_number, owner, balance=0):
        self.account_number = account_number
        self.owner = owner
        self._balance = balance  # protected (관례상 비공개)
        self.__pin = "1234"     # private (이름 맹글링)
    
    def deposit(self, amount):
        """입금"""
        if amount > 0:
            self._balance += amount
            return f"{amount}원이 입금되었습니다. 잔액: {self._balance}원"
        return "입금액은 0보다 커야 합니다."
    
    def withdraw(self, amount, pin):
        """출금"""
        if pin != self.__pin:
            return "PIN이 틀렸습니다."
        
        if amount > self._balance:
            return "잔액이 부족합니다."
        
        if amount > 0:
            self._balance -= amount
            return f"{amount}원이 출금되었습니다. 잔액: {self._balance}원"
        
        return "출금액은 0보다 커야 합니다."
    
    def get_balance(self):
        """잔액 조회"""
        return self._balance
    
    @property
    def balance(self):
        """프로퍼티를 통한 안전한 잔액 접근"""
        return self._balance

# 사용 예제
account = BankAccount("123-456", "Alice", 1000)
print(account.deposit(500))     # 500원이 입금되었습니다. 잔액: 1500원
print(account.withdraw(200, "1234"))  # 200원이 출금되었습니다. 잔액: 1300원
print(f"현재 잔액: {account.balance}원")  # 현재 잔액: 1300원
```

## 특수 메서드 (매직 메서드)

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        """문자열 표현 (사용자용)"""
        return f"Vector({self.x}, {self.y})"
    
    def __repr__(self):
        """문자열 표현 (개발자용)"""
        return f"Vector({self.x!r}, {self.y!r})"
    
    def __add__(self, other):
        """벡터 덧셈"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __eq__(self, other):
        """벡터 동등성 비교"""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False
    
    def __len__(self):
        """벡터의 크기"""
        return int((self.x ** 2 + self.y ** 2) ** 0.5)

# 사용 예제
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1)           # Vector(3, 4)
print(v1 + v2)      # Vector(4, 6)
print(v1 == v2)     # False
print(len(v1))      # 5
```

## 실습 프로젝트

###️ 학생 관리 시스템

```python
class Student:
    def __init__(self, student_id, name, grade=1):
        self.student_id = student_id
        self.name = name
        self.grade = grade
        self.subjects = {}  # 과목별 점수
    
    def add_subject(self, subject, score):
        """과목 점수 추가"""
        if 0 <= score <= 100:
            self.subjects[subject] = score
            return f"{subject} 과목에 {score}점이 등록되었습니다."
        return "점수는 0-100 사이여야 합니다."
    
    def get_average(self):
        """평균 점수 계산"""
        if not self.subjects:
            return 0
        return sum(self.subjects.values()) / len(self.subjects)
    
    def get_grade_letter(self):
        """학점 계산"""
        avg = self.get_average()
        if avg >= 90: return 'A'
        elif avg >= 80: return 'B'
        elif avg >= 70: return 'C'
        elif avg >= 60: return 'D'
        else: return 'F'
    
    def __str__(self):
        avg = self.get_average()
        grade = self.get_grade_letter()
        return f"학생: {self.name} (ID: {self.student_id}), 평균: {avg:.1f}, 학점: {grade}"

class StudentManager:
    def __init__(self):
        self.students = {}
    
    def add_student(self, student):
        """학생 추가"""
        self.students[student.student_id] = student
        return f"{student.name} 학생이 등록되었습니다."
    
    def find_student(self, student_id):
        """학생 검색"""
        return self.students.get(student_id)
    
    def get_top_students(self, n=3):
        """상위 학생들"""
        sorted_students = sorted(
            self.students.values(),
            key=lambda s: s.get_average(),
            reverse=True
        )
        return sorted_students[:n]
    
    def get_statistics(self):
        """전체 통계"""
        if not self.students:
            return "등록된 학생이 없습니다."
        
        averages = [s.get_average() for s in self.students.values()]
        return {
            'total_students': len(self.students),
            'class_average': sum(averages) / len(averages),
            'highest_score': max(averages),
            'lowest_score': min(averages)
        }

# 사용 예제
manager = StudentManager()

# 학생 생성 및 등록
alice = Student("2024001", "Alice")
bob = Student("2024002", "Bob")

alice.add_subject("수학", 95)
alice.add_subject("영어", 87)
alice.add_subject("과학", 92)

bob.add_subject("수학", 78)
bob.add_subject("영어", 85)
bob.add_subject("과학", 90)

manager.add_student(alice)
manager.add_student(bob)

print(alice)  # 학생: Alice (ID: 2024001), 평균: 91.3, 학점: A
print(bob)    # 학생: Bob (ID: 2024002), 평균: 84.3, 학점: B

# 통계 확인
stats = manager.get_statistics()
print(f"전체 학생 수: {stats['total_students']}")
print(f"반 평균: {stats['class_average']:.1f}")
```

###️ 도서관 관리 시스템

```python
from datetime import datetime, timedelta

class Book:
    def __init__(self, isbn, title, author, copies=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies
        self.borrowed_by = []  # (대출자, 대출일, 반납예정일)
    
    def is_available(self):
        """대출 가능 여부"""
        return self.available_copies > 0
    
    def borrow(self, borrower, days=14):
        """도서 대출"""
        if not self.is_available():
            return False, "대출 가능한 책이 없습니다."
        
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=days)
        
        self.borrowed_by.append((borrower, borrow_date, due_date))
        self.available_copies -= 1
        
        return True, f"대출 완료. 반납 예정일: {due_date.strftime('%Y-%m-%d')}"
    
    def return_book(self, borrower):
        """도서 반납"""
        for i, (name, borrow_date, due_date) in enumerate(self.borrowed_by):
            if name == borrower:
                self.borrowed_by.pop(i)
                self.available_copies += 1
                
                # 연체료 계산
                today = datetime.now()
                if today > due_date:
                    overdue_days = (today - due_date).days
                    fee = overdue_days * 100  # 하루당 100원
                    return True, f"반납 완료. 연체료: {fee}원"
                
                return True, "반납 완료."
        
        return False, "대출 기록이 없습니다."
    
    def __str__(self):
        return f"『{self.title}』 - {self.author} (대출가능: {self.available_copies}/{self.total_copies})"

class Library:
    def __init__(self, name):
        self.name = name
        self.books = {}  # ISBN을 키로 하는 도서 딕셔너리
    
    def add_book(self, book):
        """도서 추가"""
        if book.isbn in self.books:
            # 기존 도서의 사본 추가
            self.books[book.isbn].total_copies += book.total_copies
            self.books[book.isbn].available_copies += book.available_copies
        else:
            self.books[book.isbn] = book
        
        return f"도서가 추가되었습니다: {book.title}"
    
    def find_book(self, title=None, author=None, isbn=None):
        """도서 검색"""
        results = []
        
        for book in self.books.values():
            if isbn and book.isbn == isbn:
                return [book]
            
            if title and title.lower() in book.title.lower():
                results.append(book)
            elif author and author.lower() in book.author.lower():
                results.append(book)
        
        return results
    
    def borrow_book(self, isbn, borrower):
        """도서 대출"""
        if isbn in self.books:
            return self.books[isbn].borrow(borrower)
        return False, "해당 도서를 찾을 수 없습니다."
    
    def return_book(self, isbn, borrower):
        """도서 반납"""
        if isbn in self.books:
            return self.books[isbn].return_book(borrower)
        return False, "해당 도서를 찾을 수 없습니다."

# 사용 예제
library = Library("중앙도서관")

# 도서 추가
book1 = Book("978-1234567890", "파이썬 완전정복", "김개발", 3)
book2 = Book("978-0987654321", "데이터 구조와 알고리즘", "이코딩", 2)

library.add_book(book1)
library.add_book(book2)

# 도서 검색
python_books = library.find_book(title="파이썬")
print(f"검색 결과: {len(python_books)}권")

# 도서 대출
success, message = library.borrow_book("978-1234567890", "Alice")
print(message)

# 도서 목록
for book in library.books.values():
    print(book)
```

## 체크리스트

### 기본 OOP 개념
- [ ] 클래스와 객체의 차이 이해
- [ ] 생성자(__init__) 활용
- [ ] 인스턴스 변수와 메서드 구분
- [ ] self 매개변수의 역할 이해

### 고급 기능
- [ ] 클래스 변수와 인스턴스 변수 구분
- [ ] 프라이빗 속성(_var, __var) 활용
- [ ] 프로퍼티(@property) 사용
- [ ] 특수 메서드 구현

### 실무 활용
- [ ] 실제 문제를 클래스로 모델링
- [ ] 적절한 캡슐화 적용
- [ ] 메서드의 단일 책임 원칙
- [ ] 코드 재사용성 고려

## 다음 단계

🎉 **축하합니다!** 객체지향 프로그래밍 기초를 마스터했습니다.

이제 [10. 객체지향 프로그래밍 고급](../10_oop_advanced/)으로 넘어가서 상속, 다형성, 추상화 등 고급 OOP 개념을 학습해봅시다.

---

💡 **팁:**
- 클래스는 명사로, 메서드는 동사로 이름을 짓세요
- 하나의 클래스는 하나의 책임만 가지도록 설계하세요
- 캡슐화를 통해 내부 구현을 숨기고 인터페이스를 명확히 하세요
- 실제 세계의 객체를 모델링할 때 추상화를 적절히 활용하세요 
