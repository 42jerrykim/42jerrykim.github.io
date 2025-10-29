---
draft: true
title: "18. 비동기 프로그래밍"
description: "asyncio와 이벤트 루프를 활용한 현대적 비동기 처리"
collection_order: 18
---

# 챕터 18: 비동기 프로그래밍

> "Don't wait, be async!" - 현대 애플리케이션의 성능과 확장성을 극대화하는 비동기 프로그래밍의 세계입니다.

## 학습 목표
- 비동기 프로그래밍의 개념과 장점을 이해할 수 있다
- asyncio 모듈의 핵심 개념을 파악할 수 있다
- async/await 문법을 활용할 수 있다
- 비동기 I/O 작업을 효율적으로 처리할 수 있다

## 비동기 프로그래밍 기초

### 1. 동기 vs 비동기 비교

```python
import time
import asyncio

# 동기 방식 - 순차 실행
def sync_fetch_data(name, delay):
    """동기 데이터 가져오기"""
    print(f"{name} 시작")
    time.sleep(delay)  # 블로킹 대기
    print(f"{name} 완료")
    return f"{name} 결과"

def sync_example():
    """동기 방식 데모"""
    print("=== 동기 방식 ===")
    start_time = time.time()
    
    results = []
    results.append(sync_fetch_data("작업1", 2))
    results.append(sync_fetch_data("작업2", 1))
    results.append(sync_fetch_data("작업3", 3))
    
    end_time = time.time()
    print(f"총 소요시간: {end_time - start_time:.2f}초")
    return results

# 비동기 방식 - 동시 실행
async def async_fetch_data(name, delay):
    """비동기 데이터 가져오기"""
    print(f"{name} 시작")
    await asyncio.sleep(delay)  # 논블로킹 대기
    print(f"{name} 완료")
    return f"{name} 결과"

async def async_example():
    """비동기 방식 데모"""
    print("\n=== 비동기 방식 ===")
    start_time = time.time()
    
    # 모든 작업을 동시에 실행
    results = await asyncio.gather(
        async_fetch_data("작업1", 2),
        async_fetch_data("작업2", 1),
        async_fetch_data("작업3", 3)
    )
    
    end_time = time.time()
    print(f"총 소요시간: {end_time - start_time:.2f}초")
    return results

# 성능 비교 실행
if __name__ == "__main__":
    # 동기 방식 (6초 소요)
    sync_results = sync_example()
    
    # 비동기 방식 (3초 소요)
    async_results = asyncio.run(async_example())
```

### 2. 기본 async/await 문법

```python
import asyncio
import time

# 기본 코루틴 정의
async def simple_coroutine():
    """간단한 코루틴"""
    print("코루틴 시작")
    await asyncio.sleep(1)  # 1초 대기 (비동기)
    print("코루틴 완료")
    return "결과값"

# 코루틴 실행 방법들
async def coroutine_examples():
    """코루틴 실행 예제"""
    print("=== 코루틴 실행 방법들 ===")
    
    # 방법 1: await로 직접 실행
    result1 = await simple_coroutine()
    print(f"결과1: {result1}")
    
    # 방법 2: create_task()로 태스크 생성
    task = asyncio.create_task(simple_coroutine())
    result2 = await task
    print(f"결과2: {result2}")
    
    # 방법 3: 여러 코루틴 동시 실행
    results = await asyncio.gather(
        simple_coroutine(),
        simple_coroutine(),
        simple_coroutine()
    )
    print(f"동시 실행 결과: {results}")

# 태스크 관리
async def task_management():
    """태스크 생성과 관리"""
    print("\n=== 태스크 관리 ===")
    
    async def background_task(name, duration):
        print(f"백그라운드 작업 {name} 시작")
        await asyncio.sleep(duration)
        print(f"백그라운드 작업 {name} 완료")
        return f"작업_{name}_결과"
    
    # 여러 태스크 생성
    tasks = [
        asyncio.create_task(background_task("A", 1)),
        asyncio.create_task(background_task("B", 2)),
        asyncio.create_task(background_task("C", 1.5))
    ]
    
    # 다른 작업 수행 중
    print("메인 작업 수행 중...")
    await asyncio.sleep(0.5)
    
    # 모든 태스크 완료 대기
    results = await asyncio.gather(*tasks)
    print(f"모든 태스크 결과: {results}")
    
    # 태스크 상태 확인
    for i, task in enumerate(tasks):
        print(f"태스크 {i}: done={task.done()}, cancelled={task.cancelled()}")

# 실행
async def main():
    await coroutine_examples()
    await task_management()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. 이벤트 루프 이해

```python
import asyncio
import time

class EventLoopDemo:
    """이벤트 루프 데모"""
    
    async def cpu_bound_task(self, name, iterations):
        """CPU 집약적 작업 (비동기에 적합하지 않음)"""
        print(f"CPU 작업 {name} 시작")
        
        total = 0
        for i in range(iterations):
            total += i * i
            
            # 주기적으로 제어권 양보
            if i % 100000 == 0:
                await asyncio.sleep(0)  # 이벤트 루프에 제어권 양보
        
        print(f"CPU 작업 {name} 완료")
        return total
    
    async def io_bound_task(self, name, delay):
        """I/O 집약적 작업 (비동기에 적합)"""
        print(f"I/O 작업 {name} 시작")
        await asyncio.sleep(delay)  # I/O 대기 시뮬레이션
        print(f"I/O 작업 {name} 완료")
        return f"IO_{name}_결과"
    
    async def demonstrate_event_loop(self):
        """이벤트 루프 동작 데모"""
        print("=== 이벤트 루프 동작 ===")
        
        # 현재 이벤트 루프 가져오기
        loop = asyncio.get_running_loop()
        print(f"현재 이벤트 루프: {loop}")
        
        # I/O 집약적 작업들 (효율적)
        print("\n1. I/O 집약적 작업 (비동기에 적합):")
        start_time = time.time()
        
        io_tasks = [
            self.io_bound_task(f"IO{i}", 1) 
            for i in range(3)
        ]
        io_results = await asyncio.gather(*io_tasks)
        
        io_time = time.time() - start_time
        print(f"I/O 작업 시간: {io_time:.2f}초")
        
        # CPU 집약적 작업들 (비효율적)
        print("\n2. CPU 집약적 작업 (비동기에 부적합):")
        start_time = time.time()
        
        cpu_tasks = [
            self.cpu_bound_task(f"CPU{i}", 500000)
            for i in range(2)
        ]
        cpu_results = await asyncio.gather(*cpu_tasks)
        
        cpu_time = time.time() - start_time
        print(f"CPU 작업 시간: {cpu_time:.2f}초")

# 콜백 vs async/await 비교
class CallbackVsAsync:
    """콜백 패턴 vs async/await 비교"""
    
    def callback_example(self):
        """콜백 기반 코드 (복잡함)"""
        print("\n=== 콜백 기반 ===")
        
        def fetch_user(user_id, callback):
            # 네트워크 요청 시뮬레이션
            def on_complete():
                user_data = {"id": user_id, "name": f"User{user_id}"}
                callback(user_data)
            
            # 실제로는 비동기 네트워크 요청
            asyncio.get_event_loop().call_later(1, on_complete)
        
        def fetch_posts(user_id, callback):
            def on_complete():
                posts = [f"Post{i} by User{user_id}" for i in range(3)]
                callback(posts)
            
            asyncio.get_event_loop().call_later(1, on_complete)
        
        def process_user_data(user_data):
            print(f"사용자 정보: {user_data}")
            
            # 콜백 지옥 시작...
            def on_posts_fetched(posts):
                print(f"사용자 포스트: {posts}")
                # 더 깊은 중첩 필요시...
            
            fetch_posts(user_data["id"], on_posts_fetched)
        
        fetch_user(123, process_user_data)
    
    async def async_example(self):
        """async/await 기반 코드 (깔끔함)"""
        print("\n=== async/await 기반 ===")
        
        async def fetch_user(user_id):
            await asyncio.sleep(1)  # 네트워크 요청 시뮬레이션
            return {"id": user_id, "name": f"User{user_id}"}
        
        async def fetch_posts(user_id):
            await asyncio.sleep(1)  # 네트워크 요청 시뮬레이션
            return [f"Post{i} by User{user_id}" for i in range(3)]
        
        # 깔끔한 순차 처리
        user_data = await fetch_user(123)
        print(f"사용자 정보: {user_data}")
        
        posts = await fetch_posts(user_data["id"])
        print(f"사용자 포스트: {posts}")
        
        # 또는 동시 처리
        user_data, posts = await asyncio.gather(
            fetch_user(456),
            fetch_posts(456)
        )
        print(f"동시 처리 결과: {user_data}, {posts}")

# 실행
async def main():
    demo = EventLoopDemo()
    await demo.demonstrate_event_loop()
    
    callback_demo = CallbackVsAsync()
    callback_demo.callback_example()
    await asyncio.sleep(3)  # 콜백 완료 대기
    
    await callback_demo.async_example()

if __name__ == "__main__":
    asyncio.run(main())
```

## asyncio 핵심 기능

### 1. 동시 실행 패턴

```python
import asyncio
import random
import time

class AsyncPatterns:
    """비동기 패턴 모음"""
    
    async def gather_pattern(self):
        """asyncio.gather() 패턴 - 모든 결과 한번에"""
        print("=== gather 패턴 ===")
        
        async def fetch_data(name, delay):
            await asyncio.sleep(delay)
            return f"{name} 완료 ({delay}초)"
        
        start_time = time.time()
        
        # 모든 작업을 동시에 실행하고 모든 결과 대기
        results = await asyncio.gather(
            fetch_data("빠른작업", 1),
            fetch_data("중간작업", 2),
            fetch_data("느린작업", 3)
        )
        
        end_time = time.time()
        print(f"gather 실행 시간: {end_time - start_time:.2f}초")
        print(f"결과: {results}")
    
    async def as_completed_pattern(self):
        """asyncio.as_completed() 패턴 - 완료순 처리"""
        print("\n=== as_completed 패턴 ===")
        
        async def random_task(name):
            delay = random.uniform(1, 3)
            await asyncio.sleep(delay)
            return f"{name} 완료 ({delay:.1f}초)"
        
        tasks = [
            random_task("작업1"),
            random_task("작업2"),
            random_task("작업3"),
            random_task("작업4")
        ]
        
        # 완료되는 순서대로 결과 처리
        print("완료되는 순서대로 처리:")
        for future in asyncio.as_completed(tasks):
            result = await future
            print(f"  {result}")
    
    async def wait_pattern(self):
        """asyncio.wait() 패턴 - 조건부 대기"""
        print("\n=== wait 패턴 ===")
        
        async def worker(name, duration):
            await asyncio.sleep(duration)
            return f"작업자_{name}"
        
        tasks = [
            asyncio.create_task(worker(f"W{i}", i)) 
            for i in range(1, 5)
        ]
        
        # 첫 번째 작업 완료까지만 기다리기
        done, pending = await asyncio.wait(
            tasks, 
            return_when=asyncio.FIRST_COMPLETED
        )
        
        print(f"완료된 작업 수: {len(done)}")
        print(f"대기 중인 작업 수: {len(pending)}")
        
        # 완료된 작업 결과 확인
        for task in done:
            result = await task
            print(f"첫 완료 작업: {result}")
        
        # 나머지 작업들 취소 또는 완료 대기
        choice = "완료"  # 또는 "취소"
        
        if choice == "취소":
            for task in pending:
                task.cancel()
            print("나머지 작업들 취소됨")
        else:
            print("나머지 작업들도 완료 대기 중...")
            remaining_results = await asyncio.gather(*pending)
            print(f"나머지 결과: {remaining_results}")
    
    async def timeout_pattern(self):
        """타임아웃 패턴"""
        print("\n=== 타임아웃 패턴 ===")
        
        async def slow_task(name, duration):
            print(f"{name} 시작 ({duration}초 소요 예정)")
            await asyncio.sleep(duration)
            return f"{name} 완료"
        
        # 성공 사례
        try:
            result = await asyncio.wait_for(
                slow_task("빠른작업", 1), 
                timeout=2.0
            )
            print(f"성공: {result}")
        except asyncio.TimeoutError:
            print("빠른작업 타임아웃!")
        
        # 타임아웃 사례
        try:
            result = await asyncio.wait_for(
                slow_task("느린작업", 3), 
                timeout=2.0
            )
            print(f"성공: {result}")
        except asyncio.TimeoutError:
            print("느린작업 타임아웃!")
    
    async def shield_pattern(self):
        """asyncio.shield() 패턴 - 취소 방지"""
        print("\n=== shield 패턴 ===")
        
        async def critical_task():
            print("중요한 작업 시작")
            await asyncio.sleep(3)
            print("중요한 작업 완료")
            return "중요한 결과"
        
        async def main_task():
            # 중요한 작업을 shield로 보호
            shielded = asyncio.shield(critical_task())
            
            try:
                # 1초 후 타임아웃 (하지만 shield된 작업은 계속)
                result = await asyncio.wait_for(shielded, timeout=1.0)
                return result
            except asyncio.TimeoutError:
                print("메인 작업 타임아웃, 하지만 중요한 작업은 계속 실행")
                # shield된 작업은 백그라운드에서 계속 실행됨
                return await shielded
        
        result = await main_task()
        print(f"최종 결과: {result}")

# 실행
async def main():
    patterns = AsyncPatterns()
    await patterns.gather_pattern()
    await patterns.as_completed_pattern()
    await patterns.wait_pattern()
    await patterns.timeout_pattern()
    await patterns.shield_pattern()

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. 비동기 컨텍스트 매니저와 큐

```python
import asyncio
import aiofiles
import json
from contextlib import asynccontextmanager

# 비동기 컨텍스트 매니저
class AsyncResource:
    """비동기 리소스 관리"""
    
    def __init__(self, name):
        self.name = name
        self.is_connected = False
    
    async def __aenter__(self):
        print(f"{self.name} 리소스 연결 중...")
        await asyncio.sleep(0.1)  # 연결 시뮬레이션
        self.is_connected = True
        print(f"{self.name} 리소스 연결 완료")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"{self.name} 리소스 정리 중...")
        await asyncio.sleep(0.1)  # 정리 시뮬레이션
        self.is_connected = False
        print(f"{self.name} 리소스 정리 완료")
        return False
    
    async def do_work(self):
        if not self.is_connected:
            raise RuntimeError("리소스가 연결되지 않음")
        print(f"{self.name}에서 작업 수행")
        await asyncio.sleep(1)
        return f"{self.name} 작업 결과"

@asynccontextmanager
async def async_context_demo():
    """비동기 컨텍스트 매니저 데코레이터 예제"""
    print("컨텍스트 진입")
    resource = "임시 리소스"
    try:
        yield resource
    finally:
        print("컨텍스트 정리")
        await asyncio.sleep(0.1)

# 비동기 큐 패턴
class AsyncQueueDemo:
    """비동기 큐 데모"""
    
    def __init__(self):
        self.queue = asyncio.Queue(maxsize=5)
    
    async def producer(self, name, count):
        """생산자"""
        for i in range(count):
            item = f"{name}_item_{i}"
            await self.queue.put(item)
            print(f"생산자 {name}: {item} 생산")
            await asyncio.sleep(0.5)
        print(f"생산자 {name} 완료")
    
    async def consumer(self, name):
        """소비자"""
        while True:
            try:
                item = await asyncio.wait_for(
                    self.queue.get(), 
                    timeout=2.0
                )
                print(f"소비자 {name}: {item} 처리 중...")
                await asyncio.sleep(1)
                print(f"소비자 {name}: {item} 처리 완료")
                self.queue.task_done()
            except asyncio.TimeoutError:
                print(f"소비자 {name} 타임아웃으로 종료")
                break
    
    async def run_demo(self):
        """큐 데모 실행"""
        print("=== 비동기 큐 데모 ===")
        
        # 생산자와 소비자 동시 실행
        await asyncio.gather(
            self.producer("P1", 3),
            self.producer("P2", 2), 
            self.consumer("C1"),
            self.consumer("C2")
        )
        
        # 모든 아이템 처리 완료 대기
        await self.queue.join()
        print("모든 아이템 처리 완료")

# 비동기 파일 I/O
async def async_file_demo():
    """비동기 파일 I/O 데모"""
    print("\n=== 비동기 파일 I/O ===")
    
    # 비동기 파일 쓰기
    async with aiofiles.open('async_test.txt', 'w', encoding='utf-8') as f:
        await f.write("비동기로 작성된 첫 번째 줄\n")
        await f.write("비동기로 작성된 두 번째 줄\n")
        await f.write("비동기로 작성된 세 번째 줄\n")
    
    print("파일 쓰기 완료")
    
    # 비동기 파일 읽기
    async with aiofiles.open('async_test.txt', 'r', encoding='utf-8') as f:
        contents = await f.read()
        print(f"파일 내용:\n{contents}")
    
    # 비동기 JSON 처리
    data = {
        "name": "비동기 데이터",
        "items": ["아이템1", "아이템2", "아이템3"],
        "timestamp": "2024-01-01"
    }
    
    async with aiofiles.open('async_data.json', 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=2))
    
    async with aiofiles.open('async_data.json', 'r', encoding='utf-8') as f:
        json_content = await f.read()
        loaded_data = json.loads(json_content)
        print(f"JSON 데이터: {loaded_data}")

# 실행
async def main():
    # 비동기 컨텍스트 매니저
    print("=== 비동기 컨텍스트 매니저 ===")
    async with AsyncResource("DB커넥션") as resource:
        result = await resource.do_work()
        print(f"결과: {result}")
    
    # 데코레이터 방식
    async with async_context_demo() as resource:
        print(f"컨텍스트에서 작업: {resource}")
    
    # 비동기 큐
    queue_demo = AsyncQueueDemo()
    await queue_demo.run_demo()
    
    # 비동기 파일 I/O
    await async_file_demo()

if __name__ == "__main__":
    asyncio.run(main())
```

## 체크리스트

### 비동기 프로그래밍 기본
- [ ] 동기 vs 비동기 차이점 이해
- [ ] async/await 문법 숙달
- [ ] 이벤트 루프 개념 파악
- [ ] 코루틴과 태스크 구분

### asyncio 핵심 기능
- [ ] asyncio.gather() 활용
- [ ] asyncio.wait() 패턴 이해
- [ ] 타임아웃 처리 방법
- [ ] 비동기 컨텍스트 매니저 사용

### 비동기 I/O
- [ ] aiofiles로 파일 I/O
- [ ] 비동기 네트워킹 구현
- [ ] 큐를 이용한 생산자-소비자 패턴
- [ ] 동기화 도구 활용

### 고급 패턴
- [ ] as_completed() 패턴
- [ ] shield()로 취소 방지
- [ ] 에러 처리와 복구
- [ ] 성능 최적화 고려

### 실무 적용
- [ ] 웹 크롤링 구현
- [ ] API 클라이언트 개발
- [ ] 실시간 데이터 처리
- [ ] 백그라운드 작업 관리

## 다음 단계

🎉 **축하합니다!** 비동기 프로그래밍을 마스터했습니다.

비동기 프로그래밍은 현대 웹 애플리케이션과 마이크로서비스의 핵심 기술입니다. 이제 [19. 성능 최적화](../19_performance_optimization/)로 넘어가서 파이썬 애플리케이션의 성능을 극한까지 끌어올리는 기법을 학습해봅시다.

---

💡 **비동기 프로그래밍 가이드:**
- **I/O 중심 애플리케이션**에서 최대 효과
- **동시 연결 수가 많을 때** 메모리 효율적
- **await 키워드**를 빼먹지 말 것
- **blocking 함수**는 executor로 처리
- **에러 처리**를 철저히 할 것