---
draft: true
title: "05. 자료구조"
description: "리스트·튜플·딕셔너리·세트의 특성과 시간복잡도 관점을 함께 설명합니다. 상황별 선택 기준과 파이썬다운 조작 패턴을 통해 데이터 처리를 단단히 만듭니다."
tags:
  - Python
  - Implementation(구현)
  - Software-Architecture(소프트웨어아키텍처)
  - Algorithm(알고리즘)
  - Backend(백엔드)
  - Best-Practices
  - Clean-Code(클린코드)
  - Refactoring(리팩토링)
  - Testing(테스트)
  - Debugging(디버깅)
  - Logging(로깅)
  - Security(보안)
  - Performance(성능)
  - Concurrency(동시성)
  - Async(비동기)
  - OOP(객체지향)
  - Data-Structures(자료구조)
  - DevOps
  - Deployment(배포)
  - Design-Pattern(디자인패턴)
  - Web(웹)
  - Database(데이터베이스)
  - Networking(네트워킹)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Automation(자동화)
  - Documentation(문서화)
  - Git
  - Code-Quality(코드품질)
lastmod: 2026-01-17
collection_order: 5
---
# 챕터 5: 자료구조

> "적절한 자료구조 선택은 효율적인 프로그램의 첫걸음" - 데이터를 체계적으로 관리하는 방법을 익혀봅시다.

## 학습 목표
- 파이썬의 내장 자료구조 특성을 이해할 수 있다
- 상황에 맞는 적절한 자료구조를 선택할 수 있다
- 각 자료구조의 메서드와 연산을 활용할 수 있다
- 자료구조의 성능 특성을 파악할 수 있다

## 핵심 개념(이론)

### 1) 자료구조의 역할과 경계
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
- 자료구조는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 리스트 (List)

리스트(List)는 파이썬에서 가장 널리 쓰이는 가변(mutable) 시퀀스 자료구조로, 내부적으로는 동적 배열(dynamic array)로 구현되어 있어 인덱스로 즉시 접근할 수 있습니다. 요소를 추가·삭제·정렬할 수 있고 서로 다른 타입을 섞어 담을 수 있어 유연하지만, 이 유연성에는 대가가 따릅니다. 배열 끝에 요소를 추가하는 `append`는 평균적으로 O(1)이지만, 맨 앞에 삽입하거나 삭제하면 뒤따르는 모든 요소가 한 칸씩 밀려야 해서 O(n)이 걸립니다.

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

리스트 컴프리헨션(list comprehension)은 `for` 루프와 `append` 호출을 한 줄로 압축하는 문법으로, [PEP 202](https://peps.python.org/pep-0202/)로 도입되었으며 각 반복마다 `append` 메서드를 조회하지 않고 최적화된 바이트코드로 실행되어 동등한 일반 루프보다 빠른 경우가 많습니다. 대괄호 뒤에 `if` 조건을 붙이면 필터링이 되고, 값 자리에 삼항 표현식(`A if 조건 else B`)을 쓰면 조건에 따라 다른 값을 만들 수 있으며, 컴프리헨션을 중첩하면 다차원 구조를 생성하거나 평탄화(flatten)할 수 있습니다.

```python
# 기본 형태
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 조건부 필터링 (뒤쪽 if)
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# 조건부 값 선택 (값 자리의 삼항 표현식)
labels = ["짝수" if x % 2 == 0 else "홀수" for x in range(6)]
# ['짝수', '홀수', '짝수', '홀수', '짝수', '홀수']

# 필터와 변환을 함께 사용
fizz = [x for x in range(1, 16) if x % 3 == 0 or x % 5 == 0]
# [3, 5, 6, 9, 10, 12, 15]

# 중첩 루프: 2차원 행렬 생성
matrix = [[i * j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# 중첩 구조 평탄화(flatten)
nested = [[1, 2], [3, 4], [5, 6]]
flat = [x for row in nested for x in row]
# [1, 2, 3, 4, 5, 6]
```

컴프리헨션은 간결하지만, 조건과 중첩이 늘어날수록 한 줄에 담긴 로직을 해석하는 비용이 커집니다. 하나의 컴프리헨션 안에서 `for` 절이 2개를 넘거나 `if`가 여러 겹 중첩되면, 일반 `for` 루프로 풀어 쓰고 각 단계에 이름을 붙이는 편이 유지보수에 유리합니다.

## 튜플 (Tuple)

튜플(Tuple)은 불변(immutable) 시퀀스로, 한 번 생성되면 요소를 추가·삭제·수정할 수 없습니다. 이 불변성 덕분에 튜플은 해시 가능(hashable)하므로 딕셔너리의 키나 세트의 원소로 쓸 수 있습니다 — 가변 객체인 리스트는 이 용도로 쓸 수 없습니다. 좌표나 RGB 색상 값처럼 "함께 묶여야 의미를 갖고 이후 바뀌지 않는 값의 묶음"을 표현할 때, 튜플은 리스트보다 그 의도를 코드로 분명히 드러냅니다.

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

# 네임드 튜플: 인덱스 대신 이름으로 필드에 접근
from collections import namedtuple
Person = namedtuple('Person', ['name', 'age', 'city'])
p = Person('Alice', 30, 'Seoul')
print(p.name, p.age)   # Alice 30
print(p._asdict())     # {'name': 'Alice', 'age': 30, 'city': 'Seoul'}
p2 = p._replace(age=31)  # 일부 필드만 바꾼 새 인스턴스 생성 (원본 p는 불변)
print(p2)               # Person(name='Alice', age=31, city='Seoul')
```

네임드튜플(namedtuple)은 튜플의 불변성과 메모리 효율을 유지하면서 `point[0]` 대신 `point.x`처럼 이름으로 필드에 접근하게 해 코드의 가독성을 높입니다. `_asdict()`는 딕셔너리로, `_replace()`는 원본을 바꾸지 않고 일부 필드만 다른 새 인스턴스를 만듭니다.

## 딕셔너리 (Dictionary)

딕셔너리(Dictionary)는 해시 테이블(hash table)로 구현된 키-값 매핑으로, 키의 해시값을 이용해 평균 O(1)에 조회·삽입·삭제를 수행합니다. 파이썬 3.7부터는 삽입 순서를 보장하므로 순서가 예측 가능한 매핑이 필요할 때도 딕셔너리를 안심하고 쓸 수 있습니다. 키는 반드시 해시 가능한 불변 객체여야 하므로 문자열·숫자·튜플은 키로 쓸 수 있지만 리스트나 다른 딕셔너리는 쓸 수 없습니다.

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
```

### 딕셔너리 컴프리헨션

딕셔너리 컴프리헨션은 리스트 컴프리헨션과 같은 규칙을 `{키: 값 for ...}` 형태로 적용합니다. 두 시퀀스를 `zip`으로 묶어 매핑을 만들거나, 조건으로 걸러내거나, 키와 값을 뒤바꿔 역매핑을 만드는 패턴이 실무에서 자주 쓰입니다.

```python
# 기본 형태
squared_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 조건부 필터링
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# 두 리스트를 zip으로 묶어 매핑 생성
names = ["Alice", "Bob", "Charlie"]
scores_list = [90, 85, 92]
name_to_score = {name: score for name, score in zip(names, scores_list)}
# {'Alice': 90, 'Bob': 85, 'Charlie': 92}

# 키-값 반전 (역매핑)
score_to_name = {score: name for name, score in name_to_score.items()}
# {90: 'Alice', 85: 'Bob', 92: 'Charlie'}

# 기존 딕셔너리를 조건에 따라 변환
prices = {"apple": 1000, "banana": 1500, "cherry": 3000}
discounted = {item: int(price * 0.9) for item, price in prices.items() if price >= 1500}
# {'banana': 1350, 'cherry': 2700}
```

## 세트 (Set)

세트(Set)는 해시 테이블 기반의 순서 없는 컬렉션으로, 중복을 자동으로 제거하고 `in` 연산자로 멤버십을 평균 O(1)에 검사합니다. 리스트에서 `in`으로 특정 값의 존재 여부를 확인하면 최악의 경우 모든 요소를 순회하는 O(n) 연산이 되지만, 세트는 해시값으로 위치를 바로 찾기 때문에 대량의 데이터에서 중복 제거나 존재 여부 확인이 필요하면 세트가 압도적으로 유리합니다.

```python
# 세트 생성
fruits = {"apple", "banana", "cherry"}
numbers = set([1, 2, 3, 3, 4, 4, 5])  # 중복 자동 제거

# 세트 연산
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

union = set1 | set2                  # 합집합: {1, 2, 3, 4, 5, 6}
intersection = set1 & set2           # 교집합: {3, 4}
difference = set1 - set2             # 차집합: {1, 2}
symmetric = set1 ^ set2              # 대칭차집합: {1, 2, 5, 6}

# 세트 메서드
fruits.add("orange")          # 요소 추가
fruits.remove("banana")       # 요소 제거 (없으면 오류)
fruits.discard("grape")       # 요소 제거 (없어도 OK)
```

### 세트 컴프리헨션

세트 컴프리헨션은 `{식 for ...}` 형태로, 리스트 컴프리헨션과 문법은 같지만 결과에서 중복이 자동으로 제거됩니다. 여러 입력에서 만들어지는 값 중 "고유한 값의 집합"만 필요할 때 사용합니다.

```python
# 기본 형태 (중복 자동 제거)
unique_lengths = {len(word) for word in ["apple", "kiwi", "fig", "plum", "pear"]}
# {3, 4, 5}

# 조건부 필터링과 중첩
vowel_letters = {ch for word in ["hello", "world"] for ch in word if ch in "aeiou"}
# {'o', 'e'}
```

## collections 모듈로 확장하기

파이썬의 4대 내장 자료구조(리스트·튜플·딕셔너리·세트)만으로는 번거로운 문제들이 있습니다. 표준 라이브러리 `collections` 모듈은 이런 상황을 위해 특화된 자료구조를 제공하며, 비슷한 기능을 직접 구현하기 전에 먼저 이 모듈에 원하는 도구가 있는지 확인하는 것이 좋습니다.

### Counter — 빈도 계산

`Counter`는 딕셔너리의 서브클래스로, 원소의 등장 횟수를 세는 데 특화되어 있습니다. 존재하지 않는 키를 조회해도 `KeyError` 대신 0을 반환하고, `most_common(n)`으로 빈도 상위 n개를 즉시 얻을 수 있으며, 두 `Counter`끼리 `+`나 `-` 연산으로 빈도를 합치거나 뺄 수 있습니다.

```python
from collections import Counter

votes = ["A", "B", "A", "C", "B", "A", "D"]
tally = Counter(votes)
print(tally)                  # Counter({'A': 3, 'B': 2, 'C': 1, 'D': 1})
print(tally["A"])             # 3
print(tally["Z"])             # 0 (KeyError 대신 기본값 반환)
print(tally.most_common(2))   # [('A', 3), ('B', 2)]

# Counter 간 연산
morning = Counter({"coffee": 5, "tea": 2})
afternoon = Counter({"coffee": 3, "tea": 4, "juice": 1})
total = morning + afternoon
# Counter({'coffee': 8, 'tea': 6, 'juice': 1})
diff = afternoon - morning
# Counter({'juice': 1, 'tea': 2})  (0 이하 결과는 자동 제외)
```

### defaultdict — 기본값이 있는 딕셔너리

`defaultdict`는 존재하지 않는 키에 접근할 때 `KeyError`를 던지는 대신, 지정한 팩토리 함수를 호출해 기본값을 만들어 자동으로 채워 넣습니다. `dict.setdefault(key, [])`를 반복 호출하거나 키 존재 여부를 매번 검사하는 분기 없이, 그룹핑 로직을 한 줄로 줄일 수 있습니다.

```python
from collections import defaultdict

# 일반 dict로 그룹핑하면 매번 존재 여부를 검사해야 한다
students_by_grade = {}
for name, grade in [("Alice", "A"), ("Bob", "B"), ("Charlie", "A")]:
    if grade not in students_by_grade:
        students_by_grade[grade] = []
    students_by_grade[grade].append(name)

# defaultdict는 팩토리 함수(list)가 자동으로 기본값을 만든다
grouped = defaultdict(list)
for name, grade in [("Alice", "A"), ("Bob", "B"), ("Charlie", "A")]:
    grouped[grade].append(name)
# defaultdict(<class 'list'>, {'A': ['Alice', 'Charlie'], 'B': ['Bob']})

# 정수 기본값으로 카운팅도 가능하다 (Counter가 더 적합하지만 원리는 동일)
word_length_count = defaultdict(int)
for word in ["cat", "dog", "bird", "ant"]:
    word_length_count[len(word)] += 1
# defaultdict(<class 'int'>, {3: 3, 4: 1})
```

### deque — 양쪽 끝이 빠른 큐

리스트는 끝에서의 `append`/`pop`은 O(1)이지만, 앞쪽에서 `insert(0, x)`나 `pop(0)`을 수행하려면 뒤따르는 모든 요소를 이동해야 해 O(n)이 걸립니다. `deque`(double-ended queue)는 이중 연결 리스트 기반으로 구현되어 양쪽 끝 모두에서 O(1)에 추가·삭제가 가능하므로, 큐(queue)나 슬라이딩 윈도우(sliding window)처럼 양 끝을 자주 다루는 작업에 적합합니다.

```python
from collections import deque

# 큐로 사용: 왼쪽에서 빼고 오른쪽에 추가 (FIFO)
queue = deque(["작업1", "작업2", "작업3"])
queue.append("작업4")       # 오른쪽에 추가: O(1)
first = queue.popleft()     # 왼쪽에서 제거: O(1)
print(first, list(queue))   # 작업1 ['작업2', '작업3', '작업4']

# 최근 N개만 유지하는 슬라이딩 윈도우
recent_logs = deque(maxlen=3)
for log in ["로그1", "로그2", "로그3", "로그4", "로그5"]:
    recent_logs.append(log)
print(list(recent_logs))    # ['로그3', '로그4', '로그5'] (오래된 항목 자동 제거)

# 회전(rotate)
d = deque([1, 2, 3, 4, 5])
d.rotate(2)
print(list(d))              # [4, 5, 1, 2, 3]
```

## 자료구조 성능 비교와 선택 기준

자료구조 선택은 "무엇을 담을 수 있는가"가 아니라 "어떤 연산을 얼마나 자주, 어디에서 수행하는가"로 결정해야 합니다. 같은 데이터를 리스트에 담느냐 세트에 담느냐에 따라 조회 연산의 시간 복잡도가 O(n)에서 O(1)로 바뀔 수 있고, 이 차이는 데이터가 커질수록 체감 가능한 성능 차이로 이어집니다. 아래 표는 각 자료구조의 대표 연산과 평균(amortized) 시간 복잡도를 정리한 것입니다. 딕셔너리와 세트의 O(1)은 해시 충돌이 드물다는 가정의 평균 케이스이며, 최악의 경우(해시 충돌이 몰릴 때)는 O(n)까지 나빠질 수 있습니다.

| 연산 | list | tuple | dict | set | deque |
|------|------|-------|------|-----|-------|
| 인덱스 접근 `a[i]` | O(1) | O(1) | - | - | O(n) |
| 끝에 추가/삭제 | O(1) | 불변 | O(1) | O(1) | O(1) |
| 앞에 추가/삭제 | O(n) | 불변 | - | - | O(1) |
| 특정 값 검색 `in` | O(n) | O(n) | O(1) 평균 | O(1) 평균 | O(n) |
| 키로 조회 `d[k]` | - | - | O(1) 평균 | - | - |
| 중간 삽입/삭제 | O(n) | 불변 | O(1) 평균 | - | O(n) |
| 정렬 | O(n log n) | O(n log n)* | - | - | O(n log n)* |

(* 튜플과 deque 자체를 정렬하는 메서드는 없으며, `sorted()`로 새 리스트를 만듭니다.)

순서가 중요하고 인덱스로 자주 접근한다면 리스트를, 값이 절대 바뀌지 않아야 하고 딕셔너리 키나 세트 원소로 써야 한다면 튜플을 선택합니다. "이 값이 존재하는가"를 자주 묻거나 "이름으로 값을 찾는다"는 요구가 있다면 딕셔너리나 세트가 리스트보다 근본적으로 유리하며, 데이터가 수백 개를 넘어가는 순간 이 차이는 체감할 수준으로 커집니다. 큐처럼 양 끝에서 자주 추가·제거가 일어나는 작업에는 리스트 대신 `deque`를 쓰는 것이 정석입니다 — 리스트의 `pop(0)`을 반복 호출하는 코드는 흔히 발견되는 성능 함정입니다.

## 얕은 복사와 깊은 복사

파이썬에서 변수는 객체를 담는 상자가 아니라 객체를 가리키는 참조(reference)입니다. `b = a`는 객체를 복제하지 않고 같은 객체를 가리키는 이름을 하나 더 만들 뿐이므로, `b`를 통해 내용을 바꾸면 `a`에서도 변경이 보입니다. 이 문제를 피하려면 명시적으로 복사해야 하는데, 복사에는 얕은 복사(shallow copy)와 깊은 복사(deep copy) 두 가지가 있고 둘의 차이는 중첩된 가변 객체를 다룰 때 드러납니다.

얕은 복사(`list(a)`, `a.copy()`, 슬라이싱 `a[:]`, `copy.copy()`)는 바깥쪽 컨테이너만 새로 만들고, 그 안의 요소는 원본과 동일한 객체를 그대로 참조합니다. 요소가 숫자·문자열처럼 불변 객체라면 문제가 없지만, 요소 자체가 리스트나 딕셔너리 같은 가변 객체라면 바깥 컨테이너는 분리되어도 안쪽 객체는 여전히 공유되어 있어 한쪽을 수정하면 다른 쪽도 함께 바뀝니다. 이 공유를 완전히 끊으려면 `copy.deepcopy()`로 중첩된 모든 계층을 재귀적으로 복제해야 합니다.

```python
import copy

original = [[1, 2, 3], [4, 5, 6]]

# 얕은 복사: 바깥 리스트만 새로 생성
shallow = original.copy()
shallow[0].append(999)
print(original)                   # [[1, 2, 3, 999], [4, 5, 6]]  <- 원본도 바뀜!
print(shallow)                    # [[1, 2, 3, 999], [4, 5, 6]]
print(original[0] is shallow[0])  # True: 안쪽 리스트는 같은 객체

# 깊은 복사: 중첩된 모든 계층을 재귀적으로 복제
original2 = [[1, 2, 3], [4, 5, 6]]
deep = copy.deepcopy(original2)
deep[0].append(999)
print(original2)                   # [[1, 2, 3], [4, 5, 6]]  <- 원본은 그대로
print(deep)                        # [[1, 2, 3, 999], [4, 5, 6]]
print(original2[0] is deep[0])     # False: 완전히 분리된 객체
```

얕은 복사는 깊은 복사보다 빠르고 메모리도 적게 쓰므로, 요소가 모두 불변 객체이거나 안쪽 객체 공유가 문제되지 않는 상황에서는 얕은 복사로 충분합니다. 설정 템플릿을 복제해 각기 다르게 수정하는 경우처럼 중첩 구조를 완전히 독립시켜야 할 때만 `deepcopy`의 추가 비용을 감수합니다.

## 실습 프로젝트

아래 두 프로젝트는 지금까지 다룬 컴프리헨션과 `collections` 모듈을 실제 문제에 적용합니다. 첫 번째는 딕셔너리·리스트 컴프리헨션과 `defaultdict`로 통계를 계산하는 성적 관리 시스템이고, 두 번째는 `Counter`와 `defaultdict`로 텍스트를 분석하는 도구입니다.

### 학생 성적 관리 시스템

이 클래스는 학생별 점수를 딕셔너리에 저장하고, 딕셔너리 컴프리헨션으로 전체 평균을 한 번에 계산하며, `defaultdict`로 과목별 점수를 자동으로 그룹핑합니다.

```python
from collections import defaultdict

class StudentManager:
    """딕셔너리와 컴프리헨션을 활용한 성적 관리 클래스"""

    def __init__(self, subjects):
        self.subjects = subjects   # ["국어", "수학", "영어"]
        self.students = {}         # {이름: [점수, 점수, 점수]}

    def add_student(self, name, scores):
        """학생과 과목별 점수 추가"""
        self.students[name] = scores

    def get_average(self, name):
        """학생의 평균 점수"""
        scores = self.students.get(name)
        return sum(scores) / len(scores) if scores else None

    def get_all_averages(self):
        """전체 학생의 평균을 딕셔너리 컴프리헨션으로 계산"""
        return {name: sum(scores) / len(scores) for name, scores in self.students.items()}

    def get_top_students(self, n=3):
        """평균 상위 n명"""
        averages = self.get_all_averages()
        return sorted(averages.items(), key=lambda item: item[1], reverse=True)[:n]

    def get_subject_averages(self):
        """defaultdict로 과목별 점수를 모아 평균을 계산"""
        by_subject = defaultdict(list)
        for scores in self.students.values():
            for subject, score in zip(self.subjects, scores):
                by_subject[subject].append(score)
        return {subject: sum(scores) / len(scores) for subject, scores in by_subject.items()}

    def get_honor_roll(self, threshold=90):
        """평균이 threshold 이상인 학생만 리스트 컴프리헨션으로 추출"""
        return [name for name, avg in self.get_all_averages().items() if avg >= threshold]

# 사용 예제
manager = StudentManager(subjects=["국어", "수학", "영어"])
manager.add_student("Alice", [90, 85, 92])
manager.add_student("Bob", [78, 90, 88])
manager.add_student("Charlie", [95, 89, 94])

print(f"Alice 평균: {manager.get_average('Alice'):.1f}")
print(f"상위 2명: {manager.get_top_students(2)}")
print(f"과목별 평균: {manager.get_subject_averages()}")
print(f"우등생(평균 90 이상): {manager.get_honor_roll()}")
```

### 단어 빈도 분석기

이 함수는 `Counter`로 전체 빈도를 계산하고, `defaultdict`로 첫 글자별 단어 목록을 그룹핑하며, 세트 컴프리헨션으로 고유 단어 집합을 구합니다.

```python
import re
from collections import Counter, defaultdict

def analyze_text(text):
    """텍스트 분석 함수"""
    # 단어 추출 (영문자만), 리스트 컴프리헨션으로 소문자 정규화
    words = [w.lower() for w in re.findall(r"\b[a-zA-Z]+\b", text)]

    # 빈도 계산
    word_count = Counter(words)

    # 고유 단어 집합 (세트 컴프리헨션)
    unique_words = {w for w in words}

    # 첫 글자별로 단어를 그룹핑 (defaultdict)
    by_first_letter = defaultdict(list)
    for word in unique_words:
        by_first_letter[word[0]].append(word)

    return {
        'total_words': len(words),
        'unique_words': len(unique_words),
        'most_common': word_count.most_common(5),
        'by_first_letter': dict(by_first_letter),
    }

# 사용 예제
text = """Python is a great programming language.
Python is easy to learn and Python is powerful."""

result = analyze_text(text)
print(f"총 단어 수: {result['total_words']}")
print(f"고유 단어 수: {result['unique_words']}")
print(f"빈번한 단어: {result['most_common']}")
print(f"첫 글자별 그룹: {result['by_first_letter']}")
```

## 체크리스트

### 기본 자료구조
- [ ] 리스트 생성, 수정, 삭제 가능
- [ ] 튜플의 불변성 이해
- [ ] 딕셔너리 키-값 조작
- [ ] 세트의 중복 제거 특성 활용

### 고급 활용
- [ ] 컴프리헨션 문법 숙달
- [ ] 자료구조 간 변환
- [ ] 중첩 구조 처리
- [ ] 상황별 적절한 자료구조 선택

### 성능 고려
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
