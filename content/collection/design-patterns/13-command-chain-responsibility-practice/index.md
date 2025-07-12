---
collection_order: 131
draft: true
title: "[Design Patterns] 커맨드와 책임 연쇄 패턴 실습 - 요청 캡슐화와 처리 체인"
description: "Command와 Chain of Responsibility 패턴을 통해 요청 캡슐화와 처리 체인을 실습합니다. GUI 액션 시스템, 로그 처리 체인, 게임 AI 명령 등을 구현하며 실행 취소, 매크로, 요청 라우팅 등의 고급 기능을 마스터하는 실무 설계 기법을 학습합니다."
date: 2024-12-13T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Behavioral Patterns
- Request Processing
- Practice
- Action Systems
tags:
- Command Pattern Practice
- Chain of Responsibility Practice
- Request Encapsulation
- Processing Chain
- GUI Actions
- Undo Redo
- Macro Commands
- Log Processing
- Game AI Commands
- Request Routing
- Behavioral Patterns
- Design Patterns
- GoF Patterns
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Software Architecture
- Action Framework
- 커맨드 패턴 실습
- 책임 연쇄 패턴 실습
- 요청 캡슐화
- 처리 체인
- GUI 액션
- 실행 취소 다시 실행
- 매크로 명령
- 로그 처리
- 게임 AI 명령
- 요청 라우팅
- 행동 패턴
- 디자인 패턴
- GoF 패턴
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 소프트웨어 아키텍처
- 액션 프레임워크
---

# Command & Chain of Responsibility 패턴 실습 - 요청 캡슐화와 처리 체인

## 🎯 **실습 목표**
- Command 패턴으로 Undo/Redo 시스템 구현
- Chain of Responsibility로 요청 처리 체인 구현
- 매크로 명령과 복합 명령 처리
- 웹 미들웨어 스타일 체인 구현

## 📋 **실습 1: 텍스트 에디터 Command 시스템**

### **요구사항**
실행 취소/재실행이 가능한 텍스트 에디터

### **💻 코드 템플릿**

```java
// TODO 1: Command 인터페이스 정의
public interface Command {
    void execute();
    void undo();
    boolean canExecute();
    String getDescription();
}

// TODO 2: Document 클래스 (Receiver)
public class Document {
    private StringBuilder content;
    private int cursorPosition;
    
    // TODO: 텍스트 조작 메서드들 구현
    public void insertText(String text, int position) {
        // TODO: 텍스트 삽입
    }
    
    public String deleteText(int start, int length) {
        // TODO: 텍스트 삭제 후 삭제된 텍스트 반환
        return "";
    }
}

// TODO 3: 구체적인 Command 구현
public class InsertTextCommand implements Command {
    private final Document document;
    private final String text;
    private final int position;
    
    // TODO: 실행과 취소 로직 구현
}

public class DeleteTextCommand implements Command {
    private final Document document;
    private final int start;
    private final int length;
    private String deletedText; // undo를 위해 저장
    
    // TODO: 삭제와 복원 로직 구현
}

// TODO 4: 매크로 명령 구현
public class MacroCommand implements Command {
    private final List<Command> commands;
    private final String description;
    
    // TODO: 여러 명령을 하나로 묶어서 실행/취소
}

// TODO 5: Command Manager (Invoker)
public class CommandManager {
    private final Stack<Command> undoStack;
    private final Stack<Command> redoStack;
    private final int maxHistorySize;
    
    public void executeCommand(Command command) {
        // TODO: 명령 실행 후 undo 스택에 추가
    }
    
    public void undo() {
        // TODO: 마지막 명령 취소
    }
    
    public void redo() {
        // TODO: 마지막으로 취소한 명령 재실행
    }
}
```

## 📋 **실습 2: 지원 요청 처리 체인**

### **요구사항**
다단계 고객 지원 시스템 (Level 1 → Level 2 → Level 3)

### **💻 코드 템플릿**

```java
// TODO 1: Handler 추상 클래스 정의
public abstract class SupportHandler {
    protected SupportHandler nextHandler;
    protected final String handlerName;
    protected final int maxHandleLevel;
    
    public SupportHandler setNext(SupportHandler handler) {
        this.nextHandler = handler;
        return handler;
    }
    
    public final void handleRequest(SupportRequest request) {
        // TODO: 처리 가능 여부 확인 후 처리 또는 다음 핸들러로 전달
    }
    
    protected abstract boolean canHandle(SupportRequest request);
    protected abstract void doHandle(SupportRequest request);
}

// TODO 2: 구체적인 Handler 구현
public class Level1SupportHandler extends SupportHandler {
    // TODO: 기본적인 문의 처리 (비밀번호 재설정, 계정 문의 등)
}

public class Level2TechnicalHandler extends SupportHandler {
    // TODO: 기술적 문제 처리 (API 오류, 연동 문제 등)
}

public class Level3SpecialistHandler extends SupportHandler {
    // TODO: 전문가 수준 문제 처리 (시스템 장애, 보안 문제 등)
}

// TODO 3: 요청 우선순위 기반 라우팅
public class PriorityBasedChain {
    private final Map<Priority, SupportHandler> handlers;
    
    // TODO: 우선순위에 따른 핸들러 직접 라우팅
}

// TODO 4: 요청 정보 클래스
public class SupportRequest {
    private final String id;
    private final String category;
    private final Priority priority;
    private final String description;
    private final LocalDateTime timestamp;
    
    // TODO: 요청 분류를 위한 메서드들
}
```

## 📋 **실습 3: HTTP 미들웨어 체인**

### **💻 코드 템플릿**

```java
// TODO 1: 미들웨어 인터페이스
public interface Middleware {
    void handle(HttpRequest request, HttpResponse response, MiddlewareChain chain);
}

// TODO 2: 미들웨어 체인
public class MiddlewareChain {
    private final List<Middleware> middlewares;
    private int currentIndex = 0;
    
    public void proceed(HttpRequest request, HttpResponse response) {
        // TODO: 다음 미들웨어 실행
    }
}

// TODO 3: 구체적인 미들웨어들
public class AuthenticationMiddleware implements Middleware {
    // TODO: 인증 확인
}

public class RateLimitMiddleware implements Middleware {
    // TODO: 요청 제한 확인
}

public class LoggingMiddleware implements Middleware {
    // TODO: 요청/응답 로깅
}

public class CompressionMiddleware implements Middleware {
    // TODO: 응답 압축
}

// TODO 4: Express.js 스타일 미들웨어 빌더
public class MiddlewareBuilder {
    private final List<Middleware> middlewares = new ArrayList<>();
    
    public MiddlewareBuilder use(Middleware middleware) {
        middlewares.add(middleware);
        return this;
    }
    
    public MiddlewareChain build() {
        return new MiddlewareChain(middlewares);
    }
}
```

## 📋 **실습 4: 이벤트 처리 Command 시스템**

### **💻 코드 템플릿**

```java
// TODO 1: 이벤트 기반 Command
public interface EventCommand {
    void execute(Event event);
    boolean canHandle(Event event);
    int getPriority();
}

// TODO 2: Command 스케줄러
public class CommandScheduler {
    private final PriorityQueue<ScheduledCommand> scheduledCommands;
    private final ExecutorService executor;
    
    // TODO: 지연 실행, 반복 실행, 조건부 실행 Command 지원
}

// TODO 3: 분산 Command 실행
public class DistributedCommandProcessor {
    // TODO: 여러 노드에 Command 분산 실행
}
```

## ✅ **체크리스트**

### **Command 패턴**
- [ ] 실행 취소/재실행 구현
- [ ] 매크로 명령 구현
- [ ] Command 큐잉 시스템
- [ ] 분산 명령 처리

### **Chain of Responsibility**
- [ ] 요청 처리 체인 구현
- [ ] 동적 체인 구성
- [ ] 우선순위 기반 라우팅
- [ ] 미들웨어 패턴 구현

### **패턴 조합**
- [ ] Command + Chain 결합 사용
- [ ] 에러 처리 메커니즘
- [ ] 성능 모니터링
- [ ] 로깅 및 디버깅 지원

## 🔍 **추가 도전**

1. **Command Sourcing**: 이벤트 소싱 패턴 구현
2. **Async Command**: 비동기 명령 처리
3. **Command Batching**: 명령 배치 처리
4. **Distributed Chain**: 분산 책임 체인

## 🚀 **실무 적용**

### **Command 패턴 활용**
- GUI 이벤트 처리
- 트랜잭션 관리
- 작업 큐 시스템
- 이벤트 소싱

### **Chain of Responsibility 활용**  
- 웹 프레임워크 미들웨어
- 예외 처리 체인
- 승인 워크플로우
- 로그 처리 파이프라인

---

💡 **핵심 포인트**: Command는 '무엇을 할 것인가'를 객체로 캡슐화하고, Chain of Responsibility는 '누가 할 것인가'를 유연하게 결정합니다. 두 패턴의 조합은 복잡한 요청 처리 시스템의 핵심입니다. 