---
draft: true
image: "tmp_wordcloud.png"
title: "[Python Cheatsheet] 43. struct & bytes - 바이너리 데이터 pack/unpack"
slug: "struct-bytes-binary-pack-unpack-endian-parse-tutorial"
description: "파이썬 struct 모듈과 bytes를 빠르게 쓰기 위한 치트시트입니다. 바이너리 데이터 pack/unpack, 포맷 문자, 엔디언, 파일 헤더 파싱, 네트워크 프로토콜 처리 패턴을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 43
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - struct
  - bytes
  - bytearray
  - binary
  - 바이너리
  - pack
  - unpack
  - 패킹
  - 언패킹
  - format
  - 포맷
  - endian
  - 엔디언
  - big-endian
  - little-endian
  - network
  - 네트워크
  - protocol
  - 프로토콜
  - header
  - 헤더
  - parsing
  - 파싱
  - file-format
  - 파일포맷
  - C-struct
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
  - low-level
  - 저수준
---
struct는 파이썬 값과 C 구조체/바이너리 데이터 간의 변환을 제공합니다. 이 치트시트는 pack/unpack, 포맷 문자, 엔디언, 파일 헤더 파싱 패턴을 정리합니다.

## 언제 이 치트시트를 보나?

- **바이너리 파일 포맷**(BMP, WAV 등)을 읽거나 써야 할 때
- **네트워크 프로토콜**에서 고정 길이 바이너리 데이터를 처리할 때
- C 코드와 **데이터 교환**이 필요할 때

## 핵심 패턴

- `struct.pack(fmt, v1, v2, ...)`: 값들을 bytes로 변환
- `struct.unpack(fmt, buffer)`: bytes를 튜플로 변환
- 포맷 문자: `b/B`(1바이트), `h/H`(2바이트), `i/I`(4바이트), `q/Q`(8바이트)
- 엔디언: `<`(리틀), `>`(빅), `!`(네트워크=빅)

## struct - 기본 pack/unpack

```python
import struct

# pack: 값 → bytes
data = struct.pack('i', 42)  # 정수를 4바이트로
print(data)  # b'*\x00\x00\x00' (리틀 엔디언)
print(len(data))  # 4

# unpack: bytes → 튜플
values = struct.unpack('i', data)
print(values)  # (42,)
print(values[0])  # 42
```

```python
# 여러 값 pack/unpack
import struct

# 정수(4), 실수(8), 문자(1)
packed = struct.pack('idc', 42, 3.14, b'A')
print(len(packed))  # 13 (패딩 포함)

unpacked = struct.unpack('idc', packed)
print(unpacked)  # (42, 3.14, b'A')
```

## 포맷 문자 (자주 사용)

| 포맷 | C 타입 | 파이썬 타입 | 크기 |
|------|--------|------------|------|
| `b` | signed char | int | 1 |
| `B` | unsigned char | int | 1 |
| `h` | short | int | 2 |
| `H` | unsigned short | int | 2 |
| `i` | int | int | 4 |
| `I` | unsigned int | int | 4 |
| `q` | long long | int | 8 |
| `Q` | unsigned long long | int | 8 |
| `f` | float | float | 4 |
| `d` | double | float | 8 |
| `c` | char | bytes (1) | 1 |
| `s` | char[] | bytes | n |
| `?` | _Bool | bool | 1 |
| `x` | pad byte | 없음 | 1 |

```python
import struct

# 다양한 타입
packed = struct.pack('BHI', 255, 65535, 2**32-1)
print(struct.unpack('BHI', packed))  # (255, 65535, 4294967295)

# 문자열 (고정 길이)
packed = struct.pack('10s', b'hello')
print(packed)  # b'hello\x00\x00\x00\x00\x00'
print(struct.unpack('10s', packed))  # (b'hello\x00\x00\x00\x00\x00',)

# 반복
packed = struct.pack('3i', 1, 2, 3)
print(struct.unpack('3i', packed))  # (1, 2, 3)
```

## 엔디언 (바이트 순서)

```python
import struct

value = 0x01020304

# 리틀 엔디언 (Intel, AMD) - 낮은 바이트가 먼저
little = struct.pack('<I', value)
print(little.hex())  # '04030201'

# 빅 엔디언 (네트워크, 일부 파일 포맷) - 높은 바이트가 먼저
big = struct.pack('>I', value)
print(big.hex())  # '01020304'

# 네트워크 바이트 순서 (= 빅 엔디언)
network = struct.pack('!I', value)
print(network.hex())  # '01020304'

# 네이티브 (시스템 기본)
native = struct.pack('=I', value)  # 또는 '@'
```

## Struct 클래스 (성능 최적화)

```python
import struct

# 같은 포맷 반복 사용 시 Struct 객체가 효율적
header_format = struct.Struct('>BBHI')  # 빅 엔디언

# 한 번만 포맷 파싱
print(header_format.size)  # 8

# pack/unpack
packed = header_format.pack(1, 2, 1000, 999999)
unpacked = header_format.unpack(packed)
print(unpacked)  # (1, 2, 1000, 999999)
```

## 파일 헤더 파싱 예시

```python
import struct

# BMP 파일 헤더 읽기 예시
def read_bmp_header(filepath: str) -> dict:
    with open(filepath, 'rb') as f:
        # BMP 파일 헤더 (14바이트)
        header = f.read(14)
        
        # 리틀 엔디언으로 파싱
        magic, file_size, _, _, offset = struct.unpack('<2sIHHI', header)
        
        return {
            'magic': magic,           # b'BM'
            'file_size': file_size,
            'data_offset': offset
        }

# WAV 파일 헤더 예시
def read_wav_header(filepath: str) -> dict:
    with open(filepath, 'rb') as f:
        # RIFF 청크
        riff, size, wave = struct.unpack('<4sI4s', f.read(12))
        
        # fmt 청크
        fmt, fmt_size = struct.unpack('<4sI', f.read(8))
        audio_fmt, channels, sample_rate, byte_rate, block_align, bits = \
            struct.unpack('<HHIIHH', f.read(16))
        
        return {
            'channels': channels,
            'sample_rate': sample_rate,
            'bits_per_sample': bits
        }
```

## 네트워크 프로토콜 예시

```python
import struct

# 간단한 프로토콜 패킷 정의
# [type: 1byte][length: 2bytes][data: variable]

def create_packet(msg_type: int, data: bytes) -> bytes:
    header = struct.pack('!BH', msg_type, len(data))
    return header + data

def parse_packet(packet: bytes) -> tuple:
    msg_type, length = struct.unpack('!BH', packet[:3])
    data = packet[3:3+length]
    return msg_type, data

# 사용
packet = create_packet(1, b'Hello')
msg_type, data = parse_packet(packet)
print(f"Type: {msg_type}, Data: {data}")  # Type: 1, Data: b'Hello'
```

## bytes / bytearray 조작

```python
# bytes 생성
b1 = b'\x00\x01\x02\x03'
b2 = bytes([0, 1, 2, 3])
b3 = bytes.fromhex('00010203')

# hex 변환
print(b1.hex())  # '00010203'
print(b1.hex(' '))  # '00 01 02 03'

# bytearray (변경 가능)
ba = bytearray(b'hello')
ba[0] = ord('H')
print(ba)  # bytearray(b'Hello')

# int ↔ bytes
num = 1000
num_bytes = num.to_bytes(2, 'big')      # b'\x03\xe8'
num_back = int.from_bytes(num_bytes, 'big')  # 1000
```

## 자주 하는 실수/주의점

- **엔디언 명시**: 포맷 앞에 `<`/`>` 없으면 네이티브 사용 (이식성 문제)
- **패딩**: 기본적으로 C 구조체처럼 패딩 있음 → `=`로 패딩 없이
- **문자열 길이 고정**: `10s`는 정확히 10바이트 (짧으면 null 패딩)
- **부호 있는/없는 구분**: `i` vs `I`, `h` vs `H` 등
- **unpack은 튜플 반환**: 단일 값도 `(value,)` 형태

```python
import struct

# 패딩 차이
print(struct.calcsize('Bi'))   # 8 (패딩 포함)
print(struct.calcsize('=Bi'))  # 5 (패딩 없음)

# 단일 값 unpack
data = struct.pack('i', 42)
(value,) = struct.unpack('i', data)  # 튜플 언패킹
# 또는
value = struct.unpack('i', data)[0]
```

## 관련 링크(공식 문서)

- [struct — Interpret bytes as packed binary data](https://docs.python.org/3/library/struct.html)
- [bytes/bytearray](https://docs.python.org/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview)
