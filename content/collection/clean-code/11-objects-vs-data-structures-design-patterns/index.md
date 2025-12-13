---
draft: true
---
# 6장: 객체와 자료구조

## 강의 목표
- 객체와 자료구조의 본질적 차이점 이해
- 적절한 추상화 수준 설정 능력 개발
- 디미터 법칙과 그 활용법 습득

## 자료 추상화

변수를 private으로 선언하더라도 각 값마다 조회(get) 함수와 설정(set) 함수를 제공한다면 구현을 외부로 노출하는 셈입니다.

### 구체적인 클래스 vs 추상적인 클래스

```java
// Bad: 구체적인 Vehicle 클래스
public class Vehicle {
    private double fuelTankCapacityInGallons;
    private double gallonsOfGasoline;
    
    public double getFuelTankCapacityInGallons() {
        return fuelTankCapacityInGallons;
    }
    
    public double getGallonsOfGasoline() {
        return gallonsOfGasoline;
    }
}

// Good: 추상적인 Vehicle 클래스
public interface Vehicle {
    double getPercentFuelRemaining();
}
```

첫 번째 클래스는 자동차 연료 상태를 구체적인 숫자 값으로 알려줍니다. 두 번째 클래스는 자동차 연료 상태를 백분율이라는 추상적인 개념으로 알려줍니다.

두 번째 클래스가 더 좋습니다. 자료를 세세하게 공개하기보다는 추상적인 개념으로 표현하는 편이 좋습니다. 인터페이스나 조회/설정 함수만으로는 추상화가 이뤄지지 않습니다. 개발자는 객체가 포함하는 자료를 표현할 가장 좋은 방법을 심각하게 고민해야 합니다.

## 자료/객체 비대칭

객체와 자료구조 사이에는 본질적인 차이가 있습니다.

- **객체**: 추상화 뒤로 자료를 숨긴 채 자료를 다루는 함수만 공개
- **자료구조**: 자료를 그대로 공개하며 별다른 함수는 제공하지 않음

두 정의는 본질적으로 상반됩니다.

### 절차적인 도형 클래스

```java
// 절차적인 방식
public class Square {
    public Point topLeft;
    public double side;
}

public class Rectangle {
    public Point topLeft;
    public double height;
    public double width;
}

public class Circle {
    public Point center;
    public double radius;
}

public class Geometry {
    public final double PI = 3.141592653589793;
    
    public double area(Object shape) throws NoSuchShapeException {
        if (shape instanceof Square) {
            Square s = (Square)shape;
            return s.side * s.side;
        } else if (shape instanceof Rectangle) {
            Rectangle r = (Rectangle)shape;
            return r.height * r.width;
        } else if (shape instanceof Circle) {
            Circle c = (Circle)shape;
            return PI * c.radius * c.radius;
        }
        throw new NoSuchShapeException();
    }
}
```

### 다형적인 도형 클래스

```java
// 다형적인 방식
public class Square implements Shape {
    private Point topLeft;
    private double side;
    
    public double area() {
        return side * side;
    }
}

public class Rectangle implements Shape {
    private Point topLeft;
    private double height;
    private double width;
    
    public double area() {
        return height * width;
    }
}

public class Circle implements Shape {
    private Point center;
    private double radius;
    private final double PI = 3.141592653589793;
    
    public double area() {
        return PI * radius * radius;
    }
}
```

### 두 방식의 장단점

**절차적인 코드의 장단점**:
- 기존 자료구조를 변경하지 않으면서 새 함수를 추가하기 쉽다
- 새로운 자료구조를 추가하기 어렵다 (모든 함수를 고쳐야 함)

**객체지향 코드의 장단점**:
- 기존 함수를 변경하지 않으면서 새 클래스를 추가하기 쉽다
- 새로운 함수를 추가하기 어렵다 (모든 클래스를 고쳐야 함)

> **객체 지향과 절차 지향은 상호 보완적입니다.** 복잡한 시스템을 짜다 보면 새로운 함수가 아니라 새로운 자료 타입이 필요한 경우가 생긴다. 이때는 클래스와 객체 지향 기법이 가장 적합하다. 반면, 새로운 자료 타입이 아니라 새로운 함수가 필요한 경우도 생긴다. 이때는 절차적인 코드와 자료 구조가 좀 더 적합하다.

## 디미터 법칙

디미터 법칙은 잘 알려진 휴리스틱으로, 모듈은 자신이 조작하는 객체의 속사정을 몰라야 한다는 법칙입니다.

객체는 자료를 숨기고 함수를 공개합니다. 즉, 객체는 조회 함수로 내부 구조를 공개하면 안 된다는 의미입니다.

### 기차 충돌 (Train Wreck)

다음과 같은 코드를 기차 충돌이라 부릅니다.

```java
// Bad: 기차 충돌
final String outputDir = ctxt.getOptions().getScratchDir().getAbsolutePath();
```

일반적으로 조잡하다 여겨지는 방식이므로 피하는 편이 좋습니다. 다음과 같이 나누는 편이 좋습니다.

```java
// Better: 나누어서 표현
Options opts = ctxt.getOptions();
File scratchDir = opts.getScratchDir();
final String outputDir = scratchDir.getAbsolutePath();
```

### 잡종 구조

이런 혼란으로 말미암아 때때로 절반은 객체, 절반은 자료구조인 잡종 구조가 나옵니다. 잡종 구조는 중요한 기능을 수행하는 함수도 있고, 공개 변수나 공개 조회/설정 함수도 있습니다.

덕택에 잡종 구조는 새로운 함수는 물론이고 새로운 자료구조도 추가하기 어렵습니다. 양쪽 세상에서 단점만 모아놓은 구조입니다. 그러므로 잡종 구조는 피하는 편이 좋습니다.

### 구조체 감추기

만약 ctxt, options, scratchDir이 진짜 객체라면? 그렇다면 앞서 코드 예제처럼 줄줄이 사탕으로 엮어서는 안 됩니다. 객체라면 내부 구조를 감춰야 하니까요.

```java
// Bad: 내부 구조 노출
ctxt.getAbsolutePathOfScratchDirectoryOption();

// Bad: ctxt 객체에 공개해야 하는 메서드가 너무 많아짐
ctxt.getScratchDirectoryOption().getAbsolutePath();
```

첫 번째 방법은 ctxt 객체에 공개해야 하는 메서드가 너무 많아집니다. 두 번째 방법은 getScratchDirectoryOption()이 객체가 아니라 자료구조를 반환한다고 가정합니다.

ctxt가 객체라면 **뭔가를 하라고** 말해야지 속을 드러내라고 말하면 안 됩니다.

```java
// Good: 의도를 명확히 표현
String outFile = outputDir + "/" + className + ".class";
FileOutputStream fout = new FileOutputStream(outFile);
BufferedOutputStream bos = new BufferedOutputStream(fout);

// 위 코드의 의도는 임시 파일을 생성하는 것
// 따라서 ctxt 객체에 임시 파일을 생성하라고 시키자
BufferedOutputStream bos = ctxt.createScratchFileStream(classFileName);
```

## 자료 전달 객체

자료구조체의 전형적인 형태는 공개 변수만 있고 함수가 없는 클래스입니다. 이런 자료구조체를 때로는 자료 전달 객체(Data Transfer Object, DTO)라 합니다.

DTO는 굉장히 유용한 구조체입니다. 특히 데이터베이스와 통신하거나 소켓에서 받은 메시지의 구문을 분석할 때 유용합니다.

### 빈(Bean) 구조

```java
// Bean 형태의 DTO
public class Address {
    private String street;
    private String streetExtra;
    private String city;
    private String state;
    private String zip;
    
    public Address(String street, String streetExtra, String city, String state, String zip) {
        this.street = street;
        this.streetExtra = streetExtra;
        this.city = city;
        this.state = state;
        this.zip = zip;
    }
    
    public String getStreet() {
        return street;
    }
    
    public String getStreetExtra() {
        return streetExtra;
    }
    
    public String getCity() {
        return city;
    }
    
    public String getState() {
        return state;
    }
    
    public String getZip() {
        return zip;
    }
}
```

### 활성 레코드

활성 레코드는 DTO의 특수한 형태입니다. 공개 변수가 있거나 비공개 변수에 조회/설정 함수가 있는 자료구조지만, 대개 save나 find와 같은 탐색 함수도 제공합니다.

```java
// 활성 레코드 예시
public class Employee {
    public String name;
    public String address;
    // ...
    
    public void save() {
        // 데이터베이스에 저장
    }
    
    public static Employee findById(int id) {
        // 데이터베이스에서 조회
        return null;
    }
}

// 비즈니스 규칙은 별도 객체에서
public class EmployeeService {
    private Employee employee;
    
    public void calculatePay() {
        // 급여 계산 로직
    }
    
    public void promoteEmployee() {
        // 승진 로직
    }
}
```

활성 레코드는 자료구조로 취급합니다. 비즈니스 규칙을 담으면서 내부 자료를 숨기는 객체는 따로 생성합니다.

## 결론

객체는 동작을 공개하고 자료를 숨깁니다. 그래서 기존 동작을 변경하지 않으면서 새 객체 타입을 추가하기는 쉬운 반면, 기존 객체에 새 동작을 추가하기는 어렵습니다.

자료구조는 별다른 동작 없이 자료를 노출합니다. 그래서 기존 자료구조에 새 동작을 추가하기는 쉬우나, 기존 함수에 새 자료구조를 추가하기는 어렵습니다.

시스템을 구현할 때, 새로운 자료 타입을 추가하는 유연성이 필요하면 객체가 더 적합합니다. 다른 경우로 새로운 동작을 추가하는 유연성이 필요하면 자료 구조와 절차적인 코드가 더 적합합니다.

우수한 소프트웨어 개발자는 편견 없이 이 사실을 이해해 직면한 문제에 최적인 해결책을 선택합니다.

## 강의 진행 방식
1. **도입 (10분)**: 절차적 코드 vs 객체지향 코드 경험 공유
2. **이론 (30분)**: 객체와 자료구조의 차이점 설명
3. **실습 (35분)**: 절차적 코드를 객체지향으로, 또는 그 반대로 리팩토링
4. **토론 (15분)**: 프로젝트에서 적절한 구조 선택 방법

## 실습 과제
1. **구조 변환**: 제공된 절차적 코드를 객체지향으로 변환 (또는 그 반대)
2. **디미터 법칙 적용**: 기차 충돌이 일어나는 코드를 디미터 법칙에 맞게 수정
3. **DTO 설계**: 실제 시스템에서 사용할 DTO와 비즈니스 객체 분리 설계

## 평가 기준
- 객체와 자료구조 구분 능력 (30%)
- 디미터 법칙 적용 능력 (35%)
- 적절한 구조 선택 능력 (35%)

## 설계 결정 가이드

### 객체를 선택해야 할 때
- [ ] 새로운 타입을 추가할 가능성이 높은가?
- [ ] 기존 함수 변경을 최소화해야 하는가?
- [ ] 데이터 은닉이 중요한가?
- [ ] 복잡한 비즈니스 로직이 있는가?

### 자료구조를 선택해야 할 때
- [ ] 새로운 함수를 추가할 가능성이 높은가?
- [ ] 기존 자료구조 변경을 최소화해야 하는가?
- [ ] 단순한 데이터 전달이 목적인가?
- [ ] 성능이 중요한 고려사항인가?

## 객체지향 설계 체크리스트
- [ ] 클래스가 데이터가 아닌 행동을 중심으로 설계되었는가?
- [ ] 구체적인 구현이 아닌 추상적인 인터페이스를 제공하는가?
- [ ] 디미터 법칙을 준수하는가?
- [ ] 기차 충돌 코드가 없는가?
- [ ] DTO와 비즈니스 객체가 명확히 구분되는가?
- [ ] 객체의 협력이 자연스럽게 이뤄지는가?
- [ ] 잡종 구조를 피하고 있는가?

## 실무 적용 팁
- **도메인 모델링**: 비즈니스 도메인을 객체로 표현
- **API 설계**: 외부 시스템과의 통신은 DTO 활용
- **계층 분리**: 프레젠테이션, 비즈니스, 데이터 계층 명확히 구분
- **리팩토링**: 절차적 코드에서 객체지향으로 점진적 변환

## 추가 자료
- Gang of Four "Design Patterns" - Strategy, Template Method 패턴
- Martin Fowler의 "Patterns of Enterprise Application Architecture" - DTO 패턴
- Domain-Driven Design에서의 Entity vs Value Object
- ORM 프레임워크에서의 Active Record vs Data Mapper 패턴 