---

image: "wordcloud.png"
title: "[Python Cheatsheet] 37. datetime - timezone/파싱/포맷"
slug: "datetime-timezone-handling-utc-iso-format-parse-guide"
description: "datetime을 안전하게 다루기 위한 치트시트입니다. naive/aware 구분, timezone(UTC) 기본, ISO 파싱/포맷, 타임존 변환, 흔한 버그 포인트(로컬타임/서머타임)를 최소 예제로 정리합니다."
lastmod: 2026-01-17
collection_order: 37
tags:
  - Python
  - 파이썬
  - Cheatsheet
  - 치트시트
  - Quick-Reference
  - Implementation
  - 함정
  - pitfalls
  - Best-Practices
  - JSON
  - logging
  - 로깅
  - testing
  - 테스트
  - Performance
  - 성능
  - Tutorial
  - 튜토리얼
  - 구현
  - Code-Quality
  - 코드품질
  - String
  - War
  - 전쟁
  - HTML
  - Error-Handling
  - 에러처리
  - Debugging
  - 디버깅
  - Documentation
  - 문서화
  - Refactoring
  - 리팩토링
  - Clean-Code
  - 클린코드
  - Optimization
  - 최적화
  - Configuration
  - 설정
  - Guide
  - 가이드
  - Deployment
  - 배포
  - Automation
  - 자동화
  - Workflow
  - 워크플로우
  - Troubleshooting
  - 트러블슈팅
  - Education
---
날짜와 시간은 버그가 숨기 쉬운 영역입니다. 이 치트시트는 naive/aware 구분, UTC 기준 저장, ISO 파싱/포맷, 타임존 변환의 핵심 원칙과 흔한 함정을 정리합니다.

## 언제 이 치트시트를 보나?

- “시간이 9시간 어긋난다/서머타임에서 깨진다” 같은 버그가 날 때
- 저장(JSON/DB)과 표시(UI)에서 **시간 기준**을 정리해야 할 때

## 핵심 패턴

- 저장/전송: 가능하면 **UTC(aware datetime)** + ISO 문자열
- 표시: 로컬 타임존으로 변환해서 보여주기
- naive(타임존 정보 없음) vs aware(타임존 포함) 혼용 금지

## 최소 예제

```python
from datetime import datetime, timezone

now_utc = datetime.now(timezone.utc)  # aware
print(now_utc.isoformat())
```

```python
from datetime import datetime, timezone

# ISO 파싱(간단 케이스): '2026-01-17T12:34:56+00:00'
s = "2026-01-17T12:34:56+00:00"
dt = datetime.fromisoformat(s)
print(dt.tzinfo)
```

```python
from datetime import datetime, timezone

dt = datetime(2026, 1, 17, 12, 0, tzinfo=timezone.utc)
print(dt.strftime("%Y-%m-%d %H:%M %Z"))
```

```python
from datetime import timedelta, datetime, timezone

dt = datetime.now(timezone.utc)
print(dt + timedelta(days=7))
```

## 자주 하는 실수/주의점

- naive datetime을 저장/전송에 쓰면 기준이 사라져서 추후 해석이 깨질 수 있음
- 로컬 타임/서머타임(DST) 경계에서는 “존재하지 않는 시간/중복 시간”이 생길 수 있음 → UTC 저장을 기본으로
- `strptime` 포맷 문자열은 오류에 취약 → 가능하면 ISO 기반(`fromisoformat`)을 우선 고려

## 관련 링크(공식 문서)

- [datetime — Basic date and time types](https://docs.python.org/3/library/datetime.html)

