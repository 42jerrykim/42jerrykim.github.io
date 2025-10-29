---
draft: true
title: "21. 네트워킹"
description: "네트워크 프로그래밍과 HTTP, WebSocket 등 통신 프로토콜"
collection_order: 21
---

# 챕터 21: 네트워킹

> "연결된 세상에서 소통하라" - 네트워크 프로그래밍을 통해 전 세계와 연결되는 애플리케이션을 만들어봅시다.

## 학습 목표
- 네트워크 프로토콜의 기본 개념을 이해할 수 있다
- TCP/UDP 소켓 프로그래밍을 구현할 수 있다
- HTTP 클라이언트와 서버를 개발할 수 있다
- 실시간 통신과 WebSocket을 활용할 수 있다

## 네트워크 기초

### TCP 소켓 프로그래밍

```python
import socket
import threading

# TCP 서버
class TCPServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"TCP 서버 시작: {self.host}:{self.port}")
        
        while True:
            client_socket, address = server_socket.accept()
            print(f"클라이언트 연결: {address}")
            
            # 클라이언트 처리
            client_thread = threading.Thread(
                target=self.handle_client, 
                args=(client_socket,)
            )
            client_thread.start()
    
    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                    
                message = data.decode('utf-8')
                print(f"받은 메시지: {message}")
                
                # 에코 응답
                response = f"서버 응답: {message}"
                client_socket.send(response.encode('utf-8'))
                
        except Exception as e:
            print(f"클라이언트 처리 오류: {e}")
        finally:
            client_socket.close()

# TCP 클라이언트
class TCPClient:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        
    def connect_and_send(self, message):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024)
            
            print(f"서버 응답: {response.decode('utf-8')}")
            client_socket.close()
            
        except Exception as e:
            print(f"클라이언트 오류: {e}")

# 사용 예제
if __name__ == "__main__":
    # 서버 시작 (별도 스레드에서)
    server = TCPServer()
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()
    
    import time
    time.sleep(1)  # 서버 시작 대기
    
    # 클라이언트 테스트
    client = TCPClient()
    client.connect_and_send("안녕하세요!")
```

### HTTP 클라이언트

```python
import requests
import json

class HTTPClient:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get(self, url, params=None):
        """GET 요청"""
        full_url = self._build_url(url)
        try:
            response = self.session.get(full_url, params=params)
            return self._handle_response(response)
        except Exception as e:
            return {'error': str(e)}
    
    def post(self, url, data=None, json_data=None):
        """POST 요청"""
        full_url = self._build_url(url)
        try:
            if json_data:
                response = self.session.post(full_url, json=json_data)
            else:
                response = self.session.post(full_url, data=data)
            return self._handle_response(response)
        except Exception as e:
            return {'error': str(e)}
    
    def _build_url(self, url):
        if self.base_url:
            return f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"
        return url
    
    def _handle_response(self, response):
        result = {
            'status_code': response.status_code,
            'headers': dict(response.headers)
        }
        
        try:
            result['data'] = response.json()
        except:
            result['data'] = response.text
            
        return result

# 사용 예제
def http_demo():
    client = HTTPClient('https://httpbin.org')
    
    # GET 요청
    response = client.get('/get', params={'key': 'value'})
    print(f"GET 응답: {response['status_code']}")
    
    # POST 요청
    data = {'name': 'Python', 'version': '3.9'}
    response = client.post('/post', json_data=data)
    print(f"POST 응답: {response['status_code']}")

if __name__ == "__main__":
    http_demo()
```

## 체크리스트

### 네트워크 기초
- [ ] TCP vs UDP 차이점 이해
- [ ] 소켓 프로그래밍 기본 개념
- [ ] HTTP 프로토콜 이해
- [ ] 클라이언트-서버 아키텍처

### 소켓 프로그래밍
- [ ] TCP 소켓 구현
- [ ] 멀티스레딩 활용
- [ ] 에러 처리
- [ ] 연결 관리

### HTTP 통신
- [ ] requests 라이브러리 사용
- [ ] REST API 호출
- [ ] 세션 관리
- [ ] 응답 처리

## 다음 단계

🎉 **축하합니다!** 네트워킹 기초를 마스터했습니다.

이제 [22. 데이터베이스](../22_database/)로 넘어가서 데이터 저장과 관리 기술을 학습해봅시다.

---

💡 **네트워킹 가이드:**
- **TCP는 신뢰성**, **UDP는 속도**
- **에러 처리**를 항상 고려
- **타임아웃** 설정으로 안정성 확보
- **보안**을 염두에 둔 개발 