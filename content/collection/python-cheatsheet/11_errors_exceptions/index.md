---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 11. Errors & Exceptions - try/raise 패턴"
slug: "error-handling-exceptions-try-raise-best-practices-guide"
description: "예외 처리를 빠르게 설계/작성하기 위한 치트시트입니다. try/except/else/finally, raise/raise from, 예외 계층과 커스텀 예외, 자원 정리(with)와 로깅 연결까지 실전 패턴을 정리합니다."
lastmod: 2026-01-17
collection_order: 11
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - errors
  - exceptions
  - 예외
  - 예외처리
  - try
  - except
  - else
  - finally
  - raise
  - raise-from
  - exception-chaining
  - traceback
  - 스택트레이스
  - 디버깅
  - debugging
  - logging
  - 로깅
  - context-manager
  - 컨텍스트매니저
  - with
  - resource-management
  - 자원관리
  - custom-exception
  - 사용자정의예외
  - ValueError
  - TypeError
  - KeyError
  - IndexError
  - OSError
  - FileNotFoundError
  - assert
  - assertion
  - testing
  - 테스트
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - security
  - 보안
  - reliability
  - 안정성
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - clean-code
  - 클린코드
  - api-design
  - 설계
---
예외 처리는 견고한 프로그램의 필수 요소입니다. 이 치트시트는 try/except/else/finally 구조, raise from으로 원인 보존, 자원 정리(with) 등 실전 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- “여기서 어떤 예외를 잡아야 하지?”가 애매할 때
- 원인 예외를 잃지 않고 더 좋은 메시지로 감싸고 싶을 때

## 핵심 패턴

- 좁게 잡기: `except Exception:` 남용보다 **구체 예외**를 먼저
- 성공/실패 분리: `try/except/else`로 “성공 로직”을 else에 두면 깔끔
- 원인 보존: `raise NewError(...) from e`
- 자원 정리: `finally`보다 `with`(context manager)를 우선 고려

## 최소 예제

```python
def parse_int(s: str) -> int:
    try:
        return int(s)
    except ValueError as e:
        raise ValueError(f"invalid int: {s!r}") from e
```

```python
# try/except/else/finally
try:
    x = 10 / 2
except ZeroDivisionError:
    print("divide by zero")
else:
    print("ok:", x)
finally:
    print("always runs")
```

```python
# with: 자원 정리
with open("data.txt", "r", encoding="utf-8") as f:
    data = f.read()
```

## 자주 하는 실수/주의점

- 너무 넓게 잡으면 버그가 숨겨짐(`except Exception: pass`) → 로깅/재발생(raise) 전략 필요
- 에러 메시지에 사용자 입력을 넣을 때는 `repr`(`!r`)로 안전하게
- `assert`는 운영에서 최적화 옵션으로 비활성화될 수 있음 → 입력 검증은 예외로 처리

## 관련 링크(공식 문서)

- [Errors and Exceptions (Tutorial)](https://docs.python.org/3/tutorial/errors.html)
- [Exception hierarchy](https://docs.python.org/3/library/exceptions.html)

