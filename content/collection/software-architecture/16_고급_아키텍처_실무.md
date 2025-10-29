---
draft: true
---
# 16장. 고급 아키텍처 실무

## 학습 목표
- 대규모 시스템 분해 전략을 이해한다
- 아키텍처 진화와 마이그레이션 방법을 습득한다
- 성능 엔지니어링 접근법을 학습한다
- 아키텍처 위험 관리 방법을 파악한다

---

## 대규모 시스템 분해 전략

### Strangler Fig 패턴

대규모 시스템을 분해할 때는 **점진적이고 위험을 최소화하는 전략**이 필요합니다.

```java
// Strangler Fig 패턴 구현
@Component
public class StranglerFigProxy {
    
    private final LegacySystemClient legacyClient;
    private final NewServiceClient newServiceClient;
    private final FeatureToggleService featureToggle;
    
    public CustomerData getCustomer(String customerId) {
        if (featureToggle.isEnabled("new-customer-service", customerId)) {
            try {
                return newServiceClient.getCustomer(customerId);
            } catch (Exception e) {
                log.warn("신규 서비스 실패, 레거시로 폴백: {}", e.getMessage());
                return legacyClient.getCustomer(customerId);
            }
        } else {
            return legacyClient.getCustomer(customerId);
        }
    }
    
    public void updateCustomer(String customerId, CustomerUpdateRequest request) {
        if (featureToggle.isEnabled("new-customer-service", customerId)) {
            newServiceClient.updateCustomer(customerId, request);
        }
        
        legacyClient.updateCustomer(customerId, request);
        validateDataConsistency(customerId);
    }
    
    private void validateDataConsistency(String customerId) {
        CompletableFuture.runAsync(() -> {
            try {
                CustomerData legacyData = legacyClient.getCustomer(customerId);
                CustomerData newData = newServiceClient.getCustomer(customerId);
                
                if (!dataMatches(legacyData, newData)) {
                    alertService.sendAlert("데이터 불일치 발견: " + customerId);
                }
            } catch (Exception e) {
                log.error("데이터 검증 실패: {}", customerId, e);
            }
        });
    }
}

// 피처 토글 서비스
@Service
public class FeatureToggleService {
    
    private final RedisTemplate<String, String> redisTemplate;
    
    public boolean isEnabled(String feature, String context) {
        String key = "feature:" + feature;
        String config = redisTemplate.opsForValue().get(key);
        
        if (config == null) {
            return false;
        }
        
        FeatureConfig featureConfig = parseConfig(config);
        
        if (featureConfig.getRolloutPercentage() == 100) {
            return true;
        }
        
        int hash = Math.abs(context.hashCode()) % 100;
        return hash < featureConfig.getRolloutPercentage();
    }
}
```

### 도메인 기반 분해

```java
// 도메인 경계 식별
@Component
public class DomainBoundaryAnalyzer {
    
    public List<DomainBoundary> analyzeBoundaries(SystemModel system) {
        List<DomainBoundary> boundaries = new ArrayList<>();
        
        Map<String, Set<String>> dataGroups = analyzeDataCohesion(system);
        Map<String, Set<String>> functionalGroups = analyzeFunctionalCohesion(system);
        
        for (String domain : dataGroups.keySet()) {
            DomainBoundary boundary = new DomainBoundary(domain);
            boundary.setDataEntities(dataGroups.get(domain));
            boundary.setFunctions(functionalGroups.get(domain));
            
            double cohesionScore = calculateCohesion(boundary);
            double couplingScore = calculateCoupling(boundary, system);
            boundary.setQualityScore(cohesionScore - couplingScore);
            
            boundaries.add(boundary);
        }
        
        return boundaries.stream()
            .sorted((b1, b2) -> Double.compare(b2.getQualityScore(), b1.getQualityScore()))
            .collect(Collectors.toList());
    }
}
```

---

## 아키텍처 진화

### 적응성 함수 (Fitness Function)

```java
// 적응성 함수 구현
@Component
public class ArchitectureFitnessFunction {
    
    public FitnessResult evaluateArchitecture(SystemArchitecture architecture) {
        FitnessResult result = new FitnessResult();
        
        double modularity = measureModularity(architecture);
        result.addMetric("modularity", modularity, 0.8);
        
        double coupling = measureCoupling(architecture);
        result.addMetric("coupling", coupling, 0.3);
        
        int cyclicDependencies = countCyclicDependencies(architecture);
        result.addMetric("cyclic_dependencies", cyclicDependencies, 0);
        
        double testCoverage = measureTestCoverage(architecture);
        result.addMetric("test_coverage", testCoverage, 0.8);
        
        return result;
    }
    
    @Scheduled(fixedRate = 3600000) // 1시간마다 실행
    public void continuousArchitectureValidation() {
        SystemArchitecture currentArchitecture = architectureService.getCurrentArchitecture();
        FitnessResult result = evaluateArchitecture(currentArchitecture);
        
        for (FitnessMetric metric : result.getMetrics()) {
            if (!metric.meetsThreshold()) {
                alertService.sendArchitectureAlert(
                    String.format("아키텍처 임계값 위반: %s = %f", 
                        metric.getName(), metric.getValue())
                );
            }
        }
        
        metricsRepository.save(new ArchitectureMetrics(LocalDateTime.now(), result));
    }
}
```

---

## 성능 엔지니어링

### 성능 모니터링

```java
// 성능 메트릭 수집
@Component
public class PerformanceMetricsCollector {
    
    private final MeterRegistry meterRegistry;
    
    @EventListener
    public void handleRequest(RequestEvent event) {
        Timer.Sample sample = Timer.start(meterRegistry);
        
        Timer requestTimer = Timer.builder("http.request.duration")
            .tag("method", event.getMethod())
            .tag("uri", event.getUri())
            .register(meterRegistry);
        
        sample.stop(requestTimer);
        
        Counter.builder("http.request.count")
            .tag("method", event.getMethod())
            .register(meterRegistry)
            .increment();
        
        if (event.getStatus() >= 400) {
            Counter.builder("http.request.errors")
                .tag("status", String.valueOf(event.getStatus()))
                .register(meterRegistry)
                .increment();
        }
    }
}

// 성능 병목 탐지
@Service
public class PerformanceBottleneckDetector {
    
    @Scheduled(fixedRate = 60000) // 1분마다 실행
    public void detectBottlenecks() {
        List<PerformanceBottleneck> bottlenecks = new ArrayList<>();
        
        bottlenecks.addAll(detectResponseTimeBottlenecks());
        bottlenecks.addAll(detectCpuBottlenecks());
        bottlenecks.addAll(detectMemoryBottlenecks());
        
        for (PerformanceBottleneck bottleneck : bottlenecks) {
            if (bottleneck.getSeverity() == Severity.CRITICAL) {
                alertService.sendCriticalAlert(bottleneck);
                autoOptimizer.tryAutoOptimization(bottleneck);
            }
        }
    }
    
    private List<PerformanceBottleneck> detectResponseTimeBottlenecks() {
        List<PerformanceBottleneck> bottlenecks = new ArrayList<>();
        Map<String, Double> p95ResponseTimes = metricsService.getP95ResponseTimes();
        
        for (Map.Entry<String, Double> entry : p95ResponseTimes.entrySet()) {
            String endpoint = entry.getKey();
            double p95Time = entry.getValue();
            double threshold = getThresholdForEndpoint(endpoint);
            
            if (p95Time > threshold) {
                bottlenecks.add(PerformanceBottleneck.builder()
                    .type(BottleneckType.RESPONSE_TIME)
                    .component(endpoint)
                    .severity(calculateSeverity(p95Time, threshold))
                    .build());
            }
        }
        
        return bottlenecks;
    }
}
```

---

## 아키텍처 위험 관리

### 위험 평가

```java
// 아키텍처 위험 평가
@Service
public class ArchitectureRiskAssessment {
    
    public RiskAssessmentReport assessRisks(SystemArchitecture architecture) {
        RiskAssessmentReport report = new RiskAssessmentReport();
        
        List<TechnicalRisk> technicalRisks = assessTechnicalRisks(architecture);
        report.addTechnicalRisks(technicalRisks);
        
        List<OperationalRisk> operationalRisks = assessOperationalRisks(architecture);
        report.addOperationalRisks(operationalRisks);
        
        List<SecurityRisk> securityRisks = assessSecurityRisks(architecture);
        report.addSecurityRisks(securityRisks);
        
        return report;
    }
    
    private List<TechnicalRisk> assessTechnicalRisks(SystemArchitecture architecture) {
        List<TechnicalRisk> risks = new ArrayList<>();
        
        // 단일 장애점 탐지
        List<Component> singlePoints = findSinglePointsOfFailure(architecture);
        for (Component component : singlePoints) {
            risks.add(TechnicalRisk.builder()
                .type(RiskType.SINGLE_POINT_OF_FAILURE)
                .component(component.getName())
                .probability(0.3)
                .impact(0.9)
                .description("단일 장애점으로 인한 전체 시스템 장애 가능성")
                .build());
        }
        
        // 기술 부채 위험
        double technicalDebtRatio = calculateTechnicalDebtRatio(architecture);
        if (technicalDebtRatio > 0.3) {
            risks.add(TechnicalRisk.builder()
                .type(RiskType.TECHNICAL_DEBT)
                .probability(0.8)
                .impact(0.6)
                .description(String.format("높은 기술 부채 비율: %f", technicalDebtRatio))
                .build());
        }
        
        return risks;
    }
}

// 지속적 위험 모니터링
@Component
public class ContinuousRiskMonitoring {
    
    @Scheduled(cron = "0 0 2 * * ?") // 매일 새벽 2시 실행
    public void dailyRiskAssessment() {
        SystemArchitecture currentArchitecture = architectureService.getCurrentArchitecture();
        RiskAssessmentReport report = riskAssessment.assessRisks(currentArchitecture);
        
        RiskAssessmentReport previousReport = getPreviousReport();
        RiskChangeAnalysis changeAnalysis = analyzeRiskChanges(previousReport, report);
        
        for (Risk newRisk : changeAnalysis.getNewRisks()) {
            alertService.sendRiskAlert("새로운 위험 탐지", newRisk);
        }
        
        for (Risk increasedRisk : changeAnalysis.getIncreasedRisks()) {
            alertService.sendRiskAlert("위험 수준 증가", increasedRisk);
        }
        
        riskReportRepository.save(report);
        dashboardService.updateRiskDashboard(report);
    }
}
```

---

## 핵심 요약

### 고급 아키텍처 실무 영역

| **영역** | **핵심 기법** | **주요 도구** | **성공 요인** |
|---------|-------------|-------------|-------------|
| **시스템 분해** | Strangler Fig, 점진적 마이그레이션 | 피처 토글, 병렬 실행 | 위험 최소화 |
| **아키텍처 진화** | 적응성 함수, 버전 전략 | 지속적 모니터링 | 자동화된 검증 |
| **성능 엔지니어링** | 메트릭 수집, 병목 탐지 | APM 도구, 자동 최적화 | 데이터 기반 결정 |
| **위험 관리** | 위험 평가, 완화 전략 | 모니터링, 알림 시스템 | 예방적 접근 |

### 실무 적용 가이드라인
1. **점진적 변화 (Incremental Change)**
2. **측정 가능한 목표 (Measurable Goals)**
3. **자동화된 검증 (Automated Validation)**
4. **지속적 모니터링 (Continuous Monitoring)**

---

## 생각해보기

1. 레거시 시스템 분해 시 가장 큰 위험 요소는 무엇인가?
2. 아키텍처 진화의 성공을 어떻게 측정할 것인가?
3. 성능 최적화와 개발 생산성 사이의 균형점은?

---

## 추가 학습 자료

### 도서
- "Monolith to Microservices" - Sam Newman
- "Building Evolutionary Architectures" - Neal Ford

### 온라인 자료
- Microservices.io 패턴 카탈로그
- Martin Fowler 블로그 