---
collection_order: 19
title: "[Design Pattern] Memento - 메멘토 패턴"
description: "Memento 패턴은 객체의 내부 상태를 캡슐화해 외부에 노출하지 않고 이전 상태로 복원합니다. 상태 저장 및 복원으로 실행 취소나 롤백 기능을 구현합니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design-Pattern
  - 디자인패턴
  - GoF
  - State
  - History
  - Code-Quality
  - 코드품질
  - Software-Architecture
  - 소프트웨어아키텍처
  - OOP
  - 객체지향
  - Java
  - C++
  - Python
  - CSharp
  - Database
  - Git
  - GitHub
  - REST
  - API
  - Implementation
  - 구현
  - Memory
  - Gaming
  - 게임
  - 역사
---

메멘토 패턴(Memento Pattern)은 객체의 내부 상태를 캡슐화하여 저장하고, 나중에 해당 상태로 복원할 수 있게 하는 행위 디자인 패턴이다. 이 패턴을 사용하면 객체의 캡슐화를 위반하지 않으면서 실행 취소(Undo)나 스냅샷 기능을 구현할 수 있다.

## 개요

**메멘토 패턴의 정의**

메멘토 패턴은 객체의 상태를 외부에 저장했다가 나중에 복원할 수 있게 한다. 저장된 상태(메멘토)는 캡슐화되어 있어 원본 객체만 접근할 수 있고, 관리자(Caretaker)는 메멘토의 내용을 알 수 없다.

**패턴의 필요성 및 사용 사례**

메멘토 패턴은 다음과 같은 상황에서 유용하다:

- **Undo/Redo**: 텍스트 에디터, 그래픽 편집기
- **게임 저장**: 체크포인트, 세이브 파일
- **트랜잭션 롤백**: 데이터베이스 상태 복원
- **히스토리 관리**: 브라우저 히스토리, 폼 입력 기록
- **스냅샷**: 특정 시점의 상태 캡처

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 캡슐화 유지하면서 상태 저장 | 메모리 사용량 증가 |
| Undo/Redo 쉽게 구현 | 상태가 크면 비효율적 |
| 스냅샷 기능 제공 | 동적 언어에서 캡슐화 어려움 |
| 복구 지점 관리 용이 | 메멘토 생성 비용 |

## 메멘토 패턴의 구성 요소

```
┌─────────────────────────────────────┐
│            Originator               │
├─────────────────────────────────────┤
│ - state                             │
├─────────────────────────────────────┤
│ + save(): Memento                   │
│ + restore(Memento)                  │
└─────────────────────────────────────┘
              │
              │ creates
              ▼
┌─────────────────────────────────────┐
│             Memento                 │
├─────────────────────────────────────┤
│ - state (private)                   │
├─────────────────────────────────────┤
│ + getState() (only for Originator)  │
└─────────────────────────────────────┘
              △
              │ stores
┌─────────────────────────────────────┐
│           Caretaker                 │
├─────────────────────────────────────┤
│ - history: List<Memento>            │
├─────────────────────────────────────┤
│ + backup()                          │
│ + undo()                            │
└─────────────────────────────────────┘
```

**1. Originator (원조자)**
- 상태를 가진 객체
- 메멘토 생성 및 복원 담당

**2. Memento (메멘토)**
- 원조자의 상태 스냅샷
- 원조자만 접근 가능한 상태 저장

**3. Caretaker (관리자)**
- 메멘토 보관 및 관리
- 메멘토 내용에는 접근하지 않음

## 구현 예제

### Python 예제 - 텍스트 에디터

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from typing import List
from dataclasses import dataclass
from datetime import datetime

# Memento - 에디터 상태 스냅샷
@dataclass
class EditorMemento:
    _content: str
    _cursor_position: int
    _timestamp: datetime
    
    def get_content(self) -> str:
        return self._content
    
    def get_cursor_position(self) -> int:
        return self._cursor_position
    
    def get_timestamp(self) -> datetime:
        return self._timestamp

# Originator - 텍스트 에디터
class TextEditor:
    def __init__(self):
        self._content = ""
        self._cursor_position = 0
    
    def write(self, text: str) -> None:
        self._content = (self._content[:self._cursor_position] 
                        + text 
                        + self._content[self._cursor_position:])
        self._cursor_position += len(text)
    
    def delete(self, count: int) -> None:
        start = max(0, self._cursor_position - count)
        self._content = self._content[:start] + self._content[self._cursor_position:]
        self._cursor_position = start
    
    def move_cursor(self, position: int) -> None:
        self._cursor_position = max(0, min(position, len(self._content)))
    
    def save(self) -> EditorMemento:
        return EditorMemento(self._content, self._cursor_position, datetime.now())
    
    def restore(self, memento: EditorMemento) -> None:
        self._content = memento.get_content()
        self._cursor_position = memento.get_cursor_position()
    
    def display(self) -> str:
        cursor_display = self._content[:self._cursor_position] + "|" + self._content[self._cursor_position:]
        return f"'{cursor_display}'"

# Caretaker - 히스토리 관리자
class History:
    def __init__(self, editor: TextEditor):
        self._editor = editor
        self._history: List[EditorMemento] = []
        self._redo_stack: List[EditorMemento] = []
    
    def backup(self) -> None:
        self._history.append(self._editor.save())
        self._redo_stack.clear()
    
    def undo(self) -> bool:
        if len(self._history) <= 1:
            return False
        
        self._redo_stack.append(self._history.pop())
        self._editor.restore(self._history[-1])
        return True
    
    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        
        memento = self._redo_stack.pop()
        self._history.append(memento)
        self._editor.restore(memento)
        return True
    
    def show_history(self) -> None:
        print("\n📜 히스토리:")
        for i, m in enumerate(self._history):
            print(f"  {i+1}. '{m.get_content()}' ({m.get_timestamp().strftime('%H:%M:%S')})")

# 사용 예제
if __name__ == "__main__":
    editor = TextEditor()
    history = History(editor)
    
    print("=== 텍스트 에디터 (Memento 패턴) ===\n")
    
    history.backup()  # 초기 상태 저장
    
    editor.write("Hello")
    print(f"입력 후: {editor.display()}")
    history.backup()
    
    editor.write(" World")
    print(f"입력 후: {editor.display()}")
    history.backup()
    
    editor.write("!")
    print(f"입력 후: {editor.display()}")
    history.backup()
    
    history.show_history()
    
    print("\n=== Undo 테스트 ===")
    history.undo()
    print(f"Undo 1: {editor.display()}")
    
    history.undo()
    print(f"Undo 2: {editor.display()}")
    
    print("\n=== Redo 테스트 ===")
    history.redo()
    print(f"Redo: {editor.display()}")
```

### Java 예제 - 게임 저장

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// Memento - 게임 상태 스냅샷
class GameMemento {
    private final int level;
    private final int health;
    private final int score;
    private final String position;
    private final Date timestamp;
    
    public GameMemento(int level, int health, int score, String position) {
        this.level = level;
        this.health = health;
        this.score = score;
        this.position = position;
        this.timestamp = new Date();
    }
    
    // package-private: Originator만 접근
    int getLevel() { return level; }
    int getHealth() { return health; }
    int getScore() { return score; }
    String getPosition() { return position; }
    Date getTimestamp() { return timestamp; }
    
    @Override
    public String toString() {
        return String.format("레벨:%d HP:%d 점수:%d 위치:%s", level, health, score, position);
    }
}

// Originator - 게임 캐릭터
class GameCharacter {
    private int level;
    private int health;
    private int score;
    private String position;
    
    public GameCharacter() {
        this.level = 1;
        this.health = 100;
        this.score = 0;
        this.position = "시작점";
    }
    
    public void play(String action) {
        switch (action) {
            case "fight":
                health -= 20;
                score += 100;
                break;
            case "heal":
                health = Math.min(100, health + 30);
                break;
            case "levelup":
                level++;
                health = 100;
                break;
            case "move":
                position = "지역" + (level + new Random().nextInt(3));
                break;
        }
    }
    
    public GameMemento save() {
        return new GameMemento(level, health, score, position);
    }
    
    public void restore(GameMemento memento) {
        this.level = memento.getLevel();
        this.health = memento.getHealth();
        this.score = memento.getScore();
        this.position = memento.getPosition();
    }
    
    public void display() {
        System.out.printf("🎮 레벨:%d | ❤️HP:%d | 🏆점수:%d | 📍%s%n", 
                         level, health, score, position);
    }
}

// Caretaker - 세이브 슬롯 관리자
class SaveManager {
    private Map<String, GameMemento> saveSlots = new LinkedHashMap<>();
    private GameCharacter character;
    
    public SaveManager(GameCharacter character) {
        this.character = character;
    }
    
    public void saveGame(String slotName) {
        saveSlots.put(slotName, character.save());
        System.out.println("💾 저장됨: " + slotName);
    }
    
    public boolean loadGame(String slotName) {
        GameMemento memento = saveSlots.get(slotName);
        if (memento == null) {
            System.out.println("❌ 저장 슬롯 없음: " + slotName);
            return false;
        }
        character.restore(memento);
        System.out.println("📂 불러옴: " + slotName);
        return true;
    }
    
    public void showSaves() {
        System.out.println("\n=== 저장 슬롯 ===");
        for (Map.Entry<String, GameMemento> entry : saveSlots.entrySet()) {
            System.out.println("  " + entry.getKey() + ": " + entry.getValue());
        }
    }
}

// 사용 예제
public class MementoDemo {
    public static void main(String[] args) {
        GameCharacter hero = new GameCharacter();
        SaveManager saveManager = new SaveManager(hero);
        
        System.out.println("=== 게임 시작 ===");
        hero.display();
        saveManager.saveGame("시작");
        
        System.out.println("\n=== 플레이 ===");
        hero.play("move");
        hero.play("fight");
        hero.play("fight");
        hero.display();
        saveManager.saveGame("보스전 전");
        
        System.out.println("\n=== 보스전 (사망) ===");
        hero.play("fight");
        hero.play("fight");
        hero.play("fight");
        hero.display();
        
        System.out.println("\n=== 세이브 로드 ===");
        saveManager.showSaves();
        saveManager.loadGame("보스전 전");
        hero.display();
    }
}
```

## 실제 사용 사례

### 1. 브라우저 히스토리
history.back(), history.forward()

### 2. Git
커밋이 메멘토 역할, 특정 커밋으로 복원 가능

### 3. 데이터베이스 트랜잭션
SAVEPOINT, ROLLBACK

### 4. 직렬화
객체 상태를 저장하고 복원

## 관련 패턴

| 패턴 | 메멘토와의 관계 |
|------|---------------|
| **Command** | Undo 구현 시 함께 사용 |
| **Iterator** | 메멘토 히스토리 순회 |
| **Prototype** | 상태 복제에 사용 가능 |

## FAQ

**Q1: 메멘토와 직렬화의 차이점은?**

직렬화는 객체를 바이트 스트림으로 변환하고, 메멘토는 캡슐화를 유지하면서 상태를 저장합니다.

**Q2: 메모리 사용을 어떻게 줄일 수 있나요?**

변경된 부분만 저장(증분 저장)하거나, 오래된 메멘토를 삭제하거나, 압축을 사용할 수 있습니다.

## 참고 자료

- GoF의 "Design Patterns"
- Head First Design Patterns