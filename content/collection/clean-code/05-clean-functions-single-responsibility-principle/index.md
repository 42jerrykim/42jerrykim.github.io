---
draft: true
---
# 3장: 함수 작성법

## 강의 목표
- 작고 명확한 함수 작성 능력 개발
- 단일 책임 원칙을 함수 레벨에서 적용
- 함수의 추상화 수준 이해와 적용

## 작게 만들어라

함수를 만드는 첫 번째 규칙은 '작게!'다. 함수를 만드는 두 번째 규칙은 '더 작게!'다.

### 함수가 작아야 하는 이유
- **이해하기 쉽다**: 작은 함수는 한눈에 들어온다
- **테스트하기 쉽다**: 적은 경로와 조건을 가진다
- **재사용하기 쉽다**: 단일 책임을 가지므로 다른 곳에서도 활용 가능
- **디버깅하기 쉽다**: 문제가 발생한 지점을 빠르게 찾을 수 있다

### 다양한 언어에서의 함수 분해 예제

```java
// Java - Bad: 긴 함수
public static String testableHtml(PageData pageData, boolean includeSuiteSetup) {
    WikiPage wikiPage = pageData.getWikiPage();
    StringBuffer buffer = new StringBuffer();
    if (pageData.hasAttribute("Test")) {
        if (includeSuiteSetup) {
            WikiPage suiteSetup = PageCrawlerImpl.getInheritedPage(
                SuiteResponder.SUITE_SETUP_NAME, wikiPage);
            if (suiteSetup != null) {
                WikiPagePath pagePath = suiteSetup.getPageCrawler().getFullPath(suiteSetup);
                String pagePathName = PathParser.render(pagePath);
                buffer.append("!include -setup .").append(pagePathName).append("\n");
            }
        }
        // ... 더 많은 코드
    }
    return buffer.toString();
}

// Java - Good: 작은 함수들로 분해
public static String renderPageWithSetupsAndTeardowns(PageData pageData, boolean isSuite) {
    boolean isTestPage = pageData.hasAttribute("Test");
    if (isTestPage) {
        WikiPage testPage = pageData.getWikiPage();
        StringBuffer newPageContent = new StringBuffer();
        includeSetupPages(testPage, newPageContent, isSuite);
        newPageContent.append(pageData.getContent());
        includeTeardownPages(testPage, newPageContent, isSuite);
        pageData.setContent(newPageContent.toString());
    }
    return pageData.getHtml();
}
```

```python
# Python - Bad: 긴 함수
def process_user_order(user_id, items, discount_code):
    # 사용자 검증
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("Invalid user")
    if not user.is_active:
        raise ValueError("Inactive user")
        
    # 재고 확인
    total_price = 0
    for item in items:
        stock = get_stock(item['id'])
        if stock < item['quantity']:
            raise ValueError(f"Insufficient stock for {item['name']}")
        total_price += item['price'] * item['quantity']
    
    # 할인 적용
    if discount_code:
        discount = get_discount(discount_code)
        if discount and discount.is_valid():
            total_price = total_price * (1 - discount.percentage)
    
    # 주문 생성 및 저장
    order = create_order(user, items, total_price)
    save_order(order)
    send_confirmation_email(user.email, order)
    return order

# Python - Good: 작은 함수들로 분해
def process_user_order(user_id, items, discount_code):
    user = validate_user(user_id)
    validate_stock(items)
    total_price = calculate_total_price(items, discount_code)
    order = create_and_save_order(user, items, total_price)
    notify_order_confirmation(user, order)
    return order

def validate_user(user_id):
    user = get_user_by_id(user_id)
    if not user or not user.is_active:
        raise ValueError("Invalid or inactive user")
    return user
```

```javascript
// JavaScript - Bad: 긴 함수
function processPayment(cardData, amount, currency) {
    // 카드 검증
    if (!cardData.number || cardData.number.length < 16) {
        throw new Error('Invalid card number');
    }
    if (!cardData.cvv || cardData.cvv.length < 3) {
        throw new Error('Invalid CVV');
    }
    
    // 금액 검증
    if (amount <= 0) {
        throw new Error('Invalid amount');
    }
    
    // 환율 적용
    let convertedAmount = amount;
    if (currency !== 'USD') {
        const exchangeRate = getExchangeRate(currency);
        convertedAmount = amount * exchangeRate;
    }
    
    // 결제 처리
    const paymentData = {
        cardNumber: cardData.number,
        amount: convertedAmount,
        timestamp: new Date()
    };
    
    const result = chargeCard(paymentData);
    logTransaction(result);
    sendReceipt(cardData.email, result);
    
    return result;
}

// JavaScript - Good: 작은 함수들로 분해
function processPayment(cardData, amount, currency) {
    validateCardData(cardData);
    validateAmount(amount);
    const convertedAmount = convertCurrency(amount, currency);
    const paymentResult = executePayment(cardData, convertedAmount);
    finalizePayment(cardData.email, paymentResult);
    return paymentResult;
}

function validateCardData(cardData) {
    if (!cardData.number || cardData.number.length < 16) {
        throw new Error('Invalid card number');
    }
    if (!cardData.cvv || cardData.cvv.length < 3) {
        throw new Error('Invalid CVV');
    }
}
```

### 블록과 들여쓰기
if 문/else 문/while 문 등에 들어가는 블록은 한 줄이어야 합니다. 대개 거기서 함수를 호출합니다. 그러면 바깥을 감싸는 함수(enclosing function)가 작아질 뿐 아니라 블록 안에서 호출하는 함수 이름을 적절히 짓는다면, 코드를 이해하기도 쉬워집니다.

중첩 구조가 생길만큼 함수가 커져서는 안 됩니다. 함수에서 들여쓰기 수준은 1단이나 2단을 넘어서면 안 됩니다.

## 한 가지만 해라

> **함수는 한 가지를 해야 한다. 그 한 가지를 잘 해야 한다. 그 한 가지만을 해야 한다.**

### 한 가지 일을 판단하는 기준
함수가 '한 가지'만 하는지 판단하는 방법이 하나 더 있습니다. 단순히 다른 표현이 아니라 의미 있는 이름으로 다른 함수를 추출할 수 있다면 그 함수는 여러 작업을 하는 셈입니다.

### TO 문단 기법
함수를 기술할 때 TO 문단으로 기술할 수 있다면 그 함수는 한 가지 작업만 한다는 증거입니다.

```
TO RenderPageWithSetupsAndTeardowns, 페이지가 테스트 페이지인지 확인한 후 테스트 페이지라면 설정 페이지와 해제 페이지를 넣는다. 테스트 페이지가 아니라면 페이지를 그대로 반환한다.
```

## 함수 당 추상화 수준은 하나로

함수가 확실히 '한 가지' 작업만 하려면 함수 내 모든 문장의 추상화 수준이 동일해야 합니다.

### 추상화 수준 예시
- **높은 수준**: `getHtml()`
- **중간 수준**: `String pagePathName = PathParser.render(pagePath)`  
- **낮은 수준**: `.append("\n")`

한 함수 내에서 추상화 수준을 섞으면 코드를 읽는 사람이 헷갈립니다. 특정 표현이 근본 개념인지 아니면 세부사항인지 구분하기 어려운 탓입니다.

### 내려가기 규칙
코드는 위에서 아래로 이야기처럼 읽혀야 좋습니다. 한 함수 다음에는 추상화 수준이 한 단계 낮은 함수가 옵니다. 즉, 위에서 아래로 읽으면 함수 추상화 수준이 한 번에 한 단계씩 낮아집니다.

```
TO 설정 페이지와 해제 페이지를 포함하려면, 설정 페이지를 포함하고, 테스트 페이지 내용을 포함하고, 해제 페이지를 포함한다.
  TO 설정 페이지를 포함하려면, 슈트이면 슈트 설정 페이지를 포함한 후 일반 설정 페이지를 포함한다.
    TO 슈트 설정 페이지를 포함하려면, 부모 계층에서 "SuiteSetUp" 페이지를 찾아 include 문과 페이지 경로를 추가한다.
```

## Switch 문

switch 문은 작게 만들기 어렵습니다. 또한 '한 가지' 작업만 하는 switch 문도 만들기 어렵습니다. 본질적으로 switch 문은 N가지를 처리합니다.

### Switch 문의 문제점
```java
// Bad: Switch문이 반복됨
public Money calculatePay(Employee e) throws InvalidEmployeeType {
    switch (e.type) {
        case COMMISSIONED:
            return calculateCommissionedPay(e);
        case HOURLY:
            return calculateHourlyPay(e);
        case SALARIED:
            return calculateSalariedPay(e);
        default:
            throw new InvalidEmployeeType(e.type);
    }
}
```

이 함수에는 몇 가지 문제가 있습니다:
1. 함수가 길다 (새 직원 유형을 추가하면 더 길어진다)
2. '한 가지' 작업만 수행하지 않는다
3. SRP(Single Responsibility Principle)를 위반한다
4. OCP(Open Closed Principle)를 위반한다

### 다형성을 활용한 해결책
```java
// Good: 다형성 활용
public abstract class Employee {
    public abstract boolean isPayday();
    public abstract Money calculatePay();
    public abstract void deliverPay(Money pay);
}

public interface EmployeeFactory {
    public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType;
}

public class EmployeeFactoryImpl implements EmployeeFactory {
    public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType {
        switch (r.type) {
            case COMMISSIONED:
                return new CommissionedEmployee(r);
            case HOURLY:
                return new HourlyEmployee(r);
            case SALARIED:
                return new SalariedEmployee(r);
            default:
                throw new InvalidEmployeeType(r.type);
        }
    }
}
```

## 서술적인 이름을 사용하라

> "코드를 읽으면서 짐작했던 기능을 각 루틴이 그대로 수행한다면 깨끗한 코드라 불러도 되겠다." - Ward Cunningham

작은 함수에게 좋은 이름을 붙이는 것이 더 중요합니다.

### 좋은 함수 이름의 조건
- **길어도 괜찮다**: `testableHtml` 보다는 `SetupTeardownIncluder.render`
- **일관성이 있어야 한다**: 모듈 내에서 함수 이름은 같은 문구, 명사, 동사를 사용

**예시**: `includeSetupAndTeardownPages`, `includeSetupPages`, `includeSuiteSetupPage`, `includeSetupPage` 등은 비슷한 문구를 사용해 일관성을 보여줍니다.

## 함수 인수

함수에서 이상적인 인수 개수는 0개(무항)입니다. 다음은 1개(단항), 다음은 2개(이항)입니다. 3개(삼항)는 가능한 한 피하는 편이 좋습니다. 4개 이상(다항)은 특별한 이유가 필요합니다.

### 인수가 어려운 이유
- **개념적으로 어렵다**: 인수는 개념을 이해하기 어렵게 만든다
- **테스트 관점에서 어렵다**: 갖가지 인수 조합으로 함수를 검증하는 테스트 케이스를 작성해야 한다

### 많이 쓰이는 단항 형식
1. **인수에 질문을 던지는 경우**
   - `boolean fileExists("MyFile")`

2. **인수를 뭔가로 변환해 결과를 반환하는 경우**
   - `InputStream fileOpen("MyFile")`

3. **이벤트 함수**
   - `void passwordAttemptFailedNtimes(int attempts)`

### 플래그 인수
플래그 인수는 추하다! 함수로 부울 값을 넘기는 관례는 정말로 끔찍합니다. 부울 값으로 함수 동작을 제어하는 것은 함수가 한꺼번에 여러 가지를 처리한다고 대놓고 공표하는 셈입니다.

```java
// Bad
render(boolean isSuite)

// Good  
renderForSuite()
renderForSingleTest()
```

### 이항 함수
인수가 2개인 함수는 인수가 1개인 함수보다 이해하기 어렵습니다.

```java
// 자연적인 순서가 있는 경우는 괜찮음
Point p = new Point(0, 0);

// 하지만 다음은 혼란스러움
assertEquals(expected, actual);  // 순서를 기억해야 함
```

### 삼항 함수
인수가 3개인 함수는 신중히 고려하라고 권합니다.

```java
// 순서를 기억하기 어려움
assertEquals(message, expected, actual)

// 더 좋은 방법
assertEquals(1.0, amount, .001)  // 부동소수점 비교시 델타값
```

### 인수 객체
인수가 2-3개 필요하다면 일부를 독자적인 클래스 변수로 선언할 가능성을 짚어봅니다.

```java
// Bad
Circle makeCircle(double x, double y, double radius);

// Good
Circle makeCircle(Point center, double radius);
```

### 인수 목록
때로는 인수 개수가 가변적인 함수도 필요합니다.

```java
String.format("%s worked %.2f hours.", name, hours);

// 실제로는 이항 함수다
String.format(String format, Object... args);
```

### 동사와 키워드
함수의 의도나 인수의 순서와 의도를 제대로 표현하려면 좋은 함수 이름이 필수입니다.

```java
// Bad
write(name);

// Good
writeField(name);

// 더 좋음 (키워드 형식)
assertEquals(expected, actual);
assertExpectedEqualsActual(expected, actual);
```

## 부수 효과를 일으키지 마라

부수 효과는 거짓말입니다. 함수에서 한 가지를 하겠다고 약속하고선 남몰래 다른 짓도 하니까요.

```java
// Bad: 부수 효과가 있는 함수
public class UserValidator {
    private Cryptographer cryptographer;
    
    public boolean checkPassword(String userName, String password) {
        User user = UserGateway.findByName(userName);
        if (user != null) {
            String codedPhrase = user.getPhraseEncodedByPassword();
            String phrase = cryptographer.decrypt(codedPhrase, password);
            if ("Valid Password".equals(phrase)) {
                Session.initialize();  // 부수 효과!
                return true;
            }
        }
        return false;
    }
}
```

함수 이름은 암호를 확인한다고 되어 있지만, 세션을 초기화한다는 부수 효과가 있습니다.

### 출력 인수
일반적으로 우리는 인수를 함수 입력으로 해석합니다.

```java
// Bad: 출력 인수
appendFooter(s);  // s에 footer를 append하는가? 아니면 s를 footer에 append하는가?

// Good: 객체 지향
report.appendFooter();
```

## 명령과 조회를 분리하라

함수는 뭔가를 수행하거나 뭔가에 답하거나 둘 중 하나만 해야 합니다. 둘 다 하면 안 됩니다.

```java
// Bad: 명령과 조회를 동시에
public boolean set(String attribute, String value);

if (set("username", "unclebob")) {
    // set이 성공했다는 뜻인가? 아니면 username이 unclebob으로 설정되어 있다는 뜻인가?
}

// Good: 명령과 조회 분리
if (attributeExists("username")) {
    setAttribute("username", "unclebob");
}
```

## 오류 코드보다 예외를 사용하라

명령 함수에서 오류 코드를 반환하는 방식은 명령/조회 분리 규칙을 미묘하게 위반합니다.

```java
// Bad: 오류 코드 반환
if (deletePage(page) == E_OK) {
    if (registry.deleteReference(page.name) == E_OK) {
        if (configKeys.deleteKey(page.name.makeKey()) == E_OK) {
            logger.log("page deleted");
        } else {
            logger.log("configKey not deleted");
        }
    } else {
        logger.log("deleteReference from registry failed");
    }
} else {
    logger.log("delete failed");
    return E_ERROR;
}

// Good: 예외 사용
try {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
} catch (Exception e) {
    logger.log(e.getMessage());
}
```

### Try/Catch 블록 뽑아내기
try/catch 블록은 코드 구조에 혼란을 일으키며, 정상 동작과 오류 처리 동작을 뒤섞습니다. 그러므로 try/catch 블록을 별도 함수로 뽑아내는 편이 좋습니다.

```java
// Good: 오류 처리도 한 가지 작업이다
public void delete(Page page) {
    try {
        deletePageAndAllReferences(page);
    } catch (Exception e) {
        logError(e);
    }
}

private void deletePageAndAllReferences(Page page) throws Exception {
    deletePage(page);
    registry.deleteReference(page.name);
    configKeys.deleteKey(page.name.makeKey());
}

private void logError(Exception e) {
    logger.log(e.getMessage());
}
```

## 반복하지 마라

중복은 소프트웨어에서 모든 악의 근원입니다. 많은 원칙과 기법이 중복을 없애거나 제어할 목적으로 나왔습니다.

- 관계형 데이터베이스의 정규화
- 객체지향 프로그래밍 (부모 클래스로 중복 제거)
- 구조적 프로그래밍, AOP, COP 모두 어떤 면에서 중복 제거 전략

## 구조적 프로그래밍

에츠허르 다익스트라(Edsger Dijkstra)의 구조적 프로그래밍 원칙에 따르면 모든 함수와 함수 내 모든 블록에 입구(entry)와 출구(exit)가 하나만 존재해야 합니다.

즉, 함수는 return 문이 하나여야 하며, 루프 안에서 break나 continue를 사용해선 안 되며, goto는 절대로 안 됩니다.

**함수가 작다면** 위 규칙은 별 이익을 제공하지 못합니다. 함수가 아주 클 때만 상당한 이익을 제공합니다. 함수를 작게 만든다면 때로는 return, break, continue를 여러 차례 사용해도 괜찮습니다.

## 강의 진행 방식
1. **도입 (10분)**: 복잡한 함수 경험 공유
2. **이론 (30분)**: 함수 작성 원칙들 설명
3. **실습 (35분)**: 긴 함수 리팩토링 실습
4. **코드 리뷰 (15분)**: 팀별 함수 개선 결과 발표

## 실습 과제
1. **함수 분해**: 제공된 긴 함수를 작은 함수들로 분해
2. **추상화 수준 정리**: 혼재된 추상화 수준을 가진 함수 개선
3. **함수 네이밍**: 의미있는 함수 이름으로 리팩토링

## 평가 기준
- 함수 분해 능력 (35%)
- 추상화 수준 이해도 (25%)
- 네이밍 품질 (20%)
- 부수 효과 제거 (20%)

## 함수 품질 체크리스트
- [ ] 함수가 20줄 이내인가?
- [ ] 함수가 한 가지 일만 하는가?
- [ ] 함수 내 추상화 수준이 일관된가?
- [ ] 함수 이름이 하는 일을 정확히 표현하는가?
- [ ] 인수 개수가 최소화되었는가?
- [ ] 부수 효과가 없는가?
- [ ] 명령과 조회가 분리되었는가?

## 언어별 함수 작성 팁
### Java
- 메서드 오버로딩을 활용한 인수 개수 조절
- Stream API를 활용한 함수형 프로그래밍
- Optional을 활용한 null 처리

### Python
- 데코레이터를 활용한 횡단 관심사 분리
- 타입 힌트를 활용한 함수 시그니처 명시
- `*args`, `**kwargs`의 적절한 사용

### JavaScript
- 화살표 함수와 고차 함수 활용
- 구조 분해 할당을 통한 매개변수 처리
- async/await를 통한 비동기 처리

## 실무 적용 팁
- **함수 추출 단축키**: IDE의 Extract Method 기능 적극 활용
- **코드 리뷰 포인트**: 함수 길이와 복잡도를 우선적으로 검토
- **테스트 작성**: 작은 함수일수록 테스트 작성이 쉬워짐
- **성능 고려**: 함수 분해와 성능 사이의 균형점 찾기

## 추가 자료
- Kent Beck의 "Implementation Patterns"
- Martin Fowler의 "Refactoring" - Extract Method 패턴
- 함수형 프로그래밍의 순수 함수 개념 