---
title: "[Algorithm] C++/Python 백준 10828번 : 스택"
categories: 
- Algorithm
- DataStructures
tags:
- Stack
- Implementation
- Fast I/O
- O(N)
- DataStructures
- ProblemSolving
image: "tmp_wordcloud.png"
date: 2024-10-25
---

스택은 컴퓨터 과학에서 매우 기본적이면서도 중요한 자료 구조 중 하나이다. 백준 온라인 저지의 10828번 문제는 이러한 스택의 구현과 관련된 문제로, 다양한 명령을 효율적으로 처리해야 한다. 이번 글에서는 이 문제를 상세히 분석하고, C++과 Python으로 구현하는 방법을 소개한다.

문제 : [https://www.acmicpc.net/problem/10828](https://www.acmicpc.net/problem/10828)

## 문제 설명

백준 10828번 문제는 정수를 저장할 수 있는 스택을 구현하고, 주어진 명령을 처리하는 프로그램을 작성하는 것이다. 스택은 LIFO(Last In, First Out) 구조로, 가장 나중에 삽입된 요소가 먼저 제거되는 특성을 가진다. 문제에서 요구하는 명령은 총 다섯 가지로, `push X`, `pop`, `size`, `empty`, `top`이 있다.

- `push X`: 정수 X를 스택에 넣는 연산이다.
- `pop`: 스택에서 가장 위에 있는 정수를 빼고, 그 수를 출력한다. 스택이 비어있으면 -1을 출력한다.
- `size`: 스택에 들어있는 정수의 개수를 출력한다.
- `empty`: 스택이 비어있으면 1, 아니면 0을 출력한다.
- `top`: 스택의 가장 위에 있는 정수를 출력한다. 스택이 비어있으면 -1을 출력한다.

입력으로는 첫 번째 줄에 명령의 수 N(1 ≤ N ≤ 10,000)이 주어지고, 그 다음 N개의 줄에 각 명령이 주어진다. 출력은 각 명령에 대해 요구되는 결과를 한 줄씩 출력하면 된다.

예를 들어, 다음과 같은 입력이 주어졌을 때:

```
14
push 1
push 2
top
size
empty
pop
pop
pop
size
empty
pop
push 3
empty
top
```

출력은 다음과 같이 된다:

```
2
2
0
2
1
-1
0
1
-1
0
3
```

## 접근 방식

이 문제는 기본적인 스택 자료 구조의 구현과 명령 처리를 요구한다. 스택을 구현하는 방법은 여러 가지가 있지만, C++에서는 `std::vector`를 이용하거나 직접 배열을 관리할 수 있다. Python에서는 리스트를 사용하여 스택을 쉽게 구현할 수 있다.

효율적인 입출력이 중요하다. 특히, C++에서는 `std::cin`과 `std::cout`의 동기화를 해제하고, `std::cin.tie(NULL)`을 사용하여 입출력 속도를 향상시킬 수 있다. 이는 큰 입력을 처리할 때 시간 초과를 방지하는 데 도움이 된다.

명령을 처리할 때는 각 명령을 빠르게 파싱하고, 스택의 상태를 정확하게 관리해야 한다. `push` 명령의 경우 추가적인 정수 X를 입력받아 스택에 삽입하고, 나머지 명령들은 스택의 현재 상태를 기반으로 결과를 출력하면 된다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <vector>
#include <string>

int main() {
    // 빠른 입출력 설정
    std::ios::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    int N;
    std::cin >> N;
    
    std::vector<int> stack; // 스택을 벡터로 구현
    std::string command;
    int X;
    
    for(int i = 0; i < N; ++i){
        std::cin >> command; // 명령어 입력
        if(command == "push"){
            std::cin >> X; // push 명령어의 경우 추가로 정수 X 입력
            stack.push_back(X); // 스택에 X 삽입
        }
        else if(command == "pop"){
            if(stack.empty()){
                std::cout << "-1\n"; // 스택이 비어있으면 -1 출력
            }
            else{
                std::cout << stack.back() << "\n"; // 스택의 가장 위 요소 출력
                stack.pop_back(); // 스택에서 제거
            }
        }
        else if(command == "size"){
            std::cout << stack.size() << "\n"; // 스택의 크기 출력
        }
        else if(command == "empty"){
            std::cout << (stack.empty() ? "1" : "0") << "\n"; // 스택이 비어있는지 여부 출력
        }
        else if(command == "top"){
            if(stack.empty()){
                std::cout << "-1\n"; // 스택이 비어있으면 -1 출력
            }
            else{
                std::cout << stack.back() << "\n"; // 스택의 가장 위 요소 출력
            }
        }
    }
    
    return 0;
}
```

### 코드의 동작 단계별 설명

1. **입출력 속도 향상**:
    ```cpp
    std::ios::sync_with_stdio(false);
    std::cin.tie(NULL);
    ```
    - `std::ios::sync_with_stdio(false);`는 C++의 표준 입출력과 C의 표준 입출력 간의 동기화를 해제하여 입출력 속도를 향상시킨다.
    - `std::cin.tie(NULL);`는 `cin`과 `cout`의 묶음을 풀어, `cin`이 `cout`을 자동으로 flush하지 않도록 한다.

2. **스택 구현**:
    ```cpp
    std::vector<int> stack;
    ```
    - `std::vector`를 사용하여 스택을 구현하였다. `push_back`과 `pop_back` 메서드를 통해 스택의 `push`와 `pop` 연산을 수행한다.

3. **명령 처리**:
    ```cpp
    for(int i = 0; i < N; ++i){
        std::cin >> command;
        // 명령어에 따라 분기 처리
    }
    ```
    - 입력으로 주어진 N개의 명령을 하나씩 처리한다. 각 명령어에 따라 적절한 연산을 수행하고, 결과를 출력한다.

4. **각 명령어에 대한 처리**:
    - **push X**: 스택에 X를 삽입한다.
    - **pop**: 스택의 가장 위 요소를 출력하고 제거한다. 스택이 비어있으면 -1을 출력한다.
    - **size**: 스택의 크기를 출력한다.
    - **empty**: 스택이 비어있으면 1, 아니면 0을 출력한다.
    - **top**: 스택의 가장 위 요소를 출력한다. 스택이 비어있으면 -1을 출력한다.

## C++ without library 코드와 설명

```cpp
#include <iostream>
#include <cstring>
#include <cstdlib>

struct Stack {
    int* arr; // 스택을 저장할 배열
    int top;
    int capacity;
    
    Stack(int size) {
        arr = (int*)malloc(sizeof(int) * size);
        top = -1;
        capacity = size;
    }
    
    void push(int x) {
        if(top + 1 >= capacity){
            // 필요시 용량을 늘리는 로직 추가 가능
            // 여기서는 최대 용량을 넘지 않는다고 가정
        }
        arr[++top] = x;
    }
    
    int pop(){
        if(top == -1){
            return -1;
        }
        return arr[top--];
    }
    
    int size(){
        return top + 1;
    }
    
    int empty(){
        return top == -1 ? 1 : 0;
    }
    
    int getTop(){
        if(top == -1){
            return -1;
        }
        return arr[top];
    }
};

int main(){
    std::ios::sync_with_stdio(false);
    std::cin.tie(NULL);
    
    int N;
    std::cin >> N;
    
    Stack stack(N); // 스택의 최대 크기를 N으로 설정
    std::string command;
    int X;
    
    for(int i = 0; i < N; ++i){
        std::cin >> command;
        if(command == "push"){
            std::cin >> X;
            stack.push(X);
        }
        else if(command == "pop"){
            std::cout << stack.pop() << "\n";
        }
        else if(command == "size"){
            std::cout << stack.size() << "\n";
        }
        else if(command == "empty"){
            std::cout << stack.empty() << "\n";
        }
        else if(command == "top"){
            std::cout << stack.getTop() << "\n";
        }
    }
    
    free(stack.arr); // 할당한 메모리 해제
    return 0;
}
```

### 코드의 동작 단계별 설명

1. **스택 구조체 정의**:
    ```cpp
    struct Stack {
        int* arr;
        int top;
        int capacity;
        // 생성자와 메서드 정의
    };
    ```
    - 스택을 배열로 구현하기 위해 구조체를 정의하였다. `arr`는 스택을 저장할 배열, `top`은 현재 스택의 최상위 인덱스, `capacity`는 스택의 최대 크기를 나타낸다.

2. **스택 초기화 및 메서드 구현**:
    ```cpp
    Stack(int size) {
        arr = (int*)malloc(sizeof(int) * size);
        top = -1;
        capacity = size;
    }
    ```
    - 생성자에서 스택의 배열을 동적으로 할당하고, `top`을 -1로 초기화하여 스택이 비어있음을 나타낸다.

    ```cpp
    void push(int x) { /* ... */ }
    int pop() { /* ... */ }
    int size() { /* ... */ }
    int empty() { /* ... */ }
    int getTop() { /* ... */ }
    ```
    - 각 메서드는 `push`, `pop`, `size`, `empty`, `top` 명령을 처리하기 위한 기능을 제공한다.

3. **명령 처리**:
    ```cpp
    for(int i = 0; i < N; ++i){
        std::cin >> command;
        // 명령어에 따라 스택의 메서드를 호출
    }
    ```
    - 입력으로 주어진 N개의 명령을 하나씩 읽어들여, 해당 명령에 맞는 스택의 메서드를 호출하여 처리한다.

4. **메모리 관리**:
    ```cpp
    free(stack.arr);
    ```
    - 동적으로 할당한 메모리를 프로그램 종료 전에 해제하여 메모리 누수를 방지한다.

## Python 코드와 설명

```python
import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    stack = []
    idx = 1
    output = []
    
    for _ in range(N):
        command = data[idx]
        if command == "push":
            idx += 1
            X = int(data[idx])
            stack.append(X)
        elif command == "pop":
            if stack:
                output.append(str(stack.pop()))
            else:
                output.append("-1")
        elif command == "size":
            output.append(str(len(stack)))
        elif command == "empty":
            output.append("1" if not stack else "0")
        elif command == "top":
            if stack:
                output.append(str(stack[-1]))
            else:
                output.append("-1")
        idx += 1
    
    print('\n'.join(output))

if __name__ == "__main__":
    main()
```

### 코드의 동작 단계별 설명

1. **입출력 최적화**:
    ```python
    import sys
    input = sys.stdin.read
    data = input().split()
    ```
    - `sys.stdin.read`를 사용하여 모든 입력을 한 번에 읽어들이고, 이를 공백으로 분리하여 리스트 `data`에 저장한다. 이는 입력이 많을 때 효율적이다.

2. **스택 구현**:
    ```python
    stack = []
    ```
    - Python의 리스트를 이용하여 스택을 구현하였다. `append`와 `pop` 메서드를 통해 스택의 `push`와 `pop` 연산을 수행한다.

3. **명령 처리**:
    ```python
    for _ in range(N):
        command = data[idx]
        # 명령어에 따라 스택 연산 수행
    ```
    - 리스트 `data`를 순회하면서 각 명령어를 처리한다. `push` 명령의 경우 추가로 정수 X를 읽어와 스택에 삽입한다. 나머지 명령들은 스택의 현재 상태에 따라 결과를 리스트 `output`에 저장한다.

4. **출력**:
    ```python
    print('\n'.join(output))
    ```
    - 결과를 리스트 `output`에 저장한 후, 한 번에 출력하여 시간 효율을 높인다.

## 결론

백준 10828번 문제는 기본적인 스택 자료 구조의 구현과 효율적인 명령 처리를 요구한다. C++과 Python 모두에서 스택을 효과적으로 구현할 수 있으며, 특히 입출력 최적화를 통해 시간 제한을 만족시킬 수 있다. C++에서는 `std::vector`를 사용하여 간편하게 스택을 구현할 수 있으며, Python에서는 리스트를 활용하여 동일한 기능을 수행할 수 있다.

추가적으로, C++에서 표준 라이브러리를 사용하지 않고 스택을 구현함으로써 메모리 관리의 중요성을 체감할 수 있었다. 이러한 문제를 통해 자료 구조의 기본 원리를 이해하고, 효율적인 알고리즘 설계의 필요성을 다시 한 번 느낄 수 있었다. 앞으로 더 복잡한 자료 구조와 알고리즘 문제를 풀 때에도 이러한 기본기를 바탕으로 문제를 접근하면 보다 효율적으로 해결할 수 있을 것이다.