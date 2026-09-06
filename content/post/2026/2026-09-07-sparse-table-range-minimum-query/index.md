---
title: "[Algorithm] Sparse Table — 정적 배열 구간 질의를 O(1)로 답하는 법"
description: "Sparse Table은 값이 바뀌지 않는 배열에서 구간 최솟값 같은 멱등 연산을 O(1)에 답하는 정적 자료구조다. 2의 거듭제곱 구간 전처리 원리, C++ 구현, 세그먼트 트리·누적합과의 비교, LCA 응용과 흔한 구현 실수까지 정리한다."
date: 2026-09-07
lastmod: 2026-09-07
draft: false
categories:
  - Algorithm
  - Data-Structures
tags:
  - Algorithm(알고리즘)
  - Competitive-Programming(경쟁프로그래밍)
  - Data-Structures(자료구조)
  - Time-Complexity(시간복잡도)
  - Space-Complexity(공간복잡도)
  - Complexity-Analysis(복잡도분석)
  - Range-Query
  - Segment-Tree(세그먼트트리)
  - Prefix-Sum
  - LCA(Lowest Common Ancestor)
  - Euler-Tour
  - Mo-Algorithm
  - Array(배열)
  - C++
  - Implementation(구현)
  - Optimization(최적화)
  - Performance(성능)
  - Best-Practices
  - Edge-Cases(엣지케이스)
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Advanced
  - Deep-Dive
  - Reference(참고)
  - Problem-Solving(문제해결)
  - BOJ(백준)
  - Baekjoon
  - Divide-and-Conquer(분할정복)
image: "wordcloud.png"
---

## 개요

배열이 한 번 만들어진 뒤 절대 바뀌지 않는데 구간 최솟값·최댓값·GCD 같은 질의만 수만 번 반복해서 들어온다면, 매번 구간을 순회하는 O(구간 길이)나 갱신까지 지원하는 세그먼트 트리의 O(log n)은 모두 필요 이상의 비용을 치르는 선택일 수 있다. **Sparse Table**은 이런 상황을 겨냥해 전처리에 O(n log n) 시간과 공간을 한 번 투자하는 대신, 이후의 모든 질의를 로그조차 필요 없는 O(1)에 끝내는 정적(static) 자료구조다. 이 글은 Sparse Table이 성립하는 수학적 근거, C++ 구현, 세그먼트 트리·누적합 배열과의 비교, 그리고 LCA(최소 공통 조상) 계산에 응용되는 확장까지 다룬다.

## 핵심 원리: 멱등 연산과 2의 거듭제곱 분해

Sparse Table의 출발점은 "0 이상의 모든 정수는 서로 다른 2의 거듭제곱들의 합으로 유일하게 표현된다"는 사실이다. 이 사실을 구간에 적용하면 임의의 구간 `[L, R]`을 O(log n)개의 길이 2^k 구간으로 쪼개어 덮을 수 있다는 결론이 나온다. 전처리 단계에서는 `table[k][i]`에 "인덱스 i부터 시작하는 길이 2^k 구간"의 답을 저장하는 DP 테이블을 만든다. 점화식은 `table[k][i] = f(table[k-1][i], table[k-1][i + 2^(k-1)])`로, 길이 2^k 구간을 절반씩 두 개의 2^(k-1) 구간으로 나눠 병합하는 분할정복(divide-and-conquer) 방식이며 전체 전처리에는 O(n log n) 시간과 공간이 든다. 다만 매 질의마다 재귀로 구간을 쪼개는 일반적인 분할정복과 달리, Sparse Table은 가능한 모든 2^k 구간의 답을 질의 이전에 한 번씩 미리 계산해 저장해 둔다는 점에서 상향식(bottom-up) DP에 가깝다 — 그 대가로 질의 시점에는 재귀 호출 없이 테이블 조회 두 번으로 끝난다.

질의 방식은 병합 함수 f가 <strong>멱등(idempotent)</strong>인지에 따라 갈린다. 최솟값·최댓값·GCD·비트 AND/OR처럼 같은 원소를 두 번 세어도 결과가 바뀌지 않는 연산이라면, 구간 `[L, R]`을 딱 두 개의 (겹쳐도 무방한) 2^k 구간만으로 덮어 O(1)에 답할 수 있다. `k = floor(log2(R - L + 1))`로 두면 `f(table[k][L], table[k][R - 2^k + 1])`가 정답이 되는데, 두 구간이 서로 겹치더라도 멱등성 덕분에 결과가 훼손되지 않기 때문이다. 반면 합(sum)처럼 멱등이 아닌 연산은 원소가 두 번 세어지면 값이 실제로 바뀌므로, 구간을 겹치지 않는 O(log n)개의 조각으로 정확히 분해해서 더해야 하며 이 경우 질의는 O(log n)으로 늘어난다.

## 구현: 로그 테이블과 O(1) 질의

아래는 구간 최솟값(RMQ)을 O(1)에 답하는 Sparse Table의 최소 구현이다. `log2()`를 실행 중에 직접 호출하는 대신, 정수 DP로 `log_table`을 미리 채워두는 방식을 썼다 — 이유는 실전 팁 절에서 다룬다.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class SparseTable {
public:
    explicit SparseTable(const vector<int>& arr) {
        n = static_cast<int>(arr.size());
        log_table.assign(n + 1, 0);
        for (int i = 2; i <= n; i++) {
            log_table[i] = log_table[i / 2] + 1;
        }
        int levels = log_table[n] + 1;
        table.assign(levels, vector<int>(n));
        table[0] = arr;
        for (int k = 1; k < levels; k++) {
            int len = 1 << k;
            for (int i = 0; i + len <= n; i++) {
                table[k][i] = min(table[k - 1][i], table[k - 1][i + (len >> 1)]);
            }
        }
    }

    // [l, r] 구간(양 끝 포함)의 최솟값을 O(1)에 반환
    int query(int l, int r) const {
        int k = log_table[r - l + 1];
        return min(table[k][l], table[k][r - (1 << k) + 1]);
    }

private:
    int n;
    vector<int> log_table;
    vector<vector<int>> table;
};

int main() {
    vector<int> arr = {5, 2, 4, 7, 1, 3, 6};
    SparseTable st(arr);

    cout << "query(1, 4): " << st.query(1, 4) << "\n"; // min(2,4,7,1) = 1
    cout << "query(0, 2): " << st.query(0, 2) << "\n"; // min(5,2,4) = 2
    cout << "query(4, 6): " << st.query(4, 6) << "\n"; // min(1,3,6) = 1
    return 0;
}
```

`query(1, 4)`를 예로 추적하면, 구간 길이는 4이므로 `k = log_table[4] = 2`이고 `table[2][1]`과 `table[2][4-4+1] = table[2][1]`을 비교한다 — 우연히 같은 칸을 두 번 보게 되는 경계 사례지만, 이 칸이 정확히 `[1,4]` 전체의 최솟값(1)을 담고 있으므로 답은 그대로 맞는다. 구간 길이가 5(`2^2 < 5 < 2^3`)처럼 정확히 2의 거듭제곱이 아닌 경우에는 두 `table[k]` 조회 구간이 실제로 겹치면서 서로 다른 칸을 비교하게 되고, 멱등성 덕분에 그 겹침이 결과를 해치지 않는다.

## 비교: 배열 순회 vs 누적합 vs 세그먼트 트리 vs Sparse Table

| 특성 | 매번 배열 순회 | 누적합(prefix sum) | 세그먼트 트리 | Sparse Table |
|---|---|---|---|---|
| 구간 쿼리 | O(구간 길이) | O(1) (합처럼 가역 연산일 때만) | O(log n) | O(1) (멱등 연산일 때) |
| 값 변경 | O(1) | O(n) (그 이후 전체 재계산) | O(log n) | 불가 (사실상 전체 재구축) |
| 전처리 | 없음 | O(n) | O(n) | O(n log n) |
| 공간 | O(n) | O(n) | O(n) | O(n log n) |
| 적합한 경우 | 쿼리가 드물고 구간이 짧음 | 정적 데이터 + 합처럼 뺄셈이 되는 연산 | 값 변경과 쿼리가 모두 빈번 | 정적 데이터 + 최솟값처럼 멱등인 연산, 쿼리가 매우 많음 |

누적합 배열이 항상 손해인 것은 아니다 — 합(sum)만 필요하고 데이터가 절대 바뀌지 않는다면 O(1) 쿼리에 O(n log n)이 아닌 O(n) 공간만 쓰는 누적합 쪽이 더 낫다. Sparse Table의 존재 이유는 정확히 "최솟값·최댓값·GCD처럼 뺄셈으로 역연산할 수 없는 멱등 연산"에 있다.

## 확장: LCA를 O(1)로 푸는 법과 Mo's Algorithm과의 경계

Sparse Table이 실전에서 가장 빈번하게 쓰이는 자리 중 하나는 트리의 <strong>최소 공통 조상(LCA)</strong>을 O(1) 질의로 구하는 기법이다. 트리를 오일러 투어(Euler tour)로 순회하면 각 정점을 방문할 때마다 깊이(depth)를 기록한 배열이 만들어지고, 두 정점 u·v의 LCA는 이 배열에서 u와 v가 처음 등장하는 두 위치 사이의 <strong>구간 최솟값(깊이가 가장 얕은 정점)</strong>을 찾는 문제로 정확히 환원된다. 이 배열은 트리가 고정되어 있는 한 절대 바뀌지 않으므로 Sparse Table의 "정적 데이터" 전제와 정확히 들어맞고, 오일러 투어 O(n) 전처리 위에 Sparse Table의 O(n log n) 전처리를 얹으면 이후 임의의 LCA 질의를 O(1)에 답할 수 있다.

반대로 최빈값(mode)이나 "서로 다른 원소의 개수"처럼 두 부분 구간의 답을 O(1)·O(log n)에 병합하는 방법 자체가 마땅치 않은 질의에는 Sparse Table도 세그먼트 트리도 직접 적용하기 어렵다. 이런 경우의 표준 대안이 **Mo's Algorithm**이다 — 질의를 오프라인으로 모아 √n 블록 기준으로 재정렬한 뒤 포인터를 슬금슬금 옮기며 하나의 단순한 자료구조만 유지하는 방식으로, 병합 난이도와 무관하게 O((n+q)√n)에 답한다. 다만 Mo's Algorithm은 질의를 실시간으로 받는 온라인 문제에는 쓸 수 없다는 제약이 있어, "멱등 연산 + 정적 데이터"라는 좁지만 흔한 조건에서는 여전히 Sparse Table의 O(1) 쿼리를 대체하지 못한다. 국내 온라인 저지에서는 BOJ 10868 "최솟값" 문제가 값 변경이 전혀 없는 순수 구간 최솟값 질의를 다뤄 Sparse Table을 처음 연습하기에 적합한 예로 꼽힌다.

## 실전 팁: 자주 하는 실수

1. **합(sum)에 멱등 공식을 그대로 적용한다.** `f(table[k][L], table[k][R-2^k+1])` 공식은 두 구간이 겹쳐도 결과가 바뀌지 않는 멱등 연산에서만 성립한다. 합처럼 겹치면 값이 실제로 달라지는 연산에 같은 공식을 쓰면 원소를 이중으로 세어 틀린 값을 얻는다 — 합은 겹치지 않는 O(log n)개 조각으로 분해해야 한다.
2. **`log2()`를 실행 중에 직접 호출한다.** 부동소수점 `log2(4.0)`이 반올림 오차로 `1.9999999`가 되어 정수로 캐스팅할 때 `k`가 1만큼 작게 잡히는 경우가 실제로 있다. 위 구현처럼 `log_table`을 정수 DP로 미리 채워두면 이 오차를 원천 차단한다.
3. **`table`의 레벨 수를 `log2(n)`으로만 잡고 +1을 빠뜨린다.** 길이 n인 배열 전체를 담당하는 최상위 레벨까지 포함하려면 `log_table[n] + 1`개의 레벨이 필요하다. 이를 놓치면 구간 길이가 정확히 2의 거듭제곱인 최댓값 질의에서 배열 범위를 벗어난다.
4. **값이 하나라도 바뀌는 문제에 Sparse Table을 선택한다.** 원소 하나만 갱신돼도 그 원소를 포함하는 모든 레벨의 `table[k][i]`를 다시 계산해야 하므로 사실상 O(n log n) 전체 재구축과 다르지 않다. 갱신이 섞여 있다면 세그먼트 트리를 쓴다.
5. **질의 구간이 비어있거나 `l > r`인 경계를 처리하지 않는다.** 위 구현은 `r - l + 1 >= 1`을 전제하므로, 호출 전에 빈 구간 여부를 별도로 걸러야 한다.

## 요약

Sparse Table은 "배열이 절대 바뀌지 않는다"는 전제를 받아들이는 대가로, 세그먼트 트리보다 구현이 단순하면서도 멱등 연산에 한해 로그 팩터조차 없는 O(1) 쿼리를 얻는 자료구조다. 핵심은 모든 구간을 2의 거듭제곱 길이 조각으로 분해할 수 있다는 사실과, 멱등 연산은 그 조각들이 겹쳐도 결과가 훼손되지 않는다는 성질을 결합한 것이다. 갱신이 전혀 없고 최솟값·최댓값·GCD 같은 멱등 질의가 매우 많이 반복되는 상황(대표적으로 LCA)에서는 표준 선택이 되지만, 값 변경이 섞이거나 합처럼 비멱등 연산이 필요하면 세그먼트 트리나 누적합 배열로 넘어가야 한다.

## 평가 기준

이 글을 읽은 후에는 다음을 할 수 있어야 한다. 겹치는 두 구간으로 덮는 O(1) 질의 공식이 최솟값·최댓값 같은 멱등 연산에서만 성립하고 합(sum)에는 왜 적용할 수 없는지 설명할 수 있다. 정적 데이터에 멱등 질의가 반복되는 상황에서는 Sparse Table을, 값 변경이 섞인 상황에서는 세그먼트 트리를 근거를 들어 선택할 수 있다. `log_table`을 부동소수점 `log2()` 대신 정수 DP로 채워야 하는 이유를 설명하고 직접 구현할 수 있다. 오일러 투어로 트리를 배열로 평탄화한 뒤 Sparse Table을 얹어 LCA를 O(1) 질의로 바꾸는 과정을 설명할 수 있다.

## 참고 자료

- [Sparse Table — cp-algorithms.com](https://cp-algorithms.com/data_structures/sparse-table.html)
- [Range minimum query — Wikipedia](https://en.wikipedia.org/wiki/Range_minimum_query)
