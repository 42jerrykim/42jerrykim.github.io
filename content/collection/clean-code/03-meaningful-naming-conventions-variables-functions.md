---
draft: true
---
# 2장: 의미있는 네이밍

## 강의 목표
- 의도가 분명한 이름 짓기 원칙 습득
- 잘못된 정보를 전달하는 네이밍 패턴 식별
- 검색 가능하고 발음 가능한 이름 작성 능력 개발

## 의도를 분명히 밝히는 이름

좋은 이름을 지으려면 시간이 걸리지만 좋은 이름으로 절약하는 시간이 훨씬 더 많습니다. 변수나 함수 그리고 클래스 이름은 다음과 같은 질문에 모두 답해야 합니다:
- 왜 존재하는가?
- 무엇을 하는가?
- 어떻게 사용하는가?

따로 주석이 필요하다면 의도를 분명히 드러내지 못했다는 말입니다.

### 실습 예제: 다양한 언어에서의 네이밍

```java
// Java - Bad Naming
int d; // elapsed time in days
List<int[]> list1 = new ArrayList<int[]>();
for (int[] x : theList)
    if (x[0] == 4)
        list1.add(x);

// Java - Good Naming  
int elapsedTimeInDays;
List<Cell> flaggedCells = new ArrayList<Cell>();
for (Cell cell : gameBoard)
    if (cell.isFlagged())
        flaggedCells.add(cell);
```

```python
# Python - Bad Naming
def get_them(the_list):
    list1 = []
    for x in the_list:
        if x[0] == 4:
            list1.append(x)
    return list1

# Python - Good Naming
def get_flagged_cells(game_board):
    flagged_cells = []
    for cell in game_board:
        if cell.is_flagged():
            flagged_cells.append(cell)
    return flagged_cells
```

```javascript
// JavaScript - Bad Naming
function getThem(theList) {
    const list1 = [];
    for (const x of theList) {
        if (x[0] === 4) {
            list1.push(x);
        }
    }
    return list1;
}

// JavaScript - Good Naming
function getFlaggedCells(gameBoard) {
    const flaggedCells = [];
    for (const cell of gameBoard) {
        if (cell.isFlagged()) {
            flaggedCells.push(cell);
        }
    }
    return flaggedCells;
}
```

위 예제에서 보듯이, 좋은 이름은 코드의 맥락과 의도를 명확하게 드러냅니다.

## 그릇된 정보를 피하라

프로그래머는 코드에 그릇된 단서를 남겨서는 안 됩니다. 그릇된 단서는 코드 의미를 흐립니다.

### 피해야 할 네이밍 패턴

1. **널리 쓰이는 의미와 다른 단어 사용 금지**
   - `hp`, `aix`, `sco` (유닉스 플랫폼 이름과 혼동)
   
2. **실제 타입과 다른 이름 사용 금지**
   - `accountList` (실제로 List가 아닌 경우)
   - `accounts` 또는 `accountGroup`, `bunchOfAccounts` 등이 더 적합

3. **서로 흡사한 이름 사용 금지**
   - `XYZControllerForEfficientHandlingOfStrings` vs `XYZControllerForEfficientStorageOfStrings`
   - 유사한 개념은 유사한 표기법을 사용해야 함

4. **일관성 없는 철자 사용 금지**
   - 같은 개념을 때로는 `name`, 때로는 `nm`으로 표기하면 안 됨

## 의미 있게 구분하라

컴파일러나 인터프리터만 통과하려는 생각으로 코드를 구현하면 문제가 생깁니다.

### 연속된 숫자 덧붙이기 금지
```java
// Bad
public static void copyChars(char a1[], char a2[]) {
    for (int i = 0; i < a1.length; i++) {
        a2[i] = a1[i];
    }
}

// Good
public static void copyChars(char source[], char destination[]) {
    for (int i = 0; i < source.length; i++) {
        destination[i] = source[i];
    }
}
```

### 불용어(Noise Word) 추가 금지
`Product`라는 클래스가 있다면:
- `ProductInfo`와 `ProductData`는 의미가 불분명
- `ProductManager`와 `ProductHandler`는 구별이 어려움

읽는 사람이 차이를 알도록 이름을 지어야 합니다.

## 발음하기 쉬운 이름 사용하라

사람들은 단어에 능숙합니다. 발음하기 어려운 이름은 토론하기도 어렵습니다.

```java
// Bad: 발음하기 어려운 이름
class DtaRcrd102 {
    private Date genymdhms;
    private Date modymdhms;
    private final String pszqint = "102";
    // ...
}

// Good: 발음하기 쉬운 이름
class Customer {
    private Date generationTimestamp;
    private Date modificationTimestamp;
    private final String recordId = "102";
    // ...
}
```

이제 프로그래머들이 "generation timestamp"라고 말할 수 있습니다.

## 검색하기 쉬운 이름 사용하라

문자 하나를 사용하는 이름과 상수는 텍스트 코드에서 쉽게 눈에 띄지 않습니다.

### 검색의 어려움
- `e`라는 변수는 검색하기 어려움 (영어에서 가장 많이 쓰이는 문자)
- `7`이라는 숫자는 검색하기 어려움

### 개선 방법
```java
// Bad
for (int j = 0; j < 34; j++) {
    s += (t[j] * 4) / 5;
}

// Good
int realDaysPerIdealDay = 4;
const int WORK_DAYS_PER_WEEK = 5;
int sum = 0;
for (int j = 0; j < NUMBER_OF_TASKS; j++) {
    int realTaskDays = taskEstimate[j] * realDaysPerIdealDay;
    int realTaskWeeks = (realTaskDays / WORK_DAYS_PER_WEEK);
    sum += realTaskWeeks;
}
```

## 인코딩을 피하라

### 헝가리안 표기법 지양
현대 프로그래밍 언어는 컴파일러가 타입을 강제하며, 변수 이름에 타입을 인코딩할 필요가 없습니다.

```java
// Bad: 헝가리안 표기법
PhoneNumber phoneString;  // 타입이 바뀌어도 변수명은 바뀌지 않음

// Good: 깔끔한 이름
PhoneNumber phone;
```

### 멤버 변수 접두어 지양
```java
// Bad: 멤버 변수 접두어
public class Part {
    private String m_dsc; // 설명 문자열
    void setName(String name) {
        m_dsc = name;
    }
}

// Good: 깔끔한 이름
public class Part {
    private String description;
    void setName(String name) {
        this.description = name;
    }
}
```

### 인터페이스 클래스와 구현 클래스
인터페이스 이름은 접두어를 붙이지 않는 편이 좋습니다.

```java
// Bad
interface IShapeFactory { }
class ShapeFactory implements IShapeFactory { }

// Good
interface ShapeFactory { }
class ShapeFactoryImpl implements ShapeFactory { }
// 또는
class ConcreteShapeFactory implements ShapeFactory { }
```

## 자신의 기억력을 자랑하지 마라

문자 하나만 사용하는 변수 이름은 문제가 있습니다. 루프에서 반복 횟수를 세는 변수 `i`, `j`, `k`는 괜찮습니다(단, 루프 범위가 아주 작고 다른 이름과 충돌하지 않을 때만).

**명료함이 최고입니다.**

똑똑한 프로그래머와 전문 프로그래머 사이에서 나타나는 차이점 하나만 들자면, 전문 프로그래머는 **명료함이 최고**라는 사실을 이해합니다.

## 클래스 이름

클래스 이름과 객체 이름은 명사나 명사구가 적합합니다.
- **Good**: `Customer`, `WikiPage`, `Account`, `AddressParser`
- **Bad**: `Manager`, `Processor`, `Data`, `Info` (피하기)

동사는 사용하지 않습니다.

## 메서드 이름

메서드 이름은 동사나 동사구가 적합합니다.
- **Good**: `postPayment`, `deletePage`, `save`

접근자(Accessor), 변경자(Mutator), 조건자(Predicate)는 관례에 따라 값 앞에 `get`, `set`, `is`를 붙입니다.

```java
string name = employee.getName();
customer.setName("mike");
if (paycheck.isPosted()) {
    // ...
}
```

## 기발한 이름은 피하라

재미난 이름보다 명료한 이름을 선택하세요.
- `HolyHandGrenade` → `DeleteItems`
- `whack()` → `kill()`
- `eatMyShorts()` → `abort()`

**의도를 분명하고 솔직하게 표현하세요.**

## 한 개념에 한 단어를 사용하라

추상적인 개념 하나에 단어 하나를 선택해 이를 고수합니다.

- `fetch`, `retrieve`, `get`을 제각각 메서드 이름으로 사용하면 혼란스럽습니다.
- 일관성 있는 어휘를 사용하세요.

**메서드 이름은 독자적이고 일관적이어야 합니다.**

## 말장난을 하지 마라

한 단어를 두 가지 목적으로 사용하지 마세요.

예를 들어, 지금까지 `add`라는 메서드가 기존 값 두 개를 더하거나 이어서 새로운 값을 만든다고 가정합시다. 그런데 새로 작성하는 메서드는 집합에 값 하나를 추가합니다. 

이 메서드를 `add`라고 불러도 될까요? 아닙니다. `insert`나 `append`라는 이름이 적당합니다.

## 해법 영역에서 가져온 이름을 사용하라

코드를 읽을 사람도 프로그래머입니다. 따라서 전산 용어, 알고리즘 이름, 패턴 이름, 수학 용어 등을 사용해도 괜찮습니다.

- `JobQueue` (큐 자료구조를 알고 있는 프로그래머에게 의미 있음)
- `AccountVisitor` (VISITOR 패턴을 알고 있는 프로그래머에게 의미 있음)

## 문제 영역에서 가져온 이름을 사용하라

적절한 '프로그래머 용어'가 없다면 문제 영역에서 이름을 가져옵니다. 그러면 코드를 보수하는 프로그래머가 분야 전문가에게 의미를 물어볼 수 있습니다.

**우수한 프로그래머와 설계자라면 해법 영역과 문제 영역을 구분할 줄 알아야 합니다.**

## 의미 있는 맥락을 추가하라

스스로 의미가 분명한 이름이 있습니다. 하지만 대부분은 그렇지 못합니다. 그래서 클래스, 함수, 이름 공간에 넣어 맥락을 부여합니다. 모든 방법이 실패하면 마지막 수단으로 접두어를 붙입니다.

```java
// Bad: 맥락이 불분명
private void printGuessStatistics(char candidate, int count) {
    String number;
    String verb;
    String pluralModifier;
    if (count == 0) {
        number = "no";
        verb = "are";
        pluralModifier = "s";
    } else if (count == 1) {
        number = "1";
        verb = "is";
        pluralModifier = "";
    } else {
        number = Integer.toString(count);
        verb = "are";
        pluralModifier = "s";
    }
    String guessMessage = String.format(
        "There %s %s %s%s", verb, number, candidate, pluralModifier
    );
    print(guessMessage);
}

// Good: 맥락이 분명한 클래스로 개선
public class GuessStatisticsMessage {
    private String number;
    private String verb;
    private String pluralModifier;
    
    public String make(char candidate, int count) {
        createPluralDependentMessageParts(count);
        return String.format(
            "There %s %s %s%s", 
            verb, number, candidate, pluralModifier
        );
    }
    
    private void createPluralDependentMessageParts(int count) {
        if (count == 0) {
            thereAreNoLetters();
        } else if (count == 1) {
            thereIsOneLetter();
        } else {
            thereAreManyLetters(count);
        }
    }
    
    private void thereAreManyLetters(int count) {
        number = Integer.toString(count);
        verb = "are";
        pluralModifier = "s";
    }
    
    private void thereIsOneLetter() {
        number = "1";
        verb = "is";
        pluralModifier = "";
    }
    
    private void thereAreNoLetters() {
        number = "no";
        verb = "are";
        pluralModifier = "s";
    }
}
```

## 불필요한 맥락을 없애라

"고급 휘발유 충전소"(Gas Station Deluxe)라는 애플리케이션을 짠다고 가정하자. 모든 클래스 이름을 GSD로 시작하는 것은 바람직하지 않습니다.

일반적으로는 **짧은 이름이 긴 이름보다 좋습니다.** 단, 의미가 분명한 경우에 한해서입니다.

## 강의 진행 방식
1. **도입 (10분)**: 나쁜 네이밍으로 인한 경험담
2. **이론 (25분)**: 각 네이밍 원칙 설명
3. **실습 (40분)**: 코드 리팩토링 - 네이밍 개선
4. **그룹 활동 (15분)**: 팀별 네이밍 컨벤션 작성

## 실습 과제
1. **네이밍 리팩토링**: 제공된 나쁜 코드를 좋은 네이밍으로 개선
2. **네이밍 컨벤션 문서**: 팀 프로젝트용 네이밍 가이드라인 작성
3. **코드 리뷰**: 동료의 코드에서 네이밍 개선점 찾기

## 평가 기준
- 네이밍 원칙 이해도 (30%)
- 실제 코드 개선 능력 (40%)
- 네이밍 컨벤션 작성 품질 (30%)

## 네이밍 품질 체크리스트
- [ ] 변수/함수 이름만으로 용도를 알 수 있는가?
- [ ] 발음하기 쉬운가?
- [ ] 검색하기 쉬운가?
- [ ] 그릇된 정보를 담고 있지 않은가?
- [ ] 의미있게 구분되는가?
- [ ] 일관성 있는 네이밍 규칙을 따르는가?

## 언어별 네이밍 컨벤션
### Java
- 클래스: PascalCase (`UserService`)
- 메서드/변수: camelCase (`getUserName`)
- 상수: SCREAMING_SNAKE_CASE (`MAX_RETRY_COUNT`)

### Python  
- 클래스: PascalCase (`UserService`)
- 함수/변수: snake_case (`get_user_name`)
- 상수: SCREAMING_SNAKE_CASE (`MAX_RETRY_COUNT`)

### JavaScript
- 클래스: PascalCase (`UserService`)
- 함수/변수: camelCase (`getUserName`)
- 상수: SCREAMING_SNAKE_CASE (`MAX_RETRY_COUNT`)

## 실무 적용 팁
- **IDE 활용**: 리팩토링 도구를 사용한 안전한 이름 변경
- **코드 리뷰**: 네이밍을 중점적으로 검토하는 리뷰 프로세스
- **네이밍 사전**: 프로젝트별 용어 사전 관리
- **점진적 개선**: 기존 코드의 네이밍을 점진적으로 개선

## 추가 자료
- Google Style Guide (Java, Python, C++)
- 각 언어별 네이밍 컨벤션 표준
- 오픈소스 프로젝트의 네이밍 사례 연구 