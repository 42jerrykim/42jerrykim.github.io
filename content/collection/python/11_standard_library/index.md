---
draft: true
title: "11. 표준 라이브러리"
description: "표준 라이브러리의 핵심 모듈(os/pathlib, datetime, collections, itertools 등)을 실무 관점으로 소개합니다. 외부 라이브러리 전에 표준 도구로 문제를 푸는 감각을 기릅니다."
tags:
  - python
  - Python
  - 파이썬
  - programming
  - 프로그래밍
  - software-engineering
  - 소프트웨어공학
  - computer-science
  - 컴퓨터과학
  - backend
  - 백엔드
  - development
  - 개발
  - best-practices
  - 베스트프랙티스
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
  - performance
  - 성능
  - concurrency
  - 동시성
  - async
  - 비동기
  - oop
  - 객체지향
  - data-structures
  - 자료구조
  - algorithms
  - 알고리즘
  - standard-library
  - 표준라이브러리
  - packaging
  - 패키징
  - deployment
  - 배포
  - architecture
  - 아키텍처
  - design-patterns
  - 디자인패턴
  - web
  - 웹
  - database
  - 데이터베이스
  - networking
  - 네트워킹
  - ci-cd
  - 자동화
  - documentation
  - 문서화
  - git
  - 버전관리
  - tooling
  - 개발도구
  - code-quality
  - 코드품질
lastmod: 2026-01-17
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

## 핵심 개념(이론)

### 1) 표준 라이브러리의 역할과 경계
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
- 표준 라이브러리는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

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
