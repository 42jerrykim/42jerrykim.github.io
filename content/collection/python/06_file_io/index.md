---
draft: true
title: "06. 파일 입출력"
description: "파일 읽기/쓰기, 경로 처리, 인코딩, 다양한 포맷(JSON/CSV 등) 기본을 다룹니다. 예외 처리와 컨텍스트 매니저를 통해 안전하게 I/O를 처리하는 습관을 만듭니다."
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
collection_order: 6
---
# 챕터 6: 파일 입출력

> "데이터는 프로그램의 연료다" - 파일을 통해 데이터를 영구적으로 저장하고 불러오는 방법을 마스터해봅시다.

## 학습 목표
- 파일을 안전하게 열고 닫을 수 있다
- 다양한 모드로 파일을 읽고 쓸 수 있다
- 파일 경로와 디렉토리를 효과적으로 다룰 수 있다
- 다양한 파일 형식을 처리할 수 있다

## 핵심 개념(이론)

### 1) 파일 입출력의 역할과 경계
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
- 파일 입출력는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

## 기본 파일 연산

### 파일 열기와 닫기

**기본 파일 열기:**

```python
# 기본적인 파일 열기 (권장하지 않는 방법)
file = open('example.txt', 'r', encoding='utf-8')
content = file.read()
file.close()  # 반드시 닫아야 함!

print(content)
```

**문제점과 개선된 방법:**

```python
# 예외 발생 시에도 안전한 파일 처리
file = None
try:
    file = open('example.txt', 'r', encoding='utf-8')
    content = file.read()
    print(content)
except FileNotFoundError:
    print("파일을 찾을 수 없습니다.")
except IOError:
    print("파일을 읽는 중 오류가 발생했습니다.")
finally:
    if file:
        file.close()
```

### with 문을 사용한 안전한 파일 처리

```python
# with 문 (컨텍스트 매니저) - 권장 방법
with open('example.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)
# 자동으로 파일이 닫힘

# 여러 파일 동시 처리
with open('input.txt', 'r', encoding='utf-8') as infile, \
     open('output.txt', 'w', encoding='utf-8') as outfile:
    data = infile.read()
    processed_data = data.upper()  # 대문자로 변환
    outfile.write(processed_data)
```

### 파일 모드

```python
# 텍스트 모드
# 'r' - 읽기 (기본값)
# 'w' - 쓰기 (파일 내용 덮어쓰기)
# 'a' - 추가 (파일 끝에 내용 추가)
# 'x' - 배타적 생성 (파일이 이미 존재하면 에러)

# 읽기 모드
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# 쓰기 모드 (기존 내용 삭제)
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("새로운 내용")

# 추가 모드 (기존 내용 유지)
with open('log.txt', 'a', encoding='utf-8') as f:
    f.write("로그 메시지\n")

# 바이너리 모드
# 'rb', 'wb', 'ab' - 바이너리 읽기/쓰기/추가

with open('image.jpg', 'rb') as f:
    binary_data = f.read()

with open('copy.jpg', 'wb') as f:
    f.write(binary_data)
``` 
