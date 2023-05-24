---
title: "[C#] CancellationTokenSource 클래스 사용법"
category: 
- CSharp
tag:
- CSharp
# header:
#   teaser: /assets/images/git-story.png
marp: true
---

# CancellationTokenSource 이란

작업의 가능한 취소를 처리하기 위해 예제에서는 개체에 전달되는 취소 토큰을 생성하는 개체를 TaskFactory 인스턴스화 CancellationTokenSource 합니다. 개체는 TaskFactory 취소 토큰을 특정 계측에 대한 판독값 수집을 담당하는 각 작업에 전달합니다. 

---

# 예제 코드

```csharp
CancellationTokenSource source = new CancellationTokenSource();
CancellationToken token = source.Token;
TaskFactory factory = new TaskFactory(token);

// when
bool itShouldNotBeTrue = false;

factory.StartNew(async () =>
{
	Console.WriteLine("Task Start");
	await Task.Delay(1000);
	// if (cancelSource.Token.IsCancellationRequested)
	// {
	//     return;
	// }
	await Task.Delay(1000);
	itShouldNotBeTrue = true;
	Console.WriteLine("Task End : " + itShouldNotBeTrue.ToString());
}, source.Token);
Thread.Sleep(100);
source.Cancel();
Console.WriteLine("Task Cancel : " + itShouldNotBeTrue.ToString());
Thread.Sleep(3000);
```

---

# 예제 설명

위의 코드에 대한 결과값은 아래와 같다.

```
Task Start
Task Cancel : False
Task End : True
```

---

# 해결 방법

```source.Token```을 사용하면 factory.StartNew로 실행한 스레드를 다 실행하는것을 확인 할 수 있다. 따라서 아래와 같이 Task.Delay()에서 CancellationTokenSource을 인식 할 수 있도록 해야 한다.

```
await Task.Delay(1000, token); 
```