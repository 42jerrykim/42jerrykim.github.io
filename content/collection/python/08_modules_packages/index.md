---
draft: true
title: "08. 모듈과 패키지"
description: "모듈/패키지 구조와 import 메커니즘을 이해해 코드를 재사용 가능하게 구성합니다. 의존성 경계와 공개 API 설계 기준을 정리해 프로젝트 구조화를 시작합니다."
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

## 핵심 내용

### 모듈 생성과 import 방식

파이썬에서는 **모듈(module)**이 코드 재사용의 최소 단위입니다. 확장자 `.py`로 끝나는 파일 하나가 곧 하나의 모듈이며, 특별한 선언 없이 함수·클래스·변수를 정의하기만 하면 다른 파일에서 그대로 가져다 쓸 수 있습니다. `import` 문을 만나면 파이썬 인터프리터는 먼저 `sys.modules`라는 전역 캐시를 확인합니다. 해당 모듈이 이미 로드되어 있으면 캐시된 모듈 객체를 즉시 반환하고, 없으면 파일을 찾아 처음부터 끝까지 실행한 뒤 그 결과(정의된 이름들)를 모듈 객체에 담아 캐시에 등록합니다. 즉 같은 프로세스 안에서 동일한 모듈을 100번 import해도 **파일 내용은 딱 한 번만 실행**됩니다. "import할 때마다 파일이 다시 실행된다"는 흔한 오해와 달리, 두 번째 import부터는 캐시 조회에 불과합니다.

```python
# math_utils.py
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
    print(f"add(2, 3) = {add(2, 3)}")
```

`if __name__ == "__main__":` 관용구는 이 캐시 동작과 밀접합니다. 파이썬은 실행되는 모든 모듈에 `__name__`이라는 특수 변수를 자동으로 채워 넣는데, **직접 실행된 파일**의 `__name__`은 항상 문자열 `"__main__"`이 되고, **다른 곳에서 import된 모듈**의 `__name__`은 해당 모듈의 실제 이름(`math_utils`)이 됩니다. 이 차이를 이용하면 한 파일을 "import될 때는 함수 정의만 제공하고, 직접 실행될 때는 데모 코드를 돌리는" 두 가지 용도로 겸용할 수 있습니다. 위 예제를 `python math_utils.py`로 직접 실행하면 `if` 블록이 동작하지만, 다른 파일에서 `import math_utils`로 가져오면 그 블록은 실행되지 않습니다.

같은 모듈을 가져오는 방법은 상황에 따라 나뉘고, 각각 이름이 어느 네임스페이스에 등록되는지가 다릅니다. `import module_name`은 모듈 객체 전체를 현재 네임스페이스에 등록하므로 항상 `module_name.attr` 형태로 접근해야 하며, 어느 모듈에서 온 이름인지 코드만 보고 알 수 있어 가독성이 좋습니다. `from module_name import name`은 모듈 안의 특정 이름만 현재 네임스페이스로 **복사**합니다. 이때 복사되는 것은 객체에 대한 참조이므로, 가져온 이름을 재할당해도 원본 모듈의 이름에는 영향이 없습니다. `as` 별칭은 이름 충돌을 피하거나(표준 라이브러리 `math`와 사용자 정의 이름이 겹치는 경우 등) 긴 이름을 줄일 때 씁니다.

```python
# 방법 1: 모듈 전체 import — module.attr 형태로 접근
import math_utils
result = math_utils.add(5, 3)

# 방법 2: 특정 이름만 import — 현재 네임스페이스로 복사
from math_utils import add, PI
result = add(5, 3)

# 방법 3: 별칭(as) — 이름 충돌 회피, 긴 이름 축약
import math_utils as mu
from math_utils import factorial as fact

# 방법 4: 표준 라이브러리도 동일한 문법을 따른다
import json
from collections import Counter, defaultdict
```

`import`가 어떤 파일을 찾아낼지는 **모듈 검색 경로**가 결정합니다. 파이썬은 `sys.path`라는 문자열 리스트를 순서대로 훑으면서 요청된 이름과 일치하는 `.py` 파일이나 패키지 디렉터리를 찾습니다. 이 리스트는 대체로 (1) 실행 중인 스크립트가 위치한 디렉터리, (2) 환경 변수 `PYTHONPATH`에 나열된 경로, (3) 표준 라이브러리 설치 경로, (4) `pip`로 설치한 서드파티 패키지가 놓이는 `site-packages` 순서로 구성됩니다. 이 검색 규칙의 세부 사항은 파이썬 공식 문서의 [Import System](https://docs.python.org/3/reference/import.html)에 정리되어 있습니다. 원하는 경로 어디에서도 모듈을 찾지 못하면 `ModuleNotFoundError`가 발생합니다.

```python
import sys

# 검색 경로 확인 (실행 위치에 따라 내용은 달라진다)
for path in sys.path:
    print(path)

# 런타임에 경로를 추가할 수도 있지만, 임시방편에 가깝다
sys.path.append("/path/to/my/modules")
```

`sys.path`를 직접 조작해서 문제를 해결하는 방식은 스크립트 하나짜리 실험에는 편리하지만, 협업 프로젝트에서는 경로가 실행 위치·운영체제에 따라 달라져 재현성이 떨어집니다. 실무에서는 프로젝트를 패키지로 구조화하고 `pip install -e .`(editable install)로 설치하거나, 프로젝트 루트에서 `python -m package.module`처럼 모듈 형태로 실행해 `sys.path` 조작 없이도 import가 정상 동작하게 만드는 쪽을 우선합니다.

### 패키지 구조

여러 모듈이 늘어나면 파일 하나로는 관리가 어려워지고, 이때 **패키지(package)**로 묶어 계층을 만듭니다. 패키지는 본질적으로 `__init__.py` 파일을 포함한 디렉터리입니다. `__init__.py`는 세 가지 역할을 겸합니다. 첫째, 해당 디렉터리가 단순 폴더가 아니라 import 가능한 패키지임을 파이썬에 알리는 표식입니다(파이썬 3.3부터는 `__init__.py` 없이도 네임스페이스 패키지로 동작하지만, 명시적인 `__init__.py`가 여전히 표준적이고 예측 가능한 선택입니다). 둘째, 패키지가 처음 import될 때 실행되는 초기화 코드를 담는 자리입니다. 셋째, 하위 모듈 중 무엇을 패키지의 공개 API로 노출할지 결정하는 재수출(re-export) 지점입니다. `__init__.py`에서 하위 모듈의 이름을 미리 import해 두면, 사용자는 내부 파일 구조를 몰라도 `package.name`만으로 접근할 수 있습니다.

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

패키지 내부 모듈이 서로를 참조할 때는 **절대 import**와 **상대 import** 중 하나를 선택합니다. 절대 import는 최상위 패키지 이름부터 전체 경로를 명시하는 방식으로(`from my_package.math_operations.basic import add`), 어디서 실행하든 대상이 명확하다는 장점이 있습니다. 상대 import는 현재 모듈이 속한 패키지를 기준으로 `.`(같은 패키지), `..`(상위 패키지)처럼 상대 경로로 표기하는 방식으로(`from .basic import add`), [PEP 328](https://peps.python.org/pep-0328/)에서 도입되었습니다. 패키지 내부 리팩터링으로 최상위 패키지 이름 자체가 바뀌어도 상대 import는 코드를 고칠 필요가 없다는 것이 이점입니다.

```python
# my_package/__init__.py — 하위 모듈의 이름을 재수출해 공개 API를 만든다
from .math_operations.basic import add, subtract
from .string_utils.validators import is_email

__all__ = ["add", "subtract", "is_email"]
__version__ = "1.0.0"

# my_package/math_operations/basic.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# my_package/string_utils/validators.py
import re  # 표준 라이브러리는 절대 import로 가져온다

def is_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

상대 import에는 한 가지 함정이 있습니다. `from .basic import add`가 적힌 파일을 `python basic.py`처럼 **스크립트로 직접 실행**하면 `ImportError: attempted relative import with no known parent package` 오류가 발생합니다. 직접 실행된 파일의 `__name__`은 `"__main__"`이 되어 파이썬이 그 파일을 어떤 패키지에도 속하지 않은 것으로 취급하기 때문입니다. 상대 import를 쓰는 모듈은 반드시 패키지의 일부로서 `import my_package.math_operations.basic`처럼 가져오거나, 프로젝트 루트에서 `python -m my_package.math_operations.basic`처럼 모듈로 실행해야 합니다. `__init__.py`에 정의하는 `__all__` 리스트는 `from package import *`로 가져올 때 어떤 이름까지 노출할지 제한하는 용도로, 의도치 않은 내부 구현 노출을 막는 안전장치입니다.

### 표준 라이브러리 활용

파이썬은 "배터리 포함(batteries included)" 철학으로 유명합니다. 파일 처리, 날짜 계산, 정규식, 자료구조 확장까지 별도 설치 없이 표준 라이브러리만으로 상당 부분을 해결할 수 있습니다. 아래 표는 자주 쓰이는 모듈을 용도별로 정리한 것이며, 각 모듈의 세부 API와 활용 패턴은 [11장 표준 라이브러리 탐구](../11_standard_library/)에서 더 자세히 다룹니다.

| 모듈 | 주요 용도 |
|------|----------|
| `os`, `pathlib` | 파일·디렉터리 경로 조작 |
| `sys` | 인터프리터 상태, 명령행 인자, 모듈 검색 경로 |
| `json` | JSON 직렬화/역직렬화 |
| `datetime` | 날짜와 시간 계산 |
| `collections` | `Counter`, `defaultdict` 등 확장 자료구조 |

## 실습 프로젝트

### 프로젝트 1: Task Manager 패키지

앞서 설명한 상대 import와 `__init__.py` 재수출 패턴을 실제 패키지에 적용해 봅니다. `task_manager` 패키지는 `task.py`와 `project.py` 두 모듈을 가지고, `__init__.py`가 이 둘을 재수출해 사용자가 내부 파일 구조를 몰라도 `task_manager.Task`처럼 바로 접근할 수 있게 합니다.

```
task_manager/
    __init__.py
    task.py
    project.py
```

```python
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


# task_manager/project.py
from .task import Task, TaskStatus  # 같은 패키지 안의 형제 모듈 — 상대 import

class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, title, description=""):
        task = Task(title, description)
        self.tasks.append(task)
        return task

    def progress(self):
        if not self.tasks:
            return 0.0
        done = sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED)
        return done / len(self.tasks) * 100


# task_manager/__init__.py
from .task import Task, TaskStatus
from .project import Project

__all__ = ["Task", "TaskStatus", "Project"]
__version__ = "1.0.0"

def create_task(title, description=""):
    return Task(title, description)
```

```python
# 사용 예제 (외부에서는 절대 import)
import task_manager

task = task_manager.create_task("웹사이트 개발", "홈페이지 리뉴얼")
task.start()
print(task)  # Task: 웹사이트 개발 [진행중]

project = task_manager.Project("리뉴얼 프로젝트")
project.add_task("디자인 시안", "메인 페이지 시안 작성")
project.add_task("퍼블리싱")
project.tasks[0].complete()
print(f"진행률: {project.progress():.1f}%")  # 진행률: 50.0%
```

패키지 외부에서는 `import task_manager` 한 줄로 `Task`, `TaskStatus`, `Project`, `create_task`에 모두 접근할 수 있습니다. `__init__.py`가 재수출을 담당한 덕분에 사용자는 `task_manager.task.Task`처럼 내부 파일 경로를 알 필요가 없습니다. 이것이 앞서 "패키지 구조"에서 설명한 공개 API 설계의 실제 효과입니다.

### 프로젝트 2: 설정 관리자 패키지

두 번째 프로젝트는 여러 하위 모듈이 같은 인터페이스(`load()` 함수)를 따르게 하고, `__main__.py`를 이용해 패키지를 스크립트처럼 실행하는 구조를 보여줍니다. `config_loader` 패키지는 설정을 JSON 파일과 환경 변수 중 어디서 읽을지를 소스별로 나눕니다.

```
config_loader/
    __init__.py
    __main__.py
    loader.py
    sources/
        __init__.py
        json_source.py
        env_source.py
```

```python
# config_loader/sources/json_source.py
import json
from pathlib import Path

def load(path):
    """JSON 파일에서 설정을 읽는다."""
    file_path = Path(path)
    if not file_path.exists():
        return {}
    with file_path.open(encoding="utf-8") as f:
        return json.load(f)


# config_loader/sources/env_source.py
import os

def load(prefix="APP_"):
    """지정한 접두사를 가진 환경 변수를 설정으로 읽는다."""
    result = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            config_key = key[len(prefix):].lower()
            result[config_key] = value
    return result


# config_loader/sources/__init__.py
from . import json_source, env_source  # 함수가 아니라 모듈 자체를 재수출

__all__ = ["json_source", "env_source"]
```

`sources/__init__.py`는 앞서 본 재수출과 다른 형태입니다. 함수 하나를 꺼내는 대신 **모듈 자체**를 재수출해서, 상위 코드가 `json_source.load(...)`처럼 출처를 명시적으로 호출하게 합니다. 여러 소스가 같은 이름의 함수(`load`)를 갖는 상황에서 함수만 꺼내 오면 이름이 충돌하므로, 모듈째로 노출하는 쪽이 더 안전합니다.

```python
# config_loader/loader.py
from .sources import json_source, env_source  # 상대 import: 하위 패키지 참조

def load_config(json_path="config.json", env_prefix="APP_"):
    """JSON 설정에 환경 변수를 덮어써 병합한다."""
    config = json_source.load(json_path)
    config.update(env_source.load(env_prefix))
    return config


# config_loader/__init__.py
from .loader import load_config

__all__ = ["load_config"]


# config_loader/__main__.py
from .loader import load_config

if __name__ == "__main__":
    print(load_config())
```

```python
# 사용 예제 (외부에서는 절대 import)
import os
from config_loader import load_config

os.environ["APP_DEBUG"] = "true"
config = load_config(env_prefix="APP_")
print(config)  # {'debug': 'true'}
```

패키지를 스크립트처럼 실행하고 싶다면 `__init__.py`가 아니라 별도의 `__main__.py`가 필요합니다. `python -m config_loader`를 실행하면 파이썬은 먼저 `config_loader/__init__.py`를 평범하게 import하고(이때 `__name__`은 `"config_loader"`), 이어서 `config_loader/__main__.py`를 `__name__ == "__main__"` 상태로 실행합니다. `__init__.py` 안에 `if __name__ == "__main__":` 블록을 두어도 패키지를 `-m`으로 실행할 때는 결코 참이 되지 않는다는 것이 흔히 놓치는 함정입니다. 파일 하나짜리 스크립트에는 앞서 본 관용구가 그대로 적용되지만, 패키지 전체의 실행 진입점을 만들 때는 `__main__.py`라는 전용 파일이 필요합니다.

## 체크리스트

- **import 캐시**: `import`가 `sys.modules` 캐시를 거치며, 같은 모듈은 프로세스당 한 번만 실행된다는 것을 설명할 수 있다.
- **import 형태 구분**: `import`, `from ... import`, `as` 별칭이 네임스페이스에 이름을 등록하는 방식의 차이를 구분할 수 있다.
- **`__name__ == "__main__"`**: 이 관용구가 스크립트 실행과 모듈 import를 구분하는 원리를 설명할 수 있다.
- **모듈 검색 경로**: `sys.path`의 구성 순서를 설명하고 `ModuleNotFoundError`의 원인을 진단할 수 있다.
- **`__init__.py`의 역할**: 패키지 표식, 초기화 코드, 재수출이라는 세 가지 역할을 구분할 수 있다.
- **절대/상대 import와 `__main__.py`**: 언제 절대 import를, 언제 상대 import를 쓸지 판단하고 "no known parent package" 오류와 `python -m` 실행 방식의 차이를 설명할 수 있다.

## 다음 단계

축하합니다. 파이썬 모듈과 패키지의 동작 원리를 익혔습니다.

이제 [09. 객체지향 프로그래밍 기초](../09_oop_basics/)로 넘어가서 클래스와 객체를 통한 코드 구조화 방법을 학습해봅시다.

---

💡 **팁:**
- `import`는 모듈을 다시 실행하지 않고 캐시에서 가져온다는 점을 기억하세요. 모듈 최상위 코드에 부작용(side effect)을 두면 첫 import 시점에만 실행됩니다.
- 패키지 내부 모듈끼리는 상대 import를, 패키지 외부에서 패키지를 가져올 때는 절대 import를 사용하는 것이 일반적입니다.
- `__init__.py`의 재수출은 신중하게 하세요. 너무 많은 이름을 재수출하면 공개 API의 경계가 흐려집니다.
- 패키지를 `python -m package`로 실행하려면 `__init__.py`가 아니라 `__main__.py`가 필요하다는 것을 기억하세요.
