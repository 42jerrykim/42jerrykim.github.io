---
draft: false
image: "wordcloud.png"
title: "[Python Master] 21. 네트워킹 - HTTP/TCP/소켓 프로그래밍"
slug: "python-networking-http-tcp-socket-programming-guide"
description: "네트워크 기초(HTTP/TCP)와 파이썬 네트워킹 도구를 개념 중심으로 정리합니다. 요청/응답, 타임아웃, 재시도, 보안(SSL) 같은 실무 기본기를 함께 다룹니다."
tags:
  - Python
  - Implementation(구현)
  - Software-Architecture(소프트웨어아키텍처)
  - Algorithm(알고리즘)
  - Backend(백엔드)
  - Best-Practices
  - Clean-Code(클린코드)
  - Refactoring(리팩토링)
  - Testing(테스트)
  - Debugging(디버깅)
  - Logging(로깅)
  - Security(보안)
  - Performance(성능)
  - Concurrency(동시성)
  - Async(비동기)
  - OOP(객체지향)
  - Data-Structures(자료구조)
  - DevOps
  - Deployment(배포)
  - Design-Pattern(디자인패턴)
  - Web(웹)
  - Database(데이터베이스)
  - Networking(네트워킹)
  - CI-CD(Continuous Integration/Continuous Deployment)
  - Automation(자동화)
  - Documentation(문서화)
  - Git
  - Code-Quality(코드품질)
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
따라서 이 주제는 기능이 아니라 <strong>품질(신뢰성/유지보수성/보안)</strong>을 위한 기반으로 이해해야 합니다.

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

소켓(socket)은 운영체제가 제공하는 네트워크 통신의 최소 단위 추상화로, IP 주소와 포트 번호로 식별되는 통신 종단점(endpoint)입니다. 파이썬의 `socket` 모듈은 BSD 소켓 API를 거의 그대로 감싼 저수준 인터페이스이며, `requests`나 웹 프레임워크 같은 상위 도구들도 결국 이 계층 위에서 동작합니다. TCP(Transmission Control Protocol)는 3-way handshake로 연결을 맺고 순서 보장과 재전송으로 신뢰성을 확보하는 대신 UDP보다 지연이 크고, UDP는 그 반대로 순서·도달을 보장하지 않는 대신 오버헤드가 작습니다. 아래 예제는 `socket.SOCK_STREAM`(TCP)으로 연결을 맺고 클라이언트가 보낸 메시지를 그대로 돌려주는 에코 서버/클라이언트를 스레드 기반으로 구현합니다. 여러 클라이언트를 동시에 받으려면 연결마다 별도 스레드로 처리해야 하며, 이는 [17장: 동시성](/post/python/python-concurrency-threading-multiprocessing-gil-guide/)에서 다룬 스레딩 모델을 그대로 활용한 것입니다.

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

이 예제는 메시지 경계를 `recv(1024)` 한 번의 호출로 가정하지만, TCP는 스트림 프로토콜이라 실제로는 한 메시지가 여러 번에 나뉘어 도착하거나 여러 메시지가 한 번의 `recv`에 합쳐져 도착할 수 있습니다. 실무에서는 길이 프리픽스나 구분자(`\n` 등)로 메시지 경계를 애플리케이션이 직접 설계해야 하며, TCP 자체는 이 경계를 보장하지 않습니다.

### HTTP 클라이언트: requests

HTTP 클라이언트는 소켓을 직접 다루는 대신 요청/응답 모델을 추상화해 개발 생산성을 높입니다. 파이썬 표준 라이브러리에는 `urllib.request`가 있지만, 실무에서는 더 간결한 API와 커넥션 풀링, 세션 재사용을 제공하는 서드파티 `requests` 라이브러리를 널리 사용합니다. `requests`를 쓸 때 반드시 챙겨야 할 세 가지는 헤더(headers)로 요청 메타데이터(User-Agent, 인증 토큰 등)를 지정하는 것, `timeout`을 명시적으로 설정해 응답이 오지 않는 상황에서 무한 대기를 막는 것, 그리고 `requests.exceptions`의 구체적인 예외(`Timeout`, `ConnectionError`, `HTTPError`)를 구분해 처리하는 것입니다. `timeout`을 생략하면 기본값이 없어 서버가 응답하지 않을 때 프로그램이 사실상 영원히 멈출 수 있다는 점이 실무에서 가장 흔한 실수입니다.

```python
import requests

class HTTPClient:
    """헤더, 타임아웃, 예외 처리를 갖춘 HTTP 클라이언트 래퍼"""

    def __init__(self, base_url=None, default_timeout=5, default_headers=None):
        self.base_url = base_url
        self.default_timeout = default_timeout
        self.session = requests.Session()
        if default_headers:
            self.session.headers.update(default_headers)

    def get(self, path, params=None, headers=None, timeout=None):
        url = self._build_url(path)
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout or self.default_timeout,
            )
            response.raise_for_status()
            return self._parse(response)
        except requests.exceptions.Timeout:
            return {'error': 'timeout', 'url': url}
        except requests.exceptions.ConnectionError:
            return {'error': 'connection_failed', 'url': url}
        except requests.exceptions.HTTPError as exc:
            return {'error': 'http_error', 'status_code': exc.response.status_code}

    def post(self, path, data=None, json_data=None, headers=None, timeout=None):
        url = self._build_url(path)
        try:
            response = self.session.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout or self.default_timeout,
            )
            response.raise_for_status()
            return self._parse(response)
        except requests.exceptions.Timeout:
            return {'error': 'timeout', 'url': url}
        except requests.exceptions.ConnectionError:
            return {'error': 'connection_failed', 'url': url}
        except requests.exceptions.HTTPError as exc:
            return {'error': 'http_error', 'status_code': exc.response.status_code}

    def _build_url(self, path):
        if self.base_url:
            return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        return path

    def _parse(self, response):
        try:
            data = response.json()
        except ValueError:
            data = response.text
        return {'status_code': response.status_code, 'data': data}


# 사용 예제
if __name__ == "__main__":
    client = HTTPClient(
        'https://httpbin.org',
        default_headers={'User-Agent': 'python-networking-chapter/1.0'},
    )

    result = client.get('/get', params={'key': 'value'})
    print(f"GET 응답: {result['status_code']}")

    result = client.post('/post', json_data={'name': 'Python', 'version': '3.12'})
    print(f"POST 응답: {result['status_code']}")
```

`raise_for_status()`는 4xx/5xx 응답을 예외로 승격시켜 상태 코드를 매번 수동으로 확인하지 않아도 되게 해 줍니다. 이 코드처럼 `Timeout`, `ConnectionError`, `HTTPError`를 개별적으로 잡으면 호출자가 실패 원인(응답이 늦었는지, 연결 자체가 안 됐는지, 서버가 오류를 반환했는지)을 구분해 재시도 여부를 판단할 수 있습니다. 원인을 뭉뚱그려 `except Exception`으로 처리하면 디버깅 시 원인 파악이 어려워지고, 재시도해서는 안 되는 오류(예: 400 Bad Request)까지 무한 재시도하는 버그로 이어지기 쉽습니다. 예외 처리 자체의 설계 원칙은 [7장: 예외 처리](/post/python/python-exception-handling-try-except-finally-custom-errors-guide/)를 참고하십시오.

### 타임아웃과 재시도 전략

네트워크 호출이 실패하는 이유는 대부분 일시적입니다. DNS 지연, 순간적인 패킷 손실, 서버의 일시적 과부하는 몇 초 뒤 재시도하면 성공하는 경우가 많습니다. 문제는 "언제 포기하고 재시도할 것인가"인데, 타임아웃 없이 무작정 기다리면 스레드나 커넥션이 계속 묶여 있다가 시스템 전체의 처리량이 떨어지고, 반대로 실패 즉시 재시도하면 이미 과부하 상태인 서버에 요청을 더 쏟아부어 상황을 악화시킬 수 있습니다(이른바 thundering herd). 그래서 실무에서는 지수 백오프(exponential backoff)와 약간의 무작위 지연(jitter)을 조합해 재시도 간격을 점점 늘리며, 멱등(idempotent)하지 않은 요청(예: 결제 POST)은 재시도 여부 자체를 신중히 설계해야 합니다. `requests`는 `urllib3.util.Retry`와 `HTTPAdapter`를 세션에 장착해 이 전략을 선언적으로 적용할 수 있습니다.

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def build_session_with_retry(total_retries=3, backoff_factor=0.5):
    """일시적 오류(5xx, 연결 오류)에 지수 백오프로 재시도하는 세션 생성"""
    retry_strategy = Retry(
        total=total_retries,
        backoff_factor=backoff_factor,  # 대기 시간 = backoff_factor * (2 ** (재시도 횟수 - 1))
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=['GET', 'HEAD', 'OPTIONS'],  # 멱등 메서드만 자동 재시도
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)

    session = requests.Session()
    session.mount('https://', adapter)
    session.mount('http://', adapter)
    return session


if __name__ == "__main__":
    session = build_session_with_retry()
    response = session.get('https://httpbin.org/status/503', timeout=5)
    print(response.status_code)
```

`allowed_methods`를 GET/HEAD/OPTIONS로 제한한 것은 POST처럼 부수 효과가 있는 요청을 자동으로 재시도하면 같은 작업이 중복 실행될 위험이 있기 때문입니다. POST를 안전하게 재시도하려면 서버가 idempotency key 같은 멱등성 보장 메커니즘을 지원해야 합니다.

### HTTP 서버 만들기: http.server와 socketserver

`requests`가 클라이언트 쪽 추상화라면, `http.server`와 `socketserver`는 파이썬 표준 라이브러리가 제공하는 서버 쪽 최소 도구입니다. 이 둘은 실무용 프로덕션 서버(Flask, FastAPI 등은 [23장: 웹 개발](/post/python/python-web-development-flask-django-rest-api-guide/)에서 다룹니다)를 대체하려는 것이 아니라, 클라이언트 코드를 테스트할 목(mock) 서버를 빠르게 띄우거나 로컬 파일을 임시로 공유할 때 유용합니다. `http.server.BaseHTTPRequestHandler`를 상속해 `do_GET`, `do_POST` 같은 메서드를 오버라이드하면 요청 메서드별 처리를 정의할 수 있고, `socketserver.ThreadingMixIn`을 함께 사용하면 요청마다 별도 스레드에서 처리해 한 클라이언트가 서버를 독점하는 상황을 막을 수 있습니다.

```python
import json
from http.server import BaseHTTPRequestHandler
from socketserver import ThreadingMixIn, TCPServer


class EchoAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({'path': self.path, 'method': 'GET'}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(length)
        try:
            payload = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        response_body = json.dumps({'received': payload}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        pass  # 콘솔 출력을 줄이기 위해 접근 로그를 끔


class ThreadingHTTPServer(ThreadingMixIn, TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    server = ThreadingHTTPServer(('localhost', 8000), EchoAPIHandler)
    print("서버 시작: http://localhost:8000")
    server.serve_forever()
```

`Content-Length` 헤더를 정확히 계산해 보내지 않으면 클라이언트가 응답 본문을 어디까지 읽어야 할지 몰라 연결이 멈춘 것처럼 보일 수 있습니다. `do_POST`에서 `Content-Length`만큼만 `rfile.read()`로 읽는 것도 같은 이유이며, 이 값을 무시하고 무작정 읽으면 클라이언트가 연결을 끊을 때까지 블로킹됩니다.

### HTTPS와 TLS, 인증서 검증

HTTP 통신은 평문으로 오가기 때문에 중간자(man-in-the-middle)가 내용을 읽거나 조작할 수 있습니다. HTTPS는 TCP 위에 TLS(Transport Layer Security) 계층을 추가해 이 문제를 해결하는데, 클라이언트와 서버는 TLS handshake 과정에서 서버 인증서를 검증하고 대칭키를 교환한 뒤 이후 통신을 암호화합니다. 여기서 핵심은 인증서 검증입니다. 클라이언트가 신뢰할 수 있는 CA(Certificate Authority)가 서버 인증서에 서명했는지 확인하지 않으면, 공격자가 자신을 서버인 것처럼 위장해도 클라이언트가 이를 구분하지 못합니다. `requests`는 기본적으로 `verify=True`로 인증서를 검증하며, 사설 인증서를 쓰는 사내망 테스트 환경이 아닌 이상 `verify=False`로 이 검증을 끄는 것은 강하게 지양해야 합니다. 이는 TLS가 막으려는 공격을 그대로 열어주는 것과 같습니다. 저수준 `socket` 코드에서 TLS를 적용하려면 `ssl.create_default_context()`로 시스템 신뢰 저장소 기반의 컨텍스트를 만들고 `wrap_socket()`으로 소켓을 감싸면 됩니다.

```python
import socket
import ssl

def fetch_tls_certificate_info(host, port=443):
    """TLS handshake 후 서버 인증서 정보를 확인하는 예제"""
    context = ssl.create_default_context()  # 시스템 CA 저장소로 인증서를 검증

    with socket.create_connection((host, port), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=host) as tls_sock:
            cert = tls_sock.getpeercert()
            return {
                'subject': dict(x[0] for x in cert['subject']),
                'issuer': dict(x[0] for x in cert['issuer']),
                'notAfter': cert['notAfter'],
            }


if __name__ == "__main__":
    info = fetch_tls_certificate_info('www.python.org')
    print(info)
```

`server_hostname` 인자는 SNI(Server Name Indication)에 쓰이는 동시에, 반환된 인증서의 이름이 실제로 이 호스트와 일치하는지 검증하는 데도 사용됩니다. `verify=False`나 `context.check_hostname = False`처럼 검증을 비활성화하는 코드를 개발 중 임시로 추가했다가 프로덕션에 그대로 남기면, 편의를 위해 켰던 예외 설정이 보안 구멍으로 굳어버리는 경우가 흔합니다.

## 실습 프로젝트

### 프로젝트 1: URL 상태 점검 도구

이 프로젝트는 앞서 다룬 세션 재사용, 타임아웃, 재시도 전략을 하나의 점검 도구로 묶습니다. 여러 URL의 상태 코드와 응답 시간을 확인하고, 실패한 URL은 원인(타임아웃/연결 실패/기타 오류)을 구분해 보고합니다.

```python
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class URLHealthChecker:
    def __init__(self, timeout=5, retries=2):
        self.timeout = timeout
        retry_strategy = Retry(
            total=retries,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=['GET'],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount('https://', adapter)
        self.session.mount('http://', adapter)

    def check(self, url):
        start = time.monotonic()
        try:
            response = self.session.get(url, timeout=self.timeout)
            elapsed_ms = (time.monotonic() - start) * 1000
            return {
                'url': url,
                'ok': response.ok,
                'status_code': response.status_code,
                'elapsed_ms': round(elapsed_ms, 1),
            }
        except requests.exceptions.Timeout:
            return {'url': url, 'ok': False, 'error': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'url': url, 'ok': False, 'error': 'connection_failed'}
        except requests.exceptions.RequestException as exc:
            return {'url': url, 'ok': False, 'error': str(exc)}

    def check_all(self, urls):
        return [self.check(url) for url in urls]


def print_report(results):
    for result in results:
        if result['ok']:
            print(f"[OK]   {result['url']} - {result['status_code']} ({result['elapsed_ms']}ms)")
        else:
            reason = result.get('error', result.get('status_code'))
            print(f"[FAIL] {result['url']} - {reason}")


if __name__ == "__main__":
    urls = [
        'https://httpbin.org/status/200',
        'https://httpbin.org/status/500',
        'https://httpbin.org/delay/1',
    ]
    checker = URLHealthChecker(timeout=3, retries=1)
    print_report(checker.check_all(urls))
```

이 도구는 URL을 하나씩 순차적으로 점검하므로 목록이 길어지면 느려집니다. [18장: 비동기 프로그래밍](/post/python/python-async-programming-asyncio-async-await-event-loop-guide/)의 `asyncio`나 [17장: 동시성](/post/python/python-concurrency-threading-multiprocessing-gil-guide/)의 스레드 풀을 적용하면 여러 URL을 동시에 점검하도록 확장할 수 있습니다.

### 프로젝트 2: 스레드 기반 TCP 에코 서버와 자동 검증 클라이언트

두 번째 프로젝트는 소켓 기초에서 다룬 에코 서버를 `socketserver.ThreadingTCPServer`로 다시 구성하고, 서버가 실제로 정확히 응답하는지 클라이언트 쪽에서 자동으로 검증합니다. `socketserver`를 쓰면 연결 수락, 스레드 생성 같은 반복적인 코드를 프레임워크가 대신 처리해 주므로 핸들러 클래스만 작성하면 됩니다.

```python
import socket
import threading
import time
from socketserver import BaseRequestHandler, ThreadingTCPServer


class EchoHandler(BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            self.request.sendall(data)  # 받은 그대로 되돌려 보냄


def run_server(host='localhost', port=9090):
    server = ThreadingTCPServer((host, port), EchoHandler)
    server.daemon_threads = True
    server.allow_reuse_address = True
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def verify_echo(host='localhost', port=9090, messages=None):
    messages = messages or ['hello', 'python networking', 'done']
    with socket.create_connection((host, port), timeout=3) as sock:
        for message in messages:
            sock.sendall(message.encode('utf-8'))
            response = sock.recv(1024).decode('utf-8')
            assert response == message, f"불일치: 보낸 값={message!r}, 받은 값={response!r}"
            print(f"검증 성공: {message!r}")


if __name__ == "__main__":
    server = run_server()
    time.sleep(0.2)  # 서버 스레드가 accept 루프에 진입할 시간을 확보
    try:
        verify_echo()
    finally:
        server.shutdown()
```

이 검증 스크립트는 별도 테스트 프레임워크 없이 `assert`만으로 서버 동작을 확인합니다. 실제 프로젝트라면 [24장: 테스트와 디버깅](/post/python/python-testing-debugging-pytest-tdd-mocking-guide/)에서 다루는 `pytest` 같은 도구로 이 검증 로직을 정식 테스트 케이스로 옮기는 것이 좋습니다.

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

### 안정성과 보안
- [ ] 타임아웃과 재시도(백오프) 전략 구분
- [ ] http.server/socketserver로 간단한 서버 구현
- [ ] TLS 인증서 검증의 필요성 이해

## 다음 단계

🎉 **축하합니다!** 네트워킹 기초를 마스터했습니다.

이제 [22. 데이터베이스](/post/python/python-database-sql-nosql-orm-transaction-guide/)로 넘어가서 데이터 저장과 관리 기술을 학습해봅시다.

---

💡 **네트워킹 가이드:**
- **TCP는 신뢰성**, **UDP는 속도**
- **에러 처리**를 항상 고려
- **타임아웃** 설정으로 안정성 확보
- **보안**을 염두에 둔 개발 
