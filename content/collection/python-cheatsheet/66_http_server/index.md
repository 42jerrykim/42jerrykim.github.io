---
draft: true
image: "wordcloud.png"
title: "[Python Cheatsheet] 66. http.server - 간단한 HTTP 서버"
slug: "lightweight-http-server-setup-file-sharing-api-guide"
description: "파이썬 http.server 모듈을 빠르게 사용하기 위한 치트시트입니다. 한 줄로 파일 서버 실행, 커스텀 핸들러, 간단한 API 서버 만들기 등을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 66
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - http
  - HTTP
  - server
  - 서버
  - http.server
  - SimpleHTTPServer
  - file-server
  - 파일서버
  - web-server
  - 웹서버
  - localhost
  - 로컬호스트
  - static-files
  - 정적파일
  - development
  - 개발
  - testing
  - 테스트
  - handler
  - 핸들러
  - BaseHTTPRequestHandler
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`http.server`는 **간단한 HTTP 서버**를 제공합니다. 정적 파일 서빙, 개발 테스트, 로컬 파일 공유 등에 유용합니다. (프로덕션용 아님)

## 언제 이 치트시트를 보나?

- **로컬에서 파일을 HTTP로 서빙**하고 싶을 때
- **간단한 테스트 서버**가 필요할 때
- **다른 기기에서 파일 접근**이 필요할 때

## 한 줄로 실행

```bash
# 현재 디렉토리를 8000 포트로 서빙
python -m http.server

# 포트 지정
python -m http.server 8080

# 특정 디렉토리
python -m http.server -d /path/to/directory

# 특정 IP에 바인딩
python -m http.server --bind 0.0.0.0

# 모든 옵션
python -m http.server 8080 --bind 0.0.0.0 -d ./public
```

## 최소 예제

### 1. 코드에서 서버 실행

```python
import http.server
import socketserver

PORT = 8000

# 간단한 파일 서버
with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
```

### 2. 커스텀 핸들러

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 응답 상태
        self.send_response(200)
        
        # 헤더
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # 본문
        response = f"<h1>Hello! Path: {self.path}</h1>"
        self.wfile.write(response.encode())
    
    def do_POST(self):
        # POST 데이터 읽기
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = f'{{"received": {len(post_data)} bytes}}'
        self.wfile.write(response.encode())

# 서버 실행
server = HTTPServer(('localhost', 8000), MyHandler)
print("Server running on http://localhost:8000")
server.serve_forever()
```

### 3. JSON API 서버

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# 간단한 데이터 저장소
data = {"items": []}

class APIHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # CORS
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        if self.path == '/api/items':
            self._send_json(data)
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        if self.path == '/api/items':
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))
            data["items"].append(body)
            self._send_json({"status": "created"}, 201)
        else:
            self._send_json({"error": "Not found"}, 404)

server = HTTPServer(('localhost', 8000), APIHandler)
server.serve_forever()
```

### 4. 특정 디렉토리 서빙

```python
from http.server import SimpleHTTPRequestHandler
import socketserver
import os

# 서빙할 디렉토리
os.chdir('/path/to/directory')

PORT = 8000
with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    httpd.serve_forever()
```

### 5. 스레드 서버 (동시 요청)

```python
from http.server import SimpleHTTPRequestHandler
import socketserver

PORT = 8000

# ThreadingTCPServer: 각 요청을 별도 스레드에서 처리
class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

with ThreadedHTTPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Threaded server at port {PORT}")
    httpd.serve_forever()
```

### 6. 요청 정보 출력

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class DebugHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Path: {self.path}")
        print(f"Headers: {dict(self.headers)}")
        print(f"Client: {self.client_address}")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")
    
    # 로그 출력 비활성화
    def log_message(self, format, *args):
        pass  # 또는 커스텀 로깅

HTTPServer(('', 8000), DebugHandler).serve_forever()
```

### 7. 파일 업로드 처리

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class UploadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 업로드 폼 제공
        html = '''
        <html>
        <body>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
        </body>
        </html>
        '''
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def do_POST(self):
        if self.path == '/upload':
            # multipart 파싱
            content_type = self.headers['Content-Type']
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                        'CONTENT_TYPE': content_type}
            )
            
            file_item = form['file']
            if file_item.filename:
                # 파일 저장
                with open(file_item.filename, 'wb') as f:
                    f.write(file_item.file.read())
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Uploaded: {file_item.filename}".encode())
            return
        
        self.send_response(404)
        self.end_headers()

HTTPServer(('', 8000), UploadHandler).serve_forever()
```

### 8. HTTPS (SSL)

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

# 인증서 필요 (openssl로 생성)
# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

server = HTTPServer(('localhost', 4443), SimpleHTTPRequestHandler)
server.socket = ssl.wrap_socket(
    server.socket,
    keyfile='key.pem',
    certfile='cert.pem',
    server_side=True
)
print("HTTPS server on https://localhost:4443")
server.serve_forever()
```

## 자주 하는 실수

### 1. 프로덕션에 사용

```python
# 경고: http.server는 개발/테스트용
# 프로덕션에서는 nginx, gunicorn 등 사용

# 보안 문제:
# - 디렉토리 트래버설 공격에 취약할 수 있음
# - 성능이 낮음
# - 인증/권한 기능 없음
```

### 2. 0.0.0.0 바인딩 주의

```python
# 로컬 전용
python -m http.server  # localhost만

# 네트워크 공개 (주의!)
python -m http.server --bind 0.0.0.0
# 같은 네트워크의 모든 기기에서 접근 가능
```

## 한눈에 정리

| 용도 | 명령/코드 |
|------|----------|
| 빠른 파일 서버 | `python -m http.server` |
| 포트 지정 | `python -m http.server 8080` |
| 커스텀 핸들러 | `BaseHTTPRequestHandler` 상속 |
| 동시 처리 | `ThreadingMixIn` 사용 |

## 참고

- [http.server - Python Docs](https://docs.python.org/3/library/http.server.html)
