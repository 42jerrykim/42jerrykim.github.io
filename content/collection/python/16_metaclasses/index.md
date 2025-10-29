---
draft: true
title: "16. 메타클래스"
description: "클래스 생성을 제어하는 고급 파이썬 기능인 메타클래스"
collection_order: 16
---

# 챕터 16: 메타클래스

> "클래스도 객체다" - 파이썬에서 클래스 자체를 제어하는 메타프로그래밍의 세계에 오신 것을 환영합니다.

## 학습 목표
- 메타클래스의 개념과 동작 방식을 이해할 수 있다
- type() 함수를 활용한 동적 클래스 생성을 구현할 수 있다
- 커스텀 메타클래스를 만들고 활용할 수 있다
- 메타클래스의 실용적 사용 사례를 파악할 수 있다

## 메타클래스 기초 이해

### 클래스도 객체다

```python
# 클래스도 객체라는 것을 증명해보자
class MyClass:
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

# 클래스 자체도 객체임을 확인
print(type(MyClass))  # <class 'type'>
print(isinstance(MyClass, type))  # True

# 클래스의 속성을 동적으로 추가
MyClass.class_variable = "I'm a class variable"
print(MyClass.class_variable)  # I'm a class variable

# 클래스에 메서드도 동적으로 추가 가능
def new_method(self):
    return f"New method called with value: {self.value}"

MyClass.new_method = new_method

# 인스턴스에서 새 메서드 사용
obj = MyClass(42)
print(obj.new_method())  # New method called with value: 42
```

### type의 두 가지 역할

```python
# 역할 1: 객체의 타입 확인
print(type(5))          # <class 'int'>
print(type("hello"))    # <class 'str'>
print(type([1, 2, 3]))  # <class 'list'>

# 역할 2: 동적 클래스 생성
# type(name, bases, dict) 형식

# 빈 클래스 생성
EmptyClass = type('EmptyClass', (), {})
print(EmptyClass)  # <class '__main__.EmptyClass'>

# 속성이 있는 클래스 생성
attrs = {
    'class_var': 'Hello',
    'instance_method': lambda self: f"Instance method called"
}
MyDynamicClass = type('MyDynamicClass', (), attrs)

obj = MyDynamicClass()
print(obj.class_var)        # Hello
print(obj.instance_method()) # Instance method called
```

### 메타클래스 계층 구조

```python
# 계층 구조 이해
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

# 인스턴스 → 클래스 → 메타클래스
dog = Dog()

print("=== 메타클래스 계층 구조 ===")
print(f"dog의 타입: {type(dog)}")           # <class '__main__.Dog'>
print(f"Dog의 타입: {type(Dog)}")           # <class 'type'>
print(f"type의 타입: {type(type)}")         # <class 'type'>

print(f"dog은 Dog의 인스턴스: {isinstance(dog, Dog)}")      # True
print(f"Dog은 type의 인스턴스: {isinstance(Dog, type)}")    # True
print(f"type은 type의 인스턴스: {isinstance(type, type)}")  # True
```

## 동적 클래스 생성

### type()을 활용한 클래스 생성

```python
# 함수들을 미리 정의
def init_method(self, name, age):
    self.name = name
    self.age = age

def str_method(self):
    return f"Person(name='{self.name}', age={self.age})"

def get_info(self):
    return f"{self.name} is {self.age} years old"

# 동적으로 Person 클래스 생성
Person = type(
    'Person',  # 클래스 이름
    (),        # 상속받을 클래스들 (빈 튜플 = object만 상속)
    {          # 클래스 속성과 메서드들
        '__init__': init_method,
        '__str__': str_method,
        'get_info': get_info,
        'species': 'Homo sapiens'  # 클래스 변수
    }
)

# 동적으로 생성된 클래스 사용
person = Person("Alice", 30)
print(person)           # Person(name='Alice', age=30)
print(person.get_info()) # Alice is 30 years old
print(Person.species)   # Homo sapiens
```

### 상속 관계를 가진 동적 클래스

```python
# 기본 클래스
class Vehicle:
    def __init__(self, brand):
        self.brand = brand
    
    def start(self):
        return f"{self.brand} vehicle started"

# Car 클래스를 동적으로 생성 (Vehicle 상속)
def car_init(self, brand, model):
    super(Car, self).__init__(brand)  # 부모 클래스 초기화
    self.model = model

def honk(self):
    return f"{self.brand} {self.model} goes beep beep!"

Car = type(
    'Car',
    (Vehicle,),  # Vehicle을 상속
    {
        '__init__': car_init,
        'honk': honk,
        'wheels': 4  # 클래스 변수
    }
)

# 사용 예제
car = Car("Toyota", "Camry")
print(car.start())  # Toyota vehicle started
print(car.honk())   # Toyota Camry goes beep beep!
print(f"This car has {car.wheels} wheels")  # This car has 4 wheels
```

## 커스텀 메타클래스 만들기

### 기본 메타클래스 구현

```python
class MyMetaClass(type):
    """커스텀 메타클래스"""
    
    def __new__(cls, name, bases, attrs):
        print(f"Creating class '{name}' with MyMetaClass")
        print(f"Bases: {bases}")
        print(f"Attributes: {list(attrs.keys())}")
        
        # 모든 메서드에 로깅 기능 추가
        for key, value in attrs.items():
            if callable(value) and not key.startswith('__'):
                attrs[key] = cls.add_logging(value, key)
        
        # 클래스 생성
        return super().__new__(cls, name, bases, attrs)
    
    def __init__(cls, name, bases, attrs):
        print(f"Initializing class '{name}'")
        super().__init__(name, bases, attrs)
    
    @staticmethod
    def add_logging(func, func_name):
        """메서드에 로깅 기능 추가"""
        def wrapper(self, *args, **kwargs):
            print(f"[LOG] Calling {func_name} with args: {args}, kwargs: {kwargs}")
            result = func(self, *args, **kwargs)
            print(f"[LOG] {func_name} returned: {result}")
            return result
        return wrapper

# 메타클래스를 사용하는 클래스
class Calculator(metaclass=MyMetaClass):
    def __init__(self, name):
        self.name = name
    
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

# 사용해보기
print("=== Calculator 인스턴스 생성 ===")
calc = Calculator("My Calculator")

print("\n=== 메서드 호출 ===")
result1 = calc.add(5, 3)
result2 = calc.multiply(4, 6)
```

### 싱글톤 메타클래스

```python
class SingletonMeta(type):
    """싱글톤 패턴을 구현하는 메타클래스"""
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print(f"Creating new instance of {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            print(f"Returning existing instance of {cls.__name__}")
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, host="localhost", port=5432):
        self.host = host
        self.port = port
        self.connected = False
    
    def connect(self):
        if not self.connected:
            print(f"Connecting to {self.host}:{self.port}")
            self.connected = True
        return self.connected
    
    def get_connection_info(self):
        return f"Connected to {self.host}:{self.port}" if self.connected else "Not connected"

# 싱글톤 테스트
print("=== 싱글톤 테스트 ===")
db1 = DatabaseConnection()
db2 = DatabaseConnection("remote-host", 3306)

print(f"db1 is db2: {db1 is db2}")  # True
print(f"db1 host: {db1.host}")      # localhost (첫 번째 인스턴스 값 유지)
```

### 속성 검증 메타클래스

```python
class ValidatedMeta(type):
    """속성 검증을 수행하는 메타클래스"""
    
    def __new__(cls, name, bases, attrs):
        # 필수 속성 체크
        required_attrs = attrs.get('_required_attrs', [])
        for attr in required_attrs:
            if attr not in attrs:
                raise AttributeError(f"Class {name} must define {attr}")
        
        # 타입 힌트 검증
        annotations = attrs.get('__annotations__', {})
        for attr_name, attr_type in annotations.items():
            if attr_name in attrs:
                value = attrs[attr_name]
                if not isinstance(value, attr_type):
                    raise TypeError(f"{attr_name} must be of type {attr_type.__name__}")
        
        return super().__new__(cls, name, bases, attrs)

class Person(metaclass=ValidatedMeta):
    _required_attrs = ['name', 'age']
    
    name: str = "Unknown"
    age: int = 0
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old"

# 올바른 사용
person = Person("Alice", 25)
print(person.introduce())

# 잘못된 클래스 정의 시도 (에러 발생)
try:
    class InvalidPerson(metaclass=ValidatedMeta):
        _required_attrs = ['name', 'age']
        name: str = "Test"
        # age가 없어서 에러 발생
except AttributeError as e:
    print(f"Error: {e}")

## 고급 메타클래스 기능

### __prepare__ 메서드 활용

```python
class OrderedMeta(type):
    """클래스 정의 순서를 보존하는 메타클래스"""
    
    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        print(f"Preparing namespace for {name}")
        # OrderedDict를 반환하여 정의 순서 보존
        from collections import OrderedDict
        return OrderedDict()
    
    def __new__(cls, name, bases, namespace, **kwargs):
        print(f"Creating {name} with ordered attributes: {list(namespace.keys())}")
        return super().__new__(cls, name, bases, namespace)

class OrderedClass(metaclass=OrderedMeta):
    third_attr = 3
    first_attr = 1
    second_attr = 2
    
    def method_c(self):
        pass
    
    def method_a(self):
        pass
    
    def method_b(self):
        pass
```

### 자동 등록 시스템

```python
class RegistryMeta(type):
    """클래스를 자동으로 레지스트리에 등록하는 메타클래스"""
    
    registry = {}
    
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        
        # 기본 클래스가 아닌 경우에만 등록
        if bases:
            cls.registry[name] = new_class
            print(f"Registered {name} in registry")
        
        return new_class
    
    @classmethod
    def get_registered_classes(cls):
        return cls.registry.copy()

class Plugin(metaclass=RegistryMeta):
    """플러그인 베이스 클래스"""
    
    def execute(self):
        raise NotImplementedError

class EmailPlugin(Plugin):
    def execute(self):
        return "Sending email..."

class SMSPlugin(Plugin):
    def execute(self):
        return "Sending SMS..."

class PushNotificationPlugin(Plugin):
    def execute(self):
        return "Sending push notification..."

# 등록된 플러그인들 확인
print("Registered plugins:", list(RegistryMeta.get_registered_classes().keys()))

# 모든 플러그인 실행
for name, plugin_class in RegistryMeta.get_registered_classes().items():
    plugin = plugin_class()
    print(f"{name}: {plugin.execute()}")
```

### ORM 스타일 메타클래스

```python
class Field:
    """데이터베이스 필드를 나타내는 클래스"""
    
    def __init__(self, field_type, primary_key=False, nullable=True):
        self.field_type = field_type
        self.primary_key = primary_key
        self.nullable = nullable
    
    def __repr__(self):
        return f"Field({self.field_type.__name__}, pk={self.primary_key}, null={self.nullable})"

class ModelMeta(type):
    """ORM 모델을 위한 메타클래스"""
    
    def __new__(cls, name, bases, attrs):
        # Field 인스턴스들을 찾아서 메타데이터 생성
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
                # Field를 실제 속성으로 변환하기 위해 제거
                attrs.pop(key)
        
        # 메타데이터 저장
        attrs['_fields'] = fields
        attrs['_table_name'] = name.lower()
        
        new_class = super().__new__(cls, name, bases, attrs)
        
        # 각 필드에 대한 프로퍼티 동적 생성
        for field_name, field in fields.items():
            cls._create_property(new_class, field_name, field)
        
        return new_class
    
    @staticmethod
    def _create_property(cls, field_name, field):
        """필드에 대한 프로퍼티를 동적으로 생성"""
        private_name = f'_{field_name}'
        
        def getter(self):
            return getattr(self, private_name, None)
        
        def setter(self, value):
            if not field.nullable and value is None:
                raise ValueError(f"{field_name} cannot be None")
            if value is not None and not isinstance(value, field.field_type):
                raise TypeError(f"{field_name} must be of type {field.field_type.__name__}")
            setattr(self, private_name, value)
        
        setattr(cls, field_name, property(getter, setter))

class Model(metaclass=ModelMeta):
    """ORM 모델 베이스 클래스"""
    
    def __init__(self, **kwargs):
        for field_name in self._fields:
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name])
    
    def to_dict(self):
        return {field_name: getattr(self, field_name) 
                for field_name in self._fields}
    
    def __repr__(self):
        field_values = ', '.join(f"{k}={v}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({field_values})"

# 모델 정의
class User(Model):
    id = Field(int, primary_key=True, nullable=False)
    name = Field(str, nullable=False)
    email = Field(str, nullable=False)
    age = Field(int, nullable=True)

# 사용 예제
user = User(id=1, name="Alice", email="alice@example.com", age=25)
print(user)  # User(id=1, name=Alice, email=alice@example.com, age=25)
print(f"Table name: {User._table_name}")
print(f"Fields: {User._fields}")

# 타입 검증 테스트
try:
    user.age = "invalid"  # 에러 발생
except TypeError as e:
    print(f"Type error: {e}")

## 메타클래스 대안

### 클래스 데코레이터

```python
def add_logging(cls):
    """클래스의 모든 메서드에 로깅 추가하는 데코레이터"""
    for name, method in cls.__dict__.items():
        if callable(method) and not name.startswith('__'):
            def make_logged_method(original_method, method_name):
                def logged_method(self, *args, **kwargs):
                    print(f"[DECORATOR] Calling {method_name}")
                    result = original_method(self, *args, **kwargs)
                    print(f"[DECORATOR] {method_name} finished")
                    return result
                return logged_method
            
            setattr(cls, name, make_logged_method(method, name))
    return cls

@add_logging
class SimpleCalculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b

calc = SimpleCalculator()
calc.add(5, 3)
calc.subtract(10, 4)
```

### __init_subclass__ 활용

```python
class ValidatedBase:
    """서브클래스 초기화를 제어하는 기본 클래스"""
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # 필수 메서드 체크
        required_methods = getattr(cls, '_required_methods', [])
        for method_name in required_methods:
            if not hasattr(cls, method_name):
                raise NotImplementedError(
                    f"Class {cls.__name__} must implement {method_name}"
                )
        
        print(f"Validated class: {cls.__name__}")

class APIHandler(ValidatedBase):
    _required_methods = ['handle_get', 'handle_post']
    
    def handle_get(self):
        return "GET request handled"
    
    def handle_post(self):
        return "POST request handled"

# 올바른 구현
handler = APIHandler()
print(handler.handle_get())

# 잘못된 구현 시도
try:
    class IncompleteHandler(ValidatedBase):
        _required_methods = ['handle_get', 'handle_post']
        
        def handle_get(self):
            return "GET only"
        # handle_post 누락
except NotImplementedError as e:
    print(f"Error: {e}")
```

## 실습 프로젝트

###️ 프로젝트 1: 자동 속성 검증 시스템

```python
class ValidationError(Exception):
    """검증 오류를 위한 커스텀 예외"""
    pass

class Validator:
    """기본 검증기 클래스"""
    
    def validate(self, value):
        raise NotImplementedError

class IntegerValidator(Validator):
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value):
        if not isinstance(value, int):
            raise ValidationError(f"Expected int, got {type(value).__name__}")
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Value {value} is less than minimum {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Value {value} is greater than maximum {self.max_value}")

class StringValidator(Validator):
    def __init__(self, min_length=None, max_length=None, pattern=None):
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
    
    def validate(self, value):
        if not isinstance(value, str):
            raise ValidationError(f"Expected str, got {type(value).__name__}")
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f"String too short (min: {self.min_length})")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f"String too long (max: {self.max_length})")
        if self.pattern is not None:
            import re
            if not re.match(self.pattern, value):
                raise ValidationError(f"String doesn't match pattern {self.pattern}")

class ValidatedAttribute:
    """검증 가능한 속성 디스크립터"""
    
    def __init__(self, validator, default=None):
        self.validator = validator
        self.default = default
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, self.default)
    
    def __set__(self, obj, value):
        self.validator.validate(value)
        setattr(obj, self.private_name, value)

class ValidatedMeta(type):
    """검증이 포함된 메타클래스"""
    
    def __new__(cls, name, bases, attrs):
        # ValidatedAttribute 인스턴스들을 찾아서 처리
        for key, value in attrs.items():
            if isinstance(value, ValidatedAttribute):
                value.__set_name__(None, key)  # 이름 설정
        
        return super().__new__(cls, name, bases, attrs)

class User(metaclass=ValidatedMeta):
    """검증된 사용자 클래스"""
    
    name = ValidatedAttribute(
        StringValidator(min_length=2, max_length=50),
        default="Unknown"
    )
    age = ValidatedAttribute(
        IntegerValidator(min_value=0, max_value=150),
        default=0
    )
    email = ValidatedAttribute(
        StringValidator(pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
        default=""
    )
    
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email
    
    def __str__(self):
        return f"User(name='{self.name}', age={self.age}, email='{self.email}')"

# 테스트
try:
    user = User("Alice", 25, "alice@example.com")
    print(user)
    
    # 잘못된 값 설정 시도
    user.age = -5  # 에러 발생
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    user2 = User("", 25, "invalid-email")  # 에러 발생
except ValidationError as e:
    print(f"Validation error: {e}")
```

###️ 프로젝트 2: 간단한 ORM 프레임워크

```python
import sqlite3
from typing import Any, Dict, List

class DatabaseField:
    """데이터베이스 필드 정의"""
    
    def __init__(self, field_type, primary_key=False, nullable=True, default=None):
        self.field_type = field_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
    
    def to_sql_type(self):
        """Python 타입을 SQL 타입으로 변환"""
        type_mapping = {
            int: 'INTEGER',
            str: 'TEXT',
            float: 'REAL',
            bool: 'BOOLEAN'
        }
        return type_mapping.get(self.field_type, 'TEXT')

class QuerySet:
    """쿼리 실행을 위한 클래스"""
    
    def __init__(self, model_class, db_connection):
        self.model_class = model_class
        self.db_connection = db_connection
    
    def create(self, **kwargs):
        """새 레코드 생성"""
        fields = list(self.model_class._fields.keys())
        placeholders = ', '.join(['?' for _ in fields])
        field_names = ', '.join(fields)
        
        values = [kwargs.get(field, self.model_class._fields[field].default) 
                 for field in fields]
        
        query = f"INSERT INTO {self.model_class._table_name} ({field_names}) VALUES ({placeholders})"
        cursor = self.db_connection.execute(query, values)
        self.db_connection.commit()
        
        # 생성된 객체 반환
        kwargs['id'] = cursor.lastrowid
        return self.model_class(**kwargs)
    
    def all(self):
        """모든 레코드 조회"""
        query = f"SELECT * FROM {self.model_class._table_name}"
        cursor = self.db_connection.execute(query)
        
        results = []
        for row in cursor.fetchall():
            field_names = list(self.model_class._fields.keys())
            kwargs = dict(zip(field_names, row))
            results.append(self.model_class(**kwargs))
        
        return results
    
    def filter(self, **kwargs):
        """조건에 맞는 레코드 필터링"""
        conditions = []
        values = []
        
        for field, value in kwargs.items():
            conditions.append(f"{field} = ?")
            values.append(value)
        
        where_clause = " AND ".join(conditions)
        query = f"SELECT * FROM {self.model_class._table_name} WHERE {where_clause}"
        
        cursor = self.db_connection.execute(query, values)
        
        results = []
        for row in cursor.fetchall():
            field_names = list(self.model_class._fields.keys())
            obj_kwargs = dict(zip(field_names, row))
            results.append(self.model_class(**obj_kwargs))
        
        return results

class ORMMeta(type):
    """ORM을 위한 메타클래스"""
    
    def __new__(cls, name, bases, attrs):
        # DatabaseField 인스턴스들을 찾아서 처리
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, DatabaseField):
                fields[key] = value
                attrs.pop(key)  # 필드는 클래스 속성에서 제거
        
        # 메타데이터 설정
        attrs['_fields'] = fields
        attrs['_table_name'] = name.lower()
        
        new_class = super().__new__(cls, name, bases, attrs)
        
        # 동적으로 프로퍼티 생성
        for field_name, field in fields.items():
            cls._create_property(new_class, field_name, field)
        
        return new_class
    
    @staticmethod
    def _create_property(cls, field_name, field):
        """필드에 대한 프로퍼티 생성"""
        private_name = f'_{field_name}'
        
        def getter(self):
            return getattr(self, private_name, field.default)
        
        def setter(self, value):
            if not field.nullable and value is None:
                raise ValueError(f"{field_name} cannot be None")
            if value is not None and not isinstance(value, field.field_type):
                # 타입 변환 시도
                try:
                    value = field.field_type(value)
                except (ValueError, TypeError):
                    raise TypeError(f"{field_name} must be of type {field.field_type.__name__}")
            setattr(self, private_name, value)
        
        setattr(cls, field_name, property(getter, setter))

class Model(metaclass=ORMMeta):
    """ORM 모델 기본 클래스"""
    
    _db_connection = None
    
    @classmethod
    def set_database(cls, db_path):
        """데이터베이스 연결 설정"""
        cls._db_connection = sqlite3.connect(db_path, check_same_thread=False)
        cls._create_table()
    
    @classmethod
    def _create_table(cls):
        """테이블 생성"""
        if not cls._fields:
            return
        
        columns = []
        for field_name, field in cls._fields.items():
            column_def = f"{field_name} {field.to_sql_type()}"
            if field.primary_key:
                column_def += " PRIMARY KEY"
            if not field.nullable:
                column_def += " NOT NULL"
            columns.append(column_def)
        
        columns_sql = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {cls._table_name} ({columns_sql})"
        cls._db_connection.execute(query)
        cls._db_connection.commit()
    
    @classmethod
    def objects(cls):
        """QuerySet 반환"""
        return QuerySet(cls, cls._db_connection)
    
    def __init__(self, **kwargs):
        for field_name in self._fields:
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name])
    
    def __str__(self):
        field_values = []
        for field_name in self._fields:
            value = getattr(self, field_name)
            field_values.append(f"{field_name}={value}")
        return f"{self.__class__.__name__}({', '.join(field_values)})"

# 모델 정의
class User(Model):
    id = DatabaseField(int, primary_key=True)
    name = DatabaseField(str, nullable=False)
    email = DatabaseField(str, nullable=False)
    age = DatabaseField(int, default=0)

class Post(Model):
    id = DatabaseField(int, primary_key=True)
    title = DatabaseField(str, nullable=False)
    content = DatabaseField(str, default="")
    user_id = DatabaseField(int, nullable=False)

# 사용 예제
if __name__ == "__main__":
    # 데이터베이스 설정
    User.set_database(":memory:")  # 메모리 데이터베이스 사용
    Post.set_database(":memory:")
    
    # 사용자 생성
    user1 = User.objects().create(name="Alice", email="alice@example.com", age=25)
    user2 = User.objects().create(name="Bob", email="bob@example.com", age=30)
    
    print("Created users:")
    for user in User.objects().all():
        print(f"  {user}")
    
    # 포스트 생성
    post1 = Post.objects().create(title="Hello World", content="First post", user_id=user1.id)
    post2 = Post.objects().create(title="Python Tips", content="Some tips", user_id=user1.id)
    
    print("\nAll posts:")
    for post in Post.objects().all():
        print(f"  {post}")
    
    # 필터링
    alice_posts = Post.objects().filter(user_id=user1.id)
    print(f"\nAlice's posts ({len(alice_posts)}):")
    for post in alice_posts:
        print(f"  {post}")
```

## 체크리스트

### 메타클래스 기본 개념
- [ ] 클래스도 객체라는 개념 이해
- [ ] type의 두 가지 역할 구분
- [ ] 인스턴스-클래스-메타클래스 계층 구조 파악
- [ ] 메타클래스가 언제 필요한지 판단

### 동적 클래스 생성
- [ ] type() 함수로 클래스 동적 생성
- [ ] 상속 관계가 있는 동적 클래스 생성
- [ ] 메서드와 속성 동적 할당
- [ ] 클래스 네임스페이스 조작

### 커스텀 메타클래스
- [ ] type 상속한 메타클래스 구현
- [ ] __new__ 메서드 활용
- [ ] __init__ 메서드와 차이점 이해
- [ ] 메타클래스로 클래스 동작 제어

### 고급 기능
- [ ] __prepare__ 메서드 활용
- [ ] __call__ 메서드로 인스턴스 생성 제어
- [ ] 싱글톤 패턴 구현
- [ ] 자동 등록 시스템 구현

### 실용적 활용
- [ ] ORM 스타일 모델 구현
- [ ] 속성 검증 시스템 구현
- [ ] 플러그인 아키텍처 구현
- [ ] 디버깅 도구 구현

### 메타클래스 대안
- [ ] 클래스 데코레이터 활용
- [ ] __init_subclass__ 활용
- [ ] 상황에 맞는 최적 선택

## 다음 단계

🎉 **축하합니다!** 메타클래스를 마스터했습니다.

메타클래스는 파이썬의 가장 고급 기능 중 하나입니다. 이제 [17. 동시성 프로그래밍](../17_concurrency/)으로 넘어가서 멀티스레딩과 멀티프로세싱을 활용한 병렬 처리를 학습해봅시다.

---

💡 **메타클래스 사용 가이드:**
- **언제 사용하나?** 클래스 생성 자체를 제어해야 할 때
- **언제 사용하지 않나?** 클래스 데코레이터나 __init_subclass__로 해결 가능할 때
- **핵심 원칙:** "메타클래스는 99%의 사용자가 필요로 하지 않는 마법이다" - Tim Peters
- **실무 활용:** ORM, 플러그인 시스템, 자동 등록, 속성 검증 등
``` 