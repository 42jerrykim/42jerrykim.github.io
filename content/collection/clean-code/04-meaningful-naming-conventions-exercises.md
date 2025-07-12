---
draft: true
---
# Chapter 2: 의미있는 네이밍 - 실습 과제

## 실습 개요
이 실습은 의미있는 네이밍 원칙을 실제 코드에 적용하고, 팀 차원의 네이밍 컨벤션을 수립하는 것을 목표로 합니다.

## 실습 1: 네이밍 리팩토링 (50분)

### 목표
제공된 나쁜 네이밍의 코드를 Clean Code 네이밍 원칙에 따라 개선합니다.

### 리팩토링 대상 코드

#### Java 예시
```java
// Bad Naming - 전자상거래 주문 처리 시스템
public class OrderProcessor {
    private List<Map<String, Object>> d;
    private int c = 0;
    private double t = 0.0;
    
    public void p(Map<String, Object> o) {
        String s = (String) o.get("status");
        if (s.equals("pending")) {
            double a = (Double) o.get("amount");
            int q = (Integer) o.get("quantity");
            String pid = (String) o.get("productId");
            
            if (check(pid, q)) {
                o.put("status", "confirmed");
                t += a;
                c++;
                log(o);
            }
        }
    }
    
    public boolean check(String id, int q) {
        // 재고 확인 로직
        return getStock(id) >= q;
    }
    
    public void log(Map<String, Object> o) {
        System.out.println("Order " + o.get("id") + " processed");
    }
    
    public List<Map<String, Object>> getD() {
        return d;
    }
    
    public int getC() {
        return c;
    }
    
    public double getT() {
        return t;
    }
    
    private int getStock(String productId) {
        // 실제 재고 조회 로직
        return 100;
    }
}
```

#### Python 예시
```python
# Bad Naming - 학생 관리 시스템
class StudentManager:
    def __init__(self):
        self.d = []
        self.c = 0
        
    def a(self, n, a, s):
        st = {
            'n': n,
            'a': a,
            's': s,
            'id': self.c
        }
        self.d.append(st)
        self.c += 1
        return st['id']
    
    def u(self, id, **kwargs):
        for i, st in enumerate(self.d):
            if st['id'] == id:
                for k, v in kwargs.items():
                    if k in ['n', 'a', 's']:
                        st[k] = v
                return True
        return False
    
    def g(self, id=None):
        if id is None:
            return self.d
        for st in self.d:
            if st['id'] == id:
                return st
        return None
    
    def calc_avg(self):
        if not self.d:
            return 0
        total = sum(st['s'] for st in self.d)
        return total / len(self.d)
```

#### JavaScript 예시
```javascript
// Bad Naming - 게임 점수 관리 시스템
class GameManager {
    constructor() {
        this.p = [];
        this.s = 0;
        this.t = 0;
        this.l = 1;
    }
    
    ap(n) {
        const newP = {
            n: n,
            s: 0,
            l: this.l,
            a: true
        };
        this.p.push(newP);
        return newP;
    }
    
    us(pId, pts) {
        const p = this.fp(pId);
        if (p && p.a) {
            p.s += pts;
            this.s += pts;
            this.cl();
        }
    }
    
    fp(id) {
        return this.p.find(p => p.n === id);
    }
    
    cl() {
        if (this.s >= this.l * 1000) {
            this.l++;
            this.s = 0;
            this.p.forEach(p => p.a = false);
        }
    }
    
    gls() {
        return this.p.sort((a, b) => b.s - a.s);
    }
}
```

### 리팩토링 과제

각 언어별로 다음 네이밍 원칙을 적용하여 코드를 개선하세요:

1. **의도를 분명히 밝히는 이름**
2. **그릇된 정보를 피하는 이름**
3. **의미있게 구분하는 이름**
4. **발음하기 쉬운 이름**
5. **검색하기 쉬운 이름**

### 리팩토링 템플릿

#### Java 리팩토링 결과
```java
// Good Naming - 개선된 주문 처리 시스템
public class OrderProcessor {
    private List<Order> processedOrders;
    private int confirmedOrderCount = 0;
    private double totalRevenue = 0.0;
    
    public void processOrder(Order order) {
        OrderStatus status = order.getStatus();
        if (status == OrderStatus.PENDING) {
            double orderAmount = order.getAmount();
            int requestedQuantity = order.getQuantity();
            String productId = order.getProductId();
            
            if (isStockSufficient(productId, requestedQuantity)) {
                order.setStatus(OrderStatus.CONFIRMED);
                totalRevenue += orderAmount;
                confirmedOrderCount++;
                logOrderProcessing(order);
            }
        }
    }
    
    public boolean isStockSufficient(String productId, int requestedQuantity) {
        return getAvailableStock(productId) >= requestedQuantity;
    }
    
    public void logOrderProcessing(Order order) {
        System.out.println("Order " + order.getId() + " has been processed");
    }
    
    // Getters
    public List<Order> getProcessedOrders() { return processedOrders; }
    public int getConfirmedOrderCount() { return confirmedOrderCount; }
    public double getTotalRevenue() { return totalRevenue; }
    
    private int getAvailableStock(String productId) {
        // 실제 재고 조회 로직
        return 100;
    }
}
```

### 네이밍 개선 체크리스트
```markdown
## 네이밍 개선 체크리스트

### Before & After 비교
| Before | After | 개선 이유 |
|--------|--------|-----------|
| d | processedOrders | 변수의 목적이 명확해짐 |
| c | confirmedOrderCount | 카운터의 대상이 구체적임 |
| p() | processOrder() | 메서드가 하는 일을 명확히 표현 |
| check() | isStockSufficient() | 부울 반환 메서드의 의도가 명확 |

### 적용된 네이밍 원칙
- [ ] 의도를 분명히 밝히는 이름
- [ ] 그릇된 정보를 피하는 이름
- [ ] 의미있게 구분하는 이름
- [ ] 발음하기 쉬운 이름
- [ ] 검색하기 쉬운 이름
- [ ] 클래스 이름은 명사 사용
- [ ] 메서드 이름은 동사 사용
```

## 실습 2: 네이밍 컨벤션 문서 작성 (30분)

### 목표
팀 프로젝트에서 사용할 포괄적인 네이밍 가이드라인을 작성합니다.

### 네이밍 컨벤션 템플릿

```markdown
# 팀 프로젝트 네이밍 컨벤션

## 1. 기본 원칙
- 의도를 명확히 표현하는 이름 사용
- 줄임말보다는 완전한 단어 사용
- 일관성 있는 네이밍 규칙 적용
- 도메인 용어 활용

## 2. 언어별 명명 규칙

### Java
#### 클래스 및 인터페이스
- **규칙**: PascalCase 사용
- **예시**: `UserService`, `OrderRepository`, `PaymentProcessor`
- **금지**: `userservice`, `User_Service`, `USERSERVICE`

#### 메서드 및 변수
- **규칙**: camelCase 사용
- **예시**: `getUserById()`, `calculateTotalAmount`, `isOrderValid`
- **금지**: `getuserbyid`, `get_user_by_id`, `GetUserById`

#### 상수
- **규칙**: SCREAMING_SNAKE_CASE 사용
- **예시**: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_SECONDS`
- **금지**: `maxRetryCount`, `Max_Retry_Count`

### Python
#### 클래스
- **규칙**: PascalCase 사용
- **예시**: `UserService`, `OrderManager`, `PaymentValidator`

#### 함수 및 변수
- **규칙**: snake_case 사용
- **예시**: `get_user_by_id()`, `calculate_total_amount`, `is_order_valid`

#### 상수
- **규칙**: SCREAMING_SNAKE_CASE 사용
- **예시**: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_SECONDS`

### JavaScript
#### 클래스
- **규칙**: PascalCase 사용
- **예시**: `UserService`, `OrderManager`, `PaymentProcessor`

#### 함수 및 변수
- **규칙**: camelCase 사용
- **예시**: `getUserById()`, `calculateTotalAmount`, `isOrderValid`

#### 상수
- **규칙**: SCREAMING_SNAKE_CASE 사용
- **예시**: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT_SECONDS`

## 3. 도메인별 네이밍 가이드

### 사용자 관리
- 사용자 생성: `createUser`, `registerUser`
- 사용자 조회: `getUserById`, `findUserByEmail`
- 사용자 수정: `updateUser`, `modifyUserProfile`
- 사용자 삭제: `deleteUser`, `removeUser`

### 주문 관리
- 주문 생성: `createOrder`, `placeOrder`
- 주문 조회: `getOrderById`, `findOrdersByUserId`
- 주문 상태 변경: `confirmOrder`, `cancelOrder`, `completeOrder`

### 결제 처리
- 결제 실행: `processPayment`, `executePayment`
- 결제 검증: `validatePayment`, `verifyPaymentData`
- 환불 처리: `refundPayment`, `processRefund`

## 4. 금지 사항
- [ ] 한 글자 변수명 (i, j, k 제외한 반복문 인덱스)
- [ ] 숫자로 시작하는 이름
- [ ] 예약어 사용
- [ ] 발음하기 어려운 줄임말
- [ ] 문화적으로 부적절한 이름

## 5. 부울 변수/메서드 네이밍
- **접두어 사용**: `is`, `has`, `can`, `should`, `will`
- **예시**: `isValid`, `hasPermission`, `canEdit`, `shouldRetry`
- **금지**: `valid`, `permission`, `edit` (부울임을 알 수 없음)

## 6. 컬렉션 네이밍
- **복수형 사용**: `users`, `orders`, `products`
- **의미 있는 접미사**: `userList`, `orderQueue`, `productSet`
- **금지**: `userData`, `orderInfo` (모호한 표현)
```

## 실습 3: 코드 리뷰 - 네이밍 개선점 찾기 (30분)

### 목표
동료의 코드에서 네이밍 관련 개선점을 찾아 건설적인 피드백을 제공합니다.

### 리뷰 대상 코드

```java
// 리뷰 대상: 도서관 관리 시스템
public class LibrarySystem {
    private Map<String, Object> books;
    private List<String> users;
    private Map<String, List<String>> borrows;
    
    public LibrarySystem() {
        this.books = new HashMap<>();
        this.users = new ArrayList<>();
        this.borrows = new HashMap<>();
    }
    
    public void addB(String isbn, String title, String author, boolean available) {
        Map<String, Object> book = new HashMap<>();
        book.put("title", title);
        book.put("author", author);
        book.put("available", available);
        books.put(isbn, book);
    }
    
    public boolean borrowBook(String userId, String isbn) {
        if (users.contains(userId) && books.containsKey(isbn)) {
            Map<String, Object> book = books.get(isbn);
            boolean avail = (Boolean) book.get("available");
            if (avail) {
                book.put("available", false);
                borrows.computeIfAbsent(userId, k -> new ArrayList<>()).add(isbn);
                return true;
            }
        }
        return false;
    }
    
    public List<String> getUserBorrowedBooks(String userId) {
        return borrows.getOrDefault(userId, new ArrayList<>());
    }
    
    public boolean returnB(String userId, String isbn) {
        List<String> userBooks = borrows.get(userId);
        if (userBooks != null && userBooks.contains(isbn)) {
            userBooks.remove(isbn);
            Map<String, Object> book = books.get(isbn);
            book.put("available", true);
            return true;
        }
        return false;
    }
}
```

### 코드 리뷰 템플릿

```markdown
# 코드 리뷰: 네이밍 개선 사항

## 1. 발견된 네이밍 문제점

### 심각도 HIGH (즉시 수정 필요)
| 라인 | 현재 이름 | 문제점 | 제안 개선명 |
|------|-----------|--------|-------------|
| 15 | `addB` | 메서드명이 무엇을 하는지 불명확 | `addBook` |
| 17 | `avail` | 줄임말로 의미가 모호함 | `isAvailable` |
| 35 | `returnB` | 메서드명이 불완전함 | `returnBook` |

### 심각도 MEDIUM (개선 권장)
| 라인 | 현재 이름 | 문제점 | 제안 개선명 |
|------|-----------|--------|-------------|
| 4 | `borrows` | 동사형으로 혼란스러움 | `userBorrowedBooks` |
| 36 | `userBooks` | 너무 일반적인 이름 | `borrowedBooksByUser` |

### 심각도 LOW (참고사항)
| 라인 | 현재 이름 | 문제점 | 제안 개선명 |
|------|-----------|--------|-------------|
| 3 | `books` | 적절하지만 더 명확할 수 있음 | `bookCatalog` |

## 2. 전체적인 네이밍 개선 방향

### 일관성 개선
- [ ] 메서드명에서 줄임말 제거 (`addB` → `addBook`)
- [ ] 부울 변수에 `is`, `has` 접두어 사용
- [ ] 컬렉션 변수명에 용도 명시

### 의도 명확화
- [ ] 변수명에서 데이터 타입보다는 용도 강조
- [ ] 메서드명에서 동작을 명확히 표현
- [ ] 매개변수명을 더 구체적으로 작성

## 3. 리팩토링된 코드 제안

```java
public class LibraryManagementSystem {
    private Map<String, Book> bookCatalog;
    private Set<String> registeredUsers;
    private Map<String, List<String>> userBorrowedBooks;
    
    public void addBookToCatalog(String isbn, String title, String author) {
        Book newBook = new Book(isbn, title, author, true);
        bookCatalog.put(isbn, newBook);
    }
    
    public boolean borrowBook(String userId, String bookIsbn) {
        if (isUserRegistered(userId) && isBookAvailable(bookIsbn)) {
            Book book = bookCatalog.get(bookIsbn);
            book.setAvailable(false);
            addBookToBorrowedList(userId, bookIsbn);
            return true;
        }
        return false;
    }
    
    private boolean isUserRegistered(String userId) {
        return registeredUsers.contains(userId);
    }
    
    private boolean isBookAvailable(String bookIsbn) {
        Book book = bookCatalog.get(bookIsbn);
        return book != null && book.isAvailable();
    }
}
```

## 4. 피드백 제공 방법
- 건설적이고 구체적인 제안
- 개선 이유 명확히 설명
- 우선순위 표시 (High/Medium/Low)
- 대안 제시
```

## 실습 4: 네이밍 퀴즈 (20분)

### 다음 중 좋은 네이밍을 선택하고 이유를 설명하세요

#### 문제 1: 사용자 나이 확인 메서드
```java
// A
public boolean checkAge(int age) { return age >= 18; }

// B  
public boolean isAdult(int age) { return age >= 18; }

// C
public boolean validateUserAge(int userAge) { return userAge >= 18; }
```

#### 문제 2: 주문 목록 변수
```java
// A
List<Order> orderList;

// B
List<Order> orders;

// C
List<Order> orderData;
```

#### 문제 3: 결제 처리 클래스
```java
// A
class PaymentProcessor

// B
class PaymentHandler

// C
class PaymentManager
```

## 평가 기준

### 실습 1: 네이밍 리팩토링 (40점)
- 원칙별 적용 정확성 (25점)
- 개선된 코드의 가독성 (10점)
- Before/After 비교 분석 (5점)

### 실습 2: 컨벤션 문서 (30점)
- 규칙의 구체성과 실용성 (20점)
- 예시의 적절성 (5점)
- 팀 적용 가능성 (5점)

### 실습 3: 코드 리뷰 (20점)
- 문제점 식별 정확성 (10점)
- 개선 제안의 품질 (10점)

### 실습 4: 퀴즈 (10점)
- 정답 선택과 논리적 근거 (10점)

## 제출 형식
- 파일명: `02_meaningful-naming-conventions_실습_[이름].md`
- 제출 기한: 다음 강의 시작 전
- 포함 내용: 리팩토링된 코드, 네이밍 컨벤션 문서, 코드 리뷰 결과

## 추가 자료
- [Google Java Style Guide - Naming](https://google.github.io/styleguide/javaguide.html#s5-naming)
- [PEP 8 - Naming Conventions](https://www.python.org/dev/peps/pep-0008/#naming-conventions)
- [MDN JavaScript Guide - Grammar and Types](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Grammar_and_Types)
- Clean Code Chapter 2 추가 예시 