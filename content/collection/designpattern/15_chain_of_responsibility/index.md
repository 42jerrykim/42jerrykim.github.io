---
collection_order: 15
title: "[Design Pattern] Chain of Responsibility - 책임 연쇄 패턴"
description: "Chain of Responsibility 패턴은 요청 처리 객체들을 체인으로 연결하여 책임을 분산합니다. 클라이언트와 처리 객체의 결합도를 낮추고 동적으로 처리자를 변경합니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design-Pattern
  - 디자인패턴
  - GoF
  - Software-Architecture
  - Implementation
  - Logging
  - 로깅
  - Authentication
  - 인증
  - Code-Quality
  - 코드품질
  - 소프트웨어아키텍처
  - OOP
  - 객체지향
  - Java
  - C++
  - Python
  - CSharp
  - Git
  - GitHub
  - 구현
  - Security
  - Process
---

책임 연쇄 패턴(Chain of Responsibility Pattern)은 요청을 처리할 수 있는 객체들을 체인 형태로 연결하여, 요청이 처리될 때까지 체인을 따라 전달하는 행위 디자인 패턴이다. 이 패턴을 사용하면 요청을 보내는 객체와 처리하는 객체 사이의 결합도를 낮추고, 동적으로 처리자를 추가하거나 변경할 수 있다.

## 개요

**책임 연쇄 패턴의 정의**

책임 연쇄 패턴은 여러 핸들러를 체인 형태로 연결하고, 요청이 체인을 따라 전달되면서 적절한 핸들러가 처리하도록 한다. 클라이언트는 어떤 핸들러가 요청을 처리할지 알 필요 없이, 체인의 첫 번째 핸들러에게만 요청을 보내면 된다.

**패턴의 필요성 및 사용 사례**

책임 연쇄 패턴은 다음과 같은 상황에서 유용하다:

- **미들웨어/필터**: 웹 요청 처리 파이프라인
- **이벤트 처리**: GUI 이벤트 버블링
- **로깅**: 다양한 로그 레벨 처리
- **인증/권한**: 다단계 인증 검사
- **유효성 검사**: 연속적인 데이터 검증
- **예외 처리**: 예외 처리 핸들러 체인

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 요청자와 처리자 분리 | 요청이 처리되지 않을 수 있음 |
| 처리자 추가/제거 용이 | 디버깅이 어려울 수 있음 |
| 단일 책임 원칙 준수 | 체인이 길면 성능 저하 |
| 처리 순서 유연하게 변경 | 요청 흐름 추적이 복잡 |

## 책임 연쇄 패턴의 구성 요소

```
Client
   │
   ▼
┌─────────────────────────────────────┐
│          <<interface>>              │
│            Handler                  │
├─────────────────────────────────────┤
│ + setNext(Handler): Handler         │
│ + handle(Request): Result           │
└─────────────────────────────────────┘
              △
              │
    ┌─────────┴─────────┐
    │                   │
┌──────────────┐  ┌──────────────┐
│  HandlerA    │  │  HandlerB    │
├──────────────┤  ├──────────────┤
│ - next       │→ │ - next       │→ ...
├──────────────┤  ├──────────────┤
│ + handle()   │  │ + handle()   │
└──────────────┘  └──────────────┘
```

**1. Handler (핸들러)**
- 요청을 처리하는 인터페이스 정의
- 다음 핸들러에 대한 참조 설정 메서드

**2. ConcreteHandler (구체적 핸들러)**
- 요청을 처리하거나 다음 핸들러로 전달
- 자신이 처리할 수 있는 요청만 처리

**3. Client (클라이언트)**
- 체인의 첫 핸들러에게 요청 전송

## 구현 예제

### Python 예제 - 기술 지원 요청 처리

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

class Priority(Enum):
    LOW = 1      # 일반 문의
    MEDIUM = 2   # 기술 지원
    HIGH = 3     # 긴급 장애
    CRITICAL = 4 # 보안 이슈

class SupportRequest:
    def __init__(self, title: str, priority: Priority, description: str):
        self.title = title
        self.priority = priority
        self.description = description

# Handler 추상 클래스
class SupportHandler(ABC):
    def __init__(self):
        self._next_handler: Optional[SupportHandler] = None
    
    def set_next(self, handler: 'SupportHandler') -> 'SupportHandler':
        self._next_handler = handler
        return handler
    
    def handle(self, request: SupportRequest) -> str:
        if self.can_handle(request):
            return self.process(request)
        elif self._next_handler:
            return self._next_handler.handle(request)
        else:
            return f"⚠ 요청을 처리할 수 있는 담당자가 없습니다: {request.title}"
    
    @abstractmethod
    def can_handle(self, request: SupportRequest) -> bool:
        pass
    
    @abstractmethod
    def process(self, request: SupportRequest) -> str:
        pass

# ConcreteHandler - 일반 상담원
class FrontDeskSupport(SupportHandler):
    def can_handle(self, request: SupportRequest) -> bool:
        return request.priority == Priority.LOW
    
    def process(self, request: SupportRequest) -> str:
        return f"📞 [일반 상담원] '{request.title}' 처리 완료 - FAQ 안내"

# ConcreteHandler - 기술 지원팀
class TechSupport(SupportHandler):
    def can_handle(self, request: SupportRequest) -> bool:
        return request.priority == Priority.MEDIUM
    
    def process(self, request: SupportRequest) -> str:
        return f"🔧 [기술 지원팀] '{request.title}' 처리 완료 - 원격 지원"

# ConcreteHandler - 시스템 엔지니어
class SystemEngineer(SupportHandler):
    def can_handle(self, request: SupportRequest) -> bool:
        return request.priority == Priority.HIGH
    
    def process(self, request: SupportRequest) -> str:
        return f"⚙️ [시스템 엔지니어] '{request.title}' 긴급 대응 완료"

# ConcreteHandler - 보안 전문가
class SecurityExpert(SupportHandler):
    def can_handle(self, request: SupportRequest) -> bool:
        return request.priority == Priority.CRITICAL
    
    def process(self, request: SupportRequest) -> str:
        return f"🔒 [보안 전문가] '{request.title}' 보안 조치 완료"

# 사용 예제
if __name__ == "__main__":
    # 체인 구성
    front_desk = FrontDeskSupport()
    tech_support = TechSupport()
    engineer = SystemEngineer()
    security = SecurityExpert()
    
    front_desk.set_next(tech_support).set_next(engineer).set_next(security)
    
    # 다양한 요청 처리
    requests = [
        SupportRequest("비밀번호 재설정 방법", Priority.LOW, "비밀번호 변경"),
        SupportRequest("프린터 연결 오류", Priority.MEDIUM, "네트워크 프린터"),
        SupportRequest("서버 다운", Priority.HIGH, "메인 서버 응답 없음"),
        SupportRequest("데이터 유출 의심", Priority.CRITICAL, "비정상 접근 감지"),
    ]
    
    print("=== 기술 지원 요청 처리 ===\n")
    for req in requests:
        result = front_desk.handle(req)
        print(f"{result}\n")
```

### Java 예제 - 미들웨어 체인

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

// 요청 객체
class HttpRequest {
    private String path;
    private String method;
    private String token;
    private String body;
    
    public HttpRequest(String path, String method, String token, String body) {
        this.path = path;
        this.method = method;
        this.token = token;
        this.body = body;
    }
    // getters...
    public String getPath() { return path; }
    public String getMethod() { return method; }
    public String getToken() { return token; }
    public String getBody() { return body; }
}

// Handler 인터페이스
interface Middleware {
    Middleware setNext(Middleware next);
    boolean handle(HttpRequest request);
}

// BaseHandler - 기본 구현
abstract class BaseMiddleware implements Middleware {
    protected Middleware next;
    
    @Override
    public Middleware setNext(Middleware next) {
        this.next = next;
        return next;
    }
    
    @Override
    public boolean handle(HttpRequest request) {
        if (next != null) {
            return next.handle(request);
        }
        return true; // 체인 끝까지 통과
    }
    
    protected abstract boolean process(HttpRequest request);
}

// ConcreteHandler - 로깅 미들웨어
class LoggingMiddleware extends BaseMiddleware {
    @Override
    public boolean handle(HttpRequest request) {
        process(request);
        return super.handle(request);
    }
    
    @Override
    protected boolean process(HttpRequest request) {
        System.out.println("📝 [LOG] " + request.getMethod() + " " + request.getPath());
        return true;
    }
}

// ConcreteHandler - 인증 미들웨어
class AuthMiddleware extends BaseMiddleware {
    @Override
    public boolean handle(HttpRequest request) {
        if (!process(request)) {
            System.out.println("🚫 인증 실패");
            return false;
        }
        return super.handle(request);
    }
    
    @Override
    protected boolean process(HttpRequest request) {
        String token = request.getToken();
        if (token == null || token.isEmpty()) {
            return false;
        }
        System.out.println("✅ [AUTH] 토큰 검증 통과");
        return true;
    }
}

// ConcreteHandler - Rate Limiting 미들웨어
class RateLimitMiddleware extends BaseMiddleware {
    private int requestCount = 0;
    private static final int MAX_REQUESTS = 5;
    
    @Override
    public boolean handle(HttpRequest request) {
        if (!process(request)) {
            System.out.println("🚫 요청 제한 초과");
            return false;
        }
        return super.handle(request);
    }
    
    @Override
    protected boolean process(HttpRequest request) {
        requestCount++;
        if (requestCount > MAX_REQUESTS) {
            return false;
        }
        System.out.println("✅ [RATE] 요청 허용 (" + requestCount + "/" + MAX_REQUESTS + ")");
        return true;
    }
}

// ConcreteHandler - 입력 검증 미들웨어
class ValidationMiddleware extends BaseMiddleware {
    @Override
    public boolean handle(HttpRequest request) {
        if (!process(request)) {
            System.out.println("🚫 입력 검증 실패");
            return false;
        }
        return super.handle(request);
    }
    
    @Override
    protected boolean process(HttpRequest request) {
        String body = request.getBody();
        if (body != null && body.contains("<script>")) {
            return false; // XSS 방지
        }
        System.out.println("✅ [VALID] 입력 검증 통과");
        return true;
    }
}

// 사용 예제
public class ChainDemo {
    public static void main(String[] args) {
        // 미들웨어 체인 구성
        Middleware chain = new LoggingMiddleware();
        chain.setNext(new AuthMiddleware())
             .setNext(new RateLimitMiddleware())
             .setNext(new ValidationMiddleware());
        
        System.out.println("=== 정상 요청 ===");
        HttpRequest validReq = new HttpRequest("/api/users", "GET", "valid-token", "{}");
        boolean result = chain.handle(validReq);
        System.out.println("결과: " + (result ? "성공" : "실패") + "\n");
        
        System.out.println("=== 인증 없는 요청 ===");
        HttpRequest noAuthReq = new HttpRequest("/api/users", "GET", "", "{}");
        result = chain.handle(noAuthReq);
        System.out.println("결과: " + (result ? "성공" : "실패") + "\n");
        
        System.out.println("=== XSS 공격 시도 ===");
        HttpRequest xssReq = new HttpRequest("/api/post", "POST", "valid-token", "<script>alert('XSS')</script>");
        result = chain.handle(xssReq);
        System.out.println("결과: " + (result ? "성공" : "실패"));
    }
}
```

### C# 예제 - 결제 검증 체인

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;

public class PaymentRequest
{
    public decimal Amount { get; set; }
    public string CardNumber { get; set; }
    public string CVV { get; set; }
    public decimal AccountBalance { get; set; }
    public bool IsFraudSuspect { get; set; }
}

// Handler 추상 클래스
public abstract class PaymentHandler
{
    protected PaymentHandler _next;
    
    public PaymentHandler SetNext(PaymentHandler handler)
    {
        _next = handler;
        return handler;
    }
    
    public virtual bool Handle(PaymentRequest request)
    {
        if (_next != null)
            return _next.Handle(request);
        return true;
    }
}

// ConcreteHandler - 카드 유효성 검사
public class CardValidationHandler : PaymentHandler
{
    public override bool Handle(PaymentRequest request)
    {
        if (string.IsNullOrEmpty(request.CardNumber) || request.CardNumber.Length != 16)
        {
            Console.WriteLine("❌ [카드검증] 유효하지 않은 카드번호");
            return false;
        }
        Console.WriteLine("✅ [카드검증] 카드번호 유효");
        return base.Handle(request);
    }
}

// ConcreteHandler - CVV 검증
public class CVVValidationHandler : PaymentHandler
{
    public override bool Handle(PaymentRequest request)
    {
        if (string.IsNullOrEmpty(request.CVV) || request.CVV.Length != 3)
        {
            Console.WriteLine("❌ [CVV검증] 유효하지 않은 CVV");
            return false;
        }
        Console.WriteLine("✅ [CVV검증] CVV 유효");
        return base.Handle(request);
    }
}

// ConcreteHandler - 잔액 확인
public class BalanceCheckHandler : PaymentHandler
{
    public override bool Handle(PaymentRequest request)
    {
        if (request.AccountBalance < request.Amount)
        {
            Console.WriteLine($"❌ [잔액확인] 잔액 부족 (잔액: {request.AccountBalance:C}, 요청: {request.Amount:C})");
            return false;
        }
        Console.WriteLine($"✅ [잔액확인] 잔액 충분 (잔액: {request.AccountBalance:C})");
        return base.Handle(request);
    }
}

// ConcreteHandler - 사기 탐지
public class FraudDetectionHandler : PaymentHandler
{
    public override bool Handle(PaymentRequest request)
    {
        if (request.IsFraudSuspect)
        {
            Console.WriteLine("❌ [사기탐지] 의심스러운 거래 감지");
            return false;
        }
        Console.WriteLine("✅ [사기탐지] 정상 거래");
        return base.Handle(request);
    }
}

// ConcreteHandler - 한도 확인
public class LimitCheckHandler : PaymentHandler
{
    private const decimal DailyLimit = 5000000m;
    
    public override bool Handle(PaymentRequest request)
    {
        if (request.Amount > DailyLimit)
        {
            Console.WriteLine($"❌ [한도확인] 일일 한도 초과 (한도: {DailyLimit:C})");
            return false;
        }
        Console.WriteLine($"✅ [한도확인] 한도 내 거래");
        return base.Handle(request);
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        // 결제 검증 체인 구성
        var handler = new CardValidationHandler();
        handler.SetNext(new CVVValidationHandler())
               .SetNext(new BalanceCheckHandler())
               .SetNext(new FraudDetectionHandler())
               .SetNext(new LimitCheckHandler());
        
        Console.WriteLine("=== 정상 결제 요청 ===");
        var validRequest = new PaymentRequest
        {
            CardNumber = "1234567890123456",
            CVV = "123",
            Amount = 50000,
            AccountBalance = 100000,
            IsFraudSuspect = false
        };
        bool result = handler.Handle(validRequest);
        Console.WriteLine($"결과: {(result ? "결제 승인" : "결제 거부")}\n");
        
        Console.WriteLine("=== 잔액 부족 요청 ===");
        var insufficientRequest = new PaymentRequest
        {
            CardNumber = "1234567890123456",
            CVV = "123",
            Amount = 150000,
            AccountBalance = 100000,
            IsFraudSuspect = false
        };
        result = handler.Handle(insufficientRequest);
        Console.WriteLine($"결과: {(result ? "결제 승인" : "결제 거부")}\n");
        
        Console.WriteLine("=== 사기 의심 거래 ===");
        var fraudRequest = new PaymentRequest
        {
            CardNumber = "1234567890123456",
            CVV = "123",
            Amount = 50000,
            AccountBalance = 100000,
            IsFraudSuspect = true
        };
        result = handler.Handle(fraudRequest);
        Console.WriteLine($"결과: {(result ? "결제 승인" : "결제 거부")}");
    }
}
```

## 실제 사용 사례

### 1. Java Servlet Filter
```java
filterChain.doFilter(request, response);
```

### 2. Express.js Middleware
```javascript
app.use(logger);
app.use(authenticate);
app.use(router);
```

### 3. DOM Event Bubbling
이벤트가 자식에서 부모 요소로 전파

### 4. ASP.NET Core Middleware
```csharp
app.UseAuthentication();
app.UseAuthorization();
app.UseEndpoints(...);
```

## 관련 패턴

| 패턴 | 책임 연쇄와의 관계 |
|------|------------------|
| **Composite** | 부모 컴포넌트를 핸들러로 사용 가능 |
| **Command** | 요청을 Command 객체로 캡슐화 가능 |
| **Decorator** | 둘 다 체인 구조이지만 목적이 다름 |

## FAQ

**Q1: 요청이 처리되지 않으면 어떻게 하나요?**

체인 끝에 기본 핸들러를 두거나, 처리되지 않은 요청에 대해 예외를 발생시킵니다.

**Q2: 모든 핸들러가 요청을 처리해야 하나요?**

아닙니다. 필터 체인처럼 모든 핸들러가 처리하는 방식과, 하나만 처리하고 중단하는 방식 모두 가능합니다.

**Q3: 체인의 순서가 중요한가요?**

네, 순서에 따라 결과가 달라질 수 있습니다. 예를 들어 인증은 로깅보다 먼저 수행되어야 할 수 있습니다.

## 참고 자료

- GoF의 "Design Patterns"
- Servlet Filter 문서
- Express.js Middleware 가이드