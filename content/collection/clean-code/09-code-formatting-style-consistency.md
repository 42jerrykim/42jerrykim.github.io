---
draft: true
---
# 5장: 형식 맞추기

## 강의 목표
- 코드 형식화의 목적과 중요성 이해
- 가독성을 높이는 형식화 원칙 습득
- 팀 차원의 일관된 코딩 스타일 수립 능력 개발

## 형식을 맞추는 목적

코드 형식은 중요합니다! 너무 중요하기 때문에 무시하기 어렵습니다. 형식은 의사소통의 일환이며, 의사소통은 전문 개발자의 일차적 의무입니다.

오늘 구현한 기능이 다음 버전에서 바뀔 확률은 아주 높습니다. 그런데 오늘 구현한 코드의 가독성은 앞으로 바뀔 코드의 품질에 지대한 영향을 미칩니다. 오랜 시간이 지나 원래 코드의 흔적을 더 이상 찾아보기 어려울 정도로 코드가 바뀌어도 맨 처음 잡아놓은 구현 스타일과 가독성 수준은 유지보수 용이성과 확장성에 계속 영향을 미칩니다.

원래 코드는 사라져도 개발자의 스타일과 규율은 사라지지 않습니다.

## 적절한 행 길이를 유지하라

소스 파일도 신문 기사와 비슷하게 작성합니다. 이름은 간단하면서도 설명이 가능하게 짓습니다. 이름만 보고도 올바른 모듈을 살펴보고 있는지 아닌지를 판단할 정도로 신경 써서 짓습니다.

### 5.1.1 신문 기사처럼 작성하라

소스 파일 첫 부분은 고차원 개념과 알고리즘을 설명합니다. 아래로 내려갈수록 의도를 세세하게 묘사합니다. 마지막에는 가장 저차원 함수와 세부 내역이 나옵니다.

### 5.1.2 개념은 빈 행으로 분리하라

거의 모든 코드는 왼쪽에서 오른쪽으로 그리고 위에서 아래로 읽힙니다. 각 행은 수식이나 절을 나타내고, 일련의 행 묶음은 완결된 생각 하나를 표현합니다. 생각 사이는 빈 행을 넣어 분리해야 마땅합니다.

```java
// Bad: 빈 행이 없어 구분이 어려움
package fitnesse.wikitext.widgets;
import java.util.regex.*;
public class BoldWidget extends ParentWidget {
    public static final String REGEXP = "'''.+?'''";
    private static final Pattern pattern = Pattern.compile("'''(.+?)'''",
        Pattern.MULTILINE + Pattern.DOTALL);
    public BoldWidget(ParentWidget parent, String text) throws Exception {
        super(parent);
        Matcher match = pattern.matcher(text);
        match.find();
        addChildWidgets(match.group(1));
    }
    public String render() throws Exception {
        StringBuffer html = new StringBuffer("<b>");
        html.append(childHtml()).append("</b>");
        return html.toString();
    }
}

// Good: 빈 행으로 개념 분리
package fitnesse.wikitext.widgets;

import java.util.regex.*;

public class BoldWidget extends ParentWidget {
    public static final String REGEXP = "'''.+?'''";
    
    private static final Pattern pattern = Pattern.compile("'''(.+?)'''",
        Pattern.MULTILINE + Pattern.DOTALL);
    
    public BoldWidget(ParentWidget parent, String text) throws Exception {
        super(parent);
        Matcher match = pattern.matcher(text);
        match.find();
        addChildWidgets(match.group(1));
    }
    
    public String render() throws Exception {
        StringBuffer html = new StringBuffer("<b>");
        html.append(childHtml()).append("</b>");
        return html.toString();
    }
}
```

### 5.1.3 세로 밀집도

줄바꿈이 개념을 분리한다면 세로 밀집도는 연관성을 의미합니다. 즉, 서로 밀접한 코드 행은 세로로 가까이 놓여야 한다는 뜻입니다.

```java
// Bad: 불필요한 주석으로 밀집도 방해
public class ReporterConfig {
    /**
     * 리포터 리스너의 클래스 이름
     */
    private String m_className;
    
    /**
     * 리포터 리스너의 속성
     */
    private List<Property> m_properties = new ArrayList<Property>();
    
    /**
     * 리포터 리스너의 속성을 추가한다.
     */
    public void addProperty(Property property) {
        m_properties.add(property);
    }
}

// Good: 밀접한 코드는 가까이
public class ReporterConfig {
    private String m_className;
    private List<Property> m_properties = new ArrayList<Property>();
    
    public void addProperty(Property property) {
        m_properties.add(property);
    }
}
```

### 5.1.4 수직 거리

서로 밀접한 개념은 세로로 가까이 둬야 합니다. 물론 두 개념이 서로 다른 파일에 속한다면 규칙이 통하지 않습니다. 하지만 타당한 근거가 없다면 서로 밀접한 개념은 한 파일에 속해야 마땅합니다. 이게 바로 protected 변수를 피해야 하는 이유 중 하나입니다.

**변수 선언**: 변수는 사용하는 위치에 최대한 가까이 선언합니다.

```java
// Good: 지역 변수는 각 함수 맨 처음에 선언
private static void readPreferences() {
    InputStream is = null;  // 변수를 맨 처음에 선언
    try {
        is = new FileInputStream(getPreferencesFile());
        setPreferences(new Properties(getPreferences()));
        getPreferences().load(is);
    } catch (IOException e) {
        try {
            if (is != null)
                is.close();
        } catch (IOException e1) {
        }
    }
}

// 루프를 제어하는 변수는 루프 문 내부에 선언
public int countTestCases() {
    int count = 0;
    for (Test each : tests)  // 루프 제어 변수
        count += each.countTestCases();
    return count;
}
```

**인스턴스 변수**: 클래스 맨 처음에 선언합니다. 변수 간에 세로로 거리를 두지 않습니다.

```java
// Good: 인스턴스 변수를 클래스 맨 처음에 선언
public class TestSuite implements Test {
    static public Test createTest(Class<? extends TestCase> theClass, String name) {
        // ...
    }
    
    public static Constructor<? extends TestCase> getTestConstructor(Class<? extends TestCase> theClass) throws NoSuchMethodException {
        // ...
    }
    
    public static Test warning(final String message) {
        // ...
    }
    
    private static String exceptionToString(Throwable t) {
        // ...
    }
    
    private String fName;           // 인스턴스 변수들
    private Vector<Test> fTests = new Vector<Test>(10);
    
    public TestSuite() {
    }
    
    public TestSuite(final Class<? extends TestCase> theClass) {
        // ...
    }
}
```

**종속 함수**: 한 함수가 다른 함수를 호출한다면 두 함수는 세로로 가까이 배치합니다. 또한 가능하다면 호출하는 함수를 호출되는 함수보다 먼저 배치합니다.

```java
public class WikiPageResponder implements SecureResponder {
    protected WikiPage page;
    protected PageData pageData;
    protected String pageTitle;
    protected Request request;
    protected PageCrawler crawler;
    
    public Response makeResponse(FitNesseContext context, Request request) throws Exception {
        String pageName = getPageNameOrDefault(request, "FrontPage");
        loadPage(pageName, context);
        if (page == null)
            return notFoundResponse(context, request);
        else
            return makePageResponse(context);
    }
    
    private String getPageNameOrDefault(Request request, String defaultPageName) {
        String pageName = request.getResource();
        if (StringUtil.isBlank(pageName))
            pageName = defaultPageName;
        return pageName;
    }
    
    protected void loadPage(String resource, FitNesseContext context) throws Exception {
        WikiPagePath path = PathParser.parse(resource);
        crawler = context.root.getPageCrawler();
        crawler.setDeadEndStrategy(new VirtualEnabledPageCrawler());
        page = crawler.getPage(context.root, path);
        if (page != null)
            pageData = page.getData();
    }
}
```

**개념적 유사성**: 어떤 코드 조각이 다른 코드 조각을 호출하는 관계가 없더라도 가까이 배치할 함수들이 있습니다.

```java
public class Assert {
    static public void assertTrue(String message, boolean condition) {
        if (!condition)
            fail(message);
    }
    
    static public void assertTrue(boolean condition) {
        assertTrue(null, condition);
    }
    
    static public void assertFalse(String message, boolean condition) {
        assertTrue(message, !condition);
    }
    
    static public void assertFalse(boolean condition) {
        assertFalse(null, condition);
    }
}
```

### 5.1.5 세로 순서

일반적으로 함수 호출 종속성은 아래 방향으로 유지합니다. 다시 말해, 호출되는 함수를 호출하는 함수보다 나중에 배치합니다. 그러면 소스 코드 모듈이 고차원에서 저차원으로 자연스럽게 내려갑니다.

## 가로 형식 맞추기

프로그래머는 명백하게 짧은 행을 선호합니다. 그러므로 짧은 행이 바람직합니다.

### 5.2.1 가로 공백과 밀집도

가로로는 공백을 사용해 밀접한 개념과 느슨한 개념을 표현합니다.

```java
private void measureLine(String line) {
    lineCount++;
    int lineSize = line.length();
    totalChars += lineSize;
    lineWidthHistogram.addLine(lineSize, lineCount);
    recordWidestLine(lineSize);
}
```

할당 연산자를 강조하려고 앞뒤에 공백을 줍니다. 할당문은 왼쪽 요소와 오른쪽 요소가 분명히 나뉩니다. 공백을 넣으면 두 가지 주요 요소가 확실히 나뉜다는 사실이 더욱 분명해집니다.

함수 이름과 이어지는 괄호 사이에는 공백을 넣지 않았습니다. 함수와 인수는 서로 밀접하기 때문입니다. 공백을 넣으면 한 개념이 아니라 별개로 보입니다.

### 5.2.2 가로 정렬

```java
// Bad: 가로 정렬은 엉뚱한 부분을 강조
public class FitNesseExpediter implements ResponseSender {
    private   Socket          socket;
    private   InputStream     input;
    private   OutputStream    output;
    private   Request         request;      
    private   Response        response;    
    private   FitNesseContext context;
    protected long            requestParsingTimeLimit;
    private   long            requestProgress;
    private   long            requestParsingDeadline;
    private   boolean         hasError;

// Good: 정렬하지 않으면 오히려 중요한 결함이 눈에 띈다
public class FitNesseExpediter implements ResponseSender {
    private Socket socket;
    private InputStream input;
    private OutputStream output;
    private Request request;
    private Response response;
    private FitNesseContext context;
    protected long requestParsingTimeLimit;
    private long requestProgress;
    private long requestParsingDeadline;
    private boolean hasError;
```

### 5.2.3 들여쓰기

소스 파일은 윤곽도(outline)와 계층이 비슷합니다. 파일 전체에 적용되는 정보가 있고, 파일 내 개별 클래스에 적용되는 정보가 있고, 클래스 내 각 메서드에 적용되는 정보가 있고, 블록 내 블록에 재귀적으로 적용되는 정보가 있습니다.

계층에서 각 수준은 이름을 선언하는 범위이자 선언문과 실행문을 해석하는 범위입니다.

**들여쓰기 무시하기**: 때로는 간단한 if 문, 짧은 while 문, 짧은 함수에서 들여쓰기 규칙을 무시하고픈 유혹이 생깁니다.

```java
// Bad: 들여쓰기 무시
public CommentWidget(ParentWidget parent, String text){super(parent, text);}
public String render() throws Exception {return "";}

// Good: 들여쓰기 적용
public CommentWidget(ParentWidget parent, String text) {
    super(parent, text);
}

public String render() throws Exception {
    return "";
}
```

## 팀 규칙

팀은 한 가지 규칙에 합의해야 합니다. 그리고 모든 팀원은 그 규칙을 따라야 합니다. 그래야 소프트웨어가 일관적인 스타일을 보입니다.

좋은 소프트웨어 시스템은 읽기 쉬운 문서로 이뤄진다는 사실을 기억하기 바랍니다. 스타일은 일관적이고 매끄러워야 합니다. 한 소스 파일에서 봤던 형식이 다른 소스 파일에도 쓰이리라는 신뢰감을 독자에게 줘야 합니다.

온갖 스타일을 뒤섞어 소스 코드를 필요 이상으로 복잡하게 만드는 실수는 반드시 피합니다.

## 밥 아저씨의 형식 규칙

다음은 본 저자가 사용하는 규칙입니다. 코드 자체가 최고의 구현 표준 문서가 되기를 바랍니다.

```java
public class CodeAnalyzer implements JavaFileAnalysis {
    private int lineCount;
    private int maxLineWidth;
    private int widestLineNumber;
    private LineWidthHistogram lineWidthHistogram;
    private int totalChars;
    
    public CodeAnalyzer() {
        lineWidthHistogram = new LineWidthHistogram();
    }
    
    public static List<File> findJavaFiles(File parentDirectory) {
        List<File> files = new ArrayList<File>();
        findJavaFiles(parentDirectory, files);
        return files;
    }
    
    private static void findJavaFiles(File parentDirectory, List<File> files) {
        for (File file : parentDirectory.listFiles()) {
            if (file.getName().endsWith(".java"))
                files.add(file);
            else if (file.isDirectory())
                findJavaFiles(file, files);
        }
    }
    
    public void analyzeFile(File javaFile) throws Exception {
        BufferedReader br = new BufferedReader(new FileReader(javaFile));
        String line;
        while ((line = br.readLine()) != null)
            measureLine(line);
    }
    
    private void measureLine(String line) {
        lineCount++;
        int lineSize = line.length();
        totalChars += lineSize;
        lineWidthHistogram.addLine(lineSize, lineCount);
        recordWidestLine(lineSize);
    }
    
    private void recordWidestLine(int lineSize) {
        if (lineSize > maxLineWidth) {
            maxLineWidth = lineSize;
            widestLineNumber = lineCount;
        }
    }
    
    public int getLineCount() {
        return lineCount;
    }
    
    public int getMaxLineWidth() {
        return maxLineWidth;
    }
    
    public int getWidestLineNumber() {
        return widestLineNumber;
    }
    
    public LineWidthHistogram getLineWidthHistogram() {
        return lineWidthHistogram;
    }
    
    public double getMeanLineWidth() {
        return (double)totalChars/lineCount;
    }
    
    public int getMedianLineWidth() {
        Integer[] sortedWidths = getSortedWidths();
        int cumulativeLineCount = 0;
        for (int width : sortedWidths) {
            cumulativeLineCount += lineCountForWidth(width);
            if (cumulativeLineCount > lineCount/2)
                return width;
        }
        throw new Error("Cannot get here");
    }
    
    private int lineCountForWidth(int width) {
        return lineWidthHistogram.getLinesforWidth(width).size();
    }
    
    private Integer[] getSortedWidths() {
        Set<Integer> widths = lineWidthHistogram.getWidths();
        Integer[] sortedWidths = (widths.toArray(new Integer[0]));
        Arrays.sort(sortedWidths);
        return sortedWidths;
    }
}
```

## 강의 진행 방식
1. **도입 (10분)**: 나쁜 형식의 코드 경험 공유
2. **이론 (25분)**: 형식화 원칙들 설명
3. **실습 (40분)**: 제공된 코드를 팀 규칙에 맞게 형식화
4. **그룹 활동 (15분)**: 팀 코딩 스타일 가이드 작성

## 실습 과제
1. **코드 형식화**: 형식이 엉망인 코드를 Clean Code 원칙에 맞게 개선
2. **스타일 가이드 작성**: 팀 프로젝트용 코딩 스타일 가이드 문서 작성
3. **형식 분석**: 오픈소스 프로젝트의 형식 규칙 분석 및 평가

## 평가 기준
- 형식화 원칙 이해도 (30%)
- 코드 형식 개선 능력 (40%)
- 팀 규칙 수립 능력 (30%)

## 형식화 체크리스트
- [ ] 파일 크기가 적절한가? (500줄 이내)
- [ ] 개념별로 빈 행으로 분리되었는가?
- [ ] 관련 코드가 세로로 가까이 배치되었는가?
- [ ] 변수 선언이 사용 위치 근처에 있는가?
- [ ] 종속 함수가 가까이 배치되었는가?
- [ ] 행 길이가 적절한가? (120자 이내)
- [ ] 가로 공백이 의미 있게 사용되었는가?
- [ ] 들여쓰기가 일관되게 적용되었는가?
- [ ] 팀 규칙에 따라 일관된 스타일인가?

## 현대적 형식화 도구
### 자동 포매터
- **Java**: Google Java Format, IntelliJ Formatter
- **Python**: Black, autopep8
- **JavaScript**: Prettier, ESLint
- **C++**: clang-format

### 설정 파일 예시
```json
// .prettierrc (JavaScript/TypeScript)
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

```python
# pyproject.toml (Python - Black)
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
```

### 린터와 통합
- **IDE 통합**: 실시간 형식 검사
- **Git Hooks**: 커밋 전 자동 형식화
- **CI/CD**: 빌드 과정에서 형식 검증

## 실무 적용 팁
- **에디터 설정**: 팀 전체가 동일한 에디터 설정 사용
- **자동화**: 수동 형식화보다는 도구 활용
- **코드 리뷰**: 형식 관련 피드백 최소화를 위한 자동화
- **점진적 적용**: 기존 코드는 점진적으로 개선

## 추가 자료
- Google Style Guides (Java, Python, C++, JavaScript)
- Airbnb JavaScript Style Guide
- PEP 8 (Python Style Guide)
- 각 언어별 공식 스타일 가이드 