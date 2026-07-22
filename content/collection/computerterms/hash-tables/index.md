---
image: "wordcloud.png"
slug: hash-tables
collection_order: 9
draft: false
title: "[Computer Terms] 해시테이블 (Hash Table)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "해시테이블은 해시 함수로 키를 배열 인덱스로 변환해 평균 O(1) 탐색을 제공하는 자료구조입니다. 해시 충돌 처리 방식과 균형 트리 대비 트레이드오프를 C 코드와 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Data-Structure(자료구조)
- Hash-Table(해시테이블)
- Hashing(해싱)
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

[배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)의 O(1) 인덱스 접근과, [트리](/post/computerterms/trees/)에서 다룬 균형 BST의 O(log n) 탐색을 안다고 가정한다. 해시테이블은 "배열의 O(1) 접근을, 정수 인덱스가 아니라 임의의 키(문자열 등)에도 쓸 수 있게 만들면 어떨까"라는 질문에서 출발한다.

## 왜 배열의 인덱스 접근을 임의의 키로 확장하려 하는가

배열은 인덱스가 정수일 때만 O(1) 접근을 제공한다. 그런데 실무에서 찾고 싶은 대상은 "이메일 주소로 사용자 찾기", "단어로 사전 뜻 찾기"처럼 정수가 아닌 키인 경우가 대부분이다. 균형 BST를 쓰면 임의의 키로도 O(log n) 탐색이 가능하지만, 정렬 순서를 유지하는 대가로 매 탐색마다 트리 높이만큼 비교 연산을 거쳐야 한다. **해시테이블(Hash Table)**은 키를 **해시 함수(Hash Function)**로 정수 인덱스로 변환해, 배열의 O(1) 접근 성질을 임의의 키에도 그대로 적용한다.

## 해시 함수와 충돌

해시 함수는 임의의 키를 고정된 범위의 정수(배열 인덱스)로 매핑한다. 문제는 키의 가짓수가 배열 크기보다 훨씬 많으므로, 서로 다른 두 키가 같은 인덱스로 매핑되는 **충돌(Collision)**이 필연적으로 발생한다는 점이다. 해시테이블의 설계는 대부분 "이 충돌을 어떻게 처리할 것인가"의 문제로 귀결된다.

가장 널리 쓰이는 방식은 **체이닝(Chaining)**이다. 각 배열 칸(버킷)에 값을 직접 저장하는 대신, 같은 인덱스로 매핑된 키들을 [연결리스트](/post/computerterms/arrays-and-linked-lists/)로 엮어 저장한다. 충돌이 나도 데이터를 잃지 않고, 버킷마다 리스트 길이가 다르더라도 삽입 자체는 항상 O(1)이다.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUCKET_COUNT 16

typedef struct Entry {
    char *key;
    int value;
    struct Entry *next;   /* 체이닝: 같은 버킷의 다음 엔트리 */
} Entry;

typedef struct {
    Entry *buckets[BUCKET_COUNT];
} HashTable;

/* djb2 해시 함수: 문자열을 순회하며 값을 누적 */
unsigned int hash(const char *key) {
    unsigned int h = 5381;
    while (*key) {
        h = h * 33 + (unsigned char)(*key++);
    }
    return h % BUCKET_COUNT;
}

void ht_init(HashTable *ht) {
    memset(ht->buckets, 0, sizeof(ht->buckets));
}

void ht_set(HashTable *ht, const char *key, int value) {
    unsigned int idx = hash(key);
    for (Entry *e = ht->buckets[idx]; e != NULL; e = e->next) {
        if (strcmp(e->key, key) == 0) {   /* 이미 존재하는 키면 값만 갱신 */
            e->value = value;
            return;
        }
    }
    Entry *entry = malloc(sizeof(Entry));
    entry->key = strdup(key);
    entry->value = value;
    entry->next = ht->buckets[idx];       /* 버킷 맨 앞에 삽입 (push_front와 동일) */
    ht->buckets[idx] = entry;
}

int ht_get(HashTable *ht, const char *key, int *out) {
    unsigned int idx = hash(key);
    for (Entry *e = ht->buckets[idx]; e != NULL; e = e->next) {
        if (strcmp(e->key, key) == 0) {
            *out = e->value;
            return 0;
        }
    }
    return -1;   /* 키를 찾지 못함 */
}

int main(void) {
    HashTable ht;
    ht_init(&ht);
    ht_set(&ht, "apple", 100);
    ht_set(&ht, "banana", 200);

    int value;
    if (ht_get(&ht, "apple", &value) == 0) {
        printf("apple: %d\n", value);   /* apple: 100 */
    }
    if (ht_get(&ht, "cherry", &value) != 0) {
        printf("cherry: not found\n");
    }
    return 0;
}
```

`ht_set`과 `ht_get`이 각 버킷 안에서 [스택과 큐](/post/computerterms/stacks-and-queues/)에서 다룬 push_front와 동일한 방식으로 체이닝을 구현한 것에 주목할 만하다. 해시테이블은 새 자료구조가 아니라, 배열과 연결리스트를 조합해 "임의의 키로 O(1) 접근"이라는 성질을 만들어낸 결과다.

## 왜 "평균" O(1)인가

해시테이블의 탐색·삽입이 O(1)이라는 말에는 "충돌이 고르게 분산된다"는 전제가 깔려 있다. 해시 함수가 편향돼 있거나, 버킷 수 대비 데이터가 너무 많이 쌓이면(적재율이 높으면) 특정 버킷의 체인이 길어져 탐색이 사실상 연결리스트를 순회하는 것과 같아진다 — 극단적인 경우 모든 키가 같은 버킷에 몰리면 O(n)으로 퇴화한다. 실무 구현체는 **적재율(Load Factor, 원소 수 ÷ 버킷 수)**이 특정 임계값(보통 0.7~1.0)을 넘으면 버킷 배열 크기를 늘리고 기존 원소를 재배치하는 **리해싱(Rehashing)**으로 이 문제를 완화한다.

## 비교: 균형 BST vs 해시테이블

| 특성 | 균형 BST | 해시테이블 |
|---|---|---|
| 평균 탐색·삽입 | O(log n) | O(1) |
| 최악 탐색·삽입 | O(log n) (균형 보장) | O(n) (충돌 심할 때) |
| 정렬된 순서 순회 | 가능 (중위 순회) | 불가능 (버킷 순서는 의미 없음) |
| 최솟값/최댓값 조회 | O(log n) | O(n) (전체 스캔 필요) |
| 메모리 오버헤드 | 노드당 포인터 2개 | 버킷 배열 + 체인 포인터 |

## 흔한 오개념

**"해시테이블은 항상 O(1)이다"** — 충돌 분산이 고르다는 전제를 빼먹은 채 평균 복잡도를 최악의 경우 보장으로 오해하는 경우다. 실시간성이 중요한 시스템(임베디드, 게임 엔진의 프레임 예산)에서는 이 최악의 경우 O(n) 가능성 때문에 오히려 최악 O(log n)을 보장하는 균형 BST를 선택하기도 한다.

**"해시 함수는 충돌이 없어야 좋은 것이다"** — 유한한 버킷 수에 무한히 많은 키를 매핑해야 하므로 충돌은 수학적으로 피할 수 없다(비둘기집 원리). 좋은 해시 함수의 기준은 "충돌이 없다"가 아니라 "충돌이 특정 패턴 없이 고르게 분산된다"는 것이다.

## 다른 개념과의 연결

해시테이블은 파이썬 `dict`, 자바스크립트 객체, C++ `std::unordered_map`처럼 대부분의 언어에서 "맵/딕셔너리"라는 이름으로 표준 라이브러리에 내장돼 있다 — 직접 구현하기 전에 언어 표준 구현을 먼저 쓰는 것이 정석이다. 다음 챕터에서는 [트리](/post/computerterms/trees/)의 "부모-자식" 관계를 "임의의 노드끼리 연결"로 일반화한 [그래프](/post/computerterms/graphs/)를 다룬다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 해시테이블이 배열의 O(1) 접근을 임의의 키로 확장하는 원리를 설명할 수 있다. 체이닝 방식의 충돌 처리와, 적재율이 높아질 때 성능이 저하되는 이유를 설명할 수 있다. 정렬된 순회나 최악의 경우 보장이 필요한 상황과, 평균 O(1)이 중요한 상황을 구분해 균형 BST와 해시테이블 중 하나를 선택할 수 있다.

## 참고 자료

> Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.), Chapter 11: Hash Tables. MIT Press.

- [cppreference: std::unordered_map](https://en.cppreference.com/w/cpp/container/unordered_map) — 리해싱 정책과 적재율(`max_load_factor`)을 다루는 표준 라이브러리 문서
- [Python docs: dict implementation](https://docs.python.org/3/faq/design.html#how-are-dictionaries-implemented-in-cpython) — CPython 딕셔너리의 오픈 어드레싱 기반 해시테이블 구현 설명
