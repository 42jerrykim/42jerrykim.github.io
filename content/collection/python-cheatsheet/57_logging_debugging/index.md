---

image: "wordcloud.png"
title: "[Python Cheatsheet] 57. Logging & Debugging - traceback 읽기"
slug: "effective-logging-debug-exception-traceback-best-practices"
description: "로깅과 디버깅을 빠르게 정리하는 치트시트입니다. logging 기본 설정, logger 사용 패턴, 예외 로깅(exception), traceback 읽는 법, breakpoint/pdb 활용(선택)과 실무 함정을 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 57
tags:
  - Python
  - 파이썬
  - Cheatsheet
  - 치트시트
  - Quick-Reference
  - logging
  - 로깅
  - debugging
  - 디버깅
  - error-handling
  - Monitoring
  - 모니터링
  - troubleshooting
  - 트러블슈팅
  - 성능
  - Performance
  - Best-Practices
  - pitfalls
  - 함정
  - testing
  - 테스트
  - Tutorial
  - 튜토리얼
  - Implementation
  - 구현
  - Code-Quality
  - 코드품질
  - Stack
  - String
  - HTML
  - Configuration
  - 에러처리
  - Documentation
  - 문서화
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - Optimization
  - 최적화
  - 설정
  - Guide
  - 가이드
  - Deployment
  - 배포
  - Automation
  - 자동화
  - Workflow
  - 워크플로우
  - Education
---
로깅과 디버깅은 문제를 빠르게 찾고 운영 환경을 모니터링하는 핵심 도구입니다. 이 치트시트는 logging 설정, 예외 로깅, traceback 읽는 법, breakpoint 활용을 정리합니다.

## 언제 이 치트시트를 보나?

- 예외가 났는데 “어디서 왜 났는지” 빠르게 파악해야 할 때
- print 디버깅을 로깅으로 정리하고 싶을 때

## 핵심 패턴

- 로거는 `logging.getLogger(__name__)`로 모듈 단위 생성
- 예외는 `logger.exception(...)`으로 스택트레이스를 함께 남기기(예외 처리 블록에서)
- 포맷팅은 f-string보다 로깅 포맷(지연 평가)도 고려: `logger.info("x=%s", x)`

## 최소 예제

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("service started")
```

```python
import logging

logger = logging.getLogger(__name__)

try:
    1 / 0
except ZeroDivisionError:
    logger.exception("division failed")  # traceback 포함
```

```python
# breakpoint (Py3.7+)
def f(x):
    breakpoint()
    return x + 1
```

## 자주 하는 실수/주의점

- 운영 환경에서 `print()`만으로는 추적이 어렵고, 레벨/구조화가 안 됨 → logging 사용
- `logger.exception`은 except 블록 안에서 사용해야 의미 있는 traceback이 남음
- 민감 정보(토큰/비밀번호)를 로그에 남기지 말기

## 관련 링크(공식 문서)

- [logging — Logging facility for Python](https://docs.python.org/3/library/logging.html)
- [The Python Debugger — pdb](https://docs.python.org/3/library/pdb.html)

