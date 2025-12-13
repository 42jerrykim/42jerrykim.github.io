---
title: "[Algorithm] C++/Python 백준 17169번: Eat Economically - 그리디 O(N log N)"
description: "2N개의 메뉴에서 점심·저녁 가격이 다를 때 i쌍(점심 i, 저녁 i)을 중복 없이 골라 총 비용을 최소화하는 문제. 잔여 그래프 관찰을 바탕으로 매 단계 3가지 증분 케이스만 비교하는 O(N log N) 그리디로 모든 i의 정답을 한 번에 계산한다."
date: 2025-08-14
lastmod: 2025-08-14
categories:
- Algorithm
- Greedy
tags:
- Algorithm
- 알고리즘
- BOJ
- 백준
- Problem-17169
- cpp
- python
- C++
- Python
- Data Structures
- 자료구조
- Implementation
- 구현
- Implementation Details
- 구현 디테일
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
- Min Cost Flow
- 최소비용유량
- Residual Graph
- 잔여그래프
- Shortest Path
- 최단경로
- Dijkstra
- 다익스트라
- Binary Search
- 이분탐색
- Two Pointers
- 투포인터
- Sliding Window
- 슬라이딩윈도우
- Hashing
- 해싱
- String
- 문자열
- Geometry
- 기하
- Math
- 수학
- Modulo
- 모듈러
- Priority Queue
- 우선순위 큐
- Multiset
- 세트
- Heap
- 힙
- O(NlogN)
- Greedy-Exchange
- 교환논법
image: "wordcloud.png"
---

## 문제
- 링크: https://www.acmicpc.net/problem/17169
- 요약: 2N개의 메뉴가 있고 각 메뉴는 `점심(l)`/`저녁(d)` 가격이 다를 수 있습니다. 하루에 점심 1개, 저녁 1개씩 먹으며 같은 메뉴를 두 번 이상 먹지 않습니다. i=1..N에 대해 점심 i개+저녁 i개를 선택할 때의 최소 총비용을 출력합니다.
- 제한: N ≤ 250,000, 가격 ≤ 1e9, 시간 3초, 메모리 1024MB

## 입력/출력
```
입력
N
l1 d1
l2 d2
...
l(2N) d(2N)

출력
N줄. i번째 줄에 점심 i개, 저녁 i개를 선택했을 때의 최소 총비용.
```

예시(문제 본문)
```
입력
1
4 9
5 3

출력
7
```

## 접근 개요
- MCMF(최소비용유량)로 자연스럽게 모델링되지만, 모든 i에 대한 답을 한 번에 구하기 위해 잔여 그래프 관찰을 이용한 그리디 증분이 가능합니다.
- 상태를 세 집합으로 유지: U(미선택), L(점심으로 선택됨), D(저녁으로 선택됨). k단계에서 k-1→k로 갈 때 총비용 증가분을 최소화하는 선택만 수행합니다.
- 증가분은 다음 3가지 조합만 고려하면 충분합니다.
  1) U에서 서로 다른 두 아이템을 골라 L과 D에 각각 배치: 비용 `min(l_i) + min(d_j)` (단 i≠j, 겹치면 두 번째 후보 사용)
  2) D의 하나를 L로 스왑(비용 `l_v - d_v`) + U에서 D 두 개 채움(비용 `min2(d)`)
  3) L의 하나를 D로 스왑(비용 `d_w - l_w`) + U에서 L 두 개 채움(비용 `min2(l)`)
- 각 단계에서 위 3가지 중 최소 증가분을 택하면 전체 최적. 이는 잔여 그래프 관점에서 두 증분 최단경로의 결합을 매 단계 최적으로 선택하는 것과 동치입니다(교환/잔여 경로 논증).

```mermaid
flowchart LR
  U((U: 미선택)) ---|U→L| L((L: 점심))
  U ---|U→D| D((D: 저녁))
  L <-->|스왑| D

  subgraph 증분 케이스
    A[1) U->L + U->D]
    B[2) D->L + U->D + U->D]
    C[3) L->D + U->L + U->L]
  end
```

## 알고리즘 설계
- 자료구조
  - `U_by_l`: U에서 `(l, id)` 최소 힙/정렬 구조
  - `U_by_d`: U에서 `(d, id)` 최소 힙/정렬 구조
  - `L_sw`: L에서 D로 바꿀 때의 증가비용 `(d-l, id)` 최소 구조
  - `D_sw`: D에서 L로 바꿀 때의 증가비용 `(l-d, id)` 최소 구조
- 단계 k(1..N)
  - 위 3케이스의 후보 비용을 계산하고 최소를 선택해 집합 이동을 반영합니다.
  - 누적합으로 총비용을 갱신하고 `ans[k]`를 기록합니다.
- 올바름 근거(요지)
  - 증분 최적성: (U→L/U→D/스왑)을 통한 모든 (ΔL,ΔD)=(1,1) 조합은 위 3케이스의 선형결합으로 표현됩니다. 반대 방향 스왑의 동시 발생은 제거가능(교환 논법)하며, 각 단계에서 최소 증가분 선택이 전역 최적을 훼손하지 않습니다.

## 복잡도
- 시간: O(N log N) — multiset/힙 연산이 단계마다 상수회 발생
- 공간: O(N)

## 구현 (C++)
```cpp
// 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
#include <bits/stdc++.h>
using namespace std;

struct Item { long long l, d; };

int main(){
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int N; if(!(cin>>N)) return 0; int M=2*N;
	vector<Item> a(M); for(int i=0;i<M;++i) cin>>a[i].l>>a[i].d;

	multiset<pair<long long,int>> U_by_l, U_by_d; // (l,i), (d,i)
	multiset<pair<long long,int>> L_sw, D_sw;     // (d-l,i), (l-d,i)
	vector<char> inU(M,1), inL(M,0), inD(M,0);
	for(int i=0;i<M;++i){ U_by_l.insert({a[i].l,i}); U_by_d.insert({a[i].d,i}); }

	auto erase_U = [&](int id){ if(!inU[id]) return; inU[id]=0; U_by_l.erase(U_by_l.find({a[id].l,id})); U_by_d.erase(U_by_d.find({a[id].d,id})); };
	auto move_U_to_L = [&](int id){ erase_U(id); inL[id]=1; L_sw.insert({a[id].d-a[id].l,id}); };
	auto move_U_to_D = [&](int id){ erase_U(id); inD[id]=1; D_sw.insert({a[id].l-a[id].d,id}); };
	auto move_D_to_L = [&](int id){ if(!inD[id]) return; inD[id]=0; D_sw.erase(D_sw.find({a[id].l-a[id].d,id})); inL[id]=1; L_sw.insert({a[id].d-a[id].l,id}); };
	auto move_L_to_D = [&](int id){ if(!inL[id]) return; inL[id]=0; L_sw.erase(L_sw.find({a[id].d-a[id].l,id})); inD[id]=1; D_sw.insert({a[id].l-a[id].d,id}); };

	auto pick_min_two_distinct = [&](long long &cost,int &idL,int &idD){
		if(U_by_l.empty()||U_by_d.empty()) return false; auto il=*U_by_l.begin(); auto id=*U_by_d.begin();
		if(il.second!=id.second){ cost=il.first+id.first; idL=il.second; idD=id.second; return true; }
		long long best=LLONG_MAX; int pL=-1,pD=-1; auto it=U_by_l.begin(); ++it; if(it!=U_by_l.end()){ long long c=it->first+id.first; if(c<best){best=c;pL=it->second;pD=id.second;} }
		auto jt=U_by_d.begin(); ++jt; if(jt!=U_by_d.end()){ long long c=il.first+jt->first; if(c<best){best=c;pL=il.second;pD=jt->second;} }
		if(best==LLONG_MAX) return false; cost=best; idL=pL; idD=pD; return true; };

	long long total=0; vector<long long> ans(N+1);
	for(int k=1;k<=N;++k){
		const long long INF=(1LL<<62);
		long long c1=INF,c2=INF,c3=INF; int uL=-1,uD=-1, vDL=-1, x1=-1,x2=-1, wLD=-1, y1=-1,y2=-1;
		// 1) U->L + U->D
		{
			long long c; int idL,idD; if(pick_min_two_distinct(c,idL,idD)){ c1=c; uL=idL; uD=idD; }
		}
		// 2) D->L + U->D + U->D
		if(!D_sw.empty() && U_by_d.size()>=2){ auto it=U_by_d.begin(); auto p1=*it; ++it; auto p2=*it; auto sw=*D_sw.begin(); c2=p1.first+p2.first+sw.first; vDL=sw.second; x1=p1.second; x2=p2.second; }
		// 3) L->D + U->L + U->L
		if(!L_sw.empty() && U_by_l.size()>=2){ auto it=U_by_l.begin(); auto p1=*it; ++it; auto p2=*it; auto sw=*L_sw.begin(); c3=p1.first+p2.first+sw.first; wLD=sw.second; y1=p1.second; y2=p2.second; }

		long long best=c1; int typ=1; if(c2<best){best=c2;typ=2;} if(c3<best){best=c3;typ=3;}
		if(typ==1){ move_U_to_L(uL); move_U_to_D(uD); }
		else if(typ==2){ move_D_to_L(vDL); move_U_to_D(x1); move_U_to_D(x2); }
		else { move_L_to_D(wLD); move_U_to_L(y1); move_U_to_L(y2); }
		total+=best; ans[k]=total;
	}
	for(int i=1;i<=N;++i) cout<<ans[i]<<'\n';
	return 0;
}
```

## 구현 (Python)
```python
# 더 많은 정보는 42jerrykim.github.io 에서 확인하세요.
import sys, heapq
input = sys.stdin.readline

def solve():
    N = int(input().strip())
    M = 2 * N
    L = [0]*M
    D = [0]*M
    for i in range(M):
        l, d = map(int, input().split())
        L[i] = l; D[i] = d

    # U 힙: (값, id). lazy deletion을 위해 살아있는지 체크 집합 유지
    U_by_l = [(L[i], i) for i in range(M)]
    U_by_d = [(D[i], i) for i in range(M)]
    heapq.heapify(U_by_l)
    heapq.heapify(U_by_d)

    aliveU = [True]*M

    # 스왑 힙 (증가비용, id)
    L_sw = []  # (D[i]-L[i], i)
    D_sw = []  # (L[i]-D[i], i)
    inL = [False]*M
    inD = [False]*M

    def eraseU(i):
        if aliveU[i]:
            aliveU[i] = False

    def move_U_to_L(i):
        eraseU(i)
        inL[i] = True
        heapq.heappush(L_sw, (D[i]-L[i], i))

    def move_U_to_D(i):
        eraseU(i)
        inD[i] = True
        heapq.heappush(D_sw, (L[i]-D[i], i))

    def move_D_to_L(i):
        if not inD[i]: return
        inD[i] = False
        heapq.heappush(L_sw, (D[i]-L[i], i))

    def move_L_to_D(i):
        if not inL[i]: return
        inL[i] = False
        heapq.heappush(D_sw, (L[i]-D[i], i))

    def pop_clean(heap, valid):
        # valid: callable(id)->bool
        while heap and not valid(heap[0][1]):
            heapq.heappop(heap)
        return heap[0] if heap else None

    def valid_U(i):
        return i >= 0 and aliveU[i]

    def type1():
        # U에서 서로 다른 두 아이템으로 U->L, U->D
        a = pop_clean(U_by_l, valid_U)
        b = pop_clean(U_by_d, valid_U)
        if not a or not b: return None
        if a[1] != b[1]:
            return (a[0] + b[0], ('uL', a[1]), ('uD', b[1]))
        # 겹치면 두 번째 후보 사용: 임시 pop 후 복구
        x = heapq.heappop(U_by_l)
        y = heapq.heappop(U_by_d)
        a2 = pop_clean(U_by_l, valid_U)
        b2 = pop_clean(U_by_d, valid_U)
        cand = []
        if a2: cand.append((a2[0] + y[0], ('uL', a2[1]), ('uD', y[1])))
        if b2: cand.append((x[0] + b2[0], ('uL', x[1]), ('uD', b2[1])))
        heapq.heappush(U_by_l, x)
        heapq.heappush(U_by_d, y)
        if not cand: return None
        return min(cand, key=lambda t: t[0])

    def type2():
        # D->L + U->D + U->D
        picks = []
        popped = []
        for _ in range(2):
            b = pop_clean(U_by_d, valid_U)
            if not b:
                for z in popped: heapq.heappush(U_by_d, z)
                return None
            z = heapq.heappop(U_by_d)
            popped.append(z)
            picks.append(z)
        sw = pop_clean(D_sw, lambda i: inD[i])
        for z in popped: heapq.heappush(U_by_d, z)
        if not sw: return None
        cost = picks[0][0] + picks[1][0] + sw[0]
        return (cost, ('dL', sw[1]), ('uD', picks[0][1]), ('uD', picks[1][1]))

    def type3():
        # L->D + U->L + U->L
        picks = []
        popped = []
        for _ in range(2):
            a0 = pop_clean(U_by_l, valid_U)
            if not a0:
                for z in popped: heapq.heappush(U_by_l, z)
                return None
            z = heapq.heappop(U_by_l)
            popped.append(z)
            picks.append(z)
        sw = pop_clean(L_sw, lambda i: inL[i])
        for z in popped: heapq.heappush(U_by_l, z)
        if not sw: return None
        cost = picks[0][0] + picks[1][0] + sw[0]
        return (cost, ('lD', sw[1]), ('uL', picks[0][1]), ('uL', picks[1][1]))

    total = 0
    ans = [0]*(N+1)
    for k in range(1, N+1):
        cands = []
        t1 = type1()
        if t1: cands.append(t1)
        t2 = type2()
        if t2: cands.append(t2)
        t3 = type3()
        if t3: cands.append(t3)
        best = min(cands, key=lambda t: t[0])
        total += best[0]
        for op in best[1:]:
            if op[0] == 'uL': move_U_to_L(op[1])
            elif op[0] == 'uD': move_U_to_D(op[1])
            elif op[0] == 'dL': move_D_to_L(op[1])
            elif op[0] == 'lD': move_L_to_D(op[1])
        ans[k] = total

    print('\n'.join(map(str, ans[1:])))

if __name__ == "__main__":
    solve()
```

## 코너 케이스 체크리스트
- N=1, 2: 초기 단계에서 스왑 힙이 비어 있는 상황 처리(케이스1만 고려)
- `min(l)`와 `min(d)`가 같은 아이템인 경우: 케이스1에서 두 번째 후보 사용
- 동일 가격/대량 동률: multiset/heap로 안정 처리
- 큰 입력: O(N log N), 64-bit 합계(`long long`) 사용
- 스왑 후 상태 갱신 누락 방지: L↔D 이동 시 대응 힙에서 제거/추가 일관성 유지

## 참고자료/유사문제
- 문제: https://www.acmicpc.net/problem/17169
- 잔여 그래프/증분 해석 관련 메모: LP 최적화 글의 "Eat Economically" 단락

