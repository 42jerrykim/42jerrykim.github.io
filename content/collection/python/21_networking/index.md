---
draft: true
title: "21. 네트워킹"
description: "네트워크 기초(HTTP/TCP)와 파이썬 네트워킹 도구를 개념 중심으로 정리합니다. 요청/응답, 타임아웃, 재시도, 보안(SSL) 같은 실무 기본기를 함께 다룹니다."
tags:
  - Python
  - 파이썬
  - Implementation
  - Software-Architecture
  - Algorithm
  - 알고리즘
  - backend
  - 백엔드
  - Best-Practices
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
  - Performance
  - 성능
  - concurrency
  - 동시성
  - async
  - 비동기
  - oop
  - 객체지향
  - Data-Structures
  - 자료구조
  - DevOps
  - deployment
  - 배포
  - 소프트웨어아키텍처
  - Design-Pattern
  - 디자인패턴
  - web
  - 웹
  - database
  - 데이터베이스
  - networking
  - 네트워킹
  - CI-CD
  - 자동화
  - Documentation
  - 문서화
  - Git
  - Code-Quality
  - 코드품질
lastmod: 2026-01-17
collection_order: 21
---
# 챕터 21: 네트워킹

> "연결된 세상에서 소통하라" - 네트워크 프로그래밍을 통해 전 세계와 연결되는 애플리케이션을 만들어봅시다.

## 학습 목표
- 네트워크 프로토콜의 기본 개념을 이해할 수 있다
- TCP/UDP 소켓 프로그래밍을 구현할 수 있다
- HTTP 클라이언트와 서버를 개발할 수 있다
- 실시간 통신과 WebSocket을 활용할 수 있다

## 핵심 개념(이론)

### 1) 네트워킹의 역할과 경계
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
- 네트워킹는 기능이 아니라 구조/품질을 위한 기반이다.
- 트레이드오프와 실패 모드를 먼저 생각하고, 판단 기준을 남기자.

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
