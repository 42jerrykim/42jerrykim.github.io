---
draft: true
title: "12. 정규표현식"
description: "정규표현식을 활용하여 강력한 텍스트 처리와 패턴 매칭을 마스터합니다"
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

## 핵심 내용

### 1. 정규표현식 기본

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

### 2. re 모듈 함수들

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

### 3. 그룹화와 캡처링

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