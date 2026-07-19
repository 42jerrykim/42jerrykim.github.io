---
draft: false
collection_order: 230
title: "[Design Patterns] 23. 패턴을 활용한 코드 리뷰와 설계 리뷰"
slug: "pattern-code-review-design-review"
description: "디자인 패턴을 활용하여 체계적이고 효과적인 코드 리뷰와 설계 리뷰 프로세스를 구축하는 방법을 학습합니다. 패턴 기반 리뷰 체크리스트, 자동화 도구, 품질 메트릭, 팀 협업 방법론을 통해 코드 품질과 설계 일관성을 보장하는 전문가 수준의 리뷰 시스템을 구현합니다."
image: "wordcloud.png"
date: 2024-12-23T10:00:00+09:00
lastmod: 2026-07-18T10:00:00+09:00
categories:
- Design Patterns
- Code Review
- Design Review
- Quality Assurance
tags:
- Design-Pattern(디자인패턴)
- Code-Review(코드리뷰)
- Code-Quality(코드품질)
- Best-Practices
- SOLID
- Clean-Code(클린코드)
- Software-Architecture(소프트웨어아키텍처)
- Maintainability
- Readability
- Testing(테스트)
- Singleton
- Factory
- Strategy
- Observer
- Decorator
- Command
- Proxy
- Behavioral-Pattern
- Creational-Pattern
- Structural-Pattern
- OOP(객체지향)
- Java
- Documentation(문서화)
- Deep-Dive
- Advanced
- Case-Study
- Comparison(비교)
---

디자인 패턴을 활용한 효과적인 코드 리뷰와 설계 리뷰 방법을 탐구합니다. 패턴이라는 공통 언어로 팀의 설계 품질을 향상시키는 방법을 학습합니다.

## 서론: 집단 지성으로 완성되는 설계

> *"개인의 경험은 한계가 있지만, 팀의 집단 지성은 완벽한 설계를 만들어낸다. 패턴은 이러한 지식을 효율적으로 공유하는 공통 언어다."*

**코드 리뷰와 설계 리뷰**는 소프트웨어 품질을 보장하는 핵심 활동입니다. 이 글에서는 디자인 패턴을 활용해 더 효과적이고 체계적인 리뷰 프로세스를 구축하는 방법을 제시합니다.

### 패턴 기반 리뷰의 핵심 가치
- **공통 언어**: 패턴 이름으로 복잡한 설계를 간결하게 표현
- **검증 가능한 품질**: 패턴의 구조적 특성으로 객관적 평가
- **지식 전파**: 경험 있는 개발자의 노하우 체계적 공유
- **일관성 유지**: 팀 차원의 설계 표준 확립

## 패턴 기반 코드 리뷰 프레임워크

### 흔한 오해: 패턴 준수 = 좋은 리뷰

패턴 이름이 붙어 있고 GoF가 정의한 구조를 그대로 따랐다고 해서 리뷰를 통과시켜도 되는 것은 아닙니다. 패턴 준수는 "구조가 알려진 형태를 따르는가"를 확인할 뿐, "이 문제에 이 패턴이 필요했는가"나 "패턴이 실제 요구사항을 해결하는가"는 별개의 질문입니다. 아래 Observer 예시에서 `notifyObservers`가 정확한 구조로 구현되어 있어도, 관찰자 등록이 애초에 필요 없는 단순 알림 하나뿐이라면 패턴 자체가 과설계일 수 있습니다. 좋은 리뷰어는 "패턴을 올바르게 구현했는가"와 "이 패턴이 여기서 최선의 선택인가"를 항상 분리해서 묻습니다.

### 코드 리뷰 체크리스트 - 패턴 관점

패턴이 적용된 코드를 리뷰할 때는 동작 여부만이 아니라 패턴의 Intent와 실제 구현이 일치하는지, 필수 구성 요소가 빠짐없이 갖춰졌는지를 함께 검토해야 합니다. 아래 체크리스트는 Observer 패턴이 적용된 주문 서비스 코드를 예로 들어, 리뷰어가 확인해야 할 항목과 개선 전후 코드를 함께 보여줍니다. 이 체크리스트는 패턴 전반에 공통되는 원칙이며, 패턴별 세부 주의 항목은 글 하단 "패턴별 코드 리뷰 체크리스트" 표에 정리되어 있습니다.

```java
import java.util.ArrayList;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;

/**
 * 코드 리뷰 체크리스트 - 패턴 적용 검증
 * 
 * □ 패턴 적용 적절성
 *   - 문제 상황과 패턴이 매치하는가?
 *   - 패턴의 Intent와 실제 사용 목적이 일치하는가?
 *   - 더 간단한 해결책은 없는가?
 * 
 * □ 패턴 구현 완전성
 *   - 패턴의 필수 구성 요소가 모두 구현되었는가?
 *   - 패턴의 협력 관계가 올바르게 표현되었는가?
 *   - 패턴의 변형이 적절하게 적용되었는가?
 * 
 * □ 코드 품질
 *   - 네이밍이 패턴의 의도를 명확히 드러내는가?
 *   - 추상화 수준이 일관되는가?
 *   - 단일 책임 원칙이 지켜졌는가?
 */

// 리뷰 대상 코드가 의존하는 최소 도메인 타입 (실제 프로젝트에서는 별도 파일로 분리)
enum OrderStatus {
    PENDING, CONFIRMED, CANCELLED
}

class Order {
    private final Long id;
    private OrderStatus status;

    public Order(Long id, OrderStatus status) {
        this.id = id;
        this.status = status;
    }

    public void setStatus(OrderStatus status) {
        this.status = status;
    }

    public OrderStatus getStatus() {
        return status;
    }

    // 불변 스타일 API: 상태를 바꾼 새 인스턴스를 반환
    public Order confirm() {
        return new Order(this.id, OrderStatus.CONFIRMED);
    }
}

interface OrderObserver {
    void onOrderUpdated(Order order);
}

interface OrderRepository {
    Order save(Order order);
}

// 리뷰 예시 1: Observer 패턴 적용 검토
public class OrderService {
    private List<OrderObserver> observers = new ArrayList<>(); // 올바른 패턴 구현

    @Autowired
    private OrderRepository orderRepository;
    
    public void addObserver(OrderObserver observer) {
        observers.add(observer);
    }
    
    public void removeObserver(OrderObserver observer) {
        observers.remove(observer);
    }
    
    // 리뷰 포인트: notifyObservers가 private으로 숨겨져 있어 패턴 의도 불분명
    private void notifyObservers(Order order) {
        for (OrderObserver observer : observers) {
            observer.onOrderUpdated(order);
        }
    }
    
    public void confirmOrder(Order order) {
        order.setStatus(OrderStatus.CONFIRMED);
        orderRepository.save(order);
        
        // 올바른 알림 호출
        notifyObservers(order);
    }
}

// 리뷰 개선 제안
public class ImprovedOrderService {
    private static final Logger log = LoggerFactory.getLogger(ImprovedOrderService.class);

    private final List<OrderObserver> observers = new ArrayList<>();

    @Autowired
    private OrderRepository orderRepository;
    
    public void addObserver(OrderObserver observer) {
        if (observer != null && !observers.contains(observer)) { // 중복 방지
            observers.add(observer);
        }
    }
    
    public void removeObserver(OrderObserver observer) {
        observers.remove(observer);
    }
    
    // protected로 변경하여 확장 가능성 열어둠
    protected void notifyObservers(Order order) {
        // 예외 안전성 추가
        for (OrderObserver observer : new ArrayList<>(observers)) {
            try {
                observer.onOrderUpdated(order);
            } catch (Exception e) {
                log.error("Observer notification failed", e);
                // 관찰자 오류가 전체 프로세스를 중단하지 않도록
            }
        }
    }
    
    @Transactional
    public void confirmOrder(Order order) {
        Order savedOrder = orderRepository.save(order.confirm());
        notifyObservers(savedOrder); // 저장 후 알림
    }
}
```

### 효과적인 리뷰 기법

좋은 리뷰어는 코드에 암묵적으로 숨어 있는 패턴을 짚어내고, 이를 명시적으로 드러내도록 제안합니다. 다음 예시는 조건문으로 분기 처리된 파일 처리 로직에서 Strategy 패턴을 발견하고, 이를 명시적인 인터페이스 구조로 리팩토링하는 리뷰 과정을 보여줍니다.

```java
import java.util.List;

// 리뷰 기법 1: 패턴 인식 및 명명
public class PatternRecognitionReview {

    // 아래 9개 메서드는 실제 파일 I/O를 생략한 스텁입니다. 이 예시의 핵심은
    // "조건 분기 뒤에 숨은 Strategy 패턴을 찾아내는 리뷰 시각"이지 파싱 로직 자체가 아니므로,
    // 컴파일 가능성만 보장하는 최소 동작(로그 출력)만 남겨 둡니다.
    private static void readTextFile(String filePath) { System.out.println("read text: " + filePath); }
    private static void parseTextContent() { System.out.println("parse text content"); }
    private static void generateTextReport() { System.out.println("generate text report"); }
    private static void readCsvFile(String filePath) { System.out.println("read csv: " + filePath); }
    private static void parseCsvContent() { System.out.println("parse csv content"); }
    private static void generateCsvReport() { System.out.println("generate csv report"); }
    private static void readJsonFile(String filePath) { System.out.println("read json: " + filePath); }
    private static void parseJsonContent() { System.out.println("parse json content"); }
    private static void generateJsonReport() { System.out.println("generate json report"); }

    // Before: 패턴이 숨겨진 코드
    public static class LegacyFileProcessor {
        public void processFile(String filePath) {
            if (filePath.endsWith(".txt")) {
                // 텍스트 파일 처리
                readTextFile(filePath);
                parseTextContent();
                generateTextReport();
            } else if (filePath.endsWith(".csv")) {
                // CSV 파일 처리
                readCsvFile(filePath);
                parseCsvContent();
                generateCsvReport();
            } else if (filePath.endsWith(".json")) {
                // JSON 파일 처리
                readJsonFile(filePath);
                parseJsonContent();
                generateJsonReport();
            }
        }
    }
    
    // 리뷰 포인트: "이 코드에서 Strategy 패턴을 발견할 수 있습니다"
    // After: 패턴을 명시적으로 적용 (LegacyFileProcessor를 대체)
    public interface FileProcessingStrategy {
        boolean supports(String filePath);
        void process(String filePath);
    }
    
    public static class TextFileProcessingStrategy implements FileProcessingStrategy {
        @Override
        public boolean supports(String filePath) {
            return filePath.endsWith(".txt");
        }
        
        @Override  
        public void process(String filePath) {
            readTextFile(filePath);
            parseTextContent();
            generateTextReport();
        }
    }
    
    public static class FileProcessor {
        private final List<FileProcessingStrategy> strategies;
        
        public FileProcessor(List<FileProcessingStrategy> strategies) {
            this.strategies = strategies;
        }
        
        public void processFile(String filePath) {
            FileProcessingStrategy strategy = strategies.stream()
                .filter(s -> s.supports(filePath))
                .findFirst()
                .orElseThrow(() -> new UnsupportedOperationException("Unsupported file type: " + filePath));
                
            strategy.process(filePath);
        }
    }
}
```

## 리뷰 도구와 자동화

### 정적 분석 기반 패턴 검증

사람이 매번 패턴 준수 여부를 눈으로 확인하는 데는 한계가 있으므로, 정적 분석 규칙으로 반복적인 검증을 자동화할 수 있습니다. 아래 코드는 Singleton 패턴의 필수 조건(private 생성자, getInstance 메서드, 스레드 안전성)을 검증하는 규칙과, 이를 포함한 자동화된 리뷰 워크플로우의 구조를 보여줍니다.

```java
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

// 정적 분석 규칙에 필요한 최소 타입 정의 (실제 프로젝트에서는 정적 분석기 API가 제공)
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
@interface AnalysisRule {
}

enum IssueSeverity { ERROR, WARNING }

// Issue·ClassInfo처럼 "필드 조합 자체가 값의 전부"인 타입은 생성자·getter를 직접 적을 필요가 없습니다.
// Java 16부터 정식 도입된 record는 필드 선언만으로 생성자·접근자·equals/hashCode/toString을 컴파일러가 만들어 주므로,
// 아래 여섯 개 DTO는 모두 record로 선언해 이 검증 로직의 핵심(SingletonPatternRule.validate)에 시선이 머물게 합니다.
record Issue(IssueSeverity severity, String message) {
    static Issue error(String message) { return new Issue(IssueSeverity.ERROR, message); }
    static Issue warning(String message) { return new Issue(IssueSeverity.WARNING, message); }
}

// 리플렉션/AST 분석 결과를 감싸는 클래스 메타데이터. boolean 필드의 record 접근자는
// isXxx()가 아니라 필드명 그대로(privateConstructor(), threadSafe())가 생성된다는 점에 주의합니다.
record ClassInfo(String className, List<String> staticFields, List<String> methodNames,
                  boolean privateConstructor, boolean threadSafe) {
    boolean hasStaticField(String name) { return staticFields.contains(name); }
    boolean hasMethod(String name) { return methodNames.contains(name); }
}

// 커스텀 정적 분석 규칙
public class PatternValidationRules {
    
    /**
     * 규칙 1: Singleton 패턴 검증
     * - private 생성자 확인
     * - getInstance() 메서드 존재 확인
     * - 스레드 안전성 검증
     */
    @AnalysisRule
    public class SingletonPatternRule {
        
        public List<Issue> validate(ClassInfo classInfo) {
            List<Issue> issues = new ArrayList<>();
            
            if (isSingletonPattern(classInfo)) {
                // private 생성자 확인
                if (!hasPrivateConstructor(classInfo)) {
                    issues.add(Issue.error("Singleton must have private constructor"));
                }
                
                // getInstance 메서드 확인
                if (!hasGetInstanceMethod(classInfo)) {
                    issues.add(Issue.error("Singleton must have getInstance() method"));
                }
                
                // 스레드 안전성 확인
                if (!isThreadSafe(classInfo)) {
                    issues.add(Issue.warning("Singleton should be thread-safe"));
                }
            }
            
            return issues;
        }
        
        private boolean isSingletonPattern(ClassInfo classInfo) {
            return classInfo.hasStaticField("instance") && 
                   classInfo.hasMethod("getInstance");
        }

        private boolean hasPrivateConstructor(ClassInfo classInfo) {
            return classInfo.privateConstructor();
        }

        private boolean hasGetInstanceMethod(ClassInfo classInfo) {
            return classInfo.hasMethod("getInstance");
        }

        private boolean isThreadSafe(ClassInfo classInfo) {
            return classInfo.threadSafe();
        }
    }
}

// 자동화 워크플로우가 주고받는 입출력 타입. 아래 네 개도 필드 조합이 곧 값이므로 record로 선언합니다.
// 다만 ReviewReport는 addSection() 호출마다 내부 Map 상태가 바뀌는 가변 객체이므로 record로 표현할 수 없어 class로 남깁니다.
record CodeBase(List<ClassInfo> classes) {}
record DetectedPattern(String patternName, String className) {}
record PatternValidationResult(DetectedPattern pattern, List<Issue> issues) {}
record CodeQualityMetrics(int cyclomaticComplexity, double testCoverage) {}
record ImprovementSuggestion(String description, String targetClassName) {}

class ReviewReport {
    private final Map<String, Object> sections = new LinkedHashMap<>();

    public void addSection(String name, Object content) {
        sections.put(name, content);
    }
}

interface PatternDetector {
    List<DetectedPattern> detectPatterns(CodeBase codeBase);
}

interface PatternValidator {
    List<PatternValidationResult> validatePatterns(List<DetectedPattern> patterns);
}

interface MetricsCalculator {
    CodeQualityMetrics calculate(CodeBase codeBase);
}

interface SuggestionEngine {
    List<ImprovementSuggestion> generateSuggestions(
        List<DetectedPattern> patterns,
        List<PatternValidationResult> validations,
        CodeQualityMetrics metrics);
}

// 리뷰 자동화 워크플로우
@Service
public class AutomatedReviewService {

    @Autowired
    private PatternDetector patternDetector;

    @Autowired
    private PatternValidator patternValidator;

    @Autowired
    private MetricsCalculator metricsCalculator;

    @Autowired
    private SuggestionEngine suggestionEngine;
    
    public ReviewReport conductAutomatedReview(CodeBase codeBase) {
        ReviewReport report = new ReviewReport();
        
        // 1. 패턴 적용 탐지
        List<DetectedPattern> patterns = patternDetector.detectPatterns(codeBase);
        report.addSection("Detected Patterns", patterns);
        
        // 2. 패턴 구현 검증
        List<PatternValidationResult> validations = patternValidator.validatePatterns(patterns);
        report.addSection("Pattern Validations", validations);
        
        // 3. 코드 품질 메트릭
        CodeQualityMetrics metrics = metricsCalculator.calculate(codeBase);
        report.addSection("Quality Metrics", metrics);
        
        // 4. 개선 제안 생성
        List<ImprovementSuggestion> suggestions = suggestionEngine.generateSuggestions(
            patterns, validations, metrics);
        report.addSection("Improvement Suggestions", suggestions);
        
        return report;
    }
}
```

### 자동화 리뷰 워크플로우

자동화된 리뷰는 `CodeBase` 하나를 입력받아 네 단계를 거쳐 하나의 `ReviewReport`로 수렴합니다. `patternDetector`가 `ClassInfo` 목록에서 패턴 후보를 찾아내면, `patternValidator`가 `SingletonPatternRule`처럼 패턴별로 정의된 개별 규칙을 실행해 구조적 결함을 `Issue`로 기록하고, `metricsCalculator`는 패턴 탐지 결과와 무관하게 코드베이스 전체의 품질 지표를 독립적으로 계산합니다. 마지막으로 `suggestionEngine`이 탐지·검증·지표 세 결과를 모두 받아 `ImprovementSuggestion` 목록을 생성하면, 이 네 결과가 함께 `ReviewReport`로 조립됩니다. 아래 다이어그램은 이 단계들이 어떤 데이터를 주고받는지, 그리고 자동화가 멈추고 사람이 넘겨받는 지점이 어디인지를 보여줍니다.

```mermaid
flowchart TD
    A["CodeBase 원본 코드"] --> B["patternDetector: 패턴 탐지"]
    B --> C["DetectedPattern 목록"]
    A --> D["metricsCalculator: 품질 지표 계산"]
    D --> E["CodeQualityMetrics"]
    C --> F["patternValidator: 패턴 구현 검증</br>(SingletonPatternRule 등 개별 규칙 실행)"]
    F --> G["PatternValidationResult 목록"]
    C --> H["suggestionEngine: 개선안 생성"]
    G --> H
    E --> H
    H --> I["ImprovementSuggestion 목록"]
    C --> J["ReviewReport 조립"]
    G --> J
    E --> J
    I --> J
    J --> K["사람 리뷰어: 패턴 필요성 최종 판단"]
```

자동화가 만들어내는 것은 `PatternValidationResult`처럼 구조적으로 검증 가능한 사실뿐입니다. `SingletonPatternRule`은 스레드 안전성 위반이나 private 생성자 누락은 찾아내지만, 애초에 이 클래스에 Singleton이 필요했는지는 판단하지 못합니다. 이 경계가 앞서 다룬 "패턴 준수 = 좋은 리뷰"라는 오해를 자동화 도구로도 해소할 수 없는 이유이며, 그래서 워크플로우의 마지막 단계는 항상 사람의 판단으로 남습니다.

## 리뷰 효과 측정과 개선

### 리뷰 품질 메트릭

리뷰 프로세스 자체도 지속적으로 개선하려면 효과를 측정할 지표가 필요합니다. 다음은 결함 발견율, 패턴 적용 개선율, 참여도 등 리뷰 효과성을 정량적으로 분석하는 컴포넌트가 어떤 협력 구조를 가지는지 보여주는 설계 스케치입니다. `CodeReview`, `TimeRange`, `ReviewEffectivenessReport`, `PatternType`, `PatternReviewMetrics`는 사내 이슈 트래커·리뷰 플랫폼과 연동되는 가상 타입이며 이 글에서 정의하지 않으므로, 이 블록은 그대로 컴파일되지 않습니다. `.builder()` 호출 역시 Lombok `@Builder` 같은 외부 도구가 생성해 준다고 가정한 것입니다.

```text
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.stereotype.Component;

@Component
public class ReviewQualityAnalyzer {
    
    // 리뷰 효과성 측정
    public ReviewEffectivenessReport analyzeReviewEffectiveness(
            List<CodeReview> reviews, TimeRange timeRange) {
        
        ReviewEffectivenessReport report = new ReviewEffectivenessReport();
        
        // 1. 결함 발견율
        double defectDetectionRate = calculateDefectDetectionRate(reviews, timeRange);
        report.setDefectDetectionRate(defectDetectionRate);
        
        // 2. 패턴 적용 개선율
        double patternImprovementRate = calculatePatternImprovementRate(reviews);
        report.setPatternImprovementRate(patternImprovementRate);
        
        // 3. 코드 품질 향상도
        CodeQualityTrend qualityTrend = analyzeCodeQualityTrend(timeRange);
        report.setQualityTrend(qualityTrend);
        
        // 4. 리뷰 참여도
        ReviewParticipationMetrics participation = calculateParticipationMetrics(reviews);
        report.setParticipationMetrics(participation);
        
        return report;
    }
    
    // 패턴별 리뷰 성과 분석
    public Map<PatternType, PatternReviewMetrics> analyzePatternReviewMetrics(
            List<CodeReview> reviews) {
        
        Map<PatternType, PatternReviewMetrics> metrics = new HashMap<>();
        
        for (PatternType patternType : PatternType.values()) {
            List<CodeReview> patternReviews = reviews.stream()
                .filter(review -> review.involvePattern(patternType))
                .collect(Collectors.toList());
                
            if (!patternReviews.isEmpty()) {
                PatternReviewMetrics patternMetrics = PatternReviewMetrics.builder()
                    .totalReviews(patternReviews.size())
                    .averageReviewTime(calculateAverageReviewTime(patternReviews))
                    .defectsFound(countDefectsFound(patternReviews))
                    .improvementsSuggested(countImprovementsSuggested(patternReviews))
                    .implementationQualityScore(calculateImplementationQuality(patternReviews))
                    .build();
                    
                metrics.put(patternType, patternMetrics);
            }
        }
        
        return metrics;
    }
}
```

## 실무 적용 사례

### 대규모 팀의 리뷰 표준화

팀 규모가 커지면 팀마다 다른 리뷰 기준을 일관되게 관리하기 위한 정책과 워크플로우 설정이 필요합니다. 아래는 백엔드와 프론트엔드 팀에 서로 다른 리뷰 정책을 적용하고, 패턴 분석부터 승인까지 이어지는 리뷰 워크플로우 단계를 구성하는 방법을 보여주는 설계 스케치입니다. 위 `ReviewQualityAnalyzer`와 마찬가지로 `ReviewPolicy`, `ReviewPolicyManager`, `PatternComplexity`, `CodeQualityGate`, `ReviewWorkflowEngine`과 각 파이프라인 단계(`AutomatedPatternAnalysisStage` 등)는 이 글에서 정의하지 않는 가상 타입이므로 그대로 컴파일되지 않습니다. 실제로 이런 정책 엔진을 구현하려면 `ReviewPolicy`를 불변 값 객체(record)로, `ReviewWorkflowEngine`을 12편의 Strategy와 13편의 Chain of Responsibility를 조합한 구조로 설계하는 편이 현실적입니다.

```text
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

// 엔터프라이즈 리뷰 프레임워크
@Configuration
public class EnterpriseReviewFramework {
    
    // 팀별 리뷰 정책 설정
    @Bean
    public ReviewPolicyManager reviewPolicyManager() {
        ReviewPolicyManager manager = new ReviewPolicyManager();
        
        // 백엔드 팀 정책
        ReviewPolicy backendPolicy = ReviewPolicy.builder()
            .teamName("Backend")
            .requiredReviewers(2)
            .mandatoryPatternCheck(true)
            .patternComplexityThreshold(PatternComplexity.MEDIUM)
            .codeQualityGate(CodeQualityGate.STRICT)
            .build();
            
        // 프론트엔드 팀 정책  
        ReviewPolicy frontendPolicy = ReviewPolicy.builder()
            .teamName("Frontend")
            .requiredReviewers(1)
            .mandatoryPatternCheck(false)
            .patternComplexityThreshold(PatternComplexity.LOW)
            .codeQualityGate(CodeQualityGate.STANDARD)
            .build();
            
        manager.addPolicy("backend", backendPolicy);
        manager.addPolicy("frontend", frontendPolicy);
        
        return manager;
    }
    
    // 자동화된 리뷰 워크플로우
    @Bean
    public ReviewWorkflowEngine reviewWorkflowEngine() {
        return ReviewWorkflowEngine.builder()
            .addStage(new AutomatedPatternAnalysisStage())
            .addStage(new CodeQualityCheckStage())
            .addStage(new SecurityScanStage())
            .addStage(new HumanReviewStage())
            .addStage(new ApprovalStage())
            .build();
    }
}
```

## 실습 과제

### 과제 1: 리뷰 체크리스트 작성
Observer 패턴이 적용된 코드를 위한 상세한 리뷰 체크리스트를 작성하세요.

### 과제 2: 자동화 도구 구현
Strategy 패턴의 구현 완전성을 검증하는 정적 분석 도구를 구현하세요.

### 과제 3: 리뷰 개선 제안
팀의 현재 리뷰 프로세스를 분석하고, 패턴 기반 리뷰 도입을 위한 개선 계획을 수립하세요.

## 토론 주제

1. **리뷰 효율성 vs 철저함**: 시간 제약 하에서 효과적인 리뷰 방법은?
2. **자동화 vs 인간 판단**: 어디까지 자동화하고 어디서 인간의 직관이 필요한가?
3. **팀 문화와 리뷰**: 건설적인 리뷰 문화 조성 방법

## 한눈에 보는 패턴 코드 리뷰

### 패턴별 코드 리뷰 체크리스트

| 패턴 | 확인 사항 | 주의 포인트 |
|------|----------|-----------|
| Singleton | DCL 구현, 스레드 안전성 | 테스트 어려움, 전역 상태 |
| Factory | 생성 로직 복잡도 정당화 | 과도한 추상화 |
| Strategy | 인터페이스 일관성, 전략 개수 | 전략 폭발 |
| Observer | 메모리 누수, 해제 로직 | 순환 참조, 알림 순서 |
| Decorator | 체인 깊이, 순서 의존성 | 과도한 래핑 |
| Composite | 재귀 종료 조건, 깊이 제한 | 무한 루프 위험 |
| Proxy | 투명성 유지, 성능 영향 | 숨겨진 복잡성 |
| Command | Undo 구현 완전성 | 메모리 사용량 |

패턴 개별 항목을 확인했다면, 다음은 패턴 유무와 무관하게 모든 클래스·모듈에 적용되는 더 근본적인 설계 원칙과 패턴 도입 자체의 타당성을 함께 점검할 차례입니다. 아래 표는 SOLID 다섯 원칙 각각에 대해 리뷰어가 무엇을 확인해야 하는지와 판단 기준을 한 행씩 짝지어 놓았고, 마지막 세 행은 SOLID 준수와 별개로 "패턴이 정말 필요한가", "올바른 패턴을 골랐는가", "GoF 의도와 실제 구현이 일치하는가"를 순서대로 점검하도록 배치했습니다. 즉 이 표 하나로 원칙 준수 여부와 패턴 선택의 타당성을 함께 훑을 수 있습니다.

### 설계 리뷰 체크리스트

| 카테고리 | 체크 항목 | 판단 기준 |
|---------|----------|----------|
| SOLID | SRP 준수 | 클래스당 변경 이유 1개 |
| SOLID | OCP 준수 | 확장에 열림, 수정에 닫힘 |
| SOLID | LSP 준수 | 서브타입 치환 가능 |
| SOLID | ISP 준수 | 사용하지 않는 메서드 강제 X |
| SOLID | DIP 준수 | 추상화에 의존 |
| 패턴 | 패턴 필요성 | 복잡성 정당화 |
| 패턴 | 올바른 패턴 선택 | 요구사항과 매칭 |
| 패턴 | 구현 정확성 | GoF 의도와 일치 |

체크리스트로 결함을 찾았다면, 그 결함을 어떤 톤과 우선순위로 전달할지가 다음 문제입니다. 아래 표는 결함을 Critical(버그·보안)부터 Nit(스타일)까지 네 단계로 나누고, 각 단계에 해당하는 전형적인 예시와 리뷰어가 요구해야 할 대응 수위를 짝지어 정리한 것입니다. 같은 "패턴 오용"이라도 경쟁 조건(race condition)처럼 즉시 장애로 이어지는 결함은 Critical로 분류해 수정을 강제해야 하지만, 네이밍처럼 가독성에만 영향을 주는 지적은 Minor로 낮춰 모든 코멘트를 같은 무게로 요구하지 않도록 합니다.

### 리뷰 피드백 수준별 가이드

| 수준 | 유형 | 예시 | 대응 |
|------|------|------|------|
| Critical | 버그/보안 | NPE 가능성, 경쟁 조건 | 반드시 수정 |
| Major | 설계 결함 | 패턴 오용, SOLID 위반 | 수정 권장 |
| Minor | 개선 제안 | 네이밍, 가독성 | 선택적 |
| Nit | 스타일 | 포맷, 주석 | 자동화 가능 |

피드백 수준을 정했다면, 애초에 패턴을 도입하겠다는 제안 자체를 검토할 때 리뷰어가 던져야 할 질문 목록으로 넘어갑니다. 이 질문들은 위 "패턴 준수 = 좋은 리뷰"라는 오해를 막는 실질적 도구입니다.

### 패턴 도입 리뷰 질문

| 질문 | 목적 | 기대 답변 |
|------|------|----------|
| 왜 이 패턴이 필요한가? | 필요성 검증 | 구체적인 문제 상황 |
| 더 단순한 대안은? | 과설계 방지 | 검토한 대안 목록 |
| 확장 포인트는 어디인가? | OCP 확인 | 변경 가능 지점 |
| 테스트 용이성은? | 품질 확인 | Mock/Stub 전략 |
| 팀이 이해할 수 있는가? | 유지보수성 | 문서화 계획 |

무엇을 볼지 정했다면, 그것을 얼마나 오래·얼마나 많은 인원이 볼지도 리뷰 품질에 직접 영향을 줍니다. 아래 표의 리뷰 크기·시간 기준은 SmartBear가 발표한 "Best Practices for Code Review"가 정리한 시스코(Cisco)의 대규모 코드 리뷰 데이터 분석 결과를 인용한 것으로, 이 연구에 따르면 한 번에 검토하는 분량이 200-400 LOC를 넘어서거나 리뷰 시간이 60분을 넘기면 결함 발견율이 뚜렷하게 떨어졌습니다. 응답 시간 기준(24시간 이내)은 같은 연구가 강조한 "리뷰가 지연될수록 작성자가 그 코드의 문맥을 잊는다"는 관찰을 실무 규칙으로 옮긴 것이며, 리뷰어 수(1-2명)는 그 이상 인원이 참여해도 결함 발견율 증가폭이 크지 않다는 관찰에 따른 것입니다.

### 코드 리뷰 효율성 매트릭스

| 측면 | 권장 기준 | 근거 |
|------|----------|------|
| 리뷰 크기 | 200-400 LOC | 집중력 한계 |
| 리뷰 시간 | 60분 이내 | 피로도 증가 |
| 리뷰어 수 | 1-2명 | 효율적 피드백 |
| 응답 시간 | 24시간 이내 | 컨텍스트 유지 |

마지막으로, 위에서 다룬 항목 중 사람이 굳이 붙잡고 있지 않아도 되는 부분을 도구에 넘기면 리뷰어는 패턴 타당성 같은 판단이 필요한 항목에 시간을 더 쓸 수 있습니다.

### 자동화 가능 항목

| 항목 | 도구 | 효과 |
|------|------|------|
| 코드 스타일 | Checkstyle, ESLint | 일관성 보장 |
| 정적 분석 | SonarQube, SpotBugs | 잠재 버그 발견 |
| 복잡도 측정 | PMD, Complexity | 리팩토링 대상 식별 |
| 테스트 커버리지 | JaCoCo, Istanbul | 테스트 품질 확인 |
| 의존성 분석 | ArchUnit, Dependency | 아키텍처 준수 |

---

## 참고 자료

- **도서**: "Design Patterns: Elements of Reusable Object-Oriented Software" by Gamma, Helm, Johnson, Vlissides (GoF, 1994) — 이 글에서 다루는 모든 패턴 리뷰 기준의 1차 출처.
- **도서**: "Code Complete" by Steve McConnell  
- **도서**: "The Art of Readable Code" by Dustin Boswell
- **논문**: "Best Practices for Code Review" - SmartBear Software
- **도구**: SonarQube, Checkstyle, PMD, SpotBugs
- **플랫폼**: GitHub PR Review, GitLab MR, Bitbucket PR

---

## 평가 기준

이 글을 읽은 후 스스로 점검해볼 수 있는 체크리스트입니다.

- Observer 패턴이 적용된 코드에서 알림 실패 시 예외 전파, 메모리 누수 등 구조적 결함을 식별할 수 있는가?
- Strategy 패턴으로 리팩토링해야 할 조건 분기 코드를 알아볼 수 있는가?
- 패턴 적용이 과설계인지, 실제 문제 해결에 필요한지 판단할 수 있는가?
- 리뷰 코멘트를 Critical/Major/Minor/Nit 수준으로 구분해 우선순위를 매길 수 있는가?
- 어떤 항목을 자동화 도구에 맡기고 어떤 항목을 사람이 판단해야 하는지 구분할 수 있는가?

---

## 다음 단계

이 글에서 다룬 리뷰 체크리스트와 자동화 도구는 22편에서 정리한 안티패턴 목록을 전제로 움직입니다. 리뷰어가 "이 패턴이 왜 필요한가"를 물을 수 있는 것은 God Object나 Copy-Paste Programming 같은 안티패턴의 증상을 이미 알고 있기 때문이며, 정적 분석 규칙이 Singleton의 구조적 결함을 잡아낼 수 있는 것도 안티패턴 카탈로그가 먼저 "무엇이 잘못된 형태인가"를 정의해 두었기 때문입니다. 즉 리뷰는 안티패턴 지식을 매 커밋마다 실행하는 절차이고, 안티패턴은 리뷰가 걸러내야 할 대상의 목록입니다.

패턴을 활용한 효과적인 리뷰 시스템을 구축했다면, 마지막 글([새로운 패턴 발견과 정의](/post/design-patterns/discovering-defining-new-patterns/))에서는 기존 GoF 카탈로그에 없는 반복 구조를 팀 안에서 발견하고, 이를 검증 가능한 패턴으로 문서화하는 방법을 탐구해보겠습니다.

> *"최고의 리뷰는 코드를 개선할 뿐만 아니라, 개발자를 성장시킨다."*
