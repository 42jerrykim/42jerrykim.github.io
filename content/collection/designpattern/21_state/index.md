---
collection_order: 21
title: "[Design Pattern] State - 상태 패턴"
description: "State 패턴은 객체의 내부 상태가 변경될 때 행동이 바뀌도록 합니다. 조건문 없이도 상태 변경에 따른 다양한 동작을 구현하여 유지보수성과 확장성을 높입니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - State
  - 상태
  - Behavioral Pattern
  - 행위 패턴
  - GoF
  - Gang of Four
  - State Machine
  - 상태 기계
  - Finite State Machine
  - 유한 상태 기계
  - Context
  - 컨텍스트
  - Concrete State
  - 구체 상태
  - State Transition
  - 상태 전이
  - Behavior Change
  - 행동 변경
  - Polymorphism
  - 다형성
  - Encapsulation
  - 캡슐화
  - Open Closed Principle
  - 개방 폐쇄 원칙
  - Conditional Logic
  - 조건 로직
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
  - Vending Machine
  - 자판기
  - TCP Connection
  - Game State
  - 게임 상태
  - Workflow
  - 워크플로우
---

상태 패턴(State Pattern)은 객체의 내부 상태가 변경될 때 객체의 행동이 바뀌도록 하는 행위 디자인 패턴이다. 이 패턴을 사용하면 복잡한 조건문 없이도 상태에 따른 다양한 동작을 구현할 수 있으며, 상태별 행동을 별도의 클래스로 분리하여 유지보수성을 높인다.

## 개요

**상태 패턴의 정의**

상태 패턴은 유한 상태 기계(Finite State Machine)의 개념을 객체지향적으로 구현한 패턴이다. 각 상태를 별도의 클래스로 캡슐화하고, 현재 상태에 따라 동작을 위임함으로써 조건문의 복잡성을 줄인다.

**패턴의 필요성 및 사용 사례**

상태 패턴은 다음과 같은 상황에서 유용하다:

- **자판기**: 동전 투입, 상품 선택, 배출 등 상태에 따른 동작
- **TCP 연결**: 연결, 대기, 종료 등의 상태 관리
- **게임 캐릭터**: 서있기, 걷기, 뛰기, 점프 등 상태 전환
- **문서 워크플로우**: 초안, 검토 중, 승인됨, 반려됨 등
- **주문 처리**: 대기, 처리 중, 배송 중, 완료 등
- **UI 컴포넌트**: 활성화, 비활성화, 호버, 포커스 등

**조건문 vs 상태 패턴**

```python
# 조건문 방식 (복잡하고 유지보수 어려움)
def handle(self, action):
    if self.state == "IDLE":
        if action == "start":
            self.state = "RUNNING"
    elif self.state == "RUNNING":
        if action == "pause":
            self.state = "PAUSED"
    # ... 상태가 늘어날수록 복잡해짐

# 상태 패턴 (깔끔하고 확장 용이)
def handle(self, action):
    self.state.handle(self, action)
```

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 상태별 행동을 별도 클래스로 분리 | 상태가 적으면 과도한 설계 |
| 복잡한 조건문 제거 | 클래스 수 증가 |
| 새 상태 추가 용이 (개방-폐쇄 원칙) | 상태 전이 로직이 분산될 수 있음 |
| 상태 전이 명시적으로 표현 | 상태 간 의존성 발생 가능 |

## 상태 패턴의 구성 요소

```
┌──────────────────────────────────────┐
│             Context                  │
├──────────────────────────────────────┤
│ - state: State                       │
├──────────────────────────────────────┤
│ + setState(State)                    │
│ + request()                          │
│   └── state.handle(this)             │
└──────────────────────────────────────┘
              │
              │ delegates to
              ▼
┌──────────────────────────────────────┐
│          <<interface>>               │
│              State                   │
├──────────────────────────────────────┤
│ + handle(Context)                    │
└──────────────────────────────────────┘
              △
              │
    ┌─────────┼─────────┐
    │         │         │
┌─────────┐ ┌─────────┐ ┌─────────┐
│ StateA  │ │ StateB  │ │ StateC  │
├─────────┤ ├─────────┤ ├─────────┤
│+handle()│ │+handle()│ │+handle()│
└─────────┘ └─────────┘ └─────────┘
```

**1. State (상태)**
- 상태별 행동을 정의하는 인터페이스
- Context가 호출하는 메서드 선언

**2. ConcreteState (구체적 상태)**
- State 인터페이스의 구체적 구현
- 해당 상태에서의 행동과 상태 전이 로직 포함

**3. Context (컨텍스트)**
- 현재 상태 객체에 대한 참조 유지
- 상태 변경 메서드 제공
- 클라이언트의 요청을 현재 상태에 위임

## 구현 예제

### Python 예제 - 자판기

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional

# State 인터페이스
class VendingMachineState(ABC):
    @abstractmethod
    def insert_coin(self, machine: 'VendingMachine') -> None:
        pass
    
    @abstractmethod
    def eject_coin(self, machine: 'VendingMachine') -> None:
        pass
    
    @abstractmethod
    def select_product(self, machine: 'VendingMachine') -> None:
        pass
    
    @abstractmethod
    def dispense(self, machine: 'VendingMachine') -> None:
        pass
    
    @abstractmethod
    def get_state_name(self) -> str:
        pass

# ConcreteState - 동전 없음
class NoCoinState(VendingMachineState):
    def insert_coin(self, machine: 'VendingMachine') -> None:
        print("✓ 동전이 투입되었습니다.")
        machine.set_state(HasCoinState())
    
    def eject_coin(self, machine: 'VendingMachine') -> None:
        print("✗ 반환할 동전이 없습니다.")
    
    def select_product(self, machine: 'VendingMachine') -> None:
        print("✗ 먼저 동전을 투입해주세요.")
    
    def dispense(self, machine: 'VendingMachine') -> None:
        print("✗ 동전을 투입하고 상품을 선택해주세요.")
    
    def get_state_name(self) -> str:
        return "동전 없음"

# ConcreteState - 동전 있음
class HasCoinState(VendingMachineState):
    def insert_coin(self, machine: 'VendingMachine') -> None:
        print("✗ 이미 동전이 투입되어 있습니다.")
    
    def eject_coin(self, machine: 'VendingMachine') -> None:
        print("✓ 동전이 반환되었습니다.")
        machine.set_state(NoCoinState())
    
    def select_product(self, machine: 'VendingMachine') -> None:
        if machine.get_product_count() > 0:
            print("✓ 상품이 선택되었습니다.")
            machine.set_state(SoldState())
        else:
            print("✗ 상품이 품절되었습니다. 동전을 반환합니다.")
            machine.set_state(NoCoinState())
    
    def dispense(self, machine: 'VendingMachine') -> None:
        print("✗ 먼저 상품을 선택해주세요.")
    
    def get_state_name(self) -> str:
        return "동전 있음"

# ConcreteState - 판매 중
class SoldState(VendingMachineState):
    def insert_coin(self, machine: 'VendingMachine') -> None:
        print("✗ 잠시 기다려주세요. 상품이 나오고 있습니다.")
    
    def eject_coin(self, machine: 'VendingMachine') -> None:
        print("✗ 이미 상품이 선택되어 반환할 수 없습니다.")
    
    def select_product(self, machine: 'VendingMachine') -> None:
        print("✗ 상품이 나오고 있습니다. 잠시 기다려주세요.")
    
    def dispense(self, machine: 'VendingMachine') -> None:
        print("🎁 상품이 배출되었습니다!")
        machine.release_product()
        
        if machine.get_product_count() > 0:
            machine.set_state(NoCoinState())
        else:
            print("⚠ 상품이 모두 소진되었습니다.")
            machine.set_state(SoldOutState())
    
    def get_state_name(self) -> str:
        return "판매 중"

# ConcreteState - 품절
class SoldOutState(VendingMachineState):
    def insert_coin(self, machine: 'VendingMachine') -> None:
        print("✗ 품절입니다. 동전을 받을 수 없습니다.")
    
    def eject_coin(self, machine: 'VendingMachine') -> None:
        print("✗ 투입된 동전이 없습니다.")
    
    def select_product(self, machine: 'VendingMachine') -> None:
        print("✗ 품절입니다.")
    
    def dispense(self, machine: 'VendingMachine') -> None:
        print("✗ 배출할 상품이 없습니다.")
    
    def get_state_name(self) -> str:
        return "품절"

# Context - 자판기
class VendingMachine:
    def __init__(self, product_count: int):
        self._product_count = product_count
        if product_count > 0:
            self._state: VendingMachineState = NoCoinState()
        else:
            self._state: VendingMachineState = SoldOutState()
    
    def set_state(self, state: VendingMachineState) -> None:
        print(f"  [상태 변경: {self._state.get_state_name()} → {state.get_state_name()}]")
        self._state = state
    
    def get_product_count(self) -> int:
        return self._product_count
    
    def release_product(self) -> None:
        self._product_count -= 1
    
    def refill(self, count: int) -> None:
        self._product_count += count
        print(f"✓ 상품 {count}개 보충. 총 재고: {self._product_count}개")
        if isinstance(self._state, SoldOutState):
            self._state = NoCoinState()
    
    def insert_coin(self) -> None:
        print("\n[동전 투입]")
        self._state.insert_coin(self)
    
    def eject_coin(self) -> None:
        print("\n[동전 반환]")
        self._state.eject_coin(self)
    
    def select_product(self) -> None:
        print("\n[상품 선택]")
        self._state.select_product(self)
        self._state.dispense(self)
    
    def __str__(self) -> str:
        return f"자판기 [상태: {self._state.get_state_name()}, 재고: {self._product_count}개]"

# 사용 예제
if __name__ == "__main__":
    print("=== 자판기 시뮬레이션 ===\n")
    
    machine = VendingMachine(2)
    print(machine)
    
    # 정상 구매 시나리오
    machine.insert_coin()
    machine.select_product()
    print(machine)
    
    # 동전 반환 시나리오
    machine.insert_coin()
    machine.eject_coin()
    print(machine)
    
    # 마지막 상품 구매
    machine.insert_coin()
    machine.select_product()
    print(machine)
    
    # 품절 상태에서 시도
    machine.insert_coin()
    machine.select_product()
    
    # 상품 보충
    print("\n[상품 보충]")
    machine.refill(3)
    print(machine)
    
    # 다시 구매
    machine.insert_coin()
    machine.select_product()
    print(machine)
```

### Java 예제 - 문서 워크플로우

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

// State 인터페이스
interface DocumentState {
    void publish(Document doc);
    void review(Document doc);
    void reject(Document doc);
    void approve(Document doc);
    String getStateName();
}

// ConcreteState - 초안 상태
class DraftState implements DocumentState {
    @Override
    public void publish(Document doc) {
        System.out.println("✓ 문서를 검토 요청했습니다.");
        doc.setState(new PendingReviewState());
    }
    
    @Override
    public void review(Document doc) {
        System.out.println("✗ 초안 상태에서는 검토할 수 없습니다.");
    }
    
    @Override
    public void reject(Document doc) {
        System.out.println("✗ 초안은 반려할 수 없습니다.");
    }
    
    @Override
    public void approve(Document doc) {
        System.out.println("✗ 초안은 바로 승인할 수 없습니다.");
    }
    
    @Override
    public String getStateName() { return "초안"; }
}

// ConcreteState - 검토 대기 상태
class PendingReviewState implements DocumentState {
    @Override
    public void publish(Document doc) {
        System.out.println("✗ 이미 검토 요청된 상태입니다.");
    }
    
    @Override
    public void review(Document doc) {
        System.out.println("✓ 검토를 시작합니다.");
        doc.setState(new UnderReviewState());
    }
    
    @Override
    public void reject(Document doc) {
        System.out.println("✓ 검토 전 반려되었습니다.");
        doc.setState(new DraftState());
    }
    
    @Override
    public void approve(Document doc) {
        System.out.println("✗ 검토 후에 승인할 수 있습니다.");
    }
    
    @Override
    public String getStateName() { return "검토 대기"; }
}

// ConcreteState - 검토 중 상태
class UnderReviewState implements DocumentState {
    @Override
    public void publish(Document doc) {
        System.out.println("✗ 검토 중에는 다시 제출할 수 없습니다.");
    }
    
    @Override
    public void review(Document doc) {
        System.out.println("✗ 이미 검토 중입니다.");
    }
    
    @Override
    public void reject(Document doc) {
        System.out.println("✓ 문서가 반려되었습니다. 수정이 필요합니다.");
        doc.setState(new DraftState());
    }
    
    @Override
    public void approve(Document doc) {
        System.out.println("✓ 문서가 승인되었습니다!");
        doc.setState(new ApprovedState());
    }
    
    @Override
    public String getStateName() { return "검토 중"; }
}

// ConcreteState - 승인됨 상태
class ApprovedState implements DocumentState {
    @Override
    public void publish(Document doc) {
        System.out.println("✓ 승인된 문서가 발행되었습니다!");
        doc.setState(new PublishedState());
    }
    
    @Override
    public void review(Document doc) {
        System.out.println("✗ 이미 승인된 문서입니다.");
    }
    
    @Override
    public void reject(Document doc) {
        System.out.println("✓ 승인이 취소되었습니다.");
        doc.setState(new DraftState());
    }
    
    @Override
    public void approve(Document doc) {
        System.out.println("✗ 이미 승인되었습니다.");
    }
    
    @Override
    public String getStateName() { return "승인됨"; }
}

// ConcreteState - 발행됨 상태
class PublishedState implements DocumentState {
    @Override
    public void publish(Document doc) {
        System.out.println("✗ 이미 발행되었습니다.");
    }
    
    @Override
    public void review(Document doc) {
        System.out.println("✗ 발행된 문서는 검토할 수 없습니다.");
    }
    
    @Override
    public void reject(Document doc) {
        System.out.println("✗ 발행된 문서는 반려할 수 없습니다.");
    }
    
    @Override
    public void approve(Document doc) {
        System.out.println("✗ 발행된 문서입니다.");
    }
    
    @Override
    public String getStateName() { return "발행됨"; }
}

// Context - 문서
class Document {
    private String title;
    private String content;
    private DocumentState state;
    
    public Document(String title, String content) {
        this.title = title;
        this.content = content;
        this.state = new DraftState();
    }
    
    public void setState(DocumentState state) {
        System.out.println("  [" + this.state.getStateName() + " → " + state.getStateName() + "]");
        this.state = state;
    }
    
    public void publish() {
        System.out.println("\n[발행 요청]");
        state.publish(this);
    }
    
    public void review() {
        System.out.println("\n[검토 시작]");
        state.review(this);
    }
    
    public void reject() {
        System.out.println("\n[반려]");
        state.reject(this);
    }
    
    public void approve() {
        System.out.println("\n[승인]");
        state.approve(this);
    }
    
    @Override
    public String toString() {
        return String.format("문서 '%s' [상태: %s]", title, state.getStateName());
    }
}

// 사용 예제
public class StateDemo {
    public static void main(String[] args) {
        System.out.println("=== 문서 워크플로우 ===\n");
        
        Document doc = new Document("2024년 사업 계획서", "내용...");
        System.out.println(doc);
        
        // 워크플로우 시나리오
        doc.publish();    // 초안 → 검토 대기
        doc.review();     // 검토 대기 → 검토 중
        doc.reject();     // 검토 중 → 초안 (반려)
        System.out.println(doc);
        
        // 다시 제출
        doc.publish();    // 초안 → 검토 대기
        doc.review();     // 검토 대기 → 검토 중
        doc.approve();    // 검토 중 → 승인됨
        doc.publish();    // 승인됨 → 발행됨
        System.out.println(doc);
        
        // 발행 후 시도
        doc.reject();     // 불가
    }
}
```

### C# 예제 - 음악 플레이어

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;

// State 인터페이스
public interface IPlayerState
{
    void Play(MusicPlayer player);
    void Pause(MusicPlayer player);
    void Stop(MusicPlayer player);
    void Next(MusicPlayer player);
    void Previous(MusicPlayer player);
    string StateName { get; }
}

// ConcreteState - 정지 상태
public class StoppedState : IPlayerState
{
    public string StateName => "정지됨";
    
    public void Play(MusicPlayer player)
    {
        Console.WriteLine("▶ 재생 시작");
        player.SetState(new PlayingState());
    }
    
    public void Pause(MusicPlayer player)
    {
        Console.WriteLine("✗ 이미 정지 상태입니다.");
    }
    
    public void Stop(MusicPlayer player)
    {
        Console.WriteLine("✗ 이미 정지 상태입니다.");
    }
    
    public void Next(MusicPlayer player)
    {
        Console.WriteLine("⏭ 다음 곡으로 이동");
        player.NextTrack();
    }
    
    public void Previous(MusicPlayer player)
    {
        Console.WriteLine("⏮ 이전 곡으로 이동");
        player.PreviousTrack();
    }
}

// ConcreteState - 재생 상태
public class PlayingState : IPlayerState
{
    public string StateName => "재생 중";
    
    public void Play(MusicPlayer player)
    {
        Console.WriteLine("✗ 이미 재생 중입니다.");
    }
    
    public void Pause(MusicPlayer player)
    {
        Console.WriteLine("⏸ 일시 정지");
        player.SetState(new PausedState());
    }
    
    public void Stop(MusicPlayer player)
    {
        Console.WriteLine("⏹ 정지");
        player.ResetPosition();
        player.SetState(new StoppedState());
    }
    
    public void Next(MusicPlayer player)
    {
        Console.WriteLine("⏭ 다음 곡 재생");
        player.NextTrack();
    }
    
    public void Previous(MusicPlayer player)
    {
        Console.WriteLine("⏮ 이전 곡 재생");
        player.PreviousTrack();
    }
}

// ConcreteState - 일시 정지 상태
public class PausedState : IPlayerState
{
    public string StateName => "일시 정지";
    
    public void Play(MusicPlayer player)
    {
        Console.WriteLine("▶ 재생 계속");
        player.SetState(new PlayingState());
    }
    
    public void Pause(MusicPlayer player)
    {
        Console.WriteLine("✗ 이미 일시 정지 상태입니다.");
    }
    
    public void Stop(MusicPlayer player)
    {
        Console.WriteLine("⏹ 정지");
        player.ResetPosition();
        player.SetState(new StoppedState());
    }
    
    public void Next(MusicPlayer player)
    {
        Console.WriteLine("⏭ 다음 곡으로 이동 (일시 정지 유지)");
        player.NextTrack();
    }
    
    public void Previous(MusicPlayer player)
    {
        Console.WriteLine("⏮ 이전 곡으로 이동 (일시 정지 유지)");
        player.PreviousTrack();
    }
}

// Context - 음악 플레이어
public class MusicPlayer
{
    private IPlayerState _state;
    private string[] _playlist;
    private int _currentTrackIndex;
    private int _position; // 재생 위치 (초)
    
    public MusicPlayer(string[] playlist)
    {
        _playlist = playlist;
        _currentTrackIndex = 0;
        _position = 0;
        _state = new StoppedState();
    }
    
    public void SetState(IPlayerState state)
    {
        Console.WriteLine($"  [{_state.StateName} → {state.StateName}]");
        _state = state;
    }
    
    public void NextTrack()
    {
        _currentTrackIndex = (_currentTrackIndex + 1) % _playlist.Length;
        _position = 0;
        ShowCurrentTrack();
    }
    
    public void PreviousTrack()
    {
        _currentTrackIndex = (_currentTrackIndex - 1 + _playlist.Length) % _playlist.Length;
        _position = 0;
        ShowCurrentTrack();
    }
    
    public void ResetPosition()
    {
        _position = 0;
    }
    
    public void ShowCurrentTrack()
    {
        Console.WriteLine($"  🎵 현재 곡: {_playlist[_currentTrackIndex]}");
    }
    
    // 클라이언트 인터페이스
    public void Play() { Console.WriteLine("\n[Play 버튼]"); _state.Play(this); }
    public void Pause() { Console.WriteLine("\n[Pause 버튼]"); _state.Pause(this); }
    public void Stop() { Console.WriteLine("\n[Stop 버튼]"); _state.Stop(this); }
    public void Next() { Console.WriteLine("\n[Next 버튼]"); _state.Next(this); }
    public void Previous() { Console.WriteLine("\n[Previous 버튼]"); _state.Previous(this); }
    
    public override string ToString()
    {
        return $"플레이어 [상태: {_state.StateName}, 곡: {_playlist[_currentTrackIndex]}]";
    }
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        string[] playlist = {
            "Bohemian Rhapsody - Queen",
            "Imagine - John Lennon",
            "Hotel California - Eagles"
        };
        
        var player = new MusicPlayer(playlist);
        Console.WriteLine("=== 음악 플레이어 ===\n");
        Console.WriteLine(player);
        
        player.Play();    // 정지됨 → 재생 중
        player.Pause();   // 재생 중 → 일시 정지
        player.Play();    // 일시 정지 → 재생 중
        player.Next();    // 다음 곡
        player.Stop();    // 재생 중 → 정지됨
        
        Console.WriteLine("\n" + player);
        
        player.Previous(); // 이전 곡 (정지 상태에서)
        player.Play();     // 재생 시작
    }
}
```

## 실제 사용 사례

### 1. TCP 연결 상태
CLOSED, LISTEN, SYN_SENT, ESTABLISHED, FIN_WAIT 등

### 2. 게임 캐릭터 상태
Idle, Walking, Running, Jumping, Attacking, Dead

### 3. 주문 처리 시스템
Pending, Confirmed, Processing, Shipped, Delivered, Cancelled

### 4. 인증 세션
Anonymous, Authenticating, Authenticated, Expired

## 관련 패턴

| 패턴 | 상태와의 관계 |
|------|-------------|
| **Strategy** | 둘 다 위임 사용, Strategy는 알고리즘 선택에 초점 |
| **Flyweight** | 상태 객체를 공유할 때 사용 |
| **Singleton** | 상태 객체가 하나만 필요할 때 적용 |

## FAQ

**Q1: 상태 패턴과 전략 패턴의 차이점은?**

전략 패턴에서는 클라이언트가 전략을 선택하고, 상태 패턴에서는 Context 내부에서 상태가 전이됩니다. 상태 패턴의 상태들은 서로를 알 수 있고 전이를 트리거할 수 있습니다.

**Q2: 상태 전이 로직은 어디에 두어야 하나요?**

상태 클래스에 두거나 Context에 둘 수 있습니다. 상태 클래스에 두면 상태가 자율적이지만 결합도가 높아지고, Context에 두면 중앙 집중적이지만 조건문이 늘어날 수 있습니다.

**Q3: 상태 객체를 매번 생성해야 하나요?**

상태 객체가 무상태(stateless)라면 싱글턴 또는 플라이웨이트로 공유할 수 있습니다. 상태별 데이터가 있다면 매번 새로 생성해야 합니다.

**Q4: 복잡한 상태 기계는 어떻게 관리하나요?**

상태가 많고 전이가 복잡하면 상태 기계 전용 라이브러리(XState, Statechart 등)를 사용하거나, 상태 전이 테이블을 별도로 관리하는 것이 좋습니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- Statecharts (David Harel)