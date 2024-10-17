---
title: "[Algorithm] C++/Python 백준 5342번 : Billing 다국어"
categories: 
- Algorithm
- Implementation
- String
tags:
- Implementation
- String
- Hash Map
- Data Structures
- Input Processing
- Brute Force
- Optimization
- O(N)
- Problem Solving
image: "tmp_wordcloud.png"
date: 2024-10-17
---

이번 포스트에서는 백준 온라인 저지의 문제 번호 5342번, "Billing 다국어"에 대해 자세히 살펴보고, C++ 및 Python으로 문제를 해결하는 방법을 설명한다. 이 문제는 다양한 사무용품의 구매 목록을 입력받아 총 비용을 계산하는 구현 문제이다. 문제의 요구사항을 정확히 이해하고 효율적으로 구현하는 방법을 알아보자.

문제 : [https://www.acmicpc.net/problem/5342](https://www.acmicpc.net/problem/5342)

## 문제 설명

회계 부서는 지난 학기 동안 구매한 각 부서의 사무용품 비용을 청구하는 데 어려움을 겪고 있다. 사무용품의 목록과 각 항목의 비용이 주어지면, 입력된 구매 목록을 바탕으로 총 비용을 계산하는 프로그램을 작성해야 한다. 

각 사무용품의 이름과 비용은 다음과 같다:

| Item      | Cost  |
|-----------|-------|
| Paper     | 57.99 |
| Printer   | 120.50|
| Planners  | 31.25 |
| Binders   | 22.50 |
| Calendar  | 10.95 |
| Notebooks | 11.20 |
| Ink       | 66.95 |

입력은 사무용품의 목록이 한 줄에 하나씩 주어진다. 입력의 끝은 "EOI"라는 문자열로 표시된다. 프로그램은 입력된 모든 항목의 비용을 합산하여 총 비용을 출력해야 한다. 출력은 반드시 달러 기호("$")로 시작하며, 소수점 아래 두 자리까지 표시되어야 한다.

### 예제 입력 1

```
Binders
Calendar
Ink
Notebooks
Binders
Ink
EOI
```

### 예제 출력 1

```
$201.05
```

## 접근 방식

이 문제는 주어진 사무용품 목록을 입력받아 각 항목의 비용을 합산하는 간단한 구현 문제이다. 해결하기 위해 다음과 같은 단계를 따른다:

1. **사무용품과 비용 매핑**: 주어진 사무용품과 비용을 효율적으로 조회할 수 있도록 자료 구조를 선택한다. 이 문제에서는 항목 이름을 키로, 비용을 값으로 하는 해시 맵(`unordered_map`)을 사용한다.

2. **입력 처리**: 표준 입력으로부터 사무용품 이름을 한 줄씩 읽어들인다. "EOI" 문자열이 입력될 때까지 반복한다.

3. **비용 합산**: 입력된 사무용품 이름이 해시 맵에 존재하면 해당 비용을 총 합계에 더한다. 존재하지 않는 항목은 무시한다.

4. **출력 형식 지정**: 최종 합계는 달러 기호("$")로 시작하고 소수점 아래 두 자리까지 표시해야 하므로, 출력 시 형식을 지정하여 출력한다.

이러한 접근 방식을 통해 문제를 효율적으로 해결할 수 있다. 시간 복잡도는 입력되는 항목의 수에 선형적으로 비례하므로 O(N)이다.

## C++ 코드와 설명

아래는 최적화된 C++ 코드로, 각 단계에 대한 주석을 포함하고 있다.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    // Initialize a map with item names and their corresponding costs
    unordered_map<string, double> items = {
        {"Paper", 57.99},
        {"Printer", 120.50},
        {"Planners", 31.25},
        {"Binders", 22.50},
        {"Calendar", 10.95},
        {"Notebooks", 11.20},
        {"Ink", 66.95}
    };
    
    double total = 0.0; // Variable to store the total cost
    string line;
    
    // Read input lines until "EOI" is encountered
    while(getline(cin, line)){
        if(line == "EOI") break; // End of input
        auto it = items.find(line);
        if(it != items.end()){
            total += it->second; // Add the cost if the item exists in the map
        }
        // If the item is not found, it is ignored
    }
    
    // Print the total cost with a dollar sign and exactly two decimal places
    printf("$%.2lf\n", total);
    
    return 0;
}
```

### 코드 동작 설명

1. **해시 맵 초기화**: `unordered_map`을 사용하여 각 사무용품 이름을 키로, 비용을 값으로 매핑한다. 이를 통해 입력된 항목의 비용을 O(1)의 시간 복잡도로 조회할 수 있다.

2. **입력 처리 루프**: `while(getline(cin, line))`을 사용하여 표준 입력으로부터 한 줄씩 입력을 받는다. 입력이 "EOI"일 경우 루프를 종료한다.

3. **비용 합산**: 입력된 `line`이 해시 맵에 존재하는지 확인하기 위해 `items.find(line)`을 사용한다. 존재하면 해당 비용을 `total`에 더한다. 존재하지 않으면 무시한다.

4. **결과 출력**: `printf`를 사용하여 총 비용을 달러 기호와 함께 소수점 아래 두 자리까지 출력한다.

이 코드는 간결하면서도 효율적으로 문제를 해결한다. 해시 맵을 사용함으로써 입력된 항목을 빠르게 조회할 수 있으며, 불필요한 항목은 자동으로 무시된다.

## C++ without library 코드와 설명

아래는 C++ 표준 라이브러리를 사용하지 않고, `stdio.h`와 `malloc.h`만을 사용하여 구현한 최적화된 코드이다.

```cpp
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct Item {
    char name[20];
    double cost;
} Item;

int main(){
    // Initialize the list of items
    Item items[] = {
        {"Paper", 57.99},
        {"Printer", 120.50},
        {"Planners", 31.25},
        {"Binders", 22.50},
        {"Calendar", 10.95},
        {"Notebooks", 11.20},
        {"Ink", 66.95}
    };
    int itemCount = sizeof(items)/sizeof(items[0]);
    
    double total = 0.0;
    char line[30];
    
    // Read each line until "EOI" is encountered
    while(scanf("%s", line) != EOF){
        if(strcmp(line, "EOI") == 0) break; // End of input
        // Iterate through the items to find a match
        for(int i=0; i<itemCount; i++){
            if(strcmp(line, items[i].name) == 0){
                total += items[i].cost; // Add the cost if matched
                break; // Move to the next input line
            }
        }
    }
    
    // Print the total cost with dollar sign and two decimal places
    printf("$%.2lf\n", total);
    
    return 0;
}
```

### 코드 동작 설명

1. **아이템 구조체 정의**: `Item` 구조체를 정의하여 각 사무용품의 이름과 비용을 저장한다.

2. **아이템 리스트 초기화**: 사전에 정의된 사무용품과 그 비용을 `items` 배열에 저장한다. 배열의 크기를 계산하여 `itemCount`에 저장한다.

3. **입력 처리 루프**: `scanf`를 사용하여 표준 입력으로부터 문자열을 한 번에 하나씩 읽어들인다. 입력이 "EOI"일 경우 루프를 종료한다.

4. **비용 합산**: 입력된 `line`과 `items` 배열의 각 항목을 `strcmp`로 비교하여 일치하는 항목을 찾는다. 일치하는 항목을 찾으면 해당 비용을 `total`에 더하고, 다음 입력으로 넘어간다.

5. **결과 출력**: `printf`를 사용하여 총 비용을 달러 기호와 함께 소수점 아래 두 자리까지 출력한다.

이 코드는 표준 라이브러리를 사용하지 않고, 기본적인 C 함수를 활용하여 구현되었다. 해시 맵을 사용하지 않았기 때문에 항목을 찾기 위해 선형 탐색을 사용하지만, 아이템의 수가 적기 때문에 성능에 큰 영향을 주지 않는다.

## Python 코드와 설명

아래는 최적화된 Python 코드로, 각 단계에 대한 주석을 포함하고 있다.

```python
# Initialize a dictionary with item names and their corresponding costs
items = {
    "Paper": 57.99,
    "Printer": 120.50,
    "Planners": 31.25,
    "Binders": 22.50,
    "Calendar": 10.95,
    "Notebooks": 11.20,
    "Ink": 66.95
}

total = 0.0  # Variable to store the total cost

while True:
    try:
        line = input().strip()  # Read input line and remove leading/trailing whitespaces
        if line == "EOI":
            break  # End of input
        if line in items:
            total += items[line]  # Add the cost if the item exists in the dictionary
        # If the item is not found, it is ignored
    except EOFError:
        break  # Handle unexpected end of input

# Print the total cost with a dollar sign and exactly two decimal places
print(f"${total:.2f}")
```

### 코드 동작 설명

1. **딕셔너리 초기화**: Python의 `dict`를 사용하여 각 사무용품 이름을 키로, 비용을 값으로 매핑한다. 이를 통해 입력된 항목의 비용을 O(1)의 시간 복잡도로 조회할 수 있다.

2. **입력 처리 루프**: `while True` 루프를 사용하여 표준 입력으로부터 한 줄씩 입력을 받는다. 입력이 "EOI"일 경우 루프를 종료한다. 예기치 않은 입력 종료(`EOFError`)도 처리하여 프로그램이 안정적으로 종료되도록 한다.

3. **비용 합산**: 입력된 `line`이 딕셔너리에 존재하는지 확인한 후, 존재하면 해당 비용을 `total`에 더한다. 존재하지 않는 항목은 무시한다.

4. **결과 출력**: `print` 함수와 포매팅을 사용하여 총 비용을 달러 기호와 함께 소수점 아래 두 자리까지 출력한다.

이 Python 코드는 간결하고 이해하기 쉬우며, Python의 내장 자료 구조와 함수들을 효과적으로 활용하여 문제를 해결한다.

## 결론

이번 포스트에서는 백준 온라인 저지의 문제 5342번 "Billing 다국어"를 다양한 프로그래밍 언어로 구현하고 설명하였다. 문제는 사무용품의 구매 목록을 입력받아 총 비용을 계산하는 간단한 구현 문제였지만, 효율적인 자료 구조 선택과 입력 처리가 중요하였다.

C++을 사용할 때는 `unordered_map`을 활용하여 빠른 조회를 구현하였고, 표준 라이브러리를 사용하지 않는 경우에는 선형 탐색을 통해 문제를 해결하였다. Python에서는 딕셔너리를 활용하여 더욱 간결하게 구현할 수 있었다.

추가적으로, 더 큰 데이터셋이나 더 많은 항목이 주어지는 경우에는 효율적인 자료 구조 선택이 더욱 중요해질 것이다. 또한, 입력 데이터의 형식이 다양해질 경우, 입력 처리 방식을 유연하게 설계하는 것이 필요하다. 이번 문제를 통해 기본적인 구현 능력과 자료 구조 활용 능력을 향상시킬 수 있었다.