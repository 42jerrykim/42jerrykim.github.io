---
draft: true
collection_order: 101
title: "[Design Patterns] 10. 브릿지와 플라이웨이트: 분리와 효율성 — 실습"
slug: "bridge-flyweight-separation-efficiency-practice"
description: "Bridge 패턴으로 다중 플랫폼 파일 시스템을, Flyweight 패턴으로 메모리 효율적인 텍스트 렌더링 시스템을 직접 구현합니다. 패턴 적용 전후의 메모리 사용량과 성능 차이를 비교 분석하며 실전 감각을 익히는 실습형 글입니다."
image: "wordcloud.png"
date: 2024-12-10T11:00:00+09:00
lastmod: 2026-07-17T14:30:00+09:00
categories:
- Design Patterns
- Structural Patterns
- Performance Optimization
- Practice
- Memory Efficiency
tags:
- Design-Pattern(디자인패턴)
- GoF(Gang of Four)
- Structural-Pattern
- Software-Architecture(소프트웨어아키텍처)
- Memory(메모리)
- Tutorial(튜토리얼)
- Implementation(구현)
- Best-Practices
- Optimization(최적화)
- Performance(성능)
- Java
- OOP(객체지향)
- Abstraction(추상화)
- Encapsulation(캡슐화)
- Composition(합성)
- Interface(인터페이스)
- Coupling(결합도)
- Cohesion(응집도)
- Guide(가이드)
- Beginner
- Advanced
- Case-Study
- Refactoring(리팩토링)
- Code-Quality(코드품질)
- Modularity
- Maintainability
- Readability
- Benchmark
- Profiling(프로파일링)
---

이 실습에서는 Bridge 패턴으로 다중 플랫폼 시스템을, Flyweight 패턴으로 메모리 효율적인 시스템을 직접 구현합니다.

## 실습 목표

1. Bridge 패턴으로 다중 플랫폼 파일 시스템 구현
2. Flyweight 패턴으로 메모리 효율적인 텍스트 렌더링 구현  
3. 패턴 적용 전후 성능 비교 분석

## 과제 1: Bridge 패턴 - 파일 시스템

GoF는 Bridge를 **"추상화와 구현을 분리하여 이 둘이 독립적으로 변화할 수 있게 하는"** 패턴으로 정의한다(Gamma, Helm, Johnson, Vlissides, *Design Patterns*, 1994). 이 과제는 그 정의를 파일 시스템이라는 익숙한 도메인에 적용해 추상화(`FileManager`)와 구현(`FileSystemImpl`)을 분리하는 감각을 익히는 것이 목적이다. Windows/Linux/Mac은 경로 구분자나 권한 모델이 다르지만, 파일을 복사·이동·확인하는 비즈니스 로직 자체는 플랫폼과 무관하다. `FileManager` 계층에 비즈니스 로직(`BasicFileManager`는 단순 복사, `SecureFileManager`는 권한 검사 추가)을, `FileSystemImpl` 계층에 플랫폼별 세부 구현을 두면 N개 매니저 × M개 플랫폼을 N+M개 클래스로 구현할 수 있다.

### 기본 구조
```java
// 추상화: 파일 매니저
public abstract class FileManager {
    protected FileSystemImpl fileSystem;
    
    public FileManager(FileSystemImpl fileSystem) {
        this.fileSystem = fileSystem;
    }
    
    public abstract void copyFile(String source, String destination);
    public abstract void moveFile(String source, String destination);
    public abstract boolean fileExists(String path);
}

// 구현 인터페이스
public interface FileSystemImpl {
    void createFile(String path, String content);
    String readFile(String path);
    void deleteFile(String path);
    boolean exists(String path);
    String getPathSeparator();
}
```

### 구현 과제
- WindowsFileSystem (경로 구분자: \, 드라이브 문자 지원)
- LinuxFileSystem (경로 구분자: /, 권한 모드)
- MacFileSystem (확장 속성 지원)
- BasicFileManager, SecureFileManager 구현

### 구현체별 비교

세 `FileSystemImpl` 구현체는 인터페이스는 동일하지만 내부적으로 다루는 플랫폼 특성이 다르다. 구현을 시작하기 전에 아래 차이를 먼저 정리해두면 어떤 메서드에서 분기가 필요한지 감을 잡기 쉽다.

| 구현체 | 경로 구분자 | 권한 모델 | 특이사항 |
|--------|-----------|----------|---------|
| WindowsFileSystem | `\` | ACL 기반 | 드라이브 문자(`C:`) 지원 필요 |
| LinuxFileSystem | `/` | rwx 권한 모드(8진수) | 심볼릭 링크 처리 고려 |
| MacFileSystem | `/` | POSIX 권한 + 확장 속성 | 확장 속성(xattr) 저장 필요 |

## 과제 2: Flyweight 패턴 - 텍스트 렌더링

이 과제는 Flyweight 패턴으로 대량의 문자 객체를 효율적으로 렌더링하는 감각을 익히는 것이 목적이다. 문자, 폰트, 굵기, 기울임 등은 같은 조합이 문서 전체에서 반복되므로 내재적 상태로 캐싱하고, 좌표(x, y)만 외재적 상태로 매번 새로 전달한다. 100만 개 문자를 렌더링하더라도 실제 Flyweight 인스턴스 수는 (문자 × 폰트 조합) 수준에 그친다는 것을 메모리 측정으로 직접 확인하는 것이 이 과제의 핵심이다.

### 기본 구조

아래는 `CharacterFlyweightFactory.getFlyweight()`까지 포함한 완성 참조 구현이다. 나머지 과제(`TextDocument`, 성능 테스트)는 이 구조를 참고해 직접 구현한다.

```java
// Flyweight 인터페이스
public interface CharacterFlyweight {
    void render(RenderContext context, int x, int y);
    int getWidth(RenderContext context);
    int getHeight(RenderContext context);
}

// 실습 시 실제 렌더링 대상(Canvas, Graphics 등)에 맞게 교체해도 된다
public interface RenderContext {
    void drawChar(char c, String fontFamily, int fontSize, boolean bold, boolean italic, int x, int y);
    int measureWidth(char c, String fontFamily, int fontSize, boolean bold, boolean italic);
}

// 참조 구현: 내재적 상태(문자, 폰트, 크기, 굵기, 기울임)만 보유하는 구체 Flyweight
public class ConcreteCharacterFlyweight implements CharacterFlyweight {
    private final char character;
    private final String fontFamily;
    private final int fontSize;
    private final boolean isBold;
    private final boolean isItalic;

    public ConcreteCharacterFlyweight(char character, String fontFamily,
                                       int fontSize, boolean isBold, boolean isItalic) {
        this.character = character;
        this.fontFamily = fontFamily;
        this.fontSize = fontSize;
        this.isBold = isBold;
        this.isItalic = isItalic;
    }

    @Override
    public void render(RenderContext context, int x, int y) {
        // x, y는 외재적 상태이므로 매개변수로만 받고 저장하지 않는다
        context.drawChar(character, fontFamily, fontSize, isBold, isItalic, x, y);
    }

    @Override
    public int getWidth(RenderContext context) {
        return context.measureWidth(character, fontFamily, fontSize, isBold, isItalic);
    }

    @Override
    public int getHeight(RenderContext context) {
        return fontSize;
    }
}

// 팩토리 - 동일한 내재적 상태 조합은 캐싱해 재사용한다
public class CharacterFlyweightFactory {
    private final Map<String, CharacterFlyweight> flyweights = new ConcurrentHashMap<>();

    public CharacterFlyweight getFlyweight(char character, String fontFamily,
                                         int fontSize, boolean isBold, boolean isItalic) {
        String key = character + "_" + fontFamily + "_" + fontSize + "_" + isBold + "_" + isItalic;
        return flyweights.computeIfAbsent(key, k ->
            new ConcreteCharacterFlyweight(character, fontFamily, fontSize, isBold, isItalic));
    }

    public int getFlyweightCount() {
        return flyweights.size();
    }
}
```

### 구현 과제
- ConcreteCharacterFlyweight (내재적 상태 관리, 위 참조 구현 완료)
- TextDocument (외재적 상태 관리)
- 100만 개 문자 처리 성능 테스트

## 과제 3: 성능 비교

이 과제는 앞서 구현한 Bridge/Flyweight 패턴이 실제로 오버헤드나 절약 효과를 만들어내는지 수치로 검증하는 것이 목적이다. 패턴을 적용했다고 해서 항상 이득인 것은 아니며, 간접 호출 비용과 메모리 절약 사이의 트레이드오프를 직접 측정해봐야 언제 패턴을 쓸지 판단할 수 있다.

### 측정 항목
- Bridge: 직접 구현 vs 패턴 적용 시간 오버헤드
- Flyweight: 일반 구현 vs 패턴 적용 메모리 사용량
- 처리량과 응답 시간 비교

### 측정 결과를 판단에 반영하는 법

숫자를 얻는 것 자체가 목적이 아니라, 그 숫자로 "이 상황에서 패턴을 계속 쓸지"를 결정하는 것이 이 과제의 핵심이다. Bridge의 간접 호출 오버헤드가 파일 복사처럼 I/O가 지배적인 작업 시간에 비해 무시할 수준으로 나온다면, 오버헤드를 이유로 Bridge를 포기할 근거는 약하다. 반대로 초당 수백만 번 호출되는 순수 연산 경로에서 오버헤드 비율이 두 자릿수로 나온다면, 그 경로만 패턴 밖으로 빼내는 것을 고려해야 한다. Flyweight도 마찬가지로, 측정한 절약률이 문자·폰트 조합의 다양성에 크게 좌우된다는 점을 함께 기록해야 한다. 조합이 매우 다양해 캐시 재사용률이 낮으면 절약 효과가 기대만큼 크지 않을 수 있으므로, "몇 퍼센트 절약되었다"는 결과와 함께 "어떤 입력 분포에서 측정했는가"를 반드시 명시해야 재현 가능하고 신뢰할 수 있는 결론이 된다.

## 완성도 체크리스트

### Bridge 패턴
- [ ] 추상화와 구현 분리 — `FileManager`가 `FileSystemImpl`의 구체 클래스를 직접 참조하지 않고 인터페이스로만 의존하는지 확인
- [ ] 여러 플랫폼 구현체 작성 — Windows/Linux/Mac 세 구현체가 각자의 경로 구분자·권한 모델을 올바르게 반영하는지 확인
- [ ] 런타임 교체 기능 — 동일한 `FileManager` 인스턴스에서 구현체를 바꿔도 비즈니스 로직이 깨지지 않는지 확인
- [ ] 단위 테스트 작성 — 구현체별로 최소 1개 이상의 테스트가 있어 회귀를 잡아낼 수 있는지 확인

### Flyweight 패턴
- [ ] 내재적/외재적 상태 분리 — 좌표·색상 등 인스턴스별 값이 Flyweight 내부 필드에 저장되지 않는지 확인
- [ ] 팩토리 정상 동작 — 동일 키로 재요청 시 새 인스턴스가 아니라 캐시된 인스턴스가 반환되는지 확인
- [ ] 메모리 절약 확인 — Flyweight 적용 전/후 힙 사용량을 실측해 절약이 실제로 발생했는지 확인
- [ ] 대용량 처리 테스트 — 100만 개 문자 규모에서도 Flyweight 인스턴스 수가 문자·폰트 조합 수준에 머무는지 확인

### 성능 측정
- [ ] 오버헤드 측정 — Bridge 간접 호출과 직접 호출의 시간 차이를 벤치마크로 수치화했는지 확인
- [ ] 메모리 절약률 계산 — 일반 구현 대비 Flyweight의 절약률을 실측치로 제시했는지 확인
- [ ] 결과 분석 및 문서화 — 측정 환경(JVM 버전, 힙 설정 등)과 함께 결과를 기록해 재현 가능한지 확인

## 추가 도전 과제

1. Bridge + Strategy 결합으로 파일 압축 알고리즘 적용
2. Flyweight + Observer 결합으로 문서 변경 알림
3. JIT 최적화를 고려한 성능 개선

---

**실습 팁**
- 작은 단위로 구현하고 테스트
- 메모리 측정 도구(JProfiler, VisualVM) 활용
- JVM 워밍업 고려한 성능 측정
- 실제 사용 시나리오 기반 테스트 케이스 작성 