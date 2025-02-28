---
title: "[Data Structure] C#에서의 Lock-Free 우선순위 큐 구현"
categories:
- Data Structure
- Priority Queue
date: 2025-02-28
tags: 
- DataStructure
- PriorityQueue
- C#
- 동시성 프로그래밍
- 우선순위 큐
- Concurrent Programming
- Priority Queue
- Lock-Free
- Thread-Safe
- Data Structure
- Atomic Operations
- CAS
- Multithreading
- Synchronization
- Performance
- Scalability
- Resource Management
- Queue Operations
- Enqueue
- Dequeue
- Data Integrity
- Consistency
- High Performance
- Software Development
- System Design
- Algorithm Optimization
- Memory Management
- ABA Problem
- Free List
- Event Handling
- Task Scheduling
- Load Balancing
- Application Architecture
- Code Complexity
- Error Handling
- Debugging
- Testing
- Software Engineering
- Data Loss Prevention
- Concurrency Control
- Thread Management
- Resource Allocation
- System Performance
- Application Performance
- User Experience
- Software Reliability
- Code Quality
- Design Patterns
- Object-Oriented Programming
- Functional Programming
- Asynchronous Programming
- Distributed Systems
- Cloud Computing
- 우선순위 큐
- C#
- 동시성 프로그래밍
- 우선순위 큐
- 락 프리
- 스레드 안전
- 자료구조
- 원자적 연산
- CAS
- 멀티스레딩
- 동기화
- 성능
- 확장성
- 자원 관리
- 큐 연산
- 삽입
- 제거
- 데이터 무결성
- 일관성
- 고성능
- 소프트웨어 개발
- 시스템 설계
- 알고리즘 최적화
- 메모리 관리
- ABA 문제
- 프리 리스트
- 이벤트 처리
- 작업 스케줄링
- 로드 밸런싱
- 애플리케이션 아키텍처
- 코드 복잡성
- 오류 처리
- 디버깅
- 테스트
- 소프트웨어 공학
- 데이터 손실 방지
- 동시성 제어
- 스레드 관리
- 자원 할당
- 시스템 성능
- 애플리케이션 성능
- 사용자 경험
- 소프트웨어 신뢰성
- 코드 품질
- 디자인 패턴
- 객체 지향 프로그래밍
- 함수형 프로그래밍
- 비동기 프로그래밍
- 분산 시스템
- 클라우드 컴퓨팅
description: "동시성 프로그래밍에서 우선순위 큐는 중요한 자료구조로, 멀티스레드 환경에서 lock-free하고 thread-safe하게 구현하는 것이 필수적이다. 이 보고서는 C#에서 우선순위 큐를 구현하는 방법과 관련 개념, 문제 해결 기법을 다룬다. 우선순위 큐는 FIFO 큐와 달리 각 요소에 우선순위를 부여하여 처리 순서를 조정할 수 있는 장점이 있다."
image: index.png

---

동시성 프로그래밍에서 우선순위 큐는 중요한 자료구조이며, 특히 멀티스레드 환경에서 lock-free하고 thread-safe하게 구현하는 것은 고성능 애플리케이션 개발에 필수적이다. 이 보고서에서는 C\#에서 lock-free하고 thread-safe한 우선순위 큐를 구현하는 방법과 관련 개념, 구현 접근법, 그리고 실제 코드 예시를 상세히 다루고자 한다. 동시성 환경에서 발생할 수 있는 문제점과 이를 해결하기 위한 다양한 기법들을 살펴보며, 실제 애플리케이션에서 활용할 수 있는 우선순위 큐 구현 방법을 제시한다.

## 우선순위 큐와 동시성 프로그래밍의 이해

우선순위 큐는 일반적인 FIFO(First In, First Out) 큐와 달리 각 요소에 우선순위가 부여되어 우선순위가 높은 요소가 먼저 처리되는 자료구조이다. 멀티스레드 환경에서 이러한 우선순위 큐를 사용할 때는 여러 스레드가 동시에 접근하여 데이터를 추가하거나 제거하는 경우에도 정확성을 보장해야 한다.

동시성 프로그래밍은 대규모 데이터를 처리하는 기업용 프로젝트에서 핵심적인 도전 과제 중 하나이다. 프로젝트가 확장되고 많은 사용자를 확보하게 되면, 아무리 강력한 서버라도 결국 병목 현상에 직면하게 된다[^8]. 전 세계 사용자가 동시에 수만 개의 요청을 보내는 글로벌 프로젝트를 개발한다고 상상해보자. 무제한 서버 용량을 가정하지 않는 한, 서버가 이 모든 요청을 효율적으로 처리할 수 있을까?

동시성 프로그래밍은 이러한 여러 동시 요청을 처리하기 위한 기술이다. 모든 것을 한 번에 처리하여 서버에 과부하를 주는 대신, 들어오는 작업을 큐에 넣고 하나씩 처리하는 것이 더 효율적인 경우가 많다[^8]. 우선순위 큐를 사용하면 이러한 작업들 중에서도 중요도나 긴급성에 따라 처리 순서를 조정할 수 있는 이점이 있다.

### Lock-Free 자료구조의 개념

Lock-free 자료구조는 전통적인 잠금 메커니즘(mutex, semaphore 등)을 사용하지 않고도 여러 스레드가 안전하게 데이터에 접근할 수 있도록 설계된 자료구조이다. 이러한 접근 방식은 일반적으로 원자적 연산(atomic operations)과 CAS(Compare-And-Swap) 기법을 사용하여 구현된다.

Lock-free 자료구조를 구현할 때는 이른바 ABA 문제에 주의해야 한다. 이 문제는 스레드가 값을 A에서 B로 변경한 후 다시 A로 변경하는 상황에서 발생한다. 이전 연구에서는 free list를 사용한 lock-free 구현이 ABA 문제로 인해 오류가 발생할 수 있다고 지적하고 있다[^1].

### Thread-Safe 프로그래밍의 중요성

Thread-safe한 코드는 여러 스레드가 동시에 실행될 때도 정확한 결과를 보장한다. 우선순위 큐와 같은 자료구조에서 thread safety는 데이터 일관성과 무결성을 유지하는 데 필수적이다. 특히 큐의 삽입(enqueue)과 제거(dequeue) 연산이 원자적으로 수행되지 않으면, 데이터 손실이나 중복 처리와 같은 문제가 발생할 수 있다.

## C\#에서의 우선순위 큐 구현 접근법

C\#에서 lock-free하고 thread-safe한 우선순위 큐를 구현하기 위한 여러 접근법이 있다. 각 접근법은 특정 상황에서 장단점을 가지고 있으므로, 애플리케이션의 요구사항에 따라 적절한 방법을 선택해야 한다.

### 제한된 우선순위 레벨을 가진 우선순위 큐

일반적인 우선순위 큐는 광범위하고 복잡한 주제이다. 이를 단순화하기 위해, 구현을 제한된 수의 명확한 우선순위 레벨로 제한할 수 있다. 이러한 접근법은 코드 복잡성을 줄이고, 더 중요하게는 enqueue와 dequeue 연산의 시간 복잡도를 개선할 수 있다[^4].

이러한 제한된 우선순위 큐는 대역폭 관리, 명령 실행 우선순위 지정, 서로 다른 소스에서 이벤트를 우선순위 기반으로 병합하는 등의 사례에서 좋은 선택이 될 수 있다. 간단히 말해, 개발 중에 우선순위 레벨을 알 수 있는 경우에 적합하다[^4].

```csharp
public enum QueuePriority
{
    Lower,
    Normal,
    High
}
```

위 코드는 우선순위 큐 구현에 사용될 수 있는 간단한 우선순위 열거형이다[^4]. 이러한 명확한 우선순위 레벨을 사용하면 구현이 더 간단해지고 성능도 향상될 수 있다.

### ReaderWriterLockSlim을 사용한 구현

thread-safe한 우선순위 큐를 구현하는 한 가지 방법은 ReaderWriterLockSlim을 사용하는 것이다. 이 클래스는 .NET에서 제공하는 고급 동기화 메커니즘으로, 여러 읽기 작업이 동시에 진행될 수 있지만 쓰기 작업은 독점적으로 수행되도록 보장한다. 자세한 내용은 [ReaderWriterLockSlim 문서](https://learn.microsoft.com/ko-kr/dotnet/api/system.threading.readerwriterlockslim?view=net-9.0)를 참조하길 바란다.

GitHub에서 공유된 예제 코드는 ReaderWriterLockSlim을 사용하여 thread-safe한 우선순위 큐를 구현하는 방법을 보여준다[^6]:

```csharp
public class PriorityQueue<T> where T : class
{
    private Comparer<T> comparer;
    private ReaderWriterLockSlim rwLock = new ReaderWriterLockSlim();
    private List<T> list = new List<T>();

    // 이하 코드 생략
}
```

이 구현에서는 내부적으로 List<T>를 사용하고 힙(heap) 속성을 유지하기 위한 메서드를 포함하고 있다. ReaderWriterLockSlim을 사용하여 읽기 작업(예: Count 속성 접근)과 쓰기 작업(예: Enqueue, Dequeue 메서드)을 동기화한다[^6].

### .NET 6의 내장 PriorityQueue 활용

.NET 6부터는 PriorityQueue 클래스가 기본적으로 제공되고 있다. 이 클래스는 요소가 지정된 우선순위 값에 따라 정렬되는 큐 유형이다[^7]. 그러나 기본 PriorityQueue는 thread-safe하지 않기 때문에, 멀티스레드 환경에서 사용하려면 적절한 동기화 메커니즘을 추가해야 한다.

```csharp
// .NET 6에서 PriorityQueue 인스턴스 생성
PriorityQueue<string, int> priorityQueue = new PriorityQueue<string, int>();
```

Enqueue() 메서드를 사용하여 PriorityQueue에 항목을 추가할 수 있으며, 이 메서드는 두 개의 매개변수(요소와 우선순위 값)를 받는다[^7].

## Lock-Free, Thread-Safe 우선순위 큐 구현

이제 C\#에서 lock-free하고 thread-safe한 우선순위 큐를 구현하는 실제 코드를 살펴보자. 이 구현은 앞서 논의한 개념과 접근법을 조합하여 효율적이고 안전한 우선순위 큐를 제공한다.

### CAS 연산을 활용한 Lock-Free 구현

Lock-free 자료구조는 일반적으로 CAS(Compare-And-Swap) 연산을 기반으로 구현된다. CAS는 원자적으로 메모리 위치의 값을 예상 값과 비교하고, 일치하는 경우에만 새 값으로 업데이트하는 연산이다.

C\#에서는 Interlocked.CompareExchange 메서드를 사용하여 CAS 연산을 수행할 수 있다. 이를 활용하여 lock-free 우선순위 큐를 구현할 수 있다.

```csharp
using System;
using System.Threading;
using System.Collections.Generic;

public class LockFreePriorityQueue<T> where T : class, IComparable<T>
{
    private class Node
    {
        public T Value;
        public Node Next;

        public Node(T value)
        {
            Value = value;
            Next = null;
        }
    }

    private Node head;

    public LockFreePriorityQueue()
    {
        head = null;
    }

    public void Enqueue(T item)
    {
        Node newNode = new Node(item);
        Node current, next;

        do
        {
            current = head;

            // 빈 큐이거나 새 항목의 우선순위가 head보다 높은 경우
            if (current == null || item.CompareTo(current.Value) < 0)
            {
                newNode.Next = current;
                // CAS를 사용하여 head를 원자적으로 업데이트
                if (Interlocked.CompareExchange(ref head, newNode, current) == current)
                    return;
            }
            else
            {
                // 적절한 위치를 찾을 때까지 연결 리스트 탐색
                do
                {
                    next = current.Next;
                    // 리스트의 끝에 도달했거나 적절한 위치를 찾은 경우
                    if (next == null || item.CompareTo(next.Value) < 0)
                        break;
                    current = next;
                } while (true);

                // 새 노드를 적절한 위치에 삽입
                newNode.Next = next;
                if (Interlocked.CompareExchange(ref current.Next, newNode, next) == next)
                    return;
            }
            // CAS가 실패한 경우 다시 시도
        } while (true);
    }

    public bool TryDequeue(out T result)
    {
        Node current, next;

        do
        {
            current = head;
            if (current == null)
            {
                result = default(T);
                return false;
            }

            next = current.Next;
            // CAS를 사용하여 head를 원자적으로 업데이트
            if (Interlocked.CompareExchange(ref head, next, current) == current)
            {
                result = current.Value;
                return true;
            }
            // CAS가 실패한 경우 다시 시도
        } while (true);
    }

    public T Dequeue()
    {
        T result;
        if (TryDequeue(out result))
            return result;
        throw new InvalidOperationException("Queue is empty");
    }

    public bool IsEmpty => head == null;
}
```

이 구현은 연결 리스트를 기반으로 하며, 요소는 우선순위에 따라 정렬된다. Enqueue와 Dequeue 연산은 CAS를 사용하여 원자적으로 수행되며, 외부 잠금 메커니즘 없이도 thread-safe하게 동작한다.

### 다중 우선순위 레벨 지원 구현

더 복잡한 시나리오에서는 여러 우선순위 레벨을 지원하는 우선순위 큐가 필요할 수 있다. 이를 위해 각 우선순위 레벨에 대해 별도의 lock-free 큐를 유지하는 방식으로 구현할 수 있다.

```csharp
using System;
using System.Threading;
using System.Collections.Generic;

public enum Priority
{
    Low,
    Normal,
    High,
    Critical
}

public class MultiLevelPriorityQueue<T> where T : class
{
    private readonly LockFreeQueue<T>[] queues;

    public MultiLevelPriorityQueue()
    {
        int levelCount = Enum.GetValues(typeof(Priority)).Length;
        queues = new LockFreeQueue<T>[levelCount];
        
        for (int i = 0; i < levelCount; i++)
        {
            queues[i] = new LockFreeQueue<T>();
        }
    }

    public void Enqueue(T item, Priority priority)
    {
        queues[(int)priority].Enqueue(item);
    }

    public T Dequeue()
    {
        // 높은 우선순위부터 낮은 우선순위 순으로 확인
        for (int i = queues.Length - 1; i >= 0; i--)
        {
            T item;
            if (queues[i].TryDequeue(out item))
                return item;
        }
        
        throw new InvalidOperationException("Queue is empty");
    }

    public bool TryDequeue(out T result)
    {
        result = default(T);
        
        // 높은 우선순위부터 낮은 우선순위 순으로 확인
        for (int i = queues.Length - 1; i >= 0; i--)
        {
            if (queues[i].TryDequeue(out result))
                return true;
        }
        
        return false;
    }

    public bool IsEmpty
    {
        get
        {
            for (int i = 0; i < queues.Length; i++)
            {
                if (!queues[i].IsEmpty)
                    return false;
            }
            return true;
        }
    }
}

// 단순한 lock-free 큐 구현
public class LockFreeQueue<T> where T : class
{
    private class Node
    {
        public T Value;
        public Node Next;

        public Node(T value = default(T))
        {
            Value = value;
            Next = null;
        }
    }

    private Node head;
    private Node tail;

    public LockFreeQueue()
    {
        head = tail = new Node();
    }

    public void Enqueue(T item)
    {
        Node newNode = new Node(item);
        Node oldTail, oldNext;

        while (true)
        {
            oldTail = tail;
            oldNext = oldTail.Next;

            // tail이 변경되었는지 확인
            if (oldTail != tail)
                continue;

            // 다른 스레드가 enqueue를 완료하지 않은 경우 도움
            if (oldNext != null)
            {
                Interlocked.CompareExchange(ref tail, oldNext, oldTail);
                continue;
            }

            // 새 노드를 tail.Next에 추가
            if (Interlocked.CompareExchange(ref oldTail.Next, newNode, null) == null)
                break;
        }

        // tail을 새 노드로 업데이트
        Interlocked.CompareExchange(ref tail, newNode, oldTail);
    }

    public bool TryDequeue(out T result)
    {
        Node oldHead, oldTail, oldHeadNext;

        while (true)
        {
            oldHead = head;
            oldTail = tail;
            oldHeadNext = oldHead.Next;

            // head가 변경되었는지 확인
            if (oldHead != head)
                continue;

            // 빈 큐인 경우
            if (oldHeadNext == null)
            {
                result = default(T);
                return false;
            }

            // head와 tail이 같은데 next가 null이 아닌 경우(다른 스레드가 enqueue 중)
            if (oldHead == oldTail)
            {
                Interlocked.CompareExchange(ref tail, oldHeadNext, oldTail);
                continue;
            }

            // head를 다음 노드로 업데이트
            if (Interlocked.CompareExchange(ref head, oldHeadNext, oldHead) == oldHead)
            {
                result = oldHeadNext.Value;
                return true;
            }
        }
    }

    public bool IsEmpty => head.Next == null;
}
```

이 구현은 각 우선순위 레벨에 대해 별도의 lock-free 큐를 유지하며, Dequeue 연산 시 높은 우선순위의 큐부터 확인한다. 이 접근법은 제한된 우선순위 레벨을 가진 시나리오에서 효율적으로 작동한다.

## .NET 6 PriorityQueue를 활용한 Thread-Safe 구현

.NET 6에서 도입된 PriorityQueue 클래스는 내부적으로 이진 힙을 사용하여 우선순위 큐 기능을 제공한다. 그러나 이 클래스는 기본적으로 thread-safe하지 않다. 여기서는 이 클래스를 thread-safe하게 만드는 래퍼 클래스를 구현해 보자.

```csharp
using System;
using System.Threading;
using System.Collections.Generic;

public class ThreadSafePriorityQueue<TElement, TPriority> where TPriority : IComparable<TPriority>
{
    private readonly PriorityQueue<TElement, TPriority> queue;
    private readonly ReaderWriterLockSlim rwLock;

    public ThreadSafePriorityQueue()
    {
        queue = new PriorityQueue<TElement, TPriority>();
        rwLock = new ReaderWriterLockSlim();
    }

    public void Enqueue(TElement element, TPriority priority)
    {
        rwLock.EnterWriteLock();
        try
        {
            queue.Enqueue(element, priority);
        }
        finally
        {
            rwLock.ExitWriteLock();
        }
    }

    public TElement Dequeue()
    {
        rwLock.EnterWriteLock();
        try
        {
            return queue.Dequeue();
        }
        finally
        {
            rwLock.ExitWriteLock();
        }
    }

    public bool TryDequeue(out TElement element, out TPriority priority)
    {
        rwLock.EnterWriteLock();
        try
        {
            return queue.TryDequeue(out element, out priority);
        }
        finally
        {
            rwLock.ExitWriteLock();
        }
    }

    public TElement Peek()
    {
        rwLock.EnterReadLock();
        try
        {
            return queue.Peek();
        }
        finally
        {
            rwLock.ExitReadLock();
        }
    }

    public bool TryPeek(out TElement element, out TPriority priority)
    {
        rwLock.EnterReadLock();
        try
        {
            return queue.TryPeek(out element, out priority);
        }
        finally
        {
            rwLock.ExitReadLock();
        }
    }

    public int Count
    {
        get
        {
            rwLock.EnterReadLock();
            try
            {
                return queue.Count;
            }
            finally
            {
                rwLock.ExitReadLock();
            }
        }
    }

    public void Clear()
    {
        rwLock.EnterWriteLock();
        try
        {
            queue.Clear();
        }
        finally
        {
            rwLock.ExitWriteLock();
        }
    }
}
```

이 구현은 내장 PriorityQueue 클래스를 감싸고 ReaderWriterLockSlim을 사용하여 thread safety를 보장한다. 읽기 작업(Peek, TryPeek, Count)은 읽기 잠금을, 쓰기 작업(Enqueue, Dequeue, TryDequeue, Clear)은 쓰기 잠금을 사용한다.

### Await 가능한 동시성 우선순위 큐

좀 더 복잡한 시나리오에서는 await 가능한 우선순위 큐가 필요할 수 있다. 이러한 큐는 항목이 큐에 추가될 때까지 비동기적으로 대기할 수 있는 기능을 제공한다.

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Collections.Concurrent;

public class AwaitablePriorityQueue<T> where T : class
{
    private readonly SemaphoreSlim semaphore = new SemaphoreSlim(0);
    private readonly ConcurrentDictionary<int, ConcurrentQueue<T>> queues = new ConcurrentDictionary<int, ConcurrentQueue<T>>();
    private readonly List<int> priorityLevels = new List<int>();
    private readonly object syncRoot = new object();

    public AwaitablePriorityQueue()
    {
    }

    private ConcurrentQueue<T> GetOrCreateQueue(int priority)
    {
        return queues.GetOrAdd(priority, _ =>
        {
            lock (syncRoot)
            {
                if (!priorityLevels.Contains(priority))
                {
                    priorityLevels.Add(priority);
                    priorityLevels.Sort();
                }
            }
            return new ConcurrentQueue<T>();
        });
    }

    public void Enqueue(T item, int priority)
    {
        ConcurrentQueue<T> queue = GetOrCreateQueue(priority);
        queue.Enqueue(item);
        semaphore.Release();
    }

    public T Dequeue()
    {
        semaphore.Wait();
        return DequeueInternal();
    }

    public async Task<T> DequeueAsync(CancellationToken cancellationToken = default)
    {
        await semaphore.WaitAsync(cancellationToken);
        return DequeueInternal();
    }

    private T DequeueInternal()
    {
        lock (syncRoot)
        {
            // 우선순위 높은 순으로 확인
            for (int i = priorityLevels.Count - 1; i >= 0; i--)
            {
                int priority = priorityLevels[i];
                if (queues.TryGetValue(priority, out ConcurrentQueue<T> queue))
                {
                    T item;
                    if (queue.TryDequeue(out item))
                        return item;
                }
            }
        }

        // 항목을 찾지 못한 경우(semaphore가 신호를 보냈지만 다른 스레드가 이미 항목을 가져간 경우)
        // 이는 버그이므로 예외 발생
        throw new InvalidOperationException("Inconsistent queue state");
    }

    public bool TryDequeue(out T result)
    {
        if (semaphore.Wait(0))
        {
            result = DequeueInternal();
            return true;
        }
        
        result = default(T);
        return false;
    }

    public bool IsEmpty => semaphore.CurrentCount == 0;
    
    public int Count => semaphore.CurrentCount;
}
```

이 구현은 SemaphoreSlim을 사용하여 큐에 항목이 추가될 때까지 비동기적으로 대기할 수 있는 기능을 제공한다. 내부적으로는 ConcurrentDictionary와 ConcurrentQueue를 사용하여 여러 우선순위 레벨을 관리한다.

## 우선순위 큐 구현의 성능 및 최적화

우선순위 큐의 성능은 구현 방식과 사용 사례에 따라 크게 달라질 수 있다. 여기서는 다양한 구현의 성능 특성과 최적화 방법에 대해 알아보자.

### 시간 복잡도 분석

우선순위 큐의 일반적인 연산(Enqueue, Dequeue, Peek)의 시간 복잡도는 구현 방식에 따라 다르다:

1. 힙 기반 구현:
    - Enqueue: O(log n)
    - Dequeue: O(log n)
    - Peek: O(1)
2. 정렬된 리스트 기반 구현:
    - Enqueue: O(n)
    - Dequeue: O(1)
    - Peek: O(1)
3. 제한된 우선순위 레벨을 가진 멀티큐 구현:
    - Enqueue: O(1)
    - Dequeue: O(k), 여기서 k는 우선순위 레벨의 수
    - Peek: O(k)

Lock-free 구현에서는 경합(contention)이 성능에 큰 영향을 미친다. 많은 스레드가 동시에 작업할 경우, CAS 연산의 재시도로 인해 성능이 저하될 수 있다.

### 벤치마크 결과

다양한 우선순위 큐 구현의 성능을 비교하기 위한 벤치마크 코드는 다음과 같다:

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using System.Diagnostics;
using System.Collections.Concurrent;

public class PriorityQueueBenchmark
{
    private const int OperationCount = 1000000;
    private const int ThreadCount = 8;

    public static async Task RunBenchmarkAsync()
    {
        Console.WriteLine("Starting benchmark...");
        Console.WriteLine($"Operations: {OperationCount}, Threads: {ThreadCount}");
        Console.WriteLine();

        // 다양한 우선순위 큐 구현 벤치마크
        await BenchmarkQueueAsync("LockFreePriorityQueue", () => new LockFreePriorityQueue<int>());
        await BenchmarkQueueAsync("MultiLevelPriorityQueue", () => new MultiLevelPriorityQueue<int>());
        await BenchmarkQueueAsync("ThreadSafePriorityQueue", () => new ThreadSafePriorityQueue<int, int>());
        await BenchmarkQueueAsync("AwaitablePriorityQueue", () => new AwaitablePriorityQueue<int>());
        
        Console.WriteLine("Benchmark completed.");
    }

    private static async Task BenchmarkQueueAsync<T>(string name, Func<T> queueFactory) where T : class
    {
        Console.WriteLine($"Benchmarking {name}...");
        
        T queue = queueFactory();
        Stopwatch sw = new Stopwatch();
        
        // 벤치마크 준비
        CountdownEvent readySignal = new CountdownEvent(ThreadCount);
        ManualResetEventSlim startSignal = new ManualResetEventSlim(false);
        CountdownEvent completedSignal = new CountdownEvent(ThreadCount);
        
        // 작업 분배
        int opsPerThread = OperationCount / ThreadCount;
        
        // 스레드 생성
        Task[] tasks = new Task[ThreadCount];
        for (int i = 0; i < ThreadCount; i++)
        {
            int threadId = i;
            tasks[i] = Task.Run(() =>
            {
                // 스레드 준비 완료 알림
                readySignal.Signal();
                // 모든 스레드가 동시에 시작할 수 있도록 대기
                startSignal.Wait();
                
                // 벤치마크 실행
                Random random = new Random(threadId);
                for (int j = 0; j < opsPerThread; j++)
                {
                    // 50% 확률로 Enqueue, 50% 확률로 Dequeue
                    if (random.Next(2) == 0)
                    {
                        // 특정 우선순위 큐 구현에 맞게 Enqueue 메서드 호출
                        // 이 부분은 각 구현에 맞게 수정해야 함
                    }
                    else
                    {
                        // 특정 우선순위 큐 구현에 맞게 Dequeue 메서드 호출
                        // 이 부분은 각 구현에 맞게 수정해야 함
                    }
                }
                
                // 스레드 작업 완료 알림
                completedSignal.Signal();
            });
        }
        
        // 모든 스레드가 준비될 때까지 대기
        readySignal.Wait();
        
        // 벤치마크 시작
        sw.Start();
        startSignal.Set();
        
        // 모든 스레드가 완료될 때까지 대기
        await Task.Run(() => completedSignal.Wait());
        sw.Stop();
        
        Console.WriteLine($"{name} completed in {sw.ElapsedMilliseconds} ms");
        Console.WriteLine($"Operations per second: {OperationCount * 1000 / sw.ElapsedMilliseconds:N0}");
        Console.WriteLine();
    }
}
```

이 벤치마크 코드는 다양한 우선순위 큐 구현의 성능을 측정하며, 실제 Enqueue와 Dequeue 메서드 호출 부분은 각 구현에 맞게 수정해야 한다.

### 공간 복잡도와 최적화

우선순위 큐의 공간 복잡도는 일반적으로 O(n)이다. 그러나 구현 방식에 따라 추가적인 공간 오버헤드가 발생할 수 있다.

공간 최적화를 위한 몇 가지 기법은 다음과 같다:

1. 배열 기반 힙: 동적 배열을 사용하여 힙을 구현하면 포인터 오버헤드를 줄일 수 있다.
2. 노드 풀링: 노드 객체를 재사용하여 가비지 컬렉션 부하를 줄일 수 있다.
3. 제한된 우선순위 레벨: 우선순위 레벨의 수를 제한하면 메모리 사용량을 줄일 수 있다.

시간 최적화를 위한 기법은 다음과 같다:

1. 인라이닝: 자주 호출되는 작은 메서드는 인라인화하여 메서드 호출 오버헤드를 줄일 수 있다.
2. SIMD 활용: 적절한 경우 SIMD(Single Instruction, Multiple Data) 연산을 활용하여 성능을 향상시킬 수 있다.
3. 캐시 지역성 고려: 메모리 접근 패턴을 최적화하여 캐시 히트율을 높일 수 있다.

## 우선순위 큐의 실제 활용 사례

우선순위 큐는 다양한 실제 애플리케이션에서 유용하게 활용된다. 여기서는 몇 가지 주요 활용 사례에 대해 알아보자.

### 대역폭 관리

네트워크 애플리케이션에서 우선순위 큐는 데이터 패킷의 우선순위를 관리하는 데 사용될 수 있다. 예를 들어, 실시간 비디오 스트리밍은 이메일 전송보다 높은 우선순위를 가질 수 있다[^4].

```csharp
// 네트워크 패킷을 위한 우선순위 큐 구현
public class NetworkPacketQueue
{
    private readonly ThreadSafePriorityQueue<Packet, int> queue = new ThreadSafePriorityQueue<Packet, int>();
    
    public void EnqueuePacket(Packet packet)
    {
        // 패킷 유형에 따라 우선순위 결정
        int priority = DeterminePriority(packet);
        queue.Enqueue(packet, priority);
    }
    
    public Packet DequeuePacket()
    {
        return queue.Dequeue();
    }
    
    private int DeterminePriority(Packet packet)
    {
        switch (packet.Type)
        {
            case PacketType.RealTimeVideo:
                return 100;
            case PacketType.VoiceCall:
                return 80;
            case PacketType.InteractiveData:
                return 60;
            case PacketType.BackgroundDownload:
                return 40;
            case PacketType.Email:
                return 20;
            default:
                return 0;
        }
    }
}
```


### 작업 스케줄링

운영 체제의 작업 스케줄러는 우선순위 큐를 사용하여 CPU 시간을 할당할 작업의 순서를 결정한다. 높은 우선순위를 가진 작업은 낮은 우선순위의 작업보다 먼저 실행된다.

```csharp
// 작업 스케줄러 구현
public class TaskScheduler
{
    private readonly AwaitablePriorityQueue<Task> taskQueue = new AwaitablePriorityQueue<Task>();
    private readonly CancellationTokenSource cts = new CancellationTokenSource();
    private readonly Thread[] workerThreads;
    
    public TaskScheduler(int threadCount)
    {
        workerThreads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++)
        {
            workerThreads[i] = new Thread(WorkerThreadFunc);
            workerThreads[i].Start();
        }
    }
    
    public void ScheduleTask(Task task, TaskPriority priority)
    {
        taskQueue.Enqueue(task, (int)priority);
    }
    
    private void WorkerThreadFunc()
    {
        while (!cts.Token.IsCancellationRequested)
        {
            try
            {
                Task task = taskQueue.DequeueAsync(cts.Token).Result;
                task.Execute();
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error executing task: {ex.Message}");
            }
        }
    }
    
    public void Shutdown()
    {
        cts.Cancel();
        foreach (Thread thread in workerThreads)
        {
            thread.Join();
        }
    }
}

public enum TaskPriority
{
    Low = 0,
    BelowNormal = 1,
    Normal = 2,
    AboveNormal = 3,
    High = 4,
    Realtime = 5
}
```


### 이벤트 기반 시스템

이벤트 기반 시스템에서 우선순위 큐는 이벤트의 처리 순서를 결정하는 데 사용될 수 있다. 중요한 이벤트는 덜 중요한 이벤트보다 먼저 처리된다.

```csharp
// 이벤트 처리 시스템 구현
public class EventProcessor<T> where T : IEvent
{
    private readonly ThreadSafePriorityQueue<T, int> eventQueue = new ThreadSafePriorityQueue<T, int>();
    private readonly Thread processingThread;
    private readonly CancellationTokenSource cts = new CancellationTokenSource();
    private readonly ManualResetEventSlim waitHandle = new ManualResetEventSlim(false);
    
    public EventProcessor()
    {
        processingThread = new Thread(ProcessEvents);
        processingThread.Start();
    }
    
    public void EnqueueEvent(T @event)
    {
        eventQueue.Enqueue(@event, @event.Priority);
        waitHandle.Set();
    }
    
    private void ProcessEvents()
    {
        while (!cts.Token.IsCancellationRequested)
        {
            if (eventQueue.Count == 0)
            {
                waitHandle.Reset();
                waitHandle.Wait(cts.Token);
                continue;
            }
            
            T @event = eventQueue.Dequeue();
            ProcessEvent(@event);
        }
    }
    
    private void ProcessEvent(T @event)
    {
        try
        {
            @event.Process();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error processing event: {ex.Message}");
        }
    }
    
    public void Shutdown()
    {
        cts.Cancel();
        waitHandle.Set();
        processingThread.Join();
    }
}

public interface IEvent
{
    int Priority { get; }
    void Process();
}
```


### 그래프 알고리즘

다익스트라(Dijkstra) 알고리즘과 같은 그래프 알고리즘은 우선순위 큐를 사용하여 가장 비용이 적은 노드를 효율적으로 선택한다. 이를 통해 시간 복잡도를 O(V²)에서 O(E log V)로 줄일 수 있다(V는 정점 수, E는 간선 수).

```csharp
// 다익스트라 알고리즘 구현
public class Dijkstra
{
    public static Dictionary<int, int> FindShortestPaths(Graph graph, int startVertex)
    {
        Dictionary<int, int> distances = new Dictionary<int, int>();
        PriorityQueue<int, int> priorityQueue = new PriorityQueue<int, int>();
        
        // 초기화
        foreach (int vertex in graph.Vertices)
        {
            distances[vertex] = vertex == startVertex ? 0 : int.MaxValue;
        }
        
        priorityQueue.Enqueue(startVertex, 0);
        
        while (priorityQueue.Count > 0)
        {
            priorityQueue.TryDequeue(out int currentVertex, out int currentDistance);
            
            // 이미 더 짧은 경로를 찾은 경우 스킵
            if (currentDistance > distances[currentVertex])
                continue;
            
            foreach (var neighbor in graph.GetNeighbors(currentVertex))
            {
                int newDistance = currentDistance + neighbor.Weight;
                
                // 더 짧은 경로를 찾은 경우 업데이트
                if (newDistance < distances[neighbor.Vertex])
                {
                    distances[neighbor.Vertex] = newDistance;
                    priorityQueue.Enqueue(neighbor.Vertex, newDistance);
                }
            }
        }
        
        return distances;
    }
}
```


## 우선순위 큐 구현 시 주의사항

우선순위 큐, 특히 lock-free하고 thread-safe한 구현을 개발할 때는 몇 가지 주의사항을 고려해야 한다.

### ABA 문제와 해결책

ABA 문제는 병렬 프로그래밍에서 발생하는 중요한 문제 중 하나이다. 이 문제는 스레드가 메모리 위치의 값을 A에서 변경할 예정인데, 다른 스레드가 그 값을 A에서 B로, 다시 A로 변경한 경우에 발생한다. 첫 번째 스레드는 값이 여전히 A이므로 변경을 진행하지만, 실제로는 중간에 B로 변경되었다가 다시 A로 돌아온 것이다.

Lock-free 구현에서 이 문제를 해결하기 위한 방법은 다음과 같다:

1. 버전 번호 사용: 포인터와 함께 버전 번호를 저장하여 ABA 문제를 감지한다.
2. 해저드 포인터(Hazard Pointers): 스레드가 접근 중인 객체를 추적하여 다른 스레드가 해당 객체를 수정하지 못하도록 한다.
3. RCU(Read-Copy-Update): 읽기 작업이 진행 중인 동안에는 쓰기 작업이 이전 버전을 수정하지 않도록 한다.

### 메모리 관리와 가비지 컬렉션 문제

C\#은 가비지 컬렉션(GC)을 사용하여 메모리를 관리하지만, 고성능 애플리케이션에서는 GC로 인한 성능 저하가 문제가 될 수 있다. 이를 최소화하기 위한 방법은 다음과 같다:

1. 객체 재사용: 객체 풀을 사용하여 객체를 재사용하고 GC 부하를 줄인다.
2. 값 타입 사용: 가능한 경우 참조 타입 대신 값 타입을 사용하여 GC 부하를 줄인다.
3. 큰 객체 힙 관리: 대규모 데이터 구조는 큰 객체 힙(Large Object Heap)에 할당되므로 이를 고려하여 설계한다.
```csharp
// 객체 풀 구현 예시
public class NodePool<T> where T : class
{
    private readonly ConcurrentBag<Node<T>> pool = new ConcurrentBag<Node<T>>();
    
    public Node<T> Rent()
    {
        if (pool.TryTake(out Node<T> node))
            return node;
        
        return new Node<T>();
    }
    
    public void Return(Node<T> node)
    {
        node.Value = default;
        node.Next = null;
        pool.Add(node);
    }
}

public class Node<T> where T : class
{
    public T Value;
    public Node<T> Next;
}
```

### 데드락과 라이브락 방지

Lock-free 구현은 데드락의 위험을 제거하지만, 라이브락과 같은 다른 문제가 발생할 수 있다. 라이브락은 스레드가 계속 실행되지만 진행하지 못하는 상태를 말한다. 이를 방지하기 위한 방법은 다음과 같다:

1. 지수 백오프: CAS 연산이 실패할 경우 지수적으로 증가하는 시간만큼 대기 후 재시도한다.
2. 임의성 도입: 여러 스레드가 동일한 패턴으로 경합하는 것을 방지하기 위해 임의의 요소를 도입한다.

```csharp
// 지수 백오프 구현 예시
private void EnqueueWithBackoff(T item, int priority)
{
    Random random = new Random();
    int backoff = 1;
    
    while (true)
    {
        if (TryEnqueue(item, priority))
            return;
        
        // 백오프 시간만큼 대기
        Thread.Sleep(random.Next(0, backoff));
        
        // 백오프 시간을 두 배로 증가(최대 한도까지)
        backoff = Math.Min(backoff * 2, MaxBackoff);
    }
}
```

### 테스트와 검증

Lock-free 알고리즘과 thread-safe 구현은 테스트하기 어렵다. 다음과 같은 테스트 방법을 사용하여 구현의 정확성을 검증할 수 있다:

1. 단위 테스트: 기본 기능을 검증하는 단위 테스트를 작성한다.
2. 스트레스 테스트: 여러 스레드가 동시에 많은 수의 작업을 수행하도록 하여 경쟁 조건을 테스트한다.
3. 모델 검사: 정형 검증 도구를 사용하여 알고리즘의 정확성을 검증한다. 예를 들어, 검색 결과[^2]에서 언급된 SPIN 모델 체커가 있다.

```csharp
// 스트레스 테스트 예시
[Test]
public void StressTest()
{
    ThreadSafePriorityQueue<int, int> queue = new ThreadSafePriorityQueue<int, int>();
    const int ThreadCount = 10;
    const int OperationsPerThread = 10000;
    
    ConcurrentBag<int> dequeued = new ConcurrentBag<int>();
    CountdownEvent countdown = new CountdownEvent(ThreadCount);
    
    // 스레드 생성 및 시작
    for (int i = 0; i < ThreadCount; i++)
    {
        int threadId = i;
        Task.Run(() =>
        {
            Random random = new Random(threadId);
            
            for (int j = 0; j < OperationsPerThread; j++)
            {
                int value = threadId * OperationsPerThread + j;
                
                // 절반은 Enqueue, 절반은 Dequeue
                if (j % 2 == 0)
                {
                    queue.Enqueue(value, random.Next(100));
                }
                else
                {
                    try
                    {
                        if (queue.TryDequeue(out int result, out int _))
                        {
                            dequeued.Add(result);
                        }
                    }
                    catch (InvalidOperationException)
                    {
                        // 큐가 비어 있을 수 있음
                    }
                }
            }
            
            countdown.Signal();
        });
    }
    
    // 모든 스레드가 완료될 때까지 대기
    countdown.Wait();
    
    // 최종 큐에 남아 있는 항목 처리
    while (queue.Count > 0)
    {
        dequeued.Add(queue.Dequeue());
    }
    
    // 결과 검증
    Assert.AreEqual(ThreadCount * OperationsPerThread / 2, dequeued.Count);
}
```

## 결론

C\#에서 lock-free하고 thread-safe한 우선순위 큐를 구현하는 것은 복잡하지만 중요한 작업이다. 이 보고서에서는 다양한 구현 접근법과 실제 코드 예시를 통해 이러한 우선순위 큐를 구현하는 방법을 살펴보았다.

기본적인 lock-free 우선순위 큐부터 다중 우선순위 레벨 지원, .NET 6의 내장 PriorityQueue를 활용한 thread-safe 구현, 그리고 await 가능한 우선순위 큐까지 다양한 방식의 구현을 알아보았다. 또한 성능 최적화, 메모리 관리, ABA 문제와 같은 주의사항과 이를 해결하기 위한 방법도 논의하였다.

각 구현 방식은 특정 사용 사례에 맞게 선택해야 한다. 간단한 애플리케이션에서는 .NET 6의 내장 PriorityQueue와 간단한 잠금 메커니즘을 조합한 구현이 충분할 수 있다. 반면, 고성능이 요구되는 애플리케이션에서는 CAS 연산을 활용한 lock-free 구현이나 제한된 우선순위 레벨을 가진 멀티큐 구현이 더 적합할 수 있다.

중요한 것은 개발하려는 애플리케이션의 요구사항을 명확히 이해하고, 그에 맞는 우선순위 큐 구현을 선택하는 것이다. 또한 철저한 테스트와 검증을 통해 구현의 정확성을 보장해야 한다.

동시성 프로그래밍은 어렵지만 중요한 분야이며, 우선순위 큐는 이러한 동시성 환경에서 자원을 효율적으로 관리하기 위한 필수적인 도구이다. 이 보고서가 C\#에서 lock-free하고 thread-safe한 우선순위 큐를 구현하는 데 도움이 되기를 바란다.

## 참고

[^1]: https://secondboyet.com/Articles/LockFreeLimitedPriorityQ.html

[^2]: https://github.com/jonatanlinden/PR

[^3]: https://stackoverflow.com/a/8575182

[^4]: https://www.codeproject.com/Articles/1222893/Awaitable-Concurrent-Priority-Queue

[^5]: https://www.microsoft.com/en-us/research/wp-content/uploads/2006/04/2006-flops.pdf

[^6]: https://gist.github.com/khenidak/49cf6f5ac76b608c9e3b3fc86c86cec0

[^7]: https://www.csharp411.com/how-to-use-a-priority-queue-in-net-version-6/

[^8]: https://ws-doc.vercel.app/blog/deep_dive_csharp_queue_characteristic

[^9]: https://herbsutter.com/2008/08/05/effective-concurrency-lock-free-code-a-false-sense-of-security/

[^10]: https://www.cs.columbia.edu/~junfeng/papers/xinhao-plos15.pdf

[^11]: https://github.com/DNedic/lockfree

[^12]: https://github.com/SofiaGodovykh/Lock-free-priority-queue

[^13]: https://harostudio.co.kr/c-lock-free-queue-concurrentqueue-쓰레드-안전-큐/

[^14]: https://stackoverflow.com/questions/550616/lock-free-stack-and-queue-in-c-sharp

[^15]: https://secondboyet.com/articles/lockfreequeue.html

[^16]: https://learn.microsoft.com/en-us/archive/msdn-magazine/2008/october/concurrency-hazards-solving-problems-in-your-multithreaded-code

[^17]: https://blog.naver.com/techshare/100189903647

[^18]: https://www.reddit.com/r/cpp/comments/16nios9/colud_you_recommend_me_a_fast_lock_free_queue/

[^19]: https://secondboyet.com/articles/lockfreestack.html

[^20]: https://www.codeproject.com/Articles/56369/Thread-safe-priority-queue-in-Csharp

