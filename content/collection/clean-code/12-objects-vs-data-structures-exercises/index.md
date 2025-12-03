---
draft: true
---
# Chapter 6: 객체와 자료구조 - 실습 과제

## 실습 개요
이 실습은 객체와 자료구조의 차이를 이해하고, 적절한 데이터 추상화를 적용하며, 디미터 법칙을 준수하는 코드를 작성하는 것을 목표로 합니다.

## 실습 1: 구조 변환 (45분)

### 목표
제공된 절차적 코드를 객체지향으로 변환하거나, 과도한 객체지향 코드를 적절한 자료구조로 변환합니다.

### 변환 대상 코드 - 절차적 → 객체지향

#### Java 예시 - 기하학 도형 계산
```java
// Bad: 절차적 프로그래밍 스타일
public class GeometryCalculator {
    public static final int SQUARE = 1;
    public static final int RECTANGLE = 2;
    public static final int CIRCLE = 3;
    
    public static class Point {
        public double x, y;
    }
    
    public static class Square {
        public Point topLeft;
        public double side;
    }
    
    public static class Rectangle {
        public Point topLeft;
        public double height, width;
    }
    
    public static class Circle {
        public Point center;
        public double radius;
    }
    
    public double calculateArea(Object shape) throws NoSuchShapeException {
        if (shape instanceof Square) {
            Square s = (Square) shape;
            return s.side * s.side;
        } else if (shape instanceof Rectangle) {
            Rectangle r = (Rectangle) shape;
            return r.height * r.width;
        } else if (shape instanceof Circle) {
            Circle c = (Circle) shape;
            return Math.PI * c.radius * c.radius;
        }
        throw new NoSuchShapeException();
    }
    
    public double calculatePerimeter(Object shape) throws NoSuchShapeException {
        if (shape instanceof Square) {
            Square s = (Square) shape;
            return 4 * s.side;
        } else if (shape instanceof Rectangle) {
            Rectangle r = (Rectangle) shape;
            return 2 * (r.height + r.width);
        } else if (shape instanceof Circle) {
            Circle c = (Circle) shape;
            return 2 * Math.PI * c.radius;
        }
        throw new NoSuchShapeException();
    }
    
    public void draw(Object shape) throws NoSuchShapeException {
        if (shape instanceof Square) {
            Square s = (Square) shape;
            System.out.println("Drawing Square at (" + s.topLeft.x + "," + s.topLeft.y + ") with side " + s.side);
        } else if (shape instanceof Rectangle) {
            Rectangle r = (Rectangle) shape;
            System.out.println("Drawing Rectangle at (" + r.topLeft.x + "," + r.topLeft.y + ") " + r.width + "x" + r.height);
        } else if (shape instanceof Circle) {
            Circle c = (Circle) shape;
            System.out.println("Drawing Circle at (" + c.center.x + "," + c.center.y + ") with radius " + c.radius);
        }
        throw new NoSuchShapeException();
    }
}

class NoSuchShapeException extends Exception {
    public NoSuchShapeException() {
        super("Unknown shape type");
    }
}
```

### 변환 과제 1: 객체지향 방식으로 변환

다음 원칙을 적용하여 객체지향으로 변환하세요:

1. **다형성 활용**: 타입 체크 대신 다형성 사용
2. **캡슐화**: 데이터와 행동을 함께 묶기
3. **확장성**: 새로운 도형 추가가 쉽도록 설계

### 변환 결과 템플릿

#### Java 객체지향 변환 결과
```java
// Good: 객체지향 방식
public abstract class Shape {
    protected final Point position;
    
    public Shape(Point position) {
        this.position = new Point(position.x, position.y);
    }
    
    public abstract double calculateArea();
    public abstract double calculatePerimeter();
    public abstract void draw();
    
    public Point getPosition() {
        return new Point(position.x, position.y);
    }
}

public class Point {
    private final double x;
    private final double y;
    
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }
    
    public double getX() { return x; }
    public double getY() { return y; }
    
    @Override
    public String toString() {
        return String.format("(%.1f, %.1f)", x, y);
    }
}

public class Square extends Shape {
    private final double side;
    
    public Square(Point topLeft, double side) {
        super(topLeft);
        this.side = side;
    }
    
    @Override
    public double calculateArea() {
        return side * side;
    }
    
    @Override
    public double calculatePerimeter() {
        return 4 * side;
    }
    
    @Override
    public void draw() {
        System.out.printf("Drawing Square at %s with side %.1f%n", 
                         position, side);
    }
    
    public double getSide() { return side; }
}

public class Rectangle extends Shape {
    private final double width;
    private final double height;
    
    public Rectangle(Point topLeft, double width, double height) {
        super(topLeft);
        this.width = width;
        this.height = height;
    }
    
    @Override
    public double calculateArea() {
        return width * height;
    }
    
    @Override
    public double calculatePerimeter() {
        return 2 * (width + height);
    }
    
    @Override
    public void draw() {
        System.out.printf("Drawing Rectangle at %s %.1fx%.1f%n", 
                         position, width, height);
    }
}

public class Circle extends Shape {
    private final double radius;
    
    public Circle(Point center, double radius) {
        super(center);
        this.radius = radius;
    }
    
    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
    
    @Override
    public double calculatePerimeter() {
        return 2 * Math.PI * radius;
    }
    
    @Override
    public void draw() {
        System.out.printf("Drawing Circle at %s with radius %.1f%n", 
                         position, radius);
    }
    
    public double getRadius() { return radius; }
}

// 사용 예시
public class ShapeManager {
    private final List<Shape> shapes = new ArrayList<>();
    
    public void addShape(Shape shape) {
        shapes.add(shape);
    }
    
    public double calculateTotalArea() {
        return shapes.stream()
                    .mapToDouble(Shape::calculateArea)
                    .sum();
    }
    
    public void drawAllShapes() {
        shapes.forEach(Shape::draw);
    }
}
```

### 변환 대상 코드 - 객체지향 → 자료구조

#### Java 예시 - 과도한 캡슐화
```java
// Bad: 과도한 객체지향 (자료구조가 더 적합한 경우)
public class Employee {
    private String firstName;
    private String lastName;
    private String department;
    private double salary;
    private LocalDate hireDate;
    private String email;
    private String phoneNumber;
    
    // 수많은 getter/setter들
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    
    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }
    
    public String getDepartment() { return department; }
    public void setDepartment(String department) { this.department = department; }
    
    public double getSalary() { return salary; }
    public void setSalary(double salary) { this.salary = salary; }
    
    public LocalDate getHireDate() { return hireDate; }
    public void setHireDate(LocalDate hireDate) { this.hireDate = hireDate; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public String getPhoneNumber() { return phoneNumber; }
    public void setPhoneNumber(String phoneNumber) { this.phoneNumber = phoneNumber; }
    
    // 의미 있는 행동이 없음
    public String getFullName() {
        return firstName + " " + lastName;
    }
    
    public boolean isLongTermEmployee() {
        return ChronoUnit.YEARS.between(hireDate, LocalDate.now()) >= 5;
    }
}

public class EmployeeProcessor {
    public void processEmployeeData(Employee employee) {
        // 모든 필드에 접근하기 위해 수많은 getter 호출
        String report = String.format(
            "Employee: %s %s\nDepartment: %s\nSalary: %.2f\nHire Date: %s\nEmail: %s\nPhone: %s",
            employee.getFirstName(),
            employee.getLastName(), 
            employee.getDepartment(),
            employee.getSalary(),
            employee.getHireDate(),
            employee.getEmail(),
            employee.getPhoneNumber()
        );
        
        System.out.println(report);
    }
}
```

### 변환 과제 2: 자료구조 방식으로 변환

다음 상황에서는 자료구조가 더 적합합니다:
- 단순한 데이터 전송 객체(DTO)
- 설정 정보 저장
- 데이터베이스 레코드 표현

### 변환 결과 템플릿

#### Java 자료구조 변환 결과
```java
// Good: 단순한 자료구조 (Record 사용 - Java 14+)
public record EmployeeData(
    String firstName,
    String lastName,
    String department,
    double salary,
    LocalDate hireDate,
    String email,
    String phoneNumber
) {
    // 생성자에서 유효성 검사
    public EmployeeData {
        if (firstName == null || firstName.trim().isEmpty()) {
            throw new IllegalArgumentException("First name cannot be empty");
        }
        if (lastName == null || lastName.trim().isEmpty()) {
            throw new IllegalArgumentException("Last name cannot be empty");
        }
        if (salary < 0) {
            throw new IllegalArgumentException("Salary cannot be negative");
        }
    }
    
    // 파생 데이터를 위한 메서드
    public String fullName() {
        return firstName + " " + lastName;
    }
    
    public long yearsOfService() {
        return ChronoUnit.YEARS.between(hireDate, LocalDate.now());
    }
}

// 비즈니스 로직은 별도 서비스에서 처리
public class EmployeeService {
    public boolean isEligibleForPromotion(EmployeeData employee) {
        return employee.yearsOfService() >= 2 && employee.salary() >= 50000;
    }
    
    public double calculateBonus(EmployeeData employee) {
        if (employee.yearsOfService() >= 5) {
            return employee.salary() * 0.1;
        } else if (employee.yearsOfService() >= 2) {
            return employee.salary() * 0.05;
        }
        return 0;
    }
    
    public String generateReport(EmployeeData employee) {
        return String.format("""
            Employee Report
            ===============
            Name: %s
            Department: %s
            Salary: $%.2f
            Years of Service: %d
            Bonus Eligible: $%.2f
            """, 
            employee.fullName(),
            employee.department(),
            employee.salary(),
            employee.yearsOfService(),
            calculateBonus(employee)
        );
    }
}
```

### 구조 변환 체크리스트
```markdown
## 구조 변환 체크리스트

### 객체지향 설계 체크 (절차적 → 객체지향)
- [ ] 타입 체크 코드를 다형성으로 대체
- [ ] 데이터와 행동을 함께 묶음
- [ ] 새로운 타입 추가 시 기존 코드 수정 불필요
- [ ] 캡슐화를 통한 데이터 보호

### 자료구조 설계 체크 (객체지향 → 자료구조)
- [ ] 단순한 데이터 저장 목적
- [ ] 의미 있는 행동 부재
- [ ] 모든 필드 접근이 필요한 경우
- [ ] 불변성 보장 (final, record 등)

### 설계 선택 기준
| 상황 | 객체 지향 | 자료구조 |
|------|-----------|----------|
| 새로운 타입 추가 빈번 | ✅ 적합 | ❌ 부적합 |
| 새로운 함수 추가 빈번 | ❌ 부적합 | ✅ 적합 |
| 복잡한 비즈니스 로직 | ✅ 적합 | ❌ 부적합 |
| 단순한 데이터 전송 | ❌ 부적합 | ✅ 적합 |
```

## 실습 2: 디미터 법칙 적용 (35분)

### 목표
기차 충돌(Train Wreck)이 일어나는 코드를 디미터 법칙에 맞게 수정합니다.

### 개선 대상 코드

#### Java 예시 - 주문 시스템
```java
// Bad: 디미터 법칙 위반 (기차 충돌)
public class OrderProcessor {
    public void processOrder(Order order) {
        // 기차 충돌 - 여러 단계의 객체 체인 접근
        String customerCity = order.getCustomer().getAddress().getCity();
        String customerCountry = order.getCustomer().getAddress().getCountry();
        
        // 배송비 계산을 위한 복잡한 체인
        double shippingFee = order.getShippingInfo()
                                 .getDestination()
                                 .getRegion()
                                 .getShippingRate()
                                 .getStandardRate();
        
        // 할인 정보 접근
        boolean isVipCustomer = order.getCustomer()
                                    .getMembership()
                                    .getLevel()
                                    .equals("VIP");
        
        // 재고 확인
        for (OrderItem item : order.getItems()) {
            int availableStock = item.getProduct()
                                    .getInventory()
                                    .getWarehouse()
                                    .getStock()
                                    .getAvailableQuantity();
            
            if (availableStock < item.getQuantity()) {
                throw new InsufficientStockException("Not enough stock for " + 
                    item.getProduct().getName());
            }
        }
        
        // 결제 정보 처리
        String paymentMethod = order.getPayment()
                                   .getMethod()
                                   .getType()
                                   .toString();
        
        if (paymentMethod.equals("CREDIT_CARD")) {
            String cardNumber = order.getPayment()
                                    .getMethod()
                                    .getCreditCard()
                                    .getNumber();
            // 카드 처리...
        }
        
        System.out.println("Processing order for " + customerCity + ", " + customerCountry);
        System.out.println("Shipping fee: " + shippingFee);
        System.out.println("VIP customer: " + isVipCustomer);
    }
}

// 관련 클래스들 (문제가 있는 구조)
class Order {
    private Customer customer;
    private List<OrderItem> items;
    private ShippingInfo shippingInfo;
    private Payment payment;
    
    // getter들...
    public Customer getCustomer() { return customer; }
    public List<OrderItem> getItems() { return items; }
    public ShippingInfo getShippingInfo() { return shippingInfo; }
    public Payment getPayment() { return payment; }
}

class Customer {
    private Address address;
    private Membership membership;
    
    public Address getAddress() { return address; }
    public Membership getMembership() { return membership; }
}

class Address {
    private String city;
    private String country;
    
    public String getCity() { return city; }
    public String getCountry() { return country; }
}
```

### 개선 과제

다음 디미터 법칙을 적용하여 개선하세요:

1. **최소 지식 원칙**: 객체는 자신과 직접 관련된 객체만 알아야 함
2. **메서드 위임**: 복잡한 탐색 대신 적절한 메서드 제공
3. **캡슐화 강화**: 내부 구조를 숨기고 인터페이스 제공

### 개선 결과 템플릿

#### Java 디미터 법칙 적용 결과
```java
// Good: 디미터 법칙 준수
public class OrderProcessor {
    private final ShippingCalculator shippingCalculator;
    private final StockValidator stockValidator;
    private final PaymentProcessor paymentProcessor;
    
    public OrderProcessor(ShippingCalculator shippingCalculator,
                         StockValidator stockValidator,
                         PaymentProcessor paymentProcessor) {
        this.shippingCalculator = shippingCalculator;
        this.stockValidator = stockValidator;
        this.paymentProcessor = paymentProcessor;
    }
    
    public void processOrder(Order order) {
        // 디미터 법칙 준수 - 직접적인 메서드 호출
        String customerLocation = order.getCustomerLocation();
        double shippingFee = order.calculateShippingFee();
        boolean isVipCustomer = order.isVipCustomer();
        
        // 재고 검증 - 책임을 적절한 객체에 위임
        if (!stockValidator.hasEnoughStock(order)) {
            throw new InsufficientStockException("Insufficient stock for order");
        }
        
        // 결제 처리 - 결제 관련 로직은 결제 처리기에 위임
        PaymentResult result = paymentProcessor.processPayment(order);
        if (!result.isSuccessful()) {
            throw new PaymentException("Payment failed: " + result.getErrorMessage());
        }
        
        System.out.println("Processing order for " + customerLocation);
        System.out.println("Shipping fee: " + shippingFee);
        System.out.println("VIP customer: " + isVipCustomer);
    }
}

// 개선된 Order 클래스 - 적절한 메서드 제공
public class Order {
    private final Customer customer;
    private final List<OrderItem> items;
    private final ShippingInfo shippingInfo;
    private final Payment payment;
    
    public Order(Customer customer, List<OrderItem> items, 
                ShippingInfo shippingInfo, Payment payment) {
        this.customer = customer;
        this.items = new ArrayList<>(items);
        this.shippingInfo = shippingInfo;
        this.payment = payment;
    }
    
    // 디미터 법칙 준수 - 위임 메서드들
    public String getCustomerLocation() {
        return customer.getFullAddress();
    }
    
    public double calculateShippingFee() {
        return shippingInfo.calculateFee(customer.getShippingRegion());
    }
    
    public boolean isVipCustomer() {
        return customer.isVipMember();
    }
    
    public List<OrderItem> getItems() {
        return new ArrayList<>(items);
    }
    
    public boolean hasPaymentMethod(PaymentType type) {
        return payment.isOfType(type);
    }
    
    public PaymentDetails getPaymentDetails() {
        return payment.getPaymentDetails();
    }
    
    public double getTotalAmount() {
        return items.stream()
                   .mapToDouble(OrderItem::getSubtotal)
                   .sum();
    }
}

// 개선된 Customer 클래스
public class Customer {
    private final String id;
    private final String name;
    private final Address address;
    private final Membership membership;
    
    public Customer(String id, String name, Address address, Membership membership) {
        this.id = id;
        this.name = name;
        this.address = address;
        this.membership = membership;
    }
    
    // 위임 메서드들 - 내부 구조를 숨김
    public String getFullAddress() {
        return address.getFullAddress();
    }
    
    public String getShippingRegion() {
        return address.getRegion();
    }
    
    public boolean isVipMember() {
        return membership.isVipLevel();
    }
    
    public String getId() { return id; }
    public String getName() { return name; }
}

// 개선된 Address 클래스
public class Address {
    private final String street;
    private final String city;
    private final String state;
    private final String country;
    private final String postalCode;
    
    public Address(String street, String city, String state, 
                  String country, String postalCode) {
        this.street = street;
        this.city = city;
        this.state = state;
        this.country = country;
        this.postalCode = postalCode;
    }
    
    public String getFullAddress() {
        return String.format("%s, %s, %s, %s %s", 
                           street, city, state, country, postalCode);
    }
    
    public String getRegion() {
        return country; // 또는 더 복잡한 지역 결정 로직
    }
    
    public String getCity() { return city; }
    public String getCountry() { return country; }
}

// 보조 서비스 클래스들
public class StockValidator {
    public boolean hasEnoughStock(Order order) {
        return order.getItems().stream()
                   .allMatch(this::hasEnoughStockForItem);
    }
    
    private boolean hasEnoughStockForItem(OrderItem item) {
        return item.isStockAvailable();
    }
}

public class PaymentProcessor {
    public PaymentResult processPayment(Order order) {
        if (order.hasPaymentMethod(PaymentType.CREDIT_CARD)) {
            return processCreditCardPayment(order);
        } else if (order.hasPaymentMethod(PaymentType.PAYPAL)) {
            return processPayPalPayment(order);
        }
        return PaymentResult.failure("Unsupported payment method");
    }
    
    private PaymentResult processCreditCardPayment(Order order) {
        // 신용카드 결제 처리
        return PaymentResult.success("Credit card payment processed");
    }
    
    private PaymentResult processPayPalPayment(Order order) {
        // PayPal 결제 처리
        return PaymentResult.success("PayPal payment processed");
    }
}
```

### 디미터 법칙 체크리스트
```markdown
## 디미터 법칙 체크리스트

### 위반 패턴 확인
- [ ] 메서드 체이닝 (a.getB().getC().getD())
- [ ] 깊은 탐색 (3단계 이상의 객체 접근)
- [ ] 내부 구조에 대한 과도한 지식
- [ ] 기차 충돌 코드

### 개선 방법
- [ ] 위임 메서드 제공
- [ ] 적절한 추상화 레벨 유지
- [ ] 책임 분산
- [ ] 인터페이스 단순화

### 개선 효과
| 항목 | Before | After |
|------|--------|--------|
| 결합도 | 높음 | 낮음 |
| 유지보수성 | 어려움 | 쉬움 |
| 테스트 용이성 | 어려움 | 쉬움 |
| 캡슐화 | 약함 | 강함 |
```

## 실습 3: DTO 설계 (30분)

### 목표
실제 시스템에서 사용할 DTO(Data Transfer Object)와 비즈니스 객체를 분리하여 설계합니다.

### 설계 요구사항

다음 시나리오에 대한 DTO와 비즈니스 객체를 설계하세요:

**시나리오**: 온라인 쇼핑몰의 상품 관리 시스템
- 상품 정보 조회 API
- 상품 생성/수정 API
- 상품 검색 API

### 설계 과제

1. **API 응답용 DTO** 설계
2. **API 요청용 DTO** 설계  
3. **비즈니스 도메인 객체** 설계
4. **매핑 로직** 구현

### 설계 결과 템플릿

#### DTO 설계 결과
```java
// API 응답용 DTO
public record ProductResponseDto(
    Long id,
    String name,
    String description,
    BigDecimal price,
    String category,
    int stockQuantity,
    boolean available,
    LocalDateTime createdAt,
    LocalDateTime updatedAt,
    List<String> imageUrls,
    ProductRatingDto rating
) {}

public record ProductRatingDto(
    double averageRating,
    int totalReviews
) {}

// API 요청용 DTO (생성)
public record CreateProductRequestDto(
    @NotBlank String name,
    @NotBlank String description,
    @NotNull @DecimalMin("0.01") BigDecimal price,
    @NotBlank String category,
    @NotNull @Min(0) Integer stockQuantity,
    List<String> imageUrls
) {}

// API 요청용 DTO (수정)
public record UpdateProductRequestDto(
    String name,
    String description,
    BigDecimal price,
    String category,
    Integer stockQuantity,
    List<String> imageUrls
) {}

// 검색용 DTO
public record ProductSearchDto(
    String keyword,
    String category,
    BigDecimal minPrice,
    BigDecimal maxPrice,
    Boolean availableOnly,
    String sortBy,
    String sortDirection,
    int page,
    int size
) {
    public ProductSearchDto {
        // 기본값 설정
        page = Math.max(0, page);
        size = Math.max(1, Math.min(100, size));
        sortBy = sortBy != null ? sortBy : "name";
        sortDirection = sortDirection != null ? sortDirection : "ASC";
    }
}

// 비즈니스 도메인 객체
public class Product {
    private final ProductId id;
    private ProductName name;
    private ProductDescription description;
    private Price price;
    private Category category;
    private Stock stock;
    private final List<ProductImage> images;
    private final ProductMetadata metadata;
    
    public Product(ProductId id, ProductName name, ProductDescription description,
                  Price price, Category category, Stock stock) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.price = price;
        this.category = category;
        this.stock = stock;
        this.images = new ArrayList<>();
        this.metadata = new ProductMetadata();
    }
    
    // 비즈니스 로직 메서드들
    public boolean isAvailable() {
        return stock.isAvailable();
    }
    
    public void updatePrice(Price newPrice) {
        if (newPrice.isLowerThan(this.price)) {
            // 가격 인하 시 특별 처리
            metadata.recordPriceChange(this.price, newPrice);
        }
        this.price = newPrice;
    }
    
    public void reserveStock(int quantity) {
        if (!stock.canReserve(quantity)) {
            throw new InsufficientStockException(
                "Cannot reserve " + quantity + " items. Available: " + stock.getAvailable()
            );
        }
        stock.reserve(quantity);
    }
    
    public void addImage(ProductImage image) {
        if (images.size() >= 10) {
            throw new IllegalStateException("Maximum 10 images allowed per product");
        }
        images.add(image);
    }
    
    // 도메인 이벤트 발생
    public void markAsOutOfStock() {
        if (stock.isEmpty()) {
            DomainEvents.publish(new ProductOutOfStockEvent(this.id));
        }
    }
    
    // Getters for necessary fields
    public ProductId getId() { return id; }
    public ProductName getName() { return name; }
    public ProductDescription getDescription() { return description; }
    public Price getPrice() { return price; }
    public Category getCategory() { return category; }
    public Stock getStock() { return stock; }
    public List<ProductImage> getImages() { return new ArrayList<>(images); }
    public ProductMetadata getMetadata() { return metadata; }
}

// 값 객체들
public record ProductId(Long value) {
    public ProductId {
        if (value == null || value <= 0) {
            throw new IllegalArgumentException("Product ID must be positive");
        }
    }
}

public record Price(BigDecimal amount) {
    public Price {
        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("Price must be positive");
        }
    }
    
    public boolean isLowerThan(Price other) {
        return this.amount.compareTo(other.amount) < 0;
    }
}

// 매핑 서비스
@Service
public class ProductMapper {
    
    public ProductResponseDto toResponseDto(Product product) {
        return new ProductResponseDto(
            product.getId().value(),
            product.getName().value(),
            product.getDescription().value(),
            product.getPrice().amount(),
            product.getCategory().name(),
            product.getStock().getAvailable(),
            product.isAvailable(),
            product.getMetadata().getCreatedAt(),
            product.getMetadata().getUpdatedAt(),
            product.getImages().stream()
                   .map(ProductImage::getUrl)
                   .toList(),
            new ProductRatingDto(
                product.getMetadata().getAverageRating(),
                product.getMetadata().getTotalReviews()
            )
        );
    }
    
    public Product fromCreateRequest(CreateProductRequestDto dto) {
        return new Product(
            null, // ID는 저장 시 생성
            new ProductName(dto.name()),
            new ProductDescription(dto.description()),
            new Price(dto.price()),
            Category.valueOf(dto.category()),
            new Stock(dto.stockQuantity())
        );
    }
    
    public void updateFromRequest(Product product, UpdateProductRequestDto dto) {
        if (dto.name() != null) {
            product.updateName(new ProductName(dto.name()));
        }
        if (dto.description() != null) {
            product.updateDescription(new ProductDescription(dto.description()));
        }
        if (dto.price() != null) {
            product.updatePrice(new Price(dto.price()));
        }
        // ... 기타 필드 업데이트
    }
}
```

## 평가 기준

### 실습 1: 구조 변환 (40점)
- 적절한 설계 패턴 선택 (20점)
- 객체지향/자료구조 원칙 적용 (15점)
- 확장성과 유지보수성 고려 (5점)

### 실습 2: 디미터 법칙 적용 (35점)
- 기차 충돌 제거 (15점)
- 적절한 위임 메서드 설계 (15점)
- 캡슐화 강화 (5점)

### 실습 3: DTO 설계 (25점)
- DTO와 도메인 객체 분리 (15점)
- 적절한 매핑 로직 (10점)

## 제출 형식
- 파일명: `06_objects-vs-data-structures_실습_[이름].md`
- 제출 기한: 다음 강의 시작 전
- 포함 내용: 
  - 변환된 코드
  - 디미터 법칙 적용 결과
  - DTO 설계 문서

## 추가 자료
- Martin Fowler의 "Refactoring" - Data Class와 Feature Envy
- Domain-Driven Design 관련 자료
- DTO vs Entity 설계 패턴
- Law of Demeter 상세 가이드 