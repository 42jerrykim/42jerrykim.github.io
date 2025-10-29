---
draft: true
title: "10. 객체지향 프로그래밍 고급"
description: "상속, 다형성, 추상화 등 객체지향 프로그래밍의 고급 개념을 마스터합니다"
collection_order: 10
---

# 10. 객체지향 프로그래밍 고급

파이썬의 객체지향 프로그래밍 고급 기능을 통해 더 복잡하고 유연한 시스템을 설계할 수 있습니다.

## 학습 목표

이 챕터를 완료하면 다음을 할 수 있습니다:

- **상속**을 통한 코드 재사용과 확장
- **다형성**을 활용한 유연한 프로그램 설계
- **추상화**를 통한 인터페이스 설계
- **다중 상속**과 MRO 이해
- **프로퍼티**와 **디스크립터** 활용

## 핵심 내용

### 1. 상속 (Inheritance)

**기본 상속**

```python
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        return "Some generic animal sound"
    
    def info(self):
        return f"{self.name} is a {self.species}"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed
    
    def make_sound(self):  # 메서드 오버라이딩
        return "Woof!"
    
    def fetch(self):  # 새로운 메서드 추가
        return f"{self.name} is fetching the ball!"

# 사용 예제
my_dog = Dog("Buddy", "Golden Retriever")
print(my_dog.info())      # 상위 클래스 메서드
print(my_dog.make_sound()) # 오버라이딩된 메서드
print(my_dog.fetch())     # 하위 클래스 고유 메서드
```

**super() 함수 심화**

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old"

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
        self.grades = {}
    
    def introduce(self):
        return super().introduce() + f", Student ID: {self.student_id}"
    
    def add_grade(self, subject, grade):
        self.grades[subject] = grade

class GraduateStudent(Student):
    def __init__(self, name, age, student_id, research_area):
        super().__init__(name, age, student_id)
        self.research_area = research_area
    
    def introduce(self):
        return super().introduce() + f", Research: {self.research_area}"
```

### 2. 다형성 (Polymorphism)

**메서드 오버라이딩을 통한 다형성**

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# 다형성 활용
def print_shape_info(shape):
    print(f"Area: {shape.area():.2f}")
    print(f"Perimeter: {shape.perimeter():.2f}")

shapes = [
    Rectangle(5, 3),
    Circle(4),
    Rectangle(2, 8)
]

for shape in shapes:
    print_shape_info(shape)  # 동일한 인터페이스, 다른 구현
```

### 3. 추상화 (Abstraction)

**추상 기본 클래스**

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.is_running = False
    
    @abstractmethod
    def start_engine(self):
        pass
    
    @abstractmethod
    def stop_engine(self):
        pass
    
    def get_info(self):  # 구체적인 구현
        return f"{self.brand} {self.model}"

class Car(Vehicle):
    def start_engine(self):
        if not self.is_running:
            self.is_running = True
            return f"{self.get_info()} engine started with key"
        return f"{self.get_info()} is already running"
    
    def stop_engine(self):
        if self.is_running:
            self.is_running = False
            return f"{self.get_info()} engine stopped"
        return f"{self.get_info()} is already stopped"

class Motorcycle(Vehicle):
    def start_engine(self):
        if not self.is_running:
            self.is_running = True
            return f"{self.get_info()} engine started with kick"
        return f"{self.get_info()} is already running"
    
    def stop_engine(self):
        if self.is_running:
            self.is_running = False
            return f"{self.get_info()} engine stopped"
        return f"{self.get_info()} is already stopped"
```

### 4. 다중 상속과 MRO

**다중 상속**

```python
class Flyable:
    def fly(self):
        return "Flying through the air"

class Swimmable:
    def swim(self):
        return "Swimming through water"

class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name):
        super().__init__(name, "Duck")
    
    def make_sound(self):
        return "Quack!"

# MRO (Method Resolution Order) 확인
print(Duck.__mro__)
# 또는
print(Duck.mro())

# 사용 예제
duck = Duck("Donald")
print(duck.make_sound())  # Duck의 메서드
print(duck.fly())         # Flyable의 메서드
print(duck.swim())        # Swimmable의 메서드
print(duck.info())        # Animal의 메서드
```

**다이아몬드 문제 해결**

```python
class A:
    def method(self):
        print("A method")

class B(A):
    def method(self):
        print("B method")
        super().method()

class C(A):
    def method(self):
        print("C method")
        super().method()

class D(B, C):
    def method(self):
        print("D method")
        super().method()

# MRO: D -> B -> C -> A
d = D()
d.method()
print(D.__mro__)
```

### 5. 프로퍼티 (Properties)

**@property 데코레이터**

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9
    
    @property
    def kelvin(self):
        return self._celsius + 273.15

# 사용 예제
temp = Temperature(25)
print(f"Celsius: {temp.celsius}")
print(f"Fahrenheit: {temp.fahrenheit}")
print(f"Kelvin: {temp.kelvin}")

temp.fahrenheit = 100
print(f"New Celsius: {temp.celsius}")
```

## 실습 프로젝트

### 프로젝트 1: 도형 계산기

다양한 도형의 넓이와 둘레를 계산하는 시스템을 만들어봅시다.

```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    """도형의 추상 기본 클래스"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def area(self):
        """넓이 계산 (추상 메서드)"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """둘레 계산 (추상 메서드)"""
        pass
    
    def info(self):
        """도형 정보 출력"""
        return (f"{self.name} - "
                f"Area: {self.area():.2f}, "
                f"Perimeter: {self.perimeter():.2f}")

class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius

class Triangle(Shape):
    def __init__(self, side1, side2, side3):
        super().__init__("Triangle")
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
    
    def area(self):
        # 헤론의 공식
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))
    
    def perimeter(self):
        return self.side1 + self.side2 + self.side3

class ShapeCalculator:
    def __init__(self):
        self.shapes = []
    
    def add_shape(self, shape):
        if isinstance(shape, Shape):
            self.shapes.append(shape)
        else:
            raise TypeError("Only Shape objects can be added")
    
    def calculate_total_area(self):
        return sum(shape.area() for shape in self.shapes)
    
    def calculate_total_perimeter(self):
        return sum(shape.perimeter() for shape in self.shapes)
    
    def get_largest_shape(self):
        if not self.shapes:
            return None
        return max(self.shapes, key=lambda s: s.area())
    
    def display_all(self):
        for shape in self.shapes:
            print(shape.info())
        print(f"\nTotal Area: {self.calculate_total_area():.2f}")
        print(f"Total Perimeter: {self.calculate_total_perimeter():.2f}")
        
        largest = self.get_largest_shape()
        if largest:
            print(f"Largest Shape: {largest.name} (Area: {largest.area():.2f})")

# 사용 예제
if __name__ == "__main__":
    calculator = ShapeCalculator()
    
    calculator.add_shape(Rectangle(5, 3))
    calculator.add_shape(Circle(4))
    calculator.add_shape(Triangle(3, 4, 5))
    
    calculator.display_all()
```

### 프로젝트 2: 게임 캐릭터 시스템

RPG 게임의 캐릭터 시스템을 구현해봅시다.

```python
from abc import ABC, abstractmethod
import random

class Character(ABC):
    def __init__(self, name, health, attack_power):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack_power = attack_power
        self.level = 1
        self.experience = 0
    
    @abstractmethod
    def special_attack(self, target):
        pass
    
    def attack(self, target):
        damage = random.randint(self.attack_power - 5, self.attack_power + 5)
        target.take_damage(damage)
        return f"{self.name} attacks {target.name} for {damage} damage!"
    
    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        if self.health == 0:
            return f"{self.name} has been defeated!"
        return f"{self.name} takes {damage} damage. Health: {self.health}/{self.max_health}"
    
    def heal(self, amount):
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        healed = self.health - old_health
        return f"{self.name} heals for {healed} HP. Health: {self.health}/{self.max_health}"
    
    def gain_experience(self, exp):
        self.experience += exp
        if self.experience >= self.level * 100:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.experience = 0
        self.max_health += 20
        self.health = self.max_health
        self.attack_power += 5
        return f"{self.name} levels up to level {self.level}!"
    
    def is_alive(self):
        return self.health > 0
    
    def status(self):
        return (f"{self.name} (Level {self.level}) - "
                f"HP: {self.health}/{self.max_health}, "
                f"Attack: {self.attack_power}, "
                f"EXP: {self.experience}/{self.level * 100}")

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=25)
        self.armor = 10
    
    def special_attack(self, target):
        damage = self.attack_power * 2
        target.take_damage(damage)
        return f"{self.name} uses Mighty Strike on {target.name} for {damage} damage!"
    
    def take_damage(self, damage):
        reduced_damage = max(1, damage - self.armor)
        return super().take_damage(reduced_damage)

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=80, attack_power=30)
        self.mana = 50
        self.max_mana = 50
    
    def special_attack(self, target):
        if self.mana >= 20:
            self.mana -= 20
            damage = self.attack_power * 1.5
            target.take_damage(damage)
            return f"{self.name} casts Fireball on {target.name} for {damage} damage! Mana: {self.mana}/{self.max_mana}"
        else:
            return f"{self.name} doesn't have enough mana for Fireball!"
    
    def restore_mana(self, amount):
        old_mana = self.mana
        self.mana = min(self.max_mana, self.mana + amount)
        restored = self.mana - old_mana
        return f"{self.name} restores {restored} mana. Mana: {self.mana}/{self.max_mana}"

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=20)
        self.arrows = 30
    
    def special_attack(self, target):
        if self.arrows >= 3:
            self.arrows -= 3
            hits = 3
            total_damage = 0
            result = f"{self.name} uses Triple Shot on {target.name}:\n"
            
            for i in range(hits):
                damage = random.randint(self.attack_power - 2, self.attack_power + 2)
                target.take_damage(damage)
                total_damage += damage
                result += f"  Arrow {i+1}: {damage} damage\n"
            
            result += f"Total damage: {total_damage}. Arrows left: {self.arrows}"
            return result
        else:
            return f"{self.name} doesn't have enough arrows for Triple Shot!"

class Game:
    def __init__(self):
        self.characters = []
    
    def add_character(self, character):
        self.characters.append(character)
    
    def battle(self, char1, char2):
        print(f"\n=== Battle: {char1.name} vs {char2.name} ===")
        print(char1.status())
        print(char2.status())
        print()
        
        round_num = 1
        while char1.is_alive() and char2.is_alive():
            print(f"Round {round_num}:")
            
            # 캐릭터 1 공격
            if random.choice([True, False]):  # 50% 확률로 특수 공격
                print(char1.special_attack(char2))
            else:
                print(char1.attack(char2))
            
            if not char2.is_alive():
                break
            
            # 캐릭터 2 공격
            if random.choice([True, False]):  # 50% 확률로 특수 공격
                print(char2.special_attack(char1))
            else:
                print(char2.attack(char1))
            
            print()
            round_num += 1
        
        winner = char1 if char1.is_alive() else char2
        print(f"{winner.name} wins the battle!")
        winner.gain_experience(50)
        print(winner.gain_experience.__doc__ and winner.level_up())

# 사용 예제
if __name__ == "__main__":
    game = Game()
    
    warrior = Warrior("Conan")
    mage = Mage("Gandalf")
    archer = Archer("Legolas")
    
    game.add_character(warrior)
    game.add_character(mage)
    game.add_character(archer)
    
    # 캐릭터 상태 출력
    for char in game.characters:
        print(char.status())
    
    # 전투 시뮬레이션
    game.battle(warrior, mage)
```

## 체크리스트

### 상속과 다형성
- [ ] 클래스 상속 구조 설계
- [ ] 메서드 오버라이딩 구현
- [ ] super() 함수 활용
- [ ] 다형성을 통한 유연한 설계

### 추상화
- [ ] 추상 기본 클래스 설계
- [ ] 인터페이스 정의와 구현
- [ ] 추상 메서드와 구체 메서드 구분
- [ ] 계층적 설계 원칙 적용

### 고급 기능
- [ ] 다중 상속과 MRO 이해
- [ ] 프로퍼티를 통한 캡슐화
- [ ] 디스크립터 패턴 활용
- [ ] 메타클래스 기본 개념

### 실무 적용
- [ ] 객체지향 설계 원칙 적용
- [ ] 코드 재사용성 향상
- [ ] 유지보수성 고려한 설계
- [ ] 테스트 가능한 구조 설계

## 다음 단계

🎉 **축하합니다!** 파이썬 객체지향 프로그래밍 고급 기능을 마스터했습니다.

이제 [11. 표준 라이브러리](../11_standard_library/)로 넘어가서 파이썬의 강력한 내장 모듈들을 활용하는 방법을 학습해봅시다.

---

💡 **팁:**
- 상속은 "is-a" 관계일 때만 사용하세요
- 컴포지션을 상속보다 우선 고려해보세요
- 추상화를 통해 인터페이스와 구현을 분리하세요
- MRO를 이해하면 다중 상속의 복잡성을 해결할 수 있습니다

## 체크리스트
- [ ] 상속 계층 설계 능력
- [ ] 다형성 활용 기법
- [ ] 추상 클래스 구현
- [ ] 프로퍼티 활용
- [ ] 고급 메서드 타입 구분

## 다음 단계
고급 OOP를 마스터했다면, 파이썬 표준 라이브러리의 다양한 모듈을 학습합니다. 