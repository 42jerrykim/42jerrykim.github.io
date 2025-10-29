---
title: "[Algorithm] cpp-python 백준 18485번 : Nine Judges"
description: "심사위원 선호 순위로 유도된 다수결 비교(토너먼트)에서 해밀토니안 경로를 구성해 상위 p개를 취해 ‘plausible set’을 찾는다. 분할-정복 머지와 다수결 비교로 O(n·k log k), 구현은 pos 테이블로 O(n·k) 메모리. 엣지/동률 없음(다수결 임계), 입력 정합성·인덱스·출력 형식 점검."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Graph
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-18485
- cpp
- python
- C++
- Python
- Implementation
- 구현
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Proof of Correctness
- 정당성 증명
- Edge Cases
- 코너 케이스
- Pitfalls
- 실수 포인트
- Optimization
- 최적화
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Code Review
- 코드리뷰
- Template
- 템플릿
- Testing
- 테스트
- Complexity Analysis
- 복잡도 분석
- Invariant
- 불변식
- Greedy
- 그리디
- Graph
- 그래프
- Tournament
- 토너먼트
- Hamiltonian Path
- 해밀토니안 경로
- Majority
- 다수결
- Preference Order
- 선호도 순위
- Pairwise Comparison
- 쌍대 비교
- Divide and Conquer
- 분할정복
- Merge
- 머지
- Ordering
- 순서화
- Ranking Aggregation
- 순위 집계
- Kemeny (concept)
- Stability
- 안정보장
- Plausible Set
- 문제선정
- Petrozavodsk
- Open Cup
- XCPC
- Math
- 수학적 모델링
- Implementation Details
- 구현 디테일
- I/O
- 입출력
- Zero-based vs One-based
- 인덱스
- Memory
- 메모리
- O(nklogk)
- O(nk)
image: "wordcloud.png"
---

## 문제 정보
- 문제: https://www.acmicpc.net/problem/18485
- 요약: `n (≤9, 홀수)`명의 심사위원이 제시한 `k (≤5e4)`개 문제의 선호 리스트가 주어진다. 정확히 `p`개를 뽑아 구성하는 문제셋 `S`가 무한 반복되는 무작위 교체 절차에서 양의 확률로 무한히 자주 나타날 수(plausible) 있으면 된다. 임의의 하나의 plausible set을 출력하라.
- 제한/스펙: 시간 2초, 메모리 512MB, `n`은 작고 `k`가 크다.

## 입출력 형식/예제
입력
```
n k p
<각 심사위원 i에 대해 길이 k의 순열 a_{i,1..k}>
```

출력
```
p개의 서로 다른 문제 번호 (1..k), 순서는 임의
```

예제
```
입력
3 5 3
3 2 5 1 4
1 4 2 5 3
2 4 5 1 3

출력(가능 예)
2 1 4
```

## 접근 개요(아이디어 스케치)
- 다수결 비교 정의: 문제 `x, y`에 대해 과반((n+1)/2) 이상의 심사위원이 `x`를 `y` 앞에 두면 `x > y`로 본다. 이는 모든 쌍에서 승패가 정해지는 방향 그래프(토너먼트)를 이룬다.
- 토너먼트에는 항상 해밀토니안 경로가 존재한다. 이 경로의 앞쪽 문제들은 다수결 관점에서 “강한” 문제들이다.
- 해밀토니안 경로를 분할정복 머지로 구성한 뒤, 경로의 선두 `p`개를 답으로 사용하면 해당 집합이 plausible set이 됨이 알려져 있다(이 과정은 관련 캠프/에디토리얼의 고전적 구성).

## 알고리즘 설계
- 자료구조:
  - `pos[judge][problem] = 등수(작을수록 선호)` 테이블 (크기 O(n·k)).
  - `beats(a,b)`: 과반 심사위원이 `a`를 `b`보다 선호하면 `true`.
- 해밀토니안 경로 구성(분할정복):
  1) 전체 문제 집합을 반으로 쪼개 각각 재귀적으로 경로를 만든다.
  2) 두 경로를 병합할 때, 머지 과정에서 현재 두 후보 `L[i], R[j]`를 비교하여 `beats(L[i], R[j])`면 `L[i]`를, 아니면 `R[j]`를 결과에 추가한다.
  3) 최종 경로 `order`를 얻는다.
- 답 구성: `order`의 앞쪽 `p`개 문제 번호를 출력.

올바름(핵심 근거):
- 토너먼트에서 분할정복-머지 방식은 해밀토니안 경로를 생성한다(머지 중 항상 하나가 다수결에서 우세이므로 진행 가능).
- 생성된 경로의 선두 `p`개는 무작위 교체 프로세스에서 양의 정적분 확률로 반복 출현하는 plausible set이 됨이 알려져 있다(관련 대회/에디토리얼 정리).

## 복잡도
- 시간: `O(k log k)`번 비교 × 비교당 `O(n)` → `O(n · k log k)`
- 공간: `O(n · k)` (선호 순위 테이블) + `O(k)` (재귀/머지 보조 배열)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k, p;
    if (!(cin >> n >> k >> p)) return 0;

    vector<vector<int>> pos(n, vector<int>(k + 1));
    for (int j = 0; j < n; ++j) {
        for (int r = 1; r <= k; ++r) {
            int id; cin >> id;
            pos[j][id] = r;
        }
    }

    const int maj = (n / 2) + 1;
    auto beats = [&](int a, int b) -> bool {
        int cnt = 0;
        for (int j = 0; j < n; ++j) {
            if (pos[j][a] < pos[j][b]) {
                if (++cnt >= maj) return true;
            }
        }
        return false;
    };

    function<vector<int>(const vector<int>&)> build = [&](const vector<int>& v) -> vector<int> {
        if (v.size() <= 1) return v;
        size_t mid = v.size() / 2;
        vector<int> L(v.begin(), v.begin() + mid);
        vector<int> R(v.begin() + mid, v.end());
        L = build(L);
        R = build(R);
        vector<int> res; res.reserve(v.size());
        size_t i = 0, j = 0;
        while (i < L.size() && j < R.size()) {
            if (beats(L[i], R[j])) res.push_back(L[i++]);
            else res.push_back(R[j++]);
        }
        while (i < L.size()) res.push_back(L[i++]);
        while (j < R.size()) res.push_back(R[j++]);
        return res;
    };

    vector<int> all(k); iota(all.begin(), all.end(), 1);
    vector<int> order = build(all);
    for (int i = 0; i < p; ++i) {
        if (i) cout << ' ';
        cout << order[i];
    }
    cout << '\n';
    return 0;
}
```

## 6-1) 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def solve():
    n, k, p = map(int, input().split())
    pos = [[0]*(k+1) for _ in range(n)]
    for j in range(n):
        arr = list(map(int, input().split()))
        for r, pid in enumerate(arr, 1):
            pos[j][pid] = r

    maj = (n // 2) + 1

    def beats(a: int, b: int) -> bool:
        cnt = 0
        for j in range(n):
            if pos[j][a] < pos[j][b]:
                cnt += 1
                if cnt >= maj:
                    return True
        return False

    def build(v):
        if len(v) <= 1:
            return v
        mid = len(v) // 2
        L = build(v[:mid])
        R = build(v[mid:])
        res = []
        i = j = 0
        while i < len(L) and j < len(R):
            if beats(L[i], R[j]):
                res.append(L[i]); i += 1
            else:
                res.append(R[j]); j += 1
        if i < len(L):
            res.extend(L[i:])
        if j < len(R):
            res.extend(R[j:])
        return res

    order = build(list(range(1, k+1)))
    print(*order[:p])

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- `n=1`(항상 선호 동일 경로, 아무 경로나 가능), `p=1`, `p=k-1` 등 극단 파라미터
- 선호 순위가 거의 동일/역순/랜덤 분포
- `k`가 최대(5e4)인 대형 입력에서 시간·메모리 한계 여유 확인
- 출력 공백/개행, 1-based 번호 유지

## 제출 전 점검
- 입출력 형식/개행 확인, 인덱스 1-based 유지
- 64-bit 정수 불필요(모두 인덱스), 초기화/경계/재귀 깊이(Python에서 setrecursionlimit)
- C++ `beats` 조기 종료(과반 달성 시 탈출로 속도 향상)

## 참고자료/유사문제
- Petrozavodsk Winter 2019 Day 5 (Gennady Korotkevich Contest 4) I – Nine Judges
- Open Cup 2018/2019 Grand Prix of Gomel I – Nine Judges
- 토너먼트의 해밀토니안 경로 고전 정리 및 관련 에디토리얼


