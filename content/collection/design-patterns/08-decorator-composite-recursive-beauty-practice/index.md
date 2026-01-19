---
draft: true
collection_order: 81
title: "[Design Patterns] 데코레이터와 컴포지트 패턴 실습 - 재귀적 구조의 미학"
description: "Decorator와 Composite 패턴을 통해 재귀적 구조와 동적 기능 확장을 실습합니다. 음료 주문 시스템, 파일 시스템, GUI 컴포넌트, 로깅 시스템 등의 프로젝트를 통해 객체 구조의 투명성과 확장성을 체험하고 실무에서의 강력한 설계 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-08T11:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Structural Patterns
- Recursive Patterns
- Practice
- Pattern Implementation
tags:
- Decorator Pattern Practice
- Composite Pattern Practice
- Recursive Structure
- Dynamic Enhancement
- Tree Structure
- File System Modeling
- GUI Components
- Beverage System
- Logging System
- Structural Patterns
- Design Patterns
- GoF Patterns
- Object Composition
- Transparency Principle
- Practice Project
- Hands-on Learning
- Code Implementation
- Pattern Implementation
- Software Architecture
- Flexible Design
- Extensible Design
- 데코레이터 패턴 실습
- 컴포지트 패턴 실습
- 재귀적 구조
- 동적 기능 확장
- 트리 구조
- 파일 시스템 모델링
- GUI 컴포넌트
- 음료 시스템
- 로깅 시스템
- 구조 패턴
- 디자인 패턴
- GoF 패턴
- 객체 컴포지션
- 투명성 원칙
- 실습 프로젝트
- 실습 학습
- 코드 구현
- 패턴 구현
- 소프트웨어 아키텍처
- 유연한 설계
- 확장 가능한 설계
---

이 실습에서는 Decorator와 Composite 패턴을 활용하여 동적 기능 확장과 트리 구조 객체 처리를 구현합니다.

## 실습 목표
- Decorator 패턴으로 동적 기능 확장 구현
- Composite 패턴으로 트리 구조 객체 처리
- 재귀적 구조와 투명성의 이해
- GUI 컴포넌트와 파일 시스템 모델링

## 실습 1: 음료 주문 시스템 (Decorator)

### 요구사항
다양한 토핑을 추가할 수 있는 음료 주문 시스템

### 코드 템플릿

```java
// TODO 1: Component 인터페이스 정의
public interface Beverage {
    String getDescription();
    double getCost();
    int getCalories();
    List<String> getIngredients();
}

// TODO 2: 기본 음료 구현 (ConcreteComponent)
public class Espresso implements Beverage {
    // TODO: 에스프레소 기본 구현
}

public class DarkRoast implements Beverage {
    // TODO: 다크로스트 기본 구현
}

public class HouseBlend implements Beverage {
    // TODO: 하우스 블렌드 기본 구현
}

// TODO 3: Decorator 추상 클래스
public abstract class CondimentDecorator implements Beverage {
    protected Beverage beverage;
    
    public CondimentDecorator(Beverage beverage) {
        this.beverage = beverage;
    }
    
    // TODO: 기본 위임 구현
}

// TODO 4: 구체적인 Decorator들
public class Milk extends CondimentDecorator {
    // TODO: 우유 추가 (+0.60원, +50칼로리)
}

public class Mocha extends CondimentDecorator {
    // TODO: 모카 추가 (+0.80원, +80칼로리)
}

public class Whip extends CondimentDecorator {
    // TODO: 휘핑크림 추가 (+0.70원, +60칼로리)
}

public class SoyMilk extends CondimentDecorator {
    // TODO: 두유 추가 (+0.50원, +30칼로리)
}

// TODO 5: 음료 빌더 (Decorator 패턴 + Builder 패턴)
public class BeverageBuilder {
    private Beverage beverage;
    
    public static BeverageBuilder base(Beverage baseBeverage) {
        // TODO: 기본 음료로 시작
        return new BeverageBuilder();
    }
    
    public BeverageBuilder addMilk() {
        // TODO: 우유 Decorator 추가
        return this;
    }
    
    public BeverageBuilder addMocha() {
        // TODO: 모카 Decorator 추가
        return this;
    }
    
    public Beverage build() {
        return beverage;
    }
}
```

## 실습 2: 파일 시스템 (Composite)

### 요구사항
파일과 폴더를 동일하게 처리하는 파일 시스템

### 코드 템플릿

```java
// TODO 1: Component 인터페이스
public interface FileSystemComponent {
    String getName();
    long getSize();
    void display(int depth);
    void add(FileSystemComponent component);
    void remove(FileSystemComponent component);
    List<FileSystemComponent> getChildren();
    
    // TODO: 검색 기능
    List<FileSystemComponent> search(String name);
    List<FileSystemComponent> findByExtension(String extension);
}

// TODO 2: Leaf 구현 (File)
public class File implements FileSystemComponent {
    private final String name;
    private final long size;
    private final String extension;
    private final LocalDateTime lastModified;
    
    // TODO: 파일 구현 (add, remove는 UnsupportedOperationException)
}

// TODO 3: Composite 구현 (Directory)
public class Directory implements FileSystemComponent {
    private final String name;
    private final List<FileSystemComponent> children;
    private final LocalDateTime created;
    
    // TODO: 디렉토리 구현 (재귀적 처리)
    
    @Override
    public long getSize() {
        // TODO: 모든 하위 파일들의 크기 합계
        return 0;
    }
    
    @Override
    public void display(int depth) {
        // TODO: 트리 구조로 출력
    }
    
    @Override
    public List<FileSystemComponent> search(String name) {
        // TODO: 재귀적 검색
        return new ArrayList<>();
    }
}

// TODO 4: 파일 시스템 유틸리티
public class FileSystemUtils {
    // TODO: 전체 크기 계산
    public static long getTotalSize(FileSystemComponent component) {
        return 0;
    }
    
    // TODO: 깊이 우선 탐색
    public static void walkFileSystem(FileSystemComponent root, 
                                    Consumer<FileSystemComponent> visitor) {
        // TODO: 방문자 패턴과 결합
    }
    
    // TODO: 경로 찾기
    public static String getPath(FileSystemComponent target, 
                               FileSystemComponent root) {
        return "";
    }
}
```

## 실습 3: GUI 컴포넌트 시스템

### 코드 템플릿

```java
// TODO 1: GUI Component (Composite)
public abstract class UIComponent {
    protected String name;
    protected int x, y, width, height;
    protected boolean visible = true;
    
    public abstract void render(Graphics graphics);
    public abstract void add(UIComponent component);
    public abstract void remove(UIComponent component);
    
    // TODO: 이벤트 처리
    public void handleClick(int x, int y) {
        if (contains(x, y)) {
            onClick();
        }
    }
    
    protected abstract void onClick();
    protected boolean contains(int x, int y) {
        return x >= this.x && x <= this.x + width && 
               y >= this.y && y <= this.y + height;
    }
}

// TODO 2: 기본 컴포넌트들 (Leaf)
public class Button extends UIComponent {
    private String text;
    private Color backgroundColor;
    
    // TODO: 버튼 렌더링 및 이벤트 처리
}

public class Label extends UIComponent {
    private String text;
    private Font font;
    
    // TODO: 라벨 렌더링
}

// TODO 3: 컨테이너 컴포넌트들 (Composite)
public class Panel extends UIComponent {
    private final List<UIComponent> children = new ArrayList<>();
    private Color backgroundColor;
    
    // TODO: 패널 렌더링 (자식들 포함)
    
    @Override
    public void handleClick(int x, int y) {
        // TODO: 자식 컴포넌트들에게 이벤트 전파
    }
}

// TODO 4: Decorator로 기능 확장
public abstract class UIComponentDecorator extends UIComponent {
    protected UIComponent component;
    
    // TODO: 기본 위임 구현
}

public class BorderDecorator extends UIComponentDecorator {
    private final Color borderColor;
    private final int borderWidth;
    
    // TODO: 테두리 그리기
}

public class ScrollDecorator extends UIComponentDecorator {
    private int scrollX, scrollY;
    
    // TODO: 스크롤 기능 추가
}
```

## 실습 4: 로깅 시스템 (Decorator + Composite)

### 코드 템플릿

```java
// TODO 1: Logger 인터페이스
public interface Logger {
    void log(LogLevel level, String message);
    void log(LogLevel level, String message, Throwable throwable);
}

// TODO 2: 기본 Logger들 (ConcreteComponent)
public class ConsoleLogger implements Logger {
    // TODO: 콘솔 출력
}

public class FileLogger implements Logger {
    private final String filename;
    // TODO: 파일 출력
}

// TODO 3: Logger Decorator들
public class TimestampDecorator implements Logger {
    private final Logger logger;
    
    // TODO: 타임스탬프 추가
}

public class FilterDecorator implements Logger {
    private final Logger logger;
    private final LogLevel minLevel;
    
    // TODO: 로그 레벨 필터링
}

// TODO 4: Composite Logger
public class CompositeLogger implements Logger {
    private final List<Logger> loggers;
    
    // TODO: 여러 로거에 동시 출력
}
```

## 체크리스트

### Decorator 패턴
- [ ] 기본 구성요소와 장식자 구현
- [ ] 동적 기능 추가/제거
- [ ] 투명성 확보 (인터페이스 일관성)
- [ ] 여러 장식자 조합 테스트

### Composite 패턴
- [ ] Leaf와 Composite 구현
- [ ] 재귀적 구조 처리
- [ ] 트리 순회 알고리즘
- [ ] 투명성 vs 안전성 고려

### 패턴 조합
- [ ] Decorator + Composite 결합
- [ ] Builder 패턴과 함께 사용
- [ ] Visitor 패턴으로 확장
- [ ] 성능 최적화 (캐싱, 지연 로딩)

## 추가 도전

1. **Stream Decorator**: Java Stream API 스타일 체이닝
2. **Cached Composite**: 계산 결과 캐싱
3. **Async Decorator**: 비동기 처리 장식자
4. **Reactive Composite**: 변경 사항 자동 전파

## 실무 적용

### Decorator 활용 사례
- HTTP 클라이언트 미들웨어
- 데이터베이스 커넥션 래핑
- 스트림 처리 파이프라인
- AOP (Aspect-Oriented Programming)

### Composite 활용 사례
- GUI 컴포넌트 계층
- 조직도/메뉴 구조
- 수식 파서 (AST)
- 파일 시스템 모델링

---

**핵심 포인트**: Decorator는 수직적 기능 확장을, Composite는 수평적 구조 관리를 담당합니다. 두 패턴 모두 재귀적 구조를 통해 강력한 확장성과 유연성을 제공합니다. 