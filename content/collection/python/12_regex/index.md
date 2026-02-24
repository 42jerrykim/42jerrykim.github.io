---
draft: true
title: "12. 정규표현식"
description: "정규표현식의 문법과 동작 원리를 배우고, 실제 텍스트 처리에서 언제 regex를 쓰고 피해야 하는지 판단 기준을 제공합니다. 성능·가독성·디버깅 팁도 함께 다룹니다."
tags:
  - Python
  - 파이썬
  - Implementation
  - Software-Architecture
  - Algorithm
  - 알고리즘
  - backend
  - 백엔드
  - Best-Practices
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
  - Performance
  - 성능
  - concurrency
  - 동시성
  - async
  - 비동기
  - oop
  - 객체지향
  - Data-Structures
  - 자료구조
  - DevOps
  - deployment
  - 배포
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - web
  - 웹
  - database
  - 데이터베이스
  - networking
  - 네트워킹
  - CI-CD
  - 자동화
  - Documentation
  - 문서화
  - Git
  - Code-Quality
  - 코드품질
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

### 정규표현식 기본

**기본 메타문자**

```python
import re

# . : 임의의 한 문자
pattern = r'c.t'
text = "cat cut cot"
matches = re.findall(pattern, text)
print(f"Pattern {pattern}: {matches}")  # ['cat', 'cut', 'cot']

# * : 0회 이상 반복
pattern = r'go*d'
text = "gd god good"
matches = re.findall(pattern, text)
print(f"Pattern {pattern}: {matches}")  # ['gd', 'god', 'good']

# + : 1회 이상 반복
pattern = r'go+d'
text = "gd god good"
matches = re.findall(pattern, text)
print(f"Pattern {pattern}: {matches}")  # ['god', 'good']

# ? : 0회 또는 1회
pattern = r'colou?r'
text = "color colour"
matches = re.findall(pattern, text)
print(f"Pattern {pattern}: {matches}")  # ['color', 'colour']
```

**문자 클래스**

```python
# [] : 문자 집합
pattern = r'[aeiou]'
text = "Hello World"
matches = re.findall(pattern, text)
print(f"Vowels: {matches}")  # ['e', 'o', 'o']

# \d : 숫자
pattern = r'\d+'
text = "I have 3 apples and 10 oranges"
matches = re.findall(pattern, text)
print(f"Numbers: {matches}")  # ['3', '10']

# \w : 단어 문자
pattern = r'\w+'
text = "hello_world 123"
matches = re.findall(pattern, text)
print(f"Words: {matches}")  # ['hello_world', '123']
```

### re 모듈 함수들

```python
import re

text = "Python is awesome. Python is powerful."

# re.search() - 첫 번째 매치 찾기
match = re.search(r'Python', text)
if match:
    print(f"Found: {match.group()}")

# re.findall() - 모든 매치 리스트로 반환
matches = re.findall(r'Python', text)
print(f"All matches: {matches}")

# re.sub() - 치환
new_text = re.sub(r'Python', 'Java', text)
print(f"Substituted: {new_text}")

# re.split() - 분할
text2 = "apple,banana;orange"
parts = re.split(r'[,;]', text2)
print(f"Split: {parts}")  # ['apple', 'banana', 'orange']
```

### 그룹화와 캡처링

```python
# () : 그룹화
text = "John: 25, Jane: 30"
pattern = r'(\w+): (\d+)'

matches = re.findall(pattern, text)
for name, age in matches:
    print(f"{name} is {age} years old")

# 명명된 그룹
pattern = r'(?P<name>\w+): (?P<age>\d+)'
for match in re.finditer(pattern, text):
    print(f"Name: {match.group('name')}, Age: {match.group('age')}")
```

## 실습 프로젝트

### 프로젝트 1: 이메일 검증기

```python
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def extract_emails(text):
    pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    return re.findall(pattern, text)

# 테스트
emails = [
    "user@example.com",
    "test.email+tag@domain.co.uk",
    "invalid.email",
    "user@domain.",
]

print("이메일 검증 결과:")
for email in emails:
    print(f"{email:25} {'✓' if validate_email(email) else '✗'}")

# 텍스트에서 이메일 추출
text = """
연락처: john@example.com, jane@test.org
관리자: admin@company.com
"""

found_emails = extract_emails(text)
print(f"\n추출된 이메일: {found_emails}")
```

### 프로젝트 2: 로그 분석기

```python
import re
from collections import Counter

class SimpleLogAnalyzer:
    def __init__(self):
        # Apache 로그 패턴
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
        print(f"📊 로그 분석 결과")
        print(f"총 요청 수: {results['total_requests']}")
        
        print(f"\n상위 IP 주소:")
        for ip, count in results['ips'].most_common(3):
            print(f"  {ip}: {count}회")
        
        print(f"\n상태 코드:")
        for status, count in results['status_codes'].most_common():
            print(f"  {status}: {count}회")

# 샘플 로그 데이터
sample_log = """
192.168.1.1 - - [10/Oct/2024:13:55:36 +0000] "GET /index.html" 200 2326
192.168.1.2 - - [10/Oct/2024:13:55:37 +0000] "POST /api/users" 201 1024
192.168.1.1 - - [10/Oct/2024:13:55:38 +0000] "GET /about.html" 404 512
"""

analyzer = SimpleLogAnalyzer()
results = analyzer.analyze_log(sample_log)
analyzer.display_results(results)
```

## 체크리스트

### 기본 패턴
- [ ] 메타문자와 문자 클래스 이해
- [ ] 수량자 활용 (*, +, ?, {n,m})
- [ ] 앵커 사용 (^, $)
- [ ] 이스케이프 문자 처리

### re 모듈 함수
- [ ] search, match, findall 차이점 이해
- [ ] sub, split 함수 활용
- [ ] 컴파일된 패턴 사용
- [ ] 플래그 옵션 활용

### 고급 기법
- [ ] 그룹화와 캡처링
- [ ] 명명된 그룹 사용
- [ ] 전방/후방 탐색 이해
- [ ] 비캡처링 그룹 활용

### 실무 활용
- [ ] 데이터 검증 패턴
- [ ] 텍스트 추출과 파싱
- [ ] 로그 분석
- [ ] 데이터 정제

## 다음 단계

🎉 **축하합니다!** 파이썬 정규표현식을 마스터했습니다.

이제 [13. 데코레이터](../13_decorators/)로 넘어가서 함수와 클래스를 강화하는 고급 기법을 학습해봅시다.

---

💡 **팁:**
- 복잡한 패턴은 단계별로 구성하고 테스트하세요
- re.VERBOSE 플래그로 패턴에 주석을 추가할 수 있습니다
- 성능이 중요한 경우 패턴을 컴파일해서 재사용하세요
- 정규표현식 테스트 도구를 활용하여 패턴을 검증하세요 
