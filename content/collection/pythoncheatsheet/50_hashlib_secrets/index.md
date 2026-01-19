---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 50. hashlib & secrets - 해시/보안 난수 패턴"
slug: "hashlib-and-secrets-hash-md5-sha1-sha256-sha512-checksum-digest-token"
description: "파이썬 hashlib과 secrets 모듈을 빠르게 쓰기 위한 치트시트입니다. MD5/SHA 해시 생성, 파일 체크섬, 보안 토큰 생성, 안전한 비밀번호 비교, random vs secrets 차이를 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 50
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - hashlib
  - secrets
  - hash
  - 해시
  - md5
  - sha1
  - sha256
  - sha512
  - checksum
  - 체크섬
  - digest
  - hexdigest
  - security
  - 보안
  - cryptography
  - 암호화
  - token
  - 토큰
  - random
  - 난수
  - secure-random
  - 보안난수
  - password
  - 비밀번호
  - compare_digest
  - urlsafe
  - token_hex
  - token_bytes
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
hashlib은 해시 함수를, secrets는 보안 난수를 제공합니다. 이 치트시트는 MD5/SHA 해시 생성, 파일 체크섬, 보안 토큰 생성, random vs secrets 차이를 정리합니다.

## 언제 이 치트시트를 보나?

- **파일 무결성 검증**(체크섬)이 필요할 때
- **보안 토큰, API 키, 임시 비밀번호**를 생성해야 할 때
- `random` 모듈이 보안에 적합한지 궁금할 때

## 핵심 패턴

- `hashlib.sha256(data).hexdigest()`: 해시 생성
- `secrets.token_hex(n)`: 보안 난수 토큰 (n바이트)
- `secrets.compare_digest(a, b)`: 타이밍 공격 방지 비교
- **random ❌ 보안용**, **secrets ✅ 보안용**

## hashlib - 해시 생성

```python
import hashlib

# 문자열 해시 (UTF-8 인코딩 필요)
text = "Hello, World!"
hash_obj = hashlib.sha256(text.encode('utf-8'))

# 16진수 문자열
print(hash_obj.hexdigest())
# dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f

# bytes
print(hash_obj.digest())
# b'\xdf\xfdb...'

# 다양한 해시 알고리즘
print(hashlib.md5(text.encode()).hexdigest())     # MD5 (보안용 비권장)
print(hashlib.sha1(text.encode()).hexdigest())    # SHA-1 (보안용 비권장)
print(hashlib.sha256(text.encode()).hexdigest())  # SHA-256
print(hashlib.sha512(text.encode()).hexdigest())  # SHA-512
print(hashlib.sha3_256(text.encode()).hexdigest())  # SHA-3
```

```python
# 점진적 해시 (대용량 데이터)
import hashlib

hash_obj = hashlib.sha256()
hash_obj.update(b"Hello, ")
hash_obj.update(b"World!")
print(hash_obj.hexdigest())
# dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f
```

## hashlib - 파일 체크섬

```python
import hashlib

def file_hash(filepath: str, algorithm: str = 'sha256') -> str:
    """파일의 해시값 계산"""
    hash_obj = hashlib.new(algorithm)
    
    with open(filepath, 'rb') as f:
        # 청크 단위로 읽어서 메모리 효율적 처리
        for chunk in iter(lambda: f.read(8192), b''):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()

# 사용
checksum = file_hash('large_file.bin')
print(f"SHA-256: {checksum}")

# MD5 체크섬 (호환성용)
md5_sum = file_hash('file.zip', 'md5')
print(f"MD5: {md5_sum}")
```

```python
# 파일 무결성 검증
def verify_file(filepath: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
    actual_hash = file_hash(filepath, algorithm)
    return actual_hash == expected_hash

# 다운로드 후 검증
if verify_file('downloaded.zip', 'abc123...'):
    print("File integrity OK")
else:
    print("File corrupted!")
```

## secrets - 보안 난수

```python
import secrets

# 16진수 토큰 (32자 = 16바이트)
token = secrets.token_hex(16)
print(token)  # 'a3f2b1c9e8d7f6a5b4c3d2e1f0a9b8c7'

# bytes 토큰
token_bytes = secrets.token_bytes(16)
print(token_bytes)  # b'\xa3\xf2\xb1...'

# URL 안전 토큰 (Base64)
token_url = secrets.token_urlsafe(16)
print(token_url)  # 'o_z2sckO9Vy6...'
```

```python
# 보안 난수 정수
import secrets

# 0 ~ n-1 범위
random_int = secrets.randbelow(100)  # 0-99

# 특정 비트 수의 난수
random_bits = secrets.randbits(128)  # 128비트 난수

# 리스트에서 무작위 선택
items = ['apple', 'banana', 'cherry']
choice = secrets.choice(items)
```

## secrets - 실전 패턴

```python
import secrets
import string

# 임시 비밀번호 생성
def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

print(generate_password())  # 'aK3$mP9@xL2!nQ5&'

# 더 안전한 패스프레이즈
def generate_passphrase(num_words: int = 4) -> str:
    words = ['correct', 'horse', 'battery', 'staple', 
             'apple', 'banana', 'cherry', 'dragon']  # 실제로는 더 큰 단어 리스트 사용
    return '-'.join(secrets.choice(words) for _ in range(num_words))

print(generate_passphrase())  # 'horse-apple-staple-dragon'
```

```python
# API 키 생성
def generate_api_key() -> str:
    return f"sk_{secrets.token_urlsafe(32)}"

api_key = generate_api_key()
print(api_key)  # 'sk_Xy3kL9mN...'
```

```python
# 비밀번호 재설정 토큰
def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)

# 이메일 인증 코드 (6자리 숫자)
def generate_verification_code() -> str:
    return ''.join(str(secrets.randbelow(10)) for _ in range(6))

print(generate_verification_code())  # '847293'
```

## 안전한 비교

```python
import secrets
import hmac

# 타이밍 공격 방지 비교
def verify_token(user_token: str, stored_token: str) -> bool:
    # 일반 비교 (취약)
    # return user_token == stored_token  # ❌ 타이밍 공격에 취약
    
    # 안전한 비교
    return secrets.compare_digest(user_token, stored_token)  # ✅

# 또는 hmac.compare_digest 사용
def verify_token_hmac(user_token: str, stored_token: str) -> bool:
    return hmac.compare_digest(user_token, stored_token)
```

## random vs secrets

```python
import random
import secrets

# random - 예측 가능 (시뮬레이션, 게임용)
random.seed(42)  # 시드 설정 가능 → 재현 가능
print(random.randint(0, 100))  # 항상 같은 값

# secrets - 예측 불가능 (보안용)
# 시드 설정 불가, OS의 암호학적 난수 소스 사용
print(secrets.randbelow(100))  # 매번 다른 값
```

| 용도 | 모듈 |
|------|------|
| 게임, 시뮬레이션, 테스트 | `random` |
| 비밀번호, 토큰, API 키 | `secrets` |
| 세션 ID, 인증 코드 | `secrets` |
| 암호화 키, nonce | `secrets` (또는 `os.urandom`) |

## 자주 하는 실수/주의점

- **MD5/SHA-1은 보안용 비권장**: 충돌 공격 가능, 체크섬/캐시 키에만 사용
- **random은 보안에 부적합**: PRNG(의사 난수)로 예측 가능
- **비밀번호 저장에 해시만 사용 ❌**: bcrypt, scrypt, argon2 같은 KDF 사용 권장
- **토큰 비교 시 `==` 사용 ❌**: 타이밍 공격 방지를 위해 `compare_digest` 사용
- **솔트 없는 해시 ❌**: 비밀번호 해시에는 반드시 솔트 추가

```python
# 비밀번호 해시 (권장 방식)
# pip install bcrypt
import bcrypt

password = b"my_password"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)

# 검증
if bcrypt.checkpw(password, hashed):
    print("Password correct")
```

## 관련 링크(공식 문서)

- [hashlib — Secure hashes and message digests](https://docs.python.org/3/library/hashlib.html)
- [secrets — Generate secure random numbers](https://docs.python.org/3/library/secrets.html)
- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html)
