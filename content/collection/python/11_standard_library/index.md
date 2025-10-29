---
draft: true
title: "11. 표준 라이브러리"
description: "파이썬의 강력한 내장 모듈들을 활용하여 효율적인 프로그래밍을 합니다"
collection_order: 11
---

# 11. 표준 라이브러리

파이썬의 표준 라이브러리는 "배터리 포함(batteries included)" 철학에 따라 다양한 기능을 제공합니다.

## 학습 목표

이 챕터를 완료하면 다음을 할 수 있습니다:

- **os, sys** 모듈로 시스템 작업 수행
- **datetime, time** 모듈로 날짜와 시간 처리
- **collections** 모듈의 특수 자료구조 활용
- **itertools** 모듈로 반복자 도구 사용
- **functools** 모듈로 함수형 프로그래밍 적용

## 핵심 내용

### 시스템 관련 모듈

**os 모듈 - 운영체제 인터페이스**

```python
import os
from pathlib import Path

# 현재 작업 디렉토리
print(f"Current directory: {os.getcwd()}")

# 디렉토리 목록
for item in os.listdir('.'):
    print(f"  {item}")

# 경로 조작
path = os.path.join('folder', 'subfolder', 'file.txt')
print(f"Joined path: {path}")

# 파일/디렉토리 작업
if not os.path.exists('test_dir'):
    os.makedirs('test_dir')
    print("Directory created")

# pathlib 모듈 (Python 3.4+)
current_path = Path('.')
print(f"Current path: {current_path.absolute()}")
```

### 날짜와 시간

**datetime 모듈**

```python
from datetime import datetime, date, timedelta

# 현재 날짜와 시간
now = datetime.now()
print(f"Current datetime: {now}")

# 날짜 포매팅
print(f"Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 날짜 계산
tomorrow = now + timedelta(days=1)
print(f"Tomorrow: {tomorrow.date()}")
```

### 특수 자료구조 (collections)

```python
from collections import defaultdict, Counter, deque

# defaultdict - 기본값이 있는 딕셔너리
dd = defaultdict(list)
dd['fruits'].append('apple')
print(f"Default dict: {dict(dd)}")

# Counter - 개수 세기
text = "hello world"
counter = Counter(text)
print(f"Character count: {counter}")

# deque - 양방향 큐
dq = deque(['a', 'b', 'c'])
dq.appendleft('z')
print(f"Deque: {dq}")
```

## 실습 프로젝트

### 프로젝트 1: 파일 시스템 분석기

```python
import os
from pathlib import Path
from collections import Counter
from datetime import datetime

class FileSystemAnalyzer:
    def __init__(self, root_path='.'):
        self.root_path = Path(root_path).resolve()
        self.stats = {
            'total_files': 0,
            'total_directories': 0,
            'file_types': Counter()
        }
    
    def analyze(self):
        """파일 시스템 분석 실행"""
        print(f"Analyzing: {self.root_path}")
        
        for item in self.root_path.rglob('*'):
            if item.is_file():
                self.stats['total_files'] += 1
                ext = item.suffix.lower()
                self.stats['file_types'][ext or 'no extension'] += 1
            elif item.is_dir():
                self.stats['total_directories'] += 1
        
        self._display_results()
    
    def _display_results(self):
        """결과 출력"""
        print(f"\n📊 Analysis Results")
        print(f"📁 Total Directories: {self.stats['total_directories']:,}")
        print(f"📄 Total Files: {self.stats['total_files']:,}")
        
        print(f"\n📋 File Types:")
        for ext, count in self.stats['file_types'].most_common(10):
            print(f"  {ext:15} {count:6,} files")

# 사용 예제
if __name__ == "__main__":
    analyzer = FileSystemAnalyzer('.')
    analyzer.analyze()
```

## 체크리스트

### 시스템 모듈
- [ ] os 모듈로 파일/디렉토리 작업
- [ ] sys 모듈로 시스템 정보 접근
- [ ] pathlib로 경로 조작
- [ ] 환경 변수 활용

### 날짜/시간 처리
- [ ] datetime 모듈 완전 활용
- [ ] 날짜 포매팅과 파싱
- [ ] 시간 계산과 차이
- [ ] 성능 측정

### 특수 자료구조
- [ ] collections 모듈의 다양한 구조
- [ ] 적절한 자료구조 선택
- [ ] 성능과 메모리 효율성 고려
- [ ] 실무에서의 활용 패턴

### 고급 도구
- [ ] itertools로 효율적인 반복
- [ ] functools로 함수형 프로그래밍
- [ ] 메모이제이션과 캐싱
- [ ] 데코레이터 고급 활용

## 다음 단계

🎉 **축하합니다!** 파이썬 표준 라이브러리를 마스터했습니다.

이제 [12. 정규표현식](../12_regex/)로 넘어가서 텍스트 처리의 강력한 도구를 학습해봅시다.

---

💡 **팁:**
- 표준 라이브러리를 먼저 확인한 후 외부 라이브러리를 고려하세요
- 성능이 중요한 작업에는 collections와 itertools를 활용하세요
- 날짜와 시간 처리 시 시간대(timezone)를 항상 고려하세요 