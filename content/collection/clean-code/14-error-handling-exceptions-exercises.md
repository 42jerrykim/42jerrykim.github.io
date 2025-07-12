---
draft: true
---
# Chapter 7: 오류 처리 - 실습 과제

## 실습 개요
이 실습은 오류 코드를 예외 처리로 변환하고, 안전하고 깔끔한 오류 처리 구조를 설계하며, null 처리 개선을 통해 견고한 코드를 작성하는 것을 목표로 합니다.

## 실습 1: 오류 코드를 예외로 변환 (45분)

### 목표
기존의 오류 코드 방식을 예외 처리 방식으로 리팩토링하여 코드의 가독성과 유지보수성을 향상시킵니다.

### 리팩토링 대상 코드

#### Java 예시 - 파일 처리 시스템
```java
// Bad: 오류 코드 방식
public class FileProcessor {
    public static final int SUCCESS = 0;
    public static final int FILE_NOT_FOUND = 1;
    public static final int PERMISSION_DENIED = 2;
    public static final int INVALID_FORMAT = 3;
    public static final int IO_ERROR = 4;
    
    public int processFile(String fileName) {
        // 파일 존재 확인
        File file = new File(fileName);
        if (!file.exists()) {
            logError("File not found: " + fileName);
            return FILE_NOT_FOUND;
        }
        
        // 권한 확인
        if (!file.canRead()) {
            logError("Permission denied: " + fileName);
            return PERMISSION_DENIED;
        }
        
        // 파일 형식 확인
        if (!fileName.endsWith(".txt") && !fileName.endsWith(".csv")) {
            logError("Invalid file format: " + fileName);
            return INVALID_FORMAT;
        }
        
        try {
            // 파일 내용 읽기
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line;
            StringBuilder content = new StringBuilder();
            
            while ((line = reader.readLine()) != null) {
                // 각 줄의 형식 검증
                if (!isValidLine(line)) {
                    reader.close();
                    logError("Invalid line format in file: " + fileName);
                    return INVALID_FORMAT;
                }
                content.append(processLine(line));
            }
            reader.close();
            
            // 처리된 내용 저장
            writeToOutputFile(content.toString(), fileName);
            
        } catch (IOException e) {
            logError("IO Error processing file: " + fileName + " - " + e.getMessage());
            return IO_ERROR;
        }
        
        return SUCCESS;
    }
    
    // 호출자 코드 - 복잡한 오류 처리
    public void processMultipleFiles(String[] fileNames) {
        for (String fileName : fileNames) {
            int result = processFile(fileName);
            
            if (result == FILE_NOT_FOUND) {
                System.err.println("Skipping missing file: " + fileName);
                continue;
            } else if (result == PERMISSION_DENIED) {
                System.err.println("Access denied for file: " + fileName);
                continue;
            } else if (result == INVALID_FORMAT) {
                System.err.println("Invalid format in file: " + fileName);
                continue;
            } else if (result == IO_ERROR) {
                System.err.println("IO error processing file: " + fileName);
                break; // 심각한 오류이므로 중단
            } else if (result == SUCCESS) {
                System.out.println("Successfully processed: " + fileName);
            }
        }
    }
    
    private boolean isValidLine(String line) {
        return line != null && line.trim().length() > 0;
    }
    
    private String processLine(String line) {
        return line.toUpperCase();
    }
    
    private void writeToOutputFile(String content, String originalFileName) throws IOException {
        String outputFileName = originalFileName.replace(".", "_processed.");
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName))) {
            writer.write(content);
        }
    }
    
    private void logError(String message) {
        System.err.println("ERROR: " + message);
    }
}
```

### 개선 과제

다음 원칙을 적용하여 예외 처리 방식으로 변환하세요:

1. **오류 코드 대신 예외 사용**
2. **의미 있는 예외 클래스 설계**
3. **Try-Catch-Finally 구조 활용**
4. **호출자 코드 단순화**

### 리팩토링 결과 템플릿

#### Java 예외 처리 변환 결과
```java
// Good: 예외 처리 방식
// 1. 커스텀 예외 클래스들
public class FileProcessingException extends Exception {
    public FileProcessingException(String message) {
        super(message);
    }
    
    public FileProcessingException(String message, Throwable cause) {
        super(message, cause);
    }
}

public class FileNotFoundException extends FileProcessingException {
    public FileNotFoundException(String fileName) {
        super("File not found: " + fileName);
    }
}

public class FilePermissionException extends FileProcessingException {
    public FilePermissionException(String fileName) {
        super("Permission denied: " + fileName);
    }
}

public class InvalidFileFormatException extends FileProcessingException {
    public InvalidFileFormatException(String fileName, String reason) {
        super("Invalid file format in " + fileName + ": " + reason);
    }
}

public class FileIOException extends FileProcessingException {
    public FileIOException(String fileName, Throwable cause) {
        super("IO error processing file: " + fileName, cause);
    }
}

// 2. 개선된 FileProcessor
public class FileProcessor {
    private static final Set<String> SUPPORTED_EXTENSIONS = 
        Set.of(".txt", ".csv");
    
    public void processFile(String fileName) throws FileProcessingException {
        try {
            validateFile(fileName);
            String content = readAndProcessFile(fileName);
            writeProcessedContent(content, fileName);
        } catch (IOException e) {
            throw new FileIOException(fileName, e);
        }
    }
    
    private void validateFile(String fileName) throws FileProcessingException {
        File file = new File(fileName);
        
        if (!file.exists()) {
            throw new FileNotFoundException(fileName);
        }
        
        if (!file.canRead()) {
            throw new FilePermissionException(fileName);
        }
        
        if (!hasValidExtension(fileName)) {
            throw new InvalidFileFormatException(fileName, 
                "Supported formats: " + SUPPORTED_EXTENSIONS);
        }
    }
    
    private boolean hasValidExtension(String fileName) {
        return SUPPORTED_EXTENSIONS.stream()
                                 .anyMatch(fileName::endsWith);
    }
    
    private String readAndProcessFile(String fileName) 
            throws IOException, InvalidFileFormatException {
        
        try (BufferedReader reader = new BufferedReader(new FileReader(fileName))) {
            StringBuilder content = new StringBuilder();
            String line;
            int lineNumber = 0;
            
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                if (!isValidLine(line)) {
                    throw new InvalidFileFormatException(fileName, 
                        "Invalid line format at line " + lineNumber);
                }
                content.append(processLine(line)).append("\n");
            }
            
            return content.toString();
        }
    }
    
    private void writeProcessedContent(String content, String originalFileName) 
            throws IOException {
        String outputFileName = generateOutputFileName(originalFileName);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFileName))) {
            writer.write(content);
        }
    }
    
    // 3. 단순해진 호출자 코드
    public void processMultipleFiles(String[] fileNames) {
        for (String fileName : fileNames) {
            try {
                processFile(fileName);
                System.out.println("Successfully processed: " + fileName);
                
            } catch (FileNotFoundException e) {
                System.err.println("Skipping missing file: " + fileName);
                
            } catch (FilePermissionException e) {
                System.err.println("Access denied for file: " + fileName);
                
            } catch (InvalidFileFormatException e) {
                System.err.println("Format error: " + e.getMessage());
                
            } catch (FileIOException e) {
                System.err.println("IO error: " + e.getMessage());
                break; // 심각한 오류이므로 중단
                
            } catch (FileProcessingException e) {
                System.err.println("Unexpected error: " + e.getMessage());
            }
        }
    }
    
    private boolean isValidLine(String line) {
        return line != null && line.trim().length() > 0;
    }
    
    private String processLine(String line) {
        return line.toUpperCase();
    }
    
    private String generateOutputFileName(String originalFileName) {
        int dotIndex = originalFileName.lastIndexOf('.');
        if (dotIndex > 0) {
            return originalFileName.substring(0, dotIndex) + "_processed" + 
                   originalFileName.substring(dotIndex);
        }
        return originalFileName + "_processed";
    }
}
```

### 오류 처리 개선 체크리스트
```markdown
## 오류 처리 리팩토링 체크리스트

### Before & After 비교
| 항목 | Before (오류 코드) | After (예외 처리) |
|------|-------------------|-------------------|
| 반환값 | int 오류 코드 | void (예외로 오류 표현) |
| 오류 정보 | 제한적 (코드만) | 풍부함 (메시지, 원인, 스택 트레이스) |
| 호출자 코드 | 복잡한 조건문 | 명확한 try-catch 구조 |
| 오류 무시 | 쉬움 (반환값 확인 안 함) | 어려움 (예외 처리 강제) |
| 가독성 | 낮음 | 높음 |

### 적용된 예외 처리 원칙
- [ ] 오류 코드 대신 예외 사용
- [ ] 의미 있는 예외 클래스 정의
- [ ] 예외에 충분한 정보 포함
- [ ] Try-Catch-Finally 구조 활용
- [ ] 호출자를 고려한 예외 계층 구조
```

## 실습 2: Wrapper 클래스로 외부 라이브러리 예외 감싸기 (35분)

### 목표
외부 라이브러리의 예외를 감싸는 Wrapper 클래스를 구현하여 의존성을 줄이고 일관된 예외 처리를 제공합니다.

### 개선 대상 코드

```java
// Bad: 외부 라이브러리 예외를 직접 사용
public class DatabaseService {
    private Connection connection;
    
    public void saveUser(User user) throws SQLException, 
                                         ClassNotFoundException, 
                                         IllegalAccessException,
                                         InstantiationException {
        try {
            // 여러 외부 라이브러리 사용
            Class.forName("com.mysql.cj.jdbc.Driver");
            connection = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/userdb", "user", "password");
            
            PreparedStatement stmt = connection.prepareStatement(
                "INSERT INTO users (name, email) VALUES (?, ?)");
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getEmail());
            
            int result = stmt.executeUpdate();
            if (result == 0) {
                throw new SQLException("Failed to insert user");
            }
            
        } catch (SQLException e) {
            // 외부 라이브러리 예외를 그대로 전파
            throw e;
        } catch (ClassNotFoundException e) {
            throw e;
        }
    }
    
    public User findUser(String email) throws SQLException, ClassNotFoundException {
        try {
            PreparedStatement stmt = connection.prepareStatement(
                "SELECT * FROM users WHERE email = ?");
            stmt.setString(1, email);
            
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return new User(rs.getString("name"), rs.getString("email"));
            }
            return null;
            
        } catch (SQLException e) {
            throw e;
        }
    }
    
    // 호출자는 모든 외부 라이브러리 예외를 처리해야 함
    public void processUserRegistration(User user) {
        try {
            saveUser(user);
            System.out.println("User registered successfully");
        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
        } catch (ClassNotFoundException e) {
            System.err.println("Driver not found: " + e.getMessage());
        } catch (IllegalAccessException e) {
            System.err.println("Access error: " + e.getMessage());
        } catch (InstantiationException e) {
            System.err.println("Instantiation error: " + e.getMessage());
        }
    }
}
```

### 개선 과제

Wrapper 패턴을 사용하여 다음을 구현하세요:

1. **내부 예외 클래스 정의**
2. **외부 라이브러리 예외 변환**
3. **일관된 인터페이스 제공**
4. **의존성 격리**

### 개선 결과 템플릿

```java
// Good: Wrapper 클래스로 외부 의존성 격리
// 1. 내부 예외 계층 구조
public class DatabaseException extends Exception {
    public DatabaseException(String message) {
        super(message);
    }
    
    public DatabaseException(String message, Throwable cause) {
        super(message, cause);
    }
}

public class UserNotFoundException extends DatabaseException {
    public UserNotFoundException(String email) {
        super("User not found with email: " + email);
    }
}

public class DatabaseConnectionException extends DatabaseException {
    public DatabaseConnectionException(String message, Throwable cause) {
        super("Database connection failed: " + message, cause);
    }
}

public class DataPersistenceException extends DatabaseException {
    public DataPersistenceException(String operation, Throwable cause) {
        super("Failed to " + operation + " data", cause);
    }
}

// 2. Wrapper 클래스
public class DatabaseService {
    private final DatabaseConnectionManager connectionManager;
    
    public DatabaseService() {
        this.connectionManager = new DatabaseConnectionManager();
    }
    
    public void saveUser(User user) throws DatabaseException {
        try (Connection connection = connectionManager.getConnection()) {
            PreparedStatement stmt = connection.prepareStatement(
                "INSERT INTO users (name, email) VALUES (?, ?)");
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getEmail());
            
            int result = stmt.executeUpdate();
            if (result == 0) {
                throw new DataPersistenceException("insert user", 
                    new RuntimeException("No rows affected"));
            }
            
        } catch (SQLException e) {
            throw new DataPersistenceException("save user", e);
        } catch (Exception e) {
            throw new DatabaseConnectionException("Unable to save user", e);
        }
    }
    
    public User findUser(String email) throws DatabaseException {
        try (Connection connection = connectionManager.getConnection()) {
            PreparedStatement stmt = connection.prepareStatement(
                "SELECT * FROM users WHERE email = ?");
            stmt.setString(1, email);
            
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return new User(rs.getString("name"), rs.getString("email"));
            }
            
            throw new UserNotFoundException(email);
            
        } catch (SQLException e) {
            throw new DataPersistenceException("find user", e);
        } catch (UserNotFoundException e) {
            throw e; // 다시 던지기
        } catch (Exception e) {
            throw new DatabaseConnectionException("Unable to find user", e);
        }
    }
    
    // 3. 연결 관리 클래스 (외부 의존성 격리)
    private static class DatabaseConnectionManager {
        private static final String DRIVER_CLASS = "com.mysql.cj.jdbc.Driver";
        private static final String CONNECTION_URL = 
            "jdbc:mysql://localhost:3306/userdb";
        private static final String USERNAME = "user";
        private static final String PASSWORD = "password";
        
        static {
            try {
                Class.forName(DRIVER_CLASS);
            } catch (ClassNotFoundException e) {
                throw new RuntimeException("Database driver not found", e);
            }
        }
        
        public Connection getConnection() throws SQLException {
            return DriverManager.getConnection(CONNECTION_URL, USERNAME, PASSWORD);
        }
    }
}

// 4. 단순해진 호출자 코드
public class UserRegistrationService {
    private final DatabaseService databaseService;
    
    public UserRegistrationService(DatabaseService databaseService) {
        this.databaseService = databaseService;
    }
    
    public void processUserRegistration(User user) {
        try {
            databaseService.saveUser(user);
            System.out.println("User registered successfully: " + user.getEmail());
            
        } catch (DataPersistenceException e) {
            System.err.println("Failed to save user data: " + e.getMessage());
            
        } catch (DatabaseConnectionException e) {
            System.err.println("Database connection issue: " + e.getMessage());
            
        } catch (DatabaseException e) {
            System.err.println("Database error: " + e.getMessage());
        }
    }
    
    public User findExistingUser(String email) {
        try {
            return databaseService.findUser(email);
            
        } catch (UserNotFoundException e) {
            System.out.println("User not found, ready for new registration");
            return null;
            
        } catch (DatabaseException e) {
            System.err.println("Error checking existing user: " + e.getMessage());
            return null;
        }
    }
}
```

## 실습 3: null 처리 개선 (30분)

### 목표
null 반환과 null 전달을 제거하여 NullPointerException을 방지하고 코드의 안정성을 향상시킵니다.

### 개선 대상 코드

```java
// Bad: null을 반환하고 전달하는 코드
public class EmployeeService {
    private List<Employee> employees = new ArrayList<>();
    
    // null 반환 문제
    public Employee findEmployeeById(String id) {
        for (Employee emp : employees) {
            if (emp.getId().equals(id)) {
                return emp;
            }
        }
        return null; // 찾지 못하면 null 반환
    }
    
    // null 반환 문제
    public List<Employee> getEmployeesByDepartment(String department) {
        List<Employee> result = new ArrayList<>();
        for (Employee emp : employees) {
            if (emp.getDepartment().equals(department)) {
                result.add(emp);
            }
        }
        return result.isEmpty() ? null : result; // 빈 리스트 대신 null 반환
    }
    
    // null 전달 허용 문제
    public double calculateBonus(Employee employee, String performanceRating) {
        if (employee == null) {
            return 0.0; // null 방어 코드
        }
        
        if (performanceRating == null) {
            performanceRating = "AVERAGE"; // null 기본값 처리
        }
        
        double baseSalary = employee.getSalary();
        switch (performanceRating) {
            case "EXCELLENT": return baseSalary * 0.2;
            case "GOOD": return baseSalary * 0.1;
            case "AVERAGE": return baseSalary * 0.05;
            default: return 0.0;
        }
    }
    
    // 호출자에서 null 체크 필요
    public void processEmployeeBonus(String employeeId, String rating) {
        Employee employee = findEmployeeById(employeeId);
        if (employee != null) { // null 체크 필요
            double bonus = calculateBonus(employee, rating);
            if (bonus > 0) {
                System.out.println("Bonus for " + employee.getName() + ": $" + bonus);
            }
        } else {
            System.out.println("Employee not found: " + employeeId);
        }
    }
    
    public void printDepartmentEmployees(String department) {
        List<Employee> deptEmployees = getEmployeesByDepartment(department);
        if (deptEmployees != null) { // null 체크 필요
            for (Employee emp : deptEmployees) {
                System.out.println(emp.getName());
            }
        } else {
            System.out.println("No employees found in department: " + department);
        }
    }
}
```

### 개선 과제

다음 기법을 사용하여 null 처리를 개선하세요:

1. **Optional 사용**
2. **빈 컬렉션 반환**
3. **Special Case Object 패턴**
4. **null 전달 방지**

### 개선 결과 템플릿

```java
// Good: null을 제거한 안전한 코드
public class EmployeeService {
    private final List<Employee> employees = new ArrayList<>();
    
    // 1. Optional 사용 - null 대신 Optional 반환
    public Optional<Employee> findEmployeeById(String id) {
        if (id == null || id.trim().isEmpty()) {
            return Optional.empty();
        }
        
        return employees.stream()
                       .filter(emp -> id.equals(emp.getId()))
                       .findFirst();
    }
    
    // 2. 빈 컬렉션 반환 - null 대신 빈 리스트
    public List<Employee> getEmployeesByDepartment(String department) {
        if (department == null || department.trim().isEmpty()) {
            return Collections.emptyList();
        }
        
        return employees.stream()
                       .filter(emp -> department.equals(emp.getDepartment()))
                       .collect(Collectors.toList());
    }
    
    // 3. null 전달 방지 - 매개변수 검증
    public double calculateBonus(Employee employee, PerformanceRating rating) {
        Objects.requireNonNull(employee, "Employee cannot be null");
        Objects.requireNonNull(rating, "Performance rating cannot be null");
        
        double baseSalary = employee.getSalary();
        return baseSalary * rating.getBonusMultiplier();
    }
    
    // 4. 열거형으로 null 방지
    public enum PerformanceRating {
        EXCELLENT(0.2),
        GOOD(0.1),
        AVERAGE(0.05),
        POOR(0.0);
        
        private final double bonusMultiplier;
        
        PerformanceRating(double bonusMultiplier) {
            this.bonusMultiplier = bonusMultiplier;
        }
        
        public double getBonusMultiplier() {
            return bonusMultiplier;
        }
    }
    
    // 5. Optional과 함수형 스타일로 안전한 처리
    public void processEmployeeBonus(String employeeId, PerformanceRating rating) {
        findEmployeeById(employeeId)
            .map(employee -> calculateBonus(employee, rating))
            .filter(bonus -> bonus > 0)
            .ifPresentOrElse(
                bonus -> System.out.println("Bonus calculated: $" + bonus),
                () -> System.out.println("No bonus or employee not found: " + employeeId)
            );
    }
    
    // 6. 컬렉션 안전 처리
    public void printDepartmentEmployees(String department) {
        List<Employee> deptEmployees = getEmployeesByDepartment(department);
        
        if (deptEmployees.isEmpty()) {
            System.out.println("No employees found in department: " + department);
        } else {
            System.out.println("Employees in " + department + ":");
            deptEmployees.forEach(emp -> System.out.println("- " + emp.getName()));
        }
    }
    
    // 7. Special Case Object 패턴
    public Employee getEmployeeByIdOrDefault(String id) {
        return findEmployeeById(id)
                   .orElse(Employee.NULL_EMPLOYEE);
    }
}

// Special Case Object
public class Employee {
    public static final Employee NULL_EMPLOYEE = new NullEmployee();
    
    private String id;
    private String name;
    private String department;
    private double salary;
    
    // 생성자, getter, setter...
    
    public boolean isNull() {
        return false;
    }
    
    // Null Object 구현
    private static class NullEmployee extends Employee {
        public NullEmployee() {
            super("", "Unknown Employee", "Unknown", 0.0);
        }
        
        @Override
        public boolean isNull() {
            return true;
        }
        
        @Override
        public String toString() {
            return "No Employee Found";
        }
    }
}

// 8. 입력 검증 유틸리티
public class ValidationUtils {
    public static String requireNonNullAndNotEmpty(String value, String paramName) {
        if (value == null) {
            throw new IllegalArgumentException(paramName + " cannot be null");
        }
        if (value.trim().isEmpty()) {
            throw new IllegalArgumentException(paramName + " cannot be empty");
        }
        return value.trim();
    }
    
    public static <T> T requireNonNull(T value, String paramName) {
        if (value == null) {
            throw new IllegalArgumentException(paramName + " cannot be null");
        }
        return value;
    }
}
```

### null 처리 개선 체크리스트
```markdown
## null 처리 개선 체크리스트

### null 반환 제거
- [ ] Optional 사용으로 null 반환 방지
- [ ] 빈 컬렉션 반환 (Collections.emptyList() 등)
- [ ] Special Case Object 패턴 적용
- [ ] 기본값 제공 메서드 구현

### null 전달 방지
- [ ] 매개변수 null 검증
- [ ] Objects.requireNonNull() 사용
- [ ] 입력 검증 유틸리티 활용
- [ ] 불변 객체 사용

### 안전한 코드 패턴
- [ ] Optional.map(), flatMap() 활용
- [ ] Stream API의 null 안전 메서드 사용
- [ ] 열거형으로 상수 관리
- [ ] 방어적 복사 적용

### 개선 효과
| 항목 | Before | After |
|------|--------|--------|
| NullPointerException | 자주 발생 | 거의 없음 |
| null 체크 코드 | 많음 | 최소화 |
| 가독성 | 낮음 | 높음 |
| 안정성 | 낮음 | 높음 |
```

## 평가 기준

### 실습 1: 오류 코드를 예외로 변환 (40점)
- 적절한 예외 클래스 설계 (15점)
- 오류 코드 제거 완성도 (15점)
- 호출자 코드 단순화 (10점)

### 실습 2: Wrapper 클래스 구현 (35점)
- 외부 의존성 격리 정도 (15점)
- 예외 변환의 적절성 (10점)
- 일관된 인터페이스 제공 (10점)

### 실습 3: null 처리 개선 (25점)
- Optional 활용 능력 (10점)
- null 반환/전달 제거 (10점)
- 안전한 코드 패턴 적용 (5점)

## 제출 형식
- 파일명: `07_error-handling-exceptions_실습_[이름].md`
- 제출 기한: 다음 강의 시작 전
- 포함 내용: 
  - 리팩토링된 코드
  - Before/After 비교 분석
  - 적용한 원칙 설명

## 추가 자료
- [Effective Java - 예외 처리](https://www.oracle.com/java/technologies/javase/javadoc.html)
- [Java Optional 사용 가이드](https://docs.oracle.com/javase/8/docs/api/java/util/Optional.html)
- [Spring Framework 예외 처리 전략](https://spring.io/guides)
- Vavr 라이브러리의 Try, Either 타입 소개 