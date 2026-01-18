---
draft: true
title: "08. 모듈과 패키지"
description: "모듈/패키지 구조와 import 메커니즘을 이해해 코드를 재사용 가능하게 구성합니다. 의존성 경계와 공개 API 설계 기준을 정리해 프로젝트 구조화를 시작합니다."
tags:
  - python
  - Python
  - 파이썬
  - programming
  - 프로그래밍
  - software-engineering
  - 소프트웨어공학
  - computer-science
  - 컴퓨터과학
  - backend
  - 백엔드
  - development
  - 개발
  - best-practices
  - 베스트프랙티스
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
  - performance
  - 성능
  - concurrency
  - 동시성
  - async
  - 비동기
  - oop
  - 객체지향
  - data-structures
  - 자료구조
  - algorithms
  - 알고리즘
  - standard-library
  - 표준라이브러리
  - packaging
  - 패키징
  - deployment
  - 배포
  - architecture
  - 아키텍처
  - design-patterns
  - 디자인패턴
  - web
  - 웹
  - database
  - 데이터베이스
  - networking
  - 네트워킹
  - ci-cd
  - 자동화
  - documentation
  - 문서화
  - git
  - 버전관리
  - tooling
  - 개발도구
  - code-quality
  - 코드품질
lastmod: 2026-01-17
collection_order: 8
---
# 챕터 8: 모듈과 패키지

> "좋은 코드는 재사용 가능한 코드다" - 모듈과 패키지를 통해 체계적이고 재사용 가능한 코드를 작성해봅시다.

## 학습 목표
- 모듈의 개념과 import 시스템을 이해할 수 있다
- 패키지를 만들고 구조화할 수 있다
- 표준 라이브러리를 효과적으로 활용할 수 있다
- 가상 환경과 패키지 관리를 할 수 있다

## 핵심 개념(이론)

### 1) 모듈과 패키지의 역할과 경계
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
- 모듈과 패키지는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 모듈 기본

### 모듈 생성과 import

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

### import 방법들

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

### 기본 패키지 구조

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

### 패키지 파일 예제

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

###️ 프로젝트: Task Manager 패키지

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

### 모듈 시스템
- **import 문**: 다양한 import 방법들
- **모듈 경로**: sys.path와 PYTHONPATH
- **모듈 속성**: __name__, __file__, __doc__
- **표준 라이브러리**: 내장 모듈들 활용

### 패키지 구조
- **__init__.py**: 패키지 초기화 파일
- **상대 import**: . 과 .. 사용법
- **__all__**: 공개 API 정의
- **패키지 계층**: 중첩된 패키지 구조

### 가상 환경과 패키지 관리
- **venv**: 표준 가상 환경 도구
- **pip**: 패키지 설치와 관리
- **requirements.txt**: 의존성 명세
- **패키지 배포**: setup.py, pyproject.toml

## 체크리스트

### 모듈 기본
- [ ] import 문 다양한 형태 이해
- [ ] 모듈 경로와 검색 순서 파악
- [ ] 표준 라이브러리 주요 모듈 활용
- [ ] __name__ == "__main__" 패턴 이해

### 패키지 설계
- [ ] 적절한 패키지 구조 설계
- [ ] __init__.py 파일 활용
- [ ] 상대 import와 절대 import 구분
- [ ] 패키지 공개 API 설계

### 환경 관리
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
