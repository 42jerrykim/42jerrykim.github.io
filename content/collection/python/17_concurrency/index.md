---
draft: true
title: "17. 동시성 프로그래밍"
description: "멀티스레딩과 멀티프로세싱을 활용한 병렬 처리"
collection_order: 17
---

# 챕터 17: 동시성 프로그래밍

> "동시에 여러 일을 처리하라" - 현대 애플리케이션에서 성능을 극대화하는 핵심 기술입니다.

## 학습 목표
- 동시성과 병렬성의 차이를 이해할 수 있다
- 멀티스레딩과 멀티프로세싱을 적절히 선택할 수 있다
- 스레드와 프로세스 간 통신을 구현할 수 있다
- 동시성 문제를 해결할 수 있다

## 동시성 기본 개념

### 1. 동시성 vs 병렬성

```python
import time
import threading
import multiprocessing

# 순차 실행
def sequential_task():
    print("=== 순차 실행 ===")
    start_time = time.time()
    
    def cpu_bound_task(n):
        result = 0
        for i in range(n):
            result += i * i
        return result
    
    # 4개 작업을 순차적으로 실행
    results = []
    for i in range(4):
        result = cpu_bound_task(1000000)
        results.append(result)
    
    end_time = time.time()
    print(f"순차 실행 시간: {end_time - start_time:.2f}초")
    return results

# 동시 실행 (스레딩) - 동시성
def concurrent_task():
    print("\n=== 동시 실행 (스레딩) ===")
    start_time = time.time()
    
    def cpu_bound_task(n):
        result = 0
        for i in range(n):
            result += i * i
        return result
    
    # 스레드로 실행
    threads = []
    results = [None] * 4
    
    def worker(index, n):
        results[index] = cpu_bound_task(n)
    
    for i in range(4):
        thread = threading.Thread(target=worker, args=(i, 1000000))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"스레딩 실행 시간: {end_time - start_time:.2f}초")
    return results

# 병렬 실행 (프로세싱) - 진정한 병렬성
def parallel_task():
    print("\n=== 병렬 실행 (프로세싱) ===")
    start_time = time.time()
    
    def cpu_bound_task(n):
        result = 0
        for i in range(n):
            result += i * i
        return result
    
    # 프로세스 풀로 실행
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(cpu_bound_task, [1000000] * 4)
    
    end_time = time.time()
    print(f"프로세싱 실행 시간: {end_time - start_time:.2f}초")
    return results

# 성능 비교
if __name__ == "__main__":
    sequential_task()
    concurrent_task()
    parallel_task()
```

### 2. GIL (Global Interpreter Lock) 이해

```python
import threading
import time

# GIL의 영향을 보여주는 예제
def demonstrate_gil():
    print("=== GIL 영향 데모 ===")
    
    # CPU 집약적 작업
    def cpu_intensive():
        total = 0
        for i in range(10000000):
            total += i * i
        return total
    
    # I/O 집약적 작업
    def io_intensive():
        for _ in range(10):
            time.sleep(0.1)  # I/O 대기 시뮬레이션
        return "IO complete"
    
    # CPU 집약적 작업 - 스레딩 vs 순차
    print("\n1. CPU 집약적 작업:")
    
    # 순차 실행
    start = time.time()
    for _ in range(2):
        cpu_intensive()
    sequential_cpu_time = time.time() - start
    print(f"순차 실행: {sequential_cpu_time:.2f}초")
    
    # 스레딩 실행 (GIL 때문에 별로 빨라지지 않음)
    start = time.time()
    threads = []
    for _ in range(2):
        thread = threading.Thread(target=cpu_intensive)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    threading_cpu_time = time.time() - start
    print(f"스레딩 실행: {threading_cpu_time:.2f}초")
    print(f"CPU 작업 성능 개선: {sequential_cpu_time / threading_cpu_time:.2f}배")
    
    # I/O 집약적 작업 - 스레딩 vs 순차
    print("\n2. I/O 집약적 작업:")
    
    # 순차 실행
    start = time.time()
    for _ in range(5):
        io_intensive()
    sequential_io_time = time.time() - start
    print(f"순차 실행: {sequential_io_time:.2f}초")
    
    # 스레딩 실행 (I/O 대기 중 GIL 해제되어 빨라짐)
    start = time.time()
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=io_intensive)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    threading_io_time = time.time() - start
    print(f"스레딩 실행: {threading_io_time:.2f}초")
    print(f"I/O 작업 성능 개선: {sequential_io_time / threading_io_time:.2f}배")

demonstrate_gil()
```

## 멀티스레딩 (threading)

### 1. 기본 스레드 생성과 관리

```python
import threading
import time
import random

class WorkerThread(threading.Thread):
    """커스텀 워커 스레드"""
    
    def __init__(self, thread_id, name, work_time):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.work_time = work_time
    
    def run(self):
        """스레드가 실행할 작업"""
        print(f"스레드 {self.name} 시작")
        for i in range(5):
            print(f"{self.name}: 작업 {i+1}/5 수행 중...")
            time.sleep(self.work_time)
        print(f"스레드 {self.name} 완료")

# 여러 스레드 생성 및 실행
def thread_management_demo():
    print("=== 스레드 관리 데모 ===")
    
    threads = []
    
    # 3개의 워커 스레드 생성
    for i in range(3):
        worker_name = f"Worker-{i+1}"
        work_time = random.uniform(0.5, 1.5)
        thread = WorkerThread(i+1, worker_name, work_time)
        threads.append(thread)
    
    # 모든 스레드 시작
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # 모든 스레드 완료 대기
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"모든 스레드 완료. 총 소요시간: {end_time - start_time:.2f}초")

thread_management_demo()
```

### 2. 스레드 동기화

```python
import threading
import time
import random

# 공유 자원
shared_resource = 0
lock = threading.Lock()

def unsafe_increment():
    """Lock 없는 위험한 증가 함수"""
    global shared_resource
    for _ in range(100000):
        shared_resource += 1

def safe_increment():
    """Lock을 사용한 안전한 증가 함수"""
    global shared_resource
    for _ in range(100000):
        with lock:
            shared_resource += 1

def demonstrate_thread_safety():
    """스레드 안전성 데모"""
    global shared_resource
    
    print("=== 스레드 안전성 데모 ===")
    
    # 1. 위험한 방법 (Race Condition 발생 가능)
    print("\n1. Lock 없이 실행 (Race Condition):")
    shared_resource = 0
    
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=unsafe_increment)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"기대값: 500000, 실제값: {shared_resource}")
    
    # 2. 안전한 방법 (Lock 사용)
    print("\n2. Lock 사용하여 실행:")
    shared_resource = 0
    
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=safe_increment)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"기대값: 500000, 실제값: {shared_resource}")

demonstrate_thread_safety()
```

### 3. 생산자-소비자 패턴

```python
import threading
import queue
import time
import random

def producer_consumer_demo():
    """생산자-소비자 패턴 데모"""
    print("\n=== 생산자-소비자 패턴 ===")
    
    # 작업 큐 (스레드 안전)
    work_queue = queue.Queue(maxsize=10)
    
    # 종료 신호
    shutdown_event = threading.Event()
    
    def producer(name, num_items):
        """생산자 스레드"""
        for i in range(num_items):
            if shutdown_event.is_set():
                break
            
            item = f"{name}-item-{i+1}"
            work_queue.put(item)
            print(f"생산자 {name}: {item} 생산")
            time.sleep(random.uniform(0.1, 0.5))
        
        print(f"생산자 {name} 완료")
    
    def consumer(name):
        """소비자 스레드"""
        while not shutdown_event.is_set():
            try:
                # 1초 timeout으로 아이템 가져오기
                item = work_queue.get(timeout=1)
                print(f"소비자 {name}: {item} 처리 중...")
                time.sleep(random.uniform(0.2, 0.8))
                work_queue.task_done()
                print(f"소비자 {name}: {item} 처리 완료")
            except queue.Empty:
                continue
        
        print(f"소비자 {name} 종료")
    
    # 생산자 스레드들
    producers = []
    for i in range(2):
        producer_thread = threading.Thread(
            target=producer, 
            args=(f"Producer-{i+1}", 5)
        )
        producers.append(producer_thread)
        producer_thread.start()
    
    # 소비자 스레드들
    consumers = []
    for i in range(3):
        consumer_thread = threading.Thread(
            target=consumer,
            args=(f"Consumer-{i+1}",)
        )
        consumers.append(consumer_thread)
        consumer_thread.daemon = True  # 메인 종료 시 같이 종료
        consumer_thread.start()
    
    # 모든 생산자 완료 대기
    for producer_thread in producers:
        producer_thread.join()
    
    # 모든 작업 완료 대기
    work_queue.join()
    
    # 소비자들에게 종료 신호
    shutdown_event.set()
    
    print("생산자-소비자 데모 완료")

producer_consumer_demo()
```

## 멀티프로세싱 (multiprocessing)

### 1. 기본 프로세스 생성

```python
import multiprocessing
import time
import os

def worker_process(name, work_time):
    """워커 프로세스 함수"""
    print(f"프로세스 {name} 시작 (PID: {os.getpid()})")
    
    # CPU 집약적 작업 시뮬레이션
    total = 0
    for i in range(1000000):
        total += i * i
    
    print(f"프로세스 {name} 완료 (PID: {os.getpid()})")
    return total

def multiprocessing_demo():
    """멀티프로세싱 기본 데모"""
    print("=== 멀티프로세싱 데모 ===")
    print(f"메인 프로세스 PID: {os.getpid()}")
    
    # 프로세스 리스트
    processes = []
    
    # 4개의 워커 프로세스 생성
    for i in range(4):
        process = multiprocessing.Process(
            target=worker_process,
            args=(f"Worker-{i+1}", 1)
        )
        processes.append(process)
    
    # 모든 프로세스 시작
    start_time = time.time()
    for process in processes:
        process.start()
    
    # 모든 프로세스 완료 대기
    for process in processes:
        process.join()
    
    end_time = time.time()
    print(f"모든 프로세스 완료. 소요시간: {end_time - start_time:.2f}초")

if __name__ == "__main__":
    multiprocessing_demo()
```

### 2. 프로세스 간 통신

```python
import multiprocessing
import time
import random

def queue_communication():
    """큐를 이용한 프로세스 간 통신"""
    print("\n=== 큐 통신 데모 ===")
    
    def producer_process(queue, name, count):
        """생산자 프로세스"""
        for i in range(count):
            item = f"{name}-item-{i+1}"
            queue.put(item)
            print(f"생산자 {name}: {item} 생산")
            time.sleep(random.uniform(0.1, 0.3))
        
        # 종료 신호
        queue.put(None)
        print(f"생산자 {name} 완료")
    
    def consumer_process(queue, name):
        """소비자 프로세스"""
        while True:
            item = queue.get()
            if item is None:
                break
            
            print(f"소비자 {name}: {item} 처리 중...")
            time.sleep(random.uniform(0.2, 0.5))
            print(f"소비자 {name}: {item} 처리 완료")
        
        print(f"소비자 {name} 완료")
    
    # 큐 생성
    comm_queue = multiprocessing.Queue()
    
    # 프로세스 생성
    producer = multiprocessing.Process(
        target=producer_process,
        args=(comm_queue, "Producer", 5)
    )
    
    consumer = multiprocessing.Process(
        target=consumer_process,
        args=(comm_queue, "Consumer")
    )
    
    # 프로세스 시작
    producer.start()
    consumer.start()
    
    # 완료 대기
    producer.join()
    consumer.join()

def pipe_communication():
    """파이프를 이용한 프로세스 간 통신"""
    print("\n=== 파이프 통신 데모 ===")
    
    def sender_process(conn, name):
        """송신자 프로세스"""
        for i in range(5):
            message = f"Message {i+1} from {name}"
            conn.send(message)
            print(f"송신: {message}")
            time.sleep(0.5)
        
        conn.close()
        print(f"송신자 {name} 완료")
    
    def receiver_process(conn, name):
        """수신자 프로세스"""
        while True:
            try:
                message = conn.recv()
                print(f"수신 by {name}: {message}")
            except EOFError:
                break
        
        print(f"수신자 {name} 완료")
    
    # 파이프 생성
    parent_conn, child_conn = multiprocessing.Pipe()
    
    # 프로세스 생성
    sender = multiprocessing.Process(
        target=sender_process,
        args=(child_conn, "Sender")
    )
    
    receiver = multiprocessing.Process(
        target=receiver_process,
        args=(parent_conn, "Receiver")
    )
    
    # 프로세스 시작
    sender.start()
    receiver.start()
    
    # 완료 대기
    sender.join()
    receiver.join()

if __name__ == "__main__":
    queue_communication()
    pipe_communication()
```

### 3. 프로세스 풀

```python
import multiprocessing
import time
import math

def cpu_intensive_function(n):
    """CPU 집약적 함수"""
    result = 0
    for i in range(n):
        result += math.sqrt(i)
    return result

def process_pool_demo():
    """프로세스 풀 데모"""
    print("\n=== 프로세스 풀 데모 ===")
    
    # 작업 데이터
    work_data = [1000000, 1200000, 800000, 1500000, 900000, 1100000]
    
    # 1. 순차 처리
    print("1. 순차 처리:")
    start_time = time.time()
    sequential_results = [cpu_intensive_function(n) for n in work_data]
    sequential_time = time.time() - start_time
    print(f"순차 처리 시간: {sequential_time:.2f}초")
    
    # 2. 프로세스 풀 처리
    print("\n2. 프로세스 풀 처리:")
    start_time = time.time()
    
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool_results = pool.map(cpu_intensive_function, work_data)
    
    pool_time = time.time() - start_time
    print(f"프로세스 풀 처리 시간: {pool_time:.2f}초")
    print(f"성능 개선: {sequential_time / pool_time:.2f}배")
    
    # 결과 검증
    print(f"결과 일치: {sequential_results == pool_results}")
    
    # 3. 비동기 처리
    print("\n3. 비동기 프로세스 풀:")
    start_time = time.time()
    
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        # 비동기로 작업 제출
        async_results = [pool.apply_async(cpu_intensive_function, (n,)) for n in work_data]
        
        # 결과 수집
        async_final_results = [result.get() for result in async_results]
    
    async_time = time.time() - start_time
    print(f"비동기 처리 시간: {async_time:.2f}초")
    print(f"결과 일치: {sequential_results == async_final_results}")

if __name__ == "__main__":
    process_pool_demo()
```

## concurrent.futures 모듈

### 1. ThreadPoolExecutor와 ProcessPoolExecutor

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time
import requests

def io_bound_task(url):
    """I/O 집약적 작업 (웹 요청)"""
    try:
        response = requests.get(url, timeout=5)
        return f"{url}: {response.status_code}"
    except Exception as e:
        return f"{url}: Error - {str(e)}"

def cpu_bound_task(n):
    """CPU 집약적 작업"""
    total = 0
    for i in range(n * 100000):
        total += i * i
    return total

def concurrent_futures_demo():
    """concurrent.futures 데모"""
    print("=== concurrent.futures 데모 ===")
    
    # 테스트 URL들
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404"
    ]
    
    # 1. ThreadPoolExecutor (I/O 집약적 작업)
    print("\n1. ThreadPoolExecutor (I/O 작업):")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(io_bound_task, url): url for url in urls}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                print(f"결과: {result}")
            except Exception as exc:
                print(f"{url} 오류: {exc}")
    
    thread_time = time.time() - start_time
    print(f"ThreadPool 실행 시간: {thread_time:.2f}초")
    
    # 2. ProcessPoolExecutor (CPU 집약적 작업)
    print("\n2. ProcessPoolExecutor (CPU 작업):")
    cpu_tasks = [10, 15, 8, 12, 20]
    
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=4) as executor:
        future_to_task = {executor.submit(cpu_bound_task, n): n for n in cpu_tasks}
        
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                result = future.result()
                print(f"작업 {task}: 결과 {result}")
            except Exception as exc:
                print(f"작업 {task} 오류: {exc}")
    
    process_time = time.time() - start_time
    print(f"ProcessPool 실행 시간: {process_time:.2f}초")

if __name__ == "__main__":
    concurrent_futures_demo()
```

## 실습 프로젝트

###️ 프로젝트 1: 웹 크롤러 (멀티스레딩)

```python
import threading
import requests
import time
from urllib.parse import urljoin, urlparse
import queue
from collections import defaultdict

class WebCrawler:
    """멀티스레드 웹 크롤러"""
    
    def __init__(self, max_workers=5, max_pages=50):
        self.max_workers = max_workers
        self.max_pages = max_pages
        self.url_queue = queue.Queue()
        self.visited_urls = set()
        self.results = defaultdict(dict)
        self.lock = threading.Lock()
        self.session = requests.Session()
        
        # User-Agent 설정
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def is_valid_url(self, url):
        """유효한 URL인지 확인"""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)
        except:
            return False
    
    def crawl_page(self, url):
        """단일 페이지 크롤링"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # 결과 저장
            page_info = {
                'status_code': response.status_code,
                'content_length': len(response.content),
                'title': self.extract_title(response.text),
                'links_found': len(self.extract_links(response.text, url))
            }
            
            with self.lock:
                self.results[url] = page_info
            
            # 새 링크들을 큐에 추가
            for link in self.extract_links(response.text, url):
                if link not in self.visited_urls and len(self.visited_urls) < self.max_pages:
                    self.url_queue.put(link)
            
            print(f"✓ {url} - {page_info['status_code']} ({page_info['content_length']} bytes)")
            
        except Exception as e:
            with self.lock:
                self.results[url] = {'error': str(e)}
            print(f"✗ {url} - Error: {str(e)}")
    
    def extract_title(self, html):
        """HTML에서 제목 추출 (간단한 방법)"""
        try:
            start = html.find('<title>') + 7
            end = html.find('</title>')
            if start > 6 and end > start:
                return html[start:end].strip()
        except:
            pass
        return "No title"
    
    def extract_links(self, html, base_url):
        """HTML에서 링크 추출 (간단한 방법)"""
        links = []
        try:
            import re
            # href 속성 찾기
            href_pattern = r'href=["\']([^"\']+)["\']'
            matches = re.findall(href_pattern, html)
            
            for match in matches[:10]:  # 최대 10개 링크만
                full_url = urljoin(base_url, match)
                if self.is_valid_url(full_url):
                    links.append(full_url)
        except:
            pass
        return links
    
    def worker(self):
        """워커 스레드 함수"""
        while True:
            try:
                url = self.url_queue.get(timeout=5)
                
                with self.lock:
                    if url in self.visited_urls or len(self.visited_urls) >= self.max_pages:
                        self.url_queue.task_done()
                        continue
                    self.visited_urls.add(url)
                
                self.crawl_page(url)
                self.url_queue.task_done()
                
            except queue.Empty:
                break
    
    def crawl(self, start_urls):
        """크롤링 시작"""
        print(f"웹 크롤러 시작 - 워커: {self.max_workers}, 최대 페이지: {self.max_pages}")
        
        # 시작 URL들을 큐에 추가
        for url in start_urls:
            self.url_queue.put(url)
        
        # 워커 스레드들 시작
        threads = []
        for i in range(self.max_workers):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # 모든 작업 완료 대기
        self.url_queue.join()
        
        return self.results

# 크롤러 사용 예제
def crawler_demo():
    crawler = WebCrawler(max_workers=3, max_pages=10)
    
    start_urls = [
        "https://httpbin.org/",
        "https://python.org/"
    ]
    
    start_time = time.time()
    results = crawler.crawl(start_urls)
    end_time = time.time()
    
    print(f"\n크롤링 완료!")
    print(f"소요 시간: {end_time - start_time:.2f}초")
    print(f"처리된 페이지: {len(results)}")
    
    # 결과 요약
    success_count = sum(1 for result in results.values() if 'error' not in result)
    error_count = len(results) - success_count
    
    print(f"성공: {success_count}, 실패: {error_count}")

if __name__ == "__main__":
    crawler_demo()
```

###️ 프로젝트 2: 이미지 처리 도구 (멀티프로세싱)

```python
import multiprocessing
import os
import time
from PIL import Image
import glob

class ImageProcessor:
    """멀티프로세싱 이미지 처리기"""
    
    def __init__(self, num_processes=None):
        self.num_processes = num_processes or multiprocessing.cpu_count()
    
    @staticmethod
    def resize_image(args):
        """이미지 리사이즈 함수"""
        input_path, output_path, size = args
        
        try:
            with Image.open(input_path) as img:
                # 비율 유지하면서 리사이즈
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # RGB로 변환 (JPEG 저장을 위해)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.save(output_path, 'JPEG', quality=85)
                
            return f"✓ {os.path.basename(input_path)} -> {size}"
            
        except Exception as e:
            return f"✗ {os.path.basename(input_path)}: {str(e)}"
    
    @staticmethod
    def apply_filter(args):
        """이미지 필터 적용"""
        input_path, output_path, filter_type = args
        
        try:
            with Image.open(input_path) as img:
                # RGB 변환
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 필터 적용
                if filter_type == 'grayscale':
                    img = img.convert('L').convert('RGB')
                elif filter_type == 'sepia':
                    # 간단한 세피아 효과
                    pixels = img.load()
                    for i in range(img.width):
                        for j in range(img.height):
                            r, g, b = pixels[i, j]
                            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                            pixels[i, j] = (min(255, tr), min(255, tg), min(255, tb))
                
                img.save(output_path, 'JPEG', quality=85)
                
            return f"✓ {os.path.basename(input_path)} -> {filter_type}"
            
        except Exception as e:
            return f"✗ {os.path.basename(input_path)}: {str(e)}"
    
    @staticmethod
    def create_thumbnail(args):
        """썸네일 생성"""
        input_path, output_path, size = args
        
        try:
            with Image.open(input_path) as img:
                # 정사각형 썸네일 생성
                img = img.convert('RGB')
                
                # 중앙에서 정사각형으로 자르기
                width, height = img.size
                min_dimension = min(width, height)
                
                left = (width - min_dimension) // 2
                top = (height - min_dimension) // 2
                right = left + min_dimension
                bottom = top + min_dimension
                
                img = img.crop((left, top, right, bottom))
                img = img.resize(size, Image.Resampling.LANCZOS)
                
                img.save(output_path, 'JPEG', quality=85)
                
            return f"✓ {os.path.basename(input_path)} -> thumbnail {size}"
            
        except Exception as e:
            return f"✗ {os.path.basename(input_path)}: {str(e)}"
    
    def batch_process(self, input_dir, output_dir, operation, **kwargs):
        """배치 이미지 처리"""
        # 입력 이미지 파일들 찾기
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(input_dir, ext)))
            image_files.extend(glob.glob(os.path.join(input_dir, ext.upper())))
        
        if not image_files:
            print(f"❌ {input_dir}에서 이미지 파일을 찾을 수 없습니다.")
            return
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # 작업 인수 준비
        task_args = []
        for input_file in image_files:
            filename = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(output_dir, f"{filename}_processed.jpg")
            
            if operation == 'resize':
                size = kwargs.get('size', (800, 600))
                task_args.append((input_file, output_file, size))
            elif operation == 'filter':
                filter_type = kwargs.get('filter_type', 'grayscale')
                task_args.append((input_file, output_file, filter_type))
            elif operation == 'thumbnail':
                size = kwargs.get('size', (150, 150))
                task_args.append((input_file, output_file, size))
        
        # 작업 함수 선택
        work_function = {
            'resize': self.resize_image,
            'filter': self.apply_filter,
            'thumbnail': self.create_thumbnail
        }.get(operation)
        
        if not work_function:
            print(f"❌ 알 수 없는 작업: {operation}")
            return
        
        print(f"🚀 {len(task_args)}개 이미지 처리 시작 ({operation})")
        print(f"프로세스 수: {self.num_processes}")
        
        # 멀티프로세싱으로 처리
        start_time = time.time()
        
        with multiprocessing.Pool(processes=self.num_processes) as pool:
            results = pool.map(work_function, task_args)
        
        end_time = time.time()
        
        # 결과 출력
        print(f"\n처리 결과:")
        for result in results:
            print(result)
        
        success_count = sum(1 for r in results if r.startswith('✓'))
        error_count = len(results) - success_count
        
        print(f"\n📊 요약:")
        print(f"처리 시간: {end_time - start_time:.2f}초")
        print(f"성공: {success_count}, 실패: {error_count}")
        print(f"초당 처리: {len(results)/(end_time - start_time):.2f} 이미지/초")

# 사용 예제
def image_processing_demo():
    """이미지 처리 데모"""
    # 데모용 샘플 이미지 생성
    def create_sample_images():
        sample_dir = "sample_images"
        os.makedirs(sample_dir, exist_ok=True)
        
        # PIL로 간단한 테스트 이미지 생성
        colors = ['red', 'green', 'blue', 'yellow', 'purple']
        for i, color in enumerate(colors):
            img = Image.new('RGB', (400, 300), color)
            img.save(os.path.join(sample_dir, f"sample_{i+1}.jpg"))
        
        return sample_dir
    
    # 샘플 이미지 생성
    input_dir = create_sample_images()
    
    # 이미지 프로세서 생성
    processor = ImageProcessor(num_processes=2)
    
    # 1. 리사이즈 작업
    print("=== 이미지 리사이즈 ===")
    processor.batch_process(
        input_dir, 
        "resized_images", 
        "resize", 
        size=(200, 150)
    )
    
    # 2. 필터 적용
    print("\n=== 그레이스케일 필터 ===")
    processor.batch_process(
        input_dir, 
        "filtered_images", 
        "filter", 
        filter_type="grayscale"
    )
    
    # 3. 썸네일 생성
    print("\n=== 썸네일 생성 ===")
    processor.batch_process(
        input_dir, 
        "thumbnails", 
        "thumbnail", 
        size=(100, 100)
    )

if __name__ == "__main__":
    image_processing_demo()
```

## 체크리스트

### 동시성 기본 개념
- [ ] 동시성과 병렬성의 차이점 이해
- [ ] GIL의 영향과 제약사항 파악
- [ ] I/O 바운드 vs CPU 바운드 작업 구분
- [ ] 적절한 동시성 모델 선택 능력

### 멀티스레딩
- [ ] Thread 클래스로 스레드 생성
- [ ] Lock을 사용한 동기화
- [ ] 생산자-소비자 패턴 구현
- [ ] 스레드 안전성 고려

### 멀티프로세싱
- [ ] Process 클래스로 프로세스 생성
- [ ] Queue, Pipe로 프로세스 간 통신
- [ ] ProcessPool을 활용한 병렬처리
- [ ] 공유 메모리 사용

### concurrent.futures
- [ ] ThreadPoolExecutor 활용
- [ ] ProcessPoolExecutor 활용
- [ ] Future 객체 이해
- [ ] as_completed() 패턴 활용

### 동시성 문제 해결
- [ ] Race Condition 방지
- [ ] 데드락 회피
- [ ] 성능 최적화 고려
- [ ] 적절한 워커 수 설정

## 다음 단계

🎉 **축하합니다!** 동시성 프로그래밍을 마스터했습니다.

동시성 처리는 현대 애플리케이션의 성능을 극대화하는 핵심 기술입니다. 이제 [18. 비동기 프로그래밍](../18_async_programming/)으로 넘어가서 더욱 효율적인 비동기 처리 패러다임을 학습해봅시다.

---

💡 **동시성 프로그래밍 가이드:**
- **I/O 작업이 많다면** → 멀티스레딩 또는 비동기 프로그래밍
- **CPU 작업이 많다면** → 멀티프로세싱
- **간단한 병렬처리** → concurrent.futures 사용
- **복잡한 동시성** → threading/multiprocessing 직접 사용
- **성능 측정 필수** → 실제 워크로드로 벤치마킹 