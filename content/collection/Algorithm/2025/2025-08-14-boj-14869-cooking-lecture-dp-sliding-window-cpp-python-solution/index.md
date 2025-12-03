---
title: "[Algorithm] C++/Python 백준 14869번: 요리 강좌 - DP, 슬라이딩 윈도우 최적화"
description: "연속 수강 길이 S~E, 학원 변경 비용 T, 불허용 학원 제약을 동시에 만족하는 최소비용을 구합니다. prefix sum과 단조 큐로 블록 DP를 슬라이딩 윈도우 최적화해 O(NM)로 해결, 정당성과 엣지 케이스 점검까지 담았습니다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- "Algorithm"
- "Dynamic Programming"
tags:
- "Algorithm"
- "알고리즘"
- "BOJ"
- "백준"
- "Problem-14869"
- "cpp"
- "C++"
- "python"
- "Python"
- "Implementation"
- "구현"
- "Time Complexity"
- "시간복잡도"
- "Space Complexity"
- "공간복잡도"
- "Proof of Correctness"
- "정당성 증명"
- "Edge Cases"
- "코너 케이스"
- "Pitfalls"
- "실수 포인트"
- "Optimization"
- "최적화"
- "Competitive Programming"
- "경쟁프로그래밍"
- "Editorial"
- "에디토리얼"
- "Code Review"
- "코드리뷰"
- "Template"
- "템플릿"
- "Testing"
- "테스트"
- "Complexity Analysis"
- "복잡도 분석"
- "Invariant"
- "불변식"
- "Dynamic Programming"
- "동적계획법"
- "DP Optimization"
- "DP 최적화"
- "Sliding Window"
- "슬라이딩윈도우"
- "Monotone Queue"
- "단조 큐"
- "Deque"
- "덱"
- "Prefix Sum"
- "누적합"
- "Range DP"
- "구간 DP"
- "Run Length"
- "구간 길이 제약"
- "Forbidden Academy"
- "불허용 학원"
- "Transition"
- "전이"
- "Window Minima"
- "윈도우 최소값"
- "KOI"
- "KOI 2017"
- "Cooking Lecture"
- "요리 강좌"
- "State"
- "상태"
- "Boundary Conditions"
- "경계 조건"
- "64-bit"
- "long long"
- "Memory"
- "메모리"
- "Subtasks"
- "서브태스크"
- "O(NM)"
- "빅오"
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/14869
- 요약: N개 학원에서 M개의 강좌를 순서대로 수강한다. 한 학원에서 연속 수강 가능한 강좌 수는 S~E이고(단, 마지막 블록은 1~E 허용), 블록이 바뀔 때마다 비용 T가 든다. 또 학원 i로 옮길 때 직전 학원이 `불허용 학원[i]`이면 안 된다. 전체 최소 비용을 구한다.

## 입력/출력
```
입력
N M S E T
N줄의 비용 행렬 (각 줄에 M개)
N줄의 불허용 학원 번호(1-indexed)

출력
최소 비용
```

예시(문제 본문):
```
입력
4 5 2 3 2
1 2 1 3 8
1 2 3 7 2
1 8 8 1 2
10 1 1 8 8
2
3
4
3

출력
9
```

## 접근 개요
- 핵심 모델링: 수강 계획은 같은 학원으로 이루어진 연속 구간(블록)들의 연결이다. 블록 길이는 앞의 블록들에 대해 S~E, 마지막 블록은 1~E 허용.
- 블록이 바뀔 때마다 T가 추가. 또한 새 블록 학원 i는 직전 블록 학원이 i도 아니고 `banned[i]`도 아니어야 한다.
- `dp[j][i]`: j번째 강좌까지 수강을 끝냈고 마지막 블록의 학원이 i일 때 최소 비용.
- 전이: j에서 끝나는 블록의 시작을 t+1이라 하면(즉 길이 L=j−t), 앞의 유효 t는 j−E ≤ t ≤ j−S (단, j=M이면 j−E ≤ t ≤ j−1). 비용은 `블록(i, t+1..j)` + `(t==0 ? 0 : min_{p!=i, p!=banned[i]} dp[t][p] + T)`.
- 블록 비용은 학원 i의 구간합으로 O(1) 계산(누적합).
- 전이에서 t는 구간(슬라이딩 윈도우)이므로 각 학원 i에 대해 `G_i[t] = (t==0?0:bestPrev(i,t)+T) - prefix[i][t]`를 유지하면 `dp[j][i] = min_{t in window} G_i[t] + prefix[i][j]`로 변형 가능.
- 각 i별로 t에 대한 단조 큐(덱)로 윈도우 최소값을 관리, `bestPrev(i,t)`는 그 시점 t의 전 학원 최솟값들에서 i와 `banned[i]`를 제외하여 O(1)에 선택(전역 top-3 유지) → 전체 O(NM).

```mermaid
flowchart TD
  T((t)) -->|L in [S,E]| J((j))
  subgraph Block on academy i
    direction LR
    A1[PrefixSum(i, t..j)]
  end
  T -->|dp[t][p] + T, p!=i, p!=banned[i]| J
  J -->|min over t-window| DPj[dp[j][i]]
```

## 알고리즘
- 전처리: 학원 i(0-index)의 누적합 `prefix[i][k] = sum(cost[i][1..k])`.
- 상태: `dp[j][i]`는 명시 저장 대신, 각 j마다 현재 열만 유지.
- 보조값: 각 i에 대해 덱에 `(t, G_i[t])`를 유지. 윈도우는 j가 증가할 때 `[max(0,j−E) .. (j<M? j−S : j−1)]`로 이동.
- 전역 최솟값: 각 t에서 `minV1, minI1`, `minV2, minI2`, `minV3, minI3`를 유지하여, i와 `banned[i]` 제외한 최솟값을 O(1)로 선택.
- 계산: 각 j에서 유효 t들을 덱에 밀어넣고 만료 t를 팝. 그 후 `dp[j][i] = front(G_i) + prefix[i][j]`.
- 정당성: 블록 분해의 최적성(각 블록 비용은 독립 구간합), 동일 학원으로 블록을 쪼개는 선택은 항상 병합한 해보다 이득이 없으므로 경계에서 `i` 제외가 무손실. 불허용 학원은 전이 시 후보에서 제외하여 강제.

## 복잡도
- 시간: O(NM)
- 공간: O(NM) (누적합) + O(N) (덱/현재 열/전역 최솟값)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M, S, E, T;
    if (!(cin >> N >> M >> S >> E >> T)) return 0;

    const long long INF = (long long)4e18;

    vector<vector<long long>> prefix(N, vector<long long>(M + 1, 0));
    for (int i = 0; i < N; ++i) {
        for (int j = 1; j <= M; ++j) {
            int c; cin >> c;
            prefix[i][j] = prefix[i][j - 1] + c;
        }
    }
    vector<int> banned(N);
    for (int i = 0; i < N; ++i) {
        int x; cin >> x;
        banned[i] = x - 1; // zero-based
    }

    vector<deque<pair<int, long long>>> dq(N);
    vector<long long> dp(N, INF);

    vector<long long> minV1(M + 1, INF), minV2(M + 1, INF), minV3(M + 1, INF);
    vector<int> minI1(M + 1, -1), minI2(M + 1, -1), minI3(M + 1, -1);

    auto choosePrev = [&](int t, int i) -> long long {
        long long v1 = minV1[t], v2 = minV2[t], v3 = minV3[t];
        int i1 = minI1[t], i2 = minI2[t], i3 = minI3[t];
        if (i1 != i && i1 != banned[i]) return v1;
        if (i2 != -1 && i2 != i && i2 != banned[i]) return v2;
        return v3; // N >= 3
    };

    int lastPushedT = -1;

    for (int j = 1; j <= M; ++j) {
        int lbound = max(0, j - E);
        int ubound = (j == M ? j - 1 : j - S);

        for (int i = 0; i < N; ++i) {
            while (!dq[i].empty() && dq[i].front().first < lbound) dq[i].pop_front();
        }

        if (ubound > lastPushedT) {
            for (int t = lastPushedT + 1; t <= ubound; ++t) {
                if (t == 0) {
                    for (int i = 0; i < N; ++i) {
                        long long val = 0; // 0 - prefix[i][0]
                        while (!dq[i].empty() && dq[i].back().second >= val) dq[i].pop_back();
                        dq[i].emplace_back(t, val);
                    }
                } else {
                    for (int i = 0; i < N; ++i) {
                        long long bestPrev = choosePrev(t, i);
                        long long val = (bestPrev >= INF / 4) ? INF : bestPrev + T - prefix[i][t];
                        while (!dq[i].empty() && dq[i].back().second >= val) dq[i].pop_back();
                        dq[i].emplace_back(t, val);
                    }
                }
            }
            lastPushedT = ubound;
        }

        if (ubound >= lbound) {
            for (int i = 0; i < N; ++i) {
                if (dq[i].empty()) dp[i] = INF;
                else {
                    long long base = dq[i].front().second;
                    dp[i] = (base >= INF / 4) ? INF : base + prefix[i][j];
                }
            }
        } else {
            for (int i = 0; i < N; ++i) dp[i] = INF;
        }

        long long v1 = INF, v2 = INF, v3 = INF; int i1 = -1, i2 = -1, i3 = -1;
        for (int i = 0; i < N; ++i) {
            long long v = dp[i];
            if (v < v1) { v3 = v2; i3 = i2; v2 = v1; i2 = i1; v1 = v; i1 = i; }
            else if (v < v2) { v3 = v2; i3 = i2; v2 = v; i2 = i; }
            else if (v < v3) { v3 = v; i3 = i; }
        }
        minV1[j] = v1; minI1[j] = i1;
        minV2[j] = v2; minI2[j] = i2;
        minV3[j] = v3; minI3[j] = i3;
    }

    long long ans = INF;
    for (int i = 0; i < N; ++i) ans = min(ans, dp[i]);
    cout << ans << '\n';
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from collections import deque

def main():
    input = sys.stdin.readline
    N, M, S, E, T = map(int, input().split())
    INF = 4 * 10**18

    prefix = [[0]*(M+1) for _ in range(N)]
    for i in range(N):
        arr = list(map(int, input().split()))
        ps = prefix[i]
        for j, c in enumerate(arr, start=1):
            ps[j] = ps[j-1] + c
    banned = [int(input())-1 for _ in range(N)]

    dq = [deque() for _ in range(N)]
    dp = [INF]*N

    minV1 = [INF]*(M+1)
    minV2 = [INF]*(M+1)
    minV3 = [INF]*(M+1)
    minI1 = [-1]*(M+1)
    minI2 = [-1]*(M+1)
    minI3 = [-1]*(M+1)

    def choose_prev(t, i):
        v1, v2, v3 = minV1[t], minV2[t], minV3[t]
        i1, i2, i3 = minI1[t], minI2[t], minI3[t]
        if i1 != i and i1 != banned[i]:
            return v1
        if i2 != -1 and i2 != i and i2 != banned[i]:
            return v2
        return v3

    last_pushed_t = -1

    for j in range(1, M+1):
        lbound = max(0, j - E)
        ubound = (j - 1) if (j == M) else (j - S)

        for i in range(N):
            while dq[i] and dq[i][0][0] < lbound:
                dq[i].popleft()

        if ubound > last_pushed_t:
            for t in range(last_pushed_t + 1, ubound + 1):
                if t == 0:
                    for i in range(N):
                        val = 0
                        while dq[i] and dq[i][-1][1] >= val:
                            dq[i].pop()
                        dq[i].append((t, val))
                else:
                    for i in range(N):
                        best_prev = choose_prev(t, i)
                        val = INF if best_prev >= INF//4 else best_prev + T - prefix[i][t]
                        while dq[i] and dq[i][-1][1] >= val:
                            dq[i].pop()
                        dq[i].append((t, val))
            last_pushed_t = ubound

        if ubound >= lbound:
            for i in range(N):
                if not dq[i]:
                    dp[i] = INF
                else:
                    base = dq[i][0][1]
                    dp[i] = INF if base >= INF//4 else base + prefix[i][j]
        else:
            for i in range(N):
                dp[i] = INF

        v1 = v2 = v3 = INF
        i1 = i2 = i3 = -1
        for i in range(N):
            v = dp[i]
            if v < v1:
                v3, i3 = v2, i2
                v2, i2 = v1, i1
                v1, i1 = v, i
            elif v < v2:
                v3, i3 = v2, i2
                v2, i2 = v, i
            elif v < v3:
                v3, i3 = v, i
        minV1[j], minI1[j] = v1, i1
        minV2[j], minI2[j] = v2, i2
        minV3[j], minI3[j] = v3, i3

    ans = min(dp)
    print(ans)

if __name__ == "__main__":
    main()
```

## 코너 케이스 체크리스트
- 마지막 블록은 1~E 길이 허용: j=M일 때 윈도우 상한을 `j-1`로 설정
- S=1, E=1: 모든 블록 길이 1, 전이만 발생 → 불허용/같은 학원 제외 로직 필수
- T=0: 같은 학원으로 블록을 쪼갤 유인이 없으므로 경계에서 같은 학원 제외해도 무손실
- E≥M: 단일 블록 가능, t=0 전이(시작 케이스)로 커버
- 불허용 학원=자기 자신/서로 교차: 전역 top-3에서 안전하게 제외해 INF 방지(N≥3)
- 비용 상한/합산: `long long` 사용, INF 여유

## 제출 전 점검
- 입력/출력 형식과 개행
- 누적합 인덱스(1-indexed) 일관성
- 전이 범위: j<M은 [j−E..j−S], j=M은 [j−E..j−1]
- 같은 학원/불허용 학원 제외가 올바른지 확인
- 64-bit 정수 사용, 오버플로 방지

## 참고자료
- 문제: https://www.acmicpc.net/problem/14869
- 출처: KOI 2017 고등부 3번


