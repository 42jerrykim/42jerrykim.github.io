---
draft: true
title: "[Python Cheatsheet] 60. unittest.mock - 모킹과 패칭"
slug: "unittest-mock-magicmock-patch-testing-mocking-stub-fake-side-effect"
description: "파이썬 unittest.mock 모듈을 빠르게 사용하기 위한 치트시트입니다. Mock, MagicMock, patch, side_effect, return_value 등 테스트 모킹 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 60
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - mock
  - Mock
  - MagicMock
  - patch
  - 패치
  - unittest
  - testing
  - 테스트
  - mocking
  - 모킹
  - stub
  - 스텁
  - fake
  - 페이크
  - side_effect
  - return_value
  - assert_called
  - call_count
  - spec
  - autospec
  - dependency
  - 의존성
  - isolation
  - 격리
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`unittest.mock`은 테스트에서 **객체를 가짜로 대체**하는 기능을 제공합니다. 외부 의존성 격리, API 호출 모킹 등 단위 테스트에 필수적입니다.

## 언제 이 치트시트를 보나?

- **외부 API 호출**을 테스트에서 격리하고 싶을 때
- **데이터베이스나 파일** 접근 없이 테스트하고 싶을 때
- **특정 함수의 반환값**을 제어하고 싶을 때

## 핵심 클래스

```python
from unittest.mock import Mock, MagicMock, patch

# Mock: 기본 모의 객체
mock = Mock()

# MagicMock: 매직 메서드 지원
magic = MagicMock()

# patch: 모듈의 객체 대체
with patch('module.function') as mock_func:
    pass
```

## 최소 예제

### 1. Mock 기본

```python
from unittest.mock import Mock

# 모의 객체 생성
mock = Mock()

# 아무 속성이나 메서드 접근 가능
mock.some_method()
mock.some_attribute
mock.nested.deep.call()

# 반환값 설정
mock.get_value.return_value = 42
print(mock.get_value())  # 42

# 호출 확인
mock.get_value()
mock.get_value.assert_called()
mock.get_value.assert_called_once()
```

### 2. return_value vs side_effect

```python
from unittest.mock import Mock

mock = Mock()

# return_value: 항상 같은 값 반환
mock.method.return_value = "always this"
print(mock.method())  # "always this"
print(mock.method())  # "always this"

# side_effect: 호출마다 다른 동작
mock.method.side_effect = [1, 2, 3]
print(mock.method())  # 1
print(mock.method())  # 2
print(mock.method())  # 3

# side_effect로 예외 발생
mock.method.side_effect = ValueError("error!")
# mock.method()  # ValueError: error!

# side_effect로 함수 실행
mock.method.side_effect = lambda x: x * 2
print(mock.method(5))  # 10
```

### 3. 호출 확인 (assert)

```python
from unittest.mock import Mock, call

mock = Mock()

mock.method(1, 2, key='value')

# 호출 여부
mock.method.assert_called()
mock.method.assert_called_once()

# 특정 인자로 호출되었는지
mock.method.assert_called_with(1, 2, key='value')
mock.method.assert_called_once_with(1, 2, key='value')

# 호출 횟수
print(mock.method.call_count)  # 1

# 호출 기록
print(mock.method.call_args)  # call(1, 2, key='value')
print(mock.method.call_args_list)  # [call(1, 2, key='value')]

# 여러 호출 확인
mock.method(1)
mock.method(2)
mock.method.assert_has_calls([call(1), call(2)])
```

### 4. patch 데코레이터

```python
from unittest.mock import patch
import requests

def get_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# patch로 requests.get 대체
@patch('requests.get')
def test_get_user(mock_get):
    # 모의 응답 설정
    mock_get.return_value.json.return_value = {'name': 'Alice'}
    
    result = get_user(123)
    
    assert result == {'name': 'Alice'}
    mock_get.assert_called_once_with("https://api.example.com/users/123")
```

### 5. patch 컨텍스트 매니저

```python
from unittest.mock import patch

def test_something():
    with patch('module.function') as mock_func:
        mock_func.return_value = 'mocked'
        
        # 테스트 코드
        result = module.function()
        assert result == 'mocked'
    
    # with 블록 밖에서는 원래 함수 복원
```

### 6. patch.object - 객체의 메서드 패치

```python
from unittest.mock import patch

class Calculator:
    def add(self, a, b):
        return a + b

calc = Calculator()

with patch.object(calc, 'add', return_value=100):
    print(calc.add(1, 2))  # 100

print(calc.add(1, 2))  # 3 (복원됨)
```

### 7. MagicMock - 매직 메서드 지원

```python
from unittest.mock import Mock, MagicMock

# Mock은 매직 메서드 자동 지원 안 함
mock = Mock()
# len(mock)  # TypeError

# MagicMock은 지원
magic = MagicMock()
magic.__len__.return_value = 5
print(len(magic))  # 5

# 컨텍스트 매니저로 사용
magic.__enter__.return_value = 'entered'
with magic as m:
    print(m)  # 'entered'
```

### 8. spec - 인터페이스 제한

```python
from unittest.mock import Mock

class Database:
    def connect(self):
        pass
    
    def query(self, sql):
        pass

# spec 없이: 아무 메서드나 호출 가능 (오타 감지 불가)
mock = Mock()
mock.conect()  # 오타지만 에러 없음

# spec 있으면: 실제 클래스 인터페이스만 허용
mock = Mock(spec=Database)
# mock.conect()  # AttributeError: Mock has no attribute 'conect'
mock.connect()  # OK
```

### 9. autospec - 시그니처 검증

```python
from unittest.mock import create_autospec

def add(a, b):
    return a + b

# autospec: 시그니처도 검증
mock_add = create_autospec(add)
mock_add(1, 2)  # OK
# mock_add(1)  # TypeError: missing argument 'b'
# mock_add(1, 2, 3)  # TypeError: too many arguments
```

### 10. 실전 예제 - 서비스 테스트

```python
from unittest.mock import Mock, patch

# 테스트 대상 코드
class UserService:
    def __init__(self, db, email_client):
        self.db = db
        self.email_client = email_client
    
    def create_user(self, name, email):
        user_id = self.db.insert('users', {'name': name, 'email': email})
        self.email_client.send_welcome(email)
        return user_id

# 테스트
def test_create_user():
    # 의존성 모킹
    mock_db = Mock()
    mock_db.insert.return_value = 123
    
    mock_email = Mock()
    
    # 테스트
    service = UserService(mock_db, mock_email)
    result = service.create_user('Alice', 'alice@example.com')
    
    # 검증
    assert result == 123
    mock_db.insert.assert_called_once_with(
        'users', 
        {'name': 'Alice', 'email': 'alice@example.com'}
    )
    mock_email.send_welcome.assert_called_once_with('alice@example.com')
```

### 11. patch.dict - 딕셔너리 패치

```python
from unittest.mock import patch
import os

# 환경 변수 패치
with patch.dict(os.environ, {'API_KEY': 'test_key'}):
    print(os.environ['API_KEY'])  # 'test_key'

# 블록 밖에서는 원래 값
```

## 자주 하는 실수

### 1. 잘못된 경로로 patch

```python
# mymodule.py
from requests import get

def fetch():
    return get('http://example.com')

# 잘못: requests.get을 패치
@patch('requests.get')
def test_fetch(mock_get):
    fetch()  # 패치 안 됨!

# 올바름: mymodule.get을 패치 (import된 위치)
@patch('mymodule.get')
def test_fetch(mock_get):
    fetch()  # 패치됨
```

### 2. assert_called vs assert_called_with

```python
from unittest.mock import Mock

mock = Mock()
mock.method('wrong', 'args')

# 호출 여부만 확인 (인자 무시)
mock.method.assert_called()  # OK

# 특정 인자로 호출되었는지
# mock.method.assert_called_with('right', 'args')  # AssertionError
```

## 한눈에 정리

| 기능 | 사용법 |
|------|--------|
| 반환값 설정 | `mock.return_value = 값` |
| 예외 발생 | `mock.side_effect = Exception()` |
| 순차 반환 | `mock.side_effect = [1, 2, 3]` |
| 호출 확인 | `mock.assert_called_once_with(args)` |
| 모듈 패치 | `@patch('module.obj')` |
| 객체 패치 | `patch.object(obj, 'method')` |

## 참고

- [unittest.mock - Python Docs](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-mock](https://pypi.org/project/pytest-mock/)
