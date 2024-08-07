---
title: "[CSharp] C# 비동기 프로그래밍 async/await"
categories: CSharp
tags:
- async
- await
- CSharp
- programming
- I/O
- CPU
- Task
- asynchronous
- performance
- .NET
header:
teaser: /assets/images/2024/whenany-async-breakfast.png
---

비동기 프로그래밍은 현대 소프트웨어 개발에서 필수적인 기술로 자리 잡고 있습니다. 특히 I/O 바인딩된 작업이나 CPU 바인딩된 작업을 효율적으로 처리하기 위해 비동기 프로그래밍을 활용하는 것이 중요합니다. C#에서는 `async`와 `await` 키워드를 통해 비동기 코드를 쉽게 작성할 수 있는 언어 수준의 비동기 프로그래밍 모델을 제공합니다. 이 모델은 작업 기반 비동기 패턴(TAP)을 따르며, 비동기 작업을 모델링하는 `Task` 및 `Task<T>` 객체를 사용하여 비동기 작업을 수행합니다. 비동기 프로그래밍의 핵심은 UI 스레드를 차단하지 않고도 비동기 작업을 수행할 수 있다는 점입니다. 예를 들어, 웹 서비스에서 데이터를 다운로드하거나 게임에서 복잡한 계산을 수행할 때 비동기 프로그래밍을 통해 UI가 매끄럽게 작동하도록 할 수 있습니다. 이 문서에서는 비동기 프로그래밍의 기본 개념과 C#에서의 구현 방법, 그리고 비동기 프로그래밍을 사용할 때의 주의사항에 대해 설명합니다. 비동기 프로그래밍을 통해 더 나은 사용자 경험을 제공하고, 애플리케이션의 성능을 향상시킬 수 있는 방법을 알아보세요.


|![](/assets/images/2024/whenany-async-breakfast.png)|
|:---:|
||


<!--
##### Outline #####
-->

<!--
---
## 비동기 프로그래밍 시나리오
**비동기 프로그래밍의 필요성**  
**비동기 프로그래밍의 장점**  
**C#의 비동기 프로그래밍 모델**  
**TAP(작업 기반 비동기 패턴) 소개**  

## 비동기 모델 개요
**비동기 작업의 기본 개념**  
**Task 및 Task<T> 개체의 역할**  
**async 및 await 키워드의 사용**  
**I/O 바인딩 및 CPU 바인딩 코드의 차이**  

## Practical Examples
**I/O 바인딩된 예제: 웹 서비스에서 데이터 다운로드**  
**CPU 바인딩 예제: 게임에 대한 계산 수행**  
**백그라운드에서 수행되는 작업의 이해**  

## 이해해야 할 주요 부분
**비동기 코드의 사용 시나리오**  
**async 및 await의 작동 방식**  
**비동기 메서드의 작성 규칙**  
**비동기 메서드의 예외 처리**  

## CPU 바인딩된 작업 및 I/O 바인딩된 작업 인식
**I/O 바인딩 작업의 식별 방법**  
**CPU 바인딩 작업의 식별 방법**  
**비동기 프로그래밍에서의 성능 고려사항**  

## 추가 예
**HTML 다운로드 및 문자열 검색 예제**  
**여러 작업이 완료될 때까지 대기하는 방법**  
**LINQ를 사용한 비동기 작업 처리**  

## 중요한 정보 및 조언
**비동기 메서드 작성 시 유의사항**  
**비차단 방식으로 작업을 기다리는 코드 작성**  
**ValueTask 사용의 장점**  
**ConfigureAwait의 사용 시기**  

## 전체 예제
**비동기 프로그래밍의 전체 코드 예제**  
**예제 코드의 설명 및 실행 결과**  

## 결론
**비동기 프로그래밍의 중요성 요약**  
**C#에서 비동기 프로그래밍을 활용하는 방법**  
**비동기 프로그래밍의 미래와 발전 방향**  

## 다른 리소스
**비동기 프로그래밍 관련 자료 링크**  
**C# 비동기 프로그래밍에 대한 추가 학습 자료**  
**비동기 프로그래밍의 최신 동향 및 기술**  
---
-->

## 비동기 프로그래밍 시나리오

비동기 프로그래밍은 현대 소프트웨어 개발에서 매우 중요한 개념입니다. 특히, 사용자 인터페이스(UI)가 있는 애플리케이션이나 서버 애플리케이션에서 비동기 프로그래밍은 필수적입니다. 이 섹션에서는 비동기 프로그래밍의 필요성과 장점, C#의 비동기 프로그래밍 모델, 그리고 TAP(작업 기반 비동기 패턴)에 대해 자세히 살펴보겠습니다.

**비동기 프로그래밍의 필요성**  

비동기 프로그래밍은 주로 I/O 작업이 많은 애플리케이션에서 필요합니다. 예를 들어, 웹 애플리케이션에서 데이터베이스에 접근하거나 외부 API로부터 데이터를 가져오는 경우, 이러한 작업이 완료될 때까지 애플리케이션이 멈추지 않도록 하기 위해 비동기 프로그래밍이 필요합니다. 비동기 프로그래밍을 사용하면, 사용자는 애플리케이션이 응답하지 않는 상황을 피할 수 있습니다.

**비동기 프로그래밍의 장점**  

비동기 프로그래밍의 주요 장점은 다음과 같습니다:
- **응답성 향상**: 비동기 작업을 통해 UI 스레드가 차단되지 않으므로, 사용자 경험이 향상됩니다.
- **리소스 효율성**: 비동기 작업은 CPU와 I/O 리소스를 보다 효율적으로 사용할 수 있게 해줍니다.
- **확장성**: 서버 애플리케이션에서 비동기 프로그래밍을 사용하면, 더 많은 클라이언트 요청을 처리할 수 있습니다.

**C#의 비동기 프로그래밍 모델**  

C#에서는 비동기 프로그래밍을 위해 `async`와 `await` 키워드를 사용합니다. 이 키워드들은 비동기 메서드를 정의하고 호출하는 데 사용됩니다. 비동기 메서드는 `Task` 또는 `Task<T>`를 반환하며, 이는 비동기 작업의 완료를 나타냅니다. 이러한 모델은 비동기 프로그래밍을 보다 직관적으로 만들어 줍니다.

**TAP(작업 기반 비동기 패턴) 소개**  

TAP는 C#에서 비동기 프로그래밍을 위한 표준 패턴입니다. TAP는 비동기 작업을 `Task` 객체로 표현하며, 이는 비동기 작업의 완료를 나타내는 데 사용됩니다. TAP를 사용하면 비동기 메서드를 쉽게 작성하고, 예외 처리를 간편하게 할 수 있습니다. 다음은 TAP를 사용하는 간단한 예제입니다:

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://api.github.com";
        string result = await DownloadStringAsync(url);
        Console.WriteLine(result);
    }

    static async Task<string> DownloadStringAsync(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.UserAgent.TryParseAdd("request");
            return await client.GetStringAsync(url);
        }
    }
}
```

위의 예제에서 `DownloadStringAsync` 메서드는 비동기적으로 웹 페이지의 내용을 다운로드합니다. `await` 키워드를 사용하여 비동기 작업이 완료될 때까지 기다리며, 이 동안 UI 스레드는 차단되지 않습니다.

이와 같이 비동기 프로그래밍은 현대 애플리케이션에서 필수적인 요소이며, C#에서는 TAP를 통해 이를 쉽게 구현할 수 있습니다. 다음 섹션에서는 비동기 모델의 개요에 대해 더 자세히 알아보겠습니다.

## 비동기 모델 개요

비동기 프로그래밍은 현대 소프트웨어 개발에서 매우 중요한 개념입니다. 특히, 사용자 인터페이스(UI)가 있는 애플리케이션이나 서버 애플리케이션에서 비동기 프로그래밍을 통해 성능을 극대화할 수 있습니다. 이 섹션에서는 비동기 작업의 기본 개념, C#에서의 Task 및 Task<T> 개체의 역할, async 및 await 키워드의 사용법, 그리고 I/O 바인딩과 CPU 바인딩 코드의 차이에 대해 설명하겠습니다.

**비동기 작업의 기본 개념**  

비동기 작업은 프로그램의 흐름을 차단하지 않고 동시에 여러 작업을 수행할 수 있게 해줍니다. 예를 들어, 웹 애플리케이션에서 사용자가 버튼을 클릭했을 때, 서버에 요청을 보내고 응답을 기다리는 동안 UI가 멈추지 않도록 할 수 있습니다. 비동기 작업은 일반적으로 I/O 작업(파일 읽기/쓰기, 네트워크 요청 등)에서 많이 사용됩니다.

**Task 및 Task<T> 개체의 역할**  

C#에서 비동기 작업을 수행하기 위해 주로 사용하는 개체는 `Task`와 `Task<T>`입니다. `Task`는 비동기 작업의 결과를 나타내며, `Task<T>`는 특정 타입의 결과를 반환하는 비동기 작업을 나타냅니다. 예를 들어, 다음과 같은 코드로 비동기 작업을 정의할 수 있습니다:

```csharp
public async Task<string> DownloadDataAsync(string url)
{
    using (HttpClient client = new HttpClient())
    {
        string result = await client.GetStringAsync(url);
        return result;
    }
}
```

**async 및 await 키워드의 사용**  

`async`와 `await` 키워드는 비동기 메서드를 정의하고 호출하는 데 사용됩니다. `async` 키워드는 메서드의 정의에 추가되어 해당 메서드가 비동기적으로 실행될 수 있음을 나타냅니다. `await` 키워드는 비동기 작업이 완료될 때까지 기다리도록 지시합니다. 위의 예제에서 `await`는 `GetStringAsync` 메서드가 완료될 때까지 기다리게 합니다.

**I/O 바인딩 및 CPU 바인딩 코드의 차이**  

I/O 바인딩 작업은 주로 외부 리소스(예: 파일 시스템, 네트워크 등)와의 상호작용을 포함하며, 이러한 작업은 대기 시간이 길 수 있습니다. 반면, CPU 바인딩 작업은 CPU의 계산 능력을 많이 소모하는 작업으로, 일반적으로 비동기 프로그래밍의 이점을 덜 받습니다. 예를 들어, 대량의 데이터 처리나 복잡한 계산을 수행하는 경우 CPU 바인딩 작업이 됩니다. 비동기 프로그래밍은 주로 I/O 바인딩 작업에서 성능을 향상시키는 데 유용합니다.

이러한 비동기 모델의 이해는 C#에서 비동기 프로그래밍을 효과적으로 활용하는 데 필수적입니다. 다음 섹션에서는 비동기 프로그래밍의 실제 예제를 통해 이론을 더욱 구체화하겠습니다.

## Practical Examples

**I/O 바인딩된 예제: 웹 서비스에서 데이터 다운로드** 

I/O 바인딩 작업은 주로 네트워크 요청이나 파일 시스템 접근과 같은 외부 자원에 의존하는 작업입니다. 이러한 작업은 대기 시간이 길어질 수 있으므로 비동기 프로그래밍을 통해 효율적으로 처리할 수 있습니다. 아래는 C#에서 웹 서비스를 통해 데이터를 비동기적으로 다운로드하는 예제입니다.

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://jsonplaceholder.typicode.com/posts";
        string result = await DownloadDataAsync(url);
        Console.WriteLine(result);
    }

    static async Task<string> DownloadDataAsync(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            HttpResponseMessage response = await client.GetAsync(url);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
    }
}
```

위의 코드에서 `DownloadDataAsync` 메서드는 주어진 URL에서 데이터를 비동기적으로 다운로드합니다. `HttpClient`를 사용하여 GET 요청을 보내고, 응답을 기다리는 동안 다른 작업을 수행할 수 있습니다.

---

**CPU 바인딩 예제: 게임에 대한 계산 수행**  

CPU 바인딩 작업은 주로 계산이 많이 필요한 작업으로, CPU의 성능에 따라 실행 시간이 달라집니다. 이러한 작업은 비동기적으로 처리하기보다는 병렬 처리를 통해 성능을 향상시킬 수 있습니다. 아래는 C#에서 CPU 바인딩 작업을 비동기적으로 수행하는 예제입니다.

```csharp
using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        int number = 100000000;
        long result = await Task.Run(() => CalculateFactorial(number));
        Console.WriteLine($"Factorial of {number} is {result}");
    }

    static long CalculateFactorial(int n)
    {
        if (n == 0) return 1;
        long result = 1;
        for (int i = 1; i <= n; i++)
        {
            result *= i;
        }
        return result;
    }
}
```

위의 코드에서 `CalculateFactorial` 메서드는 주어진 숫자의 팩토리얼을 계산합니다. `Task.Run`을 사용하여 이 작업을 비동기적으로 실행하고, 메인 스레드는 다른 작업을 수행할 수 있습니다.

---

**백그라운드에서 수행되는 작업의 이해** 

비동기 프로그래밍의 또 다른 중요한 측면은 백그라운드에서 작업을 수행하는 것입니다. 이는 사용자 인터페이스(UI)가 응답성을 유지하면서 긴 작업을 처리할 수 있도록 합니다. 아래는 C#에서 백그라운드 작업을 수행하는 예제입니다.

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        Console.WriteLine("백그라운드 작업 시작...");
        var cancellationTokenSource = new CancellationTokenSource();
        var token = cancellationTokenSource.Token;

        Task backgroundTask = Task.Run(() => LongRunningOperation(token), token);

        // 사용자가 작업을 취소할 수 있도록 대기
        Console.WriteLine("작업을 취소하려면 아무 키나 누르세요.");
        Console.ReadKey();
        cancellationTokenSource.Cancel();

        try
        {
            await backgroundTask;
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("작업이 취소되었습니다.");
        }
    }

    static void LongRunningOperation(CancellationToken token)
    {
        for (int i = 0; i < 10; i++)
        {
            token.ThrowIfCancellationRequested();
            Console.WriteLine($"작업 진행 중... {i + 1}");
            Thread.Sleep(1000); // 1초 대기
        }
    }
}
```

위의 코드에서 `LongRunningOperation` 메서드는 백그라운드에서 실행되며, 사용자가 작업을 취소할 수 있도록 `CancellationToken`을 사용합니다. 이로 인해 UI는 응답성을 유지하면서 긴 작업을 처리할 수 있습니다.

---

이와 같이 비동기 프로그래밍을 활용하면 I/O 바인딩 및 CPU 바인딩 작업을 효율적으로 처리할 수 있습니다. 각 예제는 비동기 프로그래밍의 장점을 잘 보여주며, 실제 애플리케이션에서 유용하게 사용될 수 있습니다.

## 이해해야 할 주요 부분

**비동기 코드의 사용 시나리오**  

비동기 프로그래밍은 주로 I/O 작업이 많은 애플리케이션에서 사용됩니다. 예를 들어, 웹 애플리케이션에서 데이터베이스에 접근하거나 외부 API로부터 데이터를 가져오는 경우, 비동기 코드를 사용하면 사용자 인터페이스(UI)가 멈추지 않고 원활하게 작동할 수 있습니다. 비동기 코드는 다음과 같은 시나리오에서 유용합니다:

- 웹 요청 처리
- 파일 입출력 작업
- 데이터베이스 쿼리 실행
- 대기 시간이 긴 작업(예: 이미지 처리)

**async 및 await의 작동 방식**  

`async`와 `await` 키워드는 C#에서 비동기 메서드를 작성할 때 사용됩니다. `async` 키워드는 메서드가 비동기적으로 실행될 것임을 나타내며, `await` 키워드는 비동기 작업이 완료될 때까지 기다리도록 지시합니다. 이 두 키워드를 사용하면 비동기 작업을 쉽게 작성하고 관리할 수 있습니다.

예를 들어, 다음과 같은 비동기 메서드를 작성할 수 있습니다:

```csharp
public async Task<string> DownloadDataAsync(string url)
{
    using (HttpClient client = new HttpClient())
    {
        string result = await client.GetStringAsync(url);
        return result;
    }
}
```

위의 코드에서 `DownloadDataAsync` 메서드는 주어진 URL에서 데이터를 비동기적으로 다운로드합니다. `await` 키워드를 사용하여 데이터 다운로드가 완료될 때까지 기다립니다.

**비동기 메서드의 작성 규칙**  

비동기 메서드를 작성할 때는 몇 가지 규칙을 따라야 합니다:

1. 메서드의 반환 타입은 `Task` 또는 `Task<T>`여야 합니다.
2. 메서드 이름은 일반적으로 `Async`로 끝나야 합니다. 예: `GetDataAsync`.
3. 메서드 내부에서 `await` 키워드를 사용하여 비동기 작업을 기다려야 합니다.

이러한 규칙을 따르면 코드의 가독성과 유지보수성이 향상됩니다.

**비동기 메서드의 예외 처리**  

비동기 메서드에서 발생하는 예외는 일반적인 동기 메서드와 유사하게 처리할 수 있습니다. `try-catch` 블록을 사용하여 예외를 처리할 수 있으며, `await` 키워드가 있는 메서드에서 발생한 예외는 호출하는 쪽으로 전파됩니다.

예를 들어:

```csharp
public async Task<string> GetDataWithErrorHandlingAsync(string url)
{
    try
    {
        using (HttpClient client = new HttpClient())
        {
            string result = await client.GetStringAsync(url);
            return result;
        }
    }
    catch (HttpRequestException e)
    {
        // 예외 처리 로직
        Console.WriteLine($"Request error: {e.Message}");
        return null;
    }
}
```

위의 코드에서 `HttpRequestException`이 발생할 경우, 예외를 잡아내어 적절한 처리를 할 수 있습니다. 비동기 메서드에서의 예외 처리는 동기 메서드와 동일하게 중요합니다.

이와 같이 비동기 프로그래밍의 주요 부분을 이해하고 활용하면, 더 나은 성능과 사용자 경험을 제공하는 애플리케이션을 개발할 수 있습니다.

## CPU 바인딩된 작업 및 I/O 바인딩된 작업 인식

비동기 프로그래밍을 이해하기 위해서는 CPU 바인딩 작업과 I/O 바인딩 작업을 구분하는 것이 중요합니다. 이 두 가지 작업 유형은 성능과 효율성에 큰 영향을 미치기 때문입니다. 아래에서는 각 작업의 식별 방법과 비동기 프로그래밍에서 고려해야 할 성능 요소에 대해 설명하겠습니다.

**I/O 바인딩 작업의 식별 방법** 

I/O 바인딩 작업은 주로 외부 장치와의 상호작용에 의존하는 작업입니다. 예를 들어, 파일 시스템에 접근하거나 네트워크를 통해 데이터를 전송하는 작업이 이에 해당합니다. 이러한 작업은 대개 다음과 같은 특징을 가집니다:

- **대기 시간**: I/O 작업은 외부 장치의 응답을 기다리는 시간이 길어질 수 있습니다. 예를 들어, 웹 서버에서 데이터를 다운로드할 때, 네트워크 지연으로 인해 작업이 완료되기까지 시간이 걸릴 수 있습니다.
- **비차단성**: I/O 바인딩 작업은 비동기적으로 처리할 수 있습니다. 즉, 작업이 진행되는 동안 다른 작업을 수행할 수 있습니다. C#에서는 `async`와 `await` 키워드를 사용하여 이러한 작업을 쉽게 처리할 수 있습니다.

**CPU 바인딩 작업의 식별 방법** 

CPU 바인딩 작업은 주로 CPU의 계산 능력에 의존하는 작업입니다. 이러한 작업은 대개 다음과 같은 특징을 가집니다:

- **계산 집약적**: CPU 바인딩 작업은 복잡한 계산을 수행하거나 대량의 데이터를 처리하는 데 많은 CPU 자원을 소모합니다. 예를 들어, 이미지 처리, 데이터 분석, 게임 로직 계산 등이 이에 해당합니다.
- **비동기 처리의 필요성**: CPU 바인딩 작업은 비동기적으로 처리하기 어려운 경우가 많습니다. 이러한 작업은 일반적으로 스레드를 차지하므로, 비동기 프로그래밍을 통해 다른 작업을 동시에 수행하기 어렵습니다.

**비동기 프로그래밍에서의 성능 고려사항**  

비동기 프로그래밍을 사용할 때는 성능을 최적화하기 위해 몇 가지 사항을 고려해야 합니다:

1. **작업 유형에 따른 선택**: I/O 바인딩 작업은 비동기적으로 처리하여 대기 시간을 최소화할 수 있지만, CPU 바인딩 작업은 스레드를 차지하므로 비동기 처리의 이점을 누리기 어렵습니다. 따라서 작업의 유형에 따라 적절한 접근 방식을 선택해야 합니다.

2. **스레드 풀 관리**: CPU 바인딩 작업이 많을 경우, 스레드 풀의 크기를 조정하여 성능을 최적화할 수 있습니다. C#에서는 `ThreadPool.SetMinThreads` 메서드를 사용하여 최소 스레드 수를 설정할 수 있습니다.

3. **비동기 메서드의 사용**: I/O 바인딩 작업을 비동기 메서드로 작성하여, 대기 시간 동안 다른 작업을 수행할 수 있도록 해야 합니다. 예를 들어, 다음과 같은 코드로 비동기 메서드를 작성할 수 있습니다:

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://example.com";
        string content = await DownloadContentAsync(url);
        Console.WriteLine(content);
    }

    static async Task<string> DownloadContentAsync(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            return await client.GetStringAsync(url);
        }
    }
}
```

이 예제에서는 `HttpClient`를 사용하여 비동기적으로 웹 페이지의 내용을 다운로드합니다. 이와 같이 I/O 바인딩 작업을 비동기적으로 처리하면, 프로그램의 응답성을 높일 수 있습니다.

비동기 프로그래밍에서 CPU 바인딩 작업과 I/O 바인딩 작업을 올바르게 인식하고 처리하는 것은 성능 최적화의 핵심입니다. 이를 통해 더 나은 사용자 경험을 제공할 수 있습니다.

## 추가 예

**HTML 다운로드 및 문자열 검색 예제**  

비동기 프로그래밍을 활용하여 웹에서 HTML을 다운로드하고 특정 문자열을 검색하는 예제를 살펴보겠습니다. 이 예제에서는 `HttpClient`를 사용하여 웹 페이지의 내용을 비동기적으로 가져오고, 가져온 내용에서 특정 문자열이 포함되어 있는지 확인합니다.

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://example.com"; // 다운로드할 URL
        string searchString = "Example Domain"; // 검색할 문자열

        string htmlContent = await DownloadHtmlAsync(url);
        bool containsString = htmlContent.Contains(searchString);

        Console.WriteLine($"HTML 다운로드 완료. '{searchString}' 포함 여부: {containsString}");
    }

    static async Task<string> DownloadHtmlAsync(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            return await client.GetStringAsync(url);
        }
    }
}
```

이 코드는 `DownloadHtmlAsync` 메서드를 통해 지정된 URL에서 HTML 콘텐츠를 비동기적으로 다운로드합니다. 다운로드가 완료되면, 해당 콘텐츠에서 특정 문자열이 포함되어 있는지 확인합니다.

---

**여러 작업이 완료될 때까지 대기하는 방법**  

비동기 프로그래밍에서는 여러 작업을 동시에 실행하고, 모든 작업이 완료될 때까지 대기할 수 있습니다. `Task.WhenAll` 메서드를 사용하여 여러 비동기 작업을 동시에 실행하고, 모든 작업이 완료될 때까지 기다리는 방법을 살펴보겠습니다.

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string[] urls = { "https://example.com", "https://example.org", "https://example.net" };
        Task<string>[] downloadTasks = new Task<string>[urls.Length];

        for (int i = 0; i < urls.Length; i++)
        {
            downloadTasks[i] = DownloadHtmlAsync(urls[i]);
        }

        string[] results = await Task.WhenAll(downloadTasks);

        foreach (var result in results)
        {
            Console.WriteLine($"HTML 다운로드 완료: {result.Substring(0, 50)}..."); // 첫 50자 출력
        }
    }

    static async Task<string> DownloadHtmlAsync(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            return await client.GetStringAsync(url);
        }
    }
}
```

위의 예제에서는 여러 URL에서 HTML을 비동기적으로 다운로드하고, 모든 다운로드가 완료될 때까지 기다립니다. `Task.WhenAll`을 사용하여 모든 작업이 완료된 후 결과를 출력합니다.

---

**LINQ를 사용한 비동기 작업 처리**  

LINQ를 사용하여 비동기 작업을 처리하는 방법도 있습니다. 예를 들어, 여러 URL에서 HTML을 다운로드한 후, 각 HTML에서 특정 문자열을 검색하는 작업을 비동기적으로 수행할 수 있습니다.

```csharp
using System;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string[] urls = { "https://example.com", "https://example.org", "https://example.net" };
        string searchString = "Example";

        var results = await Task.WhenAll(urls.Select(url => SearchInHtmlAsync(url, searchString)));

        foreach (var result in results)
        {
            Console.WriteLine(result);
        }
    }

    static async Task<string> SearchInHtmlAsync(string url, string searchString)
    {
        string htmlContent = await DownloadHtmlAsync(url);
        bool containsString = htmlContent.Contains(searchString);
        return $"{url}: '{searchString}' 포함 여부: {containsString}";
    }

    static async Task<string> DownloadHtmlAsync(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            return await client.GetStringAsync(url);
        }
    }
}
```

이 예제에서는 LINQ의 `Select` 메서드를 사용하여 각 URL에 대해 비동기적으로 HTML을 다운로드하고, 특정 문자열이 포함되어 있는지 확인합니다. 결과는 비동기적으로 수집되어 출력됩니다.

---

이와 같이 비동기 프로그래밍을 활용하면 여러 작업을 동시에 처리하고, 효율적으로 결과를 얻을 수 있습니다. 비동기 프로그래밍의 장점을 잘 활용하여 성능을 극대화할 수 있습니다.

## 중요한 정보 및 조언

**비동기 메서드 작성 시 유의사항**  
비동기 메서드를 작성할 때는 몇 가지 중요한 사항을 고려해야 합니다. 첫째, 비동기 메서드는 항상 `async` 키워드로 시작해야 하며, 반환 타입은 `Task` 또는 `Task<T>`여야 합니다. 둘째, 비동기 메서드 내에서 `await` 키워드를 사용하여 비동기 작업이 완료될 때까지 기다릴 수 있습니다. 이때, `await`는 메서드의 실행을 일시 중지하고, 다른 작업이 실행될 수 있도록 합니다. 셋째, 비동기 메서드에서 예외 처리를 적절히 수행해야 합니다. 비동기 메서드 내에서 발생한 예외는 호출한 메서드로 전파되므로, `try-catch` 블록을 사용하여 예외를 처리하는 것이 좋습니다.

**비차단 방식으로 작업을 기다리는 코드 작성**  
비동기 프로그래밍의 핵심은 비차단 방식으로 작업을 기다리는 것입니다. 이를 위해 `await` 키워드를 사용하여 비동기 작업이 완료될 때까지 기다릴 수 있습니다. 예를 들어, 다음과 같은 코드를 작성할 수 있습니다:

```csharp
public async Task<string> DownloadDataAsync(string url)
{
    using (HttpClient client = new HttpClient())
    {
        // 비동기적으로 데이터 다운로드
        string result = await client.GetStringAsync(url);
        return result;
    }
}
```

위의 코드에서 `GetStringAsync` 메서드는 비동기적으로 데이터를 다운로드하며, `await` 키워드를 사용하여 다운로드가 완료될 때까지 기다립니다. 이 방식은 UI 스레드를 차단하지 않으므로 사용자 경험을 향상시킵니다.

**ValueTask 사용의 장점**  
`ValueTask`는 비동기 메서드의 성능을 개선할 수 있는 유용한 구조체입니다. 일반적으로 `Task`는 힙에 할당되지만, `ValueTask`는 스택에 할당될 수 있어 메모리 할당을 줄일 수 있습니다. 특히, 비동기 메서드가 자주 호출되거나 결과가 즉시 반환될 가능성이 높은 경우 `ValueTask`를 사용하는 것이 좋습니다. 다음은 `ValueTask`를 사용하는 예제입니다:

```csharp
public ValueTask<int> GetValueAsync()
{
    // 즉시 값을 반환하는 경우
    return new ValueTask<int>(42);
}
```

이 예제에서 `GetValueAsync` 메서드는 즉시 값을 반환하므로, `ValueTask`를 사용하여 메모리 할당을 최소화합니다.

**ConfigureAwait의 사용 시기**  
`ConfigureAwait` 메서드는 비동기 작업이 완료된 후 어떤 컨텍스트에서 계속 실행될지를 지정하는 데 사용됩니다. 기본적으로 `await`는 호출한 스레드의 컨텍스트를 유지하지만, UI 애플리케이션에서는 UI 스레드에서 실행되어야 하는 경우가 많습니다. 그러나 백그라운드 작업에서는 UI 컨텍스트가 필요하지 않을 수 있습니다. 이때 `ConfigureAwait(false)`를 사용하여 성능을 개선할 수 있습니다. 예를 들어:

```csharp
public async Task DoWorkAsync()
{
    await Task.Delay(1000).ConfigureAwait(false);
    // UI 컨텍스트가 필요하지 않은 작업 수행
}
```

위의 코드에서 `ConfigureAwait(false)`를 사용하면, 비동기 작업이 완료된 후 UI 스레드가 아닌 다른 스레드에서 계속 실행됩니다. 이는 성능을 향상시키고, 데드락을 방지하는 데 도움이 됩니다.

이와 같은 유의사항과 조언을 통해 비동기 프로그래밍을 보다 효과적으로 활용할 수 있습니다. 비동기 메서드를 작성할 때는 항상 성능과 사용자 경험을 고려하여 최적의 코드를 작성하는 것이 중요합니다.

## 전체 예제

**비동기 프로그래밍의 전체 코드 예제**  
비동기 프로그래밍을 이해하기 위해, 간단한 예제를 통해 비동기 메서드를 작성하고 실행해보겠습니다. 이 예제에서는 웹에서 데이터를 비동기적으로 다운로드하고, 다운로드한 데이터를 처리하는 과정을 보여줍니다.

아래는 Python과 C#에서 비동기 프로그래밍을 구현한 예제 코드입니다.

### Python 예제

```python
import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    url = 'https://jsonplaceholder.typicode.com/posts'
    data = await fetch_data(url)
    print(data)

# 비동기 메인 함수 실행
if __name__ == '__main__':
    asyncio.run(main())
```

위의 Python 코드는 `aiohttp` 라이브러리를 사용하여 비동기적으로 웹에서 데이터를 다운로드합니다. `fetch_data` 함수는 주어진 URL에서 데이터를 가져오고, `main` 함수는 이 데이터를 출력합니다.

### C# 예제

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task<string> FetchData(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            return await client.GetStringAsync(url);
        }
    }

    static async Task Main(string[] args)
    {
        string url = "https://jsonplaceholder.typicode.com/posts";
        string data = await FetchData(url);
        Console.WriteLine(data);
    }
}
```

C# 예제에서는 `HttpClient`를 사용하여 비동기적으로 데이터를 다운로드합니다. `FetchData` 메서드는 URL에서 데이터를 가져오고, `Main` 메서드는 이 데이터를 출력합니다.

**예제 코드의 설명 및 실행 결과**  
위의 두 예제 모두 비동기 프로그래밍의 기본 개념을 보여줍니다. `async`와 `await` 키워드를 사용하여 비동기 작업을 수행하고, 메인 스레드를 차단하지 않고도 데이터를 다운로드할 수 있습니다. 

실행 결과로는 JSON 형식의 데이터가 출력됩니다. 이 데이터는 웹 서비스에서 제공하는 게시물 목록으로, 비동기적으로 다운로드된 결과입니다. 

이러한 비동기 프로그래밍 기법을 사용하면, I/O 작업이 완료될 때까지 기다리는 동안 다른 작업을 수행할 수 있어 애플리케이션의 성능을 향상시킬 수 있습니다.

## 결론

**비동기 프로그래밍의 중요성 요약**  
비동기 프로그래밍은 현대 소프트웨어 개발에서 필수적인 기술로 자리 잡았습니다. 특히, 사용자 인터페이스(UI)가 있는 애플리케이션에서는 비동기 프로그래밍을 통해 사용자 경험을 향상시킬 수 있습니다. 비동기 프로그래밍을 사용하면 애플리케이션이 긴 작업을 수행하는 동안에도 사용자와의 상호작용을 유지할 수 있습니다. 이는 특히 네트워크 요청, 파일 입출력, 데이터베이스 쿼리와 같은 I/O 바인딩 작업에서 더욱 중요합니다. 비동기 프로그래밍을 통해 애플리케이션의 응답성을 높이고, 자원을 효율적으로 사용할 수 있습니다.

**C#에서 비동기 프로그래밍을 활용하는 방법**  
C#에서는 `async`와 `await` 키워드를 사용하여 비동기 프로그래밍을 쉽게 구현할 수 있습니다. `async` 키워드는 메서드가 비동기적으로 실행될 수 있음을 나타내며, `await` 키워드는 비동기 작업이 완료될 때까지 기다리도록 지시합니다. 다음은 C#에서 비동기 메서드를 작성하는 간단한 예제입니다.

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        string url = "https://api.github.com";
        string result = await DownloadDataAsync(url);
        Console.WriteLine(result);
    }

    static async Task<string> DownloadDataAsync(string url)
    {
        using (HttpClient client = new HttpClient())
        {
            client.DefaultRequestHeaders.UserAgent.TryParseAdd("request");
            return await client.GetStringAsync(url);
        }
    }
}
```

위의 예제에서 `DownloadDataAsync` 메서드는 비동기적으로 웹 페이지의 데이터를 다운로드합니다. `await` 키워드를 사용하여 데이터가 다운로드될 때까지 기다리며, 이 동안 다른 작업을 수행할 수 있습니다.

**비동기 프로그래밍의 미래와 발전 방향**  
비동기 프로그래밍은 앞으로도 계속 발전할 것입니다. 특히, 클라우드 컴퓨팅과 마이크로서비스 아키텍처의 발전으로 인해 비동기 프로그래밍의 필요성이 더욱 커질 것입니다. 또한, 새로운 언어 기능과 라이브러리가 지속적으로 개발되고 있어 비동기 프로그래밍이 더욱 직관적이고 효율적으로 이루어질 것입니다. 예를 들어, C# 9.0에서는 `init` 접근자를 통해 비동기 프로그래밍의 패턴을 더욱 간소화할 수 있는 방법이 도입되었습니다.

결론적으로, 비동기 프로그래밍은 소프트웨어 개발에서 중요한 역할을 하며, C#과 같은 현대 프로그래밍 언어에서 이를 효과적으로 활용하는 방법을 배우는 것은 개발자에게 큰 이점이 될 것입니다. 비동기 프로그래밍의 발전 방향을 주의 깊게 살펴보며, 새로운 기술을 지속적으로 학습하는 것이 중요합니다.

## 다른 리소스

**비동기 프로그래밍 관련 자료 링크**  
비동기 프로그래밍에 대한 이해를 높이기 위해 다양한 자료를 참고하는 것이 중요합니다. 다음은 유용한 링크들입니다:

- [Microsoft Docs - Asynchronous Programming](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/async/)  
  이 문서는 C#에서 비동기 프로그래밍을 구현하는 방법에 대한 공식 문서입니다. `async` 및 `await` 키워드의 사용법과 비동기 메서드 작성에 대한 자세한 설명이 포함되어 있습니다.

- [Async/Await - Best Practices in C#](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/async/best-practices-in-asynchronous-programming)  
  비동기 프로그래밍을 할 때 유의해야 할 모범 사례를 정리한 문서입니다. 성능 최적화 및 코드 가독성을 높이는 방법에 대한 팁이 포함되어 있습니다.

- [C# Asynchronous Programming - YouTube](https://www.youtube.com/results?search_query=c%23+asynchronous+programming)  
  YouTube에서 제공하는 다양한 비동기 프로그래밍 관련 강의와 튜토리얼을 통해 시각적으로 학습할 수 있습니다.

**C# 비동기 프로그래밍에 대한 추가 학습 자료**  
비동기 프로그래밍을 더 깊이 이해하기 위해 다음과 같은 자료를 추천합니다:

- **책: "C# 9.0 in a Nutshell"**  
  이 책은 C#의 다양한 기능을 다루고 있으며, 비동기 프로그래밍에 대한 장도 포함되어 있습니다. 비동기 프로그래밍의 기초부터 고급 개념까지 폭넓게 다루고 있습니다.

- **온라인 강의: Pluralsight - Asynchronous Programming in C#**  
  Pluralsight에서 제공하는 이 강의는 비동기 프로그래밍의 기초부터 고급 개념까지 체계적으로 배울 수 있는 좋은 자료입니다.

- **블로그: "The Code Blogger"**  
  이 블로그에서는 비동기 프로그래밍에 대한 다양한 주제를 다루고 있으며, 실용적인 예제와 함께 설명하고 있습니다.

**비동기 프로그래밍의 최신 동향 및 기술**  
비동기 프로그래밍은 계속해서 발전하고 있으며, 최신 동향을 파악하는 것이 중요합니다. 다음은 현재 주목할 만한 기술과 트렌드입니다:

- **.NET 6의 새로운 비동기 기능**  
  .NET 6에서는 비동기 프로그래밍을 위한 새로운 기능과 개선 사항이 추가되었습니다. 특히, `ValueTask`와 같은 새로운 타입이 성능을 개선하는 데 도움을 줍니다.

- **Reactive Extensions (Rx)**  
  Rx는 비동기 데이터 스트림을 처리하기 위한 라이브러리로, 비동기 프로그래밍의 새로운 패러다임을 제공합니다. 이벤트 기반 프로그래밍을 더 쉽게 구현할 수 있도록 도와줍니다.

- **gRPC와 비동기 통신**  
  gRPC는 고성능의 원격 프로시저 호출(RPC) 프레임워크로, 비동기 통신을 지원합니다. 이를 통해 클라이언트와 서버 간의 비동기 데이터 전송이 가능해집니다.

이러한 자료와 리소스를 통해 비동기 프로그래밍에 대한 이해를 높이고, C#에서의 비동기 프로그래밍을 더욱 효과적으로 활용할 수 있습니다.

<!--
##### Reference #####
-->

## Reference


* [https://learn.microsoft.com/ko-kr/dotnet/csharp/asynchronous-programming/async-scenarios](https://learn.microsoft.com/ko-kr/dotnet/csharp/asynchronous-programming/async-scenarios)
* [https://learn.microsoft.com/ko-kr/dotnet/csharp/asynchronous-programming/](https://learn.microsoft.com/ko-kr/dotnet/csharp/asynchronous-programming/)
* [https://kangworld.tistory.com/25](https://kangworld.tistory.com/25)
* [https://www.csharpstudy.com/CSharp/CSharp-async-await.aspx](https://www.csharpstudy.com/CSharp/CSharp-async-await.aspx)


<!--
#  비동기 프로그래밍 시나리오

##  이 문서의 내용

I/O 바인딩된 요구 사항이 있는 경우(예: 네트워크에 데이터 요청, 데이터베이스 액세스 또는 파일 시스템 읽기 및 쓰기) 비동기
프로그래밍을 활용하는 것이 좋습니다. 부담이 큰 계산을 수행하는 것과 같이 CPU 바인딩된 코드가 있을 수도 있으며 이는 비동기 코드 작성의
좋은 시나리오이기도 합니다.

C#에는 콜백을 조작하거나 비동기를 지원하는 라이브러리를 따를 필요 없이 비동기 코드를 쉽게 작성할 수 있는 언어 수준 비동기 프로그래밍
모델이 있습니다. 이 모델은 [ TAP(작업 기반 비동기 패턴) ](../../standard/asynchronous-programming-
patterns/task-based-asynchronous-pattern-tap) 을 따릅니다.

##  비동기 모델 개요

비동기 프로그래밍의 핵심은 비동기 작업을 모델링하는 ` Task ` 및 ` Task<T> ` 개체입니다. 이러한 개체는 ` async ` 및
` await ` 키워드를 통해 지원됩니다. 대부분의 경우 모델은 매우 간단합니다.

  * I/O 바인딩된 코드에서는 ` async ` 메서드의 내부에서 ` Task ` 또는 ` Task<T> ` 를 반환하는 작업을 기다립니다. 
  * CPU 바인딩된 코드에서는 [ Task.Run ](/ko-kr/dotnet/api/system.threading.tasks.task.run) 메서드로 백그라운드 스레드에서 시작되는 작업을 기다립니다. 

` await ` 키워드가 마법이 일어나는 곳입니다. ` await ` 를 수행한 메서드의 호출자에게 제어를 넘기고, 궁극적으로 UI가
응답하거나 서비스가 탄력적일 수 있도록 합니다. ` async ` 및 ` await ` 외에 비동기 코드를 사용하는 [ 여러 방법
](../../standard/asynchronous-programming-patterns/task-based-asynchronous-
pattern-tap) 이 있지만, 이 문서에서는 언어 수준 구문을 집중적으로 설명합니다.

참고 항목

다음 예제에서 [ System.Net.Http.HttpClient ](/ko-
kr/dotnet/api/system.net.http.httpclient) 클래스는 웹 서비스에서 일부 데이터를 다운로드하는 데 사용됩니다.
이러한 예제에서 사용되는 ` s_httpClient ` 개체는 ` Program ` 클래스의 정적 필드입니다(전체 예제를 확인하세요).

` private static readonly HttpClient s_httpClient = new(); `

###  I/O 바인딩된 예제: 웹 서비스에서 데이터 다운로드

단추가 눌릴 때 웹 서비스에서 일부 데이터를 다운로드해야 할 수 있지만 UI 스레드를 차단하지 않으려고 합니다. 이 작업은 다음과 같이
구현할 수 있습니다.

    
    
    s_downloadButton.Clicked += async (o, e) =>
    {
        // This line will yield control to the UI as the request
        // from the web service is happening.
        //
        // The UI thread is now free to perform other work.
        var stringData = await s_httpClient.GetStringAsync(URL);
        DoSomethingWithData(stringData);
    };
    

이 코드는 ` Task ` 개체 조작 시 위험에 빠지지 않고 의도(데이터를 비동기식으로 다운로드)를 표현합니다.

###  CPU 바인딩 예제: 게임에 대한 계산 수행

단추를 누르면 화면의 많은 적에게 손상을 입힐 수 있는 모바일 게임을 작성한다고 가정합니다. 손상 계산을 수행하는 것은 부담이 클 수 있고
UI 스레드에서 이 작업을 수행하면 계산이 수행될 때 게임이 일시 중지되는 것처럼 보입니다.

이 작업을 처리하는 가장 좋은 방법은 ` Task.Run ` 을 사용하여 작업을 수행하는 백그라운드 스레드를 시작하고 ` await ` 를
사용하여 결과를 기다리는 것입니다. 이렇게 하면 작업이 수행되는 동안 UI가 매끄럽게 느껴질 수 있습니다.

    
    
    static DamageResult CalculateDamageDone()
    {
        return new DamageResult()
        {
            // Code omitted:
            //
            // Does an expensive calculation and returns
            // the result of that calculation.
        };
    }
    
    s_calculateButton.Clicked += async (o, e) =>
    {
        // This line will yield control to the UI while CalculateDamageDone()
        // performs its work. The UI thread is free to perform other work.
        var damageResult = await Task.Run(() => CalculateDamageDone());
        DisplayDamage(damageResult);
    };
    

이 코드는 단추 클릭 이벤트의 의도를 표현하고 백그라운드 스레드를 수동으로 관리할 필요가 없고 비차단 방식으로 작업을 수행합니다.

###  백그라운드에서 수행되는 작업

C#에서는 컴파일러가 해당 코드를, ` await ` 에 도달할 때 실행을 양도하고 백그라운드 작업이 완료될 때 실행을 다시 시작하는 것과
같은 작업을 추적하는 상태 시스템으로 변환합니다.

이론적으로 보면 이 변환은 [ 비동기 프라미스 모델
](https://en.wikipedia.org/wiki/Futures_and_promises) 입니다.

##  이해해야 할 주요 부분

  * 비동기 코드는 I/O 바인딩된 코드와 CPU 바인딩된 코드에 둘 다 사용할 수 있지만 시나리오마다 다르게 사용됩니다. 
  * 비동기 코드는 백그라운드에서 수행되는 작업을 모델링하는 데 사용되는 구문인 ` Task<T> ` 및 ` Task ` 를 사용합니다. 
  * ` async ` 키워드는 본문에서 ` await ` 키워드를 사용할 수 있는 비동기 메서드로 메서드를 변환합니다. 
  * ` await ` 키워드가 적용되면 이 키워드는 호출 메서드를 일시 중단하고 대기 작업이 완료할 때까지 제어 권한을 다시 호출자에게 양도합니다. 
  * ` await ` 는 비동기 메서드 내부에서만 사용할 수 있습니다. 

##  CPU 바인딩된 작업 및 I/O 바인딩된 작업 인식

이 가이드의 처음 두 예제에서는 I/O 바인딩된 작업과 CPU 바인딩된 작업에 ` async ` 및 ` await ` 를 사용하는 방법을
설명했습니다. 이 방법은 수행해야 하는 작업이 I/O 바인딩된 작업 또는 CPU 바인딩된 작업일 경우 이를 식별할 수 있는 키입니다. 이
방법이 코드 성능에 큰 영향을 미칠 수 있고 잠재적으로 특정 구문을 잘못 사용하게 될 수 있기 때문입니다.

다음은 코드를 작성하기 전에 질문해야 하는 두 가지 질문입니다.

  1. 코드가 데이터베이스의 데이터와 같은 무엇인가를 “기다리게” 되나요? 

대답이 "예"이면 **I/O 바인딩된** 작업입니다.

  2. 코드가 비용이 높은 계산을 수행하게 되나요? 

대답이 "예"이면 **CPU 바인딩된** 작업입니다.

**I/O 바인딩된** 작업이 있을 경우 ` Task.Run ` _없이_ ` async ` 및 ` await ` 를 사용합니다. 작업 병렬
라이브러리를 사용 _하면 안 됩니다_ .

**CPU 바인딩된** 작업이 있고 빠른 응답이 필요할 경우 ` async ` 및 ` await ` 를 사용하지만 ` Task.Run ` 을
__ 사용하여 또 다른 스레드에서 작업을 생성합니다. 작업이 동시성 및 병렬 처리에 해당할 경우 [ 작업 병렬 라이브러리
](../../standard/parallel-programming/task-parallel-library-tpl) 를 사용할 것을 고려할
수도 있습니다.

또한 항상 코드 실행을 측정해야 합니다. 예를 들어 CPU 바인딩된 작업이 다중 스레딩 시 컨텍스트 전환의 오버헤드에 비해 부담이 크지 않은
상황이 될 수 있습니다. 모든 선택에는 절충점이 있습니다. 상황에 맞는 올바른 절충점을 선택해야 합니다.

##  추가 예

다음 예제에서는 C#에서 비동기 코드를 작성할 수 있는 다양한 방법을 보여 줍니다. 예제에서는 발생할 수 있는 몇 가지 시나리오를 다룹니다.

이 코드 조각은 지정된 URL에서 HTML을 다운로드하고 HTML에서 문자열 ".NET"이 발생하는 횟수를 계산합니다. 이 작업을 수행하고
횟수를 반환하는 Web API 컨트롤러 메서드를 정의하기 위해 ASP.NET을 사용합니다.

참고 항목

프로덕션 코드에서 HTML 구문 분석을 수행하려는 경우 정규식을 사용하지 마세요. 대신 구문 분석 라이브러리를 사용하세요.

    
    
    [HttpGet, Route("DotNetCount")]
    static public async Task<int> GetDotNetCount(string URL)
    {
        // Suspends GetDotNetCount() to allow the caller (the web server)
        // to accept another request, rather than blocking on this one.
        var html = await s_httpClient.GetStringAsync(URL);
        return Regex.Matches(html, @"\.NET").Count;
    }
    

다음은 단추가 눌릴 때 같은 작업을 수행하는 유니버설 Windows 앱용으로 작성된 동일한 시나리오입니다.

    
    
    private readonly HttpClient _httpClient = new HttpClient();
    
    private async void OnSeeTheDotNetsButtonClick(object sender, RoutedEventArgs e)
    {
        // Capture the task handle here so we can await the background task later.
        var getDotNetFoundationHtmlTask = _httpClient.GetStringAsync("https://dotnetfoundation.org");
    
        // Any other work on the UI thread can be done here, such as enabling a Progress Bar.
        // This is important to do here, before the "await" call, so that the user
        // sees the progress bar before execution of this method is yielded.
        NetworkProgressBar.IsEnabled = true;
        NetworkProgressBar.Visibility = Visibility.Visible;
    
        // The await operator suspends OnSeeTheDotNetsButtonClick(), returning control to its caller.
        // This is what allows the app to be responsive and not block the UI thread.
        var html = await getDotNetFoundationHtmlTask;
        int count = Regex.Matches(html, @"\.NET").Count;
    
        DotNetCountLabel.Text = $"Number of .NETs on dotnetfoundation.org: {count}";
    
        NetworkProgressBar.IsEnabled = false;
        NetworkProgressBar.Visibility = Visibility.Collapsed;
    }
    

###  여러 작업이 완료될 때까지 대기

동시에 데이터의 여러 부분을 검색해야 하는 상황이 될 수 있습니다. ` Task ` API에는 여러 백그라운드 작업에서 비차단 대기를
수행하는 비동기 코드를 작성할 수 있는 [ Task.WhenAll ](/ko-
kr/dotnet/api/system.threading.tasks.task.whenall) 및 [ Task.WhenAny ](/ko-
kr/dotnet/api/system.threading.tasks.task.whenany) 메서드가 포함됩니다.

이 예제에서는 ` userId ` 집합에 대한 ` User ` 데이터를 확인하는 방법을 보여 줍니다.

    
    
    private static async Task<User> GetUserAsync(int userId)
    {
        // Code omitted:
        //
        // Given a user Id {userId}, retrieves a User object corresponding
        // to the entry in the database with {userId} as its Id.
    
        return await Task.FromResult(new User() { id = userId });
    }
    
    private static async Task<IEnumerable<User>> GetUsersAsync(IEnumerable<int> userIds)
    {
        var getUserTasks = new List<Task<User>>();
        foreach (int userId in userIds)
        {
            getUserTasks.Add(GetUserAsync(userId));
        }
    
        return await Task.WhenAll(getUserTasks);
    }
    

다음은 LINQ를 사용하여 이 코드를 보다 간결하게 작성하는 또 다른 방법입니다.

    
    
    private static async Task<User[]> GetUsersAsyncByLINQ(IEnumerable<int> userIds)
    {
        var getUserTasks = userIds.Select(id => GetUserAsync(id)).ToArray();
        return await Task.WhenAll(getUserTasks);
    }
    

코드 양은 더 적지만 LINQ를 비동기 코드와 함께 사용할 때는 주의하세요. LINQ는 연기된(지연) 실행을 사용하므로, `
.ToList() ` 또는 ` .ToArray() ` 호출을 반복하도록 생성된 시퀀스를 적용해야 비동기 호출이 ` foreach ` 루프에서
수행되면 즉시 비동기 호출이 발생합니다. 위의 예제에서는 [ Enumerable.ToArray ](/ko-
kr/dotnet/api/system.linq.enumerable.toarray) 을(를) 사용하여 쿼리를 열심히 수행하고 결과를 배열에
저장합니다. 코드 ` id => GetUserAsync(id) ` (은)는 강제로 실행되고 작업을 시작합니다.

##  중요한 정보 및 조언

비동기 프로그래밍을 사용하는 경우 예기치 않은 동작을 방지할 수 있는 몇 가지 세부 정보를 고려해야 합니다.

  * ` async ` **메서드에는 본문에** ` await ` **키워드가 있어야 합니다. 키워드가 없으면 일시 중단되지 않습니다.**

기억해야 할 중요한 정보입니다. ` await ` 가 ` async ` 메서드의 본문에서 사용되지 않으면 C# 컴파일러가 경고를 생성하지만
코드는 일반 메서드인 것처럼 컴파일 및 실행됩니다. 이는 C# 컴파일러가 비동기 메서드에 대해 생성한 상태 시스템이 아무것도 수행하지 않기
때문에 매우 비효율적입니다.

  * **작성하는 모든 비동기 메서드 이름의 접미사로 “Async”를 추가합니다.**

이 규칙을 .NET에서 사용하여 동기 및 비동기 메서드를 더 쉽게 구별할 수 있습니다. 코드에서 명시적으로 호출되지 않은 특정 메서드(예:
이벤트 처리기 또는 웹 컨트롤러 메서드)가 반드시 적용되는 것은 아닙니다. 이러한 메서드는 코드에서 명시적으로 호출되지 않으므로 명시적으로
명명하는 것은 별로 중요하지 않습니다.

  * ` async void ` 는 **이벤트 처리기에만 사용해야 합니다.**

이벤트에는 반환 형식이 없어서 ` Task ` 및 ` Task<T> ` 를 사용할 수 없으므로 비동기 이벤트 처리기가 작동하도록 허용하는
유일한 방법은 ` async void ` 입니다. ` async void ` 의 다른 사용은 TAP 모델을 따르지 않고 다음과 같이 사용이
어려울 수 있습니다.

    * ` async void ` 메서드에서 throw된 예외는 해당 메서드 외부에서 catch될 수 없습니다. 
    * ` async void ` 메서드는 테스트하기가 어렵습니다. 
    * 호출자가 ` async void ` 메서드를 비동기로 예상하지 않을 경우 이러한 메서드는 의도하지 않은 잘못된 결과를 일으킬 수 있습니다. 
  * **LINQ 식에서 비동기 람다를 사용할 경우 신중하게 스레드**

LINQ의 람다 식은 연기된 실행을 사용합니다. 즉, 예상치 않은 시점에 코드 실행이 끝날 수 있습니다. 이 코드에 차단 작업을 도입하면
코드가 제대로 작성되지 않은 경우 교착 상태가 쉽게 발생할 수 있습니다. 또한 이 코드처럼 비동기 코드를 중첩하면 코드 실행에 대해
추론하기가 훨씬 더 어려울 수도 있습니다. 비동기 및 LINQ는 강력하지만 가능한 한 신중하고 분명하게 함께 사용되어야 합니다.

  * **비차단 방식으로 작업을 기다리는 코드 작성**

` Task ` 가 완료될 때까지 대기하는 수단으로 현재 스레드를 차단하면 교착 상태가 발생하고 컨텍스트 스레드가 차단될 수 있고 더 복잡한
오류 처리가 필요할 수 있습니다. 다음 표에서는 비차단 방식으로 작업 대기를 처리하는 방법에 대한 지침을 제공합니다.

사용 기능...  |  대체 방법  |  수행할 작업   
---|---|---  
` await ` |  ` Task.Wait ` 또는 ` Task.Result ` |  백그라운드 작업의 결과 검색   
` await Task.WhenAny ` |  ` Task.WaitAny ` |  작업이 완료될 때까지 대기   
` await Task.WhenAll ` |  ` Task.WaitAll ` |  모든 작업이 완료될 때까지 대기   
` await Task.Delay ` |  ` Thread.Sleep ` |  일정 기간 대기   
  * **가능하면** ` ValueTask ` 를 **사용**

비동기 메서드에서 ` Task ` 개체를 반환하면 특정 경로에 성능 병목 현상이 발생할 수 있습니다. ` Task ` 는 참조 형식이므로
이를 사용하는 것은 개체 할당을 의미합니다. ` async ` 한정자로 선언된 메서드가 캐시된 결과를 반환하거나 동기적으로 완료된 경우
코드의 성능이 중요한 섹션에서 추가 할당에 상당한 시간이 소요될 수 있습니다. 연속 루프에서 이러한 할당이 발생하면 부담이 될 수 있습니다.
자세한 내용은 [ 일반화된 비동기 반환 형식 ](../language-reference/keywords/async#return-types)
을 참조하세요.

  * ` ConfigureAwait(false) ` 를 **사용**

일반적인 질문은 "언제 [ Task.ConfigureAwait(Boolean) ](/ko-
kr/dotnet/api/system.threading.tasks.task.configureawait#system-threading-
tasks-task-configureawait\(system-boolean\)) 메서드를 사용해야 하는가"입니다. 이 메서드를 사용하면 `
Task ` 인스턴스가 awaiter를 구성할 수 있습니다. 이는 중요한 고려 사항이며 잘못 설정할 경우 성능에 영향을 미칠 수 있고 심지어
교착 상태가 발생할 수도 있습니다. ` ConfigureAwait ` 에 대한 자세한 내용은 [ ConfigureAwait FAQ
](https://devblogs.microsoft.com/dotnet/configureawait-faq) 를 참조하세요.

  * **상태 저장 코드 작성 분량 감소**

전역 개체의 상태나 특정 메서드의 실행에 의존하지 마세요. 대신, 메서드의 반환 값에만 의존합니다. 이유는 무엇입니까?

    * 코드를 더 쉽게 추론할 수 있습니다. 
    * 코드를 더 쉽게 테스트할 수 있습니다. 
    * 비동기 및 동기 코드를 훨씬 더 쉽게 혼합할 수 있습니다. 
    * 일반적으로 함께 경합 상태를 피할 수 있습니다. 
    * 반환 값에 의존하면 비동기 코드를 간단히 조정할 수 있습니다. 
    * (이점) 이 방법은 실제로 종속성 주입에도 잘 작동합니다. 

권장되는 목적은 코드에서 완전하거나 거의 완전한 [ 참조 투명성
](https://en.wikipedia.org/wiki/Referential_transparency_%28computer_science%29)
을 달성하는 것입니다. 이렇게 하면 예측 가능하고 테스트 가능하고 유지 관리 가능한 코드베이스가 생성됩니다.

##  전체 예제

다음 코드는 예제에 관한 _Program.cs_ 파일의 전체 텍스트입니다.

    
    
    using System.Text.RegularExpressions;
    using System.Windows;
    using Microsoft.AspNetCore.Mvc;
    
    class Button
    {
        public Func<object, object, Task>? Clicked
        {
            get;
            internal set;
        }
    }
    
    class DamageResult
    {
        public int Damage
        {
            get { return 0; }
        }
    }
    
    class User
    {
        public bool isEnabled
        {
            get;
            set;
        }
    
        public int id
        {
            get;
            set;
        }
    }
    
    public class Program
    {
        private static readonly Button s_downloadButton = new();
        private static readonly Button s_calculateButton = new();
    
        private static readonly HttpClient s_httpClient = new();
    
        private static readonly IEnumerable<string> s_urlList = new string[]
        {
                "https://learn.microsoft.com",
                "https://learn.microsoft.com/aspnet/core",
                "https://learn.microsoft.com/azure",
                "https://learn.microsoft.com/azure/devops",
                "https://learn.microsoft.com/dotnet",
                "https://learn.microsoft.com/dotnet/desktop/wpf/get-started/create-app-visual-studio",
                "https://learn.microsoft.com/education",
                "https://learn.microsoft.com/shows/net-core-101/what-is-net",
                "https://learn.microsoft.com/enterprise-mobility-security",
                "https://learn.microsoft.com/gaming",
                "https://learn.microsoft.com/graph",
                "https://learn.microsoft.com/microsoft-365",
                "https://learn.microsoft.com/office",
                "https://learn.microsoft.com/powershell",
                "https://learn.microsoft.com/sql",
                "https://learn.microsoft.com/surface",
                "https://dotnetfoundation.org",
                "https://learn.microsoft.com/visualstudio",
                "https://learn.microsoft.com/windows",
                "https://learn.microsoft.com/maui"
        };
    
        private static void Calculate()
        {
            // <PerformGameCalculation>
            static DamageResult CalculateDamageDone()
            {
                return new DamageResult()
                {
                    // Code omitted:
                    //
                    // Does an expensive calculation and returns
                    // the result of that calculation.
                };
            }
    
            s_calculateButton.Clicked += async (o, e) =>
            {
                // This line will yield control to the UI while CalculateDamageDone()
                // performs its work. The UI thread is free to perform other work.
                var damageResult = await Task.Run(() => CalculateDamageDone());
                DisplayDamage(damageResult);
            };
            // </PerformGameCalculation>
        }
    
        private static void DisplayDamage(DamageResult damage)
        {
            Console.WriteLine(damage.Damage);
        }
    
        private static void Download(string URL)
        {
            // <UnblockingDownload>
            s_downloadButton.Clicked += async (o, e) =>
            {
                // This line will yield control to the UI as the request
                // from the web service is happening.
                //
                // The UI thread is now free to perform other work.
                var stringData = await s_httpClient.GetStringAsync(URL);
                DoSomethingWithData(stringData);
            };
            // </UnblockingDownload>
        }
    
        private static void DoSomethingWithData(object stringData)
        {
            Console.WriteLine("Displaying data: ", stringData);
        }
    
        // <GetUsersForDataset>
        private static async Task<User> GetUserAsync(int userId)
        {
            // Code omitted:
            //
            // Given a user Id {userId}, retrieves a User object corresponding
            // to the entry in the database with {userId} as its Id.
    
            return await Task.FromResult(new User() { id = userId });
        }
    
        private static async Task<IEnumerable<User>> GetUsersAsync(IEnumerable<int> userIds)
        {
            var getUserTasks = new List<Task<User>>();
            foreach (int userId in userIds)
            {
                getUserTasks.Add(GetUserAsync(userId));
            }
    
            return await Task.WhenAll(getUserTasks);
        }
        // </GetUsersForDataset>
    
        // <GetUsersForDatasetByLINQ>
        private static async Task<User[]> GetUsersAsyncByLINQ(IEnumerable<int> userIds)
        {
            var getUserTasks = userIds.Select(id => GetUserAsync(id)).ToArray();
            return await Task.WhenAll(getUserTasks);
        }
        // </GetUsersForDatasetByLINQ>
    
        // <ExtractDataFromNetwork>
        [HttpGet, Route("DotNetCount")]
        static public async Task<int> GetDotNetCount(string URL)
        {
            // Suspends GetDotNetCount() to allow the caller (the web server)
            // to accept another request, rather than blocking on this one.
            var html = await s_httpClient.GetStringAsync(URL);
            return Regex.Matches(html, @"\.NET").Count;
        }
        // </ExtractDataFromNetwork>
    
        static async Task Main()
        {
            Console.WriteLine("Application started.");
    
            Console.WriteLine("Counting '.NET' phrase in websites...");
            int total = 0;
            foreach (string url in s_urlList)
            {
                var result = await GetDotNetCount(url);
                Console.WriteLine($"{url}: {result}");
                total += result;
            }
            Console.WriteLine("Total: " + total);
    
            Console.WriteLine("Retrieving User objects with list of IDs...");
            IEnumerable<int> ids = new int[] { 1, 2, 3, 4, 5, 6, 7, 8, 9, 0 };
            var users = await GetUsersAsync(ids);
            foreach (User? user in users)
            {
                Console.WriteLine($"{user.id}: isEnabled={user.isEnabled}");
            }
    
            Console.WriteLine("Application ending.");
        }
    }
    
    // Example output:
    //
    // Application started.
    // Counting '.NET' phrase in websites...
    // https://learn.microsoft.com: 0
    // https://learn.microsoft.com/aspnet/core: 57
    // https://learn.microsoft.com/azure: 1
    // https://learn.microsoft.com/azure/devops: 2
    // https://learn.microsoft.com/dotnet: 83
    // https://learn.microsoft.com/dotnet/desktop/wpf/get-started/create-app-visual-studio: 31
    // https://learn.microsoft.com/education: 0
    // https://learn.microsoft.com/shows/net-core-101/what-is-net: 42
    // https://learn.microsoft.com/enterprise-mobility-security: 0
    // https://learn.microsoft.com/gaming: 0
    // https://learn.microsoft.com/graph: 0
    // https://learn.microsoft.com/microsoft-365: 0
    // https://learn.microsoft.com/office: 0
    // https://learn.microsoft.com/powershell: 0
    // https://learn.microsoft.com/sql: 0
    // https://learn.microsoft.com/surface: 0
    // https://dotnetfoundation.org: 16
    // https://learn.microsoft.com/visualstudio: 0
    // https://learn.microsoft.com/windows: 0
    // https://learn.microsoft.com/maui: 6
    // Total: 238
    // Retrieving User objects with list of IDs...
    // 1: isEnabled= False
    // 2: isEnabled= False
    // 3: isEnabled= False
    // 4: isEnabled= False
    // 5: isEnabled= False
    // 6: isEnabled= False
    // 7: isEnabled= False
    // 8: isEnabled= False
    // 9: isEnabled= False
    // 0: isEnabled= False
    // Application ending.
    

##  다른 리소스


-->

<!--






-->

<!--
#  async 및 await를 사용한 비동기 프로그래밍

##  이 문서의 내용

[ TAP(Task 비동기 프로그래밍) 모델 ](task-asynchronous-programming-model) 은 비동기 코드에 대한
추상화를 제공합니다. 항상 그렇듯이 코드는 일련의 명령문으로 작성합니다. 다음 명령문이 시작되기 전에 각 명령문이 완료되는 것처럼 해당
코드를 읽을 수 있습니다. 이러한 명령문 중 일부에서 작업을 시작하고 진행 중인 작업을 나타내는 [ Task ](/ko-
kr/dotnet/api/system.threading.tasks.task) 를 반환할 수 있으므로 컴파일러는 여러 가지 변환을 수행합니다.

이 구문의 목표는 일련의 명령문처럼 읽지만 외부 리소스 할당과 작업 완료 시점에 따라 훨씬 더 복잡한 순서로 실행되는 코드를 사용하도록
설정하는 것입니다. 사람이 비동기 작업이 포함된 프로세스에 대한 지침을 제공하는 방법과 비슷합니다. 이 문서에서는 ` async ` 및 `
await ` 키워드를 사용하여 일련의 비동기 명령이 포함된 코드를 쉽게 추론하는 방법을 알아보기 위해 아침 식사를 준비하기 위한 지침의
예를 사용합니다. 아침 식사를 준비하는 방법을 설명하기 위해 작성하는 지침은 다음 목록과 같습니다.

  1. 커피 한 잔을 따릅니다. 
  2. 팬을 가열한 다음 계란 두 개를 볶습니다. 
  3. 베이컨 세 조각을 튀깁니다. 
  4. 빵 두 조각을 굽습니다. 
  5. 토스트에 버터와 잼을 바릅니다. 
  6. 오렌지 주스 한잔을 따릅니다. 

요리에 대한 경험이 있는 경우 이러한 지침은 **비동기적으로** 실행됩니다. 계란 프라이를 위해 팬을 데우기 시작한 다음, 베이컨을
시작합니다. 토스터에 빵을 넣고 계란 프라이를 시작합니다. 프로세스의 각 단계에서 작업을 시작한 다음, 주의가 필요한 작업에 주의를
돌립니다.

아침을 요리하는 것은 병렬로 수행되지 않는 비동기 작업의 좋은 예입니다. 한 사람(또는 스레드)이 이러한 모든 작업을 처리할 수 있습니다.
아침 식사 비유를 계속하면 첫 번째 작업이 완료되기 전에 다음 작업을 시작하여 한 사람이 비동기적으로 아침 식사를 만들 수 있습니다. 누군가
보고 있는지 여부에 관계없이 요리는 계속됩니다. 계란 프라이를 위해 팬을 데우기 시작하자마자 베이컨을 튀기기 시작할 수 있습니다. 베이컨
튀김이 시작되면 토스터에 빵을 넣을 수 있습니다.

병렬 알고리즘의 경우 여러 요리사(또는 스레드)가 필요합니다. 한 사람은 계란을 만들고 또 한 사람은 베이컨을 만드는 방식으로 진행될
것입니다. 즉 각각은 하나의 작업에만 집중할 것입니다. 각 요리사(또는 스레드)는 베이컨이 뒤집을 준비가 되거나 토스트가 나올 때까지
동기적으로 차단됩니다.

이제 C# 문으로 작성된 동일한 명령을 고려합니다.

    
    
    using System;
    using System.Threading.Tasks;
    
    namespace AsyncBreakfast
    {
        // These classes are intentionally empty for the purpose of this example. They are simply marker classes for the purpose of demonstration, contain no properties, and serve no other purpose.
        internal class Bacon { }
        internal class Coffee { }
        internal class Egg { }
        internal class Juice { }
        internal class Toast { }
    
        class Program
        {
            static void Main(string[] args)
            {
                Coffee cup = PourCoffee();
                Console.WriteLine("coffee is ready");
    
                Egg eggs = FryEggs(2);
                Console.WriteLine("eggs are ready");
    
                Bacon bacon = FryBacon(3);
                Console.WriteLine("bacon is ready");
    
                Toast toast = ToastBread(2);
                ApplyButter(toast);
                ApplyJam(toast);
                Console.WriteLine("toast is ready");
    
                Juice oj = PourOJ();
                Console.WriteLine("oj is ready");
                Console.WriteLine("Breakfast is ready!");
            }
    
            private static Juice PourOJ()
            {
                Console.WriteLine("Pouring orange juice");
                return new Juice();
            }
    
            private static void ApplyJam(Toast toast) =>
                Console.WriteLine("Putting jam on the toast");
    
            private static void ApplyButter(Toast toast) =>
                Console.WriteLine("Putting butter on the toast");
    
            private static Toast ToastBread(int slices)
            {
                for (int slice = 0; slice < slices; slice++)
                {
                    Console.WriteLine("Putting a slice of bread in the toaster");
                }
                Console.WriteLine("Start toasting...");
                Task.Delay(3000).Wait();
                Console.WriteLine("Remove toast from toaster");
    
                return new Toast();
            }
    
            private static Bacon FryBacon(int slices)
            {
                Console.WriteLine($"putting {slices} slices of bacon in the pan");
                Console.WriteLine("cooking first side of bacon...");
                Task.Delay(3000).Wait();
                for (int slice = 0; slice < slices; slice++)
                {
                    Console.WriteLine("flipping a slice of bacon");
                }
                Console.WriteLine("cooking the second side of bacon...");
                Task.Delay(3000).Wait();
                Console.WriteLine("Put bacon on plate");
    
                return new Bacon();
            }
    
            private static Egg FryEggs(int howMany)
            {
                Console.WriteLine("Warming the egg pan...");
                Task.Delay(3000).Wait();
                Console.WriteLine($"cracking {howMany} eggs");
                Console.WriteLine("cooking the eggs ...");
                Task.Delay(3000).Wait();
                Console.WriteLine("Put eggs on plate");
    
                return new Egg();
            }
    
            private static Coffee PourCoffee()
            {
                Console.WriteLine("Pouring coffee");
                return new Coffee();
            }
        }
    }
    

![synchronous breakfast](https://learn.microsoft.com/ko-
kr/dotnet/csharp/asynchronous-programming/media/synchronous-breakfast.png)

동기적으로 준비된 아침 식사는 합계가 각 작업의 합계이기 때문에 약 30분이 걸렸습니다.

컴퓨터에서는 사람들이 수행하는 것과 같은 방식으로 이러한 명령을 해석하지 않습니다. 다음 명령문으로 이동하기 전에 작업이 완료될 때까지
컴퓨터는 각 명령문에서 차단됩니다. 이로 인해 불만족스러운 아침 식사를 만듭니다. 이전 작업이 완료될 때까지 이후 작업을 시작할 수
없었습니다. 아침 식사를 만드는 데 훨씬 더 오래 걸리고, 일부 음식은 식은 채로 제공되었을 것입니다.

컴퓨터에서 위의 명령을 비동기적으로 실행하게 하려면 비동기 코드를 작성해야 합니다.

이러한 문제는 현재 작성하는 프로그램에 중요합니다. 클라이언트 프로그램을 작성할 때 UI에서 사용자 입력에 응답해야 합니다. 웹에서 데이터를
다운로드하는 동안 애플리케이션에서 휴대폰이 중지된 것처럼 표시하면 안 됩니다. 서버 프로그램을 작성하는 경우 스레드가 차단되지 않도록
합니다. 이러한 스레드는 다른 요청을 처리할 수 있습니다. 비동기 대안이 있을 때 동기 코드를 사용하면 비용이 적게 드는 규모 확장 기능이
저하됩니다. 차단된 스레드에 대한 비용을 지불합니다.

성공적인 최신 애플리케이션에는 비동기 코드가 필요합니다. 언어 지원 없이 비동기 코드를 작성하는 경우 콜백, 완료 이벤트 또는 코드의 원래
의도를 모호하게 하는 다른 수단이 필요했습니다. 동기 코드의 이점은 단계별 작업을 통해 쉽게 검사하고 이해할 수 있다는 점입니다. 기존의
비동기 모델에서는 코드의 기본 동작이 아니라 코드의 비동기적 특성에 집중할 수 밖에 없었습니다.

##  차단하는 대신 대기

앞의 코드에서는 동기 코드를 구성하여 비동기 작업을 수행하는 잘못된 사례를 보여 줍니다. 작성한 대로 이 코드는 실행되는 스레드에서 다른
작업을 수행하지 못하도록 차단합니다. 작업이 진행되는 동안에는 중단되지 않습니다. 마치 빵을 넣은 후 토스터를 쳐다보는 것과 같습니다.
토스트가 나오기 전까지 아무하고도 대화하지 않을 것입니다.

먼저 이 코드를 업데이트하여 작업이 실행되는 동안 스레드가 차단되지 않도록 하겠습니다. ` await ` 키워드는 작업을 차단하지 않는
방식으로 시작한 다음, 해당 작업이 완료되면 실행을 계속합니다. 간단한 비동기 버전의 아침 식사 준비 코드는 다음과 같습니다.

    
    
    static async Task Main(string[] args)
    {
        Coffee cup = PourCoffee();
        Console.WriteLine("coffee is ready");
    
        Egg eggs = await FryEggsAsync(2);
        Console.WriteLine("eggs are ready");
    
        Bacon bacon = await FryBaconAsync(3);
        Console.WriteLine("bacon is ready");
    
        Toast toast = await ToastBreadAsync(2);
        ApplyButter(toast);
        ApplyJam(toast);
        Console.WriteLine("toast is ready");
    
        Juice oj = PourOJ();
        Console.WriteLine("oj is ready");
        Console.WriteLine("Breakfast is ready!");
    }
    

Important

총 경과 시간은 초기 동기 버전과 거의 같습니다. 이 코드에서는 아직 비동기 프로그래밍의 몇 가지 주요 기능을 활용하지 않았습니다.

팁

` FryEggsAsync ` , ` FryBaconAsync ` 및 ` ToastBreadAsync ` 의 메서드 본문은 각각 `
Task<Egg> ` , ` Task<Bacon> ` 및 ` Task<Toast> ` 를 반환하도록 모두 업데이트되었습니다. 이 메서드들은
원래 버전에서 “Async” 접미사를 포함하도록 이름이 바뀌었습니다. 해당 구현은 이 문서의 뒷부분에 나오는  최종 버전  의 일부로
표시됩니다.

참고 항목

` Main ` 메서드는 ` return ` 식이 없더라도 기본적으로 ` Task ` 이(가) 반환 됩니다. 자세한 내용은 [ void 반환
비동기 함수 평가 ](/ko-kr/dotnet/csharp/language-reference/language-
specification/classes#14153-evaluation-of-a-void-returning-async-function) 를
참조하세요.

이 코드는 계란이나 베이컨을 요리하는 동안 차단되지 않습니다. 하지만 이 코드는 다른 작업을 시작하지 않습니다. 토스트가 토스터에 넣어져
나올 때까지 쳐다보고 있습니다. 그러나 적어도 주의를 끌려고 하는 누구에게나 응답할 수는 있습니다. 여러 주문을 받는 식당에서 요리사는 첫
번째 요리를 하는 동안 또 다른 아침 식사 준비를 시작할 수 있습니다.

시작했지만 아직 완료되지 않은 작업을 기다리는 동안 아침 식사 작업 스레드가 차단되지 않습니다. 일부 애플리케이션의 경우 이 변경만으로
충분합니다. GUI 애플리케이션은 이 변경만으로도 사용자에게 응답합니다. 그러나 지금 시나리오에서는 더 많은 작업이 필요합니다. 각 구성
요소 작업이 순차적으로 실행되지 않도록 해야 합니다. 이전 작업이 완료되기를 기다리기 전에 각 구성 요소 작업을 시작하는 것이 좋습니다.

##  동시에 작업 시작

대부분의 시나리오에서는 독립적인 몇 가지 작업을 즉시 시작하려고 합니다. 그런 다음, 각 작업이 완료되면 준비된 다른 작업을 계속할 수
있습니다. 아침 식사 비유에서 이는 아침 식사를 더 빨리 준비하는 방법입니다. 모든 것을 거의 동시에 완료할 수 있습니다. 이에 따라 따뜻한
아침 식사가 준비됩니다.

[ System.Threading.Tasks.Task ](/ko-kr/dotnet/api/system.threading.tasks.task)
및 관련 형식은 진행 중인 작업을 추론하는 데 사용할 수 있는 클래스입니다. 이를 통해 아침 식사를 만드는 방법과 더 유사한 코드를 작성할
수 있습니다. 계란, 베이컨 및 토스트 요리를 동시에 시작할 수 있을 것입니다. 각 요리에 필요한 작업이 있으므로 해당 작업에 주의를
기울이고, 다음 작업을 처리한 다음, 주의가 필요한 다른 작업을 기다립니다.

작업을 시작하고, 해당 작업을 나타내는 [ Task ](/ko-kr/dotnet/api/system.threading.tasks.task)
개체를 유지합니다. 결과를 사용하기 전에 각 작업을 기다립니다( ` await ` ).

아침 식사 코드를 이처럼 변경해 보겠습니다. 첫 번째 단계는 작업을 기다리지 않고 시작될 때 해당 작업을 저장하는 것입니다.

    
    
    Coffee cup = PourCoffee();
    Console.WriteLine("Coffee is ready");
    
    Task<Egg> eggsTask = FryEggsAsync(2);
    Egg eggs = await eggsTask;
    Console.WriteLine("Eggs are ready");
    
    Task<Bacon> baconTask = FryBaconAsync(3);
    Bacon bacon = await baconTask;
    Console.WriteLine("Bacon is ready");
    
    Task<Toast> toastTask = ToastBreadAsync(2);
    Toast toast = await toastTask;
    ApplyButter(toast);
    ApplyJam(toast);
    Console.WriteLine("Toast is ready");
    
    Juice oj = PourOJ();
    Console.WriteLine("Oj is ready");
    Console.WriteLine("Breakfast is ready!");
    

앞의 코드는 아침 식사를 더 빨리 준비하지 않습니다. 작업이 시작되자마자 모든 ` await ` 작업이 완료됩니다. 다음으로, 아침 식사를
제공하기 전에 베이컨과 달걀에 대한 ` await ` 문을 메서드 끝으로 이동할 수 있습니다.

    
    
    Coffee cup = PourCoffee();
    Console.WriteLine("Coffee is ready");
    
    Task<Egg> eggsTask = FryEggsAsync(2);
    Task<Bacon> baconTask = FryBaconAsync(3);
    Task<Toast> toastTask = ToastBreadAsync(2);
    
    Toast toast = await toastTask;
    ApplyButter(toast);
    ApplyJam(toast);
    Console.WriteLine("Toast is ready");
    Juice oj = PourOJ();
    Console.WriteLine("Oj is ready");
    
    Egg eggs = await eggsTask;
    Console.WriteLine("Eggs are ready");
    Bacon bacon = await baconTask;
    Console.WriteLine("Bacon is ready");
    
    Console.WriteLine("Breakfast is ready!");
    

![asynchronous breakfast](https://learn.microsoft.com/ko-
kr/dotnet/csharp/asynchronous-programming/media/asynchronous-breakfast.png)

비동기적으로 준비된 아침 식사에는 대략 20분이 걸렸는데, 일부 작업이 동시에 실행되었기 때문에 이렇게 시간을 절약할 수 있는 것입니다.

앞의 코드가 더 잘 작동합니다. 모든 비동기 작업을 한 번에 시작합니다. 결과가 필요할 때만 각 작업을 기다립니다. 앞의 코드는 다른
마이크로서비스를 요청한 다음, 결과를 단일 페이지로 결합하는 웹 애플리케이션의 코드와 비슷할 수 있습니다. 모든 요청을 즉시 수행한 다음,
이러한 모든 작업을 기다리고( ` await ` ) 웹 페이지를 구성합니다.

##  작업 구성

토스트를 제외한 모든 아침 식사가 동시에 준비되었습니다. 토스트를 만드는 것은 비동기 작업(빵 굽기)과 동기 작업(버터와 잼 바르기)의
구성입니다. 이 코드를 업데이트하면 중요한 개념을 알 수 있습니다.

Important

동기 작업이 뒤따르는 비동기 작업으로 구성된 작업은 비동기 작업입니다. 즉 작업의 일부가 비동기이면 전체 작업이 비동기입니다.

이전 코드에서는 [ Task ](/ko-kr/dotnet/api/system.threading.tasks.task) 또는 [
Task<TResult> ](/ko-kr/dotnet/api/system.threading.tasks.task-1) 개체를 사용하여 실행
중인 작업을 유지할 수 있음을 보여 주었습니다. 결과를 사용하기 전에 각 작업을 기다립니다( ` await ` ). 다음 단계는 다른 작업의
결합을 나타내는 메서드를 만드는 것입니다. 아침 식사를 제공하기 전에 빵을 구운 후에 버터와 잼을 바르는 것을 나타내는 작업을 기다리려고
합니다. 이 작업은 다음 코드를 사용하여 나타낼 수 있습니다.

    
    
    static async Task<Toast> MakeToastWithButterAndJamAsync(int number)
    {
        var toast = await ToastBreadAsync(number);
        ApplyButter(toast);
        ApplyJam(toast);
    
        return toast;
    }
    

앞의 메서드에서 해당 시그니처에는 ` async ` 한정자가 있습니다. 이 경우 이 메서드에서 비동기 작업이 포함된 ` await ` 문을
포함하고 있다고 컴파일러에 알립니다. 이 메서드는 빵을 구운 다음, 버터와 잼을 바르는 작업을 나타내며, 이러한 세 가지 작업의 구성을
나타내는 [ Task<TResult> ](/ko-kr/dotnet/api/system.threading.tasks.task-1) 를
반환합니다. 이제 main 코드 블록은 다음과 같습니다.

    
    
    static async Task Main(string[] args)
    {
        Coffee cup = PourCoffee();
        Console.WriteLine("coffee is ready");
    
        var eggsTask = FryEggsAsync(2);
        var baconTask = FryBaconAsync(3);
        var toastTask = MakeToastWithButterAndJamAsync(2);
    
        var eggs = await eggsTask;
        Console.WriteLine("eggs are ready");
    
        var bacon = await baconTask;
        Console.WriteLine("bacon is ready");
    
        var toast = await toastTask;
        Console.WriteLine("toast is ready");
    
        Juice oj = PourOJ();
        Console.WriteLine("oj is ready");
        Console.WriteLine("Breakfast is ready!");
    }
    

앞의 변경에서는 비동기 코드를 사용하는 데 있어 중요한 기술을 보여 주었습니다. 작업을 반환하는 새 메서드로 구분하여 작업을 구성합니다.
해당 작업을 기다리는 시기를 선택할 수 있습니다. 다른 작업을 동시에 시작할 수 있습니다.

##  비동기 예외

이 시점까지 이러한 모든 작업이 성공적으로 완료된다고 암시적으로 가정했습니다. 비동기 메서드는 동기 메서드와 마찬가지로 예외를
throw합니다. 예외 및 오류 처리에 대한 비동기 지원은 일반적인 비동기 지원과 같은 목표를 달성하려고 합니다. 즉, 일련의 동기 문처럼
읽는 코드를 작성해야 합니다. 작업은 성공적으로 완료될 수 없는 경우 예외를 throw합니다. 시작된 작업이 ` awaited ` 인 경우
클라이언트 코드에서 해당 예외를 catch할 수 있습니다. 예를 들어 토스트를 만드는 동안 토스터에 불이 난다고 가정해 보겠습니다. `
ToastBreadAsync ` 메서드를 다음 코드와 일치하도록 수정하여 이 상황을 시뮬레이션할 수 있습니다.

    
    
    private static async Task<Toast> ToastBreadAsync(int slices)
    {
        for (int slice = 0; slice < slices; slice++)
        {
            Console.WriteLine("Putting a slice of bread in the toaster");
        }
        Console.WriteLine("Start toasting...");
        await Task.Delay(2000);
        Console.WriteLine("Fire! Toast is ruined!");
        throw new InvalidOperationException("The toaster is on fire");
        await Task.Delay(1000);
        Console.WriteLine("Remove toast from toaster");
    
        return new Toast();
    }
    

참고 항목

연결할 수 없는 코드에 대해 앞의 코드를 컴파일하면 경고가 표시됩니다. 토스터에 불이 나면 작업이 정상적으로 진행되지 않으므로 이는
의도적입니다.

이러한 변경을 수행한 후 애플리케이션을 실행하면 다음 텍스트와 유사하게 출력됩니다.

    
    
    Pouring coffee
    Coffee is ready
    Warming the egg pan...
    putting 3 slices of bacon in the pan
    Cooking first side of bacon...
    Putting a slice of bread in the toaster
    Putting a slice of bread in the toaster
    Start toasting...
    Fire! Toast is ruined!
    Flipping a slice of bacon
    Flipping a slice of bacon
    Flipping a slice of bacon
    Cooking the second side of bacon...
    Cracking 2 eggs
    Cooking the eggs ...
    Put bacon on plate
    Put eggs on plate
    Eggs are ready
    Bacon is ready
    Unhandled exception. System.InvalidOperationException: The toaster is on fire
       at AsyncBreakfast.Program.ToastBreadAsync(Int32 slices) in Program.cs:line 65
       at AsyncBreakfast.Program.MakeToastWithButterAndJamAsync(Int32 number) in Program.cs:line 36
       at AsyncBreakfast.Program.Main(String[] args) in Program.cs:line 24
       at AsyncBreakfast.Program.<Main>(String[] args)
    

토스터에 불이 붙은 시점과 예외가 관찰되는 시점 사이에 꽤 많은 작업이 완료되었음을 알 수 있습니다. 비동기적으로 실행되는 작업에서 예외를
throw하면 해당 Task가 _**오류** _ 상태가 됩니다. Task 개체는 [ Task.Exception ](/ko-
kr/dotnet/api/system.threading.tasks.task.exception#system-threading-tasks-
task-exception) 속성에서 throw된 예외를 포함합니다. 오류 상태인 작업이 대기되면 예외를 throw합니다.

이해해야 할 두 가지 중요한 메커니즘이 있습니다. 하나는 예외가 오류 상태인 작업에 저장되는 방식이고 다른 하나는 코드가 오류 상태인 작업을
대기할 때 예외가 패키지 해제되었다가 다시 throw되는 방식입니다.

비동적으로 실행되는 코드가 예외를 throw하면 해당 예외는 ` Task ` 에 저장됩니다. 비동기 작업 중에는 둘 이상의 예외가
throw될 수 있으므로 [ Task.Exception ](/ko-
kr/dotnet/api/system.threading.tasks.task.exception#system-threading-tasks-
task-exception) 속성은 [ System.AggregateException ](/ko-
kr/dotnet/api/system.aggregateexception) 입니다. throw된 모든 예외는 [
AggregateException.InnerExceptions ](/ko-
kr/dotnet/api/system.aggregateexception.innerexceptions#system-
aggregateexception-innerexceptions) 컬렉션에 추가됩니다. 해당 ` Exception ` 속성이 null이면 새
` AggregateException ` 이 만들어지고 throw된 예외는 컬렉션의 첫 번째 항목이 됩니다.

오류 상태인 작업의 가장 일반적인 시나리오는 ` Exception ` 속성이 정확히 하나의 예외를 포함하는 것입니다. 코드가 오류 상태인
작업을 ` awaits ` 하면 [ AggregateException.InnerExceptions ](/ko-
kr/dotnet/api/system.aggregateexception.innerexceptions#system-
aggregateexception-innerexceptions) 컬렉션의 첫 번째 예외가 다시 throw됩니다. 그렇기 때문에 이 예제의
출력에 ` AggregateException ` 대신 ` InvalidOperationException ` 이 표시되는 것입니다. 첫 번째
내부 예외를 추출하면 동기 메서드로 작업하는 것과 최대한 유사하게 비동기 메서드로 작업할 수 있습니다. 시나리오에서 여러 예외를 생성할 수
있는 경우 코드에서 ` Exception ` 속성을 검사할 수 있습니다.

팁

인수 유효성 검사 예외는 작업 반환 메서드에서 _동기적으로_ 나타나는 것이 좋습니다. 자세한 내용과 이 작업을 수행하는 방법의 예는 [ 작업
반환 메서드의 예외 ](../fundamentals/exceptions/creating-and-throwing-
exceptions#exceptions-in-task-returning-methods) 를 참조하세요.

계속하기 전에 ` ToastBreadAsync ` 메서드에서 다음 두 줄을 주석으로 처리합니다. 또 다른 불이 시작되기를 원치는 않으니까요.

    
    
    Console.WriteLine("Fire! Toast is ruined!");
    throw new InvalidOperationException("The toaster is on fire");
    

##  효율적인 작업 대기

` Task ` 클래스의 메서드를 사용하여 앞의 코드 끝에 있는 일련의 ` await ` 문을 향상시킬 수 있습니다. 이러한 API 중
하나인 [ WhenAll ](/ko-kr/dotnet/api/system.threading.tasks.task.whenall) 은 다음
코드와 같이 인수 목록의 모든 작업이 완료되면 완료된 [ Task ](/ko-
kr/dotnet/api/system.threading.tasks.task) 를 반환합니다.

    
    
    await Task.WhenAll(eggsTask, baconTask, toastTask);
    Console.WriteLine("Eggs are ready");
    Console.WriteLine("Bacon is ready");
    Console.WriteLine("Toast is ready");
    Console.WriteLine("Breakfast is ready!");
    

또 다른 옵션으로, 인수가 완료되면 완료된 ` Task<Task> ` 를 반환하는 [ WhenAny ](/ko-
kr/dotnet/api/system.threading.tasks.task.whenany) 를 사용하는 것입니다. 반환된 작업은 이미
완료되었음을 알고 있으므로 기다릴 수 있습니다. 다음 코드에서는 [ WhenAny ](/ko-
kr/dotnet/api/system.threading.tasks.task.whenany) 를 사용하여 첫 번째 작업이 완료될 때까지 기다린
다음, 결과를 처리하는 방법을 보여 줍니다. 완료된 작업의 결과가 처리되면 완료된 작업을 ` WhenAny ` 에 전달된 작업 목록에서
제거합니다.

    
    
    var breakfastTasks = new List<Task> { eggsTask, baconTask, toastTask };
    while (breakfastTasks.Count > 0)
    {
        Task finishedTask = await Task.WhenAny(breakfastTasks);
        if (finishedTask == eggsTask)
        {
            Console.WriteLine("Eggs are ready");
        }
        else if (finishedTask == baconTask)
        {
            Console.WriteLine("Bacon is ready");
        }
        else if (finishedTask == toastTask)
        {
            Console.WriteLine("Toast is ready");
        }
        await finishedTask;
        breakfastTasks.Remove(finishedTask);
    }
    

끝부분에 줄 ` await finishedTask; ` 이(가) 표시됩니다. 이 줄 ` await Task.WhenAny ` 은(는) 완료된
작업을 기다리지 않습니다. ` await ` ` Task.WhenAny ` 에서 반환된 ` Task ` 입니다. ` Task.WhenAny
` 결과는 완료되었거나 오류가 발생한 작업입니다. 실행이 완료된 것을 알고 있더라도 해당 작업을 다시 ` await ` 해야 합니다. 이것이
결과를 검색하거나 오류를 일으키는 예외가 발생하는지 확인하는 방법입니다.

변경 내용을 모두 적용한 후 코드의 최종 버전은 다음과 같습니다.

    
    
    using System;
    using System.Collections.Generic;
    using System.Threading.Tasks;
    
    namespace AsyncBreakfast
    {
        // These classes are intentionally empty for the purpose of this example. They are simply marker classes for the purpose of demonstration, contain no properties, and serve no other purpose.
        internal class Bacon { }
        internal class Coffee { }
        internal class Egg { }
        internal class Juice { }
        internal class Toast { }
    
        class Program
        {
            static async Task Main(string[] args)
            {
                Coffee cup = PourCoffee();
                Console.WriteLine("coffee is ready");
    
                var eggsTask = FryEggsAsync(2);
                var baconTask = FryBaconAsync(3);
                var toastTask = MakeToastWithButterAndJamAsync(2);
    
                var breakfastTasks = new List<Task> { eggsTask, baconTask, toastTask };
                while (breakfastTasks.Count > 0)
                {
                    Task finishedTask = await Task.WhenAny(breakfastTasks);
                    if (finishedTask == eggsTask)
                    {
                        Console.WriteLine("eggs are ready");
                    }
                    else if (finishedTask == baconTask)
                    {
                        Console.WriteLine("bacon is ready");
                    }
                    else if (finishedTask == toastTask)
                    {
                        Console.WriteLine("toast is ready");
                    }
                    await finishedTask;
                    breakfastTasks.Remove(finishedTask);
                }
    
                Juice oj = PourOJ();
                Console.WriteLine("oj is ready");
                Console.WriteLine("Breakfast is ready!");
            }
    
            static async Task<Toast> MakeToastWithButterAndJamAsync(int number)
            {
                var toast = await ToastBreadAsync(number);
                ApplyButter(toast);
                ApplyJam(toast);
    
                return toast;
            }
    
            private static Juice PourOJ()
            {
                Console.WriteLine("Pouring orange juice");
                return new Juice();
            }
    
            private static void ApplyJam(Toast toast) =>
                Console.WriteLine("Putting jam on the toast");
    
            private static void ApplyButter(Toast toast) =>
                Console.WriteLine("Putting butter on the toast");
    
            private static async Task<Toast> ToastBreadAsync(int slices)
            {
                for (int slice = 0; slice < slices; slice++)
                {
                    Console.WriteLine("Putting a slice of bread in the toaster");
                }
                Console.WriteLine("Start toasting...");
                await Task.Delay(3000);
                Console.WriteLine("Remove toast from toaster");
    
                return new Toast();
            }
    
            private static async Task<Bacon> FryBaconAsync(int slices)
            {
                Console.WriteLine($"putting {slices} slices of bacon in the pan");
                Console.WriteLine("cooking first side of bacon...");
                await Task.Delay(3000);
                for (int slice = 0; slice < slices; slice++)
                {
                    Console.WriteLine("flipping a slice of bacon");
                }
                Console.WriteLine("cooking the second side of bacon...");
                await Task.Delay(3000);
                Console.WriteLine("Put bacon on plate");
    
                return new Bacon();
            }
    
            private static async Task<Egg> FryEggsAsync(int howMany)
            {
                Console.WriteLine("Warming the egg pan...");
                await Task.Delay(3000);
                Console.WriteLine($"cracking {howMany} eggs");
                Console.WriteLine("cooking the eggs ...");
                await Task.Delay(3000);
                Console.WriteLine("Put eggs on plate");
    
                return new Egg();
            }
    
            private static Coffee PourCoffee()
            {
                Console.WriteLine("Pouring coffee");
                return new Coffee();
            }
        }
    }
    

![when any async breakfast](https://learn.microsoft.com/ko-
kr/dotnet/csharp/asynchronous-programming/media/whenany-async-breakfast.png)

비동기적으로 준비된 아침 식사의 최종 버전에는 대략 6분이 걸렸는데, 일부 작업을 동시에 실행하고 코드가 여러 작업을 한 번에 모니터링하고
필요한 경우에만 작업을 수행했기 때문입니다.

이 최종 코드는 비동기입니다. 이 코드는 아침 식사를 요리하는 방법을 더 정확하게 반영하고 있습니다. 앞의 코드를 이 문서의 첫 번째 코드
샘플과 비교해 보세요. 핵심 작업은 코드를 읽어 파악할 수 있습니다. 이 코드는 이 문서의 시작 부분에 나와 있는 아침 식사 준비 지침을
읽는 것과 동일한 방식으로 읽을 수 있습니다. ` async ` 및 ` await ` 언어 기능을 사용하면 모든 사용자가 작성된 이러한
지침을 따를 수 있습니다. 가능한 한 작업을 시작하지만 작업이 완료될 때까지 기다리는 것을 차단하지 않도록 합니다.

##  다음 단계


-->

<!--






-->

<!--
async await 두 번째 편이자 마지막 편!

빵!  끗!

##  인트로

이틀간 밤을  새우며  stackoverflow와 저명한 C# 개발자의 개인 홈페이지에서 글을 읽으며 async await 개념을 정리했다.
아직도 궁금한 부분이 많고 이해하지 못하는 부분도 많다.

그럼에도 불구하고 포스팅을 하는 이유는 국내에 async와 await에 관한 글이 많지 않기 때문이다.

※ 꽤 긴 글이 될 것 같습니다. 여러 내용 가운데 본인이 필요로 하는 지식이 있길 기원합니다.

※ 잘못된 지식이 있을 수 있습니다. 잘못된 내용이 있다면 댓글로 알려주세요. 반영하겠습니다 :)

async awiat의 선행 지식인 동기 비동기의 개념이 아직 부족하시다면 해당 포스팅을 참고하시기 바랍니다.

[ async await 기초 #1 (+ 동기 비동기의 개념) ](https://kangworld.tistory.com/24)

[ [C#] async await 기초 #1 : 동기 비동기 개념 이해하기  인트로 C# .NET FRAMEWORK 4.5부터 추가된
async awiat 키워드에 대해서 알아보려 한다. async awiat는 서버(ex 게임 서버 웹서버)를 구축할 때 사용되는 중요한 개념
중 하나다. 블로그에 정리하고 싶었는데  kangworld.tistory.com
](https://kangworld.tistory.com/24)

##  async

async 키워드는 해당  메서드 내에  await 키워드를 사용할 수 있게 만들어준다. 추가로 async 메서드의  반환 값을  일반적인
메서드와 다른 방식으로 다루도록 변경한다.

말이 조금 어렵다. 일단 지금은 async는 await 키워드를 메서드 내에 사용할 수 있게 만들어준다를 기억하자.

형식에 대해서 간단히 알아보면 async메서드는 반드시 void 또는 Task 또는 Task<T>를 반환해야 한다.

대부분 Task 혹은  Task<T>를  반환한다.

void를 사용하게 되면 비동기 메서드를 호출하는 쪽에서 비동기 제어할 수 없다. 종종 이벤트 핸들러로 사용할 때 void를 사용하곤 하는데
UI버튼을 클릭하면 일어나는 작업들을 비동기로 처리할 때 void를 사용하는 것이 대표적인 예시이다.

    
    
    public async void MyAsyncFunc()
    {
    
    }
    
    
    public async Task MyAsyncFunc()
    {
    	await Task.Delay(1000);
    }
    
    
    public async Task<int> MyAsyncFunc()
    {
    	await Task.Delay(1000);
    
    	return 1;
    }

##  await

await는 비동기 작업의 흐름을 제어하는 키워드라고 할 수 있다. 나아가 비동기 작업이 실행될 수 있는 곳이 바로 await이다.

아래 코드를 보면 알 수 있듯 await는 단항 연산자이며  **awaitable** 이라는 하나의 인수(argument)를 가진다.

> awaitable  
>  간단하게 Task 또는 Task<T>를 반환하는 함수(+메서드)라고 생각하면 된다.  
>  
>  +awaitable은 void도 반환하지만 Task를 반환하는 awaitable과는 결이 다르다고 한다.
    
    
    public static void Main(string[] args)
    {
        MyAsyncFunc();
        Console.WriteLine("End Main");
        Console.Read();
    }
    
    public static async void MyAsyncFunc()
    {
        await Task.Delay(5000);
        Console.WriteLine("End MyAsyncFunc");
    }

메인 스레드는 MyAsyncFunc 메서드를 호출하고  await Task.Delay(5000)를 실행한다.

Task.Delay(5000)는 내부적으로 타이머를 사용하며 타이머는 스레드 풀의 큐에 들어가게 된다. 이후 await에 의해 작업의 흐름이
MyAsyncFunc를 호출한 호출자 스레드에게 넘어간다.

호출자 스레드(메인 스레드)는 "End Main"을 출력하고 5초 뒤에 Task.Delay(5000) 작업이 끝나면  스레드 풀에  있는
잉여 스레드가 "End MyAsyncFunc"를 출력된다. 중요한 점은 호출자 스레드를 5초간 Block하지 않는다는 사실이다.

> C# Console 또는 Web apps의 실행 결과입니다.  
>  Windows Forms 또는 WPF와 같이 GUI를 다루는 app은 다르게 동작합니다.

지금 이해가  안 되더라도  이후에 다시  설명할 테니  대충 흐름만 알고 넘어가자.

await 키워드를 만나는 순간 내부적으로 복잡한 일이 발생하는데 지금 당장 다룰 문제는 아닌 것 같다.

그럼 이제 await를 더 자세하게 이해하기 위한 예제 코드를 살펴보자

###  ** await 예제 #1 - Task  **

Task 클래스는 비동기 작업 래퍼(wrapper)이다.

이해하기 쉽게 Task.Delay(5000)를 설명하면 5초 후 완료되는  작업을 Task 형태로 래핑하는 작업을 수행한다.  참고로
Thread.Sleep(5000)는 스레드의 실행을 5초간 중지하는 반면 Task.Delay(5000)는 현재 스레드를 중지하지 않는다.

    
    
    using System;
    using System.Threading.Tasks;
    
    namespace AsyncTest
    {
        class Program
        {
            public static void Main(string[] args)
            {
                TaskTest();
                System.Console.WriteLine("Main Done");
            }
            private static void TaskTest()
            {
                Task.Delay(5000);
                System.Console.WriteLine("TaskTest Done");
            }
        }
    }

실행 결과를 보면 "TaskTest Done"이 바로 출력되는 것을 확인할 수 있다.  ~~ ~~

![](https://blog.kakaocdn.net/dn/bkcHE5/btrbVnwH7GK/wlGoZDUltVhNhbGiPouukk/img.gif)

(+ 2021.08.29 수정

5초를 기다리지 않고  "TaskTest Done"이 바로 출력되는 이유는 Task.Delay(5000);의 반환 값인 5초를 기다리는
작업(Task)을 await 하지 않았기 때문이다. Task를 await 하지 않았기에 프로그램은 5초를 기다리는 작업이 완료되길 기다리지
않고 계속 실행된다. 실제로 await 하지 않은 Task의 Status를 살펴보면 대기(  WaitingForActivation)후 완료(
RanToCompletion)됨을 볼 수 있다. 마치 혼자 눈 감고 5초를 셌는데 기다리는 친구는 아무도 없는 느낌이다.

여기서 한 가지 중요한 사실을 알 수 있다. Task와 같은 awaitable을 await 키워드 없이 사용하게 되면 작업의 종료 시점이
언제인지 알 수 없게 되며 작업을 통제할 수 없다. 작업을 통제할 수 없게 되면 때에 따라 해당 작업이 무의미할 수도 있다. 작업의 통제라는
개념이 지금은 이해가 안 될 수 있지만 후에 서술한 예제를 보면 이해하기 쉬울 것이다.)

![](https://blog.kakaocdn.net/dn/bg1iA0/btrdrlxLfDW/7hFUcq8M0hr94Ybzcgut6k/img.png)
![](https://blog.kakaocdn.net/dn/bPBxq9/btrdptcuhgq/54MprZMEK0nHLTqriOfk2K/img.png)

###  ** await 예제 #2 - async await  **

이전 예제를 살펴봤다면 이런 궁금증이 들지도 모른다.

"만약 모든 Task가 비동기라면 Task.Delay(5000)는 왜  쓴 거고  async await는 도대체 뭔데? 어디에  사용하는
건데?"

이젠  async와 await 키워드를 사용해서  Task.Delay(5000)를 비동기적으로 수행함과 동시에 흐름을 제어해보자.

[변경점 1] TaskTest 메서드에 async 키워드가 추가됐다.

[변경점 2]  Task.Delay(5000) 앞에  await 키워드가 추가됐다.

    
    
    using System;
    using System.Threading.Tasks;
    
    namespace AsyncTest
    {
        class Program
        {
            public static void Main(string[] args)
            {
                TaskTest();
                System.Console.WriteLine("Main Thread is NOT Blocked");
                Console.ReadLine();
            }
            private static async void TaskTest()
            {
                await Task.Delay(5000);
                System.Console.WriteLine("TaskTest Done");
            }
        }
    }

대략적으로 실행 과정은 이러하다.

[1] Main 메서드 진입

[2] TaskTest 메서드 진입

[3] await Task.Delay(5000)를 실행

[4] 스레드 풀의 스레드가 Task.Delay(5000)를 실행하고 작업의 흐름이 TaskTest를 호출한 호출자에게 넘어간다.

> Task.Delay는 새로운 Thread를 생성하지 않습니다.  
>  Task.Delay는 내부적으로 thread-pool을 사용하는 timer를 사용합니다.

[5] 호출자 스레드는 "Main Thread is NOT Blocked"를 출력한다.

[6] 5초간의 딜레이를 마치고  Task.Delay(5000)를 실행한 스레드는 "TaskTest Done"를 출력한다.

![](https://blog.kakaocdn.net/dn/coVlg8/btrbWeM0tgj/SQEZkRsQNObByInYcT1Ac1/img.gif)

###  ** await 예제 #3 - Task를 반환하는 async 메서드  **

비동기로 실행할 수 있는 더 현실적이고 멋진 일을 해보자.

await를 처음 설명할 때 await는 비동기 작업의 흐름을 제어하는 키워드라고 언급한  적 있다. (사실 우리는 이미 TaskTest에서
await키워드로 흐름을 제어하고 있었다!)  흐름을 제어할 수 있다는 말은 어떤 일의 순서를 정할 수 있다는 의미이기도 하다.

동기로 실행되는 코드에 사이에 await 키워드를  끼워 넣어  작업의 순서를 정해보고 비동기 작업이 왜  유용했는지  체감해보자.

[변경점 1] Main 메서드에 async 키워드가 추가됐다.

[변경점 2] Main 메서드가 Task를 반환한다.

[변경점 3] TaskTest 메서드가 Task를 반환한다.

[변경점 4] Task t = TaskTest(); 코드를 통해 TaskTest로부터 t를 반환받는다.

[변경점 5] await t; t(awaitable)이 끝날  때까지  기다린다.

[변경점 6] await t; 전후로 for문이 추가되었다.

이제 Main 메서드도 async 메서드이다. 즉 Main 내부에서 await 키워드를 사용할 수 있으며 TaskTest 메서드처럼
t(awaitable)이 끝나기 전까지  그다음  코드가 실행되지 않게 된다.

    
    
    using System;
    using System.Threading.Tasks;
    
    namespace AsyncTest
    {
        class Program
        {
            public static async Task Main(string[] args)
            {
                Task t = TaskTest();
                
                for(int i = 0; i < 10; i++)
                {
                    System.Console.WriteLine("Do Something Before TaskTest");
                }
    
                await t;
    
                for (int i = 0; i < 10; i++)
                {
                    System.Console.WriteLine("Do Something after TaskTest");
                }
    
                Console.ReadLine();
            }
    
            private static async Task TaskTest()
            {
                await Task.Delay(5000);
                System.Console.WriteLine("TaskTest Done");
            }
        }
    }

실행결과에서 보듯 await를 통해 비동기 작업의 순서를 정해줄 수 있으며, Task.Delay(5000)처럼 오래 걸리는 비동기 작업이
처리되는 동안 다른 작업을 수행할 수 있다는 장점이 있다.

![](https://blog.kakaocdn.net/dn/xo3rL/btrbPbqEUD6/QF3IMxddHeCTmpQcMvrmCk/img.gif)

###  ** await 예제 #4 - Task<T>를 반환하는 async 메서드  **

마지막이며 가장 중요한 예제이다.

예제  #3까지  사용했던 TaskTest 예제이다.

    
    
    private static async Task TaskTest()
    {
        await Task.Delay(5000);
        System.Console.WriteLine("TaskTest Done");
    }

이제 TaskTest를 다르게 생각해보자. Task.Delay(5000)이 그저 5초를 기다리는 작업이 아닌 DB에서 데이터를 가져온다던지
혹은 네트워크상에서 데이터를 받아온다던지, 물리적인 저장공간에서 데이터를 입력하고 읽어오는 작업 등 매우 오래 걸리는 작업이라고 생각해보자.
그리고 그 작업이 끝나면 어떤 값을 반환할 수 있다고 생각해보자.

    
    
    private static async Task TaskTest()
    {
        await Task.Delay(5000); // DB or Server에서 데이터 가져오기 등 매우 오래 걸리는 작업이라 생각해보자
        System.Console.WriteLine("TaskTest Done");
    }

예를 들어 서버로부터  어떤 유저의 메신저 ID를 가져와서 반환한다고 가정하면 다음과 같이 변경할 수 있다.

    
    
    private static async Task<int> TaskTest()
    {
        await Task.Delay(5000); // DB or Server에서 데이터 가져오기 등 매우 오래 걸리는 작업이라 생각해보자
        System.Console.WriteLine("TaskTest Done");
    
        int UID = 100;
    
        return UID;
    }

그리고 이 반환된 UID를 호출한 쪽에서 받아보자.

[변경점 1]  더 이상  Task t = TaskTest();가 아닌 제네릭이 추가된  Task<int> t = TaskTest();이다.

[변경점 2] int UID = await t;

> 반환 값이 있는 경우 await를 통해서  반환 값을  추출할 수 있다.
    
    
    public static async Task Main(string[] args)
    {
        Task<int> t = TaskTest();
                
        for(int i = 0; i < 10; i++)
        {
            System.Console.WriteLine("Do Something Before TaskTest");
        }
    
        int UID = await t;
    
        Console.WriteLine($"UserID : {UID}");
    
        Console.ReadLine();
    }

![](https://blog.kakaocdn.net/dn/mBu4j/btrbV1GZ6pp/bw1cktVJ2Ue8CjyTNYIPnk/img.gif)

눈치가 빠른 분들은 TaskTest 메서드의 어색한 부분을 찾았을 것이다.

이해를  돕기 위해  int UID = 100;라고  하드 코딩한  것이지 다음과 같이  코딩하는 게  일반적인 방법일 것이다.

    
    
    private static async Task<int> TaskTest()
    {
        int UID = await DB or server에서 UID 얻어오는 비동기 메서드 호출...;
        System.Console.WriteLine("TaskTest Done");
    
        return UID;
    }

###  ** await 마무리  **

await 키워드를 실행하려 할 때 발생하는 상황을 정리하려 한다.

서술할 내용이 이해가 안 된다면 예제를 다시 보고 깊게  여러 번 생각하길 바랍니다.

async 메서드 내부의 await를 만나면  세 가지  경우로 나뉘게 된다.

첫 번째, awaitable이 예외를  발생한 채  끝난다면 await는  exception을 던진다. (본 포스팅에서 다루진 않았다.)

두 번째, awaitable이 이미 끝난 상태라면 async 메서드를,  마치 일반  메서드처럼,  동기 방식으로 계속 실행한다.

(참고 :  [ Task.FromResult 이해하기 ](https://kangworld.tistory.com/195) )

세 번째,  awaitable이 끝나지 않았다면 작업이 끝난 후 await 이후의 나머지 코드를 실행하도록 대기 작업으로 등록하고 async
메서드의 호출자에게 Task를 반환한다.

사실  몇 가지  예제로 async와 await를 이해하는 건 정말 어려운 일이다. 이해했다면 당신은 천재일지도...

언제나 그렇듯 코드로 이해하자. microsoft docs에 좋은 예제가 있어서 소개하려 한다.

##  예제 : 동기식 코드

식당에서 음식을 준비하는 과정을 동기식으로 구현한 코드다. 로직은 다음과 같다.

1\. 커피 한 잔을 따릅니다.

2\. 팬을 데운 다음, 계란 프라이 두 개를 만듭니다.

3\. 베이컨 세 조각을 튀깁니다.

4\. 빵 두 조각을 굽습니다.

5\. 토스트에 버터와 잼을 바릅니다.

6\. 오렌지 주스 한잔을 따릅니다.

![](https://blog.kakaocdn.net/dn/dBOxfa/btraBwiSDAz/kNFrBq47NpdnpxmVSmg0M1/img.png)
https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-
guide/concepts/async/#final-version

코드가 길다. 근데 다른 거 다 볼 필요 없이  **지금은 Main 함수만 이해하면 된다.**

Main에서 커피를 따르고 프라이를 만들고 베이컨을 튀기는 작업들이 순차적으로 일어나고 있다. 한 작업이 끝나야 다른 작업도 끝이 난다는
의미이다. 그 이유는 요리하는 함수  내부의 ** .Wait  ** 가  작업자 스레드를 블로킹하기 때문이다. (동기적으로 수행된다)

일반적인 동기식 프로그래밍이 바로 이런 방식이다. 하나가 끝나야 그다음이 있다.

    
    
    using System;
    using System.Threading.Tasks;
    
    namespace AsyncBreakfast
    {
        class Toast{}
        class Juice{}
        class Bacon{}
        class Egg{}
        class Coffee{}
    
        class Program
        {
            static void Main(string[] args)
            {
                Coffee cup = PourCoffee();
                Console.WriteLine("coffee is ready");
    
                Egg eggs = FryEggs(2);
                Console.WriteLine("eggs are ready");
    
                Bacon bacon = FryBacon(3);
                Console.WriteLine("bacon is ready");
    
                Toast toast = ToastBread(2);
                ApplyButter(toast);
                ApplyJam(toast);
                Console.WriteLine("toast is ready");
    
                Juice oj = PourOJ();
                Console.WriteLine("oj is ready");
                Console.WriteLine("Breakfast is ready!");
            }
    
            private static Juice PourOJ()
            {
                Console.WriteLine("Pouring orange juice");
                return new Juice();
            }
    
            private static void ApplyJam(Toast toast) =>
                Console.WriteLine("Putting jam on the toast");
    
            private static void ApplyButter(Toast toast) =>
                Console.WriteLine("Putting butter on the toast");
    
            private static Toast ToastBread(int slices)
            {
                for (int slice = 0; slice < slices; slice++)
                {
                    Console.WriteLine("Putting a slice of bread in the toaster");
                }
                Console.WriteLine("Start toasting...");
                Task.Delay(3000).Wait();
                Console.WriteLine("Remove toast from toaster");
    
                return new Toast();
            }
    
            private static Bacon FryBacon(int slices)
            {
                Console.WriteLine($"putting {slices} slices of bacon in the pan");
                Console.WriteLine("cooking first side of bacon...");
                Task.Delay(3000).Wait();
                for (int slice = 0; slice < slices; slice++)
                {
                    Console.WriteLine("flipping a slice of bacon");
                }
                Console.WriteLine("cooking the second side of bacon...");
                Task.Delay(3000).Wait();
                Console.WriteLine("Put bacon on plate");
    
                return new Bacon();
            }
    
            private static Egg FryEggs(int howMany)
            {
                Console.WriteLine("Warming the egg pan...");
                Task.Delay(3000).Wait();
                Console.WriteLine($"cracking {howMany} eggs");
                Console.WriteLine("cooking the eggs ...");
                Task.Delay(3000).Wait();
                Console.WriteLine("Put eggs on plate");
    
                return new Egg();
            }
    
            private static Coffee PourCoffee()
            {
                Console.WriteLine("Pouring coffee");
                return new Coffee();
            }
        }
    }

![](https://blog.kakaocdn.net/dn/beEWka/btraJnrfXiu/YPn6e0tTGkjR2KmBbFUoM0/img.gif)
동기식 실행 결과

###  ** 예제 : 비동기식 코드 Version 1  **

Main 함수와 일부 함수가 수정되었다.

수정된 내용으로는 await가 추가되었다. Main함수 내에도 await가 있으니 async 키워드가 붙어야 한다.

실행 결과는 달라진 게 없다. 요리하는 함수 내에 await가 붙었지만 Main함수에서 요리하는 함수를 await로 호출했기 때문에
await가 코드가 끝날 때까지 순차적으로 기다려야 한다.

    
    
    static async Task Main(string[] args)
    {
        Coffee cup = PourCoffee();
        Console.WriteLine("coffee is ready");
    
        Egg eggs = await FryEggsAsync(2);
        Console.WriteLine("eggs are ready");
    
        Bacon bacon = await FryBaconAsync(3);
        Console.WriteLine("bacon is ready");
    
        Toast toast = await ToastBreadAsync(2);
        ApplyButter(toast);
        ApplyJam(toast);
        Console.WriteLine("toast is ready");
    
        Juice oj = PourOJ();
        Console.WriteLine("oj is ready");
        Console.WriteLine("Breakfast is ready!");
    }
    
    private static async Task<Toast> ToastBreadAsync(int slices)
    {
        for (int slice = 0; slice < slices; slice++)
        {
        	Console.WriteLine("Putting a slice of bread in the toaster");
        }
        Console.WriteLine("Start toasting...");
        await Task.Delay(3000);
        Console.WriteLine("Remove toast from toaster");
    
        return new Toast();
    }
    
    private static async Task<Bacon> FryBaconAsync(int slices)
    {
        Console.WriteLine($"putting {slices} slices of bacon in the pan");
        Console.WriteLine("cooking first side of bacon...");
        await Task.Delay(3000);
        for (int slice = 0; slice < slices; slice++)
        {
        	Console.WriteLine("flipping a slice of bacon");
        }
        Console.WriteLine("cooking the second side of bacon...");
        await Task.Delay(3000);
        Console.WriteLine("Put bacon on plate");
    
        return new Bacon();
    }
    
    private static async Task<Egg> FryEggsAsync(int howMany)
    {
        Console.WriteLine("Warming the egg pan...");
        await Task.Delay(3000);
        Console.WriteLine($"cracking {howMany} eggs");
        Console.WriteLine("cooking the eggs ...");
        await Task.Delay(3000);
        Console.WriteLine("Put eggs on plate");
    
        return new Egg();
    }

![](https://blog.kakaocdn.net/dn/FbVtA/btraDAylXZI/pCDYimb7EpHHssffBBAXfK/img.gif)

###  ** 예제 : 비동기식 코드 Version 2  **

이젠 비동기식 코드로 한 단계 개선했다. 계란, 베이컨, 토스트를 만드는 일을 동시에 시작하게 되었다.

하지만 아직 아쉬운 부분은 Toast toast = await toastTask;이다. 사실 계란 프라이 또는 베이컨이 먼저 완료될 수도
있는데 무조건 토스트가 완료되길 기다리고 있기에 완벽하게 비동기라고 보긴 어렵다.

다만 이전보다 수행 속도가 눈에 띄게 차이 나기 시작했다.

    
    
    static async Task Main(string[] args)
    {
        Coffee cup = PourCoffee();
        Console.WriteLine("coffee is ready");
    
        Task<Egg> eggsTask = FryEggsAsync(2);
        Task<Bacon> baconTask = FryBaconAsync(3);
        Task<Toast> toastTask = ToastBreadAsync(2);
    
        Toast toast = await toastTask;
        ApplyButter(toast);
        ApplyJam(toast);
        Console.WriteLine("toast is ready");
        Juice oj = PourOJ();
        Console.WriteLine("oj is ready");
    
        Egg eggs = await eggsTask;
        Console.WriteLine("eggs are ready");
        Bacon bacon = await baconTask;
        Console.WriteLine("bacon is ready");
    
        Console.WriteLine("Breakfast is ready!");
    }

![](https://blog.kakaocdn.net/dn/bbmtpF/btraLtEQu28/soQoBJ4x9cALirh1TuTTB0/img.png)
https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-
guide/concepts/async/#final-version
![](https://blog.kakaocdn.net/dn/brQtBU/btraInFm2eK/ExNOT3LRRqJdDpiF8YEArk/img.gif)

###  ** 예제 : 비동기식 코드 Version 3  **

최종적인 비동기식 코드이다. List에 Task를 저장하고 가장 빠르게 조리된 음식을 출력하며 이후에 List에서 Task를 삭제한다.
Version 2와 다르게 임의의 Task를 고정적으로 기다릴 필요 없이 완료된 시간에 따라 Task의 처리가 이루어진다.

    
    
    static async Task Main(string[] args)
    {
        Task.Delay(5000).Wait();
    
        Coffee cup = PourCoffee();
        Console.WriteLine("coffee is ready");
    
        var eggsTask = FryEggsAsync(2);
        var baconTask = FryBaconAsync(3);
        var toastTask = MakeToastWithButterAndJamAsync(2);
    
        var breakfastTasks = new List<Task> { eggsTask, baconTask, toastTask };
        while (breakfastTasks.Count > 0)
        {
            Task finishedTask = await Task.WhenAny(breakfastTasks);
            if (finishedTask == eggsTask)
            {
            	Console.WriteLine("eggs are ready");
            }
            else if (finishedTask == baconTask)
            {
            	Console.WriteLine("bacon is ready");
            }
            else if (finishedTask == toastTask)
            {
            	Console.WriteLine("toast is ready");
            }
            breakfastTasks.Remove(finishedTask);
        }
    
        Juice oj = PourOJ();
        Console.WriteLine("oj is ready");
        Console.WriteLine("Breakfast is ready!");
    }
    
    static async Task<Toast> MakeToastWithButterAndJamAsync(int number)
    {
        var toast = await ToastBreadAsync(number);
        ApplyButter(toast);
        ApplyJam(toast);
    
        return toast;
    }

![](https://blog.kakaocdn.net/dn/VolaC/btraJzS7N1g/wz0LqxGAdxNnEYvZDs3Krk/img.png)
https://docs.microsoft.com/ko-kr/dotnet/csharp/programming-
guide/concepts/async/#final-version
![](https://blog.kakaocdn.net/dn/c2FNQV/btraIm0OalT/gcYeU4UbGQVusfgdkz8C80/img.gif)

##  마치며

사실  적고 싶은  내용은 많았는데 글이 길어지니 피로도가 급격히 쌓여 생각보다 부실하게  마무리됐다..

생각나는 내용들이 있다면 계속 추가하겠습니다.

TODO : ~~본문 개념 정리하기에 코드 추가, await Task.Run vs await Task, IO bound vs CPU
bound, await Task 반환 원리, 이벤트 헨들러~~

참고 자료

[ https://www.c-sharpcorner.com/article/async-and-await-in-c-sharp/
](https://www.c-sharpcorner.com/article/async-and-await-in-c-sharp/)

[ https://stackoverflow.com/questions/58035605/not-awaiting-an-async-call-is-
still-async-right ](https://stackoverflow.com/questions/58035605/not-awaiting-
an-async-call-is-still-async-right)

[ https://blog.stephencleary.com/2012/02/async-and-await.html
](https://blog.stephencleary.com/2012/02/async-and-await.html)


-->

<!--






-->

<!--
C# 5.0 : async / await 키워드  
  

C# 5.0부터 새로운 C# 키워드로 **async** 와 **await** 가 추가되었다. 이 키워드들은 기존의 비동기 프로그래밍
(asynchronous programming)을 보다 손쉽게 지원하기 위해 C# 5.0에 추가된 중요한 기능이다.  
  
C# async는 컴파일러에게 해당 메서드가 await를 가지고 있음을 알려주는 역활을 한다. async라고 표시된 메서드는 await를
1개 이상 가질 수 있는데, 하나도 없는 경우라도 컴파일은 가능하지만 Warning 메시지가 표시된다. async를 표시한다고 해서 자동으로
비동기 방식으로 프로그램을 수행하는 것은 아니고, 일종의 보조 역활을 하는 컴파일러 지시어로 볼 수 있다. async 메서드의 리턴 타입은
대부분의 경우 Task<TResult> (리턴값이 있는 경우) 혹은 Task (리턴값이 없는 경우) 인데, 예를 들어 리턴값이 string일
경우 async Task<string&gt method() 와 같이 정의하고 return "문자열"과 같이 문자열만 리턴한다. C#
컴파일러는 return 문의 문자열을 자동으로 Task<string&gt로 변환해 준다. 또 다른 async 메서드의 리턴 타입으로 void
타입이 있는데, 특히 이벤트핸들러를 위해 void 리턴을 허용하고 있다.  
  
실제 핵심 키워드는 await인데, 이 await는 일반적으로 [ Task ](/Threads/task.aspx) 혹은 [ Task<T>
](/Threads/taskOfT.aspx) 객체와 함께 사용된다. Task 이외의 클래스도 사용 가능한데, awaitable 클래스, 즉
GetAwaiter() 라는 메서드를 갖는 클래스이면 함께 사용 가능하다.  
  
UI 프로그램에서 await는 Task와 같은 awaitable 클래스의 객체가 완료되기를 기다리는데, 여기서 중요한 점은 ** UI
쓰레드가 정지되지 않고 메시지 루프를 계속 돌 수 있도록  ** 필요한 코드를 컴파일러가 await 키워드를 만나면 자동으로 추가한다는
점이다. 메시지 루프가 계속 돌게 만든다는 것은 마우스 클릭이나 키보드 입력 등과 같은 윈도우 메시지들을 계속 처리할 수 있다는 것을
의미한다. await는 해당 Task가 끝날 때까지 기다렸다가 완료 후, await 바로 다음 실행문부터 실행을 계속한다. await가
기다리는 Task 혹은 실행 메서드는 별도의 Worker Thread에서 돌 수도 있고, 또는 UI Thread에서 돌 수도 있다.  
  
아래 예제는 버튼 클릭으로 Run()이라는 async 메서드를 실행하고, Run 메서드 안에서 비동기 Task를 만들어 실행하고 결과를
기다리는 await 문의 예를 보여주고 있다. await는 LongCalcAsync() 라는 메서드가 끝나기를 기다렸다가 끝나면 결과를
sum에 할당한 후 다음 문장들을 계속 실행한다. 특히 여기서 주목할 만한 것은 결과값을 Label 컨트롤에 뿌려줄 때, Invoke()나
BeginInvoke()를 쓸 필요가 없다는 점이다. Background Thread에서 비동기 Task가 끝난 후, await가 다시
Caller가 갖고 있던 쓰레드 즉 UI Thread로 다음 문장들을 실행하게 하기 때문이다.

##  예제

    
    

    // 예제1

    private void button1_Click(object sender, EventArgs e)

    {

         Run();  //UI Thread에서 실행

    }

    

    private async void Run()

    {

        // 비동기로 Worker Thread에서 도는 task1

        // Task.Run(): .NET Framework 4.5+

        var task1 = Task.Run(() => LongCalcAsync(10));

    

        // task1이 끝나길 기다렸다가 끝나면 결과치를 sum에 할당

        int sum = await task1;

    

        // UI Thread 에서 실행

        // Control.Invoke 혹은 Control.BeginInvok 필요없음

        this.label1.Text = "Sum = " + sum;

        this.button1.Enabled = true;

    }

    

    private int LongCalcAsync(int times)

    {

        int result = 0;

        for (int i = 0; i < times; i++)

        {

            result += i;

            Thread.Sleep(1000); 

        }

        return result;

    }

    

* * *

##

[ ![](https://www.csharpstudy.com/image/CSharp-Basic-Practice-eBook.png) ]()

.NET 4.5 Async 혹은 TaskAsync 메서드들  
  

C# 5.0과 함께 선보인 .NET 4.5는 기존의 동기화(Synchronous) 메서드들과 구분하여 C#의 await (혹은 VB의
Await)를 지원하기 위해 많은 Async 메서드들을 추가하였다. 이 새 메서드들은 기본적으로 기존의 Synchronous 메서드명 뒤에
Async를 붙여 명명되었는데, 만약 기존에 Async로 끝나는 메서드가 이미 있었던 경우에는 TaskAsync를 메서드명에 붙여
명명하였다.  
  

##  예제

    
    

    System.IO.Stream.Read() : 기존 동기 메서드

    System.IO.Stream.ReadAsync() : 4.5 Async 메서드

    

    WebClient.DownloadStringAsync() : 기존 비동기 메서드

    WebClient.DownloadStringTaskAsync() : 4.5 TaskAsync 메서드

    

* * *

await : UI 쓰레드에서 도는 Task  
  

[Advanced Topic] await가 기다리는 Task는 대부분의 경우 Background Worker Thread에서 실행된다.
하지만 await를 썼다고 해서 자동으로 그 Task(혹은 메서드)가 Worker Thread에서 도는 것은 아니다. 아래 예제는
await를 사용했지만, 해당 Task(LongCalc2)는 (별도로 Worker Thread를 생성하지 않고) UI 쓰레드에서 실행된다.
만약 Worker Thread를 생성하려면, Task.Run() 등과 메서드를 사용하여 비동기 작업을 지정할 수 있다.  
  

##  예제

    
    

    // 예제3

    private void button1_Click(object sender, EventArgs e)

    {

         Run();  //UI Thread에서 실행

    }

    

    private async void Run()

    {    

        int sum = await LongCalc2(10);

        this.label1.Text = "Sum = " + sum;

        this.button1.Enabled = true;

    }

    

    private async Task<int> LongCalc2(int times)

    {

        //UI Thread에서 실행

        Debug.WriteLine(Thread.CurrentThread.ManagedThreadId);

        int result = 0;

        for (int i = 0; i < times; i++)

        {

            result += i;                

            await Task.Delay(1000);

        }

        return result;

    }

    

* * *

await : Task.ContinueWith()  
  

[Advanced Topic] 앞에서 이야기 하였듯이 await는 해당 Task가 끝난 후 await 문장이 있었던 곳으로부터 계속 다음
문장들을 실행하도록 되어있다. 이러한 기능은 .NET 4.0에서 소개 되었던 Task클래스의 ContinueWith()를 써서 아래와 같이
구현될 수 있다. 물론 C# 5.0 컴파일러가 await를 이렇게 변경한다는 것은 아니지만, 개념적으로 동일한 방식이라 볼 수 있다.  
  
아래 예제에서 ContinueWith() 메서드는 첫번째 파라미터에서 task1 이 끝난 후 실행될 명령들을 람다식으로 지정하고 있다.
그리고 두번째 파라미터에는 실행블럭이 현재 쓰레드 (예제의 경우 UI Thread)에서 실행하도록
TaskScheduler.FromCurrentSynchronizationContext()를 지정하고 있다. 즉, 개념적으로 await는 특정
Task가 실행된 후 이러 이러한 실행블럭을 현재 실행 (쓰레드) 컨텍스트에서 실행하도록 하는 것이다.  
  

##  예제

    
    

    // 예제4

    private void Run2()

    {    

        var task1 = Task<int>.Run(() => LongCalc2(10));

        

        // await task1과 동일한 효과

        //

        task1.ContinueWith(x => {

          this.label1.Text = "Sum = " + task1.Result;

          this.button1.Enabled = true;      

        }, TaskScheduler.FromCurrentSynchronizationContext());

    }

    

    

* * *

콘솔프로그램에서의 await  
  

[Advanced Topic] 윈폼이나 WPF 같은 UI 프로그램은 await가 실행되기 전에 당시 실행되고 있는 쓰레드를 캡쳐해서
SynchronizationContext 에 가지고 있으며, await가 끝난 후에 이 컨텍스트로부터 원래 쓰레드 맥락에서 다음 문장들을
실행하게 한다. 하지만, 콘솔 프로그램이나 윈도우즈 서비스 프로그램의 경우에는 SynchronizationContext가 디폴트로 null
이 되어, await 이후의 문장들을 실행할 때 Thread Pool에서 작업 쓰레드를 가져와 실행하게 된다. 아래 예제는 awiat 실행
이전에 SynchronizationContext.Current 가 null 임을 체크하고 있으며, 또한 await 이후에 쓰레드가 작업
쓰레드임을 ManagedThreadId 속성을 통해 확인해 보는 것이다.  
  

##  예제

    
    

    // 예제5

    //using System;

    //using System.Threading;

    //using System.Threading.Tasks;

    

    static void Main(string[] args)

    {            

        Console.WriteLine("Main:" + Thread.CurrentThread.ManagedThreadId);

        Run();

        Console.ReadLine();

    }

    

    private async void Run()

    {

        // 비동기로 Worker Thread에서 도는 task1

        var task1 = Task.Run(() => LongCalcAsync(10));

    

        // 콘솔프로그램인 경우 SynchronizationContext가 null

        Console.WriteLine(SynchronizationContext.Current);

    

        // task1이 끝나길 기다렸다가 끝나면 결과치를 sum에 할당

        int sum = await task1;

    

        // Worker Thread 에서 실행

        Console.WriteLine(sum);

        Console.WriteLine(Thread.CurrentThread.ManagedThreadId);

    }

    

    private int LongCalcAsync(int times)

    {

        int result = 0;

        for (int i = 0; i < times; i++)

        {

            result += i;

            Thread.Sleep(1000); 

        }

        return result;

    }

    

* * *

본 웹사이트는 광고를 포함하고 있습니다. 광고 클릭에서 발생하는 수익금은 모두 웹사이트 서버의 유지 및 관리, 그리고 기술 콘텐츠 향상을
위해 쓰여집니다.

﻿


-->

<!--






-->

