---
draft: true
collection_order: 150
title: "[Design Patterns] 인터프리터와 미디에이터: 파싱과 조정의 패턴"
description: "언어를 객체로 구현하는 Interpreter 패턴과 복잡한 상호작용을 중재하는 Mediator 패턴을 심도 있게 분석합니다. 문법 해석 엔진, 비즈니스 규칙 엔진, 객체 간 통신 조정, UI 컴포넌트 상호작용 등 복잡한 로직과 관계를 체계적으로 관리하는 전문가 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-15T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Behavioral Patterns
- Language Processing
- Communication Patterns
tags:
- Design-Pattern
- GoF
- Software-Architecture
- 디자인패턴
---

Interpreter와 Mediator 패턴을 통해 언어 처리와 객체 관계 관리를 탐구합니다. DSL 구현과 복잡한 상호작용의 중앙 집중화 방법을 학습합니다.

## 서론: 언어의 구현과 관계의 중재

> *"좋은 소프트웨어는 복잡한 것을 단순하게 표현한다. Interpreter는 언어를 통해, Mediator는 중재를 통해 이를 실현한다."*

현대 소프트웨어 개발에서 우리는 두 가지 근본적인 도전에 직면합니다:

1. **복잡한 규칙과 논리를 어떻게 표현하고 실행할 것인가?** (언어 처리)
2. **수많은 객체들의 복잡한 상호작용을 어떻게 관리할 것인가?** (관계 관리)

**Interpreter 패턴**은 **"언어를 객체로 만들어 실행 가능하게"** 합니다. 문법 규칙을 클래스로 표현하고, 문장을 객체 트리로 변환하여 해석하고 실행합니다.

**Mediator 패턴**은 **"복잡한 관계를 중재자로 단순화"** 합니다. 여러 객체 간의 상호작용을 중앙의 중재자가 관리하여 결합도를 낮춥니다.

이 두 패턴은 **"복잡성의 구조화"**라는 공통 목표를 가집니다:
- Interpreter: **문법적 복잡성**의 구조화
- Mediator: **관계적 복잡성**의 구조화

## Interpreter 패턴 - 언어의 객체화

### Interpreter 패턴의 핵심 철학

Interpreter 패턴은 **"문법을 클래스로, 문장을 객체 트리로"** 변환하는 것입니다. 이를 통해 언어의 실행 엔진을 객체지향적으로 구현할 수 있습니다.

```java
// Interpreter 패턴 없이 구현한다면?
class BadRuleEngine {
    public boolean evaluate(String expression, Map<String, Boolean> variables) {
        // 😱 복잡한 파싱과 평가 로직이 한 곳에 집중
        if (expression.contains("AND")) {
            String[] parts = expression.split("AND");
            return evaluate(parts[0].trim(), variables) && 
                   evaluate(parts[1].trim(), variables);
        } else if (expression.contains("OR")) {
            String[] parts = expression.split("OR");
            return evaluate(parts[0].trim(), variables) || 
                   evaluate(parts[1].trim(), variables);
        } else {
            return variables.getOrDefault(expression.trim(), false);
        }
        // 😱 새로운 연산자 추가 시 전체 메서드 수정
        // 😱 우선순위, 괄호 처리 등이 매우 복잡
        // 😱 에러 처리와 디버깅이 어려움
    }
}
```

### Interpreter 패턴으로 우아하게 해결

```java
// Interpreter 패턴의 우아함
// 1. 추상 표현식 인터페이스
interface Expression {
    boolean interpret(Context context);
    String toString(); // 디버깅을 위한 문자열 표현
}

// 2. 컨텍스트 - 해석에 필요한 정보 저장
class Context {
    private final Map<String, Boolean> variables;
    private final Map<String, Expression> functions;
    private final Stack<String> callStack; // 디버깅용
    
    public Context() {
        this.variables = new HashMap<>();
        this.functions = new HashMap<>();
        this.callStack = new Stack<>();
    }
    
    public boolean getVariable(String name) {
        if (!variables.containsKey(name)) {
            throw new RuntimeException("Undefined variable: " + name);
        }
        return variables.get(name);
    }
    
    public void setVariable(String name, boolean value) {
        variables.put(name, value);
    }
    
    public void defineFunction(String name, Expression expression) {
        functions.put(name, expression);
    }
    
    public Expression getFunction(String name) {
        return functions.get(name);
    }
    
    public void pushCall(String name) {
        callStack.push(name);
    }
    
    public void popCall() {
        if (!callStack.isEmpty()) {
            callStack.pop();
        }
    }
    
    public List<String> getCallStack() {
        return new ArrayList<>(callStack);
    }
}

// 3. 단말 표현식 (Terminal Expressions)
class VariableExpression implements Expression {
    private final String variableName;
    
    public VariableExpression(String variableName) {
        this.variableName = variableName;
    }
    
    @Override
    public boolean interpret(Context context) {
        return context.getVariable(variableName);
    }
    
    @Override
    public String toString() {
        return variableName;
    }
}

class ConstantExpression implements Expression {
    private final boolean value;
    
    public ConstantExpression(boolean value) {
        this.value = value;
    }
    
    @Override
    public boolean interpret(Context context) {
        return value;
    }
    
    @Override
    public String toString() {
        return Boolean.toString(value);
    }
}

// 4. 비단말 표현식 (Non-Terminal Expressions)
class AndExpression implements Expression {
    private final Expression left;
    private final Expression right;
    
    public AndExpression(Expression left, Expression right) {
        this.left = left;
        this.right = right;
    }
    
    @Override
    public boolean interpret(Context context) {
        // 단락 평가 (Short-circuit evaluation)
        boolean leftResult = left.interpret(context);
        if (!leftResult) {
            return false; // 왼쪽이 false면 오른쪽은 평가하지 않음
        }
        return right.interpret(context);
    }
    
    @Override
    public String toString() {
        return "(" + left.toString() + " AND " + right.toString() + ")";
    }
}

class OrExpression implements Expression {
    private final Expression left;
    private final Expression right;
    
    public OrExpression(Expression left, Expression right) {
        this.left = left;
        this.right = right;
    }
    
    @Override
    public boolean interpret(Context context) {
        // 단락 평가
        boolean leftResult = left.interpret(context);
        if (leftResult) {
            return true; // 왼쪽이 true면 오른쪽은 평가하지 않음
        }
        return right.interpret(context);
    }
    
    @Override
    public String toString() {
        return "(" + left.toString() + " OR " + right.toString() + ")";
    }
}

class NotExpression implements Expression {
    private final Expression expression;
    
    public NotExpression(Expression expression) {
        this.expression = expression;
    }
    
    @Override
    public boolean interpret(Context context) {
        return !expression.interpret(context);
    }
    
    @Override
    public String toString() {
        return "NOT(" + expression.toString() + ")";
    }
}

// 5. 함수 호출 표현식
class FunctionExpression implements Expression {
    private final String functionName;
    
    public FunctionExpression(String functionName) {
        this.functionName = functionName;
    }
    
    @Override
    public boolean interpret(Context context) {
        Expression function = context.getFunction(functionName);
        if (function == null) {
            throw new RuntimeException("Undefined function: " + functionName);
        }
        
        context.pushCall(functionName);
        try {
            return function.interpret(context);
        } finally {
            context.popCall();
        }
    }
    
    @Override
    public String toString() {
        return functionName + "()";
    }
}

// 6. 파서 - 문자열을 Expression 트리로 변환
class BooleanExpressionParser {
    private final String input;
    private int position;
    
    public BooleanExpressionParser(String input) {
        this.input = input.replaceAll("\\s+", ""); // 공백 제거
        this.position = 0;
    }
    
    public Expression parse() {
        Expression result = parseOr();
        if (position < input.length()) {
            throw new RuntimeException("Unexpected character at position " + position);
        }
        return result;
    }
    
    private Expression parseOr() {
        Expression left = parseAnd();
        
        while (position < input.length() && peek("OR")) {
            consume("OR");
            Expression right = parseAnd();
            left = new OrExpression(left, right);
        }
        
        return left;
    }
    
    private Expression parseAnd() {
        Expression left = parseNot();
        
        while (position < input.length() && peek("AND")) {
            consume("AND");
            Expression right = parseNot();
            left = new AndExpression(left, right);
        }
        
        return left;
    }
    
    private Expression parseNot() {
        if (peek("NOT")) {
            consume("NOT");
            return new NotExpression(parseAtom());
        }
        return parseAtom();
    }
    
    private Expression parseAtom() {
        if (peek("(")) {
            consume("(");
            Expression expr = parseOr();
            consume(")");
            return expr;
        }
        
        if (peek("true")) {
            consume("true");
            return new ConstantExpression(true);
        }
        
        if (peek("false")) {
            consume("false");
            return new ConstantExpression(false);
        }
        
        // 변수나 함수 파싱
        String identifier = parseIdentifier();
        if (peek("(")) {
            consume("(");
            consume(")");
            return new FunctionExpression(identifier);
        }
        
        return new VariableExpression(identifier);
    }
    
    private String parseIdentifier() {
        StringBuilder sb = new StringBuilder();
        while (position < input.length() && Character.isLetterOrDigit(input.charAt(position))) {
            sb.append(input.charAt(position++));
        }
        
        if (sb.length() == 0) {
            throw new RuntimeException("Expected identifier at position " + position);
        }
        
        return sb.toString();
    }
    
    private boolean peek(String token) {
        return input.substring(position).startsWith(token);
    }
    
    private void consume(String token) {
        if (!peek(token)) {
            throw new RuntimeException("Expected '" + token + "' at position " + position);
        }
        position += token.length();
    }
}

// 7. 비즈니스 규칙 엔진
class BusinessRuleEngine {
    private final Map<String, Expression> rules;
    private final Context context;
    
    public BusinessRuleEngine() {
        this.rules = new HashMap<>();
        this.context = new Context();
    }
    
    public void addRule(String name, String ruleExpression) {
        BooleanExpressionParser parser = new BooleanExpressionParser(ruleExpression);
        Expression expression = parser.parse();
        rules.put(name, expression);
        System.out.println("Added rule '" + name + "': " + expression);
    }
    
    public void setVariable(String name, boolean value) {
        context.setVariable(name, value);
    }
    
    public boolean evaluateRule(String ruleName) {
        Expression rule = rules.get(ruleName);
        if (rule == null) {
            throw new RuntimeException("Rule not found: " + ruleName);
        }
        
        try {
            boolean result = rule.interpret(context);
            System.out.println("Rule '" + ruleName + "' evaluated to: " + result);
            return result;
        } catch (Exception e) {
            System.err.println("Error evaluating rule '" + ruleName + "': " + e.getMessage());
            System.err.println("Call stack: " + context.getCallStack());
            throw e;
        }
    }
    
    public Map<String, Boolean> evaluateAllRules() {
        Map<String, Boolean> results = new HashMap<>();
        for (String ruleName : rules.keySet()) {
            try {
                results.put(ruleName, evaluateRule(ruleName));
            } catch (Exception e) {
                results.put(ruleName, false); // 에러 시 false로 처리
            }
        }
        return results;
    }
    
    public void printRules() {
        System.out.println("=== Business Rules ===");
        for (Map.Entry<String, Expression> entry : rules.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
}

// 사용 예시
class InterpreterPatternDemo {
    public static void main(String[] args) {
        BusinessRuleEngine engine = new BusinessRuleEngine();
        
        // 비즈니스 규칙 정의
        engine.addRule("basic_discount", "isVip OR (age >= 65 AND isLoyalCustomer)");
        engine.addRule("free_shipping", "orderValue >= 50 OR isPremiumMember");
        engine.addRule("special_offer", "isNewCustomer AND NOT hasUsedPromo");
        
        // 고객 정보 설정
        engine.setVariable("isVip", false);
        engine.setVariable("age", 70);
        engine.setVariable("isLoyalCustomer", true);
        engine.setVariable("orderValue", 30);
        engine.setVariable("isPremiumMember", false);
        engine.setVariable("isNewCustomer", true);
        engine.setVariable("hasUsedPromo", false);
        
        // 규칙 평가
        System.out.println("\n=== Rule Evaluation ===");
        Map<String, Boolean> results = engine.evaluateAllRules();
        
        // 결과 출력
        System.out.println("\n=== Results ===");
        results.forEach((rule, result) -> 
            System.out.printf("%s: %s\n", rule, result ? "[APPLY]" : "[NO]")
        );
    }
}
```

### 고급 Interpreter - 수식 계산기

```java
// 수식 계산을 위한 Interpreter 구현
interface MathExpression {
    double evaluate();
    String toString();
}

class NumberExpression implements MathExpression {
    private final double value;
    
    public NumberExpression(double value) {
        this.value = value;
    }
    
    @Override
    public double evaluate() {
        return value;
    }
    
    @Override
    public String toString() {
        return String.valueOf(value);
    }
}

class AddExpression implements MathExpression {
    private final MathExpression left, right;
    
    public AddExpression(MathExpression left, MathExpression right) {
        this.left = left;
        this.right = right;
    }
    
    @Override
    public double evaluate() {
        return left.evaluate() + right.evaluate();
    }
    
    @Override
    public String toString() {
        return "(" + left + " + " + right + ")";
    }
}

class MultiplyExpression implements MathExpression {
    private final MathExpression left, right;
    
    public MultiplyExpression(MathExpression left, MathExpression right) {
        this.left = left;
        this.right = right;
    }
    
    @Override
    public double evaluate() {
        return left.evaluate() * right.evaluate();
    }
    
    @Override
    public String toString() {
        return "(" + left + " * " + right + ")";
    }
}

// 사용 예시: (5 + 3) * 2
class MathDemo {
    public static void main(String[] args) {
        MathExpression expr = new MultiplyExpression(
            new AddExpression(
                new NumberExpression(5),
                new NumberExpression(3)
            ),
            new NumberExpression(2)
        );
        
        System.out.println("Expression: " + expr);
        System.out.println("Result: " + expr.evaluate()); // 16.0
    }
}
```

## Mediator 패턴 - 관계의 중재

### Mediator 패턴의 핵심 철학

Mediator 패턴은 **"많은 객체 간의 복잡한 상호작용을 중재자가 관리"**하여 객체들이 서로를 직접 참조하지 않도록 합니다.

```java
// Mediator 패턴 없이 구현한다면?
class BadChatSystem {
    class BadUser {
        private String name;
        private List<BadUser> contacts = new ArrayList<>();
        
        public void addContact(BadUser user) {
            contacts.add(user);
            user.contacts.add(this); // 😱 양방향 결합
        }
        
        public void sendMessage(String message, BadUser recipient) {
            // 😱 사용자가 직접 다른 사용자에게 메시지 전송
            recipient.receiveMessage(message, this);
        }
        
        public void broadcastMessage(String message) {
            // 😱 모든 연락처를 직접 관리
            for (BadUser contact : contacts) {
                contact.receiveMessage(message, this);
            }
        }
        
        // 😱 새로운 기능 추가 시 모든 User 클래스 수정 필요
        // 😱 그룹 채팅, 메시지 필터링 등을 추가하기 어려움
    }
}
```

### Mediator 패턴으로 우아하게 해결

```java
// Mediator 패턴의 우아함
// 1. Mediator 인터페이스
interface ChatMediator {
    void sendMessage(Message message, User sender);
    void addUser(User user);
    void removeUser(User user);
    void createGroup(String groupName, List<User> members);
    void sendGroupMessage(String groupName, Message message, User sender);
}

// 2. Message 클래스
class Message {
    private final String content;
    private final MessageType type;
    private final LocalDateTime timestamp;
    private final String messageId;
    
    public Message(String content, MessageType type) {
        this.content = content;
        this.type = type;
        this.timestamp = LocalDateTime.now();
        this.messageId = UUID.randomUUID().toString();
    }
    
    // getters
    public String getContent() { return content; }
    public MessageType getType() { return type; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getMessageId() { return messageId; }
}

enum MessageType {
    TEXT, IMAGE, FILE, SYSTEM_NOTIFICATION
}

// 3. 구체적인 Mediator 구현
class AdvancedChatRoom implements ChatMediator {
    private final List<User> users;
    private final Map<String, List<User>> groups;
    private final List<MessageFilter> filters;
    private final MessageLogger logger;
    
    public AdvancedChatRoom() {
        this.users = new ArrayList<>();
        this.groups = new HashMap<>();
        this.filters = new ArrayList<>();
        this.logger = new MessageLogger();
    }
    
    @Override
    public void addUser(User user) {
        users.add(user);
        user.setMediator(this);
        
        // 시스템 알림
        Message welcomeMessage = new Message(
            user.getName() + " joined the chat", 
            MessageType.SYSTEM_NOTIFICATION
        );
        broadcastSystemMessage(welcomeMessage, user);
        
        System.out.println("👋 " + user.getName() + " joined the chat room");
    }
    
    @Override
    public void removeUser(User user) {
        users.remove(user);
        
        // 모든 그룹에서 제거
        groups.values().forEach(group -> group.remove(user));
        
        Message leaveMessage = new Message(
            user.getName() + " left the chat", 
            MessageType.SYSTEM_NOTIFICATION
        );
        broadcastSystemMessage(leaveMessage, user);
        
        System.out.println("👋 " + user.getName() + " left the chat room");
    }
    
    @Override
    public void sendMessage(Message message, User sender) {
        // 메시지 필터링
        if (!applyFilters(message, sender)) {
            System.out.println("🚫 Message blocked by filter");
            return;
        }
        
        // 로깅
        logger.logMessage(message, sender, users);
        
        // 모든 사용자에게 전송 (발신자 제외)
        for (User user : users) {
            if (user != sender) {
                user.receive(message, sender.getName());
            }
        }
    }
    
    @Override
    public void createGroup(String groupName, List<User> members) {
        // 유효한 사용자들만 필터링
        List<User> validMembers = members.stream()
            .filter(users::contains)
            .collect(Collectors.toList());
        
        groups.put(groupName, new ArrayList<>(validMembers));
        
        Message groupCreatedMessage = new Message(
            "Group '" + groupName + "' created with " + validMembers.size() + " members",
            MessageType.SYSTEM_NOTIFICATION
        );
        
        // 그룹 멤버들에게만 알림
        for (User member : validMembers) {
            member.receive(groupCreatedMessage, "System");
        }
        
        System.out.println("👥 Group '" + groupName + "' created");
    }
    
    @Override
    public void sendGroupMessage(String groupName, Message message, User sender) {
        List<User> groupMembers = groups.get(groupName);
        if (groupMembers == null) {
            sender.receive(
                new Message("Group '" + groupName + "' not found", MessageType.SYSTEM_NOTIFICATION), 
                "System"
            );
            return;
        }
        
        if (!groupMembers.contains(sender)) {
            sender.receive(
                new Message("You are not a member of group '" + groupName + "'", MessageType.SYSTEM_NOTIFICATION), 
                "System"
            );
            return;
        }
        
        // 메시지 필터링
        if (!applyFilters(message, sender)) {
            return;
        }
        
        // 로깅
        logger.logGroupMessage(message, sender, groupName, groupMembers);
        
        // 그룹 멤버들에게 전송 (발신자 제외)
        for (User member : groupMembers) {
            if (member != sender) {
                member.receiveGroupMessage(message, sender.getName(), groupName);
            }
        }
    }
    
    public void addMessageFilter(MessageFilter filter) {
        filters.add(filter);
    }
    
    private boolean applyFilters(Message message, User sender) {
        for (MessageFilter filter : filters) {
            if (!filter.isAllowed(message, sender)) {
                return false;
            }
        }
        return true;
    }
    
    private void broadcastSystemMessage(Message message, User excludeUser) {
        for (User user : users) {
            if (user != excludeUser) {
                user.receive(message, "System");
            }
        }
    }
    
    public void printStatistics() {
        System.out.println("=== Chat Room Statistics ===");
        System.out.println("Total users: " + users.size());
        System.out.println("Total groups: " + groups.size());
        System.out.println("Total messages: " + logger.getTotalMessages());
    }
}

// 4. User 추상 클래스
abstract class User {
    protected ChatMediator mediator;
    protected final String name;
    protected final UserType userType;
    
    public User(String name, UserType userType) {
        this.name = name;
        this.userType = userType;
    }
    
    public void setMediator(ChatMediator mediator) {
        this.mediator = mediator;
    }
    
    public abstract void send(String messageContent);
    public abstract void receive(Message message, String senderName);
    public abstract void receiveGroupMessage(Message message, String senderName, String groupName);
    
    public String getName() { return name; }
    public UserType getUserType() { return userType; }
}

enum UserType {
    REGULAR, MODERATOR, ADMIN
}

// 5. 구체적인 User 구현
class RegularUser extends User {
    public RegularUser(String name) {
        super(name, UserType.REGULAR);
    }
    
    @Override
    public void send(String messageContent) {
        if (mediator != null) {
            Message message = new Message(messageContent, MessageType.TEXT);
            mediator.sendMessage(message, this);
        }
    }
    
    public void sendToGroup(String groupName, String messageContent) {
        if (mediator != null) {
            Message message = new Message(messageContent, MessageType.TEXT);
            mediator.sendGroupMessage(groupName, message, this);
        }
    }
    
    @Override
    public void receive(Message message, String senderName) {
        System.out.printf("📱 [%s] %s: %s\n", 
                         name, senderName, message.getContent());
    }
    
    @Override
    public void receiveGroupMessage(Message message, String senderName, String groupName) {
        System.out.printf("👥 [%s] %s@%s: %s\n", 
                         name, senderName, groupName, message.getContent());
    }
}

class ModeratorUser extends RegularUser {
    public ModeratorUser(String name) {
        super(name);
    }
    
    public void kickUser(User user) {
        if (mediator != null) {
            mediator.removeUser(user);
            System.out.println("🔨 " + name + " kicked " + user.getName());
        }
    }
    
    @Override
    public void receive(Message message, String senderName) {
        System.out.printf("🛡️ [%s] %s: %s\n", 
                         name, senderName, message.getContent());
    }
}

// 6. 메시지 필터
interface MessageFilter {
    boolean isAllowed(Message message, User sender);
}

class ProfanityFilter implements MessageFilter {
    private final Set<String> bannedWords = Set.of("spam", "bad", "inappropriate");
    
    @Override
    public boolean isAllowed(Message message, User sender) {
        String content = message.getContent().toLowerCase();
        for (String bannedWord : bannedWords) {
            if (content.contains(bannedWord)) {
                System.out.println("🚫 Message from " + sender.getName() + " blocked: contains '" + bannedWord + "'");
                return false;
            }
        }
        return true;
    }
}

class RateLimitFilter implements MessageFilter {
    private final Map<User, List<LocalDateTime>> userMessageTimes = new HashMap<>();
    private final int maxMessagesPerMinute = 10;
    
    @Override
    public boolean isAllowed(Message message, User sender) {
        LocalDateTime now = LocalDateTime.now();
        List<LocalDateTime> messageTimes = userMessageTimes.computeIfAbsent(sender, k -> new ArrayList<>());
        
        // 1분 이전 메시지들 제거
        messageTimes.removeIf(time -> time.isBefore(now.minusMinutes(1)));
        
        if (messageTimes.size() >= maxMessagesPerMinute) {
            System.out.println("🚫 Rate limit exceeded for " + sender.getName());
            return false;
        }
        
        messageTimes.add(now);
        return true;
    }
}

// 7. 메시지 로거
class MessageLogger {
    private int totalMessages = 0;
    private final Map<String, Integer> userMessageCounts = new HashMap<>();
    
    public void logMessage(Message message, User sender, List<User> recipients) {
        totalMessages++;
        userMessageCounts.merge(sender.getName(), 1, Integer::sum);
        
        System.out.printf("📝 LOG: %s sent message to %d users at %s\n",
                         sender.getName(), recipients.size() - 1, message.getTimestamp());
    }
    
    public void logGroupMessage(Message message, User sender, String groupName, List<User> members) {
        totalMessages++;
        userMessageCounts.merge(sender.getName(), 1, Integer::sum);
        
        System.out.printf("📝 LOG: %s sent group message to %s (%d members) at %s\n",
                         sender.getName(), groupName, members.size() - 1, message.getTimestamp());
    }
    
    public int getTotalMessages() {
        return totalMessages;
    }
    
    public Map<String, Integer> getUserMessageCounts() {
        return new HashMap<>(userMessageCounts);
    }
}

// 사용 예시
class MediatorPatternDemo {
    public static void main(String[] args) {
        // 채팅방 생성
        AdvancedChatRoom chatRoom = new AdvancedChatRoom();
        
        // 필터 추가
        chatRoom.addMessageFilter(new ProfanityFilter());
        chatRoom.addMessageFilter(new RateLimitFilter());
        
        // 사용자 생성 및 추가
        User alice = new RegularUser("Alice");
        User bob = new RegularUser("Bob");
        User charlie = new RegularUser("Charlie");
        User moderator = new ModeratorUser("ModeratorDave");
        
        chatRoom.addUser(alice);
        chatRoom.addUser(bob);
        chatRoom.addUser(charlie);
        chatRoom.addUser(moderator);
        
        System.out.println("\n=== General Chat ===");
        
        // 일반 채팅
        alice.send("Hello everyone!");
        bob.send("Hi Alice!");
        charlie.send("Good morning!");
        
        System.out.println("\n=== Group Creation ===");
        
        // 그룹 생성
        chatRoom.createGroup("developers", Arrays.asList(alice, bob, charlie));
        
        System.out.println("\n=== Group Chat ===");
        
        // 그룹 채팅
        ((RegularUser) alice).sendToGroup("developers", "Let's discuss the new project");
        ((RegularUser) bob).sendToGroup("developers", "Great idea!");
        
        System.out.println("\n=== Filter Testing ===");
        
        // 필터 테스트
        alice.send("This message contains spam keyword");
        
        System.out.println("\n=== Statistics ===");
        
        // 통계 출력
        chatRoom.printStatistics();
    }
}
```

## Interpreter와 Mediator의 현대적 활용

### Spring Framework에서의 활용

```java
// Spring에서 Mediator 패턴 활용
@Component
public class ApplicationEventPublisher {
    // Spring의 ApplicationContext가 Mediator 역할
    
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // 주문 생성 이벤트 처리
    }
    
    @EventListener  
    public void handleUserRegistered(UserRegisteredEvent event) {
        // 사용자 등록 이벤트 처리
    }
}

// Spring Expression Language (SpEL) - Interpreter 패턴
@Value("#{systemProperties['user.name']}")
private String userName;

@PreAuthorize("hasRole('ADMIN') and #order.amount > 1000")
public void processOrder(Order order) {
    // SpEL이 Interpreter 패턴으로 표현식 해석
}
```

### 현대적 DSL 설계

```java
// Fluent Interface를 활용한 내부 DSL
class QueryBuilder {
    public static Query select(String... columns) {
        return new Query().select(columns);
    }
}

// 사용 예시 - SQL과 유사한 DSL
Query query = select("name", "email")
    .from("users")
    .where("age").greaterThan(18)
    .and("status").equals("active")
    .orderBy("name")
    .limit(10);
```

## 한눈에 보는 Interpreter & Mediator 패턴

### Interpreter vs Mediator 핵심 비교

| 비교 항목 | Interpreter 패턴 | Mediator 패턴 |
|----------|-----------------|--------------|
| **핵심 목적** | 언어/문법 해석 | 객체 간 상호작용 조정 |
| **해결 문제** | 문법 파싱, DSL 처리 | 복잡한 객체 간 의존성 |
| **구조** | 문법 규칙별 클래스 계층 | 중재자 + Colleague 구조 |
| **확장 방식** | 새 표현식 클래스 추가 | 중재자 로직 수정 |
| **복잡도 위치** | 분산 (각 표현식 클래스) | 집중 (Mediator) |
| **사용 빈도** | 드묾 (특수 목적) | 중간 (GUI, 시스템 통합) |

### Interpreter 패턴 구성 요소

| 구성 요소 | 역할 | 예시 |
|----------|------|------|
| AbstractExpression | 해석 인터페이스 정의 | `interpret(Context)` |
| TerminalExpression | 종단 기호 해석 | 숫자, 변수, 리터럴 |
| NonterminalExpression | 비종단 기호 해석 | 연산자, 조합 규칙 |
| Context | 전역 정보 저장 | 변수 값, 해석 상태 |
| Client | 구문 트리 구성 | 파서 역할 |

### Mediator 패턴 통신 비교

| 비교 항목 | 직접 통신 | Mediator 통신 |
|----------|----------|--------------|
| 결합도 | O(n²) 연결 | O(n) 연결 |
| 의존성 | Colleague 서로 의존 | Mediator만 의존 |
| 확장성 | 새 Colleague 추가 어려움 | Mediator만 수정 |
| 복잡성 | 분산 (각 객체에) | 집중 (Mediator에) |

### 적용 시나리오 비교

| 시나리오 | Interpreter | Mediator |
|----------|-------------|----------|
| 수식 계산기 | O | X |
| SQL 파서 | O | X |
| 정규표현식 엔진 | O | X |
| 채팅방 | X | O |
| GUI 폼 컴포넌트 연동 | X | O |
| 항공 관제 시스템 | X | O |
| DSL 구현 | O | X |

### 현대적 대안 비교

| 패턴 | 전통적 구현 | 현대적 대안 |
|------|-----------|-----------|
| Interpreter | 직접 구현 | ANTLR, Parser Combinator, 정규표현식 |
| Mediator | 직접 구현 | Event Bus, Message Queue, Redux |

### 장단점 비교

| 패턴 | 장점 | 단점 |
|------|------|------|
| Interpreter | 문법 변경 용이, 새 표현식 추가 쉬움 | 복잡한 문법에 비효율, 성능 이슈 |
| Mediator | 결합도 감소, 상호작용 집중 관리 | God Object 위험, 단일 실패점 |

### Mediator vs Observer 비교

| 비교 항목 | Mediator | Observer |
|----------|----------|----------|
| 통신 방향 | 양방향 | 단방향 |
| 중재자 역할 | 능동적 조정 | 없음 (Subject만) |
| 결합도 | Mediator에 집중 | Subject-Observer |
| 사용 목적 | 복잡한 상호작용 조정 | 상태 변경 통지 |

### 적용 체크리스트

| Interpreter 체크 항목 | Mediator 체크 항목 |
|---------------------|------------------|
| 단순한 문법인가? (복잡하면 파서 도구 사용) | 객체 간 복잡한 의존성이 있는가? |
| 문법 변경이 빈번한가? | N:N 통신을 N:1로 줄이고 싶은가? |
| 성능이 크리티컬하지 않은가? | 객체들의 상호작용을 한 곳에서 관리? |
| DSL이 비즈니스 가치를 제공하는가? | 새 Colleague 추가 시 기존 코드 수정 최소화? |

---

## 결론: 복잡성의 구조화

Interpreter와 Mediator 패턴은 서로 다른 종류의 복잡성을 해결합니다:

### 패턴별 핵심 가치:

**Interpreter 패턴:**
- **문법적 복잡성**의 구조화
- **도메인 특화 언어** 구현
- **규칙 엔진**과 **표현식 평가**
- **확장 가능한 문법** 정의

**Mediator 패턴:**
- **관계적 복잡성**의 단순화
- **느슨한 결합** 실현
- **중앙집중식 제어**
- **재사용 가능한 상호작용**

### 현대적 활용:

```
Interpreter Pattern → Modern Evolution:
- Spring Expression Language (SpEL)
- Apache Camel Route Definitions
- Business Rule Engines (Drools)
- GraphQL Query Parsers

Mediator Pattern → Modern Evolution:
- Spring Application Events
- Message Brokers (RabbitMQ, Kafka)
- React Context API
- Microservice Event Bus
```

### 실무 가이드라인:

```
Interpreter 패턴 적용 시점:
- 도메인 특화 언어(DSL)가 필요할 때
- 복잡한 비즈니스 규칙을 표현해야 할 때
- 사용자가 규칙을 정의할 수 있어야 할 때
- 문법이 자주 변경될 가능성이 있을 때

Mediator 패턴 적용 시점:
- 객체 간 복잡한 상호작용이 있을 때
- 결합도를 낮추고 싶을 때
- 통신 프로토콜을 중앙에서 관리하고 싶을 때
- 재사용 가능한 컴포넌트를 만들고 싶을 때

주의사항:
- Interpreter: 성능 오버헤드 고려
- Mediator: Single Point of Failure 방지
- 과도한 추상화 지양
- 적절한 복잡성 수준 유지
```

두 패턴 모두 **"복잡성을 구조화"**하여 이해하기 쉽고 확장 가능한 시스템을 만드는 핵심 도구입니다. 현대 소프트웨어 아키텍처에서 필수불가결한 패턴들입니다.

다음 글에서는 **Memento와 Visitor 패턴**을 탐구하겠습니다. 상태 보존과 연산 분리를 통한 유연한 객체 조작 방법을 살펴보겠습니다.

---

**핵심 메시지:**
"Interpreter는 복잡한 규칙을 객체로 만들어 실행 가능하게 하고, Mediator는 복잡한 관계를 중재자로 단순화한다. 두 패턴 모두 복잡성을 구조화하여 시스템의 이해도와 확장성을 높이는 핵심 메커니즘이다."

### 평가 기준

**독자가 이 글을 읽은 후 달성해야 할 목표:**
- [ ] Interpreter 패턴을 사용한 간단한 DSL을 구현할 수 있다
- [ ] Mediator 패턴을 활용한 컴포넌트 간 통신을 설계할 수 있다
- [ ] 파싱과 해석의 기본 원리를 이해할 수 있다
- [ ] 복잡한 객체 관계를 중재자로 단순화할 수 있다
- [ ] 각 패턴의 성능 특성과 적용 한계를 파악할 수 있다

---

**핵심 메시지:**
"Interpreter는 복잡한 규칙을 객체로 만들어 실행 가능하게 하고, Mediator는 복잡한 관계를 중재자로 단순화한다. 두 패턴 모두 복잡성을 구조화하여 시스템의 이해도와 확장성을 높이는 핵심 메커니즘이다." 