---
title: "[Python] Python 3.15 PEP 810: lazy import로 CLI 시작 시간 줄이기"
description: "Python 3.15에 새로 들어간 PEP 810 명시적 lazy import의 문법·동작 원리·전역 제어 옵션을 정리하고, 시작 시간 50–70% 절감 주장의 출처와 부작용 주의점, 적용 판단 기준까지 함께 살펴본다."
date: 2026-11-13T00:30:00+09:00
lastmod: 2026-11-13
draft: false
categories:
  - Python
  - Programming
tags:
  - Python
  - Python-3.15
  - PEP-810
  - Lazy-Import
  - Lazy-Loading
  - Import-System
  - Startup-Time
  - CLI
  - CLI-Tools
  - Command-Line
  - Performance(성능)
  - Optimization(최적화)
  - Memory(메모리)
  - Latency
  - Benchmark
  - Profiling(프로파일링)
  - Interpreter(인터프리터)
  - JIT(JIT컴파일)
  - Programming-Language(프로그래밍언어)
  - Language-Design
  - Software-Engineering(소프트웨어공학)
  - Best-Practices
  - Productivity(생산성)
  - Open-Source(오픈소스)
  - Release-Notes
  - Standard-Library
  - Circular-Import
  - Side-Effects
  - Deep-Dive
  - 파이썬
  - 지연 임포트
  - 시작 시간
image: "wordcloud.png"
---

`mytool --help`만 쳤는데 반응이 느리다면, 원인은 보통 쓰지도 않을 모듈을 시작하자마자 전부 import하기 때문이다. Python 3.15.0은 2026년 10월 9일 릴리스됐고, 대표 기능인 <strong>PEP 810(명시적 lazy import)</strong>은 이 문제를 문법 수준에서 다룬다. 이 글은 PEP 원문과 What's New를 기준으로 동작 방식과 한계를 정리한다. 성능 수치는 모두 PEP가 인용한 값이며 필자가 재측정한 것이 아니다.

## 문제: 일반 import는 즉시 로드한다

일반 `import json`은 문장을 실행하는 순간 모듈을 찾고 로드하고 실행한다. CLI 도구가 최상단에서 수십 개 모듈을 import하면 `--help`나 잘못된 인자 오류처럼 대부분의 모듈이 필요 없는 경로에서도 그 비용을 낸다.

기존 우회책은 함수 안에서 import하는 것이다. PEP는 비테스트 표준 라이브러리 import의 약 17%가 이미 함수 안에 있다고 인용한다. 하지만 의존성이 코드 곳곳에 흩어지고, 누군가 최상단에 import 한 줄을 추가하면 효과가 조용히 사라진다.

## 문법과 동작

```python
import sys

lazy import json
print('json' in sys.modules)   # False: 이름만 바인딩됨
result = json.dumps({"hello": "world"})
print('json' in sys.modules)   # True: 첫 사용 시점에 로드됨
```

`lazy`는 모듈 최상위 import 앞에만 붙일 수 있는 소프트 키워드다. 이름은 즉시 lazy 프록시 객체에 바인딩되고, 처음 사용할 때 실제 import가 일어나 이름이 진짜 객체로 교체된다(reification). `lazy from` 형태는 이름 단위로 동작한다.

```python
lazy from json import dumps, loads
result = dumps({"hello": "world"})   # dumps만 해소됨
data = loads(result)                 # loads는 이때 해소됨
```

다음은 SyntaxError다: 함수·클래스·`try` 블록 안의 `lazy`, `lazy from x import *`, `lazy from __future__ import ...`. 의존 모듈로 전파되지 않는 비재귀 방식이라, `json`이 내부적으로 하는 import는 평소대로 동작한다.

| 항목 | 동작 |
|---|---|
| 로드 시점 | 첫 사용 시 `__import__` 호출 (그 시점의 import 시스템 상태 기준) |
| 로드 실패 | lazy 객체는 그대로 남고 다음 접근에서 재시도, traceback에 정의 위치와 접근 위치가 함께 표시 |
| 해소 전 상태 | `sys.modules`가 아니라 `sys.lazy_modules`에 있음 |
| `globals()` | 해소를 일으키지 않고 원본 네임스페이스 반환 |

## 전역 제어와 호환

코드에 `lazy`를 일일이 쓰지 않고 실행 옵션으로도 제어할 수 있다. 우선순위는 `sys.set_lazy_imports()` 호출, `-X lazy_imports`, 환경변수 `PYTHON_LAZY_IMPORTS` 순이다.

| 모드 | 의미 |
|---|---|
| `normal` (기본) | 명시한 `lazy`만 지연 |
| `all` | `try` 블록·star import를 제외한 모든 최상위 import를 지연 후보로 |
| `none` | 명시한 `lazy`까지 포함해 전부 즉시 로드 |

개별 판단은 필터로 한다. 함수가 `False`를 돌려주면 그 import는 즉시 로드된다.

```python
import sys

def exclude_side_effect_modules(importer, name, fromlist):
    # False를 반환하면 이 모듈은 lazy로 두지 않고 즉시 로드
    return name not in {'legacy_plugin_system', 'metrics_collector'}

sys.set_lazy_imports_filter(exclude_side_effect_modules)
```

3.15 미만 버전과 같은 코드를 공유해야 하면 모듈 변수 `__lazy_modules__ = ["json"]`로 선언할 수 있다. 3.15에서는 해당 모듈을 `lazy`로 쓴 것처럼 처리하고, 이전 버전은 무시하므로 문법 오류가 나지 않는다.

## 성능 주장을 읽는 법

PEP는 실제 배포 사례에서 시작 시간 약 50–70% 감소, 메모리 30–40% 절감을 보고했다고 쓴다. 단, 이 수치는 PEP 자체의 통제 실험이 아니라 사례 보고다. 직접 검증하려면 `python -X importtime`으로 자기 도구의 import 비용부터 확인하는 편이 정확하다.

오버헤드 쪽은 통제 측정이 있다. 278개 표준 라이브러리 모듈을 import하는 벤치마크에서 기준선 161.2 ms 대비 설정별 161.4–162.0 ms였고, 차이는 약 4 ms 표준편차 안이다. 해소 후에는 바이트코드 특수화로 lazy 검사가 사라져 정상 상태 오버헤드가 없다는 것이 PEP의 설명이다.

## 부작용과 주의점

- **오류와 부작용이 첫 사용 시점으로 이동한다.** 설치 안 된 패키지의 ImportError가 시작이 아니라 한참 뒤 특정 명령에서 터질 수 있다.
- **import로 등록하는 패턴이 깨진다.** 플러그인 레지스트리처럼 import 부작용에 기대는 코드는 명시적 탐색으로 바꾸거나 필터로 제외해야 한다.
- **순환 import는 여전히 실패한다.** 한쪽이 import 시점에 다른 쪽을 건드리면 lazy여도 같다.
- **`.pth` 파일의 import는 항상 즉시 실행된다.**
- 필터 함수가 무거우면 그 비용은 그대로 더해진다.

## 설계에서 기각된 대안

PEP 690은 암묵적·전역 방식에 dict 타입 수정을 요구해 기각됐고, PEP 810은 명시적 키워드와 프록시 객체로 방향을 바꿨다. lazy를 기본값으로 하는 안과 `__lazy_modules__ = ["*"]`도 기각됐다. 타입 전용 문법, 블록 문법, `TYPE_CHECKING` 자동 처리, C API는 후속 과제로 미뤄졌다.

## 3.15의 다른 변경

What's New 기준으로 `frozendict` 내장 타입(PEP 814), `sentinel`(PEP 661), 샘플링 프로파일러 Tachyon을 포함한 `profiling` 패키지(PEP 799), 자유 스레딩용 Stable ABI(PEP 803), UTF-8 기본 인코딩(PEP 686), 컴프리헨션 내 `*`/`**` 언패킹(PEP 798), 기본 프레임 포인터(PEP 831)가 들어갔다. JIT도 개선됐다고 하나 세부는 확인하지 못했다.

## 적용 판단

효과가 큰 경우는 시작 시간이 체감되는 CLI, 서버리스 콜드 스타트, 무거운 선택적 의존성(pandas, numpy 등)을 일부 경로에서만 쓰는 도구다. 장기 실행 서버는 시작 비용을 한 번만 내므로 이득이 작고, 오히려 첫 요청 지연과 늦은 오류 발견이 단점이 될 수 있다. 먼저 `-X importtime`으로 병목 모듈을 찾고, 그것들에만 `lazy`를 붙이는 순서를 권한다.

## 참고 및 출처

- PEP 810 – Explicit lazy imports: <https://peps.python.org/pep-0810/>
- What's New in Python 3.15: <https://docs.python.org/3.15/whatsnew/3.15.html>
- PEP 690 – Lazy Imports (기각): <https://peps.python.org/pep-0690/>
