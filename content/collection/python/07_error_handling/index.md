---
draft: true
title: "07. 예외 처리"
description: "프로그램의 안정성을 높이는 예외 처리 기법"
collection_order: 7
---

# 챕터 7: 예외 처리

> "실패는 성공의 어머니다" - 예외 상황을 우아하게 처리하여 견고한 프로그램을 만들어봅시다.

## 학습 목표
- 예외와 에러의 개념을 이해할 수 있다
- try-except 문을 활용하여 예외를 처리할 수 있다
- 다양한 예외 타입을 구분하고 적절히 처리할 수 있다
- 사용자 정의 예외를 만들고 활용할 수 있다

## 예외 처리 기본

### 예외란 무엇인가?

```python
# 예외 발생 상황들
print("=== 일반적인 예외 상황들 ===")

# 1. ZeroDivisionError
try:
    result = 10 / 0
except ZeroDivisionError:
    print("❌ 0으로 나눌 수 없습니다.")

# 2. ValueError
try:
    number = int("hello")
except ValueError:
    print("❌ 문자열을 숫자로 변환할 수 없습니다.")

# 3. FileNotFoundError
try:
    with open("nonexistent.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("❌ 파일을 찾을 수 없습니다.")

# 4. IndexError
try:
    numbers = [1, 2, 3]
    print(numbers[10])
except IndexError:
    print("❌ 리스트 인덱스가 범위를 벗어났습니다.")

# 5. KeyError
try:
    person = {"name": "Alice", "age": 25}
    print(person["height"])
except KeyError:
    print("❌ 딕셔너리에 해당 키가 없습니다.")
```

### try-except 기본 구조

```python
# 기본 try-except 구조
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("0으로 나눌 수 없습니다.")
        return None

print(safe_divide(10, 2))  # 5.0
print(safe_divide(10, 0))  # None

# 여러 예외 처리
def safe_convert_and_access(data, index):
    try:
        # 문자열을 숫자로 변환
        number = int(data[index])
        return number
    except IndexError:
        print(f"❌ 인덱스 {index}가 범위를 벗어났습니다.")
        return None
    except ValueError:
        print(f"❌ '{data[index]}'를 숫자로 변환할 수 없습니다.")
        return None

# 테스트
data = ["10", "20", "hello", "30"]
print(safe_convert_and_access(data, 0))   # 10
print(safe_convert_and_access(data, 2))   # None (ValueError)
print(safe_convert_and_access(data, 10))  # None (IndexError)
```

## 핵심 내용

### 예외 처리 기본
- **try-except**: 기본 예외 처리 구조
- **다중 예외**: 여러 예외 타입 처리
- **예외 정보**: 예외 객체 활용
- **예외 전파**: raise를 통한 재발생

### 완전한 예외 처리
- **try-except-else-finally**: 완전한 구조
- **else 절**: 예외가 없을 때 실행
- **finally 절**: 항상 실행되는 정리 코드
- **리소스 관리**: 안전한 자원 해제

### 사용자 정의 예외
- **Exception 상속**: 커스텀 예외 클래스
- **예외 계층**: 의미 있는 예외 분류
- **예외 정보**: 추가 속성과 메서드
- **예외 체인**: from 키워드 활용

### 고급 패턴
- **재시도 로직**: 일시적 오류 대응
- **예외 변환**: 적절한 추상화 수준
- **로깅 통합**: 예외 상황 기록
- **우아한 실패**: 사용자 친화적 오류 처리

## 체크리스트

### 기본 예외 처리
- [ ] try-except 구문 이해
- [ ] 주요 예외 타입 파악
- [ ] 예외 정보 활용
- [ ] 적절한 예외 처리 범위

### 고급 예외 처리
- [ ] try-except-else-finally 활용
- [ ] 리소스 안전한 관리
- [ ] 예외 전파와 변환
- [ ] 컨텍스트 매니저 이해

### 사용자 정의 예외
- [ ] 커스텀 예외 클래스 설계
- [ ] 의미 있는 예외 계층 구조
- [ ] 예외 메시지와 속성 활용
- [ ] 예외 체인 연결

### 실무 적용
- [ ] 견고한 코드 작성
- [ ] 사용자 친화적 오류 메시지
- [ ] 로깅과 모니터링 통합
- [ ] 테스트 가능한 예외 처리

## 다음 단계

🎉 **축하합니다!** 파이썬 예외 처리를 마스터했습니다.

이제 [08. 모듈과 패키지](../08_modules_packages/)로 넘어가서 코드를 체계적으로 구조화하고 재사용하는 방법을 학습해봅시다.

---

💡 **팁:**
- 예외 처리는 프로그램의 안정성을 위한 필수 요소입니다
- 구체적인 예외부터 일반적인 예외 순으로 처리하세요
- 예외 메시지는 사용자가 이해하기 쉽게 작성하세요
```python
# 패턴 1: 여러 예외를 하나로 처리
def read_number_from_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read().strip()
            return int(content)
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"❌ 오류 발생: {type(e).__name__}: {e}")
        return None

# 패턴 2: 예외 정보 활용
def detailed_error_handling(filename):
    try:
        with open(filename, 'r') as f:
            data = f.read()
            number = int(data)
            return 100 / number
    except FileNotFoundError as e:
        print(f"파일 오류: {filename}을 찾을 수 없습니다.")
        print(f"상세 정보: {e}")
    except ValueError as e:
        print(f"데이터 형식 오류: 파일 내용이 숫자가 아닙니다.")
        print(f"상세 정보: {e}")
    except ZeroDivisionError:
        print("계산 오류: 파일의 숫자가 0이어서 나눌 수 없습니다.")
    except Exception as e:
        print(f"예상치 못한 오류: {type(e).__name__}: {e}")

# 패턴 3: 예외 다시 발생시키기
def validate_and_process(value):
    try:
        number = int(value)
        if number < 0:
            raise ValueError("음수는 허용되지 않습니다.")
        return number * 2
    except ValueError as e:
        print(f"입력값 검증 실패: {e}")
        raise  # 예외를 다시 발생시킴

# 사용 예제
try:
    result = validate_and_process("-5")
except ValueError:
    print("상위 레벨에서 예외를 처리했습니다.")
```

## 완전한 예외 처리: try-except-else-finally

```python
# 완전한 예외 처리 구조
def comprehensive_file_processing(filename):
    file_handle = None
    try:
        print(f"📂 파일 '{filename}' 열기 시도...")
        file_handle = open(filename, 'r', encoding='utf-8')
        
        content = file_handle.read()
        print(f"📄 파일 내용 읽기 완료 ({len(content)}글자)")
        
        # 숫자 데이터 처리
        numbers = [int(line.strip()) for line in content.split('\n') if line.strip()]
        total = sum(numbers)
        
        return total, len(numbers)
        
    except FileNotFoundError:
        print("❌ 파일을 찾을 수 없습니다.")
        return None, 0
    
    except ValueError as e:
        print(f"❌ 데이터 형식 오류: {e}")
        return None, 0
    
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {type(e).__name__}: {e}")
        return None, 0
    
    else:
        # 예외가 발생하지 않았을 때만 실행
        print("✅ 파일 처리가 성공적으로 완료되었습니다.")
    
    finally:
        # 항상 실행되는 블록
        if file_handle and not file_handle.closed:
            file_handle.close()
            print("📁 파일이 안전하게 닫혔습니다.")
        print("🔚 파일 처리 작업 종료")

# 테스트용 파일 생성
with open('numbers.txt', 'w') as f:
    f.write('10\n20\n30\n40\n50')

# 함수 테스트
total, count = comprehensive_file_processing('numbers.txt')
if total is not None:
    print(f"📊 총합: {total}, 개수: {count}")

# 파일 정리
import os
os.remove('numbers.txt')
```

## 사용자 정의 예외

### 기본 사용자 정의 예외

```python
# 사용자 정의 예외 클래스
class CustomError(Exception):
    """기본 사용자 정의 예외"""
    pass

class ValidationError(CustomError):
    """데이터 검증 오류"""
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

class AgeValidationError(ValidationError):
    """나이 검증 오류"""
    pass

class EmailValidationError(ValidationError):
    """이메일 검증 오류"""
    pass

# 검증 함수들
def validate_age(age):
    if not isinstance(age, int):
        raise AgeValidationError("나이는 정수여야 합니다.", code="TYPE_ERROR")
    if age < 0:
        raise AgeValidationError("나이는 0 이상이어야 합니다.", code="NEGATIVE_AGE")
    if age > 150:
        raise AgeValidationError("나이는 150 이하여야 합니다.", code="TOO_OLD")
    return True

def validate_email(email):
    if not isinstance(email, str):
        raise EmailValidationError("이메일은 문자열이어야 합니다.")
    if "@" not in email:
        raise EmailValidationError("이메일에 @가 포함되어야 합니다.", code="MISSING_AT")
    if "." not in email.split("@")[1]:
        raise EmailValidationError("이메일 도메인에 .이 포함되어야 합니다.", code="INVALID_DOMAIN")
    return True

# 사용자 등록 함수
def register_user(name, age, email):
    try:
        # 이름 검증
        if not name or not name.strip():
            raise ValidationError("이름은 필수입니다.")
        
        # 나이 검증
        validate_age(age)
        
        # 이메일 검증
        validate_email(email)
        
        print(f"✅ 사용자 등록 성공: {name} ({age}세, {email})")
        return True
        
    except AgeValidationError as e:
        print(f"❌ 나이 오류: {e}")
        if e.code:
            print(f"   오류 코드: {e.code}")
        return False
        
    except EmailValidationError as e:
        print(f"❌ 이메일 오류: {e}")
        if e.code:
            print(f"   오류 코드: {e.code}")
        return False
        
    except ValidationError as e:
        print(f"❌ 검증 오류: {e}")
        return False

# 테스트
test_cases = [
    ("Alice", 25, "alice@example.com"),  # 정상
    ("Bob", -5, "bob@example.com"),      # 나이 오류
    ("Charlie", 30, "invalid-email"),     # 이메일 오류
    ("", 25, "test@example.com"),        # 이름 오류
]

for name, age, email in test_cases:
    print(f"\n📝 등록 시도: {name}, {age}, {email}")
    register_user(name, age, email)
```

### 고급 예외 처리 패턴

```python
# 예외 체인과 컨텍스트
class DatabaseError(Exception):
    """데이터베이스 관련 오류"""
    pass

class UserNotFoundError(DatabaseError):
    """사용자를 찾을 수 없음"""
    pass

def find_user_in_database(user_id):
    """데이터베이스에서 사용자 검색 시뮬레이션"""
    try:
        # 실제로는 데이터베이스 조회
        if user_id <= 0:
            raise ValueError("사용자 ID는 양수여야 합니다.")
        if user_id > 1000:
            raise UserNotFoundError(f"사용자 ID {user_id}를 찾을 수 없습니다.")
        
        # 시뮬레이션: 네트워크 오류
        import random
        if random.random() < 0.3:  # 30% 확률로 네트워크 오류
            raise ConnectionError("데이터베이스 연결 실패")
        
        return {"id": user_id, "name": f"User{user_id}", "email": f"user{user_id}@example.com"}
        
    except ValueError as e:
        # 입력값 오류를 DatabaseError로 변환
        raise DatabaseError(f"잘못된 입력값: {e}") from e
    except ConnectionError as e:
        # 연결 오류를 DatabaseError로 변환
        raise DatabaseError(f"데이터베이스 연결 문제: {e}") from e

# 재시도 로직이 포함된 함수
def get_user_with_retry(user_id, max_retries=3):
    """재시도 로직이 포함된 사용자 조회"""
    for attempt in range(max_retries):
        try:
            user = find_user_in_database(user_id)
            print(f"✅ 사용자 조회 성공 (시도 {attempt + 1}회): {user}")
            return user
            
        except DatabaseError as e:
            print(f"❌ 시도 {attempt + 1}회 실패: {e}")
            
            # 마지막 시도였다면 예외 발생
            if attempt == max_retries - 1:
                print(f"💥 최대 재시도 횟수({max_retries}회) 초과")
                raise
            
            # 잠시 대기 후 재시도
            import time
            wait_time = 2 ** attempt  # 지수 백오프
            print(f"⏳ {wait_time}초 후 재시도...")
            time.sleep(wait_time)

# 테스트
test_user_ids = [5, -1, 1001, 100]
for user_id in test_user_ids:
    print(f"\n🔍 사용자 ID {user_id} 조회 시도:")
    try:
        get_user_with_retry(user_id)
    except DatabaseError as e:
        print(f"최종 실패: {e}")
```

## 실습 프로젝트

###️ 프로젝트 1: 견고한 계산기

```python
class CalculatorError(Exception):
    """계산기 전용 예외"""
    pass

class DivisionByZeroError(CalculatorError):
    """0으로 나누기 오류"""
    pass

class InvalidOperatorError(CalculatorError):
    """잘못된 연산자 오류"""
    pass

class Calculator:
    """예외 처리가 포함된 견고한 계산기"""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        """덧셈"""
        try:
            result = float(a) + float(b)
            self.history.append(f"{a} + {b} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"덧셈 오류: 숫자가 아닌 값이 입력되었습니다.") from e
    
    def subtract(self, a, b):
        """뺄셈"""
        try:
            result = float(a) - float(b)
            self.history.append(f"{a} - {b} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"뺄셈 오류: 숫자가 아닌 값이 입력되었습니다.") from e
    
    def multiply(self, a, b):
        """곱셈"""
        try:
            result = float(a) * float(b)
            self.history.append(f"{a} × {b} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"곱셈 오류: 숫자가 아닌 값이 입력되었습니다.") from e
    
    def divide(self, a, b):
        """나눗셈"""
        try:
            a, b = float(a), float(b)
            if b == 0:
                raise DivisionByZeroError("0으로 나눌 수 없습니다.")
            result = a / b
            self.history.append(f"{a} ÷ {b} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"나눗셈 오류: 숫자가 아닌 값이 입력되었습니다.") from e
    
    def power(self, a, b):
        """거듭제곱"""
        try:
            a, b = float(a), float(b)
            # 매우 큰 결과 방지
            if abs(a) > 1000 and abs(b) > 10:
                raise CalculatorError("결과가 너무 클 수 있습니다.")
            result = a ** b
            self.history.append(f"{a} ^ {b} = {result}")
            return result
        except (ValueError, TypeError) as e:
            raise CalculatorError(f"거듭제곱 오류: 숫자가 아닌 값이 입력되었습니다.") from e
        except OverflowError:
            raise CalculatorError("계산 결과가 너무 큽니다.")
    
    def calculate(self, expression):
        """문자열 수식 계산"""
        try:
            # 간단한 보안 검사
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                raise CalculatorError("허용되지 않는 문자가 포함되어 있습니다.")
            
            # 수식 계산
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
            
        except ZeroDivisionError:
            raise DivisionByZeroError("수식에서 0으로 나누기가 발생했습니다.")
        except (SyntaxError, NameError) as e:
            raise CalculatorError(f"잘못된 수식입니다: {expression}") from e
        except Exception as e:
            raise CalculatorError(f"수식 계산 오류: {e}") from e
    
    def get_history(self):
        """계산 기록 반환"""
        return self.history.copy()
    
    def clear_history(self):
        """계산 기록 삭제"""
        self.history.clear()

def calculator_interface():
    """계산기 인터페이스"""
    calc = Calculator()
    
    print("=== 견고한 계산기 ===")
    print("지원 연산: +, -, *, /, ** (거듭제곱)")
    print("명령어: history (기록), clear (기록삭제), quit (종료)")
    
    while True:
        try:
            user_input = input("\n계산식 또는 명령어 입력: ").strip()
            
            if user_input.lower() == 'quit':
                print("계산기를 종료합니다.")
                break
            
            elif user_input.lower() == 'history':
                history = calc.get_history()
                if history:
                    print("\n📊 계산 기록:")
                    for i, record in enumerate(history[-10:], 1):  # 최근 10개만
                        print(f"  {i}. {record}")
                else:
                    print("계산 기록이 없습니다.")
                continue
            
            elif user_input.lower() == 'clear':
                calc.clear_history()
                print("✅ 계산 기록이 삭제되었습니다.")
                continue
            
            # 계산 실행
            result = calc.calculate(user_input)
            print(f"결과: {result}")
            
            # 결과 타입별 추가 정보
            if isinstance(result, float):
                if result.is_integer():
                    print(f"정수로 표현: {int(result)}")
                else:
                    print(f"반올림 (소수점 2자리): {result:.2f}")
            
        except DivisionByZeroError as e:
            print(f"❌ 나눗셈 오류: {e}")
        
        except InvalidOperatorError as e:
            print(f"❌ 연산자 오류: {e}")
        
        except CalculatorError as e:
            print(f"❌ 계산기 오류: {e}")
        
        except KeyboardInterrupt:
            print("\n\n프로그램을 중단합니다.")
            break
        
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {type(e).__name__}: {e}")
            print("프로그램을 계속 진행합니다.")

# 계산기 실행
if __name__ == "__main__":
    calculator_interface()
```

###️ 프로젝트 2: 파일 처리 유틸리티

```python
import os
import shutil
from pathlib import Path
import json
from datetime import datetime

class FileUtilityError(Exception):
    """파일 유틸리티 전용 예외"""
    pass

class FileOperationError(FileUtilityError):
    """파일 작업 오류"""
    pass

class DirectoryError(FileUtilityError):
    """디렉토리 관련 오류"""
    pass

class FileUtility:
    """견고한 파일 처리 유틸리티"""
    
    def __init__(self, base_dir=None):
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.operation_log = []
    
    def log_operation(self, operation, success=True, error=None):
        """작업 로그 기록"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "success": success,
            "error": str(error) if error else None
        }
        self.operation_log.append(log_entry)
    
    def safe_copy_file(self, source, destination):
        """안전한 파일 복사"""
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            # 소스 파일 존재 확인
            if not source_path.exists():
                raise FileNotFoundError(f"소스 파일이 존재하지 않습니다: {source}")
            
            if not source_path.is_file():
                raise FileOperationError(f"소스가 파일이 아닙니다: {source}")
            
            # 대상 디렉토리 생성
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 파일 크기 확인 (너무 큰 파일 방지)
            file_size = source_path.stat().st_size
            if file_size > 100 * 1024 * 1024:  # 100MB 제한
                raise FileOperationError(f"파일이 너무 큽니다: {file_size / 1024 / 1024:.1f}MB")
            
            # 백업 생성 (대상 파일이 이미 존재하는 경우)
            if dest_path.exists():
                backup_path = dest_path.with_suffix(dest_path.suffix + '.backup')
                shutil.copy2(dest_path, backup_path)
                print(f"기존 파일 백업: {backup_path}")
            
            # 파일 복사
            shutil.copy2(source_path, dest_path)
            
            # 복사 검증
            if not dest_path.exists():
                raise FileOperationError("파일 복사가 완료되지 않았습니다.")
            
            if source_path.stat().st_size != dest_path.stat().st_size:
                raise FileOperationError("복사된 파일 크기가 다릅니다.")
            
            self.log_operation(f"파일 복사: {source} → {destination}")
            print(f"✅ 파일 복사 완료: {source} → {destination}")
            return True
            
        except FileNotFoundError as e:
            self.log_operation(f"파일 복사 실패: {source} → {destination}", False, e)
            raise
        except PermissionError as e:
            error_msg = f"권한 부족: {e}"
            self.log_operation(f"파일 복사 실패: {source} → {destination}", False, error_msg)
            raise FileOperationError(error_msg) from e
        except OSError as e:
            error_msg = f"파일 시스템 오류: {e}"
            self.log_operation(f"파일 복사 실패: {source} → {destination}", False, error_msg)
            raise FileOperationError(error_msg) from e
    
    def safe_delete_file(self, file_path, use_recycle_bin=True):
        """안전한 파일 삭제"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                raise FileNotFoundError(f"파일이 존재하지 않습니다: {file_path}")
            
            if not path.is_file():
                raise FileOperationError(f"파일이 아닙니다: {file_path}")
            
            # 휴지통 사용 옵션
            if use_recycle_bin:
                # 실제 구현에서는 send2trash 라이브러리 사용 권장
                recycle_dir = self.base_dir / ".recycle_bin"
                recycle_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                recycled_name = f"{path.stem}_{timestamp}{path.suffix}"
                recycled_path = recycle_dir / recycled_name
                
                shutil.move(str(path), str(recycled_path))
                print(f"🗑️ 파일을 휴지통으로 이동: {recycled_path}")
            else:
                path.unlink()
                print(f"🗑️ 파일 완전 삭제: {file_path}")
            
            self.log_operation(f"파일 삭제: {file_path}")
            return True
            
        except FileNotFoundError as e:
            self.log_operation(f"파일 삭제 실패: {file_path}", False, e)
            raise
        except PermissionError as e:
            error_msg = f"권한 부족: {e}"
            self.log_operation(f"파일 삭제 실패: {file_path}", False, error_msg)
            raise FileOperationError(error_msg) from e
    
    def create_directory_structure(self, structure_dict, base_path=None):
        """디렉토리 구조 생성"""
        if base_path is None:
            base_path = self.base_dir
        else:
            base_path = Path(base_path)
        
        try:
            for name, content in structure_dict.items():
                current_path = base_path / name
                
                if isinstance(content, dict):
                    # 디렉토리 생성 후 재귀 호출
                    current_path.mkdir(exist_ok=True)
                    print(f"📁 디렉토리 생성: {current_path}")
                    self.create_directory_structure(content, current_path)
                
                elif isinstance(content, str):
                    # 파일 생성
                    current_path.parent.mkdir(parents=True, exist_ok=True)
                    current_path.write_text(content, encoding='utf-8')
                    print(f"📄 파일 생성: {current_path}")
                
                else:
                    # 빈 파일 생성
                    current_path.parent.mkdir(parents=True, exist_ok=True)
                    current_path.touch()
                    print(f"📄 빈 파일 생성: {current_path}")
            
            self.log_operation(f"디렉토리 구조 생성: {base_path}")
            return True
            
        except PermissionError as e:
            error_msg = f"권한 부족: {e}"
            self.log_operation(f"디렉토리 구조 생성 실패: {base_path}", False, error_msg)
            raise DirectoryError(error_msg) from e
        except OSError as e:
            error_msg = f"파일 시스템 오류: {e}"
            self.log_operation(f"디렉토리 구조 생성 실패: {base_path}", False, error_msg)
            raise DirectoryError(error_msg) from e
    
    def backup_directory(self, source_dir, backup_name=None):
        """디렉토리 백업"""
        try:
            source_path = Path(source_dir)
            
            if not source_path.exists():
                raise DirectoryError(f"소스 디렉토리가 존재하지 않습니다: {source_dir}")
            
            if not source_path.is_dir():
                raise DirectoryError(f"소스가 디렉토리가 아닙니다: {source_dir}")
            
            # 백업 이름 생성
            if backup_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{source_path.name}_backup_{timestamp}"
            
            backup_path = self.base_dir / "backups" / backup_name
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 디렉토리 복사
            shutil.copytree(source_path, backup_path, dirs_exist_ok=True)
            
            # 백업 정보 저장
            backup_info = {
                "source": str(source_path),
                "backup_path": str(backup_path),
                "timestamp": datetime.now().isoformat(),
                "file_count": sum(1 for _ in backup_path.rglob('*') if _.is_file())
            }
            
            info_file = backup_path / "backup_info.json"
            info_file.write_text(json.dumps(backup_info, indent=2, ensure_ascii=False))
            
            self.log_operation(f"디렉토리 백업: {source_dir} → {backup_path}")
            print(f"✅ 백업 완료: {backup_path}")
            return backup_path
            
        except shutil.Error as e:
            error_msg = f"백업 과정에서 오류 발생: {e}"
            self.log_operation(f"디렉토리 백업 실패: {source_dir}", False, error_msg)
            raise DirectoryError(error_msg) from e
    
    def get_operation_log(self):
        """작업 로그 반환"""
        return self.operation_log.copy()
    
    def save_operation_log(self, filename=None):
        """작업 로그 파일로 저장"""
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"file_operations_{timestamp}.json"
            
            log_file = self.base_dir / filename
            log_file.write_text(
                json.dumps(self.operation_log, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            
            print(f"📝 작업 로그 저장: {log_file}")
            return log_file
            
        except Exception as e:
            raise FileOperationError(f"로그 저장 실패: {e}") from e

# 파일 유틸리티 사용 예제
def demo_file_utility():
    """파일 유틸리티 데모"""
    try:
        # 유틸리티 생성
        util = FileUtility("./file_demo")
        
        # 테스트 구조 생성
        test_structure = {
            "documents": {
                "reports": {
                    "2024_report.txt": "2024년 보고서 내용"
                },
                "notes": {
                    "meeting_notes.txt": "회의 내용\n- 항목 1\n- 항목 2"
                }
            },
            "images": {},
            "backup": {},
            "readme.txt": "프로젝트 설명 파일"
        }
        
        print("📁 디렉토리 구조 생성 중...")
        util.create_directory_structure(test_structure)
        
        # 파일 복사 테스트
        print("\n📋 파일 복사 테스트...")
        util.safe_copy_file(
            "./file_demo/readme.txt",
            "./file_demo/backup/readme_backup.txt"
        )
        
        # 백업 테스트
        print("\n💾 디렉토리 백업 테스트...")
        backup_path = util.backup_directory("./file_demo/documents")
        
        # 작업 로그 저장
        print("\n📝 작업 로그 저장...")
        log_file = util.save_operation_log()
        
        # 로그 출력
        print("\n📊 작업 로그:")
        for i, log in enumerate(util.get_operation_log(), 1):
            status = "✅" if log["success"] else "❌"
            print(f"  {i}. {status} {log['operation']} ({log['timestamp'][:19]})")
        
        print(f"\n🎉 데모 완료! 생성된 파일들을 확인해보세요.")
        print(f"   - 메인 디렉토리: ./file_demo")
        print(f"   - 백업: {backup_path}")
        print(f"   - 로그: {log_file}")
        
    except (FileUtilityError, FileOperationError, DirectoryError) as e:
        print(f"❌ 파일 유틸리티 오류: {e}")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {type(e).__name__}: {e}")

# 데모 실행
if __name__ == "__main__":
    demo_file_utility()
```

## 핵심 내용

### 예외 처리 기본
- **try-except**: 기본 예외 처리 구조
- **다중 예외**: 여러 예외 타입 처리
- **예외 정보**: 예외 객체 활용
- **예외 전파**: raise를 통한 재발생

### 완전한 예외 처리
- **try-except-else-finally**: 완전한 구조
- **else 절**: 예외가 없을 때 실행
- **finally 절**: 항상 실행되는 정리 코드
- **리소스 관리**: 안전한 자원 해제

### 사용자 정의 예외
- **Exception 상속**: 커스텀 예외 클래스
- **예외 계층**: 의미 있는 예외 분류
- **예외 정보**: 추가 속성과 메서드
- **예외 체인**: from 키워드 활용

### 고급 패턴
- **재시도 로직**: 일시적 오류 대응
- **예외 변환**: 적절한 추상화 수준
- **로깅 통합**: 예외 상황 기록
- **우아한 실패**: 사용자 친화적 오류 처리

## 체크리스트

### 기본 예외 처리
- [ ] try-except 구문 이해
- [ ] 주요 예외 타입 파악
- [ ] 예외 정보 활용
- [ ] 적절한 예외 처리 범위

### 고급 예외 처리
- [ ] try-except-else-finally 활용
- [ ] 리소스 안전한 관리
- [ ] 예외 전파와 변환
- [ ] 컨텍스트 매니저 이해

### 사용자 정의 예외
- [ ] 커스텀 예외 클래스 설계
- [ ] 의미 있는 예외 계층 구조
- [ ] 예외 메시지와 속성 활용
- [ ] 예외 체인 연결

### 실무 적용
- [ ] 견고한 코드 작성
- [ ] 사용자 친화적 오류 메시지
- [ ] 로깅과 모니터링 통합
- [ ] 테스트 가능한 예외 처리

## 다음 단계

🎉 **축하합니다!** 파이썬 예외 처리를 마스터했습니다.

이제 [08. 모듈과 패키지](../08_modules_packages/)로 넘어가서 코드를 체계적으로 구조화하고 재사용하는 방법을 학습해봅시다.

---

💡 **팁:**
- 예외 처리는 프로그램의 안정성을 위한 필수 요소입니다
- 구체적인 예외부터 일반적인 예외 순으로 처리하세요
- 예외 메시지는 사용자가 이해하기 쉽게 작성하세요
- finally 블록을 활용하여 리소스를 안전하게 해제하세요 