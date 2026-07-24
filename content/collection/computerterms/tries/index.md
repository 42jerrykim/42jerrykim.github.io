---
image: "wordcloud.png"
slug: tries
collection_order: 46
draft: false
title: "[Computer Terms] 트라이 (Trie, Prefix Tree)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "트라이는 문자열을 문자 단위 트리로 저장해 접두사 검색을 빠르게 처리하는 자료구조입니다. 해시테이블 대비 자동완성에 유리한 이유를 C 코드와 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Data-Structure(자료구조)
- Trie
- Tree(트리)
- Hash-Table(해시테이블)
- String(문자열)
- Array(배열)
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

[해시테이블](/post/computerterms/hash-tables/)의 평균 O(1) 탐색과 해시 충돌 개념, [트리](/post/computerterms/trees/)의 노드·자식·리프 용어, [힙과 우선순위 큐](/post/computerterms/heaps-and-priority-queues/)에서 다룬 "특정 연산 하나에 특화된 트리" 개념을 안다고 가정한다. 트라이는 힙이 "최솟값"에 특화됐듯 "문자열 접두사"에 특화된 트리다.

## 자동완성은 왜 해시테이블만으로 부족한가

검색창에 "app"까지 입력했을 때 "apple", "application", "apply"를 추천하는 자동완성 기능을 해시테이블로 구현한다고 해보자. 해시테이블은 키 전체를 해시 함수에 넣어 인덱스를 만들기 때문에, "app"이라는 부분 문자열과 "apple"이라는 전체 문자열은 해시값이 완전히 무관하다. 즉 "app으로 시작하는 모든 단어"를 찾으려면 저장된 모든 키를 순회하며 접두사를 일일이 비교하는 O(n·m) 작업(n은 저장된 단어 수, m은 접두사 길이)이 필요하다. **트라이(Trie, Prefix Tree)**는 문자열을 "문자 하나당 간선 하나"로 트리에 펼쳐 저장해서, 접두사 검색을 트리를 한 번 내려가는 것만으로 끝낸다.

## 트라이의 정의: 문자 단위 트리

트라이는 루트에서 시작해 각 간선이 문자 하나를 나타내는 트리다. 루트에서 어떤 노드까지의 경로에 놓인 문자들을 순서대로 이으면 그 노드가 나타내는 문자열이 된다. 예를 들어 "cat"을 저장하면 루트 → `c` → `a` → `t` 순서로 노드 3개가 생기고, 이어서 "car"를 저장하면 `c`, `a` 노드는 재사용하고 `t` 옆에 `r` 자식만 새로 추가한다. 이렇게 **공통 접두사를 가진 문자열은 트리의 같은 경로를 공유**한다는 것이 트라이의 핵심 성질이다. 문자열의 끝을 표시하기 위해 각 노드에는 보통 `is_end`(또는 `is_word`) 플래그를 둔다 — 이 플래그가 없으면 "car"가 저장됐는지, "car"가 "carpet"의 접두사로만 존재하는지 구분할 수 없다.

## 삽입과 탐색

삽입은 문자열을 한 글자씩 따라가며, 해당 문자로 가는 자식이 없으면 새로 만들고 있으면 재사용하는 과정이다. 문자열 끝에 도달하면 그 노드의 `is_end`를 표시한다. 탐색(정확한 단어 존재 여부)도 같은 경로를 따라가되, 중간에 자식이 없으면 즉시 실패하고, 끝까지 도달했을 때 `is_end`가 표시돼 있어야 성공이다. 두 연산 모두 문자열 길이 m에 대해 O(m)이며, 저장된 단어 수 n과 무관하다는 점이 해시테이블과 다르다 — 해시테이블도 평균 O(m)(해시 계산 비용)이지만, 접두사 검색으로 확장하면 트라이만 O(p + k)(p는 접두사 길이, k는 결과 수)를 유지하고 해시테이블은 전체 순회가 필요해진다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ALPHABET_SIZE 26

typedef struct TrieNode {
    struct TrieNode *children[ALPHABET_SIZE];
    int is_end;
} TrieNode;

TrieNode *trie_create_node(void) {
    TrieNode *node = malloc(sizeof(TrieNode));
    node->is_end = 0;
    for (int i = 0; i < ALPHABET_SIZE; i++) node->children[i] = NULL;
    return node;
}

void trie_insert(TrieNode *root, const char *word) {
    TrieNode *cur = root;
    for (size_t i = 0; word[i] != '\0'; i++) {
        int idx = word[i] - 'a';
        if (cur->children[idx] == NULL) {
            cur->children[idx] = trie_create_node();
        }
        cur = cur->children[idx];
    }
    cur->is_end = 1;
}

/* 정확한 단어 존재 여부 : O(단어 길이) */
int trie_search(TrieNode *root, const char *word) {
    TrieNode *cur = root;
    for (size_t i = 0; word[i] != '\0'; i++) {
        int idx = word[i] - 'a';
        if (cur->children[idx] == NULL) return 0;
        cur = cur->children[idx];
    }
    return cur->is_end;
}

/* 접두사로 시작하는 단어가 하나라도 있는지 : O(접두사 길이) */
int trie_starts_with(TrieNode *root, const char *prefix) {
    TrieNode *cur = root;
    for (size_t i = 0; prefix[i] != '\0'; i++) {
        int idx = prefix[i] - 'a';
        if (cur->children[idx] == NULL) return 0;
        cur = cur->children[idx];
    }
    return 1;
}

int main(void) {
    TrieNode *root = trie_create_node();
    trie_insert(root, "cat");
    trie_insert(root, "car");
    trie_insert(root, "card");

    printf("search 'car': %d\n", trie_search(root, "car"));       /* 1 */
    printf("search 'ca': %d\n", trie_search(root, "ca"));         /* 0: 저장된 단어가 아님 */
    printf("starts_with 'ca': %d\n", trie_starts_with(root, "ca")); /* 1: cat/car/card 접두사 */
    return 0;
}
```

`trie_search`와 `trie_starts_with`가 구조는 거의 같지만 반환 조건이 다른 이유가 트라이 이해의 핵심이다. `search`는 경로 끝 노드의 `is_end`까지 확인해야 "완전한 단어"임을 보장하지만, `starts_with`는 경로가 끝까지 이어지기만 하면 되므로 `is_end`를 보지 않는다. "ca"가 저장된 단어는 아니지만 접두사로는 존재한다는 결과가 이 차이에서 나온다.

## 메모리 트레이드오프: 배열 vs 맵

위 구현은 각 노드가 알파벳 크기(26)만큼의 포인터 배열을 갖는다. 이 방식은 자식 접근이 인덱스 연산 O(1)로 끝나 빠르지만, 실제로 자식이 1~2개뿐인 노드에서도 26칸을 전부 할당해 메모리를 낭비한다. 대안으로 각 노드가 (문자 → 자식) **해시맵**이나 정렬된 배열을 쓰면, 실제 존재하는 자식 수만큼만 메모리를 쓰지만 자식 접근이 해시 계산 또는 이진 탐색만큼 느려진다. 유니코드처럼 알파벳 크기가 수만에 달하는 언어를 다뤄야 한다면 고정 배열 방식은 사실상 불가능하므로 맵 기반 구현이 필수적이다.

## 비교: 해시테이블 vs 트라이

| 특성 | 해시테이블 | 트라이 |
|---|---|---|
| 정확한 단어 탐색 | 평균 O(m) | O(m) |
| 접두사로 시작하는 단어 검색 | O(n·m) — 전체 순회 필요 | O(p + k) — p는 접두사 길이, k는 결과 수 |
| 메모리(배열 기반 자식) | O(총 문자 수) | O(총 노드 수 × 알파벳 크기) — 공유 접두사만큼 절약 |
| 정렬된 순서로 순회 | 지원 안 함 | 지원 (DFS로 사전순 순회) |
| 구현 복잡도 | 낮음 (표준 라이브러리 다수 제공) | 중간 (직접 구현 필요한 경우 많음) |

## 흔한 오개념

**"트라이는 항상 해시테이블보다 메모리 효율적이다"** — 공통 접두사가 많은 단어 집합(사전, URL 경로)에서는 경로 공유 덕분에 트라이가 유리하지만, 공통 접두사가 거의 없는 무작위 문자열 집합에서는 오히려 트라이가 더 많은 노드를 만들어 해시테이블보다 메모리를 많이 쓸 수 있다. 알파벳 크기가 큰 배열 기반 구현이라면 이 낭비가 더 커진다.

**"트라이 탐색은 저장된 단어 수에 비례해 느려진다"** — 트라이의 탐색·삽입 시간은 저장된 단어 개수(n)가 아니라 찾는 문자열의 길이(m)에만 비례한다. 해시테이블처럼 해시 충돌이 늘어나 성능이 저하되는 현상이 트라이에는 없다 — 다만 이는 각 노드의 자식 접근이 O(1)이라는 전제(배열 기반)에서만 성립하며, 맵 기반 구현이라면 그 맵 자체의 접근 비용이 더해진다.

## 다른 개념과의 연결

트라이는 [트리](/post/computerterms/trees/)의 일종이지만 "값의 크기 순서"가 아니라 "문자 경로"로 구조가 결정된다는 점에서 [힙과 우선순위 큐](/post/computerterms/heaps-and-priority-queues/)나 이진 탐색 트리와 근본적으로 다른 설계 목표를 갖는다. 다음 장에서 다룰 **유니온-파인드**는 트리 구조를 완전히 다른 목적(집합의 소속 관계 관리)으로 활용하는 사례를 보여준다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 트라이가 공통 접두사를 공유하는 원리와, 이 덕분에 접두사 검색이 해시테이블보다 유리한 이유를 설명할 수 있다. `is_end` 플래그가 왜 필요한지, 이것이 없을 때 어떤 구분이 불가능해지는지 설명할 수 있다. 알파벳 크기와 데이터 특성(공통 접두사 비율)에 따라 배열 기반과 맵 기반 자식 표현 중 무엇을 선택할지 근거를 들어 판단할 수 있다.

## 참고 자료

> Fredkin, E. (1960). Trie Memory. *Communications of the ACM*, 3(9), 490–499.

- [cppreference: std::map](https://en.cppreference.com/w/cpp/container/map) — 맵 기반 트라이 자식 표현에 활용할 수 있는 표준 컨테이너
- [Wikipedia: Trie](https://en.wikipedia.org/wiki/Trie) — 트라이의 변형(압축 트라이, radix tree 등)과 응용 사례 정리
