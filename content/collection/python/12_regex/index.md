---
draft: false
image: "wordcloud.png"
title: "[Python Master] 12. 정규표현식 - re 모듈/패턴 매칭/성능"
slug: "python-regex-re-module-pattern-matching-performance-guide"
description: "정규표현식의 문법과 동작 원리를 배우고, 실제 텍스트 처리에서 언제 regex를 쓰고 피해야 하는지 판단 기준을 제공합니다. 성능·가독성·디버깅 팁도 함께 다룹니다."
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
collection_order: 12
---
# 12. 정규표현식

정규표현식(Regular Expression)은 텍스트 패턴을 정의하고 검색, 치환하는 강력한 도구입니다.

## 학습 목표

이 챕터를 완료하면 다음을 할 수 있습니다:

- **기본 패턴**과 **메타문자** 이해
- **re 모듈**의 다양한 함수 활용
- **그룹화**와 **캡처링** 기법 사용
- **고급 패턴**으로 복잡한 텍스트 처리
- **실무 예제**로 데이터 검증과 추출

## 핵심 개념(이론)

### 1) 정규 표현식의 역할과 경계
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
- 정규 표현식는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 핵심 내용

### 정규표현식 엔진은 어떻게 매칭하는가

Python의 `re` 모듈은 **백트래킹(backtracking) 기반 NFA(Nondeterministic Finite Automaton) 엔진**이다. 문자열을 앞에서부터 한 글자씩 읽으며 패턴의 각 요소를 시도하고, 어느 지점에서 매칭이 막히면 직전 분기점으로 되돌아가 다른 선택지를 다시 시도한다. 이 되돌아가기(backtrack) 과정이 반복되기 때문에, 정규식은 "패턴을 컴파일해서 한 번에 답을 찾는" 결정적 알고리즘이 아니라 **가능한 경로를 순차 탐색하는 탐색 알고리즘**에 가깝다. Perl 계열 정규식(Python 포함)은 순수 정규 언어(regular language)를 넘어서는 기능—역참조(backreference), 전방/후방 탐색—까지 지원하기 때문에 표현력은 크지만, 그 대가로 특정 패턴에서 지수적으로 느려질 수 있다. 이 특성은 뒤의 "흔한 오해와 성능 함정"에서 실측치와 함께 다시 다룬다.

이 엔진 모델을 알고 있으면 두 가지가 자연스럽게 이해된다. 첫째, 왜 `*`나 `+`가 기본적으로 **탐욕적(greedy)**으로 동작하는지—엔진은 일단 최대한 많이 먹고 보되, 이후 매칭이 실패하면 하나씩 반환(backtrack)하며 재시도한다. 둘째, 왜 중첩된 반복 패턴이 위험한지—`(a+)+`처럼 반복 안에 반복이 있으면 같은 문자열을 나누는 방법의 수가 조합적으로 폭발하고, 엔진은 실패를 확인하기 위해 그 모든 조합을 백트래킹으로 훑는다.

### 메타문자와 수량자

정규식 패턴은 리터럴 문자와 **메타문자(metacharacter)**의 조합이다. 메타문자는 "다음에 오는 문자를 몇 번, 어떤 범위에서 매칭할지"를 지시하는 특수 기호로, 이 표를 외우기보다는 "하나의 문자를 어떻게 지정할지(`.`, `[...]`, `\d`)"와 "그 문자를 몇 번 반복할지(`*`, `+`, `?`, `{m,n}`)"라는 두 축으로 나눠 이해하는 편이 기억에 오래 남는다.

| 메타문자 | 의미 | 예시 |
|---|---|---|
| `.` | 개행 문자를 제외한 임의의 한 문자 | `c.t` → cat, cut, cot |
| `*` | 앞 요소 0회 이상 반복(탐욕적) | `go*d` → gd, god, good |
| `+` | 앞 요소 1회 이상 반복(탐욕적) | `go+d` → god, good |
| `?` | 앞 요소 0회 또는 1회 | `colou?r` → color, colour |
| `{m,n}` | 앞 요소 m회 이상 n회 이하 반복 | `\d{2,4}` → 12, 123, 1234 |
| `[...]` | 대괄호 안 문자 집합 중 하나 | `[aeiou]` → 모음 하나 |
| `\d`, `\w`, `\s` | 숫자, 단어 문자, 공백(각각 부정형 `\D`, `\W`, `\S`) | `\d+` → 연속된 숫자 |
| `^`, `$` | 문자열(또는 라인)의 시작, 끝 | `^\d+$` → 숫자로만 구성 |

다음 예제는 위 메타문자들이 실제 문자열에서 어떻게 매칭 범위를 결정하는지 보여준다. `\d{2,4}`처럼 수량자에 범위를 지정하면, 엔진은 가능한 한 긴 쪽(4자리)부터 시도하고 실패하면 짧은 쪽으로 줄여간다는 점에 주의한다.

```python
import re

pattern = r'c.t'
text = "cat cut cot cnt"
print(re.findall(pattern, text))  # ['cat', 'cut', 'cot', 'cnt']

pattern = r'go*d'
text = "gd god good gooood"
print(re.findall(pattern, text))  # ['gd', 'god', 'good', 'gooood']

pattern = r'[aeiou]'
text = "Hello World"
print(re.findall(pattern, text))  # ['e', 'o', 'o']

pattern = r'\d{2,4}'
text = "1 12 123 1234 12345"
print(re.findall(pattern, text))  # ['12', '123', '1234', '1234']
```

마지막 결과 `'12345'`가 `'1234'`와 `'5'`로 잘리는 것은 버그가 아니라 `{2,4}`가 "최대 4자리까지" 소비하기 때문이다. 문자 클래스와 수량자를 결합할 때는 항상 "이 패턴이 실제로 몇 글자까지 먹을 수 있는가"를 먼저 계산해 보는 습관이 필요하다.

### match, search, findall, finditer의 차이

`re` 모듈은 매칭 결과를 얻는 함수를 네 가지 제공하는데, 이름이 비슷해 보여도 **탐색 위치와 반환 형태**가 서로 다르다. `re.match()`는 문자열의 **맨 앞**에서만 매칭을 시도하고 실패하면 즉시 `None`을 반환한다—중간에 패턴이 있어도 찾지 않는다. `re.search()`는 문자열 전체를 스캔하며 **첫 번째로 매칭되는 지점**을 찾는다. `re.findall()`은 매칭된 문자열(또는 그룹)을 전부 **리스트**로 모아 반환하므로 결과가 많으면 메모리를 그만큼 사용한다. `re.finditer()`는 매칭될 때마다 `Match` 객체를 하나씩 만들어내는 **제너레이터(iterator)**를 반환하므로, 매칭 위치(`start()`, `end()`)까지 필요하거나 결과가 매우 많을 때 메모리 효율이 좋다.

```python
import re

text = "cat scatter concatenate"

print(re.match(r'cat', text))     # <Match: span=(0, 3), match='cat'> — 맨 앞이라 성공
print(re.search(r'cat', text))    # <Match: span=(0, 3), match='cat'> — 첫 매치 지점
print(re.findall(r'cat', text))   # ['cat', 'cat', 'cat'] — 세 곳 모두 문자열로

for m in re.finditer(r'cat', text):
    print(m.start(), m.end(), m.group())
# 0 3 cat
# 5 8 cat
# 15 18 cat
```

`re.match(r'scatter', text)`는 `text`가 `"scatter"`로 시작하지 않으므로 항상 `None`이다—문자열 전체에서 `"scatter"`를 찾고 싶다면 `re.search()`를 써야 한다. 이 차이를 혼동해 `match()`로 "포함 여부"를 검사하려다 실패하는 것은 초심자가 가장 자주 겪는 실수 중 하나다.

### 치환: sub와 subn

`re.sub(pattern, repl, text)`는 패턴에 매칭된 부분을 `repl`로 바꾼 새 문자열을 반환한다. `repl`에는 단순 문자열뿐 아니라 **그룹 역참조**(`\1`, `\g<name>`)나 **함수**를 넘길 수 있어, 매칭된 내용에 따라 다른 치환을 적용하는 것도 가능하다. `re.subn()`은 `sub()`와 동일하게 동작하되 `(치환된 문자열, 치환 횟수)` 튜플을 반환하므로, 몇 건이 바뀌었는지 로그로 남기거나 검증할 때 유용하다.

```python
import re

# 그룹 역참조로 날짜 형식 변경: YYYY-MM-DD -> DD/MM/YYYY
text = "2024-01-15"
print(re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', text))  # 15/01/2024

# repl에 함수를 넘겨 매칭마다 다른 처리
def upper_match(m):
    return m.group().upper()

print(re.sub(r'\w+', upper_match, "hello world"))  # HELLO WORLD

# subn으로 치환 횟수까지 확인
result, count = re.subn(r'o', '0', "foo bar boo")
print(result, count)  # f00 bar b00 4
```

`repl`을 함수로 넘기는 방식은 단순 문자열 치환으로는 표현할 수 없는 로직—예를 들어 매칭된 숫자를 세 자리마다 콤마로 묶거나, 매칭 위치에 따라 다른 값을 넣는 등—을 처리할 때 특히 유용하다.

### 그룹화: 캡처, 비캡처, 이름 있는 그룹

괄호 `()`는 패턴의 일부를 하나의 단위로 묶는 **그룹화**의 기본 도구이며, 동시에 그 부분 문자열을 별도로 꺼낼 수 있게 **캡처**한다. `findall()`이 그룹이 있는 패턴에서 튜플의 리스트를 반환하는 이유도 각 그룹의 매칭 결과를 따로 담기 때문이다. 그런데 그룹화는 필요하지만 캡처는 필요 없는 경우—예를 들어 `(?:Mr|Ms|Dr)`처럼 단순히 선택지를 묶기만 할 때—가 있다. 이때 `(?:...)`로 **비캡처 그룹(non-capturing group)**을 쓰면 그룹 번호를 소비하지 않고 결과에도 포함되지 않아, 뒤에 이어지는 캡처 그룹의 번호가 밀리지 않는다. 그룹이 많아질수록 번호(`\1`, `\2`, ...)만으로는 어떤 그룹이 무엇을 의미하는지 알기 어려워지는데, `(?P<name>...)`로 **이름 있는 그룹(named group)**을 쓰면 `match.group('name')`처럼 의미가 드러나는 이름으로 접근할 수 있어 패턴이 길어져도 가독성이 유지된다.

```python
import re

# () : 캡처 그룹
text = "John: 25, Jane: 30"
for name, age in re.findall(r'(\w+): (\d+)', text):
    print(f"{name} is {age} years old")

# (?:...) : 비캡처 그룹 — Mr/Ms/Dr 선택지는 묶되 결과에는 포함하지 않음
print(re.findall(r'(?:Mr|Ms|Dr)\. (\w+)', "Dr. Smith and Ms. Jones"))
# ['Smith', 'Jones']

# (?P<name>...) : 이름 있는 그룹
pattern = r'(?P<name>\w+): (?P<age>\d+)'
for m in re.finditer(pattern, text):
    print(m.group('name'), m.group('age'))
```

이름 있는 그룹은 뒤에서 다룰 로그 분석기처럼 필드가 5개, 10개로 늘어나는 실전 패턴에서 특히 진가를 발휘한다.

### 전방탐색과 후방탐색(lookahead/lookbehind)

전방탐색(lookahead, `(?=...)`/`(?!...)`)과 후방탐색(lookbehind, `(?<=...)`/`(?<!...)`)은 **너비가 0인(zero-width) 어서션**이다. 즉 특정 위치의 앞뒤에 어떤 패턴이 있는지 "확인만" 하고, 그 부분 자체는 매칭 결과에 포함하지 않는다(그룹과 달리 문자를 소비하지 않는다). `(?=...)`는 뒤에 해당 패턴이 와야 함을, `(?!...)`는 뒤에 오면 안 됨을, `(?<=...)`는 앞에 해당 패턴이 있어야 함을, `(?<!...)`는 앞에 있으면 안 됨을 의미한다. 비밀번호처럼 "여러 조건을 모두 만족해야 하지만 각 조건이 문자열의 다른 위치에 흩어져 있는" 검증이나, 통화 기호처럼 "구분자는 확인하되 결과에는 포함하지 않는" 추출에 적합하다.

```python
import re

# 전방탐색: 대문자·숫자·특수문자를 각각 포함하고 길이 8자 이상인지 확인
password_pattern = re.compile(
    r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$'
)
for pw in ["abc12345", "Abcdefg1", "Abcdef1!", "Ab1!"]:
    print(pw, bool(password_pattern.match(pw)))
# abc12345 False (대문자·특수문자 없음)
# Abcdefg1 False (특수문자 없음)
# Abcdef1! True
# Ab1!     False (길이 8 미만)

# 후방탐색: $ 뒤의 숫자만 추출(기호 자체는 결과에서 제외)
text = "Price: $100, Cost: 50won, Total: $250"
print(re.findall(r'(?<=\$)\d+', text))   # ['100', '250']
print(re.findall(r'\d+(?=won)', text))   # ['50']
```

각 전방탐색은 같은 위치(문자열의 시작)를 기준으로 독립적으로 검사하므로, `.{8,}$`처럼 실제로 문자를 소비하는 부분은 마지막 조건 하나뿐이다. 이 조합 방식을 이해하면 "조건 여러 개를 AND로 검증"하는 패턴을 스스로 만들 수 있다.

### re.compile로 재사용하기: 성능과 가독성

같은 패턴을 반복해서 매칭할 때는 `re.compile()`로 미리 컴파일한 `Pattern` 객체를 재사용하는 편이 좋다. `re` 모듈은 내부적으로 최근 사용한 패턴 문자열을 작은 캐시에 저장해 두어 `re.findall(r'\d+', s)`처럼 매번 새로 호출해도 파싱 비용이 완전히 반복되지는 않지만, 이 캐시는 크기 제한이 있고 프로세스 전역에서 공유되므로 다른 모듈이 많은 패턴을 쓰면 밀려날 수 있다. 명시적으로 `compile()`한 객체를 변수에 담아 두면 캐시 적중을 언어 차원에서 보장받을 뿐 아니라, "이 패턴은 여러 번 쓰인다"는 의도가 코드에 드러나 가독성도 좋아진다.

```python
import timeit

compiled = re.compile(r'\d+')

def with_compile():
    return compiled.findall("order 12 item 345 qty 6")

def without_compile():
    return re.findall(r'\d+', "order 12 item 345 qty 6")

t1 = timeit.timeit(with_compile, number=20000)
t2 = timeit.timeit(without_compile, number=20000)
print(f"compiled: {t1:.4f}s, uncompiled: {t2:.4f}s")
# compiled: 0.0153s, uncompiled: 0.0208s (환경에 따라 수치는 달라짐, 우열 관계는 유지되는 경향)
```

이 실측치는 실행 환경(CPU, Python 버전)에 따라 달라지지만, 반복 횟수가 많을수록 컴파일 재사용의 이득이 누적된다는 경향은 유지된다. 한두 번만 쓰는 일회성 패턴이라면 `compile()` 여부가 성능에 미치는 영향은 미미하므로, "반복 매칭인가"를 기준으로 판단하면 된다.

### 실전 패턴: 이메일, 전화번호, URL

**이메일 형식 검증**은 실무에서 가장 자주 마주치는 정규식 용도이지만, RFC 5322가 정의하는 이메일 주소의 완전한 문법은 따옴표로 감싼 로컬 파트, 주석, 국제화 도메인 등을 포함해 정규식 한 줄로 담기 어려울 만큼 복잡하다. 그래서 실무에서는 "로컬파트@도메인.최상위도메인" 형태를 근사하는 패턴으로 **입력 형식을 1차로 거르는** 용도로만 쓰고, 실제로 그 주소가 살아 있는지는 확인 메일을 보내 클릭을 유도하는 방식으로 검증하는 것이 일반적이다.

```python
import re

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_email(email):
    return bool(EMAIL_PATTERN.match(email))

emails = ["user@example.com", "test.email+tag@domain.co.uk", "invalid.email", "user@domain."]
for e in emails:
    print(e, validate_email(e))
# user@example.com True
# test.email+tag@domain.co.uk True
# invalid.email False
# user@domain. False

# 텍스트 안에서 이메일 후보를 찾아내는 것은 검증과 다른 문제 — \b로 단어 경계를 잡는다
EMAIL_FIND_PATTERN = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
text = "연락처: john@example.com, jane@test.org 관리자: admin@company.com"
print(EMAIL_FIND_PATTERN.findall(text))
```

**전화번호 추출**은 표기 방식이 하이픈, 공백, 국가 코드 등으로 다양해서 그룹으로 지역번호·국번·번호를 나눠 받은 뒤 정규화하는 접근이 흔히 쓰인다. 아래 패턴은 `010-1234-5678`, `02-123-4567`, `+82 10 9876 5432` 형식을 하나로 처리하지만, `(02) 123-4567`처럼 괄호를 쓰는 표기나 `010.1234.5678`처럼 마침표를 구분자로 쓰는 표기는 잡아내지 못한다. 정규식으로 전화번호를 다룰 때는 "이 패턴이 어떤 표기까지 포괄하는지"를 항상 원본 데이터 샘플로 확인해야 한다—포괄하지 못하는 형식은 조용히 누락되기 때문이다.

```python
PHONE_PATTERN = re.compile(
    r'(?:\+?82[-\s]?)?0?(?P<area>\d{1,2})[-\s]?(?P<prefix>\d{3,4})[-\s]?(?P<line>\d{4})'
)

def normalize_phone(text):
    return [
        f"0{m.group('area')}-{m.group('prefix')}-{m.group('line')}"
        for m in PHONE_PATTERN.finditer(text)
    ]

sample_text = (
    "연락처는 010-1234-5678 이고, 회사 대표번호는 02-123-4567 입니다. "
    "해외에서 걸 때는 +82 10 9876 5432 형식을 씁니다."
)
print(normalize_phone(sample_text))
# ['010-1234-5678', '02-123-4567', '010-9876-5432']
```

**URL 파싱**은 정규식의 역할을 어디까지로 한정할지가 특히 중요한 사례다. URL은 스킴(scheme), 호스트, 경로, 쿼리스트링, 프래그먼트로 구성된 구조화된 문자열이므로, 이 구조를 분해하는 작업은 표준 라이브러리 `urllib.parse.urlparse()`가 이미 RFC 3986 규칙에 맞춰 안전하게 처리해 준다. 정규식은 "텍스트 뭉치에서 URL처럼 보이는 후보를 찾아내는" 검출 단계까지만 담당하고, 찾아낸 문자열의 내부 구조를 분해하는 것은 전용 파서에 맡기는 역할 분담이 실무에서 안정적이다.

```python
from urllib.parse import urlparse

URL_PATTERN = re.compile(r'https?://[^\s<>"\')]+')
text = (
    "공식 문서는 https://docs.python.org/3/library/re.html 를 참고하세요. "
    "백업: http://example.com/a?b=1#frag"
)
urls = URL_PATTERN.findall(text)
print(urls)

for u in urls:
    parsed = urlparse(u)
    print(parsed.scheme, parsed.netloc, parsed.path, parsed.query, parsed.fragment)
# https docs.python.org /3/library/re.html
# http example.com /a b=1 frag
```

### 흔한 오해와 성능 함정

**`.`은 개행 문자를 매칭하지 않는다.** `a.b`는 `"a\nb"`(줄바꿈 포함)에 매칭되지 않으며, 여러 줄에 걸친 텍스트까지 `.`으로 잡고 싶다면 `re.DOTALL` 플래그가 필요하다. **`^`와 `$`는 기본적으로 문자열 전체의 시작·끝만 의미한다.** 여러 줄 문자열에서 각 줄의 시작·끝을 잡으려면 `re.MULTILINE`을 켜야 한다. **`*`/`+`는 기본적으로 탐욕적(greedy)이라 가능한 한 많이 소비한다.** `<.+>`를 `"<a><b>"`에 적용하면 `<a>`가 아니라 `<a><b>` 전체가 매칭되는데, 이는 버그가 아니라 설계다—`<a>`만 원한다면 `<.+?>`처럼 `?`를 붙여 비탐욕적(non-greedy)으로 바꿔야 한다.

```python
text = "line1\nline2\nline3"
print(re.findall(r'^line\d', text))               # ['line1']
print(re.findall(r'^line\d', text, re.MULTILINE)) # ['line1', 'line2', 'line3']

print(re.match(r'a.b', "a\nb"))                    # None
print(re.match(r'a.b', "a\nb", re.DOTALL))          # <Match: match='a\nb'>

greedy = re.search(r'<.+>', "<a><b>")
nongreedy = re.search(r'<.+?>', "<a><b>")
print(greedy.group(), nongreedy.group())            # <a><b>  <a>
```

**중첩된 반복 수량자는 지수적으로 느려질 수 있다.** `(a+)+b`처럼 반복 그룹을 다시 반복하면, 같은 문자열을 여러 그룹으로 나누는 조합의 수가 입력 길이에 따라 폭발적으로 늘어난다. 매칭이 실패해야 확정되는 경우(마지막에 `b`가 없는 경우) 엔진은 그 모든 조합을 백트래킹으로 확인해야 하므로, 아래처럼 문자열 길이를 몇 자만 늘려도 실행 시간이 눈에 띄게 증가한다.

```python
import time

pattern_bad = re.compile(r'(a+)+b')
for n in (15, 18, 20, 22):
    start = time.perf_counter()
    pattern_bad.match('a' * n)  # 'b'가 없으므로 항상 실패
    print(n, f"{time.perf_counter() - start:.4f}s")
# 15 0.0013s
# 18 0.0094s
# 20 0.0372s
# 22 0.1551s   (측정 환경에 따라 절대값은 다르지만 증가 추세는 지수적)
```

이 현상을 **ReDoS(Regular Expression Denial of Service)**라고 부르며, 사용자 입력을 그대로 정규식에 사용하는 서비스에서는 실제 보안 문제로 이어질 수 있다. 반복 그룹을 중첩하지 않도록 패턴을 설계하거나, 신뢰할 수 없는 입력에는 매칭 시간에 제한을 두는 방어가 필요하다.

### 정규식이 적합하지 않은 경우

정규식이 다루는 정규 언어(regular language)는 "중첩"이나 "짝을 맞추는 구조"를 표현하지 못한다는 근본적인 한계가 있다. HTML/XML처럼 태그가 서로 다른 깊이로 중첩되는 구조, 괄호가 짝을 이뤄야 하는 수식, JSON처럼 객체 안에 객체가 들어가는 형식은 문맥 자유 언어(context-free language)에 속하며, 이를 정규식만으로 안전하게 파싱하려는 시도는 태그 개수가 늘어날수록 패턴이 기하급수적으로 복잡해지거나 예외 케이스에서 조용히 틀린다. 이런 구조화된 데이터는 `html.parser`나 `xml.etree.ElementTree`, `json` 모듈처럼 그 형식을 위해 설계된 전용 파서에 맡기는 것이 안전하고, 정규식은 파싱 결과에서 특정 패턴을 다시 검색하는 보조 역할로 쓰는 편이 낫다.

설령 대상이 정규 언어로 표현 가능한 구조라 해도, 전방탐색과 비캡처 그룹을 여러 겹으로 쌓은 한 줄짜리 패턴은 작성자 본인도 몇 주 뒤에는 해독하기 어려운 "쓰기 전용 코드"가 되기 쉽다. `re.VERBOSE` 플래그를 쓰면 패턴 안에 공백과 주석을 넣어 가독성을 크게 높일 수 있으므로, 패턴이 세 줄을 넘어가기 시작하면 적용을 고려할 만하다. 그래도 여전히 복잡하다면, "정규식 한 줄"이라는 목표 자체를 내려놓고 여러 개의 작은 패턴이나 일반 문자열 메서드(`str.split()`, `str.startswith()`)로 나눠 처리하는 편이 유지보수 측면에서 낫다. 정규식 문법과 플래그의 전체 목록은 [Python 공식 `re` 모듈 문서](https://docs.python.org/3/library/re.html)를, 단계별 튜토리얼은 [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html)를 1차 출처로 참고할 수 있다.

## 실습 프로젝트

### 웹 서버 로그 분석기

지금까지 다룬 `re.compile()`에 의한 재사용, 이름 있는 그룹, `finditer` 계열의 반복 매칭을 하나로 묶으면 실전 규모의 텍스트 처리 도구를 만들 수 있다. 아래 로그 분석기는 Apache 접근 로그 한 줄에서 IP·시각·HTTP 메서드·URL·상태 코드를 이름 있는 그룹으로 한 번에 뽑아내고, `Counter`로 집계한다. 로그 형식이 고정되어 있고 반복적으로 같은 패턴을 수천~수만 줄에 적용한다는 점에서, `compile()`로 미리 컴파일해 두는 이점이 가장 잘 드러나는 사례이기도 하다.

```python
import re
from collections import Counter

class SimpleLogAnalyzer:
    def __init__(self):
        # Apache Combined Log Format의 앞부분을 이름 있는 그룹으로 분해
        self.pattern = re.compile(
            r'(?P<ip>\d+\.\d+\.\d+\.\d+) .* \[(?P<datetime>[^\]]+)\] '
            r'"(?P<method>\w+) (?P<url>[^"]*)" (?P<status>\d+)'
        )

    def analyze_log(self, log_text):
        results = {
            'ips': Counter(),
            'status_codes': Counter(),
            'methods': Counter(),
            'total_requests': 0
        }

        for line in log_text.strip().split('\n'):
            match = self.pattern.search(line)
            if match:
                data = match.groupdict()
                results['ips'][data['ip']] += 1
                results['status_codes'][data['status']] += 1
                results['methods'][data['method']] += 1
                results['total_requests'] += 1

        return results

    def display_results(self, results):
        print(f"총 요청 수: {results['total_requests']}")

        print("상위 IP 주소:")
        for ip, count in results['ips'].most_common(3):
            print(f"  {ip}: {count}회")

        print("상태 코드:")
        for status, count in results['status_codes'].most_common():
            print(f"  {status}: {count}회")

sample_log = """
192.168.1.1 - - [10/Oct/2024:13:55:36 +0000] "GET /index.html" 200 2326
192.168.1.2 - - [10/Oct/2024:13:55:37 +0000] "POST /api/users" 201 1024
192.168.1.1 - - [10/Oct/2024:13:55:38 +0000] "GET /about.html" 404 512
"""

analyzer = SimpleLogAnalyzer()
results = analyzer.analyze_log(sample_log)
analyzer.display_results(results)
```

이 구현은 로그 한 줄이 패턴과 정확히 일치하지 않으면(`search()`가 `None`을 반환하면) 조용히 건너뛴다. 실제 운영 환경에서는 형식이 어긋난 줄이 얼마나 되는지도 함께 집계해 두어야, 정규식이 놓친 데이터가 있다는 사실을 나중에라도 알아챌 수 있다.

## 체크리스트

### 기본 패턴
- [ ] 메타문자와 문자 클래스 이해
- [ ] 수량자 활용 (*, +, ?, {n,m})과 탐욕적/비탐욕적 매칭의 차이
- [ ] 앵커 사용 (^, $)과 MULTILINE 플래그의 관계
- [ ] 이스케이프 문자 처리

### re 모듈 함수
- [ ] match, search, findall, finditer의 탐색 위치·반환 형태 차이 설명
- [ ] sub, subn 함수로 문자열 치환과 치환 횟수 확인
- [ ] compile()로 패턴을 재사용해야 하는 상황 판단
- [ ] DOTALL, MULTILINE, VERBOSE 플래그 활용

### 고급 기법
- [ ] 캡처 그룹, 비캡처 그룹 `(?:...)`, 이름 있는 그룹 `(?P<name>...)` 구분
- [ ] 전방탐색 `(?=...)`/`(?!...)`, 후방탐색 `(?<=...)`/`(?<!...)`으로 너비 0 조건 표현
- [ ] 중첩 반복 패턴이 ReDoS로 이어지는 이유 설명
- [ ] 정규식으로 풀 문제와 전용 파서(html.parser, json, urlparse)로 풀 문제 구분

### 실무 활용
- [ ] 이메일·전화번호 등 형식 검증 패턴 작성과 그 한계 인지
- [ ] 텍스트에서 URL 후보를 찾아내고 urlparse로 구조 분해
- [ ] 이름 있는 그룹을 활용한 로그 분석
- [ ] 매칭 실패(패턴이 놓친 데이터)를 함께 집계하는 방어적 설계

## 다음 단계

파이썬 정규표현식의 매칭 원리, re 모듈 함수, 그룹과 전방/후방 탐색, 컴파일 재사용, 그리고 정규식이 적합하지 않은 경계까지 살펴봤습니다.

이제 [13. 데코레이터](/post/python/python-decorators-closures-caching-logging-pattern-guide/)로 넘어가서 함수와 클래스를 강화하는 고급 기법을 학습해봅시다.

---

💡 **팁:**
- 복잡한 패턴은 `re.VERBOSE`로 주석을 달아가며 단계별로 구성하고 테스트하세요
- 반복적으로 쓰는 패턴은 `re.compile()`로 재사용해 파싱 비용을 줄이세요
- 사용자 입력을 그대로 패턴에 넣기 전에 중첩 반복 구조(ReDoS 위험)가 없는지 점검하세요
- 구조화된 데이터(HTML, JSON, URL)는 정규식 대신 전용 파서를 우선 고려하세요
