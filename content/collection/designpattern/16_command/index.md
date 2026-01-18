---
collection_order: 16
title: "[Design Pattern] Command - 커맨드 패턴"
description: "Command 패턴은 요청을 객체로 캡슐화하여 호출자와 수신자를 분리합니다. 명령의 실행 취소(undo), 큐잉, 로깅 등 다양한 기능을 유연하게 구현할 수 있습니다."
date: 2022-01-01
last_modified_at: 2022-03-01
categories: Design Pattern
image: "tmp_wordcloud.png"
header:
  teaser: /assets/images/undefined/design-pattern-nedir-2021-12-18-143754.jpg
tags:
  - Design Pattern
  - 디자인 패턴
  - Command
  - 커맨드
  - Behavioral Pattern
  - 행위 패턴
  - GoF
  - Gang of Four
  - Encapsulation
  - 캡슐화
  - Request
  - 요청
  - Invoker
  - 호출자
  - Receiver
  - 수신자
  - Undo
  - 실행 취소
  - Redo
  - 재실행
  - Queue
  - 큐
  - Macro
  - 매크로
  - Transaction
  - 트랜잭션
  - Logging
  - 로깅
  - Action
  - 액션
  - Callback
  - 콜백
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
  - GUI
  - Menu
  - Button
  - Scheduler
  - 스케줄러
---

커맨드 패턴(Command Pattern)은 요청을 객체로 캡슐화하여 요청을 보내는 객체와 요청을 수행하는 객체를 분리하는 행위 디자인 패턴이다. 이 패턴을 통해 요청의 큐잉, 로깅, 실행 취소(Undo)/재실행(Redo) 등 다양한 기능을 유연하게 구현할 수 있다.

## 개요

**커맨드 패턴의 정의**

커맨드 패턴은 실행될 기능(메서드 호출)을 캡슐화하여 클래스로 만들고, 이를 통해 요청을 객체로 다룰 수 있게 한다. 호출자(Invoker)는 구체적인 명령이나 수신자(Receiver)에 대해 알 필요 없이, 오직 Command 인터페이스를 통해서만 명령을 실행한다.

**패턴의 필요성 및 사용 사례**

커맨드 패턴은 다음과 같은 상황에서 유용하다:

- **Undo/Redo**: 텍스트 에디터, 그래픽 편집기 등에서 실행 취소 기능
- **트랜잭션**: 여러 명령을 묶어 원자적으로 실행하거나 롤백
- **매크로**: 여러 명령을 연속으로 실행
- **큐잉**: 명령을 큐에 저장했다가 나중에 실행
- **로깅**: 명령 실행 이력 기록 및 재실행
- **GUI 버튼/메뉴**: 동일한 기능을 여러 UI 요소에서 호출
- **스케줄러**: 명령을 예약하여 특정 시간에 실행

**패턴의 장점과 단점**

| 장점 | 단점 |
|------|------|
| 호출자와 수신자 분리 (느슨한 결합) | 간단한 명령에도 클래스가 필요 |
| Undo/Redo 쉽게 구현 | 클래스 수 증가 |
| 명령의 조합과 큐잉 가능 | 명령 상태 관리 복잡 |
| 새 명령 추가 용이 | 단순 작업에는 과도한 설계 |

## 커맨드 패턴의 구성 요소

```
┌──────────────┐        ┌─────────────────────────┐
│   Client     │───────▶│       Invoker           │
└──────────────┘        ├─────────────────────────┤
      │                 │ - command: Command       │
      │                 ├─────────────────────────┤
      │                 │ + setCommand(Command)   │
      │                 │ + executeCommand()      │
      │                 └───────────┬─────────────┘
      │                             │
      │                             │ calls execute()
      ▼                             ▼
┌─────────────────────────────────────────────────┐
│              <<interface>>                       │
│                 Command                          │
├─────────────────────────────────────────────────┤
│ + execute()                                      │
│ + undo()                                         │
└─────────────────────────────────────────────────┘
                       △
                       │
         ┌─────────────┼─────────────┐
         │             │             │
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ ConcreteCmd1   │ │ ConcreteCmd2   │ │ ConcreteCmd3   │
├────────────────┤ ├────────────────┤ ├────────────────┤
│ - receiver     │ │ - receiver     │ │ - receiver     │
├────────────────┤ ├────────────────┤ ├────────────────┤
│ + execute()    │ │ + execute()    │ │ + execute()    │
│ + undo()       │ │ + undo()       │ │ + undo()       │
└────────┬───────┘ └────────────────┘ └────────────────┘
         │
         │ delegates to
         ▼
┌────────────────┐
│    Receiver    │
├────────────────┤
│ + action()     │
└────────────────┘
```

**1. Command (커맨드)**
- 명령을 실행하기 위한 인터페이스
- execute()와 필요시 undo() 메서드 선언

**2. ConcreteCommand (구체적 커맨드)**
- Command 인터페이스 구현
- Receiver와의 바인딩 및 실행 로직 포함
- execute() 호출 시 Receiver의 메서드 호출

**3. Invoker (호출자)**
- Command를 저장하고 실행을 요청
- 명령의 이력 관리 (Undo/Redo 스택)

**4. Receiver (수신자)**
- 실제 작업을 수행하는 객체
- Command가 요청한 동작을 처리

**5. Client (클라이언트)**
- ConcreteCommand를 생성하고 Receiver를 설정

## 구현 예제

### Python 예제 - 텍스트 에디터 (Undo/Redo)

```python
# 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

from abc import ABC, abstractmethod
from typing import List
import copy

# Command 인터페이스
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

# Receiver - 텍스트 문서
class Document:
    def __init__(self):
        self._content: str = ""
        self._cursor_position: int = 0
    
    @property
    def content(self) -> str:
        return self._content
    
    @property
    def cursor_position(self) -> int:
        return self._cursor_position
    
    def insert_text(self, text: str, position: int) -> None:
        self._content = self._content[:position] + text + self._content[position:]
        self._cursor_position = position + len(text)
    
    def delete_text(self, start: int, length: int) -> str:
        deleted = self._content[start:start + length]
        self._content = self._content[:start] + self._content[start + length:]
        self._cursor_position = start
        return deleted
    
    def set_cursor(self, position: int) -> None:
        self._cursor_position = max(0, min(position, len(self._content)))
    
    def display(self) -> None:
        print(f"내용: \"{self._content}\"")
        print(f"커서 위치: {self._cursor_position}")

# ConcreteCommand - 텍스트 삽입
class InsertTextCommand(Command):
    def __init__(self, document: Document, text: str, position: int = None):
        self._document = document
        self._text = text
        self._position = position if position is not None else document.cursor_position
    
    def execute(self) -> None:
        self._document.insert_text(self._text, self._position)
    
    def undo(self) -> None:
        self._document.delete_text(self._position, len(self._text))
    
    def get_description(self) -> str:
        return f"삽입: \"{self._text}\" at {self._position}"

# ConcreteCommand - 텍스트 삭제
class DeleteTextCommand(Command):
    def __init__(self, document: Document, start: int, length: int):
        self._document = document
        self._start = start
        self._length = length
        self._deleted_text: str = ""
    
    def execute(self) -> None:
        self._deleted_text = self._document.delete_text(self._start, self._length)
    
    def undo(self) -> None:
        self._document.insert_text(self._deleted_text, self._start)
    
    def get_description(self) -> str:
        return f"삭제: \"{self._deleted_text}\" at {self._start}"

# Invoker - 에디터
class TextEditor:
    def __init__(self, document: Document):
        self._document = document
        self._history: List[Command] = []  # Undo 스택
        self._redo_stack: List[Command] = []  # Redo 스택
    
    def execute_command(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # 새 명령 실행 시 Redo 스택 초기화
        print(f"✓ 실행: {command.get_description()}")
    
    def undo(self) -> bool:
        if not self._history:
            print("✗ 실행 취소할 명령이 없습니다")
            return False
        
        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)
        print(f"↩ Undo: {command.get_description()}")
        return True
    
    def redo(self) -> bool:
        if not self._redo_stack:
            print("✗ 재실행할 명령이 없습니다")
            return False
        
        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
        print(f"↪ Redo: {command.get_description()}")
        return True
    
    def show_history(self) -> None:
        print("\n명령 이력:")
        for i, cmd in enumerate(self._history, 1):
            print(f"  {i}. {cmd.get_description()}")
        print()

# 사용 예제
if __name__ == "__main__":
    # 문서와 에디터 생성
    doc = Document()
    editor = TextEditor(doc)
    
    print("=== 텍스트 에디터 ===\n")
    
    # 텍스트 입력
    editor.execute_command(InsertTextCommand(doc, "Hello"))
    doc.display()
    print()
    
    editor.execute_command(InsertTextCommand(doc, " World"))
    doc.display()
    print()
    
    editor.execute_command(InsertTextCommand(doc, "!", doc.cursor_position))
    doc.display()
    
    editor.show_history()
    
    # Undo 테스트
    print("=== Undo 테스트 ===")
    editor.undo()
    doc.display()
    print()
    
    editor.undo()
    doc.display()
    print()
    
    # Redo 테스트
    print("=== Redo 테스트 ===")
    editor.redo()
    doc.display()
    print()
    
    # 삭제 명령
    print("=== 삭제 명령 ===")
    editor.execute_command(DeleteTextCommand(doc, 0, 2))  # "He" 삭제
    doc.display()
    print()
    
    editor.undo()
    doc.display()
```

### Java 예제 - 스마트 홈 리모컨

```java
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

import java.util.*;

// Command 인터페이스
interface Command {
    void execute();
    void undo();
    String getDescription();
}

// NoCommand (Null Object Pattern)
class NoCommand implements Command {
    public void execute() {}
    public void undo() {}
    public String getDescription() { return "No Command"; }
}

// Receiver - 조명
class Light {
    private String location;
    private int brightness = 0;
    
    public Light(String location) {
        this.location = location;
    }
    
    public void on() {
        brightness = 100;
        System.out.println(location + " 조명 켜짐 (밝기: " + brightness + "%)");
    }
    
    public void off() {
        brightness = 0;
        System.out.println(location + " 조명 꺼짐");
    }
    
    public void dim(int level) {
        brightness = level;
        System.out.println(location + " 조명 밝기 조절: " + brightness + "%");
    }
    
    public int getBrightness() { return brightness; }
}

// Receiver - 에어컨
class AirConditioner {
    private String location;
    private boolean isOn = false;
    private int temperature = 24;
    
    public AirConditioner(String location) {
        this.location = location;
    }
    
    public void on() {
        isOn = true;
        System.out.println(location + " 에어컨 켜짐 (설정 온도: " + temperature + "°C)");
    }
    
    public void off() {
        isOn = false;
        System.out.println(location + " 에어컨 꺼짐");
    }
    
    public void setTemperature(int temp) {
        temperature = temp;
        System.out.println(location + " 에어컨 온도 설정: " + temperature + "°C");
    }
    
    public int getTemperature() { return temperature; }
    public boolean isOn() { return isOn; }
}

// ConcreteCommand - 조명 켜기
class LightOnCommand implements Command {
    private Light light;
    private int previousBrightness;
    
    public LightOnCommand(Light light) {
        this.light = light;
    }
    
    public void execute() {
        previousBrightness = light.getBrightness();
        light.on();
    }
    
    public void undo() {
        if (previousBrightness == 0) {
            light.off();
        } else {
            light.dim(previousBrightness);
        }
    }
    
    public String getDescription() { return "조명 켜기"; }
}

// ConcreteCommand - 조명 끄기
class LightOffCommand implements Command {
    private Light light;
    private int previousBrightness;
    
    public LightOffCommand(Light light) {
        this.light = light;
    }
    
    public void execute() {
        previousBrightness = light.getBrightness();
        light.off();
    }
    
    public void undo() {
        if (previousBrightness > 0) {
            light.dim(previousBrightness);
        }
    }
    
    public String getDescription() { return "조명 끄기"; }
}

// ConcreteCommand - 에어컨 켜기
class ACOnCommand implements Command {
    private AirConditioner ac;
    
    public ACOnCommand(AirConditioner ac) {
        this.ac = ac;
    }
    
    public void execute() {
        ac.on();
    }
    
    public void undo() {
        ac.off();
    }
    
    public String getDescription() { return "에어컨 켜기"; }
}

// ConcreteCommand - 매크로 커맨드
class MacroCommand implements Command {
    private List<Command> commands;
    private String name;
    
    public MacroCommand(String name, List<Command> commands) {
        this.name = name;
        this.commands = new ArrayList<>(commands);
    }
    
    public void execute() {
        System.out.println("=== " + name + " 매크로 실행 ===");
        for (Command cmd : commands) {
            cmd.execute();
        }
    }
    
    public void undo() {
        System.out.println("=== " + name + " 매크로 취소 ===");
        for (int i = commands.size() - 1; i >= 0; i--) {
            commands.get(i).undo();
        }
    }
    
    public String getDescription() { return name + " 매크로"; }
}

// Invoker - 리모컨
class RemoteControl {
    private Command[] onCommands;
    private Command[] offCommands;
    private Stack<Command> undoStack = new Stack<>();
    
    public RemoteControl(int numSlots) {
        onCommands = new Command[numSlots];
        offCommands = new Command[numSlots];
        
        Command noCommand = new NoCommand();
        for (int i = 0; i < numSlots; i++) {
            onCommands[i] = noCommand;
            offCommands[i] = noCommand;
        }
    }
    
    public void setCommand(int slot, Command onCmd, Command offCmd) {
        onCommands[slot] = onCmd;
        offCommands[slot] = offCmd;
    }
    
    public void onButtonPressed(int slot) {
        onCommands[slot].execute();
        undoStack.push(onCommands[slot]);
    }
    
    public void offButtonPressed(int slot) {
        offCommands[slot].execute();
        undoStack.push(offCommands[slot]);
    }
    
    public void undoButtonPressed() {
        if (!undoStack.isEmpty()) {
            Command lastCmd = undoStack.pop();
            System.out.println("↩ Undo: " + lastCmd.getDescription());
            lastCmd.undo();
        }
    }
}

// 사용 예제
public class CommandDemo {
    public static void main(String[] args) {
        // 장치 생성
        Light livingRoomLight = new Light("거실");
        Light bedroomLight = new Light("침실");
        AirConditioner ac = new AirConditioner("거실");
        
        // 커맨드 생성
        Command livingLightOn = new LightOnCommand(livingRoomLight);
        Command livingLightOff = new LightOffCommand(livingRoomLight);
        Command bedroomLightOn = new LightOnCommand(bedroomLight);
        Command bedroomLightOff = new LightOffCommand(bedroomLight);
        Command acOn = new ACOnCommand(ac);
        Command acOff = new ACOnCommand(ac);
        
        // 리모컨 설정
        RemoteControl remote = new RemoteControl(4);
        remote.setCommand(0, livingLightOn, livingLightOff);
        remote.setCommand(1, bedroomLightOn, bedroomLightOff);
        remote.setCommand(2, acOn, acOff);
        
        // 매크로 - "외출 모드"
        List<Command> partyOffCmds = Arrays.asList(
            livingLightOff, bedroomLightOff, acOff
        );
        Command leaveHomeMacro = new MacroCommand("외출 모드", partyOffCmds);
        remote.setCommand(3, leaveHomeMacro, leaveHomeMacro);
        
        // 테스트
        System.out.println("=== 개별 버튼 테스트 ===");
        remote.onButtonPressed(0);  // 거실 조명 켜기
        remote.onButtonPressed(1);  // 침실 조명 켜기
        remote.onButtonPressed(2);  // 에어컨 켜기
        
        System.out.println("\n=== Undo 테스트 ===");
        remote.undoButtonPressed();  // 에어컨 끄기
        
        System.out.println("\n=== 매크로 테스트 ===");
        remote.onButtonPressed(3);  // 외출 모드 실행
    }
}
```

### C# 예제 - 파일 작업 큐

```csharp
// 42jerrykim.github.io에서 더 많은 정보를 확인 할 수 있다

using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;

// Command 인터페이스
public interface ICommand
{
    void Execute();
    void Undo();
    string Description { get; }
}

// Receiver - 파일 시스템 관리자
public class FileSystemReceiver
{
    public void CreateFile(string path, string content)
    {
        Console.WriteLine($"[파일 생성] {path}");
        // 실제로는: File.WriteAllText(path, content);
    }
    
    public void DeleteFile(string path)
    {
        Console.WriteLine($"[파일 삭제] {path}");
        // 실제로는: File.Delete(path);
    }
    
    public void CopyFile(string source, string destination)
    {
        Console.WriteLine($"[파일 복사] {source} -> {destination}");
        // 실제로는: File.Copy(source, destination);
    }
    
    public void MoveFile(string source, string destination)
    {
        Console.WriteLine($"[파일 이동] {source} -> {destination}");
        // 실제로는: File.Move(source, destination);
    }
}

// ConcreteCommand - 파일 생성
public class CreateFileCommand : ICommand
{
    private readonly FileSystemReceiver _receiver;
    private readonly string _path;
    private readonly string _content;
    
    public CreateFileCommand(FileSystemReceiver receiver, string path, string content)
    {
        _receiver = receiver;
        _path = path;
        _content = content;
    }
    
    public void Execute() => _receiver.CreateFile(_path, _content);
    public void Undo() => _receiver.DeleteFile(_path);
    public string Description => $"파일 생성: {_path}";
}

// ConcreteCommand - 파일 삭제
public class DeleteFileCommand : ICommand
{
    private readonly FileSystemReceiver _receiver;
    private readonly string _path;
    private string _backupContent;
    
    public DeleteFileCommand(FileSystemReceiver receiver, string path)
    {
        _receiver = receiver;
        _path = path;
    }
    
    public void Execute()
    {
        // 백업 후 삭제 (실제로는 파일 내용 읽기)
        _backupContent = $"[백업된 내용: {_path}]";
        _receiver.DeleteFile(_path);
    }
    
    public void Undo() => _receiver.CreateFile(_path, _backupContent);
    public string Description => $"파일 삭제: {_path}";
}

// ConcreteCommand - 파일 이동
public class MoveFileCommand : ICommand
{
    private readonly FileSystemReceiver _receiver;
    private readonly string _source;
    private readonly string _destination;
    
    public MoveFileCommand(FileSystemReceiver receiver, string source, string destination)
    {
        _receiver = receiver;
        _source = source;
        _destination = destination;
    }
    
    public void Execute() => _receiver.MoveFile(_source, _destination);
    public void Undo() => _receiver.MoveFile(_destination, _source);
    public string Description => $"파일 이동: {_source} -> {_destination}";
}

// Invoker - 작업 큐
public class CommandQueue
{
    private readonly Queue<ICommand> _pendingCommands = new Queue<ICommand>();
    private readonly Stack<ICommand> _executedCommands = new Stack<ICommand>();
    private bool _isProcessing = false;
    
    public void AddCommand(ICommand command)
    {
        _pendingCommands.Enqueue(command);
        Console.WriteLine($"✚ 큐에 추가: {command.Description}");
    }
    
    public void ProcessAll()
    {
        Console.WriteLine("\n=== 명령 큐 처리 시작 ===");
        _isProcessing = true;
        
        while (_pendingCommands.Count > 0)
        {
            var command = _pendingCommands.Dequeue();
            Console.WriteLine($"▶ 실행 중: {command.Description}");
            
            try
            {
                command.Execute();
                _executedCommands.Push(command);
                Thread.Sleep(500); // 시뮬레이션
            }
            catch (Exception ex)
            {
                Console.WriteLine($"✗ 실패: {ex.Message}");
                // 실패 시 롤백 옵션
            }
        }
        
        _isProcessing = false;
        Console.WriteLine("=== 명령 큐 처리 완료 ===\n");
    }
    
    public void UndoLast()
    {
        if (_executedCommands.Count > 0)
        {
            var command = _executedCommands.Pop();
            Console.WriteLine($"↩ Undo: {command.Description}");
            command.Undo();
        }
        else
        {
            Console.WriteLine("✗ 실행 취소할 명령이 없습니다");
        }
    }
    
    public void UndoAll()
    {
        Console.WriteLine("\n=== 전체 롤백 ===");
        while (_executedCommands.Count > 0)
        {
            UndoLast();
        }
        Console.WriteLine("=== 롤백 완료 ===\n");
    }
    
    public int PendingCount => _pendingCommands.Count;
    public int ExecutedCount => _executedCommands.Count;
}

// 사용 예제
public class Program
{
    public static void Main(string[] args)
    {
        var fileSystem = new FileSystemReceiver();
        var commandQueue = new CommandQueue();
        
        // 명령 생성 및 큐에 추가
        commandQueue.AddCommand(new CreateFileCommand(fileSystem, "/docs/readme.txt", "Hello World"));
        commandQueue.AddCommand(new CreateFileCommand(fileSystem, "/docs/config.json", "{}"));
        commandQueue.AddCommand(new MoveFileCommand(fileSystem, "/docs/readme.txt", "/backup/readme.txt"));
        commandQueue.AddCommand(new DeleteFileCommand(fileSystem, "/docs/config.json"));
        
        Console.WriteLine($"\n대기 중인 명령: {commandQueue.PendingCount}개\n");
        
        // 모든 명령 실행
        commandQueue.ProcessAll();
        
        Console.WriteLine($"실행된 명령: {commandQueue.ExecutedCount}개");
        
        // 마지막 명령 취소
        Console.WriteLine("\n=== 단일 Undo ===");
        commandQueue.UndoLast();
        
        // 전체 롤백
        commandQueue.UndoAll();
    }
}
```

## 실제 사용 사례

### 1. Java Runnable
```java
Runnable task = () -> System.out.println("Task executed");
executor.submit(task);
```

### 2. Redux Action
```javascript
dispatch({ type: 'INCREMENT', payload: 5 });
```

### 3. Git 명령
각 커밋은 커맨드 패턴의 구현으로, reset으로 undo 가능

### 4. 데이터베이스 트랜잭션
```sql
BEGIN TRANSACTION;
-- 명령들
ROLLBACK; -- Undo
COMMIT;
```

## 관련 패턴

| 패턴 | 커맨드와의 관계 |
|------|--------------|
| **Memento** | Undo를 위한 상태 저장에 사용 가능 |
| **Composite** | 매크로 커맨드 구현에 사용 |
| **Strategy** | 둘 다 행위를 캡슐화하지만, 목적이 다름 |
| **Chain of Responsibility** | 요청을 처리할 핸들러 결정에 사용 가능 |

## FAQ

**Q1: 커맨드 패턴과 전략 패턴의 차이점은?**

전략 패턴은 알고리즘을 선택하기 위한 것이고, 커맨드 패턴은 요청을 객체로 캡슐화하여 실행, 취소, 큐잉 등을 하기 위한 것입니다.

**Q2: 복잡한 Undo는 어떻게 구현하나요?**

Memento 패턴과 함께 사용하여 상태를 저장하거나, 역연산을 직접 구현합니다. 복잡한 경우 스냅샷 기반 접근이 필요할 수 있습니다.

**Q3: 커맨드 객체의 생명주기는?**

실행 후 바로 버리거나 (일회성), 히스토리에 보관하거나 (Undo용), 큐에 저장했다가 나중에 실행할 수 있습니다.

**Q4: 람다로 대체할 수 있나요?**

간단한 커맨드는 람다로 대체 가능합니다. 하지만 Undo 기능이나 상태가 필요한 경우 클래스로 구현해야 합니다.

## 참고 자료

- GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"
- Head First Design Patterns
- Java Executor Framework 문서