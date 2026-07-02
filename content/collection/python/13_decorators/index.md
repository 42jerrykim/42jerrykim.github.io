---
draft: true
title: "13. 데코레이터"
description: "데코레이터의 동작 원리(클로저, 함수 객체)를 설명하고, 실무에서 로그/캐시/권한 같은 횡단 관심사를 구현하는 패턴을 정리합니다. 과도한 사용의 위험도 함께 다룹니다."
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
lastmod: 2026-07-02
collection_order: 13
---
# 13. 데코레이터

데코레이터(Decorator)는 함수나 클래스의 기능을 수정하거나 확장하는 파이썬의 강력한 기능입니다.

## 학습 목표

이 챕터를 완료하면 다음을 할 수 있습니다:

- **함수 데코레이터** 이해와 구현
- **클래스 데코레이터** 활용
- **매개변수가 있는 데코레이터** 작성
- **내장 데코레이터** 완전 활용
- **실무 패턴**으로 코드 품질 향상

## 핵심 개념(이론)

### 1) `@`는 문법 설탕이다: `f = deco(f)`

데코레이터 문법의 실체는 단순한 재할당입니다. `@my_decorator`를 함수 정의 위에 붙이는 것은, 함수 정의 직후에 `say_goodbye = my_decorator(say_goodbye)`를 실행하는 것과 **완전히 동일**합니다 (도입 배경과 문법 논의는 [PEP 318](https://peps.python.org/pep-0318/) 참조). 즉 데코레이터는 마법이 아니라 "함수를 받아 함수를 돌려주는 일급 함수(higher-order function)"이며, 이 디슈가링(desugaring) 한 줄만 이해하면 아래 모든 변형이 유도됩니다.

```python
@my_decorator
def say_goodbye(): ...

# 위 코드는 정확히 아래와 같다
def say_goodbye(): ...
say_goodbye = my_decorator(say_goodbye)
```

### 2) 상태는 클로저(closure)에 저장된다

`wrapper`가 원본 `func`를 기억하는 이유는 **클로저** 때문입니다. `my_decorator(func)`가 반환하는 `wrapper`는 자신을 둘러싼 스코프의 `func`를 자유 변수(free variable)로 캡처하며, 이는 `wrapper.__closure__`에서 확인할 수 있습니다. 호출 횟수 세기처럼 값을 변경해야 하면 `nonlocal` 선언이 필요합니다 — 이것이 클래스 기반 데코레이터(`self.count`)와의 근본적 차이입니다.

### 3) 매개변수 있는 데코레이터 = 3중 중첩

`@retry(max_attempts=3)`처럼 인자를 받는 데코레이터는 구조가 다릅니다. `retry(max_attempts=3)`가 **먼저 호출되어 데코레이터를 반환**하고, 그 반환값이 함수에 적용됩니다. 즉 `f = retry(max_attempts=3)(f)` — "데코레이터를 만들어 주는 팩토리 → 데코레이터 → wrapper"의 3중 중첩입니다. 아래 실용 예제의 `retry`가 이 구조를 그대로 보여줍니다.

### 4) `functools.wraps`가 없으면 함수의 정체성이 사라진다

`wrapper`로 교체된 함수는 `__name__`이 `"wrapper"`가 되고 `__doc__`·시그니처 정보를 잃습니다. 이는 디버깅·문서 도구·직렬화(pickle)를 조용히 깨뜨립니다. `@functools.wraps(func)`는 원본의 `__name__`, `__doc__`, `__module__` 등을 복사하고 `__wrapped__` 속성으로 원본 접근 경로까지 남깁니다.

```python
import functools

def bad_deco(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def good_deco(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_deco
def area(r):
    """원의 넓이"""
    return 3.14159 * r * r

@good_deco
def perimeter(r):
    """원의 둘레"""
    return 2 * 3.14159 * r

print(area.__name__, area.__doc__)            # wrapper None  ← 정체성 소실!
print(perimeter.__name__, perimeter.__doc__)  # perimeter 원의 둘레
print(perimeter.__wrapped__(1))               # 원본 함수에 직접 접근 가능
```

## 흔한 오해/함정

- **표준 라이브러리를 두고 손수 만들지 말 것**: 캐싱이 필요하면 먼저 `functools.lru_cache`(또는 3.9+의 `functools.cache`)를 씁니다. 직접 구현(아래 프로젝트 2)은 TTL·커스텀 키·분산 캐시처럼 `lru_cache`가 못 하는 요구가 있을 때만 정당화됩니다.

  ```python
  import functools

  @functools.lru_cache(maxsize=128)
  def fib(n):
      return n if n < 2 else fib(n - 1) + fib(n - 2)

  print(fib(100))            # 순식간에 계산
  print(fib.cache_info())    # 히트/미스 통계 내장
  ```

- **클래스 기반 데코레이터를 메서드에 붙이면 `self`가 사라진다**: `CountCalls` 같은 클래스 데코레이터는 함수를 인스턴스로 교체하는데, 일반 클래스 인스턴스는 함수와 달리 디스크립터 프로토콜(`__get__`)을 구현하지 않아 **바운드 메서드가 만들어지지 않습니다**. 인스턴스 메서드에는 클로저 기반 데코레이터를 쓰거나, 클래스 데코레이터에 `__get__`을 구현해야 합니다.

- **스택 순서는 아래에서 위로**: `@a` 위에 `@b`가 있으면 `f = b(a(f))`입니다. 즉 **함수에 가까운 데코레이터가 먼저 적용**되고, 호출 시에는 바깥(위쪽) wrapper부터 실행됩니다. 로깅·트랜잭션·권한처럼 순서가 의미 있는 조합에서 자주 틀리는 지점입니다.

## 요약
- `@deco`는 `f = deco(f)`의 문법 설탕이고, 상태는 클로저가 담는다. 인자 있는 데코레이터는 3중 중첩(`deco(args)(f)`)이다.
- `functools.wraps`는 선택이 아니라 기본값이다. 캐싱은 `lru_cache` 먼저, 직접 구현은 그것이 부족할 때만.

## 핵심 내용

### 데코레이터 기본 개념

**함수를 인수로 받는 함수**

```python
def my_decorator(func):
    def wrapper():
        print("함수 실행 전")
        func()
        print("함수 실행 후")
    return wrapper

def say_hello():
    print("안녕하세요!")

# 데코레이터 수동 적용
decorated_func = my_decorator(say_hello)
decorated_func()

# @ 문법 사용
@my_decorator
def say_goodbye():
    print("안녕히가세요!")

say_goodbye()
```

**인수가 있는 함수 데코레이터**

```python
def timing_decorator(func):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 실행 시간: {end_time - start_time:.4f}초")
        return result
    return wrapper

@timing_decorator
def calculate_sum(n):
    return sum(range(n))

result = calculate_sum(100000)
print(f"결과: {result}")
```

### 실용적인 데코레이터들

**로깅 데코레이터**

```python
import functools
from datetime import datetime

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {func.__name__} 호출됨")
        print(f"  인수: args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            print(f"  결과: {result}")
            return result
        except Exception as e:
            print(f"  에러: {e}")
            raise
    return wrapper

@log_calls
def divide(a, b):
    """두 수를 나누는 함수"""
    return a / b

# 테스트
divide(10, 2)
try:
    divide(10, 0)
except ZeroDivisionError:
    pass
```

**재시도 데코레이터**

```python
import time
import random

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"시도 {attempt + 1} 실패: {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_network_call():
    """가끔 실패하는 네트워크 호출 시뮬레이션"""
    if random.random() < 0.7:  # 70% 확률로 실패
        raise ConnectionError("네트워크 연결 실패")
    return "성공적으로 데이터를 받았습니다!"

# 테스트
try:
    result = unreliable_network_call()
    print(result)
except ConnectionError as e:
    print(f"최종 실패: {e}")
```

### 클래스 데코레이터

**클래스를 데코레이터로 사용**

```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} 호출 횟수: {self.count}")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"안녕하세요, {name}님!"

# 테스트
print(greet("김철수"))
print(greet("이영희"))
print(greet("박민수"))
```

**클래스에 데코레이터 적용**

```python
def add_str_method(cls):
    """클래스에 __str__ 메서드를 자동으로 추가"""
    def __str__(self):
        attrs = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    
    cls.__str__ = __str__
    return cls

@add_str_method
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("김철수", 30)
print(person)  # Person(name=김철수, age=30)
```

### 내장 데코레이터들

**@property**

```python
import math

class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("반지름은 양수여야 합니다")
        self._radius = value
    
    @property
    def area(self):
        return math.pi * self._radius ** 2
    
    @property
    def circumference(self):
        return 2 * math.pi * self._radius

circle = Circle(5)
print(f"반지름: {circle.radius}")
print(f"넓이: {circle.area}")
print(f"둘레: {circle.circumference}")

circle.radius = 10
print(f"새 반지름: {circle.radius}")
```

**@staticmethod와 @classmethod**

```python
class MathUtils:
    pi = 3.14159
    
    @staticmethod
    def add(a, b):
        """정적 메서드 - 클래스나 인스턴스 상태와 무관"""
        return a + b
    
    @classmethod
    def circle_area(cls, radius):
        """클래스 메서드 - 클래스 변수에 접근 가능"""
        return cls.pi * radius ** 2
    
    def instance_method(self):
        """인스턴스 메서드 - 인스턴스 상태에 접근 가능"""
        return "인스턴스 메서드입니다"

# 사용 예제
print(MathUtils.add(5, 3))           # 정적 메서드
print(MathUtils.circle_area(4))      # 클래스 메서드

math = MathUtils()
print(math.instance_method())        # 인스턴스 메서드
```

## 실습 프로젝트

### 프로젝트 1: 성능 모니터링 시스템

```python
import time
import functools
import threading
from collections import defaultdict, deque
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.stats = defaultdict(lambda: {
            'total_calls': 0,
            'total_time': 0,
            'avg_time': 0,
            'min_time': float('inf'),
            'max_time': 0,
            'recent_times': deque(maxlen=10)
        })
        self.lock = threading.Lock()
    
    def monitor(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                
                with self.lock:
                    stats = self.stats[func.__name__]
                    stats['total_calls'] += 1
                    stats['total_time'] += execution_time
                    stats['avg_time'] = stats['total_time'] / stats['total_calls']
                    stats['min_time'] = min(stats['min_time'], execution_time)
                    stats['max_time'] = max(stats['max_time'], execution_time)
                    stats['recent_times'].append(execution_time)
        
        return wrapper
    
    def get_report(self):
        """성능 리포트 생성"""
        report = []
        report.append("📊 Performance Monitor Report")
        report.append("=" * 50)
        
        for func_name, stats in self.stats.items():
            report.append(f"\n🔧 Function: {func_name}")
            report.append(f"  총 호출 수: {stats['total_calls']:,}")
            report.append(f"  총 실행 시간: {stats['total_time']:.4f}초")
            report.append(f"  평균 실행 시간: {stats['avg_time']:.4f}초")
            report.append(f"  최소 실행 시간: {stats['min_time']:.4f}초")
            report.append(f"  최대 실행 시간: {stats['max_time']:.4f}초")
            
            if stats['recent_times']:
                recent_avg = sum(stats['recent_times']) / len(stats['recent_times'])
                report.append(f"  최근 평균 시간: {recent_avg:.4f}초")
        
        return "\n".join(report)
    
    def reset_stats(self):
        """통계 초기화"""
        with self.lock:
            self.stats.clear()

# 전역 모니터 인스턴스
monitor = PerformanceMonitor()

# 사용할 데코레이터
def performance_monitor(func):
    return monitor.monitor(func)

# 테스트 함수들
@performance_monitor
def quick_function():
    time.sleep(0.01)
    return "빠른 작업 완료"

@performance_monitor
def slow_function():
    time.sleep(0.1)
    return "느린 작업 완료"

@performance_monitor
def cpu_intensive_task(n):
    """CPU 집약적인 작업"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# 테스트 실행
if __name__ == "__main__":
    print("성능 테스트 시작...")
    
    # 여러 번 함수 호출
    for i in range(5):
        quick_function()
        slow_function()
        cpu_intensive_task(10000)
    
    # 리포트 출력
    print(monitor.get_report())
```

### 프로젝트 2: 캐시 시스템

```python
import functools
import time
import hashlib
import pickle
from typing import Any, Callable

class CacheSystem:
    def __init__(self, max_size=100, ttl=300):  # TTL: Time To Live (초)
        self.max_size = max_size
        self.ttl = ttl
        self.cache = {}
        self.access_times = {}
    
    def _generate_key(self, func, args, kwargs):
        """함수 호출의 고유 키 생성"""
        key_data = (func.__name__, args, tuple(sorted(kwargs.items())))
        key_string = pickle.dumps(key_data)
        return hashlib.md5(key_string).hexdigest()
    
    def _is_expired(self, timestamp):
        """캐시 항목이 만료되었는지 확인"""
        return time.time() - timestamp > self.ttl
    
    def _cleanup_expired(self):
        """만료된 캐시 항목 정리"""
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp > self.ttl
        ]
        
        for key in expired_keys:
            del self.cache[key]
            del self.access_times[key]
    
    def _evict_lru(self):
        """LRU(Least Recently Used) 방식으로 오래된 항목 제거"""
        if len(self.cache) >= self.max_size:
            lru_key = min(self.access_times, key=self.access_times.get)
            del self.cache[lru_key]
            del self.access_times[lru_key]
    
    def cache_result(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 만료된 캐시 정리
            self._cleanup_expired()
            
            # 캐시 키 생성
            cache_key = self._generate_key(func, args, kwargs)
            current_time = time.time()
            
            # 캐시 히트 확인
            if cache_key in self.cache:
                result, timestamp = self.cache[cache_key]
                if not self._is_expired(timestamp):
                    self.access_times[cache_key] = current_time
                    print(f"🎯 Cache HIT for {func.__name__}")
                    return result
                else:
                    # 만료된 캐시 제거
                    del self.cache[cache_key]
                    del self.access_times[cache_key]
            
            # 캐시 미스 - 함수 실행
            print(f"💨 Cache MISS for {func.__name__}")
            result = func(*args, **kwargs)
            
            # 캐시 크기 확인 및 LRU 정리
            self._evict_lru()
            
            # 결과 캐시에 저장
            self.cache[cache_key] = (result, current_time)
            self.access_times[cache_key] = current_time
            
            return result
        
        return wrapper
    
    def get_stats(self):
        """캐시 통계 반환"""
        total_items = len(self.cache)
        current_time = time.time()
        expired_items = sum(
            1 for _, timestamp in self.cache.values()
            if current_time - timestamp > self.ttl
        )
        
        return {
            'total_items': total_items,
            'expired_items': expired_items,
            'active_items': total_items - expired_items,
            'cache_usage': f"{total_items}/{self.max_size}"
        }
    
    def clear_cache(self):
        """캐시 초기화"""
        self.cache.clear()
        self.access_times.clear()

# 전역 캐시 시스템
cache_system = CacheSystem(max_size=50, ttl=60)  # 최대 50개 항목, 60초 TTL

def cached(func):
    """캐시 데코레이터"""
    return cache_system.cache_result(func)

# 테스트 함수들
@cached
def expensive_calculation(n):
    """시간이 오래 걸리는 계산"""
    print(f"  실제 계산 수행 중... (n={n})")
    time.sleep(1)  # 계산 시간 시뮬레이션
    return sum(i ** 2 for i in range(n))

@cached
def fetch_user_data(user_id):
    """사용자 데이터 가져오기 (DB 조회 시뮬레이션)"""
    print(f"  데이터베이스에서 사용자 {user_id} 조회 중...")
    time.sleep(0.5)  # DB 조회 시간 시뮬레이션
    return {
        'id': user_id,
        'name': f'User_{user_id}',
        'email': f'user{user_id}@example.com'
    }

@cached
def complex_query(category, limit=10):
    """복잡한 쿼리 (키워드 인수 포함)"""
    print(f"  복잡한 쿼리 수행 중... (category={category}, limit={limit})")
    time.sleep(0.8)
    return [f"{category}_item_{i}" for i in range(limit)]

# 테스트 실행
if __name__ == "__main__":
    print("캐시 시스템 테스트 시작...\n")
    
    # 첫 번째 호출 (캐시 미스)
    print("=== 첫 번째 호출 ===")
    result1 = expensive_calculation(100)
    print(f"결과: {result1}\n")
    
    # 두 번째 호출 (캐시 히트)
    print("=== 두 번째 호출 (같은 인수) ===")
    result2 = expensive_calculation(100)
    print(f"결과: {result2}\n")
    
    # 다른 인수로 호출
    print("=== 다른 인수로 호출 ===")
    result3 = expensive_calculation(200)
    print(f"결과: {result3}\n")
    
    # 사용자 데이터 테스트
    print("=== 사용자 데이터 테스트 ===")
    user1 = fetch_user_data(1)
    print(f"사용자 1: {user1}")
    
    user1_cached = fetch_user_data(1)  # 캐시 히트
    print(f"사용자 1 (캐시): {user1_cached}\n")
    
    # 복잡한 쿼리 테스트
    print("=== 복잡한 쿼리 테스트 ===")
    query1 = complex_query("books", limit=5)
    print(f"쿼리 결과: {query1}")
    
    query1_cached = complex_query("books", limit=5)  # 캐시 히트
    print(f"쿼리 결과 (캐시): {query1_cached}\n")
    
    # 캐시 통계
    print("=== 캐시 통계 ===")
    stats = cache_system.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
```

## 체크리스트

### 기본 데코레이터
- [ ] 함수 데코레이터 이해와 구현
- [ ] @functools.wraps 사용법
- [ ] *args, **kwargs 활용
- [ ] 반환값과 예외 처리

### 고급 데코레이터
- [ ] 매개변수가 있는 데코레이터
- [ ] 클래스 기반 데코레이터
- [ ] 클래스에 적용하는 데코레이터
- [ ] 데코레이터 체이닝

### 내장 데코레이터
- [ ] @property와 getter/setter
- [ ] @staticmethod, @classmethod
- [ ] @functools.lru_cache
- [ ] 기타 유용한 내장 데코레이터

### 실무 패턴
- [ ] 로깅과 모니터링
- [ ] 캐싱과 메모이제이션
- [ ] 재시도와 에러 처리
- [ ] 권한 검사와 검증

## 다음 단계

🎉 **축하합니다!** 파이썬 데코레이터를 마스터했습니다.

이제 [14. 제너레이터와 이터레이터](../14_generators_iterators/)로 넘어가서 메모리 효율적인 데이터 처리 방법을 학습해봅시다.

---

💡 **팁:**
- 데코레이터는 함수의 시그니처를 보존하기 위해 @functools.wraps를 사용하세요
- 복잡한 로직은 클래스 기반 데코레이터로 구현하는 것이 좋습니다
- 성능이 중요한 경우 데코레이터의 오버헤드를 고려하세요
- 데코레이터 체이닝 시 실행 순서를 명확히 이해하세요 
