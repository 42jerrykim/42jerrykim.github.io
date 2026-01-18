---
collection_order: 17
title: "[Design Pattern] Iterator - 반복자 패턴"
description: "Iterator 패턴은 컬렉션 내부 구조를 노출하지 않고 요소들을 순차적으로 접근하게 합니다. 일관된 인터페이스로 다양한 집합체를 순회하며 유연성을 높입니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Iterator
  - 반복자
  - Behavioral Pattern
  - 행위 패턴
  - GoF
  - Gang of Four
  - Collection
  - 컬렉션
  - Aggregate
  - 집합체
  - Traversal
  - 순회
  - Cursor
  - 커서
  - hasNext
  - next
  - Internal Iterator
  - 내부 반복자
  - External Iterator
  - 외부 반복자
  - Encapsulation
  - 캡슐화
  - Single Responsibility
  - 단일 책임
  - Iterable
  - For Each
  - Generator
  - 제너레이터
  - Code Reusability
  - 코드 재사용성
  - Maintainability
  - 유지보수성
  - Software Design
  - 소프트웨어 설계
  - OOP
  - 객체지향 프로그래밍
  - Java
  - C++
  - Python
  - C#
  - ArrayList
  - LinkedList
  - HashMap
  - Stream API
---

반복자 패턴(Iterator Pattern)은 컬렉션의 내부 구조를 노출하지 않고 그 안의 요소들을 순차적으로 접근할 수 있게 해주는 행위 디자인 패턴이다. 이 패턴을 사용하면 다양한 종류의 컬렉션(배열, 리스트, 트리 등)을 동일한 방식으로 순회할 수 있다.

## 개요

**반복자 패턴의 정의**

반복자 패턴은 집합체(Aggregate)의 요소들을 순회하는 책임을 반복자(Iterator) 객체에 분리한다. 클라이언트는 컬렉션의 내부 구조(배열인지, 연결 리스트인지)를 알 필요 없이 동일한 인터페이스로 순회할 수 있다.

**패턴의 필요성 및 사용 사례**

반복자 패턴은 다음과 같은 상황에서 유용하다:

- **컬렉션 추상화**: 다양한 자료구조를 동일한 방식으로 순회
- **내부 구조 은닉**: 컬렉션의 구현 세부사항 숨김
- **다중 순회**: 동시에 여러 반복자로 독립적 순회
- **다양한 순회 방식**: 정방향, 역방향, 필터링 순회 등
- **지연 평가**: 필요할 때만 요소 생성 (Generator)

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 단일 책임 원칙 (순회 로직 분리) | 간단한 컬렉션에는 과도한 설계 |
| 다양한 컬렉션의 일관된 순회 | 직접 접근보다 성능이 약간 느릴 수 있음 |
| 동시에 여러 순회 가능 | 일부 특수 컬렉션에는 부적합 |
| 새로운 순회 방식 추가 용이 | Iterator 상태 관리 필요 |

## 반복자 패턴의 구성 요소

```
┌──────────────────────┐          ┌──────────────────────┐
│   <<interface>>      │          │    <<interface>>     │
│      Iterable        │          │      Iterator        │
├──────────────────────┤          ├──────────────────────┤
│ + createIterator()   │          │ + hasNext(): bool    │
└──────────┬───────────┘          │ + next(): T          │
           │                      │ + current(): T       │
           │                      └──────────┬───────────┘
           │                                 │
           │                                 │
┌──────────────────────┐          ┌──────────────────────┐
│  ConcreteIterable    │─────────▶│  ConcreteIterator    │
├──────────────────────┤          ├──────────────────────┤
│ - elements: T[]      │          │ - collection         │
├──────────────────────┤          │ - currentIndex       │
│ + createIterator()   │          ├──────────────────────┤
│ + getElement(i)      │          │ + hasNext()          │
│ + size()             │          │ + next()             │
└──────────────────────┘          │ + current()          │
                                  └──────────────────────┘
```

**1. Iterator (반복자)**
- 요소 접근과 순회를 위한 인터페이스
- hasNext(), next(), current() 등의 메서드 정의

**2. ConcreteIterator (구체적 반복자)**
- Iterator 인터페이스 구현
- 현재 위치 추적 및 다음 요소 반환

**3. Iterable/Aggregate (집합체)**
- Iterator를 생성하는 인터페이스
- createIterator() 메서드 제공

**4. ConcreteIterable (구체적 집합체)**
- 실제 요소들을 저장하는 컬렉션
- 해당 컬렉션을 위한 Iterator 생성

## 내부 반복자 vs 외부 반복자

### 외부 반복자 (External Iterator)
클라이언트가 순회를 제어

```python
iterator = collection.iterator()
while iterator.has_next():
    item = iterator.next()
    process(item)
```

### 내부 반복자 (Internal Iterator)
컬렉션이 순회를 제어, 클라이언트는 처리 로직만 제공

```python
collection.for_each(lambda item: process(item))
```

## 구현 예제

### Python 예제 - 사용자 정의 컬렉션

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

# Iterator 인터페이스
class Iterator(ABC, Generic[T]):
    @abstractmethod
    def has_next(self) -> bool:
        pass
    
    @abstractmethod
    def next(self) -> T:
        pass
    
    @abstractmethod
    def reset(self) -> None:
        pass

# Iterable 인터페이스
class Iterable(ABC, Generic[T]):
    @abstractmethod
    def create_iterator(self) -> Iterator[T]:
        pass

# 책 클래스
class Book:
    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year
    
    def __str__(self) -> str:
        return f"'{self.title}' by {self.author} ({self.year})"

# ConcreteIterable - 책장
class BookShelf(Iterable[Book]):
    def __init__(self):
        self._books: List[Book] = []
    
    def add_book(self, book: Book) -> None:
        self._books.append(book)
    
    def get_book(self, index: int) -> Book:
        return self._books[index]
    
    def size(self) -> int:
        return len(self._books)
    
    def create_iterator(self) -> Iterator[Book]:
        return BookShelfIterator(self)
    
    def create_reverse_iterator(self) -> Iterator[Book]:
        return ReverseBookShelfIterator(self)
    
    def create_filtered_iterator(self, year_from: int) -> Iterator[Book]:
        return FilteredBookIterator(self, year_from)

# ConcreteIterator - 순방향 반복자
class BookShelfIterator(Iterator[Book]):
    def __init__(self, bookshelf: BookShelf):
        self._bookshelf = bookshelf
        self._index = 0
    
    def has_next(self) -> bool:
        return self._index < self._bookshelf.size()
    
    def next(self) -> Book:
        if not self.has_next():
            raise StopIteration("No more books")
        book = self._bookshelf.get_book(self._index)
        self._index += 1
        return book
    
    def reset(self) -> None:
        self._index = 0

# ConcreteIterator - 역방향 반복자
class ReverseBookShelfIterator(Iterator[Book]):
    def __init__(self, bookshelf: BookShelf):
        self._bookshelf = bookshelf
        self._index = bookshelf.size() - 1
    
    def has_next(self) -> bool:
        return self._index >= 0
    
    def next(self) -> Book:
        if not self.has_next():
            raise StopIteration("No more books")
        book = self._bookshelf.get_book(self._index)
        self._index -= 1
        return book
    
    def reset(self) -> None:
        self._index = self._bookshelf.size() - 1

# ConcreteIterator - 필터링 반복자
class FilteredBookIterator(Iterator[Book]):
    def __init__(self, bookshelf: BookShelf, year_from: int):
        self._bookshelf = bookshelf
        self._year_from = year_from
        self._index = 0
        self._advance_to_next_valid()
    
    def _advance_to_next_valid(self) -> None:
        while (self._index < self._bookshelf.size() and 
               self._bookshelf.get_book(self._index).year < self._year_from):
            self._index += 1
    
    def has_next(self) -> bool:
        return self._index < self._bookshelf.size()
    
    def next(self) -> Book:
        if not self.has_next():
            raise StopIteration("No more books")
        book = self._bookshelf.get_book(self._index)
        self._index += 1
        self._advance_to_next_valid()
        return book
    
    def reset(self) -> None:
        self._index = 0
        self._advance_to_next_valid()

# 사용 예제
if __name__ == "__main__":
    # 책장 생성 및 책 추가
    shelf = BookShelf()
    shelf.add_book(Book("1984", "George Orwell", 1949))
    shelf.add_book(Book("Clean Code", "Robert C. Martin", 2008))
    shelf.add_book(Book("Design Patterns", "GoF", 1994))
    shelf.add_book(Book("The Pragmatic Programmer", "Hunt & Thomas", 2019))
    shelf.add_book(Book("Brave New World", "Aldous Huxley", 1932))
    
    # 순방향 순회
    print("=== 순방향 순회 ===")
    iterator = shelf.create_iterator()
    while iterator.has_next():
        print(f"  {iterator.next()}")
    
    # 역방향 순회
    print("\n=== 역방향 순회 ===")
    reverse_iter = shelf.create_reverse_iterator()
    while reverse_iter.has_next():
        print(f"  {reverse_iter.next()}")
    
    # 필터링 순회 (2000년 이후 출판)
    print("\n=== 2000년 이후 출판 ===")
    filtered_iter = shelf.create_filtered_iterator(2000)
    while filtered_iter.has_next():
        print(f"  {filtered_iter.next()}")
    
    # Python의 Iterator Protocol 구현
    print("\n=== Python Iterator Protocol ===")
    
    class PythonBookShelf:
        def __init__(self):
            self._books = []
        
        def add_book(self, book):
            self._books.append(book)
        
        def __iter__(self):
            return iter(self._books)
        
        def __len__(self):
            return len(self._books)
    
    py_shelf = PythonBookShelf()
    py_shelf.add_book(Book("Python Crash Course", "Eric Matthes", 2015))
    py_shelf.add_book(Book("Fluent Python", "Luciano Ramalho", 2015))
    
    for book in py_shelf:
        print(f"  {book}")
```

### Java 예제 - 소셜 네트워크 프로필 순회

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// 프로필 클래스
class Profile {
    private String id;
    private String name;
    private String email;
    private List<String> friends;
    
    public Profile(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.friends = new ArrayList<>();
    }
    
    public void addFriend(String friendId) {
        friends.add(friendId);
    }
    
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public List<String> getFriends() { return friends; }
    
    @Override
    public String toString() {
        return String.format("%s (%s) - %d friends", name, email, friends.size());
    }
}

// Iterator 인터페이스
interface ProfileIterator {
    boolean hasNext();
    Profile getNext();
    void reset();
}

// Iterable 인터페이스
interface SocialNetwork {
    ProfileIterator createFriendsIterator(String profileId);
    ProfileIterator createCoworkersIterator(String profileId);
}

// ConcreteIterable - 소셜 네트워크
class Facebook implements SocialNetwork {
    private Map<String, Profile> profiles = new HashMap<>();
    
    public void addProfile(Profile profile) {
        profiles.put(profile.getId(), profile);
    }
    
    public Profile getProfile(String id) {
        return profiles.get(id);
    }
    
    public List<String> getFriendIds(String profileId) {
        Profile profile = profiles.get(profileId);
        return profile != null ? profile.getFriends() : Collections.emptyList();
    }
    
    // 협업자 관계 시뮬레이션 (여기서는 친구의 친구)
    public List<String> getCoworkerIds(String profileId) {
        Set<String> coworkers = new HashSet<>();
        Profile profile = profiles.get(profileId);
        if (profile != null) {
            for (String friendId : profile.getFriends()) {
                Profile friend = profiles.get(friendId);
                if (friend != null) {
                    coworkers.addAll(friend.getFriends());
                }
            }
            coworkers.remove(profileId); // 자기 자신 제외
            coworkers.removeAll(profile.getFriends()); // 직접 친구 제외
        }
        return new ArrayList<>(coworkers);
    }
    
    @Override
    public ProfileIterator createFriendsIterator(String profileId) {
        return new FacebookIterator(this, "friends", profileId);
    }
    
    @Override
    public ProfileIterator createCoworkersIterator(String profileId) {
        return new FacebookIterator(this, "coworkers", profileId);
    }
}

// ConcreteIterator - Facebook 반복자
class FacebookIterator implements ProfileIterator {
    private Facebook facebook;
    private String type;
    private String profileId;
    private int currentIndex = 0;
    private List<String> cache = new ArrayList<>();
    
    public FacebookIterator(Facebook facebook, String type, String profileId) {
        this.facebook = facebook;
        this.type = type;
        this.profileId = profileId;
        lazyLoad();
    }
    
    private void lazyLoad() {
        if (cache.isEmpty()) {
            if ("friends".equals(type)) {
                cache = facebook.getFriendIds(profileId);
            } else if ("coworkers".equals(type)) {
                cache = facebook.getCoworkerIds(profileId);
            }
        }
    }
    
    @Override
    public boolean hasNext() {
        return currentIndex < cache.size();
    }
    
    @Override
    public Profile getNext() {
        if (!hasNext()) {
            return null;
        }
        String friendId = cache.get(currentIndex);
        currentIndex++;
        return facebook.getProfile(friendId);
    }
    
    @Override
    public void reset() {
        currentIndex = 0;
    }
}

// 사용 예제
public class IteratorDemo {
    public static void main(String[] args) {
        // 소셜 네트워크 설정
        Facebook facebook = new Facebook();
        
        Profile alice = new Profile("1", "Alice", "alice@email.com");
        Profile bob = new Profile("2", "Bob", "bob@email.com");
        Profile charlie = new Profile("3", "Charlie", "charlie@email.com");
        Profile david = new Profile("4", "David", "david@email.com");
        Profile eve = new Profile("5", "Eve", "eve@email.com");
        
        // 친구 관계 설정
        alice.addFriend("2"); alice.addFriend("3");
        bob.addFriend("1"); bob.addFriend("4");
        charlie.addFriend("1"); charlie.addFriend("5");
        david.addFriend("2");
        eve.addFriend("3");
        
        facebook.addProfile(alice);
        facebook.addProfile(bob);
        facebook.addProfile(charlie);
        facebook.addProfile(david);
        facebook.addProfile(eve);
        
        // Alice의 친구 순회
        System.out.println("=== Alice의 친구 ===");
        ProfileIterator friendsIterator = facebook.createFriendsIterator("1");
        while (friendsIterator.hasNext()) {
            Profile friend = friendsIterator.getNext();
            System.out.println("  " + friend);
        }
        
        // Alice의 협업자 (친구의 친구) 순회
        System.out.println("\n=== Alice의 협업자 (친구의 친구) ===");
        ProfileIterator coworkersIterator = facebook.createCoworkersIterator("1");
        while (coworkersIterator.hasNext()) {
            Profile coworker = coworkersIterator.getNext();
            System.out.println("  " + coworker);
        }
    }
}
```

### C# 예제 - 트리 구조 순회

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;
using System.Collections;
using System.Collections.Generic;

// 트리 노드
public class TreeNode<T>
{
    public T Value { get; set; }
    public List<TreeNode<T>> Children { get; } = new List<TreeNode<T>>();
    
    public TreeNode(T value)
    {
        Value = value;
    }
    
    public void AddChild(TreeNode<T> child)
    {
        Children.Add(child);
    }
}

// 트리 순회 방식
public enum TraversalType
{
    DepthFirst,   // 깊이 우선 (전위)
    BreadthFirst  // 너비 우선
}

// 트리 클래스 (IEnumerable 구현)
public class Tree<T> : IEnumerable<T>
{
    public TreeNode<T> Root { get; private set; }
    
    public Tree(T rootValue)
    {
        Root = new TreeNode<T>(rootValue);
    }
    
    public IEnumerator<T> GetEnumerator()
    {
        return new DepthFirstIterator<T>(Root);
    }
    
    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }
    
    public IEnumerable<T> DepthFirst()
    {
        return new TreeTraversal<T>(Root, TraversalType.DepthFirst);
    }
    
    public IEnumerable<T> BreadthFirst()
    {
        return new TreeTraversal<T>(Root, TraversalType.BreadthFirst);
    }
}

// 순회 가능한 래퍼
public class TreeTraversal<T> : IEnumerable<T>
{
    private readonly TreeNode<T> _root;
    private readonly TraversalType _type;
    
    public TreeTraversal(TreeNode<T> root, TraversalType type)
    {
        _root = root;
        _type = type;
    }
    
    public IEnumerator<T> GetEnumerator()
    {
        return _type switch
        {
            TraversalType.DepthFirst => new DepthFirstIterator<T>(_root),
            TraversalType.BreadthFirst => new BreadthFirstIterator<T>(_root),
            _ => throw new ArgumentException("Unknown traversal type")
        };
    }
    
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

// 깊이 우선 반복자
public class DepthFirstIterator<T> : IEnumerator<T>
{
    private readonly TreeNode<T> _root;
    private readonly Stack<TreeNode<T>> _stack = new Stack<TreeNode<T>>();
    private TreeNode<T> _current;
    
    public DepthFirstIterator(TreeNode<T> root)
    {
        _root = root;
        Reset();
    }
    
    public T Current => _current.Value;
    
    object IEnumerator.Current => Current;
    
    public bool MoveNext()
    {
        if (_stack.Count == 0)
            return false;
        
        _current = _stack.Pop();
        
        // 자식들을 역순으로 스택에 추가 (왼쪽부터 방문하기 위해)
        for (int i = _current.Children.Count - 1; i >= 0; i--)
        {
            _stack.Push(_current.Children[i]);
        }
        
        return true;
    }
    
    public void Reset()
    {
        _stack.Clear();
        if (_root != null)
            _stack.Push(_root);
        _current = null;
    }
    
    public void Dispose() { }
}

// 너비 우선 반복자
public class BreadthFirstIterator<T> : IEnumerator<T>
{
    private readonly TreeNode<T> _root;
    private readonly Queue<TreeNode<T>> _queue = new Queue<TreeNode<T>>();
    private TreeNode<T> _current;
    
    public BreadthFirstIterator(TreeNode<T> root)
    {
        _root = root;
        Reset();
    }
    
    public T Current => _current.Value;
    
    object IEnumerator.Current => Current;
    
    public bool MoveNext()
    {
        if (_queue.Count == 0)
            return false;
        
        _current = _queue.Dequeue();
        
        foreach (var child in _current.Children)
        {
            _queue.Enqueue(child);
        }
        
        return true;
    }
    
    public void Reset()
    {
        _queue.Clear();
        if (_root != null)
            _queue.Enqueue(_root);
        _current = null;
    }
    
    public void Dispose() { }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        // 트리 구조 생성
        //         1
        //       / | \
        //      2  3  4
        //     / \    |
        //    5   6   7
        
        var tree = new Tree<int>(1);
        var node2 = new TreeNode<int>(2);
        var node3 = new TreeNode<int>(3);
        var node4 = new TreeNode<int>(4);
        var node5 = new TreeNode<int>(5);
        var node6 = new TreeNode<int>(6);
        var node7 = new TreeNode<int>(7);
        
        tree.Root.AddChild(node2);
        tree.Root.AddChild(node3);
        tree.Root.AddChild(node4);
        node2.AddChild(node5);
        node2.AddChild(node6);
        node4.AddChild(node7);
        
        // 깊이 우선 순회
        Console.WriteLine("=== 깊이 우선 순회 (DFS) ===");
        foreach (var value in tree.DepthFirst())
        {
            Console.Write($"{value} ");
        }
        Console.WriteLine();
        
        // 너비 우선 순회
        Console.WriteLine("\n=== 너비 우선 순회 (BFS) ===");
        foreach (var value in tree.BreadthFirst())
        {
            Console.Write($"{value} ");
        }
        Console.WriteLine();
        
        // 기본 foreach (깊이 우선)
        Console.WriteLine("\n=== 기본 foreach ===");
        foreach (var value in tree)
        {
            Console.Write($"{value} ");
        }
        Console.WriteLine();
        
        // LINQ 활용
        Console.WriteLine("\n=== LINQ 활용 ===");
        var evenNumbers = tree.BreadthFirst().Where(x => x % 2 == 0);
        Console.WriteLine("짝수만: " + string.Join(", ", evenNumbers));
    }
}
```

## 실제 사용 사례

### 1. Java Iterator / Iterable
```java
List<String> list = Arrays.asList("a", "b", "c");
Iterator<String> it = list.iterator();
while (it.hasNext()) {
    System.out.println(it.next());
}
```

### 2. Python Iterator Protocol
```python
for item in collection:
    print(item)
```

### 3. C# IEnumerable / IEnumerator
```csharp
foreach (var item in collection)
{
    Console.WriteLine(item);
}
```

### 4. JavaScript Symbol.iterator
```javascript
for (const item of collection) {
    console.log(item);
}
```

## 관련 패턴

| 패턴 | 반복자와의 관계 |
|------|--------------|
| **Composite** | Composite 구조를 순회할 때 Iterator 사용 |
| **Factory Method** | Iterator 생성에 Factory 사용 |
| **Memento** | Iterator가 현재 상태를 저장/복원 |
| **Visitor** | 순회 + 각 요소에 연산 적용 시 함께 사용 |

## FAQ

**Q1: 외부 반복자와 내부 반복자의 차이점은?**

외부 반복자는 클라이언트가 직접 순회를 제어(hasNext/next 호출)하고, 내부 반복자는 컬렉션이 순회를 제어하며 클라이언트는 콜백(람다)만 제공합니다.

**Q2: 순회 중 컬렉션을 수정하면 어떻게 되나요?**

대부분의 언어에서 ConcurrentModificationException 같은 예외가 발생합니다. 안전한 수정을 위해서는 Iterator의 remove() 메서드를 사용하거나 복사본을 만들어야 합니다.

**Q3: Generator와 Iterator의 차이는?**

Generator는 지연 평가(lazy evaluation)를 통해 필요할 때마다 값을 생성하는 특수한 Iterator입니다. 메모리 효율적이며 무한 시퀀스도 표현할 수 있습니다.

**Q4: 커스텀 Iterator는 언제 필요한가요?**

기본 컬렉션 외의 자료구조(그래프, 트리 등)를 순회하거나, 필터링/변환이 포함된 순회, 역방향 순회 등 특수한 순회 방식이 필요할 때 커스텀 Iterator를 구현합니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Java Iterator 인터페이스 문서
- Python Iterator Protocol (PEP 234)