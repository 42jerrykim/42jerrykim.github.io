---

image: "wordcloud.png"
title: "[Python Cheatsheet] 48. random - 난수 생성과 무작위 선택"
slug: "random-module-guide-efficient-random-number-generation-examples"
description: "파이썬 random 모듈을 빠르게 사용하기 위한 치트시트입니다. 난수 생성, 무작위 선택, 셔플, 가중치 선택, 시드 설정 등 핵심 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 48
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - random
  - 난수
  - 랜덤
  - randint
  - choice
  - choices
  - sample
  - shuffle
  - uniform
  - gauss
  - seed
  - 시드
  - 무작위
  - sampling
  - 샘플링
  - weighted
  - 가중치
  - probability
  - 확률
  - simulation
  - 시뮬레이션
  - game
  - 게임
  - lottery
  - 복권
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - cryptography
  - 암호화
  - secrets
---
`random` 모듈은 **의사 난수 생성**을 위한 도구입니다. 시뮬레이션, 게임, 테스트 데이터 생성 등에 사용합니다. 보안용으로는 `secrets` 모듈을 사용하세요.

## 언제 이 치트시트를 보나?

- **무작위 숫자**를 생성해야 할 때
- 리스트에서 **랜덤 선택**이 필요할 때
- **셔플, 샘플링**이 필요할 때

## 핵심 함수

```python
import random

# 정수
random.randint(a, b)     # a~b 포함 정수
random.randrange(a, b)   # a~b-1 정수

# 실수
random.random()          # 0.0~1.0 미만
random.uniform(a, b)     # a~b 실수

# 선택
random.choice(seq)       # 하나 선택
random.choices(seq, k=n) # n개 복원 선택
random.sample(seq, k=n)  # n개 비복원 선택
random.shuffle(seq)      # 제자리 셔플
```

## 최소 예제

### 1. 정수 난수

```python
import random

# a 이상 b 이하 정수 (양끝 포함)
random.randint(1, 10)    # 1~10 중 하나

# a 이상 b 미만 정수 (range처럼)
random.randrange(1, 10)  # 1~9 중 하나

# step 지정
random.randrange(0, 100, 5)  # 0, 5, 10, ..., 95 중 하나
```

### 2. 실수 난수

```python
import random

# 0.0 <= x < 1.0
random.random()           # 0.7234...

# a <= x <= b
random.uniform(1.5, 5.5)  # 1.5~5.5 실수
```

### 3. 리스트에서 선택

```python
import random

items = ['apple', 'banana', 'cherry', 'date']

# 하나 선택
random.choice(items)      # 'banana'

# 여러 개 선택 (복원 - 중복 가능)
random.choices(items, k=3)  # ['apple', 'cherry', 'apple']

# 여러 개 선택 (비복원 - 중복 없음)
random.sample(items, k=3)   # ['date', 'apple', 'cherry']
```

### 4. 가중치 선택

```python
import random

items = ['common', 'rare', 'legendary']
weights = [70, 25, 5]  # 확률 비율

# 가중치 적용 선택
random.choices(items, weights=weights, k=10)
# ['common', 'common', 'rare', 'common', 'common', ...]

# 누적 가중치
cum_weights = [70, 95, 100]  # 누적합
random.choices(items, cum_weights=cum_weights, k=5)
```

### 5. 셔플

```python
import random

deck = list(range(1, 53))  # 카드 덱

# 제자리 셔플 (원본 변경)
random.shuffle(deck)
print(deck[:5])  # [23, 7, 42, 15, 38]

# 원본 유지 셔플
original = [1, 2, 3, 4, 5]
shuffled = random.sample(original, len(original))
print(original)   # [1, 2, 3, 4, 5]
print(shuffled)   # [3, 1, 5, 2, 4]
```

### 6. 시드 설정 (재현 가능)

```python
import random

random.seed(42)
print(random.random())  # 0.6394267984578837
print(random.randint(1, 100))  # 14

# 같은 시드 = 같은 결과
random.seed(42)
print(random.random())  # 0.6394267984578837
print(random.randint(1, 100))  # 14
```

### 7. 분포 함수

```python
import random

# 정규분포 (가우스)
random.gauss(mu=0, sigma=1)     # 평균 0, 표준편차 1

# 삼각분포
random.triangular(low=0, high=10, mode=3)

# 지수분포
random.expovariate(lambd=1.5)

# 베타분포
random.betavariate(alpha=2, beta=5)
```

### 8. 실용 예제

```python
import random

# 주사위 굴리기
def roll_dice(n=1):
    return [random.randint(1, 6) for _ in range(n)]

print(roll_dice(3))  # [4, 2, 6]

# 로또 번호 생성 (1~45 중 6개)
def lotto():
    return sorted(random.sample(range(1, 46), 6))

print(lotto())  # [3, 12, 25, 33, 38, 42]

# 비밀번호 생성 (비보안용)
import string
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + '!@#$%'
    return ''.join(random.choices(chars, k=length))

print(generate_password())  # 'kX7#mP2nQ$aB'
```

### 9. 가중치 로또/가챠 시스템

```python
import random

def gacha():
    """가챠 시스템 시뮬레이션"""
    grades = ['SSR', 'SR', 'R', 'N']
    weights = [1, 9, 30, 60]  # 1%, 9%, 30%, 60%
    return random.choices(grades, weights=weights)[0]

# 100번 뽑기
results = [gacha() for _ in range(100)]
for grade in ['SSR', 'SR', 'R', 'N']:
    print(f"{grade}: {results.count(grade)}회")
```

### 10. Random 인스턴스 (독립적 생성기)

```python
import random

# 독립적인 난수 생성기
rng1 = random.Random(42)
rng2 = random.Random(42)

# 각각 독립적으로 시드 관리
print(rng1.random())  # 0.6394267984578837
print(rng2.random())  # 0.6394267984578837

# 전역 random과 독립
random.seed(0)
print(rng1.random())  # 0.02501... (rng1은 자체 시드 유지)
```

## random vs secrets

```python
import random
import secrets

# random: 시뮬레이션, 게임, 테스트용 (예측 가능)
random.randint(1, 100)

# secrets: 보안용 (암호학적 안전)
secrets.randbelow(100)      # 0~99
secrets.choice(['a', 'b'])  # 보안 선택
secrets.token_hex(16)       # 보안 토큰
```

## 자주 하는 실수

### 1. sample에서 k가 너무 클 때

```python
import random

items = [1, 2, 3]
# random.sample(items, 5)  # ValueError: Sample larger than population

# choices는 k가 커도 됨 (복원 추출)
random.choices(items, k=5)  # [2, 1, 3, 1, 2]
```

### 2. 빈 시퀀스에서 choice

```python
import random

# random.choice([])  # IndexError: Cannot choose from an empty sequence

items = []
if items:
    random.choice(items)
```

### 3. shuffle 반환값

```python
import random

items = [1, 2, 3]
# 잘못: shuffle은 None 반환
result = random.shuffle(items)
print(result)  # None

# 올바름: 원본이 변경됨
random.shuffle(items)
print(items)  # [3, 1, 2]
```

## 한눈에 정리

| 함수 | 용도 | 예시 |
|------|------|------|
| `randint(a, b)` | 정수 (a~b 포함) | `randint(1, 6)` |
| `random()` | 0~1 미만 실수 | `random()` |
| `choice(seq)` | 하나 선택 | `choice(['a', 'b'])` |
| `choices(seq, k=n)` | n개 복원 선택 | `choices([1,2,3], k=5)` |
| `sample(seq, k=n)` | n개 비복원 선택 | `sample([1,2,3], k=2)` |
| `shuffle(seq)` | 제자리 섞기 | `shuffle(list)` |
| `seed(n)` | 시드 설정 | `seed(42)` |

## 참고

- [random - Python Docs](https://docs.python.org/3/library/random.html)
- [secrets - Python Docs](https://docs.python.org/3/library/secrets.html)
