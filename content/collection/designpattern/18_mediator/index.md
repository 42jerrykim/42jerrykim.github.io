---
collection_order: 18
title: "[Design Pattern] Mediator - 중재자 패턴"
description: "Mediator 패턴은 객체들 간의 직접 통신을 제한하고 중재자를 통해 상호작용하게 합니다. 복잡한 의존성을 줄이고 유연하게 시스템을 구성할 수 있습니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Mediator
  - 중재자
  - Behavioral Pattern
  - 행위 패턴
  - GoF
  - Gang of Four
  - Loose Coupling
  - 느슨한 결합
  - Colleague
  - 동료
  - Communication
  - 통신
  - Centralized Control
  - 중앙 집중 제어
  - Event Bus
  - 이벤트 버스
  - Message Broker
  - 메시지 브로커
  - Chat Room
  - 채팅방
  - Air Traffic Control
  - 항공 교통 관제
  - GUI Components
  - Dialog
  - 다이얼로그
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
  - MVC
  - Controller
  - 컨트롤러
  - Hub
  - 허브
  - Coordinator
  - 조정자
---

중재자 패턴(Mediator Pattern)은 객체들 간의 직접적인 통신을 제한하고, 중재자 객체를 통해서만 상호작용하도록 하는 행위 디자인 패턴이다. 이 패턴을 사용하면 객체 간의 복잡한 의존 관계를 줄이고, 시스템의 결합도를 낮출 수 있다.

## 개요

**중재자 패턴의 정의**

중재자 패턴은 다수의 객체가 서로 직접 통신하는 대신 중재자를 통해 통신하게 함으로써, 객체들의 상호의존성을 캡슐화한다. 마치 항공 교통 관제사가 비행기들 사이의 통신을 중재하는 것처럼, 중재자는 동료(Colleague) 객체들 사이의 상호작용을 조정한다.

**패턴의 필요성 및 사용 사례**

중재자 패턴은 다음과 같은 상황에서 유용하다:

- **채팅 시스템**: 채팅방(중재자)을 통한 사용자 간 메시지 전달
- **GUI 컴포넌트**: 다이얼로그가 버튼, 체크박스 등의 상호작용 조정
- **항공 관제**: 비행기들의 통신을 관제탑이 중재
- **이벤트 버스**: 컴포넌트 간 이벤트 전달
- **MVC 아키텍처**: Controller가 Model과 View 사이 중재

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 컴포넌트 간 결합도 감소 | 중재자가 God Object가 될 수 있음 |
| 컴포넌트 재사용성 향상 | 중재자의 복잡도 증가 |
| 상호작용 로직 중앙 집중 | 단일 실패 지점 |
| 새 컴포넌트 추가 용이 | 디버깅이 어려울 수 있음 |

## 중재자 패턴의 구성 요소

```
┌────────────────────────────────────┐
│          <<interface>>             │
│            Mediator                │
├────────────────────────────────────┤
│ + notify(sender, event)            │
└────────────────────────────────────┘
              △
              │
┌────────────────────────────────────┐
│        ConcreteMediator            │
├────────────────────────────────────┤
│ - colleagueA: ColleagueA           │
│ - colleagueB: ColleagueB           │
├────────────────────────────────────┤
│ + notify(sender, event)            │
└────────────────────────────────────┘
         │         │
         │         │
         ▼         ▼
┌──────────┐  ┌──────────┐
│ColleagueA│  │ColleagueB│
├──────────┤  ├──────────┤
│-mediator │  │-mediator │
├──────────┤  ├──────────┤
│+operation│  │+operation│
└──────────┘  └──────────┘
```

**1. Mediator (중재자)**
- 동료 객체 간 통신을 위한 인터페이스 정의

**2. ConcreteMediator (구체적 중재자)**
- 동료 객체들의 참조 유지
- 동료 객체 간 조정 로직 구현

**3. Colleague (동료)**
- 중재자에 대한 참조 유지
- 다른 동료와 직접 통신하지 않고 중재자를 통해 통신

## 구현 예제

### Python 예제 - 채팅방

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime

# Mediator 인터페이스
class ChatMediator(ABC):
    @abstractmethod
    def send_message(self, message: str, sender: 'User') -> None:
        pass
    
    @abstractmethod
    def add_user(self, user: 'User') -> None:
        pass

# Colleague - 사용자
class User:
    def __init__(self, name: str, mediator: ChatMediator):
        self.name = name
        self._mediator = mediator
        mediator.add_user(self)
    
    def send(self, message: str) -> None:
        print(f"💬 [{self.name}] 전송: {message}")
        self._mediator.send_message(message, self)
    
    def receive(self, message: str, sender_name: str) -> None:
        print(f"   [{self.name}] 수신: {message} (from {sender_name})")

# ConcreteMediator - 채팅방
class ChatRoom(ChatMediator):
    def __init__(self, name: str):
        self._name = name
        self._users: List[User] = []
        self._message_history: List[Dict] = []
    
    def add_user(self, user: User) -> None:
        self._users.append(user)
        print(f"📢 [{self._name}] {user.name}님이 입장했습니다.")
    
    def send_message(self, message: str, sender: User) -> None:
        self._message_history.append({
            "time": datetime.now(),
            "sender": sender.name,
            "message": message
        })
        
        for user in self._users:
            if user != sender:
                user.receive(message, sender.name)
    
    def show_history(self) -> None:
        print(f"\n=== [{self._name}] 채팅 기록 ===")
        for msg in self._message_history:
            print(f"{msg['time'].strftime('%H:%M')} - {msg['sender']}: {msg['message']}")

# 사용 예제
if __name__ == "__main__":
    # 채팅방 (중재자) 생성
    room = ChatRoom("개발팀")
    
    # 사용자 (동료) 생성
    alice = User("Alice", room)
    bob = User("Bob", room)
    charlie = User("Charlie", room)
    
    print()
    
    # 메시지 전송 (중재자를 통해)
    alice.send("안녕하세요!")
    print()
    
    bob.send("네, 안녕하세요!")
    print()
    
    charlie.send("오늘 회의는 몇 시죠?")
    
    room.show_history()
```

### Java 예제 - GUI 다이얼로그

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// Mediator 인터페이스
interface DialogMediator {
    void notify(Component sender, String event);
}

// Colleague 기본 클래스
abstract class Component {
    protected DialogMediator mediator;
    protected String name;
    
    public Component(String name) {
        this.name = name;
    }
    
    public void setMediator(DialogMediator mediator) {
        this.mediator = mediator;
    }
    
    public String getName() { return name; }
}

// ConcreteColleague - 체크박스
class Checkbox extends Component {
    private boolean checked = false;
    
    public Checkbox(String name) { super(name); }
    
    public void click() {
        checked = !checked;
        System.out.println("☑️ [" + name + "] " + (checked ? "체크됨" : "체크 해제"));
        if (mediator != null) {
            mediator.notify(this, "check");
        }
    }
    
    public boolean isChecked() { return checked; }
}

// ConcreteColleague - 텍스트 필드
class TextBox extends Component {
    private String text = "";
    private boolean enabled = true;
    
    public TextBox(String name) { super(name); }
    
    public void setText(String text) {
        this.text = text;
        System.out.println("📝 [" + name + "] 입력: " + text);
        if (mediator != null) {
            mediator.notify(this, "textChanged");
        }
    }
    
    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
        System.out.println("   [" + name + "] " + (enabled ? "활성화" : "비활성화"));
    }
    
    public String getText() { return text; }
    public boolean isEnabled() { return enabled; }
}

// ConcreteColleague - 버튼
class Button extends Component {
    private boolean enabled = false;
    
    public Button(String name) { super(name); }
    
    public void click() {
        if (enabled) {
            System.out.println("🔘 [" + name + "] 클릭됨");
            if (mediator != null) {
                mediator.notify(this, "click");
            }
        } else {
            System.out.println("🔘 [" + name + "] 비활성화 상태");
        }
    }
    
    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
        System.out.println("   [" + name + "] " + (enabled ? "활성화" : "비활성화"));
    }
    
    public boolean isEnabled() { return enabled; }
}

// ConcreteMediator - 회원가입 다이얼로그
class SignUpDialog implements DialogMediator {
    private Checkbox termsCheckbox;
    private TextBox usernameBox;
    private TextBox passwordBox;
    private Button submitButton;
    
    public SignUpDialog() {
        System.out.println("=== 회원가입 다이얼로그 초기화 ===\n");
        
        termsCheckbox = new Checkbox("약관 동의");
        usernameBox = new TextBox("사용자명");
        passwordBox = new TextBox("비밀번호");
        submitButton = new Button("가입하기");
        
        termsCheckbox.setMediator(this);
        usernameBox.setMediator(this);
        passwordBox.setMediator(this);
        submitButton.setMediator(this);
        
        // 초기 상태: 약관 미동의 시 입력 필드 비활성화
        usernameBox.setEnabled(false);
        passwordBox.setEnabled(false);
        submitButton.setEnabled(false);
    }
    
    @Override
    public void notify(Component sender, String event) {
        if (sender == termsCheckbox && event.equals("check")) {
            handleTermsChange();
        } else if (event.equals("textChanged")) {
            validateForm();
        } else if (sender == submitButton && event.equals("click")) {
            submitForm();
        }
    }
    
    private void handleTermsChange() {
        boolean accepted = termsCheckbox.isChecked();
        usernameBox.setEnabled(accepted);
        passwordBox.setEnabled(accepted);
        if (!accepted) {
            submitButton.setEnabled(false);
        } else {
            validateForm();
        }
    }
    
    private void validateForm() {
        boolean valid = termsCheckbox.isChecked()
            && !usernameBox.getText().isEmpty()
            && passwordBox.getText().length() >= 4;
        submitButton.setEnabled(valid);
    }
    
    private void submitForm() {
        System.out.println("\n🎉 회원가입 완료!");
        System.out.println("   사용자명: " + usernameBox.getText());
    }
    
    // 시뮬레이션용 getter
    public Checkbox getTermsCheckbox() { return termsCheckbox; }
    public TextBox getUsernameBox() { return usernameBox; }
    public TextBox getPasswordBox() { return passwordBox; }
    public Button getSubmitButton() { return submitButton; }
}

// 사용 예제
public class MediatorDemo {
    public static void main(String[] args) {
        SignUpDialog dialog = new SignUpDialog();
        
        System.out.println("\n=== 시나리오 1: 약관 미동의 상태에서 가입 시도 ===");
        dialog.getSubmitButton().click();
        
        System.out.println("\n=== 시나리오 2: 약관 동의 ===");
        dialog.getTermsCheckbox().click();
        
        System.out.println("\n=== 시나리오 3: 정보 입력 ===");
        dialog.getUsernameBox().setText("john_doe");
        dialog.getPasswordBox().setText("1234");
        
        System.out.println("\n=== 시나리오 4: 가입하기 ===");
        dialog.getSubmitButton().click();
    }
}
```

## 실제 사용 사례

### 1. Java Swing/AWT
JDialog가 버튼, 텍스트필드 등의 상호작용 중재

### 2. MVC 아키텍처
Controller가 Model과 View 사이의 중재자 역할

### 3. 이벤트 버스
Vue.js의 EventBus, Android의 EventBus 라이브러리

### 4. 채팅 서버
WebSocket 서버가 클라이언트들 사이의 메시지 중재

## 관련 패턴

| 패턴 | 중재자와의 관계 |
|------|---------------|
| **Observer** | 중재자가 Observer 패턴으로 구현되기도 함 |
| **Facade** | Facade는 단방향, Mediator는 양방향 통신 |
| **Command** | 중재자가 Command를 사용하여 통신 가능 |

## FAQ

**Q1: 중재자와 퍼사드 패턴의 차이점은?**

퍼사드는 서브시스템에 대한 단순화된 인터페이스를 제공하고 (단방향), 중재자는 컴포넌트 간의 양방향 통신을 조정합니다.

**Q2: 중재자가 너무 복잡해지면?**

관련 기능별로 여러 중재자로 분리하거나, 특정 프로토콜에 대해 별도의 핸들러를 두는 것을 고려하세요.

## 참고 자료

- GoF의 "Design Patterns"
- Head First Design Patterns