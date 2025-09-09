---
image: "tmp_wordcloud.png"
categories: Algorithm
date: "2024-10-10T00:00:00Z"
header:
  teaser: /assets/images/undefined/algorithm.png
tags:
- Trie
- DFS
- Recursion
- DataStructures
- StringProcessing
title: '[Algorithm] C++/Python 백준 14725번 : 개미굴'
---

알고리즘 문제 해결에서 계층적 데이터 구조를 다루는 것은 흔한 도전 과제이다. 백준 온라인 저지의 14725번 문제인 **"개미굴"**은 이러한 계층 구조를 표현하고 탐색하기 위해 Trie 자료 구조를 활용하는 좋은 연습 문제이다. 이 글에서는 "개미굴" 문제를 분석하고, Trie를 이용한 해결 방법을 살펴보며, C++, 표준 라이브러리를 사용하지 않은 C++, 그리고 Python으로 구현한 코드를 제시하고자 한다. 이를 통해 Trie 구현과 재귀적 탐색 기법에 대한 이해를 높이고자 한다.

## 문제 소개

문제 : [https://www.acmicpc.net/problem/14725](https://www.acmicpc.net/problem/14725)

|![/assets/images/undefined/algorithm.png](/assets/images/undefined/algorithm.png)|
|:---:|
||

## 문제 설명

개미는 먹이를 저장하기 위해 복잡한 개미굴을 건설한다. 각 개미는 먹이가 있는 방을 따라 개미굴을 내려가며, 더 이상 내려갈 수 없을 때까지 이동한다. 개미는 이동하면서 지나온 방의 먹이 정보를 로봇 개미에게 전달한다.

로봇 개미는 개미들이 지나온 먹이 정보를 받아 개미굴의 구조를 파악하고자 한다. 로봇 개미가 전달하는 정보는 각 층마다 지나온 방의 먹이 이름을 순서대로 나타낸 것이다. 이를 바탕으로 개미굴의 전체 구조를 시각화해야 한다.

개미굴은 다음과 같은 규칙으로 시각화된다:

- 각 층은 `--`로 구분한다.
- 같은 층에 여러 개의 방이 있을 때는 사전 순서대로 출력한다.
- 최상위 굴부터 시작하여 하나의 굴에서 여러 개로 나뉠 때 먹이 종류별로 최대 한 번만 나온다.

**예제 입력:**

```
4
2 KIWI BANANA
2 KIWI APPLE
2 APPLE APPLE
3 APPLE BANANA KIWI
```

**예제 출력:**

```
APPLE
--APPLE
--BANANA
----KIWI
KIWI
--APPLE
--BANANA
```

위 예제에서 로봇 개미들은 각자 지나온 방의 먹이 정보를 전달한다. 우리의 목표는 이 정보를 바탕으로 개미굴의 구조를 시각화하는 것이다.

## 접근 방식

이 문제는 문자열 트리인 **Trie** 자료 구조를 활용하여 해결할 수 있다. Trie는 문자열을 효율적으로 저장하고 탐색하기 위한 트리 구조로, 공통된 접두사를 공유하는 문자열들을 효율적으로 관리할 수 있다.

**구현 전략:**

1. **Trie 구축:**
   - 각 로봇 개미가 전달한 먹이 정보를 Trie에 삽입한다.
   - Trie의 각 노드는 먹이 이름을 키로 가지며, 자식 노드들을 사전 순서대로 저장하기 위해 `map` 또는 `dictionary`를 사용한다.

2. **Trie 탐색 및 출력:**
   - DFS(Depth-First Search)를 사용하여 Trie를 탐색하면서 개미굴을 출력한다.
   - 각 노드의 깊이에 따라 `--`를 반복하여 들여쓰기를 구현한다.
   - 자식 노드들은 사전 순서대로 방문하여 출력 규칙을 만족한다.

3. **주의사항:**
   - 동일한 경로가 중복되지 않도록 Trie에 삽입 시 확인한다.
   - 메모리 및 시간 효율성을 고려하여 자료 구조를 선택한다.

## C++ 코드와 설명

```cpp
#include <iostream>
#include <map>
#include <vector>
#include <string>
using namespace std;

// Trie의 노드 구조체 정의
struct Node {
    map<string, Node*> children; // 자식 노드들을 사전 순으로 저장
};

// Trie에 먹이 정보를 삽입하는 함수
void insert(Node* root, const vector<string>& foods) {
    Node* current = root;
    for (const string& food : foods) {
        // 자식 노드에 해당 먹이 이름이 없으면 새로 생성
        if (current->children.find(food) == current->children.end()) {
            current->children[food] = new Node();
        }
        // 현재 노드를 자식 노드로 이동
        current = current->children[food];
    }
}

// Trie를 DFS로 탐색하며 개미굴 구조를 출력하는 함수
void dfs(Node* node, int depth) {
    for (const auto& child : node->children) {
        // 현재 깊이에 따라 '--'를 출력하여 들여쓰기 구현
        for (int i = 0; i < depth; ++i) {
            cout << "--";
        }
        // 먹이 이름 출력
        cout << child.first << '\n';
        // 재귀적으로 자식 노드 방문
        dfs(child.second, depth + 1);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N; // 로봇 개미의 수
    cin >> N;
    Node* root = new Node(); // Trie의 루트 노드 생성

    for (int i = 0; i < N; ++i) {
        int K; // 먹이 정보의 개수
        cin >> K;
        vector<string> foods(K);
        for (int j = 0; j < K; ++j) {
            cin >> foods[j]; // 먹이 이름 입력
        }
        insert(root, foods); // Trie에 먹이 정보 삽입
    }

    dfs(root, 0); // Trie 탐색 및 출력

    return 0;
}
```

**코드 설명**

- **구조체 `Node` 정의:**
  - 각 노드는 `map<string, Node*> children`을 멤버로 가지며, 이는 자식 노드들을 사전 순으로 저장한다.

- **함수 `insert`:**
  - 루트 노드와 먹이 정보 벡터를 인자로 받아 Trie에 삽입한다.
  - 현재 노드에서 해당 먹이 이름을 가진 자식 노드가 없으면 새로 생성한다.
  - 먹이 이름을 따라 자식 노드로 이동한다.

- **함수 `dfs`:**
  - 현재 노드의 자식들을 순회하며 깊이에 따라 `--`를 출력한다.
  - 재귀적으로 자식 노드를 방문하여 전체 Trie를 탐색한다.

- **`main` 함수:**
  - 입력을 받아 Trie를 구축하고, DFS를 통해 개미굴 구조를 출력한다.
  - `ios::sync_with_stdio(false);`와 `cin.tie(nullptr);`를 통해 입출력 속도를 향상시킨다.

## C++ without library 코드와 설명

```cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Trie의 노드 구조체 정의
typedef struct Node {
    char* food; // 현재 노드의 먹이 이름
    struct Node** children; // 자식 노드들
    int childCount; // 자식 노드의 수
    int capacity; // 자식 노드 배열의 용량
} Node;

// 노드 생성 함수
Node* createNode(char* food) {
    Node* node = (Node*)malloc(sizeof(Node));
    node->food = food ? strdup(food) : NULL;
    node->children = NULL;
    node->childCount = 0;
    node->capacity = 0;
    return node;
}

// 자식 노드 추가 함수
void addChild(Node* parent, Node* child) {
    // 자식 노드 배열 확장
    if (parent->childCount == parent->capacity) {
        parent->capacity = parent->capacity ? parent->capacity * 2 : 4;
        parent->children = (Node**)realloc(parent->children, sizeof(Node*) * parent->capacity);
    }
    // 자식 노드 추가
    parent->children[parent->childCount++] = child;
}

// 자식 노드들 정렬 함수
int compare(const void* a, const void* b) {
    Node* nodeA = *(Node**)a;
    Node* nodeB = *(Node**)b;
    return strcmp(nodeA->food, nodeB->food);
}

// Trie에 먹이 정보를 삽입하는 함수
void insert(Node* root, char foods[][16], int k) {
    Node* current = root;
    for (int i = 0; i < k; ++i) {
        int found = 0;
        for (int j = 0; j < current->childCount; ++j) {
            if (strcmp(current->children[j]->food, foods[i]) == 0) {
                current = current->children[j];
                found = 1;
                break;
            }
        }
        if (!found) {
            Node* child = createNode(foods[i]);
            addChild(current, child);
            current = child;
        }
    }
}

// Trie를 DFS로 탐색하며 개미굴 구조를 출력하는 함수
void dfs(Node* node, int depth) {
    // 자식 노드들 정렬
    qsort(node->children, node->childCount, sizeof(Node*), compare);
    for (int i = 0; i < node->childCount; ++i) {
        for (int j = 0; j < depth; ++j) {
            printf("--");
        }
        printf("%s\n", node->children[i]->food);
        dfs(node->children[i], depth + 1);
    }
}

// 메모리 해제 함수
void freeNode(Node* node) {
    for (int i = 0; i < node->childCount; ++i) {
        freeNode(node->children[i]);
    }
    free(node->food);
    free(node->children);
    free(node);
}

int main() {
    int N;
    scanf("%d", &N);
    Node* root = createNode(NULL);

    for (int i = 0; i < N; ++i) {
        int K;
        scanf("%d", &K);
        char foods[15][16];
        for (int j = 0; j < K; ++j) {
            scanf("%s", foods[j]);
        }
        insert(root, foods, K);
    }

    dfs(root, 0);
    freeNode(root);

    return 0;
}
```

**코드 설명**

- **구조체 `Node` 정의:**
  - `char* food`: 현재 노드의 먹이 이름을 저장한다.
  - `Node** children`: 자식 노드들의 포인터 배열을 저장한다.
  - `int childCount`, `int capacity`: 자식 노드의 수와 배열의 용량을 관리한다.

- **함수 `createNode`:**
  - 새로운 노드를 생성하고 초기화한다.

- **함수 `addChild`:**
  - 자식 노드 배열의 용량이 부족하면 `realloc`으로 확장한다.
  - 새로운 자식 노드를 추가한다.

- **함수 `insert`:**
  - 입력된 먹이 정보를 Trie에 삽입한다.
  - 현재 노드의 자식 중에 해당 먹이 이름이 있는지 검색한다.
  - 없으면 새로운 노드를 생성하여 추가한다.

- **함수 `compare`:**
  - `qsort`를 위한 비교 함수로, 자식 노드들을 사전 순으로 정렬한다.

- **함수 `dfs`:**
  - 자식 노드들을 정렬하고, 재귀적으로 방문하며 개미굴 구조를 출력한다.

- **함수 `freeNode`:**
  - 동적으로 할당된 메모리를 해제한다.

- **`main` 함수:**
  - 입력을 받아 Trie를 구축하고, DFS를 통해 개미굴 구조를 출력한다.
  - 메모리 누수를 방지하기 위해 `freeNode`를 호출하여 메모리를 해제한다.

## Python 코드와 설명

```python
import sys
sys.setrecursionlimit(10**6)

class Node:
    def __init__(self):
        self.children = {}

def insert(root, foods):
    current = root
    for food in foods:
        if food not in current.children:
            current.children[food] = Node()
        current = current.children[food]

def dfs(node, depth):
    for food in sorted(node.children.keys()):
        print('--' * depth + food)
        dfs(node.children[food], depth + 1)

def main():
    N = int(sys.stdin.readline())
    root = Node()
    for _ in range(N):
        inputs = sys.stdin.readline().split()
        K = int(inputs[0])
        foods = inputs[1:]
        insert(root, foods)
    dfs(root, 0)

if __name__ == "__main__":
    main()
```

**코드 설명**

- **클래스 `Node`:**
  - `children` 딕셔너리를 멤버로 가지며, 자식 노드들을 저장한다.

- **함수 `insert`:**
  - 루트 노드와 먹이 리스트를 받아 Trie에 삽입한다.
  - 자식 노드에 해당 먹이 이름이 없으면 새로운 노드를 생성한다.

- **함수 `dfs`:**
  - 자식 노드들의 키(먹이 이름)를 사전 순으로 정렬하여 순회한다.
  - 깊이에 따라 `'--'`를 반복하여 들여쓰기를 구현한다.
  - 재귀적으로 자식 노드를 방문한다.

- **함수 `main`:**
  - 표준 입력을 받아 Trie를 구축하고, DFS를 통해 개미굴 구조를 출력한다.
  - `sys.setrecursionlimit(10**6)`를 통해 재귀 한도를 늘려 스택 오버플로를 방지한다.

## 결론

이 문제는 Trie 자료 구조와 DFS 탐색을 활용하여 문자열 계층 구조를 효율적으로 구성하고 출력하는 방법을 연습할 수 있었다. Trie를 사용함으로써 공통된 접두사를 가진 경로들을 효과적으로 관리할 수 있었으며, 사전 순서대로 정렬하여 출력 규칙을 만족시켰다.

구현 과정에서 메모리 관리와 입출력 최적화의 중요성을 다시 한 번 느낄 수 있었다. 특히, C++에서 `map`과 같은 STL 컨테이너를 사용하지 않고 구현할 때는 자료 구조와 메모리 관리에 더욱 신경 써야 했다.

추가적으로, 입력 데이터의 크기가 커질 경우를 대비하여 입출력 속도를 향상시키는 방법과 재귀 호출의 깊이에 따른 스택 오버플로를 방지하는 방법을 고려해야 한다는 점도 알게 되었다.

이번 문제를 통해 문자열 처리와 트리 구조에 대한 이해를 더욱 깊게 할 수 있었으며, 다양한 언어로 구현해 봄으로써 각 언어의 특징과 장단점을 비교해 볼 수 있었다.