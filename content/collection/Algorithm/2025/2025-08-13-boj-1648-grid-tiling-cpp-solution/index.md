---
title: "[Algorithm] C++ 백준 1648번: 격자판 채우기"
description: "2x1 도미노로 N×M 격자를 빈칸 없이 채우는 경우의 수를 9901로 계산. 열 너비 W를 최소로 두고 상태압축 비트마스크 DP로 스캔하며 수평/수직 배치 전이를 수행한다. 마스크 불변식으로 정당성을 보이고, 시간/공간 복잡도와 구현 포인트, 엣지 케이스(N·M 홀수=0)까지 정리했다."
date: 2025-08-13
lastmod: 2025-08-13
categories:
- Algorithm
- Dynamic Programming
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-1648
- cpp
- C++
- Dynamic Programming
- 동적계획법
- DP
- Bitmask
- 비트마스크
- State Compression
- 상태압축
- Profile DP
- 프로필DP
- Grid
- 격자
- Grid Tiling
- 격자 타일링
- Domino
- 도미노
- Tiling
- 타일링
- Implementation
- 구현
- Recursion
- 재귀
- Memoization
- 메모이제이션
- Invariant
- 불변식
- Proof of Correctness
- 정당성 증명
- Complexity Analysis
- 복잡도 분석
- Time Complexity
- 시간복잡도
- Space Complexity
- 공간복잡도
- Optimization
- 최적화
- Modulo
- 모듈러
- 9901
- Mask DP
- 마스크 DP
- Row-major Scan
- 행우선스캔
- Competitive Programming
- 경쟁프로그래밍
- Editorial
- 에디토리얼
- Testing
- 테스트
- Edge Cases
- 코너 케이스
- Implementation Details
- 구현 디테일
- Code Review
- 코드리뷰
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/1648
- 요약: 2x1(또는 1x2) 도미노로 N×M 격자를 빈칸 없이 채우는 가짓수를 9901로 출력한다.

### 제한/스펙
- 1 ≤ N, M ≤ 14, 시간 2초, 메모리 128MB
- 정답을 9901로 나눈 나머지 출력

## 입출력
```
입력
3 6

출력
41
```

```
입력
5 5

출력
0
```

## 접근 개요
- 열 너비 W를 min(N, M)로 두고, 격자를 행(또는 열) 우선으로 한 칸씩 스캔한다.
- 길이 W의 비트마스크로 "현재 위치 포함 오른쪽으로 W칸 구간에서 위로부터 내려온 수직 도미노로 이미 점유된 칸" 상태를 관리한다.
- 현재 칸이 점유(mask의 LSB=1)이면 다음 칸으로 진행, 비어 있으면 수평(오른쪽) 또는 수직(아래) 배치를 시도한다.
- 메모이제이션된 DFS/DP로 상태 `(pos, mask)`를 캐싱하여 O(H·W·2^W) 시간에 해결한다(H=max(N,M)).

## 알고리즘 설계
- 상태: `pos ∈ [0, H*W)`, `mask ∈ [0, 1<<W)`
  - `pos`는 스캔 인덱스, `mask`의 LSB는 `pos` 칸의 점유 여부를 나타낸다.
- 전이:
  - `mask & 1 = 1`이면 해당 칸은 이미 점유 → `dfs(pos+1, mask>>1)`
  - 아니라면 두 선택지를 고려
    - 수평 배치: 같은 행에서 `c+1 < W`이고 다음 칸도 비어 있어야 함 → 새로운 마스크 `(mask>>1) | 1`
    - 수직 배치: 아래 행 존재(`r+1 < H`) → 새로운 마스크 `(mask>>1) | (1<<(W-1))`
- 기저: `pos == H*W`이면 `mask == 0`인 경우만 1을 반환
- 올바름(핵심 근거):
  - 마스크는 아직 처리되지 않은 윈도우의 점유 상태를 정확히 추적하며, 수평/수직 전이는 도미노 배치의 유일한 두 경우만을 허용한다.
  - 모든 칸을 좌→우, 상→하로 한 번씩 방문하므로 중복/누락 없이 완전 탐색이 되며, 동일 상태의 재방문은 메모이제이션으로 통합된다.

## 복잡도
- 시간: O(H·W·2^W) (W = min(N, M) ≤ 14)
- 공간: O(H·2^W)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <iostream>
#include <vector>
#include <functional>
using namespace std;

static const int MOD = 9901;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    if (!(cin >> N >> M)) return 0;

    int H = max(N, M);
    int W = min(N, M);

    if ((H * W) % 2 == 1) {
        cout << 0;
        return 0;
    }

    vector<vector<int>> dp(H * W + 1, vector<int>(1 << W, -1));

    function<int(int, int)> dfs = [&](int pos, int mask) -> int {
        if (pos == H * W) return mask == 0 ? 1 : 0;
        int &res = dp[pos][mask];
        if (res != -1) return res;
        res = 0;

        int r = pos / W;
        int c = pos % W;

        if (mask & 1) {
            res = dfs(pos + 1, mask >> 1);
        } else {
            if (c + 1 < W && (mask & 2) == 0) {
                res += dfs(pos + 1, (mask >> 1) | 1);
                if (res >= MOD) res -= MOD;
            }
            if (r + 1 < H) {
                res += dfs(pos + 1, (mask >> 1) | (1 << (W - 1)));
                if (res >= MOD) res -= MOD;
            }
        }
        return res;
    };

    cout << dfs(0, 0) % MOD;
    return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)
MOD = 9901


def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N, M = map(int, data[:2])
    H, W = (N, M) if N >= M else (M, N)
    if (H * W) % 2 == 1:
        print(0)
        return

    @lru_cache(None)
    def dfs(pos: int, mask: int) -> int:
        if pos == H * W:
            return 1 if mask == 0 else 0
        r, c = divmod(pos, W)
        if mask & 1:
            return dfs(pos + 1, mask >> 1)
        total = 0
        if c + 1 < W and (mask & 2) == 0:
            total += dfs(pos + 1, (mask >> 1) | 1)
        if r + 1 < H:
            total += dfs(pos + 1, (mask >> 1) | (1 << (W - 1)))
        return total % MOD

    print(dfs(0, 0) % MOD)


if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- N·M이 홀수인 경우 → 정답 0
- W=1(세로 또는 가로 한 변이 1) → 짝수 길이만 성립
- N=M=1 → 0, N=M=2 → 2
- 최대치 W=14에서도 상태 수는 2^W로 제한되어 시간 내 통과
- 대칭 입력(N, M 순서 교체)에도 동일한 결과(H=max, W=min 적용)

## 제출 전 점검
- 모듈러 9901 적용 누락 여부 점검
- 인덱스 경계: `c+1<W`, `r+1<H` 확인
- `mask` 시프트/OR 연산 실수 여부 점검
- 입력 파싱 및 출력 개행/형식 확인



