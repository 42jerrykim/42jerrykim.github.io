---
draft: true
---
# Chapter 3: 함수 작성법 - 실습 과제

## 실습 개요
이 실습은 작고 명확한 함수를 작성하고, 함수의 추상화 수준을 적절히 관리하며, Clean Code 함수 원칙을 실제 코드에 적용하는 것을 목표로 합니다.

## 실습 1: 함수 분해 (45분)

### 목표
제공된 긴 함수를 작은 함수들로 분해하여 가독성과 유지보수성을 향상시킵니다.

### 분해 대상 코드

#### Java 예시 - 주문 처리 시스템
```java
// Bad: 긴 함수 - 주문 처리
public class OrderProcessor {
    public String processOrder(String orderData) {
        // 주문 데이터 파싱
        String[] parts = orderData.split(",");
        String customerId = parts[0];
        String productId = parts[1];
        int quantity = Integer.parseInt(parts[2]);
        String discountCode = parts.length > 3 ? parts[3] : null;
        
        // 고객 정보 검증
        if (customerId == null || customerId.trim().isEmpty()) {
            return "Error: Invalid customer ID";
        }
        
        // 재고 확인
        int availableStock = getStock(productId);
        if (availableStock < quantity) {
            return "Error: Insufficient stock. Available: " + availableStock + ", Requested: " + quantity;
        }
        
        // 가격 계산
        double unitPrice = getProductPrice(productId);
        double totalPrice = unitPrice * quantity;
        
        // 할인 적용
        if (discountCode != null && !discountCode.trim().isEmpty()) {
            if (isValidDiscountCode(discountCode)) {
                double discountRate = getDiscountRate(discountCode);
                if (discountCode.startsWith("PERCENT")) {
                    totalPrice = totalPrice * (1 - discountRate);
                } else if (discountCode.startsWith("FIXED")) {
                    totalPrice = Math.max(0, totalPrice - discountRate);
                }
            } else {
                return "Error: Invalid discount code";
            }
        }
        
        // 세금 계산
        double taxRate = 0.1; // 10%
        double taxAmount = totalPrice * taxRate;
        double finalPrice = totalPrice + taxAmount;
        
        // 재고 차감
        updateStock(productId, quantity);
        
        // 주문 저장
        String orderId = generateOrderId();
        saveOrder(orderId, customerId, productId, quantity, finalPrice);
        
        // 이메일 발송
        String customerEmail = getCustomerEmail(customerId);
        if (customerEmail != null) {
            sendOrderConfirmationEmail(customerEmail, orderId, finalPrice);
        }
        
        // 결과 반환
        return "Order processed successfully. Order ID: " + orderId + ", Total: $" + String.format("%.2f", finalPrice);
    }
    
    // Helper methods (구현 생략)
    private int getStock(String productId) { return 100; }
    private double getProductPrice(String productId) { return 29.99; }
    private boolean isValidDiscountCode(String code) { return true; }
    private double getDiscountRate(String code) { return 0.1; }
    private void updateStock(String productId, int quantity) {}
    private String generateOrderId() { return "ORD-" + System.currentTimeMillis(); }
    private void saveOrder(String orderId, String customerId, String productId, int quantity, double price) {}
    private String getCustomerEmail(String customerId) { return "customer@example.com"; }
    private void sendOrderConfirmationEmail(String email, String orderId, double price) {}
}
```

#### Python 예시 - 학생 성적 분석
```python
# Bad: 긴 함수 - 학생 성적 분석
def analyze_student_performance(students_data, subject_weights):
    results = []
    
    for student_record in students_data:
        # 학생 정보 추출
        student_id = student_record['id']
        student_name = student_record['name']
        scores = student_record['scores']
        
        # 점수 검증
        valid_scores = []
        for score in scores:
            if isinstance(score, (int, float)) and 0 <= score <= 100:
                valid_scores.append(score)
            else:
                print(f"Warning: Invalid score {score} for student {student_name}")
        
        if len(valid_scores) == 0:
            results.append({
                'student_id': student_id,
                'name': student_name,
                'status': 'No valid scores',
                'grade': 'F'
            })
            continue
        
        # 가중 평균 계산
        if len(subject_weights) != len(valid_scores):
            # 가중치가 없으면 단순 평균
            weighted_average = sum(valid_scores) / len(valid_scores)
        else:
            # 가중 평균 계산
            total_weighted_score = 0
            total_weight = 0
            for i, score in enumerate(valid_scores):
                weight = subject_weights[i] if i < len(subject_weights) else 1
                total_weighted_score += score * weight
                total_weight += weight
            weighted_average = total_weighted_score / total_weight if total_weight > 0 else 0
        
        # 등급 계산
        if weighted_average >= 90:
            grade = 'A'
        elif weighted_average >= 80:
            grade = 'B'
        elif weighted_average >= 70:
            grade = 'C'
        elif weighted_average >= 60:
            grade = 'D'
        else:
            grade = 'F'
        
        # 상태 결정
        if grade in ['A', 'B']:
            status = 'Excellent'
        elif grade == 'C':
            status = 'Good'
        elif grade == 'D':
            status = 'Needs Improvement'
        else:
            status = 'Failing'
        
        # 개선 권장사항
        recommendations = []
        if weighted_average < 70:
            recommendations.append("Consider additional tutoring")
        if min(valid_scores) < 60:
            recommendations.append("Focus on weak subjects")
        if max(valid_scores) - min(valid_scores) > 30:
            recommendations.append("Work on consistency across subjects")
        
        results.append({
            'student_id': student_id,
            'name': student_name,
            'average': round(weighted_average, 2),
            'grade': grade,
            'status': status,
            'recommendations': recommendations
        })
    
    return results
```

### 분해 과제

다음 원칙을 적용하여 함수를 분해하세요:

1. **함수는 작게 (20줄 이내)**
2. **한 가지 일만 하기**
3. **같은 추상화 수준 유지**
4. **서술적인 이름 사용**

### 분해 템플릿

#### Java 리팩토링 결과
```java
// Good: 분해된 함수들
public class OrderProcessor {
    
    public String processOrder(String orderData) {
        try {
            OrderRequest request = parseOrderData(orderData);
            validateOrder(request);
            
            OrderCalculation calculation = calculateOrderTotal(request);
            Order order = createOrder(request, calculation);
            
            processOrderFulfillment(order);
            notifyCustomer(order);
            
            return formatSuccessResponse(order);
        } catch (OrderProcessingException e) {
            return "Error: " + e.getMessage();
        }
    }
    
    private OrderRequest parseOrderData(String orderData) {
        String[] parts = orderData.split(",");
        if (parts.length < 3) {
            throw new OrderProcessingException("Invalid order data format");
        }
        
        return new OrderRequest(
            parts[0].trim(),  // customerId
            parts[1].trim(),  // productId
            Integer.parseInt(parts[2]),  // quantity
            parts.length > 3 ? parts[3].trim() : null  // discountCode
        );
    }
    
    private void validateOrder(OrderRequest request) {
        validateCustomer(request.getCustomerId());
        validateStock(request.getProductId(), request.getQuantity());
        validateDiscountCode(request.getDiscountCode());
    }
    
    private void validateCustomer(String customerId) {
        if (customerId == null || customerId.isEmpty()) {
            throw new OrderProcessingException("Invalid customer ID");
        }
    }
    
    private void validateStock(String productId, int quantity) {
        int availableStock = getStock(productId);
        if (availableStock < quantity) {
            throw new OrderProcessingException(
                String.format("Insufficient stock. Available: %d, Requested: %d", 
                             availableStock, quantity)
            );
        }
    }
    
    private OrderCalculation calculateOrderTotal(OrderRequest request) {
        double baseAmount = calculateBaseAmount(request);
        double discountedAmount = applyDiscount(baseAmount, request.getDiscountCode());
        double finalAmount = addTax(discountedAmount);
        
        return new OrderCalculation(baseAmount, discountedAmount, finalAmount);
    }
    
    private double calculateBaseAmount(OrderRequest request) {
        double unitPrice = getProductPrice(request.getProductId());
        return unitPrice * request.getQuantity();
    }
    
    private double applyDiscount(double amount, String discountCode) {
        if (discountCode == null || discountCode.isEmpty()) {
            return amount;
        }
        
        double discountRate = getDiscountRate(discountCode);
        if (discountCode.startsWith("PERCENT")) {
            return amount * (1 - discountRate);
        } else if (discountCode.startsWith("FIXED")) {
            return Math.max(0, amount - discountRate);
        }
        
        return amount;
    }
    
    private Order createOrder(OrderRequest request, OrderCalculation calculation) {
        String orderId = generateOrderId();
        Order order = new Order(orderId, request, calculation);
        saveOrder(order);
        return order;
    }
}
```

### 함수 분해 체크리스트
```markdown
## 함수 분해 체크리스트

### 원래 함수 분석
- [ ] 함수 길이: ___줄 (목표: 20줄 이내)
- [ ] 수행하는 작업 수: ___개 (목표: 1개)
- [ ] 추상화 수준: 혼재됨/일관됨
- [ ] 들여쓰기 깊이: ___단계 (목표: 2단계 이내)

### 분해 후 개선사항
| 새 함수명 | 수행 작업 | 줄 수 | 추상화 수준 |
|-----------|-----------|-------|-------------|
| parseOrderData() | 데이터 파싱 | 8줄 | 낮음 |
| validateOrder() | 유효성 검사 | 5줄 | 중간 |
| calculateOrderTotal() | 가격 계산 | 7줄 | 중간 |
| createOrder() | 주문 생성 | 6줄 | 높음 |

### 개선 효과
- [ ] 가독성 향상
- [ ] 테스트 용이성 증가
- [ ] 재사용성 개선
- [ ] 유지보수성 향상
```

## 실습 2: 추상화 수준 정리 (30분)

### 목표
혼재된 추상화 수준을 가진 함수를 일관된 수준으로 개선합니다.

### 대상 코드

```java
// Bad: 혼재된 추상화 수준
public class ReportGenerator {
    public void generateUserReport(List<User> users) {
        // 높은 수준의 추상화
        System.out.println("=== User Report ===");
        
        // 낮은 수준의 추상화 (구체적인 구현)
        for (int i = 0; i < users.size(); i++) {
            User user = users.get(i);
            
            // 중간 수준의 추상화
            String userInfo = formatUserInfo(user);
            
            // 낮은 수준의 추상화 (직접적인 출력)
            System.out.print("User ID: " + user.getId());
            System.out.print(" | Name: " + user.getName());
            System.out.print(" | Email: " + user.getEmail());
            
            // 높은 수준의 추상화
            calculateUserMetrics(user);
            
            // 낮은 수준의 추상화
            if (user.getLastLoginDate() != null) {
                long daysSinceLogin = ChronoUnit.DAYS.between(
                    user.getLastLoginDate().toInstant(),
                    Instant.now()
                );
                System.out.print(" | Days since login: " + daysSinceLogin);
            }
            
            System.out.println();
        }
        
        // 높은 수준의 추상화
        printReportSummary(users);
    }
    
    private String formatUserInfo(User user) {
        return user.getName() + " (" + user.getEmail() + ")";
    }
    
    private void calculateUserMetrics(User user) {
        // 복잡한 메트릭 계산...
    }
    
    private void printReportSummary(List<User> users) {
        System.out.println("Total users: " + users.size());
    }
}
```

### 개선 과제

추상화 수준을 다음과 같이 구분하여 개선하세요:

- **높은 수준**: 비즈니스 로직, 전체 흐름
- **중간 수준**: 도메인 개념 조작
- **낮은 수준**: 구체적인 구현, 상세 로직

### 개선 템플릿

```java
// Good: 일관된 추상화 수준
public class ReportGenerator {
    
    // 높은 수준: 전체 보고서 생성 흐름
    public void generateUserReport(List<User> users) {
        printReportHeader();
        printUserDetails(users);
        printReportSummary(users);
    }
    
    // 중간 수준: 사용자 세부 정보 출력
    private void printUserDetails(List<User> users) {
        users.forEach(this::printSingleUserInfo);
    }
    
    // 중간 수준: 개별 사용자 정보 출력
    private void printSingleUserInfo(User user) {
        String basicInfo = formatBasicUserInfo(user);
        String loginInfo = formatLoginInfo(user);
        String metrics = calculateAndFormatMetrics(user);
        
        System.out.println(basicInfo + loginInfo + metrics);
    }
    
    // 낮은 수준: 기본 사용자 정보 포맷팅
    private String formatBasicUserInfo(User user) {
        return String.format("User ID: %s | Name: %s | Email: %s", 
                           user.getId(), user.getName(), user.getEmail());
    }
    
    // 낮은 수준: 로그인 정보 포맷팅
    private String formatLoginInfo(User user) {
        if (user.getLastLoginDate() == null) {
            return " | Never logged in";
        }
        
        long daysSinceLogin = calculateDaysSinceLogin(user.getLastLoginDate());
        return " | Days since login: " + daysSinceLogin;
    }
    
    // 낮은 수준: 로그인 후 경과 일수 계산
    private long calculateDaysSinceLogin(LocalDateTime lastLoginDate) {
        return ChronoUnit.DAYS.between(
            lastLoginDate.toInstant(),
            Instant.now()
        );
    }
}
```

### 추상화 수준 체크리스트
```markdown
## 추상화 수준 분석

### 함수별 추상화 수준
| 함수명 | 추상화 수준 | 담당 역할 |
|--------|-------------|-----------|
| generateUserReport() | 높음 | 전체 흐름 제어 |
| printUserDetails() | 중간 | 사용자 목록 처리 |
| printSingleUserInfo() | 중간 | 개별 사용자 처리 |
| formatBasicUserInfo() | 낮음 | 구체적 포맷팅 |
| calculateDaysSinceLogin() | 낮음 | 세부 계산 |

### 개선 효과
- [ ] 코드 이해도 향상
- [ ] 내려가기 규칙 준수
- [ ] 각 함수의 역할 명확화
- [ ] 수정 시 영향 범위 최소화
```

## 실습 3: 함수 네이밍 개선 (25분)

### 목표
의미있는 함수 이름으로 리팩토링하여 코드의 의도를 명확히 표현합니다.

### 네이밍 개선 대상

```java
// Bad: 모호한 함수 이름들
public class UserManager {
    
    public boolean check(String email) {
        return email.contains("@") && email.contains(".");
    }
    
    public void process(User user) {
        if (user.getAge() >= 18) {
            user.setStatus("ADULT");
        } else {
            user.setStatus("MINOR");
        }
        save(user);
    }
    
    public List<User> get(String criteria) {
        // 복잡한 쿼리 로직
        return queryUsers(criteria);
    }
    
    public void handle(User user, String action) {
        switch (action) {
            case "activate":
                user.setActive(true);
                break;
            case "deactivate":
                user.setActive(false);
                break;
            case "delete":
                user.setDeleted(true);
                break;
        }
    }
    
    public String format(User user) {
        return user.getName() + " (" + user.getEmail() + ")";
    }
    
    public boolean validate(Object data) {
        return data != null && !data.toString().isEmpty();
    }
}
```

### 네이밍 개선 과제

다음 원칙을 적용하여 함수 이름을 개선하세요:

1. **동사로 시작**
2. **구체적인 동작 표현**
3. **부울 반환 시 is/has/can 사용**
4. **매개변수 타입을 고려한 네이밍**

### 네이밍 개선 템플릿

```java
// Good: 명확한 함수 이름들
public class UserManager {
    
    public boolean isValidEmailFormat(String email) {
        return email.contains("@") && email.contains(".");
    }
    
    public void updateUserStatusByAge(User user) {
        if (user.getAge() >= 18) {
            user.setStatus("ADULT");
        } else {
            user.setStatus("MINOR");
        }
        saveUser(user);
    }
    
    public List<User> findUsersByCriteria(String searchCriteria) {
        return queryUsers(searchCriteria);
    }
    
    public void updateUserActiveStatus(User user, String action) {
        switch (action) {
            case "activate":
                activateUser(user);
                break;
            case "deactivate":
                deactivateUser(user);
                break;
            case "delete":
                markUserAsDeleted(user);
                break;
        }
    }
    
    public String formatUserDisplayName(User user) {
        return user.getName() + " (" + user.getEmail() + ")";
    }
    
    public boolean hasValidData(Object data) {
        return data != null && !data.toString().isEmpty();
    }
    
    // 추가된 명확한 헬퍼 메서드들
    private void activateUser(User user) {
        user.setActive(true);
    }
    
    private void deactivateUser(User user) {
        user.setActive(false);
    }
    
    private void markUserAsDeleted(User user) {
        user.setDeleted(true);
    }
    
    private void saveUser(User user) {
        // 사용자 저장 로직
    }
}
```

### 네이밍 개선 체크리스트
```markdown
## 함수 네이밍 개선 결과

### Before & After 비교
| Before | After | 개선 이유 |
|--------|--------|-----------|
| check() | isValidEmailFormat() | 구체적인 검증 대상 명시 |
| process() | updateUserStatusByAge() | 처리 내용을 구체적으로 표현 |
| get() | findUsersByCriteria() | 조회 방식과 조건 명시 |
| handle() | updateUserActiveStatus() | 처리하는 속성 명확화 |
| format() | formatUserDisplayName() | 포맷팅 용도 구체화 |
| validate() | hasValidData() | 부울 반환에 적절한 접두어 |

### 적용된 네이밍 원칙
- [ ] 동사로 시작하는 메서드명
- [ ] 구체적인 동작 표현
- [ ] 부울 반환 메서드의 적절한 접두어
- [ ] 매개변수 타입을 고려한 명명
- [ ] 일관성 있는 네이밍 규칙
```

## 실습 4: 종합 리팩토링 (30분)

### 목표
모든 함수 작성 원칙을 종합적으로 적용하여 복잡한 클래스를 개선합니다.

### 리팩토링 대상 코드

```java
// Bad: 모든 문제가 집약된 클래스
public class DataProcessor {
    
    public String process(String input, int type, boolean flag) {
        String result = "";
        
        if (type == 1) {
            String[] parts = input.split(",");
            for (int i = 0; i < parts.length; i++) {
                if (parts[i] != null && !parts[i].trim().isEmpty()) {
                    if (flag) {
                        parts[i] = parts[i].toUpperCase();
                    } else {
                        parts[i] = parts[i].toLowerCase();
                    }
                    if (i > 0) result += ",";
                    result += parts[i].trim();
                }
            }
        } else if (type == 2) {
            String[] lines = input.split("\n");
            for (String line : lines) {
                if (line.trim().length() > 0) {
                    String[] words = line.split(" ");
                    for (int j = 0; j < words.length; j++) {
                        if (words[j].length() > 0) {
                            if (flag) {
                                words[j] = words[j].substring(0, 1).toUpperCase() + 
                                          words[j].substring(1).toLowerCase();
                            }
                            result += words[j];
                            if (j < words.length - 1) result += " ";
                        }
                    }
                    result += "\n";
                }
            }
        }
        
        return result.trim();
    }
}
```

### 종합 리팩토링 과제

모든 함수 작성 원칙을 적용하여 개선하세요:
1. 함수 분해
2. 추상화 수준 정리
3. 의미있는 네이밍
4. 매개변수 개수 최소화
5. 부수 효과 제거

### 리팩토링 결과 템플릿

```java
// Good: 개선된 데이터 처리 클래스
public enum ProcessingType {
    CSV_FORMAT(1),
    TEXT_FORMAT(2);
    
    private final int value;
    
    ProcessingType(int value) {
        this.value = value;
    }
    
    public static ProcessingType fromValue(int value) {
        for (ProcessingType type : values()) {
            if (type.value == value) {
                return type;
            }
        }
        throw new IllegalArgumentException("Invalid processing type: " + value);
    }
}

public class TextDataProcessor {
    
    public String processTextData(String input, ProcessingType type, boolean shouldUppercase) {
        switch (type) {
            case CSV_FORMAT:
                return processCsvData(input, shouldUppercase);
            case TEXT_FORMAT:
                return processTextLines(input, shouldUppercase);
            default:
                throw new IllegalArgumentException("Unsupported processing type: " + type);
        }
    }
    
    private String processCsvData(String csvInput, boolean shouldUppercase) {
        String[] parts = csvInput.split(",");
        List<String> processedParts = new ArrayList<>();
        
        for (String part : parts) {
            String cleanedPart = cleanCsvPart(part, shouldUppercase);
            if (!cleanedPart.isEmpty()) {
                processedParts.add(cleanedPart);
            }
        }
        
        return String.join(",", processedParts);
    }
    
    private String cleanCsvPart(String part, boolean shouldUppercase) {
        if (part == null || part.trim().isEmpty()) {
            return "";
        }
        
        String trimmedPart = part.trim();
        return shouldUppercase ? trimmedPart.toUpperCase() : trimmedPart.toLowerCase();
    }
    
    private String processTextLines(String textInput, boolean shouldCapitalize) {
        String[] lines = textInput.split("\n");
        List<String> processedLines = new ArrayList<>();
        
        for (String line : lines) {
            String processedLine = processTextLine(line, shouldCapitalize);
            if (!processedLine.isEmpty()) {
                processedLines.add(processedLine);
            }
        }
        
        return String.join("\n", processedLines).trim();
    }
    
    private String processTextLine(String line, boolean shouldCapitalize) {
        if (line.trim().isEmpty()) {
            return "";
        }
        
        String[] words = line.split(" ");
        List<String> processedWords = new ArrayList<>();
        
        for (String word : words) {
            String processedWord = processWord(word, shouldCapitalize);
            if (!processedWord.isEmpty()) {
                processedWords.add(processedWord);
            }
        }
        
        return String.join(" ", processedWords);
    }
    
    private String processWord(String word, boolean shouldCapitalize) {
        if (word.isEmpty()) {
            return "";
        }
        
        if (shouldCapitalize) {
            return capitalizeFirstLetter(word);
        }
        
        return word;
    }
    
    private String capitalizeFirstLetter(String word) {
        return word.substring(0, 1).toUpperCase() + word.substring(1).toLowerCase();
    }
}
```

## 평가 기준

### 실습 1: 함수 분해 (35점)
- 적절한 함수 크기 (10점)
- 단일 책임 원칙 적용 (15점)
- 분해 후 가독성 향상 (10점)

### 실습 2: 추상화 수준 정리 (25점)
- 일관된 추상화 수준 유지 (15점)
- 내려가기 규칙 준수 (10점)

### 실습 3: 함수 네이밍 (20점)
- 의도가 명확한 이름 (10점)
- 일관성 있는 네이밍 규칙 (10점)

### 실습 4: 종합 리팩토링 (20점)
- 모든 원칙의 종합적 적용 (15점)
- 전체적인 코드 품질 향상 (5점)

## 제출 형식
- 파일명: `03_clean-functions_실습_[이름].md`
- 제출 기한: 다음 강의 시작 전
- 포함 내용: 
  - 리팩토링된 코드
  - Before/After 비교 분석
  - 적용한 원칙 설명

## 추가 자료
- Martin Fowler의 "Refactoring" - Extract Method
- Robert C. Martin의 함수 작성 가이드
- 각 언어별 함수형 프로그래밍 패턴
- SOLID 원칙 중 SRP(단일 책임 원칙) 적용 사례 