---
title : "3A – Arrange, Act, Assert"
date: 2022-01-01
---

> 본 글은 [Bill Wake](https://xp123.com/articles/contact/)의 [3A – Arrange, Act, Assert](https://xp123.com/articles/3a-arrange-act-assert/)내용을 번역한 글 입니다.

# 어떻게 좋은 테스트를 만들 것인가?

몇몇의 테스트는 명확해 보이지만 다른 테스트들은 구문을 실행하는것처럼 보인다. 어떻게 하면 내용이 잘 전달되면서 명확하게 정의된 테스트를 만들 수 있을까?

> 좋은 유닛 테스트의 구조는 무었인가? <br> 3A: Arrange, Act, Assert

우리는 오브젝트의 동작를 테스트 하는것을 원한다. 한가지 좋은 접근 방법은 오브젝트를 하나의 관심있는 환경에 집어 넣고 여러 동작을 취하는것이다.

오브젝트가 가지고 있는 다양한 타입의 동작는 다음과 같다.
* Constructors
* Mutators, also known as modifiers or commands
* Accessors, also known as queries
* Iterators

나는 오래전에 이러한 분리법을 배웠다 하지만 어디서 배웠는지는 기억하지 못한다. (아마 추상 데이터 타입 연구였던것 같다.) 이는 Bertrand Meyer의 "[명령 쿼리 분리](https://en.wikipedia.org/wiki/Command%E2%80%93query_separation)"원칙에 구체화되어 있으며 다른 사람들이 독자적으로 발명했다.

이러한 차이를 염두에두고 테스트를 만들 수 있다.

* Arrange: 테스트 할 오브젝트의 집합. collaborators들로 둘러쌓인 오브젝트가 필요 할 수도 있다. 테스트 목적을 위해 collaborators는 테스트용 오브젝트(mocks, fakes, etc.)나 실제 오브젝트가 될 수 있다.

* Act: 오즈젝트에 가하는 행동(일부 mutator를 통해서). 때로는 파라미터(테스트 오브젝트가 될 수도 있다.)를 줄 수도 있다.

* Assert: collaborators, 파리미터, 드물게는 전역 변수에 관련된 오브젝트에 대한 요구를 만든다. 

# 어디서 부터 시작해야 하는가?

Arrange가 먼저 나오기 때문에 먼저 쓰는 것이 자연스러운 것이라고 생각할 수 있다.

객체의 동작을 체계적으로 처리 한다면 Act를 먼저 작성할 수 있다.

하지만 
But a useful technique I learned from Jim Newkirk is that writing the Assert first is a great place to start. When you have a new behavior you know you want to test, Assert First lets you start by asking “Suppose it worked; how would I be able to tell?” With the Assert in place, you can do what Industrial Logic calls “Frame First” and lean on the IDE to “fill in the blanks.”

# FAQ

Aren’t some things easier to test with a sequence of actions and assertions?

Occasionally a sequence is needed, but the 3A pattern is partly a reaction to large tests that look like this:

    Arrange
    Act
    Assert
    Act
    Assert
    Arrange more
    Act
    Assert
    …

To understand a test like that, you have to track state over a series of activities. It’s hard to see what object is the focus of the test, and it’s hard to see that you’ve covered each interesting case. Such multi-step unit tests are usually better off being split into several tests.

But I won’t say “never do it”; there could be some case where the goal is to track a cumulative state and it’s just easier to understand in one series of calls. 

Sometimes we want to make sure of our setup. Is it OK to have an extra assert?

Such a test looks like this:

    Arrange
    Assert that the setup is OK
    Act
    Assert that the behavior is right

First, consider whether this should be two separate tests, or whether setup is too complicated (if we can’t trust objects to be in the initial state we want). Still, if it seems necessary to do this checking, it’s worth bending the guideline.

What about the notion of having “one assert per test”?

I don’t follow that guideline too closely. I consider it for two things: 

    A series of assertions may indicate the object is missing functionality which should be added (and tested). The classical case is equals(): It’s better to define an equals() method than (possibly create and) repeat a bunch of assertions about held data.
    A series of similar assertions might benefit from a helper (assertion) method.

(If an object has many accessors, it may indicate the object is doing too much.)

When a test modifies an object, I typically find it easiest to consider most accessors together. 

For example, consider a list that tracks the number of objects and the maximum entry. One test might look like this:

    List list = new List();
    list.add(3);
    assertEquals(1, list.size());
    assertEquals(3, list.max());

That is, it considers the case “what all happens when one item is inserted into an empty list?” Then the various assertions each explore a different “dimension” of the object.

 What about setup?

Most xUnit frameworks let you define a method that is called before each test. This lets you pull out some common code for the tests, and it is part of the initial Arrange. (Thus you have to look in two places to understand the full Arrange-ment.)

What about teardown?

Most xUnit frameworks let you define a method that is called after each test. For example, if a test opens a file connection, the teardown could close that connection.

If you need teardown, use it, of course. But I’m not adding a fourth A to the pattern: most unit tests don’t need teardown. Unit tests (for the bulk of the system) don’t talk to external systems, databases, files, etc., and Arrange-Act-Assert is a pattern for unit tests. 