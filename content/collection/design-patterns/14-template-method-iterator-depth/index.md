---
collection_order: 140
title: "[Design Patterns] 템플릿 메서드와 이터레이터: 제어의 깊이"
description: "알고리즘의 골격을 정의하는 Template Method 패턴과 컬렉션 순회를 추상화하는 Iterator 패턴의 제어 구조와 설계 철학을 탐구합니다. 할리우드 원칙, Hook 메서드, 지연 평가, Stream API까지 포괄하여 제어 흐름을 우아하게 관리하는 고급 설계 기법을 학습합니다."
image: "wordcloud.png"
date: 2024-12-14T10:00:00+09:00
lastmod: 2024-12-15T14:30:00+09:00
categories:
- Design Patterns
- Behavioral Patterns
- Control Flow
- Collection Processing
tags:
- Template Method Pattern
- Iterator Pattern
- Behavioral Patterns
- Algorithm Skeleton
- Hollywood Principle
- Hook Methods
- Collection Traversal
- Lazy Evaluation
- Stream Processing
- Control Flow
- Design Patterns
- GoF Patterns
- Abstract Algorithm
- Primitive Operations
- Inversion Of Control
- Template Framework
- Iteration Protocol
- External Iterator
- Internal Iterator
- Aggregate Objects
- Cursor Pattern
- Enumeration
- Collection Interface
- Functional Iteration
- Pipeline Processing
- Map Reduce Pattern
- Reactive Streams
- Generator Pattern
- Coroutine Pattern
- Async Iterator
- Parallel Processing
- 템플릿 메서드 패턴
- 이터레이터 패턴
- 행동 패턴
- 알고리즘 골격
- 할리우드 원칙
- 훅 메서드
- 컬렉션 순회
- 지연 평가
- 스트림 처리
- 제어 흐름
- 디자인 패턴
- GoF 패턴
- 추상 알고리즘
- 기본 연산
- 제어 역전
- 템플릿 프레임워크
- 반복 프로토콜
- 외부 이터레이터
- 내부 이터레이터
- 집계 객체
- 커서 패턴
- 열거
- 컬렉션 인터페이스
- 함수형 반복
- 파이프라인 처리
- 맵 리듀스 패턴
- 리액티브 스트림
- 제너레이터 패턴
- 코루틴 패턴
- 비동기 이터레이터
- 병렬 처리
---

Template Method와 Iterator 패턴을 통해 알고리즘 골격 정의와 순회 추상화를 탐구합니다. 재사용 가능한 구조와 유연한 접근 방법을 설계합니다.

## 서론: 구조의 정의와 접근의 추상화

> *"Template Method는 '어떻게 할 것인가'의 구조를 정의하고, Iterator는 '어떻게 접근할 것인가'를 추상화한다."*

소프트웨어 개발에서 **"재사용 가능한 구조"**와 **"유연한 접근 방법"**은 핵심적인 설계 고려사항입니다. 비슷한 알고리즘이지만 세부 구현이 다른 경우, 동일한 컬렉션이지만 다양한 순회 방식이 필요한 경우... 이런 상황을 어떻게 우아하게 해결할 수 있을까요?

**Template Method 패턴**은 **"알고리즘의 골격을 정의"**하고 세부 구현을 하위 클래스에 위임하는 **할리우드 원칙(Hollywood Principle)**을 구현합니다. **Iterator 패턴**은 **"순회 방법을 추상화"**하여 컬렉션의 내부 구조를 숨기고 다양한 접근 방식을 제공합니다.

이 두 패턴은 **"제어 역전(Inversion of Control)"**과 **"캡슐화"**의 완벽한 예시입니다:
- Template Method: 알고리즘 **구조**의 제어 역전
- Iterator: 컬렉션 **순회**의 캡슐화

## Template Method 패턴 - 알고리즘 골격의 정의

### Template Method의 핵심 철학

Template Method 패턴의 핵심은 **"Don't call us, we'll call you"** (할리우드 원칙)입니다. 상위 클래스가 알고리즘의 제어 흐름을 관리하고, 하위 클래스는 특정 단계만 구현합니다.

```java
// Template Method 없이 구현한다면?
class BadDataProcessor {
    public void processCsvData(String file) {
        // CSV 특화 읽기
        String data = readCsvFile(file);
        // CSV 특화 변환
        List<Record> records = parseCsv(data);
        // CSV 특화 저장
        saveCsvData(records);
    }
    
    public void processJsonData(String file) {
        // JSON 특화 읽기
        String data = readJsonFile(file);
        // JSON 특화 변환
        List<Record> records = parseJson(data);
        // JSON 특화 저장
        saveJsonData(records);
    }
    
    // 😱 공통 알고리즘 구조의 중복
    // 😱 새로운 포맷 추가 시 전체 메서드 복사
    // 😱 에러 처리, 로깅 등 횡단 관심사 중복
}
```

### Template Method로 우아하게 해결

```java
// Template Method 패턴의 우아함
abstract class DataProcessor {
    // Template Method - 알고리즘 골격 정의 (final로 오버라이드 방지)
    public final ProcessingResult processData(String inputFile) {
        ProcessingResult result = new ProcessingResult();
        
        try {
            // 1. 전처리 (Hook Method)
            onProcessingStarted(inputFile);
            
            // 2. 데이터 읽기 (Concrete Method)
            RawData rawData = readData(inputFile);
            result.addStep("Read", "Success");
            
            // 3. 데이터 검증 (Hook Method)
            if (!validateData(rawData)) {
                result.addStep("Validation", "Failed");
                return result.markAsFailed("Data validation failed");
            }
            result.addStep("Validation", "Success");
            
            // 4. 데이터 변환 (Abstract Method - 필수 구현)
            ProcessedData processedData = transformData(rawData);
            result.addStep("Transform", "Success");
            result.setProcessedData(processedData);
            
            // 5. 추가 처리 (Hook Method)
            enhanceData(processedData);
            result.addStep("Enhancement", "Success");
            
            // 6. 데이터 저장 (Concrete Method)
            saveData(processedData);
            result.addStep("Save", "Success");
            
            // 7. 후처리 (Hook Method)
            onProcessingCompleted(result);
            
            return result.markAsSuccess();
            
        } catch (Exception e) {
            result.addStep("Error", e.getMessage());
            onProcessingFailed(e, result);
            return result.markAsFailed(e.getMessage());
        }
    }
    
    // Concrete Methods - 공통 구현
    protected RawData readData(String inputFile) {
        System.out.println("📖 Reading data from: " + inputFile);
        // 파일 시스템 접근, 에러 처리 등 공통 로직
        return new RawData(inputFile, readFileContent(inputFile));
    }
    
    protected void saveData(ProcessedData data) {
        System.out.println("💾 Saving processed data: " + data.getRecordCount() + " records");
        // 데이터베이스 저장, 파일 출력 등 공통 로직
        persistData(data);
    }
    
    // Hook Methods - 선택적 확장 포인트 (기본 구현 제공)
    protected void onProcessingStarted(String inputFile) {
        System.out.println("[Start] Processing started for: " + inputFile);
    }
    
    protected boolean validateData(RawData data) {
        // 기본 검증 로직
        return data != null && !data.isEmpty();
    }
    
    protected void enhanceData(ProcessedData data) {
        // 기본적으로는 아무것도 하지 않음
        System.out.println("[Info] Basic data enhancement applied");
    }
    
    protected void onProcessingCompleted(ProcessingResult result) {
        System.out.println("[OK] Processing completed successfully");
    }
    
    protected void onProcessingFailed(Exception e, ProcessingResult result) {
        System.err.println("[Error] Processing failed: " + e.getMessage());
    }
    
    // Abstract Methods - 하위 클래스에서 반드시 구현
    protected abstract ProcessedData transformData(RawData rawData);
    protected abstract String getProcessorType();
    
    // Helper methods
    private String readFileContent(String inputFile) {
        // 실제 파일 읽기 로직
        return "file content from " + inputFile;
    }
    
    private void persistData(ProcessedData data) {
        // 실제 데이터 저장 로직
        System.out.println("Data persisted: " + data.getRecordCount() + " records");
    }
}

// ConcreteClass - CSV 처리기
class CsvDataProcessor extends DataProcessor {
    @Override
    protected ProcessedData transformData(RawData rawData) {
        System.out.println("🔄 Transforming CSV data...");
        
        String content = rawData.getContent();
        List<DataRecord> records = new ArrayList<>();
        
        // CSV 파싱 로직
        String[] lines = content.split("\n");
        if (lines.length > 0) {
            String[] headers = lines[0].split(",");
            
            for (int i = 1; i < lines.length; i++) {
                String[] values = lines[i].split(",");
                Map<String, String> recordData = new HashMap<>();
                
                for (int j = 0; j < Math.min(headers.length, values.length); j++) {
                    recordData.put(headers[j].trim(), values[j].trim());
                }
                
                records.add(new DataRecord(recordData));
            }
        }
        
        return new ProcessedData(records, "CSV");
    }
    
    @Override
    protected boolean validateData(RawData data) {
        // CSV 특화 검증
        if (!super.validateData(data)) {
            return false;
        }
        
        String content = data.getContent();
        return content.contains(",") && content.contains("\n");
    }
    
    @Override
    protected void enhanceData(ProcessedData data) {
        super.enhanceData(data);
        System.out.println("📊 CSV-specific enhancement: calculating column statistics");
        
        // CSV 특화 개선 로직
        for (DataRecord record : data.getRecords()) {
            record.addMetadata("format", "csv");
            record.addMetadata("processed_at", LocalDateTime.now().toString());
        }
    }
    
    @Override
    protected String getProcessorType() {
        return "CSV_PROCESSOR";
    }
}

// ConcreteClass - JSON 처리기
class JsonDataProcessor extends DataProcessor {
    @Override
    protected ProcessedData transformData(RawData rawData) {
        System.out.println("🔄 Transforming JSON data...");
        
        String content = rawData.getContent();
        List<DataRecord> records = new ArrayList<>();
        
        // 간단한 JSON 파싱 시뮬레이션
        if (content.trim().startsWith("{") && content.trim().endsWith("}")) {
            Map<String, String> recordData = new HashMap<>();
            recordData.put("type", "json_object");
            recordData.put("content", content);
            records.add(new DataRecord(recordData));
        }
        
        return new ProcessedData(records, "JSON");
    }
    
    @Override
    protected boolean validateData(RawData data) {
        if (!super.validateData(data)) {
            return false;
        }
        
        String content = data.getContent().trim();
        return (content.startsWith("{") && content.endsWith("}")) ||
               (content.startsWith("[") && content.endsWith("]"));
    }
    
    @Override
    protected void enhanceData(ProcessedData data) {
        super.enhanceData(data);
        System.out.println("🔧 JSON-specific enhancement: schema validation");
        
        // JSON 특화 개선 로직
        for (DataRecord record : data.getRecords()) {
            record.addMetadata("format", "json");
            record.addMetadata("schema_version", "1.0");
        }
    }
    
    @Override
    protected String getProcessorType() {
        return "JSON_PROCESSOR";
    }
}

// 고급 Template Method - 조건부 실행
abstract class ConditionalDataProcessor extends DataProcessor {
    @Override
    public final ProcessingResult processData(String inputFile) {
        // 전처리 조건 확인
        if (!shouldProcess(inputFile)) {
            return ProcessingResult.skipped("Processing skipped based on conditions");
        }
        
        // 원본 템플릿 메서드 실행
        ProcessingResult result = super.processData(inputFile);
        
        // 후처리 조건 확인
        if (result.isSuccess() && shouldPostProcess(result)) {
            performPostProcessing(result);
        }
        
        return result;
    }
    
    // 추가 Hook Methods
    protected boolean shouldProcess(String inputFile) {
        return true; // 기본적으로 모든 파일 처리
    }
    
    protected boolean shouldPostProcess(ProcessingResult result) {
        return result.getProcessedData().getRecordCount() > 0;
    }
    
    protected void performPostProcessing(ProcessingResult result) {
        System.out.println("🔄 Performing post-processing...");
    }
}

// 지원 클래스들
class RawData {
    private final String source;
    private final String content;
    
    public RawData(String source, String content) {
        this.source = source;
        this.content = content;
    }
    
    public String getSource() { return source; }
    public String getContent() { return content; }
    public boolean isEmpty() { return content == null || content.trim().isEmpty(); }
}

class ProcessedData {
    private final List<DataRecord> records;
    private final String format;
    
    public ProcessedData(List<DataRecord> records, String format) {
        this.records = records;
        this.format = format;
    }
    
    public List<DataRecord> getRecords() { return records; }
    public String getFormat() { return format; }
    public int getRecordCount() { return records.size(); }
}

class DataRecord {
    private final Map<String, String> data;
    private final Map<String, String> metadata;
    
    public DataRecord(Map<String, String> data) {
        this.data = new HashMap<>(data);
        this.metadata = new HashMap<>();
    }
    
    public Map<String, String> getData() { return data; }
    public Map<String, String> getMetadata() { return metadata; }
    public void addMetadata(String key, String value) { metadata.put(key, value); }
}

class ProcessingResult {
    private final List<ProcessingStep> steps;
    private boolean success;
    private String message;
    private ProcessedData processedData;
    
    public ProcessingResult() {
        this.steps = new ArrayList<>();
        this.success = false;
    }
    
    public void addStep(String stepName, String status) {
        steps.add(new ProcessingStep(stepName, status, LocalDateTime.now()));
    }
    
    public ProcessingResult markAsSuccess() {
        this.success = true;
        this.message = "Processing completed successfully";
        return this;
    }
    
    public ProcessingResult markAsFailed(String message) {
        this.success = false;
        this.message = message;
        return this;
    }
    
    public static ProcessingResult skipped(String reason) {
        ProcessingResult result = new ProcessingResult();
        result.message = reason;
        return result;
    }
    
    // getters
    public boolean isSuccess() { return success; }
    public String getMessage() { return message; }
    public ProcessedData getProcessedData() { return processedData; }
    public void setProcessedData(ProcessedData processedData) { this.processedData = processedData; }
    public List<ProcessingStep> getSteps() { return steps; }
    
    static class ProcessingStep {
        private final String stepName;
        private final String status;
        private final LocalDateTime timestamp;
        
        public ProcessingStep(String stepName, String status, LocalDateTime timestamp) {
            this.stepName = stepName;
            this.status = status;
            this.timestamp = timestamp;
        }
        
        public String getStepName() { return stepName; }
        public String getStatus() { return status; }
        public LocalDateTime getTimestamp() { return timestamp; }
    }
}
```

## Iterator 패턴 - 순회의 추상화

### Iterator 패턴의 핵심 철학

Iterator 패턴은 **"컬렉션의 내부 구조를 숨기고 순회 방법을 추상화"**합니다. 클라이언트는 컬렉션이 배열인지 연결리스트인지 트리인지 알 필요 없이 동일한 방식으로 순회할 수 있습니다.

```java
// Iterator 없이 구현한다면?
class BadTreeTraversal {
    public void processTree(TreeNode root) {
        // 😱 클라이언트가 트리 순회 로직을 알아야 함
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            process(node);
            
            if (node.right != null) stack.push(node.right);
            if (node.left != null) stack.push(node.left);
        }
    }
    
    public void processList(ListNode head) {
        // 😱 다른 자료구조마다 다른 순회 로직
        ListNode current = head;
        while (current != null) {
            process(current);
            current = current.next;
        }
    }
    
    // 😱 자료구조 변경 시 모든 클라이언트 코드 수정 필요
}
```

### Iterator 패턴으로 우아하게 해결

```java
// Iterator 패턴의 우아함
interface Iterator<T> {
    boolean hasNext();
    T next();
    default void remove() {
        throw new UnsupportedOperationException("Remove operation not supported");
    }
}

interface Iterable<T> {
    Iterator<T> iterator();
}

// Binary Tree with multiple traversal methods
class BinaryTree<T extends Comparable<T>> implements Iterable<T> {
    private Node<T> root;
    
    static class Node<T> {
        T data;
        Node<T> left, right;
        
        Node(T data) {
            this.data = data;
        }
    }
    
    public void insert(T data) {
        root = insertRec(root, data);
    }
    
    private Node<T> insertRec(Node<T> root, T data) {
        if (root == null) {
            return new Node<>(data);
        }
        
        if (data.compareTo(root.data) < 0) {
            root.left = insertRec(root.left, data);
        } else if (data.compareTo(root.data) > 0) {
            root.right = insertRec(root.right, data);
        }
        
        return root;
    }
    
    // 기본 반복자 - Inorder 순회
    @Override
    public Iterator<T> iterator() {
        return new InorderIterator();
    }
    
    // 다양한 순회 방식 제공
    public Iterator<T> preorderIterator() {
        return new PreorderIterator();
    }
    
    public Iterator<T> levelOrderIterator() {
        return new LevelOrderIterator();
    }
    
    // Inorder Iterator 구현
    private class InorderIterator implements Iterator<T> {
        private final Stack<Node<T>> stack = new Stack<>();
        private Node<T> current;
        
        public InorderIterator() {
            current = root;
        }
        
        @Override
        public boolean hasNext() {
            return current != null || !stack.isEmpty();
        }
        
        @Override
        public T next() {
            if (!hasNext()) {
                throw new NoSuchElementException("No more elements");
            }
            
            // 왼쪽 끝까지 이동
            while (current != null) {
                stack.push(current);
                current = current.left;
            }
            
            // 스택에서 노드 꺼내기
            current = stack.pop();
            T data = current.data;
            
            // 오른쪽 서브트리로 이동
            current = current.right;
            
            return data;
        }
    }
    
    // Preorder Iterator 구현
    private class PreorderIterator implements Iterator<T> {
        private final Stack<Node<T>> stack = new Stack<>();
        
        public PreorderIterator() {
            if (root != null) {
                stack.push(root);
            }
        }
        
        @Override
        public boolean hasNext() {
            return !stack.isEmpty();
        }
        
        @Override
        public T next() {
            if (!hasNext()) {
                throw new NoSuchElementException("No more elements");
            }
            
            Node<T> current = stack.pop();
            
            // 오른쪽 먼저 푸시 (스택이므로 왼쪽이 먼저 처리됨)
            if (current.right != null) {
                stack.push(current.right);
            }
            if (current.left != null) {
                stack.push(current.left);
            }
            
            return current.data;
        }
    }
    
    // Level Order Iterator 구현
    private class LevelOrderIterator implements Iterator<T> {
        private final Queue<Node<T>> queue = new LinkedList<>();
        
        public LevelOrderIterator() {
            if (root != null) {
                queue.add(root);
            }
        }
        
        @Override
        public boolean hasNext() {
            return !queue.isEmpty();
        }
        
        @Override
        public T next() {
            if (!hasNext()) {
                throw new NoSuchElementException("No more elements");
            }
            
            Node<T> current = queue.poll();
            
            if (current.left != null) {
                queue.add(current.left);
            }
            if (current.right != null) {
                queue.add(current.right);
            }
            
            return current.data;
        }
    }
}

// 고급 Iterator - 필터링과 변환
class FilteringIterator<T> implements Iterator<T> {
    private final Iterator<T> baseIterator;
    private final Predicate<T> filter;
    private T nextElement;
    private boolean hasNextElement;
    
    public FilteringIterator(Iterator<T> baseIterator, Predicate<T> filter) {
        this.baseIterator = baseIterator;
        this.filter = filter;
        advance();
    }
    
    private void advance() {
        hasNextElement = false;
        while (baseIterator.hasNext()) {
            T element = baseIterator.next();
            if (filter.test(element)) {
                nextElement = element;
                hasNextElement = true;
                break;
            }
        }
    }
    
    @Override
    public boolean hasNext() {
        return hasNextElement;
    }
    
    @Override
    public T next() {
        if (!hasNext()) {
            throw new NoSuchElementException("No more elements");
        }
        
        T result = nextElement;
        advance();
        return result;
    }
}

// 변환 Iterator
class MappingIterator<T, R> implements Iterator<R> {
    private final Iterator<T> baseIterator;
    private final Function<T, R> mapper;
    
    public MappingIterator(Iterator<T> baseIterator, Function<T, R> mapper) {
        this.baseIterator = baseIterator;
        this.mapper = mapper;
    }
    
    @Override
    public boolean hasNext() {
        return baseIterator.hasNext();
    }
    
    @Override
    public R next() {
        return mapper.apply(baseIterator.next());
    }
}

// 복합 Iterator 작업을 위한 유틸리티 클래스
class IteratorUtils {
    public static <T> Iterator<T> filter(Iterator<T> iterator, Predicate<T> predicate) {
        return new FilteringIterator<>(iterator, predicate);
    }
    
    public static <T, R> Iterator<R> map(Iterator<T> iterator, Function<T, R> mapper) {
        return new MappingIterator<>(iterator, mapper);
    }
    
    public static <T> Iterator<T> limit(Iterator<T> iterator, int maxSize) {
        return new Iterator<T>() {
            private int count = 0;
            
            @Override
            public boolean hasNext() {
                return count < maxSize && iterator.hasNext();
            }
            
            @Override
            public T next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                count++;
                return iterator.next();
            }
        };
    }
    
    public static <T> List<T> toList(Iterator<T> iterator) {
        List<T> result = new ArrayList<>();
        while (iterator.hasNext()) {
            result.add(iterator.next());
        }
        return result;
    }
}
```

### 현대적 Iterator - Stream과의 연계

```java
// Stream 지원 Iterator
class StreamableBinaryTree<T extends Comparable<T>> extends BinaryTree<T> {
    
    // Stream 지원
    public Stream<T> stream() {
        return StreamSupport.stream(
            Spliterators.spliteratorUnknownSize(iterator(), Spliterator.ORDERED),
            false
        );
    }
    
    public Stream<T> parallelStream() {
        return StreamSupport.stream(
            Spliterators.spliteratorUnknownSize(iterator(), Spliterator.ORDERED),
            true
        );
    }
    
    // 특정 순회 방식의 Stream
    public Stream<T> preorderStream() {
        return StreamSupport.stream(
            Spliterators.spliteratorUnknownSize(preorderIterator(), Spliterator.ORDERED),
            false
        );
    }
    
    public Stream<T> levelOrderStream() {
        return StreamSupport.stream(
            Spliterators.spliteratorUnknownSize(levelOrderIterator(), Spliterator.ORDERED),
            false
        );
    }
    
    // 지연 평가 Iterator
    public Iterator<T> lazyFilteredIterator(Predicate<T> predicate) {
        return new Iterator<T>() {
            private final Iterator<T> baseIterator = iterator();
            private T nextItem = null;
            private boolean hasNextItem = false;
            
            @Override
            public boolean hasNext() {
                if (!hasNextItem) {
                    findNext();
                }
                return hasNextItem;
            }
            
            @Override
            public T next() {
                if (!hasNext()) {
                    throw new NoSuchElementException();
                }
                hasNextItem = false;
                return nextItem;
            }
            
            private void findNext() {
                while (baseIterator.hasNext()) {
                    T item = baseIterator.next();
                    if (predicate.test(item)) {
                        nextItem = item;
                        hasNextItem = true;
                        return;
                    }
                }
                hasNextItem = false;
            }
        };
    }
}

// 사용 예시
class IteratorPatternDemo {
    public static void main(String[] args) {
        StreamableBinaryTree<Integer> tree = new StreamableBinaryTree<>();
        
        // 트리에 데이터 삽입
        int[] values = {50, 30, 70, 20, 40, 60, 80};
        for (int value : values) {
            tree.insert(value);
        }
        
        System.out.println("=== Iterator Pattern Demo ===\n");
        
        // 1. 기본 순회 (Inorder)
        System.out.println("Inorder traversal:");
        for (Integer value : tree) {
            System.out.print(value + " ");
        }
        System.out.println("\n");
        
        // 2. Preorder 순회
        System.out.println("Preorder traversal:");
        Iterator<Integer> preorderIter = tree.preorderIterator();
        while (preorderIter.hasNext()) {
            System.out.print(preorderIter.next() + " ");
        }
        System.out.println("\n");
        
        // 3. Stream 연산
        System.out.println("Even numbers (using Stream):");
        tree.stream()
            .filter(n -> n % 2 == 0)
            .forEach(n -> System.out.print(n + " "));
        System.out.println("\n");
        
        // 4. 복합 Iterator 연산
        System.out.println("Filtered and mapped values:");
        Iterator<String> complexIter = IteratorUtils.map(
            IteratorUtils.filter(tree.iterator(), n -> n > 40),
            n -> "Value:" + n
        );
        
        List<String> results = IteratorUtils.toList(complexIter);
        results.forEach(System.out::println);
    }
}
```

## Template Method와 Iterator의 시너지

두 패턴을 결합하면 매우 강력한 처리 파이프라인을 만들 수 있습니다:

```java
// Template Method + Iterator 결합
abstract class IterativeProcessor<T> {
    // Template Method
    public final ProcessingResult processCollection(Iterable<T> collection) {
        ProcessingResult result = new ProcessingResult();
        
        try {
            onProcessingStarted(collection);
            
            Iterator<T> iterator = collection.iterator();
            int processedCount = 0;
            
            while (iterator.hasNext()) {
                T item = iterator.next();
                
                if (shouldProcessItem(item)) {
                    processItem(item);
                    processedCount++;
                }
                
                if (shouldBreakEarly(processedCount)) {
                    break;
                }
            }
            
            onProcessingCompleted(processedCount);
            return result.markAsSuccess();
            
        } catch (Exception e) {
            onProcessingFailed(e);
            return result.markAsFailed(e.getMessage());
        }
    }
    
    // Hook Methods
    protected void onProcessingStarted(Iterable<T> collection) {}
    protected boolean shouldProcessItem(T item) { return true; }
    protected boolean shouldBreakEarly(int processedCount) { return false; }
    protected void onProcessingCompleted(int processedCount) {}
    protected void onProcessingFailed(Exception e) {}
    
    // Abstract Method
    protected abstract void processItem(T item);
}

// 구체적인 구현
class NumberProcessor extends IterativeProcessor<Integer> {
    private int sum = 0;
    
    @Override
    protected void processItem(Integer item) {
        sum += item;
        System.out.println("Processing: " + item + ", Running sum: " + sum);
    }
    
    @Override
    protected boolean shouldProcessItem(Integer item) {
        return item > 0; // 양수만 처리
    }
    
    @Override
    protected void onProcessingCompleted(int processedCount) {
        System.out.println("Final sum: " + sum + " (processed " + processedCount + " items)");
    }
    
    public int getSum() { return sum; }
}
```

## 한눈에 보는 Template Method & Iterator 패턴

### Template Method vs Iterator 핵심 비교

| 비교 항목 | Template Method | Iterator |
|----------|----------------|----------|
| **핵심 목적** | 알고리즘 골격 정의, 일부 단계 위임 | 컬렉션 순회 추상화 |
| **관계 유형** | 상속 (is-a) | 컴포지션 (has-a) |
| **확장 방식** | 서브클래스에서 메서드 오버라이드 | Iterator 구현체 생성 |
| **제어 흐름** | 부모가 제어 (Hollywood Principle) | Iterator가 제어 |
| **재사용 단위** | 알고리즘 골격 | 순회 로직 |
| **GoF 분류** | 행동 패턴 (클래스) | 행동 패턴 (객체) |

### Template Method 훅(Hook) 유형

| 훅 유형 | 설명 | 구현 |
|--------|------|------|
| Abstract Method | 반드시 구현 필요 | `protected abstract void step()` |
| Hook Method | 선택적 오버라이드 | `protected void hook() {}` |
| Primitive Operation | 기본 구현 제공 | `protected void primitive() {...}` |

### Iterator 유형 비교

| Iterator 유형 | 특징 | 예시 |
|--------------|------|------|
| External Iterator | 클라이언트가 순회 제어 | `for (Iterator it = ...)` |
| Internal Iterator | 컬렉션이 순회 제어 | `forEach()`, `stream()` |
| Robust Iterator | 순회 중 변경 안전 | `CopyOnWriteArrayList` |
| Null Iterator | 빈 컬렉션 처리 | 항상 hasNext()=false |

### 현대 Java에서의 구현

| 패턴 | 전통적 구현 | 현대적 구현 |
|------|-----------|-----------|
| Template Method | 추상 클래스 상속 | 람다 + 함수 인터페이스 |
| Iterator | `Iterator<E>` 구현 | `Stream<E>`, `Spliterator` |

### 적용 시나리오 비교

| 시나리오 | Template Method | Iterator |
|----------|----------------|----------|
| 알고리즘 골격 정의 | O | X |
| 컬렉션 순회 | X | O |
| 프레임워크 확장점 | O | X |
| 트리/그래프 순회 | X | O |
| 데이터 처리 파이프라인 | O | O (Stream) |
| 테스트 픽스처 (setUp/tearDown) | O | X |

### Java Collections에서의 활용

| 클래스/인터페이스 | Template Method | Iterator |
|-----------------|----------------|----------|
| AbstractList | get(), size() 추상화 | listIterator() |
| AbstractMap | entrySet() 추상화 | keySet().iterator() |
| AbstractCollection | - | iterator() 필수 구현 |
| Stream | - | Spliterator 기반 |

### 장단점 비교

| 패턴 | 장점 | 단점 |
|------|------|------|
| Template Method | 코드 중복 제거, 확장점 제공, 제어 역전 | 상속 강제, 유연성 제한 |
| Iterator | 내부 구조 은닉, 다양한 순회 지원, SRP | 단순 순회에 과도, 클래스 증가 |

### Hollywood Principle vs 일반 호출

| 측면 | Hollywood Principle | 일반 호출 |
|------|-------------------|----------|
| 제어 방향 | 프레임워크 → 사용자 코드 | 사용자 코드 → 라이브러리 |
| 호출 주체 | 상위 클래스 | 클라이언트 |
| 예시 | Template Method | 일반 메서드 호출 |
| 원칙 | "Don't call us, we'll call you" | - |

### 적용 체크리스트

| Template Method 체크 항목 | Iterator 체크 항목 |
|-------------------------|-------------------|
| 알고리즘 골격이 고정되어 있는가? | 컬렉션 내부 구조를 숨겨야 하는가? |
| 일부 단계만 변형이 필요한가? | 여러 순회 방식을 지원해야 하는가? |
| 코드 중복이 발생하는가? | 동시 순회가 필요한가? |
| 프레임워크 확장점을 제공하는가? | 복잡한 데이터 구조를 순회하는가? |

---

## 결론: 구조와 접근의 완벽한 조화

Template Method와 Iterator 패턴은 **"구조의 정의"**와 **"접근의 추상화"**를 통해 코드의 재사용성과 유연성을 극대화합니다:

### 패턴별 핵심 가치:

**Template Method 패턴:**
- 알고리즘 **구조**의 재사용
- **할리우드 원칙** 구현
- **확장 포인트** 명확화
- **공통 로직** 중앙집중화

**Iterator 패턴:**
- 순회 방법의 **추상화**
- 컬렉션 **내부 구조** 은닉
- **다양한 순회 방식** 지원
- **지연 평가**와 **메모리 효율성**

### 현대적 활용:

```
Template Method → Modern Evolution:
- Spring Framework Templates
- Java 8+ Stream API
- Testing Frameworks (JUnit)
- Web MVC Frameworks

Iterator → Modern Evolution:
- Java Collections Framework
- Stream API and Spliterator
- Reactive Streams
- Generator Functions (Python, JavaScript)
```

### 실무 가이드라인:

```
Template Method 적용 시점:
- 알고리즘 구조가 유사하지만 세부 구현이 다를 때
- 프레임워크나 라이브러리 설계 시
- 공통 로직과 변경 로직을 분리하고 싶을 때
- 제어 역전(IoC)을 구현하고 싶을 때

Iterator 적용 시점:
- 컬렉션 내부 구조를 숨기고 싶을 때
- 다양한 순회 방식을 제공해야 할 때
- 지연 평가나 메모리 효율성이 중요할 때
- 함수형 프로그래밍 스타일을 적용할 때

주의사항:
- Template Method의 과도한 Hook 메서드 방지
- Iterator의 상태 관리와 동시성 문제
- 성능 오버헤드 고려
- 복잡성과 유연성의 균형
```

두 패턴 모두 **"추상화"**를 통해 복잡성을 관리하고 코드의 품질을 향상시키는 강력한 도구입니다. 현대 프로그래밍의 핵심 개념인 **"분리"**와 **"재사용"**을 완벽하게 구현합니다.

다음 글에서는 **패턴의 조합과 상호작용**을 탐구하겠습니다. 여러 패턴을 함께 사용할 때의 시너지 효과와 주의사항을 살펴보겠습니다.

---

**핵심 메시지:**
"Template Method는 '무엇을 해야 하는가'의 구조를 정의하고, Iterator는 '어떻게 접근해야 하는가'를 추상화한다. 두 패턴 모두 제어 역전을 통해 유연성과 재사용성을 극대화하는 핵심 메커니즘이다." 