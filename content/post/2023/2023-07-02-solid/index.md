---
image: "tmp_wordcloud.png"
categories: null
date: "2023-07-02T00:00:00Z"
header:
  teaser: https://images.velog.io/images/haero_kim/post/169ef81a-0c8c-4241-a73a-135d5b67ffea/1_XOMTPWTpDLypkp079p9XXg.png
tags:
- SOLIDPrinciples
- SoftwareDevelopment
- Object-Oriented Programming
- CodeQuality
- SoftwareDesign
- ProgrammingBestPractices
- CodeMaintainability
- ScalableCode
- Robert C. Martin
- UncleBob
- SoftwareEngineering
- CodingPrinciples
- CodeReusability
- CodeReadability
- DependencyInversion
- InterfaceSegregation
- LiskovSubstitution
- Open/Closed Principle
- SingleResponsibilityPrinciple
- CodeRefactoring
title: '[Software] SOLID 원칙 이해 - 유지 관리가 가능하고 확장 가능한 코드의 핵심'
---

SOLID 원칙은 소프트웨어 커뮤니티에서 밥 아저씨라는 애칭으로 잘 알려진 Robert C. Martin에 의해 소개되었습니다. 그의 연구는 소프트웨어 업계에 큰 영향을 미쳤으며, 이러한 원칙은 많은 개발자가 소프트웨어를 설계하고 제작할 때 초석이 되었습니다. SOLID 원칙은 단순한 이론적 개념이 아니라 실용적인 지침으로, 이를 준수하면 더 강력하고 유연하며 이해하기 쉬운 코드를 만들 수 있습니다.

|![](https://images.velog.io/images/haero_kim/post/169ef81a-0c8c-4241-a73a-135d5b67ffea/1_XOMTPWTpDLypkp079p9XXg.png)|
|:---:|
|Solid 그림|

## 소개

소프트웨어 개발 영역에서는 보다 효율적이고 유지 관리가 용이하며 견고한 코드를 만들기 위해 몇 가지 원칙을 따릅니다. 이러한 원칙 중 SOLID 원칙은 특별한 위치를 차지합니다. SOLID는 객체 지향 프로그래밍 및 설계의 5가지 중요한 원칙을 요약한 약어입니다. 이러한 원칙은 관리, 이해 및 확장이 용이한 소프트웨어를 작성하기 위한 강력한 기반을 제공합니다.

다음 섹션에서는 이러한 각 원칙을 자세히 살펴보면서 그 의미와 중요성, 실제 적용 사례를 살펴봅니다. 숙련된 개발자이든 이 분야의 초보자이든 이러한 원칙을 이해하고 적용하면 코딩 기술과 제작하는 소프트웨어의 품질이 향상될 것입니다.

## 단일 책임 원칙(SRP)

SOLID 약어의 첫 글자는 단일 책임 원칙(SRP)을 나타냅니다. 이 원칙은 "클래스는 변경할 이유가 하나만 있어야 한다"는 것을 말합니다. 즉, 코드의 각 클래스는 하나의 역할 또는 책임만 가져야 한다는 뜻입니다. 이 원칙은 개발자가 프로그램을 각각 특정 기능을 처리하는 별개의 부분으로 나누도록 권장합니다.

이 원칙을 설명하기 위해 실제 레스토랑의 예를 생각해 보겠습니다. 레스토랑에는 요리사, 웨이터, 계산원 등 다양한 역할이 있습니다. 각 사람은 특정 업무를 담당합니다. 요리사는 음식을 준비하고, 웨이터는 손님에게 서빙을 하며, 계산원은 계산을 처리합니다. 만약 요리사가 서빙과 결제까지 담당한다면 비효율적일 뿐만 아니라 오류가 발생하기 쉽습니다. 마찬가지로 소프트웨어 개발에서도 각 클래스가 단일 책임을 맡으면 시스템이 더 체계적이고 관리하기 쉬워집니다.

SRP를 적용하면 몇 가지 이점이 있습니다. 첫째, 코드 유지 관리가 더 쉬워집니다. 각 클래스가 단일 책임을 맡으면 코드베이스를 탐색하고 변경하기가 더 쉬워집니다. 특정 기능을 변경해야 하는 경우 어떤 클래스를 수정해야 하는지 정확히 알 수 있습니다. 따라서 코드의 다른 부분에 버그가 발생할 위험이 줄어듭니다.

둘째, SRP는 코드의 가독성을 향상시킵니다. 각 클래스가 단일 작업에 집중하면 코드가 더 간단하고 이해하기 쉬워집니다. 이는 다른 개발자가 코드를 더 빨리 이해할 수 있으므로 팀에서 작업할 때 특히 유용합니다.

마지막으로 SRP를 준수하면 코드베이스가 더 유연하고 적응력이 높아집니다. 기능이 서로 다른 클래스로 분리되어 있으면 코드의 다른 부분에 영향을 주지 않고 기능을 추가, 제거 또는 수정하기가 더 쉬워집니다. 이러한 적응성은 요구 사항이 빠르게 변화하는 오늘날의 급변하는 소프트웨어 개발 환경에서 매우 중요합니다.

결론적으로, 단일 책임 원칙은 더 깔끔하고 체계적이며 효율적인 코드베이스를 만드는 것입니다. 코드를 더 쉽게 읽고, 유지 관리하고, 확장하여 더 나은 소프트웨어와 원활한 개발 프로세스로 이어지게 하는 것입니다.

급여 시스템에서 '직원' 클래스를 생각해 봅시다. 이 클래스는 이름, 아이디, 급여와 같은 직원 데이터와 관련된 책임만 가져야 합니다. 이 클래스에 직원 데이터를 데이터베이스에 저장하거나 보고서를 인쇄하는 메서드를 추가하면 SRP를 위반하게 됩니다. 이러한 책임은 `EmployeeDB` 및 `EmployeeReport`와 같은 별도의 클래스로 이동해야 합니다.

```python
class Employee:
    def __init__(self, id, name, salary):
        self.id = id
        self.name = name
        self.salary = salary

class EmployeeDB:
    def save_employee(self, employee):
        # code to save employee to database

class EmployeeReport:
    def generate_report(self, employee):
        # code to generate report
```

## 개방/폐쇄 원리(OCP)

SOLID 약어의 두 번째 원칙은 개방/폐쇄 원칙(OCP)입니다. 이 원칙은 "소프트웨어 엔티티(클래스, 모듈, 함수 등)는 확장을 위해서는 개방적이어야 하지만 수정을 위해서는 폐쇄적이어야 한다"고 주장합니다. 즉, 기존 코드를 변경하지 않고도 클래스에 새로운 기능이나 동작을 추가할 수 있어야 한다는 뜻입니다.

이 원칙을 설명하기 위해 스마트폰의 예를 생각해 보세요. 스마트폰은 기본적으로 다양한 작업을 수행하도록 설계되었지만, 확장할 수 있도록 설계되었습니다. 스마트폰의 운영 체제나 하드웨어를 수정할 필요 없이 앱 스토어에서 앱을 다운로드하여 스마트폰에 새로운 기능을 추가할 수 있습니다. 이것이 바로 기존 코드를 수정하지 않고 기능을 확장할 수 있는 개방형/폐쇄형 원칙의 핵심입니다.

개방형/폐쇄형 원칙을 구현하면 몇 가지 이점이 있습니다. 첫째, 코드의 안정성이 향상됩니다. 기존 클래스를 수정하지 않고 확장하여 새로운 기능을 추가하면 기존 기능에 새로운 버그가 발생할 위험이 줄어듭니다. 이는 작은 변경이 예기치 않은 파급 효과를 가져올 수 있는 대규모 코드베이스에서 특히 중요합니다.

둘째, 개방형/폐쇄형 원칙은 코드의 변경량을 최소화합니다. 새로운 기능을 추가해야 하는 경우 기존 클래스를 변경하는 대신 기존 클래스를 상속하는 새 클래스를 생성하면 됩니다. 이렇게 하면 코드베이스의 복잡성이 줄어들어 코드 관리 및 유지 관리가 더 쉬워집니다.

마지막으로, 개방형/폐쇄형 원칙은 코드 재사용성을 촉진합니다. 클래스를 확장 가능하도록 설계하면 새로운 기능에 기존 코드를 재사용할 수 있으므로 작성해야 하는 코드의 양을 줄이고 코드베이스를 더욱 효율적으로 만들 수 있습니다.

결론적으로, 개방형/폐쇄형 원칙은 안정적이고 유지 관리가 쉬우며 효율적인 소프트웨어를 만드는 것입니다. 소프트웨어 엔티티를 확장에는 개방적이지만 수정에는 폐쇄적으로 설계하면 기존 기능을 방해하지 않으므로 안심하고 새로운 기능을 추가할 수 있습니다.

`Shape` 클래스와 `AreaCalculator` 클래스를 생각해 봅시다. 서로 다른 도형의 면적을 계산해야 하는 경우, (새로운 도형을 추가하여) 확장할 수 있도록 클래스를 개방형으로 설계하고 (`AreaCalculator` 클래스를 변경하지 않고) 수정할 수 있도록 폐쇄형으로 설계할 수 있습니다.

```python
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * (self.radius ** 2)

class AreaCalculator:
    def total_area(self, shapes):
        total = 0
        for shape in shapes:
            total += shape.area()
        return total
```

## 리스코프의 대체 원리(LSP)

SOLID 약어의 세 번째 원칙은 리스코프의 대체 원칙(LSP)입니다. 이 원칙은 "파생 또는 자식 클래스는 기본 또는 부모 클래스로 대체할 수 있어야 한다"는 것입니다. 즉, 상위 클래스의 객체는 프로그램의 정확성에 영향을 주지 않고 하위 클래스의 객체로 대체할 수 있어야 합니다.

이 원칙을 설명하기 위해 새의 예를 생각해 보겠습니다. 간단한 모델에서 먹기, 날기 등의 메서드를 가진 Bird 클래스가 있을 수 있습니다. Pigeon이라는 서브클래스가 있다면 다른 새와 마찬가지로 먹고 날 수 있으므로 아무런 문제 없이 Bird로 대체할 수 있습니다. 그러나 다른 하위 클래스 펭귄이 있다면 먹기는 가능하지만 날지는 못합니다. 비행이 예상되는 상황에서 새를 펭귄으로 대체하려고 하면 문제가 발생합니다. 이는 리스코프 치환 원칙에 위배됩니다.

리스코프 치환 원칙은 상속을 사용할 때 시스템의 무결성을 유지하는 데 매우 중요합니다. 이 원칙은 서브클래스가 예상치 못한 동작 없이 슈퍼클래스를 대신할 수 있도록 보장합니다. 따라서 슈퍼클래스가 사용되는 모든 곳에서 올바르게 작동할 것이라는 확신을 가지고 새로운 서브클래스를 도입할 수 있으므로 코드의 유연성이 향상됩니다.

LSP를 준수하면 코드 유지 관리도 더 쉬워집니다. 모든 서브클래스가 슈퍼클래스를 대체할 수 있는 경우 메서드를 호출하기 전에 클래스의 유형을 확인할 필요가 없습니다. 따라서 코드의 복잡성이 줄어들고 이해와 유지 관리가 더 쉬워집니다.

결론적으로, 리스코프 대체 원칙은 코드에서 상속이 올바르게 사용되도록 하여 보다 유연하고 유지 관리하기 쉬운 시스템을 만드는 것입니다. 서브클래스가 항상 슈퍼클래스를 대체할 수 있도록 보장함으로써 보다 강력하고 안정적인 코드베이스를 만들 수 있습니다.

`fly` 메서드를 가진 `Bird` 클래스를 생각해봅시다. 만약 날 수 없는 서브클래스 `Penguin`이 있다면, `Bird` 객체가 예상되는 모든 곳에서 `Penguin` 객체를 사용하려고 하면 LSP를 위반하게 됩니다.

```python
class Bird:
    def fly(self):
        pass

class Penguin(Bird):
    pass

penguin = Penguin()
penguin.fly()  # This should not be possible, as penguins can't fly
```

## 인터페이스 분리 원칙(ISP)

SOLID 약어의 네 번째 원칙은 인터페이스 분리 원칙(ISP)입니다. 이 원칙은 "클라이언트와 무관한 인터페이스를 구현하도록 강요하지 않는다"는 것입니다. 즉, 하나의 범용 인터페이스보다는 여러 개의 특정 인터페이스를 사용하는 것이 더 낫다는 것을 의미합니다.

이 원칙을 설명하기 위해 레스토랑 메뉴의 예를 생각해 보겠습니다. 채식주의자라면 채식 메뉴와 비채식 메뉴가 모두 포함된 일반 메뉴보다는 채식 메뉴만 포함된 메뉴를 선호할 것입니다. 마찬가지로 소프트웨어 개발에서도 고객이 사용하지 않는 인터페이스에 의존하도록 강요해서는 안 됩니다. 이 원칙은 고객 요구 사항에 맞는 집중적인 인터페이스를 만드는 것입니다.

인터페이스 분리 원칙을 준수하면 몇 가지 이점이 있습니다. 첫째, 변경으로 인한 부작용을 줄일 수 있습니다. 인터페이스가 변경되면 해당 인터페이스에 의존하는 모든 클라이언트도 변경해야 할 수 있습니다. 인터페이스를 작고 집중적으로 유지하면 변경으로 인해 영향을 받는 클라이언트 수를 최소화할 수 있습니다.

둘째, ISP는 읽기 쉽고 유지 관리하기 쉬운 코드를 장려합니다. 인터페이스가 작고 집중되어 있으면 각 인터페이스가 무엇을 하고 어떻게 사용되는지 더 쉽게 이해할 수 있습니다. 이렇게 하면 코드를 탐색하고 유지 관리하기가 더 쉬워집니다.

마지막으로, 인터페이스 분리 원칙은 보다 유연하고 적응력 있는 코드베이스로 이어집니다. 인터페이스가 작고 집중되어 있으면 코드의 다른 부분에 영향을 주지 않고 기능을 추가, 제거 또는 수정하기가 더 쉽습니다.

결론적으로 인터페이스 분리 원칙은 유지 관리가 쉽고 유연하며 견고한 소프트웨어를 만드는 것입니다. 인터페이스를 작고 집중적으로 설계하면 탐색, 이해 및 수정하기 쉬운 코드베이스를 만들 수 있습니다.

`print`, `fax`, `scan` 메서드가 있는 `Printer` 인터페이스를 생각해 봅시다. 인쇄만 지원하는 `SimplePrinter` 클래스가 있다면, 이 클래스는 `fax`와 `scan` 메서드를 강제로 구현해야 하므로 ISP를 위반하게 됩니다. 대신 각 기능에 대해 별도의 인터페이스를 만들어야 합니다.

```python
class Printer:
    def print(self):
        pass

class Fax:
    def fax(self):
        pass

class Scanner:
    def scan(self):
        pass

class SimplePrinter(Printer):
    def print(self):
        # code to print

class MultiFunctionPrinter(Printer, Fax, Scanner):
    def print(self):
        # code to print

    def fax(self):
        # code to fax

    def scan(self):
        # code to scan
```

## 의존성 반전 원리(DIP)

SOLID 약어의 마지막 원칙은 의존성 반전 원칙(DIP)입니다. 이 원칙은 "상위 레벨 모듈/클래스는 하위 레벨 모듈/클래스에 의존해서는 안 된다. 둘 다 추상화에 의존해야 합니다." 본질적으로 이 원칙은 코드 모듈 간의 종속성을 줄이는 것입니다.

더 자세히 살펴보기 전에 의존성 반전이 의존성 주입과 동일하지 않다는 점을 명확히 하는 것이 중요합니다. 두 개념 모두 종속성 관리를 다루지만, 종속성 주입은 종속성 반전을 달성하기 위한 기술입니다. 종속성 주입은 하나의 객체가 종속성을 획득하는 방법에 관한 것이고, 종속성 반전은 특정 클래스와 인터페이스가 서로 의존하는 수준에 관한 것입니다.

종속성 반전 원리를 설명하기 위해 TV 리모컨과 배터리를 예로 들어 보겠습니다. 리모컨은 특정 브랜드의 배터리에 종속되지 않습니다. 필요한 사양을 충족하는 모든 브랜드의 배터리를 사용할 수 있습니다. 이 경우 리모컨(상위 모듈)은 특정 배터리 브랜드(하위 모듈)에 의존하지 않습니다. 대신, 둘 다 필요한 전압을 제공하는 전원이라는 개념이라는 추상화에 의존합니다.

종속성 반전 원칙을 적용하면 몇 가지 이점이 있습니다. 첫째, 코드 재사용성이 향상됩니다. 상위 수준 모듈이 구체적인 하위 수준 모듈이 아닌 추상화에 종속되어 있으면 동일한 추상화를 따르는 다른 하위 수준 모듈에서 이러한 상위 수준 모듈을 재사용하기가 더 쉬워집니다.

둘째, DIP는 모듈 간의 결합을 줄입니다. 모듈이 추상화에 의존하는 경우 한 모듈의 변경 사항이 다른 모듈에 영향을 미칠 가능성이 적습니다. 따라서 코드가 더 견고해지고 유지 관리가 더 쉬워집니다.

마지막으로 종속성 반전 원칙은 보다 유연하고 적응력 있는 코드베이스를 촉진합니다. 모듈이 추상화에 의존하는 경우 코드의 다른 부분에 영향을 주지 않고 새로운 기능을 도입하거나 기존 기능을 수정하기가 더 쉽습니다.

결론적으로 종속성 반전 원칙은 강력하고 유연하며 유지 관리가 쉬운 소프트웨어를 만드는 것입니다. 상위 수준 모듈이 하위 수준 모듈이 아닌 추상화에 종속되도록 하면 관리, 이해 및 수정이 더 쉬운 코드베이스를 만들 수 있습니다.

`LightBulb` 클래스와 `Switch` 클래스를 생각해 봅시다. `Switch` 클래스가 `LightBulb` 클래스에 직접 종속되어 있다면 다른 종류의 전구로 전환하기 어려울 것입니다. 추상화(`SwitchableDevice`)에 의존하면 전환되는 장치의 유형을 쉽게 변경할 수 있습니다.

```python
class SwitchableDevice:
    def turn_on

(self):
        pass

    def turn_off(self):
        pass

class LightBulb(SwitchableDevice):
    def turn_on(self):
        print("LightBulb: Bulb turned on...")

    def turn_off(self):
        print("LightBulb: Bulb turned off...")

class Fan(SwitchableDevice):
    def turn_on(self):
        print("Fan: Fan turned on...")

    def turn_off(self):
        print("Fan: Fan turned off...")

class ElectricSwitch:
    def __init__(self, device):
        self.device = device
        self.on = False

    def press(self):
        if self.on:
            self.device.turn_off()
            self.on = False
        else:
            self.device.turn_on()
            self.on = True

lightbulb = LightBulb()
switch = ElectricSwitch(lightbulb)
switch.press()  # Output: "LightBulb: Bulb turned on..."
switch.press()  # Output: "LightBulb: Bulb turned off..."

fan = Fan()
switch = ElectricSwitch(fan)
switch.press()  # Output: "Fan: Fan turned on..."
switch.press()  # Output: "Fan: Fan turned off..."
```

이 예제에서 `ElectricSwitch` 클래스는 `LightBulb` 또는 `Fan` 클래스에 직접 종속되지 않습니다. 대신 `SwitchableDevice` 추상화에 의존합니다. 따라서 종속성 반전 원칙을 준수하여 `ElectricSwitch` 클래스를 변경하지 않고도 다른 유형의 장치로 쉽게 전환할 수 있습니다.

## FAQ

다음은 SOLID 원칙에 대해 자주 묻는 질문(FAQ)입니다:

**1. SOLID 원칙이란 무엇인가요?**

SOLID 원칙은 객체 지향 프로그래밍 및 설계의 5가지 원칙을 말합니다. 다음과 같습니다:

- 단일 책임 원칙(SRP)
- 개방형/폐쇄형 원칙(OCP)
- 리스코프 대체 원칙(LSP)
- 인터페이스 분리 원칙(ISP)
- 의존성 반전 원칙(DIP)

이러한 원칙은 유지 관리, 이해 및 확장이 용이한 소프트웨어를 설계하기 위한 지침을 제공합니다.

**2. 누가 SOLID 원칙을 도입했나요?**

SOLID 원칙은 밥 아저씨라고도 알려진 로버트 C. 마틴이 소개했습니다. 그는 소프트웨어 개발 분야에 큰 공헌을 한 소프트웨어 엔지니어이자 강사입니다.

**3. SOLID 원칙이 중요한 이유는 무엇인가요?**

SOLID 원칙이 중요한 이유는 개발자가 유지 관리, 이해 및 확장하기 쉬운 소프트웨어를 만드는 데 도움이 되기 때문입니다. 이러한 원칙을 준수함으로써 개발자는 더욱 견고하고 유연하며 효율적인 코드를 만들 수 있습니다.

**4. 의존성 반전과 의존성 주입의 차이점은 무엇인가요?**

의존성 반전은 구체적인 유형에 대한 의존성을 피하고 추상화를 위해 노력하도록 안내하는 원칙입니다. 의존성 주입은 이 원칙을 구현하는 기법입니다. 내부에서 종속성을 생성하지 않고 외부 소스에서 종속성을 객체에 제공하는 방식입니다.

**5. SOLID 원칙을 다른 프로그래밍 패러다임에도 적용할 수 있나요?**

SOLID 원칙은 객체 지향 프로그래밍을 염두에 두고 설계되었지만, 많은 개념이 다른 프로그래밍 패러다임에도 적용될 수 있습니다. 예를 들어, 클래스가 변경되어야 하는 이유가 하나만 있어야 한다는 단일 책임 원칙은 함수형 프로그래밍의 함수에 적용될 수 있습니다.

**6. 항상 모든 SOLID 원칙을 적용해야 하나요?**

SOLID 원칙은 일반적으로 모범 사례로 간주되지만, 딱딱하고 빠른 규칙은 아닙니다. 단순성이나 성능을 위해 원칙을 위반하는 것이 합당한 상황이 있을 수 있습니다. 중요한 것은 원칙을 이해하고 정보에 입각한 결정을 내리는 것입니다.

## 결론

소프트웨어 개발의 세계에서 SOLID 원칙은 견고하고 유지 관리가 가능하며 확장 가능한 코드를 만드는 데 나침반과 같은 역할을 합니다. 로버트 C. 마틴이 소개한 이 원칙은 관리하기 쉽고 이해하기 쉬운 소프트웨어를 설계하기 위한 프레임워크를 제공합니다.

요약하자면 SOLID 원칙은 다음과 같습니다:

- **단일 책임 원칙(SRP)**: 클래스는 변경해야 할 이유가 하나만 있어야 하며, 이를 통해 유지 관리가 쉽고 가독성이 향상됩니다.
- **개방/폐쇄 원칙(OCP)**: 소프트웨어 엔티티는 확장을 위해서는 개방적이어야 하지만 수정을 위해서는 폐쇄적이어야 안정성이 향상되고 코드 변경이 최소화됩니다.
- **리스코프의 대체 원칙(LSP)**: 파생 클래스나 자식 클래스는 기본 클래스나 부모 클래스로 대체할 수 있어야 유연성이 향상되고 코드 유지 관리가 쉬워집니다.
- **인터페이스 분리 원칙(ISP)**: 클라이언트가 자신과 무관한 인터페이스를 구현하도록 강요해서는 안 되며, 이를 통해 부작용과 변경이 필요한 빈도를 줄여야 합니다.
- **의존성 반전 원칙(DIP)**: 상위 레벨 모듈/클래스는 하위 레벨 모듈/클래스에 의존해서는 안 됩니다. 둘 다 추상화에 의존하여 코드 재사용성을 높이고 결합을 줄여야 합니다.

이러한 원칙은 각각 고유한 이점을 제공하며, 함께 적용하면 코드의 품질을 크게 향상시킬 수 있습니다. 이해하기 쉽고, 변경하고, 확장하기 쉬운 코드를 작성하여 소프트웨어를 더욱 견고하고 적응력 있게 만들도록 장려합니다.

개발자로서 이러한 원칙을 일상적인 코딩 관행에 통합하기 위해 노력하는 것이 중요합니다. 소프트웨어를 생각하고 설계하는 방식에 변화가 필요할 수도 있지만, 코드 품질과 유지보수성 측면에서 얻을 수 있는 이점은 그만한 가치가 있습니다. SOLID 원칙을 준수하면 시간이 지나도 변하지 않는 소프트웨어를 만들 수 있으며, 사용자의 요구와 기술의 발전에 따라 적응하고 성장할 수 있습니다.

## Reference

* https://forreya.medium.com/the-solid-principles-writing-scalable-maintainable-code-13040ada3bca
* https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design
* https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/
* https://en.wikipedia.org/wiki/SOLID
* https://www.baeldung.com/solid-principles
* https://medium.com/backticks-tildes/the-s-o-l-i-d-principles-in-pictures-b34ce2f1e898
* https://realpython.com/solid-principles-python/
* https://www.geeksforgeeks.org/solid-principle-in-programming-understand-with-real-life-examples/