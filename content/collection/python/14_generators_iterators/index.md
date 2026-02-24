---
draft: true
title: "14. 제너레이터와 이터레이터"
description: "이터레이터/제너레이터 프로토콜을 이해해 메모리 효율적인 데이터 처리를 설계합니다. lazy evaluation이 유리한 상황과 디버깅/예외 처리 포인트를 함께 정리합니다."
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
collection_order: 14
---
# 14. 제너레이터와 이터레이터

제너레이터와 이터레이터는 메모리 효율적이고 지연 평가(lazy evaluation)를 지원하는 파이썬의 핵심 기능입니다.

## 학습 목표

이 챕터를 완료하면 다음을 할 수 있습니다:

- **이터레이터 프로토콜** 이해와 구현
- **제너레이터 함수**와 **표현식** 활용
- **yield** 키워드의 고급 사용법
- **비동기 제너레이터** 기본 이해
- **대용량 데이터** 효율적 처리

## 핵심 개념(이론)

### 1) 제너레이터와 이터레이터의 역할과 경계
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
- 제너레이터와 이터레이터는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 핵심 내용

### 이터레이터 기본

**이터러블과 이터레이터**

```python
# 리스트는 이터러블
numbers = [1, 2, 3, 4, 5]

# 이터레이터 생성
iterator = iter(numbers)

# 하나씩 값 가져오기
print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3

# for 루프는 내부적으로 이터레이터 사용
for num in numbers:
    print(num)

# 사용자 정의 이터레이터
class CountDown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

# 사용 예제
countdown = CountDown(3)
for num in countdown:
    print(f"카운트다운: {num}")
```

**range의 내부 동작**

```python
class MyRange:
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step
    
    def __iter__(self):
        return MyRangeIterator(self.start, self.stop, self.step)

class MyRangeIterator:
    def __init__(self, start, stop, step):
        self.current = start
        self.stop = stop
        self.step = step
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if (self.step > 0 and self.current >= self.stop) or \
           (self.step < 0 and self.current <= self.stop):
            raise StopIteration
        
        value = self.current
        self.current += self.step
        return value

# 테스트
my_range = MyRange(0, 5)
for i in my_range:
    print(i)  # 0, 1, 2, 3, 4
```

### 제너레이터 함수

**기본 제너레이터**

```python
def simple_generator():
    print("제너레이터 시작")
    yield 1
    print("첫 번째 yield 후")
    yield 2
    print("두 번째 yield 후")
    yield 3
    print("제너레이터 끝")

# 제너레이터 객체 생성
gen = simple_generator()
print(type(gen))  # <class 'generator'>

# 하나씩 값 가져오기
print(next(gen))  # 제너레이터 시작, 1
print(next(gen))  # 첫 번째 yield 후, 2
print(next(gen))  # 두 번째 yield 후, 3

# StopIteration 예외 발생
try:
    print(next(gen))
except StopIteration:
    print("제너레이터 완료")
```

**실용적인 제너레이터들**

```python
def fibonacci(n):
    """피보나치 수열 제너레이터"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# 사용
fib = fibonacci(10)
print(list(fib))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def read_large_file(filename, chunk_size=1024):
    """대용량 파일을 청크 단위로 읽기"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {filename}")
        return

def infinite_sequence():
    """무한 수열 제너레이터"""
    num = 0
    while True:
        yield num
        num += 1

# 처음 10개만 가져오기
infinite = infinite_sequence()
first_ten = [next(infinite) for _ in range(10)]
print(first_ten)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 제너레이터 표현식

```python
# 리스트 컴프리헨션 vs 제너레이터 표현식
numbers = range(1000000)

# 리스트 컴프리헨션 - 메모리에 모든 값 저장
squares_list = [x**2 for x in numbers]

# 제너레이터 표현식 - 지연 평가
squares_gen = (x**2 for x in numbers)

print(type(squares_list))  # <class 'list'>
print(type(squares_gen))   # <class 'generator'>

# 메모리 사용량 비교
import sys
print(f"리스트 크기: {sys.getsizeof(squares_list):,} bytes")
print(f"제너레이터 크기: {sys.getsizeof(squares_gen):,} bytes")

# 제너레이터 표현식 활용
# 조건부 필터링
even_squares = (x**2 for x in range(20) if x % 2 == 0)
print(list(even_squares))  # [0, 4, 16, 36, 64, 100, 144, 196, 256, 324]

# 문자열 처리
text = "Hello World Python"
words = (word.lower() for word in text.split())
print(list(words))  # ['hello', 'world', 'python']
```

### 고급 제너레이터 기법

**yield from**

```python
def inner_generator():
    yield 1
    yield 2
    yield 3

def outer_generator():
    yield 'start'
    yield from inner_generator()  # 다른 제너레이터 위임
    yield 'end'

# 테스트
result = list(outer_generator())
print(result)  # ['start', 1, 2, 3, 'end']

def flatten(nested_list):
    """중첩 리스트 평면화"""
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)  # 재귀적으로 평면화
        else:
            yield item

# 테스트
nested = [1, [2, 3], [4, [5, 6]], 7]
flat = list(flatten(nested))
print(flat)  # [1, 2, 3, 4, 5, 6, 7]
```

**제너레이터와 send()**

```python
def accumulator():
    """값을 받아서 누적하는 제너레이터"""
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value

# 사용 예제
acc = accumulator()
next(acc)  # 제너레이터 시작

print(acc.send(5))    # 5
print(acc.send(10))   # 15
print(acc.send(3))    # 18

def averager():
    """이동 평균 계산 제너레이터"""
    values = []
    while True:
        value = yield
        if value is not None:
            values.append(value)
            average = sum(values) / len(values)
            print(f"현재 평균: {average:.2f}")

# 사용 예제
avg = averager()
next(avg)  # 제너레이터 시작

avg.send(10)  # 현재 평균: 10.00
avg.send(20)  # 현재 평균: 15.00
avg.send(15)  # 현재 평균: 15.00
```

## 실습 프로젝트

### 프로젝트 1: 대용량 데이터 처리 시스템

```python
import csv
import json
from datetime import datetime
from collections import defaultdict

class DataProcessor:
    def __init__(self):
        self.processors = []
    
    def add_processor(self, processor_func):
        """데이터 처리 함수 추가"""
        self.processors.append(processor_func)
    
    def process_file(self, filename, file_type='csv'):
        """파일을 스트리밍 방식으로 처리"""
        if file_type == 'csv':
            yield from self._process_csv(filename)
        elif file_type == 'json':
            yield from self._process_json(filename)
    
    def _process_csv(self, filename):
        """CSV 파일 스트리밍 처리"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row_num, row in enumerate(reader, 1):
                    # 각 행에 대해 등록된 프로세서 적용
                    processed_row = row
                    for processor in self.processors:
                        processed_row = processor(processed_row)
                        if processed_row is None:
                            break  # 필터링된 행
                    
                    if processed_row is not None:
                        yield {
                            'row_number': row_num,
                            'data': processed_row
                        }
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {filename}")
    
    def _process_json(self, filename):
        """JSON Lines 파일 스트리밍 처리"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    try:
                        data = json.loads(line.strip())
                        processed_data = data
                        
                        for processor in self.processors:
                            processed_data = processor(processed_data)
                            if processed_data is None:
                                break
                        
                        if processed_data is not None:
                            yield {
                                'line_number': line_num,
                                'data': processed_data
                            }
                    except json.JSONDecodeError:
                        print(f"라인 {line_num}: JSON 파싱 오류")
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {filename}")

# 데이터 처리 함수들
def clean_numeric_fields(row):
    """숫자 필드 정리"""
    if isinstance(row, dict):
        for key, value in row.items():
            if isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                try:
                    row[key] = float(value) if '.' in value else int(value)
                except ValueError:
                    pass
    return row

def filter_valid_email(row):
    """유효한 이메일이 있는 행만 통과"""
    if isinstance(row, dict) and 'email' in row:
        email = row['email']
        if '@' in email and '.' in email:
            return row
    return None

def add_processing_timestamp(row):
    """처리 시간 추가"""
    if isinstance(row, dict):
        row['processed_at'] = datetime.now().isoformat()
    return row

def create_sample_csv():
    """테스트용 샘플 CSV 파일 생성"""
    import random
    
    data = [
        ['name', 'age', 'email', 'salary'],
        ['김철수', '25', 'kim@example.com', '3500000'],
        ['이영희', '30', 'lee@test.org', '4200000'],
        ['박민수', 'invalid', 'invalid-email', '3800000'],
        ['정수진', '28', 'jung@company.com', '4500000'],
        ['최영호', '35', 'choi@domain.net', '5200000']
    ]
    
    with open('sample_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    print("샘플 CSV 파일 생성 완료: sample_data.csv")

# 테스트 실행
if __name__ == "__main__":
    # 샘플 데이터 생성
    create_sample_csv()
    
    # 데이터 프로세서 설정
    processor = DataProcessor()
    processor.add_processor(clean_numeric_fields)
    processor.add_processor(filter_valid_email)
    processor.add_processor(add_processing_timestamp)
    
    print("대용량 데이터 처리 시작...\n")
    
    # 스트리밍 처리
    processed_count = 0
    for result in processor.process_file('sample_data.csv'):
        processed_count += 1
        print(f"처리된 행 {result['row_number']}: {result['data']}")
    
    print(f"\n총 {processed_count}개 행이 처리되었습니다.")
```

### 프로젝트 2: 실시간 데이터 스트림 분석기

```python
import random
import time
from collections import deque
from datetime import datetime, timedelta

class RealTimeAnalyzer:
    def __init__(self, window_size=100):
        self.window_size = window_size
        self.data_window = deque(maxlen=window_size)
        self.metrics = {}
    
    def data_stream_generator(self, duration_seconds=60):
        """실시간 데이터 스트림 시뮬레이션"""
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            # 센서 데이터 시뮬레이션
            timestamp = datetime.now()
            temperature = random.normalvariate(22, 5)  # 평균 22도, 표준편차 5
            humidity = random.normalvariate(50, 10)    # 평균 50%, 표준편차 10
            pressure = random.normalvariate(1013, 20)  # 평균 1013hPa, 표준편차 20
            
            data_point = {
                'timestamp': timestamp,
                'temperature': temperature,
                'humidity': humidity,
                'pressure': pressure
            }
            
            yield data_point
            time.sleep(0.1)  # 100ms 간격
    
    def calculate_moving_average(self, field):
        """이동 평균 계산 제너레이터"""
        values = [point[field] for point in self.data_window if field in point]
        if values:
            return sum(values) / len(values)
        return 0
    
    def detect_anomalies(self, current_value, field, threshold=2):
        """이상값 탐지 (Z-score 기반)"""
        values = [point[field] for point in self.data_window if field in point]
        if len(values) < 10:  # 최소 10개 데이터 필요
            return False
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return False
        
        z_score = abs((current_value - mean) / std_dev)
        return z_score > threshold
    
    def analyze_stream(self, data_stream):
        """실시간 데이터 분석"""
        for data_point in data_stream:
            # 데이터 윈도우에 추가
            self.data_window.append(data_point)
            
            # 현재 메트릭 계산
            current_metrics = {
                'timestamp': data_point['timestamp'],
                'raw_data': data_point,
                'moving_averages': {
                    'temperature': self.calculate_moving_average('temperature'),
                    'humidity': self.calculate_moving_average('humidity'),
                    'pressure': self.calculate_moving_average('pressure')
                },
                'anomalies': {}
            }
            
            # 이상값 탐지
            for field in ['temperature', 'humidity', 'pressure']:
                is_anomaly = self.detect_anomalies(data_point[field], field)
                current_metrics['anomalies'][field] = is_anomaly
            
            yield current_metrics
    
    def generate_alerts(self, metrics_stream):
        """알림 생성 제너레이터"""
        for metrics in metrics_stream:
            alerts = []
            
            # 온도 알림
            temp = metrics['raw_data']['temperature']
            if temp > 35:
                alerts.append(f"🔥 고온 경고: {temp:.1f}°C")
            elif temp < 5:
                alerts.append(f"🧊 저온 경고: {temp:.1f}°C")
            
            # 습도 알림
            humidity = metrics['raw_data']['humidity']
            if humidity > 80:
                alerts.append(f"💧 고습도 경고: {humidity:.1f}%")
            elif humidity < 20:
                alerts.append(f"🌵 저습도 경고: {humidity:.1f}%")
            
            # 이상값 알림
            anomaly_fields = [field for field, is_anomaly in metrics['anomalies'].items() if is_anomaly]
            if anomaly_fields:
                alerts.append(f"⚠️ 이상값 탐지: {', '.join(anomaly_fields)}")
            
            metrics['alerts'] = alerts
            yield metrics

def create_dashboard_generator(analyzer):
    """대시보드 출력 제너레이터"""
    data_stream = analyzer.data_stream_generator(duration_seconds=30)  # 30초간 실행
    metrics_stream = analyzer.analyze_stream(data_stream)
    alert_stream = analyzer.generate_alerts(metrics_stream)
    
    for i, metrics in enumerate(alert_stream):
        if i % 10 == 0:  # 1초마다 출력 (10개 데이터포인트)
            print(f"\n{'='*60}")
            print(f"실시간 모니터링 - {metrics['timestamp'].strftime('%H:%M:%S')}")
            print(f"{'='*60}")
            
            # 현재 값
            raw = metrics['raw_data']
            print(f"📊 현재 값:")
            print(f"  온도: {raw['temperature']:6.1f}°C")
            print(f"  습도: {raw['humidity']:6.1f}%")
            print(f"  기압: {raw['pressure']:6.1f}hPa")
            
            # 이동 평균
            avg = metrics['moving_averages']
            print(f"\n📈 이동 평균 ({analyzer.window_size}개 데이터):")
            print(f"  온도: {avg['temperature']:6.1f}°C")
            print(f"  습도: {avg['humidity']:6.1f}%")
            print(f"  기압: {avg['pressure']:6.1f}hPa")
            
            # 알림
            if metrics['alerts']:
                print(f"\n🚨 알림:")
                for alert in metrics['alerts']:
                    print(f"  {alert}")
            else:
                print(f"\n✅ 모든 값이 정상 범위입니다.")
        
        yield metrics

# 테스트 실행
if __name__ == "__main__":
    print("실시간 데이터 스트림 분석 시작...\n")
    
    analyzer = RealTimeAnalyzer(window_size=50)
    dashboard = create_dashboard_generator(analyzer)
    
    # 대시보드 실행
    total_points = 0
    alert_count = 0
    
    for metrics in dashboard:
        total_points += 1
        if metrics['alerts']:
            alert_count += 1
    
    print(f"\n{'='*60}")
    print(f"분석 완료")
    print(f"{'='*60}")
    print(f"총 데이터 포인트: {total_points}")
    print(f"알림 발생 횟수: {alert_count}")
    if total_points > 0:
        print(f"알림 비율: {alert_count/total_points*100:.1f}%")
```

## 체크리스트

### 이터레이터 프로토콜
- [ ] __iter__와 __next__ 메서드 구현
- [ ] StopIteration 예외 처리
- [ ] 이터러블과 이터레이터 차이점 이해
- [ ] 내장 함수들과의 연동

### 제너레이터 함수
- [ ] yield 키워드 완전 이해
- [ ] 제너레이터 상태 관리
- [ ] 무한 수열과 지연 평가
- [ ] 메모리 효율성 활용

### 고급 기법
- [ ] yield from 활용
- [ ] send()와 양방향 통신
- [ ] throw()와 close() 메서드
- [ ] 제너레이터 표현식 최적화

### 실무 적용
- [ ] 대용량 파일 처리
- [ ] 스트리밍 데이터 분석
- [ ] 파이프라인 구축
- [ ] 성능 최적화

## 다음 단계

🎉 **축하합니다!** 파이썬 제너레이터와 이터레이터를 마스터했습니다.

이제 [15. 컨텍스트 매니저](../15_context_managers/)로 넘어가서 리소스를 안전하게 관리하는 방법을 학습해봅시다.

---

💡 **팁:**
- 대용량 데이터는 항상 제너레이터로 처리하세요
- 제너레이터는 한 번만 사용 가능하므로 재사용 시 새로 생성하세요
- 메모리 사용량이 중요한 경우 제너레이터 표현식을 우선 고려하세요
- yield from을 사용하여 제너레이터를 깔끔하게 연결하세요 
