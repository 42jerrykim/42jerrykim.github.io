---
draft: true
---
# 4장: 주석과 문서화

## 강의 목표
- 주석의 적절한 사용법 이해
- 좋은 주석과 나쁜 주석 구분 능력 개발
- 코드 자체로 의도를 표현하는 능력 향상

## 주석에 대한 기본 철학

> **"나쁜 코드에 주석을 달지 마라. 새로 짜라." - Brian W. Kernighan & P.J. Plaugher**

주석은 필요악입니다. 프로그래밍 언어를 치밀하게 사용해 의도를 표현할 능력이 있다면, 주석은 거의 필요하지 않습니다. 주석은 언제나 실패를 의미합니다.

### 주석은 거짓말을 한다

코드는 변화하고 진화합니다. 하지만 주석이 언제나 코드를 따라가지는 않습니다. 주석이 코드에서 분리되어 점점 더 부정확한 고아로 변하는 사례가 너무도 흔합니다.

프로그래머들이 주석을 유지하고 보수하기란 현실적으로 불가능합니다. 코드를 변경할 때마다 주석도 바꿔야 한다면, 차라리 코드를 깔끔하게 정리하고 표현력을 강화하는 방향으로, 즉 주석이 필요 없는 방향으로 에너지를 쏟겠습니다.

## 주석은 나쁜 코드를 보완하지 못한다

코드에 주석을 추가하는 일반적인 이유는 코드 품질이 나쁘기 때문입니다. 모듈을 짜고 보니 짜임새가 엉망이고 알아먹기 어렵다. 그래서 자신에게 이렇게 말합니다. "이런! 주석을 달아야겠다!"

**주석을 달 시간에 코드를 정리하세요!**

표현력이 풍부하고 깔끔하며 주석이 거의 없는 코드가, 복잡하고 어수선하며 주석이 많이 달린 코드보다 훨씬 좋습니다.

## 코드로 의도를 표현하라

확실히 코드만으로 의도를 설명하기 어려운 경우가 존재합니다. 하지만 몇 초만 더 생각하면 코드로 대다수 의도를 표현할 수 있습니다.

```java
// Bad: 주석으로 의도 설명
// 직원에게 복지 혜택을 받을 자격이 있는지 검사한다.
if ((employee.flags & HOURLY_FLAG) && (employee.age > 65))

// Good: 코드로 의도 표현
if (employee.isEligibleForFullBenefits())
```

많은 경우 주석으로 달려는 설명을 함수로 만들어 표현해도 충분합니다.

## 좋은 주석

어떤 주석은 필요하거나 유익합니다. 하지만 정말로 좋은 주석은, 주석을 달지 않을 방법을 찾아낸 주석입니다.

### 4.3.1 법적인 주석
때로는 회사가 정립한 구현 표준에 맞춰 법적인 이유로 특정 주석을 넣으라고 명시합니다.

```java
// Copyright (C) 2003,2004,2005 by Object Mentor, Inc. All rights reserved.
// GNU General Public License 버전 2 이상을 따르는 조건으로 배포한다.
```

### 4.3.2 정보를 제공하는 주석
때로는 기본적인 정보를 주석으로 제공하면 편리합니다.

```java
// 테스트 중인 Responder 인스턴스를 반환한다.
protected abstract Responder responderInstance();

// kk:mm:ss EEE, MMM dd, yyyy 형식이다.
Pattern timeMatcher = Pattern.compile("\\d*:\\d*:\\d* \\w*, \\w* \\d*, \\d*");
```

하지만 이왕이면 함수 이름에 정보를 담는 편이 더 좋습니다:

```java
protected abstract Responder responderBeingTested();
```

### 4.3.3 의도를 설명하는 주석
때로는 주석이 구현을 이해하게 도와주는 선을 넘어 결정에 깔린 의도까지 설명합니다.

```java
public int compareTo(Object o) {
    if(o instanceof WikiPagePath) {
        WikiPagePath p = (WikiPagePath) o;
        String compressedName = StringUtil.join(names, "");
        String compressedArgumentName = StringUtil.join(p.names, "");
        return compressedName.compareTo(compressedArgumentName);
    }
    return 1; // 오른쪽 유형이므로 정렬 순위가 더 높다.
}
```

### 4.3.4 의미를 명료하게 밝히는 주석
때로는 모호한 인수나 반환값의 의미를 읽기 좋게 표현하면 이해하기 쉬워집니다.

```java
public void testCompareTo() throws Exception {
    WikiPagePath a = PathParser.parse("PageA");
    WikiPagePath ab = PathParser.parse("PageA.PageB");
    WikiPagePath b = PathParser.parse("PageB");
    WikiPagePath aa = PathParser.parse("PageA.PageA");
    WikiPagePath bb = PathParser.parse("PageB.PageB");
    WikiPagePath ba = PathParser.parse("PageB.PageA");
    
    assertTrue(a.compareTo(a) == 0);    // a == a
    assertTrue(a.compareTo(b) != 0);    // a != b
    assertTrue(ab.compareTo(ab) == 0);  // ab == ab
    assertTrue(a.compareTo(b) == -1);   // a < b
    assertTrue(aa.compareTo(ab) == -1); // aa < ab
    assertTrue(ba.compareTo(bb) == -1); // ba < bb
    assertTrue(b.compareTo(a) == 1);    // b > a
    assertTrue(ab.compareTo(aa) == 1);  // ab > aa
    assertTrue(bb.compareTo(ba) == 1);  // bb > ba
}
```

물론 그릇된 주석을 달아놓을 위험은 상당히 높습니다. 더 나은 방법이 있는지 고민하고 정확히 달도록 각별히 주의합니다.

### 4.3.5 결과를 경고하는 주석
때로 다른 프로그래머에게 결과를 경고할 목적으로 주석을 사용합니다.

```java
// 여유 시간이 충분하지 않다면 실행하지 마십시오.
public void _testWithReallyBigFile() {
    writeLinesToFile(10000000);
    
    response = responder.getResponse();
    // ...
}

public static SimpleDateFormat makeStandardHttpDateFormat() {
    // SimpleDateFormat은 스레드에 안전하지 못하다.
    // 따라서 각 인스턴스를 독립적으로 생성해야 한다.
    SimpleDateFormat df = new SimpleDateFormat("EEE, dd MMM yyyy HH:mm:ss z");
    df.setTimeZone(TimeZone.getTimeZone("GMT"));
    return df;
}
```

### 4.3.6 TODO 주석
때로는 '앞으로 할 일'을 TODO 주석으로 남겨두면 편합니다.

```java
// TODO-MdM 현재 필요하지 않다.
// 체크아웃 모델을 도입하면 함수가 필요 없다.
protected VersionInfo makeVersion() throws Exception {
    return null;
}
```

TODO 주석은 프로그래머가 필요하다 여기지만 당장 구현하기 어려운 업무를 기술합니다. 더 이상 필요 없는 기능을 삭제하라는 알림, 누군가에게 문제를 봐달라는 요청, 더 좋은 이름을 떠올려달라는 부탁, 앞으로 발생할 이벤트에 맞춰 코드를 고치라는 주의 등에 유용합니다.

하지만 어떤 용도로 사용하든 시스템에 나쁜 코드를 남겨 놓는 핑계가 되어서는 안 됩니다.

### 4.3.7 중요성을 강조하는 주석
자칫 대수롭지 않다고 여겨질 뭔가의 중요성을 강조하기 위해서도 주석을 사용합니다.

```java
String listItemContent = match.group(3).trim();
// 여기서 trim은 정말 중요하다. trim 함수는 문자열에서 시작 공백을 제거한다.
// 문자열에 시작 공백이 있으면 다른 문자열로 인식되기 때문이다.
new ListItemWidget(this, listItemContent, this.level + 1);
return buildList(text.substring(match.end()));
```

### 4.3.8 공개 API에서 Javadoc
설명이 잘 된 공개 API는 참으로 유용하고 만족스럽습니다. 표준 자바 라이브러리에서 사용한 Javadoc이 좋은 예입니다. Javadoc 없이는 자바 프로그램을 짜기 어려웠을 것입니다.

## 나쁜 주석

대다수 주석이 이 범주에 속합니다. 일반적으로 대다수 주석은 허술한 코드를 지탱하거나, 엉성한 코드를 변명하거나, 미숙한 결정을 합리화하는 등 프로그래머가 주절거리는 독백에서 크게 벗어나지 못합니다.

### 4.4.1 주절거리는 주석
특별한 이유 없이 의무감으로 혹은 프로세스에서 하라고 하니까 마지못해 주석을 단다면 전적으로 시간낭비입니다.

```java
public void loadProperties() {
    try {
        String propertiesPath = propertiesLocation + "/" + PROPERTIES_FILE;
        FileInputStream propertiesStream = new FileInputStream(propertiesPath);
        loadedProperties.load(propertiesStream);
    } catch(IOException e) {
        // 속성 파일이 없다면 기본값을 모두 메모리로 읽어 들인다.
    }
}
```

catch 블록에 있는 주석은 무슨 뜻일까요? 누가 기본값을 읽어 들이는가? loadedProperties.load를 호출하기 전에 읽어 들이는가? 아니면 loadedProperties.load가 파일을 읽어 들이기 전에 모든 기본값부터 읽어 들이는가? 아니면 catch 블록에서 예외를 잡아 기본값을 읽어 들이는가?

답을 알아내려면 다른 코드를 뒤져보는 수밖에 없습니다. 이해가 안 되어 다른 모듈까지 뒤져야 하는 주석은 독자와 제대로 소통하지 못하는 주석입니다.

### 4.4.2 같은 이야기를 중복하는 주석
코드 내용을 그대로 중복하는 주석이 있습니다.

```java
// this.closed가 true일 때 반환되는 유틸리티 메서드다.
// 타임아웃에 도달하면 예외를 던진다.
public synchronized void waitForClose(final long timeoutMillis) throws Exception {
    if(!closed) {
        wait(timeoutMillis);
        if(!closed)
            throw new Exception("MockResponseSender could not be closed");
    }
}
```

### 4.4.3 오해할 여지가 있는 주석
때때로 의도는 좋았으나 주석이 잘못된 정보를 제공하는 경우가 있습니다.

위의 `waitForClose` 메서드를 보면, this.closed가 true로 변하는 순간에 메서드는 반환되지 않습니다. this.closed가 true여야 메서드는 반환됩니다. 아니면 무조건 타임아웃을 기다렸다 this.closed가 그래도 true가 아니면 예외를 던집니다.

### 4.4.4 의무적으로 다는 주석
모든 함수에 Javadoc을 달거나 모든 변수에 주석을 달아야 한다는 규칙은 어리석기 그지없습니다.

```java
/**
 *
 * @param title CD 제목
 * @param author CD 저자
 * @param tracks CD 트랙 수
 * @param durationInMinutes CD 길이(단위: 분)
 */
public void addCD(String title, String author, int tracks, int durationInMinutes) {
    CD cd = new CD();
    cd.title = title;
    cd.author = author;
    cd.tracks = tracks;
    cd.duration = durationInMinutes;
    cdList.add(cd);
}
```

### 4.4.5 이력을 기록하는 주석
때때로 사람들이 모듈을 편집할 때마다 모듈 첫머리에 주석을 추가합니다.

```java
/**
 * 변경 이력 (11-Oct-2001부터)
 * --------------------------------
 * 11-Oct-2001 : 클래스를 다시 정리하고 새로운 패키징
 * 05-Nov-2001: getDescription() 메소드 추가
 * 이하 생략
 */
```

이제는 소스 코드 관리 시스템이 있으니 이런 주석은 제거하는 편이 좋습니다.

### 4.4.6 있으나 마나 한 주석
너무 당연한 사실을 언급하며 새로운 정보를 제공하지 못하는 주석입니다.

```java
/**
 * 기본 생성자
 */
protected AnnualDateRule() {
}

/**
 * 월 중 일자
 */
private int dayOfMonth;
```

### 4.4.7 무서운 잡음
때로는 Javadoc도 잡음입니다. 다음은 잘 알려진 오픈소스 라이브러리에서 가져온 코드입니다.

```java
/** The name. */
private String name;

/** The version. */
private String version;

/** The licenceName. */
private String licenceName;

/** The version. */
private String info;
```

잘라서 붙여넣기 오류가 보입니다. 주석을 달 때 주의를 기울이지 않는다면 이처럼 실수가 생깁니다.

### 4.4.8 함수나 변수로 표현할 수 있다면 주석을 달지 마라

```java
// Bad: 주석으로 설명
// 전역 목록 <smodule>에 속하는 모듈이 우리가 속한 하위 시스템에 의존하는가?
if (smodule.getDependSubsystems().contains(subSysMod.getSubSystem()))

// Good: 코드로 표현
ArrayList moduleDependees = smodule.getDependSubsystems();
String ourSubSystem = subSysMod.getSubSystem();
if (moduleDependees.contains(ourSubSystem))
```

### 4.4.9 위치를 표시하는 주석
때때로 프로그래머는 소스 파일에서 특정 위치를 표시하려 주석을 사용합니다.

```java
// Actions //////////////////////////////////
```

이런 배너는 가독성만 낮춥니다. 특히 뒷부분에 슬래시로 이어지는 잡음은 제거해야 마땅합니다.

### 4.4.10 닫는 괄호에 다는 주석
때로는 프로그래머가 닫는 괄호에 특별한 주석을 달아놓습니다.

```java
public class wc {
    public static void main(String[] args) {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        String line;
        int lineCount = 0;
        int charCount = 0;
        int wordCount = 0;
        try {
            while ((line = in.readLine()) != null) {
                lineCount++;
                charCount += line.length();
                String words[] = line.split("\\W");
                wordCount += words.length;
            } // while
            System.out.println("wordCount = " + wordCount);
            System.out.println("lineCount = " + lineCount);
            System.out.println("charCount = " + charCount);
        } // try
        catch (IOException e) {
            System.err.println("Error:" + e.getMessage());
        } // catch
    } // main
}
```

중첩이 심하고 장황한 함수라면 의미가 있을지도 모르지만 작고 캡슐화된 함수에는 잡음일 뿐입니다. 닫는 괄호에 주석을 달아야겠다는 생각이 든다면 대신에 함수를 줄이려 시도하자.

### 4.4.11 공로를 돌리거나 저자를 표시하는 주석
```java
/* 릭이 추가함 */
```

소스 코드 관리 시스템은 누가 언제 무엇을 추가했는지 귀신처럼 기억합니다. 저자 이름으로 코드를 오염시킬 필요가 없습니다.

### 4.4.12 주석으로 처리한 코드
주석으로 처리된 코드만큼 밉살스러운 관행도 드뭅니다.

```java
InputStreamResponse response = new InputStreamResponse();
response.setBody(formatter.getResultStream(), formatter.getByteCount());
// InputStream resultsStream = formatter.getResultStream();
// StreamReader reader = new StreamReader(resultsStream);
// response.setContent(reader.read(formatter.getByteCount()));
```

주석으로 처리한 코드는 다른 사람들이 지우기를 주저합니다. 이유가 있어 남겨놓았으리라고, 중요하니까 지우면 안 된다고 생각합니다. 그래서 질 나쁜 와인처럼 오래될수록 낡아갑니다.

이제는 소스 코드 관리 시스템이 우리를 대신해 코드를 기억해줍니다. 이제는 주석으로 처리할 필요가 없습니다. 그냥 코드를 삭제하세요.

### 4.4.13 HTML 주석
소스 코드에서 HTML 주석은 혐오 그 자체입니다.

```java
/**
 * 적합도 함수에서 사용하는 작업 설명입니다.
 * <p/>
 * 이 클래스는 다음과 같은 용도로 사용됩니다:
 * <ul>
 * <li>함수 실행</li>
 * <li>결과를 텍스트로 변환</li>
 * </ul>
 */
```

HTML은 편집기/IDE에서도 읽기 어렵습니다. 주석에 HTML 태그를 삽입해야 하는 책임은 프로그래머가 아니라 도구가 져야 합니다.

### 4.4.14 전역 정보
주석을 달아야 한다면 근처에 있는 코드만 기술하세요. 코드 일부에 주석을 달면서 시스템의 전반적인 정보를 기술하지 마세요.

```java
/**
 * 적합도 함수에서 사용하는 포트의 기본값.
 * 이 함수를 호출하는 코드가 먼저 setFitnessePort(int port)를 호출해
 * 포트를 설정해야 한다는 사실을 명심하라.
 */
public void setFitnessePort(int fitnessePort) {
    this.fitnessePort = fitnessePort;
}
```

### 4.4.15 너무 많은 정보
주석에다 흥미로운 역사나 관련 없는 정보를 장황하게 늘어놓지 마세요.

### 4.4.16 모호한 관계
주석과 주석이 설명하는 코드는 둘 사이 관계가 명백해야 합니다.

```java
/*
 * 모든 픽셀을 담을 만큼 충분한 배열로 시작한다(여기에 필터 바이트를 더한다).
 * 그리고 헤더 정보를 위해 200바이트를 더한다.
 */
this.pngBytes = new byte[((this.width + 1) * this.height * 3) + 200];
```

여기서 필터 바이트는 무엇일까요? +1과 관련이 있을까요? 아니면 *3과 관련이 있을까요? 아니면 둘 다? 한 픽셀이 한 바이트인가요? 200을 추가하는 이유는? 주석을 다는 목적은 코드만으로 설명이 부족해서입니다. 주석 자체가 다시 설명을 요구하니 안타깝기 그지없습니다.

### 4.4.17 함수 헤더
짧은 함수는 긴 설명이 필요 없습니다. 짧고 한 가지만 수행하며 이름을 잘 붙인 함수가 주석으로 헤더를 추가한 함수보다 훨씬 좋습니다.

### 4.4.18 비공개 코드에서 Javadoc
공개 API는 Javadoc이 유용하지만 공개하지 않을 코드라면 Javadoc은 쓸모가 없습니다. 시스템 내부에 속한 클래스와 함수에 Javadoc을 생성할 필요는 없습니다.

## 강의 진행 방식
1. **도입 (15분)**: 나쁜 주석 경험 사례 공유
2. **이론 (30분)**: 좋은 주석 vs 나쁜 주석 분류
3. **실습 (30분)**: 주석 제거 및 코드 개선 실습
4. **토론 (15분)**: 프로젝트에서의 주석 정책 수립

## 실습 과제
1. **주석 제거**: 나쁜 주석이 포함된 코드를 개선하여 주석 없이도 이해 가능하도록 수정
2. **주석 분류**: 제공된 코드의 주석들을 좋은 주석/나쁜 주석으로 분류하고 이유 설명
3. **문서화 정책**: 팀 프로젝트용 주석 작성 가이드라인 수립

## 평가 기준
- 주석 유형 분류 능력 (30%)
- 코드 개선을 통한 주석 제거 능력 (40%)
- 효과적인 주석 작성 능력 (30%)

## 주석 작성 체크리스트
**작성 전 확인사항:**
- [ ] 코드로 표현할 수 있는가?
- [ ] 함수명이나 변수명을 개선하면 주석이 불필요해지는가?
- [ ] 이 주석이 코드보다 읽기 쉬운가?

**작성 시 확인사항:**
- [ ] 정확한 정보를 제공하는가?
- [ ] 간결하고 명확한가?
- [ ] 코드와 일치하는가?
- [ ] 유지보수 시에도 정확성을 보장할 수 있는가?

**피해야 할 주석:**
- [ ] 코드 내용을 그대로 반복하는 주석
- [ ] 오해를 불러일으킬 수 있는 부정확한 주석
- [ ] 의무적으로 다는 형식적인 주석
- [ ] 이력이나 변경 사항을 기록하는 주석
- [ ] 당연한 내용을 설명하는 주석

## 실무 적용 팁
- **코드 리뷰**: 주석의 필요성과 적절성을 중점적으로 검토
- **리팩토링**: 주석이 필요한 코드는 개선의 여지가 있다고 판단
- **문서화 도구**: API 문서는 자동 생성 도구 활용
- **팀 컨벤션**: 주석 작성 가이드라인을 팀 내에서 명확히 정의

## 추가 자료
- "Clean Code" - Robert C. Martin의 주석 관련 챕터
- "Code Complete" - Steve McConnell의 문서화 가이드
- 각 언어별 문서화 도구 (Javadoc, Sphinx, JSDoc 등)
- 코드 주석 vs 외부 문서화의 역할 구분 