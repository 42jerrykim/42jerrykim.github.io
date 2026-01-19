---
draft: true
title: "[Python Cheatsheet] 38. zoneinfo - 표준 시간대 (Python 3.9+)"
slug: "datetime-standard-timezone-iana-zoneinfo-guide"
description: "파이썬 zoneinfo 모듈을 빠르게 사용하기 위한 치트시트입니다. IANA 타임존, aware datetime 생성, 시간대 변환, DST 처리 등 표준 시간대 작업 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 38
tags:
  - python
  - Python
  - python3
  - python39
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - zoneinfo
  - timezone
  - 시간대
  - 타임존
  - iana
  - tz-database
  - datetime
  - 날짜시간
  - aware
  - naive
  - utc
  - dst
  - daylight-saving
  - 서머타임
  - convert
  - 변환
  - localize
  - 지역화
  - ZoneInfo
  - available_timezones
  - astimezone
  - replace
  - now
  - international
  - 국제화
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - pytz
  - dateutil
---
`zoneinfo`는 Python 3.9+에서 **IANA 시간대 데이터베이스**를 사용하는 표준 모듈입니다. pytz 없이도 올바른 시간대 처리가 가능합니다.

## 언제 이 치트시트를 보나?

- **시간대가 있는 datetime**을 다룰 때
- **UTC ↔ 로컬 시간** 변환이 필요할 때
- **서로 다른 시간대 간 변환**이 필요할 때

## 핵심 사용법

```python
from zoneinfo import ZoneInfo
from datetime import datetime

# ZoneInfo 객체 생성
tz_seoul = ZoneInfo("Asia/Seoul")
tz_utc = ZoneInfo("UTC")

# aware datetime 생성
dt = datetime(2024, 6, 15, 12, 0, tzinfo=tz_seoul)

# 현재 시간 (특정 시간대)
now = datetime.now(tz_seoul)

# 시간대 변환
dt_utc = dt.astimezone(tz_utc)
```

## 최소 예제

### 1. 기본 사용

```python
from zoneinfo import ZoneInfo
from datetime import datetime

# 서울 시간대
seoul = ZoneInfo("Asia/Seoul")

# aware datetime 생성
dt = datetime(2024, 6, 15, 14, 30, tzinfo=seoul)
print(dt)  # 2024-06-15 14:30:00+09:00

# 현재 시간
now = datetime.now(seoul)
print(now)
```

### 2. 시간대 변환

```python
from zoneinfo import ZoneInfo
from datetime import datetime

seoul = ZoneInfo("Asia/Seoul")
new_york = ZoneInfo("America/New_York")
utc = ZoneInfo("UTC")

# 서울 시간
dt_seoul = datetime(2024, 6, 15, 14, 0, tzinfo=seoul)
print(f"Seoul: {dt_seoul}")
# Seoul: 2024-06-15 14:00:00+09:00

# UTC로 변환
dt_utc = dt_seoul.astimezone(utc)
print(f"UTC: {dt_utc}")
# UTC: 2024-06-15 05:00:00+00:00

# 뉴욕으로 변환
dt_ny = dt_seoul.astimezone(new_york)
print(f"New York: {dt_ny}")
# New York: 2024-06-15 01:00:00-04:00
```

### 3. UTC 시간 다루기

```python
from zoneinfo import ZoneInfo
from datetime import datetime, timezone

# UTC 시간 생성 방법 1: ZoneInfo
utc_tz = ZoneInfo("UTC")
dt1 = datetime.now(utc_tz)

# UTC 시간 생성 방법 2: datetime.timezone.utc
dt2 = datetime.now(timezone.utc)

# 둘 다 동일하게 동작
print(dt1.astimezone(ZoneInfo("Asia/Seoul")))
```

### 4. 사용 가능한 시간대 목록

```python
from zoneinfo import available_timezones

# 모든 사용 가능한 시간대
all_zones = available_timezones()
print(len(all_zones))  # 약 594개

# 특정 지역 시간대 필터링
asia_zones = [tz for tz in all_zones if tz.startswith('Asia/')]
print(sorted(asia_zones)[:5])
# ['Asia/Aden', 'Asia/Almaty', 'Asia/Amman', 'Asia/Anadyr', 'Asia/Aqtau']
```

### 5. naive → aware 변환

```python
from zoneinfo import ZoneInfo
from datetime import datetime

# naive datetime (시간대 없음)
naive = datetime(2024, 6, 15, 14, 0)

# aware로 변환 (해당 시간대의 시간으로 해석)
seoul = ZoneInfo("Asia/Seoul")
aware = naive.replace(tzinfo=seoul)
print(aware)  # 2024-06-15 14:00:00+09:00
```

### 6. DST (서머타임) 자동 처리

```python
from zoneinfo import ZoneInfo
from datetime import datetime

ny = ZoneInfo("America/New_York")

# 여름 (DST 적용, -04:00)
summer = datetime(2024, 7, 1, 12, 0, tzinfo=ny)
print(summer)  # 2024-07-01 12:00:00-04:00

# 겨울 (DST 미적용, -05:00)
winter = datetime(2024, 1, 1, 12, 0, tzinfo=ny)
print(winter)  # 2024-01-01 12:00:00-05:00
```

### 7. 문자열 파싱과 시간대

```python
from zoneinfo import ZoneInfo
from datetime import datetime

# ISO 형식 파싱 (Python 3.11+)
dt = datetime.fromisoformat("2024-06-15T14:00:00+09:00")
print(dt)

# 수동으로 시간대 추가
naive_str = "2024-06-15 14:00:00"
naive = datetime.strptime(naive_str, "%Y-%m-%d %H:%M:%S")
aware = naive.replace(tzinfo=ZoneInfo("Asia/Seoul"))
```

### 8. 시간 비교

```python
from zoneinfo import ZoneInfo
from datetime import datetime

seoul = ZoneInfo("Asia/Seoul")
tokyo = ZoneInfo("Asia/Tokyo")

# 같은 시각 (다른 표현)
dt_seoul = datetime(2024, 6, 15, 14, 0, tzinfo=seoul)
dt_tokyo = datetime(2024, 6, 15, 14, 0, tzinfo=tokyo)

# 서울과 도쿄는 같은 UTC 오프셋
print(dt_seoul == dt_tokyo)  # True

# UTC 시간 확인
print(dt_seoul.utcoffset())  # 9:00:00
print(dt_tokyo.utcoffset())  # 9:00:00
```

### 9. 날짜 연산

```python
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

seoul = ZoneInfo("Asia/Seoul")
dt = datetime(2024, 6, 15, 14, 0, tzinfo=seoul)

# timedelta 연산
next_day = dt + timedelta(days=1)
print(next_day)  # 2024-06-16 14:00:00+09:00

# DST 경계를 넘는 경우도 자동 처리
ny = ZoneInfo("America/New_York")
before_dst = datetime(2024, 3, 10, 1, 30, tzinfo=ny)
after_2h = before_dst + timedelta(hours=2)
print(after_2h)  # DST로 인해 3:30이 됨
```

### 10. tzdata 패키지 (Windows)

```python
# Windows에서는 tzdata 패키지 필요
# pip install tzdata

from zoneinfo import ZoneInfo

# 패키지 설치 후 사용 가능
seoul = ZoneInfo("Asia/Seoul")
```

## 주요 시간대 예시

```python
from zoneinfo import ZoneInfo

# 주요 도시
ZoneInfo("Asia/Seoul")       # 서울 (KST, +09:00)
ZoneInfo("Asia/Tokyo")       # 도쿄 (JST, +09:00)
ZoneInfo("Asia/Shanghai")    # 상하이 (CST, +08:00)
ZoneInfo("America/New_York") # 뉴욕 (EST/EDT)
ZoneInfo("America/Los_Angeles")  # LA (PST/PDT)
ZoneInfo("Europe/London")    # 런던 (GMT/BST)
ZoneInfo("Europe/Paris")     # 파리 (CET/CEST)
ZoneInfo("UTC")              # UTC
```

## 자주 하는 실수

### 1. naive datetime 비교

```python
from zoneinfo import ZoneInfo
from datetime import datetime

naive = datetime(2024, 6, 15, 14, 0)
aware = datetime(2024, 6, 15, 14, 0, tzinfo=ZoneInfo("Asia/Seoul"))

# TypeError: can't compare offset-naive and offset-aware datetimes
# naive == aware
```

### 2. replace vs astimezone 혼동

```python
from zoneinfo import ZoneInfo
from datetime import datetime

seoul = ZoneInfo("Asia/Seoul")
utc = ZoneInfo("UTC")

dt_seoul = datetime(2024, 6, 15, 14, 0, tzinfo=seoul)

# replace: 시각은 유지, 시간대만 변경 (잘못된 사용)
wrong = dt_seoul.replace(tzinfo=utc)
print(wrong)  # 2024-06-15 14:00:00+00:00 (틀림!)

# astimezone: 올바른 변환
correct = dt_seoul.astimezone(utc)
print(correct)  # 2024-06-15 05:00:00+00:00 (맞음!)
```

## 한눈에 정리

| 작업 | 방법 |
|------|------|
| 시간대 객체 생성 | `ZoneInfo("Asia/Seoul")` |
| aware datetime | `datetime(..., tzinfo=tz)` |
| 현재 시간 | `datetime.now(tz)` |
| 시간대 변환 | `dt.astimezone(new_tz)` |
| 사용 가능 시간대 | `available_timezones()` |

## 참고

- [zoneinfo - Python Docs](https://docs.python.org/3/library/zoneinfo.html)
- [IANA Time Zone Database](https://www.iana.org/time-zones)
- [PEP 615 - Support for IANA Time Zone Database](https://peps.python.org/pep-0615/)
