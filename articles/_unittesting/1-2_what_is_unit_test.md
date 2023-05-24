---
title: "2장 단위 테스트란 무엇인가"
date: 2022-03-11
header:
  teaser:  /assets/images/Khorikov-UT-HI.png
---

단위 테스트에 접근하는 방법은 고전파(classical school)와 런던파(London school)로 나뉘어 있다. 고전파는 모든 사람이 단위 테스트와 테스트 주도 개발에 원론적으로 접근하는 방식, 런던파는 런던의 프로그래밍 커뮤니티에서 시작되었다.

# 2.1 '단위 테스트'의 정의

단위 테스트는

* 작은 코드 조각 단위라고도 함)을 검증하고,
* 빠르게 수행하고,
* 격리된 방식으로 처리하는 자동화된 테스트다.

## 2.1.1 격리 문제에 대한 런던파의 접근

코드 조각(단위)을 격리된 방식으로 검증한다는 것은 무엇을 의미하는가? 런던파에서는 테스트 대상 시스템을 협력자(collaborator)에게서 격리하는 것을 일컫는다. 즉, 하나의 클래스가 다른 클래스 또는 여러 클래스에 의존하면 이 모든 의존성을 테스트 대역(test double)으로 대체해야 한다. 

|![](/assets/images/2022/2022-03-11-100314.png)|
|:--:|
|그림 2.1 테스트 대상 시스템의 의존성을 테스트 대역으로 대체하면, 테스트 대상 시스템만 검증하는 데 집중할 수 있다.|

온라인 상점을 운영한다고 가정하자. 샘플 애플리케이션에는 고객이 제품을 구매할 수 있다는 간단한 유스케이스use case가 하나 있다. 상점에 재고가 충분하면 구매는 성공으로 간주되고, 구매 수량만큼 상점의 제품 수량이 줄어든다. 제품이 충분하지 않으면 구매는 성공하지 못하며 상점에 아무 일도 일어나지 않는다.

예제 2.1에는 상점에 재고가 충분히 있을 때만 구매가 성공하는지 검증하는 두 가지 테스트가 있다. 테스트는 고전적인 스타일로 작성됐으며 일반적인 3단 구성인 준비, 실행, 검증 패턴(간단히 AAA<sup>Arrange, Act, Asset</sup> 패턴이라고 하며 3장에서 자세히 설명한다.)을 사용한다.

```csharp
// 예제 2.1 고전적인 스타일로 작성된 테스트

using Xunit;

namespace Book.Chapter2.Listing1
{
    public class CustomerTests
    {
        [Fact]
        public void Purchase_succeeds_when_enough_inventory()
        {
            // Arrange
            var store = new Store();
            store.AddInventory(Product.Shampoo, 10);
            var customer = new Customer();

            // Act
            bool success = customer.Purchase(store, Product.Shampoo, 5);

            // Assert
            Assert.True(success);
            Assert.Equal(5, store.GetInventory(Product.Shampoo));
        }

        [Fact]
        public void Purchase_fails_when_not_enough_inventory()
        {
            // Arrange
            var store = new Store();
            store.AddInventory(Product.Shampoo, 10);
            var customer = new Customer();

            // Act
            bool success = customer.Purchase(store, Product.Shampoo, 15);

            // Assert
            Assert.False(success);
            Assert.Equal(10, store.GetInventory(Product.Shampoo));
        }
    }
}
```

```csharp
// 참조

using System;
using System.Collections.Generic;

namespace Book.Chapter2.Listing1
{
    public class Store
    {
        private readonly Dictionary<Product, int> _inventory = new Dictionary<Product, int>();

        public bool HasEnoughInventory(Product product, int quantity)
        {
            return GetInventory(product) >= quantity;
        }

        public void RemoveInventory(Product product, int quantity)
        {
            if (!HasEnoughInventory(product, quantity))
            {
                throw new Exception("Not enough inventory");
            }

            _inventory[product] -= quantity;
        }

        public void AddInventory(Product product, int quantity)
        {
            if (_inventory.ContainsKey(product))
            {
                _inventory[product] += quantity;
            }
            else
            {
                _inventory.Add(product, quantity);
            }
        }

        public int GetInventory(Product product)
        {
            bool productExists = _inventory.TryGetValue(product, out int remaining);
            return productExists ? remaining : 0;
        }
    }

    public enum Product
    {
        Shampoo,
        Book
    }

    public class Customer
    {
        public bool Purchase(Store store, Product product, int quantity)
        {
            if (!store.HasEnoughInventory(product, quantity))
            {
                return false;
            }

            store.RemoveInventory(product, quantity);

            return true;
        }
    }
}
```

준비 부분은 의존성과 테스트 대상 시스템을 모두 준비하는 부분이다. ```customer.Purchase()``` 호출은 실행 단계이며 검증하고자 하는 동작을 수행한다. 검증문(assert statement)은 검증 단계이며, 동작이 예상 결과로 이어지는지 확인한다.

고객(Customer)은 테스트 대상 시스템(SUT, Systerm Under Test), 상점(Store)은 협력자에 해당한다. 다음 두 가지 이유로 협력자가 필요하다.

* 테스트 대상 메서드를 컴파일하려면 ```customer.Purchase()```가 Store 인스턴스를 인수로 필요 하다
* 검증 단계에서 ```customer.Purchase()```의 결과 중 하나로 상점 제품 수량이 감소할 가능성이 있다.

테스트에서 두 클래스는 서로 격리돼 있지 않기 때문에 Customer가 올바르게 작동하더라도 Customer에 영향을 미치는 Store 내부에 버그가 있으면 단위 테스트에 실패할 수 있다. 

이제 런던 스타일로 예제를 수정해보자. 동일한 테스트에서 Store 인스턴스는 테스트 대역, 구체적으로 목으로 교체해본다.

```csharp
// 예제 2.2 런던 스타일로 작성된 단위 테스트

using Moq;
using Xunit;

namespace Book.Chapter2.Listing2
{
    public class CustomerTests
    {
        [Fact]
        public void Purchase_succeeds_when_enough_inventory()
        {
            // Arrange
            var storeMock = new Mock<IStore>();
            storeMock
                .Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
                .Returns(true);
            var customer = new Customer();

            // Act
            bool success = customer.Purchase(storeMock.Object, Product.Shampoo, 5);

            // Assert
            Assert.True(success);
            storeMock.Verify(x => x.RemoveInventory(Product.Shampoo, 5), Times.Once);
        }

        [Fact]
        public void Purchase_fails_when_not_enough_inventory()
        {
            // Arrange
            var storeMock = new Mock<IStore>();
            storeMock
                .Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
                .Returns(false);
            var customer = new Customer();

            // Act
            bool success = customer.Purchase(storeMock.Object, Product.Shampoo, 5);

            // Assert
            Assert.False(success);
            storeMock.Verify(x => x.RemoveInventory(Product.Shampoo, 5), Times.Never);
        }
    }
}
```

```csharp
// 참조

using System;
using System.Collections.Generic;

namespace Book.Chapter2.Listing2
{
    public class Store : IStore
    {
        private readonly Dictionary<Product, int> _inventory = new Dictionary<Product, int>();

        public bool HasEnoughInventory(Product product, int quantity)
        {
            return GetInventory(product) >= quantity;
        }

        public void RemoveInventory(Product product, int quantity)
        {
            if (!HasEnoughInventory(product, quantity))
            {
                throw new Exception("Not enough inventory");
            }

            _inventory[product] -= quantity;
        }

        public void AddInventory(Product product, int quantity)
        {
            if (_inventory.ContainsKey(product))
            {
                _inventory[product] += quantity;
            }
            else
            {
                _inventory.Add(product, quantity);
            }
        }

        public int GetInventory(Product product)
        {
            bool productExists = _inventory.TryGetValue(product, out int remaining);
            return productExists ? remaining : 0;
        }
    }

    public interface IStore
    {
        bool HasEnoughInventory(Product product, int quantity);
        void RemoveInventory(Product product, int quantity);
        void AddInventory(Product product, int quantity);
        int GetInventory(Product product);
    }

    public enum Product
    {
        Shampoo,
        Book
    }

    public class Customer
    {
        public bool Purchase(IStore store, Product product, int quantity)
        {
            if (!store.HasEnoughInventory(product, quantity))
            {
                return false;
            }

            store.RemoveInventory(product, quantity);

            return true;
        }
    }
}
```

준비 단계에서 테스트는 Store의 실제 인스턴스를 생성하지 않고 Moq의 내장 클래스인 ```Mock<T>```를 사용해 대체한다. 테스트는 더 이상 Store를 사용하지 않는다. Store 클래스 대신 IStore 인터페이스로 목을 만들어 사용했다. 

고전적인 방법에서는 상점 상태를 검증했다. 지금은 Customer와 Store 간의 상호 작용을 검사한다. 고객이 상점으로 호출해야 하는 메서드(x.RemoveInventory)뿐만 아니라 호출 횟수까지 검증할 수 있다. 고객은 구매가 성공하면 이 메서드를 한 번만 호출해야 하고(Times.Once), 구매가 실패하면 절대로 호출하면 안된다(Times.Never).

## 2.1.2 격리 문제에 대한 고전파의 접근

런던 스타일은 테스트 대역(목)으로 테스트 대상 코드 조각을 분리해서 격리 요구 사항에 다가간다. 

고전적인 방법에서 코드를 꼭 격리하는 방식으로 테스트해야 하는 것은 아니다. 대신 단위 테스트는 서로 격리해서 실행해야 한다. 이렇게 하면 테스트를 어떤 순서(병렬이나 순차 등)로든 가장 적합한 방식으로 실행할 수 있으며 서로의 결과에 영향을 미치지 않는다.

각각의 테스트를 격리하는 것은 여러 클래스가 모두 메모리에 상주하고 공유 상태에 도달하지 않는 한, 여러 클래스를 한 번에 테스트해도 괜찮다는 뜻이다. 이를 통해 테스트가 서로 소통하고 실행 컨텍스트에 영향을 줄 수 있다. 데이터베이스, 파일 시스템 등 프로세스 외부 의존성이 이러한 공유 상태의 대표적인 예다.

> **공유 의존성, 비공개 의존성, 프로세스 외부 의존성**
>
> 공유 의존성(shared dependency)은 테스트 간에 공유되고 서로의 결과에 영향을 미칠 수 있는 수단을 제공하는 의존성이다. 대표적으로 정적 가변 필드(static mutable field)가 있다. 데이터베이스도 공유 의존성의 전형적인 예가 될 수 있다.
>
> 비공개 의존성(private dependency)은 공유하지 않는 의존성이다.
>
> 프로세스 외부 의존성(out-of-process dependency)은 애플리케이션 실행 프로세스 외부에서 실행되는 의존성이다. 프로세스 외부 의존성은 대부분 공유 의존성에 해당하지만 모두 그런 것은 아니다. 예를 들어 데이터베이스는 프로세스 외부이면서 공유 의존성이다. 그러나 각 테스트 실행 전에 도커 컨테이너로 데이터베이스를 시작하면 테스트가 더 이상 동일한 인스턴스로 작동하지 않기 때문에 프로세스 외부이면서 공유하지 않는 의존성이 된다.

|![](/assets/images/2022/2022-03-11-105320.png)|
|:--:|
| 그림 23 단의 테스트를 서로 격리하는 것은 테스트 대상 클래스에서 공유 의존성만 격리하는 것을 의미한다. 비공개 의존성은 그대르 둘 수 있다.|

공유 의존성을 대체하는 또 다른 이유는 테스트 실행 속도를 높이는 데 있다. 공유 의존성은 거의 항상 실행 프로세스 외부에 있는 데 반해, 비공개 의존성은 보통 그 경계를 넘지 않는다. 따라서 데이터베이스나 파일 시스템 등의 공유 의존성에 대한 호출은 비공개 의존성에 대한 호출보다 더 오래 걸린다.

# 2.2 단위 테스트의 런던파와 고전파

격리 특성에 따라 런던파와 고전파로 나뉘어 진다.

||격리 특성|격리 주체|단위의 크기|테스트 대역 사용 대상|
|:--:|:--|:--|:--|:--|
|런던파|테스트 대상 시스템에서 협력자를 격리|코드 조각(단위)|단일 클래스|불변 의존성 외 모든 의존성|
|고전파|단위 테스트끼리 격리|단위 테스트|단일 클래스 또는 클래스 세트|공유 의존성|

## 2.2.1 고전파와 런던파가 의존성을 다루는 방법

테스트 대역을 어디에서나 흔히 사용할 수 있지만, 런던파는 테스트에서 일부 의존성을 그대로 사용할 수 있도록 하고 있다. 