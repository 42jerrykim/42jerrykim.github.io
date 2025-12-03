---
draft: true
---
# Chapter 4: 주석과 문서화 - 실습 과제

## 실습 개요
이 실습은 좋은 주석과 나쁜 주석을 구분하고, 주석 없이도 이해 가능한 코드를 작성하며, 효과적인 문서화 정책을 수립하는 것을 목표로 합니다.

## 실습 1: 주석 제거 및 코드 개선 (45분)

### 목표
나쁜 주석이 포함된 코드를 개선하여 주석 없이도 이해 가능하도록 수정합니다.

### 개선 대상 코드

#### Java 예시 - 쇼핑몰 주문 시스템
```java
// Bad: 나쁜 주석들로 가득한 코드
public class OrderService {
    
    // 생성자
    public OrderService() {
        // 아무것도 하지 않음
    }
    
    /**
     * 주문을 처리하는 메서드
     * @param o 주문 객체
     * @return 성공하면 true, 실패하면 false
     */
    public boolean processOrder(Order o) {
        // null 체크
        if (o == null) {
            return false; // null이면 false 반환
        }
        
        // 주문 상태가 PENDING인지 확인
        if (!o.getStatus().equals("PENDING")) {
            return false; // PENDING이 아니면 false 반환
        }
        
        // 재고 확인
        for (OrderItem item : o.getItems()) {
            // 각 아이템에 대해 재고 확인
            if (getStock(item.getProductId()) < item.getQuantity()) {
                return false; // 재고 부족시 false 반환
            }
        }
        
        // 총 금액 계산 - 복잡한 로직
        double total = 0;
        for (OrderItem item : o.getItems()) {
            // 단가 * 수량으로 계산
            double itemTotal = item.getPrice() * item.getQuantity();
            // 할인 적용 - 10개 이상이면 10% 할인
            if (item.getQuantity() >= 10) {
                itemTotal = itemTotal * 0.9; // 10% 할인 적용
            }
            total += itemTotal; // 총액에 추가
        }
        
        // 배송비 추가 - 50달러 미만이면 배송비 10달러
        if (total < 50.0) {
            total += 10.0; // 배송비 추가
        }
        
        o.setTotalAmount(total); // 총액 설정
        
        // 재고 차감
        for (OrderItem item : o.getItems()) {
            updateStock(item.getProductId(), item.getQuantity()); // 재고 업데이트
        }
        
        // 주문 상태를 CONFIRMED로 변경
        o.setStatus("CONFIRMED");
        
        // 데이터베이스에 저장
        saveOrder(o);
        
        // 이메일 발송
        sendConfirmationEmail(o.getCustomerEmail(), o.getId());
        
        return true; // 성공 반환
    }
    
    // 재고 조회 메서드 - 실제로는 데이터베이스에서 조회
    private int getStock(String productId) {
        // TODO: 데이터베이스 조회 구현 필요
        return 100; // 임시로 100 반환
    }
    
    // 재고 업데이트 메서드
    private void updateStock(String productId, int quantity) {
        // 재고 차감 로직
        // 실제로는 데이터베이스 업데이트
    }
    
    // 주문 저장
    private void saveOrder(Order order) {
        // 데이터베이스에 주문 저장
    }
    
    // 확인 이메일 발송
    private void sendConfirmationEmail(String email, String orderId) {
        // 이메일 발송 로직
    }
}
```

#### Python 예시 - 학생 성적 시스템
```python
# Bad: 나쁜 주석들로 가득한 Python 코드
class GradeCalculator:
    
    def __init__(self):
        # 생성자 - 아무것도 하지 않음
        pass
    
    def calc_grade(self, scores, weights=None):
        """
        성적을 계산하는 함수
        scores: 점수 리스트
        weights: 가중치 리스트 (옵션)
        return: 최종 성적
        """
        
        # 점수가 없으면 0 반환
        if not scores:
            return 0
        
        # 가중치가 없으면 단순 평균
        if weights is None:
            # 모든 점수를 더해서 개수로 나눔
            return sum(scores) / len(scores)
        
        # 가중치와 점수의 개수가 다르면 에러
        if len(scores) != len(weights):
            raise ValueError("점수와 가중치의 개수가 다름")
        
        # 가중 평균 계산
        total = 0  # 총점
        weight_sum = 0  # 가중치 합
        
        # 각 점수와 가중치를 곱해서 더함
        for i in range(len(scores)):
            total += scores[i] * weights[i]  # 점수 * 가중치
            weight_sum += weights[i]  # 가중치 합계
        
        # 가중치 합이 0이면 0 반환
        if weight_sum == 0:
            return 0
        
        return total / weight_sum  # 가중 평균 반환
    
    def get_letter_grade(self, numeric_grade):
        """
        숫자 성적을 문자 성적으로 변환
        """
        # A: 90 이상
        if numeric_grade >= 90:
            return 'A'
        # B: 80 이상 90 미만
        elif numeric_grade >= 80:
            return 'B'
        # C: 70 이상 80 미만
        elif numeric_grade >= 70:
            return 'C'
        # D: 60 이상 70 미만
        elif numeric_grade >= 60:
            return 'D'
        # F: 60 미만
        else:
            return 'F'
```

### 개선 과제

다음 단계를 따라 코드를 개선하세요:

1. **불필요한 주석 제거**: 코드와 동일한 내용 반복하는 주석
2. **변수/메서드명 개선**: 주석 대신 의미 있는 이름 사용
3. **매직넘버 상수화**: 의미 있는 상수명으로 대체
4. **복잡한 로직 분해**: 주석이 필요한 복잡한 부분을 별도 메서드로 분리

### 개선 결과 템플릿

#### Java 개선 결과
```java
// Good: 주석 없이도 이해 가능한 깔끔한 코드
public class OrderService {
    private static final double BULK_DISCOUNT_RATE = 0.1;
    private static final int BULK_DISCOUNT_THRESHOLD = 10;
    private static final double SHIPPING_FEE = 10.0;
    private static final double FREE_SHIPPING_THRESHOLD = 50.0;
    
    public boolean processOrder(Order order) {
        if (!isValidOrderForProcessing(order)) {
            return false;
        }
        
        if (!hasEnoughStockForAllItems(order)) {
            return false;
        }
        
        calculateAndSetOrderTotal(order);
        reduceStockForOrderItems(order);
        confirmOrder(order);
        saveOrder(order);
        sendConfirmationEmail(order.getCustomerEmail(), order.getId());
        
        return true;
    }
    
    private boolean isValidOrderForProcessing(Order order) {
        return order != null && "PENDING".equals(order.getStatus());
    }
    
    private boolean hasEnoughStockForAllItems(Order order) {
        return order.getItems().stream()
                   .allMatch(this::hasEnoughStock);
    }
    
    private boolean hasEnoughStock(OrderItem item) {
        return getAvailableStock(item.getProductId()) >= item.getQuantity();
    }
    
    private void calculateAndSetOrderTotal(Order order) {
        double itemsTotal = calculateItemsTotal(order.getItems());
        double shippingFee = calculateShippingFee(itemsTotal);
        order.setTotalAmount(itemsTotal + shippingFee);
    }
    
    private double calculateItemsTotal(List<OrderItem> items) {
        return items.stream()
                   .mapToDouble(this::calculateItemTotalWithDiscount)
                   .sum();
    }
    
    private double calculateItemTotalWithDiscount(OrderItem item) {
        double baseTotal = item.getPrice() * item.getQuantity();
        return applyBulkDiscountIfEligible(baseTotal, item.getQuantity());
    }
    
    private double applyBulkDiscountIfEligible(double total, int quantity) {
        if (quantity >= BULK_DISCOUNT_THRESHOLD) {
            return total * (1 - BULK_DISCOUNT_RATE);
        }
        return total;
    }
    
    private double calculateShippingFee(double itemsTotal) {
        return itemsTotal < FREE_SHIPPING_THRESHOLD ? SHIPPING_FEE : 0.0;
    }
    
    private void reduceStockForOrderItems(Order order) {
        order.getItems().forEach(this::reduceStockForItem);
    }
    
    private void reduceStockForItem(OrderItem item) {
        reduceStock(item.getProductId(), item.getQuantity());
    }
    
    private void confirmOrder(Order order) {
        order.setStatus("CONFIRMED");
    }
}
```

### 주석 제거 체크리스트
```markdown
## 주석 개선 체크리스트

### 제거된 나쁜 주석들
- [ ] 코드와 동일한 내용 반복하는 주석
- [ ] 당연한 내용을 설명하는 주석  
- [ ] 오래된/잘못된 정보를 담은 주석
- [ ] 닫는 괄호 주석
- [ ] 저작권/법적 정보가 아닌 주석

### 개선 방법
| 기존 주석 | 개선 방법 | 결과 |
|-----------|-----------|------|
| `// null 체크` | 메서드명으로 의도 표현 | `isValidOrderForProcessing()` |
| `// 10% 할인 적용` | 상수와 메서드명으로 표현 | `BULK_DISCOUNT_RATE`, `applyBulkDiscountIfEligible()` |
| `// 배송비 추가` | 메서드명으로 의도 표현 | `calculateShippingFee()` |

### 보존된 좋은 주석 (있다면)
- [ ] 비즈니스 규칙 설명
- [ ] 알고리즘의 의도 설명  
- [ ] 주의사항이나 경고
- [ ] 공개 API 문서화
```

## 실습 2: 주석 분류 및 평가 (30분)

### 목표
제공된 코드의 주석들을 좋은 주석과 나쁜 주석으로 분류하고 이유를 설명합니다.

### 분류 대상 코드

```java
public class PaymentProcessor {
    
    // WARNING: This method handles sensitive financial data
    // Always validate input parameters before processing
    public PaymentResult processPayment(PaymentRequest request) {
        
        // Validate request - can't be null
        if (request == null) {
            return PaymentResult.failure("Invalid request");
        }
        
        // Check amount - business rule: minimum $0.01, maximum $10,000
        if (request.getAmount() < 0.01 || request.getAmount() > 10000.00) {
            return PaymentResult.failure("Amount out of range");
        }
        
        /* 
         * Credit card validation using Luhn algorithm
         * This is required by PCI DSS compliance standards
         * Reference: https://en.wikipedia.org/wiki/Luhn_algorithm
         */
        if (!isValidCreditCard(request.getCardNumber())) {
            return PaymentResult.failure("Invalid card number");
        }
        
        // TODO: Implement proper encryption for card data
        String encryptedCard = encrypt(request.getCardNumber());
        
        // Process payment
        return executePayment(request);
    }
    
    /**
     * Validates credit card number using Luhn algorithm
     * 
     * The Luhn algorithm is a simple checksum formula used to validate
     * various identification numbers including credit card numbers.
     * 
     * @param cardNumber the credit card number to validate
     * @return true if the card number is valid, false otherwise
     */
    private boolean isValidCreditCard(String cardNumber) {
        // Remove spaces and dashes
        cardNumber = cardNumber.replaceAll("[\\s-]", "");
        
        int sum = 0;
        boolean alternate = false;
        
        // Process digits from right to left
        for (int i = cardNumber.length() - 1; i >= 0; i--) {
            int digit = Character.getNumericValue(cardNumber.charAt(i));
            
            if (alternate) {
                digit *= 2;
                if (digit > 9) {
                    digit = digit % 10 + 1;
                }
            }
            
            sum += digit;
            alternate = !alternate;
        }
        
        return (sum % 10 == 0);
    }
    
    // Method to encrypt sensitive data
    private String encrypt(String data) {
        // This is a placeholder implementation
        // In production, use proper encryption library
        return "ENCRYPTED_" + data.hashCode();
    }
    
    /*
     * This method was added on 2023-12-15 by John Smith
     * Modified on 2024-01-10 by Sarah Johnson - fixed bug #1234
     * TODO: Refactor this method to use new payment gateway API
     */
    private PaymentResult executePayment(PaymentRequest request) {
        // Simulate payment processing
        return PaymentResult.success("Payment processed successfully");
    }
}
```

### 분류 과제

각 주석을 다음 카테고리로 분류하고 이유를 설명하세요:

1. **좋은 주석** - 유지할 가치가 있는 주석
2. **나쁜 주석** - 제거하거나 개선해야 하는 주석
3. **애매한 주석** - 상황에 따라 판단이 필요한 주석

### 분류 템플릿

```markdown
## 주석 분류 및 평가

### 좋은 주석 (유지 권장)
| 라인 | 주석 내용 | 분류 이유 | 개선 제안 |
|------|-----------|-----------|-----------|
| 4-5 | WARNING 및 보안 주의사항 | 중요한 보안 경고, 개발자 안전 | 없음 |
| 13-17 | Luhn 알고리즘 설명 및 참조 | 복잡한 알고리즘 의도 설명, 외부 참조 | 없음 |
| 25-32 | Luhn 알고리즘 JavaDoc | 공개 API 문서화, 매개변수/반환값 설명 | 없음 |

### 나쁜 주석 (제거 권장)
| 라인 | 주석 내용 | 문제점 | 개선 방법 |
|------|-----------|--------|-----------|
| 8 | `// Validate request - can't be null` | 코드와 동일한 내용 반복 | 메서드명으로 의도 표현 |
| 25 | `// Process payment` | 당연한 내용 설명 | 제거 |
| 55-58 | 변경 이력 주석 | 버전 관리 시스템으로 대체 가능 | 제거, Git 사용 |
| 63 | `// Simulate payment processing` | 임시 코드 설명 | 메서드명 개선으로 대체 |

### 애매한 주석 (상황별 판단)
| 라인 | 주석 내용 | 고려사항 | 권장사항 |
|------|-----------|-----------|-----------|
| 11-12 | 비즈니스 규칙 설명 | 도메인 지식 필요 여부 | 상수로 추출 후 제거 고려 |
| 20 | TODO 주석 | 구현 예정 여부 | 이슈 트래커로 이관 후 제거 |
| 50-52 | 임시 구현 설명 | 코드 리뷰 맥락 | 프로덕션에서는 제거 |

### 개선 제안
1. **상수 추출**: 매직넘버들을 의미 있는 상수로 추출
2. **메서드 분해**: 복잡한 검증 로직을 별도 메서드로 분리
3. **메서드명 개선**: 주석 없이도 의도가 명확한 메서드명 사용
```

## 실습 3: 문서화 정책 수립 (35분)

### 목표
팀 프로젝트용 주석 작성 가이드라인과 문서화 정책을 수립합니다.

### 정책 수립 과제

다음 영역에 대한 구체적인 가이드라인을 작성하세요:

1. **주석 작성 원칙**
2. **JavaDoc/Docstring 작성 규칙**
3. **코드 내 문서화 vs 외부 문서화**
4. **리뷰 기준**

### 문서화 정책 템플릿

```markdown
# 팀 프로젝트 주석 및 문서화 정책

## 기본 원칙

### 주석 작성 철학
- **코드 우선**: 주석보다는 명확한 코드 작성을 우선시
- **필요충분**: 꼭 필요한 정보만 포함
- **정확성 유지**: 코드 변경 시 주석도 함께 업데이트
- **읽는 사람 관점**: 코드를 처음 보는 개발자를 고려

### 작성해야 하는 주석
- [ ] 복잡한 비즈니스 로직의 의도
- [ ] 알고리즘의 선택 이유
- [ ] 보안상 중요한 주의사항
- [ ] 외부 시스템과의 연동 규칙
- [ ] 성능상 고려사항

### 작성하지 말아야 하는 주석
- [ ] 코드와 동일한 내용 반복
- [ ] 당연한 내용 설명
- [ ] 변경 이력 (Git으로 관리)
- [ ] 개발자 개인 정보
- [ ] 오래된/잘못된 정보

## 언어별 문서화 규칙

### Java - JavaDoc
```java
/**
 * 결제를 처리하는 서비스 클래스
 * 
 * PCI DSS 준수를 위해 카드 정보는 항상 암호화하여 처리하며,
 * 모든 결제 요청은 보안 검증을 거칩니다.
 * 
 * @author Payment Team
 * @since 1.0
 * @see PaymentGateway
 */
public class PaymentService {
    
    /**
     * 결제 요청을 처리합니다.
     * 
     * 카드 번호는 Luhn 알고리즘으로 검증하며, 금액은 최소 $0.01에서
     * 최대 $10,000까지 처리 가능합니다.
     * 
     * @param request 결제 요청 정보 (null 불가)
     * @return 결제 처리 결과
     * @throws IllegalArgumentException 요청 정보가 유효하지 않은 경우
     * @throws PaymentException 결제 처리 중 오류 발생 시
     */
    public PaymentResult processPayment(PaymentRequest request) {
        // 구현...
    }
}
```

### Python - Docstring
```python
class PaymentService:
    """결제 처리 서비스
    
    PCI DSS 준수를 위해 모든 카드 정보는 암호화하여 처리합니다.
    
    Attributes:
        gateway: 결제 게이트웨이 인스턴스
        encryption_service: 암호화 서비스
        
    Examples:
        >>> service = PaymentService()
        >>> result = service.process_payment(payment_request)
        >>> print(result.success)
        True
    """
    
    def process_payment(self, request: PaymentRequest) -> PaymentResult:
        """결제 요청을 처리합니다.
        
        Args:
            request: 결제 요청 정보
                - amount: 결제 금액 (0.01 ~ 10000.00)
                - card_number: 카드 번호 (Luhn 알고리즘 검증)
                - cvv: 보안 코드
                
        Returns:
            PaymentResult: 결제 처리 결과
                - success: 성공 여부
                - transaction_id: 거래 번호 (성공 시)
                - error_message: 오류 메시지 (실패 시)
                
        Raises:
            ValueError: 요청 정보가 유효하지 않은 경우
            PaymentError: 결제 처리 중 오류 발생 시
            
        Note:
            카드 정보는 메모리에 보관하지 않으며, 처리 후 즉시 삭제됩니다.
        """
        # 구현...
```

### JavaScript - JSDoc
```javascript
/**
 * 결제 처리 서비스
 * @class
 * @description PCI DSS 준수 결제 처리 서비스
 */
class PaymentService {
    /**
     * 결제 요청을 처리합니다.
     * 
     * @param {PaymentRequest} request - 결제 요청 정보
     * @param {number} request.amount - 결제 금액 (0.01-10000.00)
     * @param {string} request.cardNumber - 카드 번호
     * @param {string} request.cvv - 보안 코드
     * @returns {Promise<PaymentResult>} 결제 처리 결과
     * @throws {Error} 요청 정보가 유효하지 않은 경우
     * 
     * @example
     * const service = new PaymentService();
     * const result = await service.processPayment({
     *   amount: 99.99,
     *   cardNumber: '4111111111111111',
     *   cvv: '123'
     * });
     */
    async processPayment(request) {
        // 구현...
    }
}
```

## 문서화 수준 가이드

### Level 1: 공개 API (필수)
- 모든 public 클래스, 메서드에 상세한 문서화
- 매개변수, 반환값, 예외 상황 모두 기술
- 사용 예제 포함

### Level 2: 내부 구현 (선택적)
- 복잡한 알고리즘이나 비즈니스 로직
- 성능상 중요한 고려사항
- 외부 시스템 연동 부분

### Level 3: 헬퍼 메서드 (최소한)
- 메서드명만으로 이해 어려운 경우만
- 간단한 한 줄 설명

## 코드 리뷰 체크리스트

### 주석 품질 검토
- [ ] 코드 없이 주석만 읽어도 이해되는가?
- [ ] 주석이 코드와 일치하는가?
- [ ] 불필요한 주석은 없는가?
- [ ] 중요한 정보가 누락되지 않았는가?

### 문서화 완성도 검토
- [ ] 공개 API는 모두 문서화되었는가?
- [ ] 매개변수와 반환값이 명확히 설명되었는가?
- [ ] 예외 상황이 적절히 기술되었는가?
- [ ] 사용 예제가 포함되었는가?

## 도구 및 자동화

### 권장 도구
- **Java**: Checkstyle, SpotBugs
- **Python**: pydocstyle, sphinx
- **JavaScript**: ESLint, JSDoc

### CI/CD 통합
- 문서화 누락 시 빌드 실패
- 생성된 문서 자동 배포
- 주석 커버리지 측정

## 예외 상황

### 주석을 허용하는 경우
- 임시 해결책 (TODO, FIXME)
- 복잡한 정규식이나 알고리즘
- 성능 최적화를 위한 트릭
- 법적/보안상 요구사항

### 주석 대신 권장하는 방법
- 메서드 추출 (Extract Method)
- 변수 추출 (Extract Variable)
- 상수 추출 (Extract Constant)
- 의미 있는 네이밍
```

## 평가 기준

### 실습 1: 주석 제거 및 코드 개선 (40점)
- 불필요한 주석 식별 및 제거 (15점)
- 코드 가독성 향상 (15점)
- 메서드/변수명 개선 (10점)

### 실습 2: 주석 분류 및 평가 (30점)
- 좋은/나쁜 주석 구분 정확성 (20점)
- 분류 이유의 타당성 (10점)

### 실습 3: 문서화 정책 수립 (30점)
- 정책의 구체성과 실용성 (20점)
- 팀 적용 가능성 (10점)

## 제출 형식
- 파일명: `04_code-comments-documentation_실습_[이름].md`
- 제출 기한: 다음 강의 시작 전
- 포함 내용: 
  - 개선된 코드
  - 주석 분류 결과
  - 문서화 정책 문서

## 추가 자료
- [Oracle JavaDoc Guidelines](https://www.oracle.com/technical-resources/articles/java/javadoc-tool.html)
- [Google Style Guides](https://google.github.io/styleguide/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [JSDoc Getting Started](https://jsdoc.app/about-getting-started.html) 