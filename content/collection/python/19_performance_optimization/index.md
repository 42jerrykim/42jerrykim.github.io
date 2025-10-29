---
draft: true
title: "19. 성능 최적화"
description: "파이썬 코드의 성능을 측정하고 최적화하는 기법들"
collection_order: 19
---

# 챕터 19: 성능 최적화

> "측정하지 않으면 최적화할 수 없다" - 성능 병목을 찾아내고 효율적인 파이썬 코드를 작성해봅시다.

## 학습 목표
- 성능 병목 지점을 식별하고 측정할 수 있다
- 다양한 최적화 기법을 적용할 수 있다
- 프로파일링 도구를 효과적으로 사용할 수 있다
- 성능과 가독성의 균형을 맞출 수 있다

## 성능 측정과 프로파일링

### 기본 성능 측정

```python
import time
import timeit
from functools import wraps

# 시간 측정 데코레이터
def measure_time(func):
    """함수 실행 시간을 측정하는 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"{func.__name__}: {end_time - start_time:.6f}초")
        return result
    return wrapper

# 벤치마킹 클래스
class PerformanceBenchmark:
    """성능 벤치마크 도구"""
    
    def __init__(self):
        self.results = {}
    
    def time_function(self, func, *args, **kwargs):
        """함수 실행 시간 측정"""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        func_name = func.__name__
        
        if func_name not in self.results:
            self.results[func_name] = []
        self.results[func_name].append(execution_time)
        
        return result, execution_time
    
    def timeit_function(self, func, number=1000, *args, **kwargs):
        """timeit을 사용한 정확한 측정"""
        def wrapper():
            return func(*args, **kwargs)
        
        execution_time = timeit.timeit(wrapper, number=number) / number
        func_name = func.__name__
        
        if func_name not in self.results:
            self.results[func_name] = []
        self.results[func_name].append(execution_time)
        
        return execution_time
    
    def compare_functions(self, functions, *args, **kwargs):
        """여러 함수의 성능 비교"""
        results = {}
        
        for func in functions:
            times = []
            for _ in range(5):  # 5번 실행하여 평균 계산
                _, exec_time = self.time_function(func, *args, **kwargs)
                times.append(exec_time)
            
            avg_time = sum(times) / len(times)
            results[func.__name__] = avg_time
        
        # 결과 출력
        print("=== 성능 비교 결과 ===")
        sorted_results = sorted(results.items(), key=lambda x: x[1])
        
        fastest_time = sorted_results[0][1]
        
        for func_name, avg_time in sorted_results:
            speedup = fastest_time / avg_time
            print(f"{func_name}: {avg_time:.6f}초 (×{speedup:.2f})")
        
        return results

# 사용 예제
def list_creation_comparison():
    """리스트 생성 방법 비교"""
    
    @measure_time
    def using_append(n):
        result = []
        for i in range(n):
            result.append(i * 2)
        return result
    
    @measure_time
    def using_list_comprehension(n):
        return [i * 2 for i in range(n)]
    
    @measure_time
    def using_map(n):
        return list(map(lambda x: x * 2, range(n)))
    
    benchmark = PerformanceBenchmark()
    n = 100000
    
    print("리스트 생성 방법 비교 (100,000개 요소):")
    benchmark.compare_functions(
        [using_append, using_list_comprehension, using_map], 
        n
    )

if __name__ == "__main__":
    list_creation_comparison()
```

### 고급 프로파일링

```python
import cProfile
import pstats
import io
import sys
from memory_profiler import profile

class CodeProfiler:
    """코드 프로파일링 도구"""
    
    def __init__(self):
        self.profiler = cProfile.Profile()
    
    def profile_function(self, func, *args, **kwargs):
        """함수 프로파일링"""
        self.profiler.enable()
        result = func(*args, **kwargs)
        self.profiler.disable()
        
        return result
    
    def get_stats(self, sort_by='cumulative', lines=10):
        """프로파일링 결과 출력"""
        s = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=s)
        ps.sort_stats(sort_by)
        ps.print_stats(lines)
        
        return s.getvalue()
    
    def save_stats(self, filename):
        """프로파일링 결과를 파일로 저장"""
        self.profiler.dump_stats(filename)

# 메모리 프로파일링 예제
@profile
def memory_intensive_function():
    """메모리 집약적 함수 (memory_profiler 데코레이터 사용)"""
    # 대용량 리스트 생성
    big_list = [i for i in range(1000000)]
    
    # 딕셔너리 생성
    big_dict = {i: str(i) for i in range(100000)}
    
    # 리스트 복사
    copied_list = big_list.copy()
    
    # 메모리 정리
    del big_list, big_dict, copied_list

# CPU 집약적 함수 예제
def fibonacci_recursive(n):
    """재귀적 피보나치 (비효율적)"""
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

def fibonacci_iterative(n):
    """반복적 피보나치 (효율적)"""
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_memoized(n, memo={}):
    """메모이제이션을 사용한 피보나치"""
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoized(n-1, memo) + fibonacci_memoized(n-2, memo)
    return memo[n]

# 프로파일링 실행 예제
def profiling_example():
    """프로파일링 예제"""
    profiler = CodeProfiler()
    
    print("=== 피보나치 함수 성능 비교 ===")
    
    # 각 함수 프로파일링
    functions = [
        (fibonacci_iterative, "반복적"),
        (fibonacci_memoized, "메모이제이션"),
        # fibonacci_recursive는 너무 느려서 제외
    ]
    
    n = 35
    for func, name in functions:
        print(f"\n{name} 방식 (n={n}):")
        result = profiler.profile_function(func, n)
        print(f"결과: {result}")
        print(profiler.get_stats(lines=5))

if __name__ == "__main__":
    profiling_example()
```

## 코드 최적화 기법

### 데이터 구조 최적화

```python
import array
import collections
import sys
from collections import defaultdict, Counter

class DataStructureOptimization:
    """데이터 구조 최적화 예제"""
    
    def list_vs_array_comparison(self):
        """리스트 vs 배열 메모리 사용량 비교"""
        
        # 일반 리스트
        normal_list = [i for i in range(10000)]
        
        # array 모듈 사용
        int_array = array.array('i', range(10000))
        
        print("=== 메모리 사용량 비교 ===")
        print(f"일반 리스트: {sys.getsizeof(normal_list)} bytes")
        print(f"array.array: {sys.getsizeof(int_array)} bytes")
        print(f"메모리 절약: {sys.getsizeof(normal_list) / sys.getsizeof(int_array):.2f}배")
    
    def collections_optimization(self):
        """collections 모듈 최적화"""
        
        # defaultdict 사용
        def count_words_dict(words):
            """일반 딕셔너리로 단어 개수 세기"""
            word_count = {}
            for word in words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            return word_count
        
        def count_words_defaultdict(words):
            """defaultdict로 단어 개수 세기"""
            word_count = defaultdict(int)
            for word in words:
                word_count[word] += 1
            return dict(word_count)
        
        def count_words_counter(words):
            """Counter로 단어 개수 세기"""
            return dict(Counter(words))
        
        # 테스트 데이터
        words = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple'] * 1000
        
        benchmark = PerformanceBenchmark()
        print("\n=== 단어 개수 세기 성능 비교 ===")
        benchmark.compare_functions(
            [count_words_dict, count_words_defaultdict, count_words_counter],
            words
        )
    
    def string_optimization(self):
        """문자열 처리 최적화"""
        
        def string_concat_plus(strings):
            """+ 연산자로 문자열 연결"""
            result = ""
            for s in strings:
                result += s
            return result
        
        def string_concat_join(strings):
            """join으로 문자열 연결"""
            return "".join(strings)
        
        def string_concat_format(strings):
            """format으로 문자열 연결"""
            return "{}".format("".join(strings))
        
        # 테스트 데이터
        test_strings = ["hello"] * 1000
        
        benchmark = PerformanceBenchmark()
        print("\n=== 문자열 연결 성능 비교 ===")
        benchmark.compare_functions(
            [string_concat_plus, string_concat_join, string_concat_format],
            test_strings
        )

# __slots__ 최적화 예제
class RegularClass:
    """일반 클래스"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class OptimizedClass:
    """__slots__를 사용한 최적화된 클래스"""
    __slots__ = ['x', 'y', 'z']
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def slots_optimization_demo():
    """__slots__ 최적화 데모"""
    import sys
    
    # 객체 생성
    regular_obj = RegularClass(1, 2, 3)
    optimized_obj = OptimizedClass(1, 2, 3)
    
    print("=== __slots__ 메모리 최적화 ===")
    print(f"일반 클래스 객체: {sys.getsizeof(regular_obj.__dict__)} bytes")
    print(f"__slots__ 클래스 객체: {sys.getsizeof(optimized_obj)} bytes")
    
    # 많은 객체 생성 시 메모리 사용량 비교
    regular_objects = [RegularClass(i, i+1, i+2) for i in range(10000)]
    optimized_objects = [OptimizedClass(i, i+1, i+2) for i in range(10000)]
    
    regular_total = sum(sys.getsizeof(obj.__dict__) for obj in regular_objects)
    optimized_total = sum(sys.getsizeof(obj) for obj in optimized_objects)
    
    print(f"\n10,000개 객체 메모리 사용량:")
    print(f"일반 클래스: {regular_total:,} bytes")
    print(f"__slots__ 클래스: {optimized_total:,} bytes")
    print(f"메모리 절약: {regular_total / optimized_total:.2f}배")

if __name__ == "__main__":
    optimizer = DataStructureOptimization()
    optimizer.list_vs_array_comparison()
    optimizer.collections_optimization()
    optimizer.string_optimization()
    slots_optimization_demo()
```

### 알고리즘 최적화

```python
import bisect
import heapq
from functools import lru_cache
import numpy as np

class AlgorithmOptimization:
    """알고리즘 최적화 예제"""
    
    def search_optimization(self):
        """검색 최적화"""
        
        def linear_search(arr, target):
            """선형 검색 O(n)"""
            for i, item in enumerate(arr):
                if item == target:
                    return i
            return -1
        
        def binary_search_manual(arr, target):
            """수동 이진 검색 O(log n)"""
            left, right = 0, len(arr) - 1
            
            while left <= right:
                mid = (left + right) // 2
                if arr[mid] == target:
                    return mid
                elif arr[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1
            
            return -1
        
        def binary_search_bisect(arr, target):
            """bisect 모듈을 사용한 이진 검색"""
            index = bisect.bisect_left(arr, target)
            if index < len(arr) and arr[index] == target:
                return index
            return -1
        
        # 테스트 데이터
        sorted_array = list(range(0, 100000, 2))  # 짝수만
        target = 50000
        
        benchmark = PerformanceBenchmark()
        print("=== 검색 알고리즘 성능 비교 ===")
        benchmark.compare_functions(
            [linear_search, binary_search_manual, binary_search_bisect],
            sorted_array, target
        )
    
    def sorting_optimization(self):
        """정렬 최적화"""
        import random
        
        def bubble_sort(arr):
            """버블 정렬 O(n²)"""
            arr = arr.copy()
            n = len(arr)
            for i in range(n):
                for j in range(0, n - i - 1):
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
            return arr
        
        def quick_sort(arr):
            """퀵 정렬 O(n log n)"""
            if len(arr) <= 1:
                return arr
            
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]
            
            return quick_sort(left) + middle + quick_sort(right)
        
        def python_builtin_sort(arr):
            """파이썬 내장 정렬 (Timsort)"""
            return sorted(arr)
        
        # 테스트 데이터 (작은 크기로 제한)
        test_data = [random.randint(1, 1000) for _ in range(1000)]
        
        benchmark = PerformanceBenchmark()
        print("\n=== 정렬 알고리즘 성능 비교 ===")
        
        # 버블 정렬은 너무 느려서 작은 데이터로만 테스트
        small_data = test_data[:100]
        benchmark.compare_functions(
            [bubble_sort, quick_sort, python_builtin_sort],
            small_data
        )
    
    @lru_cache(maxsize=128)
    def expensive_calculation(self, n):
        """비용이 많이 드는 계산 (캐시됨)"""
        result = 0
        for i in range(n):
            result += i ** 2
        return result
    
    def caching_optimization(self):
        """캐싱을 통한 최적화"""
        
        def without_cache(n):
            """캐시 없는 비용이 많이 드는 계산"""
            result = 0
            for i in range(n):
                result += i ** 2
            return result
        
        # 캐시 없는 버전과 캐시 있는 버전 비교
        n = 10000
        
        print("\n=== 캐싱 최적화 비교 ===")
        
        # 첫 번째 실행 (캐시 미스)
        start = time.perf_counter()
        result1 = without_cache(n)
        time1 = time.perf_counter() - start
        
        start = time.perf_counter()
        result2 = self.expensive_calculation(n)
        time2 = time.perf_counter() - start
        
        print(f"첫 번째 실행 (캐시 미스):")
        print(f"  캐시 없음: {time1:.6f}초")
        print(f"  캐시 있음: {time2:.6f}초")
        
        # 두 번째 실행 (캐시 히트)
        start = time.perf_counter()
        result3 = without_cache(n)
        time3 = time.perf_counter() - start
        
        start = time.perf_counter()
        result4 = self.expensive_calculation(n)  # 캐시에서 바로 반환
        time4 = time.perf_counter() - start
        
        print(f"\n두 번째 실행 (캐시 히트):")
        print(f"  캐시 없음: {time3:.6f}초")
        print(f"  캐시 있음: {time4:.6f}초")
        print(f"  성능 향상: {time3/time4:.0f}배")

if __name__ == "__main__":
    optimizer = AlgorithmOptimization()
    optimizer.search_optimization()
    optimizer.sorting_optimization()
    optimizer.caching_optimization()
```

## 실습 프로젝트

###️ 프로젝트 1: 성능 분석 도구

```python
import time
import psutil
import threading
import matplotlib.pyplot as plt
from collections import deque
import cProfile
import pstats
import io

class PerformanceMonitor:
    """실시간 성능 모니터링 도구"""
    
    def __init__(self, duration=60, interval=0.1):
        self.duration = duration
        self.interval = interval
        self.monitoring = False
        
        # 데이터 저장
        self.timestamps = deque()
        self.cpu_usage = deque()
        self.memory_usage = deque()
        self.function_stats = {}
        
        # 스레드
        self.monitor_thread = None
    
    def start_monitoring(self):
        """모니터링 시작"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print("성능 모니터링 시작됨")
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("성능 모니터링 중지됨")
    
    def _monitor_loop(self):
        """모니터링 루프"""
        start_time = time.time()
        
        while self.monitoring and (time.time() - start_time) < self.duration:
            current_time = time.time() - start_time
            
            # CPU 사용률
            cpu_percent = psutil.cpu_percent(interval=None)
            
            # 메모리 사용률
            memory_info = psutil.virtual_memory()
            memory_percent = memory_info.percent
            
            # 데이터 저장
            self.timestamps.append(current_time)
            self.cpu_usage.append(cpu_percent)
            self.memory_usage.append(memory_percent)
            
            # 최대 1000개 데이터 포인트 유지
            if len(self.timestamps) > 1000:
                self.timestamps.popleft()
                self.cpu_usage.popleft()
                self.memory_usage.popleft()
            
            time.sleep(self.interval)
    
    def profile_function(self, func, *args, **kwargs):
        """함수 프로파일링"""
        profiler = cProfile.Profile()
        
        # 프로파일링 시작
        profiler.enable()
        start_time = time.perf_counter()
        
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            profiler.disable()
        
        # 통계 수집
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s)
        ps.sort_stats('cumulative')
        ps.print_stats(20)
        
        func_name = func.__name__
        self.function_stats[func_name] = {
            'execution_time': end_time - start_time,
            'profile_data': s.getvalue(),
            'result': result
        }
        
        return result
    
    def generate_report(self):
        """성능 보고서 생성"""
        report = []
        report.append("=== 성능 분석 보고서 ===\n")
        
        if self.timestamps:
            avg_cpu = sum(self.cpu_usage) / len(self.cpu_usage)
            max_cpu = max(self.cpu_usage)
            avg_memory = sum(self.memory_usage) / len(self.memory_usage)
            max_memory = max(self.memory_usage)
            
            report.append(f"모니터링 기간: {max(self.timestamps):.1f}초")
            report.append(f"평균 CPU 사용률: {avg_cpu:.1f}%")
            report.append(f"최대 CPU 사용률: {max_cpu:.1f}%")
            report.append(f"평균 메모리 사용률: {avg_memory:.1f}%")
            report.append(f"최대 메모리 사용률: {max_memory:.1f}%\n")
        
        # 함수 실행 시간
        if self.function_stats:
            report.append("=== 함수 실행 시간 ===")
            for func_name, stats in self.function_stats.items():
                exec_time = stats['execution_time']
                report.append(f"{func_name}: {exec_time:.6f}초")
            report.append("")
        
        return "\n".join(report)
    
    def plot_performance(self):
        """성능 그래프 생성"""
        if not self.timestamps:
            print("모니터링 데이터가 없습니다.")
            return
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # CPU 사용률 그래프
        ax1.plot(list(self.timestamps), list(self.cpu_usage), 'b-', label='CPU 사용률')
        ax1.set_ylabel('CPU 사용률 (%)')
        ax1.set_title('실시간 성능 모니터링')
        ax1.legend()
        ax1.grid(True)
        
        # 메모리 사용률 그래프
        ax2.plot(list(self.timestamps), list(self.memory_usage), 'r-', label='메모리 사용률')
        ax2.set_xlabel('시간 (초)')
        ax2.set_ylabel('메모리 사용률 (%)')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()

# 테스트 함수들
def cpu_intensive_task():
    """CPU 집약적 작업"""
    total = 0
    for i in range(1000000):
        total += i ** 2
    return total

def memory_intensive_task():
    """메모리 집약적 작업"""
    # 큰 리스트 생성
    big_list = [i for i in range(500000)]
    
    # 리스트 처리
    processed = [x * 2 for x in big_list]
    
    # 메모리 정리
    del big_list
    return len(processed)

def io_intensive_task():
    """I/O 집약적 작업 시뮬레이션"""
    import time
    for _ in range(10):
        time.sleep(0.1)  # I/O 대기 시뮬레이션
    return "IO complete"

# 사용 예제
def performance_monitoring_demo():
    """성능 모니터링 데모"""
    monitor = PerformanceMonitor(duration=30, interval=0.5)
    
    # 모니터링 시작
    monitor.start_monitoring()
    
    try:
        # 다양한 작업 실행
        print("CPU 집약적 작업 실행 중...")
        result1 = monitor.profile_function(cpu_intensive_task)
        
        time.sleep(2)
        
        print("메모리 집약적 작업 실행 중...")
        result2 = monitor.profile_function(memory_intensive_task)
        
        time.sleep(2)
        
        print("I/O 집약적 작업 실행 중...")
        result3 = monitor.profile_function(io_intensive_task)
        
        time.sleep(5)  # 추가 모니터링
        
    finally:
        # 모니터링 중지
        monitor.stop_monitoring()
    
    # 보고서 생성
    print("\n" + monitor.generate_report())
    
    # 그래프 표시 (matplotlib이 설치된 경우)
    try:
        monitor.plot_performance()
    except ImportError:
        print("matplotlib이 설치되지 않아 그래프를 표시할 수 없습니다.")

if __name__ == "__main__":
    performance_monitoring_demo()
```

## 체크리스트

### 성능 측정
- [ ] timeit 모듈로 실행 시간 측정
- [ ] cProfile로 함수별 성능 분석
- [ ] memory_profiler로 메모리 사용량 분석
- [ ] 벤치마킹 도구 개발

### 코드 최적화
- [ ] 리스트 컴프리헨션 활용
- [ ] 적절한 데이터 구조 선택
- [ ] __slots__로 메모리 최적화
- [ ] 내장 함수와 라이브러리 활용

### 알고리즘 최적화
- [ ] 시간 복잡도 개선
- [ ] 캐싱과 메모이제이션 적용
- [ ] 효율적인 검색/정렬 알고리즘
- [ ] 데이터 구조 최적화

### 고급 최적화
- [ ] 프로파일링 도구 활용
- [ ] 병목 지점 식별
- [ ] 메모리 사용량 최적화
- [ ] I/O 성능 개선

### 실무 적용
- [ ] 성능 모니터링 시스템 구축
- [ ] 자동화된 성능 테스트
- [ ] 성능 회귀 검출
- [ ] 최적화 전후 비교 분석

## 다음 단계

🎉 **축하합니다!** 성능 최적화를 마스터했습니다.

성능 최적화는 지속적인 과정입니다. 이제 [20. 메모리 관리](../20_memory_management/)로 넘어가서 파이썬의 메모리 관리 메커니즘을 더 깊이 이해해봅시다.

---

💡 **성능 최적화 가이드:**
- **측정 먼저** - 추측하지 말고 측정하라
- **병목 집중** - 가장 느린 부분을 우선 최적화
- **가독성 유지** - 성능과 가독성의 균형 유지
- **프로파일링 도구** 활용으로 정확한 분석
- **지속적 모니터링**으로 성능 회귀 방지 