---
collection_order: 14
title: "[Design Pattern] Template Method - 템플릿 메서드 패턴"
description: "Template Method 패턴은 알고리즘 구조를 상위 클래스에서 정의하고 하위 클래스에서 세부 구현을 제공합니다. 전체 흐름은 고정하고 특정 단계만 유연하게 변경합니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Template Method
  - 템플릿 메서드
  - Behavioral Pattern
  - 행위 패턴
  - GoF
  - Gang of Four
  - Algorithm Skeleton
  - 알고리즘 골격
  - Abstract Class
  - 추상 클래스
  - Hook Method
  - 훅 메서드
  - Inheritance
  - 상속
  - Polymorphism
  - 다형성
  - Inversion of Control
  - 제어 역전
  - Hollywood Principle
  - 할리우드 원칙
  - Code Reuse
  - 코드 재사용
  - DRY Principle
  - Framework
  - 프레임워크
  - Primitive Operation
  - 원시 연산
  - Final Method
  - 최종 메서드
  - Code Reusability
  - 코드 재사용성
  - Maintainability
  - 유지보수성
  - Software Design
  - 소프트웨어 설계
  - OOP
  - 객체지향 프로그래밍
  - Java
  - C++
  - Python
  - C#
  - Servlet
  - JUnit
  - Spring
  - Lifecycle
  - 생명주기
---

템플릿 메서드 패턴(Template Method Pattern)은 알고리즘의 골격을 상위 클래스에 정의하고, 일부 단계의 구현을 하위 클래스에 위임하는 행위 디자인 패턴이다. 이 패턴을 사용하면 알고리즘의 전체 구조를 변경하지 않으면서 특정 단계만 재정의할 수 있다.

## 개요

**템플릿 메서드 패턴의 정의**

템플릿 메서드 패턴은 상위 클래스에서 알고리즘의 뼈대를 정의하고, 세부 구현은 하위 클래스가 담당하도록 하는 패턴이다. "템플릿 메서드"는 알고리즘의 각 단계를 순서대로 호출하는 메서드이며, 일반적으로 final로 선언하여 하위 클래스가 변경하지 못하도록 한다.

**할리우드 원칙 (Hollywood Principle)**

"전화하지 마세요, 우리가 전화할게요(Don't call us, we'll call you)"라는 원칙으로, 상위 클래스가 하위 클래스의 메서드를 호출하는 제어 역전(Inversion of Control) 개념을 표현한다.

**패턴의 필요성 및 사용 사례**

템플릿 메서드 패턴은 다음과 같은 상황에서 유용하다:

- **코드 중복 제거**: 여러 클래스에서 비슷한 알고리즘이 반복될 때
- **확장 포인트 제공**: 프레임워크에서 사용자 코드가 끼어들 지점 제공
- **알고리즘 변형**: 전체 구조는 유지하면서 특정 단계만 변경
- **공통 로직 강제**: 모든 하위 클래스가 동일한 흐름을 따르도록 보장
- **훅 제공**: 선택적으로 확장 가능한 지점 제공

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 코드 중복 제거 | 상속에 의존하므로 유연성 제한 |
| 알고리즘 구조 강제 | 리스코프 치환 원칙 위반 가능성 |
| 확장 포인트 명확히 제공 | 단계가 많으면 유지보수 어려움 |
| 서브클래스의 구현 범위 제한 | 추상 메서드가 많으면 하위 클래스 부담 |

## 템플릿 메서드 패턴의 구성 요소

```
┌─────────────────────────────────────────────┐
│          AbstractClass                      │
├─────────────────────────────────────────────┤
│ + templateMethod() (final)                  │
│   ├── primitiveOperation1()                 │
│   ├── primitiveOperation2()                 │
│   ├── concreteOperation()                   │
│   └── hook()                                │
│                                             │
│ # primitiveOperation1() (abstract)          │
│ # primitiveOperation2() (abstract)          │
│ # concreteOperation()                       │
│ # hook() { }  // 기본 구현 (선택적)         │
└─────────────────────────────────────────────┘
                    △
                    │
         ┌──────────┴──────────┐
         │                     │
┌─────────────────┐  ┌─────────────────┐
│  ConcreteClassA │  │  ConcreteClassB │
├─────────────────┤  ├─────────────────┤
│ +primitiveOp1() │  │ +primitiveOp1() │
│ +primitiveOp2() │  │ +primitiveOp2() │
│ +hook()         │  │                 │
└─────────────────┘  └─────────────────┘
```

**1. AbstractClass (추상 클래스)**
- templateMethod(): 알고리즘의 골격을 정의 (final로 선언 권장)
- primitiveOperation(): 하위 클래스가 구현해야 하는 추상 메서드
- concreteOperation(): 공통 로직을 구현한 일반 메서드
- hook(): 선택적으로 오버라이드할 수 있는 메서드 (기본 구현 제공)

**2. ConcreteClass (구체 클래스)**
- 추상 메서드(primitiveOperation) 구현
- 필요시 훅 메서드 오버라이드

## 구현 예제

### Python 예제 - 데이터 마이닝 파이프라인

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import List, Dict, Any

# AbstractClass - 데이터 마이닝 템플릿
class DataMiner(ABC):
    """데이터 마이닝 알고리즘의 템플릿"""
    
    def mine(self, path: str) -> Dict[str, Any]:
        """템플릿 메서드 - 알고리즘의 골격"""
        raw_data = self.extract_data(path)
        parsed_data = self.parse_data(raw_data)
        
        if self.should_analyze():  # 훅 메서드
            analysis = self.analyze_data(parsed_data)
        else:
            analysis = {}
        
        report = self.create_report(parsed_data, analysis)
        self.send_report(report)  # 콘크리트 메서드
        
        return report
    
    @abstractmethod
    def extract_data(self, path: str) -> str:
        """원시 연산 - 데이터 추출"""
        pass
    
    @abstractmethod
    def parse_data(self, raw_data: str) -> List[Dict]:
        """원시 연산 - 데이터 파싱"""
        pass
    
    def analyze_data(self, data: List[Dict]) -> Dict[str, Any]:
        """콘크리트 연산 - 기본 분석 (오버라이드 가능)"""
        return {
            "count": len(data),
            "summary": "기본 분석 완료"
        }
    
    @abstractmethod
    def create_report(self, data: List[Dict], analysis: Dict) -> Dict[str, Any]:
        """원시 연산 - 리포트 생성"""
        pass
    
    def send_report(self, report: Dict[str, Any]) -> None:
        """콘크리트 연산 - 리포트 전송 (공통)"""
        print(f"📤 리포트 전송 완료: {report.get('title', 'Unknown')}")
    
    def should_analyze(self) -> bool:
        """훅 메서드 - 분석 수행 여부 (기본값: True)"""
        return True

# ConcreteClass - CSV 마이너
class CSVMiner(DataMiner):
    """CSV 파일 마이닝"""
    
    def extract_data(self, path: str) -> str:
        print(f"📂 CSV 파일 읽기: {path}")
        # 실제로는 파일을 읽음
        return "name,age,city\nAlice,30,Seoul\nBob,25,Busan\nCharlie,35,Incheon"
    
    def parse_data(self, raw_data: str) -> List[Dict]:
        print("📊 CSV 데이터 파싱 중...")
        lines = raw_data.strip().split('\n')
        headers = lines[0].split(',')
        data = []
        for line in lines[1:]:
            values = line.split(',')
            data.append(dict(zip(headers, values)))
        print(f"   파싱 완료: {len(data)}개 레코드")
        return data
    
    def create_report(self, data: List[Dict], analysis: Dict) -> Dict[str, Any]:
        return {
            "title": "CSV 데이터 리포트",
            "type": "csv",
            "records": len(data),
            "analysis": analysis
        }

# ConcreteClass - JSON 마이너
class JSONMiner(DataMiner):
    """JSON 파일 마이닝"""
    
    def extract_data(self, path: str) -> str:
        print(f"📂 JSON 파일 읽기: {path}")
        return '[{"name": "Alice", "score": 95}, {"name": "Bob", "score": 87}]'
    
    def parse_data(self, raw_data: str) -> List[Dict]:
        import json
        print("📊 JSON 데이터 파싱 중...")
        data = json.loads(raw_data)
        print(f"   파싱 완료: {len(data)}개 레코드")
        return data
    
    def analyze_data(self, data: List[Dict]) -> Dict[str, Any]:
        """커스텀 분석 로직"""
        scores = [d.get('score', 0) for d in data if 'score' in d]
        return {
            "count": len(data),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "max_score": max(scores) if scores else 0
        }
    
    def create_report(self, data: List[Dict], analysis: Dict) -> Dict[str, Any]:
        return {
            "title": "JSON 데이터 리포트",
            "type": "json",
            "records": len(data),
            "analysis": analysis
        }

# ConcreteClass - PDF 마이너 (분석 건너뛰기)
class PDFMiner(DataMiner):
    """PDF 파일 마이닝"""
    
    def extract_data(self, path: str) -> str:
        print(f"📂 PDF 파일 읽기: {path}")
        return "PDF 텍스트 내용..."
    
    def parse_data(self, raw_data: str) -> List[Dict]:
        print("📊 PDF 텍스트 파싱 중...")
        # 간단히 문단으로 분리
        paragraphs = raw_data.split('...')
        return [{"content": p.strip()} for p in paragraphs if p.strip()]
    
    def create_report(self, data: List[Dict], analysis: Dict) -> Dict[str, Any]:
        return {
            "title": "PDF 텍스트 리포트",
            "type": "pdf",
            "paragraphs": len(data),
            "analysis": analysis
        }
    
    def should_analyze(self) -> bool:
        """PDF는 분석 건너뛰기"""
        print("   ⏭ PDF 분석 건너뛰기")
        return False

# 사용 예제
if __name__ == "__main__":
    print("=== CSV 마이닝 ===")
    csv_miner = CSVMiner()
    csv_report = csv_miner.mine("data.csv")
    print(f"결과: {csv_report}\n")
    
    print("=== JSON 마이닝 ===")
    json_miner = JSONMiner()
    json_report = json_miner.mine("data.json")
    print(f"결과: {json_report}\n")
    
    print("=== PDF 마이닝 ===")
    pdf_miner = PDFMiner()
    pdf_report = pdf_miner.mine("document.pdf")
    print(f"결과: {pdf_report}")
```

### Java 예제 - 게임 초기화

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

// AbstractClass - 게임 템플릿
abstract class Game {
    
    // 템플릿 메서드 - final로 변경 불가
    public final void play() {
        initialize();
        startGame();
        
        while (!isGameOver()) {
            playTurn();
        }
        
        endGame();
        printWinner();
        
        if (shouldSaveScore()) {
            saveScore();
        }
    }
    
    // 원시 연산 - 하위 클래스에서 반드시 구현
    protected abstract void initialize();
    protected abstract void startGame();
    protected abstract void playTurn();
    protected abstract boolean isGameOver();
    protected abstract void endGame();
    protected abstract void printWinner();
    
    // 콘크리트 연산 - 공통 구현
    protected void saveScore() {
        System.out.println("🏆 점수가 저장되었습니다.");
    }
    
    // 훅 메서드 - 선택적 오버라이드
    protected boolean shouldSaveScore() {
        return true;
    }
}

// ConcreteClass - 체스 게임
class ChessGame extends Game {
    private int turn = 0;
    private static final int MAX_TURNS = 3; // 데모용
    
    @Override
    protected void initialize() {
        System.out.println("♟ 체스 보드 초기화");
        System.out.println("   백과 흑 말 배치 완료");
    }
    
    @Override
    protected void startGame() {
        System.out.println("♟ 체스 게임 시작! 백이 먼저 시작합니다.");
    }
    
    @Override
    protected void playTurn() {
        turn++;
        String player = (turn % 2 == 1) ? "백" : "흑";
        System.out.println("   " + player + "의 턴 (턴 " + turn + ")");
        // 실제로는 사용자 입력 처리
    }
    
    @Override
    protected boolean isGameOver() {
        return turn >= MAX_TURNS;
    }
    
    @Override
    protected void endGame() {
        System.out.println("♟ 체스 게임 종료");
    }
    
    @Override
    protected void printWinner() {
        System.out.println("🏆 백 승리!");
    }
}

// ConcreteClass - 틱택토 게임
class TicTacToeGame extends Game {
    private int moveCount = 0;
    private static final int MAX_MOVES = 4; // 데모용
    
    @Override
    protected void initialize() {
        System.out.println("⭕ 3x3 보드 초기화");
    }
    
    @Override
    protected void startGame() {
        System.out.println("⭕ 틱택토 시작! X가 먼저");
    }
    
    @Override
    protected void playTurn() {
        moveCount++;
        String player = (moveCount % 2 == 1) ? "X" : "O";
        System.out.println("   " + player + " 차례 (이동 " + moveCount + ")");
    }
    
    @Override
    protected boolean isGameOver() {
        return moveCount >= MAX_MOVES;
    }
    
    @Override
    protected void endGame() {
        System.out.println("⭕ 틱택토 게임 종료");
    }
    
    @Override
    protected void printWinner() {
        System.out.println("🏆 X 승리!");
    }
    
    @Override
    protected boolean shouldSaveScore() {
        // 틱택토는 점수 저장 안함
        return false;
    }
}

// 사용 예제
public class TemplateMethodDemo {
    public static void main(String[] args) {
        System.out.println("=== 체스 게임 ===");
        Game chess = new ChessGame();
        chess.play();
        
        System.out.println("\n=== 틱택토 게임 ===");
        Game ticTacToe = new TicTacToeGame();
        ticTacToe.play();
    }
}
```

### C# 예제 - 문서 변환기

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;

// AbstractClass - 문서 변환 템플릿
public abstract class DocumentConverter
{
    // 템플릿 메서드
    public void Convert(string sourcePath, string destPath)
    {
        Console.WriteLine($"\n{'=',(int)40}");
        Console.WriteLine($"변환 시작: {GetConverterName()}");
        Console.WriteLine($"{'=',(int)40}");
        
        // 1. 소스 파일 열기
        var document = OpenDocument(sourcePath);
        
        // 2. 유효성 검사 (훅)
        if (ShouldValidate())
        {
            ValidateDocument(document);
        }
        
        // 3. 문서 파싱
        var content = ParseDocument(document);
        
        // 4. 전처리 (훅)
        content = PreProcess(content);
        
        // 5. 형식 변환
        var converted = ConvertFormat(content);
        
        // 6. 후처리 (훅)
        converted = PostProcess(converted);
        
        // 7. 저장
        SaveDocument(converted, destPath);
        
        // 8. 정리
        Cleanup();
        
        Console.WriteLine($"✅ 변환 완료: {destPath}");
    }
    
    // 원시 연산 - 반드시 구현
    protected abstract string GetConverterName();
    protected abstract object OpenDocument(string path);
    protected abstract string ParseDocument(object document);
    protected abstract string ConvertFormat(string content);
    protected abstract void SaveDocument(string content, string path);
    
    // 훅 메서드 - 선택적 오버라이드
    protected virtual bool ShouldValidate() => true;
    
    protected virtual void ValidateDocument(object document)
    {
        Console.WriteLine("   📋 문서 유효성 검사 통과");
    }
    
    protected virtual string PreProcess(string content)
    {
        return content; // 기본: 변경 없음
    }
    
    protected virtual string PostProcess(string content)
    {
        return content; // 기본: 변경 없음
    }
    
    // 콘크리트 연산 - 공통 구현
    protected void Cleanup()
    {
        Console.WriteLine("   🧹 임시 파일 정리");
    }
}

// ConcreteClass - Word to PDF 변환기
public class WordToPdfConverter : DocumentConverter
{
    protected override string GetConverterName() => "Word → PDF 변환기";
    
    protected override object OpenDocument(string path)
    {
        Console.WriteLine($"   📂 Word 문서 열기: {path}");
        return new { Type = "Word", Content = "Word 문서 내용..." };
    }
    
    protected override string ParseDocument(object document)
    {
        Console.WriteLine("   📖 Word 문서 파싱");
        return "파싱된 Word 내용";
    }
    
    protected override string ConvertFormat(string content)
    {
        Console.WriteLine("   🔄 PDF 형식으로 변환");
        return $"[PDF] {content}";
    }
    
    protected override void SaveDocument(string content, string path)
    {
        Console.WriteLine($"   💾 PDF 파일 저장: {path}");
    }
    
    protected override string PostProcess(string content)
    {
        Console.WriteLine("   📐 PDF 페이지 최적화");
        return content + " (최적화됨)";
    }
}

// ConcreteClass - HTML to Markdown 변환기
public class HtmlToMarkdownConverter : DocumentConverter
{
    protected override string GetConverterName() => "HTML → Markdown 변환기";
    
    protected override object OpenDocument(string path)
    {
        Console.WriteLine($"   📂 HTML 파일 열기: {path}");
        return "<html><body><h1>제목</h1><p>내용</p></body></html>";
    }
    
    protected override string ParseDocument(object document)
    {
        Console.WriteLine("   📖 HTML DOM 파싱");
        return document.ToString();
    }
    
    protected override string ConvertFormat(string content)
    {
        Console.WriteLine("   🔄 Markdown 형식으로 변환");
        // 실제로는 HTML 태그를 Markdown으로 변환
        return content
            .Replace("<h1>", "# ")
            .Replace("</h1>", "\n")
            .Replace("<p>", "")
            .Replace("</p>", "\n")
            .Replace("<html><body>", "")
            .Replace("</body></html>", "");
    }
    
    protected override void SaveDocument(string content, string path)
    {
        Console.WriteLine($"   💾 Markdown 파일 저장: {path}");
    }
    
    protected override bool ShouldValidate()
    {
        // HTML은 유효성 검사 건너뛰기
        Console.WriteLine("   ⏭ HTML 유효성 검사 건너뛰기");
        return false;
    }
}

// ConcreteClass - JSON to XML 변환기
public class JsonToXmlConverter : DocumentConverter
{
    protected override string GetConverterName() => "JSON → XML 변환기";
    
    protected override object OpenDocument(string path)
    {
        Console.WriteLine($"   📂 JSON 파일 열기: {path}");
        return "{\"name\": \"John\", \"age\": 30}";
    }
    
    protected override string ParseDocument(object document)
    {
        Console.WriteLine("   📖 JSON 파싱");
        return document.ToString();
    }
    
    protected override string ConvertFormat(string content)
    {
        Console.WriteLine("   🔄 XML 형식으로 변환");
        return "<root><name>John</name><age>30</age></root>";
    }
    
    protected override void SaveDocument(string content, string path)
    {
        Console.WriteLine($"   💾 XML 파일 저장: {path}");
    }
    
    protected override string PreProcess(string content)
    {
        Console.WriteLine("   🔧 JSON 정규화");
        return content.Trim();
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("=== 문서 변환 시스템 ===");
        
        var wordConverter = new WordToPdfConverter();
        wordConverter.Convert("report.docx", "report.pdf");
        
        var htmlConverter = new HtmlToMarkdownConverter();
        htmlConverter.Convert("page.html", "page.md");
        
        var jsonConverter = new JsonToXmlConverter();
        jsonConverter.Convert("data.json", "data.xml");
    }
}
```

## 실제 사용 사례

### 1. Java Servlet doGet/doPost
```java
// HttpServlet의 service()가 템플릿 메서드
protected void service(req, resp) {
    if (method.equals("GET")) doGet(req, resp);
    else if (method.equals("POST")) doPost(req, resp);
}
```

### 2. JUnit Test Framework
```java
// TestCase의 runBare()가 템플릿 메서드
public void runBare() {
    setUp();
    runTest();
    tearDown();
}
```

### 3. Spring AbstractController
```java
public abstract class AbstractController {
    protected abstract ModelAndView handleRequestInternal(req, resp);
}
```

### 4. React 라이프사이클
```javascript
// componentDidMount, componentDidUpdate 등이 훅 역할
class MyComponent extends React.Component {
    componentDidMount() { }
    render() { }
}
```

## 관련 패턴

| 패턴 | 템플릿 메서드와의 관계 |
|------|---------------------|
| **Strategy** | Strategy는 합성, Template Method는 상속 |
| **Factory Method** | 템플릿 메서드의 특수한 형태 |
| **Hook** | 훅 메서드가 템플릿 메서드 패턴의 일부 |

## FAQ

**Q1: 템플릿 메서드 패턴과 전략 패턴의 차이점은?**

템플릿 메서드는 상속을 통해 알고리즘의 일부를 변경하고, 전략 패턴은 합성을 통해 전체 알고리즘을 교체합니다. 템플릿 메서드는 컴파일 타임에 결정되고, 전략은 런타임에 변경 가능합니다.

**Q2: 훅 메서드와 추상 메서드의 차이점은?**

추상 메서드는 반드시 구현해야 하지만, 훅 메서드는 기본 구현이 있어 선택적으로 오버라이드합니다. 훅은 확장 지점을 제공하면서도 구현을 강제하지 않습니다.

**Q3: 템플릿 메서드를 final로 선언해야 하나요?**

권장됩니다. 알고리즘의 골격이 변경되면 패턴의 의도가 훼손될 수 있습니다. 다만 특별한 이유가 있다면 오버라이드를 허용할 수 있습니다.

**Q4: 추상 메서드가 많아지면 어떻게 하나요?**

기본 구현을 가진 훅 메서드로 변경하거나, 상속 대신 합성(전략 패턴)을 고려하세요. 너무 많은 추상 메서드는 하위 클래스의 부담을 증가시킵니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- Java Servlet API 문서