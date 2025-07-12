---
draft: true
---
# 9장: 단위 테스트

## 강의 목표
- TDD의 핵심 원칙과 법칙 이해
- 깨끗하고 유지보수 가능한 테스트 코드 작성 능력 개발
- F.I.R.S.T 원칙을 통한 테스트 품질 향상

## 9.1 TDD 법칙 세 가지

Test-Driven Development는 다음 세 가지 법칙을 따릅니다:

- **첫 번째 법칙**: 실패하는 단위 테스트를 작성할 때까지 실제 코드를 작성하지 않는다
- **두 번째 법칙**: 컴파일은 실패하지 않으면서 실행이 실패하는 정도로만 단위 테스트를 작성한다
- **세 번째 법칙**: 현재 실패하는 테스트를 통과할 정도로만 실제 코드를 작성한다

### TDD 사이클 예시

```java
// Java (JUnit 5) - 1단계: Red - 실패하는 테스트 작성
@Test
public void testGetAreaOfRectangle() {
    Rectangle rectangle = new Rectangle(2, 3);
    assertEquals(6, rectangle.getArea());
}
// 컴파일 실패: Rectangle 클래스가 존재하지 않음

// 2단계: Green - 최소한의 코드로 테스트 통과
public class Rectangle {
    private int width, height;
    
    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }
    
    public int getArea() {
        return 6; // 일단 하드코딩으로 테스트 통과
    }
}

// 3단계: 다른 테스트 추가
@Test
public void testGetAreaOfDifferentRectangle() {
    Rectangle rectangle = new Rectangle(3, 4);
    assertEquals(12, rectangle.getArea());
}

// 4단계: Refactor - 올바른 구현으로 리팩토링
public class Rectangle {
    private int width, height;
    
    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }
    
    public int getArea() {
        return width * height; // 올바른 구현
    }
}
```

```python
# Python (pytest) - TDD 사이클
import pytest

# 1단계: Red - 실패하는 테스트
def test_get_area_of_rectangle():
    rectangle = Rectangle(2, 3)
    assert rectangle.get_area() == 6

# 2단계: Green - 최소한의 구현
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def get_area(self):
        return 6  # 하드코딩

# 3단계: 더 많은 테스트 추가
def test_get_area_of_different_rectangle():
    rectangle = Rectangle(3, 4)
    assert rectangle.get_area() == 12

# 4단계: Refactor - 일반화된 구현
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def get_area(self):
        return self.width * self.height
```

```javascript
// JavaScript (Jest) - TDD 사이클
// 1단계: Red - 실패하는 테스트
test('should calculate area of rectangle', () => {
    const rectangle = new Rectangle(2, 3);
    expect(rectangle.getArea()).toBe(6);
});

// 2단계: Green - 최소한의 구현
class Rectangle {
    constructor(width, height) {
        this.width = width;
        this.height = height;
    }
    
    getArea() {
        return 6; // 하드코딩
    }
}

// 3단계: 더 많은 테스트
test('should calculate area of different rectangle', () => {
    const rectangle = new Rectangle(3, 4);
    expect(rectangle.getArea()).toBe(12);
});

// 4단계: Refactor - 올바른 구현
class Rectangle {
    constructor(width, height) {
        this.width = width;
        this.height = height;
    }
    
    getArea() {
        return this.width * this.height;
    }
}
```

이 세 법칙을 따르면 개발과 테스트가 대략 30초 주기로 묶입니다. 테스트와 실제 코드가 함께 나올뿐더러 테스트가 실제 코드보다 불과 몇 초 전에 나옵니다.

## 9.2 깨끗한 테스트 코드 유지하기

테스트 코드는 실제 코드만큼이나 중요합니다. 이류 시민이 아닙니다. 테스트 코드는 사고와 설계와 주의가 필요합니다. 실제 코드 못지않게 깨끗하게 짜야 합니다.

### 테스트는 유연성, 유지보수성, 재사용성을 제공한다

테스트 코드가 지저분하면 변경하기 어려워집니다. 테스트 코드가 복잡할수록 실제 코드를 짜는 시간보다 테스트 케이스를 추가하는 시간이 더 걸리기 십상입니다.

실제 코드를 변경해 기존 테스트 케이스가 실패하기 시작하면, 지저분한 코드로 인해, 실패하는 테스트 케이스를 점검하는 과정에서 버그가 숨어드는 참사가 발생합니다.

**테스트 코드가 있다면 변경이 쉬워집니다!** 코드에 유연성, 유지보수성, 재사용성을 제공하는 버팀목이 바로 **단위 테스트**입니다. 이유는 단순합니다. 테스트 케이스가 있으면 변경이 두렵지 않기 때문입니다.

## 9.3 깨끗한 테스트 코드

깨끗한 테스트 코드를 만들려면? 세 가지가 필요합니다. **가독성, 가독성, 가독성.** 어쩌면 가독성은 실제 코드보다 테스트 코드에 더더욱 중요합니다.

```java
// Bad: 지저분한 테스트 코드
public void testGetPageHieratchyAsXml() throws Exception {
    crawler.addPage(root, PathParser.parse("PageOne"));
    crawler.addPage(root, PathParser.parse("PageOne.ChildOne"));
    crawler.addPage(root, PathParser.parse("PageTwo"));
    
    request.setResource("root");
    request.addInput("type", "pages");
    Responder responder = new SerializedPageResponder();
    SimpleResponse response = (SimpleResponse) responder.makeResponse(
        new FitNesseContext(root), request);
    String xml = response.getContent();
    
    assertEquals("text/xml", response.getContentType());
    assertSubString("<name>PageOne</name>", xml);
    assertSubString("<name>PageTwo</name>", xml);
    assertSubString("<name>ChildOne</name>", xml);
}

// Good: 깨끗한 테스트 코드
public void testGetPageHierarchyAsXml() throws Exception {
    makePages("PageOne", "PageOne.ChildOne", "PageTwo");
    
    submitRequest("root", "type:pages");
    
    assertResponseIsXML();
    assertResponseContains("<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>");
}
```

### BUILD-OPERATE-CHECK 패턴

위 테스트 코드는 BUILD-OPERATE-CHECK 패턴이 위와 같은 테스트 구조에 적합합니다.

1. **BUILD**: 테스트 자료를 만든다
2. **OPERATE**: 테스트 자료를 조작한다
3. **CHECK**: 조작한 결과가 올바른지 확인한다

### 도메인에 특화된 테스트 언어

도메인에 특화된 언어(DSL)로 테스트 코드를 구현하는 기법을 보여줍니다. 흔히 쓰는 시스템 조작 API를 사용하는 대신 API 위에다 함수와 유틸리티를 구현한 후 그 함수와 유틸리티를 사용하므로 테스트 코드를 짜기도 읽기도 쉬워집니다.

```java
// 도메인 특화 언어 예시
@Test
public void turnOnLoTempAlarmAtThreashold() throws Exception {
    hw.setTemp(WAY_TOO_COLD);
    controller.tic();
    assertTrue(hw.heaterState());
    assertTrue(hw.blowerState());
    assertFalse(hw.coolerState());
    assertFalse(hw.hiTempAlarm());
    assertTrue(hw.loTempAlarm());
}

// 더 읽기 쉬운 버전
@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
    wayTooCold();
    assertEquals("HBchL", hw.getState());
}

// 상태를 문자열로 표현: Heater/Blower/Cooler/hiTempAlarm/loTempAlarm
// 대문자는 켜짐, 소문자는 꺼짐
```

## 9.4 이중 표준

테스트 API 코드에 적용하는 표준은 실제 코드에 적용하는 표준과 확실히 다릅니다. 단순하고, 간결하고, 표현력이 풍부해야 하지만, 실제 코드만큼 효율적일 필요는 없습니다.

실제 환경이 아니라 테스트 환경에서 돌아가는 코드이기 때문인데, 실제 환경과 테스트 환경은 요구사항이 판이하게 다릅니다.

```java
// 실제 코드에서는 성능이 중요하지만 테스트에서는 가독성이 더 중요
@Test
public void turnOnCoolerAndBlowerIfTooHot() throws Exception {
    tooHot();
    assertEquals("hBChl", hw.getState());
}

@Test
public void turnOnHeaterAndBlowerIfTooCold() throws Exception {
    tooCold();
    assertEquals("HBchl", hw.getState());
}

@Test
public void turnOnHiTempAlarmAtThreshold() throws Exception {
    wayTooHot();
    assertEquals("hBCHl", hw.getState());
}

@Test
public void turnOnLoTempAlarmAtThreshold() throws Exception {
    wayTooCold();
    assertEquals("HBchL", hw.getState());
}
```

## 9.5 테스트 당 assert 하나

JUnit으로 테스트 코드를 짤 때는 함수마다 assert 문을 단 하나만 사용해야 한다고 주장하는 학파가 있습니다. 가혹하다 여길지 모르지만 확실히 장점이 있습니다. assert 문이 하나라면 결론이 하나기 때문에 코드를 이해하기 빠르고 쉽습니다.

```java
// Bad: 여러 assert
public void testGetPageHierarchyAsXml() throws Exception {
    givenPages("PageOne", "PageOne.ChildOne", "PageTwo");
    
    whenRequestIsIssued("root", "type:pages");
    
    thenResponseShouldBeXML();
    thenResponseShouldContain("<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>");
}

// Good: 단일 assert
public void testGetPageHierarchyAsXml() throws Exception {
    givenPages("PageOne", "PageOne.ChildOne", "PageTwo");
    whenRequestIsIssued("root", "type:pages");
    thenResponseShouldBeXML();
}

public void testGetPageHierarchyHasRightTags() throws Exception {
    givenPages("PageOne", "PageOne.ChildOne", "PageTwo");
    whenRequestIsIssued("root", "type:pages");
    thenResponseShouldContain("<name>PageOne</name>", "<name>PageTwo</name>", "<name>ChildOne</name>");
}
```

### 테스트 당 개념 하나

어쩌면 "테스트 함수마다 한 개념만 테스트하라"는 규칙이 더 낫겠습니다.

```java
// Bad: 한 테스트에서 여러 개념 테스트
public void testAddMonths() {
    SerialDate d1 = SerialDate.createInstance(31, 5, 2004);
    
    SerialDate d2 = SerialDate.addMonths(1, d1);
    assertEquals(30, d2.getDayOfMonth());
    assertEquals(6, d2.getMonth());
    assertEquals(2004, d2.getYYYY());
    
    SerialDate d3 = SerialDate.addMonths(2, d1);
    assertEquals(31, d3.getDayOfMonth());
    assertEquals(7, d3.getMonth());
    assertEquals(2004, d3.getYYYY());
    
    SerialDate d4 = SerialDate.addMonths(1, SerialDate.createInstance(31, 1, 2004));
    assertEquals(29, d4.getDayOfMonth());
    assertEquals(2, d4.getMonth());
    assertEquals(2004, d4.getYYYY());
}

// Good: 개념별로 분리
public void testAddOneMonthToEndOfMayGivesEndOfJune() {
    SerialDate d1 = SerialDate.createInstance(31, 5, 2004);
    SerialDate d2 = SerialDate.addMonths(1, d1);
    assertEquals(30, d2.getDayOfMonth());
    assertEquals(6, d2.getMonth());
    assertEquals(2004, d2.getYYYY());
}

public void testAddTwoMonthsToEndOfMayGivesEndOfJuly() {
    SerialDate d1 = SerialDate.createInstance(31, 5, 2004);
    SerialDate d3 = SerialDate.addMonths(2, d1);
    assertEquals(31, d3.getDayOfMonth());
    assertEquals(7, d3.getMonth());
    assertEquals(2004, d3.getYYYY());
}
```

## 9.6 F.I.R.S.T

깨끗한 테스트는 다음 다섯 가지 규칙을 따르는데, 각 규칙에서 첫 글자를 따오면 FIRST가 됩니다.

### Fast (빠르게)
테스트는 빨라야 합니다. 테스트는 빨리 돌아야 한다는 얘기입니다. 테스트가 느리면 자주 돌릴 엄두를 못 냅니다. 자주 돌리지 않으면 초반에 문제를 찾아내 고치지 못합니다. 코드를 마음껏 정리하지도 못합니다.

### Independent (독립적으로)
각 테스트를 서로 의존하면 안 됩니다. 한 테스트가 다음 테스트가 실행될 환경을 준비해서는 안 됩니다. 각 테스트는 독립적으로 그리고 어떤 순서로 실행해도 괜찮아야 합니다.

```java
// Bad: 테스트 간 의존성
public class UserServiceTest {
    private static User savedUser;
    
    @Test
    public void testCreateUser() {
        savedUser = userService.create("John", "john@example.com");
        assertNotNull(savedUser.getId());
    }
    
    @Test
    public void testUpdateUser() {
        // 이전 테스트에 의존!
        savedUser.setEmail("newemail@example.com");
        User updated = userService.update(savedUser);
        assertEquals("newemail@example.com", updated.getEmail());
    }
}

// Good: 독립적인 테스트
public class UserServiceTest {
    @Test
    public void testCreateUser() {
        User user = userService.create("John", "john@example.com");
        assertNotNull(user.getId());
    }
    
    @Test
    public void testUpdateUser() {
        // 각 테스트마다 필요한 데이터 준비
        User user = userService.create("John", "john@example.com");
        user.setEmail("newemail@example.com");
        User updated = userService.update(user);
        assertEquals("newemail@example.com", updated.getEmail());
    }
}
```

### Repeatable (반복 가능한)
테스트는 어떤 환경에서도 반복 가능해야 합니다. 실제 환경, QA 환경, 버스를 타고 집으로 가는 길에 사용하는 노트북 환경(네트워크가 연결되지 않은)에서도 실행할 수 있어야 합니다.

### Self-Validating (자가검증하는)
테스트는 부울(bool) 값으로 결과를 내야 합니다. 성공 아니면 실패입니다. 통과 여부를 알리고 로그 파일을 읽게 만들어서는 안 됩니다. 통과 여부를 보려고 텍스트 파일 두 개를 수동으로 비교하게 만들어서도 안 됩니다.

### Timely (적시에)
테스트는 적시에 작성해야 합니다. 단위 테스트는 테스트하려는 실제 코드를 구현하기 직전에 구현합니다. 실제 코드를 구현한 다음에 테스트 코드를 만들면 실제 코드가 테스트하기 어렵다는 사실을 발견할지도 모릅니다.

## 현대적 테스팅 프레임워크와 도구

### Java 생태계
- **JUnit 5**: 현대적 테스트 프레임워크
- **Mockito**: 모킹 프레임워크
- **TestContainers**: 통합 테스트용 컨테이너
- **AssertJ**: 유창한 assertion 라이브러리

```java
// JUnit 5 + AssertJ 예시
@Test
@DisplayName("사용자 생성 시 올바른 정보가 설정되어야 한다")
void shouldCreateUserWithCorrectInformation() {
    // Given
    String name = "John Doe";
    String email = "john@example.com";
    
    // When
    User user = new User(name, email);
    
    // Then
    assertThat(user.getName()).isEqualTo(name);
    assertThat(user.getEmail()).isEqualTo(email);
    assertThat(user.getId()).isNotNull();
}
```

### Python 생태계
- **pytest**: 강력하고 유연한 테스트 프레임워크
- **pytest-mock**: 모킹 기능
- **hypothesis**: 속성 기반 테스트
- **factory_boy**: 테스트 데이터 생성

```python
# pytest 예시
def test_user_creation():
    # Given
    name = "John Doe"
    email = "john@example.com"
    
    # When
    user = User(name, email)
    
    # Then
    assert user.name == name
    assert user.email == email
    assert user.id is not None

# 파라미터화된 테스트
@pytest.mark.parametrize("width,height,expected", [
    (2, 3, 6),
    (4, 5, 20),
    (0, 10, 0),
])
def test_rectangle_area(width, height, expected):
    rectangle = Rectangle(width, height)
    assert rectangle.get_area() == expected
```

### JavaScript 생태계
- **Jest**: React 생태계 표준 테스트 프레임워크
- **Vitest**: 빠른 테스트 실행
- **Testing Library**: 사용자 중심 테스트
- **Cypress**: E2E 테스트

```javascript
// Jest 예시
describe('User', () => {
    test('should create user with correct information', () => {
        // Given
        const name = 'John Doe';
        const email = 'john@example.com';
        
        // When
        const user = new User(name, email);
        
        // Then
        expect(user.name).toBe(name);
        expect(user.email).toBe(email);
        expect(user.id).toBeDefined();
    });
    
    test.each([
        [2, 3, 6],
        [4, 5, 20],
        [0, 10, 0],
    ])('should calculate area correctly: %i × %i = %i', (width, height, expected) => {
        const rectangle = new Rectangle(width, height);
        expect(rectangle.getArea()).toBe(expected);
    });
});
```

## 강의 진행 방식
1. **도입 (10분)**: 테스트 코드 경험 및 TDD 소개
2. **이론 (25분)**: TDD 법칙과 깨끗한 테스트 원칙
3. **실습 (45분)**: TDD 사이클로 간단한 기능 구현
4. **코드 리뷰 (10분)**: 테스트 코드 품질 검토

## 실습 과제
1. **TDD 실습**: Red-Green-Refactor 사이클로 계산기 구현
2. **테스트 리팩토링**: 지저분한 테스트 코드를 깨끗하게 개선
3. **F.I.R.S.T 원칙 적용**: 기존 테스트를 F.I.R.S.T 원칙에 맞게 수정

## 평가 기준
- TDD 사이클 이해도 (30%)
- 테스트 코드 품질 (40%)
- F.I.R.S.T 원칙 적용 (30%)

## 테스트 품질 체크리스트
- [ ] 테스트가 빠르게 실행되는가?
- [ ] 각 테스트가 독립적으로 실행 가능한가?
- [ ] 어떤 환경에서든 반복 실행 가능한가?
- [ ] 테스트 결과가 명확한가? (성공/실패)
- [ ] 실제 코드보다 먼저 작성되었는가?
- [ ] 하나의 개념만 테스트하는가?
- [ ] 테스트 이름이 명확한가?
- [ ] Given-When-Then 구조가 명확한가?
- [ ] 도메인 특화 언어를 활용했는가?

## 실무 적용 팁
- **커버리지 도구**: 코드 커버리지 측정으로 테스트 완성도 확인
- **CI/CD 통합**: 자동화된 테스트 실행 환경 구축
- **테스트 피라미드**: 단위 테스트 > 통합 테스트 > E2E 테스트 비율 유지
- **변이 테스트**: 테스트의 품질을 검증하는 고급 기법
- **테스트 더블**: Mock, Stub, Fake 등을 적절히 활용

## 추가 자료
- Kent Beck의 "Test Driven Development: By Example"
- Martin Fowler의 "Mocks Aren't Stubs" 글
- 각 언어별 테스팅 프레임워크 공식 문서
- Google Testing Blog
- 테스트 피라미드와 테스트 전략에 관한 자료 