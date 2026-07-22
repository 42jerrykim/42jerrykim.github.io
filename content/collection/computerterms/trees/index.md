---
image: "wordcloud.png"
slug: trees
collection_order: 8
draft: false
title: "[Computer Terms] 트리 (Tree)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "트리는 노드 사이에 계층 관계를 갖는 자료구조로, 이진 탐색 트리와 균형 트리를 중심으로 순회 방식·탐색 성능·불균형 문제를 C 코드와 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Data-Structure(자료구조)
- Tree(트리)
- Binary-Search-Tree(이진탐색트리)
- Recursion(재귀)
- Array(배열)
- Linked-List(연결리스트)
- C
- Time-Complexity(시간복잡도)
- Algorithm(알고리즘)
- Reference(참고)
- Documentation(문서화)
- Tutorial(튜토리얼)
- Guide(가이드)
- Beginner
- Computer-Science(컴퓨터과학)
- Fundamentals(기초)
- Best-Practices
- Comparison(비교)
- Deep-Dive
- Case-Study
- Software-Engineering(소프트웨어공학)
- Debugging(디버깅)
- Performance(성능)
- Implementation(구현)
---

## 이 장을 읽기 전에

[배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)의 포인터 기반 노드 구조와, [스택과 큐](/post/computerterms/stacks-and-queues/)에서 다룬 순회용 자료구조(호출 스택, 큐)를 안다고 가정한다. 트리는 연결리스트의 "노드가 다음 노드 하나를 가리킨다"는 규칙을 "노드가 자식 노드 여러 개를 가리킨다"로 확장한 것이므로, 연결리스트를 계층 구조로 일반화한 자료구조로 접근한다.

## 왜 계층 구조가 필요한가

배열과 연결리스트, 스택과 큐는 모두 원소들이 **한 줄로** 나열된다는 공통점이 있다. 그런데 파일 시스템의 폴더 구조, 조직도, HTML 문서의 태그 중첩처럼 현실의 많은 데이터는 "부모 아래에 여러 자식이 있다"는 계층 관계를 갖는다. 이런 관계를 배열이나 단순 연결리스트로 표현하려 하면 부모-자식 관계를 별도 필드로 흉내 내야 해서 부자연스럽다. **트리(Tree)**는 이 계층 관계를 자료구조 자체의 형태로 표현한다.

## 트리의 정의와 용어

트리는 하나의 **루트(Root)** 노드에서 시작해, 각 노드가 0개 이상의 **자식(Child)** 노드를 가리키는 구조다. 자식이 없는 노드를 **리프(Leaf)**라 하고, 루트에서 어떤 노드까지의 경로 길이를 그 노드의 **깊이(Depth)**, 루트에서 가장 먼 리프까지의 깊이를 트리의 **높이(Height)**라 한다. 트리는 정의상 사이클이 없다 — 자식에서 다시 조상으로 돌아가는 간선이 있다면 그것은 트리가 아니라 그래프다.

각 노드가 자식을 최대 2개까지만 가질 수 있는 트리를 **이진 트리(Binary Tree)**라 하며, 여기에 "왼쪽 서브트리의 모든 값은 현재 노드보다 작고, 오른쪽 서브트리의 모든 값은 크다"는 정렬 규칙을 추가한 것이 **이진 탐색 트리(Binary Search Tree, BST)**다.

## 이진 탐색 트리의 삽입과 탐색

BST의 핵심은 이 정렬 규칙 덕분에, 매 노드에서 "찾는 값이 더 작은가 큰가"만 비교해 왼쪽 또는 오른쪽으로만 내려가면 된다는 것이다. 이 과정은 정렬된 배열의 이진 탐색과 원리가 같지만, 트리는 삽입 시 배열처럼 뒤쪽 원소를 옮길 필요가 없다.

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int value;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

TreeNode *bst_insert(TreeNode *root, int value) {
    if (root == NULL) {
        TreeNode *node = malloc(sizeof(TreeNode));
        node->value = value;
        node->left = node->right = NULL;
        return node;
    }
    if (value < root->value) {
        root->left = bst_insert(root->left, value);
    } else if (value > root->value) {
        root->right = bst_insert(root->right, value);
    }
    /* value == root->value 인 경우 중복이므로 그대로 반환 */
    return root;
}

TreeNode *bst_search(TreeNode *root, int value) {
    if (root == NULL || root->value == value) return root;
    if (value < root->value) return bst_search(root->left, value);
    return bst_search(root->right, value);
}

void inorder_print(const TreeNode *root) {
    if (root == NULL) return;
    inorder_print(root->left);
    printf("%d ", root->value);
    inorder_print(root->right);
}

int main(void) {
    TreeNode *root = NULL;
    int values[] = {5, 3, 8, 1, 4, 7, 9};
    for (size_t i = 0; i < sizeof(values) / sizeof(values[0]); i++) {
        root = bst_insert(root, values[i]);
    }

    inorder_print(root);   /* 1 3 4 5 7 8 9 : 항상 오름차순 */
    printf("\n");

    TreeNode *found = bst_search(root, 7);
    printf("7 found: %s\n", found != NULL ? "yes" : "no");
    return 0;
}
```

`inorder_print`(왼쪽 → 현재 → 오른쪽 순회)가 항상 오름차순으로 출력되는 것은 우연이 아니라 BST 정렬 규칙의 직접적인 결과다. 이 성질 때문에 BST를 "정렬된 상태를 유지하면서 삽입·삭제가 가능한 자료구조"로 설명하기도 한다.

## 트리 순회의 세 가지 방식

트리 순회는 방문 순서에 따라 이름이 다르다. **전위 순회(Preorder)**는 현재 노드 → 왼쪽 → 오른쪽 순으로, 트리 구조 자체를 복제하거나 직렬화할 때 쓴다. **중위 순회(Inorder)**는 왼쪽 → 현재 → 오른쪽 순으로, BST에서는 항상 정렬된 값을 낸다. **후위 순회(Postorder)**는 왼쪽 → 오른쪽 → 현재 노드 순으로, 자식을 모두 처리한 뒤에야 부모를 처리해야 하는 경우(예: 디렉터리 삭제, 트리 메모리 해제)에 쓴다. 세 방식 모두 재귀 호출 자체가 [스택과 큐](/post/computerterms/stacks-and-queues/)에서 다룬 호출 스택을 사용하는 깊이 우선 순회다.

## 균형이 깨지면 생기는 문제

BST의 탐색·삽입·삭제는 이론적으로 O(log n)이지만, 이는 트리가 **균형(balanced)**을 이룰 때만 성립한다. 정렬된 값을 순서대로 삽입하면(1, 2, 3, 4, 5...) 모든 노드가 오른쪽 자식만 갖는 사실상의 연결리스트가 되어 탐색이 O(n)으로 퇴화한다. 이 문제를 막기 위해 삽입·삭제 시 자동으로 균형을 재조정하는 **AVL 트리**, **레드-블랙 트리** 같은 균형 이진 탐색 트리가 존재한다. C++ `std::map`, Java `TreeMap`은 내부적으로 레드-블랙 트리를 사용해 최악의 경우에도 O(log n)을 보장한다.

## 비교: 배열/연결리스트/트리

| 특성 | 정렬된 배열 | 연결리스트 | 균형 BST |
|---|---|---|---|
| 탐색 | O(log n) | O(n) | O(log n) |
| 삽입(정렬 유지) | O(n) (이동) | O(n) (탐색) + O(1) | O(log n) |
| 순서대로 순회 | O(n) | O(n) | O(n) (중위 순회) |
| 최솟값/최댓값 | O(1) (끝 인덱스) | O(n) | O(log n) (가장 왼쪽/오른쪽) |

## 흔한 오개념

**"이진 탐색 트리는 항상 O(log n)이다"** — 삽입 순서에 따라 트리가 편향되면 O(n)으로 퇴화한다는 사실을 빼먹은 채 이름만 보고 성능을 단정하는 오해다. 입력이 이미 정렬돼 있거나 정렬에 가까운 경우 이 퇴화가 특히 쉽게 일어나므로, 입력 분포를 통제할 수 없는 상황에서는 처음부터 균형 트리를 쓰는 것이 안전하다.

**"트리 순회는 재귀로만 구현할 수 있다"** — 재귀는 컴파일러가 호출 스택을 자동으로 관리해주는 구현일 뿐, 원리상 [스택과 큐](/post/computerterms/stacks-and-queues/)에서 다룬 사용자 정의 스택으로 반복문 기반 순회를 그대로 구현할 수 있다. 트리 깊이가 매우 깊어 재귀 호출 스택 오버플로가 우려되는 상황(예: 파싱 트리, 대량 계층 데이터)에서는 반복문 구현이 실무적으로 더 안전하다.

## 다른 개념과의 연결

다음에 다룰 [해시테이블](/post/computerterms/hash-tables/)은 평균 O(1) 탐색으로 균형 BST의 O(log n)보다 빠르지만, 정렬된 순서로 순회하는 기능을 잃는다는 트레이드오프가 있다 — "정렬이 필요한가"가 둘 중 하나를 고르는 핵심 판단 기준이 된다. [그래프](/post/computerterms/graphs/) 챕터에서는 트리가 "사이클이 없는 연결 그래프"의 특수한 경우임을 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 이진 탐색 트리가 탐색에 O(log n)을 보장하는 조건(균형)과, 그 조건이 깨지는 입력 패턴을 설명할 수 있다. 전위·중위·후위 순회 중 어떤 것이 어떤 용도(직렬화, 정렬 출력, 메모리 해제)에 맞는지 선택할 수 있다. 정렬된 배열, 연결리스트, 균형 BST 중 상황에 맞는 자료구조를 근거와 함께 고를 수 있다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Chapter 12–13: Binary Search Trees, Red-Black Trees. MIT Press.

- [cppreference: std::map](https://en.cppreference.com/w/cpp/container/map) — 레드-블랙 트리 기반 균형 트리의 실제 표준 라이브러리 구현
- [Visualgo: Binary Search Tree](https://visualgo.net/en/bst) — BST 삽입·삭제·균형 붕괴 과정을 시각적으로 확인할 수 있는 자료
