---
draft: true
---
# Chapter 5: 형식화 - 실습 과제

## 실습 개요
이 실습은 코드 형식화의 중요성을 이해하고, 일관성 있는 코딩 스타일을 적용하며, 팀 차원의 스타일 가이드를 작성하는 것을 목표로 합니다.

## 실습 1: 코드 형식화 개선 (40분)

### 목표
형식이 엉망인 코드를 Clean Code 형식화 원칙에 맞게 개선합니다.

### 개선 대상 코드

#### Java 예시 - 사용자 관리 시스템
```java
// Bad: 형식이 엉망인 코드
import java.util.*;import java.time.*;
public class UserManager{
private List<User>users=new ArrayList<>();private Map<String,String>userSessions=new HashMap<>();
private final int MAX_SESSIONS=100;
public UserManager(){this.users=new ArrayList<>();}
public boolean addUser(String name,String email,int age){
if(name==null||name.trim().isEmpty()){return false;}
if(email==null||!email.contains("@")){return false;}
if(age<0||age>150){return false;}
User newUser=new User(name,email,age);users.add(newUser);return true;
}

public User findUserByEmail(String email){if(email==null)return null;for(User user:users){if(user.getEmail().equals(email))return user;}return null;}

public List<User>getUsersByAgeRange(int minAge,int maxAge){
List<User>result=new ArrayList<>();
for(User user:users){if(user.getAge()>=minAge&&user.getAge()<=maxAge){result.add(user);}}
return result;
}

public boolean authenticateUser(String email,String password){
User user=findUserByEmail(email);if(user==null)return false;
if(!user.getPassword().equals(password))return false;
String sessionId=UUID.randomUUID().toString();userSessions.put(sessionId,email);
if(userSessions.size()>MAX_SESSIONS){cleanupOldSessions();}
return true;
}

private void cleanupOldSessions(){
// 임시 구현 - 첫 번째 세션 제거
Iterator<String>it=userSessions.keySet().iterator();
if(it.hasNext()){it.next();it.remove();}
}

class User{private String name;private String email;private int age;private String password;
public User(String name,String email,int age){this.name=name;this.email=email;this.age=age;this.password="default123";}
public String getName(){return name;}public String getEmail(){return email;}public int getAge(){return age;}public String getPassword(){return password;}
}
}
```

#### Python 예시 - 데이터 분석 시스템
```python
# Bad: 형식이 엉망인 Python 코드
import pandas as pd,numpy as np,matplotlib.pyplot as plt
from datetime import datetime,timedelta
class DataAnalyzer:
def __init__(self,data_source):self.data_source=data_source;self.df=None;self.processed_data={}
def load_data(self):
try:self.df=pd.read_csv(self.data_source)
except Exception as e:print(f"Error loading data: {e}");return False
return True
def clean_data(self):
if self.df is None:return False
self.df=self.df.dropna()
for col in self.df.columns:
if self.df[col].dtype=='object':self.df[col]=self.df[col].str.strip()
self.df=self.df.drop_duplicates()
return True
def analyze_sales_by_month(self):
if 'date' not in self.df.columns or 'sales' not in self.df.columns:return None
self.df['date']=pd.to_datetime(self.df['date'])
monthly_sales=self.df.groupby(self.df['date'].dt.to_period('M'))['sales'].sum()
self.processed_data['monthly_sales']=monthly_sales;return monthly_sales
def generate_report(self):
if not self.processed_data:return "No data to report"
report=""
for key,value in self.processed_data.items():report+=f"{key}:\n{value}\n\n"
return report
def plot_data(self,chart_type='line'):
if 'monthly_sales' not in self.processed_data:return
data=self.processed_data['monthly_sales']
plt.figure(figsize=(10,6))
if chart_type=='line':plt.plot(data.index.astype(str),data.values)
elif chart_type=='bar':plt.bar(range(len(data)),data.values)
plt.title('Monthly Sales Analysis')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### 개선 과제

다음 형식화 원칙을 적용하여 코드를 개선하세요:

1. **수직 형식화**
   - 적절한 빈 줄로 논리적 블록 구분
   - 관련된 코드들 밀접하게 배치
   - 변수 선언과 사용을 가깝게 위치

2. **수평 형식화**
   - 적절한 들여쓰기와 공백 사용
   - 연산자 주변 공백 배치
   - 행 길이 제한 (80-120자)

3. **팀 규칙**
   - 일관된 중괄호 위치
   - 통일된 명명 규칙
   - 임포트 구문 정리

### 개선 결과 템플릿

#### Java 개선 결과
```java
// Good: 깔끔하게 형식화된 코드
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class UserManager {
    private static final int MAX_SESSIONS = 100;
    
    private final List<User> users;
    private final Map<String, String> userSessions;
    
    public UserManager() {
        this.users = new ArrayList<>();
        this.userSessions = new HashMap<>();
    }
    
    public boolean addUser(String name, String email, int age) {
        if (!isValidName(name)) {
            return false;
        }
        
        if (!isValidEmail(email)) {
            return false;
        }
        
        if (!isValidAge(age)) {
            return false;
        }
        
        User newUser = new User(name, email, age);
        users.add(newUser);
        
        return true;
    }
    
    public User findUserByEmail(String email) {
        if (email == null) {
            return null;
        }
        
        for (User user : users) {
            if (user.getEmail().equals(email)) {
                return user;
            }
        }
        
        return null;
    }
    
    public List<User> getUsersByAgeRange(int minAge, int maxAge) {
        List<User> result = new ArrayList<>();
        
        for (User user : users) {
            int userAge = user.getAge();
            if (userAge >= minAge && userAge <= maxAge) {
                result.add(user);
            }
        }
        
        return result;
    }
    
    public boolean authenticateUser(String email, String password) {
        User user = findUserByEmail(email);
        if (user == null) {
            return false;
        }
        
        if (!user.getPassword().equals(password)) {
            return false;
        }
        
        createUserSession(email);
        
        return true;
    }
    
    private boolean isValidName(String name) {
        return name != null && !name.trim().isEmpty();
    }
    
    private boolean isValidEmail(String email) {
        return email != null && email.contains("@");
    }
    
    private boolean isValidAge(int age) {
        return age >= 0 && age <= 150;
    }
    
    private void createUserSession(String email) {
        String sessionId = UUID.randomUUID().toString();
        userSessions.put(sessionId, email);
        
        if (userSessions.size() > MAX_SESSIONS) {
            cleanupOldSessions();
        }
    }
    
    private void cleanupOldSessions() {
        Iterator<String> iterator = userSessions.keySet().iterator();
        if (iterator.hasNext()) {
            iterator.next();
            iterator.remove();
        }
    }
    
    // Inner class with proper formatting
    public static class User {
        private final String name;
        private final String email;
        private final int age;
        private final String password;
        
        public User(String name, String email, int age) {
            this.name = name;
            this.email = email;
            this.age = age;
            this.password = "default123";
        }
        
        // Getters
        public String getName() { 
            return name; 
        }
        
        public String getEmail() { 
            return email; 
        }
        
        public int getAge() { 
            return age; 
        }
        
        public String getPassword() { 
            return password; 
        }
    }
}
```

#### Python 개선 결과
```python
# Good: 깔끔하게 형식화된 Python 코드
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class DataAnalyzer:
    """데이터 분석을 위한 클래스"""
    
    def __init__(self, data_source: str):
        """
        Args:
            data_source: CSV 파일 경로
        """
        self.data_source = data_source
        self.df = None
        self.processed_data = {}
    
    def load_data(self) -> bool:
        """CSV 파일에서 데이터를 로드합니다."""
        try:
            self.df = pd.read_csv(self.data_source)
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def clean_data(self) -> bool:
        """데이터를 정리합니다."""
        if self.df is None:
            return False
        
        # 결측값 제거
        self.df = self.df.dropna()
        
        # 문자열 컬럼 공백 제거
        string_columns = self.df.select_dtypes(include=['object']).columns
        for col in string_columns:
            self.df[col] = self.df[col].str.strip()
        
        # 중복 제거
        self.df = self.df.drop_duplicates()
        
        return True
    
    def analyze_sales_by_month(self) -> pd.Series:
        """월별 매출을 분석합니다."""
        required_columns = ['date', 'sales']
        if not all(col in self.df.columns for col in required_columns):
            return None
        
        # 날짜 형식 변환
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # 월별 매출 집계
        monthly_sales = self.df.groupby(
            self.df['date'].dt.to_period('M')
        )['sales'].sum()
        
        self.processed_data['monthly_sales'] = monthly_sales
        
        return monthly_sales
    
    def generate_report(self) -> str:
        """분석 결과 보고서를 생성합니다."""
        if not self.processed_data:
            return "No data to report"
        
        report_lines = []
        for key, value in self.processed_data.items():
            report_lines.append(f"{key}:")
            report_lines.append(str(value))
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def plot_data(self, chart_type: str = 'line') -> None:
        """데이터를 시각화합니다."""
        if 'monthly_sales' not in self.processed_data:
            print("Monthly sales data not available")
            return
        
        data = self.processed_data['monthly_sales']
        
        plt.figure(figsize=(12, 6))
        
        if chart_type == 'line':
            plt.plot(data.index.astype(str), data.values, marker='o')
        elif chart_type == 'bar':
            plt.bar(range(len(data)), data.values)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        self._configure_plot()
        plt.show()
    
    def _configure_plot(self) -> None:
        """차트 설정을 구성합니다."""
        plt.title('Monthly Sales Analysis', fontsize=16, fontweight='bold')
        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Sales', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
```

### 형식화 체크리스트
```markdown
## 형식화 개선 체크리스트

### 수직 형식화
- [ ] 관련 있는 코드들을 세로로 가깝게 배치
- [ ] 빈 줄을 사용해 논리적 블록 구분
- [ ] 변수 선언을 사용 위치 근처에 배치
- [ ] 메서드 순서를 논리적으로 배치

### 수평 형식화
- [ ] 연산자 주변에 적절한 공백
- [ ] 메서드 인수 사이에 공백
- [ ] 행 길이 제한 준수 (80-120자)
- [ ] 일관된 들여쓰기

### 일관성
- [ ] 중괄호 위치 통일
- [ ] 네이밍 규칙 일관성
- [ ] 임포트 구문 정리
- [ ] 주석 스타일 통일

### 개선 효과
| 항목 | Before | After | 개선점 |
|------|--------|--------|---------|
| 가독성 | 매우 어려움 | 쉬움 | 논리적 구조 명확화 |
| 유지보수 | 어려움 | 쉬움 | 코드 블록 구분 명확 |
| 협업 | 매우 어려움 | 원활 | 일관된 스타일 적용 |
```

## 실습 2: 스타일 가이드 작성 (35분)

### 목표
팀 프로젝트용 포괄적인 코딩 스타일 가이드 문서를 작성합니다.

### 스타일 가이드 템플릿

```markdown
# 팀 프로젝트 코딩 스타일 가이드

## 1. 기본 원칙

### 일관성
- 프로젝트 전체에서 동일한 스타일 적용
- 기존 코드 스타일을 존중하고 따름
- 개인 취향보다는 팀 합의 우선

### 가독성
- 코드를 읽는 사람을 고려한 작성
- 명확하고 이해하기 쉬운 구조
- 적절한 공백과 들여쓰기 활용

### 유지보수성
- 코드 수정이 쉽도록 구조화
- 논리적 블록 단위로 코드 조직
- 변경 영향도를 최소화하는 형식

## 2. 언어별 상세 규칙

### Java 스타일 규칙

#### 들여쓰기 및 공백
```java
// Good: 4칸 들여쓰기
public class Calculator {
    private int result = 0;
    
    public int add(int a, int b) {
        if (a > 0 && b > 0) {
            result = a + b;
            return result;
        }
        return 0;
    }
}

// Bad: 불일치하는 들여쓰기
public class Calculator {
  private int result = 0;
      
public int add(int a,int b){
if(a>0&&b>0){
result=a+b;
return result;
}
return 0;
}
}
```

#### 중괄호 규칙
```java
// Good: K&R 스타일 (여는 중괄호는 같은 줄)
if (condition) {
    doSomething();
} else {
    doSomethingElse();
}

// 메서드와 클래스는 새 줄에 여는 중괄호
public class MyClass 
{
    public void myMethod() 
    {
        // 구현
    }
}
```

#### 행 길이 및 줄 바꿈
```java
// Good: 행 길이 100자 이내
public boolean validateUserInput(String name, String email, 
                                int age, String phoneNumber) {
    return isValidName(name) 
        && isValidEmail(email) 
        && isValidAge(age) 
        && isValidPhone(phoneNumber);
}

// 메서드 체이닝 시 줄 바꿈
user.setName("John")
    .setEmail("john@example.com")
    .setAge(25)
    .save();
```

#### 빈 줄 사용
```java
public class UserService {
    private final UserRepository repository;
    private final EmailService emailService;
    
    // 생성자와 필드 사이 빈 줄
    public UserService(UserRepository repository, EmailService emailService) {
        this.repository = repository;
        this.emailService = emailService;
    }
    
    // 메서드 사이 빈 줄
    public User createUser(String name, String email) {
        User user = new User(name, email);
        repository.save(user);
        
        // 논리적 블록 사이 빈 줄
        emailService.sendWelcomeEmail(user);
        
        return user;
    }
    
    public void deleteUser(Long userId) {
        repository.deleteById(userId);
    }
}
```

### Python 스타일 규칙 (PEP 8 기반)

#### 들여쓰기 및 공백
```python
# Good: 4칸 들여쓰기
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, a: int, b: int) -> int:
        if a > 0 and b > 0:
            self.result = a + b
            return self.result
        return 0

# 연산자 주변 공백
x = a + b
y = (a + b) * c
z = function(arg1, arg2, arg3)
```

#### 행 길이 및 줄 바꿈
```python
# Good: 행 길이 88자 이내 (Black formatter 기준)
def validate_user_input(
    name: str, 
    email: str, 
    age: int, 
    phone_number: str
) -> bool:
    return (
        is_valid_name(name)
        and is_valid_email(email) 
        and is_valid_age(age)
        and is_valid_phone(phone_number)
    )

# 긴 문자열 처리
message = (
    "This is a very long message that needs to be "
    "split across multiple lines to maintain "
    "readability and comply with line length limits."
)
```

#### 임포트 순서
```python
# 1. 표준 라이브러리
import os
import sys
from datetime import datetime

# 2. 서드파티 라이브러리  
import numpy as np
import pandas as pd
import requests

# 3. 로컬 애플리케이션/라이브러리
from myproject.models import User
from myproject.utils import helper_function
```

### JavaScript/TypeScript 스타일 규칙

#### 들여쓰기 및 세미콜론
```javascript
// Good: 2칸 들여쓰기, 세미콜론 사용
class Calculator {
  constructor() {
    this.result = 0;
  }
  
  add(a, b) {
    if (a > 0 && b > 0) {
      this.result = a + b;
      return this.result;
    }
    return 0;
  }
}

// 객체 리터럴
const user = {
  name: 'John',
  email: 'john@example.com',
  age: 25,
};
```

#### 함수 선언 vs 화살표 함수
```javascript
// 일반 함수 선언
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// 화살표 함수 (간단한 경우)
const multiply = (a, b) => a * b;

// 화살표 함수 (복잡한 경우)
const processUserData = (userData) => {
  const validatedData = validateData(userData);
  const processedData = transformData(validatedData);
  return processedData;
};
```

## 3. 공통 형식화 규칙

### 네이밍 컨벤션
| 요소 | Java | Python | JavaScript |
|------|------|--------|------------|
| 클래스 | PascalCase | PascalCase | PascalCase |
| 메서드/함수 | camelCase | snake_case | camelCase |
| 변수 | camelCase | snake_case | camelCase |
| 상수 | SCREAMING_SNAKE_CASE | SCREAMING_SNAKE_CASE | SCREAMING_SNAKE_CASE |
| 패키지/모듈 | lowercase | snake_case | kebab-case |

### 주석 스타일
```java
// Java
/**
 * 클래스나 공개 메서드용 JavaDoc
 */
public class Example {
    // 한 줄 주석은 // 사용
    /* 여러 줄 주석은 이렇게 */
}
```

```python
# Python
class Example:
    """클래스용 docstring"""
    
    def method(self):
        """메서드용 docstring"""
        # 한 줄 주석은 # 사용
        pass
```

```javascript
// JavaScript
/**
 * JSDoc 스타일 주석
 */
class Example {
  // 한 줄 주석
  /* 여러 줄 주석 */
}
```

## 4. 파일 및 프로젝트 구조

### 파일 명명 규칙
- Java: `ClassName.java`
- Python: `module_name.py`
- JavaScript: `fileName.js` 또는 `component-name.js`

### 디렉토리 구조
```
project/
├── src/
│   ├── main/
│   │   ├── java/com/company/project/
│   │   └── resources/
│   └── test/
├── docs/
├── config/
└── README.md
```

## 5. 도구 및 자동화

### 권장 포맷터
- **Java**: Google Java Format, Spotless
- **Python**: Black, isort
- **JavaScript**: Prettier, ESLint

### IDE 설정
```json
// VS Code settings.json 예시
{
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.formatOnSave": true,
  "java.format.settings.url": "https://raw.githubusercontent.com/google/styleguide/gh-pages/eclipse-java-google-style.xml",
  "python.formatting.provider": "black",
  "prettier.singleQuote": true,
  "prettier.trailingComma": "es5"
}
```

### Git 훅 설정
```bash
#!/bin/sh
# pre-commit hook 예시
echo "Running code formatter..."

# Java
if command -v google-java-format &> /dev/null; then
    find . -name "*.java" -exec google-java-format -i {} \;
fi

# Python
if command -v black &> /dev/null; then
    black --check .
fi

# JavaScript
if command -v prettier &> /dev/null; then
    prettier --check "**/*.{js,ts,json}"
fi
```

## 6. 예외 상황

### 레거시 코드
- 기존 파일 수정 시 해당 파일의 기존 스타일 유지
- 전면 리팩토링 시에만 새 스타일 적용

### 서드파티 코드
- 외부 라이브러리 코드는 원본 스타일 유지
- 래퍼 클래스 작성 시 팀 스타일 적용

### 성능 고려사항
- 성능상 이유로 스타일을 위반하는 경우 주석으로 설명
- 코드 리뷰에서 합당한 이유인지 검토
```

## 실습 3: 형식 분석 및 평가 (25분)

### 목표
오픈소스 프로젝트의 형식 규칙을 분석하고 평가합니다.

### 분석 대상 프로젝트 (선택)
1. **Spring Framework** (Java)
2. **Django** (Python)  
3. **React** (JavaScript)
4. **Vue.js** (JavaScript)

### 분석 과제

선택한 프로젝트의 GitHub 저장소에서 다음을 분석하세요:

1. **코딩 스타일 문서** 존재 여부
2. **자동화 도구** 사용 현황
3. **일관성** 평가
4. **좋은 점과 개선점** 도출

### 분석 템플릿

```markdown
# 오픈소스 프로젝트 형식 분석 보고서

## 분석 대상
- **프로젝트명**: [프로젝트 이름]
- **언어**: [주요 언어]
- **저장소**: [GitHub URL]
- **분석 일자**: [날짜]

## 1. 스타일 가이드 분석

### 공식 스타일 가이드
- [ ] 존재함 / [ ] 존재하지 않음
- **위치**: [링크 또는 파일 경로]
- **내용 요약**: 
  - 들여쓰기: ___ 칸
  - 행 길이 제한: ___ 자
  - 중괄호 스타일: K&R / Allman / Other
  - 네이밍 규칙: [설명]

### 실제 코드 스타일 확인
```[언어]
// 대표적인 코드 예시 (3-5개 파일에서 추출)
[코드 샘플]
```

## 2. 자동화 도구 분석

### 사용 중인 도구
- [ ] 코드 포맷터: [도구명]
- [ ] 린터: [도구명]  
- [ ] CI/CD 통합: [도구명]
- [ ] Git 훅: [설명]

### 설정 파일 분석
```[설정 파일 형식]
[설정 내용 예시]
```

## 3. 일관성 평가

### 긍정적 측면
- [ ] 프로젝트 전체 일관성 유지
- [ ] 명확한 형식 규칙
- [ ] 자동화된 스타일 체크
- [ ] 기여자 가이드 제공

### 개선 필요 사항
- [ ] 일부 파일의 스타일 불일치
- [ ] 오래된 코드의 형식 문제
- [ ] 설정 파일 누락
- [ ] 문서화 부족

## 4. 학습 포인트

### 도입할 만한 좋은 관행
1. [구체적인 관행 1]
   - 설명: [상세 설명]
   - 적용 방법: [구현 방안]

2. [구체적인 관행 2]
   - 설명: [상세 설명]  
   - 적용 방법: [구현 방안]

### 피해야 할 문제점
1. [문제점 1]
   - 문제 상황: [설명]
   - 해결 방안: [대안]

## 5. 팀 프로젝트 적용 제안

### 즉시 적용 가능한 요소
- [제안 1]: [구체적 실행 방법]
- [제안 2]: [구체적 실행 방법]

### 장기적 개선 방향
- [제안 1]: [로드맵]
- [제안 2]: [로드맵]

## 6. 결론
[전체적인 평가와 핵심 학습 내용 요약]
```

## 평가 기준

### 실습 1: 코드 형식화 개선 (40점)
- 수직 형식화 적용 (15점)
- 수평 형식화 적용 (15점)
- 일관성 있는 스타일 적용 (10점)

### 실습 2: 스타일 가이드 작성 (35점)
- 규칙의 구체성과 명확성 (20점)
- 실용성과 적용 가능성 (10점)
- 자동화 도구 연계 방안 (5점)

### 실습 3: 형식 분석 및 평가 (25점)
- 분석의 정확성과 깊이 (15점)
- 팀 프로젝트 적용 제안의 실용성 (10점)

## 제출 형식
- 파일명: `05_code-formatting-style_실습_[이름].md`
- 제출 기한: 다음 강의 시작 전
- 포함 내용: 
  - 개선된 코드
  - 스타일 가이드 문서
  - 오픈소스 분석 보고서

## 추가 자료
- [Google Style Guides](https://google.github.io/styleguide/)
- [PEP 8 - Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Prettier - Code Formatter](https://prettier.io/)
- [Black - Python Formatter](https://black.readthedocs.io/) 