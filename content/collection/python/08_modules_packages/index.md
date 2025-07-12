---
draft: true
title: "08. 모듈과 패키지"
description: "코드 구조화와 재사용을 위한 모듈과 패키지 시스템"
collection_order: 8
---

# 챕터 8: 모듈과 패키지

> "좋은 코드는 재사용 가능한 코드다" - 모듈과 패키지를 통해 체계적이고 재사용 가능한 코드를 작성해봅시다.

## 학습 목표
- 모듈의 개념과 import 시스템을 이해할 수 있다
- 패키지를 만들고 구조화할 수 있다
- 표준 라이브러리를 효과적으로 활용할 수 있다
- 가상 환경과 패키지 관리를 할 수 있다

## 모듈 기본

### 1. 모듈 생성과 import

```python
# math_utils.py 파일 생성
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

PI = 3.14159

if __name__ == "__main__":
    print("math_utils 모듈이 직접 실행되었습니다.")
```

### 2. import 방법들

```python
# 방법 1: 전체 모듈 import
import math_utils
result = math_utils.add(5, 3)

# 방법 2: 특정 함수만 import
from math_utils import add, PI

# 방법 3: 별칭 사용
import math_utils as math
from math_utils import factorial as fact

# 방법 4: 표준 라이브러리 활용
import datetime
import os
import json
from collections import Counter, defaultdict
```

## 패키지 구조

### 1. 기본 패키지 구조

```
my_package/
    __init__.py
    math_operations/
        __init__.py
        basic.py
        advanced.py
    string_utils/
        __init__.py
        validators.py
        formatters.py
```

### 2. 패키지 파일 예제

```python
# my_package/__init__.py
"""My Package v1.0.0"""
from .math_operations.basic import add, subtract
from .string_utils.validators import is_email

__version__ = "1.0.0"

# my_package/math_operations/basic.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# my_package/string_utils/validators.py
import re

def is_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

## 실습 프로젝트

### 🛠️ 프로젝트: Task Manager 패키지

```python
# task_manager/__init__.py
from .task import Task
from .project import Project

__version__ = "1.0.0"

def create_task(title, description=""):
    return Task(title, description)

# task_manager/task.py
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = "대기중"
    IN_PROGRESS = "진행중"
    COMPLETED = "완료"

class Task:
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
    
    def start(self):
        self.status = TaskStatus.IN_PROGRESS
    
    def complete(self):
        self.status = TaskStatus.COMPLETED
    
    def __str__(self):
        return f"Task: {self.title} [{self.status.value}]"

# 사용 예제
import task_manager

task = task_manager.create_task("웹사이트 개발", "홈페이지 리뉴얼")
task.start()
print(task)  # Task: 웹사이트 개발 [진행중]
```

## 핵심 내용

### 1. 모듈 시스템
- **import 문**: 다양한 import 방법들
- **모듈 경로**: sys.path와 PYTHONPATH
- **모듈 속성**: __name__, __file__, __doc__
- **표준 라이브러리**: 내장 모듈들 활용

### 2. 패키지 구조
- **__init__.py**: 패키지 초기화 파일
- **상대 import**: . 과 .. 사용법
- **__all__**: 공개 API 정의
- **패키지 계층**: 중첩된 패키지 구조

### 3. 가상 환경과 패키지 관리
- **venv**: 표준 가상 환경 도구
- **pip**: 패키지 설치와 관리
- **requirements.txt**: 의존성 명세
- **패키지 배포**: setup.py, pyproject.toml

## 체크리스트

### ✅ 모듈 기본
- [ ] import 문 다양한 형태 이해
- [ ] 모듈 경로와 검색 순서 파악
- [ ] 표준 라이브러리 주요 모듈 활용
- [ ] __name__ == "__main__" 패턴 이해

### ✅ 패키지 설계
- [ ] 적절한 패키지 구조 설계
- [ ] __init__.py 파일 활용
- [ ] 상대 import와 절대 import 구분
- [ ] 패키지 공개 API 설계

### ✅ 환경 관리
- [ ] 가상 환경 생성과 활용
- [ ] 패키지 설치와 관리
- [ ] 의존성 관리
- [ ] 프로젝트 구조화

## 다음 단계

🎉 **축하합니다!** 파이썬 모듈과 패키지를 마스터했습니다.

이제 [09. 객체지향 프로그래밍 기초](../09_oop_basics/)로 넘어가서 더 체계적인 코드 구조화 방법을 학습해봅시다.

---

💡 **팁:**
- 모듈과 패키지로 코드를 논리적으로 구조화하세요
- __init__.py를 통해 패키지의 공개 인터페이스를 명확히 하세요
- 표준 라이브러리를 적극 활용하여 바퀴를 다시 발명하지 마세요
- 가상 환경을 사용하여 프로젝트별 의존성을 관리하세요 