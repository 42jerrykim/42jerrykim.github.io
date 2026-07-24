---
image: "wordcloud.png"
slug: segment-trees
collection_order: 48
draft: false
title: "[Computer Terms] 세그먼트 트리 (Segment Tree)"
date: 2026-07-22
last_modified_at: 2026-07-22
categories: ComputerTerms
description: "세그먼트 트리는 구간 합·구간 최솟값 같은 구간 쿼리를 O(log n)에 처리하는 트리입니다. 배열 순회 대비 이점과 트리 구축·쿼리 원리를 컴파일 가능한 C 코드로 다루고, 배열 크기 산정·경계 조건에서 흔히 나는 구현 버그도 함께 짚습니다."
tags:
- Technology(기술)
- Education(교육)
- Data-Structure(자료구조)
- Segment-Tree(세그먼트트리)
- Tree(트리)
- Array(배열)
- Heap(힙)
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

[배열과 연결리스트](/post/computerterms/arrays-and-linked-lists/)의 배열 인덱스 접근, [트리](/post/computerterms/trees/)의 완전 이진 트리 개념, [힙과 우선순위 큐](/post/computerterms/heaps-and-priority-queues/)에서 다룬 "완전 이진 트리를 배열 하나로 표현하는" 기법을 안다고 가정한다. 세그먼트 트리는 힙과 같은 배열 표현 방식을 구간 쿼리라는 다른 문제에 적용한 자료구조다.

## 구간 합을 반복해서 구해야 한다면

배열에 저장된 값들의 "구간 합(예: 인덱스 3부터 7까지의 합)"을 한 번만 구한다면 그 구간을 순회하는 O(구간 길이)로 충분하다. 그런데 이 질의가 수만 번 반복되고, 중간중간 배열의 특정 값이 바뀌기도 한다면 어떨까. 매번 구간을 순회하면 질의 Q번에 대해 총 O(Q·n)이 든다. 값이 바뀔 때마다 **누적합 배열**을 다시 계산해두는 방법도 있지만, 값 변경 자체가 O(n)이 되어 값 변경이 잦은 상황에서는 오히려 손해다. **세그먼트 트리(Segment Tree)**는 값 변경과 구간 쿼리를 모두 O(log n)에 처리해 두 상황을 동시에 만족시킨다.

## 세그먼트 트리의 구조: 구간을 표현하는 트리

세그먼트 트리는 [힙](/post/computerterms/heaps-and-priority-queues/)처럼 완전 이진 트리를 배열 하나로 표현한다. 다만 힙의 각 노드가 "값 하나"를 담는 것과 달리, 세그먼트 트리의 각 노드는 "원본 배열의 특정 구간에 대한 집계값(합, 최솟값, 최댓값 등)"을 담는다. 루트는 전체 배열 `[0, n-1]`의 집계값을 담고, 왼쪽 자식은 왼쪽 절반 `[0, mid]`, 오른쪽 자식은 오른쪽 절반 `[mid+1, n-1]`을 담는 식으로 재귀적으로 절반씩 나뉜다. 리프 노드에 도달하면 그 노드는 원본 배열의 원소 하나만을 담는다. 원본 배열 크기가 n일 때 트리의 리프는 n개, 전체 노드는 대략 2n개이므로 4n 크기의 배열로 여유 있게 표현하는 것이 일반적인 구현 관례다.

## 구축: 아래에서 위로 집계값 합치기

트리 구축은 재귀적으로 배열을 절반씩 나누다가 리프에서 원본 값을 채우고, 재귀가 돌아오면서 두 자식의 집계값을 합쳐 부모 값을 계산하는 방식으로 이뤄진다. 이 과정은 각 노드를 정확히 한 번씩만 방문하므로 O(n)에 끝난다.

```c
#include <stdio.h>

#define MAX_N 100

int tree[4 * MAX_N];
int source[MAX_N];

/* node가 담당하는 구간 [start, end]의 합을 재귀적으로 구축 */
void build(int node, int start, int end) {
    if (start == end) {
        tree[node] = source[start];
        return;
    }
    int mid = (start + end) / 2;
    build(2 * node + 1, start, mid);
    build(2 * node + 2, mid + 1, end);
    tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
}
```

`build`가 자식 인덱스로 힙과 동일한 `2*node+1`, `2*node+2` 공식을 쓰는 것은 우연이 아니다 — 세그먼트 트리도 힙처럼 완전 이진 트리를 배열로 표현하기 때문에 같은 부모-자식 인덱스 공식이 그대로 적용된다. 다만 힙과 달리 각 노드가 담당하는 "구간"이라는 정보를 재귀 호출의 매개변수(`start`, `end`)로 함께 들고 다녀야 한다.

이 구현에서 실무자가 가장 자주 겪는 버그 두 가지는 디버깅으로 잡기 까다롭다. 첫째, `tree` 배열 크기를 `4 * MAX_N`이 아니라 `2 * MAX_N`처럼 작게 잡으면, 트리가 완전 이진 트리가 아닐 때(원소 수가 2의 거듭제곱이 아닐 때) 일부 리프 인덱스가 배열 범위를 벗어나 세그먼테이션 폴트나 조용한 메모리 손상이 발생한다 — 완전 이진 트리를 배열로 담으려면 이론상 최대 `4n`칸이 필요하다는 점을 잊기 쉽다. 둘째, `mid = (start + end) / 2`에서 재귀를 `build(2*node+1, start, mid)`, `build(2*node+2, mid+1, end)`로 나눌 때 `mid` 계산이나 자식 구간 경계를 한 칸이라도 잘못 잡으면(예: `mid`가 아니라 `mid-1`을 쓰는 실수) 특정 원소가 두 번 세어지거나 아예 누락되는데, 출력값이 "그럴듯하게 틀린" 숫자로 나와서 원인 파악에 시간이 걸린다.

## 구간 쿼리: 구간을 3가지로 분류해 재귀

구간 합 쿼리 `[l, r]`을 처리할 때, 현재 노드가 담당하는 구간 `[start, end]`는 세 경우 중 하나다. 질의 구간과 전혀 겹치지 않으면 0(합의 항등원)을 반환하고 더 내려가지 않는다. 질의 구간이 현재 노드의 구간을 완전히 포함하면 그 노드의 집계값을 그대로 반환한다. 일부만 겹치면 왼쪽·오른쪽 자식으로 나눠 재귀 호출한 뒤 합쳐서 반환한다. 이 "완전히 포함되면 즉시 반환"하는 가지치기 덕분에, 순진하게 배열 전체를 순회하는 O(n)과 달리 실제로 방문하는 노드 수가 O(log n)에 묶인다.

```c
/* node가 담당하는 구간 [start, end]에서 질의 구간 [l, r]의 합을 구함 */
int query(int node, int start, int end, int l, int r) {
    if (r < start || end < l) return 0;                    /* 겹치지 않음 */
    if (l <= start && end <= r) return tree[node];          /* 완전 포함 */

    int mid = (start + end) / 2;
    int left_sum = query(2 * node + 1, start, mid, l, r);
    int right_sum = query(2 * node + 2, mid + 1, end, l, r);
    return left_sum + right_sum;
}

/* index 위치의 값을 value로 갱신 : O(log n) */
void update(int node, int start, int end, int index, int value) {
    if (start == end) {
        tree[node] = value;
        return;
    }
    int mid = (start + end) / 2;
    if (index <= mid) {
        update(2 * node + 1, start, mid, index, value);
    } else {
        update(2 * node + 2, mid + 1, end, index, value);
    }
    tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
}

int main(void) {
    int n = 6;
    int values[] = {1, 3, 5, 7, 9, 11};
    for (int i = 0; i < n; i++) source[i] = values[i];

    build(0, 0, n - 1);
    printf("sum[1..4]: %d\n", query(0, 0, n - 1, 1, 4));   /* 3+5+7+9 = 24 */

    update(0, 0, n - 1, 2, 100);   /* index 2의 값을 5 -> 100으로 변경 */
    printf("sum[1..4] after update: %d\n", query(0, 0, n - 1, 1, 4));   /* 3+100+7+9 = 119 */
    return 0;
}
```

`query`가 왜 O(log n)에 끝나는가는 "구간이 완전히 겹치는 노드는 트리의 각 레벨마다 최대 2개씩만 존재한다"는 사실에서 나온다. 어떤 레벨에서 질의 구간과 부분적으로만 겹치는 노드는 왼쪽 경계 근처, 오른쪽 경계 근처에서 각각 하나씩뿐이고 나머지는 완전 포함되거나 전혀 겹치지 않아 즉시 반환된다. 트리 높이가 O(log n)이므로 전체 방문 노드 수도 O(log n)으로 묶인다.

## 비교: 배열 순회 vs 누적합 배열 vs 세그먼트 트리

| 특성 | 매번 배열 순회 | 누적합(prefix sum) 배열 | 세그먼트 트리 |
|---|---|---|---|
| 구간 쿼리 | O(구간 길이) | O(1) | O(log n) |
| 값 변경 | O(1) | O(n) — 이후 모든 누적합 재계산 | O(log n) |
| 구축 비용 | 없음 | O(n) | O(n) |
| 적합한 경우 | 쿼리가 드물고 구간이 짧은 경우 | 값이 고정되고 쿼리만 반복되는 경우 | 값 변경과 쿼리가 모두 빈번한 경우 |

세그먼트 트리가 누적합 배열보다 항상 나은 것은 아니다 — 값이 한 번 설정된 뒤 절대 바뀌지 않는다면 누적합 배열의 O(1) 쿼리를 이길 방법이 없다. 세그먼트 트리의 존재 이유는 정확히 "값 변경"과 "구간 쿼리"가 번갈아 반복되는 상황이다.

## 흔한 오개념

**"세그먼트 트리는 구간 합에만 쓴다"** — 구간 합은 가장 흔한 예시일 뿐, 노드가 담는 집계값을 결합 법칙(associativity)을 만족하는 어떤 연산으로든 바꿀 수 있다. 구간 최솟값·최댓값·최대공약수·비트 OR/AND 등 결합 법칙을 만족하는 연산이면 `build`·`query`의 `+` 연산자를 그 연산으로 바꾸는 것만으로 동일한 구조를 재사용할 수 있다.

**"세그먼트 트리는 항상 누적합 배열보다 좋은 선택이다"** — 값이 절대 바뀌지 않는 정적인 데이터라면 누적합 배열이 O(1) 쿼리로 세그먼트 트리의 O(log n)보다 빠르고 구현도 단순하다. 세그먼트 트리는 값 변경이 섞여 있을 때만 진가를 발휘하며, 정적 데이터에 세그먼트 트리를 쓰는 것은 불필요한 복잡도를 더하는 과잉 설계다.

## 다른 개념과의 연결

세그먼트 트리는 [힙과 우선순위 큐](/post/computerterms/heaps-and-priority-queues/)의 "완전 이진 트리를 배열로 표현한다"는 아이디어를 값 하나가 아닌 구간 집계값에 적용한 것이다. 이번 장으로 이 컬렉션의 자료구조 갈래(배열·연결리스트부터 트리·그래프·힙·트라이·유니온-파인드를 거쳐)에 이어, 다음 장에서 다룰 **스킵 리스트**는 트리 대신 여러 층의 연결리스트로 O(log n) 탐색을 얻는 전혀 다른 접근을 보여준다.

## 평가 기준

이 챕터를 읽은 후에는 다음을 할 수 있어야 한다. 세그먼트 트리의 각 노드가 담당하는 구간과 그 구간의 집계값이 자식 노드로부터 어떻게 합쳐지는지 설명할 수 있다. 구간 쿼리가 "겹치지 않음/완전 포함/부분 겹침" 세 경우로 나뉘어 재귀되는 이유와, 이 가지치기가 왜 O(log n)을 보장하는지 설명할 수 있다. 정적 데이터에는 누적합 배열을, 값 변경이 빈번한 데이터에는 세그먼트 트리를 근거를 들어 선택할 수 있다.

## 참고 자료

> Bentley, J. L. (1977). Solutions to Klee's rectangle problems. *Unpublished manuscript*, Carnegie Mellon University — 구간 분할 기반 트리 자료구조의 초기 아이디어 중 하나로 널리 인용된다.

- [cp-algorithms: Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html) — 세그먼트 트리 구축·쿼리·갱신의 표준 구현과 다양한 변형(지연 전파 등) 정리
- [Visualgo: Segment Tree](https://visualgo.net/en/segmenttree) — 구간 합 세그먼트 트리의 구축·쿼리 과정을 단계별로 시각화한 자료
