---
collection_order: 160
draft: true
title: "[Design Patterns] 메멘토와 비지터: 상태 보존과 연산 분리"
description: "객체의 상태를 캡슐화하여 저장하는 Memento 패턴과 구조와 연산을 분리하는 Visitor 패턴의 고급 활용법을 탐구합니다. Undo/Redo 시스템, 상태 스냅샷, 이중 디스패치, 객체 구조 순회 등 복잡한 상태 관리와 연산 확장을 위한 전문가 수준의 설계 기법을 학습합니다."
date: 2024-12-16T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Behavioral Patterns
- State Management
- Operation Extension
tags:
- Memento Pattern
- Visitor Pattern
- State Preservation
- Undo Redo System
- State Snapshot
- Double Dispatch
- Object Structure Traversal
- Behavioral Patterns
- Design Patterns
- GoF Patterns
- State Encapsulation
- Operation Separation
- Caretaker Pattern
- Originator Pattern
- Element Visitor
- Composite Visitor
- Tree Traversal
- AST Processing
- Document History
- Version Control
- State Rollback
- Time Travel Debugging
- External Operations
- Structure Independence
- Algorithm Extension
- Open Closed Principle
- Polymorphic Dispatch
- Type Safety
- Compiler Design
- Data Structure Processing
- Report Generation
- Export Operations
- 메멘토 패턴
- 비지터 패턴
- 상태 보존
- 실행 취소 재실행 시스템
- 상태 스냅샷
- 이중 디스패치
- 객체 구조 순회
- 행동 패턴
- 디자인 패턴
- GoF 패턴
- 상태 캡슐화
- 연산 분리
- 관리자 패턴
- 생성자 패턴
- 요소 비지터
- 복합 비지터
- 트리 순회
- AST 처리
- 문서 히스토리
- 버전 제어
- 상태 롤백
- 시간 여행 디버깅
- 외부 연산
- 구조 독립성
- 알고리즘 확장
- 개방 폐쇄 원칙
- 다형적 디스패치
- 타입 안전성
- 컴파일러 설계
- 자료구조 처리
- 보고서 생성
- 내보내기 연산
---

# Memento와 Visitor - 상태 보존과 연산 분리

## **서론: 시간을 저장하고 기능을 분리하다**

> *"Memento는 시간을 객체로 만들어 과거로 돌아갈 수 있게 하고, Visitor는 구조와 연산을 분리하여 무한한 확장을 가능하게 한다."*

소프트웨어 개발에서 우리는 두 가지 근본적인 도전에 직면합니다:

1. **어떻게 객체의 과거 상태를 안전하게 보존하고 복원할 것인가?** (시간적 캡슐화)
2. **어떻게 객체 구조를 변경하지 않고 새로운 연산을 추가할 것인가?** (연산의 확장성)

**Memento 패턴**은 **"캡슐화를 유지하면서 객체의 상태를 저장하고 복원"** 할 수 있게 합니다. 마치 시간을 되돌리는 마법과 같습니다.

**Visitor 패턴**은 **"객체 구조와 연산을 분리"** 하여 기존 클래스를 수정하지 않고도 새로운 기능을 추가할 수 있게 합니다.

이 두 패턴은 **객체지향 프로그래밍의 한계를 창의적으로 극복**하는 대표적인 예시입니다:
- Memento: **시간적 복잡성** 관리
- Visitor: **기능적 복잡성** 관리

## **1. Memento 패턴 - 시간을 되돌리는 마법**

### **1.1 Memento 패턴의 핵심 철학**

Memento 패턴의 핵심은 **"캡슐화를 깨지 않으면서 객체의 내부 상태를 외부에 저장"** 하는 것입니다. 이는 시간 여행을 가능하게 하는 마법 같은 패턴입니다.

```java
// ❌ Memento 패턴 없이 구현한다면?
class BadDocumentEditor {
    private String content;
    private int cursorPosition;
    private List<String> contentHistory = new ArrayList<>();
    private List<Integer> positionHistory = new ArrayList<>();
    
    public void saveState() {
        // 😱 내부 상태를 직접 노출
        contentHistory.add(content);
        positionHistory.add(cursorPosition);
    }
    
    public void undo() {
        if (!contentHistory.isEmpty()) {
            // 😱 캡슐화 깨짐, 상태 동기화 문제
            content = contentHistory.remove(contentHistory.size() - 1);
            cursorPosition = positionHistory.remove(positionHistory.size() - 1);
        }
    }
    
    // 😱 새로운 상태가 추가될 때마다 모든 히스토리 관련 코드 수정
    // 😱 외부에서 히스토리에 직접 접근 가능 (캡슐화 위반)
    // 😱 메모리 누수 위험 (히스토리 무제한 증가)
}
```

### **1.2 Memento 패턴으로 우아하게 해결**

```java
// ✅ Memento 패턴의 우아함
// 1. Memento 인터페이스 (Marker Interface)
interface DocumentMemento {
    // 외부에서는 구체적인 내용을 알 수 없음
    LocalDateTime getTimestamp();
    String getDescription();
}

// 2. Originator - 상태를 가진 원본 객체
class DocumentEditor {
    private StringBuilder content;
    private int cursorPosition;
    private Map<String, Object> properties;
    private LocalDateTime lastModified;
    
    public DocumentEditor() {
        this.content = new StringBuilder();
        this.cursorPosition = 0;
        this.properties = new HashMap<>();
        this.lastModified = LocalDateTime.now();
    }
    
    // 문서 편집 메서드들
    public void insertText(String text) {
        content.insert(cursorPosition, text);
        cursorPosition += text.length();
        lastModified = LocalDateTime.now();
    }
    
    public void deleteText(int length) {
        if (length > 0 && cursorPosition >= length) {
            content.delete(cursorPosition - length, cursorPosition);
            cursorPosition -= length;
            lastModified = LocalDateTime.now();
        }
    }
    
    public void setCursorPosition(int position) {
        if (position >= 0 && position <= content.length()) {
            this.cursorPosition = position;
        }
    }
    
    public void setProperty(String key, Object value) {
        properties.put(key, value);
        lastModified = LocalDateTime.now();
    }
    
    // Memento 생성 - 현재 상태를 저장
    public DocumentMemento createMemento() {
        return new ConcreteDocumentMemento(
            content.toString(),
            cursorPosition,
            new HashMap<>(properties),
            lastModified
        );
    }
    
    // Memento로부터 상태 복원
    public void restoreFromMemento(DocumentMemento memento) {
        if (memento instanceof ConcreteDocumentMemento) {
            ConcreteDocumentMemento concreteMemento = (ConcreteDocumentMemento) memento;
            
            this.content = new StringBuilder(concreteMemento.content);
            this.cursorPosition = concreteMemento.cursorPosition;
            this.properties = new HashMap<>(concreteMemento.properties);
            this.lastModified = concreteMemento.lastModified;
            
            System.out.println("✅ Document restored to state: " + memento.getDescription());
        }
    }
    
    // Nested Class로 Memento 구현 (캡슐화 보장)
    private static class ConcreteDocumentMemento implements DocumentMemento {
        private final String content;
        private final int cursorPosition;
        private final Map<String, Object> properties;
        private final LocalDateTime lastModified;
        private final LocalDateTime snapshotTime;
        
        private ConcreteDocumentMemento(String content, int cursorPosition,
                                      Map<String, Object> properties, LocalDateTime lastModified) {
            this.content = content;
            this.cursorPosition = cursorPosition;
            this.properties = properties;
            this.lastModified = lastModified;
            this.snapshotTime = LocalDateTime.now();
        }
        
        @Override
        public LocalDateTime getTimestamp() {
            return snapshotTime;
        }
        
        @Override
        public String getDescription() {
            return String.format("Content: %d chars, Cursor: %d, Modified: %s",
                               content.length(), cursorPosition, 
                               lastModified.format(DateTimeFormatter.ofPattern("HH:mm:ss")));
        }
    }
    
    // 현재 상태 출력
    public void printStatus() {
        System.out.printf("Content: '%s' | Cursor: %d | Length: %d\n",
                         content.toString(), cursorPosition, content.length());
    }
    
    public String getContent() {
        return content.toString();
    }
    
    public int getCursorPosition() {
        return cursorPosition;
    }
}

// 3. Caretaker - Memento 관리자
class DocumentHistory {
    private final Deque<DocumentMemento> undoStack;
    private final Deque<DocumentMemento> redoStack;
    private final int maxHistorySize;
    private final DocumentEditor editor;
    
    public DocumentHistory(DocumentEditor editor, int maxHistorySize) {
        this.editor = editor;
        this.maxHistorySize = maxHistorySize;
        this.undoStack = new ArrayDeque<>();
        this.redoStack = new ArrayDeque<>();
    }
    
    // 현재 상태를 히스토리에 저장
    public void saveState() {
        DocumentMemento memento = editor.createMemento();
        undoStack.addLast(memento);
        redoStack.clear(); // 새로운 상태 저장 시 redo 스택 클리어
        
        // 히스토리 크기 제한
        while (undoStack.size() > maxHistorySize) {
            undoStack.removeFirst();
        }
        
        System.out.println("💾 State saved: " + memento.getDescription());
    }
    
    // Undo 수행
    public boolean undo() {
        if (undoStack.isEmpty()) {
            System.out.println("❌ No more states to undo");
            return false;
        }
        
        // 현재 상태를 redo 스택에 저장
        redoStack.addLast(editor.createMemento());
        
        // 이전 상태로 복원
        DocumentMemento previousState = undoStack.removeLast();
        editor.restoreFromMemento(previousState);
        
        System.out.println("↶ Undo performed");
        return true;
    }
    
    // Redo 수행
    public boolean redo() {
        if (redoStack.isEmpty()) {
            System.out.println("❌ No more states to redo");
            return false;
        }
        
        // 현재 상태를 undo 스택에 저장
        undoStack.addLast(editor.createMemento());
        
        // redo 상태로 복원
        DocumentMemento redoState = redoStack.removeLast();
        editor.restoreFromMemento(redoState);
        
        System.out.println("↷ Redo performed");
        return true;
    }
    
    // 히스토리 정보
    public void printHistory() {
        System.out.println("=== Document History ===");
        System.out.println("Undo available: " + undoStack.size());
        System.out.println("Redo available: " + redoStack.size());
        
        if (!undoStack.isEmpty()) {
            System.out.println("Recent states:");
            int count = 0;
            for (DocumentMemento memento : undoStack) {
                if (count++ >= 3) break; // 최근 3개만 표시
                System.out.println("  " + memento.getDescription());
            }
        }
    }
    
    public boolean canUndo() {
        return !undoStack.isEmpty();
    }
    
    public boolean canRedo() {
        return !redoStack.isEmpty();
    }
    
    public void clearHistory() {
        undoStack.clear();
        redoStack.clear();
        System.out.println("🗑️ History cleared");
    }
}

// 4. 고급 Memento - 압축 및 최적화
class OptimizedDocumentMemento implements DocumentMemento {
    private final byte[] compressedContent;
    private final int cursorPosition;
    private final LocalDateTime timestamp;
    private final String description;
    
    public OptimizedDocumentMemento(String content, int cursorPosition) {
        this.compressedContent = compressString(content);
        this.cursorPosition = cursorPosition;
        this.timestamp = LocalDateTime.now();
        this.description = String.format("Compressed: %d bytes, Cursor: %d",
                                        compressedContent.length, cursorPosition);
    }
    
    public String getDecompressedContent() {
        return decompressString(compressedContent);
    }
    
    public int getCursorPosition() {
        return cursorPosition;
    }
    
    @Override
    public LocalDateTime getTimestamp() {
        return timestamp;
    }
    
    @Override
    public String getDescription() {
        return description;
    }
    
    // 간단한 압축 시뮬레이션
    private byte[] compressString(String content) {
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            GZIPOutputStream gzos = new GZIPOutputStream(baos);
            gzos.write(content.getBytes(StandardCharsets.UTF_8));
            gzos.close();
            return baos.toByteArray();
        } catch (Exception e) {
            return content.getBytes(StandardCharsets.UTF_8);
        }
    }
    
    private String decompressString(byte[] compressed) {
        try {
            ByteArrayInputStream bais = new ByteArrayInputStream(compressed);
            GZIPInputStream gzis = new GZIPInputStream(bais);
            return new String(gzis.readAllBytes(), StandardCharsets.UTF_8);
        } catch (Exception e) {
            return new String(compressed, StandardCharsets.UTF_8);
        }
    }
}

// 사용 예시
class MementoPatternDemo {
    public static void main(String[] args) {
        DocumentEditor editor = new DocumentEditor();
        DocumentHistory history = new DocumentHistory(editor, 10);
        
        System.out.println("=== Document Editor Demo ===\n");
        
        // 초기 상태 저장
        history.saveState();
        
        // 텍스트 편집
        editor.insertText("Hello");
        editor.printStatus();
        history.saveState();
        
        editor.insertText(" World");
        editor.printStatus();
        history.saveState();
        
        editor.setCursorPosition(5);
        editor.insertText(" Beautiful");
        editor.printStatus();
        history.saveState();
        
        // 히스토리 출력
        System.out.println();
        history.printHistory();
        
        // Undo 테스트
        System.out.println("\n=== Undo/Redo Test ===");
        
        history.undo();
        editor.printStatus();
        
        history.undo();
        editor.printStatus();
        
        history.redo();
        editor.printStatus();
        
        // 새로운 편집 (redo 스택 클리어 테스트)
        editor.insertText("!");
        editor.printStatus();
        
        System.out.println("\nTrying to redo after new edit:");
        history.redo(); // 실패해야 함
        
        System.out.println();
        history.printHistory();
    }
}
```

## **2. Visitor 패턴 - 연산의 외부화**

### **2.1 Visitor 패턴의 핵심 철학**

Visitor 패턴은 **"객체 구조와 연산을 분리"** 하여 기존 클래스를 수정하지 않고도 새로운 기능을 추가할 수 있게 합니다. 이는 **개방-폐쇄 원칙**의 완벽한 구현입니다.

```java
// ❌ Visitor 패턴 없이 구현한다면?
abstract class BadShape {
    // 😱 새로운 연산을 추가할 때마다 모든 Shape 클래스 수정
    public abstract double calculateArea();
    public abstract void draw();
    public abstract String exportToSVG();
    public abstract void applyTexture();
    // 😱 계속 메서드가 추가됨... 개방-폐쇄 원칙 위배
}

class BadCircle extends BadShape {
    // 😱 모든 연산이 Circle 클래스 안에 존재
    @Override
    public double calculateArea() { /* 구현 */ }
    
    @Override
    public void draw() { /* 구현 */ }
    
    @Override
    public String exportToSVG() { /* 구현 */ }
    
    @Override
    public void applyTexture() { /* 구현 */ }
    
    // 😱 새로운 연산 추가 시 모든 Shape 클래스 수정 필요
}
```

### **2.2 Visitor 패턴으로 우아하게 해결**

```java
// ✅ Visitor 패턴의 우아함
// 1. Visitor 인터페이스
interface ShapeVisitor {
    void visit(Circle circle);
    void visit(Rectangle rectangle);
    void visit(Triangle triangle);
    void visit(CompoundShape compoundShape);
}

// 2. Element 인터페이스
interface Shape {
    void accept(ShapeVisitor visitor);
    String getName();
}

// 3. Concrete Elements
class Circle implements Shape {
    private final double radius;
    private final Point center;
    
    public Circle(double radius, Point center) {
        this.radius = radius;
        this.center = center;
    }
    
    @Override
    public void accept(ShapeVisitor visitor) {
        visitor.visit(this); // Double Dispatch
    }
    
    @Override
    public String getName() {
        return "Circle";
    }
    
    public double getRadius() { return radius; }
    public Point getCenter() { return center; }
}

class Rectangle implements Shape {
    private final double width;
    private final double height;
    private final Point topLeft;
    
    public Rectangle(double width, double height, Point topLeft) {
        this.width = width;
        this.height = height;
        this.topLeft = topLeft;
    }
    
    @Override
    public void accept(ShapeVisitor visitor) {
        visitor.visit(this);
    }
    
    @Override
    public String getName() {
        return "Rectangle";
    }
    
    public double getWidth() { return width; }
    public double getHeight() { return height; }
    public Point getTopLeft() { return topLeft; }
}

class Triangle implements Shape {
    private final Point[] vertices;
    
    public Triangle(Point p1, Point p2, Point p3) {
        this.vertices = new Point[]{p1, p2, p3};
    }
    
    @Override
    public void accept(ShapeVisitor visitor) {
        visitor.visit(this);
    }
    
    @Override
    public String getName() {
        return "Triangle";
    }
    
    public Point[] getVertices() { return vertices.clone(); }
}

// Composite 패턴과 결합
class CompoundShape implements Shape {
    private final List<Shape> children;
    private final String name;
    
    public CompoundShape(String name) {
        this.name = name;
        this.children = new ArrayList<>();
    }
    
    public void addShape(Shape shape) {
        children.add(shape);
    }
    
    @Override
    public void accept(ShapeVisitor visitor) {
        visitor.visit(this);
        // 자식 Shape들도 방문
        for (Shape child : children) {
            child.accept(visitor);
        }
    }
    
    @Override
    public String getName() {
        return name;
    }
    
    public List<Shape> getChildren() {
        return new ArrayList<>(children);
    }
}

// 4. Concrete Visitors - 다양한 연산 구현
class AreaCalculatorVisitor implements ShapeVisitor {
    private double totalArea = 0;
    private final Map<String, Double> areaByShape = new HashMap<>();
    
    @Override
    public void visit(Circle circle) {
        double area = Math.PI * circle.getRadius() * circle.getRadius();
        totalArea += area;
        areaByShape.put("Circle_" + System.identityHashCode(circle), area);
        
        System.out.printf("📐 Circle area: %.2f (radius: %.2f)\n", area, circle.getRadius());
    }
    
    @Override
    public void visit(Rectangle rectangle) {
        double area = rectangle.getWidth() * rectangle.getHeight();
        totalArea += area;
        areaByShape.put("Rectangle_" + System.identityHashCode(rectangle), area);
        
        System.out.printf("📐 Rectangle area: %.2f (%.2f x %.2f)\n", 
                         area, rectangle.getWidth(), rectangle.getHeight());
    }
    
    @Override
    public void visit(Triangle triangle) {
        // 신발끈 공식 (Shoelace formula) 사용
        Point[] vertices = triangle.getVertices();
        double area = Math.abs(
            (vertices[0].x * (vertices[1].y - vertices[2].y) +
             vertices[1].x * (vertices[2].y - vertices[0].y) +
             vertices[2].x * (vertices[0].y - vertices[1].y)) / 2.0
        );
        
        totalArea += area;
        areaByShape.put("Triangle_" + System.identityHashCode(triangle), area);
        
        System.out.printf("📐 Triangle area: %.2f\n", area);
    }
    
    @Override
    public void visit(CompoundShape compoundShape) {
        System.out.printf("📐 Compound shape '%s' contains %d children\n",
                         compoundShape.getName(), compoundShape.getChildren().size());
    }
    
    public double getTotalArea() {
        return totalArea;
    }
    
    public Map<String, Double> getAreaByShape() {
        return new HashMap<>(areaByShape);
    }
    
    public void reset() {
        totalArea = 0;
        areaByShape.clear();
    }
}

class DrawingVisitor implements ShapeVisitor {
    private final StringBuilder canvas = new StringBuilder();
    private int indentLevel = 0;
    
    @Override
    public void visit(Circle circle) {
        addIndent();
        canvas.append(String.format("🔵 Drawing Circle: center(%.1f, %.1f), radius=%.1f\n",
                                   circle.getCenter().x, circle.getCenter().y, circle.getRadius()));
    }
    
    @Override
    public void visit(Rectangle rectangle) {
        addIndent();
        canvas.append(String.format("⬜ Drawing Rectangle: top-left(%.1f, %.1f), size=%.1fx%.1f\n",
                                   rectangle.getTopLeft().x, rectangle.getTopLeft().y,
                                   rectangle.getWidth(), rectangle.getHeight()));
    }
    
    @Override
    public void visit(Triangle triangle) {
        addIndent();
        Point[] vertices = triangle.getVertices();
        canvas.append(String.format("🔺 Drawing Triangle: vertices[(%.1f,%.1f), (%.1f,%.1f), (%.1f,%.1f)]\n",
                                   vertices[0].x, vertices[0].y,
                                   vertices[1].x, vertices[1].y,
                                   vertices[2].x, vertices[2].y));
    }
    
    @Override
    public void visit(CompoundShape compoundShape) {
        addIndent();
        canvas.append(String.format("📦 Drawing Compound Shape: '%s'\n", compoundShape.getName()));
        indentLevel++;
    }
    
    private void addIndent() {
        for (int i = 0; i < indentLevel; i++) {
            canvas.append("  ");
        }
    }
    
    public String getCanvas() {
        return canvas.toString();
    }
    
    public void reset() {
        canvas.setLength(0);
        indentLevel = 0;
    }
}

class SVGExportVisitor implements ShapeVisitor {
    private final StringBuilder svg = new StringBuilder();
    private boolean headerAdded = false;
    
    public SVGExportVisitor() {
        addSVGHeader();
    }
    
    @Override
    public void visit(Circle circle) {
        if (!headerAdded) addSVGHeader();
        
        svg.append(String.format(
            "  <circle cx=\"%.1f\" cy=\"%.1f\" r=\"%.1f\" fill=\"blue\" stroke=\"black\" stroke-width=\"1\"/>\n",
            circle.getCenter().x, circle.getCenter().y, circle.getRadius()
        ));
    }
    
    @Override
    public void visit(Rectangle rectangle) {
        if (!headerAdded) addSVGHeader();
        
        svg.append(String.format(
            "  <rect x=\"%.1f\" y=\"%.1f\" width=\"%.1f\" height=\"%.1f\" fill=\"red\" stroke=\"black\" stroke-width=\"1\"/>\n",
            rectangle.getTopLeft().x, rectangle.getTopLeft().y,
            rectangle.getWidth(), rectangle.getHeight()
        ));
    }
    
    @Override
    public void visit(Triangle triangle) {
        if (!headerAdded) addSVGHeader();
        
        Point[] vertices = triangle.getVertices();
        String points = String.format("%.1f,%.1f %.1f,%.1f %.1f,%.1f",
                                     vertices[0].x, vertices[0].y,
                                     vertices[1].x, vertices[1].y,
                                     vertices[2].x, vertices[2].y);
        
        svg.append(String.format(
            "  <polygon points=\"%s\" fill=\"green\" stroke=\"black\" stroke-width=\"1\"/>\n",
            points
        ));
    }
    
    @Override
    public void visit(CompoundShape compoundShape) {
        svg.append(String.format("  <!-- Compound Shape: %s -->\n", compoundShape.getName()));
    }
    
    private void addSVGHeader() {
        svg.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        svg.append("<svg width=\"800\" height=\"600\" xmlns=\"http://www.w3.org/2000/svg\">\n");
        headerAdded = true;
    }
    
    public String getSVG() {
        return svg.toString() + "</svg>\n";
    }
}

class ValidationVisitor implements ShapeVisitor {
    private final List<String> errors = new ArrayList<>();
    private final List<String> warnings = new ArrayList<>();
    
    @Override
    public void visit(Circle circle) {
        if (circle.getRadius() <= 0) {
            errors.add("Circle has invalid radius: " + circle.getRadius());
        }
        if (circle.getRadius() > 1000) {
            warnings.add("Circle has very large radius: " + circle.getRadius());
        }
    }
    
    @Override
    public void visit(Rectangle rectangle) {
        if (rectangle.getWidth() <= 0 || rectangle.getHeight() <= 0) {
            errors.add("Rectangle has invalid dimensions: " + 
                      rectangle.getWidth() + "x" + rectangle.getHeight());
        }
        if (rectangle.getWidth() * rectangle.getHeight() > 1000000) {
            warnings.add("Rectangle has very large area");
        }
    }
    
    @Override
    public void visit(Triangle triangle) {
        Point[] vertices = triangle.getVertices();
        // 삼각형의 세 점이 일직선상에 있는지 확인
        double area = Math.abs(
            (vertices[0].x * (vertices[1].y - vertices[2].y) +
             vertices[1].x * (vertices[2].y - vertices[0].y) +
             vertices[2].x * (vertices[0].y - vertices[1].y)) / 2.0
        );
        
        if (area < 0.001) {
            errors.add("Triangle vertices are collinear");
        }
    }
    
    @Override
    public void visit(CompoundShape compoundShape) {
        if (compoundShape.getChildren().isEmpty()) {
            warnings.add("Compound shape '" + compoundShape.getName() + "' is empty");
        }
    }
    
    public List<String> getErrors() {
        return new ArrayList<>(errors);
    }
    
    public List<String> getWarnings() {
        return new ArrayList<>(warnings);
    }
    
    public boolean isValid() {
        return errors.isEmpty();
    }
    
    public void reset() {
        errors.clear();
        warnings.clear();
    }
}

// Point 클래스
class Point {
    final double x, y;
    
    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }
}

// 사용 예시
class VisitorPatternDemo {
    public static void main(String[] args) {
        // 도형 생성
        Circle circle = new Circle(5.0, new Point(10, 10));
        Rectangle rectangle = new Rectangle(8.0, 6.0, new Point(0, 0));
        Triangle triangle = new Triangle(
            new Point(0, 0), new Point(4, 0), new Point(2, 3)
        );
        
        // 복합 도형 생성
        CompoundShape group = new CompoundShape("Main Group");
        group.addShape(circle);
        group.addShape(rectangle);
        group.addShape(triangle);
        
        System.out.println("=== Visitor Pattern Demo ===\n");
        
        // 1. 넓이 계산
        System.out.println("1. Area Calculation:");
        AreaCalculatorVisitor areaCalculator = new AreaCalculatorVisitor();
        group.accept(areaCalculator);
        System.out.printf("Total area: %.2f\n\n", areaCalculator.getTotalArea());
        
        // 2. 그리기
        System.out.println("2. Drawing:");
        DrawingVisitor drawer = new DrawingVisitor();
        group.accept(drawer);
        System.out.println(drawer.getCanvas());
        
        // 3. SVG 내보내기
        System.out.println("3. SVG Export:");
        SVGExportVisitor svgExporter = new SVGExportVisitor();
        group.accept(svgExporter);
        System.out.println(svgExporter.getSVG());
        
        // 4. 유효성 검증
        System.out.println("4. Validation:");
        ValidationVisitor validator = new ValidationVisitor();
        group.accept(validator);
        
        if (validator.isValid()) {
            System.out.println("✅ All shapes are valid");
        } else {
            System.out.println("❌ Validation errors found:");
            validator.getErrors().forEach(error -> System.out.println("  - " + error));
        }
        
        if (!validator.getWarnings().isEmpty()) {
            System.out.println("⚠️ Warnings:");
            validator.getWarnings().forEach(warning -> System.out.println("  - " + warning));
        }
    }
}
```

## **3. Memento와 Visitor의 현대적 활용**

### **3.1 Git의 커밋 시스템 (Memento 패턴)**

```java
// Git의 커밋이 Memento 패턴의 실제 구현
class GitRepository {
    private WorkingDirectory workingDir;
    private List<Commit> commitHistory;
    
    public Commit createCommit(String message) {
        // 현재 작업 디렉토리 상태를 Memento로 저장
        return new Commit(workingDir.createSnapshot(), message);
    }
    
    public void checkout(String commitHash) {
        // 특정 커밋의 Memento로 작업 디렉토리 복원
        Commit commit = findCommit(commitHash);
        workingDir.restoreFromSnapshot(commit.getSnapshot());
    }
}

class Commit {
    private final TreeSnapshot snapshot; // Memento
    private final String hash;
    private final String message;
    private final LocalDateTime timestamp;
    
    // Git의 각 커밋이 파일 시스템 상태의 Memento
}
```

### **3.2 컴파일러의 AST 처리 (Visitor 패턴)**

```java
// 컴파일러에서 AST 노드 처리
interface ASTVisitor {
    void visit(BinaryOperationNode node);
    void visit(VariableNode node);
    void visit(FunctionCallNode node);
}

class OptimizationVisitor implements ASTVisitor {
    @Override
    public void visit(BinaryOperationNode node) {
        // 상수 접기 최적화
        if (node.isConstantExpression()) {
            node.replaceWithConstant(node.evaluate());
        }
    }
    
    // 새로운 최적화를 추가해도 AST 노드 클래스는 수정하지 않음
}

class CodeGeneratorVisitor implements ASTVisitor {
    @Override
    public void visit(BinaryOperationNode node) {
        // 바이트코드 생성
        emit("LOAD " + node.getLeft());
        emit("LOAD " + node.getRight());
        emit(getOpcode(node.getOperator()));
    }
}
```

## **결론: 시간과 기능의 마법사들**

Memento와 Visitor 패턴은 객체지향 프로그래밍의 한계를 창의적으로 극복하는 패턴들입니다:

### **패턴별 핵심 가치:**

**Memento 패턴:**
- ✅ **시간적 캡슐화** - 과거 상태 보존
- ✅ **캡슐화 유지** - 내부 구조 노출 없이 상태 저장
- ✅ **Undo/Redo** 시스템 구현
- ✅ **버전 관리**와 **스냅샷** 기능

**Visitor 패턴:**
- ✅ **연산의 외부화** - 구조와 기능 분리
- ✅ **개방-폐쇄 원칙** 실현
- ✅ **Double Dispatch** 메커니즘
- ✅ **타입별 다형성** 처리

### **현대적 활용:**

```
Memento Pattern → Modern Evolution:
- Git Version Control System
- Database Transaction Logs
- Game Save/Load Systems
- Document Version History (Google Docs)

Visitor Pattern → Modern Evolution:
- Compiler AST Processing
- XML/JSON Tree Traversal
- Functional Pattern Matching
- Code Analysis Tools (SonarQube)
```

### **실무 가이드라인:**

```
✅ Memento 패턴 적용 시점:
- Undo/Redo 기능이 필요할 때
- 객체 상태의 스냅샷이 필요할 때
- 캡슐화를 유지하면서 상태 저장이 필요할 때
- 버전 관리나 히스토리 기능이 필요할 때

✅ Visitor 패턴 적용 시점:
- 객체 구조는 안정적이지만 연산이 자주 추가될 때
- 타입별로 다른 처리가 필요할 때
- 기존 클래스를 수정하지 않고 기능 확장이 필요할 때
- 복잡한 객체 구조를 순회하며 처리해야 할 때

⚠️ 주의사항:
- Memento: 메모리 사용량 최적화 필요
- Visitor: 객체 구조 변경 시 모든 Visitor 수정
- 과도한 복잡성 방지
- 성능 오버헤드 고려
```

### **함수형 프로그래밍과의 비교:**

```
Memento vs Immutability:
- Memento: 가변 객체 + 상태 저장
- Immutable: 불변 객체 + 새 인스턴스 생성

Visitor vs Pattern Matching:
- Visitor: 객체지향적 Double Dispatch
- Pattern Matching: 함수형 언어의 네이티브 지원
```

두 패턴 모두 **"시간의 조작"**과 **"기능의 확장"**이라는 복잡한 문제를 우아하게 해결하는 마법 같은 도구입니다. 현대 소프트웨어에서도 여전히 강력한 도구로 활용되고 있다.

다음 글에서는 **패턴의 조합과 상호작용**을 탐구하겠습니다. 여러 패턴을 함께 사용할 때의 시너지 효과와 아키텍처 설계 전략을 살펴보겠습니다.

---

**💡 핵심 메시지:**
"Memento는 시간을 되돌리는 마법을, Visitor는 기능을 무한 확장하는 마법을 제공한다. 두 패턴 모두 객체지향의 한계를 창의적으로 극복하며, 현대 프로그래밍에서도 여전히 강력한 도구로 활용되고 있다." 