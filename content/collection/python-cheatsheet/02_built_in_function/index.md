---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 02. Built-in Functions"
slug: "essential-built-in-functions-reference-fast-lookup-guide"
description: "파이썬 내장 함수/타입을 알파벳 및 용도별로 빠르게 찾는 치트시트입니다. 공식 문서 기준(A~Z, _) 전체 목록과 핵심 시그니처, 자주 하는 실수, 선택 기준을 짧게 정리합니다."
lastmod: 2026-01-17
collection_order: 2
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - builtins
  - built-in
  - built-in-functions
  - 내장함수
  - standard-library
  - 표준라이브러리
  - quick-reference
  - 빠른참조
  - abs
  - all
  - any
  - print
  - input
  - open
  - len
  - range
  - enumerate
  - zip
  - map
  - filter
  - sum
  - min
  - max
  - sorted
  - repr
  - format
  - dir
  - getattr
  - setattr
  - hasattr
  - vars
  - locals
  - globals
  - type
  - isinstance
  - issubclass
  - iter
  - next
  - aiter
  - anext
  - breakpoint
  - eval
  - exec
  - compile
  - memoryview
  - bytes
  - bytearray
  - str
  - int
  - float
  - bool
  - list
  - tuple
  - dict
  - set
  - frozenset
  - object
  - super
  - classmethod
  - staticmethod
  - property
  - slice
  - reversed
  - round
  - pow
  - hex
  - oct
  - bin
  - ord
  - chr
  - ascii
  - id
  - hash
  - help
  - __import__
last_modified_at: 2023-01-20
date: 2022-01-17
categories: Python
header:
  teaser: /assets/images/2023/Screenshot_2023-01-17_at_20-55-19_WelcometoPython.org.png
---
파이썬 인터프리터에는 항상 사용할 수 있는 많은 함수와 타입이 내장되어 있습니다. 이 치트시트는 공식 문서 기준 A~Z 전체 목록과 핵심 시그니처, 자주 하는 실수, 선택 기준을 빠르게 찾아볼 수 있게 정리합니다. 이 페이지는 [공식 문서 Built-in Functions](https://docs.python.org/3/library/functions.html) 기준으로 **A~Z, _ 전체 목록**을 빠르게 찾아볼 수 있게 정리한 치트시트입니다.

## 빠른 네비게이션

- **Alphabet**: [A](#a) [B](#b) [C](#c) [D](#d) [E](#e) [F](#f) [G](#g) [H](#h) [I](#i) [L](#l) [M](#m) [N](#n) [O](#o) [P](#p) [R](#r) [S](#s) [T](#t) [V](#v) [Z](#z) [_](#_)
- **By use-case**:
  - [반복/이터레이션](#by-usecase-iteration)
  - [타입/변환](#by-usecase-types)
  - [문자열/표현/포맷](#by-usecase-text)
  - [리스트/정렬/집계](#by-usecase-collections)
  - [리플렉션/인스펙션](#by-usecase-reflection)
  - [실행/코드 평가(주의)](#by-usecase-exec)
  - [입출력/파일](#by-usecase-io)
  - [비동기](#by-usecase-async)

## Notes (꼭 알아둘 것)

- `zip(*iterables, strict=False)`는 3.10+에서 `strict`가 추가되었습니다. 길이 불일치 버그를 숨기기 싫다면 `strict=True`를 고려하세요. (공식 문서: [Built-in Functions](https://docs.python.org/3/library/functions.html))
- `aiter()`/`anext()`는 3.10+ 추가된 비동기 내장 함수입니다. (공식 문서: [Built-in Functions](https://docs.python.org/3/library/functions.html))
- `eval()`/`exec()`/`compile()`은 강력하지만 **보안/유지보수 리스크**가 큽니다. 가능한 대안을 우선 고려하세요. (공식 문서: [Built-in Functions](https://docs.python.org/3/library/functions.html))
- `__import__()`는 고급 기능이며 직접 사용은 일반적으로 권장되지 않습니다. (공식 문서: [Built-in Functions](https://docs.python.org/3/library/functions.html))

## By use-case

### By use-case: iteration

주로 “반복/순회/변환”에서 가장 자주 찾습니다.

- `enumerate`, `zip`, `iter`, `next`, `range`, `reversed`
- `all`, `any`, `map`, `filter`

### By use-case: types

타입 생성/변환.

- `bool`, `int`, `float`, `complex`
- `str`, `bytes`, `bytearray`, `memoryview`
- `list`, `tuple`, `set`, `frozenset`, `dict`, `object`
- `type`, `isinstance`, `issubclass`

### By use-case: text

문자열/표현/포맷/코드포인트.

- `format`, `repr`, `ascii`
- `chr`, `ord`

### By use-case: collections

정렬/집계/수치.

- `len`, `sum`, `min`, `max`, `sorted`, `round`, `pow`, `divmod`

### By use-case: reflection

인스펙션/동적 접근.

- `dir`, `vars`, `locals`, `globals`
- `getattr`, `setattr`, `hasattr`, `delattr`
- `callable`, `id`, `hash`, `help`

### By use-case: exec

코드 실행/평가(주의).

- `eval`, `exec`, `compile`, `__import__`

### By use-case: io

입출력/파일.

- `print`, `input`, `open`

### By use-case: async

비동기 반복.

- `aiter`, `anext`

---

## A

### abs

- **Signature**: `abs(number, /)`
- **What**: 숫자의 절댓값(복소수면 크기)을 반환.

### aiter

- **Signature**: `aiter(async_iterable, /)`
- **What**: 비동기 이터러블의 async iterator를 반환.
- **Version**: Added in 3.10.

### all

- **Signature**: `all(iterable, /)`
- **What**: 모든 요소가 truthy(또는 비어있으면) `True`.

### anext

- **Signature**: `anext(async_iterator, /)` / `anext(async_iterator, default, /)`
- **What**: async iterator의 다음 값을 await로 받음. exhausted면 default 또는 `StopAsyncIteration`.
- **Version**: Added in 3.10.

### any

- **Signature**: `any(iterable, /)`
- **What**: 요소 중 하나라도 truthy면 `True`(비어있으면 `False`).

### ascii

- **Signature**: `ascii(object, /)`
- **What**: `repr()`과 유사하되 non-ASCII를 이스케이프해 반환.

## B

### bin

- **Signature**: `bin(integer, /)`
- **What**: 정수를 `0b...` 이진 문자열로 변환.

### bool

- **Signature**: `bool(object=False, /)`
- **What**: truthiness를 불리언으로 변환.

### breakpoint

- **Signature**: `breakpoint(*args, **kws)`
- **What**: 디버거 진입(기본은 `pdb`).

### bytearray

- **Signature**: `bytearray(...)`
- **What**: 가변 바이트 시퀀스 타입.

### bytes

- **Signature**: `bytes(...)`
- **What**: 불변 바이트 시퀀스 타입.

## C

### callable

- **Signature**: `callable(object, /)`
- **What**: 호출 가능한 객체인지 반환.

### chr

- **Signature**: `chr(i, /)`
- **What**: 유니코드 코드포인트 정수 → 1글자 문자열.

### classmethod

- **Signature**: `classmethod(function, /)`
- **What**: 클래스 메서드 디스크립터로 변환.

### compile

- **Signature**: `compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)`
- **What**: 소스 코드를 코드 객체로 컴파일.
- **Gotchas**: 외부 입력을 컴파일/실행하는 패턴은 보안상 매우 위험.

### complex

- **Signature**: `complex(...)`
- **What**: 복소수 타입 생성/변환.

## D

### delattr

- **Signature**: `delattr(object, name, /)`
- **What**: 속성 삭제.

### dict

- **Signature**: `dict(...)`
- **What**: 매핑 타입.

### dir

- **Signature**: `dir([object])`
- **What**: 현재/객체의 속성 이름 목록(디버깅용).

### divmod

- **Signature**: `divmod(a, b, /)`
- **What**: `(a // b, a % b)`를 튜플로 반환.

## E

### enumerate

- **Signature**: `enumerate(iterable, start=0)`
- **What**: `(index, value)`를 생성하는 이터레이터.

### eval

- **Signature**: `eval(source, /, globals=None, locals=None)`
- **What**: 표현식을 평가.
- **Gotchas**: 신뢰할 수 없는 입력에 절대 사용 금지(코드 실행 취약점).

### exec

- **Signature**: `exec(source, /, globals=None, locals=None, *, closure=None)`
- **What**: 동적 코드 실행.
- **Gotchas**: 신뢰할 수 없는 입력에 절대 사용 금지.

## F

### filter

- **Signature**: `filter(function, iterable)`
- **What**: 조건에 맞는 요소만 걸러내는 이터레이터.

### float

- **Signature**: `float(...)`
- **What**: 부동소수 타입 변환/생성.

### format

- **Signature**: `format(value, format_spec='')`
- **What**: 포맷 규칙에 따라 문자열로 변환.

### frozenset

- **Signature**: `frozenset([iterable])`
- **What**: 불변 set.

## G

### getattr

- **Signature**: `getattr(object, name[, default])`
- **What**: 동적으로 속성 조회.

### globals

- **Signature**: `globals()`
- **What**: 전역 네임스페이스 dict.

## H

### hasattr

- **Signature**: `hasattr(object, name, /)`
- **What**: 속성 존재 여부.

### hash

- **Signature**: `hash(object, /)`
- **What**: 해시 값.

### help

- **Signature**: `help([object])`
- **What**: 도움말 출력.

### hex

- **Signature**: `hex(integer, /)`
- **What**: 정수를 `0x...` 16진 문자열로 변환.

## I

### id

- **Signature**: `id(object, /)`
- **What**: 객체의 “식별자”(구현 의존).

### input

- **Signature**: `input([prompt])`
- **What**: 표준 입력에서 한 줄을 문자열로 받음.

### int

- **Signature**: `int(...)`
- **What**: 정수 타입 변환/생성.

### isinstance

- **Signature**: `isinstance(object, classinfo, /)`
- **What**: 타입/상속 관계 포함 검사.

### issubclass

- **Signature**: `issubclass(class, classinfo, /)`
- **What**: 서브클래스 관계 검사.

### iter

- **Signature**: `iter(object[, sentinel])`
- **What**: 이터레이터 생성(센티넬 변형은 고급 패턴).

## L

### len

- **Signature**: `len(s, /)`
- **What**: 길이 반환.

### list

- **Signature**: `list([iterable])`
- **What**: 리스트 타입.

### locals

- **Signature**: `locals()`
- **What**: 로컬 네임스페이스 매핑(동작은 상황 의존).

## M

### map

- **Signature**: `map(function, iterable, /, *iterables)`
- **What**: 함수 적용 결과를 생성하는 이터레이터.

### max

- **Signature**: `max(iterable, /, *, default=..., key=None)` / `max(arg1, arg2, /, *args, key=None)`
- **What**: 최댓값.

### memoryview

- **Signature**: `memoryview(object, /)`
- **What**: 버퍼 프로토콜 기반 뷰.

### min

- **Signature**: `min(iterable, /, *, default=..., key=None)` / `min(arg1, arg2, /, *args, key=None)`
- **What**: 최솟값.

## N

### next

- **Signature**: `next(iterator[, default])`
- **What**: 다음 값 또는 default(없으면 `StopIteration`).

## O

### object

- **Signature**: `object()`
- **What**: 모든 클래스의 최상위 베이스.

### oct

- **Signature**: `oct(integer, /)`
- **What**: 정수를 `0o...` 8진 문자열로 변환.

### open

- **Signature**: `open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)`
- **What**: 파일 열기.
- **Gotchas**: 텍스트는 `encoding='utf-8'` 명시 습관 추천.

### ord

- **Signature**: `ord(c, /)`
- **What**: 1글자 문자열 → 유니코드 코드포인트 정수.

## P

### pow

- **Signature**: `pow(base, exp, mod=None)`
- **What**: 거듭제곱(모듈러 포함 가능).

### print

- **Signature**: `print(*objects, sep=' ', end='\\n', file=None, flush=False)`
- **What**: 출력.

### property

- **Signature**: `property(fget=None, fset=None, fdel=None, doc=None)`
- **What**: 프로퍼티 디스크립터.

## R

### range

- **Signature**: `range(stop)` / `range(start, stop[, step])`
- **What**: 정수 시퀀스(지연).

### repr

- **Signature**: `repr(object, /)`
- **What**: 개발자용 표현 문자열.

### reversed

- **Signature**: `reversed(seq, /)`
- **What**: 역순 이터레이터.

### round

- **Signature**: `round(number[, ndigits])`
- **What**: 반올림.

## S

### set

- **Signature**: `set([iterable])`
- **What**: 집합 타입.

### setattr

- **Signature**: `setattr(object, name, value, /)`
- **What**: 동적으로 속성 설정.

### slice

- **Signature**: `slice(stop)` / `slice(start, stop[, step])`
- **What**: 슬라이스 객체.

### sorted

- **Signature**: `sorted(iterable, /, *, key=None, reverse=False)`
- **What**: 정렬된 새 리스트 반환.

### staticmethod

- **Signature**: `staticmethod(function, /)`
- **What**: static method 디스크립터.

### str

- **Signature**: `str(object='')`
- **What**: 문자열 타입.

### sum

- **Signature**: `sum(iterable, /, start=0)`
- **What**: 합계.

### super

- **Signature**: `super([type[, object-or-type]])`
- **What**: 상속에서 부모 접근.

## T

### tuple

- **Signature**: `tuple([iterable])`
- **What**: 튜플 타입.

### type

- **Signature**: `type(object)` / `type(name, bases, dict, /, **kwargs)`
- **What**: 타입 조회 또는 동적 타입 생성.

## V

### vars

- **Signature**: `vars([object])`
- **What**: `__dict__`를 반환(없으면 `TypeError`).

## Z

### zip

- **Signature**: `zip(*iterables, strict=False)`
- **What**: 병렬 반복을 위한 튜플 이터레이터.
- **Version**: `strict` Added in 3.10.
- **Gotchas**: 길이 불일치가 버그라면 `strict=True`로 조기 실패.

## _

### __import__

- **Signature**: `__import__(name, globals=None, locals=None, fromlist=(), level=0)`
- **What**: import 시스템의 고급 훅. 일상적인 사용은 보통 불필요.
- **Gotchas**: 직접 사용보단 일반 `import` 또는 `importlib` 접근을 우선 고려.

---

## 참고(공식 문서)

- [Built-in Functions](https://docs.python.org/3/library/functions.html)
