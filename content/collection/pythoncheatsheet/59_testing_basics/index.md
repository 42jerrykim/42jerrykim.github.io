---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 59. Testing - unittest/pytest 관점"
slug: "testing-testing-basics-tests-unit-test-integration-test-unittest-aaa"
description: "테스트를 빠르게 시작하기 위한 치트시트입니다. Arrange-Act-Assert, pytest 스타일 assert, unittest 기본, fixture/parameterize 개념, mock의 최소 사용 원칙과 실무에서 자주 깨지는 포인트를 정리합니다."
lastmod: 2026-01-17
collection_order: 59
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - testing
  - tests
  - 테스트
  - unit-test
  - 단위테스트
  - integration-test
  - 통합테스트
  - unittest
  - pytest
  - assert
  - assertions
  - AAA
  - arrange-act-assert
  - fixture
  - fixtures
  - parameterize
  - parametrization
  - mocking
  - mock
  - patch
  - test-double
  - stub
  - coverage
  - 코드커버리지
  - regression
  - 회귀테스트
  - refactoring
  - 리팩토링
  - debugging
  - 디버깅
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - ci
  - automation
  - 자동화
  - reliability
  - 안정성
  - design
  - 설계
  - dependency-injection
  - 의존성주입
  - standard-library
  - 표준라이브러리
---
테스트는 코드 변경에 대한 자신감을 주고 리팩토링을 안전하게 합니다. 이 치트시트는 AAA 패턴, pytest/unittest 기본, fixture, mock의 최소 사용 원칙을 정리합니다.

## 언제 이 치트시트를 보나?

- 기능을 추가/수정했는데 “어디가 깨질지” 불안할 때
- 리팩토링을 안전하게 하고 싶을 때

## 핵심 패턴

- 테스트는 **AAA(Arrange-Act-Assert)**로 읽기 쉽게
- 가능하면 “순수 함수/의존성 분리”로 테스트하기 쉬운 구조 만들기
- mock은 마지막 수단(행동 검증이 필요할 때만 최소로)

## 최소 예제

```python
def add(a: int, b: int) -> int:
    return a + b

def test_add():
    # Arrange
    a, b = 1, 2
    # Act
    out = add(a, b)
    # Assert
    assert out == 3
```

```python
import unittest

class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 2, 3)

if __name__ == "__main__":
    unittest.main()
```

## 자주 하는 실수/주의점

- 테스트가 “구현 디테일”에 붙으면 리팩토링 때 같이 깨짐 → 결과/계약 중심으로
- 외부 의존(DB/네트워크)을 그대로 붙이면 느리고 flaky해짐 → 경계 분리/대체 전략 필요
- 테스트 이름/데이터를 읽기 좋게 만들면 유지보수가 쉬워짐

## 관련 링크(공식 문서)

- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)
