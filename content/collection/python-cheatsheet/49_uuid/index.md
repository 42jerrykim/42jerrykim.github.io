---

image: "wordcloud.png"
title: "[Python Cheatsheet] 49. uuid - 고유 식별자 생성"
slug: "unique-id-generation-uuid-module-guide"
description: "파이썬 uuid 모듈을 빠르게 사용하기 위한 치트시트입니다. UUID1/4/5 생성, 문자열 변환, 데이터베이스 키 활용, 버전별 차이점을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 49
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - uuid
  - UUID
  - unique-identifier
  - 고유식별자
  - guid
  - GUID
  - uuid1
  - uuid4
  - uuid5
  - uuid3
  - random
  - 난수
  - identifier
  - 식별자
  - primary-key
  - 기본키
  - database
  - 데이터베이스
  - distributed
  - 분산
  - collision
  - 충돌
  - rfc4122
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
  - security
  - 보안
---
`uuid` 모듈은 **RFC 4122 기반의 고유 식별자(UUID)**를 생성합니다. 데이터베이스 키, 분산 시스템의 ID, 파일명 등에 널리 사용됩니다.

## 언제 이 치트시트를 보나?

- **전역적으로 고유한 ID**가 필요할 때
- 데이터베이스의 **기본 키**로 UUID를 사용할 때
- **분산 시스템**에서 충돌 없는 ID가 필요할 때

## UUID 버전 요약

| 버전 | 생성 방식 | 특징 |
|------|----------|------|
| UUID1 | MAC 주소 + 타임스탬프 | 시간순 정렬 가능, MAC 노출 |
| UUID3 | 네임스페이스 + MD5 | 결정론적, 같은 입력 = 같은 출력 |
| UUID4 | 완전 랜덤 | 가장 많이 사용, 예측 불가 |
| UUID5 | 네임스페이스 + SHA-1 | UUID3보다 안전 |

## 최소 예제

### 1. UUID4 - 가장 일반적

```python
import uuid

# 완전 랜덤 UUID (가장 많이 사용)
id1 = uuid.uuid4()
print(id1)  # 550e8400-e29b-41d4-a716-446655440000

# 여러 개 생성
ids = [uuid.uuid4() for _ in range(3)]
for i in ids:
    print(i)
```

### 2. UUID1 - 시간 기반

```python
import uuid

# MAC 주소 + 타임스탬프 기반
id1 = uuid.uuid1()
print(id1)  # 6ba7b810-9dad-11d1-80b4-00c04fd430c8

# 동일 시점에 생성해도 다름 (시퀀스 번호)
id2 = uuid.uuid1()
print(id1 != id2)  # True
```

### 3. UUID5/UUID3 - 네임스페이스 기반

```python
import uuid

# UUID5 (SHA-1 기반) - 같은 입력 = 같은 출력
namespace = uuid.NAMESPACE_DNS
name = "example.com"

id1 = uuid.uuid5(namespace, name)
id2 = uuid.uuid5(namespace, name)
print(id1 == id2)  # True
print(id1)  # cfbff0d1-9375-5685-968c-48ce8b15ae17

# UUID3 (MD5 기반)
id3 = uuid.uuid3(namespace, name)
print(id3)  # 9073926b-929f-31c2-abc9-fad77ae3e8eb
```

### 4. 문자열 변환

```python
import uuid

id = uuid.uuid4()

# UUID → 문자열
str_id = str(id)
print(str_id)       # '550e8400-e29b-41d4-a716-446655440000'
print(id.hex)       # '550e8400e29b41d4a716446655440000' (하이픈 없음)

# 문자열 → UUID
restored = uuid.UUID(str_id)
restored_hex = uuid.UUID('550e8400e29b41d4a716446655440000')
print(restored == restored_hex)  # True
```

### 5. UUID 속성

```python
import uuid

id = uuid.uuid4()

print(id.hex)       # 32자 16진수 문자열
print(id.int)       # 128비트 정수
print(id.bytes)     # 16바이트
print(id.version)   # 4 (UUID 버전)
print(id.variant)   # RFC_4122
```

### 6. 데이터베이스 키로 사용

```python
import uuid

class User:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name

user1 = User("Alice")
user2 = User("Bob")

print(f"User1: {user1.id}")
print(f"User2: {user2.id}")

# 딕셔너리 키로 사용
users = {
    user1.id: user1,
    user2.id: user2
}
```

### 7. 짧은 ID 만들기

```python
import uuid
import base64

def short_uuid():
    """22자 URL-safe 짧은 UUID"""
    u = uuid.uuid4()
    return base64.urlsafe_b64encode(u.bytes).rstrip(b'=').decode('ascii')

print(short_uuid())  # 'VGhpcyBpcyBhbiBleGFt'

def shorter_uuid():
    """8자 짧은 ID (충돌 가능성 있음)"""
    return uuid.uuid4().hex[:8]

print(shorter_uuid())  # 'a1b2c3d4'
```

### 8. URL에서 UUID 파싱

```python
import uuid
import re

def extract_uuids(text):
    """텍스트에서 UUID 추출"""
    pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return [uuid.UUID(m) for m in matches]

url = "https://example.com/user/550e8400-e29b-41d4-a716-446655440000/profile"
uuids = extract_uuids(url)
print(uuids)  # [UUID('550e8400-e29b-41d4-a716-446655440000')]
```

### 9. 유효성 검사

```python
import uuid

def is_valid_uuid(val):
    """UUID 문자열 유효성 검사"""
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

print(is_valid_uuid('550e8400-e29b-41d4-a716-446655440000'))  # True
print(is_valid_uuid('not-a-uuid'))  # False
print(is_valid_uuid('550e8400e29b41d4a716446655440000'))  # True (하이픈 없어도)
```

### 10. 네임스페이스 상수

```python
import uuid

# 미리 정의된 네임스페이스
print(uuid.NAMESPACE_DNS)   # DNS 이름용
print(uuid.NAMESPACE_URL)   # URL용
print(uuid.NAMESPACE_OID)   # ISO OID용
print(uuid.NAMESPACE_X500)  # X.500 DN용

# 커스텀 네임스페이스
MY_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "myapp.example.com")
user_id = uuid.uuid5(MY_NAMESPACE, "user:alice")
```

## UUID 버전 선택 가이드

```python
import uuid

# 완전 랜덤, 예측 불가 필요 → UUID4
uuid.uuid4()

# 같은 입력에 같은 ID 필요 → UUID5
uuid.uuid5(uuid.NAMESPACE_DNS, "example.com")

# 시간순 정렬 필요, MAC 노출 괜찮음 → UUID1
uuid.uuid1()

# 레거시 호환 (MD5) → UUID3
uuid.uuid3(uuid.NAMESPACE_DNS, "example.com")
```

## 자주 하는 실수

### 1. 문자열로 비교

```python
import uuid

id1 = uuid.uuid4()
id2 = uuid.UUID(str(id1))

# UUID 객체로 비교
print(id1 == id2)  # True

# 문자열 비교 시 대소문자 주의
print(str(id1).lower() == str(id2).lower())  # True
```

### 2. UUID1의 프라이버시

```python
import uuid

# UUID1은 MAC 주소를 포함 (프라이버시 우려)
id1 = uuid.uuid1()
print(id1.node)  # MAC 주소 (정수)

# 프라이버시가 중요하면 UUID4 사용
```

## 한눈에 정리

| 함수 | 용도 | 특징 |
|------|------|------|
| `uuid4()` | 일반 고유 ID | 랜덤, 가장 많이 사용 |
| `uuid1()` | 시간 기반 ID | 정렬 가능, MAC 노출 |
| `uuid5(ns, name)` | 결정론적 ID | 같은 입력 = 같은 출력 |
| `UUID(string)` | 문자열 → UUID | 파싱/검증 |

## 참고

- [uuid - Python Docs](https://docs.python.org/3/library/uuid.html)
- [RFC 4122 - UUID URN](https://tools.ietf.org/html/rfc4122)
