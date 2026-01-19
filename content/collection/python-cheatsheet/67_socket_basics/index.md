---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 67. socket - 소켓 프로그래밍 최소 패턴"
slug: "easy-socket-programming-guide-tcp-udp-server-client-network"
description: "파이썬 socket 모듈을 빠르게 쓰기 위한 치트시트입니다. TCP/UDP 클라이언트/서버, 연결/송수신/종료, 타임아웃, 간단한 HTTP 요청 패턴과 주의점을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 67
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - socket
  - 소켓
  - network
  - 네트워크
  - tcp
  - TCP
  - udp
  - UDP
  - client
  - 클라이언트
  - server
  - 서버
  - connection
  - 연결
  - send
  - recv
  - 송수신
  - bind
  - listen
  - accept
  - connect
  - timeout
  - 타임아웃
  - ip
  - port
  - 포트
  - localhost
  - AF_INET
  - SOCK_STREAM
  - SOCK_DGRAM
  - blocking
  - non-blocking
  - standard-library
  - 표준라이브러리
  - best-practices
  - 베스트프랙티스
  - pitfalls
  - 함정
---
socket 모듈은 저수준 네트워크 인터페이스를 제공합니다. 이 치트시트는 TCP/UDP 클라이언트/서버의 최소 패턴, 타임아웃 처리, 주의점을 정리합니다.

## 언제 이 치트시트를 보나?

- **저수준 네트워크 통신**이 필요할 때
- **커스텀 프로토콜** 구현이 필요할 때
- HTTP 라이브러리 없이 **간단한 요청**을 보내고 싶을 때

## 핵심 패턴

- TCP: `SOCK_STREAM` - 연결 지향, 신뢰성 보장
- UDP: `SOCK_DGRAM` - 비연결, 빠르지만 손실 가능
- 서버: `bind()` → `listen()` → `accept()` → `recv()`/`send()`
- 클라이언트: `connect()` → `send()`/`recv()`

## TCP 클라이언트

```python
import socket

# TCP 클라이언트 기본
def tcp_client():
    # AF_INET: IPv4, SOCK_STREAM: TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(5.0)  # 5초 타임아웃
        sock.connect(('localhost', 8080))
        
        # 데이터 전송
        sock.sendall(b'Hello, Server!')
        
        # 데이터 수신
        data = sock.recv(1024)  # 최대 1024바이트
        print(f'Received: {data.decode()}')

tcp_client()
```

```python
# 간단한 HTTP GET 요청
import socket

def simple_http_get(host: str, path: str = '/') -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(10.0)
        sock.connect((host, 80))
        
        # HTTP 요청 전송
        request = f'GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'
        sock.sendall(request.encode())
        
        # 응답 수신
        response = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        
        return response.decode()

# 실제로는 requests나 urllib 사용 권장
# print(simple_http_get('example.com', '/'))
```

## TCP 서버

```python
import socket

def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # 주소 재사용 허용 (빠른 재시작)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server.bind(('localhost', 8080))
        server.listen(5)  # 대기 큐 크기
        print('Server listening on port 8080...')
        
        while True:
            # 클라이언트 연결 대기
            client, addr = server.accept()
            with client:
                print(f'Connected by {addr}')
                
                # 데이터 수신
                data = client.recv(1024)
                if data:
                    print(f'Received: {data.decode()}')
                    # 응답 전송
                    client.sendall(b'Hello, Client!')

# tcp_server()
```

```python
# 다중 클라이언트 처리 (스레드)
import socket
import threading

def handle_client(client: socket.socket, addr: tuple):
    with client:
        print(f'Connected: {addr}')
        while True:
            data = client.recv(1024)
            if not data:
                break
            client.sendall(data)  # 에코 서버
    print(f'Disconnected: {addr}')

def threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('localhost', 8080))
        server.listen(5)
        
        while True:
            client, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client, addr))
            thread.start()
```

## UDP 클라이언트/서버

```python
import socket

# UDP 클라이언트
def udp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(5.0)
        
        # connect 없이 바로 전송 (비연결)
        sock.sendto(b'Hello, UDP Server!', ('localhost', 9999))
        
        # 응답 수신
        data, addr = sock.recvfrom(1024)
        print(f'Received from {addr}: {data.decode()}')

# UDP 서버
def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', 9999))
        print('UDP Server listening on port 9999...')
        
        while True:
            data, addr = sock.recvfrom(1024)
            print(f'Received from {addr}: {data.decode()}')
            sock.sendto(b'ACK', addr)
```

## 타임아웃 처리

```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # 전체 타임아웃 설정
    sock.settimeout(5.0)
    
    try:
        sock.connect(('localhost', 8080))
        sock.sendall(b'test')
        data = sock.recv(1024)
    except socket.timeout:
        print('Connection timed out')
    except socket.error as e:
        print(f'Socket error: {e}')
```

```python
# 논블로킹 모드
import socket
import select

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(False)

try:
    sock.connect(('localhost', 8080))
except BlockingIOError:
    pass  # 논블로킹에서는 바로 반환

# select로 대기
ready = select.select([sock], [sock], [], 5.0)
if ready[1]:  # 쓰기 가능 = 연결됨
    sock.sendall(b'test')
```

## 유용한 함수

```python
import socket

# 호스트 이름 → IP
ip = socket.gethostbyname('example.com')
print(ip)  # 93.184.216.34

# 서비스 이름 → 포트
port = socket.getservbyname('http')
print(port)  # 80

# 현재 호스트 이름
hostname = socket.gethostname()
print(hostname)

# 주소 정보 조회
info = socket.getaddrinfo('example.com', 80)
for family, socktype, proto, canonname, sockaddr in info:
    print(sockaddr)  # ('93.184.216.34', 80)
```

## 소켓 옵션

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 주소 재사용 (서버 재시작 시 유용)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# TCP Keepalive
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# 버퍼 크기
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)

# TCP_NODELAY (Nagle 알고리즘 비활성화)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
```

## 자주 하는 실수/주의점

- **recv()는 요청한 만큼 안 올 수 있음**: 루프로 전체 수신 필요
  ```python
  def recv_all(sock, length):
      data = b''
      while len(data) < length:
          chunk = sock.recv(length - len(data))
          if not chunk:
              raise ConnectionError('Connection closed')
          data += chunk
      return data
  ```
- **sendall() vs send()**: `send()`는 일부만 보낼 수 있음, `sendall()` 권장
- **리소스 정리**: `with` 문 또는 `try/finally`로 소켓 닫기
- **인코딩**: 문자열은 `encode()`/`decode()` 필요
- **포트 번호**: 1024 미만은 root 권한 필요
- **IPv6**: `AF_INET6` 사용, 듀얼 스택은 별도 처리 필요

## 고수준 대안

```python
# 일반 HTTP 요청 → requests 라이브러리
import requests
response = requests.get('https://example.com')

# 비동기 서버 → asyncio
import asyncio

async def handle_client(reader, writer):
    data = await reader.read(100)
    writer.write(data)
    await writer.drain()
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, 'localhost', 8080)
    async with server:
        await server.serve_forever()

# 웹 서버 → Flask, FastAPI 등
```

## 관련 링크(공식 문서)

- [socket — Low-level networking interface](https://docs.python.org/3/library/socket.html)
- [Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
