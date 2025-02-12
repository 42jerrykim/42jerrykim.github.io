---
title: "[Algorithm] C++/Python 백준 8217번 : 유성"
categories: 
- Algorithm
- Diamond IV
- Segment Tree
- Binary Search
tags:
- Parallel Binary Search
- Binary Indexed Tree
- Simulation
- Inlining
- O((Q+M)*log M)
- Fenwick Tree
- Mathematical Idea
- Binary Search
image: "index.png"
date: 2025-02-03
---

이번 포스트에서는 백준 8217번 **유성** 문제를 해결하는 과정을 소개한다. 문제는 원형 구간에 운석이 내리는 시뮬레이션과, 각 회원국이 목표 운석 수를 달성하는 최소 날짜를 구하는 문제로 구성되어 있다. 이 문제는 입력 규모가 매우 크기 때문에, 단순한 시뮬레이션 방식으로는 시간 초과가 발생한다. 따라서, **Binary Indexed Tree(Fenwick Tree)**를 이용한 구간 업데이트와 **Parallel Binary Search** 기법을 결합하여 효율적으로 문제를 해결하였다. 본 포스트에서는 C++와 Python 두 가지 언어로 최적화된 코드를 작성하고, 코드의 각 부분을 상세하게 설명한다.

문제 : [https://www.acmicpc.net/problem/8217](https://www.acmicpc.net/problem/8217)

## 문제 설명

문제 **유성**는 BIU(백준 우주 연합)가 새로 발견한 행성에서 운석 샘플을 채취하는 상황을 배경으로 한다. 행성의 궤도는 원형으로 구성되어 있으며, 이를 M개의 구역으로 나누어 1번부터 M번까지 번호를 부여한다. 각 구역은 BIU 회원국 중 한 나라가 소유하고 있으며, 각 회원국은 자신만의 운석 샘플 목표량 \(p_j\)를 설정한다.  
문제에서는 Q일간 예보된 유성우 정보가 주어진다. 각 날짜마다 특정 구역 범위에 일정량의 운석이 내리는데, 행성의 궤도가 원형이므로 만약 시작 구역 번호가 종료 구역 번호보다 큰 경우, 두 구간 \([l, M]\)과 \([1, r]\)에 동시에 운석이 떨어진다.  
각 회원국은 자신이 소유한 구역에 내린 운석의 누적 합이 목표량 이상이 되는 최소 날짜를 구해야 한다. 만약 Q일 동안 목표를 달성하지 못하면 "NIE"를 출력해야 한다.  
문제의 핵심은 큰 입력 규모와 wrap-around 구간 업데이트를 빠르게 처리하는 것이다. 단순 시뮬레이션으로는 시간 초과가 발생하기 때문에, 효율적인 자료구조와 알고리즘을 사용하여 각 회원국별로 빠르게 최소 날짜를 결정해야 한다.

## 접근 방식

이 문제는 두 가지 핵심 난관을 가진다. 첫째, 매일의 유성우 업데이트에 대해 원형 구간(일부는 wrap-around)을 빠르게 처리해야 하며, 둘째, 각 회원국이 소유한 여러 구역에 대해 누적 합을 빠르게 계산해야 한다. 이를 위해 **Binary Indexed Tree (BIT)**를 사용하여 구간 업데이트와 점 쿼리를 \(O(\log M)\) 시간에 수행하도록 하였다.  
또한, 각 회원국이 목표 운석 수를 달성하는 최소 날짜를 결정하기 위해 **Parallel Binary Search** 기법을 사용하였다. 각 회원국에 대해 초기 검색 범위를 \([1, Q+1]\)로 설정한 후, candidate day(중간값)를 기준으로 1일부터 해당 날짜까지의 모든 유성우 업데이트를 BIT에 반영하여 시뮬레이션한다. 각 회원국이 소유한 구역에 대해 BIT 쿼리를 수행하고, 누적 운석 수가 목표 이상인 경우 이분 탐색 범위를 하향 조정하며, 그렇지 않은 경우 상향 조정한다. 이 과정으로 전체 시간 복잡도는 \(O((Q+M)\log M)\) 내로 해결할 수 있다.

## C++ 코드와 설명

아래는 최적화된 C++ 코드이다. 각 줄에 주석을 추가하여 코드의 동작을 상세히 설명하였다.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
 
typedef long long ll;
 
// Binary Indexed Tree (Fenwick Tree)를 구현한다.
// BIT는 구간 업데이트와 점 쿼리를 O(log n) 시간에 수행한다.
struct BIT {
    int n;
    vector<ll> tree;
    BIT(int n) : n(n), tree(n+1, 0) { }
    
    // BIT에 delta 값을 더한다. i부터 n까지 영향을 준다.
    void update(int i, ll delta) {
        for(; i <= n; i += i & -i)
            tree[i] += delta;
    }
    
    // BIT의 1부터 i까지의 합을 반환한다.
    ll query(int i) {
        ll sum = 0;
        for(; i; i -= i & -i)
            sum += tree[i];
        return sum;
    }
    
    // BIT를 초기화한다.
    void clear() {
        fill(tree.begin(), tree.end(), 0);
    }
};
 
// 각 유성우 업데이트 정보를 저장하는 구조체
struct Update {
    int l, r;
    ll a;
};
 
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N, M;
    cin >> N >> M;
    
    // 1번부터 M번 구역의 소유국 정보를 입력받는다.
    vector<int> owner(M+1);
    for (int i = 1; i <= M; i++){
        cin >> owner[i];
    }
    
    // 각 회원국의 목표 운석 샘플 수량을 입력받는다.
    vector<ll> target(N+1);
    for (int i = 1; i <= N; i++){
        cin >> target[i];
    }
    
    int Q;
    cin >> Q;
    // 유성우 업데이트 정보를 입력받는다.
    vector<Update> updates(Q+1);
    for (int i = 1; i <= Q; i++){
        int l, r;
        ll a;
        cin >> l >> r >> a;
        updates[i] = {l, r, a};
    }
    
    // 각 회원국이 소유한 구역 인덱스를 저장한다.
    vector<vector<int>> zonesByCountry(N+1);
    for (int i = 1; i <= M; i++){
        zonesByCountry[owner[i]].push_back(i);
    }
    
    // 각 회원국에 대해 이분 탐색을 위한 초기 범위를 설정한다.
    vector<int> lo(N+1, 1), hi(N+1, Q+1);
    
    // candidate day(중간값)를 기준으로 처리할 회원국 번호를 모아둘 bucket
    vector<vector<int>> bucket(Q+2);
    
    BIT bit(M+1);
    
    // Parallel Binary Search 진행
    while (true) {
        bool progress = false;
        // 각 날짜에 해당하는 bucket을 초기화
        for (int d = 1; d <= Q; d++){
            bucket[d].clear();
        }
        
        // 아직 결정되지 않은 회원국에 대해 candidate day를 계산하여 bucket에 추가한다.
        for (int i = 1; i <= N; i++){
            if (lo[i] < hi[i]) {
                progress = true;
                int mid = (lo[i] + hi[i]) / 2;
                bucket[mid].push_back(i);
            }
        }
        if (!progress) break;
        
        // BIT를 초기화
        bit.clear();
        
        // 1일부터 Q일까지 유성우 업데이트를 적용하며, candidate day에 해당하는 회원국의 검증을 수행한다.
        for (int day = 1; day <= Q; day++){
            int l = updates[day].l, r = updates[day].r;
            ll a = updates[day].a;
            if (l <= r) {
                // 일반 구간 [l, r] 업데이트
                bit.update(l, a);
                bit.update(r+1, -a);
            } else {
                // wrap-around인 경우: [l, M]과 [1, r] 업데이트
                bit.update(l, a);
                bit.update(M+1, -a);
                bit.update(1, a);
                bit.update(r+1, -a);
            }
            
            // candidate day가 현재 day와 같은 회원국에 대해 목표 달성 여부 확인
            if (!bucket[day].empty()){
                for (int country : bucket[day]) {
                    ll sum = 0;
                    // 해당 회원국이 소유한 모든 구역에 대해 BIT 쿼리를 수행
                    for (int pos : zonesByCountry[country]){
                        sum += bit.query(pos);
                        if(sum >= target[country])
                            break;
                    }
                    // 목표 달성 여부에 따라 이분 탐색 범위를 조정
                    if(sum >= target[country])
                        hi[country] = day;
                    else
                        lo[country] = day + 1;
                }
            }
        }
    }
    
    // 결과 출력: 목표 달성 불가능한 경우 "NIE" 출력
    for (int i = 1; i <= N; i++){
        if(hi[i] == Q+1)
            cout << "NIE\n";
        else
            cout << hi[i] << "\n";
    }
    
    return 0;
}
```

**C++ 코드 동작 요약**

- **입력 및 전처리:** 구역 소유 정보, 회원국별 목표, 유성우 업데이트 정보를 입력받고, 각 회원국이 소유한 구역 인덱스를 저장한다.
- **BIT 활용:** BIT를 이용하여 구간 업데이트와 점 쿼리를 \(O(\log M)\)에 수행한다.
- **Parallel Binary Search:** 각 회원국에 대해 candidate day를 bucket에 모은 뒤, 1일부터 해당 날짜까지의 업데이트를 적용해 목표 달성 여부를 확인하고, 이분 탐색 범위를 조정한다.
- **결과 출력:** 최종적으로 각 회원국이 목표를 달성할 수 있는 최소 날짜를 출력하며, 불가능할 경우 "NIE"를 출력한다.

## Python 코드와 설명

아래는 Python으로 구현한 최종 버전 코드이다. Python 특성상 최적화를 위해 sys.stdin.buffer와 sys.stdout.write를 사용하고, BIT 업데이트와 쿼리를 내부 while 루프로 직접 구현하여 함수 호출 오버헤드를 줄였다.

```python
import sys
def main():
    # 빠른 입력을 위해 sys.stdin.buffer.read() 사용
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    # 1-indexed로 구역의 소유국 정보를 저장
    owner = [0] * (M + 1)
    for i in range(1, M + 1):
        owner[i] = int(next(it))
    # 각 회원국의 목표 운석 샘플 수량 (1-indexed)
    target = [0] * (N + 1)
    for i in range(1, N + 1):
        target[i] = int(next(it))
    Q = int(next(it))
    # 업데이트 정보: (l, r, a) 튜플을 1-indexed로 저장
    updates = [None] * (Q + 1)
    for i in range(1, Q + 1):
        l = int(next(it)); r = int(next(it)); a = int(next(it))
        updates[i] = (l, r, a)
    
    # 각 회원국이 소유한 구역의 인덱스 리스트를 미리 저장 (1-indexed)
    zonesByCountry = [[] for _ in range(N + 1)]
    for pos in range(1, M + 1):
        zonesByCountry[ owner[pos] ].append(pos)
    
    # 각 회원국의 목표 달성 날짜를 찾기 위해 이분 탐색 범위를 설정
    # lo[i] ~ hi[i]-1 중 최소로 목표를 달성할 수 있는 날
    lo = [1] * (N + 1)
    hi = [Q + 1] * (N + 1)
    
    # candidate day(업데이트 날짜)를 기준으로 처리할 회원국 번호를 모아둘 bucket
    bucket = [[] for _ in range(Q + 2)]
    
    # BIT 배열 (1-indexed, 인덱스 1 ~ M+1 사용)
    size_BIT = M + 1
    BIT = [0] * (size_BIT + 1)
    m_val = size_BIT  # BIT의 최대 인덱스
    
    # Parallel Binary Search 진행
    while True:
        progress = False
        # bucket 초기화: 후보 날짜 1~Q
        for d in range(1, Q + 1):
            bucket[d].clear()
        # 아직 결정되지 않은 회원국에 대해 중간값(mid) 계산 후 bucket에 추가
        for i in range(1, N + 1):
            if lo[i] < hi[i]:
                progress = True
                mid = (lo[i] + hi[i]) >> 1  # (lo+hi)//2
                bucket[mid].append(i)
        if not progress:
            break

        # BIT 초기화: 모든 값을 0으로 재설정
        for i in range(m_val + 1):
            BIT[i] = 0

        # 1일부터 Q일까지 업데이트를 순차적으로 적용하며, candidate day에 해당하는 회원국 검증
        for day in range(1, Q + 1):
            l, r, a = updates[day]
            if l <= r:
                # 구간 [l, r] 업데이트
                i = l
                while i <= m_val:
                    BIT[i] += a
                    i += i & -i
                i = r + 1
                while i <= m_val:
                    BIT[i] -= a
                    i += i & -i
            else:
                # wrap-around인 경우: [l, m_val]과 [1, r] 업데이트
                i = l
                while i <= m_val:
                    BIT[i] += a
                    i += i & -i
                i = m_val
                while i <= m_val:
                    BIT[i] -= a
                    i += i & -i
                i = 1
                while i <= m_val:
                    BIT[i] += a
                    i += i & -i
                i = r + 1
                while i <= m_val:
                    BIT[i] -= a
                    i += i & -i

            # candidate day가 현재 day인 회원국들에 대해 목표 달성 여부 확인
            if bucket[day]:
                for country in bucket[day]:
                    tot = 0
                    for pos in zonesByCountry[country]:
                        s = 0
                        j = pos
                        while j:
                            s += BIT[j]
                            j -= j & -j
                        tot += s
                        if tot >= target[country]:
                            break
                    if tot >= target[country]:
                        hi[country] = day
                    else:
                        lo[country] = day + 1

        # 하루 단위 업데이트 for-loop 종료

    # 결과 출력: 목표 달성이 불가능하면 "NIE" 출력
    out_lines = []
    for i in range(1, N + 1):
        out_lines.append("NIE" if hi[i] == Q + 1 else str(hi[i]))
    sys.stdout.write("\n".join(out_lines))

if __name__ == '__main__':
    main()
```

**Python 코드 동작 요약**

- **입력 및 전처리:** sys.stdin.buffer.read()로 빠르게 입력을 받아, 각 구역의 소유 정보와 회원국별 목표, 유성우 업데이트 정보를 파싱한다.
- **BIT 구현:** BIT 배열을 직접 관리하며, while 루프를 통해 구간 업데이트와 점 쿼리를 수행하여 함수 호출 오버헤드를 최소화하였다.
- **Parallel Binary Search:** 각 회원국에 대해 이분 탐색 범위를 설정하고, candidate day마다 BIT에 업데이트를 적용한 후, 각 회원국의 소유 구역에 대해 누적 합을 계산하여 이분 탐색 범위를 조정한다.
- **결과 출력:** 각 회원국의 목표 달성 최소 날짜를 출력하며, 달성 불가능한 경우 "NIE"를 출력한다.

## 결론

이번 문제는 큰 입력 규모와 원형 구간 업데이트라는 난관을 극복하기 위해 **Binary Indexed Tree**와 **Parallel Binary Search** 기법을 결합하여 해결하였다. C++와 Python 두 가지 언어로 최적화된 코드를 구현하며, 특히 Python에서는 함수 호출 오버헤드를 줄이고 지역 변수 캐싱 및 인라인 구현을 통해 최대한 효율적으로 작성하였다.  
문제 풀이를 통해 자료구조와 알고리즘의 적절한 결합이 극한의 제약 조건에서도 효과적으로 작동할 수 있음을 다시 한 번 확인할 수 있었다. 향후 유사한 문제에서도 이와 같은 최적화 기법을 적극 활용할 수 있을 것으로 보인다.