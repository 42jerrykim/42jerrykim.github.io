---
image: "tmp_wordcloud.png"
categories: CollisionDetection
date: "2024-08-19T00:00:00Z"
header: null
tags:
- collision
- detection
- algorithm
- game
- physics
- simulation
- graphics
- programming
- 2D
- 3D
- spatial
- objects
- bounding
- boxes
- circles
- performance
- optimization
- sweep
- prune
- intersection
- Euclidean
- distance
- rigid
- body
- motion
- video
- games
- mechanics
- simulations
- robotics
- computational
- geometry
- hitbox
- hurtbox
- AABB
- OBB
- BSP
- octree
- hierarchy
- bounding
- volumes
- insertion
- sort
- transitive
- property
- inequality
- linear
- interpolation
- root
- finding
- algorithm
- stiction
- resting
- contact
- soft
- body
- collision
- detection
- algorithms
- fast
- efficient
- real-time
teaser: /assets/images/undefined/teaser.jpg

title: '[CollisionDetection] 충돌 감지 알고리즘'
---

충돌 감지(collision detection)는 컴퓨터 그래픽스, 게임, 로봇 공학 등 다양한 분야에서 필수적인 알고리즘이다. 이 알고리즘은 두 개 이상의 공간 객체가 서로 교차하는지를 감지하는 문제로, 특히 게임 개발에서는 캐릭터가 벽을 통과하지 않도록 하거나, 물체 간의 상호작용을 구현하는 데 중요한 역할을 한다. 기본적으로 충돌 감지 알고리즘은 두 객체의 경계 상자를 비교하여 충돌 여부를 판단하는 방식으로 작동한다. 예를 들어, 두 원의 충돌을 감지할 때는 각 원의 중심점 간의 거리를 계산하고, 이 거리가 두 원의 반지름의 합보다 작은지를 확인하는 방식이다. 이러한 간단한 방법 외에도, 더 복잡한 형태의 객체를 다루기 위해 다양한 최적화 기법이 필요하다. 예를 들어, 스윕 앤 프룬(sweep and prune) 알고리즘은 객체의 위치를 정렬하여 불필요한 충돌 검사를 줄이는 방법으로, 성능을 크게 향상시킬 수 있다. 이처럼 충돌 감지 알고리즘은 단순한 수학적 원리를 바탕으로 하여, 실제 게임 환경에서의 물리적 상호작용을 효과적으로 구현하는 데 기여하고 있다.


|![]()|
|:---:|
||


<!--
##### Outline #####
-->

<!--
---
## 서론
**충돌 감지의 중요성**  
**충돌 감지의 기본 개념**  
**게임 및 시뮬레이션에서의 활용**  

## 충돌 감지의 기초
**충돌 감지란 무엇인가?**  
**2D 및 3D 충돌 감지의 차이점**  
**기본적인 충돌 감지 알고리즘**  

## 원형 충돌 감지
**원형 충돌 감지의 원리**  
**원형 충돌 감지 알고리즘 구현**  
**원형 충돌 감지의 장단점**  

## 충돌 감지 알고리즘
**단순한 충돌 감지 알고리즘**  
**스윕 앤 프룬(Sweep and Prune) 알고리즘**  
**계층적 경계 볼륨(Hierarchical Bounding Volume) 알고리즘**  

## 실용적인 예제
**원형 충돌 감지 예제**  
**게임에서의 충돌 감지 구현**  
**시뮬레이션에서의 충돌 감지 활용**  

## 자주 묻는 질문
**충돌 감지의 성능을 향상시키는 방법은?**  
**충돌 감지에서의 정확도와 속도 간의 균형은?**  
**어떤 알고리즘이 가장 효율적인가?**  

## 관련 기술
**물리 엔진과의 관계**  
**게임 개발에서의 충돌 감지**  
**로봇 공학에서의 충돌 감지**  

## 결론
**충돌 감지의 중요성 요약**  
**미래의 충돌 감지 기술 전망**  
**게임 및 시뮬레이션에서의 충돌 감지의 역할**  

---
-->

<!--
---
## 서론
**충돌 감지의 중요성**  
**충돌 감지의 기본 개념**  
**게임 및 시뮬레이션에서의 활용**  
-->

## 서론

**충돌 감지의 중요성**  

충돌 감지는 컴퓨터 그래픽스와 게임 개발에서 매우 중요한 요소이다. 물체가 서로 충돌하는 상황을 정확하게 감지하는 것은 게임의 현실감을 높이고, 사용자 경험을 향상시키는 데 필수적이다. 충돌 감지가 제대로 이루어지지 않으면, 게임의 물리적 상호작용이 비현실적으로 보이거나, 사용자에게 혼란을 줄 수 있다. 따라서 충돌 감지 기술은 게임 개발자와 시뮬레이션 엔지니어에게 필수적인 기술로 자리 잡고 있다.

**충돌 감지의 기본 개념**  

충돌 감지란 두 개 이상의 물체가 서로 접촉하거나 겹치는지를 판단하는 과정을 의미한다. 이 과정은 물리 엔진의 핵심 기능 중 하나로, 물체의 위치, 형태, 속도 등을 고려하여 충돌 여부를 판단한다. 기본적으로 충돌 감지는 두 물체의 경계가 겹치는지를 확인하는 방식으로 이루어진다. 이러한 경계는 다양한 형태로 정의될 수 있으며, 원형, 사각형, 다각형 등 여러 가지 형태가 있다.

**게임 및 시뮬레이션에서의 활용**  

게임과 시뮬레이션에서 충돌 감지는 다양한 방식으로 활용된다. 예를 들어, 액션 게임에서는 캐릭터가 적과 충돌할 때 피해를 입거나, 아이템을 획득하는 등의 상호작용이 발생한다. 또한, 시뮬레이션에서는 물체 간의 물리적 상호작용을 통해 현실적인 결과를 도출할 수 있다. 이러한 이유로 충돌 감지는 게임의 재미와 시뮬레이션의 정확성을 높이는 데 중요한 역할을 한다. 

<!--
## 충돌 감지의 기초
**충돌 감지란 무엇인가?**  
**2D 및 3D 충돌 감지의 차이점**  
**기본적인 충돌 감지 알고리즘**  
-->

## 충돌 감지의 기초

**충돌 감지란 무엇인가?**  
충돌 감지는 두 개 이상의 객체가 서로 겹치는지를 판단하는 기술이다. 이는 게임, 시뮬레이션, 로봇 공학 등 다양한 분야에서 필수적인 요소로 작용한다. 충돌 감지는 객체 간의 상호작용을 결정하고, 이를 통해 현실감 있는 환경을 구현할 수 있도록 돕는다.

**2D 및 3D 충돌 감지의 차이점**  
2D 충돌 감지는 평면에서의 객체 간의 충돌을 다루며, 주로 원형, 사각형 등의 간단한 형태로 이루어진다. 반면, 3D 충돌 감지는 입체 공간에서의 충돌을 다루며, 구, 큐브, 다면체 등 복잡한 형태를 포함한다. 3D 충돌 감지는 계산이 더 복잡하고, 더 많은 데이터를 처리해야 하므로 성능 최적화가 중요하다.

**기본적인 충돌 감지 알고리즘**  
기본적인 충돌 감지 알고리즘으로는 AABB(축 정렬 경계 상자)와 OBB(정의되지 않은 경계 상자) 등이 있다. AABB는 객체의 최소 및 최대 좌표를 사용하여 충돌 여부를 판단하며, OBB는 회전된 객체의 경계를 고려하여 충돌을 감지한다. 이러한 알고리즘들은 간단하면서도 효과적인 충돌 감지를 가능하게 한다.

<!--
## 원형 충돌 감지
**원형 충돌 감지의 원리**  
**원형 충돌 감지 알고리즘 구현**  
**원형 충돌 감지의 장단점**  
-->

## 원형 충돌 감지

**원형 충돌 감지의 원리**  

원형 충돌 감지는 두 개의 원이 서로 겹치는지를 판단하는 알고리즘이다. 이 원들은 각각의 중심 좌표와 반지름을 가지고 있으며, 두 원의 중심 간의 거리와 반지름을 비교하여 충돌 여부를 결정한다. 두 원이 충돌하는 조건은 다음과 같다.

- 두 원의 중심 간의 거리 < 두 원의 반지름의 합

이 조건이 성립하면 두 원은 충돌하고, 그렇지 않으면 충돌하지 않는다. 이 원리는 2D 게임이나 시뮬레이션에서 매우 유용하게 사용된다.

**원형 충돌 감지 알고리즘 구현**  

원형 충돌 감지를 구현하기 위해서는 다음과 같은 간단한 수학 공식을 사용할 수 있다. 아래는 Python으로 작성한 예제 코드이다.

```python
import math

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

def is_colliding(circle1, circle2):
    distance = math.sqrt((circle1.x - circle2.x) ** 2 + (circle1.y - circle2.y) ** 2)
    return distance < (circle1.radius + circle2.radius)

# 예제 사용
circle1 = Circle(0, 0, 5)
circle2 = Circle(3, 4, 5)

if is_colliding(circle1, circle2):
    print("충돌 발생")
else:
    print("충돌 없음")
```

이 코드는 두 개의 원이 충돌하는지를 판단하는 간단한 예제이다. `Circle` 클래스는 원의 중심 좌표와 반지름을 저장하고, `is_colliding` 함수는 두 원의 충돌 여부를 판단한다.

**원형 충돌 감지의 장단점**  

원형 충돌 감지의 장점은 구현이 간단하고 계산이 빠르다는 점이다. 원형 충돌 감지는 수학적으로 간단한 계산으로 이루어져 있어, 많은 객체가 존재하는 환경에서도 효율적으로 사용할 수 있다. 

하지만 단점도 존재한다. 원형 충돌 감지는 원형 형태의 객체에만 적합하며, 복잡한 형태의 객체에 대해서는 정확한 충돌 감지를 제공하지 못한다. 따라서 다양한 형태의 객체가 존재하는 경우, 다른 충돌 감지 알고리즘과 함께 사용해야 할 필요가 있다. 

이와 같은 원형 충돌 감지는 게임 개발 및 시뮬레이션에서 매우 유용하게 활용될 수 있으며, 기본적인 충돌 감지 알고리즘으로 자리 잡고 있다.

<!--
## 충돌 감지 알고리즘
**단순한 충돌 감지 알고리즘**  
**스윕 앤 프룬(Sweep and Prune) 알고리즘**  
**계층적 경계 볼륨(Hierarchical Bounding Volume) 알고리즘**  
-->

## 충돌 감지 알고리즘

**단순한 충돌 감지 알고리즘**  

단순한 충돌 감지 알고리즘은 기본적인 형태의 충돌 감지 방법이다. 이 알고리즘은 주로 두 개체의 경계 상자를 비교하여 충돌 여부를 판단한다. 예를 들어, 두 개체가 사각형 형태일 경우, 각 개체의 좌표를 비교하여 겹치는 부분이 있는지를 확인한다. 이 방법은 구현이 간단하고 빠르지만, 복잡한 형태의 개체에 대해서는 정확도가 떨어질 수 있다. 

```python
def is_colliding(rect1, rect2):
    return (rect1.x < rect2.x + rect2.width and
            rect1.x + rect1.width > rect2.x and
            rect1.y < rect2.y + rect2.height and
            rect1.y + rect1.height > rect2.y)
```

**스윕 앤 프룬(Sweep and Prune) 알고리즘**  

스윕 앤 프룬 알고리즘은 충돌 감지의 효율성을 높이기 위해 사용되는 방법이다. 이 알고리즘은 모든 개체를 특정 축에 따라 정렬한 후, 각 개체의 경계 상자를 비교하여 충돌 가능성이 있는 개체 쌍만을 선별한다. 이 방법은 많은 개체가 존재할 때 성능을 크게 향상시킬 수 있다. 

```python
def sweep_and_prune(objects):
    # 각 객체의 경계 상자를 정렬
    sorted_objects = sorted(objects, key=lambda obj: obj.bounding_box.x)
    potential_collisions = []
    
    for i in range(len(sorted_objects)):
        for j in range(i + 1, len(sorted_objects)):
            if sorted_objects[i].bounding_box.intersects(sorted_objects[j].bounding_box):
                potential_collisions.append((sorted_objects[i], sorted_objects[j]))
    return potential_collisions
```

**계층적 경계 볼륨(Hierarchical Bounding Volume) 알고리즘**  

계층적 경계 볼륨 알고리즘은 복잡한 개체를 여러 개의 경계 볼륨으로 나누어 충돌 감지를 수행하는 방법이다. 이 알고리즘은 개체의 구조를 계층적으로 구성하여, 상위 경계 볼륨이 충돌하지 않으면 하위 볼륨을 검사하지 않아도 되므로 성능을 크게 향상시킬 수 있다. 

```python
class BoundingVolume:
    def __init__(self, children):
        self.children = children

    def intersects(self, other):
        # 상위 경계 볼륨 간의 충돌 검사
        for child in self.children:
            if child.intersects(other):
                return True
        return False
```

이와 같은 알고리즘들은 각각의 장단점이 있으며, 상황에 따라 적절한 방법을 선택하여 사용해야 한다. 충돌 감지의 성능을 높이기 위해서는 이러한 알고리즘들을 조합하여 사용하는 것이 효과적이다.

<!--
## 실용적인 예제
**원형 충돌 감지 예제**  
**게임에서의 충돌 감지 구현**  
**시뮬레이션에서의 충돌 감지 활용**  
-->

## 실용적인 예제

**원형 충돌 감지 예제**  

원형 충돌 감지는 게임 개발 및 시뮬레이션에서 매우 유용하게 사용된다. 예를 들어, 2D 게임에서 플레이어 캐릭터와 적 캐릭터 간의 충돌을 감지할 때 원형 충돌 감지 알고리즘을 사용할 수 있다. 이 알고리즘은 각 객체의 중심과 반지름을 이용하여 두 객체가 충돌하는지를 판단한다. 

아래는 원형 충돌 감지를 구현하는 간단한 코드 예제이다.

```python
class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

def check_collision(circle1, circle2):
    distance_squared = (circle1.x - circle2.x) ** 2 + (circle1.y - circle2.y) ** 2
    radius_sum_squared = (circle1.radius + circle2.radius) ** 2
    return distance_squared <= radius_sum_squared

# 예제 사용
circle1 = Circle(0, 0, 5)
circle2 = Circle(3, 4, 5)

if check_collision(circle1, circle2):
    print("충돌 발생!")
else:
    print("충돌 없음.")
```

이 코드는 두 개의 원형 객체가 충돌하는지를 판단하는 간단한 예제이다. `check_collision` 함수는 두 원의 중심 간의 거리와 반지름의 합을 비교하여 충돌 여부를 결정한다.

**게임에서의 충돌 감지 구현**  

게임에서 충돌 감지는 매우 중요한 요소이다. 플레이어가 적과 충돌하거나 장애물에 부딪힐 때, 게임의 흐름과 재미에 큰 영향을 미친다. 충돌 감지를 구현하기 위해서는 다양한 알고리즘을 사용할 수 있으며, 각 알고리즘의 특성과 장단점을 이해하는 것이 중요하다.

예를 들어, AABB(축 정렬 경계 상자) 알고리즘은 사각형 객체의 충돌을 감지하는 데 유용하다. 이 알고리즘은 각 객체의 최소 및 최대 좌표를 계산하여 두 객체가 겹치는지를 판단한다. 아래는 AABB 충돌 감지를 구현한 코드 예제이다.

```python
class AABB:
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

def check_aabb_collision(aabb1, aabb2):
    return (aabb1.x_min < aabb2.x_max and
            aabb1.x_max > aabb2.x_min and
            aabb1.y_min < aabb2.y_max and
            aabb1.y_max > aabb2.y_min)

# 예제 사용
aabb1 = AABB(0, 0, 5, 5)
aabb2 = AABB(3, 3, 7, 7)

if check_aabb_collision(aabb1, aabb2):
    print("충돌 발생!")
else:
    print("충돌 없음.")
```

이 코드는 두 개의 AABB 객체가 충돌하는지를 판단하는 예제이다. `check_aabb_collision` 함수는 두 AABB의 경계가 겹치는지를 확인하여 충돌 여부를 결정한다.

**시뮬레이션에서의 충돌 감지 활용**  

시뮬레이션에서도 충돌 감지는 중요한 역할을 한다. 예를 들어, 물리 기반 시뮬레이션에서는 객체 간의 상호작용을 정확하게 모델링하기 위해 충돌 감지가 필수적이다. 물체가 서로 충돌할 때, 그에 따른 힘과 반응을 계산해야 하며, 이를 위해서는 정확한 충돌 감지가 필요하다.

아래는 물리 시뮬레이션에서 충돌 감지를 활용하는 간단한 예제이다.

```python
class PhysicsObject:
    def __init__(self, position, velocity, radius):
        self.position = position
        self.velocity = velocity
        self.radius = radius

def update_physics(objects):
    for obj in objects:
        obj.position += obj.velocity

def simulate(objects):
    update_physics(objects)
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if check_collision(objects[i], objects[j]):
                print(f"충돌 발생: 객체 {i}와 객체 {j}")

# 예제 사용
objects = [
    PhysicsObject(0, 1, 5),
    PhysicsObject(10, -1, 5)
]

simulate(objects)
```

이 코드는 물리 객체의 위치를 업데이트하고, 충돌 여부를 확인하는 간단한 시뮬레이션 예제이다. `simulate` 함수는 모든 객체의 물리적 상태를 업데이트한 후, 충돌 여부를 확인하여 충돌이 발생했음을 출력한다. 

이와 같이 실용적인 예제를 통해 충돌 감지의 중요성과 활용 방법을 이해할 수 있다. 충돌 감지는 게임 및 시뮬레이션의 핵심 요소로, 다양한 알고리즘과 기법을 통해 구현할 수 있다.

<!--
## 자주 묻는 질문
**충돌 감지의 성능을 향상시키는 방법은?**  
**충돌 감지에서의 정확도와 속도 간의 균형은?**  
**어떤 알고리즘이 가장 효율적인가?**  
-->

## 자주 묻는 질문

**충돌 감지의 성능을 향상시키는 방법은?**  

충돌 감지의 성능을 향상시키기 위해서는 여러 가지 방법이 있다. 첫째, 공간 분할 기법을 활용하는 것이 효과적이다. 예를 들어, 쿼드트리(Quad Tree)나 옥트리(Octree)와 같은 데이터 구조를 사용하면, 충돌 검사를 수행할 때 필요한 객체의 수를 줄일 수 있다. 둘째, 객체의 움직임을 예측하여 충돌 가능성이 낮은 객체들끼리는 충돌 검사를 생략하는 방법도 있다. 마지막으로, 알고리즘의 최적화를 통해 불필요한 계산을 줄이는 것이 중요하다. 

**충돌 감지에서의 정확도와 속도 간의 균형은?**  

충돌 감지에서 정확도와 속도 간의 균형은 매우 중요한 문제이다. 일반적으로, 높은 정확도를 요구할수록 계산량이 증가하여 속도가 느려질 수 있다. 따라서, 개발자는 게임이나 시뮬레이션의 요구 사항에 따라 적절한 알고리즘을 선택해야 한다. 예를 들어, 실시간 게임에서는 속도가 더 중요할 수 있으므로, 근사 알고리즘을 사용할 수 있다. 반면, 시뮬레이션에서는 정확도가 더 중요할 수 있으므로, 보다 정밀한 알고리즘을 선택할 수 있다. 

**어떤 알고리즘이 가장 효율적인가?**  

가장 효율적인 알고리즘은 사용되는 상황에 따라 다르다. 2D 게임에서는 AABB(축 정렬 경계 상자) 충돌 감지 알고리즘이 간단하고 빠르기 때문에 많이 사용된다. 3D 게임에서는 BVH(경계 볼륨 계층) 알고리즘이 효율적일 수 있다. 또한, 스윕 앤 프룬(Sweep and Prune) 알고리즘은 많은 객체가 있는 경우에 유용하다. 따라서, 각 알고리즘의 장단점을 고려하여 상황에 맞는 알고리즘을 선택하는 것이 중요하다. 

--- 

이와 같은 방식으로 각 섹션을 작성할 수 있다. 각 주제에 대해 더 깊이 있는 설명을 추가하고, 예제 코드나 다이어그램을 포함하여 독자들이 이해하기 쉽게 구성하는 것이 좋다.

<!--
## 관련 기술
**물리 엔진과의 관계**  
**게임 개발에서의 충돌 감지**  
**로봇 공학에서의 충돌 감지**  
-->

## 관련 기술

**물리 엔진과의 관계**  

충돌 감지는 물리 엔진과 밀접한 관계가 있다. 물리 엔진은 객체 간의 상호작용을 시뮬레이션하는 소프트웨어로, 충돌 감지 기능을 포함하고 있다. 물리 엔진은 충돌이 발생했을 때, 객체의 운동을 계산하고 반응을 시뮬레이션하는 역할을 한다. 이러한 기능은 게임 개발에서 매우 중요하며, 현실적인 물리적 상호작용을 구현하는 데 필수적이다. 예를 들어, 게임에서 캐릭터가 벽에 부딪히면, 물리 엔진은 캐릭터의 속도와 방향을 조정하여 자연스러운 반응을 만들어낸다.

**게임 개발에서의 충돌 감지**  

게임 개발에서 충돌 감지는 필수적인 요소이다. 게임의 재미와 몰입감을 높이기 위해서는 객체 간의 상호작용이 자연스럽고 현실적이어야 한다. 충돌 감지 알고리즘은 게임의 성능에 큰 영향을 미치며, 다양한 게임 장르에서 활용된다. 예를 들어, 액션 게임에서는 적과의 충돌을 감지하여 전투 시스템을 구현하고, 레이싱 게임에서는 차량 간의 충돌을 감지하여 경주를 진행한다. 이러한 충돌 감지 시스템은 게임의 전반적인 품질을 결정짓는 중요한 요소이다.

**로봇 공학에서의 충돌 감지**  

로봇 공학에서도 충돌 감지는 매우 중요한 역할을 한다. 로봇이 환경과 상호작용할 때, 충돌 감지 시스템은 로봇이 안전하게 작업을 수행할 수 있도록 돕는다. 예를 들어, 자율주행차는 주변 장애물과의 충돌을 피하기 위해 고급 충돌 감지 알고리즘을 사용한다. 이러한 시스템은 로봇이 주어진 작업을 수행하는 동안 안전성을 보장하고, 효율성을 높이는 데 기여한다. 로봇 공학에서의 충돌 감지는 기술 발전과 함께 더욱 중요해지고 있으며, 다양한 응용 분야에서 활용되고 있다.

<!--
## 결론
**충돌 감지의 중요성 요약**  
**미래의 충돌 감지 기술 전망**  
**게임 및 시뮬레이션에서의 충돌 감지의 역할**  
-->

## 결론

**충돌 감지의 중요성 요약**  

충돌 감지는 게임 및 시뮬레이션에서 매우 중요한 역할을 한다. 이는 객체 간의 상호작용을 관리하고, 현실적인 물리적 반응을 구현하는 데 필수적이다. 충돌 감지를 통해 사용자 경험을 향상시키고, 게임의 몰입감을 높일 수 있다. 또한, 충돌 감지는 로봇 공학 및 자율주행차와 같은 다양한 분야에서도 필수적인 기술로 자리 잡고 있다. 

**미래의 충돌 감지 기술 전망**  

미래의 충돌 감지 기술은 더욱 정교해질 것으로 예상된다. 인공지능과 머신러닝 기술의 발전으로, 충돌 감지 시스템은 더 높은 정확도와 효율성을 갖출 수 있을 것이다. 또한, 가상현실(VR) 및 증강현실(AR) 기술의 발전에 따라, 실시간으로 복잡한 환경에서의 충돌 감지가 더욱 중요해질 것이다. 이러한 기술들은 사용자에게 더욱 몰입감 있는 경험을 제공할 수 있을 것이다.

**게임 및 시뮬레이션에서의 충돌 감지의 역할**  

게임 및 시뮬레이션에서 충돌 감지는 단순한 물리적 상호작용을 넘어서, 스토리텔링과 게임플레이의 핵심 요소로 작용한다. 충돌 감지를 통해 캐릭터의 움직임과 반응을 자연스럽게 만들 수 있으며, 이는 플레이어의 몰입도를 높이는 데 기여한다. 또한, 충돌 감지는 게임의 난이도 조절 및 다양한 게임 메커니즘을 구현하는 데 중요한 역할을 한다. 

결론적으로, 충돌 감지는 게임 및 시뮬레이션의 핵심 기술로, 앞으로도 계속해서 발전하고 중요성이 증가할 것이다.

<!--
##### Reference #####
-->

## Reference


* [https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection](https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection)
* [https://en.wikipedia.org/wiki/Collision_detection](https://en.wikipedia.org/wiki/Collision_detection)
* [https://leanrada.com/notes/sweep-and-prune/](https://leanrada.com/notes/sweep-and-prune/)
* [https://leanrada.com/notes/sweep-and-prune-2/](https://leanrada.com/notes/sweep-and-prune-2/)


<!--
Another simple shape for collision detection is between two circles. This
algorithm works by taking the center points of the two circles and ensuring
the distance between the center points are less than the two radii added
together.

    
    
    <div id="cr-stage"></div>
    <p>
      Move the circle with arrow keys. Green means collision, blue means no
      collision.
    </p>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crafty/0.5.4/crafty-min.js"></script>
    
    
    
    #cr-stage {
      position: static !important;
      height: 200px !important;
    }
    
    
    
    Crafty.init(200, 200);
    
    const dim1 = { x: 5, y: 5 };
    const dim2 = { x: 20, y: 20 };
    
    Crafty.c("Circle", {
      circle(radius, color) {
        this.radius = radius;
        this.w = this.h = radius * 2;
        this.color = color || "#000000";
    
        this.bind("Move", Crafty.DrawManager.drawAll);
        return this;
      },
    
      draw() {
        const ctx = Crafty.canvas.context;
        ctx.save();
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(
          this.x + this.radius,
          this.y + this.radius,
          this.radius,
          0,
          Math.PI * 2,
        );
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      },
    });
    
    const circle1 = Crafty.e("2D, Canvas, Circle").attr(dim1).circle(15, "red");
    
    const circle2 = Crafty.e("2D, Canvas, Circle, Fourway")
      .fourway(2)
      .attr(dim2)
      .circle(20, "blue");
    
    circle2.bind("EnterFrame", function () {
      const dx = circle1.x - circle2.x;
      const dy = circle1.y - circle2.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
    
      const colliding = distance < circle1.radius + circle2.radius;
      this.color = colliding ? "green" : "blue";
    });
    


-->

<!--






-->

<!--
Term in computer science

**Collision detection** is the [ computational problem
](/wiki/Computational_problem "Computational problem") of detecting an [
intersection ](/wiki/Intersection_\(geometry\) "Intersection \(geometry\)") of
two or more [ spatial ](/wiki/Space "Space") objects, commonly computer
graphics objects. It has applications in various computing fields, primarily
in [ computer graphics ](/wiki/Computer_graphics "Computer graphics") , [
computer games ](/wiki/Computer_game "Computer game") , [ computer simulations
](/wiki/Computer_simulation "Computer simulation") , [ robotics
](/wiki/Robotics "Robotics") and [ computational physics
](/wiki/Computational_physics "Computational physics") . Collision detection
is a classic problem of [ computational geometry
](/wiki/Computational_geometry "Computational geometry") . Collision detection
[ algorithms ](/wiki/Algorithm "Algorithm") can be divided into operating on
2D or 3D spatial objects.  [  1  ]

[
![](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Billiards_balls.jpg/200px-
Billiards_balls.jpg) ](/wiki/File:Billiards_balls.jpg) Billiards balls hitting
each other are a classic example applicable within the science of collision
detection.

In physical simulation, experiments such as playing [ billiards
](/wiki/Billiards "Billiards") are conducted.  [  2  ]  The [ physics
](/wiki/Physics "Physics") of bouncing billiard balls are understood under the
umbrella of [ rigid body motion ](/wiki/Rigid_body_motion "Rigid body motion")
and [ elastic collisions ](/wiki/Elastic_collision "Elastic collision") .  [
3  ]  An initial description of the situation would be given, with a very
precise physical description of the billiard table and balls, as well as
initial positions of all the balls.  [  4  ]  Based on a force applied to the
cue ball, the [ computer program ](/wiki/Computer_program "Computer program")
would calculate the trajectories, precise motion and eventual resting places
of all the balls. A program to simulate this game would consist of several
portions, one of which would be responsible for calculating the precise
impacts between the billiard balls. This particular example also turns out to
be [ ill conditioned ](/wiki/Condition_number "Condition number") : as a small
error in any calculation will cause drastic changes in the final position of
the billiard balls.

Video games have similar requirements, with some crucial differences. While
some computer simulations need to simulate real-world physics as precisely as
possible, computer games need to simulate real-world physics in an
_acceptable_ way, in [ real time ](/wiki/Real-time_computing "Real-time
computing") and robustly. Compromises are allowed, so long as the resulting
simulation is satisfying to the game players.

##  Collision detection in computer simulation

[  [ edit  ](/w/index.php?title=Collision_detection&action=edit&section=2
"Edit section: Collision detection in computer simulation") ]

Physical simulators differ in the way they react on a collision. Some use the
softness of the material to calculate a force, which will resolve the
collision in the following time steps like it is in reality. This is very CPU
intensive for low softness materials. Some simulators estimate the time of
collision by [ linear interpolation ](/wiki/Linear_interpolation "Linear
interpolation") , [ roll back ](/wiki/Rollback_\(data_management\) "Rollback
\(data management\)") the simulation, and calculate the collision by the more
abstract methods of [ conservation laws ](/wiki/Conservation_laws
"Conservation laws") .

Some iterate the linear interpolation ( [ Newton's method
](/wiki/Newton%27s_method "Newton's method") ) to calculate the time of
collision with a much higher precision than the rest of the simulation.
Collision detection utilizes time coherence to allow even finer time steps
without much increasing CPU demand, such as in [ air traffic control
](/wiki/Air_traffic_control "Air traffic control") .

After an inelastic collision, special states of sliding and resting can occur
and, for example, the [ Open Dynamics Engine ](/wiki/Open_Dynamics_Engine
"Open Dynamics Engine") uses constraints to simulate them. Constraints avoid
inertia and thus instability. Implementation of rest by means of a [ scene
graph ](/wiki/Scene_graph "Scene graph") avoids drift.

In other words, physical simulators usually function one of two ways: where
the collision is detected _[ a posteriori ](/wiki/Empirical_evidence
"Empirical evidence") _ (after the collision occurs) or _[ a priori
](/wiki/A_priori_and_a_posteriori "A priori and a posteriori") _ (before the
collision occurs). In addition to the _a posteriori_ and _a priori_
distinction, almost all modern collision detection algorithms are broken into
a hierarchy of algorithms. Often the terms "discrete" and "continuous" are
used rather than _a posteriori_ and _a priori_ .

###  _A posteriori_ (discrete) versus _a priori_ (continuous)

[  [ edit  ](/w/index.php?title=Collision_detection&action=edit&section=3
"Edit section: A posteriori \(discrete\) versus a priori \(continuous\)") ]

In the _a posteriori_ case, the physical simulation is advanced by a small
step, then checked to see if any objects are intersecting or visibly
considered intersecting. At each simulation step, a list of all intersecting
bodies is created, and the positions and trajectories of these objects are
"fixed" to account for the collision. This method is called _a posteriori_
because it typically misses the actual instant of collision, and only catches
the collision after it has actually happened.

In the _a priori_ methods, there is a collision detection algorithm which will
be able to predict very precisely the trajectories of the physical bodies. The
instants of collision are calculated with high precision, and the physical
bodies never actually interpenetrate. This is called _a priori_ because the
collision detection algorithm calculates the instants of collision before it
updates the configuration of the physical bodies.

The main benefits of the _a posteriori_ methods are as follows. In this case,
the collision detection algorithm need not be aware of the myriad of physical
variables; a simple list of physical bodies is fed to the algorithm, and the
program returns a list of intersecting bodies. The collision detection
algorithm doesn't need to understand friction, elastic collisions, or worse,
nonelastic collisions and deformable bodies. In addition, the _a posteriori_
algorithms are in effect one dimension simpler than the _a priori_ algorithms.
An _a priori_ algorithm must deal with the time variable, which is absent from
the _a posteriori_ problem.

On the other hand, _a posteriori_ algorithms cause problems in the "fixing"
step, where intersections (which aren't physically correct) need to be
corrected. Moreover, if the discrete step is too large, the collision could go
undetected, resulting in an object which passes through another if it is
sufficiently fast or small.

The benefits of the _a priori_ algorithms are increased fidelity and
stability. It is difficult (but not completely impossible) to separate the
physical simulation from the collision detection algorithm. However, in all
but the simplest cases, the problem of determining ahead of time when two
bodies will collide (given some initial data) has no closed form solution—a
numerical [ root finder ](/wiki/Root-finding_algorithm "Root-finding
algorithm") is usually involved.

Some objects are in _resting contact_ , that is, in collision, but neither
bouncing off, nor interpenetrating, such as a vase resting on a table. In all
cases, resting contact requires special treatment: If two objects collide ( _a
posteriori_ ) or slide ( _a priori_ ) and their relative motion is below a
threshold, friction becomes [ stiction ](/wiki/Stiction "Stiction") and both
objects are arranged in the same branch of the [ scene graph
](/wiki/Scene_graph "Scene graph") .

The obvious approaches to collision detection for multiple objects are very
slow. [ Checking every object against every other object
](/wiki/Triangular_number "Triangular number") will, of course, work, but is
too inefficient to be used when the number of objects is at all large.
Checking objects with complex geometry against each other in the obvious way,
by checking each face against each other face, is itself quite slow. Thus,
considerable research has been applied to speed up the problem.

###  Exploiting temporal coherence

[  [ edit  ](/w/index.php?title=Collision_detection&action=edit&section=5
"Edit section: Exploiting temporal coherence") ]

In many applications, the configuration of physical bodies from one time step
to the next changes very little. Many of the objects may not move at all.
Algorithms have been designed so that the calculations done in a preceding
time step can be reused in the current time step, resulting in faster
completion of the calculation.

At the coarse level of collision detection, the objective is to find pairs of
objects which might potentially intersect. Those pairs will require further
analysis. An early high performance algorithm for this was developed by [ Ming
C. Lin ](/wiki/Ming_C._Lin "Ming C. Lin") at the [ University of California,
Berkeley ](/wiki/University_of_California,_Berkeley "University of California,
Berkeley") [ [1] ](http://www.cs.berkeley.edu/~jfc/mirtich/collDet.html) , who
suggested using [ axis-aligned bounding boxes ](/wiki/Axis-
aligned_bounding_box "Axis-aligned bounding box") for all _n_ bodies in the
scene.

Each box is represented by the product of three intervals (i.e., a box would
be  I  1  ×  I  2  ×  I  3  =  [  a  1  ,  b  1  ]  ×  [  a  2  ,  b  2  ]  ×
[  a  3  ,  b  3  ]  {\displaystyle I_{1}\times I_{2}\times
I_{3}=[a_{1},b_{1}]\times [a_{2},b_{2}]\times [a_{3},b_{3}]}
![{\\displaystyle I_{1}\\times I_{2}\\times I_{3}=\[a_{1},b_{1}\]\\times
\[a_{2},b_{2}\]\\times
\[a_{3},b_{3}\]}](https://wikimedia.org/api/rest_v1/media/math/render/svg/450c59ef778cb75d1ea83e0aed119f8d988cab8c)
). A common algorithm for collision detection of bounding boxes is [ sweep and
prune ](/wiki/Sweep_and_prune "Sweep and prune") . Observe that two such
boxes,  I  1  ×  I  2  ×  I  3  {\displaystyle I_{1}\times I_{2}\times I_{3}}
![{\\displaystyle I_{1}\\times I_{2}\\times
I_{3}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0df2268640d53db4400dd6961c34eede7fcb505f)
and  J  1  ×  J  2  ×  J  3  {\displaystyle J_{1}\times J_{2}\times J_{3}}
![{\\displaystyle J_{1}\\times J_{2}\\times
J_{3}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/43bddcffb9603a20584862f1c263f7ca48b81161)
intersect [ if, and only if ](/wiki/If_and_only_if "If and only if") ,  I  1
{\displaystyle I_{1}}  ![{\\displaystyle
I_{1}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/03f18d041b2df30adef07164dbf285878893dedc)
intersects  J  1  {\displaystyle J_{1}}  ![{\\displaystyle
J_{1}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/260ffe7da7c858cf114ad89a6c794944ea4e760f)
,  I  2  {\displaystyle I_{2}}  ![{\\displaystyle
I_{2}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/5e3506ae39df854f347365bae6f326ef4f565be5)
intersects  J  2  {\displaystyle J_{2}}  ![{\\displaystyle
J_{2}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0f9986a8fbfd51097a5ff5e82d3252c9572b5835)
and  I  3  {\displaystyle I_{3}}  ![{\\displaystyle
I_{3}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/becba5d3350c4dd244f3cda48eb13439f21ed350)
intersects  J  3  {\displaystyle J_{3}}  ![{\\displaystyle
J_{3}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/461776bf90e008ad7e31e0b5dca1c3ddc1273378)
. It is supposed that, from one time step to the next, if  I  k
{\displaystyle I_{k}}  ![{\\displaystyle
I_{k}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/d658e7f6b34dd1d3025a7c9a72efba5b9f46475d)
and  J  k  {\displaystyle J_{k}}  ![{\\displaystyle
J_{k}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/a99023826aca8b6316815468d3dcf4a512f383eb)
intersect, then it is very likely that at the next time step they will still
intersect. Likewise, if they did not intersect in the previous time step, then
they are very likely to continue not to.

So we reduce the problem to that of tracking, from frame to frame, which
intervals do intersect. We have three lists of intervals (one for each axis)
and all lists are the same length (since each list has length  n
{\displaystyle n}  ![{\\displaystyle
n}](https://wikimedia.org/api/rest_v1/media/math/render/svg/a601995d55609f2d9f5e233e36fbe9ea26011b3b)
, the number of bounding boxes.) In each list, each interval is allowed to
intersect all other intervals in the list. So for each list, we will have an
n  ×  n  {\displaystyle n\times n}  ![{\\displaystyle n\\times
n}](https://wikimedia.org/api/rest_v1/media/math/render/svg/59d2b4cb72e304526cf5b5887147729ea259da78)
[ matrix ](/wiki/Matrix_\(math\) "Matrix \(math\)") M  =  (  m  i  j  )
{\displaystyle M=(m_{ij})}  ![{\\displaystyle
M=\(m_{ij}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/e79c1e2a873c7bc24cf17ee6f07d435093f5995c)
of zeroes and ones:  m  i  j  {\displaystyle m_{ij}}  ![{\\displaystyle
m_{ij}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/cd6f1bb2d6548dca472922bcbcb77e7ad3a5b4df)
is 1 if intervals  i  {\displaystyle i}  ![{\\displaystyle
i}](https://wikimedia.org/api/rest_v1/media/math/render/svg/add78d8608ad86e54951b8c8bd6c8d8416533d20)
and  j  {\displaystyle j}  ![{\\displaystyle
j}](https://wikimedia.org/api/rest_v1/media/math/render/svg/2f461e54f5c093e92a55547b9764291390f0b5d0)
intersect, and 0 if they do not intersect.

By our assumption, the matrix  M  {\displaystyle M}  ![{\\displaystyle
M}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f82cade9898ced02fdd08712e5f0c0151758a0dd)
associated to a list of intervals will remain essentially unchanged from one
time step to the next. To exploit this, the list of intervals is actually
maintained as a list of labeled endpoints. Each element of the list has the
coordinate of an endpoint of an interval, as well as a unique integer
identifying that interval. Then, we [ sort ](/wiki/Sorting_algorithm "Sorting
algorithm") the list by coordinates, and update the matrix  M  {\displaystyle
M}  ![{\\displaystyle
M}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f82cade9898ced02fdd08712e5f0c0151758a0dd)
as we go. It's not so hard to believe that this algorithm will work relatively
quickly if indeed the configuration of bounding boxes does not change
significantly from one time step to the next.

In the case of deformable bodies such as cloth simulation, it may not be
possible to use a more specific pairwise pruning algorithm as discussed below,
and an _n_ -body pruning algorithm is the best that can be done.

If an upper bound can be placed on the velocity of the physical bodies in a
scene, then pairs of objects can be pruned based on their initial distance and
the size of the time step.

Once we've selected a pair of physical bodies for further investigation, we
need to check for collisions more carefully. However, in many applications,
individual objects (if they are not too deformable) are described by a set of
smaller primitives, mainly triangles. So now, we have two sets of triangles,
S  =  S  1  ,  S  2  ,  …  ,  S  n  {\displaystyle S={S_{1},S_{2},\dots
,S_{n}}}  ![{\\displaystyle S={S_{1},S_{2},\\dots
,S_{n}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/82ab8405af4ab712c8b4d4e47a658ed87bc00832)
and  T  =  T  1  ,  T  2  ,  …  ,  T  n  {\displaystyle T={T_{1},T_{2},\dots
,T_{n}}}  ![{\\displaystyle T={T_{1},T_{2},\\dots
,T_{n}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/b479580c6c1db84e33c21af1cda4536b0a719ee7)
(for simplicity, we will assume that each set has the same number of
triangles.)

The obvious thing to do is to check all triangles  S  j  {\displaystyle S_{j}}
![{\\displaystyle
S_{j}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/222db49df2eefdb67737ba2d2dbd221a1bae0bf0)
against all triangles  T  k  {\displaystyle T_{k}}  ![{\\displaystyle
T_{k}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/51cc852c6e446a4871f78e05492699a9525b9acb)
for collisions, but this involves  n  2  {\displaystyle n^{2}}
![{\\displaystyle
n^{2}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/ac9810bbdafe4a6a8061338db0f74e25b7952620)
comparisons, which is highly inefficient. If possible, it is desirable to use
a pruning algorithm to reduce the number of pairs of triangles we need to
check.

The most widely used family of algorithms is known as the _hierarchical
bounding volumes_ method. As a preprocessing step, for each object (in our
example,  S  {\displaystyle S}  ![{\\displaystyle
S}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4611d85173cd3b508e67077d4a1252c9c05abca2)
and  T  {\displaystyle T}  ![{\\displaystyle
T}](https://wikimedia.org/api/rest_v1/media/math/render/svg/ec7200acd984a1d3a3d7dc455e262fbe54f7f6e0)
) we will calculate a [ hierarchy of bounding volumes
](/wiki/Bounding_volume_hierarchy "Bounding volume hierarchy") . Then, at each
time step, when we need to check for collisions between  S  {\displaystyle S}
![{\\displaystyle
S}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4611d85173cd3b508e67077d4a1252c9c05abca2)
and  T  {\displaystyle T}  ![{\\displaystyle
T}](https://wikimedia.org/api/rest_v1/media/math/render/svg/ec7200acd984a1d3a3d7dc455e262fbe54f7f6e0)
, the hierarchical bounding volumes are used to reduce the number of pairs of
triangles under consideration. For simplicity, we will give an example using
bounding spheres, although it has been noted that spheres are undesirable in
many cases.  [ _[ citation needed  ](/wiki/Wikipedia:Citation_needed
"Wikipedia:Citation needed") _ ]

If  E  {\displaystyle E}  ![{\\displaystyle
E}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4232c9de2ee3eec0a9c0a19b15ab92daa6223f9b)
is a set of triangles, we can pre-calculate a bounding sphere  B  (  E  )
{\displaystyle B(E)}  ![{\\displaystyle
B\(E\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7efcbf46eeaf242b4a57e27413d69d8de0b20370)
. There are many ways of choosing  B  (  E  )  {\displaystyle B(E)}
![{\\displaystyle
B\(E\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7efcbf46eeaf242b4a57e27413d69d8de0b20370)
, we only assume that  B  (  E  )  {\displaystyle B(E)}  ![{\\displaystyle
B\(E\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7efcbf46eeaf242b4a57e27413d69d8de0b20370)
is a sphere that completely contains  E  {\displaystyle E}  ![{\\displaystyle
E}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4232c9de2ee3eec0a9c0a19b15ab92daa6223f9b)
and is as small as possible.

Ahead of time, we can compute  B  (  S  )  {\displaystyle B(S)}
![{\\displaystyle
B\(S\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/93fe493dc8f9d402ebc492def1832a60a21e9451)
and  B  (  T  )  {\displaystyle B(T)}  ![{\\displaystyle
B\(T\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/58329c775b28dba986ce47422a4eeca8ef9613b3)
. Clearly, if these two spheres do not intersect (and that is very easy to
test), then neither do  S  {\displaystyle S}  ![{\\displaystyle
S}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4611d85173cd3b508e67077d4a1252c9c05abca2)
and  T  {\displaystyle T}  ![{\\displaystyle
T}](https://wikimedia.org/api/rest_v1/media/math/render/svg/ec7200acd984a1d3a3d7dc455e262fbe54f7f6e0)
. This is not much better than an _n_ -body pruning algorithm, however.

If  E  =  E  1  ,  E  2  ,  …  ,  E  m  {\displaystyle E={E_{1},E_{2},\dots
,E_{m}}}  ![{\\displaystyle E={E_{1},E_{2},\\dots
,E_{m}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/597c325e99f71c1aea40febe815eb214051f2114)
is a set of triangles, then we can split it into two halves  L  (  E  )  :=  E
1  ,  E  2  ,  …  ,  E  m  /  2  {\displaystyle L(E):={E_{1},E_{2},\dots
,E_{m/2}}}  ![{\\displaystyle L\(E\):={E_{1},E_{2},\\dots
,E_{m/2}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/e852003bdd81ec5e8f5f7bbfef0270d4553c5e43)
and  R  (  E  )  :=  E  m  /  2  \+  1  ,  …  ,  E  m  −  1  ,  E  m
{\displaystyle R(E):={E_{m/2+1},\dots ,E_{m-1},E_{m}}}  ![{\\displaystyle
R\(E\):={E_{m/2+1},\\dots
,E_{m-1},E_{m}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/7dc13274542c37a95cacfc6db242cbfe64c61ad7)
. We can do this to  S  {\displaystyle S}  ![{\\displaystyle
S}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4611d85173cd3b508e67077d4a1252c9c05abca2)
and  T  {\displaystyle T}  ![{\\displaystyle
T}](https://wikimedia.org/api/rest_v1/media/math/render/svg/ec7200acd984a1d3a3d7dc455e262fbe54f7f6e0)
, and we can calculate (ahead of time) the bounding spheres  B  (  L  (  S  )
)  ,  B  (  R  (  S  )  )  {\displaystyle B(L(S)),B(R(S))}  ![{\\displaystyle
B\(L\(S\)\),B\(R\(S\)\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/a9c85ca2c8903a9e4e3123cd82d28d8a4aada8a7)
and  B  (  L  (  T  )  )  ,  B  (  R  (  T  )  )  {\displaystyle
B(L(T)),B(R(T))}  ![{\\displaystyle
B\(L\(T\)\),B\(R\(T\)\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/6e8e5f35a14ee07f0e575bbca7ab8f204ca2c841)
. The hope here is that these bounding spheres are much smaller than  B  (  S
)  {\displaystyle B(S)}  ![{\\displaystyle
B\(S\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/93fe493dc8f9d402ebc492def1832a60a21e9451)
and  B  (  T  )  {\displaystyle B(T)}  ![{\\displaystyle
B\(T\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/58329c775b28dba986ce47422a4eeca8ef9613b3)
. And, if, for instance,  B  (  S  )  {\displaystyle B(S)}  ![{\\displaystyle
B\(S\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/93fe493dc8f9d402ebc492def1832a60a21e9451)
and  B  (  L  (  T  )  )  {\displaystyle B(L(T))}  ![{\\displaystyle
B\(L\(T\)\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/0557b28f96fd600a89c1d9081bdf7f81488f2bb1)
do not intersect, then there is no sense in checking any triangle in  S
{\displaystyle S}  ![{\\displaystyle
S}](https://wikimedia.org/api/rest_v1/media/math/render/svg/4611d85173cd3b508e67077d4a1252c9c05abca2)
against any triangle in  L  (  T  )  {\displaystyle L(T)}  ![{\\displaystyle
L\(T\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/48ba63c960059a240ba065883c25abf1dad569c0)
.

As a [ precomputation ](/wiki/Precomputation "Precomputation") , we can take
each physical body (represented by a set of triangles) and recursively
decompose it into a [ binary tree ](/wiki/Binary_tree "Binary tree") , where
each node  N  {\displaystyle N}  ![{\\displaystyle
N}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f5e3890c981ae85503089652feb48b191b57aae3)
represents a set of triangles, and its two children represent  L  (  N  )
{\displaystyle L(N)}  ![{\\displaystyle
L\(N\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/5e2b06859874cbba17603928fd3097092ebd2895)
and  R  (  N  )  {\displaystyle R(N)}  ![{\\displaystyle
R\(N\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/d694574fe2f6db83f7da2f5d5325f26f61f7cf21)
. At each node in the tree, we can pre-compute the bounding sphere  B  (  N  )
{\displaystyle B(N)}  ![{\\displaystyle
B\(N\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f885668a7b8825f61b83f4a8d556c87b9702714e)
.

When the time comes for testing a pair of objects for collision, their
bounding sphere tree can be used to eliminate many pairs of triangles.

Many variants of the algorithms are obtained by choosing something other than
a sphere for  B  (  T  )  {\displaystyle B(T)}  ![{\\displaystyle
B\(T\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/58329c775b28dba986ce47422a4eeca8ef9613b3)
. If one chooses [ axis-aligned bounding boxes ](/wiki/Axis-
aligned_bounding_box "Axis-aligned bounding box") , one gets AABBTrees. [
Oriented bounding box ](/wiki/Oriented_bounding_box "Oriented bounding box")
trees are called OBBTrees. Some trees are easier to update if the underlying
object changes. Some trees can accommodate higher order primitives such as [
splines ](/wiki/Spline_\(mathematics\) "Spline \(mathematics\)") instead of
simple triangles.

###  Exact pairwise collision detection

[  [ edit  ](/w/index.php?title=Collision_detection&action=edit&section=7
"Edit section: Exact pairwise collision detection") ]

Once we're done pruning, we are left with a number of candidate pairs to check
for exact collision detection.

A basic observation is that for any two [ convex ](/wiki/Convex_set "Convex
set") objects which are disjoint, one can find a plane in space so that one
object lies completely on one side of that plane, and the other object lies on
the opposite side of that plane. This allows the development of very fast
collision detection algorithms for convex objects.

Early work in this area involved " [ separating plane
](/wiki/Separating_axis_theorem "Separating axis theorem") " methods. Two
triangles collide essentially only when they can not be separated by a plane
going through three vertices. That is, if the triangles are  v  1  ,  v  2  ,
v  3  {\displaystyle {v_{1},v_{2},v_{3}}}  ![{\\displaystyle
{v_{1},v_{2},v_{3}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/28c2f7082133be23b4cbf8473e9bef0a1c6d30e1)
and  v  4  ,  v  5  ,  v  6  {\displaystyle {v_{4},v_{5},v_{6}}}
![{\\displaystyle
{v_{4},v_{5},v_{6}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/789d7ab623897259ecc614e1c3fc27098ba8df80)
where each  v  j  {\displaystyle v_{j}}  ![{\\displaystyle
v_{j}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/73fffa4919c0d6268f6a8d9f38c04dd3296fd0a5)
is a vector in  R  3  {\displaystyle \mathbb {R} ^{3}}  ![{\\displaystyle
\\mathbb {R}
^{3}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f936ddf584f8f3dd2a0ed08917001b7a404c10b5)
, then we can take three vertices,  v  i  ,  v  j  ,  v  k  {\displaystyle
v_{i},v_{j},v_{k}}  ![{\\displaystyle
v_{i},v_{j},v_{k}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/6ea6b672e7160a9a9a5cf839cfaf662ae8583b68)
, find a plane going through all three vertices, and check to see if this is a
separating plane. If any such plane is a separating plane, then the triangles
are deemed to be disjoint. On the other hand, if none of these planes are
separating planes, then the triangles are deemed to intersect. There are
twenty such planes.

If the triangles are coplanar, this test is not entirely successful. One can
add some extra planes, for instance, planes that are [ normal
](/wiki/Normal_\(geometry\) "Normal \(geometry\)") to triangle edges, to fix
the problem entirely. In other cases, objects that meet at a flat face must
necessarily also meet at an angle elsewhere, hence the overall collision
detection will be able to find the collision.

Better methods have since been developed. Very fast algorithms are available
for finding the closest points on the surface of two convex polyhedral
objects. Early work by [ Ming C. Lin ](/wiki/Ming_C._Lin "Ming C. Lin") [  5
]  used a variation on the [ simplex algorithm ](/wiki/Simplex_algorithm
"Simplex algorithm") from [ linear programming ](/wiki/Linear_programming
"Linear programming") . The [ Gilbert-Johnson-Keerthi distance algorithm
](/wiki/Gilbert-Johnson-Keerthi_distance_algorithm "Gilbert-Johnson-Keerthi
distance algorithm") has superseded that approach. These algorithms approach
constant time when applied repeatedly to pairs of stationary or slow-moving
objects, when used with starting points from the previous collision check.

The end result of all this algorithmic work is that collision detection can be
done efficiently for thousands of moving objects in real time on typical
personal computers and game consoles.

Where most of the objects involved are fixed, as is typical of video games, a
priori methods using precomputation can be used to speed up execution.

Pruning is also desirable here, both _n_ -body pruning and pairwise pruning,
but the algorithms must take time and the types of motions used in the
underlying physical system into consideration.

When it comes to the exact pairwise collision detection, this is highly
trajectory dependent, and one almost has to use a numerical [ root-finding
algorithm ](/wiki/Root-finding_algorithm "Root-finding algorithm") to compute
the instant of impact.

As an example, consider two triangles moving in time  v  1  (  t  )  ,  v  2
(  t  )  ,  v  3  (  t  )  {\displaystyle {v_{1}(t),v_{2}(t),v_{3}(t)}}
![{\\displaystyle
{v_{1}\(t\),v_{2}\(t\),v_{3}\(t\)}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/57cf3bc20cd19af2cbaf28273b6d6c4ee539a5ae)
and  v  4  (  t  )  ,  v  5  (  t  )  ,  v  6  (  t  )  {\displaystyle
{v_{4}(t),v_{5}(t),v_{6}(t)}}  ![{\\displaystyle
{v_{4}\(t\),v_{5}\(t\),v_{6}\(t\)}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/46b9e9b93dad83ae2e340de805e1d30df097407b)
. At any point in time, the two triangles can be checked for intersection
using the twenty planes previously mentioned. However, we can do better, since
these twenty planes can all be tracked in time. If  P  (  u  ,  v  ,  w  )
{\displaystyle P(u,v,w)}  ![{\\displaystyle
P\(u,v,w\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/04d09d6d0ab81fe806f172ee0eaec4af9c58402f)
is the plane going through points  u  ,  v  ,  w  {\displaystyle u,v,w}
![{\\displaystyle
u,v,w}](https://wikimedia.org/api/rest_v1/media/math/render/svg/d4cabca98f60f9ee828adb0d73276eb90eb2ee56)
in  R  3  {\displaystyle \mathbb {R} ^{3}}  ![{\\displaystyle \\mathbb {R}
^{3}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f936ddf584f8f3dd2a0ed08917001b7a404c10b5)
then there are twenty planes  P  (  v  i  (  t  )  ,  v  j  (  t  )  ,  v  k
(  t  )  )  {\displaystyle P(v_{i}(t),v_{j}(t),v_{k}(t))}  ![{\\displaystyle
P\(v_{i}\(t\),v_{j}\(t\),v_{k}\(t\)\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/dc6557c773b8bc30821d876fadf5b2a06a047ddf)
to track. Each plane needs to be tracked against three vertices, this gives
sixty values to track. Using a root finder on these sixty functions produces
the exact collision times for the two given triangles and the two given
trajectory. We note here that if the trajectories of the vertices are assumed
to be linear polynomials in  t  {\displaystyle t}  ![{\\displaystyle
t}](https://wikimedia.org/api/rest_v1/media/math/render/svg/65658b7b223af9e1acc877d848888ecdb4466560)
then the final sixty functions are in fact cubic polynomials, and in this
exceptional case, it is possible to locate the exact collision time using the
formula for the roots of the cubic. Some numerical analysts suggest that using
the formula for the roots of the cubic is not as numerically stable as using a
root finder for polynomials.  [ _[ citation needed
](/wiki/Wikipedia:Citation_needed "Wikipedia:Citation needed") _ ]

###  Spatial partitioning

[  [ edit  ](/w/index.php?title=Collision_detection&action=edit&section=9
"Edit section: Spatial partitioning") ]

Alternative algorithms are grouped under the [ spatial partitioning
](/wiki/Spatial_partitioning "Spatial partitioning") umbrella, which includes
[ octrees ](/wiki/Octree "Octree") , [ binary space partitioning
](/wiki/Binary_space_partitioning "Binary space partitioning") (or BSP trees)
and other, similar approaches. If one splits space into a number of simple
cells, and if two objects can be shown not to be in the same cell, then they
need not be checked for intersection. Since BSP trees can be precomputed, that
approach is well suited to handling walls and fixed obstacles in games. These
algorithms are generally older than the algorithms described above.

[ Bounding boxes ](/wiki/Bounding_box "Bounding box") (or [ bounding volumes
](/wiki/Bounding_volume "Bounding volume") ) are most often a 2D rectangle or
3D [ cuboid ](/wiki/Cuboid "Cuboid") , but other shapes are possible. A
bounding box in a video game is sometimes called a  Hitbox  . The bounding
diamond, the minimum bounding parallelogram, the convex hull, the bounding
circle or bounding ball, and the bounding ellipse have all been tried, but
bounding boxes remain the most popular due to their simplicity.  [  6  ]
Bounding boxes are typically used in the early (pruning) stage of collision
detection, so that only objects with overlapping bounding boxes need be
compared in detail.

###  Triangle centroid segments

[  [ edit  ](/w/index.php?title=Collision_detection&action=edit&section=11
"Edit section: Triangle centroid segments") ]

A [ triangle mesh ](/wiki/Triangle_mesh "Triangle mesh") object is commonly
used in 3D body modeling. Normally the collision function is a triangle to
triangle intercept or a bounding shape associated with the mesh. A triangle
centroid is a center of mass location such that it would balance on a pencil
tip. The simulation need only add a centroid dimension to the physics
parameters. Given centroid points in both object and target it is possible to
define the line segment connecting these two points.

The position vector of the centroid of a triangle is the average of the
position vectors of its vertices. So if its vertices have Cartesian
coordinates  (  x  1  ,  y  1  ,  z  1  )  {\displaystyle (x_{1},y_{1},z_{1})}
![{\\displaystyle
\(x_{1},y_{1},z_{1}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/781d7569148878d5fab8e65498162edcc5430791)
,  (  x  2  ,  y  2  ,  z  2  )  {\displaystyle (x_{2},y_{2},z_{2})}
![{\\displaystyle
\(x_{2},y_{2},z_{2}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/b6c761bb04bd0bf983b9b8e83310e5407b7426ad)
and  (  x  3  ,  y  3  ,  z  3  )  {\displaystyle (x_{3},y_{3},z_{3})}
![{\\displaystyle
\(x_{3},y_{3},z_{3}\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/94ba1a3c9bf8723b8006201b672500819c041d87)
then the centroid is  (  (  x  1  \+  x  2  \+  x  3  )  3  ,  (  y  1  \+  y
2  \+  y  3  )  3  ,  (  z  1  \+  z  2  \+  z  3  )  3  )  {\displaystyle
\left({\frac {(x_{1}+x_{2}+x_{3})}{3}},{\frac {(y_{1}+y_{2}+y_{3})}{3}},{\frac
{(z_{1}+z_{2}+z_{3})}{3}}\right)}  ![{\\displaystyle \\left\({\\frac
{\(x_{1}+x_{2}+x_{3}\)}{3}},{\\frac {\(y_{1}+y_{2}+y_{3}\)}{3}},{\\frac
{\(z_{1}+z_{2}+z_{3}\)}{3}}\\right\)}](https://wikimedia.org/api/rest_v1/media/math/render/svg/f128a8003a85f8125a796cd8a152771412fc81ae)
.

Here is the function for a line segment distance between two 3D points.  d  i
s  t  a  n  c  e  =  (  z  2  −  z  1  )  2  \+  (  x  2  −  x  1  )  2  \+  (
y  2  −  y  1  )  2  {\displaystyle \mathrm {distance} ={\sqrt
{(z_{2}-z_{1})^{2}+(x_{2}-x_{1})^{2}+(y_{2}-y_{1})^{2}}}}  ![{\\displaystyle
\\mathrm {distance} ={\\sqrt
{\(z_{2}-z_{1}\)^{2}+\(x_{2}-x_{1}\)^{2}+\(y_{2}-y_{1}\)^{2}}}}](https://wikimedia.org/api/rest_v1/media/math/render/svg/db58ca90620dc84957b53a6d8a4351cbf678e955)

Here the length/distance of the segment is an adjustable "hit" criteria size
of segment. As the objects approach the length decreases to the threshold
value. A triangle sphere becomes the effective geometry test. A sphere
centered at the centroid can be sized to encompass all the triangle's
vertices.

Video games have to split their very limited computing time between several
tasks. Despite this resource limit, and the use of relatively primitive
collision detection algorithms, programmers have been able to create
believable, if inexact, systems for use in games.  [ _[ citation needed
](/wiki/Wikipedia:Citation_needed "Wikipedia:Citation needed") _ ]

For a long time, video games had a very limited number of objects to treat,
and so checking all pairs was not a problem. In two-dimensional games, in some
cases, the hardware was able to efficiently detect and report overlapping
pixels between [ sprites ](/wiki/Sprite_\(computer_graphics\) "Sprite
\(computer graphics\)") on the screen.  [  7  ]  In other cases, simply tiling
the screen and binding each _sprite_ into the tiles it overlaps provides
sufficient pruning, and for pairwise checks, bounding rectangles or circles
called [ hitboxes ](/wiki/Hitbox "Hitbox") are used and deemed sufficiently
accurate.

Three-dimensional games have used spatial partitioning methods for  n
{\displaystyle n}  ![{\\displaystyle
n}](https://wikimedia.org/api/rest_v1/media/math/render/svg/a601995d55609f2d9f5e233e36fbe9ea26011b3b)
-body pruning, and for a long time used one or a few spheres per actual 3D
object for pairwise checks. Exact checks are very rare, except in games
attempting to [ simulate ](/wiki/Simulation_game "Simulation game") reality
closely. Even then, exact checks are not necessarily used in all cases.

Because games do not need to mimic actual physics, stability is not as much of
an issue. Almost all games use _a posteriori_ collision detection, and
collisions are often resolved using very simple rules. For instance, if a
character becomes embedded in a wall, they might be simply moved back to their
last known good location. Some games will calculate the distance the character
can move before getting embedded into a wall, and only allow them to move that
far.

In many cases for video games, approximating the characters by a point is
sufficient for the purpose of collision detection with the environment. In
this case, [ binary space partitioning ](/wiki/Binary_space_partitioning
"Binary space partitioning") trees provide a viable, efficient and simple
algorithm for checking if a point is embedded in the scenery or not. Such a
data structure can also be used to handle "resting position" situation
gracefully when a character is running along the ground. Collisions between
characters, and collisions with projectiles and hazards, are treated
separately.

A robust simulator is one that will react to any input in a reasonable way.
For instance, if we imagine a high speed [ racecar video game
](/wiki/Racing_game "Racing game") , from one simulation step to the next, it
is conceivable that the cars would advance a substantial distance along the
race track. If there is a shallow obstacle on the track (such as a brick
wall), it is not entirely unlikely that the car will completely leap over it,
and this is very undesirable. In other instances, the "fixing" that posteriori
algorithms require isn't implemented correctly, resulting in [ bugs
](/wiki/Software_bug "Software bug") that can trap characters in walls or
allow them to pass through them and fall into an endless void where there may
or may not be a deadly [ bottomless pit
](/wiki/Bottomless_pit_\(video_gaming\) "Bottomless pit \(video gaming\)") ,
sometimes referred to as "black hell", "blue hell", or "green hell", depending
on the predominant color. These are the hallmarks of a failing collision
detection and physical simulation system. _[ Big Rigs: Over the Road Racing
](/wiki/Big_Rigs:_Over_the_Road_Racing "Big Rigs: Over the Road Racing") _ is
an infamous example of a game with a failing or possibly missing collision
detection system.

A **hitbox** is an invisible shape commonly used in [ video games
](/wiki/Video_game "Video game") for real-time collision detection; it is a
type of bounding box. It is often a rectangle (in 2D games) or [ cuboid
](/wiki/Cuboid "Cuboid") (in 3D) that is attached to and follows a point on a
visible object (such as a model or a sprite). Circular or spheroidial shapes
are also common, though they are still most often called "boxes". It is common
for animated objects to have hitboxes attached to each moving part to ensure
accuracy during motion.  [  8  ]  [ _[ unreliable source?
](/wiki/Wikipedia:Reliable_sources "Wikipedia:Reliable sources") _ ]

Hitboxes are used to detect "one-way" collisions such as a character being hit
by a punch or a bullet. They are unsuitable for the detection of collisions
with feedback (e.g. bumping into a wall) due to the difficulty experienced by
both humans and [ AI ](/wiki/Artificial_intelligence_\(video_games\)
"Artificial intelligence \(video games\)") in managing a hitbox's ever-
changing locations; these sorts of collisions are typically handled with much
simpler [ axis-aligned bounding boxes ](/wiki/Axis-aligned_bounding_box "Axis-
aligned bounding box") instead. Players may use the term "hitbox" to refer to
these types of interactions regardless.

A **hurtbox** is a hitbox used to detect incoming sources of damage. In this
context, the term _hitbox_ is typically reserved for those which deal damage.
For example, an attack may only land if the hitbox around an attacker's punch
connects with one of the opponent's hurtboxes on their body, while opposing
hitboxes colliding may result in the players trading or cancelling blows, and
opposing hurtboxes do not interact with each other. The term is not
standardized across the industry; some games reverse their definitions of
_hitbox_ and _hurtbox_ , while others only use "hitbox" for both sides.

  1. ** ^  ** Teschner, M.; Kimmerle, S.; Heidelberger, B.; Zachmann, G.; Raghupathi, L.; Fuhrmann, A.; Cani, M.-P.; Faure, F.; Magnenat-Thalmann, N.; Strasser, W.; Volino, P. (2005). [ "Collision Detection for Deformable Objects" ](https://hal.inria.fr/inria-00394479/document) . _Computer Graphics Forum_ . **24** : 61–81. [ CiteSeerX ](/wiki/CiteSeerX_\(identifier\) "CiteSeerX \(identifier\)") [ 10.1.1.58.2505 ](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.58.2505) . [ doi ](/wiki/Doi_\(identifier\) "Doi \(identifier\)") : [ 10.1111/j.1467-8659.2005.00829.x ](https://doi.org/10.1111%2Fj.1467-8659.2005.00829.x) . [ S2CID ](/wiki/S2CID_\(identifier\) "S2CID \(identifier\)") [ 1359430 ](https://api.semanticscholar.org/CorpusID:1359430) . 
  2. ** ^  ** [ "myPhysicsLab Billiards" ](https://www.myphysicslab.com/engine2D/billiards-en.html) . _www.myphysicslab.com_ . Retrieved  2024-07-08  . 
  3. ** ^  ** Pool Table Simulation (calpoly.edu) https://users.csc.calpoly.edu/~zwood/teaching/csc471/finalW19/jpietrok/index.html 
  4. ** ^  ** https://www.cs.rpi.edu/~cutler/classes/advancedgraphics/S09/final_projects/anderson.pdf 
  5. ** ^  ** Lin, Ming C (1993). [ "Efficient Collision Detection for Animation and Robotics (thesis)" ](https://web.archive.org/web/20140728124049/https://wwwx.cs.unc.edu/~geom/papers/documents/dissertations/lin93.pdf) (PDF)  . University of California, Berkeley. Archived from [ the original ](https://wwwx.cs.unc.edu/~geom/papers/documents/dissertations/lin93.pdf) (PDF)  on 2014-07-28. 
  6. ** ^  ** Caldwell, Douglas R. (2005-08-29). [ "Unlocking the Mysteries of the Bounding Box" ](https://web.archive.org/web/20120728180104/http://www.stonybrook.edu/libmap/coordinates/seriesa/no2/a2.htm) . US Army Engineer Research & Development Center, Topographic Engineering Center, Research Division, Information Generation and Management Branch. Archived from [ the original ](http://www.stonybrook.edu/libmap/coordinates/seriesa/no2/a2.htm) on 2012-07-28  . Retrieved  2014-05-13  . 
  7. ** ^  ** [ "Components of the Amiga: The MC68000 and the Amiga Custom Chips" ](http://amigadev.elowar.com/read/ADCD_2.1/Hardware_Manual_guide/node0004.html#line95) (Reference manual) (2.1 ed.). Chapter 1. [ Archived ](https://web.archive.org/web/20180717093216/http://amigadev.elowar.com/read/ADCD_2.1/Hardware_Manual_guide/node0004.html#line95) from the original on 2018-07-17  . Retrieved  2018-07-17  . " Additionally, you can use system hardware to detect collisions between objects and have your program react to such collisions. "
  8. ** ^  ** [ "Hitbox" ](http://developer.valvesoftware.com/wiki/Hitbox) . _Valve Developer Community_ . [ Valve ](/wiki/Valve_Corporation "Valve Corporation") . Retrieved  18 September  2011  . 


-->

<!--






-->

<!--
5 Aug 2023  ¬∑ 13 min read

tags:  algo  games

Sweep-and-prune is my go-to algorithm when I want to quickly implement
collision detection for a game. I think it‚Äôs an awesome and elegant
algorithm, so I wrote a post about it.

This post is lengthy with many examples and explanations, thus split into two
parts. You can jump to specific bits using this special springboard:

As for the rest of the post, I try to paint a picture of what I think are
first principles and show it with **interactive demos** ! Let‚Äôs go!

* * *

##  Collision detection

As you may know, the problem of collision detection is pretty common in video
game programming. It‚Äôs a prerequisite to the implementation of certain game
mechanics or simulations.

![video of mario with goombas bumping into each
other](https://leanrada.com/notes/sweep-and-prune/mario.gif) Goombas colliding

Some of these mechanics include: preventing characters from passing through
each other, [ goombas ](https://youtu.be/Ky69PjyHCqg) turning around when
bumping into another, big cells eating smaller cells in [ agar.io
](https://agar.io/) , or just about any game physics. All of these need some
kind of collision detection.

![video of agar.io with cells eating smaller
cells](https://leanrada.com/notes/sweep-and-prune/agario.gif) Cells consuming
smaller cells on contact

Here I‚Äôll cover several related approaches, starting with the simplest and
building up to the [ **sweep-and-prune**
](https://en.wikipedia.org/wiki/Sweep_and_prune) algorithm. I won‚Äôt cover
other approaches, such as space partitioning or spatial tree subdivision.

Balls.

I‚Äôll use this **rigid-body ball simulation** as a recurring example to
demonstrate the algorithms throughout the post:

Alright, let‚Äôs dive in! How do we detect these collisions?

##  Naive approach üê•

The straightforward solution is to test every potential pair of objects for
collision. That is, _check every ball against every other ball_ .

    
    
    for (let i = 0; i < balls.length; i++) {
      const ball1 = balls[i];
      
      for (let j = i + 1; j < balls.length; j++) {
        const ball2 = balls[j];
        
        if (intersects(ball1, ball2)) {
          bounce(ball1, ball2);
        }
      }
    }

Note in the above code that the inner loop starts at ` i + 1 ` to prevent
duplicate pairs from being counted (A-B vs B-A). Other than that, it‚Äôs a
pretty simple solution.

These checks are done on every time step, ensuring that balls will bounce
exactly when they collide.

Here‚Äôs a slowed-down, highlighted simulation, showing pairs being tested for
intersection per time step:

Pairs are highlighted  when being tested via ` intersects() ` .

And it works. But if we had more than just a handful of balls we would start
seeing performance issues.

##  Performance, or lack thereof

This naive algorithm runs in _**O(n 2  ) ** _ time in [ Big O terms
](https://en.wikipedia.org/wiki/Big_O_notation) . That is, for an input of _n_
balls, the algorithm‚Äôs running time grows proportionally to the _square_ of
the input _n_ . That‚Äôs a lot! üìà

This is because for _n_ balls, there are around _(n * (n-1))/2_ pairs to test,
or _0.5n 2  \- 0.5n _ . For example, if n = 5 there would be a total of 10
pairs. For n = 10, there would be 45 pairs. For n = 15, 105 pairs (!). And so
on‚Ä¶ Using Big O notation, we can simplify this information into a compact
expression _‚ÄúO(n 2  )‚Äù _

To (painfully) demonstrate how the performance scales badly for bigger inputs,
here‚Äôs a simulation with n = 20:

20 balls = 190 pairs to test

That‚Äôs a lot of tests per frame! Clearly, the naive solution does not scale
well for large numbers of objects.

How can we improve this solution?

The worst case running time for _any_ collision detection algorithm is always
_O(n 2  ) _ . That‚Äôs when all objects intersect simultaneously and you have
no choice but to process each of the n  2  collisions.

Thus, it‚Äôs more practical to compare the average and best cases.

Having said that, the naive algorithm is still _Œò(n 2  ) _ for _any_ case, no
matter the number of actual collisions. A lot of room for improvement!

##  Prologue: Improving the solution

Usually when optimising algorithms, you wanna find **redundant or unnecessary
work** . Then find a way to consolidate that redundancy. (That sounded
corporate-ish.)

A good place to start would be the ` intersects() ` function since it is
called for every candidate pair. If we take the [ typical object intersection
test
](https://gdbooks.gitbooks.io/3dcollisions/content/Chapter2/static_aabb_aabb.html)
to be its implementation, we get a bunch of these **inequality checks** :

    
    
    function intersects(object1, object2) {
      
      return object1.left < object2.right
          && object1.right > object2.left
          && object1.top < object2.bottom
          && object1.bottom > object2.top;
    }

In the above code, the ` intersects() ` function checks if two objects
intersect by comparing their opposing bounds for each direction. (Refer to [
this MDN article ](https://developer.mozilla.org/en-
US/docs/Games/Techniques/3D_collision_detection#aabb_vs._aabb) for a better
explanation.)

We can break the test down to its constituent checks:

  1. ` object1.left < object2.right `
  2. ` object1.right > object2.left `
  3. ` object1.top < object2.bottom `
  4. ` object1.bottom > object2.top `

Each check is solely concerned with one particular axis in a specific
direction.

Here‚Äôs the key thing: Due to the ` && ` operator‚Äôs [ short-circuit
evaluation ](https://en.wikipedia.org/wiki/Short-circuit_evaluation) , if any
one of these checks turns out to be false, then the overall test will
immediately evaluate to false.

Our goal then is to generalise the case where at least _one_ of these checks
is false across many tests as possible.

It‚Äôs the same idea as the [ separating axis theorem
](https://personal.math.vt.edu/mrlugo/sat.html) , which implies that two
objects can‚Äôt be colliding if there‚Äôs at least one axis where their
shadows don‚Äôt overlap.

Let‚Äôs say we focus only on the second check - ` object1.right > object2.left
` . Don‚Äôt worry about the rest of the checks. As hinted above, optimising in
just one axis can still make a big difference later, so we‚Äôll focus on this
single check for now.

Let‚Äôs look at it in the context of multiple objects. Consider three objects
- A, B, and C - in this horizontal configuration:

There are three potential pairs to be checked here: A-B, B-C, and A-C.
Remember, we‚Äôre trying to find redundant work. Pretend we‚Äôre running all
the pairs through the check, like so:

    
    
    A.right > B.left 
    B.right > C.left 
    A.right > C.left 

See any redundant work? Maybe abstractify it a little‚Ä¶

    
    
    A > B 
    B > C 
    A > C 

Voil√†. Due to the [ **transitive property of inequality**
](https://www.mathwords.com/t/transitive_property_inequalities.htm) , realise
that we don‚Äôt need to run the **third test** ! _If we know that` A > B ` and
` B > C ` are both ` false ` , then we would know that ` A > C ` is ` false `
as well. _

> ‚ÄúIf _a ‚â§ b_ and _b ‚â§ c_ , then _a ‚â§ c_ .‚Äù  the transitive property
> of inequality

So in this example, we don‚Äôt really need to run ` intersects(A, C) ` .

    
    
    intersects(A, B) 
    
    
    intersects(B, C) 
    
    
    
    

We‚Äôve skipped one ` intersects() ` call for free! ‚ú®

I‚Äôm handwaving the fact that ` P.left ‚â§ P.right ` is implied for any
object P. Nevertheless, working those details out would just mean more
transitivity.

You might be wondering how this contrived example could apply to general
n-body collision detection. A smart reader such as you might also have
realised that this skip only works if A, B, and C are in a **particular
order** .

What particular order? Try  dragging  the balls below to see when the
optimisation applies and when it does not:

    
    
    intersects(A, B) 
    intersects(B, C) 
    intersects(A, C) 

**Tip:** Drag the balls so that they‚Äôre horizontally spaced out in this
order: A‚ÄëB‚ÄëC

While it‚Äôs true that this skip only works when A, B, and C are ordered,
remember that these labels are _arbitrary_ ! What if we simply decided to
always call the leftmost ball A, the middle ball B, and the rightmost C? Then
the optimisation would always be applicable! üååüß†

But wait‚Ä¶ labeling objects according to some logical ordering is essentially
‚ú® **sorting** ‚ú®! What if we sorted the list of objects every time? Would
the number of skipped tests be worth the cost of sorting?

##  Chapter 1. Sorting

Sorting, inequalities, and optimisation go hand in hand in hand. _A sorted
list allows us to exploit the transitive property of inequality en masse._

![a\[0\] ‚â§ a\[1\] ‚â§ a\[2\] ‚â§ ... ‚â§
a\[n-1\]](https://leanrada.com/notes/sweep-and-prune/sorted.png) The
inequality relationships of elements in a sorted list.

Even if we had to sort the list of objects every frame, the quickest general
sorting algorithm runs in _O(n log n)_ time which is certainly lower than _O(n
2  ) _ .

As shown by the tri-object example above, to achieve the power to skip tests
we need to sort the list of objects by x position.

However, objects aren‚Äôt zero-width points. They‚Äôre _widthy_ , by which I
mean having a size thus occupying an interval in the x-axis, also known as
‚Äúwidth‚Äù. How can one unambiguously sort by x position if objects span
intervals in the x-axis?

##  Sort by min x

A solution to sorting widthy objects is to sort them by their **minimum x**
(their left edge‚Äôs x-coordinate). This technique can be applied to improve
the naive approach.

It involves minimal modifications to the O(n  2  ) solution. But it will
result in a good chunk of tests skipped. I‚Äôll explain later.

First, the modified code:

    
    
    + 
    + sortByLeft(balls);
    + 
      
      for (let i = 0; i < balls.length; i++) {
        const ball1 = balls[i];
        
        for (let j = i + 1; j < balls.length; j++) {
          const ball2 = balls[j];
    + 
    +     
    +     if (ball2.left > ball1.right) break;
    + 
          
          if (intersects(ball1, ball2)) {
            bounce(ball1, ball2);
          }
        }
      }

It‚Äôs mostly the same as the naive solution, differing only in two extra
lines of code.

The first line ` sortByLeft(balls) ` simply sorts the list, with ranking based
on the balls‚Äô left edge x-coords.

    
    
    function sortByLeft(balls) {
      balls.sort((a,b) => a.left - b.left);
    }

And in the inner loop, there is now this break:

    
    
    if (ball2.left > ball1.right) break;

Let‚Äôs break that down.

First, we know that the list is sorted, so the following statement holds true
for any positive integer ` c ` :

` balls[  j  +  c  ].left  >=  balls[  j  ].left `

The break condition, which is derived from the first operand of the
intersection test, if true indicates early that the current pair being tested
for intersection would fail:

` balls2.left  > ball1.right `  
or ` balls[  j  ].left  > ball1.right `

But there are more implications. If it was true, then by combining the above
two inequations‚Ä¶

` balls[  j  +  c  ].left  >=  balls[  j  ].left  > ball1.right `

And by transitive property, the following statement would also be true!

` balls[  j  +  c  ].left  > ball1.right `

Which means the intersection tests of balls at ` balls[  j  +  c  ] ` would
also fail. We know this without needing to test those balls individually. A
range of balls have been eliminated from testing!

In conclusion, when the current _ball2_ ` balls[  j  ] ` stops overlapping
with the current _ball1_ , then any further _ball2_ s in the iteration `
balls[  j  +  c  ] ` would be guaranteed to not overlap _ball1_ as well. In
other words, we stop the inner loop when it gets too far away.

Finally, here‚Äôs a demo:

Pairs highlighted  when tested by ` intersects() ` .

Pretty cool, right! It‚Äôs much faster now.

Some observations:

  * Since the list is sorted, the tests are performed from left to right. 
  * More importantly, it visibly does fewer tests than the naive approach. üìâ This is due the above optimisation which effectively limits pairs to those that overlap in the x-axis! 

Let‚Äôs analyse the time complexity. üëì

The sort - if we take the "fastest" sorting algorithm, like mergesort or
quicksort - would add an _O(n log n)_ term.

The two-level loop, now with an early break, would average out to _O(n + m)_
where _m_ is the total number of x-overlaps. This could degenerate into n  2
but as mentioned above, it‚Äôs more useful to look at the average and best
cases. At best, the loop would be _O(n)_ , wasting no excess processing when
there are no overlaps. On average it‚Äôs _O(n + m)_ .

The average case refers to a world where objects are mostly evenly distributed
and only a couple intersections per object is happening. I think this is a
reasonable assumption for a relatively simple video game like a platformer or
side-scroller.

Here‚Äôs the code with running time annotations:

    
    
    sortByLeft(balls);
    
    
    for (let i = 0; i < balls.length; i++) {
      const ball1 = balls[i];
      
      for (let j = i + 1; j < balls.length; j++) {
        const ball2 = balls[j];
        if (ball2.left > ball1.right) break;
        if (intersects(ball1, ball2)) {
          bounce(ball1, ball2);
        }
      }
    }

Adding those together we get _**O(n log n + m)** _ .

This is a super good improvement over the naive approach‚Äôs _O(n 2  ) _ ,
because **[1]** _n log n_ is [ much smaller ](https://bigocheatsheet.com/)
than _n 2  _ and **[2]** it is partially output-based - depending on the
number of overlaps, it does not process more than necessary.

[ ![](https://www.bigocheatsheet.com/img/big-o-complexity-chart.png)
bigocheatsheet.com  ](https://www.bigocheatsheet.com)

Furthermore, the choice of sorting algorithm could be improved. We‚Äôll look
into that in the next part (somehow better than _n log n_ !).

If you got this far trying to find a decent collision detection algorithm,
then you can stop reading and take the above design! It‚Äôs the perfect
balance between programming effort and running time performance. If you are
curious how this develops or just want to see more interactive demos, read on
to the next part.

##  Visual comparison

Here‚Äôs a side-by-side comparison of the strategies we‚Äôve covered so far!
Observe the amount of intersection tests required per frame. üîç n = 10

(Not shown: the cost of sorting. Let‚Äôs just say the intersection test is
sufficiently expensive.)

Aaand that concludes the first part. Those two lines of code definitely were
the MVPs.

How will it compare to the more advanced versions?

[ Continued in part 2. ](/notes/sweep-and-prune-2/)


-->

<!--






-->

<!--
6 Aug 2023  ¬∑ 13 min read

tags:  algo  games

In the [ first part ](/notes/sweep-and-prune/) , we figured that sorting lets
us exploit the transitive property of inequality to optimise the number of
pairwise tests.

We ended up with - let‚Äôs call it a **‚Äúsimplified version‚Äù** , of the
full sweep-and-prune algorithm.

This part explores the more sophisticated versions of sweep-and-prune.

![Classy rageface](https://leanrada.com/notes/sweep-and-
prune-2/sophisticated.png) Sophisticated sip and prune.

##  Proper sweep-and-prune üßê

Let‚Äôs see how the original version tackled the problem (Not sure which
one‚Äôs original, tbh).

First, sorting widthy objects.

To account for the width of objects while keeping the benefits of unambiguous
sort order, we track the left and the right edges of each object as two
separate points.

This is done by maintaining a separate **array of edge points** corresponding
to the objects‚Äô left & right edges.

See how it works by playing with this  draggable  demo. The left and right
edges of each ball are visualised. These edge points are stored in a sorted
array shown below the box.

Of course, we need to initialise the edge data and continually keep them in
sync with the objects. I‚Äôll leave that out as an implementation detail.

    
    
    let edges: Array<{
      object: Object;  
      x: number;       
      isLeft: boolean; 
    }>;

This sorted array of edges is all we need to facilitate the reduction of
unnecessary pairwise tests.

###  Index as position, position as index

Remember the ` intersects() ` function? Let‚Äôs focus only on the x-axis
checks:

    
    
    function intersects(object1, object2) {
      return object1.left < object2.right
          && object1.right > object2.left
          ;
    }

We can replace these x-coordinate comparisons with a new approach based on
array indices. Since we have a sorted array of every object‚Äôs left and right
points, finding x-overlaps can be done via index-based searches rather than
global pairwise testing.

Take one ball for example. Get the indices of its left and right points, and
you can simply run in between those two points in the array to find all
x-overlapping objects! This is a very fast linear operation.

Here‚Äôs a viz. Try  dragging  the  highlighted ball  below and observe the
edges enclosed visually and in the sorted array:

The above is a simple 1-to-n overlap detection (which is flawed, btw). For
n-to-n overlap detection, turns out there is a neat way to find all
overlapping pairs in a single pass!

##  Chapter 2. Sweeping

To generalise the above to an n-interval overlap scan, imagine a vertical line
sweeping across the whole space from left to right. The sweep line keeps track
of the objects it is currently touching.

Let‚Äôs see what that looks like without collision:

Objects touching the line are lit up in  pink  .

As for the implementation, the line is merely a metaphor. It‚Äôs just a
visualisation of an iteration through the sorted list of edges.

To keep track of objects touching the line, we maintain a set called  `
touching ` in code.

Whenever the line runs into an object (a left edge), the object is added to
the set. Likewise, whenever it exits an object (right edge), the object is
removed from the set.

    
    
    sort(edges);
    
    const touching = new Set();
    for (const edge of edges) {
      if (edge.isLeft) {
        
        touching.add(edge.object);
      } else {
        
        touching.delete(edge.object);
      }
    }

Once we have the sweep working, detecting overlaps is easy‚Ä¶

üëâ Whenever the sweep line enters a new object (a left edge), in addition to
inserting it to ` touching ` , we can mark it as overlapping with the rest of
the objects in ` touching ` .

Watch closely whenever the line enters a ball while the line is ` touching `
other balls. Detected overlaps are highlighted:

X-overlapping pairs are highlighted  as the line sweeps.

Here‚Äôs the updated code for detecting and reporting overlaps:

    
    
      sort(edges);
      
      const touching = new Set();
      for (const edge of edges) {
        if (edge.isLeft) {
          
    +     
    +     
    +     for (const other of touching) {
    +       onOverlapX(other, edge.object);
    +     }
    +     
          touching.add(edge.object);
        } else {
          
          touching.delete(edge.object);
        }
      }

##  Chapter 3. Pruning

` onOverlapX() ` is called whenever two balls are overlapping in the x
dimension. What about the other dimension, _y_ ? What if we‚Äôre working with
3D, how about _z_ ?

Don‚Äôt worry; the sweep is just a broad-phase test, a way to _prune_
candidate pairs in bulk. There will be a narrow-phase test to determine
exactly the intersections in each of the remaining pairs.

` onOverlapX() ` can be hooked up to an exact intersection test like the full
` intersects() ` function earlier. Or, since we already know that the argument
pair overlaps in _x_ , we can just check for _y_ .

    
    
    onOverlapX = function(object1, object2) {
      
      if (object1.top < object2.bottom
       && object1.bottom > object2.top) {
        collide(object1, object2);
      }
    }

While the above formula works for most games, a more precise and time-
consuming check could be done at this level since most candidates have already
been pruned. Our ball example would work better with the following circle
intersection test using the [ Euclidean distance formula
](https://en.wikipedia.org/wiki/Euclidean_distance) :

    
    
    onOverlapX = function(object1, object2) {
      
      const distance = sqrt(
          (object1.x - object2.x) ** 2
        + (object1.y - object2.y) ** 2
      );
      if (distance < object1.radius + object2.radius) {
        bounce(object1, object2);
      }
    }

Finally, the demo:

Ball sim using sweep-and-prune. ` onOverlapX() ` calls highlighted  .

Notice that it behaves very similarly to the simplified version. It limits
tests to x-overlapping pairs.

The sweep-and-prune algorithm is also known as sort-and-sweep.

###  Note for higher dimensions

There is a variant which performs the **sweep for each axis** , not just _x_ .
For example in 3D, it maintains three _separate_ sorted lists of edges for x,
y, and z. Indeed, this is how the full sweep-and-prune implementation works as
described in the [ original paper by D. Baraff
](https://ecommons.cornell.edu/handle/1813/7115) . Object pairs are flagged
for overlaps separately per dimension. Pairs flagged in all dimensions would
be considered intersecting.

This is the advantage the full sweep-and-prune has over the simplified
‚Äúsorted pairwise‚Äù version. It can prune in multiple dimensions!

2D sweep-and-prune. Only pairs with overlapping

[ AABBs
](https://en.wikipedia.org/wiki/Bounding_volume#:~:text=axis%2Daligned%20bounding%20box)

are tested

.

##  Performance of sweep-and-prune

Here‚Äôs a side-by-side comparison of the strategies we‚Äôve covered so far!
Observe the amount of intersection checks required per frame. üîç

Let‚Äôs analyse the time complexity of 1D sweep-and-prune. üëì

The sort step, again, is _O(n log n)_ .

The sweep, which is a linear pass with an inner loop for overlaps, should be
_O(n + m)_ in the average case. Again, _m_ is the number of overlaps.

    
    
    function sweepAndPrune(edges) {
      
      sort(edges);
    
      const touching = new Set();
    
      
      for (const edge of edges) {
        if (edge.isLeft) {
          
          for (const other of touching) {
            onOverlapX(other, edge.object);
          }
          touching.add(edge.object); 
        } else {
          touching.delete(edge.object);
        }
      }
    }

So this sweep-and-prune is _**O(n log n + m)** _ .

That‚Äôs great, but it‚Äôs the same as simplified sweep-and-prune but with
more code and more state to keep tabs on. _Can we improve it further?_

##  Small detail, big improvement

Again, let‚Äôs ask the question: Where is redundant work being done here?

Let‚Äôs look at the sort step, which is the bottleneck of the algorithm
according to the analysis.

The following is a visualisation of the sorting of the edges array, using an
optimised [ quicksort ](https://en.wikipedia.org/wiki/Quicksort) (n log n):

Sort  comparisons  and  swaps  are highlighted. The fixed lines at the top are
edge array positions, connected to actual ball edge x positions below. Line
crossings signal incorrect order.

You can see that most of the time, the sort does nothing at all! The list is
almost always **already sorted from the previous frame** .

Even when it becomes unsorted, it usually just takes a couple of swaps to be
sorted again. There won‚Äôt be more than a few object boundaries changing
places in one time step.

Fortunately, the subject of sorting algorithms is well-researched. We‚Äôre
dealing with the special quality of being _nearly-sorted_ . And one great
choice for sorting nearly-sorted lists is [ **insertion sort**
](https://en.wikipedia.org/wiki/Insertion_sort) !

    
    
    function insertionSort(edges) {
      for (let i = 1; i < edges.length; i++) {
        for (let j = i - 1; j >= 0; j--) {
          if (edges[j].x < edges[j + 1].x) break;
          [edges[j], edges[j + 1]] = [edges[j + 1], edges[j]];
        }
      }
    }

Insertion sort has a running time of _O(n)_ at best when the list is already
sorted or nearly-sorted, and _O(n 2  ) _ at worst when the list is in reverse.
We can argue that the average case is _**O(n)** _ , since the list is almost
always sorted due to the previous frame‚Äôs sort.

Here‚Äôs insertion sort in action:

Sort  comparisons  and  swaps  are highlighted.

Look at it go!

By switching to insertion sort, we‚Äôve reduced the overall average running
time of sweep-and-prune to _**O(n + m)** _ ! Awesome!

**Caveat:** It‚Äôs important to consider the primary axis of sweep-and-prune
due to the sweeps plus the nature of insertion sort. It should be the axis
where objects are most widely distributed to minimize swaps and overlaps.

Of course, don‚Äôt forget about our simplified sweep-and-prune from the first
part. Since it has a sort step as well, we can make it insertion sort too. So
it can also be _O(n + m)_ ! Can we ever top that?

##  Sweeps and swaps

Well, there is yet another way to optimise this algorithm! Hold on to your
balloons, it‚Äôs about to get quite dense. ü™®

Look at the insertion sort example above. You can observe that  swaps  happen
when and only **when an edge point passes through another edge point** .

The event where an edge point passes another can be classified into four
cases:

Case  |  Description   
---|---  
` )‚Üî( ` |  R edge from the west swaps with L edge from the east.   
` (‚Üî) ` |  L edge from the west swaps with R edge from the east.   
` (‚Üî( ` |  L edges swap.   
` )‚Üî) ` |  R edges swap.   
  
Each swap scenario can mean something significant. Let‚Äôs look more closely
into each case.

###  case )‚Üî(. ‚ÄúEntering‚Äù

Video: Animation of a R edge swapping with a L edge | Source: /notes/sweep-and-prune-2/swap-rl.mp4 

When a right edge from the west swaps with a left edge from the east, we can
infer that the corresponding balls are **initiating an overlap** .

###  case (‚Üî). ‚ÄúExiting‚Äù

Video: Animation of a L edge swapping with a R edge | Source: /notes/sweep-and-prune-2/swap-lr.mp4 

Conversely, when a left edge from the west swaps with a right edge from the
east, the corresponding balls **cease to overlap** .

###  cases (‚Üî( and )‚Üî)

Video: Animation of a L edge swapping with a L edge | Source: /notes/sweep-and-prune-2/swap-ll.mp4 

Edges of the same polarity can swap without affecting the overlappedness of
their corresponding balls. We can ignore these ones.

##  Swaps and sweeps

Based on these swap events we can reframe the mechanics of sweep-and-prune in
a new perspective, a bottom-up way centred around the swaps.

A fun way to think about it is to pretend that a right edge is equivalent to a
_localised_ sweep line. In that sense, the right edge _is_ the line sweeping
over these other left edges.

Video: Animation a line sweep vs animation of an edge swap | Source: /notes/sweep-and-prune-2/swap-as-sweep.mp4  An edge can be thought of as a local sweep line. 

Just as in a global sweep, passing over left edges will mark the corresponding
balls as ‚Äútouching‚Äù; in right-edge-as-a-local-sweep version, _swapping_
left edges will mark its ball as overlapping with the right edge‚Äôs ball.

In the global sweep, there is a global ` touching ` set keeping track of which
balls are in contact with the sweep line. In local swaps, we keep track of
overlaps _per ball_ . (More precisely, per pair.)

Lastly, in the global sweep, a right edge means the end of contact with a
ball. In a local swap, a left edge passing over a right edge means the same
thing. The corresponding balls are unmarked as overlapping.

Essentially, instead of a global sweep line, small local ‚Äúsweeps‚Äù happen
around each ball. Swaps become mini-sweeps.

Thus we arrive at the one-dimensional sweep-and-prune‚Äôs final form:

    
    
    function init() {
      overlapping = new Map()
    }
    
    function sweepAndPrune(edges) {
      
      for (let i = 1; i < edges.length; i++) {
        for (let j = i - 1; j >= 0; j--) {
          if (edges[j].x < edges[j + 1].x) break;
    
          
          [edges[j], edges[j + 1]] = [edges[j + 1], edges[j]];
    
          
    
          
          const edge1 = edges[j];
          const edge2 = edges[j + 1];
    
          if (edge1.isLeft && !edge2.isLeft) { 
            
            overlapping.set(
              key(edge1, edge2),
              [edge1.ball, edge2.ball]
            );
          } else if (!edge1.isLeft && edge2.isLeft) { 
            
            overlapping.delete(key(edge1, edge2));
          }
        }
      }
    
      return overlapping.values();
    }

It‚Äôs essentially insertion sort hooked up to track overlaps.

Let‚Äôs see it in action:

While it behaves the same and has the same time complexity as the preceding
variants, I‚Äôm guessing it‚Äôs practically much more efficient in terms of
processing speed. In video games where every frame has a processing budget,
the actual speed matters, not just the scalability. As always, benchmarking
will determine the real practical measurement of speed. (Disclaimer: I
haven‚Äôt done any benchmarks!)

##  Quick comparisons

Algorithm  |  Average time  |  Best time  |  Space   
---|---|---|---  
Global pairwise  |  O(n  2  )  |  O(n  2  )  |  O(1)   
Sorted pairwise (quicksort)  |  O(n log n + m)  |  O(n log n)  |  O(1)   
Sorted pairwise (insertion)  |  O(n + m)  |  O(n)  |  O(1)   
Sweep-and-prune (quicksort)  |  O(n log n + m)  |  O(n)  |  O(n)   
Sweep-and-prune (insertion)  |  O(n + m)  |  O(n)  |  O(n)   
Sweep-and-prune (final)  |  O(n + m)  |  O(n)  |  O(n + m)   
  
n = number of balls, m = number of collisions

(todo: Add benchmark here. I‚Äôm a little lazy right now. üò∫)

The real measure of speed lies in real measurements on real hardware!

> [ Stop Doing Algorithm Analysis
> ](https://www.reddit.com/r/ProgrammerHumor/comments/ncb11u/stop_doing_algorithm_analysis/)  
>  by [ u/theawesomenachos ](https://www.reddit.com/user/theawesomenachos/) in
> [ ProgrammerHumor ](https://www.reddit.com/r/ProgrammerHumor/)

##  Appendix

Things I‚Äôve noted or realised while writing this post:

  * General algorithm design insights 
    * Pre-sorting a list can replace a bunch of inequality checks, and unlocks: 
      * Some power when linearly scanning over the list 
      * Faster range / adjacency checks 
      * (unrelated, but good to bring up) Binary search 
    * Different sorting algorithms have situational strengths. 
  * Big O, while useful, can only go so far when analysing performance. 
  * I might need a frontend framework for my blog now, at least for the interactive demos. 
    * Vanilla JS is starting to get scary with bigger demos like these. 
    * ` .mjs ` is pretty good though. 

Bonus demo, 25 balls! It‚Äôs a ball party ‚öΩ‚öæüèÄüèê


-->

<!--






-->

