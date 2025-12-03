---
draft: true
---
# Chapter 10: 클래스 - 실습 과제

## 실습 개요
이 실습은 클래스의 캡슐화, 단일 책임 원칙(SRP), 응집도 향상, 결합도 감소를 통해 깔끔하고 유지보수가 용이한 클래스를 설계하는 것을 목표로 합니다.

## 실습 1: 단일 책임 원칙(SRP) 적용 (45분)

### 목표
하나의 클래스가 여러 책임을 가지고 있는 코드를 단일 책임 원칙에 따라 분리하여 유지보수성을 향상시킵니다.

### 리팩토링 대상 코드

#### Java 예시 - 사용자 관리 클래스
```java
// Bad: 여러 책임을 가진 클래스
public class UserManager {
    private List<User> users = new ArrayList<>();
    private Connection dbConnection;
    private EmailService emailService;
    
    // 생성자
    public UserManager() {
        try {
            // 데이터베이스 연결 초기화
            Class.forName("com.mysql.cj.jdbc.Driver");
            this.dbConnection = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/userdb", "user", "password");
            this.emailService = new EmailService();
            loadUsersFromDatabase();
        } catch (Exception e) {
            throw new RuntimeException("Failed to initialize UserManager", e);
        }
    }
    
    // 책임 1: 사용자 비즈니스 로직
    public boolean isValidUser(User user) {
        if (user == null || user.getEmail() == null || user.getName() == null) {
            return false;
        }
        
        // 이메일 형식 검증
        String emailRegex = "^[A-Za-z0-9+_.-]+@(.+)$";
        if (!user.getEmail().matches(emailRegex)) {
            return false;
        }
        
        // 이름 길이 검증
        if (user.getName().trim().length() < 2) {
            return false;
        }
        
        // 나이 검증
        if (user.getAge() < 0 || user.getAge() > 120) {
            return false;
        }
        
        return true;
    }
    
    public User createUser(String name, String email, int age) {
        User user = new User(name, email, age);
        if (!isValidUser(user)) {
            throw new IllegalArgumentException("Invalid user data");
        }
        
        // 중복 이메일 확인
        if (findUserByEmail(email) != null) {
            throw new IllegalArgumentException("Email already exists: " + email);
        }
        
        return user;
    }
    
    // 책임 2: 데이터베이스 액세스
    public void saveUser(User user) {
        try {
            String sql = "INSERT INTO users (name, email, age, created_date) VALUES (?, ?, ?, ?)";
            PreparedStatement stmt = dbConnection.prepareStatement(sql);
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getEmail());
            stmt.setInt(3, user.getAge());
            stmt.setTimestamp(4, new Timestamp(System.currentTimeMillis()));
            
            int result = stmt.executeUpdate();
            if (result > 0) {
                users.add(user);
                System.out.println("User saved to database: " + user.getEmail());
            }
            
        } catch (SQLException e) {
            throw new RuntimeException("Failed to save user", e);
        }
    }
    
    public User findUserByEmail(String email) {
        try {
            String sql = "SELECT * FROM users WHERE email = ?";
            PreparedStatement stmt = dbConnection.prepareStatement(sql);
            stmt.setString(1, email);
            
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                return new User(
                    rs.getString("name"),
                    rs.getString("email"), 
                    rs.getInt("age")
                );
            }
            return null;
            
        } catch (SQLException e) {
            throw new RuntimeException("Failed to find user", e);
        }
    }
    
    private void loadUsersFromDatabase() {
        try {
            String sql = "SELECT * FROM users";
            Statement stmt = dbConnection.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
            
            while (rs.next()) {
                User user = new User(
                    rs.getString("name"),
                    rs.getString("email"),
                    rs.getInt("age")
                );
                users.add(user);
            }
            
        } catch (SQLException e) {
            throw new RuntimeException("Failed to load users", e);
        }
    }
    
    // 책임 3: 이메일 발송
    public void sendWelcomeEmail(User user) {
        try {
            String subject = "Welcome to Our Service!";
            String body = generateWelcomeEmailBody(user);
            
            emailService.sendEmail(user.getEmail(), subject, body);
            System.out.println("Welcome email sent to: " + user.getEmail());
            
        } catch (Exception e) {
            System.err.println("Failed to send welcome email: " + e.getMessage());
        }
    }
    
    private String generateWelcomeEmailBody(User user) {
        StringBuilder body = new StringBuilder();
        body.append("Dear ").append(user.getName()).append(",\n\n");
        body.append("Welcome to our service! We're excited to have you on board.\n");
        body.append("Your account has been successfully created with email: ");
        body.append(user.getEmail()).append("\n\n");
        body.append("Best regards,\nThe Team");
        return body.toString();
    }
    
    // 책임 4: 리포팅
    public void generateUserReport() {
        try {
            StringBuilder report = new StringBuilder();
            report.append("=== USER REPORT ===\n");
            report.append("Total Users: ").append(users.size()).append("\n");
            report.append("Generated: ").append(new Date()).append("\n\n");
            
            // 나이별 통계
            Map<String, Integer> ageGroups = new HashMap<>();
            ageGroups.put("Under 20", 0);
            ageGroups.put("20-30", 0);
            ageGroups.put("30-40", 0);
            ageGroups.put("Over 40", 0);
            
            for (User user : users) {
                if (user.getAge() < 20) {
                    ageGroups.put("Under 20", ageGroups.get("Under 20") + 1);
                } else if (user.getAge() < 30) {
                    ageGroups.put("20-30", ageGroups.get("20-30") + 1);
                } else if (user.getAge() < 40) {
                    ageGroups.put("30-40", ageGroups.get("30-40") + 1);
                } else {
                    ageGroups.put("Over 40", ageGroups.get("Over 40") + 1);
                }
            }
            
            report.append("Age Groups:\n");
            for (Map.Entry<String, Integer> entry : ageGroups.entrySet()) {
                report.append("  ").append(entry.getKey()).append(": ")
                      .append(entry.getValue()).append("\n");
            }
            
            // 파일로 저장
            String fileName = "user_report_" + System.currentTimeMillis() + ".txt";
            try (FileWriter writer = new FileWriter(fileName)) {
                writer.write(report.toString());
                System.out.println("Report generated: " + fileName);
            }
            
        } catch (IOException e) {
            throw new RuntimeException("Failed to generate report", e);
        }
    }
    
    // 책임 5: 캐시 관리
    private Map<String, User> userCache = new HashMap<>();
    
    public User getCachedUser(String email) {
        if (userCache.containsKey(email)) {
            System.out.println("User retrieved from cache: " + email);
            return userCache.get(email);
        }
        
        User user = findUserByEmail(email);
        if (user != null) {
            userCache.put(email, user);
            System.out.println("User cached: " + email);
        }
        
        return user;
    }
    
    public void clearCache() {
        userCache.clear();
        System.out.println("User cache cleared");
    }
    
    // 리소스 정리
    public void cleanup() {
        try {
            if (dbConnection != null && !dbConnection.isClosed()) {
                dbConnection.close();
            }
            clearCache();
        } catch (SQLException e) {
            System.err.println("Error closing database connection: " + e.getMessage());
        }
    }
}

// User 클래스
public class User {
    private String name;
    private String email;
    private int age;
    
    public User(String name, String email, int age) {
        this.name = name;
        this.email = email;
        this.age = age;
    }
    
    // getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
}

// 사용 예시
public class UserService {
    public void registerNewUser(String name, String email, int age) {
        UserManager userManager = new UserManager();
        try {
            User user = userManager.createUser(name, email, age);
            userManager.saveUser(user);
            userManager.sendWelcomeEmail(user);
            userManager.generateUserReport();
        } finally {
            userManager.cleanup();
        }
    }
}
```

### 개선 과제

단일 책임 원칙을 적용하여 다음과 같이 클래스를 분리하세요:

1. **UserValidator** - 사용자 검증 로직
2. **UserRepository** - 데이터베이스 액세스
3. **UserEmailService** - 이메일 발송
4. **UserReportGenerator** - 리포트 생성
5. **UserCacheManager** - 캐시 관리
6. **UserService** - 비즈니스 로직 조정

### 개선 결과 템플릿

```java
// Good: 단일 책임 원칙을 적용한 클래스 분리

// 1. 사용자 검증 전담 클래스
public class UserValidator {
    private static final String EMAIL_REGEX = "^[A-Za-z0-9+_.-]+@(.+)$";
    private static final int MIN_NAME_LENGTH = 2;
    private static final int MIN_AGE = 0;
    private static final int MAX_AGE = 120;
    
    public ValidationResult validate(User user) {
        ValidationResult result = new ValidationResult();
        
        if (user == null) {
            result.addError("User cannot be null");
            return result;
        }
        
        validateName(user.getName(), result);
        validateEmail(user.getEmail(), result);
        validateAge(user.getAge(), result);
        
        return result;
    }
    
    private void validateName(String name, ValidationResult result) {
        if (name == null || name.trim().length() < MIN_NAME_LENGTH) {
            result.addError("Name must be at least " + MIN_NAME_LENGTH + " characters");
        }
    }
    
    private void validateEmail(String email, ValidationResult result) {
        if (email == null || !email.matches(EMAIL_REGEX)) {
            result.addError("Invalid email format");
        }
    }
    
    private void validateAge(int age, ValidationResult result) {
        if (age < MIN_AGE || age > MAX_AGE) {
            result.addError("Age must be between " + MIN_AGE + " and " + MAX_AGE);
        }
    }
}

// 검증 결과 클래스
public class ValidationResult {
    private final List<String> errors = new ArrayList<>();
    
    public void addError(String error) {
        errors.add(error);
    }
    
    public boolean isValid() {
        return errors.isEmpty();
    }
    
    public List<String> getErrors() {
        return new ArrayList<>(errors);
    }
    
    public String getErrorMessage() {
        return String.join(", ", errors);
    }
}

// 2. 데이터베이스 액세스 전담 클래스
public class UserRepository {
    private final DatabaseConnection dbConnection;
    
    public UserRepository(DatabaseConnection dbConnection) {
        this.dbConnection = dbConnection;
    }
    
    public void save(User user) throws UserRepositoryException {
        try {
            String sql = "INSERT INTO users (name, email, age, created_date) VALUES (?, ?, ?, ?)";
            PreparedStatement stmt = dbConnection.prepareStatement(sql);
            stmt.setString(1, user.getName());
            stmt.setString(2, user.getEmail());
            stmt.setInt(3, user.getAge());
            stmt.setTimestamp(4, new Timestamp(System.currentTimeMillis()));
            
            int result = stmt.executeUpdate();
            if (result == 0) {
                throw new UserRepositoryException("Failed to save user: no rows affected");
            }
            
        } catch (SQLException e) {
            throw new UserRepositoryException("Failed to save user: " + user.getEmail(), e);
        }
    }
    
    public Optional<User> findByEmail(String email) throws UserRepositoryException {
        try {
            String sql = "SELECT * FROM users WHERE email = ?";
            PreparedStatement stmt = dbConnection.prepareStatement(sql);
            stmt.setString(1, email);
            
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                User user = new User(
                    rs.getString("name"),
                    rs.getString("email"),
                    rs.getInt("age")
                );
                return Optional.of(user);
            }
            
            return Optional.empty();
            
        } catch (SQLException e) {
            throw new UserRepositoryException("Failed to find user: " + email, e);
        }
    }
    
    public List<User> findAll() throws UserRepositoryException {
        try {
            List<User> users = new ArrayList<>();
            String sql = "SELECT * FROM users";
            Statement stmt = dbConnection.createStatement();
            ResultSet rs = stmt.executeQuery(sql);
            
            while (rs.next()) {
                User user = new User(
                    rs.getString("name"),
                    rs.getString("email"),
                    rs.getInt("age")
                );
                users.add(user);
            }
            
            return users;
            
        } catch (SQLException e) {
            throw new UserRepositoryException("Failed to load users", e);
        }
    }
    
    public boolean existsByEmail(String email) throws UserRepositoryException {
        return findByEmail(email).isPresent();
    }
}

// 3. 이메일 발송 전담 클래스
public class UserEmailService {
    private final EmailSender emailSender;
    private final EmailTemplateEngine templateEngine;
    
    public UserEmailService(EmailSender emailSender, EmailTemplateEngine templateEngine) {
        this.emailSender = emailSender;
        this.templateEngine = templateEngine;
    }
    
    public void sendWelcomeEmail(User user) throws EmailServiceException {
        try {
            Email welcomeEmail = createWelcomeEmail(user);
            emailSender.send(welcomeEmail);
        } catch (Exception e) {
            throw new EmailServiceException("Failed to send welcome email to: " + user.getEmail(), e);
        }
    }
    
    private Email createWelcomeEmail(User user) {
        Map<String, Object> templateData = new HashMap<>();
        templateData.put("userName", user.getName());
        templateData.put("userEmail", user.getEmail());
        
        String subject = "Welcome to Our Service!";
        String body = templateEngine.render("welcome_email_template", templateData);
        
        return new Email(user.getEmail(), subject, body);
    }
}

// 4. 리포트 생성 전담 클래스
public class UserReportGenerator {
    public void generateReport(List<User> users, String outputPath) throws ReportGenerationException {
        try {
            UserReport report = createUserReport(users);
            saveReportToFile(report, outputPath);
        } catch (IOException e) {
            throw new ReportGenerationException("Failed to generate user report", e);
        }
    }
    
    private UserReport createUserReport(List<User> users) {
        UserStatistics statistics = calculateStatistics(users);
        return new UserReport(users.size(), new Date(), statistics);
    }
    
    private UserStatistics calculateStatistics(List<User> users) {
        Map<String, Integer> ageGroups = new HashMap<>();
        ageGroups.put("Under 20", 0);
        ageGroups.put("20-30", 0);
        ageGroups.put("30-40", 0);
        ageGroups.put("Over 40", 0);
        
        for (User user : users) {
            String ageGroup = categorizeAge(user.getAge());
            ageGroups.put(ageGroup, ageGroups.get(ageGroup) + 1);
        }
        
        return new UserStatistics(ageGroups);
    }
    
    private String categorizeAge(int age) {
        if (age < 20) return "Under 20";
        if (age < 30) return "20-30";
        if (age < 40) return "30-40";
        return "Over 40";
    }
    
    private void saveReportToFile(UserReport report, String outputPath) throws IOException {
        String fileName = outputPath + "/user_report_" + System.currentTimeMillis() + ".txt";
        try (FileWriter writer = new FileWriter(fileName)) {
            writer.write(report.toString());
        }
    }
}

// 5. 캐시 관리 전담 클래스
public class UserCacheManager {
    private final Map<String, User> cache = new HashMap<>();
    private final UserRepository userRepository;
    
    public UserCacheManager(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public Optional<User> get(String email) {
        User cachedUser = cache.get(email);
        if (cachedUser != null) {
            return Optional.of(cachedUser);
        }
        
        try {
            Optional<User> user = userRepository.findByEmail(email);
            user.ifPresent(u -> cache.put(email, u));
            return user;
        } catch (UserRepositoryException e) {
            return Optional.empty();
        }
    }
    
    public void put(String email, User user) {
        cache.put(email, user);
    }
    
    public void remove(String email) {
        cache.remove(email);
    }
    
    public void clear() {
        cache.clear();
    }
    
    public int size() {
        return cache.size();
    }
}

// 6. 비즈니스 로직 조정 클래스
public class UserService {
    private final UserValidator validator;
    private final UserRepository repository;
    private final UserEmailService emailService;
    private final UserCacheManager cacheManager;
    
    public UserService(UserValidator validator, 
                      UserRepository repository,
                      UserEmailService emailService,
                      UserCacheManager cacheManager) {
        this.validator = validator;
        this.repository = repository;
        this.emailService = emailService;
        this.cacheManager = cacheManager;
    }
    
    public User registerUser(String name, String email, int age) throws UserServiceException {
        try {
            // 사용자 생성 및 검증
            User user = new User(name, email, age);
            ValidationResult validationResult = validator.validate(user);
            
            if (!validationResult.isValid()) {
                throw new UserServiceException("Invalid user data: " + validationResult.getErrorMessage());
            }
            
            // 중복 이메일 확인
            if (repository.existsByEmail(email)) {
                throw new UserServiceException("User already exists with email: " + email);
            }
            
            // 사용자 저장
            repository.save(user);
            
            // 캐시에 추가
            cacheManager.put(email, user);
            
            // 환영 이메일 발송
            emailService.sendWelcomeEmail(user);
            
            return user;
            
        } catch (UserRepositoryException | EmailServiceException e) {
            throw new UserServiceException("Failed to register user: " + email, e);
        }
    }
    
    public Optional<User> findUser(String email) throws UserServiceException {
        try {
            return cacheManager.get(email);
        } catch (Exception e) {
            throw new UserServiceException("Failed to find user: " + email, e);
        }
    }
}
```

## 실습 2: 클래스 응집도 향상 (35분)

### 목표
관련성이 낮은 메서드들이 한 클래스에 모여 있는 코드를 높은 응집도를 가지도록 리팩토링합니다.

### 개선 대상 코드

```java
// Bad: 낮은 응집도를 가진 유틸리티 클래스
public class MixedUtilities {
    
    // 문자열 관련 메서드들
    public static String reverseString(String str) {
        return new StringBuilder(str).reverse().toString();
    }
    
    public static boolean isPalindrome(String str) {
        String reversed = reverseString(str.toLowerCase());
        return str.toLowerCase().equals(reversed);
    }
    
    public static String capitalizeWords(String str) {
        String[] words = str.split(" ");
        StringBuilder result = new StringBuilder();
        for (String word : words) {
            if (word.length() > 0) {
                result.append(Character.toUpperCase(word.charAt(0)))
                      .append(word.substring(1).toLowerCase())
                      .append(" ");
            }
        }
        return result.toString().trim();
    }
    
    // 날짜 관련 메서드들
    public static String formatDate(Date date, String pattern) {
        SimpleDateFormat formatter = new SimpleDateFormat(pattern);
        return formatter.format(date);
    }
    
    public static boolean isWeekend(Date date) {
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        int dayOfWeek = cal.get(Calendar.DAY_OF_WEEK);
        return dayOfWeek == Calendar.SATURDAY || dayOfWeek == Calendar.SUNDAY;
    }
    
    public static int daysBetween(Date start, Date end) {
        long diffInMillies = Math.abs(end.getTime() - start.getTime());
        return (int) (diffInMillies / (1000 * 60 * 60 * 24));
    }
    
    // 수학 계산 메서드들
    public static double calculateDistance(double x1, double y1, double x2, double y2) {
        return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
    }
    
    public static boolean isPrime(int number) {
        if (number <= 1) return false;
        for (int i = 2; i <= Math.sqrt(number); i++) {
            if (number % i == 0) return false;
        }
        return true;
    }
    
    public static int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    
    // 파일 관련 메서드들
    public static boolean fileExists(String filePath) {
        return new File(filePath).exists();
    }
    
    public static String readFileContent(String filePath) throws IOException {
        return new String(Files.readAllBytes(Paths.get(filePath)));
    }
    
    public static void writeToFile(String filePath, String content) throws IOException {
        Files.write(Paths.get(filePath), content.getBytes());
    }
    
    // 네트워크 관련 메서드들
    public static boolean isValidIP(String ip) {
        String[] parts = ip.split("\\.");
        if (parts.length != 4) return false;
        
        for (String part : parts) {
            try {
                int num = Integer.parseInt(part);
                if (num < 0 || num > 255) return false;
            } catch (NumberFormatException e) {
                return false;
            }
        }
        return true;
    }
    
    public static String getHostName() {
        try {
            return InetAddress.getLocalHost().getHostName();
        } catch (UnknownHostException e) {
            return "Unknown";
        }
    }
}
```

### 개선 과제

응집도가 높은 클래스들로 분리하세요:

1. **StringUtils** - 문자열 처리
2. **DateUtils** - 날짜 처리  
3. **MathUtils** - 수학 계산
4. **FileUtils** - 파일 처리
5. **NetworkUtils** - 네트워크 관련

## 실습 3: 데이터 전송 객체(DTO) 설계 (30분)

### 목표
복잡한 데이터 구조를 가진 객체를 깔끔한 DTO로 설계하여 데이터 전송과 캡슐화를 개선합니다.

### 개선 대상 코드

```java
// Bad: 복잡하고 불안전한 데이터 객체
public class CustomerData {
    public String customerName;
    public String customerEmail;
    public String customerPhone;
    public String customerAddress;
    public Date customerBirthDate;
    public String customerStatus;
    public double customerBalance;
    public List<String> customerOrders;
    public Map<String, Object> customerPreferences;
    public String lastLoginTime;
    public boolean isVipCustomer;
    public String customerNotes;
    
    // 복잡한 생성자
    public CustomerData(String name, String email, String phone, String address,
                       Date birthDate, String status, double balance,
                       List<String> orders, Map<String, Object> preferences,
                       String lastLogin, boolean isVip, String notes) {
        this.customerName = name;
        this.customerEmail = email;
        this.customerPhone = phone;
        this.customerAddress = address;
        this.customerBirthDate = birthDate;
        this.customerStatus = status;
        this.customerBalance = balance;
        this.customerOrders = orders;
        this.customerPreferences = preferences;
        this.lastLoginTime = lastLogin;
        this.isVipCustomer = isVip;
        this.customerNotes = notes;
    }
    
    // 데이터 접근이 불안전함
    public void addOrder(String orderId) {
        if (customerOrders == null) {
            customerOrders = new ArrayList<>();
        }
        customerOrders.add(orderId);
    }
    
    public void updatePreference(String key, Object value) {
        if (customerPreferences == null) {
            customerPreferences = new HashMap<>();
        }
        customerPreferences.put(key, value);
    }
}
```

### 개선 과제

안전하고 깔끔한 DTO를 설계하세요:

1. **불변 객체 설계**
2. **Builder 패턴 적용**
3. **적절한 캡슐화**
4. **유효성 검증 포함**

## 평가 기준

### 실습 1: 단일 책임 원칙 적용 (50점)
- 책임 분리의 적절성 (20점)
- 클래스 간 결합도 관리 (15점)
- 인터페이스 설계 품질 (15점)

### 실습 2: 응집도 향상 (30점)
- 관련 기능의 적절한 그룹핑 (15점)
- 유틸리티 클래스 설계 (15점)

### 실습 3: DTO 설계 (20점)
- 불변 객체 구현 (10점)
- Builder 패턴 적용 (10점)

## 제출 형식
- 파일명: `10_clean-classes-solid-principles_실습_[이름].md`
- 제출 기한: 다음 강의 시작 전
- 포함 내용:
  - 리팩토링된 코드
  - 클래스 다이어그램
  - 설계 결정 사항 설명

## 추가 자료
- [SOLID 원칙 가이드](https://en.wikipedia.org/wiki/SOLID)
- [Effective Java - 클래스와 인터페이스](https://www.oracle.com/java/technologies/javase/javadoc.html)
- [GoF 디자인 패턴](https://refactoring.guru/design-patterns) 