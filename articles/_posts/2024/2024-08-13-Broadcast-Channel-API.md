---
title: "[WebDevelopment] Broadcast Channel API로 브라우저 간 통신하기"
categories: webdevelopment
tags:
- BroadcastChannel
- WebAPI
- JavaScript
- RealTimeCommunication
- WebDevelopment
- Frontend
- WebApplications
- Messaging
- BrowserContexts
- Tabs
- Windows
- Iframes
- Frames
- UserSessions
- ThemePreferences
- Synchronization
- EventListener
- PostMessage
- Communication
- WebWorkers
- ServiceWorkers
- LocalStorage
- IndexedDB
- PubSub
- React
- Hooks
- StateManagement
- CrossTabCommunication
- WebSockets
- Performance
- API
- Development
- Coding
- Programming
- SoftwareEngineering
- UserExperience
- Collaboration
- Updates
- Notifications
- DataTransfer
- ClientSide
- WebStandards
- BrowserCompatibility
- Debugging
- CodeExample
- HandsOn
- Tutorial
- Learning
- Technology
- Innovation
- SoftwareDevelopment
- OpenSource
header:
teaser: /assets/images/undefined/teaser.jpg
---

현대 웹 애플리케이션에서 서로 다른 브라우저 컨텍스트(탭, 창, 프레임 또는 iframe 등) 간의 통신은 사용자 세션의 일관성을 유지하고, 업데이트를 전파하며, 협업 기능을 가능하게 하는 데 필수적이다. Broadcast Channel API는 개발자가 이러한 컨텍스트 간의 실시간 통신을 최소한의 오버헤드로 달성할 수 있도록 해주는 간단하면서도 강력한 도구이다. 이 블로그에서는 Broadcast Channel API의 작동 방식, 실제 사용 사례를 살펴보고, 구현을 보여주는 실습 예제를 제공할 것이다. Broadcast Channel API는 동일한 출처 내에서 서로 다른 브라우징 컨텍스트 간의 통신을 가능하게 해주는 메시징 API이다. postMessage와 같은 다른 메시징 기술과 달리, Broadcast Channel API는 특정 창이나 프레임에 대한 참조를 유지할 필요 없이 통신을 단순화한다. 이 API는 여러 개의 열린 창이나 탭에 정보를 방송해야 할 때 특히 유용하다. Broadcast Channel API를 사용하면 메시지를 보내고 받을 수 있는 채널을 생성하고, 해당 채널에 구독하여 메시지를 수신할 수 있다. 이 API는 사용이 간편하여 여러 창이나 탭을 동기화해야 할 때 이상적인 선택이다.


|![]()|
|:---:|
||


<!--
##### Outline #####
-->

<!--
---
## Broadcast Channel API 개요
**Broadcast Channel API란?**  
**Broadcast Channel API의 필요성**  
**Broadcast Channel API의 장점**  
**Broadcast Channel API의 사용 사례**

## Broadcast Channel API의 작동 원리
**채널 생성하기**  
**메시지 수신하기**  
**메시지 전송하기**  

## 실용적인 예제
**탭 간 테마 동기화 예제**  
**카운터 애플리케이션 예제**  
**React에서의 Broadcast Channel 사용 예제**  

## Broadcast Channel API의 한계
**동일 출처 제한**  
**대량 데이터 전송의 비효율성**  
**브라우저 호환성 문제**  

## 자주 묻는 질문
**Broadcast Channel API는 어떤 상황에서 사용해야 하나요?**  
**Broadcast Channel API와 다른 메시징 API의 차이점은 무엇인가요?**  
**Broadcast Channel API의 보안 문제는 무엇인가요?**  

## 관련 기술
**WebSockets**  
**Service Workers**  
**Local Storage**  

## 결론
**Broadcast Channel API의 요약**  
**미래의 웹 애플리케이션에서의 역할**  
**개발자에게의 권장 사항**  

---
-->

<!--
---
## Broadcast Channel API 개요
**Broadcast Channel API란?**  
**Broadcast Channel API의 필요성**  
**Broadcast Channel API의 장점**  
**Broadcast Channel API의 사용 사례**
-->

## Broadcast Channel API 개요

**Broadcast Channel API란?**  

Broadcast Channel API는 웹 애플리케이션 간에 메시지를 전송할 수 있는 간단한 방법을 제공하는 API이다. 이 API는 동일한 출처의 여러 탭이나 창 간에 데이터를 공유할 수 있도록 해준다. 이를 통해 개발자는 사용자 경험을 향상시키고, 여러 탭에서의 상태 동기화를 쉽게 구현할 수 있다.

**Broadcast Channel API의 필요성**  

현대의 웹 애플리케이션은 종종 여러 탭이나 창에서 동시에 열리게 된다. 이때 각 탭 간의 상태를 동기화하는 것은 사용자에게 일관된 경험을 제공하는 데 필수적이다. 예를 들어, 사용자가 한 탭에서 설정을 변경하면 다른 탭에서도 동일한 설정이 반영되어야 한다. Broadcast Channel API는 이러한 요구를 충족시키기 위해 설계되었다.

**Broadcast Channel API의 장점**  

Broadcast Channel API의 주요 장점은 다음과 같다. 첫째, 사용이 간편하다. 복잡한 설정 없이도 간단한 코드로 메시지를 전송하고 수신할 수 있다. 둘째, 성능이 우수하다. 다른 방법에 비해 낮은 지연 시간으로 메시지를 전달할 수 있다. 셋째, 다양한 사용 사례에 적용할 수 있다. 예를 들어, 실시간 협업 애플리케이션이나 게임 등에서 유용하게 사용될 수 있다.

**Broadcast Channel API의 사용 사례**  

Broadcast Channel API는 여러 가지 상황에서 유용하게 사용될 수 있다. 예를 들어, 사용자가 여러 탭에서 동일한 애플리케이션을 사용할 때, 각 탭의 상태를 동기화하여 일관된 사용자 경험을 제공할 수 있다. 또한, 실시간 채팅 애플리케이션에서 메시지를 전송하고 수신하는 데에도 활용될 수 있다. 이 외에도 다양한 웹 애플리케이션에서 상태 관리 및 데이터 동기화에 유용하게 사용될 수 있다.

<!--
## Broadcast Channel API의 작동 원리
**채널 생성하기**  
**메시지 수신하기**  
**메시지 전송하기**  
-->

## Broadcast Channel API의 작동 원리

**채널 생성하기**  

Broadcast Channel API를 사용하기 위해서는 먼저 채널을 생성해야 한다. 채널은 이름을 통해 구분되며, 동일한 이름을 가진 채널은 서로 연결된다. 채널을 생성하는 방법은 다음과 같다.

```javascript
const channel = new BroadcastChannel('my_channel');
```

위의 코드에서 'my_channel'은 채널의 이름이다. 이 이름을 통해 다른 스크립트나 탭에서 동일한 채널에 접근할 수 있다. 채널을 생성한 후에는 메시지를 주고받을 준비가 완료된다.

**메시지 수신하기**  

메시지를 수신하기 위해서는 `onmessage` 이벤트 리스너를 설정해야 한다. 이 리스너는 다른 탭이나 스크립트에서 전송된 메시지를 수신할 수 있도록 해준다. 다음은 메시지를 수신하는 예제 코드이다.

```javascript
channel.onmessage = (event) => {
    console.log('Received message:', event.data);
};
```

위의 코드에서 `event.data`는 수신된 메시지를 나타낸다. 이 메시지는 다른 탭에서 전송된 데이터로, 이를 통해 실시간으로 정보를 공유할 수 있다.

**메시지 전송하기**  

메시지를 전송하는 것은 매우 간단하다. `postMessage` 메서드를 사용하여 원하는 데이터를 전송할 수 있다. 다음은 메시지를 전송하는 예제 코드이다.

```javascript
channel.postMessage('Hello from another tab!');
```

위의 코드에서 'Hello from another tab!'이라는 문자열이 다른 탭으로 전송된다. 수신 측에서는 이 메시지를 `onmessage` 이벤트 리스너를 통해 받을 수 있다. 이를 통해 여러 탭 간의 실시간 통신이 가능해진다.

---

이와 같이 Broadcast Channel API는 간단한 방법으로 여러 탭 간의 메시지를 주고받을 수 있는 기능을 제공한다. 이를 통해 웹 애플리케이션의 사용자 경험을 향상시킬 수 있다.

<!--
## 실용적인 예제
**탭 간 테마 동기화 예제**  
**카운터 애플리케이션 예제**  
**React에서의 Broadcast Channel 사용 예제**  
-->

## 실용적인 예제

**탭 간 테마 동기화 예제**  

탭 간 테마 동기화 예제는 사용자가 여러 개의 브라우저 탭을 열고 있을 때, 한 탭에서 테마를 변경하면 다른 탭에서도 자동으로 변경되는 기능을 구현하는 것이다. 이 예제는 사용자가 웹 애플리케이션을 사용할 때 일관된 사용자 경험을 제공하는 데 유용하다. 

아래는 이 기능을 구현하기 위한 간단한 코드 예제이다.

```javascript
// 채널 생성
const channel = new BroadcastChannel('theme_channel');

// 테마 변경 함수
function changeTheme(theme) {
    document.body.className = theme;
    channel.postMessage(theme); // 메시지 전송
}

// 메시지 수신
channel.onmessage = (event) => {
    changeTheme(event.data); // 수신한 메시지로 테마 변경
};

// 버튼 클릭 시 테마 변경
document.getElementById('light-theme').onclick = () => changeTheme('light');
document.getElementById('dark-theme').onclick = () => changeTheme('dark');
```

이 코드는 사용자가 버튼을 클릭하여 테마를 변경할 때마다 `BroadcastChannel`을 통해 다른 탭에 변경 사항을 전파하는 방식으로 작동한다.

**카운터 애플리케이션 예제**  

카운터 애플리케이션 예제는 사용자가 여러 탭에서 카운터 값을 증가시키거나 감소시킬 때, 모든 탭에서 카운터 값이 동기화되는 기능을 구현하는 것이다. 이 예제는 실시간으로 데이터를 공유해야 하는 애플리케이션에서 유용하다.

![](/plantuml/broadcast-channel-api-ex2.svg)

아래는 카운터 애플리케이션을 구현하기 위한 코드 예제이다.

```javascript
let count = 0;
const channel = new BroadcastChannel('counter_channel');

// 카운터 업데이트 함수
function updateCounter() {
    document.getElementById('counter').innerText = count;
    channel.postMessage(count); // 메시지 전송
}

// 메시지 수신
channel.onmessage = (event) => {
    count = event.data; // 수신한 메시지로 카운터 값 업데이트
    updateCounter();
};

// 버튼 클릭 시 카운터 증가 및 감소
document.getElementById('increment').onclick = () => {
    count++;
    updateCounter();
};

document.getElementById('decrement').onclick = () => {
    count--;
    updateCounter();
};
```

이 코드는 사용자가 카운터를 증가시키거나 감소시킬 때마다 `BroadcastChannel`을 통해 다른 탭에 카운터 값을 전파하는 방식으로 작동한다.

**React에서의 Broadcast Channel 사용 예제**  

React 애플리케이션에서 `BroadcastChannel`을 사용하는 방법은 다음과 같다. 이 예제에서는 상태 관리 라이브러리 없이 React의 상태를 사용하여 간단한 카운터 애플리케이션을 구현한다.

```javascript
import React, { useEffect, useState } from 'react';

const Counter = () => {
    const [count, setCount] = useState(0);
    const channel = new BroadcastChannel('counter_channel');

    useEffect(() => {
        channel.onmessage = (event) => {
            setCount(event.data); // 수신한 메시지로 카운터 값 업데이트
        };

        return () => {
            channel.close(); // 컴포넌트 언마운트 시 채널 닫기
        };
    }, [channel]);

    const increment = () => {
        setCount((prevCount) => {
            const newCount = prevCount + 1;
            channel.postMessage(newCount); // 메시지 전송
            return newCount;
        });
    };

    const decrement = () => {
        setCount((prevCount) => {
            const newCount = prevCount - 1;
            channel.postMessage(newCount); // 메시지 전송
            return newCount;
        });
    };

    return (
        <div>
            <h1>Count: {count}</h1>
            <button onClick={increment}>Increment</button>
            <button onClick={decrement}>Decrement</button>
        </div>
    );
};

export default Counter;
```

이 코드는 React의 상태 관리 기능을 활용하여 카운터 값을 관리하고, `BroadcastChannel`을 통해 다른 탭과 동기화하는 방식으로 작동한다.

<!--
## Broadcast Channel API의 한계
**동일 출처 제한**  
**대량 데이터 전송의 비효율성**  
**브라우저 호환성 문제**  
-->

## Broadcast Channel API의 한계

**동일 출처 제한**  

Broadcast Channel API는 동일 출처 정책에 따라 작동한다. 이는 같은 출처에서만 메시지를 주고받을 수 있다는 의미이다. 즉, 서로 다른 도메인이나 프로토콜을 사용하는 웹 페이지 간에는 메시지를 전송할 수 없다. 이러한 제한은 보안상의 이유로 설정되었지만, 개발자에게는 불편함을 초래할 수 있다. 예를 들어, 여러 서브도메인에서 애플리케이션을 운영하는 경우, 각 서브도메인 간의 데이터 동기화가 어려워질 수 있다. 

**대량 데이터 전송의 비효율성**  

Broadcast Channel API는 주로 작은 크기의 메시지를 전송하는 데 적합하다. 대량의 데이터를 전송할 경우, 성능 저하가 발생할 수 있다. 이는 메시지가 여러 번 전송되거나, 수신 측에서 데이터를 처리하는 데 시간이 걸릴 수 있기 때문이다. 따라서 대량의 데이터를 전송해야 하는 경우, 다른 방법을 고려하는 것이 좋다. 예를 들어, WebSockets나 Fetch API를 사용하여 데이터를 전송하는 것이 더 효율적일 수 있다.

**브라우저 호환성 문제**  

Broadcast Channel API는 모든 브라우저에서 지원되지 않는다. 특히 구형 브라우저나 일부 모바일 브라우저에서는 이 API를 사용할 수 없다. 따라서 개발자는 애플리케이션의 사용자 기반을 고려하여 이 API를 사용할지 여부를 결정해야 한다. 만약 특정 브라우저에서 지원되지 않는다면, 대체 방법을 마련해야 한다. 예를 들어, Local Storage나 Cookies를 사용하여 데이터를 동기화하는 방법이 있다. 

이러한 한계에도 불구하고, Broadcast Channel API는 간단한 메시징 기능을 제공하며, 특정 상황에서는 매우 유용하게 사용될 수 있다. 개발자는 이러한 한계를 이해하고, 적절한 상황에서 이 API를 활용해야 한다.

<!--
## 자주 묻는 질문
**Broadcast Channel API는 어떤 상황에서 사용해야 하나요?**  
**Broadcast Channel API와 다른 메시징 API의 차이점은 무엇인가요?**  
**Broadcast Channel API의 보안 문제는 무엇인가요?**  
-->

## 자주 묻는 질문

**Broadcast Channel API는 어떤 상황에서 사용해야 하나요?**  

Broadcast Channel API는 여러 탭이나 창에서 동일한 웹 애플리케이션을 사용할 때, 데이터나 상태를 동기화해야 할 필요가 있을 때 유용하다. 예를 들어, 사용자가 여러 탭에서 같은 웹사이트를 열고 있을 때, 한 탭에서의 변경 사항을 다른 탭에 즉시 반영하고 싶을 때 사용할 수 있다. 이 API는 특히 실시간 협업 애플리케이션이나 게임, 채팅 애플리케이션 등에서 효과적이다.

**Broadcast Channel API와 다른 메시징 API의 차이점은 무엇인가요?**  

Broadcast Channel API는 동일 출처의 여러 탭 간에 메시지를 전송할 수 있는 간단한 방법을 제공한다. WebSockets와 같은 다른 메시징 API는 서버와 클라이언트 간의 양방향 통신을 지원하지만, Broadcast Channel API는 클라이언트 간의 통신에 중점을 둔다. 또한, Local Storage와 같은 다른 저장소 API는 데이터 저장 및 검색에 중점을 두지만, Broadcast Channel API는 실시간 메시징에 초점을 맞춘다. 이러한 차이점으로 인해 각 API는 특정 상황에서 더 적합하게 사용될 수 있다.

**Broadcast Channel API의 보안 문제는 무엇인가요?**  

Broadcast Channel API는 동일 출처 정책을 따르기 때문에, 서로 다른 출처의 웹 페이지 간에는 메시지를 전송할 수 없다. 그러나 동일 출처 내에서의 사용은 보안상의 위험이 있을 수 있다. 예를 들어, 악의적인 스크립트가 Broadcast Channel을 통해 다른 탭의 데이터를 엿볼 수 있는 가능성이 있다. 따라서 개발자는 이 API를 사용할 때 보안에 대한 충분한 고려가 필요하며, 민감한 데이터는 다른 방법으로 보호해야 한다.

<!--
## 관련 기술
**WebSockets**  
**Service Workers**  
**Local Storage**  
-->

## 관련 기술

**WebSockets**  

WebSockets는 클라이언트와 서버 간의 양방향 통신을 가능하게 하는 프로토콜이다. HTTP 프로토콜과는 달리, WebSockets는 지속적인 연결을 유지하며 실시간 데이터 전송을 지원한다. 이는 채팅 애플리케이션이나 실시간 게임과 같은 애플리케이션에서 매우 유용하다. WebSockets는 Broadcast Channel API와 함께 사용될 수 있으며, 두 기술 모두 클라이언트 간의 데이터 전송을 효율적으로 처리할 수 있다. 그러나 WebSockets는 서버와의 연결이 필요하므로, 동일 출처 정책을 따르지 않는 경우에도 사용할 수 있다.

**Service Workers**  

Service Workers는 웹 애플리케이션의 백그라운드에서 실행되는 스크립트로, 오프라인 기능 및 푸시 알림과 같은 기능을 제공한다. Service Workers는 네트워크 요청을 가로채고, 캐시를 관리하며, 사용자에게 푸시 알림을 보낼 수 있다. Broadcast Channel API와 함께 사용하면, Service Workers가 여러 탭 간의 상태를 동기화하는 데 도움을 줄 수 있다. 예를 들어, 사용자가 오프라인 상태에서 작업을 수행할 때, Service Workers는 데이터를 캐시하고, 온라인 상태로 돌아왔을 때 Broadcast Channel을 통해 다른 탭과 동기화할 수 있다.

**Local Storage**  

Local Storage는 웹 브라우저에 데이터를 저장할 수 있는 간단한 방법을 제공하는 API이다. Local Storage는 키-값 쌍으로 데이터를 저장하며, 브라우저가 종료되더라도 데이터가 유지된다. Broadcast Channel API와 함께 사용하면, Local Storage에 저장된 데이터를 여러 탭 간에 동기화할 수 있다. 예를 들어, 사용자가 한 탭에서 설정을 변경하면, Broadcast Channel을 통해 다른 탭에 변경 사항을 전파할 수 있다. 그러나 Local Storage는 동기화가 즉각적이지 않으며, 데이터의 크기 제한이 있으므로 대량의 데이터를 처리하는 데는 적합하지 않다.

이와 같이, WebSockets, Service Workers, Local Storage는 각각의 장점과 용도가 있으며, Broadcast Channel API와 함께 사용하여 웹 애플리케이션의 기능을 확장할 수 있다. 이러한 기술들은 현대 웹 개발에서 중요한 역할을 하며, 개발자들은 이들을 적절히 활용하여 사용자 경험을 향상시킬 수 있다.

<!--
## 결론
**Broadcast Channel API의 요약**  
**미래의 웹 애플리케이션에서의 역할**  
**개발자에게의 권장 사항**  
-->

## 결론

**Broadcast Channel API의 요약**  

Broadcast Channel API는 웹 애플리케이션에서 여러 탭 간의 통신을 가능하게 하는 유용한 도구이다. 이 API를 사용하면 동일한 출처의 여러 브라우저 탭이나 창에서 메시지를 쉽게 전송하고 수신할 수 있다. 이를 통해 사용자 경험을 향상시키고, 애플리케이션의 상태를 동기화하는 데 큰 도움이 된다. 

**미래의 웹 애플리케이션에서의 역할**  

미래의 웹 애플리케이션에서는 사용자 경험이 더욱 중요해질 것이다. Broadcast Channel API는 이러한 변화에 발맞추어 여러 탭 간의 실시간 통신을 지원함으로써, 사용자에게 더 나은 경험을 제공할 수 있다. 특히, 실시간 데이터 업데이트가 필요한 애플리케이션에서 이 API의 활용도가 높아질 것으로 예상된다. 

**개발자에게의 권장 사항**  

개발자들은 Broadcast Channel API를 활용하여 애플리케이션의 상태를 효율적으로 관리하고, 사용자 간의 상호작용을 개선할 수 있다. 그러나 이 API의 한계와 브라우저 호환성 문제를 항상 염두에 두어야 한다. 따라서, 다른 메시징 기술과 함께 사용하여 최적의 솔루션을 찾는 것이 중요하다. 

이와 같은 방식으로 Broadcast Channel API를 이해하고 활용하면, 더욱 발전된 웹 애플리케이션을 개발할 수 있을 것이다.

<!--
##### Reference #####
-->

## Reference


* [https://dev.to/rigalpatel001/how-to-use-the-broadcast-channel-api-for-real-time-communication-across-browser-windows-23if](https://dev.to/rigalpatel001/how-to-use-the-broadcast-channel-api-for-real-time-communication-across-browser-windows-23if)
* [https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API](https://developer.mozilla.org/en-US/docs/Web/API/Broadcast_Channel_API)
* [https://dev-record-levelup.tistory.com/6](https://dev-record-levelup.tistory.com/6)
* [https://developer.mozilla.org/en-US/docs/Web/API/BroadcastChannel](https://developer.mozilla.org/en-US/docs/Web/API/BroadcastChannel)
* [https://devblog.kakaostyle.com/ko/2022-10-12-1-sync-data-between-activities/](https://devblog.kakaostyle.com/ko/2022-10-12-1-sync-data-between-activities/)
* [https://idleday.tistory.com/93](https://idleday.tistory.com/93)


<!--
In modern web applications, communication between different browser contexts
(such as tabs, windows, frames, or iframes) is essential, especially for
maintaining consistency in user sessions, broadcasting updates, or enabling
collaborative features. The Broadcast Channel API is a straightforward yet
powerful tool that allows developers to achieve real-time communication across
these contexts with minimal overhead.

In this blog, we'll explore how the Broadcast Channel API works, dive into its
practical use cases, and provide a hands-on example to demonstrate its
implementation.

##  What is the Broadcast Channel API?

The Broadcast Channel API is a messaging API that enables communication
between different browsing contexts within the same origin. Unlike other
messaging techniques like postMessage, which requires maintaining references
to specific windows or frames, the Broadcast Channel API simplifies
communication by creating a channel that any context can join or leave freely.

This API is particularly useful for scenarios where you need to broadcast
information to multiple open windows or tabs without worrying about managing
connections between them.

##  How Does It Work?

Using the Broadcast Channel API involves three key steps:

**1\. Creating a Channel:** You create a new broadcast channel using the
BroadcastChannel constructor, passing in a channel name.

**2\. Listening for Messages:** You set up an event listener to listen for
messages broadcasted on the channel.

**3.Sending Messages:** You broadcast messages to all contexts subscribed to
the channel.

Here’s a quick example to illustrate these steps.

###  Example: Synchronizing Theme Preferences Across Tabs

Let’s say you have a web application where users can switch between light and
dark themes. If a user changes the theme in one tab, you want that change to
immediately reflect in all other open tabs.  

    
    
    // Step 1: Create a Broadcast Channel
    const themeChannel = new BroadcastChannel('theme');
    
    // Step 2: Listen for messages on the channel
    themeChannel.onmessage = (event) => {
        document.body.className = event.data; // Apply the received theme
        console.log(`Theme changed to: ${event.data}`);
    };
    
    // Function to toggle between themes
    function toggleTheme() {
        const currentTheme = document.body.className;
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.body.className = newTheme;
    
        // Step 3: Broadcast the new theme to other tabs
        themeChannel.postMessage(newTheme);
    }
    
    // Example of toggling theme
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    
    

Enter fullscreen mode  Exit fullscreen mode

###  Limitations

While the Broadcast Channel API is incredibly useful, it's important to note
that:

  * It only works across contexts within the same origin. 
  * It's not designed for large-scale, high-frequency data transfer (for which you might consider using WebSockets or Service Workers). 

_The Broadcast Channel API is a powerful yet simple tool for enabling real-
time communication across different browser contexts. Its ease of use makes it
an ideal choice for scenarios where you need to keep multiple windows or tabs
in sync without diving into complex messaging setups._


-->

<!--






-->

<!--
The **Broadcast Channel API** allows basic communication between [ browsing
contexts ](/en-US/docs/Glossary/Browsing_context) (that is, _windows_ , _tabs_
, _frames_ , or _iframes_ ) and workers on the same [ origin ](/en-
US/docs/Glossary/Origin) .

**Note:** To be exact, communication is allowed between browsing contexts
using the same [ storage partition ](/en-
US/docs/Web/Privacy/State_Partitioning) . Storage is first partitioned
according to top-level sites—so for example, if you have one opened page at `
a.com ` that embeds an iframe from ` b.com ` , and another page opened to `
b.com ` , then the iframe cannot communicate with the second page despite them
being technically same-origin. However, if the first page is also on ` b.com `
, then the iframe can communicate with the second page.

By creating a [ ` BroadcastChannel ` ](/en-US/docs/Web/API/BroadcastChannel)
object, you can receive any messages that are posted to it. You don't have to
maintain a reference to the frames or workers you wish to communicate with:
they can "subscribe" to a particular channel by constructing their own [ `
BroadcastChannel ` ](/en-US/docs/Web/API/BroadcastChannel) with the same name,
and have bi-directional communication between all of them.

![The principle of the Broadcast Channel
API](https://developer.mozilla.org/en-
US/docs/Web/API/Broadcast_Channel_API/broadcastchannel.png)


-->

<!--






-->

<!--
##  **\- BroadcastChannel이란?**

  * Broadcast Channel API는 브라우징 컨텍스트 간의 통신을 보다 쉽게 ​​해주는 간단한 API이다. 
  * 즉, 창/탭, iframe, 웹 작업자 및 서비스 작업자 간의 통신이며, 지정된 채널에 게시된 메시지는 해당 채널의 _**모든 청취자** _ 에게 전달된다. 
  * BroadcastChannel생성자는 _**채널 이름** _ 이라는 단일 매개변수를 사용한다 . 이름은 채널을 식별하고 브라우징 컨텍스트 전반에 존재한다. 

##  **\- 사용방법**

  * 채널을 오픈한 다음 메세지를 보내면, 해당 채널을 구독하는 컨텍스트에서 메세지를 받아볼 수 있다. 
  * 아래처럼 채널을 생성할 수 있다. 만약 처음이면 생성되고, 이미 생성된 채널이면 구독하게 된다. 

    
    
    // my_bus 라는 채널에 연결한다.
    const channel = new BroadcastChannel('my_bus');

  * 메세지를 보낼 때는 postMessage라는 메서드를 사용한다. 메세지의 형식은 정해져 있지 않고 [ structed clone algorithm ](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm) 을 사용해서 시리얼라이즈되므로 웬만한 데이터 타입은 다 쓸 수 있다. 
  * 메세지가 포스팅되면 브로드캐스트 채널로 메세지 이벤트가 실행된다. 메세지 이벤트가 발생했을 때 실행할 콜백은 아래처럼 달아두면 된다. 

    
    
    // my_bus에 메시지를 보낸다.
    channel.postMessage('This is a test message.'); 
    
    // my_bus에서 메시지를 수신한다.
    channel.onmessage = function(e) {
        console.log('Received', e.data);
    };
    
    // 완료되면 채널을 닫는다.
    channel.close();

##  **\- 주의점**

  * 단, 자신이 포스팅한 메세지는 자신이 받아볼 수 없다. 즉 포스팅을 한 페이지한테는 message이벤트가 실행되지 않는다. 
  * 창 중 하나가 시크릿 모드이거나 여러 브라우저에서 (예: Firefox에서 Chrome으로)브로드캐스트 채널이 작동하지 않는다. 
  * Broadcast Channel API는 아래처럼 호스트가 다르면 작동하지 않는다.    
[ https://www.abc.com/ ](https://www.abc.com/)  
[ https://abc.com/ ](https://abc.com/)

##

##  **\- 다른 기능과의 차이점**

  * [ Channel Messaging API ](https://developer.mozilla.org/en-US/docs/Web/API/Channel_Messaging_API) 와 차이점은 기본적으로 broadcastchannel은 one-to-many를 위한 것이고 messagechannel는 one-to-one을 위한 것이라는 점이다. 
  * window.postMessage 와의 차이점은, broadcastchannel은 same origin만 지원하지만 window.postMessage는 그렇지 않다는 점이다. 그리고 window.postMessage는 타켓 윈도우의 참조도 알고 있어야 하는 반면 broadcastchannel은 채널 이름으로 구독하고 양방향 소통이 가능해서 사용이 훨씬 쉽다. 

* * *

> **_ Reference  
>  _ ** _  
>  [ https://developer-alle.tistory.com/m/433 ](https://developer-
> alle.tistory.com/m/433)  
>  [ https://developer.chrome.com/blog/broadcastchannel/
> ](https://developer.chrome.com/blog/broadcastchannel/)  
>  _
>
> _ [ https://hjcode.tistory.com/100 ](https://hjcode.tistory.com/100) _


-->

<!--






-->

<!--
#  BroadcastChannel

##  Baseline  2022

Newly available

The **` BroadcastChannel ` ** interface represents a named channel that any [
browsing context ](/en-US/docs/Glossary/Browsing_context) of a given [ origin
](/en-US/docs/Glossary/Origin) can subscribe to. It allows communication
between different documents (in different windows, tabs, frames or iframes) of
the same origin. Messages are broadcasted via a [ ` message ` ](/en-
US/docs/Web/API/BroadcastChannel/message_event "message") event fired at all `
BroadcastChannel ` objects listening to the channel, except the object that
sent the message.

EventTarget  BroadcastChannel

_This interface also inherits methods from its parent,[ ` EventTarget ` ](/en-
US/docs/Web/API/EventTarget) . _

[ ` BroadcastChannel.postMessage() ` ](/en-
US/docs/Web/API/BroadcastChannel/postMessage)

    

Sends the message, of any type of object, to each ` BroadcastChannel ` object
listening to the same channel.

[ ` BroadcastChannel.close() ` ](/en-US/docs/Web/API/BroadcastChannel/close)

    

Closes the channel object, indicating it won't get any new messages, and
allowing it to be, eventually, garbage collected.

_This interface also inherits events from its parent,[ ` EventTarget ` ](/en-
US/docs/Web/API/EventTarget) . _

[ ` message ` ](/en-US/docs/Web/API/BroadcastChannel/message_event "message")

    

Fired when a message arrives on the channel. Also available via the `
onmessage ` property.

[ ` messageerror ` ](/en-US/docs/Web/API/BroadcastChannel/messageerror_event
"messageerror")

    

Fired when a message arrives that can't be deserialized. Also available via
the ` onmessageerror ` property.

BCD tables only load in the browser  with JavaScript enabled. Enable
JavaScript to view data.


-->

<!--






-->

<!--
ì•ˆë…•í•˜ì„¸ìš”! ğŸ‘‹ ì¹´ì¹´ì˜¤ìŠ¤íƒ€ì�¼ í”„ë¡ íŠ¸ì—”ë“œ ì±•í„° ì†Œì†� Jason(ì
œì�´ìŠ¨/í™©ì£¼ì„±)ì�…ë‹ˆë‹¤.

ì—¬ëŸ¬ë¶„ì�€ í˜¹ì‹œ ì„œë¹„ìŠ¤ë¥¼ ê°œë°œí•˜ë©´ì„œ ë¸Œë�¼ìš°ì €ì�˜ ìœˆë�„ìš°,
íƒ­ í˜¹ì�€ ì›¹ë·° ì•¡í‹°ë¹„í‹° ê°„ ë�°ì�´í„°ë¥¼ ë�™ê¸°í™” í•´ì¤˜ì•¼ í–ˆë�˜
ê²½í—˜ì�´ ì�ˆìœ¼ì‹ ê°€ìš”?

í�˜ì�´ìŠ¤ë¶�ì�´ë‚˜ ì�¸ìŠ¤íƒ€ê·¸ë�¨ê³¼ ê°™ì�´ ì‚¬ìš©ì��ê°€ ìƒ�ì„¸
í�˜ì�´ì§€ì—�ì„œ ê²Œì‹œë¬¼ ì¢‹ì•„ìš”ë¥¼ ëˆ„ë¥¸ ë’¤ì—� íƒ€ì�„ë�¼ì�¸ í™”ë©´ìœ¼ë¡œ
ë�Œì•„ì™”ì�„ ë•Œ í•´ë‹¹ ë³€ê²½ ë‚´ìš©ì�´ ë°˜ì˜�ë�œ ê²½ìš°ë¥¼ ì˜ˆë¥¼ ë“¤ ìˆ˜
ì�ˆì�„ ê²ƒ ê°™ìŠµë‹ˆë‹¤.

ì�‘ë…„ ì´ˆ ì˜¤í”ˆí•œ ì§€ê·¸ì�¬ê·¸ ì—�í”½ ì„œë¹„ìŠ¤ì—�ì„œë�„ ì�´ì™€ ë¹„ìŠ·í•œ
ê¸°ëŠ¥ì�´ ë“¤ì–´ê°”ëŠ”ë�°ìš”, ì•± ë‚´ ì„œë¹„ìŠ¤ë¥¼ ì œê³µí•˜ë©´ì„œ ê°€ëŠ¥í•œ
ë„¤ì�´í‹°ë¸Œ ì•±ì�„ ì‚¬ìš©í•˜ëŠ” ë“¯í•œ ê²½í—˜ì�„ ì£¼ê¸° ìœ„í•´ í�˜ì�´ì§€
ì�´ë�™ ì‹œ ì•± ì�¸í„°í�˜ì�´ìŠ¤ë¥¼ í†µí•´ ìƒˆë¡œìš´ ì›¹ë·° ì•¡í‹°ë¹„í‹°ì™€
í•¨ê»˜ í�˜ì�´ì§€ë¥¼ ë³´ì—¬ì£¼ëŠ” ë°©ì‹�ì�„ ì �ìš©í•˜ê²Œ ë�˜ì—ˆìŠµë‹ˆë‹¤.

![epick.png](https://devblog.kakaostyle.com/img/content/2022-10-12-1/epick.png)

ê·¸ëŸ¬ë‹¤ ë³´ë‹ˆ ë©”ì�¸ í™”ë©´ì—�ì„œ ê²Œì‹œë¬¼ì�„ í�´ë¦­í•˜ì—¬ ìƒˆë¡œìš´
ì•¡í‹°ë¹„í‹°ë¥¼ ì—° ë’¤ì—� ì¢‹ì•„ìš”ë¥¼ í�´ë¦­í•˜ê³ ì•¡í‹°ë¹„í‹°ë¥¼ ë‹«ê²Œ
ë��ì�„ ë•Œ ì�´ì „ì—� ì�ˆë�˜ ë©”ì�¸ í™”ë©´ì—�ì„œë�„ í•´ë‹¹ ì¢‹ì•„ìš” ìƒ�íƒœê°€
ë°˜ì˜�ë�˜ì–´ì•¼ í–ˆê³ ì�´ëŸ¬í•œ ë¶€ë¶„ì—�ì„œ ì•¡í‹°ë¹„í‹° ê°„ ë�°ì�´í„°
ë�™ê¸°í™”ê°€ í•„ìš”í•˜ê²Œ ë�˜ì—ˆìŠµë‹ˆë‹¤.

![problem.png](https://devblog.kakaostyle.com/img/content/2022-10-12-1/problem.png)

ì—¬ëŸ¬ ë°©ë²•ì�„ ì‹œë�„í•˜ë‹¤ ìµœì¢…ì �ìœ¼ë¡œ ì €ëŠ” ì�´ ë¬¸ì œë¥¼ Broadcast
Channelì�´ë�¼ëŠ” Web APIë¥¼ ì ‘í•œ ë’¤ pubkey/broadcast-channel
ë�¼ì�´ë¸ŒëŸ¬ë¦¬ë¥¼ í™œìš©í•˜ì—¬ í•´ê²°í•˜ê²Œ ë�˜ì—ˆê³ , ì˜¤ëŠ˜ì�€ ì�´
ë¶€ë¶„ì—� ëŒ€í•´ ê°„ë�µí•˜ê²Œ ì—¬ëŸ¬ë¶„ë“¤ê»˜ ê³µìœ ë“œë¦¬ë ¤ê³ í•©ë‹ˆë‹¤.

##  Broadcast Channel API

[ Broadcast Channel API ](https://developer.mozilla.org/en-
US/docs/Web/API/Broadcast_Channel_API) ë�€ ë�™ì�¼í•œ ì¶œì²˜ì—�ì„œ ì„œë¡œ
ë‹¤ë¥¸ ë¸Œë�¼ìš°ì§• ì»¨í…�ìŠ¤íŠ¸(íƒ­, ìœˆë�„ìš°, iframe ë“±)ë“¤ì�´ ì±„ë„�ì�„
ê°œì„¤í•˜ê±°ë‚˜ ì°¸ì—¬í•˜ì—¬ í•´ë‹¹ ì±„ë„�ì—�ì„œ ë©”ì‹œì§€ë¥¼ ì „ì†¡í•˜ê±°ë‚˜
ë°›ëŠ” ë“± ì–‘ë°©í–¥ í†µì‹ ì�„ ê°€ëŠ¥í•˜ê²Œ í•´ì¤�ë‹ˆë‹¤.

![Broadcast
Channel.png](https://devblog.kakaostyle.com/img/content/2022-10-12-1/broadcast_channel.png)

> ì°¸ì¡°: [ https://developer.mozilla.org/en-
> US/docs/Web/API/Broadcast_Channel_API ](https://developer.mozilla.org/en-
> US/docs/Web/API/Broadcast_Channel_API)

ê³µì‹� ë¬¸ì„œì�˜ ì˜ˆì‹œë�„ ë‚˜ì™€ ì�ˆë“¯ ì‚¬ìš©ë²•ì�´ ì •ë§� ê°„ë‹¨í•œë�°ìš”.

ë¨¼ì € ìƒˆë¡œìš´ BroadcastChannel ì�¸í„°í�˜ì�´ìŠ¤ë¥¼ ìƒ�ì„±í•´ì£¼ë©´ì„œ
ì�„ì�˜ì�˜ ì±„ë„� ì�´ë¦„ì�„ ì�¸ì��ë¡œ ë„£ì–´ì£¼ê²Œ ë�˜ë©´ ë‚´ë¶€ì—�ì„œ í•´ë‹¹
ì±„ë„�ì�„ ìƒ�ì„±í•˜ê±°ë‚˜ ì�´ë¯¸ ì—´ë ¤ì�ˆëŠ” ê²½ìš° í•´ë‹¹ ì±„ë„�ì—�
ì°¸ì—¬í•˜ê²Œ ë�©ë‹ˆë‹¤.

    
    
    const bc = new BroadcastChannel('test_app');
    

###  ë©”ì‹œì§€ ìˆ˜ì‹

ë©”ì‹œì§€ ìˆ˜ì‹ ì�€Â ` onmessage ` ë¥¼ í™œìš©í•˜ê±°ë‚˜ ` addEventListener `
ë¥¼ ì¶”ê°€í•˜ì—¬ ìˆ˜ì‹ í• ìˆ˜ ì�ˆìŠµë‹ˆë‹¤.

    
    
    // onmessage ë°©ì‹�
    bc.onmessage = function(event) {
      console.log(event);
    };
    
    // addEventListener ë°©ì‹�
    bc.addEventListener('message', function(event) {
      console.log(event);
    });
    

###  ë©”ì‹œì§€ ì „ë‹¬

ê·¸ëŸ¬ê³ ë‚˜ì„œÂ ` postMessage ` Â ë©”ì„œë“œë¥¼ í†µí•´ ë©”ì‹œì§€ë¥¼ ë³´ë‚´ë©´
ì•„ë�˜ì™€ ê°™ì�´ ê²°ê³¼ë¥¼ ì–»ì�„ ìˆ˜ ì�ˆìŠµë‹ˆë‹¤.

    
    
    bc.postMessage("Hello! I'm here!");
    

![code1.png](https://devblog.kakaostyle.com/img/content/2022-10-12-1/code1.png)

> ì„œë¡œ ë‹¤ë¥¸ ìœˆë�„ìš°ì—�ì„œ ì™¼ìª½ì�€ ë©”ì‹œì§€ë¥¼ ìˆ˜ì‹ . ì˜¤ë¥¸ìª½ì�€
> ë©”ì‹œì§€ë¥¼ ì „ë‹¬.

###  ì±„ë„� ë‹«ê¸°

` close ` Â ë©”ì„œë“œë¥¼ í˜¸ì¶œí•´ì„œ ì±„ë„�ì�„ ë‹«ê²Œ ë�˜ë©´ ì�´í›„Â `
postMessage ` ë¥¼ í†µí•´ ë©”ì‹œì§€ë¥¼ ì „ë‹¬í•´ë�„ ìˆ˜ì‹ í•˜ì§€ ì•Šê²Œ
ë�©ë‹ˆë‹¤.

![code2.png](https://devblog.kakaostyle.com/img/content/2022-10-12-1/code2.png)

##  pubkey/broadcast-channel ë�¼ì�´ë¸ŒëŸ¬ë¦¬

ë„¤ì�´í‹°ë¸Œ Web APIì�˜ ê²½ìš° [ ì§€ì›� ë¸Œë�¼ìš°ì € ìŠ¤í�™
](https://caniuse.com/broadcastchannel) ì�´ ì œí•œì �ì�´ë‹¤ ë³´ë‹ˆ
ë„¤ì�´í‹°ë¸Œ ë°©ì‹�ê³¼ í•¨ê»˜ ì¶”ê°€ë¡œ í™˜ê²½ì—� ë”°ë�¼ ë³„ë�„ localStorage,
IndexedDB ë“± ë‹¤ì–‘í•œ ë©”ì†Œë“œë¡œ ì œê³µí•´ì£¼ëŠ” [ pubkey/broadcast-
channel ](https://github.com/pubkey/broadcast-channel) ë�¼ì�´ë¸ŒëŸ¬ë¦¬ë¥¼
ì‚¬ìš©í•˜ê²Œ ë�˜ì—ˆìŠµë‹ˆë‹¤.

ë¨¼ì € íŒ¨í‚¤ì§€ë¥¼ ì„¤ì¹˜í•´ì¤�ë‹ˆë‹¤.

    
    
    # npm
    npm install broadcast-channel
    # yarn
    yarn add broadcast-channel
    

ì±„ë„� ìƒ�ì„±ì�€ ê¸°ì¡´ ë„¤ì�´í‹°ë¸Œ Web APIë�‘ ë¹„ìŠ·í•˜ë©° í•„ìš”í• ê²½ìš°
ë”°ë¡œ ì˜µì…˜ì�„ ì„¤ì •í• ìˆ˜ ì�ˆìŠµë‹ˆë‹¤.

    
    
    import { BroadcastChannel } from 'broadcast-channel';
    
    // ê¸°ë³¸ ì‚¬ìš©ë²•
    const bc = new BroadcastChannel('test_app');
    
    // ì˜µì…˜ - ë¡œì»¬ìŠ¤í† ë¦¬ì§€ ë°©ì‹�ë§Œ ì‚¬ìš©í•  ê²½ìš°
    const bc = new BroadcastChannel('test_app', {
      type: 'localstorage', // ì‚¬ìš© ë°©ì‹� ì§€ì •: 'native', 'idb', 'localstorage'
    });
    

###  ë©”ì‹œì§€ ìˆ˜ì‹

ê¸°ì¡´ ë„¤ì�´í‹°ë¸Œ Web APIì™€ ë‹¤ë¥´ê²Œ íŒŒë�¼ë¯¸í„°ê°€ ` event ` ê°€ ì•„ë‹Œ
` message ` ì�…ë‹ˆë‹¤.

    
    
    // onmessage ë°©ì‹�
    bc.onmessage = function(message) {
      console.log(message); // "Hello! I'm here!"
    };
    
    // addEventListener ë°©ì‹�
    bc.addEventListener('message', function(message) {
      console.log(message); // "Hello! I'm here!"
    });
    

###  ë©”ì‹œì§€ ì „ë‹¬ ë°� ì±„ë„� ë‹«ê¸°

ë©”ì‹œì§€ ì „ë‹¬ ë¶€ë¶„ê³¼ ì±„ë„�ì�„ ë‹«ëŠ” ë¶€ë¶„ì�€ ê¸°ì¡´ê³¼
ë�™ì�¼í•©ë‹ˆë‹¤.

    
    
    // ë©”ì‹œì§€ ì „ë‹¬
    bc.postMessage("Hello! I'm here!");
    
    
    
    // ì±„ë„� ë‹«ê¸°
    bc.close();
    

##  ë¦¬ì•¡íŠ¸ì—�ì„œ í•¨ê»˜ ì‚¬ìš©í•´ë³´ê¸°

ì�´ì œ ê°„ë‹¨í•œ ë¦¬ì•¡íŠ¸ Counter ì•±ì—� broadcast-channel ë�¼ì�´ë¸ŒëŸ¬ë¦¬ë¥¼
ë�„ì�…í•˜ì—¬ íƒ­ ê°„ ë�°ì�´í„° ë�™ê¸°í™”í•˜ëŠ” ê²ƒì�„ ë§Œë“¤ì–´ ë³´ê²
ìŠµë‹ˆë‹¤.

![sample.png](https://devblog.kakaostyle.com/img/content/2022-10-12-1/sample.png)

###  ê¸°ë³¸ Counter ì½”ë“œ

    
    
    // src/App.tsx
    import { useState } from 'react';
    
    const App = () => {
      const [count, setCount] = useState<number>(0);
    
      const handleClick = () => {
        setCount((prev) => {
          const next = prev + 1;
          return next;
        });
      };
    
      return (
        <div>
          <h1>Counter</h1>
          <div>
            <div>Current count: {count}</div>
            <div>
              <button onClick={handleClick}>Count</button>
            </div>
          </div>
        </div>
      );
    };
    
    export default App;
    

###  useBroadcastChannel React Hooks

ë¦¬ì•¡íŠ¸ì—�ì„œ ì‚¬ìš©í•˜ê¸° í�¸í•˜ê²Œ broadcast-channel ë�¼ì�´ë¸ŒëŸ¬ë¦¬ë¥¼
í›…ìœ¼ë¡œ ë§Œë“¤ì–´ì¤�ë‹ˆë‹¤. íŒŒë�¼ë¯¸í„°ë¡œëŠ” **ì±„ë„� ì�´ë¦„** ,
**ë©”ì‹œì§€ í•¸ë“¤ëŸ¬** , **ë�¼ì�´ë¸ŒëŸ¬ë¦¬ ì˜µì…˜** ì�„ ë°›ë�„ë¡�
êµ¬í˜„í•´ì£¼ì—ˆìŠµë‹ˆë‹¤.

    
    
    // src/hooks.ts
    import { useRef, useEffect, useCallback } from 'react';
    import { BroadcastChannel, BroadcastChannelOptions } from 'broadcast-channel';
    
    export interface UseBroadcastChannelOptions
      extends Omit<BroadcastChannelOptions, 'node'> {}
    
    export function useBroadcastChannel<T>(
      channelName: string,
      onMessage: (message: T) => void,
      options?: UseBroadcastChannelOptions
    ) {
      const broadcastChannelRef = useRef<BroadcastChannel<T> | null>(null);
      const onMessageRef = useRef<((message: T) => void) | null>(null);
    
      const handlePostMessage = useCallback((message: T) => {
        if (broadcastChannelRef.current) {
          broadcastChannelRef.current.postMessage(message);
        }
      }, []);
    
      useEffect(() => {
        onMessageRef.current = onMessage;
      }, [onMessage]);
    
      useEffect(() => {
        let mounted = true;
        const channel = new BroadcastChannel<T>(channelName, options);
    
        const handleMessage = (message: T) => {
          if (!mounted) {
            return;
          }
          onMessageRef.current?.(message);
        };
    
        channel.onmessage = handleMessage;
        broadcastChannelRef.current = channel;
    
        return () => {
          mounted = false;
          broadcastChannelRef.current = null;
          channel.close();
        };
      }, [channelName, options]);
    
      return { postMessage: handlePostMessage };
    }
    

###  Counter Appì—� useBroadcastChannel ë�„ì�…

ë§ˆì§€ë§‰ìœ¼ë¡œ ë§Œë“¤ì—ˆë�˜ í›…ì�„ ë¦¬ì•¡íŠ¸ ì•±ì—� ì¶”ê°€í•˜ê³ ` onMessage `
ë¶€ë¶„ê³¼ ` postMessage ` ë¶€ë¶„ì�„ ë�„ì�…í•´ ì¤�ë‹ˆë‹¤.

    
    
    // src/App.tsx
    import { useState } from 'react';
    import { useBroadcastChannel } from './hooks';
    
    const App = () => {
      const [count, setCount] = useState<number>(0);
      const { postMessage } = useBroadcastChannel<number>('test-app', (message) => {
        // ë©”ì‹œì§€ë¥¼ ì „ë‹¬ë°›ìœ¼ë©´ setCount í•¨ìˆ˜ í˜¸ì¶œ
        setCount(message);
      });
    
      const handleClick = () => {
        setCount((prev) => {
          const next = prev + 1;
          // ë‹¤ë¥¸ ìœˆë�„ìš°ë‚˜ íƒ­ì—� ì•Œë ¤ì£¼ê¸° ìœ„í•´ postMessage ë©”ì„œë“œ í˜¸ì¶œ
          postMessage(next);
          return next;
        });
      };
    
      return (
        <div>
          <h1>Counter</h1>
          <div>
            <div>Current count: {count}</div>
            <div>
              <button onClick={handleClick}>Count</button>
            </div>
          </div>
        </div>
      );
    };
    
    export default App;
    

![sample_result.gif](https://devblog.kakaostyle.com/img/content/2022-10-12-1/sample_result.gif)

##  ë§ˆì¹˜ë©°

ë§Œì•½ [ TanStack Query ](https://tanstack.com/query/v4) (React Query)ë¥¼
ì‚¬ìš©í•´ ë�°ì�´í„°ë¥¼ ê´€ë¦¬í•˜ê³ ì�ˆë‹¤ë©´ ì§�ì ‘ ë�°ì�´í„°ë¥¼ ì£¼ê³ ë°›ëŠ”
ëŒ€ì‹ ì‹¤í—˜ ë²„ì „ í”ŒëŸ¬ê·¸ì�¸ì�¸ [ broadcastQueryClient
](https://tanstack.com/query/v4/docs/plugins/broadcastQueryClient) ë¥¼
í™œìš©í•´ ë�°ì�´í„°ë¥¼ ë�™ê¸°í™” í• ìˆ˜ë�„ ì�ˆìŠµë‹ˆë‹¤. í�´ë�¼ì�´ì–¸íŠ¸
ì›¹ë·°ê°„ ë�°ì�´í„°ë¥¼ ë�™ê¸°í™” í•˜ëŠ” ëŒ€ì‹ ì›¹ë·° ì „í™˜ì�´ ì�¼ì–´ë‚
ë•Œ(visibilitychange ì�´ë²¤íŠ¸) ì„œë²„ì—�ì„œ ìƒˆë¡œ ë�°ì�´í„°ë¥¼ ë°›ì•„ì˜¬
ìˆ˜ë�„ ì�ˆìŠµë‹ˆë‹¤. ì�´ì™€ ê°™ì�´ ë¬¸ì œë¥¼ í•´ê²°í•˜ëŠ” ë°©ë²•ì�€
ì—¬ëŸ¬ê°€ì§€ê°€ ì�ˆìœ¼ë‹ˆ ìƒ�í™©ì—� ë§�ê²Œ ë�„ì�…í•´ë³´ë©´ ì¢‹ì�„ ê²ƒ
ê°™ìŠµë‹ˆë‹¤.

ì¶”ê°€ë¡œ ìœ„ì—� ë§Œë“¤ì—ˆë�˜ ë¦¬ì•¡íŠ¸ í›…ì�„ [ ëª¨ë“ˆ
](https://github.com/use-broadcast-channel/use-broadcast-channel) ë¡œ
ë§Œë“¤ì–´ ê³µê°œí–ˆìŠµë‹ˆë‹¤. ì�´ìŠˆ ë°� PRì�€ ì–¸ì œë‚˜ í™˜ì˜�ì�…ë‹ˆë‹¤. :) (
~~Starë�„ ì£¼ì‹œë©´ ì¢‹ìŠµë‹ˆë‹¤~~ )

ë§ˆì§€ë§‰ìœ¼ë¡œ ì§€ê·¸ì�¬ê·¸ ì—�í”½ ì„œë¹„ìŠ¤ ë°� ì§€ê·¸ì�¬ê·¸ ì•± ë‚´ ì›¹ë·°
í�˜ì�´ì§€ë¥¼ í•¨ê»˜ ê°œë°œí•´ë³´ê³ ì‹¶ìœ¼ì‹œë©´ ì–¸ì œë“ í�¸í•˜ê²Œ [ ë§�í�¬
](https://career.kakaostyle.com/o/31890) ë¥¼ í†µí•´ ì§€ì›�í•´ì£¼ì„¸ìš”!

ê°�ì‚¬í•©ë‹ˆë‹¤.


-->

<!--






-->

<!--
Broadcast Channel API - Web APIs | MDN 

The Broadcast Channel API allows basic communication between browsing contexts
(that is, windows, tabs, frames, or iframes) and workers on the same origin.

developer.mozilla.org


-->

<!--






-->

