---
draft: false
collection_order: 100
title: "[Design Patterns] 10. 브릿지와 플라이웨이트: 분리와 효율성"
slug: "bridge-flyweight-separation-efficiency"
description: "추상화와 구현을 분리해 조합 폭발을 막는 Bridge 패턴과, 객체 상태를 공유해 메모리를 절약하는 Flyweight 패턴을 비교합니다. 내재적·외재적 상태 분리, 성능 벤치마크, 두 패턴의 결합 사례까지 폭넓게 다룹니다."
image: "wordcloud.png"
date: 2024-12-10T10:00:00+09:00
lastmod: 2026-07-18T10:00:00+09:00
categories:
- Design Patterns
- Structural Patterns
- Performance Optimization
- Memory Management
tags:
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Structural-Pattern
- Behavioral-Pattern
- Software-Architecture(소프트웨어아키텍처)
- OOP(객체지향)
- Abstraction(추상화)
- Encapsulation(캡슐화)
- Composition(합성)
- Polymorphism(다형성)
- Interface(인터페이스)
- Coupling(결합도)
- Cohesion(응집도)
- Adapter
- Strategy
- State
- Memory(메모리)
- Optimization(최적화)
- Performance(성능)
- Benchmark
- Profiling(프로파일링)
- Java
- Implementation(구현)
- Best-Practices
- Case-Study
- Deep-Dive
- Advanced
- Comparison(비교)
- SOLID
---

Bridge와 Flyweight 패턴을 통해 분리와 효율성의 철학을 탐구합니다. 변화의 축을 분리하고, 공유를 통해 메모리 효율성을 극대화하는 방법을 학습합니다.

## 서론: 두 가지 다른 최적화 철학

> *"좋은 설계는 변화에 유연하고 자원을 효율적으로 사용한다. Bridge는 변화의 축을 분리하여 유연성을 추구하고, Flyweight는 공유를 통해 효율성을 극대화한다."*

소프트웨어 설계에서 우리는 종종 **두 가지 근본적인 도전**에 직면합니다:

1. **복잡성 관리**: 변화하는 요구사항에 어떻게 유연하게 대응할 것인가?
2. **자원 효율성**: 제한된 메모리와 CPU를 어떻게 최적으로 활용할 것인가?

**Bridge와 Flyweight 패턴**은 이 두 도전에 대한 서로 다른 해답을 제시합니다:

### Bridge 패턴의 철학: "분리하여 정복하라"
- **문제**: 추상화와 구현이 함께 변화하면서 발생하는 조합 폭발
- **해결**: 추상화와 구현을 독립적인 계층구조로 분리
- **가치**: 런타임 구현체 교체, 플랫폼 독립성, 테스트 용이성

### Flyweight 패턴의 철학: "공유하여 절약하라"
- **문제**: 대량의 유사한 객체들이 메모리를 낭비하는 상황
- **해결**: 공통 상태는 공유하고 고유 상태만 개별 보관
- **가치**: 메모리 효율성, 성능 향상, 확장성 확보

```java
// 현실적인 문제 상황들
public class DesignChallenges {
    
    // 문제 1: 조합 폭발 (Bridge가 해결)
    public void combinationExplosion() {
        // 원하는 것: 다양한 리모컨 × 다양한 기기
        // WindowsTV, WindowsRadio, MacTV, MacRadio, LinuxTV, LinuxRadio...
        // N개 플랫폼 × M개 기기 = N×M개 클래스 폭발!
        
        // 문제: 새로운 플랫폼이나 기기 추가 시 기하급수적 증가
    }
    
    // 문제 2: 메모리 낭비 (Flyweight가 해결)  
    public void memoryWaste() {
        // 게임 맵에 나무 10만 그루가 있다면?
        // 각 나무마다 텍스처, 모델, 색상 정보를 개별 보관?
        // 10만 × 10MB = 1TB 메모리 필요! 😱
        
        List<Tree> forest = new ArrayList<>();
        for (int i = 0; i < 100000; i++) {
            forest.add(new Tree(x, y, "oak", "green", textureData)); // 중복!
        }
    }
}
```

이런 문제들을 어떻게 우아하게 해결할 수 있을까요?

## Bridge 패턴: 추상화와 구현의 우아한 분리

### 패턴의 동기와 철학

Bridge 패턴은 **"추상화(Abstraction)와 구현(Implementation)을 분리하여 각각 독립적으로 변화할 수 있게 하는"** 패턴입니다. 

GoF는 이를 "Decouple an abstraction from its implementation so that the two can vary independently"라고 정의했습니다.

#### Bridge 패턴의 핵심 구조

Bridge 패턴의 구조는 추상화 계층(`Notification` 등)과 구현 계층(`MessageSender` 등)이라는 두 개의 독립적인 클래스 계층으로 나뉜다. 핵심은 추상화가 구현 인터페이스에 대한 참조만 들고 있을 뿐 특정 구현 클래스를 알지 못한다는 점이다. 이 참조가 바로 "다리(Bridge)" 역할을 하며, 컴파일 타임이 아니라 런타임에 조립된다.

이 분리가 갖는 설계 의도는 두 계층이 서로 다른 이유로, 다른 속도로 변화한다는 관찰에서 나온다. 알림의 종류(단순/긴급/예약)는 비즈니스 요구에 따라 늘어나고, 전송 방식(이메일/SMS/Slack)은 인프라 사정에 따라 늘어난다. 두 축이 하나의 클래스 계층에 얽혀 있으면 한쪽이 바뀔 때마다 다른 쪽까지 손대야 하지만, Bridge로 분리하면 각 축을 독립적으로 확장할 수 있다.

아래 예제는 알림 시스템을 통해 이 구조를 보여준다. `Notification` 계층(추상화)은 "무엇을 언제 보낼지"를 책임지고, `MessageSender` 계층(구현)은 "어떻게 전달할지"를 책임진다. `setSender` 메서드로 런타임에 구현체를 교체할 수 있다는 점이 이 구조의 실질적 이점이다.

```java
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Timer;
import java.util.TimerTask;

// 문제 상황: 조합 폭발을 피하고 싶은 경우
// 여러 종류의 메시징 시스템 × 여러 종류의 전송 방식

// 구현 인터페이스 (Implementation)
interface MessageSender {
    void sendMessage(String message, String recipient);
    boolean isConnected();
    void connect();
    void disconnect();
}

// 구체적 구현들 (ConcreteImplementation)
class EmailSender implements MessageSender {
    private String smtpServer;
    private int port;
    private boolean connected = false;
    
    public EmailSender(String smtpServer, int port) {
        this.smtpServer = smtpServer;
        this.port = port;
    }
    
    @Override
    public void connect() {
        System.out.println("Connecting to SMTP server: " + smtpServer + ":" + port);
        // SMTP 연결 로직
        connected = true;
    }
    
    @Override
    public void sendMessage(String message, String recipient) {
        if (!connected) connect();
        System.out.println("Sending email to " + recipient + ": " + message);
        // 실제 이메일 전송 로직
    }
    
    @Override
    public boolean isConnected() {
        return connected;
    }
    
    @Override
    public void disconnect() {
        System.out.println("Disconnecting from SMTP server");
        connected = false;
    }
}

class SMSSender implements MessageSender {
    private String apiKey;
    private String serviceUrl;
    private boolean connected = false;
    
    public SMSSender(String apiKey, String serviceUrl) {
        this.apiKey = apiKey;
        this.serviceUrl = serviceUrl;
    }
    
    @Override
    public void connect() {
        System.out.println("Connecting to SMS service: " + serviceUrl);
        // SMS API 연결 로직
        connected = true;
    }
    
    @Override
    public void sendMessage(String message, String recipient) {
        if (!connected) connect();
        System.out.println("Sending SMS to " + recipient + ": " + message);
        // 실제 SMS 전송 로직
    }
    
    @Override
    public boolean isConnected() {
        return connected;
    }
    
    @Override
    public void disconnect() {
        System.out.println("Disconnecting from SMS service");
        connected = false;
    }
}

class SlackSender implements MessageSender {
    private String webhookUrl;
    private String channel;
    private boolean connected = false;
    
    public SlackSender(String webhookUrl, String channel) {
        this.webhookUrl = webhookUrl;
        this.channel = channel;
    }
    
    @Override
    public void connect() {
        System.out.println("Connecting to Slack webhook: " + webhookUrl);
        // Slack 웹훅 연결 확인
        connected = true;
    }
    
    @Override
    public void sendMessage(String message, String recipient) {
        if (!connected) connect();
        System.out.println("Sending Slack message to " + channel + ": " + message);
        // 실제 Slack 메시지 전송 로직
    }
    
    @Override
    public boolean isConnected() {
        return connected;
    }
    
    @Override
    public void disconnect() {
        System.out.println("Disconnecting from Slack");
        connected = false;
    }
}

// 추상화 (Abstraction)
abstract class Notification {
    protected MessageSender sender;
    protected String title;
    
    public Notification(MessageSender sender, String title) {
        this.sender = sender;
        this.title = title;
    }
    
    public abstract void send(String message, String recipient);
    
    // 공통 기능
    protected String formatMessage(String content) {
        return "[" + title + "] " + content;
    }
    
    public void setSender(MessageSender sender) {
        if (this.sender != null && this.sender.isConnected()) {
            this.sender.disconnect();
        }
        this.sender = sender;
    }
}

// 구체적 추상화들 (RefinedAbstraction)
class SimpleNotification extends Notification {
    public SimpleNotification(MessageSender sender, String title) {
        super(sender, title);
    }
    
    @Override
    public void send(String message, String recipient) {
        String formattedMessage = formatMessage(message);
        sender.sendMessage(formattedMessage, recipient);
    }
}

class UrgentNotification extends Notification {
    private int retryCount;
    
    public UrgentNotification(MessageSender sender, String title, int retryCount) {
        super(sender, title);
        this.retryCount = retryCount;
    }
    
    @Override
    public void send(String message, String recipient) {
        String urgentMessage = "🚨 URGENT 🚨 " + formatMessage(message);
        
        // 재시도 로직 포함
        for (int i = 0; i < retryCount; i++) {
            try {
                sender.sendMessage(urgentMessage, recipient);
                System.out.println("Message sent successfully on attempt " + (i + 1));
                break;
            } catch (Exception e) {
                System.out.println("Attempt " + (i + 1) + " failed, retrying...");
                if (i == retryCount - 1) {
                    System.out.println("All retry attempts failed");
                }
            }
        }
    }
}

class ScheduledNotification extends Notification {
    private LocalDateTime scheduledTime;
    private Timer timer = new Timer();
    
    public ScheduledNotification(MessageSender sender, String title, LocalDateTime scheduledTime) {
        super(sender, title);
        this.scheduledTime = scheduledTime;
    }
    
    @Override
    public void send(String message, String recipient) {
        String scheduledMessage = formatMessage(message + " (Scheduled for: " + scheduledTime + ")");
        
        long delay = Duration.between(LocalDateTime.now(), scheduledTime).toMillis();
        
        if (delay > 0) {
            timer.schedule(new TimerTask() {
                @Override
                public void run() {
                    sender.sendMessage(scheduledMessage, recipient);
                    System.out.println("Scheduled message sent at: " + LocalDateTime.now());
                }
            }, delay);
            System.out.println("Message scheduled for: " + scheduledTime);
        } else {
            sender.sendMessage(scheduledMessage, recipient);
            System.out.println("Message sent immediately (past scheduled time)");
        }
    }
}

// 사용 예시
public class BridgePatternExample {
    public static void main(String[] args) {
        // 다양한 구현체 생성
        MessageSender emailSender = new EmailSender("smtp.gmail.com", 587);
        MessageSender smsSender = new SMSSender("api-key-123", "https://sms-service.com");
        MessageSender slackSender = new SlackSender("https://hooks.slack.com/...", "#alerts");
        
        // 다양한 추상화 객체 생성
        Notification simpleEmail = new SimpleNotification(emailSender, "System Alert");
        Notification urgentSMS = new UrgentNotification(smsSender, "Critical Error", 3);
        Notification scheduledSlack = new ScheduledNotification(
            slackSender, "Daily Report", 
            LocalDateTime.now().plusMinutes(5)
        );
        
        // 사용
        simpleEmail.send("Server is running normally", "admin@company.com");
        urgentSMS.send("Database connection failed!", "+1234567890");
        scheduledSlack.send("Daily metrics report", "#general");
        
        // 런타임에 구현체 교체 가능
        urgentSMS.setSender(slackSender);  // SMS -> Slack으로 변경
        urgentSMS.send("Now sending via Slack instead", "#emergency");
        
        // 장점: N개 알림 타입 × M개 전송 방식 = N+M개 클래스 (조합 폭발 방지!)
    }
}
```

#### Bridge vs Adapter vs Strategy 비교

세 패턴이 자주 혼동되는 이유는 셋 다 "객체를 필드로 들고 있다가 호출을 위임하는" 동일한 구현 형태(합성 + 위임)를 취하기 때문입니다. UML 다이어그램만 보면 세 패턴 모두 클래스 A가 인터페이스 B를 참조하는 동일한 구조로 그려집니다. 차이는 구조가 아니라 "이 구조를 도입한 의도"에 있습니다. Bridge는 설계 초기에 추상화와 구현이라는 두 변화 축을 미리 분리해두는 것이 목적이고, Adapter는 이미 존재하는 호환되지 않는 인터페이스를 사후에 맞추는 것이 목적이며, Strategy는 알고리즘을 런타임에 바꿔 끼우는 것이 목적입니다. 즉 코드 형태만으로는 세 패턴을 구분할 수 없고, "왜 이 위임 구조를 도입했는가"라는 설계 의도를 알아야 구분할 수 있습니다.

```java
// Bridge, Adapter, Strategy의 차이점을 명확히 이해하기

// 1. Bridge: 추상화와 구현을 분리 (구조적 분리)
class MediaPlayer {
    private AudioCodec codec;  // 구현을 참조
    
    public MediaPlayer(AudioCodec codec) {
        this.codec = codec;
    }
    
    public void play(String filename) {
        codec.decode(filename);
        codec.play();
    }
    
    // 런타임에 코덱 교체 가능
    public void changeCodec(AudioCodec newCodec) {
        this.codec = newCodec;
    }
}

// 2. Adapter: 인터페이스 불일치 해결 (호환성 문제)
class LegacyAudioAdapter implements AudioCodec {
    private LegacyAudioLibrary legacyLib;
    
    @Override
    public void decode(String filename) {
        legacyLib.loadAudioFile(filename);  // 다른 인터페이스를 변환
    }
}

// 3. Strategy: 알고리즘 교체 (행동 변경)
class CompressionContext {
    private CompressionStrategy strategy;
    
    public void compress(String data) {
        strategy.compress(data);  // 압축 알고리즘 교체
    }
}

/*
비교 요약:
- Bridge: "무엇을 하는가"와 "어떻게 하는가"를 분리
- Adapter: "호환되지 않는 것"을 "호환되게" 만듦
- Strategy: "다양한 방법" 중 "하나를 선택"하여 수행
*/
```

## Flyweight 패턴: 메모리 효율성의 극한 추구

### 패턴의 동기와 철학

Flyweight 패턴은 **"대량의 유사한 객체들을 효율적으로 지원"**하는 패턴입니다. 핵심 아이디어는 **내재적 상태(Intrinsic State)**와 **외재적 상태(Extrinsic State)**를 분리하는 것입니다.

Flyweight의 설계 의도는 객체가 가진 상태를 두 종류로 구분하는 데서 시작한다. 내재적 상태(intrinsic state)는 여러 객체가 동일한 값을 공유해도 무방한 데이터로, 문자의 폰트나 글리프 데이터처럼 불변이며 컨텍스트에 의존하지 않는다. 외재적 상태(extrinsic state)는 위치나 색상처럼 객체마다 달라 공유할 수 없는 데이터다.

이 구분이 성립하려면 내재적 상태를 불변 객체로 만들고, 외재적 상태는 별도의 Context 객체나 메서드 매개변수로 전달해야 한다. Flyweight Factory는 동일한 내재적 상태를 갖는 객체를 캐싱해 재사용함으로써, 개별 인스턴스를 새로 생성하는 대신 이미 존재하는 Flyweight를 공유한다.

Flyweight는 "캐시가 있는 팩토리"라는 표면적 형태 때문에 오브젝트 풀(Object Pool)이나 단순 캐싱과 자주 혼동되지만, 셋은 해결하는 문제와 인스턴스의 생애주기가 다르다. 오브젝트 풀은 DB 커넥션이나 스레드처럼 **생성 비용이 비싼 가변 객체**를 미리 만들어 두고 "대여(checkout) → 사용 → 반납(release)" 주기로 재사용하는 기법이다. 반납된 객체는 내부 상태가 초기화되어 다음 대여자에게 다른 용도로 다시 쓰인다 — 즉 풀 안의 한 인스턴스가 시간에 따라 여러 논리적 신원을 거쳐 간다. 단순 캐싱은 "같은 입력에 같은 계산 결과"를 재사용해 재계산을 피하는 것이 목적이며, 캐시 항목은 각자 독립적으로 존재하다가 개별적으로 축출(evict)된다. 반면 Flyweight의 목적은 재계산 회피나 생성 비용 회피가 아니라 **동시에 살아 있는 논리적 인스턴스 수를 물리적 인스턴스 수보다 훨씬 적게 유지하는 것**이다 — `ConcreteCharacter('A', "Arial", 12)`는 대여되었다가 반납되는 것이 아니라, 프로그램이 종료될 때까지 동일한 신원으로 계속 공유되는 불변 객체이며, 문서에 'A'가 10만 번 등장해도 그 인스턴스는 결코 늘어나지 않는다. 따라서 "캐시에 값을 담아 재사용하니 Flyweight"라고 판단해 가변 상태를 캐시 대상 객체에 그대로 남겨두면, 한 인스턴스를 공유하는 여러 컨텍스트가 서로의 상태를 오염시키는 버그로 이어진다 — 이것이 Flyweight를 흉내 낸 캐싱에서 가장 흔히 발생하는 오적용이다.

아래 텍스트 에디터 예제에서 `ConcreteCharacter`(내재적 상태: 문자, 폰트, 글리프 데이터)는 팩토리에 의해 공유되고, `CharacterContext`(외재적 상태: 좌표, 색상)만 문자 하나하나마다 새로 생성된다. 알파벳과 특수문자 수십 종만 있으면 되므로, 수십만 자를 렌더링해도 Flyweight 인스턴스 수는 수십 개 수준에 머문다.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

// 문제 상황: 텍스트 에디터에서 백만 개의 문자를 렌더링
// 각 문자마다 폰트, 크기, 색상 정보를 개별적으로 저장한다면?

// 비효율적인 방법
class Character_BAD {
    private char c;
    private String fontFamily;  // "Arial" (반복!)
    private int fontSize;       // 12 (반복!)
    private Color color;        // Color.BLACK (반복!)
    private int x, y;          // 위치는 각자 다름
    
    // 1,000,000개 문자 × 100 bytes = 100MB 메모리 사용
}

// Flyweight 방법으로 해결
// 공통된 부분(폰트 정보)은 공유하고, 개별적인 부분(위치)만 따로 저장

// Flyweight 인터페이스
interface CharacterFlyweight {
    void render(Canvas canvas, int x, int y, Color color);
    int getWidth();
    int getHeight();
}

// 구체적 Flyweight - 내재적 상태만 보유
class ConcreteCharacter implements CharacterFlyweight {
    private final char character;      // 내재적 상태
    private final String fontFamily;   // 내재적 상태  
    private final int fontSize;        // 내재적 상태
    private final byte[] glyphData;    // 내재적 상태 (폰트 렌더링 데이터)
    
    // 한 번 생성되면 변경되지 않음 (불변 객체)
    public ConcreteCharacter(char character, String fontFamily, int fontSize) {
        this.character = character;
        this.fontFamily = fontFamily;
        this.fontSize = fontSize;
        this.glyphData = loadGlyphData(character, fontFamily, fontSize);
    }
    
    @Override
    public void render(Canvas canvas, int x, int y, Color color) {
        // x, y, color는 외재적 상태로 매개변수로 받음
        canvas.setColor(color);
        canvas.drawGlyph(glyphData, x, y);
    }
    
    @Override
    public int getWidth() {
        return calculateWidth(glyphData);
    }
    
    @Override
    public int getHeight() {
        return fontSize;
    }
    
    private byte[] loadGlyphData(char c, String font, int size) {
        // 실제로는 폰트 파일에서 글리프 데이터를 로딩
        System.out.println("Loading glyph data for '" + c + "' in " + font + " " + size + "pt");
        return new byte[1024]; // 가상의 글리프 데이터
    }
    
    private int calculateWidth(byte[] glyphData) {
        // 글리프 데이터에서 너비 계산
        return fontSize / 2; // 간단한 예시
    }
}

// Flyweight Factory - 객체 공유 관리
class CharacterFlyweightFactory {
    private static final Map<String, CharacterFlyweight> flyweights = new ConcurrentHashMap<>();
    
    public static CharacterFlyweight getCharacter(char c, String fontFamily, int fontSize) {
        String key = c + "_" + fontFamily + "_" + fontSize;
        
        return flyweights.computeIfAbsent(key, k -> {
            System.out.println("Creating new flyweight for: " + key);
            return new ConcreteCharacter(c, fontFamily, fontSize);
        });
    }
    
    public static int getFlyweightCount() {
        return flyweights.size();
    }
    
    public static void printStatistics() {
        System.out.println("Total flyweights created: " + flyweights.size());
        System.out.println("Memory saved: " + calculateMemorySaved() + " MB");
    }
    
    private static long calculateMemorySaved() {
        // 단순 계산 예시
        return flyweights.size() * 100; // 각 flyweight가 100KB 절약한다고 가정
    }
}

// Context - 외재적 상태 보유
class CharacterContext {
    private final int x, y;                    // 외재적 상태 (위치)
    private final Color color;                 // 외재적 상태 (색상)
    private final CharacterFlyweight flyweight; // Flyweight 참조
    
    public CharacterContext(int x, int y, Color color, char c, String fontFamily, int fontSize) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.flyweight = CharacterFlyweightFactory.getCharacter(c, fontFamily, fontSize);
    }
    
    public void render(Canvas canvas) {
        flyweight.render(canvas, x, y, color);
    }
    
    public int getX() { return x; }
    public int getY() { return y; }
    public Color getColor() { return color; }
    public CharacterFlyweight getFlyweight() { return flyweight; }
}

// 텍스트 문서 - Flyweight 활용
class TextDocument {
    private List<CharacterContext> characters = new ArrayList<>();
    private String defaultFontFamily = "Arial";
    private int defaultFontSize = 12;
    
    public void addText(String text, int startX, int startY, Color color) {
        int currentX = startX;
        int currentY = startY;
        
        for (char c : text.toCharArray()) {
            if (c == '\n') {
                currentX = startX;
                currentY += defaultFontSize + 2; // 줄 간격
                continue;
            }
            
            CharacterContext context = new CharacterContext(
                currentX, currentY, color, c, defaultFontFamily, defaultFontSize
            );
            characters.add(context);
            
            // 다음 문자 위치 계산
            currentX += context.getFlyweight().getWidth();
        }
    }
    
    public void render(Canvas canvas) {
        System.out.println("Rendering document with " + characters.size() + " characters");
        for (CharacterContext character : characters) {
            character.render(canvas);
        }
    }
    
    public void printMemoryUsage() {
        System.out.println("Document statistics:");
        System.out.println("- Total characters: " + characters.size());
        System.out.println("- Unique flyweights: " + CharacterFlyweightFactory.getFlyweightCount());
        
        // 메모리 절약 계산
        long withoutFlyweight = characters.size() * 100L; // 각 문자당 100 bytes
        long withFlyweight = CharacterFlyweightFactory.getFlyweightCount() * 100L + characters.size() * 20L; // flyweight + context
        long saved = withoutFlyweight - withFlyweight;
        
        System.out.println("- Memory without Flyweight: " + withoutFlyweight + " bytes");
        System.out.println("- Memory with Flyweight: " + withFlyweight + " bytes");
        System.out.println("- Memory saved: " + saved + " bytes (" + 
                          (saved * 100 / withoutFlyweight) + "% reduction)");
    }
}

// 사용 예시
public class FlyweightPatternExample {
    public static void main(String[] args) {
        Canvas canvas = new MockCanvas();
        TextDocument document = new TextDocument();
        
        // 대량의 텍스트 추가 (현실적인 시나리오)
        document.addText("Hello World! This is a sample text.", 10, 10, Color.BLACK);
        document.addText("Hello World! This is another line.", 10, 30, Color.BLUE);
        document.addText("Same characters appear multiple times.", 10, 50, Color.BLACK);
        
        // 더 많은 텍스트 추가 (Flyweight 효과 확인)
        for (int i = 0; i < 100; i++) {
            document.addText("Line " + i + ": Hello World!", 10, 70 + i * 20, 
                           i % 2 == 0 ? Color.BLACK : Color.BLUE);
        }
        
        // 렌더링
        document.render(canvas);
        
        // 메모리 사용량 분석
        document.printMemoryUsage();
        CharacterFlyweightFactory.printStatistics();
        
        /*
         * 출력 예시:
         * Creating new flyweight for: H_Arial_12
         * Creating new flyweight for: e_Arial_12
         * Creating new flyweight for: l_Arial_12
         * Creating new flyweight for: o_Arial_12
         * Creating new flyweight for:  _Arial_12  (공백)
         * ...
         * 
         * Document statistics:
         * - Total characters: 3847
         * - Unique flyweights: 26  (a-z, A-Z, 0-9, 공백, 특수문자 등)
         * - Memory without Flyweight: 384,700 bytes
         * - Memory with Flyweight: 79,540 bytes
         * - Memory saved: 305,160 bytes (79% reduction)
         */
    }
}

// Mock Canvas for demonstration
class MockCanvas implements Canvas {
    private Color currentColor = Color.BLACK;
    
    @Override
    public void setColor(Color color) {
        this.currentColor = color;
    }
    
    @Override
    public void drawGlyph(byte[] glyphData, int x, int y) {
        // 실제로는 화면에 그리기
        // System.out.println("Drawing glyph at (" + x + "," + y + ") with color " + currentColor);
    }
}

interface Canvas {
    void setColor(Color color);
    void drawGlyph(byte[] glyphData, int x, int y);
}

enum Color {
    BLACK, BLUE, RED, GREEN
}
```

### 게임 개발에서의 Flyweight 활용

```java
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;

// 게임에서 파티클 시스템 최적화
// 수만 개의 파티클이 동시에 존재하는 상황
// 아래 Texture / Graphics / TextureManager / SparkParticle / ExplosionParticle 는
// 실제 게임 엔진(예: libGDX, LWJGL)이 제공한다고 가정한 가상 타입이며, 이 파일 안에서는 정의하지 않는다.

// Flyweight 인터페이스
interface ParticleFlyweight {
    void update(float deltaTime, float x, float y, float velocityX, float velocityY);
    void render(Graphics graphics, float x, float y, float scale, float alpha);
}

// 구체적 Flyweight들
class FireParticle implements ParticleFlyweight {
    private final Texture texture;      // 내재적 상태
    private final Color baseColor;      // 내재적 상태
    private final float baseLifetime;   // 내재적 상태
    
    public FireParticle() {
        this.texture = TextureManager.load("fire_particle.png");
        this.baseColor = Color.ORANGE;
        this.baseLifetime = 2.0f;
    }
    
    @Override
    public void update(float deltaTime, float x, float y, float velocityX, float velocityY) {
        // 물리 업데이트 (외재적 상태를 매개변수로 받음)
        // 실제로는 더 복잡한 파티클 물리 계산
    }
    
    @Override
    public void render(Graphics graphics, float x, float y, float scale, float alpha) {
        graphics.setColor(baseColor.withAlpha(alpha));
        graphics.drawTexture(texture, x, y, scale);
    }
}

class SmokeParticle implements ParticleFlyweight {
    private final Texture texture;
    private final Color baseColor;
    private final float baseLifetime;
    
    public SmokeParticle() {
        this.texture = TextureManager.load("smoke_particle.png");
        this.baseColor = Color.GRAY;
        this.baseLifetime = 5.0f;
    }
    
    @Override
    public void update(float deltaTime, float x, float y, float velocityX, float velocityY) {
        // 연기 특유의 물리 업데이트
    }
    
    @Override
    public void render(Graphics graphics, float x, float y, float scale, float alpha) {
        graphics.setColor(baseColor.withAlpha(alpha * 0.7f)); // 연기는 더 투명
        graphics.drawTexture(texture, x, y, scale);
    }
}

// Flyweight Factory
class ParticleTypeFactory {
    private static final Map<String, ParticleFlyweight> particleTypes = new HashMap<>();
    
    static {
        particleTypes.put("fire", new FireParticle());
        particleTypes.put("smoke", new SmokeParticle());
        particleTypes.put("spark", new SparkParticle());
        particleTypes.put("explosion", new ExplosionParticle());
    }
    
    public static ParticleFlyweight getParticleType(String type) {
        return particleTypes.get(type);
    }
}

// Context - 각 파티클의 개별 상태
class Particle {
    private float x, y;              // 외재적 상태 (위치)
    private float velocityX, velocityY; // 외재적 상태 (속도)
    private float scale;             // 외재적 상태 (크기)
    private float alpha;             // 외재적 상태 (투명도)
    private float lifetime;          // 외재적 상태 (수명)
    private ParticleFlyweight type;  // Flyweight 참조
    
    public Particle(float x, float y, String typeName) {
        this.x = x;
        this.y = y;
        this.velocityX = (float) (Math.random() - 0.5) * 100;
        this.velocityY = (float) (Math.random() - 0.5) * 100;
        this.scale = 1.0f;
        this.alpha = 1.0f;
        this.lifetime = 0.0f;
        this.type = ParticleTypeFactory.getParticleType(typeName);
    }
    
    public void update(float deltaTime) {
        // 위치 업데이트
        x += velocityX * deltaTime;
        y += velocityY * deltaTime;
        
        // 수명 업데이트
        lifetime += deltaTime;
        alpha = Math.max(0, 1.0f - lifetime / 3.0f); // 3초 후 완전 투명
        
        // Flyweight에 위임
        type.update(deltaTime, x, y, velocityX, velocityY);
    }
    
    public void render(Graphics graphics) {
        if (alpha > 0) {
            type.render(graphics, x, y, scale, alpha);
        }
    }
    
    public boolean isAlive() {
        return alpha > 0;
    }
}

// 파티클 시스템
class ParticleSystem {
    private List<Particle> particles = new ArrayList<>();
    
    public void emit(String particleType, float x, float y, int count) {
        for (int i = 0; i < count; i++) {
            particles.add(new Particle(x + (float) Math.random() * 10, 
                                     y + (float) Math.random() * 10, 
                                     particleType));
        }
    }
    
    public void update(float deltaTime) {
        // 파티클 업데이트 및 죽은 파티클 제거
        particles.removeIf(particle -> {
            particle.update(deltaTime);
            return !particle.isAlive();
        });
    }
    
    public void render(Graphics graphics) {
        for (Particle particle : particles) {
            particle.render(graphics);
        }
    }
    
    public void printStatistics() {
        System.out.println("Active particles: " + particles.size());
        System.out.println("Particle types: " + ParticleTypeFactory.particleTypes.size());
        
        // 메모리 계산
        long withoutFlyweight = particles.size() * 1000L; // 각 파티클이 1KB라고 가정
        long withFlyweight = particles.size() * 100L + ParticleTypeFactory.particleTypes.size() * 500L;
        
        System.out.println("Memory usage - Without Flyweight: " + withoutFlyweight + " bytes");
        System.out.println("Memory usage - With Flyweight: " + withFlyweight + " bytes");
        System.out.println("Memory saved: " + (withoutFlyweight - withFlyweight) + " bytes");
    }
}
```

## Bridge vs Flyweight: 두 철학의 비교

### 패턴의 철학적 차이

```java
// 두 패턴의 근본적 차이점 이해하기

// Bridge: "구조적 분리"를 통한 유연성
class DatabaseManager {
    private DatabaseConnector connector;  // 구현과 분리
    
    public DatabaseManager(DatabaseConnector connector) {
        this.connector = connector;
    }
    
    public void saveUser(User user) {
        // 추상화 레벨의 비즈니스 로직
        validateUser(user);
        String sql = "INSERT INTO users...";
        connector.execute(sql);  // 구현에 위임
    }
    
    // 런타임에 구현체 교체 가능 (Bridge의 핵심)
    public void switchDatabase(DatabaseConnector newConnector) {
        this.connector = newConnector;
    }
}

// Flyweight: "상태 분리"를 통한 효율성
class Icon {
    private final String imagePath;    // 내재적 상태 (공유)
    private final byte[] imageData;    // 내재적 상태 (공유)
    
    // 외재적 상태는 매개변수로 받음
    public void draw(Graphics g, int x, int y, int size) {
        g.drawImage(imageData, x, y, size, size);
    }
}

/*
핵심 차이점:

Bridge 패턴:
- 목적: 추상화와 구현의 독립적 변화
- 관점: 구조적 유연성 (Structural Flexibility)
- 해결: 조합 폭발 문제
- 시점: 설계 타임 분리, 런타임 교체

Flyweight 패턴:  
- 목적: 메모리 사용량 최적화
- 관점: 자원 효율성 (Resource Efficiency)
- 해결: 메모리 낭비 문제
- 시점: 런타임 상태 분리, 객체 공유
*/
```

### 언제 어떤 패턴을 선택할 것인가?

Bridge와 Flyweight 중 무엇을 적용할지는 막연한 감이 아니라 설계 상황이 가진 두 가지 정량적 특성으로 판단할 수 있다. Bridge는 추상화 축의 변형 수와 구현 축의 변형 수를 곱한 값(N×M, 조합해서 만들 때 필요한 클래스 수)이 두 축을 단순히 더한 값(N+M, 분리했을 때 필요한 클래스 수)보다 클 때, 또는 런타임에 구현체를 교체해야 할 때 적용을 검토한다. Flyweight는 예상 인스턴스 수가 일정 임계치를 넘고 내재적 상태와 외재적 상태를 분리할 수 있을 때 적용을 검토한다. 두 조건이 동시에 성립하면 두 패턴을 결합해야 한다는 신호다.

아래 `PatternDecisionGuide`는 이 두 조건을 실제로 계산하는 판단 로직이다. `DesignContext`에 설계 상황(추상화/구현 변형 수, 런타임 교체 필요 여부, 예상 인스턴스 수, 상태 분리 가능 여부)을 채워 넣으면 `recommend`가 `BRIDGE`, `FLYWEIGHT`, `BOTH`, `NEITHER` 중 하나를 결정론적으로 반환한다.

```java
// 선택 가이드라인을 실제로 계산하는 의사결정 로직

import java.util.List;

public class PatternDecisionGuide {

    enum RecommendedPattern { BRIDGE, FLYWEIGHT, BOTH, NEITHER }

    // 설계 상황을 나타내는 입력값
    static class DesignContext {
        final String name;
        final int abstractionVariants;    // 추상화 축의 변형 수 (예: 알림 종류)
        final int implementationVariants; // 구현 축의 변형 수 (예: 전송 방식)
        final boolean needsRuntimeSwap;   // 런타임에 구현체를 교체해야 하는가
        final long expectedInstanceCount; // 예상 인스턴스 수
        final boolean stateSeparable;     // 내재적/외재적 상태 분리가 자연스러운가

        DesignContext(String name, int abstractionVariants, int implementationVariants,
                      boolean needsRuntimeSwap, long expectedInstanceCount, boolean stateSeparable) {
            this.name = name;
            this.abstractionVariants = abstractionVariants;
            this.implementationVariants = implementationVariants;
            this.needsRuntimeSwap = needsRuntimeSwap;
            this.expectedInstanceCount = expectedInstanceCount;
            this.stateSeparable = stateSeparable;
        }
    }

    // Flyweight를 검토할 인스턴스 수 임계치 (프로젝트 상황에 맞게 조정 가능한 예시값)
    private static final long FLYWEIGHT_INSTANCE_THRESHOLD = 10_000L;

    // N×M(조합 시 클래스 수)이 N+M(분리 시 클래스 수)보다 큰지로 조합 폭발 여부를 판정
    static boolean combinationExplosionExpected(DesignContext ctx) {
        long combined = (long) ctx.abstractionVariants * ctx.implementationVariants;
        long separated = ctx.abstractionVariants + ctx.implementationVariants;
        return combined > separated;
    }

    static boolean shouldApplyBridge(DesignContext ctx) {
        return combinationExplosionExpected(ctx) || ctx.needsRuntimeSwap;
    }

    static boolean shouldApplyFlyweight(DesignContext ctx) {
        return ctx.expectedInstanceCount >= FLYWEIGHT_INSTANCE_THRESHOLD && ctx.stateSeparable;
    }

    static RecommendedPattern recommend(DesignContext ctx) {
        boolean bridge = shouldApplyBridge(ctx);
        boolean flyweight = shouldApplyFlyweight(ctx);
        if (bridge && flyweight) return RecommendedPattern.BOTH;
        if (bridge) return RecommendedPattern.BRIDGE;
        if (flyweight) return RecommendedPattern.FLYWEIGHT;
        return RecommendedPattern.NEITHER;
    }

    public static void main(String[] args) {
        List<DesignContext> scenarios = List.of(
            new DesignContext("알림 시스템 (알림 3종 x 전송 3종, 런타임 교체 필요)", 3, 3, true, 0L, false),
            new DesignContext("텍스트 에디터 (문자 10만개 렌더링)", 1, 1, false, 100_000L, true),
            new DesignContext("게임 렌더링 (API 2종 x 렌더러 3종 + 스프라이트 5만개)", 2, 3, true, 50_000L, true),
            new DesignContext("단순 CRUD 서비스 (변형 1종, 인스턴스 10개)", 1, 1, false, 10L, false)
        );

        for (DesignContext ctx : scenarios) {
            RecommendedPattern result = recommend(ctx);
            System.out.printf("%-55s -> %-9s (조합폭발=%b, 대량공유=%b)%n",
                ctx.name, result, combinationExplosionExpected(ctx), shouldApplyFlyweight(ctx));
        }
    }
}

/*
 * 실행 결과:
 * 알림 시스템 (알림 3종 x 전송 3종, 런타임 교체 필요)      -> BRIDGE    (조합폭발=true, 대량공유=false)
 * 텍스트 에디터 (문자 10만개 렌더링)                       -> FLYWEIGHT (조합폭발=false, 대량공유=true)
 * 게임 렌더링 (API 2종 x 렌더러 3종 + 스프라이트 5만개)     -> BOTH      (조합폭발=true, 대량공유=true)
 * 단순 CRUD 서비스 (변형 1종, 인스턴스 10개)               -> NEITHER   (조합폭발=false, 대량공유=false)
 */
```

첫 번째 시나리오는 3×3=9개 클래스가 3+3=6개보다 많아 조합 폭발 조건을 만족하고 런타임 교체도 필요하므로 `BRIDGE`로 판정된다. 두 번째 시나리오는 인스턴스 수(10만)가 임계치를 넘고 상태 분리가 가능하므로 `FLYWEIGHT`로, 세 번째는 두 조건을 모두 만족해 `BOTH`로, 네 번째는 어느 조건도 만족하지 않아 `NEITHER`로 판정된다. 여기서 쓴 임계치(1만 개)와 조합 폭발 기준(N×M > N+M)은 절대적 규칙이 아니라 판단의 출발점이며, 실제 임계치는 클래스 관리 비용과 메모리 제약에 따라 팀이 조정해야 한다.

아래는 Bridge와 Flyweight를 실제로 결합한 게임 렌더링 시스템 예시다. 그래픽 API(OpenGL/DirectX/Vulkan)를 Bridge로 교체 가능하게 하고, 스프라이트 데이터는 Flyweight로 공유한다.

```java
// 실제 결합 예시: 게임 렌더링 시스템
interface RenderingEngine {  // Bridge의 구현 인터페이스
    void drawSprite(SpriteData sprite, float x, float y, float scale);
}

class OpenGLRenderer implements RenderingEngine {
    @Override
    public void drawSprite(SpriteData sprite, float x, float y, float scale) {
        // OpenGL 구현
    }
}

class SpriteData {  // Flyweight
    private final Texture texture;     // 내재적 상태
    private final int width, height;   // 내재적 상태
    
    public void render(RenderingEngine engine, float x, float y, float scale) {
        engine.drawSprite(this, x, y, scale);  // Bridge + Flyweight
    }
}

class GameRenderer {  // Bridge의 추상화
    private RenderingEngine engine;
    
    public GameRenderer(RenderingEngine engine) {
        this.engine = engine;
    }
    
    public void renderSprite(String spriteType, float x, float y, float scale) {
        SpriteData sprite = SpriteFactory.getSprite(spriteType);  // Flyweight
        sprite.render(engine, x, y, scale);  // Bridge
    }
}
```

## 성능 분석과 실무 고려사항

### 성능 측정 결과

Bridge의 간접 호출 비용과 Flyweight의 메모리 절감 효과를 논하기 전에, 무엇이 상대적으로 무시할 만한 오버헤드이고 무엇이 실측이 필요한 수치인지부터 구분해야 한다. 인터페이스를 통한 가상 호출(virtual call)은 JIT가 충분히 워밍업된 이후에는 인라인화나 분기 예측으로 비용이 거의 사라지는 경우가 많지만, 그 정도는 JVM 구현·호출 지점의 다형성(monomorphic/polymorphic)·JIT 컴파일 단계에 따라 달라지므로 "20% 오버헤드"처럼 고정된 수치로 일반화할 수 없다. 반대로 Flyweight의 메모리 절감률은 원리상 예측 가능하다 — 공유되는 내재적 상태 인스턴스 수가 K개로 고정된 채 컨텍스트 수 N이 늘어나면, 절감률은 N이 커질수록 100%에 점근한다. 아래 표는 이 두 가지 서로 다른 성격의 수치를 보여주기 위한 예시이며 실제 벤치마크 실행 결과가 아니다.

```java
// 예시 성능 특성 (실측 아님)

/*
Bridge 패턴 오버헤드 측정:
=================================
작업              | 직접 호출  | Bridge 패턴 | 오버헤드
간단한 메서드     |   1.0ns   |    1.2ns   |   20%
복잡한 메서드     |  100ns    |   102ns    |    2%
I/O 작업         |   1ms     |   1.001ms  |   0.1%

결론: I/O나 복잡한 작업에서는 오버헤드가 무시할 수준


Flyweight 패턴 메모리 효율성:
===================================  
객체 수          | 일반 구현  | Flyweight | 메모리 절약
1,000개         |   40MB    |    8MB   |    80%
10,000개        |  400MB    |   25MB   |   93.8%
100,000개       | 4,000MB   |   85MB   |   97.9%
1,000,000개     |40,000MB   |  350MB   |   99.1%

결론: 객체 수가 많을수록 효과가 기하급수적으로 증가

※ 위 수치는 이해를 돕기 위한 예시이며 실측치가 아닙니다. 실제 절약률은 객체 크기, JVM/런타임, 힙 설정에 따라 달라집니다.
*/

import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryUsage;
import java.util.ArrayList;
import java.util.List;

// 이 벤치마크가 "Flyweight 미적용" 대조군으로 쓰는 문자 객체.
// 위쪽 Character_BAD와 같은 문제(폰트/크기/색상을 매번 중복 보관)를 보여주기 위한 별도 클래스다.
class RegularCharacter {
    private final char character;
    private final String fontFamily;
    private final int fontSize;
    private final int x, y;

    public RegularCharacter(char character, String fontFamily, int fontSize, int x, int y) {
        this.character = character;
        this.fontFamily = fontFamily;
        this.fontSize = fontSize;
        this.x = x;
        this.y = y;
    }
}

// 메모리 사용량 실시간 측정
public class PerformanceMonitor {
    private static final MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
    
    public static void measureMemoryUsage(String phase) {
        MemoryUsage heapUsage = memoryBean.getHeapMemoryUsage();
        long usedMemory = heapUsage.getUsed();
        long maxMemory = heapUsage.getMax();
        
        System.out.printf("%s - Memory Usage: %,d bytes (%.1f%% of max)\n", 
                         phase, usedMemory, (double) usedMemory / maxMemory * 100);
    }
    
    public static void benchmarkFlyweight() {
        measureMemoryUsage("Before creating objects");
        
        // Flyweight 없이
        List<RegularCharacter> regularChars = new ArrayList<>();
        for (int i = 0; i < 100000; i++) {
            regularChars.add(new RegularCharacter('A', "Arial", 12, i, i));
        }
        measureMemoryUsage("After creating 100k regular objects");
        
        // 메모리 정리
        regularChars.clear();
        System.gc();
        measureMemoryUsage("After GC");
        
        // Flyweight 사용
        List<CharacterContext> flyweightChars = new ArrayList<>();
        for (int i = 0; i < 100000; i++) {
            flyweightChars.add(new CharacterContext(i, i, Color.BLACK, 'A', "Arial", 12));
        }
        measureMemoryUsage("After creating 100k flyweight objects");
    }
}
```

`PerformanceMonitor`는 표의 예시 수치를 감으로 받아들이지 않고 실제 힙 사용량으로 검증하는 최소한의 방법을 보여준다. `MemoryMXBean.getHeapMemoryUsage()`는 JVM이 관리하는 힙의 현재 사용량·최대치를 조회하는 표준 API이며, 객체 10만 개를 일반 방식과 Flyweight 방식으로 각각 생성한 뒤 그 사이의 힙 사용량 변화를 비교하는 데 쓸 수 있다. 다만 `System.gc()` 호출은 JVM에 가비지 컬렉션을 강력히 "요청"할 뿐 즉시 실행이나 완전한 회수를 보장하지 않으므로(GC 실행 여부와 시점은 명세상 구현 정의다), 이 방식으로 얻은 측정값에는 노이즈가 섞일 수 있다. 실무에서 신뢰도 높은 비교가 필요하다면 이 수동 측정보다 JFR(Java Flight Recorder)이나 프로파일러의 힙 덤프 비교, 혹은 JMH 같은 벤치마크 도구를 사용하는 편이 안전하다.

### 실무 적용 가이드라인

Bridge와 Flyweight를 실무에 적용할 때 실제로 부딪히는 문제는 "이 패턴을 쓸지 말지"가 아니라 패턴 주변의 세부 구현이다. Bridge는 구현체 호출 방식(동기 단건 호출 대 비동기 배치 호출)에 따라 처리량이 수 배 차이 날 수 있고, Flyweight는 팩토리 캐시가 무한정 자라나 "메모리를 아끼려던 캐시 자체가 새로운 메모리 누수원이 되는" 역설을 어떻게 막느냐가 관건이다. 아래 `PracticalGuidelines`는 이 두 문제에 대한 구체적인 대응 — Bridge 쪽은 큐잉을 통한 메시지 배치 전송, Flyweight 쪽은 캐시 크기 제한과 LRU 축출 — 을 코드로 보여준다.

```java
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;

// 실무에서의 주의사항과 최적화 팁

public class PracticalGuidelines {
    
    // Bridge 패턴 최적화
    public void bridgeOptimization() {
        /*
        Bridge 패턴 최적화 팁:
        
        1. 인터페이스 설계 최적화
           - 메서드 수를 최소화 (호출 오버헤드 감소)
           - 배치 처리 지원 (여러 작업을 한 번에)
           - 비동기 처리 고려
        
        2. 구현체 선택 최적화
           - 환경에 따른 자동 선택
           - 성능 모니터링 기반 동적 교체
           - 폴백 메커니즘 구현
        
        3. 메모리 관리
           - 구현체 풀링 활용
           - 약한 참조 사용 고려
           - 생명주기 관리
        */
        
        // 큐에 쌓인 메시지 한 건을 나타내는 값 객체.
        // MessageSender는 Bridge 절(위 BridgePatternExample)에서 정의한 인터페이스를 재사용한다고 가정한다.
        class Message {
            final String text;
            final String recipient;

            Message(String text, String recipient) {
                this.text = text;
                this.recipient = recipient;
            }
        }

        // 예시: 최적화된 Bridge 구현
        class OptimizedMessageBridge {
            private MessageSender sender;
            private final Queue<Message> messageQueue = new LinkedList<>();
            private final ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
            
            public OptimizedMessageBridge(MessageSender sender) {
                this.sender = sender;
                // 배치 처리를 위한 스케줄러
                scheduler.scheduleAtFixedRate(this::flushMessages, 0, 100, TimeUnit.MILLISECONDS);
            }
            
            public void sendMessage(String message, String recipient) {
                messageQueue.offer(new Message(message, recipient));
            }
            
            private void flushMessages() {
                List<Message> batch = new ArrayList<>();
                while (!messageQueue.isEmpty() && batch.size() < 50) {
                    batch.add(messageQueue.poll());
                }
                if (!batch.isEmpty()) {
                    // MessageSender 인터페이스는 sendBatch를 선언하지 않으므로 개별 호출로 대체한다.
                    // 실제 전송 프로토콜이 배치 API를 지원한다면 인터페이스에 sendBatch(List<Message>)를
                    // 추가해 한 번의 네트워크 호출로 묶는 것이 효율적이다.
                    for (Message m : batch) {
                        sender.sendMessage(m.text, m.recipient);
                    }
                }
            }
        }
    }
    
    // Flyweight 패턴 최적화
    public void flyweightOptimization() {
        /*
        Flyweight 패턴 최적화 팁:
        
        1. 팩토리 최적화
           - ConcurrentHashMap 사용 (동시성)
           - WeakReference 활용 (메모리 누수 방지)
           - LRU 캐시 구현 (메모리 제한)
        
        2. 내재적/외재적 상태 분리 최적화
           - 불변 객체로 내재적 상태 설계
           - 외재적 상태 전달 최적화 (객체 풀링)
           - 지연 초기화 활용
        
        3. 가비지 컬렉션 최적화
           - 객체 생성 최소화
           - 재사용 가능한 외재적 상태 객체
           - 메모리 풀 활용
        */
        
        // 예시: 최적화된 Flyweight Factory
        class OptimizedFlyweightFactory<T> {
            private final Map<String, T> flyweights = new ConcurrentHashMap<>();
            private final Function<String, T> factory;
            private final int maxSize;
            
            public OptimizedFlyweightFactory(Function<String, T> factory, int maxSize) {
                this.factory = factory;
                this.maxSize = maxSize;
            }
            
            public T getFlyweight(String key) {
                return flyweights.computeIfAbsent(key, k -> {
                    if (flyweights.size() >= maxSize) {
                        // LRU 정책으로 오래된 항목 제거
                        evictOldest();
                    }
                    return factory.apply(k);
                });
            }
            
            private void evictOldest() {
                // 단순화된 LRU 구현
                String firstKey = flyweights.keySet().iterator().next();
                flyweights.remove(firstKey);
            }
        }
    }
}
```

두 구현에서 눈여겨볼 지점은 최적화가 패턴 자체의 구조를 바꾸지 않고 그 접점에 표준적인 시스템 프로그래밍 기법을 얹는 방식으로 이뤄진다는 것이다. `OptimizedMessageBridge`는 Bridge가 정의하는 위임 호출(`sender.sendMessage`) 자체는 그대로 둔 채 앞단에 큐와 스케줄러를 얹어 호출 빈도만 조절했고, `OptimizedFlyweightFactory`도 Flyweight의 공유 개념은 그대로 두고 `maxSize`라는 캐시 상한과 축출 정책만 추가했다. 다만 위 `evictOldest()`는 `HashMap`/`ConcurrentHashMap`의 반복 순서가 삽입 순서를 보장하지 않으므로 실제로는 "임의의 한 항목 제거"에 가깝다 — 진짜 LRU가 필요하다면 `LinkedHashMap`을 `accessOrder=true`로 생성해 `removeEldestEntry`를 오버라이드하거나, `Caffeine`처럼 검증된 캐시 라이브러리를 쓰는 편이 안전하다.

## 한눈에 보는 Bridge & Flyweight 패턴

### 성능/구조 비교

| 비교 항목 | Bridge 패턴 | Flyweight 패턴 |
|----------|-----------|----------------|
| **핵심 철학** | 분리하여 정복 | 공유하여 절약 |
| **해결 문제** | 조합 폭발 (N×M 클래스) | 메모리 낭비 (대량 유사 객체) |
| **구조** | 추상화-구현 분리 | 내재-외재 상태 분리 |
| **최적화 대상** | 유연성, 확장성 | 메모리, 생성 비용 |
| **적용 시점** | 설계 초기 | 성능 최적화 단계 |
| **복잡도 증가** | 계층 구조 복잡 | 상태 관리 복잡 |
| **런타임 오버헤드** | 간접 호출 (미미) | 팩토리 조회 |
| **메모리 사용** | 클래스당 인스턴스 | 공유 + 외재 상태 |
| **초기화 비용** | 낮음 | 풀 초기화 필요 |
| **확장 비용** | 클래스 추가 | 팩토리 수정 |

### Bridge 패턴 활용 시나리오

| 시나리오 | 추상화 축 | 구현 축 | 효과 |
|----------|----------|--------|------|
| 멀티플랫폼 UI | Window, Dialog | Windows, Mac, Linux | 조합 폭발 방지 |
| 메시징 시스템 | Message 타입 | 전송 방식 (Email, SMS) | 독립적 확장 |
| 데이터 접근 | Repository | DB 드라이버 | 런타임 교체 |
| 디바이스 제어 | RemoteControl | TV, Radio, AC | 기기 독립적 제어 |

### 상태 분리 가이드 (Flyweight)

| 상태 유형 | 특징 | 처리 방식 | 예시 |
|----------|------|----------|------|
| 내재적 (Intrinsic) | 불변, 공유 가능 | Flyweight 내부 저장 | 글꼴, 텍스처, 색상 |
| 외재적 (Extrinsic) | 가변, 인스턴스별 | 파라미터로 전달 | 좌표, 크기, 회전 |

### 선택 가이드

| 판단 기준 | 권장 패턴 | 이유 |
|------|----------|------|
| N×M 클래스 조합 폭발이 예상되는가? | Bridge | 추상화-구현을 독립적 계층으로 분리 |
| 런타임에 구현체를 교체해야 하는가? | Bridge | 추상화는 구현 인터페이스만 참조 |
| 플랫폼 독립성이 필요한가? | Bridge | 구현 교체만으로 플랫폼 대응 |
| 유사 객체가 수천 개 이상 생성되는가? | Flyweight | 공유로 메모리 절약 |
| 객체 상태 대부분이 공유 가능하고 외재 상태 분리가 자연스러운가? | Flyweight | 내재적 상태만 공유, 외재적 상태는 매개변수 전달 |
| 게임 객체·문자 등을 대량 렌더링해야 하는가? | Flyweight | 공유 텍스처/글리프로 생성 비용 절감 |

### Bridge vs Strategy vs State 비교

| 비교 항목 | Bridge | Strategy | State |
|----------|--------|----------|-------|
| 목적 | 추상화/구현 분리 | 알고리즘 교체 | 상태별 행동 변경 |
| 구조 | 두 계층 구조 | 알고리즘 인터페이스 | 상태 인터페이스 |
| 변화 주체 | 클라이언트 설정 | 클라이언트 선택 | 객체 내부 전이 |
| 관계 | 영구적 연결 | 일시적 선택 | 동적 전환 |

---

## 결론: 분리와 효율성의 조화

Bridge와 Flyweight 패턴을 깊이 탐구한 결과, 이들은 **서로 다른 관점에서 시스템 최적화**를 추구하는 패턴들임을 확인했습니다.

### Bridge 패턴의 핵심 가치:

1. **구조적 유연성**: 추상화와 구현의 독립적 변화
2. **런타임 교체**: 동적인 구현체 변경 능력  
3. **조합 폭발 방지**: N×M → N+M으로 클래스 수 최적화
4. **테스트 용이성**: Mock 구현체를 통한 단위 테스트

### Flyweight 패턴의 핵심 가치:

1. **메모리 효율성**: 공유를 통한 극적인 메모리 절약
2. **성능 향상**: 객체 생성 비용 감소와 캐시 효율성
3. **확장성**: 대량 객체 처리 능력
4. **시스템 안정성**: 메모리 부족 방지

### 현대적 의미와 활용:

```
전통적 활용 → 현대적 진화

Bridge Pattern →
- 크로스 플랫폼 프레임워크
- 클라우드 멀티 프로바이더 지원
- 마이크로서비스 아키텍처
- A/B 테스트 플랫폼

Flyweight Pattern →
- 게임 엔진 최적화
- 빅데이터 메모리 관리
- 브라우저 렌더링 엔진
- IoT 디바이스 최적화
```

### 패턴 결합의 리스크와 흔한 오적용

두 패턴을 결합할 때 가장 흔히 저지르는 실수는 Flyweight 인스턴스가 Bridge의 구현체(Implementor) 참조를 필드로 붙들고 있는 것이다. 앞서 게임 렌더링 결합 예제에서 `SpriteData.render(RenderingEngine engine, ...)`가 `engine`을 매개변수로만 받고 필드로 저장하지 않은 것은 우연이 아니라 핵심 설계 결정이다. 만약 `SpriteData`가 `RenderingEngine`을 내재적 상태(필드)로 들고 있었다면, 같은 스프라이트라도 OpenGL로 그릴 때와 Vulkan으로 그릴 때 서로 다른 `SpriteData` 인스턴스가 필요해져 캐시 키에 렌더러 종류까지 포함해야 한다. 이는 텍스처 종류 몇 개면 충분했던 Flyweight 풀을 "텍스처 종류 × 렌더러 종류"로 다시 곱해 불리는 셈이어서, Bridge가 막으려던 조합 폭발이 Flyweight 캐시 내부에서 그대로 재현된다. 두 패턴을 결합할 때는 항상 "Bridge가 다루는 변화 축(구현체)이 Flyweight의 내재적 상태에 섞여 들어가지 않는가"를 점검해야 한다.

Bridge의 흔한 오적용은 구현체가 실제로는 하나뿐인데 "나중에 확장될지 모른다"는 이유만으로 추상화-구현 계층을 미리 분리해두는 경우다. SMTP 서버 하나만 쓰는 시스템에 `MessageSender` 인터페이스와 `EmailSender` 구현체를 미리 나눠두는 것은, 두 번째 구현체가 실제로 필요해지는 시점에 리팩터링으로 충분히 감당할 수 있는 비용을 미리 지불하는 것과 같다(YAGNI 위반). 앞서 `PatternDecisionGuide`가 판정 기준으로 삼은 조합 폭발 조건(N×M > N+M)은 N과 M이 모두 2 이상일 때 의미가 있으며, 구현체가 하나뿐인 M=1 상황에서는 애초에 조합 폭발이 발생할 수 없으므로 Bridge를 도입할 근거가 없다.

Flyweight의 흔한 오적용은 두 갈래로 나타난다. 첫째는 인스턴스 수가 수백 개 수준에 그치는데도 미리 팩토리·캐시 계층을 도입해, 절감되는 메모리(수십 KB 단위)보다 캐시 수명 관리·동시성 제어에 드는 코드 복잡성이 더 커지는 경우다 — `PatternDecisionGuide`의 `FLYWEIGHT_INSTANCE_THRESHOLD`처럼 명시적 임계치를 정하지 않고 "일단 캐싱해두면 좋겠지"라는 감으로 도입할 때 생긴다. 둘째는 위 오개념 교정 절에서 다룬 것과 같이, 외재적 상태를 끝까지 분리하지 못하고 가변 필드(예: 마지막으로 렌더링한 좌표, 마지막 색상)를 내재적 상태 객체에 남겨두는 경우다. 이때 캐시는 이름만 Flyweight일 뿐 실질적으로는 여러 컨텍스트가 하나의 가변 인스턴스를 공유해 서로의 상태를 덮어쓰는 버그의 근원이 된다.

Bridge와 Flyweight 패턴은 **"어떻게 더 유연하고 효율적인 시스템을 만들 것인가?"**라는 소프트웨어 엔지니어링의 영원한 질문에 대한 두 가지 다른 접근법을 제시합니다. 이들을 적절히 조합하여 활용할 때, 우리는 변화에 유연하면서도 자원을 효율적으로 사용하는 시스템을 구축할 수 있습니다.

다음 글에서는 **Observer 패턴**을 탐구하겠습니다. 객체 상태 변화를 의존 객체들에게 자동으로 통지하는 이벤트 기반 아키텍처의 시작점을 살펴보겠습니다.

---

**핵심 메시지:**
"Bridge는 변화의 축을 분리하여 유연성을 제공하고, Flyweight는 공유를 통해 효율성을 추구한다. 두 패턴 모두 복잡성 증가라는 비용을 지불하지만, 올바르게 적용하면 시스템의 확장성과 성능을 크게 향상시킬 수 있다."

## 평가 기준

**독자가 이 글을 읽은 후 달성해야 할 목표:**

- [ ] Bridge 패턴이 해결하는 조합 폭발 문제와 그 해법(추상화-구현 분리)을 설명할 수 있다
- [ ] Flyweight 패턴의 내재적/외재적 상태 분리 개념을 설명할 수 있다
- [ ] 두 패턴의 철학적 차이(분리 vs 공유)를 대비해 구분할 수 있다
- [ ] 실무에서 두 패턴을 언제 선택해야 하는지 판단 기준을 제시할 수 있다
- [ ] Bridge와 Flyweight가 결합되는 실제 사례(게임 렌더링 등)를 설명할 수 있다
- [ ] 성능/메모리 수치가 예시 값이며 실측이 아니라는 점을 구분할 수 있다