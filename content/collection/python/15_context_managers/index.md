---
draft: true
title: "15. 컨텍스트 매니저"
description: "with문과 컨텍스트 매니저를 활용하여 리소스를 안전하게 관리합니다"
collection_order: 15
---

# 15. 컨텍스트 매니저

컨텍스트 매니저는 리소스를 안전하게 관리하고 정리하는 파이썬의 핵심 기능입니다.

## 학습 목표

이 챕터를 완료하면 다음을 할 수 있습니다:

- **with문**의 동작 원리 이해
- **커스텀 컨텍스트 매니저** 구현
- **contextlib 모듈** 완전 활용
- **리소스 관리** 모범 사례 적용
- **예외 상황**에서도 안전한 정리

## 핵심 내용

### 컨텍스트 매니저 기본

**with문의 필요성**

```python
# 전통적인 방식 - 위험함
file = open('example.txt', 'r')
try:
    content = file.read()
    # 에러 발생 시 파일이 닫히지 않을 수 있음
    result = process_content(content)
finally:
    file.close()

# with문 사용 - 안전함
with open('example.txt', 'r') as file:
    content = file.read()
    result = process_content(content)
# 자동으로 파일이 닫힘 (에러 발생 시에도)
```

**컨텍스트 매니저 프로토콜**

```python
class SimpleContextManager:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        print(f"{self.name} 리소스 획득")
        return self  # with문의 as 뒤에 할당될 객체
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f"{self.name} 리소스 해제")
        if exc_type:
            print(f"예외 발생: {exc_type.__name__}: {exc_value}")
        return False  # 예외를 다시 발생시킴

# 사용 예제
with SimpleContextManager("테스트") as cm:
    print("컨텍스트 내부 작업")
    # raise ValueError("예외 테스트")  # 주석 해제 시 예외 처리 확인
```

### 파일과 데이터베이스 관리

**안전한 파일 처리**

```python
class SafeFileManager:
    def __init__(self, filename, mode='r', encoding='utf-8'):
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.file = None
    
    def __enter__(self):
        try:
            self.file = open(self.filename, self.mode, encoding=self.encoding)
            print(f"파일 열기 성공: {self.filename}")
            return self.file
        except IOError as e:
            print(f"파일 열기 실패: {e}")
            raise
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()
            print(f"파일 닫기 완료: {self.filename}")
        
        if exc_type:
            print(f"파일 처리 중 오류: {exc_value}")
        return False

# 사용 예제
with SafeFileManager('test.txt', 'w') as f:
    f.write("안전한 파일 쓰기")
    f.write("컨텍스트 매니저로 관리됨")
```

**데이터베이스 연결 관리**

```python
import sqlite3

class DatabaseConnection:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        print(f"데이터베이스 연결: {self.db_path}")
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"트랜잭션 롤백: {exc_value}")
            self.connection.rollback()
        else:
            print("트랜잭션 커밋")
            self.connection.commit()
        
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("데이터베이스 연결 종료")
        
        return False

# 사용 예제
with DatabaseConnection(':memory:') as cursor:
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT
        )
    ''')
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", 
                   ("김철수", "kim@example.com"))
```

### contextlib 모듈

**@contextmanager 데코레이터**

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name):
    """실행 시간 측정 컨텍스트 매니저"""
    start_time = time.time()
    print(f"{name} 시작")
    
    try:
        yield start_time  # with문의 as 뒤에 전달될 값
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print(f"{name} 완료: {duration:.4f}초")

# 사용 예제
with timer("데이터 처리") as start:
    time.sleep(0.1)
    current_time = time.time()
    print(f"중간 경과: {current_time - start:.4f}초")

@contextmanager
def temporary_attribute(obj, attr_name, value):
    """임시로 객체 속성 변경"""
    old_value = getattr(obj, attr_name, None)
    setattr(obj, attr_name, value)
    print(f"속성 {attr_name}을 {value}로 변경")
    
    try:
        yield obj
    finally:
        if old_value is not None:
            setattr(obj, attr_name, old_value)
        else:
            delattr(obj, attr_name)
        print(f"속성 {attr_name} 복원")

# 사용 예제
class TestObject:
    def __init__(self):
        self.name = "원본"

obj = TestObject()
print(f"원래 이름: {obj.name}")

with temporary_attribute(obj, 'name', '임시'):
    print(f"임시 이름: {obj.name}")

print(f"복원된 이름: {obj.name}")
```

**기타 유용한 contextlib 도구들**

```python
from contextlib import contextmanager, closing, suppress, redirect_stdout
import io
import urllib.request

# closing: __exit__ 메서드가 없는 객체를 컨텍스트 매니저로 만들기
with closing(urllib.request.urlopen('https://www.python.org')) as response:
    data = response.read()

# suppress: 특정 예외 무시
with suppress(FileNotFoundError):
    with open('nonexistent.txt') as f:
        print(f.read())

print("파일이 없어도 계속 실행됩니다.")

# redirect_stdout: 표준 출력 리다이렉션
output_buffer = io.StringIO()

with redirect_stdout(output_buffer):
    print("이 출력은 버퍼로 갑니다")
    print("여러 줄 출력")

captured_output = output_buffer.getvalue()
print(f"캡처된 출력: {repr(captured_output)}")
```

### 고급 컨텍스트 매니저 패턴

**중첩 컨텍스트 매니저**

```python
@contextmanager
def multi_file_manager(*filenames):
    """여러 파일을 동시에 관리"""
    files = []
    try:
        for filename in filenames:
            file = open(filename, 'r')
            files.append(file)
        yield files
    finally:
        for file in files:
            if file:
                file.close()
                print(f"파일 닫기: {file.name}")

# 사용 예제 (파일들이 존재한다고 가정)
# with multi_file_manager('file1.txt', 'file2.txt') as files:
#     for file in files:
#         print(f"{file.name}: {file.read()}")
```

**조건부 컨텍스트 매니저**

```python
@contextmanager
def conditional_timer(enabled=True):
    """조건부 타이머"""
    if enabled:
        start_time = time.time()
        print("타이머 시작")
    
    try:
        yield
    finally:
        if enabled:
            duration = time.time() - start_time
            print(f"실행 시간: {duration:.4f}초")

# 사용 예제
with conditional_timer(True):
    time.sleep(0.1)
    print("측정된 작업")

with conditional_timer(False):
    time.sleep(0.1)
    print("측정되지 않은 작업")
```

## 실습 프로젝트

### 프로젝트 1: 로그 관리 시스템

```python
import logging
import sys
from contextlib import contextmanager
from datetime import datetime
import threading

class LogManager:
    def __init__(self):
        self.loggers = {}
        self.lock = threading.Lock()
    
    @contextmanager
    def logger_context(self, name, level=logging.INFO, 
                      filename=None, format_string=None):
        """로거 컨텍스트 매니저"""
        
        # 기본 포매터
        if format_string is None:
            format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        formatter = logging.Formatter(format_string)
        
        # 로거 생성
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # 핸들러 설정
        handlers = []
        
        # 파일 핸들러
        if filename:
            file_handler = logging.FileHandler(filename, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            handlers.append(file_handler)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        handlers.append(console_handler)
        
        try:
            with self.lock:
                self.loggers[name] = logger
            
            logger.info(f"로거 '{name}' 시작")
            yield logger
            
        finally:
            logger.info(f"로거 '{name}' 종료")
            
            # 핸들러 정리
            for handler in handlers:
                logger.removeHandler(handler)
                handler.close()
            
            with self.lock:
                if name in self.loggers:
                    del self.loggers[name]
    
    @contextmanager
    def performance_logging(self, logger, operation_name):
        """성능 로깅 컨텍스트"""
        start_time = datetime.now()
        logger.info(f"'{operation_name}' 시작")
        
        try:
            yield
            
        except Exception as e:
            logger.error(f"'{operation_name}' 실패: {e}")
            raise
            
        finally:
            duration = datetime.now() - start_time
            logger.info(f"'{operation_name}' 완료 (소요시간: {duration.total_seconds():.4f}초)")
    
    @contextmanager
    def error_handling(self, logger, operation_name, reraise=True):
        """에러 처리 컨텍스트"""
        try:
            yield
            
        except Exception as e:
            logger.error(f"'{operation_name}' 중 오류 발생", exc_info=True)
            
            if reraise:
                raise
            else:
                logger.warning(f"'{operation_name}' 오류를 무시하고 계속 진행")

# 테스트 함수들
def simulate_work():
    """작업 시뮬레이션"""
    import time
    import random
    
    time.sleep(random.uniform(0.1, 0.3))
    
    # 20% 확률로 예외 발생
    if random.random() < 0.2:
        raise RuntimeError("시뮬레이션된 오류")
    
    return "작업 완료"

def test_log_manager():
    """로그 매니저 테스트"""
    log_manager = LogManager()
    
    # 기본 로깅
    with log_manager.logger_context('basic_test', filename='test.log') as logger:
        logger.info("기본 테스트 시작")
        logger.warning("경고 메시지")
        logger.error("에러 메시지")
    
    # 성능 로깅
    with log_manager.logger_context('performance_test') as logger:
        with log_manager.performance_logging(logger, "시뮬레이션 작업"):
            result = simulate_work()
            logger.info(f"작업 결과: {result}")
    
    # 에러 처리 로깅
    with log_manager.logger_context('error_test') as logger:
        for i in range(3):
            with log_manager.error_handling(logger, f"작업 {i+1}", reraise=False):
                result = simulate_work()
                logger.info(f"작업 {i+1} 결과: {result}")

if __name__ == "__main__":
    test_log_manager()
```

### 프로젝트 2: 임시 환경 관리자

```python
import os
import tempfile
import shutil
from contextlib import contextmanager
from pathlib import Path

class EnvironmentManager:
    """환경 설정 및 임시 리소스 관리"""
    
    @contextmanager
    def temporary_directory(self, prefix="temp_", cleanup=True):
        """임시 디렉토리 생성 및 관리"""
        temp_dir = tempfile.mkdtemp(prefix=prefix)
        temp_path = Path(temp_dir)
        
        print(f"임시 디렉토리 생성: {temp_path}")
        
        try:
            yield temp_path
            
        finally:
            if cleanup and temp_path.exists():
                shutil.rmtree(temp_path)
                print(f"임시 디렉토리 삭제: {temp_path}")
    
    @contextmanager
    def environment_variables(self, **variables):
        """환경 변수 임시 설정"""
        old_values = {}
        
        # 현재 값 저장 및 새 값 설정
        for key, value in variables.items():
            old_values[key] = os.environ.get(key)
            os.environ[key] = str(value)
            print(f"환경 변수 설정: {key}={value}")
        
        try:
            yield
            
        finally:
            # 원래 값 복원
            for key, old_value in old_values.items():
                if old_value is None:
                    if key in os.environ:
                        del os.environ[key]
                        print(f"환경 변수 삭제: {key}")
                else:
                    os.environ[key] = old_value
                    print(f"환경 변수 복원: {key}={old_value}")
    
    @contextmanager
    def working_directory(self, path):
        """작업 디렉토리 임시 변경"""
        old_cwd = os.getcwd()
        new_path = Path(path).resolve()
        
        print(f"작업 디렉토리 변경: {old_cwd} → {new_path}")
        os.chdir(new_path)
        
        try:
            yield new_path
            
        finally:
            os.chdir(old_cwd)
            print(f"작업 디렉토리 복원: {new_path} → {old_cwd}")
    
    @contextmanager
    def file_backup(self, filepath):
        """파일 백업 및 복원"""
        file_path = Path(filepath)
        backup_path = None
        
        if file_path.exists():
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            shutil.copy2(file_path, backup_path)
            print(f"파일 백업: {file_path} → {backup_path}")
        
        try:
            yield file_path
            
        except Exception:
            # 예외 발생 시 복원
            if backup_path and backup_path.exists():
                shutil.copy2(backup_path, file_path)
                print(f"파일 복원: {backup_path} → {file_path}")
            raise
            
        finally:
            # 백업 파일 정리
            if backup_path and backup_path.exists():
                backup_path.unlink()
                print(f"백업 파일 삭제: {backup_path}")

def test_environment_manager():
    """환경 매니저 테스트"""
    env_manager = EnvironmentManager()
    
    print("=== 임시 디렉토리 테스트 ===")
    with env_manager.temporary_directory("test_") as temp_dir:
        print(f"임시 디렉토리 사용: {temp_dir}")
        
        # 파일 생성 테스트
        test_file = temp_dir / "test.txt"
        test_file.write_text("테스트 내용")
        print(f"파일 생성: {test_file}")
        
        # 서브 디렉토리 생성
        sub_dir = temp_dir / "subdir"
        sub_dir.mkdir()
        print(f"서브 디렉토리 생성: {sub_dir}")
    
    print("\n=== 환경 변수 테스트 ===")
    print(f"원래 PATH: {os.environ.get('PATH', 'None')[:50]}...")
    print(f"원래 TEST_VAR: {os.environ.get('TEST_VAR', 'None')}")
    
    with env_manager.environment_variables(TEST_VAR="임시값", PATH="/tmp"):
        print(f"임시 PATH: {os.environ.get('PATH')}")
        print(f"임시 TEST_VAR: {os.environ.get('TEST_VAR')}")
    
    print(f"복원된 PATH: {os.environ.get('PATH', 'None')[:50]}...")
    print(f"복원된 TEST_VAR: {os.environ.get('TEST_VAR', 'None')}")
    
    print("\n=== 작업 디렉토리 테스트 ===")
    print(f"현재 디렉토리: {os.getcwd()}")
    
    with env_manager.working_directory("/tmp"):
        print(f"임시 디렉토리: {os.getcwd()}")
        # 여기서 임시 디렉토리에서 작업 수행
    
    print(f"복원된 디렉토리: {os.getcwd()}")

if __name__ == "__main__":
    test_environment_manager()
```

## 체크리스트

### 기본 컨텍스트 매니저
- [ ] __enter__와 __exit__ 메서드 구현
- [ ] 예외 처리와 정리 작업
- [ ] with문 동작 원리 이해
- [ ] 리소스 안전 관리

### contextlib 활용
- [ ] @contextmanager 데코레이터
- [ ] closing, suppress 함수
- [ ] redirect_stdout/stderr
- [ ] ExitStack 고급 활용

### 실무 패턴
- [ ] 파일과 네트워크 리소스 관리
- [ ] 데이터베이스 트랜잭션
- [ ] 임시 환경과 설정 변경
- [ ] 로깅과 모니터링

### 고급 기법
- [ ] 중첩 컨텍스트 매니저
- [ ] 조건부 컨텍스트 관리
- [ ] 비동기 컨텍스트 매니저 기초
- [ ] 커스텀 예외 처리

## 다음 단계

🎉 **축하합니다!** 파이썬 컨텍스트 매니저를 마스터했습니다.

이제 중급에서 고급으로 넘어가는 단계입니다. 다음 챕터들에서는 메타클래스, 동시성, 비동기 프로그래밍 등 더욱 고급 주제들을 다룰 예정입니다.

---

💡 **팁:**
- 리소스를 사용하는 모든 곳에서 컨텍스트 매니저를 고려하세요
- @contextmanager 데코레이터로 간단한 컨텍스트 매니저를 빠르게 만들 수 있습니다
- __exit__ 메서드에서 False를 반환하면 예외가 다시 발생합니다
- ExitStack을 사용하여 동적으로 컨텍스트 매니저를 관리할 수 있습니다 