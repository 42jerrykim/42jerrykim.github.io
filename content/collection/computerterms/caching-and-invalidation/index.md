---
image: "wordcloud.png"
slug: caching-and-invalidation
collection_order: 22
draft: false
title: "[Computer Terms] 캐싱과 캐시 무효화 (Caching, Cache Invalidation)"
date: 2026-07-21
last_modified_at: 2026-07-21
categories: ComputerTerms
description: "캐싱은 느린 원본 대신 빠른 사본을 먼저 확인해 반복 조회를 줄이는 기법입니다. 지역성 원리, LRU 교체 정책, 캐시 무효화가 왜 어려운 문제인지 C 코드와 함께 다룹니다."
tags:
- Technology(기술)
- Education(교육)
- Caching(캐싱)
- Cache-Invalidation(캐시무효화)
- LRU
- Memory(메모리)
- Performance(성능)
- Hash-Table(해시테이블)
- C
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
- Data-Structure(자료구조)
- Distributed-Systems(분산시스템)
- Debugging(디버깅)
- Advanced
---

## 이 장을 읽기 전에

[메모리 관리와 가상 메모리](/post/computerterms/memory-management/)에서 다룬 페이지 폴트·스와핑, [해시테이블](/post/computerterms/hash-tables/)의 O(1) 조회, [DNS와 소켓](/post/computerterms/dns-and-sockets/)에서 언급했던 DNS 캐시·TTL을 안다고 가정한다. 캐싱은 새로운 자료구조가 아니라, "느린 것을 매번 다시 계산·조회하지 말고 빠른 곳에 사본을 두자"는 공통 아이디어가 CPU부터 웹 서비스까지 시스템 전 계층에 반복해서 나타나는 것이다.

## 왜 캐시가 거의 모든 시스템에 등장하는가

CPU 레지스터·캐시·RAM·디스크·네트워크는 접근 속도가 자릿수 단위로 차이 난다. CPU 캐시 접근이 몇 나노초라면 디스크 접근은 몇 밀리초, 네트워크 요청은 그보다 더 걸릴 수 있다. **캐시(Cache)**는 자주 쓰는 데이터의 사본을 더 빠른 계층에 보관해, 매번 느린 원본까지 가지 않아도 되게 한다. 이것이 가능한 이유는 실제 데이터 접근 패턴이 **지역성(Locality)**을 갖기 때문이다 — 방금 접근한 데이터를 곧 다시 접근할 가능성이 높고(시간 지역성), 방금 접근한 데이터 근처의 데이터에 접근할 가능성이 높다(공간 지역성). [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/) 챕터에서 배열이 캐시 지역성에 유리하다고 짚었던 것이 바로 이 공간 지역성의 실제 사례다.

## LRU: 캐시가 가득 찼을 때 무엇을 버릴까

캐시 공간은 원본보다 항상 작으므로, 새 데이터를 넣을 자리가 없으면 기존 데이터 중 하나를 버려야 한다. 가장 널리 쓰이는 정책이 **LRU(Least Recently Used)**로, 가장 오랫동안 사용되지 않은 항목을 버린다. 이 정책을 구현하려면 "가장 최근에 쓴 것"과 "가장 오래전에 쓴 것"을 모두 O(1)에 알아낼 수 있어야 하는데, [해시테이블](/post/computerterms/hash-tables/)만으로는 순서를 알 수 없고 [연결리스트](/post/computerterms/arrays-and-linked-lists/)만으로는 특정 키를 O(1)에 찾을 수 없다. 그래서 실제 LRU 캐시는 이 둘을 조합한다.

```c
#include <stdio.h>
#include <stdlib.h>

#define CAPACITY 3

typedef struct Node {
    int key, value;
    struct Node *prev, *next;
} Node;

typedef struct {
    Node *head, *tail;   /* head 쪽이 가장 최근 사용, tail 쪽이 가장 오래됨 */
    Node *map[100];      /* 키를 노드로 바로 찾기 위한 단순화된 해시테이블 대용 */
    int size;
} LRUCache;

void lru_init(LRUCache *c) {
    c->head = c->tail = NULL;
    c->size = 0;
    for (int i = 0; i < 100; i++) c->map[i] = NULL;
}

void move_to_front(LRUCache *c, Node *node) {
    if (c->head == node) return;
    if (node->prev) node->prev->next = node->next;
    if (node->next) node->next->prev = node->prev;
    if (c->tail == node) c->tail = node->prev;

    node->prev = NULL;
    node->next = c->head;
    if (c->head) c->head->prev = node;
    c->head = node;
    if (!c->tail) c->tail = node;
}

void lru_put(LRUCache *c, int key, int value) {
    if (c->map[key] != NULL) {
        c->map[key]->value = value;
        move_to_front(c, c->map[key]);
        return;
    }

    if (c->size == CAPACITY) {   /* 가장 오래된 항목(tail) 제거 */
        Node *victim = c->tail;
        c->map[victim->key] = NULL;
        c->tail = victim->prev;
        if (c->tail) c->tail->next = NULL;
        free(victim);
        c->size--;
    }

    Node *node = malloc(sizeof(Node));
    node->key = key;
    node->value = value;
    node->prev = node->next = NULL;
    c->map[key] = node;
    move_to_front(c, node);
    c->size++;
}

int main(void) {
    LRUCache cache;
    lru_init(&cache);
    lru_put(&cache, 1, 100);
    lru_put(&cache, 2, 200);
    lru_put(&cache, 3, 300);
    lru_put(&cache, 1, 999);   /* 1을 다시 씀 → 1이 가장 최근 사용으로 이동 */
    lru_put(&cache, 4, 400);   /* 용량 초과 → 가장 오래된 2가 제거됨 */

    printf("head(가장 최근): key=%d\n", cache.head->key);   /* 4 */
    printf("tail(가장 오래됨): key=%d\n", cache.tail->key);  /* 3 */
    return 0;
}
```

이중 연결리스트로 사용 순서를, 해시테이블(여기서는 단순화한 배열)로 키 조회를 각각 O(1)에 처리한다 — 자료구조 갈래에서 다룬 두 구조의 강점을 조합해야 LRU를 O(1)로 구현할 수 있다는 것을 보여주는 예다.

## 캐싱보다 어려운 문제: 무효화

캐시를 쓰는 것 자체는 어렵지 않지만, **원본이 바뀌었을 때 캐시된 사본을 언제 버릴지**는 "컴퓨터 과학에서 이름 짓기, 캐시 무효화, 오프바이원 에러만이 어려운 두 가지 문제다"(필 칼튼의 유명한 농담이 인용될 만큼)라는 말이 나올 정도로 까다롭다. 무효화 전략은 크게 두 갈래다. **TTL(Time To Live)**은 일정 시간이 지나면 무조건 캐시를 만료시킨다 — 구현은 간단하지만, TTL이 짧으면 캐시 효과가 줄고 길면 원본과 사본이 다른 **오래된 데이터(Stale Data)**를 오래 보여줄 수 있다. **명시적 무효화**는 원본이 바뀌는 시점에 캐시를 직접 지우거나 갱신한다 — 항상 최신 상태를 보장하지만, 원본을 바꾸는 모든 경로에서 캐시 무효화를 빠뜨리지 않아야 한다.

## 비교: TTL 기반 vs 명시적 무효화

| 특성 | TTL 기반 | 명시적 무효화 |
|---|---|---|
| 구현 복잡도 | 낮음 (만료 시간만 설정) | 높음 (원본 변경 경로마다 무효화 로직 필요) |
| 최신성 보장 | 최대 TTL만큼 오래될 수 있음 | 즉시 반영 (누락이 없다면) |
| 실패 모드 | Stale Data를 짧게 보여줌 | 무효화 누락 시 Stale Data가 무기한 유지될 수 있음 |
| 대표 사례 | DNS 레코드, 브라우저 캐시 | 데이터베이스 write-through 캐시 |

## 흔한 오개념

**"캐시는 히트율이 높을수록 무조건 좋다"** — 히트율이 높아도 캐시된 데이터가 오래돼(Stale) 있다면 "빠르지만 틀린 답"을 주는 것이다. 캐싱을 도입할 때는 히트율뿐 아니라 "이 데이터가 얼마나 자주, 얼마나 빨리 바뀌는가"와 "오래된 데이터를 보여줘도 되는 허용 범위가 얼마인가"를 함께 판단해야 한다.

**"캐시는 항상 메모리에만 있다"** — CPU 캐시부터 CDN(콘텐츠 전송 네트워크)까지, 캐시는 어느 계층에든 존재할 수 있다. 브라우저 캐시, DNS 캐시, 데이터베이스 쿼리 캐시, [메모리 관리와 가상 메모리](/post/computerterms/memory-management/)에서 언급한 TLB까지 모두 "느린 원본 대신 빠른 사본을 먼저 본다"는 같은 원리를 계층마다 다른 곳에 적용한 것이다.

## 다른 개념과의 연결

LRU의 이중 연결리스트+해시테이블 조합은 [배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/), [해시테이블](/post/computerterms/hash-tables/) 챕터의 직접적인 응용이다. 캐시 무효화의 어려움은 [ACID Transactions](/post/computerterms/acid-transactions/)에서 다룬 일관성 문제와 본질적으로 같은 종류다 — "여러 곳에 있는 사본을 어떻게 일치시킬 것인가". 다음 챕터에서는 이 데이터를 보호하는 관점(암호화, 인증)으로 넘어간다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 캐싱이 유효한 이유(시간·공간 지역성)를 설명할 수 있다. LRU 캐시를 O(1) 삽입·조회로 구현하기 위해 왜 두 가지 자료구조를 조합해야 하는지 설명할 수 있다. TTL 기반과 명시적 무효화 각각의 장단점을 이해하고, 데이터 특성에 맞는 전략을 선택할 수 있다.

## 참고 자료

> Hennessy, J. L., & Patterson, D. A. (2017). *Computer Architecture: A Quantitative Approach* (6th ed.), Chapter 2: Memory Hierarchy Design. Morgan Kaufmann.

- [Redis Documentation: Eviction Policies](https://redis.io/docs/latest/develop/reference/eviction/) — LRU를 포함한 실제 캐시 서버의 교체 정책 구현
- [Martin Fowler: Cache Invalidation](https://martinfowler.com/bliki/TwoHardThings.html) — 캐시 무효화가 어려운 문제로 꼽히는 이유에 대한 실무 관점 에세이
