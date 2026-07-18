---
draft: true
collection_order: 81
title: "[Design Patterns] 데코레이터와 컴포지트 패턴 실습 - 재귀적 구조의 미학"
slug: "decorator-composite-recursive-beauty-practice"
description: "Decorator와 Composite 패턴을 통해 재귀적 구조와 동적 기능 확장을 실습합니다. 음료 주문 시스템, 파일 시스템, GUI 컴포넌트, 로깅 시스템 등의 프로젝트를 통해 객체 구조의 투명성과 확장성을 체험하고 실무에서의 강력한 설계 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-08T11:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Structural Patterns
- Recursive Patterns
- Practice
- Pattern Implementation
tags:
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Tutorial(튜토리얼)
- Implementation(구현)
- Software-Architecture(소프트웨어아키텍처)
- Structural-Pattern
- Decorator
- Recursion(재귀)
- Tree(트리)
- Composition(합성)
- OOP(객체지향)
- Interface(인터페이스)
- Abstraction(추상화)
- Best-Practices
- Code-Quality(코드품질)
- Maintainability
- Readability
- Refactoring(리팩토링)
- Testing(테스트)
- Guide(가이드)
- Case-Study
- Advanced
- Java
- File-System
- Modularity
- SOLID
---

이 실습에서는 Decorator와 Composite 패턴을 활용하여 동적 기능 확장과 트리 구조 객체 처리를 구현합니다.

두 패턴은 모두 "재귀적 구조"를 사용하지만 재귀가 향하는 방향이 다릅니다. Decorator는 하나의 객체를 감싸고 또 감싸는 방식으로 안쪽을 향해 재귀하며 기능을 층층이 쌓고(수직적 확장), Composite는 하나의 노드가 여러 자식을 갖고 각 자식이 다시 트리가 될 수 있는 방식으로 바깥을 향해 재귀하며 구조를 표현합니다(수평·계층적 확장). 아래 실습들은 이 두 재귀 방향을 각각 별도로 다룬 뒤, 마지막 로깅 시스템에서 두 패턴을 함께 조합해봅니다.

## 실습 목표
- 실습 1에서 `Milk`, `Mocha` 등 서로 다른 순서로 감싼 두 `Beverage` 조합의 `getCost()` 결과가 실제로 다르게 나오는 경우를 하나 이상 코드로 재현할 수 있다.
- 실습 2에서 3단계 이상 중첩된 `Directory` 트리에 대해 `getSize()`가 하위 트리 전체를 재귀적으로 합산함을 테스트로 검증할 수 있다.
- 실습 3, 4에서 Composite로 구성한 트리의 특정 노드에만 Decorator를 씌워, 트리 전체가 아닌 해당 노드만 동작이 바뀌는 것을 보일 수 있다.
- `File.add()`처럼 Leaf에 대한 부적절한 호출이 컴파일 타임이 아닌 런타임 예외로만 걸러지는 지점을 최소 1곳 지적할 수 있다.

## 실습 1: 음료 주문 시스템 (Decorator)

### 왜 Decorator인가

토핑 조합은 "우유만", "우유+모카", "두유+휘핑+모카"처럼 경우의 수가 조합적으로 늘어납니다. 토핑마다 서브클래스를 만드는 상속 방식은 조합의 수만큼 클래스가 폭발적으로 늘어나 유지보수가 불가능해집니다. Decorator는 토핑 하나를 클래스 하나로 만들고 런타임에 필요한 만큼 겹쳐 씌우는 방식으로, 새 토핑을 추가해도 기존 클래스를 전혀 건드리지 않고 조합의 자유도를 그대로 유지합니다.

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
    @Override
    public String getDescription() {
        return "에스프레소";
    }

    @Override
    public double getCost() {
        return 1.99;
    }

    @Override
    public int getCalories() {
        return 5;
    }

    @Override
    public List<String> getIngredients() {
        return new ArrayList<>(List.of("에스프레소 원두"));
    }
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

### 왜 Composite인가

파일 탐색기는 "파일 하나를 더블클릭"하는 것과 "폴더를 더블클릭해 들어가는" 것을 사용자가 같은 방식으로 다룰 수 있어야 합니다. `File`과 `Directory`를 서로 다른 타입으로 다루면 트리를 순회하는 코드마다 `instanceof` 분기가 필요해집니다. Composite는 `FileSystemComponent`라는 공통 인터페이스로 Leaf(File)와 Composite(Directory)를 통일해, 클라이언트 코드가 대상이 파일인지 폴더인지 신경 쓰지 않고 재귀적으로 트리를 다룰 수 있게 합니다.

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

    public File(String name, long size, String extension, LocalDateTime lastModified) {
        this.name = name;
        this.size = size;
        this.extension = extension;
        this.lastModified = lastModified;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public long getSize() {
        return size;
    }

    @Override
    public void display(int depth) {
        // TODO: depth만큼 들여쓰기 후 "- " + name 출력
    }

    @Override
    public void add(FileSystemComponent component) {
        throw new UnsupportedOperationException("파일에는 자식을 추가할 수 없습니다: " + name);
    }

    @Override
    public void remove(FileSystemComponent component) {
        throw new UnsupportedOperationException("파일에는 자식을 제거할 수 없습니다: " + name);
    }

    @Override
    public List<FileSystemComponent> getChildren() {
        return Collections.emptyList();
    }

    @Override
    public List<FileSystemComponent> search(String name) {
        // TODO: 이름이 일치하면 자기 자신을 담은 리스트, 아니면 빈 리스트를 반환 (재귀의 기저 조건)
        return Collections.emptyList();
    }

    @Override
    public List<FileSystemComponent> findByExtension(String extension) {
        // TODO: 확장자가 일치하면 자기 자신을 담은 리스트, 아니면 빈 리스트를 반환
        return Collections.emptyList();
    }
}

// TODO 3: Composite 구현 (Directory)
public class Directory implements FileSystemComponent {
    private final String name;
    private final List<FileSystemComponent> children;
    private final LocalDateTime created;

    public Directory(String name) {
        this.name = name;
        this.children = new ArrayList<>();
        this.created = LocalDateTime.now();
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public void add(FileSystemComponent component) {
        children.add(component);
    }

    @Override
    public void remove(FileSystemComponent component) {
        children.remove(component);
    }

    @Override
    public List<FileSystemComponent> getChildren() {
        return children;
    }

    @Override
    public long getSize() {
        // 재귀적 처리: 각 자식이 File이면 자신의 크기를, Directory면 다시 getSize()를 호출해
        // 하위 트리 전체를 합산한다. 재귀의 기저 조건은 File.getSize()가 담당한다.
        long total = 0;
        for (FileSystemComponent child : children) {
            total += child.getSize();
        }
        return total;
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

    @Override
    public List<FileSystemComponent> findByExtension(String extension) {
        // TODO: 자식들을 순회하며 재귀적으로 확장자가 일치하는 File을 모두 수집
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

### 왜 Composite와 Decorator를 함께 쓰는가

GUI는 두 가지 문제를 동시에 갖습니다. 첫째, `Panel`이 `Button`과 다른 `Panel`을 자식으로 담는 계층 구조라는 점(Composite의 영역)이고, 둘째, 이미 만들어진 컴포넌트에 테두리나 스크롤 같은 부가 기능을 씌우고 싶다는 점(Decorator의 영역)입니다. 이 실습에서는 `UIComponent`라는 하나의 추상화 위에 Composite로 트리를 구성하고, 그 위에 다시 Decorator로 개별 컴포넌트를 감싸는 이중 구조를 다룹니다.

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

### 왜 Decorator와 Composite를 함께 쓰는가

로그에 타임스탬프를 붙이거나 특정 레벨 이하를 걸러내는 기능은 `Logger` 하나를 감싸는 Decorator로 자연스럽게 표현되고, 콘솔과 파일에 동시에 로그를 남기고 싶다는 요구는 여러 `Logger`를 하나처럼 다루는 Composite(`CompositeLogger`)로 표현됩니다. 두 요구를 한 인터페이스(`Logger`) 위에서 자유롭게 조합할 수 있다는 것이 이 실습의 핵심입니다. 예를 들어 `CompositeLogger`로 콘솔+파일 로거를 묶은 뒤, 그 결과를 다시 `TimestampDecorator`로 감싸면 "타임스탬프가 붙은 로그를 콘솔과 파일에 동시에" 남기는 동작을 코드 수정 없이 조립만으로 얻을 수 있습니다.

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
- [ ] 기본 구성요소와 장식자 구현 — `Espresso` 같은 ConcreteComponent 없이는 감쌀 대상 자체가 없어 체인을 시작할 수 없다.
- [ ] 동적 기능 추가/제거 — 상속으로는 컴파일 타임에 조합이 고정되므로, 런타임에 토핑을 바꾸는 요구는 Decorator로만 자연스럽게 풀린다.
- [ ] 투명성 확보 (인터페이스 일관성) — `CondimentDecorator`가 `Beverage`를 구현하지 않으면 감싼 결과를 다시 감쌀 수 없어 체인이 끊긴다.
- [ ] 여러 장식자 조합 테스트 — 감싸는 순서에 따라 `getCost()` 결과가 달라질 수 있으므로 순서 의존성을 실제로 확인해야 한다.

### Composite 패턴
- [ ] Leaf와 Composite 구현 — `File`(Leaf)과 `Directory`(Composite)가 없으면 트리의 끝단과 중간 노드를 구분해 다룰 대상이 없다.
- [ ] 재귀적 구조 처리 — `Directory.getSize()`가 자식의 `getSize()`를 재귀 호출하지 않으면 하위 트리 크기를 합산할 수 없다.
- [ ] 트리 순회 알고리즘 — `display()`, `search()` 같은 깊이 우선 순회 없이는 트리 전체를 탐색할 수 없다.
- [ ] 투명성 vs 안전성 고려 — `File.add()`를 인터페이스에 남겨두면(투명성) 호출 자체는 막지 못하고 런타임 예외로만(안전성 부족) 방어할 수 있다는 트레이드오프를 확인해야 한다.

### 패턴 조합
- [ ] Decorator + Composite 결합 — 실습 3, 4처럼 트리 구조(Composite) 안의 개별 노드에 부가 기능(Decorator)을 씌우는 요구가 동시에 있을 때만 결합의 가치가 생긴다.
- [ ] Builder 패턴과 함께 사용 — `BeverageBuilder`처럼 여러 Decorator를 순서대로 씌우는 코드를 메서드 체이닝으로 감추면 호출부의 가독성이 올라간다.
- [ ] Visitor 패턴으로 확장 — 트리 구조를 바꾸지 않고 새 연산(예: 파일 통계 집계)을 추가하려면 각 노드에 `accept()`를 더하는 Visitor가 필요하다.
- [ ] 성능 최적화 (캐싱, 지연 로딩) — `getSize()`처럼 매 호출마다 전체 트리를 재귀 순회하는 연산은 트리가 크면 반복 비용이 커지므로 캐싱 여부를 검토해야 한다.

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

## 선택 기준과 한계

"기능을 조합해서 늘려야 하는가, 구조를 계층으로 표현해야 하는가"가 두 패턴을 가르는 기본 질문입니다. 같은 종류의 객체 하나에 여러 부가 기능을 씌우고 싶다면 Decorator를, 서로 다른 개체들이 부분-전체 관계를 이루고 그 관계를 재귀적으로 순회해야 한다면 Composite를 선택합니다. 실습 3, 4처럼 "계층 구조 안의 개별 노드에 부가 기능을 씌우고 싶다"는 요구가 동시에 있을 때만 두 패턴을 함께 쓰며, 둘 중 하나만으로 요구를 만족한다면 나머지 패턴을 억지로 끼워 넣을 필요는 없습니다.

두 패턴 모두 한계가 뚜렷합니다. Decorator 체인이 길어지면 디버거로 스택을 추적하기 어려워지고, 어떤 순서로 감쌌는지에 따라 결과가 달라지므로(`Milk` 이후 `Mocha`를 씌우는 것과 그 반대는 가격 계산 순서가 다를 수 있음) 체인 구성 자체가 암묵적 지식이 됩니다. Composite는 깊은 트리에서 재귀 호출이 스택 프레임을 소비하므로, `getSize()`처럼 매 호출마다 자식을 순회하는 연산은 트리가 매우 깊거나 노드 수가 많을 때 반복적(iterative) 순회로 바꾸는 것을 고려해야 합니다. 두 패턴 다 "인터페이스를 통일해 다형성으로 처리한다"는 이점의 대가로 타입 안전성을 일부 포기한다는 점도 감안해야 합니다. 예를 들어 `Directory.add()`는 컴파일 타임에는 막을 수 없고 `File.add()` 호출 시 런타임 예외로만 막을 수 있습니다.

---

**핵심 포인트**: Decorator는 수직적 기능 확장을, Composite는 수평적 구조 관리를 담당합니다. 두 패턴 모두 재귀적 구조를 통해 강력한 확장성과 유연성을 제공합니다. 